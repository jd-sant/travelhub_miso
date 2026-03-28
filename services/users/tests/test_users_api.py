import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine, select

from core.security import verify_password
from db.session import get_session
from adapters.models.user import User
from entrypoints.api.routers.users import router as users_router


def _build_app(test_engine):
    app = FastAPI()
    app.include_router(users_router, prefix="/api/v1")

    def override_get_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    return app


@pytest.fixture(scope="module")
def test_engine(tmp_path_factory):
    db_file = tmp_path_factory.mktemp("users_service") / "users_test.db"
    engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def client(test_engine):
    with Session(test_engine) as session:
        existing_users = session.exec(select(User)).all()
        for user in existing_users:
            session.delete(user)
        session.commit()

    app = _build_app(test_engine)
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_create_user_hashes_password_and_returns_public_fields(client, test_engine):
    payload = {
        "email": "ana@example.com",
        "phone": "3001234567",
        "password": "miPasswordSegura123",
        "status": 1,
    }

    response = client.post("/api/v1/users", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == payload["email"]
    assert body["phone"] == payload["phone"]
    assert body["status"] == payload["status"]
    assert "id" in body
    assert "password" not in body

    with Session(test_engine) as session:
        stored_user = session.exec(
            select(User).where(User.email == payload["email"])
        ).first()

    assert stored_user is not None
    assert stored_user.password != payload["password"]
    assert stored_user.password.startswith("pbkdf2_sha256$")
    assert verify_password(payload["password"], stored_user.password)


def test_get_users_returns_created_users(client):
    user_1 = {
        "email": "uno@example.com",
        "phone": "3000000001",
        "password": "passwordSegura1",
        "status": 1,
    }
    user_2 = {
        "email": "dos@example.com",
        "phone": "3000000002",
        "password": "passwordSegura2",
        "status": 0,
    }

    assert client.post("/api/v1/users", json=user_1).status_code == 201
    assert client.post("/api/v1/users", json=user_2).status_code == 201

    response = client.get("/api/v1/users")

    assert response.status_code == 200
    users = response.json()
    assert len(users) == 2
    emails = {item["email"] for item in users}
    assert emails == {"uno@example.com", "dos@example.com"}
    assert all("password" not in item for item in users)


def test_create_user_returns_409_on_duplicate_email(client):
    payload = {
        "email": "dup@example.com",
        "phone": "3001239999",
        "password": "miPasswordSegura123",
        "status": 1,
    }

    response1 = client.post("/api/v1/users", json=payload)
    assert response1.status_code == 201

    response2 = client.post("/api/v1/users", json=payload)
    assert response2.status_code == 409
    assert response2.json() == {"detail": "El correo electrónico ya existe"}
