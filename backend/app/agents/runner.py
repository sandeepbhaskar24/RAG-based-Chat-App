"""Runs the agent graph and converts LangGraph streams into simple events for chat_service."""
import logging
from collections.abc import Iterator

from langchain_core.messages import AIMessage, AIMessageChunk, BaseMessage, HumanMessage

from app.agents.evidence import Evidence
from app.agents.graph import get_graph
from app.rag.chain import extract_sources

logger = logging.getLogger(__name__)
STREAM_NODES = {"direct_answer", "kb_answer", "weather_agent"}


def _text(msg) -> str:
    content = msg.content
    if isinstance(content, str):
        return content
    return "".join(
        part.get("text", "")
        for part in content
        if isinstance(part, dict) and part.get("type") == "text"
    )


def _tool_status(call: dict) -> str:
    name, args = call["name"], call.get("args", {})
    if name == "search_knowledge_base":
        return f"Searching documents for “{str(args.get('query', ''))[:60]}”…"
    if name == "rewrite_query":
        return "Refining the search query…"
    if name == "check_sources":
        return "Verifying the answer against the sources…"
    if name == "get_weather":
        return f"Fetching live weather for {args.get('location', 'your location')}…"
    return "Working…"


def _normalize_doc_ids(doc_ids) -> list[int]:
    """Normalize attachment IDs once, before creating Evidence and graph state."""
    if not doc_ids:
        return []
    normalized = []
    for value in doc_ids:
        try:
            doc_id = int(value)
        except (TypeError, ValueError):
            logger.warning("Ignoring invalid document ID passed to run_agents: %r", value)
            continue
        if doc_id > 0 and doc_id not in normalized:
            normalized.append(doc_id)
    return normalized


def run_agents(
    question: str,
    history: list[BaseMessage],
    user_id: int,
    doc_ids: list[int] | None,
    has_docs: bool,
) -> Iterator[dict]:
    """`doc_ids` are IDs attached to THIS request; `has_docs` means the user has indexed docs."""
    normalized_doc_ids = _normalize_doc_ids(doc_ids)
    effective_has_docs = bool(has_docs or normalized_doc_ids)

    logger.info(
        "run_agents input: user_id=%s, question=%r, attached_doc_ids=%s, "
        "attached_doc_count=%d, has_docs_arg=%s, effective_has_docs=%s, history_len=%d",
        user_id, question[:250], normalized_doc_ids, len(normalized_doc_ids),
        has_docs, effective_has_docs, len(history or []),
    )

    evidence = Evidence(
        user_id=user_id,
        doc_ids=normalized_doc_ids or None,
        question=question,
    )
    state = {
        "question": question,
        "history": history or [],
        "has_docs": effective_has_docs,
        "messages": [HumanMessage(question)],
        "steps": 0,
    }
    config = {"configurable": {"evidence": evidence}, "recursion_limit": 30}

    route, streamed, final_text = "direct", False, ""
    for mode, payload in get_graph().stream(state, config, stream_mode=["messages", "updates"]):
        if mode == "messages":
            chunk, meta = payload
            if meta.get("langgraph_node") in STREAM_NODES and isinstance(chunk, AIMessageChunk):
                text = _text(chunk)
                if text:
                    streamed = True
                    yield {"type": "token", "text": text}
            continue

        for node, update in payload.items():
            if not isinstance(update, dict):
                continue
            if node == "router":
                route = update.get("route", route)
                label = {
                    "retrieve": "Searching your documents…",
                    "weather": "Checking live weather…",
                }.get(route)
                if label:
                    yield {"type": "status", "text": label}
            elif node == "kb_plan" and update.get("task_type") == "document_summary":
                yield {"type": "status", "text": "Preparing a full-document summary…"}
            elif node == "kb_full_summary":
                messages = update.get("messages") or []
                if messages:
                    last = messages[-1]
                    if isinstance(last, AIMessage) and not last.tool_calls:
                        final_text = _text(last)
            elif node in ("kb_agent", "weather_agent"):
                messages = update.get("messages") or []
                if messages:
                    last = messages[-1]
                    for call in getattr(last, "tool_calls", None) or []:
                        yield {"type": "status", "text": _tool_status(call)}
            if node in STREAM_NODES:
                messages = update.get("messages") or []
                if messages:
                    last = messages[-1]
                    if isinstance(last, AIMessage) and not last.tool_calls:
                        final_text = _text(last)

    if not streamed and final_text:
        yield {"type": "token", "text": final_text}

    yield {
        "type": "final",
        "route": route,
        "sources": extract_sources(evidence.docs) if route == "retrieve" else [],
    }
