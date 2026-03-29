from datetime import datetime, timedelta, timezone
from uuid import uuid4

from core.config import settings
from core.security import build_payment_fingerprint, build_request_checksum, hash_token, verify_checksum
from domain.ports.payment_gateway import PaymentGateway
from domain.ports.payment_repository import PaymentRepository
from domain.schemas.payment import (
    PaymentChargeRequest,
    PaymentChargeResponse,
    PaymentEventResponse,
    PaymentPublicResponse,
    PaymentStatus,
)
from domain.use_cases.base import BaseUseCase
from errors import DuplicatePaymentError, InvalidChecksumError


class CreatePaymentChargeUseCase(BaseUseCase[PaymentChargeRequest, PaymentPublicResponse]):
    def __init__(
        self,
        repository: PaymentRepository,
        gateway: PaymentGateway,
    ):
        self.repository = repository
        self.gateway = gateway

    def execute(self, payload: PaymentChargeRequest) -> PaymentPublicResponse:
        canonical_payload = self._canonical_payload(payload)
        if payload.request_checksum and not verify_checksum(
            payload=canonical_payload,
            expected_checksum=payload.request_checksum,
            secret=settings.payment_integrity_secret,
        ):
            raise InvalidChecksumError("Invalid payment checksum")

        request_checksum = payload.request_checksum or build_request_checksum(
            canonical_payload,
            settings.payment_integrity_secret,
        )

        token_hash = hash_token(payload.payment_method_token)
        request_fingerprint = build_payment_fingerprint(
            reservation_id=str(payload.reservation_id),
            traveler_id=str(payload.traveler_id),
            amount_in_cents=payload.amount_in_cents,
            currency=payload.currency,
            token_hash=token_hash,
        )

        since = datetime.now(timezone.utc) - timedelta(
            seconds=settings.payment_duplicate_window_seconds
        )
        duplicate_payment = self.repository.find_recent_duplicate(
            request_fingerprint=request_fingerprint,
            since=since,
        )
        if duplicate_payment is not None:
            raise DuplicatePaymentError(duplicate_payment.payment_id)

        gateway_result = self.gateway.charge(payload)
        now = datetime.now(timezone.utc)
        payment = PaymentChargeResponse(
            payment_id=uuid4(),
            reservation_id=payload.reservation_id,
            traveler_id=payload.traveler_id,
            status=gateway_result.status,
            amount_in_cents=payload.amount_in_cents,
            currency=payload.currency,
            gateway_charge_id=gateway_result.gateway_charge_id,
            gateway_status=gateway_result.gateway_status,
            idempotency_key=payload.idempotency_key,
            request_fingerprint=request_fingerprint,
            request_checksum=request_checksum,
            payment_method_token_hash=token_hash,
            failure_reason=gateway_result.failure_reason,
            card_brand=gateway_result.card_brand,
            card_last4=gateway_result.card_last4,
            created_at=now,
            updated_at=now,
        )

        if gateway_result.status == PaymentStatus.confirmed:
            payment.receipt_id = uuid4()
            payment.receipt_number = self._build_receipt_number(now)

        stored_payment = self.repository.save_payment_result(payment)
        self.repository.add_events(stored_payment.payment_id, self._build_events(stored_payment))
        return self._to_public_response(stored_payment)

    def _build_events(self, payment: PaymentChargeResponse) -> list[PaymentEventResponse]:
        now = datetime.now(timezone.utc)
        base_payload = {
            "payment_id": str(payment.payment_id),
            "reservation_id": str(payment.reservation_id),
            "traveler_id": str(payment.traveler_id),
            "amount_in_cents": payment.amount_in_cents,
            "currency": payment.currency,
            "gateway_charge_id": payment.gateway_charge_id,
            "receipt_id": str(payment.receipt_id) if payment.receipt_id else None,
            "receipt_number": payment.receipt_number,
            "status": payment.status.value,
            "failure_reason": payment.failure_reason,
        }

        if payment.status == PaymentStatus.confirmed:
            event_types = [
                "payment.succeeded",
                "reservation.confirmation.requested",
                "inventory.update.requested",
                "receipt.generated",
            ]
        else:
            event_types = ["payment.failed"]

        return [
            PaymentEventResponse(
                event_id=uuid4(),
                payment_id=payment.payment_id,
                event_type=event_type,
                payload=base_payload,
                created_at=now,
            )
            for event_type in event_types
        ]

    def _build_receipt_number(self, created_at: datetime) -> str:
        return created_at.strftime("RCPT-%Y%m%d-%H%M%S")

    def _canonical_payload(self, payload: PaymentChargeRequest) -> str:
        return "|".join(
            [
                str(payload.reservation_id),
                str(payload.traveler_id),
                str(payload.amount_in_cents),
                payload.currency.upper(),
                payload.payment_method_token,
                payload.idempotency_key,
            ]
        )

    def _to_public_response(self, payment: PaymentChargeResponse) -> PaymentPublicResponse:
        return PaymentPublicResponse(
            payment_id=payment.payment_id,
            reservation_id=payment.reservation_id,
            status=payment.status,
            amount_in_cents=payment.amount_in_cents,
            currency=payment.currency,
            gateway_charge_id=payment.gateway_charge_id,
            receipt_id=payment.receipt_id,
            receipt_number=payment.receipt_number,
            failure_reason=payment.failure_reason,
        )
