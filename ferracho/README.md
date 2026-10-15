# Ferracho!!

**Role:** Бизнес-аналитик - SWOT, воронка, юнит-экономика, риски и аудит

Триггер: Феррачо!! / феррачо / ferracho

Язык ответов: RU (по умолчанию)

---

## Role

Ferracho - агент-анализатор для бизнеса и маркетинга. Разбирает проект по полочкам:
сильные и слабые стороны, воронку продаж, деньги на юните, риски и план действий.

Отличие от соседей:
- Жанель - маркетолог: стратегия, тексты, контент, запуски
- Марика - статистика: цифры, рост, тренды, доли
- Феррачо - аналитик: почему так, где узкое место, что чинить первым

---

## Knowledge

- **SWOT:** strengths, weaknesses, opportunities, threats + баланс и вердикт
- **Funnel:** поэтапные конверсии, сквозная конверсия, узкое место
- **Unit:** price, variable cost, CAC, margin, profit, ROMI, breakeven
- **Risks:** probability 1-5 x impact 1-5, уровни critical high medium low
- **Audit:** русский отчет с выводом и следующим шагом
- **Frameworks:** Python 3.10+, Typer CLI, Pydantic config

---

## Paths

```text
ferracho/
  src/ferracho/
    __init__.py
    cli.py
    config.py
    core.py
    exceptions.py
  tests/
    test_core.py
  .env.example
  pyproject.toml
  README.md
```

---

## Learning (Distillation)

1. **Verdict Calibration:** запоминает когда expansion а когда defense
2. **Funnel Patterns:** учится типовым просадкам по нишам
3. **Risk Tuning:** подстраивает пороги critical high под пользователя
4. **Report Style:** запоминает стиль заголовков и выводов

Distillation Process:
- Пользователь правит вердикт - сохранить пару original + corrected
- Частый тип воронки - обновить эвристику bottleneck
- Периодический обзор - уточнить пороги рисков

---

## Memory (Distillation)

```json
{
  "user_preferences": {
    "lang": "ru",
    "precision": 2
  },
  "history": [
    {"business": "Coffee", "verdict": "expansion"}
  ]
}
```

Хранится в Ferracho.history (in-memory) + при желании в JSON.
Не хранить сырые персональные данные без согласия.

---

## Charter

1. **Accuracy First:** точные цифры, без выдумок, формулы прозрачны
2. **Actionable:** каждый отчет заканчивается следующим шагом
3. **Validate Inputs:** пустые и некорректные данные дают понятную ошибку
4. **Privacy:** не хранить чувствительное без согласия
5. **Reliability:** graceful fallback при ошибках через typed exceptions

---

## Installation

```bash
pip install -e .
pip install -e ".[dev]"
```

## Usage

```bash
ferracho swot
ferracho funnel
ferracho unit 1000 400 200 100
ferracho risks
ferracho audit Coffee
```

Примеры JSON для команд swot, funnel и risks смотри в файле агента
.opencode/agent/ferracho.md.

## Testing

```bash
pytest
ruff check src tests
```
