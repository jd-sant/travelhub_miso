import importlib.util
import os
import sys
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.security import verify_password


def _load_users_service_module(db_url: str):
    os.environ["DATABASE_URL"] = db_url
    service_path = Path(__file__).resolve().parents[1] / "main.py"
    service_dir = str(service_path.parent)
    if service_dir not in sys.path:
        sys.path.append(service_dir)

    spec = importlib.util.spec_from_file_location("users_service_test_module", service_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("No se pudo cargar el modulo main del backend")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _build_client(module):
    app = FastAPI()
    app.include_router(module.router, prefix="/api/v1")
    module.create_db_and_tables()
    return TestClient(app)


@pytest.fixture(scope="module")
def users_module(tmp_path_factory):
    db_file = tmp_path_factory.mktemp("users_service") / "users_test.db"
    module = _load_users_service_module(f"sqlite:///{db_file}")
    module.create_db_and_tables()
    return module


@pytest.fixture
def client(users_module):
    with users_module.Session(users_module.engine) as session:
        existing_users = session.exec(users_module.select(users_module.User)).all()
        for user in existing_users:
            session.delete(user)
        session.commit()

    return _build_client(users_module)


def test_create_user_hashes_password_and_returns_public_fields(client, users_module):
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

    with users_module.Session(users_module.engine) as session:
        stored_user = session.exec(
            users_module.select(users_module.User).where(
                users_module.User.correo_electronico == payload["correo_electronico"]
            )
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
