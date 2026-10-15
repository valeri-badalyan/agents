# Agent System

This repository contains specialized AI agents configured as opencode subagents.

## Available Agents

- **V3** — Orchestrator that coordinates all agents and routes tasks (primary agent, replaces Valeri)
- **Valeri** — Legacy orchestrator (kept for backward compatibility)
- **Jouli** — Natural language translation engine (100+ languages)
- **Leo Da Vinci** — 3D design agent for scenes, illustrations, and rendering
- **Omar Hayam** — Narrative agent for storylines, characters, and world-building
- **Enrique** — Humorous trilingual companion (RU/AM/EN) with memory. Trigger: enrike/enrique
- **Zhanel** — Marketer (strategy, copy, content, launches). Trigger: Жанель иди сюда / жанель / zhanel
- **Marika** — Statistics lead (describe, growth, trends, shares, RU/EN/ZH reports). Trigger: марика / marika
- **Ferracho** — Business analyzer (SWOT, funnel, unit-economics, risks, audit). Trigger: Феррачо!! / феррачо / ferracho
- **Halib** — Designer (concepts, palettes, typography, layouts, logo, style guides, audit). Trigger: Халиб / халиб / halib
- **Aryubi** — Финансист (budget, cashflow, P&L, investments, разбор). Trigger: Арюби / арюби / aryubi
- **Mika** — Весёлый провайдер (тарифы, покрытие, диагностика, подключение RU/EN/HY). Trigger: мика / mika

## Quick Start

```bash
# List agents
python session_loader.py --list

# Load orchestrator
python session_loader.py v3

# Load legacy orchestrator
python session_loader.py valeri

# Load translator
python session_loader.py jouli

# Load design agent
python session_loader.py leo-davinci

# Load narrative agent
python session_loader.py omar-hayam

# Load companion (also triggers on enrike/enrique)
python session_loader.py enrique

# Load marketer (also triggers on Жанель иди сюда / жанель)
python session_loader.py zhanel

# Load statistics lead (also triggers on марика / marika)
python session_loader.py marika

# Load business analyzer (also triggers on Феррачо!! / феррачо / ferracho)
python session_loader.py ferracho

# Load designer (also triggers on Халиб / халиб / halib)
python session_loader.py halib

# Load financier (also triggers on Арюби / арюби / aryubi)
python session_loader.py aryubi

# Load provider (also triggers on мика / mika)
python session_loader.py mika
```

## Opencode Configuration

Agents are configured in `.opencode/agent/` directory:

```
.opencode/
├── agent/
│   ├── v3.md              # Orchestrator (primary mode, default)
│   ├── valeri.md          # Legacy orchestrator (primary mode, backward compat)
│   ├── jouli.md           # Translator (subagent mode)
│   ├── leo-davinci.md     # Design agent (subagent mode)
│   ├── omar-hayam.md      # Narrative agent (subagent mode)
│   ├── enrique.md         # Companion (subagent mode, trigger: enrike/enrique)
│   ├── zhanel.md          # Marketer (subagent mode, trigger: Жанель иди сюда / жанель)
│   ├── marika.md          # Statistics lead (subagent mode, trigger: марика / marika)
│   ├── ferracho.md        # Business analyzer (subagent mode, trigger: Феррачо!! / феррачо / ferracho)
│   ├── halib.md           # Designer (subagent mode, trigger: Халиб / халиб / halib)
│   ├── aryubi.md          # Financier (subagent mode, trigger: Арюби / арюби / aryubi)
│   ├── mika.md            # Provider (subagent mode, trigger: мика / mika)
opencode.json              # Main configuration
```

## Usage with Opencode

V3 is the default primary agent. It routes tasks to subagents:

- **Translation tasks** → Jouli agent
- **3D/visual design tasks** → Leo Da Vinci agent
- **Story/narrative tasks** → Omar Hayam agent
- **Marketing tasks** → Zhanel agent
- **Statistics tasks** → Marika agent
- **Business analysis tasks** → Ferracho agent
- **Design tasks (concept, palette, layout, logo, audit)** → Halib agent
- **Finance tasks (budget, cashflow, P&L, investments)** → Aryubi agent
- **Provider tasks (tariffs, coverage, diagnosis, connection)** → Mika agent

## Rules

See `RULES.md` for hard rules governing all agents.

## Structure

- `v3/` — Orchestrator agent (src, tests, config)
- `valeri/` — Legacy orchestrator (src, tests, config)
- `jouli/` — Translator agent (src, tests, config)
- `leo-davinci/` — Design agent (src, tests, config)
- `omar-hayam/` — Narrative agent (src, tests, config)
- `enrique/` — Companion agent (src, tests, config)
- `zhanel/` — Marketer agent (src, tests, config)
- `marika/` — Statistics lead agent (src, tests, config)
- `ferracho/` — Business analyzer agent (src, tests, config)
- `halib/` — Designer agent (src, tests, config)
- `aryubi/` — Financier agent (src, tests, config)
- `mika/` — Provider agent (src, tests, config)
- `session_loader.py` — Main entry point
- `.opencode/` — Opencode agent definitions
- `opencode.json` — Opencode configuration
