# Marika

**Role:** Руководитель статистики — описательная аналитика, рост, тренды, доли и отчёты

Триггер: `марика` / `marika` (а также `统计`, `статистика марика`)

Языки ответов: RU / EN / ZH (русский, английский, китайский)

---

## Role

Marika — агент-руководитель статистики. Считает по любым числам:
среднее, медиану, разброс, прирост в %, тренд (рост/спад/флэт),
доли в % и собирает короткий отчёт на трёх языках.

---

## Knowledge

- **Descriptive:** count, sum, mean, median, min, max, range, variance, stdev
- **Growth:** absolute change + percent change (old → new)
- **Trend:** least-squares slope → up / down / flat + локализация
- **Shares:** словарь {название: значение} → {название: %} + total
- **Reports:** шаблоны RU / EN / ZH
- **Frameworks:** Python 3.10+, Typer CLI, Pydantic config

---

## Paths

```
marika/
├── src/marika/
│   ├── __init__.py      # Package exports
│   ├── cli.py           # CLI interface (typer)
│   ├── config.py        # Settings (pydantic-settings)
│   ├── core.py          # Statistics engine
│   └── exceptions.py    # Custom exceptions
├── tests/
│   └── test_core.py     # Engine tests
├── .env.example         # Config template
├── pyproject.toml       # Dependencies
└── README.md            # This file
```

---

## Learning (Distillation)

1. **Precision Learning:** запоминает удобную точность округления
2. **Lang Adaptation:** подстраивает язык отчёта под пользователя (ru/en/zh)
3. **Trend Calibration:** учится отличать шум от реального тренда
4. **Title Style:** запоминает стиль заголовков

**Distillation Process:**
- Пользователь правит отчёт → Store original + corrected pair
- Частый язык → Update default_lang
- Периодический обзор → Refine trend epsilon

---

## Memory (Distillation)

```json
{
  "user_preferences": {
    "lang": "ru",
    "precision": 2
  },
  "history": [
    {"title": "Продажи", "lang": "ru", "count": 12}
  ]
}
```

Хранится в `Marika.history` (in-memory) + при желании в JSON.
Не хранить сырые персональные данные без согласия.

---

## Charter

1. **Accuracy First:** точные цифры, без выдумок; формулы прозрачны
2. **Trilingual:** RU / EN / ZH на одинаковом уровне
3. **Validate Inputs:** пустые/нечисловые данные → понятная ошибка
4. **Privacy:** не хранить чувствительное без согласия
5. **Reliability:** graceful fallback при ошибках (typed exceptions)

---

## Installation

```bash
pip install -e .
pip install -e ".[dev]"
```

## Usage

```bash
marika describe "1,2,3,4,5"
marika growth 100 150
marika trend "1,2,3,5,8"
marika shares '{"ads": 30, "organic": 70}'
marika report "10,12,15,14,18" --lang ru
marika report "10,12,15,14,18" --lang en
marika report "10,12,15,14,18" --lang zh
```

## Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

## Testing

```bash
pytest
ruff check src tests
```
