from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from app.models.entities import TaskPriority, TaskStatus


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)


class UserRead(ORMModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime


class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8, max_length=128)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None


class ProjectRead(ORMModel):
    id: int
    user_id: int
    name: str
    description: str | None
    created_at: datetime


class TagCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)


class TagRead(ORMModel):
    id: int
    user_id: int
    name: str


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    project_id: int | None = None
    status: TaskStatus = TaskStatus.planned
    priority: TaskPriority = TaskPriority.medium
    deadline: datetime | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    project_id: int | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    deadline: datetime | None = None


class TimeEntryCreate(BaseModel):
    started_at: datetime
    ended_at: datetime

    @model_validator(mode="after")
    def validate_period(self) -> "TimeEntryCreate":
        if self.ended_at <= self.started_at:
            raise ValueError("ended_at должен быть позже started_at")
        return self


class TimeEntryRead(ORMModel):
    id: int
    task_id: int
    user_id: int
    started_at: datetime
    ended_at: datetime
    duration_minutes: int


class TaskRead(ORMModel):
    id: int
    user_id: int
    project_id: int | None
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    deadline: datetime | None
    created_at: datetime
    updated_at: datetime
    project: ProjectRead | None = None
    tags: list[TagRead] = []
    time_entries: list[TimeEntryRead] = []


class ProjectWithTasks(ProjectRead):
    tasks: list[TaskRead] = []

