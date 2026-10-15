"""CLI for Olinho idea-to-browser agent."""

from __future__ import annotations

import logging

import typer

from olinho.core import Olinho

logging.basicConfig(level=logging.INFO)

app = typer.Typer(help="Олиньо!! — реализует идеи и выкладывает в браузер")
agent = Olinho()


@app.command()
def classify(idea: str) -> None:
    """Detect type: olinho classify 'сделай игру кликер'."""
    result = agent.classify(idea)
    typer.echo(f"Тип: {result['type']} ({result['title']}) уверенность: {result['confidence']}")


@app.command()
def build(idea: str, name: str = "") -> None:
    """Scaffold project: olinho build 'лендинг кофейни' --name coffee."""
    result = agent.build(idea, name or None)
    typer.echo(f"Готово: {result['path']}")
    typer.echo(f"Открой в Chrome: {result['preview_url']}")


@app.command()
def ship(idea: str, name: str = "", open_browser: bool = False) -> None:
    """Full pipeline: olinho ship 'игра про космос' --open-browser."""
    result = agent.ship(idea, name or None, open_browser=open_browser)
    typer.echo(f"Проект: {result['path']} тип: {result['type']}")
    typer.echo(f"Preview: {result['preview_url']}")
    if "zip" in result:
        typer.echo(f"ZIP для хостинга: {result['zip']}")


@app.command()
def preview(path: str, browser: str = "chrome") -> None:
    """Open in browser: olinho preview projects/my-idea --browser chrome."""
    result = agent.preview(path, browser)
    typer.echo(f"Открыто: {result['url']}")


@app.command()
def pack(path: str) -> None:
    """Zip for deploy: olinho pack projects/my-idea."""
    result = agent.pack(path)
    typer.echo(f"ZIP: {result['zip']}")


if __name__ == "__main__":
    app()
