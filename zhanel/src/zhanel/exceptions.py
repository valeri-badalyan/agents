"""Custom exceptions for Zhanel agent."""


class ZhanelError(Exception):
    """Base exception for Zhanel errors."""


class StrategyError(ZhanelError):
    """Raised when strategy / positioning fails."""


class CopyError(ZhanelError):
    """Raised when copywriting generation fails."""


class ContentPlanError(ZhanelError):
    """Raised when content plan generation fails."""


class AuditError(ZhanelError):
    """Raised when idea audit fails."""


class ConfigurationError(ZhanelError):
    """Raised when configuration is invalid."""
