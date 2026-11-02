"""Sandy configuration via pydantic-settings."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for Sandy music director agent."""

    default_lang: str = "ru"
    default_arc: str = "rise"
    rehearsal_break_every: int = 50
    max_retries: int = 3
    request_timeout: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
