"""Tests for Ferracho analyzer core."""

import pytest

from ferracho.core import Ferracho
from ferracho.exceptions import AnalysisError, FunnelError, RiskError, SwotError, UnitEconomicsError


@pytest.fixture
def agent() -> Ferracho:
    """Provide fresh Ferracho instance."""
    return Ferracho()


def test_swot_ok(agent: Ferracho) -> None:
    """Valid SWOT returns counts and verdict."""
    result = agent.swot_analysis({
        "strengths": ["brand", "team"],
        "weaknesses": ["budget"],
        "opportunities": ["market"],
        "threats": [],
    })
    assert result["counts"]["strengths"] == 2
    assert result["total"] == 4
    assert result["balance"] == 2
    assert result["verdict"] == "expansion"


def test_swot_empty(agent: Ferracho) -> None:
    """Empty SWOT raises SwotError."""
    with pytest.raises(SwotError):
        agent.swot_analysis({"strengths": [], "weaknesses": [], "opportunities": [], "threats": []})


def test_swot_bad_type(agent: Ferracho) -> None:
    """Non-list quadrant raises SwotError."""
    with pytest.raises(SwotError):
        agent.swot_analysis({"strengths": "brand"})  # type: ignore[dict-item]


def test_funnel_ok(agent: Ferracho) -> None:
    """Funnel computes conversions and bottleneck."""
    result = agent.funnel_analysis({"visit": 1000, "lead": 200, "deal": 50})
    assert result["total_conversion_pct"] == pytest.approx(5.0)
    assert len(result["steps"]) == 2
    assert "bottleneck" in result
    assert result["bottleneck"] == "visit -> lead"


def test_funnel_first_zero(agent: Ferracho) -> None:
    """Zero first stage raises FunnelError."""
    with pytest.raises(FunnelError):
        agent.funnel_analysis({"visit": 0, "lead": 10})


def test_funnel_too_short(agent: Ferracho) -> None:
    """Single stage raises FunnelError."""
    with pytest.raises(FunnelError):
        agent.funnel_analysis({"visit": 100})


def test_unit_ok(agent: Ferracho) -> None:
    """Unit economics math is correct."""
    result = agent.unit_economics(1000, 400, 200, 100)
    assert result["margin"] == pytest.approx(600)
    assert result["profit_per_unit"] == pytest.approx(400)
    assert result["monthly_profit"] == pytest.approx(40000)
    assert result["romi_pct"] == pytest.approx(200)


def test_unit_negative(agent: Ferracho) -> None:
    """Negative price raises UnitEconomicsError."""
    with pytest.raises(UnitEconomicsError):
        agent.unit_economics(-10, 5, 5, 10)


def test_risk_sorted(agent: Ferracho) -> None:
    """Risks sorted highest first with levels."""
    result = agent.risk_matrix([
        {"title": "low risk", "probability": 1, "impact": 1},
        {"title": "big risk", "probability": 5, "impact": 5},
    ])
    assert result[0]["title"] == "big risk"
    assert result[0]["level"] == "critical"
    assert result[1]["level"] == "low"


def test_risk_bad_scale(agent: Ferracho) -> None:
    """Out of range probability raises RiskError."""
    with pytest.raises(RiskError):
        agent.risk_matrix([{"title": "x", "probability": 9, "impact": 2}])


def test_audit_ok(agent: Ferracho) -> None:
    """Audit report contains business name and conclusion."""
    text = agent.audit_report("Coffee", "Small coffee shop", {"strengths": ["taste"], "weaknesses": [], "opportunities": [], "threats": []})
    assert "Coffee" in text
    assert "Вывод" in text


def test_audit_funnel(agent: Ferracho) -> None:
    """Audit with funnel shows conversion."""
    text = agent.audit_report("Shop", "Retail point", None, {"visit": 1000, "deal": 50})
    assert "конверсия" in text
    assert "Узкое место" in text


def test_audit_empty_name(agent: Ferracho) -> None:
    """Empty business name raises AnalysisError."""
    with pytest.raises(AnalysisError):
        agent.audit_report("", "desc")


def test_history_recorded(agent: Ferracho) -> None:
    """Audits stored in history."""
    agent.audit_report("Shop", "Retail point")
    hist = agent.get_history()
    assert len(hist) == 1
    assert hist[0]["business"] == "Shop"
