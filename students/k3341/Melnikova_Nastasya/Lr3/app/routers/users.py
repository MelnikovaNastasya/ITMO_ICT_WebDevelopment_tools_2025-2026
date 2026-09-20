from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.api.dependencies import CurrentUser, DbSession
from app.core.security import hash_password, verify_password
from app.models import User
from app.schemas import PasswordChange, UserRead

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("/me", response_model=UserRead)
def me(current_user: CurrentUser) -> User:
    return current_user


@router.get("", response_model=list[UserRead])
def list_users(db: DbSession, current_user: CurrentUser) -> list[User]:
    return list(db.scalars(select(User).order_by(User.id)).all())


@router.patch("/me/password", status_code=204)
def change_password(data: PasswordChange, db: DbSession, current_user: CurrentUser) -> None:
    if not verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Старый пароль неверен")
    current_user.hashed_password = hash_password(data.new_password)
    db.commit()

