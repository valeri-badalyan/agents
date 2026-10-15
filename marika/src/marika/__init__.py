"""Marika package exports."""

from marika.config import settings
from marika.core import Marika, engine
from marika.exceptions import (
    ConfigurationError,
    GrowthError,
    MarikaError,
    ReportError,
    SharesError,
    StatisticsError,
    TrendError,
)

__version__ = "0.1.0"
__all__ = [
    "ConfigurationError",
    "GrowthError",
    "Marika",
    "MarikaError",
    "ReportError",
    "SharesError",
    "StatisticsError",
    "TrendError",
    "engine",
    "settings",
]
