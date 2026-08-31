"""Character creation and management."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Character:
    """Represents a character in a scenario."""

    name: str
    role: str = "supporting"
    backstory: str = ""
    motivation: str = ""
    conflict: str = ""
    arc: str = ""
    traits: list[str] = field(default_factory=list)
    relationships: dict[str, str] = field(default_factory=dict)

    def add_trait(self, trait: str) -> None:
        """Add a personality trait."""
        if trait not in self.traits:
            self.traits.append(trait)

    def add_relationship(self, character: str, relationship: str) -> None:
        """Add a relationship with another character."""
        self.relationships[character] = relationship

    def describe(self) -> str:
        """Get a brief character description."""
        parts = [self.name]
        if self.role:
            parts.append(f"({self.role})")
        if self.backstory:
            parts.append(f"- {self.backstory}")
        if self.motivation:
            parts.append(f"Motivation: {self.motivation}")
        if self.conflict:
            parts.append(f"Conflict: {self.conflict}")
        return " ".join(parts)

    def to_dict(self) -> dict[str, Any]:
        """Convert character to dictionary."""
        return {
            "name": self.name,
            "role": self.role,
            "backstory": self.backstory,
            "motivation": self.motivation,
            "conflict": self.conflict,
            "arc": self.arc,
            "traits": self.traits,
            "relationships": self.relationships,
        }

    def __repr__(self) -> str:
        return f"Character(name={self.name!r}, role={self.role!r})"