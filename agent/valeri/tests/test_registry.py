from pathlib import Path

from valeri.registry import AgentRegistry


def test_registry_discover_agents(tmp_path: Path):
    agent_dir = tmp_path / "jouli"
    agent_dir.mkdir()
    (agent_dir / "src").mkdir()
    (agent_dir / "README.md").touch()
    (agent_dir / "pyproject.toml").touch()

    registry = AgentRegistry(tmp_path)
    agents = registry.discover_agents()

    assert "jouli" in agents


def test_registry_get_agent_path(tmp_path: Path):
    agent_dir = tmp_path / "jouli"
    agent_dir.mkdir()

    registry = AgentRegistry(tmp_path)
    path = registry.get_agent_path("jouli")

    assert path == agent_dir


def test_registry_get_agent_path_not_found(tmp_path: Path):
    registry = AgentRegistry(tmp_path)
    path = registry.get_agent_path("nonexistent")

    assert path is None


def test_registry_is_agent_valid(tmp_path: Path):
    agent_dir = tmp_path / "jouli"
    agent_dir.mkdir()
    (agent_dir / "src").mkdir()
    (agent_dir / "README.md").touch()
    (agent_dir / "pyproject.toml").touch()

    registry = AgentRegistry(tmp_path)
    assert registry.is_agent_valid("jouli") is True


def test_registry_is_agent_invalid(tmp_path: Path):
    agent_dir = tmp_path / "jouli"
    agent_dir.mkdir()

    registry = AgentRegistry(tmp_path)
    assert registry.is_agent_valid("jouli") is False