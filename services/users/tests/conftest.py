import os
import sys

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import delete as sa_delete
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from adapters.models.role import Role
from adapters.models.user import User
from adapters.models.user_role import UserRole
from db.session import get_session
from entrypoints.api.routers.internal import router as internal_router
from entrypoints.api.routers.users import router as users_router

# Make tests/ importable so helpers.py can be used
sys.path.insert(0, os.path.dirname(__file__))

from helpers import INTERNAL_API_KEY 


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(autouse=True)
def _clean_tables(test_engine):
    with Session(test_engine) as session:
        session.execute(sa_delete(UserRole))
        session.execute(sa_delete(Role))
        session.execute(sa_delete(User))
        session.commit()


@pytest.fixture
def session(test_engine):
    with Session(test_engine) as session:
        yield session


@pytest.fixture
def client(test_engine):
    os.environ["INTERNAL_API_KEY"] = INTERNAL_API_KEY

    app = FastAPI()
    app.include_router(users_router, prefix="/api/v1")
    app.include_router(internal_router, prefix="/api/v1")

    def override_get_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
