from fastapi import status
from fastapi.testclient import TestClient

from app import app

client = TestClient(app=app)


def test_healthy_return():
    response = client.get("/status")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "Healthy"}
