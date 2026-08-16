"""Shared helpers for Grade 5 math: simple English, sparse diagrams, quizzes."""

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
    "arith": (
        "Arithmetic",
        "https://phet.colorado.edu/sims/html/arithmetic/latest/arithmetic_all.html",
        "Try multiply and divide. Watch how the numbers change.",
    ),
    "area_mult": (
        "Area Model Multiplication",
        "https://phet.colorado.edu/sims/html/area-model-multiplication/latest/area-model-multiplication_all.html",
        "Split a big rectangle into tens and ones. Multiply each part, then add.",
    ),
    "area_dec": (
        "Area Model Decimals",
        "https://phet.colorado.edu/sims/html/area-model-decimals/latest/area-model-decimals_all.html",
        "Tenths, hundredths, and thousandths can fill a grid. That is how decimals work.",
    ),
    "frac_eq": (
        "Fractions: Equality",
        "https://phet.colorado.edu/sims/html/fractions-equality/latest/fractions-equality_all.html",
        "Two fractions can name the same amount. Match equal pieces.",
    ),
    "build_frac": (
        "Build a Fraction",
        "https://phet.colorado.edu/sims/html/build-a-fraction/latest/build-a-fraction_all.html",
        "Build unit fractions and mixed numbers with equal pieces.",
    ),
    "frac_mixed": (
        "Fractions: Mixed Numbers",
        "https://phet.colorado.edu/sims/html/fractions-mixed-numbers/latest/fractions-mixed-numbers_all.html",
        "Build a mixed number. See how wholes and leftover parts sit together.",
    ),
}


def phet_box(key: str) -> str:
    title, url, line = PHET[key]
    return phet(title, url, line)


def figure(title: str, inner_html: str, caption: str = "") -> str:
    cap = f'<p style="margin:10px 0 0;font-size:0.95rem;color:#334155;">{caption}</p>' if caption else ""
    return (
        '<div class="vl-figure" style="background:#fff;border:1px solid #cbd5e1;border-radius:12px;'
        'padding:14px 16px;margin:18px 0;max-width:560px;">'
        f'<div style="font-weight:800;color:#312e81;margin-bottom:10px;">{title}</div>'
        f"{inner_html}{cap}</div>"
    )


def place_value_thousandths(ones="2", tenths="4", hundredths="0", thousandths="7") -> str:
    cell = (
        "border:1px solid #94a3b8;padding:10px 12px;text-align:center;"
        "min-width:72px;font-size:1.15rem;"
    )
    head = cell + "background:#eef2ff;font-weight:700;font-size:0.85rem;"
    body = cell + "background:#fff;font-weight:800;"
    table = (
        '<table style="border-collapse:collapse;margin:0 auto;">'
        "<tr>"
        f'<th style="{head}">ones</th>'
        f'<th style="{head}">.</th>'
        f'<th style="{head}">tenths</th>'
        f'<th style="{head}">hundredths</th>'
        f'<th style="{head}">thousandths</th>'
        "</tr><tr>"
        f'<td style="{body}">{ones}</td>'
        f'<td style="{body}">.</td>'
        f'<td style="{body}">{tenths}</td>'
        f'<td style="{body}">{hundredths}</td>'
        f'<td style="{body}">{thousandths}</td>'
        "</tr></table>"
    )
    return figure(
        "Place-value chart (through thousandths)",
        table,
        f"This number is {ones}.{tenths}{hundredths}{thousandths}. "
        "Each place is 10 times the place on its right.",
    )


def fraction_bars(rows, caption="") -> str:
    """rows: list of (label, parts_filled, parts_total, color)."""
    bars = []
    for label, filled, total, color in rows:
        cells = []
        w = max(12, int(280 / total))
        for i in range(total):
            bg = color if i < filled else "#f8fafc"
            cells.append(
                f'<span style="display:inline-block;width:{w}px;height:28px;border:1px solid #334155;'
                f'background:{bg};box-sizing:border-box;"></span>'
            )
        bars.append(
            f'<div style="margin:8px 0;"><span style="display:inline-block;width:52px;font-weight:700;">'
            f"{label}</span>{''.join(cells)}</div>"
        )
    return figure("Same-size wholes, different pieces", "".join(bars), caption)


def volume_prism(length=4, width=3, height=2) -> str:
    svg = f"""
<svg viewBox="0 0 280 210" width="280" height="210" role="img" aria-label="Rectangular prism {length} by {width} by {height}">
  <polygon points="70,70 190,70 230,30 110,30" fill="#c7d2fe" stroke="#312e81" stroke-width="2"/>
  <polygon points="190,70 230,30 230,130 190,170" fill="#818cf8" stroke="#312e81" stroke-width="2"/>
  <polygon points="70,70 190,70 190,170 70,170" fill="#e0e7ff" stroke="#312e81" stroke-width="2"/>
  <text x="130" y="188" text-anchor="middle" font-size="14" fill="#1e293b">length = {length}</text>
  <text x="238" y="108" font-size="14" fill="#1e293b">w = {width}</text>
  <text x="18" y="128" font-size="14" fill="#1e293b">h = {height}</text>
</svg>
"""
    return figure(
        "A rectangular prism",
        svg,
        f"Volume = length × width × height = {length} × {width} × {height} = {length * width * height} cubic units.",
    )


_plane_seq = 0


def coordinate_plane(points=None, xmax=6, ymax=6, title="The coordinate plane", caption=""):
    """First-quadrant grid. points: list of (x, y, label) or (x, y)."""
    global _plane_seq
    _plane_seq += 1
    marker = f"vl-arrow-{_plane_seq}"
    ox, oy = 48, 300
    scale = 36
    w = ox + xmax * scale + 44
    h = oy + 36
    lines = []
    for i in range(xmax + 1):
        x = ox + i * scale
        lines.append(f'<line x1="{x}" y1="{oy - ymax * scale}" x2="{x}" y2="{oy}" stroke="#cbd5e1" stroke-width="1"/>')
        if i:
            lines.append(f'<text x="{x}" y="{oy + 16}" text-anchor="middle" font-size="12" fill="#334155">{i}</text>')
    for j in range(ymax + 1):
        y = oy - j * scale
        lines.append(f'<line x1="{ox}" y1="{y}" x2="{ox + xmax * scale}" y2="{y}" stroke="#cbd5e1" stroke-width="1"/>')
        if j:
            lines.append(f'<text x="{ox - 14}" y="{y + 4}" text-anchor="end" font-size="12" fill="#334155">{j}</text>')
    axes = (
        f'<line x1="{ox}" y1="{oy}" x2="{ox + xmax * scale + 18}" y2="{oy}" stroke="#0f172a" stroke-width="2" marker-end="url(#{marker})"/>'
        f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy - ymax * scale - 18}" stroke="#0f172a" stroke-width="2" marker-end="url(#{marker})"/>'
        f'<text x="{ox + xmax * scale + 26}" y="{oy + 4}" font-size="14" font-weight="700" fill="#1e3a8a">x</text>'
        f'<text x="{ox - 6}" y="{oy - ymax * scale - 24}" text-anchor="middle" font-size="14" font-weight="700" fill="#1e3a8a">y</text>'
        f'<text x="{ox - 10}" y="{oy + 16}" text-anchor="end" font-size="12" fill="#64748b">0</text>'
    )
    dots = []
    for pt in points or []:
        x, y = pt[0], pt[1]
        label = pt[2] if len(pt) > 2 else f"({x}, {y})"
        px = ox + x * scale
        py = oy - y * scale
        dots.append(f'<circle cx="{px}" cy="{py}" r="6" fill="#dc2626"/>')
        dots.append(
            f'<text x="{px + 10}" y="{py - 8}" font-size="13" font-weight="700" fill="#7f1d1d">{html.escape(label)}</text>'
        )
    svg = f"""
<svg viewBox="0 0 {w} {h}" width="{min(w, 420)}" role="img" aria-label="{html.escape(title)}">
  <defs>
    <marker id="{marker}" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="#0f172a"/>
    </marker>
  </defs>
  {''.join(lines)}
  {axes}
  {''.join(dots)}
</svg>
"""
    default_cap = (
        "An ordered pair is (x, y). Start at the origin (0, 0). "
        "Go right for x, then up for y."
    )
    return figure(title, svg, caption or default_cap)


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
        "<h2>Big practice (25 problems)</h2>"
        "<p>Start easy. Then they get a little trickier. Take your time. Line up decimals, find a common denominator, or sketch a grid if you need to.</p>"
        "<ul>"
        "<li><strong>1–15:</strong> Warm-up</li>"
        "<li><strong>16–30:</strong> A little harder</li>"
        "<li><strong>31–40:</strong> Think twice</li>"
        "<li><strong>41–50:</strong> Super thinker</li>"
        "</ul>"
    )


def practice_slots(start: int, count: int = 25) -> str:
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
<p>This is <strong>fifth grade math</strong>. You are building a strong base for middle school. We work with fractions, decimals to the thousandths place, multi-digit operations, volume, and the coordinate plane.</p>
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
        if str(correct).lstrip("-$¢").replace(".", "", 1).replace("/", "", 1).isdigit():
            try:
                core = str(correct).replace("$", "").replace("¢", "").replace(":", "")
                filler = str(int(float(core.split("/")[0])) + len(unique) * 2 + 3)
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
    for delta in (1, -1, 2, -2, 10, -10, 100, -100, 5, 20, -20, 50, 1000, -1000):
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


def fill_qs(qs, need, factory):
    while len(qs) < need:
        qs.append(factory(len(qs) + 1))
    return renumber(qs[:need])
