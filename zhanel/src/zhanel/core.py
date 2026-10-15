"""Core logic for Zhanel — marketing strategist and copywriter."""

from __future__ import annotations

import logging
import random

from zhanel.exceptions import AuditError, ContentPlanError, CopyError, StrategyError

logger = logging.getLogger(__name__)

AUDIENCE_SEGMENTS: list[dict[str, str]] = [
    {
        "segment": "Новички",
        "jtbd": "Разобраться быстро и без стресса",
        "pain": "Боятся ошибиться и переплатить",
        "message": "Просто, по шагам, с поддержкой",
    },
    {
        "segment": "Практики",
        "jtbd": "Получить результат быстрее",
        "pain": "Устали от воды и общих советов",
        "message": "Конкретика, цифры, кейсы",
    },
    {
        "segment": "Эстеты / фанаты",
        "jtbd": "Принадлежать к бренду и делиться",
        "pain": "Боятся безвкусицы и навязчивости",
        "message": "Эстетика, история, комьюнити",
    },
]

POSITIONING_TEMPLATES: list[str] = [
    "{product} для {audience}, которые хотят {benefit} без {pain}",
    "{product} — {benefit} за {timeframe} для {audience}",
    "Единственный {product}, где {differentiator}",
]

CONTENT_RUBRICS: list[dict[str, str]] = [
    {"rubric": "Польза", "share": "40%", "example": "Гайд / разбор / инструкция"},
    {"rubric": "Продажа", "share": "20%", "example": "Кейс / отзыв / оффер"},
    {"rubric": "Вовлечение", "share": "20%", "example": "Опрос / мем / закулисье"},
    {"rubric": "Личность бренда", "share": "20%", "example": "История / ценности / команда"},
]

LAUNCH_STEPS: list[str] = [
    "1. Позиционирование: кому, зачем, почему мы (1 страница)",
    "2. Оффер и цены: 2-3 тарифа, якорь, гарантия",
    "3. Посадочная: заголовок с выгодой + 3 доказательства + CTA",
    "4. Контент-прогрев на 2 недели: боль → решение → кейсы → оффер",
    "5. Каналы: 1 основной + 1 запасной (Telegram + Reels / VK / TikTok)",
    "6. Запуск: лид-магнит → вебинар/разбор → продажи 5-7 дней",
    "7. Аналитика: CTR, заявки, конверсия в оплату, CAC, LTV",
]

KPI_BY_GOAL: dict[str, list[str]] = {
    "awareness": ["Охват", "Показы", "Share of voice", "Запоминаемость"],
    "leads": ["CTR", "CPL", "Конверсия в заявку", "MQL"],
    "sales": ["Конверсия в оплату", "CAC", "Средний чек", "LTV / CAC"],
}


def _validate_text(value: str, field_name: str) -> str:
    """Validate non-empty user input."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


class Zhanel:
    """Marketing agent: strategy, copywriting, content-plans and audits."""

    def __init__(self) -> None:
        """Initialize Zhanel agent."""
        self.name: str = "zhanel"
        logger.debug("Zhanel agent initialized")

    def analyze_audience(self, product: str) -> dict[str, object]:
        """Segment target audience for a product.

        Args:
            product: Product or service description.

        Returns:
            Dict with product and 3 segments.

        Raises:
            StrategyError: If product is empty.
        """
        try:
            prod = _validate_text(product, "product")
        except ValueError as exc:
            raise StrategyError(str(exc)) from exc
        logger.info("Analyzed audience for %s", prod)
        return {"product": prod, "segments": [dict(s) for s in AUDIENCE_SEGMENTS]}

    def positioning(self, product: str, audience: str, benefit: str) -> dict[str, str]:
        """Build USP / positioning statement.

        Args:
            product: Product name.
            audience: Target audience.
            benefit: Key benefit.

        Returns:
            Dict with usp string and logic explanation.

        Raises:
            StrategyError: If inputs are invalid.
        """
        try:
            prod = _validate_text(product, "product")
            aud = _validate_text(audience, "audience")
            ben = _validate_text(benefit, "benefit")
        except ValueError as exc:
            raise StrategyError(str(exc)) from exc
        usp = f"{prod} для {aud}, которые хотят {ben} — без воды и переплат."
        logic = "Логика: кому + какая выгода + отстройка от боли (цена/сложность)."
        logger.info("Built positioning for %s", prod)
        return {"usp": usp, "logic": logic}

    def ad_copy(self, product: str, angle: str = "all") -> dict[str, object]:
        """Generate 3 ad headlines with different angles.

        Args:
            product: Product name.
            angle: One of pain, benefit, provocative, all.

        Returns:
            Dict with list of variants and logic notes.

        Raises:
            CopyError: If product or angle is invalid.
        """
        try:
            prod = _validate_text(product, "product")
            ang = _validate_text(angle, "angle").lower()
        except ValueError as exc:
            raise CopyError(str(exc)) from exc
        variants: dict[str, dict[str, str]] = {
            "pain": {
                "headline": f"Устала сливать деньги на {prod} без результата?",
                "logic": "Угол боли: бьём в проблему, обещаем разбор.",
            },
            "benefit": {
                "headline": f"{prod}: первые заявки уже на этой неделе",
                "logic": "Угол выгоды: конкретный результат + срок.",
            },
            "provocative": {
                "headline": f"Хватит делать {prod} по-старому. Вот как надо",
                "logic": "Угол провокации: ломаем шаблон, даём новый взгляд.",
            },
        }
        if ang != "all" and ang not in variants:
            raise CopyError(f"Unknown angle '{ang}'. Supported: pain, benefit, provocative, all")
        picked = variants if ang == "all" else {ang: variants[ang]}
        logger.info("Generated ad copy for %s angle=%s", prod, ang)
        return {"product": prod, "variants": picked}

    def slogan(self, business: str, seed: int | None = None) -> dict[str, object]:
        """Generate 5 slogan options.

        Args:
            business: Business / brand description.
            seed: Optional seed for deterministic shuffle.

        Returns:
            Dict with slogans list.

        Raises:
            CopyError: If business is empty.
        """
        try:
            biz = _validate_text(business, "business")
        except ValueError as exc:
            raise CopyError(str(exc)) from exc
        base = [
            f"{biz} — по делу, без воды",
            f"{biz}, который работает на тебя",
            f"Попробуй {biz} один раз — и поймёшь",
            f"{biz}: результат, а не обещания",
            f"Твой {biz} — твои правила",
            f"С {biz} проще, чем кажется",
            f"{biz} — выбирай лучшее",
        ]
        rng = random.Random(seed)
        rng.shuffle(base)
        logger.info("Generated slogans for %s", biz)
        return {"business": biz, "slogans": base[:5]}

    def naming(self, concept: str, seed: int | None = None) -> dict[str, object]:
        """Generate 7 naming options for a concept.

        Args:
            concept: Business concept description.
            seed: Optional seed for deterministic output.

        Returns:
            Dict with names and check advice.

        Raises:
            CopyError: If concept is empty.
        """
        try:
            conc = _validate_text(concept, "concept")
        except ValueError as exc:
            raise CopyError(str(exc)) from exc
        first_word = conc.split()[0].strip(" ,.!?").capitalize()
        pool = [
            first_word,
            f"{first_word}ka",
            f"{first_word}Lab",
            f"Pro{first_word}",
            f"{first_word}&Co",
            f"True{first_word}",
            f"{first_word}Point",
            f"My{first_word}",
        ]
        rng = random.Random(seed)
        rng.shuffle(pool)
        logger.info("Generated naming for %s", conc)
        return {
            "concept": conc,
            "names": pool[:7],
            "check": "Проверь: занятость в соцсетях, домен .ru/.kz, ассоциации на русском и казахском.",
        }

    def content_plan(self, brand: str, weeks: int = 4) -> dict[str, object]:
        """Build a weekly content plan.

        Args:
            brand: Brand / niche description.
            weeks: Number of weeks (1-12).

        Returns:
            Dict with rubrics and plan by weeks.

        Raises:
            ContentPlanError: If inputs are invalid.
        """
        try:
            br = _validate_text(brand, "brand")
        except ValueError as exc:
            raise ContentPlanError(str(exc)) from exc
        if not isinstance(weeks, int) or not 1 <= weeks <= 12:
            raise ContentPlanError("weeks must be int 1..12")
        plan: list[dict[str, str]] = []
        days = ["Пн", "Ср", "Пт", "Вс"]
        rubric_cycle = ["Польза", "Вовлечение", "Продажа", "Личность бренда"]
        for w in range(1, weeks + 1):
            for i, day in enumerate(days):
                rubric = rubric_cycle[(w + i) % len(rubric_cycle)]
                plan.append(
                    {
                        "week": f"Неделя {w}",
                        "day": day,
                        "rubric": rubric,
                        "topic": f"{br}: {rubric.lower()} — тема {w}.{i + 1}",
                    }
                )
        logger.info("Built content plan brand=%s weeks=%d", br, weeks)
        return {
            "brand": br,
            "weeks": weeks,
            "rubrics": [dict(r) for r in CONTENT_RUBRICS],
            "plan": plan,
        }

    def launch_checklist(self, product: str) -> dict[str, object]:
        """Return go-to-market launch checklist.

        Args:
            product: Product name.

        Returns:
            Dict with steps list.

        Raises:
            StrategyError: If product is empty.
        """
        try:
            prod = _validate_text(product, "product")
        except ValueError as exc:
            raise StrategyError(str(exc)) from exc
        logger.info("Built launch checklist for %s", prod)
        return {"product": prod, "steps": list(LAUNCH_STEPS)}

    def kpi(self, goal: str = "sales") -> dict[str, object]:
        """Suggest KPI set for a goal.

        Args:
            goal: One of awareness, leads, sales.

        Returns:
            Dict with goal and metrics.

        Raises:
            StrategyError: If goal unknown.
        """
        try:
            g = _validate_text(goal, "goal").lower()
        except ValueError as exc:
            raise StrategyError(str(exc)) from exc
        if g not in KPI_BY_GOAL:
            raise StrategyError(f"Unknown goal '{g}'. Supported: {', '.join(sorted(KPI_BY_GOAL))}")
        return {"goal": g, "metrics": list(KPI_BY_GOAL[g])}

    def audit_idea(self, idea: str) -> dict[str, str]:
        """Honestly audit a marketing idea.

        Args:
            idea: Idea description.

        Returns:
            Dict with verdict and reasoning.

        Raises:
            AuditError: If idea is empty.
        """
        try:
            text = _validate_text(idea, "idea")
        except ValueError as exc:
            raise AuditError(str(exc)) from exc
        low = text.lower()
        weak_signals = ["все", "всегда", "гарантия", "вирусный", "быстро разбогатеть", "без бюджета"]
        found = [s for s in weak_signals if s in low]
        if found:
            verdict = "Эта идея, скорее всего, не сработает как есть."
            reasoning = (
                f"Слабые сигналы: {', '.join(found)}. "
                "Слишком общее обещание, нет сегмента и оффера. "
                "Уточни: кому, какая боль, какой первый шаг и как меряешь результат."
            )
        elif len(text) < 30:
            verdict = "Идея сырая — нужна конкретика."
            reasoning = "Опиши продукт, аудиторию и цель (лиды/продажи/охват). Тогда дам 3 рабочих варианта."
        else:
            verdict = "Идея рабочая, если докрутить."
            reasoning = (
                "Сильная сторона: есть замысел. Дальше: сегмент → оффер → 1 канал → "
                "тест на малом бюджете 5-7 дней → замер CTR/заявок."
            )
        logger.info("Audited idea len=%d", len(text))
        return {"idea": text, "verdict": verdict, "reasoning": reasoning}


engine = Zhanel()
