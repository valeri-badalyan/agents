"""CLI for Ferracho analyzer agent."""

from __future__ import annotations

import json
import logging

import typer

from ferracho.core import Ferracho

logging.basicConfig(level=logging.INFO)

app = typer.Typer(help="Ferracho!! - бизнес-аналитик: swot, funnel, unit, risks, audit")
agent = Ferracho()


@app.command()
def swot(data: str) -> None:
    """Run SWOT from JSON, e.g. ferracho swot with strengths list."""
    payload = json.loads(data)
    result = agent.swot_analysis(payload)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command()
def funnel(data: str) -> None:
    """Run funnel from JSON with ordered stage volumes."""
    payload = json.loads(data)
    result = agent.funnel_analysis(payload)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command()
def unit(price: float, variable_cost: float, cac: float, monthly_volume: float) -> None:
    """Show unit economics: ferracho unit 1000 400 200 100."""
    result = agent.unit_economics(price, variable_cost, cac, monthly_volume)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command()
def risks(data: str) -> None:
    """Score risks from JSON list."""
    payload = json.loads(data)
    result = agent.risk_matrix(payload)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command()
def audit(business_name: str, description: str) -> None:
    """Print audit report: ferracho audit Coffee with description."""
    typer.echo(agent.audit_report(business_name, description))


if __name__ == "__main__":
    app()
