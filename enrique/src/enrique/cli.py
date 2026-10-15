"""CLI for Enrique — humorous companion."""

from __future__ import annotations

import typer
from rich.console import Console

from enrique.core import Enrique
from enrique.exceptions import EnriqueError

app = typer.Typer(name="enrique", help="Enrique — funny trilingual companion", add_completion=False)
console = Console()


def _engine(memory: str | None = None) -> Enrique:
    return Enrique(memory_path=memory) if memory else Enrique()


@app.command()
def chat(
    text: str = typer.Argument(..., help="Message (say 'enrike' to reload SSOT)"),
    lang: str | None = typer.Option(None, "--lang", "-l", help="ru|hy|en"),
    memory: str | None = typer.Option(None, "--memory", help="Custom memory JSON path"),
) -> None:
    """Chat with Enrique."""
    try:
        eng = _engine(memory)
        out = eng.chat(text, lang=lang)
        console.print(f"[green]{out['reply']}[/green]")
        console.print(f"[dim]{out['reasoning']}[/dim]")
    except EnriqueError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(1)


@app.command()
def recall(
    lang: str | None = typer.Option(None, "--lang", help="Filter by ru|hy|en"),
    memory: str | None = typer.Option(None, "--memory", help="Custom memory JSON path"),
) -> None:
    """Show remembered main things (facts) from SSOT."""
    eng = _engine(memory)
    facts = eng.memory.get_facts(lang=lang)
    if not facts:
        console.print("[yellow]Nothing remembered yet. Tell me something juicy![/yellow]")
        return
    for f in facts:
        console.print(f"- [{f.get('lang')}] {f.get('text')}")


@app.command()
def patterns(memory: str | None = typer.Option(None, "--memory", help="Custom memory path")) -> None:
    """Show detected conversation patterns."""
    eng = _engine(memory)
    console.print(eng.memory.get_patterns())


def main() -> None:
    """CLI entry point."""
    app()


if __name__ == "__main__":
    main()
