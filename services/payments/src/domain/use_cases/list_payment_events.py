from uuid import UUID

from domain.ports.payment_repository import PaymentRepository
from domain.schemas.payment import PaymentEventResponse
from domain.use_cases.base import BaseUseCase


class ListPaymentEventsUseCase(BaseUseCase[UUID, list[PaymentEventResponse]]):
    def __init__(self, repository: PaymentRepository):
        self.repository = repository

    def execute(self, payment_id: UUID) -> list[PaymentEventResponse]:
        return self.repository.list_events(payment_id)
