"""Neural voiceover cache for Grade 8 lessons (edge-tts)."""
from __future__ import annotations

import asyncio
import hashlib
import subprocess
import wave
from pathlib import Path

VOICE = "en-US-JennyNeural"
RATE = "-8%"
CACHE = Path(__file__).resolve().parent / "voice"
FFMPEG = "ffmpeg"

SUP = {
    "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
    "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9",
    "ⁿ": "n", "⁻": "negative ",
}
ORD = {"0": "zero", "1": "one", "2": "squared", "3": "cubed", "4": "to the fourth",
       "5": "to the fifth", "6": "to the sixth", "7": "to the seventh",
       "8": "to the eighth", "9": "to the ninth", "n": "to the n"}


def spoken(text: str) -> str:
    s = str(text)
    s = s.replace("√", " square root of ")
    s = s.replace("π", " pi ")
    s = s.replace("×", " times ")
    s = s.replace("÷", " divided by ")
    s = s.replace("·", " times ")
    s = s.replace("−", " minus ")
    s = s.replace("–", " minus ")
    s = s.replace("≠", " is not equal to ")
    s = s.replace("≤", " less than or equal to ")
    s = s.replace("≥", " greater than or equal to ")
    s = s.replace("→", " goes to ")
    s = s.replace("°", " degrees ")
    s = s.replace("∞", " infinity ")
    s = s.replace("±", " plus or minus ")

    def sup_chunk(m):
        raw = "".join(SUP.get(c, c) for c in m.group(0)).strip()
        if raw in ORD:
            return " " + ORD[raw] + " "
        if raw.startswith("negative"):
            return " to the " + raw + " "
        return " to the " + raw + " "

    import re
    s = re.sub(r"[⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ⁻]+", sup_chunk, s)
    s = re.sub(r"\^(\{)?(-?[0-9n]+)(\})?", lambda m: " " + ORD.get(m.group(2), "to the " + m.group(2)) + " ", s)
    s = s.replace("=", " equals ")
    s = " ".join(s.split())
    if s and s[-1] not in ".!?":
        s += "."
    return s


def _duration(path: Path) -> float:
    with wave.open(str(path), "rb") as wf:
        return wf.getnframes() / float(wf.getframerate() or 1)


async def _synth(text: str, mp3: Path) -> None:
    import edge_tts
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    await communicate.save(str(mp3))


def ensure_voice(text: str) -> tuple[Path, float]:
    CACHE.mkdir(parents=True, exist_ok=True)
    line = spoken(text)
    digest = hashlib.sha1((VOICE + RATE + line).encode("utf-8")).hexdigest()[:16]
    wav = CACHE / f"{digest}.wav"
    if wav.exists() and wav.stat().st_size > 44:
        return wav, _duration(wav)
    mp3 = CACHE / f"{digest}.mp3"
    asyncio.run(_synth(line, mp3))
    subprocess.run(
        [FFMPEG, "-y", "-i", str(mp3), "-ar", "44100", "-ac", "1", str(wav)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    mp3.unlink(missing_ok=True)
    return wav, _duration(wav)
