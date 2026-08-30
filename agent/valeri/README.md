# Valeri

**Role:** Orchestrator Agent — Coordinates all other agents

---

## Role

Valeri is the master orchestrator that:
- Initializes and loads all agents from the repository
- Routes tasks to the appropriate agent
- Manages agent sessions and state
- Handles inter-agent communication
- Provides a unified interface for all agent capabilities

---

## Knowledge

- **Agent Registry:** Knows all available agents and their capabilities
- **Task Routing:** Maps tasks to the right agent based on keywords/context
- **Session Management:** Tracks active sessions and agent states
- **Error Handling:** Coordinates fallback strategies across agents

---

## Paths

```
valeri/
├── src/valeri/
│   ├── __init__.py
│   ├── orchestrator.py   # Main orchestrator logic
│   ├── registry.py       # Agent registry and discovery
│   ├── session.py        # Session management
│   └── router.py         # Task routing engine
├── tests/
├── .env.example
├── pyproject.toml
└── README.md
```

---

## Learning (Distillation)

Valeri learns through distillation:

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

Valeri maintains memory through distillation:

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
from valeri import Orchestrator

# Initialize orchestrator
valeri = Orchestrator()

# Load all agents from repo
valeri.load_agents()

# Or load specific agent
valeri.load_agent("jouli")

# Route a task
result = valeri.route("Translate hello to Spanish")

# Direct agent call
result = valeri.agents["jouli"].translate("Hello", "es")
```

## CLI

```bash
# Start with Valeri orchestrator
valeri

# Load specific agent directly
jouli translate "Hello" --to es
```
