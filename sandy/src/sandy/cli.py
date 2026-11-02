"""CLI for Sandy music director agent."""

from __future__ import annotations

import json
import logging

import typer

from sandy.core import Sandy

logging.basicConfig(level=logging.INFO)

app = typer.Typer(help="Sandy — музыкальный директор: recommend, keys, setlist, rehearsal, brief, chat")
agent = Sandy()


def _dump(data: object) -> None:
    typer.echo(json.dumps(data, ensure_ascii=False, indent=2))


@app.command()
def recommend(mood: str, scene: str = "", bpm: float = 0) -> None:
    """Music direction: sandy recommend epic --scene "финал" --bpm 100."""
    _dump(agent.recommend_music(mood, scene, bpm or None))


@app.command()
def keys(key_a: str, key_b: str) -> None:
    """Key compatibility: sandy keys Am C."""
    _dump(agent.key_compatibility(key_a, key_b))


@app.command()
def setlist(path: str, arc: str = "rise") -> None:
    """Build setlist from JSON file of songs: sandy setlist songs.json --arc wave."""
    with open(path, encoding="utf-8") as fh:
        songs = json.load(fh)
    _dump(agent.build_setlist(songs, arc))


@app.command()
def rehearsal(minutes: int, songs: str, band: int = 4) -> None:
    """Rehearsal plan: sandy rehearsal 120 "Song A,Song B" --band 5."""
    titles = [s.strip() for s in songs.split(",") if s.strip()]
    for block in agent.rehearsal_plan(minutes, titles, band):
        typer.echo(f"{block['start']:>3}′ +{block['minutes']:>3}′  {block['task']}")


@app.command()
def brief(project: str, scenes: str, lang: str = "ru") -> None:
    """Soundtrack brief: sandy brief "Промо" "Интро:epic,Финал:happy"."""
    parsed = []
    for chunk in scenes.split(","):
        name, _, mood = chunk.partition(":")
        parsed.append({"name": name.strip(), "mood": mood.strip()})
    typer.echo(agent.soundtrack_brief(project, parsed, lang))


@app.command()
def chat(text: str, lang: str = "auto") -> None:
    """Chat: sandy chat "музыка для грустной сцены"."""
    typer.echo(agent.chat(text, None if lang == "auto" else lang)["reply"])


@app.command()
def greet(lang: str = "ru") -> None:
    """Greet: sandy greet ru."""
    typer.echo(agent.greet(lang))


if __name__ == "__main__":
    app()
