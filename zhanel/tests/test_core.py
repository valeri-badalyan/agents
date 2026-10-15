"""Tests for Zhanel core logic."""

import pytest

from zhanel.core import Zhanel
from zhanel.exceptions import AuditError, ContentPlanError, CopyError, StrategyError


@pytest.fixture
def agent() -> Zhanel:
    """Provide fresh Zhanel instance."""
    return Zhanel()


def test_audience_ok(agent: Zhanel) -> None:
    """Audience returns 3 segments."""
    result = agent.analyze_audience("фитнес-приложение")
    assert result["product"] == "фитнес-приложение"
    segments = result["segments"]
    assert isinstance(segments, list)
    assert len(segments) == 3


def test_audience_empty(agent: Zhanel) -> None:
    """Empty product raises StrategyError."""
    with pytest.raises(StrategyError):
        agent.analyze_audience("  ")


def test_positioning_ok(agent: Zhanel) -> None:
    """Positioning contains product and audience."""
    result = agent.positioning("кофейня", "студенты", "вкусный кофе")
    assert "кофейня" in result["usp"]
    assert "студенты" in result["usp"]
    assert "logic" in result


def test_ad_copy_all(agent: Zhanel) -> None:
    """All angles return 3 variants."""
    result = agent.ad_copy("фитнес-приложение", "all")
    variants = result["variants"]
    assert isinstance(variants, dict)
    assert set(variants.keys()) == {"pain", "benefit", "provocative"}


def test_ad_copy_single(agent: Zhanel) -> None:
    """Single angle returns one variant."""
    result = agent.ad_copy("курс", "pain")
    assert list(result["variants"].keys()) == ["pain"]  # type: ignore[attr-defined]


def test_ad_copy_bad_angle(agent: Zhanel) -> None:
    """Unknown angle raises CopyError."""
    with pytest.raises(CopyError):
        agent.ad_copy("курс", "nasa")


def test_slogan_deterministic(agent: Zhanel) -> None:
    """Same seed gives same slogans."""
    s1 = agent.slogan("кофейня", seed=42)
    s2 = agent.slogan("кофейня", seed=42)
    assert s1["slogans"] == s2["slogans"]
    assert len(s1["slogans"]) == 5  # type: ignore[arg-type]


def test_naming_ok(agent: Zhanel) -> None:
    """Naming returns 7 options + check."""
    result = agent.naming("кофейня третье место", seed=1)
    assert len(result["names"]) == 7  # type: ignore[arg-type]
    assert "check" in result


def test_content_plan_weeks(agent: Zhanel) -> None:
    """4 weeks = 16 posts (4 per week)."""
    result = agent.content_plan("бьюти-бренд", weeks=2)
    assert len(result["plan"]) == 8  # type: ignore[arg-type]
    assert "rubrics" in result


def test_content_plan_bad_weeks(agent: Zhanel) -> None:
    """Invalid weeks raises ContentPlanError."""
    with pytest.raises(ContentPlanError):
        agent.content_plan("бренд", weeks=99)


def test_launch_ok(agent: Zhanel) -> None:
    """Launch returns steps."""
    result = agent.launch_checklist("онлайн-курс")
    assert len(result["steps"]) >= 5  # type: ignore[arg-type]


def test_kpi_sales(agent: Zhanel) -> None:
    """Sales KPI contains CAC."""
    result = agent.kpi("sales")
    assert "CAC" in result["metrics"]  # type: ignore[operator]


def test_kpi_bad_goal(agent: Zhanel) -> None:
    """Unknown goal raises StrategyError."""
    with pytest.raises(StrategyError):
        agent.kpi("nasa")


def test_audit_weak(agent: Zhanel) -> None:
    """Weak idea gets honest verdict."""
    result = agent.audit_idea("запустим вирусный ролик для всех с гарантией")
    assert "не сработает" in result["verdict"]


def test_audit_short(agent: Zhanel) -> None:
    """Too short idea flagged as raw."""
    result = agent.audit_idea("сделай рекламу")
    assert "сырая" in result["verdict"]


def test_audit_empty(agent: Zhanel) -> None:
    """Empty idea raises AuditError."""
    with pytest.raises(AuditError):
        agent.audit_idea("  ")
