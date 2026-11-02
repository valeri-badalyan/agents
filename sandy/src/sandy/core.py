"""Core logic for Sandy — музыкальный директор (RU/EN)."""

from __future__ import annotations

import logging
import re
from itertools import pairwise
from typing import Any

from sandy.exceptions import BriefError, MoodError, MusicKeyError, RehearsalError, SetlistError

logger = logging.getLogger(__name__)

SUPPORTED_LANGS: tuple[str, ...] = ("ru", "en")
LANG_ALIASES: dict[str, str] = {"russian": "ru", "english": "en"}

# Mood -> musical direction. bpm is (min, max).
MOODS: dict[str, dict[str, Any]] = {
    "epic": {"genres": ["orchestral", "hybrid trailer"], "bpm": (80, 110), "mode": "minor",
             "instruments": ["струнные", "медь", "большие барабаны", "хор"],
             "ru": "эпично", "en": "epic"},
    "happy": {"genres": ["pop", "funk", "indie pop"], "bpm": (110, 128), "mode": "major",
              "instruments": ["гитара", "бас", "хлопки", "синт-лиды"],
              "ru": "радостно", "en": "happy"},
    "sad": {"genres": ["piano ballad", "ambient", "neo-classical"], "bpm": (60, 80), "mode": "minor",
            "instruments": ["фортепиано", "виолончель", "пэды"],
            "ru": "грустно", "en": "sad"},
    "calm": {"genres": ["lo-fi", "ambient", "acoustic"], "bpm": (70, 90), "mode": "major",
             "instruments": ["rhodes", "акустическая гитара", "мягкие барабаны"],
             "ru": "спокойно", "en": "calm"},
    "energetic": {"genres": ["edm", "rock", "drum & bass"], "bpm": (125, 175), "mode": "minor",
                  "instruments": ["дисторшн-гитара", "синт-бас", "бочка four-on-the-floor"],
                  "ru": "энергично", "en": "energetic"},
    "tense": {"genres": ["dark ambient", "hybrid score"], "bpm": (90, 120), "mode": "minor",
              "instruments": ["остинато струнных", "низкие пульсы", "райзеры"],
              "ru": "напряжённо", "en": "tense"},
    "romantic": {"genres": ["soul", "r&b", "jazz ballad"], "bpm": (65, 95), "mode": "major",
                 "instruments": ["фортепиано", "саксофон", "струнные"],
                 "ru": "романтично", "en": "romantic"},
}

MOOD_ALIASES: dict[str, str] = {
    "эпик": "epic", "эпично": "epic", "эпичный": "epic",
    "радость": "happy", "весело": "happy", "весёлый": "happy", "веселый": "happy", "радостно": "happy",
    "грусть": "sad", "грустно": "sad", "грустный": "sad",
    "спокойно": "calm", "спокойный": "calm", "релакс": "calm", "chill": "calm",
    "энергия": "energetic", "энергично": "energetic", "драйв": "energetic", "drive": "energetic",
    "напряжение": "tense", "напряжённо": "tense", "тревожно": "tense", "suspense": "tense",
    "романтика": "romantic", "романтично": "romantic", "love": "romantic",
}

# Camelot wheel: key -> code (number + A minor / B major).
CAMELOT: dict[str, str] = {
    "Ab minor": "1A", "B major": "1B", "Eb minor": "2A", "F# major": "2B",
    "Bb minor": "3A", "Db major": "3B", "F minor": "4A", "Ab major": "4B",
    "C minor": "5A", "Eb major": "5B", "G minor": "6A", "Bb major": "6B",
    "D minor": "7A", "F major": "7B", "A minor": "8A", "C major": "8B",
    "E minor": "9A", "G major": "9B", "B minor": "10A", "D major": "10B",
    "F# minor": "11A", "A major": "11B", "Db minor": "12A", "E major": "12B",
}
ENHARMONIC: dict[str, str] = {
    "G#": "Ab", "D#": "Eb", "A#": "Bb", "Gb": "F#", "C#": "Db", "Cb": "B", "E#": "F", "Fb": "E", "B#": "C",
}
# Minor keys conventionally spelled with sharps on the wheel.
MINOR_SPELLING: dict[str, str] = {"Gb": "F#", "C#": "Db"}

ARCS: tuple[str, ...] = ("rise", "wave", "peak", "chill")

GREETINGS: dict[str, str] = {
    "ru": "Привет! Я Сэнди 🎼 — музыкальный директор. Подберу звук, соберу сетлист, сведу тональности и проведу репетицию.",
    "en": "Hi! I'm Sandy 🎼 — your music director. Sound picks, setlists, key matching and rehearsals.",
}


def normalize_lang(lang: str) -> str:
    """Normalize language code to ru/en.

    Args:
        lang: Raw language code.

    Returns:
        Normalized code.

    Raises:
        BriefError: If language unsupported.
    """
    if not isinstance(lang, str):
        raise BriefError("lang must be a string")
    code = LANG_ALIASES.get(lang.strip().lower(), lang.strip().lower())
    if code not in SUPPORTED_LANGS:
        raise BriefError(f"Unsupported lang '{lang}'. Supported: ru, en")
    return code


def detect_lang(text: str) -> str:
    """Detect ru/en by alphabet (ru default)."""
    if not isinstance(text, str) or not text.strip():
        return "ru"
    low = text.lower()
    latin = sum(1 for ch in low if "a" <= ch <= "z")
    cyrillic = sum(1 for ch in low if "а" <= ch <= "я" or ch == "ё")
    return "en" if latin > cyrillic and latin > 2 else "ru"


def parse_key(key: str) -> str:
    """Parse a key like 'Am', 'C#m', 'F# major', '8A' or 'ля минор' to a Camelot code.

    Args:
        key: Key in letter, Camelot or Russian notation.

    Returns:
        Camelot code, e.g. '8A'.

    Raises:
        MusicKeyError: If key cannot be parsed.
    """
    if not isinstance(key, str) or not key.strip():
        raise MusicKeyError("key must be a non-empty string, e.g. Am, C, F#m, 8A")
    raw = key.strip()
    camelot = re.fullmatch(r"(1[0-2]|[1-9])\s*([abAB])", raw)
    if camelot:
        return f"{camelot.group(1)}{camelot.group(2).upper()}"

    ru_notes = {"до": "C", "ре": "D", "ми": "E", "фа": "F", "соль": "G", "ля": "A", "си": "B"}
    low = raw.lower()
    ru = re.fullmatch(r"(до|ре|ми|фа|соль|ля|си)(-диез| диез|-бемоль| бемоль)?\s*(мажор|минор)", low)
    if ru:
        note = ru_notes[ru.group(1)]
        acc = "#" if ru.group(2) and "диез" in ru.group(2) else "b" if ru.group(2) else ""
        raw = f"{note}{acc} {'minor' if ru.group(3) == 'минор' else 'major'}"

    m = re.fullmatch(r"([A-Ga-g])([#b]?)\s*(m|min|minor|maj|major|M)?", raw.strip())
    if not m:
        raise MusicKeyError(f"Не понимаю тональность '{key}'. Примеры: Am, C, F#m, Bb major, 8A, ля минор")
    note = m.group(1).upper() + m.group(2)
    quality = m.group(3) or ""
    is_minor = quality in ("m", "min", "minor")
    note = ENHARMONIC.get(note, note)
    if is_minor:
        note = MINOR_SPELLING.get(note, note)
    name = f"{note} {'minor' if is_minor else 'major'}"
    if name not in CAMELOT:
        raise MusicKeyError(f"Неизвестная тональность '{key}'")
    return CAMELOT[name]


def key_distance(code_a: str, code_b: str) -> int:
    """Harmonic distance between two Camelot codes (0 = same, 1 = perfect neighbour)."""
    num_a, let_a = int(code_a[:-1]), code_a[-1]
    num_b, let_b = int(code_b[:-1]), code_b[-1]
    diff = abs(num_a - num_b)
    step = min(diff, 12 - diff)
    return step + (0 if let_a == let_b else 1)


def _validate_bpm(bpm: Any, field: str, exc: type[Exception]) -> float:
    """Validate BPM is a positive number in a sane range."""
    if isinstance(bpm, bool) or not isinstance(bpm, (int, float)):
        raise exc(f"{field} must be a number, got {bpm!r}")
    if not 20 <= float(bpm) <= 300:
        raise exc(f"{field} must be between 20 and 300 BPM")
    return float(bpm)


class Sandy:
    """Музыкальный директор: подбор музыки, сетлисты, тональности, репетиции, брифы."""

    def __init__(self, lang: str = "ru") -> None:
        """Initialize Sandy agent.

        Args:
            lang: Default language ru/en.
        """
        try:
            self.lang: str = normalize_lang(lang)
        except BriefError:
            self.lang = "ru"
        self.name: str = "sandy"
        self.history: list[dict[str, Any]] = []

    def greet(self, lang: str | None = None) -> str:
        """Return greeting."""
        code = normalize_lang(lang) if lang else self.lang
        self.history.append({"action": "greet", "lang": code})
        return GREETINGS[code]

    def list_moods(self) -> list[str]:
        """Return supported moods."""
        return list(MOODS)

    def recommend_music(self, mood: str, scene: str = "", bpm: float | None = None) -> dict[str, Any]:
        """Recommend a musical direction for a mood/scene.

        Args:
            mood: epic/happy/sad/calm/energetic/tense/romantic (RU aliases ok).
            scene: Optional scene description (goes into the brief).
            bpm: Optional target BPM; clamped into the mood range.

        Returns:
            Dict with mood, genres, bpm, mode, instruments, scene, tips.

        Raises:
            MoodError: If mood unknown or bpm invalid.
        """
        if not isinstance(mood, str) or not mood.strip():
            raise MoodError("mood must be a non-empty string")
        key = MOOD_ALIASES.get(mood.strip().lower(), mood.strip().lower())
        if key not in MOODS:
            raise MoodError(f"Не знаю настроение '{mood}'. Знаю: {', '.join(MOODS)}")
        info = MOODS[key]
        low, high = info["bpm"]
        if bpm is not None:
            target = _validate_bpm(bpm, "bpm", MoodError)
            chosen = min(max(target, low), high)
        else:
            chosen = (low + high) / 2
        tips = [
            f"Держи темп около {round(chosen)} BPM ({low}–{high}).",
            f"Лад: {'минор' if info['mode'] == 'minor' else 'мажор'}.",
            "Оставь место для голоса/диалога: убери середину 1–3 кГц под речь.",
        ]
        result = {
            "mood": key,
            "genres": list(info["genres"]),
            "bpm": round(chosen),
            "bpm_range": [low, high],
            "mode": info["mode"],
            "instruments": list(info["instruments"]),
            "scene": scene.strip() if isinstance(scene, str) else "",
            "tips": tips,
        }
        logger.info("Recommended mood=%s bpm=%s", key, result["bpm"])
        self.history.append({"action": "recommend", "mood": key})
        return result

    def key_compatibility(self, key_a: str, key_b: str) -> dict[str, Any]:
        """Check harmonic compatibility of two keys (Camelot wheel).

        Args:
            key_a: First key.
            key_b: Second key.

        Returns:
            Dict with camelot codes, distance, compatible flag and advice.
        """
        code_a, code_b = parse_key(key_a), parse_key(key_b)
        dist = key_distance(code_a, code_b)
        compatible = dist <= 1
        if dist == 0:
            advice = "Та же тональность — сводится идеально."
        elif compatible:
            advice = "Соседи по кругу Camelot — гармоничный переход."
        elif dist == 2:
            advice = "Энергетический скачок: переходи через брейк или ударный проигрыш."
        else:
            advice = "Конфликт тональностей: нужна модуляция, пауза или транспонирование."
        self.history.append({"action": "keys", "pair": [code_a, code_b]})
        return {"a": code_a, "b": code_b, "distance": dist, "compatible": compatible, "advice": advice}

    def build_setlist(self, songs: list[dict[str, Any]], arc: str = "rise") -> dict[str, Any]:
        """Order songs into a setlist by energy arc and note transitions.

        Args:
            songs: List of dicts with title, bpm, optional key and energy (1–10).
            arc: rise (нарастание) / wave (волны) / peak (пик в середине) / chill (на спад).

        Returns:
            Dict with ordered setlist, transitions, total and arc.

        Raises:
            SetlistError: If input invalid.
        """
        if not isinstance(songs, list) or not songs:
            raise SetlistError("Нужен хотя бы один трек: [{'title': ..., 'bpm': ..., 'energy': 1-10}]")
        if arc not in ARCS:
            raise SetlistError(f"Unknown arc '{arc}'. Use: {', '.join(ARCS)}")
        items: list[dict[str, Any]] = []
        for i, song in enumerate(songs):
            if not isinstance(song, dict) or not str(song.get("title", "")).strip():
                raise SetlistError(f"Song #{i + 1} must be a dict with a title")
            bpm = _validate_bpm(song.get("bpm"), f"bpm of '{song['title']}'", SetlistError)
            energy = song.get("energy")
            if energy is None:
                energy = max(1, min(10, round((bpm - 60) / 12)))
            if isinstance(energy, bool) or not isinstance(energy, (int, float)) or not 1 <= energy <= 10:
                raise SetlistError(f"energy of '{song['title']}' must be 1–10")
            item = {"title": str(song["title"]).strip(), "bpm": bpm, "energy": energy}
            if song.get("key"):
                try:
                    item["camelot"] = parse_key(str(song["key"]))
                except MusicKeyError as exc:
                    raise SetlistError(str(exc)) from exc
                item["key"] = str(song["key"])
            items.append(item)

        by_energy = sorted(items, key=lambda s: (s["energy"], s["bpm"]))
        if arc == "rise":
            ordered = by_energy
        elif arc == "chill":
            ordered = by_energy[::-1]
        elif arc == "peak":
            left, right = by_energy[::2], by_energy[1::2]
            ordered = left + right[::-1]
        else:  # wave: alternate low/high, ending high
            ordered, lo, hi = [], 0, len(by_energy) - 1
            while lo <= hi:
                ordered.append(by_energy[lo])
                if lo != hi:
                    ordered.append(by_energy[hi])
                lo, hi = lo + 1, hi - 1

        transitions: list[dict[str, Any]] = []
        for prev, nxt in pairwise(ordered):
            note_parts = []
            jump = abs(nxt["bpm"] - prev["bpm"])
            if jump > 20:
                note_parts.append(f"скачок темпа {round(jump)} BPM — нужен брейк/отсчёт")
            if ("camelot" in prev and "camelot" in nxt
                    and key_distance(prev["camelot"], nxt["camelot"]) > 1):
                note_parts.append(f"тональности {prev['camelot']}→{nxt['camelot']} конфликтуют")
            transitions.append({
                "from": prev["title"], "to": nxt["title"],
                "note": "; ".join(note_parts) or "плавный переход",
            })
        self.history.append({"action": "setlist", "arc": arc, "count": len(ordered)})
        return {"arc": arc, "setlist": [s["title"] for s in ordered], "items": ordered,
                "transitions": transitions, "total": len(ordered)}

    def rehearsal_plan(self, minutes: int, songs: list[str], band_size: int = 4) -> list[dict[str, Any]]:
        """Build a timed rehearsal plan.

        Args:
            minutes: Total rehearsal time (30–480).
            songs: Song titles to rehearse.
            band_size: Number of musicians (affects soundcheck time).

        Returns:
            List of blocks with start, duration and task.

        Raises:
            RehearsalError: If input invalid or time too short.
        """
        if isinstance(minutes, bool) or not isinstance(minutes, int) or not 30 <= minutes <= 480:
            raise RehearsalError("minutes must be an int between 30 and 480")
        if not isinstance(songs, list) or not songs or not all(isinstance(s, str) and s.strip() for s in songs):
            raise RehearsalError("songs must be a non-empty list of titles")
        if isinstance(band_size, bool) or not isinstance(band_size, int) or band_size < 1:
            raise RehearsalError("band_size must be a positive int")

        soundcheck = min(10 + band_size * 2, 30)
        warmup = 10
        runthrough = 15 if minutes >= 90 else 0
        breaks = (minutes // 50) * 5 if minutes >= 90 else 0
        work = minutes - soundcheck - warmup - runthrough - breaks
        per_song = work // len(songs)
        if per_song < 5:
            raise RehearsalError("Слишком мало времени: меньше 5 минут на песню. Сократи список или добавь время.")

        plan: list[dict[str, Any]] = []
        t = 0

        def add(duration: int, task: str) -> None:
            nonlocal t
            plan.append({"start": t, "minutes": duration, "task": task})
            t += duration

        add(soundcheck, "Саундчек и линия (мониторы, баланс)")
        add(warmup, "Разогрев: грув-джем по метроному")
        breaks_left = breaks // 5
        since_break = soundcheck + warmup
        for title in songs:
            add(per_song, f"«{title.strip()}»: разбор сложных мест → прогон целиком")
            since_break += per_song
            if breaks_left and since_break >= 50:
                add(5, "Перерыв")
                breaks_left -= 1
                since_break = 0
        if runthrough:
            add(runthrough, "Сквозной прогон сетлиста без остановок")
        leftover = minutes - t
        if leftover > 0:
            add(leftover, "Заметки, запись проблемных мест, план на следующую репетицию")
        self.history.append({"action": "rehearsal", "minutes": minutes, "songs": len(songs)})
        return plan

    def soundtrack_brief(self, project: str, scenes: list[dict[str, str]], lang: str | None = None) -> str:
        """Generate a markdown soundtrack brief for a video/game/event.

        Args:
            project: Project name.
            scenes: List of {"name": ..., "mood": ...}.
            lang: ru/en.

        Returns:
            Markdown brief.

        Raises:
            BriefError: If input invalid.
        """
        if not isinstance(project, str) or not project.strip():
            raise BriefError("project must be a non-empty string")
        if not isinstance(scenes, list) or not scenes:
            raise BriefError("scenes must be a non-empty list of {'name', 'mood'}")
        code = normalize_lang(lang) if lang else self.lang
        title = "Музыкальный бриф" if code == "ru" else "Music brief"
        lines = [f"# {title}: {project.strip()}", ""]
        for i, scene in enumerate(scenes, 1):
            if not isinstance(scene, dict) or not scene.get("name") or not scene.get("mood"):
                raise BriefError(f"Scene #{i} needs 'name' and 'mood'")
            try:
                rec = self.recommend_music(scene["mood"], scene["name"])
            except MoodError as exc:
                raise BriefError(str(exc)) from exc
            mood_label = MOODS[rec["mood"]][code]
            lines += [
                f"## {i}. {scene['name']}",
                f"- {'Настроение' if code == 'ru' else 'Mood'}: {mood_label}",
                f"- {'Жанры' if code == 'ru' else 'Genres'}: {', '.join(rec['genres'])}",
                f"- BPM: {rec['bpm']} ({rec['bpm_range'][0]}–{rec['bpm_range'][1]})",
                f"- {'Лад' if code == 'ru' else 'Mode'}: {rec['mode']}",
                f"- {'Инструменты' if code == 'ru' else 'Instruments'}: {', '.join(rec['instruments'])}",
                "",
            ]
        self.history.append({"action": "brief", "project": project.strip(), "scenes": len(scenes)})
        return "\n".join(lines).rstrip() + "\n"

    def chat(self, text: str, lang: str | None = None) -> dict[str, Any]:
        """Chat with simple intent routing.

        Args:
            text: User message.
            lang: Optional forced language.

        Returns:
            Dict with lang, intent, reply.

        Raises:
            BriefError: If text empty.
        """
        if not isinstance(text, str) or not text.strip():
            raise BriefError("Напиши запрос — например: «Сэнди, музыка для грустной сцены»")
        code = normalize_lang(lang) if lang else detect_lang(text)
        low = text.lower()
        ru = code == "ru"

        mood = next((m for m in list(MOOD_ALIASES) + list(MOODS) if m in low), None)
        if mood:
            rec = self.recommend_music(mood)
            intent = "recommend"
            reply = (f"{'Направление' if ru else 'Direction'}: {', '.join(rec['genres'])}, "
                     f"{rec['bpm']} BPM, {rec['mode']}. "
                     f"{'Инструменты' if ru else 'Instruments'}: {', '.join(rec['instruments'])}.")
        elif any(w in low for w in ["сетлист", "setlist", "порядок", "плейлист", "playlist"]):
            intent = "setlist"
            reply = ("Пришли треки: название, BPM, тональность, энергия 1–10 — и дугу (rise/wave/peak/chill)."
                     if ru else "Send tracks: title, BPM, key, energy 1–10 — and an arc (rise/wave/peak/chill).")
        elif any(w in low for w in ["тональн", "key", "camelot", "сведени", "mix"]):
            intent = "keys"
            reply = ("Назови две тональности (например Am и C) — проверю, сводятся ли."
                     if ru else "Give me two keys (e.g. Am and C) — I'll check if they mix.")
        elif any(w in low for w in ["репетиц", "rehears"]):
            intent = "rehearsal"
            reply = ("Сколько минут, какие песни и сколько музыкантов? Распишу репетицию по блокам."
                     if ru else "How many minutes, which songs, how many musicians? I'll lay out the rehearsal.")
        elif any(w in low for w in ["бриф", "brief", "саундтрек", "soundtrack"]):
            intent = "brief"
            reply = ("Дай название проекта и сцены с настроением — соберу музыкальный бриф."
                     if ru else "Give me the project name and scenes with moods — I'll write a music brief.")
        else:
            intent = "greet"
            reply = GREETINGS[code] + ("\nНастроения: " if ru else "\nMoods: ") + ", ".join(MOODS)
        self.history.append({"action": "chat", "lang": code, "intent": intent})
        return {"lang": code, "intent": intent, "reply": reply}

    def get_history(self) -> list[dict[str, Any]]:
        """Return interaction history."""
        return list(self.history)


engine = Sandy()
