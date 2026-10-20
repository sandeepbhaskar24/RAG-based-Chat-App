"""Qdrant client, collection bootstrap and per-user filtering helpers.

langchain-qdrant stores each chunk as {"page_content": ..., "metadata": {...}},
so payload filters use keys like "metadata.user_id".
"""
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
)

from app.core.config import settings
from app.rag.embeddings import get_embeddings

logger = logging.getLogger(__name__)
_lock = threading.Lock()

USER_KEY = "metadata.user_id"
DOC_KEY = "metadata.doc_id"


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


def delete_document_vectors(doc_id: int, user_id: int) -> None:
    get_vector_store()  # makes sure the collection exists
    get_client().delete(
        collection_name=settings.QDRANT_COLLECTION,
        points_selector=FilterSelector(filter=build_filter(user_id, [doc_id])),
    )


def ping() -> bool:
    try:
        get_client().get_collections()
        return True
    except Exception:
        return False
