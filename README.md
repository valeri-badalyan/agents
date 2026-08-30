# Agents

A collection of specialized AI agents, each designed for specific tasks.

---

## Agents Overview

| Agent | Role | Status |
|-------|------|--------|
| [Jouli](./jouli/) | Natural Language Translator | Active |

---

## Jouli — Translator Agent

**Role:** Natural Language Translation

**Knowledge:**
- Multi-language translation (100+ languages)
- Language auto-detection
- Context-aware translation

**Paths:**
- Source: `jouli/src/jouli/`
- Tests: `jouli/tests/`
- Config: `jouli/.env.example`

**Learning (Distillation):**
- Learns from translation corrections
- Adapts to user preferred terminology
- Improves accuracy over time

**Memory (Distillation):**
- Stores translation history
- Remembers user preferences
- Maintains glossary of terms

**Charter:**
- Provide accurate, natural translations
- Preserve meaning and tone
- Support batch processing
- Respect rate limits and API quotas

---

## General Rules (Hard Rules)

See [RULES.md](./RULES.md)

---

## Adding New Agents

1. Create a folder named after the agent (lowercase, no spaces)
2. Include: `README.md`, source code, tests
3. Update this root README with agent details
4. Follow the rules in `RULES.md`

---

## Structure

```
agents/
├── README.md          # This file
├── RULES.md           # Hard rules for all agents
├── jouli/             # Jouli translator agent
│   ├── README.md
│   ├── src/
│   ├── tests/
│   └── ...
└── [next-agent]/      # Future agents
```
