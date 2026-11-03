"""Сценический движок полнометражной версии.

Сценарий — текст. Строки:
  @ <фон> <музыка> | <состав> | <флаги>       — новая сцена
  @ card | Заголовок RU | Title EN             — титр главы
  <КТО> | реплика RU | реплика EN | действия   — реплика
  ~ <сек> | | | действия                         — сцена без слов
Состав: «A=300 casual, B=1000». Флаги: night, crowd.
Действия (через пробел): X>500 идти, X=500 встать, X^ прыжок, X^^ большой прыжок,
X:fall упасть сверху, X_ расплющиться, X~ отлипнуть, X! трястись, X* исцеление,
X:suit / X:casual, X:hair=3, X:up / X:point / X:wave / X:cross, X:hide / X:show,
fx=bam@X, cloud@X, slipper@X, dart@X, ants, police, shake, flash, boom@X,
hearts@X, sweat@X, zzz@X, notes@X, sfx=имя, sfx_end=имя, hold=1.5,
cap={RU|EN} — надпись сверху.
"""

import math
import random
import re
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any

from PIL import Image, ImageDraw

import cast as C
import draw as D

W, H = D.W, D.H
GROUND: dict[str, int] = {"city": 640, "street": 640, "lab": 620, "kitchen": 620, "barber": 640, "food": 640,
                          "park": 620, "ending": 640, "home": 640, "pizzeria": 630, "hospital": 630, "tv": 630,
                          "lair": 630, "rooftop": 620, "police": 630, "gym": 630, "park2": 620}
FX_WORDS: dict[str, tuple[str, str]] = {
    "bam": ("БАМ!", "BAM!"), "splat": ("ШЛЁП!", "SPLAT!"), "boing": ("БОЙН-Н!", "BOING!"), "wham": ("ХРЯСЬ!", "WHAM!"),
    "zap": ("ВЖУХ!", "ZAP!"), "oops": ("ОЙ!", "OOPS!"), "pow": ("БАХ!", "POW!"), "bulk": ("БУЛЬК!", "SPLASH!"),
    "crack": ("ХРУСЬ!", "CRACK!"), "wow": ("ВАУ!", "WOW!"), "pshh": ("ПШШ!", "PSSH!"), "bonk": ("БДЫЩ!", "BONK!"),
    "yay": ("УРА!", "HOORAY!"), "aaa": ("А-А-А!", "AAAH!"), "ding": ("ДЗЫНЬ!", "DING!"),
}
OUTDOOR = {"city", "street", "park", "park2", "rooftop", "home"}
PRE, GAP, POST = 0.5, 0.45, 0.6


@dataclass
class Line:
    """A dialogue line or a silent beat."""

    spk: str | None
    ru: str
    en: str
    acts: list[str]
    caps: list[tuple[str, str]]
    silent: float = 0.0
    audio: Any = None
    start: float = 0.0
    dur: float = 0.0

    def opt(self, key: str) -> str | None:
        """Value of key=value action."""
        for a in self.acts:
            if a.startswith(key + "="):
                return a.split("=", 1)[1]
        return None


@dataclass
class Scene:
    """Stage scene or chapter card."""

    bg: str
    music: str
    cast: dict[str, dict[str, Any]]
    flags: set[str]
    lines: list[Line] = field(default_factory=list)
    title: tuple[str, str] | None = None
    start: float = 0.0
    dur: float = 0.0
    index: int = 0


CAP_RE = re.compile(r"cap=\{([^|}]*)\|([^}]*)\}")


def parse(text: str) -> list[Scene]:
    """Parse screenplay text into scenes."""
    scenes: list[Scene] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("//"):
            continue
        if line.startswith("@"):
            parts = [p.strip() for p in line[1:].split("|")]
            head = parts[0].split()
            if head[0] in ("card", "title", "credits"):
                sc = Scene(head[0], head[1] if len(head) > 1 else "happy", {}, set())
                sc.title = (parts[1] if len(parts) > 1 else "", parts[2] if len(parts) > 2 else "")
            else:
                castd: dict[str, dict[str, Any]] = {}
                if len(parts) > 1 and parts[1]:
                    for item in parts[1].split(","):
                        bits = item.split()
                        code, x = bits[0].split("=")
                        castd[code] = {"x": float(x), "suit": "suit" in bits, "hair": 1.0}
                        for b in bits[1:]:
                            if b.startswith("hair="):
                                castd[code]["hair"] = float(b[5:])
                            if b == "hidden":
                                castd[code]["hidden"] = True
                flags = set(parts[2].split()) if len(parts) > 2 else set()
                sc = Scene(head[0], head[1] if len(head) > 1 else "happy", castd, flags)
            sc.index = len(scenes)
            scenes.append(sc)
            continue
        parts = [p.strip() for p in line.split("|")]
        while len(parts) < 4:
            parts.append("")
        spk, ru, en, acts = parts[0], parts[1], parts[2], parts[3]
        caps = CAP_RE.findall(acts)
        acts = CAP_RE.sub("", acts)
        if spk.startswith("~"):
            ln = Line(None, "", "", acts.split(), caps, silent=float(spk[1:].strip() or 3))
        else:
            ln = Line(spk, ru, en, acts.split(), caps)
        scenes[-1].lines.append(ln)
    return scenes


def layout(scenes: list[Scene], card_dur: float = 4.5) -> float:
    """Assign start/dur to scenes and lines (audio must be set). Returns total length."""
    t = 0.0
    for sc in scenes:
        sc.start = t
        if sc.bg in ("card", "title") and not sc.lines:
            sc.dur = card_dur if sc.bg == "card" else 7.0
        elif sc.bg == "credits":
            sc.dur = 40.0
        else:
            lt = PRE
            for ln in sc.lines:
                ln.start = lt
                ln.dur = ln.silent if ln.spk is None else len(ln.audio) / 44100
                lt += ln.dur + GAP + float(ln.opt("hold") or 0)
            sc.dur = lt + POST
        t += sc.dur
    return t


# ---------------- per-frame state ----------------

@dataclass
class Actor:
    """Animated state of one cast member."""

    x: float
    y: float = 0.0
    squash: float = 1.0
    suit: bool = False
    hair: float = 1.0
    visible: bool = True
    arms: tuple[float, float] | None = None
    shake: float = 0.0
    glow: float = 0.0
    flat: bool = False


ARM_POSES = {"up": (160, 160), "point": (15, 95), "wave": (15, 150), "cross": (60, 60), "down": (5, 5)}


def _k(t: float, a: float, d: float) -> float:
    if d <= 0:
        return 1.0 if t >= a else 0.0
    return max(0.0, min(1.0, (t - a) / d))


def actors_at(sc: Scene, t: float, ground: int) -> tuple[dict[str, Actor], list[tuple[str, Line, float]]]:
    """Replay actions up to time t. Returns actors and active effects (name, line, local time)."""
    acts: dict[str, Actor] = {}
    for code, c in sc.cast.items():
        acts[code] = Actor(c["x"], suit=c["suit"], hair=c["hair"], visible=not c.get("hidden"))
    effects: list[tuple[str, Line, float]] = []
    for ln in sc.lines:
        if t < ln.start:
            break
        lt = t - ln.start
        cur = lt < ln.dur + GAP
        for a in ln.acts:
            m = re.fullmatch(r"([A-Z]\d?)([>=])(-?\d+)", a)
            if m and m.group(1) in acts:
                ac = acts[m.group(1)]
                x1 = float(m.group(3))
                if m.group(2) == "=":
                    ac.x = x1
                else:
                    dur = max(0.4, min(abs(x1 - ac.x) / 260, max(0.6, ln.dur)))
                    k = _k(lt, 0, dur)
                    walking = 0 < k < 1
                    ac.x = ac.x + (x1 - ac.x) * k
                    if walking and ac.arms is None:
                        s = math.sin(t * 9) * 25
                        ac.arms = (10 + s, 10 - s)
                        ac.y -= abs(math.sin(t * 9)) * 6
                continue
            m = re.fullmatch(r"([A-Z]\d?)(\^\^|\^|_|~|!|\*)", a)
            if m and m.group(1) in acts:
                ac = acts[m.group(1)]
                op = m.group(2)
                if op == "^" and lt < 0.6:
                    ac.y -= math.sin(math.pi * lt / 0.6) * 70
                elif op == "^^" and lt < 1.0:
                    ac.y -= math.sin(math.pi * lt / 1.0) * 260
                elif op == "_":
                    ac.flat = True
                    ac.squash = 1 - 0.78 * _k(lt, 0, 0.15)
                elif op == "~":
                    p = _k(lt, 0, 0.6)
                    base = 0.22 if ac.flat else 0.55
                    if p < 1:
                        ac.squash = base + (1 - base) * p + math.sin(p * math.pi * 3) * 0.12 * (1 - p)
                    else:
                        ac.squash = 1.0
                    if p >= 1:
                        ac.flat = False
                elif op == "!" and cur:
                    ac.shake = math.sin(t * 45) * 6
                elif op == "*":
                    k = _k(lt, max(0.0, ln.dur - 0.6), 1.6)
                    if 0 < k < 1:
                        ac.glow = math.sin(k * math.pi)
                        effects.append(("heal@" + m.group(1), ln, k))
                continue
            m = re.fullmatch(r"([A-Z]\d?):(\w+)(?:=([\d.]+))?", a)
            if m and m.group(1) in acts:
                ac = acts[m.group(1)]
                cmd = m.group(2)
                if cmd == "suit":
                    ac.suit = True
                elif cmd == "casual":
                    ac.suit = False
                elif cmd == "hair":
                    ac.hair = float(m.group(3) or 1)
                elif cmd == "hide":
                    ac.visible = False
                elif cmd == "show":
                    ac.visible = True
                elif cmd == "fall":
                    ac.visible = True
                    p = _k(lt, 0, 0.55)
                    ac.y -= (1 - p) ** 2 * 750
                    if p >= 1 and lt < 0.95:
                        ac.squash = 0.7 + 0.3 * _k(lt, 0.55, 0.4)
                elif cmd in ARM_POSES and cur:
                    ac.arms = ARM_POSES[cmd]
                continue
            if cur or a.startswith(("police",)):
                effects.append((a, ln, lt))
    # flatten persists
    for ac in acts.values():
        if ac.flat and ac.squash > 0.5:
            ac.squash = 0.22
    for ac in acts.values():
        ac.y += ground
    return acts, effects


def mouth(lt: float) -> float:
    """Talking mouth value."""
    return abs(math.sin(lt * 17)) * (0.6 + 0.4 * abs(math.sin(lt * 5.3)))


# ---------------- backgrounds ----------------

def _grad(d: ImageDraw.ImageDraw, top, bot, y0: int, y1: int) -> None:
    for y in range(y0, y1):
        k = (y - y0) / max(1, y1 - y0)
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * k) for i in range(3)))


@lru_cache(maxsize=64)
def background(kind: str, lang: str, night: bool = False) -> Image.Image:
    """Background image for any scene kind."""
    if kind in ("city", "lab", "kitchen", "barber", "food", "park", "ending"):
        img = D.background(kind, lang).copy()
    else:
        img = Image.new("RGBA", (W, H))
        d = ImageDraw.Draw(img)
        rnd = random.Random(kind)
        if kind == "street":
            img = D.background("city", lang).copy()
            d = ImageDraw.Draw(img)
            _grad(d, (120, 190, 250), (200, 230, 255), 0, 140)
            d.rectangle([180, 380, 420, 470], fill=(250, 240, 220), outline=D.BLACK, width=4)
            D.text_center(d, 300, 425, "АПТЕКА" if lang == "ru" else "PHARMACY", 30, (40, 150, 60))
        elif kind == "home":
            _grad(d, (190, 170, 230), (160, 140, 210), 0, 590)
            d.rectangle([0, 590, W, H], fill=(140, 100, 70))
            d.rounded_rectangle([760, 400, 1220, 600], radius=30, fill=(80, 120, 200), outline=D.BLACK, width=4)
            d.rounded_rectangle([760, 330, 1220, 440], radius=30, fill=(70, 105, 180), outline=D.BLACK, width=4)
            d.rectangle([150, 110, 450, 300], fill=(30, 30, 40), outline=(90, 90, 90), width=10)
            d.rectangle([170, 130, 430, 280], fill=(60, 110, 160))
            d.rectangle([560, 120, 680, 260], fill=(150, 210, 255), outline=(255, 255, 255), width=8)
        elif kind == "pizzeria":
            _grad(d, (255, 200, 120), (240, 170, 90), 0, 600)
            d.rectangle([0, 600, W, H], fill=(120, 60, 40))
            for x in range(0, W, 80):
                for y in range(600, H, 40):
                    if (x // 80 + y // 40) % 2:
                        d.rectangle([x, y, x + 80, y + 40], fill=(240, 240, 240))
            d.rounded_rectangle([340, 40, 940, 130], radius=20, fill=(200, 30, 40), outline=D.BLACK, width=4)
            D.text_center(d, 640, 85, "ПИЦЦА «МУРАШ»" if lang == "ru" else "MURASH PIZZA", 48, (255, 240, 200), 3)
            d.rectangle([60, 430, 560, 600], fill=(170, 100, 60), outline=D.BLACK, width=4)
            d.ellipse([1000, 300, 1200, 500], fill=(80, 60, 50), outline=D.BLACK, width=6)
            d.ellipse([1040, 340, 1160, 460], fill=(255, 120, 40))
            for i in range(4):
                d.rectangle([90 + i * 110, 390, 170 + i * 110, 430], fill=(220, 170, 90), outline=D.BLACK, width=2)
        elif kind == "hospital":
            _grad(d, (220, 245, 245), (200, 230, 235), 0, 600)
            d.rectangle([0, 600, W, H], fill=(180, 200, 210))
            d.rectangle([900, 420, 1220, 520], fill=(255, 255, 255), outline=(120, 120, 140), width=4)
            d.rectangle([900, 400, 960, 440], fill=(200, 220, 255))
            for lx in (910, 1210):
                d.rectangle([lx, 520, lx + 10, 600], fill=(120, 120, 140))
            d.rectangle([100, 80, 300, 320], fill=(255, 255, 255), outline=(150, 150, 150), width=4)
            d.rectangle([185, 120, 215, 280], fill=(230, 40, 40))
            d.rectangle([120, 185, 280, 215], fill=(230, 40, 40))
            for i in range(5):
                d.line([(500, 150 + i * 40), (760, 150 + i * 40)], fill=(160, 160, 160), width=3)
            D.text_center(d, 630, 110, "РЕНТГЕН" if lang == "ru" else "X-RAY", 28, (60, 60, 80))
        elif kind == "tv":
            _grad(d, (40, 20, 70), (90, 30, 110), 0, 600)
            d.rectangle([0, 600, W, H], fill=(50, 40, 70))
            for i in range(8):
                x = 80 + i * 160
                d.polygon([(x, 0), (x + 40, 0), (x + 120, 600), (x - 80, 600)], fill=(110, 60, 150))
            d.rounded_rectangle([380, 60, 900, 160], radius=16, fill=(250, 210, 60), outline=D.BLACK, width=4)
            D.text_center(d, 640, 110, "ШОУ «ГЕРОИ»" if lang == "ru" else "HERO SHOW", 48, (150, 20, 80))
            d.rounded_rectangle([520, 470, 760, 600], radius=12, fill=(240, 240, 255), outline=D.BLACK, width=4)
        elif kind == "lair":
            _grad(d, (40, 40, 50), (70, 60, 70), 0, 600)
            d.rectangle([0, 600, W, H], fill=(50, 50, 55))
            for x in range(0, W, 160):
                d.rectangle([x + 20, 0, x + 50, 600], fill=(60, 60, 70))
            for i in range(3):
                cx = 300 + i * 340
                d.rounded_rectangle([cx - 70, 300, cx + 70, 600], radius=20, fill=(90, 110, 90), outline=D.BLACK, width=4)
                d.ellipse([cx - 40, 340, cx + 40, 420], fill=(160, 40, 200))
            d.polygon([(500, 20), (780, 20), (740, 120), (540, 120)], fill=(30, 30, 30), outline=(200, 30, 30))
            D.text_center(d, 640, 70, "ЛИГА ВРЕДИТЕЛЕЙ" if lang == "ru" else "LEAGUE OF PESTS", 30, (220, 40, 40))
        elif kind == "rooftop":
            _grad(d, (255, 150, 90), (255, 210, 140), 0, 560)
            x = -20
            while x < W:
                w = rnd.randint(90, 160)
                h = rnd.randint(120, 320)
                d.rectangle([x, 560 - h, x + w, 560], fill=(120, 90, 110))
                x += w + 10
            d.rectangle([0, 560, W, H], fill=(110, 110, 120))
            d.rectangle([980, 440, 1100, 560], fill=(150, 150, 160), outline=D.BLACK, width=3)
            d.line([(1040, 440), (1040, 360)], fill=D.BLACK, width=4)
            d.rectangle([1040, 360, 1100, 395], fill=(200, 30, 40))
        elif kind == "police":
            _grad(d, (200, 215, 240), (180, 195, 225), 0, 600)
            d.rectangle([0, 600, W, H], fill=(100, 110, 130))
            d.rectangle([80, 430, 600, 600], fill=(120, 90, 60), outline=D.BLACK, width=4)
            d.rectangle([800, 80, 1180, 360], fill=(255, 255, 255), outline=D.BLACK, width=4)
            for i in range(3):
                d.rectangle([830 + i * 120, 110, 920 + i * 120, 230], fill=(230, 230, 230), outline=D.BLACK)
                d.ellipse([855 + i * 120, 125, 895 + i * 120, 165], fill=(120, 120, 120))
            D.text_center(d, 990, 300, "РАЗЫСКИВАЮТСЯ" if lang == "ru" else "WANTED", 36, (200, 30, 30))
            D.text_center(d, 340, 80, "ПОЛИЦИЯ" if lang == "ru" else "POLICE", 50, (30, 60, 160), 3, (255, 255, 255))
        elif kind == "gym":
            _grad(d, (230, 230, 200), (210, 210, 180), 0, 600)
            d.rectangle([0, 600, W, H], fill=(190, 140, 90))
            for y in (630, 680):
                d.line([(0, y), (W, y)], fill=(170, 120, 70), width=3)
            d.rectangle([900, 470, 1200, 490], fill=(80, 80, 80))
            for wx in (900, 1180):
                d.ellipse([wx - 30, 420, wx + 30, 540], fill=(40, 40, 40))
            d.rectangle([100, 120, 400, 300], fill=(200, 40, 40), outline=D.BLACK, width=4)
            D.text_center(d, 250, 210, "НЕ СДАВАЙСЯ!" if lang == "ru" else "NEVER QUIT!", 30, (255, 255, 255))
        elif kind == "park2":
            img = D.background("park", lang).copy()
            d = ImageDraw.Draw(img)
            d.rectangle([430, 590, 850, 680], fill=(100, 180, 80))
            d.rectangle([600, 200, 640, 540], fill=(120, 80, 40))
            d.ellipse([480, 80, 760, 300], fill=(60, 150, 60))
        else:
            _grad(d, (10, 10, 40), (60, 20, 70), 0, H)
    if night:
        dark = Image.new("RGBA", img.size, (10, 10, 50, 140))
        img = img.copy()
        img.alpha_composite(dark)
        d = ImageDraw.Draw(img)
        rnd = random.Random(7)
        if kind not in OUTDOOR:
            return img
        for _ in range(40):
            x, y = rnd.randint(0, W), rnd.randint(0, 250)
            d.ellipse([x - 1, y - 1, x + 2, y + 2], fill=(255, 255, 220))
        d.ellipse([1050, 50, 1130, 130], fill=(250, 250, 210))
    return img


# ---------------- drawing ----------------

def draw_actor(d: ImageDraw.ImageDraw, code: str, ac: Actor, mth: float, talking: bool, t: float) -> None:
    """Draw one actor."""
    arms = ac.arms
    if arms is None:
        arms = (10 + 12 * math.sin(t * 4), 10 + 25 * abs(math.sin(t * 3))) if talking else (10, 10)
    x = ac.x + ac.shake
    if code == "A":
        D.hero(d, x, ac.y, 1.0, mouth=mth, arms=arms, squash=ac.squash, suit=ac.suit, hair=ac.hair, glow=ac.glow)
    elif code == "B":
        D.baron(d, x, ac.y, 1.0, talk=abs(math.sin(t * 8)) if talking else 0,
                aim=1.0 if ac.arms in (ARM_POSES["point"], ARM_POSES["up"]) else 0.0)
    elif code == "G":
        C.ant(d, x, ac.y, 1.0, mouth=mth, wave=1.0 if talking or ac.arms else 0.0, squash=ac.squash)
    elif code in C.STYLES:
        C.figure(d, x, ac.y, code, 1.0, mouth=mth, arms=arms, squash=ac.squash)


def _anchor(acts: dict[str, Actor], target: str) -> tuple[float, float]:
    ac = acts.get(target)
    if ac is None:
        return (640.0, 400.0)
    return (ac.x, ac.y - 190 * ac.squash)


def draw_effects(img: Image.Image, d: ImageDraw.ImageDraw, ov: ImageDraw.ImageDraw, acts: dict[str, Actor],
                 effects: list[tuple[str, Line, float]], t: float, lang: str, speaker: str | None) -> tuple[bool, float]:
    """Draw transient effects. Returns (overlay used, camera shake)."""
    used, shake = False, 0.0
    li = 0 if lang == "ru" else 1
    for name, ln, lt in effects:
        tgt = name.split("@")[1] if "@" in name else None
        base = name.split("@")[0]
        ax, ay = _anchor(acts, tgt) if tgt else (640.0, 360.0)
        if base == "heal":
            D.plus_sparkles(d, ax, ay + 60, lt, n=16, spread=80)
        elif base.startswith("fx="):
            word = FX_WORDS.get(base[3:], (base[3:].upper(), base[3:].upper()))[li]
            k = min(1.0, lt / 0.2) * (1 - _k(lt, 1.2, 0.4))
            if k > 0:
                D.starburst(d, ax + 120, ay - 90, 70, word, k)
        elif base == "cloud":
            used = True
            fade = 1 - _k(lt, max(0.5, ln.dur - 0.4), 0.6)
            D.cloud(ov, ax, ay + 40, min(1.0, 0.3 + lt), 1.0, seed=int(ln.start * 10) % 50, alpha=int(180 * fade))
        elif base == "slipper":
            fall = _k(lt, max(0.0, ln.dur - 0.5), 0.5)
            if fall > 0:
                D.slipper(d, ax + 20, -100 + (ay + 190 + 100) * fall, 1.0)
        elif base == "dart":
            p = _k(lt, 0.0, 0.5)
            if p < 1:
                dx = 1300 - (1300 - ax) * p
                d.line([(dx, ay + 50), (dx + 40, ay + 50)], fill=(80, 80, 80), width=5)
                d.polygon([(dx - 12, ay + 50), (dx, ay + 44), (dx, ay + 56)], fill=(200, 30, 30))
            elif lt < ln.dur:
                d.line([(ax + 15, ay + 60), (ax + 45, ay + 60)], fill=(80, 80, 80), width=5)
                d.polygon([(ax + 45, ay + 52), (ax + 60, ay + 60), (ax + 45, ay + 68)], fill=(160, 40, 200))
        elif base == "ants":
            p = lt / max(1.0, ln.dur)
            for i in range(60):
                r = random.Random(i)
                x = -200 + (p * 1.6 + r.random() * 0.5) * W
                y = 600 + r.randint(0, 90)
                d.ellipse([x - 9, y - 6, x + 9, y + 6], fill=(120, 30, 20))
                d.ellipse([x + 7, y - 6, x + 17, y + 4], fill=(120, 30, 20))
                d.line([(x + 14, y - 5), (x + 20, y - 14 + 3 * math.sin(t * 20 + i))], fill=D.BLACK, width=2)
        elif base == "police":
            used = True
            blink = int(t * 6) % 2
            ov.rectangle([0, 0, W, H], fill=(255, 0, 0, 38) if blink else (0, 0, 255, 38))
        elif base == "shake":
            shake = math.sin(t * 50) * 10 * (1 - _k(lt, 0, max(0.6, ln.dur)))
        elif base == "flash":
            used = True
            a = int(255 * (1 - _k(lt, 0, 0.5)))
            if a > 0:
                ov.rectangle([0, 0, W, H], fill=(255, 255, 255, a))
        elif base == "boom":
            k = _k(lt, 0, 0.8)
            if k < 1:
                r = 40 + 240 * k
                d.ellipse([ax - r, ay - r + 80, ax + r, ay + r + 80], fill=(255, int(200 - 150 * k), 40))
                d.ellipse([ax - r * 0.6, ay - r * 0.6 + 80, ax + r * 0.6, ay + r * 0.6 + 80], fill=(255, 250, 180))
        elif base in ("hearts", "notes", "zzz", "sweat"):
            for i in range(4):
                ph = (lt * 0.7 + i * 0.25) % 1.0
                px = ax + 40 + math.sin(ph * 6 + i) * 25
                py = ay - 40 - ph * 120
                if base == "hearts":
                    D.text_center(d, px, py, "♥", int(30 + 10 * ph), (230, 40, 90))
                elif base == "notes":
                    D.text_center(d, px, py, "♪", int(34 + 6 * ph), (60, 40, 150))
                elif base == "zzz":
                    D.text_center(d, px, py, "z", int(24 + 20 * ph), (80, 80, 160))
                else:
                    d.ellipse([ax + 30 + i * 9, ay + 10 + ph * 50, ax + 38 + i * 9, ay + 24 + ph * 50], fill=(120, 200, 255))
    _ = (img, speaker)
    return used, shake


SUB_COLORS = {"A": (255, 220, 70), "B": (215, 170, 255), "N": (255, 255, 255), "S": (170, 230, 255),
              "M": (255, 170, 200), "P": (180, 255, 190), "L": (140, 240, 170), "G": (255, 160, 110),
              "T": (240, 200, 150), "K": (220, 150, 255), "C": (150, 190, 255), "O": (255, 190, 120),
              "D": (200, 255, 255), "H": (255, 140, 220)}
