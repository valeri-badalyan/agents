"""Messi configuration via pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for Messi agent."""

    default_position: str = "forward"
    default_formation: str = "4-3-3"
    default_level: str = "beginner"
    max_retries: int = 3
    request_timeout: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
