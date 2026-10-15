"""Versioned long-term memory for Enrique.

Stores conversation history, key facts (main things),
observed patterns, and reasoning traces. Never stores
secrets — callers must filter sensitive data first.
"""

from __future__ import annotations

import json
import logging
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from enrique.exceptions import MemoryError, ValidationError

logger = logging.getLogger(__name__)

MEMORY_VERSION = 1
SUPPORTED_LANGS = ("ru", "hy", "en")


def _utc_now() -> str:
    """Return current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def _validate_text(text: str, field: str = "text") -> str:
    """Validate non-empty user text input."""
    if not isinstance(text, str):
        raise ValidationError(f"{field} must be a string")
    cleaned = text.strip()
    if not cleaned:
        raise ValidationError(f"{field} must not be empty")
    if len(cleaned) > 5000:
        raise ValidationError(f"{field} too long (max 5000 chars)")
    return cleaned


class MemoryStore:
    """JSON-backed versioned memory for conversations and patterns."""

    def __init__(self, path: str | Path = "./enrique_memory.json") -> None:
        """Initialize memory store at given path."""
        self.path = Path(path)
        self.data: dict[str, Any] = {
            "version": MEMORY_VERSION,
            "history": [],
            "facts": [],
            "patterns": {},
            "reasoning_log": [],
        }
        self.load()

    def load(self) -> None:
        """Load memory from disk if file exists."""
        if not self.path.exists():
            logger.info("No memory file at %s, starting fresh", self.path)
            return
        try:
            raw = self.path.read_text(encoding="utf-8")
            loaded: dict[str, Any] = json.loads(raw)
            if not isinstance(loaded, dict):
                raise MemoryError("Memory file is corrupt: not an object")
            # Migrate / merge with defaults, keep version.
            for key in ("history", "facts", "reasoning_log"):
                if key in loaded and isinstance(loaded[key], list):
                    self.data[key] = loaded[key]
            if "patterns" in loaded and isinstance(loaded["patterns"], dict):
                self.data["patterns"] = loaded["patterns"]
            self.data["version"] = int(loaded.get("version", MEMORY_VERSION))
            logger.info("Loaded memory v%s from %s", self.data["version"], self.path)
        except json.JSONDecodeError as exc:
            raise MemoryError(f"Memory file corrupt: {exc}") from exc
        except OSError as exc:
            raise MemoryError(f"Cannot read memory: {exc}") from exc

    def save(self) -> None:
        """Persist memory to disk."""
        try:
            if self.path.parent and str(self.path.parent) not in ("", "."):
                self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(
                json.dumps(self.data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            logger.debug("Saved memory to %s", self.path)
        except OSError as exc:
            raise MemoryError(f"Cannot save memory: {exc}") from exc

    def add_exchange(
        self,
        user_text: str,
        reply_text: str,
        lang: str,
        max_history: int = 200,
    ) -> None:
        """Record one conversation turn."""
        user_text = _validate_text(user_text, "user_text")
        reply_text = _validate_text(reply_text, "reply_text")
        if lang not in SUPPORTED_LANGS:
            lang = "en"
        self.data["history"].append(
            {
                "ts": _utc_now(),
                "lang": lang,
                "user": user_text,
                "enrique": reply_text,
            }
        )
        # Trim history.
        if len(self.data["history"]) > max_history:
            self.data["history"] = self.data["history"][-max_history:]
        self._update_patterns(user_text)
        self.save()

    def add_fact(self, fact: str, lang: str = "en", max_facts: int = 100) -> bool:
        """Store a key fact (main thing). Returns True if new."""
        fact = _validate_text(fact, "fact")
        if lang not in SUPPORTED_LANGS:
            lang = "en"
        existing = {f["text"].lower() for f in self.data["facts"]}
        if fact.lower() in existing:
            return False
        self.data["facts"].append({"text": fact, "lang": lang, "ts": _utc_now()})
        if len(self.data["facts"]) > max_facts:
            self.data["facts"] = self.data["facts"][-max_facts:]
        self.save()
        return True

    def get_facts(self, lang: str | None = None) -> list[dict[str, str]]:
        """Return stored key facts, optionally filtered by language."""
        facts: list[dict[str, str]] = self.data.get("facts", [])
        if lang is None:
            return list(facts)
        return [f for f in facts if f.get("lang") == lang]

    def get_history(self, limit: int = 20) -> list[dict[str, str]]:
        """Return last N conversation turns."""
        if limit <= 0:
            raise ValidationError("limit must be positive")
        return list(self.data.get("history", [])[-limit:])

    def log_reasoning(self, summary: str) -> None:
        """Append a reasoning trace entry."""
        summary = _validate_text(summary, "summary")
        self.data["reasoning_log"].append({"ts": _utc_now(), "summary": summary})
        self.data["reasoning_log"] = self.data["reasoning_log"][-100:]
        self.save()

    def get_patterns(self) -> dict[str, Any]:
        """Return detected conversation patterns."""
        return dict(self.data.get("patterns", {}))

    def _update_patterns(self, user_text: str) -> None:
        """Update simple word-frequency patterns from user text."""
        words = re.findall(r"[\w\u0400-\u04FF\u0530-\u058F]+", user_text.lower())
        stop = {"the", "and", "и", "в", "на", "է", "ու", "a", "is", "это"}
        meaningful = [w for w in words if len(w) > 2 and w not in stop]
        counts: Counter[str] = Counter(self.data["patterns"].get("top_words", {}))
        counts.update(meaningful)
        top = dict(counts.most_common(20))
        self.data["patterns"]["top_words"] = top
        self.data["patterns"]["total_turns"] = len(self.data["history"])
        # Language distribution.
        lang_counts: Counter[str] = Counter(t.get("lang", "en") for t in self.data["history"])
        self.data["patterns"]["langs"] = dict(lang_counts)

    def clear(self) -> None:
        """Clear all memory (history, facts, patterns)."""
        self.data = {
            "version": MEMORY_VERSION,
            "history": [],
            "facts": [],
            "patterns": {},
            "reasoning_log": [],
        }
        self.save()
