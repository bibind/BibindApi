"""Unit tests for authentication service and routes."""

from fastapi.testclient import TestClient

from app.routes.auth import router
from app.main import app

app.include_router(router)
client = TestClient(app)


def test_login_success() -> None:
    response = client.post(
        "/auth/login",
        json={"email": "user@example.com", "password": "password"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert "refresh_token" in body


def test_me_endpoint() -> None:
    login = client.post(
        "/auth/login",
        json={"email": "user@example.com", "password": "password"},
    ).json()
    headers = {"Authorization": f"Bearer {login['access_token']}"}
    resp = client.get("/auth/me", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "user@example.com"


def test_permissions() -> None:
    login = client.post(
        "/auth/login",
        json={"email": "user@example.com", "password": "password"},
    ).json()
    headers = {"Authorization": f"Bearer {login['access_token']}"}
    resp = client.get("/auth/permissions", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["permissions"] == ["offres:read", "projets:read"]
