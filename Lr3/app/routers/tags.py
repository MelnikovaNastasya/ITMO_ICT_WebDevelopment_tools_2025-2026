from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.dependencies import CurrentUser, DbSession
from app.models import Tag
from app.schemas import TagCreate, TagRead

router = APIRouter(prefix="/tags", tags=["Теги"])


@router.get("", response_model=list[TagRead])
def list_tags(db: DbSession, current_user: CurrentUser) -> list[Tag]:
    return list(db.scalars(select(Tag).where(Tag.user_id == current_user.id)).all())


@router.post("", response_model=TagRead, status_code=status.HTTP_201_CREATED)
def create_tag(data: TagCreate, db: DbSession, current_user: CurrentUser) -> Tag:
    duplicate = db.scalar(select(Tag).where(Tag.user_id == current_user.id, Tag.name == data.name))
    if duplicate:
        raise HTTPException(status_code=409, detail="Такой тег уже существует")
    tag = Tag(name=data.name, user_id=current_user.id)
    db.add(tag); db.commit(); db.refresh(tag)
    return tag


@router.delete("/{tag_id}", status_code=204)
def delete_tag(tag_id: int, db: DbSession, current_user: CurrentUser) -> None:
    tag = db.scalar(select(Tag).where(Tag.id == tag_id, Tag.user_id == current_user.id))
    if tag is None:
        raise HTTPException(status_code=404, detail="Тег не найден")
    db.delete(tag); db.commit()

