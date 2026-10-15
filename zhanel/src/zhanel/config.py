"""Zhanel configuration via pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for Zhanel agent."""

    default_language: str = "ru"
    default_tone: str = "friendly"
    default_brand: str = ""
    default_product: str = ""
    default_weeks: int = 4
    max_retries: int = 3
    request_timeout: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
