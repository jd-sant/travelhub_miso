from fastapi import Depends
from sqlmodel import Session

from adapters.gateways.stripe_gateway import FakeStripePaymentGateway
from adapters.repositories.payment_repository import SQLModelPaymentRepository
from db.session import get_session
from domain.ports.payment_gateway import PaymentGateway
from domain.ports.payment_repository import PaymentRepository
from domain.use_cases.create_payment_charge import CreatePaymentChargeUseCase
from domain.use_cases.get_payment import GetPaymentUseCase
from domain.use_cases.list_payment_events import ListPaymentEventsUseCase


def get_payment_repository(
    session: Session = Depends(get_session),
) -> PaymentRepository:
    return SQLModelPaymentRepository(session)


def get_payment_gateway() -> PaymentGateway:
    return FakeStripePaymentGateway()


def get_create_payment_charge_use_case(
    repository: PaymentRepository = Depends(get_payment_repository),
    gateway: PaymentGateway = Depends(get_payment_gateway),
) -> CreatePaymentChargeUseCase:
    return CreatePaymentChargeUseCase(repository, gateway)


def get_get_payment_use_case(
    repository: PaymentRepository = Depends(get_payment_repository),
) -> GetPaymentUseCase:
    return GetPaymentUseCase(repository)


def get_list_payment_events_use_case(
    repository: PaymentRepository = Depends(get_payment_repository),
) -> ListPaymentEventsUseCase:
    return ListPaymentEventsUseCase(repository)
