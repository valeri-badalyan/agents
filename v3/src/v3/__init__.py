"""V3 Orchestrator Agent — Coordinates all other agents."""

from v3.orchestrator import Orchestrator, V3
from v3.registry import AgentRegistry
from v3.router import Router
from v3.session import Session

__version__ = "1.0.0"
__all__ = ["AgentRegistry", "Orchestrator", "Router", "Session", "V3"]
