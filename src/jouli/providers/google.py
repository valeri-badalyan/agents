from deep_translator import GoogleTranslator
from deep_translator.exceptions import (
    LanguageNotSupportedException,
    RequestError,
    TranslationNotFound,
)

from jouli.config import settings
from jouli.exceptions import LanguageError, ProviderError
from jouli.providers.base import TranslationResult, TranslatorProvider


class GoogleProvider(TranslatorProvider):
    """Google Translate provider using deep-translator."""

    def __init__(self):
        self._translator = GoogleTranslator(
            source="auto",
            target="en",
        )
        if settings.google_translate_api_key:
            self._translator = GoogleTranslator(
                source="auto",
                target="en",
                api_key=settings.google_translate_api_key,
            )

    @property
    def name(self) -> str:
        return "google"

    def translate(
        self,
        text: str,
        target_lang: str,
        source_lang: str | None = None,
    ) -> TranslationResult:
        try:
            translator = GoogleTranslator(
                source=source_lang or "auto",
                target=target_lang,
                api_key=settings.google_translate_api_key,
            )
            result = translator.translate(text)
            detected_source = source_lang or translator.detect(text)
            return TranslationResult(
                text=result,
                source_lang=detected_source,
                target_lang=target_lang,
                provider=self.name,
            )
        except LanguageNotSupportedException as e:
            raise LanguageError(f"Unsupported language: {e}") from e
        except TranslationNotFound as e:
            raise ProviderError(self.name, f"Translation not found: {e}") from e
        except RequestError as e:
            raise ProviderError(self.name, f"Request failed: {e}") from e
        except Exception as e:
            raise ProviderError(self.name, f"Unexpected error: {e}") from e

    def detect_language(self, text: str) -> str:
        try:
            return GoogleTranslator(source="auto", target="en").detect(text)
        except Exception as e:
            raise ProviderError(self.name, f"Language detection failed: {e}") from e

    def get_supported_languages(self) -> list[str]:
        return GoogleTranslator.get_supported_languages()