import os

import pytest

from tests.conftest import make_user

MONDAY = "2026-01-05"


@pytest.fixture
def people(client):
    sara = make_user(client, "sara@example.com", "Sara")
    omar = make_user(client, "omar@example.com", "Omar")
    lina = make_user(client, "lina@example.com", "Lina")
    return sara, omar, lina


def log_workout(client, auth, weight=60, reps=8, sets=3, key="bench_press"):
    body = {
        "day": MONDAY,
        "sets": [{"exercise_key": key, "set_number": i + 1, "weight_kg": weight, "reps": reps} for i in range(sets)],
    }
    res = client.post("/api/workouts/logs", json=body, headers=auth)
    assert res.status_code == 201
    return res.json()["id"]


def test_usernames_are_generated_and_unique(client, people):
    sara, omar, _ = people
    assert client.get("/api/auth/me", headers=sara).json()["username"] == "sara"
    # a second "sara@other.com" gets a different username
    other = make_user(client, "sara@other.com", "Sara 2")
    assert client.get("/api/auth/me", headers=other).json()["username"].startswith("sara")
    assert client.get("/api/auth/me", headers=other).json()["username"] != "sara"


def test_change_username(client, people):
    sara, omar, _ = people
    assert (
        client.patch("/api/me/social", json={"username": "@Sara.Lifts"}, headers=sara).json()["username"]
        == "sara.lifts"
    )
    assert client.patch("/api/me/social", json={"username": "sara.lifts"}, headers=omar).status_code == 409
    for bad in ["ab", "has space", "عربي", "me"]:
        assert client.patch("/api/me/social", json={"username": bad}, headers=omar).status_code == 422, bad


def test_register_with_username(client):
    body = {"email": "x@example.com", "name": "X", "password": "strongpass1", "username": "iron_x"}
    token = client.post("/api/auth/register", json=body).json()["access_token"]
    assert client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"}).json()["username"] == "iron_x"
    body2 = {**body, "email": "y@example.com"}
    assert client.post("/api/auth/register", json=body2).status_code == 409


def test_search_finds_by_username_or_name_but_not_email_or_self(client, people):
    sara, omar, lina = people
    found = client.get("/api/users/search", params={"q": "om"}, headers=sara).json()
    assert [u["username"] for u in found] == ["omar"]
    assert client.get("/api/users/search", params={"q": "Lina"}, headers=sara).json()[0]["name"] == "Lina"
    assert client.get("/api/users/search", params={"q": "example.com"}, headers=sara).json() == []
    assert client.get("/api/users/search", params={"q": "sara"}, headers=sara).json() == []
    assert "email" not in found[0]


def test_follow_unfollow_and_counts(client, people):
    sara, omar, _ = people
    assert client.post("/api/users/omar/follow", headers=sara).status_code == 204
    assert client.post("/api/users/omar/follow", headers=sara).status_code == 204  # idempotent
    profile = client.get("/api/users/omar", headers=sara).json()
    assert profile["user"]["is_following"] is True and profile["user"]["followers"] == 1
    assert client.get("/api/users/sara", headers=omar).json()["user"]["follows_you"] is True
    assert [u["username"] for u in client.get("/api/users/me/following", headers=sara).json()] == ["omar"]
    assert [u["username"] for u in client.get("/api/users/me/followers", headers=omar).json()] == ["sara"]

    assert client.delete("/api/users/omar/follow", headers=sara).status_code == 204
    assert client.get("/api/users/omar", headers=sara).json()["user"]["followers"] == 0


def test_cannot_follow_yourself_or_unknown(client, people):
    sara, _, _ = people
    assert client.post("/api/users/sara/follow", headers=sara).status_code == 400
    assert client.post("/api/users/nobody/follow", headers=sara).status_code == 404


def test_feed_shows_me_and_people_i_follow(client, people):
    sara, omar, lina = people
    client.post("/api/users/omar/follow", headers=sara)
    mine = log_workout(client, sara, weight=40)
    omars = log_workout(client, omar, weight=100, reps=5, sets=4)
    log_workout(client, lina)  # not followed

    feed = client.get("/api/feed", headers=sara).json()
    assert [item["id"] for item in feed] == [omars, mine]
    item = feed[0]
    assert item["user"]["username"] == "omar" and not item["is_mine"]
    assert item["sets_count"] == 4 and item["volume_kg"] == 100 * 5 * 4
    assert item["exercises"][0]["name_en"] == "Barbell Bench Press"
    assert item["exercises"][0]["best_weight_kg"] == 100

    # paging
    assert [i["id"] for i in client.get("/api/feed", params={"before_id": omars}, headers=sara).json()] == [mine]


def test_private_users_are_hidden(client, people):
    sara, omar, _ = people
    client.post("/api/users/omar/follow", headers=sara)
    log_id = log_workout(client, omar)
    client.patch("/api/me/social", json={"is_private": True}, headers=omar)

    assert client.get("/api/feed", headers=sara).json() == []
    profile = client.get("/api/users/omar", headers=sara).json()
    assert profile["is_private"] and profile["workouts"] == [] and profile["workouts_count"] is None
    assert client.post(f"/api/workouts/logs/{log_id}/like", headers=sara).status_code == 404
    # omar still sees his own
    assert len(client.get("/api/feed", headers=omar).json()) == 1


def test_likes(client, people):
    sara, omar, _ = people
    client.post("/api/users/omar/follow", headers=sara)
    log_id = log_workout(client, omar)
    assert client.post(f"/api/workouts/logs/{log_id}/like", headers=sara).status_code == 204
    assert client.post(f"/api/workouts/logs/{log_id}/like", headers=sara).status_code == 204  # once only
    item = client.get("/api/feed", headers=sara).json()[0]
    assert item["likes"] == 1 and item["liked_by_me"] is True
    client.delete(f"/api/workouts/logs/{log_id}/like", headers=sara)
    assert client.get("/api/feed", headers=sara).json()[0]["likes"] == 0
    # deleting a liked workout works
    client.post(f"/api/workouts/logs/{log_id}/like", headers=sara)
    assert client.delete(f"/api/workouts/logs/{log_id}", headers=omar).status_code == 204


def test_old_databases_get_usernames(tmp_path, monkeypatch):
    import sqlite3

    from sqlmodel import create_engine

    from app import database

    path = tmp_path / "old.db"
    conn = sqlite3.connect(path)
    conn.execute(
        'CREATE TABLE "user" (id INTEGER PRIMARY KEY, email VARCHAR, name VARCHAR, '
        "hashed_password VARCHAR, created_at DATETIME)"
    )
    conn.execute("""INSERT INTO "user" VALUES (1, 'old.user@example.com', 'Old', 'x', '2026-01-01')""")
    conn.commit()
    conn.close()

    monkeypatch.setattr(database, "engine", create_engine(f"sqlite:///{path}"))
    database.init_db()
    row = sqlite3.connect(path).execute('SELECT username, is_private FROM "user"').fetchone()
    assert row == ("old.user", 0)


@pytest.mark.skipif(not os.getenv("TEST_DATABASE_URL"), reason="Postgres only")
def test_supabase_api_roles_cannot_read_tables(monkeypatch):
    """On Postgres, Supabase's public API roles must not be able to read any table."""
    from sqlalchemy import text
    from sqlmodel import SQLModel, create_engine

    from app import database
    from app.config import normalize_database_url

    engine = create_engine(normalize_database_url(os.environ["TEST_DATABASE_URL"]))
    SQLModel.metadata.create_all(engine)
    with engine.begin() as conn:
        for role in ("anon", "authenticated"):
            if not conn.execute(text("SELECT 1 FROM pg_roles WHERE rolname = :r"), {"r": role}).first():
                conn.execute(text(f"CREATE ROLE {role} NOLOGIN"))
        conn.execute(text("GRANT USAGE ON SCHEMA public TO anon"))
        conn.execute(text('GRANT SELECT ON "user" TO anon'))  # simulate an exposed table

    monkeypatch.setattr(database, "engine", engine)
    database.init_db()

    with engine.connect() as conn:
        conn.execute(text("SET ROLE anon"))
        with pytest.raises(Exception, match="permission denied"):
            conn.execute(text('SELECT * FROM "user"'))
        conn.rollback()
    with engine.connect() as conn:
        rls = conn.execute(text("SELECT relrowsecurity FROM pg_class WHERE relname = 'user'")).scalar()
    assert rls is True
    SQLModel.metadata.drop_all(engine)
    engine.dispose()
