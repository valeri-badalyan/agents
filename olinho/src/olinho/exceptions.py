"""Custom exceptions for Olinho agent."""


class OlinhoError(Exception):
    """Base exception for Olinho errors."""


class IdeaError(OlinhoError):
    """Raised when idea classification or validation fails."""


class BuildError(OlinhoError):
    """Raised when project scaffolding fails."""


class PreviewError(OlinhoError):
    """Raised when browser preview fails."""


class ConfigurationError(OlinhoError):
    """Raised when configuration is invalid."""
