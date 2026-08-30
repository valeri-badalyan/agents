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

| Agent | Role | Type | Status |
|-------|------|------|--------|
| [Valeri](./agent/valeri/) | Orchestrator — Coordinates all agents | Python | Active |
| [Jouli](./agent/jouli/) | Natural Language Translator | Python | Active |
| [Omar Hayam](./agent/omar-hayam.md) | Scenario Writer — Stories, narratives, games, films | Prompt | Active |

---

## Valeri — Orchestrator Agent

**Role:** Coordinates all other agents, routes tasks, manages sessions

**Knowledge:**
- Agent registry and discovery
- Task routing based on content
- Session management and state

**Paths:**
- Source: `agent/valeri/src/valeri/`
- Tests: `agent/valeri/tests/`
- Config: `agent/valeri/.env.example`

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
- Source: `agent/jouli/src/jouli/`
- Tests: `agent/jouli/tests/`
- Config: `agent/jouli/.env.example`

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

## Omar Hayam — Scenario Writer Agent

**Role:** Creates storylines, narratives, and scenarios for games and films

**Knowledge:**
- Narrative design: story structure, plot arcs, pacing, tension curves
- Character development: backstories, motivations, relationships, arcs
- World-building: settings, lore, rules of the universe, atmosphere
- Dialogue: natural, character-specific speech patterns and subtext
- Game scenarios: branching narratives, player agency, quest design
- Film scenarios: three-act structure, visual storytelling, scene composition

**Paths:**
- Prompt: `agent/omar-hayam.md`

**Learning (Distillation):**
- Learns genre preferences and tone from feedback
- Adapts character voices based on user corrections
- Improves pacing and structure over time

**Memory (Distillation):**
- Stores style preferences (genre, tone, pacing)
- Maintains character library
- Keeps scenario archive for reference

**Charter:**
- Create original, engaging scenarios
- Maintain character and world consistency
- Follow proper story structure principles
- Support multiple formats and genres
- Be creative, bold, and original

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

1. Create a folder inside `agent/` named after the agent (lowercase, no spaces)
2. Include: `README.md`, source code (for Python agents), or prompt file (for prompt agents)
3. Update this root README with agent details
4. Follow the rules in `RULES.md`

---

## Structure

```
agents/
├── README.md              # This file
├── RULES.md               # Hard rules for all agents
├── session_loader.py      # Main entry point
└── agent/
    ├── valeri/            # Orchestrator agent (Python)
    │   ├── README.md
    │   ├── src/valeri/
    │   ├── tests/
    │   └── ...
    ├── jouli/             # Translator agent (Python)
    │   ├── README.md
    │   ├── src/jouli/
    │   ├── tests/
    │   └── ...
    └── omar-hayam.md      # Scenario writer (Prompt)
```