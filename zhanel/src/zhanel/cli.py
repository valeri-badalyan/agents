"""CLI for Zhanel marketing agent."""

from __future__ import annotations

import logging

import typer

from zhanel.core import Zhanel

logging.basicConfig(level=logging.INFO)

app = typer.Typer(help="Жанель — маркетолог: стратегия, тексты, контент-планы")
agent = Zhanel()


@app.command()
def audience(product: str) -> None:
    """Segment audience: zhanel audience 'фитнес-приложение'."""
    result = agent.analyze_audience(product)
    typer.echo(f"Продукт: {result['product']}")
    segments = result["segments"]
    assert isinstance(segments, list)
    for s in segments:
        assert isinstance(s, dict)
        typer.echo(f"- {s['segment']}: {s['jtbd']} / боль: {s['pain']}")


@app.command()
def usp(product: str, audience_arg: str = "новички", benefit: str = "результат") -> None:
    """Build positioning: zhanel usp 'кофейня' 'студенты' 'вкусный кофе'."""
    result = agent.positioning(product, audience_arg, benefit)
    typer.echo(result["usp"])
    typer.echo(result["logic"])


@app.command()
def copy(product: str, angle: str = "all") -> None:
    """Ad headlines: zhanel copy 'фитнес-приложение' --angle all."""
    result = agent.ad_copy(product, angle)
    variants = result["variants"]
    assert isinstance(variants, dict)
    for key, val in variants.items():
        assert isinstance(val, dict)
        typer.echo(f"[{key}] {val['headline']}")


@app.command()
def slogan(business: str) -> None:
    """Slogans: zhanel slogan 'кофейня'."""
    result = agent.slogan(business, seed=1)
    slogans = result["slogans"]
    assert isinstance(slogans, list)
    for i, s in enumerate(slogans, 1):
        typer.echo(f"{i}. {s}")


@app.command()
def plan(brand: str, weeks: int = 4) -> None:
    """Content plan: zhanel plan 'бьюти-бренд' --weeks 4."""
    result = agent.content_plan(brand, weeks)
    plan_items = result["plan"]
    assert isinstance(plan_items, list)
    for item in plan_items:
        assert isinstance(item, dict)
        typer.echo(f"{item['week']} {item['day']} [{item['rubric']}] {item['topic']}")


@app.command()
def launch(product: str) -> None:
    """Launch checklist: zhanel launch 'онлайн-курс'."""
    result = agent.launch_checklist(product)
    steps = result["steps"]
    assert isinstance(steps, list)
    for step in steps:
        typer.echo(f"- {step}")


@app.command()
def audit(idea: str) -> None:
    """Audit idea: zhanel audit 'запустим вирусный ролик для всех'."""
    result = agent.audit_idea(idea)
    typer.echo(result["verdict"])
    typer.echo(result["reasoning"])


if __name__ == "__main__":
    app()
