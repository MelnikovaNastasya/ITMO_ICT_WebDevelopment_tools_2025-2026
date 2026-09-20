# TimeFlow — лабораторная работа по FastAPI

Серверное приложение тайм-менеджера на 15 баллов. Пользователь регистрируется, получает JWT и управляет только своими проектами, задачами, тегами и записями времени.

## Что реализовано

- 6 таблиц PostgreSQL: `users`, `projects`, `tasks`, `tags`, `task_tags`, `time_entries`.
- one-to-many: пользователь → задачи; проект → задачи; задача → записи времени.
- many-to-many: задачи ↔ теги через `task_tags`; дополнительное поле связи — `added_at`.
- CRUD проектов и задач, API тегов и учёта времени.
- Вложенные проект, теги и записи времени в ответе задачи.
- Регистрация, вход, JWT, хэширование Argon2, текущий пользователь, список пользователей и смена пароля.
- Alembic, `.env`, типизация, Swagger и pytest-тесты.


Открыть Swagger: <http://127.0.0.1:8000/docs>.

## Запуск на macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
python -m uvicorn app.main:app --reload
```


## Основные эндпоинты

| Метод | Адрес | Назначение |
|---|---|---|
| POST | `/auth/register` | регистрация |
| POST | `/auth/login` | получение JWT |
| GET | `/users/me` | текущий пользователь |
| GET | `/users` | список пользователей |
| PATCH | `/users/me/password` | смена пароля |
| GET/POST | `/projects` | список/создание проектов |
| GET/PATCH/DELETE | `/projects/{id}` | проект и его задачи/изменение/удаление |
| GET/POST | `/tasks` | список с фильтрами/создание задач |
| GET/PATCH/DELETE | `/tasks/{id}` | задача с вложенными данными/изменение/удаление |
| GET/POST/DELETE | `/tags` | работа с тегами |
| POST/DELETE | `/tasks/{id}/tags/{tag_id}` | many-to-many связь |
| GET/POST | `/tasks/{id}/time` | учёт времени |

## Тесты

Тесты используют отдельную SQLite in-memory БД, поэтому не портят PostgreSQL:

```bash
pytest -q
```

## Миграции после изменения моделей

```bash
alembic revision --autogenerate -m "описание изменения"
alembic upgrade head
```

## Структура

```text
timeflow/
├── app/
│   ├── api/dependencies.py
│   ├── core/config.py, security.py
│   ├── db/database.py
│   ├── models/entities.py
│   ├── routers/
│   ├── schemas/schemas.py
│   └── main.py
├── alembic/versions/0001_initial.py
├── docs/index.md
├── tests/
├── .env.example
├── alembic.ini
└── requirements.txt
```

## JWT вручную

`security.py` сам создаёт токен через `jwt.encode`, а зависимость `get_current_user` извлекает Bearer-токен, декодирует его, берёт `sub` и загружает пользователя. Готовые библиотеки авторизации вроде fastapi-users не используются. Сторонние пакеты используются только для разрешённых операций: создания JWT и хэширования.


