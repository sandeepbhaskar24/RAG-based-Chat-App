"""Wires the three agents into ONE LangGraph.

START -> router --DIRECT---> direct_answer -> END
                --CLARIFY--> clarify -> END
                --WEATHER--> weather_extract -> weather_fetch -> weather_answer -> END
                --OVERVIEW-> summarize -> END
                --RAG------> rewrite -> search -> assess -> generate -> verify -> END
                                          ^          |
                                          +-- retry <+  (at most once)
                                                     +--> no_answer -> END

One flat graph (not nested subgraphs) keeps the flow easy to read in one place.
Nodes push live events (status / token) with emit(); runner.py turns them into the SSE stream.
"""
from functools import lru_cache

from langgraph.graph import END, START, StateGraph

from app.agents.rag_agent import (assess_node, generate_node, no_answer_node, retry_node,
                                  rewrite_node, route_after_assess, route_after_retry,
                                  search_node, summarize_node, verify_node)
from app.agents.router import clarify_node, direct_answer_node, route_from_router, router_node
from app.agents.state import AgentState
from app.agents.weather_agent import (route_after_extract, route_after_fetch, weather_answer_node,
                                      weather_extract_node, weather_fetch_node)


@lru_cache
def get_graph():
    g = StateGraph(AgentState)

    # Agent 1: router (+ the two routes that need no retrieval)
    g.add_node("router", router_node)
    g.add_node("direct_answer", direct_answer_node)
    g.add_node("clarify", clarify_node)

    # Agent 2: RAG
    g.add_node("rewrite", rewrite_node)
    g.add_node("search", search_node)
    g.add_node("assess", assess_node)
    g.add_node("retry", retry_node)
    g.add_node("generate", generate_node)
    g.add_node("verify", verify_node)
    g.add_node("no_answer", no_answer_node)
    g.add_node("summarize", summarize_node)

    # Agent 3: weather
    g.add_node("weather_extract", weather_extract_node)
    g.add_node("weather_fetch", weather_fetch_node)
    g.add_node("weather_answer", weather_answer_node)

    # Routing
    g.add_edge(START, "router")
    g.add_conditional_edges("router", route_from_router, {
        "direct": "direct_answer", "clarify": "clarify", "rag": "rewrite",
        "weather": "weather_extract", "no_answer": "no_answer",
        "summarize": "summarize"})

    # RAG flow
    g.add_edge("rewrite", "search")
    g.add_edge("search", "assess")
    g.add_conditional_edges("assess", route_after_assess,
                            {"generate": "generate", "retry": "retry", "no_answer": "no_answer"})
    g.add_conditional_edges("retry", route_after_retry, {"search": "search", "no_answer": "no_answer"})
    g.add_edge("generate", "verify")

    # Weather flow
    g.add_conditional_edges("weather_extract", route_after_extract, {"fetch": "weather_fetch", END: END})
    g.add_conditional_edges("weather_fetch", route_after_fetch, {"answer": "weather_answer", END: END})

    # Everything ends here
    for node in ("direct_answer", "clarify", "verify", "no_answer", "weather_answer", "summarize"):
        g.add_edge(node, END)

    return g.compile()