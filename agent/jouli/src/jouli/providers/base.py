from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class TranslationResult:
    text: str
    source_lang: str
    target_lang: str
    provider: str


class TranslatorProvider(ABC):
    """Abstract base class for translation providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider identifier (e.g., 'google', 'deepl')."""

    @abstractmethod
    def translate(
        self,
        text: str,
        target_lang: str,
        source_lang: str | None = None,
    ) -> TranslationResult:
        """Translate text to target language."""

    @abstractmethod
    def detect_language(self, text: str) -> str:
        """Detect the language of the given text."""

    @abstractmethod
    def get_supported_languages(self) -> list[str]:
        """Return list of supported language codes."""
