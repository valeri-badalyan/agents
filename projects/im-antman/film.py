"""Сборка фильма «I'm Antman! (Я Энтмен!)»: озвучка, музыка, анимация → MP4.

Запуск:  python film.py [ru|en|all] [--out DIR]
"""

import argparse
import logging
import math
import os
import subprocess
import textwrap
from dataclasses import dataclass, field
from typing import Any

import numpy as np
from PIL import Image, ImageDraw

import draw as D
import sound
import tts
from script import CREDITS, SCENES, TITLE_EN, TITLE_RU

log = logging.getLogger("film")
FPS = 24
SR = tts.SR
PRE, GAP, POST = 0.5, 0.35, 0.5
FADE = 0.35


@dataclass
class Line:
    """One timed line inside a scene."""

    spk: str
    text: str
    opts: dict[str, Any]
    audio: np.ndarray
    start: float = 0.0
    dur: float = 0.0


@dataclass
class Scene:
    """Timed scene."""

    kind: str
    music: str
    lines: list[Line] = field(default_factory=list)
    start: float = 0.0
    dur: float = 0.0


def build_timeline(lang: str) -> list[Scene]:
    """Synthesize voices and lay out scene timings."""
    scenes: list[Scene] = []
    t = 0.0
    for sd in SCENES:
        sc = Scene(sd["kind"], sd["music"], start=t)
        lt = PRE
        for spk, ru, en, opts in sd["lines"]:
            text = ru if lang == "ru" else en
            audio = tts.synth(text, lang, spk)
            ln = Line(spk, text, opts, audio, start=lt, dur=len(audio) / SR)
            sc.lines.append(ln)
            lt += ln.dur + GAP + float(opts.get("hold", 0))
            log.info("[%s] %s: %.1fs", lang, spk, ln.dur)
        sc.dur = sd.get("duration", lt + POST)
        scenes.append(sc)
        t += sc.dur
    return scenes


def build_audio(scenes: list[Scene], total: float) -> np.ndarray:
    """Mix voices, sfx and ducked music."""
    n = int(total * SR) + SR
    voice = np.zeros(n, np.float32)
    fx = np.zeros(n, np.float32)
    music = np.zeros(n, np.float32)

    def put(buf: np.ndarray, clip: np.ndarray, at: float) -> None:
        i = int(at * SR)
        j = min(n, i + len(clip))
        if j > i:
            buf[i:j] += clip[: j - i]

    for sc in scenes:
        loop = sound.music(sc.music)
        seg = np.resize(loop, int(sc.dur * SR))
        ramp = min(len(seg) // 2, int(0.3 * SR))
        seg[:ramp] *= np.linspace(0, 1, ramp)
        seg[-ramp:] *= np.linspace(1, 0, ramp)
        put(music, seg, sc.start)
        for ln in sc.lines:
            at = sc.start + ln.start
            put(voice, ln.audio, at)
            if "sfx" in ln.opts:
                put(fx, sound.sfx(ln.opts["sfx"]), at)
            if "sfx_end" in ln.opts:
                put(fx, sound.sfx(ln.opts["sfx_end"]), at + ln.dur + 0.05)
    # duck music under voice
    env = np.abs(voice)
    k = int(0.25 * SR)
    env = np.convolve(env, np.ones(k) / k, mode="same")
    duck = 1.0 - 0.65 * np.clip(env * 8, 0, 1)
    mix = voice * 1.0 + fx * 0.55 + music * 0.22 * duck
    peak = float(np.max(np.abs(mix))) or 1.0
    return (mix / max(1.0, peak / 0.95)).astype(np.float32)


# ---------------- per-frame context ----------------

@dataclass
class Ctx:
    """What is happening at a given frame of a scene."""

    t: float
    dur: float
    lang: str
    li: int
    lt: float
    ld: float
    spk: str | None

    def talk(self, spk: str) -> float:
        """Mouth openness for speaker."""
        if self.spk == spk and self.lt < self.ld:
            return abs(math.sin(self.lt * 17)) * (0.6 + 0.4 * abs(math.sin(self.lt * 5.3)))
        return 0.0

    def k(self, line: int, a: float = 0.0, b: float | None = None) -> float:
        """Progress 0..1 inside line `line` between fractions a..b of its time (seconds if b given as negative)."""
        if self.li < line:
            return 0.0
        if self.li > line:
            return 1.0
        end = self.ld if b is None else b
        if end <= a:
            return 1.0
        return max(0.0, min(1.0, (self.lt - a) / (end - a)))


def ease(x: float) -> float:
    """Smoothstep."""
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def lerp(a: float, b: float, k: float) -> float:
    """Linear interpolation."""
    return a + (b - a) * k


def walk(t: float) -> tuple[float, float]:
    """Leg/arm swing for walking."""
    s = math.sin(t * 9) * 25
    return (10 + s, 10 - s)


def render_scene(img: Image.Image, sc: Scene, c: Ctx) -> None:
    """Draw scene animation for one frame."""
    d = ImageDraw.Draw(img)
    ov_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ov = ImageDraw.Draw(ov_img)
    use_ov = False
    kind = sc.kind
    t = c.t

    if kind == "title":
        for i in range(80):
            x = (i * 137) % D.W
            y = (i * 89) % 420
            b = int(150 + 100 * math.sin(t * 3 + i))
            d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(b, b, b))
        z = ease(t / 1.5)
        D.hero(d, 640, 690, 0.4 + 0.9 * z, mouth=0, arms=(150, 150))
        D.text_center(d, 640, 130, TITLE_EN, int(40 + 50 * z), D.GOLD, 6, (150, 20, 20))
        D.text_center(d, 640, 230, f"({TITLE_RU})", int(20 + 30 * z), (255, 255, 255), 4, (150, 20, 20))
        D.text_center(d, 640, 300, "Комедия · 12+" if c.lang == "ru" else "Comedy · 12+", 30, (255, 200, 200), 3)
        D.plus_sparkles(d, 640, 500, (t % 2.0) / 2.0, n=20, spread=200)

    elif kind == "city":
        trip_k = c.k(1, 0.0, 0.9)
        if c.li < 1:
            x = lerp(-80, 560, ease(t / max(1.0, sc.lines[0].dur + PRE)))
            D.hero(d, x, 640, 1.0, suit=False, arms=walk(t))
            d.rectangle([x + 20, 520, x + 90, 535], fill=(200, 150, 80), outline=D.BLACK, width=2)
        else:
            jump = math.sin(min(1.0, trip_k) * math.pi) * 80
            sq = 1.0 if trip_k < 1 else lerp(0.55, 1.0, ease(c.k(1, 0.9, 1.6)))
            D.hero(d, 600, 640 - jump, 1.0, mouth=c.talk("A"), suit=False, arms=(160, 160), squash=sq)
            bx, by = 690 + trip_k * 160, 520 - math.sin(trip_k * math.pi) * 260 + trip_k * 100
            d.rectangle([bx, by, bx + 70, by + 15], fill=(200, 150, 80), outline=D.BLACK, width=2)
            if trip_k >= 1:
                d.ellipse([bx - 10, by + 10, bx + 90, by + 40], fill=(240, 180, 60), outline=(200, 60, 30), width=5)
            D.starburst(d, 470, 470, 70, "БАМ!" if c.lang == "ru" else "BAM!", ease(c.k(1, 0.2, 0.5)) * (1 - c.k(1, 1.4, 2.2)))

    elif kind == "lab":
        D.person(d, 260, 620, "scientist", mouth=c.talk("S"),
                 arms=(10, 10) if c.li != 1 else (120 + 30 * math.sin(t * 8), 140 - 30 * math.sin(t * 8)))
        vat_box = [820, 360, 1100, 620]
        d.rectangle(vat_box, fill=(60, 90, 70), outline=(200, 220, 230), width=6)
        if c.li <= 0:
            hx = lerp(-80, 520, ease(c.k(0)))
            D.hero(d, hx, 620, 1.0, suit=False, arms=walk(t))
            d.rectangle([hx + 20, 500, hx + 90, 515], fill=(200, 150, 80), outline=D.BLACK, width=2)
        elif c.li in (1, 2):
            hx = 520 if c.li == 1 else lerp(520, 700, ease(c.k(2)))
            D.hero(d, hx, 620, 1.0, suit=False, mouth=c.talk("A"), arms=(10, 100) if c.li == 2 else (10, 10))
        else:
            k = c.k(3, 0.0, 0.8)
            hx = lerp(700, 960, k)
            hy = 620 - math.sin(k * math.pi) * 230 + (k ** 2) * 10
            if k >= 1:
                hy = 640 - 40 * ease(c.k(3, 1.2, 2.2))
            D.hero(d, hx, hy, 1.0, suit=False, arms=(170, 170), glow=1.0 if k >= 1 else 0, eyes_closed=k >= 1)
        # liquid front
        d.rectangle([826, 405, 1094, 614], fill=(70, 230, 110))
        d.line([(826, 405), (1094, 405)], fill=(160, 255, 180), width=6)
        d.text((960, 520), "☢", font=D.font(80), fill=(30, 120, 50), anchor="mm")
        if c.li == 3:
            sk = c.k(3, 0.7, 1.8)
            if 0 < sk < 1:
                for i in range(18):
                    a = math.pi * (0.1 + 0.8 * i / 17)
                    r = 40 + 180 * sk
                    px, py = 960 + math.cos(a) * r, 405 - math.sin(a) * r * 1.2 + sk * sk * 160
                    d.ellipse([px - 12, py - 12, px + 12, py + 12], fill=(90, 255, 120))
            D.starburst(d, 960, 230, 80, "БУЛЬК!" if c.lang == "ru" else "SPLASH!",
                        ease(c.k(3, 0.7, 1.0)) * (1 - ease(c.k(3, 1.8, 2.4))))

    elif kind == "kitchen":
        hx = 640
        arms = (10, 60)
        if c.li == 2:
            arms = (160 + 15 * math.sin(t * 10), 160 - 15 * math.sin(t * 10))
        hop = abs(math.sin(t * 6)) * 30 if c.li == 2 else 0
        D.hero(d, hx, 620 - hop, 1.0, suit=False, mouth=c.talk("A"), arms=arms)
        d.rectangle([720, 440, 860, 470], fill=(230, 190, 120), outline=D.BLACK, width=2)
        if c.li == 1:
            cut = c.k(1, 0.2, 0.4)
            heal = c.k(1, 1.2, 2.2)
            if cut > 0 and heal < 1:
                d.ellipse([706, 506, 720, 520], fill=(220, 0, 0))
            D.plus_sparkles(d, 715, 510, c.k(1, 1.0, 2.6), n=10, spread=40)
        if c.li >= 3:
            ph = ease(c.k(3, 0.0, 0.4))
            d.rounded_rectangle([900, 380 - 30 * ph, 1220, 560 - 30 * ph], radius=24, fill=(255, 255, 255), outline=D.BLACK, width=4)
            D.text_center(d, 1060, 420 - 30 * ph, "☎ МАМА" if c.lang == "ru" else "☎ MOM", 36, (200, 40, 120))
            D.text_center(d, 1060, 480 - 30 * ph, "♥ ♥ ♥", 36, (230, 40, 80))
            if c.talk("M") > 0.3:
                D.text_center(d, 1060, 530 - 30 * ph, "!!!", 30, (230, 40, 80))

    elif kind == "barber":
        snip = c.li == 1
        cyc = (t * 1.6) % 1.0
        hair = 1.0 + (2.4 * (1 - cyc) if snip else (2.4 if c.li >= 2 else 1.6))
        if c.li == 0:
            hair = 1.0 + 1.4 * ease(c.k(0))
        D.hero(d, 640, 640, 1.0, suit=False, hair=hair, mouth=c.talk("A"), arms=(15, 15))
        d.polygon([(590, 455), (690, 455), (740, 600), (540, 600)], fill=(120, 180, 230), outline=D.BLACK)
        shake = math.sin(t * 60) * 6 if c.li == 3 else 0
        bb = D.person(d, 880, 640, "barber", mouth=c.talk("P"), shake=shake,
                      arms=(10, 120 + 20 * math.sin(t * 14) if snip else 30))
        if snip:
            hx, hy = 760 + math.sin(t * 14) * 10, 400
            d.line([(hx, hy), (hx - 40, hy - 15 + 10 * math.sin(t * 20))], fill=(150, 150, 160), width=6)
            d.line([(hx, hy), (hx - 40, hy + 15 - 10 * math.sin(t * 20))], fill=(150, 150, 160), width=6)
            for i in range(6):
                fy = 420 + ((t * 200 + i * 40) % 200)
                d.line([(600 + i * 15, fy), (608 + i * 15, fy + 12)], fill=(110, 65, 30), width=4)
        if c.li == 3:
            D.text_center(d, 880 + shake, 360, "⚡", 50, (255, 200, 0))
        _ = bb

    elif kind == "food":
        plates = 1 + int(min(1.0, t / max(1.0, sc.dur - 1)) * 9)
        for i in range(plates):
            px = 380 + (i % 3) * 30
            py = 470 - (i // 1) * 14
            d.ellipse([px - 60, py - 8, px + 60, py + 8], fill=(255, 255, 255), outline=(120, 120, 120), width=2)
        D.hero(d, 640, 640, 1.0, suit=False, mouth=c.talk("A") or abs(math.sin(t * 9)) * 0.6,
               arms=(10, 130 + 20 * math.sin(t * 9)))
        d.ellipse([735, 455 + 8 * math.sin(t * 9), 765, 485 + 8 * math.sin(t * 9)], fill=(140, 80, 40))
        for i in range(2):
            gx = 860 + i * 70
            d.rectangle([gx, 420, gx + 45, 480], fill=(255, 220, 200), outline=D.BLACK, width=2)
        D.text_center(d, 640, 120, f"× {plates * 3}", 60, (200, 40, 40), 4, (255, 255, 255))

    elif kind in ("park", "fight", "climax"):
        # villain position
        if kind == "park":
            bx = lerp(1400, 960, ease(c.k(0, 0.0, 2.5)))
        else:
            bx = 960
        hx = 330
        # hero
        if kind == "park":
            if c.li >= 2:
                land = ease(c.k(2, 0.0, 0.5))
                hy = lerp(-50, 620, land)
                D.hero(d, hx, hy, 1.0, mouth=c.talk("A"), arms=(150, 30) if c.li == 2 else (40, 40),
                       squash=1.0 if land < 1 else lerp(0.8, 1.0, ease(c.k(2, 0.5, 0.8))))
                if 0.5 < c.lt < 1.3 and c.li == 2:
                    for i in range(8):
                        a = math.pi * i / 7
                        r = 60 + (c.lt - 0.5) * 140
                        d.ellipse([hx + math.cos(a) * r - 14, 620 - math.sin(a) * r * 0.3 - 14,
                                   hx + math.cos(a) * r + 14, 620 - math.sin(a) * r * 0.3 + 14], fill=(200, 180, 140))
        elif kind == "fight":
            sq, glow = 1.0, 0.0
            if c.li == 1:
                glow = c.k(1, max(0.0, c.ld - 0.8), c.ld + 0.4)
            if c.li >= 3 or (c.li == 2 and c.lt > c.ld):
                sq = 0.22
                if c.li == 3 and c.lt > c.ld:
                    p = ease(c.k(3, c.ld, c.ld + 0.5))
                    sq = lerp(0.22, 1.0, p) + math.sin(p * math.pi * 3) * 0.12 * (1 - p)
            shake = math.sin(t * 40) * 5 if c.li == 1 and c.lt < c.ld * 0.5 else 0
            D.hero(d, hx + shake, 620, 1.0, mouth=c.talk("A"), squash=sq, glow=glow,
                   arms=(40, 40) if c.li != 1 else (120, 20))
            if c.li == 1:
                D.plus_sparkles(d, hx, 470, c.k(1, c.ld * 0.5, c.ld + 0.8), n=16, spread=80)
        else:  # climax
            hx = lerp(330, 650, ease(c.k(0)))
            if c.li < 2:
                D.hero(d, hx, 620, 1.0, mouth=c.talk("A"), arms=walk(t) if c.li == 0 else (60, 160))
            else:
                D.hero(d, 520, 620, 1.0, arms=(10, 170))
        # villain
        if kind != "climax" or c.li < 2 or c.k(2, 0.0, 1.5) < 1:
            aim = 1.0 if (kind == "fight" and c.li == 0) or (kind == "park" and c.li == 1) or (kind == "climax" and c.li == 1) else 0.0
            sweat = kind == "climax" and c.li >= 1
            bxx = bx + (math.sin(t * 30) * 4 if sweat else 0)
            if kind == "climax" and c.li == 2:
                bxx = bx + 40
            D.baron(d, bxx, 620, 1.0, talk=abs(math.sin(t * 8)) if c.talk("B") else 0, aim=aim)
            if sweat:
                for i in range(3):
                    sy = 400 + ((t * 120 + i * 30) % 60)
                    d.ellipse([bxx + 30 + i * 12, sy, bxx + 40 + i * 12, sy + 16], fill=(120, 200, 255))
        # spray clouds
        if (kind == "park" and c.li == 1) or (kind == "fight" and c.li in (0, 1)):
            use_ov = True
            if kind == "park":
                cloud_x = lerp(820, 600, c.k(1))
                D.cloud(ov, cloud_x, 460, min(1.0, c.lt / 1.0), 0.9, seed=4)
            else:
                cloud_x = lerp(830, hx, ease(c.k(0, 0.0, c.ld if c.li == 0 else 0.1)))
                fade = 1.0 - (c.k(1, c.ld * 0.5, c.ld) if c.li == 1 else 0.0)
                D.cloud(ov, cloud_x, 470, min(1.0, 0.3 + c.lt), 1.1, seed=7, alpha=int(190 * fade))
        if kind == "climax" and c.li == 1:
            for i in range(3):
                pk = ((c.lt * 1.4) + i * 0.33) % 1.0
                d.ellipse([850 - pk * 60 - 8, 495 - 8, 850 - pk * 60 + 8, 495 + 8], fill=(200, 230, 200))
        # slipper
        if kind == "fight" and c.li >= 2:
            fall = ease(c.k(2, c.ld * 0.4, c.ld)) if c.li == 2 else 1.0
            lift = ease(c.k(3, c.ld, c.ld + 0.4)) if c.li == 3 else 0.0
            sy = lerp(-100, 625, fall) - lift * 800
            D.slipper(d, hx + 20, sy, 1.0)
            if c.li == 2 and c.lt > c.ld:
                D.starburst(d, 560, 330, 80, "ШЛЁП!" if c.lang == "ru" else "SPLAT!", ease(c.k(2, c.ld, c.ld + 0.3)))
            if c.li == 3 and c.lt > c.ld + 0.2:
                D.starburst(d, 330, 250, 70, "БОЙН-Н!" if c.lang == "ru" else "BOING!", 1.0)
        # police
        if kind == "climax" and c.li == 2:
            ck = ease(c.k(2, 0.0, 1.5))
            cx = lerp(-400, 820, ck)
            d.rounded_rectangle([cx - 190, 500, cx + 190, 610], radius=20, fill=(255, 255, 255), outline=D.BLACK, width=4)
            d.rounded_rectangle([cx - 110, 440, cx + 110, 510], radius=16, fill=(170, 210, 240), outline=D.BLACK, width=4)
            d.rectangle([cx - 190, 545, cx + 190, 565], fill=(30, 80, 200))
            D.text_center(d, cx, 525, "ПОЛИЦИЯ" if c.lang == "ru" else "POLICE", 26, (30, 80, 200))
            for wx in (-120, 120):
                d.ellipse([cx + wx - 35, 580, cx + wx + 35, 650], fill=D.BLACK)
            blink = int(t * 6) % 2
            d.rectangle([cx - 30, 420, cx, 440], fill=(255, 30, 30) if blink else (120, 0, 0))
            d.rectangle([cx, 420, cx + 30, 440], fill=(40, 40, 255) if not blink else (0, 0, 120))
            if ck >= 1:
                use_ov = True
                col = (255, 0, 0, 40) if blink else (0, 0, 255, 40)
                ov.rectangle([0, 0, D.W, D.H], fill=col)
                D.text_center(d, 640, 140, "ГОРОД СПАСЁН!" if c.lang == "ru" else "CITY SAVED!", 64, D.GOLD, 5, (150, 20, 20))

    elif kind == "ending":
        hop = abs(math.sin(t * 5)) * 25 if c.li == 1 and c.lt > c.ld * 0.5 else 0
        D.hero(d, 520, 640 - hop, 1.1, suit=False, hair=3.2 + 0.2 * math.sin(t * 2), mouth=c.talk("A"),
               arms=(10, 10) if c.li < 1 else (165, 30))
        if c.li == 1 and c.lt > c.ld * 0.6:
            D.plus_sparkles(d, 520, 380, ((c.lt - c.ld * 0.6) % 1.5) / 1.5, n=20, spread=160)
            D.text_center(d, 640, 110, TITLE_RU if c.lang == "ru" else TITLE_EN, 80, D.GOLD, 6, (150, 20, 20))

    elif kind == "credits":
        rows = CREDITS[c.lang]
        off = D.H + 40 - t / sc.dur * (D.H + 60 + len(rows) * 60)
        for i, row in enumerate(rows):
            y = off + i * 60
            if -40 < y < D.H + 40:
                D.text_center(d, 640, y, row, 56 if i == 0 else 34, D.GOLD if i == 0 else (240, 240, 240), 3)
        D.hero(d, 1120, 700, 0.6, arms=(20 + 20 * math.sin(t * 4), 150 + 20 * math.sin(t * 6)))

    if use_ov:
        img.alpha_composite(ov_img)


SUB_COLORS = {"A": (255, 220, 70), "B": (215, 170, 255), "N": (255, 255, 255),
              "S": (170, 230, 255), "M": (255, 170, 200), "P": (180, 255, 190)}


def subtitle(img: Image.Image, text: str, spk: str, lang: str) -> None:
    """Draw subtitle box at the bottom."""
    lines = textwrap.wrap(text, 52)
    if not lines:
        return
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    h = 44 * len(lines) + 20
    d.rounded_rectangle([90, D.H - h - 18, D.W - 90, D.H - 14], radius=14, fill=(0, 0, 0, 165))
    img.alpha_composite(ov)
    d = ImageDraw.Draw(img)
    for i, s in enumerate(lines):
        d.text((640, D.H - h - 18 + 32 + i * 44), s, font=D.font(32), fill=SUB_COLORS.get(spk, (255, 255, 255)),
               anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
    _ = lang


def frame_at(scenes: list[Scene], gt: float, lang: str) -> Image.Image:
    """Render the frame for global time gt."""
    sc = scenes[-1]
    for s in scenes:
        if s.start <= gt < s.start + s.dur:
            sc = s
            break
    t = gt - sc.start
    li, lt, ld, spk = -1, t, 0.0, None
    for i, ln in enumerate(sc.lines):
        if t >= ln.start:
            li, lt, ld, spk = i, t - ln.start, ln.dur, ln.spk
    c = Ctx(t, sc.dur, lang, li, lt, ld, spk)
    img = D.background(sc.kind, lang).copy()
    render_scene(img, sc, c)
    if li >= 0 and lt < ld + 0.25:
        subtitle(img, sc.lines[li].text, sc.lines[li].spk, lang)
    fade = min(1.0, t / FADE, (sc.dur - t) / FADE)
    if fade < 1.0:
        img = Image.blend(Image.new("RGBA", img.size, (0, 0, 0, 255)), img, max(0.0, fade))
    return img.convert("RGB")


def make(lang: str, out_dir: str) -> str:
    """Build one language version, return mp4 path."""
    os.makedirs(out_dir, exist_ok=True)
    scenes = build_timeline(lang)
    total = sum(s.dur for s in scenes)
    log.info("[%s] total %.1fs", lang, total)
    audio = build_audio(scenes, total)
    wav = os.path.join(out_dir, f"audio_{lang}.f32")
    audio[: int(total * SR)].tofile(wav)
    name = "I_m_Antman_RU.mp4" if lang == "ru" else "I_m_Antman_EN.mp4"
    out = os.path.join(out_dir, name)
    title = "Я Энтмен!" if lang == "ru" else "I'm Antman!"
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{D.W}x{D.H}", "-r", str(FPS),
           "-i", "-", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", wav,
           "-c:v", "libx264", "-preset", "medium", "-crf", "26", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart",
           "-metadata", f"title={title}", "-metadata", f"language={'rus' if lang == 'ru' else 'eng'}", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None
    nframes = int(total * FPS)
    for f in range(nframes):
        proc.stdin.write(frame_at(scenes, f / FPS, lang).tobytes())
        if f % (FPS * 20) == 0:
            log.info("[%s] frame %d/%d", lang, f, nframes)
    proc.stdin.close()
    proc.wait()
    os.remove(wav)
    return out


def main() -> None:
    """CLI entry."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    ap = argparse.ArgumentParser()
    ap.add_argument("lang", nargs="?", default="all", choices=["ru", "en", "all"])
    ap.add_argument("--out", default="out")
    ap.add_argument("--still", type=float, default=None, help="save a single frame at time T (debug)")
    a = ap.parse_args()
    langs = ["ru", "en"] if a.lang == "all" else [a.lang]
    for lang in langs:
        if a.still is not None:
            sc = build_timeline(lang)
            frame_at(sc, a.still, lang).save(os.path.join(a.out, f"still_{lang}_{a.still}.png"))
            continue
        log.info("done: %s", make(lang, a.out))


if __name__ == "__main__":
    main()
