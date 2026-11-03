"""Retrieval: dense (semantic) vector search, optionally + BM25 keywords, merged with RRF.

BM25 is OFF by default (settings.USE_BM25 = False), so retrieval is semantic search only.
With several rewritten queries, RRF still merges the per-query result lists into one ranking.

Both searches are restricted to the user's own chunks (and optionally selected documents) by
`build_filter`, so authorization is applied BEFORE any text is returned.
"""
import logging
import re
import threading
from concurrent.futures import ThreadPoolExecutor

from langchain_core.documents import Document

from app.core.config import settings
from app.rag.retriever import retrieve
from app.rag.vector_store import build_filter, ensure_collection, get_client

logger = logging.getLogger(__name__)
_WORD = re.compile(r"\w+")


def _tokens(text: str) -> list[str]:
    return _WORD.findall(text.lower())


def doc_key(d: Document):
    """Stable identity for a chunk: its Qdrant point id, else page + text."""
    return d.metadata.get("_id") or (d.metadata.get("page"), " ".join(d.page_content.split()))


def merge_unique(*lists: list[Document]) -> list[Document]:
    seen, out = set(), []
    for lst in lists:
        for d in lst:
            k = doc_key(d)
            if k not in seen:
                seen.add(k)
                out.append(d)
    return out


def reciprocal_rank_fusion(result_lists: list[list[Document]], k: int | None = None) -> list[Document]:
    """score(doc) = sum over lists of 1 / (k + rank). Duplicates collapse into one chunk."""
    k = k or settings.RRF_K
    scores: dict = {}
    docs: dict = {}
    for lst in result_lists:
        for rank, d in enumerate(lst, start=1):
            key = doc_key(d)
            docs.setdefault(key, d)
            scores[key] = scores.get(key, 0.0) + 1.0 / (k + rank)
    ordered = sorted(scores, key=scores.get, reverse=True)
    return [docs[key] for key in ordered[: settings.MAX_CANDIDATES]]


def load_corpus(user_id: int, doc_ids: list[int] | None) -> list[Document]:
    """Read the user's chunks out of Qdrant (text only) so BM25 can index them."""
    client = get_client()
    ensure_collection(client)
    flt, docs, offset = build_filter(user_id, doc_ids), [], None
    while True:
        points, offset = client.scroll(
            settings.QDRANT_COLLECTION, scroll_filter=flt, limit=500, offset=offset,
            with_payload=True, with_vectors=False)
        for p in points:
            payload = p.payload or {}
            meta = dict(payload.get("metadata") or {})
            meta["_id"] = str(p.id)
            docs.append(Document(page_content=payload.get("page_content", ""), metadata=meta))
        if offset is None:
            return docs


class KeywordIndex:
    def __init__(self, docs: list[Document]):
        from rank_bm25 import BM25Okapi          # imported lazily: only needed when USE_BM25 is on

        self.docs = docs
        self.bm25 = BM25Okapi([_tokens(d.page_content) or [""] for d in docs]) if docs else None

    def search(self, query: str, k: int) -> list[Document]:
        if self.bm25 is None:
            return []
        scores = self.bm25.get_scores(_tokens(query))
        top = sorted(range(len(scores)), key=scores.__getitem__, reverse=True)[:k]
        return [self.docs[i] for i in top if scores[i] > 0]


class HybridRetriever:
    """One per request. The BM25 index is built lazily the first time it is needed and reused
    by the retry. (It is rebuilt per request, which is fine for personal libraries; cache it
    per user if the corpus gets large.)"""

    def __init__(self, user_id: int, doc_ids: list[int] | None):
        self.user_id, self.doc_ids = user_id, doc_ids
        self._index: KeywordIndex | None = None
        self._lock = threading.Lock()

    def _keyword_search(self, query: str) -> list[Document]:
        with self._lock:
            if self._index is None:
                self._index = KeywordIndex(load_corpus(self.user_id, self.doc_ids))
        return self._index.search(query, settings.BM25_TOP_K)

    def search(self, queries: list[str]) -> list[Document]:
        """Run the search for every query IN PARALLEL, then fuse with RRF."""
        use_bm25 = getattr(settings, "USE_BM25", False)
        with ThreadPoolExecutor(max_workers=max(1, len(queries)) * (2 if use_bm25 else 1)) as pool:
            futures = []
            for q in queries:
                futures.append(pool.submit(retrieve, q, self.user_id, self.doc_ids, settings.DENSE_TOP_K))
                if use_bm25:
                    futures.append(pool.submit(self._keyword_search, q))
            result_lists = []
            for f in futures:
                try:
                    result_lists.append(f.result())
                except Exception:
                    logger.exception("One retrieval branch failed; continuing with the others")
        return reciprocal_rank_fusion(result_lists)