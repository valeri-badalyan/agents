
from valeri.session import Session


def test_session_create():
    session = Session()
    assert session.is_active is True
    assert session.id is not None


def test_session_create_with_id():
    session = Session("test-123")
    assert session.id == "test-123"


def test_session_update():
    session = Session()
    session.update("key", "value")
    assert session.get("key") == "value"


def test_session_get_default():
    session = Session()
    assert session.get("missing", "default") == "default"


def test_session_history():
    session = Session()
    session.add_to_history({"action": "test"})
    assert len(session.history) == 1
    assert session.history[0]["action"] == "test"


def test_session_clear_history():
    session = Session()
    session.add_to_history({"action": "test"})
    session.clear_history()
    assert len(session.history) == 0


def test_session_deactivate():
    session = Session()
    session.deactivate()
    assert session.is_active is False


def test_session_to_dict():
    session = Session("test-123")
    session.update("key", "value")
    d = session.to_dict()
    assert d["id"] == "test-123"
    assert d["state"]["key"] == "value"