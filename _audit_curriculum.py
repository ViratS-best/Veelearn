#!/usr/bin/env python3
"""Deep audit of curriculum polish: diagrams, uniqueness, scaffolds, solved examples."""
from __future__ import annotations

import importlib
import re
import sys

from curriculum_kit import (
    asks_for_tool,
    diagram_for_context,
    pick_diagram,
    pick_scaffold,
    polish_content,
    stem_key,
)

PACKAGES = [
    ("grade1_math_curriculum", "First"),
    ("grade2_math_curriculum", "Second"),
    ("grade3_math_curriculum", "Third"),
    ("grade4_math_curriculum", "Fourth"),
    ("grade5_math_curriculum", "Fifth"),
    ("grade6_math_curriculum", "Sixth"),
    ("grade7_math_curriculum", "Seventh"),
    ("grade8_math_curriculum", "Eighth"),
    ("algebra2_curriculum", "Algebra 2"),
    ("mathcounts_curriculum", "MathCounts"),
]

BANNED = re.compile(r"\b(wait|recalculate)\b", re.I)
FIXED_TAPE = re.compile(r"A tape diagram keeps the parts lined up\.")  # old caption
OLD_FIXED_CAPTIONS = [
    "A tape diagram keeps the parts lined up.",
    "Sketch the situation on a line or table.",
]


def audit_unit(title, content, questions, issues):
    if len(questions) != 55:
        issues.append(f"{title}: {len(questions)} questions (want 55)")
    slots = len(re.findall(r"<!--QUIZ_SLOT_\d+-->", content))
    if slots != 55:
        issues.append(f"{title}: {slots} quiz slots (want 55)")

    stems = []
    for q in questions:
        text = q.get("question_text") or ""
        ans = q.get("correct_answer")
        opts = q.get("options") or []
        if ans not in opts:
            issues.append(f"{title}: answer {ans!r} not in options for Q{q.get('order_index')}")
        if len(opts) != 4:
            issues.append(f"{title}: {len(opts)} options on Q{q.get('order_index')}")
        if BANNED.search(text) or BANNED.search(q.get("explanation") or ""):
            issues.append(f"{title}: banned phrasing Q{q.get('order_index')}")

        plain = stem_key(text)
        stems.append(plain)

        has_diag = "vl-q-diagram" in text or "<svg" in text
        has_scaf = "vl-scaffold" in text

        # No diagram/scaffold unless tool language (or already in stem from bank)
        if has_scaf and not asks_for_tool(text):
            # scaffold HTML itself may contain "Fill the ratio table" — check stem only
            stem_only = re.sub(r'<div class="vl-scaffold".*?</div>\s*</div>', " ", text, flags=re.S)
            stem_only = re.sub(r'<div class="vl-q-diagram".*?</div>', " ", stem_only, flags=re.S)
            if not asks_for_tool(stem_only):
                issues.append(
                    f"{title}: Q{q.get('order_index')} has scaffold without tool cue: {plain[:80]!r}"
                )

        if has_diag and not asks_for_tool(text):
            stem_only = re.sub(r'<div class="vl-scaffold".*?</div>\s*</div>', " ", text, flags=re.S)
            stem_only = re.sub(r'<div class="vl-q-diagram".*?</div>', " ", stem_only, flags=re.S)
            # Quizzes should not get random diagrams
            if not asks_for_tool(stem_only) and "vl-q-diagram" in text:
                issues.append(
                    f"{title}: Q{q.get('order_index')} has diagram without tool cue: {plain[:80]!r}"
                )

        # irrational must never get ratio stuff
        if "irrational" in plain and ("ratio table" in text.lower() or "tape" in text.lower()):
            issues.append(f"{title}: irrational Q got ratio/tape visual")

    if len(stems) != len(set(stems)):
        # find dupes
        seen = {}
        for i, s in enumerate(stems, 1):
            if s in seen:
                issues.append(f"{title}: duplicate stem Q{seen[s]} and Q{i}: {s[:70]!r}")
                break
            seen[s] = i

    # Solved examples: diagrams only when the problem itself is visual; never force random ones.
    solved_blocks = re.findall(
        r'<div style="background:#f8fafc;border:1px solid #cbd5e1;border-radius:12px;'
        r'padding:18px;margin:18px 0;">.*?</div>',
        content,
        flags=re.I | re.S,
    )
    nonsense = 0
    for block in solved_blocks:
        if re.search(r"Marked value:\s*\d+", block, re.I):
            nonsense += 1
        plain = re.sub(r"<[^>]+>", " ", block)
        has_fig = bool(re.search(r"<svg|vl-figure|vl-q-diagram", block, re.I))
        # If the problem is clearly combinatorial and we drew a number line — bad
        if has_fig and re.search(r"number line|Marked value", block, re.I):
            if re.search(r"letter string|password|permutation|combination|at least one", plain, re.I):
                issues.append(f"{title}: combinatorics example got a number-line diagram")
    if nonsense:
        issues.append(f"{title}: {nonsense} nonsense 'Marked value' diagrams")

    # Hard / stretch quizzes must not be trivial outfit fillers
    for q in questions:
        if q.get("difficulty") not in ("hard", "stretch"):
            continue
        plain = stem_key(q.get("question_text") or "")
        if "outfit" in plain or "(set " in (q.get("question_text") or "").lower():
            issues.append(f"{title}: hard/stretch Q{q.get('order_index')} still trivial: {plain[:70]!r}")

    # Diagram variety in content: tape captions should vary if multiple tapes
    tapes = re.findall(r"Tape parts: ([^<]+)", content)
    if len(tapes) >= 3 and len(set(tapes)) == 1:
        issues.append(f"{title}: all tape diagrams use same parts {tapes[0]!r}")

    fracs = re.findall(r"(\d+/\d+) shaded", content)
    if len(fracs) >= 3 and len(set(fracs)) == 1:
        issues.append(f"{title}: all fraction bars use same {fracs[0]!r}")


def unit_tests(issues):
    # regression: irrational
    if pick_diagram("Eighth", "Which is irrational?", 23):
        issues.append("unit: irrational still gets a diagram")
    if pick_scaffold("Eighth", "Which is irrational?", 23, 11):
        issues.append("unit: irrational still gets a scaffold")

    d1 = diagram_for_context("Ratios", "Use a tape diagram for 3:5.", 8, require_tool=True)
    d2 = diagram_for_context("Ratios", "Use a tape diagram for 2:7.", 9, require_tool=True)
    if d1 == d2:
        issues.append("unit: different ratios produced identical diagrams")
    if "3" not in d1 or "5" not in d1:
        issues.append("unit: 3:5 tape missing numbers")
    if "2" not in d2 or "7" not in d2:
        issues.append("unit: 2:7 tape missing numbers")

    f1 = diagram_for_context("Frac", "Shade 2/5 of the bar.", None, require_tool=False)
    f2 = diagram_for_context("Frac", "Shade 3/8 of the bar.", None, require_tool=False)
    if "2/5" not in f1 or "3/8" not in f2:
        issues.append("unit: fraction captions wrong")
    if f1 == f2:
        issues.append("unit: different fractions identical")

    s1 = pick_scaffold("R", "Fill the ratio table for 4:6.", 24, 1)
    s2 = pick_scaffold("R", "Fill the ratio table for 5:8.", 40, 2)
    if not s1 or s1["rows"][0] != [4, 6]:
        issues.append(f"unit: scaffold 4:6 bad: {s1}")
    if not s2 or s2["rows"][0] != [5, 8]:
        issues.append(f"unit: scaffold 5:8 bad: {s2}")

    html = (
        '<div style="background:#f8fafc;border:1px solid #cbd5e1;border-radius:12px;'
        'padding:18px;margin:18px 0;">'
        "<h4>Let's try one together (1)</h4>"
        "<p><strong>Problem:</strong> Find 2/5 of 20 using a fraction bar.</p>"
        "<p><strong>Think it through:</strong></p><ol><li>step</li></ol>"
        "<p><strong>Answer:</strong> 8</p></div>"
    )
    out = polish_content("Fifth Fractions", html)
    if "svg" not in out.lower() and "vl-figure" not in out:
        issues.append("unit: solved example polish did not insert diagram")


def main():
    issues = []
    unit_tests(issues)

    for pkg_name, _ in PACKAGES:
        mod = importlib.import_module(pkg_name)
        units = mod.all_units()
        if len(units) != 8:
            issues.append(f"{pkg_name}: {len(units)} units")
        for title, _d, content, questions in units:
            audit_unit(title, content, questions, issues)

    # Sample DB if password available
    print(f"ISSUES: {len(issues)}")
    for line in issues[:80]:
        print(" -", line)
    if len(issues) > 80:
        print(f" ... and {len(issues) - 80} more")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
