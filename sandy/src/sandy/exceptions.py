"""Custom exceptions for Sandy music director agent."""

from __future__ import annotations


class SandyError(Exception):
    """Base exception for Sandy errors."""


class MoodError(SandyError):
    """Raised when music recommendation by mood/scene fails."""


class MusicKeyError(SandyError):
    """Raised when a musical key cannot be parsed."""


class SetlistError(SandyError):
    """Raised when a setlist cannot be built."""


class RehearsalError(SandyError):
    """Raised when a rehearsal plan cannot be built."""


class BriefError(SandyError):
    """Raised when a soundtrack brief cannot be built."""


class ConfigurationError(SandyError):
    """Raised when configuration is invalid."""
