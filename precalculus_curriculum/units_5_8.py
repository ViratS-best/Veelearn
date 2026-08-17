#!/usr/bin/env python3
"""Deep Precalculus units 5–8: polar, conics, sequences/limits, vectors/matrices."""

from __future__ import annotations

import math

from curriculum_kit import lesson_figure, svg_parabola, svg_circle, svg_plane

from hs_curriculum import (
    concept_block,
    solved,
    practice_slots,
    unit_shell,
    page_break,
    mq,
    xy_graph,
    sample_curve,
    number_line,
    argand,
    unit_circle_svg,
    labeled_right_triangle,
)

from .common import AUDIENCE, STRETCH_LABEL


def _polar(r_fn, t0=0.0, t1=2 * math.pi, n=180):
    pts = []
    for i in range(n + 1):
        th = t0 + (t1 - t0) * i / n
        r = r_fn(th)
        pts.append((r * math.cos(th), r * math.sin(th)))
    return pts


def _ellipse(a, b, n=80):
    return [(a * math.cos(2 * math.pi * i / n), b * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]


def _hyp_branches(a, b, xmax=6, n=28):
    right_up, right_dn, left_up, left_dn = [], [], [], []
    for i in range(n + 1):
        x = a + (xmax - a) * i / n
        y = b * math.sqrt(max(x * x / (a * a) - 1.0, 0.0))
        right_up.append((x, y))
        right_dn.append((x, -y))
        left_up.append((-x, y))
        left_dn.append((-x, -y))
    return right_up, right_dn, left_up, left_dn


def _add(qs, rows):
    for row in rows:
        text, ans, expl = row[0], row[1], row[2]
        dist = row[3] if len(row) > 3 else None
        qs.append(mq(text, ans, expl, len(qs) + 1, distractors=dist))
    return qs


# ===========================================================================
# UNIT 5: Analytic Trigonometry & Polar
# ===========================================================================

def _u5_questions():
    qs = []
    _add(qs, [
        ("$\\sin A+\\sin B$ equals:",
         "2 sin((A+B)/2) cos((A-B)/2)",
         "The sum-to-product formula for sine.",
         ["2 cos((A+B)/2) sin((A-B)/2)", "sin(A+B)", "sin A cos B"]),
        ("$\\cos A+\\cos B$ equals:",
         "2 cos((A+B)/2) cos((A-B)/2)",
         "Sum-to-product for cosine of a sum.",
         ["-2 sin((A+B)/2) sin((A-B)/2)", "cos(A+B)", "2 sin A cos B"]),
        ("Product-to-sum: $2\\sin A\\cos B$ equals:",
         "sin(A+B)+sin(A-B)",
         "The inverse of the sum-to-product pair.",
         ["cos(A+B)", "2 sin(A+B)", "sin A + cos B"]),
        ("Sum-to-product is most useful when you want to:",
         "turn a sum of sines into a product you can solve",
         "Products set equal to zero factor; sums of sines do not.",
         ["replace polar with rectangular only", "find a derivative", "graph a line"]),
        ("$\\sin 75^\\circ+\\sin 15^\\circ$ simplifies using sum-to-product to:",
         "\\sqrt{6}/2",
         "$(A+B)/2=45^\\circ$ and $(A-B)/2=30^\\circ$, so $2\\sin 45^\\circ\\cos 30^\\circ=2\\cdot\\frac{\\sqrt{2}}{2}\\cdot\\frac{\\sqrt{3}}{2}=\\frac{\\sqrt{6}}{2}$.",
         ["\\sqrt{2}", "1", "0"]),
        ("The polar point $(r,\\theta)=(2,\\pi/3)$ has rectangular coordinates:",
         "(1, \\sqrt{3})",
         "$x=r\\cos\\theta=2\\cdot1/2=1$, $y=r\\sin\\theta=2\\cdot\\sqrt{3}/2=\\sqrt{3}$.",
         ["(2, \u03c0/3)", "(\\sqrt{3}, 1)", "(1, 1)"]),
        ("A point with $x=-1$, $y=0$ can be written in polar as:",
         "(1, \u03c0)",
         "$r=1$ and $\\theta=\\pi$ (negative x-axis).",
         ["(1, 0)", "(-1, 0) as polar r=-1 \u03b8=0 is also possible", "(0, \u03c0)"]),
        ("$r=0$ in polar represents:",
         "the origin (any \u03b8)",
         "Radius zero is the pole, independent of the angle.",
         ["the unit circle", "a line", "undefined"]),
        ("Negative $r$ in $(r,\\theta)$ means:",
         "the opposite ray: ( |r|, \u03b8+\u03c0 )",
         "Go $|r|$ in the direction $\\theta+\\pi$.",
         ["an imaginary point", "below the x-axis always", "r must stay positive"]),
        ("$\\theta=\\pi/4$ as a polar graph is:",
         "the ray at 45°",
         "Fixed angle, any $r$ (including negative $r$ extending the line).",
         ["a circle", "a cardioid", "a rose"]),
        ("$r=2$ as a polar graph is:",
         "a circle of radius 2 about the origin",
         "Constant radius is a circle centered at the pole.",
         ["a line", "a four-petal rose", "a spiral"]),
        ("$r=2\\cos\\theta$ is a circle through the origin with diameter:",
         "2 along the x-axis",
         "Convert: $r=2x/r$ so $x^2+y^2=2x$, $(x-1)^2+y^2=1$.",
         ["2 along the y-axis", "4", "1 vertical"]),
        ("$r=2a\\sin\\theta$ is a circle along the:",
         "y-axis",
         "Analogous conversion produces a circle of diameter $2a$ on the y-axis.",
         ["x-axis only", "line y=x", "origin-free horizontal line"]),
        ("The four-petal rose $r=2\\cos(2\\theta)$ has petals along:",
         "the axes of \u03b8=0, \u03c0/2, ... of the 2\u03b8 maxima",
         "Max $|r|$ when $|\\cos 2\\theta|=1$, i.e. $2\\theta=n\\pi$, $\\theta=n\\pi/2$.",
         ["only the origin", "a single circle", "a cardioid"]),
        ("$r=1+\\cos\\theta$ is a:",
         "cardioid",
         "The limaçon with $a=b$ is a cardioid dimpled at the origin.",
         ["four-petal rose", "line", "hyperbola"]),
        ("Convert $(x,y)=(0,2)$ to polar with $r>0$ and $\\theta\\in[0,2\\pi)$.",
         "(2, \u03c0/2)",
         "$r=2$, $\\theta=\\pi/2$ (positive y-axis).",
         ["(2, 0)", "(2, \u03c0)", "(0, 2)"]),
        ("Convert $(r,\\theta)=(4,5\\pi/6)$ to $x$.",
         "-2\\sqrt{3}",
         "$x=4\\cos(5\\pi/6)=4(-\\sqrt{3}/2)=-2\\sqrt{3}$.",
         ["2\\sqrt{3}", "4", "-4"]),
        ("$x=r\\cos\\theta$ and $y=r\\sin\\theta$ imply $x^2+y^2=$:",
         "r^2",
         "The polar-to-rectangular identity from Pythagoras.",
         ["r", "\u03b8", "1"]),
        ("$\\theta=\\arctan(y/x)$ is incomplete because:",
         "you must adjust the quadrant using the signs of x and y",
         "Arctan only returns $(-\\pi/2,\\pi/2)$; left-half-plane points need $\\pm\\pi$.",
         ["r is always negative", "\u03b8 cannot be \u03c0", "x must be 0"]),
        ("The rectangular equation $x=2$ in polar form is:",
         "r cos \u03b8 = 2",
         "Substitute $x=r\\cos\\theta$.",
         ["r=2", "\u03b8=2", "r sin \u03b8=2"]),
        ("De Moivre: $[\\cos\\theta+i\\sin\\theta]^n$ equals:",
         "cos(n\u03b8)+i sin(n\u03b8)",
         "Raise modulus $1$ to $n$ and multiply the angle by $n$.",
         ["n cos \u03b8 + i n sin \u03b8", "cos(\u03b8^n)+i sin(\u03b8^n)", "1"]),
        ("$(1+i)^2$ in polar starts from $1+i=\\sqrt{2}\\mathrm{cis}(\\pi/4)$, so the square is:",
         "2 cis(\u03c0/2) = 2i",
         "$r^2=2$, angle $\\pi/2$: $2(\\cos\\pi/2+i\\sin\\pi/2)=2i$.",
         ["2", "1+i", "0"]),
        ("The $n$-th roots of a complex number lie on:",
         "a circle, equally spaced by 2\u03c0/n",
         "De Moivre’s root formula: same modulus $r^{1/n}$, angles $(\\theta+2\\pi k)/n$.",
         ["a line", "a rose", "the real axis only"]),
        ("$\\mathrm{cis}\\,\\theta$ is shorthand for:",
         "cos \u03b8 + i sin \u03b8",
         "Standard polar abbreviation.",
         ["cosh \u03b8", "csc \u03b8", "i^\u03b8"]),
        ("$[2\\,\\mathrm{cis}\\,(\\pi/6)]^3$ equals:",
         "8 cis(\u03c0/2)",
         "$r^n=8$, $n\\theta=\\pi/2$.",
         ["6 cis(\u03c0/2)", "8 cis(\u03c0/6)", "2 cis(\u03c0/2)"]),
        ("The polar form of $i$ is:",
         "1 cis(\u03c0/2)",
         "Modulus $1$, argument $\\pi/2$.",
         ["1 cis(0)", "i cis(0)", "1 cis(\u03c0)"]),
        ("The polar form of $-4$ is:",
         "4 cis(\u03c0)",
         "Negative real axis, modulus $4$.",
         ["4 cis(0)", "-4 cis(0)", "4 cis(\u03c0/2)"]),
        ("$3-3i$ has argument:",
         "-\u03c0/4",
         "Quadrant IV, reference $\\pi/4$.",
         ["\u03c0/4", "3\u03c0/4", "-\u03c0/2"]),
        ("Modulus of $3-4i$ is:",
         5,
         "$\\sqrt{9+16}=5$.",
         ["7", "12", "1"]),
        ("Multiplying two polar complex numbers multiplies moduli and:",
         "adds arguments",
         "$(r_1\\mathrm{cis}\\theta_1)(r_2\\mathrm{cis}\\theta_2)=r_1 r_2\\,\\mathrm{cis}(\\theta_1+\\theta_2)$.",
         ["adds moduli", "multiplies arguments", "subtracts moduli"]),
        ("$\\sin 3x+\\sin x=0$ can be solved by first writing:",
         "2 sin(2x) cos x = 0",
         "Sum-to-product: $2\\sin(2x)\\cos x=0$.",
         ["sin(4x)=0", "2 cos(2x) sin x=0", "3 sin x"]),
        ("A polar point $(3,4\\pi/3)$ is in which rectangular quadrant?",
         "III",
         "Angle $4\\pi/3$ is quadrant III; $r>0$ stays there.",
         ["I", "II", "IV"]),
        ("$r=2\\sin(3\\theta)$ is a rose with how many petals?",
         3,
         "For $r=a\\sin(n\\theta)$ with $n$ odd, there are $n$ petals.",
         ["6", "2", "1"]),
        ("$r=2\\cos(2\\theta)$ has how many petals?",
         4,
         "Even $n$ in $\\cos(n\\theta)$ gives $2n$ petals.",
         ["2", "8", "1"]),
        ("Rectangular $(1,-\\sqrt{3})$ has polar $\\theta=$ (principal, $r>0$):",
         "-\u03c0/3",
         "Quadrant IV, $r=2$, argument $-\\pi/3$.",
         ["\u03c0/3", "2\u03c0/3", "\u03c0"]),
        ("$z\\bar z$ equals:",
         "|z|^2",
         "A complex number times its conjugate is the square of the modulus.",
         ["0", "2 Re z", "arg z"]),
        ("The argument of a product $zw$ is:",
         "arg z + arg w",
         "Polar multiplication adds angles (mod $2\\pi$).",
         ["arg z · arg w", "arg z - arg w", "0"]),
        ("Convert $r\\sin\\theta=4$ to rectangular.",
         "y=4",
         "$y=r\\sin\\theta$.",
         ["x=4", "x^2+y^2=16", "a circle r=4"]),
        ("$1+i\\sqrt{3}$ has modulus:",
         2,
         "$\\sqrt{1+3}=2$.",
         ["\\sqrt{3}", "4", "1"]),
        ("De Moivre with $n=0$ recovers:",
         "1 (cis 0)",
         "Any nonzero complex to the $0$ power is $1$.",
         ["0", "i", "the original z"]),
        ("A limaçon $r=a+b\\cos\\theta$ has an inner loop when:",
         "|a|<|b|",
         "The ratio $|a|/|b|<1$ produces a loop through the pole.",
         ["|a|=|b|", "|a|>|b|", "b=0"]),
        ("The principal argument of a positive real number is:",
         0,
         "Positive real axis.",
         ["\u03c0", "\u03c0/2", "1"]),
        ("$\\cos A-\\cos B$ equals:",
         "-2 sin((A+B)/2) sin((A-B)/2)",
         "The cosine difference sum-to-product formula.",
         ["2 cos((A+B)/2) cos((A-B)/2)", "cos(A-B)", "sin A - sin B"]),
        ("To convert $x^2+y^2=2x$ into polar, first replace $x^2+y^2$ by:",
         "r^2",
         "Then $r^2=2r\\cos\\theta$, so $r=2\\cos\\theta$ (or $r=0$).",
         ["\u03b8", "2r", "x"]),
        ("The imaginary part of $2\\,\\mathrm{cis}(\\pi/6)$ is:",
         1,
         "$2\\sin(\\pi/6)=2\\cdot1/2=1$.",
         ["\\sqrt{3}", "2", "0"]),
        ("SAT Stretch: Identify $r=4\\cos(2\\theta)$.",
         "4-petal rose, max |r|=4",
         "Even $n=2$ in $\\cos(n\\theta)$ gives $2n=4$ petals; amplitude $|a|=4$.",
         ["3-petal rose", "circle radius 4", "cardioid"]),
        ("SAT Stretch: Solve $\\sin 3x+\\sin x=0$ on $[0,\\pi]$.",
         "0, \u03c0/2, \u03c0",
         "$2\\sin(2x)\\cos x=0$. Then $\\sin(2x)=0$ gives $x=k\\pi/2$, so $x=0,\\pi/2,\\pi$ on $[0,\\pi]$. "
         "$\\cos x=0$ gives $x=\\pi/2$, already listed.",
         ["0, \u03c0/4, 3\u03c0/4, \u03c0", "\u03c0/2 only", "no solution"]),
        ("SAT Stretch: Convert $z=-2\\sqrt{3}+2i$ to polar $r\\,\\mathrm{cis}\\,\\theta$ with $\\theta\\in(-\\pi,\\pi]$.",
         "4 cis(5\u03c0/6)",
         "$r=\\sqrt{12+4}=4$. Quadrant II: $\\theta=\\pi-\\pi/6=5\\pi/6$.",
         ["4 cis(\u03c0/6)", "4 cis(-5\u03c0/6)", "2 cis(5\u03c0/6)"]),
        ("SAT Stretch: The square roots of $16\\,\\mathrm{cis}\\,(\\pi/3)$ are:",
         "4 cis(\u03c0/6) and 4 cis(7\u03c0/6)",
         "$r^{1/2}=4$, angles $(\\pi/3+2\\pi k)/2$ for $k=0,1$: $\\pi/6$ and $7\\pi/6$.",
         ["4 cis(\u03c0/3) only", "16 cis(\u03c0/6)", "2 cis(\u03c0/6)"]),
        ("SAT Stretch: $r=2/(1-\\cos\\theta)$ is which conic in polar form?",
         "parabola (e=1)",
         "Standard $r=\\dfrac{ed}{1-e\\cos\\theta}$ with $e=1$ is a parabola.",
         ["ellipse e<1", "hyperbola e>1", "circle e=0"]),
        ("SAT Stretch: Product $(1+i)(1-i)$ via polar is $r=$:",
         2,
         "Each has modulus $\\sqrt{2}$; product modulus $2$. Arguments $\\pi/4+( -\\pi/4)=0$, so the product is $2$.",
         ["0", "1", "\\sqrt{2}"]),
        ("SAT Stretch: A rose $r=a\\sin(n\\theta)$ with $n=4$ has how many petals?",
         8,
         "Even $n$ produces $2n$ petals.",
         ["4", "2", "n"]),
        ("SAT Stretch: $\\mathrm{Arg}((1+i)^8)$ in $(-\\pi,\\pi]$ equals:",
         0,
         "$(1+i)=\\sqrt{2}\\,\\mathrm{cis}(\\pi/4)$, so eighth power has argument $2\\pi\\equiv0$.",
         ["\u03c0", "2\u03c0", "\u03c0/4"]),
        ("SAT Stretch: Rectangular form of $6\\,\\mathrm{cis}(-2\\pi/3)$ is:",
         "-3 - 3\\sqrt{3} i",
         "$6(-1/2 + i(-\\sqrt{3}/2))=-3-3\\sqrt{3}\\,i$.",
         ["-3 + 3\\sqrt{3} i", "3 - 3\\sqrt{3} i", "6i"]),
        ("SAT Stretch: Solve $r=2\\cos\\theta$ and $r=1$ simultaneously (intersection in polar).",
         "\u03b8=\u00b1\u03c0/3",
         "$1=2\\cos\\theta$, $\\cos\\theta=1/2$, $\\theta=\\pm\\pi/3$ (plus the pole if it satisfies both).",
         ["\u03b8=0 only", "\u03b8=\u03c0/2", "no intersection"]),
    ])
    return qs[:55]


def build_unit5():
    title = "Precalculus Unit 5: Analytic Trigonometry & Polar"
    description = (
        "Sum-to-product identities, polar coordinates and graphs, polar/rectangular conversion, "
        "De Moivre, and complex numbers in polar form — with rose plots and Argand diagrams."
    )
    concepts = [
        "Sum-to-product",
        "Polar coordinates",
        "Polar graphs",
        "Convert polar/rectangular",
        "De Moivre intro",
        "Complex in polar form",
    ]

    rose = _polar(lambda th: 2 * math.cos(2 * th), 0, 2 * math.pi, 240)

    c1 = concept_block(
        "1. Sum-to-product",
        [
            "Angle-addition formulas from a trigonometry course can be rearranged into sum-to-product identities. "
            "The four you need are $\\sin A+\\sin B=2\\sin\\dfrac{A+B}{2}\\cos\\dfrac{A-B}{2}$, "
            "$\\sin A-\\sin B=2\\cos\\dfrac{A+B}{2}\\sin\\dfrac{A-B}{2}$, "
            "$\\cos A+\\cos B=2\\cos\\dfrac{A+B}{2}\\cos\\dfrac{A-B}{2}$, and "
            "$\\cos A-\\cos B=-2\\sin\\dfrac{A+B}{2}\\sin\\dfrac{A-B}{2}$.",
            "The point of the rewrite is algebraic: a product can be zero if a factor is zero, while a sum of "
            "two sines is awkward to solve. Equations such as $\\sin 3x+\\sin x=0$ become "
            "$2\\sin(2x)\\cos x=0$ in one line, then split into two ordinary trig equations from Unit 4.",
            "Product-to-sum formulas run the other direction and are how you later integrate $\\sin mx\\cos nx$ "
            "in calculus. In Precalculus they also simplify exact values such as $\\sin 75^\\circ\\cos 15^\\circ$.",
            "You do not need to derive the identities on every test, but you should recognize which pair you "
            "need: sum of sines versus difference of cosines look similar and are easy to mix up. A quick "
            "numeric check with $A=B=\\pi/2$ catches a sign error immediately.",
            "These identities live in the same toolkit as double-angle. Double-angle is the special case "
            "$A=B$. Sum-to-product is the case of two different angles. Polar form later in the unit will "
            "multiply complex numbers by adding angles — a different addition, but the same geometric circle.",
            "When a multiple-choice question offers $2\\sin((A+B)/2)\\cos((A-B)/2)$, that is $\\sin A+\\sin B$, "
            "not $\\cos A+\\cos B$. Matching the outer function (sin versus cos of the average) is the fastest elimination.",
        ],
        "Sum-to-product turns “when is this wave plus that wave zero?” into factoring, which is the Precalculus "
        "way to solve two-frequency equations without a graphing calculator.",
        "Write the identity down before you substitute the messy angles. Then the average $(A+B)/2$ and the "
        "half-difference $(A-B)/2$ are ordinary numbers or ordinary expressions you already know how to solve.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#4f46e5", sample_curve(lambda x: math.sin(3 * x) + math.sin(x), 0, 2 * math.pi)),
                    ("#dc2626", sample_curve(lambda x: 2 * math.sin(2 * x) * math.cos(x), 0, 2 * math.pi)),
                ],
                xlim=(-0.3, 7), ylim=(-2.5, 2.5),
            ),
            "$\\sin 3x+\\sin x$ (blue) overlays $2\\sin(2x)\\cos x$ (red)",
            "The two graphs coincide: that is the sum-to-product identity in a picture.",
        )
        + solved(
            1, "Write the sum-to-product form of $\\sin A+\\sin B$.",
            ["Average the angles and take half the difference.",
             "$\\sin A+\\sin B=2\\sin\\dfrac{A+B}{2}\\cos\\dfrac{A-B}{2}$.",
             "Check $A=B$: right side $2\\sin A\\cos 0=2\\sin A$, and left side $2\\sin A$."],
            "$2\\sin\\dfrac{A+B}{2}\\cos\\dfrac{A-B}{2}$", "", "Easy",
        )
        + solved(
            2, "Rewrite $\\sin 3x+\\sin x$ as a product.",
            ["$A=3x$, $B=x$, so $(A+B)/2=2x$ and $(A-B)/2=x$.",
             "The identity gives $2\\sin(2x)\\cos x$."],
            "$2\\sin(2x)\\cos x$", "", "Medium",
        )
        + solved(
            3, "Solve $\\sin 3x+\\sin x=0$ on $[0,\\pi]$.",
            ["$2\\sin(2x)\\cos x=0$, so $\\sin(2x)=0$ or $\\cos x=0$.",
             "$\\sin(2x)=0\\Rightarrow 2x=k\\pi\\Rightarrow x=k\\pi/2$. In $[0,\\pi]$: $0,\\pi/2,\\pi$.",
             "$\\cos x=0\\Rightarrow x=\\pi/2$ (already listed).",
             "Solutions: $0,\\pi/2,\\pi$."],
            "$0,\\pi/2,\\pi$", "Factoring a product is why the identity was worth using.", "Hard",
        ),
        ("Mixing the cosine-sum identity with the sine-sum identity",
         "$\\cos A+\\cos B$ has two cosines of the half-angles, not a sine times a cosine. If your rewritten "
         "product has the wrong outer functions, a substitution $A=B=0$ will fail ($2=2\\cos0\\cos0$ works for "
         "cosine-sum; sine-sum would give $0=0$ and not catch the mix-up — use $A=B=\\pi/2$ instead)."),
        ("Average first",
         "On a fill-in, compute $(A+B)/2$ and $(A-B)/2$ as the first two lines. The rest is copying the correct template."),
        [
            "I can state the four sum-to-product formulas.",
            "I can turn $\\sin 3x+\\sin x$ into a product.",
            "I can solve the resulting factored trig equation.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Polar coordinates",
        [
            "A polar coordinate pair $(r,\\theta)$ locates a point by a directed distance $r$ from the origin "
            "(the pole) and an angle $\\theta$ from the positive x-axis (the polar axis). The same point has "
            "many names: add $2\\pi$ to $\\theta$, or replace $(r,\\theta)$ by $(-r,\\theta+\\pi)$.",
            "Conversion to rectangular is $x=r\\cos\\theta$, $y=r\\sin\\theta$. Conversion back uses "
            "$r=\\sqrt{x^2+y^2}$ (nonnegative choice) and $\\theta=\\mathrm{atan2}(y,x)$ — that is, arctan adjusted "
            "for quadrant. Plain $\\arctan(y/x)$ is a trap in quadrants II and III.",
            "The pole itself is $r=0$ with $\\theta$ arbitrary. A ray $\\theta=c$ is a half-line (and, allowing "
            "negative $r$, often the whole line through the origin at that angle). A circle $r=a$ ($a>0$) is "
            "centered at the pole with radius $a$.",
            "Negative $r$ is a Precalculus convention: plot $|r|$ in the opposite direction. It makes rose "
            "formulas and limaçons draw correctly without splitting cases. If a problem insists on $r\\geq0$, "
            "convert with the $+\\pi$ rule.",
            "Polar is the natural language of rotation and of complex multiplication (later this unit). It is "
            "also how radar, spirals, and some planetary models are written. Rectangular remains better for "
            "vertical and horizontal lines, which become $r\\cos\\theta=a$ and $r\\sin\\theta=b$.",
            "Plotting a single point is a two-step: rotate the ray, then march $r$ units (backward if $r<0$). "
            "Label both $(r,\\theta)$ and $(x,y)$ until the conversion formulas feel like Unit 1 composition.",
        ],
        "Polar coordinates are how you will graph roses, multiply complex numbers, and later set up area "
        "integrals in calculus with $dA=\\frac12 r^2\\,d\\theta$.",
        "To plot: ray first, then $r$. To convert: $x=r\\cos\\theta$, $y=r\\sin\\theta$. Coming back, protect "
        "the quadrant; do not trust $\\arctan(y/x)$ alone when $x<0$.",
        lesson_figure(
            xy_graph(
                curves=[("#94a3b8", [(0, 0), (1, math.sqrt(3))])],
                points=[(1, math.sqrt(3), "(2, \u03c0/3)")],
                xlim=(-1, 3), ylim=(-1, 3),
            ),
            "Polar point $(r,\\theta)=(2,\\pi/3)$ as the rectangular point $(1,\\sqrt{3})$",
            "The ray at $60^\\circ$ and distance $2$ land on $x=2\\cos(\\pi/3)=1$, $y=2\\sin(\\pi/3)=\\sqrt{3}$.",
        )
        + solved(
            4, "Convert $(2,\\pi/3)$ to rectangular.",
            ["$x=2\\cos(\\pi/3)=2\\cdot1/2=1$.",
             "$y=2\\sin(\\pi/3)=2\\cdot\\sqrt{3}/2=\\sqrt{3}$.",
             "The point is $(1,\\sqrt{3})$."],
            "$(1,\\sqrt{3})$", "", "Easy",
        )
        + solved(
            5, "Give a polar pair with $r>0$ for the rectangular point $(-1,0)$.",
            ["Distance from origin $r=1$.",
             "The negative x-axis is $\\theta=\\pi$.",
             "So $(1,\\pi)$. (Also $(1,\\pi+2\\pi n)$.)"],
            "$(1,\\pi)$", "", "Medium",
        )
        + solved(
            6, "Explain how $(-2,\\pi/6)$ relates to a positive-$r$ pair.",
            ["Negative $r$ means reverse the ray: add $\\pi$ to the angle.",
             "$(-2,\\pi/6)=(2,\\pi/6+\\pi)=(2,7\\pi/6)$.",
             "Both names plot the same point in quadrant III."],
            "$(2,7\\pi/6)$", "Many names, one point.", "Hard",
        ),
        ("Using $\\theta=\\arctan(y/x)$ in quadrant II",
         "For $(-1,1)$, $y/x=-1$ so $\\arctan(-1)=-\\pi/4$, which is quadrant IV. The actual angle is $3\\pi/4$. "
         "Always look at the signs of $x$ and $y$ after you compute a reference angle."),
        ("Ray, then radius",
         "Students sometimes plot $r$ along the x-axis and then rotate the point, which is a different (wrong) "
         "motion. Rotate the ray first."),
        [
            "I can convert polar points to $(x,y)$.",
            "I can find $r>0$ and a quadrant-correct $\\theta$.",
            "I can rewrite a negative $r$ as a positive $r$ with $\\theta+\\pi$.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Polar graphs",
        [
            "A polar equation $r=f(\\theta)$ is a curve. The standard catalog: $r=a$ circle about the pole; "
            "$\\theta=c$ a line through the pole; $r=2a\\cos\\theta$ a circle on the x-axis through the origin; "
            "$r=2a\\sin\\theta$ a circle on the y-axis; $r=a\\cos(n\\theta)$ or $a\\sin(n\\theta)$ a rose; "
            "$r=a\\pm b\\cos\\theta$ a limaçon (cardioid when $|a|=|b|$).",
            "Roses: if $n$ is odd, there are $n$ petals; if $n$ is even, there are $2n$ petals. The four-petal "
            "rose $r=2\\cos(2\\theta)$ has maximum $|r|=2$ when $|\\cos 2\\theta|=1$, i.e. $\\theta=n\\pi/2$. "
            "Identifying “four petals on the axes versus on the diagonals” is an SAT-style polar question.",
            "Cardioids look like apples with a dimple at the origin. Limacons with $|a|<|b|$ grow an inner loop. "
            "You can sketch them by testing $\\theta=0,\\pi/2,\\pi,3\\pi/2$ and plotting the four $r$-values, then "
            "filling the obvious symmetry.",
            "Spirals $r=a\\theta$ and lemniscates $r^2=a^2\\cos(2\\theta)$ appear in richer courses. For this "
            "unit, roses, circles, cardioids, and lines are the required pictures. Always convert to rectangular "
            "if you need to confirm a circle: $r=2\\cos\\theta$ becomes $(x-1)^2+y^2=1$.",
            "Graphing technology can hide the fact that $\\theta$ from $0$ to $2\\pi$ may trace a rose twice "
            "when $n$ is odd (the second lap retraces). That is why an odd rose still has $n$ petals, not $2n$.",
            "Matching a multiple-choice polar graph is a petal-count plus orientation problem. $\\cos$ roses "
            "are symmetric about the x-axis; $\\sin$ roses about the y-axis. Circles $r=2\\cos\\theta$ live to "
            "the right of the origin; $r=2\\sin\\theta$ live above it.",
        ],
        "Polar graphs are how Precalculus visualizes periodic direction. They are also the pictures behind "
        "De Moivre powers (rotating a point) and behind conic polar forms in Unit 6.",
        "Name the family from the formula (rose, circle, cardioid, line). For a rose, count petals from $n$ "
        "odd/even. Plot four cardinal $\\theta$ values to place the petals.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", rose)],
                xlim=(-3, 3), ylim=(-3, 3),
            ),
            "Four-petal rose $r=2\\cos(2\\theta)$",
            "Even $n=2$ produces $2n=4$ petals. Max $|r|=2$ along $\\theta=0,\\pi/2,\\pi,3\\pi/2$ as $2\\theta$ hits multiples of $\\pi$.",
        )
        + solved(
            7, "What curve is $r=2$?",
            ["Constant radius $2$.",
             "That is a circle centered at the pole.",
             "In rectangular form, $x^2+y^2=4$."],
            "circle radius $2$ about the origin", "", "Easy",
        )
        + solved(
            8, "Identify $r=2\\cos\\theta$.",
            ["Multiply by $r$: $r^2=2r\\cos\\theta$.",
             "$x^2+y^2=2x$, complete the square: $(x-1)^2+y^2=1$.",
             "Circle of radius $1$ centered at $(1,0)$, through the origin."],
            "circle diameter $2$ on the x-axis", "", "Medium",
        )
        + solved(
            9, "How many petals does $r=2\\cos(2\\theta)$ have, and what is the maximum $|r|$?",
            ["$n=2$ is even, so $2n=4$ petals.",
             "Maximum $|r|$ is $|2|=2$.",
             "It is a four-petal rose of “amplitude” $2$."],
            "4 petals, max $|r|=2$", "Odd $n$ would have given $n$ petals, not $2n$.", "Hard",
        ),
        ("Doubling the petal count for odd $n$",
         "$r=\\sin(3\\theta)$ has three petals, not six. The extra lap of $\\theta\\in[0,2\\pi]$ retraces the "
         "same three petals. Even $n$ really does double."),
        ("Convert a suspected circle",
         "If the polar formula is linear in $\\cos\\theta$ or $\\sin\\theta$ with no extra $n$, multiply by $r$ "
         "and complete the square. You should get a circle through the origin."),
        [
            "I can recognize circles, lines, roses, and cardioids in polar form.",
            "I can count rose petals from $n$.",
            "I can convert $r=2a\\cos\\theta$ to a rectangular circle.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Convert polar/rectangular",
        [
            "The two conversion pairs are worth memorizing as identities, not as one-way recipes. "
            "$x=r\\cos\\theta$, $y=r\\sin\\theta$, $r^2=x^2+y^2$, and $\\tan\\theta=y/x$ (with quadrant). "
            "Any polar equation can be rewritten by substituting; any rectangular equation can be rewritten "
            "by grouping $x^2+y^2$ and $x$ or $y$.",
            "Lines: $x=2$ becomes $r\\cos\\theta=2$. $y=-3$ becomes $r\\sin\\theta=-3$. A slanted line through "
            "the origin is already polar: $\\theta=c$. Circles through the origin, as above, become "
            "$r=2a\\cos\\theta$ or $r=2a\\sin\\theta$.",
            "Going the other way, $r=4\\cos\\theta$ is the circle $(x-2)^2+y^2=4$. $r=1$ is $x^2+y^2=1$. "
            "$\\theta=\\pi/4$ is $y=x$ (with the usual caveats about the ray versus the line).",
            "Points convert one at a time. Prefer $r\\geq0$ and $\\theta\\in(-\\pi,\\pi]$ or $[0,2\\pi)$ as the "
            "problem requests. A calculator’s rectangular-to-polar mode uses atan2; your by-hand version is "
            "reference angle plus ASTC.",
            "Some equations are nicer in one system. $x^2+y^2=2x$ is a chore until polar eats it. $r=2/(1-\\cos\\theta)$ "
            "is a polar parabola (Unit 6 eccentricity) that is messier in $x$ and $y$. Choose the system that "
            "matches the symmetry.",
            "A conversion error almost always comes from the wrong quadrant for $\\theta$ or from forgetting "
            "$r^2=x^2+y^2$ and writing $r=x^2+y^2$ instead. Dimensional sense: $r$ is a length, $x^2+y^2$ is a length squared.",
        ],
        "Conversion is the dictionary between the two graphing languages of the plane. Conics, complex numbers, "
        "and calculus area problems all require you to be bilingual.",
        "For points, use $x=r\\cos\\theta$ and $y=r\\sin\\theta$. For equations, replace $x^2+y^2$ with $r^2$ "
        "and $x$ with $r\\cos\\theta$. Then cancel a leftover $r=0$ (the pole) if it is an extra factor.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", _polar(lambda th: 2 * math.cos(th), -math.pi / 2, math.pi / 2, 80))],
                points=[(1, 0, "center (1,0)"), (2, 0, "(2,0)"), (0, 0, "origin")],
                xlim=(-1, 3), ylim=(-2, 2),
            ),
            "$r=2\\cos\\theta$ is the circle $(x-1)^2+y^2=1$",
            "Converted points include the origin and $(2,0)$. The polar formula only needs $\\theta\\in[-\\pi/2,\\pi/2]$ to draw the full circle.",
        )
        + solved(
            10, "Convert $(0,2)$ to polar with $r>0$, $\\theta\\in[0,2\\pi)$.",
            ["$r=2$.",
             "Positive y-axis: $\\theta=\\pi/2$.",
             "The pair is $(2,\\pi/2)$."],
            "$(2,\\pi/2)$", "", "Easy",
        )
        + solved(
            11, "Find the $x$-coordinate of $(4,5\\pi/6)$.",
            ["$x=4\\cos(5\\pi/6)=4(-\\sqrt{3}/2)=-2\\sqrt{3}$.",
             "The y-coordinate would be $4\\cdot1/2=2$."],
            "$-2\\sqrt{3}$", "", "Medium",
        )
        + solved(
            12, "Convert $x^2+y^2=2x$ to polar and simplify.",
            ["$r^2=2r\\cos\\theta$.",
             "Bring to one side: $r(r-2\\cos\\theta)=0$.",
             "So $r=0$ (the pole, already on the curve) or $r=2\\cos\\theta$."],
            "$r=2\\cos\\theta$", "The pole satisfies $r=2\\cos\\theta$ at $\\theta=\\pi/2$ as well.", "Hard",
        ),
        ("Writing $r=x^2+y^2$",
         "The identity is $r^2=x^2+y^2$. Dropping the square makes every later simplification dimensionally wrong "
         "and usually produces a spiral that was supposed to be a circle."),
        ("Cancel $r$ only after noting $r=0$",
         "When $r^2=2r\\cos\\theta$, factor. The solution $r=0$ is the pole; check whether it already lies on "
         "$r=2\\cos\\theta$ before you throw it away as extra."),
        [
            "I can convert points both ways.",
            "I can rewrite $x=a$ and $y=b$ in polar.",
            "I can turn $x^2+y^2=2ax$ into $r=2a\\cos\\theta$.",
        ],
        16,
    )

    c5 = concept_block(
        "5. De Moivre intro",
        [
            "A complex number $z=x+iy$ can be written $z=r(\\cos\\theta+i\\sin\\theta)=r\\,\\mathrm{cis}\\,\\theta$, "
            "where $r=|z|$ and $\\theta=\\arg z$. De Moivre’s theorem says "
            "$\\bigl[r(\\cos\\theta+i\\sin\\theta)\\bigr]^n=r^n(\\cos(n\\theta)+i\\sin(n\\theta))$ for integer $n$. "
            "In words: raise the modulus to $n$ and multiply the angle by $n$.",
            "The geometric meaning is rotation and scaling. Squaring $1+i=\\sqrt{2}\\,\\mathrm{cis}(\\pi/4)$ rotates "
            "it to $\\pi/2$ and scales the modulus to $2$, landing on $2i$. Higher powers walk around a circle "
            "in equal angle steps.",
            "Roots run De Moivre in reverse. The $n$-th roots of $r\\,\\mathrm{cis}\\,\\theta$ are "
            "$r^{1/n}\\,\\mathrm{cis}\\dfrac{\\theta+2\\pi k}{n}$ for $k=0,1,\\ldots,n-1$. They lie equally spaced "
            "on a circle of radius $r^{1/n}$. Square roots come in a pair separated by $\\pi$; cube roots in an "
            "equilateral triangle.",
            "For $n=0$, every nonzero $z^0=1$. For negative integers, $z^{-1}=\\dfrac{1}{r}\\mathrm{cis}(-\\theta)$, "
            "which is the polar form of the reciprocal. De Moivre unifies powers and roots under one rotation rule.",
            "A common computation: $[2\\,\\mathrm{cis}(\\pi/6)]^3=8\\,\\mathrm{cis}(\\pi/2)=8i$. Always multiply "
            "the angle, do not raise the angle to a power. $\\theta^n$ is the wrong operation.",
            "De Moivre is the reason polar form exists in Precalculus. Rectangular form is painful for $z^{12}$; "
            "polar form is three lines. The next lesson practices the polar arithmetic (multiply, divide, conjugate) "
            "that makes De Moivre feel natural.",
        ],
        "Powers of complex numbers, roots of unity, and later Euler’s formula $e^{i\\theta}=\\mathrm{cis}\\,\\theta$ "
        "all start here. Rotation in the plane is multiplication by a unit complex number.",
        "Write $z$ in polar form, apply $r\\mapsto r^n$ and $\\theta\\mapsto n\\theta$, then convert back if the "
        "problem wants $a+bi$. For roots, include every $k=0,\\ldots,n-1$.",
        lesson_figure(
            argand([(1, 1, "1+i"), (0, 2, "(1+i)^2=2i")], lim=4),
            "De Moivre: $(1+i)^2=2i$ on the Argand plane",
            "$1+i$ has argument $\\pi/4$. Doubling the argument lands on the positive imaginary axis; the modulus becomes $2$.",
        )
        + solved(
            13, "State De Moivre’s formula for $[\\cos\\theta+i\\sin\\theta]^n$.",
            ["Modulus $1$ stays $1$.",
             "The angle multiplies by $n$.",
             "Result: $\\cos(n\\theta)+i\\sin(n\\theta)$."],
            "$\\cos(n\\theta)+i\\sin(n\\theta)$", "", "Easy",
        )
        + solved(
            14, "Compute $(1+i)^2$ with De Moivre.",
            ["$1+i=\\sqrt{2}\\,\\mathrm{cis}(\\pi/4)$.",
             "Square: $2\\,\\mathrm{cis}(\\pi/2)=2i$.",
             "Rectangular check: $(1+i)^2=1+2i-1=2i$."],
            "$2i$", "", "Medium",
        )
        + solved(
            15, "Find both square roots of $16\\,\\mathrm{cis}(\\pi/3)$.",
            ["Modulus $16^{1/2}=4$.",
             "Angles $(\\pi/3+2\\pi k)/2$ for $k=0,1$: $\\pi/6$ and $7\\pi/6$.",
             "Roots: $4\\,\\mathrm{cis}(\\pi/6)$ and $4\\,\\mathrm{cis}(7\\pi/6)$."],
            "$4\\,\\mathrm{cis}(\\pi/6),\\ 4\\,\\mathrm{cis}(7\\pi/6)$",
            "They differ in argument by $\\pi$, as square roots must.", "Hard",
        ),
        ("Raising the angle to the $n$-th power",
         "De Moivre multiplies the angle by $n$. Writing $\\cos(\\theta^n)$ is a different (wrong) function. "
         "Check $n=2$, $\\theta=\\pi/4$: you want $\\cos(\\pi/2)=0$, not $\\cos((\\pi/4)^2)$."),
        ("Include every $k$ for roots",
         "A calculator’s square-root button on a complex number returns one value. Algebra wants both (or all $n$). "
         "The missing roots are rotations by $2\\pi/n$."),
        [
            "I can raise a polar complex number to an integer power.",
            "I can find all $n$-th roots with De Moivre.",
            "I can interpret the result as rotation and scaling on the Argand plane.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Complex in polar form",
        [
            "Polar arithmetic is short. Multiply: multiply moduli, add arguments. Divide: divide moduli, "
            "subtract arguments. Conjugate: keep $r$, negate $\\theta$. Modulus $|z|=r$ is the distance from "
            "the origin on the Argand plane.",
            "Standard examples: $i=1\\,\\mathrm{cis}(\\pi/2)$, $-4=4\\,\\mathrm{cis}(\\pi)$, "
            "$3-3i=3\\sqrt{2}\\,\\mathrm{cis}(-\\pi/4)$ (quadrant IV). Always compute $r=\\sqrt{x^2+y^2}$ first, "
            "then the reference angle from $|x|$ and $|y|$, then attach the quadrant.",
            "The identity $z\\bar z=|z|^2$ is polar-obvious: $r\\,\\mathrm{cis}\\theta$ times $r\\,\\mathrm{cis}(-\\theta)$ "
            "is $r^2\\,\\mathrm{cis} 0=r^2$. Dividing $z/|z|$ produces a unit complex number, a pure rotation.",
            "Powers of $i$ become obvious: $i^n=\\mathrm{cis}(n\\pi/2)$, which cycles every $4$. Negative reals "
            "have argument $\\pi$ (or $-\\pi$, the same ray). Zero has modulus $0$ and undefined argument.",
            "Principal argument $\\mathrm{Arg}\\,z$ is usually taken in $(-\\pi,\\pi]$. When you add angles, "
            "reduce back into that interval. $(1+i)^8$ has argument $8\\cdot\\pi/4=2\\pi\\equiv0$, so the result "
            "is a positive real (modulus $(\\sqrt{2})^8=16$).",
            "Connecting the unit: polar points, polar graphs, De Moivre, and complex polar form are one geometry. "
            "A rose is a real polar graph; a power $z^n$ is a polar point spinning. The Argand plane is the "
            "xy-plane with extra multiplication.",
        ],
        "Complex polar form is the practical skill: multiply, divide, and power without expanding binomials. "
        "It is also the picture of 2D rotation matrices in Unit 8.",
        "Modulus first, quadrant-correct argument second, then multiply/add. Reduce the final argument into "
        "the requested interval before you convert back to $a+bi$.",
        lesson_figure(
            argand(
                [(3, 0, "3"), (0, 2, "2i"), (-2, 0, "-2"), (1, 1, "1+i")],
                lim=5,
            ),
            "Argand plane: real on the horizontal axis, imaginary vertical",
            "Each complex number is a vector from the origin. Polar form names that vector by length and angle.",
        )
        + solved(
            16, "Write $i$ in polar form.",
            ["Modulus $|i|=1$.",
             "Positive imaginary axis: argument $\\pi/2$.",
             "$i=1\\,\\mathrm{cis}(\\pi/2)$."],
            "$1\\,\\mathrm{cis}(\\pi/2)$", "", "Easy",
        )
        + solved(
            17, "Find the modulus and argument of $3-4i$.",
            ["Modulus $\\sqrt{9+16}=5$.",
             "Quadrant IV, reference $\\arctan(4/3)$.",
             "Argument $-\\arctan(4/3)$ (not the $3$-$4$-$5$ angle in QI)."],
            "$|z|=5$, $\\arg=-\\arctan(4/3)$", "A 3-4-5 triangle still helps the reference.", "Medium",
        )
        + solved(
            18, "Compute $(1+i)(1-i)$ using polar form.",
            ["Each has modulus $\\sqrt{2}$. Arguments $\\pi/4$ and $-\\pi/4$.",
             "Product modulus $2$, argument $0$.",
             "The product is $2$, matching the rectangular $(1+1)=2$."],
            "$2$", "Adding opposite arguments cancels the imaginary part.", "Hard",
        ),
        ("Leaving argument in quadrant I when $x<0$",
         "Modulus is never signed; argument carries the quadrant. A point in II with reference $\\pi/6$ has "
         "argument $5\\pi/6$, not $\\pi/6$ and not $-\\pi/6$."),
        ("Add arguments, then reduce mod $2\\pi$",
         "After a high power, an argument like $9\\pi/2$ should be reduced: $9\\pi/2-4\\pi=\\pi/2$. Principal "
         "value questions expect that reduction."),
        [
            "I can write $a+bi$ as $r\\,\\mathrm{cis}\\,\\theta$.",
            "I can multiply and divide in polar form.",
            "I can read modulus and argument from an Argand diagram.",
        ],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title, AUDIENCE, concepts, body, practice_slots(31, 25, STRETCH_LABEL),
    )
    return title, description, content, _u5_questions()


# ===========================================================================
# UNIT 6: Conic Sections
# ===========================================================================

def _u6_questions():
    qs = []
    _add(qs, [
        ("The parabola $y=\\dfrac{1}{8}x^2$ has focus:",
         "(0,2)",
         "Form $x^2=4py$ with $4p=8$, $p=2$, focus $(0,p)=(0,2)$.",
         ["(0,8)", "(2,0)", "(0,1/8)"]),
        ("Directrix of $x^2=8y$ is:",
         "y=-2",
         "$4p=8$, $p=2$, directrix $y=-p$.",
         ["y=2", "x=-2", "y=0"]),
        ("A parabola opens right if its standard form is:",
         "(y-k)^2=4p(x-h) with p>0",
         "Squared y-variable means horizontal opening.",
         ["(x-h)^2=4p(y-k)", "x^2/a^2+y^2/b^2=1", "xy=1"]),
        ("Vertex of $(y+1)^2=12(x-4)$ is:",
         "(4,-1)",
         "Read $(h,k)=(4,-1)$ from the shifted form.",
         ["(-1,4)", "(12,4)", "(0,0)"]),
        ("Distance from a point on a parabola to the focus equals distance to the:",
         "directrix",
         "That equidistance is the definition of a parabola.",
         ["vertex", "origin", "latus rectum only"]),
        ("$x^2+y^2=25$ is a circle of radius:",
         5,
         "$r^2=25$.",
         ["25", "10", "5/2"]),
        ("The ellipse $\\dfrac{x^2}{9}+\\dfrac{y^2}{4}=1$ has vertices:",
         "(\u00b13,0)",
         "Larger denominator $9$ is under $x^2$, so major axis horizontal, $a=3$.",
         ["(0,\u00b12)", "(\u00b12,0)", "(\u00b19,0)"]),
        ("For that ellipse, $c$ satisfies $c^2=a^2-b^2$, so $c=$:",
         "\\sqrt{5}",
         "$9-4=5$, $c=\\sqrt{5}$. Foci $(\\pm\\sqrt{5},0)$.",
         ["5", "\\sqrt{13}", "1"]),
        ("A circle is an ellipse with:",
         "a=b",
         "Equal semi-axes; eccentricity $0$.",
         ["a>b always", "foci at infinity", "no center"]),
        ("Center of $\\dfrac{(x-2)^2}{16}+\\dfrac{(y+3)^2}{9}=1$ is:",
         "(2,-3)",
         "Opposite the signs inside the shifted squares.",
         ["(-2,3)", "(16,9)", "(0,0)"]),
        ("The hyperbola $\\dfrac{x^2}{4}-\\dfrac{y^2}{9}=1$ opens:",
         "left-right",
         "The positive term is the $x^2$ term, so transverse axis is horizontal.",
         ["up-down", "as a circle", "only in quadrant I"]),
        ("Asymptotes of $\\dfrac{x^2}{a^2}-\\dfrac{y^2}{b^2}=1$ are:",
         "y=\u00b1(b/a)x",
         "The rectangle $a$ by $b$ produces those two lines through the origin (or through the center).",
         ["y=\u00b1(a/b)x", "x=\u00b1a", "y=\u00b1b"]),
        ("Vertices of $\\dfrac{y^2}{16}-\\dfrac{x^2}{9}=1$ are:",
         "(0,\u00b14)",
         "Transverse axis vertical, $a=4$.",
         ["(\u00b13,0)", "(0,\u00b13)", "(\u00b14,0)"]),
        ("A hyperbola has two branches because:",
         "the difference of distances to two foci is constant",
         "That two-focus definition produces two disconnected curves.",
         ["it is a circle cut in half", "eccentricity is 0", "a=b"]),
        ("$xy=1$ is a hyperbola rotated; its asymptotes are:",
         "the coordinate axes",
         "Rectangular hyperbola $xy=c$ has the axes as asymptotes.",
         ["y=\u00b1x only", "a circle", "no asymptotes"]),
        ("Complete the square: $x^2+y^2-6x+4y=0$ becomes:",
         "(x-3)^2+(y+2)^2=13",
         "$x^2-6x+y^2+4y=0\\Rightarrow (x-3)^2-9+(y+2)^2-4=0$.",
         ["(x-3)^2+(y+2)^2=0", "(x+3)^2+(y-2)^2=13", "x^2+y^2=13"]),
        ("$x^2-y^2-4x=5$ after completing the square is:",
         "(x-2)^2-y^2=9",
         "$(x-2)^2-4-y^2=5$, so $(x-2)^2-y^2=9$, a hyperbola.",
         ["a circle", "(x-2)^2+y^2=9", "a parabola"]),
        ("$y=x^2-6x+5$ as a conic is a:",
         "parabola",
         "Only one variable is squared.",
         ["circle", "ellipse", "hyperbola"]),
        ("If both squared terms have the same sign and different coefficients, the conic is:",
         "an ellipse (or circle if equal)",
         "Same sign, possibly stretched.",
         ["a hyperbola", "a parabola", "two lines"]),
        ("Opposite signs on $x^2$ and $y^2$ classify the conic as:",
         "a hyperbola",
         "Difference of squares in the standard form.",
         ["an ellipse", "a point", "a parabola"]),
        ("Eccentricity of a circle is:",
         0,
         "$e=c/a=0$ when foci coincide with the center.",
         ["1", ">1", "undefined"]),
        ("Eccentricity of a parabola is:",
         1,
         "By definition $e=1$ for a parabola (focus-directrix ratio).",
         ["0", "2", "<1"]),
        ("An ellipse has eccentricity:",
         "0 \u2264 e < 1",
         "$c<a$ so $e=c/a<1$.",
         ["e=1", "e>1", "e=2"]),
        ("A hyperbola has eccentricity:",
         "e>1",
         "$c>a$ for a hyperbola.",
         ["e=0", "e=1", "0<e<1"]),
        ("Polar $r=\\dfrac{ed}{1-e\\cos\\theta}$ with $e=1$ is a:",
         "parabola",
         "The polar conic dictionary: $e<1$ ellipse, $e=1$ parabola, $e>1$ hyperbola.",
         ["ellipse", "circle", "rose"]),
        ("A satellite orbit that is a slightly flattened circle is modeled by:",
         "an ellipse with small e",
         "Kepler: bound orbits are ellipses with the sun at a focus.",
         ["a hyperbola", "a parabola e=1", "a line"]),
        ("A parabolic mirror focuses incoming parallel rays to:",
         "the focus",
         "The reflection property of a parabola.",
         ["the directrix", "the vertex only", "infinity along the axis? no, to the focus"]),
        ("The whisper-gallery property belongs to:",
         "an ellipse",
         "Sound from one focus reflects to the other focus.",
         ["a hyperbola", "a parabola only", "a circle only"]),
        ("A hyperbolic navigation system uses:",
         "difference of distances to two foci",
         "That is the definition of a hyperbola; LORAN-style systems use it.",
         ["sum of distances", "a single radius", "eccentricity 0"]),
        ("The latus rectum of a parabola $x^2=4py$ is a segment through the focus of length:",
         "4p",
         "The focal width is $|4p|$.",
         ["p", "2p", "p^2"]),
        ("Foci of $\\dfrac{x^2}{25}+\\dfrac{y^2}{9}=1$ are:",
         "(\u00b14,0)",
         "$c^2=25-9=16$, $c=4$.",
         ["(\u00b15,0)", "(0,\u00b14)", "(\u00b13,0)"]),
        ("For $\\dfrac{x^2}{9}-\\dfrac{y^2}{16}=1$, $c=$:",
         5,
         "$c^2=a^2+b^2=9+16=25$.",
         ["7", "4", "3"]),
        ("Equation of a circle center $(3,-1)$ radius $4$ is:",
         "(x-3)^2+(y+1)^2=16",
         "Standard circle form.",
         ["(x+3)^2+(y-1)^2=16", "(x-3)^2+(y+1)^2=4", "x^2+y^2=16"]),
        ("$x^2=12y$ has $p=$:",
         3,
         "$4p=12$.",
         ["12", "6", "4"]),
        ("Major axis length of $\\dfrac{x^2}{16}+\\dfrac{y^2}{4}=1$ is:",
         8,
         "$2a=8$ because $a=4$.",
         ["4", "2", "16"]),
        ("Which is not a conic section of a plane with a double cone?",
         "a sine wave",
         "The plane slices give circle, ellipse, parabola, hyperbola (and degenerate cases).",
         ["ellipse", "parabola", "hyperbola"]),
        ("$e=c/a$ for an ellipse uses $c$ as the:",
         "center-to-focus distance",
         "$c^2=a^2-b^2$.",
         ["major-axis length", "radius", "directrix distance only"]),
        ("A vertical parabola $(x-h)^2=4p(y-k)$ with $p<0$ opens:",
         "down",
         "Negative $p$ reverses the opening.",
         ["up", "right", "left"]),
        ("Asymptotes of $\\dfrac{(x-1)^2}{9}-\\dfrac{(y+2)^2}{4}=1$ pass through:",
         "(1,-2)",
         "The center is the crossing of the asymptotes.",
         ["(0,0)", "(3,2)", "(1,2)"]),
        ("Completing the square on $y^2+8x=0$ yields:",
         "y^2=-8x, a left-opening parabola",
         "$4p=-8$, $p=-2$, vertex origin, opens left.",
         ["a circle", "an ellipse", "a hyperbola"]),
        ("The circle $x^2+y^2-2x=0$ has radius:",
         1,
         "$(x-1)^2+y^2=1$.",
         ["2", "0", "\\sqrt{2}"]),
        ("Ellipse vs hyperbola: the foci of an ellipse lie:",
         "inside, on the major axis",
         "Hyperbola foci lie outside along the transverse axis.",
         ["outside the curve", "on the directrix", "at infinity"]),
        ("Polar conic $r=\\dfrac{4}{1+0.5\\cos\\theta}$ has $e=$:",
         "0.5",
         "Coefficient of cosine in the denominator’s second term is $e$.",
         ["4", "1", "2"]),
        ("That polar conic is therefore an:",
         "ellipse",
         "$e=0.5<1$.",
         ["parabola", "hyperbola", "rose"]),
        ("A flashlight beam (parallel rays from a bulb at the focus of a paraboloid) is the 3D version of:",
         "the parabolic reflection property",
         "Focus to parallel, or parallel to focus.",
         ["an ellipse whisper gallery", "hyperbola navigation", "a circular orbit"]),
        ("SAT Stretch: Classify $2x^2-8x+y^2+4y=0$ after completing the square.",
         "ellipse center (2,-2)",
         "$2(x^2-4x)+(y^2+4y)=0$, $2(x-2)^2-8+(y+2)^2-4=0$, $2(x-2)^2+(y+2)^2=12$, "
         "$\\dfrac{(x-2)^2}{6}+\\dfrac{(y+2)^2}{12}=1$, ellipse centered at $(2,-2)$.",
         ["hyperbola", "circle r=\\sqrt{6}", "parabola"]),
        ("SAT Stretch: The eccentricity of $\\dfrac{x^2}{25}+\\dfrac{y^2}{9}=1$ is:",
         "4/5",
         "$c=4$, $a=5$, $e=4/5$.",
         ["3/5", "5/4", "1"]),
        ("SAT Stretch: Hyperbola $\\dfrac{x^2}{9}-\\dfrac{y^2}{16}=1$ has asymptotes:",
         "y=\u00b1(4/3)x",
         "$b/a=4/3$.",
         ["y=\u00b1(3/4)x", "y=\u00b14x", "x=\u00b13"]),
        ("SAT Stretch: Which point on $x^2=8y$ is $5$ units from the focus $(0,2)$?",
         "(\u00b12\\sqrt{6}, 3)",
         "$4p=8$ so the focus is $(0,2)$. Substitute $y=x^2/8$ into $(x-0)^2+(y-2)^2=25$: "
         "$8y+(y-2)^2=25$, $y^2+4y-21=0$, $y=3$ (discard $y=-7$). Then $x^2=24$, so $x=\\pm 2\\sqrt{6}$. "
         "Check: distance from $(\\pm 2\\sqrt{6},3)$ to the directrix $y=-2$ is also $5$.",
         ["(4,2)", "(0,0)", "(0,5)"]),
        ("SAT Stretch: Complete the square to show $x^2-y^2-6x+8y=8$ is:",
         "hyperbola center (3,4)",
         "$(x-3)^2-9-(y-4)^2+16=8$, $(x-3)^2-(y-4)^2=1$.",
         ["ellipse center (3,4)", "circle", "two lines only"]),
        ("SAT Stretch: Polar $r=\\dfrac{6}{2-3\\cos\\theta}$ has $e=$:",
         "3/2",
         "Divide top and bottom by $2$: $r=\\dfrac{3}{1-(3/2)\\cos\\theta}$, so $e=3/2>1$, a hyperbola.",
         ["3", "2", "6"]),
        ("SAT Stretch: An elliptical orbit with $a=20$ and $c=12$ has periapsis distance:",
         8,
         "Closest approach $a-c=8$ (focus to near vertex).",
         ["12", "20", "32"]),
        ("SAT Stretch: The chord through the focus of $y^2=12x$ parallel to the directrix has length:",
         12,
         "Latus rectum length $|4p|$ with $4p=12$.",
         ["6", "3", "24"]),
        ("SAT Stretch: Which completed form is a degenerate conic (a point)?",
         "(x-1)^2+(y+2)^2=0",
         "Radius $0$ is a single point, a degenerate ellipse/circle.",
         ["(x-1)^2+(y+2)^2=1", "x^2-y^2=1", "y=x^2"]),
        ("SAT Stretch: For $\\dfrac{(x-h)^2}{a^2}+\\dfrac{(y-k)^2}{b^2}=1$ with $a>b$, the foci are:",
         "(h\u00b1c, k) with c=sqrt(a^2-b^2)",
         "Horizontal major axis: foci shift $c$ from the center along $x$.",
         ["(h, k\u00b1c)", "(h\u00b1a, k)", "(0, \u00b1c)"]),
    ])
    return qs[:55]


def build_unit6():
    title = "Precalculus Unit 6: Conic Sections"
    description = (
        "Parabolas, circles and ellipses, hyperbolas, completing the square to classify, eccentricity, "
        "and applications — with graphs of the actual conics, not placeholder dots."
    )
    concepts = [
        "Parabolas",
        "Circles and ellipses",
        "Hyperbolas",
        "Complete the square to classify",
        "Eccentricity",
        "Applications",
    ]

    ru, rd, lu, ld = _hyp_branches(2, 3, 6, 24)
    c1 = concept_block(
        "1. Parabolas",
        [
            "A parabola is the set of points equidistant from a focus and a directrix. In standard form, "
            "$(x-h)^2=4p(y-k)$ opens up if $p>0$ and down if $p<0$, with vertex $(h,k)$, focus $(h,k+p)$, "
            "and directrix $y=k-p$. Squaring $y$ instead, $(y-k)^2=4p(x-h)$, opens right or left.",
            "The number $|4p|$ is the length of the latus rectum, the chord through the focus parallel to the "
            "directrix. It is a quick graphing aid: from the focus, go $|2p|$ left and right (for a vertical "
            "parabola) to mark two extra points.",
            "The defining equidistance is also the reflection property: rays parallel to the axis reflect through "
            "the focus, which is why headlights and satellite dishes are parabolic. Algebraically you rarely "
            "need that property, but it is the reason the curve is famous.",
            "To graph $x^2=8y$, read $4p=8$, $p=2$. Vertex at the origin, focus $(0,2)$, directrix $y=-2$. "
            "The curve is a vertical stretch of $y=x^2/8$. Mark the focus and sketch a U sitting on the vertex.",
            "Shifted parabolas are translations. $(y+1)^2=12(x-4)$ has vertex $(4,-1)$ and $p=3$, so it opens "
            "right, focus $(7,-1)$. Completing the square (lesson 4 of this unit) is how you reach this form "
            "from an expanded equation such as $y^2+2y-12x+13=0$.",
            "A parabola is the $e=1$ conic. It is the boundary between ellipses ($e<1$) and hyperbolas ($e>1$). "
            "In polar form that dictionary becomes a single formula with a parameter $e$, which lesson 5 uses.",
        ],
        "Parabolas model trajectories (with gravity), mirrors, and the $e=1$ slice of a cone. The focus-directrix "
        "definition is the one definition that still works after a rotation.",
        "Identify which variable is squared (opening direction), read $4p$ (focus distance), and mark vertex, "
        "focus, and directrix before you plot extra points.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: x ** 2 / 8, -8, 8))],
                points=[(0, 0, "vertex"), (0, 2, "focus")],
                dashes=[("h", -2, "directrix y=-2")],
                xlim=(-9, 9), ylim=(-4, 10),
            ),
            "Parabola $x^2=8y$: focus $(0,2)$, directrix $y=-2$",
            "Every point on the blue curve is equally far from the focus and from the dashed directrix.",
        )
        + solved(
            1, "Find the focus of $x^2=8y$.",
            ["$4p=8$, so $p=2$.",
             "Vertical opening, vertex origin, focus $(0,p)=(0,2)$.",
             "Directrix $y=-2$."],
            "$(0,2)$", "", "Easy",
        )
        + solved(
            2, "Name the vertex of $(y+1)^2=12(x-4)$.",
            ["Compare to $(y-k)^2=4p(x-h)$.",
             "$h=4$, $k=-1$.",
             "Vertex $(4,-1)$; $4p=12$ so $p=3$, opens right."],
            "$(4,-1)$", "", "Medium",
        )
        + solved(
            3, "A point on $x^2=8y$ is $5$ units from the focus. How far is it from the directrix?",
            ["By definition the two distances are equal.",
             "The distance to the directrix is also $5$.",
             "This is $e=1$ in a single sentence."],
            "$5$", "", "Hard",
        ),
        ("Treating $p$ as $4p$",
         "The equation shows $4p$, not $p$. If $x^2=8y$ then $p=2$, not $8$. The focus is only $2$ units from "
         "the vertex, which is much closer than students who use $8$ expect."),
        ("Squared variable names the axis",
         "If $x$ is squared, the axis is vertical. If $y$ is squared, the axis is horizontal. That one check "
         "prevents drawing an up-down U for a left-right parabola."),
        [
            "I can read $p$, the focus, and the directrix from $x^2=4py$.",
            "I can locate the vertex of a shifted parabola.",
            "I can use the focus-directrix definition numerically.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Circles and ellipses",
        [
            "A circle $(x-h)^2+(y-k)^2=r^2$ is the set of points at fixed distance $r$ from the center. It is "
            "also the ellipse with $a=b=r$. The helper picture of a circle with a marked radius is useful, but "
            "the matching graph is the actual circle or ellipse in the plane.",
            "An ellipse $\\dfrac{(x-h)^2}{a^2}+\\dfrac{(y-k)^2}{b^2}=1$ with $a>b$ has a horizontal major axis "
            "of length $2a$, a minor axis of length $2b$, and foci $(h\\pm c,k)$ where $c^2=a^2-b^2$. If $b>a$, "
            "the major axis is vertical and the foci shift in $y$.",
            "The geometric definition: the sum of distances to the two foci is the constant $2a$. That is why "
            "you can draw an ellipse with two pins and a loop of string. It is also the whisper-gallery property: "
            "a sound from one focus reflects to the other.",
            "Graphing: plot the center, run $a$ along the major axis and $b$ along the minor, sketch the box, "
            "and draw a smooth oval tangent to the box at the four vertices. Mark the foci inside, on the major axis.",
            "A circle is the $e=0$ ellipse. Flattening the circle (increasing $c$ toward $a$) increases "
            "eccentricity toward $1$ and eventually, in the limit, the ellipse opens into a parabola.",
            "Intercepts of $\\dfrac{x^2}{9}+\\dfrac{y^2}{4}=1$ are $(\\pm3,0)$ and $(0,\\pm2)$. Those four points "
            "plus the center are enough to sketch. The foci sit at $(\\pm\\sqrt{5},0)$, inside the oval.",
        ],
        "Ellipses are the bound orbits of Kepler’s first law and the cross-sections of cylinders. Circles are "
        "the special case you already knew; the new skill is $a$, $b$, $c$, and the two-foci string definition.",
        "Compare the denominators to name the major axis. Compute $c=\\sqrt{|a^2-b^2|}$. Plot vertices first, "
        "foci second. If $a=b$, stop and call it a circle.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", _ellipse(3, 2))],
                points=[(3, 0, "a=3"), (0, 2, "b=2"), (math.sqrt(5), 0, "focus"), (-math.sqrt(5), 0, "")],
                xlim=(-5, 5), ylim=(-4, 4),
            ),
            "Ellipse $\\dfrac{x^2}{9}+\\dfrac{y^2}{4}=1$ with foci $(\\pm\\sqrt{5},0)$",
            "The major axis is horizontal because $9>4$. The foci lie inside, on that axis.",
        )
        + solved(
            4, "Find the radius of $x^2+y^2=25$.",
            ["$r^2=25$, so $r=5$.",
             "Center at the origin.",
             "It is also an ellipse with $a=b=5$."],
            "$5$", "", "Easy",
        )
        + solved(
            5, "For $\\dfrac{x^2}{9}+\\dfrac{y^2}{4}=1$, name the vertices and $c$.",
            ["$a=3$, $b=2$, major axis along $x$.",
             "Vertices $(\\pm3,0)$; co-vertices $(0,\\pm2)$.",
             "$c^2=9-4=5$, $c=\\sqrt{5}$, foci $(\\pm\\sqrt{5},0)$."],
            "vertices $(\\pm3,0)$, $c=\\sqrt{5}$", "", "Medium",
        )
        + solved(
            6, "Find the center of $\\dfrac{(x-2)^2}{16}+\\dfrac{(y+3)^2}{9}=1$.",
            ["The shifts are $x-2$ and $y+3$.",
             "Center $(2,-3)$.",
             "$a=4$ horizontal, $b=3$ vertical, so the major axis is horizontal."],
            "$(2,-3)$", "", "Hard",
        ),
        ("Putting foci on the minor axis",
         "Foci always lie on the major axis, the longer one. If the larger denominator is under $y^2$, the "
         "foci move up and down, not left and right."),
        ("Box then oval",
         "Sketch the rectangle of width $2a$ and height $2b$ centered at $(h,k)$. The ellipse is the inscribed "
         "oval, not the rectangle itself and not a diamond through the vertices."),
        [
            "I can write a circle from center and radius.",
            "I can read $a$, $b$, and $c$ from an ellipse equation.",
            "I can locate the center of a shifted ellipse.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Hyperbolas",
        [
            "A hyperbola $\\dfrac{(x-h)^2}{a^2}-\\dfrac{(y-k)^2}{b^2}=1$ opens left-right. The vertices are "
            "$(h\\pm a,k)$, the foci $(h\\pm c,k)$ with $c^2=a^2+b^2$, and the asymptotes are the lines through "
            "the center with slopes $\\pm b/a$. If the $y^2$ term is the positive one, the hyperbola opens up-down.",
            "The geometric definition: the absolute difference of distances to two foci is the constant $2a$. "
            "That is why a hyperbola has two branches — one for each way of subtracting. Navigation systems "
            "that compare signal times are hyperbola problems.",
            "Graphing: plot the center, the vertices, and the fundamental rectangle of width $2a$ and height "
            "$2b$. Draw the diagonals of that rectangle; those are the asymptotes. Then sketch each branch "
            "through a vertex, hugging the asymptotes far out.",
            "The rectangular hyperbola $xy=c$ is a $45^\\circ$ rotation of $x^2-y^2=k$. Its asymptotes are the "
            "coordinate axes. You met $y=1/x$ as a rational parent in Algebra 2; it is this hyperbola.",
            "Unlike an ellipse, $c$ is larger than $a$, so the foci lie outside the vertices along the transverse "
            "axis. Eccentricity $e=c/a$ is therefore greater than $1$.",
            "A quick identification: if the expanded equation has $x^2$ and $y^2$ with opposite signs, you are "
            "looking at a hyperbola (after completing the square). Same signs mean ellipse; only one square "
            "means parabola.",
        ],
        "Hyperbolas are the unbound conics: slingshot space trajectories, shock waves, and difference-of-distance "
        "loci. The asymptotes are the most important graphing feature.",
        "Name the positive square (transverse axis). Build the rectangle $2a$ by $2b$. Draw diagonals (asymptotes), "
        "then the two branches through the vertices.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#4f46e5", ru), ("#4f46e5", rd), ("#4f46e5", lu), ("#4f46e5", ld),
                    ("#94a3b8", [(-6, -9), (6, 9)]),
                    ("#94a3b8", [(-6, 9), (6, -9)]),
                ],
                points=[(2, 0, "vertex"), (-2, 0, "")],
                xlim=(-7, 7), ylim=(-10, 10),
            ),
            "Hyperbola $\\dfrac{x^2}{4}-\\dfrac{y^2}{9}=1$ with asymptotes $y=\\pm\\dfrac{3}{2}x$",
            "Branches open left-right through $(\\pm2,0)$. Far from the origin they hug the gray asymptotes.",
        )
        + solved(
            7, "Does $\\dfrac{x^2}{4}-\\dfrac{y^2}{9}=1$ open left-right or up-down?",
            ["The $x^2$ term is the positive one.",
             "Transverse axis horizontal: left-right.",
             "Vertices $(\\pm2,0)$."],
            "left-right", "", "Easy",
        )
        + solved(
            8, "Write the asymptotes of $\\dfrac{x^2}{a^2}-\\dfrac{y^2}{b^2}=1$.",
            ["Through the origin (center), slopes $\\pm b/a$.",
             "$y=\\pm(b/a)x$.",
             "For $a=2$, $b=3$, that is $y=\\pm(3/2)x$."],
            "$y=\\pm(b/a)x$", "", "Medium",
        )
        + solved(
            9, "Find $c$ for $\\dfrac{x^2}{9}-\\dfrac{y^2}{16}=1$.",
            ["$c^2=a^2+b^2=9+16=25$.",
             "$c=5$.",
             "Foci $(\\pm5,0)$, outside the vertices $(\\pm3,0)$."],
            "$c=5$", "Addition under the square root, not subtraction as in an ellipse.", "Hard",
        ),
        ("Using $c^2=a^2-b^2$ on a hyperbola",
         "Ellipses subtract; hyperbolas add. If you subtract on a hyperbola you can get a negative $c^2$ and "
         "a fake “no foci” conclusion."),
        ("Asymptotes before branches",
         "Sketching the two lines first keeps the branches from drifting into the wrong pair of opposite angles "
         "of the rectangle."),
        [
            "I can tell which way a hyperbola opens.",
            "I can write the asymptotes from $a$ and $b$.",
            "I can compute $c=\\sqrt{a^2+b^2}$.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Complete the square to classify",
        [
            "Expanded conics such as $x^2+y^2-6x+4y=0$ hide their type. Completing the square on $x$ and on $y$ "
            "(and dividing to make the right-hand side $1$ when needed) produces a standard form you can name: "
            "circle, ellipse, parabola, hyperbola, or a degenerate case (point, line, two lines, empty set).",
            "Recipe. Group $x$ terms and $y$ terms. If an $x^2$ coefficient is not $1$, factor it out of the $x$ "
            "group before completing the square (same for $y$). Add the appropriate constants to both sides. "
            "Then read the signs of the squared terms.",
            "Classification: one squared variable — parabola. Two squared, same sign — ellipse (circle if the "
            "remaining coefficients match after moving to standard form). Two squared, opposite signs — hyperbola. "
            "If the right-hand side is $0$ and both squares are nonnegative, you may have a point; if it is negative, empty.",
            "Example: $x^2+y^2-6x+4y=0$ becomes $(x-3)^2+(y+2)^2=13$, a circle of radius $\\sqrt{13}$ centered "
            "at $(3,-2)$. Example: $x^2-y^2-4x=5$ becomes $(x-2)^2-y^2=9$, a hyperbola.",
            "Degenerate warning: $(x-1)^2+(y+2)^2=0$ is the single point $(1,-2)$. $x^2-y^2=0$ is the pair of "
            "lines $y=\\pm x$. A test may call these degenerate conics; they still come from the same completing-the-square process.",
            "Completing the square is the “messy equation in, named graph out” skill. Combined with Units 2 and 3, "
            "it is how you identify a curve from a general quadratic $Ax^2+Bxy+Cy^2+Dx+Ey+F=0$ when $B=0$. "
            "(The $B\\neq0$ rotation case is a later optional topic.)",
        ],
        "Classification by completing the square is the algebra that turns a general second-degree equation into "
        "a picture you already know how to graph.",
        "Factor leading coefficients, complete both squares, move the constant, then look at the signs. Name the "
        "conic before you bother with foci.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", [(3 + math.sqrt(13) * math.cos(t), -2 + math.sqrt(13) * math.sin(t))
                                    for t in [i * 2 * math.pi / 72 for i in range(73)]])],
                points=[(3, -2, "center (3,-2)")],
                xlim=(-2, 8), ylim=(-7, 3),
            ),
            "Circle $(x-3)^2+(y+2)^2=13$ obtained by completing the square",
            "The expanded starting equation $x^2+y^2-6x+4y=0$ did not look like a circle until the squares were completed.",
        )
        + solved(
            10, "Complete the square: $x^2+y^2-6x+4y=0$.",
            ["$x^2-6x+y^2+4y=0$.",
             "$(x-3)^2-9+(y+2)^2-4=0$.",
             "$(x-3)^2+(y+2)^2=13$."],
            "circle center $(3,-2)$, radius $\\sqrt{13}$", "", "Easy",
        )
        + solved(
            11, "Classify $y=x^2-6x+5$.",
            ["Only $x$ is squared.",
             "This is a parabola (vertical).",
             "Vertex by completing the square: $y=(x-3)^2-4$."],
            "parabola", "", "Medium",
        )
        + solved(
            12, "Show $x^2-y^2-6x+8y=8$ is a hyperbola and name the center.",
            ["$(x-3)^2-9-(y-4)^2+16=8$.",
             "$(x-3)^2-(y-4)^2=1$.",
             "Opposite signs: hyperbola, center $(3,4)$."],
            "hyperbola, center $(3,4)$", "", "Hard",
        ),
        ("Forgetting to factor a coefficient before completing the square",
         "From $2x^2-8x$ you must write $2(x^2-4x)$ and complete the square inside the parentheses, adding "
         "$2\\cdot4=8$ to the other side, not $4$. Skipping the factor throws the center and the radii off."),
        ("Signs after moving the constant",
         "If both squares end up with the same sign and the right side is negative, the graph is empty. That is "
         "still a classification, not a failed problem."),
        [
            "I can complete the square in $x$ and $y$.",
            "I can name the conic from the signs of the squares.",
            "I can recognize a degenerate point or line pair.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Eccentricity",
        [
            "Eccentricity $e$ measures how far a conic is from being circular. For ellipses and hyperbolas, "
            "$e=c/a$. For a circle $c=0$ so $e=0$. For an ellipse $0\\leq e<1$. For a parabola $e=1$ by definition "
            "(focus-directrix ratio). For a hyperbola $e>1$.",
            "The focus-directrix definition unifies all four: the set of points whose distance to a focus is $e$ "
            "times the distance to a corresponding directrix. When $e=1$ those distances are equal (a parabola). "
            "When $e<1$ the points stay closer to the focus (an ellipse). When $e>1$ they run away (a hyperbola).",
            "Polar form makes the unification algebraic: $r=\\dfrac{ed}{1-e\\cos\\theta}$ (or sine, or a plus). "
            "Reading $e$ off the formula after dividing so the constant in the denominator is $1$ tells you the type "
            "immediately. $r=\\dfrac{6}{2-3\\cos\\theta}=\\dfrac{3}{1-(3/2)\\cos\\theta}$ has $e=3/2$, a hyperbola.",
            "In orbits, small $e$ means a nearly circular path; $e$ near $1$ from below is a long thin ellipse; "
            "$e=1$ is escape on a parabola; $e>1$ is a hyperbolic flyby. The same number $e$ that classifies "
            "the graph classifies the physics.",
            "For $\\dfrac{x^2}{25}+\\dfrac{y^2}{9}=1$, $a=5$, $c=4$, $e=4/5=0.8$, a fairly flat ellipse. For a "
            "circle, quoting $e=0$ is a complete answer. For a parabola, quoting $e=1$ is a complete answer.",
            "Directrices of an ellipse sit outside at $x=\\pm a/e$ (horizontal major axis). You rarely need them "
            "for a sketch, but they complete the $e$-definition. Hyperbola directrices sit between the branches at $x=\\pm a/e$.",
        ],
        "Eccentricity is the single parameter that names every nondegenerate conic and that appears in polar "
        "conic formulas and in orbital mechanics.",
        "Compute $e=c/a$ for ellipse/hyperbola, or read $e$ from polar form after making the denominator $1-e\\cos\\theta$. "
        "Then classify: $0$, between $0$ and $1$, $1$, or greater than $1$.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#4f46e5", _ellipse(5, 3)),
                    ("#dc2626", sample_curve(lambda x: x ** 2 / 8, -6, 6)),
                ],
                xlim=(-6, 6), ylim=(-4, 8),
            ),
            "Blue ellipse ($e<1$) versus red parabola ($e=1$)",
            "The parabola is the $e=1$ boundary. Flatten the ellipse further and it would open toward a parabola.",
        )
        + solved(
            13, "State the eccentricity of a circle and of a parabola.",
            ["Circle: $e=0$.",
             "Parabola: $e=1$.",
             "Those two values are definitions worth memorizing exactly."],
            "circle $0$, parabola $1$", "", "Easy",
        )
        + solved(
            14, "Find $e$ for $\\dfrac{x^2}{25}+\\dfrac{y^2}{9}=1$.",
            ["$a=5$, $b=3$, $c=4$.",
             "$e=c/a=4/5$.",
             "Since $e<1$, the conic is an ellipse (already known from the equation)."],
            "$4/5$", "", "Medium",
        )
        + solved(
            15, "Identify $r=\\dfrac{6}{2-3\\cos\\theta}$ by eccentricity.",
            ["Divide numerator and denominator by $2$: $r=\\dfrac{3}{1-(3/2)\\cos\\theta}$.",
             "$e=3/2>1$.",
             "The graph is a hyperbola."],
            "hyperbola, $e=3/2$", "Always divide so the constant term in the denominator is $1$.", "Hard",
        ),
        ("Leaving polar form as $2-3\\cos\\theta$ and calling $e=3$",
         "The standard polar conic has $1-e\\cos\\theta$ in the denominator. You must divide through by the "
         "constant $2$ before the coefficient of cosine is $e$. Here $e=3/2$, not $3$."),
        ("$e=c/a$ with the wrong $a$",
         "For an ellipse $a$ is the larger semi-axis, the one the foci live on. Using the smaller $b$ in the "
         "denominator of $e$ makes $e>1$ and a fake hyperbola."),
        [
            "I know $e$ for circle, ellipse, parabola, and hyperbola.",
            "I can compute $e=c/a$ from a standard equation.",
            "I can read $e$ from a polar conic formula.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Applications",
        [
            "Parabolic mirrors and microphones use the reflection property: parallel incoming rays meet at the "
            "focus, and a source at the focus produces a parallel beam. Headlights, satellite dishes, and some "
            "solar cookers are physical paraboloids — 3D versions of this lesson’s 2D parabola.",
            "Elliptical orbits: Kepler’s first law says a planet travels on an ellipse with the sun at one focus. "
            "Periapsis (nearest point) is $a-c$ from that focus; apoapsis is $a+c$. A nearly circular orbit has "
            "small $e$. Comets can have $e$ close to $1$ (very long ellipses) or $e>1$ (one-time hyperbolic visits).",
            "Whispering galleries: an elliptical room sends a whisper from one focus to the other. The sum of "
            "path lengths is $2a$ for every reflection path that obeys the equal-angle law, matching the string definition.",
            "Hyperbolic navigation (LORAN and related systems): a receiver measures the difference in arrival "
            "times from two stations, hence a difference of distances, hence a hyperbola. A second pair of "
            "stations gives a second hyperbola; their intersection is the location.",
            "Trajectories in a uniform gravitational field (no air) are parabolas. Escape trajectories in an "
            "inverse-square field are parabolas or hyperbolas depending on energy. Precalculus does not require "
            "the physics derivation; it requires you to pick the right conic for the stated property.",
            "When a word problem mentions a focus and a directrix, it is a parabola. When it mentions a constant "
            "sum of distances, it is an ellipse. When it mentions a constant difference, it is a hyperbola. "
            "That dictionary is the application skill.",
        ],
        "Applications are how conics earn their place in Precalculus: optics, orbits, architecture, and navigation "
        "are all focus-directrix or two-foci geometry.",
        "Match the stated property to the definition: equal distances (parabola), constant sum (ellipse), constant "
        "difference (hyperbola). Then use $a$, $b$, $c$, or $p$ from earlier lessons to compute the number asked.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: x ** 2 / 8, -6, 6))],
                points=[(0, 2, "bulb/focus")],
                xlim=(-7, 7), ylim=(-1, 8),
            ),
            "Parabolic reflector: a source at the focus produces rays parallel to the axis",
            "In reverse, incoming parallel light (from a distant star) concentrates at the focus.",
        )
        + solved(
            16, "Where should the bulb sit in a parabolic headlight $x^2=8y$?",
            ["Focus of $x^2=8y$ is $(0,2)$.",
             "Place the bulb at the focus so the beam comes out parallel.",
             "The vertex is the back of the mirror, not the bulb location."],
            "$(0,2)$", "", "Easy",
        )
        + solved(
            17, "An ellipse has $a=20$ and $c=12$. How close does the planet get to the sun (at a focus)?",
            ["Periapsis $a-c=8$.",
             "Apoapsis would be $a+c=32$.",
             "Eccentricity $e=12/20=0.6$."],
            "$8$", "", "Medium",
        )
        + solved(
            18, "Why do two radio stations produce a hyperbolic locus for a receiver?",
            ["The receiver records a time difference, hence a distance difference.",
             "A constant difference of distances to two foci is the definition of a hyperbola.",
             "A second pair of stations gives a second hyperbola; intersection locates the receiver."],
            "constant difference of distances", "", "Hard",
        ),
        ("Putting the sun at the center of the ellipse",
         "Kepler’s law puts the sun at a focus, not at the center. The empty focus is a geometric point, not a second sun."),
        ("Name the property first",
         "If the problem never mentions a focus, it may just want a completed-square classification. If it mentions "
         "equal distances to a line and a point, it wants the parabola definition, not an orbit story."),
        [
            "I can place a bulb at a parabolic focus.",
            "I can compute periapsis $a-c$ on an elliptical orbit.",
            "I can connect time-difference navigation to hyperbolas.",
        ],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title, AUDIENCE, concepts, body, practice_slots(31, 25, STRETCH_LABEL),
    )
    return title, description, content, _u6_questions()


# ===========================================================================
# UNIT 7: Sequences, Series & Limits Intro
# ===========================================================================

def _u7_questions():
    qs = []
    _add(qs, [
        ("The sequence $3,7,11,15,\\ldots$ has common difference:",
         4,
         "Arithmetic: each term adds $4$.",
         ["3", "7", "12"]),
        ("The $n$th term of that sequence is:",
         "4n-1",
         "$a_n=3+(n-1)4=4n-1$.",
         ["4n+3", "n+4", "3n"]),
        ("A geometric sequence with $a_1=5$ and $r=2$ has $a_4=$:",
         40,
         "$5\\cdot2^{3}=40$.",
         ["10", "80", "32"]),
        ("The common ratio of $81,27,9,3,\\ldots$ is:",
         "1/3",
         "Each term is one-third of the previous.",
         ["3", "-3", "1/9"]),
        ("An arithmetic sequence cannot have a common ratio unless:",
         "it is constant (ratio 1) or a trivial two-term case",
         "Linear versus exponential growth disagree except in special cases.",
         ["the difference is 1", "n is even", "a1=0 always"]),
        ("$\\sum_{k=1}^{4} k$ equals:",
         10,
         "$1+2+3+4=10$.",
         ["4", "24", "16"]),
        ("$\\sum_{k=1}^{n} k$ equals:",
         "n(n+1)/2",
         "The Gauss formula for the arithmetic series of the first $n$ positives.",
         ["n^2", "n(n-1)/2", "2n"]),
        ("Sigma notation $\\sum_{k=0}^{3} 2^k$ expands to:",
         "1+2+4+8",
         "Index from $0$ to $3$: $2^0$ through $2^3$.",
         ["2+4+6+8", "0+2+4+6", "2^3 only"]),
        ("The sum of an arithmetic series with $n$ terms, first $a_1$, last $a_n$ is:",
         "n(a1+an)/2",
         "Average of the first and last, times the count.",
         ["n a1", "(a1+an)/2", "n(n-1)d/2 only"]),
        ("$\\sum_{k=1}^{5} (2k-1)$ is the sum of the first five:",
         "odd positives",
         "$1+3+5+7+9=25$.",
         ["evens", "powers of 2", "multiples of 3"]),
        ("Infinite geometric $|r|<1$ with first term $a$ sums to:",
         "a/(1-r)",
         "The remainder of the geometric series formula as $n\\to\\infty$.",
         ["a/r", "a(1-r)", "infinity always"]),
        ("$1+\\dfrac{1}{2}+\\dfrac{1}{4}+\\dfrac{1}{8}+\\cdots$ equals:",
         2,
         "$a=1$, $r=1/2$, $1/(1-1/2)=2$.",
         ["1", "infinity", "1/2"]),
        ("$1+2+4+8+\\cdots$ diverges because:",
         "|r|=2>1",
         "The terms grow; there is no finite sum.",
         ["a=1", "the terms are integers", "n is infinite"]),
        ("Repeating decimal $0.333\\ldots=0.3+0.03+0.003+\\cdots$ is geometric with $r=$:",
         "0.1",
         "$a=0.3$, $r=1/10$, sum $0.3/(1-0.1)=1/3$.",
         ["0.3", "3", "1/3"]),
        ("A geometric series with $r=-1/2$ and $a=1$ converges to:",
         "2/3",
         "$1/(1-(-1/2))=1/(3/2)=2/3$.",
         ["1/2", "2", "-1"]),
        ("Graphically, $\\lim_{x\\to2}(x+1)$ is the y-value the graph approaches as $x$ approaches:",
         2,
         "The height approaches $3$. The function is also defined there.",
         ["1", "3 as the input", "infinity"]),
        ("If a graph has a hole at $x=1$ but the nearby y-values approach $4$, the limit is:",
         4,
         "Limits care about approach, not the missing point.",
         ["undefined always", "1", "0"]),
        ("A jump discontinuity (left height $2$, right height $5$) means the two-sided limit:",
         "does not exist",
         "Left and right limits disagree.",
         ["equals 2", "equals 5", "equals 3.5"]),
        ("As $x\\to\\infty$, $y=1/x$ approaches:",
         0,
         "The x-axis is a horizontal asymptote.",
         ["1", "infinity", "-1"]),
        ("A vertical asymptote at $x=3$ means as $x\\to3$, $|f(x)|$:",
         "grows without bound",
         "The limit is infinite (does not exist as a real number).",
         ["approaches 3", "approaches 0", "is 1"]),
        ("$\\lim_{x\\to3}\\dfrac{x^2-9}{x-3}$ equals:",
         6,
         "Factor: $(x-3)(x+3)/(x-3)\\to6$ for $x\\neq3$.",
         ["0", "undefined", "3"]),
        ("$\\lim_{x\\to\\infty}\\dfrac{2x^2+1}{x^2-5}$ equals:",
         2,
         "Divide by $x^2$: ratio of leadings $2/1=2$.",
         ["0", "infinity", "1"]),
        ("$\\lim_{x\\to\\infty}\\dfrac{3x}{x^2+1}$ equals:",
         0,
         "Denominator degree larger.",
         ["3", "1", "infinity"]),
        ("$\\lim_{x\\to0}\\dfrac{x}{x}$ equals:",
         1,
         "For $x\\neq0$ the ratio is $1$; the limit is $1$ even though $x=0$ is undefined.",
         ["0", "undefined", "infinity"]),
        ("If after cancelling a rational the remaining polynomial is $2x+1$, then as $x\\to4$ the limit is:",
         9,
         "Plug in to the simplified expression: $8+1=9$.",
         ["4", "2", "undefined"]),
        ("Squeeze: if $g\\leq f\\leq h$ near $a$ and $\\lim g=\\lim h=L$, then $\\lim f=$:",
         "L",
         "The squeeze (sandwich) theorem.",
         ["g(a)", "does not exist", "0"]),
        ("$-x^2\\leq x^2\\sin(1/x)\\leq x^2$ for $x\\neq0$ squeezes the middle to:",
         "0 as x\\to 0",
         "Both $-x^2$ and $x^2$ go to $0$.",
         ["1", "infinity", "sin(1/x)"]),
        ("Why does $\\sin x$ squeezed by $\\pm1$ not prove $\\lim_{x\\to\\infty}\\sin x=0$?",
         "the bounding functions do not share a limit of 0 at infinity",
         "$\\pm1$ do not both approach $0$; they stay put. Squeeze needs matching limits.",
         ["sin is undefined", "1 is too small", "x is not 0"]),
        ("$|\\mathrm{sinc}|$ idea: $\\left|\\dfrac{\\sin x}{x}\\right|\\leq\\dfrac{1}{|x|}$ for large $|x|$ implies as $x\\to\\infty$ the fraction:",
         "goes to 0",
         "The bound $1/|x|\\to0$, so squeeze to $0$.",
         ["goes to 1", "oscillates with amplitude 1", "is undefined"]),
        ("A constant sequence $a_n=7$ has limit:",
         7,
         "Eventually (in fact always) the terms sit at $7$.",
         ["0", "n", "infinity"]),
        ("$a_n=2n+1$ is arithmetic with $d=$:",
         2,
         "Each term increases by $2$.",
         ["1", "2n", "n"]),
        ("Geometric $a_n=3\\cdot(1/2)^{n-1}$ has $a_6=$:",
         "3/32",
         "$3\\cdot(1/2)^5=3/32$.",
         ["3/16", "3/2", "32/3"]),
        ("$\\sum_{k=1}^{10} 5$ equals:",
         50,
         "Ten copies of $5$.",
         ["5", "15", "10"]),
        ("Partial sum $s_n=\\dfrac{1-(1/3)^n}{1-1/3}$ of $a=1,r=1/3$ tends to:",
         "3/2",
         "As $n\\to\\infty$, $(1/3)^n\\to0$, so $s_n\\to1/(2/3)=3/2$.",
         ["1", "3", "0"]),
        ("If $|r|=1$ and $r\\neq1$, an infinite geometric series:",
         "diverges (oscillates or fails to settle)",
         "$r=-1$ oscillates; $r=1$ is the constant series $a+a+\\cdots$, which diverges unless $a=0$.",
         ["always sums to a", "converges to 0", "equals n"]),
        ("$\\lim_{x\\to2^-}\\dfrac{1}{x-2}$ tends to:",
         "-\u221e",
         "From the left, the denominator is a small negative.",
         ["+\u221e", "0", "2"]),
        ("$\\lim_{x\\to\\infty}\\dfrac{5x^3-x}{10x^3+4}=$:",
         "1/2",
         "Lead ratio $5/10$.",
         ["5", "0", "5/4"]),
        ("Hole of $\\dfrac{x^2-1}{x-1}$ corresponds to a limit as $x\\to1$ of:",
         2,
         "Simplified $x+1\\to2$.",
         ["0", "1", "undefined"]),
        ("The sequence $1,1/2,1/3,1/4,\\ldots$ plotted on a number line crowds toward:",
         0,
         "The terms approach the origin from the right.",
         ["1", "infinity", "-1"]),
        ("$\\sum_{k=1}^{n} r^{k-1}=\\dfrac{1-r^n}{1-r}$ for $r\\neq1$. If $r=1$ the sum is:",
         "n",
         "$n$ terms of $1$.",
         ["1", "0", "infinity"]),
        ("A recursive $a_1=4$, $a_{n+1}=a_n+3$ is:",
         "arithmetic with d=3",
         "Add $3$ each time, start at $4$.",
         ["geometric r=3", "neither", "harmonic"]),
        ("$\\lim_{x\\to0} x\\sin(1/x)$ equals:",
         0,
         "Squeeze: $-|x|\\leq x\\sin(1/x)\\leq|x|$.",
         ["1", "does not exist", "infinity"]),
        ("First term $a=8$, $r=1/4$, infinite sum:",
         "32/3",
         "$8/(1-1/4)=8/(3/4)=32/3$.",
         ["2", "8", "4"]),
        ("$\\lim_{x\\to-\\infty}\\dfrac{x}{\\sqrt{x^2+1}}$ equals:",
         "-1",
         "For large negative $x$, factor $|x|=-x$ out of the square root.",
         ["1", "0", "infinity"]),
        ("Sigma $\\sum_{k=3}^{6} k^2$ equals:",
         86,
         "$9+16+25+36=86$.",
         ["70", "91", "14"]),
        ("SAT Stretch: The infinite geometric $a=5$, $r=-2/3$ sums to:",
         "3",
         "$5/(1-(-2/3))=5/(5/3)=3$.",
         ["5", "-3", "15/2"]),
        ("SAT Stretch: $\\lim_{x\\to2}\\dfrac{x^3-8}{x-2}$ equals:",
         12,
         "Factor $x^3-8=(x-2)(x^2+2x+4)$, so the limit is $4+4+4=12$.",
         ["0", "8", "6"]),
        ("SAT Stretch: How many terms of $2+6+18+\\cdots$ are needed to exceed $2000$ if you only used a finite geometric sum?",
         "n=7",
         "$s_n=2(3^n-1)/2=3^n-1>2000$, $3^n>2001$, $3^6=729$, $3^7=2187$, so $n=7$.",
         ["n=6", "n=8", "n=5"]),
        ("SAT Stretch: $\\lim_{x\\to\\infty}(\\sqrt{x^2+4x}-x)$ equals:",
         2,
         "Rationalize: $\\dfrac{4x}{\\sqrt{x^2+4x}+x}\\to\\dfrac{4}{1+1}=2$.",
         ["0", "infinity", "4"]),
        ("SAT Stretch: If $0\\leq a_n\\leq b_n$ and $\\sum b_n$ converges, then $\\sum a_n$:",
         "converges (comparison)",
         "A Precalculus glimpse of the comparison test: squeezed partial sums are bounded and increasing.",
         ["diverges", "equals 0", "equals sum b_n"]),
        ("SAT Stretch: $\\lim_{h\\to0}\\dfrac{(3+h)^2-9}{h}$ equals:",
         6,
         "Expand: $(9+6h+h^2-9)/h=6+h\\to6$. This is the derivative of $x^2$ at $3$.",
         ["9", "0", "3"]),
        ("SAT Stretch: The repeating $0.121212\\ldots$ as a geometric series equals:",
         "4/33",
         "$0.12+0.0012+\\cdots=0.12/(1-0.01)=0.12/0.99=12/99=4/33$.",
         ["12/90", "1/8", "12/100"]),
        ("SAT Stretch: Sequence $a_n=\\dfrac{n}{n+1}$ has limit $1$. Which $N$ guarantees $|a_n-1|<0.01$ for $n>N$?",
         "N=99",
         "$|a_n-1|=1/(n+1)<0.01\\Rightarrow n+1>100\\Rightarrow n>99$.",
         ["N=1", "N=1000", "N=0"]),
        ("SAT Stretch: $\\sum_{k=0}^{\\infty} (1/2)^k \\cos(k\\pi)$ converges to:",
         "2/3",
         "$\\cos(k\\pi)=(-1)^k$, so this is $1/(1-(-1/2))=2/3$.",
         ["1", "0", "diverges"]),
        ("SAT Stretch: $\\lim_{x\\to0}\\dfrac{\\sin(3x)}{x}$ using squeeze/small-angle intuition equals:",
         3,
         "$\\dfrac{\\sin(3x)}{3x}\\cdot3\\to1\\cdot3=3$.",
         ["1", "0", "sin 3"]),
    ])
    return qs[:55]


def build_unit7():
    title = "Precalculus Unit 7: Sequences, Series & Limits Intro"
    description = (
        "Arithmetic and geometric sequences, sigma notation, infinite geometric sums, graphical limit "
        "intuition, algebraic rational limits, and the squeeze idea — with number lines and plotted terms."
    )
    concepts = [
        "Arithmetic and geometric",
        "Sigma notation",
        "Infinite geometric",
        "Limit intuition graphically",
        "Limit algebraically (rational)",
        "Squeeze idea",
    ]

    seq_pts = [(n, 3 + (n - 1) * 4) for n in range(1, 7)]
    c1 = concept_block(
        "1. Arithmetic and geometric",
        [
            "A sequence is an ordered list $a_1,a_2,a_3,\\ldots$. An arithmetic sequence has a constant difference "
            "$d=a_{n+1}-a_n$. Its explicit formula is $a_n=a_1+(n-1)d$. The graph of points $(n,a_n)$ lies on a "
            "straight line — discrete linear growth.",
            "A geometric sequence has a constant ratio $r=a_{n+1}/a_n$ (when terms are nonzero). Explicit formula "
            "$a_n=a_1 r^{n-1}$. The points $(n,a_n)$ lie on an exponential curve. Growth ($|r|>1$), decay ($0<|r|<1$), "
            "or oscillation (negative $r$) are all geometric.",
            "Recognizing the type is the first move. If differences are constant, arithmetic. If ratios are constant, "
            "geometric. If neither, it is some other sequence (possibly $n^2$, Fibonacci, or a rational $n/(n+1)$).",
            "Recursive definitions specify a start and a rule: $a_1=4$, $a_{n+1}=a_n+3$ is arithmetic with $d=3$. "
            "$b_1=5$, $b_{n+1}=2b_n$ is geometric with $r=2$. Recursion is how computers generate the list; the "
            "explicit formula is how you jump to $a_{100}$ without listing $99$ terms.",
            "Word problems: a theater with $20$ extra seats in each row is arithmetic. A bouncing ball that rises "
            "to $80\\%$ of the previous height is geometric. Interest compounded per period is geometric. A job "
            "that adds a fixed raise each year is arithmetic.",
            "Plotting the first several terms on a number line (for 1D sequences of positions) or as points "
            "$(n,a_n)$ makes the long-run behavior visible: arithmetic walks off to $\\pm\\infty$ unless $d=0$; "
            "geometric with $|r|<1$ crowds toward $0$.",
        ],
        "Sequences are discrete functions. Arithmetic is linear; geometric is exponential. Series (the next "
        "lessons) add them up. Limits (later) ask what the list is heading toward.",
        "Compute two or three differences and two or three ratios. If one of those is constant, write $a_n$ "
        "explicitly. Then you can evaluate any index without listing.",
        lesson_figure(
            xy_graph(
                points=[(n, 3 + (n - 1) * 4, f"a{n}") for n in range(1, 6)],
                xlim=(0, 6), ylim=(0, 22), xlab="n", ylab="a_n",
            ),
            "Arithmetic terms $3,7,11,15,19$ plotted as $(n,a_n)$",
            "The points lie on a line of slope $d=4$. A geometric sequence would hug an exponential instead.",
        )
        + solved(
            1, "Find $d$ and $a_n$ for $3,7,11,15,\\ldots$.",
            ["$d=4$.",
             "$a_n=3+(n-1)4=4n-1$.",
             "Check $n=4$: $16-1=15$."],
            "$d=4$, $a_n=4n-1$", "", "Easy",
        )
        + solved(
            2, "Find $a_4$ if $a_1=5$ and $r=2$ (geometric).",
            ["$a_n=5\\cdot2^{n-1}$.",
             "$a_4=5\\cdot8=40$.",
             "The list is $5,10,20,40$."],
            "$40$", "", "Medium",
        )
        + solved(
            3, "Identify $81,27,9,3,\\ldots$ and find $r$.",
            ["Ratios $27/81=1/3$, $9/27=1/3$.",
             "Geometric with $r=1/3$.",
             "Terms decay toward $0$."],
            "geometric, $r=1/3$", "", "Hard",
        ),
        ("Calling every decreasing sequence arithmetic",
         "Decay can be geometric (multiply by $1/3$) or arithmetic (subtract $4$). Check ratios as well as "
         "differences. $81,27,9$ has differences $-54,-18$, not constant."),
        ("Write $a_n$, then plug in $n$",
         "A question that asks for the $20$th term wants the explicit formula, not nineteen additions. Find $d$ "
         "or $r$ first."),
        [
            "I can recognize arithmetic versus geometric lists.",
            "I can write $a_n=a_1+(n-1)d$ and $a_n=a_1 r^{n-1}$.",
            "I can plot the first terms as points $(n,a_n)$.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Sigma notation",
        [
            "A series is a sum of sequence terms. Sigma notation $\\sum_{k=1}^{n} a_k$ means $a_1+a_2+\\cdots+a_n$. "
            "The index $k$ is a dummy variable; $\\sum_{j=1}^{n} a_j$ is the same sum. Changing the bounds is a "
            "substitution, like $u$-sub later in calculus.",
            "Expanding is the way to start. $\\sum_{k=0}^{3} 2^k=1+2+4+8=15$. $\\sum_{k=1}^{4} k=10$. "
            "$\\sum_{k=1}^{5}(2k-1)=1+3+5+7+9=25$, the first five odds.",
            "Closed forms you should know: $\\sum_{k=1}^{n} k=\\dfrac{n(n+1)}{2}$, $\\sum_{k=1}^{n} 1=n$, and "
            "the finite geometric sum $\\sum_{k=0}^{n-1} r^k=\\dfrac{1-r^n}{1-r}$ for $r\\neq1$. The arithmetic "
            "series formula $s_n=\\dfrac{n}{2}(a_1+a_n)$ is the same idea as Gauss pairing.",
            "Linearity: $\\sum (ca_k+b_k)=c\\sum a_k+\\sum b_k$. You can pull out constants and split sums. You "
            "cannot pull a $k$ out if it depends on the index — $\\sum k a_k$ is not $k\\sum a_k$.",
            "A common error is off-by-one in the number of terms. From $k=0$ to $k=3$ there are four terms, not "
            "three. From $k=3$ to $k=6$ there are four terms. Count: last minus first plus one.",
            "Sigma is the language of the rest of this unit. Infinite sums are limits of sigma partial sums. "
            "The geometric closed form is how repeating decimals become fractions. Later, Riemann sums in calculus "
            "are sigmas of rectangle areas.",
        ],
        "Sigma notation is compact addition. Closed forms turn a long addition into a formula in $n$, which is "
        "what you need when $n=100$ or when $n\\to\\infty$.",
        "Expand a short sigma to see what it says. Count the terms. Then apply a known closed form (odds, integers, "
        "geometric) rather than adding by hand.",
        lesson_figure(
            number_line(0, 10, closed=[(1, "1"), (3, "3"), (5, "5"), (7, "7"), (9, "9")]),
            "The terms of $\\sum_{k=1}^{5}(2k-1)$ on a number line",
            "Five odd numbers. Their sum is $25$, which is also $5^2$ — a pattern worth noticing.",
        )
        + solved(
            4, "Evaluate $\\sum_{k=1}^{4} k$.",
            ["$1+2+3+4=10$.",
             "Or $n(n+1)/2$ with $n=4$: $10$.",
             "Both routes agree."],
            "$10$", "", "Easy",
        )
        + solved(
            5, "Expand $\\sum_{k=0}^{3} 2^k$.",
            ["$k=0,1,2,3$ give $1+2+4+8$.",
             "The sum is $15$.",
             "Geometric formula: $(1-2^4)/(1-2)=15$."],
            "$1+2+4+8=15$", "", "Medium",
        )
        + solved(
            6, "Find $\\sum_{k=1}^{5}(2k-1)$ using the arithmetic series formula.",
            ["First term $1$, last term $9$, $n=5$.",
             "$s=5(1+9)/2=25$.",
             "It is also $n^2$ for the first $n$ odds."],
            "$25$", "", "Hard",
        ),
        ("Using $n$ as both the last index and the number of terms when the sum does not start at $1$",
         "$\\sum_{k=3}^{6} k$ has four terms, not six. The arithmetic formula needs the actual count $n=4$, "
         "with first $3$ and last $6$."),
        ("Expand once",
         "If a sigma looks unfamiliar, write the first three and last term. Most mistakes vanish once the sum "
         "is visible as ordinary addition."),
        [
            "I can expand a sigma and count terms.",
            "I can use $n(n+1)/2$ and the arithmetic series formula.",
            "I can sum a short geometric list with $(1-r^n)/(1-r)$.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Infinite geometric",
        [
            "An infinite geometric series $a+ar+ar^2+\\cdots$ converges (has a finite sum) precisely when $|r|<1$, "
            "in which case the sum is $S=\\dfrac{a}{1-r}$. The partial sums $s_n=a\\dfrac{1-r^n}{1-r}$ lose the "
            "$r^n$ term as $n\\to\\infty$ because $|r|^n\\to0$.",
            "If $|r|>1$, the terms grow and the series diverges. If $r=1$, you are adding $a$ forever. If $r=-1$, "
            "the partial sums oscillate and never settle on one number.",
            "The classic sum $1+1/2+1/4+\\cdots=2$ is $a=1$, $r=1/2$. A repeating decimal $0.333\\ldots$ is "
            "$0.3+0.03+0.003+\\cdots$ with $a=0.3$, $r=0.1$, summing to $1/3$. That is why every repeating decimal "
            "is rational.",
            "Negative ratios still work when $|r|<1$. $1-1/2+1/4-1/8+\\cdots=\\dfrac{1}{1-(-1/2)}=\\dfrac{2}{3}$. "
            "The terms alternate and shrink; the partial sums spiral in toward $2/3$.",
            "A bouncing-ball total distance is an infinite geometric series after the first drop: if the ball "
            "drops $10$ m and rebounds to $6$ m, $3.6$ m, … the extra up-and-down after the first drop is "
            "geometric with $r=0.6$. Do not forget the first drop is not doubled.",
            "Convergence is a limit statement: $S=\\lim_{n\\to\\infty}s_n$. The next lessons make that limit "
            "language graphical and algebraic. For this lesson, the test is the simple number $|r|$.",
        ],
        "Infinite geometric series turn repeating decimals into fractions, model total bounced distance, and "
        "are the first infinite sums you can evaluate by hand in Precalculus.",
        "Identify $a$ (first term of the infinite tail) and $r$. If $|r|<1$, compute $a/(1-r)$. If not, say the "
        "series diverges. Watch the first-drop versus rebound split in word problems.",
        lesson_figure(
            xy_graph(
                points=[(n, 2 * (1 - (0.5) ** n), f"s{n}") for n in range(1, 8)],
                dashes=[("h", 2, "S=2")],
                xlim=(0, 8), ylim=(0, 2.4), xlab="n", ylab="s_n",
            ),
            "Partial sums of $1+1/2+1/4+\\cdots$ climbing toward $2$",
            "Each new term fills half the remaining gap to the dashed line $S=2$.",
        )
        + solved(
            7, "Sum $1+1/2+1/4+1/8+\\cdots$.",
            ["$a=1$, $r=1/2$, $|r|<1$.",
             "$S=1/(1-1/2)=2$.",
             "Partial sums $1,1.5,1.75,1.875,\\ldots$ visibly approach $2$."],
            "$2$", "", "Easy",
        )
        + solved(
            8, "Why does $1+2+4+8+\\cdots$ diverge?",
            ["$r=2$, $|r|>1$.",
             "Terms grow; partial sums $s_n=2^n-1\\to\\infty$.",
             "The formula $a/(1-r)$ is illegal here."],
            "diverges ($|r|>1$)", "", "Medium",
        )
        + solved(
            9, "Write $0.333\\ldots$ as an infinite geometric series and sum it.",
            ["$0.3+0.03+0.003+\\cdots$, so $a=0.3$, $r=0.1$.",
             "$S=0.3/(1-0.1)=0.3/0.9=1/3$.",
             "Every repeating decimal is a geometric series in disguise."],
            "$1/3$", "", "Hard",
        ),
        ("Using $a/(1-r)$ when $|r|\\geq1$",
         "The formula is the remnant of $s_n$ after $r^n$ dies. If $|r|\\geq1$, that remnant never happens. "
         "Check $|r|$ before you divide."),
        ("First term of the infinite part",
         "If a ball falls $10$ then bounces $6, 3.6, \\ldots$, the infinite geometric that starts at the first "
         "ascent has $a=6$, $r=0.6$, and you still add the extra descents. Draw a timeline of up and down."),
        [
            "I can test $|r|<1$ for convergence.",
            "I can compute $S=a/(1-r)$.",
            "I can turn a repeating decimal into a geometric series.",
        ],
        11,
    )

    hole_lim = sample_curve(lambda x: (x ** 2 - 9) / (x - 3) if abs(x - 3) > 0.12 else 1e9, 0, 6, skip=(3,))
    c4 = concept_block(
        "4. Limit intuition graphically",
        [
            "The limit $\\lim_{x\\to a} f(x)=L$ means that as $x$ gets close to $a$ (from both sides, if we mean "
            "the two-sided limit), the outputs $f(x)$ get close to $L$. The function need not be defined at $a$. "
            "A hole at $(a,L)$ still has limit $L$. A filled point somewhere else at $x=a$ does not change the limit.",
            "If the left-hand height and the right-hand height disagree (a jump), the two-sided limit does not "
            "exist. If the graph shoots up or down a vertical asymptote, we say the limit is infinite, which is "
            "a way of saying it does not exist as a real number.",
            "As $x\\to\\infty$, a horizontal asymptote $y=L$ is exactly the statement $\\lim_{x\\to\\infty} f(x)=L$. "
            "The graph of $1/x$ approaches $0$; the graph of $\\dfrac{2x^2}{x^2+1}$ approaches $2$. You already "
            "met this language with rational functions in Unit 2.",
            "Sequences have limits too: $\\lim_{n\\to\\infty} a_n=L$ means the plotted terms $(n,a_n)$ eventually "
            "sit as close as you like to the height $L$. The sequence $n/(n+1)$ climbs toward $1$. The sequence "
            "$(-1)^n$ does not settle, so that limit does not exist.",
            "Graphical limit reading is a Precalculus skill that calculus will make $\\varepsilon$-$\\delta$ precise. "
            "For now, the picture is the definition: follow the graph with your finger toward the interesting "
            "x-value and see what y you are heading for.",
            "A vertical asymptote at $x=3$ for $1/(x-3)$ has left limit $-\\infty$ and right limit $+\\infty$. "
            "Those one-sided infinite limits exist as extended descriptions, but the two-sided real limit does not.",
        ],
        "Limits are how you describe holes, jumps, and asymptotes without waving your hands. They connect the "
        "rational graphs of Unit 2 to the derivatives of calculus.",
        "Ask three questions of a graph: what height do I approach from the left? from the right? as $|x|$ gets "
        "huge? If the first two disagree, there is no two-sided limit at that x.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", hole_lim)],
                points=[(3, 6, "hole, limit 6")],
                xlim=(0, 6), ylim=(2, 10),
            ),
            "$y=\\dfrac{x^2-9}{x-3}$ has a hole at $x=3$; the limit is $6$",
            "Nearby points hug the line $y=x+3$. The missing point does not stop the limit from existing.",
        )
        + solved(
            10, "If a graph has a hole at $x=1$ whose nearby y-values approach $4$, what is $\\lim_{x\\to1} f(x)$?",
            ["Limits follow the nearby points, not the missing one.",
             "The limit is $4$.",
             "$f(1)$ itself may be undefined or even equal to some other number."],
            "$4$", "", "Easy",
        )
        + solved(
            11, "A jump has left height $2$ and right height $5$. Does the two-sided limit exist?",
            ["Left and right limits disagree.",
             "The two-sided limit does not exist.",
             "One-sided limits exist separately: $2$ from the left, $5$ from the right."],
            "does not exist", "", "Medium",
        )
        + solved(
            12, "Describe $\\lim_{x\\to3^-}\\dfrac{1}{x-3}$.",
            ["From the left, $x-3$ is a small negative.",
             "The fraction is a large negative.",
             "The left-hand limit is $-\\infty$ (not a real number)."],
            "$-\\infty$", "The right-hand limit is $+\\infty$; they disagree even as infinities.", "Hard",
        ),
        ("Confusing $f(a)$ with the limit",
         "A filled dot at a different height from the hole is a classic trick. The limit is the hole’s height "
         "(what nearby points do). $f(a)$ is whatever the filled dot says, which might be different or missing."),
        ("Trace with a finger",
         "On a multiple-choice graph, cover the x-value with a finger and see what y the ink is heading for. "
         "That is the limit, even if a circle is missing or a separate dot is filled."),
        [
            "I can read a limit from a hole, a jump, or an asymptote.",
            "I can tell one-sided from two-sided limits.",
            "I can connect horizontal asymptotes to $x\\to\\infty$.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Limit algebraically (rational)",
        [
            "When a rational function is defined at $a$, the limit as $x\\to a$ is just $f(a)$ (polynomials and "
            "rationals are continuous on their domains). The interesting case is $0/0$ form: factor, cancel the "
            "common $(x-a)$, then substitute. That cancelled factor was a hole, and the limit is the hole’s y-value.",
            "Example: $\\lim_{x\\to3}\\dfrac{x^2-9}{x-3}=\\lim_{x\\to3}(x+3)=6$. You are not dividing by zero "
            "in the limit; you are simplifying for $x\\neq3$ and then approaching.",
            "At infinity, compare degrees exactly as in Unit 2. Equal degrees: ratio of leading coefficients. "
            "Denominator degree larger: $0$. Numerator degree larger: infinite (or a slant, whose limit is infinite). "
            "$\\lim_{x\\to\\infty}\\dfrac{2x^2+1}{x^2-5}=2$.",
            "Difference of square roots, such as $\\sqrt{x^2+4x}-x$ as $x\\to\\infty$, is $\\infty-\\infty$ form. "
            "Rationalize by multiplying by the conjugate. The hidden $4x$ in the numerator over two copies of $x$ "
            "produces the finite limit $2$.",
            "One-sided algebraic limits of $1/(x-2)$ are read from the sign of the denominator. From the left, "
            "negative and small; from the right, positive and small. The two-sided limit does not exist.",
            "A difference quotient $\\dfrac{(3+h)^2-9}{h}$ as $h\\to0$ is this lesson wearing a calculus costume. "
            "Expand, cancel $h$, get $6+h\\to6$. That $6$ is the slope of $y=x^2$ at $x=3$. Precalculus can "
            "compute it; calculus will name it $f'(3)$.",
        ],
        "Algebraic limits are cancelled holes and leading-term ratios. They turn Unit 2 graphing rules into "
        "numbers, and they are the computational engine of the first month of calculus.",
        "If plugging in gives a number, stop. If you get $0/0$, factor and cancel. If $x\\to\\infty$, divide by "
        "the highest power in the denominator. If $\\infty-\\infty$ with square roots, conjugate.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: (2 * x ** 2 + 1) / (x ** 2 - 5) if abs(x) > 2.3 else 1e9, -8, 8, skip=(-math.sqrt(5), math.sqrt(5))))],
                dashes=[("h", 2, "y=2")],
                xlim=(-8, 8), ylim=(-4, 8),
            ),
            "$y=\\dfrac{2x^2+1}{x^2-5}$ approaches the dashed line $y=2$",
            "Equal degrees, leading ratio $2/1$. Vertical asymptotes remain at $x=\\pm\\sqrt{5}$.",
        )
        + solved(
            13, "Evaluate $\\lim_{x\\to3}\\dfrac{x^2-9}{x-3}$.",
            ["Factor: $(x-3)(x+3)/(x-3)$.",
             "For $x\\neq3$ this is $x+3$.",
             "Approach $3$: the limit is $6$."],
            "$6$", "", "Easy",
        )
        + solved(
            14, "Evaluate $\\lim_{x\\to\\infty}\\dfrac{2x^2+1}{x^2-5}$.",
            ["Divide by $x^2$: $\\dfrac{2+1/x^2}{1-5/x^2}$.",
             "As $x\\to\\infty$ this is $2/1=2$.",
             "Equal-degree shortcut: leading over leading."],
            "$2$", "", "Medium",
        )
        + solved(
            15, "Evaluate $\\lim_{x\\to2}\\dfrac{x^3-8}{x-2}$.",
            ["$x^3-8=(x-2)(x^2+2x+4)$.",
             "Cancel: $x^2+2x+4$.",
             "At $x=2$: $4+4+4=12$."],
            "$12$", "Difference of cubes is the factoring pattern here.", "Hard",
        ),
        ("Substituting $x=a$ into a $0/0$ form and writing “undefined” as the limit",
         "Undefined at the point is why you cancel. The limit is the simplified function’s value. “Undefined” "
         "is the wrong multiple-choice bubble."),
        ("Degree comparison at infinity",
         "Glance at the highest powers. Most SAT rational limits at infinity are settled by that glance plus "
         "the leading coefficients."),
        [
            "I can cancel $0/0$ rational limits.",
            "I can evaluate rational limits at infinity from degrees.",
            "I can factor a difference of cubes for a hole.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Squeeze idea",
        [
            "The squeeze (sandwich) theorem: if $g(x)\\leq f(x)\\leq h(x)$ near $a$ (except possibly at $a$) and "
            "$\\lim_{x\\to a} g(x)=\\lim_{x\\to a} h(x)=L$, then $\\lim_{x\\to a} f(x)=L$. The middle function is "
            "trapped and has no choice but to go to $L$.",
            "The standard Precalculus example is $x\\sin(1/x)$ as $x\\to0$. Because $|\\sin|\\leq1$, you have "
            "$-|x|\\leq x\\sin(1/x)\\leq|x|$. Both bounds go to $0$, so the middle does too, even though $\\sin(1/x)$ "
            "oscillates wildly.",
            "A bound that does not squeeze fails. $-1\\leq\\sin x\\leq1$ is true, but $\\pm1$ do not both approach "
            "$0$ as $x\\to\\infty$, so you cannot conclude $\\sin x\\to0$. The bounding functions must share the same limit.",
            "Geometric series remainder estimates are squeeze in disguise: the leftover $r^n$ is trapped between "
            "$0$ and something going to $0$ when $|r|<1$. Comparison of series (a stretch item) is squeeze on "
            "partial sums: $0\\leq s_n^{(a)}\\leq s_n^{(b)}\\to S$ implies the smaller series converges.",
            "The famous $\\lim_{x\\to0}\\dfrac{\\sin x}{x}=1$ is proved in calculus by squeezing a geometric picture "
            "of a sector. In Precalculus you may use the result: $\\dfrac{\\sin(3x)}{x}=3\\cdot\\dfrac{\\sin(3x)}{3x}\\to3$.",
            "When a function oscillates inside a shrinking envelope, think squeeze. When it oscillates inside a "
            "fixed envelope, the limit usually does not exist. Draw the envelope — two parabolas, two lines "
            "$y=\\pm|x|$, or two constants — and ask whether those envelopes meet.",
        ],
        "Squeeze is the tool for limits you cannot cancel algebraically because of an oscillation. It is also "
        "the honesty check on a false argument that “bounded implies limit $0$.”",
        "Write a true inequality $g\\leq f\\leq h$ whose sides have obvious limits. If those limits match, you "
        "are done. If they do not match, squeeze does not apply (yet).",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#16a34a", sample_curve(lambda x: abs(x), -1.2, 1.2)),
                    ("#16a34a", sample_curve(lambda x: -abs(x), -1.2, 1.2)),
                    ("#4f46e5", sample_curve(
                        lambda x: x * math.sin(1 / x) if abs(x) > 0.03 else 0, -1.2, 1.2, skip=(0,)
                    )),
                ],
                xlim=(-1.4, 1.4), ylim=(-1.4, 1.4),
            ),
            "$y=\\pm|x|$ squeezing $y=x\\sin(1/x)$ toward $0$",
            "The wild blue oscillation is trapped in a V that pinches at the origin, so the limit is $0$.",
        )
        + solved(
            16, "If $g\\leq f\\leq h$ near $a$ and both $g$ and $h$ have limit $L$, what is $\\lim f$?",
            ["Squeeze theorem: the limit is $L$.",
             "The middle function cannot escape the closing gap.",
             "This requires the inequality near $a$, not necessarily at $a$."],
            "$L$", "", "Easy",
        )
        + solved(
            17, "Explain why $-1\\leq\\sin x\\leq1$ does not prove $\\sin x\\to0$ as $x\\to\\infty$.",
            ["The bounds are the constants $-1$ and $1$.",
             "Those constants do not share a limit of $0$; they do not even go to $0$.",
             "Squeeze needs matching limits of the bounds."],
            "bounds do not both tend to $0$", "", "Medium",
        )
        + solved(
            18, "Evaluate $\\lim_{x\\to0} x\\sin(1/x)$.",
            ["$|\\sin(1/x)|\\leq1$, so $|x\\sin(1/x)|\\leq|x|$.",
             "$-|x|\\leq x\\sin(1/x)\\leq|x|$.",
             "Both $\\pm|x|\\to0$, hence the middle $\\to0$."],
            "$0$", "The inner oscillation is real; the envelope dies.", "Hard",
        ),
        ("Claiming a bounded oscillation has limit $0$",
         "$\\sin x$ is bounded and does not tend to $0$. Boundedness is not enough; the envelope must shrink "
         "to a single height."),
        ("Write the inequality first",
         "On a squeeze problem, the first sentence of the solution should be the inequality, with a reason "
         "($|\\sin|\\leq1$, or a geometric picture). Then take limits of the sides."),
        [
            "I can state the squeeze theorem.",
            "I can squeeze $x\\sin(1/x)$ to $0$.",
            "I know why a fixed bound does not force a limit of $0$.",
        ],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title, AUDIENCE, concepts, body, practice_slots(31, 25, STRETCH_LABEL),
    )
    return title, description, content, _u7_questions()


# ===========================================================================
# UNIT 8: Vectors, Parametric & Matrices
# ===========================================================================

def _u8_questions():
    qs = []
    _add(qs, [
        ("The vector $\\langle 3,1\\rangle+\\langle -1,4\\rangle$ equals:",
         "<2,5>",
         "Add components: $3-1=2$, $1+4=5$.",
         ["<4,5>", "<2,3>", "<3,4>"]),
        ("$3\\langle 2,-1\\rangle$ equals:",
         "<6,-3>",
         "Scalar multiplication stretches each component.",
         ["<5,2>", "<2,-3>", "<6,-1>"]),
        ("The magnitude of $\\langle 3,4\\rangle$ is:",
         5,
         "$\\sqrt{9+16}=5$.",
         ["7", "12", "1"]),
        ("A unit vector in the direction of $\\langle 0,5\\rangle$ is:",
         "<0,1>",
         "Divide by the length $5$: $\\langle 0,1\\rangle$.",
         ["<0,5>", "<1,0>", "<0,1/5>"]),
        ("The zero vector $\\langle 0,0\\rangle$ has magnitude:",
         0,
         "It is the only vector with no direction.",
         ["1", "undefined", "2"]),
        ("$\\langle 2,3\\rangle\\cdot\\langle 4,-1\\rangle$ equals:",
         5,
         "$2\\cdot4+3\\cdot(-1)=8-3=5$.",
         ["8", "-3", "11"]),
        ("Two nonzero vectors are perpendicular when their dot product is:",
         0,
         "The cosine of the angle is zero iff the angle is $90^\\circ$.",
         ["1", "their magnitudes' product", "negative"]),
        ("$\\cos\\theta$ for the angle between $\\mathbf{u},\\mathbf{v}$ is:",
         "(u·v)/(|u||v|)",
         "The geometric definition of the dot product.",
         ["|u||v|", "u·v only", "|u+v|"]),
        ("$\\langle 1,0\\rangle\\cdot\\langle 0,1\\rangle$ equals:",
         0,
         "The standard basis vectors of the plane are orthogonal.",
         ["1", "-1", "2"]),
        ("If $\\mathbf{u}\\cdot\\mathbf{v}<0$, the angle between them is:",
         "obtuse",
         "Negative cosine means $\\theta>90^\\circ$ (and less than $180^\\circ$ for the vector angle).",
         ["acute", "right", "zero"]),
        ("The parametric pair $x=1+2t$, $y=3+t$ passes through $(1,3)$ at $t=$:",
         0,
         "The constant terms are the position at $t=0$.",
         ["1", "2", "-1"]),
        ("The direction vector of $x=1+2t$, $y=3+t$ is:",
         "<2,1>",
         "The coefficients of $t$ are the direction.",
         ["<1,3>", "<2,3>", "<1,1>"]),
        ("$x=\\cos t$, $y=\\sin t$ traces:",
         "the unit circle",
         "$x^2+y^2=1$, traversed counterclockwise from $(1,0)$.",
         ["a line", "a parabola", "the origin only"]),
        ("$x=t$, $y=t^2$ traces:",
         "the parabola y=x^2",
         "Eliminate $t$: $y=x^2$.",
         ["a circle", "x=y^2", "a hyperbola"]),
        ("A parametric speed is large when the direction vector is:",
         "long (large |<dx/dt, dy/dt>|)",
         "The particle covers more arc per unit time.",
         ["the origin", "t=0 always", "a unit circle only"]),
        ("Eliminate $t$ from $x=2t$, $y=4t+1$ to get:",
         "y=2x+1",
         "$t=x/2$, so $y=4(x/2)+1=2x+1$.",
         ["y=x/2", "x=2y", "y=4x"]),
        ("From $x=\\cos t$, $y=\\sin t$, eliminating $t$ yields:",
         "x^2+y^2=1",
         "Pythagorean identity.",
         ["y=x", "x+y=1", "y=x^2"]),
        ("$x=t^2$, $y=t$ eliminates to:",
         "x=y^2",
         "The graph is a sideways parabola, traversed up then... as $t$ runs through $\\mathbb{R}$, $y$ covers all reals.",
         ["y=x^2", "a circle", "x=y"]),
        ("Parametric $x=3+2\\cos t$, $y=-1+2\\sin t$ is a circle of radius:",
         2,
         "Center $(3,-1)$, radius $2$.",
         ["3", "1", "4"]),
        ("Eliminating $t$ loses:",
         "the timing and direction of travel",
         "The rectangular graph is the path, not the movie.",
         ["the path entirely", "the center", "x and y"]),
        ("The determinant of $\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}$ is:",
         -2,
         "$ad-bc=4-6=-2$.",
         ["8", "2", "7"]),
        ("A $2\\times2$ matrix is invertible iff its determinant is:",
         "nonzero",
         "Otherwise the columns are parallel and the linear map collapses a direction.",
         ["1", "positive", "equal to the trace"]),
        ("The inverse of $\\begin{pmatrix}a&b\\\\c&d\\end{pmatrix}$ is $\\dfrac{1}{ad-bc}$ times:",
         "[[d,-b],[-c,a]]",
         "Swap the diagonal, negate the off-diagonal.",
         ["[[a,b],[c,d]]", "[[d,b],[c,a]]", "the zero matrix"]),
        ("$\\begin{pmatrix}2&0\\\\0&3\\end{pmatrix}$ sends $\\langle 1,1\\rangle$ to:",
         "<2,3>",
         "A diagonal matrix scales the axes independently.",
         ["<1,1>", "<3,2>", "<0,0>"]),
        ("If $\\det A=0$, the linear map $A$ is:",
         "not invertible (collapses area to 0)",
         "Images of the plane lie on a line (or a point).",
         ["a rotation", "the identity", "always a reflection"]),
        ("The system $x+2y=5$, $3x+4y=11$ in matrix form is $A\\mathbf{x}=\\mathbf{b}$ with $\\mathbf{b}=$:",
         "<5,11>",
         "The constants on the right-hand side.",
         ["<1,3>", "<2,4>", "<5,4>"]),
        ("If $A^{-1}$ exists, the solution of $A\\mathbf{x}=\\mathbf{b}$ is:",
         "x = A^{-1} b",
         "Multiply both sides on the left by the inverse.",
         ["x = A b", "x = b A", "x = det A"]),
        ("Cramer's rule for $2\\times2$ uses determinants of matrices that replace a column by:",
         "the constant vector b",
         "$x=\\det(A_x)/\\det A$, $y=\\det(A_y)/\\det A$.",
         ["the zero vector", "a row of 1s", "A inverse"]),
        ("A unique solution of a $2\\times2$ linear system exists when:",
         "det A \u2260 0",
         "The two lines are not parallel.",
         ["det A = 0", "b = 0", "A is zero"]),
        ("$I_2\\mathbf{v}=\\mathbf{v}$ for every $\\mathbf{v}$ because $I_2$ is:",
         "the 2x2 identity",
         "Ones on the diagonal, zeros off it.",
         ["the zero matrix", "a rotation by 90°", "singular"]),
        ("$\\|\\langle 5,12\\rangle\\|$ equals:",
         13,
         "A $5$-$12$-$13$ triple.",
         ["17", "60", "7"]),
        ("$\\langle 1,2\\rangle-\\langle 4,0\\rangle$ equals:",
         "<-3,2>",
         "Subtract components.",
         ["<5,2>", "<3,-2>", "<-3,-2>"]),
        ("Dot product of a vector with itself is:",
         "the square of its magnitude",
         "$\\mathbf{u}\\cdot\\mathbf{u}=|\\mathbf{u}|^2$.",
         ["0", "1 always", "the magnitude"]),
        ("$x=2\\cos t$, $y=3\\sin t$ is an:",
         "ellipse x^2/4 + y^2/9 = 1",
         "Divide: $\\cos t=x/2$, $\\sin t=y/3$, square-add.",
         ["circle r=2", "line", "hyperbola"]),
        ("The angle between $\\langle 1,1\\rangle$ and $\\langle 1,0\\rangle$ has $\\cos\\theta=$:",
         "1/\\sqrt{2}",
         "$\\mathbf{u}\\cdot\\mathbf{v}=1$, magnitudes $\\sqrt{2}$ and $1$.",
         ["1", "0", "\\sqrt{2}"]),
        ("Matrix $\\begin{pmatrix}0&-1\\\\1&0\\end{pmatrix}$ rotates the plane by:",
         "90° counterclockwise",
         "It sends $\\langle 1,0\\rangle$ to $\\langle 0,1\\rangle$.",
         ["90° clockwise", "180°", "0°"]),
        ("If two direction vectors of parametric lines are scalar multiples, the lines are:",
         "parallel (or the same line)",
         "Same direction.",
         ["perpendicular", "always intersecting", "circles"]),
        ("$\\det\\begin{pmatrix}2&1\\\\4&2\\end{pmatrix}=$:",
         0,
         "$4-4=0$; rows are dependent, no inverse.",
         ["4", "8", "-2"]),
        ("Parametric $x=t$, $y=1/t$ ($t\\neq0$) eliminates to:",
         "xy=1",
         "A rectangular hyperbola.",
         ["y=x", "x^2+y^2=1", "y=t"]),
        ("The projection idea: $\\mathbf{u}\\cdot\\hat{\\mathbf{v}}$ is the:",
         "scalar component of u along v",
         "Dot with a unit vector extracts that component.",
         ["cross product", "area", "determinant"]),
        ("Adding $\\langle 1,0\\rangle$ and $\\langle 0,2\\rangle$ as a parallelogram's diagonal gives:",
         "<1,2>",
         "Vector addition is the parallelogram law.",
         ["<1,0>", "<0,2>", "<0,0>"]),
        ("$A=\\begin{pmatrix}1&1\\\\0&1\\end{pmatrix}$ is a shear. $\\det A=$:",
         1,
         "Area is preserved; the map is invertible.",
         ["0", "2", "-1"]),
        ("The system $2x+y=1$, $4x+2y=2$ has:",
         "infinitely many solutions",
         "The second equation is a double of the first; $\\det A=0$ and $\\mathbf{b}$ is consistent.",
         ["no solution", "a unique solution", "x=1,y=1 only"]),
        ("$x=4-t$, $y=t$ eliminates to:",
         "x+y=4",
         "A line of intercepts $4$ and $4$.",
         ["xy=4", "y=4x", "x-y=4"]),
        ("A vector of length $1$ along $\\langle 3,4\\rangle$ is:",
         "<3/5,4/5>",
         "Divide by $5$.",
         ["<3,4>", "<1,1>", "<5,5>"]),
        ("SAT Stretch: The linear map $A=\\begin{pmatrix}2&1\\\\0&2\\end{pmatrix}$ stretches area by $\\det A=$:",
         4,
         "A shear-scale: area scale factor is $|\\det A|=4$. The inverse map scales area by $1/4$.",
         ["2", "0", "1"]),
        ("SAT Stretch: Inverse of $A=\\begin{pmatrix}2&1\\\\0&2\\end{pmatrix}$, as a matrix, is $\\dfrac{1}{4}$ times:",
         "[[2,-1],[0,2]]",
         "$\\mathrm{adj}=\\begin{pmatrix}2&-1\\\\0&2\\end{pmatrix}$, divide by $\\det=4$. Check: $A A^{-1}=I$.",
         ["[[2,1],[0,2]]", "[[1,0],[0,1]]", "[[2,0],[-1,2]]"]),
        ("SAT Stretch: If $A$ sends $\\mathbf{e}_1$ to $\\langle 2,0\\rangle$ and $\\mathbf{e}_2$ to $\\langle 1,2\\rangle$, then $A^{-1}$ sends $\\langle 2,0\\rangle$ to:",
         "<1,0>",
         "The inverse undoes the map: $A^{-1}(A\\mathbf{e}_1)=\\mathbf{e}_1=\\langle 1,0\\rangle$.",
         ["<2,0>", "<0,1>", "<1,2>"]),
        ("SAT Stretch: Parametric $x=t+1/t$, $y=t-1/t$ ($t\\neq0$) satisfies:",
         "x^2-y^2=4",
         "$(t+1/t)^2-(t-1/t)^2=4$. A hyperbola.",
         ["x^2+y^2=4", "xy=1", "y=x"]),
        ("SAT Stretch: Vectors $\\langle 1,2\\rangle$ and $\\langle k,4\\rangle$ are parallel when $k=$:",
         2,
         "Need $\\langle k,4\\rangle=c\\langle 1,2\\rangle$, so $4=2c$ and $k=c$, hence $k=2$. "
         "Equivalently the determinant $1\\cdot4-2k=0$.",
         ["4", "1", "0"]),
        ("SAT Stretch: The cosine of the angle between $\\langle 3,4\\rangle$ and $\\langle -5,12\\rangle$ equals:",
         "33/65",
         "Dot product $3(-5)+4(12)=-15+48=33$. Magnitudes $5$ and $13$, so $\\cos\\theta=33/65$.",
         ["-33/65", "63/65", "33/16"]),
        ("SAT Stretch: Solve $\\begin{pmatrix}1&2\\\\3&5\\end{pmatrix}\\begin{pmatrix}x\\\\y\\end{pmatrix}=\\begin{pmatrix}1\\\\1\\end{pmatrix}$.",
         "x=-3, y=2",
         "$x+2y=1$ and $3x+5y=1$. Triple the first and subtract: $y=2$, then $x+4=1$, so $x=-3$. "
         "Check: $3(-3)+5(2)=-9+10=1$.",
         ["x=1, y=0", "x=2, y=-1/2", "no solution"]),
        ("SAT Stretch: A particle $x=2t$, $y=t^2$ has speed at $t=1$ equal to:",
         "\\sqrt{8}",
         "Velocity $\\langle 2,2t\\rangle$, at $t=1$ length $\\sqrt{4+4}=\\sqrt{8}=2\\sqrt{2}$.",
         ["2", "1", "\\sqrt{2}"]),
        ("SAT Stretch: $A=\\begin{pmatrix}\\cos\\theta&-\\sin\\theta\\\\\\sin\\theta&\\cos\\theta\\end{pmatrix}$ has inverse:",
         "A^T (rotation by -\u03b8)",
         "Rotation matrices are orthogonal: $A^{-1}=A^T=A(-\\theta)$.",
         ["-A", "A itself for all \u03b8", "the zero matrix"]),
        ("SAT Stretch: The linear map $\\langle x,y\\rangle\\mapsto\\langle x+2y,\\,3x+4y\\rangle$ has inverse scale factor for area equal to:",
         "-1/2",
         "$\\det=4-6=-2$, so area is scaled by $2$ and flipped. The inverse scales area by $1/(-2)=-1/2$.",
         ["-2", "0", "1"]),
    ])
    return qs[:55]


def build_unit8():
    title = "Precalculus Unit 8: Vectors, Parametric & Matrices"
    description = (
        "Vector operations, dot product and angle, parametric equations, eliminating the parameter, "
        "2x2 matrices and inverses, and linear systems — with arrows from the origin and path graphs."
    )
    concepts = [
        "Vector operations",
        "Dot product and angle",
        "Parametric equations",
        "Eliminate the parameter",
        "2x2 matrices and inverses",
        "Systems via matrices",
    ]

    c1 = concept_block(
        "1. Vector operations",
        [
            "A vector $\\langle u_1,u_2\\rangle$ is an arrow: magnitude and direction, free to slide (in this "
            "course we often draw it from the origin). Addition is componentwise and matches the parallelogram "
            "(or tip-to-tail) law. Scalar multiplication $c\\mathbf{u}$ stretches ($|c|>1$), shrinks ($|c|<1$), "
            "or reverses ($c<0$) the arrow.",
            "Magnitude $|\\mathbf{u}|=\\sqrt{u_1^2+u_2^2}$ is the Pythagorean length. A unit vector is a vector "
            "of length $1$; $\\hat{\\mathbf{u}}=\\mathbf{u}/|\\mathbf{u}|$ points the same way as $\\mathbf{u}$ "
            "(when $\\mathbf{u}\\neq\\mathbf{0}$). The zero vector has length $0$ and no direction.",
            "Subtraction $\\mathbf{u}-\\mathbf{v}$ is the arrow from the tip of $\\mathbf{v}$ to the tip of "
            "$\\mathbf{u}$ when both are drawn from the same point. In components it is still componentwise. "
            "Displacement from $A$ to $B$ is $\\overrightarrow{AB}=\\langle x_B-x_A, y_B-y_A\\rangle$.",
            "Graphically, two arrows from the origin make the picture this lesson needs: $\\langle 3,1\\rangle$ "
            "and $\\langle -1,4\\rangle$, and their sum $\\langle 2,5\\rangle$ as the parallelogram diagonal. "
            "Never replace that picture with a lone origin dot.",
            "Vectors add forces, velocities, and displacements. A plane’s velocity relative to the ground is "
            "the vector sum of airspeed and wind. That application is ordinary component addition once you "
            "draw the arrows.",
            "Later in the unit, a $2\\times2$ matrix will eat a vector and spit out another vector — a linear "
            "map. Getting comfortable with $\\langle x,y\\rangle$ as a column now makes that multiplication "
            "look like a natural extension of scalar stretch.",
        ],
        "Vectors are the language of motion and of linear maps. Addition, scalar multiplication, and magnitude "
        "are the three operations you must do without hesitation.",
        "Work in components for computation; draw arrows from the origin for meaning. Magnitude is always a "
        "square root of a sum of squares, never a sum of the components.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#4f46e5", [(0, 0), (3, 1)]),
                    ("#dc2626", [(0, 0), (-1, 4)]),
                    ("#16a34a", [(0, 0), (2, 5)]),
                ],
                points=[(3, 1, "u"), (-1, 4, "v"), (2, 5, "u+v")],
                xlim=(-3, 6), ylim=(-1, 6),
            ),
            "Arrows from the origin: $\\mathbf{u}=\\langle 3,1\\rangle$, $\\mathbf{v}=\\langle -1,4\\rangle$, and $\\mathbf{u}+\\mathbf{v}$",
            "The green diagonal of the parallelogram is the sum $\\langle 2,5\\rangle$.",
        )
        + solved(
            1, "Add $\\langle 3,1\\rangle+\\langle -1,4\\rangle$.",
            ["Add x-components: $3+(-1)=2$.",
             "Add y-components: $1+4=5$.",
             "The sum is $\\langle 2,5\\rangle$."],
            "$\\langle 2,5\\rangle$", "", "Easy",
        )
        + solved(
            2, "Find $|\\langle 3,4\\rangle|$.",
            ["$\\sqrt{3^2+4^2}=\\sqrt{25}=5$.",
             "A $3$-$4$-$5$ right triangle.",
             "The unit vector is $\\langle 3/5,4/5\\rangle$."],
            "$5$", "", "Medium",
        )
        + solved(
            3, "Find a unit vector in the direction of $\\langle 0,5\\rangle$.",
            ["Length is $5$.",
             "Divide: $\\langle 0,5\\rangle/5=\\langle 0,1\\rangle$.",
             "It points straight up, length $1$."],
            "$\\langle 0,1\\rangle$", "", "Hard",
        ),
        ("Adding magnitudes instead of adding components",
         "$|\\mathbf{u}|+|\\mathbf{v}|$ is larger than $|\\mathbf{u}+\\mathbf{v}|$ unless the vectors are parallel "
         "and in the same direction. The triangle inequality is that fact. Always add components, then take magnitude."),
        ("Draw both arrows from the origin",
         "On a test sketch, put tails at $(0,0)$ unless the problem is about a displacement between two points. "
         "The parallelogram then sits in a standard place."),
        [
            "I can add and scalar-multiply in components.",
            "I can compute magnitude and a unit vector.",
            "I can draw two arrows from the origin and their sum.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Dot product and angle",
        [
            "The dot product $\\mathbf{u}\\cdot\\mathbf{v}=u_1 v_1+u_2 v_2$ is a number. Geometrically, "
            "$\\mathbf{u}\\cdot\\mathbf{v}=|\\mathbf{u}||\\mathbf{v}|\\cos\\theta$, so "
            "$\\cos\\theta=\\dfrac{\\mathbf{u}\\cdot\\mathbf{v}}{|\\mathbf{u}||\\mathbf{v}|}$. That formula is "
            "how you find the angle between two arrows.",
            "Perpendicular vectors (nonzero) have dot product $0$, because $\\cos 90^\\circ=0$. Parallel vectors "
            "have $|\\mathbf{u}\\cdot\\mathbf{v}|=|\\mathbf{u}||\\mathbf{v}|$. A negative dot product means an "
            "obtuse angle. These sign checks are faster than computing $\\theta$ when a question only asks acute/right/obtuse.",
            "The identity $\\mathbf{u}\\cdot\\mathbf{u}=|\\mathbf{u}|^2$ recovers magnitude. The projection of "
            "$\\mathbf{u}$ onto a unit vector $\\hat{\\mathbf{v}}$ is the scalar $\\mathbf{u}\\cdot\\hat{\\mathbf{v}}$, "
            "the signed length of the shadow of $\\mathbf{u}$ along $\\mathbf{v}$.",
            "Algebraically, dot product is commutative and distributive. It is not associative in the vector sense "
            "(the output is a scalar, so $(\\mathbf{u}\\cdot\\mathbf{v})\\cdot\\mathbf{w}$ does not make sense as "
            "three vectors dotted). Work left to right: first the number, then maybe a scalar times a vector.",
            "The standard basis $\\mathbf{i}=\\langle 1,0\\rangle$ and $\\mathbf{j}=\\langle 0,1\\rangle$ are "
            "orthonormal: length $1$ and dot product $0$. Any $\\langle a,b\\rangle=a\\mathbf{i}+b\\mathbf{j}$.",
            "In Unit 5, the modulus of a complex number was a vector length, and the argument was a vector angle. "
            "Dot product is the real-plane version of “how aligned are these two directions?”",
        ],
        "The angle between two directions — forces, headings, or columns of a matrix — is a dot product question. "
        "Orthogonality is the special case $\\mathbf{u}\\cdot\\mathbf{v}=0$.",
        "Compute the four numbers $u_1,u_2,v_1,v_2$, form the dot product, divide by the product of magnitudes, "
        "and take $\\arccos$ if you need $\\theta$. For a yes/no perpendicular question, stop at whether the dot is $0$.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#4f46e5", [(0, 0), (2, 3)]),
                    ("#dc2626", [(0, 0), (4, -1)]),
                ],
                points=[(2, 3, "u"), (4, -1, "v")],
                xlim=(-1, 6), ylim=(-3, 5),
            ),
            "Angle between $\\langle 2,3\\rangle$ and $\\langle 4,-1\\rangle$ via the dot product",
            "$\\mathbf{u}\\cdot\\mathbf{v}=8-3=5>0$, so the angle is acute. The arrows share a tail at the origin.",
        )
        + solved(
            4, "Compute $\\langle 2,3\\rangle\\cdot\\langle 4,-1\\rangle$.",
            ["$2\\cdot4+3\\cdot(-1)=8-3=5$.",
             "Positive, so the angle is acute.",
             "Not perpendicular."],
            "$5$", "", "Easy",
        )
        + solved(
            5, "Are $\\langle 1,0\\rangle$ and $\\langle 0,1\\rangle$ perpendicular?",
            ["Dot product $0$.",
             "Yes: they are the coordinate axes.",
             "Each has length $1$ as well (orthonormal)."],
            "yes", "", "Medium",
        )
        + solved(
            6, "Find $\\cos\\theta$ for the angle between $\\langle 1,1\\rangle$ and $\\langle 1,0\\rangle$.",
            ["Dot product $1$.",
             "Magnitudes $\\sqrt{2}$ and $1$.",
             "$\\cos\\theta=1/\\sqrt{2}$, so $\\theta=\\pi/4$."],
            "$1/\\sqrt{2}$", "", "Hard",
        ),
        ("Using $\\mathbf{u}\\cdot\\mathbf{v}=|\\mathbf{u}||\\mathbf{v}|$ without the cosine",
         "That equality holds only when $\\theta=0$. The general formula includes $\\cos\\theta$. Dropping cosine "
         "is how people “prove” every pair of vectors is parallel."),
        ("Sign of the dot product",
         "Before computing an inverse cosine, look at the sign. Negative means obtuse — a multiple-choice trap "
         "is the supplementary angle or a calculator in degree mode mixing with radians."),
        [
            "I can compute a dot product in components.",
            "I can test perpendicularity.",
            "I can find $\\cos\\theta$ between two vectors.",
        ],
        6,
    )

    circ_par = _ellipse(1, 1)
    c3 = concept_block(
        "3. Parametric equations",
        [
            "A parametric description of a plane curve gives $x$ and $y$ as functions of a third variable $t$ "
            "(often time): $x=x(t)$, $y=y(t)$. As $t$ runs through an interval, the point $(x(t),y(t))$ traces "
            "a path. The same geometric curve can be traced at different speeds or in reverse by changing the "
            "parametrization.",
            "A line through $(x_0,y_0)$ with direction $\\langle a,b\\rangle$ is $x=x_0+at$, $y=y_0+bt$. At $t=0$ "
            "you are at the given point; the direction vector is the pair of coefficients of $t$. This is the "
            "vector equation $\\mathbf{r}(t)=\\mathbf{r}_0+t\\mathbf{d}$ written in components.",
            "Circles: $x=h+r\\cos t$, $y=k+r\\sin t$ traces a circle of radius $r$ about $(h,k)$, counterclockwise "
            "from the rightmost point if $t$ starts at $0$ and increases. Ellipses replace $r$ by $a$ and $b$. "
            "The unit circle $x=\\cos t$, $y=\\sin t$ is the parent.",
            "Parabolas: $x=t$, $y=t^2$ is $y=x^2$ traversed left-to-right as $t$ increases. $x=t^2$, $y=t$ is "
            "the sideways parabola $x=y^2$. Timing matters: you cannot see $t$ on the static graph, but you can "
            "see it in a table of values.",
            "Velocity in the plane is the vector $\\langle x'(t), y'(t)\\rangle$ (once calculus provides derivatives). "
            "In Precalculus you can still say: a large coefficient of $t$ means a fast line; $t$ in a cosine with "
            "a large $B$ means a fast trip around a circle.",
            "Parametric equations are how projectiles, Ferris wheels (Unit 4), and later space curves are written. "
            "The next lesson eliminates $t$ to recover a rectangular relation — the path without the movie.",
        ],
        "Parametric form is a path plus a clock. Physics problems, circular motion, and computer graphics all "
        "use $(x(t),y(t))$ rather than $y$ as a function of $x$ (which cannot describe a full circle as a single $f(x)$).",
        "Read the point at $t=0$, read the direction or the radius from the formulas, then sketch a few more $t$ "
        "values to see the orientation (clockwise versus counterclockwise, left-to-right versus out-and-back).",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", circ_par)],
                points=[(1, 0, "t=0"), (0, 1, "t=\u03c0/2")],
                xlim=(-2, 2), ylim=(-2, 2),
            ),
            "Parametric unit circle $x=\\cos t$, $y=\\sin t$",
            "At $t=0$ the particle is at $(1,0)$; at $t=\\pi/2$ it is at $(0,1)$, traveling counterclockwise.",
        )
        + solved(
            7, "Where is $x=1+2t$, $y=3+t$ when $t=0$, and what is the direction vector?",
            ["$t=0$ gives $(1,3)$.",
             "Direction $\\langle 2,1\\rangle$.",
             "The path is the line through $(1,3)$ with that slope $1/2$."],
            "$(1,3)$, direction $\\langle 2,1\\rangle$", "", "Easy",
        )
        + solved(
            8, "What curve is $x=\\cos t$, $y=\\sin t$?",
            ["$x^2+y^2=\\cos^2 t+\\sin^2 t=1$.",
             "The unit circle, starting at $(1,0)$, counterclockwise.",
             "It is not a function $y=f(x)$ on the whole circle."],
            "unit circle", "", "Medium",
        )
        + solved(
            9, "Identify $x=3+2\\cos t$, $y=-1+2\\sin t$.",
            ["Center $(3,-1)$, radius $2$.",
             "A circle: $(x-3)^2+(y+1)^2=4$.",
             "Traversed counterclockwise from $(5,-1)$."],
            "circle center $(3,-1)$, radius $2$", "", "Hard",
        ),
        ("Thinking a circle cannot be parametric because $y$ is not a function of $x$",
         "That is why we use a parameter. $y=f(x)$ fails the vertical line test on a full circle; $(x(t),y(t))$ "
         "does not care. Parametric form is more flexible than $y=f(x)$."),
        ("Point at $t=0$ first",
         "Most matching questions are settled by where the particle is at $t=0$ and which way it moves for small "
         "positive $t$. Compute those two facts before you eliminate $t$."),
        [
            "I can read a line’s point and direction from $x=x_0+at$, $y=y_0+bt$.",
            "I can recognize a parametric circle or ellipse.",
            "I can interpret $t$ as time along a path.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Eliminate the parameter",
        [
            "Eliminating $t$ means producing a rectangular equation $F(x,y)=0$ (or $y=f(x)$) that the moving "
            "point satisfies. The path is recovered; the timing is lost. A particle that goes back and forth "
            "on a segment still eliminates to the line containing that segment.",
            "For a line, solve one equation for $t$ and substitute. $x=2t$, $y=4t+1$ gives $t=x/2$, hence "
            "$y=2x+1$. For a circle or ellipse, use $\\cos^2+\\sin^2=1$. For $x=t$, $y=t^2$, just replace: $y=x^2$.",
            "Sometimes you need a Pythagorean or a hyperbolic identity. $x=t+1/t$, $y=t-1/t$ satisfies "
            "$x^2-y^2=4$, a hyperbola — a stretch calculation. $x=t$, $y=1/t$ is $xy=1$.",
            "Domain restrictions survive. If $t\\geq0$ in $x=t$, $y=t^2$, you only get the right half of the "
            "parabola in the sense that $x\\geq0$. If $t$ is an angle in $[0,\\pi]$, you may get only a semicircle. "
            "State the remaining restriction on $x$ or $y$ when it matters.",
            "Eliminating $t$ is the inverse of parametrizing. In Unit 1, inverse functions undid $f$. Here you "
            "undo the clock to reveal the set of points. Both are “forget some structure to see a simpler object.”",
            "A test trap is claiming two parametrizations that trace the same ellipse in opposite directions are "
            "“different curves.” After eliminating $t$, they look identical. The difference is orientation, which "
            "the rectangular equation cannot see.",
        ],
        "Eliminating the parameter is how you recognize “this movie is secretly an ellipse” and how you graph "
        "a parametric equation on paper without a table of twenty $t$-values.",
        "Solve for $t$ if it appears linearly. Use $\\cos^2+\\sin^2=1$ if $t$ is an angle in a circle/ellipse. "
        "Then note any leftover restriction ($x\\geq0$, $t\\neq0$, a half-interval of angles).",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: x ** 2, -2.5, 2.5))],
                points=[(-1, 1, "t=-1"), (0, 0, "t=0"), (2, 4, "t=2")],
                xlim=(-3, 3), ylim=(-1, 7),
            ),
            "Eliminating $t$ from $x=t$, $y=t^2$ yields the parabola $y=x^2$",
            "Marked times show left-to-right travel. The static curve does not remember $t$.",
        )
        + solved(
            10, "Eliminate $t$ from $x=2t$, $y=4t+1$.",
            ["$t=x/2$.",
             "$y=4(x/2)+1=2x+1$.",
             "The path is the line $y=2x+1$."],
            "$y=2x+1$", "", "Easy",
        )
        + solved(
            11, "Eliminate $t$ from $x=\\cos t$, $y=\\sin t$.",
            ["Square and add: $x^2+y^2=1$.",
             "The path is the unit circle.",
             "If $t\\in[0,\\pi]$ only, you would have the upper semicircle plus endpoints."],
            "$x^2+y^2=1$", "", "Medium",
        )
        + solved(
            12, "Eliminate $t$ from $x=2\\cos t$, $y=3\\sin t$.",
            ["$\\cos t=x/2$, $\\sin t=y/3$.",
             "$\\dfrac{x^2}{4}+\\dfrac{y^2}{9}=1$.",
             "An ellipse centered at the origin, horizontal semi-axis $2$, vertical $3$."],
            "$\\dfrac{x^2}{4}+\\dfrac{y^2}{9}=1$", "", "Hard",
        ),
        ("Forgetting the domain of $t$",
         "If $x=t^2$, $y=t$, then $x=y^2$ with $x\\geq0$ automatically, and $y$ covers all reals as $t$ does. "
         "If a problem restricts $t\\geq0$, then $y\\geq0$ as well. Report the restriction when it cuts the graph."),
        ("Path versus motion",
         "After eliminating, say “the path is …” not “the particle is at rest on …”. Two different movies can "
         "share a path."),
        [
            "I can eliminate $t$ from a linear parametrization.",
            "I can recover $x^2/a^2+y^2/b^2=1$ from cosine/sine.",
            "I can note leftover domain restrictions.",
        ],
        16,
    )

    c5 = concept_block(
        "5. 2x2 matrices and inverses",
        [
            "A $2\\times2$ matrix $A=\\begin{pmatrix}a&b\\\\c&d\\end{pmatrix}$ is a linear map of the plane: it "
            "sends the vector $\\langle x,y\\rangle$ to $\\langle ax+by, cx+dy\\rangle$. The first column is the "
            "image of $\\langle 1,0\\rangle$; the second column is the image of $\\langle 0,1\\rangle$. Linear maps "
            "send parallelograms to parallelograms and send the origin to the origin.",
            "The determinant $\\det A=ad-bc$ is the signed area scale factor. If $\\det A=0$, the map squashes "
            "the plane onto a line (or a point) and is not invertible. If $\\det A\\neq0$, the inverse map exists "
            "and has determinant $1/\\det A$.",
            "The inverse formula is $A^{-1}=\\dfrac{1}{ad-bc}\\begin{pmatrix}d&-b\\\\-c&a\\end{pmatrix}$: swap the "
            "main diagonal, negate the off-diagonal, divide by the determinant. Check by multiplying $AA^{-1}=I$, "
            "the identity $\\begin{pmatrix}1&0\\\\0&1\\end{pmatrix}$.",
            "Special maps: a diagonal matrix stretches the axes. $\\begin{pmatrix}0&-1\\\\1&0\\end{pmatrix}$ rotates "
            "$90^\\circ$ counterclockwise. A shear $\\begin{pmatrix}1&k\\\\0&1\\end{pmatrix}$ has determinant $1$ "
            "(area-preserving). Rotation matrices satisfy $A^{-1}=A^T$.",
            "Thinking of $A^{-1}$ as “the linear map that undoes $A$” is the Unit 1 inverse idea again. If $A$ "
            "sends $\\mathbf{e}_1$ to $\\mathbf{u}$, then $A^{-1}$ sends $\\mathbf{u}$ back to $\\mathbf{e}_1$. "
            "That sentence is an SAT stretch item in this unit.",
            "Matrix-vector multiplication is composition of the map with a point. Matrix-matrix multiplication "
            "is composition of two maps. The order matters: $AB$ is not usually $BA$, just as $f\\circ g$ is not $g\\circ f$.",
        ],
        "Matrices are functions from the plane to itself that preserve lines through the origin and addition. "
        "Inverses undo those functions. Systems of equations (next lesson) are “find the input that maps to $\\mathbf{b}$.”",
        "Write the two columns as the images of the basis vectors. Compute $ad-bc$. If it is nonzero, write the "
        "inverse by the swap-and-negate recipe and multiply to check.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#94a3b8", [(0, 0), (1, 0)]),
                    ("#94a3b8", [(0, 0), (0, 1)]),
                    ("#4f46e5", [(0, 0), (2, 0)]),
                    ("#dc2626", [(0, 0), (1, 2)]),
                ],
                points=[(2, 0, "A e1"), (1, 2, "A e2")],
                xlim=(-1, 4), ylim=(-1, 3),
            ),
            "Linear map $A=\\begin{pmatrix}2&1\\\\0&2\\end{pmatrix}$ sends the unit arrows to $\\langle 2,0\\rangle$ and $\\langle 1,2\\rangle$",
            "The gray unit square is sheared and scaled into a parallelogram of area $|\\det A|=4$.",
        )
        + solved(
            13, "Compute $\\det\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}$.",
            ["$ad-bc=4-6=-2$.",
             "Nonzero, so an inverse exists.",
             "Area is scaled by $2$ and orientation is reversed (negative det)."],
            "$-2$", "", "Easy",
        )
        + solved(
            14, "Find the inverse of $\\begin{pmatrix}2&1\\\\0&2\\end{pmatrix}$.",
            ["$\\det=4$.",
             "Swap-and-negate: $\\begin{pmatrix}2&-1\\\\0&2\\end{pmatrix}$.",
             "Divide by $4$: $A^{-1}=\\dfrac{1}{4}\\begin{pmatrix}2&-1\\\\0&2\\end{pmatrix}$."],
            "$\\dfrac{1}{4}\\begin{pmatrix}2&-1\\\\0&2\\end{pmatrix}$", "", "Medium",
        )
        + solved(
            15, "If $A$ sends $\\mathbf{e}_1$ to $\\langle 2,0\\rangle$, where does $A^{-1}$ send $\\langle 2,0\\rangle$?",
            ["$A^{-1}$ undoes $A$.",
             "$A^{-1}(A\\mathbf{e}_1)=\\mathbf{e}_1$.",
             "So $A^{-1}\\langle 2,0\\rangle=\\langle 1,0\\rangle$."],
            "$\\langle 1,0\\rangle$", "Inverse maps are inverse functions on vectors.", "Hard",
        ),
        ("Dividing by $ad-bc$ before swapping",
         "The recipe is swap, negate off-diagonal, then divide the whole matrix by the determinant. Dividing "
         "only $a$ and $d$ (or forgetting the minus signs on $b$ and $c$) produces a matrix that does not invert $A$."),
        ("Columns as images",
         "If you know where $\\mathbf{e}_1$ and $\\mathbf{e}_2$ go, you know $A$. If you know $A$, you know those "
         "two images. That dictionary is faster than multiplying by generic $\\langle x,y\\rangle$ when a question "
         "is about a specific basis vector."),
        [
            "I can compute a $2\\times2$ determinant.",
            "I can write $A^{-1}$ when $\\det A\\neq0$.",
            "I can interpret $A$ and $A^{-1}$ as inverse linear maps.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Systems via matrices",
        [
            "A linear system $ax+by=e$, $cx+dy=f$ is the matrix equation $A\\mathbf{x}=\\mathbf{b}$ with "
            "$A=\\begin{pmatrix}a&b\\\\c&d\\end{pmatrix}$, $\\mathbf{x}=\\langle x,y\\rangle$, $\\mathbf{b}=\\langle e,f\\rangle$. "
            "Geometrically you are asking which input vector $A$ sends to $\\mathbf{b}$. If $A$ is invertible, "
            "there is exactly one: $\\mathbf{x}=A^{-1}\\mathbf{b}$.",
            "If $\\det A=0$, the two lines are parallel (or the same line). Then either there is no solution "
            "(inconsistent $\\mathbf{b}$) or infinitely many (the two equations describe one line). A unique "
            "solution exists precisely when $\\det A\\neq0$.",
            "Cramer’s rule is a determinant shortcut: $x=\\dfrac{\\det A_x}{\\det A}$ where $A_x$ replaces the "
            "first column of $A$ by $\\mathbf{b}$, and similarly for $y$ with the second column. It is the same "
            "solution as $A^{-1}\\mathbf{b}$, packaged as two $2\\times2$ determinants.",
            "Checking is cheap: plug $(x,y)$ back into both original equations. A sign error in the inverse "
            "formula is caught immediately. For a stretch system such as $\\begin{pmatrix}1&2\\\\3&5\\end{pmatrix}"
            "\\begin{pmatrix}x\\\\y\\end{pmatrix}=\\begin{pmatrix}1\\\\1\\end{pmatrix}$, elimination may be faster "
            "than the inverse: $x+2y=1$, $3x+5y=1$ yields $y=2$, $x=-3$.",
            "Dependent systems ($\\det A=0$ but consistent) are not failures; they are lines that coincide. "
            "The solution set is a line in the plane, which you can write parametrically using Unit 8 lesson 3.",
            "This lesson closes Precalculus’s linear algebra corner: vectors, matrices, inverses, and systems "
            "are one story. Calculus will add derivatives; linear algebra courses will add $n$ dimensions. The "
            "$2\\times2$ case is the complete picture in the plane.",
        ],
        "Solving $A\\mathbf{x}=\\mathbf{b}$ is the practical reason matrices exist in Precalculus: two equations, "
        "two unknowns, one inverse (when it exists).",
        "Write $A$ and $\\mathbf{b}$. Compute $\\det A$. If nonzero, use $A^{-1}\\mathbf{b}$ or Cramer or elimination, "
        "then substitute back. If zero, check consistency of the two lines.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#4f46e5", sample_curve(lambda x: (5 - x) / 2, -1, 6)),
                    ("#dc2626", sample_curve(lambda x: (11 - 3 * x) / 4, -1, 6)),
                ],
                points=[(1, 2, "(1,2)")],
                xlim=(-1, 6), ylim=(-1, 6),
            ),
            "The system $x+2y=5$, $3x+4y=11$ as two lines meeting at $(1,2)$",
            "Unique intersection because $\\det A=4-6=-2\\neq0$. The solution is $A^{-1}\\langle 5,11\\rangle$.",
        )
        + solved(
            16, "Write $x+2y=5$, $3x+4y=11$ as $A\\mathbf{x}=\\mathbf{b}$ and name $\\mathbf{b}$.",
            ["$A=\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}$.",
             "$\\mathbf{b}=\\langle 5,11\\rangle$.",
             "$\\det A=-2\\neq0$, so a unique solution exists."],
            "$\\mathbf{b}=\\langle 5,11\\rangle$", "", "Easy",
        )
        + solved(
            17, "Solve that system using elimination.",
            ["Triple the first: $3x+6y=15$.",
             "Subtract the second: $2y=4$, $y=2$.",
             "$x+4=5$, $x=1$. Solution $(1,2)$."],
            "$(1,2)$", "Check: $3+8=11$.", "Medium",
        )
        + solved(
            18, "The system $2x+y=1$, $4x+2y=2$ has how many solutions, and why?",
            ["$\\det A=4-4=0$.",
             "The second equation is exactly twice the first, so the lines coincide.",
             "Infinitely many solutions (one line of them)."],
            "infinitely many", "If the second right-hand side had been $3$, there would be none.", "Hard",
        ),
        ("Inverting a singular matrix on a calculator and reading garbage",
         "If $\\det A=0$, there is no inverse to apply. Decide first whether the system is parallel-inconsistent "
         "or coincident-infinite. Do not press the inverse button."),
        ("Substitute back",
         "A $2\\times2$ check is two multiplications. It catches the almost-correct pair that satisfies only one equation."),
        [
            "I can write a $2\\times2$ system as $A\\mathbf{x}=\\mathbf{b}$.",
            "I can solve with $A^{-1}$ or elimination when $\\det A\\neq0$.",
            "I can interpret $\\det A=0$ as no unique solution.",
        ],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title, AUDIENCE, concepts, body, practice_slots(31, 25, STRETCH_LABEL),
    )
    return title, description, content, _u8_questions()


def build_master():
    units = [('Functions, Composition & Inverses', ['Domain and range review', 'Composition', 'Inverses algebraically', 'Inverses graphically', 'Even/odd and symmetry', 'Piecewise and absolute value']), ('Polynomial & Rational Functions', ['End behavior and zeros', 'Remainder/factor theorems', 'Graphing polynomials', 'Asymptotes of rationals', 'Holes and intercepts', 'Inequalities with sign charts']), ('Exponential & Logarithmic Functions', ['Growth and decay', 'Log as inverse', 'Log laws', 'Change of base', 'Solve exp/log equations', 'Logistic intro']), ('Trigonometry for Precalculus', ['Unit circle fluency', 'Graph all six', 'Identities toolkit', 'Trig equations', 'Inverse trig', 'Modeling with sine']), ('Analytic Trigonometry & Polar', ['Sum-to-product', 'Polar coordinates', 'Polar graphs', 'Convert polar/rectangular', 'De Moivre intro', 'Complex in polar form']), ('Conic Sections', ['Parabolas', 'Circles and ellipses', 'Hyperbolas', 'Complete the square to classify', 'Eccentricity', 'Applications']), ('Sequences, Series & Limits Intro', ['Arithmetic and geometric', 'Sigma notation', 'Infinite geometric', 'Limit intuition graphically', 'Limit algebraically (rational)', 'Squeeze idea']), ('Vectors, Parametric & Matrices', ['Vector operations', 'Dot product and angle', 'Parametric equations', 'Eliminate the parameter', '2x2 matrices and inverses', 'Systems via matrices'])]
    items = "".join(f"<li>Unit {i} — {u[0]}</li>" for i, u in enumerate(units, 1))
    return (
        f"<h1>Precalculus Complete</h1>"
        f"<p><strong>For:</strong> <strong>High school Precalculus</strong>. Eight deep units, each with six concepts, "
        "worked examples with matching diagrams, 5 quizzes per concept, and a 25-problem stretch finale.</p>"
        f"{page_break()}"
        "<h2>The eight units</h2>"
        f"<ol>{items}</ol>"
    )
