import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine, select

from core.security import verify_password
from db.session import get_session
from adapters.models.user import User
from entrypoints.api.routers.users import router as users_router
from errors import UserConflictError


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
        "correo_electronico": "ana@example.com",
        "telefono": "3001234567",
        "contrasena": "miPasswordSegura123",
        "estado": 1,
    }

    response = client.post("/api/v1/users", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["correo_electronico"] == payload["correo_electronico"]
    assert body["telefono"] == payload["telefono"]
    assert body["estado"] == payload["estado"]
    assert "id_usuario" in body
    assert "contrasena" not in body

    with Session(test_engine) as session:
        stored_user = session.exec(
            select(User).where(User.correo_electronico == payload["correo_electronico"])
        ).first()

    assert stored_user is not None
    assert stored_user.contrasena != payload["contrasena"]
    assert stored_user.contrasena.startswith("pbkdf2_sha256$")
    assert verify_password(payload["contrasena"], stored_user.contrasena)


def test_get_users_returns_created_users(client):
    user_1 = {
        "correo_electronico": "uno@example.com",
        "telefono": "3000000001",
        "contrasena": "passwordSegura1",
        "estado": 1,
    }
    user_2 = {
        "correo_electronico": "dos@example.com",
        "telefono": "3000000002",
        "contrasena": "passwordSegura2",
        "estado": 0,
    }

    assert client.post("/api/v1/users", json=user_1).status_code == 201
    assert client.post("/api/v1/users", json=user_2).status_code == 201

    response = client.get("/api/v1/users")

    assert response.status_code == 200
    users = response.json()
    assert len(users) == 2
    emails = {item["correo_electronico"] for item in users}
    assert emails == {"uno@example.com", "dos@example.com"}
    assert all("contrasena" not in item for item in users)


def test_create_user_returns_409_on_duplicate_email(client):
    payload = {
        "correo_electronico": "dup@example.com",
        "telefono": "3001239999",
        "contrasena": "miPasswordSegura123",
        "estado": 1,
    }

    response1 = client.post("/api/v1/users", json=payload)
    assert response1.status_code == 201

    response2 = client.post("/api/v1/users", json=payload)
    assert response2.status_code == 409
    assert response2.json() == {"detail": "El correo_electronico ya existe"}
