"""Agent registry — discovers and manages agents in the repository."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class AgentRegistry:
    """Discovers and tracks agents in the repository."""

    def __init__(self, repo_root: Path) -> None:
        """Initialize registry with repository root.

        Args:
            repo_root: Path to the agents repository root.
        """
        self.repo_root = repo_root
        self._agents: dict[str, Path] = {}
        # Both orchestrators are excluded from discovery to avoid self-loading.
        self._excluded = {
            "v3",
            "valeri",
            "__pycache__",
            ".git",
            ".github",
            "node_modules",
            "projects",
        }

    def discover_agents(self) -> list[str]:
        """Discover all agent folders in the repository.

        Returns:
            Sorted list of discovered agent names.
        """
        self._agents.clear()
        try:
            entries = list(self.repo_root.iterdir())
        except OSError as exc:
            logger.error("Failed to list repo root %s: %s", self.repo_root, exc)
            return []

        for item in entries:
            if (
                item.is_dir()
                and item.name not in self._excluded
                and not item.name.startswith(".")
                and ((item / "src").exists() or (item / "pyproject.toml").exists())
            ):
                self._agents[item.name] = item

        return sorted(self._agents.keys())

    def get_agent_path(self, agent_name: str) -> Path | None:
        """Get the path to an agent's folder.

        Args:
            agent_name: Name of the agent.

        Returns:
            Path to agent folder, or None if not found.
        """
        if not agent_name or not isinstance(agent_name, str):
            logger.warning("Invalid agent name requested: %r", agent_name)
            return None
        if agent_name in self._agents:
            return self._agents[agent_name]

        path = self.repo_root / agent_name
        if path.exists() and path.is_dir():
            self._agents[agent_name] = path
            return path

        return None

    def get_agent_config(self, agent_name: str) -> dict[str, Any] | None:
        """Get agent configuration from pyproject.toml.

        Args:
            agent_name: Name of the agent.

        Returns:
            Parsed config dict, or None on failure.
        """
        try:
            import tomllib
        except ImportError as exc:
            logger.error("tomllib unavailable: %s", exc)
            return None

        agent_path = self.get_agent_path(agent_name)
        if not agent_path:
            return None

        config_path = agent_path / "pyproject.toml"
        if not config_path.exists():
            return None

        try:
            with open(config_path, "rb") as f:
                data: dict[str, Any] = tomllib.load(f)
                return data
        except OSError as exc:
            logger.error("Failed to read config for %s: %s", agent_name, exc)
            return None

    def is_agent_valid(self, agent_name: str) -> bool:
        """Check if an agent folder has required structure.

        Args:
            agent_name: Name of the agent.

        Returns:
            True if src, README.md and pyproject.toml exist.
        """
        agent_path = self.get_agent_path(agent_name)
        if not agent_path:
            return False

        has_src = (agent_path / "src").exists()
        has_readme = (agent_path / "README.md").exists()
        has_config = (agent_path / "pyproject.toml").exists()

        return has_src and has_readme and has_config

    def list_valid_agents(self) -> list[str]:
        """List only valid agents with proper structure.

        Returns:
            List of valid agent names.
        """
        all_agents = self.discover_agents()
        return [name for name in all_agents if self.is_agent_valid(name)]

    def __repr__(self) -> str:
        return f"AgentRegistry(agents={len(self._agents)})"
