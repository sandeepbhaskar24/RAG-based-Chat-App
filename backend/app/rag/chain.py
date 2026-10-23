"""History-aware RAG: condense follow-up -> (retrieve elsewhere) -> stream the answer."""
from collections.abc import Iterator

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.rag.prompts import CONDENSE_PROMPT, RAG_PROMPT

from sqlalchemy import select

from app.db.models import Document as DocRow
from app.db.session import SessionLocal


def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE,
        api_key=settings.OPENROUTER_API_KEY or None,
        base_url=settings.OPENAI_BASE_URL,
        max_retries=2,
        streaming=True,
    )


def condense_question(question: str, history: list[BaseMessage]) -> str:
    """Rewrite a follow-up ('what about its price?') into a standalone search query."""
    if not history:
        return question
    chain = CONDENSE_PROMPT | get_llm() | StrOutputParser()
    rewritten = chain.invoke({"history": history[-6:], "question": question}).strip()
    return rewritten or question

def _filename_map(docs: list[Document]) -> dict[int, str]:
    ids = {i for d in docs for i in d.metadata.get("doc_ids", [])}
    if not ids:
        return {}
    with SessionLocal() as db:
        rows = db.execute(select(DocRow.id, DocRow.filename).where(DocRow.id.in_(ids))).all()
    return dict(rows)


def _names(meta: dict, names: dict[int, str]) -> str:
    return ", ".join(names.get(i, "unknown") for i in meta.get("doc_ids", [])) or "unknown"


def format_context(docs: list[Document]) -> str:
    if not docs:
        return "(no relevant context found)"
    names = _filename_map(docs)
    blocks = []
    for i, doc in enumerate(docs, start=1):
        meta = doc.metadata
        page = f", page {meta['page']}" if meta.get("page") else ""
        blocks.append(f"[{i}] (source: {_names(meta, names)}{page})\n{doc.page_content}")
    return "\n\n".join(blocks)


def extract_sources(docs: list[Document]) -> list[dict]:
    names = _filename_map(docs)
    sources, seen = [], set()
    for i, doc in enumerate(docs, start=1):
        meta = doc.metadata
        dids = meta.get("doc_ids", [])
        key = (tuple(dids), meta.get("page"), doc.page_content[:80])
        if key in seen:
            continue
        seen.add(key)
        sources.append({
            "ref": i,
            "doc_id": dids[0] if dids else None,
            "doc_ids": dids,
            "filename": _names(meta, names),
            "page": meta.get("page"),
            "snippet": doc.page_content[:200],
            "score": meta.get("score"),
        })
    return sources


def stream_rag_answer(question: str, history: list[BaseMessage], docs: list[Document]) -> Iterator[str]:
    chain = RAG_PROMPT | get_llm() | StrOutputParser()
    yield from chain.stream(
        {"context": format_context(docs), "history": history, "question": question}
    )
