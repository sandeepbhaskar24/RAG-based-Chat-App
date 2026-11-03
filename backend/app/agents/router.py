"""Agent 1 - the router. One LLM call decides: DIRECT, RAG, CLARIFY (or WEATHER)."""
import logging
from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field

from app.agents.context import RequestContext, emit, get_ctx
from app.agents.llm import call_structured, stream_answer
from app.agents.prompts import DIRECT_PROMPT, ROUTER_PROMPT
from app.agents.state import AgentState
from app.core.config import settings
from app.db import crud
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)

STATUS = {"RAG": "Searching your documents\u2026", "OVERVIEW": "Reading your documents\u2026",
          "WEATHER": "Checking live weather\u2026"}


class RouteDecision(BaseModel):
    route: Literal["DIRECT", "RAG", "OVERVIEW", "CLARIFY", "WEATHER"]
    reason: str = Field(description="One short sentence explaining the choice")
    confidence: float = Field(default=0.5, description="0 to 1")
    clarification_question: str = Field(default="", description="Only for CLARIFY")


def decide_route(ctx: RequestContext, question: str, history: list, has_docs: bool) -> RouteDecision:
    docs_note = ("The user HAS uploaded documents." if has_docs
                 else "The user has NOT uploaded any documents.")
    if ctx.doc_ids:
        docs_note += " The user attached a document to this message."
    try:
        with ctx.stage("route"):
            decision = call_structured(
                ctx.budget, "route", RouteDecision,
                [SystemMessage(f"{ROUTER_PROMPT}\n\n{docs_note}"), *history[-6:], HumanMessage(question)])
    except Exception:
        logger.exception("Router failed; using a safe default")
        return RouteDecision(route="RAG" if has_docs else "DIRECT", reason="router error", confidence=0.0)

    # Low-confidence DIRECT while the user has documents: search instead of guessing.
    if decision.route == "DIRECT" and has_docs and decision.confidence < settings.ROUTER_MIN_CONFIDENCE:
        decision.route = "RAG"
    logger.info("Router -> %s (%.2f): %s", decision.route, decision.confidence, decision.reason)
    return decision


# ── Graph nodes ─────────────────────────────────────────────────────────────────

def router_node(state: AgentState, config: RunnableConfig):
    decision = decide_route(get_ctx(config), state["question"], state["history"], state["has_docs"])
    if decision.route in STATUS:
        emit("status", STATUS[decision.route])
    return {"route": decision.route, "clarification": decision.clarification_question}


def route_from_router(state: AgentState) -> str:
    """Conditional edge: which branch of the graph runs next."""
    if state["route"] in ("RAG", "OVERVIEW"):
        if not state.get("has_docs"):
            return "no_answer"                  # nothing uploaded at all
        if state["route"] == "OVERVIEW":
            return "summarize"                  # whole-document question -> read it, don't search it
    return state["route"].lower()               # direct | rag | clarify | weather


def user_document_names(user_id: int, limit: int = 20) -> list[str]:
    """File names of the user's ready documents (cheap DB read, no LLM)."""
    try:
        with SessionLocal() as db:
            docs = crud.list_documents(db, user_id)
        names = [d.filename for d in docs if d.status == "ready"]
    except Exception:
        logger.exception("Could not list documents")
        return []
    extra = len(names) - limit
    return names[:limit] + ([f"...and {extra} more"] if extra > 0 else [])


def direct_answer_node(state: AgentState, config: RunnableConfig):
    """DIRECT: this call IS the final generation (no retrieval).

    The model is told the user's file NAMES so it can answer "what documents/knowledge base do I have?".
    """
    ctx = get_ctx(config)
    documents = "\n".join(f"- {n}" for n in user_document_names(ctx.user_id)) or "(none uploaded yet)"
    messages = [SystemMessage(DIRECT_PROMPT.format(documents=documents)),
                *state["history"], HumanMessage(state["question"])]
    parts = []
    for text in stream_answer(ctx.budget, "direct_answer", messages):
        parts.append(text)
        emit("token", text)
    return {"answer": "".join(parts)}


def clarify_node(state: AgentState):
    """CLARIFY: the router already wrote the question, so no extra LLM call."""
    question = (state.get("clarification", "").strip()
                or "Could you tell me a bit more about what you're looking for?")
    emit("token", question)
    return {"answer": question}