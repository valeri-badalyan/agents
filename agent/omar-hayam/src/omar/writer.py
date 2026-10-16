"""Main scenario writing logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from omar.characters import Character
from omar.format import ScenarioFormatter
from omar.templates import StoryTemplate


@dataclass
class Scenario:
    """Represents a written scenario."""

    title: str
    genre: str
    logline: str
    synopsis: str
    characters: list[Character]
    acts: list[dict[str, Any]]
    scenes: list[dict[str, Any]]
    dialogue_samples: list[dict[str, str]]


class OmarWriter:
    """Scenario writer for games and films."""

    def __init__(self):
        self.formatter = ScenarioFormatter()
        self._templates: dict[str, StoryTemplate] = {}
        self._load_default_templates()

    def _load_default_templates(self) -> None:
        """Load default story templates."""
        self._templates["three-act"] = StoryTemplate(
            name="Three-Act Structure",
            acts=["Setup", "Confrontation", "Resolution"],
            description="Classic three-act structure with clear turning points.",
        )
        self._templates["hero-journey"] = StoryTemplate(
            name="Hero's Journey",
            acts=[
                "Ordinary World",
                "Call to Adventure",
                "Refusal",
                "Meeting Mentor",
                "Crossing Threshold",
                "Tests & Allies",
                "Approach Inmost Cave",
                "Ordeal",
                "Reward",
                "Road Back",
                "Resurrection",
                "Return with Elixir",
            ],
            description="Joseph Campbell's monomyth structure.",
        )

    def create_scenario(
        self,
        title: str,
        genre: str = "drama",
        characters: list[str] | None = None,
        setting: str = "",
        tone: str = "neutral",
        structure: str = "three-act",
    ) -> Scenario:
        """Create a new scenario."""
        chars = [Character(name=name) for name in (characters or [])]
        template = self._templates.get(structure, self._templates["three-act"])

        acts = [{"act": i + 1, "name": act_name, "scenes": []} for i, act_name in enumerate(template.acts)]

        logline = self._generate_logline(title, genre, characters, setting)
        synopsis = self._generate_synopsis(title, genre, setting, tone)

        return Scenario(
            title=title,
            genre=genre,
            logline=logline,
            synopsis=synopsis,
            characters=chars,
            acts=acts,
            scenes=[],
            dialogue_samples=[],
        )

    def _generate_logline(
        self,
        title: str,
        genre: str,
        characters: list[str] | None,
        setting: str,
    ) -> str:
        """Generate a one-sentence logline."""
        protag = characters[0] if characters else "A protagonist"
        setting_part = f"in {setting}" if setting else ""
        return f"{protag} {setting_part} must overcome conflict in this {genre} story."

    def _generate_synopsis(
        self,
        title: str,
        genre: str,
        setting: str,
        tone: str,
    ) -> str:
        """Generate a 2-3 paragraph synopsis."""
        return (
            f"{title} is a {tone} {genre} set {setting}.\n\n"
            f"The story follows characters as they navigate challenges "
            f"and growth in this compelling narrative."
        )

    def add_character(self, scenario: Scenario, name: str, **kwargs: Any) -> Character:
        """Add a character to the scenario."""
        char = Character(name=name, **kwargs)
        scenario.characters.append(char)
        return char

    def add_scene(
        self,
        scenario: Scenario,
        act: int,
        title: str,
        description: str,
    ) -> None:
        """Add a scene to an act."""
        if 1 <= act <= len(scenario.acts):
            scene = {"title": title, "description": description}
            scenario.acts[act - 1]["scenes"].append(scene)
            scenario.scenes.append({"act": act, **scene})

    def add_dialogue(
        self,
        scenario: Scenario,
        character: str,
        line: str,
    ) -> None:
        """Add a dialogue sample."""
        scenario.dialogue_samples.append({"character": character, "line": line})

    def format_scenario(self, scenario: Scenario, fmt: str = "markdown") -> str:
        """Format scenario for output."""
        return self.formatter.format(scenario, fmt)

    def list_templates(self) -> list[str]:
        """List available story templates."""
        return list(self._templates.keys())