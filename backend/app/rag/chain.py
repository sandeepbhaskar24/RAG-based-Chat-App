"""History-aware RAG: condense follow-up -> (retrieve elsewhere) -> stream the answer."""
from collections.abc import Iterator

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.rag.prompts import CONDENSE_PROMPT, RAG_PROMPT


def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE,
        api_key=settings.OPENAI_API_KEY or None,
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


def format_context(docs: list[Document]) -> str:
    if not docs:
        return "(no relevant context found)"
    blocks = []
    for i, doc in enumerate(docs, start=1):
        meta = doc.metadata
        page = f", page {meta['page']}" if meta.get("page") else ""
        blocks.append(f"[{i}] (source: {meta.get('filename', 'unknown')}{page})\n{doc.page_content}")
    return "\n\n".join(blocks)


def extract_sources(docs: list[Document]) -> list[dict]:
    """Deduplicated citation list returned to the UI (numbering matches the prompt's [n])."""
    sources, seen = [], set()
    for i, doc in enumerate(docs, start=1):
        meta = doc.metadata
        key = (meta.get("doc_id"), meta.get("page"))
        if key in seen:
            continue
        seen.add(key)
        sources.append(
            {
                "ref": i,
                "doc_id": meta.get("doc_id"),
                "filename": meta.get("filename"),
                "page": meta.get("page"),
                "snippet": doc.page_content[:200],
                "score": meta.get("score"),
            }
        )
    return sources


def stream_rag_answer(question: str, history: list[BaseMessage], docs: list[Document]) -> Iterator[str]:
    chain = RAG_PROMPT | get_llm() | StrOutputParser()
    yield from chain.stream(
        {"context": format_context(docs), "history": history, "question": question}
    )
