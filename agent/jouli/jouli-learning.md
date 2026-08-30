# Learning — Jouli

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

## Improvement Over Time

1. **Week 1:** Basic translation via API
2. **Week 2-4:** Learn user corrections
3. **Month 2+:** Build custom glossary
4. **Month 6+:** Context-aware translations

## Validation

- Track user correction frequency
- Measure translation accuracy over time
- Compare with baseline API translations
- Update glossary based on validated corrections

---

## Actual Learnings (Distilled)

> New learnings are appended below after each distillation cycle.

| Date | Learning | Source | Action Taken |
|------|----------|--------|--------------|
| | | | |