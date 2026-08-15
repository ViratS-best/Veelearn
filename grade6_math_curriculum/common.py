"""Shared helpers for Grade 6 math: clear English, extra diagrams, quizzes."""

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
    "unit_rates": (
        "Unit Rates",
        "https://phet.colorado.edu/sims/html/unit-rates/latest/unit-rates_all.html",
        "Compare prices and speeds. Find the amount for 1.",
    ),
    "nl_int": (
        "Number Line: Integers",
        "https://phet.colorado.edu/sims/html/number-line-integers/latest/number-line-integers_all.html",
        "Walk left and right from zero. Negative is the other side of zero.",
    ),
    "expr": (
        "Expression Exchange",
        "https://phet.colorado.edu/sims/html/expression-exchange/latest/expression-exchange_all.html",
        "Trade coins for like terms. See how 3x + 2x becomes 5x.",
    ),
    "area": (
        "Area Builder",
        "https://phet.colorado.edu/sims/html/area-builder/latest/area-builder_all.html",
        "Build shapes from squares. Area is the count of square units.",
    ),
    "build_frac": (
        "Build a Fraction",
        "https://phet.colorado.edu/sims/html/build-a-fraction/latest/build-a-fraction_all.html",
        "Split wholes into equal pieces. That picture helps you divide fractions.",
    ),
    "arith": (
        "Arithmetic",
        "https://phet.colorado.edu/sims/html/arithmetic/latest/arithmetic_all.html",
        "Fluency with multiply and divide keeps ratio tables moving.",
    ),
}


def phet_box(key: str) -> str:
    title, url, line = PHET[key]
    return phet(title, url, line)


def figure(title: str, inner_html: str, caption: str = "") -> str:
    cap = f'<p style="margin:10px 0 0;font-size:0.95rem;color:#334155;">{caption}</p>' if caption else ""
    return (
        '<div class="vl-figure" style="background:#fff;border:1px solid #cbd5e1;border-radius:12px;'
        'padding:14px 16px;margin:18px 0;max-width:620px;">'
        f'<div style="font-weight:800;color:#312e81;margin-bottom:10px;">{title}</div>'
        f"{inner_html}{cap}</div>"
    )


_svg_seq = 0


def _mark():
    global _svg_seq
    _svg_seq += 1
    return f"vl-m{_svg_seq}"


def tape_diagram(rows, title="Tape diagram", caption=""):
    """rows: list of (label, [(color, count, cell_label), ...])."""
    blocks = []
    for label, cells in rows:
        parts = []
        for color, count, cell_label in cells:
            for i in range(count):
                txt = cell_label if (cell_label and i == 0) else ""
                parts.append(
                    f'<span style="display:inline-flex;align-items:center;justify-content:center;'
                    f'width:36px;height:32px;border:1px solid #1e293b;background:{color};'
                    f'font-size:0.75rem;font-weight:700;">{txt}</span>'
                )
        blocks.append(
            f'<div style="margin:8px 0;display:flex;align-items:center;gap:10px;">'
            f'<span style="width:72px;font-weight:700;">{html.escape(label)}</span>'
            f'<span>{"".join(parts)}</span></div>'
        )
    return figure(title, "".join(blocks), caption)


def double_number_line(top_label, top_vals, bot_label, bot_vals, title="Double number line", caption=""):
    n = len(top_vals)
    w, h = 520, 130
    left, right = 50, 490
    y_top, y_bot = 40, 90
    marker = _mark()
    ticks = []
    for i in range(n):
        x = left + i * (right - left) / max(n - 1, 1)
        ticks.append(f'<line x1="{x}" y1="{y_top - 8}" x2="{x}" y2="{y_top + 8}" stroke="#0f172a" stroke-width="2"/>')
        ticks.append(f'<line x1="{x}" y1="{y_bot - 8}" x2="{x}" y2="{y_bot + 8}" stroke="#0f172a" stroke-width="2"/>')
        ticks.append(f'<text x="{x}" y="{y_top - 14}" text-anchor="middle" font-size="13" font-weight="700">{top_vals[i]}</text>')
        ticks.append(f'<text x="{x}" y="{y_bot + 22}" text-anchor="middle" font-size="13" font-weight="700">{bot_vals[i]}</text>')
    svg = f"""
<svg viewBox="0 0 {w} {h}" width="{w}" role="img" aria-label="{html.escape(title)}">
  <defs>
    <marker id="{marker}" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="#0f172a"/>
    </marker>
  </defs>
  <text x="8" y="{y_top + 4}" font-size="12" fill="#1e3a8a" font-weight="700">{html.escape(top_label)}</text>
  <text x="8" y="{y_bot + 4}" font-size="12" fill="#9a3412" font-weight="700">{html.escape(bot_label)}</text>
  <line x1="{left}" y1="{y_top}" x2="{right}" y2="{y_top}" stroke="#0f172a" stroke-width="2" marker-end="url(#{marker})"/>
  <line x1="{left}" y1="{y_bot}" x2="{right}" y2="{y_bot}" stroke="#0f172a" stroke-width="2" marker-end="url(#{marker})"/>
  {''.join(ticks)}
</svg>
"""
    return figure(title, svg, caption)


def percent_bar(percent=25, whole=80, title="Percent bar", caption=""):
    w, h = 480, 90
    bar_w = 400
    filled = bar_w * percent / 100
    part = whole * percent / 100
    svg = f"""
<svg viewBox="0 0 {w} {h}" width="{w}" role="img" aria-label="{percent} percent of {whole}">
  <rect x="40" y="28" width="{bar_w}" height="28" fill="#e2e8f0" stroke="#0f172a" stroke-width="2"/>
  <rect x="40" y="28" width="{filled}" height="28" fill="#6366f1" stroke="#0f172a" stroke-width="2"/>
  <text x="40" y="22" font-size="12" fill="#334155">0%</text>
  <text x="{40 + bar_w}" y="22" text-anchor="end" font-size="12" fill="#334155">100% = {whole}</text>
  <text x="{40 + filled}" y="74" text-anchor="middle" font-size="13" font-weight="700" fill="#312e81">{percent}% = {part:g}</text>
</svg>
"""
    return figure(title, svg, caption or f"{percent}% of {whole} is {part:g}.")


def integer_line(lo=-6, hi=6, marks=None, title="Integer number line", caption=""):
    marks = marks or []
    w, h = 540, 90
    left, right = 30, 510
    y = 45
    n = hi - lo
    marker = _mark()
    ticks = []
    for v in range(lo, hi + 1):
        x = left + (v - lo) * (right - left) / n
        ticks.append(f'<line x1="{x}" y1="{y - 8}" x2="{x}" y2="{y + 8}" stroke="#0f172a" stroke-width="2"/>')
        ticks.append(f'<text x="{x}" y="{y + 24}" text-anchor="middle" font-size="12">{v}</text>')
        if v == 0:
            ticks.append(f'<text x="{x}" y="{y - 14}" text-anchor="middle" font-size="11" fill="#64748b">zero</text>')
    dots = []
    colors = ["#dc2626", "#2563eb", "#059669", "#d97706"]
    for i, (val, lab) in enumerate(marks):
        x = left + (val - lo) * (right - left) / n
        c = colors[i % len(colors)]
        dots.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{c}"/>')
        dots.append(f'<text x="{x}" y="{y - 16}" text-anchor="middle" font-size="12" font-weight="700" fill="{c}">{html.escape(lab)}</text>')
    svg = f"""
<svg viewBox="0 0 {w} {h}" width="{w}" role="img" aria-label="{html.escape(title)}">
  <defs>
    <marker id="{marker}" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="#0f172a"/>
    </marker>
  </defs>
  <line x1="{left}" y1="{y}" x2="{right}" y2="{y}" stroke="#0f172a" stroke-width="2" marker-end="url(#{marker})"/>
  {''.join(ticks)}
  {''.join(dots)}
</svg>
"""
    return figure(title, svg, caption)


def four_quadrant_plane(points=None, lim=5, title="Four-quadrant coordinate plane", caption=""):
    points = points or []
    scale = 28
    pad = 36
    ox = pad + lim * scale
    oy = pad + lim * scale
    w = pad * 2 + lim * 2 * scale + 20
    h = w
    marker = _mark()
    lines = []
    for v in range(-lim, lim + 1):
        x = ox + v * scale
        y = oy - v * scale
        lines.append(f'<line x1="{x}" y1="{oy - lim * scale}" x2="{x}" y2="{oy + lim * scale}" stroke="#e2e8f0"/>')
        lines.append(f'<line x1="{ox - lim * scale}" y1="{y}" x2="{ox + lim * scale}" y2="{y}" stroke="#e2e8f0"/>')
        if v:
            lines.append(f'<text x="{x}" y="{oy + 14}" text-anchor="middle" font-size="11">{v}</text>')
            lines.append(f'<text x="{ox - 12}" y="{y + 4}" text-anchor="end" font-size="11">{v}</text>')
    qlabs = (
        f'<text x="{ox + lim * scale - 8}" y="{oy - lim * scale + 16}" text-anchor="end" font-size="11" fill="#64748b">I</text>'
        f'<text x="{ox - lim * scale + 8}" y="{oy - lim * scale + 16}" font-size="11" fill="#64748b">II</text>'
        f'<text x="{ox - lim * scale + 8}" y="{oy + lim * scale - 6}" font-size="11" fill="#64748b">III</text>'
        f'<text x="{ox + lim * scale - 8}" y="{oy + lim * scale - 6}" text-anchor="end" font-size="11" fill="#64748b">IV</text>'
    )
    dots = []
    for pt in points:
        x, y = pt[0], pt[1]
        lab = pt[2] if len(pt) > 2 else f"({x}, {y})"
        px, py = ox + x * scale, oy - y * scale
        dots.append(f'<circle cx="{px}" cy="{py}" r="6" fill="#dc2626"/>')
        dots.append(f'<text x="{px + 8}" y="{py - 8}" font-size="12" font-weight="700" fill="#7f1d1d">{html.escape(lab)}</text>')
    svg = f"""
<svg viewBox="0 0 {w} {h}" width="{min(w, 420)}" role="img" aria-label="{html.escape(title)}">
  <defs>
    <marker id="{marker}" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="#0f172a"/>
    </marker>
  </defs>
  {''.join(lines)}
  <line x1="{ox - lim * scale}" y1="{oy}" x2="{ox + lim * scale + 14}" y2="{oy}" stroke="#0f172a" stroke-width="2" marker-end="url(#{marker})"/>
  <line x1="{ox}" y1="{oy + lim * scale}" x2="{ox}" y2="{oy - lim * scale - 14}" stroke="#0f172a" stroke-width="2" marker-end="url(#{marker})"/>
  <text x="{ox + lim * scale + 18}" y="{oy + 4}" font-size="14" font-weight="700" fill="#1e3a8a">x</text>
  <text x="{ox + 8}" y="{oy - lim * scale - 18}" font-size="14" font-weight="700" fill="#1e3a8a">y</text>
  {qlabs}
  {''.join(dots)}
</svg>
"""
    return figure(
        title,
        svg,
        caption
        or "Quadrant I: (+, +). II: (−, +). III: (−, −). IV: (+, −). Right is +x. Up is +y.",
    )


def parallelogram_area(base=6, height=4, title="Area of a parallelogram"):
    svg = f"""
<svg viewBox="0 0 280 170" width="280" role="img" aria-label="parallelogram base {base} height {height}">
  <polygon points="50,130 200,130 240,40 90,40" fill="#c7d2fe" stroke="#312e81" stroke-width="2"/>
  <line x1="90" y1="40" x2="90" y2="130" stroke="#dc2626" stroke-width="2" stroke-dasharray="4 3"/>
  <text x="125" y="148" text-anchor="middle" font-size="13">base = {base}</text>
  <text x="98" y="90" font-size="13" fill="#b91c1c">h = {height}</text>
</svg>
"""
    return figure(title, svg, f"Area = base × height = {base} × {height} = {base * height} square units.")


def triangle_area(base=6, height=4, title="Area of a triangle"):
    svg = f"""
<svg viewBox="0 0 260 170" width="260" role="img" aria-label="triangle base {base} height {height}">
  <polygon points="40,140 220,140 130,30" fill="#fde68a" stroke="#92400e" stroke-width="2"/>
  <line x1="130" y1="30" x2="130" y2="140" stroke="#dc2626" stroke-width="2" stroke-dasharray="4 3"/>
  <text x="130" y="158" text-anchor="middle" font-size="13">base = {base}</text>
  <text x="138" y="95" font-size="13" fill="#b91c1c">h = {height}</text>
</svg>
"""
    return figure(title, svg, f"Area = ½ × base × height = ½ × {base} × {height} = {base * height / 2:g} square units.")


def prism_net(length=4, width=3, height=2, title="Net of a rectangular prism"):
    u = 18
    l, w, h = length * u, width * u, height * u
    # layout:  [  T ]
    #       [L F R Bk]
    #          [  B ]
    ox, oy = 20 + h, 20
    faces = [
        (ox, oy, l, w, "#c7d2fe", "top"),
        (ox - h, oy + w, h, l, "#a5b4fc", "left"),
        (ox, oy + w, l, h, "#e0e7ff", "front"),
        (ox + l, oy + w, h, l, "#818cf8", "right"),
        (ox + l + h, oy + w, l, h, "#c7d2fe", "back"),
        (ox, oy + w + h, l, w, "#a5b4fc", "bottom"),
    ]
    rects = []
    for x, y, fw, fh, color, lab in faces:
        rects.append(
            f'<rect x="{x}" y="{y}" width="{fw}" height="{fh}" fill="{color}" stroke="#312e81" stroke-width="2"/>'
        )
        rects.append(
            f'<text x="{x + fw / 2}" y="{y + fh / 2 + 4}" text-anchor="middle" font-size="11" fill="#1e293b">{lab}</text>'
        )
    vw = ox + l + h + l + 30
    vh = oy + w + h + w + 20
    svg = f'<svg viewBox="0 0 {vw} {vh}" width="{min(vw, 420)}" role="img">{"".join(rects)}</svg>'
    sa = 2 * (length * width + length * height + width * height)
    return figure(
        title,
        svg,
        f"Surface area = 2(lw + lh + wh) = 2({length}×{width} + {length}×{height} + {width}×{height}) = {sa} square units.",
    )


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
        f"Volume = l × w × h = {length} × {width} × {height} = {length * width * height} cubic units.",
    )


def balance_scale(left="x + 3", right="11", title="A balanced equation"):
    svg = f"""
<svg viewBox="0 0 320 150" width="320" role="img" aria-label="balance scale">
  <line x1="40" y1="70" x2="280" y2="70" stroke="#0f172a" stroke-width="4"/>
  <polygon points="160,70 148,92 172,92" fill="#0f172a"/>
  <line x1="160" y1="92" x2="160" y2="130" stroke="#0f172a" stroke-width="4"/>
  <rect x="130" y="130" width="60" height="10" fill="#334155"/>
  <rect x="48" y="42" width="90" height="28" rx="6" fill="#dbeafe" stroke="#1e3a8a"/>
  <rect x="182" y="42" width="90" height="28" rx="6" fill="#dcfce7" stroke="#166534"/>
  <text x="93" y="61" text-anchor="middle" font-size="14" font-weight="700">{html.escape(left)}</text>
  <text x="227" y="61" text-anchor="middle" font-size="14" font-weight="700">{html.escape(right)}</text>
</svg>
"""
    return figure(title, svg, "Both sides have the same value. Whatever you do to one side, do to the other.")


def inequality_line(op=">", value=3, title="Graph an inequality", caption=""):
    lo, hi = -2, 8
    w, h = 480, 80
    left, right = 30, 450
    y = 40
    marker = _mark()
    ticks = []
    for v in range(lo, hi + 1):
        x = left + (v - lo) * (right - left) / (hi - lo)
        ticks.append(f'<line x1="{x}" y1="{y - 7}" x2="{x}" y2="{y + 7}" stroke="#0f172a" stroke-width="2"/>')
        ticks.append(f'<text x="{x}" y="{y + 22}" text-anchor="middle" font-size="12">{v}</text>')
    vx = left + (value - lo) * (right - left) / (hi - lo)
    if op in (">", "≥"):
        shade = f'<line x1="{vx}" y1="{y}" x2="{right - 8}" y2="{y}" stroke="#6366f1" stroke-width="8" opacity="0.45"/>'
    else:
        shade = f'<line x1="{left + 8}" y1="{y}" x2="{vx}" y2="{y}" stroke="#6366f1" stroke-width="8" opacity="0.45"/>'
    fill = "#fff" if op in (">", "<") else "#6366f1"
    svg = f"""
<svg viewBox="0 0 {w} {h}" width="{w}" role="img" aria-label="{html.escape(title)}">
  <defs>
    <marker id="{marker}" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="#0f172a"/>
    </marker>
  </defs>
  <line x1="{left}" y1="{y}" x2="{right}" y2="{y}" stroke="#0f172a" stroke-width="2" marker-end="url(#{marker})"/>
  {shade}
  {''.join(ticks)}
  <circle cx="{vx}" cy="{y}" r="8" fill="{fill}" stroke="#312e81" stroke-width="2"/>
</svg>
"""
    open_closed = "Open circle: the endpoint is not included." if op in (">", "<") else "Filled circle: the endpoint is included."
    return figure(title, svg, caption or f"x {op} {value}. {open_closed}")


def dot_plot(values, title="Dot plot", caption=""):
    from collections import Counter

    counts = Counter(values)
    lo, hi = min(values), max(values)
    w = 80 + (hi - lo + 1) * 28
    h = 40 + max(counts.values()) * 14 + 28
    dots = []
    for v, c in counts.items():
        x = 40 + (v - lo) * 28
        for i in range(c):
            y = h - 28 - i * 14
            dots.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#2563eb"/>')
    ticks = []
    for v in range(lo, hi + 1):
        x = 40 + (v - lo) * 28
        ticks.append(f'<text x="{x}" y="{h - 8}" text-anchor="middle" font-size="12">{v}</text>')
    svg = f'<svg viewBox="0 0 {w} {h}" width="{min(w, 480)}" role="img">{"".join(dots)}{"".join(ticks)}</svg>'
    return figure(title, svg, caption or "Each dot is one data value. A stack means that number showed up more often.")


def histogram(bins, title="Histogram", caption=""):
    """bins: list of (label, count)."""
    max_c = max(b[1] for b in bins) or 1
    bar_w = 48
    w = 40 + len(bins) * (bar_w + 12)
    h = 150
    bars = []
    for i, (lab, count) in enumerate(bins):
        bh = 100 * count / max_c
        x = 30 + i * (bar_w + 12)
        y = 120 - bh
        bars.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{bh}" fill="#818cf8" stroke="#312e81"/>')
        bars.append(f'<text x="{x + bar_w / 2}" y="138" text-anchor="middle" font-size="11">{html.escape(str(lab))}</text>')
        bars.append(f'<text x="{x + bar_w / 2}" y="{y - 4}" text-anchor="middle" font-size="11">{count}</text>')
    svg = f'<svg viewBox="0 0 {w} {h}" width="{min(w, 480)}" role="img">{"".join(bars)}</svg>'
    return figure(title, svg, caption or "A histogram groups data into intervals (bins). Bar height is how many land in that bin.")


def box_plot(minimum, q1, med, q3, maximum, title="Box plot", caption=""):
    lo, hi = minimum - 1, maximum + 1
    w, h = 460, 90
    left, right = 30, 430
    y = 40

    def x_of(v):
        return left + (v - lo) * (right - left) / (hi - lo)

    xs = [x_of(v) for v in (minimum, q1, med, q3, maximum)]
    svg = f"""
<svg viewBox="0 0 {w} {h}" width="{w}" role="img" aria-label="box plot">
  <line x1="{xs[0]}" y1="{y}" x2="{xs[4]}" y2="{y}" stroke="#0f172a" stroke-width="2"/>
  <rect x="{xs[1]}" y="{y - 16}" width="{xs[3] - xs[1]}" height="32" fill="#c7d2fe" stroke="#312e81" stroke-width="2"/>
  <line x1="{xs[2]}" y1="{y - 16}" x2="{xs[2]}" y2="{y + 16}" stroke="#b91c1c" stroke-width="3"/>
  <line x1="{xs[0]}" y1="{y - 10}" x2="{xs[0]}" y2="{y + 10}" stroke="#0f172a" stroke-width="2"/>
  <line x1="{xs[4]}" y1="{y - 10}" x2="{xs[4]}" y2="{y + 10}" stroke="#0f172a" stroke-width="2"/>
  <text x="{xs[0]}" y="{y + 34}" text-anchor="middle" font-size="11">min {minimum}</text>
  <text x="{xs[1]}" y="{y + 34}" text-anchor="middle" font-size="11">Q1 {q1}</text>
  <text x="{xs[2]}" y="14" text-anchor="middle" font-size="11" fill="#b91c1c">median {med}</text>
  <text x="{xs[3]}" y="{y + 34}" text-anchor="middle" font-size="11">Q3 {q3}</text>
  <text x="{xs[4]}" y="{y + 34}" text-anchor="middle" font-size="11">max {maximum}</text>
</svg>
"""
    return figure(
        title,
        svg,
        caption or "The box is the middle 50% of the data (Q1 to Q3). The line inside is the median. Whiskers reach min and max.",
    )


def fraction_divide_bars(wholes=3, piece="1/2", title="How many pieces fit?"):
    den = int(piece.split("/")[1])
    cells = []
    for _ in range(wholes):
        group = []
        for j in range(den):
            group.append(
                f'<span style="display:inline-block;width:28px;height:28px;border:1px solid #1e293b;'
                f'background:#86efac;box-sizing:border-box;"></span>'
            )
        cells.append(
            f'<span style="display:inline-block;margin-right:8px;border:2px solid #166534;">{"".join(group)}</span>'
        )
    inner = f'<div>{"".join(cells)}</div>'
    return figure(
        title,
        inner,
        f"{wholes} wholes, each split into {den} equal pieces. {wholes} ÷ {piece} = {wholes * den}.",
    )


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
        "<p>Start easy. Then they get a little trickier. Sketch a tape diagram, number line, or table if you need to.</p>"
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
<p>This is <strong>sixth grade math</strong>. You are bridging elementary arithmetic and middle-school algebra. We work with ratios, rational numbers, basic algebra, geometry, and data.</p>
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
        core = str(correct).lstrip("-$¢").replace(".", "", 1).replace("/", "", 1)
        if core.isdigit() or (core.replace("-", "", 1).isdigit()):
            try:
                n = int(float(str(correct).replace("$", "").split("/")[0]))
                filler = str(n + len(unique) * 2 + 3)
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
    for delta in (1, -1, 2, -2, 10, -10, 5, 20, -5, 3, -3, 50):
        v = c + delta
        if v != c:
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
