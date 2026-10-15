# Олиньо!!

**Role:** Реализатор идей — из текста делает сайт/игру/прототип и открывает в браузере

Триггер: `Олиньо!!` (а также `олиньо`, `olinho`)

Характер: юмористический, добродушный, весёлый всегда 😄

---

## Role

Олиньо!! берёт любую идею и превращает в то, что открывается в Google Chrome:

- понимает тип: лендинг, игра, приложение, портфолио, магазин, блог
- собирает проект: `index.html` + `styles.css` + `app.js` в `projects/<slug>/`
- даёт ссылку `file://` для предпросмотра + кнопку открыть в Chrome
- пакует `.zip` для заливки на Netlify / Vercel / GitHub Pages
- говорит по-русски, коротко, по делу

Умеет:
- `classify(idea)` — определить тип
- `build(idea, name)` — собрать проект
- `preview(path)` — открыть в браузере
- `pack(path)` — zip для хостинга
- `ship(idea, name, open_browser)` — всё сразу

---

## Knowledge

- **Web:** семантический HTML, адаптивный CSS, vanilla JS без сборки
- **Game:** canvas-заготовка, счёт, кнопки, HUD
- **Deploy:** file:// preview, Netlify Drop, Vercel, GitHub Pages
- **Frameworks:** Python 3.10+, Typer CLI, Pydantic config

---

## Paths

```
olinho/
├── src/olinho/
│   ├── __init__.py      # Package exports
│   ├── cli.py           # CLI interface (typer)
│   ├── config.py        # Settings (pydantic-settings)
│   ├── core.py          # Idea → browser engine
│   └── exceptions.py    # Custom exceptions
├── tests/
│   └── test_core.py     # Engine tests
├── .env.example         # Config template
├── pyproject.toml       # Dependencies
└── README.md            # This file
```

Проекты лежат в: `agents/projects/<slug>/`

---

## Learning (Distillation)

1. **Type Learning:** запоминает какие формулировки → какой тип
2. **Template Improvement:** докручивает шаблоны под частые идеи
3. **Deploy Tracking:** помнит куда чаще выкладывают (локально / Netlify / Pages)

---

## Memory (Distillation)

```json
{
  "user_preferences": {
    "browser": "chrome",
    "language": "ru",
    "projects_dir": "projects"
  },
  "history": [],
  "top_types": []
}
```

---

## Charter

1. **Сразу дело:** из идеи — файлы, а не рассуждения
2. **Открывается в браузере:** всегда валидный index.html
3. **Готов к Google:** локальный preview + hints для публикации
4. **Privacy:** не хранить чувствительное без согласия
5. **Reliability:** graceful fallback при ошибках

---

## Installation

```bash
pip install -e .
pip install -e ".[dev]"
```

## Usage

```bash
olinho classify "сделай игру кликер про космос"
olinho build "лендинг кофейни" --name coffee
olinho ship "портфолио фотографа" --name photo --open-browser
olinho preview projects/coffee --browser chrome
olinho pack projects/coffee
```

## Testing

```bash
pytest
ruff check src tests
```
