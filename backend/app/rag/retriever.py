from langchain_core.documents import Document

from app.core.config import settings
from app.rag.vector_store import build_filter, get_vector_store


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
