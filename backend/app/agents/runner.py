"""Runs the LangGraph and converts its stream into simple events for chat_service.

Yields dicts:
  {"type": "status", "text": "..."}   progress hint
  {"type": "token",  "text": "..."}   piece of the answer
  {"type": "final",  "route", "sources", "citations", "grounded", "llm_calls"}

How streaming works: nodes call emit(...), which LangGraph delivers as "custom" events.
The "values" events carry the full state after each step; the last one is the finished state.
"""
import logging
import time
from collections.abc import Iterator

from langchain_core.messages import BaseMessage

from app.agents.context import RequestContext
from app.agents.graph import get_graph

logger = logging.getLogger(__name__)


def run_agents(question: str, history: list[BaseMessage], user_id: int,
               doc_ids: list[int] | None, has_docs: bool) -> Iterator[dict]:
    start = time.perf_counter()
    ctx = RequestContext(user_id=user_id, doc_ids=doc_ids)
    state = {"question": question, "history": history, "has_docs": has_docs or bool(doc_ids)}
    config = {"configurable": {"ctx": ctx}, "recursion_limit": 25}   # the graph's only loop is the 1 retry

    final_state: dict = state
    for mode, payload in get_graph().stream(state, config, stream_mode=["custom", "values"]):
        if mode == "custom":
            yield payload
        else:
            final_state = payload

    route = final_state.get("route", "DIRECT")
    logger.info("request done route=%s llm_calls=%d/%d (%s) total=%.0f ms", route,
                ctx.budget.used, ctx.budget.limit, ",".join(ctx.budget.labels),
                (time.perf_counter() - start) * 1000)
    yield {"type": "final", "route": route.lower(),
           "sources": final_state.get("sources", []),
           "citations": final_state.get("citations", []),
           "grounded": final_state.get("grounded"),
           "llm_calls": ctx.budget.used}