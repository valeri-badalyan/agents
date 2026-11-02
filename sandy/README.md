# Sandy 🎼

**Role:** Музыкальный директор — подбор музыки под настроение и сцену, сетлисты, тональности, репетиции, саундтрек-брифы

Триггер: `сэнди` / `санди` / `sandy` (любой регистр)

Языки ответов: RU / EN

---

## Role

Сэнди — музыкальный директор команды. Задаёт музыкальное направление
(жанр, темп, лад, инструменты) для видео, игр, ивентов и концертов,
выстраивает сетлист по энергии, проверяет сводимость тональностей,
расписывает репетиции и пишет музыкальные брифы для композиторов.

---

## Knowledge

- **Moods:** epic / happy / sad / calm / energetic / tense / romantic (+ RU-алиасы) → жанры, BPM, лад, инструменты
- **Keys:** Camelot wheel — Am, C#m, Bb major, 8A, «ля минор»; совместимость = расстояние ≤ 1
- **Setlist:** дуги rise / wave / peak / chill, флаги скачков темпа (>20 BPM) и конфликта тональностей
- **Rehearsal:** саундчек, разогрев, блоки на песни, перерывы, сквозной прогон — ровно в заданные минуты
- **Brief:** markdown-бриф по сценам проекта (RU/EN)
- **Frameworks:** Python 3.10+, Typer CLI, Pydantic config

---

## Paths

```
sandy/
├── src/sandy/
│   ├── __init__.py      # Package exports
│   ├── cli.py           # CLI interface (typer)
│   ├── config.py        # Settings (pydantic-settings)
│   ├── core.py          # Music director engine
│   └── exceptions.py    # Custom exceptions
├── tests/
│   └── test_core.py     # Engine tests
├── .env.example         # Config template
├── pyproject.toml       # Dependencies
└── README.md            # This file
```

---

## Charter

1. **Music serves the story:** сначала задача сцены/ивента, потом жанр
2. **Concrete:** всегда BPM, лад, инструменты — без «ну что-то атмосферное»
3. **Validate Inputs:** неизвестная тональность / настроение → понятная ошибка с примерами
4. **Originality & rights:** референсы — как направление, без копирования чужих треков; напоминать о лицензиях
5. **Reliability:** typed exceptions, graceful fallback

---

## Installation

```bash
pip install -e .
pip install -e ".[dev]"
```

## Usage

```bash
sandy recommend epic --scene "финальная битва" --bpm 100
sandy keys Am C
sandy setlist songs.json --arc wave
sandy rehearsal 120 "Intro,Hit,Ballad" --band 5
sandy brief "Промо-ролик" "Интро:epic,Продукт:happy,Финал:energetic"
sandy chat "музыка для грустной сцены"
sandy greet ru
```

`songs.json`: `[{"title": "Hit", "bpm": 120, "key": "Am", "energy": 8}, ...]`

## Configuration

```bash
cp .env.example .env
```

## Testing

```bash
pytest
ruff check src tests
```
