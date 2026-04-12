#!/usr/bin/env python3
"""
Inject 65 supplemental courses: CC+ Grade 1..13 × 5 strands (math, physics, chemistry, bioearth, applied).

- New titles prefixed with "CC+ " so existing "Grade N ..." rows are NOT overwritten (additive).
- Merges PhET URLs from veelearn-frontend/script.js into the injector SIMS table.
- Embeds 3 PhET labs per course (rotated from expanded per-strand lists).
- Adds Wikimedia reference images per strand.
- Quiz questions emphasize on-task checks + solved walkthroughs + sim usage (same hydration as inject_60).

Run (PowerShell example — secrets only in the shell, not in repo files):
  cd <repo>
  $env:MYSQLHOST="your-host"
  $env:MYSQLPASSWORD="your-password"
  $env:MYSQLPORT="26399"   # if needed
  python inject_65_college_supplement.py

Requires: pip install pymysql python-dotenv
"""

from __future__ import annotations

import json
import os
import random
import re
import sys
from pathlib import Path

import pymysql

import inject_60_grade_courses as inj

# inject_60_grade_courses already re-wraps stdout on win32; do not wrap again here.


def load_phet_titles_urls_from_script(script_path: Path) -> dict[str, str]:
    text = script_path.read_text(encoding="utf-8")
    pairs = re.findall(r'\{\s*title:\s*"([^"]+)",\s*url:\s*"([^"]+)"', text)
    return {t: u for t, u in pairs}


def figure_gallery(strand: str, grade: int) -> str:
    """Stable HTTPS images (Wikimedia / NOAA) — educational use."""
    blocks: list[tuple[str, str]] = []
    if strand == "math":
        blocks = [
            (
                "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/US_Navy_number_line.png/640px-US_Navy_number_line.png",
                "Number line model for operations and signed numbers.",
            ),
            (
                "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Pythagorean.svg/480px-Pythagorean.svg.png",
                "Geometric right-triangle relationships (Pythagorean idea).",
            ),
        ]
    elif strand == "physics":
        blocks = [
            (
                "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Free_body.svg/500px-Free_body.svg.png",
                "Free-body style thinking: identify forces before writing equations.",
            ),
            (
                "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Refraction_photo.png/500px-Refraction_photo.png",
                "Refraction connects ray models to observable bending of light.",
            ),
        ]
    elif strand == "chemistry":
        blocks = [
            (
                "https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Water_molecule_3D.svg/400px-Water_molecule_3D.svg.png",
                "Molecular models link particle diagrams to macro properties.",
            ),
            (
                "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Electron_shell_011_Sodium_-_no_label.svg/480px-Electron_shell_011_Sodium_-_no_label.svg.png",
                "Electron-shell diagrams support periodic trends reasoning.",
            ),
        ]
    elif strand == "bioearth":
        blocks = [
            (
                "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Punnett_square.svg/440px-Punnett_square.svg.png",
                "Punnett structure for probability reasoning in genetics tasks.",
            ),
            (
                "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Carbon_cycle-cute_diagram.svg/500px-Carbon_cycle-cute_diagram.svg.png",
                "Systems view: matter and energy through Earth-life cycles.",
            ),
        ]
    else:
        blocks = [
            (
                "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Stemplot_basics.svg/500px-Stemplot_basics.svg.png",
                "Data representation supports decisions under uncertainty.",
            ),
            (
                "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cartesian-coordinate-system.svg/420px-Cartesian-coordinate-system.svg.png",
                "Coordinate models for trends, constraints, and optimization.",
            ),
        ]

    figs = []
    for url, cap in blocks:
        safe = cap.replace('"', "&quot;")
        figs.append(
            f'<figure style="margin:16px 0;text-align:center;">'
            f'<img src="{url}" alt="{safe}" loading="lazy" '
            f'style="max-width:100%;height:auto;border-radius:8px;border:1px solid #dbe5ef;background:#fff;"/>'
            f'<figcaption style="font-size:0.88em;color:#475569;margin-top:8px;">{cap} <em>(Grade {grade})</em></figcaption>'
            f"</figure>"
        )
    return '<h2>Module 3A: Reference Figures (read alongside solved examples)</h2>' + "".join(figs)


def build_content_ccplus(course: dict) -> str:
    base = inj.build_content(course)
    gallery = figure_gallery(course["strand"], course["grade"])
    return base.replace("<h2>Module 3: Drawings and Visual Models</h2>", gallery + "<h2>Module 3: Drawings and Visual Models</h2>", 1)


STRAND_EXTENDED: dict[str, list[str]] = {
    "math": [
        "Arithmetic",
        "Make a Ten",
        "Number Compare",
        "Number Line: Operations",
        "Number Line: Integers",
        "Fractions: Intro",
        "Fraction Matcher",
        "Build a Fraction",
        "Area Model Multiplication",
        "Area Builder",
        "Ratio and Proportion",
        "Unit Rates",
        "Graphing Slope-Intercept",
        "Graphing Lines",
        "Graphing Quadratics",
        "Trig Tour",
        "Function Builder",
        "Expression Exchange",
        "Equality Explorer",
        "Calculus Grapher",
        "Area Model Algebra",
        "Area Model Decimals",
        "Plinko Probability",
        "Curve Fitting",
        "Least-Squares Regression",
        "Mean: Share and Balance",
        "Proportion Playground",
    ],
    "physics": [
        "Forces and Motion: Basics",
        "Balancing Act",
        "Friction",
        "Projectile Motion",
        "Collision Lab",
        "Vector Addition",
        "Energy Skate Park",
        "Energy Skate Park: Basics",
        "Energy Forms and Changes",
        "Gravity Force Lab",
        "Gravity Force Lab: Basics",
        "Gravity and Orbits",
        "Pendulum Lab",
        "Masses and Springs",
        "Wave Interference",
        "Waves Intro",
        "Wave on a String",
        "Sound Waves",
        "Under Pressure",
        "Buoyancy",
        "Buoyancy: Basics",
        "Density",
        "Bending Light",
        "Geometric Optics",
        "Circuit Construction Kit (DC)",
        "Ohm's Law",
        "Charges and Fields",
        "Coulomb's Law",
        "Faraday's Law",
        "Magnets and Electromagnets",
    ],
    "chemistry": [
        "States of Matter: Basics",
        "States of Matter",
        "Gas Properties",
        "Density",
        "Build an Atom",
        "Build a Molecule",
        "Isotopes and Atomic Mass",
        "Atomic Interactions",
        "Molecule Shapes: Basics",
        "Molecule Shapes",
        "Molecule Polarity",
        "Balancing Chemical Equations",
        "Reactants, Products and Leftovers",
        "Concentration",
        "Molarity",
        "pH Scale: Basics",
        "Acid-Base Solutions",
        "Beer's Law Lab",
        "Diffusion",
        "Molecules and Light",
    ],
    "bioearth": [
        "Natural Selection",
        "Greenhouse Effect",
        "Membrane Transport",
        "Neuron",
        "Gene Expression Essentials",
        "Build a Nucleus",
    ],
    "applied": [
        "Center and Variability",
        "Plinko Probability",
        "Curve Fitting",
        "Least-Squares Regression",
        "Function Builder",
        "Unit Rates",
        "Area Builder",
        "Graphing Slope-Intercept",
        "Ratio and Proportion",
        "Equality Explorer",
    ],
}


def filtered_cycle(strand: str) -> list[str]:
    names = STRAND_EXTENDED[strand]
    ok = [n for n in names if n in inj.SIMS]
    if len(ok) >= 3:
        return ok
    return list(inj.SIMS.keys())[:25]


def pick_three_sims(strand: str, grade_index: int) -> list[str]:
    cyc = filtered_cycle(strand)
    n = len(cyc)
    return [cyc[(grade_index * 3 + k) % n] for k in range(3)]


def display_topic_for(strand: str, grade: int) -> str:
    arr = inj.TOPICS[strand]
    idx = min(grade - 1, len(arr) - 1)
    return arr[idx]


def make_blueprints_65() -> list[dict]:
    courses = []
    for grade in range(1, 14):
        gi = grade - 1
        for strand in inj.STRANDS:
            topic = display_topic_for(strand, grade)
            title = f"CC+ Grade {grade} — {strand} — {topic}"
            sims = pick_three_sims(strand, gi)
            courses.append(
                {
                    "grade": grade,
                    "strand": strand,
                    "title": title,
                    "display_topic": topic,
                    "description": (
                        f"College-core pathway supplement for Grade {grade} {strand}: {topic}. "
                        "On-task questions, full solved walkthroughs, three PhET investigations, diagrams, and transfer practice. "
                        "Designed to sit alongside older catalog courses without replacing them."
                    ),
                    "focus_points": list(inj.FOCUS[strand]),
                    "sims": sims,
                }
            )
    return courses


def build_questions_ccplus(course: dict) -> list[dict]:
    """Tighter alignment to course topic, walkthroughs, and embedded sims."""
    grade = course["grade"]
    strand = course["strand"]
    title = course["title"]
    topic = course.get("display_topic") or inj.course_topic(course)
    focus = course["focus_points"]
    alignment = inj.derive_alignment(course)
    scope = alignment["scope"]
    seed = sum(ord(ch) for ch in title) + grade * 131 + len(topic) * 17
    rr = random.Random(seed)

    out: list[dict] = []

    def add(text, correct, wrongs, explanation, idx=None):
        out.append(
            inj.make_question(
                text,
                correct,
                wrongs,
                explanation,
                idx if idx is not None else len(out) + 1,
            )
        )

    add(
        f"({topic}) Which goal is most on-task for this module?",
        scope[0],
        [scope[1] if len(scope) > 1 else "Unrelated memorization", "Skipping definitions", "Random advanced topic"],
        "Stay aligned with the stated title scope before extending.",
    )
    add(
        f"({topic}) Which practice best shows '{focus[0]}'?",
        "Explain reasoning with a representation (diagram, table, or model) before compressing to symbols.",
        ["Give only a final answer with no steps", "Copy a template without fitting the context", "Avoid assumptions entirely"],
        "Mastery includes visible reasoning and fit-for-purpose models.",
    )

    solved = inj.solved_problem_bank(course) or inj.generic_solved_bank(course)
    w1, w2, w3 = solved[0], solved[1], solved[2]
    add(
        f"In '{topic}', Solved Walkthrough 1 ends with which final result?",
        str(w1["answer"]),
        [str(w2["answer"]), str(w3["answer"]), "The walkthrough has no conclusion"],
        "Students should retrace the full solution path, not only read headings.",
    )
    add(
        f"In '{topic}', which first step appears in Solved Walkthrough 2?",
        w2["steps"][0],
        [w1["steps"][0], w3["steps"][0], "Guess and check without justification"],
        "Reading solved work means identifying the logical entry move.",
    )
    add(
        f"({topic}) Why do we include three PhET labs in this course?",
        "To collect interactive evidence that supports or revises your mental model",
        ["To replace all written work", "Because screenshots count as proof with no interpretation", "To avoid doing calculations"],
        "Simulations are tools for evidence, not substitutes for reasoning.",
    )

    # Strand-specific computations (same spirit as inject_60 but tied to topic label)
    if strand == "math":
        if grade <= 4:
            a = rr.randint(12 + grade, 28 + grade)
            b = rr.randint(9 + grade, 22 + grade)
            add(f"({topic}) Compute {a} + {b}.", str(a + b), [str(a + b + 2), str(max(a + b - 3, 0)), str(a + b + 5)], "Decompose, add, then verify with inverse operation.")
        elif grade <= 8:
            x = rr.randint(3, 9)
            rhs = rr.randint(24, 55)
            c = rr.randint(5, 17)
            sol = (rhs - c) / x
            ca = f"x = {sol:.2f}" if sol % 1 else f"x = {int(sol)}"
            add(f"({topic}) Solve {x}x + {c} = {rhs}.", ca, [f"x = {sol + 1:.2f}", f"x = {max(sol - 1, 0):.2f}", "x = 0"], "Isolate x with inverse operations; substitute back.")
        else:
            m, b0 = rr.randint(2, 7), rr.randint(-4, 9)
            xv = rr.randint(2, 8)
            add(
                f"({topic}) For y = {m}x + ({b0}), find y when x = {xv}.",
                str(m * xv + b0),
                [str(m * xv + b0 + 3), str(m * xv + b0 - 4), str(m + xv + b0)],
                "Substitute, multiply, then add the constant term.",
            )
    elif strand == "physics":
        m = rr.randint(grade + 1, grade + 6)
        force = rr.randint(20 + grade, 50 + grade * 2)
        v = rr.randint(grade + 2, grade + 9)
        add(
            f"({topic}) F = {force} N, m = {m} kg. Acceleration?",
            f"{force / m:.2f} m/s^2",
            [f"{m / force:.2f} m/s^2", f"{force + m:.2f} m/s^2", f"{force - m:.2f} m/s^2"],
            "Use a = F/m with consistent SI units.",
        )
        add(
            f"({topic}) KE for m={m} kg, v={v} m/s?",
            f"{0.5 * m * v * v:.2f} J",
            [f"{m * v:.2f} J", f"{m * v * v:.2f} J", f"{0.5 * m * v:.2f} J"],
            "Kinetic energy uses 1/2 mv^2.",
        )
    elif strand == "chemistry":
        moles = rr.uniform(0.6, 2.4)
        vol = rr.uniform(0.5, 2.0)
        add(
            f"({topic}) Molarity when n={moles:.2f} mol and V={vol:.2f} L?",
            f"{moles / vol:.2f} M",
            [f"{moles * vol:.2f} M", f"{vol / moles:.2f} M", f"{moles + vol:.2f} M"],
            "M = n/V.",
        )
        add(
            f"({topic}) Why balance a reaction before yield calculations?",
            "Atom counts (and charge in ionic redox) must be conserved.",
            ["To make coefficients larger", "To remove energy tracking", "It is optional for gases"],
            "Stoichiometry rests on conservation.",
        )
    elif strand == "bioearth":
        start = rr.randint(50 + grade * 4, 120 + grade * 6)
        r_pct = rr.choice([8, 10, 12, 15])
        next_pop = round(start * (1 + r_pct / 100))
        add(
            f"({topic}) Population {start} grows {r_pct}% one year. Best estimate?",
            str(next_pop),
            [str(start + r_pct), str(start - r_pct), str(start + 2 * r_pct)],
            "Percent growth multiplies by (1 + r).",
        )
        add(
            f"({topic}) Bb × Bb cross — probability of homozygous recessive (bb)?",
            "25%",
            ["50%", "75%", "100%"],
            "Standard monohybrid Punnett square: 1/4 bb.",
        )
    else:
        vals = [rr.randint(10, 35) for _ in range(6)]
        mean = sum(vals) / len(vals)
        add(
            f"({topic}) Mean of {vals}?",
            f"{mean:.2f}",
            [f"{mean + 1.5:.2f}", f"{max(mean - 2, 0):.2f}", str(sum(vals))],
            "Mean = sum/count.",
        )
        budget, cost = rr.randint(180, 360), rr.randint(12, 28)
        add(
            f"({topic}) Budget ${budget}, item ${cost}. Max whole items?",
            str(budget // cost),
            [str(budget // cost + 2), "1", str(int(budget / cost))],
            "Integer constraints require floor division when items are whole.",
        )

    sim_a, sim_b, sim_c = course["sims"]
    add(
        f"({topic}) Which three sims are embedded in this course?",
        f"{sim_a}; {sim_b}; {sim_c}",
        [f"{sim_a}; {sim_b}; Arithmetic", f"{sim_a} only", "No sims are listed"],
        "Cross-check Module 5 against your notes.",
    )
    add(
        f"({topic}) In a CER paragraph after a lab, 'Evidence' should be:",
        "Measured/observed data tied to the procedure",
        ["Your claim restated", "A definition from the glossary", "A guess without trials"],
        "Evidence must be concrete and linked to how it was produced.",
    )
    add(
        f"({topic}) Before submitting, what should you verify on every symbolic result?",
        "Units, domain/restrictions, and reasonableness in context",
        ["Only font size", "Whether the answer is an integer", "Nothing if the calculator agrees"],
        "Sanity checks catch model mismatches.",
    )
    add(
        f"In '{topic}', Solved Walkthrough 3 final answer:",
        str(w3["answer"]),
        [str(w1["answer"]), str(w2["answer"]), "Not stated"],
        "Locates attention on the third full solution.",
    )

    # renumber order_index
    for i, q in enumerate(out, 1):
        q["order_index"] = i
    return out


def upsert_cc_course(cursor, course, creator_id, rng):
    title = course["title"]
    grade = course["grade"]
    content = build_content_ccplus(course)
    questions = build_questions_ccplus(course)

    cursor.execute(
        "SELECT id FROM courses WHERE title=%s AND grade_level=%s ORDER BY id ASC LIMIT 1",
        (title, grade),
    )
    row = cursor.fetchone()
    if row:
        course_id = row["id"]
        cursor.execute(
            "UPDATE courses SET description=%s, content=%s, status='approved' WHERE id=%s",
            (course["description"], content, course_id),
        )
        action = "updated"
    else:
        cursor.execute(
            """
            INSERT INTO courses (title, description, content, creator_id, status, grade_level)
            VALUES (%s, %s, %s, %s, 'approved', %s)
            """,
            (title, course["description"], content, creator_id, grade),
        )
        cursor.execute("SELECT LAST_INSERT_ID() AS id")
        course_id = cursor.fetchone()["id"]
        action = "inserted"

    cursor.execute("DELETE FROM course_questions WHERE course_id=%s", (course_id,))
    qids = []
    for raw_q in questions:
        q = inj.shuffle_options(raw_q, rng)
        cursor.execute(
            """
            INSERT INTO course_questions
            (course_id, question_text, question_type, options, correct_answer, explanation, points, order_index)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                course_id,
                q["question_text"],
                q["question_type"],
                json.dumps(q["options"]),
                q["correct_answer"],
                q["explanation"],
                q["points"],
                q["order_index"],
            ),
        )
        cursor.execute("SELECT LAST_INSERT_ID() AS id")
        qids.append(cursor.fetchone()["id"])

    hydrated = content + "".join(
        [inj.placeholder_html(qid, idx) for idx, qid in enumerate(qids, 1)]
    )
    cursor.execute("UPDATE courses SET content=%s, status='approved' WHERE id=%s", (hydrated, course_id))
    return {"id": course_id, "grade": grade, "title": title, "questions": len(qids), "action": action}


def main() -> int:
    script_js = Path(__file__).resolve().parent / "veelearn-frontend" / "script.js"
    if script_js.is_file():
        extra = load_phet_titles_urls_from_script(script_js)
        before = len(inj.SIMS)
        inj.SIMS.update(extra)
        print(f"Merged PhET map: +{len(inj.SIMS) - before} new entries from script.js (total {len(inj.SIMS)}).")
    else:
        print("WARN: script.js not found — using injector SIMS only.")

    cfg = inj.AIVEN_CONFIG
    if not cfg.get("password"):
        print("ERROR: Set MYSQLPASSWORD or AIVEN_PASSWORD in your environment.")
        return 1

    courses = make_blueprints_65()
    if len(courses) != 65:
        print(f"ERROR: expected 65 courses, got {len(courses)}")
        return 1

    rng = random.Random(int(os.getenv("COURSE_RANDOM_SEED", "20260404")))

    print("Connecting to MySQL...")
    try:
        conn = pymysql.connect(**cfg)
    except Exception as exc:
        print(f"Connection failed: {exc}")
        return 1

    processed = []
    try:
        cursor = conn.cursor()
        creator_id = inj.resolve_creator_id(cursor)
        print(f"Using creator_id: {creator_id}")

        for i, course in enumerate(courses, 1):
            result = upsert_cc_course(cursor, course, creator_id, rng)
            processed.append(result)
            print(
                f"[{i:02d}/65] G{result['grade']:02d} | {result['action'].upper()} | ID {result['id']} | Q {result['questions']}"
            )
        conn.commit()

        ids = [x["id"] for x in processed]
        rows = inj.verify(cursor, ids)
        by_grade: dict[int, dict] = {}
        for row in rows:
            g = int(row["grade_level"])
            by_grade.setdefault(g, {"courses": 0, "questions": 0, "placeholders": 0})
            by_grade[g]["courses"] += 1
            by_grade[g]["questions"] += int(row["q_count"])
            by_grade[g]["placeholders"] += int(row["p_count"])

        print("\n=== CC+ 65 COMPLETE ===")
        for g in range(1, 14):
            st = by_grade.get(g, {"courses": 0, "questions": 0, "placeholders": 0})
            print(f"Grade {g:02d}: courses={st['courses']} Q={st['questions']} placeholders={st['placeholders']}")

        ok = all(by_grade.get(g, {}).get("courses") == 5 for g in range(1, 14))
        hyd = all(
            by_grade.get(g, {}).get("questions") == by_grade.get(g, {}).get("placeholders")
            for g in range(1, 14)
        )
        print("Per-grade 5 courses:", "OK" if ok else "MISMATCH")
        print("Placeholder vs question count:", "OK" if hyd else "CHECK")
    except Exception as exc:
        try:
            conn.rollback()
        except Exception:
            pass
        print(f"ERROR: {exc}")
        import traceback

        traceback.print_exc()
        return 1
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
