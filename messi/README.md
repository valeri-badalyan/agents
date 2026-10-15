# Messi

**Role:** Football Agent — тактика, тренировки, мотивация и викторины

---

## Role

Messi — агент-футболист. Разбирает схемы, составляет планы тренировок под позицию и уровень, мотивирует как настоящий капитан и проверяет знания через викторину.

---

## Knowledge

- **Formations:** 4-4-2, 4-3-3, 3-5-2, 4-2-3-1, 5-3-2 — стиль, сильные и слабые стороны
- **Training:** beginner / amateur / pro + позиции (вратарь, защитник, полузащитник, нападающий, вингер)
- **Quiz:** базовые правила футбола, офсайд, длительность матча, схемы
- **Frameworks:** Python 3.10+, Typer CLI, Pydantic config

---

## Paths

```
messi/
├── src/messi/
│   ├── __init__.py      # Package exports
│   ├── cli.py           # CLI interface (typer)
│   ├── config.py        # Settings (pydantic-settings)
│   ├── core.py          # Football engine
│   └── exceptions.py    # Custom exceptions
├── tests/
│   └── test_core.py     # Engine tests
├── .env.example         # Config template
├── pyproject.toml       # Dependencies
└── README.md            # This file
```

---

## Learning (Distillation)

Messi learns through distillation:

1. **Tactics Learning:** Запоминает какие схемы нравятся пользователю
2. **Training Adaptation:** Подстраивает нагрузку под прогресс
3. **Quiz Improvement:** Запоминает сложные вопросы для повторения
4. **Motivation Style:** Адаптирует тон под игрока

**Distillation Process:**
- Пользователь правит план → Store original + corrected pair
- После N тренировок → Update level recommendation
- Периодический обзор → Refine tactics advice

---

## Memory (Distillation)

Messi maintains memory through distillation:

1. **Training History:** Хранит прошлые планы и уровни
2. **User Preferences:** Любимая схема, позиция, уровень
3. **Quiz Scores:** Результаты викторин
4. **Favorite Advice:** Часто запрашиваемые разборы

**Memory Structure:**
```json
{
  "user_preferences": {
    "formation": "4-3-3",
    "position": "forward",
    "level": "amateur"
  },
  "history": [],
  "quiz_scores": []
}
```

---

## Charter

1. **Love the Game:** Вдохновлять играть и тренироваться
2. **Accuracy First:** Точные разборы без выдумок
3. **Safety:** Тренировки с учётом уровня, без травм
4. **Privacy:** Не хранить чувствительные данные без согласия
5. **Reliability:** Graceful fallback при ошибках

---

## Installation

```bash
pip install -e .
pip install -e ".[dev]"
```

## Usage

```bash
messi tactics 4-3-3
messi train --level amateur --position winger
messi motivate --name Лео
messi quiz
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
