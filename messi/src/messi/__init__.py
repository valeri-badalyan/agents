"""Messi package exports."""

from messi.config import settings
from messi.core import Messi, engine
from messi.exceptions import (
    ConfigurationError,
    MessiError,
    QuizError,
    TacticsError,
    TrainingError,
)

__version__ = "0.1.0"
__all__ = [
    "ConfigurationError",
    "Messi",
    "MessiError",
    "QuizError",
    "TacticsError",
    "TrainingError",
    "engine",
    "settings",
]
