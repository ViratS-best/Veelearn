"""Full API smoke test against the PostgreSQL-backed backend.

Creates throwaway users/courses/classes, exercises the route surface, then deletes
everything it created (tracked by id). Run with the server on PORT (default 5055):

    python api_smoke.py
    python api_smoke.py --cleanup-only
"""
from __future__ import annotations

import json
import os
import sys
import time
import uuid

import psycopg2
import requests

sys.stdout.reconfigure(errors="replace")

BASE = os.environ.get("SMOKE_BASE", "http://127.0.0.1:5055")
TAG = uuid.uuid4().hex[:8].upper()
PW = "Passw0rd123"

created = {
    "users": [],
    "courses": [],
    "simulators": [],
    "classes": [],
    "schools": [],
    "assignments": [],
    "questions": [],
    "units": [],
}
tokens = {}
failures: list[str] = []
checks = {"pass": 0, "fail": 0}


def db():
    return psycopg2.connect(
        host=os.environ["PGHOST"],
        port=int(os.environ["PGPORT"]),
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
        dbname=os.environ.get("PG_DATABASE", "defaultdb"),
        sslmode="require",
    )


def call(method: str, path: str, who: str | None = None, body=None, expect=(200, 201), allow_all=False):
    headers = {}
    if who and who in tokens:
        headers["Authorization"] = f"Bearer {tokens[who]}"
    if who == "cookie":
        headers["Cookie"] = f"token={tokens.get('student_cookie', '')}"
    try:
        r = requests.request(method, BASE + path, json=body, headers=headers, timeout=45)
    except Exception as exc:  # noqa: BLE001
        checks["fail"] += 1
        failures.append(f"{method} {path} -> EXCEPTION {exc}")
        return None, 0
    ok = r.status_code in expect or (allow_all and r.status_code < 500)
    checks["pass" if ok else "fail"] += 1
    label = "PASS" if ok else "FAIL"
    print(f"{label} {method:6s} {path:58s} {r.status_code}")
    if not ok:
        body_txt = r.text[:220].replace("\n", " ")
        failures.append(f"{method} {path} -> {r.status_code} {body_txt}")
    try:
        return r, r.status_code
    except Exception:  # noqa: BLE001
        return None, r.status_code


def login(email: str, key: str):
    r = requests.post(f"{BASE}/api/login", json={"email": email, "password": PW}, timeout=30)
    if r.status_code == 200 and r.json().get("success"):
        tokens[key] = r.json()["data"]["token"]
        return True
    print("LOGIN FAILED", email, r.status_code, r.text[:160])
    return False


def register(key: str, role_patch: dict | None = None, path="/api/register", extra=None):
    email = f"smoke_{key}_{TAG.lower()}@example.com"
    body = {"email": email, "password": PW}
    if extra:
        body.update(extra)
    r = requests.post(BASE + path, json=body, timeout=30)
    if r.status_code not in (200, 201):
        print(f"REGISTER {key}: {r.status_code} {r.text[:180]}")
        return None
    data = r.json().get("data") or {}
    uid = (data.get("user") or {}).get("id")
    if not uid:
        print("REGISTER no id", key)
        return None
    created["users"].append(uid)
    if data.get("token"):
        tokens[key] = data["token"]
    if role_patch:
        conn = db()
        with conn.cursor() as cur:
            sets = ", ".join(f"{k}=%s" for k in role_patch)
            cur.execute(f"UPDATE users SET {sets} WHERE id=%s", (*role_patch.values(), uid))
            if "school_name" in (extra or {}):
                pass
        conn.commit()
        conn.close()
    return uid


def setup_users():
    student = register("student", {"role": "student"})
    teacher = register("teacher", {"role": "teacher", "teacher_approved": 1, "class_code": f"T{TAG[:4]}"})
    parent = register("parent", {"role": "parent"})
    admin = register("admin", {"role": "superadmin", "is_admin_approved": 1, "is_approved": 1})
    promo = register("promo", {"role": "user"})
    sa = register("schooladmin", {"role": "school_admin"},
                  path="/api/register/school-admin",
                  extra={"name": "Smoke School", "school_name": f"Smoke High {TAG}"})
    # Roles were patched in the DB after the JWT was issued, so log in again to
    # pick up the new role claims before exercising admin-only routes.
    for key in ("student", "teacher", "parent", "admin", "schooladmin", "promo"):
        email = f"smoke_{key}_{TAG.lower()}@example.com"
        login(email, key)
    return {"student": student, "teacher": teacher, "parent": parent, "admin": admin, "schooladmin": sa, "promo": promo}


def get_school_id():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT school_id FROM users WHERE id=%s", (created["users"][-1],))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def main() -> int:
    print(f"== smoke run {TAG} ==")
    ids = setup_users()
    print("users:", ids)
    if not all([ids["student"], ids["teacher"], ids["admin"]]):
        print("setup failed, aborting")
        return 2
    tokens.setdefault("cookie", tokens.get("student", ""))
    tokens["student_cookie"] = tokens.get("student", "")
    school_id = get_school_id()

    # --- teacher promotion flow -------------------------------------------------
    call("POST", "/api/user/become-teacher", "promo", {}, allow_all=True)
    call("PUT", f"/api/admin/approve-teacher/{ids['promo']}", "admin", {}, allow_all=True)
    call("GET", "/api/users/pending-teachers", "admin", allow_all=True)

    # --- course lifecycle -------------------------------------------------------
    r, _ = call("POST", "/api/courses", "teacher", {
        "title": f"Smoke Course {TAG}", "description": "temp", "content": "<h3>Hello</h3><p>Body $x^2$</p>",
        "status": "pending", "grade_level": 9,
    }, expect=(200, 201))
    course_id = (r.json().get("data") or {}).get("id") if r is not None else None
    if course_id:
        created["courses"].append(course_id)
    print("course:", course_id)

    call("GET", "/api/my-courses", "teacher")
    if course_id:
        call("GET", f"/api/courses/{course_id}", "teacher")
        call("PUT", f"/api/courses/{course_id}", "teacher", {"title": f"Smoke Course {TAG} v2", "content": "<p>v2</p>"}, allow_all=True)
        call("GET", "/api/admin/courses/pending", "admin")
        call("GET", f"/api/admin/courses/{course_id}/preview", "admin")
        call("PUT", f"/api/admin/courses/{course_id}/status", "admin", {"status": "approved"}, allow_all=True)
        call("PUT", f"/api/courses/{course_id}/type", "teacher", {"course_type": "single"}, allow_all=True)
        call("PUT", f"/api/courses/{course_id}/resubmit", "teacher", {}, allow_all=True)
        call("GET", f"/api/courses/{course_id}/type", "teacher")

        # quiz question CRUD
        q, _ = call("POST", f"/api/courses/{course_id}/questions", "teacher", {
            "question_text": "What is 2+2?", "question_type": "multiple_choice",
            "options": ["3", "4", "5"], "correct_answer": "4", "points": 1, "order_index": 0,
        }, allow_all=True)
        qid = ((q.json().get("data") or {}) if q is not None else {}).get("id")
        if qid:
            created["questions"].append(qid)
        print("question:", qid)
        call("GET", f"/api/courses/{course_id}/questions", "teacher")
        if qid:
            call("PUT", f"/api/courses/{course_id}/questions/{qid}", "teacher", {"question_text": "What is 2+2?", "correct_answer": "4"}, allow_all=True)
            call("GET", f"/api/courses/{course_id}/questions/{qid}/attempts", "student", allow_all=True)

        # units
        r2, _ = call("POST", "/api/courses", "teacher", {"title": f"Smoke Child {TAG}", "status": "approved", "content": "<p>c</p>"}, allow_all=True)
        child_id = ((r2.json().get("data") or {}) if r2 is not None else {}).get("id")
        if child_id:
            created["courses"].append(child_id)
            u, _ = call("POST", f"/api/courses/{course_id}/units", "teacher", {"child_course_id": child_id, "order_index": 0}, allow_all=True)
            uid = ((u.json().get("data") or {}) if u is not None else {}).get("id")
            if uid:
                created["units"].append(uid)
            print("unit:", uid)
            call("GET", f"/api/courses/{course_id}/units", "teacher")
            if uid:
                call("PUT", f"/api/courses/units/{uid}", "teacher", {"order_index": 1}, allow_all=True)
                call("PUT", f"/api/courses/{course_id}/units/reorder", "teacher", {"unit_ids": [uid]}, allow_all=True)
                call("PUT", f"/api/courses/units/{uid}/progress", "student", {"completed": True}, allow_all=True)
                call("POST", f"/api/courses/units/{uid}/complete", "student", {"completed": True}, allow_all=True)
        call("GET", "/api/courses/available-for-units", "teacher")

        # likes / progress / enroll
        call("POST", f"/api/courses/{course_id}/like", "student", {}, allow_all=True)
        call("GET", f"/api/courses/{course_id}/like", "student", allow_all=True)
        call("GET", f"/api/courses/{course_id}/likes", "student", allow_all=True)
        call("DELETE", f"/api/courses/{course_id}/like", "student", allow_all=True)
        call("POST", f"/api/courses/{course_id}/enroll", "student", {}, allow_all=True)
        call("GET", f"/api/courses/{course_id}/progress", "student", allow_all=True)
        call("PUT", f"/api/courses/{course_id}/progress", "student", {"progress_percentage": 25, "last_page_index": 1}, allow_all=True)
        call("GET", f"/api/users/enrollments/{course_id}/progress", "student", allow_all=True)
        call("GET", "/api/student/enrolled-courses", "student", allow_all=True)
        call("POST", f"/api/courses/{course_id}/complete", "student", {}, allow_all=True)

        # quiz answer as student
        if qid:
            call("POST", f"/api/courses/{course_id}/questions/{qid}/answer", "student", {"answer": "4"}, allow_all=True)
            call("DELETE", f"/api/courses/{course_id}/questions/{qid}/attempt", "student", allow_all=True)

    # --- classroom / EMS --------------------------------------------------------
    call("POST", "/api/classes", "schooladmin", {"name": f"Smoke Class {TAG}"}, allow_all=True)
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM classes WHERE name=%s ORDER BY id DESC LIMIT 1", (f"Smoke Class {TAG}",))
    row = cur.fetchone()
    conn.close()
    class_id = row[0] if row else None
    if class_id:
        created["classes"].append(class_id)
    print("class:", class_id)
    if class_id:
        call("GET", "/api/classes/my-classes", "schooladmin", allow_all=True)
        call("GET", f"/api/classes/{class_id}/enrolled-students", "schooladmin", allow_all=True)
        call("GET", f"/api/classes/{class_id}/unassigned-students", "schooladmin", allow_all=True)
        ce, _ = call("POST", "/api/class-enrollments", "schooladmin", {"class_id": class_id, "student_id": ids["student"]}, allow_all=True)
        call("GET", f"/api/posts/class/{class_id}", "student", allow_all=True)
        call("POST", "/api/posts/class", "teacher", {"class_id": class_id, "content": "hi class"}, allow_all=True)
    if school_id:
        call("GET", f"/api/posts/school/{school_id}", "schooladmin", allow_all=True)
        call("POST", "/api/posts/school", "schooladmin", {"content": "smoke announcement"}, allow_all=True)

    # teacher assignment via class code
    if course_id:
        call("POST", "/api/teacher/assign-course", "teacher", {
            "classCode": f"T{TAG[:4]}", "courseId": course_id, "title": "Smoke assignment",
        }, allow_all=True)
        call("GET", "/api/teacher/my-assignments", "teacher", allow_all=True)
    if class_id and course_id:
        r3, _ = call("POST", "/api/assignments", "teacher", {
            "class_id": class_id, "course_id": course_id, "title": "Smoke hw", "due_date": None,
        }, allow_all=True)
        aid = ((r3.json().get("data") or {}) if r3 is not None else {}).get("id")
        if aid:
            created["assignments"].append(aid)
        print("assignment:", aid)
        call("GET", "/api/student/my-assignments", "student", allow_all=True)
        call("GET", "/api/student/assignments", "student", allow_all=True)
        call("GET", "/api/teacher/class/T%s/submissions" % TAG[:4], "teacher", allow_all=True)
        if aid:
            call("GET", f"/api/assignments/{aid}/progress", "teacher", allow_all=True)
            call("POST", f"/api/assignments/{aid}/submit", "student", {"completion_percentage": 80}, allow_all=True)
            call("POST", "/api/student/submit-assignment", "student", {"assignment_id": aid, "completion_percentage": 80}, allow_all=True)
            call("GET", f"/api/student/{ids['student']}/assignment/{aid}/accuracy", "teacher", allow_all=True)
            call("GET", f"/api/teacher/assignment/{aid}/student-accuracy", "teacher", allow_all=True)

    # --- posts / calendar / messages -------------------------------------------
    call("GET", "/api/calendar", "student", allow_all=True)
    call("POST", "/api/calendar/parse-post", "teacher", {"content": "Quiz Friday at 10am"}, allow_all=True)
    ms, _ = call("POST", "/api/messages/send", "teacher", {"recipient_id": ids["student"], "content": "hello"}, allow_all=True)
    mid = ((ms.json().get("data") or {}) if ms is not None else {}).get("id")
    call("GET", "/api/messages", "student", allow_all=True)
    if mid:
        call("PUT", f"/api/messages/{mid}/read", "student", {}, allow_all=True)

    # --- gamification -----------------------------------------------------------
    call("GET", "/api/learner/profile", "student", allow_all=True)
    call("GET", "/api/learner/store", "student", allow_all=True)
    call("POST", "/api/users/grant-gems", "admin", {"userId": ids["student"], "amount": 500}, allow_all=True)
    call("POST", "/api/learner/checkin", "student", {}, allow_all=True)
    call("POST", "/api/learner/award-xp", "student", {"amount": 10, "source": "smoke"}, allow_all=True)
    if course_id:
        call("POST", "/api/learner/reward-quiz", "student", {"courseId": course_id, "correct": 1, "total": 1}, allow_all=True)
        call("GET", f"/api/learner/boss-state/{course_id}", "student", allow_all=True)
        call("POST", f"/api/learner/boss-state/{course_id}", "student", {"boss_hp": 90}, allow_all=True)
    call("PUT", "/api/learner/settings", "student", {"avatar_config": {"hat": None}}, allow_all=True)
    call("POST", "/api/learner/feedback", "student", {"message": "smoke feedback", "rating": 5}, allow_all=True)
    call("GET", "/api/learner/feedback", "admin", allow_all=True)
    call("POST", "/api/learner/store/purchase", "student", {"itemId": "hat_gold"}, allow_all=True)
    call("POST", "/api/learner/equip", "student", {"slot": "hat", "itemId": "hat_gold"}, allow_all=True)
    call("GET", "/api/users/volunteer-stats", "student", allow_all=True)

    # --- simulators -------------------------------------------------------------
    r4, _ = call("POST", "/api/simulators", "teacher", {
        "title": f"Smoke Sim {TAG}", "description": "temp", "blocks": [], "connections": [],
        "tags": ["smoke"], "is_public": False, "status": "draft",
    }, allow_all=True)
    sdata = (r4.json().get("data") or {}) if r4 is not None else {}
    sid = sdata.get("id") or (sdata.get("simulator") or {}).get("id") or sdata.get("simulatorId")
    if sid:
        created["simulators"].append(sid)
    print("simulator:", sid)
    if sid:
        call("GET", f"/api/simulators/{sid}", "teacher", allow_all=True)
        call("PUT", f"/api/simulators/{sid}", "teacher", {"title": f"Smoke Sim {TAG} v2"}, allow_all=True)
        call("POST", f"/api/simulators/{sid}/publish", "teacher", {}, allow_all=True)
        call("POST", f"/api/simulators/{sid}/ratings", "student", {"rating": 4, "review": "ok"}, allow_all=True)
        call("GET", f"/api/simulators/{sid}/ratings", "student", allow_all=True)
        call("POST", f"/api/simulators/{sid}/comments", "student", {"content": "nice"}, allow_all=True)
        call("GET", f"/api/simulators/{sid}/comments", "student", allow_all=True)
        call("POST", f"/api/simulators/{sid}/versions", "teacher", {"blocks": [], "version_note": "v2"}, allow_all=True)
        call("GET", f"/api/simulators/{sid}/versions", "teacher", allow_all=True)
        call("GET", f"/api/simulators/{sid}/versions/1", "teacher", allow_all=True)
        call("POST", f"/api/simulators/{sid}/fork", "student", {}, allow_all=True)
        call("GET", f"/api/simulators/{sid}/forks", "teacher", allow_all=True)
        call("POST", f"/api/simulators/{sid}/download", "student", {}, allow_all=True)
        call("GET", "/api/simulators", None, allow_all=True)
        call("GET", "/api/simulators/trending/all", None, allow_all=True)
        call("GET", "/api/my-simulators", "teacher", allow_all=True)
        call("GET", "/api/my-blocked-simulators", "teacher", allow_all=True)
        if course_id:
            call("POST", f"/api/courses/{course_id}/simulators", "teacher", {"simulator_id": sid}, allow_all=True)
            call("GET", f"/api/courses/{course_id}/simulators", "teacher", allow_all=True)
            call("DELETE", f"/api/courses/{course_id}/simulators/{sid}", "teacher", allow_all=True)

    # --- schools / certificates / sponsorships / admin --------------------------
    call("GET", "/api/schools", "admin", allow_all=True)
    call("GET", "/api/schools/pending", "admin", allow_all=True)
    call("GET", "/api/schools/my-school", "schooladmin", allow_all=True)
    call("GET", "/api/schools/my-school/students", "schooladmin", allow_all=True)
    if school_id:
        call("GET", f"/api/schools/by-code/{TAG[:6]}", "schooladmin", allow_all=True)
        call("PUT", f"/api/schools/{school_id}/approve", "admin", {}, allow_all=True)
    call("GET", "/api/certificates/verify/NOPE123", None, expect=(200, 404), allow_all=True)
    call("GET", "/api/sponsorships", None, allow_all=True)
    call("POST", "/api/sponsorships", "admin", {"sponsor_name": f"Smoke Sponsor {TAG}", "contribution_amount": 10, "tier": "bronze"}, allow_all=True)
    call("GET", "/api/users", "admin", allow_all=True)
    call("GET", "/api/superadmin/users", "admin", allow_all=True)
    call("GET", "/api/users/pending-teachers", "admin", allow_all=True)
    call("GET", "/api/users/teachers", "admin", allow_all=True)
    call("GET", "/api/users/parents", "admin", allow_all=True)
    call("GET", f"/api/users/{ids['teacher']}/courses", "admin", allow_all=True)
    call("GET", "/api/users/lookup?email=smoke_teacher_%s@example.com" % TAG.lower(), "admin", allow_all=True)
    call("GET", "/api/users/me", "student", allow_all=True)
    call("GET", "/api/users/profile", "student", allow_all=True)
    call("PUT", f"/api/users/{ids['student']}/role", "admin", {"role": "student"}, allow_all=True)
    call("PUT", f"/api/superadmin/users/{ids['student']}/role", "admin", {"role": "student"}, allow_all=True)
    call("PUT", f"/api/admin/users/smoke_student_{TAG.lower()}@example.com/role", "admin", {"role": "student"}, allow_all=True)
    call("POST", "/api/users/update-volunteer-hours", "teacher", {"hours": 1}, allow_all=True)
    call("GET", "/api/search?q=algebra", "student", allow_all=True)
    call("GET", "/api/courses/all", "admin", allow_all=True)
    call("GET", "/api/parent/my-children", "parent", allow_all=True)
    call("POST", "/api/parent/link-student", "parent", {"student_email": f"smoke_student_{TAG.lower()}@example.com"}, allow_all=True)
    call("GET", f"/api/parent/child/{ids['student']}/progress", "parent", allow_all=True)
    call("GET", "/api/student/my-parent-code", "student", allow_all=True)
    call("GET", "/api/student/my-classes", "student", allow_all=True)
    call("POST", "/api/student/enroll-class", "student", {"class_code": f"T{TAG[:4]}"}, allow_all=True)
    call("GET", "/api/user/class-code", "teacher", allow_all=True)
    call("PUT", f"/api/classes/{class_id}/teacher", "schooladmin", {"teacher_id": ids["teacher"]}, allow_all=True) if class_id else None
    call("POST", "/api/student/update-status", "student", {"status": "active"}, allow_all=True)

    # --- AI routes (no keys configured: must fail gracefully, not crash) --------
    for path, body in [
        ("/api/ai/tutor/chat", {"message": "hi", "courseId": course_id}),
        ("/api/ai/editor-help", {"prompt": "help", "content": "x"}),
        ("/api/ai/notes-course", {"notes": "photosynthesis", "title": "Smoke"}),
        ("/api/ai/simulator-help", {"prompt": "help"}),
    ]:
        call("POST", path, "teacher", body, expect=(200, 201, 400, 401, 403, 404, 429, 500, 503), allow_all=True)
    call("GET", "/api/ai/tutor/history", "student", allow_all=True)
    call("GET", "/api/ai/editor-help/history", "teacher", allow_all=True)
    call("DELETE", "/api/ai/editor-help/history", "teacher", allow_all=True)
    call("GET", "/api/ai/notes-course/nonexistent", "teacher", allow_all=True)

    # --- auth edge cases --------------------------------------------------------
    call("POST", "/api/forgot-password", None, {"email": f"smoke_student_{TAG.lower()}@example.com"}, allow_all=True)
    call("POST", "/api/reset-password", None, {"token": "bogus", "password": PW}, allow_all=True)
    call("POST", "/api/logout", "student", {}, allow_all=True)
    call("GET", "/api/courses", None, expect=(200, 401), allow_all=True)
    call("GET", "/api/users/me", None, expect=(200, 401), allow_all=True)

    print(f"\n== {checks['pass']} passed, {checks['fail']} failed ==")
    if failures:
        print("\nFAILURES:")
        for f in failures:
            print(" -", f)
    with open("_smoke_created.json", "w", encoding="utf-8") as fh:
        json.dump({"tag": TAG, "ids": ids, "created": created}, fh, indent=2)
    print("\ncreated:", json.dumps(created))
    return 0 if checks["fail"] == 0 else 1


def cleanup():
    path = "_smoke_created.json"
    if not os.path.exists(path):
        print("nothing to clean")
        return
    data = json.load(open(path, encoding="utf-8"))
    users = data["created"]["users"]
    courses = data["created"]["courses"]
    sims = data["created"]["simulators"]
    classes = data["created"]["classes"]
    schools = [s for s in [data["ids"].get("schooladmin")] if s]  # placeholder
    conn = db()
    cur = conn.cursor()
    uids = ",".join(str(u) for u in users) if users else "NULL"
    cids = ",".join(str(c) for c in courses) if courses else "NULL"
    sids = ",".join(str(s) for s in sims) if sims else "NULL"
    clids = ",".join(str(c) for c in classes) if classes else "NULL"

    statements = [
        f"DELETE FROM user_quiz_attempts WHERE user_id IN ({uids})",
        f"DELETE FROM course_views WHERE user_id IN ({uids}) OR course_id IN ({cids})",
        f"DELETE FROM course_enrollment_progress WHERE user_id IN ({uids}) OR course_id IN ({cids})",
        f"DELETE FROM enrollments WHERE user_id IN ({uids}) OR course_id IN ({cids})",
        f"DELETE FROM course_likes WHERE user_id IN ({uids}) OR course_id IN ({cids})",
        f"DELETE FROM assignment_submissions WHERE student_id IN ({uids})",
        f"DELETE FROM assignment_progress WHERE student_id IN ({uids})",
        f"DELETE FROM classroom_assignments WHERE course_id IN ({cids}) OR teacher_id IN ({uids})",
        f"DELETE FROM assignments WHERE course_id IN ({cids})",
        f"DELETE FROM class_enrollments WHERE student_id IN ({uids}) OR class_id IN ({clids})",
        f"DELETE FROM messages WHERE sender_id IN ({uids}) OR recipient_id IN ({uids})",
        f"DELETE FROM posts WHERE author_id IN ({uids}) OR class_id IN ({clids})",
        f"DELETE FROM calendar_events WHERE class_id IN ({clids})",
        f"DELETE FROM certificates WHERE user_id IN ({uids})",
        f"DELETE FROM user_badges WHERE user_id IN ({uids})",
        f"DELETE FROM user_inventory WHERE user_id IN ({uids})",
        f"DELETE FROM user_learning_profile WHERE user_id IN ({uids})",
        f"DELETE FROM user_boss_state WHERE user_id IN ({uids})",
        f"DELETE FROM user_xp_events WHERE user_id IN ({uids})",
        f"DELETE FROM user_feedback WHERE user_id IN ({uids})",
        f"DELETE FROM parent_student_links WHERE parent_id IN ({uids}) OR student_id IN ({uids})",
        f"DELETE FROM simulator_comments WHERE simulator_id IN ({sids}) OR user_id IN ({uids})",
        f"DELETE FROM simulator_ratings WHERE simulator_id IN ({sids}) OR user_id IN ({uids})",
        f"DELETE FROM simulator_versions WHERE simulator_id IN ({sids})",
        f"DELETE FROM simulator_downloads WHERE simulator_id IN ({sids}) OR user_id IN ({uids})",
        f"DELETE FROM simulator_interactive_params WHERE course_id IN ({cids})",
        f"DELETE FROM simulators WHERE id IN ({sids}) OR creator_id IN ({uids})",
        f"DELETE FROM course_questions WHERE course_id IN ({cids})",
        f"DELETE FROM course_units WHERE parent_course_id IN ({cids}) OR child_course_id IN ({cids})",
        f"DELETE FROM course_units WHERE child_course_id IN ({cids})",
        f"DELETE FROM classes WHERE id IN ({clids})",
        f"DELETE FROM sponsorships WHERE sponsor_name LIKE 'Smoke Sponsor%'",
        f"DELETE FROM ai_tutor_messages WHERE user_id IN ({uids})",
        f"DELETE FROM ai_editor_help_messages WHERE user_id IN ({uids})",
        f"DELETE FROM notes_course_jobs WHERE user_id IN ({uids})",
        f"DELETE FROM courses WHERE id IN ({cids})",
        f"DELETE FROM users WHERE id IN ({uids})",
    ]
    for stmt in statements:
        try:
            cur.execute(stmt)
            conn.commit()
        except Exception as exc:  # noqa: BLE001
            conn.rollback()
            print("skip:", stmt.split("WHERE")[0].strip(), "->", str(exc).splitlines()[0][:110])
    # schools created by the smoke school-admin
    try:
        cur.execute("DELETE FROM schools WHERE name LIKE 'Smoke High %'")
        conn.commit()
    except Exception as exc:  # noqa: BLE001
        conn.rollback()
        print("skip schools:", str(exc).splitlines()[0][:110])
    for table in ("users", "courses", "course_questions", "course_units", "enrollments", "simulators", "classes", "posts", "messages"):
        cur.execute(f"SELECT count(*) FROM {table}")
        print(f"{table}: {cur.fetchone()[0]}")
    conn.close()
    os.remove(path)


if __name__ == "__main__":
    if "--cleanup-only" in sys.argv:
        cleanup()
        raise SystemExit(0)
    code = main()
    cleanup()
    raise SystemExit(code)
