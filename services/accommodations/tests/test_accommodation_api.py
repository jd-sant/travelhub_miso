from uuid import uuid4

from fastapi.testclient import TestClient
from sqlmodel import Session

from adapters.models.accommodation import Accommodation


def test_get_accommodation_endpoint_success(
    client: TestClient, session: Session
):
    """Test GET /api/v1/accommodations/{id} endpoint successfully"""
    accommodation = Accommodation(
        id=uuid4(),
        name="Hotel Paradise",
        description="A beautiful hotel with ocean view",
        location="Miami, USA",
        price_per_night=150.00,
        rating=4.5,
        available_rooms=10,
        status=1,
    )
    session.add(accommodation)
    session.commit()

    response = client.get(f"/api/v1/accommodations/{accommodation.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(accommodation.id)
    assert data["name"] == accommodation.name
    assert data["description"] == accommodation.description
    assert data["location"] == accommodation.location
    assert data["price_per_night"] == accommodation.price_per_night
    assert data["rating"] == accommodation.rating
    assert data["available_rooms"] == accommodation.available_rooms
    assert data["status"] == accommodation.status


def test_get_accommodation_endpoint_not_found(client: TestClient):
    """Test GET /api/v1/accommodations/{id} endpoint when not found"""
    non_existent_id = uuid4()

    response = client.get(f"/api/v1/accommodations/{non_existent_id}")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_health_check(client: TestClient):
    """Test health check endpoint"""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
