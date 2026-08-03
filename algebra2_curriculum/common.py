"""Shared helpers for deep Algebra 2 (grade 10) curriculum HTML + quiz generation."""

from __future__ import annotations

import math
import re


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


def _plain(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text or "").strip()


def enrich_why(short: str) -> str:
    core = _plain(short)
    return (
        f"<p><strong>Big idea:</strong> {core}</p>"
        "<p><strong>Why Algebra 2 cares:</strong> Later units (logs, rationals, trig) assume you can move "
        "between graphs, equations, and words without losing meaning. If you only memorize steps, a tiny "
        "wording change on a quiz will break the whole solution.</p>"
        "<p><strong>What good looks like:</strong> You can explain the idea in plain English, show a tiny "
        "numeric example, and name which tool you used (factor, complete the square, substitution, "
        "property of exponents/logs, etc.).</p>"
        "<p><strong>Practice habit:</strong> After each solved example, cover the answer and reteach the steps "
        "out loud. If you cannot name why a step is legal, reread that part before the quick practice.</p>"
    )


def enrich_think(short: str) -> str:
    core = _plain(short)
    return (
        f"<p><strong>Your plan on paper:</strong> {core}</p>"
        "<p><strong>Step-by-step routine (do this every time):</strong></p>"
        "<ol>"
        "<li>Rewrite the goal in one sentence: <em>I am solving / graphing / simplifying ___</em>.</li>"
        "<li>Underline constraints: domain, undefined points, extraneous roots, integer requirements.</li>"
        "<li>Choose the tool: factor, formula, complete square, substitution, property of exponents/logs, etc.</li>"
        "<li>Box intermediate results (discriminant, rewritten form, restricted values).</li>"
        "<li>Check: plug back in, check domain, and ask if the answer size/sign makes sense.</li>"
        "</ol>"
        "<p><strong>If you feel stuck:</strong> Replace awkward numbers with friendlier ones that keep the same "
        "structure, solve the tiny version, then return to the real numbers with the same outline.</p>"
    )


def _watch_extra(title: str) -> str:
    t = title.lower()
    if "extraneous" in t or "domain" in t or "undefined" in t:
        return (
            "<p><strong>Extra detail:</strong> Squaring both sides, clearing denominators, or taking even roots "
            "can create fake solutions. Always list the domain / allowed values first, solve, then test every "
            "candidate in the <em>original</em> equation.</p>"
        )
    if "sign" in t or "factor" in t or "distribut" in t:
        return (
            "<p><strong>Extra detail:</strong> Most Algebra 2 sign errors come from distributing a negative "
            "across parentheses or dropping a factor when canceling. Expand carefully, then factor back to check.</p>"
        )
    if "log" in t or "exponent" in t:
        return (
            "<p><strong>Extra detail:</strong> Log and exponential properties only apply when bases and arguments "
            "are valid. Write the domain (argument $>0$, base $>0$ and $\\neq 1$) before using any property.</p>"
        )
    if "complex" in t or "imaginary" in t:
        return (
            "<p><strong>Extra detail:</strong> Treat $i$ like a variable with the rule $i^2=-1$. Combine like terms "
            "(reals with reals, imaginaries with imaginaries). Do not “cancel $i$” casually across equations.</p>"
        )
    return (
        "<p><strong>Extra detail:</strong> Invent a 10-second story of a student who falls for this trap. "
        "If you can tell that story, you will catch it earlier on quizzes and tests.</p>"
    )


def _strategy_extra(title: str) -> str:
    t = title.lower()
    if "box" in t or "intermediate" in t:
        return (
            "<p><strong>Boxing habit:</strong> Label boxes like <code>a=</code>, <code>b=</code>, <code>c=</code>, "
            "<code>Δ=</code>, <code>domain</code>, <code>candidate roots</code>. Combine only after every piece is boxed.</p>"
        )
    if "graph" in t or "transform" in t:
        return (
            "<p><strong>Graph habit:</strong> Start from a parent function, list transformations in order "
            "(horizontal shifts/scales first as written inside, then vertical), then plot 3–5 key points.</p>"
        )
    if "check" in t or "plug" in t or "verify" in t:
        return (
            "<p><strong>Verify habit:</strong> Substitute every proposed solution into the original equation. "
            "For inequalities, test a point in each interval. For graphs, check intercepts and end behavior.</p>"
        )
    return (
        "<p><strong>Make the play automatic:</strong> Write the strategy name at the top of your scratch paper, "
        "then execute it without skipping steps. Algebra 2 rewards clean outlines more than last-second inspiration.</p>"
    )


def enrich_watch(title: str, short: str) -> str:
    core = _plain(short)
    return (
        f"<p><strong>The trap called &quot;{title}&quot;:</strong> {core}</p>"
        "<p><strong>Why this trap shows up so often:</strong> Under time pressure, students jump to a familiar "
        "formula before checking domain, structure, or whether the equation was changed illegally "
        "(squaring, canceling a variable factor, etc.).</p>"
        f"{_watch_extra(title)}"
        "<p><strong>Warning signs:</strong> a solution that makes a denominator zero, a negative under an even root "
        "in the reals, a log of a non-positive number, or an answer that fails a quick plug-in check.</p>"
        "<p><strong>How to dodge it:</strong></p>"
        "<ul>"
        "<li>State domain / restrictions before solving.</li>"
        "<li>Name the legal move you are about to use (factor, square, take log, etc.).</li>"
        "<li>Box middle results so factors do not disappear.</li>"
        "<li>Plug every candidate into the original problem.</li>"
        "</ul>"
        "<p><strong>Repair move:</strong> Keep the wrong work visible. Write a corrected outline beside it, then "
        "recompute. Comparing the two outlines teaches faster than erasing everything.</p>"
    )


def enrich_strategy(title: str, short: str) -> str:
    core = _plain(short)
    return (
        f"<p><strong>Strategy — {title}:</strong> {core}</p>"
        "<p><strong>How to use it in Algebra 2:</strong> Treat this like a coach play. Practice it slowly in the "
        "lesson until it feels automatic, then use it on homework and tests.</p>"
        f"{_strategy_extra(title)}"
        "<p><strong>Concrete scratch-paper actions:</strong></p>"
        "<ol>"
        f"<li>Write the strategy name at the top: {title}.</li>"
        "<li>List what must not be lost (domain, coefficients, rewritten form, key points).</li>"
        "<li>Box every intermediate result and label it.</li>"
        "<li>Finish the algebra, then verify.</li>"
        "<li>Ask: Did I answer the original question (solve vs simplify vs graph)?</li>"
        "</ol>"
        "<p><strong>When to move on:</strong> If after a minute you still cannot name the structure "
        "(quadratic? rational? exponential?), rewrite the problem in simpler words before guessing a tool.</p>"
    )


def enrich_checklist_item(item: str) -> str:
    core = _plain(item)
    skill = core[2:] if core.lower().startswith("i ") else core
    return (
        f"<p><strong>Goal:</strong> {core}</p>"
        f"<p><em>How I prove I am ready:</em> I can teach &quot;{skill}&quot; with a tiny example, "
        f"explain why each step is allowed, and name a common trap.</p>"
        f"<p><em>30-second self-test:</em> Cover the solved examples. Can I restate the idea, invent one Easy "
        f"example, and spot one rushed mistake? If not, return to the walkthroughs before the 5 quick problems.</p>"
    )


def why_box(title: str, body: str) -> str:
    return callout("Why this matters", title, enrich_why(body), "#f0f9ff", "#7dd3fc")


def think_box(title: str, body: str) -> str:
    return callout("How to think about it", title, enrich_think(body), "#f5f3ff", "#c4b5fd")


def watch_out(title: str, body: str) -> str:
    return callout("Watch out", title, enrich_watch(title, body), "#fffbeb", "#fcd34d")


def strategy_tip(title: str, body: str) -> str:
    return callout("Test strategy", title, enrich_strategy(title, body), "#ecfdf5", "#6ee7b7")


def check_yourself(items) -> str:
    lis = "".join(
        f'<li style="background:#e0f2fe;border-radius:10px;padding:12px 14px;margin:10px 0;">'
        f"{enrich_checklist_item(i)}</li>"
        for i in items
    )
    return (
        '<div style="background:#f8fafc;border:1px dashed #94a3b8;border-radius:12px;'
        'padding:16px;margin:16px 0;">'
        "<h4>Check yourself before moving on</h4>"
        "<p>Do not just nod at these. For each bullet, speak an example out loud. "
        "If you cannot, go back to the solved examples before the quick practice.</p>"
        f"<ul style='list-style:none;padding-left:0;'>{lis}</ul>"
        "</div>"
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
        "<li><strong>Problems 1–15:</strong> Easy / skill builders &amp; early chapter checks</li>"
        "<li><strong>Problems 16–30:</strong> Medium / mixed quiz &amp; homework style</li>"
        "<li><strong>Problems 31–40:</strong> Hard / chapter test &amp; multi-step</li>"
        "<li><strong>Problems 41–50:</strong> Stretch / honors Algebra 2 &amp; early Precalculus / SAT Math</li>"
        "</ul>"
        "<p>Take your time. Algebra 2 skill is built by explaining each transformation out loud.</p>"
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
    bridge = (
        "<p><strong>Before the examples:</strong> Read each walkthrough like a tutor is beside you. "
        "Pause after every step and ask “Why is this step legal?” "
        "Examples get harder on purpose so you see the same idea under more pressure.</p>"
    )
    after = (
        "<p><strong>After the examples:</strong> Cover the final answers and reteach one Easy and one Hard example "
        "without looking. Then read the Watch out and Test strategy boxes carefully — they are full explanations, "
        "not slogans. Only then attempt the 5 quick problems.</p>"
    )
    parts = [
        page_break(),
        f"<h2>{title}</h2>",
        p(*intro_paras),
        why_box("Keep this in mind", why),
        think_box("A clear plan", think),
        bridge,
        examples_html,
        after,
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
<p>This unit is written for <strong>10th-grade Algebra 2</strong> students. We go slowly and explain every idea
in clear language with LaTeX. Read each section fully. Do the 5 quick problems after each idea.
Then finish the 50-problem set at the end (Easy → Stretch).</p>
{why_box("You are building lasting skill",
    "Algebra 2 is the bridge from Algebra 1 procedures to Precalculus and college math. "
    "If you understand why each rewrite is legal, hard multi-step problems stop feeling like magic.")}
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
