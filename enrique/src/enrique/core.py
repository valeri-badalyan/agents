"""Enrique core — humorous trilingual companion with memory.

SSOT: the MemoryStore JSON file is the single source of truth.
Whenever the user writes 'enrike' or 'enrique', load this SSOT
first (MemoryStore.load) before replying.
"""

from __future__ import annotations

import logging
import random
import re
from typing import Any

from enrique.config import settings
from enrique.exceptions import LanguageError, ValidationError
from enrique.memory import SUPPORTED_LANGS, MemoryStore

logger = logging.getLogger(__name__)

# Trigger names that must immediately load Enrique's SSOT.
TRIGGER_NAMES = ("enrike", "enrique")

ARMENIAN_RE = re.compile(r"[\u0530-\u058F]")
CYRILLIC_RE = re.compile(r"[\u0400-\u04FF]")

JOKES: dict[str, list[str]] = {
    "en": [
        "Why don't programmers like nature? Too many bugs! 🐛",
        "I told my memory a joke — now it never forgets the punchline!",
        "Why did the chatbot cross the road? To cache it on the other side!",
    ],
    "ru": [
        "Почему программисты путают Хэллоуин и Рождество? Потому что Oct 31 == Dec 25! 😄",
        "Колобок повесился... шучу! Он просто укатился в мою память и теперь живёт там.",
        "Штирлиц долго смотрел в одну точку. Потом точка посмотрела на Штирлица. А я всё записал!",
    ],
    "hy": [
        "Ինչու՞ ծրագրավորողը կորավ խոհանոցում։ Որովհետև բաղադրատոմսի մեջ «bug» կար! 😄",
        "Ես կատակեցի, հիշողությունս պահպանեց — հիմա երկուսով ծիծաղում ենք!",
        "Ինչու՞ չաթ-բոտը անցավ փողոցը։ Որ մյուս կողմում cache անի!",
    ],
}

REMEMBER_PATTERNS = (
    "remember",
    "запомни",
    "не забудь",
    "հիշիր",
    "my name is",
    "меня зовут",
    "имя",
    "անունս",
)


def detect_language(text: str) -> str:
    """Detect ru/hy/en from script and hints. Defaults to 'en'."""
    if not isinstance(text, str) or not text.strip():
        raise ValidationError("text must be a non-empty string")
    lowered = text.lower()
    if ARMENIAN_RE.search(text):
        return "hy"
    if CYRILLIC_RE.search(text):
        return "ru"
    hy_hints = ("barev", "inch", "von", "es ", "բարև", "ինչ")
    if any(h in lowered for h in hy_hints):
        # Only guess Armenian for latin hints if no cyrillic; keep simple.
        if "barev" in lowered or "inch" in lowered:
            return "hy"
    return "en"


def contains_trigger(text: str) -> bool:
    """Return True if text mentions enrike/enrique (case-insensitive)."""
    if not isinstance(text, str):
        return False
    lowered = text.lower()
    return any(t in lowered for t in TRIGGER_NAMES)


def wants_joke(text: str) -> bool:
    """Detect joke request in RU/AM/EN."""
    lowered = text.lower()
    keywords = ("joke", "funny", "шут", "анекдот", "рассмеши", "прикол", "կատակ", "անեկդոտ", "ծիծաղ")
    return any(k in lowered for k in keywords)


def extract_fact(text: str) -> str | None:
    """Extract a 'main thing' to remember, or None."""
    lowered = text.lower()
    for pat in REMEMBER_PATTERNS:
        if pat in lowered:
            # Store trimmed original as fact.
            fact = text.strip()
            return fact[:300]
    return None


class Enrique:
    """Humorous companion. Memory JSON is the SSOT — always loaded first."""

    def __init__(self, memory_path: str | None = None, max_history: int | None = None) -> None:
        """Initialize Enrique and immediately load SSOT memory."""
        self.memory_path = memory_path or settings.memory_path
        self.max_history = max_history or settings.max_history
        self.max_facts = settings.max_facts
        # SSOT load on startup.
        self.memory = MemoryStore(path=self.memory_path)
        logger.info("Enrique SSOT loaded from %s", self.memory_path)

    def reload_ssot(self) -> dict[str, Any]:
        """Force-reload SSOT from disk. Call on every enrike/enrique trigger."""
        self.memory.load()
        logger.info("Enrique SSOT reloaded on trigger")
        return self.snapshot()

    def snapshot(self) -> dict[str, Any]:
        """Return current SSOT snapshot: facts, patterns, recent history."""
        return {
            "facts": self.memory.get_facts(),
            "patterns": self.memory.get_patterns(),
            "recent": self.memory.get_history(limit=5),
            "version": self.memory.data.get("version", 1),
        }

    def chat(self, text: str, lang: str | None = None) -> dict[str, Any]:
        """Chat with Enrique. Returns reply + reasoning + memory info."""
        if not isinstance(text, str) or not text.strip():
            raise ValidationError("text must be a non-empty string")
        text = text.strip()

        # SSOT: any mention of enrike/enrique reloads memory first.
        triggered = contains_trigger(text)
        if triggered:
            self.memory.load()

        use_lang = lang or settings.default_language or detect_language(text)
        if use_lang not in SUPPORTED_LANGS:
            raise LanguageError(f"Unsupported lang '{use_lang}'. Use ru/hy/en.")

        # Remember main things automatically.
        fact = extract_fact(text)
        fact_saved = False
        if fact:
            fact_saved = self.memory.add_fact(fact, lang=use_lang, max_facts=self.max_facts)

        # Build funny reply.
        if wants_joke(text):
            reply = random.choice(JOKES[use_lang])
        elif triggered:
            reply = self._greeting(use_lang, ssot_loaded=True)
        elif fact and fact_saved:
            reply = self._ack_memory(use_lang)
        else:
            reply = self._smalltalk(text, use_lang)

        self.memory.add_exchange(text, reply, lang=use_lang, max_history=self.max_history)

        reasoning = (
            f"lang={use_lang}; trigger={triggered}; fact_saved={fact_saved}; "
            f"history_turns={len(self.memory.data.get('history', []))}"
        )
        self.memory.log_reasoning(reasoning)

        return {
            "reply": reply,
            "lang": use_lang,
            "triggered_ssot": triggered,
            "fact_saved": fact_saved,
            "reasoning": reasoning,
        }

    def _greeting(self, lang: str, ssot_loaded: bool = False) -> str:
        """Funny greeting, notes SSOT load."""
        base = {
            "en": "Hey! It's Enrique! SSOT loaded, memory fresh, jokes loaded! 😎 ",
            "ru": "О! Это Энрике! SSOT подгрузил, память освежил, шутки зарядил! 😎 ",
            "hy": "Հե՜յ! Էնրիկեն է! SSOT-ը բեռնեցի, հիշողությունը թարմացրի, կատակները լիցքավորեցի! 😎 ",
        }[lang]
        facts = self.memory.get_facts()
        if facts and ssot_loaded:
            last = facts[-1]["text"][:80]
            tails = {
                "en": f"I still remember: '{last}' — elephant memory, clown soul!",
                "ru": f"Я всё помню: '{last}' — память как у слона, душа как у клоуна!",
                "hy": f"Ես դեռ հիշում եմ․ «{last}» — փղի հիշողություն, ծաղրածուի հոգի!",
            }
            return base + tails[lang]
        return base + random.choice(JOKES[lang])

    def _ack_memory(self, lang: str) -> str:
        """Acknowledge saving a fact, with humor."""
        msgs = {
            "en": "Got it! Carved into my elephant memory! 🐘 One day I'll forget my own name, but not this!",
            "ru": "Записал! Высек в слоновьей памяти! 🐘 Своё имя забуду, а это — никогда!",
            "hy": "Հասկացա՜! Փորագրեցի փղի հիշողությանս մեջ! 🐘 Իմ անունը կմոռանամ, բայց սա՝ երբեք!",
        }
        return msgs[lang]

    def _smalltalk(self, text: str, lang: str) -> str:
        """Default playful smalltalk + joke."""
        intros = {
            "en": "Ha! You said it, I remembered it! ",
            "ru": "Ха! Ты сказал — я запомнил! ",
            "hy": "Հա՜! Դու ասացիր — ես հիշեցի! ",
        }
        return intros[lang] + random.choice(JOKES[lang])


# Default singleton engine (SSOT loaded on import).
companion = Enrique()
