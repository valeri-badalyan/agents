"""Персонажи полнометражной версии: общая фигура со стилями + муравей Гоша."""

import math
from typing import Any

from PIL import ImageDraw

import draw as D
from draw import BLACK, SKIN, Body

# kind -> style
STYLES: dict[str, dict[str, Any]] = {
    "S": {"torso": (245, 245, 245), "legs": (70, 70, 80), "hair": "wild", "hc": (205, 205, 210), "x": ["goggles"]},
    "P": {"torso": (240, 240, 240), "legs": (40, 40, 45), "hair": "short", "hc": (30, 30, 30), "x": ["stripes", "mustache"]},
    "M": {"dress": (235, 120, 160), "hair": "bun", "hc": (120, 90, 70), "x": ["apron"]},
    "L": {"torso": (60, 160, 110), "legs": (50, 70, 130), "hair": "long", "hc": (170, 60, 40), "x": ["notebook"]},
    "T": {"torso": (140, 90, 60), "legs": (200, 200, 240), "hair": "bald", "hc": (0, 0, 0), "x": ["slipper_hat", "glasses"], "w": 1.1},
    "K": {"dress": (120, 50, 150), "hair": "none", "hc": (0, 0, 0), "x": ["wings", "proboscis", "antennae", "bigeyes"], "w": 0.8,
          "skin": (200, 210, 160)},
    "C": {"torso": (40, 60, 120), "legs": (30, 40, 80), "hair": "short", "hc": (90, 70, 50), "x": ["cap", "mustache", "badge"], "w": 1.15},
    "O": {"torso": (240, 140, 40), "legs": (60, 60, 70), "hair": "bald", "hc": (60, 40, 30), "x": ["tie"], "w": 1.4,
          "skin": (240, 170, 140)},
    "D": {"torso": (250, 250, 250), "legs": (90, 130, 170), "hair": "short", "hc": (60, 60, 60), "x": ["stethoscope", "glasses"]},
    "H": {"torso": (150, 40, 120), "legs": (30, 30, 30), "hair": "slick", "hc": (240, 210, 80), "x": ["mic", "tie"]},
    "X1": {"torso": (80, 160, 200), "legs": (60, 60, 60), "hair": "short", "hc": (40, 30, 20), "x": []},
    "X2": {"dress": (250, 200, 60), "hair": "long", "hc": (40, 30, 20), "x": []},
    "X3": {"torso": (150, 200, 90), "legs": (90, 70, 50), "hair": "short", "hc": (200, 160, 60), "x": ["cap"]},
}


def _arm(d: ImageDraw.ImageDraw, b: Body, side: int, ang: float, color, hand, w: float) -> tuple[float, float]:
    sh = (side * 30 * w, 142)
    a = math.radians(ang)
    end = (side * (30 * w + math.sin(a) * 68), 142 - math.cos(a) * 68)
    d.line([b.p(*sh), b.p(*end)], fill=color, width=b.w(16))
    d.ellipse(b.circ(end[0], end[1], 10), fill=hand)
    return end


def figure(d: ImageDraw.ImageDraw, x: float, y: float, kind: str, s: float = 1.0, mouth: float = 0.0,
           arms: tuple[float, float] = (10, 10), squash: float = 1.0) -> Body:
    """Draw a styled supporting character."""
    st = STYLES[kind]
    b = Body(x, y, s, squash)
    w = st.get("w", 1.0)
    skin = st.get("skin", SKIN)
    ex = st["x"]
    hc = st["hc"]
    if "wings" in ex:
        for side in (-1, 1):
            d.ellipse(b.box(side * 20, 120, side * 95, 230), fill=(210, 235, 255), outline=(120, 150, 190), width=b.w(3))
    if st.get("hair") == "long":
        d.rectangle(b.box(-38, 130, 38, 205), fill=hc)
    top = st.get("torso") or st.get("dress")
    if "dress" in st:
        for side in (-1, 1):
            d.rectangle(b.box(side * 4, 0, side * 16, 50), fill=skin)
            d.rectangle(b.box(side * 2, 0, side * 20, 10), fill=BLACK)
        _arm(d, b, -1, arms[0], st["dress"], skin, w)
        _arm(d, b, 1, arms[1], st["dress"], skin, w)
        d.polygon([b.p(-55 * w, 40), b.p(55 * w, 40), b.p(30 * w, 152), b.p(-30 * w, 152)], fill=st["dress"], outline=BLACK)
        if "apron" in ex:
            d.polygon([b.p(-30, 45), b.p(30, 45), b.p(22, 125), b.p(-22, 125)], fill=(255, 255, 255))
    else:
        for side in (-1, 1):
            d.rectangle(b.box(side * 4 * w, 0, side * 21 * w, 72), fill=st["legs"])
            d.rectangle(b.box(side * 2 * w, 0, side * 24 * w, 12), fill=BLACK)
        _arm(d, b, -1, arms[0], top, skin, w)
        end = _arm(d, b, 1, arms[1], top, skin, w)
        d.rounded_rectangle(b.box(-34 * w, 58, 34 * w, 152), radius=b.w(14), fill=top, outline=(90, 90, 90), width=b.w(2))
        if "stripes" in ex:
            for i in range(5):
                c = (210, 40, 40) if i % 2 == 0 else (250, 250, 250)
                d.rectangle(b.box(-26, 62 + i * 15, 26, 77 + i * 15), fill=c)
        if "tie" in ex:
            d.polygon([b.p(0, 148), b.p(-8, 135), b.p(0, 85), b.p(8, 135)], fill=(200, 30, 40))
        if "badge" in ex:
            d.polygon([b.p(18, 135), b.p(24, 122), b.p(30, 135), b.p(24, 128)], fill=D.GOLD)
            d.ellipse(b.circ(24, 128, 7), fill=D.GOLD)
        if "stethoscope" in ex:
            d.line([b.p(-12, 150), b.p(-16, 110), b.p(0, 95), b.p(16, 110), b.p(12, 150)], fill=(60, 60, 60), width=b.w(4))
            d.ellipse(b.circ(0, 95, 7), fill=(160, 160, 170))
        if "notebook" in ex:
            d.rectangle(b.box(end[0] - 4, end[1] - 4, end[0] + 22, end[1] + 26), fill=(255, 255, 240), outline=BLACK)
        if "mic" in ex:
            d.line([b.p(*end), b.p(end[0] - 6, end[1] + 30)], fill=BLACK, width=b.w(6))
            d.ellipse(b.circ(end[0] - 6, end[1] + 34, 9), fill=(80, 80, 80))
    d.rectangle(b.box(-10, 148, 10, 162), fill=skin)
    hair = st.get("hair")
    if hair == "wild":
        for k in range(9):
            a = math.radians(150 - k * 15)
            d.line([b.p(0, 200), b.p(math.cos(a) * 52, 200 + math.sin(a) * 52)], fill=hc, width=b.w(10))
    if hair == "bun":
        d.ellipse(b.circ(0, 236, 18), fill=hc)
    d.ellipse(b.circ(0, 190, 35), fill=skin)
    if hair in ("short", "long", "bun"):
        d.chord(b.circ(0, 196, 37), 180, 360, fill=hc)
    elif hair == "slick":
        d.chord(b.circ(0, 194, 38), 170, 370, fill=hc)
    elif hair == "bald":
        for side in (-1, 1):
            d.ellipse(b.box(side * 28, 182, side * 40, 205), fill=hc)
    # face
    if "bigeyes" in ex:
        for side in (-1, 1):
            d.ellipse(b.circ(side * 14, 196, 12), fill=(250, 60, 60), outline=BLACK, width=b.w(2))
            d.ellipse(b.circ(side * 12, 199, 4), fill=(255, 255, 255))
    elif "goggles" in ex:
        for side in (-1, 1):
            d.ellipse(b.circ(side * 13, 194, 10), fill=(200, 230, 255), outline=BLACK, width=b.w(3))
            d.ellipse(b.circ(side * 13, 194, 3), fill=BLACK)
    else:
        for side in (-1, 1):
            d.ellipse(b.circ(side * 12, 194, 4), fill=BLACK)
        if "glasses" in ex:
            for side in (-1, 1):
                d.ellipse(b.circ(side * 13, 194, 11), outline=BLACK, width=b.w(3))
            d.line([b.p(-2, 196), b.p(2, 196)], fill=BLACK, width=b.w(3))
    if hair in ("long", "bun") or "dress" in st:
        for side in (-1, 1):
            d.line([b.p(side * 10, 202), b.p(side * 20, 206)], fill=BLACK, width=b.w(2))
    if "mustache" in ex:
        d.polygon([b.p(-20, 178), b.p(0, 184), b.p(20, 178), b.p(24, 168), b.p(0, 176), b.p(-24, 168)], fill=(40, 30, 25))
    if "proboscis" in ex:
        d.line([b.p(0, 182), b.p(-45, 165)], fill=(60, 30, 60), width=b.w(4))
    if "antennae" in ex:
        for side in (-1, 1):
            d.line([b.p(side * 10, 222), b.p(side * 30, 262)], fill=BLACK, width=b.w(3))
            d.ellipse(b.circ(side * 30, 262, 5), fill=(120, 50, 150))
    if "cap" in ex:
        d.chord(b.circ(0, 212, 36), 180, 360, fill=st["torso"] if kind == "C" else (220, 60, 60))
        d.rectangle(b.box(-40, 208, 40, 216), fill=BLACK)
        if kind == "C":
            d.ellipse(b.circ(0, 225, 7), fill=D.GOLD)
    if "slipper_hat" in ex:
        d.rounded_rectangle(b.box(-45, 222, 45, 240), radius=b.w(8), fill=(150, 90, 60), outline=BLACK)
        d.chord(b.box(-30, 225, 40, 262), 180, 360, fill=(240, 120, 170), outline=BLACK)
    mh = 3 + 12 * mouth
    d.ellipse(b.box(-8, 168 - mh / 2, 8, 168 + mh / 2), fill=(150, 30, 40))
    return b


def ant(d: ImageDraw.ImageDraw, x: float, y: float, s: float = 1.0, mouth: float = 0.0, wave: float = 0.0,
        squash: float = 1.0) -> Body:
    """Gosha, the talking ant (~110 px tall)."""
    b = Body(x, y, s, squash)
    c = (150, 45, 30)
    for side in (-1, 1):
        d.line([b.p(side * 6, 40), b.p(side * 14, 18), b.p(side * 10, 0)], fill=BLACK, width=b.w(5))
    d.ellipse(b.box(-22, 20, 22, 60), fill=c, outline=BLACK, width=b.w(2))
    d.ellipse(b.box(-13, 55, 13, 80), fill=c, outline=BLACK, width=b.w(2))
    for side in (-1, 1):
        a = math.radians(40 + (wave * 90 if side == 1 else 0) + math.sin(wave * 12) * 15 * wave)
        d.line([b.p(side * 10, 72), b.p(side * (10 + math.sin(a) * 28), 72 - math.cos(a) * 28)], fill=BLACK, width=b.w(5))
    d.rectangle(b.box(-12, 74, 12, 82), fill=(60, 180, 90))
    d.ellipse(b.circ(0, 98, 20), fill=c, outline=BLACK, width=b.w(2))
    for side in (-1, 1):
        d.line([b.p(side * 6, 115), b.p(side * 14, 132), b.p(side * 24, 136)], fill=BLACK, width=b.w(3))
        d.ellipse(b.circ(side * 24, 136, 4), fill=c)
        d.ellipse(b.circ(side * 8, 102, 7), fill=(255, 255, 255), outline=BLACK, width=b.w(1))
        d.ellipse(b.circ(side * 7, 101, 3), fill=BLACK)
    mh = 2 + 7 * mouth
    d.ellipse(b.box(-5, 88 - mh / 2, 5, 88 + mh / 2), fill=(60, 10, 10))
    return b
