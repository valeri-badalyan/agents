from pathlib import Path

from valeri.registry import AgentRegistry
from valeri.router import Router


def test_router_route_task(tmp_path: Path):
    agent_dir = tmp_path / "jouli"
    agent_dir.mkdir()
    (agent_dir / "src").mkdir()

    registry = AgentRegistry(tmp_path)
    registry.discover_agents()
    router = Router(registry)

    agent = router.route_task("Translate hello to Spanish")
    assert agent == "jouli"


def test_router_route_task_detect(tmp_path: Path):
    agent_dir = tmp_path / "jouli"
    agent_dir.mkdir()
    (agent_dir / "src").mkdir()

    registry = AgentRegistry(tmp_path)
    registry.discover_agents()
    router = Router(registry)

    agent = router.route_task("Detect the language of this text")
    assert agent == "jouli"


def test_router_add_rule(tmp_path: Path):
    registry = AgentRegistry(tmp_path)
    router = Router(registry)

    router.add_rule("summarize|summary", ["summarizer"])
    rules = router.get_rules()
    assert "summarize|summary" in rules


def test_router_remove_rule(tmp_path: Path):
    registry = AgentRegistry(tmp_path)
    router = Router(registry)

    router.add_rule("test", ["agent"])
    router.remove_rule("test")
    rules = router.get_rules()
    assert "test" not in rules