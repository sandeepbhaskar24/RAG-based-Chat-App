"""Cross-encoder reranking (no generative LLM involved).

Uses fastembed's ONNX cross-encoder (small, CPU-friendly). If it can't be loaded, we fall back to
the RRF order and leave `rerank_score` unset - the RAG agent then treats retrieval as "uncertain".
"""
import logging
import math
from functools import lru_cache

from langchain_core.documents import Document

from app.core.config import settings

logger = logging.getLogger(__name__)


@lru_cache
def _model():
    try:
        from fastembed.rerank.cross_encoder import TextCrossEncoder

        return TextCrossEncoder(model_name=settings.RERANK_MODEL)
    except Exception:
        logger.warning("Cross-encoder unavailable; falling back to RRF order", exc_info=True)
        return None


def rerank(question: str, docs: list[Document], top_k: int) -> list[Document]:
    """Score every chunk against the ORIGINAL question; keep the best `top_k`.

    Adds metadata["rerank_score"] in 0..1 (sigmoid of the model's raw score).
    """
    if not docs:
        return []
    model = _model()
    if model is None:
        return docs[:top_k]
    try:
        raw = list(model.rerank(question, [d.page_content for d in docs]))
    except Exception:
        logger.exception("Reranking failed; falling back to RRF order")
        return docs[:top_k]
    for d, s in zip(docs, raw):
        d.metadata["rerank_score"] = 1.0 / (1.0 + math.exp(-float(s)))
    return sorted(docs, key=lambda d: d.metadata["rerank_score"], reverse=True)[:top_k]