"""Shared helpers for deep Algebra 2 (grade 10) curriculum HTML + quiz generation."""

from __future__ import annotations

import math


def page_break():
    return '<hr class="page-break" />'


def quiz_slot(n: int) -> str:
    return f"<!--QUIZ_SLOT_{n}-->"


def slots_range(start: int, count: int = 5) -> str:
    return "\n".join(quiz_slot(i) for i in range(start, start + count))


def p(*paragraphs: str) -> str:
    return "".join(f"<p>{x}</p>" for x in paragraphs)


def ul(items) -> str:
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def ol(items) -> str:
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def callout(kind: str, title: str, body: str, bg: str, border: str) -> str:
    if body and not body.strip().startswith("<"):
        body = f"<p>{body}</p>"
    return (
        f'<div style="background:{bg};border:1px solid {border};border-radius:12px;'
        f'padding:18px;margin:16px 0;">'
        f"<h4>{kind}: {title}</h4>{body}</div>"
    )


def _as_html(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    if text.startswith("<"):
        return text
    return f"<p>{text}</p>"


def why_box(_title: str, body: str) -> str:
    return _as_html(body)


def think_box(_title: str, body: str) -> str:
    return _as_html(body)


def watch_out(title: str, body: str) -> str:
    return callout("Common mistake", title, _as_html(body), "#fffbeb", "#fcd34d")


def strategy_tip(_title: str, _body: str) -> str:
    return ""


def check_yourself(_items) -> str:
    return ""


def mini_practice_heading(concept_name: str) -> str:
    return (
        f"<h3>Quick practice — {concept_name} (5 problems)</h3>"
        "<p>Do these on paper first. They check the idea you just learned. "
        "Answers and explanations appear after you submit.</p>"
    )


def end_practice_heading() -> str:
    return (
        "<h2>Full Practice Set (50 Problems)</h2>"
        "<p>These get harder as you go:</p>"
        "<ul>"
        "<li><strong>Problems 1–15:</strong> Easy / skill builders &amp; early chapter checks</li>"
        "<li><strong>Problems 16–30:</strong> Medium / mixed quiz &amp; homework style</li>"
        "<li><strong>Problems 31–40:</strong> Hard / chapter test &amp; multi-step</li>"
        "<li><strong>Problems 41–50:</strong> Stretch / honors Algebra 2 &amp; early Precalculus / SAT Math</li>"
        "</ul>"
    )


def solved(num, problem, steps, answer, note="", level="Easy"):
    colors = {
        "Easy": "#dcfce7",
        "Medium": "#dbeafe",
        "Hard": "#fef3c7",
        "Challenge": "#fce7f3",
        "Honors": "#fee2e2",
        "SAT": "#ffedd5",
    }
    bg = colors.get(level, "#f4f8ff")
    steps_html = "".join(f"<li>{s}</li>" for s in steps)
    note_html = f"<p><em>{note}</em></p>" if note else ""
    return (
        f'<div style="background:#f8fafc;border:1px solid #cbd5e1;border-radius:12px;'
        f'padding:18px;margin:18px 0;">'
        f'<p><span style="background:{bg};padding:3px 12px;border-radius:999px;'
        f'font-weight:700;font-size:0.9em;">{level}</span></p>'
        f"<h4>Fully solved example {num}</h4>"
        f"<p><strong>Problem:</strong> {problem}</p>"
        f"<p><strong>Slow walkthrough:</strong></p>"
        f"<ol>{steps_html}</ol>"
        f'<p><strong>Final answer:</strong> <span style="background:#dcfce7;padding:3px 10px;'
        f'border-radius:6px;font-weight:700;">{answer}</span></p>{note_html}</div>'
    )


def concept_block(
    title: str,
    intro_paras,
    why: str,
    think: str,
    examples_html: str,
    watch: tuple[str, str] | None,
    tip: tuple[str, str] | None,
    checklist,
    quiz_start: int,
):
    parts = [
        page_break(),
        f"<h2>{title}</h2>",
        p(*intro_paras),
        why_box("", why),
        think_box("", think),
        examples_html,
    ]
    if watch:
        parts.append(watch_out(watch[0], watch[1]))
    parts.append(mini_practice_heading(title))
    parts.append(slots_range(quiz_start, 5))
    return "\n".join(part for part in parts if part)


def make_question(text, correct, distractors, explanation, idx, points=1):
    opts = [str(correct)] + [str(d) for d in distractors[:3]]
    unique = []
    for opt in opts:
        if opt not in unique:
            unique.append(opt)
    while len(unique) < 4:
        filler = f"Choice {len(unique) + 1}"
        if str(correct).replace(".", "", 1).lstrip("-").isdigit():
            try:
                filler = str(int(float(correct)) + len(unique) * 3 + 1)
            except ValueError:
                pass
        if filler not in unique and filler != str(correct):
            unique.append(filler)
    return {
        "question_text": text,
        "question_type": "multiple_choice",
        "options": unique,
        "correct_answer": str(correct),
        "explanation": explanation,
        "points": points,
        "order_index": idx,
    }


def near_int(correct, count=3):
    c = int(correct)
    pool = []
    for delta in (1, -1, 2, -2, 3, -3, 5, -5, 10, -10, c * 2, abs(c - 7), c + 7):
        v = c + delta if abs(delta) <= 20 else delta
        if isinstance(v, int) and v != c:
            pool.append(str(v))
    unique = []
    for pval in pool:
        if pval not in unique:
            unique.append(pval)
        if len(unique) >= count:
            break
    while len(unique) < count:
        filler = str(c + 11 + len(unique))
        if filler != str(c) and filler not in unique:
            unique.append(filler)
    return unique[:count]


def near_str(correct: str, alts, count=3):
    unique = []
    for a in alts:
        if str(a) != str(correct) and str(a) not in unique:
            unique.append(str(a))
        if len(unique) >= count:
            break
    while len(unique) < count:
        filler = f"Option {len(unique) + 1}"
        if filler not in unique and filler != str(correct):
            unique.append(filler)
    return unique[:count]


def mq(text, correct, explanation, idx, distractors=None):
    if distractors is not None:
        d = distractors
    elif str(correct).lstrip("-").isdigit():
        d = near_int(correct)
    else:
        d = near_str(correct, [])
    return make_question(text, correct, d, explanation, idx)


def renumber(questions):
    out = []
    for i, q in enumerate(questions, 1):
        qq = dict(q)
        qq["order_index"] = i
        out.append(qq)
    return out


def practice_slots(start: int, count: int = 50) -> str:
    return end_practice_heading() + "\n" + "\n".join(quiz_slot(i) for i in range(start, start + count))


def unit_shell(title: str, audience: str, roadmap_items, body_html: str, final_slots_html: str) -> str:
    return f"""
<h1>{title}</h1>
<p><strong>Audience:</strong> {audience}</p>
<p>This unit is written for <strong>10th-grade Algebra 2</strong> students. Each idea is explained in
clear language with LaTeX, then shown in fully worked examples. After the examples you will see a
common mistake for that idea, then 5 quick problems. A 50-problem set at the end goes from Easy to Stretch.</p>
<h2>What you will learn in this unit</h2>
{ol(roadmap_items)}
{body_html}
{final_slots_html}
"""


def quadratic_roots(a, b, c):
    """Return (disc, roots_list as complex or float)."""
    disc = b * b - 4 * a * c
    if disc >= 0:
        r1 = (-b + math.sqrt(disc)) / (2 * a)
        r2 = (-b - math.sqrt(disc)) / (2 * a)
        return disc, [r1, r2]
    return disc, []
