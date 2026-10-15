"""Tests for Marika statistics core."""

import pytest

from marika.core import Marika
from marika.exceptions import GrowthError, ReportError, SharesError, StatisticsError, TrendError


@pytest.fixture
def agent() -> Marika:
    """Provide fresh Marika instance."""
    return Marika()


def test_describe_ok(agent: Marika) -> None:
    """Valid data returns full stats."""
    result = agent.describe([1, 2, 3, 4])
    assert result["count"] == 4
    assert result["sum"] == 10
    assert result["mean"] == pytest.approx(2.5)
    assert result["median"] == pytest.approx(2.5)
    assert result["min"] == 1
    assert result["max"] == 4
    assert "stdev" in result


def test_describe_single(agent: Marika) -> None:
    """Single value has zero variance."""
    result = agent.describe([5])
    assert result["count"] == 1
    assert result["mean"] == pytest.approx(5.0)
    assert result["stdev"] == pytest.approx(0.0)


def test_describe_empty(agent: Marika) -> None:
    """Empty list raises StatisticsError."""
    with pytest.raises(StatisticsError):
        agent.describe([])


def test_describe_bad_type(agent: Marika) -> None:
    """Non-numeric input raises StatisticsError."""
    with pytest.raises(StatisticsError):
        agent.describe([1, "a", 3])  # type: ignore[list-item]


def test_growth_ok(agent: Marika) -> None:
    """100 -> 150 is +50%."""
    result = agent.growth_rate(100, 150)
    assert result["absolute_change"] == pytest.approx(50)
    assert result["percent_change"] == pytest.approx(50)


def test_growth_zero_base(agent: Marika) -> None:
    """Zero base raises GrowthError."""
    with pytest.raises(GrowthError):
        agent.growth_rate(0, 10)


def test_trend_up(agent: Marika) -> None:
    """Increasing series is up."""
    result = agent.trend([1, 2, 3, 4, 5])
    assert result["direction"] == "up"
    assert result["slope"] > 0


def test_trend_down(agent: Marika) -> None:
    """Decreasing series is down."""
    result = agent.trend([5, 4, 3, 2, 1])
    assert result["direction"] == "down"


def test_trend_flat(agent: Marika) -> None:
    """Constant series is flat."""
    result = agent.trend([3, 3, 3, 3])
    assert result["direction"] == "flat"


def test_trend_too_short(agent: Marika) -> None:
    """Single point raises TrendError."""
    with pytest.raises(TrendError):
        agent.trend([1])


def test_shares_ok(agent: Marika) -> None:
    """Shares sum to 100."""
    result = agent.shares({"a": 30, "b": 70})
    assert result["total"] == pytest.approx(100)
    assert result["breakdown"]["a"] == pytest.approx(30)
    assert result["breakdown"]["b"] == pytest.approx(70)


def test_shares_zero_total(agent: Marika) -> None:
    """Zero total raises SharesError."""
    with pytest.raises(SharesError):
        agent.shares({"a": 0, "b": 0})


def test_report_ru(agent: Marika) -> None:
    """Russian report contains key words."""
    text = agent.summary_report([1, 2, 3, 4], lang="ru")
    assert "Среднее" in text
    assert "Тренд" in text


def test_report_en(agent: Marika) -> None:
    """English report contains key words."""
    text = agent.summary_report([1, 2, 3, 4], lang="en")
    assert "Mean" in text
    assert "Trend" in text


def test_report_zh(agent: Marika) -> None:
    """Chinese report contains key words."""
    text = agent.summary_report([1, 2, 3, 4], lang="zh")
    assert "平均值" in text
    assert "趋势" in text


def test_report_bad_lang(agent: Marika) -> None:
    """Unsupported lang raises ReportError."""
    with pytest.raises(ReportError):
        agent.summary_report([1, 2, 3], lang="fr")


def test_history_recorded(agent: Marika) -> None:
    """Reports are stored in history."""
    agent.summary_report([1, 2, 3], lang="en", title="Test")
    hist = agent.get_history()
    assert len(hist) == 1
    assert hist[0]["lang"] == "en"
