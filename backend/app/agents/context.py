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
    doc_ids: list[int] | None                 # set when the user attached a document
    budget: LLMBudget = field(default_factory=LLMBudget)
    retriever: HybridRetriever = field(init=False)

    def __post_init__(self):
        self.retriever = HybridRetriever(self.user_id, self.doc_ids)

    @contextmanager
    def stage(self, name: str):
        """Log how long a pipeline stage took."""
        start = time.perf_counter()
        try:
            yield
        finally:
            logger.info("stage [%s] %.0f ms", name, (time.perf_counter() - start) * 1000)


def get_ctx(config: RunnableConfig) -> RequestContext:
    return config["configurable"]["ctx"]


def emit(event_type: str, text: str) -> None:
    """Send a live event to the client ("status" hint or answer "token")."""
    get_stream_writer()({"type": event_type, "text": text})