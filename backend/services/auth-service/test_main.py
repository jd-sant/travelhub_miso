import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "auth-service"}


def test_register_user():
    response = client.post("/auth/register", json={"username": "testuser", "password": "secret"})
    assert response.status_code == 201
    assert response.json()["message"] == "User registered successfully"


def test_register_duplicate_user():
    client.post("/auth/register", json={"username": "dupuser", "password": "secret"})
    response = client.post("/auth/register", json={"username": "dupuser", "password": "secret"})
    assert response.status_code == 400


def test_login():
    client.post("/auth/register", json={"username": "loginuser", "password": "mypassword"})
    response = client.post(
        "/auth/token",
        data={"username": "loginuser", "password": "mypassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials():
    response = client.post(
        "/auth/token",
        data={"username": "nouser", "password": "wrong"},
    )
    assert response.status_code == 401
