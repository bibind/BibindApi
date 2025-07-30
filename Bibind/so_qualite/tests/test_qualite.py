"""Unit tests for the qualite service."""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/docs")
    assert response.status_code == 200
