def test_register_and_me(client, auth):
    res = client.get("/api/auth/me", headers=auth)
    assert res.status_code == 200
    assert res.json()["email"] == "sara@example.com"


def test_duplicate_email_is_rejected(client, auth):
    res = client.post("/api/auth/register", json={"email": "SARA@example.com", "name": "X", "password": "strongpass1"})
    assert res.status_code == 409


def test_short_password_is_rejected(client):
    res = client.post("/api/auth/register", json={"email": "a@b.com", "name": "A", "password": "123"})
    assert res.status_code == 422


def test_login(client, auth):
    ok = client.post("/api/auth/login", json={"email": "sara@example.com", "password": "strongpass1"})
    assert ok.status_code == 200 and ok.json()["access_token"]
    bad = client.post("/api/auth/login", json={"email": "sara@example.com", "password": "wrongpass1"})
    assert bad.status_code == 401


def test_protected_routes_need_token(client):
    assert client.get("/api/profile").status_code == 401
    assert client.get("/api/auth/me", headers={"Authorization": "Bearer nonsense"}).status_code == 401
