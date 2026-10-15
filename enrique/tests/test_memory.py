"""Tests for Enrique versioned memory — isolated, no external calls."""

from __future__ import annotations

import json

import pytest

from enrique.exceptions import ValidationError
from enrique.memory import MemoryStore


def test_memory_roundtrip(tmp_path) -> None:
    """Facts and history persist across reloads."""
    p = tmp_path / "mem.json"
    m = MemoryStore(path=p)
    m.add_fact("my name is Valeri", lang="en")
    m.add_exchange("barev", "hello!", lang="hy")
    m2 = MemoryStore(path=p)
    assert any("Valeri" in f["text"] for f in m2.get_facts())
    assert len(m2.get_history()) == 1


def test_memory_version_present(tmp_path) -> None:
    """Saved file contains version field."""
    p = tmp_path / "mem.json"
    m = MemoryStore(path=p)
    m.save()
    raw = json.loads(p.read_text(encoding="utf-8"))
    assert raw["version"] == 1


def test_memory_duplicate_fact(tmp_path) -> None:
    """Duplicate facts are not stored twice."""
    m = MemoryStore(path=tmp_path / "mem.json")
    assert m.add_fact("same fact", lang="en") is True
    assert m.add_fact("Same Fact", lang="en") is False


def test_memory_patterns(tmp_path) -> None:
    """Patterns track top words and turns."""
    m = MemoryStore(path=tmp_path / "mem.json")
    m.add_exchange("I love Armenian coffee and coffee", "yum!", lang="en")
    pats = m.get_patterns()
    assert pats["total_turns"] >= 1
    assert "coffee" in pats.get("top_words", {})


def test_memory_empty_fact_raises(tmp_path) -> None:
    """Empty fact raises ValidationError."""
    m = MemoryStore(path=tmp_path / "mem.json")
    with pytest.raises(ValidationError):
        m.add_fact("   ")


def test_memory_clear(tmp_path) -> None:
    """Clear wipes history and facts."""
    m = MemoryStore(path=tmp_path / "mem.json")
    m.add_fact("something", lang="en")
    m.clear()
    assert m.get_facts() == []
    assert m.get_history(limit=10) == []
