"""The data that flows through the graph. Each node returns only the keys it changes."""
from typing import Literal, TypedDict

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage


class AgentState(TypedDict, total=False):
    # ── input (set by runner.py) ──
    question: str
    history: list[BaseMessage]              # prior chat turns (token-budgeted)
    has_docs: bool                          # does the user have any ready document?

    # ── Agent 1: router ──
    route: Literal["DIRECT", "RAG", "CLARIFY", "WEATHER"]
    clarification: str                      # question to ask when route == CLARIFY

    # ── Agent 2: RAG ──
    queries: list[str]                      # search queries for the current attempt
    candidates: list[Document]              # fused (pre-rerank) chunks, grows on retry
    docs: list[Document]                    # reranked best chunks
    evaluation: object                      # Evaluation (see rag_agent.py)
    retried: bool                           # True after the single allowed retry
    context_text: str                       # numbered excerpts given to the final LLM
    used_docs: list[Document]               # chunk i here == citation [i + 1]

    # ── Agent 3: weather ──
    weather: object                         # WeatherRequest (location, units, days)
    report: str                             # raw weather data fetched from Open-Meteo

    # ── output ──
    answer: str
    sources: list[dict]
    citations: list[dict]
    grounded: bool | None