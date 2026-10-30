"""Agent 1 - deterministic-first router for document retrieval, weather and direct answers."""
import logging
import re
from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field

from app.agents.llm import get_llm
from app.agents.prompts import DIRECT_PROMPT, ROUTER_PROMPT
from app.agents.state import AgentState

logger = logging.getLogger(__name__)


class RouteDecision(BaseModel):
    route: Literal["direct", "retrieve", "weather"]
    reason: str = Field(description="One short sentence explaining the choice")


DOCUMENT_PATTERNS = (
    r"\b(uploaded|attached|provided)\s+(document|file|pdf|notes?|report|book)\b",
    r"\b(the|this|that|my)\s+(document|file|pdf|notes?|report|book)\b",
    r"\b(in|from|according\s+to|based\s+on)\s+(the|this|that|my)\s+(document|file|pdf|notes?|report|book)\b",
    r"\b(document|file|pdf|notes?|report)\s+(attached|uploaded)\b",
    r"\b(summarize|summarise|summary|analy[sz]e|review|outline|extract)\b.*\b(document|file|pdf|notes?|report|book)\b",
    r"\b(what|which|where|when|why|how)\b.*\b(document|file|pdf|notes?|report)\b",
    r"\baccording\s+to\s+(my|the|this|that)\s+(upload|document|file|pdf|notes?)\b",
)

# Only clear live/local weather requests; conceptual weather questions stay eligible for KB.
WEATHER_PATTERNS = (
    r"\b(current|currently|live|today|tonight|tomorrow|this\s+week|forecast)\b.*\b(weather|temperature|rain|rainfall|humidity|wind)\b",
    r"\b(weather|temperature|rain|rainfall|humidity|wind)\b.*\b(in|for|at)\s+[\w .'-]+",
    r"\b(is\s+it\s+raining|will\s+it\s+rain|weather\s+forecast)\b",
    r"\b(weather|temperature)\s+(today|tomorrow|now|currently)\b",
)

FOLLOW_UP_PATTERNS = (
    r"\b(what\s+about|how\s+about|and\s+what|explain\s+more|tell\s+me\s+more|continue|elaborate|why\s+is\s+that|what\s+does\s+it\s+mean)\b",
    r"\b(it|this|that|these|those|they|them|its|their)\b",
)


def _message_text(message) -> str:
    """Get readable text from LangChain messages without assuming content is a string."""
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(
            part.get("text", "")
            for part in content
            if isinstance(part, dict) and part.get("type") == "text"
        )
    return str(content or "")


def is_document_query(question: str) -> bool:
    return any(re.search(pattern, question, re.IGNORECASE) for pattern in DOCUMENT_PATTERNS)


def is_weather_query(question: str) -> bool:
    return any(re.search(pattern, question, re.IGNORECASE) for pattern in WEATHER_PATTERNS)


def is_document_follow_up(question: str, history: list) -> bool:
    """Recognize short follow-ups when recent chat clearly concerns retrieved documents."""
    if not history:
        return False
    recent_text = "\n".join(_message_text(m) for m in history[-8:])
    has_document_context = bool(
        re.search(r"\b(document|uploaded|attached|pdf|file|notes|report)\b", recent_text, re.I)
        or re.search(r"\[\d+\]", recent_text)
    )
    is_follow_up = any(re.search(pattern, question, re.IGNORECASE) for pattern in FOLLOW_UP_PATTERNS)
    return has_document_context and is_follow_up


def router_node(state: AgentState, config: RunnableConfig):
    evidence = config["configurable"]["evidence"]
    question = (state.get("question") or "").strip()
    history = state.get("history", [])
    doc_ids = list(evidence.doc_ids or [])
    has_docs = bool(state.get("has_docs") or doc_ids)

    logger.info(
        "Router input: user_id=%s, doc_ids=%s, doc_count=%d, has_docs=%s, question=%r",
        evidence.user_id, doc_ids, len(doc_ids), has_docs, question[:250],
    )

    # Current-turn attachments remain authoritative, matching the original behavior.
    if doc_ids:
        logger.info("Router -> retrieve (current-turn document attachment)")
        return {"route": "retrieve"}

    if has_docs and is_document_query(question):
        logger.info("Router -> retrieve (explicit document intent)")
        return {"route": "retrieve"}

    if has_docs and is_document_follow_up(question, history):
        logger.info("Router -> retrieve (document-context follow-up)")
        return {"route": "retrieve"}

    if is_weather_query(question):
        logger.info("Router -> weather (live weather intent)")
        return {"route": "weather"}

    # No indexed documents means there is no reason to spend an LLM call routing to KB.
    if not has_docs:
        logger.info("Router -> direct (no indexed documents)")
        return {"route": "direct"}

    try:
        decider = get_llm(0).with_structured_output(RouteDecision, method="function_calling")
        decision = decider.invoke(
            [SystemMessage(f"{ROUTER_PROMPT}\n\nThe user HAS indexed documents."),
             *history[-8:], HumanMessage(question)],
            config,
        )
        route = decision.route
        logger.info("Router -> %s (%s)", route, decision.reason)
    except Exception:
        logger.exception("Router LLM failed; falling back to retrieval")
        route = "retrieve"
    return {"route": route}


def route_from_router(state: AgentState) -> str:
    return state["route"]


def direct_answer_node(state: AgentState, config: RunnableConfig):
    reply = get_llm().invoke(
        [SystemMessage(DIRECT_PROMPT), *state["history"], HumanMessage(state["question"])],
        config,
    )
    return {"messages": [reply]}
