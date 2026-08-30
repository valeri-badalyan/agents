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

---

## Agents Overview

| Agent | Role | Status |
|-------|------|--------|
| [Valeri](./valeri/) | Orchestrator — Coordinates all agents | Active |
| [Jouli](./jouli/) | Natural Language Translator | Active |

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
├── valeri/                # Orchestrator agent
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