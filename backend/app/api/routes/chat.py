from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db import crud
from app.db.models import User
from app.db.session import get_db
from app.schemas.chat import ChatRequest, MessageOut, SessionCreate, SessionOut
from app.services import chat_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("")
def chat(req: ChatRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Ask a question; the answer streams back as Server-Sent Events (see chat_service)."""
    session, history = chat_service.prepare_chat(db, user, req.message, req.session_id, req.doc_ids)
    stream = chat_service.stream_chat(user.id, session.id, session.title, req.message, req.doc_ids, history)
    return StreamingResponse(
        stream,
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get("/sessions", response_model=list[SessionOut])
def list_sessions(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return crud.list_sessions(db, user.id)


@router.post("/sessions", response_model=SessionOut, status_code=201)
def create_session(body: SessionCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return crud.create_session(db, user.id, body.title)


def _owned_session(db: Session, user: User, session_id: int):
    session = crud.get_session(db, user.id, session_id)
    if session is None:
        raise HTTPException(404, "Chat session not found")
    return session


@router.get("/sessions/{session_id}/messages", response_model=list[MessageOut])
def get_messages(session_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    _owned_session(db, user, session_id)
    return crud.list_messages(db, session_id)


@router.patch("/sessions/{session_id}", response_model=SessionOut)
def rename_session(session_id: int, body: SessionCreate, db: Session = Depends(get_db),
                   user: User = Depends(get_current_user)):
    return crud.rename_session(db, _owned_session(db, user, session_id), body.title)


@router.delete("/sessions/{session_id}", status_code=204)
def delete_session(session_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    crud.delete_session(db, _owned_session(db, user, session_id))
    return Response(status_code=204)
