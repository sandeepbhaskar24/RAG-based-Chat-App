from bisect import bisect_right

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings


def get_splitter() -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
        add_start_index=True,          # lets us map each chunk back to its page
    )


def split_documents(docs: list[Document]) -> list[Document]:
    """Split the WHOLE file as one continuous text (chunks may span page breaks).

    Each chunk gets page = the page where the chunk starts (None for non-paged files).
    """
    if not docs:
        return []

    sep = "\n\n"
    parts, offsets, pages, pos = [], [], [], 0
    for d in docs:
        offsets.append(pos)
        pages.append(d.metadata.get("page"))
        parts.append(d.page_content)
        pos += len(d.page_content) + len(sep)
    text = sep.join(parts)

    chunks = get_splitter().create_documents([text])
    for c in chunks:
        i = bisect_right(offsets, c.metadata["start_index"]) - 1
        c.metadata = {"page": pages[max(i, 0)]}
    return chunks