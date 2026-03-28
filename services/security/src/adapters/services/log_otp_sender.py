import logging

from domain.ports.otp_sender import OtpSender

logger = logging.getLogger(__name__)


class LogOtpSender(OtpSender):
    def send(self, email: str, code: str) -> None:
        logger.info("[OTP] %s: %s", email, code)
