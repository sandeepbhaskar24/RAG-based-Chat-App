from langchain_core.documents import Document
from app.core.config import settings

from app.db import crud
from app.db.session import SessionLocal
from app.rag.vector_store import build_filter, get_client, get_vector_store


def sample_chunks(user_id: int, doc_ids: list[int] | None, n: int) -> list[Document]:
    """Evenly spaced chunks (ordered by page) from the target document(s).
    No doc attached -> the user's most recent ready document."""
    if not doc_ids:
        with SessionLocal() as db:
            ready = [d.id for d in crud.list_documents(db, user_id) if d.status == "ready"]
        doc_ids = ready[:1]
        if not doc_ids:
            return []
    points, _ = get_client().scroll(
        settings.QDRANT_COLLECTION, scroll_filter=build_filter(user_id, doc_ids),
        limit=500, with_payload=True, with_vectors=False)
    docs = [Document(page_content=p.payload["page_content"],
                     metadata=dict(p.payload.get("metadata") or {})) for p in points]
    docs.sort(key=lambda d: d.metadata.get("page") or 0)
    if len(docs) > n:
        step = len(docs) / n
        docs = [docs[int(i * step)] for i in range(n)]
    return docs



def retrieve(query: str, user_id: int, doc_ids: list[int] | None = None, k: int | None = None) -> list[Document]:
    """Similarity search restricted to the user's own chunks (optionally a subset of documents)."""
    results = get_vector_store().similarity_search_with_score(
        query,
        k=k or settings.RETRIEVAL_K,
        filter=build_filter(user_id, doc_ids),
    )
    docs: list[Document] = []
    for doc, score in results:
        doc.metadata["score"] = float(score)
        docs.append(doc)
    return docs