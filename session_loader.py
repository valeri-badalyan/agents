"""Session loader — Main entry point for agent system."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


def find_repo_root() -> Path:
    """Find the repository root directory."""
    current = Path(__file__).parent
    while current != current.parent:
        if (current / ".git").exists() or (current / "agent").exists():
            return current
        current = current.parent
    return Path.cwd()


def get_agent_dir(repo_root: Path | None = None) -> Path:
    """Get the agent directory."""
    root = repo_root or find_repo_root()
    agent_dir = root / "agent"
    if agent_dir.exists():
        return agent_dir
    return root


def load_agent(agent_name: str, repo_root: Path | None = None) -> Any:
    """Load a specific agent by name."""
    agent_dir = get_agent_dir(repo_root)
    agent_path = agent_dir / agent_name

    if not agent_path.exists():
        raise ValueError(f"Agent '{agent_name}' not found at {agent_path}")

    src_path = agent_path / "src"
    if src_path.exists() and str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    import importlib
    module = importlib.import_module(agent_name)

    agent_class_name = agent_name.capitalize()
    if hasattr(module, agent_class_name):
        return getattr(module, agent_class_name)()
    return module


def load_all_agents(repo_root: Path | None = None) -> dict[str, Any]:
    """Load all available agents."""
    agent_dir = get_agent_dir(repo_root)
    agents = {}

    excluded = {"__pycache__", ".git", ".github", "node_modules", ".env"}

    for item in agent_dir.iterdir():
        if (
            item.is_dir()
            and item.name not in excluded
            and not item.name.startswith(".")
            and ((item / "src").exists() or (item / "pyproject.toml").exists())
        ):
            try:
                agents[item.name] = load_agent(item.name, repo_root)
            except (ImportError, ValueError) as e:
                print(f"Warning: Could not load agent '{item.name}': {e}")

    return agents


def create_session(agent_name: str | None = None, repo_root: Path | None = None) -> dict[str, Any]:
    """Create a new session, optionally loading a specific agent."""
    session = {"agents": {}, "active_agent": None}

    if agent_name:
        session["agents"][agent_name] = load_agent(agent_name, repo_root)
        session["active_agent"] = agent_name
    else:
        try:
            valeri = load_agent("valeri", repo_root)
            session["agents"]["valeri"] = valeri
            session["active_agent"] = "valeri"
            loaded = valeri.load_agents()
            for name in loaded:
                session["agents"][name] = valeri.get_agent(name)
        except (ImportError, ValueError):
            session["agents"] = load_all_agents(repo_root)
            if session["agents"]:
                session["active_agent"] = next(iter(session["agents"].keys()))

    return session


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Agent Session Loader")
    parser.add_argument("agent", nargs="?", help="Agent name to load (default: valeri)")
    parser.add_argument("--list", "-l", action="store_true", help="List all agents")
    parser.add_argument("--repo", "-r", type=Path, help="Repository root path")

    args = parser.parse_args()
    agent_dir = get_agent_dir(args.repo)

    if args.list:
        print("Available agents:")
        excluded = {"__pycache__", ".git", ".github", "node_modules"}
        for item in sorted(agent_dir.iterdir()):
            if item.is_dir() and item.name not in excluded and not item.name.startswith("."):
                has_src = (item / "src").exists()
                has_readme = (item / "README.md").exists()
                has_voice = (item / "voice.md").exists()
                status = "✓" if has_src and has_readme else "✗"
                voice = " [voice]" if has_voice else ""
                print(f"  {status} {item.name}{voice}")
        return

    agent_name = args.agent or "valeri"
    session = create_session(agent_name, args.repo)

    print(f"Session created with agent: {session['active_agent']}")
    print(f"Loaded agents: {list(session['agents'].keys())}")


if __name__ == "__main__":
    main()