from datetime import datetime, timezone
from uuid import uuid4

from core.config import settings
from domain.ports.payment_checkout_repository import PaymentCheckoutRepository
from domain.schemas.checkout import (
    PaymentCheckoutSessionRecord,
    PaymentCheckoutSessionRequest,
    PaymentCheckoutSessionResponse,
)
from domain.use_cases.base import BaseUseCase


class CreatePaymentCheckoutSessionUseCase(
    BaseUseCase[PaymentCheckoutSessionRequest, PaymentCheckoutSessionResponse]
):
    def __init__(self, repository: PaymentCheckoutRepository):
        self.repository = repository

    def execute(self, payload: PaymentCheckoutSessionRequest) -> PaymentCheckoutSessionResponse:
        now = datetime.now(timezone.utc)
        session = PaymentCheckoutSessionRecord(
            payment_transaction_id=uuid4(),
            reservation_id=payload.reservation_id,
            traveler_id=payload.traveler_id,
            amount_in_cents=payload.amount_in_cents,
            currency=payload.currency,
            property_name=payload.property_name,
            check_in_date=payload.check_in_date,
            check_out_date=payload.check_out_date,
            idempotency_key=f"stripe-checkout-{uuid4()}",
            status="created",
            created_at=now,
            updated_at=now,
        )
        stored = self.repository.create_session(session)
        return PaymentCheckoutSessionResponse(
            payment_transaction_id=stored.payment_transaction_id,
            amount_in_cents=stored.amount_in_cents,
            currency=stored.currency,
            publishable_key=settings.stripe_publishable_key,
            stripe_enabled=settings.stripe_enabled,
        )
