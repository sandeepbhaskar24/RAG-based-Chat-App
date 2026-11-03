"""Per-request helpers shared by every node.

The graph STATE holds data that changes step by step (queries, docs, answer...).
The CONTEXT holds per-request tools: the LLM call budget and the retriever. It is passed
to the graph via config["configurable"]["ctx"], so nodes read it with get_ctx(config).
"""
import logging
import time
from contextlib import contextmanager
from dataclasses import dataclass, field

from langchain_core.runnables import RunnableConfig
from langgraph.config import get_stream_writer

from app.agents.llm import LLMBudget
from app.rag.hybrid import HybridRetriever

logger = logging.getLogger(__name__)


@dataclass
class RequestContext:
    user_id: int
    doc_ids: list[int] | None
    budget: LLMBudget = field(default_factory=LLMBudget)
    retriever: HybridRetriever = field(init=False)
    t0: float = field(default_factory=time.perf_counter)                      # NEW
    timings: list[tuple[str, float, float]] = field(default_factory=list)     # NEW (name, start_ms, ms)

    def __post_init__(self):
        self.retriever = HybridRetriever(self.user_id, self.doc_ids)

    @contextmanager
    def stage(self, name: str):
        """Log how long a pipeline stage took."""
        start = time.perf_counter()
        try:
            yield
        finally:
            end = time.perf_counter()
            self.timings.append((name, (start - self.t0) * 1000, (end - start) * 1000))
            logger.info("stage [%s] %.0f ms", name, (end - start) * 1000)

    def log_summary(self) -> None:                                            # NEW
        total = (time.perf_counter() - self.t0) * 1000
        lines = ["", " +-- REQUEST TIMELINE ─────────────────────────────────────"]
        for name, at, ms in self.timings:
            lines.append(f"│ {name:<18} start +{at:7.0f} ms   took {ms:7.0f} ms")
        lines.append(" |-- LLM CALLS ────────────────────────────────────────────")
        for c in self.budget.calls:
            ttft = f"{c['ttft_ms']:.0f} ms" if c["ttft_ms"] is not None else "-"
            lines.append(f"│ {c['label']:<18} total {c['total_ms']:7.0f} ms   first token {ttft}")
        lines.append(f" +-- agent graph total: {total:.0f} ms "
                     f"({self.budget.used}/{self.budget.limit} LLM calls)")
        logger.info("\n".join(lines))


def get_ctx(config: RunnableConfig) -> RequestContext:
    return config["configurable"]["ctx"]


def emit(event_type: str, text: str) -> None:
    """Send a live event to the client ("status" hint or answer "token")."""
    get_stream_writer()({"type": event_type, "text": text})