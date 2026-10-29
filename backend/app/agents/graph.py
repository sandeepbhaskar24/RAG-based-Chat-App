"""Wires the three agents into one LangGraph.

START -> router --direct---> direct_answer -> END
                 --retrieve-> kb_agent <-> kb_tools / kb_nudge -> kb_answer -> END
                 --weather--> weather_agent <-> weather_tools -> END

One flat graph (not nested subgraphs) so token streaming works with a simple node filter.
"""
from functools import lru_cache

from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from app.agents.kb_agent import (KB_TOOLS, kb_agent_node, kb_answer_node, kb_nudge_node,
                                 route_after_kb_agent)
from app.agents.router import direct_answer_node, route_from_router, router_node
from app.agents.state import AgentState
from app.agents.weather_agent import (route_after_weather_agent, weather_agent_node,
                                      weather_tool_node)


@lru_cache
def get_graph():
    g = StateGraph(AgentState)

    g.add_node("router", router_node)
    g.add_node("direct_answer", direct_answer_node)

    g.add_node("kb_agent", kb_agent_node)
    g.add_node("kb_tools", ToolNode(KB_TOOLS))
    g.add_node("kb_nudge", kb_nudge_node)
    g.add_node("kb_answer", kb_answer_node)

    g.add_node("weather_agent", weather_agent_node)
    g.add_node("weather_tools", weather_tool_node)

    g.add_edge(START, "router")
    g.add_conditional_edges("router", route_from_router,
                            {"direct": "direct_answer", "retrieve": "kb_agent", "weather": "weather_agent"})

    g.add_conditional_edges("kb_agent", route_after_kb_agent, ["kb_tools", "kb_nudge", "kb_answer"])
    g.add_edge("kb_tools", "kb_agent")          # retrieval loop
    g.add_edge("kb_nudge", "kb_agent")
    g.add_edge("kb_answer", END)

    g.add_conditional_edges("weather_agent", route_after_weather_agent, ["weather_tools", END])
    g.add_edge("weather_tools", "weather_agent")

    g.add_edge("direct_answer", END)
    return g.compile()