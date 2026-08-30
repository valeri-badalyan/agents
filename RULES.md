# Hard Rules

These rules apply to **ALL agents** in this repository. No exceptions.

---

## Code Quality

1. **No secrets or API keys in code** — Use environment variables or `.env` files (never committed)
2. **All code must be typed** — Use type hints everywhere
3. **All public functions must have docstrings**
4. **No print statements in production code** — Use logging
5. **All functions must handle errors gracefully** — No unhandled exceptions

## Testing

6. **Every agent must have tests** — Minimum 80% code coverage
7. **Tests must be isolated** — No external API calls in tests (mock everything)
8. **Tests must pass before commit** — Run `pytest` before pushing

## Structure — MANDATORY

9. **Each agent MUST be in `agent/` folder** — Named after the agent (lowercase, no spaces)
10. **Each agent folder MUST have these exact files:**

### For Python Agents:
```
agent/[name]/
├── README.md              # Role, knowledge, paths, learning, memory, charter
├── voice.md               # Agent personality and communication style
├── [name]-charter.md      # Mission, responsibilities, boundaries, rules
├── [name]-learning.md     # Distillation process, triggers, actual learnings
├── src/[name]/            # Source code
├── tests/                 # Test files
├── .env.example           # Required environment variables
└── pyproject.toml         # Dependencies and config
```

### For Prompt Agents:
```
agent/[name]/
├── README.md              # Role, knowledge, paths, learning, memory, charter
├── voice.md               # Agent personality and communication style
├── [name]-charter.md      # Mission, responsibilities, boundaries, rules
├── [name]-learning.md     # Distillation process, triggers, actual learnings
└── [name].md              # Agent prompt file
```

### Learning File Structure (MANDATORY):
Each `[name]-learning.md` MUST have:
1. **Index** — Table of contents
2. **Distillation Process** — How the agent learns
3. **Triggers** — When learnings are pulled and applied
4. **Actual Learnings** — Table for distilled learnings (append only)

11. **ALL files are mandatory** — No exceptions. New agents must include every file listed above.

## Documentation

11. **Root README must list ALL agents** — Updated when adding new agents
12. **Each agent README must define (in this order):**
    - Role — What the agent does
    - Knowledge — What the agent knows
    - Paths — Where files are located
    - Charter — The agent's mission and constraints
    - Learning — How the agent learns (through distillation) — MUST BE LAST
    - Memory — How the agent remembers (through distillation) — MUST BE LAST

## Version Control

13. **No commits to main without review** — Use feature branches
14. **Commit messages must be descriptive** — Follow conventional commits
15. **Never commit `.env` files** — Only `.env.example`

## Security

16. **Validate all inputs** — Never trust user input
17. **Use least privilege** — Agents only access what they need
18. **Log security events** — Track access and failures

## API Usage

19. **Respect rate limits** — Implement backoff and retries
20. **Cache responses when possible** — Reduce API calls
21. **Handle API failures gracefully** — Fallback options required

## Distillation Rules

22. **Learning must be explicit** — Document what the agent learned
23. **Memory must be versioned** — Track changes over time
24. **Knowledge must be validated** — Verify before storing
25. **Privacy first** — Never store sensitive user data without consent

---

## Enforcement

- CI/CD will check for rule compliance
- Violations must be fixed before merge
- Rules can only be updated via pull request with team review
