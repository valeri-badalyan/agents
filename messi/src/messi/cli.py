"""CLI for Messi football agent."""

from __future__ import annotations

import logging

import typer

from messi.core import Messi

logging.basicConfig(level=logging.INFO)

app = typer.Typer(help="Messi — футбольный агент: тактика, тренировки, мотивация")
agent = Messi()


@app.command()
def tactics(formation: str = "4-3-3") -> None:
    """Analyze formation, e.g. messi tactics 4-3-3."""
    result = agent.analyze_formation(formation)
    typer.echo(f"Схема {result['formation']} ({result['style']})")
    typer.echo(f"Сила: {result['strength']}")
    typer.echo(f"Слабость: {result['weakness']}")
    typer.echo(result["advice"])


@app.command()
def train(level: str = "beginner", position: str = "forward") -> None:
    """Show training plan: messi train --level amateur --position winger."""
    plan = agent.training_plan(level, position)
    typer.echo(f"План ({plan['level']}, {plan['position']}):")
    exercises = plan["exercises"]
    assert isinstance(exercises, list)
    for i, ex in enumerate(exercises, 1):
        typer.echo(f"{i}. {ex}")


@app.command()
def motivate(name: str = "чемпион") -> None:
    """Print motivational message."""
    typer.echo(agent.motivate(name))


@app.command()
def quiz() -> None:
    """Print a random quiz question."""
    q = agent.quiz_question()
    typer.echo(q["question"])
    options = q["options"]
    assert isinstance(options, list)
    for opt in options:
        typer.echo(f"- {opt}")


if __name__ == "__main__":
    app()
