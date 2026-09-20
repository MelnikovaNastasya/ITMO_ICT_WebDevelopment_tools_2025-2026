from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.dependencies import CurrentUser, DbSession
from app.models import Project, Tag, Task, TaskTag, TimeEntry
from app.models.entities import TaskPriority, TaskStatus
from app.schemas import TaskCreate, TaskRead, TaskUpdate, TimeEntryCreate, TimeEntryRead

router = APIRouter(prefix="/tasks", tags=["Задачи и время"])


def task_options():
    return (
        selectinload(Task.project),
        selectinload(Task.tags),
        selectinload(Task.time_entries),
    )


def owned_task(task_id: int, user_id: int, db: DbSession) -> Task:
    task = db.scalar(select(Task).where(Task.id == task_id, Task.user_id == user_id).options(*task_options()))
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


def validate_project(project_id: int | None, user_id: int, db: DbSession) -> None:
    if project_id is not None and db.scalar(select(Project).where(Project.id == project_id, Project.user_id == user_id)) is None:
        raise HTTPException(status_code=400, detail="Указан чужой или несуществующий проект")


@router.get("", response_model=list[TaskRead])
def list_tasks(
    db: DbSession,
    current_user: CurrentUser,
    task_status: TaskStatus | None = Query(None, alias="status"),
    priority: TaskPriority | None = None,
    deadline_before: datetime | None = None,
) -> list[Task]:
    query = select(Task).where(Task.user_id == current_user.id).options(*task_options())
    if task_status: query = query.where(Task.status == task_status)
    if priority: query = query.where(Task.priority == priority)
    if deadline_before: query = query.where(Task.deadline <= deadline_before)
    return list(db.scalars(query.order_by(Task.created_at.desc())).all())


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, db: DbSession, current_user: CurrentUser) -> Task:
    validate_project(data.project_id, current_user.id, db)
    task = Task(**data.model_dump(), user_id=current_user.id)
    db.add(task); db.commit()
    return owned_task(task.id, current_user.id, db)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: DbSession, current_user: CurrentUser) -> Task:
    return owned_task(task_id, current_user.id, db)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, data: TaskUpdate, db: DbSession, current_user: CurrentUser) -> Task:
    task = owned_task(task_id, current_user.id, db)
    values = data.model_dump(exclude_unset=True)
    if "project_id" in values: validate_project(values["project_id"], current_user.id, db)
    for key, value in values.items(): setattr(task, key, value)
    db.commit()
    return owned_task(task_id, current_user.id, db)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: DbSession, current_user: CurrentUser) -> None:
    task = owned_task(task_id, current_user.id, db)
    db.delete(task); db.commit()


@router.post("/{task_id}/tags/{tag_id}", response_model=TaskRead)
def add_tag(task_id: int, tag_id: int, db: DbSession, current_user: CurrentUser) -> Task:
    owned_task(task_id, current_user.id, db)
    tag = db.scalar(select(Tag).where(Tag.id == tag_id, Tag.user_id == current_user.id))
    if tag is None: raise HTTPException(status_code=404, detail="Тег не найден")
    if db.get(TaskTag, (task_id, tag_id)) is None:
        db.add(TaskTag(task_id=task_id, tag_id=tag_id)); db.commit()
    return owned_task(task_id, current_user.id, db)


@router.delete("/{task_id}/tags/{tag_id}", status_code=204)
def remove_tag(task_id: int, tag_id: int, db: DbSession, current_user: CurrentUser) -> None:
    owned_task(task_id, current_user.id, db)
    link = db.get(TaskTag, (task_id, tag_id))
    if link is None: raise HTTPException(status_code=404, detail="Связь не найдена")
    db.delete(link); db.commit()


@router.get("/{task_id}/time", response_model=list[TimeEntryRead])
def list_time(task_id: int, db: DbSession, current_user: CurrentUser) -> list[TimeEntry]:
    owned_task(task_id, current_user.id, db)
    return list(db.scalars(select(TimeEntry).where(TimeEntry.task_id == task_id, TimeEntry.user_id == current_user.id)).all())


@router.post("/{task_id}/time", response_model=TimeEntryRead, status_code=201)
def add_time(task_id: int, data: TimeEntryCreate, db: DbSession, current_user: CurrentUser) -> TimeEntry:
    owned_task(task_id, current_user.id, db)
    minutes = int((data.ended_at - data.started_at).total_seconds() // 60)
    entry = TimeEntry(**data.model_dump(), duration_minutes=minutes, task_id=task_id, user_id=current_user.id)
    db.add(entry); db.commit(); db.refresh(entry)
    return entry

