"""Рисование персонажей, фонов и эффектов для «Я Энтмен!» (PIL)."""

import math
import random
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

SKIN = (245, 200, 160)
SUIT = (205, 35, 40)
BLACK = (25, 25, 30)
GOLD = (255, 205, 40)


@lru_cache(maxsize=64)
def font(size: int) -> ImageFont.FreeTypeFont:
    """Return cached bold font of given size."""
    return ImageFont.truetype(FONT_BOLD, size)


class Body:
    """Coordinate helper: (u, v) in body units, v grows upward from feet."""

    def __init__(self, x: float, y: float, s: float, squash: float = 1.0, flip: bool = False) -> None:
        self.x, self.y = x, y
        self.sx = s / math.sqrt(max(squash, 0.05))
        self.sy = s * squash
        self.s = s
        self.f = -1 if flip else 1

    def p(self, u: float, v: float) -> tuple[float, float]:
        """Body point to screen point."""
        return (self.x + u * self.sx * self.f, self.y - v * self.sy)

    def box(self, u0: float, v0: float, u1: float, v1: float) -> list[float]:
        """Body box to screen box."""
        a, b = self.p(u0, v0), self.p(u1, v1)
        return [min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])]

    def circ(self, u: float, v: float, r: float) -> list[float]:
        """Circle box."""
        return self.box(u - r, v - r, u + r, v + r)

    def w(self, width: float) -> int:
        """Scaled line width."""
        return max(1, int(width * self.s))


def _arm(d: ImageDraw.ImageDraw, b: Body, side: int, ang: float, color, hand, length: float = 70) -> tuple[float, float]:
    sh = (side * 30, 142)
    a = math.radians(ang)
    end = (side * (30 + math.sin(a) * length), 142 - math.cos(a) * length)
    d.line([b.p(*sh), b.p(*end)], fill=color, width=b.w(17))
    d.ellipse(b.circ(end[0], end[1], 10), fill=hand)
    return end


def hero(d: ImageDraw.ImageDraw, x: float, y: float, s: float = 1.0, mouth: float = 0.0,
         arms: tuple[float, float] = (10, 10), squash: float = 1.0, suit: bool = True,
         hair: float = 1.0, glow: float = 0.0, eyes_closed: bool = False) -> Body:
    """Draw Anton / Antman. Returns body helper (for props)."""
    b = Body(x, y, s, squash)
    if glow > 0:
        g = int(120 * glow)
        d.ellipse(b.box(-80, -10, 80, 260), outline=(80, 255, 120), width=b.w(4 + 6 * glow))
        _ = g
    legc = SUIT if suit else (45, 70, 130)
    torso = SUIT if suit else (60, 120, 210)
    hand = BLACK if suit else SKIN
    # big hair (behind head)
    if not suit and hair > 1.05:
        r = 36 + (hair - 1) * 38
        d.ellipse(b.box(-r, 190 - r * 0.9, r, 200 + r), fill=(110, 65, 30))
    # legs
    for side in (-1, 1):
        d.rectangle(b.box(side * 4, 0, side * 22, 72), fill=legc)
        d.rectangle(b.box(side * 2, 0, side * 25, 16), fill=BLACK if suit else (240, 240, 240))
    # arms behind torso
    _arm(d, b, -1, arms[0], torso, hand)
    _arm(d, b, 1, arms[1], torso, hand)
    d.rounded_rectangle(b.box(-34, 62, 34, 152), radius=b.w(14), fill=torso)
    if suit:
        d.rectangle(b.box(-34, 70, 34, 82), fill=BLACK)
        d.ellipse(b.circ(0, 120, 18), fill=GOLD, outline=BLACK, width=b.w(3))
        fa = font(max(8, int(22 * b.s)))
        cx, cy = b.p(0, 120)
        d.text((cx, cy), "A", font=fa, fill=BLACK, anchor="mm")
    # neck + head
    d.rectangle(b.box(-10, 148, 10, 162), fill=SKIN)
    d.ellipse(b.circ(0, 190, 36), fill=SKIN)
    if suit:
        hb = b.circ(0, 192, 39)
        d.chord(hb, 165, 375, fill=BLACK)
        for side in (-1, 1):
            d.line([b.p(side * 12, 224), b.p(side * 22, 250), b.p(side * 34, 266)], fill=BLACK, width=b.w(5))
            d.ellipse(b.circ(side * 34, 266, 7), fill=SUIT)
            d.ellipse(b.box(side * 4, 186, side * 27, 206), fill=(250, 250, 250), outline=(90, 90, 90), width=b.w(2))
    else:
        d.chord(b.circ(0, 194, 38), 180, 360, fill=(110, 65, 30))
        for side in (-1, 1):
            if eyes_closed:
                d.line([b.p(side * 17, 192), b.p(side * 7, 192)], fill=BLACK, width=b.w(3))
            else:
                d.ellipse(b.circ(side * 12, 192, 4.5), fill=BLACK)
    mh = 3 + 12 * mouth
    d.ellipse(b.box(-9, 174 - mh / 2, 9, 174 + mh / 2), fill=(150, 30, 40))
    return b


def baron(d: ImageDraw.ImageDraw, x: float, y: float, s: float = 1.0, talk: float = 0.0, aim: float = 0.0) -> Body:
    """Draw Baron Bugspray facing left (aim: arm raise 0..1)."""
    b = Body(x, y - talk * 6, s)
    # tank
    d.rounded_rectangle(b.box(30, 70, 64, 168), radius=b.w(10), fill=(70, 165, 75), outline=BLACK, width=b.w(3))
    cx, cy = b.p(47, 120)
    d.text((cx, cy), "☠", font=font(max(8, int(30 * b.s))), fill=BLACK, anchor="mm")
    for side in (-1, 1):
        d.rectangle(b.box(side * 6, 0, side * 18, 60), fill=BLACK)
    d.polygon([b.p(-48, 18), b.p(48, 18), b.p(32, 155), b.p(-32, 155)], fill=(115, 40, 145), outline=BLACK)
    for v in (60, 90, 120):
        d.ellipse(b.circ(-8, v, 4), fill=GOLD)
    # arm with nozzle (points left)
    hand = (-30 - 60, 125 + 30 * aim)
    d.line([b.p(-30, 140), b.p(*hand)], fill=(115, 40, 145), width=b.w(16))
    d.line([b.p(50, 100), b.p(20, 60), b.p(-40, 80), b.p(hand[0] + 5, hand[1] - 5)], fill=(60, 60, 60), width=b.w(5))
    d.rectangle(b.box(hand[0] - 26, hand[1] - 5, hand[0], hand[1] + 5), fill=(160, 160, 170))
    d.ellipse(b.circ(hand[0], hand[1], 10), fill=BLACK)
    # gas-mask head
    d.ellipse(b.circ(0, 185, 33), fill=(125, 135, 120), outline=BLACK, width=b.w(3))
    for side in (-1, 1):
        d.ellipse(b.circ(side * 13, 193, 10), fill=(40, 60, 70), outline=BLACK, width=b.w(2))
        d.ellipse(b.circ(side * 13 - 3, 197, 3), fill=(220, 240, 255))
    d.ellipse(b.circ(-4, 168, 14), fill=(80, 85, 80), outline=BLACK, width=b.w(2))
    for k in range(-2, 3):
        d.line([b.p(-4 + k * 5, 160), b.p(-4 + k * 5, 176)], fill=BLACK, width=b.w(2))
    # top hat
    d.rectangle(b.box(-40, 212, 40, 220), fill=BLACK)
    d.rectangle(b.box(-26, 218, 26, 270), fill=BLACK)
    d.rectangle(b.box(-26, 224, 26, 232), fill=(115, 40, 145))
    return b


def person(d: ImageDraw.ImageDraw, x: float, y: float, kind: str, s: float = 1.0, mouth: float = 0.0,
           arms: tuple[float, float] = (10, 10), shake: float = 0.0) -> Body:
    """Draw a supporting character: 'scientist' or 'barber'."""
    b = Body(x + shake, y, s)
    if kind == "scientist":
        coat, legs, hairc = (245, 245, 245), (70, 70, 80), (200, 200, 205)
    else:
        coat, legs, hairc = (240, 240, 240), (40, 40, 45), (30, 30, 30)
    for side in (-1, 1):
        d.rectangle(b.box(side * 4, 0, side * 20, 72), fill=legs)
    _arm(d, b, -1, arms[0], coat, SKIN)
    _arm(d, b, 1, arms[1], coat, SKIN)
    d.rounded_rectangle(b.box(-34, 50, 34, 152), radius=b.w(12), fill=coat, outline=(160, 160, 160), width=b.w(2))
    if kind == "barber":
        for i in range(5):
            c = (210, 40, 40) if i % 2 == 0 else (250, 250, 250)
            d.rectangle(b.box(-26, 60 + i * 15, 26, 75 + i * 15), fill=c)
    d.rectangle(b.box(-10, 148, 10, 162), fill=SKIN)
    if kind == "scientist":
        for k in range(9):
            a = math.radians(150 - k * 15)
            d.line([b.p(0, 200), b.p(math.cos(a) * 52, 200 + math.sin(a) * 52)], fill=hairc, width=b.w(10))
    d.ellipse(b.circ(0, 190, 35), fill=SKIN)
    if kind == "scientist":
        for side in (-1, 1):
            d.ellipse(b.circ(side * 13, 194, 10), fill=(200, 230, 255), outline=BLACK, width=b.w(3))
            d.ellipse(b.circ(side * 13, 194, 3), fill=BLACK)
    else:
        d.chord(b.circ(0, 196, 37), 180, 360, fill=hairc)
        for side in (-1, 1):
            d.ellipse(b.circ(side * 12, 194, 4), fill=BLACK)
        d.polygon([b.p(-20, 178), b.p(0, 184), b.p(20, 178), b.p(24, 168), b.p(0, 176), b.p(-24, 168)], fill=BLACK)
    mh = 3 + 12 * mouth
    d.ellipse(b.box(-8, 168 - mh / 2, 8, 168 + mh / 2), fill=(150, 30, 40))
    return b


# ---------------- effects ----------------

def plus_sparkles(d: ImageDraw.ImageDraw, x: float, y: float, t: float, n: int = 14, spread: float = 90) -> None:
    """Green healing '+' particles rising around (x, y); t in 0..1."""
    if t <= 0 or t >= 1:
        return
    for i in range(n):
        r = random.Random(i * 7 + 3)
        px = x + r.uniform(-spread, spread)
        py = y + r.uniform(-spread, spread * 0.6) - t * 120 * r.uniform(0.6, 1.2)
        sz = 6 + 8 * r.random() * (1 - t)
        c = (90, 255, 130)
        d.line([(px - sz, py), (px + sz, py)], fill=c, width=4)
        d.line([(px, py - sz), (px, py + sz)], fill=c, width=4)


def starburst(d: ImageDraw.ImageDraw, x: float, y: float, r: float, text: str, k: float = 1.0) -> None:
    """Comic 'BAM!' starburst."""
    if k <= 0:
        return
    r *= k
    pts = []
    for i in range(24):
        a = math.pi * 2 * i / 24
        rr = r if i % 2 == 0 else r * 0.62
        pts.append((x + math.cos(a) * rr * 1.3, y + math.sin(a) * rr))
    d.polygon(pts, fill=(255, 225, 40), outline=(210, 30, 30))
    d.text((x, y), text, font=font(max(10, int(r * 0.42))), fill=(210, 30, 30), anchor="mm",
           stroke_width=2, stroke_fill=(255, 255, 255))


def cloud(ov: ImageDraw.ImageDraw, x: float, y: float, t: float, size: float = 1.0, seed: int = 1, alpha: int = 170) -> None:
    """Puffy toxic cloud on an RGBA overlay; t 0..1 growth."""
    rnd = random.Random(seed)
    for _ in range(16):
        dx, dy = rnd.uniform(-1, 1), rnd.uniform(-0.6, 0.6)
        rr = rnd.uniform(30, 70) * size * min(1.0, t * 1.5)
        cx, cy = x + dx * 110 * size * t, y + dy * 80 * size * t
        g = rnd.randint(150, 200)
        ov.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(g - 30, g + 30, g - 50, alpha))


def slipper(d: ImageDraw.ImageDraw, x: float, y: float, s: float = 1.0) -> None:
    """Giant house slipper (seen from the side), bottom at y."""
    d.rounded_rectangle([x - 190 * s, y - 40 * s, x + 190 * s, y], radius=int(20 * s), fill=(150, 90, 60), outline=BLACK, width=4)
    d.chord([x - 120 * s, y - 120 * s, x + 200 * s, y + 20 * s], 180, 360, fill=(240, 120, 170), outline=BLACK, width=4)
    d.ellipse([x + 30 * s, y - 140 * s, x + 110 * s, y - 80 * s], fill=(255, 255, 255), outline=BLACK, width=3)


def text_center(d: ImageDraw.ImageDraw, x: float, y: float, txt: str, size: int, fill, stroke: int = 0, sfill=(0, 0, 0)) -> None:
    """Centered text."""
    d.text((x, y), txt, font=font(size), fill=fill, anchor="mm", stroke_width=stroke, stroke_fill=sfill)


# ---------------- backgrounds ----------------

def _vgrad(img: Image.Image, top, bottom, y0: int = 0, y1: int = H) -> None:
    d = ImageDraw.Draw(img)
    for y in range(y0, y1):
        k = (y - y0) / max(1, (y1 - y0))
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bottom[i] - top[i]) * k) for i in range(3)))


@lru_cache(maxsize=32)
def background(kind: str, lang: str) -> Image.Image:
    """Static background per scene kind (cached)."""
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    rnd = random.Random(kind)
    if kind in ("title", "credits"):
        _vgrad(img, (10, 10, 40), (60, 20, 70))
    elif kind == "city":
        _vgrad(img, (120, 190, 250), (200, 230, 255), 0, 560)
        x = -20
        while x < W:
            w = rnd.randint(110, 190)
            h = rnd.randint(200, 430)
            c = rnd.choice([(170, 120, 100), (120, 140, 170), (200, 180, 140), (150, 160, 150)])
            d.rectangle([x, 560 - h, x + w, 560], fill=c, outline=(70, 70, 80), width=3)
            for wy in range(560 - h + 20, 540, 45):
                for wx in range(x + 15, x + w - 25, 35):
                    d.rectangle([wx, wy, wx + 20, wy + 25], fill=(255, 240, 160) if rnd.random() < 0.3 else (90, 110, 140))
            x += w + rnd.randint(5, 25)
        d.rectangle([0, 560, W, H], fill=(120, 120, 125))
        d.rectangle([0, 560, W, 580], fill=(170, 170, 175))
        text_center(d, 640, 80, "МУРАВЕЙСК" if lang == "ru" else "ANTHILL FALLS", 44, (255, 255, 255), 4, (60, 60, 120))
    elif kind == "lab":
        _vgrad(img, (70, 90, 110), (110, 130, 150), 0, 620)
        for x in range(0, W, 80):
            d.line([(x, 0), (x, 620)], fill=(90, 110, 130), width=2)
        d.rectangle([0, 620, W, H], fill=(60, 65, 75))
        d.rectangle([60, 470, 330, 490], fill=(140, 110, 80))
        d.rectangle([80, 490, 100, 620], fill=(100, 80, 60))
        d.rectangle([290, 490, 310, 620], fill=(100, 80, 60))
        for i, c in enumerate([(255, 80, 80), (80, 200, 255), (120, 255, 120)]):
            fx = 110 + i * 70
            d.ellipse([fx, 420, fx + 40, 470], fill=c, outline=BLACK, width=2)
            d.rectangle([fx + 14, 395, fx + 26, 425], fill=(220, 230, 240), outline=BLACK)
        d.rounded_rectangle([780, 60, 1180, 140], radius=12, fill=(250, 220, 50), outline=BLACK, width=4)
        text_center(d, 980, 100, "РЕГЕНЕРИН-9000" if lang == "ru" else "REGENERIN-9000", 34, BLACK)
    elif kind == "kitchen":
        _vgrad(img, (255, 235, 170), (250, 215, 150), 0, 600)
        d.rectangle([0, 600, W, H], fill=(180, 130, 90))
        d.rectangle([880, 90, 1160, 330], fill=(150, 210, 255), outline=(255, 255, 255), width=12)
        d.line([(1020, 90), (1020, 330)], fill=(255, 255, 255), width=8)
        d.rectangle([60, 180, 260, 600], fill=(235, 240, 245), outline=(150, 150, 160), width=4)
        d.line([(60, 330), (260, 330)], fill=(150, 150, 160), width=4)
        d.rectangle([380, 470, 1240, 600], fill=(170, 110, 70), outline=(110, 70, 40), width=4)
        d.rectangle([370, 455, 1250, 475], fill=(220, 220, 225))
    elif kind == "barber":
        _vgrad(img, (120, 200, 190), (90, 170, 160), 0, 600)
        d.rectangle([0, 600, W, H], fill=(240, 240, 240))
        for x in range(0, W, 60):
            d.rectangle([x, 600 + (x // 60 % 2) * 30, x + 60, 630 + (x // 60 % 2) * 30], fill=(40, 40, 40))
        d.rounded_rectangle([420, 70, 860, 360], radius=20, fill=(210, 235, 245), outline=(170, 130, 60), width=12)
        d.rectangle([1120, 120, 1160, 420], fill=(255, 255, 255), outline=BLACK, width=3)
        for k in range(6):
            d.line([(1120, 130 + k * 50), (1160, 160 + k * 50)], fill=(220, 30, 30), width=10)
        text_center(d, 640, 40, "ПАРИКМАХЕРСКАЯ" if lang == "ru" else "BARBERSHOP", 30, (255, 255, 255), 3, (40, 90, 90))
    elif kind == "food":
        _vgrad(img, (255, 210, 180), (240, 180, 150), 0, 560)
        d.rectangle([0, 560, W, H], fill=(150, 100, 70))
        d.rectangle([250, 480, 1030, 520], fill=(250, 250, 250), outline=(180, 0, 0), width=4)
        for x in range(260, 1030, 40):
            d.rectangle([x, 482, x + 20, 518], fill=(230, 60, 60))
        d.rectangle([300, 520, 320, 650], fill=(100, 70, 50))
        d.rectangle([960, 520, 980, 650], fill=(100, 70, 50))
    elif kind in ("park", "fight", "climax"):
        _vgrad(img, (110, 180, 245), (190, 225, 255), 0, 520)
        d.ellipse([1080, 40, 1200, 160], fill=(255, 230, 90))
        for hx, hr in ((150, 300), (600, 380), (1050, 320)):
            d.ellipse([hx - hr, 440, hx + hr, 640], fill=(110, 190, 90))
        d.rectangle([0, 520, W, H], fill=(100, 180, 80))
        for tx in (90, 330, 980, 1210):
            d.rectangle([tx - 14, 360, tx + 14, 540], fill=(120, 80, 40))
            d.ellipse([tx - 80, 230, tx + 80, 400], fill=(60, 150, 60))
        d.polygon([(480, 600), (800, 600), (760, 660), (440, 660)], fill=(230, 60, 60))
        for k in range(6):
            d.line([(470 + k * 55, 600), (450 + k * 55, 660)], fill=(255, 255, 255), width=5)
        d.ellipse([560, 575, 640, 610], fill=(240, 200, 120), outline=BLACK, width=2)
    elif kind == "ending":
        _vgrad(img, (190, 170, 230), (160, 140, 210), 0, 590)
        d.rectangle([0, 590, W, H], fill=(140, 100, 70))
        d.rounded_rectangle([760, 400, 1220, 600], radius=30, fill=(80, 120, 200), outline=BLACK, width=4)
        d.rounded_rectangle([760, 330, 1220, 440], radius=30, fill=(70, 105, 180), outline=BLACK, width=4)
        d.rectangle([180, 110, 460, 300], fill=(255, 250, 230), outline=(150, 110, 60), width=10)
        text_center(d, 320, 205, "Я ♥ ЗДОРОВ" if lang == "ru" else "I ♥ HEALING", 26, (200, 30, 40))
    return img
