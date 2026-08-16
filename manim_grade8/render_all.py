"""Render all Grade 8 ManimGL unit lessons to veelearn-frontend/videos/grade8."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
MANIM = REPO / ".venv-manim" / "Scripts" / "manimgl.exe"
OUT = REPO / "veelearn-frontend" / "videos" / "grade8"

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


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    only = sys.argv[1:]
    scenes = SCENES
    if only:
        scenes = [s for s in SCENES if s[1] in only or s[0] in only or s[1].split("-")[1] in only]
        if not scenes:
            print("No matching scenes", only)
            return 1
    for cls, name in scenes:
        cmd = [
            str(MANIM),
            str(ROOT / "scenes.py"),
            cls,
            "-w",
            "-m",
            "--file_name",
            name,
            "--video_dir",
            str(OUT),
            "-c",
            "#0b1020",
            "--config_file",
            str(ROOT / "custom_config.yml"),
        ]
        print("\n===", name, "===")
        print(" ".join(cmd))
        env = {k: v for k, v in __import__("os").environ.items()}
        env["PYTHONPATH"] = str(ROOT)
        env.pop("G8_SMOKE", None)
        proc = subprocess.run(cmd, cwd=str(ROOT), env=env)
        if proc.returncode != 0:
            print("FAILED", name, proc.returncode)
            return proc.returncode
        dest = OUT / f"{name}.mp4"
        print("wrote", dest, "exists" if dest.exists() else "MISSING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
