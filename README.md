# RAG Chat App

A desktop **Retrieval-Augmented Generation (RAG)** chat application. Upload your own documents (PDF, DOCX, TXT, MD), then chat with them. Answers are streamed token-by-token and cite the exact document and page they came from.

- **Backend:** FastAPI + LangChain + Qdrant (vectors) + MySQL (users, chats, documents)
- **Frontend:** PyQt5 desktop client with a custom dark, frameless UI
- **LLM / embeddings:** any OpenAI-compatible endpoint (defaults to [OpenRouter](https://openrouter.ai))

---

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Directory Structure](#directory-structure)
4. [Prerequisites](#prerequisites)
5. [Setup](#setup)
6. [Configuration](#configuration)
7. [Running the App](#running-the-app)
8. [Using the App](#using-the-app)
9. [API Reference](#api-reference)
10. [How the RAG Pipeline Works](#how-the-rag-pipeline-works)
11. [Testing](#testing)
12. [Troubleshooting](#troubleshooting)
13. [Known Limitations](#known-limitations)
14. [Security Notes](#security-notes)
15. [Credits](#credits)

---

## Features

- **Account system** – register / log in with JWT authentication; the token is stored locally so you stay logged in between launches.
- **Document library** – upload PDF, DOCX, TXT and MD files (up to 20 MB). Indexing runs in the background and the UI shows live status (`processing` → `ready` / `failed`).
- **Per-user isolation** – every vector is tagged with `user_id`; retrieval is always filtered so users can only search their own documents.
- **Scoped questions** – attach a document with the **+** button to restrict a question to that file, or ask without one to search your whole library.
- **Streaming answers** – responses arrive over Server-Sent Events (SSE) and render live, with a **Stop** button to cancel.
- **Inline citations** – answers reference sources as `[1]`, `[2]`, followed by a *Sources* list (filename + page).
- **History-aware chat** – follow-up questions ("what about its price?") are rewritten into standalone queries before retrieval; history is trimmed to a token budget.
- **Chat management** – saved conversations in the sidebar with rename and delete via right-click.
- **Rich message rendering** – Markdown, tables and syntax-highlighted code blocks (Pygments).

---

## Architecture

```
┌────────────────────────┐        HTTP / SSE         ┌─────────────────────────────┐
│   PyQt5 Desktop App    │ ────────────────────────► │        FastAPI Backend      │
│  (frontend/)           │ ◄──────────────────────── │        (backend/)           │
│                        │                           │                             │
│  • Login / Sign up     │                           │  /auth  /documents  /chat   │
│  • Chat bubbles        │                           │          /health            │
│  • Document library    │                           └──────┬───────────┬──────────┘
└────────────────────────┘                                  │           │
                                                            ▼           ▼
                                                    ┌────────────┐ ┌────────────┐
                                                    │   MySQL    │ │   Qdrant   │
                                                    │ users,     │ │ document   │
                                                    │ chats,     │ │ chunk      │
                                                    │ documents  │ │ vectors    │
                                                    └────────────┘ └────────────┘
                                                            │
                                                            ▼
                                              ┌──────────────────────────┐
                                              │ OpenAI-compatible API    │
                                              │ (OpenRouter): LLM +      │
                                              │ embeddings               │
                                              └──────────────────────────┘
```

**Chat request flow**

```
user question
   │
   ├─► condense follow-up into a standalone question (uses recent history)
   ├─► embed question → Qdrant similarity search (filtered by user_id [+ doc_ids])
   ├─► build prompt: system rules + numbered context + history + question
   ├─► stream LLM tokens back as SSE `token` events
   └─► save assistant message + sources → emit `sources` and `done`
```

---

## Directory Structure

```
RAG-Chat-App/
├── README.md
├── docker-compose.yml            # Qdrant + MySQL for local development
├── .gitignore
│
├── backend/                      # FastAPI service
│   ├── main.py                   # App entry point (lifespan, CORS, routers)
│   ├── requirements.txt
│   ├── requirements-dev.txt      # pytest etc.
│   ├── .env.example              # copy to .env and fill in
│   ├── storage/
│   │   └── uploads/              # uploaded files, one sub-folder per user id
│   └── app/
│       ├── api/
│       │   ├── deps.py           # get_current_user (Bearer JWT dependency)
│       │   └── routes/
│       │       ├── auth.py       # /auth/register, /auth/login, /auth/me
│       │       ├── chat.py       # /chat (SSE), /chat/sessions[...]
│       │       ├── documents.py  # /documents upload / list / get / delete
│       │       └── health.py     # /health (DB + Qdrant status)
│       ├── core/
│       │   ├── config.py         # Settings (pydantic-settings, .env loading)
│       │   ├── logging.py        # Logging setup
│       │   └── security.py       # Password hashing + JWT create/decode
│       ├── db/
│       │   ├── models.py         # SQLAlchemy models: User, Document, ChatSession, Message
│       │   ├── session.py        # Engine, SessionLocal, init_db()
│       │   └── crud.py           # Database access helpers
│       ├── rag/
│       │   ├── loaders.py        # PDF / DOCX / TXT / MD → LangChain Documents
│       │   ├── splitter.py       # RecursiveCharacterTextSplitter
│       │   ├── embeddings.py     # OpenAI-compatible embeddings client
│       │   ├── vector_store.py   # Qdrant client, collection bootstrap, user filters
│       │   ├── ingest.py         # load → split → embed → upsert
│       │   ├── retriever.py      # Filtered similarity search
│       │   ├── memory.py         # Chat history rebuilt within a token budget
│       │   ├── prompts.py        # RAG + question-condensing prompts
│       │   └── chain.py          # Condense, format context, stream answer, sources
│       ├── schemas/              # Pydantic request/response models
│       │   ├── auth.py
│       │   ├── chat.py
│       │   └── document.py
│       └── services/
│           ├── chat_service.py       # Chat orchestration + SSE event stream
│           └── document_service.py   # Upload validation, background ingestion, delete
│
└── frontend/                     # PyQt5 desktop client
    ├── main.py                   # App entry point / MainWindow
    ├── requirements.txt
    ├── Reqs/                     # Icons and images (app_icon.png, search.png, loading.gif, ...)
    ├── auth_token.x              # JWT saved after login (git-ignored, auto-created)
    ├── auth/
    │   ├── login_window.py       # Frameless login / sign-up dialog (+ blur overlay)
    │   └── logout.py             # Clears token and resets account UI
    ├── services/
    │   └── handle_requests.py    # All HTTP/SSE logic + worker threads
    ├── ui/                       # Generated UI code (from the .ui files)
    │   ├── mainUI.py
    │   ├── login_page_ui.py
    │   ├── message_ui.py
    │   ├── confirm_dialog.py
    │   └── widgets/
    │       ├── chat_area.py      # Scrollable chat container
    │       └── chat_bubble.py    # Markdown + code-highlighted message bubbles
    ├── ui_controllers/           # Custom widgets and window behaviour
    │   ├── auto_grow_text_edit.py  # Growing input box with attach chip + buttons
    │   ├── documents_panel.py      # Document library list
    │   ├── sticky_search_button.py
    │   ├── py_toggle.py            # Animated toggle switch
    │   ├── show_confirm_dialog.py
    │   ├── show_message.py
    │   └── ui_functions.py         # Sidebar, page navigation, window controls
    └── xml_ui/                   # Qt Designer .ui source files
        ├── mainUI.ui
        ├── login_page_ui.ui
        ├── message_ui.ui
        └── confirm_dialog.ui
```

---

## Prerequisites

| Requirement | Notes |
|---|---|
| **Python 3.10+** | Required by the backend (modern type hints, LangChain 1.x). Use a separate virtual environment for the backend and the frontend if you prefer. |
| **Docker + Docker Compose** | Optional but recommended – starts Qdrant and MySQL in one command. |
| **OpenRouter (or OpenAI-compatible) API key** | Used for both the chat model and embeddings. |
| **Roboto font** | Optional – the UI is designed around it and falls back to a system font. |
| **Windows / macOS / Linux** | The frontend was developed on Windows 11; PyQt5 runs on all three. |

> **No Docker?** You can run with SQLite and an in-memory Qdrant – see [Running without Docker](#running-without-docker).

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/sandeepbhaskar14/<your-repo-name>.git
cd <your-repo-name>
```

### 2. Start MySQL and Qdrant

From the repository root:

```bash
docker compose up -d
```

This starts:

| Service | Port | Purpose |
|---|---|---|
| Qdrant | `6333` (REST), `6334` (gRPC) | Vector database |
| MySQL 8.4 | `3306` | Relational database (`rag_chat` is created automatically) |

The default MySQL root password is `password`. Override it with the `MYSQL_ROOT_PASSWORD` environment variable and update `DATABASE_URL` to match.

### 3. Set up the backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env        # Windows: copy .env.example .env
```

Open `backend/.env` and set at least:

```env
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxx
JWT_SECRET=a-long-random-string
```

Generate a strong secret with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

### 4. Set up the frontend

Open a **new terminal** (so the backend can keep running):

```bash
cd frontend
python -m venv .venv
.venv\Scripts\activate       # macOS / Linux: source .venv/bin/activate
pip install -r frontend/requirements.txt   # or: pip install -r requirements.txt
```

---

## Configuration

All backend settings are read from environment variables or a `.env` file (checked in the repo root and in `backend/`). Defaults come from `backend/app/core/config.py`.

| Variable | Default | Description |
|---|---|---|
| `APP_NAME` | `RAG Chat API` | API title |
| `DEBUG` | `false` | Verbose logging |
| `CORS_ORIGINS` | `["*"]` | Allowed origins (restrict in production) |
| `JWT_SECRET` | `change-me` | **Change this.** Secret used to sign tokens |
| `JWT_ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | Token lifetime (24 h) |
| `DATABASE_URL` | `mysql+pymysql://root:password@localhost:3306/rag_chat?charset=utf8mb4` | SQLAlchemy URL; use `sqlite:///./dev.db` for SQLite |
| `OPENROUTER_API_KEY` | – | API key used for the LLM **and** embeddings |
| `OPENAI_BASE_URL` | `https://openrouter.ai/api/v1` | Any OpenAI-compatible base URL |
| `LLM_MODEL` | `gpt-4o-mini` | Chat model name |
| `LLM_TEMPERATURE` | `0.2` | Sampling temperature |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model name |
| `EMBEDDING_DIM` | `1536` | Must match the embedding model's output size |
| `QDRANT_URL` | `http://localhost:6333` | Use `:memory:` for an in-process store |
| `QDRANT_API_KEY` | – | For Qdrant Cloud |
| `QDRANT_COLLECTION` | `documents` | Collection name |
| `CHUNK_SIZE` | `900` | Characters per chunk |
| `CHUNK_OVERLAP` | `120` | Overlap between chunks |
| `RETRIEVAL_K` | `5` | Chunks retrieved per question |
| `HISTORY_TOKEN_BUDGET` | `2000` | Max tokens of chat history sent to the LLM |
| `UPLOAD_DIR` | `backend/storage/uploads` | Where files are stored |
| `MAX_UPLOAD_MB` | `20` | Upload size limit |

**Frontend:** set `RAG_API_URL` if the backend is not at `http://127.0.0.1:8000`.

```bash
# macOS / Linux
export RAG_API_URL=http://192.168.1.20:8000
# Windows (PowerShell)
$env:RAG_API_URL = "http://192.168.1.20:8000"
```

### Notes on model names

- With OpenRouter, model IDs are usually provider-prefixed, e.g. `LLM_MODEL=openai/gpt-4o-mini` and `EMBEDDING_MODEL=openai/text-embedding-3-small`. Check the model page on OpenRouter if you get a "model not found" error.
- If you change `EMBEDDING_MODEL`, update `EMBEDDING_DIM` to match **and** delete the existing Qdrant collection – vectors of different sizes cannot share a collection. Re-upload your documents afterwards.

---

## Running the App

### Start the backend

```bash
cd backend
uvicorn main:app --reload
```

- API: http://127.0.0.1:8000
- Interactive docs (Swagger): http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

Database tables are created automatically on startup.

### Start the desktop client

```bash
cd frontend
python main.py
```

> **Important:** run the client from inside the `frontend/` folder. Icons (`Reqs/…`) and the token file (`auth_token.x`) use paths relative to the working directory.

### Running without Docker

In `backend/.env`:

```env
DATABASE_URL=sqlite:///./dev.db
QDRANT_URL=:memory:
```

Everything works, but the in-memory Qdrant store is wiped whenever the backend restarts, so documents must be re-uploaded (their DB rows will remain, but the vectors will be gone).

---

## Using the App

1. **Sign up** – click *Log In* → *Sign Up*. Username: 3–50 characters (letters, digits, `_ . -`). Password: at least 8 characters with an uppercase letter, a lowercase letter and a special symbol.
2. **Log in** – your session token is saved locally, so you are logged in automatically next time.
3. **Add documents** – either:
   - click **+** in the chat box to upload *and attach* a file to your next question, or
   - go to **Settings → Documents → + Add document** to upload to your library only.
4. **Wait for indexing** – the status icon shows ⏳ while processing and ✓ when ready. Failed files show `!` (hover for the error).
5. **Ask questions** – type and press **Enter** (use **Shift+Enter** for a new line).
   - With an attached file, the question searches only that file.
   - With no attachment, it searches all of your documents.
6. **Stop a response** – click the stop button while an answer is streaming.
7. **Manage chats** – expand the sidebar (menu icon); right-click a chat to rename or delete it.
8. **Delete documents** – click ✕ on a row in **Settings → Documents**. This removes the file, the DB record and its vectors.

---

## API Reference

All routes except `/auth/register`, `/auth/login` and `/health` require the header `Authorization: Bearer <token>`.

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/auth/register` | Create an account (`201`) |
| `POST` | `/auth/login` | Returns `{access_token, token_type, user}` |
| `GET` | `/auth/me` | Current user |
| `POST` | `/documents/upload` | Multipart `file` (pdf/docx/txt/md); returns `202`, indexes in background |
| `GET` | `/documents` | List documents (poll `status`: `processing` / `ready` / `failed`) |
| `GET` | `/documents/{id}` | Single document |
| `DELETE` | `/documents/{id}` | Remove file, DB row and vectors (`204`) |
| `POST` | `/chat` | `{message, session_id?, doc_ids?}` → SSE stream |
| `GET` | `/chat/sessions` | List chat sessions |
| `POST` | `/chat/sessions` | Create a session |
| `GET` | `/chat/sessions/{id}/messages` | Message history (with sources) |
| `PATCH` | `/chat/sessions/{id}` | Rename |
| `DELETE` | `/chat/sessions/{id}` | Delete (`204`) |
| `GET` | `/health` | DB + Qdrant status |

### `/chat` SSE events

```
event: session   data: {"session_id": 1, "title": "..."}
event: token     data: {"text": "Par"}                    (repeated)
event: sources   data: {"sources": [{"ref":1,"doc_id":3,"filename":"a.pdf","page":2,"snippet":"...","score":0.83}]}
event: done      data: {"message_id": 12}
event: error     data: {"detail": "..."}                  (instead of sources/done on failure)
```

### Quick test with curl

```bash
# register + login
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"Passw0rd!"}'

TOKEN=$(curl -s -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"Passw0rd!"}' | python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# upload a document
curl -X POST http://127.0.0.1:8000/documents/upload \
  -H "Authorization: Bearer $TOKEN" -F "file=@report.pdf"

# ask a question (streamed)
curl -N -X POST http://127.0.0.1:8000/chat \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"message":"Summarise the report"}'
```

---

## How the RAG Pipeline Works

**Ingestion** (`app/rag/ingest.py`)

1. **Load** – PDFs are read page by page (`pdfplumber`); DOCX paragraphs and tables are extracted (`python-docx`); TXT/MD are read as UTF-8.
2. **Split** – `RecursiveCharacterTextSplitter` with `CHUNK_SIZE=900` and `CHUNK_OVERLAP=120`.
3. **Tag** – each chunk gets metadata: `user_id`, `doc_id`, `filename`, `page`, `chunk_index`.
4. **Embed + store** – chunks are embedded and upserted into the Qdrant collection (payload indexes are created on `metadata.user_id` and `metadata.doc_id`).

**Answering** (`app/services/chat_service.py`, `app/rag/chain.py`)

1. The user message is saved and the recent history is rebuilt within `HISTORY_TOKEN_BUDGET`.
2. If there is history, the question is **condensed** into a standalone query.
3. Qdrant returns the top `RETRIEVAL_K` chunks, **filtered by user** (and optionally by selected documents).
4. The prompt instructs the model to answer **only** from the numbered context, to say so when the answer isn't there, and to cite `[n]`.
5. Tokens are streamed to the client; the final answer and its sources are persisted.

---

## Testing

```bash
cd backend
pip install -r requirements-dev.txt
pytest
```

The tests use SQLite, an in-memory Qdrant and fake embeddings/LLM, so **no API key or network access is needed**.

---

## Troubleshooting

| Problem | Likely cause / fix |
|---|---|
| Client says **"Server not reachable"** | Backend isn't running, or `RAG_API_URL` is wrong. Check http://127.0.0.1:8000/health. |
| Backend crashes on startup with a MySQL error | MySQL container still starting – wait a few seconds, or confirm `docker compose ps`. Check `DATABASE_URL`. |
| `JWT_SECRET is the default value` warning | Set a strong `JWT_SECRET` in `.env`. |
| Embedding / chat call returns 401 or "model not found" | Check `OPENROUTER_API_KEY` and use provider-prefixed model IDs (e.g. `openai/gpt-4o-mini`). |
| `TypeError` about `None` for `OPENROUTER_API_KEY` | The variable is missing from `.env` – add it. |
| Document stuck on **failed**: "No extractable text found" | The PDF is a scan (image only). OCR it first. |
| Vector size mismatch error in Qdrant | You changed the embedding model. Update `EMBEDDING_DIM`, delete the `documents` collection, re-upload files. |
| Icons missing / blank buttons in the client | Run `python main.py` from inside `frontend/` so `Reqs/` resolves. Make sure the icon files exist. |
| Stuck in a login loop after a backend reset | Delete `frontend/auth_token.x` and log in again (the token is invalid, e.g. after changing `JWT_SECRET`). |
| `ModuleNotFoundError: ui...` | Run from `frontend/`, not the repo root. |

---

## Known Limitations

- Scanned / image-only PDFs are not supported (no OCR).
- Stopping a response drops the connection; a stopped answer is **not** saved to history.
- Retrieval is plain vector similarity (no re-ranking or hybrid search yet).
- The Settings → *Update*, *Change Password*, *Two-Factor Authentication* and *Edit profile* sections are UI placeholders and not yet wired to the backend.
- The backend has no email field; accounts are username + password only.
- Database migrations are not set up – tables are created with `create_all()` on startup (consider Alembic for schema changes).

---

## Security Notes

- Change `JWT_SECRET` before deploying anywhere beyond your own machine.
- Passwords are hashed (Werkzeug); plain-text passwords are never stored.
- Restrict `CORS_ORIGINS` and serve the API over HTTPS in production.
- The client stores the JWT in `frontend/auth_token.x`. It is git-ignored – never commit it, and never commit `.env`.
- Uploaded files are stored on disk under `backend/storage/uploads/<user_id>/` with randomised filenames.

---

## Credits

Built by **Sandeep Bhaskar** – [GitHub](https://github.com/sandeepbhaskar14) · [LinkedIn](https://linkedin.com/in/sandeep-bhaskar-3b8686292)

Built with [FastAPI](https://fastapi.tiangolo.com), [LangChain](https://www.langchain.com), [Qdrant](https://qdrant.tech), [PyQt5](https://riverbankcomputing.com/software/pyqt/), [Pygments](https://pygments.org) and [Markdown](https://python-markdown.github.io).

