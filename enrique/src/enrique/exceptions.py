"""Custom exceptions for Enrique."""


class EnriqueError(Exception):
    """Base exception for Enrique errors."""


class ConfigurationError(EnriqueError):
    """Raised when configuration is invalid."""


class LanguageError(EnriqueError):
    """Raised when language code is invalid or unsupported."""


class MemoryError(EnriqueError):
    """Raised when memory load/save fails."""


class ValidationError(EnriqueError):
    """Raised when user input is invalid."""
