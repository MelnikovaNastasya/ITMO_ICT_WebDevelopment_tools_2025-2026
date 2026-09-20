from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.dependencies import CurrentUser, DbSession
from app.models import Project
from app.schemas import ProjectCreate, ProjectRead, ProjectUpdate, ProjectWithTasks

router = APIRouter(prefix="/projects", tags=["Проекты"])


def owned_project(project_id: int, user_id: int, db: DbSession, nested: bool = False) -> Project:
    query = select(Project).where(Project.id == project_id, Project.user_id == user_id)
    if nested:
        query = query.options(selectinload(Project.tasks))
    project = db.scalar(query)
    if project is None:
        raise HTTPException(status_code=404, detail="Проект не найден")
    return project


@router.get("", response_model=list[ProjectRead])
def list_projects(db: DbSession, current_user: CurrentUser) -> list[Project]:
    return list(db.scalars(select(Project).where(Project.user_id == current_user.id)).all())


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(data: ProjectCreate, db: DbSession, current_user: CurrentUser) -> Project:
    project = Project(**data.model_dump(), user_id=current_user.id)
    db.add(project); db.commit(); db.refresh(project)
    return project


@router.get("/{project_id}", response_model=ProjectWithTasks)
def get_project(project_id: int, db: DbSession, current_user: CurrentUser) -> Project:
    return owned_project(project_id, current_user.id, db, nested=True)


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(project_id: int, data: ProjectUpdate, db: DbSession, current_user: CurrentUser) -> Project:
    project = owned_project(project_id, current_user.id, db)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    db.commit(); db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: DbSession, current_user: CurrentUser) -> None:
    project = owned_project(project_id, current_user.id, db)
    db.delete(project); db.commit()

