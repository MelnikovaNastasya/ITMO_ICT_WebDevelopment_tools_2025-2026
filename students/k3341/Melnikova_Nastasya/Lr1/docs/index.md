# TimeFlow — отчёт по лабораторной работе №1

## Цель

Реализовать серверное приложение тайм-менеджера на FastAPI с PostgreSQL, ORM, миграциями и ручной JWT-аутентификацией.

## Модель данных

В проекте шесть таблиц. Связь one-to-many используется между пользователями и задачами, проектами и задачами, задачами и записями времени. Связь many-to-many между задачами и тегами реализована через ассоциативную сущность `task_tags`, содержащую дополнительное поле `added_at`.

Исходный код моделей: [app/models/entities.py](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/blob/main/app/models/entities.py).

## Соединение с базой данных

Строка подключения читается из `.env`. Сессия SQLAlchemy создаётся в `app/db/database.py`, а в эндпоинты передаётся зависимостью FastAPI.

Код: [app/db/database.py](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/blob/main/app/db/database.py).

## API

- `/auth/register`, `/auth/login` — регистрация и JWT.
- `/users/me`, `/users`, `/users/me/password` — пользовательские методы.
- `/projects` — CRUD проектов, одиночный GET возвращает вложенные задачи.
- `/tasks` — CRUD задач и фильтрация; одиночный GET возвращает проект, теги и записи времени.
- `/tags` и `/tasks/{task_id}/tags/{tag_id}` — теги и many-to-many.
- `/tasks/{task_id}/time` — учёт времени.

Код эндпоинтов: [app/routers](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/tree/main/app/routers).

## Авторизация

JWT реализован вручную: после проверки пароля создаётся токен с идентификатором пользователя в `sub` и временем окончания в `exp`. Защищённые методы декодируют токен и получают текущего пользователя. Пароли хэшируются Argon2. Сторонняя готовая система пользователей не используется.

Код: [security.py](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/blob/main/app/core/security.py) и [dependencies.py](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/blob/main/app/api/dependencies.py).

## Миграции

Начальная миграция создаёт все таблицы, ключи, индексы, перечисления и ограничения. URL базы передаётся Alembic из `.env`.

Код: [alembic](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/tree/main/alembic).

## Практики

- [Практика 1.1](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/commits/main) — FastAPI, Pydantic, типизация и CRUD.
- [Практика 1.2](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/commits/main) — PostgreSQL, ORM, связи и вложенные модели.
- [Практика 1.3](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/commits/main) — Alembic, `.env`, `.gitignore` и структура.

Перед публикацией замените `YOUR_USERNAME` и `YOUR_REPOSITORY` на данные репозитория и при желании поставьте прямые ссылки на три соответствующих коммита.

