from fastapi import FastAPI

from app.routers import auth, parser, projects, tags, tasks, users

app = FastAPI(
    title="TimeFlow",
    description="API тайм-менеджера: задачи, проекты, теги и учёт времени",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tags.router)
app.include_router(tasks.router)
app.include_router(parser.router)


@app.get("/", tags=["Система"])
def healthcheck() -> dict[str, str]:
    return {"message": "TimeFlow работает"}
