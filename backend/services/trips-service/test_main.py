import pytest
from fastapi.testclient import TestClient
from main import app, TRIPS

client = TestClient(app)


def setup_function():
    TRIPS.clear()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "trips-service"}


def test_list_trips_empty():
    response = client.get("/trips")
    assert response.status_code == 200
    assert response.json() == []


def test_create_trip():
    payload = {
        "name": "Paris Adventure",
        "destination": "Paris, France",
        "description": "A trip to Paris",
        "start_date": "2025-06-01",
        "end_date": "2025-06-10",
        "price": 1500.0,
    }
    response = client.post("/trips", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Paris Adventure"
    assert "id" in data


def test_get_trip():
    payload = {
        "name": "Tokyo Tour",
        "destination": "Tokyo, Japan",
        "start_date": "2025-07-01",
        "end_date": "2025-07-15",
        "price": 3000.0,
    }
    created = client.post("/trips", json=payload).json()
    trip_id = created["id"]

    response = client.get(f"/trips/{trip_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Tokyo Tour"


def test_get_trip_not_found():
    response = client.get("/trips/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_delete_trip():
    payload = {
        "name": "Rome Trip",
        "destination": "Rome, Italy",
        "start_date": "2025-08-01",
        "end_date": "2025-08-08",
        "price": 1200.0,
    }
    created = client.post("/trips", json=payload).json()
    trip_id = created["id"]

    response = client.delete(f"/trips/{trip_id}")
    assert response.status_code == 204

    response = client.get(f"/trips/{trip_id}")
    assert response.status_code == 404
