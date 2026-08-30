"""Agent registry — discovers and manages agents in the repository."""

from __future__ import annotations

from pathlib import Path
from typing import Any


class AgentRegistry:
    """Discovers and tracks agents in the repository."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self._agents: dict[str, Path] = {}
        self._excluded = {"valeri", "__pycache__", ".git", ".github", "node_modules"}

    def discover_agents(self) -> list[str]:
        """Discover all agent folders in the repository."""
        self._agents.clear()

        for item in self.repo_root.iterdir():
            if (
                item.is_dir()
                and item.name not in self._excluded
                and not item.name.startswith(".")
                and (item / "src").exists() or (item / "pyproject.toml").exists()
            ):
                self._agents[item.name] = item

        return sorted(self._agents.keys())

    def get_agent_path(self, agent_name: str) -> Path | None:
        """Get the path to an agent's folder."""
        if agent_name in self._agents:
            return self._agents[agent_name]

        path = self.repo_root / agent_name
        if path.exists() and path.is_dir():
            self._agents[agent_name] = path
            return path

        return None

    def get_agent_config(self, agent_name: str) -> dict[str, Any] | None:
        """Get agent configuration from pyproject.toml."""
        import tomllib

        agent_path = self.get_agent_path(agent_name)
        if not agent_path:
            return None

        config_path = agent_path / "pyproject.toml"
        if not config_path.exists():
            return None

        with open(config_path, "rb") as f:
            return tomllib.load(f)

    def is_agent_valid(self, agent_name: str) -> bool:
        """Check if an agent folder has required structure."""
        agent_path = self.get_agent_path(agent_name)
        if not agent_path:
            return False

        has_src = (agent_path / "src").exists()
        has_readme = (agent_path / "README.md").exists()
        has_config = (agent_path / "pyproject.toml").exists()

        return has_src and has_readme and has_config

    def list_valid_agents(self) -> list[str]:
        """List only valid agents with proper structure."""
        all_agents = self.discover_agents()
        return [name for name in all_agents if self.is_agent_valid(name)]

    def __repr__(self) -> str:
        return f"AgentRegistry(agents={len(self._agents)})"