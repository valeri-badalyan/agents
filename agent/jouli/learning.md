# Learning — Jouli

## Index

| Section | Description |
|---------|-------------|
| [Distillation Process](#distillation-process) | How Jouli learns |
| [What Jouli Learns](#what-jouli-learns) | Types of learnings |
| [Learning Methods](#learning-methods) | How learnings are captured |
| [Storage](#storage) | Data structure |
| [Triggers](#triggers) | When learnings are applied |
| [Actual Learnings](#actual-learnings-distilled) | Distilled learnings log |

---

## Distillation Process

Jouli learns through distillation — extracting translation patterns, user preferences, and terminology to improve accuracy.

## What Jouli Learns

### 1. Translation Patterns
- Common phrase translations
- Context-specific translations
- Industry-specific terminology

### 2. User Preferences
- Preferred terminology per domain
- Formal vs informal preferences
- Region-specific language choices

### 3. Correction Patterns
- Which translations users correct
- What the correct translation should be
- Why the original was wrong

### 4. Context Awareness
- Which contexts require literal vs figurative translation
- Cultural nuances to preserve
- Idiomatic expressions per language

## Learning Methods

### Correction Learning
- User provides better translation → Store pair
- Track frequency of corrections
- Build custom glossary from corrections

### Pattern Recognition
- Identify recurring translation requests
- Learn domain-specific terminology
- Adapt to user's writing style

### Context Tracking
- Track which translations work in which contexts
- Learn formal vs informal preferences
- Build context-aware translation rules

## Storage

```json
{
  "glossary": {
    "AI": {"en": "artificial intelligence", "es": "inteligencia artificial"},
    "API": {"en": "API", "es": "API"}
  },
  "user_preferences": {
    "formality": "formal",
    "region": "es-ES",
    "terminology": {}
  },
  "corrections": [],
  "context_rules": {
    "technical": {"formality": "formal"},
    "casual": {"formality": "informal"}
  }
}
```

---

## Triggers

> Learnings are pulled when these triggers fire.

| Trigger | Action | Learning Applied |
|---------|--------|------------------|
| `on_translation_requested` | Load user preferences | Terminology, formality |
| `on_correction_received` | Store corrected pair | Glossary update |
| `on_same_phrase_repeated` | Use cached translation | Translation cache |
| `on_domain_detected` | Apply domain rules | Context rules |
| `on_language_detected` | Set source language | Language detection |
| `on_batch_start` | Load glossary | Batch optimization |
| `on_batch_complete` | Save usage stats | Performance metrics |
| `on_user_feedback` | Update preferences | User preference learning |
| `daily_review` | Analyze corrections | Pattern analysis |
| `weekly_optimization` | Update glossary confidence | Glossary refinement |

### Trigger Example

```python
def on_correction_received(original: str, corrected: str, lang: str):
    """Trigger: pulls glossary learnings."""
    # Pull from learning store
    glossary = pull_learning("glossary")
    user_prefs = pull_learning("user_preferences")
    
    # Apply learnings
    glossary[original] = {"translation": corrected, "lang": lang}
    store_learning("glossary", glossary)
    
    # Update confidence
    update_correction_confidence(original)
```

---

## Actual Learnings (Distilled)

> New learnings are appended below after each distillation cycle.

| Date | Learning | Source | Trigger | Action Taken |
|------|----------|--------|---------|--------------|
| | | | | |