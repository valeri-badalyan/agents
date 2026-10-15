"""Tests for Enrique core — mocked memory, no external calls."""

from __future__ import annotations

import pytest

from enrique.core import contains_trigger, detect_language, wants_joke, Enrique
from enrique.exceptions import ValidationError


def test_detect_language_ru() -> None:
    """Cyrillic text detected as Russian."""
    assert detect_language("Привет, как дела?") == "ru"


def test_detect_language_hy() -> None:
    """Armenian script detected as Armenian."""
    assert detect_language("Բարև, ինչպե՞ս ես") == "hy"


def test_detect_language_en() -> None:
    """Latin text defaults to English."""
    assert detect_language("Hello there") == "en"


def test_detect_language_empty_raises() -> None:
    """Empty text raises ValidationError."""
    with pytest.raises(ValidationError):
        detect_language("   ")


def test_contains_trigger() -> None:
    """Both spellings trigger SSOT load."""
    assert contains_trigger("hey enrique!") is True
    assert contains_trigger("ENRIKE привет") is True
    assert contains_trigger("hello world") is False


def test_wants_joke() -> None:
    """Joke intent detected in 3 languages."""
    assert wants_joke("tell me a joke") is True
    assert wants_joke("расскажи анекдот") is True
    assert wants_joke("կատակ արա") is True
    assert wants_joke("what time is it") is False


def test_chat_loads_ssot_on_trigger(tmp_path) -> None:
    """Mentioning enrike reloads SSOT and returns greeting."""
    mem = tmp_path / "m.json"
    eng = Enrique(memory_path=str(mem))
    out = eng.chat("enrike привет!")
    assert out["triggered_ssot"] is True
    assert out["lang"] == "ru"
    assert "Энрике" in out["reply"] or "SSOT" in out["reply"]


def test_chat_remembers_fact(tmp_path) -> None:
    """'remember' sentences are stored as facts."""
    mem = tmp_path / "m.json"
    eng = Enrique(memory_path=str(mem))
    out = eng.chat("remember my dog is called Rex")
    assert out["fact_saved"] is True
    assert any("Rex" in f["text"] for f in eng.memory.get_facts())


def test_chat_joke(tmp_path) -> None:
    """Joke request returns non-empty reply."""
    mem = tmp_path / "m.json"
    eng = Enrique(memory_path=str(mem))
    out = eng.chat("tell me a joke please")
    assert len(out["reply"]) > 0
    assert "reasoning" in out


def test_chat_empty_raises(tmp_path) -> None:
    """Empty chat raises ValidationError."""
    eng = Enrique(memory_path=str(tmp_path / "m.json"))
    with pytest.raises(ValidationError):
        eng.chat("   ")
