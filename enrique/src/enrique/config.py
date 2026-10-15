"""Enrique settings — typed configuration via environment variables."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for Enrique."""

    default_language: str | None = None
    memory_path: str = "./enrique_memory.json"
    max_history: int = 200
    max_facts: int = 100
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
