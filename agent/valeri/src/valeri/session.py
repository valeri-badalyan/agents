"""Session management — tracks agent sessions and state."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any


class Session:
    """Manages a single agent session."""

    def __init__(self, session_id: str | None = None):
        self.id = session_id or str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = self.created_at
        self.state: dict[str, Any] = {}
        self.history: list[dict[str, Any]] = []
        self._active = True

    def update(self, key: str, value: Any) -> None:
        """Update session state."""
        self.state[key] = value
        self.updated_at = datetime.now(timezone.utc)

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from session state."""
        return self.state.get(key, default)

    def add_to_history(self, entry: dict[str, Any]) -> None:
        """Add an entry to session history."""
        entry["timestamp"] = datetime.now(timezone.utc).isoformat()
        self.history.append(entry)
        self.updated_at = datetime.now(timezone.utc)

    def clear_history(self) -> None:
        """Clear session history."""
        self.history = []

    def deactivate(self) -> None:
        """Deactivate the session."""
        self._active = False
        self.updated_at = datetime.now(timezone.utc)

    @property
    def is_active(self) -> bool:
        """Check if session is active."""
        return self._active

    def to_dict(self) -> dict[str, Any]:
        """Convert session to dictionary."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "state": self.state,
            "history": self.history,
            "active": self._active,
        }

    def __repr__(self) -> str:
        return f"Session(id={self.id}, active={self._active})"