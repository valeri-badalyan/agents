"""CLI for Aryubi finance agent."""

from __future__ import annotations

import json
import logging

import typer

from aryubi.core import Aryubi

logging.basicConfig(level=logging.INFO)

app = typer.Typer(help="Арюби - финансист: budget, cashflow, pnl, invest, report")
agent = Aryubi()


@app.command()
def budget(income: str, expenses: str) -> None:
    """Run budget from two JSON dicts, e.g. aryubi budget with income and expenses JSON."""
    inc = json.loads(income)
    exp = json.loads(expenses)
    result = agent.budget_analysis(inc, exp)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command()
def cashflow(flows: str, start_balance: float = 0) -> None:
    """Run cashflow from JSON list, e.g. aryubi cashflow with flows list."""
    payload = json.loads(flows)
    result = agent.cashflow_analysis(payload, start_balance)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command()
def pnl(revenue: float, cogs: float, opex: float, tax_rate_pct: float = 0) -> None:
    """Show P&L: aryubi pnl 100000 40000 30000."""
    result = agent.profit_loss(revenue, cogs, opex, tax_rate_pct)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command()
def invest(principal: float, monthly_contrib: float, annual_rate_pct: float, years: float) -> None:
    """Project investments: aryubi invest 100000 10000 12 5."""
    result = agent.investment_growth(principal, monthly_contrib, annual_rate_pct, years)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command()
def report(project_name: str, description: str) -> None:
    """Print finance report: aryubi report Family with description."""
    typer.echo(agent.finance_report(project_name, description))


if __name__ == "__main__":
    app()
