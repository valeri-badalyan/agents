# Agents

A collection of specialized AI agents, each designed for specific tasks.

---

## Quick Start

```bash
# List all agents
python session_loader.py --list

# Load specific agent
python session_loader.py jouli

# Load orchestrator (default)
python session_loader.py
```

> V3 is the default orchestrator. Valeri is kept for backward compatibility.

---

## Agents Overview

| Agent | Role | Status |
|-------|------|--------|
| [V3](./v3/) | Orchestrator — Coordinates all agents (replaces Valeri) | Active |
| [Valeri](./valeri/) | Legacy orchestrator — kept for backward compatibility | Legacy |
| [Jouli](./jouli/) | Natural Language Translator | Active |
| [Enrique](./enrique/) | Humorous trilingual companion (RU/AM/EN) — trigger: enrike/enrique | Active |
| [Messi](./messi/) | Football Agent — tactics, training, motivation, quiz — trigger: Анкара Месси / Ankara Messi | Active |
| [Zhanel](./zhanel/) | Marketer — strategy, copy, content-plans, launches — trigger: Жанель иди сюда / жанель / zhanel | Active |
| [Olinho](./olinho/) | Idea-to-browser — сайты, игры, прототипы + открытие в Chrome — trigger: Олиньо!! / олинью / olinho | Active |
| [Marika](./marika/) | Руководитель статистики — describe, growth, trend, shares, отчёты RU/EN/ZH — trigger: марика / marika | Active |
| [Ferracho](./ferracho/) | Бизнес-аналитик — SWOT, воронка, юнит-экономика, риски, аудит — trigger: Феррачо!! / феррачо / ferracho | Active |
| [Halib](./halib/) | Дизайнер — концепты, палитры, типографика, макеты, лого, аудит — trigger: Халиб / халиб / halib | Active |
| [Aryubi](./aryubi/) | Финансист — бюджет, кэшфлоу, P&L, инвестиции — trigger: Арюби / арюби / aryubi | Active |
| [Mika](./mika/) | Весёлый провайдер — тарифы, покрытие, диагностика, подключение — trigger: мика / mika | Active |

---

## Valeri — Orchestrator Agent

**Role:** Coordinates all other agents, routes tasks, manages sessions

**Knowledge:**
- Agent registry and discovery
- Task routing based on content
- Session management and state

**Paths:**
- Source: `valeri/src/valeri/`
- Tests: `valeri/tests/`
- Config: `valeri/.env.example`

**Learning (Distillation):**
- Learns which agents handle which tasks
- Optimizes routing based on success/failure
- Tracks agent performance metrics

**Memory (Distillation):**
- Stores agent registry and capabilities
- Maintains session history
- Keeps routing rules and performance data

**Charter:**
- Single entry point for all agent operations
- Smart routing to best agent
- Fault tolerance across agents
- Transparency in routing decisions

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

## Messi — Football Agent

**Role:** Tactics analysis, training plans, motivation, quiz

**Knowledge:**
- Formations 4-4-2, 4-3-3, 3-5-2, 4-2-3-1, 5-3-2
- Training levels beginner/amateur/pro
- Football quiz

**Paths:**
- Source: `messi/src/messi/`
- Tests: `messi/tests/`
- Config: `messi/.env.example`

**Learning (Distillation):**
- Learns favorite formations and positions
- Adapts training load

**Memory (Distillation):**
- Stores training history and quiz scores
- Remembers user preferences

**Charter:**
- Love the game, accurate advice, safe training

---

## Session Loader

The session loader (`session_loader.py`) is the main entry point:

```python
from session_loader import load_agent, load_all_agents, create_session

# Load specific agent
jouli = load_agent("jouli")

# Load all agents
agents = load_all_agents()

# Create session with agent
session = create_session("jouli")

# Create session with orchestrator
session = create_session("valeri")
```

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
├── README.md              # This file
├── RULES.md               # Hard rules for all agents
├── session_loader.py      # Main entry point
├── v3/                    # Orchestrator agent (default)
│   ├── README.md
│   ├── src/v3/
│   ├── tests/
│   └── ...
├── valeri/                # Legacy orchestrator agent
│   ├── README.md
│   ├── src/valeri/
│   ├── tests/
│   └── ...
├── jouli/                 # Translator agent
│   ├── README.md
│   ├── src/jouli/
│   ├── tests/
│   └── ...
└── [next-agent]/          # Future agents
```