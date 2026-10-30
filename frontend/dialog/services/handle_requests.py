"""
handle_requests.py - API layer + UI update handlers for the Streamlit client.

Backend routes used (same as the PyQt client):
    POST /auth/register, POST /auth/login, GET /auth/me
    POST /documents/upload, GET /documents, GET /documents/{id}, DELETE /documents/{id}
    POST /chat (SSE: session | status | token | sources | done | error)
    GET /chat/sessions, GET /chat/sessions/{id}/messages
    PATCH /chat/sessions/{id}, DELETE /chat/sessions/{id}

State lives in st.session_state (one per browser tab).
"""
import json
import os
import re
import time
from pathlib import Path

import requests
import streamlit as st

import html
from datetime import datetime, timezone
import streamlit.components.v1 as components

MODELS = [m.strip() for m in os.getenv("RAG_MODELS", "gpt-4o-mini,gpt-4o,gpt-5").split(",") if m.strip()]
AI_AVATAR = ":material/auto_awesome:"
USER_AVATAR = ":material/person:"

# ── Configuration ──────────────────────────────────────────────────────────────
API_BASE_URL = os.getenv("RAG_API_URL", "http://127.0.0.1:8000").rstrip("/")
ALLOWED_EXTS = {".pdf", ".docx", ".txt", ".md"}
MAX_UPLOAD_MB = 20

# Keeps you logged in across browser refreshes, like the desktop app did.
# This is ONE file shared by every visitor, so set RAG_PERSIST_TOKEN=0 if the
# Streamlit server is ever shared by more than one person.
TOKEN_FILE = Path(__file__).resolve().parents[1] / "auth_token.x"
PERSIST_TOKEN = os.getenv("RAG_PERSIST_TOKEN", "1") == "1"


def _url(path: str) -> str:
    return f"{API_BASE_URL}{path}"


# ── Session state / token ──────────────────────────────────────────────────────
def _read_token_file() -> str:
    if not PERSIST_TOKEN:
        return ""
    try:
        return TOKEN_FILE.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return ""


def _write_token_file(token: str) -> None:
    if PERSIST_TOKEN:
        TOKEN_FILE.write_text(token, encoding="utf-8")


def init_state() -> None:
    ss = st.session_state
    if "initialized" in ss:
        return
    ss.initialized = True
    ss.token = _read_token_file()
    ss.user = None
    ss.messages = []            # [{"role","content","sources","attachment"?,"doc_ids"?}]
    ss.current_chat_id = None
    ss.chats, ss.docs = [], []
    ss.upload_nonce = 0
    ss.server_down = False
    ss.flash = None
    # preferences (Settings > General)
    ss.theme, ss.language = "System", "English"
    ss.font_size, ss.compact = "Default", False
    ss.show_avatars, ss.show_sources = True, True
    ss.model = MODELS[0]
    # transient UI state
    ss.inflight = None          # partial answer while streaming (survives Stop)
    ss.regen, ss.queued_prompt = False, None
    ss.confirm_delete, ss.open_settings = None, False
    ss.feedback = {}            # {message_index: "up" | "down"}
    ss.search = ""


def _clear_session(message: str | None = None) -> None:
    ss = st.session_state
    ss.token, ss.user = "", None
    ss.messages, ss.current_chat_id = [], None
    ss.chats, ss.docs = [], []
    ss.flash = message
    _write_token_file("")


def logout() -> None:
    _clear_session()


# ── Response helpers ───────────────────────────────────────────────────────────
def _normalize(response) -> dict:
    """{"status_code", **json_body}  or  {"status_code", "data": json_list}."""
    result = {"status_code": response.status_code}
    try:
        body = response.json()
    except ValueError:
        body = None
    if isinstance(body, dict):
        result.update(body)
    elif body is not None:
        result["data"] = body
    return result


def _offline(detail="Server not reachable. Is the backend running?") -> dict:
    return {"status_code": 0, "detail": detail}


def _error_text(result: dict, default="Request failed") -> str:
    detail = result.get("detail")
    if isinstance(detail, str):
        return detail
    if isinstance(detail, list) and detail:
        first = detail[0]
        return first.get("msg", default) if isinstance(first, dict) else str(first)
    return default


def _headers() -> dict:
    token = st.session_state.get("token", "")
    return {"Authorization": f"Bearer {token}"} if token else {}


def api(method: str, path: str, *, json_body=None, files=None, timeout=30) -> dict:
    """One-shot request. Always returns a dict with 'status_code' (0 = offline)."""
    try:
        r = requests.request(method, _url(path), json=json_body, files=files,
                             headers=_headers(), timeout=timeout)
    except requests.exceptions.ConnectionError:
        return _offline()
    except requests.exceptions.RequestException as e:
        return _offline(str(e))
    result = _normalize(r)
    if r.status_code == 401 and st.session_state.get("token"):
        _clear_session("Your session expired. Please log in again.")
    return result


# ── Auth ───────────────────────────────────────────────────────────────────────
def ensure_login() -> bool:
    """True when we have a verified user. Verifies a saved token once per session."""
    ss = st.session_state
    if ss.user:
        return True
    if not ss.token:
        return False
    r = api("GET", "/auth/me")
    code = r["status_code"]
    if code == 200:
        ss.user = {"id": r.get("id"), "username": r.get("username")}
        ss.server_down = False
        load_chat_history()
        load_documents()
        return True
    if code == 0:
        ss.server_down = True          # keep the token; backend is just down
        return False
    _clear_session("Token rejected. Please log in again.")
    return False


def signup(username: str, password: str) -> tuple[bool, str]:
    username = username.strip()
    if not username or not password:
        return False, "username or password can't be empty"
    if not re.fullmatch(r"[A-Za-z0-9_.-]{3,50}", username):
        return False, "username must be 3-50 characters: letters, digits, _ . -"
    if len(password) < 8:
        return False, "password must contain at least 8 characters"
    if not re.search(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\W)", password):
        return False, "password must contain at least 1 upper case, lower case and a special symbol"

    r = api("POST", "/auth/register", json_body={"username": username, "password": password})
    code = r["status_code"]
    if code == 201:
        return True, "User registered, go to the Log in tab!"
    if code == 409:
        return False, "Username already taken"
    if code == 422:
        return False, "Invalid username or password"
    if code == 0:
        return False, "Server not reachable"
    return False, _error_text(r, "Internal server error")


def login(username: str, password: str) -> tuple[bool, str]:
    username = username.strip().lower()
    if not username or not password:
        return False, "username or password can't be empty"
    r = api("POST", "/auth/login", json_body={"username": username, "password": password})
    if "access_token" in r:
        ss = st.session_state
        ss.token = r["access_token"]
        _write_token_file(ss.token)
        ss.user = {"id": r["user"]["id"], "username": r["user"]["username"]}
        ss.flash, ss.server_down = None, False
        load_chat_history()
        load_documents()
        return True, ""
    code = r["status_code"]
    if code == 0:
        return False, "Server not reachable"
    if code == 401:
        return False, "Invalid credentials"
    return False, _error_text(r, "Login failed")


# ── Chat history (sidebar) ─────────────────────────────────────────────────────
def load_chat_history() -> None:
    r = api("GET", "/chat/sessions")
    if r["status_code"] == 200:
        st.session_state.chats = r.get("data", [])


def new_chat() -> None:
    st.session_state.messages = []
    st.session_state.current_chat_id = None


def open_chat(chat_id: int) -> None:
    r = api("GET", f"/chat/sessions/{chat_id}/messages")
    if r["status_code"] != 200:
        st.toast(_error_text(r))
        return
    st.session_state.messages = [
        {"role": "user" if m["role"] == "user" else "assistant",
         "content": m["content"], "sources": m.get("sources") or []}
        for m in r.get("data", [])]
    st.session_state.current_chat_id = chat_id
    st.session_state.feedback = {}


def rename_chat(chat_id: int, input_key: str) -> None:
    title = st.session_state.get(input_key, "").strip()[:120]   # backend limit: 120
    if not title:
        return
    r = api("PATCH", f"/chat/sessions/{chat_id}", json_body={"title": title})
    if r["status_code"] == 200:
        load_chat_history()
    else:
        st.toast(_error_text(r))


def delete_chat(chat_id: int) -> None:
    r = api("DELETE", f"/chat/sessions/{chat_id}")
    if r["status_code"] == 204:
        if st.session_state.current_chat_id == chat_id:
            new_chat()
        load_chat_history()
    else:
        st.toast(_error_text(r))


# ── Documents ──────────────────────────────────────────────────────────────────
def load_documents() -> None:
    r = api("GET", "/documents")
    if r["status_code"] == 200:
        st.session_state.docs = r.get("data", [])


def delete_document(doc_id: int) -> None:
    r = api("DELETE", f"/documents/{doc_id}")
    if r["status_code"] != 204:
        st.toast(f"Delete failed: {_error_text(r)}")
    load_documents()


def _validate_upload(name: str, size: int) -> str | None:
    ext = os.path.splitext(name)[1].lower()
    if ext not in ALLOWED_EXTS:
        return f"'{ext or name}' is not supported. Supported types: PDF, DOCX, TXT, MD."
    if size == 0:
        return f"'{name}' is empty."
    if size > MAX_UPLOAD_MB * 1024 * 1024:
        return f"'{name}' is {size // (1024 * 1024)} MB. The limit is {MAX_UPLOAD_MB} MB."
    return None


def upload_document(name: str, data: bytes, on_progress=None, poll_interval=1.0, timeout=300) -> dict:
    """Upload, then poll GET /documents/{id} until indexing finishes (ready|failed)."""
    err = _validate_upload(name, len(data))
    if err:
        return {"status_code": 400, "detail": err}
    if on_progress:
        on_progress("uploading")
    r = api("POST", "/documents/upload", files={"file": (name, data)}, timeout=(5, 120))
    if r["status_code"] != 202:
        return r

    doc_id = r["id"]
    if on_progress:
        on_progress("indexing")
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        time.sleep(poll_interval)
        r = api("GET", f"/documents/{doc_id}", timeout=15)
        if r["status_code"] != 200 or r.get("status") != "processing":
            return r
    return {"status_code": 504, "id": doc_id,
            "detail": "Indexing is taking longer than expected. It keeps running in the background."}


def _upload_outcome(result: dict, name: str) -> tuple[int | None, str | None]:
    """-> (doc_id, None) on success, (None, error_text) on failure. Cleans up failed docs."""
    code, status = result.get("status_code"), result.get("status")
    if code == 200 and status == "ready":
        load_documents()
        return result["id"], None
    if code == 200 and status == "failed":
        api("DELETE", f"/documents/{result['id']}")       # don't leave a broken row behind
        load_documents()
        return None, f"Could not index '{name}': {result.get('error') or 'Unknown error'}"
    if code == 504:
        load_documents()
    return None, _error_text(result, f"Could not upload '{name}'")


def upload_to_library(uploaded_file) -> tuple[bool, str]:
    """Settings > Documents: upload only, no chat attachment."""
    res = upload_document(uploaded_file.name, uploaded_file.getvalue())
    doc_id, err = _upload_outcome(res, uploaded_file.name)
    return (True, f"Indexed {uploaded_file.name}") if doc_id else (False, err)


# ── Streaming chat ─────────────────────────────────────────────────────────────
def iter_sse(lines):
    """Parse raw SSE lines (bytes or str) into (event, data_dict) pairs."""
    event, data_lines = "message", []
    for raw in lines:
        line = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else raw
        if line == "":
            if data_lines:
                payload = "\n".join(data_lines)
                try:
                    data = json.loads(payload)
                except ValueError:
                    data = {"raw": payload}
                yield event, data
            event, data_lines = "message", []
        elif line.startswith(":"):
            continue
        elif line.startswith("event:"):
            event = line[6:].strip()
        elif line.startswith("data:"):
            data_lines.append(line[5:][1:] if line[5:6] == " " else line[5:])
    if data_lines:
        try:
            yield event, json.loads("\n".join(data_lines))
        except ValueError:
            pass


def _sources_footer(sources, answer: str = "") -> str:
    """Markdown 'Sources' list, only for chunks the answer actually cited as [n]."""
    if not sources or not answer:
        return ""
    cited = set()
    for group in re.findall(r"\[(\d+(?:\s*,\s*\d+)*)\]", answer):
        cited.update(int(n) for n in re.findall(r"\d+", group))
    sources = [s for s in sources if s.get("ref") in cited]
    if not sources:
        return ""

    grouped = {}
    for s in sources:
        grouped.setdefault((s.get("filename", "unknown"), s.get("page")), []).append(s.get("ref"))
    lines = []
    for (filename, page), refs in grouped.items():
        page_txt = f", p. {page}" if page else ""
        lines.append(f"- **[{', '.join(str(r) for r in refs)}]** {filename}{page_txt}")
    return "\n\n---\n\n**Sources**\n\n" + "\n".join(lines)


# ── Small state callbacks ──────────────────────────────────────────────────────
def request_regenerate() -> None:
    st.session_state.regen = True


def queue_prompt(text: str) -> None:
    st.session_state.queued_prompt = text


def ask_delete(chat_id) -> None:
    st.session_state.confirm_delete = chat_id


def request_settings() -> None:
    st.session_state.open_settings = True


def set_feedback(idx: int, value: str) -> None:
    fb = st.session_state.feedback
    fb[idx] = None if fb.get(idx) == value else value       # click again to undo


def current_chat_title() -> str:
    ss = st.session_state
    for c in ss.chats:
        if c["id"] == ss.current_chat_id:
            return c["title"]
    return "New chat"


def transcript_md() -> str:
    out = [f"# {current_chat_title()}\n"]
    for m in st.session_state.messages:
        out.append(f"**{'You' if m['role'] == 'user' else 'Assistant'}:**\n\n{m['content']}\n")
    return "\n".join(out)


# ── Sidebar grouping ───────────────────────────────────────────────────────────
def _local_dt(s: str) -> datetime:
    try:
        dt = datetime.fromisoformat(s)
    except (TypeError, ValueError):
        return datetime.now().astimezone()
    if dt.tzinfo is None:                       # backend stores naive UTC
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone()


def group_chats(chats: list, query: str = "") -> list[tuple[str, list]]:
    q, today = query.strip().lower(), datetime.now().astimezone().date()
    buckets = {"Today": [], "Yesterday": [], "Previous 7 Days": [], "Previous 30 Days": [], "Older": []}
    for c in chats:
        if q and q not in c["title"].lower():
            continue
        d = (today - _local_dt(c.get("updated_at", "")).date()).days
        key = ("Today" if d <= 0 else "Yesterday" if d == 1 else "Previous 7 Days" if d <= 7
               else "Previous 30 Days" if d <= 30 else "Older")
        buckets[key].append(c)
    return [(k, v) for k, v in buckets.items() if v]


# ── Streaming chat ─────────────────────────────────────────────────────────────
def _thinking(text: str = "") -> str:
    label = f'<span class="think-label">{html.escape(text)}</span>' if text else ""
    return f'<div class="typing"><span></span><span></span><span></span>{label}</div>'


def _stream_tokens(payload: dict, ctx: dict, status_ph):
    """Generator for st.write_stream. Mirrors tokens into ss.inflight so Stop can keep the partial."""
    ss = st.session_state
    r = None
    try:
        r = requests.post(_url("/chat"), json=payload, headers=_headers(),
                          stream=True, timeout=(5, 120))
        if r.status_code == 401:
            ctx["auth_failed"] = True
            return
        if r.status_code != 200:
            ctx["error"] = _error_text(_normalize(r), f"Server returned HTTP {r.status_code}")
            return

        got_token = False
        for event, data in iter_sse(r.iter_lines(chunk_size=1)):
            if event == "session":
                ss.current_chat_id = data["session_id"]
            elif event == "status":
                if not got_token:
                    status_ph.markdown(_thinking(data.get("text", "")), unsafe_allow_html=True)
            elif event == "token":
                if not got_token:
                    got_token = True
                    status_ph.empty()
                text = data.get("text", "")
                ss.inflight["text"] += text
                yield text
            elif event == "sources":
                ctx["sources"] = data.get("sources", [])
            elif event == "done":
                break
            elif event == "error":
                ctx["error"] = data.get("detail", "Unknown error")
                break
    except requests.exceptions.ConnectionError:
        ctx["error"] = "Server not reachable. Is the backend running?"
    except Exception as e:
        ctx["error"] = f"Connection error: {e}"
    finally:
        status_ph.empty()
        if r is not None:
            r.close()


def finalize_interrupted() -> None:
    """Call at the top of every run: if the previous run was cut off (Stop / new click), keep the partial."""
    ss = st.session_state
    inf = ss.inflight
    if inf is None:
        return
    ss.inflight = None
    text = inf["text"].strip()
    ss.messages.append({
        "role": "assistant", "sources": [],
        "content": f"{text}\n\n*— generation stopped —*" if text else "*Generation stopped.*"})
    load_chat_history()


def send_prompt(text: str, uploaded=None, append_user: bool = True, doc_ids=None) -> None:
    """Render the user turn, optionally index+attach a file, stream the answer, save it."""
    ss = st.session_state
    if append_user:
        msg = {"role": "user", "content": text}
        if uploaded is not None:
            msg["attachment"] = uploaded.name
        ss.messages.append(msg)
        render_message(msg, len(ss.messages) - 1)
    else:
        msg = ss.messages[-1]               # regenerate: reuse the last user turn

    with st.chat_message("assistant", avatar=AI_AVATAR):
        if uploaded is not None:
            with st.status(f"Indexing {uploaded.name}…", expanded=False) as status:
                res = upload_document(
                    uploaded.name, uploaded.getvalue(),
                    on_progress=lambda s: status.update(
                        label=("Uploading " if s == "uploading" else "Indexing ") + uploaded.name + "…"))
                doc_id, err = _upload_outcome(res, uploaded.name)
                status.update(label="Document ready" if doc_id else "Upload failed",
                              state="complete" if doc_id else "error")
            if doc_id is None:
                if not ss.token:            # 401 during upload
                    st.rerun()
                ss.messages.append({"role": "assistant", "content": f"⚠️ {err}", "sources": []})
                st.rerun()
            doc_ids = [doc_id]
            msg["doc_ids"] = doc_ids        # so Regenerate stays scoped to this file

        payload = {"message": text, "session_id": ss.current_chat_id, "model": ss.model}
        if doc_ids:
            payload["doc_ids"] = doc_ids

        ss.inflight = {"text": ""}
        ctx = {"sources": [], "error": None, "auth_failed": False}
        with st.container(key="stopbar"):
            st.button("■  Stop generating", key="stop_btn")     # clicking reruns -> interrupts the stream
        status_ph = st.empty()
        status_ph.markdown(_thinking(), unsafe_allow_html=True)
        answer = st.write_stream(_stream_tokens(payload, ctx, status_ph)) or ""

    ss.inflight = None
    if ctx["auth_failed"]:
        _clear_session("Your session expired. Please log in again.")
        st.rerun()
    if ctx["error"]:
        answer = (answer + f"\n\n⚠️ {ctx['error']}").strip()
    ss.messages.append({"role": "assistant", "content": answer, "sources": ctx["sources"]})
    load_chat_history()
    st.rerun()


# ── UI renderers ───────────────────────────────────────────────────────────────
_COPY_ICON = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
              'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
              '<rect width="14" height="14" x="8" y="8" rx="2"/>'
              '<path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>')


def _copy_button(text: str) -> None:
    payload = json.dumps(text).replace("</", "<\\/")
    components.html(f"""
<style>html,body{{margin:0;background:transparent}}
button{{width:32px;height:32px;border:0;border-radius:8px;background:transparent;cursor:pointer;
color:#8e8e8e;display:flex;align-items:center;justify-content:center;font-size:14px}}
button:hover{{background:rgba(128,128,128,.2)}}</style>
<button id="b" title="Copy" aria-label="Copy">{_COPY_ICON}</button>
<script>
const t={payload}, b=document.getElementById('b'), icon=b.innerHTML;
b.onclick=async()=>{{
  try{{await navigator.clipboard.writeText(t)}}catch(e){{
    const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();
    document.execCommand('copy');a.remove()}}
  b.textContent='✓';setTimeout(()=>b.innerHTML=icon,1500)}};
</script>""", height=34, width=34)


def _action_bar(m: dict, idx: int) -> None:
    ss = st.session_state
    fb = ss.feedback.get(idx)
    is_last = idx == len(ss.messages) - 1
    with st.container(key=f"actions_{idx}"):
        c = st.columns(5, gap="small")
        with c[0]:
            _copy_button(m["content"])
        c[1].button("", icon=":material/refresh:", key=f"regen_{idx}", help="Regenerate",
                    on_click=request_regenerate, disabled=not is_last)
        c[2].button("", icon=":material/thumb_up:", key=f"up_{idx}", help="Good response",
                    type="primary" if fb == "up" else "secondary", on_click=set_feedback, args=(idx, "up"))
        c[3].button("", icon=":material/thumb_down:", key=f"down_{idx}", help="Bad response",
                    type="primary" if fb == "down" else "secondary", on_click=set_feedback, args=(idx, "down"))
        with c[4].popover("", icon=":material/ios_share:", help="Share"):
            st.caption("Export this conversation")
            st.download_button("Download as Markdown", transcript_md(), file_name="chat.md",
                               mime="text/markdown", key=f"dl_{idx}", icon=":material/download:",
                               use_container_width=True)


def render_message(m: dict, idx: int) -> None:
    ss = st.session_state
    is_ai = m["role"] == "assistant"
    with st.chat_message(m["role"], avatar=AI_AVATAR if is_ai else USER_AVATAR):
        if is_ai:
            st.markdown(m["content"] + (_sources_footer(m.get("sources") or [], m["content"])
                                        if ss.show_sources else ""))
            _action_bar(m, idx)
        else:
            with st.container(key=f"umsg_{idx}"):      # marker used by the CSS to right-align the bubble
                if m.get("attachment"):
                    st.markdown(f'<span class="chip">📎 {html.escape(m["attachment"])}</span>',
                                unsafe_allow_html=True)
                st.markdown(m["content"])


def render_messages() -> None:
    for i, m in enumerate(st.session_state.messages):
        render_message(m, i)


def scroll_to_bottom() -> None:
    components.html("""<script>
const d = window.parent.document;
const el = d.querySelector('[data-testid="stMain"]') || d.querySelector('section.main');
if (el) el.scrollTo({top: el.scrollHeight, behavior: 'smooth'});
</script>""", height=0)


_STATUS = {"ready": ("✅", "ready"), "processing": ("⏳", "processing"), "failed": ("❗", "failed")}


def _fmt_size(n: int) -> str:
    for unit in ("B", "KB", "MB"):
        if n < 1024 or unit == "MB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024


def render_doc_row(doc: dict) -> None:
    doc_id = doc["id"]
    icon, label = _STATUS.get(doc.get("status"), ("•", doc.get("status", "")))
    c_ext, c_name, c_stat, c_del = st.columns([1.2, 6, 2, 1.2], vertical_alignment="center")
    c_ext.markdown(f"`{(doc.get('file_type') or '').upper() or 'FILE'}`")
    meta = [f"{doc.get('chunk_count', 0)} chunks"] if doc.get("status") == "ready" else [label.capitalize()]
    meta.append(_fmt_size(doc.get("size_bytes", 0)))
    c_name.markdown(f"**{html.escape(doc.get('filename', 'unknown'))}**  \n<small>{' · '.join(meta)}</small>",
                    unsafe_allow_html=True, help=doc.get("error") or None)
    c_stat.markdown(f"{icon} {label}")
    with c_del.popover("✕"):
        st.caption("Delete this file?")
        st.button("Delete", key=f"del_{doc_id}", type="primary", on_click=delete_document, args=(doc_id,))