"""Shared helpers for high-school master courses (Algebra 1 through AP Calculus)."""

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


def end_practice_heading(stretch_label: str = "Stretch / honors &amp; SAT Math") -> str:
    return (
        "<h2>Full Practice Set (25 Problems)</h2>"
        "<p>These get harder as you go — all on this unit's topic:</p>"
        "<ul>"
        "<li><strong>Problems 1–8:</strong> Medium warm-ups</li>"
        "<li><strong>Problems 9–16:</strong> Hard / chapter test style</li>"
        f"<li><strong>Problems 17–25:</strong> {stretch_label}</li>"
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


def practice_slots(start: int, count: int = 25, stretch_label: str | None = None) -> str:
    heading = end_practice_heading(stretch_label) if stretch_label else end_practice_heading()
    return heading + "\n" + "\n".join(quiz_slot(i) for i in range(start, start + count))


def unit_shell(title: str, audience: str, roadmap_items, body_html: str, final_slots_html: str, stretch_note: str | None = None) -> str:
    stretch = stretch_note or "a very hard stretch — all on this unit's topic"
    return f"""
<h1>{title}</h1>
<p><strong>Audience:</strong> {audience}</p>
<p>Each idea is explained in clear language with LaTeX, then shown in fully worked examples with a diagram
that matches that idea. After the examples you will see a common mistake, then 5 quick problems.
A 25-problem set at the end climbs from medium to {stretch}.</p>
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


def xy_graph(curves=None, points=None, dashes=None, xlim=(-6, 6), ylim=(-6, 6), w=300, h=300, xlab="x", ylab="y"):
    """Compact axes + polylines. curves: [(color, [(x,y), ...])]; dashes: [('v'|'h', val, label)]."""
    pad = 24
    x0, x1 = xlim
    y0, y1 = ylim

    def X(x):
        return pad + (x - x0) / (x1 - x0) * (w - 2 * pad)

    def Y(y):
        return h - pad - (y - y0) / (y1 - y0) * (h - 2 * pad)

    bits = [
        f'<line x1="{pad}" y1="{Y(0) if y0 <= 0 <= y1 else h - pad}" x2="{w - pad}" y2="{Y(0) if y0 <= 0 <= y1 else h - pad}" stroke="#0f172a" stroke-width="1.6"/>'
        if y0 <= 0 <= y1 else f'<line x1="{pad}" y1="{h - pad}" x2="{w - pad}" y2="{h - pad}" stroke="#0f172a" stroke-width="1.6"/>',
        f'<line x1="{X(0) if x0 <= 0 <= x1 else pad}" y1="{pad}" x2="{X(0) if x0 <= 0 <= x1 else pad}" y2="{h - pad}" stroke="#0f172a" stroke-width="1.6"/>'
        if x0 <= 0 <= x1 else f'<line x1="{pad}" y1="{pad}" x2="{pad}" y2="{h - pad}" stroke="#0f172a" stroke-width="1.6"/>',
        f'<text x="{w - pad}" y="{(Y(0) if y0 <= 0 <= y1 else h - pad) - 6}" font-size="11">{xlab}</text>',
        f'<text x="{(X(0) if x0 <= 0 <= x1 else pad) + 6}" y="{pad + 4}" font-size="11">{ylab}</text>',
    ]
    for kind, val, lab in (dashes or []):
        col = "#dc2626" if kind == "v" else "#2563eb"
        if kind == "v":
            bits.append(f'<line x1="{X(val):.1f}" y1="{pad}" x2="{X(val):.1f}" y2="{h - pad}" stroke="{col}" stroke-width="1.5" stroke-dasharray="5 4"/>')
            bits.append(f'<text x="{X(val) + 4:.1f}" y="{pad + 12}" font-size="11" fill="{col}">{lab}</text>')
        else:
            bits.append(f'<line x1="{pad}" y1="{Y(val):.1f}" x2="{w - pad}" y2="{Y(val):.1f}" stroke="{col}" stroke-width="1.5" stroke-dasharray="5 4"/>')
            bits.append(f'<text x="{pad + 4}" y="{Y(val) - 4:.1f}" font-size="11" fill="{col}">{lab}</text>')

    def path_for(pts, color, sw=2):
        segs, cur = [], []
        for x, y in pts:
            if x0 - 0.2 <= x <= x1 + 0.2 and y0 - 0.2 <= y <= y1 + 0.2 and abs(y) < 1e8:
                cur.append((x, y))
            else:
                if len(cur) >= 2:
                    segs.append(cur)
                cur = []
        if len(cur) >= 2:
            segs.append(cur)
        out = []
        for seg in segs:
            d = " ".join(("M" if i == 0 else "L") + f"{X(px):.1f},{Y(py):.1f}" for i, (px, py) in enumerate(seg))
            out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}"/>')
        return "".join(out)

    for color, pts in (curves or []):
        bits.append(path_for(pts, color))
    for item in (points or []):
        x, y, lab = item[0], item[1], item[2] if len(item) > 2 else ""
        col = item[3] if len(item) > 3 else "#b91c1c"
        bits.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="4.2" fill="{col}"/>')
        if lab:
            bits.append(f'<text x="{X(x) + 7:.1f}" y="{Y(y) - 6:.1f}" font-size="11" fill="{col}">{lab}</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">{"".join(bits)}</svg>'


def sample_curve(fn, a, b, n=56, skip=()):
    out = []
    for i in range(n + 1):
        x = a + (b - a) * i / n
        if any(abs(x - s) < 0.12 for s in skip):
            out.append((x, 1e9))
            continue
        try:
            out.append((x, fn(x)))
        except (ZeroDivisionError, ValueError, OverflowError):
            out.append((x, 1e9))
    return out


def number_line(lo, hi, closed=(), opened=(), shade=None, w=460):
    h, left, right, y = 78, 28, w - 28, 36
    n = max(hi - lo, 1)

    def xp(v):
        return left + (v - lo) * (right - left) / n

    ticks = []
    for v in range(lo, hi + 1):
        x = xp(v)
        ticks.append(f'<line x1="{x:.1f}" y1="{y - 7}" x2="{x:.1f}" y2="{y + 7}" stroke="#0f172a" stroke-width="2"/>')
        ticks.append(f'<text x="{x:.1f}" y="{y + 22}" text-anchor="middle" font-size="11">{v}</text>')
    extra = []
    if shade:
        kind = shade[0]
        if kind == "out":
            extra.append(f'<line x1="{left}" y1="{y}" x2="{xp(shade[1]):.1f}" y2="{y}" stroke="#7c3aed" stroke-width="6"/>')
            extra.append(f'<line x1="{xp(shade[2]):.1f}" y1="{y}" x2="{right}" y2="{y}" stroke="#7c3aed" stroke-width="6"/>')
        elif kind == "right":
            extra.append(f'<line x1="{xp(shade[1]):.1f}" y1="{y}" x2="{right}" y2="{y}" stroke="#7c3aed" stroke-width="6"/>')
        elif kind == "left":
            extra.append(f'<line x1="{left}" y1="{y}" x2="{xp(shade[1]):.1f}" y2="{y}" stroke="#7c3aed" stroke-width="6"/>')
        elif kind == "between":
            extra.append(f'<line x1="{xp(shade[1]):.1f}" y1="{y}" x2="{xp(shade[2]):.1f}" y2="{y}" stroke="#7c3aed" stroke-width="6"/>')
    dots = []
    for v, lab in closed:
        dots.append(f'<circle cx="{xp(v):.1f}" cy="{y}" r="6" fill="#dc2626"/>')
        if lab:
            dots.append(f'<text x="{xp(v):.1f}" y="{y - 14}" text-anchor="middle" font-size="11" fill="#b91c1c">{lab}</text>')
    for v, lab in opened:
        dots.append(f'<circle cx="{xp(v):.1f}" cy="{y}" r="6" fill="#fff" stroke="#dc2626" stroke-width="2.5"/>')
        if lab:
            dots.append(f'<text x="{xp(v):.1f}" y="{y - 14}" text-anchor="middle" font-size="11" fill="#b91c1c">{lab}</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img"><line x1="{left}" y1="{y}" x2="{right}" y2="{y}" stroke="#0f172a" stroke-width="2"/>{"".join(ticks)}{"".join(extra)}{"".join(dots)}</svg>'


def argand(points, lim=6, w=300):
    return xy_graph(points=points, xlim=(-lim, lim), ylim=(-lim, lim), w=w, h=w, xlab="real", ylab="imag")


def fill_qs(qs, need, factory):
    while len(qs) < need:
        qs.append(factory(len(qs) + 1))
    return renumber(qs[:need])


def labeled_right_triangle(a=3, b=4, c=5, a_lab="a", b_lab="b", c_lab="c", angle_lab="θ", w=280, h=200):
    """Right triangle on the x-axis. Right angle at the origin-like corner.

    Vertical leg `a` is opposite `angle_lab`, which sits at the bottom-right vertex
    (not on the right-angle square). Horizontal leg `b` is adjacent to that angle.
    """
    pad, base = 36, min(w, h) - 70
    scale = base / max(a, b, 1)
    x0, y0 = pad + 10, h - pad
    x1, y1 = x0 + b * scale, y0
    x2, y2 = x0, y0 - a * scale
    sq = 14
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<polygon points="{x0:.1f},{y0:.1f} {x1:.1f},{y1:.1f} {x2:.1f},{y2:.1f}" '
        f'fill="#eef2ff" stroke="#312e81" stroke-width="2.2"/>'
        f'<rect x="{x0:.1f}" y="{y0 - sq:.1f}" width="{sq}" height="{sq}" fill="none" stroke="#312e81" stroke-width="1.6"/>'
        f'<text x="{(x0 + x2) / 2 - 14:.1f}" y="{(y0 + y2) / 2:.1f}" font-size="13">{a_lab}</text>'
        f'<text x="{(x0 + x1) / 2:.1f}" y="{y0 + 18:.1f}" text-anchor="middle" font-size="13">{b_lab}</text>'
        f'<text x="{(x1 + x2) / 2 + 8:.1f}" y="{(y1 + y2) / 2:.1f}" font-size="13">{c_lab}</text>'
        f'<text x="{x1 - 22:.1f}" y="{y1 - 16:.1f}" font-size="13" fill="#b91c1c">{angle_lab}</text>'
        f"</svg>"
    )


def unit_circle_svg(deg=60, w=280):
    """Unit circle with one ray at `deg` and the point (cos, sin) marked."""
    import math as _m
    pad, r = 28, (w - 56) / 2
    cx = cy = w / 2
    th = _m.radians(deg)
    px = cx + r * _m.cos(th)
    py = cy - r * _m.sin(th)
    return (
        f'<svg viewBox="0 0 {w} {w}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#f8fafc" stroke="#0f172a" stroke-width="1.8"/>'
        f'<line x1="{cx - r}" y1="{cy}" x2="{cx + r}" y2="{cy}" stroke="#0f172a" stroke-width="1.2"/>'
        f'<line x1="{cx}" y1="{cy - r}" x2="{cx}" y2="{cy + r}" stroke="#0f172a" stroke-width="1.2"/>'
        f'<line x1="{cx}" y1="{cy}" x2="{px:.1f}" y2="{py:.1f}" stroke="#dc2626" stroke-width="2"/>'
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="#dc2626"/>'
        f'<text x="{px + 8:.1f}" y="{py - 6:.1f}" font-size="12" fill="#b91c1c">(cos {deg}°, sin {deg}°)</text>'
        f"</svg>"
    )


def parallel_lines_transversal(w=320, h=200):
    """Two parallel lines cut by a transversal, with one pair of corresponding angles marked."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="20" y1="70" x2="{w - 20}" y2="70" stroke="#1e3a8a" stroke-width="3"/>'
        f'<line x1="20" y1="140" x2="{w - 20}" y2="140" stroke="#1e3a8a" stroke-width="3"/>'
        f'<line x1="90" y1="30" x2="230" y2="180" stroke="#b91c1c" stroke-width="2.4"/>'
        f'<path d="M 118 70 A 18 18 0 0 1 132 82" fill="none" stroke="#f59e0b" stroke-width="2.5"/>'
        f'<path d="M 175 140 A 18 18 0 0 1 189 152" fill="none" stroke="#f59e0b" stroke-width="2.5"/>'
        f'<text x="128" y="62" font-size="12" fill="#b45309">1</text>'
        f'<text x="196" y="168" font-size="12" fill="#b45309">2</text>'
        f'<text x="{w - 70}" y="64" font-size="12">ℓ</text>'
        f'<text x="{w - 70}" y="134" font-size="12">m</text>'
        f"</svg>"
    )


def tangent_curve_svg(w=300, h=220):
    """y=x^2/4 style curve with a tangent at a marked point."""
    pts = []
    pad = 28
    for i in range(25):
        x = -3 + i * 0.25
        y = 0.25 * x * x
        X = pad + (x + 3) / 6 * (w - 2 * pad)
        Y = h - pad - (y + 0.2) / 3.2 * (h - 2 * pad)
        pts.append((X, Y))
    d = " ".join(("M" if i == 0 else "L") + f"{X:.1f},{Y:.1f}" for i, (X, Y) in enumerate(pts))
    # Point at x=2, y=1
    px = pad + (2 + 3) / 6 * (w - 2 * pad)
    py = h - pad - (1 + 0.2) / 3.2 * (h - 2 * pad)
    # Tangent slope = x/2 = 1 at x=2
    x1, x2 = px - 50, px + 50
    y1, y2 = py + 50, py - 50
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="{pad}" y1="{h - pad}" x2="{w - pad}" y2="{h - pad}" stroke="#0f172a"/>'
        f'<line x1="{pad}" y1="{pad}" x2="{pad}" y2="{h - pad}" stroke="#0f172a"/>'
        f'<path d="{d}" fill="none" stroke="#4f46e5" stroke-width="2.4"/>'
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#dc2626" stroke-width="2"/>'
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="#b91c1c"/>'
        f'<text x="{px + 8:.1f}" y="{py - 8:.1f}" font-size="12" fill="#b91c1c">P</text>'
        f"</svg>"
    )


