from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.db import crud
from app.db.models import User
from app.db.session import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    username = body.username.lower()
    if crud.get_user_by_username(db, username):
        raise HTTPException(409, "Username already taken")
    return crud.create_user(db, username, hash_password(body.password))


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, body.username.lower())
    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(401, "Incorrect username or password")
    return TokenResponse(access_token=create_access_token(user.id), user=user)


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
