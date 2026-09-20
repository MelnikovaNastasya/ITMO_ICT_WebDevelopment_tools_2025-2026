from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text

from app.core.config import settings


class UnsafeUrlError(ValueError):
    """URL нельзя запрашивать из сервиса."""


def validate_public_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise UnsafeUrlError("Разрешены только абсолютные http/https URL")

    try:
        addresses = {item[4][0] for item in socket.getaddrinfo(parsed.hostname, None)}
    except socket.gaierror as exc:
        raise UnsafeUrlError("Не удалось определить адрес сайта") from exc

    for address in addresses:
        ip = ipaddress.ip_address(address)
        if not ip.is_global:
            raise UnsafeUrlError("Локальные и служебные адреса запрещены")
    return url


def extract_title(html: str) -> str:
    title = BeautifulSoup(html, "html.parser").title
    if title is None:
        return "Без заголовка"
    return title.get_text(" ", strip=True)[:200] or "Без заголовка"


def parse_and_save(url: str, user_id: int | None = None) -> dict[str, object]:
    safe_url = validate_public_url(url)
    with httpx.Client(follow_redirects=True, timeout=15.0) as client:
        response = client.get(safe_url, headers={"User-Agent": "TimeFlow-Lr3/1.0"})
        response.raise_for_status()
    title = extract_title(response.text)

    engine = create_engine(settings.database_url, pool_pre_ping=True)
    with engine.begin() as connection:
        result = connection.execute(
            text(
                """INSERT INTO tasks
                (user_id, project_id, title, description, status, priority,
                 deadline, created_at, updated_at)
                VALUES (:user_id, NULL, :title, :description, 'planned', 'medium',
                        NULL, now(), now())
                RETURNING id"""
            ),
            {
                "user_id": user_id or settings.parser_user_id,
                "title": title,
                "description": f"Страница: {response.url}",
            },
        )
        task_id = result.scalar_one()
    engine.dispose()
    return {"url": str(response.url), "title": title, "task_id": task_id}
