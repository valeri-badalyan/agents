"""Olinho configuration via pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for Olinho agent."""

    default_projects_dir: str = "projects"
    default_browser: str = "chrome"
    default_type: str = "landing"
    default_language: str = "ru"
    max_retries: int = 3

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
