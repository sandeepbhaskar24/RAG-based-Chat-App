"""load -> split -> embed -> upsert into Qdrant."""
import logging
from pathlib import Path

from app.rag.loaders import load_file
from app.rag.splitter import split_documents
from app.rag.vector_store import get_vector_store

logger = logging.getLogger(__name__)


def ingest_file(path: str | Path, *, doc_id: int, user_id: int, filename: str) -> int:
    """Index a file and return the number of chunks stored."""
    docs = load_file(path)
    chunks = split_documents(docs)
    if not chunks:
        raise ValueError("Document produced no text chunks.")

    for index, chunk in enumerate(chunks):
        chunk.metadata.update(
            {
                "user_id": user_id,
                "doc_id": doc_id,
                "filename": filename,
                "page": chunk.metadata.get("page"),
                "chunk_index": index,
            }
        )

    get_vector_store().add_documents(chunks)
    logger.info("Ingested doc_id=%s (%s chunks)", doc_id, len(chunks))
    return len(chunks)
