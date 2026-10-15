"""Tests for V3 Session."""

import pytest

from v3.session import Session


def test_session_create() -> None:
    """New session is active with an id."""
    session = Session()
    assert session.is_active is True
    assert session.id is not None


def test_session_create_with_id() -> None:
    """Explicit id is kept."""
    session = Session("test-123")
    assert session.id == "test-123"


def test_session_update() -> None:
    """State update works."""
    session = Session()
    session.update("key", "value")
    assert session.get("key") == "value"


def test_session_update_empty_key() -> None:
    """Empty key raises ValueError."""
    session = Session()
    with pytest.raises(ValueError):
        session.update("", "value")


def test_session_get_default() -> None:
    """Missing key returns default."""
    session = Session()
    assert session.get("missing", "default") == "default"


def test_session_history() -> None:
    """History entries are timestamped."""
    session = Session()
    session.add_to_history({"action": "test"})
    assert len(session.history) == 1
    assert session.history[0]["action"] == "test"
    assert "timestamp" in session.history[0]


def test_session_history_invalid() -> None:
    """Non-dict history entry raises ValueError."""
    session = Session()
    with pytest.raises(ValueError):
        session.add_to_history("not-a-dict")  # type: ignore[arg-type]


def test_session_clear_history() -> None:
    """History can be cleared."""
    session = Session()
    session.add_to_history({"action": "test"})
    session.clear_history()
    assert len(session.history) == 0


def test_session_deactivate() -> None:
    """Deactivation works."""
    session = Session()
    session.deactivate()
    assert session.is_active is False


def test_session_to_dict() -> None:
    """Serialization keeps state."""
    session = Session("test-123")
    session.update("key", "value")
    d = session.to_dict()
    assert d["id"] == "test-123"
    assert d["state"]["key"] == "value"
