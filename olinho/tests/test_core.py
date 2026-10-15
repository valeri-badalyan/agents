"""Tests for Olinho agent."""

from __future__ import annotations

import pytest

from olinho.core import Olinho, slugify
from olinho.exceptions import BuildError, IdeaError


@pytest.fixture()
def agent(tmp_path):  # type: ignore[no-untyped-def]
    """Olinho with isolated projects dir."""
    return Olinho(projects_dir=tmp_path)


def test_slugify_basic() -> None:
    """Slug is filesystem-safe."""
    assert slugify("Кофейня на углу") == "kofeynya-na-uglu"
    assert slugify("  Hello World!! ") == "hello-world"
    assert slugify("") == "olinho-project"


def test_classify_game(agent: Olinho) -> None:
    """Game keywords detected."""
    res = agent.classify("сделай игру кликер про космос")
    assert res["type"] == "game"


def test_classify_shop(agent: Olinho) -> None:
    """Shop keywords detected."""
    res = agent.classify("магазин товаров для котов")
    assert res["type"] == "shop"


def test_classify_empty_raises(agent: Olinho) -> None:
    """Empty idea raises."""
    with pytest.raises(IdeaError):
        agent.classify("   ")


def test_build_creates_files(agent: Olinho, tmp_path) -> None:  # type: ignore[no-untyped-def]
    """Build scaffolds index.html, css, js."""
    res = agent.build("лендинг кофейни", name="coffee")
    assert res["type"] == "landing"
    path = tmp_path / "coffee"
    assert (path / "index.html").exists()
    assert (path / "styles.css").exists()
    assert (path / "app.js").exists()
    assert str(res["preview_url"]).startswith("file://")


def test_build_empty_raises(agent: Olinho) -> None:
    """Empty build raises BuildError."""
    with pytest.raises(BuildError):
        agent.build("   ")


def test_ship_packs_zip(agent: Olinho, tmp_path) -> None:  # type: ignore[no-untyped-def]
    """Ship builds + zips."""
    res = agent.ship("портфолио фотографа", name="photo", open_browser=False)
    assert "zip" in res
    assert str(res["zip"]).endswith(".zip")


def test_preview_missing_raises(agent: Olinho) -> None:
    """Preview missing path raises."""
    from olinho.exceptions import PreviewError

    with pytest.raises(PreviewError):
        agent.preview("/nonexistent/path-xyz")
