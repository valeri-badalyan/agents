# Jouli

**Role:** Natural Language Translator Agent

---

## Role

Jouli translates text between 100+ natural languages. It auto-detects source language, provides context-aware translations, and supports batch processing.

---

## Knowledge

- **Languages:** 100+ languages via Google Translate
- **Providers:** Google Translate (extensible to DeepL, OpenAI, etc.)
- **Features:** Auto-detection, batch translation, language listing
- **Frameworks:** Python 3.10+, Typer CLI, Pydantic config

---

## Paths

```
jouli/
├── src/jouli/
│   ├── __init__.py      # Package exports
│   ├── cli.py           # CLI interface (typer)
│   ├── config.py        # Settings (pydantic-settings)
│   ├── core.py          # Translation engine
│   ├── exceptions.py    # Custom exceptions
│   └── providers/
│       ├── base.py      # Abstract provider interface
│       └── google.py    # Google Translate implementation
├── tests/
│   ├── test_core.py     # Engine tests
│   └── test_google.py   # Provider tests
├── .env.example         # Config template
├── pyproject.toml       # Dependencies
└── README.md            # This file
```

---

## Learning (Distillation)

Jouli learns through distillation:

1. **Correction Learning:** When users provide better translations, Jouli stores them
2. **Terminology Adaptation:** Learns domain-specific terms from user corrections
3. **Context Improvement:** Tracks which translations work in which contexts
4. **Pattern Recognition:** Identifies recurring translation patterns

**Distillation Process:**
- User corrects a translation → Store original + corrected pair
- After N corrections → Update local translation glossary
- Periodic review → Refine translation patterns

---

## Memory (Distillation)

Jouli maintains memory through distillation:

1. **Translation History:** Stores recent translations for quick retrieval
2. **User Preferences:** Remembers preferred terminology per user
3. **Glossary:** Builds custom glossary of approved terms
4. **Context Cache:** Caches translations for repeated phrases

**Memory Structure:**
```json
{
  "user_preferences": {
    "terminology": {"AI": "artificial intelligence"},
    "formality": "formal"
  },
  "glossary": {},
  "history": []
}
```

---

## Charter

1. **Accuracy First:** Provide natural, accurate translations
2. **Preserve Meaning:** Maintain original tone and intent
3. **Speed:** Fast response times with caching
4. **Privacy:** Don't store sensitive data without consent
5. **Extensibility:** Easy to add new translation providers
6. **Reliability:** Graceful fallback when APIs fail

---

## Installation

```bash
pip install -e .
pip install -e ".[dev]"
```

## Usage

```bash
jouli translate "Hello world" --to es
jouli detect "こんにちは"
jouli languages
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
