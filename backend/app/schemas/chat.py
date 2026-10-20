from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)
    session_id: int | None = None          # omit to start a new session
    doc_ids: list[int] | None = None       # omit to search all of the user's documents


class SessionCreate(BaseModel):
    title: str = Field(default="New chat", min_length=1, max_length=120)


class SessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    created_at: datetime
    updated_at: datetime


class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    role: str
    content: str
    sources: list[dict] | None = None
    created_at: datetime
