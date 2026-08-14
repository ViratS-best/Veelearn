"""Shared helpers for Grade 1 math: simple English, new embeds, quizzes."""

import html
import json
import urllib.parse


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


def encode_data(obj) -> str:
    return urllib.parse.quote(json.dumps(obj, ensure_ascii=True, separators=(",", ":")), safe="")


def kid_tip(title: str, body: str) -> str:
    return (
        '<div class="vl-callout vl-callout-mascot" data-vl-kind="mascot">'
        '<div class="vl-callout-icon">🌟</div>'
        f'<div class="vl-callout-body"><h4>{title}</h4><p>{body}</p></div></div>'
    )


def watch_out(title: str, body: str) -> str:
    return (
        '<div class="vl-callout vl-callout-trap" data-vl-kind="trap">'
        '<div class="vl-callout-icon">⚠️</div>'
        f'<div class="vl-callout-body"><h4>Watch out: {title}</h4><p>{body}</p></div></div>'
    )


def try_this(title: str, body: str) -> str:
    return (
        '<div class="vl-callout vl-callout-strategy" data-vl-kind="strategy">'
        '<div class="vl-callout-icon">💡</div>'
        f'<div class="vl-callout-body"><h4>{title}</h4><p>{body}</p></div></div>'
    )


def step_reveal(steps, prompt="", vid="", answer=""):
    steps = list(steps)
    data = encode_data(steps)
    prompt_attr = f' data-vl-prompt="{html.escape(prompt, quote=True)}"' if prompt else ""
    ans_attr = f' data-vl-answer="{html.escape(str(answer), quote=True)}"' if answer else ""
    id_attr = f' data-vl-id="{vid}"' if vid else ""
    preview = "".join(f"<li>{s}</li>" for s in steps)
    return (
        f'<div class="vl-step-reveal"{id_attr} data-vl-steps="{data}"{prompt_attr}{ans_attr}>'
        f'<div class="vl-embed-label">Tap to see each step</div>'
        f'<ol class="vl-step-preview">{preview}</ol></div>'
    )


def matching(pairs, vid=""):
    data = encode_data([{"left": a, "right": b} for a, b in pairs])
    items = "".join(f"<li>{a} ↔ {b}</li>" for a, b in pairs)
    id_attr = f' data-vl-id="{vid}"' if vid else ""
    return (
        f'<div class="vl-matching"{id_attr} data-vl-pairs="{data}">'
        f'<div class="vl-embed-label">Match the pairs</div>'
        f'<ul class="vl-match-preview">{items}</ul></div>'
    )


def phet(title: str, url: str, kid_line: str) -> str:
    return (
        f'<div class="phet-sim-wrapper" style="border:1px solid #ddd;border-radius:12px;'
        f'overflow:hidden;background:#fff;margin:16px 0;">'
        f'<div style="background:#eef2ff;padding:12px 14px;font-weight:800;">🎮 Play: {title}</div>'
        f"<p style=\"padding:0 14px;\">{kid_line}</p>"
        f'<div style="position:relative;padding-bottom:62%;height:0;overflow:hidden;">'
        f'<iframe src="{url}" title="{title}" style="position:absolute;top:0;left:0;width:100%;'
        f'height:100%;border:0;" allowfullscreen loading="lazy"></iframe></div></div>'
    )


PHET = {
    "play": (
        "Number Play",
        "https://phet.colorado.edu/sims/html/number-play/latest/number-play_all.html",
        "Tap the toys and count. Say each number out loud.",
    ),
    "compare": (
        "Number Compare",
        "https://phet.colorado.edu/sims/html/number-compare/latest/number-compare_all.html",
        "Look at two groups. Which has more? Which has less?",
    ),
    "pairs": (
        "Number Pairs",
        "https://phet.colorado.edu/sims/html/number-pairs/latest/number-pairs_all.html",
        "Find two parts that make a whole number. This helps you add.",
    ),
    "ten": (
        "Make a Ten",
        "https://phet.colorado.edu/sims/html/make-a-ten/latest/make-a-ten_all.html",
        "Move ones to make a ten. Tens make adding easier!",
    ),
    "area": (
        "Area Builder",
        "https://phet.colorado.edu/sims/html/area-builder/latest/area-builder_all.html",
        "Cover a shape with same-size squares. Count how many you used.",
    ),
}


def phet_box(key: str) -> str:
    title, url, line = PHET[key]
    return phet(title, url, line)


def solved(num, problem, steps, answer, note=""):
    steps_html = "".join(f"<li>{s}</li>" for s in steps)
    note_html = f"<p><em>{note}</em></p>" if note else ""
    return (
        '<div style="background:#f8fafc;border:1px solid #cbd5e1;border-radius:12px;'
        'padding:18px;margin:18px 0;">'
        f"<h4>Let's try one together ({num})</h4>"
        f"<p><strong>Problem:</strong> {problem}</p>"
        f"<p><strong>Think it through:</strong></p><ol>{steps_html}</ol>"
        f'<p><strong>Answer:</strong> <span style="background:#dcfce7;padding:3px 10px;'
        f'border-radius:6px;font-weight:700;">{answer}</span></p>{note_html}</div>'
    )


def mini_practice(name: str) -> str:
    return (
        f"<h3>Quick check — {name}</h3>"
        "<p>Tap an answer. If you miss, try again. You have hearts to help you.</p>"
    )


def end_practice() -> str:
    return (
        "<h2>Big practice (50 problems)</h2>"
        "<p>Start easy. Then they get a little trickier. Take your time. Count with your fingers if you need to.</p>"
        "<ul>"
        "<li><strong>1–15:</strong> Warm-up</li>"
        "<li><strong>16–30:</strong> A little harder</li>"
        "<li><strong>31–40:</strong> Think twice</li>"
        "<li><strong>41–50:</strong> Super thinker</li>"
        "</ul>"
    )


def practice_slots(start: int, count: int = 50) -> str:
    return end_practice() + "\n" + "\n".join(quiz_slot(i) for i in range(start, start + count))


def concept_block(
    title: str,
    intro_paras,
    examples_html: str,
    extras="",
    quiz_start=None,
):
    if quiz_start is None:
        if isinstance(extras, int):
            quiz_start = extras
            extras = ""
        else:
            raise TypeError("concept_block needs quiz_start")
    parts = [
        page_break(),
        f"<h2>{title}</h2>",
        p(*intro_paras),
        examples_html,
        extras or "",
        mini_practice(title),
        slots_range(quiz_start, 5),
    ]
    return "\n".join(part for part in parts if part)


def unit_shell(title: str, roadmap_items, body_html: str, final_slots_html: str) -> str:
    return f"""
<h1>{title}</h1>
<p>This is <strong>first grade math</strong>. We use short words. We count. We draw pictures in our heads.</p>
<p>After each idea you get 5 quick questions. At the end you get a big practice set.</p>
<h2>What we will learn</h2>
{ol(roadmap_items)}
{body_html}
{final_slots_html}
"""


def make_question(text, correct, distractors, explanation, idx, points=1):
    opts = [str(correct)] + [str(d) for d in distractors[:3]]
    unique = []
    for opt in opts:
        if opt not in unique:
            unique.append(opt)
    while len(unique) < 4:
        filler = str(len(unique) + 11)
        if str(correct).lstrip("-").isdigit():
            try:
                filler = str(int(float(correct)) + len(unique) * 2 + 3)
            except ValueError:
                filler = f"Choice {len(unique) + 1}"
        if filler not in unique and filler != str(correct):
            unique.append(filler)
    return {
        "question_text": text,
        "question_type": "multiple_choice",
        "options": unique[:4],
        "correct_answer": str(correct),
        "explanation": explanation,
        "points": points,
        "order_index": idx,
    }


def near_int(correct, count=3):
    c = int(correct)
    pool = []
    for delta in (1, -1, 2, -2, 3, 10, -10, 5, c + 1 if c < 119 else 118):
        v = c + delta
        if v != c and v >= 0:
            pool.append(str(v))
    unique = []
    for pval in pool:
        if pval not in unique:
            unique.append(pval)
        if len(unique) >= count:
            break
    while len(unique) < count:
        filler = str(c + 7 + len(unique))
        if filler != str(c) and filler not in unique:
            unique.append(filler)
    return unique[:count]


def mq(text, correct, explanation, idx, distractors=None):
    if distractors is not None:
        d = distractors
    elif str(correct).lstrip("-").isdigit():
        d = near_int(correct)
    else:
        d = ["Not sure", "None of these", "Skip"]
        d = [x for x in d if x != str(correct)][:3]
    return make_question(text, correct, d, explanation, idx)


def renumber(questions):
    out = []
    for i, q in enumerate(questions, 1):
        qq = dict(q)
        qq["order_index"] = i
        out.append(qq)
    return out
