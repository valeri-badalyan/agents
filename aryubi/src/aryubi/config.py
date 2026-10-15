"""Aryubi configuration via pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for Aryubi finance agent."""

    default_lang: str = "ru"
    precision: int = 2
    default_currency: str = "RUB"
    monthly_savings_target_pct: float = 20.0
    max_retries: int = 3
    request_timeout: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
