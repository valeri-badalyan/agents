"""Marika configuration via pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for Marika statistics agent."""

    default_lang: str = "ru"
    precision: int = 2
    default_title: str = "Statistics Report"
    max_retries: int = 3
    request_timeout: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
