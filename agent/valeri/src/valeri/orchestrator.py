"""Main orchestrator logic — coordinates all agents."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

from valeri.registry import AgentRegistry
from valeri.router import Router
from valeri.session import Session


class Orchestrator:
    """Master orchestrator that coordinates all agents."""

    def __init__(self, repo_root: Path | None = None):
        self.repo_root = repo_root or self._find_repo_root()
        self.registry = AgentRegistry(self.repo_root)
        self.router = Router(self.registry)
        self.sessions: dict[str, Session] = {}
        self._loaded_agents: dict[str, Any] = {}

    def _find_repo_root(self) -> Path:
        """Find the repository root directory."""
        current = Path(__file__).parent
        while current != current.parent:
            if (current / ".git").exists() or (current / "agents").exists():
                return current
            current = current.parent
        return Path.cwd()

    def load_agents(self) -> list[str]:
        """Load all agents from the repository."""
        agents = self.registry.discover_agents()
        loaded = []
        for agent_name in agents:
            try:
                self.load_agent(agent_name)
                loaded.append(agent_name)
            except (ImportError, ValueError) as e:
                print(f"Warning: Failed to load agent '{agent_name}': {e}")
        return loaded

    def load_agent(self, agent_name: str) -> Any:
        """Load a specific agent by name."""
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
            if agent_class:
                agent_instance = agent_class()
                self._loaded_agents[agent_name] = agent_instance
                return agent_instance
            else:
                return module
        except ImportError as e:
            raise ImportError(f"Could not import agent '{agent_name}': {e}")

    def get_agent(self, agent_name: str) -> Any:
        """Get a loaded agent by name."""
        if agent_name not in self._loaded_agents:
            self.load_agent(agent_name)
        return self._loaded_agents[agent_name]

    def route(self, task: str, **kwargs: Any) -> Any:
        """Route a task to the appropriate agent."""
        agent_name = self.router.route_task(task)
        agent = self.get_agent(agent_name)

        if hasattr(agent, "translate"):
            return agent.translate(task, **kwargs)
        elif hasattr(agent, "execute"):
            return agent.execute(task, **kwargs)
        else:
            return agent(task, **kwargs) if callable(agent) else agent

    def create_session(self, session_id: str | None = None) -> Session:
        """Create a new session."""
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
        return f"Orchestrator(agents={len(self.list_agents())})"