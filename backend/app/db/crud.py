from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from app.db.models import ChatSession, Document, Message, User, _utcnow


# ---- users ----
def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.scalar(select(User).where(User.username == username))


def create_user(db: Session, username: str, password_hash: str) -> User:
    user = User(username=username, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ---- documents ----
def create_document(db: Session, *, user_id: int, filename: str, stored_path: str,
                    file_type: str, size_bytes: int) -> Document:
    doc = Document(user_id=user_id, filename=filename, stored_path=stored_path,
                   file_type=file_type, size_bytes=size_bytes, status="processing")
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def get_document(db: Session, user_id: int, doc_id: int) -> Document | None:
    doc = db.get(Document, doc_id)
    return doc if doc and doc.user_id == user_id else None


def list_documents(db: Session, user_id: int) -> list[Document]:
    return list(db.scalars(select(Document).where(Document.user_id == user_id).order_by(Document.id.desc())))


def count_user_documents(db: Session, user_id: int, doc_ids: list[int]) -> int:
    return db.scalar(
        select(func.count(Document.id)).where(Document.user_id == user_id, Document.id.in_(doc_ids))
    ) or 0


def delete_document(db: Session, doc: Document) -> None:
    db.delete(doc)
    db.commit()


# ---- chat sessions ----
def create_session(db: Session, user_id: int, title: str = "New chat") -> ChatSession:
    session = ChatSession(user_id=user_id, title=title)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session(db: Session, user_id: int, session_id: int) -> ChatSession | None:
    session = db.get(ChatSession, session_id)
    return session if session and session.user_id == user_id else None


def list_sessions(db: Session, user_id: int) -> list[ChatSession]:
    return list(db.scalars(
        select(ChatSession).where(ChatSession.user_id == user_id).order_by(ChatSession.updated_at.desc())
    ))


def rename_session(db: Session, session: ChatSession, title: str) -> ChatSession:
    session.title = title
    db.commit()
    db.refresh(session)
    return session


def delete_session(db: Session, session: ChatSession) -> None:
    db.delete(session)
    db.commit()


# ---- messages ----
def add_message(db: Session, session_id: int, role: str, content: str, sources: list | None = None) -> Message:
    msg = Message(session_id=session_id, role=role, content=content, sources=sources)
    db.add(msg)
    db.execute(update(ChatSession).where(ChatSession.id == session_id).values(updated_at=_utcnow()))
    db.commit()
    db.refresh(msg)
    return msg


def list_messages(db: Session, session_id: int) -> list[Message]:
    return list(db.scalars(select(Message).where(Message.session_id == session_id).order_by(Message.id)))


def recent_messages(db: Session, session_id: int, limit: int = 40) -> list[Message]:
    rows = db.scalars(
        select(Message).where(Message.session_id == session_id).order_by(Message.id.desc()).limit(limit)
    )
    return list(reversed(list(rows)))
