#!/usr/bin/env python3
"""Deep AP Calculus AB curriculum builders — Units 5–8."""

from __future__ import annotations

import math

from curriculum_kit import lesson_figure, svg_parabola, svg_plane

from hs_curriculum import (
    concept_block, solved, practice_slots, unit_shell, page_break, mq,
    xy_graph, sample_curve, number_line, tangent_curve_svg,
)
from .common import AUDIENCE, STRETCH_LABEL
from .units_1_4 import (
    _pack, _riemann_svg, _washer_svg, _slope_field_svg, _area_between_svg,
    _cross_section_svg, _accum_svg, _family_svg, _sign_chart_svg, _mvt_svg,
    _limit_jump_svg, _concavity_svg, _ivt_svg, _open_on, _ladder_svg,
)


# ===========================================================================
# UNIT 5: Integrals & FTC
# ===========================================================================

def _u5_questions():
    return _pack([
        ("An antiderivative of $2x$ is", "x^2+C",
         "Power rule reversed: $\\int x^n\\,dx=x^{n+1}/(n+1)+C$ for $n\\neq-1$.",
         ["2+C", "2x^2+C", "x+C"]),
        ("$\\int 3\\,dx$ equals", "3x+C", "The antiderivative of a constant $k$ is $kx+C$.", ["3+C", "3x^2+C", "0"]),
        ("$\\int x^3\\,dx$ equals", "x^4/4 + C", "Add one to the exponent and divide by the new exponent.", ["3x^2+C", "x^4+C", "x^3/3+C"]),
        ("If $F'(x)=f(x)$, then $F$ is called", "an antiderivative of f",
         "Any two antiderivatives differ by a constant on an interval.",
         ["the derivative of f", "a Riemann sum", "a slope field"]),
        ("$\\int e^x\\,dx$ equals", "e^x+C", "The exponential is its own antiderivative.", ["xe^{x-1}+C", "ln|x|+C", "1+C"]),
        ("A Riemann sum $\\sum f(x_i^*)\\Delta x$ approximates",
         "a definite integral (net area)",
         "Heights times widths of rectangles under (or against) a graph.",
         ["a derivative", "a slope field", "an asymptote"]),
        ("On $[0,4]$ with $n=4$ equal subdivisions, $\\Delta x=$", 1,
         "$(b-a)/n=4/4=1$.", [4, 0, 2]),
        ("Left Riemann sum for $f(x)=x$ on $[0,4]$ with $n=4$ uses heights",
         "0,1,2,3",
         "Left endpoints $0,1,2,3$. Sum $0+1+2+3=6$, while the true integral is $8$.",
         ["1,2,3,4", "0,2,4", "2,2,2,2"]),
        ("That left sum equals", 6, "$\\Delta x=1$ times $0+1+2+3$.", [8, 10, 4]),
        ("A right Riemann sum on an increasing positive $f$ is",
         "an overestimate of the integral",
         "Each rectangle’s height is the right (larger) endpoint value.",
         ["an underestimate", "exact always", "negative always"]),
        ("$\\int_a^b f(x)\\,dx$ equals the net signed area of $y=f(x)$ from $a$ to $b$. Area below the $x$-axis counts",
         "negative",
         "That is why “net” is in the sentence. Total area uses $\\int|f|$.",
         ["positive anyway", "zero", "as a derivative"]),
        ("$\\int_0^2 (x-1)\\,dx$ equals", 0,
         "Antiderivative $x^2/2-x$ from $0$ to $2$: $(2-2)-0=0$. Equal triangles cancel.",
         [2, 1, -1]),
        ("$\\int_1^3 4\\,dx$ equals", 8, "Rectangle width $2$ height $4$.", [4, 12, 3]),
        ("Reversing limits: $\\int_b^a f=-\\int_a^b f$. So $\\int_5^2 1\\,dx=$",
         -3, "$2-5=-3$.", [3, 7, 0]),
        ("If $f$ is odd and the integral exists, $\\int_{-a}^{a}f(x)\\,dx=$",
         0, "Symmetric signed areas cancel.", ["2∫_0^a f", "a", "f(a)"]),
        ("FTC Part 1: if $F(x)=\\int_a^x f(t)\\,dt$ and $f$ is continuous, then $F'(x)=$",
         "f(x)",
         "The derivative of the accumulation function is the original integrand, evaluated at the upper limit.",
         ["f(a)", "F(x)", "0"]),
        ("If $G(x)=\\int_2^x \\cos t\\,dt$, then $G'(x)=$", "cos x", "FTC1 with $f(t)=\\cos t$.", ["cos 2", "sin x", "-sin x"]),
        ("If $H(x)=\\int_1^{x^3} e^{t}\\,dt$, then $H'(x)=$",
         "e^{x^3} · 3x^2",
         "FTC1 plus chain rule: $f(u(x))u'(x)$ with $u=x^3$.",
         ["e^{x^3}", "e^x · 3x^2", "e^{x^3}/3x^2"]),
        ("$\\dfrac{d}{dx}\\int_{2x}^{5} f(t)\\,dt=$",
         "-2 f(2x)",
         "Flip limits: $-\\dfrac{d}{dx}\\int_5^{2x}f= -f(2x)\\cdot 2$.",
         ["f(2x)", "5f(5)-2f(2x)", "f(5)-f(2x)"]),
        ("If $F(x)=\\int_0^x (t^2-1)\\,dt$, then $F'(2)=$", 3,
         "$F'(x)=x^2-1$, so $F'(2)=3$.", [0, 1, -1]),
        ("FTC Part 2: $\\int_a^b f(x)\\,dx=F(b)-F(a)$ provided $F'=f$ and $f$ is continuous on $[a,b]$. Evaluate $\\int_0^1 2x\\,dx$.",
         1, "$F=x^2$, $1-0=1$.", [2, 0, 1 / 2]),
        ("$\\int_0^{\\pi} \\sin x\\,dx$ equals", 2, "$-\\cos x$ from $0$ to $\\pi$: $-(-1)-(-1)=2$.", [0, 1, -2]),
        ("$\\int_1^e \\dfrac{1}{x}\\,dx$ equals", 1, "$\\ln|x|$ from $1$ to $e$: $1-0=1$.", ["e", 0, "ln 1"]),
        ("$\\int_{-1}^{1} x^3\\,dx$ equals", 0, "Odd integrand on a symmetric interval.", [1 / 2, 2, 1]),
        ("If $F(3)=7$ and $F(1)=2$ with $F'=f$, then $\\int_1^3 f=$", 5,
         "FTC2 is exactly $F(3)-F(1)$.", [9, 2, 7]),
        ("Substitution: $\\int 2x\\cos(x^2)\\,dx$. Let $u=x^2$, $du=2x\\,dx$. The integral becomes",
         "∫ cos u du",
         "The $2x\\,dx$ is exactly $du$.", ["∫ 2x cos u du", "∫ cos(x^2) dx", "∫ u du"]),
        ("That antiderivative is", "sin(x^2)+C", "$\\sin u+C$, then back-substitute.", ["cos(x^2)+C", "sin(2x)+C", "x^2 sin x+C"]),
        ("$\\int_0^1 6x(x^2+1)^2\\,dx$. With $u=x^2+1$, $u(0)=1$, $u(1)=2$, so the definite integral is",
         "∫_1^2 3 u^2 du",
         "$du=2x\\,dx$, and $6x\\,dx=3\\,du$. Limits must change to $u$-values.",
         ["∫_0^1 3u^2 du", "∫_1^2 6u^2 du", "∫_0^1 6x u^2 dx"]),
        ("Evaluating $\\int_1^2 3u^2\\,du$ gives", 7, "$u^3$ from $1$ to $2$: $8-1=7$.", [3, 8, 1]),
        ("A substitution that forgets to change definite-integral bounds and also forgets to return to $x$ is",
         "invalid (either change bounds or revert to x before evaluating)",
         "Pick one legal path and finish it.",
         ["always fine", "how FTC1 works", "how Riemann sums work"]),
        ("An antiderivative of $\\sec^2 x$ is", "tan x + C", "Because $(\\tan x)'=\\sec^2 x$.", ["sec x+C", "cos x+C", "x+C"]),
        ("$\\int (4x-1)\\,dx=$", "2x^2-x+C", "Termwise power rule.", ["4x^2-x+C", "4-C", "2x-1+C"]),
        ("Midpoint Riemann on $[0,2]$ with $n=2$ for $f(x)=x^2$ uses $x^*=$",
         "0.5 and 1.5",
         "Subintervals $[0,1]$ and $[1,2]$; midpoints $1/2$ and $3/2$. Sum $1\\cdot(0.25+2.25)=2.5$.",
         ["0 and 2", "1 and 2", "0.5 only"]),
        ("That midpoint sum equals", 2.5, "$\\Delta x=1$, $f(0.5)+f(1.5)=0.25+2.25$. True $\\int_0^2 x^2=8/3\\approx 2.67$.", [4, 8 / 3, 1]),
        ("$\\int_0^3 |x-1|\\,dx$ equals", 2.5,
         "Split at $1$: $\\int_0^1(1-x)+\\int_1^3(x-1)=[x-x^2/2]_0^1+[x^2/2-x]_1^3=1/2+2=2.5$.",
         [3, 1, 0]),
        ("Net area of $y=4-x$ from $0$ to $6$ is",
         6, "$[4x-x^2/2]_0^6=24-18=6$. (Geometric: triangle up $8$ minus triangle down $2$.)",
         [12, 0, 24]),
        ("If $F(x)=\\int_{\\pi}^{x} \\sin t\\,dt$, then $F'(\\pi/2)=$", 1,
         "$F'(x)=\\sin x$, $\\sin(\\pi/2)=1$.", [0, -1, "π"]),
        ("$\\dfrac{d}{dx}\\int_{x}^{x^2} \\sqrt{1+t^3}\\,dt=$",
         "2x√(1+x^6) − √(1+x^3)",
         "Upper: $f(x^2)\\cdot 2x$; lower: $-f(x)$.",
         ["√(1+x^3)", "f(x^2)-f(x)", "2x√(1+x^6)"]),
        ("$\\int_0^{\\pi/2} \\cos x\\,dx=$", 1, "$\\sin x$ from $0$ to $\\pi/2$: $1-0=1$.", [0, 2, -1]),
        ("$\\int  \\dfrac{1}{1+x^2}$ is not required as arctan on AB if a stem stays algebraic, but $\\int \\dfrac{2x}{1+x^2}\\,dx$ by substitution is",
         "ln|1+x^2|+C",
         "$u=1+x^2$, $du=2x\\,dx$.", ["arctan x+C", "1/(1+x^2)+C", "2x ln|1+x^2|+C"]),
        ("$\\int_1^4 \\dfrac{1}{\\sqrt{x}}\\,dx=$", 2, "$2x^{1/2}$ from $1$ to $4$: $4-2=2$.", [1, 3, 8]),
        ("A trapezoidal approximation with $n=2$ on $[0,2]$ for $f(x)=x^2$ is",
         3, "$\\Delta x=1$, $\\frac12(f(0)+2f(1)+f(2))=\\frac12(0+2+4)=3$.", [2.5, 8 / 3, 4]),
        ("If $f$ is continuous, $\\int_a^a f(x)\\,dx=$", 0, "Zero width.", ["f(a)", "1", "a"]),
        ("$\\int e^{3x}\\,dx=$", "(1/3)e^{3x}+C", "Guess $e^{3x}$, compensate the chain-rule $3$.", ["3e^{3x}+C", "e^{3x}+C", "e^{3x}/3x+C"]),
        ("$\\int \\sin(5x)\\,dx=$", "(-1/5)cos(5x)+C", "Chain-rule compensation.", ["5 cos(5x)+C", "-cos(5x)+C", "cos(5x)+C"]),
        ("AP Stretch: $F(x)=\\int_{2x}^{x^2} \\sqrt{1+t^4}\\,dt$. Then $F'(1)$ equals",
         "2√2 − 2√17",
         "Chain on both limits: $F'(x)=f(x^2)(2x)-f(2x)(2)$. At $x=1$: $2\\sqrt{1+1}-2\\sqrt{1+16}=2\\sqrt{2}-2\\sqrt{17}$.",
         ["0", "√2", "2√2"]),
        ("AP Stretch: Let $F(x)=\\int_{2x}^{x^2} \\sqrt{1+t^4}\\,dt$. Then $F'(x)$ equals",
         "2x√(1+x^8) − 2√(1+16x^4)",
         "Leibniz/FTC1+chain: $f(x^2)\\cdot 2x-f(2x)\\cdot 2$, and $(2x)^4=16x^4$.",
         ["√(1+x^4)", "2x√(1+x^4)", "√(1+x^8)−√(1+16x^4)"]),
        ("AP Stretch: After $u=\\ln x$ on $\\int_e^{e^2} \\dfrac{1}{x\\ln x}\\,dx$, the integral equals",
         "ln 2",
         "$du=dx/x$, limits from $1$ to $2$, $\\int_1^2 \\dfrac{1}{u}\\,du=\\ln 2$.",
         ["1", "e", 2]),
        ("AP Stretch: A student evaluates $\\int_0^2 x(4-x^2)^3\\,dx$ by setting $u=4-x^2$ but treating $du=x\\,dx$ (missing the $-2$), and reports $\\int_4^0 u^3\\,du=-64$. The correct value is",
         32,
         "$du=-2x\\,dx$, so the integral is $-\\frac12\\int_4^0 u^3\\,du=\\frac12\\int_0^4 u^3\\,du=\\frac12\\cdot 64=32$.",
         ["-64", "64", "-32"]),
        ("AP Stretch: Table of a decreasing $f$: $f(0)=8$, $f(2)=5$, $f(4)=1$. Left Riemann $n=2$ on $[0,4]$ equals",
         26, "$\\Delta x=2$, $2(8+5)=26$, an overestimate because $f$ is decreasing.",
         [12, 16, 20]),
        ("AP Stretch: A decreasing continuous $f$ has $f(1)=10$, $f(3)=7$, $f(5)=3$, $f(7)=0$. The trapezoidal approximation to $\\int_1^7 f(x)\\,dx$ with $n=3$ equal subintervals equals",
         30,
         "$\\Delta x=2$, so $\\frac{\\Delta x}{2}(10+2\\cdot 7+2\\cdot 3+0)=10+14+6=30$. A left Riemann sum $2(10+7+3)=40$ would overestimate the decreasing function.",
         [40, 20, 26]),
        ("AP Stretch: $g(x)=\\int_0^{x} f(t)\\,dt$ for an even continuous $f$. Then $g$ is",
         "odd, and g'(x)=f(x)",
         "Accumulation of an even function from $0$ is odd (signed areas mirror with a sign change). FTC1 still gives $g'=f$.",
         ["even", "constant", "g'=0"]),
        ("AP Stretch: Let $H(x)=\\int_0^{\\sin x} \\sqrt{1+t^3}\\,dt$. Then $H'\\!\\left(\\dfrac{\\pi}{6}\\right)$ equals",
         "3√6 / 8",
         "$H'(x)=\\sqrt{1+\\sin^3 x}\\cdot\\cos x$. At $\\pi/6$: $\\sqrt{1+1/8}\\cdot\\sqrt{3}/2=(3\\sqrt{2}/4)\\cdot(\\sqrt{3}/2)=3\\sqrt{6}/8$.",
         [0, "√3/2", "√(9/8)"]),
        ("AP Stretch: Let $P(x)=\\int_{1-x}^{e^{x}} \\dfrac{1}{1+t}\\,dt$. Then $P'(0)$ equals",
         1,
         "Leibniz: $P'(x)=\\dfrac{e^{x}}{1+e^{x}}-\\dfrac{1}{2-x}\\cdot(-1)$. At $0$: $\\dfrac{1}{2}+\\dfrac{1}{2}=1$.",
         [0, "1/2", "e/(1+e)"]),
        ("AP Stretch: $K(x)=\\int_{e^{-x}}^{x^2} \\dfrac{1}{1+t^2}\\,dt$. Then $K'(1)$ equals",
         "1 + e/(e^2+1)",
         "Leibniz/FTC1+chain: $K'(x)=\\dfrac{2x}{1+x^4}+\\dfrac{e^{-x}}{1+e^{-2x}}$. At $x=1$: $1+\\dfrac{e^{-1}}{1+e^{-2}}=1+\\dfrac{e}{e^2+1}$.",
         [0, 1, "arctan 1 − arctan(1/e)"]),
    ])


def build_unit5():
    title = "AP Calculus AB Unit 5: Integrals & FTC"
    description = (
        "Antiderivatives, Riemann sums, net signed area, both parts of the Fundamental Theorem, "
        "and substitution — including chain rule on accumulation functions."
    )
    concepts = [
        "Antiderivatives",
        "Riemann sums",
        "Definite integral as net area",
        "FTC part 1",
        "FTC part 2",
        "Substitution",
    ]

    fam = xy_graph(
        curves=[
            ("#94a3b8", sample_curve(lambda x: 0.25 * x * x - 1.5, -3, 3)),
            ("#64748b", sample_curve(lambda x: 0.25 * x * x, -3, 3)),
            ("#4f46e5", sample_curve(lambda x: 0.25 * x * x + 1.4, -3, 3)),
        ],
        xlim=(-3.2, 3.2), ylim=(-2.2, 4.2), w=300, h=250,
    )

    c1 = concept_block(
        "1. Antiderivatives",
        [
            "An antiderivative of $f$ is a function $F$ with $F'=f$. On an interval, if $F$ is one antiderivative then every antiderivative is $F+C$ for a constant $C$. That family is the indefinite integral $\\int f(x)\\,dx=F(x)+C$.",
            "The power rule reverses: $\\int x^n\\,dx=\\dfrac{x^{n+1}}{n+1}+C$ for $n\\neq-1$. The missing case $n=-1$ is $\\int \\dfrac{1}{x}\\,dx=\\ln|x|+C$.",
            "Known pairs from Unit 2 reverse immediately: $\\int\\cos x=\\sin x+C$, $\\int\\sin x=-\\cos x+C$, $\\int e^x=e^x+C$, $\\int\\sec^2 x=\\tan x+C$.",
            "A chain-rule derivative such as $3e^{3x}$ reverses by compensating: $\\int e^{3x}\\,dx=\\frac13 e^{3x}+C$. Guess, differentiate to check, fix the constant factor.",
            "Checking by differentiation is not optional on AP when the antiderivative looks fancy. If $F'$ is not exactly the integrand, $C$ will not save you.",
            "Indefinite integrals produce families of curves; definite integrals in the next lessons produce numbers (net area). Keep the $+C$ until a definite integral or an initial condition kills it.",
        ],
        "Every FTC evaluation is “find an antiderivative, then subtract.” If the reverse power rule is shaky, Units 5–6 collapse.",
        "Differentiate your answer. If you do not recover the integrand, the antiderivative is wrong — fix the chain-rule constant before you go on.",
        lesson_figure(
            fam,
            "Three antiderivatives of $f(x)=x/2$: the same shape, shifted by $C$",
            "Vertical translation does not change slope. That is why $+C$ is required for an indefinite integral and why an initial condition selects one curve.",
        )
        + solved(
            1,
            "Find $\\int (6x-4)\\,dx$.",
            ["$3x^2-4x+C$.", "Check: $6x-4$."],
            "$3x^2-4x+C$", "", "Easy",
        )
        + solved(
            2,
            "Find $\\int (x^3+1/x)\\,dx$ for $x>0$.",
            ["$x^4/4+\\ln x+C$.", "Check: $x^3+1/x$."],
            "$\\dfrac{x^4}{4}+\\ln x+C$", "Use $\\ln|x|$ if the domain includes negatives.", "Medium",
        )
        + solved(
            3,
            "Find $\\int 5\\cos(5x)\\,dx$ by inspection, then check.",
            ["Guess $\\sin(5x)$; derivative is $5\\cos(5x)$.", "So the $5$ is already accounted for: $\\sin(5x)+C$."],
            "$\\sin(5x)+C$", "If the integrand had been only $\\cos(5x)$, you would divide by $5$.", "Honors",
        ),
        ("Dropping $+C$ on an indefinite integral",
         "A definite integral is a number and has no $+C$. An indefinite integral is a family and must show $+C$. Mixing the two notations is an AP communication error."),
        ("Differentiate to check before boxing",
         "Especially after a chain-rule guess. The check takes five seconds and catches the missing $1/k$ factor."),
        ["I reverse the power rule.", "I keep +C on indefinite integrals.", "I check by differentiating."],
        1,
    )

    c2 = concept_block(
        "2. Riemann sums",
        [
            "A Riemann sum $\\sum_{i=1}^{n} f(x_i^*)\\Delta x$ adds rectangle areas. Left, right, and midpoint sums name which sample point $x_i^*$ is used in each subinterval.",
            "$\\Delta x=(b-a)/n$ for equal partitions. Write the $x$-grid first, then the heights, then multiply.",
            "If $f$ is positive and increasing, left sums underestimate and right sums overestimate the integral. Decreasing reverses that. Midpoint and trapezoid have their own error patterns.",
            "A table of values is the usual AP calculator-inactive Riemann item. You cannot invent extra heights; use only the given sample points.",
            "Trapezoidal rule is the average of left and right sums: $\\dfrac{\\Delta x}{2}(y_0+2y_1+\\cdots+2y_{n-1}+y_n)$.",
            "The definite integral is defined as the limit of Riemann sums as $\\Delta x\\to 0$ (mesh to zero). FTC then gives a way to evaluate that limit without adding infinitely many rectangles.",
        ],
        "When an FRQ gives a table instead of a formula, Riemann/trapezoid/midpoint is often the only legal approximation of an integral.",
        "Draw the rectangles on a tiny sketch even if the prompt is a table. Left versus right becomes obvious, and so does over/under.",
        lesson_figure(
            _riemann_svg(4),
            "Left Riemann rectangles under a rising curve on $[1,5]$",
            "Each height is taken at the left edge of its subinterval, so on an increasing graph the rectangles sit below the curve.",
        )
        + solved(
            1,
            "For $f(x)=x$ on $[0,3]$ with $n=3$ left rectangles, compute the sum.",
            ["$\\Delta x=1$. Left heights $0,1,2$.", "Sum $0+1+2=3$."],
            "$3$", "True integral is $9/2$; left underestimates an increasing $f$.", "Easy",
        )
        + solved(
            2,
            "Right Riemann, same data.",
            ["Heights $1,2,3$.", "Sum $6$."],
            "$6$", "Overestimate.", "Medium",
        )
        + solved(
            3,
            "A table: $t=0,2,5$ hours and $v=10,16,22$ mi/h. Trapezoidal approximation of $\\int_0^5 v\\,dt$.",
            [
                "Unequal $\\Delta t$: $2$ and $3$.",
                "Trapezoids: $\\frac{2}{2}(10+16)+\\frac{3}{2}(16+22)=26+57=83$.",
                "Units: miles (rate times time).",
            ],
            "$83$ miles", "Do not force a single $\\Delta t$ when the table is irregular.", "Honors",
        ),
        ("Using a right endpoint with a left-sum instruction",
         "Read the word left/right/midpoint twice. The formula is the same; only $x_i^*$ changes."),
        ("Write Δx, list the sample x-values, list the heights, then multiply",
         "Four rows on the page. Graders can then award method points even if one height is misread from a table."),
        ["I can compute left/right/mid/trap sums.", "I can judge over vs under from monotonicity.", "I keep units on a rate table."],
        6,
    )

    net = xy_graph(
        curves=[("#4f46e5", sample_curve(lambda x: 0.5 * x - 1.2, 0, 5))],
        xlim=(-0.3, 5.3), ylim=(-2, 2.2), w=300, h=230, xlab="x", ylab="f(x)",
    )

    c3 = concept_block(
        "3. Definite integral as net area",
        [
            "$\\int_a^b f(x)\\,dx$ is the net signed area between $y=f(x)$ and the $x$-axis from $x=a$ to $x=b$. Above counts positive; below counts negative.",
            "Total area (always positive) is $\\int_a^b |f(x)|\\,dx$, which requires splitting at zeros of $f$.",
            "Geometry beats FTC on piecewise-linear graphs: triangles, rectangles, and trapezoids. AP loves a triangular net-area question with no antiderivative required.",
            "Properties: $\\int_a^b= -\\int_b^a$, $\\int_a^a=0$, additivity on adjacent intervals, and constants factor out.",
            "If $f$ is odd and the integral exists, $\\int_{-a}^{a}f=0$. If $f$ is even, $\\int_{-a}^{a}f=2\\int_0^a f$.",
            "Net area is the visual meaning of FTC2’s number $F(b)-F(a)$ and of the net-change theorem in Unit 6.",
        ],
        "Mixing net area with total area is a high-frequency sign error, especially on velocity graphs (displacement vs distance).",
        "Sketch, mark zeros, assign $+$ and $-$ to each region, then add. If the prompt says “total area,” insert absolute values.",
        lesson_figure(
            net,
            "A line crossing the axis: one positive triangle and one negative triangle",
            "Net integral is the difference of those areas. Total area is the sum of their absolute values.",
        )
        + solved(
            1,
            "Find $\\int_0^2 3\\,dx$ as area.",
            ["Rectangle width $2$, height $3$.", "Area $6$."],
            "$6$", "", "Easy",
        )
        + solved(
            2,
            "Find $\\int_0^4 (x-2)\\,dx$ as net area.",
            [
                "Zero at $x=2$. Triangle from $0$ to $2$ has area $2$ below; from $2$ to $4$ area $2$ above.",
                "Net $0$. Total area $4$.",
            ],
            "net $0$ (total area $4$ if asked)", "", "Medium",
        )
        + solved(
            3,
            "A graph of $v(t)$ is a triangle of height $6$ from $t=0$ to $t=4$ above the axis, then a triangle of height $3$ from $4$ to $6$ below. Displacement and distance on $[0,6]$?",
            [
                "Displacement $=\\frac12(4)(6)-\\frac12(2)(3)=12-3=9$.",
                "Distance $=12+3=15$.",
            ],
            "displacement $9$; distance $15$", "Velocity graph: net integral vs $\\int|v|$.", "Honors",
        ),
        ("Reporting a positive area when the prompt asked for a definite integral of a function that dips below",
         "The definite integral is allowed to be negative. “Area of the region” in later Unit 6 is nonnegative and uses $\\int(\\text{top}-\\text{bottom})$."),
        ("Split at zeros before you integrate |f|",
         "If you do not split, the calculator of net area will cancel and you will under-report total area."),
        ["I distinguish net vs total area.", "I use geometry on linear graphs.", "I apply additivity and reversal of limits."],
        11,
    )

    accum = xy_graph(
        curves=[("#dc2626", sample_curve(lambda t: math.cos(t), 0, 6.2)),
                ("#1d4ed8", sample_curve(lambda t: math.sin(t), 0, 6.2))],
        xlim=(-0.3, 6.5), ylim=(-1.6, 1.6), w=320, h=240, xlab="x", ylab="y",
    )

    c4 = concept_block(
        "4. Fundamental Theorem of Calculus, Part 1",
        [
            "If $f$ is continuous on an interval containing $a$ and $F(x)=\\int_a^x f(t)\\,dt$, then $F'(x)=f(x)$. The derivative undoes accumulation from a fixed lower limit.",
            "Variable upper limits need the chain rule: $\\dfrac{d}{dx}\\int_a^{g(x)}f(t)\\,dt=f(g(x))g'(x)$. Variable lower limits produce a minus: $\\dfrac{d}{dx}\\int_{h(x)}^a f=-f(h(x))h'(x)$.",
            "Both limits variable: $\\dfrac{d}{dx}\\int_{h(x)}^{g(x)}f=f(g(x))g'(x)-f(h(x))h'(x)$. This is the AP “accumulation + chain” item.",
            "The dummy variable $t$ inside the integral is not $x$. Never differentiate the integrand with respect to $t$ and also treat $t$ as $x$ in the same line.",
            "Sign interpretation: if $f$ is a rate, $F(x)$ is net change from time $a$ to time $x$, and $F'(x)$ recovers the rate.",
            "FTC1 is how you graph an accumulation function from the graph of $f$: $F$ increases where $f>0$, has critical points where $f=0$, and has inflections where $f$ has extrema ($F''=f'$).",
        ],
        "This is among the most-tested AB derivative skills. Missing the chain-rule factor on a variable limit is a yearly free-response error.",
        "Rewrite $\\int_{h}^{g}$ as $G(g(x))-G(h(x))$ in your head, then differentiate with the chain rule. That picture prevents dropping a minus on the lower limit.",
        lesson_figure(
            accum,
            "If $f(x)=\\cos x$ (red), an antiderivative starting at $0$ is $F(x)=\\sin x$ (blue)",
            "FTC1 says $F'=f$. Where cosine is positive, sine is increasing. Where cosine is zero, sine has a horizontal tangent.",
        )
        + solved(
            1,
            "If $F(x)=\\int_0^x (t^2+1)\\,dt$, find $F'(x)$.",
            ["FTC1: $F'(x)=x^2+1$."],
            "$x^2+1$", "", "Easy",
        )
        + solved(
            2,
            "If $H(x)=\\int_1^{3x} \\sqrt{1+t^2}\\,dt$, find $H'(x)$.",
            ["Upper limit $u=3x$, $u'=3$.", "$H'(x)=\\sqrt{1+(3x)^2}\\cdot 3=3\\sqrt{1+9x^2}$."],
            "$3\\sqrt{1+9x^2}$", "", "Medium",
        )
        + solved(
            3,
            "Differentiate $K(x)=\\int_{2x}^{x^2} \\sin(t^2)\\,dt$.",
            [
                "$K'(x)=\\sin((x^2)^2)\\cdot 2x-\\sin((2x)^2)\\cdot 2$.",
                "That is $2x\\sin(x^4)-2\\sin(4x^2)$.",
            ],
            "$2x\\sin(x^4)-2\\sin(4x^2)$", "Both limits move; both chains appear.", "Honors",
        ),
        ("Differentiating the integrand and ignoring the limits",
         "$\\dfrac{d}{dx}\\int_0^x \\sin(t^2)\\,dt$ is $\\sin(x^2)$, not $2x\\cos(x^2)$. You do not chain inside unless the upper limit itself needs a chain."),
        ("Write f(upper)·(upper)' minus f(lower)·(lower)'",
         "One template for every FTC1+chain problem. Fill the blanks; do not re-derive Leibniz’s rule from scratch each time."),
        ["I apply FTC1 to a fixed lower limit.", "I attach g'(x) for a variable upper limit.", "I subtract the lower-limit chain."],
        16,
    )

    c5 = concept_block(
        "5. Fundamental Theorem of Calculus, Part 2",
        [
            "If $f$ is continuous on $[a,b]$ and $F'=f$, then $\\int_a^b f(x)\\,dx=F(b)-F(a)$. Evaluation is a subtraction of antiderivative values, not a new kind of algebra.",
            "The hypotheses matter: continuity of $f$ on the closed interval. A jump inside $(a,b)$ makes this form of FTC illegal until you split the integral.",
            "Write the evaluation bar $F(x)\\Big|_a^b$ and compute $F(b)$ then $F(a)$ separately before subtracting. Sign errors happen in the second term.",
            "Combine with geometry: sometimes part of the interval is easier as a triangle and part needs an antiderivative.",
            "Net change language: $\\int_a^b F'(x)\\,dx=F(b)-F(a)$ even when $F$ is position, temperature, or volume. That is Unit 6’s theorem with FTC2’s proof.",
            "If you cannot find an elementary antiderivative, you may still approximate with Riemann sums — FTC2 is a gift, not an obligation when $F$ is unavailable.",
        ],
        "This is how AB actually computes most definite integrals. A correct antiderivative with a subtraction error still loses the answer point.",
        "Box $F(b)$ and $F(a)$ on separate lines, then subtract. Do not subtract inside a messy antiderivative in one gasp.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: 0.3 * x * x + 0.4, 0.2, 3.2))],
                xlim=(-0.2, 3.6), ylim=(-0.3, 4), w=300, h=230,
            ),
            "The definite integral $\\int_1^3 f$ is the area of this region — computed as $F(3)-F(1)$",
            "FTC2 converts that area into two antiderivative numbers. The picture is the meaning; the subtraction is the method.",
        )
        + solved(
            1,
            "Evaluate $\\int_1^4 2x\\,dx$.",
            ["$F=x^2$.", "$16-1=15$."],
            "$15$", "", "Easy",
        )
        + solved(
            2,
            "Evaluate $\\int_0^{\\pi/2} \\cos x\\,dx$.",
            ["$F=\\sin x$.", "$\\sin(\\pi/2)-\\sin 0=1$."],
            "$1$", "", "Medium",
        )
        + solved(
            3,
            "Evaluate $\\int_{-2}^{2} (x^3+x)\\,dx$ with a theorem, not a long antiderivative expansion.",
            [
                "The integrand is odd and continuous.",
                "Symmetric interval: the integral is $0$.",
                "(Check: $x^4/4+x^2/2$ is even, so $F(2)-F(-2)=0$.)",
            ],
            "$0$", "Odd-function shortcut is AP-legal when you name it.", "Honors",
        ),
        ("Computing F(a)-F(b) by accident",
         "The order is upper minus lower: $F(b)-F(a)$. Reversing it flips the sign of every definite integral you ever do."),
        ("Write the antiderivative, then a clear evaluation bar",
         "Graders award an antiderivative point even if the arithmetic of $F(b)-F(a)$ slips. Let them see $F$."),
        ["I evaluate F(b)−F(a).", "I split at discontinuities.", "I use odd/even shortcuts when they apply."],
        21,
    )

    c6 = concept_block(
        "6. Substitution",
        [
            "Substitution reverses the chain rule. If $u=g(x)$ and $du=g'(x)\\,dx$, then $\\int f(g(x))g'(x)\\,dx=\\int f(u)\\,du$.",
            "The entire $du$ must be present (up to a constant factor you can adjust). $\\int \\cos(x^2)\\,dx$ is not a basic $u=x^2$ substitution because $2x\\,dx$ is missing — and AB will not ask you to pretend it is elementary.",
            "On a definite integral you must either change the limits to $u(a)$ and $u(b)$ or substitute back to $x$ before evaluating. Mixing $u$-expressions with $x$-limits is illegal.",
            "Constant adjustment: $\\int x e^{x^2}\\,dx$ has $du=2x\\,dx$, so write $\\frac12\\int e^u\\,du$.",
            "After substituting, the integral should look like a Unit 5 basic form. If it looks worse, you chose a poor $u$.",
            "Check by differentiating the final answer. The chain rule should rebuild the original integrand.",
        ],
        "Substitution is the last algebraic engine of AB integration before applications. Without it, $\\int 2x\\cos(x^2)$ is a wall.",
        "Write $u=\\ldots$, $du=\\ldots$, and (for definite integrals) new limits, all before you integrate. Three declarations, then a basic antiderivative.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: 2 * x * math.exp(-0.3 * x * x), -2.8, 2.8))],
                xlim=(-3, 3), ylim=(-2.2, 2.2), w=300, h=230,
            ),
            "The integrand $2x e^{-x^2/\\text{const}}$ is a chain-rule derivative — substitution is natural",
            "The odd-looking extra $x$ is exactly $du$ waiting to happen, not a product-rule obstacle.",
        )
        + solved(
            1,
            "Find $\\int 2x(x^2+1)^3\\,dx$.",
            ["$u=x^2+1$, $du=2x\\,dx$.", "$\\int u^3\\,du=u^4/4+C=(x^2+1)^4/4+C$."],
            "$\\dfrac{(x^2+1)^4}{4}+C$", "", "Easy",
        )
        + solved(
            2,
            "Evaluate $\\int_0^{1} 6x^2(x^3+1)\\,dx$ by substitution.",
            [
                "$u=x^3+1$, $du=3x^2\\,dx$, so $6x^2\\,dx=2\\,du$.",
                "Limits: $x=0\\to u=1$, $x=1\\to u=2$.",
                "$2\\int_1^2 u\\,du=u^2|_1^2=4-1=3$.",
            ],
            "$3$", "Changed limits; never mixed $u$ with $0$ and $1$.", "Medium",
        )
        + solved(
            3,
            "Evaluate $\\int_0^{\\sqrt{\\pi}} x\\cos(x^2)\\,dx$.",
            [
                "$u=x^2$, $du=2x\\,dx$, so $\\frac12\\int \\cos u\\,du$.",
                "Limits $0$ to $\\pi$.",
                "$\\frac12\\sin u|_0^\\pi=0$.",
            ],
            "$0$", "A full period of sine from $0$ to $\\pi$ nets zero; the $1/2$ does not matter.", "Honors",
        ),
        ("Changing the integrand to u but leaving bounds in x",
         "Either $u$-limits or a return to $x$. A hybrid $\\sin u$ evaluated from $x=0$ to $x=1$ is undefined as written."),
        ("Declare u, du, and new bounds before integrating",
         "That three-line header is how AP readers see that substitution was legal."),
        ["I match du to the leftover factor.", "I change definite limits.", "I check by differentiating."],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u5_questions()


# ===========================================================================
# UNIT 6: Applications of Integration
# ===========================================================================

def _u6_questions():
    return _pack([
        ("Area between $y=x$ and $y=x^2$ on $[0,1]$ is $\\int_0^1(x-x^2)\\,dx=$",
         "1/6", "$[x^2/2-x^3/3]_0^1=1/2-1/3=1/6$.", ["1/2", "1/3", "1"]),
        ("The integrand for area is always", "top − bottom (or right − left)",
         "That difference is nonnegative if you identified the curves correctly.",
         ["top + bottom", "π(top)^2", "f'"]),
        ("If the curves swap which is on top, you must",
         "split the integral at the intersection",
         "Or use $\\int|f-g|$. Sign errors mean you subtracted the wrong way on a piece.",
         ["ignore the intersection", "always integrate from 0 to 1", "use a slope field"]),
        ("$y=\\sqrt{x}$ and $y=x/2$ intersect at $x=0$ and $x=4$. Area is $\\int_0^4(\\sqrt{x}-x/2)\\,dx=$",
         "4/3", "$[\\frac23 x^{3/2}-x^2/4]_0^4=\\frac23\\cdot 8-4=16/3-4=4/3$.", ["8", "2", "16/3"]),
        ("Integrating with respect to $y$ is wiser when",
         "the region is easier as right-minus-left",
         "A function $x=g(y)$ description can avoid splitting in $x$.",
         ["never", "only for circles about the y-axis always", "FTC forbids dy"]),
        ("Disk method about the $x$-axis: $V=\\pi\\int [R(x)]^2\\,dx$. For $y=\\sqrt{x}$ from $0$ to $4$, $R=\\sqrt{x}$, so $V=$",
         "8π", "$\\pi\\int_0^4 x\\,dx=\\pi[x^2/2]_0^4=8\\pi$.", ["4π", "16π", "2π"]),
        ("Washer method: $V=\\pi\\int\\bigl(R^2-r^2\\bigr)\\,dx$. The $r$ is",
         "the inner radius (hole)",
         "Forgetting to square, or subtracting radii before squaring, are the two classic errors.",
         ["the height of the region", "always 1", "the dummy variable"]),
        ("Region between $y=x$ and $y=x^2$ on $[0,1]$, rotated about the $x$-axis, has $R=x$ and $r=x^2$, so $V=\\pi\\int_0^1(x^2-x^4)\\,dx=$",
         "2π/15", "$[x^3/3-x^5/5]_0^1=1/3-1/5=2/15$, times $\\pi$.", ["π/2", "π/5", "2/15"]),
        ("About the $y$-axis, a disk with $x=R(y)$ uses $V=\\pi\\int [R(y)]^2\\,dy$.",
         "true", "Same formula, different independent variable.", ["false — never rotate about y", "only washers exist", "only shells (BC extra)"]),
        ("Rotating $y=1$ and $y=x$ from $x=0$ to $1$ about $y=0$ (x-axis) uses washers with $R=1$, $r=x$. $V=$",
         "2π/3", "$\\pi\\int_0^1(1-x^2)\\,dx=\\pi[x-x^3/3]_0^1=2\\pi/3$.", ["π", "π/3", "1"]),
        ("Volume with known square cross-sections on a base in the $xy$-plane: if the slice’s side is $s(x)$, then $A(x)=$",
         "s(x)^2", "Volume $\\int A(x)\\,dx$.", ["π s^2", "4s", "s/2"]),
        ("Semicircular cross-sections perpendicular to the $x$-axis with diameter $s(x)$ have $A(x)=$",
         "(1/8)π [s(x)]^2",
         "Radius $s/2$, area $\\frac12\\pi (s/2)^2=\\pi s^2/8$.",
         ["π s^2", "π s^2/4", "s^2"]),
        ("Equilateral-triangle cross-sections with side $s$ have area",
         "√3/4 s^2", "Standard geometry, then integrate.", ["s^2", "√3 s^2", "s^2/2"]),
        ("Base is the region under $y=\\sqrt{1-x^2}$ (semicircle radius $1$). Squares perpendicular to the $x$-axis: $s=\\sqrt{1-x^2}$, $V=\\int_{-1}^{1}(1-x^2)\\,dx=$",
         "4/3", "$[x-x^3/3]_{-1}^{1}= (1-1/3)-(-1+1/3)=2/3-(-2/3)=4/3$.", ["π/2", "2", "1"]),
        ("The independent variable of $\\int A$ must match",
         "the direction perpendicular to the slices",
         "If slices are perpendicular to the $x$-axis, integrate $dx$.",
         ["always x", "always y", "always t"]),
        ("Average value of $f$ on $[a,b]$ is",
         "1/(b-a) ∫_a^b f",
         "The height of a rectangle with the same area as the net integral.",
         ["∫ f", "f((a+b)/2)", "f(b)-f(a)"]),
        ("Average of $f(x)=x^2$ on $[0,3]$ is", 3,
         "$\\frac13 \\int_0^3 x^2=\\frac13\\cdot 9=3$.", [9, 1, 4.5]),
        ("MVT for integrals: some $c$ in $(a,b)$ has $f(c)$ equal to",
         "the average value of f",
         "If $f$ is continuous, it attains its average. This is IVT applied to $f$ after FTC.",
         ["f'(c)", "0 always", "f(a)+f(b)"]),
        ("Average velocity on $[a,b]$ is",
         "1/(b-a) ∫_a^b v(t) dt = (s(b)-s(a))/(b-a)",
         "Net change of position over elapsed time.",
         ["v((a+b)/2) always", "max v", "a(b)"]),
        ("If the average of $f$ on $[1,5]$ is $7$, then $\\int_1^5 f=$", 28,
         "Average times length: $7\\cdot 4=28$.", [7, 35, 12]),
        ("An accumulation $G(x)=\\int_0^x r(t)\\,dt$ from a rate $r$ is",
         "net change of the quantity from time 0 to x",
         "Units: rate times time.",
         ["the rate at x", "r'(x)", "always positive"]),
        ("If cars enter a road at $E(t)$ and leave at $L(t)$, the number on the road at time $T$ is",
         "N(0)+∫_0^T (E-L) dt",
         "In minus out, accumulated.",
         ["E(T)-L(T)", "∫ E only", "E'(T)"]),
        ("$G'(x)=r(x)$ by FTC1. A local max of $G$ occurs when $r$ changes",
         "from + to −",
         "First derivative test on the accumulation function.",
         ["from − to +", "r=0 with no sign change", "r''=0"]),
        ("If $r(t)$ is measured in liters/minute, $\\int_0^{10} r$ is in",
         "liters", "Rate times minutes.", ["liters/minute", "minutes", "liters^2"]),
        ("The graph of $G$ is increasing wherever the rate graph is",
         "above the t-axis (r>0)",
         "Same as $f'>0\\Rightarrow f$ increasing, with $f=G$ and $f'=r$.",
         ["below the t-axis", "at a peak of r", "linear"]),
        ("Net change theorem: $\\int_a^b F'(x)\\,dx=$",
         "F(b)−F(a)",
         "FTC2 in application language: total change of $F$.",
         ["F'(b)−F'(a)", "F(a)+F(b)", "0 always"]),
        ("If $s'(t)=v(t)$, displacement on $[2,6]$ is",
         "s(6)−s(2)",
         "Not necessarily distance.",
         ["s(6)+s(2)", "|s(6)|", "v(6)-v(2)"]),
        ("A temperature $H$ has $H'(t)$ given. $H(3)-H(0)=\\int_0^3 H'(t)\\,dt$ is",
         "the net change in temperature over 3 hours",
         "Sign included: a negative integral means a net drop.",
         ["the average temperature", "H'(3)", "always positive"]),
        ("If $F(4)=10$ and $\\int_4^7 F'=-3$, then $F(7)=$", 7,
         "$F(7)=F(4)+\\text{net change}=10-3=7$.", [13, -3, 4]),
        ("Distance versus displacement: distance uses",
         "∫|v| dt",
         "Split at direction changes.",
         ["∫ v dt", "v(b)-v(a)", "s(a)+s(b)"]),
        ("Area between $y=4-x^2$ and $y=x+2$: intersections from $4-x^2=x+2\\Rightarrow x^2+x-2=0\\Rightarrow x=$",
         "-2 and 1", "$(x+2)(x-1)=0$.", ["0 and 2", "±2", "1 only"]),
        ("That area is $\\int_{-2}^{1}\\bigl((4-x^2)-(x+2)\\bigr)\\,dx=\\int_{-2}^{1}(2-x-x^2)\\,dx=$",
         "9/2", "$[2x-x^2/2-x^3/3]_{-2}^{1}=(2-1/2-1/3)-(-4-2+8/3)=7/6-(-10/3)=7/6+20/6=27/6=9/2$.",
         ["4", "3", "6"]),
        ("Washer about $y=0$ for the region under $y=x$ on $[0,1]$ rotated about $y=1$: outer radius $1$, inner radius $1-x$. $V=$",
         "2π/3",
         "$\\pi\\int_0^1\\bigl(1-(1-x)^2\\bigr)\\,dx=\\pi\\int_0^1(2x-x^2)\\,dx=\\pi[x^2-x^3/3]_0^1=2\\pi/3$.",
         ["π/3", "π", "π/2"]),
        ("The washer volume about $y=1$ for $y=x$ on $[0,1]$ is $2\\pi/3$.",
         "2π/3",
         "$\\pi\\int_0^1\\bigl(1-(1-x)^2\\bigr)\\,dx=\\pi\\int_0^1(2x-x^2)\\,dx=\\pi[x^2-x^3/3]_0^1=2\\pi/3$.",
         ["π/3", "π", "π/2"]),
        ("Squares on a base between $y=x$ and $y=2$ from $x=0$ to $2$: $s(x)=2-x$, $V=\\int_0^2(2-x)^2\\,dx=$",
         "8/3", "$u=2-x$, from $2$ to $0$, $\\int_2^0 u^2(-du)=\\int_0^2 u^2=8/3$.", ["4", "2", "8"]),
        ("Average of $\\sin x$ on $[0,\\pi]$ is", "2/π",
         "$\\frac{1}{\\pi}\\int_0^\\pi\\sin x=\\frac{2}{\\pi}$.", [0, 1, "π/2"]),
        ("A rate $r(t)=3t^2$ from $t=1$ to $t=3$ produces net change", 26,
         "$\\int_1^3 3t^2=t^3|_1^3=27-1=26$.", [9, 27, 8]),
        ("If $N'(t)=40-6t$ fish/year, then $N'(2)$ equals", 28,
         "$40-12=28$ fish per year (the rate at that instant, not the net change).",
         [40, 12, 34]),
        ("Net fish change on $[0,4]$ for $N'=40-6t$ is", 112,
         "$\\int_0^4(40-6t)\\,dt=[40t-3t^2]_0^4=160-48=112$.", [64, 160, 48]),
        ("$G(x)=\\int_1^x (t^2-4)\\,dt$ has a local min when $G'=0$ and $G'$ changes $-$ to $+$, i.e. at",
         "x=2 (and not at x=-2 if x≥1)",
         "$G'(x)=x^2-4=(x-2)(x+2)$. On $[1,\\infty)$ the relevant zero is $x=2$.",
         ["x=1", "x=0", "x=4"]),
        ("Disk of $y=e^{-x}$ from $0$ to $1$ about the $x$-axis: $V=\\pi\\int_0^1 e^{-2x}\\,dx=$",
         "π(1−e^{-2})/2",
         "$\\pi\\cdot(-1/2)e^{-2x}|_0^1=\\pi(-1/2)(e^{-2}-1)=\\pi(1-e^{-2})/2$.",
         ["π(e^{-2}-1)", "π/2", "π(1-e^{-1})"]),
        ("Area in $dy$: $x=y^2$ and $x=2-y$ intersect when $y^2+y-2=0$, $y=$",
         "-2 and 1", "$(y+2)(y-1)=0$.", ["0,1", "±1", "2"]),
        ("That $dy$ area is $\\int_{-2}^{1}\\bigl((2-y)-y^2\\bigr)\\,dy=$",
         "9/2", "Same region as a previous $x$-integral can look; compute $[2y-y^2/2-y^3/3]_{-2}^{1}= (2-1/2-1/3)-(-4-2+8/3)=9/2$.",
         ["4", "2", "1"]),
        ("Cross-sections are rectangles of height $3$ and width $s(x)$. Then $A(x)=$",
         "3 s(x)", "Area of a rectangle.", ["s(x)^2", "3π s^2", "s/3"]),
        ("If water flows in at $12$ gal/min and out at $3t$ gal/min, net gallons from $0$ to $4$ min is",
         24,
         "$\\int_0^4(12-3t)\\,dt=[12t-3t^2/2]_0^4=48-24=24$.",
         [12, 48, 0]),
        ("AP Stretch: Region bounded by $y=x^2$ and $y=2x$, rotated about the $x$-axis. Washer: $R=2x$, $r=x^2$ on $[0,2]$. $V=\\pi\\int_0^2\\bigl(4x^2-x^4\\bigr)\\,dx=$",
         "64π/15",
         "$\\pi[4x^3/3-x^5/5]_0^2=\\pi(32/3-32/5)=\\pi\\cdot 32\\cdot(5-3)/15=64\\pi/15$.",
         ["8π", "32π/5", "16π/3"]),
        ("AP Stretch: The region bounded by $y=x^2$ and $y=2x$ is rotated about $y=4$. Washers on $x\\in[0,2]$ have outer radius $4-x^2$ and inner radius $4-2x$. The volume equals",
         "32π/5",
         "$(4-x^2)^2-(4-2x)^2=x^4-12x^2+16x$. Then $\\pi[x^5/5-4x^3+8x^2]_0^2=\\pi(32/5-32+32)=32\\pi/5$.",
         ["64π/15", "8π", "16π/3"]),
        ("AP Stretch: The region between $y=e^{x}$ and $y=1$ from $x=0$ to $x=1$ is rotated about the $x$-axis. Washer volume $\\pi\\int_0^1\\bigl(e^{2x}-1\\bigr)\\,dx$ equals",
         "π(e^2 − 3)/2",
         "$\\pi\\bigl[\\frac12 e^{2x}-x\\bigr]_0^1=\\pi\\bigl((e^2/2-1)-1/2\\bigr)=\\pi(e^2-3)/2$.",
         ["π(e^2-1)", "π(e-1)", "π/2"]),
        ("AP Stretch: Squares perpendicular to the $x$-axis on the base between $y=\\sqrt{x}$ and $y=x/2$ on $[0,4]$. $s(x)=\\sqrt{x}-x/2$, $V=\\int_0^4 s(x)^2\\,dx$. Expanding $s^2=x-x^{3/2}+x^2/4$, the integral equals",
         "8/15",
         "$[x^2/2-\\frac25 x^{5/2}+x^3/12]_0^4=8-\\frac25\\cdot 32+64/12=8-12.8+16/3=-4.8+5.333=8/15$. Check: $8-64/5+16/3=(120-192+80)/15=8/15$.",
         ["4/3", "1", "2"]),
        ("AP Stretch: Average value of $f(x)=1/(1+x)$ on $[0,e-1]$ is",
         "1/(e-1)",
         "$\\frac{1}{e-1}\\int_0^{e-1}\\frac{1}{1+x}\\,dx=\\frac{\\ln(1+x)}{e-1}\\Big|_0^{e-1}=\\frac{\\ln e-\\ln 1}{e-1}=\\frac{1}{e-1}$.",
         ["1", "e-1", "ln(e-1)"]),
        ("AP Stretch: In/out FRQ: $E(t)=40+2t$ and $L(t)=4t$ on $[0,10]$, $N(0)=100$. $N(10)=$",
         "400",
         "$N(10)=100+\\int_0^{10}(40+2t-4t)\\,dt=100+[40t-t^2]_0^{10}=100+400-100=400$.",
         ["100", "500", "300"]),
        ("AP Stretch: Cars enter a plaza at $E(t)=6$ and leave at $L(t)=2t$ vehicles per minute on $0\\le t\\le 4$, with $N(0)=10$. Then $N'(t)=6-2t$. The maximum of $N$ on $[0,4]$ is",
         19,
         "$N'=0$ at $t=3\\in(0,4)$. $N(3)=10+\\int_0^3(6-2t)\\,dt=10+[6t-t^2]_0^3=19$. Compare $N(0)=10$ and $N(4)=18$. The max is $19$.",
         [10, 18, 24]),
        ("AP Stretch: Net change of $F(x)=\\ln(x^2+1)$ on $[0,\\sqrt{e-1}]$ equals $\\int_0^{\\sqrt{e-1}} F'(x)\\,dx=$",
         1,
         "$F(\\sqrt{e-1})-F(0)=\\ln(e-1+1)-\\ln 1=1$.",
         ["0", "e", "ln 2"]),
        ("AP Stretch: Washer + two functions about the $y$-axis: $x=y^2$, $x=2y$, $y\\in[0,2]$. $R=2y$, $r=y^2$, $V=\\pi\\int_0^2\\bigl(4y^2-y^4\\bigr)\\,dy=$",
         "64π/15",
         "$\\pi[4y^3/3-y^5/5]_0^2=\\pi(32/3-32/5)=64\\pi/15$ (same arithmetic as an earlier $x$-washer with roles swapped).",
         ["8π", "32π/3", "4π"]),
        ("AP Stretch: Region between $y=x$ and $y=\\sqrt{x}$ on $[0,1]$, rotated about $x=2$. Washers in $y$: $R=2-y^2$, $r=2-y$. $V=\\pi\\int_0^1\\bigl[(2-y^2)^2-(2-y)^2\\bigr]\\,dy=$",
         "8π/15",
         "Expand: $y^4-5y^2+4y$. Antiderivative $y^5/5-5y^3/3+2y^2$ at $1$ is $1/5-5/3+2=8/15$. Times $\\pi$.",
         ["π/2", "4π/3", "8π"]),
    ])


def build_unit6():
    title = "AP Calculus AB Unit 6: Applications of Integration"
    description = (
        "Area between curves, volumes by disks, washers, and known cross-sections, average value, "
        "accumulation from rates, and the net change theorem."
    )
    concepts = [
        "Area between curves",
        "Volume disks/washers",
        "Volume known cross-sections",
        "Average value",
        "Accumulation functions",
        "Net change theorem",
    ]

    c1 = concept_block(
        "1. Area between curves",
        [
            "The area of the region between $y=f(x)$ and $y=g(x)$ on $[a,b]$ with $f\\ge g$ is $\\int_a^b\\bigl(f(x)-g(x)\\bigr)\\,dx$. The integrand is a height; $dx$ is a width.",
            "Find intersections by solving $f=g$; those $x$-values are typically the limits. If the curves cross inside the interval, split so that top-minus-bottom stays nonnegative on each piece.",
            "In $dy$, the integrand is right minus left. Some regions (a sideways parabola cut by a line) are one integral in $y$ and two in $x$.",
            "Area is never negative. If your calculator returns a negative number, you subtracted the wrong way or did not split.",
            "Sketch even a sloppy graph. Label which curve is top. An AP area FRQ without a sketch is how students integrate $x^2-x$ instead of $x-x^2$ on $[0,1]$.",
            "Units: if $x$ and $y$ are meters, area is square meters. Name them on an applied sketch.",
        ],
        "This is the template for every later volume integrand: a cross-sectional length built from top-minus-bottom, then squared or otherwise converted into area.",
        "Intersections, sketch, top minus bottom, integrate, units. If the sketch and the integrand disagree, trust the sketch and fix the integrand.",
        lesson_figure(
            _area_between_svg(),
            "Region between $y=\\sqrt{x}$ and $y=x/2$ on $[0,4]$",
            "The vertical strip has height $\\sqrt{x}-x/2$. Integrating that height from the two intersection points yields area.",
        )
        + solved(
            1,
            "Area between $y=x$ and $y=0$ on $[0,2]$.",
            ["Triangle area $\\frac12\\cdot 2\\cdot 2=2$, or $\\int_0^2 x\\,dx=2$."],
            "$2$", "", "Easy",
        )
        + solved(
            2,
            "Area between $y=x$ and $y=x^2$ on $[0,1]$.",
            ["Intersections $0,1$. Top is $y=x$.", "$\\int_0^1(x-x^2)\\,dx=[x^2/2-x^3/3]_0^1=1/6$."],
            "$\\dfrac{1}{6}$", "", "Medium",
        )
        + solved(
            3,
            "Area between $y=\\sqrt{x}$ and $y=x/2$.",
            [
                "Solve $\\sqrt{x}=x/2$: $x=0$ or $x=4$ (square both sides after $2\\sqrt{x}=x$ for $x>0$).",
                "$\\int_0^4(\\sqrt{x}-x/2)\\,dx=[\\frac23 x^{3/2}-x^2/4]_0^4=\\frac23\\cdot 8-4=4/3$.",
            ],
            "$\\dfrac{4}{3}$", "The figure’s shaded region is exactly this integral.", "Honors",
        ),
        ("Integrating bottom minus top and dropping the absolute value",
         "On $[0,1]$, $\\int(x^2-x)$ is negative. Area is $1/6$, not $-1/6$. Sketch first."),
        ("Find intersections on paper before you write the limits",
         "Wrong limits are the most expensive arithmetic-free error in an area FRQ."),
        ["I subtract top minus bottom.", "I split at crossings.", "I can switch to dy when it is simpler."],
        1,
    )

    c2 = concept_block(
        "2. Volumes by disks and washers",
        [
            "A disk is a washer with inner radius zero. Revolving a radius $R(x)$ about the $x$-axis produces $A(x)=\\pi[R(x)]^2$, hence $V=\\pi\\int_a^b [R(x)]^2\\,dx$.",
            "A washer has outer radius $R$ and inner radius $r$ (the hole). $A=\\pi(R^2-r^2)$. Square first, then subtract. Never $\\pi(R-r)^2$.",
            "The axis of rotation decides whether you integrate $dx$ or $dy$ and how you measure radii (perpendicular distance from the axis to the curve).",
            "If you rotate about $y=k$ instead of the $x$-axis, radii become $|y_{\\text{curve}}-k|$ expressed as functions of $x$.",
            "Sketch the 2D region, mark the axis, draw one washer, label $R$ and $r$ in terms of the curves, then integrate.",
            "AB does not require cylindrical shells, though a student who knows them may use them if the setup is correct. Disks/washers are the expected method.",
        ],
        "Washer FRQs are a staple of AB. The calculus is easy; the geometry of $R$ and $r$ is the test.",
        "One representative washer on the sketch, with $R$ and $r$ labeled as distances to the axis. Then square, subtract, multiply by $\\pi$, integrate.",
        lesson_figure(
            _washer_svg(),
            "Region between $y=x$ and $y=x^2$ on $[0,1]$, rotated about the $x$-axis",
            "A slice perpendicular to the axis is a washer: outer radius $x$, inner radius $x^2$. The small annulus sketch on the right is that slice.",
        )
        + solved(
            1,
            "Volume of the solid from $y=\\sqrt{x}$, $0\\le x\\le 4$, rotated about the $x$-axis.",
            ["Disks: $R=\\sqrt{x}$.", "$V=\\pi\\int_0^4 x\\,dx=8\\pi$."],
            "$8\\pi$", "", "Easy",
        )
        + solved(
            2,
            "Region between $y=x$ and $y=x^2$ on $[0,1]$, about the $x$-axis.",
            ["$R=x$, $r=x^2$.", "$V=\\pi\\int_0^1(x^2-x^4)\\,dx=\\pi[x^3/3-x^5/5]_0^1=2\\pi/15$."],
            "$\\dfrac{2\\pi}{15}$", "Square each radius separately.", "Medium",
        )
        + solved(
            3,
            "The same region about the line $y=1$.",
            [
                "On $[0,1]$, $x^2\\le x\\le 1$, so $x^2$ is farther from the line $y=1$. Outer radius $1-x^2$, inner radius $1-x$.",
                "$V=\\pi\\int_0^1\\bigl[(1-x^2)^2-(1-x)^2\\bigr]\\,dx$.",
                "Expand: $(1-2x^2+x^4)-(1-2x+x^2)=x^4-3x^2+2x$.",
                "$\\pi[x^5/5-x^3+x^2]_0^1=\\pi(1/5-1+1)=\\pi/5$.",
            ],
            "$\\dfrac{\\pi}{5}$", "Measure radii to the axis $y=1$, not to the $x$-axis.", "Honors",
        ),
        ("Writing π(R−r)^2",
         "That is the area of a disk of radius $R-r$, not a washer. Expand $R^2-r^2$ as a difference of squares after each radius is written."),
        ("Label R and r on the 2D sketch before integrating",
         "If you cannot point to each radius as a segment perpendicular to the axis, the integral is not ready."),
        ["I square radii before subtracting.", "I measure distance to the actual axis.", "I can switch to dy for a y-axis rotation."],
        6,
    )

    c3 = concept_block(
        "3. Volumes with known cross-sections",
        [
            "If every cross-section perpendicular to the $x$-axis is a known shape with area $A(x)$, the volume is $\\int_a^b A(x)\\,dx$. No $\\pi$ unless the shape is a circle or semicircle.",
            "The base lives in the $xy$-plane. The side length $s(x)$ of the slice is usually top minus bottom of that base.",
            "Squares: $A=s^2$. Equilateral triangles: $A=\\dfrac{\\sqrt{3}}{4}s^2$. Semicircles with diameter $s$: $A=\\dfrac{\\pi}{8}s^2$. Rectangles of fixed height $h$: $A=h s$.",
            "Perpendicular to the $y$-axis means $s=s(y)$ and $\\int A(y)\\,dy$. Read the prompt’s “perpendicular to” line twice.",
            "These solids are not solids of revolution. Do not insert $\\pi$ out of habit.",
            "A tiny 3D sketch of one slice standing on the base prevents using the wrong $s(x)$.",
        ],
        "AP uses this to test whether you understand $V=\\int A$ in general, not only for washers. The geometry of $A(x)$ is the entire problem.",
        "Write $s(x)=$ top $-$ bottom, then $A(x)=$ the shape formula, then integrate. Three formulas, one integral.",
        lesson_figure(
            _cross_section_svg(),
            "A square slice standing on a base in the $xy$-plane",
            "The side of the square is the segment across the base. Volume stacks those squares along the axis perpendicular to the slices.",
        )
        + solved(
            1,
            "Base is the region under $y=1-x$ from $x=0$ to $1$. Squares perpendicular to the $x$-axis. Find $V$.",
            ["$s=1-x$, $A=(1-x)^2$.", "$V=\\int_0^1(1-x)^2\\,dx=1/3$."],
            "$\\dfrac{1}{3}$", "", "Easy",
        )
        + solved(
            2,
            "Same base, semicircles with diameter on the base, perpendicular to the $x$-axis.",
            ["$A=\\pi s^2/8=\\pi(1-x)^2/8$.", "$V=\\dfrac{\\pi}{8}\\cdot\\dfrac13=\\pi/24$."],
            "$\\dfrac{\\pi}{24}$", "", "Medium",
        )
        + solved(
            3,
            "Base between $y=x$ and $y=2$ from $x=0$ to $2$, equilateral triangles perpendicular to the $x$-axis.",
            [
                "$s=2-x$, $A=\\dfrac{\\sqrt{3}}{4}(2-x)^2$.",
                "$V=\\dfrac{\\sqrt{3}}{4}\\int_0^2(2-x)^2\\,dx=\\dfrac{\\sqrt{3}}{4}\\cdot\\dfrac{8}{3}=\\dfrac{2\\sqrt{3}}{3}$.",
            ],
            "$\\dfrac{2\\sqrt{3}}{3}$", "No $\\pi$: these are triangles, not disks.", "Honors",
        ),
        ("Putting π into a square-cross-section volume",
         "π is for circular slices. Squares use $s^2$ only. Read the shape word."),
        ("Identify the perpendicular axis, then write s as a function of that variable",
         "If slices are perpendicular to the $y$-axis, a formula $s(x)$ is the wrong variable."),
        ["I write A(x) from the named shape.", "I get s from the base.", "I omit π unless the slice is circular."],
        11,
    )

    avg_fig = xy_graph(
        curves=[("#4f46e5", sample_curve(lambda x: 0.25 * x * x + 0.5, 0, 4))],
        dashes=[("h", 1.833, "f_avg")],
        xlim=(-0.3, 4.4), ylim=(-0.3, 5), w=300, h=240,
    )

    c4 = concept_block(
        "4. Average value of a function",
        [
            "The average value of a continuous $f$ on $[a,b]$ is $f_{\\mathrm{avg}}=\\dfrac{1}{b-a}\\int_a^b f(x)\\,dx$. It is the height of a rectangle with the same net area as the graph.",
            "This is not the average of $f(a)$ and $f(b)$ unless $f$ is linear. For $x^2$ on $[0,1]$ the average is $1/3$, not $1/2$.",
            "If $f$ is a velocity, $f_{\\mathrm{avg}}$ is average velocity, which equals $(s(b)-s(a))/(b-a)$ by FTC2 — recovering the MVT secant slope.",
            "The Mean Value Theorem for integrals: a continuous $f$ attains its average value, so some $c\\in(a,b)$ has $f(c)=f_{\\mathrm{avg}}$. Existence, not a formula for $c$.",
            "Units of $f_{\\mathrm{avg}}$ match units of $f$. The factor $1/(b-a)$ cancels the extra unit of $x$ from the integral.",
            "On a calculator AB question, you may compute the integral numerically, then divide by $b-a$. Still show the average-value formula.",
        ],
        "Average value converts an integral back into the original units of $f$, which is exactly what applied rate problems need when they ask for an average rate.",
        "Write $\\dfrac{1}{b-a}\\int_a^b f$ before you compute. That displayed formula is often its own rubric point.",
        lesson_figure(
            avg_fig,
            "A curve and a dashed horizontal line at the average height",
            "The rectangle of height $f_{\\mathrm{avg}}$ has the same area as the region under the curve. That is the definition, not a coincidence.",
        )
        + solved(
            1,
            "Average of $f(x)=3$ on $[1,5]$.",
            ["Constant function: the average is $3$.", "Formula: $\\frac14\\int_1^5 3=3$."],
            "$3$", "", "Easy",
        )
        + solved(
            2,
            "Average of $x^2$ on $[0,3]$.",
            ["$\\frac13\\int_0^3 x^2\\,dx=\\frac13\\cdot 9=3$."],
            "$3$", "Not $4.5$, the midpoint value $f(1.5)=2.25$, nor $f(3)/2$.", "Medium",
        )
        + solved(
            3,
            "Average of $\\sin x$ on $[0,\\pi]$, and name a $c$ guaranteed by the integral MVT.",
            [
                "$\\frac{1}{\\pi}\\int_0^\\pi\\sin x=\\frac{2}{\\pi}$.",
                "Solve $\\sin c=2/\\pi$, $c=\\arcsin(2/\\pi)\\in(0,\\pi)$.",
            ],
            "$2/\\pi$, with $c=\\arcsin(2/\\pi)$ (and $\\pi$ minus that)", "", "Honors",
        ),
        ("Averaging the endpoints instead of integrating",
         "$(f(a)+f(b))/2$ is the trapezoid with $n=1$, not the average value, unless $f$ is linear."),
        ("Display 1/(b−a) times the integral",
         "Then compute. Students who only compute $\\int f$ leave the answer in the wrong units and lose the average-value point."),
        ["I use 1/(b−a) ∫ f.", "I know the integral MVT guarantees a c.", "I can interpret average velocity as this formula."],
        16,
    )

    c5 = concept_block(
        "5. Accumulation functions",
        [
            "If $r(t)$ is a rate, $G(x)=G(x_0)+\\int_{x_0}^x r(t)\\,dt$ accumulates net change. FTC1 says $G'(x)=r(x)$ (at a variable upper limit).",
            "In/out problems: $N(T)=N(0)+\\int_0^T\\bigl(E(t)-L(t)\\bigr)\\,dt$. The integrand is net rate; the integral is net people, gallons, or degrees.",
            "Where $r>0$, $G$ increases. Where $r=0$ and $r$ changes $+$ to $-$, $G$ has a local max. This is Unit 3 language on an integral-defined function.",
            "Units: if $r$ is liters per minute and $t$ is minutes, $G$ is liters. Write that sentence on the FRQ.",
            "A graph of $r$ lets you compute $G$ as signed area and sketch $G$ without a formula for $r$.",
            "Do not confuse $G(x)$ with $r(x)$. One is a quantity, the other is a rate. The question “when is the amount a maximum?” is about $G$, answered with $r$’s sign chart.",
        ],
        "This is the modern AP “rate in / rate out” FRQ. Students who treat $E(t)-L(t)$ as the amount instead of the rate lose the interpretation points.",
        "Name the quantity, name the rate, write $N(T)=N(0)+\\int(E-L)$. Then FTC1 or a sign chart as asked.",
        lesson_figure(
            _accum_svg(),
            "A rate graph $v(t)$ with net area from $0$ to $t$ equal to displacement",
            "The accumulation function is the running signed area. Its derivative is the original rate curve.",
        )
        + solved(
            1,
            "If $r(t)=4$ liters/min, how much accumulates from $t=0$ to $t=5$?",
            ["$\\int_0^5 4\\,dt=20$ liters."],
            "$20$ liters", "", "Easy",
        )
        + solved(
            2,
            "$E(t)=10$, $L(t)=2t$, $N(0)=50$. Find $N(5)$.",
            ["$N(5)=50+\\int_0^5(10-2t)\\,dt=50+[10t-t^2]_0^5=50+50-25=75$."],
            "$75$", "", "Medium",
        )
        + solved(
            3,
            "For $N'(t)=10-2t$ on $[0,8]$, when is $N$ maximized?",
            [
                "$N'=0$ at $t=5$. Sign $+$ then $-$.",
                "Local (and, on $[0,8]$, absolute) max at $t=5$.",
                "$N(5)=50+\\int_0^5(10-2t)=75$ if $N(0)=50$.",
            ],
            "maximum at $t=5$", "First derivative test on the accumulation.", "Honors",
        ),
        ("Answering with the rate when the question asked for the amount",
         "$E(3)-L(3)$ is how fast the amount is changing at $t=3$, not how much is there. Amount needs an integral plus an initial condition."),
        ("Keep a units dictionary on the page: r in stuff/time, ∫r in stuff",
         "That dictionary is an AP communication point and a self-check."),
        ["I add ∫(in−out) to the initial amount.", "I use r’s sign chart to max the amount.", "I report units of the quantity."],
        21,
    )

    c6 = concept_block(
        "6. Net change theorem",
        [
            "The net change theorem is FTC2 in English: $\\int_a^b F'(x)\\,dx=F(b)-F(a)$. The integral of a rate is the net change of the quantity.",
            "Displacement is net change of position. Total distance is $\\int|v|$. Temperature change is $\\int H'$. Volume pumped is $\\int r$ when $r$ is a flow rate.",
            "Given $F(a)$ and a rate, $F(b)=F(a)+\\int_a^b F'$. That one-line rearrangement is how you recover a function value from a rate table plus an initial condition.",
            "Sign is information: a negative net change means the quantity fell. Do not abs-value unless the prompt asked for total variation or distance.",
            "If $F'$ changes sign, net change can be small while a lot of stuff moved both ways. The prompt’s wording (net vs total) decides the integral.",
            "This theorem unifies PVA, accumulation, and FTC2. On mixed review you should recognize all three names for the same fact.",
        ],
        "Almost every applied definite-integral sentence on AB is this theorem. If you only remember “area under a curve,” you will miss the units and the initial-condition structure.",
        "Translate the English into $\\int_a^b(\\text{rate})\\,dt=\\text{net change}$, then decide whether the prompt wanted net or total.",
        lesson_figure(
            _accum_svg(),
            "Net area of a velocity graph is displacement — the net change of position",
            "The theorem does not care whether you call the integrand $v$, $F'$, or $r$. The integral is still $F(b)-F(a)$.",
        )
        + solved(
            1,
            "$F'(x)=3$, $F(1)=4$. Find $F(5)$.",
            ["$F(5)=4+\\int_1^5 3\\,dx=4+12=16$."],
            "$16$", "", "Easy",
        )
        + solved(
            2,
            "$v(t)=4-t$ on $[0,6]$, $s(0)=2$. Find $s(6)$ and distance traveled.",
            [
                "$s(6)=2+\\int_0^6(4-t)\\,dt=2+[4t-t^2/2]_0^6=2+24-18=8$.",
                "Rest at $t=4$. Distance $\\int_0^4(4-t)+\\int_4^6(t-4)=8+2=10$.",
            ],
            "$s(6)=8$; distance $10$", "", "Medium",
        )
        + solved(
            3,
            "A tank has $30$ L. Water leaks at $3t$ L/min. How much is left after $4$ min, and is the answer net change applied correctly?",
            [
                "Net change of volume $=\\int_0^4 -3t\\,dt= -\\frac32 t^2|_0^4=-24$ L.",
                "Left: $30-24=6$ L.",
                "If the leak rate had exceeded the contents, you would also need a physical domain (tank empty).",
            ],
            "$6$ L remain", "The integral of a negative rate is a negative net change.", "Honors",
        ),
        ("Using ∫|F'| when the question asked for net change",
         "Net change keeps the sign. Total variation / distance / “how much water flowed in total” needs the absolute value and a split."),
        ("Write F(b)=F(a)+∫_a^b F' with names filled in",
         "That sentence is the entire net-change FRQ. Then compute."),
        ["I translate English into ∫ rate = net change.", "I can recover F(b) from F(a) and a rate.", "I split |v| for distance."],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u6_questions()


# ===========================================================================
# UNIT 7: Differential Equations
# ===========================================================================

def _u7_questions():
    return _pack([
        ("A slope field for $dy/dx=x$ has, at the point $(2,3)$, a tick of slope",
         2, "The right-hand side depends only on $x$ here: $m=2$. The $y$-coordinate does not affect the slope.",
         [3, 1, 0]),
        ("On the slope field of $dy/dx=y$, ticks along the $x$-axis ($y=0$) are",
         "horizontal (slope 0)",
         "$m=y=0$. The zero solution is an equilibrium line of horizontal ticks.",
         ["vertical", "slope 1", "undefined"]),
        ("A solution curve through a point must be",
         "tangent to the slope-field tick at that point",
         "That is how you sketch particular solutions without a formula.",
         ["perpendicular to every tick", "a straight line always", "a circle"]),
        ("If $dy/dx$ does not depend on $y$, then ticks in a vertical line (fixed $x$) are",
         "all parallel (same slope)",
         "Isoclines of constant $x$ are vertical lines for autonomous-in-$y$-missing DEs of the form $y'=f(x)$.",
         ["all horizontal", "random", "circles"]),
        ("A slope field is a picture of",
         "the DE’s slope at sample points, not a single solution",
         "Infinitely many solutions (a family) can be drawn on one field.",
         ["the second derivative only", "a Riemann sum", "a tangent line at one point only"]),
        ("A separable DE can be written $\\dfrac{dy}{dx}=g(x)h(y)$. The method is",
         "dy/h(y) = g(x) dx, then integrate both sides",
         "Provided $h(y)\\neq 0$. Check constant solutions $h(y)=0$ separately.",
         ["differentiate both sides", "use L'Hôpital", "take dy/dx = g/h"]),
        ("Solve $dy/dx=2x$ with no initial condition. $y=$",
         "x^2+C", "Separate (already in $x$ only) and integrate.", ["2+C", "2x+C", "x^2"]),
        ("$dy/dx=y$ (for $y>0$) separates as $dy/y=dx$, so $\\ln y=x+C_1$ and $y=$",
         "Ce^x", "$C=e^{C_1}>0$ here; allowing $C\\in\\mathbb{R}$ captures $y=0$ and negatives.",
         ["e^x+C", "x+C", "ln x"]),
        ("The constant solution of $y'=y(y-2)$ is found by",
         "setting y=0 or y=2 (equilibria)",
         "If $h(y)=0$, then $y'=0$ so $y$ is constant.",
         ["setting y'=1", "L'Hôpital", "MVT"]),
        ("$dy/dx=3/y$ with $y(0)=2$: $\\frac12 y^2=3x+C$. Then $C=$",
         2, "At $(0,2)$: $2=C$. So $y^2=6x+4$.", [0, 3, 4]),
        ("Exponential growth $y'=ky$ with $k>0$ has solutions",
         "y=y0 e^{kt}",
         "Separate, integrate, apply $y(0)=y_0$.",
         ["y=kt+y0", "y=k^t", "y=y0 / k"]),
        ("Half-life is the time $T$ with $y(T)=y_0/2$ for $y=y_0 e^{kt}$ ($k<0$). Then $T=$",
         "ln(1/2)/k  (or ln 2 / |k|)",
         "Take ln: $kT=\\ln(1/2)$.",
         ["k/2", "1/2", "y0/2"]),
        ("If a population doubles every $5$ years and $y'=ky$, then $k=$",
         "(ln 2)/5", "$e^{5k}=2$.", ["2/5", "5 ln 2", "ln 5"]),
        ("Newton’s law of cooling is a DE of the form",
         "dT/dt = k(T−T_a)",
         "Separable. Solutions exponentially approach ambient $T_a$.",
         ["T''=0", "dT/dt=T_a", "T=kt"]),
        ("For $y=50e^{-0.2t}$, $y'(0)=$", -10,
         "$y'=-0.2\\cdot 50e^{-0.2t}$, at $0$ is $-10$. Units: quantity per time.",
         [50, -0.2, 10]),
        ("A particular solution is a member of the family selected by",
         "an initial condition y(x0)=y0",
         "That pins down $C$.",
         ["the slope field alone with no point", "MVT", "a Riemann sum"]),
        ("$y'=2x$, $y(1)=4$. Then $y=$", "x^2+3",
         "$y=x^2+C$, $4=1+C$, $C=3$.", ["x^2+4", "2x+2", "x^2"]),
        ("$y'=y$, $y(0)=3$. Then $y=$", "3e^x",
         "$y=Ce^x$, $C=3$.", ["e^x+3", "3x", "e^{3x}"]),
        ("$y'=1/x$ for $x>0$, $y(1)=0$. Then $y=$",
         "ln x", "$y=\\ln x+C$, $0=0+C$.", ["1/x", "x", "ln|x|+1"]),
        ("Two different initial conditions for the same first-order DE typically produce",
         "two different particular solutions (often non-intersecting)",
         "Uniqueness theorems say graphs of solutions do not cross where the hypotheses hold.",
         ["the same C", "no solution", "a circle"]),
        ("On a slope field, a solution through $(1,2)$ is sketched by",
         "starting at (1,2) and following the ticks",
         "Short segments, staying tangent to nearby marks.",
         ["connecting random ticks", "drawing y=2", "drawing x=1"]),
        ("If every tick on $y=3$ is horizontal, then $y=3$ is",
         "an equilibrium solution",
         "$y'=0$ along that line, so the constant function $y=3$ solves the DE.",
         ["not a solution", "a vertical asymptote", "an inflection of every solution"]),
        ("Ticks that get steeper as you move up suggest $y'$ increases with",
         "y (for example y'=y or y'=y^2)",
         "Read the field qualitatively when no formula is given.",
         ["x only", "time only in a table of t", "second derivatives only"]),
        ("A solution that appears to approach a horizontal line as $x\\to\\infty$ is approaching",
         "an equilibrium (stable, if nearby solutions also approach it)",
         "Exponential decay to a carrying value looks like this on a field.",
         ["a VA", "a hole", "f'=DNE"]),
        ("You cannot conclude uniqueness from a slope field picture alone if",
         "ticks are missing in a region or the field looks inconsistent",
         "The picture is a sample. Still, AP asks you to reason from the given ticks.",
         ["there are many ticks", "the DE is separable", "an initial point is given"]),
        ("To verify $y=x^3$ solves $y'=3x^2$ with $y(1)=1$, check",
         "both the DE and the initial condition",
         "Differentiate: $y'=3x^2$ matches. $1^3=1$ matches.",
         ["only y(1)=1", "only that y is a polynomial", "IVT"]),
        ("Does $y=e^{2x}$ solve $y'=2y$?",
         "yes: y'=2e^{2x}=2y",
         "Substitute both $y$ and $y'$ into the DE.",
         ["no, because of the 2", "only if C=0", "only at x=0"]),
        ("Does $y=x^{-1}$ solve $xy'+y=0$ on $x>0$?",
         "yes: y'=-x^{-2}, so x(-1/x^2)+1/x=0",
         "Plug in. Domain $x\\neq 0$ must be stated.",
         ["no", "only for x<0", "only with +C"]),
        ("$y=\\cos x$ fails $y'+y=0$ because",
         "−sin x + cos x is not identically 0",
         "Verification is substitution, not a vibe.",
         ["cos x is not differentiable", "y(0)≠0", "trig is illegal in DEs"]),
        ("If $y=Ce^{-t}$ solves $y'=-y$, the particular solution with $y(0)=5$ is",
         "5e^{-t}", "$C=5$.", ["e^{-t}+5", "5-t", "e^{-5t}"]),
        ("At $(−1,4)$ on $y'=x+y$, the slope is", 3, "$-1+4=3$.", [4, -1, 0]),
        ("Which DE has all ticks depending only on $y$: $y'=2y$, $y'=x^2$, or $y'=x-y$?",
         "y'=2y",
         "Autonomous: $y'=f(y)$. Horizontal isoclines.",
         ["y'=x^2", "y'=x-y", "none of them"]),
        ("Separable: $dy/dx=x/y$, $y(0)=2$. Then $y^2/2=x^2/2+C$, $C=2$, so $y=$",
         "√(x^2+4)  (positive branch)",
         "$y(0)=2>0$ selects the positive square root.",
         ["x^2+4", "−√(x^2+4)", "x+2"]),
        ("Growth: $200$ bacteria, $k=0.3$ per hour, $y=200e^{0.3t}$. After $4$ hours, $y=$",
         "200e^{1.2}", "Do not convert to a decimal unless a calculator section asks.",
         ["800", "200+1.2", "e^{0.3}"]),
        ("Decay: $y=y_0 e^{kt}$, $y(3)=y_0/4$. Then $k=$",
         "ln(1/4)/3", "$3k=\\ln(1/4)=\\ln 1-\\ln 4=-2\\ln 2$, so $k=-(2\\ln 2)/3$.",
         ["4/3", "-4", "ln 4"]),
        ("$y'=2y+6=2(y+3)$. Let $u=y+3$, then $u'=2u$, $u=Ce^{2x}$, so $y=$",
         "Ce^{2x}-3", "Equilibrium $y=-3$.", ["Ce^{2x}+3", "2x-3", "e^{2x}"]),
        ("Particular: $y'=2y+6$, $y(0)=1$. Then $C-3=1$, $C=4$, $y=$",
         "4e^{2x}-3", "Check: $y(0)=4-3=1$, $y'=8e^{2x}=2(4e^{2x}-3+3)=2(y+3)$.",
         ["e^{2x}-3", "4e^{2x}+3", "4x-3"]),
        ("From a slope field for $y'=1-y$, solutions with $y(0)>1$ appear to",
         "decrease toward y=1",
         "$y'>0$ below $1$, $y'<0$ above $1$, so $y=1$ is attracting.",
         ["increase without bound", "hit a VA immediately", "stay at y=0"]),
        ("Verify $y=x\\ln x$ on $(0,\\infty)$ for $xy'-y=x$: $y'=\\ln x+1$, so $x(\\ln x+1)-x\\ln x=$",
         "x", "Simplifies to $x$, matching the right-hand side.",
         ["0", "ln x", "1"]),
        ("The solution of $y'=3x^2$, $y(0)=5$ is a particular",
         "cubic: y=x^3+5",
         "Family $x^3+C$, then $C=5$.",
         ["y=3x^2+5", "y=6x+5", "y=5e^{3x}"]),
        ("A slope field for $y'=-x/y$ (circles) has ticks perpendicular to",
         "the radius from the origin (so solutions are circles)",
         "$y'=-x/y$ is the circle family $x^2+y^2=C$.",
         ["the x-axis only", "every horizontal", "Riemann rectangles"]),
        ("$dy/dx=e^{x-y}$. Separate: $e^y dy=e^x dx$. Integrate: $e^y=e^x+C$. If $y(0)=0$, $C=$",
         0, "$1=1+C$. So $y=x$ (since $e^y=e^x$).", [1, -1, "e"]),
        ("For $y=x$ as that particular solution, $y'=1$ and $e^{x-y}=e^0=1$, so verification",
         "succeeds", "Both sides equal $1$.", ["fails", "needs L'Hôpital", "needs a washer"]),
        ("If $y'=k y$ and $y$ is in milligrams, $t$ in hours, then $k$ has units",
         "1/hour", "So that $ky$ has units mg/h.", ["mg", "hours", "mg·hour"]),
        ("A student writes $y=e^{x+C}$ instead of $Ce^x$ for $y'=y$. These are",
         "the same family (reparametrizing C=e^C_old, plus y=0 separately)",
         "AP accepts $Ce^x$ as the standard form.",
         ["completely different DEs", "only valid for x>0", "invalid"]),
        ("AP Stretch: The DE $x+y y'=0$ with $y(3)=-4$. Implicitly $x^2+y^2=C$. Then $C=$",
         25, "$9+16=25$. The particular solution is the circle $x^2+y^2=25$, lower semicircle $y=-\\sqrt{25-x^2}$ near $x=3$.",
         [7, 12, 0]),
        ("AP Stretch: The DE $x+y y'=0$ with $y(3)=-4$. Separating gives $x\\,dx+y\\,dy=0$, so $x^2+y^2=C$. The particular solution near $(3,-4)$ is",
         "y=−√(25−x^2)",
         "$C=9+16=25$. The negative square root matches $y(3)=-4$. Domain $|x|\\le 5$.",
         ["y=√(25−x^2)", "y=−4", "y=25-x^2"]),
        ("AP Stretch: $y'=y/x$ on $x>0$, $y(1)=2$. Separate $dy/y=dx/x$, $\\ln|y|=\\ln x+C$. Then $y=$",
         "2x",
         "$y=Ax$ with $A=2$. (Homogeneous linear; solutions are rays.)",
         ["2/x", "x+2", "2e^x"]),
        ("AP Stretch: A culture satisfies $y'=ky$ with $y(0)=500$ and $y(4)=2000$. The time $t>0$ when $y=8000$ is",
         8,
         "$2000=500e^{4k}\\Rightarrow e^{4k}=4$. Then $8000=500e^{kt}\\Rightarrow e^{kt}=16=4^2=(e^{4k})^2=e^{8k}$, so $t=8$. (Two doublings from $2000$ take as long as two doublings from $500$ to $2000$.)",
         [4, 12, 16]),
        ("AP Stretch: Newton’s law of cooling: $T'=k(T-20)$, $T(0)=80$, $T(10)=50$. The temperature at $t=20$ is",
         35,
         "$T-20=60e^{kt}$. Then $30=60e^{10k}$ so $e^{10k}=1/2$. Hence $T(20)=20+60(e^{10k})^2=20+60\\cdot\\frac14=35$.",
         [50, 20, 80]),
        ("AP Stretch: Let $y=\\dfrac{2}{1-2x}$. Differentiate $y$, then decide whether this $y$ solves the IVP $y'=y^2$, $y(0)=2$. The correct conclusion is",
         "yes: y'=4/(1-2x)^2 equals y^2, and y(0)=2",
         "Quotient/chain: $y'=2\\cdot 2(1-2x)^{-2}=4/(1-2x)^2=y^2$. The IC is $2/1=2$. Both the DE and the IC hold on $x<1/2$.",
         ["no: y'=-2/(1-2x)^2", "the DE holds but y(0)=1", "yes the IC, but y' is not y^2"]),
        ("AP Stretch: On the slope field for $y'=2y-x$, the slope at $(1,1)$ is $1$. Horizontal ticks occur on $y=x/2$. A solution through $(1,1)$ therefore starts",
         "above the isocline y=x/2 and initially increasing",
         "At $(1,1)$, $y=1>1/2$ and $2y-x=1>0$. The solution is above the slope-$0$ line and rising.",
         ["on y=x/2", "below y=x/2 and decreasing", "vertical"]),
        ("AP Stretch: On the slope field for $y'=x-y$, horizontal ticks occur where $x-y=0$, i.e. on $y=x$. A solution through $(0,1)$ has initial slope $0-1=-1$. This solution starts",
         "above y=x and initially decreasing",
         "$(0,1)$ lies above $y=x$ and the field there has slope $-1<0$. Solutions later may bend toward the isocline.",
         ["below y=x and increasing", "on y=x", "vertical"]),
        ("AP Stretch: $y'+2y=6$, $y(0)=1$. Integrating factor is not required if you write $y'=2(3-y)$ and separate: $\\int dy/(3-y)=\\int 2\\,dx$. Then $y=$",
         "3-2e^{-2x}",
         "$-\\ln|3-y|=2x+C_1$. $y(0)=1\\Rightarrow 3-y=2e^{-2x}$, $y=3-2e^{-2x}$.",
         ["3+2e^{-2x}", "1+6x", "3e^{-2x}"]),
        ("AP Stretch: Separable $y'=2x(1+y^2)$, $y(0)=1$. After separating $\\dfrac{dy}{1+y^2}=2x\\,dx$ and applying the initial condition, the particular solution is",
         "y=tan(x^2+π/4)",
         "$\\arctan y=x^2+C$. At $x=0$, $\\arctan 1=C=\\pi/4$. Domain: $x^2+\\pi/4<\\pi/2$.",
         ["y=tan(x^2)", "y=e^{x^2}", "y=x^2+1"]),
    ])


def build_unit7():
    title = "AP Calculus AB Unit 7: Differential Equations"
    description = (
        "Slope fields, separable equations, exponential growth and decay, particular solutions, "
        "qualitative reasoning from a field, and verifying a proposed solution — no Euler, series, or polar."
    )
    concepts = [
        "Slope fields",
        "Separable DEs",
        "Exponential growth/decay",
        "Particular solutions",
        "Reasoning from a slope field",
        "Verify a solution",
    ]

    c1 = concept_block(
        "1. Slope fields",
        [
            "A slope field (direction field) plots short ticks whose slope at $(x,y)$ is the value of $dy/dx$ given by the DE. It is a picture of the DE, not of one solution.",
            "To build one by hand, evaluate the right-hand side on a grid. For $y'=x-y$, the tick at $(1,2)$ has slope $1-2=-1$.",
            "Isoclines are curves of constant slope. For $y'=x-y$, slope $0$ lives on $y=x$; slope $1$ lives on $y=x-1$. Recognizing isoclines speeds up sketching.",
            "A solution curve must be tangent to the local tick. You sketch it by starting at an initial point and threading through the field.",
            "Autonomous equations $y'=f(y)$ have horizontal isoclines: every tick on a given horizontal line is parallel. That is how you spot $y'=y$ versus $y'=x$.",
            "AP will show a field and ask which DE matches, which graph could be a solution, or what happens as $x\\to\\infty$. No Euler-method stepping is required on AB.",
        ],
        "Slope-field FRQs appear most years. Matching a field to a DE is a no-calculator skill that does not need a solved formula.",
        "At a test point, compute the DE’s slope and compare to the pictured tick. One well-chosen point often eliminates three of four matching choices.",
        lesson_figure(
            _slope_field_svg(lambda x, y: x - y, highlight=[(0, 1, "(0,1)")]),
            "Slope field for $y'=x-y$, with an initial point marked",
            "On the line $y=x$ the ticks are horizontal. At $(0,1)$ the slope is $-1$, so a solution through that point starts downward.",
        )
        + solved(
            1,
            "On $y'=2x$, what is the slope at $(−1,5)$?",
            ["$m=2(-1)=-2$.", "The $y$-value is irrelevant for this DE."],
            "$-2$", "", "Easy",
        )
        + solved(
            2,
            "Which feature distinguishes $y'=y$ from $y'=x$ on a slope field?",
            [
                "For $y'=y$, ticks on a horizontal line are parallel (same $y$).",
                "For $y'=x$, ticks on a vertical line are parallel (same $x$).",
                "Look at one row versus one column of the grid.",
            ],
            "horizontal vs vertical isoclines", "", "Medium",
        )
        + solved(
            3,
            "Match a field whose ticks are steeply negative in quadrant II and steeply positive in quadrant IV, with $m=0$ on both axes, to a DE.",
            [
                "On the axes, slope $0$ suggests a factor $xy$ or similar.",
                "$y'=xy$ has $m=0$ on $x=0$ and on $y=0$, sign of $xy$ matching those quadrants.",
                "$y'=x+y$ would not vanish on both axes.",
            ],
            "$y'=xy$ is consistent", "Eliminate with axis ticks first.", "Honors",
        ),
        ("Treating a slope field as a single solution graph",
         "The field contains many solutions. A particular solution is one curve you draw on top of the field, using an initial point."),
        ("Test one easy point (an axis intercept) when matching DE to field",
         "If the field has horizontal ticks on the $x$-axis, the DE must give $y'=0$ when $y=0$. That single observation kills many foils."),
        ["I can compute a tick slope from a DE.", "I recognize isoclines.", "I sketch a solution tangent to nearby ticks."],
        1,
    )

    c2 = concept_block(
        "2. Separable differential equations",
        [
            "A first-order DE is separable if $dy/dx=g(x)h(y)$. Then, off the zeros of $h$, $\\dfrac{1}{h(y)}\\,dy=g(x)\\,dx$. Integrate both sides, then solve for $y$ if required.",
            "Constant solutions: if $h(y_0)=0$, then $y(x)\\equiv y_0$ solves the DE (an equilibrium). Check it; it may be lost when you divide by $h(y)$.",
            "The $+C$ appears after integration. An initial condition is not needed to write the general solution, but it is needed to pin down $C$.",
            "Implicit solutions such as $x^2+y^2=C$ are acceptable if you cannot or should not solve for $y$. Name the branch that matches an initial point when you do solve.",
            "Domain: a solution may exist only on an interval where the rewritten functions stay defined (logs, even roots, division by $y$).",
            "AB separable practice is mostly $y'=ky$, $y'=g(x)$, $y'=g(x)/y$, and linear-looking $y'=k(y-A)$ after a substitution $u=y-A$.",
        ],
        "Exponential models, cooling, and many FRQ “find $y$ as a function of $x$” items are this algebra. If separation is messy, the rest of Unit 7 is blocked.",
        "Write $dy/h(y)=g(x)\\,dx$, integrate, add $C$, then apply $y(x_0)=y_0$. Check constant solutions before dividing.",
        lesson_figure(
            _family_svg(),
            "A family of exponential solutions $y=Ce^{-kt}$ of $y'=-ky$",
            "Separation produces the family. The initial condition will later pick the highlighted member.",
        )
        + solved(
            1,
            "Solve $dy/dx=6x^2$.",
            ["$y=2x^3+C$."],
            "$y=2x^3+C$", "", "Easy",
        )
        + solved(
            2,
            "Solve $dy/dx=y$ for $y>0$.",
            ["$dy/y=dx$.", "$\\ln y=x+C_1$.", "$y=e^{C_1}e^{x}=Ce^{x}$ with $C>0$."],
            "$y=Ce^{x}$ ($C>0$ in this sign case)", "The general real family allows $C\\in\\mathbb{R}$, including $y=0$.", "Medium",
        )
        + solved(
            3,
            "Solve $y y'=x$ with $y(0)=-2$.",
            [
                "$y\\,dy=x\\,dx$.",
                "$y^2/2=x^2/2+C$.",
                "$4/2=0+C\\Rightarrow C=2$.",
                "$y^2=x^2+4$. Since $y(0)=-2<0$, $y=-\\sqrt{x^2+4}$.",
            ],
            "$y=-\\sqrt{x^2+4}$", "The sign of the root is an initial-condition decision.", "Honors",
        ),
        ("Dividing by y and losing the solution y=0",
         "If the DE is $y'=y(y-1)$, then $y=0$ and $y=1$ are solutions. Separation assumes $y(y-1)\\neq 0$. List equilibria first."),
        ("Keep the solution implicit until the initial condition chooses a branch",
         "Circles and $\\pm$ square roots are the usual place this matters. Plug the initial point before you drop a sign."),
        ["I separate variables and integrate both sides.", "I include +C, then apply y(x0)=y0.", "I check constant solutions before dividing."],
        6,
    )

    c3 = concept_block(
        "3. Exponential growth and decay",
        [
            "The model $y'=ky$ has solutions $y=y_0 e^{kt}$. If $k>0$, growth; if $k<0$, decay. The units of $k$ are $1/\\text{time}$.",
            "Doubling time $T$ satisfies $e^{kT}=2$, so $T=(\\ln 2)/k$. Half-life uses $e^{kT}=1/2$, so $T=(\\ln 2)/|k|$ when $k<0$.",
            "Newton cooling/heating: $T'=k(T-T_a)$ is $u'=ku$ after $u=T-T_a$. Solutions exponentially approach the ambient temperature.",
            "A word problem must produce both the DE and the initial condition. “Proportional to the amount present” is $y'=ky$, not $y'=k$.",
            "Exact answers in terms of $e$ and $\\ln$ are preferred on no-calculator paper. Decimal approximations belong to the calculator section.",
            "This is still AB: no logistic closed form is required here, and no Euler stepping. Stay with $y'=ky$ and $T'=k(T-T_a)$.",
        ],
        "Applied FRQs in Unit 7 are almost always this model plus an initial amount. The algebra is short; the modeling sentence is the hard part.",
        "Write the DE first ($dy/dt=ky$), then the general solution, then use two data points (or one point plus a doubling time) to find $k$ and $y_0$.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda t: 3.2 * math.exp(-0.45 * t), 0, 6))],
                points=[(0, 3.2, "y0")],
                xlim=(-0.3, 6.3), ylim=(-0.3, 4), w=300, h=230, xlab="t", ylab="y",
            ),
            "Exponential decay $y=y_0 e^{kt}$ with $k<0$",
            "The curve is always positive, always decreasing, and concave up, approaching $0$. That shape is a slope-field fingerprint of $y'=ky$ with $k<0$.",
        )
        + solved(
            1,
            "Write the solution of $y'=0.4y$, $y(0)=10$.",
            ["$y=10e^{0.4t}$."],
            "$y=10e^{0.4t}$", "", "Easy",
        )
        + solved(
            2,
            "A half-life of $8$ hours, $y(0)=24$. Find $y(t)$.",
            ["$k=\\ln(1/2)/8=-(\\ln 2)/8$.", "$y=24e^{-(\\ln 2)t/8}=24\\cdot 2^{-t/8}$."],
            "$y=24\\cdot 2^{-t/8}$", "The power-of-two form is exact and AP-friendly.", "Medium",
        )
        + solved(
            3,
            "Coffee at $90^\\circ$C in a $20^\\circ$C room satisfies $T'=k(T-20)$, $T(5)=60$. Find $k$ and $T(10)$.",
            [
                "$T-20=70e^{kt}$.",
                "$40=70e^{5k}\\Rightarrow e^{5k}=4/7\\Rightarrow k=\\frac15\\ln(4/7)$.",
                "$T(10)=20+70e^{2\\ln(4/7)}=20+70\\cdot(16/49)=20+160/7=300/7$.",
            ],
            "$k=\\dfrac{1}{5}\\ln\\dfrac{4}{7}$, $T(10)=\\dfrac{300}{7}$", "Use $e^{2u}=(e^u)^2$.", "Honors",
        ),
        ("Writing y=e^{kt}+C for y'=ky",
         "The constant is multiplicative: $Ce^{kt}$, not additive. Additive $C$ would solve $y'=k$, a different DE."),
        ("Find k from a ratio of two measurements",
         "$y(t_2)/y(t_1)=e^{k(t_2-t_1)}$. Taking ln isolates $k$ without needing a messy $y_0$ if it cancels."),
        ["I write y=y0 e^{kt}.", "I can find doubling time or half-life.", "I can shift to u=T−T_a for cooling."],
        11,
    )

    c4 = concept_block(
        "4. Particular solutions",
        [
            "The general solution of a first-order DE contains an arbitrary constant. A particular solution uses an initial condition $y(x_0)=y_0$ to determine that constant.",
            "Always apply the initial condition after integrating, not before. Substituting a snapshot into the DE before integrating is the related-rates error in a new costume.",
            "If the general solution is implicit, plug $(x_0,y_0)$ into the implicit form to get $C$, then solve for $y$ only if asked, choosing the correct branch.",
            "Uniqueness: through a point where $f$ and $\\partial f/\\partial y$ are continuous, the IVP $y'=f(x,y)$, $y(x_0)=y_0$ has one solution. Two solution curves do not cross there.",
            "A particular solution still has a domain. $y=1/(1-x)$ with $y(0)=1$ cannot be continued through $x=1$.",
            "On an FRQ, box the particular $y(x)$ and state the interval if it is obvious (logs, roots, denominators).",
        ],
        "AP rarely wants a $C$ left in the answer when an initial condition was given. “Find the particular solution” means kill $C$.",
        "General solution, plug the point, solve for $C$, rewrite $y$, check by differentiating and by substituting the point.",
        lesson_figure(
            _family_svg(),
            "Many solutions of one DE; an initial point selects one curve",
            "The family is the general solution. The redder, higher curve would correspond to a larger $C$ in $y=Ce^{-kt}$.",
        )
        + solved(
            1,
            "$y'=4x$, $y(0)=1$. Find the particular solution.",
            ["$y=2x^2+C$.", "$1=C$.", "$y=2x^2+1$."],
            "$y=2x^2+1$", "", "Easy",
        )
        + solved(
            2,
            "$y'=y$, $y(0)=-4$.",
            ["$y=Ce^{x}$.", "$-4=C$.", "$y=-4e^{x}$."],
            "$y=-4e^{x}$", "Negative $C$ is legal and needed.", "Medium",
        )
        + solved(
            3,
            "$y'=1/y$, $y(0)=2$. Give $y$ as a function of $x$ and the domain.",
            [
                "$y\\,dy=dx$, $y^2/2=x+C$.",
                "$2=C$, so $y^2=2x+4$, $y=\\sqrt{2x+4}$ (positive).",
                "Domain $x\\ge -2$, and the IVP is posed at $0$, so the solution lives at least on $(-2,\\infty)$.",
            ],
            "$y=\\sqrt{2x+4}$, $x\\ge -2$", "", "Honors",
        ),
        ("Reporting the general solution when an initial condition was given",
         "The word particular means $C$ is gone. If you cannot solve for $C$, you have not finished."),
        ("Check both the DE and the initial point after you have y",
         "Two checks, five seconds. That is how verification (next lessons) starts."),
        ["I determine C from (x0,y0).", "I choose the correct root/branch.", "I note the domain of the particular solution."],
        16,
    )

    c5 = concept_block(
        "5. Reasoning from a slope field",
        [
            "Without solving, you can still say whether a solution is increasing, approaching an equilibrium, or blowing up, by reading ticks along a sketched curve.",
            "If $y'>0$ throughout a region, every solution there is increasing. If ticks reverse across a line of slope $0$, that line is a candidate equilibrium.",
            "Stability: if ticks above an equilibrium point down toward it and ticks below point up toward it, solutions approach that line (attracting). The opposite is repelling.",
            "Long-run behavior $x\\to\\infty$ is a standard AP prompt. Follow the curve to the right of the window and describe it in words: “approaches $y=2$ from below.”",
            "Matching a solution graph to a field: the graph’s slope at two or three labeled points must match the ticks. A graph that cuts ticks at a sharp angle is not a solution.",
            "Still no Euler: you are not asked to step $y_{n+1}=y_n+h f(x_n,y_n)$ on AB. Qualitative tangent-following is enough.",
        ],
        "This is the no-formula half of the DE FRQ. Students who can only separate variables freeze when the field is given without an equation.",
        "Pick two points on a proposed graph, compute or read the needed slopes, and accept/reject. Then describe end behavior in a sentence.",
        lesson_figure(
            _slope_field_svg(lambda x, y: 1 - y, n=8, highlight=[(0, 0, "(0,0)")]),
            "Slope field for $y'=1-y$: attracting equilibrium $y=1$",
            "Below $y=1$ the ticks have positive slope; above, negative. Solutions are funneled toward the line $y=1$.",
        )
        + solved(
            1,
            "On $y'=1-y$, is a solution through $(0,0)$ increasing at that point?",
            ["Slope $1-0=1>0$.", "Yes, increasing at $(0,0)$."],
            "yes, slope $1$", "", "Easy",
        )
        + solved(
            2,
            "Describe $\\lim_{x\\to\\infty}y(x)$ for that solution.",
            ["The field drives $y$ up toward $1$ but not past it (slopes flatten to $0$).", "The limit is $1$."],
            "approaches $1$ from below", "", "Medium",
        )
        + solved(
            3,
            "A proposed graph through $(0,0)$ rises above $y=1$ and continues increasing. Why can it not be a solution of $y'=1-y$?",
            [
                "Above $y=1$, the DE requires negative slope.",
                "An increasing graph in that region contradicts every tick.",
                "Solutions cannot cross the equilibrium $y=1$ in finite time under uniqueness.",
            ],
            "it would need $y'<0$ above $y=1$", "", "Honors",
        ),
        ("Claiming a solution will cross a line of horizontal ticks",
         "If uniqueness holds, a solution that reaches an equilibrium stays there. Crossing $y=1$ for $y'=1-y$ is a picture of the wrong DE."),
        ("Describe end behavior in words plus a y-value",
         "“Goes to 1 from below” earns more than “flattens.” Name the equilibrium."),
        ["I read increasing/decreasing from tick signs.", "I identify attracting equilibria.", "I reject graphs that cut across ticks."],
        21,
    )

    c6 = concept_block(
        "6. Verifying a solution",
        [
            "To verify that $y=f(x)$ solves an IVP, compute $y'$ (and $y''$ if the DE is second-order — rare on AB), substitute into the DE, and simplify to an identity. Then check $y(x_0)=y_0$.",
            "Verification does not require solving the DE from scratch. It is often easier than separation when a candidate is given.",
            "Implicit candidates: differentiate the relation, then substitute $y'$ into the DE, using the relation to simplify.",
            "A function can satisfy the DE but miss the initial condition — then it is a solution of the DE but not of the IVP. AP will ask which.",
            "Domain: $y=\\sqrt{x}$ is not a solution on $(-1,1)$ of anything requiring $y'$ at $0$ from both sides. State the interval.",
            "This skill is the check step for every particular solution you produce in the first five lessons. Write it even when the prompt does not say “verify.”",
        ],
        "On mixed-review FRQs, a “show that $y=\\ldots$ satisfies” stem is free points if you substitute cleanly. It also catches algebra errors in $C$.",
        "Two columns: left side of the DE after substituting, right side after substituting. Show they match. Then a one-line IC check.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: 2 * math.exp(-0.5 * x), -0.2, 4))],
                points=[(0, 2, "IC")],
                xlim=(-0.4, 4.2), ylim=(-0.3, 2.6), w=300, h=220, xlab="x", ylab="y",
            ),
            "Candidate $y=2e^{-x/2}$: check $y'=-y/2$ and $y(0)=2$",
            "Differentiation produces $y'=-e^{-x/2}=-y/2$. The graph’s initial height is $2$. Both pieces of the IVP hold.",
        )
        + solved(
            1,
            "Verify $y=x^2$ solves $y'=2x$, $y(0)=0$.",
            ["$y'=2x$, matches.", "$0^2=0$, matches."],
            "yes, both DE and IC", "", "Easy",
        )
        + solved(
            2,
            "Does $y=e^{x}+1$ solve $y'=y-1$?",
            ["$y'=e^{x}$.", "$y-1=e^{x}$.", "Yes the DE. (No IC was given.)"],
            "yes, it solves the DE", "", "Medium",
        )
        + solved(
            3,
            "Verify $y=\\dfrac{1}{1-x}$ solves $y'=y^2$, $y(0)=1$, and state a domain.",
            [
                "$y'=(1-x)^{-2}=y^2$.",
                "$y(0)=1$.",
                "Defined for $x<1$ (or $x>1$ separately); the IVP lives on $(-\\infty,1)$.",
            ],
            "yes, on $(-\\infty,1)$", "A blow-up at $x=1$ is allowed; the solution does not extend through it.", "Honors",
        ),
        ("Checking only the initial condition",
         "Lots of functions pass through $(0,1)$. Only those whose derivative matches the DE are solutions. Always differentiate."),
        ("Substitute y and y' on paper; do not “see that it looks right”",
         "The algebra of verification is the point. Write $y'=\\ldots$ then plug."),
        ["I substitute y' into the DE.", "I check the initial condition separately.", "I state a domain when the solution blows up."],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u7_questions()


# ===========================================================================
# UNIT 8: AP Mixed Review
# ===========================================================================

def _u8_questions():
    return _pack([
        ("From a piecewise graph, $\\lim_{x\\to 2}f(x)=5$ but $f(2)=1$. The FRQ sentence is",
         "f is discontinuous at 2 because the limit does not equal f(2)",
         "Name the failed continuity bullet.",
         ["the limit DNE", "f is not defined", "f'(2)=0"]),
        ("IVT on $[1,4]$ with $f(1)=-2$, $f(4)=3$ guarantees",
         "some c in (1,4) with f(c)=0, if f is continuous on [1,4]",
         "Cite continuity, the interval, and the trapped value.",
         ["a unique root", "f'(c)=0", "a VA at 0"]),
        ("A jump at $x=1$ means you must not cite IVT on an interval that",
         "contains x=1 in its interior (or wherever the jump sits)",
         "Split into continuous pieces first.",
         ["is closed", "has f(a)≠f(b)", "is bounded"]),
        ("Algebraic FRQ: $\\lim_{x\\to 1}\\dfrac{x^2-1}{x-1}$ is justified by",
         "factoring to x+1 for x≠1, then substituting to get 2",
         "Show the rewrite; do not only quote a calculator value.",
         ["L'Hôpital without 0/0", "a slope field", "MVT"]),
        ("One-sided limits disagree at $a$. The two-sided limit",
         "DNE; report both one-sided values if asked",
         "Do not average them.",
         ["equals f(a)", "equals 0", "exists anyway"]),
        ("Particle FRQ: $v(t)=0$ and $v$ changes sign $\\Rightarrow$",
         "the particle changes direction",
         "No sign change, no turn — even if $v=0$.",
         ["speed is infinite", "a(t)=0 automatically", "s(t)=0"]),
        ("Related rates FRQ: differentiate the constraint with respect to",
         "t, then substitute the snapshot",
         "Do not freeze changing variables before differentiating.",
         ["x only", "the angle after plugging numbers first", "area only"]),
        ("Linearization FRQ: over/under is justified with",
         "the sign of f'' (concavity vs the tangent)",
         "Concave up: tangent underestimates.",
         ["the sign of f only", "IVT", "a Riemann sum"]),
        ("Candidates on $[a,b]$: the absolute max is the largest",
         "f-value among critical numbers and endpoints",
         "A local max can lose to an endpoint.",
         ["x-value only", "f' value", "f'' value"]),
        ("First derivative test sentence:",
         "f' changes from + to − at c, so f has a local max at c",
         "Name the sign change.",
         ["f'(c)=0 so max", "f''(c)=0 so max", "f(c)=0 so max"]),
        ("Area FRQ: integrand is",
         "top − bottom, limits at intersections",
         "Sketch the region.",
         ["π R^2 always", "f'", "average value"]),
        ("Washer FRQ: volume integrand is",
         "π(R^2 − r^2), radii measured to the axis",
         "Square first.",
         ["π(R−r)^2", "2π x f(x) required on AB", "s(x)^2"]),
        ("Average value FRQ: display",
         "1/(b−a) ∫_a^b f",
         "Then compute; include units of $f$.",
         ["∫ f only", "(f(a)+f(b))/2 always", "f'(c)"]),
        ("In/out FRQ: amount at time T is",
         "initial + ∫(E−L) dt",
         "Rate in minus rate out, accumulated.",
         ["E(T)−L(T)", "E'(T)", "max of E"]),
        ("Net vs total: displacement is $\\int v$; distance is",
         "∫|v|, split where v changes sign",
         "Read the stem’s word.",
         ["∫ v also", "v(b)−v(a)", "s(a)+s(b)"]),
        ("Slope-field FRQ: a solution through a point must",
         "follow the ticks (be tangent to the field)",
         "Reject graphs that cut across marks.",
         ["be a straight line", "pass through the origin", "be a circle always"]),
        ("Separable FRQ write-up: $dy/h(y)=g(x)\\,dx$, integrate, $+C$, then",
         "apply the initial condition",
         "Check $h(y)=0$ equilibria.",
         ["differentiate again", "use IVT", "use a jump"]),
        ("Exponential model: “proportional to the amount” means",
         "y'=ky, not y'=k",
         "Then $y=y_0 e^{kt}$.",
         ["y=kt", "y''=ky", "y=k/t"]),
        ("Verify a solution: substitute $y$ and $y'$ into the DE and",
         "check the initial condition",
         "Both pieces of the IVP.",
         ["only check C", "only sketch", "cite IVT"]),
        ("Qualitative: if $y'=1-y$, then $y=1$ is",
         "an attracting equilibrium",
         "Slopes point toward the line.",
         ["a VA", "repelling always", "not a solution"]),
        ("No-calculator: $\\lim_{x\\to 0}\\dfrac{\\sin x}{x}$ is",
         1, "Standard limit or L'Hôpital after citing $0/0$.", [0, "+∞", "π"]),
        ("Calculator-active: a definite integral of a non-elementary $f$ should be",
         "computed numerically after writing the integral",
         "Still display the integral; the calculator is the last step.",
         ["skipped", "replaced by a derivative", "replaced by a slope field only"]),
        ("No-calculator: $\\int_0^{\\pi/2}\\cos x\\,dx$ is mental FTC2, equal to",
         1, "Do not reach for a calculator.", [0, 2, -1]),
        ("Calculator: a table Riemann sum still requires you to",
         "show Δx and the sampled heights",
         "The calculator is not a substitute for the sum setup.",
         ["guess the integral", "skip the antiderivative step", "skip the table"]),
        ("Exact $e^{\\ln 5}$ on no-calc paper is", 5, "Do not decimalize.", [1, 0, "ln 5"]),
        ("IVT citation must include",
         "continuity on a closed interval and a y-value between f(a) and f(b)",
         "Existence of $c$, not uniqueness.",
         ["f' exists", "f''>0", "a slope field"]),
        ("MVT citation must include continuity on $[a,b]$, differentiability on $(a,b)$, and",
         "some c in (a,b) with f'(c)=(f(b)−f(a))/(b−a)",
         "Then solve and verify $c$ is in the interval.",
         ["f'(c)=0 always", "f(c)=0", "c=a"]),
        ("EVT citation: continuous on a closed bounded interval, so abs extrema exist and occur at",
         "critical numbers or endpoints",
         "Then compare $f$-values.",
         ["inflection points only", "zeros of f only", "where f''=0 only"]),
        ("FTC justification of $F'(x)=f(x)$ for $F(x)=\\int_a^x f$ requires",
         "f continuous (so FTC1 applies)",
         "Name the theorem.",
         ["MVT only", "L'Hôpital only", "a washer"]),
        ("L'Hôpital citation requires the form",
         "0/0 or ∞/∞ (after rewrite if needed)",
         "Then $\\lim f'/g'$.",
         ["1/0", "∞−∞ without rewrite", "0·∞ without rewrite"]),
        ("A graph has a hole at $(0,2)$ and $f(0)=5$. Continuity fails; the limit is",
         2, "FRQ: limit exists, value mismatches.", [5, 0, "DNE"]),
        ("$f(x)=x^3-x-1$ on $[1,2]$: $f(1)=-1$, $f(2)=5$. A root exists in $(1,2)$ by",
         "IVT", "Polynomial $\\Rightarrow$ continuous.", ["MVT", "Rolle", "EVT"]),
        ("$s(t)=t^3-6t^2+9t$. Direction change when $v=3(t-1)(t-3)$ changes sign, at",
         "t=1 and t=3", "Both zeros in a typical closed interval like $[0,4]$ are turns.",
         ["t=0 only", "t=9", "never"]),
        ("Ladder 13 ft, $x=5$, $x'=2$: $y'=$", "-5/6",
         "Related rates with implicit Pythagoras.", ["5/6", "2", "-2"]),
        ("$\\int_0^1(x-x^2)\\,dx=$", "1/6", "Area between $y=x$ and $y=x^2$.", ["1/2", "1", "0"]),
        ("Washer $y=x$, $y=x^2$, about $x$-axis: $V=$", "2π/15",
         "$\\pi\\int(x^2-x^4)\\,dx$.", ["π/2", "π", "2/15"]),
        ("$F(x)=\\int_1^{x^2}\\sqrt{t}\\,dt$, $F'(x)=$",
         "2x√(x^2)=2x|x|",
         "FTC1+chain: $\\sqrt{x^2}\\cdot 2x=|x|\\cdot 2x$. For $x>0$, $2x\\cdot x=2x^2$.",
         ["√x", "2√x", "x^2"]),
        ("For $x>0$, that $F'(x)$ simplifies to", "2x^2",
         "$\\sqrt{x^2}=x$ when $x>0$, times $2x$.", ["2x", "x", "2√x"]),
        ("$y'=2y$, $y(0)=3$: particular solution", "3e^{2x}",
         "Separate and apply IC.", ["2e^{3x}", "3+2x", "e^{2x}+3"]),
        ("MVT on $f(x)=x^2$ on $[2,5]$: $c=$", "3.5",
         "$(25-4)/3=7$, $2c=7$, $c=3.5\\in(2,5)$.", [2, 5, 7]),
        ("Average of $v(t)=3t^2$ on $[1,3]$ equals average velocity, which is",
         "(s(3)-s(1))/2",
         "$s=t^3+C$, $(27-1)/2=13$. Also $\\frac12\\int_1^3 3t^2=13$.",
         ["v(2)=12", "9", "27"]),
        ("That average velocity equals", 13,
         "$(27-1)/2=13$.", [12, 26, 8]),
        ("No-calc: $\\lim_{x\\to\\infty}\\dfrac{4x^2}{2x^2+1}=$", 2, "Degrees / leading coefficients.", [4, 0, "+∞"]),
        ("Cite Rolle for $f(x)=x^2-4x$ on $[0,4]$: some $c$ has $f'(c)=0$. That $c=$",
         2, "$f'=2x-4$, and $f(0)=f(4)=0$.", [0, 4, 1]),
        ("L'Hôpital after rewrite: $\\lim_{x\\to\\infty} x\\ln\\!\\left(1+\\dfrac{3}{x}\\right)$ equals",
         3, "Rewrite as $\\dfrac{\\ln(1+3/x)}{1/x}$, form $0/0$, then L'Hôpital yields $3$.",
         [0, 1, "+∞"]),
        ("A no-calc rewrite: $\\lim_{x\\to 0}\\dfrac{1-\\cos x}{x^2}$, after multiplying by $1+\\cos x$, equals",
         "1/2",
         "Numerator becomes $\\sin^2 x$, so $(\\sin x/x)^2 / (1+\\cos x)\\to 1/2$. This is an AB-legal standard-limit argument, not a series.",
         [0, 1, "DNE"]),
        ("AP Stretch: A $6$-ft man walks away from a $15$-ft lamppost at $4$ ft/s. Let $x$ be his distance from the pole and $s$ the length of his shadow. Similar triangles: $\\dfrac{6}{s}=\\dfrac{15}{s+x}$. When $x=8$ ft, $ds/dt$ equals",
         "8/3",
         "$6(s+x)=15s\\Rightarrow 6x=9s\\Rightarrow s=(2/3)x$. Differentiate: $s'=(2/3)x'=8/3$ ft/s (constant for this geometry).",
         ["4", "16/3", "10/3"]),
        ("AP Stretch: The region bounded by $y=x^2$ and $y=1$ on $[-1,1]$ is rotated about $y=-1$. Washers have outer radius $2$ and inner radius $x^2+1$. The volume equals",
         "68π/15",
         "Even integrand: $2\\pi\\int_0^1\\bigl(4-(x^2+1)^2\\bigr)\\,dx=2\\pi\\int_0^1(3-2x^2-x^4)\\,dx=2\\pi(3-2/3-1/5)=68\\pi/15$.",
         ["4π", "34π/15", "16π/3"]),
        ("AP Stretch: A spherical balloon has volume $V=\\dfrac{4}{3}\\pi r^3$ increasing at $36\\pi$ in$^3$/s. When $r=3$ in, the rate of change of surface area $S=4\\pi r^2$ is",
         "24π",
         "$V'=4\\pi r^2 r'=36\\pi\\Rightarrow r'=1$. Then $S'=8\\pi r r'=8\\pi\\cdot 3\\cdot 1=24\\pi$ in$^2$/s.",
         ["36π", "12π", "4π"]),
        ("AP Stretch: The quarter-disk $y=\\sqrt{4-x^2}$, $0\\le x\\le 2$, is rotated about the $x$-axis. Disk volume $\\pi\\int_0^2(4-x^2)\\,dx$ equals",
         "16π/3",
         "$\\pi[4x-x^3/3]_0^2=\\pi(8-8/3)=16\\pi/3$, a hemisphere of radius $2$.",
         ["4π", "8π/3", "2π"]),
        ("AP Stretch: $F(x)=\\int_{\\sqrt{x}}^{x^3} e^{-t^2}\\,dt$. Then $F'(4)$ equals",
         "48e^{-4096} − (1/4)e^{-4}",
         "Leibniz: $f(x^3)3x^2-f(\\sqrt{x})\\cdot\\frac{1}{2}x^{-1/2}$. At $x=4$: $3\\cdot 16\\,e^{-64^2}-e^{-4}/4=48e^{-4096}-e^{-4}/4$.",
         ["e^{-4}", "0", "48e^{-4}"]),
        ("AP Stretch: Let $Q(x)=\\int_{\\ln x}^{2x} e^{-t}\\,dt$ for $x>0$. Then $Q'(1)$ equals",
         "2e^{-2} − 1",
         "Leibniz: $Q'(x)=e^{-2x}\\cdot 2-e^{-\\ln x}\\cdot(1/x)=2e^{-2x}-1/x^2$. At $x=1$: $2e^{-2}-1$.",
         ["2e^{-2}", "0", "e^{-2}-1"]),
        ("AP Stretch: L'Hôpital after $\\infty-\\infty$ rewrite: $\\lim_{x\\to 0^+}\\left(\\dfrac{1}{x}-\\dfrac{1}{\\tan x}\\right)=\\lim_{x\\to 0^+}\\dfrac{\\tan x-x}{x\\tan x}$. The limit equals",
         0,
         "Form $0/0$. After L'Hôpital (or equivalent small-angle reasoning legal on AB via standard limits), the value is $0$.",
         ["1", "+∞", "1/3"]),
        ("AP Stretch: MVT justification numbers: $f(x)=\\ln x$ on $[1,e]$. Hypotheses hold on $(1,e)$ for $f'$. Secant slope $(1-0)/(e-1)=1/(e-1)$. Then $c=$",
         "e-1",
         "$f'(c)=1/c=1/(e-1)\\Rightarrow c=e-1$, and $1<e-1<e$ because $2<e<3$.",
         ["1", "e", "1/e"]),
        ("AP Stretch: Let $f(x)=x+1/x$ on $[1,3]$. MVT requires some $c\\in(1,3)$ with $f'(c)=\\dfrac{(3+1/3)-2}{2}=\\dfrac{2}{3}$. Solving $1-1/c^2=2/3$ and checking the open interval gives $c=$",
         "√3",
         "$1/c^2=1/3$, so $c=\\sqrt{3}$ (positive). And $1<\\sqrt{3}<3$, as required for MVT.",
         [3, "1/√3", 2 / 3]),
        ("AP Stretch: Theorem stack: $f$ is continuous on $[0,4]$ and differentiable on $(0,4)$, $f(0)=1$, $f(4)=9$. MVT guarantees some $c\\in(0,4)$ with $f'(c)=2$. Applying IVT to $f'$ to claim $f'$ hits every value between $f'(0.1)$ and $f'(3.9)$ is unjustified because",
         "f' need not be continuous, so IVT does not apply to f' from the given",
         "MVT uses $f$, which is continuous on the closed interval and differentiable on the open interval. Darboux’s theorem is not an AP AB tool; without continuity of $f'$, IVT on $f'$ is illegal.",
         ["MVT already forbids other slopes", "f' is always continuous", "IVT never applies on [0,4]"]),
    ])


def build_unit8():
    title = "AP Calculus AB Unit 8: AP Mixed Review"
    description = (
        "Mixed AB free-response skills: limits and continuity, derivative applications, integral applications, "
        "DEs and slope fields, calculator habits, and theorem justifications — still Calculus AB only."
    )
    concepts = [
        "Limit/continuity FRQ skills",
        "Derivative applications FRQ",
        "Integral applications FRQ",
        "DE and slope-field FRQ",
        "Calculator vs no-calculator habits",
        "Justifying with theorems",
    ]

    c1 = concept_block(
        "1. Limit and continuity FRQ skills",
        [
            "An FRQ graph prompt wants a sentence, not a circled number: “The left-hand and right-hand limits both equal $3$, so the two-sided limit is $3$. $f(2)=1\\neq 3$, so $f$ is not continuous at $2$.”",
            "Algebraic limit FRQs still require the rewrite on paper. A calculator table can support a numerical limit in a calculator part, but $0/0$ must be factored or conjugated in a no-calc part.",
            "IVT write-up: name $f$, name $[a,b]$, cite continuity, compute $f(a)$ and $f(b)$, name the intermediate $k$, conclude existence of $c$ (not uniqueness, not a formula for $c$).",
            "Classify discontinuities: removable (limit exists), jump (one-sided finite and unequal), infinite (VA). That vocabulary is scored.",
            "Do not invent a two-sided limit when the sides disagree. “DNE” plus the two one-sided values is the complete answer.",
            "This lesson is Unit 1 under exam timing: shorter sentences, same theorems.",
        ],
        "Continuity and IVT points are among the easiest FRQ points to bank — and the easiest to lose by omitting the word continuous.",
        "Write the three continuity bullets or the four IVT bullets as a checklist in the margin, then fill numbers.",
        lesson_figure(
            _limit_jump_svg(),
            "FRQ-style piecewise graph: one-sided limits, a jump, and a separate $f(a)$",
            "Your paragraph should name each open circle’s height and then decide DNE versus a numerical two-sided limit.",
        )
        + solved(
            1,
            "From the figure, write the two-sided limit at $x=2$ and a continuity sentence.",
            [
                "Left-hand height $3$, right-hand height $4.5$: two-sided limit DNE.",
                "$f(2)=1$ is irrelevant to that DNE, but it is the function value.",
                "Discontinuous at $2$ because the two-sided limit does not exist (jump).",
            ],
            "limit DNE (jump); $f(2)=1$", "", "Easy",
        )
        + solved(
            2,
            "Show $x^3+x=1$ has a root in $(0,1)$ in FRQ format.",
            [
                "Let $f(x)=x^3+x-1$, continuous on $[0,1]$ as a polynomial.",
                "$f(0)=-1<0<1=f(1)$.",
                "By IVT there exists $c\\in(0,1)$ with $f(c)=0$.",
            ],
            "IVT existence in $(0,1)$", "", "Medium",
        )
        + solved(
            3,
            "Find $k$ so $f(x)=\\begin{cases}x^2+k&x\\le 1\\\\ 3x&x>1\\end{cases}$ is continuous at $1$, and state whether it must then be differentiable there.",
            [
                "Left limit $1+k$, right limit $3$, value $1+k$. Need $k=2$.",
                "Left derivative $2x|_{1}=2$, right derivative $3$. Unequal, so not differentiable.",
                "Continuity is necessary but not sufficient for differentiability.",
            ],
            "$k=2$; still not differentiable", "", "Honors",
        ),
        ("Averaging one-sided limits on a jump",
         "FRQ readers treat $(3+4.5)/2$ as a conceptual error. Write DNE."),
        ("Template the IVT paragraph before the exam",
         "Continuity, interval, endpoint values, trapped $k$, existence of $c$. Five commas, five points of information."),
        ["I write complete limit/continuity sentences.", "I cite IVT with hypotheses.", "I classify jump vs removable vs infinite."],
        1,
    )

    c2 = concept_block(
        "2. Derivative applications FRQ",
        [
            "Particle motion: a table or formula for $v$ or $s$, then rest, direction, speed vs velocity, displacement vs distance, speeding up (same sign of $v$ and $a$).",
            "Related rates: picture, constraint, reduce, $d/dt$, snapshot, units. Implicit Pythagoras and similar triangles are the usual geometry.",
            "Linearization: $L(x)=f(a)+f'(a)(x-a)$, then concavity for over/under.",
            "Closed-interval extrema: candidate list, table of values, sentence “the absolute maximum is … at $x=$ …”.",
            "First derivative test: an $f'$ sign chart is a complete classification argument. $f'(c)=0$ alone is not.",
            "Keep units in every boxed answer that came from a rate. ft/s, cm$^3$/min, people per hour.",
        ],
        "These six pages of Units 3–4 become one FRQ with four parts. Practice writing short justifications, not long essays.",
        "Identify the verb: approximate (linearize), how fast (related rates), when moving left (sign of $v$), maximum (candidates). Then pick the tool.",
        lesson_figure(
            _ladder_svg(),
            "Related-rates FRQ geometry: labeled ladder, wall, and floor",
            "The picture is part of the communication. Unlabeled lengths lose a setup point even if the implicit derivative is right.",
        )
        + solved(
            1,
            "If $v(t)=t^2-4$ on $[0,3]$, when is the particle moving left?",
            ["$v<0$ on $[0,2)$.", "At rest at $t=2$; moving right on $(2,3]$."],
            "moving left on $[0,2)$", "", "Easy",
        )
        + solved(
            2,
            "13-ft ladder, foot $5$ ft out, sliding at $2$ ft/s. Speed of the top?",
            ["$y=12$, $2x x'+2y y'=0$.", "$y'=-5/6$ ft/s, so the top descends at $5/6$ ft/s."],
            "$\\dfrac{5}{6}$ ft/s down", "", "Medium",
        )
        + solved(
            3,
            "On $[0,4]$, $f'(x)=x(x-3)$. Find absolute max of $f$ if $f(0)=1$, using net change of $f$.",
            [
                "Critical numbers $0,3$; endpoints $0,4$. $x=0$ is already an endpoint.",
                "$f(3)=1+\\int_0^3 x(x-3)\\,dx=1+\\int_0^3(x^2-3x)=1+[x^3/3-3x^2/2]_0^3=1+(9-27/2)=1-4.5=-3.5$.",
                "$f(4)=f(3)+\\int_3^4 x(x-3)\\,dx=-3.5+[x^3/3-3x^2/2]_3^4=-3.5+(64/3-24)-(9-27/2)=-3.5+(64/3-24-9+13.5)$.",
                "Signs of $f'$: $+$ on $(3,4)$ after being $-$ on $(0,3)$, so abs min at $3$, abs max is the larger of $f(0)=1$ and $f(4)$. Compute $f(4)=1+\\int_0^4(x^2-3x)=1+[x^3/3-3x^2/2]_0^4=1+(64/3-24)=1+(64/3-72/3)=-8/3+1=-5/3$.",
                "Abs max is $f(0)=1$; abs min is $f(3)=-7/2$.",
            ],
            "abs max $1$ at $x=0$; abs min $-7/2$ at $x=3$", "Use $\\int f'$ to recover $f$ values when $f$ is not given.", "Honors",
        ),
        ("Omitting units on a related-rates answer",
         "A boxed $-5/6$ without “ft/s downward” is incomplete on the AP rubric."),
        ("Underline the quantity whose rate is unknown before differentiating",
         "That underline is $y'$ or $s'$ or $dV/dt$. It prevents solving for the wrong derivative."),
        ["I can run a PVA sign chart under time pressure.", "I can do a ladder/cone related-rates write-up.", "I can finish an EVT table."],
        6,
    )

    c3 = concept_block(
        "3. Integral applications FRQ",
        [
            "Area: sketch, intersections, top minus bottom. Volume: disks/washers with $R$ and $r$ labeled, or $A(x)$ for a named cross-section.",
            "Average value: write $\\dfrac{1}{b-a}\\int_a^b f$ with units of $f$.",
            "Accumulation: $N(T)=N(0)+\\int_0^T(E-L)$. Max of $N$ from the sign chart of $E-L$.",
            "Net change vs total: the stem’s English decides $\\int F'$ versus $\\int|F'|$.",
            "FTC1+chain on an accumulation with variable limits is often part (c) of an otherwise geometric FRQ. Practice $f(g(x))g'(x)-f(h(x))h'(x)$ until it is automatic.",
            "If no elementary antiderivative exists, a calculator-active part wants a numerical integral — still write the integral first.",
        ],
        "Units 5–6 are half the exam’s integral points. A missing $\\pi$ or a radius measured to the wrong axis is a full-part loss.",
        "Sketch the 2D region on every volume problem, even when you think you remember the formula. Label the axis of rotation in color.",
        lesson_figure(
            _washer_svg(),
            "Washer FRQ setup: region, axis of rotation, and a representative washer",
            "The scoring standard looks for $R$ and $r$ in terms of $x$ (or $y$) before it looks for the antiderivative.",
        )
        + solved(
            1,
            "Area between $y=x$ and $y=x^2$ on $[0,1]$.",
            ["$\\int_0^1(x-x^2)\\,dx=1/6$."],
            "$1/6$", "", "Easy",
        )
        + solved(
            2,
            "That region about the $x$-axis, washer volume.",
            ["$\\pi\\int_0^1(x^2-x^4)\\,dx=2\\pi/15$."],
            "$2\\pi/15$", "", "Medium",
        )
        + solved(
            3,
            "$N(0)=80$, $E=12+t$, $L=2t$ on $[0,6]$. Max $N$ on the interval.",
            [
                "$N'=12+t-2t=12-t$, zero at $t=12$ (outside).",
                "On $[0,6]$, $N'>0$, so max at $t=6$.",
                "$N(6)=80+\\int_0^6(12-t)\\,dt=80+[12t-t^2/2]_0^6=80+72-18=134$.",
            ],
            "$134$ at $t=6$", "Do not invent a critical point outside the given interval.", "Honors",
        ),
        ("Using disk πR^2 when the solid has a hole",
         "If two functions bound the region and you rotate, you almost always need $R^2-r^2$. Look for the hole."),
        ("Write the integral with limits and integrand before the calculator",
         "A naked decimal with no integral displayed earns little. The setup is the mathematics."),
        ["I can set up area and washer integrals.", "I can do in/out accumulation.", "I can apply FTC1 with two variable limits."],
        11,
    )

    c4 = concept_block(
        "4. DE and slope-field FRQ",
        [
            "Typical four-part DE FRQ: (a) sketch a solution on a field, (b) write a particular solution by separation, (c) evaluate a limit as $t\\to\\infty$, (d) interpret $k$ or a half-life.",
            "Part (a) is scored by tangency to ticks, not by beauty. Start at the initial point; do not cross a visible equilibrium incorrectly.",
            "Part (b) wants separated integrals, $+C$, and the initial condition. Box $y(t)$.",
            "Exponential models: write $y'=ky$ in words first (“rate proportional to amount”), then solve.",
            "Verification part: substitute $y$ and $y'$. Easy points if you show the algebra.",
            "AB still excludes Euler’s method, series solutions, and polar DEs. If a picture looks like a logistic, you may reason qualitatively from the field without the logistic formula.",
        ],
        "This FRQ is often the most formulaic on the exam. A practiced template converts it into reliable points.",
        "Field sketch first (even if part (a) is matching, not drawing), then separate, then IC, then a sentence about long-run behavior.",
        lesson_figure(
            _slope_field_svg(lambda x, y: 0.5 * y, highlight=[(0, 2, "y(0)=2")]),
            "Slope-field FRQ: $y'=0.5y$ with initial point $(0,2)$",
            "Ticks are horizontal on $y=0$ and get steeper as $|y|$ grows. The solution through $(0,2)$ is an exponential $y=2e^{x/2}$.",
        )
        + solved(
            1,
            "From the field $y'=0.5y$, is $y=0$ a solution?",
            ["Yes: constant $0$ has derivative $0$, and $0.5\\cdot 0=0$."],
            "yes, equilibrium", "", "Easy",
        )
        + solved(
            2,
            "Find the particular solution through $(0,2)$.",
            ["$dy/y=0.5\\,dx$, $\\ln|y|=0.5x+C_1$, $y=2e^{x/2}$."],
            "$y=2e^{x/2}$", "", "Medium",
        )
        + solved(
            3,
            "A student sketches a solution through $(0,2)$ that becomes negative. Why is that illegal for $y'=0.5y$ with uniqueness?",
            [
                "$y=0$ is a solution.",
                "Solutions cannot cross.",
                "Starting at $y=2>0$, the solution stays positive.",
            ],
            "cannot cross the equilibrium $y=0$", "", "Honors",
        ),
        ("Crossing an equilibrium curve on the slope-field sketch",
         "If uniqueness applies, that crossing is the wrong picture and loses the sketch point."),
        ("Write the DE in words, then in symbols, then solve",
         "The modeling sentence is often its own point: “Let $y$ be the amount; $dy/dt=ky$.”"),
        ["I can sketch a solution on a field.", "I can separate and apply an IC.", "I can discuss equilibria without Euler."],
        16,
    )

    c5 = concept_block(
        "5. Calculator versus no-calculator habits",
        [
            "No-calculator section: exact values, standard limits, FTC by hand, derivatives by rules. A decimal for $\\ln 2$ is a wrong form, not a rounding issue.",
            "Calculator section: numerical definite integrals, numerical derivatives at a point, graphs to locate roots or intersections. You must still write the mathematical object you are approximating.",
            "Store a definite integral in the calculator only after the integral is on the paper with limits and integrand. The rubric reads the paper.",
            "Radian mode is required for calculus. Degree mode silently wrecks $\\sin x$ derivatives and integrals.",
            "Do not use a calculator to “confirm” a no-calc exact answer by a rounded decimal in that section. Keep exact $e$, $\\pi$, $\\sqrt{2}$.",
            "Some problems are legal on both: a Riemann sum from a table is arithmetic, not a calculator monopoly. Show the sum.",
        ],
        "Form points and communication points depend on this habit. A correct decimal in the no-calc section can still be marked wrong if exact form was required.",
        "Ask “could I do this with FTC and algebra?” If yes, stay exact. If the antiderivative is hopeless and the section is calculator-active, write the integral then compute.",
        lesson_figure(
            _riemann_svg(4),
            "A Riemann sum from a graph or table is a no-calculator method — rectangles, not a magic integral button",
            "The calculator’s $\\int$ command is for later, when $f$ has no elementary antiderivative and the exam allows it.",
        )
        + solved(
            1,
            "No-calc: $\\int_0^1 2x\\,dx$.",
            ["$x^2|_0^1=1$."],
            "$1$ (exact)", "", "Easy",
        )
        + solved(
            2,
            "Calculator-active setup: $\\int_0^2 e^{-x^2}\\,dx$ (no elementary antiderivative).",
            [
                "Write the integral.",
                "Then report a decimal to the required places from the calculator.",
                "Do not pretend an elementary $F$ exists.",
            ],
            "display the integral, then a decimal approximation", "", "Medium",
        )
        + solved(
            3,
            "A table Riemann left sum with $\\Delta x=2$ and heights $4,7,5$. No-calc arithmetic.",
            ["$2(4+7+5)=32$."],
            "$32$", "The calculator is unnecessary and hiding the work would lose method points.", "Honors",
        ),
        ("Boxing 0.693 for ln 2 in the no-calculator section",
         "Write $\\ln 2$. Save decimals for the section that invited them."),
        ("Put the integral on paper before the calculator evaluates it",
         "Readers cannot grade a calculator screen. They grade $ \\int_0^2 e^{-x^2}\\,dx \\approx \\ldots$."),
        ["I keep exact form on no-calc.", "I write integrals before numerical evaluation.", "I stay in radian mode."],
        21,
    )

    c6 = concept_block(
        "6. Justifying with theorems",
        [
            "Name the theorem, check hypotheses, write the conclusion. IVT, EVT, MVT/Rolle, FTC1, FTC2, L'Hôpital, first derivative test, and “differentiability $\\Rightarrow$ continuity” are the AB toolkit.",
            "Hypotheses are not decorative. $|x|$ on $[-1,1]$ kills MVT. $1/x$ on $[-1,1]$ kills IVT. An open interval kills EVT.",
            "MVT numbers: compute the secant slope, solve $f'(c)=$ that slope, verify $c\\in(a,b)$. That verification sentence is required.",
            "L'Hôpital: box $0/0$ or $\\infty/\\infty$ after any rewrite of $\\infty-\\infty$ or $0\\cdot\\infty$. Then differentiate numerator and denominator.",
            "FTC1 with chain is a theorem application: $F(x)=\\int_{h(x)}^{g(x)}f= G(g(x))-G(h(x))$, so $F'=f(g)g'-f(h)h'$.",
            "A justification that only restates the conclusion (“because MVT”) without hypotheses earns nothing. A justification that checks hypotheses without a conclusion is also incomplete.",
        ],
        "The exam’s communication standard is theorem language. This lesson is how you convert Units 1–7 into the sentences readers are trained to tick.",
        "For every theorem you cite, write two short lines: “Hypotheses: … Conclusion: …”. Fill them with the problem’s numbers.",
        lesson_figure(
            _mvt_svg(),
            "MVT picture: secant $AB$ and a parallel tangent at $c$",
            "The justification still needs $c\\in(a,b)$ in symbols, not only a sketch. The sketch is evidence; the interval check is the theorem.",
        )
        + solved(
            1,
            "Cite IVT to show $f(x)=x^3-x-1$ has a root in $(1,2)$.",
            ["Continuous on $[1,2]$.", "$f(1)=-1$, $f(2)=5$, $0$ in between.", "Some $c\\in(1,2)$ with $f(c)=0$."],
            "IVT, root in $(1,2)$", "", "Easy",
        )
        + solved(
            2,
            "MVT numbers for $f(x)=x^2$ on $[1,4]$.",
            ["Hypotheses hold.", "Secant slope $5$.", "$2c=5$, $c=2.5\\in(1,4)$."],
            "$c=5/2\\in(1,4)$", "", "Medium",
        )
        + solved(
            3,
            "Why L'Hôpital on $\\lim_{x\\to 0}(\\cos x)/x$ is illegal, and what the limit actually is.",
            [
                "Form is $1/0$, not $0/0$ or $\\infty/\\infty$.",
                "Right-hand limit $+\\infty$, left $-\\infty$, so two-sided DNE.",
                "Illegally applying the rule would produce $-\\sin x\\to 0$, a false finite limit.",
            ],
            "illegal form; two-sided limit DNE", "", "Honors",
        ),
        ("Citing a theorem by acronym without hypotheses",
         "Write “$f$ is continuous on $[a,b]$ and differentiable on $(a,b)$, so by MVT …” The acronym without the if-then is not a justification."),
        ("Hypotheses line, conclusion line, numbers in both",
         "That three-part habit covers IVT, MVT, EVT, and FTC citations on every mixed FRQ."),
        ["I name hypotheses before conclusions.", "I verify MVT’s c is in (a,b).", "I check L'Hôpital’s indeterminate form after rewrites."],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u8_questions()


def build_master():
    units = [('Limits & Continuity', ['Limit from a graph and table', 'Algebraic limits', 'One-sided limits', 'Infinite limits and asymptotes', 'Continuity', 'IVT']), ('Derivative Definition & Rules', ['Definition as limit of difference quotient', 'Power/product/quotient', 'Chain rule', 'Trig derivatives', 'Exponential and log derivatives', 'Differentiability vs continuity']), ('Applications of Derivatives I', ['Tangent line and linearization', 'Related rates', 'Position velocity acceleration', 'Increasing/decreasing', 'First derivative test', 'Candidates for extrema']), ('Applications of Derivatives II', ['Concavity and second derivative', 'MVT and Rolle', 'Optimization', 'Curve sketching', "L'Hôpital (0/0, ∞/∞)", 'Implicit differentiation']), ('Integrals & FTC', ['Antiderivatives', 'Riemann sums', 'Definite integral as net area', 'FTC part 1', 'FTC part 2', 'Substitution']), ('Applications of Integration', ['Area between curves', 'Volume disks/washers', 'Volume known cross-sections', 'Average value', 'Accumulation functions', 'Net change theorem']), ('Differential Equations', ['Slope fields', 'Separable DEs', 'Exponential growth/decay', 'Particular solutions', 'Reasoning from a slope field', 'Verify a solution']), ('AP Mixed Review', ['Limit/continuity FRQ skills', 'Derivative applications FRQ', 'Integral applications FRQ', 'DE and slope-field FRQ', 'Calculator vs no-calculator habits', 'Justifying with theorems'])]
    items = "".join(f"<li>Unit {i} — {u[0]}</li>" for i, u in enumerate(units, 1))
    return (
        f"<h1>AP Calculus AB Complete</h1>"
        f"<p><strong>For:</strong> <strong>AP Calculus AB</strong>. Eight deep units, each with six concepts, "
        "worked examples with matching diagrams, 5 quizzes per concept, and a 25-problem stretch finale.</p>"
        f"{page_break()}"
        "<h2>The eight units</h2>"
        f"<ol>{items}</ol>"
    )
