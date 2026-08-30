# Learning — Valeri

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

## Improvement Over Time

1. **Week 1:** Basic keyword routing
2. **Week 2-4:** Learn from user corrections
3. **Month 2+:** Predictive routing based on context
4. **Month 6+:** Personalized routing per user

## Validation

- Compare routing accuracy monthly
- Track user satisfaction scores
- Review failed routings for patterns
- Update rules based on data, not assumptions

---

## Actual Learnings (Distilled)

> New learnings are appended below after each distillation cycle.

| Date | Learning | Source | Action Taken |
|------|----------|--------|--------------|
| | | | |