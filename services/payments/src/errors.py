from uuid import UUID


class PaymentNotFoundError(Exception):
    pass


class DuplicatePaymentError(Exception):
    def __init__(self, duplicate_payment_id: UUID):
        self.duplicate_payment_id = duplicate_payment_id
        super().__init__(f"Duplicate payment detected: {duplicate_payment_id}")


class InvalidChecksumError(Exception):
    pass


class InsecureTransportError(Exception):
    pass


class PaymentCheckoutSessionNotFoundError(Exception):
    pass


class StripeConfigurationError(Exception):
    pass


class StripeWebhookVerificationError(Exception):
    pass
