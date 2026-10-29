"""Chat orchestration + Server-Sent Events (SSE) streaming.

SSE events emitted by stream_chat():
  session  {"session_id": int, "title": str}
  status   {"text": str}                 (0..n)  progress hints from the agents
  token    {"text": str}                 (repeated)
  sources  {"sources": [...]}
  done     {"message_id": int}
  error    {"detail": str}               (instead of sources/done if something fails)
"""
import json
import logging
from collections.abc import Iterator

from fastapi import HTTPException
from langchain_core.messages import BaseMessage

from app.agents.runner import run_agents
from app.db import crud
from app.db.models import User
from app.db.session import SessionLocal
from app.rag.memory import load_history

logger = logging.getLogger(__name__)
DEFAULT_TITLE = "New chat"


def sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


def _make_title(message: str) -> str:
    title = " ".join(message.split())
    return title if len(title) <= 50 else title[:47] + "..."


def prepare_chat(db, user: User, message: str, session_id: int | None,
                 doc_ids: list[int] | None):
    """Validate the request, create/load the session and persist the user's message.

    Runs *before* streaming starts so problems surface as normal HTTP errors.
    """
    if doc_ids:
        unique = list(set(doc_ids))
        if crud.count_user_documents(db, user.id, unique) != len(unique):
            raise HTTPException(404, "One or more documents were not found")

    if session_id is not None:
        session = crud.get_session(db, user.id, session_id)
        if session is None:
            raise HTTPException(404, "Chat session not found")
    else:
        session = crud.create_session(db, user.id, _make_title(message))

    history = load_history(db, session.id)  # history *before* this message
    if session.title == DEFAULT_TITLE:
        session = crud.rename_session(db, session, _make_title(message))
    crud.add_message(db, session.id, "user", message)
    return session, history


def _has_ready_documents(user_id: int) -> bool:
    with SessionLocal() as db:
        return any(d.status == "ready" for d in crud.list_documents(db, user_id))


def stream_chat(user_id: int, session_id: int, title: str, message: str,
                doc_ids: list[int] | None, history: list[BaseMessage]) -> Iterator[str]:
    yield sse("session", {"session_id": session_id, "title": title})
    try:
        parts: list[str] = []
        sources: list[dict] = []
        for ev in run_agents(message, history, user_id, doc_ids, _has_ready_documents(user_id)):
            if ev["type"] == "token":
                parts.append(ev["text"])
                yield sse("token", {"text": ev["text"]})
            elif ev["type"] == "status":
                yield sse("status", {"text": ev["text"]})
            elif ev["type"] == "final":
                sources = ev["sources"]

        answer = "".join(parts).strip()
        if not answer:
            answer = "Sorry, I couldn't produce an answer. Please try again."
            yield sse("token", {"text": answer})

        # Own DB session: the request-scoped one may already be closed while streaming.
        with SessionLocal() as db:
            saved = crud.add_message(db, session_id, "assistant", answer, sources)
        yield sse("sources", {"sources": sources})
        yield sse("done", {"message_id": saved.id})
    except Exception:
        logger.exception("Chat generation failed (session %s)", session_id)
        yield sse("error", {"detail": "Failed to generate a response. Please try again."})


# def stream_chat(user_id: int, session_id: int, title: str, message: str,
#                 doc_ids: list[int] | None, history: list[BaseMessage]) -> Iterator[str]:
#     yield sse("session", {"session_id": session_id, "title": title})
#     try:
#         standalone = condense_question(message, history)
#         # docs = retrieve(standalone, user_id, doc_ids)
#         _SMALL_TALK = {"hi", "hello", "hey", "good morning", "good evening", "good afternoon", "thanks", "thank you"}
#         if message.strip().lower().rstrip("!.?") in _SMALL_TALK:
#             docs = []
#         else:
#             docs = retrieve(standalone, user_id, doc_ids)
#         sources = extract_sources(docs)

#         parts: list[str] = []
#         for token in stream_rag_answer(message, history, docs):
#             parts.append(token)
#             yield sse("token", {"text": token})

#         # Own DB session: the request-scoped one may already be closed while streaming.
#         with SessionLocal() as db:
#             saved = crud.add_message(db, session_id, "assistant", "".join(parts), sources)
#         yield sse("sources", {"sources": sources})
#         yield sse("done", {"message_id": saved.id})
#     except Exception:
#         logger.exception("Chat generation failed (session %s)", session_id)
#         yield sse("error", {"detail": "Failed to generate a response. Please try again."})
