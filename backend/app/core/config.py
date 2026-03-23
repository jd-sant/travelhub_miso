from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./users.db"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
