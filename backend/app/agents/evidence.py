"""Per-request evidence store shared by the KB agent's tools.

Why not graph state? The agent may issue several search calls in parallel; a store with a
lock gives every chunk one stable global number, so [n] citations in the final answer line up
with the `sources` event sent to the desktop client.
"""
import threading
from dataclasses import dataclass, field

from langchain_core.documents import Document


@dataclass
class Evidence:
    user_id: int
    doc_ids: list[int] | None = None          # set when the user attached a document
    question: str = ""
    docs: list[Document] = field(default_factory=list)      # index + 1 == citation number
    queries: list[str] = field(default_factory=list)        # every query tried so far
    last_verdict: dict | None = None                        # result of the latest check_sources
    _index: dict = field(default_factory=dict, repr=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def add(self, hits: list[Document]) -> list[tuple[int, Document]]:
        """Store hits (deduplicated) and return [(ref, doc)] with global 1-based refs."""
        out = []
        with self._lock:
            for d in hits:
                key = (d.metadata.get("page"), " ".join(d.page_content.split()))
                if key not in self._index:
                    self.docs.append(d)
                    self._index[key] = len(self.docs)
                out.append((self._index[key], d))
        return out