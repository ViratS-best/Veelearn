"""Tiny kid-friendly WAV stingers for ManimGL (no 3b1b assets needed)."""
from __future__ import annotations

import wave
from pathlib import Path

import numpy as np

SR = 22050
OUT = Path(__file__).resolve().parent / "sounds"


def save(name: str, samples: np.ndarray) -> None:
    samples = np.clip(np.asarray(samples, dtype=np.float64), -1.0, 1.0)
    pcm = (samples * 32767).astype(np.int16)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.wav"
    with wave.open(str(path), "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SR)
        wav.writeframes(pcm.tobytes())
    print(f"{path.name} {len(samples) / SR:.3f}s")


def envelope(t: np.ndarray, attack=0.004, decay=0.07) -> np.ndarray:
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    d = np.exp(-np.maximum(t - attack, 0) / max(decay, 1e-4))
    return a * d


def tone(freq: float, dur: float, decay=0.08, volume=0.55) -> np.ndarray:
    n = max(int(SR * dur), 1)
    t = np.linspace(0, dur, n, False)
    wave = np.sin(2 * np.pi * freq * t)
    wave += 0.22 * np.sin(4 * np.pi * freq * t)
    return volume * wave * envelope(t, 0.004, decay)


def mix(*parts: np.ndarray) -> np.ndarray:
    length = max(len(p) for p in parts)
    out = np.zeros(length)
    for part in parts:
        out[: len(part)] += part
    peak = np.max(np.abs(out)) or 1.0
    return 0.92 * out / peak


def place(clip: np.ndarray, start: float) -> np.ndarray:
    offset = int(start * SR)
    out = np.zeros(offset + len(clip))
    out[offset : offset + len(clip)] = clip
    return out


def noise(dur: float, volume=0.25) -> np.ndarray:
    n = max(int(SR * dur), 1)
    t = np.linspace(0, dur, n, False)
    rng = np.random.default_rng(7)
    return volume * rng.normal(0, 1, n) * envelope(t, 0.008, dur * 0.45)


def main() -> None:
    save("pop", mix(tone(880, 0.11, 0.035, 0.7), tone(1320, 0.09, 0.03, 0.35)))
    save("click", mix(tone(1900, 0.045, 0.012, 0.45), noise(0.04, 0.12)))
    save(
        "ding",
        mix(tone(784, 0.32, 0.11, 0.55), place(tone(1175, 0.26, 0.1, 0.5), 0.07)),
    )
    whoosh_t = np.linspace(0, 0.28, int(SR * 0.28), False)
    sweep = np.sin(2 * np.pi * (220 + 1400 * whoosh_t) * whoosh_t)
    save("whoosh", mix(sweep * envelope(whoosh_t, 0.02, 0.12) * 0.35, noise(0.28, 0.18)))
    save(
        "sparkle",
        mix(
            tone(1046, 0.16, 0.06, 0.4),
            place(tone(1318, 0.16, 0.06, 0.4), 0.07),
            place(tone(1568, 0.22, 0.08, 0.45), 0.14),
        ),
    )
    save(
        "success",
        mix(
            tone(523, 0.22, 0.1, 0.4),
            tone(659, 0.28, 0.12, 0.4),
            place(tone(784, 0.34, 0.14, 0.5), 0.08),
        ),
    )
    thud_t = np.linspace(0, 0.18, int(SR * 0.18), False)
    thud = np.sin(2 * np.pi * 90 * thud_t) * envelope(thud_t, 0.003, 0.05)
    save("thud", mix(thud * 0.8, noise(0.12, 0.08)))
    save("wrong", mix(tone(220, 0.22, 0.08, 0.5), place(tone(165, 0.2, 0.09, 0.45), 0.06)))


if __name__ == "__main__":
    main()
