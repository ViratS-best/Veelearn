#!/usr/bin/env python3
"""Deep AP Calculus AB curriculum builders — Units 1–4."""

from __future__ import annotations

import math

from curriculum_kit import lesson_figure, svg_parabola, svg_plane

from hs_curriculum import (
    concept_block, solved, practice_slots, unit_shell, mq,
    xy_graph, sample_curve, number_line, tangent_curve_svg,
)
from .common import AUDIENCE, STRETCH_LABEL


def _pack(rows):
    qs = []
    for i, row in enumerate(rows, 1):
        text, ans, expl, dist = row[0], row[1], row[2], row[3] if len(row) > 3 else None
        qs.append(mq(text, ans, expl, i, distractors=dist))
    return qs


def _open_on(svg, opens, xlim=(-6, 6), ylim=(-6, 6), w=300, h=300, pad=24):
    """Overlay open (hollow) points on an xy_graph SVG."""
    x0, x1 = xlim
    y0, y1 = ylim

    def X(x):
        return pad + (x - x0) / (x1 - x0) * (w - 2 * pad)

    def Y(y):
        return h - pad - (y - y0) / (y1 - y0) * (h - 2 * pad)

    bits = []
    for item in opens:
        x, y, lab = item[0], item[1], item[2] if len(item) > 2 else ""
        bits.append(
            f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="5.2" fill="#fff" '
            f'stroke="#b91c1c" stroke-width="2.3"/>'
        )
        if lab:
            bits.append(
                f'<text x="{X(x) + 8:.1f}" y="{Y(y) - 8:.1f}" font-size="11" fill="#b91c1c">{lab}</text>'
            )
    return svg.replace("</svg>", "".join(bits) + "</svg>")


def _map_xy(xlim, ylim, w, h, pad=28):
    x0, x1 = xlim
    y0, y1 = ylim

    def X(x):
        return pad + (x - x0) / (x1 - x0) * (w - 2 * pad)

    def Y(y):
        return h - pad - (y - y0) / (y1 - y0) * (h - 2 * pad)

    return X, Y, pad


def _axis_lines(X, Y, pad, w, h, xlim, ylim, xlab="x", ylab="y"):
    x0, x1 = xlim
    y0, y1 = ylim
    bits = []
    if y0 <= 0 <= y1:
        bits.append(
            f'<line x1="{pad}" y1="{Y(0):.1f}" x2="{w - pad}" y2="{Y(0):.1f}" stroke="#0f172a" stroke-width="1.5"/>'
        )
    else:
        bits.append(f'<line x1="{pad}" y1="{h - pad}" x2="{w - pad}" y2="{h - pad}" stroke="#0f172a" stroke-width="1.5"/>')
    if x0 <= 0 <= x1:
        bits.append(
            f'<line x1="{X(0):.1f}" y1="{pad}" x2="{X(0):.1f}" y2="{h - pad}" stroke="#0f172a" stroke-width="1.5"/>'
        )
    else:
        bits.append(f'<line x1="{pad}" y1="{pad}" x2="{pad}" y2="{h - pad}" stroke="#0f172a" stroke-width="1.5"/>')
    bits.append(f'<text x="{w - pad - 2}" y="{(Y(0) if y0 <= 0 <= y1 else h - pad) - 6:.1f}" font-size="11">{xlab}</text>')
    bits.append(f'<text x="{(X(0) if x0 <= 0 <= x1 else pad) + 6:.1f}" y="{pad + 10}" font-size="11">{ylab}</text>')
    return bits


def _limit_jump_svg(w=320, h=260):
    """Piecewise jump: left ray closed, right ray open, plus a filled value elsewhere."""
    xlim, ylim = (-1, 5), (-1, 6)
    X, Y, pad = _map_xy(xlim, ylim, w, h)
    bits = _axis_lines(X, Y, pad, w, h, xlim, ylim)
    # left piece y = x + 1 on [-1, 2), open at (2, 3)
    bits.append(
        f'<line x1="{X(-1):.1f}" y1="{Y(0):.1f}" x2="{X(2):.1f}" y2="{Y(3):.1f}" stroke="#4f46e5" stroke-width="2.6"/>'
    )
    # right piece y = 5 - 0.4(x-2) on (2, 5]
    bits.append(
        f'<line x1="{X(2):.1f}" y1="{Y(4.5):.1f}" x2="{X(5):.1f}" y2="{Y(3.3):.1f}" stroke="#4f46e5" stroke-width="2.6"/>'
    )
    bits.append(f'<circle cx="{X(2):.1f}" cy="{Y(3):.1f}" r="5.2" fill="#fff" stroke="#b91c1c" stroke-width="2.3"/>')
    bits.append(f'<circle cx="{X(2):.1f}" cy="{Y(4.5):.1f}" r="5.2" fill="#fff" stroke="#b91c1c" stroke-width="2.3"/>')
    bits.append(f'<circle cx="{X(2):.1f}" cy="{Y(1):.1f}" r="5.2" fill="#b91c1c"/>')
    bits.append(f'<text x="{X(2) + 8:.1f}" y="{Y(3) - 6:.1f}" font-size="11" fill="#b91c1c">(2,3)</text>')
    bits.append(f'<text x="{X(2) + 8:.1f}" y="{Y(4.5) - 6:.1f}" font-size="11" fill="#b91c1c">(2,4.5)</text>')
    bits.append(f'<text x="{X(2) + 8:.1f}" y="{Y(1) + 14:.1f}" font-size="11" fill="#b91c1c">f(2)=1</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">{"".join(bits)}</svg>'


def _secant_tangent_svg(w=320, h=240):
    """y = x^2/4 with a secant through x=0.5 and x=2.5 and the tangent at x=2."""
    xlim, ylim = (-0.5, 4.2), (-0.4, 4.2)
    X, Y, pad = _map_xy(xlim, ylim, w, h)
    bits = _axis_lines(X, Y, pad, w, h, xlim, ylim)
    pts = sample_curve(lambda t: 0.25 * t * t, 0, 3.8)
    d = " ".join(("M" if i == 0 else "L") + f"{X(x):.1f},{Y(y):.1f}" for i, (x, y) in enumerate(pts))
    bits.append(f'<path d="{d}" fill="none" stroke="#4f46e5" stroke-width="2.4"/>')
    # secant 0.5 to 2.5
    bits.append(
        f'<line x1="{X(0.5):.1f}" y1="{Y(0.0625):.1f}" x2="{X(2.5):.1f}" y2="{Y(1.5625):.1f}" '
        f'stroke="#f59e0b" stroke-width="2" stroke-dasharray="6 4"/>'
    )
    # tangent at x=2, y=1, slope=1
    bits.append(
        f'<line x1="{X(0.6):.1f}" y1="{Y(-0.4):.1f}" x2="{X(3.4):.1f}" y2="{Y(2.4):.1f}" '
        f'stroke="#dc2626" stroke-width="2.2"/>'
    )
    bits.append(f'<circle cx="{X(2):.1f}" cy="{Y(1):.1f}" r="5" fill="#b91c1c"/>')
    bits.append(f'<text x="{X(2) + 8:.1f}" y="{Y(1) - 8:.1f}" font-size="11" fill="#b91c1c">P(2,1)</text>')
    bits.append(f'<text x="{X(2.6):.1f}" y="{Y(2.1):.1f}" font-size="11" fill="#dc2626">tangent</text>')
    bits.append(f'<text x="{X(1.4):.1f}" y="{Y(0.95):.1f}" font-size="11" fill="#b45309">secant</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">{"".join(bits)}</svg>'


def _ladder_svg(w=300, h=240):
    """Leaning ladder against a wall, labeled x, y, ℓ."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="36" y="28" width="14" height="170" fill="#cbd5e1" stroke="#0f172a"/>'
        f'<line x1="50" y1="198" x2="270" y2="198" stroke="#0f172a" stroke-width="3"/>'
        f'<line x1="50" y1="40" x2="230" y2="198" stroke="#b91c1c" stroke-width="3.2"/>'
        f'<text x="148" y="108" font-size="14" fill="#b91c1c">ℓ</text>'
        f'<text x="128" y="216" font-size="14">x (ft)</text>'
        f'<text x="8" y="120" font-size="14">y (ft)</text>'
        f'<text x="58" y="24" font-size="12">wall</text>'
        f'<text x="200" y="228" font-size="12">floor</text>'
        "</svg>"
    )


def _cone_svg(w=260, h=240):
    """Inverted cone tank with water height h and radius r labeled."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<polygon points="40,36 220,36 130,210" fill="#e0e7ff" stroke="#312e81" stroke-width="2"/>'
        f'<polygon points="70,90 190,90 130,210" fill="#93c5fd" stroke="#1e3a8a" stroke-width="1.8"/>'
        f'<line x1="130" y1="90" x2="190" y2="90" stroke="#b91c1c" stroke-width="1.8" stroke-dasharray="4 3"/>'
        f'<text x="196" y="94" font-size="13" fill="#b91c1c">r</text>'
        f'<line x1="130" y1="90" x2="130" y2="210" stroke="#047857" stroke-width="1.8" stroke-dasharray="4 3"/>'
        f'<text x="136" y="160" font-size="13" fill="#047857">h</text>'
        f'<text x="86" y="28" font-size="12">cone tank</text>'
        "</svg>"
    )


def _concavity_svg(w=320, h=240):
    """Cubic-looking curve with an inflection point marked."""
    xlim, ylim = (-3.2, 3.2), (-3.2, 3.2)
    X, Y, pad = _map_xy(xlim, ylim, w, h)
    bits = _axis_lines(X, Y, pad, w, h, xlim, ylim)
    pts = sample_curve(lambda t: 0.18 * t * t * t - 0.9 * t, -2.6, 2.6)
    d = " ".join(("M" if i == 0 else "L") + f"{X(x):.1f},{Y(y):.1f}" for i, (x, y) in enumerate(pts))
    bits.append(f'<path d="{d}" fill="none" stroke="#4f46e5" stroke-width="2.5"/>')
    bits.append(f'<circle cx="{X(0):.1f}" cy="{Y(0):.1f}" r="5" fill="#dc2626"/>')
    bits.append(f'<text x="{X(0) + 8:.1f}" y="{Y(0) - 10:.1f}" font-size="12" fill="#b91c1c">inflection</text>')
    bits.append(f'<text x="{X(-2.2):.1f}" y="{Y(1.6):.1f}" font-size="11">concave down</text>')
    bits.append(f'<text x="{X(1.1):.1f}" y="{Y(-1.7):.1f}" font-size="11">concave up</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">{"".join(bits)}</svg>'


def _mvt_svg(w=320, h=240):
    """Curve on [a,b] with secant AB and a parallel tangent at c."""
    xlim, ylim = (-0.3, 4.3), (-0.4, 3.6)
    X, Y, pad = _map_xy(xlim, ylim, w, h)
    bits = _axis_lines(X, Y, pad, w, h, xlim, ylim)

    def f(t):
        return 0.18 * (t - 0.4) * (4.1 - t) + 0.35 * math.sin(1.2 * t) + 0.5

    pts = sample_curve(f, 0.4, 3.8)
    d = " ".join(("M" if i == 0 else "L") + f"{X(x):.1f},{Y(y):.1f}" for i, (x, y) in enumerate(pts))
    bits.append(f'<path d="{d}" fill="none" stroke="#4f46e5" stroke-width="2.4"/>')
    a, b = 0.5, 3.6
    bits.append(
        f'<line x1="{X(a):.1f}" y1="{Y(f(a)):.1f}" x2="{X(b):.1f}" y2="{Y(f(b)):.1f}" '
        f'stroke="#f59e0b" stroke-width="2" stroke-dasharray="6 4"/>'
    )
    c = 2.05
    m = (f(b) - f(a)) / (b - a)
    bits.append(
        f'<line x1="{X(c - 0.9):.1f}" y1="{Y(f(c) - 0.9 * m):.1f}" x2="{X(c + 0.9):.1f}" y2="{Y(f(c) + 0.9 * m):.1f}" '
        f'stroke="#dc2626" stroke-width="2.2"/>'
    )
    bits.append(f'<circle cx="{X(a):.1f}" cy="{Y(f(a)):.1f}" r="4.5" fill="#b45309"/>')
    bits.append(f'<circle cx="{X(b):.1f}" cy="{Y(f(b)):.1f}" r="4.5" fill="#b45309"/>')
    bits.append(f'<circle cx="{X(c):.1f}" cy="{Y(f(c)):.1f}" r="5" fill="#b91c1c"/>')
    bits.append(f'<text x="{X(a) - 4:.1f}" y="{Y(f(a)) + 16:.1f}" font-size="11">A</text>')
    bits.append(f'<text x="{X(b) + 6:.1f}" y="{Y(f(b)) + 4:.1f}" font-size="11">B</text>')
    bits.append(f'<text x="{X(c) + 8:.1f}" y="{Y(f(c)) - 8:.1f}" font-size="11" fill="#b91c1c">c</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">{"".join(bits)}</svg>'


def _sign_chart_svg(crit, signs, label="f′", w=460):
    """Number line with critical numbers and +/− signs for a derivative."""
    lo, hi = crit[0] - 2, crit[-1] + 2
    h, left, right, y = 90, 36, w - 36, 48
    n = max(hi - lo, 1)

    def xp(v):
        return left + (v - lo) * (right - left) / n

    bits = [f'<line x1="{left}" y1="{y}" x2="{right}" y2="{y}" stroke="#0f172a" stroke-width="2"/>']
    for v in range(lo, hi + 1):
        bits.append(f'<line x1="{xp(v):.1f}" y1="{y - 7}" x2="{xp(v):.1f}" y2="{y + 7}" stroke="#0f172a"/>')
        bits.append(f'<text x="{xp(v):.1f}" y="{y + 22}" text-anchor="middle" font-size="11">{v}</text>')
    mids = [lo] + list(crit) + [hi]
    for i, s in enumerate(signs):
        xm = (xp(mids[i]) + xp(mids[i + 1])) / 2
        col = "#047857" if s == "+" else "#b91c1c"
        bits.append(f'<text x="{xm:.1f}" y="{y - 16}" text-anchor="middle" font-size="16" fill="{col}">{s}</text>')
    for v in crit:
        bits.append(f'<circle cx="{xp(v):.1f}" cy="{y}" r="5.5" fill="#7c3aed"/>')
    bits.append(f'<text x="{left}" y="16" font-size="12">{label} sign chart</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">{"".join(bits)}</svg>'


def _riemann_svg(n=4, w=320, h=240):
    """Left Riemann rectangles under y = 0.12x^2 + 0.6 on [1, 5]."""
    xlim, ylim = (0, 6), (0, 4.2)
    X, Y, pad = _map_xy(xlim, ylim, w, h)
    bits = _axis_lines(X, Y, pad, w, h, xlim, ylim, ylab="y")
    a, b = 1.0, 5.0
    dx = (b - a) / n

    def f(t):
        return 0.12 * t * t + 0.6

    for i in range(n):
        left = a + i * dx
        ht = f(left)
        x1, y1 = X(left), Y(ht)
        x2, y0 = X(left + dx), Y(0)
        bits.append(
            f'<rect x="{min(x1, x2):.1f}" y="{y1:.1f}" width="{abs(x2 - x1):.1f}" height="{y0 - y1:.1f}" '
            f'fill="#c7d2fe" stroke="#312e81" stroke-width="1.2"/>'
        )
    pts = sample_curve(f, 0.4, 5.6)
    d = " ".join(("M" if i == 0 else "L") + f"{X(x):.1f},{Y(y):.1f}" for i, (x, y) in enumerate(pts))
    bits.append(f'<path d="{d}" fill="none" stroke="#b91c1c" stroke-width="2.4"/>')
    bits.append(f'<text x="{X(3.2):.1f}" y="{Y(3.6):.1f}" font-size="11">y=f(x)</text>')
    bits.append(f'<text x="{X(2.2):.1f}" y="{Y(0.35):.1f}" font-size="11">left Riemann</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">{"".join(bits)}</svg>'


def _area_between_svg(w=320, h=240):
    """Shaded region between y = √x and y = x/2 on [0, 4]."""
    xlim, ylim = (-0.4, 4.6), (-0.4, 2.6)
    X, Y, pad = _map_xy(xlim, ylim, w, h)
    bits = _axis_lines(X, Y, pad, w, h, xlim, ylim)
    top = sample_curve(lambda t: math.sqrt(t) if t >= 0 else 0, 0, 4)
    bot = sample_curve(lambda t: 0.5 * t, 0, 4)
    d_fill = " ".join(("M" if i == 0 else "L") + f"{X(x):.1f},{Y(y):.1f}" for i, (x, y) in enumerate(top))
    d_fill += " " + " ".join(f"L{X(x):.1f},{Y(y):.1f}" for x, y in reversed(bot)) + " Z"
    bits.append(f'<path d="{d_fill}" fill="#c7d2fe" stroke="none"/>')
    d1 = " ".join(("M" if i == 0 else "L") + f"{X(x):.1f},{Y(y):.1f}" for i, (x, y) in enumerate(top))
    d2 = " ".join(("M" if i == 0 else "L") + f"{X(x):.1f},{Y(y):.1f}" for i, (x, y) in enumerate(bot))
    bits.append(f'<path d="{d1}" fill="none" stroke="#1d4ed8" stroke-width="2.3"/>')
    bits.append(f'<path d="{d2}" fill="none" stroke="#b91c1c" stroke-width="2.3"/>')
    bits.append(f'<text x="{X(2.4):.1f}" y="{Y(1.85):.1f}" font-size="12" fill="#1d4ed8">y=√x</text>')
    bits.append(f'<text x="{X(2.8):.1f}" y="{Y(0.95):.1f}" font-size="12" fill="#b91c1c">y=x/2</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">{"".join(bits)}</svg>'


def _washer_svg(w=340, h=230):
    """2D region y=x (outer after rotation about x-axis is actually y=x vs y=x^2) plus axis of rotation."""
    xlim, ylim = (-0.3, 1.5), (-0.35, 1.35)
    X, Y, pad = _map_xy(xlim, ylim, w, h)
    bits = _axis_lines(X, Y, pad, w, h, xlim, ylim)
    top = sample_curve(lambda t: t, 0, 1)
    bot = sample_curve(lambda t: t * t, 0, 1)
    d_fill = " ".join(("M" if i == 0 else "L") + f"{X(x):.1f},{Y(y):.1f}" for i, (x, y) in enumerate(top))
    d_fill += " " + " ".join(f"L{X(x):.1f},{Y(y):.1f}" for x, y in reversed(bot)) + " Z"
    bits.append(f'<path d="{d_fill}" fill="#ddd6fe" stroke="none"/>')
    d1 = " ".join(("M" if i == 0 else "L") + f"{X(x):.1f},{Y(y):.1f}" for i, (x, y) in enumerate(top))
    d2 = " ".join(("M" if i == 0 else "L") + f"{X(x):.1f},{Y(y):.1f}" for i, (x, y) in enumerate(bot))
    bits.append(f'<path d="{d1}" fill="none" stroke="#1d4ed8" stroke-width="2.2"/>')
    bits.append(f'<path d="{d2}" fill="none" stroke="#b91c1c" stroke-width="2.2"/>')
    bits.append(
        f'<line x1="{X(-0.15):.1f}" y1="{Y(0):.1f}" x2="{X(1.4):.1f}" y2="{Y(0):.1f}" '
        f'stroke="#047857" stroke-width="2.4" stroke-dasharray="7 4"/>'
    )
    bits.append(f'<text x="{X(0.55):.1f}" y="{Y(0.22):.1f}" font-size="11">axis of rotation</text>')
    bits.append(f'<text x="{X(0.72):.1f}" y="{Y(0.88):.1f}" font-size="11" fill="#1d4ed8">y=x</text>')
    bits.append(f'<text x="{X(0.55):.1f}" y="{Y(0.48):.1f}" font-size="11" fill="#b91c1c">y=x²</text>')
    # small washer sketch on the right
    bits.append(f'<ellipse cx="292" cy="118" rx="28" ry="12" fill="none" stroke="#312e81"/>')
    bits.append(f'<ellipse cx="292" cy="118" rx="14" ry="6" fill="#f8fafc" stroke="#b91c1c"/>')
    bits.append(f'<text x="268" y="148" font-size="11">washer</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">{"".join(bits)}</svg>'


def _cross_section_svg(w=320, h=230):
    """Base region in the xy-plane with a square cross-section standing on a slice."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<polygon points="48,170 250,170 250,70 48,140" fill="#e0e7ff" stroke="#312e81" stroke-width="2"/>'
        f'<polygon points="150,140 210,140 210,80 150,80" fill="#a5b4fc" stroke="#1e3a8a" stroke-width="2"/>'
        f'<line x1="48" y1="170" x2="250" y2="170" stroke="#0f172a" stroke-width="2"/>'
        f'<text x="130" y="188" font-size="12">base in the xy-plane</text>'
        f'<text x="156" y="72" font-size="12">square slice</text>'
        f'<text x="214" y="118" font-size="11">side s(x)</text>'
        "</svg>"
    )


def _slope_field_svg(fn, xlim=(-2.2, 2.2), ylim=(-2.2, 2.2), n=8, w=300, h=300, highlight=None):
    """Small slope ticks for dy/dx = fn(x,y). Optional highlight solution points."""
    X, Y, pad = _map_xy(xlim, ylim, w, h)
    bits = _axis_lines(X, Y, pad, w, h, xlim, ylim)
    length = 9
    for i in range(n):
        for j in range(n):
            x = xlim[0] + (xlim[1] - xlim[0]) * (i + 0.5) / n
            y = ylim[0] + (ylim[1] - ylim[0]) * (j + 0.5) / n
            try:
                m = fn(x, y)
            except (ZeroDivisionError, ValueError, OverflowError):
                continue
            if m is None or abs(m) > 40:
                ang = math.pi / 2 if (m is not None and m > 0) else -math.pi / 2
            else:
                ang = math.atan(m)
            dx = length * math.cos(ang)
            dy = length * math.sin(ang)
            bits.append(
                f'<line x1="{X(x) - dx:.1f}" y1="{Y(y) + dy:.1f}" x2="{X(x) + dx:.1f}" y2="{Y(y) - dy:.1f}" '
                f'stroke="#4338ca" stroke-width="1.6"/>'
            )
    if highlight:
        for x, y, lab in highlight:
            bits.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="4.5" fill="#dc2626"/>')
            if lab:
                bits.append(f'<text x="{X(x) + 7:.1f}" y="{Y(y) - 6:.1f}" font-size="11" fill="#b91c1c">{lab}</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">{"".join(bits)}</svg>'


def _accum_svg(w=320, h=240):
    """Velocity-style curve with signed net area from 0 to t shaded."""
    xlim, ylim = (-0.4, 5.2), (-2.2, 3.2)
    X, Y, pad = _map_xy(xlim, ylim, w, h)
    bits = _axis_lines(X, Y, pad, w, h, xlim, ylim, xlab="t", ylab="v(t)")

    def v(t):
        return 1.6 * math.sin(0.9 * t) + 0.35

    pos, neg = [], []
    ts = [i * 0.08 for i in range(0, 46)]
    for t in ts:
        y = v(t)
        if y >= 0:
            pos.append((t, y))
            neg.append((t, 1e9))
        else:
            neg.append((t, y))
            pos.append((t, 1e9))
    if len(pos) >= 2:
        d = "M" + f"{X(0):.1f},{Y(0):.1f} " + " ".join(f"L{X(t):.1f},{Y(y):.1f}" for t, y in pos if y < 1e8)
        d += f" L{X(3.6):.1f},{Y(0):.1f} Z"
        bits.append(f'<path d="{d}" fill="#bbf7d0" stroke="none"/>')
    pts = sample_curve(v, 0, 5)
    d2 = " ".join(("M" if i == 0 else "L") + f"{X(x):.1f},{Y(y):.1f}" for i, (x, y) in enumerate(pts))
    bits.append(f'<path d="{d2}" fill="none" stroke="#1d4ed8" stroke-width="2.3"/>')
    bits.append(f'<line x1="{X(3.6):.1f}" y1="{Y(-2):.1f}" x2="{X(3.6):.1f}" y2="{Y(2.8):.1f}" stroke="#b91c1c" stroke-dasharray="5 4"/>')
    bits.append(f'<text x="{X(3.7):.1f}" y="{Y(2.6):.1f}" font-size="11" fill="#b91c1c">t</text>')
    bits.append(f'<text x="{X(1.1):.1f}" y="{Y(1.7):.1f}" font-size="11">net area = s(t)−s(0)</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">{"".join(bits)}</svg>'


def _ivt_svg(w=300, h=230):
    xlim, ylim = (-0.3, 4.2), (-1.6, 3.2)
    X, Y, pad = _map_xy(xlim, ylim, w, h)
    bits = _axis_lines(X, Y, pad, w, h, xlim, ylim)

    def f(t):
        return 0.55 * (t - 0.4) * (t - 0.4) - 1.15

    pts = sample_curve(f, 0.3, 3.8)
    d = " ".join(("M" if i == 0 else "L") + f"{X(x):.1f},{Y(y):.1f}" for i, (x, y) in enumerate(pts))
    bits.append(f'<path d="{d}" fill="none" stroke="#4f46e5" stroke-width="2.4"/>')
    bits.append(
        f'<line x1="{X(0):.1f}" y1="{Y(1):.1f}" x2="{X(4):.1f}" y2="{Y(1):.1f}" '
        f'stroke="#dc2626" stroke-width="1.6" stroke-dasharray="5 4"/>'
    )
    bits.append(f'<text x="{X(3.1):.1f}" y="{Y(1.25):.1f}" font-size="11" fill="#b91c1c">y=k</text>')
    bits.append(f'<circle cx="{X(0.5):.1f}" cy="{Y(f(0.5)):.1f}" r="4.5" fill="#047857"/>')
    bits.append(f'<circle cx="{X(3.5):.1f}" cy="{Y(f(3.5)):.1f}" r="4.5" fill="#047857"/>')
    bits.append(f'<text x="{X(0.5):.1f}" y="{Y(f(0.5)) + 16:.1f}" font-size="11">f(a)</text>')
    bits.append(f'<text x="{X(3.2):.1f}" y="{Y(f(3.5)) - 8:.1f}" font-size="11">f(b)</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">{"".join(bits)}</svg>'


def _corner_svg(w=300, h=230):
    """Absolute-value corner: continuous, not differentiable at 0."""
    xlim, ylim = (-3.2, 3.2), (-0.6, 3.4)
    X, Y, pad = _map_xy(xlim, ylim, w, h)
    bits = _axis_lines(X, Y, pad, w, h, xlim, ylim)
    bits.append(
        f'<polyline points="{X(-2.8):.1f},{Y(2.8):.1f} {X(0):.1f},{Y(0):.1f} {X(2.8):.1f},{Y(2.8):.1f}" '
        f'fill="none" stroke="#4f46e5" stroke-width="2.6"/>'
    )
    bits.append(f'<circle cx="{X(0):.1f}" cy="{Y(0):.1f}" r="5" fill="#dc2626"/>')
    bits.append(f'<text x="{X(0.15):.1f}" y="{Y(0.55):.1f}" font-size="12" fill="#b91c1c">corner</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">{"".join(bits)}</svg>'


def _box_opt_svg(w=280, h=210):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<polygon points="70,70 200,70 230,40 100,40" fill="#c7d2fe" stroke="#312e81"/>'
        f'<polygon points="70,70 70,160 200,160 200,70" fill="#a5b4fc" stroke="#312e81"/>'
        f'<polygon points="200,70 230,40 230,130 200,160" fill="#818cf8" stroke="#312e81"/>'
        f'<text x="118" y="180" font-size="13">x</text>'
        f'<text x="40" y="120" font-size="13">x</text>'
        f'<text x="210" y="100" font-size="13">h</text>'
        f'<text x="90" y="24" font-size="12">open-top box</text>'
        "</svg>"
    )


def _pva_svg(w=320, h=230):
    xlim, ylim = (-0.3, 5.2), (-2.4, 3.2)
    X, Y, pad = _map_xy(xlim, ylim, w, h)
    bits = _axis_lines(X, Y, pad, w, h, xlim, ylim, xlab="t", ylab="s, v")
    spts = sample_curve(lambda t: -0.35 * (t - 2.4) ** 2 + 2.4, 0, 5)
    vpts = sample_curve(lambda t: -0.7 * (t - 2.4), 0, 5)
    d1 = " ".join(("M" if i == 0 else "L") + f"{X(x):.1f},{Y(y):.1f}" for i, (x, y) in enumerate(spts))
    d2 = " ".join(("M" if i == 0 else "L") + f"{X(x):.1f},{Y(y):.1f}" for i, (x, y) in enumerate(vpts))
    bits.append(f'<path d="{d1}" fill="none" stroke="#1d4ed8" stroke-width="2.4"/>')
    bits.append(f'<path d="{d2}" fill="none" stroke="#dc2626" stroke-width="2.2"/>')
    bits.append(f'<text x="{X(3.6):.1f}" y="{Y(2.0):.1f}" font-size="12" fill="#1d4ed8">s(t)</text>')
    bits.append(f'<text x="{X(3.8):.1f}" y="{Y(-1.4):.1f}" font-size="12" fill="#dc2626">v(t)</text>')
    bits.append(f'<circle cx="{X(2.4):.1f}" cy="{Y(2.4):.1f}" r="4.5" fill="#047857"/>')
    bits.append(f'<text x="{X(2.5):.1f}" y="{Y(2.75):.1f}" font-size="11">v=0</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">{"".join(bits)}</svg>'


def _family_svg(w=300, h=230):
    xlim, ylim = (-0.4, 3.4), (-1.2, 4.2)
    X, Y, pad = _map_xy(xlim, ylim, w, h)
    bits = _axis_lines(X, Y, pad, w, h, xlim, ylim)
    for c, col in [(0.4, "#94a3b8"), (1.2, "#64748b"), (2.0, "#4f46e5"), (2.8, "#312e81")]:
        pts = sample_curve(lambda t, cc=c: cc * math.exp(-0.45 * t), 0, 3.2)
        d = " ".join(("M" if i == 0 else "L") + f"{X(x):.1f},{Y(y):.1f}" for i, (x, y) in enumerate(pts))
        bits.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2"/>')
    bits.append(f'<text x="{X(1.6):.1f}" y="{Y(3.4):.1f}" font-size="11">y=Ce^{{-kt}}</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">{"".join(bits)}</svg>'


# ===========================================================================
# UNIT 1: Limits & Continuity
# ===========================================================================

def _u1_questions():
    return _pack([
        # 1–5 graph/table
        ("The graph of $f$ has a hole at $(2,3)$, a filled point at $(2,1)$, and the two sides of the graph both approach $y=3$ as $x\\to 2$. What is $\\lim_{x\\to 2}f(x)$?",
         3, "A limit cares what $f$ approaches, not the plotted value $f(2)=1$. Both sides approach $3$.", [1, 2, "DNE"]),
        ("A table lists $f(1.9)=4.02$, $f(1.99)=4.001$, $f(2.01)=3.998$, $f(2.1)=3.97$. The best estimate of $\\lim_{x\\to 2}f(x)$ is",
         4, "Nearby outputs cluster near $4$, so the two-sided limit is $4$ even if $f(2)$ is missing.", [2, 3.9, "DNE"]),
        ("From a graph, $\\lim_{x\\to 0^-}g(x)=-2$ and $\\lim_{x\\to 0^+}g(x)=5$. Then $\\lim_{x\\to 0}g(x)$ is",
         "DNE", "A two-sided limit exists only when the one-sided limits exist and agree. $-2\\neq 5$.", [-2, 5, 0]),
        ("If $h(x)=x+1$ for $x\\neq 4$ and $h(4)=100$, then $\\lim_{x\\to 4}h(x)$ equals",
         5, "Near $x=4$ the rule is $x+1$, which approaches $5$. The spike $h(4)=100$ is irrelevant to the limit.", [100, 4, 0]),
        ("Reading a piecewise graph: the left piece ends at an open circle $(1,2)$ and the right piece starts at a closed circle $(1,2)$. $\\lim_{x\\to 1}f(x)$ is",
         2, "Both sides approach the same height $2$, so the two-sided limit is $2$. Closed versus open at $x=1$ affects $f(1)$, not the limit.", [1, 0, "DNE"]),
        # 6–10 algebraic
        ("Evaluate $\\lim_{x\\to 3}(2x-5)$.", 1, "Polynomials are continuous, so substitute: $2(3)-5=1$.", [6, -5, 3]),
        ("Evaluate $\\lim_{x\\to 2}\\dfrac{x^2-4}{x-2}$.", 4,
         "Factor $x^2-4=(x-2)(x+2)$. For $x\\neq 2$ the quotient is $x+2$, which approaches $4$.", [0, 2, "DNE"]),
        ("Evaluate $\\lim_{x\\to 0}\\dfrac{(3+x)^2-9}{x}$.", 6,
         "Expand: $9+6x+x^2-9=6x+x^2$. Divide by $x$ to get $6+x\\to 6$.", [0, 9, 3]),
        ("Evaluate $\\lim_{x\\to 0}\\dfrac{\\sqrt{x+4}-2}{x}$.", "1/4",
         "Multiply by the conjugate $\\sqrt{x+4}+2$. The numerator becomes $x$, so the quotient is $1/(\\sqrt{x+4}+2)\\to 1/4$.", ["1/2", "0", "2"]),
        ("Evaluate $\\lim_{x\\to -1}\\dfrac{x^2+3x+2}{x+1}$.", 1,
         "$x^2+3x+2=(x+1)(x+2)$. Cancel $x+1$ (valid in a punctured neighborhood) to get $x+2\\to 1$.", [-1, 2, 0]),
        # 11–15 one-sided
        ("For $f(x)=\\begin{cases}x+2&x<1\\\\ 5&x\\ge 1\\end{cases}$, $\\lim_{x\\to 1^-}f(x)$ equals",
         3, "From the left use $x+2$: as $x\\to 1^-$, $x+2\\to 3$.", [5, 1, 2]),
        ("With the same $f$, $\\lim_{x\\to 1^+}f(x)$ equals", 5, "From the right the rule is the constant $5$.", [3, 1, 0]),
        ("If $\\lim_{x\\to 0^-}f(x)=7$ and $\\lim_{x\\to 0^+}f(x)=7$, then $\\lim_{x\\to 0}f(x)$ is",
         7, "Matching finite one-sided limits force the two-sided limit to exist and equal that common value.", ["DNE", 0, 14]),
        ("$\\lim_{x\\to 0^-}\\dfrac{|x|}{x}$ equals", -1,
         "For $x<0$, $|x|=-x$, so $|x|/x=-1$. The left-hand limit is $-1$.", [1, 0, "DNE"]),
        ("$\\lim_{x\\to 3^+}\\sqrt{x-3}$ equals", 0,
         "The domain is $x\\ge 3$, so the right-hand limit exists and is $0$. The left-hand limit does not exist in the reals.", [3, "DNE", 1]),
        # 16–20 infinite / asymptotes
        ("$\\lim_{x\\to 0^+}\\dfrac{1}{x}$ equals", "+∞",
         "Positive values of $x$ make $1/x$ arbitrarily large and positive.", ["-∞", 0, 1]),
        ("The graph of $y=\\dfrac{x+1}{x-2}$ has a vertical asymptote at", "x=2",
         "The denominator vanishes at $x=2$ while the numerator does not, so $|f(x)|\\to\\infty$.", ["x=-1", "y=1", "x=0"]),
        ("$\\lim_{x\\to\\infty}\\dfrac{4x^2-1}{2x^2+5}$ equals", 2,
         "Divide numerator and denominator by $x^2$: the limit of leading coefficients is $4/2=2$ (horizontal asymptote $y=2$).", [4, 0, "+∞"]),
        ("$\\lim_{x\\to 2^-}\\dfrac{1}{x-2}$ equals", "-∞",
         "As $x\\to 2$ from below, $x-2$ is a small negative number, so the reciprocal dives to $-\\infty$.", ["+∞", 0, 2]),
        ("A rational function of equal degree has horizontal asymptote equal to",
         "the ratio of leading coefficients",
         "For large $|x|$ the highest-degree terms dominate, so $y\\to a/b$.",
         ["y=0", "there is never a horizontal asymptote", "the ratio of constant terms"]),
        # 21–25 continuity
        ("Which condition is NOT required for $f$ to be continuous at $x=a$?",
         "f'(a) exists",
         "Continuity needs $f(a)$ defined, $\\lim_{x\\to a}f(x)$ exists, and the two are equal. Differentiability is stronger.",
         ["f(a) is defined", "the two-sided limit exists", "the limit equals f(a)"]),
        ("$f(x)=\\begin{cases}x^2&x\\neq 1\\\\ k&x=1\\end{cases}$ is continuous at $x=1$ when $k$ equals",
         1, "$\\lim_{x\\to 1}x^2=1$, so you must set $f(1)=1$.", [0, 2, "any k"]),
        ("The function $f(x)=|x|$ is continuous at $x=0$ because",
         "lim x→0 |x| = |0| = 0",
         "Both one-sided limits equal $0$, matching $f(0)$. Continuity does not require a derivative.",
         ["it has a corner so it is discontinuous", "left and right limits disagree", "f(0) is undefined"]),
        ("$g(x)=\\dfrac{x^2-9}{x-3}$ has a removable discontinuity at $x=3$ because",
         "the limit exists but g(3) is undefined",
         "Canceling gives $x+3\\to 6$, so the hole can be filled by defining $g(3)=6$.",
         ["both one-sided limits are infinite", "the two-sided limit DNE", "g(3)=0"]),
        ("A jump discontinuity occurs when",
         "the one-sided limits exist and are finite but unequal",
         "That is the AP description of a jump. Infinite one-sided limits are infinite discontinuities; a matching limit with a missing point is removable.",
         ["f(a) is defined", "the function has a vertical tangent", "the limit exists and equals f(a)"]),
        # 26–30 IVT
        ("$f(x)=x^3-x-1$ is continuous on $[1,2]$, $f(1)=-1$, and $f(2)=5$. IVT guarantees a root in",
         "(1,2)",
         "$0$ lies between $f(1)$ and $f(2)$, and $f$ is continuous on the closed interval, so some $c\\in(1,2)$ satisfies $f(c)=0$.",
         ["[0,1]", "only at x=1", "nowhere; IVT never finds roots"]),
        ("IVT requires which hypothesis on $[a,b]$?", "continuity of f on [a,b]",
         "Without continuity, a function can skip values. Differentiability is not required.",
         ["f' exists on [a,b]", "f is a polynomial", "f(a)=f(b)"]),
        ("If $f$ is continuous on $[0,4]$, $f(0)=2$, and $f(4)=10$, which value must $f$ attain?",
         6, "$6$ is strictly between $2$ and $10$, so IVT supplies some $c\\in(0,4)$ with $f(c)=6$.", [12, -1, 0]),
        ("IVT does NOT guarantee that the $c$ it produces is",
         "unique",
         "The theorem is an existence statement. A continuous function may hit the target value several times.",
         ["in (a,b)", "a number where f(c)=k", "dependent on continuity"]),
        ("Why can you not apply IVT to $f(x)=1/x$ on $[-1,1]$ to conclude $f$ hits $0$?",
         "f is not continuous on [-1,1]",
         "$f$ has a vertical asymptote at $x=0$, so the continuity hypothesis fails. (Also $0$ is never an output.)",
         ["f(−1) and f(1) have the same sign", "IVT never applies on closed intervals", "1/x is a polynomial"]),
        # 31–38 medium
        ("Using a graph with an open circle at $(0,4)$ and a filled point at $(0,-1)$, $\\lim_{x\\to 0}f(x)=4$. Then $f$ is discontinuous at $0$ because",
         "the limit does not equal f(0)",
         "The limit exists, but $f(0)=-1\\neq 4$. That is a removable-looking mismatch if the hole can be reassigned.", [4, "the limit DNE", "f is not defined"]),
        ("$\\lim_{x\\to 1}\\dfrac{x^3-1}{x-1}$ equals", 3,
         "$x^3-1=(x-1)(x^2+x+1)$. Cancel to get $x^2+x+1\\to 3$.", [1, 0, "DNE"]),
        ("$\\lim_{x\\to 4^-}\\sqrt{4-x}$ equals", 0,
         "The inside $4-x$ approaches $0$ from the positive side when $x\\to 4^-$.", ["DNE", 2, 4]),
        ("The line $y=0$ is a horizontal asymptote of $y=\\dfrac{5}{x-1}$ because",
         "lim x→∞ f(x) = 0",
         "Degree of the denominator is larger, so the values die out. $x=1$ is the vertical asymptote, not a HA.",
         ["lim x→1 f(x)=0", "f(0)=0", "the function never crosses y=0"]),
        ("For $p(x)=\\begin{cases}3x+1&x\\le 2\\\\ x^2-1&x>2\\end{cases}$, the left-hand limit at $x=2$ equals",
         7, "From the left the rule is $3x+1$, so $3(2)+1=7$.", [3, 2, 4]),
        ("For the same $p$, the right-hand limit at $x=2$ is $2^2-1=3$. Because $7\\neq 3$, the two-sided limit is",
         "DNE", "Unequal finite one-sided limits mean the two-sided limit does not exist.", [7, 3, 5]),
        ("$\\lim_{x\\to\\infty}\\dfrac{7x-2}{x+9}$ equals", 7,
         "Divide by $x$: $(7-2/x)/(1+9/x)\\to 7/1=7$.", [0, 7 / 9, "+∞"]),
        ("If $f$ is continuous at $a$ and $f(a)=8$, then $\\lim_{x\\to a}f(x)$ must be",
         8, "Continuity is exactly the statement that the limit exists and equals the function value.", ["DNE", 0, 1]),
        # 39–46 hard
        ("Find $a$ so that $\\lim_{x\\to 1}\\dfrac{x^2+ax-3}{x-1}$ exists (finite). Then the limit equals",
         4, "Numerator at $x=1$ must vanish: $1+a-3=0$ so $a=2$. Then $(x+3)(x-1)/(x-1)=x+3\\to 4$.", [2, 0, "DNE"]),
        ("$\\lim_{x\\to 0}x^2\\sin(1/x)$ equals", 0,
         "Squeeze: $-x^2\\le x^2\\sin(1/x)\\le x^2$ and both $-x^2$ and $x^2$ go to $0$.", ["DNE", 1, "+∞"]),
        ("$f(x)=\\begin{cases}\\dfrac{\\sin x}{x}&x\\neq 0\\\\ 2&x=0\\end{cases}$ fails to be continuous at $0$ because",
         "the limit is 1 but f(0)=2",
         "The standard limit $\\lim_{x\\to 0}(\\sin x)/x=1\\neq 2$. Redefining $f(0)=1$ would repair it.",
         ["the limit DNE", "sin x is undefined at 0", "f'(0) DNE"]),
        ("Which justification correctly uses IVT to show $x^5+x=1$ has a root in $(0,1)$?",
         "f(0)=0<1<2=f(1) and f(x)=x^5+x is continuous, so some c in (0,1) has f(c)=1",
         "Name the continuous function, check the interval, and sandwich the target value between the endpoints.",
         ["f' is positive so there is a root", "polynomials always have five real roots", "f(0)=0 is already a root of x^5+x=1"]),
        ("$\\lim_{x\\to 2^+}\\dfrac{x-2}{(x-2)^2}$ equals", "+∞",
         "Simplify to $1/(x-2)$. From the right this is a small positive reciprocal.", ["-∞", 0, 1]),
        ("A function has $\\lim_{x\\to 3^-}f(x)=+\\infty$ and $\\lim_{x\\to 3^+}f(x)=-\\infty$. Then $x=3$ is",
         "a vertical asymptote (two-sided infinite discontinuity)",
         "Both sides blow up (in opposite directions). The two-sided finite limit DNE, and $x=3$ is still a VA.",
         ["a hole", "a jump", "a horizontal asymptote"]),
        ("$\\lim_{x\\to -\\infty}\\dfrac{3x^3-x}{6x^3+2}$ equals", "1/2",
         "Equal cubic degree: ratio of leading coefficients $3/6=1/2$.", [3, 0, "+∞"]),
        ("On a graph, $f$ approaches $2$ from the left of $x=-1$ and approaches $2$ from the right, but $f(-1)$ is an open hole. Continuity fails solely because",
         "f(-1) is not defined",
         "The limit exists and equals $2$; filling the hole would restore continuity. This is removable.",
         ["the one-sided limits disagree", "there is a vertical asymptote", "f'(-1)=0"]),
        # 47–55 AP Stretch
        ("AP Stretch: $f(x)=\\begin{cases}\\dfrac{x^2-4}{x-2}&x\\neq 2\\\\ k&x=2\\end{cases}$. For $f$ to be continuous at $2$, and for $\\lim_{x\\to 2}f'(x)$ to be discussed later, the value of $k$ that makes $f$ continuous is",
         4, "Algebraic simplification yields $x+2$ for $x\\neq 2$, so the limit is $4$. Continuity forces $k=4$.", [2, 0, -4]),
        ("AP Stretch: After rewriting the $\\infty-\\infty$ form, $\\lim_{x\\to 0}\\left(\\dfrac{1}{x}-\\dfrac{1}{\\sin x}\\right)$ is equivalent to the $0/0$ limit of",
         "(sin x − x)/(x sin x)",
         "Common denominator $x\\sin x$ produces $(\\sin x-x)/(x\\sin x)$, which is $0/0$ and ready for further analysis.",
         ["(x−sin x)/(x sin x)", "x sin x", "1−1"]),
        ("AP Stretch: Let $f$ be continuous on $[1,4]$ with $f(1)=2$, $f(4)=2$, and $f(2)=9$. Which statement is justified by IVT on $[1,2]$?",
         "f attains the value 5 at least once in (1,2)",
         "$5$ lies between $f(1)=2$ and $f(2)=9$. IVT on the continuous restriction to $[1,2]$ supplies such a point. (Rolle would need $f(1)=f(4)$ and a derivative.)",
         ["f'(c)=0 for some c in (1,4) by IVT", "f has a maximum only at an endpoint", "f never equals 2 again"]),
        ("AP Stretch: $\\lim_{x\\to 0}\\dfrac{\\sqrt{1+x}-\\sqrt{1-x}}{x}$ equals", 1,
         "Multiply by the conjugate of the numerator. The numerator becomes $(1+x)-(1-x)=2x$, and the denominator is $x(\\sqrt{1+x}+\\sqrt{1-x})\\to 2$, so the quotient $\\to 1$.",
         [0, 2, "DNE"]),
        ("AP Stretch: A table of a differentiable $f$ is incomplete at $x=0$. Values: $f(-0.01)=4.96$, $f(-0.001)=4.996$, $f(0.001)=5.004$, $f(0.01)=5.04$. The data are most consistent with",
         "lim x→0 f(x)=5 even if f(0) is unknown",
         "Both sides approach $5$. You cannot yet conclude continuity without $f(0)$, but the two-sided limit estimate is $5$.",
         ["lim DNE because f(0) is missing", "lim=0", "f is discontinuous"]),
        ("AP Stretch: For $g(x)=\\dfrac{(x-1)^2}{x-1}$ when $x\\neq 1$, $\\lim_{x\\to 1^-}g(x)$ and $\\lim_{x\\to 1^+}g(x)$ are",
         "both 0",
         "Simplify to $x-1$. Both one-sided limits of $x-1$ at $1$ are $0$, so the two-sided limit is $0$ (hole at the origin of the simplified line).",
         ["−∞ and +∞", "−1 and 1", "DNE and 0"]),
        ("AP Stretch: Which argument correctly shows $x=0$ is NOT a vertical asymptote of $y=\\dfrac{x}{x}$?",
         "lim x→0 of 1 exists and is 1, so the values stay finite",
         "After canceling, $y=1$ for $x\\neq 0$. A VA requires an infinite one-sided limit.",
         ["the numerator is 0 so there is a VA", "any 0 in a denominator is a VA", "lim x→0 does not exist"]),
        ("AP Stretch: $h$ is defined on $[-2,2]$ except at $0$, with $\\lim_{x\\to 0}h(x)=3$ and $h(x)>10$ for all $x$ in $[1,2]$. Can IVT be used on $[-2,2]$ to conclude $h$ hits $6$?",
         "No: h is not continuous on the whole closed interval",
         "A missing point (or any discontinuity) on $[-2,2]$ blocks IVT on that interval. You would need a subinterval where $h$ is continuous and the endpoint values trap $6$.",
         ["Yes, because the limit at 0 exists", "Yes, because 6 is between 3 and 10", "IVT never needs continuity"]),
        ("AP Stretch: $\\lim_{x\\to\\infty}\\left(\\sqrt{x^2+6x}-x\\right)$ (after rationalizing) equals", 3,
         "Multiply by the conjugate: $(x^2+6x-x^2)/(\\sqrt{x^2+6x}+x)=6x/(\\sqrt{x^2+6x}+x)$. Divide by $x>0$ to get $6/(\\sqrt{1+6/x}+1)\\to 6/2=3$.",
         [0, 6, "+∞"]),
    ])


def build_unit1():
    title = "AP Calculus AB Unit 1: Limits & Continuity"
    description = (
        "Limits from graphs and tables, algebraic techniques, one-sided and infinite limits, "
        "continuity, and IVT justifications — written in AP Calculus AB classroom language."
    )
    concepts = [
        "Limit from a graph and table",
        "Algebraic limits",
        "One-sided limits",
        "Infinite limits and asymptotes",
        "Continuity",
        "IVT",
    ]

    hole = _open_on(
        xy_graph(
            curves=[("#4f46e5", sample_curve(lambda x: 0.35 * x + 2.3, -2, 1.88)),
                    ("#4f46e5", sample_curve(lambda x: 0.35 * x + 2.3, 2.12, 5))],
            points=[(2, 0.8, "f(2)", "#b91c1c")],
            xlim=(-2.5, 5.5), ylim=(-1, 5), w=300, h=260,
        ),
        [(2, 3.0, "hole")],
        xlim=(-2.5, 5.5), ylim=(-1, 5), w=300, h=260,
    )

    c1 = concept_block(
        "1. Limit from a graph and table",
        [
            "On the AP Calculus AB exam, $\\lim_{x\\to a}f(x)=L$ means that the outputs of $f$ get arbitrarily close to $L$ as the inputs get arbitrarily close to $a$, from both sides, whether or not $f(a)$ equals $L$.",
            "A filled point tells you a function value. An open circle tells you a height the graph approaches but does not occupy. The two-sided limit is a statement about nearby heights, not about the ink at $x=a$.",
            "Tables estimate limits by zooming in. If $x$-values on both sides of $a$ produce $y$-values clustering around the same number, that number is the candidate for the limit.",
            "If the left-hand cluster and the right-hand cluster disagree, you must write DNE — “does not exist” — rather than averaging the two heights or reporting $f(a)$.",
            "AP free-response language rewards the sentence: “The limit exists and equals $L$ because the left-hand and right-hand limits both equal $L$.” That one sentence is a complete two-sided justification.",
            "Graph reading is Unit 1 skill one because later derivative and integral FRQs still begin with “from the graph of $f$ or $f'$, determine a limit.”",
        ],
        "If you confuse $f(a)$ with $\\lim_{x\\to a}f(x)$, every continuity, derivative, and FTC argument later in the course will start from the wrong number.",
        "First decide whether you are being asked for a function value, a one-sided limit, or a two-sided limit. Then look only at the matching graphical feature: filled point, open circle, or both sides.",
        lesson_figure(
            hole,
            "A removable-looking hole with a different plotted value",
            "Both branches approach the open circle at $(2,3)$, while $f(2)$ is the filled point lower on the line $x=2$. The limit is $3$, not $f(2)$.",
        )
        + solved(
            1,
            "From the figure, find $\\lim_{x\\to 2}f(x)$ and $f(2)$.",
            [
                "Trace the curve from the left of $x=2$: the $y$-values approach the open circle at height $3$.",
                "Trace from the right: the $y$-values approach the same open circle at height $3$.",
                "The two-sided limit is therefore $3$.",
                "The filled point on $x=2$ is at height $0.8$, so $f(2)=0.8$.",
            ],
            "$\\lim=3$, $f(2)=0.8$",
            "Never average a hole with a filled point.",
            "Easy",
        )
        + solved(
            2,
            "A table gives $f(0.9)=1.82$, $f(0.99)=1.98$, $f(1.01)=2.03$, $f(1.1)=2.21$, and $f(1)$ is blank. Estimate $\\lim_{x\\to 1}f(x)$.",
            [
                "The inputs straddle $1$.",
                "The outputs $1.82,1.98$ from the left and $2.03,2.21$ from the right both crowd near $2$.",
                "The best AP-style estimate is $2$.",
            ],
            "$2$",
            "A missing table entry at the target $x$ does not by itself make a limit fail.",
            "Medium",
        )
        + solved(
            3,
            "A graph shows $\\lim_{x\\to 0^-}f(x)=4$ and $\\lim_{x\\to 0^+}f(x)=-1$. What can you conclude about the two-sided limit and about $f(0)$?",
            [
                "The one-sided limits exist but are unequal, so $\\lim_{x\\to 0}f(x)$ DNE.",
                "The graph may still plot a filled point $f(0)$; that value is independent of the failed two-sided limit.",
                "You may not claim continuity at $0$, because a two-sided limit is required.",
            ],
            "two-sided limit DNE; $f(0)$ cannot salvage it",
            "This is a jump. Write DNE, then name the two one-sided values if the prompt asks.",
            "Honors",
        ),
        ("Reporting $f(a)$ when the question asks for a limit",
         "Circle the word limit in the stem. If you see an open circle at height $L$ and a filled point at height $k$, the limit is $L$ and the value is $k$. Mixing them is the most common Unit 1 graph error on AP multiple choice."),
        ("Write both one-sided limits before you box an answer",
         "On paper: $\\lim_{x\\to a^-}f(x)=\\ldots$ and $\\lim_{x\\to a^+}f(x)=\\ldots$. Only if those two numbers match do you write the two-sided limit. This habit also sets up continuity checks."),
        ["I can read a hole versus a plotted point.", "I can estimate a limit from a table.", "I write DNE when sides disagree."],
        1,
    )

    alg = _open_on(
        xy_graph(
            curves=[("#4f46e5", sample_curve(lambda x: x + 2, -1, 1.88)),
                    ("#4f46e5", sample_curve(lambda x: x + 2, 2.12, 4))],
            dashes=[("v", 2, "x=2")],
            xlim=(-1.5, 4.5), ylim=(-1, 7), w=300, h=260,
        ),
        [(2, 4, "(2,4) hole")],
        xlim=(-1.5, 4.5), ylim=(-1, 7), w=300, h=260,
    )

    c2 = concept_block(
        "2. Algebraic limits",
        [
            "Direct substitution is legal the instant $f$ is a polynomial, a rational function with nonzero denominator, a sine or cosine, an exponential, or any other function known to be continuous at the target.",
            "The $0/0$ indeterminate form is a signal to rewrite, not a signal that the limit is $0$ and not a signal that the limit DNE. Factor, cancel a conjugate, or use a trig identity until substitution is legal.",
            "Canceling $(x-a)$ is valid in a punctured neighborhood of $a$. Graphically you are removing a hole, which is exactly why the rewritten function can be substituted.",
            "Conjugates belong with square roots: multiply top and bottom by $\\sqrt{u}+\\sqrt{v}$ so that a difference of squares produces a factor you can cancel.",
            "AP no-calculator items expect exact answers such as $1/4$, not decimal guesses. Keep the algebra exact until the last substitution.",
            "Algebraic limits are how you justify a derivative from the definition later: the difference quotient is almost always $0/0$ until you rewrite.",
        ],
        "Every derivative rule you memorize is a packaged algebraic limit. If $0/0$ still looks like “undefined, so DNE,” the definition of $f'(a)$ will look undefined too.",
        "Substitute first. If you get a number, stop. If you get $0/0$, factor or conjugate. If you get a nonzero over zero, you are looking at an infinite limit instead.",
        lesson_figure(
            alg,
            "The rewritten line $y=x+2$ with a hole at $x=2$",
            "$(x^2-4)/(x-2)$ agrees with $x+2$ except at $x=2$, where the original expression is undefined.",
        )
        + solved(
            1,
            "Evaluate $\\lim_{x\\to 5}(3x-4)$.",
            ["This is a polynomial, hence continuous.", "Substitute: $3(5)-4=11$."],
            "$11$", "", "Easy",
        )
        + solved(
            2,
            "Evaluate $\\lim_{x\\to 3}\\dfrac{x^2-9}{x-3}$.",
            [
                "Substitution gives $0/0$, so rewrite.",
                "Factor: $x^2-9=(x-3)(x+3)$.",
                "For $x\\neq 3$ the quotient is $x+3$.",
                "Now substitute: $3+3=6$.",
            ],
            "$6$", "The hole is at $(3,6)$.", "Medium",
        )
        + solved(
            3,
            "Evaluate $\\lim_{x\\to 0}\\dfrac{\\sqrt{x+9}-3}{x}$.",
            [
                "Substitution is $0/0$. Multiply by $\\sqrt{x+9}+3$.",
                "Numerator becomes $(x+9)-9=x$.",
                "The fraction simplifies to $1/(\\sqrt{x+9}+3)$.",
                "Substitute $x=0$: $1/(3+3)=1/6$.",
            ],
            "$1/6$", "Write the conjugate in both the numerator and the denominator.", "Hard",
        ),
        ("Calling $0/0$ undefined and stopping",
         "$0/0$ is indeterminate, not a final answer. On AP AB you are expected to factor, cancel, or rationalize until a finite number, $\\pm\\infty$, or a genuine DNE remains."),
        ("Always try substitution for one second before algebra",
         "If substitution already yields a finite number, extra factoring can cancel a factor you were not allowed to cancel (because it was not $0/0$). Let the form tell you the method."),
        ["I substitute when it is legal.", "I rewrite 0/0.", "I treat nonzero/zero as infinite, not as 0/0."],
        6,
    )

    c3 = concept_block(
        "3. One-sided limits",
        [
            "$\\lim_{x\\to a^-}f(x)$ uses only $x<a$. $\\lim_{x\\to a^+}f(x)$ uses only $x>a$. Piecewise definitions are the usual AP setting.",
            "At a breakpoint, evaluate the left piece from the left and the right piece from the right. Do not plug the breakpoint into the wrong formula.",
            "Absolute value splits at $0$: $|x|/x$ is $-1$ for $x<0$ and $+1$ for $x>0$. That single example is the model for every jump built from absolute value.",
            "A square root such as $\\sqrt{x-a}$ has a right-hand limit at $a$ and no real left-hand limit. Domain restrictions create one-sided limits even without a piecewise formula.",
            "The two-sided limit exists if and only if both one-sided limits exist as finite numbers and are equal. Infinite one-sided limits are still “the one-sided limit is $\\infty$,” but they do not create a finite two-sided limit.",
            "Later, differentiability at $a$ will require the two-sided limit of the difference quotient. One-sided derivatives are the same idea with $h\\to 0^\\pm$.",
        ],
        "Jump discontinuities, closed-interval endpoints, and piecewise derivatives all live or die on one-sided limits.",
        "Cover the side of the graph you are not using with your hand. Compute only with the visible piece, then compare.",
        lesson_figure(
            _limit_jump_svg(),
            "A jump at $x=2$: unequal one-sided heights, plus a separate $f(2)$",
            "Open circles mark the heights the pieces approach. The filled point is $f(2)$ and need not match either side.",
        )
        + solved(
            1,
            "Using the figure, estimate $\\lim_{x\\to 2^-}f(x)$.",
            ["From the left the graph is the lower ray, heading toward the open circle at height $3$.", "The left-hand limit is $3$."],
            "$3$", "", "Easy",
        )
        + solved(
            2,
            "For $f(x)=\\begin{cases}2x&x<0\\\\ x+4&x\\ge 0\\end{cases}$, find both one-sided limits at $0$ and decide whether the two-sided limit exists.",
            [
                "Left: $2x\\to 0$.",
                "Right: $x+4\\to 4$.",
                "$0\\neq 4$, so the two-sided limit DNE.",
            ],
            "left $0$, right $4$, two-sided DNE", "", "Medium",
        )
        + solved(
            3,
            "Explain why $\\lim_{x\\to 0^-}\\sqrt{x}$ DNE in the reals while $\\lim_{x\\to 0^+}\\sqrt{x}=0$.",
            [
                "$\\sqrt{x}$ is defined only for $x\\ge 0$.",
                "There are no real inputs immediately to the left of $0$, so the left-hand limit is not a real number.",
                "From the right, $\\sqrt{x}\\to 0$.",
            ],
            "left DNE (domain); right $0$", "Domain is part of a one-sided limit discussion.", "Honors",
        ),
        ("Using the wrong piece at a breakpoint",
         "If the left piece is defined for $x<2$, then $x\\to 2^-$ still uses that left formula. The closed-dot formula is only for the value $f(2)$ and for the side whose inequality includes equality."),
        ("Compute left, compute right, then compare — never average",
         "Averaging $3$ and $4.5$ to report $3.75$ is not a limit. AP readers treat that as a conceptual error, not a rounding issue."),
        ["I evaluate the correct piece.", "I compare one-sided limits.", "I respect domain when a side is empty."],
        11,
    )

    asy = xy_graph(
        curves=[("#4f46e5", sample_curve(lambda x: 1 / (x - 2), -1, 1.85)),
                ("#4f46e5", sample_curve(lambda x: 1 / (x - 2), 2.15, 5))],
        dashes=[("v", 2, "x=2"), ("h", 0, "y=0")],
        xlim=(-1.5, 5.5), ylim=(-4, 4), w=300, h=280,
    )

    c4 = concept_block(
        "4. Infinite limits and asymptotes",
        [
            "An infinite limit $\\lim_{x\\to a}f(x)=+\\infty$ means the outputs grow without bound, not that they “equal infinity.” You still write DNE if the question demands a finite number, but AP also accepts the $\\pm\\infty$ description when it asks for the infinite limit itself.",
            "A vertical asymptote at $x=a$ occurs when at least one one-sided limit is infinite. Cancel common factors first: a canceled $(x-a)$ is a hole, not a VA.",
            "Horizontal asymptotes are limits at infinity. For rationals, compare degrees: larger denominator $\\to y=0$; equal degree $\\to$ ratio of leading coefficients; larger numerator $\\to$ no HA (and often an oblique asymptote, which AB rarely emphasizes).",
            "Sign charts for the factored denominator tell you which side of a VA goes to $+\\infty$ and which goes to $-\\infty$. Test one nearby number on each side.",
            "End behavior $\\lim_{x\\to\\infty}f(x)$ and $\\lim_{x\\to-\\infty}f(x)$ can differ — for example odd-degree over even-degree — so check both directions when a stem says “horizontal asymptotes.”",
            "Infinite limits reappear in improper-integral intuition later, but on AB you mainly need VA/HA identification and one-sided infinity from a rational function.",
        ],
        "Mixing a hole with a vertical asymptote is a high-frequency AP error and it wrecks continuity and derivative-from-graph items.",
        "Factor completely. Canceled factors are holes. Surviving factors in the denominator are vertical asymptotes. Then read degrees for horizontal asymptotes.",
        lesson_figure(
            asy,
            "$y=1/(x-2)$ with vertical asymptote $x=2$ and horizontal asymptote $y=0$",
            "Left of $x=2$ the curve dives to $-\\infty$; right of $x=2$ it explodes to $+\\infty$.",
        )
        + solved(
            1,
            "State $\\lim_{x\\to 0^+}1/x$.",
            ["For small positive $x$, $1/x$ is a large positive number.", "The right-hand limit is $+\\infty$."],
            "$+\\infty$", "", "Easy",
        )
        + solved(
            2,
            "Locate all vertical and horizontal asymptotes of $y=\\dfrac{2x+1}{x-3}$.",
            [
                "Denominator zero at $x=3$, numerator $7\\neq 0$, so VA $x=3$.",
                "Equal degree: HA $y=2/1=2$.",
            ],
            "VA $x=3$, HA $y=2$", "", "Medium",
        )
        + solved(
            3,
            "Determine $\\lim_{x\\to 3^-}\\dfrac{x+1}{x-3}$ and $\\lim_{x\\to 3^+}\\dfrac{x+1}{x-3}$.",
            [
                "Near $x=3$ the numerator is about $4>0$.",
                "Left: $x-3<0$ small, so the quotient is large negative: $-\\infty$.",
                "Right: $x-3>0$ small, so $+\\infty$.",
            ],
            "left $-\\infty$, right $+\\infty$", "A sign chart on $(x-3)$ is the entire argument.", "Hard",
        ),
        ("Calling every zero of a denominator a vertical asymptote",
         "If the same factor appears in the numerator, cancel first. $(x-2)/(x-2)$ has a hole at $x=2$, not a VA. AP loves this trap."),
        ("Write a one-line sign test next to each VA",
         "Pick $x=2.9$ and $x=3.1$, record the sign of each factor, and the infinity directions are then automatic."),
        ["I distinguish holes from VAs.", "I use degrees for HAs.", "I determine left/right infinity with a sign test."],
        16,
    )

    c5 = concept_block(
        "5. Continuity",
        [
            "The AP three-part definition: $f$ is continuous at $a$ if (1) $f(a)$ is defined, (2) $\\lim_{x\\to a}f(x)$ exists as a finite number, and (3) that limit equals $f(a)$.",
            "Polynomials, sine, cosine, and exponential functions are continuous everywhere they are defined. Rational functions are continuous off their denominator zeros. Roots are continuous on their domains.",
            "Removable discontinuities are holes: the limit exists, but $f(a)$ is missing or wrong. Jump discontinuities have unequal finite one-sided limits. Infinite discontinuities have a vertical asymptote.",
            "Piecewise continuity at a breakpoint is a matching problem: compute left limit, right limit, and the defined value, then force them equal by solving for a parameter $k$.",
            "Continuity on a closed interval $[a,b]$ means continuity at every interior point plus one-sided continuity at the endpoints. That is the hypothesis IVT and EVT need.",
            "Differentiability will imply continuity, but continuity will not imply differentiability. Keep the two words separate starting now.",
        ],
        "FTC, MVT, EVT, and IVT all open with “$f$ is continuous on $[a,b]$.” If you cannot certify continuity, you cannot cite those theorems.",
        "Write the three bullets every time. Then fill each bullet with a number. The first bullet that fails is the type of discontinuity.",
        lesson_figure(
            _limit_jump_svg(),
            "Jump discontinuity: one-sided limits exist and disagree",
            "Even if you moved the filled point, the unequal open-circle heights would still block two-sided continuity.",
        )
        + solved(
            1,
            "Is $f(x)=x^2-4$ continuous at $x=3$?",
            ["Polynomials are continuous everywhere.", "$f(3)=5$ equals the limit by substitution."],
            "yes", "", "Easy",
        )
        + solved(
            2,
            "Find $k$ so $f(x)=\\begin{cases}3x-1&x<2\\\\ k&x=2\\\\ x+3&x>2\\end{cases}$ is continuous at $2$.",
            [
                "Left limit: $3(2)-1=5$.",
                "Right limit: $2+3=5$.",
                "The two-sided limit is $5$, so set $k=5$.",
            ],
            "$k=5$", "If the sides had disagreed, no $k$ could save continuity.", "Medium",
        )
        + solved(
            3,
            "Classify the discontinuity of $g(x)=\\dfrac{x^2-1}{x-1}$ at $x=1$, and state how to remove it.",
            [
                "For $x\\neq 1$, $g(x)=x+1$, so the limit is $2$.",
                "$g(1)$ is undefined, so this is removable.",
                "Define $g(1)=2$ to restore continuity.",
            ],
            "removable; set $g(1)=2$", "", "Hard",
        ),
        ("Checking only that $f(a)$ exists",
         "A filled point is necessary but not sufficient. You still need a two-sided limit that matches it. Corners can be continuous; jumps cannot."),
        ("Name the discontinuity type in a sentence",
         "AP FRQ scoring often wants “removable / jump / infinite” plus a reason: limit exists but $f(a)$ missing, or one-sided limits unequal, or an infinite one-sided limit."),
        ["I use the three-part test.", "I solve for k at a breakpoint.", "I classify removable vs jump vs infinite."],
        21,
    )

    c6 = concept_block(
        "6. Intermediate Value Theorem",
        [
            "IVT: If $f$ is continuous on the closed interval $[a,b]$ and $k$ is any number strictly between $f(a)$ and $f(b)$, then there exists at least one $c$ in $(a,b)$ such that $f(c)=k$.",
            "The theorem is an existence result. It does not produce the value of $c$, does not claim uniqueness, and does not require a derivative.",
            "The standard AP root argument: define $f$, cite continuity on $[a,b]$, compute $f(a)$ and $f(b)$ with opposite signs (or with $0$ between them), conclude a root in $(a,b)$.",
            "You may not apply IVT on an interval that contains a discontinuity. $1/x$ on $[-1,1]$ is the classic illegal application.",
            "IVT can be applied on a subinterval. If the interesting values live on $[1,2]$ inside a larger domain, restrict $f$ to that closed subinterval.",
            "EVT (a continuous function on $[a,b]$ attains max and min) is a sibling theorem you will need for optimization. Do not confuse IVT’s “hits every intermediate $y$” with EVT’s “attains extreme $y$.”",
        ],
        "AP readers award the IVT point only when continuity, the interval, and the trapped $y$-value are all named. A vague “it crosses the axis” earns nothing.",
        "Write: continuous on $[a,b]$, $f(a)=\\ldots$, $f(b)=\\ldots$, $k$ between them, therefore some $c\\in(a,b)$ with $f(c)=k$.",
        lesson_figure(
            _ivt_svg(),
            "A continuous graph on $[a,b]$ must cross the line $y=k$",
            "Because $k$ sits between $f(a)$ and $f(b)$, the curve cannot jump over the dashed line.",
        )
        + solved(
            1,
            "Does IVT guarantee that $f(x)=x^3$ attains the value $2$ on $[0,2]$?",
            ["$x^3$ is continuous on $[0,2]$.", "$f(0)=0$ and $f(2)=8$, and $2$ is between them.", "Yes: some $c\\in(0,2)$ has $c^3=2$."],
            "yes", "", "Easy",
        )
        + solved(
            2,
            "Show that $x^3+x-1=0$ has a solution in $(0,1)$.",
            [
                "Let $f(x)=x^3+x-1$, continuous on $[0,1]$ as a polynomial.",
                "$f(0)=-1<0$ and $f(1)=1>0$.",
                "IVT: some $c\\in(0,1)$ has $f(c)=0$.",
            ],
            "a root exists in $(0,1)$", "Do not claim you found $c$.", "Medium",
        )
        + solved(
            3,
            "Why does $f(0)=-2$, $f(1)=5$ fail to guarantee a root of $f$ on $[0,1]$ if $f$ has a jump at $x=1/2$?",
            [
                "IVT’s hypothesis is continuity on the whole closed interval.",
                "A jump means $f$ can skip $0$.",
                "Without continuity, opposite signs are not enough.",
            ],
            "continuity fails, so IVT does not apply", "", "Honors",
        ),
        ("Claiming IVT finds the unique root",
         "IVT never said unique. A cubic can cross the axis three times. Write “at least one $c$.”"),
        ("Copy the theorem’s hypotheses onto the page before the conclusion",
         "Graders look for the words continuous and closed interval. Make them visible. Then display the two endpoint values."),
        ["I cite continuity on a closed interval.", "I trap k between f(a) and f(b).", "I do not claim uniqueness."],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u1_questions()


# ===========================================================================
# UNIT 2: Derivative Definition & Rules
# ===========================================================================

def _u2_questions():
    return _pack([
        ("The derivative $f'(a)$ is defined as",
         "lim h→0 [f(a+h)−f(a)]/h",
         "That limit of the difference quotient, when it exists, is the slope of the tangent line.",
         ["f(a)/a", "lim h→0 f(a+h)", "f(a+h)−f(a)"]),
        ("For $f(x)=x^2$, $f'(3)$ by the definition equals",
         6, "$[ (3+h)^2-9]/h=(6h+h^2)/h=6+h\\to 6$.", [9, 3, 0]),
        ("A secant through $(1,f(1))$ and $(1+h,f(1+h))$ becomes a tangent as",
         "h → 0",
         "The run of the secant shrinks to zero while the slope approaches $f'(1)$.",
         ["h → ∞", "h = 1", "h = f(1)"]),
        ("If $f'(2)$ DNE but $f$ is continuous at $2$, a possible geometric reason is",
         "a corner at x=2",
         "Absolute value at $0$ is the model: continuous, with unequal one-sided difference quotients.",
         ["a hole at x=2", "a horizontal tangent", "f(2)=0"]),
        ("Numerically, $[f(2.01)-f(2)]/0.01$ is an estimate of",
         "f'(2)", "That is a forward difference quotient with $h=0.01$.", ["f(2)", "f''(2)", "∫f"]),
        ("$\\dfrac{d}{dx}[x^5]$ equals", "5x^4", "Power rule: bring down the exponent and subtract one.", ["x^4", "5x^5", "x^6"]),
        ("If $y=x^3\\cdot x^4$, then $y'$ by the product rule (or by first simplifying) is",
         "7x^6", "Simplifying first: $x^7$, derivative $7x^6$. Product rule gives the same.", ["12x^5", "x^6", "7x^7"]),
        ("For $f(x)=(3x-1)(x+2)$, $f'(x)$ equals", "6x+5",
         "Product: $3(x+2)+(3x-1)(1)=3x+6+3x-1=6x+5$.", ["3x+2", "3", "6x-1"]),
        ("$\\dfrac{d}{dx}\\left[\\dfrac{x}{x+1}\\right]$ equals", "1/(x+1)^2",
         "Quotient: $[(1)(x+1)-x(1)]/(x+1)^2=1/(x+1)^2$.", ["1/(x+1)", "x/(x+1)^2", "-1/(x+1)^2"]),
        ("The power rule applied to $x^{-2}$ gives", "-2x^{-3}", "Bring down $-2$ and subtract $1$ from the exponent.", ["2x^{-1}", "-2x^{-1}", "x^{-3}"]),
        ("Chain rule: $\\dfrac{d}{dx}[(3x+1)^4]$ equals", "12(3x+1)^3",
         "Outer power $4u^3$ times inner $3$.", ["(3x+1)^3", "4(3x+1)^3", "12(3x+1)^4"]),
        ("$\\dfrac{d}{dx}\\sin(5x)$ equals", "5 cos(5x)", "Derivative of $\\sin u$ is $\\cos u\\cdot u'$.", ["cos(5x)", "5 sin(5x)", "-5 cos(5x)"]),
        ("If $y=\\sqrt{1+x^2}$, then $y'$ equals", "x/√(1+x^2)",
         "Write $(1+x^2)^{1/2}$. Then $(1/2)(1+x^2)^{-1/2}\\cdot 2x=x/\\sqrt{1+x^2}$.", ["1/(2√(1+x^2))", "√(1+x^2)", "2x"]),
        ("$\\dfrac{d}{dx}e^{x^2}$ equals", "2x e^{x^2}", "Exponential of $u=x^2$: $e^u\\cdot 2x$.", ["e^{x^2}", "2e^{x^2}", "x^2 e^{x^2}"]),
        ("The chain rule fails if you differentiate only the inside and forget the outside. For $\\sin(x^2)$ the wrong answer $2x$ is missing",
         "cos(x^2)", "Correct: $\\cos(x^2)\\cdot 2x$.", ["sin(x^2)", "2", "x^2"]),
        ("$\\dfrac{d}{dx}[\\cos x]$ equals", "-sin x", "Memorize the four: $\\sin'=\\cos$, $\\cos'=-\\sin$, $\\tan'=\\sec^2$, $\\sec'=\\sec\\tan$.", ["sin x", "-cos x", "sec x"]),
        ("$\\dfrac{d}{dx}[\\tan x]$ equals", "sec^2 x", "Quotient of $\\sin/\\cos$ produces $\\sec^2 x$.", ["sec x tan x", "csc^2 x", "-sec^2 x"]),
        ("$\\dfrac{d}{dx}[\\sec x]$ equals", "sec x tan x", "Standard identity from the reciprocal of cosine.", ["sec^2 x", "-sec x tan x", "tan x"]),
        ("At $x=\\pi/2$, $\\dfrac{d}{dx}[\\sin x]$ equals", 0, "$\\cos(\\pi/2)=0$.", [1, -1, "undefined"]),
        ("$\\dfrac{d}{dx}[\\sin x \\cos x]$ equals", "cos 2x",
         "Product: $\\cos^2 x-\\sin^2 x=\\cos 2x$. (Double-angle identity.)", ["1", "sin 2x", "0"]),
        ("$\\dfrac{d}{dx}[e^x]$ equals", "e^x", "The exponential is its own derivative.", ["xe^{x-1}", "ln x", "1/x"]),
        ("$\\dfrac{d}{dx}[\\ln x]$ (for $x>0$) equals", "1/x", "Definition via inverse of $e^x$, or limit of $(1/h)\\ln(1+h/x)$.", ["ln x", "1/(x ln 10)", "e^x"]),
        ("$\\dfrac{d}{dx}[\\ln(3x)]$ equals", "1/x", "Chain: $1/(3x)\\cdot 3=1/x$. Domain $x>0$.", ["3/x", "1/(3x)", "3"]),
        ("$\\dfrac{d}{dx}[a^x]$ for $a>0$, $a\\neq 1$, equals", "a^x ln a", "Rewrite $a^x=e^{x\\ln a}$.", ["x a^{x-1}", "a^x / ln a", "1/(a^x)"]),
        ("$\\dfrac{d}{dx}[\\ln|x|]$ equals", "1/x", "True for $x\\neq 0$. This is why $\\int dx/x=\\ln|x|+C$.", ["1/|x|", "ln x", "x"]),
        ("If $f$ is differentiable at $a$, then $f$ must be",
         "continuous at a",
         "Differentiability implies continuity. The converse is false: $|x|$ at $0$.",
         ["discontinuous at a", "linear", "always increasing"]),
        ("$f(x)=|x-3|$ fails to be differentiable at", 3,
         "Corner: left-hand derivative $-1$, right-hand derivative $+1$.", [0, 1, -3]),
        ("A vertical tangent at $x=a$ typically makes $f'(a)$",
         "fail to exist (infinite slope)",
         "Example: $f(x)=x^{1/3}$ at $0$. Continuous, not differentiable.",
         ["equal 0", "equal 1", "equal f(a)"]),
        ("One-sided derivatives at a corner disagree when",
         "the left- and right-hand difference quotients have different limits",
         "That is the precise test. Continuity can still hold.",
         ["f(a) is undefined", "f is a polynomial", "the limit of f exists"]),
        ("Which function is continuous at $0$ but not differentiable there?",
         "f(x)=|x|",
         "Classic AP example. $x^{1/3}$ is another (vertical tangent rather than a corner).",
         ["f(x)=x^2", "f(x)=e^x", "f(x)=1/x"]),
        ("Using $f(x)=x^2+1$, the difference quotient $[f(2+h)-f(2)]/h$ simplifies to",
         "4+h", "$(4+4h+h^2+1-5)/h=(4h+h^2)/h=4+h$.", ["4", "h", "2+h"]),
        ("$\\dfrac{d}{dx}[(2x-5)(x^2+1)]$ at $x=0$ equals", 2,
         "Product: $2(x^2+1)+(2x-5)(2x)$. At $0$: $2(1)+(-5)(0)=2$.",
         [0, 5, -5]),
        ("At $x=1$, the same product derivative $2(x^2+1)+(2x-5)(2x)$ equals $2(2)+(-3)(2)$, which is",
         -2, "Substitute $x=1$ into the already-differentiated formula: $4-6=-2$.", [1, 3, 4]),
        ("$\\dfrac{d}{dx}\\left[\\dfrac{2x+1}{x-1}\\right]$ equals", "-3/(x-1)^2",
         "Quotient: $[2(x-1)-(2x+1)(1)]/(x-1)^2=(-2-1)/(x-1)^2=-3/(x-1)^2$.", ["2/(x-1)", "3/(x-1)^2", "1/(x-1)^2"]),
        ("$\\dfrac{d}{dx}[\\cos(x^3)]$ equals", "-3x^2 sin(x^3)", "Chain: $-\\sin(u)\\cdot 3x^2$.", ["-sin(x^3)", "3x^2 cos(x^3)", "sin(x^3)"]),
        ("$\\dfrac{d}{dx}[\\ln(x^2+1)]$ equals", "2x/(x^2+1)", "Chain: $1/(x^2+1)\\cdot 2x$.", ["1/(x^2+1)", "2x", "ln(2x)"]),
        ("$\\dfrac{d}{dx}[e^{-3x}]$ equals", "-3e^{-3x}", "Chain with inner $-3$.", ["e^{-3x}", "3e^{-3x}", "-3x e^{-3x}"]),
        ("$f(x)=\\begin{cases}x^2&x\\le 1\\\\ 2x-1&x>1\\end{cases}$. Check $f'(1)$ exists?",
         "yes, f'(1)=2",
         "Value matches: $1=1$. Left derivative $2x|_{1}=2$, right derivative $2$. Both the function and the derivatives match.",
         ["no, corner", "no, jump", "yes, f'(1)=0"]),
        ("The line tangent to $y=\\sqrt{x}$ at $x=4$ has slope", "1/4",
         "$y'=\\frac12 x^{-1/2}$, so $1/(2\\cdot 2)=1/4$.", [2, 1 / 2, 4]),
        ("$\\dfrac{d}{dx}[x\\ln x]$ equals", "1+ln x", "Product: $1\\cdot\\ln x+x\\cdot(1/x)=\\ln x+1$.", ["1/x", "ln x", "x+ln x"]),
        ("If $f'(x)=0$ for all $x$ in an interval, then on that interval $f$ is",
         "constant",
         "Zero derivative means zero slope everywhere, hence a horizontal graph (MVT implies this rigorously later).",
         ["always increasing", "always decreasing", "undefined"]),
        ("$\\dfrac{d}{dx}[\\sec(2x)]$ equals", "2 sec(2x) tan(2x)", "Chain on $\\sec u$.", ["sec(2x) tan(2x)", "2 sec tan 2x without chain", "-2 sec(2x) tan(2x)"]),
        ("A cusp like $f(x)=x^{2/3}$ at $0$ is continuous there but $f'(0)$",
         "DNE (one-sided derivatives infinite with opposite sign)",
         "The graph comes in with a sharp point and vertical-ish sides.",
         ["equals 0", "equals 2/3", "equals ∞ as a real number"]),
        ("$\\lim_{h\\to 0}\\dfrac{\\cos(\\pi+h)-\\cos\\pi}{h}$ equals", 0,
         "This is exactly $\\frac{d}{dx}\\cos x$ at $x=\\pi$, and $-\\sin\\pi=0$.", [-1, 1, "DNE"]),
        ("Quotient $f=u/v$ at a point where $v=0$ but $u\\neq 0$ means $f$ itself is",
         "undefined, so f' is not computed there from the formula",
         "The function must exist in a neighborhood to be differentiable.",
         ["differentiable with infinite derivative", "continuous", "equal to u'"]),
        ("AP Stretch: $f(x)=\\begin{cases}x^2\\sin(1/x)&x\\neq 0\\\\ 0&x=0\\end{cases}$. $f'(0)$ by the definition equals",
         0,
         "Difference quotient $x\\sin(1/x)$ is squeezed between $-|x|$ and $|x|$, hence $\\to 0$.",
         ["DNE", 1, "+∞"]),
        ("AP Stretch: For $g(x)=\\begin{cases}ax+b&x<1\\\\ x^2&x\\ge 1\\end{cases}$ to be differentiable at $1$, the pair $(a,b)$ must be",
         "(2,-1)",
         "Continuity: $a+b=1$. Left derivative $a$, right derivative $2x|_{1}=2$, so $a=2$, hence $b=-1$.",
         ["(1,0)", "(2,1)", "(0,1)"]),
        ("AP Stretch: Let $q(x)=\\dfrac{\\sin(3x)}{e^{2x}}$. After the quotient (or product) rule and chain rule, $q'\\!\\left(\\dfrac{\\pi}{6}\\right)$ equals",
         "-2 e^{-π/3}",
         "$q'(x)=e^{-2x}(3\\cos 3x-2\\sin 3x)$. At $\\pi/6$: $e^{-\\pi/3}(3\\cdot 0-2\\cdot 1)=-2e^{-\\pi/3}$.",
         ["3", "0", "e^{-π/3}"]),
        ("AP Stretch: The difference quotient of $f(x)=1/x$ at $a=2$ is $\\dfrac{1/(2+h)-1/2}{h}$. Combined over a common denominator, this equals $\\dfrac{-1}{2(2+h)}$ for $h\\neq 0,-2$. Therefore $f'(2)$ from the definition is",
         "-1/4",
         "The simplified quotient $\\to -1/4$ as $h\\to 0$. Recalling $f'=-1/x^2$ is not a substitute for rewriting the difference quotient on a no-calculator FRQ.",
         ["-1/2", "1/4", "0"]),
        ("AP Stretch: Let $p(x)=e^{2x}\\tan x$. Then $p'\\!\\left(\\dfrac{\\pi}{4}\\right)$ equals",
         "4 e^{π/2}",
         "Product and chain: $p'=2e^{2x}\\tan x+e^{2x}\\sec^2 x$. At $\\pi/4$: $2e^{\\pi/2}(1)+e^{\\pi/2}(2)=4e^{\\pi/2}$.",
         ["e^{π/2}", "2 e^{π/2}", "4"]),
        ("AP Stretch: $f(x)=|x^2-1|$ is not differentiable at the $x$-values",
         "x=±1",
         "Inside the absolute value is zero at $\\pm 1$, creating corners. At $x=0$ the expression is $1$ and smooth.",
         ["only x=0", "every x", "no x"]),
        ("AP Stretch: Differentiating $y=x^x$ for $x>0$ by writing $y=e^{x\\ln x}$ yields $y'=$",
         "x^x (ln x + 1)",
         "$y'=e^{x\\ln x}\\cdot(\\ln x+1)=x^x(1+\\ln x)$.",
         ["x^{x-1}", "x^x ln x", "e^{x ln x}"]),
        ("AP Stretch: A particle’s position $s$ (meters) at time $t$ (seconds) is $s(1.8)=4.1$, $s(2.0)=5.0$, $s(2.3)=5.7$. The best estimate of instantaneous velocity at $t=2$ uses the surrounding data $\\dfrac{s(2.3)-s(1.8)}{2.3-1.8}$. That estimate, with units and direction, is",
         "3.2 m/s in the positive direction",
         "$(5.7-4.1)/0.5=3.2$. One-sided quotients $4.5$ and $7/3$ discard a neighboring point. Positive sign means motion in the positive $s$-direction.",
         ["4.5 m/s", "0.7 m/s", "3.2 with no direction"]),
        ("AP Stretch: Let $f(x)=\\begin{cases}x^2&x\\le 3\\\\ 6x-9&x>3\\end{cases}$. Compute both one-sided derivatives at $x=3$. Then $f'(3)$",
         "exists and equals 6",
         "Continuity: $9=9$. Left: $2x|_{3}=6$. Right: $6$. Matching one-sided derivatives give $f'(3)=6$.",
         ["DNE because the formulas differ", "equals 0", "equals 9"]),
        ("AP Stretch: $f(x)=|x-1|\\cdot x^2$. Using the definition at the corner candidate $x=1$, $f'_-(1)=$",
         -1,
         "$f(x)=(1-x)x^2=x^2-x^3$ for $x\\le 1$, so $f'=2x-3x^2$ and $f'_-(1)=2-3=-1$. From the right, $f=(x-1)x^2=x^3-x^2$, $f'=3x^2-2x$, $f'_+(1)=1$. Unequal one-sided derivatives, so $f'(1)$ DNE even though $f$ is continuous.",
         [1, 0, 2]),
    ])


def build_unit2():
    title = "AP Calculus AB Unit 2: Derivative Definition & Rules"
    description = (
        "Difference quotients, power/product/quotient/chain rules, trigonometric and exponential/"
        "logarithmic derivatives, and the distinction between continuity and differentiability."
    )
    concepts = [
        "Definition as limit of difference quotient",
        "Power/product/quotient",
        "Chain rule",
        "Trig derivatives",
        "Exponential and log derivatives",
        "Differentiability vs continuity",
    ]

    c1 = concept_block(
        "1. Definition as limit of difference quotient",
        [
            "The official definition is $f'(a)=\\lim_{h\\to 0}\\dfrac{f(a+h)-f(a)}{h}$, provided the limit exists as a finite number. An equivalent form is $\\lim_{x\\to a}\\dfrac{f(x)-f(a)}{x-a}$.",
            "Geometrically the numerator is a rise and the denominator is a run, so the quotient is the slope of a secant. Sending $h\\to 0$ rotates that secant onto the tangent line.",
            "Units matter: if $s$ is in meters and $t$ in seconds, $s'(t)$ is meters per second. AP related-rates and PVA items later will demand those units in a sentence.",
            "The definition is how you prove the power rule and how you handle piecewise corners. When a stem writes the limit of a difference quotient, recognize it as a derivative and evaluate the known rule at the point.",
            "Numerical estimates use small $h$: forward $[f(a+h)-f(a)]/h$, backward $[f(a)-f(a-h)]/h$, or symmetric $[f(a+h)-f(a-h)]/(2h)$. Symmetric is usually more accurate on AP calculator items.",
            "If the two-sided limit of the difference quotient DNE, $f$ is not differentiable at $a$, even if $f$ is continuous there.",
        ],
        "Every later slope, velocity, and linearization is this limit. If the definition is fuzzy, the chain rule looks like magic instead of a composed difference quotient.",
        "Write the limit with parentheses around the entire numerator. Expand, cancel $h$, then substitute $h=0$. That three-step algebra is the whole method.",
        lesson_figure(
            _secant_tangent_svg(),
            "Secants approaching the tangent to $y=x^2/4$ at $P(2,1)$",
            "The dashed secant has a slightly different slope from the solid tangent. As the second intersection point slides toward $P$, those slopes meet at $f'(2)=1$.",
        )
        + solved(
            1,
            "Use the definition to find $f'(1)$ for $f(x)=3x+2$.",
            [
                "Difference quotient: $[3(1+h)+2-(5)]/h=(3+3h+2-5)/h=3h/h=3$.",
                "The limit as $h\\to 0$ is $3$.",
            ],
            "$3$", "A linear function’s derivative is its slope.", "Easy",
        )
        + solved(
            2,
            "Use the definition to find $f'(2)$ for $f(x)=x^2$.",
            [
                "$[(2+h)^2-4]/h=(4+4h+h^2-4)/h=4+h$.",
                "$\\lim_{h\\to 0}(4+h)=4$.",
            ],
            "$4$", "Matches power rule $2x$ at $x=2$.", "Medium",
        )
        + solved(
            3,
            "Identify $\\lim_{h\\to 0}\\dfrac{\\sqrt{9+h}-3}{h}$ as a derivative and evaluate it.",
            [
                "This is $f'(9)$ for $f(x)=\\sqrt{x}$, because $f(9)=3$.",
                "$f'(x)=\\frac12 x^{-1/2}$, so $f'(9)=1/(2\\cdot 3)=1/6$.",
                "You could also rationalize; both routes are AP-legal.",
            ],
            "$1/6$", "Recognizing “this limit is $f'(a)$” saves time on no-calculator MC.", "Honors",
        ),
        ("Forgetting to cancel $h$ and then claiming the limit DNE because of division by zero",
         "After expanding, $h$ must cancel for a differentiable function. If it does not cancel, check your algebra before you write DNE."),
        ("Translate every $\\lim_{h\\to 0}[f(a+h)-f(a)]/h$ into “$f'(a)$” in the margin",
         "Then use a rule if you know $f$. The definition form is often a disguise, not a request to grind binomials."),
        ["I can expand a difference quotient.", "I can interpret a secant becoming a tangent.", "I recognize disguised f'(a) limits."],
        1,
    )

    c2 = concept_block(
        "2. Power, product, and quotient rules",
        [
            "Power rule: $\\dfrac{d}{dx}[x^n]=n x^{n-1}$ for real $n$ (with domain restrictions for non-integer $n$). Constants have derivative $0$; $c\\cdot f$ scales the derivative by $c$.",
            "Product rule: $(uv)'=u'v+uv'$. Say it as “derivative of the first times the second, plus the first times derivative of the second.” Never differentiate only one factor.",
            "Quotient rule: $\\left(\\dfrac{u}{v}\\right)'=\\dfrac{u'v-uv'}{v^2}$. Low d-high minus high d-low, over low squared. The minus sign is not optional.",
            "Sometimes simplifying first is faster: $(x^3)(x^4)=x^7$. Both orders must agree; that is a check, not a different theory.",
            "These rules assume $u$ and $v$ are already differentiable. If a factor has a corner, the product may inherit a corner.",
            "On AP, a quotient that is really a product with a negative power ($x^{-1}$) can be handled either way; pick the algebra you are less likely to sign-error.",
        ],
        "Product and quotient errors propagate into related rates and logarithmic differentiation. Getting the minus sign in the quotient rule right is worth a full FRQ point every year.",
        "Write $u$ and $v$ in a mini table with $u'$ and $v'$ before combining. That two-second table prevents dropping a factor.",
        lesson_figure(
            xy_graph(
                curves=[("#94a3b8", sample_curve(lambda x: x, -1, 3)),
                        ("#f59e0b", sample_curve(lambda x: 0.4 * x * x + 0.5, -1, 3)),
                        ("#4f46e5", sample_curve(lambda x: x * (0.4 * x * x + 0.5), -1, 2.2))],
                xlim=(-1.2, 3.2), ylim=(-1, 8), w=300, h=260, ylab="y",
            ),
            "A product $uv$: the purple graph is the pointwise product of the gray line and the gold parabola",
            "The slope of the product is not the product of the slopes; it is $u'v+uv'$.",
        )
        + solved(
            1,
            "Differentiate $y=7x^4-2x+5$.",
            ["Power rule termwise: $28x^3-2$.", "The constant vanishes."],
            "$28x^3-2$", "", "Easy",
        )
        + solved(
            2,
            "Differentiate $y=(x^2+1)(3x-4)$.",
            ["$u=x^2+1$, $u'=2x$, $v=3x-4$, $v'=3$.", "$y'=2x(3x-4)+(x^2+1)(3)=6x^2-8x+3x^2+3=9x^2-8x+3$."],
            "$9x^2-8x+3$", "", "Medium",
        )
        + solved(
            3,
            "Differentiate $y=\\dfrac{2x+1}{x^2+1}$ and evaluate $y'(0)$.",
            [
                "$u'=2$, $v'=2x$.",
                "$y'=[2(x^2+1)-(2x+1)(2x)]/(x^2+1)^2=(2x^2+2-4x^2-2x)/(x^2+1)^2=(-2x^2-2x+2)/(x^2+1)^2$.",
                "$y'(0)=2/1=2$.",
            ],
            "$y'(0)=2$", "Keep the denominator squared even after you plug in a number.", "Hard",
        ),
        ("Using $(uv)'=u'v'$",
         "That formula is false. If it were true, the derivative of $x\\cdot x$ would be $1\\cdot 1=1$, but $(x^2)'=2x$. The extra terms in the product rule are mandatory."),
        ("Say “low d-high minus high d-low” out loud",
         "The minus sign is the entire difficulty of the quotient rule. Writing $v$ first in the numerator (“low d-high”) prevents flipping it."),
        ["I apply power termwise.", "I use a u/v table for products and quotients.", "I simplify first when it is clearly cheaper."],
        6,
    )

    c3 = concept_block(
        "3. Chain rule",
        [
            "If $y=f(g(x))$, then $y'=f'(g(x))\\cdot g'(x)$. Differentiate the outer function, keep the inner function unchanged, then multiply by the inner derivative.",
            "Every $u^{n}$, $\\sin u$, $e^{u}$, and $\\ln u$ item on AB is a chain-rule item. Missing the extra factor $u'$ is the most common calculator-inactive error in this unit.",
            "Nested chains compose: $\\sin(e^{x^2})$ needs three factors. Work from the outside in, and do not skip a layer.",
            "After differentiating, you may still need to simplify for a later slope or for setting $y'=0$. Factoring out a common $e^{u}$ or a power of $u$ is good style.",
            "The chain rule is why FTC with variable limits produces $f(g(x))g'(x)$. You are meeting that pattern early.",
            "Units still multiply: if the outer function converts meters to square meters and the inner converts seconds to meters, the chain product has units square meters per second.",
        ],
        "Related rates are the chain rule with respect to time. If chain rule is weak, the ladder problem in Unit 3 is impossible even when the geometry is easy.",
        "Circle the outer function. Write its derivative with the inner copied. Then multiply by a boxed inner derivative. Three visual pieces, three factors.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: math.sin(x * x / 3), -3.2, 3.2))],
                xlim=(-3.5, 3.5), ylim=(-1.6, 1.6), w=300, h=240,
            ),
            "$y=\\sin(x^2/3)$ oscillates faster as $|x|$ grows",
            "The inner $x^2$ makes the frequency change; that changing inner speed is exactly the extra $2x/3$ from the chain rule.",
        )
        + solved(
            1,
            "Differentiate $y=(5x-2)^3$.",
            ["Outer $u^3$, inner $5x-2$.", "$y'=3(5x-2)^2\\cdot 5=15(5x-2)^2$."],
            "$15(5x-2)^2$", "", "Easy",
        )
        + solved(
            2,
            "Differentiate $y=\\sin(4x)$.",
            ["Outer sine, inner $4x$.", "$y'=\\cos(4x)\\cdot 4=4\\cos(4x)$."],
            "$4\\cos(4x)$", "", "Medium",
        )
        + solved(
            3,
            "Differentiate $y=e^{\\cos(x^2)}$.",
            [
                "Outermost exponential: $e^{u}$ with $u=\\cos(x^2)$.",
                "Then $u'=-\\sin(x^2)\\cdot 2x$.",
                "$y'=e^{\\cos(x^2)}\\cdot(-2x\\sin(x^2))$.",
            ],
            "$-2x\\sin(x^2)\\,e^{\\cos(x^2)}$", "Three layers, three factors.", "Honors",
        ),
        ("Differentiating the inside only",
         "$\\dfrac{d}{dx}\\sin(x^2)$ is not $2x$. You dropped $\\cos(x^2)$. Conversely, $\\cos(x^2)$ alone is also incomplete. Both factors are required."),
        ("Count the function layers on your fingers before you write",
         "If you count three layers, your answer must be a product of three derivatives. That counting check catches almost every chain-rule miss."),
        ["I copy the inner function into the outer derivative.", "I multiply by inner'.", "I can nest two or three chains."],
        11,
    )

    c4 = concept_block(
        "4. Trigonometric derivatives",
        [
            "The four you must have cold: $(\\sin x)'=\\cos x$, $(\\cos x)'=-\\sin x$, $(\\tan x)'=\\sec^2 x$, $(\\sec x)'=\\sec x\\tan x$. Reciprocal cofunctions $(\\csc,\\cot)$ appear less often but follow the “negative cofunction” pattern.",
            "The derivative of cosine being negative is a unit-circle fact: in the first quadrant, cosine is decreasing, so its derivative (which is $-\\sine$) is negative.",
            "Chain rule rides along: $(\\sin(u))'=\\cos(u)u'$. Arguments like $5x$ or $x^2$ are not optional extras.",
            "Product and quotient of trig functions should be simplified with identities only when it clearly helps; $\\sin 2x=2\\sin x\\cos x$ is the identity that shows up most.",
            "Radian measure is required. If a stem gives degrees, convert before differentiating, because $(\\sin x)^\\circ$ is not $\\cos x$ in degree mode.",
            "These derivatives are the engine for harmonic related rates (a rotating beacon, a Ferris wheel) and for later integrals of sine and cosine.",
        ],
        "A sign error on $(\\cos x)'$ will flip every later max/min of a sinusoidal model and will wreck slope fields that involve trigonometric right-hand sides.",
        "Write the chain-rule skeleton first: $\\cos(u)\\cdot u'$. Then fill $u$. Do not multiply $\\cos$ by the inner before applying cosine to $u$.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(math.sin, -3.2, 3.2)),
                        ("#dc2626", sample_curve(math.cos, -3.2, 3.2))],
                xlim=(-3.4, 3.4), ylim=(-1.6, 1.6), w=300, h=240,
            ),
            "$y=\\sin x$ (purple) and $y=\\cos x$ (red), which is the slope function of sine",
            "Where sine has a horizontal tangent, cosine is $0$. Where sine is increasing, cosine is positive.",
        )
        + solved(
            1,
            "Find $\\dfrac{d}{dx}[\\cos x]$ at $x=\\pi$.",
            ["The derivative is $-\\sin x$.", "$-\\sin\\pi=0$."],
            "$0$", "", "Easy",
        )
        + solved(
            2,
            "Differentiate $y=\\tan(3x)$.",
            ["$y'=\\sec^2(3x)\\cdot 3=3\\sec^2(3x)$."],
            "$3\\sec^2(3x)$", "", "Medium",
        )
        + solved(
            3,
            "Differentiate $y=\\sin x\\cos x$ and simplify.",
            ["Product: $\\cos x\\cos x+\\sin x(-\\sin x)=\\cos^2 x-\\sin^2 x=\\cos 2x$."],
            "$\\cos 2x$", "Recognizing the double-angle identity is AP style, not required if you leave $\\cos^2-\\sin^2$.", "Hard",
        ),
        ("Dropping the negative on cosine",
         "Memory aid: sine and cosine alternate, and cosine is the first one that needs a minus when you continue the cycle $\\sin,\\cos,-\\sin,-\\cos$."),
        ("Keep arguments in radians on no-calculator paper",
         "Write $\\pi/6$, not $30^\\circ$, once a derivative is in play. Degree mode is a calculator-section trap."),
        ["I know the four core trig derivatives.", "I attach chain-rule factors.", "I can combine product + trig."],
        16,
    )

    c5 = concept_block(
        "5. Exponential and logarithmic derivatives",
        [
            "$(e^x)'=e^x$. That is the characterizing property of the natural exponential, and it is why $e$ is the convenient base for calculus.",
            "$(a^x)'=a^x\\ln a$ for $a>0$. Rewrite $a^x=e^{x\\ln a}$ if you forget the extra $\\ln a$.",
            "$(\\ln x)'=1/x$ for $x>0$. More generally $(\\ln|x|)'=1/x$ for $x\\neq 0$, which is the antiderivative you will need in Unit 5.",
            "Logarithmic differentiation handles $y=x^x$ and messy quotients: take $\\ln|y|$, differentiate implicitly, then solve for $y'$. This is still AB content when the resulting derivatives are elementary.",
            "Chain rule again: $(e^{u})'=e^{u}u'$ and $(\\ln u)'=u'/u$. Missing $u'$ is the same error as in the trigonometric case.",
            "Exponential growth models $y=Ce^{kt}$ have $y'=kCe^{kt}=ky$. That differential equation is Unit 7; the derivative computation is now.",
        ],
        "Without $1/x$ and $e^{u}u'$, you cannot differentiate an accumulation of a rate that is exponential, and you cannot solve separable growth equations later.",
        "If the exponent is anything but $x$, you are in chain-rule territory. If the input of $\\ln$ is anything but $x$, same warning.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: math.exp(0.5 * x), -2, 2.4)),
                        ("#dc2626", sample_curve(lambda x: 0.5 * math.exp(0.5 * x), -2, 2.4))],
                xlim=(-2.2, 2.6), ylim=(-0.4, 4), w=300, h=250,
            ),
            "$y=e^{x/2}$ and its derivative $y'=\\frac12 e^{x/2}$",
            "The slope graph is a constant multiple of the original exponential — the fingerprint of $y'=ky$.",
        )
        + solved(
            1,
            "Differentiate $y=e^{3x}$.",
            ["$y'=e^{3x}\\cdot 3=3e^{3x}$."],
            "$3e^{3x}$", "", "Easy",
        )
        + solved(
            2,
            "Differentiate $y=\\ln(5x)$.",
            ["$y'=\\dfrac{1}{5x}\\cdot 5=\\dfrac{1}{x}$ for $x>0$."],
            "$1/x$", "The $5$ cancels. Domain still excludes $x\\le 0$.", "Medium",
        )
        + solved(
            3,
            "Differentiate $y=x^x$ for $x>0$.",
            [
                "Write $y=e^{x\\ln x}$.",
                "Then $y'=e^{x\\ln x}\\cdot(\\ln x+x\\cdot 1/x)=x^x(\\ln x+1)$.",
            ],
            "$x^x(1+\\ln x)$", "Logarithmic differentiation is the clean AP write-up.", "Honors",
        ),
        ("Using $(\\ln x)'=\\ln x$ or $(e^x)'=xe^{x-1}$",
         "Those are power-rule hallucinations. Exponential and log are their own families. Power rule applies to $x^n$ with $n$ constant, not to $x^x$ and not to $e^x$ viewed as “$e$ to a power” in the power-rule sense."),
        ("Convert $a^x$ to $e^{x\\ln a}$ when your memory of $\\ln a$ wobbles",
         "The conversion makes the chain rule mechanical and prevents dropping $\\ln a$."),
        ["I differentiate e^u with the extra u'.", "I differentiate ln u as u'/u.", "I can handle x^x by rewriting."],
        21,
    )

    c6 = concept_block(
        "6. Differentiability versus continuity",
        [
            "Theorem: if $f$ is differentiable at $a$, then $f$ is continuous at $a$. Proof sketch: $f(a+h)-f(a)=\\left(\\dfrac{f(a+h)-f(a)}{h}\\right)\\cdot h\\to f'(a)\\cdot 0=0$.",
            "The converse is false. Corners ($|x|$), cusps ($x^{2/3}$), and vertical tangents ($x^{1/3}$) are continuous but not differentiable.",
            "A jump or a hole already fails continuity, so it automatically fails differentiability. You never need a difference quotient once continuity has failed.",
            "Piecewise differentiability at a breakpoint requires two matches: the function values (continuity) and the one-sided derivatives (equal finite slopes).",
            "On a graph, a sharp point, a break, or a vertical tangent is enough to write “$f'$ DNE.” A horizontal tangent is a perfectly valid derivative of $0$.",
            "AP language: “$f$ is continuous at $a$ but $f'(a)$ does not exist because the one-sided derivatives are unequal.” That sentence is worth a point.",
        ],
        "Later first-derivative tests assume $f'$ exists on an open interval except possibly at isolated critical points. Knowing why $f'$ can fail keeps you from applying a sign chart on a jump.",
        "Check continuity first. If it fails, stop. If it holds, compare left- and right-hand derivatives. Only then claim $f'(a)$.",
        lesson_figure(
            _corner_svg(),
            "$y=|x|$ is continuous at $0$ with a corner, so $f'(0)$ DNE",
            "Left-hand secants have slope $-1$; right-hand secants have slope $+1$. Those limits of difference quotients never meet.",
        )
        + solved(
            1,
            "Is $f(x)=x^2$ differentiable at $0$?",
            ["It is a polynomial, hence differentiable everywhere.", "$f'(x)=2x$, so $f'(0)=0$ (a horizontal tangent, which is allowed)."],
            "yes, $f'(0)=0$", "", "Easy",
        )
        + solved(
            2,
            "Explain why $f(x)=|x-2|$ is not differentiable at $2$.",
            [
                "Continuous: $f(2)=0$ matches both sides.",
                "Left-hand derivative is $-1$; right-hand derivative is $+1$.",
                "Unequal one-sided derivatives $\\Rightarrow f'(2)$ DNE.",
            ],
            "$f'(2)$ DNE (corner)", "", "Medium",
        )
        + solved(
            3,
            "Find $a$ and $b$ so $f(x)=\\begin{cases}ax+b&x<0\\\\ e^x&x\\ge 0\\end{cases}$ is differentiable at $0$.",
            [
                "Continuity: $b=e^0=1$.",
                "Left derivative $a$; right derivative $e^x$ at $0$ is $1$.",
                "So $a=1$, $b=1$. Then $f(x)=e^x$ for $x\\ge 0$ and $x+1$ for $x<0$, matching value and slope.",
            ],
            "$a=1$, $b=1$", "Two equations, two unknowns: value match and slope match.", "Honors",
        ),
        ("Thinking a horizontal tangent is non-differentiable",
         "Slope $0$ is the most differentiable-looking tangent you can have. Non-differentiable pictures are corners, cusps, breaks, and vertical tangents."),
        ("Always test one-sided derivatives at a piecewise joint",
         "Matching $f$ is only half of the job. Write $f'_-(a)$ and $f'_+(a)$ explicitly."),
        ["I know differentiability implies continuity.", "I can name corner/cusp/vertical tangent.", "I can solve for parameters that make a piecewise f differentiable."],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u2_questions()


# ===========================================================================
# UNIT 3: Applications of Derivatives I
# ===========================================================================

def _u3_questions():
    return _pack([
        ("The line tangent to $y=x^2$ at $x=3$ has slope", 6, "$y'=2x$, so $2\\cdot 3=6$. Point $(3,9)$.", [9, 3, 2]),
        ("An equation of that tangent line is", "y-9=6(x-3)",
         "Point-slope with slope $6$ through $(3,9)$.", ["y-3=6(x-9)", "y=6x", "y-9=2(x-3)"]),
        ("The linearization of $f$ at $a$ is $L(x)=$", "f(a)+f'(a)(x-a)",
         "That is the tangent-line function, used to approximate $f$ near $a$.", ["f'(a)(x-a)", "f(a)+f'(x)", "f(a)x"]),
        ("Using $L(x)$ for $f(x)=\\sqrt{x}$ at $a=9$, an approximation of $\\sqrt{9.2}$ is", 3.033,
         "$f'(x)=1/(2\\sqrt{x})$, $f'(9)=1/6$. $L(9.2)=3+(1/6)(0.2)=3.033\\ldots$. Closest listed value $3.033$.",
         [3.2, 2.967, 9.1]),
        ("A tangent line overestimates $f$ near $a$ when $f$ is",
         "concave down (f''<0)",
         "The graph sits below its tangents when concave down.",
         ["concave up", "linear", "increasing"]),
        ("A 13-ft ladder leans against a wall. If the foot is 5 ft from the wall, the top is",
         12, "Pythagoras: $y=\\sqrt{169-25}=12$.", [13, 5, 8]),
        ("In that ladder, $x^2+y^2=169$. Differentiating with respect to $t$ yields",
         "2x x'+2y y'=0",
         "Implicit related rates: every length that changes gets a factor of its $t$-derivative.",
         ["2x+2y=0", "x'+y'=0", "x x'+y=0"]),
        ("If $x=5$, $y=12$, and $x'=2$ ft/s (foot sliding away), then $y'$ in ft/s is",
         "-5/6", " $2(5)(2)+2(12)y'=0\\Rightarrow 20+24y'=0\\Rightarrow y'=-5/6$.", ["5/6", "-2", "2"]),
        ("A related-rates answer must include",
         "units (and a sign for increasing/decreasing)",
         "AP FRQ scoring: numeric value without units is incomplete; a negative derivative means the quantity is decreasing.",
         ["only a positive number", "an antiderivative", "a slope field"]),
        ("Water fills a cone. Similar triangles relate $r$ and $h$ before you",
         "differentiate V=(1/3)π r^2 h with respect to t",
         "Reduce to one variable using the cone’s fixed proportions, then differentiate.",
         ["integrate both sides", "set r=h always without similar triangles", "use MVT"]),
        ("If $s(t)=t^3-6t^2$, then velocity $v(t)=s'(t)$ is", "3t^2-12t",
         "Differentiate position to get velocity.", ["3t^2-6t", "t^3-6t", "6t-12"]),
        ("For that particle, $v(t)=0$ at $t=$", "0 and 4",
         "$3t(t-4)=0$.", ["2 only", "6", "never"]),
        ("Acceleration is $a(t)=v'(t)$. For $v(t)=3t^2-12t$, $a(2)$ equals", 0,
         "$a(t)=6t-12$, so $a(2)=12-12=0$.", [6, 12, -12]),
        ("Speed is", "|v(t)|", "Speed is nonnegative; velocity carries a sign (direction).", ["v(t)", "a(t)", "s(t)"]),
        ("The particle moves right when", "v(t)>0",
         "Positive velocity means increasing position (typical AP convention on a line).",
         ["a(t)>0", "s(t)>0", "v(t)=0"]),
        ("$f$ is increasing on an interval where", "f'(x)>0",
         "Positive slope means rising $y$-values (strictly, on an interval).",
         ["f'(x)<0", "f''(x)>0", "f(x)>0"]),
        ("A sign chart for $f'$ with zeros at $x=1$ and $x=4$ and signs $+,-,+$ means $f$ decreases on",
         "(1,4)", "Wherever $f'$ is negative, $f$ is decreasing.", ["(-∞,1)", "(4,∞)", "only at x=1"]),
        ("If $f'(x)=(x-2)^2$, then $f$ is",
         "increasing on R (critical point at 2 is not a turn)",
         "$f'\\ge 0$ always and is zero only at an isolated point, so $f$ is still increasing through $x=2$.",
         ["decreasing on R", "has a local max at 2", "has a local min at 2"]),
        ("The graph of $f$ has a horizontal tangent where", "f'(x)=0",
         "Slope zero. That is a critical point if $f'$ exists.", ["f(x)=0", "f''(x)=0", "f'(x)>0"]),
        ("On $(0,\\infty)$, $f(x)=\\ln x$ is increasing because",
         "f'(x)=1/x>0",
         "The derivative test, not the fact that $\\ln$ “looks increasing.”",
         ["f(x)>0", "f''(x)<0", "ln 1=0"]),
        ("A critical number of $f$ is an interior point where",
         "f'=0 or f' DNE, and f is defined",
         "Endpoints of a closed interval are candidates for absolute extrema but are not called critical numbers in the open-interval sense.",
         ["f=0", "f''=0", "f is discontinuous"]),
        ("First derivative test: $f'$ changes from $+$ to $-$ at $c$ means",
         "local maximum at c",
         "The graph rises, then falls.",
         ["local minimum at c", "inflection at c", "no extremum"]),
        ("If $f'$ changes $-$ to $+$ at $c$, then $f$ has a",
         "local minimum at c",
         "Falls, then rises.",
         ["local maximum at c", "vertical asymptote", "jump"]),
        ("If $f'$ does not change sign at a zero of $f'$, then at that $x$ there is",
         "no local extremum",
         "Example $(x-1)^3$: flat tangent, still increasing.",
         ["always a max", "always a min", "a jump"]),
        ("The first derivative test requires a sign chart of",
         "f' on both sides of the critical number",
         "A single value $f'(c)=0$ does not tell max vs min by itself.",
         ["f only", "f'' only at endpoints", "the original table of f(a)"]),
        ("EVT: a continuous $f$ on $[a,b]$ attains its absolute max and min. Candidates are",
         "critical numbers in (a,b) and the endpoints a,b",
         "Evaluate $f$ at that finite list; the largest output is the absolute max.",
         ["only where f''=0", "only endpoints", "only where f=0"]),
        ("On $[0,3]$, $f(x)=x^2-4x+1$ has $f'(x)=2x-4=0$ at $x=2$. The candidate $x$-values are",
         "0, 2, and 3",
         "Endpoints plus the interior critical number.",
         ["only 2", "only 0 and 3", "1,2,3"]),
        ("For that $f$, $f(0)=1$, $f(2)=-3$, $f(3)=-2$. The absolute minimum on $[0,3]$ is",
         -3, "Smallest candidate value is $f(2)=-3$.", [1, -2, 0]),
        ("If $f'$ DNE at an interior point where $f$ is defined (a corner), that $x$ is",
         "still a critical number and must be tested",
         "$|x|$ on $[-1,1]$ has its min at the corner $x=0$.",
         ["ignored", "automatically a max", "a vertical asymptote"]),
        ("An absolute extremum on an open interval may fail to exist because",
         "there are no endpoints, so f may be unbounded or never attain a bound",
         "EVT needs a closed interval. $1/x$ on $(0,1]$ has no absolute max.",
         ["f' is never zero", "polynomials never have extrema", "IVT forbids extrema"]),
        ("Linearization of $f(x)=e^x$ at $0$ is $L(x)=$", "1+x",
         "$f(0)=1$, $f'(x)=e^x$, $f'(0)=1$, so $L(x)=1+x$.", ["e^x", "x", "1-x"]),
        ("Using $L(x)=1+x$, $e^{0.1}$ is approximately", 1.1, "Substitute $0.1$ into $1+x$.", [0.1, 1.01, 2.1]),
        ("A balloon’s radius increases at $2$ cm/s. $V=\\frac43\\pi r^3$, so $dV/dt=$",
         "4π r^2 dr/dt",
         "Chain rule / related rates: $4\\pi r^2 r'$.",
         ["4π r^2", "(4/3)π r^2", "4π r dr/dt"]),
        ("At $r=5$ cm with $dr/dt=2$, $dV/dt$ in cm$^3$/s is", "200π",
         "$4\\pi(25)(2)=200\\pi$.", ["20π", "100π", "40π"]),
        ("If $s(t)=t^2-4t$, the particle is at rest when $t=$", 2,
         "$v=2t-4=0\\Rightarrow t=2$.", [0, 4, 1]),
        ("For $s(t)=t^2-4t$ on $[0,5]$, displacement $s(5)-s(0)$ equals", 5,
         "$s(5)=5$, $s(0)=0$, displacement $5$. (Distance traveled is larger because of the turn at $t=2$.)",
         [9, 0, -5]),
        ("Distance traveled on $[0,5]$ for that particle is $|s(2)-s(0)|+|s(5)-s(2)|=$",
         13, "$s(2)=-4$, $s(0)=0$, $s(5)=5$: $4+9=13$.", [5, 9, 4]),
        ("$f'(x)=x(x-3)$. $f$ increases on",
         "(-∞,0] ∪ [3,∞)  (allowing isolated zeros)",
         "Sign chart: $f'$ is positive outside $[0,3]$ and negative on $(0,3)$.",
         ["(0,3)", "only at 0", "everywhere"]),
        ("First derivative test at $x=0$ for $f'(x)=x(x-3)$: signs of $f'$ go from $+$ to $-$, so $x=0$ is a",
         "local maximum",
         "Left of $0$, both factors negative, product positive; between $0$ and $3$, product negative.",
         ["local minimum", "neither", "inflection only"]),
        ("On $[1,4]$, $f(x)=x+4/x$ (for $x>0$). $f'(x)=1-4/x^2=0$ when $x=$",
         2, "$x^2=4$, and $x>0$ so $x=2$.", [4, -2, 1]),
        ("Candidates on $[1,4]$ for that $f$ are $x=1,2,4$. Then $f(1)=5$, $f(2)=4$, $f(4)=5$. Absolute min is",
         4, "Smallest candidate output is $4$.", [5, 1, 2]),
        ("If $v(t)<0$ and $a(t)>0$, the particle is",
         "moving left but slowing down (speed decreasing)",
         "Velocity and acceleration have opposite signs $\\Leftrightarrow$ speeding down (speed decreasing).",
         ["moving right and speeding up", "at rest", "moving left and speeding up"]),
        ("The tangent to $y=\\ln x$ at $x=1$ is", "y=x-1",
         "$f(1)=0$, $f'(x)=1/x$, $f'(1)=1$, so $y=0+1(x-1)$.", ["y=x", "y=1", "y=ln x"]),
        ("A shadow problem: similar triangles, then differentiate both sides with respect to",
         "t (time)",
         "Related rates always differentiate the geometric relation in $t$, not in the similar-triangle ratio alone.",
         ["x only", "the angle only", "area"]),
        ("If $f'(x)>0$ on $(a,c)$ and on $(c,b)$ but $f'(c)=0$, then $f$ on $(a,b)$ is still",
         "increasing (no sign change)",
         "An isolated root of $f'$ does not create a turn.",
         ["decreasing", "constant", "undefined at c"]),
        ("AP Stretch: A 10-ft ladder slides. $x^2+y^2=100$, $x=6$ ft, $dx/dt=3$ ft/s. Using implicit differentiation, $dy/dt$ is",
         "-9/4",
         "$y=8$, $2(6)(3)+2(8)y'=0\\Rightarrow 36+16y'=0\\Rightarrow y'=-36/16=-9/4$ ft/s.",
         ["-3", "9/4", "-6/8"]),
        ("AP Stretch: A conical tank (vertex down) has height 12 ft and top radius 4 ft. Water height $h$ ft, $V=\\frac13\\pi r^2 h$, and $r=h/3$ by similar triangles. Then $dV/dt=$",
         "(π h^2 / 9) dh/dt",
         "$V=\\frac13\\pi (h/3)^2 h=\\pi h^3/27$, so $V'=(\\pi h^2/9)h'$.",
         ["π h^2 dh/dt", "(1/3)π r^2 dh/dt without substituting r", "4π h dh/dt"]),
        ("AP Stretch: $s(t)=t^3-6t^2+9t$ on $[0,4]$. The particle’s speed is greatest at an endpoint or a critical point of speed. $v(t)=3(t-1)(t-3)$. The maximum speed on $[0,4]$ is",
         9,
         "$v(0)=9$, $v(1)=0$, $v(3)=0$, $v(4)=12-48+9=-3$? $v(t)=3t^2-12t+9$, $v(4)=48-48+9=9$. Speeds $|v|$ at candidates: $9,0,0,9$. Max speed $9$.",
         [0, 3, 12]),
        ("AP Stretch: $f'(x)=(x-1)^2(x-4)$. Sign chart: $f'$ is negative on $(-\\infty,4)$ except at $x=1$ where $f'=0$, and positive on $(4,\\infty)$. Then $f$ has",
         "a local min at x=4 and no local extremum at x=1",
         "No sign change at the even-multiplicity factor $(x-1)^2$. Sign change $-$ to $+$ at $x=4$.",
         ["local max at 1 and min at 4", "local max at 4", "extrema at both 1 and 4"]),
        ("AP Stretch: Linearization of $f(x)=\\sqrt[3]{x}$ at $a=8$ is used to estimate $\\sqrt[3]{8.24}$. Compute $f(8)$, $f'(8)$, and $L(8.24)$. The estimate equals",
         2.02,
         "$f(8)=2$. $f'(x)=\\frac13 x^{-2/3}$, so $f'(8)=\\frac13\\cdot 8^{-2/3}=\\frac13\\cdot\\frac14=\\frac1{12}$. Then $L(8.24)=2+\\frac1{12}(0.24)=2.02$.",
         [2.24, 2.08, 8.24]),
        ("AP Stretch: On $[0,2\\pi]$, $f(x)=x+2\\sin x$. Critical numbers satisfy $1+2\\cos x=0$, so $x=2\\pi/3,4\\pi/3$. Comparing $f$ at those points and the endpoints, the absolute maximum value is",
         "2π",
         "$f(0)=0$, $f(2\\pi/3)=2\\pi/3+\\sqrt{3}$, $f(4\\pi/3)=4\\pi/3-\\sqrt{3}$, $f(2\\pi)=2\\pi$. Numerically $2\\pi$ is largest, so the abs max is the right endpoint value.",
         ["2π/3+√3", "0", "4π/3-√3"]),
        ("AP Stretch: A particle has velocity $v(t)=t^2-4$ m/s on $0\\le t\\le 3$ with $s(0)=1$ m. After locating the rest time in $[0,3]$ and splitting $\\int|v|$, the distance traveled on $[0,3]$ is",
         "23/3",
         "Rest at $t=2$ only. $\\int_0^2(4-t^2)\\,dt+\\int_2^3(t^2-4)\\,dt=16/3+7/3=23/3$ m. Net displacement $\\int_0^3 v=-3$ is smaller because of the sign change.",
         ["3", "9", "16/3"]),
        ("AP Stretch: A conical tank, vertex down, has height $12$ ft and top radius $4$ ft. Water leaks with $dV/dt=-2$ ft$^3$/min when the water is $h=3$ ft deep. Similar triangles give $r=h/3$, so $V=\\pi h^3/27$. Then $dh/dt$ at that instant is",
         "-2/π",
         "$V'=(\\pi h^2/9)h'$. At $h=3$: $-2=\\pi h'$, so $h'=-2/\\pi$ ft/min.",
         ["-2", "2π", "-18/π"]),
        ("AP Stretch: $f$ is continuous on $[0,5]$, differentiable on $(0,5)$, $f'(x)>0$ on $(0,2)$, $f'(x)<0$ on $(2,5)$. The absolute maximum on $[0,5]$ occurs at",
         "x=2",
         "First derivative test plus EVT: the only turn is a local max at $2$, and you still compare $f(2)$ with $f(0)$ and $f(5)$. The stem’s sign pattern makes $f(2)$ larger than nearby values; with $f'$ positive then negative, $f(2)\\ge f(0)$ and $f(2)\\ge f(5)$ on this interval, so the abs max is at $x=2$.",
         ["x=0 only", "x=5 only", "every critical point equally"]),
        ("AP Stretch: A conical pile of sand has height always equal to the base radius. $V=\\frac13\\pi r^3$. If $dV/dt=12\\pi$ ft$^3$/min when $r=2$ ft, implicit differentiation gives $dr/dt=$",
         3,
         "$V'=\\pi r^2 r'$. At $r=2$: $12\\pi=\\pi\\cdot 4\\cdot r'$, so $r'=3$ ft/min. The similar-triangle constraint $h=r$ is already built into $V$.",
         [12, 3 / 4, 2]),
    ])


def build_unit3():
    title = "AP Calculus AB Unit 3: Applications of Derivatives I"
    description = (
        "Tangent lines and linearization, related rates with implicit time derivatives, particle motion, "
        "increasing/decreasing tests, the first derivative test, and EVT candidate lists."
    )
    concepts = [
        "Tangent line and linearization",
        "Related rates",
        "Position velocity acceleration",
        "Increasing/decreasing",
        "First derivative test",
        "Candidates for extrema",
    ]

    c1 = concept_block(
        "1. Tangent line and linearization",
        [
            "The tangent line to $y=f(x)$ at $x=a$ is $y=f(a)+f'(a)(x-a)$, provided $f'(a)$ exists. That formula is both a geometric object and a function $L(x)$ called the linearization.",
            "Linearization is the AP language for “use the tangent line to approximate $f(a+\\Delta x)$.” The error is small when $\\Delta x$ is small, and the concavity of $f$ tells you whether $L$ over- or underestimates.",
            "If $f''>0$ (concave up), the graph lies above its tangents, so $L(x)$ underestimates $f(x)$. If $f''<0$, $L$ overestimates. That one sentence is a frequent AP justification.",
            "Units of $L(x)$ match units of $f(x)$. The factor $f'(a)$ has units of $f$ per unit $x$, times $(x-a)$, restoring the units of $f$.",
            "Differentials write $dy=f'(x)\\,dx$. Numerically $dy$ is the same increment as $L(x)-f(a)$. Either notation is acceptable on AB if you identify $dx=\\Delta x$.",
            "A horizontal tangent ($f'(a)=0$) is still a tangent line: $y=f(a)$. It is not a failure of linearization.",
        ],
        "Related rates, Newton’s method (rarely tested on AB), and local error estimates all start from this line. If point-slope is shaky, every later approximation FRQ leaks points.",
        "Compute $f(a)$ and $f'(a)$ first, then write point-slope, then substitute the nearby $x$. Do not skip the middle sentence $y-f(a)=f'(a)(x-a)$.",
        lesson_figure(
            svg_parabola(h=2, k=1, lim=6),
            "A parabola $y=(x-2)^2+1$ with horizontal tangent at the vertex $(2,1)$",
            "Linearization at a vertex uses $f'(a)=0$, so $L(x)=f(a)$. Concavity ($f''>0$) means this tangent underestimates nearby values.",
        )
        + solved(
            1,
            "Find the tangent line to $y=x^2$ at $x=2$.",
            ["$y'=2x$, so slope $4$. Point $(2,4)$.", "$y-4=4(x-2)$, or $y=4x-4$."],
            "$y=4x-4$", "", "Easy",
        )
        + solved(
            2,
            "Use linearization of $f(x)=\\sqrt{x}$ at $a=4$ to approximate $\\sqrt{4.2}$.",
            [
                "$f(4)=2$, $f'(x)=1/(2\\sqrt{x})$, $f'(4)=1/4$.",
                "$L(x)=2+\\frac14(x-4)$.",
                "$L(4.2)=2+0.05=2.05$.",
            ],
            "$2.05$", "True $\\sqrt{4.2}\\approx 2.049$; slightly high because $f''<0$.", "Medium",
        )
        + solved(
            3,
            "Does the tangent to $f(x)=e^x$ at $0$ over- or underestimate $e^{0.2}$? Justify with concavity.",
            [
                "$L(x)=1+x$, so $L(0.2)=1.2$.",
                "$f''(x)=e^x>0$, so $f$ is concave up.",
                "The graph lies above its tangent: $L$ underestimates $e^{0.2}$.",
            ],
            "underestimate, because $f''>0$", "Name $f''$ and the above/below tangent fact.", "Honors",
        ),
        ("Using the secant through $(a,f(a))$ and the nearby point as if it were the tangent",
         "The tangent uses $f'(a)$, which is a limit of secants, not a particular secant with $h=0.2$ unless the problem asks for a numerical estimate of the derivative itself."),
        ("Box $f(a)$ and $f'(a)$ before writing $L(x)$",
         "Most algebra errors come from mixing the value and the slope. Two boxed numbers, then point-slope."),
        ["I can write point-slope from f(a) and f'(a).", "I can use L(x) to approximate.", "I can justify over/under with concavity."],
        1,
    )

    c2 = concept_block(
        "2. Related rates",
        [
            "Related rates problems ask how fast one quantity changes given how fast another changes. The hidden tool is the chain rule with respect to time $t$, even when the picture is geometry.",
            "Method: draw and label, write an equation relating the variables, reduce extra variables with similar triangles or a constraint, differentiate both sides with respect to $t$, then substitute the instant of interest.",
            "Never substitute the instant before differentiating if that quantity is changing. Constants (a 13-ft ladder’s length) may be substituted earlier; changing lengths may not.",
            "Implicit differentiation is normal: $x^2+y^2=\\ell^2$ becomes $2x x'+2y y'=0$. Solve for the unknown rate and include a sign.",
            "Units: if $x$ is in feet and $t$ in seconds, $x'$ is ft/s. Volume rates are ft$^3$/s. AP readers look for units in the final sentence.",
            "Similar triangles in a cone or a shadow convert two variables into one before you differentiate. That substitution is the difference between a correct $V=\\pi h^3/27$ and an incorrect leftover $r$.",
        ],
        "This is the first time AB students must differentiate an implicit geometric constraint in $t$. The same muscle is used for related-rates FRQs every year.",
        "List what is given with units, what is asked with units, and which equation connects them. Differentiate, then plug in the snapshot values.",
        lesson_figure(
            _ladder_svg(),
            "Ladder sliding away from a wall: $x^2+y^2=\\ell^2$",
            "As $x$ increases, $y$ decreases. The implicit relation forces $x x'+y y'=0$, so the rates have opposite signs.",
        )
        + solved(
            1,
            "A square’s side is $6$ cm and increasing at $2$ cm/s. How fast is the area increasing?",
            ["$A=s^2$, so $A'=2s s'$.", "At the instant: $2\\cdot 6\\cdot 2=24$ cm$^2$/s."],
            "$24$ cm$^2$/s", "", "Easy",
        )
        + solved(
            2,
            "A 13-ft ladder has its foot $5$ ft from the wall, sliding away at $2$ ft/s. How fast is the top descending?",
            [
                "$x^2+y^2=169$, $y=12$.",
                "$2x x'+2y y'=0$.",
                "$2(5)(2)+2(12)y'=0\\Rightarrow y'=-5/6$ ft/s.",
                "The top is descending at $5/6$ ft/s.",
            ],
            "$\\dfrac{5}{6}$ ft/s downward", "The negative sign is the descent.", "Medium",
        )
        + solved(
            3,
            "An inverted cone (vertex down) is $10$ ft high with top radius $5$ ft. Water is $6$ ft deep and rising at $0.4$ ft/s. How fast is the volume increasing?",
            [
                "Similar triangles: $r/h=5/10=1/2$, so $r=h/2$.",
                "$V=\\frac13\\pi r^2 h=\\frac13\\pi (h/2)^2 h=\\pi h^3/12$.",
                "$V'=(\\pi h^2/4)h'$. At $h=6$, $h'=0.4$: $V'=(\\pi\\cdot 36/4)(0.4)=9\\pi\\cdot 0.4=3.6\\pi$ ft$^3$/s.",
            ],
            "$3.6\\pi$ ft$^3$/s", "Substitute $r$ in terms of $h$ before differentiating.", "Honors",
        ),
        ("Plugging the snapshot values into the geometric equation before differentiating the changing variables",
         "If you replace $x$ by $5$ in $x^2+y^2=169$ and only then differentiate, you destroy the $x'$ term. Differentiate the identity first; substitute the instant second."),
        ("Draw, equation, reduce, differentiate, plug, units",
         "That six-word checklist is the entire FRQ rubric. Skipping “reduce” (similar triangles) is the usual cone error."),
        ["I differentiate constraints with respect to t.", "I substitute r in terms of h in a cone.", "I report units and a sign."],
        6,
    )

    c3 = concept_block(
        "3. Position, velocity, acceleration",
        [
            "On a line, $s(t)$ is position, $v(t)=s'(t)$ is velocity, and $a(t)=v'(t)=s''(t)$ is acceleration. Speed is $|v(t)|$.",
            "The particle moves right (or up, depending on the axis) when $v>0$, left when $v<0$, and is at rest when $v=0$. Changing direction requires $v$ to change sign, not merely to equal zero (a touch-and-go with no sign change is not a turn).",
            "Speeding up means velocity and acceleration have the same sign; slowing down means opposite signs. That is an AP sentence you should memorize verbatim.",
            "Displacement on $[t_1,t_2]$ is $s(t_2)-s(t_1)=\\int_{t_1}^{t_2}v(t)\\,dt$ (net signed change). Distance traveled is $\\int_{t_1}^{t_2}|v(t)|\\,dt$, which requires splitting at zeros of $v$.",
            "A sign chart of $v$ is the same tool as a sign chart of $f'$ for increasing/decreasing. PVA is the first-derivative test in motion language.",
            "Units: if $s$ is meters and $t$ seconds, $v$ is m/s and $a$ is m/s$^2$. FRQ answers without units lose the units point.",
        ],
        "Half of AP AB particle-motion FRQs are this vocabulary plus a sign chart. Mixing speed with velocity is a guaranteed lost point.",
        "Make three stacked number lines: $v$ signs, $a$ signs, and a row that says “speeding up / slowing down.” Read the story off the chart.",
        lesson_figure(
            _pva_svg(),
            "Position $s(t)$ (blue) peaking where velocity $v(t)$ (red) is zero",
            "The particle turns when velocity changes sign. After the turn, $s$ decreases as $v$ is negative.",
        )
        + solved(
            1,
            "If $s(t)=t^2-6t$, find $v(t)$ and the time the particle is at rest.",
            ["$v(t)=2t-6$.", "$v=0$ when $t=3$."],
            "$v=2t-6$; at rest at $t=3$", "", "Easy",
        )
        + solved(
            2,
            "For $s(t)=t^3-3t$, determine when the particle is moving right on $[-2,2]$.",
            [
                "$v(t)=3t^2-3=3(t-1)(t+1)$.",
                "Sign chart: $3(t^2-1)$ is positive when $|t|>1$.",
                "On $[-2,2]$, moving right on $[-2,-1)\\cup(1,2]$. (At $\\pm 1$ it is instantaneously at rest.)",
            ],
            "moving right when $|t|>1$ inside the interval", "", "Medium",
        )
        + solved(
            3,
            "For $s(t)=t^2-4t$ on $[0,5]$, compute displacement and distance traveled.",
            [
                "$v=2t-4$, rest at $t=2$.",
                "Displacement $s(5)-s(0)=5-0=5$.",
                "Distance $|s(2)-s(0)|+|s(5)-s(2)|=|-4-0|+|5-(-4)|=4+9=13$.",
            ],
            "displacement $5$; distance $13$", "Split the integral of $|v|$ at the turn.", "Honors",
        ),
        ("Calling $v=0$ a change of direction without a sign chart",
         "$v$ can touch zero and bounce back to the same sign (think $v=t^2$). No sign change means no turn. Always check signs on both sides."),
        ("Write “speed $=|v|$” and “speeding up iff $v$ and $a$ share a sign”",
         "Those two sentences are cheap points. Put them on the page before you compute."),
        ["I distinguish velocity, speed, and acceleration.", "I split distance at v=0 with a sign change.", "I use the same-sign test for speeding up."],
        11,
    )

    c4 = concept_block(
        "4. Increasing and decreasing",
        [
            "If $f'(x)>0$ on an interval, then $f$ is increasing there. If $f'(x)<0$, $f$ is decreasing. Isolated zeros of $f'$ do not break the monotonicity if the sign does not change.",
            "The practical tool is a sign chart of $f'$: mark zeros and discontinuities of $f'$ (the critical numbers and any vertical asymptotes of $f'$), then test a point in each open interval.",
            "Write the conclusion in interval notation for $x$, not for $y$. “$f$ is increasing on $(1,4)$” is the AP sentence.",
            "A horizontal tangent with no sign change — $f'(x)=(x-2)^2$ — means $f$ is still increasing (or still decreasing) through that $x$. The graph flattens but does not turn.",
            "This test assumes $f$ is differentiable on the open intervals you name. At a corner you use one-sided derivatives or just read the graph.",
            "Increasing/decreasing is how you justify a local max or min in the next lesson and how you sketch a graph in Unit 4.",
        ],
        "Without a sign chart, the first derivative test is a slogan instead of a proof. AP wants the chart or an equivalent sign argument.",
        "Factor $f'$ completely. Plot the zeros on a number line. Test one easy number in each gap. Then write increasing/decreasing intervals.",
        lesson_figure(
            _sign_chart_svg([-1, 2], ["+", "-", "+"], label="f′"),
            "Sign chart of $f'$ with critical numbers at $x=-1$ and $x=2$",
            "$f$ increases, then decreases, then increases. Those three intervals are the entire increasing/decreasing story.",
        )
        + solved(
            1,
            "If $f'(x)=x-4$, where is $f$ increasing?",
            ["$f'>0$ when $x>4$.", "$f$ is increasing on $(4,\\infty)$."],
            "$(4,\\infty)$", "", "Easy",
        )
        + solved(
            2,
            "For $f'(x)=x(x-3)$, give the intervals where $f$ is decreasing.",
            [
                "Zeros at $0$ and $3$.",
                "Test $x=-1$: $(-1)(-4)>0$. Test $x=1$: $(1)(-2)<0$. Test $x=4$: positive.",
                "$f$ decreases on $(0,3)$.",
            ],
            "$(0,3)$", "", "Medium",
        )
        + solved(
            3,
            "Explain why $f'(x)=(x-1)^2(x+2)$ being zero at $x=1$ does not mean $f$ decreases on one side of $1$.",
            [
                "$(x-1)^2$ is always nonnegative and does not change the sign of $f'$.",
                "The only sign change of $f'$ is at $x=-2$.",
                "At $x=1$, $f$ flattens but continues in the same monotonic direction.",
            ],
            "no sign change at $x=1$", "Even multiplicity $\\Rightarrow$ no turn.", "Honors",
        ),
        ("Listing the zeros of $f'$ as the increasing intervals",
         "The zeros are the partitions. The intervals between them, with a sign attached, are the answer. “$f$ increases at $x=2$” is not interval language."),
        ("Factor, number line, test points, write intervals",
         "Four steps, every time. Skipping the test point and guessing from the leading term is how sign errors happen."),
        ["I build an f' sign chart.", "I write increasing/decreasing in interval notation.", "I treat even-multiplicity zeros as non-turns."],
        16,
    )

    c5 = concept_block(
        "5. First derivative test",
        [
            "First derivative test: if $c$ is a critical number and $f'$ changes from positive to negative at $c$, then $f(c)$ is a local maximum. From negative to positive: local minimum. No sign change: neither.",
            "You must still confirm $f$ is continuous at $c$. A vertical asymptote of $f$ is not a local extremum even if $f'$ changes sign across it.",
            "The test is local: it compares $f(c)$ with $f$ in some open neighborhood, not on a whole closed interval. Absolute extrema need the candidate list in the next lesson.",
            "A table of $f'$ signs is a complete justification. You do not need $f''$ for this test (that is the second derivative test, Unit 4).",
            "If $f'(c)$ DNE because of a corner, the first derivative test still applies using one-sided signs of $f'$. The absolute-value V has a local (and global) min at the corner.",
            "AP FRQ phrasing: “$f'$ changes from positive to negative at $x=c$, so $f$ has a local maximum at $x=c$.” Cite the sign change explicitly.",
        ],
        "This is how you classify critical points when $f''$ is messy or zero. Curve sketching and optimization both call this test by name.",
        "Find critical numbers, build the $f'$ sign chart, then read $+/\\to-$ or $-/\\to+$ at each number. Write local max/min/neither.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: 0.15 * (x + 2) * (x - 1) * (x - 3) + 1.2, -2.6, 3.6))],
                points=[(-2, 1.2, "loc max?"), (1, 1.2, "loc min"), (3, 1.2, "loc max")],
                xlim=(-3, 4), ylim=(-2, 4), w=300, h=250,
            ),
            "A cubic-shaped graph whose turning points are classified by $f'$ sign changes",
            "Each marked $x$ must be checked: does $f'$ actually change sign, or is it a flat inflection of $f'$?",
        )
        + solved(
            1,
            "If $f'$ changes from $-$ to $+$ at $x=3$, classify $f(3)$.",
            ["Negative to positive means the graph falls, then rises.", "Local minimum at $x=3$."],
            "local min at $x=3$", "", "Easy",
        )
        + solved(
            2,
            "For $f'(x)=x(x-4)$, classify the critical numbers of $f$.",
            [
                "Zeros at $0$ and $4$.",
                "Signs: $+$ on $(-\\infty,0)$, $-$ on $(0,4)$, $+$ on $(4,\\infty)$.",
                "Local max at $0$; local min at $4$.",
            ],
            "local max at $0$, local min at $4$", "", "Medium",
        )
        + solved(
            3,
            "Given $f'(x)=(x-2)^2(x-5)$, classify $x=2$ and $x=5$.",
            [
                "$(x-2)^2$ does not change sign. Test: $f'$ is negative on $(-\\infty,5)$ except at $2$, and positive after $5$.",
                "$x=2$: no local extremum.",
                "$x=5$: $-$ to $+$, local minimum.",
            ],
            "neither at $2$; local min at $5$", "", "Honors",
        ),
        ("Declaring a local max just because $f'(c)=0$",
         "$f'(c)=0$ is a critical number, not a classification. Without a sign change you have no local extremum. $(x-1)^3$ is the picture to remember."),
        ("Write “f' changes from … to …” in the justification",
         "Those eight words are the first-derivative-test point on an FRQ. A circled max on a graph without the sign sentence may not earn it."),
        ["I classify using f' sign changes.", "I can handle f' DNE at a corner.", "I do not confuse local with absolute."],
        21,
    )

    c6 = concept_block(
        "6. Candidates for extrema (closed interval)",
        [
            "Extreme Value Theorem: a function continuous on a closed, bounded interval $[a,b]$ attains both an absolute maximum and an absolute minimum.",
            "The candidates theorem: those extrema occur at a critical number in $(a,b)$ or at an endpoint $a$ or $b$. The method is therefore a finite list: solve $f'=0$, include $f'$ DNE points, include $a$ and $b$, evaluate $f$ at each survivor.",
            "The largest list value is the absolute max; the smallest is the absolute min. You must actually compare the numbers — a local max in the interior might lose to an endpoint.",
            "If the interval is open, EVT does not apply. $f$ may have no absolute extrema even if it has local ones.",
            "Domain restrictions (a vertical asymptote inside $[a,b]$) destroy the EVT hypothesis because $f$ is then not continuous on the whole closed interval.",
            "Optimization in Unit 4 is this candidate list plus a geometry constraint. Master the list now with a plain formula $f(x)$ on $[a,b]$.",
        ],
        "Every “find the maximum on $[0,4]$” AP item is this algorithm. Missing an endpoint is the most expensive arithmetic-free error in the unit.",
        "Write the list $x=\\ldots$ before you compute any $y$-values. Then make a two-column table of $x$ versus $f(x)$. Circle the extreme outputs.",
        lesson_figure(
            svg_plane(points=[(0, 1, "end"), (2, -4, "crit"), (5, 5, "end")], lim=6, line=(0, 1, 5, 5)),
            "EVT candidates plotted: endpoints and an interior critical point",
            "The purple segment is only a visual aid, not the graph of $f$. Absolute extrema are decided by comparing the three $y$-values, not by how a chord looks.",
        )
        + solved(
            1,
            "List EVT candidates for $f(x)=x^2$ on $[-1,2]$.",
            ["$f'=2x=0$ at $x=0$.", "Endpoints $x=-1,2$.", "Candidates: $-1,0,2$."],
            "$x=-1,0,2$", "", "Easy",
        )
        + solved(
            2,
            "Find the absolute max and min of $f(x)=x^2-4x$ on $[0,5]$.",
            [
                "$f'=2x-4=0$ at $x=2$.",
                "$f(0)=0$, $f(2)=-4$, $f(5)=5$.",
                "Abs min $-4$ at $x=2$; abs max $5$ at $x=5$.",
            ],
            "min $-4$, max $5$", "", "Medium",
        )
        + solved(
            3,
            "Why can you not use EVT to conclude that $f(x)=1/x$ attains a maximum on $(0,1]$?",
            [
                "The interval is not closed at $0$.",
                "As $x\\to 0^+$, $f(x)\\to+\\infty$, so there is no absolute max.",
                "EVT’s closed-interval hypothesis is essential.",
            ],
            "open at $0$; $f$ unbounded", "", "Honors",
        ),
        ("Forgetting endpoints",
         "A beautiful interior critical point can still lose to $f(a)$ or $f(b)$. If the interval is closed, the endpoints are always on the list."),
        ("Table of values, not a vague “the vertex looks higher”",
         "Compute the candidate outputs. AP wants the numbers. A graph sketch is supporting evidence, not a replacement for the table."),
        ["I list critical numbers and endpoints.", "I evaluate f at every candidate.", "I know EVT needs a closed interval and continuity."],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u3_questions()


# ===========================================================================
# UNIT 4: Applications of Derivatives II
# ===========================================================================

def _u4_questions():
    return _pack([
        ("$f$ is concave up on an interval where", "f''(x)>0",
         "Positive second derivative means the slopes of $f$ are increasing, so the graph bends up.",
         ["f''(x)<0", "f'(x)>0", "f(x)>0"]),
        ("An inflection point requires $f$ to change concavity, not merely",
         "f''(c)=0",
         "$f''=0$ is a candidate. $(x-1)^4$ has $f''=0$ at $1$ with no concavity change.",
         ["f to be continuous", "f' to exist nearby", "a sign chart of f''"]),
        ("If $f''(x)=6x$, then $f$ is concave down on",
         "(-∞,0)", "$f''<0$ for $x<0$.", ["(0,∞)", "only at 0", "everywhere"]),
        ("Second derivative test: $f'(c)=0$ and $f''(c)>0$ implies",
         "local minimum at c",
         "Concave up at a horizontal tangent is a valley.",
         ["local maximum at c", "inflection at c", "no conclusion"]),
        ("If $f'(c)=0$ and $f''(c)=0$, the second derivative test",
         "is inconclusive; use the first derivative test",
         "You must go back to an $f'$ sign chart.",
         ["proves a max", "proves a min", "proves an inflection"]),
        ("MVT requires $f$ continuous on $[a,b]$ and differentiable on",
         "(a,b)",
         "Open interval for differentiability; closed for continuity.",
         ["[a,b] for differentiability too, always", "only at a", "nowhere"]),
        ("Rolle’s theorem is MVT in the special case",
         "f(a)=f(b), so some c has f'(c)=0",
         "The secant is horizontal, hence some tangent is horizontal.",
         ["f'(a)=0", "f is linear", "f''>0"]),
        ("For $f(x)=x^2$ on $[1,3]$, MVT guarantees some $c$ in $(1,3)$ with $f'(c)=$",
         4, "$(f(3)-f(1))/(3-1)=(9-1)/2=4$, and $2c=4$ so $c=2$, which lies in $(1,3)$.", [2, 8, 1]),
        ("You may not apply MVT to $f(x)=|x|$ on $[-1,1]$ because",
         "f is not differentiable at 0",
         "Continuity holds, but the open-interval differentiability hypothesis fails at the corner.",
         ["f(-1)≠f(1)", "f is not continuous", "MVT never applies to even functions"]),
        ("A justification that a number $c$ from MVT is valid must include",
         "that c lies in (a,b)",
         "Solving $f'(c)=$ secant slope is not enough until you check the interval.",
         ["that c=a", "that f(c)=0", "that f'' exists"]),
        ("To maximize the area of a rectangle with perimeter $20$, the constraint is",
         "2x+2y=20",
         "Solve for $y=10-x$, then $A=x(10-x)$.",
         ["xy=20", "x+y=20", "x=y=20"]),
        ("For $A(x)=x(10-x)$ on $(0,10)$, $A'(x)=10-2x=0$ at $x=$",
         5, "A square. $A''=-2<0$ confirms a max.", [10, 0, 2]),
        ("An open-top box from a 12-by-12 square with squares of side $x$ cut out has $V=$",
         "x(12-2x)^2",
         "Height $x$, base $12-2x$ by $12-2x$.", ["x^2(12-2x)", "12x^2", "(12-2x)^3"]),
        ("The domain of that $x$ for a real box is", "(0,6)",
         "Need $12-2x>0$ and $x>0$.", ["all reals", "[0,12]", "x>6"]),
        ("Optimization on a closed domain uses",
         "the EVT candidate list after reducing to one variable",
         "Constraint first, calculus second, endpoints last.",
         ["IVT only", "L'Hôpital", "a slope field"]),
        ("A complete curve sketch uses domain, intercepts, asymptotes, and sign charts of",
         "f' and f''",
         "First derivative: inc/dec and extrema. Second: concavity and inflections.",
         ["only f", "only f''' ", "only a table of random x"]),
        ("A vertical asymptote of $f$ should appear on the sketch as",
         "a dashed vertical line the graph approaches",
         "Match left/right infinity from a sign test.",
         ["a hole", "a filled point", "a tangent"]),
        ("If $f'\\,>0$ and $f''<0$ on an interval, the graph is",
         "increasing and concave down",
         "Rising but bending clockwise (slopes getting smaller).",
         ["decreasing and concave up", "a line", "decreasing and concave down"]),
        ("Inflection points are marked where",
         "concavity changes and f is defined",
         "The point must be on the graph of $f$.",
         ["f'=0 only", "f is undefined", "f'' is undefined always implies inflection"]),
        ("End behavior $\\lim_{x\\to\\infty}f(x)=0$ on a sketch is a",
         "horizontal asymptote to the right",
         "Draw $y=0$ dashed and let the curve flatten toward it.",
         ["vertical asymptote", "a corner", "an intercept only"]),
        ("L'Hôpital’s rule applies to the indeterminate forms",
         "0/0 and ∞/∞",
         "Not to $0/1$ or $1/0$. Rewrite other forms ($\\infty-\\infty$, $0\\cdot\\infty$) into a quotient first.",
         ["0/1", "1/1", "∞/0 as a first try without rewrite"]),
        ("$\\lim_{x\\to 0}\\dfrac{\\sin x}{x}$ by L'Hôpital (or geometry) equals", 1,
         "$0/0$, then $\\cos x/1\\to 1$.", [0, "+∞", "DNE"]),
        ("$\\lim_{x\\to\\infty}\\dfrac{3x^2+1}{x^2-4}$ by L'Hôpital twice (or degrees) equals", 3,
         "$\\infty/\\infty$, derivatives $6x/2x=3$, or leading coefficients $3/1=3$.", [0, 3 / 4, "+∞"]),
        ("$\\lim_{x\\to 0}\\dfrac{1-\\cos x}{x}$ equals", 0,
         "$0/0$, then $\\sin x/1\\to 0$.", [1, "+∞", "1/2"]),
        ("You must rewrite $\\lim_{x\\to 0}\\left(\\dfrac{1}{x}-\\dfrac{1}{\\sin x}\\right)$ before L'Hôpital because",
         "the form is ∞−∞, not a quotient",
         "Common denominator produces $0/0$: $(\\sin x-x)/(x\\sin x)$.",
         ["it is already 0/0", "L'Hôpital never needs a quotient", "the limit is obviously 0"]),
        ("Implicit: $x^2+y^2=25$, differentiate: $2x+2y y'=0$, so $y'=$",
         "-x/y",
         "Provided $y\\neq 0$. That is the slope on the circle.",
         ["-y/x", "x/y", "2x+2y"]),
        ("At the point $(3,4)$ on $x^2+y^2=25$, the tangent slope is",
         "-3/4", "$y'=-x/y=-3/4$.", [3 / 4, -4 / 3, 0]),
        ("Second implicit derivative: from $y'=-x/y$, $y''=$",
         "-(y-x y')/y^2",
         "Quotient rule, then substitute $y'$ if asked to simplify.",
         ["-1/y", "0", "x/y^2"]),
        ("If a relation does not define $y$ as a single function, $dy/dx$ from implicit differentiation still gives",
         "the slope of the tangent to the curve at a point on the relation",
         "You must plug a specific $(x,y)$ on the graph.",
         ["every possible y at that x automatically", "a slope field of an unrelated DE", "an integral"]),
        ("Logarithmic implicit differentiation of $y=(x+1)^x$ starts by writing",
         "ln y = x ln(x+1)",
         "Then differentiate both sides in $x$ and solve for $y'$.",
         ["y'=x(x+1)^{x-1}", "ln y = ln x", "y=e^x"]),
        ("$f''(x)=12x-6$. Inflection candidate $x=1/2$. Concavity changes because $f''$ changes",
         "from negative to positive",
         "Test $x=0$: $f''=-6<0$; $x=1$: $f''=6>0$. Inflection at $x=1/2$.",
         ["never", "from + to − only", "f'' is always zero"]),
        ("MVT on $f(x)=\\sqrt{x}$ on $[0,4]$ applies because $f$ is continuous on $[0,4]$ and $f'(x)=1/(2\\sqrt{x})$ exists on $(0,4)$. The guaranteed $c$ satisfies $1/(2\\sqrt{c})=(2-0)/4$, so $c=$",
         1, "$1/(2\\sqrt{c})=1/2\\Rightarrow \\sqrt{c}=1\\Rightarrow c=1\\in(0,4)$. A vertical tangent at the endpoint $0$ does not break differentiability on the open interval.",
         [0, 4, 2]),
        ("Rolle’s theorem on $g(x)=x^3-x$ on $[-1,1]$: $g(-1)=g(1)=0$, and $g'(x)=3x^2-1=0$ at $x=$",
         "±1/√3",
         "Both roots $\\pm 1/\\sqrt{3}$ lie in $(-1,1)$, so Rolle’s $c$ can be either. (MVT/Rolle never claimed uniqueness.)",
         ["0 only", "±1", "±√3"]),
        ("Maximize $xy$ subject to $x+2y=10$, $x>0,y>0$. Then $x=$",
         5, "$y=(10-x)/2$, $P=x(10-x)/2$, $P'=(10-2x)/2=0\\Rightarrow x=5$, $y=2.5$.", [10, 2, 0]),
        ("A cylinder inscribed in a sphere of radius $4$: the volume as a function of height $h$ involves",
         "r^2=16-(h/2)^2 from a right triangle in the cross-section",
         "Geometry first, then $V=\\pi r^2 h$, then $dV/dh=0$.",
         ["r=4 always", "V=4πh only", "no constraint"]),
        ("Sketch $f(x)=x^3-3x$: local max at $x=$",
         -1, "$f'=3x^2-3=3(x-1)(x+1)$, $+/\\to-$ at $-1$.", [1, 0, 3]),
        ("For that cubic, inflection at $x=$", 0, "$f''=6x$, sign change at $0$.", [1, -1, 3]),
        ("$\\lim_{x\\to 0}\\dfrac{e^x-1-x}{x^2}$ by L'Hôpital (twice) equals", "1/2",
         "Still $0/0$ after one derivative $(e^x-1)/(2x)$; again $e^x/2\\to 1/2$.", [1, 0, "+∞"]),
        ("Implicit $x^3+y^3=9$ at $(1,2)$: $3x^2+3y^2 y'=0$, so $y'=$",
         "-1/4", "$-x^2/y^2=-1/4$.", ["-1", "-4", "1/4"]),
        ("L'Hôpital does not apply to $\\lim_{x\\to 0}\\dfrac{\\cos x}{x}$ because",
         "the form is 1/0, not 0/0 or ∞/∞",
         "The limit DNE (sides $\\pm\\infty$). Forcing L'Hôpital would illegally produce $-\\sin x/1\\to 0$.",
         ["cos x is not differentiable", "the limit is 1", "you must use L'Hôpital anyway"]),
        ("On a curve sketch, a hole from a canceled factor is drawn as",
         "an open circle at the simplified function’s point",
         "Not as a vertical asymptote.",
         ["a VA", "a filled jump", "nothing; holes are ignored"]),
        ("Rolle on $f(x)=x^2-x$ on $[0,1]$: $f(0)=f(1)=0$, so some $c$ has $f'(c)=0$. That $c$ is",
         "1/2", "$f'=2x-1=0$ at $x=1/2\\in(0,1)$.", [0, 1, 2]),
        ("Second derivative test fails at $x=0$ for $f(x)=x^4$ because $f''(0)=0$, even though",
         "the first derivative test shows a local min",
         "$f'=4x^3$ changes $-$ to $+$.",
         ["f has a local max", "f is discontinuous", "f''>0 at 0"]),
        ("A related geometry optimization: fence three sides of a rectangle against a river (no fence on the river). If $120$ m of fence, $A=x(120-2x)$ is max at $x=$",
         30, "$A'=120-4x=0\\Rightarrow x=30$ (the side perpendicular to the river).", [60, 120, 40]),
        ("$\\lim_{x\\to\\infty}\\dfrac{\\ln x}{x}$ equals", 0,
         "$\\infty/\\infty$, L'Hôpital: $(1/x)/1\\to 0$. Logs grow slower than linear.", [1, "+∞", "e"]),
        ("AP Stretch: For $f(x)=\\sqrt{x}$ on $[4,9]$, MVT guarantees some $c\\in(4,9)$ with $f'(c)=(3-2)/(9-4)=1/5$. Solving $1/(2\\sqrt{c})=1/5$ and checking the open interval yields $c=$",
         "25/4",
         "$2\\sqrt{c}=5$, $\\sqrt{c}=5/2$, $c=25/4$. And $4<6.25<9$, so $c$ lies in $(4,9)$ as required.",
         [5, "9/4", 5 / 2]),
        ("AP Stretch: After rewriting $\\infty-\\infty$, $\\lim_{x\\to 0}\\left(\\dfrac{1}{x}-\\dfrac{1}{\\sin x}\\right)=\\lim_{x\\to 0}\\dfrac{\\sin x-x}{x\\sin x}$. Applying L'Hôpital (still $0/0$) eventually yields",
         0,
         "First derivatives: $(\\cos x-1)/(\\sin x+x\\cos x)$ still $0/0$; a second pass approaches $0$. On AB use repeated L'Hôpital or standard equivalents, not power-series expansions.",
         ["1", "+∞", "1/6"]),
        ("AP Stretch: Washer preview from implicit related rates: a circle $x^2+y^2=r^2$ with $r$ growing. At $(3,4)$ when $r=5$ and $dr/dt=2$, differentiating $x^2+y^2=r^2$ in $t$ with $x$ fixed ($dx/dt=0$) gives $dy/dt=$",
         "5/2",
         "$2y y'=2r r'\\Rightarrow y'= (r/y)r'=(5/4)\\cdot 2=2.5$.",
         ["2", "0", "8"]),
        ("AP Stretch: Optimize $A=2xy$ subject to $x^2/4+y^2=1$ (ellipse). Implicit $x/2+2y y'=0$ is the constraint’s slope; a Lagrange-free AB method is to solve the constraint for $y(x)$ on $[-2,2]$ and use EVT. At a max of $A$, $y=$",
         "√2/2",
         "Let $y=\\sqrt{1-x^2/4}$, $A=2x\\sqrt{1-x^2/4}$. Set $A'=0$ or substitute $u=x^2$. The maximum occurs when $x^2=2$, $y=\\sqrt{1/2}=\\sqrt{2}/2$.",
         ["1", "0", "2"]),
        ("AP Stretch: Let $f(x)=x e^{x}$. Differentiate twice with the product rule. Then $f''(0)$ equals, and near $x=0$ the graph of $f$ is",
         "2 and concave up",
         "$f'=(1+x)e^{x}$, $f''=(2+x)e^{x}$, so $f''(0)=2>0$. (Also $f'(0)=1\\neq 0$, so this is concavity, not an extremum test.)",
         ["0 and inconclusive", "1 and concave down", "2 and concave down"]),
        ("AP Stretch: Justify that $f(x)=x^3+x-1$ has exactly one real root using Rolle: if two roots $a<b$, then some $c$ has $f'(c)=0$, but $f'(x)=3x^2+1>0$ always, a contradiction. Combined with IVT on $[0,1]$ this shows",
         "exactly one real root (and it lies in (0,1))",
         "IVT gives existence; Rolle-plus-strictly-increasing $f'$ gives uniqueness.",
         ["no real roots", "three real roots", "a root only at 0"]),
        ("AP Stretch: Curve sketch of $f(x)=\\dfrac{x^2-1}{x^2-4}$: HA $y=1$, VAs $x=\\pm 2$. After simplifying, $f'(x)=\\dfrac{6x}{(x^2-4)^2}$. Then $f$ has a local extremum at",
         "x=0 (local minimum)",
         "The squared denominator is positive where defined, so $f'$ has the sign of $x$. First derivative test: $-$ to $+$ at $x=0$, and $f(0)=1/4$.",
         ["x=±2", "no critical points", "x=±1"]),
        ("AP Stretch: Implicit $x\\sin y+y=\\pi$ at $\\left(\\dfrac{\\pi}{2},\\dfrac{\\pi}{2}\\right)$. Differentiate with respect to $x$ and solve for $y'$. Then $y'$ at the given point equals",
         -1,
         "$\\sin y+x\\cos y\\, y'+y'=0$, so $y'=-\\sin y/(x\\cos y+1)$. At the point, $\\cos(\\pi/2)=0$ and $\\sin(\\pi/2)=1$, hence $y'=-1/(0+1)=-1$.",
         [0, 1, "π"]),
        ("AP Stretch: L'Hôpital after rewrite: $\\lim_{x\\to\\infty}x\\ln\\!\\left(1+\\dfrac{3}{x}\\right)$ is $0\\cdot\\infty$. Writing $\\dfrac{\\ln(1+3/x)}{1/x}$ makes $\\dfrac{0}{0}$, and the limit equals",
         3,
         "L'Hôpital: numerator $(1/(1+3/x))\\cdot(-3/x^2)$, denominator $-1/x^2$, ratio $\\to 3$.",
         [0, 1, "+∞"]),
        ("AP Stretch: MVT numbers: $f(x)=x^3$ on $[1,4]$. Hypotheses hold. Some $c\\in(1,4)$ has $f'(c)=(64-1)/3=21$. Solving $3c^2=21$ and checking the open interval gives $c=$",
         "√7",
         "$c=\\sqrt{7}$ (positive). Interval check: $1<\\sqrt{7}<4$ because $1<2.65<4$. Both the algebra and the interval sentence are required.",
         [7, 21, "√21"]),
    ])


def build_unit4():
    title = "AP Calculus AB Unit 4: Applications of Derivatives II"
    description = (
        "Concavity and inflection, MVT and Rolle with numerical justifications, optimization, "
        "full curve sketching, L'Hôpital after checking form, and implicit differentiation."
    )
    concepts = [
        "Concavity and second derivative",
        "MVT and Rolle",
        "Optimization",
        "Curve sketching",
        "L'Hôpital (0/0, ∞/∞)",
        "Implicit differentiation",
    ]

    c1 = concept_block(
        "1. Concavity and the second derivative",
        [
            "$f$ is concave up on an interval where $f''>0$ (slopes of $f$ are increasing; graph holds water). Concave down where $f''<0$.",
            "An inflection point is a point on the graph of $f$ where concavity changes. $f''(c)=0$ or $f''(c)$ DNE are candidates, not automatic inflections.",
            "The second derivative test: if $f'(c)=0$ and $f''(c)>0$, local min; if $f''(c)<0$, local max; if $f''(c)=0$, inconclusive.",
            "A sign chart of $f''$ is the concavity analogue of the $f'$ chart. Test values, then mark inflection $x$-values where the sign of $f''$ actually changes and $f$ is defined.",
            "Concavity justifies linearization error: concave up $\\Rightarrow$ tangent underestimates. That sentence links this lesson to Unit 3.",
            "On FRQs, “$f''$ changes from negative to positive at $x=c$, so $f$ has an inflection point at $x=c$” is the required language — parallel to the first derivative test.",
        ],
        "Curve sketching is incomplete without concavity. Optimization sometimes uses $f''<0$ as a one-line max confirmation after you already have $f'=0$.",
        "Compute $f''$, factor it, sign-chart it, and only then name inflections. Do not skip the sign change.",
        lesson_figure(
            _concavity_svg(),
            "A curve that is concave down, then concave up, with the inflection marked",
            "The tangent at the inflection cuts through the graph: slopes go from decreasing to increasing.",
        )
        + solved(
            1,
            "If $f''(x)=2$, what can you say about concavity?",
            ["$f''>0$ everywhere.", "$f$ is concave up on $\\mathbb{R}$ (a parabola opening up if $f'$ is linear)."],
            "concave up everywhere", "", "Easy",
        )
        + solved(
            2,
            "For $f(x)=x^3-3x$, find inflection points.",
            ["$f'=3x^2-3$, $f''=6x$.", "$f''$ changes $-$ to $+$ at $x=0$.", "$f(0)=0$, so $(0,0)$ is an inflection point."],
            "$(0,0)$", "", "Medium",
        )
        + solved(
            3,
            "Apply the second derivative test to $f(x)=x^4$ at $0$, then classify correctly.",
            [
                "$f'(0)=0$, $f''(x)=12x^2$, $f''(0)=0$: inconclusive.",
                "$f'=4x^3$ changes from $-$ to $+$ at $0$.",
                "Local minimum at $0$ by the first derivative test.",
            ],
            "inconclusive by $f''$; local min by $f'$ signs", "", "Honors",
        ),
        ("Calling every zero of $f''$ an inflection",
         "$x^4$ at $0$ has $f''=0$ and stays concave up. Demand a concavity sign change and a point that is actually on the graph."),
        ("Keep two number lines: f' and f''",
         "Mixing them produces “concave up so increasing,” which is false. $e^{-x}$ is decreasing and concave up for $x>0$ after the first bit — check $f''=e^{-x}>0$ while $f'<0$."),
        ["I sign-chart f''.", "I require a concavity change for inflection.", "I know when the second derivative test is inconclusive."],
        1,
    )

    c2 = concept_block(
        "2. Mean Value Theorem and Rolle",
        [
            "MVT: If $f$ is continuous on $[a,b]$ and differentiable on $(a,b)$, then there exists at least one $c\\in(a,b)$ such that $f'(c)=\\dfrac{f(b)-f(a)}{b-a}$.",
            "Geometrically, some tangent is parallel to the secant through the endpoints. Rolle’s theorem is the case $f(a)=f(b)$, so some $c$ has $f'(c)=0$.",
            "AP justifications must name both hypotheses, compute the secant slope, solve $f'(c)=$ that slope, and verify $c$ lies in $(a,b)$.",
            "Illegal applications: a corner on $(a,b)$, a jump on $[a,b]$, or an open interval where EVT/MVT were never claimed. $|x|$ on $[-1,1]$ is the standard counterexample for MVT.",
            "MVT is the engine behind “$f'=0$ on an interval $\\Rightarrow f$ constant” and “$f'>0\\Rightarrow f$ increasing” when those theorems are proved carefully.",
            "A numerical MVT item often uses a table of $f$ at two times and asks whether some $c$ must have $f'(c)$ equal to an average rate. Cite MVT, do not invent a derivative from one point.",
        ],
        "Readers award a dedicated “hypotheses + $c$ in $(a,b)$” point. Skipping either piece loses it even if your algebra for $c$ is perfect.",
        "Write the hypotheses first, then the displayed equation $f'(c)=(f(b)-f(a))/(b-a)$, then solve, then check the interval.",
        lesson_figure(
            _mvt_svg(),
            "Secant through $A$ and $B$ with a parallel tangent at $c$",
            "MVT promises at least one such $c$ in the open interval. There may be more than one.",
        )
        + solved(
            1,
            "State Rolle’s conclusion for $f(x)=x^2-4$ on $[-2,2]$.",
            ["$f$ is a polynomial, so hypotheses hold.", "$f(-2)=f(2)=0$.", "Some $c\\in(-2,2)$ has $f'(c)=0$. Indeed $c=0$."],
            "$f'(c)=0$ for some $c\\in(-2,2)$ (e.g. $0$)", "", "Easy",
        )
        + solved(
            2,
            "Apply MVT to $f(x)=x^2$ on $[1,4]$ and find $c$.",
            [
                "Hypotheses hold (polynomial).",
                "Secant slope $(16-1)/(4-1)=5$.",
                "$f'(x)=2x=5\\Rightarrow c=2.5\\in(1,4)$.",
            ],
            "$c=5/2$", "Name $5/2$ and the interval.", "Medium",
        )
        + solved(
            3,
            "A function is continuous on $[0,2]$ and differentiable on $(0,2)$ with $f(0)=1$, $f(2)=7$. Can $f'(x)\\le 2$ for all $x$ in $(0,2)$?",
            [
                "MVT requires some $c$ with $f'(c)=(7-1)/2=3$.",
                "If every derivative were $\\le 2$, this $c$ could not exist.",
                "Therefore $f'$ cannot stay $\\le 2$ on the whole open interval.",
            ],
            "no; MVT forces some $f'(c)=3$", "This is the AP “average rate vs instantaneous” trap in justification form.", "Honors",
        ),
        ("Solving for $c$ but never checking $c\\in(a,b)$",
         "A quadratic formula extra root outside $[a,b]$ is not a MVT $c$. Throw it away and say so."),
        ("Hypotheses, secant slope, solve, interval check",
         "Four lines. If any is missing, assume the point is at risk on an FRQ."),
        ["I can state MVT and Rolle with hypotheses.", "I can compute c and verify the interval.", "I can use MVT to rule out an impossible bound on f'."],
        6,
    )

    c3 = concept_block(
        "3. Optimization",
        [
            "Optimization is EVT on a domain that comes from geometry: reduce to one variable with a constraint, identify a realistic closed interval if possible, then run the candidate list.",
            "If the physical domain is open (a length cannot be $0$ or the full perimeter), you may still argue that $V\\to 0$ at the endpoints of the closure, so an interior critical point with $V''<0$ is the max.",
            "Primary equation (what is maximized) plus secondary equation (constraint). Solve the constraint for the easy variable, substitute, differentiate.",
            "Units and a sentence “the maximum area is … when …” are part of the answer. A naked $x=5$ is incomplete.",
            "Common models: rectangle with fixed perimeter, open box from a square sheet, cylinder in a sphere, closest point on a curve (minimize distance squared to avoid the square root).",
            "Check that your critical point lies in the domain. A critical number $x=-3$ for a length is usually extraneous.",
        ],
        "This is a guaranteed AB FRQ topic. The calculus is usually one derivative; the points are lost in the constraint or the domain.",
        "Draw, label, write two equations, reduce, $d/dx$, test, answer with units. Same skeleton as related rates, but you set a derivative to zero instead of substituting a given rate.",
        lesson_figure(
            _box_opt_svg(),
            "Open-top box from a square sheet: cut-out $x$ and remaining base $s-2x$",
            "Volume $V=x(s-2x)^2$ is a one-variable calculus problem once the picture is labeled.",
        )
        + solved(
            1,
            "A rectangle has perimeter $24$. Maximize area.",
            ["$2x+2y=24\\Rightarrow y=12-x$, $A=x(12-x)$.", "$A'=12-2x=0\\Rightarrow x=6$, $y=6$.", "Maximum area $36$ (a square)."],
            "$36$ square units, when it is a $6\\times 6$ square", "", "Easy",
        )
        + solved(
            2,
            "From a $12$ by $12$ square, cut $x$ by $x$ corners and fold an open box. Maximize $V$.",
            [
                "$V=x(12-2x)^2$, domain $(0,6)$.",
                "$V'=(12-2x)^2+x\\cdot 2(12-2x)(-2)=(12-2x)[12-2x-4x]=(12-2x)(12-6x)$.",
                "Zeros $x=6$ (endpoint, $V=0$) and $x=2$.",
                "$V(2)=2\\cdot 8^2=128$.",
            ],
            "$V=128$ when $x=2$", "", "Medium",
        )
        + solved(
            3,
            "Find the point on $y=x^2$ closest to $(0,1)$ by minimizing $D^2=x^2+(x^2-1)^2$.",
            [
                "Let $S(x)=x^2+(x^2-1)^2$. $S'=2x+2(x^2-1)(2x)=2x[1+2(x^2-1)]=2x(2x^2-1)$.",
                "Critical: $x=0$ or $x=\\pm 1/\\sqrt{2}$.",
                "$S(0)=1$, $S(\\pm 1/\\sqrt{2})=1/2+(1/2-1)^2=0.5+0.25=0.75<1$.",
                "Closest points $(\\pm 1/\\sqrt{2},\\,1/2)$.",
            ],
            "$\\left(\\pm \\dfrac{\\sqrt{2}}{2},\\dfrac12\\right)$", "Minimizing $S=D^2$ avoids a messy chain on the square root.", "Honors",
        ),
        ("Maximizing a product without the constraint",
         "If $x$ and $y$ are free, $xy$ has no max. The constraint is the problem. Write it first."),
        ("Close the physical domain and evaluate the collapsed endpoints",
         "Even when $x=0$ is not a real fence, $A(0)=0$ tells you the interior critical point is winning. That comparison is the EVT spirit."),
        ["I reduce to one variable.", "I respect the geometric domain.", "I answer with a value, a configuration, and units."],
        11,
    )

    sketch_svg = xy_graph(
        curves=[
            ("#4f46e5", sample_curve(lambda x: (x * x - 1) / (x * x - 4) if abs(abs(x) - 2) > 0.12 else 1e9, -4.5, 4.5, skip=(-2, 2))),
        ],
        dashes=[("v", 2, "x=2"), ("v", -2, "x=-2"), ("h", 1, "y=1")],
        xlim=(-4.6, 4.6), ylim=(-4, 4), w=320, h=280,
    )

    c4 = concept_block(
        "4. Curve sketching",
        [
            "A complete AP sketch is not art class: it is a report of domain, intercepts, asymptotes, $f'$ signs (inc/dec, local extrema), and $f''$ signs (concavity, inflections), then a graph that respects every bullet.",
            "Start with factoring. Vertical asymptotes versus holes, $x$-intercepts from the numerator, $y$-intercept from $f(0)$, horizontal or oblique asymptotes from end behavior.",
            "Then calculus: $f'$ for turning, $f''$ for bending. Mark those $x$-values on the axis before you draw.",
            "Match one-sided infinite limits at each VA with a sign test. A sketch that approaches a VA from the wrong side is a content error, not a drawing error.",
            "If $f'$ and $f''$ are both positive, the curve is increasing and concave up (an accelerating rise). All four sign combinations are four different local shapes.",
            "Label the special points. An AP “sketch” prompt still wants the features identifiable, not a perfect grid.",
        ],
        "This lesson packages Units 1–4. A student who can sketch $f(x)=(x^2-1)/(x^2-4)$ with VAs, HA, and a local min at $0$ is ready for mixed review.",
        "Make a feature list on paper first: domain, intercepts, asymptotes, crits, inflections. Draw only after the list is full.",
        lesson_figure(
            sketch_svg,
            "$y=(x^2-1)/(x^2-4)$: vertical asymptotes $x=\\pm 2$, horizontal asymptote $y=1$",
            "The middle branch has a local minimum at $x=0$. End behavior both approaches $y=1$.",
        )
        + solved(
            1,
            "For $y=1/x$, name the intercepts and asymptotes.",
            ["No intercepts (never $0$, undefined at $0$).", "VA $x=0$, HA $y=0$."],
            "no intercepts; VA $x=0$; HA $y=0$", "", "Easy",
        )
        + solved(
            2,
            "Sketch features of $f(x)=x^3-3x$: extrema and inflection.",
            [
                "$f'=3(x-1)(x+1)$: local max at $x=-1$, $f(-1)=2$; local min at $x=1$, $f(1)=-2$.",
                "$f''=6x$: inflection at $0$.",
                "Odd function: rotational symmetry about the origin.",
            ],
            "max $(-1,2)$, min $(1,-2)$, inflection $(0,0)$", "", "Medium",
        )
        + solved(
            3,
            "For $f(x)=\\dfrac{x^2-1}{x^2-4}$, justify the local minimum at $x=0$.",
            [
                "HA $y=1$, VAs $x=\\pm 2$, $f(0)=1/4$.",
                "Quotient rule simplifies to $f'(x)=\\dfrac{6x}{(x^2-4)^2}$.",
                "Denominator always positive where defined; $f'$ has the sign of $x$.",
                "$-$ to $+$ at $0$: local min $f(0)=1/4$ by the first derivative test.",
            ],
            "local min $(0,1/4)$", "The denominator squared never changes sign — only $6x$ does.", "Honors",
        ),
        ("Drawing a VA through a hole",
         "Canceled factors are open circles on the simplified graph. They are not walls. Factor before you sketch."),
        ("Feature list before pencil",
         "If your sketch disagrees with your $f'$ chart, the chart wins. Erase the curve, not the signs."),
        ["I list domain, intercepts, asymptotes first.", "I combine f' and f'' charts.", "I match one-sided infinity at VAs."],
        16,
    )

    c5 = concept_block(
        "5. L'Hôpital’s rule",
        [
            "If $\\lim f/g$ is $0/0$ or $\\infty/\\infty$, and $\\lim f'/g'$ exists (or is $\\pm\\infty$), then $\\lim f/g=\\lim f'/g'$. You must name the form before differentiating.",
            "Other indeterminate forms — $\\infty-\\infty$, $0\\cdot\\infty$, $1^\\infty$, $0^0$, $\\infty^0$ — must be rewritten into a quotient first. AP AB mainly tests $0/0$, $\\infty/\\infty$, and one rewrite such as $\\infty-\\infty$ or $x\\ln(1+a/x)$.",
            "L'Hôpital is not a substitute for algebra when a factor cancels cleanly, but it is legal on $0/0$ either way. Differentiating a quotient that is actually $1/0$ is illegal and produces garbage.",
            "You may need several applications. Stop when the form is no longer indeterminate.",
            "Logs versus polynomials versus exponentials: $\\ln x/x\\to 0$, $x/e^x\\to 0$ as $x\\to\\infty$. L'Hôpital proves those comparison limits.",
            "After rewriting $\\dfrac{1}{x}-\\dfrac{1}{\\sin x}$, you get $0/0$ and only then may you differentiate numerator and denominator.",
        ],
        "AB does not include series, so L'Hôpital plus algebra is how you finish hard limit items that survive into mixed review.",
        "Box the form ($0/0$ or $\\infty/\\infty$). If the box is empty because the form is $3/0$ or $5/5$, do not use the rule.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#4f46e5", sample_curve(lambda x: math.sin(x) / x if abs(x) > 0.12 else 1e9, -8, 8, skip=(0,))),
                ],
                points=[(0, 1, "limit 1")],
                xlim=(-8, 8), ylim=(-0.5, 1.4), w=320, h=240,
            ),
            "$y=(\\sin x)/x$ with the removable hole at $0$ filled by the limit $1$",
            "The $0/0$ form is a hole. L'Hôpital (or the standard limit) reports the height of that hole.",
        )
        + solved(
            1,
            "Evaluate $\\lim_{x\\to 0}\\dfrac{1-\\cos x}{x}$.",
            ["Form $0/0$.", "$\\dfrac{\\sin x}{1}\\to 0$."],
            "$0$", "", "Easy",
        )
        + solved(
            2,
            "Evaluate $\\lim_{x\\to\\infty}\\dfrac{\\ln x}{x}$.",
            ["Form $\\infty/\\infty$.", "$\\dfrac{1/x}{1}\\to 0$."],
            "$0$", "Logs grow slower than any positive power of $x$.", "Medium",
        )
        + solved(
            3,
            "Evaluate $\\lim_{x\\to 0}\\left(\\dfrac{1}{x}-\\dfrac{1}{\\sin x}\\right)$ after rewriting.",
            [
                "$\\infty-\\infty$. Common denominator: $\\dfrac{\\sin x-x}{x\\sin x}$, now $0/0$.",
                "Differentiate: $\\dfrac{\\cos x-1}{\\sin x+x\\cos x}$, still $0/0$.",
                "Again: $\\dfrac{-\\sin x}{\\cos x+\\cos x-x\\sin x}=\\dfrac{-\\sin x}{2\\cos x-x\\sin x}\\to 0/2=0$.",
            ],
            "$0$", "Rewrite first; then L'Hôpital is legal.", "Honors",
        ),
        ("Differentiating a non-indeterminate quotient",
         "$\\cos x/x$ near $0$ is $1/0$, not $0/0$. L'Hôpital would wrongly suggest $0$. Check the form every time."),
        ("Write “0/0, so L'Hôpital applies” as its own sentence",
         "That citation is part of the AP communication standard, just like citing IVT or MVT."),
        ["I verify 0/0 or ∞/∞ first.", "I rewrite ∞−∞ into a quotient.", "I can apply the rule more than once."],
        21,
    )

    circle = xy_graph(
        curves=[("#4f46e5", sample_curve(lambda t: math.sqrt(max(25 - t * t, 0)), -5, 5)),
                ("#4f46e5", sample_curve(lambda t: -math.sqrt(max(25 - t * t, 0)), -5, 5))],
        points=[(3, 4, "(3,4)")],
        dashes=[],
        xlim=(-6, 6), ylim=(-6, 6), w=280, h=280,
    )
    # tangent y-4 = (-3/4)(x-3) through (3,4)
    circle = circle.replace(
        "</svg>",
        f'<line x1="40" y1="190" x2="250" y2="70" stroke="#dc2626" stroke-width="2"/>'
        f'<text x="200" y="70" font-size="11" fill="#b91c1c">tangent</text></svg>',
    )

    c6 = concept_block(
        "6. Implicit differentiation",
        [
            "When a relation $F(x,y)=0$ defines $y$ as a differentiable function of $x$ near a point, differentiate both sides with respect to $x$, treating $y$ as $y(x)$. Every $y$ produces a $y'$ by the chain rule.",
            "Solve the resulting equation for $y'$. The formula will typically involve both $x$ and $y$; you must plug in a point that lies on the original curve.",
            "Circles, ellipses, and products $x\\sin y$ are standard. $x^2+y^2=r^2$ yields $y'=-x/y$, the slope of the circle, undefined at the left and right points where the tangent is vertical ($y=0$).",
            "Second derivatives: differentiate $y'$ again, then substitute the already-known $y'$ to simplify. That is how you test concavity on an implicit curve.",
            "Related rates in Unit 3 was implicit differentiation with $t$ as the independent variable. Here $x$ is independent and $y$ is dependent.",
            "Logarithmic differentiation of $y=f(x)^{g(x)}$ is implicit: $\\ln y=g\\ln f$, then $y'/y=\\ldots$. Still AB, provided you stay away from series.",
        ],
        "Many AB FRQs hide a tangent-line request on a relation that is not solved for $y$. Implicit differentiation is the only efficient path.",
        "Differentiate, collect every $y'$ term, factor $y'$, divide. Then substitute the point. Do not substitute the point before differentiating unless those coordinates are constants.",
        lesson_figure(
            circle,
            "Circle $x^2+y^2=25$ with tangent at $(3,4)$ of slope $-3/4$",
            "The tangent is perpendicular to the radius, which is a geometry check on the calculus: radius slope $4/3$, tangent slope $-3/4$.",
        )
        + solved(
            1,
            "Find $dy/dx$ if $x^2+y^2=25$.",
            ["$2x+2y y'=0$.", "$y'=-x/y$ ($y\\neq 0$)."],
            "$y'=-x/y$", "", "Easy",
        )
        + solved(
            2,
            "Find the tangent line to $x^2+y^2=25$ at $(3,4)$.",
            ["Slope $-3/4$.", "$y-4=-\\dfrac{3}{4}(x-3)$."],
            "$y-4=-\\dfrac{3}{4}(x-3)$", "Radius check: $(4/3)\\cdot(-3/4)=-1$.", "Medium",
        )
        + solved(
            3,
            "For $x^3+y^3=9$ at $(1,2)$, find $y''$.",
            [
                "$3x^2+3y^2 y'=0\\Rightarrow y'=-x^2/y^2$. At the point, $y'=-1/4$.",
                "Differentiate $y'=-x^2 y^{-2}$: $y''=\\dfrac{-2x y^2+ x^2\\cdot 2y y'}{y^4}$.",
                "Plug $x=1,y=2,y'=-1/4$: numerator $-2(4)+2(2)(-1/4)=-8-1=-9$, denominator $16$, so $y''=-9/16$.",
            ],
            "$y''=-9/16$", "Substitute $y'$ after the second differentiation.", "Honors",
        ),
        ("Treating $y$ as a constant when it depends on $x$",
         "The whole point of implicit is that $y$ is a function of $x$. Missing the $y'$ on a $y^2$ term is the classic error: $(y^2)'=2y y'$, not $2y$."),
        ("Plug the point only after the derivative formula exists",
         "If you set $y=4$ before differentiating $y^2$, you turn a changing quantity into a constant and lose $y'$."),
        ["I attach y' via the chain rule.", "I solve for dy/dx and substitute a point on the curve.", "I can differentiate again for y''."],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u4_questions()
