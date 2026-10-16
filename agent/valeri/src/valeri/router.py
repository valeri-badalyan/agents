"""Task routing engine — routes tasks to appropriate agents."""

from __future__ import annotations

import re

from valeri.registry import AgentRegistry


class Router:
    """Routes tasks to the appropriate agent based on content."""

    def __init__(self, registry: AgentRegistry):
        self.registry = registry
        self._routing_rules: dict[str, list[str]] = {
            "translate|translation|language|interpret": ["jouli"],
            "convert|transform|format": ["jouli"],
            "detect|identify|recognize": ["jouli"],
        }

    def route_task(self, task: str) -> str:
        """Route a task to the best agent."""
        task_lower = task.lower()

        for pattern, agents in self._routing_rules.items():
            if re.search(pattern, task_lower):
                for agent in agents:
                    if self.registry.get_agent_path(agent):
                        return agent

        available = self.registry.discover_agents()
        if available:
            return available[0]

        raise RuntimeError("No agents available in the repository")

    def add_rule(self, pattern: str, agents: list[str]) -> None:
        """Add a routing rule."""
        self._routing_rules[pattern] = agents

    def remove_rule(self, pattern: str) -> None:
        """Remove a routing rule."""
        self._routing_rules.pop(pattern, None)

    def get_rules(self) -> dict[str, list[str]]:
        """Get all routing rules."""
        return self._routing_rules.copy()

    def __repr__(self) -> str:
        return f"Router(rules={len(self._routing_rules)})"