"""Runs the agent graph and converts LangGraph streams into simple events for chat_service.

Yields dicts:
  {"type": "status", "text": "..."}      progress hint ("Searching your documents...")
  {"type": "token",  "text": "..."}      piece of the final answer
  {"type": "final",  "route": "...", "sources": [...]}
"""
from collections.abc import Iterator

from langchain_core.messages import AIMessage, AIMessageChunk, BaseMessage, HumanMessage

from app.agents.evidence import Evidence
from app.agents.graph import get_graph
from app.rag.chain import extract_sources

# Only these nodes write text the user should see; everything else (router, tool-calling
# turns of the KB agent, judges) stays internal.
STREAM_NODES = {"direct_answer", "kb_answer", "weather_agent"}


def _text(msg) -> str:
    c = msg.content
    if isinstance(c, str):
        return c
    return "".join(p.get("text", "") for p in c if isinstance(p, dict) and p.get("type") == "text")


def _tool_status(call: dict) -> str:
    name, args = call["name"], call.get("args", {})
    if name == "search_knowledge_base":
        return f"Searching documents for \u201c{str(args.get('query', ''))[:60]}\u201d\u2026"
    if name == "rewrite_query":
        return "Refining the search query\u2026"
    if name == "check_sources":
        return "Verifying the answer against the sources\u2026"
    if name == "get_weather":
        return f"Fetching live weather for {args.get('location', 'your location')}\u2026"
    return "Working\u2026"


def run_agents(question: str, history: list[BaseMessage], user_id: int,
               doc_ids: list[int] | None, has_docs: bool) -> Iterator[dict]:
    evidence = Evidence(user_id=user_id, doc_ids=doc_ids, question=question)
    state = {"question": question, "history": history, "has_docs": has_docs,
             "messages": [HumanMessage(question)], "steps": 0}
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

        for node, update in payload.items():             # mode == "updates"
            if not isinstance(update, dict):
                continue
            if node == "router":
                route = update.get("route", route)
                label = {"retrieve": "Searching your documents\u2026",
                         "weather": "Checking live weather\u2026"}.get(route)
                if label:
                    yield {"type": "status", "text": label}
            elif node in ("kb_agent", "weather_agent"):
                last = update["messages"][-1]
                for call in getattr(last, "tool_calls", None) or []:
                    yield {"type": "status", "text": _tool_status(call)}
            if node in STREAM_NODES:
                last = update["messages"][-1]
                if isinstance(last, AIMessage) and not last.tool_calls:
                    final_text = _text(last)

    if not streamed and final_text:                      # model that doesn't stream
        yield {"type": "token", "text": final_text}

    yield {"type": "final", "route": route,
           "sources": extract_sources(evidence.docs) if route == "retrieve" else []}