"""Render all Grade 8 ManimGL unit lessons to veelearn-frontend/videos/grade8."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
MANIM = REPO / ".venv-manim" / "Scripts" / "manimgl.exe"
OUT = REPO / "veelearn-frontend" / "videos" / "grade8"
STAGE = Path(os.environ.get("TEMP", str(ROOT / "out"))) / "veelearn-grade8"

SCENES = [
    ("Unit1Exponents", "unit-1-exponents"),
    ("Unit2Equations", "unit-2-equations"),
    ("Unit3Slope", "unit-3-slope"),
    ("Unit4Functions", "unit-4-functions"),
    ("Unit5Substitution", "unit-5-substitution"),
    ("Unit6Elimination", "unit-6-elimination"),
    ("Unit7Pythagoras", "unit-7-pythagoras"),
    ("Unit8Data", "unit-8-data"),
]


def _unlink(path: Path, tries: int = 10) -> None:
    for i in range(tries):
        try:
            path.unlink(missing_ok=True)
            return
        except OSError:
            time.sleep(0.5 * (i + 1))
    path.unlink(missing_ok=True)


def clear_dir(folder: Path, name: str) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    for extra in (f"{name}.mp4", f"{name}_temp.mp4", f"{name}.wav"):
        _unlink(folder / extra)


def publish(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    last_err = None
    for i in range(12):
        try:
            _unlink(dest)
            shutil.copy2(src, dest)
            return
        except OSError as err:
            last_err = err
            time.sleep(0.6 * (i + 1))
    raise last_err


def render_one(cls: str, name: str) -> int:
    clear_dir(STAGE, name)
    cmd = [
        str(MANIM),
        str(ROOT / "scenes.py"),
        cls,
        "-w",
        "-m",
        "--file_name",
        name,
        "--video_dir",
        str(STAGE),
        "-c",
        "#0b1020",
        "--config_file",
        str(ROOT / "custom_config.yml"),
    ]
    print("\n===", name, "===")
    print(" ".join(cmd))
    env = {k: v for k, v in os.environ.items()}
    env["PYTHONPATH"] = str(ROOT)
    env.pop("G8_SMOKE", None)
    # Retry OpenGL access-violation crashes common on Windows.
    for attempt in range(1, 4):
        proc = subprocess.run(cmd, cwd=str(ROOT), env=env)
        staged = STAGE / f"{name}.mp4"
        if proc.returncode == 0 and staged.exists():
            return 0
        print("attempt", attempt, "FAILED", name, proc.returncode, "staged", staged.exists())
        clear_dir(STAGE, name)
        time.sleep(2.5 * attempt)
    return 1


def main():
    STAGE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    only = sys.argv[1:]
    scenes = SCENES
    if only:
        scenes = [s for s in SCENES if s[1] in only or s[0] in only or s[1].split("-")[1] in only]
        if not scenes:
            print("No matching scenes", only)
            return 1
    for cls, name in scenes:
        # Skip if a fresh staged file already exists (resume support).
        staged = STAGE / f"{name}.mp4"
        if "--resume" in only and staged.exists() and staged.stat().st_size > 1_000_000:
            dest = OUT / f"{name}.mp4"
            publish(staged, dest)
            print("resume-copied", dest, dest.stat().st_size)
            continue
        code = render_one(cls, name)
        staged = STAGE / f"{name}.mp4"
        if code != 0 or not staged.exists():
            print("FAILED", name)
            return code or 1
        dest = OUT / f"{name}.mp4"
        publish(staged, dest)
        print("wrote", dest, dest.stat().st_size)
        time.sleep(1.5)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
