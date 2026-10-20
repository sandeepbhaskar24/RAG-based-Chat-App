from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    filename: str
    file_type: str
    size_bytes: int
    status: str            # processing | ready | failed
    chunk_count: int
    error: str | None = None
    created_at: datetime
