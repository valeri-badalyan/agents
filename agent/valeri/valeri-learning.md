# Learning — Valeri

## Index

| Section | Description |
|---------|-------------|
| [Distillation Process](#distillation-process) | How Valeri learns |
| [What Valeri Learns](#what-valeri-learns) | Types of learnings |
| [Learning Methods](#learning-methods) | How learnings are captured |
| [Storage](#storage) | Data structure |
| [Triggers](#triggers) | When learnings are applied |
| [Actual Learnings](#actual-learnings-distilled) | Distilled learnings log |

---

## Distillation Process

Valeri learns through distillation — extracting patterns from interactions to improve routing and coordination.

## What Valeri Learns

### 1. Task Routing Patterns
- Which keywords indicate which agent
- Which tasks succeed vs fail per agent
- Which agents handle edge cases best

### 2. User Preferences
- Which agents the user prefers for similar tasks
- Response format preferences
- Communication style preferences

### 3. Performance Metrics
- Agent response times
- Task completion rates
- Error frequencies per agent

### 4. Session Patterns
- Common session flows
- Which agents are used together
- Typical session durations

## Learning Methods

### Observation
- Track task → agent → outcome
- Record user corrections after routing
- Monitor agent performance over time

### Feedback Loop
- User corrects routing → Update routing rules
- Agent fails → Adjust routing confidence
- User confirms success → Reinforce routing pattern

### Pattern Recognition
- Identify recurring task types
- Group similar tasks by agent
- Build routing confidence scores

## Storage

```json
{
  "routing_rules": {
    "translate|translation|language": {"agent": "jouli", "confidence": 0.95},
    "story|narrative|scenario": {"agent": "omar-hayam", "confidence": 0.90}
  },
  "performance": {
    "jouli": {"success_rate": 0.98, "avg_response_time": 1.2},
    "omar-hayam": {"success_rate": 0.92, "avg_response_time": 3.5}
  },
  "user_preferences": {
    "preferred_agents": {},
    "response_format": "concise"
  }
}
```

---

## Triggers

> Learnings are pulled when these triggers fire.

| Trigger | Action | Learning Applied |
|---------|--------|------------------|
| `on_task_received` | Route to best agent | Routing rules, confidence scores |
| `on_routing_success` | Reinforce routing pattern | Positive reinforcement |
| `on_routing_failure` | Adjust routing rules | Negative feedback |
| `on_user_correction` | Update routing preferences | User preference learning |
| `on_session_start` | Load user preferences | Session patterns |
| `on_session_end` | Save session metrics | Performance data |
| `on_agent_added` | Update routing rules | New agent registration |
| `on_agent_removed` | Remove routing rules | Agent deregistration |
| `daily_review` | Analyze performance metrics | Trend analysis |
| `weekly_optimization` | Update routing confidence | Pattern optimization |

### Trigger Example

```python
def on_task_received(task: str) -> str:
    """Trigger: pulls routing learnings."""
    # Pull from learning store
    routing_rules = pull_learning("routing_rules")
    confidence_scores = pull_learning("confidence_scores")
    
    # Apply learnings
    best_agent = match_routing(task, routing_rules, confidence_scores)
    
    return best_agent
```

---

## Actual Learnings (Distilled)

> New learnings are appended below after each distillation cycle.

| Date | Learning | Source | Trigger | Action Taken |
|------|----------|--------|---------|--------------|
| | | | | |