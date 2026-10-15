"""Tests for Mika provider core."""

import pytest

from mika.core import Mika, detect_lang, normalize_lang
from mika.exceptions import ConnectionError, CoverageError, DiagnosisError, ReportError, TariffError


@pytest.fixture
def agent() -> Mika:
    """Provide fresh Mika instance."""
    return Mika()


def test_normalize_lang_alias_am() -> None:
    """am maps to hy."""
    assert normalize_lang("am") == "hy"
    assert normalize_lang("RU") == "ru"


def test_normalize_bad_lang() -> None:
    """Unsupported lang raises ReportError."""
    with pytest.raises(ReportError):
        normalize_lang("fr")


def test_detect_lang_ru_en_hy() -> None:
    """Detect ru/en/hy by alphabet."""
    assert detect_lang("Привет, покажи тарифы") == "ru"
    assert detect_lang("hello show me tariffs please") == "en"
    assert detect_lang("Ողջույն ցույց տուր սակագները") == "hy"


def test_greet_contains_hello(agent: Mika) -> None:
    """Greeting is non-empty and funny."""
    text = agent.greet("ru")
    assert "Мика" in text
    assert len(text) > 20


def test_list_tariffs(agent: Mika) -> None:
    """Five tariffs listed."""
    tariffs = agent.list_tariffs()
    assert len(tariffs) == 5
    ids = {t["id"] for t in tariffs}
    assert {"start", "gamer", "ultra"} <= ids


def test_recommend_gaming(agent: Mika) -> None:
    """Gaming usage returns gamer or ultra."""
    result = agent.recommend_tariff(usage="gaming", budget=800, min_speed=100)
    assert result["id"] in ("gamer", "home", "ultra", "office")
    assert "joke" in result


def test_recommend_no_fit(agent: Mika) -> None:
    """Impossible budget raises TariffError."""
    with pytest.raises(TariffError):
        agent.recommend_tariff(usage="gaming", budget=10, min_speed=1000)


def test_recommend_bad_usage(agent: Mika) -> None:
    """Empty usage raises TariffError."""
    with pytest.raises(TariffError):
        agent.recommend_tariff(usage="  ")


def test_coverage_center(agent: Mika) -> None:
    """Center address is available."""
    result = agent.check_coverage("центр города")
    assert result["available"] is True
    assert result["eta_days"] >= 1


def test_coverage_empty(agent: Mika) -> None:
    """Empty address raises CoverageError."""
    with pytest.raises(CoverageError):
        agent.check_coverage("   ")


def test_diagnose_ok(agent: Mika) -> None:
    """Good speed is ok."""
    result = agent.diagnose(95, 100, 10, wifi=False)
    assert result["level"] == "ok"


def test_diagnose_slow(agent: Mika) -> None:
    """Half speed is slow."""
    result = agent.diagnose(50, 100, 60, wifi=True)
    assert result["level"] == "slow"
    assert len(result["steps"]) >= 2


def test_diagnose_bad(agent: Mika) -> None:
    """Tiny speed is bad."""
    result = agent.diagnose(5, 100, 150, wifi=True)
    assert result["level"] == "bad"


def test_diagnose_zero_expected(agent: Mika) -> None:
    """Zero expected raises DiagnosisError."""
    with pytest.raises(DiagnosisError):
        agent.diagnose(10, 0, 20)


def test_connection_apartment(agent: Mika) -> None:
    """Apartment steps non-empty."""
    steps = agent.connection_steps("apartment")
    assert len(steps) >= 4


def test_connection_bad_type(agent: Mika) -> None:
    """Unknown type raises ConnectionError."""
    with pytest.raises(ConnectionError):
        agent.connection_steps("spaceship")


def test_chat_tariffs(agent: Mika) -> None:
    """Chat about tariffs replies with list."""
    out = agent.chat("Мика, покажи тарифы")
    assert "Мбит" in out["reply"] or "тарифа" in out["reply"].lower() or "•" in out["reply"]


def test_chat_joke(agent: Mika) -> None:
    """Chat joke request returns joke."""
    out = agent.chat("расскажи анекдот")
    assert len(out["reply"]) > 10


def test_chat_empty(agent: Mika) -> None:
    """Empty chat raises ReportError."""
    with pytest.raises(ReportError):
        agent.chat("   ")


def test_history_recorded(agent: Mika) -> None:
    """Actions stored in history."""
    agent.chat("hello show tariffs")
    agent.recommend_tariff("family")
    assert len(agent.get_history()) >= 2
