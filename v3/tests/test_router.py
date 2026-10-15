"""Tests for V3 Router (improved routing)."""

from pathlib import Path

import pytest

from v3.registry import AgentRegistry
from v3.router import Router


def _make_registry(tmp_path: Path, names: list[str]) -> AgentRegistry:
    for name in names:
        d = tmp_path / name
        d.mkdir(exist_ok=True)
        (d / "src").mkdir(exist_ok=True)
    registry = AgentRegistry(tmp_path)
    registry.discover_agents()
    return registry


def test_router_translation(tmp_path: Path) -> None:
    """Translation task routes to jouli."""
    registry = _make_registry(tmp_path, ["jouli"])
    router = Router(registry)

    assert router.route_task("Translate hello to Spanish") == "jouli"
    assert router.route_task("Переведи привет на испанский") == "jouli"


def test_router_explicit_triggers(tmp_path: Path) -> None:
    """Explicit name triggers route correctly."""
    registry = _make_registry(
        tmp_path,
        ["jouli", "zhanel", "marika", "ferracho", "halib", "aryubi", "olinho", "messi", "enrique"],
    )
    router = Router(registry)

    assert router.route_task("Жанель иди сюда, нужен запуск") == "zhanel"
    assert router.route_task("Олиньо!! сделай лендинг кофейни") == "olinho"
    assert router.route_task("марика, посчитай рост") == "marika"
    assert router.route_task("Феррачо!! сделай SWOT") == "ferracho"
    assert router.route_task("Халиб, нужна палитра") == "halib"
    assert router.route_task("Арюби, посчитай бюджет") == "aryubi"
    assert router.route_task("Анкара Месси, разбери тактику") == "messi"


def test_router_domain_keywords(tmp_path: Path) -> None:
    """Domain keywords route to specialists."""
    registry = _make_registry(
        tmp_path, ["leo-davinci", "omar-hayam", "zhanel", "marika", "halib", "aryubi"]
    )
    router = Router(registry)

    assert router.route_task("Create a 3D scene with render") == "leo-davinci"
    assert router.route_task("Напиши сюжет и персонажа") == "omar-hayam"
    assert router.route_task("Нужна маркетинг стратегия") == "zhanel"


def test_router_route_all_multi(tmp_path: Path) -> None:
    """route_all finds multiple agents."""
    registry = _make_registry(tmp_path, ["zhanel", "halib", "olinho"])
    router = Router(registry)

    matched = router.route_all("Сделай маркетинг и дизайн для лендинга")
    assert "zhanel" in matched
    assert "halib" in matched


def test_router_empty_task(tmp_path: Path) -> None:
    """Empty task raises ValueError."""
    registry = AgentRegistry(tmp_path)
    router = Router(registry)

    with pytest.raises(ValueError):
        router.route_task("   ")


def test_router_add_remove_rule(tmp_path: Path) -> None:
    """Rules can be added and removed."""
    registry = AgentRegistry(tmp_path)
    router = Router(registry)

    router.add_rule("summarize|summary", ["summarizer"])
    assert "summarize|summary" in router.get_rules()

    router.remove_rule("summarize|summary")
    assert "summarize|summary" not in router.get_rules()


def test_router_add_invalid_rule(tmp_path: Path) -> None:
    """Invalid regex raises ValueError."""
    registry = AgentRegistry(tmp_path)
    router = Router(registry)

    with pytest.raises(ValueError):
        router.add_rule("[invalid", ["x"])
