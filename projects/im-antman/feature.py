"""Полнометражный «I'm Antman! (Я Энтмен!)» — сборка часового фильма.

Запуск:  python feature.py [ru|en|all] [--out DIR] [--workers 4] [--only N] [--sheet PNG]
Сценарий — файлы chapters/*.txt (формат описан в stage.py).
"""

import argparse
import bisect
import glob
import hashlib
import logging
import math
import multiprocessing as mp
import os
import subprocess
import textwrap

import numpy as np
from PIL import Image, ImageDraw

import draw as D
import sound
import stage as ST
import tts

log = logging.getLogger("feature")
FPS = 24
SR = tts.SR
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")

NAMES = {
    "ru": {"N": "Рассказчик", "A": "Антон", "S": "Профессор Квасов", "M": "Мама", "P": "Парикмахер",
           "B": "Барон Дихлофос", "G": "Гоша", "L": "Лена", "T": "Доктор Тапок", "K": "Мадам Москитка",
           "C": "Капитан Петрович", "O": "Шеф Борис", "D": "Доктор Айболит", "H": "Ведущий", "X1": "Прохожий", "X2": "Гражданка", "X3": "Зевака"},
    "en": {"N": "Narrator", "A": "Anton", "S": "Professor Kvasov", "M": "Mom", "P": "Barber",
           "B": "Baron Bugspray", "G": "Gosha", "L": "Lena", "T": "Doctor Slipper", "K": "Madame Mosquito",
           "C": "Captain Petrovich", "O": "Boss Boris", "D": "Doctor Feelgood", "H": "TV Host", "X1": "Passerby", "X2": "Citizen", "X3": "Onlooker"},
}

CREDITS = {
    "ru": ["«Я Энтмен!»", "Полнометражная комедия · 12+", "", "В РОЛЯХ", "Антон Мурашов / Энтмен",
           "Гоша — говорящий муравей", "Лена Синицына — журналистка", "Профессор Квасов", "Мама Антона",
           "Шеф Борис", "Капитан Петрович", "", "ЛИГА ВРЕДИТЕЛЕЙ", "Барон Дихлофос", "Доктор Тапок",
           "Мадам Москитка", "", "Голоса, музыка, анимация — сделано ИИ", "", "Ни один муравей не пострадал.",
           "Тапки — пострадали.", "", "Конец"],
    "en": ["I'm Antman!", "A feature comedy · 12+", "", "STARRING", "Anton Murashov / Antman",
           "Gosha — the talking ant", "Lena Sinitsyna — reporter", "Professor Kvasov", "Anton's Mom",
           "Boss Boris", "Captain Petrovich", "", "THE LEAGUE OF PESTS", "Baron Bugspray", "Doctor Slipper",
           "Madame Mosquito", "", "Voices, music, animation — made by AI", "", "No ants were harmed.",
           "Several slippers were.", "", "The End"],
}

SCENES: list[ST.Scene] = []
STARTS: list[float] = []


# ---------------- build ----------------

def load_script() -> list[ST.Scene]:
    """Load all chapter files in order."""
    text = ""
    for p in sorted(glob.glob(os.path.join(HERE, "chapters", "*.txt"))):
        with open(p, encoding="utf-8") as f:
            text += f.read() + "\n"
    return ST.parse(text)


def _cache_path(text: str, lang: str, spk: str) -> str:
    key = hashlib.md5(repr((text, lang, spk, tts.VOICES[lang][spk])).encode()).hexdigest()
    return os.path.join(CACHE, key + ".npy")


def voice(text: str, lang: str, spk: str) -> np.ndarray:
    """TTS with on-disk cache."""
    os.makedirs(CACHE, exist_ok=True)
    path = _cache_path(text, lang, spk)
    if os.path.exists(path):
        return np.load(path)
    a = tts.synth(text, lang, spk)
    np.save(path, a)
    return a


def _synth_job(job: tuple[str, str, str]) -> int:
    voice(*job)
    return 1


def build(lang: str) -> float:
    """Synthesize and lay out. Fills SCENES; returns total seconds."""
    scenes = load_script()
    jobs = {(ln.ru if lang == "ru" else ln.en, lang, ln.spk) for sc in scenes for ln in sc.lines if ln.spk}
    todo = [j for j in jobs if not os.path.exists(_cache_path(*j))]
    if todo:
        log.info("[%s] synthesizing %d lines", lang, len(todo))
        with mp.get_context("fork").Pool(4) as pool:
            pool.map(_synth_job, todo, chunksize=4)
    for sc in scenes:
        for ln in sc.lines:
            if ln.spk:
                ln.audio = voice(ln.ru if lang == "ru" else ln.en, lang, ln.spk)
    total = ST.layout(scenes)
    SCENES[:] = scenes
    STARTS[:] = [s.start for s in scenes]
    return total


@__import__("functools").lru_cache(maxsize=32)
def music_var(style: str, shift: int) -> np.ndarray:
    """Music loop transposed by `shift` semitones (resampling)."""
    base = sound.music(style)
    if shift == 0:
        return base
    f = 2 ** (shift / 12)
    idx = np.arange(0, len(base) - 1, f)
    return np.interp(idx, np.arange(len(base)), base).astype(np.float32)


def mix(total: float) -> np.ndarray:
    """Mix voices, effects and ducked music for the whole film."""
    n = int(total * SR) + SR
    voice_b = np.zeros(n, np.float32)
    fx = np.zeros(n, np.float32)
    mus = np.zeros(n, np.float32)

    def put(buf: np.ndarray, clip: np.ndarray, at: float, gain: float = 1.0) -> None:
        i = int(at * SR)
        j = min(n, i + len(clip))
        if j > i:
            buf[i:j] += clip[: j - i] * gain

    shifts = [0, 2, -3, 5, -2, 3]
    for sc in SCENES:
        loop = music_var(sc.music, shifts[sc.index % len(shifts)])
        seg = np.resize(loop, int(sc.dur * SR)).copy()
        r = min(len(seg) // 2, int(0.4 * SR))
        if r > 0:
            seg[:r] *= np.linspace(0, 1, r)
            seg[-r:] *= np.linspace(1, 0, r)
        put(mus, seg, sc.start)
        if sc.bg == "card":
            put(fx, sound.sfx("ding"), sc.start + 0.4, 0.6)
        for ln in sc.lines:
            at = sc.start + ln.start
            if ln.audio is not None:
                put(voice_b, ln.audio, at)
            s1, s2 = ln.opt("sfx"), ln.opt("sfx_end")
            if s1:
                for nm in s1.split(","):
                    put(fx, sound.sfx(nm), at)
            if s2:
                for nm in s2.split(","):
                    put(fx, sound.sfx(nm), at + ln.dur + 0.05)
    env = np.abs(voice_b)
    k = int(0.25 * SR)
    cs = np.cumsum(np.concatenate([[0.0], env]))
    sm = (cs[k:] - cs[:-k]) / k
    sm = np.concatenate([np.zeros(k // 2), sm, np.zeros(len(env) - len(sm) - k // 2)]).astype(np.float32)
    duck = 1.0 - 0.65 * np.clip(sm * 8, 0, 1)
    out = voice_b + fx * 0.5 + mus * 0.2 * duck
    peak = float(np.max(np.abs(out))) or 1.0
    return (out / max(1.0, peak / 0.95)).astype(np.float32)


# ---------------- rendering ----------------

def subtitle(img: Image.Image, text: str, spk: str) -> None:
    """Bottom subtitle box."""
    lines = textwrap.wrap(text, 54)
    if not lines:
        return
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    h = 42 * len(lines) + 20
    d.rounded_rectangle([80, D.H - h - 14, D.W - 80, D.H - 10], radius=14, fill=(0, 0, 0, 165))
    img.alpha_composite(ov)
    d = ImageDraw.Draw(img)
    for i, s in enumerate(lines):
        d.text((640, D.H - h - 14 + 31 + i * 42), s, font=D.font(31), fill=ST.SUB_COLORS.get(spk, (255, 255, 255)),
               anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))


def offscreen_bubble(d: ImageDraw.ImageDraw, spk: str, lang: str, t: float) -> None:
    """Bubble for a speaker who is not on stage (phone / off-screen)."""
    name = NAMES[lang].get(spk, spk)
    icon = "☎ " if spk in ("M", "O", "C", "L") else "♪ "
    d.rounded_rectangle([900, 30, 1250, 120], radius=20, fill=(255, 255, 255), outline=D.BLACK, width=4)
    D.text_center(d, 1075, 75 + math.sin(t * 10) * 2, icon + name, 28, ST.SUB_COLORS.get(spk, (0, 0, 0)), 2)


def render_card(img: Image.Image, sc: ST.Scene, t: float, lang: str) -> None:
    """Chapter card / title / credits."""
    d = ImageDraw.Draw(img)
    for i in range(70):
        x, y = (i * 137) % D.W, (i * 89) % D.H
        b = int(140 + 100 * math.sin(t * 3 + i))
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(b, b, b))
    if sc.bg == "credits":
        rows = CREDITS[lang]
        off = D.H + 40 - t / sc.dur * (D.H + 120 + len(rows) * 58)
        for i, row in enumerate(rows):
            y = off + i * 58
            if -40 < y < D.H + 40:
                D.text_center(d, 640, y, row, 54 if i == 0 else 32, D.GOLD if i in (0, 3, 12) else (240, 240, 240), 3)
        D.hero(d, 1140, 700, 0.55, arms=(20 + 20 * math.sin(t * 4), 150 + 20 * math.sin(t * 6)))
        import cast as C
        C.ant(d, 1220, 700, 0.7, wave=1.0)
        return
    title = sc.title[0] if lang == "ru" else sc.title[1]
    if sc.bg == "title":
        z = min(1.0, t / 2.0)
        D.hero(d, 640, 700, 0.5 + 0.8 * z, arms=(150, 150))
        D.text_center(d, 640, 120, "I'm Antman!", int(40 + 50 * z), D.GOLD, 6, (150, 20, 20))
        D.text_center(d, 640, 215, "(Я Энтмен!)", int(20 + 30 * z), (255, 255, 255), 4, (150, 20, 20))
        D.text_center(d, 640, 285, title, 30, (255, 200, 200), 3)
        D.plus_sparkles(d, 640, 500, (t % 2.0) / 2.0, n=20, spread=220)
        return
    k = min(1.0, t / 0.6)
    parts = title.split(". ", 1)
    D.text_center(d, 640, 290, parts[0], int(30 * k) + 1, (255, 200, 120), 3)
    if len(parts) > 1:
        D.text_center(d, 640, 380, parts[1], int(64 * k) + 1, D.GOLD, 6, (150, 20, 20))
    import cast as C
    C.ant(d, 200 + t * 30, 600, 0.9, wave=1.0)
    D.hero(d, 1080 - t * 20, 690, 0.6, arms=(150, 20))


def frame(gt: float, lang: str) -> Image.Image:
    """Render frame at global time gt."""
    i = max(0, bisect.bisect_right(STARTS, gt) - 1)
    sc = SCENES[i]
    t = gt - sc.start
    cur: ST.Line | None = None
    for ln in sc.lines:
        if t >= ln.start:
            cur = ln
    if sc.bg in ("card", "title", "credits"):
        img = ST.background("card", lang).copy()
        render_card(img, sc, t, lang)
    else:
        img = ST.background(sc.bg, lang, "night" in sc.flags).copy()
        d = ImageDraw.Draw(img)
        ground = ST.GROUND.get(sc.bg, 630)
        if "crowd" in sc.flags:
            import cast as C
            for k in range(9):
                kind = ("X1", "X2", "X3")[k % 3]
                C.figure(d, 70 + k * 145, ground - 70 - abs(math.sin(t * 6 + k)) * 14, kind, 0.55,
                         arms=(150, 150) if (int(t * 2) + k) % 2 else (40, 40))
        acts, effects = ST.actors_at(sc, t, ground)
        ov_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ov = ImageDraw.Draw(ov_img)
        speaking = cur.spk if cur and cur.spk and t - cur.start < cur.dur else None
        lt = t - cur.start if cur else 0.0
        for code, ac in acts.items():
            if ac.visible:
                talking = speaking == code
                ST.draw_actor(d, code, ac, ST.mouth(lt) if talking else 0.0, talking, t)
        used, shake = ST.draw_effects(img, d, ov, acts, effects, t, lang, speaking)
        if speaking and speaking != "N" and (speaking not in acts or not acts[speaking].visible):
            offscreen_bubble(d, speaking, lang, t)
        if used:
            img.alpha_composite(ov_img)
        if shake:
            img = Image.fromarray(np.roll(np.asarray(img), int(shake), axis=1))
    if cur:
        d = ImageDraw.Draw(img)
        for ru, en in cur.caps:
            D.text_center(d, 640, 60, ru if lang == "ru" else en, 46, D.GOLD, 5, (150, 20, 20))
        if cur.spk and t - cur.start < cur.dur + 0.25:
            subtitle(img, cur.ru if lang == "ru" else cur.en, cur.spk)
    fade = min(1.0, t / 0.35, (sc.dur - t) / 0.35)
    if fade < 1.0:
        img = Image.blend(Image.new("RGBA", img.size, (0, 0, 0, 255)), img, max(0.0, fade))
    return img.convert("RGB")


def _encode_range(args: tuple[str, int, int, str]) -> str:
    lang, f0, f1, path = args
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{D.W}x{D.H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-tune", "animation",
           "-crf", "30", "-pix_fmt", "yuv420p", "-g", "240", path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    assert p.stdin is not None
    for f in range(f0, f1):
        p.stdin.write(frame(f / FPS, lang).tobytes())
        if (f - f0) % (FPS * 120) == 0:
            log.info("[%s] %s: %d/%d", lang, os.path.basename(path), f - f0, f1 - f0)
    p.stdin.close()
    p.wait()
    return path


def make(lang: str, out_dir: str, workers: int) -> str:
    """Build one language version."""
    os.makedirs(out_dir, exist_ok=True)
    total = build(lang)
    log.info("[%s] %d scenes, %.1f min", lang, len(SCENES), total / 60)
    audio = mix(total)
    apath = os.path.join(out_dir, f"_audio_{lang}.f32")
    audio[: int(total * SR)].tofile(apath)
    nfr = int(total * FPS)
    # split into chunks at frame boundaries
    chunks = max(workers * 3, 1)
    bounds = [nfr * i // chunks for i in range(chunks + 1)]
    jobs = [(lang, bounds[i], bounds[i + 1], os.path.join(out_dir, f"_seg_{lang}_{i:03d}.mp4")) for i in range(chunks)]
    with mp.get_context("fork").Pool(workers) as pool:
        segs = pool.map(_encode_range, jobs, chunksize=1)
    lst = os.path.join(out_dir, f"_list_{lang}.txt")
    with open(lst, "w") as f:
        for s in segs:
            f.write(f"file '{os.path.abspath(s)}'\n")
    name = "I_m_Antman_Feature_RU.mp4" if lang == "ru" else "I_m_Antman_Feature_EN.mp4"
    out = os.path.join(out_dir, name)
    title = "Я Энтмен! (полнометражный)" if lang == "ru" else "I'm Antman! (feature)"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", apath, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart",
                    "-metadata", f"title={title}", out], check=True)
    for s in segs + [lst, apath]:
        os.remove(s)
    prepend_intro(out)
    return out


INTRO = os.path.join(HERE, "assets", "intro_v3.mp4")


def prepend_intro(path: str) -> None:
    """Put the V3 ORIGINAL studio intro in front of the film (re-encodes)."""
    if not os.path.exists(INTRO):
        return
    tmp = path + ".tmp.mp4"
    fc = ("[0:v]scale=1280:720,fps=24,setsar=1,format=yuv420p[v0];[1:v]fps=24,setsar=1,format=yuv420p[v1];"
          "[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];"
          "[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", INTRO, "-i", path, "-filter_complex", fc,
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-tune", "animation",
                    "-crf", "29", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", "-map_metadata", "1", tmp],
                   check=True)
    os.replace(tmp, path)


def sheet(lang: str, path: str, only: int | None) -> None:
    """Contact sheet of frames for a quick visual check."""
    total = build(lang)
    pts: list[float] = []
    for sc in SCENES:
        if only is not None and sc.index != only:
            continue
        for f in (0.2, 0.45, 0.7, 0.92):
            pts.append(sc.start + sc.dur * f)
    pts = pts[:48]
    cols = 4
    rows = (len(pts) + cols - 1) // cols
    sh = Image.new("RGB", (cols * 320, rows * 180))
    for i, p in enumerate(pts):
        sh.paste(frame(p, lang).resize((320, 180)), ((i % cols) * 320, (i // cols) * 180))
    sh.save(path)
    log.info("total %.1f min", total / 60)


def main() -> None:
    """CLI."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    ap = argparse.ArgumentParser()
    ap.add_argument("lang", nargs="?", default="all", choices=["ru", "en", "all"])
    ap.add_argument("--out", default=os.path.join(HERE, "out"))
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--sheet", default=None)
    ap.add_argument("--only", type=int, default=None)
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.check:
        import re
        for sc in load_script():
            known = set(sc.cast)
            for ln in sc.lines:
                for tok in ln.acts:
                    m = re.match(r"^(?:[a-z]+[=@])?.*?@?([A-Z]\d?)(?=[>=^_~!*:]|$)", tok)
                    codes = re.findall(r"(?:^|@)([A-Z]\d?)(?=[>=^_~!*:]|$)", tok)
                    for c in codes:
                        if c not in known:
                            log.warning("scene %d (%s): '%s' uses %s not in cast", sc.index, sc.bg, tok, c)
                    _ = m
                if ln.spk and ln.spk not in tts.VOICES["ru"]:
                    log.warning("unknown speaker %s", ln.spk)
        return
    langs = ["ru", "en"] if a.lang == "all" else [a.lang]
    for lang in langs:
        if a.stats:
            total = build(lang)
            for sc in SCENES:
                log.info("%3d %-9s %6.1fs  at %5.1f min  lines=%d", sc.index, sc.bg, sc.dur, sc.start / 60, len(sc.lines))
            log.info("[%s] TOTAL %.1f min", lang, total / 60)
        elif a.sheet:
            sheet(lang, a.sheet, a.only)
        else:
            log.info("done: %s", make(lang, a.out, a.workers))


if __name__ == "__main__":
    main()
