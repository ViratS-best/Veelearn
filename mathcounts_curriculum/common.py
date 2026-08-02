"""Shared helpers for deep MathCounts / AMC curriculum HTML + quiz generation."""

from __future__ import annotations

import math
import random
import re
from collections import Counter
from itertools import combinations


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
    return (
        f'<div style="background:{bg};border:1px solid {border};border-radius:12px;'
        f'padding:18px;margin:16px 0;">'
        f"<h4>{kind}: {title}</h4>{body}</div>"
    )


def why_box(title: str, body: str) -> str:
    return callout("Why this matters", title, body, "#f0f9ff", "#7dd3fc")


def think_box(title: str, body: str) -> str:
    return callout("How to think about it", title, body, "#f5f3ff", "#c4b5fd")


def watch_out(title: str, body: str) -> str:
    return callout("Watch out", title, f"<p>{body}</p>", "#fffbeb", "#fcd34d")


def strategy_tip(title: str, body: str) -> str:
    return callout("Contest strategy", title, f"<p>{body}</p>", "#ecfdf5", "#6ee7b7")


def check_yourself(items) -> str:
    return (
        '<div style="background:#f8fafc;border:1px dashed #94a3b8;border-radius:12px;'
        'padding:16px;margin:16px 0;">'
        "<h4>Check yourself before moving on</h4>"
        + ul(items)
        + "</div>"
    )


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
        "<li><strong>Problems 1–15:</strong> Easy / Chapter MathCounts &amp; early AMC 8</li>"
        "<li><strong>Problems 16–30:</strong> Medium / AMC 8 mid-to-late &amp; MathCounts Sprint</li>"
        "<li><strong>Problems 31–40:</strong> Hard / MathCounts Target &amp; AMC 8 end</li>"
        "<li><strong>Problems 41–50:</strong> Stretch / MathCounts State–National &amp; AMC 10 style</li>"
        "</ul>"
        "<p>Take your time. Contest counting is a skill you build by explaining each step out loud.</p>"
    )


def solved(num, problem, steps, answer, note="", level="Easy"):
    colors = {
        "Easy": "#dcfce7",
        "Medium": "#dbeafe",
        "Hard": "#fef3c7",
        "Challenge": "#fce7f3",
        "National": "#fee2e2",
        "AMC10": "#ffedd5",
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
        why_box("Keep this in mind", why),
        think_box("A clear plan", think),
        examples_html,
    ]
    if watch:
        parts.append(watch_out(watch[0], watch[1]))
    if tip:
        parts.append(strategy_tip(tip[0], tip[1]))
    parts.append(check_yourself(checklist))
    parts.append(mini_practice_heading(title))
    parts.append(slots_range(quiz_start, 5))
    return "\n".join(parts)


def make_question(text, correct, distractors, explanation, idx, points=1):
    opts = [str(correct)] + [str(d) for d in distractors[:3]]
    unique = []
    for opt in opts:
        if opt not in unique:
            unique.append(opt)
    while len(unique) < 4:
        if str(correct).lstrip("-").isdigit():
            filler = str(int(correct) + len(unique) * 3 + 1)
        else:
            filler = f"Choice {len(unique) + 1}"
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
    for delta in (1, -1, 2, -2, 3, -3, 5, -5, 10, -10, max(0, c // 2), c * 2, c + 7, abs(c - 7)):
        v = c + delta if delta < 50 else delta
        if isinstance(v, int) and v >= 0 and v != c:
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


def mq(text, correct, explanation, idx, distractors=None):
    d = distractors if distractors is not None else near_int(correct)
    return make_question(text, correct, d, explanation, idx)


def perm_repeated(word: str) -> int:
    c = Counter(word)
    n = len(word)
    denom = 1
    for v in c.values():
        denom *= math.factorial(v)
    return math.factorial(n) // denom


def stars_bars_nonneg(n, k):
    return math.comb(n + k - 1, k - 1)


def stars_bars_positive(n, k):
    return stars_bars_nonneg(n - k, k)


def pie_divisible(limit, primes):
    total = 0
    for r in range(1, len(primes) + 1):
        for combo in combinations(primes, r):
            prod = 1
            for p in combo:
                prod *= p
            term = limit // prod
            total += term if r % 2 == 1 else -term
    return total


def lattice_paths(a, b):
    return math.comb(a + b, a)


def fib(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def domino_tilings(n):
    """Number of ways to tile a 2xn board with 1x2 dominoes (n >= 0)."""
    if n == 0:
        return 1
    return fib(n + 1)


def no_consecutive_ones(n):
    """Length-n binary strings with no two consecutive 1s (n >= 0)."""
    if n == 0:
        return 1
    return fib(n + 2)


def catalan(n):
    return math.comb(2 * n, n) // (n + 1)


def surjections(n, k):
    """Number of onto (surjective) functions from an n-set to a k-set."""
    total = 0
    for i in range(0, k + 1):
        term = math.comb(k, i) * (k - i) ** n
        total += term if i % 2 == 0 else -term
    return total


def binom_tex(n, k) -> str:
    return f"\\binom{{{n}}}{{{k}}}"


def frac_tex(top, bottom) -> str:
    return f"\\dfrac{{{top}}}{{{bottom}}}"


def derangement(n):
    """Number of permutations of n items with no item in its original spot."""
    if n == 0:
        return 1
    if n == 1:
        return 0
    a, b = 1, 0
    for i in range(2, n + 1):
        a, b = b, (i - 1) * (a + b)
    return b


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
<p>This unit is written for students in grades 6–8 who are preparing for
<strong>MathCounts</strong> (Chapter → State → National) and <strong>AMC 8 / early AMC 10</strong>.
Counting is not usually a big chapter in school math, so we go slowly and explain every idea
in everyday language. Read each section fully. Do the 5 quick problems after each idea.
Then finish the 50-problem set at the end.</p>
{why_box("You are building a superpower",
    "<p>Almost every hard contest counting problem is really a few easy ideas stacked carefully. "
    "If you understand <em>why</em> each step works, hard problems stop feeling like magic.</p>")}
<h2>What you will learn in this unit</h2>
{ol(roadmap_items)}
{body_html}
{final_slots_html}
"""
