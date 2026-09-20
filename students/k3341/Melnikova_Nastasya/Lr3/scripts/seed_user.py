from sqlalchemy import select

from app.core.security import hash_password
from app.db.database import SessionLocal
from app.models.entities import User


with SessionLocal() as db:
    if db.scalar(select(User).where(User.id == 1)) is None:
        db.add(
            User(
                id=1,
                email="parser@example.com",
                username="parser",
                hashed_password=hash_password("password123"),
            )
        )
        db.commit()
        print("Создан демонстрационный пользователь parser (id=1)")
