"""Custom exceptions for Marika statistics agent."""


class MarikaError(Exception):
    """Base exception for Marika errors."""


class StatisticsError(MarikaError):
    """Raised when descriptive statistics computation fails."""


class GrowthError(MarikaError):
    """Raised when growth rate computation fails."""


class TrendError(MarikaError):
    """Raised when trend analysis fails."""


class SharesError(MarikaError):
    """Raised when share/percentage breakdown fails."""


class ReportError(MarikaError):
    """Raised when report generation fails."""


class ConfigurationError(MarikaError):
    """Raised when configuration is invalid."""
