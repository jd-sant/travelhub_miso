import pytest
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from db.session import get_session
from entrypoints.api.main import create_application


@pytest.fixture(name="session")
def session_fixture():
    """Create an in-memory SQLite database for testing"""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    from db.session import SQLModel
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client with the app"""
    def get_session_override():
        return session

    app = create_application()
    from fastapi.testclient import TestClient
    from assembly import get_accommodation_repository

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
