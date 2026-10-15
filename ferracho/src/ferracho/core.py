"""Core logic for Ferracho - business and marketing analyzer."""

from __future__ import annotations

import logging
from typing import Any

from ferracho.exceptions import AnalysisError, FunnelError, RiskError, SwotError, UnitEconomicsError

logger = logging.getLogger(__name__)

SWOT_KEYS: tuple[str, ...] = ("strengths", "weaknesses", "opportunities", "threats")


def _validate_str_list(values: Any, field_name: str) -> list[str]:
    """Validate a list of non-empty strings.

    Args:
        values: Candidate list value.
        field_name: Field name used in error messages.

    Returns:
        Cleaned list of stripped strings.
    """
    if not isinstance(values, list):
        raise SwotError("field " + field_name + " must be a list of strings")
    cleaned: list[str] = []
    for item in values:
        if not isinstance(item, str) or not item.strip():
            raise SwotError("field " + field_name + " must contain non-empty strings")
        cleaned.append(item.strip())
    return cleaned


def _validate_number(value: Any, field_name: str, allow_zero: bool = True) -> float:
    """Validate a single numeric value.

    Args:
        value: Candidate number.
        field_name: Field name used in error messages.
        allow_zero: Whether zero is accepted.

    Returns:
        Value converted to float.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise AnalysisError("field " + field_name + " must be a number")
    result = float(value)
    if not allow_zero and result == 0:
        raise AnalysisError("field " + field_name + " must not be zero")
    if result < 0:
        raise AnalysisError("field " + field_name + " must be >= 0")
    return result


class Ferracho:
    """Business analyzer: SWOT, funnel, unit economics, risks, audit reports."""

    def __init__(self, precision: int = 2) -> None:
        """Initialize Ferracho agent.

        Args:
            precision: Decimal places used in reports.
        """
        self.name: str = "ferracho"
        self.precision: int = max(0, int(precision))
        self.history: list[dict[str, Any]] = []
        logger.debug("Ferracho agent initialized")
    def swot_analysis(self, data: dict[str, list[str]]) -> dict[str, Any]:
        """Run SWOT analysis over four quadrants.

        Args:
            data: Mapping with strengths, weaknesses, opportunities, threats.

        Returns:
            Dict with counts, balance score and recommendation.
        """
        if not isinstance(data, dict):
            raise SwotError("data must be a dict with SWOT quadrants")
        result: dict[str, Any] = {}
        for key in SWOT_KEYS:
            raw = data.get(key, [])
            result[key] = _validate_str_list(raw, key)
        s_count = len(result["strengths"])
        w_count = len(result["weaknesses"])
        o_count = len(result["opportunities"])
        t_count = len(result["threats"])
        total = s_count + w_count + o_count + t_count
        if total == 0:
            raise SwotError("SWOT data must contain at least one item")
        positive = s_count + o_count
        negative = w_count + t_count
        balance = positive - negative
        if balance >= 2:
            verdict = "expansion"
        elif balance <= -2:
            verdict = "defense"
        else:
            verdict = "balance"
        logger.info("SWOT computed balance=%s verdict=%s", balance, verdict)
        return {
            "counts": {"strengths": s_count, "weaknesses": w_count, "opportunities": o_count, "threats": t_count},
            "total": total,
            "balance": balance,
            "verdict": verdict,
            "items": result,
        }

    def funnel_analysis(self, stages: dict[str, float]) -> dict[str, Any]:
        """Analyze a sales funnel given ordered stage volumes.

        Args:
            stages: Ordered mapping stage name to visitor count.

        Returns:
            Dict with step conversions, total conversion and bottleneck.
        """
        if not isinstance(stages, dict) or len(stages) < 2:
            raise FunnelError("stages must be a dict with at least 2 stages")
        names: list[str] = []
        values: list[float] = []
        for key, val in stages.items():
            if not isinstance(key, str) or not key.strip():
                raise FunnelError("stage names must be non-empty strings")
            if isinstance(val, bool) or not isinstance(val, (int, float)):
                raise FunnelError("stage value for " + key.strip() + " must be a number")
            if float(val) < 0:
                raise FunnelError("stage value for " + key.strip() + " must be >= 0")
            names.append(key.strip())
            values.append(float(val))
        if values[0] == 0:
            raise FunnelError("first funnel stage must be greater than zero")
        steps: list[dict[str, Any]] = []
        bottleneck = ""
        worst_rate = 101.0
        for i in range(1, len(names)):
            prev = values[i - 1]
            cur = values[i]
            rate = (cur / prev * 100.0) if prev > 0 else 0.0
            steps.append({"from": names[i - 1], "to": names[i], "rate_pct": rate})
            if rate < worst_rate:
                worst_rate = rate
                bottleneck = names[i - 1] + " -> " + names[i]
        total_rate = (values[-1] / values[0] * 100.0) if values[0] > 0 else 0.0
        logger.info("Funnel computed total=%.2f bottleneck=%s", total_rate, bottleneck)
        return {"stages": dict(zip(names, values)), "steps": steps, "total_conversion_pct": total_rate, "bottleneck": bottleneck}
    def unit_economics(self, price: float, variable_cost: float, cac: float, monthly_volume: float) -> dict[str, float]:
        """Compute unit economics for one sold unit.

        Args:
            price: Selling price per unit.
            variable_cost: Variable cost per unit.
            cac: Customer acquisition cost per unit.
            monthly_volume: Expected units per month.

        Returns:
            Dict with margin, profit per unit, monthly profit and ROMI.
        """
        try:
            p = _validate_number(price, "price")
            vc = _validate_number(variable_cost, "variable_cost")
            ac = _validate_number(cac, "cac")
            vol = _validate_number(monthly_volume, "monthly_volume")
        except AnalysisError as exc:
            raise UnitEconomicsError(str(exc)) from exc
        margin = p - vc
        profit_per_unit = margin - ac
        monthly_profit = profit_per_unit * vol
        romi = (profit_per_unit / ac * 100.0) if ac > 0 else 0.0
        breakeven = (ac / margin) if margin > 0 else 0.0
        logger.info("Unit economics profit=%.2f romi=%.2f", profit_per_unit, romi)
        return {
            "price": p,
            "variable_cost": vc,
            "cac": ac,
            "monthly_volume": vol,
            "margin": margin,
            "profit_per_unit": profit_per_unit,
            "monthly_profit": monthly_profit,
            "romi_pct": romi,
            "breakeven_factor": breakeven,
        }

    def risk_matrix(self, risks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Score risks by probability times impact.

        Args:
            risks: List of dicts with title, probability (1-5), impact (1-5).

        Returns:
            Sorted list with score and level, highest first.
        """
        if not isinstance(risks, list) or len(risks) == 0:
            raise RiskError("risks must be a non-empty list")
        scored: list[dict[str, Any]] = []
        for item in risks:
            if not isinstance(item, dict):
                raise RiskError("each risk must be a dict")
            title = item.get("title", "")
            prob = item.get("probability", 0)
            impact = item.get("impact", 0)
            if not isinstance(title, str) or not title.strip():
                raise RiskError("risk title must be a non-empty string")
            if prob not in (1, 2, 3, 4, 5) or impact not in (1, 2, 3, 4, 5):
                raise RiskError("probability and impact must be integers 1-5")
            score = int(prob) * int(impact)
            if score >= 15:
                level = "critical"
            elif score >= 8:
                level = "high"
            elif score >= 4:
                level = "medium"
            else:
                level = "low"
            scored.append({"title": title.strip(), "probability": prob, "impact": impact, "score": score, "level": level})
        scored.sort(key=lambda r: int(r["score"]), reverse=True)
        logger.info("Risk matrix scored %d risks", len(scored))
        return scored
    def audit_report(self, business_name: str, description: str, swot: dict[str, list[str]] | None = None, funnel: dict[str, float] | None = None) -> str:
        """Build a Russian business audit report.

        Args:
            business_name: Name of the business or project.
            description: Free text description of the business.
            swot: Optional SWOT quadrants.
            funnel: Optional funnel stages.

        Returns:
            Human-readable audit report in Russian.
        """
        if not isinstance(business_name, str) or not business_name.strip():
            raise AnalysisError("business_name must be a non-empty string")
        if not isinstance(description, str) or not description.strip():
            raise AnalysisError("description must be a non-empty string")
        p = self.precision

        def fmt(v: float) -> str:
            """Format float with precision."""
            return format(v, "." + str(p) + "f")

        name = business_name.strip()
        lines: list[str] = []
        lines.append("Ferracho!! Аудит: " + name)
        lines.append("Описание: " + description.strip())
        verdict = "balance"
        if swot is not None:
            try:
                sw = self.swot_analysis(swot)
            except (SwotError, AnalysisError) as exc:
                raise AnalysisError("invalid swot block: " + str(exc)) from exc
            counts = sw["counts"]
            lines.append("SWOT: S=" + str(counts["strengths"]) + " W=" + str(counts["weaknesses"]) + " O=" + str(counts["opportunities"]) + " T=" + str(counts["threats"]))
            lines.append("Баланс SWOT: " + str(sw["balance"]) + " (" + str(sw["verdict"]) + ")")
            verdict = str(sw["verdict"])
        if funnel is not None:
            try:
                fu = self.funnel_analysis(funnel)
            except FunnelError as exc:
                raise AnalysisError("invalid funnel block: " + str(exc)) from exc
            lines.append("Сквозная конверсия: " + fmt(float(fu["total_conversion_pct"])) + "%")
            lines.append("Узкое место: " + str(fu["bottleneck"]))
        if verdict == "expansion":
            lines.append("Вывод: позиция сильная - масштабируй маркетинг и продукт.")
        elif verdict == "defense":
            lines.append("Вывод: рисков больше чем опор - сначала закрой слабые места.")
        else:
            lines.append("Вывод: баланс - точечно усиль воронку и оффер.")
        lines.append("Следующий шаг: зафиксируй 3 метрики и проверь через 14 дней.")
        report = "\n".join(lines)
        self.history.append({"business": name, "verdict": verdict})
        return report

    def get_history(self) -> list[dict[str, Any]]:
        """Return audit history.

        Returns:
            List of past audit metadata dicts.
        """
        return list(self.history)


engine = Ferracho()
