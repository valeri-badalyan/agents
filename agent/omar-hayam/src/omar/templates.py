"""Story templates and structures."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class StoryTemplate:
    """A story structure template."""

    name: str
    acts: list[str]
    description: str
    themes: list[str] = field(default_factory=list)

    def get_act(self, index: int) -> str | None:
        """Get act name by index."""
        if 0 <= index < len(self.acts):
            return self.acts[index]
        return None

    def get_all_acts(self) -> list[str]:
        """Get all act names."""
        return self.acts.copy()

    def __repr__(self) -> str:
        return f"StoryTemplate(name={self.name!r}, acts={len(self.acts)})"