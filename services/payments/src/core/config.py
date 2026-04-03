import os
from functools import lru_cache


class Settings:
    @property
    def rds_hostname(self) -> str:
        return os.getenv("RDS_HOSTNAME", "localhost")

    @property
    def rds_port(self) -> str:
        return os.getenv("RDS_PORT", "5432")

    @property
    def rds_username(self) -> str:
        return os.getenv("RDS_USERNAME", "travelhub_user")

    @property
    def rds_password(self) -> str:
        return os.getenv("RDS_PASSWORD", "travelhub_pass")

    @property
    def rds_db_name(self) -> str:
        return os.getenv("RDS_DB_NAME", "travelhub")

    @property
    def db_schema(self) -> str:
        return os.getenv("DB_SCHEMA", "payments_schema")

    @property
    def database_url(self) -> str:
        url = os.getenv("DATABASE_URL")
        if url:
            return url
        return (
            f"postgresql://{self.rds_username}:{self.rds_password}"
            f"@{self.rds_hostname}:{self.rds_port}/{self.rds_db_name}"
        )

    @property
    def db_echo(self) -> bool:
        return os.getenv("DB_ECHO", "False").lower() == "true"

    @property
    def payment_provider(self) -> str:
        return os.getenv("PAYMENT_PROVIDER", "fake_stripe")

    @property
    def payment_duplicate_window_seconds(self) -> int:
        return int(os.getenv("PAYMENT_DUPLICATE_WINDOW_SECONDS", "2"))

    @property
    def payment_integrity_secret(self) -> str:
        return os.getenv("PAYMENT_INTEGRITY_SECRET", "travelhub-payments-secret")

    @property
    def enforce_tls_header(self) -> bool:
        return os.getenv("ENFORCE_TLS_HEADER", "True").lower() == "true"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
