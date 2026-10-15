"""Custom exceptions for Messi agent."""


class MessiError(Exception):
    """Base exception for Messi errors."""


class TacticsError(MessiError):
    """Raised when tactics analysis fails."""


class TrainingError(MessiError):
    """Raised when training plan generation fails."""


class QuizError(MessiError):
    """Raised when quiz generation fails."""


class ConfigurationError(MessiError):
    """Raised when configuration is invalid."""
