"""Per-request evidence store shared by the KB agent's tools."""
import threading
from dataclasses import dataclass, field

from langchain_core.documents import Document


@dataclass
class Evidence:
    user_id: int
    doc_ids: list[int] | None = None
    question: str = ""
    docs: list[Document] = field(default_factory=list)
    queries: list[str] = field(default_factory=list)
    last_verdict: dict | None = None
    _index: dict = field(default_factory=dict, repr=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def add(self, hits: list[Document]) -> list[tuple[int, Document]]:
        """Store hits with stable 1-based references; don't merge identical chunks from different files."""
        out = []
        with self._lock:
            for d in hits:
                metadata = d.metadata or {}
                doc_identity = metadata.get("doc_id")
                if doc_identity is None:
                    ids = metadata.get("doc_ids") or []
                    doc_identity = tuple(ids) if isinstance(ids, (list, tuple)) else ids
                key = (
                    doc_identity,
                    metadata.get("source") or metadata.get("filename"),
                    metadata.get("page"),
                    " ".join(d.page_content.split()),
                )
                if key not in self._index:
                    self.docs.append(d)
                    self._index[key] = len(self.docs)
                out.append((self._index[key], d))
        return out
