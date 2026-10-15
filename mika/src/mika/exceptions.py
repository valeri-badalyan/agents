"""Custom exceptions for Mika provider agent."""

from __future__ import annotations


class MikaError(Exception):
    """Base exception for Mika errors."""


class TariffError(MikaError):
    """Raised when tariff lookup or recommendation fails."""


class CoverageError(MikaError):
    """Raised when coverage check fails."""


class DiagnosisError(MikaError):
    """Raised when connection diagnosis fails."""


class ConnectionError(MikaError):
    """Raised when connection steps cannot be built."""


class ReportError(MikaError):
    """Raised when localized reply/report generation fails."""


class ConfigurationError(MikaError):
    """Raised when configuration is invalid."""
