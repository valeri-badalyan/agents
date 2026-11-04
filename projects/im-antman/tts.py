"""Офлайн-озвучка: RHVoice (если установлен), иначе espeak-ng.

Каждому персонажу — свой голос и высота тона (через ffmpeg).
"""

import ctypes
import logging
import os
import subprocess
import tempfile

import numpy as np

log = logging.getLogger(__name__)
SR = 44100

# speaker -> (rhvoice voice, espeak voice, pitch factor, tempo)
VOICES: dict[str, dict[str, tuple[str, str, float, float]]] = {
    "ru": {
        "N": ("elena", "ru", 1.0, 0.98),
        "A": ("aleksandr", "ru", 1.14, 1.05),
        "S": ("aleksandr", "ru", 1.32, 1.12),
        "M": ("anna", "ru", 1.05, 1.0),
        "P": ("aleksandr", "ru", 0.95, 1.18),
        "B": ("aleksandr", "ru", 0.74, 0.93),
        "G": ("aleksandr", "ru", 1.6, 1.12),
        "L": ("irina", "ru", 1.04, 1.02),
        "T": ("aleksandr", "ru", 0.86, 1.22),
        "K": ("natalia", "ru", 1.25, 1.05),
        "C": ("aleksandr", "ru", 0.8, 0.9),
        "O": ("aleksandr", "ru", 0.9, 1.12),
        "D": ("aleksandr", "ru", 1.05, 0.95),
        "H": ("aleksandr", "ru", 1.2, 1.15),
        "X1": ("aleksandr", "ru", 1.0, 1.0),
        "X2": ("anna", "ru", 0.92, 0.95),
        "X3": ("aleksandr", "ru", 1.08, 1.1),
    },
    "en": {
        "N": ("clb", "en", 1.0, 0.86),
        "A": ("bdl", "en-us", 1.12, 0.92),
        "S": ("bdl", "en-us", 1.32, 0.99),
        "M": ("slt", "en-us", 1.05, 0.88),
        "P": ("bdl", "en-us", 0.95, 1.04),
        "B": ("bdl", "en-us", 0.74, 0.82),
        "G": ("bdl", "en-us", 1.6, 0.99),
        "L": ("slt", "en-us", 1.1, 0.90),
        "T": ("bdl", "en-us", 0.86, 1.07),
        "K": ("clb", "en-us", 1.28, 0.92),
        "C": ("bdl", "en-us", 0.8, 0.79),
        "O": ("bdl", "en-us", 0.9, 0.99),
        "D": ("bdl", "en-us", 1.05, 0.84),
        "H": ("bdl", "en-us", 1.2, 1.01),
        "X1": ("bdl", "en-us", 1.0, 0.88),
        "X2": ("slt", "en-us", 0.9, 0.84),
        "X3": ("bdl", "en-us", 1.08, 0.97),
    },
}


# how to pronounce things the engine reads badly
SAY: dict[str, dict[str, str]] = {
    "ru": {"V3 ORIGINAL": "Ви Три Ориджинал"},
    "en": {"V3 ORIGINAL": "V Three Original"},
}


def _rhvoice(text: str, voice: str) -> bytes | None:
    try:
        from rhvoice_wrapper import TTS  # type: ignore
    except ImportError:
        return None
    try:
        tts = _rhvoice.tts if hasattr(_rhvoice, "tts") else TTS(threads=1)
        if not hasattr(_rhvoice, "tts"):
            import atexit

            atexit.register(tts.join)
        _rhvoice.tts = tts  # type: ignore[attr-defined]
        if voice not in tts.voices:
            log.warning("RHVoice voice %s missing; have %s", voice, tts.voices)
            return None
        return tts.get(text, voice=voice, format_="wav")
    except Exception as exc:  # noqa: BLE001
        log.warning("RHVoice failed: %s", exc)
        return None


_ESPEAK: dict[str, object] = {}


def _espeak(text: str, voice: str) -> tuple[np.ndarray, int]:
    import espeakng_loader  # type: ignore

    if "lib" not in _ESPEAK:
        lib = ctypes.CDLL(espeakng_loader.get_library_path())
        lib.espeak_Initialize.restype = ctypes.c_int
        sr = lib.espeak_Initialize(1, 0, espeakng_loader.get_data_path().encode(), 0)
        cbtype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_short), ctypes.c_int, ctypes.c_void_p)
        buf: list[np.ndarray] = []

        def cb(wav, n, _ev):  # type: ignore[no-untyped-def]
            if n > 0:
                buf.append(np.ctypeslib.as_array(wav, shape=(n,)).copy())
            return 0

        c = cbtype(cb)
        lib.espeak_SetSynthCallback(c)
        _ESPEAK.update(lib=lib, sr=sr, buf=buf, cb=c)
    lib = _ESPEAK["lib"]
    buf = _ESPEAK["buf"]
    buf.clear()  # type: ignore[union-attr]
    lib.espeak_SetVoiceByName(voice.encode())  # type: ignore[attr-defined]
    lib.espeak_SetParameter(1, 165, 0)  # rate
    data = text.encode("utf-8") + b"\0"
    lib.espeak_Synth(data, len(data), 0, 1, 0, 1, None, None)  # type: ignore[attr-defined]
    lib.espeak_Synchronize()  # type: ignore[attr-defined]
    arr = np.concatenate(buf) if buf else np.zeros(1000, dtype=np.int16)  # type: ignore[arg-type]
    return arr, int(_ESPEAK["sr"])  # type: ignore[arg-type]


def _ffmpeg_fx(src: str, pitch: float, tempo: float) -> np.ndarray:
    """Pitch-shift + tempo, return float32 mono at SR."""
    at = tempo / pitch
    chain = []
    while at > 2.0 or at < 0.5:
        step = 2.0 if at > 2.0 else 0.5
        chain.append(f"atempo={step}")
        at /= step
    chain.append(f"atempo={at:.4f}")
    flt = f"aresample=44100,asetrate={int(44100 * pitch)},aresample=44100," + ",".join(chain)
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-af", flt, "-ac", "1", "-f", "f32le", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(out, dtype=np.float32).copy()


def synth(text: str, lang: str, speaker: str) -> np.ndarray:
    """Synthesize one line for a speaker; returns float32 mono at SR."""
    rv, ev, pitch, tempo = VOICES[lang][speaker]
    for a, b in SAY.get(lang, {}).items():
        text = text.replace(a, b)
    if not any(ch.isalpha() for ch in text):
        return np.zeros(int(1.2 * SR), np.float32)
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "v.wav")
        wav = _rhvoice(text, rv)
        if wav:
            with open(path, "wb") as f:
                f.write(wav)
        else:
            import wave

            arr, sr = _espeak(text, ev)
            with wave.open(path, "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(sr)
                w.writeframes(arr.astype(np.int16).tobytes())
        audio = _ffmpeg_fx(path, pitch, tempo)
    if audio.size == 0:
        return np.zeros(int(0.5 * SR), np.float32)
    peak = float(np.max(np.abs(audio))) or 1.0
    return audio / peak * 0.9
