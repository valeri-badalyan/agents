"""Tests for Aryubi finance core."""

import pytest

from aryubi.core import Aryubi
from aryubi.exceptions import (
    AnalysisError,
    BudgetError,
    CashflowError,
    InvestmentError,
    ProfitError,
)


@pytest.fixture
def agent() -> Aryubi:
    """Provide fresh Aryubi instance."""
    return Aryubi()


def test_budget_ok(agent: Aryubi) -> None:
    """Valid budget returns totals and verdict."""
    result = agent.budget_analysis(
        {"salary": 100000, "side": 20000},
        {"rent": 40000, "food": 30000, "fun": 10000},
    )
    assert result["total_income"] == pytest.approx(120000)
    assert result["total_expenses"] == pytest.approx(80000)
    assert result["balance"] == pytest.approx(40000)
    assert result["savings_rate_pct"] == pytest.approx(33.333, abs=0.01)
    assert result["verdict"] == "healthy"
    assert result["top_expense"] == "rent"


def test_budget_deficit(agent: Aryubi) -> None:
    """Expenses above income give deficit verdict."""
    result = agent.budget_analysis({"salary": 50000}, {"rent": 60000})
    assert result["verdict"] == "deficit"


def test_budget_zero_income(agent: Aryubi) -> None:
    """Zero income raises BudgetError."""
    with pytest.raises(BudgetError):
        agent.budget_analysis({"salary": 0}, {"rent": 10})


def test_budget_bad_type(agent: Aryubi) -> None:
    """Non-dict income raises BudgetError."""
    with pytest.raises(BudgetError):
        agent.budget_analysis("salary", {"rent": 10})  # type: ignore[arg-type]


def test_cashflow_ok(agent: Aryubi) -> None:
    """Cashflow computes balances and no deficit."""
    result = agent.cashflow_analysis([10000, -2000, 5000], 1000)
    assert result["balances"] == pytest.approx([11000, 9000, 14000])
    assert result["end_balance"] == pytest.approx(14000)
    assert result["deficit_month"] is None


def test_cashflow_deficit(agent: Aryubi) -> None:
    """Negative cumulative balance records deficit month."""
    result = agent.cashflow_analysis([-5000, -5000], 8000)
    assert result["deficit_month"] == 2


def test_cashflow_empty(agent: Aryubi) -> None:
    """Empty flows raise CashflowError."""
    with pytest.raises(CashflowError):
        agent.cashflow_analysis([])


def test_pnl_ok(agent: Aryubi) -> None:
    """P&L math is correct."""
    result = agent.profit_loss(100000, 40000, 30000)
    assert result["gross_profit"] == pytest.approx(60000)
    assert result["operating_profit"] == pytest.approx(30000)
    assert result["net_profit"] == pytest.approx(30000)
    assert result["net_margin_pct"] == pytest.approx(30.0)


def test_pnl_with_tax(agent: Aryubi) -> None:
    """Tax reduces net profit."""
    result = agent.profit_loss(100000, 40000, 30000, 20)
    assert result["tax_amount"] == pytest.approx(6000)
    assert result["net_profit"] == pytest.approx(24000)


def test_pnl_zero_revenue(agent: Aryubi) -> None:
    """Zero revenue raises ProfitError."""
    with pytest.raises(ProfitError):
        agent.profit_loss(0, 10, 10)


def test_invest_ok(agent: Aryubi) -> None:
    """Investment projects future value above invested."""
    result = agent.investment_growth(100000, 10000, 12, 1)
    assert result["future_value"] > result["total_invested"]
    assert result["total_invested"] == pytest.approx(220000)
    assert result["interest_earned"] > 0


def test_invest_zero_years(agent: Aryubi) -> None:
    """Zero years raise InvestmentError."""
    with pytest.raises(InvestmentError):
        agent.investment_growth(1000, 100, 10, 0)


def test_report_ok(agent: Aryubi) -> None:
    """Finance report contains name and conclusion."""
    text = agent.finance_report(
        "Family",
        "Monthly family budget",
        {"salary": 120000},
        {"rent": 40000, "food": 30000},
    )
    assert "Family" in text
    assert "Вывод" in text
    assert "Следующий шаг" in text


def test_report_pnl(agent: Aryubi) -> None:
    """Report with P&L shows margins."""
    text = agent.finance_report(
        "Shop",
        "Small retail",
        {"sales": 200000},
        {"rent": 50000},
        200000,
        80000,
        60000,
    )
    assert "Валовая прибыль" in text
    assert "Чистая прибыль" in text


def test_report_empty_name(agent: Aryubi) -> None:
    """Empty project name raises AnalysisError."""
    with pytest.raises(AnalysisError):
        agent.finance_report("", "desc")


def test_history_recorded(agent: Aryubi) -> None:
    """Reports stored in history."""
    agent.finance_report("Family", "Budget review")
    hist = agent.get_history()
    assert len(hist) == 1
    assert hist[0]["project"] == "Family"
