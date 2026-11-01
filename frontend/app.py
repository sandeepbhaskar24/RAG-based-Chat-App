import html

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="AI Assistant", page_icon="✨", layout="wide",
                   initial_sidebar_state="expanded")

from dialog.services import handle_requests as hr
from dialog.styles import build_css

hr.init_state()
ss = st.session_state
st.markdown(build_css(ss.theme, ss.font_size, ss.compact, ss.get("sidebar_open", True)),
            unsafe_allow_html=True)

FILE_TYPES = [e.lstrip(".") for e in sorted(hr.ALLOWED_EXTS)]
LANGUAGES = ["English", "Español", "Français", "Deutsch", "हिन्दी", "日本語"]
SKELETON = '<div class="skel"></div>' * 5


def install_shortcuts():
    """Ctrl/Cmd+K focuses the sidebar search box."""
    components.html("""<script>
const w = window.parent, d = w.document;
const disableSearchAutofill = () => {
  const el = d.querySelector('[data-testid="stSidebar"] input[aria-label="Search chats"]');
  if (el) {
    el.setAttribute('autocomplete', 'off');
    el.setAttribute('autocorrect', 'off');
    el.setAttribute('autocapitalize', 'none');
    el.setAttribute('spellcheck', 'false');
    el.setAttribute('name', 'chat-history-search-no-autofill');
  }
};
disableSearchAutofill();
if (!w.__ragSearchObserver) {
  w.__ragSearchObserver = new MutationObserver(disableSearchAutofill);
  w.__ragSearchObserver.observe(d, {childList: true, subtree: true});
}
if (w.__ragKey) d.removeEventListener('keydown', w.__ragKey, true);
w.__ragKey = (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
    const el = d.querySelector('[data-testid="stSidebar"] input[aria-label="Search chats"]');
    if (el) { e.preventDefault(); el.focus(); el.select(); }
  }
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'b') {
    e.preventDefault();
    const toggle = d.querySelector('[data-testid="stSidebar"] .st-key-sb_collapse button')
      || d.querySelector('.st-key-sb_expand button');
    if (toggle) toggle.click();
  }
};
d.addEventListener('keydown', w.__ragKey, true);
</script>""", height=0)


# ── Login / sign-up ────────────────────────────────────────────────────────────
def auth_page():
    st.markdown('<div class="welcome"><h1>AI Assistant</h1><p>Log in to continue</p></div>',
                unsafe_allow_html=True)
    if ss.server_down:
        st.error(f"Could not reach the server at {hr.API_BASE_URL}. Make sure the backend is running.")
        if st.button("Retry"):
            st.rerun()
        return
    if ss.flash:
        st.warning(ss.flash)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        t_login, t_signup = st.tabs(["Log in", "Sign up"])
        with t_login, st.form("login_form"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Log in", use_container_width=True, type="primary"):
                ok, msg = hr.login(u, p)
                if ok:
                    st.rerun()
                st.error(msg)
        with t_signup, st.form("signup_form"):
            u = st.text_input("Username", key="su_user")
            p = st.text_input("Password", type="password", key="su_pass")
            if st.form_submit_button("Create account", use_container_width=True, type="primary"):
                ok, msg = hr.signup(u, p)
                (st.success if ok else st.error)(msg)


# ── Dialogs ────────────────────────────────────────────────────────────────────
@st.dialog("Delete chat?")
def delete_dialog(chat_id: int):
    title = next((c["title"] for c in (ss.chats or []) if c["id"] == chat_id), "this chat")
    st.write(f"“{title}” will be permanently deleted. This can't be undone.")
    c1, c2 = st.columns(2)
    if c1.button("Cancel", use_container_width=True):
        st.rerun()
    if c2.button("Delete", type="primary", use_container_width=True):
        hr.delete_chat(chat_id)
        st.rerun()


@st.dialog("Settings", width="large")
def settings_dialog():
    t_gen, t_acc, t_docs = st.tabs(["General", "Account", "Attached documents"])

    with t_gen:
        theme = st.radio("Theme", ["Dark", "Light", "System"], horizontal=True,
                         index=["Dark", "Light", "System"].index(ss.theme), key="theme_ctl")
        ss.language = st.selectbox("Language", LANGUAGES, index=LANGUAGES.index(ss.language), key="lang_ctl")
        st.markdown("**Display**")
        font = st.radio("Text size", ["Small", "Default", "Large"], horizontal=True,
                        index=["Small", "Default", "Large"].index(ss.font_size), key="font_ctl")
        compact = st.toggle("Compact message spacing", value=ss.compact, key="compact_ctl")
        sources = st.toggle("Show sources under answers", value=ss.show_sources, key="sources_ctl")
        new = dict(theme=theme, font_size=font, compact=compact, show_sources=sources)
        if any(ss[k] != v for k, v in new.items()):
            ss.update(new)
            ss.open_settings = True          # reopen after the full rerun that applies the CSS
            st.rerun()

    with t_acc:
        name = ss.user["username"]
        st.markdown(f'<div class="profile"><div class="avatar">{html.escape(name[:2].upper())}</div>'
                    f'<div class="pname"><b>{html.escape(name)}</b><span>User ID {ss.user.get("id")}</span></div></div>',
                    unsafe_allow_html=True)
        if st.button("Log out", icon=":material/logout:", type="primary"):
            hr.logout()
            st.rerun()

    with t_docs:
        hr.load_documents()
        up = st.file_uploader("Upload a file (PDF, DOCX, TXT, MD · max 20 MB)", type=FILE_TYPES,
                              key=f"lib_up_{ss.upload_nonce}")
        if up is not None and st.button("Upload to library", type="primary"):
            with st.spinner("Uploading and indexing…"):
                ok, msg = hr.upload_to_library(up)
            if ok:
                ss.upload_nonce += 1
                st.rerun(scope="fragment")
            else:
                st.error(msg)
        n = len(ss.docs)
        head, refresh = st.columns([4, 1], vertical_alignment="center")
        head.caption(f"{n} document{'s' if n != 1 else ''}")
        if refresh.button("↻ Refresh"):
            st.rerun(scope="fragment")
        if not ss.docs:
            st.info("No documents yet.")
        for d in ss.docs:
            hr.render_doc_row(d)


# ── Sidebar ────────────────────────────────────────────────────────────────────
def sidebar():
    with st.sidebar:
        # One scrollable area contains the header, navigation and chat history.
        with st.container(key="sidebar_scroll"):
            with st.container(key="sb_top"):
                c_brand, c_col = st.columns([5, 1], vertical_alignment="center")
                c_brand.markdown('<div class="brand"><div class="logo"></div>AI Assistant</div>', unsafe_allow_html=True)
                c_col.button("", icon=":material/chevron_left:", key="sb_collapse",
                             help="Collapse sidebar (Ctrl/⌘ + B)", on_click=hr.toggle_sidebar)
                st.button("New Chat", key="new_chat", on_click=hr.new_chat,
                          use_container_width=True, help="Start a fresh conversation")
                with st.container(key="search_wrap"):
                    st.text_input("Search chats", key="search", placeholder="Search chats…",
                                  label_visibility="collapsed",
                                  help="Filter your conversation history (Ctrl/⌘ + K)")
                st.markdown('<div class="side-heading">Your Chats</div>', unsafe_allow_html=True)

            with st.container(key="history"):
                if ss.chats is None:                       # loading state
                    ph = st.empty()
                    ph.markdown(SKELETON, unsafe_allow_html=True)
                    hr.load_chat_history()
                    ph.empty()
                groups = hr.group_chats(ss.chats, ss.search)
                if not ss.chats:
                    st.markdown('<div class="empty-state">No conversations yet.<br>Start a new chat!</div>',
                                unsafe_allow_html=True)
                elif not groups:
                    st.markdown('<div class="empty-state">No chats match your search.</div>', unsafe_allow_html=True)
                for label, chats in groups:
                    st.markdown(f'<div class="group-label">{html.escape(label)}</div>', unsafe_allow_html=True)
                    for chat in chats:
                        cid = chat["id"]
                        active = cid == ss.current_chat_id
                        with st.container(key=f"row_on_{cid}" if active else f"row_{cid}"):
                            c_t, c_m = st.columns([6, 1], vertical_alignment="center")
                            c_t.button(chat["title"], key=f"chat_{cid}", use_container_width=True, help=chat["title"],
                                       on_click=hr.open_chat, args=(cid,))
                            with c_m.popover("⋯", help=f"Actions for {chat['title']}"):
                                rk = f"rn_{cid}"
                                st.text_input("Rename chat", value=chat["title"], key=rk, max_chars=120, label_visibility="visible")
                                st.button("Rename", key=f"rename_{cid}", on_click=hr.rename_chat,
                                          args=(cid, rk), use_container_width=True)
                                st.button("Delete", key=f"delc_{cid}", on_click=hr.ask_delete,
                                          args=(cid,), use_container_width=True)

        with st.container(key="sb_bottom"):
            st.button("Settings", key="open_settings_btn", on_click=hr.request_settings, use_container_width=True, help="Preferences, account and documents")
            name = ss.user["username"]
            st.markdown(f'<div class="profile"><div class="avatar">{html.escape(name[:2].upper())}</div>'
                        f'<div class="pname"><b>{html.escape(name)}</b><span>Signed in</span></div></div>',
                        unsafe_allow_html=True)


# ── Chat area ──────────────────────────────────────────────────────────────────
def _submit(prompt):
    text = (prompt.text or "").strip()
    file = prompt.files[0] if prompt.files else None
    if not text:
        st.toast("Type a message to go with your file.")
        return False
    hr.send_prompt(text, file)
    return True


def chat_area():
    regen = ss.pop("regen", False)
    if regen and ss.messages and ss.messages[-1]["role"] == "assistant":
        ss.messages.pop()

    # ── Welcome screen (empty chat) ──
    if not ss.messages:
        welcome = st.empty()
        with welcome.container():
            st.markdown('<div class="welcome"><h1>What can I help you with?</h1>'
                        '<p>Ask anything, explore ideas, or get things done.</p></div>', unsafe_allow_html=True)
            with st.container():       # chat_input inside a container renders inline (centered)
                prompt = st.chat_input("Message AI Assistant...", accept_file=True,
                                       file_type=FILE_TYPES, key="composer_welcome")
        if prompt:
            welcome.empty()
            _submit(prompt)
        return

    # ── Conversation ──
    hr.render_messages()
    prompt = st.chat_input("Message AI Assistant...", accept_file=True, file_type=FILE_TYPES, key="composer")

    if regen and ss.messages and ss.messages[-1]["role"] == "user":
        last = ss.messages[-1]
        hr.send_prompt(last["content"], None, append_user=False, doc_ids=last.get("doc_ids"))
    elif prompt:
        _submit(prompt)
    else:
        hr.scroll_to_bottom()


# ── Entry ──────────────────────────────────────────────────────────────────────
if not hr.ensure_login():
    auth_page()
    st.stop()

hr.restore_chat_from_url()
hr.finalize_interrupted()
install_shortcuts()
sidebar()
if not ss.get("sidebar_open", True):
    st.button("", icon=":material/chevron_right:", key="sb_expand", help="Open sidebar",
              on_click=hr.toggle_sidebar)

if ss.pop("open_settings", False):
    settings_dialog()
_cid = ss.pop("confirm_delete", None)
if _cid:
    delete_dialog(_cid)

chat_area()