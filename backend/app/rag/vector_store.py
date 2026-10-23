"""Qdrant client, collection bootstrap and per-user filtering helpers.

langchain-qdrant stores each chunk as {"page_content": ..., "metadata": {...}},
so payload filters use keys like "metadata.user_id".
"""
import itertools
from collections import defaultdict

from sqlalchemy import delete, select

from app.db.models import ChunkRef

import logging
import threading
from functools import lru_cache

from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    FilterSelector,
    MatchAny,
    MatchValue,
    PayloadSchemaType,
    VectorParams,
    PointIdsList
)

from app.core.config import settings
from app.rag.embeddings import get_embeddings

logger = logging.getLogger(__name__)
_lock = threading.Lock()

USER_KEY = "metadata.user_id"
DOC_KEY = "metadata.doc_ids"


@lru_cache
def get_client() -> QdrantClient:
    if settings.QDRANT_URL in ("", ":memory:"):
        return QdrantClient(":memory:")
    return QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)


def ensure_collection(client: QdrantClient) -> None:
    name = settings.QDRANT_COLLECTION
    with _lock:
        if client.collection_exists(name):
            return
        client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=settings.EMBEDDING_DIM, distance=Distance.COSINE),
        )
        for field in (USER_KEY, DOC_KEY):
            try:
                client.create_payload_index(name, field_name=field, field_schema=PayloadSchemaType.INTEGER)
            except Exception:  # pragma: no cover - index is an optimisation only
                logger.warning("Could not create payload index on %s", field)


@lru_cache
def get_vector_store() -> QdrantVectorStore:
    client = get_client()
    ensure_collection(client)
    return QdrantVectorStore(
        client=client,
        collection_name=settings.QDRANT_COLLECTION,
        embedding=get_embeddings(),
    )


def reset_caches() -> None:
    """Used by tests (and handy after changing settings)."""
    get_vector_store.cache_clear()
    get_client.cache_clear()


def build_filter(user_id: int, doc_ids: list[int] | None = None) -> Filter:
    must = [FieldCondition(key=USER_KEY, match=MatchValue(value=user_id))]
    if doc_ids:
        must.append(FieldCondition(key=DOC_KEY, match=MatchAny(any=list(doc_ids))))
    return Filter(must=must)

def _batched(items, n=500):
    it = iter(items)
    while batch := list(itertools.islice(it, n)):
        yield batch

def sync_doc_ids(db, point_ids: list[str]) -> None:
    """Make each point's payload `doc_ids` equal to what MySQL says (MySQL is the source of truth)."""
    if not point_ids:
        return
    by_point = defaultdict(list)
    for batch in _batched(point_ids):
        rows = db.execute(
            select(ChunkRef.point_id, ChunkRef.doc_id).where(ChunkRef.point_id.in_(batch))
        ).all()
        for pid, did in rows:
            by_point[pid].append(did)

    groups = defaultdict(list)                  # same doc_ids list -> one Qdrant call
    for pid, dids in by_point.items():
        groups[tuple(sorted(dids))].append(pid)

    client = get_client()
    for dids, pids in groups.items():
        client.set_payload(
            settings.QDRANT_COLLECTION,
            payload={"doc_ids": list(dids)},
            points=pids,
            key="metadata",                      # langchain-qdrant nests metadata here
        )

def release_points(db, doc_id: int, point_ids: list[str]) -> None:
    """Drop this document's claim on the given points; delete points nobody else uses."""
    if not point_ids:
        return
    orphans, shared = [], []
    for batch in _batched(point_ids):
        used = {r for (r,) in db.execute(
            select(ChunkRef.point_id).where(ChunkRef.point_id.in_(batch), ChunkRef.doc_id != doc_id)
        )}
        for p in batch:
            (shared if p in used else orphans).append(p)

    if orphans:   # Qdrant first: if this raises, MySQL is untouched and the caller can retry
        get_client().delete(
            collection_name=settings.QDRANT_COLLECTION,
            points_selector=PointIdsList(points=orphans),
        )
    for batch in _batched(point_ids):
        db.execute(delete(ChunkRef).where(ChunkRef.doc_id == doc_id, ChunkRef.point_id.in_(batch)))
    db.commit()
    sync_doc_ids(db, shared)   

def delete_document_vectors(db, doc_id: int) -> None:
    get_vector_store()                           # make sure the collection exists
    mine = [r for (r,) in db.execute(select(ChunkRef.point_id).where(ChunkRef.doc_id == doc_id))]
    release_points(db, doc_id, mine)


def ping() -> bool:
    try:
        get_client().get_collections()
        return True
    except Exception:
        return False
