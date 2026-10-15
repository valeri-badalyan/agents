"""Task routing engine — routes tasks to appropriate agents (V3 improved)."""

from __future__ import annotations

import logging
import re

from v3.registry import AgentRegistry

logger = logging.getLogger(__name__)


class Router:
    """Routes tasks to the appropriate agent based on content and triggers."""

    def __init__(self, registry: AgentRegistry) -> None:
        """Initialize router with an agent registry.

        Args:
            registry: AgentRegistry used to verify agent availability.
        """
        self.registry = registry
        # Ordered: explicit name triggers first, then domain keywords.
        # Insertion order = priority.
        self._routing_rules: dict[str, list[str]] = {
            # --- explicit triggers (highest priority) ---
            r"enrike|enrique|энрике": ["enrique"],
            r"анкара месси|ankara messi|\bmessi\b|месси": ["messi"],
            r"жанель иди сюда|жанель|zhanel": ["zhanel"],
            r"олиньо!!|олиньо|олинью|olinho": ["olinho"],
            r"марика|marika": ["marika"],
            r"феррачо!!|феррачо|ferracho": ["ferracho"],
            r"халиб|halib": ["halib"],
            r"арюби|aryubi": ["aryubi"],
            r"jouli|джоули": ["jouli"],
            r"leo-davinci|лео|да винчи|davinci": ["leo-davinci"],
            r"omar-hayam|омар|хаяма|omar|hayam": ["omar-hayam"],
            # --- domain keywords ---
            r"перевод|переведи|translate|translation|language|язык|interpret|транскрипц|диалект|акцент": ["jouli"],
            r"3d|сцена|scene|render|рендер|illustration|иллюстрац|asset|модель|blender|освещение|lighting": ["leo-davinci"],
            r"story|стори|история|сюжет|character|персонаж|world|world-building|мир|dialogue|диалог|сценарий|plot|narrative|герой|фракци|роман|квест": ["omar-hayam"],
            r"сайт|site|лендинг|landing|игра|game|прототип|prototype|браузер|browser|chrome|html|портфолио|магазин|shop|приложение|\bapp\b|собери|сделай страницу|идея": ["olinho"],
            r"маркетинг|marketing|strategy|стратегия|копирайтинг|copy|контент|launch|запуск|реклама|advertising|продвижение|бренд|brand|smm|email|позиционирование|нейминг|слоган|аудитори": ["zhanel"],
            r"статистика|statistics|describe|growth|рост|trend|тренд|share|доля|отч[её]т|report|данные|data|график|динамика|выборка|среднее|медиана": ["marika"],
            r"бизнес|business|swot|свот|воронка|funnel|юнит|unit|риск|risk|аудит|audit|экономика|cac|ltv|retention|конверси": ["ferracho"],
            r"дизайн|design|палитра|palette|типографика|typography|макет|layout|\bui\b|лого|logo|стайлгайд|styleguide|цвет|color|шрифт|font|концепт|concept|ux": ["halib"],
            r"финанс|finance|бюджет|budget|кэшфлоу|cashflow|p&l|\bpnl\b|инвестиц|invest|деньги|money|расход|доход|прибыль|убыток|dсf|npv|irr|cash": ["aryubi"],
            r"футбол|football|tactic|тактика|training|тренировка|quiz|формаци|матч|гол|coach|тренер": ["messi"],
            r"шутка|joke|поболта|анекдот|мем": ["enrique"],
        }

    def route_task(self, task: str) -> str:
        """Route a task to the best agent.

        Args:
            task: User task text.

        Returns:
            Selected agent name.

        Raises:
            ValueError: If task is empty.
            RuntimeError: If no agents are available.
        """
        if not task or not task.strip():
            raise ValueError("Task text must not be empty")
        task_lower = task.lower()

        for pattern, agents in self._routing_rules.items():
            try:
                if re.search(pattern, task_lower):
                    for agent in agents:
                        if self.registry.get_agent_path(agent):
                            return agent
            except re.error as exc:
                logger.error("Invalid routing pattern %r: %s", pattern, exc)
                continue

        available = self.registry.discover_agents()
        if available:
            logger.info("No rule matched, fallback to first agent: %s", available[0])
            return available[0]

        raise RuntimeError("No agents available in the repository")

    def route_all(self, task: str) -> list[str]:
        """Find all agents matching a task (for multi-agent coordination).

        Args:
            task: User task text.

        Returns:
            List of matching agent names (deduplicated, in priority order).
        """
        if not task or not task.strip():
            return []
        task_lower = task.lower()
        matched: list[str] = []
        for pattern, agents in self._routing_rules.items():
            try:
                if re.search(pattern, task_lower):
                    for agent in agents:
                        if (
                            self.registry.get_agent_path(agent)
                            and agent not in matched
                        ):
                            matched.append(agent)
            except re.error:
                continue
        return matched

    def add_rule(self, pattern: str, agents: list[str]) -> None:
        """Add a routing rule.

        Args:
            pattern: Regex pattern to match.
            agents: Agent names for this pattern.
        """
        try:
            re.compile(pattern)
        except re.error as exc:
            logger.error("Invalid regex %r: %s", pattern, exc)
            raise ValueError(f"Invalid regex pattern: {exc}") from exc
        if not agents:
            raise ValueError("Agents list must not be empty")
        self._routing_rules[pattern] = agents

    def remove_rule(self, pattern: str) -> None:
        """Remove a routing rule.

        Args:
            pattern: Regex pattern to remove.
        """
        self._routing_rules.pop(pattern, None)

    def get_rules(self) -> dict[str, list[str]]:
        """Get all routing rules.

        Returns:
            Copy of routing rules.
        """
        return self._routing_rules.copy()

    def __repr__(self) -> str:
        return f"Router(rules={len(self._routing_rules)})"
