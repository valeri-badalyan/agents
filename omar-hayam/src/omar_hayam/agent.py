"""Core narrative agent — creates storylines, characters, and worlds."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Character:
    """A story character."""

    name: str
    role: str = "protagonist"
    traits: list[str] = field(default_factory=list)
    backstory: str = ""
    arc: str = ""


@dataclass
class WorldElement:
    """A world-building element."""

    name: str
    kind: str = "location"
    description: str = ""
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class StoryStructure:
    """Basic story structure."""

    premise: str = ""
    act_one: str = ""
    act_two: str = ""
    act_three: str = ""
    theme: str = ""
    tone: str = ""


class OmarHayam:
    """Narrative agent for creating storylines, characters, and worlds."""

    def __init__(self) -> None:
        self.characters: list[Character] = []
        self.world: list[WorldElement] = []
        self.structure: StoryStructure = StoryStructure()

    def create_character(
        self, name: str, role: str = "protagonist", traits: list[str] | None = None, backstory: str = ""
    ) -> Character:
        """Create a new character."""
        char = Character(name=name, role=role, traits=traits or [], backstory=backstory)
        self.characters.append(char)
        return char

    def add_world_element(self, name: str, kind: str = "location", description: str = "") -> WorldElement:
        """Add a world-building element."""
        elem = WorldElement(name=name, kind=kind, description=description)
        self.world.append(elem)
        return elem

    def outline_story(self, premise: str, theme: str = "", tone: str = "") -> StoryStructure:
        """Create a basic three-act story outline."""
        self.structure = StoryStructure(premise=premise, theme=theme, tone=tone)
        return self.structure

    def write_dialogue(self, character_a: str, character_b: str, topic: str) -> str:
        """Generate a sample dialogue between two characters."""
        return (
            f"[{character_a}]: Let's talk about {topic}.\n"
            f"[{character_b}]: I've been thinking about that too.\n"
            f"[{character_a}]: Here's what I believe...\n"
            f"[{character_b}]: That makes sense, but consider this..."
        )

    def generate_pitch(self) -> str:
        """Generate a one-paragraph story pitch."""
        parts = []
        if self.structure.premise:
            parts.append(f"Premise: {self.structure.premise}")
        if self.characters:
            names = ", ".join(c.name for c in self.characters)
            parts.append(f"Characters: {names}")
        if self.world:
            places = ", ".join(w.name for w in self.world)
            parts.append(f"World: {places}")
        if self.structure.theme:
            parts.append(f"Theme: {self.structure.theme}")
        return " | ".join(parts) if parts else "No story defined yet."

    def execute(self, task: str, **kwargs: Any) -> str:
        """Main entry point — route narrative tasks."""
        task_lower = task.lower()
        if "character" in task_lower:
            name = kwargs.get("name", "Untitled")
            return f"Created character: {self.create_character(name, **{k: v for k, v in kwargs.items() if k != 'name'}).name}"
        elif "dialogue" in task_lower:
            a = kwargs.get("a", "Character A")
            b = kwargs.get("b", "Character B")
            topic = kwargs.get("topic", "life")
            return self.write_dialogue(a, b, topic)
        elif "pitch" in task_lower:
            return self.generate_pitch()
        elif "story" in task_lower or "outline" in task_lower:
            premise = kwargs.get("premise", task)
            self.outline_story(premise, kwargs.get("theme", ""), kwargs.get("tone", ""))
            return f"Story outlined: {premise}"
        else:
            return self.generate_pitch()

    def __repr__(self) -> str:
        return f"OmarHayam(characters={len(self.characters)}, world={len(self.world)})"
