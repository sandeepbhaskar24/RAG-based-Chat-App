from fastapi import APIRouter
from sqlalchemy import text

from app.db.session import engine
from app.rag.vector_store import ping

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False
    qdrant_ok = ping()
    return {"status": "ok" if db_ok and qdrant_ok else "degraded", "database": db_ok, "qdrant": qdrant_ok}
