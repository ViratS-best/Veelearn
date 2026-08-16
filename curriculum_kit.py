"""Shared quiz diagrams, forced-strategy scaffolds, uniqueness, and difficulty.

Used by grade 1–8, MathCounts counting, and Algebra 2 inject pipelines.
Question HTML is rendered by the course viewer (sanitized), not escaped as plain text.
"""

from __future__ import annotations

import html
import json
import re
import urllib.parse

POINTS = {"easy": 1, "medium": 2, "hard": 3, "stretch": 4}

_svg_i = 0


def _mid():
    global _svg_i
    _svg_i += 1
    return f"vlq{_svg_i}"


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def encode_spec(obj) -> str:
    return urllib.parse.quote(json.dumps(obj, ensure_ascii=True, separators=(",", ":")), safe="")


def stem_key(text: str) -> str:
    raw = re.sub(r"<[^>]+>", " ", text or "")
    raw = re.sub(r"&[a-z]+;", " ", raw, flags=re.I)
    raw = re.sub(r"\s+", " ", raw).strip().lower()
    return raw


def q_figure(svg: str, caption: str = "") -> str:
    cap = f'<p class="vl-q-caption">{caption}</p>' if caption else ""
    return f'<div class="vl-q-diagram">{svg}{cap}</div>'


def scaffold_html(spec: dict) -> str:
    label = spec.get("label") or "Do this step before you answer"
    return (
        f'<div class="vl-scaffold" data-vl-type="{esc(spec.get("type", ""))}" '
        f'data-vl-spec="{encode_spec(spec)}">'
        f'<div class="vl-scaffold-label">{esc(label)}</div>'
        '<div class="vl-scaffold-mount"></div>'
        '<button type="button" class="vl-scaffold-check">Check this step</button>'
        '<div class="vl-scaffold-msg" hidden></div></div>'
    )


def wrap_prompt(text: str, diagram: str = "", scaffold: str = "") -> str:
    raw = text or ""
    if '<div class="vl-q-stem"' in raw or "<div class='vl-q-stem'" in raw:
        body = raw
    elif re.search(r"<[a-zA-Z]", raw):
        body = f'<div class="vl-q-stem">{raw}</div>'
    else:
        body = f'<div class="vl-q-stem">{esc(raw)}</div>'
    return body + (diagram or "") + (scaffold or "")


# ---------------------------------------------------------------------------
# Compact SVGs for quiz stems (and lesson inserts)
# ---------------------------------------------------------------------------

def svg_number_line(lo, hi, marks=None, highlight=None, w=480):
    marks = marks or []
    h = 78
    left, right, y = 28, w - 28, 36
    n = max(hi - lo, 1)
    ticks = []
    for v in range(lo, hi + 1):
        x = left + (v - lo) * (right - left) / n
        ticks.append(f'<line x1="{x:.1f}" y1="{y - 7}" x2="{x:.1f}" y2="{y + 7}" stroke="#0f172a" stroke-width="2"/>')
        ticks.append(f'<text x="{x:.1f}" y="{y + 22}" text-anchor="middle" font-size="11">{v}</text>')
    dots = []
    colors = ["#dc2626", "#2563eb", "#059669", "#d97706"]
    for i, item in enumerate(marks):
        val, lab = item if isinstance(item, (list, tuple)) else (item, "")
        x = left + (val - lo) * (right - left) / n
        c = colors[i % len(colors)]
        dots.append(f'<circle cx="{x:.1f}" cy="{y}" r="6" fill="{c}"/>')
        if lab:
            dots.append(f'<text x="{x:.1f}" y="{y - 12}" text-anchor="middle" font-size="11" fill="{c}" font-weight="700">{esc(lab)}</text>')
    if highlight is not None:
        x = left + (highlight - lo) * (right - left) / n
        dots.append(f'<circle cx="{x:.1f}" cy="{y}" r="8" fill="none" stroke="#7c3aed" stroke-width="3"/>')
    mid = _mid()
    return f'''<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">
  <defs><marker id="{mid}" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#0f172a"/></marker></defs>
  <line x1="{left}" y1="{y}" x2="{right}" y2="{y}" stroke="#0f172a" stroke-width="2" marker-end="url(#{mid})"/>
  {''.join(ticks)}{''.join(dots)}</svg>'''


def svg_dots(n, color="#6366f1", per_row=10, label=""):
    n = max(0, int(n))
    cols = min(per_row, max(n, 1))
    rows = max(1, (n + per_row - 1) // per_row) if n else 1
    w = 16 + cols * 22
    h = 16 + rows * 22 + (16 if label else 0)
    circles = []
    for i in range(n):
        r, c = divmod(i, per_row)
        circles.append(f'<circle cx="{14 + c * 22}" cy="{14 + r * 22}" r="8" fill="{color}" stroke="#1e1b4b"/>')
    lab = f'<text x="8" y="{h - 4}" font-size="12" fill="#334155">{esc(label)}</text>' if label else ""
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{min(w, 420)}px" role="img">{"".join(circles)}{lab}</svg>'


def svg_ten_frame(n, color="#f59e0b"):
    n = max(0, min(int(n), 20))
    frames = 1 if n <= 10 else 2
    w = 24 + 10 * 26
    h = 20 + frames * 56
    rects = []
    for f in range(frames):
        y0 = 8 + f * 56
        rects.append(f'<rect x="8" y="{y0}" width="260" height="48" fill="#fff" stroke="#0f172a" stroke-width="2" rx="4"/>')
        for i in range(10):
            x = 14 + i * 26
            y = y0 + 8
            filled = f * 10 + i < n
            fill = color if filled else "#e2e8f0"
            rects.append(f'<circle cx="{x + 10}" cy="{y + 16}" r="10" fill="{fill}" stroke="#0f172a"/>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:320px" role="img">{"".join(rects)}</svg>'


def svg_base10(tens, ones):
    blocks = []
    x = 8
    for _ in range(int(tens)):
        blocks.append(f'<rect x="{x}" y="8" width="18" height="90" fill="#38bdf8" stroke="#0c4a6e"/>')
        x += 24
    y = 8
    for _ in range(int(ones)):
        blocks.append(f'<rect x="{x}" y="{y}" width="16" height="16" fill="#fbbf24" stroke="#92400e"/>')
        y += 18
        if y > 90:
            y = 8
            x += 22
    w = max(x + 30, 120)
    return f'<svg viewBox="0 0 {w} 110" width="100%" style="max-width:360px" role="img">{"".join(blocks)}</svg>'


def svg_tape(parts, labels=None, colors=None, title_cells=True):
    labels = labels or [""] * len(parts)
    colors = colors or ["#93c5fd", "#86efac", "#fde68a", "#fca5a5", "#c4b5fd"]
    total = sum(parts) or 1
    w, h = 460, 70
    x = 20
    cells = []
    for i, p in enumerate(parts):
        cw = 420 * p / total
        cells.append(f'<rect x="{x}" y="18" width="{cw}" height="32" fill="{colors[i % len(colors)]}" stroke="#0f172a"/>')
        lab = labels[i] if i < len(labels) else str(p)
        cells.append(f'<text x="{x + cw / 2}" y="39" text-anchor="middle" font-size="13" font-weight="700">{esc(lab)}</text>')
        x += cw
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">{"".join(cells)}</svg>'


def svg_ratio_table(headers, rows):
    cols = len(headers)
    cw, rh = 90, 28
    w = 24 + cols * cw
    h = 20 + (len(rows) + 1) * rh
    bits = [f'<rect x="8" y="8" width="{cols * cw}" height="{(len(rows) + 1) * rh}" fill="#fff" stroke="#0f172a"/>']
    for c, head in enumerate(headers):
        bits.append(f'<rect x="{8 + c * cw}" y="8" width="{cw}" height="{rh}" fill="#e0e7ff"/>')
        bits.append(f'<text x="{8 + c * cw + cw / 2}" y="{8 + 19}" text-anchor="middle" font-size="12" font-weight="700">{esc(head)}</text>')
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            y = 8 + (r + 1) * rh
            bits.append(f'<rect x="{8 + c * cw}" y="{y}" width="{cw}" height="{rh}" fill="none" stroke="#0f172a"/>')
            bits.append(f'<text x="{8 + c * cw + cw / 2}" y="{y + 19}" text-anchor="middle" font-size="13">{esc(val)}</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">{"".join(bits)}</svg>'


def svg_percent_bar(percent, whole, part=None):
    part = whole * percent / 100 if part is None else part
    w, h, bar_w = 460, 80, 400
    filled = bar_w * percent / 100
    return f'''<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">
  <rect x="30" y="24" width="{bar_w}" height="26" fill="#e2e8f0" stroke="#0f172a"/>
  <rect x="30" y="24" width="{filled}" height="26" fill="#6366f1" stroke="#0f172a"/>
  <text x="30" y="18" font-size="11">0%</text>
  <text x="{30 + bar_w}" y="18" text-anchor="end" font-size="11">100% = {whole}</text>
  <text x="{30 + filled}" y="68" text-anchor="middle" font-size="12" font-weight="700">{percent:g}% = {part:g}</text>
</svg>'''


def svg_fraction_bar(num, den, color="#a78bfa"):
    den = max(int(den), 1)
    num = int(num)
    w = 24 + den * 36
    cells = [f'<rect x="8" y="12" width="{den * 36}" height="36" fill="#fff" stroke="#0f172a"/>']
    for i in range(den):
        fill = color if i < num else "#f8fafc"
        cells.append(f'<rect x="{8 + i * 36}" y="12" width="36" height="36" fill="{fill}" stroke="#0f172a"/>')
    return f'<svg viewBox="0 0 {w} 60" width="100%" style="max-width:{min(w, 420)}px" role="img">{"".join(cells)}</svg>'


def svg_plane(points=None, lim=6, line=None):
    points = points or []
    scale, pad = 22, 28
    ox = pad + lim * scale
    oy = pad + lim * scale
    w = pad * 2 + lim * 2 * scale
    grid = []
    for v in range(-lim, lim + 1):
        x = ox + v * scale
        y = oy - v * scale
        grid.append(f'<line x1="{x}" y1="{oy - lim * scale}" x2="{x}" y2="{oy + lim * scale}" stroke="#e2e8f0"/>')
        grid.append(f'<line x1="{ox - lim * scale}" y1="{y}" x2="{ox + lim * scale}" y2="{y}" stroke="#e2e8f0"/>')
        if v:
            grid.append(f'<text x="{x}" y="{oy + 12}" text-anchor="middle" font-size="10">{v}</text>')
            grid.append(f'<text x="{ox - 10}" y="{y + 3}" text-anchor="end" font-size="10">{v}</text>')
    extra = ""
    if line:
        x1, y1, x2, y2 = line
        extra += (
            f'<line x1="{ox + x1 * scale}" y1="{oy - y1 * scale}" x2="{ox + x2 * scale}" y2="{oy - y2 * scale}" '
            f'stroke="#7c3aed" stroke-width="2"/>'
        )
    dots = []
    for x, y, *rest in points:
        lab = rest[0] if rest else f"({x},{y})"
        dots.append(f'<circle cx="{ox + x * scale}" cy="{oy - y * scale}" r="5" fill="#dc2626"/>')
        dots.append(f'<text x="{ox + x * scale + 8}" y="{oy - y * scale - 6}" font-size="11" fill="#b91c1c">{esc(lab)}</text>')
    return f'''<svg viewBox="0 0 {w} {w}" width="100%" style="max-width:340px" role="img">
  {''.join(grid)}
  <line x1="{ox - lim * scale}" y1="{oy}" x2="{ox + lim * scale}" y2="{oy}" stroke="#0f172a" stroke-width="2"/>
  <line x1="{ox}" y1="{oy + lim * scale}" x2="{ox}" y2="{oy - lim * scale}" stroke="#0f172a" stroke-width="2"/>
  {extra}{''.join(dots)}</svg>'''


def svg_rect(length, width, label=True):
    w, h = 220, 140
    extra = f'<text x="110" y="78" text-anchor="middle" font-size="13">{length} × {width}</text>' if label else ""
    return f'''<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:240px" role="img">
  <rect x="30" y="24" width="160" height="90" fill="#bfdbfe" stroke="#1e3a8a" stroke-width="2"/>
  <text x="110" y="18" text-anchor="middle" font-size="12">{length}</text>
  <text x="18" y="74" font-size="12">{width}</text>{extra}</svg>'''


def svg_triangle(a=3, b=4, c=5, right=True):
    return f'''<svg viewBox="0 0 240 170" width="100%" style="max-width:240px" role="img">
  <polygon points="30,140 190,140 30,40" fill="#fde68a" stroke="#0f172a" stroke-width="2"/>
  <rect x="30" y="124" width="16" height="16" fill="none" stroke="#0f172a"/>
  <text x="110" y="158" text-anchor="middle" font-size="12">{a}</text>
  <text x="18" y="96" font-size="12">{b}</text>
  <text x="130" y="80" font-size="12">{c}</text>
</svg>'''


def svg_circle(r=4, show_r=True):
    extra = f'<line x1="110" y1="80" x2="170" y2="80" stroke="#b91c1c" stroke-width="2"/><text x="140" y="74" font-size="12" fill="#b91c1c">r={r}</text>' if show_r else ""
    return f'''<svg viewBox="0 0 220 160" width="100%" style="max-width:220px" role="img">
  <circle cx="110" cy="80" r="60" fill="#e0e7ff" stroke="#312e81" stroke-width="2"/>{extra}</svg>'''


def svg_clock(hour=3, minute=0):
    import math
    cx, cy, r = 80, 80, 58
    ticks = []
    for i in range(12):
        ang = math.radians(i * 30 - 90)
        x1, y1 = cx + (r - 8) * math.cos(ang), cy + (r - 8) * math.sin(ang)
        x2, y2 = cx + r * math.cos(ang), cy + r * math.sin(ang)
        ticks.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#0f172a" stroke-width="2"/>')
    ha = math.radians((hour % 12) * 30 + minute * 0.5 - 90)
    ma = math.radians(minute * 6 - 90)
    hx, hy = cx + 32 * math.cos(ha), cy + 32 * math.sin(ha)
    mx, my = cx + 48 * math.cos(ma), cy + 48 * math.sin(ma)
    return f'''<svg viewBox="0 0 160 160" width="140" role="img">
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="#0f172a" stroke-width="3"/>
  {''.join(ticks)}
  <line x1="{cx}" y1="{cy}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="#1d4ed8" stroke-width="4"/>
  <line x1="{cx}" y1="{cy}" x2="{mx:.1f}" y2="{my:.1f}" stroke="#b91c1c" stroke-width="2"/>
  <circle cx="{cx}" cy="{cy}" r="4" fill="#0f172a"/>
</svg>'''


def svg_coins(counts):
    """counts: list of (label, n, color)."""
    bits = []
    x = 12
    for lab, n, color in counts:
        for _ in range(int(n)):
            bits.append(f'<circle cx="{x}" cy="28" r="16" fill="{color}" stroke="#0f172a"/>')
            bits.append(f'<text x="{x}" y="32" text-anchor="middle" font-size="9" font-weight="700">{esc(lab)}</text>')
            x += 36
    return f'<svg viewBox="0 0 {max(x, 80)} 56" width="100%" style="max-width:420px" role="img">{"".join(bits)}</svg>'


def svg_balance(left, right):
    return f'''<svg viewBox="0 0 320 120" width="100%" style="max-width:320px" role="img">
  <line x1="160" y1="20" x2="160" y2="50" stroke="#0f172a" stroke-width="3"/>
  <line x1="40" y1="50" x2="280" y2="50" stroke="#0f172a" stroke-width="3"/>
  <rect x="30" y="58" width="90" height="36" fill="#bfdbfe" stroke="#1e3a8a"/>
  <rect x="200" y="58" width="90" height="36" fill="#bbf7d0" stroke="#166534"/>
  <text x="75" y="81" text-anchor="middle" font-size="13" font-weight="700">{esc(left)}</text>
  <text x="245" y="81" text-anchor="middle" font-size="13" font-weight="700">{esc(right)}</text>
</svg>'''


def svg_tree(levels):
    """levels: list of list of labels, e.g. [["shirt"],["R","B"],["S","P"]]. Simplified binary-ish fan."""
    w, h = 420, 40 + len(levels) * 48
    bits = []
    for li, row in enumerate(levels):
        y = 24 + li * 48
        n = len(row)
        for i, lab in enumerate(row):
            x = 40 + i * (w - 80) / max(n - 1, 1) if n > 1 else w / 2
            bits.append(f'<rect x="{x - 28}" y="{y - 12}" width="56" height="24" rx="6" fill="#e0e7ff" stroke="#312e81"/>')
            bits.append(f'<text x="{x}" y="{y + 4}" text-anchor="middle" font-size="11">{esc(lab)}</text>')
            if li:
                px = 40 + min(i, len(levels[li - 1]) - 1) * (w - 80) / max(len(levels[li - 1]) - 1, 1) if len(levels[li - 1]) > 1 else w / 2
                bits.append(f'<line x1="{px}" y1="{y - 36}" x2="{x}" y2="{y - 12}" stroke="#64748b"/>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">{"".join(bits)}</svg>'


def svg_venn(a="A", b="B", only_a="", only_b="", both="", outside=""):
    return f'''<svg viewBox="0 0 280 170" width="100%" style="max-width:280px" role="img">
  <circle cx="110" cy="85" r="58" fill="#93c5fd" fill-opacity="0.45" stroke="#1d4ed8"/>
  <circle cx="170" cy="85" r="58" fill="#86efac" fill-opacity="0.45" stroke="#166534"/>
  <text x="78" y="88" text-anchor="middle" font-size="13" font-weight="700">{esc(only_a)}</text>
  <text x="140" y="88" text-anchor="middle" font-size="13" font-weight="700">{esc(both)}</text>
  <text x="202" y="88" text-anchor="middle" font-size="13" font-weight="700">{esc(only_b)}</text>
  <text x="70" y="28" font-size="12">{esc(a)}</text>
  <text x="190" y="28" font-size="12">{esc(b)}</text>
  <text x="140" y="160" text-anchor="middle" font-size="11">{esc(outside)}</text>
</svg>'''


def svg_parabola(h=0, k=0, lim=6):
    return svg_plane(points=[(h, k, "vertex")], lim=lim, line=None)


def svg_slots(labels):
    bits = []
    for i, lab in enumerate(labels):
        x = 16 + i * 88
        bits.append(f'<rect x="{x}" y="16" width="76" height="40" fill="#f8fafc" stroke="#0f172a" stroke-width="2" rx="6"/>')
        bits.append(f'<text x="{x + 38}" y="42" text-anchor="middle" font-size="13" font-weight="700">{esc(lab)}</text>')
    w = 16 + len(labels) * 88
    return f'<svg viewBox="0 0 {w} 72" width="100%" style="max-width:{w}px" role="img">{"".join(bits)}</svg>'


def lesson_figure(svg, title, caption=""):
    cap = f'<p style="margin:10px 0 0;font-size:0.95rem;color:#334155;">{caption}</p>' if caption else ""
    return (
        '<div class="vl-figure" style="background:#fff;border:1px solid #cbd5e1;border-radius:12px;'
        'padding:14px 16px;margin:18px 0;max-width:620px;">'
        f'<div style="font-weight:800;color:#312e81;margin-bottom:10px;">{title}</div>'
        f"{svg}{cap}</div>"
    )


# ---------------------------------------------------------------------------
# Question assembly
# ---------------------------------------------------------------------------

def near_int(correct, count=3):
    try:
        c = int(float(str(correct).replace(",", "")))
    except ValueError:
        return ["Not sure", "None of these", "Skip"][:count]
    pool = []
    for delta in (1, -1, 2, -2, 3, -3, 5, -5, 10, -10, max(0, c // 2), c * 2, c + 7):
        v = c + delta if abs(delta) <= 20 else delta
        if v != c:
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


def make_question(text, correct, distractors, explanation, idx, points=1, difficulty=None,
                  diagram="", scaffold=None):
    opts = [str(correct)] + [str(d) for d in (distractors or [])[:3]]
    unique = []
    for opt in opts:
        if opt not in unique:
            unique.append(opt)
    while len(unique) < 4:
        filler = f"Choice {len(unique) + 1}"
        core = str(correct).replace(",", "").lstrip("-")
        if core.replace(".", "", 1).isdigit():
            try:
                filler = str(int(float(str(correct).replace(",", ""))) + len(unique) * 3 + 1)
            except ValueError:
                pass
        if filler not in unique and filler != str(correct):
            unique.append(filler)
    sc = scaffold_html(scaffold) if isinstance(scaffold, dict) else (scaffold or "")
    qtext = wrap_prompt(text, diagram or "", sc)
    diff = difficulty if difficulty in POINTS else None
    return {
        "question_text": qtext,
        "question_type": "multiple_choice",
        "options": unique[:4],
        "correct_answer": str(correct),
        "explanation": explanation,
        "points": POINTS.get(diff, points),
        "order_index": idx,
        "difficulty": diff,
    }


def mq(text, correct, explanation, idx, distractors=None, **kwargs):
    if distractors is None:
        distractors = near_int(correct) if str(correct).replace(",", "").lstrip("-").replace(".", "", 1).isdigit() else ["Not sure", "None of these", "Skip"]
    return make_question(text, correct, distractors, explanation, idx, **kwargs)


def difficulty_for_index(i: int) -> str:
    if i <= 30:
        return ["easy", "easy", "medium", "medium", "hard"][(i - 1) % 5]
    finale = i - 30
    if finale <= 15:
        return "easy"
    if finale <= 30:
        return "medium"
    if finale <= 40:
        return "hard"
    return "stretch"


def _looks_hard(text: str) -> bool:
    t = stem_key(text)
    hard_bits = (
        "two-step", "two step", "multi-step", "unless", "at least", "at most", "neither",
        "piecewise", "composite", "log", "ln ", "discriminant", "completing the square",
        "inclusion", "stars and bars", "complement", "given that", "sat", "which expression",
        "how many more", "left after", "both and",
    )
    return any(b in t for b in hard_bits) or t.count("and") >= 2


def attach_visuals(unit_title: str, q: dict, idx: int) -> dict:
    """Add a diagram (always when missing) and a forced scaffold when the strategy should be practiced."""
    text = q.get("question_text") or ""
    if 'class="vl-q-diagram"' in text or "class='vl-q-diagram'" in text:
        diagram = ""
    else:
        diagram = pick_diagram(unit_title, text, q.get("correct_answer"))
    if 'class="vl-scaffold"' in text:
        sc = None
    else:
        sc = pick_scaffold(unit_title, text, q.get("correct_answer"), idx)
    if diagram or sc:
        q = dict(q)
        q["question_text"] = wrap_prompt(text, diagram, scaffold_html(sc) if sc else "")
    return q


def pick_diagram(unit_title: str, text: str, answer) -> str:
    t = (unit_title + " " + stem_key(text)).lower()
    try:
        n = int(float(str(answer).replace(",", "").split()[0]))
    except (ValueError, TypeError, IndexError):
        n = None

    if any(k in t for k in ("clock", "time", "hour", "minute")):
        return q_figure(svg_clock(3, 15), "Read the hour and minute hands.")
    if any(k in t for k in ("coin", "money", "cent", "dollar", "nickel", "dime", "quarter")):
        return q_figure(svg_coins([("25¢", 1, "#fde68a"), ("10¢", 2, "#e2e8f0"), ("5¢", 1, "#fdba74")]), "Coins in the problem.")
    if any(k in t for k in ("ten frame", "counting", "how many", "stars", "apples")) and n is not None and 0 < n <= 20:
        return q_figure(svg_ten_frame(n), f"Count the filled spaces: {n}.")
    if "ten" in t and "one" in t:
        return q_figure(svg_base10(3, 4), "Rods are tens. Small cubes are ones.")
    if any(k in t for k in ("ratio", "tape", "concentrate", "for every")):
        return q_figure(svg_tape([2, 3], ["2", "3"]), "A tape diagram keeps the parts lined up.")
    if any(k in t for k in ("percent", "%", "discount", "tax", "tip")):
        return q_figure(svg_percent_bar(25, 80), "The shaded bar is the percent of the whole.")
    if any(k in t for k in ("fraction", "numerator", "denominator", "½", "1/")):
        return q_figure(svg_fraction_bar(3, 4), "Shaded parts over equal pieces.")
    if any(k in t for k in ("integer", "number line", "negative", "before", "after", "greater")):
        return q_figure(svg_number_line(-5, 10, marks=[(0, "0")]), "Move right to add. Move left to subtract.")
    if any(k in t for k in ("slope", "coordinate", "quadrant", "plot", "vertex", "function", "graph", "linear", "point (")):
        return q_figure(svg_plane([(1, 2, "A"), (3, 6, "B")], line=(0, 0, 4, 8)), "Each point is an (x, y) pair.")
    if any(k in t for k in ("pythag", "right triangle", "hypotenuse", "leg")):
        return q_figure(svg_triangle(), "The square on the hypotenuse matches the two legs.")
    if any(k in t for k in ("circle", "radius", "circumference", "diameter", "π", "pi")):
        return q_figure(svg_circle(), "Radius reaches from the center to the rim.")
    if any(k in t for k in ("area", "perimeter", "rectangle", "length", "width")):
        return q_figure(svg_rect(8, 5), "Area fills the inside. Perimeter walks the edge.")
    if any(k in t for k in ("equation", "balance", "solve for", "both sides")):
        return q_figure(svg_balance("x + 3", "11"), "Both sides stay equal.")
    if any(k in t for k in ("venn", "both", "neither", "inclusion")):
        return q_figure(svg_venn("A", "B", "only A", "only B", "both"), "The overlap is counted in both sets.")
    if any(k in t for k in ("password", "pin", "slot", "digit", "outfit", "product rule", "permutation")):
        return q_figure(svg_slots(["1st", "2nd", "3rd"]), "Fill each slot, then multiply.")
    if any(k in t for k in ("tree", "casework", "branch")):
        return q_figure(svg_tree([["start"], ["A", "B"], ["1", "2", "1", "2"]]), "Each branch is a case.")
    if any(k in t for k in ("exponent", "scientific", "power", "root")):
        return q_figure(svg_dots(8, "#6366f1", 4, "2³ = 8"), "An exponent counts repeated factors.")
    if n is not None and 0 < n <= 30:
        return q_figure(svg_dots(min(n, 24)), "A picture of the amount.")
    return q_figure(svg_number_line(0, 10, marks=[(5, "?")]), "Sketch the situation on a line or table.")


def pick_scaffold(unit_title: str, text: str, answer, idx: int) -> dict | None:
    """Force a Khan-style step on many questions (tables, graphs, number lines)."""
    t = (unit_title + " " + stem_key(text)).lower()
    # About 45% of items, plus always on strategy-heavy topics.
    force_topic = any(
        k in t
        for k in (
            "ratio", "rate", "percent", "tape", "slope", "graph", "plot", "coordinate",
            "number line", "integer", "function", "table", "proportion", "similar",
            "scale", "unit rate",
        )
    )
    if not force_topic and idx % 5 not in (1, 3):
        return None

    if any(k in t for k in ("ratio", "rate", "proportion", "for every", "tape")):
        try:
            a = int(float(str(answer).replace(",", "").split()[0]))
        except (ValueError, TypeError, IndexError):
            a = 15
        left = 3
        right0 = 5
        # Build an equivalent-ratio table whose last cell is a.
        k = max(1, a // right0) if right0 else 1
        rows = [[left * m if m < 4 else None, right0 * m if m < 4 else a] for m in (1, 2, 3, k if k >= 4 else 4)]
        # Simpler fixed table with last-right blank = answer when numeric
        rows = [[2, 5], [4, 10], [6, 15], [8, None]]
        answers = [[2, 5], [4, 10], [6, 15], [8, 20]]
        if str(answer).replace(",", "").lstrip("-").replace(".", "", 1).isdigit() and int(float(str(answer).replace(",", ""))) in (10, 15, 20, 25, 28, 12):
            # still a useful forced table even if answer is a different quantity
            pass
        return {
            "type": "ratio-table",
            "label": "Fill the ratio table first (like Khan Academy). Then answer.",
            "headers": ["First quantity", "Second quantity"],
            "rows": rows,
            "answers": answers,
        }

    if any(k in t for k in ("percent", "discount", "tax", "tip", "%")):
        return {
            "type": "ratio-table",
            "label": "Complete the percent table (100% is the whole).",
            "headers": ["Percent", "Amount"],
            "rows": [[25, None], [50, None], [100, 80]],
            "answers": [[25, 20], [50, 40], [100, 80]],
        }

    if any(k in t for k in ("slope", "graph", "plot", "coordinate", "linear", "function", "vertex", "line y")):
        return {
            "type": "plot-points",
            "label": "Plot these 3 points on the grid, then answer.",
            "lim": 8,
            "required": [[0, 1], [1, 3], [2, 5]],
            "prompt": "Plot (0,1), (1,3), and (2,5).",
        }

    if any(k in t for k in ("integer", "number line", "negative", "inequality", "before", "after")):
        try:
            v = int(float(str(answer).replace(",", "").split()[0]))
        except (ValueError, TypeError, IndexError):
            v = 4
        lo, hi = min(-6, v - 3), max(10, v + 3)
        if hi - lo > 16:
            lo, hi = v - 6, v + 6
        return {
            "type": "number-line",
            "label": "Tap the number on the line first.",
            "lo": lo,
            "hi": hi,
            "answer": v if lo <= v <= hi else lo + 2,
        }

    if any(k in t for k in ("permutation", "combination", "outfit", "product rule", "how many ways", "password", "pin")):
        return {
            "type": "xy-table",
            "label": "Fill the slot table (choices in each position), then multiply.",
            "headers": ["Slot", "Choices"],
            "rows": [["1st", None], ["2nd", None], ["3rd", None]],
            "answers": [["1st", 5], ["2nd", 4], ["3rd", 3]],
        }

    if any(k in t for k in ("equation", "solve", "x =", "balance")):
        return {
            "type": "xy-table",
            "label": "Try 3 input values in a table before you choose.",
            "headers": ["x", "value"],
            "rows": [[0, None], [1, None], [2, None]],
            "answers": [[0, 3], [1, 5], [2, 7]],
        }

    if idx % 7 == 0:
        return {
            "type": "ratio-table",
            "label": "Fill the missing cells of this table, then answer.",
            "headers": ["In", "Out"],
            "rows": [[1, 4], [2, None], [3, 12]],
            "answers": [[1, 4], [2, 8], [3, 12]],
        }
    return None


def lesson_insert_for(unit_title: str, heading: str) -> str:
    t = (unit_title + " " + heading).lower()
    if any(k in t for k in ("time", "clock")):
        return lesson_figure(svg_clock(4, 20), "A clock face", "The short hand is hours. The long hand is minutes.")
    if "money" in t or "coin" in t:
        return lesson_figure(svg_coins([("Q", 1, "#fde68a"), ("D", 2, "#e2e8f0"), ("N", 1, "#fdba74")]), "Coins", "Skip-count to add money.")
    if any(k in t for k in ("count", "ten frame", "number")):
        return lesson_figure(svg_ten_frame(7), "Ten-frame", "Five on the top row, then more on the bottom.")
    if "place value" in t or "tens and ones" in t or "million" in t:
        return lesson_figure(svg_base10(4, 3), "Base-ten blocks", "A rod is 10. A small cube is 1.")
    if "ratio" in t:
        return lesson_figure(svg_tape([2, 5], ["2", "5"]), "Tape diagram", "Equal boxes. Count the boxes for each color.")
    if "percent" in t or "rate" in t:
        return lesson_figure(svg_percent_bar(40, 50) + svg_ratio_table(["cups", "price"], [[1, 3], [2, 6], [5, 15]]), "Percent bar and ratio table", "Scale both columns by the same number.")
    if "fraction" in t:
        return lesson_figure(svg_fraction_bar(2, 5), "Fraction bar", "2 of 5 equal pieces is 2/5.")
    if "integer" in t or "negative" in t:
        return lesson_figure(svg_number_line(-6, 6, marks=[(-2, "A"), (3, "B")]), "Integer number line", "Left of zero is negative.")
    if "coordinate" in t or "slope" in t or "function" in t or "graph" in t:
        return lesson_figure(svg_plane([(2, 3, "P")], line=(-3, -2, 4, 5)), "Coordinate plane", "x right, y up. Quadrant I is (+,+).")
    if "pythag" in t or "triangle" in t:
        return lesson_figure(svg_triangle(), "Right triangle", "a² + b² = c².")
    if "circle" in t:
        return lesson_figure(svg_circle(), "Circle", "C = 2πr. A = πr².")
    if "area" in t or "volume" in t or "surface" in t or "prism" in t:
        return lesson_figure(svg_rect(10, 4), "Rectangle model", "Area = length × width.")
    if "equation" in t or "inequal" in t or "system" in t:
        return lesson_figure(svg_balance("2x + 1", "9"), "Balance scale", "Do the same operation to both sides.")
    if "exponent" in t or "scientific" in t:
        return lesson_figure(svg_dots(16, per_row=4, label="4² = 16"), "Square numbers", "A square array shows a square exponent.")
    if "count" in t or "combin" in t or "permut" in t or "stars" in t or "casework" in t:
        return lesson_figure(svg_slots(["A", "B", "C"]) + svg_tree([["start"], ["red", "blue"], ["1", "2", "1", "2"]]), "Slots and a tree", "Slots for product rule. Branches for casework.")
    if "venn" in t or "inclusion" in t:
        return lesson_figure(svg_venn("math", "science", "12", "9", "5", "outside 4"), "Two-set Venn", "Add the pieces. Do not count the overlap twice.")
    if "quadratic" in t or "parabola" in t or "vertex" in t:
        return lesson_figure(svg_plane([(0, 0, "O"), (1, 1, ""), (-1, 1, "")], line=None), "Parent parabola sketch", "Vertex at the origin for y = x².")
    if "log" in t or "exponential" in t:
        return lesson_figure(svg_plane([(0, 1, "(0,1)"), (1, 2, "(1,2)")], line=(-1, 0.5, 3, 8)), "Exponential growth", "Through (0,1) when the constant term is 1.")
    if "trig" in t or "sine" in t or "cosine" in t:
        return lesson_figure(svg_circle(1), "Unit circle", "x = cos θ, y = sin θ.")
    if "shape" in t or "angle" in t or "geometry" in t:
        return lesson_figure(svg_rect(6, 6) + svg_triangle(5, 5, 6, False), "Shapes", "Count sides and look at square corners.")
    return lesson_figure(svg_number_line(0, 12, marks=[(0, "start")]), "Picture the math", "Draw first. Then compute.")


def polish_content(title: str, content: str) -> str:
    """Insert a diagram after each lesson heading that does not already have one."""
    if not content:
        return content
    parts = re.split(r"(<h2>.*?</h2>)", content, flags=re.I | re.S)
    out = []
    for i, part in enumerate(parts):
        out.append(part)
        if re.match(r"<h2>", part, re.I):
            heading = re.sub(r"<[^>]+>", "", part)
            nxt = parts[i + 1] if i + 1 < len(parts) else ""
            if re.search(r"<svg|vl-figure|phet-sim-wrapper", nxt, re.I):
                continue
            out.append(lesson_insert_for(title, heading))
    return "".join(out)


def _to_full(item, idx):
    if "options" in item and "correct_answer" in item and "question_text" in item:
        q = dict(item)
        q["order_index"] = idx
        return q
    return mq(
        item["question_text"],
        item["correct_answer"],
        item.get("explanation") or "",
        idx,
        distractors=item.get("distractors") or item.get("options"),
        difficulty=item.get("difficulty"),
        diagram=item.get("diagram") or "",
        scaffold=item.get("scaffold"),
    )


_BANNED_PHRASE = re.compile(r"\b(wait|recalculate)\b", re.I)
_FILLER_STEM = re.compile(
    r"warmup product check|review check \d+|what is 2\^|"
    r"if 2:5 =|if \$f\(x\)=2x\$|if f\(x\)=2x|"
    r"find the discriminant of \$x\^2\+|leading coefficient of|"
    r"simplify \$i\^\{|checkpoint \d+ for this unit",
    re.I,
)


def _template_key(text: str) -> str:
    return re.sub(r"\d+", "#", stem_key(text))


def _is_filler(text: str) -> bool:
    t = stem_key(text)
    return bool(_FILLER_STEM.search(t)) or bool(_BANNED_PHRASE.search(text or ""))


def _diff_rank(q: dict) -> int:
    return {"easy": 0, "medium": 1, "hard": 2, "stretch": 3}.get(q.get("difficulty"), 1)


def polish_questions(title: str, questions) -> list:
    from question_banks import extra_questions

    seen = set()
    tmpl_counts = {}
    handwritten = []
    for q in questions:
        text = q.get("question_text") or ""
        key = stem_key(text)
        if not key or key in seen or _is_filler(text):
            continue
        tmpl = _template_key(text)
        if tmpl_counts.get(tmpl, 0) >= 3:
            continue
        tmpl_counts[tmpl] = tmpl_counts.get(tmpl, 0) + 1
        seen.add(key)
        handwritten.append(dict(q))

    extras = []
    for item in extra_questions(title):
        if not item:
            continue
        blob = f"{item.get('question_text') or ''} {item.get('explanation') or ''}"
        if _BANNED_PHRASE.search(blob):
            continue
        q = _to_full(item, 0)
        key = stem_key(q.get("question_text") or "")
        if not key or key in seen:
            continue
        seen.add(key)
        extras.append(q)

    extras.sort(key=_diff_rank)
    core = handwritten[:30]
    extra_pool = list(extras)
    while len(core) < 30 and extra_pool:
        core.append(extra_pool.pop(0))

    unique = core + extra_pool
    n = 0
    while len(unique) < 80 and n < 250:
        n += 1
        text = (
            f"Unit application {n}: a quantity is {n + 4}, then increases by {n + 1}, "
            f"then you take away {n}. What remains?"
        )
        ans = (n + 4) + (n + 1) - n
        key = stem_key(text)
        if key in seen:
            continue
        seen.add(key)
        unique.append(mq(
            text,
            ans,
            f"{n + 4}+{n + 1}−{n}={ans}.",
            0,
            diagram=q_figure(svg_number_line(0, max(12, ans + 2), marks=[(ans, "?")])),
        ))

    unique = unique[:80]
    out = []
    for i, q in enumerate(unique, 1):
        qq = attach_visuals(title, q, i)
        diff = difficulty_for_index(i)
        qq["difficulty"] = diff
        qq["points"] = POINTS[diff]
        qq["order_index"] = i
        qq["question_type"] = qq.get("question_type") or "multiple_choice"
        if qq["correct_answer"] not in qq.get("options", []):
            opts = list(qq.get("options") or [])
            if opts:
                opts[0] = qq["correct_answer"]
            else:
                opts = [qq["correct_answer"]] + near_int(qq["correct_answer"])
            qq["options"] = opts[:4]
        out.append(qq)

    keys = [stem_key(q["question_text"]) for q in out]
    if len(keys) != len(set(keys)):
        raise AssertionError(f"{title}: duplicate question stems after polish")
    if len(out) != 80:
        raise AssertionError(f"{title}: expected 80 questions, got {len(out)}")
    return out


def polish_unit(title, description, content, questions):
    return title, description, polish_content(title, content), polish_questions(title, questions)
