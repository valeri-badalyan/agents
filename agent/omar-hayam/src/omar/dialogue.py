"""Dialogue generation."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DialogueLine:
    """A single line of dialogue."""

    character: str
    line: str
    direction: str = ""
    subtext: str = ""


@dataclass
class DialogueScene:
    """A scene of dialogue."""

    title: str
    lines: list[DialogueLine] = field(default_factory=list)

    def add_line(self, character: str, line: str, direction: str = "", subtext: str = "") -> None:
        """Add a line of dialogue."""
        self.lines.append(DialogueLine(character=character, line=line, direction=direction, subtext=subtext))

    def get_character_lines(self, character: str) -> list[DialogueLine]:
        """Get all lines for a character."""
        return [l for l in self.lines if l.character == character]

    def to_script(self) -> str:
        """Format dialogue as a script."""
        output = []
        for line in self.lines:
            if line.direction:
                output.append(f"({line.direction})")
            output.append(f"{line.character.upper()}: {line.line}")
            if line.subtext:
                output.append(f"[{line.subtext}]")
        return "\n".join(output)


class DialogueGenerator:
    """Generates dialogue for characters."""

    def __init__(self):
        self._templates: dict[str, list[str]] = {
            "argument": [
                "I can't believe you did that.",
                "You don't understand.",
                "Then help me understand!",
            ],
            "negotiation": [
                "What are your terms?",
                "I think we can work something out.",
                "Let me think about it.",
            ],
            "revelation": [
                "There's something I need to tell you.",
                "I've been keeping a secret.",
                "The truth is...",
            ],
        }

    def generate_template(self, style: str = "argument") -> list[str]:
        """Generate dialogue from a template."""
        return self._templates.get(style, self._templates["argument"]).copy()

    def create_scene(self, title: str) -> DialogueScene:
        """Create a new dialogue scene."""
        return DialogueScene(title=title)

    def add_custom_template(self, name: str, lines: list[str]) -> None:
        """Add a custom dialogue template."""
        self._templates[name] = lines

    def list_templates(self) -> list[str]:
        """List available dialogue templates."""
        return list(self._templates.keys())