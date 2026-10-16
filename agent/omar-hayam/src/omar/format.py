"""Output formatting for scenarios."""

from __future__ import annotations

from typing import Any


class ScenarioFormatter:
    """Formats scenarios for different output types."""

    def format(self, scenario: Any, fmt: str = "markdown") -> str:
        """Format scenario to specified format."""
        if fmt == "markdown":
            return self._to_markdown(scenario)
        elif fmt == "json":
            return self._to_json(scenario)
        elif fmt == "screenplay":
            return self._to_screenplay(scenario)
        else:
            return self._to_markdown(scenario)

    def _to_markdown(self, scenario: Any) -> str:
        """Format as markdown."""
        lines = [
            f"# {scenario.title}",
            f"**Genre:** {scenario.genre}",
            "",
            "## Logline",
            scenario.logline,
            "",
            "## Synopsis",
            scenario.synopsis,
            "",
            "## Characters",
        ]
        for char in scenario.characters:
            lines.append(f"- **{char.name}** ({char.role})")
        lines.extend([
            "",
            "## Acts",
        ])
        for act in scenario.acts:
            lines.append(f"### Act {act['act']}: {act['name']}")
            for scene in act.get("scenes", []):
                lines.append(f"- {scene['title']}: {scene['description']}")
        if scenario.dialogue_samples:
            lines.extend(["", "## Dialogue Samples"])
            for sample in scenario.dialogue_samples:
                lines.append(f"**{sample['character']}:** {sample['line']}")
        return "\n".join(lines)

    def _to_json(self, scenario: Any) -> str:
        """Format as JSON string."""
        import json
        data = {
            "title": scenario.title,
            "genre": scenario.genre,
            "logline": scenario.logline,
            "synopsis": scenario.synopsis,
            "characters": [c.to_dict() for c in scenario.characters],
            "acts": scenario.acts,
            "dialogue_samples": scenario.dialogue_samples,
        }
        return json.dumps(data, indent=2)

    def _to_screenplay(self, scenario: Any) -> str:
        """Format as screenplay."""
        lines = [
            "FADE IN:",
            "",
            f"INT. {scenario.title.upper()} - DAY",
            "",
        ]
        for char in scenario.characters:
            lines.extend([
                f"{char.name.upper()}",
                "(V.O.)",
                "",
            ])
        for act in scenario.acts:
            lines.append(f"--- ACT {act['act']}: {act['name'].upper()} ---")
            for scene in act.get("scenes", []):
                lines.extend([f"  {scene['title']}", ""])
        return "\n".join(lines)