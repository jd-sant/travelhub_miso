from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine, select

from adapters.models.payment import Payment
from adapters.models.payment_event import PaymentEvent
from core.config import settings
from core.security import build_request_checksum, hash_token
from db.session import get_session
from entrypoints.api.routers import payments as payments_router


SECURE_HEADERS = {"x-forwarded-proto": "https"}


def _build_app(test_engine):
    app = FastAPI()
    app.include_router(payments_router.router, prefix="/api/v1")

    def override_get_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    return app


@pytest.fixture(scope="function")
def test_engine():
    db_file = Path(__file__).resolve().parent / "payments_test.db"
    if db_file.exists():
        db_file.unlink()
    engine = create_engine(
        f"sqlite:///{db_file}",
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()
    if db_file.exists():
        db_file.unlink()


@pytest.fixture
def client(test_engine):
    with Session(test_engine) as session:
        for event in session.exec(select(PaymentEvent)).all():
            session.delete(event)
        for payment in session.exec(select(Payment)).all():
            session.delete(payment)
        session.commit()

    app = _build_app(test_engine)
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def _payload(token: str = "pm_tok_visa_ok") -> dict:
    return {
        "reservation_id": str(uuid4()),
        "traveler_id": str(uuid4()),
        "payment_method_token": token,
        "amount_in_cents": 125000,
        "currency": "cop",
        "idempotency_key": "booking-123-attempt-1",
    }


def test_create_payment_success_generates_receipt_and_events(client, test_engine):
    payload = _payload()

    response = client.post("/api/v1/payments/charges", json=payload, headers=SECURE_HEADERS)

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "confirmed"
    assert body["currency"] == "COP"
    assert body["receipt_id"] is not None
    assert body["receipt_number"].startswith("RCPT-")
    assert body["failure_reason"] is None
    assert "payment_method_token" not in body

    with Session(test_engine) as session:
        stored_payment = session.exec(select(Payment)).first()
        stored_events = session.exec(select(PaymentEvent)).all()

    assert stored_payment is not None
    assert stored_payment.payment_method_token_hash == hash_token(payload["payment_method_token"])
    assert stored_payment.payment_method_token_hash != payload["payment_method_token"]
    assert {event.event_type for event in stored_events} == {
        "payment.succeeded",
        "reservation.confirmation.requested",
        "inventory.update.requested",
        "receipt.generated",
    }


def test_create_payment_failure_returns_clear_reason(client, test_engine):
    payload = _payload(token="pm_fail_insufficient_funds")

    response = client.post("/api/v1/payments/charges", json=payload, headers=SECURE_HEADERS)

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "failed"
    assert body["failure_reason"] == "insufficient_funds"
    assert body["receipt_id"] is None

    with Session(test_engine) as session:
        stored_events = session.exec(select(PaymentEvent)).all()

    assert [event.event_type for event in stored_events] == ["payment.failed"]


def test_create_payment_rejects_duplicate_within_two_seconds(client):
    payload = _payload()

    first_response = client.post("/api/v1/payments/charges", json=payload, headers=SECURE_HEADERS)
    second_response = client.post("/api/v1/payments/charges", json=payload, headers=SECURE_HEADERS)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"]["message"] == (
        "Se detecto una transaccion duplicada en menos de 2 segundos."
    )


def test_create_payment_rejects_reused_idempotency_key(client):
    payload = _payload()

    first_response = client.post("/api/v1/payments/charges", json=payload, headers=SECURE_HEADERS)

    retry_payload = _payload(token="pm_tok_mastercard_ok")
    retry_payload["reservation_id"] = payload["reservation_id"]
    retry_payload["traveler_id"] = payload["traveler_id"]
    retry_payload["amount_in_cents"] = payload["amount_in_cents"]
    retry_payload["currency"] = payload["currency"]
    retry_payload["idempotency_key"] = payload["idempotency_key"]

    second_response = client.post(
        "/api/v1/payments/charges",
        json=retry_payload,
        headers=SECURE_HEADERS,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_create_payment_rejects_invalid_checksum(client):
    payload = _payload()
    payload["request_checksum"] = "b" * 64

    response = client.post("/api/v1/payments/charges", json=payload, headers=SECURE_HEADERS)

    assert response.status_code == 400
    assert response.json() == {"detail": "Checksum de integridad invalido."}


def test_create_payment_accepts_valid_checksum(client):
    payload = _payload()
    canonical_payload = "|".join(
        [
            payload["reservation_id"],
            payload["traveler_id"],
            str(payload["amount_in_cents"]),
            payload["currency"].upper(),
            payload["payment_method_token"],
            payload["idempotency_key"],
        ]
    )
    payload["request_checksum"] = build_request_checksum(
        canonical_payload,
        settings.payment_integrity_secret,
    )

    response = client.post("/api/v1/payments/charges", json=payload, headers=SECURE_HEADERS)

    assert response.status_code == 201


def test_get_payment_by_id_returns_created_payment(client):
    create_response = client.post("/api/v1/payments/charges", json=_payload(), headers=SECURE_HEADERS)
    payment_id = create_response.json()["payment_id"]

    response = client.get(f"/api/v1/payments/{payment_id}")

    assert response.status_code == 200
    assert response.json()["payment_id"] == payment_id


def test_list_events_returns_created_events(client):
    create_response = client.post("/api/v1/payments/charges", json=_payload(), headers=SECURE_HEADERS)
    payment_id = create_response.json()["payment_id"]

    response = client.get(f"/api/v1/payments/{payment_id}/events")

    assert response.status_code == 200
    assert len(response.json()) == 4


def test_tls_header_can_be_enforced(client, monkeypatch):
    monkeypatch.setattr(
        payments_router,
        "settings",
        SimpleNamespace(enforce_tls_header=True),
    )

    response = client.post("/api/v1/payments/charges", json=_payload())

    assert response.status_code == 400
    assert response.json() == {"detail": "TLS 1.2+ is required for payment requests"}

    secure_response = client.post(
        "/api/v1/payments/charges",
        json=_payload(),
        headers={"x-forwarded-proto": "https"},
    )
    assert secure_response.status_code == 201

    monkeypatch.setattr(
        payments_router,
        "settings",
        settings,
    )
