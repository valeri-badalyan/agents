"""CLI for Mika provider agent."""

from __future__ import annotations

import json
import logging

import typer

from mika.core import Mika

logging.basicConfig(level=logging.INFO)

app = typer.Typer(help="Mika — весёлый провайдер: tariffs, recommend, coverage, diagnose, connect, chat")
agent = Mika()


@app.command()
def tariffs() -> None:
    """List all tariffs: mika tariffs."""
    typer.echo(json.dumps(agent.list_tariffs(), ensure_ascii=False, indent=2))


@app.command()
def recommend(usage: str = "family", budget: float = 99999, speed: float = 0) -> None:
    """Recommend tariff: mika recommend gaming --budget 800 --speed 100."""
    result = agent.recommend_tariff(usage=usage, budget=budget, min_speed=speed)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command()
def coverage(address: str) -> None:
    """Check coverage: mika coverage "центр"."""
    typer.echo(json.dumps(agent.check_coverage(address), ensure_ascii=False, indent=2))


@app.command()
def diagnose(measured: float, expected: float, ping: float = 20, wifi: bool = True) -> None:
    """Diagnose: mika diagnose 20 100 --ping 80."""
    typer.echo(json.dumps(
        agent.diagnose(measured, expected, ping, wifi), ensure_ascii=False, indent=2,
    ))


@app.command()
def connect(home: str = "apartment") -> None:
    """Connection steps: mika connect house."""
    for step in agent.connection_steps(home):
        typer.echo(step)


@app.command()
def chat(text: str, lang: str = "ru") -> None:
    """Chat: mika chat "привет, покажи тарифы"."""
    out = agent.chat(text, lang=lang) if lang != "auto" else agent.chat(text)
    typer.echo(out["reply"])


@app.command()
def greet(lang: str = "ru") -> None:
    """Greet: mika greet ru."""
    typer.echo(agent.greet(lang))


if __name__ == "__main__":
    app()
