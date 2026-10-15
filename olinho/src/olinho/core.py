"""Core logic for Olinho — turns ideas into browser-ready web projects."""

from __future__ import annotations

import logging
import re
import webbrowser
import zipfile
from pathlib import Path

from olinho.config import settings
from olinho.exceptions import BuildError, IdeaError, PreviewError

logger = logging.getLogger(__name__)

PROJECT_TYPES: dict[str, dict[str, object]] = {
    "landing": {
        "keywords": ["лендинг", "landing", "сайт", "посадочная", "визитка", "landing page"],
        "title": "Лендинг",
        "sections": ["hero", "features", "gallery", "cta", "contacts"],
    },
    "game": {
        "keywords": ["игра", "game", "кликер", "аркада", "roguelike", "dungeon", "стратегия"],
        "title": "Игра",
        "sections": ["canvas", "hud", "controls", "gameover"],
    },
    "app": {
        "keywords": ["приложение", "app", "сервис", "калькулятор", "трекер", "todo", "дашборд"],
        "title": "Веб-приложение",
        "sections": ["header", "main", "controls", "output"],
    },
    "portfolio": {
        "keywords": ["портфолио", "portfolio", "работы", "дизайнер", "фотограф"],
        "title": "Портфолио",
        "sections": ["hero", "works", "about", "contacts"],
    },
    "shop": {
        "keywords": ["магазин", "shop", "store", "товары", "каталог", "e-commerce"],
        "title": "Магазин",
        "sections": ["hero", "catalog", "cart", "checkout"],
    },
    "blog": {
        "keywords": ["блог", "blog", "статьи", "новости", "дневник"],
        "title": "Блог",
        "sections": ["hero", "posts", "subscribe", "contacts"],
    },
}

DEPLOY_HINTS: list[str] = [
    "Локально: просто открой index.html в Google Chrome",
    "GitHub Pages: залей папку в репозиторий → Settings → Pages → Deploy from branch",
    "Netlify: перетащи папку на app.netlify.com/drop — получишь ссылку за 10 секунд",
    "Vercel: npx vercel --prod в папке проекта",
]


def _validate_text(value: str, field_name: str) -> str:
    """Validate non-empty user input."""
    if not isinstance(value, str) or not value.strip():
        raise IdeaError(f"{field_name} must be a non-empty string")
    return value.strip()


def slugify(text: str) -> str:
    """Convert idea text to filesystem-safe slug.

    Args:
        text: Idea or project name.

    Returns:
        Lowercase latin slug.
    """
    value = text.strip().lower()
    value = re.sub(r"[^a-z0-9а-яё\s-]", "", value)
    value = re.sub(r"[\s_]+", "-", value)
    translit = {
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e",
        "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
        "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
        "ф": "f", "х": "h", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sch",
        "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
    }
    out = "".join(translit.get(ch, ch) for ch in value)
    out = re.sub(r"-+", "-", out).strip("-")
    return out[:50] or "olinho-project"


def find_repo_root(start: Path | None = None) -> Path:
    """Find agents repo root (contains session_loader.py or valeri/)."""
    current = (start or Path.cwd()).resolve()
    while current != current.parent:
        if (current / "session_loader.py").exists() or (
            (current / "valeri").exists() and (current / "jouli").exists()
        ):
            return current
        current = current.parent
    return Path.cwd()


class Olinho:
    """Idea-to-browser agent: classifies ideas, scaffolds sites, previews."""

    def __init__(self, projects_dir: Path | str | None = None) -> None:
        """Initialize Olinho agent.

        Args:
            projects_dir: Where to create projects. Defaults to settings/repo projects/.
        """
        if projects_dir is None:
            root = find_repo_root(Path(__file__).resolve())
            candidate = root / settings.default_projects_dir
            self.projects_dir = candidate if candidate.parent.exists() else Path.cwd() / "projects"
        else:
            self.projects_dir = Path(projects_dir)
        self.name: str = "olinho"
        logger.debug("Olinho initialized projects_dir=%s", self.projects_dir)

    def classify(self, idea: str) -> dict[str, object]:
        """Detect project type from idea text.

        Args:
            idea: Free-form idea description.

        Returns:
            Dict with type, title, sections, confidence.

        Raises:
            IdeaError: If idea is empty.
        """
        text = _validate_text(idea, "idea")
        low = text.lower()
        for ptype, meta in PROJECT_TYPES.items():
            keywords = meta["keywords"]
            assert isinstance(keywords, list)
            if any(k in low for k in keywords):
                logger.info("Classified idea as %s", ptype)
                return {
                    "idea": text,
                    "type": ptype,
                    "title": meta["title"],
                    "sections": list(meta["sections"]),  # type: ignore[arg-type]
                    "confidence": "high",
                }
        logger.info("Classified idea as landing (fallback)")
        return {
            "idea": text,
            "type": settings.default_type,
            "title": PROJECT_TYPES[settings.default_type]["title"],
            "sections": list(PROJECT_TYPES[settings.default_type]["sections"]),  # type: ignore[arg-type]
            "confidence": "low",
        }

    def _render_index(self, title: str, idea: str, ptype: str, sections: list[str]) -> str:
        """Render index.html template."""
        section_html = "\n".join(
            f'    <section class="card"><h2>{s.capitalize()}</h2>'
            f"<p>Блок «{s}» для идеи: {idea}</p></section>"
            for s in sections
        )
        game_script = ""
        if ptype == "game":
            game_script = (
                "<script>\n"
                "let score=0;const b=document.getElementById('play');\n"
                "b&&b.addEventListener('click',()=>{score++;document.getElementById('score').textContent=score;});\n"
                "</script>"
            )
        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title} — Олиньо!!</title>
<link rel="stylesheet" href="styles.css" />
</head>
<body>
<header class="hero">
<h1>{title}</h1>
<p>{idea}</p>
<button id="play">Жми!! Счёт: <span id="score">0</span></button>
<a class="btn" href="#main">Смотреть вниз</a>
</header>
<main id="main">
{section_html}
</main>
<footer>Собрано Олиньо!! — открой в Google Chrome. Идея: {idea}</footer>
<script src="app.js"></script>
{game_script}
</body>
</html>
"""

    def _render_css(self) -> str:
        """Render base stylesheet."""
        return """:root{--bg:#0f1226;--card:#1d2247;--acc:#ffb300;--txt:#fff}
*{box-sizing:border-box}body{margin:0;font-family:system-ui,Arial;background:var(--bg);color:var(--txt)}
.hero{padding:64px 24px;text-align:center;background:linear-gradient(135deg,#2b2f77,#6a1b9a)}
.hero h1{font-size:48px;margin:0 0 12px}.hero p{opacity:.9;max-width:640px;margin:0 auto 20px}
.btn,#play{background:var(--acc);border:0;padding:12px 22px;border-radius:999px;font-weight:700;cursor:pointer;color:#111;text-decoration:none}
main{display:grid;gap:16px;padding:24px;max-width:960px;margin:0 auto}
.card{background:var(--card);padding:20px;border-radius:16px}
footer{text-align:center;opacity:.6;padding:24px}
@media(max-width:600px){.hero h1{font-size:32px}}
"""

    def _render_js(self, ptype: str) -> str:
        """Render base script."""
        return (
            f"console.log('Олиньо!! тип проекта: {ptype}');\n"
            "document.getElementById('play')?.addEventListener('click',()=>console.log('click'));\n"
        )

    def build(self, idea: str, name: str | None = None) -> dict[str, object]:
        """Scaffold a browser-ready project from an idea.

        Args:
            idea: Idea description.
            name: Optional project folder name.

        Returns:
            Dict with path, files, type, preview_url.

        Raises:
            BuildError: If scaffolding fails.
        """
        try:
            text = _validate_text(idea, "idea")
            detected = self.classify(text)
            ptype = str(detected["type"])
            sections = list(detected["sections"])  # type: ignore[arg-type]
            slug = slugify(name) if name and name.strip() else slugify(text)
            target = self.projects_dir / slug
            target.mkdir(parents=True, exist_ok=True)
            title = f"{detected['title']}: {text[:60]}"
            files = {
                "index.html": self._render_index(str(title), text, ptype, sections),
                "styles.css": self._render_css(),
                "app.js": self._render_js(ptype),
                "README.md": f"# {title}\n\nИдея: {text}\n\nТип: {ptype}\n\nОткрыть: `index.html` в Google Chrome.\n",
            }
            for fname, content in files.items():
                (target / fname).write_text(content, encoding="utf-8")
            preview_url = (target / "index.html").resolve().as_uri()
            logger.info("Built project %s type=%s", target, ptype)
            return {
                "idea": text,
                "type": ptype,
                "title": title,
                "path": str(target.resolve()),
                "files": sorted(files.keys()),
                "preview_url": preview_url,
                "deploy_hints": list(DEPLOY_HINTS),
            }
        except (IdeaError, OSError, ValueError) as exc:
            raise BuildError(f"Build failed: {exc}") from exc

    def preview(self, path: str, browser: str | None = None) -> dict[str, str]:
        """Open built project in browser.

        Args:
            path: Project dir or index.html path.
            browser: chrome / default / edge / firefox.

        Returns:
            Dict with url and browser used.

        Raises:
            PreviewError: If path invalid.
        """
        try:
            p = Path(path)
            if p.is_dir():
                p = p / "index.html"
            if not p.exists():
                raise PreviewError(f"Path not found: {path}")
            url = p.resolve().as_uri()
            choice = (browser or settings.default_browser).lower()
            try:
                if choice == "chrome":
                    try:
                        webbrowser.get("chrome").open(url)
                    except webbrowser.Error:
                        webbrowser.open(url)
                elif choice == "edge":
                    try:
                        webbrowser.get("windows-default").open(url)
                    except webbrowser.Error:
                        webbrowser.open(url)
                else:
                    webbrowser.open(url)
            except Exception as exc:
                raise PreviewError(f"Cannot open browser: {exc}") from exc
            logger.info("Preview opened %s", url)
            return {"url": url, "browser": choice}
        except PreviewError:
            raise
        except Exception as exc:
            raise PreviewError(str(exc)) from exc

    def pack(self, path: str) -> dict[str, str]:
        """Zip project for hosting upload.

        Args:
            path: Project directory.

        Returns:
            Dict with zip path.
        """
        p = Path(path)
        if not p.is_dir():
            raise BuildError(f"Not a directory: {path}")
        zip_path = p.with_suffix(".zip")
        try:
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for f in p.rglob("*"):
                    if f.is_file():
                        zf.write(f, f.relative_to(p.parent))
            logger.info("Packed %s", zip_path)
            return {"zip": str(zip_path.resolve()), "project": str(p.resolve())}
        except OSError as exc:
            raise BuildError(f"Pack failed: {exc}") from exc

    def ship(self, idea: str, name: str | None = None, open_browser: bool = False) -> dict[str, object]:
        """Full pipeline: classify → build → (optional) preview → pack hints.

        Args:
            idea: Idea description.
            name: Optional project name.
            open_browser: Whether to open in browser immediately.

        Returns:
            Build dict extended with zip info.
        """
        built = self.build(idea, name)
        assert isinstance(built, dict)
        path = str(built["path"])
        if open_browser:
            try:
                prev = self.preview(path)
                built["opened"] = prev
            except PreviewError as exc:
                built["opened"] = {"error": str(exc)}
        try:
            # keep a copy dir for safety, then zip
            packed = self.pack(path)
            built["zip"] = packed["zip"]
        except BuildError as exc:
            built["zip_error"] = str(exc)
        return built


engine = Olinho()
