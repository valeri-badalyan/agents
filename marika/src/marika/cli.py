"""CLI for Marika statistics agent."""

from __future__ import annotations

import json
import logging

import typer

from marika.core import Marika

logging.basicConfig(level=logging.INFO)

app = typer.Typer(help="Marika — руководитель статистики: describe, growth, trend, shares, report")
agent = Marika()


def _parse_numbers(raw: str) -> list[float]:
    """Parse comma/space separated numbers.

    Args:
        raw: Input string like "1,2,3" or "1 2 3".

    Returns:
        List of floats.
    """
    cleaned = raw.replace(",", " ").split()
    return [float(x) for x in cleaned]


@app.command()
def describe(data: str) -> None:
    """Describe numbers, e.g. marika describe "1,2,3,4"."""
    result = agent.describe(_parse_numbers(data))
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command()
def growth(old: float, new: float) -> None:
    """Show growth: marika growth 100 150."""
    result = agent.growth_rate(old, new)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command()
def trend(data: str) -> None:
    """Show trend: marika trend "1,2,3,5,8"."""
    result = agent.trend(_parse_numbers(data))
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command()
def shares(data: str) -> None:
    """Show shares from JSON: marika shares '{"a": 30, "b": 70}'."""
    parts = json.loads(data)
    result = agent.shares(parts)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command()
def report(data: str, lang: str = "ru", title: str = "") -> None:
    """Print localized report: marika report "1,2,3" --lang zh."""
    typer.echo(agent.summary_report(_parse_numbers(data), lang=lang, title=title))


if __name__ == "__main__":
    app()
