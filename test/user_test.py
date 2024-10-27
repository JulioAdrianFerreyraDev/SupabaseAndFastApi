from fastapi import status
from fastapi.testclient import TestClient

from app import app, get_database, get_current_token
from .utils import override_get_database, override_user_dependency, create_all_models, test_user

client = TestClient(app=app)
create_all_models()

app.dependency_overrides[get_database] = override_get_database
app.dependency_overrides[get_current_token] = override_user_dependency


def test_get_all_users_empty(test_user):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_all_users():
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_current_fail(test_user):
    response = client.get("/users/current")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "Not Found"}
