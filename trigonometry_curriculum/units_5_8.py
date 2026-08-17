#!/usr/bin/env python3
"""Trigonometry units 5–8: identities, multiple-angle, inverse equations, laws of sines/cosines."""
from __future__ import annotations

import math

from curriculum_kit import lesson_figure, svg_circle, svg_triangle

from hs_curriculum import (
    concept_block,
    labeled_right_triangle,
    mq,
    page_break,
    practice_slots,
    sample_curve,
    solved,
    unit_circle_svg,
    unit_shell,
    xy_graph,
)
from .common import AUDIENCE, STRETCH_LABEL
from .units_1_4 import _acute_rt, _pack, _sin_graph


def _pythag_circle(deg=60, w=280):
    """Unit circle with the right triangle that shows sin²+cos²=1."""
    pad, r = 28, (w - 56) / 2
    cx = cy = w / 2
    th = math.radians(deg)
    px = cx + r * math.cos(th)
    py = cy - r * math.sin(th)
    qx = px
    qy = cy
    return (
        f'<svg viewBox="0 0 {w} {w}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#f8fafc" stroke="#0f172a" stroke-width="1.8"/>'
        f'<line x1="{cx - r}" y1="{cy}" x2="{cx + r}" y2="{cy}" stroke="#0f172a" stroke-width="1.2"/>'
        f'<line x1="{cx}" y1="{cy - r}" x2="{cx}" y2="{cy + r}" stroke="#0f172a" stroke-width="1.2"/>'
        f'<polygon points="{cx},{cy} {px:.1f},{py:.1f} {qx:.1f},{qy:.1f}" fill="#e0e7ff" fill-opacity="0.7" stroke="#312e81" stroke-width="2"/>'
        f'<line x1="{cx}" y1="{cy}" x2="{px:.1f}" y2="{py:.1f}" stroke="#dc2626" stroke-width="2"/>'
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="#dc2626"/>'
        f'<text x="{(cx + qx) / 2:.1f}" y="{cy + 16}" text-anchor="middle" font-size="12">cos</text>'
        f'<text x="{px + 10:.1f}" y="{(cy + py) / 2:.1f}" font-size="12">sin</text>'
        f'<text x="{px + 8:.1f}" y="{py - 8:.1f}" font-size="12" fill="#b91c1c">hyp 1</text>'
        f"</svg>"
    )


def _ssa_two():
    """Ambiguous SSA: two possible locations for the third vertex."""
    return (
        '<svg viewBox="0 0 420 210" width="100%" style="max-width:420px" role="img">'
        '<line x1="40" y1="180" x2="380" y2="180" stroke="#0f172a" stroke-width="2"/>'
        '<polygon points="40,180 300,180 140,50" fill="#c7d2fe" fill-opacity="0.55" stroke="#312e81" stroke-width="2.2"/>'
        '<polygon points="40,180 300,180 250,70" fill="#fde68a" fill-opacity="0.4" stroke="#b45309" stroke-width="2" stroke-dasharray="7 4"/>'
        '<text x="28" y="176" font-size="13" fill="#b91c1c">A</text>'
        '<text x="308" y="176" font-size="13">B</text>'
        '<text x="132" y="42" font-size="13" fill="#312e81">C</text>'
        '<text x="258" y="62" font-size="13" fill="#b45309">C′</text>'
        '<text x="88" y="120" font-size="12">a</text>'
        '<text x="210" y="198" font-size="12">c (side b in some books)</text>'
        '<text x="50" y="168" font-size="12" fill="#b91c1c">angle A given</text>'
        "</svg>"
    )


def _aas_pair():
    """Two similar-looking acute triangles for AAS/ASA (law of sines)."""
    return (
        '<svg viewBox="0 0 400 180" width="100%" style="max-width:400px" role="img">'
        '<polygon points="30,150 190,150 80,40" fill="#eef2ff" stroke="#312e81" stroke-width="2"/>'
        '<polygon points="230,150 380,150 300,45" fill="#fef3c7" stroke="#92400e" stroke-width="2"/>'
        '<text x="22" y="148" font-size="12">A</text>'
        '<text x="196" y="148" font-size="12">B</text>'
        '<text x="72" y="34" font-size="12">C</text>'
        '<text x="110" y="168" font-size="12">c</text>'
        '<text x="248" y="168" font-size="12">known side</text>'
        '<text x="222" y="148" font-size="12">A</text>'
        '<text x="386" y="148" font-size="12">B</text>'
        '<text x="292" y="38" font-size="12">C</text>'
        "</svg>"
    )


def _bearing_svg():
    return (
        '<svg viewBox="0 0 260 260" width="100%" style="max-width:240px" role="img">'
        '<circle cx="130" cy="130" r="90" fill="#f8fafc" stroke="#0f172a" stroke-width="1.6"/>'
        '<line x1="130" y1="30" x2="130" y2="230" stroke="#0f172a" stroke-width="1.3"/>'
        '<line x1="40" y1="130" x2="220" y2="130" stroke="#0f172a" stroke-width="1.3"/>'
        '<line x1="130" y1="130" x2="175" y2="52" stroke="#dc2626" stroke-width="2.4"/>'
        '<text x="122" y="24" font-size="13">N</text>'
        '<text x="226" y="134" font-size="13">E</text>'
        '<text x="122" y="248" font-size="13">S</text>'
        '<text x="18" y="134" font-size="13">W</text>'
        '<text x="160" y="88" font-size="12" fill="#b91c1c">N 30° E</text>'
        "</svg>"
    )


def _heron_tri():
    return (
        '<svg viewBox="0 0 280 180" width="100%" style="max-width:280px" role="img">'
        '<polygon points="40,150 250,150 150,30" fill="#dcfce7" stroke="#166534" stroke-width="2"/>'
        '<text x="145" y="168" text-anchor="middle" font-size="13">c = 14</text>'
        '<text x="18" y="95" font-size="13">b = 13</text>'
        '<text x="210" y="90" font-size="13">a = 15</text>'
        '<text x="145" y="110" text-anchor="middle" font-size="12">s = 21</text>'
        "</svg>"
    )


# ===========================================================================
# UNIT 5: Identities
# ===========================================================================

def _u5_questions():
    return _pack([
        ("The Pythagorean identity states that $\\sin^2\\theta+\\cos^2\\theta$ equals:",
         "1", "This is $x^2+y^2=1$ on the unit circle.", ["0", "tan²θ", "sec²θ"]),
        ("$1+\\tan^2\\theta$ is identically:",
         "sec²θ", "Divide $\\sin^2+\\cos^2=1$ by $\\cos^2\\theta$.", ["csc²θ", "cot²θ", "1"]),
        ("$1+\\cot^2\\theta$ is identically:",
         "csc²θ", "Divide the fundamental identity by $\\sin^2\\theta$.", ["sec²θ", "tan²θ", "1"]),
        ("If $\\cos\\theta=3/5$ and $\\theta$ is acute, $\\sin\\theta$ equals:",
         "4/5", "$\\sin^2=1-9/25=16/25$, and QI takes the positive root.", ["3/5", "3/4", "5/3"]),
        ("$\\sin^2\\theta$ can be rewritten as:",
         "1 − cos²θ", "Solve the Pythagorean identity for sine squared.", ["1 + cos²θ", "sec²θ − 1", "tan²θ"]),
        ("Sine is an odd function, so $\\sin(-\\theta)$ equals:",
         "−sin θ", "The unit-circle $y$-coordinate changes sign under a clockwise angle.", ["sin θ", "cos θ", "−cos θ"]),
        ("Cosine is even, so $\\cos(-\\theta)$ equals:",
         "cos θ", "The $x$-coordinate is unchanged by reflecting the angle.", ["−cos θ", "sin θ", "−sin θ"]),
        ("$\\tan(-\\theta)$ equals:",
         "−tan θ", "Odd over even is odd: $(-\\sin)/\\cos$.", ["tan θ", "cot θ", "1/tan θ"]),
        ("The cofunction identity $\\sin\\theta=\\cos(?)$ is completed by:",
         "π/2 − θ", "$\\sin\\theta=\\cos(\\pi/2-\\theta)$.", ["θ", "π − θ", "π/2 + θ"]),
        ("$\\cos(\\pi/2-\\theta)$ equals:",
         "sin θ", "Cofunction pair.", ["cos θ", "−sin θ", "sec θ"]),
        ("The quotient identity for tangent is:",
         "sin θ / cos θ", "Definition on the unit circle $y/x$.", ["cos θ / sin θ", "1/sin θ", "sec θ / csc θ"]),
        ("$\\cot\\theta$ equals which quotient?",
         "cos θ / sin θ", "Reciprocal of tangent, or $x/y$.", ["sin θ / cos θ", "1/cos θ", "sin θ cos θ"]),
        ("$\\tan\\theta\\cos\\theta$ simplifies to:",
         "sin θ", "$(\\sin/\\cos)\\cdot\\cos=\\sin$, where cosine is nonzero.", ["cos θ", "1", "sec θ"]),
        ("$\\sec\\theta\\sin\\theta/\\tan\\theta$ simplifies to:",
         "1", "$(1/\\cos)\\cdot\\sin\\cdot(\\cos/\\sin)=1$.", ["tan θ", "sin θ", "0"]),
        ("$\\frac{\\sin\\theta}{\\csc\\theta}$ equals:",
         "sin²θ", "$\\sin/(1/\\sin)=\\sin^2$.", ["1", "csc²θ", "tan θ"]),
        ("Simplify $(1-\\cos^2\\theta)/\\sin\\theta$ for $\\sin\\theta\\neq 0$:",
         "sin θ", "$1-\\cos^2=\\sin^2$, then $\\sin^2/\\sin=\\sin$.", ["cos θ", "tan θ", "csc θ"]),
        ("Simplify $\\sec^2\\theta-1$:",
         "tan²θ", "Rearrange $1+\\tan^2=\\sec^2$.", ["cot²θ", "csc²θ", "1"]),
        ("Simplify $\\frac{1+\\tan^2\\theta}{\\sec\\theta}$:",
         "sec θ", "Numerator is $\\sec^2$, so $\\sec^2/\\sec=\\sec$.", ["cos θ", "tan θ", "1"]),
        ("Simplify $\\sin\\theta\\cot\\theta$:",
         "cos θ", "$\\sin\\cdot(\\cos/\\sin)=\\cos$.", ["sin θ", "tan θ", "1"]),
        ("Simplify $\\frac{\\csc\\theta}{\\cot\\theta}$:",
         "sec θ", "$(1/\\sin)/(\\cos/\\sin)=1/\\cos=\\sec$.", ["sin θ", "cos θ", "tan θ"]),
        ("To verify $\\tan\\theta\\sin\\theta=\\sec\\theta-\\cos\\theta$, a first step is to write the right side as:",
         "(1 − cos²θ)/cos θ", "$\\sec-\\cos=1/\\cos-\\cos=(1-\\cos^2)/\\cos=\\sin^2/\\cos$, which equals $\\tan\\sin$.",
         ["sin θ", "1 + cos θ", "tan²θ"]),
        ("Both sides of $\\sin^2\\theta+\\cos^2\\theta=1$ equal $1$ at $\\theta=\\pi/6$. That check:",
         "supports but does not finish a general verification", "Identities must hold for all legal θ, not one number.",
         ["proves the identity completely", "disproves the identity", "is illegal"]),
        ("A legal first move when verifying is:",
         "rewrite everything in sine and cosine", "Then cancel using Pythagorean facts. Do not divide both sides by an expression that might be zero until you track domain.",
         ["cancel sin θ from both sides immediately always", "replace θ by 90° only", "take arctan of both sides"]),
        ("If the left side becomes $\\frac{\\sin^2\\theta}{\\cos^2\\theta}$ and the right side is $\\tan^2\\theta$, the identity:",
         "checks out", "Those are equal by the quotient identity.", ["fails", "needs a plus 1", "only works in QI"]),
        ("When verifying, moving terms across the equals sign:",
         "is allowed if you treat it as an equation you are testing, but the safer habit is to transform one side only",
         "Standard instruction: start with the more complicated side and morph it into the other.",
         ["is the only legal method", "is never allowed", "requires multiplying by zero"]),
        ("Rewrite $\\sin^2\\theta=3\\cos^2\\theta$ as an equation in tangent by dividing by $\\cos^2\\theta$ (where defined). You get:",
         "tan²θ = 3", "$\\sin^2/\\cos^2=3$.", ["tan θ = 3", "sin θ = 3", "sec²θ = 3"]),
        ("Rewrite $2\\sin\\theta=\\cos\\theta$ in terms of tangent:",
         "tan θ = 1/2", "Divide by $\\cos\\theta$: $2\\tan\\theta=1$.", ["tan θ = 2", "tan θ = 1", "cot θ = 1/2"]),
        ("An equation $\\sec^2\\theta=4$ becomes, after a Pythagorean rewrite:",
         "1 + tan²θ = 4", "Then $\\tan^2\\theta=3$.", ["sin²θ = 4", "cos²θ = 4", "tan θ = 4"]),
        ("To solve $\\sin\\theta=\\cos\\theta$ on a domain where cosine is nonzero, divide to get:",
         "tan θ = 1", "Then $\\theta=\\pi/4+k\\pi$.", ["sin θ = 1", "θ = 0", "cos θ = 0"]),
        ("$1-\\sin^2\\theta$ is a rewrite of:",
         "cos²θ", "Pythagorean rearrangement.", ["sin²θ", "tan²θ", "1"]),
        ("If $\\tan\\theta=5/12$ and $\\theta$ is in QI, $\\sec\\theta$ equals:",
         "13/12", "A $5$-$12$-$13$ triangle: hyp $13$, adj $12$.", ["12/13", "13/5", "5/13"]),
        ("$\\cos^2\\theta-\\sin^2\\theta$ is also:",
         "cos(2θ)", "Double-angle, but it is still a Pythagorean-style rewrite used in identities.", ["1", "sin(2θ)", "tan²θ"]),
        ("$\\sin(-\\pi/3)$ equals:",
         "−√3/2", "Oddness: $-\\sin(\\pi/3)$.", ["√3/2", "-1/2", "1/2"]),
        ("$\\cos(-\\pi/4)$ equals:",
         "√2/2", "Evenness: $\\cos(\\pi/4)$.", ["-√2/2", "1", "0"]),
        ("Simplify $\\frac{1-\\sin^2\\theta}{\\cos\\theta}$ for $\\cos\\theta\\neq 0$:",
         "cos θ", "$(1-\\sin^2)/\\cos=\\cos^2/\\cos=\\cos$.", ["sin θ", "sec θ", "1"]),
        ("$\\tan\\theta+\\cot\\theta$ equals:",
         "sec θ csc θ", "Common denominator $\\sin\\cos$ yields $(\\sin^2+\\cos^2)/(\\sin\\cos)=1/(\\sin\\cos)=\\sec\\csc$.",
         ["1", "2", "tan θ"]),
        ("Which is NOT an identity?",
         "sin θ = 1 − cos θ", "False in general (try $\\theta=0$: $0=0$ works, but $\\theta=\\pi/2$: $1=1-0$ works? $1=1$. Try $\\theta=\\pi/6$: $1/2=1-\\sqrt{3}/2$, false).",
         ["sin²θ + cos²θ = 1", "1 + tan²θ = sec²θ", "tan θ = sin θ / cos θ"]),
        ("$\\sec(-\\theta)$ equals:",
         "sec θ", "Even, because cosine is even.", ["−sec θ", "csc θ", "cos θ"]),
        ("If $\\sin\\theta=-3/5$ and $\\theta$ is in QIII, $\\cos\\theta$ equals:",
         "−4/5", "Pythagoras gives $\\pm 4/5$; QIII forces cosine negative.", ["4/5", "3/5", "-3/4"]),
        ("Simplify $(\\sec\\theta-1)(\\sec\\theta+1)$:",
         "tan²θ", "Difference of squares: $\\sec^2-1=\\tan^2$.", ["sec²θ", "1", "cot²θ"]),
        ("$\\frac{\\cos\\theta}{\\sin\\theta}+\\frac{\\sin\\theta}{\\cos\\theta}$ equals:",
         "sec θ csc θ", "Same as $\\cot+\\tan=1/(\\sin\\cos)$.", ["1", "2", "tan θ"]),
        ("A cofunction rewrite of $\\tan(90^\\circ-\\theta)$ is:",
         "cot θ", "Standard cofunction.", ["tan θ", "−tan θ", "sec θ"]),
        ("$\\sin\\theta\\sec\\theta$ simplifies to:",
         "tan θ", "$\\sin\\cdot(1/\\cos)=\\tan$.", ["cos θ", "1", "sin θ"]),
        ("To turn $2\\cos^2\\theta=1$ into a tangent equation, use $\\cos^2=1/(1+\\tan^2)$. Then $2/(1+\\tan^2)=1$, so:",
         "tan²θ = 1", "$1+\\tan^2=2$.", ["tan θ = 2", "tan²θ = 2", "tan²θ = 0"]),
        ("$1-\\sec^2\\theta$ equals:",
         "−tan²θ", "From $1+\\tan^2=\\sec^2$.", ["tan²θ", "cot²θ", "1"]),
        ("If $\\cot\\theta=3/4$ in QI, $\\sin\\theta$ equals:",
         "4/5", "Adj $3$, opp $4$, hyp $5$.", ["3/5", "3/4", "5/4"]),
        ("SAT Stretch: $\\sin\\theta=-5/13$ and $\\theta$ is in QIII. Find $\\tan\\theta+\\sec\\theta$.",
         "-2/3", "QIII: $\\cos\\theta=-12/13$ from a $5$-$12$-$13$ triangle. Then $\\tan\\theta=5/12$ and $\\sec\\theta=-13/12$, so $5/12-13/12=-2/3$.",
         ["1/6", "2/3", "18/12"]),
        ("SAT Stretch: $\\tan\\theta=-5/12$ in QIV. Find $\\csc\\theta+\\cot\\theta$.",
         "-5",
         "Hypotenuse $13$. QIV: $\\sin=-5/13$, $\\cos=12/13$. Then $\\csc=-13/5$ and $\\cot=-12/5$, sum $-25/5=-5$.",
         ["5", "13/5", "-1"]),
        ("SAT Stretch: Simplify $\\frac{\\tan\\theta}{\\sec\\theta-1}\\cdot\\frac{\\sec\\theta+1}{\\sec\\theta+1}$ to a single function (where defined):",
         "csc θ + cot θ",
         "Multiply numerator and denominator by $\\sec+1$: numerator $\\tan(\\sec+1)$, denominator $\\sec^2-1=\\tan^2$. "
         "Quotient $(\\sec+1)/\\tan=\\sec/\\tan+1/\\tan=1/\\sin+\\cos/\\sin=(\\csc+\\cot)$.",
         ["sin θ", "tan θ", "sec θ"]),
        ("SAT Stretch: $\\sin\\theta=-8/17$ in QIII. Find $(1-\\sin\\theta)/\\cos\\theta$.",
         "-5/3",
         "QIII cosine $-15/17$. Numerator $1+8/17=25/17$. Quotient $(25/17)/(-15/17)=-25/15=-5/3$.",
         ["5/3", "-8/15", "15/17"]),
        ("SAT Stretch: Express $\\frac{\\sin\\theta}{1+\\cos\\theta}+\\frac{1+\\cos\\theta}{\\sin\\theta}$ as a single reciprocal function.",
         "2 csc θ", "Common denominator $\\sin(1+\\cos)$: numerator $\\sin^2+(1+\\cos)^2=\\sin^2+1+2\\cos+\\cos^2=2+2\\cos=2(1+\\cos)$. "
         "Fraction $=2(1+\\cos)/(\\sin(1+\\cos))=2/\\sin=2\\csc\\theta$.",
         ["2 sin θ", "sec θ", "2 cot θ"]),
        ("SAT Stretch: $\\sin\\theta=2/3$ in QI. The exact value of $\\cot^2\\theta$ is:",
         "5/4", "$\\cos^2=1-4/9=5/9$, so $\\cot^2=\\cos^2/\\sin^2=(5/9)/(4/9)=5/4$.",
         ["4/5", "√5 / 2", "9/4"]),
        ("SAT Stretch: Given $\\cos\\theta=-8/17$ in QII, the value of $\\dfrac{1}{1-\\sin\\theta}+\\dfrac{1}{1+\\sin\\theta}$ is:",
         "289/32",
         "QII sine $15/17$. The sum is $2/(1-\\sin^2)=2/\\cos^2=2\\sec^2\\theta$. Then $\\sec=-17/8$, so $2\\cdot 289/64=289/32$. Direct: $17/2+17/32=289/32$.",
         ["32/289", "17/8", "2"]),
        ("SAT Stretch: Given $\\sec\\theta=-5/3$ in QII, $\\tan\\theta$ equals:",
         "−4/3", "Cosine $-3/5$. QII sine positive $4/5$. Tangent $(4/5)/(-3/5)=-4/3$.",
         ["4/3", "3/4", "-3/4"]),
        ("SAT Stretch: $\\sin\\theta=5/13$ in QII. Find $\\tan\\theta+\\cot\\theta$.",
         "-169/60",
         "QII cosine $-12/13$. Then $\\tan=-5/12$ and $\\cot=-12/5$, so $(-5/12)+(-12/5)=(-25-144)/60=-169/60$. "
         "Equivalently $1/(\\sin\\cos)=1/((5/13)(-12/13))=-169/60$.",
         ["169/60", "-13/12", "0"]),
    ])


def build_unit5():
    title = "Trigonometry Unit 5: Identities"
    description = (
        "Pythagorean, even/odd, cofunction, and quotient identities; simplifying; verifying; "
        "and rewriting expressions to set up equations."
    )
    concepts = [
        "Pythagorean identities",
        "Even/odd and cofunction",
        "Quotient identities",
        "Simplify expressions",
        "Verify identities",
        "Rewrite to solve",
    ]

    c1 = concept_block(
        "1. Pythagorean identities",
        [
            "On the unit circle a point is $(\\cos\\theta,\\sin\\theta)$ and the radius is $1$, so $\\cos^2\\theta+\\sin^2\\theta=1$. "
            "That one sentence is the Pythagorean identity. It is not an equation you solve for a few angles; it is true for every $\\theta$ where sine and cosine are defined (always).",
            "Divide the identity by $\\cos^2\\theta$ (where $\\cos\\theta\\neq 0$) to get $1+\\tan^2\\theta=\\sec^2\\theta$. "
            "Divide by $\\sin^2\\theta$ (where $\\sin\\theta\\neq 0$) to get $\\cot^2\\theta+1=\\csc^2\\theta$. Those are not new geometries — they are the same circle written in other letters.",
            "Solving for a square is the daily move: $\\sin^2\\theta=1-\\cos^2\\theta$ and $\\cos^2\\theta=1-\\sin^2\\theta$. "
            "When a problem gives you one primary value and a quadrant, Pythagoras plus a sign chart recovers the other five functions.",
            "The geometric picture is a right triangle with legs $|\\cos\\theta|$ and $|\\sin\\theta|$ and hypotenuse $1$. "
            "In Quadrant II the cosine leg points left, but its square is still positive, so the identity does not notice the sign — you must restore signs from the quadrant after taking square roots.",
            "A square-root step always produces $\\pm$. Dropping the minus sign is how QIII cosine accidentally becomes positive on a test.",
            "These three identities are the engine of simplification. Almost every messy expression in this unit wants to become $1$, $\\tan^2$, or $\\sec^2$ after one Pythagorean substitution.",
        ],
        "Without $\\sin^2+\\cos^2=1$ you cannot convert a given sine into a cosine, cannot simplify $1-\\sin^2$, and cannot set up $\\tan^2=\\sec^2-1$ in an equation.",
        "If you know one of sine or cosine, square it, subtract from $1$, take a square root, then attach the quadrant sign. If you see $1+\\tan^2$, replace it by $\\sec^2$ immediately.",
        lesson_figure(
            _pythag_circle(60),
            "The unit-circle right triangle behind $\\sin^2\\theta+\\cos^2\\theta=1$",
            "The horizontal leg is $\\cos\\theta$, the vertical leg is $\\sin\\theta$, and the hypotenuse is the radius $1$. Pythagoras is the identity.",
        )
        + solved(1, "If $\\cos\\theta=3/5$ and $\\theta$ is acute, find $\\sin\\theta$.",
                 ["$\\sin^2\\theta=1-(3/5)^2=1-9/25=16/25$.",
                  "Acute: $\\sin\\theta=4/5$."],
                 "$4/5$", "", "Easy")
        + solved(2, "Rewrite $1+\\tan^2\\theta$ as a single function.",
                 ["Pythagorean: $1+\\tan^2\\theta=\\sec^2\\theta$."],
                 "$\\sec^2\\theta$", "", "Medium")
        + solved(3, "If $\\sin\\theta=-5/13$ and $\\theta$ is in QIII, find $\\cos\\theta$ and $\\tan\\theta$.",
                 ["$\\cos^2=1-25/169=144/169$, so $\\cos=\\pm 12/13$.",
                  "QIII: cosine negative, $\\cos\\theta=-12/13$.",
                  "$\\tan\\theta=\\sin/\\cos=(-5/13)/(-12/13)=5/12$."],
                 "$\\cos=-12/13$, $\\tan=5/12$", "The tangent is positive in QIII, matching ASTC.", "Hard"),
        ("Taking the positive square root in every quadrant",
         "Pythagoras gives a square. The sign is extra information from the quadrant. In QII and QIII cosine is negative; in QIII and QIV sine is negative."),
        ("Draw the reference triangle and then attach ASTC signs",
         "Build a QI triangle from the absolute values, then paint the correct signs onto opposite and adjacent."),
        ["I can state all three Pythagorean identities.",
         "I can recover sine from cosine (or the reverse) with a quadrant sign.",
         "I can replace $1+\\tan^2$ by $\\sec^2$ in a simplification."],
        1,
    )

    c2 = concept_block(
        "2. Even/odd and cofunction",
        [
            "Even functions satisfy $f(-x)=f(x)$. Odd functions satisfy $f(-x)=-f(x)$. "
            "Cosine and secant are even. Sine, tangent, cotangent, and cosecant are odd.",
            "On the unit circle, $-\\theta$ is a clockwise rotation. The $x$-coordinate (cosine) does not change; the $y$-coordinate (sine) flips sign. "
            "That is the whole even/odd story.",
            "Cofunction identities pair a function of $\\theta$ with the cofunction of the complement: "
            "$\\sin\\theta=\\cos(\\pi/2-\\theta)$, $\\tan\\theta=\\cot(\\pi/2-\\theta)$, $\\sec\\theta=\\csc(\\pi/2-\\theta)$, and the reverse pairings.",
            "These remain true in radians. Writing $90^\\circ$ or $\\pi/2$ is the same complement. "
            "On a mixed-unit test, convert first so you do not subtract $\\pi/2$ from $30^\\circ$.",
            "Even/odd is how you simplify $\\sin(-\\pi/6)$ to $-1/2$ without drawing a new triangle. "
            "Cofunction is how $\\cos(\\pi/2-\\pi/6)$ becomes $\\sin(\\pi/6)=1/2$.",
            "Together they let you fold any special angle back into $[0,\\pi/2]$ with a correct sign, which is the same skill as reference angles, now written as identities.",
        ],
        "Negative-angle and complement rewrites appear inside every addition formula in Unit 6. If even/odd is slow, those expansions become a tangle of signs.",
        "For a minus in the input, apply even/odd first. For a $\\pi/2$ minus, swap to the cofunction. Then evaluate the leftover acute (or QI) angle.",
        lesson_figure(
            unit_circle_svg(deg=-60),
            "$\\theta=-60^\\circ$ vs $60^\\circ$: same cosine, opposite sine",
            "The point is $(\\cos(-60^\\circ),\\sin(-60^\\circ))=(1/2,-\\sqrt{3}/2)$. That is even cosine and odd sine in one picture.",
        )
        + solved(4, "Evaluate $\\sin(-\\pi/6)$ and $\\cos(-\\pi/6)$.",
                 ["Sine odd: $\\sin(-\\pi/6)=-\\sin(\\pi/6)=-1/2$.",
                  "Cosine even: $\\cos(-\\pi/6)=\\cos(\\pi/6)=\\sqrt{3}/2$."],
                 "$-1/2$ and $\\sqrt{3}/2$", "", "Easy")
        + solved(5, "Rewrite $\\tan(\\pi/2-\\theta)$ as a cofunction of $\\theta$.",
                 ["$\\tan(\\pi/2-\\theta)=\\cot\\theta$."],
                 "$\\cot\\theta$", "", "Medium")
        + solved(6, "Simplify $\\sec(-\\theta)\\sin(-\\theta)$.",
                 ["Secant is even: $\\sec(-\\theta)=\\sec\\theta$.",
                  "Sine is odd: $\\sin(-\\theta)=-\\sin\\theta$.",
                  "Product $-\\sec\\theta\\sin\\theta=-\\tan\\theta$ (where cosine is nonzero)."],
                 "$-\\tan\\theta$", "", "Hard"),
        ("Treating every function as even",
         "$\\sin(-30^\\circ)$ is not $+1/2$. Only cosine and secant ignore the minus on the input."),
        ("Complement in matching units",
         "Write $\\pi/2-\\theta$ when $\\theta$ is in radians and $90^\\circ-\\theta$ when $\\theta$ is in degrees. Mixing $\\pi/2-30$ is meaningless."),
        ["I can apply even/odd to all six functions.",
         "I can write the six cofunction identities.",
         "I can combine even/odd with a quotient to simplify a product."],
        6,
    )

    c3 = concept_block(
        "3. Quotient identities",
        [
            "Tangent is sine over cosine: $\\tan\\theta=\\sin\\theta/\\cos\\theta$ wherever cosine is nonzero. "
            "Cotangent is cosine over sine wherever sine is nonzero. Those are definitions as much as identities.",
            "The reciprocal identities sit next to them: $\\csc=1/\\sin$, $\\sec=1/\\cos$, $\\cot=1/\\tan$. "
            "A simplification problem is usually 'write everything as sine and cosine, cancel, then optionally pack the result back into a single name.'",
            "Example: $\\tan\\theta\\cos\\theta=(\\sin\\theta/\\cos\\theta)\\cos\\theta=\\sin\\theta$. The cosine cancelled — legally, because tangent already required $\\cos\\theta\\neq 0$.",
            "When you cancel, you are restricting the domain to where the cancelled factor was nonzero. "
            "The simplified expression may look defined at extra points; the original identity holds only on the original domain.",
            "A second classic: $\\sin\\theta\\sec\\theta=\\tan\\theta$. A third: $\\frac{\\csc\\theta}{\\cot\\theta}=\\sec\\theta$. "
            "Each is one line once everything is a fraction of sine and cosine.",
            "Quotient identities are also how you convert an equation $\\sin\\theta=2\\cos\\theta$ into $\\tan\\theta=2$, which Unit 7 can solve.",
        ],
        "Every later identity proof starts by unpacking tan/sec/csc/cot into sine and cosine. If that translation is clumsy, proofs never start.",
        "Replace every name by $\\sin$, $\\cos$, or a ratio of those two. Cancel. Then, if the answer choices use a single name, pack back.",
        lesson_figure(
            unit_circle_svg(deg=45),
            "At $45^\\circ$, $y/x=1$, so $\\tan=\\sin/\\cos=1$",
            "The quotient identity is visible: the slope of the terminal ray is $\\tan\\theta=y/x$.",
        )
        + solved(7, "Simplify $\\tan\\theta\\cos\\theta$.",
                 ["$(\\sin\\theta/\\cos\\theta)\\cdot\\cos\\theta=\\sin\\theta$."],
                 "$\\sin\\theta$", "", "Easy")
        + solved(8, "Simplify $\\frac{\\csc\\theta}{\\cot\\theta}$.",
                 ["$(1/\\sin)\\div(\\cos/\\sin)=(1/\\sin)\\cdot(\\sin/\\cos)=1/\\cos=\\sec\\theta$."],
                 "$\\sec\\theta$", "", "Medium")
        + solved(9, "Simplify $\\frac{\\sin\\theta}{\\csc\\theta}+\\frac{\\cos\\theta}{\\sec\\theta}$.",
                 ["First term $\\sin\\cdot\\sin=\\sin^2$. Second $\\cos\\cdot\\cos=\\cos^2$.",
                  "Sum $\\sin^2+\\cos^2=1$."],
                 "$1$", "", "Hard"),
        ("Cancelling a factor that the original expression needed to be defined",
         "After simplifying $\\tan\\theta\\cos\\theta$ to $\\sin\\theta$, the result appears defined at $\\theta=\\pi/2$, but the original was not. Report the identity on the original domain."),
        ("Unpack to sine and cosine before inventing new cancellations",
         "If you try to cancel $\\sec$ against $\\tan$ by guessing, you will guess wrong. Translate first."),
        ["I can write tan and cot as quotients of sine and cosine.",
         "I can simplify a product or quotient of mixed functions.",
         "I can pack a sine-cosine result back into a single name."],
        11,
    )

    c4 = concept_block(
        "4. Simplify expressions",
        [
            "Simplifying means using identities to make an expression shorter, usually a single trig function or a constant. "
            "There is no unique 'simplest' form, but tests agree on targets like $1$, $\\sin\\theta$, $\\tan^2\\theta$, or $\\sec\\theta$.",
            "A reliable order: (1) rewrite reciprocal and quotient functions, (2) Pythagorean-substitute any $1-\\sin^2$ or $1+\\tan^2$, (3) factor, (4) cancel, (5) optionally use even/odd.",
            "Factoring is underrated. $(\\sec\\theta-1)(\\sec\\theta+1)=\\sec^2\\theta-1=\\tan^2\\theta$ is faster than expanding in sine and cosine.",
            "Fractions want a common denominator. $\\tan\\theta+\\cot\\theta=\\frac{\\sin}{\\cos}+\\frac{\\cos}{\\sin}=\\frac{1}{\\sin\\cos}=\\sec\\theta\\csc\\theta$.",
            "If two different-looking simplifications both match a numerical check at $\\theta=\\pi/6$, they may be equal — but a numerical check is not a proof. "
            "Still, plugging a safe acute angle is a good error detector.",
            "Never 'simplify' by dividing both sides of an unstated equation. You are simplifying an expression, not solving. There is no other side.",
        ],
        "Contest and SAT items that look like algebra are usually one Pythagorean substitution away from a constant. Practice makes that substitution automatic.",
        "Translate to sine and cosine, look for $1-\\sin^2$ or a difference of squares in sec/tan, then cancel. Check at a harmless acute angle.",
        lesson_figure(
            labeled_right_triangle(a=3, b=4, c=5, a_lab="3", b_lab="4", c_lab="5", angle_lab="θ"),
            "A $3$-$4$-$5$ triangle to numerically check a simplification",
            "If your simplified form and the original disagree at this acute $\\theta$, the algebra slipped. Agreement here does not finish a proof, but disagreement ends one.",
        )
        + solved(10, "Simplify $(1-\\cos^2\\theta)/\\sin\\theta$ for $\\sin\\theta\\neq 0$.",
                 ["$1-\\cos^2=\\sin^2$.",
                  "$\\sin^2/\\sin=\\sin$."],
                 "$\\sin\\theta$", "", "Easy")
        + solved(11, "Simplify $(\\sec\\theta-1)(\\sec\\theta+1)$.",
                 ["Difference of squares: $\\sec^2-1$.",
                  "$\\sec^2-1=\\tan^2$."],
                 "$\\tan^2\\theta$", "", "Medium")
        + solved(12, "Simplify $\\frac{1+\\tan^2\\theta}{\\csc^2\\theta}$.",
                 ["Numerator $\\sec^2\\theta$.",
                  "Denominator $\\csc^2=1/\\sin^2$.",
                  "Quotient $\\sec^2\\sin^2=(\\sin^2/\\cos^2)=\\tan^2\\theta$."],
                 "$\\tan^2\\theta$", "", "Hard"),
        ("Stopping at a longer sine-cosine fraction when a one-word name exists",
         "Answer choices are usually packed. If you have $\\sin/\\cos$, write $\\tan$. If you have $1/\\cos$, write $\\sec$."),
        ("Factor first when you see $\\sec\\pm 1$ or $1\\pm\\sin$",
         "Those patterns often want conjugates or difference of squares, not an immediate Pythagorean expansion of every term."),
        ["I can simplify using Pythagorean substitutions.",
         "I can factor secant/tangent pairs.",
         "I can combine two-term fractions of tan and cot."],
        16,
    )

    c5 = concept_block(
        "5. Verify identities",
        [
            "To verify an identity, show that one side can be rewritten as the other for all $\\theta$ in the common domain. "
            "The professional habit is to start with the more complicated side and morph it, never moving terms across the equals sign as if you were solving.",
            "You may also transform both sides independently until they meet in the middle. What you must not do is assume the identity to prove the identity — for example, by dividing both sides by the same trig expression at the first step without tracking domain.",
            "A template: complicated side $\\to$ sine and cosine $\\to$ common denominator $\\to$ Pythagorean collapse $\\to$ other side.",
            "If you get stuck, multiply by a conjugate. $1-\\sin\\theta$ in a denominator often wants $1+\\sin\\theta$ on top and bottom, producing $1-\\sin^2=\\cos^2$.",
            "Checking at one angle is a filter, not a verification. $\\sin\\theta=1-\\cos\\theta$ happens to hold at $0$ and at $\\pi/2$ but fails at $\\pi/6$. One counterexample kills an identity; one example never proves one.",
            "When the two sides have different domains (a cancelled factor), state the identity on the intersection. That precision is what 'where defined' means in the problem statement.",
        ],
        "Verification is the writing skill of trigonometry. Later, calculus will assume you can turn $\\tan^2$ into $\\sec^2-1$ in the middle of an integral without doubting the step.",
        "Pick the heavier side. Unpack. Common denominator. Pythagorean. Stop when you see the other side. Then, optionally, check at $\\pi/6$.",
        lesson_figure(
            _pythag_circle(45),
            "Verification is the same geometry as $\\sin^2+\\cos^2=1$",
            "Every verified identity is this circle plus arithmetic. If a step would not make sense on the unit circle, it is not a legal identity step.",
        )
        + solved(13, "Verify $\\tan\\theta\\cos\\theta=\\sin\\theta$ (where $\\cos\\theta\\neq 0$).",
                 ["Left side: $(\\sin\\theta/\\cos\\theta)\\cdot\\cos\\theta=\\sin\\theta$.",
                  "Right side is already $\\sin\\theta$."],
                 "both sides equal $\\sin\\theta$", "", "Easy")
        + solved(14, "Verify $\\sec^2\\theta-\\tan^2\\theta=1$.",
                 ["Left: $(1+\\tan^2)-\\tan^2=1$, using $1+\\tan^2=\\sec^2$.",
                  "Or $(1/\\cos^2)-(\\sin^2/\\cos^2)=(1-\\sin^2)/\\cos^2=\\cos^2/\\cos^2=1$."],
                 "$1=1$", "", "Medium")
        + solved(15, "Verify $\\frac{\\sin\\theta}{1+\\cos\\theta}=\\frac{1-\\cos\\theta}{\\sin\\theta}$ where both sides are defined.",
                 ["Multiply the left side top and bottom by $1-\\cos\\theta$.",
                  "Denominator $(1+\\cos)(1-\\cos)=1-\\cos^2=\\sin^2$.",
                  "Left becomes $\\sin(1-\\cos)/\\sin^2=(1-\\cos)/\\sin$, the right side."],
                 "identity holds on the common domain", "The conjugate $1-\\cos$ is the standard trick when $1+\\cos$ is in a denominator.", "Hard"),
        ("Proving an identity by plugging in $30^\\circ$ and stopping",
         "That is a check. A counterexample can disprove; an example cannot prove. You still need the algebraic chain."),
        ("Start on the side with more terms or a fraction",
         "The simpler side is the target. Aim at it. Do not complicate the already-simple side."),
        ["I can verify a one-line quotient identity.",
         "I can use $1+\\tan^2=\\sec^2$ inside a verification.",
         "I can multiply by a conjugate to create $1-\\cos^2$."],
        21,
    )

    c6 = concept_block(
        "6. Rewrite to solve",
        [
            "Before Unit 7's full equation machinery, you already need to change an equation's clothing so it mentions only one function. "
            "Pythagorean and quotient identities are the wardrobe.",
            "If both sine and cosine appear linearly, divide by cosine (where nonzero) to produce tangent. $2\\sin\\theta=\\cos\\theta$ becomes $\\tan\\theta=1/2$. "
            "Then check separately whether cosine-zero angles could have been solutions (they make the original undefined or false).",
            "If squares appear, use $\\sin^2=1-\\cos^2$ to get a quadratic in $\\cos\\theta$, or use $1+\\tan^2=\\sec^2$ to get a quadratic in $\\tan\\theta$.",
            "Example: $\\sec^2\\theta=4$ is $1+\\tan^2\\theta=4$, so $\\tan^2\\theta=3$. That is ready for square roots and quadrants.",
            "Do not divide by $\\sin\\theta$ if $\\sin\\theta=0$ might be a solution. Factor instead: $2\\sin^2\\theta-\\sin\\theta=0$ is $\\sin\\theta(2\\sin\\theta-1)=0$.",
            "The rewrite is finished when a single function equals a number, or a product of factors in one function equals zero. Solving those is Unit 7.",
        ],
        "A beautiful identity skill that never gets used on an equation is only half-learned. That is the bridge from simplify to solve.",
        "Name the functions you see. If there are two, either divide (tangent) or Pythagorean-substitute (one squared function). If a common factor exists, factor rather than divide.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#4f46e5", sample_curve(lambda x: math.sin(x), -0.2, 6.5, n=80)),
                    ("#0f766e", sample_curve(lambda x: math.cos(x), -0.2, 6.5, n=80)),
                ],
                xlim=(-0.2, 6.5), ylim=(-1.4, 1.4), w=340, h=200, xlab="θ", ylab="y",
            ),
            "$\\sin\\theta=\\cos\\theta$ is the intersection of the two parent waves",
            "Dividing produces $\\tan\\theta=1$, whose solutions $\\pi/4+k\\pi$ are exactly those intersection $x$-values in $[0,2\\pi)$: $\\pi/4$ and $5\\pi/4$.",
        )
        + solved(16, "Rewrite $2\\sin\\theta=\\cos\\theta$ in terms of tangent (where $\\cos\\theta\\neq 0$).",
                 ["Divide: $2\\tan\\theta=1$, so $\\tan\\theta=1/2$."],
                 "$\\tan\\theta=1/2$", "", "Easy")
        + solved(17, "Rewrite $\\sec^2\\theta=4$ as an equation in $\\tan\\theta$.",
                 ["$1+\\tan^2\\theta=4$.",
                  "$\\tan^2\\theta=3$."],
                 "$\\tan^2\\theta=3$", "", "Medium")
        + solved(18, "Rewrite $2\\sin^2\\theta-\\sin\\theta=0$ by factoring.",
                 ["$\\sin\\theta(2\\sin\\theta-1)=0$.",
                  "So $\\sin\\theta=0$ or $\\sin\\theta=1/2$.",
                  "Dividing by $\\sin\\theta$ at the start would have lost the $\\sin\\theta=0$ family."],
                 "$\\sin\\theta=0$ or $\\sin\\theta=1/2$", "", "Hard"),
        ("Dividing by a trig function that might be zero",
         "Factoring keeps those roots. Division throws them away. If the original is defined when that factor is zero, you just lost solutions."),
        ("Finish the rewrite with a single function equal to a number (or a factored zero product)",
         "That is the handoff to inverse trig and general solutions. A mix of sine and cosine still sitting there is not finished."),
        ["I can convert mixed sine/cosine equations into tangent.",
         "I can use $1+\\tan^2=\\sec^2$ to change a secant equation.",
         "I can factor a quadratic in $\\sin\\theta$ instead of dividing."],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
        stretch_note=STRETCH_LABEL,
    )
    return title, description, content, _u5_questions()


# ===========================================================================
# UNIT 6: Sum, Difference & Multiple Angle
# ===========================================================================

def _u6_questions():
    return _pack([
        ("$\\sin(a+b)$ expands to:",
         "sin a cos b + cos a sin b", "Sine addition formula.", ["sin a cos b − cos a sin b", "cos a cos b − sin a sin b", "sin a + sin b"]),
        ("$\\cos(a-b)$ expands to:",
         "cos a cos b + sin a sin b", "Cosine of a difference has a plus between the products.",
         ["cos a cos b − sin a sin b", "sin a cos b + cos a sin b", "cos a − cos b"]),
        ("$\\sin 75^\\circ=\\sin(45^\\circ+30^\\circ)$ equals:",
         "(√6 + √2)/4", "$\\sin 45\\cos 30+\\cos 45\\sin 30=(\\sqrt{2}/2)(\\sqrt{3}/2)+(\\sqrt{2}/2)(1/2)$.",
         ["(√6 − √2)/4", "√3/2", "1/2"]),
        ("$\\cos 15^\\circ=\\cos(45^\\circ-30^\\circ)$ equals:",
         "(√6 + √2)/4", "$\\cos 45\\cos 30+\\sin 45\\sin 30$.", ["(√6 − √2)/4", "√2/2", "1"]),
        ("$\\sin(\\pi/2-\\theta)$ using addition becomes:",
         "cos θ", "$\\sin(\\pi/2)\\cos\\theta-\\cos(\\pi/2)\\sin\\theta=1\\cdot\\cos\\theta-0$.", ["sin θ", "−cos θ", "−sin θ"]),
        ("$\\tan(a+b)$ equals:",
         "(tan a + tan b)/(1 − tan a tan b)", "Tangent addition formula, where defined.",
         ["(tan a − tan b)/(1 + tan a tan b)", "tan a + tan b", "tan a tan b"]),
        ("$\\tan 75^\\circ=\\tan(45^\\circ+30^\\circ)$ equals:",
         "2 + √3", "$(1+1/\\sqrt{3})/(1-1/\\sqrt{3})$ rationalizes to $2+\\sqrt{3}$.", ["2 − √3", "1", "√3"]),
        ("$\\tan(a-b)$ equals:",
         "(tan a − tan b)/(1 + tan a tan b)", "Difference formula.",
         ["(tan a + tan b)/(1 − tan a tan b)", "tan a − tan b", "1"]),
        ("If $\\tan a=1$ and $\\tan b=1/2$, then $\\tan(a+b)$ equals:",
         "3", "$(1+1/2)/(1-1\\cdot 1/2)=(3/2)/(1/2)=3$.", ["3/2", "1/2", "1"]),
        ("$\\tan(\\pi/4+\\theta)$ equals:",
         "(1 + tan θ)/(1 − tan θ)", "Set $a=\\pi/4$, $\\tan a=1$.", ["tan θ", "(1 − tan θ)/(1 + tan θ)", "1 + tan θ"]),
        ("$\\sin(2\\theta)$ equals:",
         "2 sin θ cos θ", "Double-angle sine.", ["sin²θ", "2 sin θ", "cos²θ − sin²θ"]),
        ("One form of $\\cos(2\\theta)$ is:",
         "cos²θ − sin²θ", "Also $2\\cos^2-1$ and $1-2\\sin^2$.", ["2 sin θ cos θ", "2 cos θ", "sin²θ − cos²θ"]),
        ("$\\cos(2\\theta)$ in terms of sine only is:",
         "1 − 2 sin²θ", "Power-reduce / double-angle variant.", ["2 sin²θ − 1", "2 sin θ cos θ", "1 − sin²θ"]),
        ("If $\\sin\\theta=3/5$ in QI, $\\sin(2\\theta)$ equals:",
         "24/25", "$\\cos=4/5$, so $2\\cdot(3/5)\\cdot(4/5)=24/25$.", ["6/5", "7/25", "12/25"]),
        ("$\\tan(2\\theta)$ equals:",
         "2 tan θ / (1 − tan²θ)", "Double-angle tangent.", ["2 tan θ", "tan²θ", "1 − tan²θ"]),
        ("The half-angle formula $\\cos^2(\\theta/2)$ equals:",
         "(1 + cos θ)/2", "Power-reduce solved for the half angle.", ["(1 − cos θ)/2", "1 + cos θ", "sin θ / 2"]),
        ("$\\sin^2(\\theta/2)$ equals:",
         "(1 − cos θ)/2", "The minus sign belongs to sine-squared.", ["(1 + cos θ)/2", "1 − cos θ", "cos θ / 2"]),
        ("$\\sin 15^\\circ$ using a half-angle of $30^\\circ$ equals:",
         "√(2 − √3)/2", "$\\sin^2 15=(1-\\cos 30)/2=(1-\\sqrt{3}/2)/2$, then take the positive root.",
         ["√(2 + √3)/2", "1/2", "√3/2"]),
        ("If $\\cos\\theta=3/5$ and $\\theta$ is in QI, $\\cos(\\theta/2)$ (also QI) equals:",
         "2√5/5", "$(1+3/5)/2=4/5$, so $\\cos(\\theta/2)=\\sqrt{4/5}=2/\\sqrt{5}=2\\sqrt{5}/5$.",
         ["√(1/5)", "3/10", "4/5"]),
        ("The sign of a half-angle sine is determined by:",
         "the quadrant of θ/2", "The formula under the square root is unsigned; you choose $\\pm$ from where $\\theta/2$ lives.",
         ["always positive", "the quadrant of 2θ", "always matching sin θ"]),
        ("$\\sin a\\cos b$ as a sum is:",
         "[sin(a+b) + sin(a−b)]/2", "Product-to-sum.", ["[cos(a+b)+cos(a−b)]/2", "sin(a+b)", "2 sin a cos b"]),
        ("$\\cos a\\cos b$ as a sum is:",
         "[cos(a+b) + cos(a−b)]/2", "Product-to-sum for two cosines.", ["[sin(a+b)+sin(a−b)]/2", "cos(a+b)", "[cos(a+b)−cos(a−b)]/2"]),
        ("$2\\sin 3x\\cos 3x$ equals:",
         "sin(6x)", "That is the double-angle $2\\sin\\theta\\cos\\theta$ with $\\theta=3x$.", ["sin(3x)", "cos(6x)", "2 sin(6x)"]),
        ("Product-to-sum is useful because it turns a product into:",
         "a sum of sines or cosines", "Those are easier to integrate or to read as beats in waves.",
         ["a tangent", "a square", "a half-angle only"]),
        ("$\\sin 5\\theta+\\sin 3\\theta$ can be rewritten as a product using:",
         "sum-to-product identities", "The reverse of product-to-sum.", ["Pythagorean only", "odd/even only", "SOH-CAH-TOA"]),
        ("$\\sin^2\\theta$ power-reduces to:",
         "(1 − cos 2θ)/2", "Standard power-reduce.", ["(1 + cos 2θ)/2", "1 − cos 2θ", "2 sin θ"]),
        ("$\\cos^2\\theta$ power-reduces to:",
         "(1 + cos 2θ)/2", "The plus sign belongs to cosine-squared.", ["(1 − cos 2θ)/2", "1 + cos 2θ", "2 cos θ"]),
        ("$\\sin^2(\\pi/6)$ via power-reduce equals:",
         "1/4", "$(1-\\cos(\\pi/3))/2=(1-1/2)/2=1/4$, matching $(1/2)^2$.", ["1/2", "3/4", "√3/2"]),
        ("$\\cos^4\\theta$ can be reduced by writing $(\\cos^2\\theta)^2$ and then:",
         "((1 + cos 2θ)/2)²", "Then reduce $\\cos^2 2\\theta$ again if needed.", ["sin 4θ", "2 cos 2θ", "1 − sin²θ"]),
        ("Power-reduce is the inverse operation of:",
         "the double-angle formulas for cosine", "Solving $1-2\\sin^2=\\cos 2\\theta$ for $\\sin^2$.",
         ["SOH-CAH-TOA", "the law of sines", "even/odd"]),
        ("$\\cos(a+b)$ expands to:",
         "cos a cos b − sin a sin b", "Minus in the cosine-of-sum formula.",
         ["cos a cos b + sin a sin b", "sin a cos b + cos a sin b", "cos a + cos b"]),
        ("$\\sin 15^\\circ=\\sin(45^\\circ-30^\\circ)$ equals:",
         "(√6 − √2)/4", "Sine of a difference.", ["(√6 + √2)/4", "√2/2", "1/2"]),
        ("If $\\cos\\theta=-3/5$ in QII, $\\cos(2\\theta)$ using $2\\cos^2-1$ equals:",
         "-7/25", "$2\\cdot(9/25)-1=18/25-25/25=-7/25$.", ["7/25", "24/25", "-24/25"]),
        ("$\\tan 15^\\circ=\\tan(45^\\circ-30^\\circ)$ equals:",
         "2 − √3", "Tangent difference formula.", ["2 + √3", "1", "√3/3"]),
        ("$\\sin(2\\cdot 15^\\circ)$ must equal $\\sin 30^\\circ=1/2$. Using $2\\sin 15\\cos 15$ is a check on:",
         "the 15° exact values", "If your $\\sin 15$ and $\\cos 15$ are right, the product times $2$ is $1/2$.",
         ["the law of sines", "radians only", "evenness of sine"]),
        ("$\\cos(2\\theta)=2\\cos^2\\theta-1$ solved for $\\cos^2\\theta$ is the power-reduce formula. That algebra step divides by:",
         "2", "Add $1$, then divide by $2$.", ["cos θ", "2θ", "0"]),
        ("The formula for $\\sin(a-b)$ has which middle sign?",
         "minus: sin a cos b − cos a sin b", "Sine difference.", ["plus", "times", "no second product"]),
        ("If $\\tan\\theta=1/2$, $\\tan(2\\theta)$ equals:",
         "4/3", "$2\\cdot(1/2)/(1-(1/2)^2)=1/(1-1/4)=1/(3/4)=4/3$.", ["1", "1/4", "4"]),
        ("$\\sin 3\\theta$ can be written using $\\sin(2\\theta+\\theta)$ as:",
         "3 sin θ − 4 sin³θ", "After expanding and using $\\cos^2=1-\\sin^2$.", ["3 sin θ", "sin³θ", "4 sin θ"]),
        ("Product $\\sin 4x\\cos 2x$ as a sum starts with:",
         "[sin(6x) + sin(2x)]/2", "$a=4x$, $b=2x$.", ["[sin 8x]/2", "sin(6x)", "2 sin 4x cos 2x"]),
        ("$\\cos 2\\theta$ when $\\theta=\\pi/3$ equals:",
         "-1/2", "$\\cos(2\\pi/3)=-1/2$, or $2(1/2)^2-1=-1/2$.", ["1/2", "1", "0"]),
        ("Half-angle $\\tan(\\theta/2)$ has several forms, including:",
         "sin θ / (1 + cos θ)", "A common rational form that avoids a nested radical.", ["2 tan θ", "1 + cos θ", "tan θ / 2"]),
        ("$\\sin^2 75^\\circ$ by power-reduce uses $\\cos 150^\\circ=-\\sqrt{3}/2$, so the value is:",
         "(2 + √3)/4", "$(1-(-\\sqrt{3}/2))/2=(2+\\sqrt{3})/4$.", ["(2 − √3)/4", "1/2", "3/4"]),
        ("The cosine addition formula at $a=b=\\theta$ becomes:",
         "cos(2θ) = cos²θ − sin²θ", "Double-angle as a special case of addition.", ["cos(2θ)=2 cos θ", "sin(2θ)", "1"]),
        ("If $a=\\pi/2$ in $\\cos(a-b)$, you recover:",
         "sin b", "$\\cos(\\pi/2-b)=\\sin b$, the cofunction identity as a special case.", ["cos b", "−sin b", "0"]),
        ("$2\\cos^2\\theta-1=0$ is a double-angle equation equivalent to:",
         "cos(2θ) = 0", "Left side is $\\cos 2\\theta$.", ["sin(2θ)=0", "cos θ=0", "tan θ=1"]),
        ("SAT Stretch: $\\sin\\theta=5/13$ in QII. Find $\\cos(2\\theta)$ using $1-2\\sin^2$.",
         "119/169", "$1-2\\cdot(25/169)=1-50/169=119/169$. QII is not needed for this form, which uses only sine.",
         ["-119/169", "10/13", "120/169"]),
        ("SAT Stretch: Find $\\sin(a+b)$ if $\\sin a=3/5$ (QI), $\\cos b=-5/13$ (QII).",
         "33/65", "Need $\\cos a=4/5$ and $\\sin b=12/13$ (QII sine is positive). Then $(3/5)(-5/13)+(4/5)(12/13)=(-15+48)/65=33/65$.",
         ["-16/65", "-33/65", "63/65"]),
        ("SAT Stretch: $\\sin a=-3/5$ in QIII and $\\cos b=5/13$ in QIV. Find $\\cos(a-b)$.",
         "16/65",
         "Then $\\cos a=-4/5$ and $\\sin b=-12/13$. So $\\cos(a-b)=(-4/5)(5/13)+(-3/5)(-12/13)=(-20+36)/65=16/65$.",
         ["-16/65", "-33/65", "56/65"]),
        ("SAT Stretch: $\\sin\\theta=-8/17$ in QIII. Find $\\cos(2\\theta)$ using $2\\cos^2\\theta-1$.",
         "161/289",
         "QIII cosine $-15/17$. Then $2(225/289)-1=(450-289)/289=161/289$.",
         ["-161/289", "1-2(64/289)", "240/289"]),
        ("SAT Stretch: $\\theta$ in QIII, $\\tan\\theta=4/3$. Then $\\sin(2\\theta)=2\\tan\\theta/(1+\\tan^2\\theta)$ equals:",
         "24/25", "$2\\cdot(4/3)/(1+16/9)=(8/3)/(25/9)=24/25$. The formula $2t/(1+t^2)$ already carries the correct sign for this $t$.",
         ["-24/25", "7/25", "4/3"]),
        ("SAT Stretch: Evaluate $\\sin 75^\\circ\\cos 15^\\circ$ by product-to-sum.",
         "(2+√3)/4",
         "$\\frac12[\\sin 90^\\circ+\\sin 60^\\circ]=\\frac12\\bigl(1+\\sqrt{3}/2\\bigr)=(2+\\sqrt{3})/4$.",
         ["(2−√3)/4", "1/2", "√3/2"]),
        ("SAT Stretch: $\\cos\\theta=7/25$ with $\\theta$ in QIV, so $\\theta/2$ is in QII. Find $\\sin(\\theta/2)$.",
         "3/5",
         "$\\sin^2(\\theta/2)=(1-7/25)/2=(18/25)/2=9/25$. QII sine is positive, so $\\sin(\\theta/2)=3/5$.",
         ["-3/5", "4/5", "√(9/25) with a minus"]),
        ("SAT Stretch: $\\sin a=4/5$ in QI and $\\cos b=-3/5$ in QIII. Find $\\sin(a+b)$.",
         "-24/25",
         "Then $\\cos a=3/5$ and $\\sin b=-4/5$. So $\\sin(a+b)=(4/5)(-3/5)+(3/5)(-4/5)=(-12-12)/25=-24/25$.",
         ["24/25", "-7/25", "0"]),
        ("SAT Stretch: Evaluate $\\tan(\\pi/12)$ given $\\pi/12=\\pi/3-\\pi/4$. The exact value is:",
         "2 − √3", "$\\tan(\\pi/3-\\pi/4)=(\\sqrt{3}-1)/(1+\\sqrt{3}\\cdot 1)$, which rationalizes to $2-\\sqrt{3}$.",
         ["2 + √3", "√3 − 1", "1"]),
    ])


def build_unit6():
    title = "Trigonometry Unit 6: Sum, Difference & Multiple Angle"
    description = (
        "Sine and cosine addition, tangent addition, double-angle, half-angle, "
        "product-to-sum, and power-reduce formulas."
    )
    concepts = [
        "Sine/cosine addition",
        "Tangent addition",
        "Double-angle",
        "Half-angle",
        "Product-to-sum",
        "Power-reduce",
    ]

    c1 = concept_block(
        "1. Sine/cosine addition",
        [
            "The addition formulas extend the special-angle list to every sum or difference of those angles. "
            "$\\sin(a+b)=\\sin a\\cos b+\\cos a\\sin b$ and $\\cos(a+b)=\\cos a\\cos b-\\sin a\\sin b$. "
            "Flip the middle sign for $a-b$: sine gets a minus, cosine gets a plus (because cosine is even in the second slot in that sense).",
            "A memory hook: cosine of a sum looks like a 'mismatch' minus, the same pattern as $\\cos(2\\theta)=\\cos^2-\\sin^2$. "
            "Sine of a sum looks like a mix-and-plus, the same pattern as $\\sin(2\\theta)=2\\sin\\cos$.",
            "Exact values such as $\\sin 75^\\circ=\\sin(45+30)$ and $\\cos 15^\\circ=\\cos(45-30)$ are the homework of this lesson. "
            "The answers live in the form $(\\sqrt{6}\\pm\\sqrt{2})/4$.",
            "You can also use the formulas with non-special values given via a quadrant. If $\\sin a=3/5$ in QI and $\\cos b=-5/13$ in QII, recover the missing sine/cosine with Pythagoras, then plug into the expansion.",
            "Cofunction identities are special cases: $\\sin(\\pi/2-\\theta)=\\cos\\theta$ is the sine-difference formula with $a=\\pi/2$. "
            "Seeing that keeps the addition formulas from feeling like a separate religion.",
            "Signs in the expansion come from the formula, not from a second ASTC pass after you already used ASTC to get $\\sin a$ and $\\cos a$. Do not flip extra signs at the end.",
        ],
        "Double-angle, half-angle, and product-to-sum are all rearrangements of these two lines. If addition is shaky, the rest of the unit is a house of cards.",
        "Write the target as a sum or difference of listed angles. Expand with the matching formula. Insert exact values or recovered sides. Simplify one fraction.",
        lesson_figure(
            unit_circle_svg(deg=75),
            "$75^\\circ=45^\\circ+30^\\circ$ on the unit circle",
            "The point is not a $30/45/60$ coordinate by itself. The addition formula builds $(\\cos 75^\\circ,\\sin 75^\\circ)$ from those two special rays.",
        )
        + solved(1, "Expand $\\sin(a+b)$.",
                 ["$\\sin(a+b)=\\sin a\\cos b+\\cos a\\sin b$."],
                 "$\\sin a\\cos b+\\cos a\\sin b$", "", "Easy")
        + solved(2, "Find the exact value of $\\sin 75^\\circ$.",
                 ["$75=45+30$.",
                  "$\\sin 45\\cos 30+\\cos 45\\sin 30=(\\sqrt{2}/2)(\\sqrt{3}/2)+(\\sqrt{2}/2)(1/2)=(\\sqrt{6}+\\sqrt{2})/4$."],
                 "$(\\sqrt{6}+\\sqrt{2})/4$", "", "Medium")
        + solved(3, "Find $\\cos(a-b)$ if $\\cos a=3/5$ (QI) and $\\sin b=5/13$ (QI).",
                 ["$\\sin a=4/5$, $\\cos b=12/13$.",
                  "$\\cos(a-b)=\\cos a\\cos b+\\sin a\\sin b=(3/5)(12/13)+(4/5)(5/13)=(36+20)/65=56/65$."],
                 "$56/65$", "", "Hard"),
        ("Using the cosine-sum minus when you meant a difference",
         "$\\cos(a-b)$ has a plus. The minus belongs to $\\cos(a+b)$. Mixing those two is the most common expansion error."),
        ("List $\\sin a,\\cos a,\\sin b,\\cos b$ with signs before substituting",
         "Four numbers, four signs, then one formula. Do not recover a side in the middle of the expansion."),
        ["I can write the four sine/cosine addition formulas.",
         "I can compute $\\sin 75^\\circ$ and $\\cos 15^\\circ$ exactly.",
         "I can expand $\\sin(a+b)$ from two given quadrant facts."],
        1,
    )

    c2 = concept_block(
        "2. Tangent addition",
        [
            "Divide the sine-addition formula by the cosine-addition formula and then divide numerator and denominator by $\\cos a\\cos b$ to obtain "
            "$\\tan(a+b)=(\\tan a+\\tan b)/(1-\\tan a\\tan b)$, wherever the expression is defined.",
            "The difference formula flips both interior signs: $(\\tan a-\\tan b)/(1+\\tan a\\tan b)$.",
            "Definedness fails when $\\cos(a+b)=0$, i.e. when $a+b=\\pi/2+k\\pi$, which is exactly when the denominator $1-\\tan a\\tan b=0$. "
            "If a multiple-choice denominator is zero, the tangent of the sum is undefined, not $0$.",
            "Classic exact value: $\\tan 75^\\circ=\\tan(45+30)=(1+1/\\sqrt{3})/(1-1/\\sqrt{3})=2+\\sqrt{3}$ after rationalizing. "
            "$\\tan 15^\\circ=2-\\sqrt{3}$.",
            "If you already know two tangents, you never need to build sine and cosine first. That is the point of the compact formula.",
            "Double-angle tangent is the special case $b=a$: $\\tan(2a)=2\\tan a/(1-\\tan^2 a)$.",
        ],
        "Slope-of-a-ray problems and some calculus derivative checks use $\\tan(a+b)$ directly. It is also the fastest exact-value path for $15^\\circ$ and $75^\\circ$ tangents.",
        "Write the formula, substitute the two tangents, simplify the fraction, and refuse to divide if the denominator is zero.",
        lesson_figure(
            unit_circle_svg(deg=75),
            "$\\tan 75^\\circ$ is the slope of the $75^\\circ$ ray",
            "The addition formula computes that slope from the slopes $1$ and $1/\\sqrt{3}$ of the $45^\\circ$ and $30^\\circ$ rays.",
        )
        + solved(4, "Write the formula for $\\tan(a+b)$.",
                 ["$(\\tan a+\\tan b)/(1-\\tan a\\tan b)$, where defined."],
                 "$(\\tan a+\\tan b)/(1-\\tan a\\tan b)$", "", "Easy")
        + solved(5, "Find $\\tan(a+b)$ if $\\tan a=1$ and $\\tan b=1/2$.",
                 ["$(1+1/2)/(1-1\\cdot 1/2)=(3/2)/(1/2)=3$."],
                 "$3$", "", "Medium")
        + solved(6, "Find exact $\\tan 15^\\circ$.",
                 ["$15=45-30$.",
                  "$(1-1/\\sqrt{3})/(1+1/\\sqrt{3})$.",
                  "Multiply top and bottom by $\\sqrt{3}$: $(\\sqrt{3}-1)/(\\sqrt{3}+1)$, then rationalize to $2-\\sqrt{3}$."],
                 "$2-\\sqrt{3}$", "", "Hard"),
        ("Reporting $0$ when $1-\\tan a\\tan b=0$",
         "A zero denominator means the cosine of the sum is zero, so tangent is undefined. That is an asymptote angle, not a root."),
        ("Rationalize $15^\\circ$ and $75^\\circ$ answers to match choices",
         "Leave $2\\pm\\sqrt{3}$, not an unrationalized $(1-1/\\sqrt{3})/(1+1/\\sqrt{3})$."),
        ["I can write both tangent addition formulas.",
         "I can compute $\\tan(a+b)$ from two numeric tangents.",
         "I can produce exact $\\tan 15^\\circ$ and $\\tan 75^\\circ$."],
        6,
    )

    c3 = concept_block(
        "3. Double-angle",
        [
            "Set $b=a$ in the addition formulas. Immediately $\\sin(2\\theta)=2\\sin\\theta\\cos\\theta$ and $\\cos(2\\theta)=\\cos^2\\theta-\\sin^2\\theta$. "
            "The cosine version has two extra outfits: $2\\cos^2\\theta-1$ and $1-2\\sin^2\\theta$, obtained by replacing $\\sin^2$ or $\\cos^2$ via Pythagoras.",
            "Pick the cosine form that matches what you know. Given only $\\sin\\theta$, use $1-2\\sin^2\\theta$. Given only $\\cos\\theta$, use $2\\cos^2\\theta-1$.",
            "Tangent double-angle: $2t/(1-t^2)$ with $t=\\tan\\theta$.",
            "A QI sine $3/5$ gives $\\cos=4/5$, hence $\\sin 2\\theta=24/25$ and $\\cos 2\\theta=(16-9)/25=7/25$. "
            "Always attach the quadrant of $2\\theta$ if you took a square root somewhere else; these product forms already include signs.",
            "Double-angle is also how you solve $\\cos(2\\theta)=0$ without expanding, and how you rewrite $2\\sin\\theta\\cos\\theta$ as a single sine in a product-to-sum setting.",
            "For $3\\theta$, write $\\sin(2\\theta+\\theta)$ and expand, then replace $\\cos^2$ to get the triple-angle polynomial $3\\sin\\theta-4\\sin^3\\theta$. That is an honors extra, not required to start.",
        ],
        "Power-reduce is double-angle solved for the square. Half-angle is double-angle with $\\theta$ renamed $\\theta/2$. Learn one well and the family is free.",
        "Write down all three cosine double-angle forms. Circle the one whose input you actually have. Substitute. Do not take an extra square root.",
        lesson_figure(
            unit_circle_svg(deg=120),
            "If $\\theta=60^\\circ$, then $2\\theta=120^\\circ$",
            "$\\sin 60=\\sqrt{3}/2$, $\\cos 60=1/2$, so $\\sin 120=2\\cdot(\\sqrt{3}/2)\\cdot(1/2)=\\sqrt{3}/2$, matching the QII point shown.",
        )
        + solved(7, "State $\\sin(2\\theta)$ and one form of $\\cos(2\\theta)$.",
                 ["$\\sin 2\\theta=2\\sin\\theta\\cos\\theta$.",
                  "$\\cos 2\\theta=\\cos^2\\theta-\\sin^2\\theta$ (or $2\\cos^2-1$ or $1-2\\sin^2$)."],
                 "$2\\sin\\theta\\cos\\theta$ and $\\cos^2-\\sin^2$", "", "Easy")
        + solved(8, "If $\\sin\\theta=3/5$ in QI, find $\\sin(2\\theta)$ and $\\cos(2\\theta)$.",
                 ["$\\cos\\theta=4/5$.",
                  "$\\sin 2\\theta=2\\cdot 3/5\\cdot 4/5=24/25$.",
                  "$\\cos 2\\theta=16/25-9/25=7/25$."],
                 "$24/25$ and $7/25$", "", "Medium")
        + solved(9, "If $\\cos\\theta=-3/5$ in QII, find $\\cos(2\\theta)$ using $2\\cos^2-1$.",
                 ["$2\\cdot(9/25)-1=18/25-1=-7/25$.",
                  "You did not need sine, and the form already carries the sign."],
                 "$-7/25$", "", "Hard"),
        ("Using $2\\sin\\theta$ as if it were $\\sin(2\\theta)$",
         "The $2$ multiplies the product $\\sin\\theta\\cos\\theta$, not the angle alone and not sine alone. $\\sin(2\\theta)$ is not $2\\sin\\theta$."),
        ("Match the cosine double-angle form to the given function",
         "If the problem gives $\\sin\\theta$ only, $1-2\\sin^2$ is the direct path. Building cosine first is extra work and extra sign risk."),
        ["I can state sine and cosine double-angle formulas.",
         "I can compute $\\sin 2\\theta$ from a QI pair $(3/5,4/5)$.",
         "I can choose $1-2\\sin^2$ or $2\\cos^2-1$ appropriately."],
        11,
    )

    c4 = concept_block(
        "4. Half-angle",
        [
            "Solve $1-2\\sin^2(\\theta/2)=\\cos\\theta$ for the square: $\\sin^2(\\theta/2)=(1-\\cos\\theta)/2$. "
            "Similarly $\\cos^2(\\theta/2)=(1+\\cos\\theta)/2$. Then $\\sin(\\theta/2)=\\pm\\sqrt{(1-\\cos\\theta)/2}$, with the sign from the quadrant of $\\theta/2$, not of $\\theta$.",
            "If $\\theta$ is in $(0,2\\pi)$, then $\\theta/2$ is in $(0,\\pi)$, so sine of the half-angle is nonnegative there — but if $\\theta$ is $2\\pi$ to $4\\pi$, the half lands in $(\\pi,2\\pi)$ and sine is negative. Track $\\theta/2$.",
            "A rational tangent half-angle, $\\tan(\\theta/2)=\\sin\\theta/(1+\\cos\\theta)$ (among equivalent forms), avoids the nested radical and is handy in integrals later.",
            "Exact $\\sin 15^\\circ$ can be done with a half of $30^\\circ$ or with a difference $45-30$. Both answers must match after simplifying radicals.",
            "When $\\cos\\theta$ is given as a negative fraction, $1-\\cos\\theta$ is larger than $1$, which is legal inside the half-angle formula because you then divide by $2$.",
            "Do not write $\\sin(\\theta/2)=\\sin\\theta/2$. That confuses a half-angle with a half-value. Parentheses matter.",
        ],
        "Half-angles produce the remaining exact values (15°, 7.5° in contest settings) and appear in Weierstrass substitutions in calculus.",
        "Write the squared formula first. Take the square root last. Choose the sign from the quadrant of $\\theta/2$.",
        lesson_figure(
            unit_circle_svg(deg=30),
            "Half of $30^\\circ$ is $15^\\circ$, whose sine is not a 30-60-90 coordinate",
            "The half-angle formula builds $\\sin 15^\\circ=\\sqrt{(1-\\cos 30^\\circ)/2}$ from the $30^\\circ$ point shown.",
        )
        + solved(10, "State $\\sin^2(\\theta/2)$ and $\\cos^2(\\theta/2)$.",
                 ["$(1-\\cos\\theta)/2$ and $(1+\\cos\\theta)/2$."],
                 "$(1-\\cos\\theta)/2$ and $(1+\\cos\\theta)/2$", "", "Easy")
        + solved(11, "Find exact $\\sin 15^\\circ$ using a half-angle.",
                 ["$\\sin^2 15=(1-\\cos 30)/2=(1-\\sqrt{3}/2)/2=(2-\\sqrt{3})/4$.",
                  "$\\sin 15=\\sqrt{(2-\\sqrt{3})/4}=\\sqrt{2-\\sqrt{3}}/2$ (positive)."],
                 "$\\sqrt{2-\\sqrt{3}}/2$", "", "Medium")
        + solved(12, "If $\\cos\\theta=-7/25$ with $\\theta$ in QII, then $\\theta/2$ is in QI. Find $\\sin(\\theta/2)$.",
                 ["$(1-(-7/25))/2=(32/25)/2=16/25$.",
                  "$\\sin(\\theta/2)=+4/5$ because $\\theta/2$ is in QI."],
                 "$4/5$", "The plus sign is from $\\theta/2$, not from $\\theta$ being in QII.", "Hard"),
        ("Using the quadrant of $\\theta$ to sign the half-angle",
         "Halving an angle can change the quadrant family. Sign from $\\theta/2$. A QIII $\\theta$ near $190^\\circ$ has a half near $95^\\circ$, still QII."),
        ("Write the squared formula before the radical",
         "This prevents dropping the $/2$ or swapping the $1\\pm\\cos$ pair."),
        ["I can write both squared half-angle formulas.",
         "I can compute $\\sin 15^\\circ$ from $\\cos 30^\\circ$.",
         "I can choose the $\\pm$ from the quadrant of $\\theta/2$."],
        16,
    )

    c5 = concept_block(
        "5. Product-to-sum",
        [
            "Adding the addition formulas for $\\sin(a+b)$ and $\\sin(a-b)$ produces $2\\sin a\\cos b=\\sin(a+b)+\\sin(a-b)$, hence "
            "$\\sin a\\cos b=\\frac12[\\sin(a+b)+\\sin(a-b)]$. The other three product-to-sum identities are similar averages.",
            "In the opposite direction, sum-to-product identities write $\\sin P+\\sin Q$ as a product of a sine and a cosine. "
            "Those are useful for factoring a sum in an equation, such as $\\sin 5x+\\sin 3x=0$.",
            "A special case you already know: $2\\sin\\theta\\cos\\theta=\\sin(2\\theta)$ is product-to-sum with $a=b=\\theta$.",
            "These identities are the algebra of beats: two close frequencies multiply as a slow envelope times a fast oscillation. "
            "Physics and music use that picture; in this course we mainly rewrite products so they are easier to integrate or to solve.",
            "Keep the $1/2$. Dropping it is the standard arithmetic error. Also keep track of whether you have a plus or a minus between the two resulting terms — cosine products and sine products differ there.",
            "When both factors have coefficients in the angle, set $a$ and $b$ equal to those full angles, not to the coefficients alone.",
        ],
        "Product-to-sum is how a product of waves becomes a sum you can integrate term by term. It is also a compact way to handle $2\\sin A\\cos B$ on a contest without expanding from scratch.",
        "Name $a$ and $b$ as the two full angles. Write the matching $1/2$ formula. Simplify $a+b$ and $a-b$.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#94a3b8", sample_curve(lambda x: math.sin(5 * x) * math.sin(3 * x), 0, math.pi, n=120)),
                    ("#4f46e5", sample_curve(lambda x: 0.5 * (math.cos(2 * x) - math.cos(8 * x)), 0, math.pi, n=120)),
                ],
                xlim=(0, math.pi), ylim=(-1.3, 1.3), w=340, h=220, xlab="x", ylab="y",
            ),
            "$\\sin 5x\\sin 3x$ overlays $\\frac12(\\cos 2x-\\cos 8x)$",
            "The gray product and the indigo sum are the same curve. Product-to-sum unpacks a product of sines into two ordinary cosines.",
        )
        + solved(13, "Write $\\sin a\\cos b$ as a sum.",
                 ["$\\frac12[\\sin(a+b)+\\sin(a-b)]$."],
                 "$\\frac12[\\sin(a+b)+\\sin(a-b)]$", "", "Easy")
        + solved(14, "Rewrite $2\\sin 3x\\cos 3x$.",
                 ["This is $\\sin(6x)$ by double-angle, which is the product-to-sum with $a=b=3x$."],
                 "$\\sin(6x)$", "", "Medium")
        + solved(15, "Rewrite $\\sin 5x\\sin 3x$ as a sum of cosines.",
                 ["$\\sin A\\sin B=\\frac12[\\cos(A-B)-\\cos(A+B)]$.",
                  "$A=5x$, $B=3x$: $\\frac12[\\cos(2x)-\\cos(8x)]$."],
                 "$\\frac12[\\cos 2x-\\cos 8x]$", "", "Hard"),
        ("Dropping the factor $1/2$",
         "Every product-to-sum identity is an average of two terms. Without $1/2$ the amplitude is twice as large as it should be."),
        ("Write $A$ and $B$ as the entire angles $5x$ and $3x$",
         "Do not set $A=5$ and $B=3$. The identities are not about the coefficients in isolation."),
        ["I can convert $\\sin a\\cos b$ to a sum.",
         "I can recognize $2\\sin\\theta\\cos\\theta$ as $\\sin 2\\theta$.",
         "I can convert $\\sin A\\sin B$ to a difference of cosines."],
        21,
    )

    c6 = concept_block(
        "6. Power-reduce",
        [
            "Power-reduce formulas are the double-angle cosine formulas solved for the square: "
            "$\\sin^2\\theta=(1-\\cos 2\\theta)/2$ and $\\cos^2\\theta=(1+\\cos 2\\theta)/2$. "
            "They replace a square of a wave by a shifted cosine of double the angle, which is linear in that cosine.",
            "That is the move calculus wants: $\\int\\sin^2 x\\,dx$ becomes $\\int(1-\\cos 2x)/2\\,dx$. In this course we use them to simplify expressions and to evaluate exact squares such as $\\sin^2 75^\\circ$.",
            "Higher even powers: $\\cos^4\\theta=(\\cos^2\\theta)^2=((1+\\cos 2\\theta)/2)^2$, then power-reduce $\\cos^2 2\\theta$ again. "
            "The leftover will involve $\\cos 4\\theta$.",
            "A product of squares: $\\sin^2\\theta\\cos^2\\theta=(\\sin 2\\theta/2)^2=\\sin^2 2\\theta/4=(1-\\cos 4\\theta)/8$.",
            "Do not power-reduce a first power. $\\sin\\theta$ is already as simple as it gets; the identities of this lesson are for even powers (or for converting a square into a double-angle cosine).",
            "Check with a number: $\\sin^2(\\pi/6)=1/4$ and $(1-\\cos(\\pi/3))/2=(1-1/2)/2=1/4$. If a formula fails this check, the plus/minus was swapped.",
        ],
        "Any time a squared sine or cosine is in the way — identities, integrals, average power of a wave — power-reduce linearizes it.",
        "Replace each square with $(1\\pm\\cos 2\\theta)/2$, matching minus with sine and plus with cosine. Repeat on leftover even powers.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#94a3b8", sample_curve(lambda x: math.sin(x) ** 2, 0, 2 * math.pi, n=90)),
                    ("#4f46e5", sample_curve(lambda x: (1 - math.cos(2 * x)) / 2, 0, 2 * math.pi, n=90)),
                ],
                xlim=(0, 2 * math.pi), ylim=(-0.2, 1.3), w=340, h=200, xlab="θ", ylab="y",
            ),
            "$\\sin^2\\theta$ (gray) coincides with $(1-\\cos 2\\theta)/2$ (indigo)",
            "The two formulas draw the same curve: a raised cosine of twice the frequency, sitting between $0$ and $1$.",
        )
        + solved(16, "Write the power-reduce formula for $\\sin^2\\theta$.",
                 ["$(1-\\cos 2\\theta)/2$."],
                 "$(1-\\cos 2\\theta)/2$", "", "Easy")
        + solved(17, "Evaluate $\\sin^2 75^\\circ$ using power-reduce.",
                 ["$(1-\\cos 150^\\circ)/2$.",
                  "$\\cos 150=-\\sqrt{3}/2$.",
                  "$(1+\\sqrt{3}/2)/2=(2+\\sqrt{3})/4$."],
                 "$(2+\\sqrt{3})/4$", "", "Medium")
        + solved(18, "Rewrite $\\sin^2\\theta\\cos^2\\theta$ in terms of $\\cos 4\\theta$.",
                 ["$(\\sin 2\\theta/2)^2=\\sin^2 2\\theta/4$.",
                  "$\\sin^2 2\\theta=(1-\\cos 4\\theta)/2$.",
                  "So the product is $(1-\\cos 4\\theta)/8$."],
                 "$(1-\\cos 4\\theta)/8$", "", "Hard"),
        ("Swapping the plus and minus in the two formulas",
         "Sine-squared uses $1-\\cos 2\\theta$ because sine-squared is $0$ when $\\theta=0$, and $1-\\cos 0=0$. Cosine-squared uses the plus: at $0$ it equals $1$."),
        ("Check at $\\theta=0$ after writing a power-reduce",
         "If $\\sin^2 0$ did not become $0$, you used the cosine formula on a sine square."),
        ["I can write both power-reduce formulas.",
         "I can evaluate $\\sin^2$ of a special angle via $\\cos 2\\theta$.",
         "I can reduce $\\sin^2\\cos^2$ to a multiple of $1-\\cos 4\\theta$."],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
        stretch_note=STRETCH_LABEL,
    )
    return title, description, content, _u6_questions()


# ===========================================================================
# UNIT 7: Inverse Trig & Equations
# ===========================================================================

def _u7_questions():
    return _pack([
        ("$\\arcsin(1/2)$ in radians is:",
         "π/6", "Range of arcsin is $[-\\pi/2,\\pi/2]$, and $\\sin(\\pi/6)=1/2$.", ["5π/6", "π/3", "π/2"]),
        ("$\\arccos(0)$ equals:",
         "π/2", "Range of arccos is $[0,\\pi]$.", ["0", "π", "-π/2"]),
        ("$\\arctan(1)$ equals:",
         "π/4", "Range of arctan is $(-\\pi/2,\\pi/2)$.", ["3π/4", "π/2", "5π/4"]),
        ("$\\arcsin(-1)$ equals:",
         "−π/2", "The negative right angle is inside arcsin's range.", ["3π/2", "π/2", "π"]),
        ("$\\arccos(-1)$ equals:",
         "π", "Arccos of $-1$ is $\\pi$, not $0$.", ["0", "−π", "π/2"]),
        ("The range of $y=\\arcsin x$ is:",
         "[−π/2, π/2]", "Closed, because sine hits $\\pm 1$.", ["(−π/2, π/2)", "[0, π]", "(−∞, ∞)"]),
        ("The range of $y=\\arccos x$ is:",
         "[0, π]", "From the positive $x$-axis around to the negative $x$-axis.", ["[−π/2, π/2]", "(0, π)", "[−π, π]"]),
        ("The range of $y=\\arctan x$ is:",
         "(−π/2, π/2)", "Open, because tangent never meets its asymptotes.", ["[−π/2, π/2]", "[0, π]", "(0, π/2)"]),
        ("The domain of $y=\\arcsin x$ is:",
         "[−1, 1]", "Sine only outputs $[-1,1]$.", ["all reals", "[0, 1]", "(−∞, ∞)"]),
        ("$\\arctan$ of a very large positive number approaches:",
         "π/2", "Horizontal asymptote of arctan.", ["π", "0", "−π/2"]),
        ("Solutions of $\\sin\\theta=1/2$ on $[0,2\\pi)$ are:",
         "π/6 and 5π/6", "QI and QII.", ["π/6 only", "π/3 and 2π/3", "π/6 and 7π/6"]),
        ("Solutions of $\\cos\\theta=-1/2$ on $[0,2\\pi)$ are:",
         "2π/3 and 4π/3", "QII and QIII, reference $\\pi/3$.", ["π/3 and 5π/3", "2π/3 only", "π/6 and 5π/6"]),
        ("Solutions of $\\tan\\theta=1$ on $[0,2\\pi)$ are:",
         "π/4 and 5π/4", "Period $\\pi$, so two solutions in a $2\\pi$ window.", ["π/4 only", "π/4 and 3π/4", "π/4 and 7π/4"]),
        ("$\\sin\\theta=0$ on $[0,2\\pi)$ has solutions:",
         "0 and π", "$2\\pi$ is excluded by the half-open interval $[0,2\\pi)$.", ["0, π, 2π", "π only", "π/2 and 3π/2"]),
        ("$\\cos\\theta=0$ on $[0,2\\pi)$ has solutions:",
         "π/2 and 3π/2", "Odd multiples of $\\pi/2$ in the interval.", ["0 and π", "π/2 only", "π/4 and 3π/4"]),
        ("The general solution of $\\sin\\theta=1/2$ is:",
         "θ = π/6 + 2πk or θ = 5π/6 + 2πk", "Two families, one per quadrant solution.",
         ["θ = π/6 + 2πk only", "θ = π/6 + πk", "θ = 2πk"]),
        ("The general solution of $\\tan\\theta=1$ is:",
         "θ = π/4 + πk", "Tangent's period $\\pi$ gives a single family.",
         ["θ = π/4 + 2πk only", "θ = π/4 + 2πk or 5π/4 + 2πk is equivalent, but the compact form uses πk", "θ = kπ"]),
        ("The general solution of $\\cos\\theta=0$ is:",
         "θ = π/2 + πk", "Odd multiples of $\\pi/2$.", ["θ = πk", "θ = 2πk", "θ = π/2 + 2πk only"]),
        ("$\\sin\\theta=-1$ has general solution:",
         "θ = 3π/2 + 2πk", "Or equivalently $-\\pi/2+2\\pi k$.", ["θ = π/2 + 2πk", "θ = π + 2πk", "θ = 2πk"]),
        ("If you write only $\\theta=\\arcsin(1/2)+2\\pi k$, you are missing:",
         "the QII family 5π/6 + 2πk", "Arcsin returns only the principal QI value.",
         ["nothing", "the QIII family", "all negative angles"]),
        ("$2\\sin^2\\theta-\\sin\\theta=0$ factors as $\\sin\\theta(2\\sin\\theta-1)=0$. On $[0,2\\pi)$ the solutions include:",
         "0, π, π/6, 5π/6", "$\\sin=0$ or $\\sin=1/2$.", ["π/6 and 5π/6 only", "0 and π only", "π/2"]),
        ("$\\cos^2\\theta=1$ on $[0,2\\pi)$ has solutions:",
         "0 and π", "$\\cos=\\pm 1$. ($2\\pi$ excluded.)", ["0 only", "π/2 and 3π/2", "0, π, 2π"]),
        ("Let $u=\\sin\\theta$. Then $2u^2+u-1=0$ factors as $(2u-1)(u+1)=0$, so $u=1/2$ or $u=-1$. On $[0,2\\pi)$ that means:",
         "π/6, 5π/6, and 3π/2", "Sine $1/2$ twice and sine $-1$ once.", ["π/6 only", "3π/2 only", "π/2 and 3π/2"]),
        ("An equation quadratic in $\\cos\\theta$ should be solved by:",
         "substituting u = cos θ, solving the quadratic, then solving each cosine equation",
         "Do not take arccos of the quadratic expression as a blob.",
         ["dividing by cos²θ immediately", "graphing y=x² only", "using SOH-CAH-TOA on a 3-4-5"]),
        ("$2\\cos^2\\theta-1=0$ is also $\\cos(2\\theta)=0$, so on $[0,2\\pi)$:",
         "θ = π/4, 3π/4, 5π/4, 7π/4", "$2\\theta=\\pi/2+\\pi k$, four values of $\\theta$ in the interval.",
         ["π/2 and 3π/2", "π/4 only", "0 and π"]),
        ("Graphically, solutions of $\\sin\\theta=1/2$ are the $x$-values where $y=\\sin\\theta$ meets the line $y=1/2$. On $[0,2\\pi)$ you see:",
         "two intersection points", "One on the rising side, one on the falling side of the first hump.",
         ["one intersection", "four intersections", "none"]),
        ("The graphs of $y=\\sin\\theta$ and $y=\\cos\\theta$ meet on $[0,2\\pi)$ at:",
         "π/4 and 5π/4", "Where $\\tan\\theta=1$.", ["π/2", "0 and π", "π/6 and 5π/6"]),
        ("A horizontal line $y=2$ meets $y=\\sin\\theta$:",
         "never (no real θ)", "Sine never leaves $[-1,1]$.", ["twice per period", "once", "at θ=2"]),
        ("The number of solutions of $\\cos\\theta=1/3$ on $[0,2\\pi)$ is:",
         "2", "Any value in $(-1,1)$ is hit twice per full period.", ["1", "0", "4"]),
        ("Graphing $y=\\tan\\theta$ against $y=2$ on $(-\\pi/2,3\\pi/2)$ excluding asymptotes shows how many hits?",
         "2", "One hit per $\\pi$-period; the window covers two tangent branches.", ["1", "3", "0"]),
        ("$\\arccos(1/2)$ equals:",
         "π/3", "Not $5\\pi/3$, which is outside arccos's range.", ["5π/3", "π/6", "2π/3"]),
        ("$\\arcsin(\\sqrt{2}/2)$ equals:",
         "π/4", "Principal value, not $3\\pi/4$.", ["3π/4", "π/6", "π/2"]),
        ("$\\arctan(-1)$ equals:",
         "−π/4", "Odd function; not $3\\pi/4$.", ["3π/4", "7π/4", "π/4"]),
        ("$\\sin(\\arcsin(0.3))$ equals:",
         "0.3", "Sine undoes arcsin on $[-1,1]$.", ["arcsin(0.3)", "π/0.3", "1"]),
        ("$\\arcsin(\\sin(2\\pi/3))$ equals:",
         "π/6", "First sine is $\\sqrt{3}/2$, then arcsin returns the QI angle, not $2\\pi/3$.",
         ["2π/3", "π/3", "−π/6"]),
        ("$\\cos\\theta=\\sqrt{3}/2$ on $[0,2\\pi)$:",
         "π/6 and 11π/6", "QI and QIV.", ["π/6 and 5π/6", "π/3 and 5π/3", "π/6 only"]),
        ("$\\sin\\theta=-1/2$ on $[0,2\\pi)$:",
         "7π/6 and 11π/6", "QIII and QIV.", ["π/6 and 5π/6", "4π/3 and 5π/3", "3π/2"]),
        ("General solution of $\\cos\\theta=1$ is:",
         "θ = 2πk", "Only the positive $x$-axis.", ["θ = πk", "θ = π/2 + 2πk", "θ = 0 only, no general form"]),
        ("$4\\sin\\theta-2=0$ on $[0,2\\pi)$:",
         "π/6 and 5π/6", "$\\sin\\theta=1/2$.", ["π/2", "π/3 and 2π/3", "7π/6 and 11π/6"]),
        ("$\\tan\\theta=-\\sqrt{3}$ on $[0,2\\pi)$:",
         "2π/3 and 5π/3", "Reference $\\pi/3$, QII and QIV.", ["π/3 and 4π/3", "π/6 and 7π/6", "4π/3 only"]),
        ("The equation $\\sin\\theta=\\sin\\alpha$ has general solution:",
         "θ = α + 2πk or θ = π − α + 2πk", "The sine-wave symmetry.",
         ["θ = α + 2πk only", "θ = α + πk", "θ = −α only"]),
        ("$u=\\tan\\theta$ in $u^2-3=0$ gives $\\tan\\theta=\\pm\\sqrt{3}$. On $[0,\\pi)$ that is:",
         "π/3 and 2π/3", "One per sign in a $\\pi$-length window that is the natural period of tangent. $[0,\\pi)$ contains $\\pi/3$ (positive) and $2\\pi/3$ (negative).",
         ["π/3 only", "π/6 and π/3", "0 and π/2"]),
        ("Graphically, $\\arccos x$ is the reflection of $y=\\cos x$ on $[0,\\pi]$ across the line:",
         "y=x", "Inverse graphs.", ["x-axis", "y-axis", "y=1"]),
        ("How many solutions of $\\sin(2\\theta)=1/2$ lie in $[0,2\\pi)$?",
         "4", "Let $\\phi=2\\theta\\in[0,4\\pi)$. Four solutions for $\\phi$, hence four for $\\theta$.",
         ["2", "1", "8"]),
        ("$\\cos(2\\theta)=-1$ on $[0,2\\pi)$ gives $2\\theta=\\pi+2\\pi k$, so $\\theta$ equals:",
         "π/2 and 3π/2", "For $k=0,1$ in range.", ["π", "0 and π", "π/4 and 3π/4"]),
        ("A calculator in degree mode returns $\\arcsin(0.5)=30$. In radians that angle is:",
         "π/6", "Do not leave $30$ as a radian answer.", ["30", "π/3", "1/2"]),
        ("SAT Stretch: Solve $2\\sin^2\\theta+\\sin\\theta-1=0$ on $[0,2\\pi)$. Factor $(2\\sin\\theta-1)(\\sin\\theta+1)=0$. Solutions:",
         "π/6, 5π/6, 3π/2",
         "$\\sin=1/2$ or $\\sin=-1$. Then $\\pi/6,5\\pi/6$ and $3\\pi/2$.",
         ["π/6 only", "3π/2 only", "π/6, 5π/6"]),
        ("SAT Stretch: Solve $2\\cos^2\\theta+\\cos\\theta-1=0$ on $[0,2\\pi)$. Solutions:",
         "π/3, π, 5π/3",
         "$(2\\cos\\theta-1)(\\cos\\theta+1)=0$, so $\\cos=1/2$ or $\\cos=-1$. Then $\\pi/3,5\\pi/3$, and $\\pi$.",
         ["π/3 and 5π/3 only", "0, π/3, 5π/3", "π only"]),
        ("SAT Stretch: Evaluate $\\arccos(\\cos(7\\pi/6))+\\arcsin(\\sin(7\\pi/6))$.",
         "2π/3",
         "$\\arccos(\\cos(7\\pi/6))=\\arccos(-\\sqrt{3}/2)=5\\pi/6$ (range $[0,\\pi]$). $\\arcsin(\\sin(7\\pi/6))=\\arcsin(-1/2)=-\\pi/6$. Sum $5\\pi/6-\\pi/6=2\\pi/3$.",
         ["7π/6", "0", "π"]),
        ("SAT Stretch: Solve $\\sin(3\\theta)=0$ on $[0,2\\pi)$. The solutions are:",
         "0, π/3, 2π/3, π, 4π/3, 5π/3",
         "$3\\theta=k\\pi$ with $0\\le 3\\theta<6\\pi$, so $k=0,1,2,3,4,5$ and $\\theta=k\\pi/3$.",
         ["0, π/3, 2π/3", "0, π, 2π", "π/3, 2π/3, π"]),
        ("SAT Stretch: Solve $\\tan\\theta=\\sqrt{3}$ and $\\theta$ in $(-\\pi,\\pi)$. The solutions are:",
         "π/3 and −2π/3", "General $\\pi/3+\\pi k$. In $(-\\pi,\\pi)$: $\\pi/3$ and $\\pi/3-\\pi=-2\\pi/3$.",
         ["π/3 only", "π/3 and 4π/3", "−π/3"]),
        ("SAT Stretch: Solve $\\sin(2\\theta)=\\sqrt{3}/2$ on $[0,2\\pi)$. Then $2\\theta\\in[0,4\\pi)$, so $\\theta$ equals:",
         "π/6, π/3, 7π/6, 4π/3",
         "$2\\theta=\\pi/3,2\\pi/3,7\\pi/3,8\\pi/3$ (the $\\sqrt{3}/2$ sine angles in two full turns). Divide by $2$.",
         ["π/6 and π/3 only", "π/3 and 2π/3", "π/6, 5π/6"]),
        ("SAT Stretch: Inverse: $\\tan(\\arctan 10)$ equals $10$, but $\\arctan(\\tan(3\\pi/4))$ equals:",
         "−π/4", "Tan of $3\\pi/4$ is $-1$; arctan returns the QIV principal value.",
         ["3π/4", "π/4", "5π/4"]),
        ("SAT Stretch: Solve $\\cos(2\\theta)=\\cos\\theta$ on $[0,2\\pi)$ by writing $2\\cos^2\\theta-1=\\cos\\theta$. Solutions:",
         "0, 2π/3, 4π/3",
         "$(2u+1)(u-1)=0$ with $u=\\cos\\theta$ gives $\\cos=1$ or $\\cos=-1/2$. In $[0,2\\pi)$: $0$, $2\\pi/3$, $4\\pi/3$.",
         ["0 only", "2π/3 and 4π/3 only", "π"]),
        ("SAT Stretch: Solve $\\cos\\theta=\\sin 2\\theta$ on $[0,2\\pi)$ by writing $\\sin 2\\theta=2\\sin\\theta\\cos\\theta$. Then $\\cos\\theta(1-2\\sin\\theta)=0$. Solutions:",
         "π/2, 3π/2, π/6, 5π/6", "$\\cos=0$ or $\\sin=1/2$.",
         ["π/6 and 5π/6 only", "π/2 only", "0 and π"]),
    ])


def build_unit7():
    title = "Trigonometry Unit 7: Inverse Trig & Equations"
    description = (
        "Inverse sine, cosine, and tangent; principal ranges; solving on $[0,2\\pi)$; "
        "general solutions; quadratics in disguise; graphical intersections."
    )
    concepts = [
        "Inverse sine cosine tangent",
        "Range of inverses",
        "Solve on [0,2π)",
        "General solution",
        "Quadratic in disguise",
        "Graphical solutions",
    ]

    c1 = concept_block(
        "1. Inverse sine, cosine, and tangent",
        [
            "The inverse sine $\\arcsin x$ (also $\\sin^{-1}x$) is the unique angle in $[-\\pi/2,\\pi/2]$ whose sine is $x$. "
            "It is not $1/\\sin x$; that is cosecant. The superscript $-1$ means inverse function, not reciprocal.",
            "Inverse cosine $\\arccos x$ returns the unique angle in $[0,\\pi]$ whose cosine is $x$. "
            "Inverse tangent $\\arctan x$ returns the unique angle in $(-\\pi/2,\\pi/2)$ whose tangent is $x$, for any real $x$.",
            "A calculator's $\\sin^{-1}$ button is $\\arcsin$. It will never output $5\\pi/6$ for $\\arcsin(1/2)$, even though sine is also $1/2$ there. "
            "The second solution is your job, using a reference angle and a quadrant.",
            "Composition: $\\sin(\\arcsin x)=x$ for $x\\in[-1,1]$. The other way, $\\arcsin(\\sin\\theta)=\\theta$ only when $\\theta$ is already in $[-\\pi/2,\\pi/2]$. "
            "$\\arcsin(\\sin(2\\pi/3))=\\arcsin(\\sqrt{3}/2)=\\pi/3$, not $2\\pi/3$.",
            "Exact values reuse Unit 1 and Unit 2: $\\arcsin(1/2)=\\pi/6$, $\\arccos(-1)=\\pi$, $\\arctan(1)=\\pi/4$, $\\arctan(-1)=-\\pi/4$.",
            "When a problem asks for $\\theta=\\arcsin(3/5)$, that is an exact symbolic answer unless a decimal is requested. Do not force a calculator approximation as the only form.",
        ],
        "Every trigonometric equation's first solution is an inverse evaluation. If you treat that first solution as the only solution, you will miss the second (or infinite) family.",
        "Evaluate the inverse to get the principal angle. Then, if the original problem is an equation on a larger interval, build the other angles from that reference.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#94a3b8", sample_curve(lambda x: math.sin(x), -math.pi, 1.5 * math.pi, n=110)),
                    ("#4f46e5", sample_curve(lambda x: math.sin(x), -math.pi / 2, math.pi / 2, n=50)),
                ],
                xlim=(-math.pi, 1.5 * math.pi), ylim=(-1.5, 1.5), w=340, h=220, xlab="θ", ylab="sin θ",
                dashes=[("v", -math.pi / 2, "-π/2"), ("v", math.pi / 2, "π/2")],
            ),
            "Arcsin uses only the increasing sine branch on $[-\\pi/2,\\pi/2]$ (indigo)",
            "The gray continuation of the sine wave is ignored. That is why $\\arcsin(1/2)=\\pi/6$ rather than $5\\pi/6$.",
        )
        + solved(1, "Evaluate $\\arcsin(1/2)$ and $\\arccos(1/2)$.",
                 ["$\\arcsin(1/2)=\\pi/6$.",
                  "$\\arccos(1/2)=\\pi/3$."],
                 "$\\pi/6$ and $\\pi/3$", "Same input, different ranges, different outputs.", "Easy")
        + solved(2, "Evaluate $\\arctan(-1)$ and $\\arcsin(-1)$.",
                 ["Arctan is odd: $\\arctan(-1)=-\\pi/4$.",
                  "$\\arcsin(-1)=-\\pi/2$."],
                 "$-\\pi/4$ and $-\\pi/2$", "", "Medium")
        + solved(3, "Simplify $\\arcsin(\\sin(2\\pi/3))$.",
                 ["$\\sin(2\\pi/3)=\\sqrt{3}/2$.",
                  "$\\arcsin(\\sqrt{3}/2)=\\pi/3$, the QI angle in range.",
                  "Not $2\\pi/3$, which sits outside $[-\\pi/2,\\pi/2]$."],
                 "$\\pi/3$", "", "Hard"),
        ("Reading $\\sin^{-1}x$ as $1/\\sin x$",
         "The reciprocal is $\\csc x$ or $(\\sin x)^{-1}$ with parentheses on the function value. $\\sin^{-1}x$ is the inverse function."),
        ("Trust the range more than a unit-circle habit that always prefers $[0,2\\pi)$",
         "Principal values can be negative. $\\arcsin(-1/2)=-\\pi/6$ is correct, even though $11\\pi/6$ is a popular coterminal."),
        ["I can evaluate arcsin, arccos, and arctan at special values.",
         "I know $\\sin^{-1}$ is not cosecant.",
         "I can simplify $\\arcsin(\\sin\\theta)$ when $\\theta$ is outside the range."],
        1,
    )

    c2 = concept_block(
        "2. Range of inverses",
        [
            "Why those particular ranges? Sine is one-to-one on $[-\\pi/2,\\pi/2]$, covering its full range $[-1,1]$. "
            "Cosine is one-to-one on $[0,\\pi]$. Tangent is one-to-one on $(-\\pi/2,\\pi/2)$, covering all reals.",
            "The graph of $y=\\arcsin x$ is the reflection of that sine piece across $y=x$. It runs from $(-1,-\\pi/2)$ to $(1,\\pi/2)$. "
            "The graph of $y=\\arccos x$ runs from $(-1,\\pi)$ down to $(1,0)$ — it is decreasing.",
            "Arctan has horizontal asymptotes $y=\\pm\\pi/2$. It never actually reaches those values, which is why its range is open.",
            "Domain of arcsin and arccos is $[-1,1]$. Domain of arctan is all reals. Asking $\\arcsin(2)$ is not a real-number question.",
            "A range error shows up as a wrong second-quadrant arccos: $\\arccos(-1/2)=2\\pi/3$, not $4\\pi/3$. The latter is a solution of $\\cos\\theta=-1/2$ but is not the inverse value.",
            "Remembering three intervals — $[-\\pi/2,\\pi/2]$, $[0,\\pi]$, $(-\\pi/2,\\pi/2)$ — is the entire lesson in one line. Write them at the top of any inverse-trig quiz.",
        ],
        "Range is the difference between 'an angle whose sine is $1/2$' and 'the inverse-sine of $1/2$'. Tests punish mixing those two sentences.",
        "Memorize the three ranges. When an inverse output is asked, it must sit in that interval, even if another coterminal angle feels more familiar.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: math.asin(max(-1, min(1, x))), -1, 1, n=50))],
                xlim=(-1.3, 1.3), ylim=(-2, 2), w=300, h=240, xlab="x", ylab="arcsin x",
            ),
            "The graph of $y=\\arcsin x$ on $[-1,1]$",
            "Outputs stay between $-\\pi/2$ and $\\pi/2$. The curve is increasing and passes through the origin.",
        )
        + solved(4, "State the range of $\\arcsin$, $\\arccos$, and $\\arctan$.",
                 ["$[-\\pi/2,\\pi/2]$, $[0,\\pi]$, $(-\\pi/2,\\pi/2)$."],
                 "those three intervals", "", "Easy")
        + solved(5, "Why is $\\arccos(-1)=\\pi$ rather than $-\\pi$ or $3\\pi$?",
                 ["Only $\\pi$ lies in $[0,\\pi]$ and has cosine $-1$.",
                  "$-\\pi$ is outside the range. $3\\pi$ is coterminal with $\\pi$ but not the principal value."],
                 "$\\pi$", "", "Medium")
        + solved(6, "Explain why $\\arctan x$ never equals $\\pi/2$.",
                 ["Tangent has a vertical asymptote at $\\pi/2$ and never attains a value there.",
                  "The inverse therefore never outputs $\\pi/2$; it only approaches it as $x\\to\\infty$."],
                 "range is open at $\\pm\\pi/2$", "", "Hard"),
        ("Using $[0,2\\pi)$ as the range of every inverse",
         "That interval is for solving equations, not for inverse outputs. Arcsin lives on a half-sized, possibly negative interval."),
        ("Write the three ranges before touching a single problem",
         "Then every inverse evaluation is a matching question: which angle in that interval has the given sine/cosine/tangent?"),
        ["I can state all three inverse ranges.",
         "I can state the domains $[-1,1]$ vs all reals.",
         "I can reject a coterminal angle that sits outside the principal range."],
        6,
    )

    c3 = concept_block(
        "3. Solve on $[0,2\\pi)$",
        [
            "A standard exam window is one full rotation, $[0,2\\pi)$ or sometimes $[0,2\\pi]$. Watch whether $2\\pi$ is included; if sine is $0$, that choice matters.",
            "Method: find the reference angle from the inverse of the absolute value. Place that reference in every quadrant where the function has the required sign. Discard anything outside the window.",
            "Sine $1/2$: reference $\\pi/6$, QI and QII: $\\pi/6,5\\pi/6$. Sine $-1/2$: QIII and QIV: $7\\pi/6,11\\pi/6$. "
            "Cosine $-1/2$: QII and QIII: $2\\pi/3,4\\pi/3$. Tangent $1$: QI and QIII: $\\pi/4,5\\pi/4$.",
            "If the value is $\\pm 1$ or $0$, use axis angles rather than a two-quadrant dance. $\\sin\\theta=1$ is only $\\pi/2$. $\\cos\\theta=-1$ is only $\\pi$ in this window.",
            "If the equation is $\\sin(2\\theta)=1/2$, first solve for $2\\theta$ on $[0,4\\pi)$, then divide by $2$. Doubling the angle doubles the number of solutions in a $2\\pi$ window for $\\theta$.",
            "Always list solutions in increasing order and check each in the original equation if you divided or squared along the way.",
        ],
        "This is the default SAT/ACT trig-equation setting. Missing the second quadrant solution is the most expensive small mistake in the unit.",
        "Reference angle, ASTC signs, list candidates, keep those in $[0,2\\pi)$. If the argument is $n\\theta$, expand the window for $n\\theta$ first.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: math.sin(x), 0, 2 * math.pi, n=90))],
                dashes=[("h", 0.5, "y=1/2")],
                xlim=(0, 2 * math.pi), ylim=(-1.4, 1.4), w=340, h=200, xlab="θ", ylab="y",
            ),
            "$y=\\sin\\theta$ meeting $y=1/2$ on $[0,2\\pi)$",
            "Two intersections: $\\pi/6$ and $5\\pi/6$. The picture is the argument that a second solution exists.",
        )
        + solved(7, "Solve $\\sin\\theta=1/2$ on $[0,2\\pi)$.",
                 ["Reference $\\pi/6$. Sine positive in QI and QII.",
                  "$\\theta=\\pi/6,5\\pi/6$."],
                 "$\\pi/6,5\\pi/6$", "", "Easy")
        + solved(8, "Solve $\\cos\\theta=-1/2$ on $[0,2\\pi)$.",
                 ["Reference $\\pi/3$. Cosine negative in QII and QIII.",
                  "$\\theta=2\\pi/3,4\\pi/3$."],
                 "$2\\pi/3,4\\pi/3$", "", "Medium")
        + solved(9, "Solve $\\sin(2\\theta)=1/2$ on $[0,2\\pi)$.",
                 ["Let $\\phi=2\\theta$. Then $\\phi\\in[0,4\\pi)$.",
                  "$\\phi=\\pi/6,5\\pi/6,\\pi/6+2\\pi,5\\pi/6+2\\pi=\\pi/6,5\\pi/6,13\\pi/6,17\\pi/6$.",
                  "$\\theta=\\phi/2=\\pi/12,5\\pi/12,13\\pi/12,17\\pi/12$."],
                 "$\\pi/12,5\\pi/12,13\\pi/12,17\\pi/12$", "Four solutions, twice as many as the $B=1$ case.", "Hard"),
        ("Stopping after the calculator's single inverse output",
         "That is one solution. Sine and cosine equations almost always have two in a $2\\pi$ window when the target is in $(-1,1)$."),
        ("For $n\\theta$, solve for $n\\theta$ on $[0,2n\\pi)$ before dividing",
         "Dividing the original window by $n$ too early drops solutions."),
        ["I can solve $\\sin\\theta=c$ and $\\cos\\theta=c$ on $[0,2\\pi)$.",
         "I can solve $\\tan\\theta=c$ using period $\\pi$.",
         "I can handle $\\sin(n\\theta)=c$ by expanding the inner window."],
        11,
    )

    c4 = concept_block(
        "4. General solution",
        [
            "A general solution lists every real angle, using an integer $k$. "
            "For sine: if $\\theta_0=\\arcsin c$ (principal) and $c\\in[-1,1]$, then $\\theta=\\theta_0+2\\pi k$ or $\\theta=\\pi-\\theta_0+2\\pi k$.",
            "For cosine: $\\theta=\\pm\\theta_0+2\\pi k$ where $\\theta_0=\\arccos c$. For tangent: $\\theta=\\theta_0+\\pi k$ where $\\theta_0=\\arctan c$.",
            "The tangent family is 'thinner' because the period is $\\pi$. Writing $\\pi/4+2\\pi k$ and $5\\pi/4+2\\pi k$ is correct but not compact; $\\pi/4+\\pi k$ already contains both.",
            "Axis equations have one family: $\\sin\\theta=0$ is $\\theta=\\pi k$, $\\cos\\theta=0$ is $\\theta=\\pi/2+\\pi k$, $\\sin\\theta=1$ is $\\theta=\\pi/2+2\\pi k$.",
            "To recover the $[0,2\\pi)$ list from a general solution, plug in integers $k$ until you leave the window. That is a useful check.",
            "If the original equation had a restricted domain from a tangent or secant, discard general-solution values that make a denominator zero even if they formally satisfy a rewritten equation.",
        ],
        "Physics phases, polar graphs, and precalculus 'all real solutions' prompts all want the $k$-form, not a two-item list.",
        "Write the two sine families (or the one tangent family). Use $k\\in\\mathbb{Z}$. Compactify tangent with $\\pi k$. Scan for undefined extras.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: math.sin(x), -2 * math.pi, 4 * math.pi, n=120))],
                dashes=[("h", 0.5, "y=1/2")],
                xlim=(-2 * math.pi, 4 * math.pi), ylim=(-1.4, 1.4), w=360, h=200, xlab="θ", ylab="y",
            ),
            "The line $y=1/2$ hits the sine wave forever — that is the general solution",
            "Each $2\\pi$ block contributes the same two $x$-offsets $\\pi/6$ and $5\\pi/6$. The integer $k$ counts blocks.",
        )
        + solved(10, "Write the general solution of $\\sin\\theta=1/2$.",
                 ["$\\theta=\\pi/6+2\\pi k$ or $\\theta=5\\pi/6+2\\pi k$, $k\\in\\mathbb{Z}$."],
                 "those two families", "", "Easy")
        + solved(11, "Write the general solution of $\\tan\\theta=1$.",
                 ["$\\theta=\\pi/4+\\pi k$."],
                 "$\\pi/4+\\pi k$", "The compact $\\pi k$ form is preferred over two $2\\pi$ families.", "Medium")
        + solved(12, "Write the general solution of $\\cos\\theta=0$.",
                 ["$\\theta=\\pi/2+\\pi k$.",
                  "Check: $k=0$ gives $\\pi/2$, $k=1$ gives $3\\pi/2$, $k=2$ gives $5\\pi/2$, all cosine zeros."],
                 "$\\pi/2+\\pi k$", "", "Hard"),
        ("Writing only the arcsin family for a sine equation",
         "You are missing $\\pi-\\theta_0+2\\pi k$, the QII/QIII partner depending on the sign of sine."),
        ("Use $\\pi k$ for tangent, $2\\pi k$ for sine/cosine families",
         "Mixing those steps either duplicates solutions or drops half of them."),
        ["I can write sine's two-family general solution.",
         "I can write tangent's $\\theta_0+\\pi k$ solution.",
         "I can specialize a general solution to $[0,2\\pi)$ by testing $k$."],
        16,
    )

    c5 = concept_block(
        "5. Quadratic in disguise",
        [
            "Many equations are quadratic after a substitution $u=\\sin\\theta$ or $u=\\cos\\theta$ or $u=\\tan\\theta$. "
            "$2\\sin^2\\theta-\\sin\\theta=0$ is $2u^2-u=0$. $2\\cos^2\\theta-3\\cos\\theta+1=0$ is a factorable quadratic in $u=\\cos\\theta$.",
            "Factor or use the quadratic formula on $u$, then solve each resulting linear trig equation on the requested window.",
            "Pythagorean substitution can create the quadratic: $2\\sin^2\\theta-\\cos\\theta=0$ becomes $2(1-\\cos^2)-\\cos=0$, a quadratic in cosine.",
            "Never divide by $\\sin\\theta$ to 'simplify' a quadratic that has a $\\sin\\theta=0$ root. Factor instead.",
            "After finding $u$, discard any $u$ outside the range of the function ($|u|>1$ for sine/cosine). Those extra quadratic roots are not angles.",
            "Double-angle forms are quadratics in disguise too: $2\\cos^2\\theta-1=1/2$ is $\\cos 2\\theta=1/2$, which may be easier than expanding.",
        ],
        "The difference between a one-step inverse and a contest equation is usually one substitution $u=\\sin\\theta$. Seeing that $u$ is the whole game.",
        "Name $u$. Solve the algebra problem completely. Throw away illegal $u$. Then solve the leftover trig equations with reference angles.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: 2 * math.sin(x) ** 2 - math.sin(x), 0, 2 * math.pi, n=90))],
                dashes=[("h", 0, "y=0")],
                xlim=(0, 2 * math.pi), ylim=(-1.5, 2.2), w=340, h=200, xlab="θ", ylab="y",
            ),
            "$y=2\\sin^2\\theta-\\sin\\theta$ crossing zero — a quadratic in $\\sin\\theta$",
            "The zeros are where $\\sin\\theta=0$ or $\\sin\\theta=1/2$: namely $0$ and $\\pi$, plus $\\pi/6$ and $5\\pi/6$ on $[0,2\\pi)$.",
        )
        + solved(13, "Solve $2\\sin^2\\theta-\\sin\\theta=0$ on $[0,2\\pi)$.",
                 ["$\\sin\\theta(2\\sin\\theta-1)=0$.",
                  "$\\sin\\theta=0$ or $1/2$.",
                  "$\\theta=0,\\pi,\\pi/6,5\\pi/6$."],
                 "$0,\\pi/6,5\\pi/6,\\pi$", "", "Easy")
        + solved(14, "Solve $2\\cos^2\\theta-3\\cos\\theta+1=0$ on $[0,2\\pi)$.",
                 ["$(2\\cos\\theta-1)(\\cos\\theta-1)=0$.",
                  "$\\cos\\theta=1/2$ or $1$.",
                  "$\\theta=0,\\pi/3,5\\pi/3$."],
                 "$0,\\pi/3,5\\pi/3$", "", "Medium")
        + solved(15, "Solve $2\\sin^2\\theta-\\cos\\theta=0$ on $[0,2\\pi)$.",
                 ["$2(1-\\cos^2\\theta)-\\cos\\theta=0$.",
                  "$2-2u^2-u=0$ with $u=\\cos\\theta$, so $2u^2+u-2=0$.",
                  "$u=(-1\\pm\\sqrt{17})/4$. Keep only the value in $[-1,1]$. $(-1+\\sqrt{17})/4\\approx 0.78$ is legal; $(-1-\\sqrt{17})/4\\approx -1.28$ is not.",
                  "Then $\\theta=\\pm\\arccos\\big((-1+\\sqrt{17})/4\\big)+2\\pi k$, and list the two values in $[0,2\\pi)$."],
                 "two angles whose cosine is $(-1+\\sqrt{17})/4$", "Discarding $|u|>1$ is part of the solution, not a side note.", "Hard"),
        ("Dividing by $\\sin\\theta$ in $2\\sin^2-\\sin=0$",
         "You lose $\\sin\\theta=0$. Factor. The zero root is often $0$ or $\\pi$, easy points to drop and easy points to check."),
        ("After the quadratic, ask whether $|u|\\le 1$",
         "A perfectly real quadratic root can still be an impossible sine. Cross it out before hunting angles."),
        ["I can substitute $u=\\sin\\theta$ and factor.",
         "I can use Pythagoras to create a quadratic in one function.",
         "I can discard $u$ outside $[-1,1]$."],
        21,
    )

    c6 = concept_block(
        "6. Graphical solutions",
        [
            "Every trig equation $\\sin\\theta=c$ is the intersection of a wave and a horizontal line. "
            "If $|c|>1$, the line misses the wave: no real solution. If $|c|=1$, they kiss at the peaks. If $|c|<1$, two intersections per $2\\pi$ for sine/cosine.",
            "Tangent versus a horizontal line $y=c$ hits once per $\\pi$-branch, forever, for every real $c$.",
            "Two waves, such as $y=\\sin\\theta$ and $y=\\cos\\theta$, intersect where $\\tan\\theta=1$ (and cosine is nonzero). The graph makes the count obvious: two hits per $2\\pi$.",
            "A transformed wave $y=2\\sin(3\\theta)$ versus $y=1$ is $\\sin(3\\theta)=1/2$. The graph on $[0,2\\pi)$ will show six intersections because three full sine cycles each contribute two hits.",
            "Graphing is also how you detect extras after a rewrite. If you squared both sides, the graph of the original may have fewer intersections than the squared equation. Check candidates.",
            "On a test without a grapher, a quick sketch of one period plus a dashed target line is enough to know whether the answer should list one, two, or four angles.",
        ],
        "Counting intersections is a sanity check on algebraic lists. If algebra produced three solutions for $\\sin\\theta=1/2$ on $[0,2\\pi)$, the sketch says one of them is an impostor.",
        "Sketch the wave, draw the target line, count hits in the window, then name the hits with reference angles.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#4f46e5", sample_curve(lambda x: math.sin(x), 0, 2 * math.pi, n=90)),
                    ("#0f766e", sample_curve(lambda x: math.cos(x), 0, 2 * math.pi, n=90)),
                ],
                xlim=(0, 2 * math.pi), ylim=(-1.4, 1.4), w=340, h=200, xlab="θ", ylab="y",
            ),
            "$y=\\sin\\theta$ and $y=\\cos\\theta$ on $[0,2\\pi)$",
            "They cross twice, at $\\pi/4$ and $5\\pi/4$. A third crossing would contradict the algebra $\\tan\\theta=1$.",
        )
        + solved(16, "How many solutions does $\\sin\\theta=1/2$ have on $[0,2\\pi)$? Use a graph argument.",
                 ["The line $y=1/2$ cuts the sine hump twice, once rising and once falling.",
                  "Two solutions."],
                 "2", "", "Easy")
        + solved(17, "How many solutions does $2\\sin(3\\theta)=1$ have on $[0,2\\pi)$?",
                 ["$\\sin(3\\theta)=1/2$. Three full sine cycles live in the window.",
                  "Each cycle contributes two solutions: $3\\times 2=6$."],
                 "6", "", "Medium")
        + solved(18, "Explain graphically why $\\sin\\theta=2$ has no real solution.",
                 ["The sine wave lives between $-1$ and $1$.",
                  "The line $y=2$ never meets it."],
                 "no intersection", "", "Hard"),
        ("Counting peaks instead of intersections",
         "A peak is an intersection only if the target line is $y=\\pm 1$ (for a parent sine). For $y=1/2$, the hits are on the sides of the hump, not at the top."),
        ("Sketch one clear period before counting",
         "Then multiply by how many periods fit in the requested window. That is faster and safer than listing in a fog."),
        ["I can count sine/line intersections on one period.",
         "I can scale that count when $B\\neq 1$.",
         "I can see when $|c|>1$ produces no real solution."],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
        stretch_note=STRETCH_LABEL,
    )
    return title, description, content, _u7_questions()


# ===========================================================================
# UNIT 8: Laws of Sines & Cosines
# ===========================================================================

def _u8_questions():
    return _pack([
        ("The law of sines says $\\dfrac{a}{\\sin A}=\\dfrac{b}{\\sin B}=\\dfrac{c}{\\sin C}$ equals:",
         "2R (the circumdiameter)", "Also described as a common ratio; numerically you often just equate two fractions.",
         ["the area", "a+b+c", "1"]),
        ("In AAS, you know two angles and a non-included side. The third angle is:",
         "180° minus the two known angles", "Then law of sines finds the remaining sides.", ["impossible to find", "90° always", "the included angle only"]),
        ("ASA uses the law of sines after you:",
         "find the third angle, then pair each side with its opposite angle", "The included side sits opposite the third angle.",
         ["jump to the law of cosines", "assume a right triangle", "drop an altitude first always"]),
        ("If $A=40^\\circ$, $B=60^\\circ$, $a=10$, then $C$ equals:",
         "80°", "$180-40-60=80$.", ["100°", "20°", "90°"]),
        ("With $A=30^\\circ$, $B=70^\\circ$, $a=8$, the law of sines gives $b$ as:",
         "8 sin 70° / sin 30°", "$b=a\\sin B/\\sin A$.", ["8 sin 30° / sin 70°", "8", "80"]),
        ("SSA is called ambiguous because:",
         "two triangles, one triangle, or none may exist", "The swinging side $a$ can miss the line, just touch, or cut twice.",
         ["angles can be negative", "the law of sines fails", "area is undefined"]),
        ("In SSA with acute $A$, if $a<b\\sin A$, the number of triangles is:",
         "0", "Side $a$ is too short to reach the opposite line.", ["1", "2", "3"]),
        ("In SSA with acute $A$, if $b\\sin A<a<b$, the number of triangles is:",
         "2", "The classic two-triangle ambiguous case.", ["0", "1", "infinitely many"]),
        ("In SSA with acute $A$, if $a>b$, the number of triangles is:",
         "1", "The swinging side is long enough to force a single triangle (the obtuse-at-$B$ option cannot close).",
         ["2", "0", "3"]),
        ("Given $a=8$, $A=30^\\circ$, $b=10$. Then $b\\sin A=5$ and $a$ sits between $5$ and $10$, so the number of triangles is:",
         "2", "Ambiguous SSA with two triangles.", ["0", "1", "4"]),
        ("The law of cosines for side $c$ is:",
         "c² = a² + b² − 2ab cos C", "SAS or SSS engine.", ["c² = a² + b² + 2ab cos C", "c = a + b − cos C", "c² = a² − b²"]),
        ("When $C=90^\\circ$, the law of cosines becomes:",
         "c² = a² + b²", "Pythagoras is the right-angle special case.", ["c² = a² − b²", "c = ab", "c² = 2ab"]),
        ("SSS: $a=5$, $b=6$, $c=7$. Then $\\cos C$ equals:",
         "1/5", "$(a^2+b^2-c^2)/(2ab)=(25+36-49)/60=12/60=1/5$.",
         ["49/60", "−1/5", "12/35"]),
        ("SAS: $a=7$, $b=8$, $C=60^\\circ$. Then $c^2$ equals:",
         "57", "$49+64-2\\cdot7\\cdot8\\cdot(1/2)=113-56=57$.", ["113", "15", "64"]),
        ("If $\\cos C$ comes out negative in the law of cosines, angle $C$ is:",
         "obtuse", "Cosine is negative in QII, and triangle angles sit in $(0^\\circ,180^\\circ)$.",
         ["acute", "right", "impossible"]),
        ("The area of a triangle with SAS data $b$, $C$, $a$ is:",
         "(1/2)ab sin C", "One-half product of two sides times sine of the included angle.",
         ["(1/2)ab", "ab sin C", "(1/2)(a+b) sin C"]),
        ("Two sides $5$ and $8$ with included angle $30^\\circ$ have area:",
         "10", "$(1/2)\\cdot 5\\cdot 8\\cdot(1/2)=10$.", ["20", "40", "5"]),
        ("If area $=12$ and $a=6$, $b=8$, then $\\sin C$ equals:",
         "1/2", "$12=(1/2)\\cdot 6\\cdot 8\\cdot\\sin C=24\\sin C$.", ["2", "12", "1"]),
        ("AAS area can be found after law of sines produces a second side, or by:",
         "(1/2)bc sin A once those letters are known", "Same SAS area formula after filling parts.",
         ["Heron only", "dropping a perpendicular is illegal", "assuming a right angle"]),
        ("The area formula $(1/2)ab\\sin C$ requires the angle to be:",
         "the included angle between those two sides", "Not an opposite angle unless you relabel.",
         ["always angle A", "the largest angle only", "an exterior angle"]),
        ("A bearing of N $30^\\circ$ E means:",
         "30° east of north", "Start at north, rotate $30^\\circ$ toward east.", ["30° north of east", "azimuth 30° west", "a heading of 300°"]),
        ("A ship sails 10 km on bearing N $45^\\circ$ E, then 10 km south. The straight-line distance from the start is found by:",
         "the law of cosines in the triangle of path legs", "The included angle at the turn can be read from the bearings.",
         ["SOH-CAH-TOA only if you ignore the turn", "adding 20 km", "the law of sines with no angles"]),
        ("From a point, town A is 8 km due north and town B is 8 km on a bearing N $60^\\circ$ E. Distance AB uses:",
         "SAS with included 60°", "Two sides and the angle between the north line and the bearing.",
         ["SSS with no angle", "right triangle 45-45 only", "SSA ambiguous"]),
        ("Interior angle between bearings N $20^\\circ$ E and S $40^\\circ$ E at a turning point is:",
         "120°", "Draw north-south; the turn from 20° east of north around to 40° east of south is $180^\\circ-20^\\circ-40^\\circ=120^\\circ$.",
         ["60°", "20°", "40°"]),
        ("Bearings are always measured from a north-south line, never from:",
         "an arbitrary side of the triangle without a compass sketch", "Always sketch N-S-E-W first.",
         ["north", "the ground", "a map"]),
        ("Heron's formula: with semi-perimeter $s$, area equals:",
         "√[s(s−a)(s−b)(s−c)]", "SSS area without an angle.", ["s(s−a)(s−b)(s−c)", "(1/2)ab", "abc/4R"]),
        ("Sides $13,14,15$ have $s=21$. Then $s-a$ if $a=15$ is:",
         "6", "$21-15=6$. The other factors are $8$ and $7$.", ["21", "15", "1"]),
        ("Area of a $13$-$14$-$15$ triangle is:",
         "84", "$\\sqrt{21\\cdot 6\\cdot 7\\cdot 8}=\\sqrt{7056}=84$.", ["91", "42", "105"]),
        ("Heron requires:",
         "all three sides", "That is why it pairs with SSS.", ["two angles", "a right angle", "one side only"]),
        ("If Heron produces a negative under the square root, the three lengths:",
         "fail the triangle inequality", "They do not form a triangle, so area is not real.",
         ["form a right triangle", "need the law of sines", "have area 0"]),
        ("Law of sines with $A=45^\\circ$, $a=5\\sqrt{2}$, $B=60^\\circ$ gives $b=$:",
         "5√3", "$b=5\\sqrt{2}\\cdot\\sin 60^\\circ/\\sin 45^\\circ=5\\sqrt{2}\\cdot(\\sqrt{3}/2)/(\\sqrt{2}/2)=5\\sqrt{3}$.",
         ["5√6", "5", "5√2"]),
        ("In triangle with $A=20^\\circ$, $B=40^\\circ$, $c=10$, side $c$ is opposite $C=120^\\circ$. Then $a=$:",
         "10 sin 20° / sin 120°", "$\\sin 120=\\sin 60=\\sqrt{3}/2$.", ["10", "10 sin 120° / sin 20°", "20"]),
        ("SSA: $A=40^\\circ$, $a=12$, $b=15$. Compute $h=b\\sin A$ to classify. $h=$:",
         "15 sin 40°", "Compare $12$ with that height and with $15$.", ["12", "15", "40"]),
        ("If SSA produces $\\sin B=1.2$, then:",
         "no triangle", "Sine cannot exceed $1$.", ["two triangles", "one right triangle", "an obtuse triangle"]),
        ("Law of cosines with $a=4$, $b=5$, $C=120^\\circ$ gives $c^2=$:",
         "61", "$c^2=16+25-2\\cdot4\\cdot5\\cdot(-1/2)=41+20=61$.", ["21", "41", "16"]),
        ("SSS largest angle is opposite the longest side. For sides $6,8,10$ the angle opposite $10$ is:",
         "90°", "$6^2+8^2=10^2$, a right triangle.", ["acute", "obtuse", "60°"]),
        ("Area with $a=10$, $b=10$, $C=90^\\circ$ is:",
         "50", "$(1/2)\\cdot 10\\cdot 10\\cdot 1=50$.", ["100", "25", "10√2"]),
        ("A plane flies 100 km north, then 100 km on bearing N $60^\\circ$ E. Distance from start uses law of cosines with included angle:",
         "120°", "The direction change from due north to N $60^\\circ$ E is not $60^\\circ$ of interior angle in the position triangle; the two path legs meet at $180^\\circ-60^\\circ=120^\\circ$.",
         ["60°", "90°", "30°"]),
        ("Heron for an equilateral side $6$: $s=9$, area $=$:",
         "9√3", "$\\sqrt{9\\cdot 3\\cdot 3\\cdot 3}=\\sqrt{243}=9\\sqrt{3}$, matching $(s^2\\sqrt{3})/4=9\\sqrt{3}$.",
         ["36", "18", "6√3"]),
        ("The law of sines can find an angle from SSA by $\\sin B=b\\sin A/a$. If that $\\sin B$ is between $0$ and $1$ and $A$ is acute, the two candidate angles are $B$ and:",
         "180° − B", "The supplementary candidate; keep it only if $A+(180-B)<180$.",
         ["90° − B", "B/2", "2B"]),
        ("SAS with included $90^\\circ$ still allows law of cosines, which reduces to Pythagoras, or you may use:",
         "right-triangle trig", "Both are consistent.", ["Heron only", "SSA ambiguous", "bearings only"]),
        ("A triangle with sides $2,3,6$ has Heron discriminant:",
         "negative (not a triangle)", "$2+3<6$.", ["positive", "zero", "84"]),
        ("The common law-of-sines ratio $a/\\sin A$ equals $2R$. If $a=10$ and $A=30^\\circ$, $R$ equals:",
         "10", "$10/(1/2)=20=2R$ so $R=10$.", ["5", "20", "30"]),
        ("Area of SAS with $a=13$, $b=14$, and $\\sin C=3/5$ equals:",
         "273/5", "$(1/2)\\cdot 13\\cdot 14\\cdot(3/5)=91\\cdot(3/5)=273/5$.",
         ["91", "182", "39"]),
        ("In ASA, the included side is opposite the third angle. After finding that angle, the first law-of-sines pair uses:",
         "the included side and the third angle", "They are opposites.", ["the two given angles only", "law of cosines", "Heron"]),
        ("Obtuse SSA: if $A$ is obtuse and $a\\le b$, the number of triangles is:",
         "0", "An obtuse angle must be opposite the longest side.", ["2", "1 always", "3"]),
        ("SAT Stretch: SSA with $A=30^\\circ$, $a=8$, $b=12$. The two possible lengths of side $c$ are:",
         "6√3 ± 2√7",
         "Law of cosines: $8^2=12^2+c^2-2\\cdot 12\\cdot c\\cdot\\cos 30^\\circ$ becomes $c^2-12\\sqrt{3}\\,c+80=0$. "
         "Then $c=[12\\sqrt{3}\\pm\\sqrt{112}]/2=6\\sqrt{3}\\pm 2\\sqrt{7}$.",
         ["6√3", "8 and 12", "6√3 ± √7"]),
        ("SAT Stretch: SAS $a=5$, $b=5$, $C=120^\\circ$. The area is:",
         "25√3/4",
         "$(1/2)\\cdot 5\\cdot 5\\cdot\\sin 120^\\circ=(25/2)(\\sqrt{3}/2)=25\\sqrt{3}/4$. (The third side is $5\\sqrt{3}$, but the area does not need it.)",
         ["25√3/2", "5√3", "14√3"]),
        ("SAT Stretch: SSS sides $13,14,15$. Cosine of the angle opposite $15$ equals:",
         "5/13",
         "$(13^2+14^2-15^2)/(2\\cdot 13\\cdot 14)=(169+196-225)/364=140/364=5/13$. Positive, so that angle is acute.",
         ["9/13", "-5/13", "15/14"]),
        ("SAT Stretch: Two SSA triangles from acute $A=30^\\circ$, side $a$, and side $b$ have $B_1=40^\\circ$ and $B_2=140^\\circ$. Areas use the shared pair $(b,A)$, so the area ratio is $c_1:c_2=\\sin C_1:\\sin C_2$. With $C_1=110^\\circ$ and $C_2=10^\\circ$, the area ratio is:",
         "sin 110° : sin 10°",
         "Area $=(1/2)bc\\sin A$ with $b$ and $A$ fixed, so areas scale with $c$. By the law of sines, $c\\propto\\sin C$.",
         ["1 : 1", "sin 40° : sin 140°", "2 : 1"]),
        ("SAT Stretch: A surveyor at $S$ sees a tower at bearing N $20^\\circ$ E. After walking $200$ m due east to $T$, the bearing is N $10^\\circ$ W. In $\\triangle ST$ (tower), angle at $S$ between north and the first sight is $20^\\circ$, and the path $ST$ is east, so angle between $ST$ and the first sight is $70^\\circ$. This is an application of:",
         "AAS or ASA after the second bearing produces another angle", "Two angles and a side (the walk) determine the triangle.",
         ["SSS only", "right-triangle SOH only", "Heron without sides"]),
        ("SAT Stretch: Heron with sides $25,25,14$. Then $s=32$, area $=\\sqrt{32\\cdot 7\\cdot 7\\cdot 18}=$:",
         "168", "$32\\cdot 18=576$, $7\\cdot 7=49$, $576\\cdot 49=28224$, $\\sqrt{28224}=168$.",
         ["175", "84", "196"]),
        ("SAT Stretch: An SSA ambiguous case with $A=40^\\circ$ produces $B=60^\\circ$ and $B=120^\\circ$. The sum of the two possible third angles $C$ is:",
         "100°",
         "$C_1=180^\\circ-40^\\circ-60^\\circ=80^\\circ$ and $C_2=180^\\circ-40^\\circ-120^\\circ=20^\\circ$, so $C_1+C_2=100^\\circ$.",
         ["140°", "180°", "80°"]),
        ("SAT Stretch: An isosceles triangle has vertex angle $120^\\circ$ and equal sides of length $a$. The base equals:",
         "a√3",
         "Law of cosines: $c^2=a^2+a^2-2a^2\\cos 120^\\circ=2a^2-2a^2(-1/2)=3a^2$, so $c=a\\sqrt{3}$.",
         ["a", "2a", "a√2"]),
        ("SAT Stretch: SSA with $A=45^\\circ$, $a=\\sqrt{2}$, $b=2$ has height $h=2\\sin 45^\\circ=\\sqrt{2}$, so $a=h$ and the triangle is right at $B$. Its area is:",
         "1",
         "Then $C=45^\\circ$ as well, hypotenuse $b=2$, legs $\\sqrt{2}$ and $\\sqrt{2}$. Area $(1/2)\\cdot\\sqrt{2}\\cdot\\sqrt{2}=1$.",
         ["√2", "2", "1/2"]),
    ])


def build_unit8():
    title = "Trigonometry Unit 8: Laws of Sines & Cosines"
    description = (
        "AAS/ASA, the ambiguous SSA case, SAS/SSS, area, bearings, and Heron's formula."
    )
    concepts = [
        "Law of sines AAS/ASA",
        "Ambiguous SSA",
        "Law of cosines SAS/SSS",
        "Area of a triangle",
        "Navigation and bearings",
        "Heron's formula",
    ]

    c1 = concept_block(
        "1. Law of sines AAS/ASA",
        [
            "The law of sines says $\\dfrac{a}{\\sin A}=\\dfrac{b}{\\sin B}=\\dfrac{c}{\\sin C}=2R$, where $R$ is the circumradius. "
            "In this unit we mostly equate two of the fractions to find a missing side or angle.",
            "AAS and ASA both provide two angles, so the third is $180^\\circ$ minus their sum. That is uniquely determined — no ambiguity. "
            "Then each unknown side is paired with its opposite angle in a sine proportion.",
            "ASA gives you the included side, which sits opposite the third angle you just computed. Start the proportion with that pair; it uses the side you actually know.",
            "AAS gives you a side opposite one of the known angles, so the first proportion can start immediately, even before finding the third angle — though finding the third angle first is still tidy.",
            "Work in degrees or radians consistently with your calculator's mode. Exact answers stay in terms of $\\sin 40^\\circ$ unless a decimal is requested.",
            "Check that the largest side sits opposite the largest angle after you finish. That one comparison catches a swapped pair in the proportion.",
        ],
        "AAS/ASA is the unique, well-behaved law-of-sines case. SSA, next, is the same formula with a trap door. Master the unique case first so the trap is visible by contrast.",
        "Find the third angle. Write $\\frac{a}{\\sin A}=\\frac{b}{\\sin B}$ using a known pair. Cross-multiply. Label the answer with the correct side letter.",
        lesson_figure(
            _aas_pair(),
            "AAS/ASA: two angles known, one unique triangle (two copies shown with different included sides)",
            "Once two angles are known, the shape is fixed. Scaling the known side scales the other two sides by the law of sines.",
        )
        + solved(1, "In $\\triangle ABC$, $A=40^\\circ$, $B=60^\\circ$, $a=10$. Find $C$.",
                 ["$C=180^\\circ-40^\\circ-60^\\circ=80^\\circ$."],
                 "$80^\\circ$", "", "Easy")
        + solved(2, "Same triangle, find $b$.",
                 ["$\\dfrac{b}{\\sin 60^\\circ}=\\dfrac{10}{\\sin 40^\\circ}$.",
                  "$b=10\\sin 60^\\circ/\\sin 40^\\circ=5\\sqrt{3}/\\sin 40^\\circ$."],
                 "$10\\sin 60^\\circ/\\sin 40^\\circ$", "", "Medium")
        + solved(3, "ASA: $A=50^\\circ$, $C=70^\\circ$, included side $b=12$. Find $a$.",
                 ["$B=60^\\circ$. Side $b$ is opposite $B$.",
                  "$\\dfrac{a}{\\sin 50^\\circ}=\\dfrac{12}{\\sin 60^\\circ}$.",
                  "$a=12\\sin 50^\\circ/\\sin 60^\\circ=12\\sin 50^\\circ/(\\sqrt{3}/2)=8\\sqrt{3}\\sin 50^\\circ$."],
                 "$12\\sin 50^\\circ/\\sin 60^\\circ$", "Start with the known side opposite the now-known angle $B$.", "Hard"),
        ("Pairing a side with a non-opposite angle in the proportion",
         "The letters must match: $a$ with $A$, $b$ with $B$. Mixing $a$ with $B$ is how an AAS problem quietly becomes nonsense."),
        ("Compute the third angle before the first sine proportion in ASA",
         "The known side is opposite that third angle. Without it you do not have a complete pair."),
        ["I can find the third angle in AAS/ASA.",
         "I can write a correct sine proportion.",
         "I can check largest-side-opposite-largest-angle at the end."],
        1,
    )

    c2 = concept_block(
        "2. Ambiguous SSA",
        [
            "SSA gives one angle, the side opposite it, and another side. The third vertex can swing on a circle of radius $a$ centered at the known vertex $A$, and that circle may miss the line through $B$, just graze it, or cut it twice.",
            "Let $h=b\\sin A$ be the height from $C$'s line to side $b$'s opposite picture — standard: given $A$, $a$, $b$. Height to side $b$ is $h=b\\sin A$. "
            "If $A$ is acute: $a<h$ yields no triangle; $a=h$ yields one right triangle; $h<a<b$ yields two triangles; $a\\ge b$ yields one triangle.",
            "If $A$ is obtuse, you need $a>b$ for a single triangle; otherwise none. An obtuse angle must opposite the longest side.",
            "Computationally: $\\sin B=b\\sin A/a$. If that exceeds $1$, no triangle. If it equals $1$, a right triangle. If it is in $(0,1)$, there are two candidate angles $B$ and $180^\\circ-B$. Keep a candidate only when $A+B<180^\\circ$.",
            "The two-triangle picture is the SAT Stretch classic: one acute $B$ and one obtuse $B'$, two different sides $c$, two different areas.",
            "Always sketch. A formula that produces $\\sin B=0.8$ is not finished until you have accepted or rejected the supplement.",
        ],
        "SSA is the one congruence condition that is not a congruence condition. Every contest writer knows that. You need the height test or the supplementary-angle test on command.",
        "Compute $h=b\\sin A$ and compare with $a$ and $b$. Then, if you solve for $B$, test both $B$ and $180^\\circ-B$ against the angle sum.",
        lesson_figure(
            _ssa_two(),
            "SSA ambiguous case: two possible positions $C$ and $C'$ for the third vertex",
            "Side $a$ (from $A$ to the opposite side's line) cuts twice. The solid triangle is acute at $B$; the dashed triangle is obtuse at $B$.",
        )
        + solved(4, "Given $A=30^\\circ$, $a=8$, $b=10$, how many triangles?",
                 ["$h=b\\sin A=10\\cdot(1/2)=5$.",
                  "$5<8<10$, so two triangles."],
                 "2", "", "Easy")
        + solved(5, "Given $A=30^\\circ$, $a=4$, $b=10$, how many triangles?",
                 ["$h=5$.",
                  "$a=4<5=h$, so zero triangles."],
                 "0", "", "Medium")
        + solved(6, "Given $A=20^\\circ$, $a=8$, $b=10$, $\\sin B=10\\sin 20^\\circ/8$. Suppose that equals $0.428$ so $B\\approx 25.4^\\circ$ or $154.6^\\circ$. Which survive?",
                 ["$20^\\circ+25.4^\\circ<180^\\circ$: keep.",
                  "$20^\\circ+154.6^\\circ=174.6^\\circ<180^\\circ$: also keep.",
                  "Both survive, two triangles. (The obtuse candidate would have died if $A$ were $30^\\circ$ and the supplement were $154^\\circ$, because $30+154=184>180$.)"],
                 "both candidates, two triangles", "The angle-sum filter is the last gate, not optional.", "Hard"),
        ("Accepting $\\sin B=1.1$ as an obtuse triangle",
         "Sine never exceeds $1$. That computation means no triangle, not an obtuse one."),
        ("Always test $180^\\circ-B$",
         "If you only keep the calculator's acute $\\arcsin$, you silently drop the second triangle in the ambiguous case."),
        ["I can compute $h=b\\sin A$ and classify 0/1/2 triangles.",
         "I can reject $\\sin B>1$.",
         "I can keep or drop $180^\\circ-B$ using the angle sum."],
        6,
    )

    c3 = concept_block(
        "3. Law of cosines SAS/SSS",
        [
            "The law of cosines is $c^2=a^2+b^2-2ab\\cos C$, and the two cyclic versions for $a^2$ and $b^2$. "
            "When $C=90^\\circ$, $\\cos C=0$ and you recover Pythagoras. When $C$ is obtuse, $\\cos C$ is negative, so $c^2$ is larger than $a^2+b^2$ — the long side opposite the obtuse angle.",
            "SAS: two sides and the included angle. Plug into the law of cosines to get the third side. Then either the law of sines or another cosine evaluation finds an angle. Prefer cosine for the largest unknown angle, to avoid SSA ambiguity on the follow-up.",
            "SSS: all three sides. Solve for an angle by $\\cos C=(a^2+b^2-c^2)/(2ab)$. The largest side's opposite angle is the one to compute first; its cosine's sign tells you acute, right, or obtuse immediately.",
            "A cosine that comes out as $0.2$ is acute; $-0.2$ is obtuse; $0$ is right. Do not dump the value into $\\arccos$ on a calculator in the wrong mode.",
            "Numerical stability: if you must find a small angle from SSS, the law of cosines is still correct, but a tiny $1-\\cos$ can be sensitive. In this course the sides are nice enough that this is not an issue.",
            "After SAS produces the third side, you have SSS, and Heron could also find the area — but the SAS area formula in the next lesson is faster.",
        ],
        "SAS and SSS are exactly the cases the law of sines cannot start. This formula is the rest of non-right trigonometry.",
        "Identify SAS vs SSS. Write the version of $c^2=a^2+b^2-2ab\\cos C$ that matches the included angle or the opposite side you want. Then take a square root or an arccos.",
        lesson_figure(
            svg_triangle(a=7, b=8, c=9, right=False),
            "An SAS/SSS triangle is not required to be right",
            "The law of cosines does not need a right angle. The right-angle case is included automatically when cosine is zero.",
        )
        + solved(7, "SAS: $a=7$, $b=8$, $C=60^\\circ$. Find $c^2$.",
                 ["$c^2=49+64-2\\cdot 7\\cdot 8\\cdot\\cos 60^\\circ=113-112\\cdot(1/2)=113-56=57$."],
                 "$57$", "", "Easy")
        + solved(8, "SSS: $a=5$, $b=6$, $c=7$. Find $\\cos C$.",
                 ["$\\cos C=(a^2+b^2-c^2)/(2ab)=(25+36-49)/60=12/60=1/5$."],
                 "$1/5$", "Positive, so $C$ is acute.", "Medium")
        + solved(9, "SSS: $a=4$, $b=5$, $c=8$. Is $C$ (opposite $8$) acute or obtuse?",
                 ["$\\cos C=(16+25-64)/40=(-23)/40<0$.",
                  "Obtuse. Also $4+5=9>8$, so it is still a triangle, just obtuse."],
                 "obtuse", "The triangle inequality can hold while cosine is negative.", "Hard"),
        ("Using $c^2=a^2+b^2+2ab\\cos C$",
         "The formula has a minus. An obtuse $C$ already inserts a negative cosine, which turns the minus into a plus in effect. Do not add a second plus by hand."),
        ("After SAS, find the largest remaining angle with the law of cosines, not sines",
         "Sines cannot see obtuse vs acute ($\\sin$ of both is positive). Cosine's sign tells the truth."),
        ["I can compute the third side from SAS.",
         "I can compute a cosine from SSS.",
         "I can classify an angle as obtuse from a negative cosine."],
        11,
    )

    c4 = concept_block(
        "4. Area of a triangle",
        [
            "The SAS area formula is $\\mathrm{Area}=\\frac12 ab\\sin C$, where $C$ is the included angle. "
            "It is the old $\\frac12\\times\\mathrm{base}\\times\\mathrm{height}$ with height $=a\\sin C$ (or $b\\sin C$).",
            "If the included angle is $30^\\circ$, sine is $1/2$ and the area is a quarter of the product of the sides. If it is $90^\\circ$, sine is $1$ and you get the right-triangle formula $\\frac12 ab$.",
            "After AAS or SSA produces enough parts, you can still use $\\frac12 bc\\sin A$ once those letters are known. For two SSA triangles, the two areas are generally different because the third sides differ.",
            "You can also use $\\mathrm{Area}=\\frac12 ab\\sin C=abc/(4R)$ in concert with the law of sines, but that is optional enrichment.",
            "If you know all three sides, Heron (next lesson but one) is the path that avoids finding an angle first. If you already have an angle, $\\frac12 ab\\sin C$ is faster than Heron.",
            "Units: sides in meters give area in square meters. Do not leave a leftover degree symbol in the area.",
        ],
        "Area is the most common 'now use trig' request after a side is found. SAS area in particular is a one-liner once the included angle is known.",
        "Identify two sides and the included angle. Write $\\frac12 ab\\sin C$. Use an exact sine if the angle is special.",
        lesson_figure(
            _acute_rt(opp=6, adj=8, hyp=10, opp_l="6", adj_l="8", hyp_l="10", theta="C"),
            "Area $\\frac12\\cdot 8\\cdot 6$ for a right angle, which is $\\frac12 ab\\sin 90^\\circ$",
            "The general SAS formula specializes to the familiar right-triangle area when $\\sin C=1$.",
        )
        + solved(10, "Find the area if $a=5$, $b=8$, $C=30^\\circ$.",
                 ["$\\frac12\\cdot 5\\cdot 8\\cdot\\sin 30^\\circ=20\\cdot(1/2)=10$."],
                 "$10$", "", "Easy")
        + solved(11, "Find the area if $a=7$, $b=8$, $C=60^\\circ$.",
                 ["$\\frac12\\cdot 7\\cdot 8\\cdot\\sqrt{3}/2=14\\sqrt{3}$."],
                 "$14\\sqrt{3}$", "", "Medium")
        + solved(12, "Area is $12$, sides $a=6$ and $b=8$. Find $\\sin C$ if $C$ is the included angle.",
                 ["$12=\\frac12\\cdot 6\\cdot 8\\cdot\\sin C=24\\sin C$.",
                  "$\\sin C=1/2$.",
                  "Then $C=30^\\circ$ or $150^\\circ$ unless extra information chooses one."],
                 "$\\sin C=1/2$", "Sine does not pick acute vs obtuse by itself — same issue as SSA.", "Hard"),
        ("Using a non-included angle in $\\frac12 ab\\sin C$",
         "The angle must sit between those two sides. Relabel if the problem named a different angle."),
        ("Keep exact sines for $30/45/60$",
         "An area of $14\\sqrt{3}$ is finished. A decimal approximation is a different question."),
        ["I can compute SAS area with $\\frac12 ab\\sin C$.",
         "I can recover $\\sin C$ from a given area.",
         "I know a right angle reduces the formula to $\\frac12 ab$."],
        16,
    )

    c5 = concept_block(
        "5. Navigation and bearings",
        [
            "A bearing such as N $30^\\circ$ E means start facing north and rotate $30^\\circ$ toward east. "
            "S $40^\\circ$ W means start facing south and rotate $40^\\circ$ toward west. Always sketch the compass first.",
            "The interior angle of a path triangle is rarely the bearing number itself. "
            "Two legs, one due north and the next N $60^\\circ$ E, meet at an interior angle of $180^\\circ-60^\\circ=120^\\circ$, not $60^\\circ$.",
            "Once the triangle is labeled with sides (distances) and interior angles (from bearings), the problem is ordinary SAS, ASA, or SSS. The trig does not change; only the translation does.",
            "A common two-leg journey is SAS: two distances and the turning angle. Law of cosines gives the straight-line distance home. Then law of sines or another cosine gives the homeward bearing.",
            "Watch 'due north' and 'due east' — those are $90^\\circ$ interior angles and often hide a right triangle, in which SOH-CAH-TOA is legal and faster.",
            "Write compass directions on every ray of the sketch. Students who skip the compass invent interior angles that are supplements of the truth.",
        ],
        "Bearings are how trigonometry talks to maps. The math is Unit 8's earlier lessons; the new skill is reading a compass sentence as an interior angle.",
        "Draw N-S-E-W. Draw each path ray from the bearing. Read the interior angle as the turn between two rays. Then name SAS/ASA/SSS and solve.",
        lesson_figure(
            _bearing_svg(),
            "Bearing N $30^\\circ$ E from the origin",
            "The red ray is $30^\\circ$ east of the north line. An interior angle in a path triangle that uses this ray and due east would be $60^\\circ$, not $30^\\circ$.",
        )
        + solved(13, "Interpret N $45^\\circ$ W as an angle from north.",
                 ["Face north, rotate $45^\\circ$ toward west.",
                  "The ray is in the second compass quadrant, $45^\\circ$ off north toward west."],
                 "$45^\\circ$ west of north", "", "Easy")
        + solved(14, "A ship goes $10$ km north, then $10$ km east. Distance from the start?",
                 ["Right triangle, both legs $10$.",
                  "Hypotenuse $10\\sqrt{2}$ km.",
                  "Bearing home from start is N $45^\\circ$ E."],
                 "$10\\sqrt{2}$ km", "", "Medium")
        + solved(15, "A plane flies $100$ km north, then $100$ km on bearing N $60^\\circ$ E. Find the included interior angle and $d^2$ from the start.",
                 ["The second leg is $60^\\circ$ off north, so the turning interior angle is $180^\\circ-60^\\circ=120^\\circ$.",
                  "SAS: $d^2=100^2+100^2-2\\cdot 100\\cdot 100\\cdot\\cos 120^\\circ=20000-20000(-1/2)=30000$.",
                  "$d=100\\sqrt{3}$ km."],
                 "interior $120^\\circ$, $d=100\\sqrt{3}$ km", "Using $60^\\circ$ as the included angle would produce the wrong (smaller) $d$.", "Hard"),
        ("Using the bearing number as the triangle's interior angle without a compass sketch",
         "N $60^\\circ$ E following a due-north leg is a $120^\\circ$ interior turn, not $60^\\circ$. Sketch north at the turning point every time."),
        ("Label each ray with its compass heading before computing",
         "Then the interior angle is the difference (or $180^\\circ$ minus a sum) of those headings. The algebra is ordinary law of cosines after that."),
        ["I can interpret N/S $x^\\circ$ E/W.",
         "I can find the interior turning angle between two legs.",
         "I can finish with SAS law of cosines for the resultant distance."],
        21,
    )

    c6 = concept_block(
        "6. Heron's formula",
        [
            "Heron's formula computes area from SSS: if $s=(a+b+c)/2$ is the semi-perimeter, then $\\mathrm{Area}=\\sqrt{s(s-a)(s-b)(s-c)}$. "
            "No angle is required. That is the point.",
            "For $13,14,15$, $s=21$, and $s-a,s-b,s-c=8,7,6$ (in some order), product $21\\cdot 8\\cdot 7\\cdot 6=7056$, square root $84$.",
            "If the quantity under the radical is negative, the three lengths fail the triangle inequality. If it is zero, the 'triangle' is degenerate (flat, area $0$).",
            "An equilateral triangle of side $a$ gives $s=3a/2$ and area $\\sqrt{3}a^2/4$, matching the usual formula — a good check.",
            "Numerically, Heron can be sensitive for very skinny triangles (subtracting nearly equal numbers). Contest sides are chosen to be friendly, as in $13$-$14$-$15$ or $25$-$25$-$14$.",
            "You may still use $\\frac12 ab\\sin C$ after finding $C$ from the law of cosines. Heron and that route must agree; disagreement means an arithmetic slip in one of them.",
        ],
        "SSS area without a detour through an angle is a standard finish. Combined with the law of cosines, SSS is a complete solving kit: angles and area from three sides.",
        "Add the sides, halve to get $s$, subtract each side from $s$, multiply the four numbers, take the square root. Check the triangle inequality first if the product looks negative.",
        lesson_figure(
            _heron_tri(),
            "A $13$-$14$-$15$ triangle with semi-perimeter $s=21$",
            "Heron: $\\sqrt{21(21-15)(21-14)(21-13)}=\\sqrt{21\\cdot 6\\cdot 7\\cdot 8}=84$.",
        )
        + solved(16, "Find $s$ for sides $13,14,15$.",
                 ["$s=(13+14+15)/2=21$."],
                 "$21$", "", "Easy")
        + solved(17, "Find the area of a $13$-$14$-$15$ triangle.",
                 ["$\\sqrt{21\\cdot(21-15)\\cdot(21-14)\\cdot(21-13)}=\\sqrt{21\\cdot 6\\cdot 7\\cdot 8}=\\sqrt{7056}=84$."],
                 "$84$", "", "Medium")
        + solved(18, "Find the area of an equilateral triangle of side $6$ using Heron, and match $\\frac{\\sqrt{3}}{4}a^2$.",
                 ["$s=9$.",
                  "$\\sqrt{9\\cdot 3\\cdot 3\\cdot 3}=\\sqrt{243}=9\\sqrt{3}$.",
                  "$\\frac{\\sqrt{3}}{4}\\cdot 36=9\\sqrt{3}$. Match."],
                 "$9\\sqrt{3}$", "", "Hard"),
        ("Forgetting to halve the perimeter",
         "Using $a+b+c$ in place of $s$ inflates the product by $16$ and the area by $4$. The $s$ is a semi-perimeter."),
        ("Check $a+b>c$ before blaming the square root",
         "A negative radicand is usually a non-triangle, not a broken formula."),
        ["I can compute $s$ and the four Heron factors.",
         "I can evaluate a friendly SSS area such as $13$-$14$-$15$.",
         "I can detect a failed triangle inequality from a negative radicand."],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
        stretch_note=STRETCH_LABEL,
    )
    return title, description, content, _u8_questions()


def build_master():
    units = [('Right Triangle Trigonometry', ['SOH-CAH-TOA', 'Reciprocal ratios', 'Cofunctions', 'Solving right triangles', 'Applications', 'Exact values for 30/45/60']), ('Unit Circle & Radian Measure', ['Degrees vs radians', 'Arc length s=rθ', 'Unit circle coordinates', 'Reference angles', 'All six functions on the circle', 'Coterminal angles']), ('Graphing Sine and Cosine', ['Parent sine', 'Parent cosine', 'Amplitude and period', 'Phase shift', 'Vertical shift', 'Write an equation from a graph']), ('Tangent and Other Graphs', ['Tangent asymptotes', 'Cotangent', 'Secant', 'Cosecant', 'Transformations', 'Domain from graphs']), ('Identities', ['Pythagorean identities', 'Even/odd and cofunction', 'Quotient identities', 'Simplify expressions', 'Verify identities', 'Rewrite to solve']), ('Sum, Difference & Multiple Angle', ['Sine/cosine addition', 'Tangent addition', 'Double-angle', 'Half-angle', 'Product-to-sum', 'Power-reduce']), ('Inverse Trig & Equations', ['Inverse sine cosine tangent', 'Range of inverses', 'Solve on [0,2π)', 'General solution', 'Quadratic in disguise', 'Graphical solutions']), ('Laws of Sines & Cosines', ['Law of sines AAS/ASA', 'Ambiguous SSA', 'Law of cosines SAS/SSS', 'Area of a triangle', 'Navigation and bearings', "Heron's formula"])]
    items = "".join(f"<li>Unit {i} — {u[0]}</li>" for i, u in enumerate(units, 1))
    return (
        f"<h1>Trigonometry Complete</h1>"
        f"<p><strong>For:</strong> <strong>High school Trigonometry</strong>. Eight deep units, each with six concepts, "
        "worked examples with matching diagrams, 5 quizzes per concept, and a 25-problem stretch finale.</p>"
        f"{page_break()}"
        "<h2>The eight units</h2>"
        f"<ol>{items}</ol>"
    )
