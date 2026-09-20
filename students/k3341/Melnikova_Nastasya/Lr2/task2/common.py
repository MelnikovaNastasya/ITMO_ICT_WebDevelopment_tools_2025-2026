import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

URLS = [
    "https://example.com/",
    "https://www.iana.org/help/example-domains",
    "https://www.python.org/",
    "https://fastapi.tiangolo.com/",
    "https://docs.python.org/3/library/asyncio.html",
    "https://docs.python.org/3/library/threading.html",
]


@dataclass(frozen=True)
class ParsedPage:
    url: str
    title: str


def extract_title(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    if soup.title is None or not soup.title.string:
        return "Страница без заголовка"
    return " ".join(soup.title.string.split())[:200]


def database_url() -> str:
    value = os.getenv("DATABASE_URL")
    if not value:
        raise RuntimeError("Создайте Lr2/.env на основе .env.example")
    return value


def parser_user_id() -> int:
    return int(os.getenv("PARSER_USER_ID", "1"))


def save_as_task(page: ParsedPage, approach: str) -> None:
    """Сохраняет заголовок страницы как задачу в БД TimeFlow из ЛР1."""
    engine = create_engine(database_url(), pool_pre_ping=True)
    now = datetime.now(timezone.utc)
    statement = text(
        """
        INSERT INTO tasks
            (user_id, project_id, title, description, status, priority, deadline, created_at, updated_at)
        VALUES
            (:user_id, NULL, :title, :description, 'planned', 'low', NULL, :created_at, :updated_at)
        """
    )
    with engine.begin() as connection:
        connection.execute(
            statement,
            {
                "user_id": parser_user_id(),
                "title": page.title,
                "description": f"Источник: {page.url}. Подход: {approach}",
                "created_at": now,
                "updated_at": now,
            },
        )
    engine.dispose()


def split_urls(urls: list[str], parts: int) -> list[list[str]]:
    return [urls[index::parts] for index in range(parts) if urls[index::parts]]

