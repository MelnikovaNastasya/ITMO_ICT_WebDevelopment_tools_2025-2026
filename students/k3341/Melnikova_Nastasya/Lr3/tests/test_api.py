from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@patch("app.routers.parser.httpx.post")
def test_sync_parser(post: Mock) -> None:
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {"url": "https://example.com/", "title": "Example", "task_id": 7}
    post.return_value = response
    result = client.post("/parser/sync", json={"url": "https://example.com", "user_id": 1})
    assert result.status_code == 200
    assert result.json()["task_id"] == 7


@patch("app.routers.parser.celery_app.send_task")
def test_async_parser(send_task: Mock) -> None:
    send_task.return_value.id = "job-123"
    result = client.post("/parser/async", json={"url": "https://example.com", "user_id": 1})
    assert result.status_code == 202
    assert result.json() == {"task_id": "job-123", "status": "queued"}
