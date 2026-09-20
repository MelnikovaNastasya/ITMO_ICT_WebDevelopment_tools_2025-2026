from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_, select

from app.api.dependencies import DbSession
from app.core.security import create_access_token, hash_password, verify_password
from app.models import User
from app.schemas import Token, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["Авторизация"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: DbSession) -> User:
    exists = db.scalar(select(User).where(or_(User.email == data.email, User.username == data.username)))
    if exists:
        raise HTTPException(status_code=409, detail="Email или имя пользователя уже заняты")
    user = User(email=data.email, username=data.username, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession
) -> Token:
    user = db.scalar(select(User).where(or_(User.username == form.username, User.email == form.username)))
    if user is None or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    return Token(access_token=create_access_token(user.id))

