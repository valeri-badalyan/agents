"""Enrique — humorous trilingual companion (RU/AM/EN) with SSOT memory."""

from enrique.config import settings
from enrique.core import Enrique, companion, contains_trigger, detect_language
from enrique.exceptions import (
    ConfigurationError,
    EnriqueError,
    LanguageError,
    MemoryError,
    ValidationError,
)
from enrique.memory import MemoryStore

__version__ = "0.1.0"
__all__ = [
    "ConfigurationError",
    "Enrique",
    "EnriqueError",
    "LanguageError",
    "MemoryError",
    "MemoryStore",
    "ValidationError",
    "companion",
    "contains_trigger",
    "detect_language",
    "settings",
]
