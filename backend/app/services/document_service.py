import logging
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from app.core.config import settings
from app.db import crud
from app.db.models import Document, User
from app.db.session import SessionLocal
from app.rag.ingest import ingest_file
from app.rag.vector_store import delete_document_vectors

logger = logging.getLogger(__name__)
_READ_CHUNK = 1024 * 1024


async def save_upload(db, user: User, upload: UploadFile) -> Document:
    """Validate and store the file on disk, then create a 'processing' DB row."""
    original_name = Path(upload.filename or "").name
    ext = Path(original_name).suffix.lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        allowed = ", ".join(sorted(settings.ALLOWED_EXTENSIONS))
        raise HTTPException(415, f"Unsupported file type '{ext}'. Allowed: {allowed}")

    user_dir = settings.UPLOAD_DIR / str(user.id)
    user_dir.mkdir(parents=True, exist_ok=True)
    stored = user_dir / f"{uuid4().hex}{ext}"

    limit = settings.MAX_UPLOAD_MB * 1024 * 1024
    size, too_big = 0, False
    with stored.open("wb") as out:
        while chunk := await upload.read(_READ_CHUNK):
            size += len(chunk)
            if size > limit:
                too_big = True
                break
            out.write(chunk)

    if too_big:
        stored.unlink(missing_ok=True)
        raise HTTPException(413, f"File exceeds the {settings.MAX_UPLOAD_MB} MB limit")
    if size == 0:
        stored.unlink(missing_ok=True)
        raise HTTPException(400, "Uploaded file is empty")

    return crud.create_document(
        db, user_id=user.id, filename=original_name, stored_path=str(stored),
        file_type=ext.lstrip("."), size_bytes=size,
    )


def ingest_document(doc_id: int) -> None:
    """Background task: index the document and record the outcome."""
    with SessionLocal() as db:
        doc = db.get(Document, doc_id)
        if doc is None:
            return
        try:
            doc.chunk_count = ingest_file(
                doc.stored_path, doc_id=doc.id, user_id=doc.user_id,
                filename=doc.filename, db=db,
            )
            doc.status, doc.error = "ready", None
        except Exception as exc:
            logger.exception("Ingestion failed for document %s", doc_id)
            db.rollback()
            try:   # releases this doc's claims; points other docs use are kept
                delete_document_vectors(db, doc.id)
            except Exception:
                logger.warning("Could not clean up vectors for document %s", doc_id)
            doc = db.get(Document, doc_id)
            doc.status, doc.error = "failed", str(exc)[:500]
        db.commit()


def delete_document(db, user: User, doc_id: int) -> None:
    doc = crud.get_document(db, user.id, doc_id)
    if doc is None:
        raise HTTPException(404, "Document not found")
    try:
        delete_document_vectors(db, doc.id)
    except Exception as exc:
        logger.exception("Vector deletion failed for document %s", doc_id)
        db.rollback()
        raise HTTPException(
            502, f"Could not remove document data: {type(exc).__name__}: {str(exc)[:200]}"
        ) from exc
    Path(doc.stored_path).unlink(missing_ok=True)
    crud.delete_document(db, doc)