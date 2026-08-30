class JouliError(Exception):
    """Base exception for Jouli errors."""


class ProviderError(JouliError):
    """Raised when a translation provider fails."""
    def __init__(self, provider: str, message: str, original: Exception | None = None):
        self.provider = provider
        self.original = original
        super().__init__(f"[{provider}] {message}")


class ConfigurationError(JouliError):
    """Raised when configuration is invalid."""


class LanguageError(JouliError):
    """Raised when language code is invalid or unsupported."""


class TranslationError(JouliError):
    """Raised when translation fails."""
