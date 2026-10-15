"""Mika configuration via pydantic-settings."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for Mika provider agent."""

    default_lang: str = "ru"
    default_currency: str = "RUB"
    support_phone: str = "8-800-555-35-35"
    support_hours: str = "24/7"
    max_retries: int = 3
    request_timeout: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
