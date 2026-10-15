"""Tests for V3 AgentRegistry."""

from pathlib import Path

from v3.registry import AgentRegistry


def test_registry_discover_agents(tmp_path: Path) -> None:
    """Discovery finds valid agent folders."""
    agent_dir = tmp_path / "jouli"
    agent_dir.mkdir()
    (agent_dir / "src").mkdir()
    (agent_dir / "README.md").touch()
    (agent_dir / "pyproject.toml").touch()

    registry = AgentRegistry(tmp_path)
    agents = registry.discover_agents()

    assert "jouli" in agents


def test_registry_excludes_orchestrators(tmp_path: Path) -> None:
    """V3 and Valeri are excluded from discovery."""
    for name in ("v3", "valeri", "jouli"):
        d = tmp_path / name
        d.mkdir()
        (d / "src").mkdir()

    registry = AgentRegistry(tmp_path)
    agents = registry.discover_agents()

    assert "v3" not in agents
    assert "valeri" not in agents
    assert "jouli" in agents


def test_registry_get_agent_path(tmp_path: Path) -> None:
    """Existing agent path is returned."""
    agent_dir = tmp_path / "jouli"
    agent_dir.mkdir()

    registry = AgentRegistry(tmp_path)
    path = registry.get_agent_path("jouli")

    assert path == agent_dir


def test_registry_get_agent_path_not_found(tmp_path: Path) -> None:
    """Missing agent returns None."""
    registry = AgentRegistry(tmp_path)
    path = registry.get_agent_path("nonexistent")

    assert path is None


def test_registry_get_agent_path_invalid_input(tmp_path: Path) -> None:
    """Empty agent name returns None."""
    registry = AgentRegistry(tmp_path)

    assert registry.get_agent_path("") is None


def test_registry_is_agent_valid(tmp_path: Path) -> None:
    """Full structure counts as valid."""
    agent_dir = tmp_path / "jouli"
    agent_dir.mkdir()
    (agent_dir / "src").mkdir()
    (agent_dir / "README.md").touch()
    (agent_dir / "pyproject.toml").touch()

    registry = AgentRegistry(tmp_path)
    assert registry.is_agent_valid("jouli") is True


def test_registry_is_agent_invalid(tmp_path: Path) -> None:
    """Incomplete structure counts as invalid."""
    agent_dir = tmp_path / "jouli"
    agent_dir.mkdir()

    registry = AgentRegistry(tmp_path)
    assert registry.is_agent_valid("jouli") is False
