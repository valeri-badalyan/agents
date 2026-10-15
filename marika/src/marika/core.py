"""Core logic for Marika — general statistics and analytics (RU/EN/ZH)."""

from __future__ import annotations

import logging
import statistics
from typing import Any

from marika.exceptions import GrowthError, ReportError, SharesError, StatisticsError, TrendError

logger = logging.getLogger(__name__)

SUPPORTED_LANGS: tuple[str, ...] = ("ru", "en", "zh")

TREND_LABELS: dict[str, dict[str, str]] = {
    "up": {"ru": "рост", "en": "upward trend", "zh": "上升趋势"},
    "down": {"ru": "спад", "en": "downward trend", "zh": "下降趋势"},
    "flat": {"ru": "стабильно", "en": "flat trend", "zh": "平稳趋势"},
}


def _validate_numbers(data: list[float], field_name: str = "data") -> list[float]:
    """Validate a non-empty list of numbers.

    Args:
        data: Values to validate.
        field_name: Name used in error messages.

    Returns:
        Cleaned list of floats.

    Raises:
        StatisticsError: If data is empty or contains non-numbers.
    """
    if not isinstance(data, list) or len(data) == 0:
        raise StatisticsError(f"{field_name} must be a non-empty list of numbers")
    cleaned: list[float] = []
    for item in data:
        if isinstance(item, bool) or not isinstance(item, (int, float)):
            raise StatisticsError(f"{field_name} must contain only numbers, got {item!r}")
        cleaned.append(float(item))
    return cleaned


def _validate_lang(lang: str) -> str:
    """Validate and normalize language code.

    Args:
        lang: Language code (ru, en, zh).

    Returns:
        Normalized lowercase code.

    Raises:
        ReportError: If language is unsupported.
    """
    if not isinstance(lang, str):
        raise ReportError("lang must be a string")
    code = lang.strip().lower()
    if code not in SUPPORTED_LANGS:
        raise ReportError(f"Unsupported lang '{lang}'. Supported: {', '.join(SUPPORTED_LANGS)}")
    return code


def _validate_number(value: float, field_name: str) -> float:
    """Validate a single numeric value.

    Args:
        value: Value to check.
        field_name: Field name for errors.

    Returns:
        Value as float.

    Raises:
        GrowthError: If value is not numeric.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise GrowthError(f"{field_name} must be a number, got {value!r}")
    return float(value)


class Marika:
    """Statistics agent: descriptive stats, growth, trends, shares, reports."""

    def __init__(self, precision: int = 2) -> None:
        """Initialize Marika agent.

        Args:
            precision: Decimal places for rounding in reports.
        """
        self.name: str = "marika"
        self.precision: int = max(0, int(precision))
        self.history: list[dict[str, Any]] = []
        logger.debug("Marika agent initialized")

    def describe(self, data: list[float]) -> dict[str, Any]:
        """Compute descriptive statistics.

        Args:
            data: List of numbers.

        Returns:
            Dict with count, sum, mean, median, min, max, stdev, variance.

        Raises:
            StatisticsError: If data is invalid.
        """
        values = _validate_numbers(data, "data")
        try:
            result: dict[str, Any] = {
                "count": len(values),
                "sum": sum(values),
                "mean": statistics.fmean(values),
                "median": statistics.median(values),
                "min": min(values),
                "max": max(values),
            }
            result["variance"] = statistics.pvariance(values) if len(values) >= 2 else 0.0
            result["stdev"] = statistics.pstdev(values) if len(values) >= 2 else 0.0
            result["range"] = result["max"] - result["min"]
            logger.info("Described %d values", len(values))
            return result
        except StatisticsError:
            raise
        except Exception as exc:
            raise StatisticsError(f"Failed to compute statistics: {exc}") from exc

    def growth_rate(self, old_value: float, new_value: float) -> dict[str, float]:
        """Compute absolute and percent change.

        Args:
            old_value: Base value.
            new_value: New value.

        Returns:
            Dict with old, new, absolute_change, percent_change.

        Raises:
            GrowthError: If inputs invalid or old value is zero.
        """
        try:
            old = _validate_number(old_value, "old_value")
            new = _validate_number(new_value, "new_value")
        except GrowthError:
            raise
        except Exception as exc:
            raise GrowthError(str(exc)) from exc
        if old == 0:
            raise GrowthError("old_value must not be zero for percent change")
        absolute = new - old
        percent = (absolute / abs(old)) * 100.0
        logger.info("Growth computed old=%s new=%s", old, new)
        return {
            "old": old,
            "new": new,
            "absolute_change": absolute,
            "percent_change": percent,
        }

    def trend(self, data: list[float]) -> dict[str, Any]:
        """Detect linear trend via least-squares slope.

        Args:
            data: Ordered list of numbers.

        Returns:
            Dict with slope, direction (up/down/flat) and labels.

        Raises:
            TrendError: If data invalid.
        """
        try:
            values = _validate_numbers(data, "data")
        except StatisticsError as exc:
            raise TrendError(str(exc)) from exc
        if len(values) < 2:
            raise TrendError("Need at least 2 points for trend analysis")
        try:
            n = len(values)
            xs = list(range(n))
            mean_x = sum(xs) / n
            mean_y = sum(values) / n
            denom = sum((x - mean_x) ** 2 for x in xs)
            slope = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, values)) / denom if denom else 0.0
            eps = 1e-9
            direction = "up" if slope > eps else ("down" if slope < -eps else "flat")
            logger.info("Trend computed slope=%s direction=%s", slope, direction)
            return {"slope": slope, "direction": direction, "labels": dict(TREND_LABELS[direction])}
        except TrendError:
            raise
        except Exception as exc:
            raise TrendError(f"Failed to compute trend: {exc}") from exc

    def shares(self, parts: dict[str, float]) -> dict[str, Any]:
        """Compute percentage shares of named parts.

        Args:
            parts: Mapping name -> value.

        Returns:
            Dict with total and breakdown {name: percent}.

        Raises:
            SharesError: If input invalid or total is zero.
        """
        if not isinstance(parts, dict) or len(parts) == 0:
            raise SharesError("parts must be a non-empty dict")
        total = 0.0
        for key, val in parts.items():
            if not isinstance(key, str) or not key.strip():
                raise SharesError("part names must be non-empty strings")
            if isinstance(val, bool) or not isinstance(val, (int, float)):
                raise SharesError(f"Value for '{key}' must be a number")
            if float(val) < 0:
                raise SharesError(f"Value for '{key}' must be >= 0")
            total += float(val)
        if total == 0:
            raise SharesError("Total must not be zero")
        breakdown = {k.strip(): (float(v) / total) * 100.0 for k, v in parts.items()}
        logger.info("Shares computed total=%s", total)
        return {"total": total, "breakdown": breakdown}

    def summary_report(self, data: list[float], lang: str = "ru", title: str = "") -> str:
        """Build a short localized statistics report.

        Args:
            data: List of numbers.
            lang: One of ru, en, zh.
            title: Optional report title.

        Returns:
            Human-readable report string.

        Raises:
            ReportError: If lang unsupported; StatisticsError if data invalid.
        """
        code = _validate_lang(lang)
        stats = self.describe(data)
        trend_info = self.trend(data) if len(data) >= 2 else {"direction": "flat", "slope": 0.0}
        direction = str(trend_info["direction"])
        p = self.precision

        def fmt(v: float) -> str:
            """Format float with precision."""
            return f"{v:.{p}f}"

        try:
            if code == "ru":
                head = title.strip() or "Отчёт по статистике"
                lines = [
                    f"📊 {head}",
                    f"Количество: {stats['count']}, Сумма: {fmt(stats['sum'])}",
                    f"Среднее: {fmt(stats['mean'])}, Медиана: {fmt(stats['median'])}",
                    f"Мин: {fmt(stats['min'])}, Макс: {fmt(stats['max'])}, Размах: {fmt(stats['range'])}",
                    f"Ст. отклонение: {fmt(stats['stdev'])}, Дисперсия: {fmt(stats['variance'])}",
                    f"Тренд: {TREND_LABELS[direction]['ru']} (наклон {fmt(float(trend_info['slope']))})",
                ]
            elif code == "en":
                head = title.strip() or "Statistics Report"
                lines = [
                    f"📊 {head}",
                    f"Count: {stats['count']}, Sum: {fmt(stats['sum'])}",
                    f"Mean: {fmt(stats['mean'])}, Median: {fmt(stats['median'])}",
                    f"Min: {fmt(stats['min'])}, Max: {fmt(stats['max'])}, Range: {fmt(stats['range'])}",
                    f"Std: {fmt(stats['stdev'])}, Variance: {fmt(stats['variance'])}",
                    f"Trend: {TREND_LABELS[direction]['en']} (slope {fmt(float(trend_info['slope']))})",
                ]
            else:
                head = title.strip() or "统计报告"
                lines = [
                    f"📊 {head}",
                    f"数量: {stats['count']}, 总和: {fmt(stats['sum'])}",
                    f"平均值: {fmt(stats['mean'])}, 中位数: {fmt(stats['median'])}",
                    f"最小值: {fmt(stats['min'])}, 最大值: {fmt(stats['max'])}, 极差: {fmt(stats['range'])}",
                    f"标准差: {fmt(stats['stdev'])}, 方差: {fmt(stats['variance'])}",
                    f"趋势: {TREND_LABELS[direction]['zh']} (斜率 {fmt(float(trend_info['slope']))})",
                ]
            report = "\n".join(lines)
            self.history.append({"title": head, "lang": code, "count": stats["count"]})
            return report
        except (StatisticsError, ReportError):
            raise
        except Exception as exc:
            raise ReportError(f"Failed to build report: {exc}") from exc

    def get_history(self) -> list[dict[str, Any]]:
        """Return report history.

        Returns:
            List of past report metadata dicts.
        """
        return list(self.history)


engine = Marika()
