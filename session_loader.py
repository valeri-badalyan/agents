"""Session loader — Main entry point for agent system."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

EXCLUDED = {"v3", "valeri", "agent", "projects", "__pycache__", ".git", ".github", "node_modules", ".env"}


def find_repo_root() -> Path:
    """Find the repository root directory."""
    current = Path(__file__).parent
    while current != current.parent:
        if (current / ".git").exists() or (current / "agent").exists() or (current / "v3").exists():
            return current
        current = current.parent
    return Path.cwd()


def get_agent_dirs(repo_root: Path | None = None) -> list[Path]:
    """Get the folders that hold agents: agent/ first, then the repo root."""
    root = repo_root or find_repo_root()
    agent_dir = root / "agent"
    return [agent_dir, root] if agent_dir.exists() else [root]


def find_agent_path(agent_name: str, repo_root: Path | None = None) -> Path | None:
    """Find an agent folder by name, preferring agent/ over the repo root."""
    for agent_dir in get_agent_dirs(repo_root):
        path = agent_dir / agent_name
        if path.is_dir():
            return path
    return None


def iter_agent_folders(repo_root: Path | None = None) -> list[Path]:
    """List agent folders across all agent dirs, without duplicates."""
    found: dict[str, Path] = {}
    for agent_dir in get_agent_dirs(repo_root):
        for item in agent_dir.iterdir():
            if (
                item.is_dir()
                and item.name not in EXCLUDED
                and not item.name.startswith(".")
                and item.name not in found
            ):
                found[item.name] = item
    return [found[name] for name in sorted(found)]


def is_prompt_agent(agent_path: Path) -> bool:
    """Check if agent is a prompt-based agent (no src/ folder)."""
    return not (agent_path / "src").exists()


def load_prompt_agent(agent_path: Path) -> dict[str, Any]:
    """Load a prompt-based agent."""
    agent_data = {
        "type": "prompt",
        "name": agent_path.name,
        "path": str(agent_path),
        "files": {},
    }

    for md_file in agent_path.glob("*.md"):
        agent_data["files"][md_file.stem] = md_file.read_text(encoding="utf-8")

    return agent_data


AGENT_MODULE_MAP = {
    "omar-hayam": "omar",
}


def load_agent(agent_name: str, repo_root: Path | None = None) -> Any:
    """Load a specific agent by name."""
    agent_path = find_agent_path(agent_name, repo_root)

    if agent_path is None:
        raise ValueError(f"Agent '{agent_name}' not found in {get_agent_dirs(repo_root)}")

    if is_prompt_agent(agent_path):
        return load_prompt_agent(agent_path)

    src_path = agent_path / "src"
    if src_path.exists() and str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    import importlib
    module_name = AGENT_MODULE_MAP.get(agent_name, agent_name)
    module = importlib.import_module(module_name)

    agent_class_name = module_name.capitalize()
    if hasattr(module, agent_class_name):
        return getattr(module, agent_class_name)()
    return module


def load_all_agents(repo_root: Path | None = None) -> dict[str, Any]:
    """Load all available agents."""
    agents = {}

    for item in iter_agent_folders(repo_root):
        if (item / "src").exists() or (item / "README.md").exists():
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
        return session

    # Default: V3 orchestrator, then legacy Valeri, then every agent directly.
    for orchestrator_name in ("v3", "valeri"):
        try:
            orchestrator = load_agent(orchestrator_name, repo_root)
            session["agents"][orchestrator_name] = orchestrator
            session["active_agent"] = orchestrator_name
            for name in orchestrator.load_agents():
                session["agents"][name] = orchestrator.get_agent(name)
            return session
        except (ImportError, ValueError):
            session = {"agents": {}, "active_agent": None}

    session["agents"] = load_all_agents(repo_root)
    if session["agents"]:
        session["active_agent"] = next(iter(session["agents"].keys()))

    return session


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Agent Session Loader")
    parser.add_argument("agent", nargs="?", help="Agent name to load (default: v3)")
    parser.add_argument("--list", "-l", action="store_true", help="List all agents")
    parser.add_argument("--repo", "-r", type=Path, help="Repository root path")

    args = parser.parse_args()

    if args.list:
        print("Available agents:")
        for item in iter_agent_folders(args.repo):
            has_src = (item / "src").exists()
            has_readme = (item / "README.md").exists()
            is_prompt = not has_src
            has_voice = (item / "voice.md").exists()
            status = "[OK]" if has_readme else "[--]"
            agent_type = "[prompt]" if is_prompt else "[python]"
            voice = " [voice]" if has_voice else ""
            print(f"  {status} {item.name} {agent_type}{voice}")
        return

    session = create_session(args.agent or "v3", args.repo)

    agent = session["agents"].get(session["active_agent"])
    if isinstance(agent, dict) and agent.get("type") == "prompt":
        print(f"Loaded prompt agent: {session['active_agent']}")
        print(f"Files: {list(agent['files'].keys())}")
    else:
        print(f"Session created with agent: {session['active_agent']}")
        print(f"Loaded agents: {list(session['agents'].keys())}")


if __name__ == "__main__":
    main()
