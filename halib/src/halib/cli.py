"""CLI for Halib designer agent."""

from __future__ import annotations

import json
import logging

import typer

from halib.core import Halib

logging.basicConfig(level=logging.INFO)

app = typer.Typer(help="Халиб — дизайнер: concept, palette, typo, layout, logo, guide, audit")
agent = Halib()


@app.command()
def concept(project: str, style: str = "minimal", mood: str = "trustworthy") -> None:
    """Build design concept: halib concept 'Coffee' --style minimal --mood calm."""
    result = agent.concept(project, style, mood)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command()
def palette(brand: str, mood: str = "trustworthy", count: int = 5) -> None:
    """Generate palette: halib palette 'Coffee' --mood premium --count 5."""
    result = agent.palette(brand, mood, count)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command()
def typo(project: str, style: str = "minimal") -> None:
    """Pick fonts: halib typo 'Coffee' --style luxury."""
    result = agent.typography(project, style)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command()
def layout(page: str = "landing") -> None:
    """Show page layout: halib layout landing."""
    result = agent.layout(page)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command()
def logo(business: str, character: str = "строгий", symbol: str = "знак") -> None:
    """Write logo brief: halib logo 'Coffee'."""
    typer.echo(agent.logo_brief(business, character, symbol))


@app.command()
def guide(brand: str, style: str = "minimal", mood: str = "trustworthy") -> None:
    """Build style guide: halib guide 'Coffee'."""
    typer.echo(agent.style_guide(brand, style, mood))


@app.command()
def audit(description: str) -> None:
    """Audit design: halib audit 'Лендинг, много текста, нет кнопки'."""
    typer.echo(agent.audit_design(description))


if __name__ == "__main__":
    app()
