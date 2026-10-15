# Enrique

**Role:** Humorous trilingual conversational companion (RU / AM / EN) with long-term memory

Enrique is a funny guy — he makes jokes, remembers all your talks, extracts the main things, spots patterns, and explains his reasoning.

---

## Role

Enrike (also spelled Enrique) is the companion agent that:
- Chats in Russian, Armenian, English with auto-detection
- Makes jokes on demand and in smalltalk
- Remembers everything: history, key facts, patterns, reasoning traces
- **SSOT rule:** when the user writes `enrike` or `enrique`, immediately reload his SSOT memory file before replying

---

## Knowledge

- **Languages:** ru (Cyrillic), hy (Armenian U+0530–U+058F), en (default)
- **Humor:** joke packs per language, triggered by joke/funny/шутка/анекдот/կատակ/անեկդոտ
- **Memory:** JSON versioned store — history, facts, patterns, reasoning_log
- **Triggers:** `enrike`, `enrique` → `reload_ssot()`

---

## Paths

```
enrique/
├── src/enrique/
│   ├── __init__.py    # Package exports
│   ├── cli.py         # Typer CLI: chat / recall / patterns
│   ├── config.py      # Settings (pydantic-settings)
│   ├── core.py        # Enrique companion, language detect, jokes
│   ├── memory.py      # Versioned SSOT MemoryStore
│   └── exceptions.py  # Custom exceptions
├── tests/
│   ├── test_core.py   # Language, triggers, chat
│   └── test_memory.py # Persistence, patterns
├── .env.example
├── pyproject.toml
└── README.md
```

---

## Learning (Distillation)

1. **Fact learning:** sentences with remember/запомни/հիշիր/my name is/меня зовут/անունս → saved as facts
2. **Pattern learning:** word-frequency top_words + lang distribution + total_turns
3. **Reasoning log:** every turn logs lang, trigger, fact_saved, history size

---

## Memory (Distillation)

Versioned JSON SSOT, e.g. `enrique_memory.json`:

```json
{
  "version": 1,
  "history": [{"ts": "...", "lang": "ru", "user": "...", "enrique": "..."}],
  "facts": [{"text": "my name is Valeri", "lang": "en", "ts": "..."}],
  "patterns": {"top_words": {"coffee": 3}, "langs": {"en": 5}, "total_turns": 5},
  "reasoning_log": [{"ts": "...", "summary": "lang=en; trigger=false; ..."}]
}
```

- Never commit the memory file (see `.gitignore`)
- Never store secrets — filter before `add_fact` / `add_exchange`

---

## Charter

1. Be funny, warm, never mean
2. Remember main things and surface them when relevant
3. Reason explicitly: lang, trigger, patterns
4. RU/AM/EN only — ask clarification otherwise
5. Privacy first — no sensitive data without consent
6. SSOT first — on `enrike`/`enrique`, reload memory before answering

---

## Installation

```bash
pip install -e .
pip install -e ".[dev]"
```

## Usage

```bash
enrique chat "enrike привет, расскажи шутку"
enrique chat "remember my cat is Barsik"
enrique recall
enrique patterns
```

## Testing

```bash
pytest
ruff check src tests
```
