import typer
from rich.console import Console
from rich.table import Table

from jouli.core import engine
from jouli.exceptions import JouliError, LanguageError, ProviderError

app = typer.Typer(
    name="jouli",
    help="Jouli - A translator agent",
    add_completion=False,
)
console = Console()


def handle_error(e: JouliError):
    console.print(f"[red]Error:[/red] {e}")
    raise typer.Exit(1)


@app.command()
def translate(
    text: str = typer.Argument(..., help="Text to translate"),
    target_lang: str = typer.Option("en", "--to", "-t", help="Target language code"),
    source_lang: str | None = typer.Option(
        None, "--from", "-f", help="Source language code (auto-detect if omitted)"
    ),
    provider: str = typer.Option("google", "--provider", "-p", help="Translation provider"),
):
    """Translate text to target language."""
    try:
        result = engine.translate(text, target_lang, source_lang, provider)
        console.print(f"[green]{result.text}[/green]")
        if source_lang is None:
            console.print(f"[dim]Detected source: {result.source_lang} → {result.target_lang} ({result.provider})[/dim]")
    except (ProviderError, LanguageError) as e:
        handle_error(e)


@app.command()
def detect(
    text: str = typer.Argument(..., help="Text to detect language for"),
    provider: str = typer.Option("google", "--provider", "-p", help="Translation provider"),
):
    """Detect the language of the given text."""
    try:
        lang = engine.detect_language(text, provider)
        console.print(f"[green]{lang}[/green]")
    except (ProviderError, LanguageError) as e:
        handle_error(e)


@app.command()
def languages(
    provider: str = typer.Option("google", "--provider", "-p", help="Translation provider"),
):
    """List supported languages for a provider."""
    try:
        langs = engine.get_supported_languages(provider)
        table = Table(title=f"Supported languages ({provider})")
        table.add_column("Code", style="cyan")
        table.add_column("Language", style="green")
        for code in sorted(langs):
            table.add_row(code, code)
        console.print(table)
    except (ProviderError, LanguageError) as e:
        handle_error(e)


@app.command()
def providers():
    """List available translation providers."""
    provs = engine.list_providers()
    table = Table(title="Available Providers")
    table.add_column("Name", style="cyan")
    table.add_column("Status", style="green")
    for p in provs:
        table.add_row(p, "✓ Registered")
    console.print(table)


def main():
    app()


if __name__ == "__main__":
    main()