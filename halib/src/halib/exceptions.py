"""Custom exceptions for Halib designer agent."""


class HalibError(Exception):
    """Base exception for Halib errors."""


class ConceptError(HalibError):
    """Raised when design concept input is invalid."""


class PaletteError(HalibError):
    """Raised when palette input is invalid."""


class TypographyError(HalibError):
    """Raised when typography input is invalid."""


class LayoutError(HalibError):
    """Raised when layout input is invalid."""


class AuditError(HalibError):
    """Raised when design audit input is invalid."""


class ConfigurationError(HalibError):
    """Raised when configuration is invalid."""
