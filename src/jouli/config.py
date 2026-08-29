from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    google_translate_api_key: str | None = None
    default_source_lang: str | None = None
    default_target_lang: str = "en"
    request_timeout: int = 30
    max_retries: int = 3

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()