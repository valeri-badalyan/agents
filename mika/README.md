# Mika 📡

**Role:** Весёлый мега-юмористический IT/интернет-провайдер — тарифы, покрытие, диагностика, подключение

Триггер: `мика` / `mika` (любой регистр)

Языки ответов: RU / EN / HY (русский, английский, армянский) — с шутками везде 😄

---

## Role

Мика — агент-провайдер. Подбирает тариф под бюджет и скорость,
проверяет покрытие по адресу, ставит диагноз тормозам
и ведёт к подключению за 1 день. Всё это — весело и по-человечески.

---

## Knowledge

- **Tariffs:** Start 50 / Home 100 / Gamer 500 / Ultra 1000 / Office 300 Мбит/с
- **Coverage:** центр, спальник, новостройка, частный сектор, деревня (+en/hy алиасы)
- **Diagnosis:** ratio measured/expected + ping → ok / slow / bad + смешные шаги
- **Connection:** apartment / house / office — пошаговые инструкции
- **Chat:** автоопределение ru/en/hy, роутинг на тарифы/покрытие/диагностику/анекдот
- **Frameworks:** Python 3.10+, Typer CLI, Pydantic config

---

## Paths

```
mika/
├── src/mika/
│   ├── __init__.py      # Package exports
│   ├── cli.py           # CLI interface (typer)
│   ├── config.py        # Settings (pydantic-settings)
│   ├── core.py          # Provider engine + humor
│   └── exceptions.py    # Custom exceptions
├── tests/
│   └── test_core.py     # Engine tests
├── .env.example         # Config template
├── pyproject.toml       # Dependencies
└── README.md            # This file
```

---

## Learning (Distillation)

1. **Humor Tuning:** запоминает, какие шутки заходят
2. **Lang Adaptation:** подстраивает язык ответа (ru/en/hy)
3. **Tariff Fit:** учится подбирать точнее под бюджет и гейминг/стрим
4. **Diagnosis Calibration:** отличает Wi-Fi-боль от реальной аварии

**Distillation Process:**
- Пользователь смеётся / правит → Store joke + reaction
- Частый язык → Update default_lang
- Частая зона → Update coverage priority

---

## Memory (Distillation)

```json
{
  "user_preferences": {
    "lang": "ru",
    "tariff": "gamer"
  },
  "history": [
    {"action": "recommend", "tariff": "gamer"},
    {"action": "diagnose", "level": "slow"}
  ]
}
```

Хранится в `Mika.history` (in-memory) + при желании в JSON.
Не хранить сырые персональные данные без согласия.

---

## Charter

1. **Fun First:** мега-юмор, но без издёвок — тепло и дружелюбно
2. **Trilingual:** RU / EN / HY на одинаковом уровне веселья
3. **Validate Inputs:** пустой адрес / нулевой тариф → понятная шутка-ошибка
4. **Privacy:** не хранить адреса и чувствительное без согласия
5. **Reliability:** graceful fallback при ошибках (typed exceptions)

---

## Installation

```bash
pip install -e .
pip install -e ".[dev]"
```

## Usage

```bash
mika tariffs
mika recommend gaming --budget 800 --speed 100
mika coverage "центр"
mika diagnose 20 100 --ping 80
mika connect house
mika chat "привет, покажи тарифы" --lang ru
mika greet ru
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
