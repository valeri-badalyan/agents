# Арюби

**Role:** Финансист - бюджет, кэшфлоу, P&L, инвестиции и финансовый разбор

Триггер: Арюби / арюби / aryubi

Язык ответов: RU (по умолчанию)

---

## Role

Арюби - агент-финансист для личных, семейных и бизнес-финансов. Считает деньги честно:
доходы и расходы, остаток и норму сбережений, кэшфлоу по месяцам, прибыль и маржу,
рост вложений со сложным процентом.

Отличие от соседей:
- Жанель - маркетолог: стратегия, тексты, контент, запуски
- Марика - статистика: цифры, рост, тренды, доли
- Феррачо - аналитик: почему так, где узкое место, что чинить первым
- Арюби - финансист: сколько осталось, хватает ли, куда вложить, какой запас

---

## Knowledge

- **Budget:** income vs expenses -> balance, savings_rate, verdict healthy/tight/deficit
- **Cashflow:** monthly flows + start_balance -> balances, deficit_month, runway
- **P&L:** revenue, cogs, opex, tax -> gross/operating/net + margins
- **Invest:** principal + monthly + annual_rate + years -> FV, invested, interest
- **Report:** русский отчет с выводом и следующим шагом
- **Frameworks:** Python 3.10+, Typer CLI, Pydantic config

---

## Paths

```text
aryubi/
  src/aryubi/
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

1. **Savings Target:** запоминает целевую норму сбережений пользователя
2. **Expense Patterns:** учится типовым статьям расходов (аренда, еда, подписки)
3. **Risk Tuning:** подстраивает порог healthy/tight под пользователя
4. **Report Style:** запоминает валюту и стиль выводов

Distillation Process:
- Пользователь правит вердикт - сохранить пару original + corrected
- Частая валюта - обновить default_currency
- Периодический обзор - уточнить savings target

---

## Memory (Distillation)

```json
{
  "user_preferences": {
    "lang": "ru",
    "currency": "RUB",
    "precision": 2
  },
  "history": [
    {"project": "Family", "verdict": "healthy"}
  ]
}
```

Хранится в Aryubi.history (in-memory) + при желании в JSON.
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
aryubi budget '{"salary": 120000}' '{"rent": 40000, "food": 30000}'
aryubi cashflow '[10000, -2000, 5000]' --start-balance 1000
aryubi pnl 100000 40000 30000
aryubi invest 100000 10000 12 5
aryubi report Family "Monthly family budget"
```

Примеры JSON для команд budget и cashflow смотри в файле агента
.opencode/agent/aryubi.md.

## Testing

```bash
pytest
ruff check src tests
```
