"""Flat LangGraph with a deterministic KB fast path and an evidence-checked advanced path."""
from functools import lru_cache

from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from app.agents.kb_agent import (
    KB_TOOLS,
    kb_agent_node,
    kb_answer_node,
    kb_nudge_node,
    kb_plan_node,
    kb_full_document_summary_node,
    kb_simple_retrieve_node,
    route_after_kb_agent,
    route_after_kb_plan,
)
from app.agents.router import direct_answer_node, route_from_router, router_node
from app.agents.state import AgentState
from app.agents.weather_agent import (
    route_after_weather_agent,
    weather_agent_node,
    weather_tool_node,
)


@lru_cache
def get_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("direct_answer", direct_answer_node)

    graph.add_node("kb_plan", kb_plan_node)
    graph.add_node("kb_simple_retrieve", kb_simple_retrieve_node)
    graph.add_node("kb_full_summary", kb_full_document_summary_node)
    graph.add_node("kb_agent", kb_agent_node)
    graph.add_node("kb_tools", ToolNode(KB_TOOLS))
    graph.add_node("kb_nudge", kb_nudge_node)
    graph.add_node("kb_answer", kb_answer_node)

    graph.add_node("weather_agent", weather_agent_node)
    graph.add_node("weather_tools", weather_tool_node)

    graph.add_edge(START, "router")
    graph.add_conditional_edges(
        "router",
        route_from_router,
        {"direct": "direct_answer", "retrieve": "kb_plan", "weather": "weather_agent"},
    )

    graph.add_conditional_edges(
        "kb_plan",
        route_after_kb_plan,
        {"kb_agent": "kb_agent", "kb_simple_retrieve": "kb_simple_retrieve",
         "kb_full_summary": "kb_full_summary"},
    )
    graph.add_edge("kb_simple_retrieve", "kb_answer")
    graph.add_edge("kb_full_summary", END)

    graph.add_conditional_edges(
        "kb_agent",
        route_after_kb_agent,
        ["kb_tools", "kb_nudge", "kb_answer"],
    )
    graph.add_edge("kb_tools", "kb_agent")
    graph.add_edge("kb_nudge", "kb_agent")
    graph.add_edge("kb_answer", END)

    graph.add_conditional_edges("weather_agent", route_after_weather_agent, ["weather_tools", END])
    graph.add_edge("weather_tools", "weather_agent")

    graph.add_edge("direct_answer", END)
    return graph.compile()
