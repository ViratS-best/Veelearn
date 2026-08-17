"""AP Calculus BC units 1–4: parametric/vector/polar derivatives, advanced integration, arc length, series tests."""
from __future__ import annotations

import math

from curriculum_kit import lesson_figure, svg_parabola, svg_circle
from hs_curriculum import (
    concept_block,
    solved,
    practice_slots,
    unit_shell,
    mq,
    xy_graph,
    sample_curve,
    number_line,
    tangent_curve_svg,
    unit_circle_svg,
    labeled_right_triangle,
)
from .common import AUDIENCE, STRETCH_LABEL

_MK = [0]


def _mid():
    _MK[0] += 1
    return f"bcv{_MK[0]}"


def plot(
    curves=None,
    points=None,
    dashes=None,
    arrows=None,
    fills=None,
    xlim=(-6, 6),
    ylim=(-6, 6),
    w=320,
    h=300,
    xlab="x",
    ylab="y",
):
    """xy_graph plus optional filled regions and velocity arrows."""
    pad = 24
    x0, x1 = xlim
    y0, y1 = ylim

    def X(x):
        return pad + (x - x0) / (x1 - x0) * (w - 2 * pad)

    def Y(y):
        return h - pad - (y - y0) / (y1 - y0) * (h - 2 * pad)

    mid = _mid()
    yaxis_x = X(0) if x0 <= 0 <= x1 else pad
    xaxis_y = Y(0) if y0 <= 0 <= y1 else h - pad
    parts = [
        f'<line x1="{pad}" y1="{xaxis_y:.1f}" x2="{w - pad}" y2="{xaxis_y:.1f}" stroke="#0f172a" stroke-width="1.6"/>',
        f'<line x1="{yaxis_x:.1f}" y1="{pad}" x2="{yaxis_x:.1f}" y2="{h - pad}" stroke="#0f172a" stroke-width="1.6"/>',
        f'<text x="{w - pad}" y="{xaxis_y - 6:.1f}" font-size="11">{xlab}</text>',
        f'<text x="{yaxis_x + 6:.1f}" y="{pad + 4}" font-size="11">{ylab}</text>',
        f'<defs><marker id="{mid}" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        f'<path d="M0,0 L6,3 L0,6 Z" fill="#dc2626"/></marker></defs>',
    ]
    for kind, val, lab in (dashes or []):
        col = "#dc2626" if kind == "v" else "#2563eb"
        if kind == "v":
            parts.append(
                f'<line x1="{X(val):.1f}" y1="{pad}" x2="{X(val):.1f}" y2="{h - pad}" '
                f'stroke="{col}" stroke-width="1.5" stroke-dasharray="5 4"/>'
            )
            parts.append(f'<text x="{X(val) + 4:.1f}" y="{pad + 12}" font-size="11" fill="{col}">{lab}</text>')
        else:
            parts.append(
                f'<line x1="{pad}" y1="{Y(val):.1f}" x2="{w - pad}" y2="{Y(val):.1f}" '
                f'stroke="{col}" stroke-width="1.5" stroke-dasharray="5 4"/>'
            )
            parts.append(f'<text x="{pad + 4}" y="{Y(val) - 4:.1f}" font-size="11" fill="{col}">{lab}</text>')

    def clip_seg(pts):
        segs, cur = [], []
        for x, y in pts:
            if x0 - 0.25 <= x <= x1 + 0.25 and y0 - 0.25 <= y <= y1 + 0.25 and abs(y) < 1e8:
                cur.append((x, y))
            else:
                if len(cur) >= 2:
                    segs.append(cur)
                cur = []
        if len(cur) >= 2:
            segs.append(cur)
        return segs

    for pts, color in (fills or []):
        if len(pts) < 3:
            continue
        d = " ".join(("M" if i == 0 else "L") + f"{X(x):.1f},{Y(y):.1f}" for i, (x, y) in enumerate(pts))
        parts.append(f'<path d="{d} Z" fill="{color}" fill-opacity="0.38" stroke="none"/>')
    for color, pts in (curves or []):
        for seg in clip_seg(pts):
            d = " ".join(("M" if i == 0 else "L") + f"{X(x):.1f},{Y(y):.1f}" for i, (x, y) in enumerate(seg))
            parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.2"/>')
    for item in (points or []):
        x, y, lab = item[0], item[1], item[2] if len(item) > 2 else ""
        col = item[3] if len(item) > 3 else "#b91c1c"
        parts.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="4.2" fill="{col}"/>')
        if lab:
            parts.append(f'<text x="{X(x) + 7:.1f}" y="{Y(y) - 6:.1f}" font-size="11" fill="{col}">{lab}</text>')
    for arr in (arrows or []):
        x, y, dx, dy = arr[0], arr[1], arr[2], arr[3]
        lab = arr[4] if len(arr) > 4 else ""
        mag = math.hypot(dx, dy) or 1
        sx, sy = 1.35 * dx / mag, 1.35 * dy / mag
        parts.append(
            f'<line x1="{X(x):.1f}" y1="{Y(y):.1f}" x2="{X(x + sx):.1f}" y2="{Y(y + sy):.1f}" '
            f'stroke="#dc2626" stroke-width="2.3" marker-end="url(#{mid})"/>'
        )
        if lab:
            parts.append(f'<text x="{X(x + sx) + 6:.1f}" y="{Y(y + sy) - 4:.1f}" font-size="11" fill="#b91c1c">{lab}</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">{"".join(parts)}</svg>'


def polar_pts(rfn, a, b, n=180):
    out = []
    for i in range(n + 1):
        th = a + (b - a) * i / n
        r = rfn(th)
        out.append((r * math.cos(th), r * math.sin(th)))
    return out


def param_pts(xfn, yfn, t0, t1, n=90):
    return [(xfn(t0 + (t1 - t0) * i / n), yfn(t0 + (t1 - t0) * i / n)) for i in range(n + 1)]


def shade_under(fn, a, b, n=48):
    curve = sample_curve(fn, a, b, n)
    return [(a, 0)] + curve + [(b, 0)]


def euler_svg(slope, x0, y0, h, steps, xlim=(-0.5, 3.2), ylim=(-0.5, 3.2), w=320, hgt=300):
    """Slope-field ticks plus polygonal Euler path."""
    pad = 24
    xa, xb = xlim
    ya, yb = ylim

    def X(x):
        return pad + (x - xa) / (xb - xa) * (w - 2 * pad)

    def Y(y):
        return hgt - pad - (y - ya) / (yb - ya) * (hgt - 2 * pad)

    bits = [
        f'<line x1="{pad}" y1="{Y(0):.1f}" x2="{w - pad}" y2="{Y(0):.1f}" stroke="#0f172a" stroke-width="1.5"/>',
        f'<line x1="{X(0):.1f}" y1="{pad}" x2="{X(0):.1f}" y2="{hgt - pad}" stroke="#0f172a" stroke-width="1.5"/>',
        f'<text x="{w - pad}" y="{Y(0) - 6:.1f}" font-size="11">x</text>',
        f'<text x="{X(0) + 6:.1f}" y="{pad + 4}" font-size="11">y</text>',
    ]
    xs = [xa + (xb - xa) * i / 8 for i in range(9)]
    ys = [ya + (yb - ya) * j / 8 for j in range(9)]
    for gx in xs:
        for gy in ys:
            try:
                m = slope(gx, gy)
            except (ZeroDivisionError, ValueError, OverflowError):
                continue
            L = 0.16
            den = math.hypot(1, m) or 1
            dx, dy = L / den, L * m / den
            bits.append(
                f'<line x1="{X(gx - dx):.1f}" y1="{Y(gy - dy):.1f}" x2="{X(gx + dx):.1f}" y2="{Y(gy + dy):.1f}" '
                f'stroke="#64748b" stroke-width="1.2"/>'
            )
    path = [(x0, y0)]
    x, y = x0, y0
    for _ in range(steps):
        y = y + h * slope(x, y)
        x = x + h
        path.append((x, y))
    d = " ".join(("M" if i == 0 else "L") + f"{X(px):.1f},{Y(py):.1f}" for i, (px, py) in enumerate(path))
    bits.append(f'<path d="{d}" fill="none" stroke="#dc2626" stroke-width="2.4"/>')
    for px, py in path:
        bits.append(f'<circle cx="{X(px):.1f}" cy="{Y(py):.1f}" r="3.5" fill="#b91c1c"/>')
    return f'<svg viewBox="0 0 {w} {hgt}" width="100%" style="max-width:{w}px" role="img">{"".join(bits)}</svg>'


def logistic_pts(L=10.0, k=0.8, y0=1.0, tmax=8.0, n=80):
    A = (L - y0) / y0
    return sample_curve(lambda t: L / (1 + A * math.exp(-k * t)), 0, tmax, n)


def pack(rows):
    qs = [mq(text, ans, expl, i, distractors=dist) for i, (text, ans, expl, dist) in enumerate(rows, 1)]
    if len(qs) != 55:
        raise AssertionError(f"expected 55 questions, got {len(qs)}")
    return qs


def _fig(svg, title, cap):
    return lesson_figure(svg, title, cap)


# ===========================================================================
# UNIT 1
# ===========================================================================

def _u1_questions():
    return pack([
        ("If $f(x)=x^3-6x$, what is $f'(2)$?", 6,
         "Power rule: $f'(x)=3x^2-6$. Then $f'(2)=12-6=6$.", ["3", "12", "0"]),
        ("Differentiate $y=e^{2x}\\sin x$. What is $y'(0)$?", 1,
         "Product and chain: $y'=2e^{2x}\\sin x+e^{2x}\\cos x$. At $0$: $0+1=1$.", ["2", "0", "e"]),
        ("If $f(x)=\\ln(x^2+1)$, then $f'(1)$ equals?", 1,
         "Chain rule: $f'(x)=\\dfrac{2x}{x^2+1}$, so $f'(1)=\\dfrac{2}{2}=1$.", ["2", "1/2", "0"]),
        ("The line tangent to $y=\\sqrt{x}$ at $x=4$ has slope?", "1/4",
         "$y'=\\dfrac{1}{2\\sqrt{x}}$, so at $x=4$ the slope is $\\dfrac{1}{4}$.", ["1/2", "2", "1/8"]),
        ("Implicit: $x^2+y^2=25$. What is $\\dfrac{dy}{dx}$ at $(3,4)$?", "-3/4",
         "$2x+2y y'=0$, so $y'=-x/y=-3/4$.", ["-4/3", "3/4", "4/3"]),
        ("Parametric $x=t^2$, $y=t^3$ with $t\\neq0$. Then $\\dfrac{dy}{dx}$ equals?", "3t/2",
         "$\\dfrac{dy/dt}{dx/dt}=\\dfrac{3t^2}{2t}=\\dfrac{3t}{2}$.", ["3t", "2t/3", "3t^2"]),
        ("For $x=t^2$, $y=t^3$ ($t\\neq0$), $\\dfrac{d^2y}{dx^2}$ equals?", "3/(4t)",
         "Differentiate $3t/2$ in $t$ and divide by $dx/dt=2t$: $\\dfrac{3/2}{2t}=\\dfrac{3}{4t}$.", ["3/(2t)", "3t/4", "3/2"]),
        ("The curve $x=\\cos t$, $y=\\sin t$ has $\\dfrac{dy}{dx}$ equal to?", "-\\cot t",
         "$\\dfrac{\\cos t}{-\\sin t}=-\\cot t$ wherever $\\sin t\\neq0$.", ["\\tan t", "-\\tan t", "\\cot t"]),
        ("If $x=2t+1$ and $y=t^2$, the slope at $t=3$ is?", 3,
         "$dy/dx=(2t)/2=t$, so at $t=3$ the slope is $3$.", ["6", "2", "9"]),
        ("A parametric path has $dx/dt=0$ and $dy/dt\\neq0$ at $t=t_0$. The tangent is?", "vertical",
         "The $x$-velocity vanishes while $y$ still changes, so the tangent line is vertical.",
         ["horizontal", "undefined because the particle stops", "the line y=x"]),
        ("Position $\\mathbf{r}(t)=\\langle t, t^2\\rangle$. Speed at $t=1$ is?", "\\sqrt{5}",
         "Velocity $\\langle 1,2t\\rangle$; at $t=1$, $|\\mathbf{v}|=\\sqrt{1+4}=\\sqrt{5}$.", ["5", "3", "\\sqrt{2}"]),
        ("For $\\mathbf{r}(t)=\\langle 3\\cos t, 3\\sin t\\rangle$, speed is constantly?", 3,
         "$\\mathbf{v}=\\langle -3\\sin t, 3\\cos t\\rangle$ has magnitude $3$.", ["9", "1", "0"]),
        ("If $\\mathbf{v}(t)=\\langle 2, 4t\\rangle$ and $\\mathbf{r}(0)=\\langle 0,1\\rangle$, then $y(1)$ is?", 3,
         "Integrate: $y=2t^2+1$, so $y(1)=3$.", ["5", "2", "1"]),
        ("Acceleration of $\\mathbf{r}(t)=\\langle t^2, e^{t}\\rangle$ at $t=0$ is?", "\\langle 2, 1\\rangle",
         "$\\mathbf{a}=\\langle 2, e^{t}\\rangle$, so $\\mathbf{a}(0)=\\langle 2,1\\rangle$.",
         ["\\langle 2, 0\\rangle", "\\langle 0, 1\\rangle", "\\langle 1, 1\\rangle"]),
        ("A particle has velocity $\\langle 3,-4\\rangle$. Instantaneous speed is?", 5,
         "Speed is the magnitude $\\sqrt{9+16}=5$.", ["7", "-1", "12"]),
        ("Polar $r=2\\cos\\theta$. At $\\theta=\\pi/4$, $\\dfrac{dy}{dx}$ equals?", 0,
         "Use $\\dfrac{r'\\sin\\theta+r\\cos\\theta}{r'\\cos\\theta-r\\sin\\theta}$. The numerator is $0$, so the tangent is horizontal.",
         ["undefined", "1", "-1"]),
        ("Conversion $x=r\\cos\\theta$, $y=r\\sin\\theta$. Polar slope uses which formula?",
         "(dy/dθ)/(dx/dθ)",
         "Treat $x(\\theta)$ and $y(\\theta)$ as a parametric curve in the parameter $\\theta$.",
         ["r'/r", "tan θ", "r cos θ"]),
        ("For $r=\\theta$ at $\\theta=\\pi$, the polar slope $\\dfrac{dy}{dx}$ is?", "π",
         "$r'=1$, $\\sin\\pi=0$, $\\cos\\pi=-1$. Numerator $=r'\\sin\\theta+r\\cos\\theta=0+\\pi(-1)=-\\pi$. Denominator $=r'\\cos\\theta-r\\sin\\theta=-1-0=-1$. Slope $=\\pi$.",
         ["0", "undefined", "-1"]),
        ("The polar curve $r=1+\\cos\\theta$ at $\\theta=0$ has a tangent that is?", "vertical",
         "At the cardioid's rightmost point, $dx/d\\theta=0$ while $dy/d\\theta\\neq0$ fails — actually $r'= -\\sin\\theta=0$, $r=2$. Numerator $0+2\\cdot 1=2$, denominator $0-2\\cdot 0=0$, so the tangent is vertical.",
         ["horizontal", "slope 1", "slope 1/2"]),
        ("Polar $r=4\\sin\\theta$ is a circle. At $\\theta=\\pi/2$ the point is?", "(0, 4)",
         "$r=4$, $\\theta=\\pi/2$ gives $x=0$, $y=4$.", ["(4, 0)", "(0, 0)", "(4, 4)"]),
        ("Arc length of $x=\\cos t$, $y=\\sin t$ on $0\\leq t\\leq \\pi/2$ is?", "π/2",
         "$\\sqrt{x'^2+y'^2}=1$, so the integral is $\\pi/2$.", ["π", "1", "√2"]),
        ("For $x=t$, $y=t^2$ on $[0,1]$, the integrand $\\sqrt{1+(y')^2}$ is?", "\\sqrt{1+4t^2}",
         "$y'=2t$, so $\\sqrt{1+4t^2}$.", ["\\sqrt{1+t^2}", "1+2t", "\\sqrt{1+2t}"]),
        ("Speed equals which of the following?", "|r'(t)|",
         "By definition speed is the magnitude of velocity.", ["r'(t)", "a(t)", "x'(t) only"]),
        ("If speed is $5$ for $2$ seconds, distance traveled is?", 10,
         "Constant speed $5$ over time $2$ gives path length $10$.", ["5", "2.5", "7"]),
        ("Parametric arc length formula on $[a,b]$ is?", "∫_a^b √((dx/dt)^2+(dy/dt)^2) dt",
         "This is the integral of speed.", ["∫ y dx", "∫ r^2 dθ", "∫ |a(t)| dt"]),
        ("Horizontal polar tangents occur when which quantity is $0$ (and the denominator is not)?",
         "r' sin θ + r cos θ",
         "That is $dy/d\\theta$. Setting it to $0$ gives horizontal tangents.",
         ["r' cos θ − r sin θ", "r itself", "θ"]),
        ("Vertical polar tangents occur when $dx/d\\theta=0$ but $dy/d\\theta\\neq0$. That numerator-denominator pair is?",
         "r' cos θ − r sin θ = 0",
         "The denominator of $dy/dx$ is $dx/d\\theta$.",
         ["r' sin θ + r cos θ = 0", "r=0", "r'=0 only"]),
        ("For $r=2+2\\cos\\theta$, a cusp at the origin occurs when $r=0$, i.e. at $\\theta=$?", "π",
         "$2+2\\cos\\theta=0$ gives $\\cos\\theta=-1$, so $\\theta=\\pi$.", ["0", "π/2", "π/3"]),
        ("The cardioid $r=1-\\cos\\theta$ is symmetric about which axis?", "the polar axis (x-axis)",
         "Replacing $\\theta$ by $-\\theta$ leaves $r$ unchanged.", ["the y-axis", "y=x", "no symmetry"]),
        ("At a polar point where both $dx/d\\theta$ and $dy/d\\theta$ vanish, you should?",
         "use a limit of dy/dx as θ approaches that value",
         "The slope formula is $0/0$; the AP expectation is a limit, not a wild guess.",
         ["conclude the particle stopped forever", "set the slope equal to tan θ", "skip the point"]),
        ("A particle follows $x=t^2-1$, $y=t^3-t$. The slope $dy/dx$ at $t=2$ is?", "11/4",
         "$x'=2t$, $y'=3t^2-1$, so at $2$: $(12-1)/4=11/4$.", ["6", "11/2", "3"]),
        ("Vector $\\mathbf{r}(t)=\\langle \\ln t, t\\rangle$ for $t>0$. Speed at $t=e$ is?", "\\sqrt{1+e^2}/e",
         "$\\mathbf{v}=\\langle 1/t, 1\\rangle$, so $|\\mathbf{v}|=\\sqrt{1/t^2+1}=\\sqrt{1+t^2}/t$. At $t=e$: $\\sqrt{1+e^2}/e$.",
         ["√(1+e^2)", "1/e", "e"]),
        ("If $x=e^{t}$, $y=e^{-t}$, then $d^2y/dx^2$ at $t=0$ is?", 2,
         "$dy/dx=-e^{-2t}$, $d^2y/dx^2=2e^{-3t}$. At $0$ this is $2$.", ["-2", "0", "1"]),
        ("Displacement from $t=0$ to $t=2$ for $\\mathbf{r}(t)=\\langle t, t^2\\rangle$ is the vector?",
         "⟨2, 4⟩",
         "$\\mathbf{r}(2)-\\mathbf{r}(0)=\\langle 2,4\\rangle$. Distance traveled is longer than $|\\langle 2,4\\rangle|$.",
         ["⟨2, 2⟩", "√20", "⟨1, 2⟩"]),
        ("Polar $r=3$, a circle. $\\dfrac{dy}{dx}$ at $\\theta=\\pi/6$ equals?", "-√3",
         "$r'=0$, so slope $=\\dfrac{r\\cos\\theta}{-r\\sin\\theta}=-\\cot\\theta$. Since $\\cot(\\pi/6)=\\sqrt{3}$, the slope is $-\\sqrt{3}$.",
         ["√3", "1/√3", "0"]),
        ("The integrand for parametric arc length is identical to?", "speed",
         "Both are $\\sqrt{(dx/dt)^2+(dy/dt)^2}$.", ["acceleration", "slope dy/dx", "r(θ)"]),
        ("A particle's velocity is $\\langle 6t, 8t\\rangle$. Speed at $t=1$ is?", 10,
         "$\\sqrt{36+64}=10$.", ["14", "48", "√14"]),
        ("For $x=t-\\sin t$, $y=1-\\cos t$ (cycloid), $dy/dx$ at $t=\\pi/2$ is?", 1,
         "$x'=1-\\cos t$, $y'=\\sin t$. At $\\pi/2$: $1/1=1$.", ["0", "undefined", "2"]),
        ("Polar $r=2\\cos\\theta$ at $\\theta=\\pi/3$. The Cartesian point is?", "(1/2, √3/2)",
         "$r=1$, $x=\\cos(\\pi/3)=1/2$, $y=\\sin(\\pi/3)=\\sqrt{3}/2$.", ["(1, √3)", "(2, π/3)", "(√3/2, 1/2)"]),
        ("If a parametric tangent is horizontal, which is true?", "dy/dt=0 and dx/dt≠0",
         "Horizontal means $dy/dx=0$ with defined slope.", ["dx/dt=0 and dy/dt≠0", "both derivatives 0", "speed is 0"]),
        ("Chain-rule check: $\\dfrac{d}{dx}[\\sin(x^2)]$ at $x=\\sqrt{\\pi}$ is?", "-2√π",
         "$2x\\cos(x^2)$ evaluated at $\\sqrt{\\pi}$ is $2\\sqrt{\\pi}\\cos\\pi=-2\\sqrt{\\pi}$.",
         ["0", "2√π", "1"]),
        ("Quotient $f(x)=\\dfrac{x}{x+1}$. Then $f'(1)$ is?", "1/4",
         "$f'=\\dfrac{1}{(x+1)^2}$, so $f'(1)=1/4$.", ["1/2", "0", "2"]),
        ("The second derivative $d^2y/dx^2$ for a parametric curve is?",
         "(d/dt(dy/dx))/(dx/dt)",
         "Never divide $d^2y/dt^2$ by $d^2x/dt^2$.", ["(d²y/dt²)/(d²x/dt²)", "d²y/dt²", "y''/x''"]),
        ("Position $\\langle 4t, 3t\\rangle$. Distance traveled on $[0,2]$ is?", 10,
         "Speed is constantly $5$, times time $2$ is $10$.", ["5", "14", "√7"]),
        ("Polar $r=\\sin(2\\theta)$ is a 4-petal rose. Petals occur where $r=0$ at $\\theta=$?", "kπ/2",
         "$\\sin(2\\theta)=0$ when $2\\theta=k\\pi$, so $\\theta=k\\pi/2$.", ["kπ", "kπ/4", "kπ/3"]),
        ("If $\\mathbf{a}(t)=\\langle 0,-32\\rangle$ and $\\mathbf{v}(0)=\\langle 10, 20\\rangle$, then $v_y(1)$ is?", -12,
         "$v_y=20-32t$, so $v_y(1)=-12$.", ["20", "-32", "8"]),
        ("AP Stretch: $x=t^2$, $y=t^3-3t$. The curve crosses itself at $(3,0)$ (the two-parameter collision $t=\\pm\\sqrt{3}$). The two slopes there are?",
         "√3 and −√3",
         "$t_1^2=t_2^2$ with $t_2=-t_1\\neq t_1$ forces $t=\\pm\\sqrt{3}$, and both give $(x,y)=(3,0)$ (not the origin: $x=t^2=0$ only at $t=0$). "
         "$dy/dx=(3t^2-3)/(2t)=3(t^2-1)/(2t)$. At $t=\\sqrt{3}$: $3(2)/(2\\sqrt{3})=\\sqrt{3}$. At $t=-\\sqrt{3}$: $-\\sqrt{3}$.",
         ["0 and undefined", "1 and −1", "3 and −3"]),
        ("AP Stretch: Polar $r=1+2\\cos\\theta$ (limaçon). Inner-loop $r=0$ when $\\cos\\theta=-1/2$, so $\\theta=$?",
         "2π/3 and 4π/3",
         "On $[0,2\\pi]$, $\\cos\\theta=-1/2$ at $2\\pi/3$ and $4\\pi/3$. Those values bound the inner loop.",
         ["π/3 and 5π/3", "π/2 and 3π/2", "π/6 and 11π/6"]),
        ("AP Stretch: $\\mathbf{r}(t)=\\langle t^2, t^3\\rangle$. The unit tangent at $t=1$ is?",
         "⟨2/√13, 3/√13⟩",
         "$\\mathbf{v}=\\langle 2t,3t^2\\rangle=\\langle 2,3\\rangle$ at $t=1$, and $|\\mathbf{v}|=\\sqrt{13}$.",
         ["⟨2, 3⟩", "⟨1, 1⟩", "⟨2/5, 3/5⟩"]),
        ("AP Stretch: For $x=2t$, $y=t^2$, the value of $d^2y/dx^2$ at $t=3$ is?", "1/2",
         "$dy/dx=t$. Then $\\dfrac{d}{dt}(t)=1$ divided by $dx/dt=2$ gives $d^2y/dx^2=1/2$ at every $t$, including $t=3$.",
         ["1/4", "3", "6"]),
        ("AP Stretch: Polar slope of $r=e^{\\theta}$ at $\\theta=0$ equals?", "1",
         "$r'=e^{\\theta}=r$. Then $dy/dx=\\dfrac{r(\\sin\\theta+\\cos\\theta)}{r(\\cos\\theta-\\sin\\theta)}=\\dfrac{0+1}{1-0}=1$.",
         ["e", "0", "undefined"]),
        ("AP Stretch: Arc length of $x=t$, $y=\\dfrac{t^3}{6}+\\dfrac{1}{2t}$ from $t=1$ to $t=2$ equals?", "17/12",
         "$y'=t^2/2-1/(2t^2)$, and $1+(y')^2=(t^2/2+1/(2t^2))^2$, so the integrand is $t^2/2+1/(2t^2)$. "
         "Antiderivative $t^3/6-1/(2t)$ evaluated from $1$ to $2$: $(8/6-1/4)-(1/6-1/2)=17/12$.",
         ["2", "1", "7/6"]),
        ("AP Stretch: A particle has $\\mathbf{v}=\\langle \\cos t, \\sin t\\rangle$. Distance on $[0,\\pi]$ versus $|\\Delta\\mathbf{r}|$ are?",
         "π versus 2",
         "Speed is $1$, so distance is $\\pi$. Displacement uses $\\mathbf{r}=\\langle\\sin t, -\\cos t\\rangle+C$. "
         "$\\Delta\\mathbf{r}=\\langle 0, 2\\rangle$ if we integrate from $0$ to $\\pi$: $\\Delta x=\\sin\\pi-\\sin 0=0$, $\\Delta y=(-\\cos\\pi)-(-\\cos 0)=1+1=2$. Distance $\\pi$, $|\\Delta r|=2$.",
         ["π versus π", "2 versus π", "1 versus 0"]),
        ("AP Stretch: $r=2\\cos(3\\theta)$ is a 3-petal rose. A petal is traced on which $\\theta$-interval starting at the first positive zero of $r$?",
         "[π/6, π/2]",
         "$\\cos(3\\theta)=0$ when $3\\theta=\\pi/2+k\\pi$. The first positive zeros are $\\theta=\\pi/6$ and $\\theta=\\pi/2$, which bound one petal.",
         ["[0, π/3]", "[0, 2π]", "[0, π/6]"]),
        ("AP Stretch: Implicit $x^3+y^3=6xy$. The slope at $(3,3)$ is?", -1,
         "Differentiate: $3x^2+3y^2 y'=6y+6x y'$, so $(3y^2-6x)y'=6y-3x^2$. At $(3,3)$: $(27-18)y'=18-27$, hence $9y'=-9$ and $y'=-1$. "
         "The folium is symmetric in $x$ and $y$, so the tangent at $(3,3)$ must be $y=-x$ plus a constant, matching slope $-1$.",
         ["0", "1", "undefined"]),
    ])


def build_unit1():
    title = "AP Calculus BC Unit 1: AB Core + Parametric/Vector/Polar Derivatives"
    description = (
        "AB derivative toolkit plus parametric dy/dx and d²y/dx², vector motion, polar slope, "
        "speed, parametric arc length, and polar tangents."
    )
    concepts = [
        "AB derivative toolkit",
        "Parametric dy/dx and d²y/dx²",
        "Vector-valued motion",
        "Polar dy/dx",
        "Speed and parametric arc length",
        "Polar tangents (horizontal and vertical)",
    ]
    parabola = param_pts(lambda t: t, lambda t: t * t, -1.6, 1.6)
    c1 = concept_block(
        "1. AB derivative toolkit",
        [
            "AP Calculus BC still grades the entire AB derivative machine: power, product, quotient, chain, "
            "implicit, inverse, and the transcendental cluster $e^u$, $\\ln u$, $\\sin u$, $\\cos u$, $\\tan u$. "
            "A BC free-response part often starts with an ordinary $f'(x)$ computation before it asks a parametric or series follow-up.",
            "The derivative $f'(a)$ is the slope of the unique line that best matches $y=f(x)$ at $x=a$, provided that limit exists. "
            "On a graph that means a tangent, not a secant and not a vertical jump. On a table it means a difference quotient with a small $\\Delta x$.",
            "Product rule: $(uv)'=u'v+uv'$. Quotient: $\\left(\\dfrac{u}{v}\\right)'=\\dfrac{u'v-uv'}{v^2}$. Chain: "
            "$\\dfrac{d}{dx}[f(g(x))]=f'(g(x))g'(x)$. Write the outer derivative first, then multiply by the inner derivative — never skip the inner piece.",
            "Implicit differentiation treats $y$ as a function of $x$ without solving. Differentiate both sides, collect every $y'$ term, and solve. "
            "The same algebra produces related-rates equations when both $x$ and $y$ depend on $t$.",
            "Inverse functions satisfy $(f^{-1})'(b)=\\dfrac{1}{f'(a)}$ when $f(a)=b$ and $f'(a)\\neq0$. Logarithmic differentiation "
            "$y=x^x$ or $y=\\dfrac{(x+1)^2}{\\sqrt{x}}$ is just $\\ln$ of both sides, then implicit differentiation.",
            "On the exam, box the rule you are using before you expand. Most BC derivative errors are dropped chain-rule factors, not exotic BC content.",
        ],
        "Every later BC topic — parametric slope, polar slope, series term-by-term differentiation, Euler's method — is this toolkit in a new costume.",
        "Name the rule, write the formula with the actual functions, then substitute the number. If two rules apply, nest them from the outside in.",
        _fig(
            tangent_curve_svg(),
            "Tangent to $y=x^2/4$ at $P$",
            "The highlighted line is the derivative: slope $1$ at the marked point, matching $y'=x/2$.",
        )
        + solved(1, "Find $f'(x)$ if $f(x)=x^2\\sin x$.",
                 ["Product rule with $u=x^2$, $v=\\sin x$.",
                  "$u'=2x$ and $v'=\\cos x$.",
                  "$f'(x)=2x\\sin x+x^2\\cos x$."],
                 "$2x\\sin x+x^2\\cos x$", "Factor $x$ if a later part asks for zeros of $f'$.", "Easy")
        + solved(2, "If $x^2+y^2=25$, find $\\dfrac{dy}{dx}$ at $(3,-4)$.",
                 ["Differentiate: $2x+2y y'=0$.",
                  "Solve: $y'=-x/y$.",
                  "At $(3,-4)$: $y'=-3/(-4)=3/4$."],
                 "$3/4$", "The sign of $y$ matters; $(3,4)$ would have given $-3/4$.", "Medium")
        + solved(3, "Differentiate $y=\\ln(\\cos(3x))$ and evaluate $y'(0)$.",
                 ["Chain: $y'=\\dfrac{1}{\\cos(3x)}\\cdot(-\\sin(3x))\\cdot 3=-3\\tan(3x)$.",
                  "At $x=0$, $\\tan 0=0$, so $y'(0)=0$."],
                 "$0$", "The inner $3$ is the piece students drop on AP FRQ 1.", "Hard"),
        ("Dropping the inner derivative",
         "Chain rule failures look like $\\dfrac{d}{dx}\\sin(x^2)=\\cos(x^2)$ with the $2x$ missing. On a calculator section the graph of your "
         "answer will not match $f'$, which is a cheap self-check."),
        ("Write the name of the rule in the margin",
         "Readers award the derivative point for a correct setup even if arithmetic wobbles later. A labeled product/chain line is free insurance."),
        [],
        1,
    )
    c2 = concept_block(
        "2. Parametric dy/dx and d²y/dx²",
        [
            "A parametric curve is a pair $x=x(t)$, $y=y(t)$. The same path can be traced at different speeds; $t$ is time (or any parameter), not the slope.",
            "The first derivative is the ordinary chain-rule identity $\\dfrac{dy}{dx}=\\dfrac{dy/dt}{dx/dt}$ provided $dx/dt\\neq0$. "
            "If $dx/dt=0$ and $dy/dt\\neq0$, the tangent is vertical. If both vanish, the formula is $0/0$ and you must take a limit or factor.",
            "The second derivative is not $\\dfrac{d^2y/dt^2}{d^2x/dt^2}$. It is $\\dfrac{d^2y}{dx^2}=\\dfrac{\\dfrac{d}{dt}\\left(\\dfrac{dy}{dx}\\right)}{dx/dt}$. "
            "Compute $dy/dx$ as a function of $t$, differentiate that with respect to $t$, then divide by $x'(t)$ again.",
            "Concavity in $x$ is the sign of $d^2y/dx^2$, not the sign of $y''(t)$. A particle can speed up in $t$ while the path is still concave down in the plane.",
            "Eliminate the parameter only when it is easy (circles, lines, $y$ as a function of $x$). AP prefers the $t$-formulas, especially when $x(t)$ is not one-to-one.",
            "On FRQs, they will ask for $dy/dx$ at a specific $t$, then for $d^2y/dx^2$ at the same $t$, then whether the path is concave up. Keep the same $t$ throughout.",
        ],
        "Polar slope and vector motion are this paragraph with different names for $x(t)$ and $y(t)$.",
        "Always compute $x'(t)$ and $y'(t)$ first on scratch paper. Then form the quotient, then differentiate the quotient in $t$.",
        _fig(
            plot(
                curves=[("#4f46e5", parabola)],
                points=[(1, 1, "t=1")],
                arrows=[(1, 1, 1, 2, "v")],
                xlim=(-2, 2.5), ylim=(-0.5, 3.2),
            ),
            "Parametric path $x=t$, $y=t^2$ with velocity at $t=1$",
            "The path is the parabola $y=x^2$. The red arrow is $\\langle 1,2\\rangle$, so $dy/dx=2$ at that instant.",
        )
        + solved(4, "For $x=t^2$, $y=t^3$ with $t>0$, find $\\dfrac{dy}{dx}$ and $\\dfrac{d^2y}{dx^2}$.",
                 ["$x'=2t$, $y'=3t^2$, so $dy/dx=3t/2$.",
                  "$\\dfrac{d}{dt}(3t/2)=3/2$. Divide by $x'=2t$: $d^2y/dx^2=3/(4t)$."],
                 "$dy/dx=3t/2$, $d^2y/dx^2=3/(4t)$", "At $t=1$ the second derivative is $3/4>0$ (concave up).", "Easy")
        + solved(5, "The curve $x=\\cos t$, $y=\\sin t$. Find $dy/dx$ at $t=\\pi/3$.",
                 ["$x'=-\\sin t$, $y'=\\cos t$.",
                  "$dy/dx=-\\cot t$.",
                  "At $\\pi/3$, $-\\cot(\\pi/3)=-1/\\sqrt{3}$."],
                 "$-1/\\sqrt{3}$", "This is the unit circle; the Cartesian slope at that point is also $-x/y$ from implicit $x^2+y^2=1$.", "Medium")
        + solved(6, "Show that $x=t-\\sin t$, $y=1-\\cos t$ has a vertical tangent at $t=0$.",
                 ["$x'=1-\\cos t$, $y'=\\sin t$.",
                  "At $t=0$, $x'=0$ and $y'=0$, so the slope formula is $0/0$.",
                  "Limit: $\\dfrac{\\sin t}{1-\\cos t}\\cdot\\dfrac{1+\\cos t}{1+\\cos t}=\\dfrac{\\sin t(1+\\cos t)}{\\sin^2 t}=\\dfrac{1+\\cos t}{\\sin t}\\to\\infty$ as $t\\to 0^+$."],
                 "vertical tangent at the cusp $t=0$", "This is the cycloid generating cusp; AP loves this example.", "Hard"),
        ("Using (d²y/dt²)/(d²x/dt²)",
         "That quotient is not $d^2y/dx^2$. The correct extra division by $dx/dt$ is the entire point of the BC formula."),
        ("Keep dy/dx as a function of t",
         "Do not convert to $x$ before you differentiate unless the problem asks for a Cartesian expression. Differentiating in $t$ is faster and safer."),
        [],
        6,
    )
    circle_path = param_pts(lambda t: 3 * math.cos(t), lambda t: 3 * math.sin(t), 0, 1.9)
    c3 = concept_block(
        "3. Vector-valued motion",
        [
            "In the plane, position is a vector $\\mathbf{r}(t)=\\langle x(t), y(t)\\rangle$. Velocity is $\\mathbf{r}'(t)=\\langle x'(t), y'(t)\\rangle$, "
            "acceleration is $\\mathbf{r}''(t)$, and speed is the scalar $|\\mathbf{r}'(t)|$.",
            "Direction of motion is the direction of $\\mathbf{v}(t)$, not the direction of $\\mathbf{r}(t)$. A particle on a circle centered at the origin "
            "has position pointing outward and velocity tangent to the circle.",
            "Displacement from $t=a$ to $t=b$ is $\\mathbf{r}(b)-\\mathbf{r}(a)$, a vector. Distance traveled is $\\int_a^b |\\mathbf{v}(t)|\\,dt$, a scalar. "
            "They agree only when the particle never turns around.",
            "Given acceleration and an initial velocity, integrate componentwise. AP calculator FRQs often give $a_x(t)$ and $a_y(t)$ as messy formulas; "
            "your calculator integrates, you still have to add the constants from $\\mathbf{v}(0)$ and $\\mathbf{r}(0)$.",
            "The tangent line in the plane at time $t_0$ passes through $\\mathbf{r}(t_0)$ with direction $\\mathbf{v}(t_0)$. Parametric equations of that line "
            "are $X=x_0+x'(t_0)s$, $Y=y_0+y'(t_0)s$.",
            "When they ask whether speed is increasing, check the sign of $\\mathbf{v}\\cdot\\mathbf{a}$. Positive dot product means the particle is speeding up.",
        ],
        "This is the language of AP BC motion FRQs: position, velocity, speed, displacement, distance, and the tangent line in the plane.",
        "Draw $\\mathbf{r}$ and $\\mathbf{v}$ as arrows on the path. Most sign errors vanish once the picture exists.",
        _fig(
            plot(
                curves=[("#4f46e5", circle_path)],
                points=[(3, 0, "t=0")],
                arrows=[(0, 3, -3, 0, "v")],
                xlim=(-4, 4), ylim=(-4, 4),
            ),
            "Circular motion $\\mathbf{r}(t)=\\langle 3\\cos t, 3\\sin t\\rangle$",
            "At $t=\\pi/2$ the particle is at $(0,3)$ and velocity $\\langle -3,0\\rangle$ is tangent, pointing left.",
        )
        + solved(7, "Find the speed of $\\mathbf{r}(t)=\\langle t, t^2\\rangle$ at $t=1$.",
                 ["$\\mathbf{v}=\\langle 1, 2t\\rangle$.",
                  "At $t=1$, $\\mathbf{v}=\\langle 1,2\\rangle$.",
                  "Speed $\\sqrt{1+4}=\\sqrt{5}$."],
                 "$\\sqrt{5}$", "Speed is never the vector itself.", "Easy")
        + solved(8, "A particle has $\\mathbf{v}(t)=\\langle 3, 4t\\rangle$ and $\\mathbf{r}(0)=\\langle 1, 0\\rangle$. Find $\\mathbf{r}(2)$.",
                 ["Integrate: $x=3t+1$, $y=2t^2$.",
                  "At $t=2$: $x=7$, $y=8$."],
                 "$\\langle 7, 8\\rangle$", "The $+1$ is the initial $x$-position; forgetting constants is the classic miss.", "Medium")
        + solved(9, "For $\\mathbf{r}(t)=\\langle \\cos t, \\sin t\\rangle$ on $[0,\\pi]$, compare distance traveled with $|\\Delta\\mathbf{r}|$.",
                 ["Speed is $1$, so distance $=\\pi$.",
                  "$\\mathbf{r}(\\pi)-\\mathbf{r}(0)=\\langle -1-1, 0-0\\rangle=\\langle -2,0\\rangle$, magnitude $2$.",
                  "The particle went halfway around the unit circle: path length $\\pi$, net displacement $2$."],
                 "distance $\\pi$, $|\\Delta r|=2$", "AP will ask both in the same part B.", "Hard"),
        ("Calling velocity the speed",
         "Velocity is a vector. Speed is $|\\mathbf{v}|$. Writing $\\mathbf{v}=5$ loses the direction point on the rubric."),
        ("Integrate each component, then apply initial conditions",
         "Do not mix $x$ and $y$ antiderivatives. After integrating, plug $t=0$ (or the given time) to lock the constants."),
        [],
        11,
    )
    card = polar_pts(lambda th: 1 - math.cos(th), 0, 2 * math.pi, 200)
    c4 = concept_block(
        "4. Polar dy/dx",
        [
            "Polar coordinates label a point by a directed distance $r$ from the origin and an angle $\\theta$ from the positive $x$-axis. "
            "The conversion $x=r\\cos\\theta$, $y=r\\sin\\theta$ turns every polar graph $r=f(\\theta)$ into an ordinary parametric curve with parameter $\\theta$.",
            "Therefore $\\dfrac{dy}{dx}=\\dfrac{dy/d\\theta}{dx/d\\theta}$. Expanding the derivatives gives the memorized pair "
            "$\\dfrac{dy}{d\\theta}=r'\\sin\\theta+r\\cos\\theta$ and $\\dfrac{dx}{d\\theta}=r'\\cos\\theta-r\\sin\\theta$.",
            "You do not need to memorize those expansions if you are willing to differentiate $x=r(\\theta)\\cos\\theta$ with the product rule on the spot. "
            "Many BC students make fewer sign errors that way.",
            "When $r$ is negative, the point is plotted in the opposite direction. The slope formula still holds because $x$ and $y$ already include the sign of $r$.",
            "At the pole $r=0$, the Cartesian point is the origin no matter what $\\theta$ is. Different $\\theta$ values can give different tangent directions at the same geometric point.",
            "A polar FRQ will typically ask for $dy/dx$ at a given $\\theta$, then for the equation of the tangent line in $x$ and $y$. Convert the point to Cartesian first.",
        ],
        "Polar area in Unit 7 uses $r(\\theta)$ as a radius function. Polar slope in this unit uses the same $r(\\theta)$ as a parametric path.",
        "Convert to $x(\\theta)$, $y(\\theta)$, differentiate, divide. If the problem already gives $r$ and $r'$, plug into the expanded formula.",
        _fig(
            plot(
                curves=[("#4f46e5", card)],
                points=[(0, 0, "pole"), (0, 1, "θ=π/2")],
                arrows=[(0, 1, -1, 0, "tangent")],
                xlim=(-2.4, 0.6), ylim=(-1.6, 1.6),
            ),
            "Cardioid $r=1-\\cos\\theta$ with tangent at $\\theta=\\pi/2$",
            "At $\\theta=\\pi/2$, $r=1$, the point is $(0,1)$, and the polar slope formula gives a horizontal tangent.",
        )
        + solved(10, "For $r=2\\cos\\theta$, show that $dy/dx=0$ at $\\theta=\\pi/4$.",
                 ["$r'=-2\\sin\\theta$. At $\\pi/4$, $r=\\sqrt{2}$ and $r'=-\\sqrt{2}$.",
                  "Numerator: $-\\sqrt{2}\\cdot\\dfrac{\\sqrt{2}}{2}+\\sqrt{2}\\cdot\\dfrac{\\sqrt{2}}{2}=-1+1=0$.",
                  "Denominator is not zero, so the tangent is horizontal."],
                 "horizontal tangent", "This circle sits to the right of the origin; $\\theta=\\pi/4$ is the top-right point.", "Easy")
        + solved(11, "Find $dy/dx$ for $r=\\theta$ at $\\theta=\\pi$.",
                 ["$r'=1$, $r=\\pi$, $\\sin\\pi=0$, $\\cos\\pi=-1$.",
                  "Numerator $1\\cdot 0+\\pi(-1)=-\\pi$. Denominator $1(-1)-\\pi\\cdot 0=-1$.",
                  "Slope $=\\pi$."],
                 "$\\pi$", "The spiral $r=\\theta$ is not a circle; the slope at the negative $x$-axis is surprisingly $\\pi$.", "Medium")
        + solved(12, "The cardioid $r=1+\\cos\\theta$. Show the tangent at $\\theta=0$ is vertical.",
                 ["$r'=-\\sin\\theta$. At $0$, $r'=0$ and $r=2$.",
                  "Numerator $0+2\\cdot 1=2$. Denominator $0-2\\cdot 0=0$.",
                  "$dx/d\\theta=0$ while $dy/d\\theta\\neq0$, so the tangent is vertical at the Cartesian point $(2,0)$."],
                 "vertical tangent at $(2,0)$", "That is the rightmost dimple of the cardioid.", "Hard"),
        ("Using tan θ as the polar slope",
         "The ray from the origin has angle $\\theta$, but the curve's tangent is not that ray unless $r'=0$. Slope is $dy/dx$, not $\\tan\\theta$."),
        ("Convert the point before writing a tangent line",
         "The line must be in $x$ and $y$. A statement like $y-\\theta=m(x-r)$ is not a line in the plane."),
        [],
        16,
    )
    c5 = concept_block(
        "5. Speed and parametric arc length",
        [
            "Speed is $|\\mathbf{v}(t)|=\\sqrt{(x'(t))^2+(y'(t))^2}$. Parametric arc length on $[a,b]$ is the definite integral of that same expression. "
            "If you can find speed, you can find arc length; they are the same integrand.",
            "The formula is the Pythagorean theorem in disguise: in a tiny time $dt$ the particle moves $dx$ horizontally and $dy$ vertically, so $ds=\\sqrt{dx^2+dy^2}$.",
            "Unlike displacement, arc length does not cancel when the particle reverses. Absolute value (the square root of a sum of squares) is always nonnegative.",
            "Some AP integrands simplify dramatically after you expand $1+(y')^2$ inside the root. Look for perfect squares such as $\\left(\\dfrac{t^2}{2}+\\dfrac{1}{2t^2}\\right)^2$.",
            "If the integral does not simplify, the calculator section allows a numerical definite integral. Still write the exact integrand on paper for the setup point.",
            "Polar arc length $\\int\\sqrt{r^2+(r')^2}\\,d\\theta$ is Unit 7. Do not mix it with this parametric formula on a motion FRQ that gives $x(t)$ and $y(t)$.",
        ],
        "Distance versus displacement is the number-one scoring trap on BC motion questions.",
        "Write $L=\\int_a^b\\sqrt{(x')^2+(y')^2}\\,dt$, substitute the derivatives, simplify the radicand, then integrate or use the calculator.",
        _fig(
            plot(
                curves=[("#4f46e5", param_pts(lambda t: math.cos(t), lambda t: math.sin(t), 0, math.pi / 2))],
                points=[(1, 0, "t=0"), (0, 1, "t=π/2")],
                xlim=(-0.4, 1.4), ylim=(-0.4, 1.4),
            ),
            "Quarter circle $x=\\cos t$, $y=\\sin t$ on $[0,\\pi/2]$",
            "Speed is identically $1$, so arc length equals the time interval $\\pi/2$, matching a quarter of the unit circle.",
        )
        + solved(13, "Find the arc length of $x=\\cos t$, $y=\\sin t$ for $0\\leq t\\leq \\pi/2$.",
                 ["$x'=-\\sin t$, $y'=\\cos t$.",
                  "$\\sqrt{\\sin^2 t+\\cos^2 t}=1$.",
                  "$L=\\int_0^{\\pi/2} 1\\,dt=\\pi/2$."],
                 "$\\pi/2$", "Geometry confirms: quarter of a unit circle.", "Easy")
        + solved(14, "Set up — then evaluate — arc length of $x=t$, $y=t^{3/2}$ on $[0,1]$.",
                 ["$y'=\\dfrac{3}{2}t^{1/2}$, so $1+(y')^2=1+\\dfrac{9}{4}t$.",
                  "$L=\\int_0^1 \\sqrt{1+\\dfrac{9}{4}t}\\,dt$.",
                  "Antiderivative $\\dfrac{8}{27}\\left(1+\\dfrac{9}{4}t\\right)^{3/2}$ from $0$ to $1$ equals $\\dfrac{8}{27}\\left(\\left(\\dfrac{13}{4}\\right)^{3/2}-1\\right)$."],
                 r"$\dfrac{8}{27}\left(\left(\dfrac{13}{4}\right)^{3/2}-1\right)$", "Setup earns the first point even if the antiderivative slips.", "Medium")
        + solved(15, "A particle has speed $\\sqrt{1+4t^2}$. Distance on $[0,1]$ is the same as arc length of $x=t$, $y=t^2$ on that interval. Estimate or exact?",
                 ["Exact: $\\int_0^1\\sqrt{1+4t^2}\\,dt$ is a hyperbolic (or trig-sub) integral.",
                  "On a calculator FRQ, evaluate numerically: about $1.479$.",
                  "The exact antiderivative is $\\dfrac{t}{2}\\sqrt{1+4t^2}+\\dfrac{1}{4}\\ln\\bigl(2t+\\sqrt{1+4t^2}\\bigr)$."],
                 "numerical $\\approx 1.479$ (calculator) or the inverse-sinh antiderivative",
                 "BC allows either form if the setup is present.", "Hard"),
        ("Integrating velocity without the square root",
         "\\int v_x dt is a displacement component, not distance. Distance needs the speed integrand."),
        ("Simplify the radicand before integrating",
         "If 1+(y')^2 is a perfect square, the square root disappears and the integral is ordinary. Check that first every time."),
        [],
        21,
    )
    rose = polar_pts(lambda th: math.cos(2 * th), 0, 2 * math.pi, 240)
    c6 = concept_block(
        "6. Polar tangents (horizontal and vertical)",
        [
            "Horizontal tangents: set $dy/d\\theta=0$ and require $dx/d\\theta\\neq0$. Vertical tangents: set $dx/d\\theta=0$ and require $dy/d\\theta\\neq0$.",
            "If both derivatives vanish, the slope is indeterminate. Factor or use a two-sided limit in $\\theta$. Cardioids and roses do this at the pole.",
            "A rose $r=a\\cos(n\\theta)$ or $r=a\\sin(n\\theta)$ has $n$ petals if $n$ is odd and $2n$ petals if $n$ is even. Petals meet at the origin, where $r=0$.",
            "To find those $\\theta$ values, solve $r(\\theta)=0$ on an interval that traces the curve once (usually $[0,\\pi]$ for odd cosine roses and $[0,2\\pi]$ for even).",
            "The tangent line at a polar point still lives in the $xy$-plane. Convert $(r,\\theta)$ to $(x,y)$ before you write $y-y_0=m(x-x_0)$.",
            "AP may ask you to confirm a horizontal tangent by showing $dy/d\\theta=0$ with a nonzero denominator, then to use that tangent in a related-rates or area setup later.",
        ],
        "Recognizing horizontal versus vertical polar tangents is a standard BC multiple-choice classification item and a common FRQ follow-up.",
        "Compute $r$ and $r'$ at the given $\\theta$, form both $dx/d\\theta$ and $dy/d\\theta$, and classify zeros.",
        _fig(
            plot(
                curves=[("#4f46e5", rose)],
                points=[(1, 0, "θ=0"), (0, 0, "pole")],
                xlim=(-1.3, 1.3), ylim=(-1.3, 1.3),
            ),
            "Four-petal rose $r=\\cos 2\\theta$",
            "Petals touch the origin when $\\cos 2\\theta=0$. Tangents at the pole are found by limits of $dy/dx$ as $\\theta$ approaches those zeros.",
        )
        + solved(16, "Find $\\theta$ in $[0,\\pi)$ where $r=2+2\\cos\\theta$ has a horizontal tangent besides the obvious algebra.",
                 ["$r'=-2\\sin\\theta$. $dy/d\\theta=(-2\\sin\\theta)\\sin\\theta+(2+2\\cos\\theta)\\cos\\theta$.",
                  "Simplify: $-2\\sin^2\\theta+2\\cos\\theta+2\\cos^2\\theta=2(2\\cos^2\\theta+\\cos\\theta-1)$ because $\\cos^2-\\sin^2=\\cos 2\\theta$ alternatively expand.",
                  "Factor $2(2\\cos\\theta-1)(\\cos\\theta+1)=0$ after rewriting. Solutions $\\cos\\theta=1/2$ or $\\cos\\theta=-1$.",
                  "$\\theta=\\pi/3$ (and $\\cos\\theta=-1$ is the pole, where the tangent needs a limit)."],
                 r"$\theta=\pi/3$ (horizontal); $\theta=\pi$ is the pole", "Always check whether a candidate is the pole.", "Easy")
        + solved(17, "For $r=\\cos 2\\theta$, find a $\\theta$ where a petal meets the origin.",
                 ["Set $r=0$: $\\cos 2\\theta=0$, so $2\\theta=\\pi/2+k\\pi$.",
                  "The first positive solution is $\\theta=\\pi/4$."],
                 r"$\theta=\pi/4$ (and $\theta=3\pi/4$, $5\pi/4$, $7\pi/4$)", "Those four values are the petal joints for the even rose.", "Medium")
        + solved(18, "Show $r=e^{\\theta}$ never has a vertical tangent.",
                 ["$r'=e^{\\theta}=r>0$.",
                  "$dx/d\\theta=e^{\\theta}(\\cos\\theta-\\sin\\theta)$. This is zero when $\\tan\\theta=1$.",
                  "At those $\\theta$, $dy/d\\theta=e^{\\theta}(\\sin\\theta+\\cos\\theta)$. When $\\tan\\theta=1$, $\\sin=\\cos$, so $dy/d\\theta=2e^{\\theta}\\cos\\theta$, which is zero only if $\\cos\\theta=0$, contradicting $\\tan\\theta=1$.",
                  "Thus $dx/d\\theta=0$ never occurs with $dy/d\\theta=0$ simultaneously, but vertical tangents do occur when $\\tan\\theta=1$. Recheck: $dx/d\\theta=0$ when $\\cos=\\sin$, i.e. $\\theta=\\pi/4+k\\pi$, and $dy/d\\theta\\neq0$ there, so vertical tangents exist. The spiral does have vertical tangents.",
                  "Correct conclusion: vertical tangents at $\\theta=\\pi/4+k\\pi$; never both derivatives zero."],
                 r"vertical tangents when $\tan\theta=1$; no cusps", "Read zeros of the denominator carefully.", "Hard"),
        ("Reporting a polar θ as if it were a Cartesian slope",
         "θ is an angle of the radius ray. The tangent's slope is dy/dx, a different number."),
        ("Check the other derivative before classifying",
         "A zero numerator is a horizontal tangent only if the denominator is not also zero. The pole is the usual exception."),
        [],
        26,
    )
    content = unit_shell(
        title, AUDIENCE, concepts, c1 + c2 + c3 + c4 + c5 + c6,
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
        stretch_note=STRETCH_LABEL,
    )
    return title, description, content, _u1_questions()


# ===========================================================================
# UNIT 2
# ===========================================================================

def _u2_questions():
    return pack([
        ("Integration by parts starts from which product-rule rearrangement?", "∫ u dv = uv − ∫ v du",
         "Differentiate $uv$, integrate, and move one integral across.", ["∫ u dv = u dv", "∫ u dv = u'v", "∫ uv = u'v'"]),
        ("Using $u=x$, $dv=e^x dx$, $\\int x e^x\\,dx$ equals?", "e^x(x−1)+C",
         "$du=dx$, $v=e^x$, so $xe^x-\\int e^x dx=e^x(x-1)+C$.", ["xe^x+C", "e^x(x+1)+C", "e^x+C"]),
        ("$\\int_0^1 x e^x\\,dx$ equals?", 1,
         "$e^x(x-1)$ from $0$ to $1$ is $0-(-1)=1$.", ["e-1", "0", "e"]),
        ("$\\int_1^e \\ln x\\,dx$ equals?", 1,
         "$u=\\ln x$, $dv=dx$ gives $[x\\ln x-x]_1^e=(e-e)-(0-1)=1$.", ["e", "0", "e-1"]),
        ("For $\\int x\\sin x\\,dx$, LIATE says choose $u=$ ?", "x",
         "Algebraic $x$ comes before trig in LIATE, so $u=x$, $dv=\\sin x\\,dx$.", ["sin x", "x sin x", "1"]),
        ("Decompose $\\dfrac{1}{x(x+1)}$ into partial fractions.", "1/x − 1/(x+1)",
         "$1=A(x+1)+Bx$. $x=0$ gives $A=1$; $x=-1$ gives $B=-1$.", ["1/x + 1/(x+1)", "x/(x+1)", "1/(x+1) − 1/x"]),
        ("$\\int_1^2 \\dfrac{1}{x(x+1)}\\,dx$ equals?", "ln(4/3)",
         "$[\\ln|x|-\\ln|x+1|]_1^2=(\\ln2-\\ln3)-(\\ln1-\\ln2)=\\ln4-\\ln3=\\ln(4/3)$.", ["ln 2", "ln(3/2)", "1"]),
        ("$\\dfrac{3}{(x-1)(x+2)}=\\dfrac{A}{x-1}+\\dfrac{B}{x+2}$. Then $A$ is?", 1,
         "$x=1$: $3=A(3)$, so $A=1$. Then $B=-1$.", ["3", "-1", "1/3"]),
        ("$\\int_2^3 \\dfrac{1}{x^2-1}\\,dx$ equals?", "(1/2) ln(3/2)",
         "$\\dfrac{1}{2}\\ln\\left|\\dfrac{x-1}{x+1}\\right|$ from $2$ to $3$ is $\\dfrac{1}{2}\\bigl(\\ln(1/2)-\\ln(1/3)\\bigr)=\\dfrac{1}{2}\\ln(3/2)$.",
         ["ln 2", "1/2", "ln(3/2)"]),
        ("Partial fractions with distinct linear factors require the numerator degree to be?", "strictly less than the denominator degree",
         "If not, divide first. Then write $A/(x-r)$ for each distinct linear factor.",
         ["equal to the denominator degree", "one more than the denominator", "zero always"]),
        ("$\\int_0^{\\pi} \\sin^2 x\\,dx$ equals?", "π/2",
         "$\\sin^2 x=(1-\\cos 2x)/2$, so $\\int_0^{\\pi}(1-\\cos 2x)/2\\,dx=\\pi/2$.", ["π", "1", "0"]),
        ("$\\int_0^{\\pi/2} \\sin^3 x\\,dx$ equals?", "2/3",
         "Write $\\sin^3 x=(1-\\cos^2 x)\\sin x$, $u=\\cos x$, from $1$ to $0$: $\\int_0^1(1-u^2)\\,du=2/3$.", ["1/3", "1", "π/2"]),
        ("$\\int \\sec^2 x\\,dx$ equals?", "tan x + C",
         "This is the standard derivative of $\\tan x$.", ["sec x + C", "sec x tan x + C", "cos x + C"]),
        ("$\\int \\tan x\\,dx$ equals?", "ln|sec x| + C",
         "$\\int \\sin x/\\cos x\\,dx=-\\ln|\\cos x|+C=\\ln|\\sec x|+C$.", ["tan x + C", "sec x + C", "ln|sin x| + C"]),
        ("For an odd power of sine, the first algebraic move is?", "save one sin x and convert the rest with 1−cos²x",
         "Then $u=\\cos x$ finishes the integral.", ["use the double-angle formula only", "use tan(x/2)", "integrate by parts immediately"]),
        ("$\\int \\dfrac{dx}{\\sqrt{4-x^2}}$ equals?", "arcsin(x/2)+C",
         "This is the $a=2$ arcsine template, or $x=2\\sin\\theta$.", ["arccos(x/2)+C", "ln|4-x^2|+C", "arcsin x + C"]),
        ("$\\int_0^1 \\dfrac{dx}{\\sqrt{1-x^2}}$ equals?", "π/2",
         "$\\arcsin x$ from $0$ to $1$ is $\\pi/2-0$.", ["π", "1", "π/4"]),
        ("The substitution for $\\sqrt{a^2-x^2}$ is?", "x = a sin θ",
         "Then $\\sqrt{a^2-x^2}=a\\cos\\theta$ (acute $\\theta$).", ["x = a tan θ", "x = a sec θ", "x = a cosh θ"]),
        ("The substitution for $\\sqrt{x^2+a^2}$ is?", "x = a tan θ",
         "A right triangle with opposite $x$ and adjacent $a$ makes the hypotenuse $\\sqrt{x^2+a^2}$.",
         ["x = a sin θ", "x = a sec θ", "u = x^2+a^2 only"]),
        ("If $x=2\\sin\\theta$, then $\\sqrt{4-x^2}$ simplifies to?", "2 cos θ",
         "$\\sqrt{4-4\\sin^2\\theta}=2|\\cos\\theta|$.", ["2 sin θ", "2", "4 cos θ"]),
        ("$\\int_1^{\\infty} x^{-2}\\,dx$ equals?", 1,
         "$\\lim_{b\\to\\infty}[-1/x]_1^b=0-(-1)=1$.", ["0", "∞", "1/2"]),
        ("$\\int_1^{\\infty} \\dfrac{1}{x}\\,dx$ does what?", "diverges",
         "$\\ln b\\to\\infty$ as $b\\to\\infty$.", ["converges to 0", "converges to 1", "converges to ln 2"]),
        ("$\\int_0^{\\infty} e^{-x}\\,dx$ equals?", 1,
         "$\\lim_{b\\to\\infty}[-e^{-x}]_0^b=0-(-1)=1$.", ["0", "e", "∞"]),
        ("$\\int_1^{\\infty} \\dfrac{1}{1+x^2}\\,dx$ equals?", "π/4",
         "$\\arctan x$ from $1$ to $\\infty$ is $\\pi/2-\\pi/4=\\pi/4$.", ["π/2", "1", "π"]),
        ("The p-integral $\\int_1^{\\infty} x^{-p}\\,dx$ converges when?", "p > 1",
         "The antiderivative $x^{1-p}/(1-p)$ vanishes at infinity precisely when $p>1$.", ["p ≥ 1", "p < 1", "p > 0"]),
        ("$\\int_0^1 x^{-1/2}\\,dx$ equals?", 2,
         "$2x^{1/2}$ from $0$ to $1$ is $2$. The integrand blows up at $0$ but the area is finite.", ["0", "1", "diverges"]),
        ("$\\int_0^1 \\dfrac{1}{x}\\,dx$ does what?", "diverges",
         "$-\\ln\\varepsilon\\to\\infty$ as $\\varepsilon\\to 0^+$.", ["converges to 0", "converges to 1", "equals 2"]),
        ("$\\int_0^1 (1-x)^{-1/2}\\,dx$ equals?", 2,
         "$u=1-x$, $\\int_0^1 u^{-1/2}\\,du=2$.", ["1", "0", "diverges"]),
        ("An improper integral of Type 2 has which feature?", "the integrand becomes infinite on a finite interval",
         "Type 1 is an infinite interval; Type 2 is an infinite spike.",
         ["the interval is infinite", "the antiderivative is a log", "it always diverges"]),
        ("$\\int_{-1}^{1} x^{-2}\\,dx$ is?", "divergent",
         "There is a Type 2 singularity at $x=0$. Splitting and taking limits, both sides diverge. The naive $[-1/x]_{-1}^{1}=-2$ is illegal.",
         ["equal to −2", "equal to 2", "equal to 0"]),
        ("After parts, $\\int e^{x}\\cos x\\,dx$ requires a second parts step and then?", "solving for the original integral",
         "The original integral reappears; move it to the left and divide by $2$.",
         ["stopping after one parts", "switching to partial fractions", "declaring divergence"]),
        ("$\\int x\\ln x\\,dx$ (parts, $u=\\ln x$) equals?", "(1/2)x^2 ln x − x^2/4 + C",
         "$dv=x dx$, $v=x^2/2$, then $\\dfrac{1}{2}x^2\\ln x-\\int x/2\\,dx$.", ["x^2 ln x + C", "x ln x − x + C", "ln x + C"]),
        ("Cover-up: $\\dfrac{x+5}{(x-1)(x+2)}$ has $A$ at $x-1$ equal to?", 2,
         "Cover $x-1$: $(1+5)/(1+2)=6/3=2$.", ["1", "5", "3"]),
        ("$\\int \\sin^2 x\\cos x\\,dx$ is best done by?", "u = sin x",
         "The cosine is already the derivative of sine (up to a constant).", ["parts with u=sin²x", "partial fractions", "x = sin θ"]),
        ("$\\int_0^{\\pi/4} \\sec^2 x\\,dx$ equals?", 1,
         "$\\tan x$ from $0$ to $\\pi/4$ is $1$.", ["√2", "π/4", "0"]),
        ("Trig sub $x=2\\tan\\theta$ is aimed at which radicand?", "√(x^2+4)",
         "Opposite $x$, adjacent $2$, hypotenuse $\\sqrt{x^2+4}$.", ["√(4−x^2)", "√(x^2−4)", "√x"]),
        ("$\\lim_{b\\to\\infty}\\int_1^b e^{-2x}\\,dx$ equals?", "1/(2e^2)",
         "$[-\\frac12 e^{-2x}]_1^{\\infty}=0-(-\\frac12 e^{-2})=\\dfrac{1}{2e^{2}}$.",
         ["1/2", "0", "∞"]),
        ("Comparison: $0\\leq \\dfrac{1}{x^2+x}\\leq \\dfrac{1}{x^2}$ for $x\\geq 1$. Conclusion for $\\int_1^{\\infty}$?",
         "the smaller integral converges because the p=2 integral does",
         "Direct comparison: a nonnegative integrand squeezed under a convergent integral converges.",
         ["both diverge", "the comparison is illegal", "it converges to 1"]),
        ("$\\int_0^1 x^{-0.9}\\,dx$ converges because the Type 2 p-test needs?", "p < 1 for ∫_0^1 x^{-p}",
         "Near $0$, $p=0.9<1$, so the spike is integrable.", ["p > 1", "p = 1", "p > 2"]),
        ("A correct parts table setup for $\\int x^2\\sin x\\,dx$ begins with $u=$ ?", "x^2",
         "Differentiate the polynomial; integrate the sine.", ["sin x", "x^2 sin x", "2x"]),
        ("$\\dfrac{2x+3}{(x+1)(x+2)}$ equals?", "1/(x+1) + 1/(x+2)",
         "Cover-up: at $-1$, $(1)/(1)=1$; at $-2$, $(-1)/(-1)=1$.", ["2/(x+1)+3/(x+2)", "1/(x+1)−1/(x+2)", "(2x+3)/(x^2+3x+2)"]),
        ("$\\int \\cos^2 x\\,dx$ uses which identity?", "(1+cos 2x)/2",
         "Even powers of cosine (or sine) need the power-reduction formula.", ["1−sin^2 x only", "cos 2x", "2 cos x"]),
        ("Why is $\\int_{-1}^{1} \\dfrac{1}{x}\\,dx$ not equal to $0$ by oddness?",
         "the integral is improper at 0 and both one-sided limits diverge",
         "Odd-function cancellation requires a genuine improper-limit pair that both exist.",
         ["it is equal to 0", "the function is even", "FTC says ln|x| from −1 to 1 is 0"]),
        ("$\\int x\\sec^2 x\\,dx$ by parts with $dv=\\sec^2 x\\,dx$ produces $v=$ ?", "tan x",
         "Then $uv-\\int\\tan x\\,dx=x\\tan x-\\int\\tan x\\,dx$.", ["sec x", "x tan x", "sec^2 x"]),
        ("Why might someone split $\\int_0^{\\infty} \\dfrac{1}{1+x^2}\\,dx$ at $x=1$?",
         "the split is optional; only the ∞ bound is improper",
         "The integrand is continuous on $[0,\\infty)$. Splitting at $1$ is legal but not required. The only improper feature is the infinite interval.",
         ["the function is undefined at 1", "both pieces diverge", "partial fractions require it"]),
        ("$\\int_2^{\\infty} \\dfrac{1}{x\\ln x}\\,dx$ diverges because?", "the antiderivative ln(ln x) → ∞",
         "$u=\\ln x$, $\\int du/u=\\ln|u|$. As $x\\to\\infty$, $\\ln(\\ln x)\\to\\infty$.",
         ["p=2 comparison", "it equals 1", "e^{-x} dominates"]),
        ("AP Stretch: $\\int_0^1 x\\ln x\\,dx$ (limit as $a\\to 0^+$) equals?", "-1/4",
         "$\\dfrac{1}{2}x^2\\ln x-x^2/4$ from $a$ to $1$ is $-1/4-(a^2/2\\ln a-a^2/4)$. And $a^2\\ln a\\to 0$, so the value is $-1/4$.",
         ["0", "1/4", "diverges"]),
        ("AP Stretch: Decompose $\\dfrac{x^2+1}{x(x-1)(x+1)}$. The coefficient of $1/x$ is?", -1,
         "Cover $x$: $(0+1)/((-1)(1))=-1$.", ["1", "0", "1/2"]),
        ("AP Stretch: $\\int_0^{\\pi/2} \\sin^2 x\\cos^2 x\\,dx$ equals?", "π/16",
         "$\\sin^2\\cos^2=(\\sin 2x/2)^2=(1-\\cos 4x)/8$. Integrate: $\\int_0^{\\pi/2}(1-\\cos 4x)/8\\,dx=(\\pi/2)/8=\\pi/16$.",
         ["π/8", "1/8", "π/4"]),
        ("AP Stretch: After $x=2\\sin\\theta$, $\\int_0^{\\sqrt{2}} \\sqrt{4-x^2}\\,dx$ equals?", "π/2 + 1",
         "$\\sqrt{4-x^2}=2\\cos\\theta$, $dx=2\\cos\\theta\\,d\\theta$, $x:0\\to\\sqrt{2}$ means $\\theta:0\\to\\pi/4$. "
         "$\\int_0^{\\pi/4} 4\\cos^2\\theta\\,d\\theta=2\\int(1+\\cos 2\\theta)d\\theta=2(\\theta+\\sin 2\\theta/2)_0^{\\pi/4}=2(\\pi/4+1/2)=\\pi/2+1$.",
         ["π", "2", "π/2"]),
        ("AP Stretch: $\\int_e^{\\infty} \\dfrac{dx}{x(\\ln x)^2}$ equals?", 1,
         "$u=\\ln x$, $du=dx/x$, from $1$ to $\\infty$: $\\int_1^{\\infty} u^{-2}du=1$.", ["0", "e", "diverges"]),
        ("AP Stretch: $\\int_0^1 \\dfrac{\\ln x}{\\sqrt{x}}\\,dx$ converges to?", -4,
         "Parts or known limit: $u=\\ln x$, $dv=x^{-1/2}dx$, and $x^{1/2}\\ln x\\to 0$ at $0$. The value is $2[x^{1/2}\\ln x]_0^1-2\\int_0^1 x^{-1/2}dx=-4$.",
         ["-2", "0", "diverges"]),
        ("AP Stretch: $\\int_2^{\\infty}\\dfrac{x}{x^3+1}\\,dx$ converges by comparison with?", "1/x^2",
         "For large $x$, $\\dfrac{x}{x^3+1}\\sim x^{-2}$. Limit comparison with $1/x^2$ gives $1$.",
         ["1/x", "e^{-x}", "1/x^3"]),
        ("AP Stretch: A Type 2 split of $\\int_0^3 (x-1)^{-2/3}\\,dx$ at $x=1$ yields?", "3(2^{1/3}+1)",
         "Antiderivative $3(x-1)^{1/3}$. Limits from both sides exist: $3(2)^{1/3}-0$ plus $0-3(-1)^{1/3}=3+3\\cdot 2^{1/3}$. "
         "From $0$ to $1^-$: $0-3(-1)^{1/3}=3$; from $1^+$ to $3$: $3\\cdot 2^{1/3}$. Total $3+3\\cdot 2^{1/3}=3(1+2^{1/3})$.",
         ["diverges", "3", "0"]),
        ("AP Stretch: $\\int_0^{\\pi} x\\sin x\\,dx$ equals?", "π",
         "Parts: $u=x$, $dv=\\sin x dx$, $[-x\\cos x]_0^{\\pi}+\\int_0^{\\pi}\\cos x\\,dx=\\pi+0=\\pi$.",
         ["0", "2", "π/2"]),
    ])


def build_unit2():
    title = "AP Calculus BC Unit 2: Advanced Integration Techniques"
    description = (
        "Integration by parts, nonrepeating partial fractions, trigonometric integrals and substitutions, "
        "and improper integrals of Types 1 and 2."
    )
    concepts = [
        "Integration by parts",
        "Partial fractions (nonrepeating linear factors)",
        "Trigonometric integrals",
        "Trigonometric substitution (intro)",
        "Improper integrals Type 1 (infinite interval)",
        "Improper integrals Type 2 (infinite integrand)",
    ]
    c1 = concept_block(
        "1. Integration by parts",
        [
            "The product rule $(uv)'=u'v+uv'$ rearranges into $\\int u\\,dv=uv-\\int v\\,du$. You choose $u$ to become simpler when differentiated "
            "and $dv$ to be something you can integrate. LIATE (Log, Inverse trig, Algebraic, Trig, Exponential) is a memory aid, not a theorem.",
            "A definite parts formula is $\\int_a^b u\\,dv=[uv]_a^b-\\int_a^b v\\,du$. Evaluate the boundary term carefully; it is often where the points live.",
            "Cyclic parts ($e^{ax}\\sin bx$ or $e^{ax}\\cos bx$) need two applications. The original integral returns; solve for it algebraically.",
            "If $u=\\ln x$ and $dv=dx$, you obtain the important antiderivative $x\\ln x-x$. Combined with a limit at $0^+$, this evaluates $\\int_0^1\\ln x\\,dx=-1$.",
            "Tabular parts (Unit 3) is the same theorem organized in columns when $u$ is a polynomial. Learn the single-step version first so you can see where the signs come from.",
            "On AP FRQs, write $u=\\ldots$, $dv=\\ldots$, $du=\\ldots$, $v=\\ldots$ on three lines. Readers give the parts point for a correct identification even if later arithmetic slips.",
        ],
        "Parts is how BC extracts polynomials from exponentials, sines, and logs — and how many series remainder integrals are born.",
        "Differentiate the factor that simplifies; integrate the factor whose antiderivative is still in your toolkit.",
        _fig(
            plot(
                curves=[("#4f46e5", sample_curve(lambda x: x * math.exp(-x), 0, 6, 70))],
                fills=[(shade_under(lambda x: x * math.exp(-x), 0, 6, 40), "#c7d2fe")],
                xlim=(-0.3, 6.2), ylim=(-0.2, 0.5),
            ),
            "The integrand $x e^{-x}$ (parts with $u=x$)",
            "The shaded region is $\\int_0^\\infty x e^{-x}\\,dx=1$, the Gamma-function value $\\Gamma(2)$.",
        )
        + solved(1, "Find $\\int x e^{x}\\,dx$.",
                 ["Set $u=x$, $dv=e^{x} dx$, so $du=dx$, $v=e^{x}$.",
                  "$xe^{x}-\\int e^{x}\\,dx=xe^{x}-e^{x}+C$.",
                  "Factor $e^{x}(x-1)+C$."],
                 "$e^{x}(x-1)+C$", "Check by differentiating: product rule returns $x e^{x}$.", "Easy")
        + solved(2, "Evaluate $\\int_1^e \\ln x\\,dx$.",
                 ["$u=\\ln x$, $dv=dx$, $du=dx/x$, $v=x$.",
                  "$[x\\ln x]_1^e-\\int_1^e 1\\,dx=(e-0)-(e-1)=1$."],
                 "$1$", "The boundary term at $1$ is $1\\cdot 0=0$.", "Medium")
        + solved(3, "Evaluate $\\int_0^{\\pi} x\\sin x\\,dx$.",
                 ["$u=x$, $dv=\\sin x dx$, $v=-\\cos x$.",
                  "$[-x\\cos x]_0^{\\pi}+\\int_0^{\\pi}\\cos x\\,dx=\\pi + [\\sin x]_0^{\\pi}=\\pi$."],
                 "$\\pi$", "At $x=\\pi$, $-\\pi\\cos\\pi=-\\pi(-1)=\\pi$; at $0$ the term is $0$.", "Hard"),
        ("Choosing u to be the factor you cannot differentiate",
         "If you set $u=e^{x}$ in $\\int x e^{x}\\,dx$, parts makes the integral worse. LIATE exists to stop that."),
        ("Write the uv boundary term with brackets",
         "On a definite integral, evaluating uv at both ends is a separate rubric point from the remaining integral."),
        [],
        1,
    )
    c2 = concept_block(
        "2. Partial fractions (nonrepeating linear factors)",
        [
            "If a rational function has a denominator that factors into distinct linear pieces and the numerator degree is smaller, write "
            "$\\dfrac{p(x)}{(x-r_1)\\cdots(x-r_k)}=\\dfrac{A_1}{x-r_1}+\\cdots+\\dfrac{A_k}{x-r_k}$.",
            "The cover-up method: to get $A_j$, drop the factor $(x-r_j)$ from the original denominator and evaluate what remains at $x=r_j$.",
            "If the numerator degree is not smaller, polynomial-divide first. The quotient is a polynomial you integrate on the spot; only the remainder needs partial fractions.",
            "Each term $A/(x-r)$ integrates to $A\\ln|x-r|$. Definite integrals become differences of logs, which you should combine into a single $\\ln$ of a quotient.",
            "Irreducible quadratics (like $x^2+1$) belong to a later template: $Bx+C$ over the quadratic. This lesson stays with distinct linear factors, the AP BC workhorse.",
            "A common exam trap is a missing factor after you cancel. Always multiply back to check $A(x-r_2)+B(x-r_1)$ recovers the numerator.",
        ],
        "Repeating factors in Unit 3 add extra terms $B/(x-r)^2$. Master the distinct case first.",
        "Factor the denominator, write one $A/(x-r)$ per root, cover-up, integrate logs.",
        _fig(
            plot(
                curves=[("#4f46e5", sample_curve(lambda x: 1 / (x * (x + 1)), 0.35, 4, 70))],
                fills=[(shade_under(lambda x: 1 / (x * (x + 1)), 1, 2, 30), "#bbf7d0")],
                xlim=(0, 4.2), ylim=(-0.2, 1.4),
                dashes=[("v", 1, "1"), ("v", 2, "2")],
            ),
            "$y=1/(x(x+1))$ with $\\int_1^2$ shaded",
            "Partial fractions turn the shaded area into $\\ln(4/3)$. Vertical asymptotes at $x=0$ and $x=-1$ stay off this window.",
        )
        + solved(4, "Decompose $\\dfrac{1}{x(x+1)}$.",
                 ["$\\dfrac{1}{x(x+1)}=\\dfrac{A}{x}+\\dfrac{B}{x+1}$.",
                  "$1=A(x+1)+Bx$. Set $x=0$: $A=1$. Set $x=-1$: $B=-1$.",
                  "So $\\dfrac{1}{x}-\\dfrac{1}{x+1}$."],
                 "$1/x-1/(x+1)$", "Multiply back: $(x+1)-x=1$. ✓", "Easy")
        + solved(5, "Evaluate $\\int_1^2 \\dfrac{1}{x(x+1)}\\,dx$.",
                 ["Antiderivative $\\ln|x|-\\ln|x+1|=\\ln\\left|\\dfrac{x}{x+1}\\right|$.",
                  "From $1$ to $2$: $\\ln(2/3)-\\ln(1/2)=\\ln(4/3)$."],
                 "$\\ln(4/3)$", "Combining logs before substituting reduces sign errors.", "Medium")
        + solved(6, "Find $A,B$ for $\\dfrac{x+5}{(x-1)(x+2)}=\\dfrac{A}{x-1}+\\dfrac{B}{x+2}$.",
                 ["Cover $x-1$: $A=(1+5)/(1+2)=2$.",
                  "Cover $x+2$: $B=(-2+5)/(-2-1)=3/(-3)=-1$.",
                  "Check: $2(x+2)-(x-1)=2x+4-x+1=x+5$."],
                 "$A=2$, $B=-1$", "Cover-up is faster than a $2\\times 2$ system once the factors are linear and distinct.", "Hard"),
        ("Forgetting to divide when degrees are equal",
         "If numerator degree is not smaller, partial fractions is applied to the remainder after division, not to the original fraction."),
        ("Combine the log answer into one logarithm",
         "AP answer keys almost always write ln|(x-a)^p (x-b)^q|. Combining also makes definite-integral arithmetic shorter."),
        [],
        6,
    )
    c3 = concept_block(
        "3. Trigonometric integrals",
        [
            "Odd sine power: factor one $\\sin x$, convert the remaining even power with $\\sin^2=1-\\cos^2$, and set $u=\\cos x$. Odd cosine powers are symmetric with $u=\\sin x$.",
            "Even powers of sine or cosine: use the power-reduction identities $\\sin^2 x=(1-\\cos 2x)/2$ and $\\cos^2 x=(1+\\cos 2x)/2$. Repeat if the power is $4$ or higher.",
            "Products $\\sin mx\\cos nx$ use the prosthaphaeresis (product-to-sum) identities, or a substitution if one factor is the derivative of the other.",
            "Tangent and secant have their own pairing: odd secant, save one $\\sec\\tan$; even secant, save $\\sec^2$ and use $\\tan^2=\\sec^2-1$.",
            "On $[0,\\pi/2]$ the classic wall $\\int_0^{\\pi/2}\\sin^n x\\cos^m x\\,dx$ is often a Beta-function value, but AP expects the $u$-sub or reduction identity, not the name Beta.",
            "A calculator FRQ may still want an exact antiderivative. Reduction identities are the expected exact method.",
        ],
        "Trig substitution in the next lesson turns algebraic square roots into these same integrals.",
        "Classify the powers (odd vs even) before you write a single $u$.",
        _fig(
            unit_circle_svg(90),
            "Unit circle: $\\sin^2+\\cos^2=1$ is the conversion engine",
            "Every odd-power trick is this Pythagorean identity plus one leftover factor whose derivative is sitting in the integrand.",
        )
        + solved(7, "Evaluate $\\int_0^{\\pi}\\sin^2 x\\,dx$.",
                 ["$\\sin^2 x=(1-\\cos 2x)/2$.",
                  "$\\int_0^{\\pi}(1-\\cos 2x)/2\\,dx=[x/2-\\sin 2x/4]_0^{\\pi}=\\pi/2$."],
                 "$\\pi/2$", "The average value of $\\sin^2$ over a full period is $1/2$.", "Easy")
        + solved(8, "Evaluate $\\int_0^{\\pi/2}\\sin^3 x\\,dx$.",
                 ["$\\sin^3 x=(1-\\cos^2 x)\\sin x$.",
                  "$u=\\cos x$, $du=-\\sin x dx$, limits $1$ down to $0$.",
                  "$\\int_0^1(1-u^2)\\,du=[u-u^3/3]_0^1=2/3$."],
                 "$2/3$", "The leftover $\\sin x$ became $du$.", "Medium")
        + solved(9, "Evaluate $\\int_0^{\\pi/2}\\sin^2 x\\cos^2 x\\,dx$.",
                 ["$\\sin^2\\cos^2=(\\sin 2x/2)^2=(1-\\cos 4x)/8$.",
                  "$\\int_0^{\\pi/2}(1-\\cos 4x)/8\\,dx=(\\pi/2)/8=\\pi/16$."],
                 "$\\pi/16$", "Power-reduction twice is faster than a double $u$-sub here.", "Hard"),
        ("Using sin²=1−cos² on an even power and getting stuck",
         "If both powers are even, 1−cos² does not produce a leftover derivative. Use the double-angle identities instead."),
        ("Check the interval length against the average value",
         "Over a whole number of half-periods, ∫ sin² = (length)/2. That mental check catches a dropped 1/2."),
        [],
        11,
    )
    c4 = concept_block(
        "4. Trigonometric substitution (intro)",
        [
            "Three triangles cover the AP intro: $\\sqrt{a^2-x^2}$ with $x=a\\sin\\theta$, $\\sqrt{x^2+a^2}$ with $x=a\\tan\\theta$, and $\\sqrt{x^2-a^2}$ with $x=a\\sec\\theta$.",
            "Draw the right triangle, label the sides, and replace the radical by the remaining side. Also replace $dx$ by the $\\theta$-differential. Limits change from $x$ to $\\theta$.",
            "After integrating in $\\theta$, convert back using the triangle (for an indefinite integral) or evaluate in $\\theta$ (for a definite integral — often cleaner).",
            "The inverse-sine integral $\\int dx/\\sqrt{a^2-x^2}=\\arcsin(x/a)+C$ is the $x=a\\sin\\theta$ case with no extra algebra. Memorize it, then know why it is true.",
            "Absolute values: $\\sqrt{a^2\\cos^2\\theta}=a|\\cos\\theta|$. On a definite integral whose $\\theta$-interval keeps cosine nonnegative, you may drop the bars.",
            "AP rarely needs the full hyperbolic substitutes. If you see $\\sqrt{x^2+a^2}$ on a noncalculator page, $x=a\\tan\\theta$ is the intended path.",
        ],
        "These substitutions turn geometric lengths (chords of circles, hyperbolas) into trig integrals you already know.",
        "Match the radicand to a triangle, write $x$ and $dx$, simplify the square root, integrate, convert back.",
        _fig(
            labeled_right_triangle(a=3, b=4, c=5, a_lab="√(a²−x²)", b_lab="x", c_lab="a", angle_lab="θ"),
            "Reference triangle for $x=a\\sin\\theta$",
            "Opposite $x$, hypotenuse $a$, so the adjacent side is $\\sqrt{a^2-x^2}$. That is the entire substitution.",
        )
        + solved(10, "Find $\\int \\dfrac{dx}{\\sqrt{4-x^2}}$.",
                 ["This matches $\\arcsin(x/a)$ with $a=2$.",
                  "Alternatively $x=2\\sin\\theta$, $dx=2\\cos\\theta d\\theta$, radical $2\\cos\\theta$.",
                  "The integral collapses to $\\int d\\theta=\\theta=\\arcsin(x/2)+C$."],
                 "$\\arcsin(x/2)+C$", "Memorizing the arcsine template is allowed; deriving it is safer.", "Easy")
        + solved(11, "Evaluate $\\int_0^1 \\dfrac{dx}{\\sqrt{1-x^2}}$.",
                 ["Antiderivative $\\arcsin x$.",
                  "$\\arcsin 1-\\arcsin 0=\\pi/2$."],
                 "$\\pi/2$", "Geometrically this is a quarter of the unit-circle upper area's inverse-sine cousin: the angle itself.", "Medium")
        + solved(12, "Evaluate $\\int_0^{\\sqrt{2}}\\sqrt{4-x^2}\\,dx$ using $x=2\\sin\\theta$.",
                 ["$dx=2\\cos\\theta d\\theta$, $\\sqrt{4-x^2}=2\\cos\\theta$, $x=0\\Rightarrow\\theta=0$, $x=\\sqrt{2}\\Rightarrow\\theta=\\pi/4$.",
                  "$\\int_0^{\\pi/4}4\\cos^2\\theta\\,d\\theta=2\\int_0^{\\pi/4}(1+\\cos 2\\theta)\\,d\\theta=2[\\theta+\\sin 2\\theta/2]_0^{\\pi/4}=\\pi/2+1$."],
                 "$\\pi/2+1$", "This is the area under the circle $x^2+y^2=4$ from $x=0$ to $x=\\sqrt{2}$.", "Hard"),
        ("Forgetting to change dx",
         "Substituting x in the radical but leaving dx as dx is the usual incomplete substitution. Always replace dx too."),
        ("Change the limits when the integral is definite",
         "If x=2 sin θ and x goes from 0 to 1, θ goes from 0 to π/6. Evaluating in θ avoids a messy back-substitution."),
        [],
        16,
    )
    c5 = concept_block(
        "5. Improper integrals Type 1 (infinite interval)",
        [
            "Type 1 means at least one limit of integration is infinite: $\\int_a^{\\infty} f(x)\\,dx=\\lim_{b\\to\\infty}\\int_a^b f(x)\\,dx$, when that limit exists as a finite number.",
            "The p-integral $\\int_1^{\\infty} x^{-p}\\,dx$ converges if and only if $p>1$. This is the comparison benchmark for almost every rational tail on AP.",
            "Exponential decay beats any polynomial: $\\int_1^{\\infty} x^n e^{-x}\\,dx$ converges for every $n$. Logs grow slowly: $\\int_2^{\\infty} dx/(x\\ln x)$ diverges.",
            "Direct comparison: if $0\\leq f\\leq g$ and $\\int g$ converges, so does $\\int f$. If $\\int f$ diverges and $f\\geq g\\geq 0$, so does $\\int g$.",
            "Limit comparison: if $f,g>0$ and $\\lim f/g=L$ with $0<L<\\infty$, then $\\int f$ and $\\int g$ both converge or both diverge.",
            "Always write the limit in $b$ (or $a\\to-\\infty$). An answer that never mentions a limit is incomplete on the FRQ rubric.",
        ],
        "The integral test for series in Unit 4 is this paragraph applied to $f(n)$.",
        "Replace the infinite bound by $b$, integrate, then take $b\\to\\infty$. Name the comparison function if you cannot integrate.",
        _fig(
            plot(
                curves=[("#4f46e5", sample_curve(lambda x: 1 / (x * x), 0.7, 6.5, 70))],
                fills=[(shade_under(lambda x: 1 / (x * x), 1, 6.5, 40), "#c7d2fe")],
                xlim=(0, 7), ylim=(-0.1, 1.3),
                points=[(1, 1, "x=1")],
            ),
            "Type 1 tail $\\int_1^{\\infty} x^{-2}\\,dx$",
            "The shaded region continues to the right without bound, yet its area approaches $1$. The graph is not a spike at the origin.",
        )
        + solved(13, "Evaluate $\\int_1^{\\infty} x^{-2}\\,dx$.",
                 ["$\\lim_{b\\to\\infty}[-1/x]_1^b=\\lim_{b\\to\\infty}(-1/b+1)=1$."],
                 "$1$", "p=2>1, so convergence was expected.", "Easy")
        + solved(14, "Show $\\int_1^{\\infty} x^{-1}\\,dx$ diverges.",
                 ["$\\lim_{b\\to\\infty}[\\ln x]_1^b=\\lim_{b\\to\\infty}\\ln b=\\infty$."],
                 "diverges", "This is the harmonic integral, twin of the harmonic series.", "Medium")
        + solved(15, "Evaluate $\\int_1^{\\infty}\\dfrac{1}{1+x^2}\\,dx$.",
                 ["$\\lim_{b\\to\\infty}\\arctan b-\\arctan 1=\\pi/2-\\pi/4=\\pi/4$."],
                 "$\\pi/4$", "The tail of arctan is a finite leftover angle.", "Hard"),
        ("Dropping the limit and writing ∞ as if it were a number",
         "You may not plug x=∞ into an antiderivative. The limit is the definition of the improper integral."),
        ("Compare with the right p-integral",
         "For a rational function, look at the degree difference. Degree den − degree num ≥ 2 is the usual convergent tail."),
        [],
        21,
    )
    c6 = concept_block(
        "6. Improper integrals Type 2 (infinite integrand)",
        [
            "Type 2 means $f$ blows up at a finite endpoint or at an interior point of $[a,b]$. You replace that bad point by a one-sided limit.",
            "If the singularity is interior, you must split the integral there and take two independent limits. Both must exist for the whole integral to converge.",
            "The p-test near $0$: $\\int_0^1 x^{-p}\\,dx$ converges iff $p<1$. Notice the inequality reverses compared with the infinite-interval p-test.",
            "A classic trap: $\\int_{-1}^{1} x^{-2}\\,dx$. The antiderivative $-1/x$ looks like it gives $-2$, but $x=0$ is a Type 2 bomb. The integral diverges.",
            "Integrals such as $\\int_0^1 \\ln x\\,dx$ mix a Type 2 log spike with parts. The boundary term $x\\ln x\\to 0$ as $x\\to 0^+$, and the value is $-1$.",
            "On FRQs, draw a vertical dashed line at the singularity, write two limits, and only then combine. Readers look for that split.",
        ],
        "Series with $a_n\\sim n^{-p}$ inherit these p-tests through the integral test.",
        "Locate every point where the integrand is undefined. Split, take limits, do not pass FTC through a discontinuity.",
        _fig(
            plot(
                curves=[("#4f46e5", sample_curve(lambda x: 1 / math.sqrt(x) if x > 0 else 1e9, 0.04, 1.2, 70))],
                fills=[(shade_under(lambda x: 1 / math.sqrt(max(x, 1e-6)), 0.04, 1, 40), "#fde68a")],
                xlim=(-0.1, 1.3), ylim=(-0.2, 5.5),
                points=[(0, 0, "spike at 0")],
            ),
            "Type 2 spike $\\int_0^1 x^{-1/2}\\,dx=2$",
            "The graph shoots up at $x=0$, but the shaded area is finite. Contrast with $1/x$, whose spike has infinite area.",
        )
        + solved(16, "Evaluate $\\int_0^1 x^{-1/2}\\,dx$.",
                 ["$\\lim_{a\\to 0^+}[2x^{1/2}]_a^1=2-0=2$."],
                 "$2$", "p=1/2<1, so the spike is integrable.", "Easy")
        + solved(17, "Show $\\int_0^1 x^{-1}\\,dx$ diverges.",
                 ["$\\lim_{a\\to 0^+}[\\ln x]_a^1=0-\\lim_{a\\to 0^+}\\ln a=\\infty$."],
                 "diverges", "Same logarithm as Type 1, now at the origin.", "Medium")
        + solved(18, "Does $\\int_{-1}^{1} x^{-2}\\,dx$ converge?",
                 ["Split at $0$: $\\lim_{a\\to 0^-}[-1/x]_{-1}^{a}+\\lim_{b\\to 0^+}[-1/x]_b^{1}$.",
                  "Left piece: $-1/a-1\\to+\\infty$. Right piece: $-1-(-1/b)\\to+\\infty$.",
                  "Both sides diverge, so the integral diverges. The illegal FTC shot $[-1/x]_{-1}^{1}=-2$ is wrong."],
                 "diverges", "Never apply FTC across a vertical asymptote.", "Hard"),
        ("Using FTC on an interval that contains a vertical asymptote",
         "The fundamental theorem requires continuity on the closed interval (or at least integrability). A blow-up inside kills a naive evaluation."),
        ("Split interior singularities before taking limits",
         "One limit from the left and one from the right. If either fails, the original integral diverges."),
        [],
        26,
    )
    content = unit_shell(
        title, AUDIENCE, concepts, c1 + c2 + c3 + c4 + c5 + c6,
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
        stretch_note=STRETCH_LABEL,
    )
    return title, description, content, _u2_questions()


# ===========================================================================
# UNIT 3
# ===========================================================================

def _u3_questions():
    return pack([
        ("A repeated linear factor $(x-r)^2$ in the denominator requires which extra term?", "B/(x−r)^2",
         "Write $A/(x-r)+B/(x-r)^2$ (and other factors as usual).", ["A/(x−r) only", "Ax+B over (x-r)^2 only", "A ln|x-r|"]),
        ("$\\dfrac{1}{x^2(x+1)}= -\\dfrac{1}{x}+\\dfrac{1}{x^2}+\\dfrac{1}{x+1}$. The $1/x^2$ coefficient came from?",
         "substituting x=0 after clearing the denominator",
         "Clearing gives $1=Ax(x+1)+B(x+1)+Cx^2$; $x=0$ yields $B=1$.", ["cover-up at x=1", "degree comparison only", "LIATE"]),
        ("$\\int \\dfrac{1}{(x-1)^2}\\,dx$ equals?", "-1/(x−1)+C",
         "Power rule: $\\int (x-1)^{-2}dx=-(x-1)^{-1}+C$.", ["ln|x-1|+C", "1/(x-1)+C", "2(x-1)+C"]),
        ("$\\int_2^3 (x-1)^{-2}\\,dx$ equals?", "1/2",
         "$[-1/(x-1)]_2^3=-1/2-(-1)=1/2$.", ["1", "-1/2", "ln 2"]),
        ("After repeating factors are decomposed, $\\int B/(x-r)^2\\,dx$ is?", "-B/(x-r) + C",
         "It is a power, not a logarithm. Only the $A/(x-r)$ term logs.", ["B ln|x-r|", "B/(x-r)", "2B(x-r)"]),
        ("Tabular parts for $\\int x^2 e^{x}\\,dx$ differentiates $x^2$ how many times to $0$?", 3,
         "The polynomial degree is $2$, so three differentiations ($x^2\\to 2x\\to 2\\to 0$).", ["2", "1", "4"]),
        ("$\\int x^2 e^{x}\\,dx$ equals?", "e^x(x^2−2x+2)+C",
         "Tabular: $x^2 e^{x}-2x e^{x}+2 e^{x}+C$.", ["e^x x^2+C", "e^x(x^2+2x+2)+C", "2x e^x+C"]),
        ("$\\int_0^1 x^2 e^{x}\\,dx$ equals?", "e−2",
         "$e^{x}(x^2-2x+2)$ from $0$ to $1$ is $e-(2)=e-2$.", ["e", "2", "e-1"]),
        ("Tabular signs along the product diagonal alternate starting with?", "+",
         "First product is $+u v$, then $-u' V$, then $+u''\\mathcal{V}$, matching parts.", ["−", "always +", "random"]),
        ("Tabular parts is the right tool when $u$ is a ? and $dv$ repeats under integration.",
         "polynomial",
         "Exponential, sine, and cosine all repeat (or cycle) when integrated.", ["logarithm", "rational function", "absolute value"]),
        ("Arc length of $y=f(x)$ on $[a,b]$ is?", "∫_a^b √(1+(f'(x))^2) dx",
         "Pythagoras on $dx$ and $dy=f'(x)dx$.", ["∫ f(x) dx", "∫ |f'(x)| dx", "∫ 2π f √(1+(f')^2) dx"]),
        ("The graph $y=x$ on $[0,1]$ has arc length?", "√2",
         "$f'=1$, so $\\int_0^1\\sqrt{2}\\,dx=\\sqrt{2}$.", ["1", "2", "π/4"]),
        ("For $y=x^{3/2}$ on $[0,4]$, $1+(y')^2$ equals?", "1+9x/4",
         "$y'=(3/2)x^{1/2}$, square it to get $9x/4$.", ["1+3x/2", "1+9x^2/4", "9x/4"]),
        ("That arc length of $y=x^{3/2}$ on $[0,4]$ evaluates to?", "8/27 (10√10 − 1)",
         "$u=1+9x/4$, $x=0\\to 1$, $x=4\\to 10$, $\\dfrac{8}{27}(10^{3/2}-1)=\\dfrac{8}{27}(10\\sqrt{10}-1)$.",
         ["8", "10√10", "27/8"]),
        ("If a calculator FRQ asks for arc length of a messy $f$, you should?",
         "write the integrand √(1+(f')^2) and evaluate the definite integral numerically",
         "The setup point is the integrand and limits; the calculator may do the number.",
         ["skip the integral and use distance between endpoints", "use polar arc length", "use Euler's method"]),
        ("Surface of revolution of $y=f(x)\\geq 0$ about the x-axis is?", "2π ∫_a^b y √(1+(y')^2) dx",
         "Each band is a frustum with radius $y$ and slant $ds$.", ["π ∫ y^2 dx", "2π ∫ x ds", "∫ √(1+(y')^2) dx"]),
        ("Rotate $y=x$ on $[0,1]$ about the x-axis. Surface area?", "π√2",
         "$2\\pi\\int_0^1 x\\sqrt{2}\\,dx=\\pi\\sqrt{2}$.", ["π", "2π", "√2"]),
        ("Disk/washer volume uses $\\pi y^2 dx$, while surface area uses?", "2π y ds",
         "Volume is stacked disks; surface is the lateral skin.", ["π y dx", "2π y^2 ds", "y' dx"]),
        ("If you rotate about the y-axis instead, the radius is typically?", "x",
         "Distance to the y-axis is $|x|$. The slant is still $ds$.", ["y", "1", "y'"]),
        ("A cone of slant $\\ell$ and base radius $r$ has lateral area?", "π r ℓ",
         "This is the $2\\pi y ds$ formula in a single frustum.", ["π r^2", "2π r", "π r^2 ℓ"]),
        ("Trapezoid error bound uses $\\dfrac{(b-a)^3}{12n^2}\\max|f''|$. For $e^x$ on $[0,1]$ with $n=1$, a bound is?",
         "e/12",
         "$\\max|f''|=e$ on $[0,1]$, so $e/12$.", ["e/2", "1/12", "e"]),
        ("If $f''>0$ on $[a,b]$, the trapezoid rule compared with the integral?", "overestimates",
         "A convex graph lies above its chords, so trapezoids sit above the curve.",
         ["underestimates", "is exact", "cannot be compared"]),
        ("Simpson error involves the fourth derivative and $n^4$ in the denominator, so doubling $n$ multiplies the bound by about?",
         "1/16",
         "$(2n)^{-4}=n^{-4}/16$.", ["1/2", "1/4", "1/8"]),
        ("Midpoint vs trapezoid for concave up $f$: midpoint tends to?", "underestimate",
         "The tangent (midpoint rectangle interpretation) sits below a convex graph.",
         ["overestimate", "match trapezoid", "be undefined"]),
        ("An error bound is not the actual error; it is?", "a guaranteed ceiling on |true − approximation|",
         "The actual error can be much smaller. AP asks whether the bound is $<10^{-k}$.",
         ["the exact remainder term of Taylor", "always equal to the error", "a lower bound"]),
        ("$\\int x\\ln x\\,dx$ is parts, not partial fractions, because?", "it is not a rational function",
         "Logs are not polynomials over polynomials. Use $u=\\ln x$.", ["the degree is too high", "it is improper", "trig sub is required"]),
        ("$\\int \\dfrac{x}{x^2+1}\\,dx$ is best done by?", "u = x^2+1 (ordinary substitution)",
         "The numerator is a multiple of the denominator's derivative. Partial fractions over $x^2+1$ would work but is slower.",
         ["trig sub immediately", "parts with u=x", "tabular"]),
        ("$\\int \\dfrac{1}{x^2\\sqrt{x^2-1}}\\,dx$ suggests?", "trig sub x = sec θ",
         "The $\\sqrt{x^2-1}$ fingerprint is $x=a\\sec\\theta$.", ["parts", "partial fractions linear", "u=x^2"]),
        ("$\\int e^{x}\\sin x\\,dx$ is?", "cyclic parts (twice), then solve for the integral",
         "Neither factor dies. Two parts returns the original.", ["a p-integral", "geometric series", "Simpson only"]),
        ("$\\int_0^1 \\dfrac{1}{\\sqrt{x}}\\,dx$ is improper, so before Simpson you must?",
         "handle the Type 2 limit (or a substitution) rather than sampling x=0 blindly",
         "A numerical rule that evaluates $f(0)$ is undefined. AP expects the improper limit first.",
         ["use n=2 anyway", "switch to polar area", "declare it 0"]),
        ("Repeating factor $(x+2)^3$ needs how many terms in $x+2$?", 3,
         "$A/(x+2)+B/(x+2)^2+C/(x+2)^3$.", ["1", "2", "4"]),
        ("$\\int x^3 e^{-x}\\,dx$ by tabular uses how many nonzero polynomial rows before $0$?", 4,
         "Degree $3$ produces four differentiated rows plus the zero row.", ["3", "1", "x"]),
        ("Arc length of $y=\\ln(\\cos x)$ on $[0,\\pi/4]$ equals?", "ln(√2 + 1)",
         "$y'=-\\tan x$, $1+(y')^2=\\sec^2 x$, integrand $\\sec x$ on $[0,\\pi/4]$. Antiderivative $\\ln|\\sec x+\\tan x|$ from $0$ to $\\pi/4$ is $\\ln(\\sqrt{2}+1)$.",
         ["π/4", "1", "ln 2"]),
        ("Rotate $y=\\sqrt{x}$ on $[0,1]$ about the x-axis. The surface integrand is?",
         "2π √x √(1+1/(4x))",
         "$y'=1/(2\\sqrt{x})$, so $1+(y')^2=1+1/(4x)$, times $2\\pi y$.",
         ["π x", "2π x √(1+4x)", "√x"]),
        ("Trapezoid with $n=2$ on $[0,2]$ has $\\Delta x=$ ?", 1,
         "$(b-a)/n=2/2=1$.", ["2", "1/2", "4"]),
        ("Simpson's rule requires $n$ to be?", "even",
         "Parabolas are fitted on pairs of subintervals.", ["odd", "a multiple of 4", "prime"]),
        ("$\\int \\dfrac{3x+1}{(x-1)(x-1)(x+2)}\\,dx$ needs a repeating template because?",
         "(x−1) appears twice",
         "Write $A/(x-1)+B/(x-1)^2+C/(x+2)$.", ["the numerator is linear", "x+2 is linear", "it is improper"]),
        ("A method-choice tell for $\\int x^5\\cos x\\,dx$ is?", "tabular parts",
         "High-degree polynomial times sine/cosine/exponential.", ["partial fractions", "trig sub √(a^2−x^2)", "p-test"]),
        ("Arc length $L$ compared with the chord between endpoints satisfies?",
         "L ≥ √((Δx)^2+(Δy)^2)",
         "A curve is at least as long as the straight segment joining its ends.",
         ["L is always 0", "L = |Δy|", "L ≤ |Δx|"]),
        ("Surface area about the x-axis uses radius?", "|y|",
         "Radius is a distance. Use $|f(x)|$ if the graph dips below the axis.", ["y'", "x only", "f''(x)"]),
        ("If $|E_T|\\leq 0.02$ is required and the formula gives $K/n^2$, you need $n$ at least?",
         "the smallest integer n with K/n^2 ≤ 0.02",
         "Solve the inequality, then round up to an integer (and to an even $n$ if you switch to Simpson).",
         ["K", "0.02", "2K"]),
        ("$\\int \\dfrac{dx}{x^2-2x+1}$ is repeating PF because $x^2-2x+1=$ ?", "(x−1)^2",
         "Then $\\int (x-1)^{-2}dx=-1/(x-1)+C$.", ["(x+1)^2", "x(x-2)", "irreducible"]),
        ("$\\int_0^{\\pi/2} x\\cos x\\,dx$ (parts) equals?", "π/2 − 1",
         "$u=x$, $dv=\\cos x dx$: $[x\\sin x]_0^{\\pi/2}-\\int\\sin x=\\pi/2-1$.", ["1", "π/2", "0"]),
        ("Numeric integration error ideas do not replace?", "the definition of a definite integral as a limit of sums",
         "Bounds tell you how close a particular $n$ is; they are not a new definition of area.",
         ["the trapezoid formula", "Simpson's formula", "max|f''|"]),
        ("Pick a method: $\\int \\dfrac{x^2+1}{x(x-1)}\\,dx$ first step is?", "polynomial division, then nonrepeating PF",
         "Numerator degree is not smaller than denominator degree $2$.", ["trig sub", "tabular", "Type 1 limit"]),
        ("Pick a method: $\\int \\sqrt{9-x^2}\\,dx$ is?", "trig sub x=3 sin θ (circle)",
         "The radicand is $a^2-x^2$.", ["parts u=√(9-x^2)", "PF", "geometric series"]),
        ("AP Stretch: $\\dfrac{x+3}{x^2(x+1)}=\\dfrac{A}{x}+\\dfrac{B}{x^2}+\\dfrac{C}{x+1}$. Then $B$ equals?", 3,
         "Clear: $x+3=A x(x+1)+B(x+1)+C x^2$. Set $x=0$: $3=B$.", ["1", "0", "-3"]),
        ("AP Stretch: $\\int_0^{\\pi} x^2\\cos x\\,dx$ by tabular equals?", "-2π",
         "Antiderivative $x^2\\sin x+2x\\cos x-2\\sin x$. From $0$ to $\\pi$: $(0+2\\pi(-1)-0)-(0)= -2\\pi$.",
         ["0", "π^2", "4"]),
        ("AP Stretch: Arc length of $y=\\dfrac{x^3}{6}+\\dfrac{1}{2x}$ from $1$ to $2$ equals?", "17/12",
         "$y'=x^2/2-1/(2x^2)$ and $1+(y')^2=(x^2/2+1/(2x^2))^2$, so the integrand is $x^2/2+1/(2x^2)$. "
         "$[x^3/6-1/(2x)]_1^2=17/12$.", ["2", "1", "7/6"]),
        ("AP Stretch: Surface of $y=x^3$ on $[0,1]$ about the x-axis equals?", "π/27 (10√10 − 1)",
         "$S=2\\pi\\int_0^1 x^3\\sqrt{1+9x^4}dx$. Let $u=1+9x^4$, $du=36 x^3 dx$, from $1$ to $10$: "
         "$(2\\pi/36)\\cdot(2/3)(10^{3/2}-1)=\\pi/27(10\\sqrt{10}-1)$.",
         ["π/3", "2π", "π"]),
        ("AP Stretch: For $f(x)=e^{x}$ on $[0,2]$, trapezoid $n=4$. A bound using $\\max|f''|=e^2$ is?", "e^2/24",
         "$(2)^3/(12\\cdot 16)\\cdot e^2=8e^2/192=e^2/24$.", ["e^2/12", "e^2/4", "2e^2"]),
        ("AP Stretch: How large must $n$ be so the trap bound for $e^{x}$ on $[0,1]$ is $<10^{-4}$? Use $\\max|f''|=e$.",
         "n ≥ 48",
         "$e/(12n^2)<10^{-4}\\Rightarrow n^2>e/(12\\cdot 10^{-4})\\approx 2264$, so $n\\geq 48$.",
         ["n ≥ 10", "n ≥ 4", "n ≥ 100"]),
        ("AP Stretch: $\\int_0^1 x^3\\sqrt{1-x^2}\\,dx$ is best started with?", "x = sin θ, then a power of cosine",
         "The $\\sqrt{1-x^2}$ is a sine substitution; after $dx$ and the radical, an odd cosine power remains.",
         ["repeating PF", "tabular with u=√(1-x^2)", "Type 1 comparison"]),
        ("AP Stretch: A method map for $\\int \\dfrac{x^2}{(x-1)^2(x+2)}\\,dx$ begins with?",
         "A/(x−1)+B/(x−1)^2+C/(x+2) (already proper)",
         "Degree 2 over degree 3 is proper. Repeating linear factor $(x-1)^2$ plus one other linear.",
         ["x=tan θ", "∫u dv with u=x^2", "integral test"]),
        ("AP Stretch: Simpson with $n=2$ for $\\int_0^{\\pi}\\sin x\\,dx$ equals?", "2π/3",
         "$h=\\pi/2$. $S=(\\pi/6)(\\sin 0+4\\sin(\\pi/2)+\\sin\\pi)=(\\pi/6)(4)=2\\pi/3$. True value $2$.",
         ["2", "π", "4"]),
    ])


def build_unit3():
    title = "AP Calculus BC Unit 3: More Integration & Arc Length"
    description = (
        "Repeating partial fractions, tabular integration by parts, arc length of y=f(x), "
        "surfaces of revolution, numeric integration error, and choosing a method."
    )
    concepts = [
        "Partial fractions with repeating linear factors",
        "Tabular integration by parts",
        "Arc length of y=f(x)",
        "Surface of revolution (intro)",
        "Numeric integration error idea",
        "Strategy: pick a method",
    ]
    c1 = concept_block(
        "1. Partial fractions with repeating linear factors",
        [
            "If $(x-r)^m$ divides the denominator, you need $m$ terms: $\\dfrac{A_1}{x-r}+\\dfrac{A_2}{(x-r)^2}+\\cdots+\\dfrac{A_m}{(x-r)^m}$. "
            "The highest power is not optional; dropping it leaves an identity that cannot fit the numerator.",
            "Clear the denominator. Powers $(x-r)^k$ with $k\\geq 2$ integrate by the power rule, not by logarithms. Only the first-power term $A/(x-r)$ produces $\\ln|x-r|$.",
            "Cover-up still finds the coefficient of the highest power: drop $(x-r)^m$ and evaluate at $x=r$. Lower-power coefficients need extra $x$-values or matching like powers.",
            "A squared factor $(x-1)^2$ is the AP favorite. Students who write only $A/(x-1)+B/(x+2)$ are one term short and will fail the multiply-back check.",
            "If an irreducible quadratic repeats — rare on BC — you would write linear numerators over each power. This course keeps repeating linears, which already appear on FRQs.",
            "After integrating, combine logs and leave the power-rule terms as rational functions. That mixed form is the expected simplified answer.",
        ],
        "Repeating factors show up whenever a characteristic equation has a double root, and in rational practice integrals throughout BC.",
        "Count the multiplicity, write that many terms, clear, solve, integrate powers and logs separately.",
        _fig(
            plot(
                curves=[("#4f46e5", sample_curve(lambda x: 1 / ((x - 1) ** 2), 1.25, 4, 60))],
                fills=[(shade_under(lambda x: 1 / ((x - 1) ** 2), 2, 3, 30), "#bbf7d0")],
                xlim=(0.5, 4.2), ylim=(-0.2, 4.2),
                dashes=[("v", 1, "x=1")],
            ),
            "$y=1/(x-1)^2$ with $\\int_2^3$ shaded",
            "The vertical asymptote is a Type 2 issue only if you integrate across $x=1$. On $[2,3]$ the integral is an ordinary $1/2$.",
        )
        + solved(1, "Decompose $\\dfrac{1}{x^2(x+1)}$.",
                 ["$\\dfrac{A}{x}+\\dfrac{B}{x^2}+\\dfrac{C}{x+1}$.",
                  "Clear: $1=Ax(x+1)+B(x+1)+Cx^2$. $x=0\\Rightarrow B=1$. $x=-1\\Rightarrow C=1$.",
                  "Then $A=-1$. So $-1/x+1/x^2+1/(x+1)$."],
                 "$-1/x+1/x^2+1/(x+1)$", "Multiply back to confirm the numerator is $1$.", "Easy")
        + solved(2, "Evaluate $\\int_2^3(x-1)^{-2}\\,dx$.",
                 ["Antiderivative $-1/(x-1)$.",
                  "$-1/2-(-1)=1/2$."],
                 "$1/2$", "No logarithm appears because the power is $-2$, not $-1$.", "Medium")
        + solved(3, "Find $B$ in $\\dfrac{x+3}{x^2(x+1)}=\\dfrac{A}{x}+\\dfrac{B}{x^2}+\\dfrac{C}{x+1}$.",
                 ["Clear: $x+3=Ax(x+1)+B(x+1)+Cx^2$.",
                  "Set $x=0$: $3=B$."],
                 "$B=3$", "Highest-power coefficients are the easy cover-up values.", "Hard"),
        ("Logging a squared factor",
         "∫ 1/(x-r)^2 dx is not ln. Differentiating ln|x-r| produces 1/(x-r), one power too low."),
        ("Write every required power before solving",
         "If multiplicity is 3, you need three undetermined coefficients in that family. Missing one makes the algebra inconsistent."),
        [],
        1,
    )
    c2 = concept_block(
        "2. Tabular integration by parts",
        [
            "When $u$ is a polynomial of degree $n$ and $dv$ is exponential or sine/cosine, parts is needed $n$ times. Tabular organizes those $n$ steps in two columns: differentiate $u$ down to $0$, integrate $dv$ the same number of times.",
            "Alternate signs $+\\ -+\\ -$ along the diagonals as you multiply across. The first sign is $+$, matching $\\int u\\,dv=uv-\\int v\\,du$.",
            "Stop when the derivative column hits $0$. The last product is a constant times the $n$-fold integral of $dv$, with the appropriate sign.",
            "Definite tabular parts: form the antiderivative and then evaluate at the bounds. Attaching limits to every product is more error-prone.",
            "Cyclic integrands $e^{ax}\\sin bx$ do not die. After two rows you solve for the original integral, just as in ordinary cyclic parts.",
            "Write at least one ordinary parts line in the margin the first time you use the table, so a reader can see you know the theorem, not just a trick.",
        ],
        "Tabular is how BC handles $\\int x^n e^{ax}\\,dx$ and $\\int x^n\\sin bx\\,dx$ without losing signs.",
        "Polynomial on the left, repeating antiderivative on the right, alternating signs, multiply diagonals.",
        _fig(
            plot(
                curves=[("#4f46e5", sample_curve(lambda x: (x ** 2) * math.exp(x), -2, 1.2, 70))],
                fills=[(shade_under(lambda x: (x ** 2) * math.exp(x), 0, 1, 25), "#c7d2fe")],
                xlim=(-2.2, 1.4), ylim=(-0.5, 4.2),
            ),
            "$y=x^2 e^{x}$ with $\\int_0^1$ shaded",
            "Tabular parts evaluates the shaded area as $e-2$. The same table produces the indefinite antiderivative $e^{x}(x^2-2x+2)$.",
        )
        + solved(4, "Find $\\int x^2 e^{x}\\,dx$ by a table.",
                 ["Differentiate $x^2,2x,2,0$. Integrate $e^{x}$ four times (same function).",
                  "Products: $+x^2 e^{x}-2x e^{x}+2 e^{x}$.",
                  "Factor $e^{x}(x^2-2x+2)+C$."],
                 "$e^{x}(x^2-2x+2)+C$", "Differentiate to check: product rule recovers $x^2 e^{x}$.", "Easy")
        + solved(5, "Evaluate $\\int_0^1 x^2 e^{x}\\,dx$.",
                 ["Use the antiderivative from the previous example.",
                  "At $1$: $e(1-2+2)=e$. At $0$: $1(2)=2$. Difference $e-2$."],
                 "$e-2$", "Forgetting the $t=0$ term $2$ is the usual miss.", "Medium")
        + solved(6, "Evaluate $\\int_0^{\\pi} x^2\\cos x\\,dx$.",
                 ["Table: $x^2,2x,2$ against $\\cos x,\\sin x,-\\cos x,-\\sin x$.",
                  "Antiderivative $x^2\\sin x+2x\\cos x-2\\sin x$.",
                  "From $0$ to $\\pi$: $-2\\pi$."],
                 "$-2\\pi$", "Sine vanishes at both $0$ and $\\pi$; only the $2x\\cos x$ term survives.", "Hard"),
        ("Starting the sign column with a minus",
         "The first diagonal is +uv. A flipped sign column corrupts every later term."),
        ("Stop when the derivative hits zero, not one row earlier",
         "The constant derivative still multiplies a remaining integral of dv. Dropping it loses the lowest-degree term."),
        [],
        6,
    )
    c3 = concept_block(
        "3. Arc length of y=f(x)",
        [
            "If $y=f(x)$ is continuously differentiable on $[a,b]$, the arc length is $L=\\int_a^b\\sqrt{1+(f'(x))^2}\\,dx$. This is the parametric formula with $x=t$, $y=f(t)$.",
            "The integrand is always at least $1$, so $L\\geq b-a$. Compared with the chord, $L\\geq\\sqrt{(b-a)^2+(f(b)-f(a))^2}$.",
            "Some AP integrands are perfect squares. If $1+(f')^2=(g(x))^2$, the square root disappears. Hunt for that before you surrender to a calculator.",
            "If $x=g(y)$ is easier, switch: $L=\\int\\sqrt{1+(dx/dy)^2}\\,dy$. Circles and sideways parabolas often prefer $y$ as the parameter.",
            "Calculator FRQs still require the correct integrand on paper. A naked decimal with no integral is incomplete.",
            "Do not confuse this formula with polar arc length $\\int\\sqrt{r^2+(r')^2}\\,d\\theta$ (Unit 7) or with surface area $2\\pi y ds$ (next lesson).",
        ],
        "Arc length is the geometric meaning of integrating speed along a graph treated as a path.",
        "Compute f', form 1+(f')^2, simplify the radicand, then integrate or use the calculator.",
        _fig(
            plot(
                curves=[("#4f46e5", sample_curve(lambda x: x, 0, 1, 20))],
                points=[(0, 0, "(0,0)"), (1, 1, "(1,1)")],
                xlim=(-0.3, 1.4), ylim=(-0.3, 1.4),
            ),
            "The segment $y=x$ on $[0,1]$ has length $\\sqrt{2}$",
            "Here $f'=1$, so $\\sqrt{1+1}=\\sqrt{2}$. The formula matches the Pythagorean theorem on the right triangle with legs $1$ and $1$.",
        )
        + solved(7, "Find the arc length of $y=x$ on $[0,1]$.",
                 ["$f'=1$, integrand $\\sqrt{2}$.",
                  "$L=\\sqrt{2}$."],
                 "$\\sqrt{2}$", "Geometry confirms.", "Easy")
        + solved(8, "Set up and evaluate arc length of $y=x^{3/2}$ on $[0,4]$.",
                 ["$y'=(3/2)x^{1/2}$, $1+(y')^2=1+9x/4$.",
                  "$u=1+9x/4$, $du=(9/4)dx$, $x=0\\to u=1$, $x=4\\to u=10$.",
                  "$L=\\dfrac{8}{27}(10\\sqrt{10}-1)$."],
                 "$\\dfrac{8}{27}(10\\sqrt{10}-1)$", "The $8/27$ comes from $(4/9)\\cdot(2/3)$.", "Medium")
        + solved(9, "Arc length of $y=\\ln(\\cos x)$ on $[0,\\pi/4]$.",
                 ["$y'=-\\tan x$, $1+\\tan^2 x=\\sec^2 x$.",
                  "Integrand $\\sec x$ on $[0,\\pi/4]$.",
                  "$\\ln|\\sec x+\\tan x|$ from $0$ to $\\pi/4=\\ln(\\sqrt{2}+1)$."],
                 "$\\ln(\\sqrt{2}+1)$", "This is a standard secant integral.", "Hard"),
        ("Using only |Δy| or the displacement",
         "Arc length is not the rise. A wiggle can be long while the net change in y is small."),
        ("Simplify 1+(f')^2 before integrating",
         "Perfect-square radicands are planted on purpose. Expanding and staring at a mess is how you miss them."),
        [],
        11,
    )
    c4 = concept_block(
        "4. Surface of revolution (intro)",
        [
            "Rotating $y=f(x)\\geq 0$ about the $x$-axis sweeps a surface whose area is $S=2\\pi\\int_a^b y\\,ds=2\\pi\\int_a^b y\\sqrt{1+(y')^2}\\,dx$. Each slice is a thin band of radius $y$ and width $ds$.",
            "This is not the disk volume $\\pi\\int y^2 dx$. Volume fills the interior; surface area paints the skin. Mixing the formulas is an instant zero on that part.",
            "About the $y$-axis, the radius is $|x|$, so $S=2\\pi\\int |x|\\,ds$. Choose $dx$ or $dy$ according to which description of the curve is cleaner.",
            "A cone is the special case $y=rx/h$ on $[0,h]$: $S=\\pi r\\ell$ with slant $\\ell=\\sqrt{r^2+h^2}$. If your general formula cannot reproduce that, the setup is wrong.",
            "As with arc length, $1+(y')^2$ may be a perfect square. The extra factor of $y$ (or $x$) then makes a substitution $u=1+k x^n$ natural.",
            "AP BC includes this formula in the curriculum; it is less common than volume but appears as a calculator setup or a short exact evaluation.",
        ],
        "Surface area is arc length with a $2\\pi$ radius weight — the same $ds$ you just learned.",
        "Write 2π ∫ (radius) ds, identify radius as distance to the axis, and use the matching ds.",
        _fig(
            svg_parabola(0, 0, 4),
            "A parabolic profile $y=x^2$ ready to rotate about the x-axis",
            "Each band has radius equal to the $y$-value and slant $ds=\\sqrt{1+(2x)^2}dx$. Volume would have used $\\pi y^2$ instead.",
        )
        + solved(10, "Rotate $y=x$ on $[0,1]$ about the x-axis. Find $S$.",
                 ["Radius $x$, $ds=\\sqrt{2} dx$.",
                  "$S=2\\pi\\int_0^1 x\\sqrt{2}\\,dx=\\pi\\sqrt{2}$."],
                 "$\\pi\\sqrt{2}$", "A cone with $r=1$, $h=1$, $\\ell=\\sqrt{2}$ has lateral area $\\pi\\sqrt{2}$.", "Easy")
        + solved(11, "Set up $S$ for $y=\\sqrt{x}$ on $[0,1]$ about the x-axis.",
                 ["$y'=1/(2\\sqrt{x})$, $1+(y')^2=1+1/(4x)$.",
                  "$S=2\\pi\\int_0^1 \\sqrt{x}\\sqrt{1+1/(4x)}\\,dx=2\\pi\\int_0^1 \\sqrt{x+1/4}\\,dx$ after algebra.",
                  "The unsimplified form looks Type 2 at $x=0$; the simplified integrand is continuous."],
                 r"$2\pi\int_0^1\sqrt{x+1/4}\,dx$", "Simplify under the radical before you panic about $x=0$.", "Medium")
        + solved(12, "Rotate $y=x^3$ on $[0,1]$ about the x-axis. Evaluate $S$.",
                 ["$S=2\\pi\\int_0^1 x^3\\sqrt{1+9x^4}\\,dx$.",
                  "$u=1+9x^4$, $du=36 x^3 dx$, $x=0\\to 1$, $x=1\\to 10$.",
                  "$S=\\dfrac{\\pi}{27}(10\\sqrt{10}-1)$."],
                 r"$\dfrac{\pi}{27}(10\sqrt{10}-1)$", "The $x^3 dx$ is exactly what the substitution wants.", "Hard"),
        ("Using π∫ y^2 dx for surface area",
         "That is volume (disks). Surface area has a 2π y ds structure."),
        ("Radius is distance to the axis",
         "About the x-axis, radius is |y|. About the y-axis, radius is |x|. Mixing them is a picture error."),
        [],
        16,
    )
    c5 = concept_block(
        "5. Numeric integration error idea",
        [
            "Trapezoid, midpoint, and Simpson are Riemann-sum cousins with known error bounds. AP wants you to decide whether an approximation is guaranteed to be within $10^{-k}$ of the truth.",
            "Trapezoid: $|E_T|\\leq \\dfrac{(b-a)^3}{12n^2}\\max|f''|$. Midpoint is half of that (with a sign flip). Simpson: $|E_S|\\leq \\dfrac{(b-a)^5}{180 n^4}\\max|f^{(4)}|$ with $n$ even.",
            "These are bounds, not the error itself. A bound of $0.02$ means the true error is at most $0.02$; it might be $0.0001$.",
            "Convexity: if $f''>0$, trapezoids overestimate and midpoints underestimate. That picture is enough for a no-calculator true/false.",
            "To force a bound below a tolerance, solve for $n$ and round up. For Simpson, round up to the next even integer.",
            "Never apply a rule that samples a point where $f$ is undefined (Type 2). Handle the improper integral first, then approximate a nearby proper integral if needed.",
        ],
        "Error bounds are how BC justifies a calculator value or a hand trapezoid on an FRQ justification line.",
        "Identify the rule, plug max|derivative| on [a,b], solve for n, round up.",
        _fig(
            plot(
                curves=[("#4f46e5", sample_curve(math.exp, 0, 1.4, 40))],
                points=[(0, 1, "A"), (1, math.e, "B")],
                xlim=(-0.2, 1.6), ylim=(-0.2, 3.2),
            ),
            "$y=e^{x}$ is convex, so the chord (trapezoid) lies above the graph",
            "On $[0,1]$ the single trapezoid has area $(1+e)/2\\approx 1.859$, larger than $\\int_0^1 e^{x}dx=e-1\\approx 1.718$. The bound $e/12$ covers the gap.",
        )
        + solved(13, "Bound $|E_T|$ for $e^{x}$ on $[0,1]$ with $n=1$.",
                 ["$f''=e^{x}$, $\\max=e$.",
                  "$(1)^3 e/(12\\cdot 1)=e/12$."],
                 "$e/12$", "Actual error is about $0.14$, and $e/12\\approx 0.23$ is a valid ceiling.", "Easy")
        + solved(14, "If $f''>0$, does trapezoid over- or under-estimate?",
                 ["The graph lies above its chords.",
                  "Trapezoids (chords) sit above the curve, so they overestimate the integral."],
                 "overestimate", "Midpoint goes the other way.", "Medium")
        + solved(15, "How large must $n$ be so the trap bound for $e^{x}$ on $[0,1]$ is $<10^{-4}$?",
                 ["$e/(12n^2)<10^{-4}$.",
                  "$n^2>e/(0.0012)\\approx 2265$, so $n\\geq 48$."],
                 "$n\\geq 48$", "Always round up; $n=47$ still misses the inequality.", "Hard"),
        ("Treating the bound as the exact error",
         "A bound of 0.05 does not mean you are 0.05 off. It means you are no more than 0.05 off."),
        ("Forgetting to round n up (and to even, for Simpson)",
         "n must be an integer. A computed 17.2 becomes 18, and Simpson would need 18 rather than 17."),
        [],
        21,
    )
    c6 = concept_block(
        "6. Strategy: pick a method",
        [
            "Before integrating, name the family: rational (divide / partial fractions), polynomial times sine/exponential (tabular parts), log or inverse trig (parts with $u=$ that factor), "
            "Pythagorean radical (trig sub), odd/even trig powers (identities), improper (limits), or a derivative-in-the-numerator gift ($u$-sub).",
            "A flowchart: (1) Is a factor the derivative of another? $u$-sub. (2) Rational? Divide if needed, then PF. (3) $\\sqrt{a^2\\pm x^2}$ or $\\sqrt{x^2-a^2}$? Trig sub. "
            "(4) $x^n e^{ax}$ or $x^n\\sin bx$? Tabular. (5) Infinite bound or vertical asymptote? Limits.",
            "Do not start two methods at once. Pick, write the first substitution line, and commit for at least three lines before switching.",
            "Mixed FRQs stack methods: PF then an improper limit; parts then an arc-length radicand; a numeric bound after an unintegrable setup.",
            "If two methods both work, choose the one with fewer minus signs. $u$-sub beats PF when the numerator is a multiple of the denominator's derivative.",
            "Calculator sections still want the method named. 'I integrated on the calculator' without an integrand earns nothing.",
        ],
        "Method choice is the difference between a two-minute integral and a dead end on BC Paper 1.",
        "Classify first in the margin: u-sub / PF / parts / trig / improper / numeric. Then execute.",
        _fig(
            plot(
                curves=[
                    ("#4f46e5", sample_curve(lambda x: math.sqrt(max(9 - x * x, 0)), -3, 3, 80)),
                    ("#059669", sample_curve(lambda x: x * math.exp(-x), 0, 5, 60)),
                ],
                xlim=(-3.4, 5.2), ylim=(-0.4, 3.4),
            ),
            "Two integrands, two methods: $\\sqrt{9-x^2}$ (trig sub) vs $x e^{-x}$ (parts)",
            "The semicircle screams $x=3\\sin\\theta$. The hump $x e^{-x}$ screams $u=x$, $dv=e^{-x}dx$. Matching the picture to the method is the whole lesson.",
        )
        + solved(16, "Choose a method for $\\int\\dfrac{x}{x^2+1}\\,dx$.",
                 ["Numerator is a multiple of the derivative of the denominator.",
                  "$u=x^2+1$, $du=2x dx$, answer $\\dfrac{1}{2}\\ln(x^2+1)+C$."],
                 "ordinary $u$-sub (not PF)", "PF over $x^2+1$ works but wastes time.", "Easy")
        + solved(17, "Choose a method for $\\int\\sqrt{9-x^2}\\,dx$.",
                 ["Radicand $a^2-x^2$ with $a=3$.",
                  "$x=3\\sin\\theta$ (circle)."],
                 "trig sub $x=3\\sin\\theta$", "This is also a circle-area geometry problem.", "Medium")
        + solved(18, "Outline $\\int\\dfrac{x^2}{(x-1)^2(x+2)}\\,dx$.",
                 ["Proper rational (deg 2 over deg 3).",
                  "Repeating linear $(x-1)^2$ plus $(x+2)$: $A/(x-1)+B/(x-1)^2+C/(x+2)$.",
                  "Integrate logs and a power."],
                 "repeating partial fractions", "No trig sub, no parts.", "Hard"),
        ("Launching partial fractions on a non-rational integrand",
         "Logs, radicals, and exponentials are not PF. Name the actual family first."),
        ("Write the method name before the first equals sign",
         "That one word — parts, trig sub, PF — keeps you from mixing templates mid-stream."),
        [],
        26,
    )
    content = unit_shell(
        title, AUDIENCE, concepts, c1 + c2 + c3 + c4 + c5 + c6,
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
        stretch_note=STRETCH_LABEL,
    )
    return title, description, content, _u3_questions()


# ===========================================================================
# UNIT 4
# ===========================================================================

def _u4_questions():
    return pack([
        ("The sequence $a_n=n/(n+1)$ has limit?", 1,
         "Divide by $n$: $1/(1+1/n)\\to 1$.", ["0", "∞", "1/2"]),
        ("$a_n=(1+1/n)^n$ converges to?", "e",
         "This is the definition of $e$ as a sequential limit.", ["1", "0", "π"]),
        ("If $a_n\\to L$ and $b_n\\to M$, then $a_n+b_n$ converges to?", "L+M",
         "Algebra of sequential limits.", ["LM", "L/M", "does not exist"]),
        ("The sequence $a_n=(-1)^n$ does what?", "diverges (oscillates)",
         "Two subsequences, even to $1$ and odd to $-1$, disagree.", ["converges to 0", "converges to 1", "converges to −1"]),
        ("A convergent sequence is eventually?", "bounded",
         "If $a_n\\to L$, tail terms sit in $(L-1,L+1)$, hence bounded.", ["unbounded", "monotone", "geometric"]),
        ("A geometric series $\\sum r^n$ from $n=0$ to $\\infty$ converges when?", "|r| < 1",
         "The partial sums $s_n=(1-r^{n+1})/(1-r)$ settle iff $|r|<1$.", ["r > 1", "|r| ≤ 1", "r = 1"]),
        ("$\\sum_{n=0}^{\\infty}(1/2)^n$ equals?", 2,
         "$a/(1-r)=1/(1-1/2)=2$.", ["1", "1/2", "∞"]),
        ("$\\sum_{n=1}^{\\infty}(1/3)^n$ equals?", "1/2",
         "First term $1/3$, ratio $1/3$: $(1/3)/(1-1/3)=1/2$.", ["3/2", "1/3", "1"]),
        ("$\\sum_{n=0}^{\\infty} 3(2/5)^n$ equals?", 5,
         "$3/(1-2/5)=3/(3/5)=5$.", ["3", "2/5", "15/2"]),
        ("If $|r|\\geq 1$, the geometric series?", "diverges",
         "Terms do not go to $0$ (or, for $r=-1$, they oscillate).", ["converges to 1", "converges to r", "converges conditionally"]),
        ("The nth-term (divergence) test says: if $a_n\\not\\to 0$, then $\\sum a_n$ ?", "diverges",
         "Necessary condition for convergence is $a_n\\to 0$.", ["converges", "converges absolutely", "is geometric"]),
        ("$a_n=n/(n+1)\\to 1\\neq 0$, so $\\sum n/(n+1)$ ?", "diverges",
         "Nth-term test applies immediately.", ["converges to 1", "converges by AST", "is p-series"]),
        ("The converse of the nth-term test is?", "false: a_n→0 does not imply convergence",
         "Harmonic $1/n\\to 0$ yet $\\sum 1/n$ diverges.", ["true", "true for geometric only", "true for p-series"]),
        ("$\\sum \\cos n$ diverges because?", "cos n does not tend to 0",
         "The sequence $\\cos n$ is dense on $[-1,1]$ and has no limit $0$.", ["it is geometric with r=1", "integral test", "AST"]),
        ("If $\\sum a_n$ converges, then $a_n$ must?", "tend to 0",
         "This is the necessary condition, not a sufficient test for convergence.", ["be positive", "be geometric", "satisfy AST"]),
        ("The integral test compares $\\sum_{n=N}^{\\infty} a_n$ with?", "∫_N^∞ f(x) dx for a positive decreasing f with f(n)=a_n",
         "Both converge or both diverge together.", ["the geometric series with r=a_1", "n!", "Taylor remainder"]),
        ("$\\sum 1/n^p$ converges when?", "p > 1",
         "The integral $\\int_1^{\\infty} x^{-p}dx$ converges iff $p>1$.", ["p ≥ 1", "p < 1", "p > 0"]),
        ("$\\sum 1/(n\\ln n)$ from $n=2$ does what?", "diverges",
         "$\\int dx/(x\\ln x)=\\ln(\\ln x)\\to\\infty$.", ["converges (p=1)", "converges by AST", "equals 1"]),
        ("For the integral test, $f$ must be eventually?", "positive, continuous, and decreasing",
         "Without monotonicity the picture of rectangles vs area can fail.", ["odd", "alternating", "polynomial"]),
        ("$\\sum 1/n^2$ converges because it is a p-series with?", "p = 2 > 1",
         "This is the Basel series; AP only needs the p-test, not the exact sum $\\pi^2/6$.", ["p = 1", "p = 0", "p = 1/2"]),
        ("Direct comparison: $0\\leq a_n\\leq b_n$ and $\\sum b_n$ converges implies?", "∑ a_n converges",
         "A smaller nonnegative series cannot diverge if the larger one converges.", ["∑ a_n diverges", "a_n → 1", "AST applies"]),
        ("Limit comparison: if $a_n,b_n>0$ and $\\lim a_n/b_n=L\\in(0,\\infty)$, then?",
         "∑ a_n and ∑ b_n both converge or both diverge",
         "The tails are asymptotic multiples of each other.", ["only ∑ a_n converges", "L must be 0", "they become geometric"]),
        ("$\\sum 1/(n^2+n)$ converges by limit comparison with?", "1/n^2",
         "$\\dfrac{1/(n^2+n)}{1/n^2}\\to 1$.", ["1/n", "1/n^3", "n"]),
        ("$\\sum 1/(n+1)$ diverges by comparison with?", "the harmonic series (or limit comparison with 1/n)",
         "It is a shift of $\\sum 1/n$.", ["1/n^2", "geometric r=1/2", "e^{-n}"]),
        ("You may not compare $\\sum (-1)^n/n$ directly with $1/n$ to conclude divergence because?",
         "direct comparison requires nonnegative terms",
         "Alternating series need AST or absolute-convergence tests, not a naive comparison with the harmonic series.",
         ["the terms go to 0", "p=1 is allowed", "it is geometric"]),
        ("AST requires $a_n$ positive, decreasing to $0$. Then $\\sum (-1)^{n+1} a_n$ ?", "converges (possibly only conditionally)",
         "Leibniz's test. Absolute convergence is a separate question.", ["diverges", "equals a_1", "is geometric"]),
        ("The AST remainder after $n$ terms satisfies $|R_n|\\leq$ ?", "a_{n+1}",
         "The error is at most the first omitted term, and has the sign of that term.", ["a_n", "1/n", "the integral remainder"]),
        ("For $\\sum (-1)^{n+1}/n$, how large must $n$ be so $|R_n|<0.01$?", "n ≥ 100",
         "$a_{n+1}=1/(n+1)<0.01\\Rightarrow n+1>100\\Rightarrow n\\geq 100$.", ["n ≥ 10", "n ≥ 99", "n ≥ 2"]),
        ("$\\sum (-1)^{n+1}/n^2$ converges?", "absolutely (hence also by AST)",
         "$\\sum 1/n^2$ is a convergent p-series, so absolute convergence holds.", ["conditionally only", "not at all", "only for even n"]),
        ("Conditional convergence means?", "the series converges but the absolute series diverges",
         "The alternating harmonic series is the prototype.", ["both converge", "both diverge", "a_n does not go to 0"]),
        ("$\\lim n^2/(n^2+3n)$ equals?", 1,
         "Divide by $n^2$: $1/(1+3/n)\\to 1$.", ["0", "3", "∞"]),
        ("Partial sums of $\\sum (1/2)^n$ approach which horizontal line?", "y = 2",
         "$s_n\\to 2$, so the sequence of dots climbs toward the line $y=2$.", ["y = 1", "y = 0", "y = 1/2"]),
        ("A telescoping series $\\sum (1/n-1/(n+1))$ converges to?", 1,
         "Partial sum $1-1/(n+1)\\to 1$.", ["0", "∞", "1/2"]),
        ("$\\sum n r^n$ for $|r|<1$ converges (term-by-term derivative of geometric). For $r=1/2$ the sum is?", 2,
         "$\\sum n x^{n}=x/(1-x)^2$ at $x=1/2$ gives $(1/2)/(1/2)^2=2$.", ["1", "4", "1/2"]),
        ("Nth-term test is inconclusive when $a_n\\to 0$. Next you should?",
         "try a more specific test (geometric, integral, comparison, AST, ratio)",
         "Inconclusive is not a synonym for converges.", ["conclude convergence", "conclude divergence", "stop"]),
        ("$\\int_2^{\\infty} dx/(x(\\ln x)^2)$ converges, so $\\sum 1/(n(\\ln n)^2)$ ?", "converges by the integral test",
         "$u=\\ln x$, $\\int u^{-2}du$ from $\\ln 2$ to $\\infty$ is finite.", ["diverges", "is geometric", "fails AST"]),
        ("Limit comparison of $n/(n^3+1)$ with $1/n^2$ gives $L=$ ?", 1,
         "$\\dfrac{n/(n^3+1)}{1/n^2}=\\dfrac{n^3}{n^3+1}\\to 1$.", ["0", "∞", "n"]),
        ("$\\sum 2^n/n!$ converges by the ratio test (Unit 5), but the nth-term test only tells you?",
         "terms go to 0, which is consistent with convergence but not a proof",
         "You still need a genuine convergence test.", ["it diverges", "the sum is 2", "it is geometric with r=2"]),
        ("AST decreasing check for $a_n=1/\\sqrt{n}$: eventually decreasing?", "yes, for n ≥ 1",
         "$1/\\sqrt{n}$ is decreasing on $[1,\\infty)$.", ["no", "only for even n", "never"]),
        ("The remainder of an alternating harmonic truncation after $4$ terms is at most?", "1/5",
         "$a_5=1/5$.", ["1/4", "1", "ln 2"]),
        ("$s_4$ for $1-1/2+1/3-1/4$ equals?", "7/12",
         "$1-1/2+1/3-1/4=(12-6+4-3)/12=7/12$.", ["1", "0", "5/6"]),
        ("Because the next term is $+1/5$, the true sum $\\ln 2$ compared with $7/12$ is?", "greater than 7/12",
         "AST: the partial sums bound the sum, and the remainder has the sign of the first omitted term.",
         ["less than 7/12", "equal to 7/12", "equal to 1"]),
        ("A p-series with $p=1$ is the?", "harmonic series, which diverges",
         "Integral of $1/x$ is $\\ln x\\to\\infty$.", ["geometric series", "telescoping 1", "absolutely convergent series"]),
        ("Direct comparison $1/(n^3+n)\\leq 1/n^3$ for $n\\geq 1$ proves?", "convergence of ∑ 1/(n^3+n)",
         "$\\sum 1/n^3$ is a convergent p-series.", ["divergence", "conditional convergence", "sum = 1"]),
        ("If $a_n\\sim 1/n$ (limit comparison $L=1$ with harmonic), then $\\sum a_n$ ?", "diverges",
         "Same behavior as $\\sum 1/n$.", ["converges", "converges absolutely", "is geometric"]),
        ("The sequence of partial sums of a convergent series is?", "a convergent sequence",
         "By definition, $\\sum a_n$ converges when $s_n\\to s$.", ["always geometric", "unbounded", "alternating"]),
        ("AP Stretch: For $\\sum (-1)^{n+1}/n^3$, the smallest $N$ with $|R_N|<10^{-4}$ satisfies?", "N ≥ 21",
         "$a_{N+1}=1/(N+1)^3<10^{-4}\\Rightarrow N+1>10^{4/3}\\approx 21.54$, so $N+1\\geq 22$, hence $N\\geq 21$. "
         "Check: $22^3=10648>10000$, $21^3=9261<10000$, so we need $N+1\\geq 22$, $N\\geq 21$.",
         ["N ≥ 10", "N ≥ 5", "N ≥ 100"]),
        ("AP Stretch: Limit comparison of $\\dfrac{n+\\sqrt{n}}{n^3-2}$ with $1/n^2$ yields $L=$ ?", 1,
         "Leading terms $n/n^3=1/n^2$, so the ratio tends to $1$.", ["0", "∞", "2"]),
        ("AP Stretch: $\\sum \\bigl(\\dfrac{n}{n+1}-\\dfrac{n+1}{n+2}\\bigr)$ is telescoping. The sum is?", "-1/2",
         "$\\dfrac{n}{n+1}-\\dfrac{n+1}{n+2}=\\dfrac{-1}{(n+1)(n+2)}$. Partial fractions give $\\dfrac{1}{n+2}-\\dfrac{1}{n+1}$ after a minus sign, "
         "so the series is $-\\sum_{n=1}^{\\infty}\\bigl(\\dfrac{1}{n+1}-\\dfrac{1}{n+2}\\bigr)=-1/2$.",
         ["1/2", "0", "1"]),
        ("AP Stretch: The integral test remainder $R_N\\leq \\int_N^{\\infty} f(x)\\,dx$ for decreasing $f$. For $f(x)=1/x^2$ and $N=10$, $R_{10}\\leq$ ?", "0.1",
         "$\\int_{10}^{\\infty} x^{-2}dx=1/10$.", ["1", "0.01", "10"]),
        ("AP Stretch: Which test proves $\\sum \\dfrac{\\ln n}{n^2}$ converges?",
         "integral test (or comparison ln n < √n, hence < 1/n^{3/2} for large n)",
         "$\\int (\\ln x)/x^2 dx$ converges by parts, or compare with a p-series $p=3/2$.",
         ["nth-term test alone", "geometric with r=ln n", "AST only"]),
        ("AP Stretch: $\\sum_{n=0}^{\\infty} (x-3)^n$ is geometric. It converges when?", "|x−3| < 1",
         "$|r|<1$ with $r=x-3$, i.e. $2<x<4$. (Endpoints fail because $r=\\pm 1$.)",
         ["|x| < 3", "all x", "x > 3"]),
        ("AP Stretch: Harmonic remainder $H_n-\\ln n\\to \\gamma$. For AP, the integral comparison already shows $H_n$ grows like?",
         "ln n (so H_n → ∞)",
         "The integral of $1/x$ is the logarithm. You do not need Euler's constant on the exam, but you do need divergence.",
         ["n^2", "a constant", "1/n"]),
        ("AP Stretch: For AST on $a_n=1/(n\\ln n)$ ($n\\geq 3$), the series $\\sum (-1)^n a_n$ ?",
         "converges conditionally",
         "AST applies ($a_n\\downarrow 0$), but $\\sum a_n$ diverges by the integral test, so the convergence is conditional.",
         ["converges absolutely", "diverges", "is geometric"]),
        ("AP Stretch: If $s$ is the sum of $\\sum (-1)^{n+1}/n$ and $s_6=1-1/2+1/3-1/4+1/5-1/6$, then?",
         "s_6 < s < s_6 + 1/7",
         "The next term is $+1/7$, so the remainder is positive and at most $1/7$. Thus $s_6<s<s_6+1/7$.",
         ["s < s_6", "s = s_6", "s > s_6 + 1"]),
    ])


def build_unit4():
    title = "AP Calculus BC Unit 4: Sequences & Series Tests"
    description = (
        "Sequence limits, geometric series, the nth-term test, the integral test, comparison tests, "
        "and the alternating series test with remainder."
    )
    concepts = [
        "Sequences and limits",
        "Geometric series",
        "nth-term / divergence test",
        "Integral test",
        "Comparison and limit comparison",
        "Alternating series and AST remainder",
    ]
    ast_sums = []
    s = 0.0
    for n in range(1, 9):
        s += ((-1) ** (n + 1)) / n
        ast_sums.append((n, s))
    c1 = concept_block(
        "1. Sequences and limits",
        [
            "A sequence is a list $a_1,a_2,a_3,\\ldots$. It converges to $L$ if the terms eventually stay arbitrarily close to $L$. Graphically, the dots $(n,a_n)$ approach a horizontal line $y=L$.",
            "Algebra of limits matches functions: sums, products, quotients (nonzero denominator limit). Squeeze still works. The standard limits $n^{1/n}\\to 1$ and $(1+1/n)^n\\to e$ are worth memorizing.",
            "A convergent sequence is bounded, but a bounded sequence need not converge ($(-1)^n$). Monotone bounded sequences do converge — the theorem behind many recursive AP setups.",
            "If $a_n=f(n)$ for a function $f$ with $\\lim_{x\\to\\infty}f(x)=L$, then $a_n\\to L$. L'Hôpital on $f$ is legal even though $n$ is discrete.",
            "Divergence happens by blowing up, by oscillating, or by approaching two different subsequential limits. Write the reason; 'diverges' alone is incomplete on an FRQ.",
            "Series are built from sequences of terms $a_n$ and sequences of partial sums $s_n$. Confusing $a_n\\to 0$ with $s_n\\to s$ is the original sin of BC series.",
        ],
        "Every series test begins with the sequence of terms. If you cannot decide $a_n\\to 0$, you are not ready to sum.",
        "Treat a_n like f(n). Compute the limit with algebra, L'Hôpital, or a known template. Then plot a few terms to sanity-check.",
        _fig(
            plot(
                curves=[],
                points=[(n, n / (n + 1), str(n)) for n in range(1, 9)] + [],
                dashes=[("h", 1, "y=1")],
                xlim=(-0.5, 9), ylim=(-0.1, 1.3),
                xlab="n", ylab="a_n",
            ),
            "The sequence $a_n=n/(n+1)$ climbing toward $y=1$",
            "The dots never reach $1$, but they get arbitrarily close. That is sequential convergence.",
        )
        + solved(1, "Find $\\lim_{n\\to\\infty} n/(n+1)$.",
                 ["Divide numerator and denominator by $n$.",
                  "$1/(1+1/n)\\to 1$."],
                 "$1$", "The graph of dots approaches the dashed line $y=1$.", "Easy")
        + solved(2, "Does $a_n=(-1)^n$ converge?",
                 ["Even terms are $1$, odd terms are $-1$.",
                  "Two subsequential limits, so the sequence diverges."],
                 "diverges", "Bounded is not enough.", "Medium")
        + solved(3, "Evaluate $\\lim (1+1/n)^n$.",
                 ["This is the sequential definition of $e$.",
                  "The limit is $e$."],
                 "$e$", "Do not write $1^\\infty=1$; it is an indeterminate power.", "Hard"),
        ("Confusing a_n with s_n",
         "a_n is one term. s_n is the sum of the first n terms. Graphs of terms and of partial sums look completely different."),
        ("Claiming a bounded oscillating sequence converges to 0",
         "(-1)^n is bounded and does not go to 0. Convergence requires one limit, not two cluster points."),
        [],
        1,
    )
    c2 = concept_block(
        "2. Geometric series",
        [
            "A geometric series has the form $\\sum_{n=0}^{\\infty} ar^n$. It converges if and only if $|r|<1$, to the sum $a/(1-r)$. If the first index is not $0$, factor out the first term so the formula still applies.",
            "Partial sums are $s_n=a\\dfrac{1-r^{n+1}}{1-r}$. The picture: dots climbing (or spiraling, if $r<0$) toward a horizontal asymptote.",
            "The case $|r|\\geq 1$ diverges because terms do not go to $0$ (except the empty case $a=0$). The series $1-1+1-1+\\cdots$ is the $r=-1$ warning.",
            "Differentiating or integrating a geometric series termwise produces $\\sum n x^{n}=x/(1-x)^2$ and $\\sum x^{n}/n=-\\ln(1-x)$ for $|x|<1$. That is Unit 5, but the seed is here.",
            "On FRQs, identify $a$ and $r$ explicitly. A common miss is using $a=$ the first displayed term while the exponent does not start at $0$.",
            "Decimal expansions $0.333\\ldots=3/10+3/100+\\cdots$ are geometric. The AP move is to write the first term and the ratio, then apply $a/(1-r)$.",
        ],
        "Geometric series are the only family whose sum you are expected to evaluate in closed form on BC besides a few telescoping examples.",
        "Write a and r, check |r|<1, then a/(1-r). Shift the index if the series does not start at n=0.",
        _fig(
            plot(
                points=[(n, 2 * (1 - 0.5 ** (n + 1)), "") for n in range(0, 9)],
                dashes=[("h", 2, "sum=2")],
                xlim=(-0.5, 9), ylim=(-0.2, 2.4),
                xlab="n", ylab="s_n",
            ),
            "Partial sums of $\\sum_{n=0}^{\\infty}(1/2)^n$ approaching $2$",
            "Each dot is $s_n=2(1-2^{-(n+1)})$. The infinite sum is the height of the dashed line, not any finite dot.",
        )
        + solved(4, "Sum $\\sum_{n=0}^{\\infty}(1/2)^n$.",
                 ["$a=1$, $r=1/2$, $|r|<1$.",
                  "Sum $1/(1-1/2)=2$."],
                 "$2$", "The picture's dashed line is this number.", "Easy")
        + solved(5, "Sum $\\sum_{n=1}^{\\infty}(1/3)^n$.",
                 ["First term $1/3$, ratio $1/3$.",
                  "$(1/3)/(1-1/3)=1/2$."],
                 "$1/2$", "Starting at $n=1$ drops the $n=0$ term $1$.", "Medium")
        + solved(6, "Sum $\\sum_{n=0}^{\\infty} 3(2/5)^n$.",
                 ["$a=3$, $r=2/5$.",
                  "$3/(1-2/5)=5$."],
                 "$5$", "Factor constants out of the series before using the formula.", "Hard"),
        ("Using a/(1-r) when |r|≥1",
         "The formula is false there. If |r|≥1 the series diverges (unless a=0)."),
        ("Mismatched first index",
         "If the series starts at n=3, factor r^3 (or the actual first term) so the remaining sum starts with exponent 0."),
        [],
        6,
    )
    c3 = concept_block(
        "3. nth-term / divergence test",
        [
            "If $\\sum a_n$ converges, then $a_n\\to 0$. The contrapositive is the nth-term test: if $a_n\\not\\to 0$, the series diverges.",
            "The converse is false. $1/n\\to 0$ but the harmonic series diverges. Seeing $a_n\\to 0$ is inconclusive — you must switch tests.",
            "Typical divergences: $a_n\\to 5$, $a_n\\to\\infty$, $a_n=(-1)^n$, $a_n=\\cos n$. In each case terms refuse to settle at $0$.",
            "Write the limit of $a_n$ on paper before naming the test. Readers award the divergence point for a correct $a_n\\not\\to 0$ computation even if you forget the test's name.",
            "This test never proves convergence. It is a filter that throws out hopeless series in ten seconds.",
            "For factorial or exponential ratios, $a_n\\to 0$ is often true (good news, inconclusive). The ratio test in Unit 5 finishes those.",
        ],
        "The nth-term test is the cheapest divergence proof on the exam. Use it before any comparison.",
        "Compute lim a_n. If the limit is not 0, stop: diverge. If it is 0, move to a real test.",
        _fig(
            plot(
                points=[(n, n / (n + 1), "") for n in range(1, 10)],
                dashes=[("h", 1, "y=1 ≠ 0")],
                xlim=(-0.5, 10.5), ylim=(-0.1, 1.3),
                xlab="n", ylab="a_n",
            ),
            "Terms $a_n=n/(n+1)$ refuse to go to $0$",
            "Because the dots head toward $1$ rather than $0$, $\\sum n/(n+1)$ diverges by the nth-term test. No further test is needed.",
        )
        + solved(7, "Does $\\sum n/(n+1)$ converge?",
                 ["$a_n\\to 1\\neq 0$.",
                  "Nth-term test: diverges."],
                 "diverges", "Do not try comparison here; the terms are huge.", "Easy")
        + solved(8, "Why doesn't $a_n=1/n\\to 0$ prove that the harmonic series converges?",
                 ["The nth-term test's converse is false.",
                  "You need the integral test (or Cauchy condensation) to prove divergence."],
                 "inconclusive (and in fact the series diverges)", "Zero terms are necessary, not sufficient.", "Medium")
        + solved(9, "Show $\\sum \\cos n$ diverges.",
                 ["$\\cos n$ has no limit, in particular not $0$.",
                  "Nth-term test applies."],
                 "diverges", "Do not confuse this with $\\sum \\cos(n)/n^2$, which does converge.", "Hard"),
        ("Declaring convergence because a_n→0",
         "That implication is backward. Harmonic series is the counterexample you must be able to quote."),
        ("Skipping the limit of a_n on a series that obviously blows up",
         "If a_n→5, you are done. Comparison with 1/n^2 would be a category error."),
        [],
        11,
    )
    c4 = concept_block(
        "4. Integral test",
        [
            "If $f$ is positive, continuous, and eventually decreasing, and $a_n=f(n)$, then $\\sum a_n$ and $\\int_N^{\\infty} f(x)\\,dx$ both converge or both diverge.",
            "The picture: rectangles of height $a_n$ sit above or below the curve $y=f(x)$. The improper integral from Unit 2 is exactly the series' continuous twin.",
            "p-series $\\sum 1/n^p$ converge iff $p>1$, copied from $\\int_1^{\\infty} x^{-p}dx$. This is the most-used corollary on BC.",
            "The integral test remainder: $R_N\\leq \\int_N^{\\infty} f(x)\\,dx$ (and a matching lower bound $\\int_{N+1}^{\\infty}$). AP uses this to guarantee a truncation error.",
            "Logs: $\\sum 1/(n\\ln n)$ diverges ($\\ln(\\ln x)$), while $\\sum 1/(n(\\ln n)^2)$ converges. The extra log power in the denominator is the difference between $p=1$ and $p>1$ in $u=\\ln x$.",
            "You may not use the integral test on an alternating integrand. Sign changes kill the rectangle comparison.",
        ],
        "The integral test is how p-series and log-p series are classified, and how you bound remainders without AST.",
        "Check positive/decreasing, integrate the continuous version, read convergence off the improper integral.",
        _fig(
            plot(
                curves=[("#4f46e5", sample_curve(lambda x: 1 / (x * x), 1, 6.5, 50))],
                fills=[(shade_under(lambda x: 1 / (x * x), 1, 6.5, 40), "#c7d2fe")],
                points=[(1, 1, "a1"), (2, 0.25, "a2"), (3, 1 / 9, "a3"), (4, 0.0625, "")],
                xlim=(0.5, 7), ylim=(-0.05, 1.15),
                xlab="x", ylab="y",
            ),
            "Integral test for $\\sum 1/n^2$: the curve $1/x^2$ and the terms as dots",
            "The shaded improper integral converges (area $1$ from $1$ to $\\infty$), so the series of dots converges too.",
        )
        + solved(10, "For which $p$ does $\\sum 1/n^p$ converge?",
                 ["Integral $\\int_1^{\\infty} x^{-p}dx$ converges iff $p>1$.",
                  "Hence the p-series converges iff $p>1$."],
                 "$p>1$", "At $p=1$ you recover the harmonic series.", "Easy")
        + solved(11, "Does $\\sum_{n=2}^{\\infty} 1/(n\\ln n)$ converge?",
                 ["$f(x)=1/(x\\ln x)$ is positive and decreasing on $[2,\\infty)$.",
                  "$\\int dx/(x\\ln x)=\\ln(\\ln x)\\to\\infty$.",
                  "The series diverges."],
                 "diverges", "This is the borderline log case.", "Medium")
        + solved(12, "Bound $R_{10}$ for $\\sum 1/n^2$ using $\\int_{10}^{\\infty} x^{-2}dx$.",
                 ["$\\int_{10}^{\\infty} x^{-2}dx=1/10$.",
                  "So $0<R_{10}\\leq 0.1$."],
                 "$R_{10}\\leq 0.1$", "A lower bound is $\\int_{11}^{\\infty}=1/11$.", "Hard"),
        ("Applying the integral test to an alternating series",
         "The comparison with area requires f≥0. Use AST instead when signs flip."),
        ("Forgetting decreasing",
         "A positive continuous f that wiggles up and down can break the rectangle sandwich. Check f'≤0 eventually, or argue from a formula like 1/x^p."),
        [],
        16,
    )
    c5 = concept_block(
        "5. Comparison and limit comparison",
        [
            "Direct comparison (nonnegative terms): if $0\\leq a_n\\leq b_n$ and $\\sum b_n$ converges, so does $\\sum a_n$. If $\\sum a_n$ diverges and $a_n\\geq b_n\\geq 0$, so does $\\sum b_n$.",
            "Limit comparison: $a_n,b_n>0$ and $\\lim a_n/b_n=L\\in(0,\\infty)$ implies the two series share a fate. $L=0$ or $L=\\infty$ can still be useful but needs extra care (one-sided comparison).",
            "The comparison series is usually a p-series or a geometric series. Look at leading powers: $n/(n^3+1)\\sim 1/n^2$.",
            "You cannot ignore signs. Direct comparison on $\\sum (-1)^n/n$ versus $1/n$ does not prove divergence of the alternating series (which in fact converges).",
            "On FRQs, name the comparison series and compute the limit $L$ (or state the inequality). 'It looks like $1/n^2$' is not enough.",
            "If limit comparison gives $L=0$ and $\\sum b_n$ converges, then $\\sum a_n$ still converges. If $L=\\infty$ and $\\sum b_n$ diverges, $\\sum a_n$ diverges.",
        ],
        "Most rational series on BC are limit-comparison clones of a p-series.",
        "Drop lower-order terms to guess the p. Then prove it with lim a_n/b_n.",
        _fig(
            plot(
                curves=[
                    ("#4f46e5", sample_curve(lambda x: 1 / (x * x), 1, 6, 50)),
                    ("#059669", sample_curve(lambda x: 1 / (x * x + x), 1, 6, 50)),
                ],
                xlim=(0.5, 6.5), ylim=(-0.05, 1.05),
            ),
            "$1/x^2$ (purple) vs $1/(x^2+x)$ (green)",
            "The green curve is smaller, and the purple p-integral converges, so the green series $\\sum 1/(n^2+n)$ converges by direct (or limit) comparison.",
        )
        + solved(13, "Show $\\sum 1/(n^2+n)$ converges.",
                 ["$0<1/(n^2+n)<1/n^2$.",
                  "$\\sum 1/n^2$ converges, so direct comparison applies.",
                  "Alternatively $\\lim n^2/(n^2+n)=1$ with $b_n=1/n^2$."],
                 "converges", "Either comparison is full credit.", "Easy")
        + solved(14, "Show $\\sum 1/(n+1)$ diverges.",
                 ["Limit comparison with $1/n$: $L=1$.",
                  "Harmonic diverges, so this shift diverges too."],
                 "diverges", "It is the harmonic series missing $n=1$.", "Medium")
        + solved(15, "Why is comparing $\\sum (-1)^n/n$ with $1/n$ illegal as a divergence proof?",
                 ["Direct comparison needs $a_n\\geq 0$.",
                  "The alternating harmonic series actually converges (AST). Absolute series diverges."],
                 "comparison requires nonnegative terms", "This is the definition of conditional convergence, coming next.", "Hard"),
        ("Comparing signed series as if they were positive",
         "Inequalities reverse when you multiply by −1. Stick to a_n≥0 for comparison tests."),
        ("Naming 1/n^2 without computing L",
         "Write lim a_n / (1/n^2) = … and box the finite positive number. That line is the rubric."),
        [],
        21,
    )
    c6 = concept_block(
        "6. Alternating series and AST remainder",
        [
            "Leibniz AST: if $a_n>0$, $a_n$ is eventually decreasing, and $a_n\\to 0$, then $\\sum (-1)^{n+1} a_n$ converges. Absolute convergence is a separate question.",
            "The remainder after $n$ terms satisfies $|R_n|\\leq a_{n+1}$ and has the same sign as the first omitted term. Partial sums therefore sandwich the true sum.",
            "Conditional convergence: the signed series converges but $\\sum |a_n|$ diverges. Alternating harmonic is the prototype. Rearrangements can then change the sum (Riemann's theorem) — BC mentions the warning, not the full proof.",
            "To force $|R_n|<10^{-k}$, solve $a_{n+1}<10^{-k}$ and take the smallest such integer $n$. For $a_n=1/n^p$ this is a root; for $1/n!$ it is a short table.",
            "Always check decreasing. $a_n=1/n+(-1)^n/n^2$ is not monotone even if it goes to $0$. For standard $1/n^p$ the check is easy.",
            "AST does not give the sum in closed form. It gives existence and an error bar. Geometric and telescoping series are the ones you actually add.",
        ],
        "AST remainder is a standard BC FRQ: 'how many terms to guarantee error less than …'",
        "Verify a_n↓0, conclude convergence, then use |R_n|≤a_{n+1} to pick n.",
        _fig(
            plot(
                points=[(n, s) for n, s in ast_sums],
                dashes=[("h", math.log(2), "ln 2")],
                xlim=(0, 9), ylim=(-0.1, 1.15),
                xlab="n", ylab="s_n",
            ),
            "Alternating harmonic partial sums oscillating toward $\\ln 2$",
            "Odd partial sums sit above the dashed limit; even ones sit below. The gap to the limit is at most the next term.",
        )
        + solved(16, "Does $\\sum (-1)^{n+1}/n$ converge?",
                 ["$a_n=1/n>0$ decreases to $0$.",
                  "AST: converges. Absolute series is harmonic, so the convergence is conditional."],
                 "conditionally convergent", "Name both AST and the harmonic divergence.", "Easy")
        + solved(17, "How large must $n$ be so the alternating harmonic remainder is $<0.01$?",
                 ["$|R_n|\\leq 1/(n+1)<0.01$.",
                  "$n+1>100$, so $n\\geq 100$."],
                 "$n\\geq 100$", "If the inequality is $\\leq 0.01$, $n=99$ is the borderline; AP usually wants a strict bound, hence $100$.", "Medium")
        + solved(18, "Given $s_6$ for the alternating harmonic series, trap $\\ln 2$.",
                 ["Next term is $+1/7$.",
                  "$s_6 < \\ln 2 < s_6+1/7$."],
                 r"$s_6<\ln 2<s_6+1/7$", "The remainder sign is the sign of the first omitted term.", "Hard"),
        ("Using |R_n|≤a_n instead of a_{n+1}",
         "The first omitted term is a_{n+1}, not the last included term. Off-by-one is the standard miss."),
        ("Skipping the decreasing check",
         "AST has three hypotheses. Terms to 0 without eventually decreasing can fail (there are textbook counterexamples)."),
        [],
        26,
    )
    content = unit_shell(
        title, AUDIENCE, concepts, c1 + c2 + c3 + c4 + c5 + c6,
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
        stretch_note=STRETCH_LABEL,
    )
    return title, description, content, _u4_questions()

