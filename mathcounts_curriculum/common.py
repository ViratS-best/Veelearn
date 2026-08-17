"""Shared helpers for deep MathCounts / AMC curriculum HTML + quiz generation."""

from __future__ import annotations

import math
import random
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
    body_html = _as_html(body)
    return (
        '<div class="vl-callout vl-callout-trap" data-vl-kind="trap">'
        '<div class="vl-callout-icon">⚠️</div>'
        f'<div class="vl-callout-body"><h4>Common mistake: {title}</h4>{body_html}</div>'
        "</div>"
    )


def strategy_tip(title: str, body: str) -> str:
    return (
        '<div class="vl-callout vl-callout-strategy" data-vl-kind="strategy">'
        '<div class="vl-callout-icon">💡</div>'
        f'<div class="vl-callout-body"><h4>Test strategy: {title}</h4>{_as_html(body)}</div>'
        "</div>"
    )


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
        "<h2>Full Practice Set (25 Problems)</h2>"
        "<p>These get harder as you go — all on this unit's topic:</p>"
        "<ul>"
        "<li><strong>Problems 1–8:</strong> Medium warm-ups</li>"
        "<li><strong>Problems 9–16:</strong> Hard / MathCounts Target &amp; AMC 8</li>"
        "<li><strong>Problems 17–25:</strong> Stretch / contest-style</li>"
        "</ul>"
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
        '<svg width="0" height="0" aria-hidden="true"></svg>'
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
    if tip:
        parts.append(strategy_tip(tip[0], tip[1]))
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


def practice_slots(start: int, count: int = 25) -> str:
    return end_practice_heading() + "\n" + "\n".join(quiz_slot(i) for i in range(start, start + count))


def unit_shell(title: str, audience: str, roadmap_items, body_html: str, final_slots_html: str) -> str:
    return f"""
<h1>{title}</h1>
<p><strong>Audience:</strong> {audience}</p>
<p>This unit is written for students in grades 6–8 who are preparing for
<strong>MathCounts</strong> (Chapter → State → National) and <strong>AMC 8 / early AMC 10</strong>.
Each idea is explained in everyday language, then shown in fully worked examples. After the examples
you will see a common mistake for that idea, then 5 quick problems. A 50-problem set at the end
goes from Easy to National / AMC 10 stretch.</p>
<h2>What you will learn in this unit</h2>
{ol(roadmap_items)}
{body_html}
{final_slots_html}
"""
