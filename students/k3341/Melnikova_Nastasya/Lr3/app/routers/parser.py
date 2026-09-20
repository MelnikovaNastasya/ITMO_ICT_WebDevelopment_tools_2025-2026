import httpx
from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException, status
from pydantic import AnyHttpUrl, BaseModel

from app.core.config import settings
from worker.celery_app import celery_app

router = APIRouter(prefix="/parser", tags=["Парсер и очередь"])


class ParseRequest(BaseModel):
    url: AnyHttpUrl
    user_id: int = 1


@router.post("/sync")
def parse_sync(payload: ParseRequest) -> dict[str, object]:
    try:
        response = httpx.post(
            f"{settings.parser_service_url.rstrip('/')}/parse",
            json={"url": str(payload.url), "user_id": payload.user_id},
            timeout=20.0,
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        detail = exc.response.json().get("detail", "Ошибка сервиса парсера")
        raise HTTPException(status_code=exc.response.status_code, detail=detail) from exc
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail="Сервис парсера недоступен") from exc


@router.post("/async", status_code=status.HTTP_202_ACCEPTED)
def parse_async(payload: ParseRequest) -> dict[str, str]:
    task = celery_app.send_task(
        "worker.tasks.parse_url_task", args=[str(payload.url), payload.user_id]
    )
    return {"task_id": task.id, "status": "queued"}


@router.get("/tasks/{task_id}")
def task_status(task_id: str) -> dict[str, object]:
    task = AsyncResult(task_id, app=celery_app)
    body: dict[str, object] = {"task_id": task_id, "status": task.status}
    if task.successful():
        body["result"] = task.result
    elif task.failed():
        body["error"] = str(task.result)
    return body
