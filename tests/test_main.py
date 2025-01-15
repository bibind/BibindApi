from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_create_cloud():
    response = client.post("/create-cloud", json={"name": "AWS", "provider": "aws"})
    assert response.status_code == 200
    assert response.json()["message"] == "Cloud provisionné"