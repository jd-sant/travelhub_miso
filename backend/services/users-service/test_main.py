import pytest
from fastapi.testclient import TestClient
from main import app, USERS

client = TestClient(app)


def setup_function():
    USERS.clear()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "users-service"}


def test_list_users_empty():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []


def test_create_user():
    payload = {
        "username": "johndoe",
        "email": "john@example.com",
        "full_name": "John Doe",
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "johndoe"
    assert "id" in data


def test_create_duplicate_user():
    payload = {"username": "dupuser", "email": "dup@example.com"}
    client.post("/users", json=payload)
    response = client.post("/users", json=payload)
    assert response.status_code == 400


def test_get_user():
    payload = {"username": "janesmith", "email": "jane@example.com", "full_name": "Jane Smith"}
    created = client.post("/users", json=payload).json()
    user_id = created["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "janesmith"


def test_get_user_not_found():
    response = client.get("/users/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_delete_user():
    payload = {"username": "todelete", "email": "delete@example.com"}
    created = client.post("/users", json=payload).json()
    user_id = created["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
