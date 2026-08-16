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

# 6 concepts × 5 drills = 30, plus 25 progressive harder finale (not 50).
TARGET_QUESTIONS = 55
CONCEPT_QUESTIONS = 30
FINALE_QUESTIONS = TARGET_QUESTIONS - CONCEPT_QUESTIONS  # 25


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
    """Plausible wrong answers — never 'Not sure' / 'Skip' / 'None of these'."""
    raw = str(correct).strip()
    # Scientific notation: 3.2 × 10⁻³ or 3.2 x 10^-3 or LaTeX
    sci = re.search(
        r"([+-]?\d+(?:\.\d+)?)\s*(?:\\times|×|x|\*)\s*10\s*(?:\^|\{)?\s*([+-]?\d+)",
        raw.replace("−", "-").replace("{", "").replace("}", ""),
        re.I,
    )
    if sci:
        coef = float(sci.group(1))
        exp = int(sci.group(2))
        alts = [
            f"{coef} × 10^{exp + 1}",
            f"{coef} × 10^{exp - 1}",
            f"{coef * 10 if coef * 10 < 100 else coef / 10} × 10^{exp - 1 if coef * 10 >= 100 else exp}",
            f"{coef} × 10^{{-exp}}",
            f"{int(coef) if coef == int(coef) else coef} × 10^{exp + 2}",
        ]
        out = []
        for a in alts:
            if a != raw and a not in out:
                out.append(a)
            if len(out) >= count:
                return out[:count]
    try:
        c = int(float(raw.replace(",", "").replace("$", "")))
    except ValueError:
        # Symbolic / expression answers: mutate nearby common wrong forms
        pool = []
        plain = raw.replace("$", "").strip()
        if "/" in plain:
            pool.extend([plain[::-1] if len(plain) < 8 else plain, "1/" + plain.replace("1/", "")])
        # Common exponent mistakes
        m = re.search(r"([a-zA-Z0-9]+)\^\{?(\d+)\}?", plain)
        if m:
            base, exp = m.group(1), int(m.group(2))
            pool.extend([
                f"${base}^{{{exp + 1}}}$",
                f"${base}^{{{max(0, exp - 1)}}}$",
                f"${base}{exp}$",
                f"${base}^{{{exp * 2}}}$",
            ])
        if "\\times" in plain or "×" in plain:
            pool.extend([plain.replace("^{-", "^{"), plain + "0"])
        pool.extend(["0", "1", "-1", "undefined", plain + "x"])
        unique = []
        for pval in pool:
            pval = str(pval)
            if pval and pval != raw and pval != plain and pval not in unique:
                unique.append(pval)
            if len(unique) >= count:
                break
        while len(unique) < count:
            filler = f"{plain or 'ans'}-alt{len(unique)+1}"
            if filler not in unique:
                unique.append(filler)
        return unique[:count]
    pool = []
    for delta in (1, -1, 2, -2, 3, -3, 5, -5, 10, -10, max(0, c // 2), c * 2, c + 7, abs(c) - 1):
        v = c + delta if abs(delta) <= 20 or delta in (c * 2, max(0, c // 2), abs(c) - 1) else delta
        if isinstance(v, float):
            v = int(v)
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
        if opt not in unique and opt.lower() not in ("not sure", "none of these", "skip", "choice 1", "choice 2", "choice 3", "choice 4"):
            unique.append(opt)
    while len(unique) < 4:
        for cand in near_int(correct, 6):
            if cand not in unique and cand != str(correct):
                unique.append(cand)
            if len(unique) >= 4:
                break
        if len(unique) < 4:
            unique.append(str(correct) + f"′{len(unique)}")
            break
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
        distractors = near_int(correct)
    # Drop garbage distractors if a bank accidentally included them
    cleaned = [
        d for d in (distractors or [])
        if str(d).strip().lower() not in ("not sure", "none of these", "skip")
    ]
    if len(cleaned) < 3:
        cleaned = (cleaned + near_int(correct, 6))[:3]
    return make_question(text, correct, cleaned, explanation, idx, **kwargs)


def difficulty_for_index(i: int) -> str:
    """Progressive difficulty across 55 questions (30 concept + 25 finale)."""
    if i <= 15:
        return "easy"
    if i <= 30:
        return "medium"
    # Finale 31–55: progressively harder, related to the unit
    finale = i - 30
    if finale <= 8:
        return "easy"
    if finale <= 16:
        return "medium"
    if finale <= 22:
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


def _seed(text: str) -> int:
    n = 17
    for i, ch in enumerate(text or ""):
        n = (n * 33 + ord(ch) + i) % 1_000_003
    return n


def _nums(text: str, limit: int = 12) -> list[int]:
    """Pull signed integers from the stem (skip years-sized noise)."""
    out = []
    for m in re.finditer(r"(?<![A-Za-z])-?\d+(?:\.\d+)?(?![A-Za-z])", text or ""):
        raw = m.group(0)
        try:
            v = float(raw)
        except ValueError:
            continue
        if abs(v) > 10_000:
            continue
        iv = int(v) if abs(v - int(v)) < 1e-9 else int(round(v))
        out.append(iv)
        if len(out) >= limit:
            break
    return out


def _pick_int(nums, seed, lo, hi, fallback=None):
    pool = [n for n in nums if lo <= n <= hi]
    if pool:
        return pool[seed % len(pool)]
    if fallback is not None:
        return fallback
    return lo + (seed % max(1, hi - lo + 1))


def _parse_fraction(text: str):
    m = re.search(r"(\d+)\s*/\s*(\d+)", text or "")
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        if b > 0:
            return a, b
    return None


def _parse_ratio(text: str):
    m = re.search(r"(\d+)\s*:\s*(\d+)(?:\s*:\s*(\d+))?", text or "")
    if m:
        parts = [int(m.group(1)), int(m.group(2))]
        if m.group(3):
            parts.append(int(m.group(3)))
        return parts
    return None


def _parse_clock(text: str):
    m = re.search(r"\b(\d{1,2})\s*:\s*(\d{2})\b", text or "")
    if m:
        h, mi = int(m.group(1)), int(m.group(2))
        if 1 <= h <= 12 and 0 <= mi <= 59:
            return h, mi
    return None


def _parse_points(text: str, lim: int = 8):
    pts = []
    for m in re.finditer(r"\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)", text or ""):
        x, y = int(m.group(1)), int(m.group(2))
        if abs(x) <= lim and abs(y) <= lim:
            pts.append((x, y, f"({x},{y})"))
    return pts


def has_kw(text: str, *phrases: str) -> bool:
    """Word-boundary match so 'ratio' does not hit 'irrational'."""
    t = (text or "").lower()
    for phrase in phrases:
        p = phrase.lower()
        if " " in p or any(ch in p for ch in "/%"):
            if p in t:
                return True
        elif re.search(rf"\b{re.escape(p)}\b", t):
            return True
    return False


def asks_for_tool(text: str) -> bool:
    """True only when the stem tells the student to use a specific visual strategy."""
    t = stem_key(text)
    cues = (
        "use a tape", "use the tape", "tape diagram", "draw a tape",
        "ratio table", "make a ratio table", "fill the ratio table", "complete the ratio table",
        "use a table", "make a table", "fill the table", "complete the table",
        "number line", "use a number line", "on the number line", "mark on the line",
        "ten-frame", "ten frame", "use a ten frame",
        "plot the", "plot these", "graph the", "on the coordinate", "coordinate plane",
        "draw a", "sketch a", "use a diagram", "use the diagram",
        "venn diagram", "tree diagram", "slot diagram", "area model",
        "use a balance", "balance scale",
    )
    if any(c in t for c in cues):
        return True
    return bool(re.search(r"\buse a[n]?\b.{0,40}\b(tape|table|line|frame|graph|diagram|model|grid|plane)\b", t))


def diagram_for_context(unit_title: str, text: str, answer=None, *, require_tool: bool = False) -> str:
    """Pick a matching figure using numbers from this problem (not one fixed template)."""
    raw = text or ""
    blob = f"{unit_title} {stem_key(raw)}"
    if require_tool and not asks_for_tool(raw) and not asks_for_tool(unit_title):
        if not has_kw(blob, "tape diagram", "ratio table", "number line", "ten frame", "ten-frame",
                      "coordinate plane", "venn", "tree diagram"):
            return ""

    seed = _seed(blob)
    nums = _nums(raw)
    try:
        ans = int(float(str(answer).replace(",", "").split()[0]))
        nums = [ans] + [n for n in nums if n != ans]
    except (ValueError, TypeError, IndexError, AttributeError):
        ans = None

    def n_at(i, lo, hi, default):
        if i < len(nums) and lo <= nums[i] <= hi:
            return nums[i]
        return _pick_int(nums, seed + i * 17, lo, hi, default)

    if has_kw(blob, "clock", "o'clock") or ("time" in blob and has_kw(blob, "hour", "minute")):
        clk = _parse_clock(raw)
        if clk:
            h, mi = clk
        else:
            h = n_at(0, 1, 12, 1 + seed % 12)
            mi = [0, 5, 10, 15, 20, 30, 45][(seed // 3) % 7]
        return q_figure(svg_clock(h, mi), f"Clock showing about {h}:{mi:02d}.")

    if has_kw(blob, "coin", "money", "cent", "dollar", "nickel", "dime", "quarter"):
        q = max(0, min(4, n_at(0, 0, 4, 1 + seed % 3)))
        d = max(0, min(5, n_at(1, 0, 5, seed % 4)))
        n = max(0, min(5, n_at(2, 0, 5, (seed // 5) % 4)))
        if q + d + n == 0:
            q, d, n = 1, 2, 1
        coins = []
        if q:
            coins.append(("25¢", q, "#fde68a"))
        if d:
            coins.append(("10¢", d, "#e2e8f0"))
        if n:
            coins.append(("5¢", n, "#fdba74"))
        return q_figure(svg_coins(coins), "Coins from the problem.")

    if has_kw(blob, "ten frame", "ten-frame"):
        fill = abs(ans) if ans is not None and 0 < abs(ans) <= 20 else abs(n_at(0, 1, 20, 1 + seed % 20))
        return q_figure(svg_ten_frame(fill), f"Ten-frame showing {fill}.")

    # Only use ten-frames for early counting with small totals — not MathCounts "counting".
    if has_kw(blob, "count on", "count back", "how many dots") or (
        has_kw(blob, "counting") and has_kw(blob, "grade 1", "grade 2", "first grade", "second grade", "tens-frame")
    ):
        if ans is not None and 0 < abs(ans) <= 20:
            return q_figure(svg_ten_frame(abs(ans)), f"Ten-frame showing {abs(ans)}.")

    if has_kw(blob, "place value") or ("tens" in blob and "ones" in blob):
        val = abs(ans) if ans is not None and 0 < abs(ans) < 100 else abs(n_at(0, 11, 99, 10 + seed % 90))
        tens, ones = divmod(val, 10)
        if tens == 0:
            tens, ones = 1 + seed % 6, 1 + (seed // 7) % 9
        return q_figure(svg_base10(tens, ones), f"{tens} tens and {ones} ones.")

    if has_kw(blob, "tape", "tape diagram", "ratio", "for every", "proportion", "unit rate"):
        parts = _parse_ratio(raw)
        if not parts:
            a = abs(n_at(0, 1, 8, 2 + seed % 5))
            b = abs(n_at(1, 1, 8, 3 + (seed // 4) % 5))
            if a == b:
                b = a + 1 + seed % 3
            parts = [a, b]
        labels = [str(p) for p in parts]
        return q_figure(svg_tape(parts, labels), f"Tape parts: {':'.join(labels)}.")

    if has_kw(blob, "percent", "%", "discount", "tax", "tip"):
        pct_candidates = [n for n in nums if 1 <= n <= 100]
        pct = pct_candidates[0] if pct_candidates else [10, 20, 25, 40, 50, 75][seed % 6]
        wholes = [n for n in nums if n > 100 or (n != pct and n >= 20)]
        whole = wholes[0] if wholes else [40, 50, 60, 80, 100, 120][(seed // 5) % 6]
        return q_figure(svg_percent_bar(pct, whole), f"{pct}% of {whole}.")

    if has_kw(blob, "fraction", "numerator", "denominator", "½", "1/2", "1/3", "1/4") or _parse_fraction(raw):
        frac = _parse_fraction(raw)
        if frac:
            num, den = frac
        else:
            den = abs(n_at(1, 2, 10, 2 + seed % 8))
            num = abs(n_at(0, 1, den, 1 + seed % den))
        den = max(2, min(den, 12))
        num = max(0, min(num, den))
        return q_figure(svg_fraction_bar(num, den), f"{num}/{den} shaded.")

    if has_kw(blob, "number line", "integer", "negative", "absolute value"):
        focus = ans if ans is not None else (nums[0] if nums else seed % 9 - 4)
        span = 6 + seed % 4
        lo, hi = focus - span, focus + span
        if hi - lo > 18:
            lo, hi = focus - 8, focus + 8
        marks = [(0, "0")] if lo <= 0 <= hi else []
        if focus != 0:
            marks.append((focus, str(focus)))
        for extra in nums[1:4]:
            if lo <= extra <= hi and all(extra != m[0] for m in marks):
                marks.append((extra, str(extra)))
        return q_figure(svg_number_line(lo, hi, marks=marks, highlight=focus), "Numbers from this problem on the line.")

    if has_kw(blob, "slope", "coordinate", "quadrant", "plot", "vertex", "linear graph", "coordinate plane"):
        lim = 6
        pts = _parse_points(raw, lim=lim)
        if len(pts) < 2:
            x1 = n_at(0, -lim + 1, lim - 1, 1 + seed % 4)
            y1 = n_at(1, -lim + 1, lim - 1, 2 + (seed // 3) % 4)
            x2 = n_at(2, -lim + 1, lim - 1, x1 + 1 + seed % 3)
            if x2 == x1:
                x2 = min(lim - 1, x1 + 2)
            slope = 1 + (seed % 3)
            y2 = max(-lim + 1, min(lim - 1, y1 + slope * (x2 - x1)))
            pts = [(x1, y1, "A"), (x2, y2, "B")]
        line = (pts[0][0], pts[0][1], pts[1][0], pts[1][1]) if len(pts) >= 2 else None
        return q_figure(svg_plane(pts[:4], lim=lim, line=line), "Points from this problem.")

    if has_kw(blob, "pythag", "hypotenuse") or ("right" in blob and "triangle" in blob):
        a = abs(n_at(0, 2, 12, 3 + seed % 6))
        b = abs(n_at(1, 2, 12, 4 + (seed // 2) % 6))
        c = abs(n_at(2, max(a, b) + 1, 20, int((a * a + b * b) ** 0.5 + 0.5) or a + b))
        return q_figure(svg_triangle(a, b, c), f"Legs {a} and {b}; hypotenuse {c}.")

    if has_kw(blob, "circle", "radius", "circumference", "diameter", "π", "pi"):
        r = abs(n_at(0, 1, 15, 2 + seed % 8))
        if has_kw(blob, "diameter") and ans is not None and ans > 0:
            r = max(1, ans // 2)
        return q_figure(svg_circle(r), f"Circle with radius {r}.")

    if has_kw(blob, "area", "perimeter", "rectangle", "surface area", "volume"):
        length = abs(n_at(0, 2, 20, 4 + seed % 10))
        width = abs(n_at(1, 1, 15, 2 + (seed // 3) % 8))
        if width == length:
            width = max(1, length - 1 - seed % 3)
        return q_figure(svg_rect(length, width), f"Rectangle {length} by {width}.")

    if has_kw(blob, "equation", "balance", "solve for"):
        left_n = n_at(0, 1, 20, 3 + seed % 8)
        right_n = ans if ans is not None else n_at(1, 1, 40, left_n + 2 + seed % 6)
        left = f"x + {left_n}" if seed % 2 == 0 else f"{2 + seed % 3}x + {left_n}"
        return q_figure(svg_balance(left, str(right_n)), "Keep both sides equal.")

    if has_kw(blob, "venn", "inclusion-exclusion", "inclusion"):
        only_a = str(abs(n_at(0, 1, 40, 5 + seed % 12)))
        only_b = str(abs(n_at(1, 1, 40, 4 + (seed // 2) % 12)))
        both = str(abs(n_at(2, 1, 20, 2 + seed % 8)))
        return q_figure(svg_venn("A", "B", only_a, only_b, both), "Venn counts from this problem.")

    if has_kw(blob, "password", "pin", "product rule", "permutation", "outfit"):
        choices = [str(abs(n_at(i, 2, 12, 2 + (seed + i) % 8))) for i in range(3)]
        labels = [f"{c} choices" for c in choices]
        return q_figure(svg_slots(labels), "Fill each slot, then multiply.")

    if has_kw(blob, "tree", "casework", "branch"):
        a = str(abs(n_at(0, 1, 9, 1 + seed % 5)))
        b = str(abs(n_at(1, 1, 9, 2 + (seed // 2) % 5)))
        return q_figure(svg_tree([["start"], [a, b], ["1", "2", "1", "2"]]), "Each branch is a case.")

    if has_kw(blob, "exponent", "scientific notation") or (has_kw(blob, "power") and has_kw(blob, "base")):
        # Only draw arrays for small powers that actually fit and match the label.
        candidates = [
            (2, 2, 4), (2, 3, 8), (2, 4, 16), (3, 2, 9), (3, 3, 27),
            (4, 2, 16), (5, 2, 25), (6, 2, 36),
        ]
        # Prefer numbers mentioned in the stem when they form a true power.
        picked = None
        for b, e, v in candidates:
            if b in nums and e in nums:
                picked = (b, e, v)
                break
        if picked is None and ans is not None:
            for b, e, v in candidates:
                if v == abs(ans):
                    picked = (b, e, v)
                    break
        if picked is None:
            picked = candidates[seed % len(candidates)]
        base, exp, val = picked
        # Cap display size but NEVER lie about the value — skip huge arrays.
        if val > 36:
            return q_figure(
                svg_number_line(0, max(10, exp + 2), marks=[(exp, f"{base}^{exp}")]),
                f"{base}^{exp} = {val} (too many dots to draw).",
            )
        factors = "×".join([str(base)] * exp)
        return q_figure(
            svg_dots(val, "#6366f1", base if base <= 8 else 6, f"{base}^{exp} = {val}"),
            f"Array of {val} dots: {factors} = {val}.",
        )

    if has_kw(blob, "quadratic", "parabola"):
        h = n_at(0, -3, 3, seed % 5 - 2)
        k = n_at(1, -2, 4, (seed // 3) % 5 - 1)
        pts = [(h, k, "V"), (h + 1, k + 1, ""), (h - 1, k + 1, "")]
        return q_figure(svg_plane(pts, lim=6, line=None), f"Vertex near ({h},{k}).")

    # Combinatorics / counting problems that need slots or complement — never a random line.
    if has_kw(blob, "letter", "string", "password", "code", "digit", "outfit", "arrangement",
              "permutation", "combination", "how many ways", "at least one", "repeats"):
        choices = [str(abs(n_at(i, 2, 12, 2 + (seed + i) % 8))) for i in range(3)]
        labels = [f"slot {i + 1}" for i in range(3)]
        if has_kw(blob, "letter", "string") and len(nums) >= 1:
            # e.g. 3-letter from 4 symbols → 3 slots
            nslots = abs(n_at(0, 2, 5, 3))
            labels = [f"pos {i + 1}" for i in range(nslots)]
        return q_figure(svg_slots(labels), "Fill each position, then multiply (or use complement).")

    # No generic fallback: wrong diagrams are worse than no diagram.
    return ""


def pick_diagram(unit_title: str, text: str, answer) -> str:
    """Quiz diagrams only when the question asks students to use a visual tool."""
    if not asks_for_tool(text):
        return ""
    return diagram_for_context(unit_title, text, answer, require_tool=True)


def pick_scaffold(unit_title: str, text: str, answer, idx: int) -> dict | None:
    """Force a Khan-style step only when the question says to use that strategy."""
    t = stem_key(text)
    if not asks_for_tool(text):
        return None
    seed = _seed(unit_title + " " + t + str(idx))
    nums = _nums(text)
    try:
        ans = int(float(str(answer).replace(",", "").split()[0]))
    except (ValueError, TypeError, IndexError, AttributeError):
        ans = None

    if any(c in t for c in ("ratio table", "tape", "for every", "proportion", "unit rate")) or has_kw(t, "ratio"):
        parts = _parse_ratio(text) or []
        a = parts[0] if parts else (abs(nums[0]) if nums and 1 <= abs(nums[0]) <= 12 else 2 + seed % 5)
        b = parts[1] if len(parts) > 1 else (abs(nums[1]) if len(nums) > 1 and 1 <= abs(nums[1]) <= 12 else 3 + (seed // 3) % 5)
        if a == 0:
            a = 2
        if b == 0:
            b = 3
        mults = [1, 2, 3, 4]
        rows = [[a * m, b * m if m < 4 else None] for m in mults]
        answers = [[a * m, b * m] for m in mults]
        if ans is not None and ans == b * 4:
            rows[-1][1] = None
        return {
            "type": "ratio-table",
            "label": f"Fill the ratio table for {a}:{b} first. Then answer.",
            "headers": ["First quantity", "Second quantity"],
            "rows": rows,
            "answers": answers,
        }

    if has_kw(t, "percent", "%", "discount", "tax", "tip") or "percent table" in t:
        whole = next((n for n in nums if n >= 20), [40, 50, 60, 80, 100][seed % 5])
        return {
            "type": "ratio-table",
            "label": f"Complete the percent table for a whole of {whole}.",
            "headers": ["Percent", "Amount"],
            "rows": [[25, None], [50, None], [100, whole]],
            "answers": [[25, whole // 4], [50, whole // 2], [100, whole]],
        }

    if any(c in t for c in ("plot", "coordinate", "graph these", "graph the")) or has_kw(t, "slope"):
        pts = _parse_points(text, lim=8)
        if len(pts) >= 3:
            required = [[p[0], p[1]] for p in pts[:3]]
        else:
            b = nums[0] if nums else 1 + seed % 4
            m = nums[1] if len(nums) > 1 and abs(nums[1]) <= 5 else 1 + (seed // 2) % 3
            required = [[0, b], [1, b + m], [2, b + 2 * m]]
        prompt = "Plot " + ", ".join(f"({x},{y})" for x, y in required) + "."
        return {
            "type": "plot-points",
            "label": "Plot these 3 points on the grid, then answer.",
            "lim": 8,
            "required": required,
            "prompt": prompt,
        }

    if "number line" in t or "ten frame" in t or "ten-frame" in t:
        v = ans if ans is not None else (nums[0] if nums else 1 + seed % 9)
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

    if any(c in t for c in ("make a table", "use a table", "fill the table", "xy table", "input-output")):
        m = nums[0] if nums and 1 <= abs(nums[0]) <= 9 else 2 + seed % 5
        b = nums[1] if len(nums) > 1 and abs(nums[1]) <= 20 else seed % 5
        rows = [[1, m + b], [2, None], [3, 3 * m + b]]
        answers = [[1, m + b], [2, 2 * m + b], [3, 3 * m + b]]
        return {
            "type": "xy-table",
            "label": f"Fill the table for y = {m}x + {b}, then answer.",
            "headers": ["x", "y"],
            "rows": rows,
            "answers": answers,
        }
    return None


def attach_visuals(unit_title: str, q: dict, idx: int) -> dict:
    """Attach a diagram/scaffold only when the quiz stem asks for that strategy."""
    text = q.get("question_text") or ""
    has_diagram = 'class="vl-q-diagram"' in text or "class='vl-q-diagram'" in text
    has_scaffold = 'class="vl-scaffold"' in text
    diagram = "" if has_diagram else pick_diagram(unit_title, text, q.get("correct_answer"))
    sc = None if has_scaffold else pick_scaffold(unit_title, text, q.get("correct_answer"), idx)
    if diagram or sc:
        q = dict(q)
        q["question_text"] = wrap_prompt(text, diagram, scaffold_html(sc) if sc else "")
    return q


def lesson_figure_for(unit_title: str, context: str) -> str:
    """Lesson figure only when the problem text itself matches a visual topic.

    Unit titles (e.g. MathCounts 'Counting') must not force unrelated diagrams.
    """
    plain = context or ""
    # Prefer problem-only matching; include unit title only as weak hint for grade-level cues.
    fig = diagram_for_context(unit_title if has_kw(unit_title, "grade 1", "grade 2", "first", "second") else "", plain, require_tool=False)
    if not fig:
        return ""
    # Convert quiz-style figure into a lesson figure block.
    if 'class="vl-q-diagram"' in fig:
        inner = fig.replace('<div class="vl-q-diagram">', "").rsplit("</div>", 1)[0]
        cap = ""
        m = re.search(r'<p class="vl-q-caption">(.*?)</p>', inner, re.S)
        if m:
            cap = m.group(1)
            inner = re.sub(r'<p class="vl-q-caption">.*?</p>', "", inner, flags=re.S)
        return lesson_figure(inner, "Picture", cap or "Use this diagram while you work.")
    return fig


def polish_content(title: str, content: str) -> str:
    """Add diagrams to solved examples and 'use a …' strategy parts — not to every heading."""
    if not content:
        return content

    # Strip previously injected nonsense diagrams (generic number-line leftovers).
    content = re.sub(
        r'<div class="vl-figure"[^>]*>[\s\S]*?Marked value:\s*\d+\.?[\s\S]*?</div>\s*</div>',
        "",
        content,
        flags=re.I,
    )
    content = re.sub(
        r'<div class="vl-q-diagram">[\s\S]*?Marked value:\s*\d+\.?[\s\S]*?</div>',
        "",
        content,
        flags=re.I,
    )

    def inject_into_solved(match: re.Match) -> str:
        block = match.group(0)
        if re.search(r"<svg|vl-figure|vl-q-diagram|phet-sim-wrapper", block, re.I):
            return block
        plain = re.sub(r"<[^>]+>", " ", block)
        fig = lesson_figure_for(title, plain)
        if not fig:
            return block
        # Place the figure right after the problem line when possible.
        if re.search(r"<p><strong>Problem:</strong>", block, re.I):
            return re.sub(
                r"(<p><strong>Problem:</strong>.*?</p>)",
                r"\1" + fig,
                block,
                count=1,
                flags=re.I | re.S,
            )
        return block.replace("</h4>", "</h4>" + fig, 1)

    content = re.sub(
        r'<div style="background:#f8fafc;border:1px solid #cbd5e1;border-radius:12px;'
        r'padding:18px;margin:18px 0;">.*?</div>',
        inject_into_solved,
        content,
        flags=re.I | re.S,
    )

    def inject_strategy(match: re.Match) -> str:
        block = match.group(0)
        if re.search(r"<svg|vl-figure|vl-q-diagram", block, re.I):
            return block
        plain = re.sub(r"<[^>]+>", " ", block)
        # Require a real visual cue — bare words like "model check" must not spawn diagrams.
        if not asks_for_tool(plain) and not has_kw(
            plain,
            "tape diagram", "ratio table", "number line", "ten frame", "ten-frame",
            "coordinate plane", "venn diagram", "tree diagram", "area model", "draw a",
            "sketch a", "plot the", "graph the",
        ):
            return block
        fig = lesson_figure_for(title, plain)
        if not fig:
            return block
        return block.replace("</div></div>", fig + "</div></div>", 1) if "</div></div>" in block else block + fig

    content = re.sub(
        r'<div class="vl-callout vl-callout-strategy"[^>]*>.*?</div>\s*</div>',
        inject_strategy,
        content,
        flags=re.I | re.S,
    )

    # Standalone "use a …" paragraphs that are not already next to a figure.
    def inject_use_a(match: re.Match) -> str:
        para = match.group(0)
        if "vl-figure" in para or "<svg" in para:
            return para
        plain = re.sub(r"<[^>]+>", " ", para)
        if not asks_for_tool(plain):
            return para
        fig = lesson_figure_for(title, plain)
        return para + fig if fig else para

    content = re.sub(r"<p>[^<]*\b[Uu]se a[n]?\b[^<]*</p>", inject_use_a, content)

    # Drop finale quiz slots beyond TARGET_QUESTIONS (old courses had 80).
    def _keep_slot(m: re.Match) -> str:
        n = int(m.group(1))
        return m.group(0) if n <= TARGET_QUESTIONS else ""

    content = re.sub(r"<!--QUIZ_SLOT_(\d+)-->", _keep_slot, content)
    content = re.sub(
        r"<h2>Big practice \(50 problems\)</h2>",
        f"<h2>Big practice ({FINALE_QUESTIONS} problems)</h2>",
        content,
    )
    content = re.sub(
        r"<li><strong>41–50:</strong> Super thinker</li>",
        "<li><strong>19–25:</strong> Super thinker / stretch</li>",
        content,
    )
    content = re.sub(
        r"<li><strong>31–40:</strong> Think twice</li>",
        "<li><strong>11–18:</strong> Think twice</li>",
        content,
    )
    content = re.sub(
        r"<li><strong>16–30:</strong> A little harder</li>",
        "<li><strong>1–10:</strong> Warm-up → medium</li>",
        content,
    )
    content = re.sub(
        r"<li><strong>1–15:</strong> Warm-up</li>\s*",
        "",
        content,
    )
    return content


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


def _topic_filler(title: str, n: int, seed: int = 0):
    """Unique no-diagram practice items keyed to the unit topic (last-resort padding).

    Always embed n in the stem so 80 unique items are guaranteed.
    """
    t = (title or "").lower()
    a = 2 + (seed + n * 3) % 12
    b = 1 + (seed + n * 5) % 9
    c = 3 + (seed + n * 7) % 15
    tag = f"(set {n})"

    if has_kw(t, "place value", "tens", "ones") or (
        has_kw(t, "count", "counting") and not has_kw(t, "permut", "combin", "casework")
    ):
        start = 10 + n
        hop = 1 + (n % 5)
        return {
            "question_text": f"{tag} Start at {start}. Count on by {hop}, three times. Where do you land?",
            "correct_answer": str(start + 3 * hop),
            "explanation": f"{start} + {hop}+{hop}+{hop} = {start + 3 * hop}.",
        }
    if has_kw(t, "add", "addition", "sum"):
        x, y = a + 5 + (n % 7), b + 3 + (n % 5)
        return {
            "question_text": f"{tag} What is {x} + {y}?",
            "correct_answer": str(x + y),
            "explanation": f"{x} + {y} = {x + y}.",
        }
    if has_kw(t, "subtract", "subtraction", "difference"):
        big = a + b + 8 + n
        sub = b + 2 + (n % 4)
        return {
            "question_text": f"{tag} What is {big} − {sub}?",
            "correct_answer": str(big - sub),
            "explanation": f"{big} − {sub} = {big - sub}.",
        }
    if has_kw(t, "ratio", "rate", "proportion", "percent"):
        return {
            "question_text": f"{tag} If {a}:{b} = {a * 2}:x, what is x?",
            "correct_answer": str(b * 2),
            "explanation": f"Double both parts: x = {b * 2}.",
        }
    if has_kw(t, "fraction"):
        den = 2 + (n % 8)
        return {
            "question_text": f"{tag} How many pieces of size 1/{den} make one whole?",
            "correct_answer": str(den),
            "explanation": f"You need {den} pieces of size 1/{den}.",
        }
    if has_kw(t, "integer", "negative"):
        return {
            "question_text": f"{tag} What is ({a + n % 5}) + (−{b})?",
            "correct_answer": str(a + n % 5 - b),
            "explanation": f"{a + n % 5} + (−{b}) = {a + n % 5 - b}.",
        }
    if has_kw(t, "slope", "linear", "graph", "function", "coordinate"):
        return {
            "question_text": f"{tag} If y = {a}x + {b}, what is y when x = {2 + n % 3}?",
            "correct_answer": str((2 + n % 3) * a + b),
            "explanation": f"Substitute x = {2 + n % 3}.",
        }
    if has_kw(t, "equation", "solve", "system"):
        k = 2 + (n % 5)
        return {
            "question_text": f"{tag} Solve {a}x + {b} = {a * k + b}. What is x?",
            "correct_answer": str(k),
            "explanation": f"{a}x = {a * k}, so x = {k}.",
        }
    if has_kw(t, "exponent", "scientific", "power"):
        base = 2 + (n % 4)
        exp = 2 + (n % 2)
        return {
            "question_text": f"{tag} What is {base}^{exp}?",
            "correct_answer": str(base ** exp),
            "explanation": f"{base}^{exp} = {base ** exp}.",
        }
    if has_kw(t, "area", "perimeter", "volume", "circle", "triangle", "pythag"):
        L, W = a + 2 + (n % 4), b + 1 + (n % 3)
        return {
            "question_text": f"{tag} A rectangle is {L} by {W}. What is its area?",
            "correct_answer": str(L * W),
            "explanation": f"Area = {L} × {W} = {L * W}.",
        }
    if has_kw(t, "permut", "combin", "stars", "casework", "inclusion") or "mathcounts" in t:
        return {
            "question_text": f"{tag} How many outfits from {a} shirts and {b} pants (one of each)?",
            "correct_answer": str(a * b),
            "explanation": f"Product rule: {a}×{b}={a * b}.",
        }
    if has_kw(t, "quadratic", "polynomial", "algebra", "log", "radical", "sequence", "trig"):
        x0 = c % 5 + 1
        return {
            "question_text": f"{tag} If f(x) = {a}x − {b}, what is f({x0})?",
            "correct_answer": str(a * x0 - b),
            "explanation": f"Substitute x = {x0}.",
        }
    # Generic numeric story without a diagram
    return {
        "question_text": (
            f"{tag} A machine starts at {n + 4}, adds {n + 1}, then subtracts {n}. "
            f"What is the final output?"
        ),
        "correct_answer": str((n + 4) + (n + 1) - n),
        "explanation": f"{n + 4} + {n + 1} − {n} = {(n + 4) + (n + 1) - n}.",
    }


_BANNED_PHRASE = re.compile(r"\b(wait|recalculate)\b", re.I)
_FILLER_STEM = re.compile(
    r"warmup product check|review check \d+|what is 2\^|"
    r"unit application \d+|checkpoint \d+ for this unit|"
    r"\(set \d+\)|how many outfits from|"
    r"if 2:5 =|if \$f\(x\)=2x\$|if f\(x\)=2x|"
    r"find the discriminant of \$x\^2\+|leading coefficient of|"
    r"simplify \$i\^\{|"
    r"a machine starts at",
    re.I,
)


def _is_filler(text: str) -> bool:
    t = stem_key(text)
    return bool(_FILLER_STEM.search(t)) or bool(_BANNED_PHRASE.search(text or ""))


def _template_key(text: str) -> str:
    return re.sub(r"\d+", "#", stem_key(text))


def _diff_rank(q: dict) -> int:
    return {"easy": 0, "medium": 1, "hard": 2, "stretch": 3}.get(q.get("difficulty"), 1)


def _is_too_easy_for_hard(text: str) -> bool:
    """True if a stem is too trivial to sit in Hard / SAT Stretch slots."""
    t = stem_key(text)
    if _is_filler(text):
        return True
    if "(set " in (text or "").lower() or "[c" in t:
        # [C n] tags are challenge fillers — those are OK
        if re.search(r"\[c\d+\]", t):
            return False
    easy_bits = (
        "how many outfits from",
        "outfits:",
        "outfit",
        "what is 2+2",
        "count back: 15, 14",
        "warmup",
        "a machine starts at",
        "(set ",
        "skill check",
        "check computation",
        "warmup product",
    )
    if any(b in t for b in easy_bits):
        return True
    # Bare power / tiny arithmetic evaluations (e.g. 2^5 = ?)
    if re.fullmatch(r"\$?\d+\s*(\^|\\?\^)\s*\{?\d+\}?\s*=?\s*\??\$?", t.replace(" ", "")):
        return True
    if re.fullmatch(r".{0,8}\d+\s*\^\s*\d+\s*=?\s*\??", t):
        return True
    # Very short arithmetic with tiny numbers and no contest cue
    if len(t) < 40 and not any(k in t for k in ("amc", "mathcounts", "sat", "complement", "at least", "how many ways", "scientific", "simplify")):
        if re.fullmatch(r"what is \d+\s*[+\-×x*]\s*\d+\??", t):
            return True
        if re.search(r"\d+\s*\^\s*\d+\s*=", t) and len(t) < 25:
            return True
    return False


def _is_off_topic(title: str, text: str) -> bool:
    """Reject challenges that clearly belong to a different unit."""
    t = (title or "").lower()
    p = stem_key(text)
    # Unit 1 exponents must not pull geometry / systems
    if "exponent" in t or "scientific" in t:
        if any(k in p for k in ("hypotenuse", "pythag", "right triangle", "leg ", "legs ", "cylinder volume", "slope of the line", "system:")):
            return True
    if "slope" in t or "linear graph" in t:
        if any(k in p for k in ("hypotenuse", "scientific notation", "password", "permutation")):
            return True
    if "pythag" in t or "cylinder" in t:
        if any(k in p for k in ("scientific notation", "2^{-", "log_", "permutation")):
            return True
    if "ratio" in t and "rational" not in t:
        if any(k in p for k in ("hypotenuse", "quadratic", "log_")):
            return True
    return False


def polish_questions(title: str, questions) -> list:
    from question_banks import extra_questions
    from challenge_banks import challenge_filler, challenges_for

    seen = set()
    tmpl_counts = {}
    handwritten = []
    for q in questions:
        text = q.get("question_text") or ""
        key = stem_key(text)
        if not key or key in seen or _is_filler(text):
            continue
        if _is_off_topic(title, text):
            continue
        tmpl = _template_key(text)
        if tmpl_counts.get(tmpl, 0) >= 3:
            continue
        tmpl_counts[tmpl] = tmpl_counts.get(tmpl, 0) + 1
        seen.add(key)
        handwritten.append(dict(q))

    extras = []
    for item in list(extra_questions(title) or []) + list(challenges_for(title) or []):
        if not item:
            continue
        blob = f"{item.get('question_text') or ''} {item.get('explanation') or ''}"
        if _BANNED_PHRASE.search(blob):
            continue
        if _is_off_topic(title, item.get("question_text") or ""):
            continue
        q = _to_full(item, 0)
        if item.get("difficulty"):
            q["difficulty"] = item["difficulty"]
        key = stem_key(q.get("question_text") or "")
        if not key or key in seen:
            continue
        seen.add(key)
        extras.append(q)

    extras.sort(key=_diff_rank)
    hard_pool = [q for q in extras if q.get("difficulty") in ("hard", "stretch")]
    other_pool = [q for q in extras if q.get("difficulty") not in ("hard", "stretch")]

    core = handwritten[:CONCEPT_QUESTIONS]
    while len(core) < CONCEPT_QUESTIONS and other_pool:
        core.append(other_pool.pop(0))
    while len(core) < CONCEPT_QUESTIONS and hard_pool:
        core.append(hard_pool.pop(0))

    # Finale prefers hard / stretch challenges (not leftover easy fillers).
    unique = core + hard_pool + other_pool

    n = 0
    while len(unique) < TARGET_QUESTIONS and n < 500:
        n += 1
        next_i = len(unique) + 1
        target = difficulty_for_index(next_i)
        if next_i > CONCEPT_QUESTIONS:
            item = challenge_filler(
                title, n, target if target in ("hard", "stretch", "medium", "easy") else "hard"
            )
            # Prefer hard/stretch banks even for early finale warm-ups
            if target in ("easy", "medium"):
                item = challenge_filler(title, n, "hard") or item
        elif target in ("hard", "stretch"):
            item = challenge_filler(title, n, target)
        else:
            item = _topic_filler(title, n, seed=_seed(title) + n)
        if not item or _is_off_topic(title, item.get("question_text") or ""):
            continue
        key = stem_key(item["question_text"])
        if not key or key in seen:
            continue
        seen.add(key)
        q = _to_full(item, 0)
        if item.get("difficulty"):
            q["difficulty"] = item["difficulty"]
        unique.append(q)

    unique = unique[:TARGET_QUESTIONS]

    out_qs = list(unique)
    for i, q in enumerate(out_qs):
        idx = i + 1
        target = difficulty_for_index(idx)
        text = q.get("question_text") or ""
        # Concept drills may stay easy; finale must be real challenge material.
        needs_upgrade = False
        if idx > CONCEPT_QUESTIONS and _is_too_easy_for_hard(text):
            needs_upgrade = True
        if (target in ("hard", "stretch") and _is_too_easy_for_hard(text)) or _is_off_topic(title, text):
            needs_upgrade = True
        if needs_upgrade:
            for attempt in range(1, 120):
                repl = challenge_filler(
                    title, idx * 17 + attempt, "hard" if target in ("easy", "medium") else target
                )
                if _is_off_topic(title, repl.get("question_text") or ""):
                    continue
                if _is_too_easy_for_hard(repl.get("question_text") or ""):
                    continue
                key = stem_key(repl["question_text"])
                if key and key not in seen:
                    seen.discard(stem_key(text))
                    seen.add(key)
                    nq = _to_full(repl, 0)
                    nq["difficulty"] = target
                    out_qs[i] = nq
                    break

    out = []
    junk = {"not sure", "none of these", "skip"}
    for i, q in enumerate(out_qs, 1):
        qq = attach_visuals(title, q, i)
        diff = difficulty_for_index(i)
        qq["difficulty"] = diff
        qq["points"] = POINTS[diff]
        qq["order_index"] = i
        qq["question_type"] = qq.get("question_type") or "multiple_choice"
        # Fix awkward stems leftover from earlier generators
        stem = qq.get("question_text") or ""
        stem = re.sub(
            r"(?i)scientific of\s+([0-9.]+)\s*\??",
            r"Write \1 in scientific notation.",
            stem,
        )
        qq["question_text"] = stem
        opts = [o for o in (qq.get("options") or []) if str(o).strip().lower() not in junk]
        if qq["correct_answer"] not in opts:
            opts = [qq["correct_answer"]] + [o for o in opts if o != qq["correct_answer"]]
        while len(opts) < 4:
            for cand in near_int(qq["correct_answer"], 6):
                if cand not in opts:
                    opts.append(cand)
                if len(opts) >= 4:
                    break
            break
        qq["options"] = opts[:4]
        out.append(qq)

    keys = [stem_key(q["question_text"]) for q in out]
    if len(keys) != len(set(keys)):
        raise AssertionError(f"{title}: duplicate question stems after polish")
    if len(out) != TARGET_QUESTIONS:
        raise AssertionError(f"{title}: expected {TARGET_QUESTIONS} questions, got {len(out)}")
    return out


def polish_unit(title, description, content, questions):
    return title, description, polish_content(title, content), polish_questions(title, questions)
