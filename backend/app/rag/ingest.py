"""load -> split -> content-hash -> embed ONLY new chunks -> record references."""
import hashlib
import logging
import uuid
from pathlib import Path

from sqlalchemy import select

from app.core.config import settings
from app.db.models import ChunkRef
from app.rag.loaders import load_file
from app.rag.splitter import split_documents
from app.rag.vector_store import (
    _batched, get_client, get_vector_store, release_points, sync_doc_ids,
)

logger = logging.getLogger(__name__)


def point_id(user_id: int, page: int | None, text: str) -> str:
    """Deterministic ID from content. Same user + same page + same text => same ID."""
    normalized = " ".join(text.split())          # ignore whitespace-only differences
    h = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"{user_id}:{page}:{h}"))


def ingest_file(path: str | Path, *, doc_id: int, user_id: int, filename: str, db) -> int:
    """Index a file, embedding only chunks not already stored. Returns unique chunk count.

    Idempotent: safe to re-run for the same doc_id after a crash.
    """
    store = get_vector_store()                   # ensures the collection exists
    client = get_client()

    docs = load_file(path)
    chunks = split_documents(docs)
    if not chunks:
        raise ValueError("Document produced no text chunks.")

    # 1. Content-based IDs; identical chunks inside this file collapse to one point
    by_id = {}
    for c in chunks:
        pid = point_id(user_id, c.metadata.get("page"), c.page_content)
        by_id.setdefault(pid, c)
    all_ids = list(by_id)

    # 2. Claim these points in MySQL BEFORE touching Qdrant, so a failure can be cleaned up
    already_mine = {r for (r,) in db.execute(select(ChunkRef.point_id).where(ChunkRef.doc_id == doc_id))}
    to_claim = [i for i in all_ids if i not in already_mine]
    if to_claim:
        db.add_all(ChunkRef(point_id=i, doc_id=doc_id, user_id=user_id) for i in to_claim)
        db.commit()

    # 3. Which points already exist in Qdrant (from this or any other document)?
    existing: set[str] = set()
    for batch in _batched(all_ids):
        for p in client.retrieve(settings.QDRANT_COLLECTION, ids=batch,
                                 with_payload=False, with_vectors=False):
            existing.add(str(p.id))

    # 4. Embed + upsert only the missing ones (this is where the embedding cost is saved)
    missing = [i for i in all_ids if i not in existing]
    if missing:
        to_add = []
        for pid in missing:
            c = by_id[pid]
            c.metadata = {"user_id": user_id, "doc_ids": [doc_id], "page": c.metadata.get("page")}
            to_add.append(c)
        store.add_documents(to_add, ids=missing)

    # 5. Payload doc_ids := MySQL truth for every point this document touches
    sync_doc_ids(db, all_ids)

    # 6. Re-ingest with different chunking? Release points this doc no longer contains
    release_points(db, doc_id, list(already_mine - set(all_ids)))

    logger.info("Ingested doc_id=%s: %s unique chunks (%s new, %s reused)",
                doc_id, len(all_ids), len(missing), len(all_ids) - len(missing))
    return len(all_ids)