"""Build the Phase 1 session seed: skills + question bank -> JSON.

Run from the repo root:

    python build_session_seed.py

Output: veelearn-backend/seed/session_seed.json  (loaded once on boot by
session-schema.js when the `skills` table is empty).

The script is a validator first and a writer second. It refuses to emit a seed
that would make the session engine serve a broken question — a wrong answer key,
a missing distractor rationale, a duplicate stem, a prerequisite that does not
exist, or a skill with no questions at all.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# Windows consoles default to cp1252 and choke on the unicode in stems/hints.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # noqa: BLE001 - older/odd streams are fine
    pass

from seed.qbank import QUESTIONS  # noqa: E402
from seed.skill_tree import SKILLS, TRACKS  # noqa: E402

ROOT = Path(__file__).parent
OUT = ROOT / "veelearn-backend" / "seed" / "session_seed.json"

KEYS = "ABCD"
# Presets the frontend board can actually mount (widget-engine.js).
VISUAL_PRESETS = {
    "number_line", "function_plot", "area_shade", "coordinate_plane",
    "geometry_board", "triangle_lab", "unit_circle", "parametric_plot",
    "inequality_region", "projectile",
}

MIN_Q_PER_SKILL = 4


def norm_stem(text: str) -> str:
    """Case/punctuation-insensitive stem key for duplicate detection.

    Deliberately conservative: numbers and unicode maths (², ÷, −) are kept, so
    two questions that merely share a template are not reported as duplicates.
    """
    s = str(text).lower().replace("\u2212", "-").replace("\u2013", "-")
    s = re.sub(r"\s+", " ", s).strip()
    return re.sub(r"[\s.:;,]+$", "", s)


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def main() -> int:
    errors: list[str] = []
    codes = [s["code"] for s in SKILLS]

    # ---- skill tree integrity ------------------------------------------
    if len(codes) != len(set(codes)):
        fail(errors, "duplicate skill codes in skill_tree.py")

    track_ids = {t["id"] for t in TRACKS}
    for s in SKILLS:
        if s["track"] not in track_ids:
            fail(errors, f"{s['code']}: unknown track {s['track']!r}")
        if s["prereq"] and s["prereq"] not in codes:
            fail(errors, f"{s['code']}: prerequisite {s['prereq']!r} does not exist")
        if s["prereq"] == s["code"]:
            fail(errors, f"{s['code']}: is its own prerequisite")
        if not s.get("intro"):
            fail(errors, f"{s['code']}: missing intro")
        if not s.get("misconceptions"):
            fail(errors, f"{s['code']}: missing misconceptions")
        if s.get("dot_target") not in (1, 2, 3, 4):
            fail(errors, f"{s['code']}: dot_target must be 1-4")

    # prerequisites must stay inside a track (keeps planning sane)
    by_code = {s["code"]: s for s in SKILLS}
    for s in SKILLS:
        p = s.get("prereq")
        if p and by_code[p]["track"] != s["track"]:
            fail(errors, f"{s['code']}: prerequisite {p} is in another track")

    # ---- question integrity --------------------------------------------
    items = []
    stems: dict[str, str] = {}
    per_skill = Counter()

    for raw in QUESTIONS:
        skill = raw["skill"]
        if skill not in by_code:
            fail(errors, f"question for unknown skill {skill!r}: {raw['stem'][:60]}")
            continue
        tier = raw["tier"]
        if tier not in (1, 2, 3, 4):
            fail(errors, f"{skill}: tier {tier} out of range")
        opts = raw["options"]
        if len(opts) != 4:
            fail(errors, f"{skill}: needs exactly 4 options, got {len(opts)}: {raw['stem'][:50]}")
            continue

        texts = [o[0] for o in opts]
        if len(set(texts)) != 4:
            fail(errors, f"{skill}: duplicate option text: {raw['stem'][:50]}")

        correct = [i for i, o in enumerate(opts) if o[1]]
        if len(correct) != 1:
            fail(errors, f"{skill}: needs exactly one correct option: {raw['stem'][:50]}")
            continue

        for i, (text, is_correct, why) in enumerate(opts):
            if not is_correct and not str(why or "").strip():
                fail(errors, f"{skill}: option {KEYS[i]} lacks a `why`: {raw['stem'][:50]}")

        if len(raw.get("hints") or []) < 2:
            fail(errors, f"{skill}: needs at least 2 hints: {raw['stem'][:50]}")
        if not raw.get("steps"):
            fail(errors, f"{skill}: needs solution steps: {raw['stem'][:50]}")

        raw_visual = raw.get("visual")
        if raw_visual is not None:
            if not isinstance(raw_visual, dict):
                fail(errors, f"{skill}: visual must be a dict: {raw['stem'][:50]}")
            elif raw_visual.get("preset") not in VISUAL_PRESETS:
                fail(errors, f"{skill}: unknown visual preset {raw_visual.get('preset')!r}")
            elif not isinstance(raw_visual.get("params", {}), dict):
                fail(errors, f"{skill}: visual params must be a dict")

        key = norm_stem(raw["stem"])
        if key in stems:
            fail(errors, f"duplicate stem ({skill}): {raw['stem'][:60]}")
        stems[key] = skill

        answer_key = KEYS[correct[0]]
        per_skill[skill] += 1
        items.append(
            {
                "skill": skill,
                "tier": tier,
                "qtype": "mcq",
                "stem": raw["stem"],
                "stem_hash": hashlib.sha256(key.encode("utf-8")).hexdigest(),
                "options": [
                    {"k": KEYS[i], "t": o[0], "why": "" if o[1] else str(o[2]).strip()}
                    for i, o in enumerate(opts)
                ],
                "answer": answer_key,
                "hints": list(raw["hints"]),
                "steps": list(raw["steps"]),
                "visual": raw.get("visual"),
                "source": "authored",
            }
        )

    for s in SKILLS:
        if per_skill[s["code"]] < MIN_Q_PER_SKILL:
            fail(errors, f"{s['code']}: only {per_skill[s['code']]} questions (min {MIN_Q_PER_SKILL})")

    # every tier should exist somewhere per skill's target depth
    for s in SKILLS:
        tiers = {q["tier"] for q in items if q["skill"] == s["code"]}
        if tiers and 1 not in tiers:
            fail(errors, f"{s['code']}: no tier-1 question")

    if errors:
        print("SEED REJECTED\n")
        for e in errors:
            print("  -", e)
        print(f"\n{len(errors)} problem(s). Nothing written.")
        return 1

    # ---- emit -----------------------------------------------------------
    payload = {
        "version": 1,
        "tracks": TRACKS,
        "skills": [
            {
                "code": s["code"],
                "track": s["track"],
                "name": s["name"],
                "grade_band": s["grade_band"],
                "order": s["order"],
                "prereq": s["prereq"],
                "dot_target": s["dot_target"],
                "intro_md": s["intro"],
                "misconceptions": s["misconceptions"],
            }
            for s in SKILLS
        ],
        "questions": items,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")

    size_kb = OUT.stat().st_size / 1024
    print(f"OK  wrote {OUT.relative_to(ROOT)}")
    print(f"    skills    {len(SKILLS)} across {len(TRACKS)} tracks")
    print(f"    questions {len(items)}  ({size_kb:.1f} KB)")
    for t in TRACKS:
        n_skills = sum(1 for s in SKILLS if s["track"] == t["id"])
        n_q = sum(per_skill[s["code"]] for s in SKILLS if s["track"] == t["id"])
        print(f"      {t['id']:<10} {n_skills:>2} skills  {n_q:>3} questions")
    tier_counts = Counter(q["tier"] for q in items)
    print("    tiers     " + "  ".join(f"t{k}={v}" for k, v in sorted(tier_counts.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
