"""Синтез музыки и звуковых эффектов (numpy, без внешних файлов)."""

from functools import lru_cache

import numpy as np

SR = 44100


def _t(dur: float) -> np.ndarray:
    return np.arange(int(dur * SR)) / SR


def _note(freq: float, dur: float, kind: str = "square", vol: float = 1.0) -> np.ndarray:
    t = _t(dur)
    if freq <= 0:
        return np.zeros_like(t)
    ph = 2 * np.pi * freq * t
    if kind == "square":
        w = np.sign(np.sin(ph)) * 0.5 + 0.5 * np.sin(ph)
    elif kind == "tri":
        w = 2 / np.pi * np.arcsin(np.sin(ph))
    else:
        w = np.sin(ph)
    env = np.minimum(1, t / 0.01) * np.exp(-t * 3.5)
    return (w * env * vol).astype(np.float32)


def _hz(n: int) -> float:
    return 440.0 * 2 ** ((n - 69) / 12)


@lru_cache(maxsize=8)
def music(style: str) -> np.ndarray:
    """Looping 8-bar backing track: 'happy' (C major bounce) or 'villain' (minor tuba march)."""
    styles = {
        "happy": (132, [(48, [60, 64, 67]), (43, [59, 62, 67]), (45, [57, 60, 64]), (41, [57, 60, 65])],
                  [72, 76, 79, 76, 74, 71, 74, 79, 72, 76, 81, 79, 77, 76, 74, 72,
                   72, 76, 79, 84, 83, 79, 74, 71, 69, 72, 76, 72, 77, 74, 72, 0], "square"),
        "villain": (112, [(45, [57, 60, 64]), (41, [57, 60, 65]), (40, [56, 59, 64]), (45, [57, 60, 64])],
                    [69, 0, 72, 69, 68, 0, 71, 68, 69, 0, 76, 74, 72, 71, 69, 68,
                     69, 0, 72, 69, 65, 0, 69, 65, 64, 68, 71, 74, 76, 0, 69, 0], "tri"),
        "sad": (76, [(45, [57, 60, 64]), (41, [57, 60, 65]), (48, [55, 60, 64]), (43, [55, 59, 62])],
                [76, 0, 74, 72, 74, 0, 72, 69, 72, 0, 71, 67, 71, 0, 0, 0,
                 69, 0, 72, 76, 77, 76, 74, 72, 71, 0, 67, 69, 71, 0, 0, 0], "sine"),
        "action": (156, [(40, [52, 55, 59]), (40, [52, 55, 59]), (43, [55, 59, 62]), (45, [57, 60, 64])],
                   [64, 64, 67, 64, 71, 69, 67, 64, 64, 64, 67, 64, 72, 71, 69, 67,
                    64, 67, 71, 76, 74, 71, 67, 71, 69, 72, 76, 72, 71, 67, 64, 0], "square"),
        "romance": (88, [(48, [60, 64, 67]), (45, [57, 60, 64]), (41, [57, 60, 65]), (43, [55, 59, 62])],
                    [79, 0, 76, 77, 79, 0, 72, 0, 77, 0, 74, 76, 77, 0, 0, 0,
                     76, 0, 72, 74, 76, 0, 69, 0, 74, 0, 71, 72, 74, 0, 0, 0], "sine"),
        "lair": (96, [(38, [50, 53, 57]), (39, [51, 55, 58]), (38, [50, 53, 57]), (37, [49, 53, 56])],
                 [62, 0, 63, 0, 62, 0, 58, 0, 62, 0, 63, 65, 66, 0, 0, 0,
                  62, 0, 63, 0, 62, 0, 57, 0, 56, 0, 57, 0, 50, 0, 0, 0], "tri"),
    }
    bpm, chords, melody, lead = styles.get(style, styles["happy"])
    chords = chords * 2
    beat = 60 / bpm
    bar = beat * 4
    total = int(bar * len(chords) * SR)
    out = np.zeros(total, np.float32)

    def add(clip: np.ndarray, at: float) -> None:
        i = int(at * SR)
        j = min(total, i + len(clip))
        out[i:j] += clip[: j - i]

    for b, (bass, ch) in enumerate(chords):
        for q in range(4):
            at = b * bar + q * beat
            add(_note(_hz(bass if q % 2 == 0 else bass + 7), beat * 0.9, "tri", 0.55), at)
            if q % 2 == 1:
                for n in ch:
                    add(_note(_hz(n), beat * 0.4, "sine", 0.18), at)
            # hat / kick
            k = _t(0.08)
            add((np.sin(2 * np.pi * 60 * k) * np.exp(-k * 40) * (0.6 if q % 2 == 0 else 0)).astype(np.float32), at)
            add((np.random.default_rng(q + b).uniform(-1, 1, len(k)) * np.exp(-k * 80) * 0.12).astype(np.float32), at + beat / 2)
    for i, n in enumerate(melody):
        if n:
            add(_note(_hz(n), beat * 0.95, lead, 0.32), i * beat)
    out /= np.max(np.abs(out)) or 1
    return out


def _noise(dur: float, seed: int = 0) -> np.ndarray:
    return np.random.default_rng(seed).uniform(-1, 1, int(dur * SR)).astype(np.float32)


def _lowpass(x: np.ndarray, k: int) -> np.ndarray:
    return np.convolve(x, np.ones(k) / k, mode="same").astype(np.float32)


@lru_cache(maxsize=32)
def sfx(name: str) -> np.ndarray:
    """Return a sound effect clip by name."""
    if name == "fanfare":
        out = np.zeros(int(1.6 * SR), np.float32)
        for i, n in enumerate([60, 64, 67, 72]):
            c = _note(_hz(n), 0.6 if i < 3 else 1.2, "square", 0.6)
            s = int(i * 0.14 * SR)
            out[s:s + len(c)] += c[: len(out) - s]
        return out / np.max(np.abs(out))
    if name == "trip":
        t = _t(0.5)
        thump = np.sin(2 * np.pi * (90 - 40 * t) * t) * np.exp(-t * 9)
        return (thump + _lowpass(_noise(0.5), 8) * np.exp(-t * 15) * 0.6).astype(np.float32)
    if name == "splash":
        t = _t(1.4)
        n = _lowpass(_noise(1.4, 2), 4) * np.exp(-t * 3.5)
        bub = sum(np.sin(2 * np.pi * (300 + 500 * ((t * (3 + j)) % 1)) * t) * 0.15 * np.exp(-t * 2) for j in range(4))
        return (n + bub).astype(np.float32)
    if name == "heal":
        out = np.zeros(int(1.0 * SR), np.float32)
        for i, n in enumerate([84, 88, 91, 96, 100]):
            c = _note(_hz(n), 0.5, "sine", 0.5)
            s = int(i * 0.08 * SR)
            out[s:s + len(c)] += c[: len(out) - s]
        return out
    if name == "spray":
        t = _t(1.6)
        hiss = _noise(1.6, 5) - _lowpass(_noise(1.6, 5), 6)
        return (hiss * np.minimum(1, t / 0.05) * np.minimum(1, (1.6 - t) / 0.3) * 0.7).astype(np.float32)
    if name == "sputter":
        t = _t(1.8)
        gate = (np.sin(2 * np.pi * 3 * t) > 0.6).astype(np.float32)
        return ((_noise(1.8, 6) - _lowpass(_noise(1.8, 6), 6)) * gate * 0.6).astype(np.float32)
    if name == "splat":
        t = _t(0.7)
        return (np.sin(2 * np.pi * (70 - 30 * t) * t) * np.exp(-t * 6) * 1.2
                + _lowpass(_noise(0.7, 9), 5) * np.exp(-t * 10)).astype(np.float32)
    if name == "boing":
        t = _t(0.9)
        f = 180 + 220 * t + 40 * np.sin(2 * np.pi * 14 * t)
        return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3)).astype(np.float32)
    if name == "land":
        return sfx("trip") * 1.2
    if name == "snip":
        out = np.zeros(int(2.0 * SR), np.float32)
        for i in range(6):
            c = (_noise(0.04, i) * np.exp(-_t(0.04) * 90)).astype(np.float32)
            s = int(i * 0.33 * SR)
            out[s:s + len(c)] += c
        return out
    if name == "siren":
        t = _t(3.0)
        f = np.where((t * 2) % 1 < 0.5, 700, 950)
        return (np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.35 * np.minimum(1, (3 - t) / 0.5)).astype(np.float32)
    if name == "whoosh":
        t = _t(0.6)
        n = _noise(0.6, 11)
        k = np.sin(np.pi * t / 0.6)
        return (_lowpass(n, 3) * k * 0.8).astype(np.float32)
    if name == "zap":
        t = _t(0.5)
        f = 1800 - 2600 * t
        return (np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t * 5) * 0.4).astype(np.float32)
    if name == "pop":
        t = _t(0.2)
        return (np.sin(2 * np.pi * (400 + 1600 * t) * t) * np.exp(-t * 25)).astype(np.float32)
    if name == "ding":
        t = _t(1.2)
        return ((np.sin(2 * np.pi * 1318 * t) + 0.5 * np.sin(2 * np.pi * 2637 * t)) * np.exp(-t * 3) * 0.5).astype(np.float32)
    if name == "boom":
        t = _t(1.5)
        return (_lowpass(_noise(1.5, 13), 30) * 6 * np.exp(-t * 2.5) + np.sin(2 * np.pi * 50 * t) * np.exp(-t * 3)).astype(np.float32)
    if name == "bzz":
        t = _t(1.5)
        f = 520 + 40 * np.sin(2 * np.pi * 7 * t)
        return (np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.18 * np.minimum(1, (1.5 - t) / 0.3)).astype(np.float32)
    if name == "cheer":
        t = _t(2.5)
        n = _lowpass(_noise(2.5, 17), 12) * 4
        claps = (np.random.default_rng(3).random(len(t)) > 0.9993).astype(np.float32)
        claps = np.convolve(claps, np.exp(-np.arange(400) / 60), mode="same")
        return ((n * 0.5 + claps * 0.6) * np.minimum(1, t / 0.3) * np.minimum(1, (2.5 - t) / 0.6)).astype(np.float32)
    if name == "dart":
        return (sfx("whoosh")[: int(0.3 * SR)] + np.pad(sfx("pop"), (int(0.25 * SR), 0))[: int(0.3 * SR)]).astype(np.float32)
    if name == "ouch":
        t = _t(0.5)
        return (np.sin(2 * np.pi * (600 - 500 * t) * t) * np.exp(-t * 6) * 0.6).astype(np.float32)
    return np.zeros(100, np.float32)
