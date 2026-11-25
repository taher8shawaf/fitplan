import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app import models  # noqa: F401
from app.config import normalize_database_url
from app.database import enforce_sqlite_foreign_keys, get_session
from app.main import app
from app.seed import seed_foods

# Tests use in-memory SQLite by default. To run them against Postgres too:
#   TEST_DATABASE_URL=postgresql://user:pass@host:5432/fitplan_test pytest
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")


@pytest.fixture
def session():
    if TEST_DATABASE_URL:
        engine = create_engine(normalize_database_url(TEST_DATABASE_URL))
        SQLModel.metadata.drop_all(engine)
    else:
        engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
        enforce_sqlite_foreign_keys(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        seed_foods(s)
        yield s
    if TEST_DATABASE_URL:
        SQLModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def client(session):
    app.dependency_overrides[get_session] = lambda: session
    # No `with`: skip the lifespan so tests never touch the real database file.
    yield TestClient(app)
    app.dependency_overrides.clear()


def make_user(client, email="sara@example.com", name="Sara"):
    res = client.post("/api/auth/register", json={"email": email, "name": name, "password": "strongpass1"})
    assert res.status_code == 201
    return {"Authorization": f"Bearer {res.json()['access_token']}"}


@pytest.fixture
def auth(client):
    return make_user(client)


@pytest.fixture
def other_auth(client):
    return make_user(client, email="omar@example.com", name="Omar")
