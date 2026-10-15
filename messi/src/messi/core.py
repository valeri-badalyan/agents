"""Core logic for Messi — football tactics, training and quiz."""

from __future__ import annotations

import logging
import random

from messi.exceptions import QuizError, TacticsError, TrainingError

logger = logging.getLogger(__name__)

FORMATIONS: dict[str, dict[str, str]] = {
    "4-4-2": {"style": "balanced", "strength": "defensive compactness", "weakness": "midfield overload"},
    "4-3-3": {"style": "attacking", "strength": "wing play", "weakness": "space behind fullbacks"},
    "3-5-2": {"style": "possession", "strength": "midfield control", "weakness": "wide areas"},
    "4-2-3-1": {"style": "flexible", "strength": "counter-press", "weakness": "isolated striker"},
    "5-3-2": {"style": "defensive", "strength": "low block", "weakness": "lack of width in attack"},
}

POSITIONS_RU: dict[str, str] = {
    "goalkeeper": "вратарь",
    "defender": "защитник",
    "midfielder": "полузащитник",
    "forward": "нападающий",
    "winger": "вингер",
    "striker": "страйкер",
}

TRAINING_PROGRAMS: dict[str, list[str]] = {
    "beginner": [
        "Разминка 10 минут: бег + растяжка",
        "Ведение мяча 15 минут: слалом между конусами",
        "Пасы в парах 15 минут: внутренняя сторона стопы",
        "Удары по воротам 10 минут: с места",
        "Заминка 5 минут",
    ],
    "amateur": [
        "Разминка 10 минут + координационная лестница",
        "Приём-передача в движении 20 минут",
        "Финты: ножницы, проброс, разворот Кройфа — 15 минут",
        "Мини-игра 3x3 — 20 минут",
        "ОФП: планка 3x60 сек, приседания 3x15",
    ],
    "pro": [
        "Активация + рывки 5x30м",
        "Прессинг и контрпрессинг в квадрате 4v2 — 20 минут",
        "Завершение атак с флангов — 20 минут",
        "Стандарты: угловые и штрафные — 15 минут",
        "Видеоразбор + восстановление",
    ],
}

QUIZ_QUESTIONS: list[dict[str, str | list[str]]] = [
    {
        "question": "Сколько игроков одной команды на поле?",
        "options": ["9", "10", "11", "12"],
        "answer": "11",
    },
    {
        "question": "Сколько длится стандартный матч?",
        "options": ["80 минут", "90 минут", "100 минут", "120 минут"],
        "answer": "90 минут",
    },
    {
        "question": "Что означает офсайд?",
        "options": [
            "Мяч вышел за линию",
            "Игрок ближе к воротам, чем предпоследний защитник в момент паса",
            "Фол в штрафной",
            "Замена",
        ],
        "answer": "Игрок ближе к воротам, чем предпоследний защитник в момент паса",
    },
    {
        "question": "Какая схема считается атакующей?",
        "options": ["5-3-2", "4-3-3", "5-4-1", "4-5-1"],
        "answer": "4-3-3",
    },
]


def _validate_text(value: str, field_name: str) -> str:
    """Validate non-empty user input."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


class Messi:
    """Football agent: tactics, training plans, motivation and quiz."""

    def __init__(self) -> None:
        """Initialize Messi agent."""
        self.name: str = "messi"
        logger.debug("Messi agent initialized")

    def analyze_formation(self, formation: str) -> dict[str, str]:
        """Analyze a football formation.

        Args:
            formation: Formation string, e.g. "4-3-3".

        Returns:
            Dict with style, strength, weakness and advice.

        Raises:
            TacticsError: If formation is unknown.
        """
        try:
            key = _validate_text(formation, "formation")
        except ValueError as exc:
            raise TacticsError(str(exc)) from exc
        if key not in FORMATIONS:
            raise TacticsError(
                f"Unknown formation '{key}'. Supported: {', '.join(sorted(FORMATIONS))}"
            )
        info = FORMATIONS[key]
        logger.info("Analyzed formation %s", key)
        return {
            "formation": key,
            "style": info["style"],
            "strength": info["strength"],
            "weakness": info["weakness"],
            "advice": f"Схема {key}: используй {info['strength']}, закрывай {info['weakness']}.",
        }

    def training_plan(self, level: str = "beginner", position: str = "forward") -> dict[str, str | list[str]]:
        """Build a training plan for level and position.

        Args:
            level: One of beginner, amateur, pro.
            position: Player position in English.

        Returns:
            Dict with level, position and exercises list.

        Raises:
            TrainingError: If level or position is invalid.
        """
        try:
            lvl = _validate_text(level, "level").lower()
            pos = _validate_text(position, "position").lower()
        except ValueError as exc:
            raise TrainingError(str(exc)) from exc
        if lvl not in TRAINING_PROGRAMS:
            raise TrainingError(
                f"Unknown level '{lvl}'. Supported: {', '.join(sorted(TRAINING_PROGRAMS))}"
            )
        pos_ru = POSITIONS_RU.get(pos, pos)
        logger.info("Built training plan level=%s position=%s", lvl, pos)
        return {
            "level": lvl,
            "position": pos_ru,
            "exercises": list(TRAINING_PROGRAMS[lvl]),
        }

    def motivate(self, player_name: str = "чемпион") -> str:
        """Return a motivational message.

        Args:
            player_name: Name to include in message.

        Returns:
            Motivational string in Russian.
        """
        name = player_name.strip() if isinstance(player_name, str) and player_name.strip() else "чемпион"
        return (
            f"{name}, помни: даже Месси когда-то начинал с первой тренировки! "
            "Выйди на поле, отдай все силы и наслаждайся игрой. Vamos!"
        )

    def quiz_question(self, seed: int | None = None) -> dict[str, str | list[str]]:
        """Return a random quiz question.

        Args:
            seed: Optional seed for deterministic choice.

        Returns:
            Dict with question, options and answer.
        """
        try:
            rng = random.Random(seed)
            return dict(rng.choice(QUIZ_QUESTIONS))
        except Exception as exc:
            raise QuizError(f"Failed to generate quiz: {exc}") from exc

    def check_quiz_answer(self, question: str, user_answer: str) -> bool:
        """Check user answer against known quiz questions.

        Args:
            question: Quiz question text.
            user_answer: Answer to verify.

        Returns:
            True if correct, False otherwise.

        Raises:
            QuizError: If question is unknown or input invalid.
        """
        try:
            q = _validate_text(question, "question")
            a = _validate_text(user_answer, "user_answer")
        except ValueError as exc:
            raise QuizError(str(exc)) from exc
        for item in QUIZ_QUESTIONS:
            if item["question"] == q:
                return str(item["answer"]).strip().lower() == a.strip().lower()
        raise QuizError(f"Unknown question: {q}")


engine = Messi()
