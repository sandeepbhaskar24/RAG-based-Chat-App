# RAG Chat – Backend

FastAPI + LangChain + Qdrant + MySQL.

## Run

```bash
docker compose up -d            # from repo root: Qdrant + MySQL
cd backend
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then set OPENAI_API_KEY and JWT_SECRET
uvicorn main:app --reload
```

Interactive docs: http://127.0.0.1:8000/docs

No Docker? Use `DATABASE_URL=sqlite:///./dev.db` and `QDRANT_URL=:memory:` in `.env`.

## Test

```bash
pip install -r requirements-dev.txt
pytest
```
(Tests use SQLite, in-memory Qdrant, and fake embeddings/LLM – no API key or network needed.)

## API

| Method | Path | Purpose |
|---|---|---|
| POST | /auth/register | create account |
| POST | /auth/login | returns `{access_token, user}` |
| GET | /auth/me | current user |
| POST | /documents/upload | multipart `file` (pdf/docx/txt/md); returns 202, indexes in background |
| GET | /documents | list (poll `status`: processing / ready / failed) |
| GET | /documents/{id} | one document |
| DELETE | /documents/{id} | removes file, DB row and vectors |
| POST | /chat | `{message, session_id?, doc_ids?}` → SSE stream |
| GET/POST | /chat/sessions | list / create |
| GET | /chat/sessions/{id}/messages | history (with sources) |
| PATCH/DELETE | /chat/sessions/{id} | rename / delete |
| GET | /health | DB + Qdrant status |

All routes except `/auth/register`, `/auth/login`, `/health` need `Authorization: Bearer <token>`.

### `/chat` SSE events

```
event: session   data: {"session_id": 1, "title": "..."}
event: token     data: {"text": "Par"}          (repeated)
event: sources   data: {"sources": [{"ref":1,"doc_id":3,"filename":"a.pdf","page":2,"snippet":"...","score":0.83}]}
event: done      data: {"message_id": 12}
event: error     data: {"detail": "..."}        (instead of sources/done on failure)
```
