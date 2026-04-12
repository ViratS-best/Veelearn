#!/usr/bin/env python3
"""
Inject 65 university-tier courses (UNIV 2026 — …) on top of existing DB rows.

- Idempotent by (title, grade_level=13); does not delete CC+ or Grade N courses.
- Merges PhET URLs from veelearn-frontend/script.js into inject_60_grade_courses.SIMS.
- Full HTML from univ_65_render + 12 MCQs + quiz placeholders (same hydration as inject_60).

Run (secrets only in environment):
  $env:MYSQLHOST="..."
  $env:MYSQLPASSWORD="..."
  python inject_univ_65.py

Requires: pymysql, python-dotenv (optional)
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
import univ_65_snippets as snip
import univ_65_render as rnd
from univ_65_definitions import UNIV_MODULES, full_title, validate_count

# UTF-8 stdout on Windows is applied by inject_60_grade_courses (do not wrap twice).


def load_phet_titles_urls_from_script(script_path: Path) -> dict[str, str]:
    text = script_path.read_text(encoding="utf-8")
    pairs = re.findall(r'\{\s*title:\s*"([^"]+)",\s*url:\s*"([^"]+)"', text)
    return {t: u for t, u in pairs}


def merged_sims_map(repo_root: Path) -> dict[str, str]:
    m = dict(inj.SIMS)
    script = repo_root / "veelearn-frontend" / "script.js"
    if not script.is_file():
        raise FileNotFoundError(f"Missing {script}")
    m.update(load_phet_titles_urls_from_script(script))
    return m


def validate_phet_trios(sims: dict[str, str]) -> None:
    missing: list[str] = []
    for strand in ("math", "physics", "chemistry", "biology", "computing"):
        for i in range(13):
            for name in snip.phet_trio(strand, i):
                if name not in sims:
                    missing.append(f"{strand}[{i}]: {name!r}")
    if missing:
        raise SystemExit("PhET title(s) not in merged SIMS map:\n" + "\n".join(missing))


def upsert_univ_course(cursor, title: str, description: str, content: str, questions: list, creator_id, rng):
    grade = 13
    cursor.execute(
        "SELECT id FROM courses WHERE title=%s AND grade_level=%s ORDER BY id ASC LIMIT 1",
        (title, grade),
    )
    row = cursor.fetchone()
    if row:
        course_id = row["id"]
        cursor.execute(
            "UPDATE courses SET description=%s, content=%s, status='approved' WHERE id=%s",
            (description, content, course_id),
        )
        action = "updated"
    else:
        cursor.execute(
            """
            INSERT INTO courses (title, description, content, creator_id, status, grade_level)
            VALUES (%s, %s, %s, %s, 'approved', %s)
            """,
            (title, description, content, creator_id, grade),
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
    validate_count()
    if not inj.AIVEN_CONFIG["password"]:
        print("ERROR: Set MYSQLPASSWORD or AIVEN_PASSWORD before running.")
        return 1

    repo = Path(__file__).resolve().parent
    sims = merged_sims_map(repo)
    validate_phet_trios(sims)

    rng = random.Random(inj.getenv_int("COURSE_RANDOM_SEED", 20260404))

    from collections import defaultdict

    strand_i: defaultdict[str, int] = defaultdict(int)
    results = []

    conn = pymysql.connect(**inj.AIVEN_CONFIG)
    try:
        with conn.cursor() as cursor:
            creator_id = inj.resolve_creator_id(cursor)
            if not creator_id:
                print("ERROR: No user row for creator fallback.")
                return 1

            for strand, short in UNIV_MODULES:
                mi = strand_i[strand]
                strand_i[strand] += 1
                title = full_title(strand, short)
                S = snip.snippet(strand, mi)
                trio = snip.phet_trio(strand, mi)
                desc = (
                    f"University-level module: {short}. "
                    f"{S['overview'][:380]}{'…' if len(S['overview']) > 380 else ''}"
                )
                body = rnd.build_html(strand, short, mi, sims)
                qs = rnd.build_quizzes(strand, mi, short, trio)
                meta = upsert_univ_course(cursor, title, desc, body, qs, creator_id, rng)
                results.append(meta)
                print(f"{meta['action']:8} | {title[:72]}… | Q={meta['questions']}")

        conn.commit()
    finally:
        conn.close()

    ids = [r["id"] for r in results]
    conn = pymysql.connect(**inj.AIVEN_CONFIG)
    try:
        with conn.cursor() as cursor:
            rows = inj.verify(cursor, ids)
    finally:
        conn.close()

    ok = all(int(row["q_count"]) == int(row["p_count"]) for row in rows)
    print(f"\nDone. Courses={len(results)}. Placeholder hydration OK: {ok}")
    if not ok:
        for row in rows:
            print(row)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
