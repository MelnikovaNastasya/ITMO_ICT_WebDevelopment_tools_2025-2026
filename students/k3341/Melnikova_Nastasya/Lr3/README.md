# Лабораторная работа №3 — Docker, FastAPI, Celery и Redis

Проект упаковывает TimeFlow и парсер в Docker-контейнеры. Поддерживаются синхронный вызов отдельного сервиса парсинга и фоновая обработка через Celery + Redis.

## Состав

- `api` — основное FastAPI-приложение TimeFlow, порт `8000`;
- `parser` — отдельный FastAPI-сервис парсинга, порт `8001`;
- `db` — PostgreSQL;
- `redis` — брокер сообщений и хранилище результатов;
- `celery-worker` — исполнитель фоновых задач.

## Запуск

На Mac сначала должен быть запущен Docker Desktop.

```bash
cp .env.example .env
docker compose up --build
```

После запуска:

- Swagger основного API: <http://localhost:8000/docs>
- Swagger парсера: <http://localhost:8001/docs>

Демонстрационный пользователь создаётся автоматически: `parser@example.com`, пароль `password123`, `user_id=1`.

## Проверка

Синхронный запрос:

```bash
curl -X POST http://localhost:8000/parser/sync \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com","user_id":1}'
```

Фоновый запрос:

```bash
curl -X POST http://localhost:8000/parser/async \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://www.python.org","user_id":1}'
```

Скопируйте `task_id` из ответа:

```bash
curl http://localhost:8000/parser/tasks/TASK_ID
```

Остановка контейнеров:

```bash
docker compose down
```

Удаление контейнеров вместе с учебной БД:

```bash
docker compose down -v
```

## Локальные тесты

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```
