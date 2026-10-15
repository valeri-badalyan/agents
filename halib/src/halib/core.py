"""Core logic for Halib — designer agent.

Covers: design concept, color palette, typography pairing,
UI layout structure, logo brief, brand style guide and honest design audit.
"""

from __future__ import annotations

import hashlib
import logging
from typing import Any

from halib.exceptions import (
    AuditError,
    ConceptError,
    LayoutError,
    PaletteError,
    TypographyError,
)

logger = logging.getLogger(__name__)

STYLES: tuple[str, ...] = (
    "minimal",
    "brutalism",
    "neubrutalism",
    "glassmorphism",
    "flat",
    "material",
    "retro",
    "luxury",
    "playful",
    "corporate",
)

MOODS: tuple[str, ...] = (
    "calm",
    "bold",
    "premium",
    "friendly",
    "energetic",
    "trustworthy",
    "elegant",
)

BASE_PALETTES: dict[str, list[str]] = {
    "calm": ["#E8F0FE", "#AECBFA", "#4285F4", "#1A3C6E", "#0B1B33"],
    "bold": ["#FFF200", "#FF3D00", "#1A1A1A", "#FFFFFF", "#6C00FF"],
    "premium": ["#0A0A0A", "#1C1C1E", "#C9A96A", "#F5F0E8", "#6E6E73"],
    "friendly": ["#FFF7ED", "#FDBA74", "#FB7185", "#34D399", "#1F2937"],
    "energetic": ["#00F5D4", "#00BBF9", "#9B5DE5", "#F15BB5", "#111111"],
    "trustworthy": ["#EFF6FF", "#93C5FD", "#2563EB", "#1E3A8A", "#0F172A"],
    "elegant": ["#FAFAF9", "#E7E5E4", "#A8A29E", "#44403C", "#1C1917"],
}

FONT_PAIRINGS: dict[str, dict[str, str]] = {
    "minimal": {"heading": "Inter", "body": "Inter", "accent": "Inter Tight"},
    "corporate": {"heading": "Manrope", "body": "Inter", "accent": "Manrope"},
    "luxury": {"heading": "Playfair Display", "body": "Inter", "accent": "Cormorant Garamond"},
    "playful": {"heading": "Nunito", "body": "Nunito Sans", "accent": "Caveat"},
    "retro": {"heading": "Bebas Neue", "body": "Space Grotesk", "accent": "DM Mono"},
    "brutalism": {"heading": "Archivo Black", "body": "Space Grotesk", "accent": "IBM Plex Mono"},
    "neubrutalism": {"heading": "Lexend Mega", "body": "Public Sans", "accent": "Space Mono"},
    "glassmorphism": {"heading": "Outfit", "body": "Inter", "accent": "Outfit"},
    "flat": {"heading": "Poppins", "body": "Open Sans", "accent": "Poppins"},
    "material": {"heading": "Roboto", "body": "Roboto", "accent": "Roboto Mono"},
}

LAYOUT_BLOCKS: dict[str, list[str]] = {
    "landing": ["hero", "trust_bar", "features", "showcase", "pricing", "testimonials", "faq", "cta", "footer"],
    "shop": ["header", "catalog", "filters", "product_card", "cart", "checkout", "footer"],
    "dashboard": ["sidebar", "topbar", "stats_cards", "chart", "table", "footer"],
    "portfolio": ["hero", "works_grid", "about", "services", "contact", "footer"],
    "blog": ["header", "featured_post", "post_grid", "newsletter", "footer"],
}


def _require_non_empty(value: Any, field_name: str, exc: type[Exception]) -> str:
    """Validate that value is a non-empty string.

    Args:
        value: Candidate value.
        field_name: Field name for error messages.
        exc: Exception class to raise.

    Returns:
        Stripped string.
    """
    if not isinstance(value, str) or not value.strip():
        raise exc("field " + field_name + " must be a non-empty string")
    return value.strip()


def _seed_index(seed_text: str, modulus: int) -> int:
    """Derive a deterministic index from text.

    Args:
        seed_text: Source string.
        modulus: Upper bound (exclusive).

    Returns:
        Index in range [0, modulus).
    """
    digest = hashlib.sha256(seed_text.encode("utf-8")).hexdigest()
    return int(digest, 16) % modulus


class Halib:
    """Designer agent: concepts, palettes, typography, layouts, audits."""

    def __init__(self, lang: str = "ru") -> None:
        """Initialize Halib agent.

        Args:
            lang: Default response language (ru or en).
        """
        self.name: str = "halib"
        self.lang: str = lang if lang in ("ru", "en") else "ru"
        self.history: list[dict[str, Any]] = []
        logger.debug("Halib agent initialized")

    def concept(self, project: str, style: str = "minimal", mood: str = "trustworthy") -> dict[str, Any]:
        """Build a design concept for a project.

        Args:
            project: Project or brand name/description.
            style: One of STYLES.
            mood: One of MOODS.

        Returns:
            Dict with concept fields: title, style, mood, principles, sections.
        """
        title = _require_non_empty(project, "project", ConceptError)
        style_norm = style.strip().lower() if isinstance(style, str) else ""
        mood_norm = mood.strip().lower() if isinstance(mood, str) else ""
        if style_norm not in STYLES:
            raise ConceptError("style must be one of: " + ", ".join(STYLES))
        if mood_norm not in MOODS:
            raise ConceptError("mood must be one of: " + ", ".join(MOODS))
        principles = [
            "Контраст и иерархия: один главный акцент на экран",
            "Воздух: отступы минимум 24px между смысловыми блоками",
            "Один стиль скруглений и теней на весь проект (" + style_norm + ")",
            "Настроение '" + mood_norm + "' держим цветом и фото, а не декором",
        ]
        sections = list(LAYOUT_BLOCKS["landing"])
        result: dict[str, Any] = {
            "project": title,
            "style": style_norm,
            "mood": mood_norm,
            "tagline": title + " — чистый " + style_norm + "-дизайн в настроении " + mood_norm,
            "principles": principles,
            "sections": sections,
        }
        self.history.append({"type": "concept", "project": title})
        logger.info("Concept built project=%s style=%s", title, style_norm)
        return result

    def palette(self, brand: str, mood: str = "trustworthy", count: int = 5) -> dict[str, Any]:
        """Generate a color palette for a brand.

        Args:
            brand: Brand or project name.
            mood: One of MOODS.
            count: Number of colors (3-5).

        Returns:
            Dict with brand, mood and list of HEX colors with roles.
        """
        name = _require_non_empty(brand, "brand", PaletteError)
        mood_norm = mood.strip().lower() if isinstance(mood, str) else ""
        if mood_norm not in MOODS:
            raise PaletteError("mood must be one of: " + ", ".join(MOODS))
        if not isinstance(count, int) or count not in (3, 4, 5):
            raise PaletteError("count must be 3, 4 or 5")
        base = BASE_PALETTES[mood_norm]
        shift = _seed_index(name.lower(), len(base))
        rotated = [base[(shift + i) % len(base)] for i in range(len(base))]
        colors = rotated[:count]
        roles = ["background", "surface", "primary", "ink", "deep"][:count]
        items = [{"role": role, "hex": hex_code} for role, hex_code in zip(roles, colors)]
        logger.info("Palette built brand=%s mood=%s", name, mood_norm)
        return {"brand": name, "mood": mood_norm, "colors": items}

    def typography(self, project: str, style: str = "minimal") -> dict[str, Any]:
        """Pick a font pairing for a project.

        Args:
            project: Project name.
            style: One of STYLES.

        Returns:
            Dict with heading/body/accent fonts and scale.
        """
        title = _require_non_empty(project, "project", TypographyError)
        style_norm = style.strip().lower() if isinstance(style, str) else ""
        if style_norm not in STYLES:
            raise TypographyError("style must be one of: " + ", ".join(STYLES))
        pairing = FONT_PAIRINGS[style_norm]
        logger.info("Typography picked project=%s style=%s", title, style_norm)
        return {
            "project": title,
            "style": style_norm,
            "heading": pairing["heading"],
            "body": pairing["body"],
            "accent": pairing["accent"],
            "scale": {"h1": 48, "h2": 36, "h3": 24, "body": 16, "caption": 13},
            "rule": "Максимум 2 семейства на проект, акцентный — только для цифр и цитат",
        }

    def layout(self, page: str = "landing", sections: list[str] | None = None) -> dict[str, Any]:
        """Build a page layout structure.

        Args:
            page: One of LAYOUT_BLOCKS keys.
            sections: Optional custom section list (overrides preset).

        Returns:
            Dict with page name and ordered block list.
        """
        if not isinstance(page, str) or not page.strip():
            raise LayoutError("page must be a non-empty string")
        page_norm = page.strip().lower()
        if sections is not None:
            if not isinstance(sections, list) or len(sections) == 0:
                raise LayoutError("sections must be a non-empty list")
            cleaned: list[str] = []
            for item in sections:
                if not isinstance(item, str) or not item.strip():
                    raise LayoutError("sections must contain non-empty strings")
                cleaned.append(item.strip())
            logger.info("Custom layout built page=%s blocks=%d", page_norm, len(cleaned))
            return {"page": page_norm, "blocks": cleaned}
        if page_norm not in LAYOUT_BLOCKS:
            raise LayoutError("page must be one of: " + ", ".join(LAYOUT_BLOCKS.keys()))
        blocks = list(LAYOUT_BLOCKS[page_norm])
        logger.info("Layout built page=%s blocks=%d", page_norm, len(blocks))
        return {"page": page_norm, "blocks": blocks}

    def logo_brief(self, business: str, character: str = "строгий", symbol: str = "знак") -> str:
        """Write a short logo brief in Russian.

        Args:
            business: Business or brand name.
            character: Logo character (e.g. строгий, игривый, премиальный).
            symbol: Preferred mark type (знак, монограмма, вордмарк).

        Returns:
            Human-readable logo brief.
        """
        name = _require_non_empty(business, "business", ConceptError)
        char = character.strip() if isinstance(character, str) and character.strip() else "строгий"
        mark = symbol.strip() if isinstance(symbol, str) and symbol.strip() else "знак"
        lines: list[str] = [
            "Халиб — лого-бриф: " + name,
            "Характер: " + char,
            "Тип знака: " + mark,
            "Конструкция: сетка 8px, охранное поле = высота строчной, мин. размер 24px",
            "Цвет: 1 основная версия + монохром (ч/б), без градиентов в базе",
            "Запрещено: тени, обводки, стоковые иконки, больше 2 цветов в знаке",
            "Сдача: SVG + PNG 1024px, версии horizontal / stacked / icon",
        ]
        self.history.append({"type": "logo_brief", "project": name})
        return "\n".join(lines)

    def style_guide(self, brand: str, style: str = "minimal", mood: str = "trustworthy") -> str:
        """Build a compact brand style guide in Russian.

        Args:
            brand: Brand name.
            style: One of STYLES.
            mood: One of MOODS.

        Returns:
            Human-readable style guide text.
        """
        name = _require_non_empty(brand, "brand", ConceptError)
        pal = self.palette(name, mood)
        typo = self.typography(name, style)
        colors_text = ", ".join(c["hex"] + " (" + c["role"] + ")" for c in pal["colors"])
        lines: list[str] = [
            "Халиб — стайлгайд: " + name,
            "Стиль: " + style.strip().lower() + " / настроение: " + mood.strip().lower(),
            "Палитра: " + colors_text,
            "Шрифты: заголовки " + typo["heading"] + ", текст " + typo["body"] + ", акцент " + typo["accent"],
            "Сетка: 12 колонок, gutter 24px, max-width 1200px",
            "Кнопки: radius 12px, primary — залитая, secondary — контур 1.5px",
            "Фото: живые, без стоковой постановочности, один пресет цветокора",
            "Следующий шаг: собери 1 экран (hero + CTA) строго по гайду и покажи мне на аудит",
        ]
        self.history.append({"type": "style_guide", "project": name})
        return "\n".join(lines)

    def audit_design(self, description: str) -> str:
        """Give an honest design audit with a score.

        Args:
            description: Free-text description of the design/screen.

        Returns:
            Russian audit text with score 1-10, issues and next step.
        """
        text = _require_non_empty(description, "description", AuditError)
        lowered = text.lower()
        score = 7
        issues: list[str] = []
        if any(w in lowered for w in ("градиент", "тень", "бегущ", "анимац", "блестит", "неон")):
            issues.append("визуальный шум: убери лишние эффекты, оставь один акцент")
            score -= 2
        if any(w in lowered for w in ("много текста", "мелкий", "не чита", "каша")):
            issues.append("иерархия: сократи текст в 2 раза, увеличь заголовок и отступы")
            score -= 2
        if any(w in lowered for w in ("кнопк", "cta", "купить", "записаться")) and "кнопк" not in lowered:
            issues.append("CTA слабый: одна primary-кнопка выше сгиба")
        if "кнопк" not in lowered and "cta" not in lowered:
            issues.append("нет явного CTA — добавь одну primary-кнопку выше сгиба")
            score -= 1
        if len(text) < 30:
            issues.append("мало контекста: пришли скрин или опиши экран подробнее")
            score -= 1
        score = max(1, min(10, score))
        verdict = "сильно" if score >= 8 else ("средне — чинится за 1 итерацию" if score >= 5 else "слабо — нужен редизайн hero")
        lines: list[str] = [
            "Халиб — аудит дизайна: " + str(score) + "/10 (" + verdict + ")",
            "Что вижу: " + text[:220],
        ]
        if issues:
            lines.append("Проблемы:")
            for issue in issues:
                lines.append("- " + issue)
        else:
            lines.append("Критичных проблем не вижу — докрути мелочи.")
        lines.append("Следующий шаг: поправь top-1 проблему и вернись на повторный аудит.")
        self.history.append({"type": "audit", "score": score})
        logger.info("Design audit scored %d", score)
        return "\n".join(lines)

    def get_history(self) -> list[dict[str, Any]]:
        """Return operation history.

        Returns:
            List of past operation metadata dicts.
        """
        return list(self.history)


engine = Halib()
