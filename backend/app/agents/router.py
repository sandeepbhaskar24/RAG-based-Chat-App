"""Agent 1 - router: vector search, weather, or answer directly?"""
import logging
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


def router_node(state: AgentState, config: RunnableConfig):
    evidence = config["configurable"]["evidence"]
    if evidence.doc_ids:                       # user attached a file -> always search it
        return {"route": "retrieve"}

    docs_note = ("The user HAS uploaded documents." if state.get("has_docs")
                 else "The user has NOT uploaded any documents.")
    try:
        decider = get_llm(0).with_structured_output(RouteDecision, method="function_calling")
        decision = decider.invoke(
            [SystemMessage(f"{ROUTER_PROMPT}\n\n{docs_note}"),
             *state["history"][-6:],
             HumanMessage(state["question"])],
            config,
        )
        route = decision.route
        logger.info("Router -> %s (%s)", route, decision.reason)
    except Exception:
        logger.exception("Router failed; falling back to retrieval")
        route = "retrieve"
    return {"route": route}


def route_from_router(state: AgentState) -> str:
    return state["route"]


def direct_answer_node(state: AgentState, config: RunnableConfig):
    reply = get_llm().invoke(
        [SystemMessage(DIRECT_PROMPT), *state["history"], HumanMessage(state["question"])], config)
    return {"messages": [reply]}