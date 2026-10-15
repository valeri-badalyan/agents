"""Tests for Messi core logic."""

import pytest

from messi.core import Messi
from messi.exceptions import QuizError, TacticsError, TrainingError


@pytest.fixture
def agent() -> Messi:
    """Provide fresh Messi instance."""
    return Messi()


def test_analyze_formation_ok(agent: Messi) -> None:
    """Valid formation returns style and advice."""
    result = agent.analyze_formation("4-3-3")
    assert result["formation"] == "4-3-3"
    assert "style" in result
    assert "advice" in result


def test_analyze_formation_unknown(agent: Messi) -> None:
    """Unknown formation raises TacticsError."""
    with pytest.raises(TacticsError):
        agent.analyze_formation("1-1-1")


def test_analyze_formation_empty(agent: Messi) -> None:
    """Empty formation raises TacticsError."""
    with pytest.raises(TacticsError):
        agent.analyze_formation("  ")


def test_training_plan_ok(agent: Messi) -> None:
    """Training plan returns exercises list."""
    plan = agent.training_plan("beginner", "forward")
    assert plan["level"] == "beginner"
    assert isinstance(plan["exercises"], list)
    assert len(plan["exercises"]) >= 3


def test_training_plan_invalid_level(agent: Messi) -> None:
    """Invalid level raises TrainingError."""
    with pytest.raises(TrainingError):
        agent.training_plan("nasa", "forward")


def test_motivate_contains_name(agent: Messi) -> None:
    """Motivation includes player name."""
    text = agent.motivate("Лео")
    assert "Лео" in text
    assert len(text) > 10


def test_quiz_deterministic() -> None:
    """Same seed gives same question."""
    agent = Messi()
    q1 = agent.quiz_question(seed=42)
    q2 = agent.quiz_question(seed=42)
    assert q1["question"] == q2["question"]


def test_check_quiz_correct(agent: Messi) -> None:
    """Correct answer returns True."""
    assert agent.check_quiz_answer("Сколько игроков одной команды на поле?", "11") is True


def test_check_quiz_wrong(agent: Messi) -> None:
    """Wrong answer returns False."""
    assert agent.check_quiz_answer("Сколько игроков одной команды на поле?", "10") is False


def test_check_quiz_unknown(agent: Messi) -> None:
    """Unknown question raises QuizError."""
    with pytest.raises(QuizError):
        agent.check_quiz_answer("Кто выиграл ЧМ 3000?", "никто")
