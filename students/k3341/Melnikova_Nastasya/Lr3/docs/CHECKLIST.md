# Скриншоты перед сдачей

Создать папку `docs/images` и добавить:

1. `docker-compose.png` — терминал после `docker compose up --build`;
2. `sync-parser.png` — ответ `POST /parser/sync` в Swagger;
3. `async-parser.png` — ответ `POST /parser/async` с HTTP 202;
4. `celery-result.png` — ответ `GET /parser/tasks/{task_id}` со статусом `SUCCESS`;
5. `tests.png` — результат команды `pytest -q`.
