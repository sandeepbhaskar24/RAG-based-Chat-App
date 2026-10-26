"""
handle_requests.py - client-side request / response layer for the RAG Chat app.

Talks to the FastAPI backend (default http://127.0.0.1:8000, override with the
RAG_API_URL environment variable):

    POST   /auth/register                     create account
    POST   /auth/login                        -> {access_token, user}
    GET    /auth/me                           current user
    POST   /documents/upload                  multipart file, indexed in background
    GET    /documents[/{id}]                  list / poll status (processing|ready|failed)
    DELETE /documents/{id}
    POST   /chat                              {message, session_id?, doc_ids?} -> SSE stream
    GET    /chat/sessions                     chat history list
    GET    /chat/sessions/{id}/messages       one conversation
    PATCH  /chat/sessions/{id}                rename
    DELETE /chat/sessions/{id}

Threads:
    WorkerThread      - one-shot JSON requests (auth, lists, rename, delete)
    ChatStreamWorker  - POST /chat and parse the Server-Sent Events stream
    UploadWorker      - upload a file, then poll until it is indexed
"""
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QTimer, QSize, Qt
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtGui, QtWidgets

from termcolor import colored
import json, os, re, time
import requests


# ── Configuration ──────────────────────────────────────────────────────────────
API_BASE_URL = os.getenv("RAG_API_URL", "http://127.0.0.1:8000").rstrip("/")
TOKEN_FILE   = "auth_token.x"

# Must match the backend's ALLOWED_EXTENSIONS / MAX_UPLOAD_MB
ALLOWED_EXTS  = {".pdf", ".docx", ".txt", ".md"}
MAX_UPLOAD_MB = 20

_SUPPORTED_FILTERS = (
    "Documents (*.pdf *.docx *.txt *.md);;"
    "All Files (*)"
)


def _url(path: str) -> str:
    return f"{API_BASE_URL}{path}"


# ── Token helpers ──────────────────────────────────────────────────────────────
# (Add your icacls lock/unlock calls here if you still want them - they were
#  previously repeated at every call site.)

def _read_token() -> str:
    try:
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


def _write_token(token: str) -> None:
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        f.write(token)


def _headers(self=None) -> dict:
    """Authorization header from the token file (also refreshes self.jwt_token)."""
    token = _read_token()
    if self is not None:
        self.jwt_token = token
    return {"Authorization": f"Bearer {token}"} if token else {}


# ── Response helpers ───────────────────────────────────────────────────────────

def _normalize(response) -> dict:
    """
    Turn an HTTP response into a dict the UI handlers can read:
      {"status_code": <http status>, **json_body}         (JSON object bodies)
      {"status_code": <http status>, "data": <json_body>} (JSON list bodies)
    """
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
    """Readable message from FastAPI's {"detail": str | [{"msg": ...}]} errors."""
    detail = result.get("detail")
    if isinstance(detail, str):
        return detail
    if isinstance(detail, list) and detail:
        first = detail[0]
        return first.get("msg", default) if isinstance(first, dict) else str(first)
    return default


def _resolve(method: str, route: str):
    """Map the app's short route names to (method, backend URL)."""
    head, _, tail = route.partition('/')
    if (method, route) == ('POST', 'register'):
        return method, _url('/auth/register')
    if (method, route) == ('POST', 'login'):
        return method, _url('/auth/login')
    if (method, route) == ('GET', 'verify_token'):
        return method, _url('/auth/me')
    if route == 'chats' and method == 'GET':
        return method, _url('/chat/sessions')
    if head == 'chat' and tail:                       # chat/<session_id>
        if method == 'GET':
            return method, _url(f'/chat/sessions/{tail}/messages')
        if method in ('PATCH', 'DELETE'):
            return method, _url(f'/chat/sessions/{tail}')
    if head == 'documents':                           # documents[/<doc_id>]
        if method == 'GET' or (method == 'DELETE' and tail):
            return method, _url('/documents' + (f'/{tail}' if tail else ''))
    raise ValueError(f"Unknown request: {method} {route}")


# ── Worker threads ─────────────────────────────────────────────────────────────

class WorkerThread(QThread):
    """One-shot JSON request. Always emits exactly one dict (see _normalize)."""
    data_fetched = pyqtSignal(dict)

    def __init__(self, data, method, route, headers=None):
        super().__init__()
        self.data    = data
        self.method  = method
        self.route   = route
        self.headers = headers

    def run(self):
        try:
            method, url = _resolve(self.method, self.route)
            response = requests.request(
                method, url, json=self.data, headers=self.headers, timeout=30)
            self.data_fetched.emit(_normalize(response))
        except requests.exceptions.ConnectionError:
            print(colored('Connection Error: Server not reachable', 'red'))
            self.data_fetched.emit(_offline())
        except requests.exceptions.RequestException as e:
            print(colored(f'Connection Error: {e}', 'red'))
            self.data_fetched.emit(_offline(str(e)))
        except ValueError as e:
            print(colored(str(e), 'red'))
            self.data_fetched.emit({"status_code": 0, "detail": str(e)})


def iter_sse(lines):
    """
    Parse raw Server-Sent-Event lines (bytes or str) into (event, data) pairs.
    `data` is the decoded JSON payload. Blank lines terminate an event.
    """
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
        elif line.startswith(":"):            # comment / keep-alive
            continue
        elif line.startswith("event:"):
            event = line[6:].strip()
        elif line.startswith("data:"):
            data_lines.append(line[5:][1:] if line[5:6] == " " else line[5:])
    if data_lines:                            # stream ended without a final blank line
        try:
            yield event, json.loads("\n".join(data_lines))
        except ValueError:
            pass


class ChatStreamWorker(QThread):
    """
    POST /chat and re-emit the SSE events as Qt signals:
        session  -> session_received({"session_id", "title"})
        token    -> token_received(text)            (many)
        sources  -> sources_received([{ref, doc_id, filename, page, snippet, score}])
        done     -> stream_done({"message_id"})
        error    -> stream_error(message)
    A 401 emits auth_failed instead. stop() aborts the request immediately.
    """
    session_received = pyqtSignal(dict)
    token_received   = pyqtSignal(str)
    sources_received = pyqtSignal(list)
    stream_done      = pyqtSignal(dict)
    stream_error     = pyqtSignal(str)
    auth_failed      = pyqtSignal()

    def __init__(self, payload, headers=None):
        super().__init__()
        self.payload   = payload
        self.headers   = headers
        self._stop     = False
        self._response = None

    def stop(self):
        self._stop = True
        resp = self._response
        if resp is not None:
            try:
                resp.close()          # unblocks the read in run()
            except Exception:
                pass

    def run(self):
        try:
            self._response = requests.post(
                _url('/chat'), json=self.payload, headers=self.headers,
                stream=True, timeout=(5, 120))
            r = self._response

            if r.status_code == 401:
                self.auth_failed.emit()
                return
            if r.status_code != 200:
                result = _normalize(r)
                self.stream_error.emit(
                    _error_text(result, f"Server returned HTTP {r.status_code}"))
                return

            # chunk_size=1 so each SSE line is delivered the moment it arrives.
            # Iterate raw bytes (not decode_unicode) so U+2028 etc. inside a
            # token can't be mistaken for a line break.
            for event, data in iter_sse(r.iter_lines(chunk_size=1)):
                if self._stop:
                    break
                if event == "session":
                    self.session_received.emit(data)
                elif event == "token":
                    self.token_received.emit(data.get("text", ""))
                elif event == "sources":
                    self.sources_received.emit(data.get("sources", []))
                elif event == "done":
                    self.stream_done.emit(data)
                    break
                elif event == "error":
                    self.stream_error.emit(data.get("detail", "Unknown error"))
                    break
        except requests.exceptions.ConnectionError:
            if not self._stop:
                self.stream_error.emit("Server not reachable. Is the backend running?")
        except Exception as e:
            if not self._stop:        # errors caused by stop() are expected
                self.stream_error.emit(f"Connection error: {e}")
        finally:
            if self._response is not None:
                try:
                    self._response.close()
                except Exception:
                    pass


class UploadWorker(QThread):
    """
    Upload a file, then poll GET /documents/{id} until indexing has finished.
    progress("uploading" | "indexing"); completed(dict) with the final document
    (status "ready" | "failed") or an error dict ({"status_code", "detail"}).
    """
    progress  = pyqtSignal(str)
    completed = pyqtSignal(dict)

    def __init__(self, path, headers=None, poll_interval=1.0, timeout=300):
        super().__init__()
        self.path          = path
        self.headers       = headers
        self.poll_interval = poll_interval
        self.timeout       = timeout

    def run(self):
        try:
            self.progress.emit("uploading")
            with open(self.path, "rb") as f:
                r = requests.post(
                    _url('/documents/upload'), headers=self.headers,
                    files={"file": (os.path.basename(self.path), f)},
                    timeout=(5, 120))
            result = _normalize(r)
            if r.status_code != 202:
                self.completed.emit(result)
                return

            doc_id = result["id"]
            self.progress.emit("indexing")
            deadline = time.monotonic() + self.timeout
            while time.monotonic() < deadline:
                time.sleep(self.poll_interval)
                r = requests.get(_url(f'/documents/{doc_id}'),
                                 headers=self.headers, timeout=15)
                result = _normalize(r)
                if r.status_code != 200 or result.get("status") != "processing":
                    self.completed.emit(result)
                    return
            self.completed.emit({"status_code": 504, "id": doc_id,
                                 "detail": "Indexing is taking longer than expected. "
                                           "It will keep running in the background."})
        except requests.exceptions.ConnectionError:
            self.completed.emit(_offline())
        except (requests.exceptions.RequestException, OSError) as e:
            self.completed.emit(_offline(str(e)))


# ── Small UI helpers ───────────────────────────────────────────────────────────

def _set_send_button_icon(self, streaming: bool):
    """Stop icon while an answer is streaming, search icon otherwise."""
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("Reqs/stop.png" if streaming else "Reqs/search.png"),
                   QtGui.QIcon.Normal, QtGui.QIcon.Off)
    size = QSize(32, 32) if streaming else QSize(24, 24)
    for te in (self.ui.text_prompt_2, self.ui.text_prompt):
        te.search_btn.setIcon(icon)
        te.search_btn.setIconSize(size)


def _sources_footer(sources, answer: str = "") -> str:
    """Markdown 'Sources' list under an answer.

    - Keeps only chunks the answer actually cited as [n] (when `answer` is given).
    - Groups chunks from the same file/page into one line: **[1, 3]** README.md
    """
    if not sources:
        return ""

    if answer:
        cited = set()
        for group in re.findall(r"\[(\d+(?:\s*,\s*\d+)*)\]", answer):
            cited.update(int(n) for n in re.findall(r"\d+", group))
        sources = [s for s in sources if s.get("ref") in cited]
        if not sources:                       # answer came from the model's own knowledge
            return ""

    grouped = {}                              # (filename, page) -> [refs], insertion-ordered
    for s in sources:
        key = (s.get("filename", "unknown"), s.get("page"))
        grouped.setdefault(key, []).append(s.get("ref"))

    lines = []
    for (filename, page), refs in grouped.items():
        page_txt = f", p. {page}" if page else ""
        ref_txt = ", ".join(str(r) for r in refs)
        lines.append(f"- **[{ref_txt}]** {filename}{page_txt}")
    return "\n\n---\n\n**Sources**\n\n" + "\n".join(lines)


# ── Document upload / clear ────────────────────────────────────────────────────

def open_document(self):
    """Chat-input '+' button: upload AND attach to the next question."""
    _start_upload(self, attach=True)


def upload_to_library(self):
    """Documents page '+ Add document': upload only, no chat attachment."""
    _start_upload(self, attach=False)


def _start_upload(self, attach: bool):
    if attach and getattr(self, 'attached_document', None):
        clear_document(self)
        return

    upload = getattr(self, '_upload_thread', None)
    if upload is not None and upload.isRunning():
        return

    if not _read_token():
        run_login(self)
        return

    path, _ = QFileDialog.getOpenFileName(
        self, "Upload a Document", "", _SUPPORTED_FILTERS)
    if not path:
        return

    filename = os.path.basename(path)
    ext      = os.path.splitext(path)[1].lower()

    if ext not in ALLOWED_EXTS:
        QMessageBox.warning(
            self, "Unsupported File",
            f"'{ext or filename}' is not supported.\n\n"
            "Supported types: PDF, DOCX, TXT, MD.")
        return

    size = os.path.getsize(path)
    if size == 0:
        QMessageBox.warning(self, "Empty File", f"'{filename}' is empty.")
        return
    if size > MAX_UPLOAD_MB * 1024 * 1024:
        QMessageBox.warning(
            self, "File Too Large",
            f"'{filename}' is {size // (1024 * 1024)} MB.\n"
            f"The limit is {MAX_UPLOAD_MB} MB.")
        return

    if attach:
        for te in (self.ui.text_prompt, self.ui.text_prompt_2):
            te.show_loading(filename)
    for btn in (self.ui.addButton, self.ui.addButton_2):
        btn.setEnabled(False)
    self.docs_panel.set_busy(True)

    self._upload_thread = UploadWorker(path, _headers(self))
    self._upload_thread.progress.connect(
        lambda stage: print(colored(f"{filename}: {stage}...", "cyan")))
    self._upload_thread.completed.connect(
        lambda result: _on_upload_completed(self, path, filename, result, attach))
    self._upload_thread.start()


def _on_upload_completed(self, path, filename, result, attach=True):
    for te in (self.ui.text_prompt, self.ui.text_prompt_2):
        te.hide_loading()
    for btn in (self.ui.addButton, self.ui.addButton_2):
        btn.setEnabled(True)
    self.docs_panel.set_busy(False)

    code   = result.get("status_code")
    status = result.get("status")

    if code == 200 and status == "ready":
        print(colored(
            f"Indexed {filename} ({result.get('chunk_count', 0)} chunks)", "cyan"))
        if attach:
            self.attached_document = {
                "filename": filename, "path": path, "text": "",
                "truncated": False, "is_image": False, "pixmap": None,
                "doc_id": result["id"],
                "chunk_count": result.get("chunk_count", 0),
            }
            for te in (self.ui.text_prompt, self.ui.text_prompt_2):
                te.set_attachment(self.attached_document)
            _set_attach_button_active(self, filename)
        load_documents(self)          # <- new doc appears in docs_list_frame

    elif code == 200 and status == "failed":
        QMessageBox.critical(
            self, "Indexing Failed",
            f"Could not index '{filename}':\n\n{result.get('error') or 'Unknown error'}")
        self._cleanup_thread = WorkerThread(
            None, 'DELETE', f"documents/{result['id']}", headers=_headers(self))
        self._cleanup_thread.data_fetched.connect(lambda _r: load_documents(self))
        self._cleanup_thread.start()

    elif code == 401:
        handle_token_expired(self)

    elif code == 504:
        QMessageBox.information(self, "Still Indexing", _error_text(result))
        load_documents(self)

    else:
        QMessageBox.critical(
            self, "Upload Failed",
            f"Could not upload '{filename}':\n\n{_error_text(result)}")

def clear_document(self):
    if getattr(self, 'attached_document', None):
        for te in (self.ui.text_prompt, self.ui.text_prompt_2):
            te.set_attachment(None)
        _set_attach_button_inactive(self)
        print(colored("Document detached", "yellow"))
    self.attached_document = None


def _set_attach_button_active(self, filename: str):
    tooltip = f"📎 {filename}\n(click to detach - it stays in your library)"
    style   = """
        QPushButton {
            background: none;
            border: 2px solid rgb(85, 170, 255);
            color: rgb(85, 170, 255);
            border-radius: 21px;
            margin-top: 3px;
        }
        QPushButton:hover {
            background-color: rgba(85, 170, 255, 30);
            border-color: rgb(231, 0, 116);
        }
    """
    for btn in (self.ui.addButton, self.ui.addButton_2):
        btn.setStyleSheet(style)
        btn.setToolTip(tooltip)


def _set_attach_button_inactive(self):
    style = """
        QPushButton {
            background: none;
            border: none;
            color: rgba(255, 255, 255, 180);
            border-radius: 21px;
            margin-top: 3px;
        }
        QPushButton:hover { background-color: rgb(45, 48, 58); }
    """
    for btn in (self.ui.addButton, self.ui.addButton_2):
        btn.setStyleSheet(style)
        btn.setToolTip("Upload a document (PDF, DOCX, TXT, MD)")


# ── Document library (optional: needs a QListWidget named `documents_list`) ────

def load_documents(self):
    """Fetch the logged-in user's documents from the server into the panel."""
    panel = getattr(self, 'docs_panel', None)
    if panel is None or not _read_token():
        return
    t = getattr(self, 'docs_thread', None)
    if t is not None and t.isRunning():          # don't replace a running QThread
        QTimer.singleShot(300, lambda: load_documents(self))
        return
    self.docs_thread = WorkerThread(None, 'GET', 'documents', headers=_headers(self))
    self.docs_thread.data_fetched.connect(lambda r: _populate_documents(self, r))
    self.docs_thread.start()


def _populate_documents(self, response):
    panel = getattr(self, 'docs_panel', None)
    if panel is None or response.get('status_code') != 200:
        return
    docs = response.get('data', [])
    panel.set_documents(docs)
    # keep refreshing while something is still being indexed
    if any(d.get('status') == 'processing' for d in docs):
        QTimer.singleShot(2000, lambda: load_documents(self))


def delete_document(self, doc_id):
    """✕ on a row: confirm, DELETE on the server, then drop it from the list."""
    from ui_controllers.show_confirm_dialog import ConfirmDialog
    t = getattr(self, 'delete_doc_thread', None)
    if t is not None and t.isRunning():
        return

    dialog = ConfirmDialog()
    dialog.ui.msg.setText("Delete Document")
    dialog.ui.info.setText("Remove this document from your library?")
    if dialog.exec_() != QDialog.Accepted:
        return

    self.delete_doc_thread = WorkerThread(
        None, 'DELETE', f'documents/{doc_id}', headers=_headers(self))

    def on_deleted(r):
        if r.get('status_code') == 204:
            attached = getattr(self, 'attached_document', None)
            if attached and attached.get('doc_id') == doc_id:
                clear_document(self)
            load_documents(self)
        else:
            QMessageBox.warning(self, "Delete Failed", _error_text(r))

    self.delete_doc_thread.data_fetched.connect(on_deleted)
    self.delete_doc_thread.start()


# ── Auth helpers ───────────────────────────────────────────────────────────────

def signup_update_ui(self):
    self.ui.signup_button.setEnabled(True)
    self.ui.label.setText('SIGN UP')
    self.ui.label.setStyleSheet('color:rgba(255, 255, 255, 180);')


@pyqtSlot(dict)
def handle_signup_response(self, response):
    code = response['status_code']
    self.ui.uname_lineEdit.setText('')
    self.ui.email_lineEdit.setText('')
    self.ui.pass_lineEdit.setText('')
    if code == 201:
        self.ui.info_label.setStyleSheet('color: rgb(0, 255, 127);')
        self.ui.info_label.setText('User registered, go to the login page!')
        return
    self.ui.info_label.setStyleSheet('color: rgb(255, 0, 0);')
    if code == 409:
        self.ui.info_label.setText("Username already taken")
    elif code == 422:
        self.ui.info_label.setText("Invalid username or password")
    elif code == 0:
        self.ui.info_label.setText("Server not reachable")
    else:
        self.ui.info_label.setText("Internal server error")


def signup(self):
    # The RAG backend registers with username + password only (no email).
    username = self.ui.uname_lineEdit.text().strip()
    password = self.ui.pass_lineEdit.text()
    pw_pat   = r'(?=.*[a-z])(?=.*[A-Z])(?=.*\W)'
    self.ui.info_label.setStyleSheet('color:rgb(255, 0, 0);')
    if not username or not password:
        self.ui.info_label.setText("username or password can't be empty")
    elif not re.fullmatch(r'[A-Za-z0-9_.-]{3,50}', username):
        self.ui.info_label.setText(
            "username must be 3-50 characters: letters, digits, _ . -")
    elif len(password) < 8:
        self.ui.info_label.setText("password must contain at least 8 characters")
    elif not re.search(pw_pat, password):
        self.ui.info_label.setText(
            "password must contain at least 1 upper case, lower case and a special symbol")
    else:
        payload = {"username": username, "password": password}
        self.ui.signup_button.setEnabled(False)
        self.ui.label.setText('Signing up...')
        self.ui.label.setStyleSheet('color: rgb(0, 255, 127);')
        self.thread = WorkerThread(payload, 'POST', 'register')
        self.thread.data_fetched.connect(lambda r: handle_signup_response(self, r))
        self.thread.finished.connect(lambda: signup_update_ui(self))
        self.thread.start()


def login_update_ui(self):
    self.ui.login_button.setEnabled(True)
    self.ui.label_3.setText('LOG IN')
    self.ui.label_3.setStyleSheet('color:rgba(255, 255, 255, 180);')


def run_login(self):
    from auth.login_window import LoginWindow
    login  = LoginWindow(self)
    result = login.exec_()
    if result == QDialog.Accepted:
        self.ui.login_button.setText("")
        self.ui.login_button.setEnabled(False)


def after_verify_token(self, response):
    code = response.get("status_code")
    if code == 200:
        username = response.get("username")
        print(colored(f"Logged in user: {username}", 'green'))
        ss = "font-family:'Roboto'; font-size:10pt; color:green;"
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Reqs/user.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.login_button.setIcon(icon)
        self.ui.login_button.setText('   ' + username)
        self.ui.login_button.setToolTip('')
        self.ui.login_button.setStyleSheet(ss)
        self.ui.login_button.setEnabled(False)
        self.ui.logged_in_label.setText('Logged In')
        self.ui.logged_in_label.setStyleSheet(ss)
        self.ui.username_label.setText(f"Username: {username}")
        self.ui.email_label.setText("")          # the RAG backend has no email field
        self.ui.button_logout.setText('Log Out')
        self.ui.button_logout.setStyleSheet("""
                                    QPushButton{
                                        color: rgb(190, 42, 42);
                                        border: 2px solid rgb(190, 42, 42);
                                        background-color: rgba(70, 49, 60, 80);
                                        border-radius : 10px;
                                    }

                                    QPushButton:hover{
                                        background-color: rgba(70, 49, 60, 40);
                                        border: 2px solid rgba(190, 42, 42, 170);
}""")
        load_chat_history(self)
        load_documents(self)
    elif code == 0:
        print(colored(response.get("detail", "Server not reachable"), 'red'))
        QMessageBox.warning(
            self, "Server Unreachable",
            f"Could not reach the server at {API_BASE_URL}.\n"
            "Make sure the backend is running.")
    else:
        print(colored(_error_text(response, "Token rejected"), 'red'))
        run_login(self)


def verify_token_(self, token, callback):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    self.thread = WorkerThread(None, 'GET', 'verify_token', headers=headers)
    self.thread.data_fetched.connect(lambda r: callback(self, r))
    self.thread.start()


def verify_token(self):
    token = _read_token()
    if token:
        verify_token_(self, token, after_verify_token)
    else:
        run_login(self)


@pyqtSlot(dict)
def handle_login_response(self, response, main_win):
    if 'access_token' in response:
        self.ui.uid_lineEdit_2.setText('')
        self.ui.pass_lineEdit_2.setText('')
        self.close()
        _write_token(response['access_token'])
        print(colored('Verifying token!', 'magenta'))
        verify_token(main_win)
    else:
        self.ui.pass_lineEdit_2.setText('')
        self.ui.uid_lineEdit_2.setText('')
        self.ui.info_label2.setStyleSheet('color: rgb(255, 0, 0);')
        if response.get('status_code') == 0:
            self.ui.info_label2.setText("Server not reachable")
        elif response.get('status_code') == 401:
            self.ui.info_label2.setText("Invalid credentials")
        else:
            self.ui.info_label2.setText(_error_text(response, "Login failed"))


def login(self, main_win):
    self.ui.info_label.setText('')
    username = self.ui.uid_lineEdit_2.text().strip().lower()
    password = self.ui.pass_lineEdit_2.text()
    if not username or not password:
        self.ui.info_label2.setStyleSheet('color:rgb(255, 0, 0);')
        self.ui.info_label2.setText("username or password can't be empty")
    else:
        payload = {"username": username, "password": password}
        self.ui.login_button.setEnabled(False)
        self.ui.label_3.setText('Signing in...')
        self.ui.label_3.setStyleSheet('color: rgb(0, 255, 127);')
        self.thread = WorkerThread(payload, 'POST', 'login')
        self.thread.data_fetched.connect(lambda r: handle_login_response(self, r, main_win))
        self.thread.finished.connect(lambda: login_update_ui(self))
        self.thread.start()


def handle_token_expired(main_window):
    run_login(main_window)


# ── Preferences (the RAG backend has none - kept so existing callers don't break) ──

def save_user_preferences(self):
    print(colored("Preferences are not supported by the RAG backend.", "yellow"))


def get_user_preferences(self):
    pass


# ── Streaming ──────────────────────────────────────────────────────────────────

def _on_stream_session(self, data):
    """Server tells us which session this chat belongs to (new or existing)."""
    self.current_chat_id = data["session_id"]


def _on_stream_sources(self, sources):
    self.last_sources = sources


def _on_stream_error(self, message):
    """Show the failure inside the AI bubble so the user sees why nothing came back."""
    self.full_text = (getattr(self, "full_text", "") + f"\n\n⚠️ {message}").strip()
    self.ai_bubble.append_stream(self.full_text)


def get_prompt_stream(self, chunk):
    if not hasattr(self, "full_text"):
        self.full_text = ""
    self.full_text += chunk
    self.ai_bubble.append_stream(self.full_text)
    if not getattr(self, '_scroll_pending', False):
        self._scroll_pending = True
        QTimer.singleShot(100, lambda: _do_scroll(self))


def _do_scroll(self):
    self._scroll_pending = False
    self.chat_area.scroll_to_bottom()


def finalize_stream(self):
    if getattr(self, '_stream_stopped', False):
        self._stream_stopped = False
        load_chat_history(self)
        return
    self._is_streaming = False
    if getattr(self, 'full_text', ''):
        self.ai_bubble.finish_stream(
            self.full_text + _sources_footer(getattr(self, 'last_sources', []), self.full_text))
    self._scroll_pending = False
    self.chat_area.scroll_to_bottom()
    _set_send_button_icon(self, streaming=False)
    clear_document(self)
    load_chat_history(self)


def stop_prompt(self):
    """
    The backend has no stop endpoint - stopping just drops the HTTP connection,
    which makes the server abandon the generation. (A stopped answer is not
    saved in the conversation history.)
    """
    thread = getattr(self, 'stream_thread', None)
    if thread is None or not thread.isRunning():
        return
    self._stream_stopped = True
    thread.stop()
    _on_stream_stopped(self)


def _on_stream_stopped(self):
    self._is_streaming   = False
    self._scroll_pending = False
    if getattr(self, 'full_text', ''):
        self.ai_bubble.finish_stream(self.full_text)
    self.chat_area.scroll_to_bottom()
    _set_send_button_icon(self, streaming=False)
    clear_document(self)


def send_prompt(self):
    from ui.widgets.chat_bubble import ChatBubble

    if hasattr(self, 'full_text'):
        del self.full_text
    self._scroll_pending = False
    self.last_sources    = []

    # Read from whichever input is active
    text = self.ui.text_prompt.toPlainText().strip()
    if not text:
        text = self.ui.text_prompt_2.toPlainText().strip()
    if not text:
        return

    headers = _headers(self)
    if not headers:                       # not logged in
        run_login(self)
        return

    self.ui.stackedWidget.setCurrentWidget(self.ui.conversation_page)

    self.ui.text_prompt.clear()
    self.ui.text_prompt.reset_height()
    self.ui.text_prompt_2.clear()
    self.ui.text_prompt_2.reset_height()

    self._is_streaming = True
    _set_send_button_icon(self, streaming=True)

    chat_width = self.chat_area.width()

    # ── Snapshot the attachment BEFORE clearing anything ───────────────
    doc = getattr(self, 'attached_document', None)

    # ── User bubble — pass the attachment so chip renders inside bubble ─
    user_bubble = ChatBubble(
        text,
        is_user=True,
        available_width=chat_width,
        attachment=doc
    )
    self.chat_area.add_bubble(user_bubble)

    # ── NOW clear the input chip (after bubble is created) ────────────
    for te in (self.ui.text_prompt, self.ui.text_prompt_2):
        te.set_attachment(None)

    # ── AI bubble ──────────────────────────────────────────────────────
    self.ai_bubble = ChatBubble("", is_user=False, available_width=chat_width)
    self.ai_bubble.start_stream()
    self.chat_area.add_bubble(self.ai_bubble)

    # ── Build payload ──────────────────────────────────────────────────
    # session_id None -> the server creates a new chat and tells us its id.
    # doc_ids omitted  -> search ALL of the user's documents.
    payload = {
        "message":    text,
        "session_id": getattr(self, 'current_chat_id', None),
    }
    if doc and doc.get("doc_id"):
        payload["doc_ids"] = [doc["doc_id"]]     # scope this question to the attached file

    # Clear the document state AFTER payload is built
    self.attached_document = None
    _set_attach_button_inactive(self)

    self.stream_thread = ChatStreamWorker(payload, headers)
    self.stream_thread.session_received.connect(lambda d: _on_stream_session(self, d))
    self.stream_thread.token_received.connect(lambda t: get_prompt_stream(self, t))
    self.stream_thread.sources_received.connect(lambda s: _on_stream_sources(self, s))
    self.stream_thread.stream_error.connect(lambda m: _on_stream_error(self, m))
    self.stream_thread.auth_failed.connect(lambda: handle_token_expired(self))
    self.stream_thread.finished.connect(lambda: finalize_stream(self))
    self.stream_thread.start()


# ── Chat history ───────────────────────────────────────────────────────────────

def load_chat_history(self):
    if not _read_token():
        return
    self.chat_history_thread = WorkerThread(None, 'GET', 'chats', headers=_headers(self))
    self.chat_history_thread.data_fetched.connect(
        lambda r: _populate_chat_history(self, r))
    self.chat_history_thread.start()


def _populate_chat_history(self, response):
    if response.get('status_code') != 200:
        return
    lw = self.ui.chat_history
    lw.clear()
    for chat in response.get('data', []):
        item = QtWidgets.QListWidgetItem(chat['title'])
        item.setData(Qt.UserRole, chat['id'])
        item.setToolTip(chat['title'])
        lw.addItem(item)


def on_chat_history_item_clicked(self, item):
    chat_id = item.data(Qt.UserRole)
    if chat_id is None:
        return
    self.load_chat_thread = WorkerThread(
        None, 'GET', f'chat/{chat_id}', headers=_headers(self))
    self.load_chat_thread.data_fetched.connect(
        lambda r: _render_loaded_chat(self, r, chat_id))
    self.load_chat_thread.start()


def _render_loaded_chat(self, response, chat_id):
    clear_document(self)
    if response.get('status_code') != 200:
        return
    from ui.widgets.chat_bubble import ChatBubble
    self.ui.stackedWidget.setCurrentWidget(self.ui.conversation_page)
    self.clear_chat()
    chat_width = self.chat_area.width()
    for msg in response.get('data', []):
        is_user = msg['role'] == 'user'
        text    = msg['content']
        if not is_user:
            text += _sources_footer(msg.get('sources') or [], text)
        bubble = ChatBubble(text, is_user=is_user, available_width=chat_width)
        self.chat_area.add_bubble(bubble)
    self.current_chat_id = chat_id
    self.chat_area.scroll_to_bottom()


# ── Context menu ───────────────────────────────────────────────────────────────

def _show_chat_context_menu(self, position):
    from PyQt5.QtWidgets import QMenu, QAction
    item = self.ui.chat_history.itemAt(position)
    if not item:
        return
    chat_id       = item.data(Qt.UserRole)
    current_title = item.text()
    menu = QMenu(self.ui.chat_history)
    menu.setStyleSheet("""
        QMenu {
            background-color: rgb(43,47,58); color:rgba(255,255,255,200);
            border:1px solid rgba(255,255,255,30); border-radius:6px;
            padding:4px; font-family:'Roboto'; font-size:10pt;
        }
        QMenu::item{padding:8px 20px;border-radius:4px;}
        QMenu::item:selected{background-color:rgb(55,62,76);color:white;}
        QMenu::separator{height:1px;background:rgba(255,255,255,20);margin:3px 8px;}
    """)
    rename_action = QAction("✏  Rename", self.ui.chat_history)
    delete_action = QAction("🗑  Delete", self.ui.chat_history)
    menu.addAction(rename_action)
    menu.addSeparator()
    menu.addAction(delete_action)
    action = menu.exec_(self.ui.chat_history.mapToGlobal(position))
    if action == rename_action:
        _rename_chat_dialog(self, item, chat_id, current_title)
    elif action == delete_action:
        _delete_chat_confirm(self, item, chat_id)


def _rename_chat_dialog(self, item, chat_id, current_title):
    from PyQt5.QtWidgets import QInputDialog
    dialog = QInputDialog(self.ui.chat_history)
    dialog.setWindowTitle("Rename Chat")
    dialog.setLabelText("New name:")
    dialog.setTextValue(current_title)
    dialog.setStyleSheet("""
        QInputDialog,QDialog{background-color:rgb(35,38,47);}
        QLabel{color:rgba(255,255,255,180);font-family:'Roboto';font-size:10pt;}
        QLineEdit{background-color:rgb(41,44,53);color:white;
            border:2px solid rgb(85,170,255);border-radius:6px;
            padding:6px 12px;font-family:'Roboto';font-size:10pt;}
        QPushButton{background-color:rgb(48,53,65);color:rgba(255,255,255,200);
            border:1px solid rgba(255,255,255,40);border-radius:6px;
            padding:6px 16px;font-family:'Roboto';font-size:9pt;min-width:70px;}
        QPushButton:hover{background-color:rgb(55,62,76);
            border:1px solid rgb(85,170,255);}
    """)
    ok        = dialog.exec_()
    new_title = dialog.textValue().strip()[:120]      # backend limit: 120 chars
    if not ok or not new_title or new_title == current_title:
        return
    self.rename_thread = WorkerThread(
        {"title": new_title}, 'PATCH', f'chat/{chat_id}', headers=_headers(self))

    def on_renamed(r):
        if r.get('status_code') == 200:
            item.setText(new_title)
            item.setToolTip(new_title)

    self.rename_thread.data_fetched.connect(on_renamed)
    self.rename_thread.start()


def _delete_chat_confirm(self, item, chat_id):
    from ui_controllers.show_confirm_dialog import ConfirmDialog
    dialog = ConfirmDialog()
    if dialog.exec_() != QDialog.Accepted:
        return
    self.delete_thread = WorkerThread(
        None, 'DELETE', f'chat/{chat_id}', headers=_headers(self))

    def on_deleted(r):
        if r.get('status_code') == 204:               # FastAPI returns 204 No Content
            row = self.ui.chat_history.row(item)
            self.ui.chat_history.takeItem(row)
            if getattr(self, 'current_chat_id', None) == chat_id:
                self.handle_new_chat()

    self.delete_thread.data_fetched.connect(on_deleted)
    self.delete_thread.start()