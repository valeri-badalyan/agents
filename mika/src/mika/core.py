"""Core logic for Mika — весёлый IT/интернет-провайдер (RU/EN/HY)."""

from __future__ import annotations

import logging
import random
from typing import Any

from mika.exceptions import ConnectionError, CoverageError, DiagnosisError, ReportError, TariffError

logger = logging.getLogger(__name__)

SUPPORTED_LANGS: tuple[str, ...] = ("ru", "en", "hy")
LANG_ALIASES: dict[str, str] = {"am": "hy", "armenian": "hy", "russian": "ru", "english": "en"}

TARIFFS: list[dict[str, Any]] = [
    {"id": "start", "name": "Старт", "speed_mbps": 50, "price": 390, "ping_ms": 15,
     "for": ["family", "surfing", "social"], "desc_ru": "Для соцсетей и кино по вечерам",
     "desc_en": "For socials and evening movies", "desc_hy": "Սոցցանցերի և երեկոյան ֆիլմերի համար"},
    {"id": "home", "name": "Домашний", "speed_mbps": 100, "price": 490, "ping_ms": 10,
     "for": ["family", "remote", "study"], "desc_ru": "Учёба, удалёнка и 4K без буферизации",
     "desc_en": "Study, remote work and 4K with no buffering", "desc_hy": "Ուսում, հեռավար աշխատանք և 4K առանց կանգերի"},
    {"id": "gamer", "name": "Геймерский", "speed_mbps": 500, "price": 790, "ping_ms": 3,
     "for": ["gaming", "stream", "cybersport"], "desc_ru": "Пинг как у киборга, фраги как у легенды",
     "desc_en": "Cyborg-level ping, legendary frags", "desc_hy": "Պինգը՝ կիբօրգի պես, ֆրագները՝ լեգենդի պես"},
    {"id": "ultra", "name": "Ультра Гигабит", "speed_mbps": 1000, "price": 990, "ping_ms": 2,
     "for": ["stream", "office", "smart_home"], "desc_ru": "Качает быстрее, чем ты моргаешь",
     "desc_en": "Downloads faster than you blink", "desc_hy": "Ներբեռնում է ավելի արագ, քան դու թարթում ես"},
    {"id": "office", "name": "Офисный", "speed_mbps": 300, "price": 1490, "ping_ms": 5,
     "for": ["office", "business"], "desc_ru": "Симметрия и белый IP для серьёзных дел",
     "desc_en": "Symmetric channel and static IP for business", "desc_hy": "Սիմետրիկ կապ և ստատիկ IP լուրջ գործերի համար"},
]

COVERAGE_ZONES: dict[str, dict[str, Any]] = {
    "центр": {"available": True, "tech": "GPON / Ethernet", "eta_days": 1},
    "спальник": {"available": True, "tech": "Ethernet", "eta_days": 1},
    "новостройка": {"available": True, "tech": "GPON", "eta_days": 2},
    "частный сектор": {"available": True, "tech": "GPON / 4G-box", "eta_days": 3},
    "деревня": {"available": False, "tech": "4G-box / спутник", "eta_days": 5},
    "center": {"available": True, "tech": "GPON / Ethernet", "eta_days": 1},
    "village": {"available": False, "tech": "4G-box / satellite", "eta_days": 5},
    "կենտրոն": {"available": True, "tech": "GPON / Ethernet", "eta_days": 1},
    "գյուղ": {"available": False, "tech": "4G-box / արբանյակ", "eta_days": 5},
}

JOKES: dict[str, list[str]] = {
    "ru": [
        "Пинг высокий? Это интернет медитирует. Сейчас вернём его в реальность 🧘‍♂️",
        "Роутер тоже устаёт — дайте ему поспать 30 секунд, он скажет спасибо скоростью 😴➡️🚀",
        "Наш гигабит такой быстрый, что торренты сами боятся качаться! 😄",
        "Wi-Fi ловит даже в холодильнике. Проверено колбасой 🌭",
    ],
    "en": [
        "High ping? Your internet is meditating. Let's bring it back to reality 🧘",
        "Routers get tired too — 30 seconds nap = +50 happiness 🚀",
        "Our gigabit is so fast, torrents download themselves! 😄",
    ],
    "hy": [
        "Պինգը բարձր է՞։ Ինտերնետը մեդիտացիա է անում։ Վերադարձնենք իրականություն 🧘",
        "Ռոութերն էլ է հոգնում — 30 վայրկյան քուն, և նա շնորհակալ կլինի արագությամբ 🚀",
        "Մեր գիգաբիթն այնքան արագ է, որ տոռենտներն իրենք են վախենում 😄",
    ],
}

GREETINGS: dict[str, str] = {
    "ru": "Привет! Я Мика 📡 — твой весёлый провайдер! Подключу, ускорю, рассмешу!",
    "en": "Hey! I'm Mika 📡 — your cheerful provider! I connect, I boost, I make you laugh!",
    "hy": "Ողջո՜ւյն։ Ես Միկան եմ 📡 — քո ուրախ պրովայդերը։ Միացնում եմ, արագացնում եմ, ծիծաղեցնում եմ!",
}


def normalize_lang(lang: str) -> str:
    """Normalize language code to ru/en/hy.

    Args:
        lang: Raw language code (ru, en, hy/am, aliases).

    Returns:
        Normalized code.

    Raises:
        ReportError: If language unsupported.
    """
    if not isinstance(lang, str):
        raise ReportError("lang must be a string")
    code = lang.strip().lower()
    code = LANG_ALIASES.get(code, code)
    if code not in SUPPORTED_LANGS:
        raise ReportError(f"Unsupported lang '{lang}'. Supported: ru, en, hy(am)")
    return code


def detect_lang(text: str) -> str:
    """Detect language by alphabet: Armenian, English or Russian default.

    Args:
        text: User text.

    Returns:
        One of ru, en, hy.
    """
    if not isinstance(text, str) or not text.strip():
        return "ru"
    lowered = text.lower()
    if any("ա" <= ch <= "ֆ" or ch in "և" for ch in lowered):
        return "hy"
    latin = sum(1 for ch in lowered if "a" <= ch <= "z")
    cyrillic = sum(1 for ch in lowered if "а" <= ch <= "я" or ch == "ё")
    if latin > cyrillic and latin > 2:
        return "en"
    return "ru"


def _validate_positive(value: float, field_name: str, exc: type[Exception]) -> float:
    """Validate that value is a non-negative number.

    Args:
        value: Value to check.
        field_name: Field name for errors.
        exc: Exception class to raise.

    Returns:
        Value as float.

    Raises:
        Exception: If invalid.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise exc(f"{field_name} must be a number, got {value!r}")
    if float(value) < 0:
        raise exc(f"{field_name} must be >= 0")
    return float(value)


class Mika:
    """Весёлый провайдер: тарифы, покрытие, диагностика, подключение."""

    def __init__(self, lang: str = "ru") -> None:
        """Initialize Mika agent.

        Args:
            lang: Default language ru/en/hy.
        """
        try:
            self.lang: str = normalize_lang(lang)
        except ReportError:
            self.lang = "ru"
        self.name: str = "mika"
        self.history: list[dict[str, Any]] = []
        logger.debug("Mika agent initialized with lang=%s", self.lang)

    def greet(self, lang: str | None = None) -> str:
        """Return greeting in requested language plus random joke.

        Args:
            lang: Optional override language.

        Returns:
            Greeting string.
        """
        code = normalize_lang(lang) if lang else self.lang
        joke = random.choice(JOKES[code])
        result = f"{GREETINGS[code]}\n{joke}"
        self.history.append({"action": "greet", "lang": code})
        return result

    def list_tariffs(self) -> list[dict[str, Any]]:
        """Return all tariffs.

        Returns:
            List of tariff dicts.
        """
        logger.info("Listed %d tariffs", len(TARIFFS))
        return [dict(t) for t in TARIFFS]

    def recommend_tariff(
        self,
        usage: str = "family",
        budget: float | None = None,
        min_speed: float = 0,
    ) -> dict[str, Any]:
        """Recommend cheapest fitting tariff with humor.

        Args:
            usage: gaming/stream/family/remote/study/office/business/surfing.
            budget: Max monthly price, None = unlimited.
            min_speed: Minimum speed in Mbps.

        Returns:
            Tariff dict with extra 'joke' key.

        Raises:
            TariffError: If nothing fits.
        """
        if not isinstance(usage, str) or not usage.strip():
            raise TariffError("usage must be a non-empty string")
        use = usage.strip().lower()
        _validate_positive(min_speed, "min_speed", TariffError)
        if budget is not None:
            _validate_positive(budget, "budget", TariffError)

        candidates = [t for t in TARIFFS if t["speed_mbps"] >= min_speed]
        if budget is not None:
            candidates = [t for t in candidates if t["price"] <= budget]
        preferred = [t for t in candidates if use in t["for"]]
        pool = preferred or candidates
        if not pool:
            raise TariffError("Нет тарифа под такой бюджет/скорость — увеличь бюджет, я уже плачу от жадности 😄")
        best = min(pool, key=lambda t: t["price"])
        result = dict(best)
        result["joke"] = random.choice(JOKES["ru"])
        logger.info("Recommended tariff %s for usage=%s", best["id"], use)
        self.history.append({"action": "recommend", "tariff": best["id"]})
        return result

    def check_coverage(self, address: str) -> dict[str, Any]:
        """Check coverage by free-form address.

        Args:
            address: Address or district string.

        Returns:
            Dict with available/tech/eta_days/matched_zone.

        Raises:
            CoverageError: If address empty.
        """
        if not isinstance(address, str) or not address.strip():
            raise CoverageError("Напиши адрес — я не экстрасенс, хотя почти 😄 (пример: центр, новостройка, деревня)")
        text = address.strip().lower()
        for zone, info in COVERAGE_ZONES.items():
            if zone in text or text in zone:
                result: dict[str, Any] = {"address": address.strip(), "matched_zone": zone, **info}
                logger.info("Coverage hit zone=%s", zone)
                self.history.append({"action": "coverage", "zone": zone})
                return result
        fallback: dict[str, Any] = {
            "address": address.strip(),
            "matched_zone": "unknown",
            "available": True,
            "tech": "Ethernet / GPON — уточнит инженер",
            "eta_days": 2,
        }
        logger.info("Coverage fallback for address=%s", address)
        return fallback

    def diagnose(
        self,
        measured_speed: float,
        expected_speed: float,
        ping_ms: float,
        wifi: bool = True,
    ) -> dict[str, Any]:
        """Diagnose connection problems and give funny steps.

        Args:
            measured_speed: Real speed in Mbps.
            expected_speed: Tariff speed in Mbps.
            ping_ms: Ping in ms.
            wifi: True if connected via Wi-Fi.

        Returns:
            Dict with level (ok/slow/bad), issues, steps.

        Raises:
            DiagnosisError: If inputs invalid.
        """
        try:
            ms = _validate_positive(measured_speed, "measured_speed", DiagnosisError)
            es = _validate_positive(expected_speed, "expected_speed", DiagnosisError)
            ping = _validate_positive(ping_ms, "ping_ms", DiagnosisError)
        except DiagnosisError:
            raise
        except Exception as exc:
            raise DiagnosisError(str(exc)) from exc
        if es == 0:
            raise DiagnosisError("expected_speed must be > 0 (тариф 0 Мбит/с — это голубиная почта 🕊️)")

        ratio = ms / es
        issues: list[str] = []
        steps: list[str] = []
        if ratio >= 0.8 and ping < 50:
            level = "ok"
            steps.append("Всё отлично! Можешь качать, играть и смеяться одновременно 😄")
        elif ratio >= 0.4:
            level = "slow"
            issues.append("Скорость ниже тарифа")
            steps.append("1. Перезагрузи роутер на 30 секунд (ему тоже нужен кофе-пауза ☕)")
            steps.append("2. Встань ближе к роутеру — стены едят Wi-Fi как чипсы 🧱")
            if wifi:
                steps.append("3. Попробуй по кабелю — кабель не врёт, в отличие от Wi-Fi 😏")
            if ping >= 50:
                issues.append("Высокий пинг")
                steps.append("4. Выключи торренты и облака на фоне — они сосут канал как спагетти 🍝")
        else:
            level = "bad"
            issues.append("Скорость сильно ниже тарифа")
            if ping >= 100:
                issues.append("Очень высокий пинг")
            steps.append("1. Перезагрузи роутер и ONT (выкл 30 сек) 🔌")
            steps.append("2. Проверь кабель — кот мог его погрызть, коты это любят 🐱")
            steps.append("3. Замерь по кабелю напрямую, без роутера")
            steps.append("4. Позвони нам 8-800-555-35-35 — приедем с бубном и обжимкой 🛠️")
        logger.info("Diagnosed level=%s ratio=%.2f ping=%s", level, ratio, ping)
        self.history.append({"action": "diagnose", "level": level})
        return {"level": level, "ratio": round(ratio, 3), "issues": issues, "steps": steps}

    def connection_steps(self, home_type: str = "apartment") -> list[str]:
        """Return funny connection steps.

        Args:
            home_type: apartment/house/office.

        Returns:
            List of steps.

        Raises:
            ConnectionError: If type unknown.
        """
        if not isinstance(home_type, str):
            raise ConnectionError("home_type must be a string")
        key = home_type.strip().lower()
        mapping: dict[str, list[str]] = {
            "apartment": [
                "1. Оставляешь заявку — 1 минута, быстрее чем заварить доширак 🍜",
                "2. Инженер приходит за 1 день с кабелем и улыбкой 😁",
                "3. Монтаж 30-60 минут, сверлим аккуратно, как хирурги 🔧",
                "4. Настраиваем Wi-Fi, даём весёлое имя сети (например Mika_Gigabit_Пушка) 📡",
                "5. Ты платишь первый месяц и улетаешь в гигабит 🚀",
            ],
            "house": [
                "1. Проверяем GPON или ставим 4G-box — домик в деревне тоже хочет Netflix 🏡",
                "2. Тянем оптику до 200м бесплатно, дальше — поцелуй инженера 😘 (шутка, по прайсу)",
                "3. Ставим уличный бокс + роутер с мощным Wi-Fi 📶",
                "4. Тестируем скорость прямо на крыльце 🧪",
            ],
            "office": [
                "1. Аудит объекта и договор за 1 день 📄",
                "2. Выделенная линия + белый IP, как у взрослых 🏢",
                "3. Резервный 4G-канал, чтобы 1С не падала в обморок 💼",
                "4. SLA и инженер на speed-dial 📞",
            ],
        }
        aliases = {"квартира": "apartment", "дом": "house", "частный": "house", "офис": "office"}
        key = aliases.get(key, key)
        if key not in mapping:
            raise ConnectionError(f"Не знаю такой тип '{home_type}'. Знаю: apartment, house, office 🏠")
        return list(mapping[key])

    def chat(self, text: str, lang: str | None = None) -> dict[str, Any]:
        """Chat with auto language detection, tariffs/coverage/diagnosis routing.

        Args:
            text: User message.
            lang: Optional forced language.

        Returns:
            Dict with lang, reply.
        """
        if not isinstance(text, str) or not text.strip():
            raise ReportError("Напиши хоть что-нибудь, а то я скучаю без твоих сообщений 🥺")
        code = normalize_lang(lang) if lang else detect_lang(text)
        low = text.lower()
        if any(w in low for w in ["тариф", "tariff", "սակագին", "цен", "price", "գին", "сколько"]):
            tariffs = self.list_tariffs()
            lines = [f"• {t['name']}: {t['speed_mbps']} Мбит/с — {t['price']} ₽/мес 😎" for t in tariffs]
            reply = ("Держи тарифы, выбирай как пирожки 🥟:\n" if code == "ru" else
                     "Here are tariffs, pick like pastries 🥟:\n" if code == "en" else
                     "Ահա սակագները, ընտրիր ինչպես կարկանդակ 🥟:\n") + "\n".join(lines)
        elif any(w in low for w in ["покрыт", "адрес", "coverage", "address", "ծածկույթ", "подключ", "connect", "միաց"]):
            reply = ("Кидай адрес — проверю покрытие быстрее, чем ты скажешь «гигабит»! 😄 "
                     "(например: Мика, покрытие центр)" if code == "ru" else
                     "Drop your address — I'll check coverage faster than you say gigabit! 😄" if code == "en" else
                     "Ուղարկիր հասցեն — կստուգեմ ծածկույթն ավելի արագ, քան կասես «գիգաբիթ» 😄")
        elif any(w in low for w in ["тормозит", "медлен", "slow", "lag", "դանդաղ", "пинг", "ping", "փինգ", "не работает"]):
            reply = ("Ой-ой, интернет чихает? 🤧 Скажи: замер скорости + тариф (например: 20 из 100, пинг 80, wifi) — "
                     "поставлю диагноз и выпишу рецепт! 💊" if code == "ru" else
                     "Uh-oh, internet is sneezing? 🤧 Tell me: measured speed + plan (e.g. 20 of 100, ping 80, wifi) — "
                     "I'll diagnose and prescribe! 💊" if code == "en" else
                     "Օհ, ինտերնետը փռշտո՞ւմ է 🤧։ Ասա՝ չափված արագություն + սակագին (օրինակ՝ 20-ը 100-ից, պինգ 80) — "
                     "ախտորոշում կտամ և դեղատոմս կգրեմ 💊")
        elif any(w in low for w in ["анекдот", "шутка", "прикол", "joke", "funny", "կատակ", "անեկդոտ"]):
            reply = random.choice(JOKES[code])
        else:
            hello = GREETINGS[code]
            reply = (f"{hello}\nМогу: показать тарифы 💰, проверить адрес 🏠, вылечить тормоза 🛠️, подключить за 1 день 🚀. "
                     f"Просто скажи! А вот тебе для настроения: {random.choice(JOKES[code])}" if code == "ru" else
                     f"{hello}\nI can: show tariffs 💰, check coverage 🏠, fix slowness 🛠️, connect in 1 day 🚀. Just ask! "
                     f"Mood booster: {random.choice(JOKES[code])}" if code == "en" else
                     f"{hello}\nԿարող եմ՝ ցույց տալ սակագներ 💰, ստուգել ծածկույթ 🏠, բուժել դանդաղություն 🛠️, միացնել 1 օրում 🚀։ "
                     f"Պարզապես ասա։ Իսկ տրամադրության համար՝ {random.choice(JOKES[code])}")
        self.history.append({"action": "chat", "lang": code})
        logger.info("Chat replied lang=%s", code)
        return {"lang": code, "reply": reply}

    def get_history(self) -> list[dict[str, Any]]:
        """Return interaction history.

        Returns:
            List of history dicts.
        """
        return list(self.history)


engine = Mika()
