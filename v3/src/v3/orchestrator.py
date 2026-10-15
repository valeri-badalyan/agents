"""Main orchestrator logic — V3 coordinates all agents."""

from __future__ import annotations

import importlib
import logging
import sys
from pathlib import Path
from typing import Any

from v3.registry import AgentRegistry
from v3.router import Router
from v3.session import Session

logger = logging.getLogger(__name__)


class Orchestrator:
    """Master orchestrator V3 that coordinates all agents."""

    def __init__(self, repo_root: Path | None = None) -> None:
        """Initialize orchestrator.

        Args:
            repo_root: Optional repository root path.
        """
        self.repo_root = repo_root or self._find_repo_root()
        self.registry = AgentRegistry(self.repo_root)
        self.router = Router(self.registry)
        self.sessions: dict[str, Session] = {}
        self._loaded_agents: dict[str, Any] = {}

    def _find_repo_root(self) -> Path:
        """Find the repository root directory.

        Returns:
            Path to repo root.
        """
        current = Path(__file__).parent
        while current != current.parent:
            if (current / ".git").exists() or (current / "agents").exists():
                return current
            current = current.parent
        return Path.cwd()

    def load_agents(self) -> list[str]:
        """Load all agents from the repository.

        Returns:
            List of successfully loaded agent names.
        """
        agents = self.registry.discover_agents()
        loaded = []
        for agent_name in agents:
            try:
                self.load_agent(agent_name)
                loaded.append(agent_name)
            except (ImportError, ValueError) as e:
                logger.warning("Failed to load agent '%s': %s", agent_name, e)
        return loaded

    def load_agent(self, agent_name: str) -> Any:
        """Load a specific agent by name.

        Args:
            agent_name: Name of the agent.

        Returns:
            Loaded agent instance or module.
        """
        if not agent_name or not isinstance(agent_name, str):
            raise ValueError("Agent name must be a non-empty string")
        if agent_name in self._loaded_agents:
            return self._loaded_agents[agent_name]

        agent_path = self.registry.get_agent_path(agent_name)
        if not agent_path:
            raise ValueError(f"Agent '{agent_name}' not found in repository")

        src_path = agent_path / "src"
        if src_path.exists() and str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            module = importlib.import_module(agent_name)
            agent_class = getattr(module, agent_name.capitalize(), None)
            # Special case: v3 module exposes V3 (uppercase) instead of V3-capitalize lookup
            if agent_class is None and agent_name == "v3":
                agent_class = getattr(module, "V3", None)
            if agent_class:
                try:
                    agent_instance = agent_class()
                except TypeError:
                    # Class requires args — return class itself
                    return agent_class
                self._loaded_agents[agent_name] = agent_instance
                return agent_instance
            return module
        except ImportError as e:
            raise ImportError(f"Could not import agent '{agent_name}': {e}") from e

    def get_agent(self, agent_name: str) -> Any:
        """Get a loaded agent by name.

        Args:
            agent_name: Name of the agent.
        """
        if agent_name not in self._loaded_agents:
            self.load_agent(agent_name)
        return self._loaded_agents[agent_name]

    def route(self, task: str, **kwargs: Any) -> Any:
        """Route a task to the appropriate agent.

        Args:
            task: Task text.
            kwargs: Extra args passed to the agent handler.
        """
        agent_name = self.router.route_task(task)
        agent = self.get_agent(agent_name)

        try:
            if hasattr(agent, "translate"):
                translate = getattr(agent, "translate")
                return translate(task, **kwargs) if callable(translate) else agent
            if hasattr(agent, "execute"):
                execute = getattr(agent, "execute")
                return execute(task, **kwargs) if callable(execute) else agent
            return agent(task, **kwargs) if callable(agent) else agent
        except Exception as exc:
            logger.error("Agent '%s' failed on task: %s", agent_name, exc)
            raise

    def route_all(self, task: str) -> list[str]:
        """Find all agents matching a task.

        Args:
            task: Task text.

        Returns:
            List of matching agent names.
        """
        return self.router.route_all(task)

    def create_session(self, session_id: str | None = None) -> Session:
        """Create a new session.

        Args:
            session_id: Optional explicit session id.
        """
        session = Session(session_id)
        self.sessions[session.id] = session
        return session

    def list_agents(self) -> list[dict[str, Any]]:
        """List all available agents with their status."""
        agents = self.registry.discover_agents()
        return [
            {
                "name": name,
                "loaded": name in self._loaded_agents,
                "path": str(self.registry.get_agent_path(name)),
            }
            for name in agents
        ]

    def __repr__(self) -> str:
        return f"V3 Orchestrator(agents={len(self.list_agents())})"


class V3(Orchestrator):
    """Alias class so session_loader can instantiate via V3()."""

    def __repr__(self) -> str:
        return f"V3(agents={len(self.list_agents())})"
