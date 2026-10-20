"""Rebuild chat history for the LLM, trimmed to a token budget (newest messages win)."""
from functools import lru_cache

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db import crud


@lru_cache
def _encoder():
    try:
        import tiktoken

        return tiktoken.get_encoding("cl100k_base")
    except Exception:  # offline / encoding not cached -> fall back to a rough estimate
        return None


def count_tokens(text: str) -> int:
    enc = _encoder()
    return len(enc.encode(text)) if enc else max(1, len(text) // 4)


def load_history(db: Session, session_id: int) -> list[BaseMessage]:
    rows = crud.recent_messages(db, session_id, limit=40)
    kept, total = [], 0
    for row in reversed(rows):  # newest first
        total += count_tokens(row.content)
        if total > settings.HISTORY_TOKEN_BUDGET:
            break
        kept.append(row)
    kept.reverse()
    return [HumanMessage(r.content) if r.role == "user" else AIMessage(r.content) for r in kept]
