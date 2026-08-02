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
        "<p><strong>Why contests care:</strong> MathCounts and AMC problems are written to punish rushed guesses. "
        "If you understand <em>why</em> a counting step is legal, you can adapt when the problem adds a twist "
        "(like distinct, at least one, or no leading zero). Memorizing a formula without the why breaks on the twist.</p>"
        "<p><strong>What good looks like:</strong> You can explain the idea to a classmate in plain English, "
        "give a tiny example with numbers under 10, and point to which rule you used (multiply, add, subtract, or divide).</p>"
        "<p><strong>Practice habit:</strong> After each solved example, cover the answer and reteach the steps out loud. "
        "If you get stuck naming a step, reread that part before the quick practice problems.</p>"
    )


def enrich_think(short: str) -> str:
    core = _plain(short)
    return (
        f"<p><strong>Your plan on paper:</strong> {core}</p>"
        "<p><strong>Step-by-step routine (do this every time):</strong></p>"
        "<ol>"
        "<li>Write one sentence: <em>I am counting ___</em> (name the object clearly).</li>"
        "<li>Underline constraints: distinct? order matter? leading zeros? at least?</li>"
        "<li>Choose the tool: product slots, disjoint cases, complement, combinations, permutations, stars and bars, or PIE.</li>"
        "<li>Compute slowly and box middle results so you do not lose a factor.</li>"
        "<li>Sanity-check: is the size reasonable? Would a tiny version of this problem give an answer you can list?</li>"
        "</ol>"
        "<p><strong>If you feel stuck:</strong> Shrink the numbers (replace 10 digits by 3, replace committee of 4 by committee of 2) "
        "and list by hand. The tiny list tells you which tool is correct, then scale back up to the real numbers.</p>"
    )


def _watch_extra(title: str) -> str:
    t = title.lower()
    if "outline" in t or "skipping" in t:
        return (
            "<p><strong>What \"outline\" means here:</strong> Before any multiply/subtract, write 2–4 short lines naming "
            "the layers. Example for \"codes of length 6 with at least one zero\": "
            "<em>(1) Total distinct 6-digit codes from 0–9 = $P(10,6)$.</em> "
            "<em>(2) Bad = no zeros = $P(9,6)$.</em> "
            "<em>(3) Good = Total − Bad.</em> "
            "Only after those three lines exist do you plug in numbers.</p>"
            "<p><strong>What goes wrong without it:</strong> Students often compute only Total, or only Bad, or they "
            "multiply Total by something random. On a Target/National layered problem, one missing layer usually costs "
            "the whole point — and you cannot recover in the last 20 seconds.</p>"
            "<p><strong>Tiny drill:</strong> Take any hard problem in this unit, cover the solution, and force yourself "
            "to write the outline first. Time the outline alone (aim under 30 seconds). That habit is the real skill.</p>"
        )
    if "overcount" in t or "divide" in t or "identical" in t:
        return (
            "<p><strong>Extra detail for this trap:</strong> Ask the swap test out loud: \"If I swap two of the things "
            "I chose, is it a new answer?\" If no, you probably need combinations or a divide-by-$k!$. "
            "Ask the label test: \"Do the groups have names (Team A vs Team B)?\" Unlabeled pairs often need ÷2.</p>"
        )
    if "zero" in t or "leading" in t:
        return (
            "<p><strong>Extra detail for this trap:</strong> Digits that form a <em>number</em> usually forbid a leading "
            "zero. Digits that form a <em>code, PIN, or license plate</em> often allow zeros in every position. "
            "Underline the word \"number\" vs \"code\" in the problem statement before you fill the first slot.</p>"
        )
    if "case" in t or "overlap" in t or "miss" in t:
        return (
            "<p><strong>Extra detail for this trap:</strong> Write case names in words first (\"exactly 1 red\", "
            "\"exactly 2 red\"…). Check that every legal outcome sits in exactly one case — no gaps, no double homes. "
            "If two cases can both claim the same outcome, you are double-counting.</p>"
        )
    return (
        "<p><strong>Extra detail:</strong> Re-read the trap name, then invent a 10-second story of a student who falls "
        "for it. If you can tell that story, you will notice the trap earlier on contest day.</p>"
    )


def _strategy_extra(title: str) -> str:
    t = title.lower()
    if "box" in t or "intermediate" in t or "audit" in t:
        return (
            "<p><strong>Why boxing matters on layered problems:</strong> A National-style count might need "
            "Total, Bad, Case 1, Case 2, and a final Good. If those five numbers live only in your head, one of them "
            "will mutate while you finish the arithmetic. Boxes turn the scratch paper into an audit trail you can "
            "re-check in 10 seconds.</p>"
            "<p><strong>How to box (exact habit):</strong> Draw a rectangle, write a label on the left "
            "(<code>Total</code>, <code>Bad</code>, <code>Paths via C</code>), write the number inside, and never erase "
            "a box — cross it out and rewrite if wrong. When you combine, point to each box with your pencil and say "
            "the operation: \"Good equals Total minus Bad.\"</p>"
            "<p><strong>Full micro-walkthrough:</strong> Distinct length-6 digit strings with at least one zero. "
            "Box 1: <code>Total = P(10,6) = 10×9×8×7×6×5</code>. Multiply in order: "
            "$10×9=90$, $90×8=720$, $720×7=5040$, $5040×6=30240$, $30240×5=151200$. "
            "Box 2: <code>Bad (no zero) = P(9,6) = 9×8×7×6×5×4 = 60480</code>. "
            "Box 3: <code>Good = 151200 − 60480 = 90720</code>. "
            "Without boxes, people often report 151200 or 60480 as the final answer by accident.</p>"
        )
    if "complement" in t or "total" in t or "bad" in t:
        return (
            "<p><strong>Complement playbook:</strong> Write three labeled boxes every time — Total, Bad, Good — "
            "even when the problem feels easy. The boxes force you to define \"bad\" in words before you compute it. "
            "If you cannot define bad cleanly, complement is the wrong tool.</p>"
        )
    if "tiny" in t or "small" in t or "shrink" in t:
        return (
            "<p><strong>Shrink-to-check playbook:</strong> Replace big parameters with tiny ones that keep the same "
            "structure (committee of 5 from 12 → committee of 2 from 4). List by hand. If your formula disagrees with "
            "the hand list, fix the formula before scaling back up.</p>"
        )
    if "tool" in t or "chooser" in t or "decision" in t or "picker" in t:
        return (
            "<p><strong>Tool-chooser playbook:</strong> Ask in order: (1) Order matter? (2) Identical objects? "
            "(3) \"At least\" / \"none\" suggesting complement? (4) Overlapping properties suggesting PIE? "
            "(5) Paths/tilings suggesting binomials or recursion? Write the chosen tool name before calculating.</p>"
        )
    return (
        "<p><strong>Make the play automatic:</strong> Say the strategy name, write it at the top of your scratch paper, "
        "then execute the numbered steps above without skipping. Contests reward habits more than last-second inspiration.</p>"
    )


def enrich_watch(title: str, short: str) -> str:
    core = _plain(short)
    return (
        f"<p><strong>The trap called &quot;{title}&quot;:</strong> {core}</p>"
        "<p><strong>Why this trap shows up so often:</strong> Under time pressure, your brain wants to jump straight to "
        "multiplying or dividing because that feels like real math. But most counting mistakes happen <em>before</em> "
        "the arithmetic — when the plan is vague, when two cases accidentally overlap, or when identical objects are "
        "treated as distinct (or the reverse).</p>"
        f"{_watch_extra(title)}"
        "<p><strong>Warning signs you hit the trap:</strong> your answer is exactly 2× too big or too small, off by a "
        "factor of $k!$, includes impossible leading zeros, or is not an integer on AMC 8 (answers must be integers 0–999).</p>"
        "<p><strong>How to dodge it:</strong></p>"
        "<ul>"
        "<li>Say the object you are counting in a full sentence before any calculation.</li>"
        "<li>Swap test: if I swap two chosen people, is it a new outcome? (Yes → permutation thinking; no → combination.)</li>"
        "<li>Label test: are rooms/teams/seats labeled? (No labels often means divide by 2.)</li>"
        "<li>Zero test: is this a number (no leading zero) or a code (zeros often allowed)?</li>"
        "</ul>"
        "<p><strong>Repair move:</strong> Do not erase blindly. Write a corrected outline beside the old work, then recompute. "
        "Comparing the two outlines teaches you faster than starting from a blank page.</p>"
    )


def enrich_strategy(title: str, short: str) -> str:
    core = _plain(short)
    return (
        f"<p><strong>Strategy — {title}:</strong> {core}</p>"
        "<p><strong>How to use it on MathCounts / AMC:</strong> Treat this like a coach play, not a two-word slogan. "
        "Practice the play slowly in this lesson until it feels automatic. On Sprint/AMC 8 you will only have seconds "
        "to choose it; on Target/Team/National you should write the play in words first, then execute.</p>"
        f"{_strategy_extra(title)}"
        "<p><strong>Concrete scratch-paper actions:</strong></p>"
        "<ol>"
        f"<li>Write the strategy name at the top: {title}.</li>"
        "<li>List the pieces you must not lose (slots, cases, path legs, intermediate totals).</li>"
        "<li>Box every intermediate number and label it clearly (Total, Bad, Good, Case 1, Case 2, Paths to C).</li>"
        "<li>Only then combine boxed numbers with $+$, ×, or $-$.</li>"
        "<li>Finish with a 5-second check: Does the size make sense? Did I answer the object from my first sentence?</li>"
        "</ol>"
        "<p><strong>Worked micro-example of boxing:</strong> Suppose Total $=720$ and Bad $=504$. "
        "Write <code>Total = 720</code> and <code>Bad = 504</code> in boxes, then Good $=720-504=216$. "
        "If you skip boxing on a layered problem, it is easy to reuse 720 by mistake or subtract the wrong piece.</p>"
        "<p><strong>When to move on:</strong> If after about 60–90 seconds on Sprint you still cannot name what you are counting, "
        "skip and return later. A blank beats a confident wrong tool.</p>"
    )


def enrich_checklist_item(item: str) -> str:
    core = _plain(item)
    skill = core[2:] if core.lower().startswith("i ") else core
    return (
        f"<p><strong>Goal:</strong> {core}</p>"
        f"<p><em>How I prove I am ready:</em> I can teach &quot;{skill}&quot; using a tiny example with numbers under 10, "
        f"explain why each step is allowed, and name a common trap that makes people miss it.</p>"
        f"<p><em>30-second self-test:</em> Cover the solved examples above. Can I restate the idea, invent one Easy "
        f"example, and spot one mistake a rushed student would make? If not, I return to the walkthroughs before the "
        f"5 quick problems — guessing through the quiz does not build contest skill.</p>"
    )


def why_box(title: str, body: str) -> str:
    return callout("Why this matters", title, enrich_why(body), "#f0f9ff", "#7dd3fc")


def think_box(title: str, body: str) -> str:
    return callout("How to think about it", title, enrich_think(body), "#f5f3ff", "#c4b5fd")


def watch_out(title: str, body: str) -> str:
    return callout("Watch out", title, enrich_watch(title, body), "#fffbeb", "#fcd34d")


def strategy_tip(title: str, body: str) -> str:
    return callout("Contest strategy", title, enrich_strategy(title, body), "#ecfdf5", "#6ee7b7")


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
        "<p>Do not just nod at these. For each bullet, actually speak an example out loud. "
        "If you cannot, go back to the solved examples — the quick practice will feel unfair until the idea is clear.</p>"
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
    bridge = (
        "<p><strong>Before the examples:</strong> Read each walkthrough like a coach is beside you. "
        "Pause after every step and ask “Why is this step allowed?” "
        "The examples get harder on purpose so you can see the same idea under more pressure.</p>"
    )
    after = (
        "<p><strong>After the examples:</strong> Cover the final answers and reteach one Easy and one Hard example "
        "without looking. Then read the Watch out and Contest strategy boxes carefully — they are written as full "
        "explanations, not slogans. Only then attempt the 5 quick problems.</p>"
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
