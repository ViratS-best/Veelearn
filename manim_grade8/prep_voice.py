"""Pre-synthesize every narration line so renders do not pause on the network."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from units_1_2 import U1, U2
from units_3_4 import U3, U4
from units_5_6 import U5, U6
from units_7_8 import U7, U8
from voice import ensure_voice

UNITS = [U1, U2, U3, U4, U5, U6, U7, U8]


def lines_for(meta: dict) -> list[str]:
    out = [
        f"Let's build a clear picture of {meta['title']}. {meta['subtitle']}.",
        "Here is the path we will take. Each idea gets its own moving picture.",
        "That's the idea. Pause, rewind any step, and try a problem on your own.",
    ]
    for part in meta["parts"]:
        out.append(part["title"] + ". Watch how the pieces move.")
        out.extend(part.get("beats", []))
        examples = part.get("examples", [])[:1]
        for ex in examples:
            out.append("Here is a worked example. " + ex["problem"])
            for i, step in enumerate(ex.get("steps", []), 1):
                out.append("Step " + str(i) + ". " + step)
            out.append("So the answer is " + str(ex["answer"]) + ".")
    return out


def main() -> int:
    n = 0
    for meta in UNITS:
        print("===", meta["file"], "===")
        for line in lines_for(meta):
            path, dur = ensure_voice(line)
            n += 1
            print(f"  {dur:5.1f}s  {line[:72]}")
    print("cached", n, "lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
