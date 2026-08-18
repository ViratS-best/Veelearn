#!/usr/bin/env python3
"""Inject deep Algebra 2 (grade 10) master + 8 units into Aiven.

Each unit: 6 deep concepts with 5 practice quizzes after each, plus 25 finale problems
(Easy → Stretch / honors / SAT). Upserts by (title, grade_level) — no duplicates.
Secrets via env only.
"""

from __future__ import annotations

import io
import json
import os
import random
import re
import ssl
import sys

import pymysql

try:
    from dotenv import load_dotenv
    load_dotenv()
    load_dotenv(os.path.join(os.path.dirname(__file__), "veelearn-backend", ".env"))
except Exception:
    pass

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from apchem_curriculum import all_units, build_master

GRADE = 11
MASTER_TITLE = 'AP Chemistry Complete'
RNG_SEED = 20260836
EXPECTED_Q = 55  # 6*5 concept drills + 25 finale


def getenv_int(name, default):
    value = os.getenv(name)
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


AIVEN_CONFIG = {
    "charset": "utf8mb4",
    "connect_timeout": getenv_int("MYSQL_CONNECT_TIMEOUT", 60),
    "cursorclass": pymysql.cursors.DictCursor,
    "db": os.getenv("MYSQL_DATABASE") or os.getenv("AIVEN_DB", "defaultdb"),
    "host": os.getenv("MYSQLHOST") or os.getenv("AIVEN_HOST", "veelearndb-asterloop-483e.i.aivencloud.com"),
    "password": os.getenv("MYSQLPASSWORD") or os.getenv("AIVEN_PASSWORD", ""),
    "port": getenv_int("MYSQLPORT", getenv_int("AIVEN_PORT", 26399)),
    "user": os.getenv("MYSQLUSER") or os.getenv("AIVEN_USER", "avnadmin"),
    "read_timeout": getenv_int("MYSQL_READ_TIMEOUT", 300),
    "write_timeout": getenv_int("MYSQL_WRITE_TIMEOUT", 300),
}

_ca_path = None
ssl_ca = os.getenv("DB_SSL_CA")
if ssl_ca:
    _ca_path = os.path.join(os.getcwd(), "ca.pem")
    with open(_ca_path, "w", encoding="utf-8") as f:
        f.write(ssl_ca.replace("\\n", "\n"))
    AIVEN_CONFIG["ssl"] = {"ca": _ca_path}
else:
    _ssl_ctx = ssl.create_default_context()
    _ssl_ctx.check_hostname = False
    _ssl_ctx.verify_mode = ssl.CERT_NONE
    AIVEN_CONFIG["ssl"] = _ssl_ctx


def shuffle_options(question, rng):
    q = dict(question)
    options = list(q["options"])
    rng.shuffle(options)
    if q["correct_answer"] not in options:
        options[0] = q["correct_answer"]
        rng.shuffle(options)
    q["options"] = options
    return q


def placeholder_html(question_id, idx):
    return (
        f'<div class="quiz-question-placeholder" data-question-id="{question_id}" '
        f'style="background:#e0e7ff;border:2px solid #667eea;padding:1.5em;margin:1.5em 0;'
        f'border-radius:8px;user-select:none;"><strong>Quiz Question {idx}</strong></div>'
    )


def fill_quiz_slots(content, placeholders):
    slots = sorted(int(m) for m in re.findall(r"<!--QUIZ_SLOT_(\d+)-->", content))
    used = 0
    for slot_n in slots:
        if used >= len(placeholders):
            content = content.replace(f"<!--QUIZ_SLOT_{slot_n}-->", "", 1)
            continue
        content = content.replace(f"<!--QUIZ_SLOT_{slot_n}-->", placeholders[used], 1)
        used += 1
    leftover = "".join(placeholders[used:])
    if leftover:
        content += "<h2>Additional Practice</h2>" + leftover
    return content


def resolve_creator_id(cursor):
    preferred = os.getenv("COURSE_CREATOR_ID")
    if preferred and preferred.isdigit():
        cursor.execute("SELECT id FROM users WHERE id=%s LIMIT 1", (int(preferred),))
        row = cursor.fetchone()
        if row:
            return row["id"]
    cursor.execute(
        "SELECT id FROM users WHERE role IN ('superadmin','admin') ORDER BY id ASC LIMIT 1"
    )
    row = cursor.fetchone()
    if row:
        return row["id"]
    cursor.execute("SELECT id FROM users ORDER BY id ASC LIMIT 1")
    row = cursor.fetchone()
    return row["id"] if row else None


def upsert_unit(cursor, title, description, content, questions, creator_id, rng):
    cursor.execute(
        "SELECT id FROM courses WHERE title=%s AND grade_level=%s ORDER BY id ASC LIMIT 1",
        (title, GRADE),
    )
    row = cursor.fetchone()
    if row:
        course_id = row["id"]
        cursor.execute(
            "UPDATE courses SET description=%s, content=%s, status='approved', course_type='single' WHERE id=%s",
            (description, content, course_id),
        )
        action = "updated"
    else:
        cursor.execute(
            """
            INSERT INTO courses (title, description, content, creator_id, status, grade_level, course_type)
            VALUES (%s, %s, %s, %s, 'approved', %s, 'single')
            """,
            (title, description, content, creator_id, GRADE),
        )
        cursor.execute("SELECT LAST_INSERT_ID() AS id")
        course_id = cursor.fetchone()["id"]
        action = "inserted"

    cursor.execute("DELETE FROM course_questions WHERE course_id=%s", (course_id,))
    qids = []
    for raw_q in questions:
        q = shuffle_options(raw_q, rng)
        cursor.execute(
            """
            INSERT INTO course_questions
            (course_id, question_text, question_type, options, correct_answer, explanation, points, order_index, difficulty)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                q.get("difficulty"),
            ),
        )
        cursor.execute("SELECT LAST_INSERT_ID() AS id")
        qids.append(cursor.fetchone()["id"])

    placeholders = [placeholder_html(qid, i) for i, qid in enumerate(qids, 1)]
    hydrated = fill_quiz_slots(content, placeholders)
    cursor.execute("UPDATE courses SET content=%s, status='approved' WHERE id=%s", (hydrated, course_id))
    return {"id": course_id, "title": title, "questions": len(qids), "action": action}


def upsert_master(cursor, creator_id):
    desc = (
        "Deep AP Chemistry master course: eight units with long explanations, "
        "quizzes after every concept, and 25 progressive finale problems per unit "
        "(Easy through honors/SAT stretch)."
    )
    content = build_master()
    cursor.execute(
        "SELECT id FROM courses WHERE title=%s AND grade_level=%s ORDER BY id ASC LIMIT 1",
        (MASTER_TITLE, GRADE),
    )
    row = cursor.fetchone()
    if row:
        master_id = row["id"]
        cursor.execute(
            """
            UPDATE courses SET description=%s, content=%s, status='approved', course_type='master'
            WHERE id=%s
            """,
            (desc, content, master_id),
        )
        action = "updated"
    else:
        cursor.execute(
            """
            INSERT INTO courses (title, description, content, creator_id, status, grade_level, course_type)
            VALUES (%s, %s, %s, %s, 'approved', %s, 'master')
            """,
            (MASTER_TITLE, desc, content, creator_id, GRADE),
        )
        cursor.execute("SELECT LAST_INSERT_ID() AS id")
        master_id = cursor.fetchone()["id"]
        action = "inserted"
    return master_id, action


def link_units(cursor, master_id, unit_ids):
    cursor.execute("DELETE FROM course_units WHERE parent_course_id=%s", (master_id,))
    for order, child_id in enumerate(unit_ids):
        cursor.execute(
            """
            INSERT INTO course_units
            (parent_course_id, child_course_id, order_index, is_draft, prerequisite_unit_id, linked_course_id)
            VALUES (%s, %s, %s, FALSE, NULL, %s)
            """,
            (master_id, child_id, order, child_id),
        )


def verify(cursor, ids):
    rows = []
    for cid in ids:
        cursor.execute(
            """
            SELECT c.id, c.title, c.course_type, c.status,
                   (SELECT COUNT(*) FROM course_questions q WHERE q.course_id = c.id) AS q_count,
                   (LENGTH(c.content) - LENGTH(REPLACE(c.content, 'quiz-question-placeholder', '')))
                     / LENGTH('quiz-question-placeholder') AS p_count
            FROM courses c
            WHERE c.id = %s
            """,
            (cid,),
        )
        rows.append(cursor.fetchone())
    return rows


def dry_check():
    bad = re.compile(r"\b(wait|recalculate)\b", re.I)
    units = all_units()
    assert len(units) == 8
    total_lines_est = 0
    for title, _d, content, questions in units:
        assert len(questions) == EXPECTED_Q, f"{title}: {len(questions)} != {EXPECTED_Q}"
        slots = len(re.findall(r"<!--QUIZ_SLOT_\d+-->", content))
        assert slots == EXPECTED_Q, f"{title}: slots {slots} != {EXPECTED_Q}"
        assert len(content) > 8000, f"{title}: content too short ({len(content)} chars)"
        if bad.search(content):
            raise AssertionError(f"{title}: banned phrasing in content")
        for q in questions:
            assert q["correct_answer"] in q["options"], f"{title}: {q['correct_answer']} not in options"
            if bad.search(q["explanation"] or ""):
                raise AssertionError(f"{title}: banned phrasing in explanation")
        total_lines_est += content.count("\n")
    print(f"DRY_CHECK OK: 8 units × {EXPECTED_Q} questions; teaching HTML ~{total_lines_est} lines worth of breaks.")


def main():
    if not AIVEN_CONFIG["password"]:
        print("ERROR: Set AIVEN_PASSWORD (or MYSQLPASSWORD).")
        return 1
    rng = random.Random(RNG_SEED)
    print("Connecting...")
    conn = pymysql.connect(**AIVEN_CONFIG)
    try:
        cursor = conn.cursor()
        creator_id = resolve_creator_id(cursor)
        print(f"creator_id={creator_id}")
        unit_results = []
        for i, (title, desc, content, questions) in enumerate(all_units(), 1):
            result = upsert_unit(cursor, title, desc, content, questions, creator_id, rng)
            unit_results.append(result)
            print(f"[Unit {i}/8] {result['action'].upper()} ID {result['id']} Q {result['questions']} | {result['title']}")
        master_id, master_action = upsert_master(cursor, creator_id)
        link_units(cursor, master_id, [u["id"] for u in unit_results])
        print(f"[Master] {master_action.upper()} ID {master_id}")
        conn.commit()
        ok = True
        for row in verify(cursor, [u["id"] for u in unit_results] + [master_id]):
            q, pcount = int(row["q_count"]), int(row["p_count"] or 0)
            ctype = row.get("course_type") or "single"
            if ctype == "master":
                match = "OK" if q == 0 else "MISMATCH"
            elif q != pcount or q != EXPECTED_Q:
                match = "MISMATCH"
                ok = False
            else:
                match = "OK"
            if match != "OK":
                ok = False
            print(f"  verify id={row['id']} type={ctype} q={q} placeholders={pcount} → {match}")
        cursor.execute("SELECT COUNT(*) AS n FROM course_units WHERE parent_course_id=%s", (master_id,))
        nlink = cursor.fetchone()["n"]
        print(f"  course_units linked: {nlink}")
        if nlink != 8:
            ok = False
        print("SUCCESS" if ok else "WARNING: mismatches")
        return 0 if ok else 2
    finally:
        conn.close()
        if _ca_path and os.path.isfile(_ca_path):
            try:
                os.remove(_ca_path)
            except OSError:
                pass


if __name__ == "__main__":
    if os.getenv("DRY_CHECK") == "1":
        dry_check()
        sys.exit(0)
    sys.exit(main())
