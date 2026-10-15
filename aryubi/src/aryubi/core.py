"""Core logic for Aryubi - finance agent: budget, cashflow, P&L, investments, audit."""

from __future__ import annotations

import logging
from typing import Any

from aryubi.exceptions import (
    AnalysisError,
    BudgetError,
    CashflowError,
    InvestmentError,
    ProfitError,
)

logger = logging.getLogger(__name__)


def _validate_number(value: Any, field_name: str) -> float:
    """Validate a single numeric value.

    Args:
        value: Candidate number.
        field_name: Field name used in error messages.

    Returns:
        Value converted to float.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise AnalysisError("field " + field_name + " must be a number")
    result = float(value)
    if result < 0:
        raise AnalysisError("field " + field_name + " must be >= 0")
    return result


def _validate_str_amount_map(data: Any, label: str) -> dict[str, float]:
    """Validate a mapping of name to non-negative amount.

    Args:
        data: Candidate mapping.
        label: Label used in error messages.

    Returns:
        Cleaned mapping of stripped names to floats.
    """
    if not isinstance(data, dict) or len(data) == 0:
        raise AnalysisError(label + " must be a non-empty dict of name to amount")
    cleaned: dict[str, float] = {}
    for key, val in data.items():
        if not isinstance(key, str) or not key.strip():
            raise AnalysisError(label + " keys must be non-empty strings")
        try:
            amount = _validate_number(val, label + "." + key.strip())
        except AnalysisError as exc:
            raise AnalysisError(str(exc)) from exc
        cleaned[key.strip()] = amount
    return cleaned


class Aryubi:
    """Finance agent: budget, cashflow, P&L, investments, finance reports."""

    def __init__(self, precision: int = 2, currency: str = "RUB") -> None:
        """Initialize Aryubi agent.

        Args:
            precision: Decimal places used in reports.
            currency: Default currency code shown in reports.
        """
        self.name: str = "aryubi"
        self.precision: int = max(0, int(precision))
        self.currency: str = currency if isinstance(currency, str) and currency.strip() else "RUB"
        self.history: list[dict[str, Any]] = []
        logger.debug("Aryubi agent initialized")

    def budget_analysis(self, income: dict[str, float], expenses: dict[str, float]) -> dict[str, Any]:
        """Compare income vs expenses: surplus/deficit and savings rate.

        Args:
            income: Mapping of income source to amount.
            expenses: Mapping of expense category to amount.

        Returns:
            Dict with totals, balance, savings rate and top expense.
        """
        try:
            clean_income = _validate_str_amount_map(income, "income")
            clean_expenses = _validate_str_amount_map(expenses, "expenses")
        except AnalysisError as exc:
            raise BudgetError(str(exc)) from exc
        total_income = sum(clean_income.values())
        total_expenses = sum(clean_expenses.values())
        if total_income == 0:
            raise BudgetError("total income must be greater than zero")
        balance = total_income - total_expenses
        savings_rate = balance / total_income * 100.0
        top_expense = max(clean_expenses.items(), key=lambda kv: kv[1])[0]
        if savings_rate >= 20:
            verdict = "healthy"
        elif savings_rate >= 0:
            verdict = "tight"
        else:
            verdict = "deficit"
        logger.info("Budget computed balance=%.2f verdict=%s", balance, verdict)
        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "balance": balance,
            "savings_rate_pct": savings_rate,
            "top_expense": top_expense,
            "verdict": verdict,
            "income": clean_income,
            "expenses": clean_expenses,
        }

    def cashflow_analysis(self, flows: list[float], start_balance: float = 0) -> dict[str, Any]:
        """Analyze monthly net cashflows: cumulative balance and runway.

        Args:
            flows: Ordered list of monthly net flows (can be negative).
            start_balance: Cash on hand before the first month.

        Returns:
            Dict with end balance, min balance, deficit month and runway.
        """
        if not isinstance(flows, list) or len(flows) == 0:
            raise CashflowError("flows must be a non-empty list of monthly net flows")
        for i, val in enumerate(flows):
            if isinstance(val, bool) or not isinstance(val, (int, float)):
                raise CashflowError("flow at index " + str(i) + " must be a number")
        if isinstance(start_balance, bool) or not isinstance(start_balance, (int, float)):
            raise CashflowError("start_balance must be a number")
        if float(start_balance) < 0:
            raise CashflowError("start_balance must be >= 0")
        running = float(start_balance)
        balances: list[float] = []
        deficit_month: int | None = None
        for idx, val in enumerate(flows):
            running += float(val)
            balances.append(running)
            if running < 0 and deficit_month is None:
                deficit_month = idx + 1
        avg_burn = sum(-float(v) for v in flows if float(v) < 0) / len(flows)
        runway: float | None = None
        if avg_burn > 0 and balances[-1] >= 0:
            runway = balances[-1] / avg_burn
        logger.info("Cashflow computed end=%.2f deficit=%s", balances[-1], deficit_month)
        return {
            "start_balance": float(start_balance),
            "flows": [float(v) for v in flows],
            "balances": balances,
            "end_balance": balances[-1],
            "min_balance": min(balances),
            "deficit_month": deficit_month,
            "runway_months": runway,
        }

    def profit_loss(self, revenue: float, cogs: float, opex: float, tax_rate_pct: float = 0) -> dict[str, float]:
        """Compute simple P&L: gross, operating and net profit with margins.

        Args:
            revenue: Total revenue.
            cogs: Cost of goods sold.
            opex: Operating expenses.
            tax_rate_pct: Tax rate in percent (0-100).

        Returns:
            Dict with gross/operating/net profit and margins.
        """
        try:
            rev = _validate_number(revenue, "revenue")
            cogs_v = _validate_number(cogs, "cogs")
            opex_v = _validate_number(opex, "opex")
            tax = _validate_number(tax_rate_pct, "tax_rate_pct")
        except AnalysisError as exc:
            raise ProfitError(str(exc)) from exc
        if rev == 0:
            raise ProfitError("revenue must be greater than zero")
        if tax > 100:
            raise ProfitError("tax_rate_pct must be between 0 and 100")
        gross = rev - cogs_v
        operating = gross - opex_v
        tax_amount = operating * tax / 100.0 if operating > 0 else 0.0
        net = operating - tax_amount
        logger.info("P&L computed net=%.2f margin=%.2f", net, net / rev * 100.0)
        return {
            "revenue": rev,
            "cogs": cogs_v,
            "opex": opex_v,
            "tax_rate_pct": tax,
            "tax_amount": tax_amount,
            "gross_profit": gross,
            "operating_profit": operating,
            "net_profit": net,
            "gross_margin_pct": gross / rev * 100.0,
            "operating_margin_pct": operating / rev * 100.0,
            "net_margin_pct": net / rev * 100.0,
        }

    def investment_growth(
        self, principal: float, monthly_contrib: float, annual_rate_pct: float, years: float
    ) -> dict[str, float]:
        """Project investment growth with monthly compounding.

        Args:
            principal: Starting capital.
            monthly_contrib: Monthly contribution.
            annual_rate_pct: Annual return rate in percent (>= 0).
            years: Horizon in years (> 0).

        Returns:
            Dict with future value, total invested and interest earned.
        """
        try:
            pv = _validate_number(principal, "principal")
            pmt = _validate_number(monthly_contrib, "monthly_contrib")
            rate = _validate_number(annual_rate_pct, "annual_rate_pct")
            yrs = _validate_number(years, "years")
        except AnalysisError as exc:
            raise InvestmentError(str(exc)) from exc
        if yrs <= 0:
            raise InvestmentError("years must be greater than zero")
        if rate > 100:
            raise InvestmentError("annual_rate_pct looks unrealistic (> 100)")
        months = round(yrs * 12)
        if months == 0:
            raise InvestmentError("years must cover at least one month")
        monthly_rate = rate / 100.0 / 12.0
        fv = pv
        if monthly_rate > 0:
            fv = pv * (1 + monthly_rate) ** months + pmt * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        else:
            fv = pv + pmt * months
        invested = pv + pmt * months
        interest = fv - invested
        logger.info("Investment projected fv=%.2f interest=%.2f", fv, interest)
        return {
            "principal": pv,
            "monthly_contrib": pmt,
            "annual_rate_pct": rate,
            "years": yrs,
            "months": float(months),
            "future_value": fv,
            "total_invested": invested,
            "interest_earned": interest,
        }

    def finance_report(
        self,
        project_name: str,
        description: str,
        income: dict[str, float] | None = None,
        expenses: dict[str, float] | None = None,
        revenue: float | None = None,
        cogs: float | None = None,
        opex: float | None = None,
    ) -> str:
        """Build a Russian finance report with conclusion and next step.

        Args:
            project_name: Name of person, family or business budget.
            description: Free text description of the finances.
            income: Optional income mapping for budget block.
            expenses: Optional expenses mapping for budget block.
            revenue: Optional revenue for P&L block.
            cogs: Optional COGS for P&L block.
            opex: Optional opex for P&L block.

        Returns:
            Human-readable finance report in Russian.
        """
        if not isinstance(project_name, str) or not project_name.strip():
            raise AnalysisError("project_name must be a non-empty string")
        if not isinstance(description, str) or not description.strip():
            raise AnalysisError("description must be a non-empty string")
        p = self.precision

        def fmt(v: float) -> str:
            """Format float with precision."""
            return format(v, "." + str(p) + "f")

        name = project_name.strip()
        lines: list[str] = []
        lines.append("Арюби. Финансовый разбор: " + name)
        lines.append("Описание: " + description.strip())
        verdict = "tight"
        if income is not None or expenses is not None:
            if income is None or expenses is None:
                raise AnalysisError("income and expenses must be provided together")
            try:
                b = self.budget_analysis(income, expenses)
            except (BudgetError, AnalysisError) as exc:
                raise AnalysisError("invalid budget block: " + str(exc)) from exc
            lines.append("Доходы: " + fmt(float(b["total_income"])) + " " + self.currency)
            lines.append("Расходы: " + fmt(float(b["total_expenses"])) + " " + self.currency)
            lines.append("Остаток: " + fmt(float(b["balance"])) + " " + self.currency)
            lines.append("Норма сбережений: " + fmt(float(b["savings_rate_pct"])) + "%")
            lines.append("Главная статья расходов: " + str(b["top_expense"]))
            verdict = str(b["verdict"])
        if revenue is not None or cogs is not None or opex is not None:
            if revenue is None or cogs is None or opex is None:
                raise AnalysisError("revenue, cogs and opex must be provided together")
            try:
                pl = self.profit_loss(revenue, cogs, opex)
            except ProfitError as exc:
                raise AnalysisError("invalid P&L block: " + str(exc)) from exc
            lines.append("Валовая прибыль: " + fmt(float(pl["gross_profit"])) + " (" + fmt(float(pl["gross_margin_pct"])) + "%)")
            lines.append("Чистая прибыль: " + fmt(float(pl["net_profit"])) + " (" + fmt(float(pl["net_margin_pct"])) + "%)")
        if verdict == "healthy":
            lines.append("Вывод: финансы здоровы - держи норму сбережений и инвестируй излишек.")
        elif verdict == "deficit":
            lines.append("Вывод: дефицит - сначала режь главную статью расходов.")
        else:
            lines.append("Вывод: впритык - подними норму сбережений до 20%.")
        lines.append("Следующий шаг: зафиксируй 3 цифры месяца и проверь через 30 дней.")
        report = "\n".join(lines)
        self.history.append({"project": name, "verdict": verdict})
        return report

    def get_history(self) -> list[dict[str, Any]]:
        """Return finance report history.

        Returns:
            List of past report metadata dicts.
        """
        return list(self.history)


engine = Aryubi()
