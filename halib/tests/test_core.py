"""Tests for Halib designer core."""

import pytest

from halib.core import Halib
from halib.exceptions import AuditError, ConceptError, LayoutError, PaletteError, TypographyError


@pytest.fixture
def agent() -> Halib:
    """Provide fresh Halib instance."""
    return Halib()


def test_concept_ok(agent: Halib) -> None:
    """Valid concept returns project, style and sections."""
    result = agent.concept("Coffee", "minimal", "calm")
    assert result["project"] == "Coffee"
    assert result["style"] == "minimal"
    assert result["mood"] == "calm"
    assert len(result["sections"]) > 0
    assert len(result["principles"]) == 4


def test_concept_bad_style(agent: Halib) -> None:
    """Unknown style raises ConceptError."""
    with pytest.raises(ConceptError):
        agent.concept("Coffee", "unknown-style", "calm")


def test_concept_bad_mood(agent: Halib) -> None:
    """Unknown mood raises ConceptError."""
    with pytest.raises(ConceptError):
        agent.concept("Coffee", "minimal", "unknown")


def test_concept_empty(agent: Halib) -> None:
    """Empty project raises ConceptError."""
    with pytest.raises(ConceptError):
        agent.concept("   ")


def test_palette_ok(agent: Halib) -> None:
    """Palette returns requested color count with roles."""
    result = agent.palette("Coffee", "premium", 5)
    assert result["brand"] == "Coffee"
    assert len(result["colors"]) == 5
    assert all(c["hex"].startswith("#") for c in result["colors"])


def test_palette_deterministic(agent: Halib) -> None:
    """Same brand gives same palette."""
    first = agent.palette("Coffee", "calm")
    second = agent.palette("Coffee", "calm")
    assert first == second


def test_palette_bad_count(agent: Halib) -> None:
    """Invalid count raises PaletteError."""
    with pytest.raises(PaletteError):
        agent.palette("Coffee", "calm", 10)


def test_palette_bad_mood(agent: Halib) -> None:
    """Unknown mood raises PaletteError."""
    with pytest.raises(PaletteError):
        agent.palette("Coffee", "unknown")


def test_typography_ok(agent: Halib) -> None:
    """Typography returns font pairing."""
    result = agent.typography("Coffee", "luxury")
    assert result["heading"] == "Playfair Display"
    assert result["body"]
    assert result["scale"]["h1"] == 48


def test_typography_bad_style(agent: Halib) -> None:
    """Unknown style raises TypographyError."""
    with pytest.raises(TypographyError):
        agent.typography("Coffee", "unknown")


def test_layout_preset(agent: Halib) -> None:
    """Preset page returns blocks."""
    result = agent.layout("landing")
    assert result["page"] == "landing"
    assert "hero" in result["blocks"]
    assert "cta" in result["blocks"]


def test_layout_custom(agent: Halib) -> None:
    """Custom sections override preset."""
    result = agent.layout("landing", ["hero", "cta"])
    assert result["blocks"] == ["hero", "cta"]


def test_layout_bad_page(agent: Halib) -> None:
    """Unknown page raises LayoutError."""
    with pytest.raises(LayoutError):
        agent.layout("unknown-page")


def test_logo_brief(agent: Halib) -> None:
    """Logo brief contains business name."""
    text = agent.logo_brief("Coffee")
    assert "Coffee" in text
    assert "SVG" in text


def test_style_guide(agent: Halib) -> None:
    """Style guide contains brand and palette."""
    text = agent.style_guide("Coffee", "minimal", "calm")
    assert "Coffee" in text
    assert "Палитра" in text
    assert "Шрифты" in text


def test_audit_ok(agent: Halib) -> None:
    """Audit returns score and next step."""
    text = agent.audit_design("Лендинг кофейни, hero с фото, есть кнопка заказать")
    assert "Халиб" in text
    assert "/10" in text
    assert "Следующий шаг" in text


def test_audit_empty(agent: Halib) -> None:
    """Empty description raises AuditError."""
    with pytest.raises(AuditError):
        agent.audit_design("   ")


def test_history_recorded(agent: Halib) -> None:
    """Concepts and audits stored in history."""
    agent.concept("Coffee")
    agent.audit_design("Лендинг с кнопкой и нормальным hero экраном для теста")
    hist = agent.get_history()
    assert len(hist) == 2
    assert hist[0]["type"] == "concept"
