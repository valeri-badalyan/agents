"""Custom exceptions for Ferracho analyzer agent."""


class FerrachoError(Exception):
    """Base exception for Ferracho errors."""


class SwotError(FerrachoError):
    """Raised when SWOT analysis input is invalid."""


class FunnelError(FerrachoError):
    """Raised when funnel analysis input is invalid."""


class UnitEconomicsError(FerrachoError):
    """Raised when unit economics computation fails."""


class RiskError(FerrachoError):
    """Raised when risk matrix input is invalid."""


class AnalysisError(FerrachoError):
    """Raised when general audit report fails."""


class ConfigurationError(FerrachoError):
    """Raised when configuration is invalid."""
