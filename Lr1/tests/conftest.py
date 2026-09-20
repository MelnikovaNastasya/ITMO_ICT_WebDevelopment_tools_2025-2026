import os

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("JWT_SECRET", "test-secret")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.main import app

engine = create_engine("sqlite+pysqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSession = sessionmaker(bind=engine, expire_on_commit=False)


def override_db():
    with TestingSession() as db:
        yield db


app.dependency_overrides[get_db] = override_db


@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(engine); Base.metadata.create_all(engine)
    yield


@pytest.fixture
def client():
    return TestClient(app)


def register_and_login(client: TestClient, username: str = "tatiana") -> dict[str, str]:
    client.post("/auth/register", json={"email": f"{username}@example.com", "username": username, "password": "password123"})
    response = client.post("/auth/login", data={"username": username, "password": "password123"})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}

