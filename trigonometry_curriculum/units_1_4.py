#!/usr/bin/env python3
"""Trigonometry units 1–4: right triangles, unit circle, sine/cosine, tangent graphs."""
from __future__ import annotations

import math

from curriculum_kit import lesson_figure, svg_circle, svg_triangle

from hs_curriculum import (
    concept_block,
    labeled_right_triangle,
    mq,
    number_line,
    practice_slots,
    sample_curve,
    solved,
    unit_circle_svg,
    unit_shell,
    xy_graph,
)
from .common import AUDIENCE, STRETCH_LABEL


def _sin_graph(A=1, B=1, C=0, D=0, a=None, b=None, n=100, color="#4f46e5"):
    if a is None:
        a = -2 * math.pi
    if b is None:
        b = 2 * math.pi
    lo, hi = D - abs(A) - 1.3, D + abs(A) + 1.3
    pts = sample_curve(lambda x, A=A, B=B, C=C, D=D: A * math.sin(B * x - C) + D, a, b, n=n)
    return xy_graph(curves=[(color, pts)], xlim=(a, b), ylim=(lo, hi), w=340, h=220, xlab="x", ylab="y")


def _cos_graph(A=1, B=1, C=0, D=0, a=None, b=None, n=100, color="#0f766e"):
    if a is None:
        a = -2 * math.pi
    if b is None:
        b = 2 * math.pi
    lo, hi = D - abs(A) - 1.3, D + abs(A) + 1.3
    pts = sample_curve(lambda x, A=A, B=B, C=C, D=D: A * math.cos(B * x - C) + D, a, b, n=n)
    return xy_graph(curves=[(color, pts)], xlim=(a, b), ylim=(lo, hi), w=340, h=220, xlab="x", ylab="y")


def _tan_graph(B=1, C=0, a=-3.5, b=3.5, n=140):
    skips = []
    k = -8
    while True:
        val = (math.pi / 2 + C + k * math.pi) / B
        if val > b + 0.3:
            break
        if val >= a - 0.3:
            skips.append(val)
        k += 1
    dashes = [("v", s, "asymp.") for s in skips if a + 0.15 < s < b - 0.15][:5]
    pts = sample_curve(
        lambda x, B=B, C=C: math.tan(B * x - C), a, b, n=n, skip=tuple(skips),
    )
    return xy_graph(
        curves=[("#b45309", pts)], dashes=dashes, xlim=(a, b), ylim=(-4.2, 4.2),
        w=340, h=230, xlab="x", ylab="y",
    )


def _csc_graph(a=-2 * math.pi, b=2 * math.pi, n=140):
    skips = tuple(k * math.pi for k in range(-4, 5))
    dashes = [("v", s, "") for s in skips if a < s < b]
    pts = sample_curve(lambda x: 1 / math.sin(x), a, b, n=n, skip=skips)
    return xy_graph(
        curves=[("#7c3aed", pts)], dashes=dashes, xlim=(a, b), ylim=(-4.5, 4.5),
        w=340, h=230, xlab="x", ylab="y",
    )


def _sec_graph(a=-2 * math.pi, b=2 * math.pi, n=140):
    skips = tuple(math.pi / 2 + k * math.pi for k in range(-4, 5))
    dashes = [("v", s, "") for s in skips if a < s < b]
    pts = sample_curve(lambda x: 1 / math.cos(x), a, b, n=n, skip=skips)
    return xy_graph(
        curves=[("#be185d", pts)], dashes=dashes, xlim=(a, b), ylim=(-4.5, 4.5),
        w=340, h=230, xlab="x", ylab="y",
    )


def _cot_graph(a=-3.4, b=3.4, n=140):
    skips = tuple(k * math.pi for k in range(-3, 4))
    dashes = [("v", s, "") for s in skips if a < s < b]
    pts = sample_curve(lambda x: 1 / math.tan(x) if abs(math.sin(x)) > 1e-9 else 1e9, a, b, n=n, skip=skips)
    return xy_graph(
        curves=[("#0369a1", pts)], dashes=dashes, xlim=(a, b), ylim=(-4.2, 4.2),
        w=340, h=230, xlab="x", ylab="y",
    )


def _acute_rt(opp=3, adj=4, hyp=5, opp_l="opp", adj_l="adj", hyp_l="hyp", theta="θ", w=300, h=210):
    """Right triangle with θ at the lower-right acute angle (opp vertical, adj horizontal)."""
    pad, base = 40, min(w, h) - 78
    scale = base / max(opp, adj, 1)
    x0, y0 = pad, h - pad
    x1, y1 = x0 + adj * scale, y0
    x2, y2 = x0, y0 - opp * scale
    sq = 14
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<polygon points="{x0:.1f},{y0:.1f} {x1:.1f},{y1:.1f} {x2:.1f},{y2:.1f}" '
        f'fill="#eef2ff" stroke="#312e81" stroke-width="2.2"/>'
        f'<rect x="{x0:.1f}" y="{y0 - sq:.1f}" width="{sq}" height="{sq}" fill="none" stroke="#312e81" stroke-width="1.6"/>'
        f'<text x="{(x0 + x2) / 2 - 22:.1f}" y="{(y0 + y2) / 2:.1f}" font-size="13">{opp_l}</text>'
        f'<text x="{(x0 + x1) / 2:.1f}" y="{y0 + 18:.1f}" text-anchor="middle" font-size="13">{adj_l}</text>'
        f'<text x="{(x1 + x2) / 2 + 10:.1f}" y="{(y1 + y2) / 2:.1f}" font-size="13">{hyp_l}</text>'
        f'<text x="{x1 - 22:.1f}" y="{y1 - 10:.1f}" font-size="14" fill="#b91c1c">{theta}</text>'
        f"</svg>"
    )


def _arc_sector(r=4, deg=60, w=280):
    th = math.radians(deg)
    pad, rr = 28, (w - 70) / 2
    cx = cy = w / 2
    px = cx + rr * math.cos(th)
    py = cy - rr * math.sin(th)
    large = 1 if deg > 180 else 0
    return (
        f'<svg viewBox="0 0 {w} {w}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="#f8fafc" stroke="#0f172a" stroke-width="1.6"/>'
        f'<line x1="{cx}" y1="{cy}" x2="{cx + rr}" y2="{cy}" stroke="#312e81" stroke-width="2"/>'
        f'<line x1="{cx}" y1="{cy}" x2="{px:.1f}" y2="{py:.1f}" stroke="#dc2626" stroke-width="2"/>'
        f'<path d="M {cx + rr} {cy} A {rr} {rr} 0 {large} 0 {px:.1f} {py:.1f}" fill="none" stroke="#d97706" stroke-width="3"/>'
        f'<text x="{cx + rr * 0.45:.1f}" y="{cy - 10}" font-size="12" fill="#b45309">θ={deg}°</text>'
        f'<text x="{cx + 8}" y="{cy + rr - 4}" font-size="12">r={r}</text>'
        f"</svg>"
    )


def _pack(rows):
    return [mq(text, ans, expl, i, distractors=dist) for i, (text, ans, expl, dist) in enumerate(rows, 1)]


# ===========================================================================
# UNIT 1: Right Triangle Trigonometry
# ===========================================================================

def _u1_questions():
    return _pack([
        ("In a right triangle, the side opposite $\\theta$ is $5$ and the hypotenuse is $13$. What is $\\sin\\theta$?",
         "5/13", "SOH: $\\sin\\theta=$ opposite/hypotenuse $=5/13$.", ["12/13", "5/12", "13/5"]),
        ("In a right triangle, the side adjacent to $\\theta$ is $8$ and the hypotenuse is $17$. What is $\\cos\\theta$?",
         "8/17", "CAH: $\\cos\\theta=$ adjacent/hypotenuse $=8/17$.", ["15/17", "8/15", "17/8"]),
        ("A right triangle has opposite $=7$ and adjacent $=24$ for angle $\\theta$. What is $\\tan\\theta$?",
         "7/24", "TOA: $\\tan\\theta=$ opposite/adjacent $=7/24$.", ["24/7", "7/25", "24/25"]),
        ("Which trigonometric ratio is defined as opposite divided by hypotenuse?",
         "sine", "The SOH part of SOH-CAH-TOA is $\\sin\\theta=$ opp/hyp.", ["cosine", "tangent", "secant"]),
        ("A $3$-$4$-$5$ right triangle has $\\sin\\theta=3/5$ for the angle opposite the side of length $3$. What is $\\cos\\theta$ for that same angle?",
         "4/5", "The adjacent side is $4$ and the hypotenuse is $5$, so $\\cos\\theta=4/5$.", ["3/5", "3/4", "5/4"]),
        ("If $\\sin\\theta=5/13$, what is $\\csc\\theta$?",
         "13/5", "Cosecant is the reciprocal of sine: $\\csc\\theta=1/\\sin\\theta=13/5$.", ["5/13", "12/5", "13/12"]),
        ("If $\\cos\\theta=8/17$, what is $\\sec\\theta$?",
         "17/8", "Secant is the reciprocal of cosine: $\\sec\\theta=1/\\cos\\theta=17/8$.", ["8/17", "17/15", "15/8"]),
        ("If $\\tan\\theta=7/24$, what is $\\cot\\theta$?",
         "24/7", "Cotangent is the reciprocal of tangent: $\\cot\\theta=1/\\tan\\theta=24/7$.", ["7/24", "24/25", "7/25"]),
        ("Which function is the reciprocal of sine?",
         "cosecant", "$\\csc\\theta=1/\\sin\\theta$. Secant is the reciprocal of cosine.", ["secant", "cotangent", "cosine"]),
        ("Given $\\sec\\theta=5/3$, what is $\\cos\\theta$?",
         "3/5", "Flip the secant ratio: $\\cos\\theta=1/\\sec\\theta=3/5$.", ["5/3", "4/5", "3/4"]),
        ("Using a cofunction identity, $\\sin 20^\\circ$ equals which cosine value?",
         "cos 70°", "$\\sin\\theta=\\cos(90^\\circ-\\theta)$, so $\\sin 20^\\circ=\\cos 70^\\circ$.", ["cos 20°", "cos 160°", "cos 10°"]),
        ("Using a cofunction identity, $\\tan 35^\\circ$ equals which cotangent value?",
         "cot 55°", "$\\tan\\theta=\\cot(90^\\circ-\\theta)$, so $\\tan 35^\\circ=\\cot 55^\\circ$.", ["cot 35°", "cot 45°", "tan 55°"]),
        ("Using a cofunction identity, $\\sec 12^\\circ$ equals which cosecant value?",
         "csc 78°", "$\\sec\\theta=\\csc(90^\\circ-\\theta)$, so $\\sec 12^\\circ=\\csc 78^\\circ$.", ["csc 12°", "csc 18°", "sec 78°"]),
        ("If $\\cos(90^\\circ-\\theta)=3/5$, what is $\\sin\\theta$?",
         "3/5", "The cofunction identity says $\\cos(90^\\circ-\\theta)=\\sin\\theta$, so $\\sin\\theta=3/5$.", ["4/5", "5/3", "12/13"]),
        ("Which pair is a cofunction identity?",
         "sin θ = cos(90°−θ)", "Sine and cosine of complementary angles are equal. The others mix the wrong functions or the wrong complement.",
         ["sin θ = sin(90°−θ)", "tan θ = tan(90°−θ)", "sin θ = sec(90°−θ)"]),
        ("The legs of a right triangle are $5$ and $12$. What is the hypotenuse?",
         "13", "Pythagoras: $\\sqrt{5^2+12^2}=\\sqrt{25+144}=\\sqrt{169}=13$.", ["17", "10", "7"]),
        ("In a right triangle the hypotenuse is $10$ and one acute angle is $30^\\circ$. What is the side opposite $30^\\circ$?",
         "5", "Opposite a $30^\\circ$ angle is half the hypotenuse: $10/2=5$. Also $\\sin 30^\\circ=1/2$.", ["5√3", "10", "5√2"]),
        ("In a $45^\\circ$-$45^\\circ$-$90^\\circ$ triangle one leg is $6$. What is the other leg?",
         "6", "The two legs of an isosceles right triangle are equal.", ["6√2", "3", "12"]),
        ("One acute angle of a right triangle is $37^\\circ$. What is the other acute angle?",
         "53°", "Acute angles in a right triangle are complementary: $90^\\circ-37^\\circ=53^\\circ$.", ["37°", "53° complementary to 127°", "90°"]),
        ("A right triangle has hypotenuse $20$ and a $60^\\circ$ angle. Length of the side adjacent to $60^\\circ$?",
         "10", "$\\cos 60^\\circ=1/2$, so adjacent $=20\\cdot(1/2)=10$.", ["10√3", "20√3", "10√2"]),
        ("A $13$-ft ladder stands $5$ ft from a wall. How high up the wall does the ladder reach?",
         "12 ft", "The $5$-$12$-$13$ triple: height $=\\sqrt{13^2-5^2}=12$.", ["8 ft", "18 ft", "√194 ft"]),
        ("From a point $40$ m from a building, the angle of elevation to the top is $30^\\circ$. What is the building's height?",
         "40√3/3 m", "Ground distance is adjacent, so $h=40\\tan 30^\\circ=40/\\sqrt{3}=40\\sqrt{3}/3$ m.",
         ["20 m", "40√3 m", "40 m"]),
        ("A lighthouse observer $50$ m above sea level looks down at $45^\\circ$ to a boat. How far is the boat from the base of the lighthouse?",
         "50 m", "Angle of depression $45^\\circ$ makes an isosceles right triangle: horizontal distance equals height.",
         ["50√2 m", "25 m", "100 m"]),
        ("A ramp rises $3$ m over a $4$ m horizontal run. What is $\\tan$ of the inclination angle?",
         "3/4", "Opposite over adjacent $=3/4$. The hypotenuse would be $5$, but tangent does not use it.",
         ["3/5", "4/5", "4/3"]),
        ("A tree casts a $15$-ft shadow when the sun's elevation is $60^\\circ$. How tall is the tree?",
         "15√3 ft", "$\\tan 60^\\circ=h/15=\\sqrt{3}$, so $h=15\\sqrt{3}$.", ["15 ft", "15/√3 ft", "30 ft"]),
        ("The exact sine of a $30^\\circ$ angle is:",
         "1/2", "In a $30$-$60$-$90$ triangle the side opposite $30^\\circ$ is half the hypotenuse.",
         ["√3/2", "√2/2", "√3"]),
        ("Evaluate $\\cos 45^\\circ$ exactly.",
         "√2/2", "In a $45$-$45$-$90$ triangle each leg over hypotenuse is $1/\\sqrt{2}=\\sqrt{2}/2$.",
         ["1", "√3/2", "√2"]),
        ("$\\tan 60^\\circ$ simplifies exactly to:",
         "√3", "Opposite $\\sqrt{3}$, adjacent $1$ in a $30$-$60$-$90$ triangle with hyp $2$.",
         ["1/√3", "√3/2", "1"]),
        ("On a $30^\\circ$-$60^\\circ$-$90^\\circ$ triangle with hypotenuse $2$, the side opposite $60^\\circ$ is:",
         "√3", "The longer leg is $\\sqrt{3}$ times the shorter; short leg is $1$, so opposite $60^\\circ$ is $\\sqrt{3}$.",
         ["1", "2", "√2"]),
        ("Which is the exact cosine of $30^\\circ$?",
         "√3/2", "Adjacent to $30^\\circ$ is $\\sqrt{3}$ when hyp $=2$.", ["1/2", "√2/2", "√3"]),
        ("A $5$-$12$-$13$ right triangle is viewed from the angle opposite $5$. What is $\\sin$ of that angle?",
         "5/13", "Opposite $5$, hypotenuse $13$.", ["12/13", "5/12", "12/5"]),
        ("For the angle adjacent to side $8$ in an $8$-$15$-$17$ triangle, $\\cos\\theta$ equals:",
         "8/17", "Adjacent $8$, hypotenuse $17$.", ["15/17", "8/15", "17/8"]),
        ("Find $\\csc\\theta$ if a right triangle has opposite $9$ and hypotenuse $41$ relative to $\\theta$.",
         "41/9", "$\\sin\\theta=9/41$, so $\\csc\\theta=41/9$.", ["9/41", "40/9", "41/40"]),
        ("Find $\\cot\\theta$ if opposite $=20$ and adjacent $=21$.",
         "21/20", "$\\cot\\theta=$ adjacent/opposite $=21/20$.", ["20/21", "21/29", "20/29"]),
        ("$\\sin 70^\\circ$ equals which of the following?",
         "cos 20°", "Cofunction: $\\sin 70^\\circ=\\cos(90^\\circ-70^\\circ)=\\cos 20^\\circ$.",
         ["sin 20°", "cos 70°", "tan 20°"]),
        ("If $\\tan\\theta=\\cot 40^\\circ$, then $\\theta$ equals:",
         "50°", "$\\tan\\theta=\\cot(90^\\circ-\\theta)$, so $90^\\circ-\\theta=40^\\circ$ and $\\theta=50^\\circ$.",
         ["40°", "45°", "130°"]),
        ("A right triangle has an acute angle of $22^\\circ$. The other acute angle is:",
         "68°", "$90^\\circ-22^\\circ=68^\\circ$.", ["22°", "78°", "158°"]),
        ("Hypotenuse $14$, angle $30^\\circ$. Side adjacent to $30^\\circ$?",
         "7√3", "$\\cos 30^\\circ=\\sqrt{3}/2$, so adjacent $=14\\cdot\\sqrt{3}/2=7\\sqrt{3}$.", ["7", "14√3", "7√2"]),
        ("A guy wire $26$ m long is anchored $10$ m from a pole. How high is the attachment on the pole?",
         "24 m", "$\\sqrt{26^2-10^2}=\\sqrt{676-100}=\\sqrt{576}=24$.", ["16 m", "36 m", "√5760 m"]),
        ("Angle of elevation $45^\\circ$ from $18$ m away. Height of the object?",
         "18 m", "$\\tan 45^\\circ=1$, so height equals the ground distance.", ["18√2 m", "9 m", "36 m"]),
        ("Exact value of $\\tan 30^\\circ$ in rationalized form:",
         "√3/3", "$1/\\sqrt{3}=\\sqrt{3}/3$.", ["√3", "1/2", "√3/2"]),
        ("Exact value of $\\sin 45^\\circ$:",
         "√2/2", "Equal legs over hyp $\\sqrt{2}$ give $1/\\sqrt{2}=\\sqrt{2}/2$.", ["1", "√2", "1/2"]),
        ("Exact value of $\\cos 60^\\circ$:",
         "1/2", "Adjacent to $60^\\circ$ is half the hypotenuse in $30$-$60$-$90$.", ["√3/2", "√2/2", "√3"]),
        ("If $\\sin\\theta=12/13$ in a right triangle, $\\cos\\theta$ is:",
         "5/13", "The remaining leg is $5$ because $5$-$12$-$13$. Adjacent/hyp $=5/13$.", ["12/5", "5/12", "13/12"]),
        ("A surveyor $80$ m from a tower measures a $30^\\circ$ angle of elevation to the top. Tower height?",
         "80√3/3 m", "$h=80\\tan 30^\\circ=80/\\sqrt{3}=80\\sqrt{3}/3$.", ["40 m", "80√3 m", "40√3 m"]),
        ("$\\sec 45^\\circ$ equals:",
         "√2", "$\\cos 45^\\circ=\\sqrt{2}/2$, so $\\sec 45^\\circ=\\sqrt{2}$.", ["√2/2", "1", "2"]),
        ("SAT Stretch: From $50$ m away, the angle of elevation to a building's roof is $60^\\circ$ and to a window on the same wall is $30^\\circ$. How far below the roof is the window?",
         "100√3/3 m",
         "Roof height $50\\tan 60^\\circ=50\\sqrt{3}$. Window height $50\\tan 30^\\circ=50/\\sqrt{3}=50\\sqrt{3}/3$. Difference $50\\sqrt{3}(1-1/3)=100\\sqrt{3}/3$.",
         ["50√3 m", "50√3/3 m", "25√3 m"]),
        ("SAT Stretch: From point $A$ on the ground, the angle of elevation to the top of a cliff is $30^\\circ$. Walking $40$ m closer, the angle becomes $45^\\circ$. How tall is the cliff?",
         "20(√3+1) m",
         "Let height be $h$ and original distance $x$. Then $h=x\\tan 30^\\circ=x/\\sqrt{3}$ and $h=(x-40)\\tan 45^\\circ=x-40$. "
         "So $x-40=x/\\sqrt{3}$. Then $x(1-1/\\sqrt{3})=40$, $x=40/(1-1/\\sqrt{3})=40\\sqrt{3}/(\\sqrt{3}-1)=20\\sqrt{3}(\\sqrt{3}+1)=20(3+\\sqrt{3})$. "
         "Then $h=x-40=20(3+\\sqrt{3})-40=20\\sqrt{3}+60-40=20\\sqrt{3}+20=20(\\sqrt{3}+1)$.",
         ["20(√3−1) m", "40 m", "20√3 m"]),
        ("SAT Stretch: $\\tan\\theta=8/15$ with $\\theta$ acute. Find $\\sin\\theta+\\cos\\theta$.",
         "23/17", "The triangle is $8$-$15$-$17$. Then $8/17+15/17=23/17$.",
         ["23/15", "17/8", "1"]),
        ("SAT Stretch: A $30^\\circ$-$60^\\circ$-$90^\\circ$ triangle has perimeter $18$. What is the hypotenuse?",
         "18−6√3",
         "Sides $x$, $x\\sqrt{3}$, $2x$ sum to $18$, so $x(3+\\sqrt{3})=18$. Rationalize: $x=18/(3+\\sqrt{3})\\cdot(3-\\sqrt{3})/(3-\\sqrt{3})=18(3-\\sqrt{3})/6=9-3\\sqrt{3}$. Hypotenuse $2x=18-6\\sqrt{3}=6(3-\\sqrt{3})$.",
         ["6(√3−1)", "6", "9"]),
        ("SAT Stretch: From the top of a $30$ m tower, the angles of depression to two buoys in line with the base are $45^\\circ$ and $30^\\circ$. Distance between the buoys?",
         "30(√3−1) m",
         "Ground distances $30\\cot 45^\\circ=30$ and $30\\cot 30^\\circ=30\\sqrt{3}$. Difference $30(\\sqrt{3}-1)$.",
         ["30√3 m", "30 m", "30(√3+1) m"]),
        ("SAT Stretch: From eye level, a tree's top has elevation $60^\\circ$ and a bird on the trunk has elevation $45^\\circ$. The observer is $12$ m from the tree. How far below the top is the bird?",
         "12(√3−1) m",
         "Top is $12\\tan 60^\\circ=12\\sqrt{3}$ above eye level; the bird is $12\\tan 45^\\circ=12$ above eye level. Difference $12(\\sqrt{3}-1)$. Eye height cancels.",
         ["12√3 m", "12 m", "12(√3+1) m"]),
        ("SAT Stretch: In right $\\triangle ABC$ with right angle $C$, $AC=20$, $\\angle A=30^\\circ$. Altitude $CD$ is drawn to hypotenuse $AB$. Length of $CD$?",
         "10",
         "$AC$ is adjacent to $\\angle A$, so $BC=20\\tan 30^\\circ=20/\\sqrt{3}$ and $AB=20/\\cos 30^\\circ=40/\\sqrt{3}$. "
         "The altitude to the hypotenuse is $(AC\\cdot BC)/AB=(20\\cdot 20/\\sqrt{3})/(40/\\sqrt{3})=10$. "
         "The trap $10\\sqrt{3}$ treats $AC$ as opposite $30^\\circ$ and uses the $1$-$\\sqrt{3}$-$2$ scale with hypotenuse $40$.",
         ["10√3", "20√3", "20/√3"]),
        ("SAT Stretch: A plane flies at $4000$ m. From an airport the elevation is $30^\\circ$; after flying horizontally toward the airport it is $60^\\circ$. How far did the plane fly?",
         "8000√3/3 m",
         "Horizontal distances $4000/\\tan 30^\\circ=4000\\sqrt{3}$ and $4000/\\tan 60^\\circ=4000/\\sqrt{3}$. Difference $4000(3-1)/\\sqrt{3}=8000/\\sqrt{3}=8000\\sqrt{3}/3$.",
         ["4000√3 m", "4000 m", "8000√3 m"]),
        ("SAT Stretch: $\\sin\\theta=8/17$ with $\\theta$ acute. Find $\\sec\\theta-\\tan\\theta$.",
         "3/5",
         "Adjacent $15$. Then $\\sec=17/15$, $\\tan=8/15$, difference $9/15=3/5$.",
         ["9/17", "8/15", "17/8"]),
    ])


def build_unit1():
    title = "Trigonometry Unit 1: Right Triangle Trigonometry"
    description = (
        "SOH-CAH-TOA, reciprocal ratios, cofunctions, solving right triangles, applications, "
        "and exact $30^\\circ/45^\\circ/60^\\circ$ values — with matching diagrams and a hard SAT Stretch set."
    )
    concepts = [
        "SOH-CAH-TOA",
        "Reciprocal ratios",
        "Cofunctions",
        "Solving right triangles",
        "Applications",
        "Exact values for 30/45/60",
    ]

    c1 = concept_block(
        "1. SOH-CAH-TOA",
        [
            "In a right triangle, every acute angle $\\theta$ has three primary trigonometric ratios. "
            "Sine is opposite over hypotenuse, cosine is adjacent over hypotenuse, and tangent is opposite over adjacent. "
            "The mnemonic SOH-CAH-TOA is not a definition — it is a packing label for those three fractions.",
            "Opposite means the side that does not touch $\\theta$ except at a vertex far away; it sits across from the angle. "
            "Adjacent means the leg that forms one ray of $\\theta$ but is not the hypotenuse. "
            "The hypotenuse is always the longest side, opposite the right angle.",
            "Switching which acute angle you look at swaps opposite and adjacent. The hypotenuse never moves. "
            "That is why $\\sin\\theta=\\cos(90^\\circ-\\theta)$ will appear in the cofunction lesson: the opposite of one acute angle is the adjacent of the other.",
            "These ratios are independent of the triangle's size. A $5$-$12$-$13$ triangle and a $10$-$24$-$26$ triangle have the same sine for corresponding angles, because every side scales by the same factor and the fractions cancel.",
            "On a test, first mark the right angle, then mark $\\theta$, then label opp / adj / hyp before writing any ratio. "
            "Students who skip the labels routinely grab the wrong two sides, especially when the triangle is rotated.",
            "Everything later in this course — the unit circle, graphs, identities — is this same ratio idea extended beyond acute angles. "
            "If SOH-CAH-TOA is automatic now, those later pictures will feel like the same triangle drawn on a circle.",
        ],
        "Without a reliable way to attach sine, cosine, and tangent to sides, you cannot solve a single right-triangle application, and you cannot read a unit-circle point as $(\\cos\\theta,\\sin\\theta)$.",
        "Name the angle first. Then name the three sides relative to that angle. Then write the one ratio the problem asks for. Never start by plugging numbers into a calculator before the ratio is written.",
        lesson_figure(
            labeled_right_triangle(a=5, b=12, c=13, a_lab="opp 5", b_lab="adj 12", c_lab="hyp 13", angle_lab="θ"),
            "A $5$-$12$-$13$ right triangle labeled for $\\theta$",
            "Opposite is the vertical leg, adjacent is the horizontal leg, hypotenuse is the slanted side. "
            "Then $\\sin\\theta=5/13$, $\\cos\\theta=12/13$, $\\tan\\theta=5/12$.",
        )
        + solved(1, "In a $5$-$12$-$13$ right triangle, find $\\sin\\theta$, $\\cos\\theta$, and $\\tan\\theta$ for the angle opposite the side of length $5$.",
                 ["Opposite $=5$, adjacent $=12$, hypotenuse $=13$.",
                  "$\\sin\\theta=5/13$.",
                  "$\\cos\\theta=12/13$.",
                  "$\\tan\\theta=5/12$."],
                 "$\\sin\\theta=5/13$, $\\cos\\theta=12/13$, $\\tan\\theta=5/12$", "", "Easy")
        + solved(2, "A right triangle has opposite $=8$ and adjacent $=15$ relative to $\\theta$. Find $\\sin\\theta$.",
                 ["The hypotenuse is missing, so use Pythagoras: $c=\\sqrt{8^2+15^2}=\\sqrt{64+225}=\\sqrt{289}=17$.",
                  "Now SOH: $\\sin\\theta=$ opposite/hypotenuse $=8/17$."],
                 "$8/17$", "Always recover the hypotenuse before writing sine or cosine if only the legs are given.", "Medium")
        + solved(3, "If $\\tan\\theta=9/12$ in an acute right triangle, find $\\sin\\theta$ in lowest terms.",
                 ["Reduce $9/12=3/4$. So opposite $=3k$ and adjacent $=4k$ for some $k>0$.",
                  "Hypotenuse $=5k$ by the $3$-$4$-$5$ triple.",
                  "$\\sin\\theta=3k/5k=3/5$."],
                 "$3/5$", "Tangent gives a similar-triangle scale; Pythagoras (or a known triple) finishes sine and cosine.", "Hard"),
        ("Calling the hypotenuse 'adjacent' because it touches $\\theta$",
         "The hypotenuse always touches both acute angles, but it is never called adjacent. Adjacent is reserved for the leg that touches $\\theta$. "
         "If your 'adjacent' is the longest side, you have mislabeled the triangle."),
        ("Write opp, adj, hyp on the figure before the ratio",
         "Circle $\\theta$, then write the three labels. Only after that copy two of them into SOH, CAH, or TOA. This two-second habit eliminates most ratio mix-ups."),
        ["I can label opposite, adjacent, and hypotenuse relative to a chosen acute angle.",
         "I can write $\\sin\\theta$, $\\cos\\theta$, and $\\tan\\theta$ as exact fractions.",
         "I can recover a missing side with Pythagoras before writing sine or cosine."],
        1,
    )

    c2 = concept_block(
        "2. Reciprocal ratios",
        [
            "Cosecant, secant, and cotangent are not new geometric ideas. They are the three primary ratios flipped. "
            "$\\csc\\theta=1/\\sin\\theta=$ hypotenuse/opposite, $\\sec\\theta=1/\\cos\\theta=$ hypotenuse/adjacent, and $\\cot\\theta=1/\\tan\\theta=$ adjacent/opposite.",
            "A useful pairing: sine with cosecant, cosine with secant, tangent with cotangent. "
            "The names are easy to mix up because 'secant' sounds like it should match sine. It does not. Secant matches cosine.",
            "On the unit circle later, secant will be the length of a tangent segment from the origin out to the line $x=1$, but you do not need that picture yet. "
            "In this unit, just invert the fraction you already have.",
            "If a primary ratio is $0$, its reciprocal is undefined. $\\sin 0^\\circ=0$ so $\\csc 0^\\circ$ does not exist. "
            "If a primary ratio is $1$, the reciprocal is also $1$. $\\tan 45^\\circ=1$ so $\\cot 45^\\circ=1$.",
            "Calculator traps: some devices have no csc button. Compute $\\sin\\theta$ first, then take the reciprocal. "
            "Do not take the reciprocal of the angle. $\\csc 30^\\circ$ is $1/\\sin 30^\\circ=2$, not $1/30$.",
            "Reciprocal identities are the fastest way to tidy an expression such as $\\sin\\theta\\csc\\theta$, which is identically $1$ wherever sine is defined and nonzero.",
        ],
        "Identities, graphs of secant and cosecant, and many contest simplifications are written in reciprocal language. If you cannot flip a ratio instantly, those problems stall.",
        "Ask: which primary function is this the flip of? Write that primary ratio from the triangle, then invert the fraction and reduce.",
        lesson_figure(
            labeled_right_triangle(a=8, b=15, c=17, a_lab="opp 8", b_lab="adj 15", c_lab="hyp 17", angle_lab="θ"),
            "An $8$-$15$-$17$ triangle for the reciprocal ratios",
            "$\\sin\\theta=8/17$ so $\\csc\\theta=17/8$. $\\cos\\theta=15/17$ so $\\sec\\theta=17/15$. $\\tan\\theta=8/15$ so $\\cot\\theta=15/8$.",
        )
        + solved(4, "In an $8$-$15$-$17$ triangle, find $\\csc\\theta$ for the angle opposite $8$.",
                 ["$\\sin\\theta=8/17$.",
                  "Flip: $\\csc\\theta=17/8$."],
                 "$17/8$", "", "Easy")
        + solved(5, "If $\\cos\\theta=5/13$, find $\\sec\\theta$ and $\\tan\\theta$.",
                 ["$\\sec\\theta=13/5$.",
                  "Opposite is $12$ because $5$-$12$-$13$.",
                  "$\\tan\\theta=12/5$."],
                 "$\\sec\\theta=13/5$, $\\tan\\theta=12/5$", "", "Medium")
        + solved(6, "Simplify $\\sin\\theta\\cdot\\sec\\theta\\cdot\\cot\\theta$ for an acute $\\theta$.",
                 ["Rewrite everything in sine and cosine: $\\sin\\theta\\cdot(1/\\cos\\theta)\\cdot(\\cos\\theta/\\sin\\theta)$.",
                  "Cancel $\\sin\\theta$ and $\\cos\\theta$ (neither is $0$ for an acute angle).",
                  "The product is $1$."],
                 "$1$", "When a product of trig functions looks messy, expand into sine and cosine and cancel.", "Hard"),
        ("Matching secant with sine because both start with s",
         "Secant is the reciprocal of cosine. Cosecant is the reciprocal of sine. The extra 'co' on cosecant is the clue that it belongs with sine's cofunction family only by name accident — memorize the pairs, do not guess from the first letter."),
        ("Invert the ratio, not the angle",
         "Write $\\csc\\theta=1/\\sin\\theta$ as a fraction of sides. Never compute $1/\\theta$."),
        ["I can write csc, sec, and cot from a labeled right triangle.",
         "I can convert a primary ratio into its reciprocal and reduce.",
         "I can simplify a product of reciprocal functions by rewriting in sine and cosine."],
        6,
    )

    c3 = concept_block(
        "3. Cofunctions",
        [
            "Two angles are complementary when they add to $90^\\circ$. In a right triangle the two acute angles are always complementary, so each is the cofunction partner of the other.",
            "The cofunction identities say that a function of $\\theta$ equals the cofunction of the complement: "
            "$\\sin\\theta=\\cos(90^\\circ-\\theta)$, $\\tan\\theta=\\cot(90^\\circ-\\theta)$, $\\sec\\theta=\\csc(90^\\circ-\\theta)$, and the three reversed forms.",
            "Geometrically this is immediate. The side opposite $\\theta$ is adjacent to $90^\\circ-\\theta$. "
            "So $\\sin\\theta=$ opp/hyp for $\\theta$ is the same fraction as $\\cos(90^\\circ-\\theta)=$ adj/hyp for the other acute angle.",
            "These identities are how you rewrite $\\sin 80^\\circ$ as $\\cos 10^\\circ$ without a calculator. "
            "They are also how some multiple-choice questions hide a correct answer in a different function of a complementary angle.",
            "The identities remain true for any $\\theta$ where both sides are defined, not only for acute angles, but in this unit we only need the acute case. "
            "Later the unit circle will show the same pairing as a $90^\\circ$ rotation.",
            "A common exam move: you are told $\\sin(90^\\circ-\\theta)=4/5$ and asked for $\\cos\\theta$. Those are equal, so the answer is $4/5$ with no extra triangle required.",
        ],
        "Cofunctions connect the two acute angles of every right triangle and later justify why the cosine graph is the sine graph shifted by $\\pi/2$.",
        "Whenever you see $90^\\circ$ minus an angle inside a trig function, swap to the cofunction and drop the $90^\\circ-$. Check that both sides are defined.",
        lesson_figure(
            _acute_rt(opp=3, adj=4, hyp=5, opp_l="opp θ = adj α", adj_l="adj θ = opp α", hyp_l="hyp 5", theta="θ"),
            "The same $3$-$4$-$5$ triangle, two complementary acute angles",
            "If $\\theta$ sits at the lower right, its opposite is the vertical $3$. That same $3$ is adjacent to the other acute angle $\\alpha=90^\\circ-\\theta$. Hence $\\sin\\theta=\\cos\\alpha$.",
        )
        + solved(7, "Rewrite $\\sin 25^\\circ$ as a cosine.",
                 ["$\\sin\\theta=\\cos(90^\\circ-\\theta)$.",
                  "$90^\\circ-25^\\circ=65^\\circ$.",
                  "So $\\sin 25^\\circ=\\cos 65^\\circ$."],
                 "$\\cos 65^\\circ$", "", "Easy")
        + solved(8, "If $\\tan\\theta=\\cot 18^\\circ$, find the acute $\\theta$.",
                 ["$\\tan\\theta=\\cot(90^\\circ-\\theta)$.",
                  "Match $90^\\circ-\\theta=18^\\circ$.",
                  "$\\theta=72^\\circ$."],
                 "$72^\\circ$", "You could also write $\\cot 18^\\circ=\\tan 72^\\circ$ and compare.", "Medium")
        + solved(9, "Given $\\sec(90^\\circ-\\theta)=13/5$, find $\\sin\\theta$.",
                 ["$\\sec(90^\\circ-\\theta)=\\csc\\theta$, so $\\csc\\theta=13/5$.",
                  "Therefore $\\sin\\theta=5/13$.",
                  "Alternatively, $\\sec(90^\\circ-\\theta)=1/\\cos(90^\\circ-\\theta)=1/\\sin\\theta$, which is the same equation."],
                 "$5/13$", "", "Hard"),
        ("Writing $\\sin(90^\\circ-\\theta)=\\sin\\theta$",
         "Sine is not its own cofunction. The partner of sine is cosine. $\\sin(90^\\circ-\\theta)=\\cos\\theta$, not $\\sin\\theta$ (unless $\\theta=45^\\circ$)."),
        ("Complement first, then swap the function name",
         "Compute $90^\\circ-\\theta$ on scratch paper, then change sine$\\leftrightarrow$cosine, tangent$\\leftrightarrow$cotangent, secant$\\leftrightarrow$cosecant."),
        ["I can convert sine to cosine of the complement (and the other five pairs).",
         "I can solve $\\tan\\theta=\\cot\\alpha$ for an acute $\\theta$.",
         "I can use a cofunction to read $\\sin\\theta$ from a given $\\cos(90^\\circ-\\theta)$."],
        11,
    )

    c4 = concept_block(
        "4. Solving right triangles",
        [
            "To solve a right triangle means to find every missing side and every missing acute angle. "
            "You always already know one angle is $90^\\circ$. The other two angles add to $90^\\circ$, so one acute angle determines the last.",
            "Typical given data: two sides; or one side and one acute angle. "
            "Two sides: use Pythagoras for the third side, then use an inverse trig function (Unit 7) or a known exact ratio for an angle. "
            "One side and one acute angle: use sine, cosine, or tangent to find another side, then Pythagoras or a second ratio for the last side.",
            "Choose the ratio that uses the side you know and the side you want. "
            "If you know the hypotenuse and want the opposite, sine is the direct path. Using tangent would force an extra step.",
            "Keep exact values when the angle is $30^\\circ$, $45^\\circ$, or $60^\\circ$. Use a calculator approximation only when the angle is something like $37^\\circ$ and the problem asks for a decimal.",
            "Always check that the hypotenuse came out longest and that both acute angles add to $90^\\circ$. "
            "Those two checks catch almost every algebra slip.",
            "Solving triangles is the engine under every ladder, ramp, and angle-of-elevation story in the next lesson. Practice the clean version here first.",
        ],
        "Applications are just this algorithm with extra words. If you can solve a bare right triangle from two pieces of data, word problems become translation plus the same steps.",
        "List what you know. Circle what you want. Pick the ratio that contains exactly those two sides (and $\\theta$). Solve with algebra, then find the leftover pieces.",
        lesson_figure(
            labeled_right_triangle(a=7, b=24, c=25, a_lab="7", b_lab="24", c_lab="25", angle_lab="θ"),
            "Solve the $7$-$24$-$25$ right triangle",
            "Sides are complete. The acute angle $\\theta$ opposite $7$ satisfies $\\tan\\theta=7/24$. The other acute angle is $90^\\circ-\\theta$.",
        )
        + solved(10, "Legs $7$ and $24$. Find the hypotenuse.",
                 ["$c=\\sqrt{7^2+24^2}=\\sqrt{49+576}=\\sqrt{625}=25$."],
                 "$25$", "", "Easy")
        + solved(11, "Hypotenuse $10$, acute angle $30^\\circ$. Find both legs.",
                 ["Opposite $30^\\circ$: $10\\sin 30^\\circ=10\\cdot(1/2)=5$.",
                  "Adjacent to $30^\\circ$: $10\\cos 30^\\circ=10\\cdot\\sqrt{3}/2=5\\sqrt{3}$.",
                  "Check: $5^2+(5\\sqrt{3})^2=25+75=100=10^2$."],
                 "opposite $5$, adjacent $5\\sqrt{3}$", "", "Medium")
        + solved(12, "In right $\\triangle ABC$ with right angle $C$, $AC=9$, $\\angle A=60^\\circ$. Find $AB$ and $BC$.",
                 ["$AC$ is adjacent to $\\angle A$. Hypotenuse $AB$ satisfies $\\cos 60^\\circ=9/AB=1/2$, so $AB=18$.",
                  "Opposite $BC$ satisfies $\\tan 60^\\circ=BC/9=\\sqrt{3}$, so $BC=9\\sqrt{3}$.",
                  "Check: $9^2+(9\\sqrt{3})^2=81+243=324=18^2$."],
                 "$AB=18$, $BC=9\\sqrt{3}$", "Name the sides with the vertices, not only with opp/adj, when the problem uses $\\triangle ABC$ notation.", "Hard"),
        ("Using sine when the known side is adjacent",
         "If you know adjacent and want hypotenuse, cosine is the matching ratio. Sine would require a side you do not have yet. Match known-and-wanted to SOH, CAH, or TOA."),
        ("Find the easy angle first",
         "If one acute angle is given, immediately write the other as $90^\\circ$ minus that angle. Then you can choose whichever angle makes the ratio nicer."),
        ["I can find the third side of a right triangle from two sides.",
         "I can find a missing side from one side and one acute angle.",
         "I can check that the hypotenuse is longest and the acute angles sum to $90^\\circ$."],
        16,
    )

    c5 = concept_block(
        "5. Applications",
        [
            "Angle of elevation is the angle up from a horizontal line of sight to an object above. "
            "Angle of depression is the angle down from a horizontal line of sight to an object below. "
            "By alternate interior angles with a horizontal, an angle of depression from the top equals the angle of elevation from the ground to that same line of sight.",
            "A ladder leaning against a wall is a right triangle: wall and ground are the legs, the ladder is the hypotenuse. "
            "A ramp is the same picture lying on its side. A guy wire from a pole is again the hypotenuse.",
            "Read the problem once just to sketch. Mark the right angle, the given length, and the given angle. "
            "Only then decide whether you need sine, cosine, or tangent.",
            "Watch units and watch what is being asked. 'How far from the wall is the base of the ladder?' is adjacent, not opposite. "
            "'How high up the wall?' is opposite if the angle is at the ground.",
            "Multi-step applications stack two right triangles — for example walking closer to a building and measuring a second elevation angle. "
            "Assign a variable to the shared height, write two tangent equations, and eliminate the unknown ground distance.",
            "Keep exact values for $30^\\circ$, $45^\\circ$, and $60^\\circ$ in the answer unless the problem asks for a decimal. "
            "A height of $20\\sqrt{3}$ m is the finished form, not a checkpoint on the way to a rounded number.",
        ],
        "This is the public face of right-triangle trigonometry: surveying, navigation, architecture, and every SAT word problem that mentions a ladder or a shadow.",
        "Sketch first. Translate each sentence into a side or an angle. Then solve the triangle you drew, not the paragraph you read.",
        lesson_figure(
            _acute_rt(
                opp=40 / math.sqrt(3),
                adj=40,
                hyp=80 / math.sqrt(3),
                opp_l="h",
                adj_l="40 m",
                hyp_l="sightline",
                theta="30°",
            ),
            "Angle of elevation $30^\\circ$; the $40$ m is the ground (adjacent)",
            "Adjacent is the $40$ m ground distance, so $h=40\\tan 30^\\circ=40/\\sqrt{3}=40\\sqrt{3}/3$ m and the sightline is $40/\\cos 30^\\circ=80/\\sqrt{3}=80\\sqrt{3}/3$ m.",
        )
        + solved(13, "A $13$-ft ladder stands $5$ ft from a wall. How high up the wall does it reach?",
                 ["The ladder is the hypotenuse of a right triangle with base $5$.",
                  "Height $=\\sqrt{13^2-5^2}=\\sqrt{169-25}=\\sqrt{144}=12$ ft."],
                 "$12$ ft", "This is the $5$-$12$-$13$ triple in disguise.", "Easy")
        + solved(14, "From $50$ m offshore, the angle of elevation to the top of a cliff is $45^\\circ$. How high is the cliff?",
                 ["$\\tan 45^\\circ=h/50=1$.",
                  "So $h=50$ m.",
                  "A $45^\\circ$ elevation makes height equal to the horizontal distance."],
                 "$50$ m", "", "Medium")
        + solved(15, "A kite string is $80$ m long and makes a $60^\\circ$ angle with the ground. Find the kite's height, assuming the string is taut and straight.",
                 ["The string is the hypotenuse.",
                  "$h=80\\sin 60^\\circ=80\\cdot\\sqrt{3}/2=40\\sqrt{3}$ m."],
                 "$40\\sqrt{3}$ m", "If the problem had given the ground distance instead of the string, you would have used tangent.", "Hard"),
        ("Treating angle of depression as if it sat at the ground",
         "Depression is measured at the observer's eye, from the horizontal down. Transfer it to the ground triangle using alternate interior angles, then place it at the correct vertex."),
        ("Underline the asked-for length on your sketch",
         "Before choosing a ratio, point to the segment the question wants. Then choose SOH, CAH, or TOA to connect that segment to a known segment."),
        ["I can translate elevation and depression into a right triangle.",
         "I can choose sine, cosine, or tangent from a labeled sketch.",
         "I can keep exact $30/45/60$ answers in application problems."],
        21,
    )

    c6 = concept_block(
        "6. Exact values for $30^\\circ/45^\\circ/60^\\circ$",
        [
            "Two special right triangles give every exact trig value you are expected to know without a calculator. "
            "The $45^\\circ$-$45^\\circ$-$90^\\circ$ triangle has legs $1$ and $1$ and hypotenuse $\\sqrt{2}$. "
            "The $30^\\circ$-$60^\\circ$-$90^\\circ$ triangle has sides $1$, $\\sqrt{3}$, $2$ opposite those angles in that order.",
            "From the isosceles right triangle: $\\sin 45^\\circ=\\cos 45^\\circ=\\sqrt{2}/2$ and $\\tan 45^\\circ=1$. "
            "From the $30$-$60$-$90$: $\\sin 30^\\circ=1/2$, $\\cos 30^\\circ=\\sqrt{3}/2$, $\\tan 30^\\circ=1/\\sqrt{3}=\\sqrt{3}/3$, "
            "and $\\sin 60^\\circ=\\sqrt{3}/2$, $\\cos 60^\\circ=1/2$, $\\tan 60^\\circ=\\sqrt{3}$.",
            "Notice the pattern in sine as the angle grows $30^\\circ$, $45^\\circ$, $60^\\circ$: $1/2$, $\\sqrt{2}/2$, $\\sqrt{3}/2$. "
            "Cosine runs that list in reverse. Tangent is sine over cosine, which produces $1/\\sqrt{3}$, $1$, $\\sqrt{3}$.",
            "Memorize the two triangles, not a disconnected list of twelve decimals. "
            "If you forget $\\cos 30^\\circ$, draw the $1$-$\\sqrt{3}$-$2$ triangle, mark $30^\\circ$, and read adjacent over hypotenuse.",
            "These exact values survive into the unit circle: $30^\\circ$ is $\\pi/6$, $45^\\circ$ is $\\pi/4$, $60^\\circ$ is $\\pi/3$, and the coordinates are the same cosine and sine numbers, with signs according to quadrant.",
            "On SAT Stretch items you will combine two exact values, or use a special triangle inside a word problem, or simplify an expression such as $\\csc 30^\\circ+\\cot 45^\\circ$. "
            "Speed comes from seeing the triangle instead of reaching for a calculator that would only give a rounded decimal anyway.",
        ],
        "Exact special-angle values are the arithmetic of the rest of trigonometry. Graphs, identities, and inverse equations all assume you can write $\\sin 60^\\circ=\\sqrt{3}/2$ without hesitation.",
        "Draw the special triangle, label the angle you care about, then read the ratio. Rationalize $1/\\sqrt{2}$ and $1/\\sqrt{3}$ as a last step if the answer choices are rationalized.",
        lesson_figure(
            labeled_right_triangle(a=1, b=math.sqrt(3), c=2, a_lab="1", b_lab="√3", c_lab="2", angle_lab="30°"),
            "The $30^\\circ$-$60^\\circ$-$90^\\circ$ triangle with short leg $1$",
            "Opposite $30^\\circ$ is $1$, adjacent is $\\sqrt{3}$, hypotenuse is $2$. So $\\sin 30^\\circ=1/2$, $\\cos 30^\\circ=\\sqrt{3}/2$, $\\tan 30^\\circ=\\sqrt{3}/3$.",
        )
        + solved(16, "Find the exact value of $\\sin 30^\\circ$ and $\\cos 30^\\circ$.",
                 ["Short leg $1$ opposite $30^\\circ$, hypotenuse $2$.",
                  "$\\sin 30^\\circ=1/2$.",
                  "$\\cos 30^\\circ=\\sqrt{3}/2$."],
                 "$1/2$ and $\\sqrt{3}/2$", "", "Easy")
        + solved(17, "Find the exact value of $\\tan 45^\\circ$ and $\\sec 45^\\circ$.",
                 ["Legs $1$ and $1$, hypotenuse $\\sqrt{2}$.",
                  "$\\tan 45^\\circ=1/1=1$.",
                  "$\\sec 45^\\circ=\\sqrt{2}/1=\\sqrt{2}$."],
                 "$1$ and $\\sqrt{2}$", "", "Medium")
        + solved(18, "Simplify $\\sin 60^\\circ\\cos 30^\\circ+\\cos 60^\\circ\\sin 30^\\circ$.",
                 ["This is the sine addition formula for $\\sin(60^\\circ+30^\\circ)$, but you can also plug exact values.",
                  "$(\\sqrt{3}/2)(\\sqrt{3}/2)+(1/2)(1/2)=3/4+1/4=1$.",
                  "As a check, $\\sin 90^\\circ=1$."],
                 "$1$", "Recognizing the addition pattern is faster, but substituting exact values is always legal.", "Hard"),
        ("Swapping $30^\\circ$ and $60^\\circ$ values",
         "Sine grows as the angle grows from $0^\\circ$ to $90^\\circ$, so $\\sin 60^\\circ$ must be larger than $\\sin 30^\\circ$. If you just wrote $\\sin 60^\\circ=1/2$, that fails the size check."),
        ("Keep the two prototype triangles on scratch paper",
         "Sketch $1$-$1$-$\\sqrt{2}$ and $1$-$\\sqrt{3}$-$2$ at the top of the page. Every exact-value question is then a read-off, not a memory search."),
        ["I can draw $45$-$45$-$90$ and $30$-$60$-$90$ with the standard side lengths.",
         "I can state all six trig values at $30^\\circ$, $45^\\circ$, and $60^\\circ$ exactly.",
         "I can combine two exact values in a short expression."],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
        stretch_note=STRETCH_LABEL,
    )
    return title, description, content, _u1_questions()


# ===========================================================================
# UNIT 2: Unit Circle & Radian Measure
# ===========================================================================

def _u2_questions():
    return _pack([
        ("How many radians are in $180^\\circ$?",
         "π", "A half-turn is $\\pi$ radians. $180^\\circ=\\pi$ rad is the conversion anchor.", ["2π", "π/2", "90"]),
        ("Convert $60^\\circ$ to radians.",
         "π/3", "Multiply by $\\pi/180$: $60\\pi/180=\\pi/3$.", ["π/6", "π/4", "2π/3"]),
        ("Convert $\\pi/4$ radians to degrees.",
         "45°", "Multiply by $180/\\pi$: $(\\pi/4)\\cdot(180/\\pi)=45$.", ["30°", "60°", "90°"]),
        ("Convert $270^\\circ$ to radians.",
         "3π/2", "$270\\cdot\\pi/180=3\\pi/2$.", ["π/2", "3π/4", "2π"]),
        ("Which statement is true?",
         "One radian is the central angle that intercepts an arc equal in length to the radius",
         "That is the definition of a radian. It is not $60^\\circ$ and not a full turn.",
         ["One radian equals 60°", "One radian equals 180°", "One radian is a full rotation"]),
        ("A circle has radius $6$ and central angle $2$ radians. Arc length?",
         "12", "$s=r\\theta=6\\cdot 2=12$. $\\theta$ must be in radians.", ["3", "12π", "6"]),
        ("Radius $4$, central angle $\\pi/3$. Arc length?",
         "4π/3", "$s=4\\cdot\\pi/3=4\\pi/3$.", ["4/3", "π/3", "12π"]),
        ("An arc of length $10$ sits on a circle of radius $5$. Central angle in radians?",
         "2", "$\\theta=s/r=10/5=2$.", ["50", "2π", "1/2"]),
        ("A wheel of radius $2$ ft rolls through $3$ radians. Distance traveled along the ground?",
         "6 ft", "The ground distance equals the arc length $s=2\\cdot 3=6$.", ["5 ft", "6π ft", "3/2 ft"]),
        ("Radius $9$, arc $3\\pi$. Measure of the central angle?",
         "π/3", "$\\theta=3\\pi/9=\\pi/3$.", ["3π/9 in degrees only", "27π", "π/9"]),
        ("The point on the unit circle at $0^\\circ$ is:",
         "(1, 0)", "$(\\cos 0^\\circ,\\sin 0^\\circ)=(1,0)$.", ["(0, 1)", "(-1, 0)", "(0, -1)"]),
        ("Coordinates of the unit-circle point at $90^\\circ$:",
         "(0, 1)", "$\\cos 90^\\circ=0$, $\\sin 90^\\circ=1$.", ["(1, 0)", "(0, -1)", "(-1, 0)"]),
        ("Unit-circle coordinates at $180^\\circ$:",
         "(-1, 0)", "Left intercept of the circle.", ["(1, 0)", "(0, -1)", "(0, 1)"]),
        ("Unit-circle point at $60^\\circ$:",
         "(1/2, √3/2)", "$\\cos 60^\\circ=1/2$, $\\sin 60^\\circ=\\sqrt{3}/2$.", ["(√3/2, 1/2)", "(1/2, 1/2)", "(√2/2, √2/2)"]),
        ("Unit-circle point at $135^\\circ$:",
         "(-√2/2, √2/2)", "Reference $45^\\circ$ in QII: cosine negative, sine positive.",
         ["(√2/2, √2/2)", "(-√2/2, -√2/2)", "(√2/2, -√2/2)"]),
        ("The reference angle for $150^\\circ$ is:",
         "30°", "In QII, reference $=180^\\circ-150^\\circ=30^\\circ$.", ["150°", "60°", "15°"]),
        ("The reference angle for $7\\pi/6$ is:",
         "π/6", "$7\\pi/6$ is in QIII. Reference $=7\\pi/6-\\pi=\\pi/6$.", ["7π/6", "π/3", "5π/6"]),
        ("The reference angle for $300^\\circ$ is:",
         "60°", "QIV: $360^\\circ-300^\\circ=60^\\circ$.", ["300°", "30°", "120°"]),
        ("$\\sin 150^\\circ$ equals:",
         "1/2", "Reference $30^\\circ$, sine positive in QII.", ["-1/2", "√3/2", "-√3/2"]),
        ("$\\cos 210^\\circ$ equals:",
         "-√3/2", "Reference $30^\\circ$, cosine negative in QIII.", ["√3/2", "-1/2", "1/2"]),
        ("At $270^\\circ$ on the unit circle, $\\tan\\theta$ is:",
         "undefined", "$\\cos 270^\\circ=0$, so tangent is undefined.", ["0", "1", "-1"]),
        ("$\\sec(2\\pi/3)$ equals:",
         "-2", "$\\cos(2\\pi/3)=-1/2$, so $\\sec=-2$.", ["2", "-1/2", "2/√3"]),
        ("$\\csc(7\\pi/6)$ equals:",
         "-2", "$\\sin(7\\pi/6)=-1/2$, so $\\csc=-2$.", ["2", "-1/2", "√3/2"]),
        ("$\\cot(3\\pi/4)$ equals:",
         "-1", "$\\tan(3\\pi/4)=-1$, so cotangent is also $-1$.", ["1", "0", "undefined"]),
        ("All six functions exist at which of these angles?",
         "π/6", "At $\\pi/2$ cosine is $0$ (sec/tan undefined). At $\\pi$ sine is $0$ (csc/cot undefined). At $3\\pi/2$ cosine is $0$. At $\\pi/6$ none of the three primary values is $0$.",
         ["π/2", "π", "3π/2"]),
        ("An angle coterminal with $30^\\circ$ is:",
         "390°", "$30^\\circ+360^\\circ=390^\\circ$.", ["60°", "150°", "330°"]),
        ("An angle coterminal with $5\\pi/4$ is:",
         "13π/4", "Add $2\\pi=8\\pi/4$: $5\\pi/4+8\\pi/4=13\\pi/4$.", ["π/4", "9π/4", "7π/4"]),
        ("The angle $-45^\\circ$ is coterminal with:",
         "315°", "$-45^\\circ+360^\\circ=315^\\circ$.", ["45°", "135°", "225°"]),
        ("Find the coterminal angle to $800^\\circ$ that lies in $[0^\\circ,360^\\circ)$.",
         "80°", "$800-2\\cdot 360=800-720=80$.", ["40°", "80π", "160°"]),
        ("Two coterminal angles differ by an integer multiple of:",
         "360° (or 2π radians)", "That is the definition of coterminal.", ["90°", "180°", "π/2"]),
        ("Convert $225^\\circ$ to radians in terms of $\\pi$.",
         "5π/4", "$225\\pi/180=5\\pi/4$.", ["3π/4", "7π/4", "5π/6"]),
        ("Arc length on a unit circle equals the central angle measured in:",
         "radians", "When $r=1$, $s=\\theta$. Degrees would need a conversion factor.", ["degrees", "revolutions only", "diameter"]),
        ("A sector of radius $10$ has central angle $72^\\circ$. Arc length?",
         "4π", "$72^\\circ=2\\pi/5$ rad, $s=10\\cdot 2\\pi/5=4\\pi$.", ["720", "10π", "72/10"]),
        ("Unit-circle cosine of $4\\pi/3$:",
         "-1/2", "QIII, reference $\\pi/3$, cosine negative.", ["1/2", "-√3/2", "√3/2"]),
        ("Reference angle of $17\\pi/6$ after reducing coterminal into $[0,2\\pi)$:",
         "π/6", "$17\\pi/6-2\\pi=17\\pi/6-12\\pi/6=5\\pi/6$, which is QII, reference $\\pi-5\\pi/6=\\pi/6$.",
         ["17π/6", "5π/6", "π/3"]),
        ("$\\sin(4\\pi/3)$ equals:",
         "-√3/2", "QIII sine is negative; reference $60^\\circ$.", ["√3/2", "-1/2", "1/2"]),
        ("The terminal ray of $\\theta=\\pi$ hits the unit circle at:",
         "(-1, 0)", "Straight left along the negative $x$-axis.", ["(1, 0)", "(0, 1)", "(0, -1)"]),
        ("How many degrees is $5\\pi/6$ radians?",
         "150°", "$(5\\pi/6)\\cdot(180/\\pi)=150$.", ["30°", "120°", "210°"]),
        ("A point in QIV on the unit circle could be:",
         "(√3/2, -1/2)", "Cosine positive, sine negative — that is QIV, and $30^\\circ$ reference.",
         ["(-√3/2, -1/2)", "(-√3/2, 1/2)", "(√3/2, 1/2)"]),
        ("$\\tan(5\\pi/4)$ equals:",
         "1", "QIII, reference $\\pi/4$, tangent positive.", ["-1", "√3", "undefined"]),
        ("Coterminal with $-3\\pi/2$ in $[0,2\\pi)$:",
         "π/2", "$-3\\pi/2+2\\pi=\\pi/2$.", ["3π/2", "π", "0"]),
        ("If $s=r\\theta$ and $s=r$, then $\\theta$ equals:",
         "1 radian", "The defining equation of one radian.", ["1 degree", "π", "r"]),
        ("$\\cos 315^\\circ$ equals:",
         "√2/2", "QIV reference $45^\\circ$, cosine positive.", ["-√2/2", "√3/2", "-1/2"]),
        ("Which angle is NOT coterminal with $\\pi/3$?",
         "2π/3", "$2\\pi/3$ is a different direction. $\\pi/3+2\\pi=7\\pi/3$ and $\\pi/3-2\\pi=-5\\pi/3$ are coterminal.",
         ["7π/3", "-5π/3", "π/3 + π"]),
        ("On the unit circle, $y$-coordinate of the point at $240^\\circ$:",
         "-√3/2", "$\\sin 240^\\circ=-\\sin 60^\\circ=-\\sqrt{3}/2$.", ["√3/2", "-1/2", "1/2"]),
        ("A central angle of $3$ radians in a circle of radius $7$ intercepts an arc of length:",
         "21", "$s=7\\cdot 3=21$.", ["10/3", "21π", "3/7"]),
        ("SAT Stretch: A point $P$ on a circle of radius $6$ has $x$-coordinate $-3$ and lies in QIII. The smallest positive central angle to $P$, in radians, is $4\\pi/3$. What is the $y$-coordinate of $P$?",
         "-3√3",
         "Then $y=-\\sqrt{36-9}=-\\sqrt{27}=-3\\sqrt{3}$ in QIII. Equivalent: reference $60^\\circ$, non-unit scale $6\\cdot(-\\sqrt{3}/2)=-3\\sqrt{3}$.",
         ["3√3", "-3", "-√3"]),
        ("SAT Stretch: Two coterminal angles are $17\\pi/6$ and $\\theta$, with $\\theta$ in $(-2\\pi,0)$. Find $\\theta$.",
         "-7π/6", "$17\\pi/6-2\\cdot 2\\pi=17\\pi/6-24\\pi/6=-7\\pi/6$, which lies in $(-2\\pi,0)$.",
         ["-π/6", "-5π/6", "-11π/6"]),
        ("SAT Stretch: A point at the terminal side of $405^\\circ$ lies on a circle of radius $10$. After reducing $405^\\circ$ to $[0,360^\\circ)$, the coordinates of the point are:",
         "(5√2, 5√2)",
         "$405^\\circ-360^\\circ=45^\\circ$. Then $(10\\cos 45^\\circ,10\\sin 45^\\circ)=(10\\cdot\\sqrt{2}/2,10\\cdot\\sqrt{2}/2)=(5\\sqrt{2},5\\sqrt{2})$.",
         ["(√2/2, √2/2)", "(10, 10)", "(-5√2, 5√2)"]),
        ("SAT Stretch: $\\theta=-7\\pi/4$ radians. Convert to degrees, reduce to $[0,360^\\circ)$, then evaluate $\\sin\\theta$.",
         "√2/2",
         "$-7\\pi/4=-315^\\circ$, and $-315^\\circ+360^\\circ=45^\\circ$, so $\\sin\\theta=\\sin 45^\\circ=\\sqrt{2}/2$.",
         ["-√2/2", "1/2", "-1/2"]),
        ("SAT Stretch: The terminal side of $\\theta$ passes through $(-3,-3)$ (not necessarily unit). $\\cos\\theta$ equals:",
         "-√2/2", "The point is on $y=x$ in QIII. Distance $\\sqrt{18}=3\\sqrt{2}$, so $\\cos\\theta=-3/(3\\sqrt{2})=-1/\\sqrt{2}=-\\sqrt{2}/2$.",
         ["√2/2", "-1", "3√2"]),
        ("SAT Stretch: The terminal side of $\\theta$ passes through $(-5,5\\sqrt{3})$. Reduce the direction angle to $[0,2\\pi)$ and find $\\tan\\theta$.",
         "-√3",
         "QII, $r=10$. Reference $\\tan^{-1}((5\\sqrt{3})/5)=60^\\circ$, so $\\theta=2\\pi/3$. Tangent in QII is negative: $-\\sqrt{3}$.",
         ["√3", "√3/2", "-1/√3"]),
        ("SAT Stretch: A wheel of radius $20$ cm rotates $150^\\circ$. Arc length traveled by a point on the rim?",
         "50π/3 cm", "$150^\\circ=5\\pi/6$, $s=20\\cdot 5\\pi/6=50\\pi/3$.", ["3000 cm", "20π cm", "150/20 cm"]),
        ("SAT Stretch: An arc of length $5\\pi$ on a circle of radius $6$ subtends a central angle. A coterminal of that angle in $(-2\\pi,0)$ is:",
         "-7π/6",
         "$\\theta=s/r=5\\pi/6$ radians ($150^\\circ$). Then $5\\pi/6-2\\pi=-7\\pi/6$.",
         ["5π/6", "-5π/6", "-π/6"]),
        ("SAT Stretch: $\\theta=17\\pi/4$. Reduce to a coterminal in $[0,2\\pi)$, convert that angle to degrees, then find $\\tan\\theta$.",
         "1",
         "$17\\pi/4-2\\cdot 2\\pi=17\\pi/4-16\\pi/4=\\pi/4=45^\\circ$, and $\\tan 45^\\circ=1$.",
         ["-1", "√3", "0"]),
    ])


def build_unit2():
    title = "Trigonometry Unit 2: Unit Circle & Radian Measure"
    description = (
        "Degrees versus radians, arc length $s=r\\theta$, unit-circle coordinates, reference angles, "
        "all six functions on the circle, and coterminal angles."
    )
    concepts = [
        "Degrees vs radians",
        "Arc length s=rθ",
        "Unit circle coordinates",
        "Reference angles",
        "All six functions on the circle",
        "Coterminal angles",
    ]

    c1 = concept_block(
        "1. Degrees vs radians",
        [
            "A degree is $1/360$ of a full turn. That number $360$ is a historical choice, not a geometric necessity. "
            "A radian is the geometrically natural unit: one radian is the central angle that intercepts an arc whose length equals the radius.",
            "A full turn is $2\\pi$ radians because the circumference is $2\\pi r$ and $\\theta=s/r=2\\pi r/r=2\\pi$. "
            "A half turn is $\\pi$ radians, which is why $180^\\circ=\\pi$ is the conversion hinge.",
            "To convert degrees to radians, multiply by $\\pi/180$. To convert radians to degrees, multiply by $180/\\pi$. "
            "The $\\pi$ in the answer is not decoration — $60^\\circ=\\pi/3$ exactly, not 'about $1.05$ unless a decimal is requested.",
            "Memorize the special-angle dictionary now: $0$, $\\pi/6$, $\\pi/4$, $\\pi/3$, $\\pi/2$, $2\\pi/3$, $3\\pi/4$, $5\\pi/6$, $\\pi$, and the rest of the way around to $2\\pi$. "
            "Every later graph and equation in this course is written in radians by default.",
            "Calculators have a degree/radian mode. A wrong mode is the most common source of 'my sine came out bizarre' errors. "
            "If $\\sin(\\pi/2)$ is not $1$, the calculator is in degree mode.",
            "When a formula contains $\\theta$ next to a length — arc length, linear speed $v=r\\omega$, later calculus — $\\theta$ must be in radians. Degrees are only a human labeling system.",
        ],
        "Radians are the unit the rest of trigonometry and calculus actually use. If you only think in degrees, arc length and sine graphs will constantly be off by a factor of $\\pi/180$.",
        "Anchor every conversion on $180^\\circ=\\pi$. Scale that equality. Check that a right angle became $\\pi/2$, not $90\\pi$.",
        lesson_figure(
            unit_circle_svg(deg=60),
            "The ray at $60^\\circ=\\pi/3$ on the unit circle",
            "The same geometric angle can be labeled $60^\\circ$ or $\\pi/3$ radians. The point is $(\\cos 60^\\circ,\\sin 60^\\circ)=(1/2,\\sqrt{3}/2)$.",
        )
        + solved(1, "Convert $150^\\circ$ to radians.",
                 ["Multiply by $\\pi/180$: $150\\pi/180=5\\pi/6$."],
                 "$5\\pi/6$", "", "Easy")
        + solved(2, "Convert $5\\pi/4$ radians to degrees.",
                 ["Multiply by $180/\\pi$: $(5\\pi/4)\\cdot(180/\\pi)=225$ degrees."],
                 "$225^\\circ$", "", "Medium")
        + solved(3, "A central angle measures $2$ radians. Express it in degrees.",
                 ["$2\\cdot(180/\\pi)=360/\\pi$ degrees, which is about $114.6^\\circ$ but the exact form is $360/\\pi$.",
                  "Do not replace $2$ radians by $2^\\circ$ — that would be a mode error, not a conversion."],
                 "$360/\\pi$ degrees", "Unless a problem asks for a decimal, leave $\\pi$ in the answer.", "Hard"),
        ("Treating $\\pi$ as if it were $180$ without the degree symbol",
         "Writing '$\\pi=180$' is a shorthand for a conversion, not an equality of numbers. $\\pi$ is about $3.14$. $180$ degrees is a half-turn. Keep the units visible: $\\pi$ rad $=180^\\circ$."),
        ("Check a known angle after converting",
         "If you converted $90^\\circ$ and did not get $\\pi/2$, the factor $\\pi/180$ was upside down. Flip it and try again."),
        ["I can convert degrees to radians and back using $\\pi/180$.",
         "I can list the special angles in both units.",
         "I know when a formula requires radians."],
        1,
    )

    c2 = concept_block(
        "2. Arc length $s=r\\theta$",
        [
            "On a circle of radius $r$, a central angle of $\\theta$ radians intercepts an arc of length $s=r\\theta$. "
            "This is the definition of radian measure rearranged: $\\theta=s/r$.",
            "If $\\theta$ is handed to you in degrees, convert first. Using $s=r\\theta$ with $\\theta=60$ (thinking '$60$ degrees') produces an arc $60$ times too large compared with using $\\theta=\\pi/3$.",
            "The same formula gives the distance a wheel travels along the ground: the ground distance equals the arc length swept on the rim, $s=r\\theta$, with $\\theta$ the rotation in radians.",
            "A full rotation $\\theta=2\\pi$ recovers the circumference $s=2\\pi r$. A half rotation recovers $\\pi r$. "
            "Those familiar facts are special cases, not a different theory.",
            "Proportional reasoning also works: arc/circumference $=\\theta/(2\\pi)$, so $s=(\\theta/(2\\pi))\\cdot 2\\pi r=r\\theta$. "
            "If you forget the compact formula, this fraction-of-the-circle picture rebuilds it.",
            "Later, sector area is $\\frac12 r^2\\theta$ in radians — the same warning about units applies. In this lesson we stay with arc length.",
        ],
        "Every circular-motion and sector problem in precalculus starts from $s=r\\theta$. Getting the radian requirement wrong makes the entire later kinematics stack collapse.",
        "Write $s=r\\theta$ with a note 'θ in radians'. Convert the angle, substitute, and include units of length on $s$.",
        lesson_figure(
            _arc_sector(r=6, deg=120),
            "Radius $6$, central angle $120^\\circ=2\\pi/3$",
            "Arc length $s=6\\cdot(2\\pi/3)=4\\pi$. The highlighted arc is the $s$ in the formula, not the chord.",
        )
        + solved(4, "Radius $6$, $\\theta=2$ radians. Find $s$.",
                 ["$s=r\\theta=6\\cdot 2=12$."],
                 "$12$", "", "Easy")
        + solved(5, "Radius $4$, central angle $60^\\circ$. Find the exact arc length.",
                 ["Convert: $60^\\circ=\\pi/3$.",
                  "$s=4\\cdot\\pi/3=4\\pi/3$."],
                 "$4\\pi/3$", "", "Medium")
        + solved(6, "An arc of length $10\\pi$ lies on a circle of radius $8$. Find the central angle in degrees.",
                 ["$\\theta=s/r=10\\pi/8=5\\pi/4$ radians.",
                  "In degrees: $(5\\pi/4)\\cdot(180/\\pi)=225^\\circ$."],
                 "$225^\\circ$", "Convert to degrees only at the end if the problem asks for degrees.", "Hard"),
        ("Plugging a degree measure straight into $s=r\\theta$",
         "The formula is built from the radian definition. Convert, then multiply. A $90^\\circ$ angle with $r=2$ has arc $\\pi$, not $180$."),
        ("Estimate before converting",
         "A $60^\\circ$ angle is $1/6$ of the circle, so $s$ should be about one-sixth of $2\\pi r$. If your answer is nowhere near that, the units were wrong."),
        ["I can compute $s=r\\theta$ with $\\theta$ in radians.",
         "I can convert a degree angle before using the arc-length formula.",
         "I can solve for $r$ or $\\theta$ when $s$ is given."],
        6,
    )

    c3 = concept_block(
        "3. Unit circle coordinates",
        [
            "The unit circle is the circle of radius $1$ centered at the origin. A ray from the origin at angle $\\theta$ (from the positive $x$-axis, counterclockwise) hits the circle at the point $(\\cos\\theta,\\sin\\theta)$.",
            "That sentence is the definition of cosine and sine for any real $\\theta$, not only acute angles. "
            "The old right-triangle ratios agree with it in Quadrant I, because the point $(\\cos\\theta,\\sin\\theta)$ is the vertex of a right triangle with hypotenuse $1$.",
            "Signs follow the axes. In QI both coordinates are positive. In QII $x$ is negative and $y$ is positive. In QIII both are negative. In QIV $x$ is positive and $y$ is negative.",
            "Special angles give exact coordinates. At $\\pi/6$ the point is $(\\sqrt{3}/2,1/2)$. At $\\pi/4$ it is $(\\sqrt{2}/2,\\sqrt{2}/2)$. At $\\pi/3$ it is $(1/2,\\sqrt{3}/2)$. "
            "Axis angles: $(1,0)$, $(0,1)$, $(-1,0)$, $(0,-1)$ at $0$, $\\pi/2$, $\\pi$, $3\\pi/2$.",
            "Because $x^2+y^2=1$ on the unit circle, $\\cos^2\\theta+\\sin^2\\theta=1$ for every $\\theta$. That is the Pythagorean identity you will live with in Unit 5, already visible as geometry.",
            "To plot an angle such as $5\\pi/6$, reduce your thinking to 'QII, reference $\\pi/6$', then attach the QI coordinates of $\\pi/6$ with a negative $x$.",
        ],
        "Graphs of sine and cosine are just these $y$- and $x$-coordinates unrolled along an axis. Inverse trig and solving equations are 'which angles hit this $y$-value on the circle?'",
        "Name the quadrant. Name the reference angle. Write the QI coordinates of the reference angle. Attach the correct signs for the quadrant.",
        lesson_figure(
            unit_circle_svg(deg=150),
            "The unit-circle point at $150^\\circ=5\\pi/6$",
            "Reference angle $30^\\circ$, Quadrant II. Coordinates $(-\\sqrt{3}/2,1/2)$.",
        )
        + solved(7, "Find the unit-circle coordinates at $60^\\circ$.",
                 ["$\\cos 60^\\circ=1/2$, $\\sin 60^\\circ=\\sqrt{3}/2$.",
                  "Point: $(1/2,\\sqrt{3}/2)$."],
                 "$(1/2,\\sqrt{3}/2)$", "", "Easy")
        + solved(8, "Find the unit-circle coordinates at $5\\pi/6$.",
                 ["$5\\pi/6=150^\\circ$ is in QII with reference $\\pi/6$.",
                  "QI point for $\\pi/6$ is $(\\sqrt{3}/2,1/2)$.",
                  "QII: $x$ negative, $y$ positive $\\Rightarrow(-\\sqrt{3}/2,1/2)$."],
                 "$(-\\sqrt{3}/2,1/2)$", "", "Medium")
        + solved(9, "A point on the unit circle in QIII has $x=-1/2$. Find $y$ and the smallest positive $\\theta$.",
                 ["$x^2+y^2=1$ gives $y=\\pm\\sqrt{3}/2$. QIII forces $y$ negative: $y=-\\sqrt{3}/2$.",
                  "This is the $240^\\circ=4\\pi/3$ point (reference $60^\\circ$ in QIII).",
                  "The QII angle $2\\pi/3$ has the same $x$ but positive $y$, so it is not this point."],
                 "$y=-\\sqrt{3}/2$, $\\theta=4\\pi/3$", "The $x$-coordinate alone does not pick the quadrant; the problem had to tell you QIII.", "Hard"),
        ("Writing $(\\sin\\theta,\\cos\\theta)$ as the point",
         "The $x$-coordinate is cosine. The $y$-coordinate is sine. Reversing them is the most common unit-circle slip and it breaks every later graph."),
        ("Build QII/III/IV from QI, never from memory of twelve separate points",
         "Know the three QI special points and the four axis points. Everything else is a sign change."),
        ["I can state $(\\cos\\theta,\\sin\\theta)$ at the axis and special angles.",
         "I can attach the correct signs in each quadrant.",
         "I can recover $y$ from $x$ on the unit circle using $x^2+y^2=1$."],
        11,
    )

    c4 = concept_block(
        "4. Reference angles",
        [
            "The reference angle $\\theta'$ is the acute angle between the terminal side of $\\theta$ and the nearer $x$-axis. "
            "It is always between $0$ and $\\pi/2$ (or $0^\\circ$ and $90^\\circ$), and it is the angle you actually look up on the special-triangle list.",
            "Recipes: QI, $\\theta'=\\theta$. QII, $\\theta'=\\pi-\\theta$ (or $180^\\circ-\\theta$). QIII, $\\theta'=\\theta-\\pi$ (or $\\theta-180^\\circ$). QIV, $\\theta'=2\\pi-\\theta$ (or $360^\\circ-\\theta$).",
            "Then $\\sin\\theta=\\pm\\sin\\theta'$, $\\cos\\theta=\\pm\\cos\\theta'$, $\\tan\\theta=\\pm\\tan\\theta'$, with the sign determined by the quadrant (ASTC: all, sine, tangent, cosine positive, in QI–QIV order).",
            "Reference angles turn every 'evaluate $\\cos 7\\pi/6$' problem into a two-step: identify $\\theta'=\\pi/6$, then attach a minus sign because cosine is negative in QIII.",
            "If $\\theta$ is outside $[0,2\\pi)$, first find a coterminal angle in that interval, then take the reference angle. "
            "Do not compute $7\\cdot 2\\pi$ minus something until the angle is reduced.",
            "Reference angles are also how you solve $\\sin\\theta=1/2$ on a full rotation: the solutions are the QI angle $\\pi/6$ and the QII angle $\\pi-\\pi/6=5\\pi/6$. Unit 7 will systematize that.",
        ],
        "Without reference angles you would need a separate memorized value for every special angle around the circle. With them you need three QI triangles and a sign chart.",
        "Reduce coterminal, name the quadrant, subtract from the nearest $x$-axis, then attach ASTC signs to the QI value.",
        lesson_figure(
            unit_circle_svg(deg=210),
            "Reference angle for $210^\\circ=7\\pi/6$",
            "The terminal side is $30^\\circ$ past the negative $x$-axis, so $\\theta'=30^\\circ=\\pi/6$. Cosine and sine of $210^\\circ$ are the QI $30^\\circ$ values with both signs negative.",
        )
        + solved(10, "Find the reference angle for $150^\\circ$.",
                 ["$150^\\circ$ is in QII.",
                  "$\\theta'=180^\\circ-150^\\circ=30^\\circ$."],
                 "$30^\\circ$", "", "Easy")
        + solved(11, "Evaluate $\\cos 210^\\circ$.",
                 ["QIII, reference $30^\\circ$.",
                  "$\\cos 30^\\circ=\\sqrt{3}/2$, cosine negative in QIII.",
                  "$\\cos 210^\\circ=-\\sqrt{3}/2$."],
                 "$-\\sqrt{3}/2$", "", "Medium")
        + solved(12, "Evaluate $\\sin(17\\pi/6)$.",
                 ["Reduce: $17\\pi/6-2\\pi=17\\pi/6-12\\pi/6=5\\pi/6$.",
                  "$5\\pi/6$ is QII with reference $\\pi/6$.",
                  "Sine is positive in QII: $\\sin(17\\pi/6)=1/2$."],
                 "$1/2$", "Reducing first is not optional when the angle is larger than $2\\pi$.", "Hard"),
        ("Measuring the reference angle to the $y$-axis",
         "Reference angles are always to the $x$-axis. For $120^\\circ$, the angle to the $y$-axis is $30^\\circ$, but the reference angle is $60^\\circ$ (to the negative $x$-axis). Using $30^\\circ$ would give the wrong special values."),
        ("ASTC after the reference, not before",
         "First get the unsigned QI value. Then apply the sign. Mixing the two steps is how $\\cos 150^\\circ$ accidentally becomes $+\\sqrt{3}/2$."),
        ["I can find $\\theta'$ in every quadrant.",
         "I can evaluate sine, cosine, and tangent of a non-acute special angle.",
         "I can reduce an angle larger than $2\\pi$ before taking a reference angle."],
        16,
    )

    c5 = concept_block(
        "5. All six functions on the circle",
        [
            "On the unit circle, $\\tan\\theta=y/x=\\sin\\theta/\\cos\\theta$ whenever $x\\neq 0$. "
            "Secant is $1/x$, cosecant is $1/y$, cotangent is $x/y$, with the matching restrictions $x\\neq 0$ or $y\\neq 0$.",
            "Undefined values occur exactly where a denominator is zero. Tangent and secant blow up at odd multiples of $\\pi/2$. "
            "Cotangent and cosecant blow up at multiples of $\\pi$. Those are the vertical asymptotes you will graph in Unit 4.",
            "You can compute a reciprocal function without naming sine or cosine first: $\\sec\\theta$ is the reciprocal of the $x$-coordinate. "
            "At $2\\pi/3$, $x=-1/2$, so $\\sec(2\\pi/3)=-2$.",
            "Signs of the six functions follow the signs of $x$, $y$, and $y/x$. In QII, sine and cosecant are positive; the other four are negative.",
            "A point not on the unit circle still determines an angle. Divide by the distance $r=\\sqrt{x^2+y^2}$ to get "
            "$\\cos\\theta=x/r$, $\\sin\\theta=y/r$, and then the four others as usual.",
            "Axis angles are the stress test. At $\\pi/2$, cosine is $0$ so tangent and secant are undefined, while sine is $1$ so cosecant is $1$ and cotangent is $0$.",
        ],
        "Graphs of tan, cot, sec, and csc are these reciprocals and quotients plotted against $\\theta$. Domain errors on equations are these same zeros of sine or cosine.",
        "Read $(x,y)$ off the circle (or compute $x/r$ and $y/r$). Then form the ratio you need, and refuse to divide by zero.",
        lesson_figure(
            unit_circle_svg(deg=120),
            "All six functions at $120^\\circ=2\\pi/3$",
            "Point $(-1/2,\\sqrt{3}/2)$. Then $\\tan=-\\sqrt{3}$, $\\sec=-2$, $\\csc=2/\\sqrt{3}=2\\sqrt{3}/3$, $\\cot=-1/\\sqrt{3}=-\\sqrt{3}/3$.",
        )
        + solved(13, "Find $\\sec(2\\pi/3)$.",
                 ["$\\cos(2\\pi/3)=-1/2$.",
                  "$\\sec=1/\\cos=-2$."],
                 "$-2$", "", "Easy")
        + solved(14, "Find $\\tan(5\\pi/4)$.",
                 ["Point at $5\\pi/4$: $(-\\sqrt{2}/2,-\\sqrt{2}/2)$.",
                  "$\\tan=y/x=1$ (positive in QIII)."],
                 "$1$", "", "Medium")
        + solved(15, "Which of the six functions are undefined at $3\\pi/2$?",
                 ["At $3\\pi/2$ the point is $(0,-1)$.",
                  "$x=0$ makes $\\tan=y/x$ and $\\sec=1/x$ undefined.",
                  "$y=-1\\neq 0$, so sine, cosine, cosecant, and cotangent exist: $-1$, $0$, $-1$, and $0$ respectively."],
                 "tangent and secant", "Undefined is not the same as $0$. Cotangent is $0$ here, not undefined.", "Hard"),
        ("Saying tangent is undefined whenever sine is $0$",
         "Tangent is $y/x$. It is undefined when $x=0$, i.e. when cosine is $0$. When sine is $0$, tangent is $0$ (and cotangent is undefined)."),
        ("Write $x$ and $y$ first, then form ratios",
         "Do not try to remember six separate special-angle tables. One point, then five arithmetic steps."),
        ["I can evaluate all six functions from a unit-circle point.",
         "I can name the angles where tan/sec or cot/csc are undefined.",
         "I can handle a non-unit point by dividing by $r$."],
        21,
    )

    c6 = concept_block(
        "6. Coterminal angles",
        [
            "Two angles are coterminal when they share a terminal side. You get from one to the other by adding or subtracting a whole number of full turns: $\\theta+360^\\circ k$ or $\\theta+2\\pi k$ for $k\\in\\mathbb{Z}$.",
            "Every angle has infinitely many coterminal partners. The standard representative in degrees is the one in $[0^\\circ,360^\\circ)$; in radians, $[0,2\\pi)$. "
            "To find it, add or subtract $360^\\circ$ or $2\\pi$ until you land in the interval.",
            "Negative angles are measured clockwise. $-45^\\circ$ is coterminal with $315^\\circ$. $-3\\pi/2$ is coterminal with $\\pi/2$.",
            "Sine, cosine, and all the rest take the same value at coterminal angles: $\\sin(\\theta+2\\pi k)=\\sin\\theta$. "
            "That is why the graphs in Unit 3 are periodic with period $2\\pi$.",
            "When you evaluate $\\sin(17\\pi/6)$, the first move is a coterminal reduction, not a new special-angle fact. "
            "$17\\pi/6-2\\pi=5\\pi/6$, and then you already know the QII sine.",
            "A trap: adding $\\pi$ (a half-turn) does not produce a coterminal angle. It produces the opposite ray. "
            "$\\theta$ and $\\theta+\\pi$ have the same tangent, but they are not coterminal, and their sines are opposites.",
        ],
        "Reducing angles is the housekeeping step before reference angles, graphs, and general solutions of equations. Skip it and you will invent extra 'special values' that do not exist.",
        "Add or subtract $2\\pi$ (or $360^\\circ$) until the angle sits in the standard interval. Then proceed with quadrant and reference angle.",
        lesson_figure(
            unit_circle_svg(deg=390),
            "$390^\\circ$ lands on the same ray as $30^\\circ$",
            "One extra full turn: $390^\\circ-360^\\circ=30^\\circ$. The unit-circle point is identical, $(\\sqrt{3}/2,1/2)$.",
        )
        + solved(16, "Find a positive coterminal angle for $-45^\\circ$ in $[0^\\circ,360^\\circ)$.",
                 ["Add $360^\\circ$: $-45+360=315$."],
                 "$315^\\circ$", "", "Easy")
        + solved(17, "Reduce $17\\pi/6$ to $[0,2\\pi)$.",
                 ["Subtract $2\\pi=12\\pi/6$: $17\\pi/6-12\\pi/6=5\\pi/6$."],
                 "$5\\pi/6$", "", "Medium")
        + solved(18, "Find the coterminal angle to $800^\\circ$ in $[0^\\circ,360^\\circ)$, and then $\\cos 800^\\circ$.",
                 ["$800\\div 360=2$ remainder $80$, so $800^\\circ\\equiv 80^\\circ$.",
                  "$\\cos 800^\\circ=\\cos 80^\\circ$, which is positive but not a special-angle exact value.",
                  "If the problem only wanted the reduced angle, the answer is $80^\\circ$."],
                 "$80^\\circ$; $\\cos 800^\\circ=\\cos 80^\\circ$", "Reduction always works even when the leftover angle is not $30/45/60$.", "Hard"),
        ("Adding $\\pi$ and calling the result coterminal",
         "A half-turn points the opposite way. Coterminal requires a full turn, $2\\pi$ or $360^\\circ$."),
        ("Divide by $360$ or $2\\pi$ and keep the remainder",
         "In degrees, remainder after dividing by $360$ is the standard representative (adjust if negative). In radians, subtract $2\\pi$ in a common-denominator form."),
        ["I can produce coterminal angles by adding $2\\pi k$.",
         "I can reduce to $[0,2\\pi)$ or $[0^\\circ,360^\\circ)$.",
         "I know that trig values agree at coterminal angles."],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
        stretch_note=STRETCH_LABEL,
    )
    return title, description, content, _u2_questions()


# ===========================================================================
# UNIT 3: Graphing Sine and Cosine
# ===========================================================================

def _u3_questions():
    return _pack([
        ("The parent sine graph $y=\\sin x$ passes through the origin with which slope sign just to the right of $0$?",
         "positive", "Near $0$, $\\sin x\\approx x>0$ for small positive $x$, so the graph rises through the origin.",
         ["negative", "zero and staying zero", "undefined"]),
        ("On $[0,2\\pi]$, $y=\\sin x$ has zeros at:",
         "0, π, 2π", "Sine is zero at integer multiples of $\\pi$.", ["π/2 and 3π/2", "π/4, 3π/4", "only at 0"]),
        ("The maximum value of $y=\\sin x$ is:",
         "1", "Sine ranges over $[-1,1]$. The max is $1$, at $\\pi/2+2\\pi k$.", ["0", "π", "2"]),
        ("A midline of the parent sine curve is the line:",
         "y=0", "The parent wave is centered on the $x$-axis.", ["y=1", "y=x", "x=0"]),
        ("The parent sine curve is odd, which means:",
         "sin(−x)=−sin x", "The graph is symmetric through the origin.", ["sin(−x)=sin x", "sin(x+π)=sin x", "sin x is never negative"]),
        ("The parent cosine graph $y=\\cos x$ at $x=0$ equals:",
         "1", "Cosine starts at a maximum: $\\cos 0=1$.", ["0", "-1", "π/2"]),
        ("On $[0,2\\pi]$, $y=\\cos x$ has zeros at:",
         "π/2 and 3π/2", "Cosine is zero where sine has extrema, at odd multiples of $\\pi/2$.",
         ["0, π, 2π", "π/4 and 3π/4", "only at π"]),
        ("Compared with $y=\\sin x$, the graph of $y=\\cos x$ is the sine graph shifted:",
         "left π/2", "$\\cos x=\\sin(x+\\pi/2)$, a left shift of $\\pi/2$.", ["right π/2", "up 1", "left π"]),
        ("The minimum of $y=\\cos x$ is:",
         "-1", "Range is still $[-1,1]$; the min occurs at $x=\\pi+2\\pi k$.", ["0", "1", "-π"]),
        ("$y=\\cos x$ is an even function, so:",
         "cos(−x)=cos x", "The graph is symmetric about the $y$-axis.", ["cos(−x)=−cos x", "cos x is always positive", "cos(x+π)=cos x"]),
        ("The amplitude of $y=4\\sin x$ is:",
         "4", "Amplitude is $|A|=|4|=4$.", ["-4", "2π", "1"]),
        ("The period of $y=\\sin(2x)$ is:",
         "π", "Period $=2\\pi/|B|=2\\pi/2=\\pi$.", ["2π", "4π", "2"]),
        ("The period of $y=\\cos(x/3)$ is:",
         "6π", "$B=1/3$, period $=2\\pi/(1/3)=6\\pi$.", ["2π/3", "3π", "π/3"]),
        ("The amplitude of $y=-5\\cos x$ is:",
         "5", "Amplitude is the absolute value $|-5|=5$. The negative sign is a reflection, not a negative height.",
         ["-5", "1", "10"]),
        ("For $y=3\\sin(4x)$, one full cycle is completed every:",
         "π/2", "Period $=2\\pi/4=\\pi/2$.", ["π/4", "8π", "3"]),
        ("$y=\\sin(x-\\pi/2)$ is the parent sine shifted:",
         "right π/2", "The form $\\sin(x-C)$ with $C>0$ is a right shift of $C$.",
         ["left π/2", "up π/2", "right π"]),
        ("The phase shift of $y=\\cos(x+\\pi/3)$ is:",
         "left π/3", "$x+\\pi/3=x-(−\\pi/3)$, a left shift of $\\pi/3$.", ["right π/3", "left π", "right π/6"]),
        ("Rewrite $y=\\sin(2x-\\pi)$ to show the phase shift clearly. The shift is:",
         "right π/2", "$2x-\\pi=2(x-\\pi/2)$, so right $\\pi/2$.", ["right π", "left π/2", "left π"]),
        ("A cosine that has been shifted right by $\\pi/4$ can be written:",
         "y=cos(x−π/4)", "Subtracting $\\pi/4$ inside shifts right.", ["y=cos(x+π/4)", "y=cos x−π/4", "y=cos(4x)"]),
        ("The graph of $y=\\sin(x+\\pi)$ is the same as:",
         "y=−sin x", "A left (or right) shift of $\\pi$ reflects sine through the $x$-axis.",
         ["y=sin x", "y=cos x", "y=sin(2x)"]),
        ("The midline of $y=\\sin x+3$ is:",
         "y=3", "A vertical shift of $+3$ moves the center line to $y=3$.", ["y=0", "y=1", "y=−3"]),
        ("The range of $y=2\\cos x-1$ is:",
         "[-3, 1]", "Amplitude $2$ about midline $y=-1$ runs from $-1-2=-3$ to $-1+2=1$.",
         ["[-1, 1]", "[-2, 2]", "[0, 2]"]),
        ("$y=-\\sin x+4$ has maximum value:",
         "5", "Amplitude $1$ about midline $4$: max $=4+1=5$. The reflection does not change amplitude.",
         ["4", "3", "-1"]),
        ("A vertical shift down $2$ applied to $y=3\\sin x$ produces:",
         "y=3 sin x − 2", "Subtract $2$ outside the sine.", ["y=3 sin(x−2)", "y=3 sin x + 2", "y=sin(3x)−2"]),
        ("The midline of $y=4\\cos(2x)+1$ is:",
         "y=1", "The $+1$ is the vertical shift $D$.", ["y=4", "y=2", "y=0"]),
        ("A sine graph has amplitude $2$, period $2\\pi$, no phase shift, midline $y=0$. An equation is:",
         "y=2 sin x", "Parent period already $2\\pi$, so $B=1$.", ["y=2 sin(2x)", "y=sin(2x)", "y=2 cos x"]),
        ("A cosine graph has amplitude $3$, period $\\pi$, and midline $y=0$. An equation is:",
         "y=3 cos(2x)", "Period $\\pi$ means $2\\pi/|B|=\\pi$ so $|B|=2$.", ["y=3 cos x", "y=3 cos(πx)", "y=cos(2x)+3"]),
        ("A sine curve has max $5$ and min $-1$. Amplitude and midline are:",
         "amp 3, midline y=2", "Midline $=(5+(-1))/2=2$, amplitude $=(5-(-1))/2=3$.",
         ["amp 5, midline y=-1", "amp 6, midline y=2", "amp 3, midline y=0"]),
        ("A graph of sine is shifted right $\\pi/6$ with amplitude $1$ and period $2\\pi$. Equation:",
         "y=sin(x−π/6)", "Right shift subtracts $\\pi/6$ inside.", ["y=sin(x+π/6)", "y=sin(6x)", "y=sin x − π/6"]),
        ("Which equation has amplitude $4$, period $\\pi$, phase shift left $\\pi/4$, midline $y=-2$?",
         "y=4 sin(2x+π/2)−2", "$B=2$ for period $\\pi$; $2(x+\\pi/4)=2x+\\pi/2$ is left $\\pi/4$; $D=-2$.",
         ["y=4 sin(x−π/4)−2", "y=4 sin(2x−π/2)−2", "y=4 sin(2x+π/4)+2"]),
        ("How many zeros does $y=\\sin x$ have on the open interval $(0,2\\pi)$?",
         "1", "Only $x=\\pi$ in that open interval. The endpoints $0$ and $2\\pi$ are excluded.",
         ["2", "3", "0"]),
        ("The first positive $x$-intercept of $y=\\cos x$ is:",
         "π/2", "$\\cos x=0$ first at $\\pi/2$.", ["π", "3π/2", "0"]),
        ("$y=\\sin(4x)$ completes how many cycles on $[0,2\\pi]$?",
         "4", "Period $\\pi/2$, so $2\\pi/(\\pi/2)=4$ cycles.", ["1", "2", "8"]),
        ("A reflection of $y=\\sin x$ across the $x$-axis is:",
         "y=−sin x", "Multiply the outputs by $-1$.", ["y=cos x", "y=sin(x+π/2)", "y=sin(2x)"]),
        ("The period of $y=\\cos(3x-\\pi)$ is:",
         "2π/3", "$B=3$; the phase does not change the period.", ["3", "π", "2π"]),
        ("Range of $y=-2\\sin x+3$:",
         "[1, 5]", "Midline $3$, amplitude $2$: from $1$ to $5$.", ["[-2, 2]", "[3, 5]", "[-5, -1]"]),
        ("A cosine with amplitude $1$ starting at a minimum at $x=0$ is:",
         "y=−cos x", "Parent cosine starts at a max; a reflection starts at a min.",
         ["y=cos x", "y=sin x", "y=cos(x−π/2)"]),
        ("Phase shift of $y=\\sin(4x+\\pi)$ is:",
         "left π/4", "$4x+\\pi=4(x+\\pi/4)$.", ["left π", "right π/4", "right π"]),
        ("If a sine wave has period $4\\pi$, then $B$ equals:",
         "1/2", "$2\\pi/|B|=4\\pi$ so $|B|=1/2$.", ["4", "4π", "2"]),
        ("The graph of $y=\\sin x$ on $[-2\\pi,2\\pi]$ has how many turning points (local max or min)?",
         "4", "In each $2\\pi$ there are two turning points; two full periods give four.",
         ["2", "8", "1"]),
        ("$y=2\\sin x$ and $y=\\sin(2x)$ differ because:",
         "the first stretches vertically, the second compresses horizontally",
         "$A=2$ vs $B=2$. Amplitude vs period.",
         ["they are identical", "both only change period", "both only change amplitude"]),
        ("A vertical shift does not change:",
         "amplitude and period", "$D$ moves the midline but $|A|$ and $2\\pi/|B|$ stay the same.",
         ["the midline", "the range", "the maximum value"]),
        ("An equation for a cosine of amplitude $2$ with midline $y=1$ and period $2\\pi$ is:",
         "y=2 cos x + 1", "Parent period, $A=2$, $D=1$.", ["y=2 cos(2x)+1", "y=cos x + 2", "y=2 cos x − 1"]),
        ("The $x$-value of the first maximum of $y=\\sin(x-\\pi/3)$ to the right of the usual sine max at $\\pi/2$ is:",
         "5π/6", "Parent max at $\\pi/2$ slides right by $\\pi/3$: $\\pi/2+\\pi/3=5\\pi/6$.",
         ["π/6", "π/3", "π/2"]),
        ("$y=\\cos(x/2)$ on $[0,2\\pi]$ shows how much of a full cycle?",
         "half a cycle", "Period is $4\\pi$, so $[0,2\\pi]$ is half of one period.",
         ["one full cycle", "two cycles", "a quarter cycle"]),
        ("Which transformation of $y=\\sin x$ produces $y=3\\sin x-1$?",
         "vertical stretch by 3, then down 1", "Multiply outputs by $3$, then subtract $1$.",
         ["horizontal stretch by 3, down 1", "right 3, down 1", "vertical shrink by 3, up 1"]),
        ("SAT Stretch: A graph has a maximum at $(\\pi/6,4)$ and the next minimum at $(7\\pi/6,-2)$. A cosine equation is:",
         "y=3 cos(x−π/6)+1",
         "Midline $=(4+(-2))/2=1$ and amplitude $=(4-(-2))/2=3$. Max to min spans half a period: $7\\pi/6-\\pi/6=\\pi$, so $T=2\\pi$ and $B=1$. Cosine has a maximum at $x=\\pi/6$, hence $y=3\\cos(x-\\pi/6)+1$.",
         ["y=3 sin(x−π/6)+1", "y=3 sin x +1", "y=6 cos(x−π/6)+1"]),
        ("SAT Stretch: Write $y=-2\\sin(2x)+1$ as a cosine with a phase shift in $[0,\\pi)$. A valid form is:",
         "y=2 cos(2x+π/2)+1",
         "$-\\sin\\theta=\\cos(\\theta+\\pi/2)$, so $-2\\sin(2x)=2\\cos(2x+\\pi/2)$. Then add $1$.",
         ["y=2 cos(2x)+1", "y=-2 cos(2x)+1", "y=2 cos(2x−π/2)+1"]),
        ("SAT Stretch: A sine graph has consecutive zeros at $x=\\pi/12$ and $x=5\\pi/12$. What is $B$ in $y=A\\sin(Bx-C)+D$?",
         "3", "Those zeros differ by $\\pi/3$. Adjacent zeros of a sine wave are half a period apart, so $T=2\\pi/3$ and $B=2\\pi/T=3$. Equivalently, zeros of $\\sin(Bx)$ differ by $\\pi/B$.",
         ["6", "2", "12"]),
        ("SAT Stretch: A cosine has a maximum of $5$ at $x=\\pi/4$ and the next maximum at $x=5\\pi/4$. The minimum value is $-1$. An equation is:",
         "y=3 cos(2(x−π/4))+2",
         "Consecutive maxima are one period apart: $T=\\pi$, so $B=2$. Amplitude $(5-(-1))/2=3$ and midline $(5-1)/2=2$. Phase: a cosine max at $x=\\pi/4$.",
         ["y=3 cos(x−π/4)+2", "y=6 cos(2x)+2", "y=3 sin(2(x−π/4))+2"]),
        ("SAT Stretch: A sine wave crosses its midline $y=1$ going upward at $x=\\pi/6$ and next crosses that midline going downward at $x=5\\pi/6$. Amplitude $4$. An equation is:",
         "y=4 sin((3/2)(x−π/6))+1",
         "Those midline crossings are half a period apart: $2\\pi/3$, so $T=4\\pi/3$ and $B=2\\pi/T=3/2$. An upward midline crossing is a sine zero, hence a right shift of $\\pi/6$.",
         ["y=4 sin(x−π/6)+1", "y=4 cos((3/2)x)+1", "y=4 sin(2(x−π/6))+1"]),
        ("SAT Stretch: A cosine has a minimum of $-2$ at $x=0$ and the next maximum of $6$ at $x=\\pi$. An equation is:",
         "y=-4 cos x + 2",
         "Half-period $\\pi$ so $T=2\\pi$, $B=1$. Midline $=(-2+6)/2=2$, amplitude $4$. A minimum at $x=0$ is an upside-down cosine.",
         ["y=4 cos x + 2", "y=4 sin x + 2", "y=-4 cos(2x)+2"]),
        ("SAT Stretch: Consecutive maxima occur at $x=-\\pi/3$ and $x=5\\pi/3$, with maximum $7$ and minimum $1$. An equation is:",
         "y=3 cos(x+π/3)+4",
         "Period $5\\pi/3-(-\\pi/3)=2\\pi$, so $B=1$. Amplitude $3$, midline $4$. A cosine maximum at $x=-\\pi/3$ is $y=3\\cos(x+\\pi/3)+4$.",
         ["y=3 cos(x−π/3)+4", "y=3 sin(x+π/3)+4", "y=6 cos(x+π/3)+1"]),
        ("SAT Stretch: Amplitude $2$, period $4$, phase shift right $1$, midline $y=-3$, using sine. Using $B=\\pi/2$ because $2\\pi/B=4$, an equation is:",
         "y=2 sin((π/2)(x−1))−3", "Period $4$ is unusual (not a multiple of $\\pi$ only) but legal: $B=2\\pi/4=\\pi/2$, right shift $1$.",
         ["y=2 sin(4x−1)−3", "y=2 sin(πx/2)−3", "y=2 sin(x−1)−3"]),
        ("SAT Stretch: A cosine has a maximum of $4$ at $x=\\pi/8$ and the following minimum of $-2$ at $x=5\\pi/8$. An equation is:",
         "y=3 cos(2(x−π/8))+1",
         "Max to min is half a period: $T=\\pi$, $B=2$. Amplitude $3$, midline $1$. Cosine max at $x=\\pi/8$.",
         ["y=3 cos(x−π/8)+1", "y=3 sin(2(x−π/8))+1", "y=6 cos(2x)+1"]),
    ])


def build_unit3():
    title = "Trigonometry Unit 3: Graphing Sine and Cosine"
    description = (
        "Parent sine and cosine, amplitude and period, phase shift, vertical shift, "
        "and writing an equation from a transformed wave."
    )
    concepts = [
        "Parent sine",
        "Parent cosine",
        "Amplitude and period",
        "Phase shift",
        "Vertical shift",
        "Write an equation from a graph",
    ]

    c1 = concept_block(
        "1. Parent sine",
        [
            "The parent sine graph is $y=\\sin x$ with $x$ in radians. It is a smooth wave of amplitude $1$, period $2\\pi$, midline $y=0$. "
            "It starts at the origin, rises to $1$ at $x=\\pi/2$, returns to $0$ at $x=\\pi$, falls to $-1$ at $x=3\\pi/2$, and completes the cycle at $x=2\\pi$.",
            "Those five landmark points — start, max, midline, min, end — are the skeleton you plot before worrying about transformations. "
            "Every transformed sine graph is this same skeleton stretched, shifted, or flipped.",
            "Sine is odd: $\\sin(-x)=-\\sin x$. The graph is rotationally symmetric about the origin. "
            "It is also $2\\pi$-periodic: $\\sin(x+2\\pi)=\\sin x$, which is the unit-circle fact that adding a full turn does not change the point.",
            "On a viewing window $[-2\\pi,2\\pi]$ you should see two full hills-and-valleys. "
            "If your sketch has the first hill peaking at $x=\\pi$, you have drawn cosine by accident, or you used degree mode.",
            "The $x$-intercepts are $k\\pi$. The turning points are at $\\pi/2+k\\pi$, alternating max and min. "
            "Knowing those two families lets you answer intercept and extrema questions without a calculator.",
            "Sine's range is $[-1,1]$. No transformation-free sine value is ever $2$. If a problem claims $\\sin x=2$, it has no real solution — a fact Unit 7 will reuse.",
        ],
        "Every later sine transformation is a distortion of this one picture. If the parent landmarks are shaky, amplitude, period, and phase problems have nothing to hang on.",
        "Plot the five landmarks on $[0,2\\pi]$, then extend left and right by copying the cycle. Label the intercepts $0,\\pi,2\\pi$ and the peak $\\pi/2$.",
        lesson_figure(
            _sin_graph(1, 1, 0, 0, a=-2 * math.pi, b=2 * math.pi),
            "Parent sine $y=\\sin x$ on $[-2\\pi,2\\pi]$",
            "The wave crosses the origin, peaks at $1$, and completes a cycle every $2\\pi$. This is the actual sine curve, not an empty plane.",
        )
        + solved(1, "List the five landmarks of $y=\\sin x$ on $[0,2\\pi]$.",
                 ["$(0,0)$, $(\\pi/2,1)$, $(\\pi,0)$, $(3\\pi/2,-1)$, $(2\\pi,0)$."],
                 "$(0,0),(\\pi/2,1),(\\pi,0),(3\\pi/2,-1),(2\\pi,0)$", "", "Easy")
        + solved(2, "Where does $y=\\sin x$ reach $-1$ on $[0,2\\pi]$?",
                 ["The minimum of parent sine is at $3\\pi/2$."],
                 "$x=3\\pi/2$", "", "Medium")
        + solved(3, "How many solutions does $\\sin x=0$ have on $[-2\\pi,2\\pi]$?",
                 ["Zeros at every integer multiple of $\\pi$.",
                  "On $[-2\\pi,2\\pi]$ those are $-2\\pi,-\\pi,0,\\pi,2\\pi$, five solutions including both endpoints."],
                 "5", "Closed interval includes both $-2\\pi$ and $2\\pi$.", "Hard"),
        ("Peaking sine at $x=0$",
         "That is cosine. Sine is $0$ at $x=0$ and rising. If your first plotted point is $(0,1)$, you graphed the wrong parent."),
        ("Always mark $\\pi/2,\\pi,3\\pi/2,2\\pi$ on the $x$-axis before drawing",
         "The landmarks live at fourths of the period. Tick marks at $1,2,3,\\ldots$ instead of $\\pi/2$ will squash the wave into the wrong places."),
        ["I can sketch $y=\\sin x$ from five landmarks.",
         "I can name intercepts and extrema on one period.",
         "I know sine is odd and $2\\pi$-periodic."],
        1,
    )

    c2 = concept_block(
        "2. Parent cosine",
        [
            "The parent cosine graph is $y=\\cos x$. It has the same amplitude $1$, period $2\\pi$, and midline $y=0$ as sine, but it starts at a maximum: $\\cos 0=1$.",
            "Landmarks on $[0,2\\pi]$: $(0,1)$, $(\\pi/2,0)$, $(\\pi,-1)$, $(3\\pi/2,0)$, $(2\\pi,1)$. "
            "You can remember this as sine slid left by $\\pi/2$, because $\\cos x=\\sin(x+\\pi/2)$.",
            "Cosine is even: $\\cos(-x)=\\cos x$. The graph is symmetric about the $y$-axis. "
            "That is the algebraic twin of 'the unit-circle $x$-coordinate does not care whether you went clockwise or counterclockwise the same amount.'",
            "Zeros of cosine are odd multiples of $\\pi/2$. Extrema are at integer multiples of $\\pi$, alternating $1$ and $-1$.",
            "A frequent identification task: a wave that starts at a peak is a cosine (or a sine with a phase shift). "
            "A wave that starts at the midline and rises is a sine. Train your eye on that first point.",
            "Because cosine is a horizontal shift of sine, every transformation you learn for one transfers to the other. "
            "The formulas for amplitude, period, phase, and vertical shift are identical; only the parent landmarks differ.",
        ],
        "Many modeling problems start at a maximum (a high tide, a highest Ferris-seat, a peak voltage). Those are cosine graphs, not sine, unless you insert a phase.",
        "Plot the five cosine landmarks. If a problem starts at a max, use cosine as the parent; if it starts at the midline rising, use sine.",
        lesson_figure(
            _cos_graph(1, 1, 0, 0, a=-2 * math.pi, b=2 * math.pi),
            "Parent cosine $y=\\cos x$ on $[-2\\pi,2\\pi]$",
            "The wave starts at $(0,1)$, drops through $(\\pi/2,0)$ to $(\\pi,-1)$, and returns to $1$ at $2\\pi$.",
        )
        + solved(4, "List the five landmarks of $y=\\cos x$ on $[0,2\\pi]$.",
                 ["$(0,1)$, $(\\pi/2,0)$, $(\\pi,-1)$, $(3\\pi/2,0)$, $(2\\pi,1)$."],
                 "$(0,1),(\\pi/2,0),(\\pi,-1),(3\\pi/2,0),(2\\pi,1)$", "", "Easy")
        + solved(5, "Explain why $y=\\cos x$ is even using the unit circle.",
                 ["$\\cos(-\\theta)$ is the $x$-coordinate after a clockwise angle $\\theta$.",
                  "That is the same $x$-coordinate as the counterclockwise angle $\\theta$.",
                  "Hence $\\cos(-x)=\\cos x$, so the graph mirrors across the $y$-axis."],
                 "$\\cos(-x)=\\cos x$", "", "Medium")
        + solved(6, "Write $y=\\cos x$ as a phase-shifted sine.",
                 ["$\\cos x=\\sin(x+\\pi/2)$.",
                  "That is parent sine shifted left by $\\pi/2$.",
                  "Equivalently $\\cos x=\\sin(\\pi/2-x)$, a reflection form of the cofunction identity."],
                 "$y=\\sin(x+\\pi/2)$", "", "Hard"),
        ("Drawing cosine through the origin like sine",
         "Cosine is $1$ at the origin, not $0$. A graph through $(0,0)$ with a peak at $\\pi/2$ is sine."),
        ("Use evenness as a sketch check",
         "The left half of cosine must be a mirror of the right half. If your $-\\pi/2$ value is not equal to your $+\\pi/2$ value, the sketch is wrong."),
        ["I can sketch $y=\\cos x$ from five landmarks.",
         "I can identify cosine as even and as a shift of sine.",
         "I can name cosine zeros and extrema on one period."],
        6,
    )

    c3 = concept_block(
        "3. Amplitude and period",
        [
            "For $y=A\\sin(Bx)$ or $y=A\\cos(Bx)$ with $B>0$, the amplitude is $|A|$ and the period is $2\\pi/B$. "
            "Amplitude is the height from the midline to a peak, not the distance from trough to crest (that distance is $2|A|$).",
            "If $A$ is negative, the graph is reflected across the midline. Amplitude stays $|A|$. "
            "$y=-2\\sin x$ still has amplitude $2$; it just starts by going down instead of up.",
            "If $B>1$, the graph is compressed horizontally: more cycles in the same window. "
            "$y=\\sin(2x)$ has period $\\pi$, so two cycles on $[0,2\\pi]$. If $0<B<1$, the graph is stretched: $y=\\sin(x/2)$ has period $4\\pi$.",
            "To sketch, divide the period into four equal parts. Those four steps are where the landmarks land after the stretch. "
            "For $y=3\\sin(2x)$, the period $\\pi$ splits into steps of $\\pi/4$: landmarks at $0,\\pi/4,\\pi/2,3\\pi/4,\\pi$.",
            "Do not confuse $B$ with the period. Students often write period $=B$ or period $=2\\pi B$. The formula is $2\\pi/|B|$.",
            "Amplitude and period are independent. You can stretch vertically and compress horizontally at the same time, as in $y=4\\cos(3x)$, amplitude $4$, period $2\\pi/3$.",
        ],
        "Almost every modeling wave is 'taller or shorter' and 'faster or slower' than the parent. Amplitude and period are those two knobs.",
        "Read $A$ for height and $B$ for speed. Compute period $=2\\pi/|B|$, then quarter it to place landmarks.",
        lesson_figure(
            _sin_graph(2, 2, 0, 0, a=-math.pi, b=math.pi),
            "$y=2\\sin(2x)$: amplitude $2$, period $\\pi$",
            "The wave reaches $2$ and $-2$ and finishes a full cycle on $[0,\\pi]$, twice as fast as parent sine and twice as tall.",
        )
        + solved(7, "State the amplitude and period of $y=4\\sin x$.",
                 ["Amplitude $|4|=4$.",
                  "Period $2\\pi/1=2\\pi$."],
                 "amplitude $4$, period $2\\pi$", "", "Easy")
        + solved(8, "State the amplitude and period of $y=-3\\cos(2x)$.",
                 ["Amplitude $|-3|=3$.",
                  "Period $2\\pi/2=\\pi$.",
                  "The negative sign reflects the graph but does not change those two numbers."],
                 "amplitude $3$, period $\\pi$", "", "Medium")
        + solved(9, "Sketch landmarks for $y=2\\sin(4x)$ on $[0,\\pi/2]$.",
                 ["Period $=2\\pi/4=\\pi/2$, so this interval is exactly one cycle.",
                  "Quarter-period $=\\pi/8$.",
                  "Points: $(0,0)$, $(\\pi/8,2)$, $(\\pi/4,0)$, $(3\\pi/8,-2)$, $(\\pi/2,0)$."],
                 "$(0,0),(\\pi/8,2),(\\pi/4,0),(3\\pi/8,-2),(\\pi/2,0)$", "", "Hard"),
        ("Calling $2|A|$ the amplitude",
         "Amplitude is the radius of the oscillation, $|A|$, from midline to peak. Peak-to-trough is $2|A|$ and is sometimes asked separately — do not mix the names."),
        ("Quarter the period, not the parent $2\\pi$, after $B$ is applied",
         "Once you have the new period $T=2\\pi/B$, the landmark spacing is $T/4$. Using $\\pi/2$ spacing on a compressed wave puts the peak in the wrong place."),
        ["I can read amplitude as $|A|$.",
         "I can compute period $2\\pi/|B|$.",
         "I can place five landmarks on one compressed or stretched cycle."],
        11,
    )

    c4 = concept_block(
        "4. Phase shift",
        [
            "The general sine is $y=A\\sin(Bx-C)$ or, factored, $y=A\\sin\\big(B(x-h)\\big)$ with $h=C/B$. "
            "The number $h$ is the phase shift: right if $h>0$, left if $h<0$.",
            "A common error is to treat $C$ itself as the shift even when $B\\neq 1$. "
            "For $y=\\sin(2x-\\pi)$, the shift is not $\\pi$ to the right; factor $2(x-\\pi/2)$ to see a right shift of $\\pi/2$.",
            "Phase shift moves every landmark horizontally. The amplitude and period do not change. "
            "A right shift of $\\pi/2$ applied to sine produces a cosine: $\\sin(x-\\pi/2)=-\\cos x$, depending on sign — actually $\\sin(x-\\pi/2)=-\\cos x$. And $\\cos x=\\sin(x+\\pi/2)$.",
            "To sketch, find the new starting $x$-value $h$, then add quarters of the period. "
            "The five $x$-coordinates are $h$, $h+T/4$, $h+T/2$, $h+3T/4$, $h+T$.",
            "Inside a cosine, the same algebra applies. $y=\\cos(x+\\pi/3)$ is a left shift of $\\pi/3$ because $x+\\pi/3=x-(−\\pi/3)$.",
            "On multiple-choice tests, two equations can look different and still be the same graph after a cofunction or a $\\pi$ shift. "
            "Always factor $B$ out before comparing phase shifts.",
        ],
        "Writing an equation from a graph is mostly 'where did the cycle start?' That is phase shift. Missing the $C/B$ division is the standard way to lose the point.",
        "Factor $B$ out of the argument so the shift sits alone as $(x-h)$. Then $h$ is the horizontal move, no further arithmetic required.",
        lesson_figure(
            _sin_graph(1, 1, math.pi / 2, 0, a=-math.pi, b=2 * math.pi),
            "$y=\\sin(x-\\pi/2)$, a right phase shift of $\\pi/2$",
            "Parent sine's origin crossing has moved to $x=\\pi/2$. The shape is unchanged; only the horizontal placement changed. This coincides with $y=-\\cos x$.",
        )
        + solved(10, "Describe the phase shift of $y=\\sin(x-\\pi/3)$.",
                 ["$B=1$, $C=\\pi/3$, so $h=\\pi/3$.",
                  "Right $\\pi/3$."],
                 "right $\\pi/3$", "", "Easy")
        + solved(11, "Describe the phase shift of $y=\\cos(2x+\\pi)$.",
                 ["Factor: $2x+\\pi=2\\big(x+\\pi/2\\big)$.",
                  "$h=-\\pi/2$, a left shift of $\\pi/2$.",
                  "Period is still $\\pi$; only the start moved."],
                 "left $\\pi/2$", "If you reported 'left $\\pi$', you forgot to divide by $B=2$.", "Medium")
        + solved(12, "The graph of $y=\\sin(2x-\\pi/3)$ starts a sine cycle at which $x$?",
                 ["Set the argument equal to $0$: $2x-\\pi/3=0$.",
                  "$x=\\pi/6$.",
                  "That is the phase shift $h=(\\pi/3)/2=\\pi/6$ to the right."],
                 "$x=\\pi/6$", "", "Hard"),
        ("Using $C$ as the shift when $B\\neq 1$",
         "Always compute $h=C/B$, or factor $B$ out first. $y=\\sin(2x-\\pi)$ is not shifted by $\\pi$."),
        ("Set $Bx-C=0$ to find where the parent 'zero' moved",
         "That $x$ is the new start of the sine cycle. Then add $T/4$ repeatedly for the other landmarks."),
        ["I can factor $B(x-h)$ to read the phase shift.",
         "I can distinguish left vs right from the sign of $h$.",
         "I can find the $x$-value where a shifted sine cycle begins."],
        16,
    )

    c5 = concept_block(
        "5. Vertical shift",
        [
            "The full sine model is $y=A\\sin(Bx-C)+D$. The number $D$ lifts or drops the entire wave. The new midline is $y=D$.",
            "Range becomes $[D-|A|, D+|A|]$. Maximum is $D+|A|$, minimum is $D-|A|$. "
            "A problem that gives max $7$ and min $-1$ is telling you $D=3$ and $|A|=4$, because the average is the midline and the half-gap is the amplitude.",
            "Vertical shift does not change period or phase. You can graph the un-shifted wave first, then slide every point up or down by $D$.",
            "On axes, draw the dashed midline $y=D$ before plotting peaks. Students who skip the midline often treat $D$ as a new amplitude.",
            "A reflection $A<0$ still uses the same midline $D$. $y=-2\\sin x+5$ has midline $5$, max $7$, min $3$.",
            "In applications, $D$ is the average value: average temperature, average height of a tide, rest length of a spring. $A$ is the swing away from that average.",
        ],
        "Real waves almost never oscillate about $y=0$. Vertical shift is how the model sits at the correct average height.",
        "Average the max and min to get $D$. Half the difference of max and min to get $|A|$. Then attach $B$ and $h$ from period and a landmark.",
        lesson_figure(
            _sin_graph(2, 1, 0, 1, a=-2 * math.pi, b=2 * math.pi),
            "$y=2\\sin x+1$: amplitude $2$, midline $y=1$",
            "The wave oscillates between $-1$ and $3$. The dashed-looking center of the oscillation is $y=1$, not the $x$-axis.",
        )
        + solved(13, "Find the midline and range of $y=\\sin x+3$.",
                 ["Midline $y=3$.",
                  "Range $[3-1,3+1]=[2,4]$."],
                 "midline $y=3$, range $[2,4]$", "", "Easy")
        + solved(14, "Find amplitude, midline, max, and min for $y=2\\cos x-1$.",
                 ["Amplitude $2$, midline $y=-1$.",
                  "Max $=-1+2=1$, min $=-1-2=-3$.",
                  "Range $[-3,1]$."],
                 "amp $2$, midline $-1$, max $1$, min $-3$", "", "Medium")
        + solved(15, "A sine wave has maximum $5$ and minimum $-1$. Find $A$ and $D$ if the graph is not reflected.",
                 ["$D=(5+(-1))/2=2$.",
                  "$|A|=(5-(-1))/2=3$.",
                  "Unreflected sine: $A=3$, $D=2$."],
                 "$A=3$, $D=2$", "This extraction from max and min is the first step of writing an equation from a graph.", "Hard"),
        ("Treating $D$ as extra amplitude",
         "$y=\\sin x+3$ does not reach $4$ because 'amplitude became $4$'. Amplitude is still $1$; the whole wave sat on a higher shelf."),
        ("Draw $y=D$ as a dashed horizontal before plotting",
         "Peaks sit $|A|$ above that line, troughs $|A|$ below. The $x$-axis may no longer be the center."),
        ["I can state the midline $y=D$.",
         "I can write the range $[D-|A|,D+|A|]$.",
         "I can recover $A$ and $D$ from a max and a min."],
        21,
    )

    c6 = concept_block(
        "6. Write an equation from a graph",
        [
            "To write $y=A\\sin(B(x-h))+D$ or a cosine analogue, extract four numbers from the picture: amplitude, period, a convenient horizontal landmark, and the midline.",
            "Midline $D$ is the average of max and min. Amplitude $|A|$ is half the difference of max and min. "
            "Period $T$ is the $x$-distance from peak to next peak (or from one midline rising-crossing to the next same-type crossing). Then $B=2\\pi/T$.",
            "Choose sine if the graph crosses the midline going up at $x=h$. Choose cosine if the graph has a peak at $x=h$. "
            "Either parent can model any wave if you allow a phase; pick the one that makes $h$ obvious.",
            "If the graph is reflected (starts at a trough when you wanted a sine start), take $A$ negative or switch to cosine with a different $h$.",
            "Check by plugging one landmark back into your equation. If the peak you used does not satisfy the equation, the phase is wrong — usually a missed $B$ factor.",
            "SAT Stretch items often give a max point and the next min point rather than a pretty picture. "
            "The $x$-gap between consecutive max and min is half a period. The $y$-average is $D$. Then write the cosine that peaks at the max point.",
        ],
        "This is the skill that turns a tide chart or a sound wave into a formula. The rest of the unit exists to feed this four-number recipe.",
        "Read $D$ and $|A|$ from max/min. Read $T$ from peak-to-peak. Pick sine or cosine from a clear landmark. Write $B=2\\pi/T$ and $h$ from that landmark.",
        lesson_figure(
            _sin_graph(2, 2, math.pi / 2, 1, a=-math.pi / 2, b=math.pi),
            "$y=2\\sin(2x-\\pi/2)+1$, which is $2\\sin\\big(2(x-\\pi/4)\\big)+1$",
            "Amplitude $2$, period $\\pi$, right shift $\\pi/4$, midline $y=1$. The drawn curve is that transformed wave. A matching equation is also $y=2\\cos(2x)+1$ after a cofunction rewrite.",
        )
        + solved(16, "A cosine graph has amplitude $3$, period $2\\pi$, no phase shift, midline $y=0$. Write an equation.",
                 ["$A=3$, $B=1$, $h=0$, $D=0$.",
                  "$y=3\\cos x$."],
                 "$y=3\\cos x$", "", "Easy")
        + solved(17, "A sine graph has max $5$, min $-1$, period $\\pi$, and a midline rising-crossing at $x=\\pi/6$. Write an equation.",
                 ["$D=(5-1)/2=2$, $|A|=(5-(-1))/2=3$. Unreflected: $A=3$.",
                  "$B=2\\pi/\\pi=2$.",
                  "Sine starts (midline rising) at $h=\\pi/6$.",
                  "$y=3\\sin\\big(2(x-\\pi/6)\\big)+2=3\\sin(2x-\\pi/3)+2$."],
                 "$y=3\\sin(2x-\\pi/3)+2$", "", "Medium")
        + solved(18, "A wave has a maximum at $(\\pi/6,4)$ and the next minimum at $(7\\pi/6,-2)$. Write a cosine equation.",
                 ["$D=(4+(-2))/2=1$, $|A|=(4-(-2))/2=3$.",
                  "Max to min is half a period: $7\\pi/6-\\pi/6=\\pi$, so $T=2\\pi$, $B=1$.",
                  "Cosine has a max at $x=\\pi/6$: $y=3\\cos(x-\\pi/6)+1$."],
                 "$y=3\\cos(x-\\pi/6)+1$", "Sine would need a phase that puts a max at $\\pi/6$, namely $3\\sin(x+\\pi/3)+1$.", "Hard"),
        ("Forgetting to divide $C$ by $B$ when you write $A\\sin(Bx-C)+D$",
         "If the shift is $h$ and the coefficient is $B$, the inside is $B(x-h)=Bx-Bh$. The subtracted number is $Bh$, not $h$."),
        ("Prefer cosine when a peak is clearly marked",
         "One labeled maximum point plus a period is enough for $y=A\\cos(B(x-h))+D$ with $h$ equal to that $x$-coordinate."),
        ["I can extract $A$, $B$, $h$, and $D$ from a graph or from two extrema.",
         "I can choose sine vs cosine to make the phase simple.",
         "I can check the equation at one landmark."],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
        stretch_note=STRETCH_LABEL,
    )
    return title, description, content, _u3_questions()


# ===========================================================================
# UNIT 4: Tangent and Other Graphs
# ===========================================================================

def _u4_questions():
    return _pack([
        ("The parent tangent $y=\\tan x$ has a vertical asymptote at:",
         "x=π/2", "Cosine is zero at $\\pi/2$, so tangent is undefined there.", ["x=0", "x=π", "x=π/4"]),
        ("The period of $y=\\tan x$ is:",
         "π", "Tangent repeats every $\\pi$, not every $2\\pi$.", ["2π", "π/2", "2"]),
        ("$\\tan 0$ equals:",
         "0", "Sine is $0$ and cosine is $1$ at $x=0$.", ["1", "undefined", "π"]),
        ("On $(-\\pi/2,\\pi/2)$, $y=\\tan x$ is:",
         "increasing from −∞ to ∞", "It passes through the origin and has vertical asymptotes at both ends of the interval.",
         ["decreasing", "always positive", "a cosine wave"]),
        ("Another asymptote of $y=\\tan x$, besides $x=\\pi/2$, is:",
         "x=−π/2", "Odd multiples of $\\pi/2$ are the tangent asymptotes.", ["x=π", "x=0", "y=1"]),
        ("$y=\\cot x$ has a vertical asymptote at:",
         "x=0", "Sine is zero at $0$, so cotangent $x/y$ is undefined.", ["x=π/2", "x=π/4", "y=0"]),
        ("The period of $y=\\cot x$ is:",
         "π", "Like tangent, cotangent has period $\\pi$.", ["2π", "π/2", "1"]),
        ("$\\cot(\\pi/4)$ equals:",
         "1", "$\\tan(\\pi/4)=1$, so cotangent is $1$.", ["0", "undefined", "√3"]),
        ("Compared with tangent, cotangent is a reflection and shift: $\\cot x$ equals:",
         "tan(π/2 − x)", "Cofunction identity.", ["tan x", "−tan x", "1/sin x"]),
        ("On $(0,\\pi)$, $y=\\cot x$ goes from:",
         "+∞ down through 0 at π/2 toward −∞", "Positive in QI, zero at $\\pi/2$, negative in QII, asymptotes at $0$ and $\\pi$.",
         ["−∞ up to +∞", "always positive", "the same as tan x"]),
        ("$y=\\sec x$ has a vertical asymptote wherever:",
         "cos x = 0", "Secant is $1/\\cos x$.", ["sin x = 0", "tan x = 0", "x=0 only"]),
        ("The range of $y=\\sec x$ is:",
         "(−∞, −1] ∪ [1, ∞)", "Cosine stays in $[-1,1]$ excluding values that make secant skip $(-1,1)$.",
         ["[-1, 1]", "(−∞, ∞)", "[0, ∞)"]),
        ("$\\sec 0$ equals:",
         "1", "$\\cos 0=1$.", ["0", "undefined", "-1"]),
        ("A local minimum of $y=\\sec x$ occurs at $x=0$ with value:",
         "1", "The cosine maximum of $1$ becomes a secant minimum of $1$.", ["-1", "0", "2"]),
        ("The period of $y=\\sec x$ is:",
         "2π", "Secant inherits cosine's period $2\\pi$.", ["π", "π/2", "1"]),
        ("$y=\\csc x$ has a vertical asymptote at:",
         "x=0", "Sine is $0$ at integer multiples of $\\pi$.", ["x=π/2", "x=π/4", "y=1"]),
        ("$\\csc(\\pi/2)$ equals:",
         "1", "$\\sin(\\pi/2)=1$.", ["0", "undefined", "-1"]),
        ("The range of $y=\\csc x$ is:",
         "(−∞, −1] ∪ [1, ∞)", "Same range idea as secant, from flipping sine.",
         ["[-1, 1]", "[0, 1]", "(−∞, ∞)"]),
        ("A local maximum of $y=\\csc x$ on $(0,2\\pi)$ occurs at:",
         "x=3π/2 with value −1", "Sine's minimum $-1$ flips to a cosecant local max of $-1$.",
         ["x=π/2 with value −1", "x=π with value 1", "x=0 with value 1"]),
        ("The period of $y=\\csc x$ is:",
         "2π", "Cosecant inherits sine's period.", ["π", "π/2", "4π"]),
        ("The period of $y=\\tan(2x)$ is:",
         "π/2", "Tangent period $\\pi/|B|=\\pi/2$.", ["π", "2π", "2"]),
        ("The period of $y=\\sec(3x)$ is:",
         "2π/3", "Secant uses $2\\pi/|B|$.", ["π/3", "3π", "2π"]),
        ("A vertical stretch of $y=\\tan x$ by $2$ is:",
         "y=2 tan x", "Multiply outputs by $2$. Asymptotes stay put.", ["y=tan(2x)", "y=tan x + 2", "y=2x"]),
        ("The phase shift of $y=\\tan(x-\\pi/4)$ is:",
         "right π/4", "Asymptotes move with the graph to $x=\\pi/4+\\pi/2=\\pi/4+2\\pi/4=3\\pi/4$, etc.",
         ["left π/4", "right π/2", "up π/4"]),
        ("Asymptotes of $y=\\tan(x-\\pi/4)$ nearest to the origin include:",
         "x=3π/4", "Parent asymptote $\\pi/2$ shifts right $\\pi/4$ to $3\\pi/4$. Also $-\\pi/4$ from $-\\pi/2+\\pi/4$.",
         ["x=π/2", "x=0", "x=π"]),
        ("The domain of $y=\\tan x$ excludes:",
         "odd multiples of π/2", "Where cosine is zero.", ["multiples of π", "even multiples of π/2", "all real numbers"]),
        ("The domain of $y=\\cot x$ excludes:",
         "integer multiples of π", "Where sine is zero.", ["odd multiples of π/2", "π/4 + kπ", "no values"]),
        ("The domain of $y=\\sec x$ is the same as the domain of:",
         "y=tan x", "Both fail where $\\cos x=0$.", ["y=sin x", "y=csc x", "y=cot x"]),
        ("Which $x$ in $[0,2\\pi]$ is missing from the domain of $y=\\csc x$?",
         "0, π, and 2π", "Sine zeros.", ["π/2 and 3π/2", "π/4 only", "none"]),
        ("On a graph of $y=\\sec x$, the gaps (open circles / asymptotes) occur at:",
         "x=π/2 + kπ", "Cosine zeros.", ["x=kπ", "x=π/4", "y=±1"]),
        ("$\\tan x$ is undefined at $x=3\\pi/2$ because:",
         "cos(3π/2)=0", "The denominator of sine/cosine vanishes.", ["sin(3π/2)=0", "the angle is negative", "3π/2 is not real"]),
        ("$y=\\cot(x/2)$ has period:",
         "2π", "Cotangent period $\\pi/|B|=\\pi/(1/2)=2\\pi$.", ["π", "4π", "π/2"]),
        ("A horizontal compression of $y=\\tan x$ by $1/2$ (period halved) is:",
         "y=tan(2x)", "$B=2$ halves the $\\pi$ period to $\\pi/2$.", ["y=2 tan x", "y=tan(x/2)", "y=tan x − 2"]),
        ("$\\sec x$ never takes the value:",
         "0", "The reciprocal of cosine cannot be $0$.", ["1", "-1", "2"]),
        ("$y=\\csc(x+\\pi/2)$ is identical to:",
         "y=sec x", "$\\sin(x+\\pi/2)=\\cos x$, so $\\csc(x+\\pi/2)=1/\\cos x=\\sec x$.",
         ["y=−sec x", "y=sin x", "y=csc x"]),
        ("The $x$-intercepts of $y=\\tan x$ on $(-\\pi/2,\\pi/2)$ occur at:",
         "x=0 only", "Tangent is zero where sine is zero and cosine is not: $x=0$ in that open interval.",
         ["x=±π/4", "x=π/2", "no intercepts"]),
        ("A graph of $y=2\\sec x$ has local min $2$ at $x=0$. That min value is:",
         "2", "Vertical stretch by $2$ sends the parent min $1$ to $2$.", ["1", "0", "1/2"]),
        ("Asymptotes of $y=\\csc(2x)$ on the open interval $(0,\\pi)$ include:",
         "x=π/2", "Sine of $2x$ is zero when $2x=k\\pi$, so $x=k\\pi/2$. The only such value strictly inside $(0,\\pi)$ is $x=\\pi/2$.",
         ["x=π/4", "x=π/6", "x=2π"]),
        ("Domain of $y=\\tan(x/2)$ excludes $x$ such that:",
         "x=π + 2πk", "$x/2=\\pi/2+k\\pi$, so $x=\\pi+2\\pi k$.", ["x=π/2 + kπ", "x=kπ", "x=2kπ"]),
        ("$y=\\cot x$ crosses the $x$-axis at:",
         "odd multiples of π/2", "Cotangent is zero where cosine is zero (and sine is not).",
         ["multiples of π", "π/4 + kπ", "never"]),
        ("Which function has period $\\pi$ rather than $2\\pi$?",
         "y=tan x", "Tangent and cotangent have period $\\pi$; sine, cosine, secant, cosecant have $2\\pi$.",
         ["y=sin x", "y=sec x", "y=csc x"]),
        ("The graph of $y=\\sec x$ between its asymptotes at $-\\pi/2$ and $\\pi/2$ looks like:",
         "a U-shape sitting on y=1", "It is the reciprocal of the top of cosine, opening upward from $(0,1)$.",
         ["a sine wave", "a line", "a parabola through the origin"]),
        ("If $y=\\tan(Bx)$ has period $\\pi/4$, then $B$ equals:",
         "4", "$\\pi/|B|=\\pi/4$ so $|B|=4$.", ["1/4", "π/4", "2"]),
        ("$y=-\\tan x$ compared with $y=\\tan x$ is:",
         "reflected across the x-axis", "Outputs change sign; asymptotes unchanged.",
         ["shifted left π", "period doubled", "undefined everywhere"]),
        ("A point on $y=\\csc x$ is $(\\pi/6, 2)$. That matches:",
         "csc(π/6)=2", "$\\sin(\\pi/6)=1/2$, reciprocal $2$.", ["sec(π/6)=2", "sin(π/6)=2", "csc(π/6)=1/2"]),
        ("Which $x$ is in the domain of both $\\tan x$ and $\\cot x$?",
         "π/4", "At $\\pi/4$ both sine and cosine are nonzero. At $0$ cotangent fails; at $\\pi/2$ tangent fails.",
         ["0", "π/2", "π"]),
        ("SAT Stretch: The first two positive vertical asymptotes of $y=\\cot(2x+\\pi/3)$ are at $x=$",
         "π/3 and 5π/6",
         "Cotangent is undefined when $2x+\\pi/3=k\\pi$, so $x=k\\pi/2-\\pi/6$. The first two positive values are $k=1,2$: $\\pi/3$ and $5\\pi/6$.",
         ["π/6 and π/3", "π/2 and π", "5π/12 and 11π/12"]),
        ("SAT Stretch: Domain of $y=\\sec(x-\\pi/4)$ in $[0,2\\pi)$ excludes:",
         "3π/4 and 7π/4", "Need $x-\\pi/4=\\pi/2+k\\pi$. For $k=0$, $x=3\\pi/4$. For $k=1$, $x=3\\pi/4+\\pi=7\\pi/4$.",
         ["π/4 and 5π/4", "0 and π", "π/2 and 3π/2"]),
        ("SAT Stretch: How many numbers in $(0,2\\pi)$ fail to lie in the domain of both $y=\\tan(2x)$ and $y=\\csc(x-\\pi/6)$?",
         "6",
         "$\\tan(2x)$ fails at $x=\\pi/4+k\\pi/2$ ($4$ values). $\\csc(x-\\pi/6)$ fails at $x=\\pi/6+k\\pi$ ($2$ values: $\\pi/6,7\\pi/6$). All six are distinct.",
         ["4", "2", "8"]),
        ("SAT Stretch: List every $x$ in $(0,2\\pi)$ that is missing from at least one of the domains of $y=\\sec(x-\\pi/6)$ and $y=\\tan(x/2)$.",
         "2π/3, π, 5π/3",
         "$\\sec(x-\\pi/6)$ fails when $x-\\pi/6=\\pi/2+k\\pi$, so $x=2\\pi/3$ and $5\\pi/3$. $\\tan(x/2)$ fails when $x/2=\\pi/2+k\\pi$, so $x=\\pi$ in this window. Union: $2\\pi/3,\\pi,5\\pi/3$.",
         ["2π/3 and 5π/3 only", "π/2 and 3π/2", "π only"]),
        ("SAT Stretch: The first positive vertical asymptote of $y=\\csc(2x+\\pi/4)$ is at $x=$",
         "3π/8",
         "Cosecant fails when $2x+\\pi/4=k\\pi$, so $x=k\\pi/2-\\pi/8$. The first positive value is $k=1$: $3\\pi/8$.",
         ["π/8", "π/4", "π/2"]),
        ("SAT Stretch: Consecutive vertical asymptotes of $y=\\cot(3x-\\pi/2)$ are one period apart. Locate two consecutive positive asymptotes and find that gap.",
         "π/3",
         "Undefined when $3x-\\pi/2=k\\pi$, so $x=k\\pi/3+\\pi/6$. Consecutive positives $k=0,1$ are $\\pi/6$ and $\\pi/2$, and $\\pi/2-\\pi/6=\\pi/3$.",
         ["π", "π/2", "π/6"]),
        ("SAT Stretch: All vertical asymptotes of $y=\\sec(x/2+\\pi/3)$ in $(0,4\\pi)$ occur at $x=$",
         "π/3 and 7π/3",
         "Secant fails when $x/2+\\pi/3=\\pi/2+k\\pi$, so $x=\\pi/3+2k\\pi$. Interior to $(0,4\\pi)$: $k=0,1$ give $\\pi/3$ and $7\\pi/3$ ($k=2$ is $13\\pi/3>4\\pi$).",
         ["π/3 only", "π/2 and 3π/2", "2π/3 and 8π/3"]),
        ("SAT Stretch: For $y=\\sec(2x)$, the first positive $x$ at which the graph has a local minimum of $1$ is:",
         "π", "Parent secant has a min of $1$ when the inside cosine is $1$, i.e. $2x=2\\pi k$, so $x=\\pi k$. The first positive value is $x=\\pi$.",
         ["0", "π/2", "π/4"]),
        ("SAT Stretch: On the interval $(\\pi/2, 3\\pi/2)$, the graph of $y=\\tan x$ consists of:",
         "two branches separated by a root at x=π",
         "Asymptotes sit at the odd multiples $\\pi/2$ and $3\\pi/2$. Between them, tangent has a zero at $x=\\pi$, so the picture is two increasing branches, not one continuous piece.",
         ["one continuous increasing piece", "undefined on the whole interval", "a cosine-shaped hill"]),
    ])


def build_unit4():
    title = "Trigonometry Unit 4: Tangent and Other Graphs"
    description = (
        "Tangent asymptotes, cotangent, secant, cosecant, transformations of those graphs, "
        "and reading domain from the pictures."
    )
    concepts = [
        "Tangent asymptotes",
        "Cotangent",
        "Secant",
        "Cosecant",
        "Transformations",
        "Domain from graphs",
    ]

    c1 = concept_block(
        "1. Tangent asymptotes",
        [
            "The parent tangent is $y=\\tan x=\\sin x/\\cos x$. It is undefined wherever cosine is zero: $x=\\pi/2+k\\pi$, the odd multiples of $\\pi/2$. "
            "Those vertical lines are asymptotes. The graph shoots up to $+\\infty$ on one side and down to $-\\infty$ on the other.",
            "Unlike sine and cosine, tangent has period $\\pi$. The piece on $(-\\pi/2,\\pi/2)$ already contains a full story: increasing through the origin from $-\\infty$ to $+\\infty$. "
            "Every other interval between consecutive asymptotes is a copy of that piece.",
            "Zeros of tangent occur where sine is zero and cosine is not: $x=k\\pi$. So the graph crosses the $x$-axis halfway between consecutive asymptotes.",
            "Because the period is $\\pi$, a sketch of one branch plus the two bounding asymptotes is enough. Then copy left and right.",
            "A calculator in degree mode will draw a wildly wrong tangent graph if you intended radians. The asymptote that should sit at about $1.57$ will appear near $90$ instead.",
            "Tangent is odd: $\\tan(-x)=-\\tan x$. Combined with the origin crossing, that is why the principal branch is symmetric through the origin.",
        ],
        "Secant shares these same asymptotes, and every tangent equation in Unit 7 is solved on one $\\pi$-period rather than a $2\\pi$-period. Seeing the asymptotes is seeing the domain.",
        "Draw the dashed lines $x=\\pi/2+k\\pi$ first. Then sketch an increasing branch through each midpoint zero $x=k\\pi$.",
        lesson_figure(
            _tan_graph(1, 0, a=-3.4, b=3.4),
            "Parent tangent $y=\\tan x$ with asymptotes at odd multiples of $\\pi/2$",
            "The curve is broken at $x=\\pm\\pi/2$ (and $\\pm 3\\pi/2$). Each connected piece increases through a zero at a multiple of $\\pi$.",
        )
        + solved(1, "Name the period of $y=\\tan x$ and the asymptotes in $(-\\pi,\\pi)$.",
                 ["Period $\\pi$.",
                  "Asymptotes at $x=-\\pi/2$ and $x=\\pi/2$ inside $(-\\pi,\\pi)$. (The lines $x=\\pm\\pi$ are zeros, not asymptotes.)"],
                 "period $\\pi$; asymptotes $x=\\pm\\pi/2$", "", "Easy")
        + solved(2, "Explain why $x=3\\pi/2$ is an asymptote of tangent.",
                 ["$\\cos(3\\pi/2)=0$ and $\\sin(3\\pi/2)=-1\\neq 0$.",
                  "The quotient $\\sin/\\cos$ has a nonzero numerator over a zero denominator, so the function has a vertical asymptote."],
                 "$x=3\\pi/2$ is an odd multiple of $\\pi/2$", "", "Medium")
        + solved(3, "Find the period and the first positive asymptote of $y=\\tan(2x)$.",
                 ["Period $\\pi/|B|=\\pi/2$.",
                  "Parent asymptote $\\pi/2$ becomes $2x=\\pi/2$, so $x=\\pi/4$.",
                  "Check: cosine of $2x$ is zero when $2x=\\pi/2+k\\pi$."],
                 "period $\\pi/2$, first positive asymptote $x=\\pi/4$", "", "Hard"),
        ("Thinking tangent has period $2\\pi$ like sine",
         "Sine and cosine need a full turn to repeat because of signs. Tangent's signs already match after a half-turn: $\\tan(x+\\pi)=\\tan x$. Using $2\\pi$ as the period is not false as a number that works, but it is not the fundamental period, and it will misplace landmarks."),
        ("Draw asymptotes before plotting any points",
         "If you plot $\\tan(1.5)$ without noticing $1.5$ is near $\\pi/2\\approx 1.57$, the enormous value looks like a mistake rather than the approach to an asymptote."),
        ["I can state that $y=\\tan x$ has period $\\pi$.",
         "I can name the asymptotes $x=\\pi/2+k\\pi$.",
         "I can sketch one increasing branch between consecutive asymptotes."],
        1,
    )

    c2 = concept_block(
        "2. Cotangent",
        [
            "Cotangent is $y=\\cot x=\\cos x/\\sin x=1/\\tan x$. Its asymptotes are the zeros of sine: $x=k\\pi$. "
            "Its zeros are the zeros of cosine: $x=\\pi/2+k\\pi$. Compared with tangent, zeros and asymptotes have swapped roles.",
            "The period is again $\\pi$. On $(0,\\pi)$ the graph decreases from $+\\infty$ (just after $x=0$) through $(\\pi/2,0)$ toward $-\\infty$ as $x$ approaches $\\pi$.",
            "The cofunction identity $\\cot x=\\tan(\\pi/2-x)$ says cotangent is a reflected and shifted tangent. "
            "You can sketch it by flipping a tangent branch and sliding, or by plotting the three landmarks: left asymptote, intercept, right asymptote.",
            "At $x=\\pi/4$, $\\cot=1$. At $x=3\\pi/4$, $\\cot=-1$. Those two points plus the intercept at $\\pi/2$ already shape the main branch.",
            "Undefined at $0$ is the feature students forget when they copy a tangent graph and merely flip it without moving the asymptotes.",
            "Like tangent, cotangent is odd. The principal decreasing branch on $(0,\\pi)$ is the one used to define $\\mathrm{arccot}$ in some textbooks, though calculator conventions vary — we only need the graph here.",
        ],
        "Cotangent shows up in identities ($1+\\cot^2=\\csc^2$) and in some polar and calculus limits. Its graph is the picture of those domain restrictions.",
        "Swap the asymptotes and zeros of tangent, then sketch a decreasing branch. Period stays $\\pi$.",
        lesson_figure(
            _cot_graph(),
            "Parent cotangent $y=\\cot x$ with asymptotes at multiples of $\\pi$",
            "Dashed verticals sit at $x=0,\\pm\\pi,\\ldots$. Each branch decreases through a zero at odd multiples of $\\pi/2$.",
        )
        + solved(4, "Name the asymptotes of $y=\\cot x$ in $[-\\pi,\\pi]$.",
                 ["Sine is zero at $-\\pi,0,\\pi$.",
                  "Those three lines are the asymptotes in the closed interval (the endpoints included as asymptotes)."],
                 "$x=-\\pi,0,\\pi$", "", "Easy")
        + solved(5, "Evaluate $\\cot(\\pi/4)$ and $\\cot(3\\pi/4)$.",
                 ["$\\cot(\\pi/4)=1$.",
                  "$\\cot(3\\pi/4)=\\cos(3\\pi/4)/\\sin(3\\pi/4)=(-\\sqrt{2}/2)/(\\sqrt{2}/2)=-1$."],
                 "$1$ and $-1$", "", "Medium")
        + solved(6, "Find the period and the first positive asymptote of $y=\\cot(x/2)$.",
                 ["Period $\\pi/|B|=\\pi/(1/2)=2\\pi$.",
                  "Asymptotes when $x/2=k\\pi$, so $x=2k\\pi$. First positive: $x=2\\pi$.",
                  "Note that $x=0$ is an asymptote but not positive."],
                 "period $2\\pi$, first positive asymptote $x=2\\pi$", "", "Hard"),
        ("Placing cotangent's asymptotes at $\\pi/2$",
         "That is tangent's pattern. Cotangent blows up where sine is zero, i.e. at multiples of $\\pi$, including the $y$-axis."),
        ("Remember: cotangent decreases on $(0,\\pi)$",
         "If your sketch increases through $\\pi/2$, you drew tangent on the wrong window or forgot the reciprocal flip."),
        ["I can name cotangent's period and asymptotes.",
         "I can evaluate cotangent at special angles.",
         "I can transform the period with $B$."],
        6,
    )

    c3 = concept_block(
        "3. Secant",
        [
            "Secant is $y=\\sec x=1/\\cos x$. Draw cosine first, then take reciprocals of the $y$-values. "
            "Where cosine has a peak of $1$, secant has a U sitting on $y=1$. Where cosine has a trough of $-1$, secant has an upside-down U hanging from $y=-1$.",
            "Where cosine is zero, secant has vertical asymptotes — the same lines as tangent: $x=\\pi/2+k\\pi$. "
            "Between those asymptotes, secant never enters the open interval $(-1,1)$. Its range is $(-\\infty,-1]\\cup[1,\\infty)$.",
            "The period is $2\\pi$, like cosine, because the pattern of U, gap, inverted U, gap needs a full turn to repeat (the two U's have opposite orientation).",
            "A local minimum of $1$ occurs at $x=2\\pi k$. A local maximum of $-1$ occurs at $x=\\pi+2\\pi k$. "
            "Those are not the same as sine's max/min locations.",
            "Secant is even, because cosine is even. The graph is symmetric about the $y$-axis.",
            "When you transform secant, transform the hidden cosine first, then take reciprocals. Asymptotes move with the zeros of the inner cosine.",
        ],
        "Secant's graph is the visual reason $\\sec x$ never equals $1/2$. Domain and range questions on tests are this picture in words.",
        "Sketch $y=\\cos x$ faintly. Reciprocate the values. Draw dashed lines through cosine's zeros. The U's cannot cross $y=\\pm 1$ toward zero.",
        lesson_figure(
            _sec_graph(),
            "Parent secant $y=\\sec x$ as the reciprocal of cosine",
            "U-shaped branches live outside $[-1,1]$, separated by the same vertical asymptotes as tangent. The curve never crosses the open strip $-1<y<1$.",
        )
        + solved(7, "State the range of $y=\\sec x$.",
                 ["Cosine outputs lie in $[-1,1]$.",
                  "Reciprocals of numbers in $[-1,1]\\setminus\\{0\\}$ lie in $(-\\infty,-1]\\cup[1,\\infty)$."],
                 "$(-\\infty,-1]\\cup[1,\\infty)$", "", "Easy")
        + solved(8, "Where are the asymptotes of $y=\\sec x$ on $[0,2\\pi]$?",
                 ["Cosine is zero at $\\pi/2$ and $3\\pi/2$."],
                 "$x=\\pi/2$ and $x=3\\pi/2$", "", "Medium")
        + solved(9, "Find the period and the first positive asymptote of $y=\\sec(2x)$.",
                 ["Period $2\\pi/2=\\pi$.",
                  "Asymptotes when $\\cos(2x)=0$, i.e. $2x=\\pi/2+k\\pi$, $x=\\pi/4+k\\pi/2$.",
                  "First positive: $x=\\pi/4$."],
                 "period $\\pi$, first positive asymptote $x=\\pi/4$", "", "Hard"),
        ("Letting secant wiggle between $-1$ and $1$ like cosine",
         "Reciprocals of numbers smaller than $1$ in absolute value are larger than $1$ in absolute value. Secant is banished from $(-1,1)$."),
        ("Draw cosine first, even on scratch paper",
         "The reciprocal picture is almost impossible to invent from memory without the cosine underneath as a guide."),
        ["I can state secant's range and period.",
         "I can locate secant asymptotes as cosine zeros.",
         "I can describe the U and inverted-U branches."],
        11,
    )

    c4 = concept_block(
        "4. Cosecant",
        [
            "Cosecant is $y=\\csc x=1/\\sin x$. The recipe is the same as secant, with sine underneath instead of cosine. "
            "Asymptotes sit at $x=k\\pi$. U-shaped branches sit on $y=1$ at $x=\\pi/2+2\\pi k$ and hang from $y=-1$ at $x=3\\pi/2+2\\pi k$.",
            "Range is again $(-\\infty,-1]\\cup[1,\\infty)$. Period is $2\\pi$. Cosecant is odd, matching sine.",
            "A phase identity connects the two reciprocal waves: $\\csc(x+\\pi/2)=\\sec x$. "
            "Shifting the cosecant graph left by $\\pi/2$ produces secant.",
            "On $(0,\\pi)$ you see a single U sitting on $(\\pi/2,1)$, with asymptotes at $0$ and $\\pi$. "
            "That is the most common window drawn in textbooks.",
            "Undefined at $0$ means the $y$-axis is an asymptote. Do not plot a point at the origin.",
            "Transformations follow $y=A\\csc(B(x-h))+D$, but $D$ can be confusing because the range is no longer symmetric about $D$ in a simple $[-1,1]$ way. "
            "In this course we mainly stretch, compress, and shift horizontally, and we read domain from the moved asymptotes.",
        ],
        "Cosecant is how $1/\\sin x$ behaves near its poles — the same poles that make cotangent undefined. Seeing both graphs together locks the $x=k\\pi$ family in memory.",
        "Sketch $y=\\sin x$ faintly. Reciprocate. Dashed lines through sine's zeros. U on each positive hump, inverted U on each negative hump.",
        lesson_figure(
            _csc_graph(),
            "Parent cosecant $y=\\csc x$ as the reciprocal of sine",
            "Asymptotes at multiples of $\\pi$. A U sits on $(\\pi/2,1)$; an inverted U hangs from $(3\\pi/2,-1)$.",
        )
        + solved(10, "Evaluate $\\csc(\\pi/2)$ and $\\csc(3\\pi/2)$.",
                 ["$\\csc(\\pi/2)=1/1=1$.",
                  "$\\csc(3\\pi/2)=1/(-1)=-1$."],
                 "$1$ and $-1$", "", "Easy")
        + solved(11, "Name the asymptotes of $y=\\csc x$ on $[0,2\\pi]$.",
                 ["Sine is zero at $0$, $\\pi$, and $2\\pi$."],
                 "$x=0,\\pi,2\\pi$", "", "Medium")
        + solved(12, "Find the first positive $x$ where $y=\\csc(x-\\pi/6)$ has an asymptote.",
                 ["Asymptotes when the inside sine is zero: $x-\\pi/6=k\\pi$.",
                  "For $k=0$, $x=\\pi/6$, which is positive.",
                  "So the first positive asymptote is $x=\\pi/6$."],
                 "$x=\\pi/6$", "The parent $y$-axis asymptote slid right by $\\pi/6$.", "Hard"),
        ("Drawing a cosecant blob through the origin",
         "Sine is zero at the origin, so cosecant cannot have a point there. The $y$-axis is a barrier, not a crossing."),
        ("Match U's to the sign of sine, not to quadrant names in isolation",
         "Wherever sine is positive, the reciprocal U opens up above $y=1$. Wherever sine is negative, the inverted U lives below $y=-1$."),
        ["I can state cosecant's range, period, and asymptotes.",
         "I can evaluate csc at $\\pi/2$ and $3\\pi/2$.",
         "I can shift the asymptotes with a phase $h$."],
        16,
    )

    c5 = concept_block(
        "5. Transformations",
        [
            "The four functions transform like sine and cosine, with two important differences. "
            "Tangent and cotangent use period $\\pi/|B|$ rather than $2\\pi/|B|$. Secant and cosecant use $2\\pi/|B|$.",
            "A vertical stretch $y=A\\tan x$ multiplies outputs but does not move asymptotes. "
            "A horizontal change $y=\\tan(Bx)$ does move asymptotes: solve $Bx=\\pi/2+k\\pi$.",
            "Phase shift: factor $B(x-h)$ the same way as in Unit 3. For $y=\\tan(2x-\\pi/3)$, write $2\\big(x-\\pi/6\\big)$ and slide every parent feature right by $\\pi/6$.",
            "Vertical shift $D$ on tangent slides the whole branch up, including the zero, but the vertical asymptotes stay vertical and unmoved (unless a phase is also present). "
            "The graph no longer crosses $y=0$ at $x=k\\pi$; it crosses $y=D$ there.",
            "For secant and cosecant, a vertical stretch changes the 'keep-out' strip: $y=2\\sec x$ never enters $(-2,2)$. "
            "A vertical shift $y=\\sec x+3$ moves that picture up $3$, so the keep-out strip becomes $(2,4)$ in the middle of the range — more awkward, which is why tests usually skip $D$ on sec/csc.",
            "Always move the asymptotes first when $B$ or $h$ changes. The curve is then sketched in the windows the asymptotes create.",
        ],
        "A transformed tangent is the usual SAT graph that looks nothing like a wave. If you treat it like sine (period $2\\pi$, no asymptotes), every landmark is wrong.",
        "Compute the new period with the correct parent period ($\\pi$ vs $2\\pi$). Solve for the new asymptotes. Then stretch and shift the branch inside each window.",
        lesson_figure(
            _tan_graph(2, math.pi / 3, a=-1.2, b=2.2),
            "$y=\\tan(2x-\\pi/3)$: period $\\pi/2$, first positive asymptote $x=5\\pi/12$",
            "Factor $2(x-\\pi/6)$. Parent asymptote $\\pi/2$ moves to $2x-\\pi/3=\\pi/2$, hence $x=5\\pi/12$. The drawn curve breaks at those dashed lines.",
        )
        + solved(13, "Find the period of $y=\\tan(3x)$.",
                 ["$\\pi/|B|=\\pi/3$."],
                 "$\\pi/3$", "", "Easy")
        + solved(14, "Find the period of $y=2\\sec(x/2)$.",
                 ["Secant uses $2\\pi/|B|=2\\pi/(1/2)=4\\pi$.",
                  "The $2$ is a vertical stretch and does not change period."],
                 "$4\\pi$", "", "Medium")
        + solved(15, "Find the first positive asymptote of $y=\\tan(2x-\\pi/3)$.",
                 ["Set $2x-\\pi/3=\\pi/2$.",
                  "$2x=\\pi/2+\\pi/3=5\\pi/6$.",
                  "$x=5\\pi/12$."],
                 "$x=5\\pi/12$", "Check it is positive and that cosine of the inside is zero there.", "Hard"),
        ("Using $2\\pi/B$ as the period of $y=\\tan(Bx)$",
         "Tangent's parent period is $\\pi$. The compressed period is $\\pi/|B|$. Using $2\\pi$ doubles every window and inserts fake extra branches."),
        ("Move asymptotes with $B$ and $h$ before stretching vertically",
         "Vertical stretches never free a forbidden $x$-value. If $x=\\pi/2$ was undefined for $\\tan x$, it is still undefined for $5\\tan x$."),
        ["I can compute periods of tan/cot vs sec/csc after a $B$ change.",
         "I can locate transformed asymptotes by solving the inside $=\\pi/2+k\\pi$ or $=k\\pi$.",
         "I know vertical stretches do not move vertical asymptotes."],
        21,
    )

    c6 = concept_block(
        "6. Domain from graphs",
        [
            "The domain of a trig graph is all real $x$ except the vertical asymptotes you can see (and the ones implied by periodicity). "
            "Reading domain from a graph means naming those excluded $x$-values as an arithmetic sequence.",
            "For $y=\\tan x$ and $y=\\sec x$, exclude $x=\\pi/2+k\\pi$. For $y=\\cot x$ and $y=\\csc x$, exclude $x=k\\pi$. "
            "After a transformation $B(x-h)$, solve the corresponding inside equation.",
            "A graph might show only two dashed lines in a window. Your domain statement still has to include all congruent copies: '...for all integers $k$'.",
            "Open circles at a finite $y$-value are not the usual picture for these four functions — they have infinite blow-ups, not removable holes. "
            "If you see a hole, something else (a cancelled factor) is going on; that is not parent tan/sec/csc/cot.",
            "When two functions are multiplied or composed, the domain is the intersection of the individual domains. "
            "$y=\\tan x\\cot x$ looks like $1$ but is still undefined at both families of asymptotes, because neither factor is defined there.",
            "On a test, match the dashed lines in the figure to an excluded-list choice. If the figure is $y=\\tan(x/2)$, the dashes are twice as far apart as parent tangent's, matching $x=\\pi+2\\pi k$.",
        ],
        "Domain is the difference between a legal equation solution and a phantom one. Unit 7 will discard answers that land on these dashed lines.",
        "Identify the function family from the picture (wave vs U vs increasing branch). Write the parent excluded set. Adjust with $B$ and $h$.",
        lesson_figure(
            _tan_graph(1, 0, a=-3.5, b=3.5),
            "Domain of $y=\\tan x$ is all reals except the dashed lines",
            "Each dashed vertical is an odd multiple of $\\pi/2$. The domain is $\\{x\\mid x\\neq \\pi/2+k\\pi,\\,k\\in\\mathbb{Z}\\}$.",
        )
        + solved(16, "Write the domain of $y=\\tan x$.",
                 ["Exclude odd multiples of $\\pi/2$.",
                  "Domain: $x\\neq\\pi/2+k\\pi$ for integers $k$."],
                 "$x\\neq\\pi/2+k\\pi$", "", "Easy")
        + solved(17, "Write the domain of $y=\\csc(x-\\pi/4)$.",
                 ["Parent csc excludes $k\\pi$.",
                  "Set $x-\\pi/4=k\\pi$, so $x=\\pi/4+k\\pi$.",
                  "Domain: $x\\neq\\pi/4+k\\pi$."],
                 "$x\\neq\\pi/4+k\\pi$", "", "Medium")
        + solved(18, "Write the domain of $y=\\sec(2x)$.",
                 ["Parent sec excludes $\\pi/2+k\\pi$.",
                  "$2x=\\pi/2+k\\pi$, so $x=\\pi/4+k\\pi/2$.",
                  "Domain: $x\\neq\\pi/4+k\\pi/2$."],
                 "$x\\neq\\pi/4+k\\pi/2$", "The excluded points are twice as dense as parent secant's, matching period $\\pi$.", "Hard"),
        ("Writing 'all real numbers' because the curve is drawn with gaps you ignored",
         "Dashed lines are not decorative. Every dashed $x$ is missing from the domain, even if the printer made the dash faint."),
        ("Solve the inside equation; do not just copy the parent exclusions",
         "After a horizontal stretch, the forbidden list changes. $y=\\tan(2x)$ is undefined at $x=\\pi/4+k\\pi/2$, not at $x=\\pi/2+k\\pi$."),
        ["I can write domain exclusions as $x\\neq$ an arithmetic sequence.",
         "I can adjust that sequence after a $B$ or $h$ transformation.",
         "I can intersect domains when two trig functions are combined."],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
        stretch_note=STRETCH_LABEL,
    )
    return title, description, content, _u4_questions()
