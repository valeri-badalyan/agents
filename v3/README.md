# V3

**Role:** Orchestrator Agent — Coordinates all other agents (replaces Valeri)

---

## Role

V3 is the master orchestrator that:
- Initializes and loads all agents from the repository
- Routes tasks to the appropriate agent (improved routing with explicit triggers)
- Manages agent sessions and state
- Handles inter-agent communication and multi-agent coordination
- Provides a unified interface for all agent capabilities

V3 replaces Valeri as the default agent (`default_agent: v3`).

---

## Knowledge

- **Agent Registry:** Knows all available agents and their capabilities
- **Task Routing:** Maps tasks to the right agent based on keywords + explicit triggers (RU/EN)
- **Session Management:** Tracks active sessions and agent states
- **Error Handling:** Coordinates fallback strategies across agents
- **Multi-match:** `route_all()` finds all matching agents for complex tasks

### Routing table

| Agent | Triggers |
|-------|----------|
| jouli | перевод, translate, language, язык |
| leo-davinci | 3D, scene, render, иллюстрация, модель |
| omar-hayam | story, сюжет, персонаж, мир, диалог |
| enrique | enrike, enrique, энрике |
| messi | Анкара Месси, Ankara Messi, messi, футбол |
| zhanel | Жанель иди сюда, zhanel, маркетинг, strategy |
| olinho | Олиньо!!, olinho, сайт, игра, прототип, браузер |
| marika | марика, marika, статистика, growth, trend |
| ferracho | Феррачо!!, ferracho, бизнес, SWOT, воронка |
| halib | Халиб, halib, дизайн, палитра, лого |
| aryubi | Арюби, aryubi, финансы, бюджет, P&L |

---

## Paths

```
v3/
├── src/v3/
│   ├── __init__.py
│   ├── orchestrator.py   # Main orchestrator logic (Orchestrator + V3 alias)
│   ├── registry.py       # Agent registry and discovery
│   ├── session.py        # Session management
│   └── router.py         # Task routing engine (improved)
├── tests/
├── .env.example
├── pyproject.toml
└── README.md
```

---

## Learning (Distillation)

V3 learns through distillation:

1. **Task Patterns:** Learns which agents handle which tasks best
2. **Routing Optimization:** Improves task routing based on success/failure
3. **Performance Tracking:** Tracks agent response times and accuracy
4. **User Preferences:** Remembers user's preferred agents for similar tasks

**Distillation Process:**
- Task arrives → Route to agent → Track result
- After N tasks → Analyze routing patterns
- Update routing rules → Improve future decisions

---

## Memory (Distillation)

V3 maintains memory through distillation:

1. **Agent Registry:** Dynamic list of all available agents
2. **Session History:** Tracks all sessions and their outcomes
3. **Performance Metrics:** Stores agent performance data
4. **Routing Rules:** Learned rules for task assignment

**Memory Structure:**
```json
{
  "agents": {
    "jouli": {"status": "active", "capabilities": ["translate", "detect"]}
  },
  "sessions": [],
  "routing_rules": {},
  "performance": {}
}
```

---

## Charter

1. **Central Control:** Single entry point for all agent operations
2. **Smart Routing:** Automatically route tasks to the best agent
3. **Session Persistence:** Maintain session state across interactions
4. **Fault Tolerance:** Handle agent failures gracefully
5. **Extensibility:** Easy to register new agents
6. **Transparency:** Log all routing decisions for debugging

---

## Usage

```python
from v3 import Orchestrator

# Initialize orchestrator
v3 = Orchestrator()

# Load all agents from repo
v3.load_agents()

# Route a task (single best agent)
result = v3.route("Translate hello to Spanish")

# Find all matching agents (multi-agent tasks)
agents = v3.route_all("Сделай маркетинг и дизайн для лендинга")
```

## CLI

```bash
# Start with V3 orchestrator
python session_loader.py v3

# List agents
python session_loader.py --list
```
