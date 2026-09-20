from worker.celery_app import celery_app
from shared.parser_logic import parse_and_save


@celery_app.task(name="worker.tasks.parse_url_task")
def parse_url_task(url: str, user_id: int = 1) -> dict[str, object]:
    return parse_and_save(url, user_id)
