"""Ferracho package exports."""

from ferracho.config import settings
from ferracho.core import Ferracho, engine
from ferracho.exceptions import (
    AnalysisError,
    ConfigurationError,
    FerrachoError,
    FunnelError,
    RiskError,
    SwotError,
    UnitEconomicsError,
)

__version__ = "0.1.0"
__all__ = [
    "AnalysisError",
    "ConfigurationError",
    "Ferracho",
    "FerrachoError",
    "FunnelError",
    "RiskError",
    "SwotError",
    "UnitEconomicsError",
    "engine",
    "settings",
]
