"""Tests for Sandy music director core."""

import pytest

from sandy.core import Sandy, detect_lang, key_distance, parse_key
from sandy.exceptions import BriefError, MoodError, MusicKeyError, RehearsalError, SetlistError


@pytest.fixture
def agent() -> Sandy:
    """Provide fresh Sandy instance."""
    return Sandy()


def test_parse_key_variants() -> None:
    """Letter, Camelot and Russian notation parse to Camelot."""
    assert parse_key("Am") == "8A"
    assert parse_key("C") == "8B"
    assert parse_key("F#m") == "11A"
    assert parse_key("G#m") == "1A"
    assert parse_key("Bb major") == "6B"
    assert parse_key("8a") == "8A"
    assert parse_key("ля минор") == "8A"
    assert parse_key("фа-диез минор") == "11A"


def test_parse_key_bad() -> None:
    """Garbage key raises MusicKeyError."""
    with pytest.raises(MusicKeyError):
        parse_key("H-moll-ish")


def test_key_distance_wraps() -> None:
    """Distance wraps around the wheel."""
    assert key_distance("12A", "1A") == 1
    assert key_distance("8A", "8B") == 1
    assert key_distance("8A", "2A") == 6


def test_key_compatibility(agent: Sandy) -> None:
    """Relative keys are compatible, tritone is not."""
    assert agent.key_compatibility("Am", "C")["compatible"] is True
    assert agent.key_compatibility("C", "F#")["compatible"] is False


def test_detect_lang() -> None:
    """Detect ru/en."""
    assert detect_lang("музыка для сцены") == "ru"
    assert detect_lang("music for a sad scene") == "en"


def test_recommend_alias_and_clamp(agent: Sandy) -> None:
    """RU alias works and bpm is clamped into range."""
    rec = agent.recommend_music("грустно", bpm=200)
    assert rec["mood"] == "sad"
    assert rec["bpm"] == rec["bpm_range"][1]


def test_recommend_unknown(agent: Sandy) -> None:
    """Unknown mood raises MoodError."""
    with pytest.raises(MoodError):
        agent.recommend_music("квантовый")


SONGS = [
    {"title": "Ballad", "bpm": 70, "key": "Am", "energy": 2},
    {"title": "Groove", "bpm": 105, "key": "C", "energy": 5},
    {"title": "Banger", "bpm": 128, "key": "Em", "energy": 9},
    {"title": "Mid", "bpm": 95, "key": "G", "energy": 4},
]


def test_setlist_rise(agent: Sandy) -> None:
    """Rise arc orders by energy ascending."""
    out = agent.build_setlist(SONGS, "rise")
    assert out["setlist"] == ["Ballad", "Mid", "Groove", "Banger"]
    assert len(out["transitions"]) == 3


def test_setlist_chill_and_peak(agent: Sandy) -> None:
    """Chill goes down, peak puts max in the middle."""
    assert agent.build_setlist(SONGS, "chill")["setlist"][0] == "Banger"
    peak = agent.build_setlist(SONGS, "peak")["setlist"]
    assert peak[0] != "Banger" and peak[-1] != "Banger"


def test_setlist_flags_tempo_jump(agent: Sandy) -> None:
    """Large BPM jump is flagged."""
    out = agent.build_setlist(SONGS, "wave")
    assert any("скачок" in t["note"] for t in out["transitions"])


def test_setlist_invalid(agent: Sandy) -> None:
    """Bad input raises SetlistError."""
    with pytest.raises(SetlistError):
        agent.build_setlist([])
    with pytest.raises(SetlistError):
        agent.build_setlist([{"title": "X", "bpm": 500}])
    with pytest.raises(SetlistError):
        agent.build_setlist(SONGS, "zigzag")


def test_rehearsal_plan_fits(agent: Sandy) -> None:
    """Plan covers exactly the given minutes and every song."""
    plan = agent.rehearsal_plan(120, ["A", "B", "C"], band_size=5)
    assert sum(b["minutes"] for b in plan) == 120
    assert sum("«" in b["task"] for b in plan) == 3


def test_rehearsal_too_short(agent: Sandy) -> None:
    """Too many songs for the time raises RehearsalError."""
    with pytest.raises(RehearsalError):
        agent.rehearsal_plan(30, [f"S{i}" for i in range(10)])


def test_brief(agent: Sandy) -> None:
    """Brief contains each scene."""
    md = agent.soundtrack_brief("Промо", [{"name": "Интро", "mood": "epic"},
                                          {"name": "Финал", "mood": "happy"}])
    assert "# Музыкальный бриф: Промо" in md
    assert "Интро" in md and "Финал" in md and "BPM" in md


def test_brief_invalid(agent: Sandy) -> None:
    """Scene without mood raises BriefError."""
    with pytest.raises(BriefError):
        agent.soundtrack_brief("X", [{"name": "Only name"}])


def test_chat_intents(agent: Sandy) -> None:
    """Chat routes by intent."""
    assert agent.chat("Сэнди, музыка для грустной сцены, грустно")["intent"] == "recommend"
    assert agent.chat("собери сетлист")["intent"] == "setlist"
    assert agent.chat("plan a rehearsal")["intent"] == "rehearsal"
    with pytest.raises(BriefError):
        agent.chat("  ")


def test_history(agent: Sandy) -> None:
    """Actions are recorded."""
    agent.greet()
    agent.recommend_music("calm")
    assert len(agent.get_history()) == 2
