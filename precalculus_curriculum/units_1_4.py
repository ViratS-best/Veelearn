#!/usr/bin/env python3
"""Deep Precalculus units 1–4: functions, polynomials/rationals, exp/log, trig."""

from __future__ import annotations

import math

from curriculum_kit import lesson_figure, svg_parabola, svg_circle, svg_plane

from hs_curriculum import (
    concept_block,
    solved,
    practice_slots,
    unit_shell,
    mq,
    xy_graph,
    sample_curve,
    number_line,
    argand,
    unit_circle_svg,
    labeled_right_triangle,
)

from .common import AUDIENCE, STRETCH_LABEL


def _ellipse(a, b, n=80):
    return [(a * math.cos(2 * math.pi * i / n), b * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]


def _add(qs, rows):
    for row in rows:
        text, ans, expl = row[0], row[1], row[2]
        dist = row[3] if len(row) > 3 else None
        qs.append(mq(text, ans, expl, len(qs) + 1, distractors=dist))
    return qs


# ===========================================================================
# UNIT 1: Functions, Composition & Inverses
# ===========================================================================

def _u1_questions():
    qs = []
    _add(qs, [
        ("Which real numbers are allowed as inputs of $f(x)=\\sqrt{x-4}$?",
         "x\u22654",
         "An even root requires a nonnegative inside: $x-4\\geq0$, so $x\\geq4$.",
         ["x>4 only", "x\u22644", "all real numbers"]),
        ("The smallest output of $g(x)=(x-1)^2+5$ is which number?",
         5,
         "A square is never negative, so the vertex value $5$ is the minimum of the range.",
         None),
        ("Find every real input missing from the domain of $h(x)=\\dfrac{x+1}{x^2-9}$.",
         "x=\u00b13",
         "The denominator is zero when $x^2=9$, so $x=3$ and $x=-3$ are excluded.",
         ["x=9 only", "x=-1 only", "no values are excluded"]),
        ("If $f(x)=\\dfrac{1}{\\sqrt{8-x}}$, which description of the domain is correct?",
         "x<8",
         "Need $8-x>0$ (strict, because the square root sits in a denominator), so $x<8$.",
         ["x\u22648", "x>8", "x\u22608"]),
        ("A graph never drops below $y=-2$ and never rises above $y=6$. A possible range is:",
         "[-2,6]",
         "If those extrema are actually attained, the range is the closed interval from $-2$ to $6$.",
         ["(-2,6)", "all real numbers", "[-6,2]"]),
        ("If $f(x)=2x-1$ and $g(x)=x^2$, what is $(f\\circ g)(3)$?",
         17,
         "Inside first: $g(3)=9$. Then $f(9)=2(9)-1=17$.",
         None),
        ("If $f(x)=x+4$ and $g(x)=3x$, compute $(g\\circ f)(-2)$.",
         6,
         "$f(-2)=2$, then $g(2)=6$. Composition is not commutative.",
         None),
        ("Given $f(x)=\\sqrt{x}$ and $g(x)=x-9$, which composition is defined at $x=5$?",
         "g(f(5))",
         "$f(5)=\\sqrt{5}$ is defined, then $g$ of that is fine. $f(g(5))=\\sqrt{-4}$ is not real.",
         ["f(g(5))", "neither composition", "both equally"]),
        ("If $h(x)=(f\\circ g)(x)=4x+7$ and $g(x)=x+1$, what is $f(x)$?",
         "4x+3",
         "$(f\\circ g)(x)=f(x+1)=4x+7$. Let $u=x+1$, so $f(u)=4(u-1)+7=4u+3$.",
         ["4x+7", "4x+11", "x+7"]),
        ("The domain of $(f\\circ g)(x)$ when $g(x)=\\dfrac{1}{x}$ and $f(x)=\\sqrt{x-2}$ requires:",
         "0<x\u22641/2",
         "Need $x\\neq0$ and $g(x)\\geq2$, so $1/x\\geq2$. For positive $x$, $x\\leq1/2$.",
         ["all x\u22600", "x\u22652", "x>2"]),
        ("Find $f^{-1}(x)$ if $f(x)=3x-12$.",
         "(x+12)/3",
         "Swap: $x=3y-12$, then $y=(x+12)/3$.",
         ["(x-12)/3", "3x+12", "x/3-12"]),
        ("If $f(x)=\\dfrac{x+1}{x-2}$, what is $f^{-1}(3)$?",
         "7/2",
         "Solve $\\dfrac{x+1}{x-2}=3$: $x+1=3x-6$, so $7=2x$, $x=7/2$.",
         ["2", "5", "1"]),
        ("A one-to-one function satisfies $f(4)=11$. What is $f^{-1}(11)$?",
         4,
         "The inverse undoes $f$, so the output $11$ is sent back to the original input $4$.",
         None),
        ("Which function fails to have an inverse on all real numbers without a domain restriction?",
         "f(x)=x^2",
         "Two inputs, $3$ and $-3$, share the output $9$, so $x^2$ is not one-to-one on $\\mathbb{R}$.",
         ["f(x)=2x+1", "f(x)=e^x", "f(x)=x^3"]),
        ("If $f(x)=5x+2$, then $(f\\circ f^{-1})(9)$ equals:",
         9,
         "By definition $f\\circ f^{-1}$ is the identity on the range of $f$.",
         ["2", "47", "11"]),
        ("The graph of $y=f^{-1}(x)$ is obtained from $y=f(x)$ by:",
         "reflecting over y=x",
         "Swapping coordinates $(a,b)\\mapsto(b,a)$ is reflection across the diagonal $y=x$.",
         ["reflecting over the x-axis", "rotating 90°", "shifting right 1"]),
        ("If $f$ contains the point $(2,7)$, the inverse graph must contain:",
         "(7,2)",
         "Every point $(a,b)$ on $f$ becomes $(b,a)$ on $f^{-1}$.",
         ["(2,7)", "(-2,-7)", "(2,-7)"]),
        ("A horizontal line $y=4$ meets $y=f(x)$ twice. What does that say about inverses?",
         "f is not one-to-one",
         "Two inputs share output $4$, so no single inverse function exists on that domain.",
         ["f has two inverses that are functions", "f is even", "the inverse is a parabola"]),
        ("On the graph of $f(x)=2x+1$ and its inverse, the intersection points besides the identity check lie on:",
         "y=x",
         "A function that is its own inverse would lie on $y=x$; here they meet the line $y=x$ at the unique solution of $2x+1=x$.",
         ["the y-axis", "x=2", "a circle"]),
        ("If the original graph is increasing, the inverse graph is:",
         "also increasing",
         "Reflection over $y=x$ preserves the increasing character of a strictly increasing function.",
         ["always decreasing", "always even", "always a parabola"]),
        ("$f(x)=x^2-9$ is even because:",
         "f(-x)=f(x) for all x",
         "$(-x)^2-9=x^2-9$, so the graph is symmetric about the y-axis.",
         ["f(-x)=-f(x)", "f(0)=0", "it has two zeros"]),
        ("Which of the following is an odd function?",
         "f(x)=x^3-x",
         "$f(-x)=-x^3+x=-(x^3-x)=-f(x)$.",
         ["f(x)=x^2+1", "f(x)=|x|", "f(x)=x^2-x"]),
        ("If $f$ is even and $f(3)=10$, then $f(-3)$ equals:",
         10,
         "Even functions satisfy $f(-x)=f(x)$, so the outputs match.",
         ["-10", "0", "3"]),
        ("A function that is both even and odd on $\\mathbb{R}$ must be:",
         "the zero function",
         "$f(-x)=f(x)$ and $f(-x)=-f(x)$ force $f(x)=0$.",
         ["f(x)=x", "f(x)=x^2", "any constant"]),
        ("The graph of an odd function is symmetric about:",
         "the origin",
         "Point symmetry through $(0,0)$ is the geometric meaning of $f(-x)=-f(x)$.",
         ["the y-axis", "the line y=x", "x=1"]),
        ("For $f(x)=\\begin{cases}2x+1 & x<0\\\\ x^2 & x\\geq0\\end{cases}$, find $f(-3)$.",
         -5,
         "$-3<0$, so use $2x+1$: $2(-3)+1=-5$.",
         None),
        ("Using the same piecewise rule, $f(4)$ equals:",
         16,
         "$4\\geq0$, so use $x^2$: $16$.",
         None),
        ("$|x-3|=5$ has solutions:",
         "x=8 or x=-2",
         "Distance from $3$ is $5$, so $x=3+5=8$ or $x=3-5=-2$.",
         ["x=8 only", "x=2 only", "x=15"]),
        ("Rewrite $y=|2x-4|$ as a piecewise rule.",
         "2x-4 if x\u22652, 4-2x if x<2",
         "The inside is zero at $x=2$. For $x\\geq2$ drop the bars; for $x<2$ negate.",
         ["2x-4 for all x", "4-2x for all x", "x-2"]),
        ("Evaluate $g(x)=\\begin{cases}5 & x\\leq1\\\\ 3x & x>1\\end{cases}$ at the boundary $x=1$.",
         5,
         "The first piece includes $x=1$ because of $\\leq$.",
         ["3", "8", "undefined"]),
        ("If $f(x)=x-8$ and $g(x)=x^2$, then $(f\\circ g)(-3)$ is:",
         1,
         "$g(-3)=9$, then $f(9)=1$.",
         None),
        ("The range of $f(x)=\\dfrac{1}{x-5}$ is all reals except:",
         "y=0",
         "A nonzero number over a linear denominator never hits $0$.",
         ["y=5", "y=1", "no exceptions"]),
        ("Solve $|(x+1)|=|x-7|$.",
         "x=3",
         "The point equidistant from $-1$ and $7$ is the midpoint $x=3$.",
         ["x=4", "x=0", "x=8"]),
        ("If $(g\\circ f)(x)=x$ and $(f\\circ g)(x)=x$ on matching domains, then $g$ is:",
         "the inverse of f",
         "Those two identities are the definition of inverse functions.",
         ["a constant", "even", "equal to f"]),
        ("Domain of $f(x)=\\sqrt{4-x^2}$ is:",
         "[-2,2]",
         "$4-x^2\\geq0\\Rightarrow x^2\\leq4\\Rightarrow -2\\leq x\\leq2$.",
         ["all reals", "(0,2]", "x\u22652"]),
        ("$f(x)=|x|+|x-2|$ for $x$ in $(0,2)$ simplifies to:",
         "2",
         "On $(0,2)$: $|x|=x$ and $|x-2|=2-x$, so the sum is $2$.",
         ["2x", "2x-2", "0"]),
        ("If $f$ is odd and $f(5)=-12$, then $f(-5)$ is:",
         12,
         "$f(-5)=-f(5)=-(-12)=12$.",
         ["-12", "0", "5"]),
        ("Find $(f\\circ f)(x)$ for $f(x)=\\dfrac{1}{x}$, $x\\neq0$.",
         "x",
         "$f(f(x))=1/(1/x)=x$, so $f$ is an involution (its own inverse).",
         ["1/x^2", "1", "x^2"]),
        ("Which statement is true of $y=|x|$ on $\\mathbb{R}$?",
         "even, not one-to-one",
         "It is symmetric about the y-axis and fails the horizontal line test.",
         ["odd and one-to-one", "odd but not even", "a linear function"]),
        ("If $f(x)=2x+3$ and $g(x)=x/2-3/2$, then $(f\\circ g)(10)$ equals:",
         10,
         "$g$ was built as $f^{-1}$, so the composition returns $10$.",
         ["13", "23", "5"]),
        ("The graph of $y=f(x)$ passes the horizontal line test. Therefore:",
         "f is one-to-one",
         "Each output comes from at most one input, which is exactly one-to-one.",
         ["f is even", "f has a hole", "f is periodic"]),
        ("$f(x)=\\begin{cases}x+2 & x<1\\\\ 4-x & x\\geq1\\end{cases}$. Is $f$ continuous at $1$ in the piecewise sense of matching values?",
         "yes, both pieces give 3",
         "Left piece at $1$ would be $3$; the defined piece $4-1=3$.",
         ["no, 3 vs 4", "undefined", "only from the right"]),
        ("If $f(g(x))=3x-1$ and $g(x)=x+4$, then $f(2)$ equals:",
         -7,
         "Set the inner output equal to $2$: $x+4=2$ so $x=-2$. Then $f(2)=(f\\circ g)(-2)=3(-2)-1=-7$.",
         ["5", "11", "2"]),
        ("A table shows $f(1)=4$, $f(4)=7$, $f(7)=1$. Then $(f\\circ f\\circ f)(1)$ is:",
         1,
         "$f(1)=4$, $f(4)=7$, $f(7)=1$, a 3-cycle.",
         ["4", "7", "0"]),
        ("Range of $f(x)=\\sqrt{x+6}$ is:",
         "y\u22650",
         "A principal square root never outputs a negative.",
         ["y\u2265-6", "all reals", "y>6"]),
        ("SAT Stretch: $f(x)=\\dfrac{2x-1}{x+3}$ ($x\\neq-3$). If $g=f^{-1}$, what is $(g\\circ f\\circ g)(5)$?",
         "-16/3",
         "Because $f\\circ g$ is the identity on the domain of $g$, $(g\\circ f\\circ g)(5)=g(5)=f^{-1}(5)$. "
         "Solve $\\dfrac{2x-1}{x+3}=5$: $2x-1=5x+15$, so $-16=3x$ and $x=-16/3$.",
         ["5", "2", "8/3"]),
        ("SAT Stretch: Restrict $f(x)=x^2-4x$ to $[2,\\infty)$. Find $f^{-1}(5)$.",
         5,
         "Complete the square: $f(x)=(x-2)^2-4$. Set $(x-2)^2-4=5$, $(x-2)^2=9$, $x-2=\\pm3$. "
         "The restricted domain forces $x-2\\geq0$, so $x=5$.",
         ["-1", "2", "9"]),
        ("SAT Stretch: If $(f\\circ g)(x)=\\dfrac{x-1}{x+2}$ and $g(x)=\\dfrac{1}{x}$, find $f(x)$.",
         "(1-x)/(1+2x)",
         "$f(1/x)=(x-1)/(x+2)$. Let $u=1/x$ so $x=1/u$. Then $f(u)=((1/u)-1)/((1/u)+2)=(1-u)/(1+2u)$.",
         ["(x-1)/(x+2)", "x/(x+2)", "(1+x)/(1-2x)"]),
        ("SAT Stretch: $f$ is odd, $g$ is even, both defined on $\\mathbb{R}$. Then $h=f\\circ g$ is:",
         "even",
         "$h(-x)=f(g(-x))=f(g(x))=h(x)$, so $h$ is even.",
         ["odd", "neither", "one-to-one"]),
        ("SAT Stretch: Inverse of $f(x)=\\begin{cases}x+2 & x\\leq0\\\\ 2x+2 & x>0\\end{cases}$ at $y=8$ is:",
         3,
         "For $y>2$ use the second piece: $2x+2=8$, $x=3>0$, consistent. The first piece cannot produce $8$.",
         ["6", "4", "2"]),
        ("SAT Stretch: Domain of $\\sqrt{g(f(x))}$ if $f(x)=x-5$ and $g(t)=6-t$ is:",
         "x\u226411",
         "Need $g(f(x))\\geq0$: $6-(x-5)\\geq0\\Rightarrow 11-x\\geq0\\Rightarrow x\\leq11$.",
         ["x\u22655", "x\u22656", "all reals"]),
        ("SAT Stretch: $f(x)=ax+b$ with $f(f(x))=x$ for all $x$, and $f$ is not the identity. Then:",
         "a=-1",
         "$f(f(x))=a(ax+b)+b=a^2x+ab+b=x$ for all $x$ forces $a^2=1$ and $b(a+1)=0$. "
         "Not the identity means we reject $a=1,b=0$, so $a=-1$ (with $b$ free).",
         ["a=1", "b=0 only", "a=2"]),
        ("SAT Stretch: Points $(1,4)$ and $(4,1)$ both lie on $y=f(x)$. Can $f$ equal $f^{-1}$ as functions?",
         "yes, if those are corresponding swapped points on an involution",
         "An involution satisfies $f=f^{-1}$, so it is symmetric across $y=x$. Both points being present is consistent with that.",
         ["never", "only if f is even", "only if f is linear with slope 2"]),
        ("SAT Stretch: $f(x)=\\dfrac{3x+1}{x-1}$ ($x\\neq1$). The value of $x$ where $f(x)=x$ (fixed points) solves:",
         "x^2-4x-1=0",
         "$3x+1=x(x-1)=x^2-x$, so $0=x^2-4x-1$.",
         ["x^2-1=0", "3x+1=0", "x=1"]),
        ("SAT Stretch: If $f(x)=2x+1$ and $g(x)=x^3$, then $(f\\circ g)^{-1}(17)$ equals:",
         2,
         "$(f\\circ g)(x)=2x^3+1$. Set $2x^3+1=17$, so $x^3=8$ and $x=2$. "
         "Composing first, then inverting, is the same as $g^{-1}(f^{-1}(17))$.",
         ["8", "9", "16"]),
    ])
    return qs[:55]


def build_unit1():
    title = "Precalculus Unit 1: Functions, Composition & Inverses"
    description = (
        "Domain, range, composition, algebraic and graphical inverses, even/odd symmetry, "
        "and piecewise/absolute-value rules — with matching graphs and a hard SAT stretch set."
    )
    concepts = [
        "Domain and range review",
        "Composition",
        "Inverses algebraically",
        "Inverses graphically",
        "Even/odd and symmetry",
        "Piecewise and absolute value",
    ]

    c1 = concept_block(
        "1. Domain and range review",
        [
            "A function is a rule that assigns each allowed input exactly one output. The domain is the complete "
            "set of those allowed inputs; the range is the complete set of outputs the rule actually produces. "
            "In Precalculus you almost always work over the real numbers, so “allowed” means “does not break "
            "a real-number operation.”",
            "Two operations create the restrictions you will see over and over. Division is undefined when the "
            "denominator is $0$. An even root (square root, fourth root, and so on) is undefined in the reals "
            "when the inside expression is negative. A logarithm, which returns in Unit 3, will add a third "
            "restriction: its argument must be strictly positive.",
            "For a rational example such as $f(x)=\\dfrac{x+1}{x^2-9}$, factor the denominator as $(x-3)(x+3)$ "
            "and exclude $x=3$ and $x=-3$. The numerator being zero at $x=-1$ does not remove that input from "
            "the domain; it only creates an $x$-intercept. Domain cares about whether the expression can be "
            "evaluated, not about whether the output happens to be zero.",
            "For a radical example such as $g(x)=\\sqrt{8-x}$, require $8-x\\geq0$, hence $x\\leq8$. If that "
            "radical sits in a denominator, as in $\\dfrac{1}{\\sqrt{8-x}}$, the inequality becomes strict: "
            "$8-x>0$, because a denominator cannot be zero either. Nested restrictions must all be satisfied "
            "at once.",
            "Range is often harder than domain because you must think about which outputs are actually hit. "
            "A parabola $y=(x-1)^2+5$ never outputs anything below $5$. A reciprocal $y=1/(x-5)$ never outputs "
            "$0$. Reading range from a graph means asking: which horizontal lines actually meet the curve?",
            "Getting domain and range fluent now pays off immediately. Composition in the next lesson is only "
            "defined where the inner output lands in the outer domain. Inverses swap domain and range. Rational "
            "graphs in Unit 2 are named by the holes and asymptotes that domain restrictions create.",
        ],
        "Every later Precalculus skill — composition, inverses, rationals, logs, inverse trig — starts by asking "
        "which inputs are legal and which outputs actually occur. A domain error silently invalidates an inverse.",
        "Write the formula, circle every dangerous operation (division, even root, later log), and turn each "
        "danger into an inequality or an exclusion. Then, separately, ask what $y$-values are produced.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: math.sqrt(x - 4) if x >= 4 else 1e9, 4, 12))],
                points=[(4, 0, "(4,0)")],
                xlim=(0, 12), ylim=(-1, 4),
            ),
            "Domain of $f(x)=\\sqrt{x-4}$ starts at $x=4$",
            "The graph exists only for $x\\geq4$. The closed endpoint $(4,0)$ is included.",
        )
        + solved(
            1, "Find the domain of $f(x)=\\dfrac{1}{x-7}$.",
            ["The only illegal operation is division by zero.",
             "Set the denominator equal to zero: $x-7=0$, so $x=7$ is excluded.",
             "Every other real number is allowed."],
            "$x\\neq7$", "", "Easy",
        )
        + solved(
            2, "Find the domain of $g(x)=\\sqrt{x-2}$.",
            ["An even root requires a nonnegative inside: $x-2\\geq0$.",
             "Add $2$ to both sides: $x\\geq2$.",
             "The endpoint $x=2$ is included because $\\sqrt{0}=0$ is defined."],
            "$x\\geq2$", "Closed at $2$; the graph starts at the point $(2,0)$.", "Medium",
        )
        + solved(
            3, "Find the domain of $h(x)=\\dfrac{1}{\\sqrt{8-x}}$.",
            ["Two restrictions: the inside of the square root must be nonnegative, and the denominator cannot be $0$.",
             "Together these force $8-x>0$, so $x<8$.",
             "Check a test point: $x=0$ gives $1/\\sqrt{8}$, which is fine; $x=8$ gives $1/0$, which is not."],
            "$x<8$", "The inequality is strict because the radical sits in a denominator.", "Hard",
        ),
        ("Treating a zero numerator as a domain problem",
         "If the numerator is zero, the output is zero — that is an $x$-intercept, not a domain hole. Only a "
         "zero denominator (or a negative even-root inside, or a nonpositive log argument) removes an input."),
        ("Factor first, then exclude",
         "On a multiple-choice domain question, factor every denominator and every even-root inside before "
         "you pick an answer. The excluded values are the roots of those factors, with multiplicity ignored."),
        [
            "I can exclude inputs that make a denominator zero.",
            "I can write the inequality for an even-root domain, strict when it sits in a denominator.",
            "I can read a simple range from a vertex or from a reciprocal that never hits zero.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Composition",
        [
            "The composition $(f\\circ g)(x)$ means $f(g(x))$: evaluate the inner function $g$ first, then feed "
            "that output into the outer function $f$. The circle notation is not multiplication. Reading it "
            "aloud as “$f$ of $g$ of $x$” keeps the order straight.",
            "Composition is not commutative. $(f\\circ g)(x)$ and $(g\\circ f)(x)$ are usually different functions. "
            "A reliable habit is to compute a numeric example both ways whenever you are unsure of the order, "
            "and to write the inner function in parentheses before you simplify.",
            "Algebraically, substitute the entire inner formula wherever the outer function has its input "
            "variable. If $f(x)=2x-1$ and $g(x)=x^2$, then $(f\\circ g)(x)=2(x^2)-1=2x^2-1$, while "
            "$(g\\circ f)(x)=(2x-1)^2=4x^2-4x+1$. Those are visibly different polynomials.",
            "The domain of $f\\circ g$ is not automatically the domain of $g$. An input $x$ is allowed only when "
            "$x$ is in the domain of $g$ and the number $g(x)$ is in the domain of $f$. That second requirement "
            "is the one students skip, and it is the one that produces the interesting inequalities.",
            "You can also undo a composition. If you are told $(f\\circ g)(x)$ and you know $g$, you can recover "
            "$f$ by substituting $u=g(x)$ and rewriting the formula in terms of $u$. This skill is exactly "
            "what inverse functions will use: an inverse is the function that “undoes” a composition back to $x$.",
            "Later in this unit you will compose a function with its inverse and get the identity. In Unit 3 you "
            "will compose $a^x$ with $\\log_a x$ and get $x$. Composition is the verb of Precalculus; almost "
            "every later identity is a statement about two functions composed.",
        ],
        "Inverses, change of base, trig identities, and parametric elimination are all composition in disguise. "
        "If the inner/outer order is shaky, those later topics feel like new languages instead of one idea.",
        "Always evaluate inside-out. Write $g(x)$ as a single number or a single expression, put parentheses "
        "around it, and only then apply $f$. Check the domain of the outer function at that inner output.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#4f46e5", sample_curve(lambda x: x ** 2, -2.5, 2.5)),
                    ("#dc2626", sample_curve(lambda x: 2 * x ** 2 - 1, -2.5, 2.5)),
                ],
                points=[(2, 4, "g(2)=4"), (2, 7, "(f\u2218g)(2)=7")],
                xlim=(-3, 3), ylim=(-2, 10),
            ),
            "$(f\\circ g)(x)=2x^2-1$ when $f(x)=2x-1$ and $g(x)=x^2$",
            "At $x=2$, the inner parabola gives $4$, then the outer linear rule sends $4$ to $7$.",
        )
        + solved(
            4, "If $f(x)=2x-1$ and $g(x)=x^2$, find $(f\\circ g)(3)$.",
            ["Inner first: $g(3)=3^2=9$.",
             "Outer next: $f(9)=2(9)-1=18-1=17$.",
             "As a formula, $(f\\circ g)(x)=2x^2-1$, and $2(9)-1=17$ matches."],
            "$17$", "", "Easy",
        )
        + solved(
            5, "If $f(x)=x+4$ and $g(x)=3x$, find $(g\\circ f)(-2)$ and compare with $(f\\circ g)(-2)$.",
            ["$(g\\circ f)(-2)=g(f(-2))=g(2)=6$.",
             "$(f\\circ g)(-2)=f(g(-2))=f(-6)=-2$.",
             "The two orders disagree, which is normal."],
            "$(g\\circ f)(-2)=6$, $(f\\circ g)(-2)=-2$", "Never assume $f\\circ g=g\\circ f$.", "Medium",
        )
        + solved(
            6, "If $(f\\circ g)(x)=4x+7$ and $g(x)=x+1$, find $f(x)$.",
            ["By definition $f(g(x))=f(x+1)=4x+7$.",
             "Let $u=x+1$, so $x=u-1$.",
             "Then $f(u)=4(u-1)+7=4u-4+7=4u+3$.",
             "Rename $u$ as $x$: $f(x)=4x+3$."],
            "$f(x)=4x+3$", "Check: $f(g(x))=4(x+1)+3=4x+7$.", "Hard",
        ),
        ("Doing the outer function first",
         "The notation $(f\\circ g)(x)$ looks as if $f$ comes first because $f$ is written on the left. In "
         "evaluation, $g$ still happens first. If you apply $f$ first you have computed $(g\\circ f)$ by accident."),
        ("Numeric probe for order",
         "When two formulas are in play, pick a simple number such as $x=2$ and evaluate both compositions. "
         "If the answers differ, you have a built-in check that you did not swap $f$ and $g$."),
        [
            "I can evaluate a composition numerically, inside-out.",
            "I can write a formula for $f\\circ g$ by substituting.",
            "I can recover $f$ from $f\\circ g$ when $g$ is known.",
        ],
        6,
    )

    inv_f = sample_curve(lambda x: 2 * x + 1, -3.5, 2.5)
    inv_id = sample_curve(lambda x: x, -6, 6)
    inv_finv = sample_curve(lambda x: (x - 1) / 2, -5, 6)

    c3 = concept_block(
        "3. Inverses algebraically",
        [
            "Two functions $f$ and $g$ are inverses when $(f\\circ g)(x)=x$ and $(g\\circ f)(x)=x$ on the "
            "appropriate domains. In words: $g$ undoes $f$, and $f$ undoes $g$. We write $g=f^{-1}$. The "
            "exponent $-1$ is not a reciprocal; $f^{-1}(x)$ is not $1/f(x)$ except in rare special cases.",
            "A function has an inverse (that is itself a function) precisely when it is one-to-one: each output "
            "comes from exactly one input. The algebraic test is “if $f(a)=f(b)$, then $a=b$.” The graphical "
            "test is the horizontal line test, which the next lesson treats in detail.",
            "The standard algebraic method has four steps. Write $y=f(x)$. Swap $x$ and $y$. Solve the new "
            "equation for $y$. Rename $y$ as $f^{-1}(x)$. For $f(x)=3x-12$ you get $x=3y-12$, hence "
            "$y=(x+12)/3$. That is the inverse.",
            "Sometimes you only need a value $f^{-1}(k)$, not the full formula. Then you can skip the swap and "
            "just solve $f(x)=k$. The solution $x$ is $f^{-1}(k)$. This is faster on tests and is the method "
            "you should use whenever the question asks for one number.",
            "Functions that fail the one-to-one test on their natural domain can still have inverses after a "
            "domain restriction. The classic example is $f(x)=x^2$ restricted to $x\\geq0$, whose inverse is "
            "$\\sqrt{x}$. Restricting to $x\\leq0$ would give $-\\sqrt{x}$ instead. The restriction is a choice "
            "that must be stated.",
            "Always verify. After you think you have $f^{-1}$, compose both ways on a convenient number, or "
            "simplify $(f\\circ f^{-1})(x)$ algebraically and confirm you get $x$. A dropped sign while swapping "
            "is caught immediately by this check.",
        ],
        "Logarithms are defined as inverses of exponentials. Inverse trig is defined the same way. If the "
        "swap-and-solve process is automatic, those later definitions will feel like the same movie with new costumes.",
        "Ask two questions: is $f$ one-to-one on the domain I am using? If yes, swap and solve, then compose "
        "to check. If you only need $f^{-1}(k)$, solve $f(x)=k$ and skip writing the full inverse formula.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", inv_f), ("#16a34a", inv_id), ("#dc2626", inv_finv)],
                points=[(0, 1, "f"), (1, 0, "f^{-1}")],
                xlim=(-6, 6), ylim=(-6, 6),
            ),
            "$f(x)=2x+1$ (blue), $y=x$ (green), $f^{-1}(x)=(x-1)/2$ (red)",
            "The inverse is the reflection of $f$ across the diagonal $y=x$.",
        )
        + solved(
            7, "Find $f^{-1}(x)$ if $f(x)=3x-12$.",
            ["Write $y=3x-12$.",
             "Swap: $x=3y-12$.",
             "Solve: $x+12=3y$, so $y=(x+12)/3$.",
             "Check: $f(f^{-1}(x))=3\\cdot(x+12)/3-12=x$."],
            "$f^{-1}(x)=\\dfrac{x+12}{3}$", "", "Easy",
        )
        + solved(
            8, "If $f(x)=\\dfrac{x+1}{x-2}$, find $f^{-1}(3)$.",
            ["You only need one value, so solve $f(x)=3$.",
             "$\\dfrac{x+1}{x-2}=3$ becomes $x+1=3x-6$.",
             "$7=2x$, so $x=7/2$.",
             "Therefore $f^{-1}(3)=7/2$."],
            "$\\dfrac{7}{2}$", "Exclude $x=2$ while solving; $7/2$ is safe.", "Medium",
        )
        + solved(
            9, "Restrict $f(x)=x^2-4x$ to $[2,\\infty)$ and find $f^{-1}(5)$.",
            ["Complete the square: $f(x)=(x-2)^2-4$.",
             "Set $(x-2)^2-4=5$, so $(x-2)^2=9$, $x-2=\\pm3$.",
             "The restricted domain $[2,\\infty)$ forces $x-2\\geq0$, so $x-2=3$ and $x=5$.",
             "The discarded root $x=-1$ is outside the restricted domain."],
            "$5$", "Without the restriction there would be two answers and no inverse function.", "Hard",
        ),
        ("Reading $f^{-1}$ as a reciprocal",
         "The symbol $f^{-1}(x)$ means the inverse function, not $1/f(x)$. Reciprocals and inverses are different "
         "ideas that unfortunately share a superscript. If a problem wanted $1/f(x)$ it would write that."),
        ("Solve $f(x)=k$ when you only need one value",
         "Writing the entire inverse formula and then substituting $k$ is extra algebra. Set $f(x)=k$ and solve; "
         "the $x$ you get is $f^{-1}(k)$."),
        [
            "I can swap and solve to find an inverse formula.",
            "I can evaluate $f^{-1}(k)$ by solving $f(x)=k$.",
            "I can restrict a domain so that a non-one-to-one formula becomes invertible.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Inverses graphically",
        [
            "Algebraically, an inverse swaps $x$ and $y$ in an equation. Graphically, that swap is a reflection "
            "across the line $y=x$. Every point $(a,b)$ on $y=f(x)$ becomes the point $(b,a)$ on $y=f^{-1}(x)$. "
            "If you remember only one picture from this unit, remember a curve, the diagonal, and the reflected copy.",
            "The horizontal line test is the graphical one-to-one test. If any horizontal line meets the graph "
            "more than once, two inputs share an output, and no inverse function exists on that domain. A strictly "
            "increasing graph (or a strictly decreasing graph) always passes.",
            "You can sketch an inverse without a formula. Plot several points of $f$, swap their coordinates, "
            "plot those new points, and connect them in the same smoothness as the original. The original graph "
            "and the inverse graph are mirrors across $y=x$; they meet that line at the fixed points of $f$.",
            "Domain and range trade places. The domain of $f^{-1}$ is the range of $f$, and the range of $f^{-1}$ "
            "is the domain of $f$. That is why a square-root inverse of $x^2$ (restricted to $x\\geq0$) has "
            "domain $[0,\\infty)$: that interval is the range of the restricted square.",
            "A graph that is already symmetric across $y=x$ is an involution: $f=f^{-1}$. The reciprocal "
            "$y=1/x$ (for $x\\neq0$) is the standard example. Linear functions $y=a-x$ are another family of "
            "involutions. Recognizing them saves you from doing unnecessary algebra.",
            "On a test, if you are given a graph of $f$ and asked a question about $f^{-1}(4)$, look for the "
            "point on $f$ whose $y$-coordinate is $4$; its $x$-coordinate is the answer. You do not need a "
            "formula at all.",
        ],
        "Graphical inverses are how you will later read inverse trig, logarithmic graphs, and the reflection "
        "that turns $y=a^x$ into $y=\\log_a x$. The picture is the definition.",
        "Draw $y=x$ first, lightly. Then either reflect plotted points or, if you have a formula, graph both "
        "$f$ and $f^{-1}$ and confirm they are mirrors. Use the horizontal line test before you claim an inverse exists.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", inv_f), ("#16a34a", inv_id), ("#dc2626", inv_finv)],
                points=[(1, 3, "(1,3) on f"), (3, 1, "(3,1) on f^{-1}")],
                xlim=(-6, 6), ylim=(-6, 6),
            ),
            "Reflecting $(1,3)$ across $y=x$ produces $(3,1)$",
            "The blue line is $f(x)=2x+1$; the red line is its inverse. Green is $y=x$.",
        )
        + solved(
            10, "The graph of $f$ contains $(2,7)$. Name a point on $y=f^{-1}(x)$.",
            ["Inverses swap coordinates.",
             "The point $(2,7)$ becomes $(7,2)$.",
             "That point must lie on the inverse graph."],
            "$(7,2)$", "", "Easy",
        )
        + solved(
            11, "A horizontal line $y=4$ meets $y=f(x)$ at two points. Does $f$ have an inverse function on that domain?",
            ["Two intersection points mean two inputs share the output $4$.",
             "So $f$ is not one-to-one.",
             "Therefore no inverse function exists unless the domain is restricted to remove one of those inputs."],
            "No (not one-to-one)", "This is the horizontal line test failing.", "Medium",
        )
        + solved(
            12, "Using the graph of $f(x)=2x+1$, find $f^{-1}(5)$ by reading a point rather than using a formula.",
            ["You want the input $x$ that $f$ sends to $5$.",
             "On the graph, find the point whose $y$-coordinate is $5$.",
             "Solve $2x+1=5$ to see it is $(2,5)$, so the inverse graph contains $(5,2)$.",
             "Hence $f^{-1}(5)=2$."],
            "$2$", "Graphically: look for $y=5$ on $f$; its $x$ is the inverse value.", "Hard",
        ),
        ("Reflecting over the wrong line",
         "Students sometimes reflect over the $x$-axis or $y$-axis because those are more familiar. Inverse "
         "graphs use the diagonal $y=x$, not an axis. If your “inverse” looks like $-f$ or $f$ flipped left-right, "
         "you used the wrong mirror."),
        ("Read $f^{-1}(k)$ off the original graph",
         "You do not have to sketch the entire inverse. Find the point on $f$ with $y=k$; the $x$-coordinate "
         "of that point is $f^{-1}(k)$."),
        [
            "I can swap coordinates to plot inverse points.",
            "I can apply the horizontal line test.",
            "I can read $f^{-1}(k)$ from a graph of $f$.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Even/odd and symmetry",
        [
            "A function is even if $f(-x)=f(x)$ for every $x$ in a domain that is symmetric about $0$. Even "
            "graphs are symmetric about the $y$-axis. The name comes from even powers: $x^2$, $x^4$, and "
            "$|x|$ are even. A cosine is even, which is why the cosine graph mirrors across the $y$-axis.",
            "A function is odd if $f(-x)=-f(x)$ on a symmetric domain. Odd graphs have origin symmetry: rotating "
            "the picture $180^\\circ$ about $(0,0)$ leaves it looking the same. Odd powers $x$, $x^3$, and "
            "$x^5-x$ are odd. A sine is odd. If $f$ is odd and defined at $0$, then $f(0)=0$.",
            "To test a formula, compute $f(-x)$ carefully — every $x$ gets a minus — and simplify. If you "
            "recover $f(x)$, the function is even. If you recover $-f(x)$, it is odd. If you recover neither, "
            "it is neither (the usual case). Do not stop at “it has an $x^2$ in it”; mixed terms such as "
            "$x^2-x$ are neither.",
            "Even and odd interact with composition. If $g$ is even, then $f\\circ g$ is even no matter what "
            "$f$ is (on a symmetric domain), because $g(-x)=g(x)$ already. If $f$ is odd and $g$ is odd, then "
            "$f\\circ g$ is odd. These facts are SAT favorites because they let you classify a composition "
            "without writing a formula.",
            "A function that is both even and odd must satisfy $f(x)=-f(x)$, hence $f(x)=0$. So the only "
            "function that is both is the zero function. Constant functions $f(x)=c$ with $c\\neq0$ are even "
            "but not odd. The identity $f(x)=x$ is odd but not even.",
            "Symmetry is a graphing shortcut. If you know a polynomial is even, you only need to plot $x\\geq0$ "
            "and mirror. If you know it is odd, you plot $x\\geq0$ and rotate through the origin. In Unit 4, "
            "even/odd is how you remember which trig functions are cosines versus sines.",
        ],
        "Even/odd classification is the fastest way to predict a graph’s mirror, to simplify a definite-looking "
        "integral later in calculus, and to answer “what is $f(-3)$ if $f$ is even and $f(3)=10$?” in two seconds.",
        "Compute $f(-x)$ with parentheses around every substituted $-x$. Compare the simplified result to "
        "$f(x)$ and to $-f(x)$. If the domain is not symmetric about $0$, do not call the function even or odd.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#4f46e5", sample_curve(lambda x: x ** 2 - 9, -4, 4)),
                    ("#dc2626", sample_curve(lambda x: x ** 3 - x, -2.2, 2.2)),
                ],
                points=[(3, 0, "even zeros"), (-3, 0, "")],
                xlim=(-5, 5), ylim=(-10, 8),
            ),
            "Blue $y=x^2-9$ is even (y-axis symmetry); red $y=x^3-x$ is odd (origin symmetry)",
            "Mirror the blue graph across the y-axis and it matches itself. Rotate the red graph $180^\\circ$ about the origin.",
        )
        + solved(
            13, "Show that $f(x)=x^2-9$ is even, and use that to find $f(-3)$.",
            ["$f(-x)=(-x)^2-9=x^2-9=f(x)$, so $f$ is even.",
             "Even means $f(-3)=f(3)$.",
             "$f(3)=0$, so $f(-3)=0$."],
            "$f(-3)=0$", "The zeros $\\pm3$ are mirrors, as evenness requires.", "Easy",
        )
        + solved(
            14, "Determine whether $f(x)=x^3-x$ is even, odd, or neither.",
            ["$f(-x)=(-x)^3-(-x)=-x^3+x=-(x^3-x)=-f(x)$.",
             "This is the odd-function identity.",
             "Therefore $f$ is odd (and not even, since it is not the zero function)."],
            "odd", "", "Medium",
        )
        + solved(
            15, "$f$ is odd and $g$ is even, both on $\\mathbb{R}$. Classify $h=f\\circ g$.",
            ["$h(-x)=f(g(-x))$.",
             "Evenness of $g$ gives $g(-x)=g(x)$.",
             "So $h(-x)=f(g(x))=h(x)$.",
             "Hence $h$ is even, regardless of $f$ being odd."],
            "even", "Inner even function “washes out” the sign of $x$ before $f$ ever sees it.", "Hard",
        ),
        ("Calling $x^2-x$ even because it “has a square”",
         "A single odd-degree term ruins evenness. $f(-x)=x^2+x$, which equals neither $f(x)=x^2-x$ nor "
         "$-f(x)$. Mixed parity is neither even nor odd."),
        ("Test with $x$ and $-x$, not with one lucky number",
         "A single check such as $f(2)=f(-2)$ is necessary but not sufficient. Prove the identity $f(-x)=f(x)$ "
         "algebraically, or know the graph’s symmetry from a parent function."),
        [
            "I can test even/odd by simplifying $f(-x)$.",
            "I can read y-axis versus origin symmetry on a graph.",
            "I can classify a composition $f\\circ g$ from the parities of $f$ and $g$.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Piecewise and absolute value",
        [
            "A piecewise function uses different formulas on different parts of the domain. The first job is "
            "always to decide which piece an input belongs to, including the boundary. Look at the inequality "
            "attached to each piece: $\\leq$ versus $<$ tells you which formula owns the endpoint.",
            "Absolute value is piecewise in disguise. By definition $|u|=u$ when $u\\geq0$ and $|u|=-u$ when "
            "$u<0$. For $y=|2x-4|$, the inside is zero at $x=2$, so the graph is the V with vertex $(2,0)$: "
            "the right ray is $y=2x-4$ and the left ray is $y=4-2x$.",
            "Equations with absolute values split into cases. $|x-3|=5$ means the distance from $x$ to $3$ is "
            "$5$, so $x=8$ or $x=-2$. Equations such as $|x-1|=|x-7|$ are solved by the midpoint (the points "
            "equidistant from $1$ and $7$) or by squaring both sides after confirming both sides are nonnegative.",
            "Inequalities with absolute values become compound statements. $|x-3|<5$ is the open interval "
            "$(-2,8)$. $|x-3|\\geq5$ is the outside: $x\\leq-2$ or $x\\geq8$. Drawing a number line and marking "
            "the two critical points is faster and safer than memorizing which inequality flips.",
            "Piecewise graphs are drawn piece by piece, with a closed dot on an included endpoint and an open "
            "dot on an excluded endpoint. Continuity at a joint is not required for the rule to be a function; "
            "it is required only if a problem asks for a continuous piecewise definition.",
            "Inverses of piecewise functions are also piecewise, but the pieces are expressed in terms of $y$. "
            "You invert each invertible piece on its range, then reassemble. This is a stretch skill: check that "
            "the $x$ you get actually belongs to the piece you used.",
        ],
        "Absolute value is the language of distance, error, and piecewise linear graphs. Piecewise rules appear "
        "in tax tables, shipping costs, and in the definition of $|x|$ that calculus later differentiates.",
        "For a numeric input, first name the piece, then substitute. For $|ax+b|$, find the vertex by setting "
        "the inside to zero, then write two linear pieces. For inequalities, mark the two critical numbers and shade.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: abs(2 * x - 4), -1, 5))],
                points=[(2, 0, "vertex (2,0)"), (0, 4, "(0,4)"), (4, 4, "(4,4)")],
                xlim=(-2, 6), ylim=(-1, 8),
            ),
            "$y=|2x-4|$ is a V with vertex at $x=2$",
            "Left of $x=2$ the graph is $y=4-2x$; right of $x=2$ it is $y=2x-4$.",
        )
        + solved(
            16, "For $f(x)=\\begin{cases}2x+1 & x<0\\\\ x^2 & x\\geq0\\end{cases}$, find $f(-3)$ and $f(4)$.",
            ["$-3<0$, so use $2x+1$: $f(-3)=-5$.",
             "$4\\geq0$, so use $x^2$: $f(4)=16$.",
             "The boundary $x=0$ belongs to the second piece: $f(0)=0$."],
            "$f(-3)=-5$, $f(4)=16$", "", "Easy",
        )
        + solved(
            17, "Solve $|x-3|=5$.",
            ["Distance from $3$ equals $5$.",
             "$x=3+5=8$ or $x=3-5=-2$.",
             "Check: $|8-3|=5$ and $|-2-3|=5$."],
            "$x=8$ or $x=-2$", "", "Medium",
        )
        + solved(
            18, "Rewrite $y=|2x-4|$ as a piecewise function, then evaluate $y$ at $x=0$ two ways.",
            ["Inside zero at $x=2$.",
             "For $x\\geq2$, $y=2x-4$. For $x<2$, $y=-(2x-4)=4-2x$.",
             "$x=0<2$, so $y=4-0=4$.",
             "Directly: $|0-4|=4$, which matches."],
            "$y=\\begin{cases}2x-4 & x\\geq2\\\\ 4-2x & x<2\\end{cases}$; $y(0)=4$",
            "The two rays meet at the vertex $(2,0)$.", "Hard",
        ),
        ("Using the wrong piece at a closed endpoint",
         "If the definition says $x\\leq1$ on the first piece, then $x=1$ uses the first piece, even if the "
         "second piece would have given a different number. The inequality, not your preference, owns the boundary."),
        ("Vertex first for absolute value",
         "Set the inside equal to zero to locate the V. Then test one point on each side to see which linear "
         "expression to keep. This is faster than expanding cases from scratch every time."),
        [
            "I can evaluate a piecewise rule, including at endpoints.",
            "I can split an absolute value into two linear pieces.",
            "I can solve $|x-a|=b$ as two distances from $a$.",
        ],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title, AUDIENCE, concepts, body, practice_slots(31, 25, STRETCH_LABEL),
    )
    return title, description, content, _u1_questions()


# ===========================================================================
# UNIT 2: Polynomial & Rational Functions
# ===========================================================================

def _u2_questions():
    qs = []
    _add(qs, [
        ("As $x\\to+\\infty$, $p(x)=-2x^3+5x$ tends to:",
         "-\u221e",
         "Odd degree with negative leading coefficient: the right end dives down.",
         ["+\u221e", "0", "5"]),
        ("The zeros of $p(x)=(x+2)(x-1)(x-3)$ are:",
         "-2, 1, and 3",
         "Each factor $x-r$ contributes a root $r$.",
         ["2, -1, -3", "only 1 and 3", "0, 1, 3"]),
        ("A cubic with a double root at $x=1$ and a simple root at $x=-4$ could be:",
         "(x-1)^2(x+4)",
         "Multiplicity two at $1$ and multiplicity one at $-4$.",
         ["(x-1)(x+4)^2", "(x+1)^2(x-4)", "x^2-1"]),
        ("End behavior of $q(x)=4x^4-x$ matches which parent?",
         "both ends up (like x^4)",
         "Even degree, positive leading coefficient: both ends rise.",
         ["both ends down", "left up right down", "left down right up"]),
        ("If $p$ is degree $5$ with positive leading coefficient, as $x\\to-\\infty$ we have $p(x)\\to$:",
         "-\u221e",
         "Odd degree, positive lead: left end down, right end up.",
         ["+\u221e", "0", "the y-intercept"]),
        ("The remainder when $x^3-2x+4$ is divided by $x-1$ is:",
         3,
         "Remainder theorem: $p(1)=1-2+4=3$.",
         None),
        ("If $p(2)=0$ for a polynomial $p$, then which factor is guaranteed?",
         "x-2",
         "Factor theorem: a root $c$ produces a factor $x-c$.",
         ["x+2", "x-1", "2x"]),
        ("Synthetic division of $x^3-6x^2+11x-6$ by $x-1$ yields quotient:",
         "x^2-5x+6",
         "Bring down $1$; synthetic row: $1$, $-5$, $6$, remainder $0$.",
         ["x^2-6x+5", "x^2+5x+6", "x-6"]),
        ("$p(x)=x^3+x^2-4x-4$ has $p(-1)=0$. A factorization is:",
         "(x+1)(x^2-4)",
         "Divide by $x+1$ to get $x^2-4$, then $(x+1)(x-2)(x+2)$.",
         ["(x-1)(x^2-4)", "(x+1)(x^2+4)", "x(x^2-4)"]),
        ("The remainder of $p(x)$ divided by $x+3$ equals:",
         "p(-3)",
         "Remainder theorem uses the root of the divisor $x-c$ with $c=-3$.",
         ["p(3)", "p(0)", "the leading coefficient"]),
        ("Near a simple zero of a cubic, the graph:",
         "crosses the x-axis",
         "Odd multiplicity: the graph changes sign and crosses.",
         ["bounces off the x-axis", "has a hole", "becomes a horizontal asymptote"]),
        ("At a zero of even multiplicity the graph:",
         "touches and turns back",
         "The sign does not change, so the graph bounces.",
         ["crosses with a vertical tangent always", "jumps", "stops"]),
        ("$p(x)=(x+2)(x-1)^2$ has which turning behavior at $x=1$?",
         "bounce (multiplicity 2)",
         "Even multiplicity at $1$; it touches and turns.",
         ["cross", "hole", "vertical asymptote"]),
        ("A polynomial of degree $4$ can have at most how many turning points?",
         3,
         "At most $n-1$ turning points for degree $n$.",
         ["4", "5", "1"]),
        ("The y-intercept of $p(x)=x^3-4x+6$ is:",
         6,
         "$p(0)$ is the constant term.",
         ["-4", "0", "1"]),
        ("$f(x)=\\dfrac{x+1}{x-2}$ has a vertical asymptote at:",
         "x=2",
         "The denominator is zero at $x=2$ and the numerator is not.",
         ["x=-1", "y=2", "x=1"]),
        ("The horizontal asymptote of $f(x)=\\dfrac{3x-1}{x+4}$ is:",
         "y=3",
         "Equal degree: ratio of leading coefficients $3/1=3$.",
         ["y=0", "y=-1", "x=3"]),
        ("For $g(x)=\\dfrac{2x^2+1}{x^3-x}$, as $x\\to\\infty$ the graph approaches:",
         "y=0",
         "Denominator degree larger: horizontal asymptote $y=0$.",
         ["y=2", "y=1", "no horizontal asymptote"]),
        ("$h(x)=\\dfrac{x^2+1}{x-1}$ has which end-behavior model?",
         "slant (oblique) asymptote",
         "Numerator degree is exactly one more than the denominator, so divide to get a linear slant.",
         ["y=0", "y=1", "a hole only"]),
        ("Compare degrees: if deg(num)=deg(den), the horizontal asymptote is:",
         "y = leading/leading",
         "The ratio of leading coefficients is the height of the horizontal asymptote.",
         ["always y=0", "always y=1", "there is never one"]),
        ("$f(x)=\\dfrac{(x-3)(x+1)}{(x-3)(x-2)}$ has a hole at:",
         "x=3",
         "The factor $x-3$ cancels, removing a point rather than an asymptote.",
         ["x=2", "x=-1", "x=0"]),
        ("After cancelling, that same $f$ has a vertical asymptote at:",
         "x=2",
         "The surviving denominator factor is $x-2$.",
         ["x=3", "x=-1", "none"]),
        ("The x-intercept of $f(x)=\\dfrac{x+1}{x-2}$ is:",
         "(-1,0)",
         "Numerator zero (and denominator not) at $x=-1$.",
         ["(2,0)", "(0,-1/2)", "(1,0)"]),
        ("The y-intercept of $f(x)=\\dfrac{x+1}{x-2}$ is:",
         "(0,-1/2)",
         "$f(0)=1/(-2)=-1/2$.",
         ["(0,1)", "(0,2)", "(0,-1)"]),
        ("A cancelled factor $(x-a)$ in both numerator and denominator produces:",
         "a hole at x=a",
         "The simplified function is undefined at $a$ but has a removable discontinuity there.",
         ["a vertical asymptote at x=a", "an extra intercept", "a slant asymptote"]),
        ("Solve $\\dfrac{x-1}{x+2}>0$ using a sign chart. The solution is:",
         "x<-2 or x>1",
         "Critical points $-2$ (undefined) and $1$ (zero). Positive on $(-\\infty,-2)$ and $(1,\\infty)$.",
         ["-2<x<1", "x>1 only", "all x\u2260-2"]),
        ("$\\dfrac{x+3}{x-1}\\leq0$ includes which endpoint?",
         "x=-3",
         "A zero of the numerator is allowed for $\\leq0$; $x=1$ is never allowed.",
         ["x=1", "both -3 and 1", "neither"]),
        ("On a sign chart, a vertical asymptote of odd multiplicity:",
         "changes the sign",
         "Odd-order factors change sign when you cross them; even-order factors do not.",
         ["never changes the sign", "is always included in the solution", "must be a hole"]),
        ("The inequality $(x-2)(x+1)\\geq0$ solves as:",
         "x\u2264-1 or x\u22652",
         "Parabola opening up is nonnegative outside the roots.",
         ["-1\u2264x\u22642", "x\u22652 only", "all reals"]),
        ("Why is $x=2$ excluded from $\\dfrac{x-4}{x-2}\\geq0$ even though the simplified sign might look fine?",
         "the original expression is undefined there",
         "Never include a point that makes a denominator zero, even for $\\geq$.",
         ["it is a root of the numerator", "it makes the value 1", "graphs never include integers"]),
        ("A degree-$6$ polynomial with positive lead, as $x\\to-\\infty$, goes:",
         "+\u221e",
         "Even degree, positive lead: both ends up.",
         ["-\u221e", "0", "oscillates"]),
        ("If synthetic division by $x-4$ leaves remainder $0$, then $4$ is:",
         "a root of p",
         "Remainder $0$ means $p(4)=0$.",
         ["the y-intercept", "a hole", "an asymptote"]),
        ("$p(x)=x^2(x-3)$ crosses the axis at:",
         "x=3 only",
         "Multiplicity $2$ at $0$ is a bounce; multiplicity $1$ at $3$ is a cross.",
         ["x=0 only", "both 0 and 3 as crosses", "nowhere"]),
        ("Horizontal asymptote of $\\dfrac{5x^2-1}{2x^2+7}$ is:",
         "y=5/2",
         "Equal degrees: $5/2$.",
         ["y=0", "y=5", "y=7/2"]),
        ("The graph of $\\dfrac{x^2-1}{x-1}$ looks like $y=x+1$ except:",
         "a hole at x=1",
         "Cancel $(x-1)$: simplified $x+1$, undefined at $x=1$.",
         ["a vertical asymptote at x=1", "a slant other than x+1", "no graph"]),
        ("Sign chart for $\\dfrac{(x-1)(x+2)}{x}$ changes at:",
         "x=-2, 0, and 1",
         "Zeros of numerator and denominator are the critical numbers.",
         ["only x=1", "only x=0", "x=2 only"]),
        ("A quartic can have how many real zeros, counting multiplicity?",
         "4",
         "Degree $4$ means four zeros in $\\mathbb{C}$, and up to four real counting multiplicity.",
         ["exactly 2", "5", "infinitely many"]),
        ("$p(x)=-x^4+3x$ as $x\\to+\\infty$ tends to:",
         "-\u221e",
         "Even degree, negative lead: both ends down.",
         ["+\u221e", "3", "0"]),
        ("Factor theorem plus $p(1)=p(-2)=0$ for a quadratic $p$ means $p(x)$ is a multiple of:",
         "(x-1)(x+2)",
         "Each root gives a linear factor.",
         ["(x+1)(x-2)", "x^2+2", "x-3"]),
        ("Oblique asymptote of $\\dfrac{x^2+3x+1}{x+1}$ is found by:",
         "polynomial division",
         "Divide; the linear quotient is the slant, the remainder over the divisor dies at infinity.",
         ["setting x=0", "factoring the remainder only", "the quadratic formula"]),
        ("$f(x)=\\dfrac{x}{x^2-4}$ is odd because:",
         "f(-x)=-f(x)",
         "Negating $x$ negates the whole fraction: an odd rational.",
         ["f(-x)=f(x)", "it has two asymptotes", "degree is 2"]),
        ("Included in $\\dfrac{x-5}{x+1}\\leq0$ is the point:",
         "x=5",
         "Numerator zero is a closed endpoint for $\\leq$; $x=-1$ is open/excluded.",
         ["x=-1", "x=0 only", "x=1"]),
        ("If a cubic bounces at $x=2$ and crosses at $x=-1$, a model is:",
         "(x-2)^2(x+1)",
         "Even multiplicity at $2$, odd at $-1$.",
         ["(x-2)(x+1)^2", "(x+2)^2(x-1)", "x^3-2"]),
        ("The hole in $\\dfrac{x^2-9}{x-3}$ has y-coordinate:",
         6,
         "Simplified $x+3$; at $x=3$ the missing point would have been $6$.",
         ["0", "3", "9"]),
        ("For equal-degree rationals, long-run height equals:",
         "ratio of leading coefficients",
         "That constant is the horizontal asymptote.",
         ["the constant term", "zero always", "the degree"]),
        ("SAT Stretch: Solve $\\dfrac{x^2-4}{x+1}\\leq0$ and report the solution set.",
         "[-2,2] excluding x=-1",
         "Factor $(x-2)(x+2)/(x+1)\\leq0$. Critical numbers $-2,-1,2$. Sign is negative on $[-2,-1)$ and $(-1,2]$; "
         "include the zeros $\\pm2$, exclude the asymptote $x=-1$. Together: $[-2,2]\\setminus\\{-1\\}$.",
         ["[-2,2]", "(-2,2)", "x\u2264-2 or x\u22652"]),
        ("SAT Stretch: $p(x)=x^3-3x+2$. Given $x=1$ is a root, the other real roots are:",
         "1 (double) and -2",
         "Since $p(1)=0$ and $p'(1)=0$, the root $x=1$ has multiplicity at least $2$. Also $p(-2)=0$, so "
         "$p(x)=(x-1)^2(x+2)$. The real roots are $1$ (double) and $-2$.",
         ["only -2", "0 and 2", "1 and 2"]),
        ("SAT Stretch: $f(x)=\\dfrac{2x^2-3x-2}{x^2-4}$. The hole is at $x=$:",
         "2",
         "Numerator $(2x+1)(x-2)$; denominator $(x-2)(x+2)$. Cancel $x-2$: hole at $x=2$, VA at $x=-2$.",
         ["-2", "1/2", "4"]),
        ("SAT Stretch: After the hole, $f(x)=\\dfrac{2x^2-3x-2}{x^2-4}$ has horizontal asymptote:",
         "y=2",
         "Simplified $\\dfrac{2x+1}{x+2}$ is still equal degree, lead ratio $2/1=2$.",
         ["y=0", "y=1", "y=-2"]),
        ("SAT Stretch: A sign chart for $\\dfrac{(x-1)^2(x+3)}{x-4}<0$ is negative on:",
         "(-3,1) U (1,4)",
         "Even multiplicity at $x=1$ does not flip the sign, but $x=1$ makes the value $0$, which a strict inequality excludes. "
         "The expression is negative on $(-3,4)$ except at $x=1$, that is $(-3,1)\\cup(1,4)$.",
         ["(-3,4)", "(-\u221e,-3)", "(4,\u221e)"]),
        ("SAT Stretch: Remainder when $x^4-5x^2+4$ is divided by $x^2-1$ is:",
         "0",
         "$x^4-5x^2+4=(x^2-4)(x^2-1)$, so $x^2-1$ divides evenly; remainder $0$.",
         ["x+1", "4", "x^2"]),
        ("SAT Stretch: How many distinct real zeros does $p(x)=(x^2+1)(x-2)^3(x+2)^2$ have?",
         2,
         "$x^2+1$ has no real zeros; distinct real zeros are $2$ and $-2$.",
         ["3", "5", "7"]),
        ("SAT Stretch: The slant asymptote of $\\dfrac{x^3+2}{x^2-1}$ is:",
         "y=x",
         "Divide: $x^3+2=(x)(x^2-1)+x+2$, so $f(x)=x+\\dfrac{x+2}{x^2-1}\\to x$.",
         ["y=x+2", "y=0", "y=x^2"]),
        ("SAT Stretch: For $\\dfrac{1-x}{x^2-x-6}\\geq0$, the closed endpoints in the solution are the zeros of:",
         "the numerator only",
         "Include $x=1$ (numerator zero). Exclude $x=3$ and $x=-2$ (denominator zeros) even if they look like boundaries.",
         ["both numerator and denominator zeros", "the denominator only", "no endpoints"]),
        ("SAT Stretch: Rewrite $\\dfrac{x+2}{x-1}\\geq 3$ as one rational inequality. The solution set is:",
         "(1, 5/2]",
         "Bring to one side: $\\dfrac{x+2}{x-1}-3=\\dfrac{5-2x}{x-1}\\geq0$. Critical numbers $x=5/2$ (include) and $x=1$ (exclude). "
         "A sign chart is positive only on $(1,5/2]$.",
         ["[5/2,\\infty)", "(-\u221e,1)", "[1,5/2]"]),
    ])
    return qs[:55]


def build_unit2():
    title = "Precalculus Unit 2: Polynomial & Rational Functions"
    description = (
        "End behavior, zeros and multiplicity, remainder and factor theorems, rational asymptotes, "
        "holes, and sign-chart inequalities — with graphs of the actual polynomials and rationals."
    )
    concepts = [
        "End behavior and zeros",
        "Remainder/factor theorems",
        "Graphing polynomials",
        "Asymptotes of rationals",
        "Holes and intercepts",
        "Inequalities with sign charts",
    ]

    p_pts = sample_curve(lambda x: (x + 2) * (x - 1) * (x - 3), -3.2, 4.2)
    c1 = concept_block(
        "1. End behavior and zeros",
        [
            "A polynomial $p(x)=a_n x^n+\\cdots+a_0$ is defined for every real $x$. Its long-run graph is "
            "controlled by one piece of data: the leading term $a_n x^n$. If $n$ is even and $a_n>0$, both "
            "ends rise (a positive even power). If $n$ is even and $a_n<0$, both ends fall. If $n$ is odd and "
            "$a_n>0$, the graph comes from $-\\infty$ on the left and leaves toward $+\\infty$ on the right. "
            "Odd degree with $a_n<0$ reverses that.",
            "A zero (root) of $p$ is an input $r$ with $p(r)=0$. By the factor theorem, $x-r$ is then a factor. "
            "If $(x-r)^k$ is the highest power that divides $p$, we say $r$ has multiplicity $k$. Multiplicity "
            "is not a decoration: it decides whether the graph crosses the axis or bounces.",
            "Odd multiplicity (including the simple case $k=1$) means the graph changes sign at $r$ and "
            "therefore crosses the $x$-axis. Even multiplicity means the graph touches at $r$ and turns back, "
            "keeping the same sign on both sides. A double root looks locally like a parabola kissing the axis.",
            "The fundamental theorem of algebra says a degree-$n$ polynomial has $n$ zeros in the complex "
            "numbers, counting multiplicity. Over the reals you may see fewer distinct $x$-intercepts, because "
            "some zeros may be complex conjugates and some real zeros may be repeated.",
            "Writing $p$ in factored form is the graphing gold. From $p(x)=-2(x+2)(x-1)^2$ you can read the "
            "zeros, the multiplicities, the y-intercept $p(0)$, and the end behavior from the leading term "
            "$-2x^3$, all without expanding.",
            "End behavior plus zeros is the skeleton of every polynomial graph in this unit. The next lessons "
            "add the remainder theorem (a fast way to test zeros) and then the local wiggles between zeros.",
        ],
        "End behavior tells you how a model blows up for large $|x|$ — population polynomials, cost functions, "
        "and later Taylor polynomials in calculus all start from leading-term dominance.",
        "Name the degree and the sign of the leading coefficient first (ends). Then list the real zeros with "
        "multiplicity (cross versus bounce). Sketch those two pieces before you worry about turning-point height.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", p_pts)],
                points=[(-2, 0, "-2"), (1, 0, "1"), (3, 0, "3")],
                xlim=(-4, 5), ylim=(-10, 10),
            ),
            "$p(x)=(x+2)(x-1)(x-3)$ with zeros marked",
            "Three simple zeros, so the graph crosses at $x=-2$, $x=1$, and $x=3$. Odd degree, positive lead: left down, right up.",
        )
        + solved(
            1, "Describe the end behavior of $p(x)=-2x^3+5x$.",
            ["Degree $3$ is odd; leading coefficient $-2$ is negative.",
             "Odd + negative: as $x\\to+\\infty$, $p\\to-\\infty$; as $x\\to-\\infty$, $p\\to+\\infty$.",
             "The lower-degree term $5x$ cannot change the ends."],
            "left up, right down", "", "Easy",
        )
        + solved(
            2, "List the zeros of $p(x)=(x+2)(x-1)(x-3)$ and state whether each is a cross or a bounce.",
            ["Zeros at $x=-2$, $x=1$, $x=3$.",
             "Each factor is to the first power, so each multiplicity is $1$ (odd).",
             "The graph crosses at all three zeros."],
            "crosses at $-2,1,3$", "", "Medium",
        )
        + solved(
            3, "A cubic has a double root at $x=1$ and a simple root at $x=-4$. Write one such polynomial and describe $x=1$.",
            ["A model is $p(x)=(x-1)^2(x+4)$.",
             "Multiplicity $2$ at $x=1$ is even, so the graph bounces there.",
             "Multiplicity $1$ at $x=-4$ is a cross.",
             "Leading term is $x^3$, so left down and right up."],
            "$p(x)=(x-1)^2(x+4)$; bounce at $x=1$", "Any nonzero constant multiple works too.", "Hard",
        ),
        ("Using the constant term for end behavior",
         "Ends are not about $p(0)$. They are about the leading term. A huge constant can lift the middle of "
         "the graph and still leave the far-right behavior unchanged."),
        ("Factored form first",
         "If a multiple-choice question gives a polynomial expanded, try to factor (or test easy integers with "
         "the remainder theorem) before you sketch. Zeros plus ends determine the shape."),
        [
            "I can read end behavior from degree and leading coefficient.",
            "I can list zeros from factored form.",
            "I can tell cross versus bounce from multiplicity.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Remainder and factor theorems",
        [
            "The remainder theorem is a one-line miracle. When a polynomial $p(x)$ is divided by the linear "
            "divisor $x-c$, the remainder is the number $p(c)$. You do not have to complete long division to "
            "know the leftover. Evaluate.",
            "The factor theorem is the remainder theorem when the remainder is $0$. If $p(c)=0$, then $x-c$ "
            "divides $p(x)$ evenly, so $p(x)=(x-c)q(x)$ for some polynomial $q$ of degree one less. Conversely, "
            "if $x-c$ is a factor, then $c$ is a root.",
            "Synthetic division is the efficient algorithm for dividing by $x-c$. Write the coefficients (including "
            "zeros for missing powers), bring down the first, multiply by $c$, add, repeat. The last number is "
            "the remainder $p(c)$; the other numbers are the coefficients of the quotient.",
            "A typical Precalculus move is: test a likely integer root with $p(c)$, confirm it is a root, "
            "synthetically divide, and factor the quotient (quadratic formula if needed). That is how you fully "
            "factor a cubic once you have spotted one rational root.",
            "Possible rational roots, if any, are factors of the constant term over factors of the leading "
            "coefficient (the rational root theorem). The list is a search list, not a promise: many polynomials "
            "have no rational roots at all, even when they have real roots.",
            "These theorems connect Units 1 and 2. Evaluating $p(c)$ is function notation. A root is an "
            "x-intercept. A linear factor is a piece of the graph’s skeleton. Remainder $3$ when dividing by "
            "$x-1$ means the point $(1,3)$ lies on the graph — even if $1$ is not a zero.",
        ],
        "Factoring cubics and quartics by hand, checking candidate roots on a test, and later polynomial "
        "long division in calculus all rest on remainder and factor.",
        "To test whether $c$ is a root, compute $p(c)$ (synthetic division is fine). If you get $0$, peel off "
        "$x-c$ and keep factoring the quotient. If you get a nonzero remainder $r$, that $r$ is $p(c)$.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: x ** 3 - 6 * x ** 2 + 11 * x - 6, -0.5, 4.5))],
                points=[(1, 0, "p(1)=0"), (2, 0, "p(2)=0"), (3, 0, "p(3)=0")],
                xlim=(-1, 5), ylim=(-8, 8),
            ),
            "$p(x)=x^3-6x^2+11x-6=(x-1)(x-2)(x-3)$",
            "Remainder theorem at $x=1$ gives $p(1)=0$, so $x-1$ is a factor; the other factors follow by division.",
        )
        + solved(
            4, "Find the remainder when $x^3-2x+4$ is divided by $x-1$.",
            ["Remainder theorem: remainder $=p(1)$.",
             "$p(1)=1-2+4=3$.",
             "So the remainder is $3$, not $0$; $x-1$ is not a factor."],
            "$3$", "", "Easy",
        )
        + solved(
            5, "Given $p(2)=0$, name a factor of $p$.",
            ["Factor theorem: $p(c)=0$ if and only if $x-c$ divides $p$.",
             "Here $c=2$, so $x-2$ is a factor.",
             "$x+2$ would correspond to the root $-2$, which was not given."],
            "$x-2$", "", "Medium",
        )
        + solved(
            6, "Factor $p(x)=x^3+x^2-4x-4$ given that $p(-1)=0$.",
            ["$x+1$ is a factor. Synthetic division with $c=-1$ on coefficients $1,1,-4,-4$.",
             "The quotient is $x^2-4$.",
             "$x^2-4=(x-2)(x+2)$.",
             "Therefore $p(x)=(x+1)(x-2)(x+2)$."],
            "$(x+1)(x-2)(x+2)$", "Check: $p(2)=8+4-8-4=0$.", "Hard",
        ),
        ("Dividing by $x+3$ and then evaluating $p(3)$",
         "The divisor $x+3$ is $x-(-3)$, so the remainder is $p(-3)$, not $p(3)$. The sign on $c$ is the "
         "opposite of the constant in $x+3$."),
        ("Synthetic division as a root check",
         "If you already plan to factor, run synthetic division instead of plugging into a huge expanded form. "
         "The last entry is $p(c)$, and if it is $0$ you already have the quotient coefficients."),
        [
            "I can find $p(c)$ as a remainder.",
            "I can turn a root into a linear factor.",
            "I can finish factoring a cubic after one successful division.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Graphing polynomials",
        [
            "A useful polynomial sketch has five ingredients: end behavior, x-intercepts with multiplicity, "
            "the y-intercept $p(0)$, a few test points between zeros, and a note on the maximum number of "
            "turning points (at most $n-1$ for degree $n$). You do not need calculus to produce a serviceable picture.",
            "Plot the zeros on the axis and mark bounce versus cross. Then use end behavior to decide which "
            "side of the axis the far right lives on. Working right-to-left (or left-to-right) through the zeros, "
            "flip to the other side at each odd-multiplicity zero and stay on the same side at each even-multiplicity zero.",
            "Local turning-point heights are the only ingredient you cannot get from factors alone. A test "
            "point in each interval, or a recognition that $(x-1)^2$ produces a local min/max on the axis, is "
            "enough for Precalculus. Calculus will later find exact turning points with derivatives.",
            "The graph of $p(x)=(x+2)(x-1)^2$ crosses at $-2$ and bounces at $1$. Because the bounce is on "
            "the axis, that turning point has height $0$. A bounce off the axis at a double root is a very "
            "common exam graph.",
            "Even-degree polynomials with positive lead look “W-ish” or “U-ish”; odd-degree polynomials with "
            "positive lead look “uphill overall” with possible extra wiggles. Matching a multiple-choice graph "
            "to a formula is usually an ends-plus-zeros problem, not a plotting-twenty-points problem.",
            "Complex zeros come in conjugate pairs for real polynomials and do not appear as x-intercepts. "
            "A quartic might cross the axis twice and still be degree $4$ because the other two zeros are "
            "complex. Do not assume “degree equals number of x-intercepts.”",
        ],
        "Being able to look at a factored cubic and see the picture is how you check calculator graphs, how you "
        "answer “which could be the graph of …?”, and how you set up sign charts in the last lesson of this unit.",
        "Ends first, zeros second, test a point in each interval third. If the question is multiple choice, "
        "eliminate graphs with the wrong ends or the wrong bounce/cross pattern before you compute anything else.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: (x + 2) * (x - 1) ** 2, -3, 3))],
                points=[(-2, 0, "cross"), (1, 0, "bounce")],
                xlim=(-4, 4), ylim=(-6, 8),
            ),
            "$p(x)=(x+2)(x-1)^2$: cross at $-2$, bounce at $1$",
            "Even multiplicity at $x=1$ keeps the graph on the same side of the axis.",
        )
        + solved(
            7, "Does $p(x)=(x+2)(x-1)^2$ cross or bounce at $x=1$?",
            ["The factor $(x-1)$ appears twice, so multiplicity $2$ is even.",
             "Even multiplicity means the graph touches and turns.",
             "It bounces at $x=1$ (and crosses at $x=-2$)."],
            "bounce at $x=1$", "", "Easy",
        )
        + solved(
            8, "What is the maximum number of turning points for a degree-$4$ polynomial?",
            ["A degree-$n$ polynomial has at most $n-1$ turning points.",
             "Here $n=4$, so at most $3$.",
             "It might have fewer; “at most” is the theorem."],
            "3", "", "Medium",
        )
        + solved(
            9, "Sketch in words $p(x)=x^2(x-3)$: intercepts and local behavior at $0$.",
            ["Zeros: $x=0$ (multiplicity $2$, bounce) and $x=3$ (simple, cross).",
             "y-intercept is $0$ as well, because of the factor $x^2$.",
             "End behavior: cubic with positive lead, left down, right up.",
             "Near $0$ the graph looks like a parabola sitting on the origin, then it crosses at $3$."],
            "bounce at $0$, cross at $3$", "Degree $3$ so at most two turning points.", "Hard",
        ),
        ("Assuming every bounce is off the axis",
         "A double root on the axis is a bounce on the axis. A turning point that is not a root sits off the "
         "axis; you need a test point or calculus to locate its height. Do not invent extra intercepts."),
        ("Match ends, then multiplicities",
         "On “which graph is this polynomial?” questions, first kill every graph with the wrong left/right "
         "behavior, then kill graphs that cross where they should bounce."),
        [
            "I can combine ends and zeros into a sketch.",
            "I can use multiplicity to decide cross versus bounce.",
            "I know a degree-$n$ graph has at most $n-1$ turns.",
        ],
        11,
    )

    rat = sample_curve(lambda x: (x + 1) / (x - 2) if abs(x - 2) > 0.12 else 1e9, -4, 6, skip=(2,))
    c4 = concept_block(
        "4. Asymptotes of rationals",
        [
            "A rational function is a ratio of polynomials, $f(x)=\\dfrac{p(x)}{q(x)}$, with $q$ not the zero "
            "polynomial. Wherever $q(x)=0$ and $p(x)\\neq0$ after cancelling common factors, the graph has a "
            "vertical asymptote: $y$ blows up to $\\pm\\infty$ as $x$ approaches that input.",
            "Horizontal asymptotes describe the far left and far right. Compare degrees. If $\\deg q>\\deg p$, "
            "then $y=0$ is a horizontal asymptote (the denominator grows faster). If the degrees are equal, "
            "the horizontal asymptote is $y=$ the ratio of leading coefficients. If $\\deg p=\\deg q+1$, there "
            "is a slant (oblique) asymptote, found by dividing.",
            "If $\\deg p\\geq\\deg q+2$, the end behavior is a polynomial of degree at least $2$ (a parabolic "
            "or higher “oblique” curve). Precalculus courses emphasize the three common cases: $y=0$, $y=L$, "
            "and a slant line.",
            "Vertical asymptotes are not holes. A hole is a cancelled common factor, treated in the next "
            "lesson. A vertical asymptote is a factor that survives in the denominator. Dashed vertical lines "
            "on a sketch keep you from accidentally connecting the two branches.",
            "Sign on each side of a vertical asymptote can be read from a sign chart or from a test point. "
            "The two sides need not match: one side may go to $+\\infty$ while the other goes to $-\\infty$.",
            "Asymptotes are the rational analogue of polynomial end behavior. Polynomials never need dashed "
            "vertical lines; rationals almost always do. Graphing without the asymptotes is like graphing a "
            "polynomial without its ends — the picture is unrecognizable.",
        ],
        "Limits at infinity in calculus are this lesson with more vocabulary. Bode plots, dose-response curves, "
        "and inverse-square laws are rational end-behavior in the wild.",
        "Factor numerator and denominator. Cancel to identify holes. Surviving denominator zeros are vertical "
        "asymptotes. Compare degrees for the horizontal or slant rule. Draw the dashed lines before any curve.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", rat)],
                dashes=[("v", 2, "x=2"), ("h", 1, "y=1")],
                xlim=(-4, 6), ylim=(-8, 8),
            ),
            "$f(x)=\\dfrac{x+1}{x-2}$ with vertical asymptote $x=2$ and horizontal $y=1$",
            "The skip at $x=2$ splits the graph into two branches. Equal degrees give $y=1$.",
        )
        + solved(
            10, "Find the vertical and horizontal asymptotes of $f(x)=\\dfrac{x+1}{x-2}$.",
            ["Denominator zero at $x=2$; numerator $3\\neq0$, so VA $x=2$.",
             "Degrees equal (both $1$), leading coefficients $1/1=1$, so HA $y=1$.",
             "There is no slant asymptote in the equal-degree case."],
            "VA $x=2$, HA $y=1$", "", "Easy",
        )
        + solved(
            11, "What is the horizontal asymptote of $g(x)=\\dfrac{2x^2+1}{x^3-x}$?",
            ["Denominator degree $3$ exceeds numerator degree $2$.",
             "The fraction tends to $0$ for large $|x|$.",
             "Horizontal asymptote $y=0$."],
            "$y=0$", "", "Medium",
        )
        + solved(
            12, "Explain why $h(x)=\\dfrac{x^2+1}{x-1}$ has a slant asymptote rather than a horizontal one.",
            ["Numerator degree $2$ is exactly one more than denominator degree $1$.",
             "Polynomial division produces a linear quotient plus a remainder over $x-1$.",
             "The linear quotient is the slant asymptote; the remainder term dies at infinity.",
             "Divide: $x^2+1=(x+1)(x-1)+2$, so $h(x)=x+1+\\dfrac{2}{x-1}$ and the slant is $y=x+1$."],
            "slant $y=x+1$", "Degree difference $1$ is the slant case.", "Hard",
        ),
        ("Calling every denominator zero a vertical asymptote before cancelling",
         "Cancel first. A factor that cancels is a hole, not an asymptote. If you skip cancelling you will "
         "draw a dashed line through a tiny gap that should just be an open circle."),
        ("Degree comparison on sight",
         "Glance at the highest powers before you expand anything. Most horizontal-asymptote questions are "
         "settled in two seconds by comparing those powers and, if they match, the leading coefficients."),
        [
            "I can locate vertical asymptotes after cancelling.",
            "I can name the horizontal asymptote from degrees.",
            "I can recognize when a slant asymptote exists and find it by division.",
        ],
        16,
    )

    hole_curve = sample_curve(
        lambda x: (x + 3) if abs(x - 3) > 0.12 else 1e9, -2, 7, skip=(3,)
    )
    c5 = concept_block(
        "5. Holes and intercepts",
        [
            "A hole (removable discontinuity) appears when a linear factor cancels from both numerator and "
            "denominator. The simplified formula describes the same outputs except at that one x-value, which "
            "is missing. Graphically you draw the simplified graph and put an open circle at the cancelled input.",
            "To find the hole’s coordinates, cancel, then substitute the cancelled x-value into the simplified "
            "rule. For $f(x)=\\dfrac{x^2-9}{x-3}=\\dfrac{(x-3)(x+3)}{x-3}$, the simplified rule is $x+3$ ($x\\neq3$), "
            "so the hole is $(3,6)$.",
            "x-intercepts come from the numerator of the simplified function being zero (denominator still nonzero). "
            "y-intercepts come from $f(0)$, provided $0$ is in the domain. A hole is not an intercept unless "
            "the missing point would have sat on an axis — and even then the graph does not include it.",
            "After cancelling, you may still have vertical asymptotes from leftover denominator factors, and "
            "you still have a horizontal or slant asymptote from the simplified degrees. Holes do not change "
            "end behavior; they only punch a point out of an otherwise ordinary curve.",
            "A common SAT trap is a rational that looks like it has two vertical asymptotes until you factor. "
            "Always write $p$ and $q$ in factored form before you name holes, intercepts, and asymptotes.",
            "Putting it together: factor, cancel (holes), surviving denominator zeros (VAs), simplified "
            "numerator zeros (x-intercepts), $f(0)$ (y-intercept), degree comparison (HA or slant). That checklist "
            "is the entire graphing program for rationals in Precalculus.",
        ],
        "Holes versus asymptotes is the difference between “undefined but fixable by redefining one point” and "
        "“blows up.” Calculus will call these removable versus infinite discontinuities.",
        "Factor completely. Circle cancelled factors as holes and compute their y-values from the simplified "
        "rule. Then treat the leftover rational exactly as in the asymptote lesson.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", hole_curve)],
                points=[(3, 6, "hole (3,6)")],
                xlim=(-2, 7), ylim=(-1, 10),
            ),
            "$y=\\dfrac{x^2-9}{x-3}$ is the line $y=x+3$ with a hole at $(3,6)$",
            "The open gap is the cancelled factor $x-3$. There is no vertical asymptote.",
        )
        + solved(
            13, "Locate the hole of $f(x)=\\dfrac{(x-3)(x+1)}{(x-3)(x-2)}$.",
            ["The factor $x-3$ cancels, so $x=3$ is a hole, not a VA.",
             "Simplified: $\\dfrac{x+1}{x-2}$ for $x\\neq3$.",
             "Hole y-value: $\\dfrac{3+1}{3-2}=4$. Hole $(3,4)$."],
            "hole $(3,4)$", "Leftover VA at $x=2$.", "Easy",
        )
        + solved(
            14, "Find the intercepts of $f(x)=\\dfrac{x+1}{x-2}$.",
            ["x-intercept: numerator $0$ so $x=-1$, point $(-1,0)$.",
             "y-intercept: $f(0)=1/(-2)=-1/2$, point $(0,-1/2)$.",
             "$x=2$ is a VA, not an intercept."],
            "$(-1,0)$ and $(0,-1/2)$", "", "Medium",
        )
        + solved(
            15, "The graph of $\\dfrac{x^2-9}{x-3}$ looks like which line, and what is missing?",
            ["Cancel $x-3$ (for $x\\neq3$) to get $y=x+3$.",
             "The missing point is $x=3$, $y=6$.",
             "So the graph is the line $y=x+3$ with a hole at $(3,6)$."],
            "line $y=x+3$ with hole $(3,6)$", "", "Hard",
        ),
        ("Leaving a hole’s y-coordinate as “undefined”",
         "The x-coordinate is undefined in the original formula, but the y-coordinate of the missing point is "
         "a perfectly ordinary number coming from the simplified formula. Compute it; questions ask for it."),
        ("Cancel, then intercepts",
         "If you find intercepts before cancelling, you might list a fake x-intercept at a hole. Use the "
         "simplified numerator for intercepts."),
        [
            "I can distinguish a hole from a vertical asymptote.",
            "I can compute hole coordinates after cancelling.",
            "I can find x- and y-intercepts of a simplified rational.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Inequalities with sign charts",
        [
            "A rational (or polynomial) inequality such as $\\dfrac{x-1}{x+2}>0$ is not solved by “moving things "
            "across” as if it were linear. The algebra that preserves inequality direction fails when you multiply "
            "by an expression that might be negative or zero. The reliable tool is a sign chart.",
            "Critical numbers are the zeros of the numerator and the zeros of the denominator (after cancelling "
            "holes, which you usually just exclude). Place those numbers on a number line. They split the line "
            "into open intervals. In each interval the expression cannot change sign, so one test point tells "
            "you the sign of the whole interval.",
            "For a strict inequality $>0$ or $<0$, never include a denominator zero, and include a numerator "
            "zero only if the inequality is $\\geq$ or $\\leq$ (where the value $0$ is allowed). Write the "
            "solution as a union of intervals, with open circles at vertical asymptotes.",
            "Multiplicity matters on a sign chart just as on a graph. Crossing a simple zero or a simple "
            "vertical asymptote flips the sign. Crossing a factor of even multiplicity does not flip the sign "
            "(the graph bounced). That is why $(x-1)^2$ in a numerator can make a “touch and stay nonnegative” interval.",
            "Polynomial inequalities are the same method with no vertical asymptotes: only the roots split the "
            "line. $(x-2)(x+1)\\geq0$ is “outside the roots” for a positive-lead quadratic, which you can also "
            "see from the parabola sitting above the axis outside the roots: $x\\leq-1$ or $x\\geq2$.",
            "On tests, a sign chart plus a number-line sketch beats casework. Once the chart is drawn, reading "
            "the solution is a coloring problem: shade where the sign matches the inequality, then respect "
            "whether endpoints are closed.",
        ],
        "Sign charts are how you solve where a graph is above the axis, where a rational is positive, and later "
        "where a derivative is positive in calculus. It is one tool with a long career.",
        "Move everything to one side so you compare with zero. Factor. Mark zeros and undefined points. Test "
        "one number per interval. Include or exclude endpoints using the inequality’s equality and the domain.",
        lesson_figure(
            number_line(-5, 5, opened=[(-2, "VA"), (1, "zero")], shade=("out", -2, 1)),
            "Sign chart for $\\dfrac{x-1}{x+2}>0$",
            "Open at the VA $x=-2$ and at the zero $x=1$. The expression is positive on $(-\\infty,-2)\\cup(1,\\infty)$.",
        )
        + solved(
            16, "Solve $\\dfrac{x-1}{x+2}>0$.",
            ["Critical numbers: $x=1$ (zero) and $x=-2$ (undefined).",
             "Test $x=-3$: $(-)/( - )>0$. Test $x=0$: $(-)/(+)<0$. Test $x=2$: $(+)/(+)>0$.",
             "Positive on $(-\\infty,-2)$ and $(1,\\infty)$. Exclude both critical numbers because the inequality is strict."],
            "$x<-2$ or $x>1$", "", "Easy",
        )
        + solved(
            17, "Solve $\\dfrac{x+3}{x-1}\\leq0$. Which endpoints are included?",
            ["Critical numbers $x=-3$ (zero) and $x=1$ (VA).",
             "The inequality allows $0$, so include $x=-3$.",
             "Never include $x=1$.",
             "The negative closed interval is $[-3,1)$."],
            "include $x=-3$, exclude $x=1$", "", "Medium",
        )
        + solved(
            18, "Solve $\\dfrac{x^2-4}{x+1}\\leq0$ as a set.",
            ["Factor: $\\dfrac{(x-2)(x+2)}{x+1}\\leq0$. Critical numbers $-2,-1,2$.",
             "Test signs: negative on $[-2,-1)$ and $(-1,2]$.",
             "Include $-2$ and $2$; exclude $-1$.",
             "Solution $[-2,2]\\setminus\\{-1\\}$."],
            "$[-2,2]$ except $x=-1$", "A compact way to write two intervals sharing a missing point.", "Hard",
        ),
        ("Multiplying both sides by the denominator",
         "You would have to split into cases according to the sign of the denominator, which is the sign chart "
         "in disguise but easier to get wrong. Keep everything on one side and test intervals instead."),
        ("Closed dots only at zeros of the numerator",
         "A vertical asymptote is never a closed endpoint. A hole is never included. Only a genuine zero of "
         "the expression can be filled in, and only when the inequality allows equality."),
        [
            "I can list critical numbers from factors.",
            "I can test intervals and write a union of solutions.",
            "I know which endpoints a $\\leq$ inequality may include.",
        ],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title, AUDIENCE, concepts, body, practice_slots(31, 25, STRETCH_LABEL),
    )
    return title, description, content, _u2_questions()


# ===========================================================================
# UNIT 3: Exponential & Logarithmic Functions
# ===========================================================================

def _u3_questions():
    qs = []
    _add(qs, [
        ("A quantity $Q=40(1.05)^t$ is best described as:",
         "exponential growth by 5% per unit time",
         "Base $1.05>1$ means 5% growth each time unit; $40$ is the initial value.",
         ["5% decay", "linear growth of 1.05", "logistic with carrying 40"]),
        ("$A=200(0.85)^t$ after $t=2$ equals:",
         144.5,
         "$200(0.85)^2=200(0.7225)=144.5$.",
         [170, 85, 144]),
        ("The half-life equation $N=N_0(1/2)^{t/h}$ with $h=8$ hours reaches half of $N_0$ at $t=$:",
         8,
         "By definition of half-life, one half-life period is $h=8$.",
         ["4", "16", "2"]),
        ("Rewrite $3^{t}=81$ as a log statement.",
         "t=log_3 81",
         "The log is the exponent: $t=\\log_3 81=4$ because $3^4=81$.",
         ["t=log_81 3", "3=log_t 81", "t=81^3"]),
        ("Continuous model $P=Pe^{rt}$ with $r=-0.02$ is:",
         "exponential decay",
         "Negative continuous rate means decay; the graph of $e^{rt}$ falls.",
         ["exponential growth", "a linear decline of 0.02", "undefined"]),
        ("$\\log_2 8$ equals:",
         3,
         "$2^3=8$, so the log is $3$.",
         None),
        ("The inverse of $f(x)=3^x$ is:",
         "f^{-1}(x)=log_3 x",
         "Exponential and log with the same base undo each other.",
         ["3x", "x^3", "log_x 3"]),
        ("The graph of $y=\\log_2 x$ is the reflection of $y=2^x$ across:",
         "y=x",
         "Inverses reflect across the diagonal, as in Unit 1.",
         ["the x-axis", "the y-axis", "x=2"]),
        ("Domain of $y=\\log_5(x-1)$ is:",
         "x>1",
         "The argument of a log must be positive: $x-1>0$.",
         ["x\u22651", "x>0", "x\u22601"]),
        ("$\\log_b 1$ for $b>0$, $b\\neq1$ equals:",
         0,
         "$b^0=1$ for every legal base.",
         ["1", "b", "undefined"]),
        ("$\\log_2 8+\\log_2 4$ simplifies to:",
         5,
         "Product rule: $\\log_2(32)=5$, or $3+2=5$.",
         ["6", "12", "1"]),
        ("$\\log_3 54-\\log_3 2$ equals:",
         3,
         "Quotient rule: $\\log_3(27)=3$.",
         ["27", "52", "1"]),
        ("$3\\log_5 2$ is the same as:",
         "log_5 8",
         "Power rule: $k\\log_b a=\\log_b(a^k)$, and $2^3=8$.",
         ["log_5 6", "(log_5 2)^3", "log_2 5"]),
        ("Expand $\\log\\dfrac{x^2}{y}$.",
         "2 log x - log y",
         "Quotient then power: $\\log x^2-\\log y=2\\log x-\\log y$.",
         ["2 log x + log y", "log x - 2 log y", "log(x^2-y)"]),
        ("Which is illegal as a real log?",
         "log(-4)",
         "The argument must be positive; $-4<0$.",
         ["log 4", "log 0.01", "ln e"]),
        ("$\\log_2 10$ using change of base (common logs) is:",
         "log 10 / log 2",
         "$\\log_b a=\\dfrac{\\log_k a}{\\log_k b}$ for any legal $k$.",
         ["log 2 / log 10", "10/2", "ln 2"]),
        ("Change of base gives $\\log_9 27=$:",
         "3/2",
         "$\\dfrac{\\ln 27}{\\ln 9}=\\dfrac{3\\ln 3}{2\\ln 3}=3/2$, or $9^{3/2}=(3^2)^{3/2}=27$.",
         ["3", "2/3", "9/27"]),
        ("A calculator-ready form of $\\log_7 20$ is:",
         "ln 20 / ln 7",
         "Natural logs are a standard change-of-base choice.",
         ["ln 7 / ln 20", "20 ln 7", "7/20"]),
        ("Why does $\\log_{1/2} 8$ come out negative?",
         "base in (0,1) and argument >1",
         "A decaying exponential hits $8$ at a negative exponent.",
         ["logs are always negative", "8 is even", "the base is larger than 8"]),
        ("$\\dfrac{\\log_5 36}{\\log_5 6}$ equals:",
         2,
         "Change of base: $\\log_6 36=2$.",
         ["6", "30", "1/2"]),
        ("Solve $2^x=32$.",
         5,
         "$32=2^5$, so $x=5$.",
         None),
        ("Solve $\\log_3(x-1)=2$.",
         10,
         "$x-1=3^2=9$, so $x=10$. Check: argument $9>0$.",
         None),
        ("Solve $e^{2x}=e^{6}$.",
         3,
         "One-to-one: $2x=6$, $x=3$.",
         None),
        ("Solve $\\log_2 x+\\log_2(x-2)=3$ (valid solution).",
         4,
         "$\\log_2(x(x-2))=3$, $x(x-2)=8$, $x^2-2x-8=0$, $(x-4)(x+2)=0$. Discard $x=-2$; $x=4$ works.",
         ["-2", "2", "8"]),
        ("Solve $5^{x+1}=25^{x-1}$.",
         3,
         "$25=5^2$ so $5^{x+1}=5^{2x-2}$, hence $x+1=2x-2$, $x=3$.",
         ["1", "2", "0"]),
        ("A logistic $P=\\dfrac{100}{1+4e^{-0.2t}}$ has carrying capacity:",
         100,
         "As $t\\to\\infty$, $e^{-0.2t}\\to0$, so $P\\to100$.",
         ["4", "0.2", "25"]),
        ("At $t=0$, that same logistic equals:",
         20,
         "$P(0)=100/(1+4)=20$.",
         ["100", "4", "0"]),
        ("Unlike an exponential, a logistic model:",
         "levels off at a carrying capacity",
         "The horizontal asymptote $y=L$ is the long-run ceiling.",
         ["grows without bound", "is a straight line", "is undefined for t>0"]),
        ("If a logistic starts below $L/2$, the graph is:",
         "S-shaped, accelerating then slowing",
         "Classic sigmoid: slow, then steep near $L/2$, then flattening toward $L$.",
         ["a downward parabola", "a V", "a hyperbola only"]),
        ("The range of $P=\\dfrac{L}{1+Ae^{-kt}}$ for $A>0,k>0,L>0$ and $t\\geq0$ is:",
         "(L/(1+A), L)",
         "Starts at $L/(1+A)$ and approaches $L$ from below, never reaching $L$ in finite time.",
         ["(0,L]", "[0,L]", "all reals"]),
        ("$4^{3/2}$ equals:",
         8,
         "$4^{3/2}=(2^2)^{3/2}=2^3=8$.",
         ["6", "16", "2"]),
        ("$\\ln e^5$ simplifies to:",
         5,
         "Log and exponential with base $e$ cancel: $\\ln(e^5)=5$.",
         ["e^5", "1", "ln 5"]),
        ("$e^{\\ln 7}$ equals:",
         7,
         "The other cancellation: $b^{\\log_b a}=a$.",
         ["ln 7", "e^7", "1"]),
        ("Solve $10^{x}=0.001$.",
         -3,
         "$0.001=10^{-3}$.",
         ["3", "0.001", "-1"]),
        ("The vertical asymptote of $y=\\log_2(x+3)$ is:",
         "x=-3",
         "Argument $\\to 0^+$ when $x\\to-3^+$.",
         ["x=0", "x=3", "y=-3"]),
        ("Product rule fails if you write $\\log(x+y)$ as:",
         "log x + log y",
         "The rule needs a product inside, not a sum. $\\log(x+y)\\neq\\log x+\\log y$.",
         ["log(xy)", "log x + log(y/x) + log y? no", "ln(e^{x+y})"]),
        ("Solve $2\\log_4 x=\\log_4 36$.",
         6,
         "Power: $\\log_4(x^2)=\\log_4 36$, so $x^2=36$, $x=6$ (domain $x>0$ discards $-6$).",
         ["36", "-6", "18"]),
        ("If $\\log_b a=c$ then $b^c$ equals:",
         "a",
         "That is the definition of logarithm.",
         ["c", "b", "1"]),
        ("A 12% annual compound model is $A=P(1.12)^t$. After $0$ years, $A=$:",
         "P",
         "Any exponential (or logistic) at $t=0$ returns the initial value.",
         ["1.12P", "0", "12P"]),
        ("$\\log_2(1/16)$ equals:",
         -4,
         "$1/16=2^{-4}$.",
         ["4", "1/4", "-2"]),
        ("Change $\\log_8 2$ into a simple fraction.",
         "1/3",
         "$8^{1/3}=2$.",
         ["3", "4", "1/2"]),
        ("Solve $\\ln(2x)=0$.",
         "1/2",
         "$2x=e^0=1$, so $x=1/2$.",
         ["0", "1", "e"]),
        ("The range of $y=2^x$ is:",
         "y>0",
         "An exponential with positive base never hits $0$ or negatives.",
         ["all reals", "y\u22650", "y>2"]),
        ("$\\log_3 9x$ expands to:",
         "2 + log_3 x",
         "$\\log_3 9+\\log_3 x=2+\\log_3 x$ (for $x>0$).",
         ["log_3 9x as a product of logs", "9 log_3 x", "2 log_3 x"]),
        ("A population $P=50e^{0.1t}$ doubles when $0.1t=\\ln 2$, so $t=$:",
         "10 ln 2",
         "$e^{0.1t}=2$, $0.1t=\\ln 2$, $t=10\\ln 2$.",
         ["ln 2", "0.1 ln 2", "2/0.1"]),
        ("SAT Stretch: Solve $\\log_2(x-1)+\\log_2(x+1)=3$ and keep only valid $x$.",
         "x=3",
         "Condense: $\\log_2((x-1)(x+1))=3$, so $x^2-1=8$, $x^2=9$, $x=\\pm3$. Domain needs $x>1$, so $x=3$. "
         "Check: $\\log_2 2+\\log_2 4=1+2=3$.",
         ["x=-3", "x=2", "x=9"]),
        ("SAT Stretch: If $f(x)=2^{x-1}$ then $(f^{-1}\\circ f^{-1})(8)$ equals:",
         3,
         "$f^{-1}(x)=1+\\log_2 x$. Then $f^{-1}(8)=4$ and $f^{-1}(4)=3$.",
         ["4", "8", "2"]),
        ("SAT Stretch: $3^{2x+1}=7^{x-1}$. Solving by logs yields $x=$:",
         "(ln 7 + ln 3)/(ln 7 - 2 ln 3)",
         "Take $\\ln$: $(2x+1)\\ln 3=(x-1)\\ln 7$. Then $2x\\ln 3-x\\ln 7=-\\ln 7-\\ln 3$, "
         "so $x=(\\ln 7+\\ln 3)/(\\ln 7-2\\ln 3)$.",
         ["(ln 7 + ln 3)/(2 ln 3 - ln 7)", "(2 ln 3)/(ln 7)", "1"]),
        ("SAT Stretch: Logistic $P=\\dfrac{120}{1+5e^{-0.4t}}$ equals $60$ when:",
         "t=(5/2) ln 5",
         "$1+5e^{-0.4t}=2$, so $e^{-0.4t}=1/5$, hence $t=(\\ln 5)/0.4=(5/2)\\ln 5$.",
         ["ln 5", "5 ln 5", "0.4 ln 5"]),
        ("SAT Stretch: Combine $\\dfrac{1}{2}\\log_b(x+1)-\\log_b(x-1)+\\log_b 4$ into a single log.",
         "log_b (4 sqrt(x+1)/(x-1))",
         "Power, then product/quotient: $\\log_b\\dfrac{4\\sqrt{x+1}}{x-1}$.",
         ["log_b(4(x+1)/(x-1))", "1/2 log_b 4(x+1)(x-1)", "log_b(sqrt(x+1)-x+1)"]),
        ("SAT Stretch: The inverse of $g(x)=\\ln(2x-1)+3$ is $g^{-1}(x)=$:",
         "(e^{x-3}+1)/2",
         "Set $y=\\ln(2x-1)+3$, so $e^{y-3}=2x-1$ and $x=(e^{y-3}+1)/2$. Swap names.",
         ["e^{x+3}/2", "ln((x-3)/2)", "(e^x+3)/2"]),
        ("SAT Stretch: Solve $2^{x^2}=4^{x+2}$ for all real $x$.",
         "1+\u221a5 and 1-\u221a5",
         "$4=2^2$, so $2^{x^2}=2^{2x+4}$. Then $x^2-2x-4=0$, $x=1\\pm\\sqrt{5}$. Both are real.",
         ["x=4 or x=-2", "2 only", "no real solution"]),
        ("SAT Stretch: For $0<b<1$ and $a>1$, $\\log_b a$ is:",
         "negative",
         "A decaying exponential $b^t$ with $0<b<1$ hits a number $a>1$ at a negative exponent.",
         ["positive", "zero", "greater than a"]),
        ("SAT Stretch: If $\\log_2(\\log_3 x)=1$, then $x=$:",
         9,
         "$\\log_3 x=2^1=2$, so $x=3^2=9$.",
         ["3", "8", "6"]),
        ("SAT Stretch: Logistic $P=\\dfrac{80}{1+Ae^{-kt}}$ has $P(0)=16$ and $P(5)=40$. Then $k=$:",
         "(2 ln 2)/5",
         "$16=80/(1+A)$ forces $A=4$. Then $40=80/(1+4e^{-5k})$ so $e^{-5k}=1/4$, hence $5k=\\ln 4=2\\ln 2$ "
         "and $k=(2\\ln 2)/5$.",
         ["ln 4", "(ln 4)/4", "4/5"]),
    ])
    return qs[:55]


def build_unit3():
    title = "Precalculus Unit 3: Exponential & Logarithmic Functions"
    description = (
        "Growth and decay, logs as inverses, log laws, change of base, solving exp/log equations, "
        "and a first look at logistic models — with matching $a^x$ and $\\log_a x$ graphs."
    )
    concepts = [
        "Growth and decay",
        "Log as inverse",
        "Log laws",
        "Change of base",
        "Solve exp/log equations",
        "Logistic intro",
    ]

    exp_pts = sample_curve(lambda x: 2 ** x, -3, 3)
    log_pts = sample_curve(lambda x: math.log(x, 2) if x > 0.08 else 1e9, 0.1, 8)

    c1 = concept_block(
        "1. Growth and decay",
        [
            "An exponential function has the form $f(x)=a\\cdot b^x$ (or $a e^{kx}$) with $a\\neq0$ and base "
            "$b>0$, $b\\neq1$. The variable lives in the exponent. That single fact is why exponential graphs "
            "are never lines and why a constant percent change produces a curve, not a slope.",
            "If $b>1$, the model is exponential growth: each step multiplies by more than $1$. If $0<b<1$, "
            "the model is exponential decay: each step multiplies by a proper fraction. The number $a=f(0)$ is "
            "the initial value. In $Q=40(1.05)^t$, you start at $40$ and grow $5\\%$ per time unit.",
            "Half-life is decay with a particularly nice base. If a quantity halves every $h$ hours, then "
            "$N=N_0\\left(\\dfrac{1}{2}\\right)^{t/h}$. After $t=h$ you have half; after $t=2h$ you have a quarter. "
            "Radioactive decay, caffeine clearance, and some cooling models use this language.",
            "Continuous compounding replaces the discrete base $1+r$ with $e^{rt}$. The number $e\\approx2.718$ "
            "is the unique base whose tangent slope at $0$ is $1$ — calculus will explain why it is natural. "
            "For Precalculus, treat $e^{rt}$ as the smooth analogue of $(1+r)^t$.",
            "Exponential graphs have a horizontal asymptote $y=0$ (unless a vertical shift is added). They "
            "never cross the x-axis. Growth starts slowly-looking near the y-intercept and then steepens; decay "
            "dives toward the axis but never lands.",
            "The inverse of an exponential is a logarithm, which is the next lesson. Every time you solve "
            "$b^x=k$ by “taking log,” you are using that inverse. Growth models that ask “when does it double?” "
            "are logarithm problems wearing an applications costume.",
        ],
        "Percent change, compound interest, half-life, and unconstrained population models are all one family. "
        "Recognizing the base tells you immediately whether the story is growth or decay.",
        "Write $f(0)$ as the start, name the multiplier per time unit, and decide whether that multiplier is "
        "greater than $1$ or between $0$ and $1$. For half-life, use base $1/2$ with exponent $t/h$.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#4f46e5", sample_curve(lambda x: 40 * (1.05) ** x, -2, 20)),
                    ("#dc2626", sample_curve(lambda x: 200 * (0.85) ** x, -1, 16)),
                ],
                xlim=(-2, 20), ylim=(-10, 220),
            ),
            "Blue $40(1.05)^t$ grows; red $200(0.85)^t$ decays toward $0$",
            "Both are exponential. The base compared with $1$ decides the direction.",
        )
        + solved(
            1, "Classify $Q=40(1.05)^t$ and evaluate $Q(0)$.",
            ["Base $1.05>1$, so this is growth of $5\\%$ per unit time.",
             "$Q(0)=40(1.05)^0=40$.",
             "The graph rises, with horizontal asymptote $y=0$ if extended left."],
            "growth; $Q(0)=40$", "", "Easy",
        )
        + solved(
            2, "Find $A=200(0.85)^t$ at $t=2$.",
            ["$0.85^2=0.7225$.",
             "$200\\times0.7225=144.5$.",
             "Decay: two steps of $15\\%$ off leave $85\\%$ of $85\\%$ of $200$."],
            "$144.5$", "", "Medium",
        )
        + solved(
            3, "A sample has half-life $8$ hours. Write $N(t)$ and find when $N$ is one-fourth of $N_0$.",
            ["$N=N_0(1/2)^{t/8}$.",
             "One-fourth is two halvings, so $t=16$ hours.",
             "Check: $(1/2)^{16/8}=(1/2)^2=1/4$."],
            "$N=N_0(1/2)^{t/8}$; $t=16$", "Two half-lives, not half of $8$.", "Hard",
        ),
        ("Treating $40(1.05)^t$ as linear $+5\\%$ of $40$ each year without compounding",
         "Exponential percent change compounds. Year two is $5\\%$ of the new amount, not $5\\%$ of the original "
         "only. That is why the formula multiplies, rather than adding $0.05\\times40$ repeatedly."),
        ("Read the base, not just the exponent",
         "A negative exponent on a base greater than $1$ is still growth-in-reverse (a point left of $0$), not "
         "a different family. Decay is about $0<b<1$ (or a negative continuous rate), not about a minus sign in the exponent alone."),
        [
            "I can classify growth versus decay from the base.",
            "I can evaluate $a\\cdot b^t$ at a given $t$.",
            "I can write a half-life model and interpret $t=h$ and $t=2h$.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Log as inverse",
        [
            "The logarithm $\\log_b a$ is defined to be the exponent you put on $b$ to get $a$. In symbols, "
            "$\\log_b a=c$ if and only if $b^c=a$, with $a>0$, $b>0$, $b\\neq1$. That sentence is the entire "
            "definition. Everything else (laws, change of base, solving) is this sentence wearing algebra.",
            "Because logs undo exponentials, $y=\\log_b x$ is the inverse of $y=b^x$. Their graphs are reflections "
            "across $y=x$. The exponential has a horizontal asymptote $y=0$; the log has a vertical asymptote "
            "$x=0$. Domain and range swap: $b^x$ has domain $\\mathbb{R}$ and range $(0,\\infty)$; $\\log_b x$ "
            "has domain $(0,\\infty)$ and range $\\mathbb{R}$.",
            "Two cancellation identities follow from inverses: $b^{\\log_b a}=a$ and $\\log_b(b^c)=c$. In base "
            "$e$ they read $e^{\\ln a}=a$ and $\\ln(e^c)=c$. These are the fastest simplifications on the SAT.",
            "Shifts work as in Unit 1. $\\log_b(x-h)$ has vertical asymptote $x=h$ and domain $x>h$. A vertical "
            "shift $\\log_b x+k$ moves the graph up without changing the asymptote. A coefficient in front is a "
            "vertical stretch, and a negative sign reflects over the x-axis.",
            "Common log is base $10$; natural log $\\ln$ is base $e$. They are not different theories. They are "
            "the two calculator buttons for the same inverse idea. Change of base (next-next lesson) converts "
            "any log into a ratio of $\\ln$ or $\\log_{10}$ values.",
            "Graphically, you should be able to sketch $y=2^x$ and $y=\\log_2 x$ on the same axes, draw $y=x$, "
            "and see the mirror. That picture is how you remember domain, range, intercepts $(1,0)$ for the log "
            "and $(0,1)$ for the exponential, and why logs of numbers between $0$ and $1$ are negative when $b>1$.",
        ],
        "Every exponential equation you solve, every Richter/pH/decibel scale, and the definition of inverse "
        "trig later, is “name the inverse and swap.” Logs are the first inverse that is not a simple algebraic formula.",
        "Translate every log statement into an exponential statement before you simplify. If you cannot say "
        "$b^{\\text{answer}}=\\text{argument}$, you have not used the definition yet.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", exp_pts), ("#dc2626", log_pts), ("#16a34a", sample_curve(lambda x: x, -3, 8))],
                points=[(0, 1, "(0,1)"), (1, 0, "(1,0)")],
                xlim=(-3, 8), ylim=(-3, 8),
            ),
            "$y=2^x$ (blue), $y=x$ (green), $y=\\log_2 x$ (red)",
            "The log is the inverse: reflection of the exponential across the diagonal.",
        )
        + solved(
            4, "Evaluate $\\log_2 8$ using the definition.",
            ["Ask: $2$ to what power is $8$?",
             "$2^3=8$.",
             "Therefore $\\log_2 8=3$."],
            "$3$", "", "Easy",
        )
        + solved(
            5, "Name the inverse of $f(x)=3^x$ and state the domain of that inverse.",
            ["The inverse is $f^{-1}(x)=\\log_3 x$.",
             "Logs require a positive argument, so domain is $x>0$.",
             "Range of the inverse is all reals, matching the domain of $3^x$."],
            "$\\log_3 x$, domain $x>0$", "", "Medium",
        )
        + solved(
            6, "Find the domain of $y=\\log_5(x-1)$ and the vertical asymptote.",
            ["Need $x-1>0$, so $x>1$.",
             "As $x\\to1^+$, the argument $\\to0^+$, so $y\\to-\\infty$.",
             "Vertical asymptote $x=1$."],
            "domain $x>1$, VA $x=1$", "Not $x\\geq1$: logs never include argument $0$.", "Hard",
        ),
        ("Writing $\\log_b(x+y)=\\log_b x+\\log_b y$",
         "That “rule” is false. The product rule needs a product inside one log, not a sum. Translating to "
         "exponentials instantly shows the mistake: $b^{c+d}=b^c b^d$, not $b^c+b^d$."),
        ("Sketch both graphs with $y=x$",
         "If you forget whether $(0,1)$ belongs to the exponential or the log, draw the pair. The exponential "
         "owns $(0,1)$; the log owns $(1,0)$. They swap under the inverse."),
        [
            "I can convert between $b^c=a$ and $\\log_b a=c$.",
            "I can name log as the inverse of exponential and reflect across $y=x$.",
            "I can find a log’s domain from a shifted argument.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Log laws",
        [
            "Three laws do almost all of the algebraic work. Product: $\\log_b(xy)=\\log_b x+\\log_b y$. "
            "Quotient: $\\log_b(x/y)=\\log_b x-\\log_b y$. Power: $\\log_b(x^k)=k\\log_b x$. Each is the log of "
            "an exponential identity: multiplying adds exponents, dividing subtracts, and a power multiplies an exponent.",
            "The laws require positive arguments (and a legal base). Expanding $\\log(x^2)$ as $2\\log x$ is "
            "safe for $x>0$; for $x<0$ the original $\\log(x^2)$ is defined but $2\\log x$ is not. In Precalculus "
            "we usually stay in $x>0$ unless a problem forces the issue.",
            "Condensing (the reverse direction) is how you solve equations such as $\\log x+\\log(x-2)=1$. You "
            "must condense to a single log before you exponentiate. Expanding is how you take a derivative later "
            "in calculus, and how you simplify a nested expression on a test.",
            "Change-of-base is not a fourth independent law so much as a consequence: $\\log_b a=\\dfrac{\\log_k a}{\\log_k b}$. "
            "We give it its own lesson because it is the calculator move. The product/quotient/power laws are "
            "the pencil moves.",
            "A frequent error is applying a law to a sum inside a log. There is no nice expansion of "
            "$\\log(x+y)$. Another is dropping the base: $\\log_2 8+\\log_2 4=\\log_2(32)$, not $\\log_4$ of something "
            "unless you meant to change base.",
            "Practice until condensing and expanding feel like factoring and distributing. The next lesson uses "
            "change of base; the lesson after that uses the laws to solve equations that are not immediately one-to-one.",
        ],
        "Log laws turn products into sums, which is why they appear in orders of magnitude, pH, decibels, and "
        "in the algebra of solving exponential models for time.",
        "Only expand or condense when the inside is a product, quotient, or power. If you see a sum or difference "
        "inside a log, stop: that is not a law, that is a different expression.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", log_pts)],
                points=[(8, 3, "log2 8=3"), (4, 2, "log2 4=2"), (32, 5, "log2 32=5")],
                xlim=(-1, 36), ylim=(-1, 6),
            ),
            "Product rule in points: $\\log_2 8+\\log_2 4=\\log_2 32$",
            "Heights $3+2=5$ match the log of the product $32$.",
        )
        + solved(
            7, "Simplify $\\log_2 8+\\log_2 4$.",
            ["Product rule: $\\log_2(8\\cdot4)=\\log_2 32$.",
             "$32=2^5$, so the value is $5$.",
             "Alternatively $3+2=5$ from known powers."],
            "$5$", "", "Easy",
        )
        + solved(
            8, "Simplify $\\log_3 54-\\log_3 2$.",
            ["Quotient rule: $\\log_3(54/2)=\\log_3 27$.",
             "$27=3^3$, so the value is $3$."],
            "$3$", "", "Medium",
        )
        + solved(
            9, "Expand $\\log\\dfrac{x^2}{y}$ fully.",
            ["Quotient: $\\log(x^2)-\\log y$.",
             "Power: $2\\log x-\\log y$.",
             "Domain in typical Precalculus work: $x>0$, $y>0$."],
            "$2\\log x-\\log y$", "Do not write $\\log(x^2-y)$.", "Hard",
        ),
        ("Inventing a law for $\\log(x+y)$",
         "Sums inside logs do not split. If a problem hands you $\\ln(x+1)$, leave it, or exponentiate both "
         "sides of an equation; do not write $\\ln x+\\ln 1$."),
        ("Condense before you exponentiate",
         "A sum of logs is not an exponent until it is one log. Use the product/quotient laws first, then "
         "rewrite in exponential form."),
        [
            "I can apply product, quotient, and power laws.",
            "I can expand and condense log expressions.",
            "I know $\\log(x+y)$ does not split.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Change of base",
        [
            "Calculators typically offer $\\log_{10}$ and $\\ln$. Change of base converts any log into a ratio "
            "of those: $\\log_b a=\\dfrac{\\ln a}{\\ln b}=\\dfrac{\\log_{10} a}{\\log_{10} b}$. The identity is "
            "true for any legal auxiliary base $k$ in both the numerator and the denominator.",
            "The proof is one line of definition. Let $y=\\log_b a$, so $b^y=a$. Take $\\ln$: $y\\ln b=\\ln a$, "
            "hence $y=\\dfrac{\\ln a}{\\ln b}$. That is why the formula looks like “divide logs.”",
            "Change of base also simplifies some exact values. $\\log_9 27=\\dfrac{\\ln 27}{\\ln 9}=\\dfrac{3\\ln 3}{2\\ln 3}=\\dfrac{3}{2}$. "
            "You can also see $9^{3/2}=(3^2)^{3/2}=3^3=27$. Either route is legal; the ratio of integer exponents "
            "on a shared prime is the fastest exact method.",
            "A related identity: $\\dfrac{\\log_c a}{\\log_c b}=\\log_b a$. So a quotient of logs with the same "
            "base is itself a log. This is how $\\dfrac{\\log_5 36}{\\log_5 6}=\\log_6 36=2$ in one step.",
            "When the base is between $0$ and $1$, logs of arguments greater than $1$ are negative. Change of "
            "base still works: $\\log_{1/2} 8=\\dfrac{\\ln 8}{\\ln(1/2)}=\\dfrac{3\\ln 2}{-\\ln 2}=-3$, matching "
            "$(1/2)^{-3}=8$.",
            "On a test, if an answer choice looks like $\\dfrac{\\ln 20}{\\ln 7}$, that is the calculator form of "
            "$\\log_7 20$, not a different number. Do not “simplify” it to $\\ln(20/7)$ — that would be a law error.",
        ],
        "Change of base is the bridge from “logs in a textbook base” to “a number your calculator can produce,” "
        "and it is how you compare growth rates with different bases.",
        "To evaluate $\\log_b a$ on a calculator, divide $\\ln a$ by $\\ln b$ (or common logs). To get an exact "
        "rational value, write both $a$ and $b$ as powers of the same integer when possible.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#4f46e5", sample_curve(lambda x: math.log(x, 9) if x > 0.2 else 1e9, 0.3, 40)),
                    ("#dc2626", sample_curve(lambda x: math.log(x, 3) if x > 0.2 else 1e9, 0.3, 40)),
                ],
                points=[(27, 1.5, "log9 27=3/2")],
                xlim=(-2, 40), ylim=(-2, 4),
            ),
            "$\\log_9 27=3/2$ sits on $y=\\log_9 x$ (blue)",
            "Change of base: $\\ln27/\\ln9=3/2$. The red curve $y=\\log_3 x$ is a vertical stretch of the blue one.",
        )
        + solved(
            10, "Write $\\log_2 10$ using common logs.",
            ["Change of base: $\\log_2 10=\\dfrac{\\log_{10} 10}{\\log_{10} 2}$.",
             "$\\log_{10}10=1$, so this is $1/\\log_{10}2$.",
             "Either form is calculator-ready."],
            "$\\log 10/\\log 2$", "", "Easy",
        )
        + solved(
            11, "Evaluate $\\log_9 27$ exactly.",
            ["$\\dfrac{\\ln 27}{\\ln 9}=\\dfrac{3\\ln 3}{2\\ln 3}=3/2$.",
             "Check: $9^{3/2}=(3^2)^{3/2}=3^3=27$."],
            "$3/2$", "", "Medium",
        )
        + solved(
            12, "Simplify $\\dfrac{\\log_5 36}{\\log_5 6}$.",
            ["Quotient of same-base logs is $\\log_6 36$.",
             "$6^2=36$, so the value is $2$.",
             "Change of base to $\\ln$ would cancel the same way."],
            "$2$", "", "Hard",
        ),
        ("Writing $\\dfrac{\\ln a}{\\ln b}=\\ln(a/b)$",
         "Change of base is a ratio of logs, not the log of a ratio. The quotient law would have one log of "
         "$a/b$, which is a different number unless $\\ln b=1$."),
        ("Powers of the same integer",
         "If both argument and base are powers of $2$, $3$, or $10$, skip the calculator and cancel exponents. "
         "That is how $\\log_8 2=1/3$ and $\\log_9 27=3/2$ become mental arithmetic."),
        [
            "I can rewrite $\\log_b a$ as a ratio of $\\ln$ or $\\log_{10}$.",
            "I can evaluate some logs exactly by matching prime powers.",
            "I can treat a quotient of same-base logs as a single log.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Solve exp/log equations",
        [
            "The one-to-one strategy: if $b^{u}=b^{v}$, then $u=v$. If $\\log_b u=\\log_b v$, then $u=v$ (with "
            "positive arguments). Matching bases, or matching logs, turns an exponential or log equation into "
            "an algebraic one.",
            "The inverse strategy: take $\\log$ of both sides of $b^{u}=k$, or rewrite $\\log_b u=c$ as $u=b^c$. "
            "These are the same inverse pair from lesson 2. Always check the domain after you solve, especially "
            "when logs of expressions in $x$ are involved.",
            "When several logs are added or subtracted, condense first with the laws, then exponentiate. "
            "$\\log_2 x+\\log_2(x-2)=3$ becomes $\\log_2(x(x-2))=3$, then $x(x-2)=8$. The quadratic may produce "
            "an extra root that makes an argument nonpositive; throw that root away.",
            "Equations with different bases, such as $3^{2x+1}=7^{x-1}$, need logs on both sides (any base). "
            "Then factor $x$ and solve a linear equation in $x$ whose coefficients are logarithms. The answer "
            "is often left in exact log form.",
            "Extraneous roots are the main hazard. Any candidate that makes a log argument $\\leq0$, or that "
            "was produced by squaring, must be tested in the original equation. Showing the check is part of "
            "the solution, not an optional courtesy.",
            "Applied doubling-time problems are this lesson: $Pe^{rt}=2P$ becomes $e^{rt}=2$, $t=\\dfrac{\\ln 2}{r}$. "
            "The algebra is short once you trust the inverse.",
        ],
        "Solving for time in a growth model, inverting a pH formula, and later solving $A e^{kt}=B$ in differential "
        "equations are the same two moves: log both sides, or rewrite a log as an exponential.",
        "Match bases if you can. Otherwise take a log (any legal base) of both sides. Condense sums of logs "
        "before you exponentiate. Then test every candidate in the original equation’s domain.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#4f46e5", sample_curve(lambda x: 2 ** x, -1, 6)),
                    ("#dc2626", sample_curve(lambda x: 32, -1, 6)),
                ],
                points=[(5, 32, "(5,32)")],
                xlim=(-1, 6), ylim=(-2, 40),
            ),
            "Solving $2^x=32$ is finding the intersection with $y=32$",
            "The unique intersection is $x=5$ because $2^5=32$.",
        )
        + solved(
            13, "Solve $2^x=32$.",
            ["Write $32=2^5$.",
             "One-to-one: $x=5$.",
             "Check: $2^5=32$."],
            "$x=5$", "", "Easy",
        )
        + solved(
            14, "Solve $\\log_3(x-1)=2$.",
            ["Rewrite as $x-1=3^2=9$.",
             "$x=10$.",
             "Check: argument $9>0$ and $\\log_3 9=2$."],
            "$x=10$", "", "Medium",
        )
        + solved(
            15, "Solve $\\log_2 x+\\log_2(x-2)=3$.",
            ["Condense: $\\log_2(x(x-2))=3$.",
             "$x(x-2)=8$, so $x^2-2x-8=0$, $(x-4)(x+2)=0$.",
             "Candidates $x=4$ and $x=-2$. Domain requires $x>2$, so discard $x=-2$.",
             "Check $x=4$: $\\log_2 4+\\log_2 2=2+1=3$."],
            "$x=4$", "The discarded root is the classic extraneous log solution.", "Hard",
        ),
        ("Keeping a root that makes a log argument negative",
         "The algebra after exponentiating can introduce extras. The original equation’s domain is the judge. "
         "If $x-2\\leq0$ in $\\log(x-2)$, that $x$ is gone."),
        ("Condense, then convert",
         "Do not exponentiate a sum of logs term by term. Make one log, then write the equivalent exponential "
         "statement once."),
        [
            "I can solve $b^u=b^v$ and $\\log_b u=c$.",
            "I can condense and then exponentiate.",
            "I can discard extraneous roots using the log domain.",
        ],
        21,
    )

    logis = sample_curve(lambda t: 100 / (1 + 4 * math.exp(-0.2 * t)), -2, 30)
    c6 = concept_block(
        "6. Logistic intro",
        [
            "Real populations cannot follow $Pe^{rt}$ forever: food, space, and resources cap growth. The "
            "logistic model $P(t)=\\dfrac{L}{1+Ae^{-kt}}$ (with $L>0$, $A>0$, $k>0$) builds in a carrying "
            "capacity $L$. As $t\\to\\infty$, the exponential $e^{-kt}\\to0$, so $P\\to L$. The graph is an S-curve.",
            "At $t=0$, $P(0)=\\dfrac{L}{1+A}$. If you know the start and the cap, you can solve for $A$. The "
            "parameter $k$ controls how quickly the S rises. Larger $k$ means a steeper middle.",
            "The steepest growth is near $P=L/2$, the inflection. Below $L/2$ the graph is concave up (growth "
            "rate increasing); above $L/2$ it is concave down (growth rate decreasing as the cap bites). You "
            "do not need derivatives to remember the shape: slow, then fast, then slow again.",
            "Logistic is still built from exponentials, so solving $P(t)=M$ for time uses the same log algebra "
            "as lesson 5. Isolate the exponential, then take $\\ln$. The SAT stretch in this unit asks exactly that.",
            "Unlike a shifted exponential, a logistic with $0<P(0)<L$ never exceeds $L$ and never hits $L$ in "
            "finite time. The line $y=L$ is a horizontal asymptote, not a value the model attains.",
            "When a word problem mentions a limited environment, a maximum enrollment, or a rumor that “everyone "
            "already knows,” logistic is the right family. When it mentions unconstrained doubling, exponential "
            "is the right family. Choosing the family is half the modeling battle.",
        ],
        "Logistic curves are the first bounded-growth models you meet, and they reappear in biology, chemistry "
        "(autocatalysis), and later as solutions of the logistic differential equation.",
        "Read $L$ off the formula as the carrying capacity. Compute $P(0)=L/(1+A)$. Sketch an S between those "
        "two heights, flattening toward $L$. To solve for $t$, isolate $e^{-kt}$ and take $\\ln$.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", logis)],
                dashes=[("h", 100, "L=100")],
                points=[(0, 20, "P(0)=20")],
                xlim=(-2, 30), ylim=(-5, 120),
            ),
            "Logistic $P=\\dfrac{100}{1+4e^{-0.2t}}$ with carrying capacity $100$",
            "The S-curve starts at $20$ and rises toward the dashed line $y=100$, never crossing it.",
        )
        + solved(
            16, "For $P=\\dfrac{100}{1+4e^{-0.2t}}$, name the carrying capacity and $P(0)$.",
            ["As $t\\to\\infty$, $P\\to100$, so $L=100$.",
             "$P(0)=100/(1+4)=20$.",
             "The graph is an S from $20$ up toward $100$."],
            "$L=100$, $P(0)=20$", "", "Easy",
        )
        + solved(
            17, "How does a logistic differ from $P=20e^{0.2t}$ in the long run?",
            ["The exponential grows without bound.",
             "The logistic levels off at a finite $L$.",
             "For small $t$ they can look similar; for large $t$ they do not."],
            "logistic levels off; exponential does not", "", "Medium",
        )
        + solved(
            18, "Solve $P=60$ for the logistic $P=\\dfrac{120}{1+5e^{-0.4t}}$.",
            ["$60=\\dfrac{120}{1+5e^{-0.4t}}$, so $1+5e^{-0.4t}=2$.",
             "$5e^{-0.4t}=1$, $e^{-0.4t}=1/5$.",
             "$-0.4t=\\ln(1/5)=-\\ln5$, hence $t=(\\ln5)/0.4=(5/2)\\ln5$."],
            "$t=\\dfrac{5}{2}\\ln5$", "Isolate the exponential, then take $\\ln$.", "Hard",
        ),
        ("Treating $L$ as a value the population reaches at a finite time",
         "The carrying capacity is an asymptote. $P(t)=L$ would require the denominator $1+Ae^{-kt}=1$, hence "
         "$A=0$, which is not a genuine logistic. Say “approaches $L$,” not “hits $L$ at $t=\\ldots$.”"),
        ("Isolate $e^{-kt}$ before taking $\\ln$",
         "Do not take $\\ln$ of a sum. Clear the denominator, subtract $1$, divide by $A$, then $\\ln$ both sides."),
        [
            "I can read $L$ and $P(0)$ from a logistic formula.",
            "I can sketch an S-curve with a horizontal asymptote $y=L$.",
            "I can solve $P(t)=M$ using logarithms.",
        ],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title, AUDIENCE, concepts, body, practice_slots(31, 25, STRETCH_LABEL),
    )
    return title, description, content, _u3_questions()


# ===========================================================================
# UNIT 4: Trigonometry for Precalculus
# ===========================================================================

def _u4_questions():
    qs = []
    _add(qs, [
        ("On the unit circle, $\\cos\\dfrac{\\pi}{3}$ equals:",
         "1/2",
         "The $60^\\circ$ point is $(1/2,\\sqrt{3}/2)$. Cosine is the x-coordinate.",
         ["\\sqrt{3}/2", "\\sqrt{2}/2", "0"]),
        ("$\\sin\\dfrac{3\\pi}{2}$ equals:",
         "-1",
         "The point is $(0,-1)$; sine is the y-coordinate.",
         ["1", "0", "1/2"]),
        ("$\\tan\\dfrac{\\pi}{4}$ equals:",
         1,
         "$\\sin$ and $\\cos$ are equal at $45^\\circ$, so their ratio is $1$.",
         ["0", "\\sqrt{3}", "undefined"]),
        ("A reference angle for $150^\\circ$ is:",
         "30°",
         "$180^\\circ-150^\\circ=30^\\circ$ in quadrant II.",
         ["150°", "60°", "15°"]),
        ("$\\cos\\theta$ is negative and $\\sin\\theta$ is positive in which quadrant?",
         "II",
         "x-coordinate negative, y-coordinate positive is quadrant II.",
         ["I", "III", "IV"]),
        ("The period of $y=\\sin x$ is:",
         "2\u03c0",
         "Sine completes one cycle every $2\\pi$ radians.",
         ["\u03c0", "1", "\u03c0/2"]),
        ("The period of $y=\\tan x$ is:",
         "\u03c0",
         "Tangent repeats every $\\pi$, with vertical asymptotes at odd multiples of $\\pi/2$.",
         ["2\u03c0", "2", "\u03c0/2"]),
        ("Amplitude of $y=3\\cos(2x)$ is:",
         3,
         "Amplitude is $|A|$ in $A\\cos(Bx)$.",
         ["2", "6", "1/3"]),
        ("Period of $y=3\\cos(2x)$ is:",
         "\u03c0",
         "Period $=2\\pi/|B|=2\\pi/2=\\pi$.",
         ["2\u03c0", "2", "3"]),
        ("$y=\\csc x$ has vertical asymptotes where:",
         "sin x = 0",
         "Cosecant is $1/\\sin x$, undefined at integer multiples of $\\pi$.",
         ["cos x = 0", "tan x = 0", "x=1"]),
        ("$\\sin^2\\theta+\\cos^2\\theta$ equals:",
         1,
         "The Pythagorean identity on the unit circle: $x^2+y^2=1$.",
         ["0", "2", "tan^2 \u03b8"]),
        ("$1+\\tan^2\\theta$ simplifies to:",
         "sec^2 \u03b8",
         "Divide the primary Pythagorean identity by $\\cos^2\\theta$.",
         ["csc^2 \u03b8", "sin^2 \u03b8", "1"]),
        ("$\\sin(2\\theta)$ expands to:",
         "2 sin \u03b8 cos \u03b8",
         "The double-angle formula for sine.",
         ["sin^2 \u03b8", "2 sin \u03b8", "cos 2\u03b8"]),
        ("$\\cos(2\\theta)$ is not equal to which of these?",
         "2 sin \u03b8 cos \u03b8",
         "That is $\\sin(2\\theta)$. Valid cosine double-angles are $\\cos^2-\\sin^2$, $2\\cos^2-1$, $1-2\\sin^2$.",
         ["cos^2 \u03b8 - sin^2 \u03b8", "2 cos^2 \u03b8 - 1", "1 - 2 sin^2 \u03b8"]),
        ("$\\tan\\theta=\\dfrac{\\sin\\theta}{\\cos\\theta}$ is undefined when:",
         "cos \u03b8 = 0",
         "Division by zero; those $\\theta$ are the tangent asymptotes.",
         ["sin \u03b8 = 0", "\u03b8 = 0", "tan \u03b8 = 1"]),
        ("Solve $\\sin\\theta=1/2$ on $[0,2\\pi)$. The solutions are:",
         "\u03c0/6 and 5\u03c0/6",
         "Sine is positive in I and II; reference $\\pi/6$.",
         ["\u03c0/6 only", "\u03c0/3 and 2\u03c0/3", "\u03c0/2"]),
        ("Solve $\\cos\\theta=0$ on $[0,2\\pi)$.",
         "\u03c0/2 and 3\u03c0/2",
         "The unit-circle x-coordinate is $0$ at the top and bottom points.",
         ["0 and \u03c0", "\u03c0/4", "2\u03c0"]),
        ("Solve $\\tan\\theta=1$ on $[0,2\\pi)$.",
         "\u03c0/4 and 5\u03c0/4",
         "Tangent has period $\\pi$; both $\\pi/4$ and $\\pi/4+\\pi$ work.",
         ["\u03c0/4 only", "\u03c0/3", "3\u03c0/4"]),
        ("How many solutions does $\\sin\\theta=2$ have in the reals?",
         0,
         "Sine never exceeds $1$ in absolute value.",
         ["2", "infinitely many", "1"]),
        ("Solve $2\\cos\\theta-1=0$ on $[0,2\\pi)$.",
         "\u03c0/3 and 5\u03c0/3",
         "$\\cos\\theta=1/2$, quadrants I and IV.",
         ["\u03c0/3 only", "2\u03c0/3 and 4\u03c0/3", "0"]),
        ("The range of $y=\\arcsin x$ is:",
         "[-\u03c0/2, \u03c0/2]",
         "Inverse sine uses the right half of the unit circle, from south to north via the east.",
         ["[0,\u03c0]", "all reals", "[0,2\u03c0]"]),
        ("$\\arcsin(1/2)$ equals:",
         "\u03c0/6",
         "The unique angle in $[-\\pi/2,\\pi/2]$ with sine $1/2$ is $\\pi/6$.",
         ["5\u03c0/6", "\u03c0/3", "30"]),
        ("$\\arccos(-1)$ equals:",
         "\u03c0",
         "Inverse cosine range is $[0,\\pi]$; cosine is $-1$ at $\\pi$.",
         ["0", "-\u03c0", "3\u03c0/2"]),
        ("$\\arctan(1)$ equals:",
         "\u03c0/4",
         "Tangent of $\\pi/4$ is $1$, and $\\pi/4$ lies in $(-\\pi/2,\\pi/2)$.",
         ["3\u03c0/4", "\u03c0/2", "1"]),
        ("$\\arcsin(\\sin(3\\pi/2))$ equals:",
         "-\u03c0/2",
         "$\\sin(3\\pi/2)=-1$, and $\\arcsin(-1)=-\\pi/2$, not $3\\pi/2$.",
         ["3\u03c0/2", "\u03c0/2", "0"]),
        ("A tide model $h=4+3\\sin\\left(\\dfrac{\\pi}{6}t\\right)$ has midline:",
         4,
         "The vertical shift $D=4$ is the midline (average height).",
         ["3", "6", "\u03c0/6"]),
        ("That same tide model has amplitude:",
         3,
         "$|A|=3$ is the distance from midline to crest.",
         ["4", "7", "6"]),
        ("Period of $h=4+3\\sin(\\pi t/6)$ is:",
         12,
         "$2\\pi/|B|=2\\pi/(\\pi/6)=12$ time units.",
         ["6", "2\u03c0", "\u03c0/6"]),
        ("A Ferris wheel height $h=10-8\\cos\\left(\\dfrac{\\pi}{16}t\\right)$ starts (at $t=0$) at height:",
         2,
         "$h(0)=10-8(1)=2$, the boarding platform.",
         ["10", "18", "8"]),
        ("Maximum of $h=5+2\\sin(3t)$ is:",
         7,
         "Midline plus amplitude: $5+2=7$.",
         ["5", "2", "3"]),
        ("$\\sin\\dfrac{\\pi}{6}$ equals:",
         "1/2",
         "The $30^\\circ$ y-coordinate on the unit circle.",
         ["\\sqrt{3}/2", "\\sqrt{2}/2", "1"]),
        ("$\\sec\\theta$ is the reciprocal of:",
         "cos \u03b8",
         "$\\sec=1/\\cos$, undefined where cosine is zero.",
         ["sin \u03b8", "tan \u03b8", "cot \u03b8"]),
        ("A cosine graph shifted right by $\\pi/2$ matches:",
         "a sine graph (standard phase)",
         "$\\cos(x-\\pi/2)=\\sin x$.",
         ["a tangent graph", "y=1", "a constant"]),
        ("$\\sin(-\\theta)$ equals:",
         "-sin \u03b8",
         "Sine is odd.",
         ["sin \u03b8", "cos \u03b8", "1"]),
        ("$\\cos(-\\theta)$ equals:",
         "cos \u03b8",
         "Cosine is even.",
         ["-cos \u03b8", "sin \u03b8", "0"]),
        ("The general solution of $\\sin\\theta=0$ is:",
         "\u03b8 = n\u03c0",
         "Sine vanishes at integer multiples of $\\pi$.",
         ["\u03b8 = n\u03c0/2", "\u03b8 = 2n\u03c0 only", "no solutions"]),
        ("$\\tan\\theta\\sin\\theta=0$ on $(0,2\\pi)$ includes $\\theta=$:",
         "\u03c0",
         "Either $\\sin\\theta=0$ or $\\tan\\theta=0$. In the open interval $(0,2\\pi)$, both happen at $\\theta=\\pi$ (and $\\tan$ is undefined at $\\pi/2,3\\pi/2$, which are not zeros).",
         ["\u03c0/2", "3\u03c0/2", "2\u03c0"]),
        ("$\\arccos(1/2)$ equals:",
         "\u03c0/3",
         "Range $[0,\\pi]$; cosine $1/2$ at $60^\\circ=\\pi/3$.",
         ["5\u03c0/3", "\u03c0/6", "-\u03c0/3"]),
        ("Amplitude of $y=-4\\sin x$ is:",
         4,
         "Amplitude is the absolute value $|-4|=4$; the sign is a reflection.",
         ["-4", "0", "1"]),
        ("$1+\\cot^2\\theta$ equals:",
         "csc^2 \u03b8",
         "The third Pythagorean identity, from dividing $1=\\sin^2+\\cos^2$ by $\\sin^2$.",
         ["sec^2 \u03b8", "tan^2 \u03b8", "1"]),
        ("If $\\sin\\theta=3/5$ in quadrant I, then $\\cos\\theta=$:",
         "4/5",
         "A $3$-$4$-$5$ right triangle; cosine is adjacent over hypotenuse.",
         ["3/5", "5/3", "3/4"]),
        ("The midline of $y=2-5\\cos(4x)$ is:",
         "y=2",
         "Vertical shift $D=2$.",
         ["y=-5", "y=4", "y=0"]),
        ("$\\sin(2\\cdot\\pi/6)$ equals:",
         "\\sqrt{3}/2",
         "$2\\cdot\\pi/6=\\pi/3$, and $\\sin(\\pi/3)=\\sqrt{3}/2$. Double-angle: $2(\\frac12)(\\frac{\\sqrt{3}}{2})=\\sqrt{3}/2$.",
         ["1/2", "1", "0"]),
        ("Domain of $y=\\arcsin x$ is:",
         "[-1,1]",
         "Sine only outputs $[-1,1]$, so inverse sine only accepts that interval.",
         ["all reals", "[0,\u03c0]", "[-2,2]"]),
        ("A cycle of $y=\\sin(Bx)$ finishes when $Bx=2\\pi$, so the period is:",
         "2\u03c0/|B|",
         "Solve $B\\cdot T=2\\pi$ for $T$.",
         ["2\u03c0 B", "|B|", "2\u03c0+|B|"]),
        ("SAT Stretch: Solve $2\\sin\\theta\\cos\\theta=\\dfrac{\\sqrt{3}}{2}$ on $[0,2\\pi)$.",
         "\u03c0/6, \u03c0/3, 7\u03c0/6, 4\u03c0/3",
         "$\\sin(2\\theta)=\\sqrt{3}/2$ and $2\\theta\\in[0,4\\pi)$, so $2\\theta=\\pi/3,2\\pi/3,7\\pi/3,8\\pi/3$. "
         "Divide by $2$: $\\theta=\\pi/6,\\pi/3,7\\pi/6,4\\pi/3$.",
         ["\u03c0/6 and 5\u03c0/6 only", "\u03c0/3 only", "0"]),
        ("SAT Stretch: If $\\cos\\theta=-3/5$ and $\\theta$ is in quadrant III, $\\tan\\theta=$:",
         "4/3",
         "Then $\\sin\\theta=-4/5$ (3-4-5, both negative in III), so $\\tan=\\sin/\\cos=(-4/5)/(-3/5)=4/3$.",
         ["-4/3", "3/4", "-3/4"]),
        ("SAT Stretch: $\\arcsin x+\\arccos x$ equals:",
         "\u03c0/2",
         "The two inverse ranges add to a right angle: cofunction identity for inverse sine and cosine.",
         ["0", "\u03c0", "x"]),
        ("SAT Stretch: Solve $\\cos(2\\theta)=\\cos\\theta$ on $[0,2\\pi)$.",
         "0, 2\u03c0/3, 4\u03c0/3",
         "$2\\cos^2\\theta-1=\\cos\\theta$, $2u^2-u-1=0$, $(2u+1)(u-1)=0$, $u=1$ or $u=-1/2$. "
         "$\\cos\\theta=1$ gives $\\theta=0$ on the half-open interval $[0,2\\pi)$ ($2\\pi$ is excluded). "
         "$\\cos\\theta=-1/2$ gives $2\\pi/3$ and $4\\pi/3$.",
         ["0, 2\u03c0/3, 4\u03c0/3, 2\u03c0", "0 only", "\u03c0"]),
        ("SAT Stretch: A sine model has max $18$, min $2$, and period $10$. One equation is:",
         "h=10+8 sin(\u03c0 t/5)",
         "Midline $10$, amplitude $8$, $B=2\\pi/10=\\pi/5$.",
         ["h=18 sin(\u03c0 t/5)", "h=8+10 sin(10t)", "h=10+8 sin(10t)"]),
        ("SAT Stretch: $\\tan\\theta+\\cot\\theta$ in terms of $\\sin$ and $\\cos$ simplifies to:",
         "1/(sin \u03b8 cos \u03b8)",
         "$\\dfrac{\\sin}{\\cos}+\\dfrac{\\cos}{\\sin}=\\dfrac{\\sin^2+\\cos^2}{\\sin\\cos}=\\dfrac{1}{\\sin\\cos}$.",
         ["1", "sin \u03b8 + cos \u03b8", "tan 2\u03b8"]),
        ("SAT Stretch: The inverse of $f(x)=2\\sin(x/3)$ near $0$ satisfies $f^{-1}(1)=$:",
         "3 arcsin(1/2)",
         "Solve $2\\sin(x/3)=1$, $\\sin(x/3)=1/2$, $x/3=\\arcsin(1/2)$, $x=3\\pi/6=\\pi/2$. "
         "As an expression: $3\\arcsin(1/2)=3\\cdot\\pi/6=\\pi/2$.",
         ["arcsin(1/2)/2", "2 arcsin 1", "3"]),
        ("SAT Stretch: How many solutions does $\\sin(3\\theta)=1/2$ have in $[0,2\\pi)$?",
         6,
         "$3\\theta$ covers $[0,6\\pi)$, three full sine periods, two solutions each, total $6$.",
         ["2", "3", "1"]),
        ("SAT Stretch: $1-2\\sin^2(5x)$ is identical to:",
         "cos(10x)",
         "The double-angle form $1-2\\sin^2 u=\\cos(2u)$ with $u=5x$.",
         ["sin(10x)", "cos(5x)", "1-sin(10x)"]),
        ("SAT Stretch: A boarding height $h=12-12\\cos(\\omega t)$ has its first maximum at $t=\\pi/\\omega$ because:",
         "cos(\u03c9 t)=-1 first at \u03c9 t=\u03c0",
         "Height is max when $-\\cos$ is max, i.e. when $\\cos=-1$. The first positive time is $\\omega t=\\pi$.",
         ["sin is 1 at t=0", "the period is \u03c0", "12-12=0"]),
    ])
    return qs[:55]


def build_unit4():
    title = "Precalculus Unit 4: Trigonometry for Precalculus"
    description = (
        "Unit-circle fluency, graphs of all six trig functions, a compact identity toolkit, "
        "trig equations, inverse trig, and sine models — with the circle and the actual waves drawn."
    )
    concepts = [
        "Unit circle fluency",
        "Graph all six",
        "Identities toolkit",
        "Trig equations",
        "Inverse trig",
        "Modeling with sine",
    ]

    sine = sample_curve(lambda x: math.sin(x), -2 * math.pi, 2 * math.pi)
    cosine = sample_curve(lambda x: math.cos(x), -2 * math.pi, 2 * math.pi)
    tan_pts = sample_curve(
        lambda x: math.tan(x) if abs(math.cos(x)) > 0.08 else 1e9,
        -math.pi + 0.2, math.pi - 0.2,
        skip=(-math.pi / 2, math.pi / 2),
    )

    c1 = concept_block(
        "1. Unit circle fluency",
        [
            "The unit circle is the circle of radius $1$ centered at the origin. An angle $\\theta$ in standard "
            "position (vertex at the origin, initial ray along the positive x-axis) meets the circle at the point "
            "$(\\cos\\theta,\\sin\\theta)$. That sentence is the definition of cosine and sine for all real $\\theta$, "
            "not just acute angles in a right triangle.",
            "The famous exact values come from $30^\\circ$-$60^\\circ$-$90^\\circ$ and $45^\\circ$-$45^\\circ$-$90^\\circ$ "
            "triangles placed on the circle. Memorize the first-quadrant table: "
            "$0,\\pi/6,\\pi/4,\\pi/3,\\pi/2$ with cosines $1,\\sqrt{3}/2,\\sqrt{2}/2,1/2,0$ and sines swapped. "
            "Every other quadrant is those values with signs from ASTC (all, sine, tangent, cosine positive).",
            "A reference angle is the acute angle to the x-axis. For $150^\\circ=5\\pi/6$, the reference is $30^\\circ$. "
            "Then $\\sin(150^\\circ)=+1/2$ (quadrant II) and $\\cos(150^\\circ)=-\\sqrt{3}/2$. Fluency means you can "
            "do this without a calculator and without redrawing a triangle every time.",
            "Radians are the Precalculus default. $\\pi$ radians $=180^\\circ$. An arc of length $\\theta$ on the "
            "unit circle subtends $\\theta$ radians, which is why the coordinates are so clean. Convert when a "
            "problem mixes units, but think in radians when you graph.",
            "Tangent is sine over cosine, so it is undefined where $\\cos\\theta=0$, i.e. odd multiples of $\\pi/2$. "
            "The other three reciprocal functions — secant, cosecant, cotangent — are undefined where their "
            "partners are zero. The unit circle tells you those locations as geometric facts, not memorized lists.",
            "Coterminal angles differ by $2\\pi n$. They share the same point on the circle, hence the same sine "
            "and cosine. This is why trig equations have infinitely many solutions on $\\mathbb{R}$ and why a "
            "problem that asks for $[0,2\\pi)$ is asking for one lap of the circle.",
        ],
        "Every later trig skill — graphs, identities, equations, inverse trig — is reading this circle fluently. "
        "If the point $(\\cos\\theta,\\sin\\theta)$ is automatic, the rest of the unit is algebra.",
        "Name the quadrant from the signs, reduce to a reference angle, then attach $\\pm$ to a first-quadrant "
        "value. Prefer radians. If cosine is the x-coordinate, you will not mix sine and cosine under stress.",
        lesson_figure(
            unit_circle_svg(60),
            "Unit circle with the ray at $60^\\circ=\\pi/3$",
            "The marked point is $(\\cos 60^\\circ,\\sin 60^\\circ)=(1/2,\\sqrt{3}/2)$. Cosine is x; sine is y.",
        )
        + solved(
            1, "Find $\\cos\\dfrac{\\pi}{3}$ and $\\sin\\dfrac{\\pi}{3}$.",
            ["$\\pi/3=60^\\circ$, a first-quadrant exact angle.",
             "The point is $(1/2,\\sqrt{3}/2)$.",
             "Cosine $1/2$, sine $\\sqrt{3}/2$."],
            "$\\cos=1/2$, $\\sin=\\sqrt{3}/2$", "", "Easy",
        )
        + solved(
            2, "Find $\\sin\\dfrac{3\\pi}{2}$.",
            ["$3\\pi/2$ is the bottom of the circle, the point $(0,-1)$.",
             "Sine is the y-coordinate $-1$.",
             "Cosine is $0$ there, so tangent is undefined."],
            "$-1$", "", "Medium",
        )
        + solved(
            3, "Find $\\cos 150^\\circ$ using a reference angle.",
            ["$150^\\circ$ is in quadrant II; reference $180^\\circ-150^\\circ=30^\\circ$.",
             "Cosine is negative in II.",
             "$\\cos 30^\\circ=\\sqrt{3}/2$, so $\\cos 150^\\circ=-\\sqrt{3}/2$."],
            "$-\\sqrt{3}/2$", "Sine of $150^\\circ$ would be $+1/2$.", "Hard",
        ),
        ("Swapping sine and cosine because “$30^\\circ$ is the small one”",
         "At $30^\\circ=\\pi/6$, sine is the small value $1/2$ and cosine is the large $\\sqrt{3}/2$. The x-coordinate "
         "is still cosine even when it is the longer-looking coordinate. Draw the point if you hesitate."),
        ("Signs from the quadrant, values from the reference",
         "Never recompute a $45^\\circ$ triangle in quadrant III. Copy $\\sqrt{2}/2$ and attach two minus signs "
         "because both cosine and sine are negative there."),
        [
            "I can read $(\\cos\\theta,\\sin\\theta)$ on the unit circle.",
            "I can use reference angles and ASTC signs.",
            "I know where tangent is undefined.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Graph all six",
        [
            "Sine is the y-coordinate traveling around the circle, so $y=\\sin x$ starts at $0$, rises to $1$ at "
            "$\\pi/2$, returns to $0$ at $\\pi$, down to $-1$ at $3\\pi/2$, and back at $2\\pi$. Cosine is the "
            "x-coordinate: it starts at $1$ and is a sine wave shifted left by $\\pi/2$. Both have amplitude $1$ "
            "and period $2\\pi$.",
            "The general sine/cosine graph is $y=A\\sin(B(x-C))+D$ (or cosine). Amplitude $|A|$ is the distance "
            "from midline to crest. Period is $2\\pi/|B|$. Phase shift is $C$ (right if the form is $x-C$). "
            "Vertical shift $D$ is the midline. A negative $A$ reflects over the midline.",
            "Tangent has period $\\pi$, zeros at $n\\pi$, and vertical asymptotes at $\\pi/2+n\\pi$. Between "
            "asymptotes it increases through all real numbers. Cotangent is decreasing between its asymptotes "
            "at $n\\pi$, with zeros at $\\pi/2+n\\pi$.",
            "Secant is $1/\\cos$: copy a cosine wave, then invert. Where cosine is $0$, secant has vertical "
            "asymptotes. Where cosine has a max of $1$, secant has a min of $1$ (a U sitting on $y=1$). Cosecant "
            "does the same to sine, with U’s sitting on $y=1$ and inverted U’s on $y=-1$.",
            "Domain from a graph: sine and cosine are all reals; tangent excludes odd multiples of $\\pi/2$; "
            "secant the same as tangent; cosecant and cotangent exclude multiples of $\\pi$. Range: sine/cosine "
            "$[-1,1]$; tangent/cotangent all reals; secant/cosecant $(-\\infty,-1]\\cup[1,\\infty)$.",
            "Matching a graph to an equation is a Precalculus staple. Read midline, amplitude, period, and "
            "whether the graph looks like sine (through the midline going up at the “start”) or cosine (starting "
            "at a max or min). Phase shift is the remaining puzzle piece.",
        ],
        "Modeling tides, sound, and Ferris wheels in the last lesson is this lesson with a story. If you cannot "
        "read $A,B,C,D$ off a sine graph, you cannot write the model.",
        "For sine/cosine: mark midline, amplitude, and one period, then plot five landmark points. For tangent: "
        "draw the asymptotes first, then the increasing branch through the origin (or the shifted copy).",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sine), ("#dc2626", tan_pts)],
                dashes=[("v", math.pi / 2, "x=\u03c0/2")],
                xlim=(-7, 7), ylim=(-4, 4),
            ),
            "Blue $y=\\sin x$; red $y=\\tan x$ with a vertical asymptote at $x=\\pi/2$",
            "Sine is bounded and period $2\\pi$. Tangent is unbounded and period $\\pi$.",
        )
        + solved(
            4, "State the period of $y=\\sin x$ and of $y=\\tan x$.",
            ["Sine (and cosine, secant, cosecant) have period $2\\pi$.",
             "Tangent (and cotangent) have period $\\pi$.",
             "A smaller period is a faster oscillation."],
            "sine $2\\pi$, tangent $\\pi$", "", "Easy",
        )
        + solved(
            5, "For $y=3\\cos(2x)$, find amplitude and period.",
            ["Amplitude $|3|=3$.",
             "Period $2\\pi/|2|=\\pi$.",
             "No vertical shift, so the midline is $y=0$."],
            "amp $3$, period $\\pi$", "", "Medium",
        )
        + solved(
            6, "Where does $y=\\csc x$ have vertical asymptotes, and why?",
            ["$\\csc x=1/\\sin x$.",
             "Undefined where $\\sin x=0$, i.e. $x=n\\pi$.",
             "Those are the same vertical lines as the zeros of sine, now blown up to infinity."],
            "at $x=n\\pi$", "Between them, cosecant has U-shaped branches sitting on $\\pm1$.", "Hard",
        ),
        ("Using $2\\pi$ as the period of tangent",
         "Tangent does repeat every $2\\pi$, but its fundamental period is $\\pi$. On a matching question, the "
         "correct period is the smallest positive repeat: $\\pi$ for tan/cot, $2\\pi$ for the others (unless $B$ changes it)."),
        ("Five-point skeleton",
         "For one period of sine or cosine, plot the start, the first quarter (max or min), the half (midline), "
         "the third quarter, and the end. Connect smoothly. That skeleton is enough to match any multiple-choice graph."),
        [
            "I can graph sine and cosine from $A,B,C,D$.",
            "I can draw tangent with its asymptotes.",
            "I can describe secant and cosecant as reciprocal graphs.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Identities toolkit",
        [
            "An identity is an equation true for all inputs in a common domain. The engine of Precalculus trig "
            "is a small toolkit, not an encyclopedia. Pythagorean: $\\sin^2\\theta+\\cos^2\\theta=1$, and the two "
            "cousins $1+\\tan^2=\\sec^2$ and $1+\\cot^2=\\csc^2$ obtained by dividing by $\\cos^2$ or $\\sin^2$.",
            "Reciprocal and quotient: $\\sec=1/\\cos$, $\\csc=1/\\sin$, $\\cot=1/\\tan=\\cos/\\sin$, "
            "$\\tan=\\sin/\\cos$. Even/odd: cosine even, sine and tangent odd. These let you simplify before "
            "you ever use a double-angle formula.",
            "Double-angle: $\\sin(2\\theta)=2\\sin\\theta\\cos\\theta$ and $\\cos(2\\theta)=\\cos^2\\theta-\\sin^2\\theta$ "
            "(also $2\\cos^2-1$ and $1-2\\sin^2$). The cosine versions are how you later integrate $\\cos^2$ in "
            "calculus; in Precalculus they solve equations like $\\cos(2\\theta)=\\cos\\theta$.",
            "Cofunctions: $\\sin(\\pi/2-\\theta)=\\cos\\theta$ and vice versa. On the unit circle, a complementary "
            "angle swaps the coordinates. Inverse sine plus inverse cosine of the same $x$ is $\\pi/2$, which is "
            "a stretch item in this unit.",
            "You prove an identity by transforming one side into the other (or both into a common third expression), "
            "using only these laws. A reliable start is “rewrite everything in sine and cosine.” A reliable check "
            "is to test a numeric $\\theta$ that is not a special angle — if the two sides disagree, it is not an identity.",
            "Unit 5 will add sum-to-product and polar form. Those are new identities, but they rest on the same "
            "Pythagorean and angle-addition ideas. Master the toolkit here so those later formulas feel like extensions.",
        ],
        "Identities turn a scary trig equation into a polynomial in $\\sin$ or $\\cos$, and they are how you "
        "simplify amplitude-phase forms. They are tools, not decorations.",
        "Rewrite in sine and cosine, use Pythagorean to trade $\\sin^2$ for $1-\\cos^2$ (or the reverse), and "
        "only then use a double-angle if the equation has a $2\\theta$ mixed with a $\\theta$.",
        lesson_figure(
            labeled_right_triangle(3, 4, 5, a_lab="3", b_lab="4", c_lab="5", angle_lab="\u03b8"),
            "A $3$-$4$-$5$ triangle on the unit-circle idea: $\\sin\\theta=3/5$, $\\cos\\theta=4/5$",
            "Pythagorean theorem $3^2+4^2=5^2$ is $\\sin^2+\\cos^2=1$ after dividing by $5^2$.",
        )
        + solved(
            7, "Simplify $\\sin^2\\theta+\\cos^2\\theta$.",
            ["This is the primary Pythagorean identity.",
             "On the unit circle it is $x^2+y^2=1$.",
             "The simplified value is $1$ (where both functions are defined)."],
            "$1$", "", "Easy",
        )
        + solved(
            8, "Show that $1+\\tan^2\\theta=\\sec^2\\theta$.",
            ["Start from $\\sin^2+\\cos^2=1$.",
             "Divide by $\\cos^2\\theta$: $\\tan^2\\theta+1=\\sec^2\\theta$.",
             "This holds wherever $\\cos\\theta\\neq0$."],
            "$1+\\tan^2=\\sec^2$", "", "Medium",
        )
        + solved(
            9, "Rewrite $\\sin(2\\theta)$ and use it to evaluate $\\sin(\\pi/3)$ another way from $\\pi/6$.",
            ["$\\sin(2\\theta)=2\\sin\\theta\\cos\\theta$.",
             "Let $\\theta=\\pi/6$: $2\\cdot(1/2)\\cdot(\\sqrt{3}/2)=\\sqrt{3}/2$.",
             "That matches $\\sin(\\pi/3)$."],
            "$\\sqrt{3}/2$", "Double-angle is a bridge between related angles.", "Hard",
        ),
        ("Cancelling $\\sin\\theta$ from both sides without noting $\\sin\\theta=0$",
         "If you divide an equation by $\\sin\\theta$, you may lose solutions where sine is zero. Move everything "
         "to one side and factor instead, the same warning as in rational equations."),
        ("Sine and cosine first",
         "When an identity is cluttered with sec/csc/tan, translate to sin/cos, combine over a common denominator, "
         "and look for $1-\\sin^2$ or $1-\\cos^2$."),
        [
            "I can use the Pythagorean identities.",
            "I can expand $\\sin(2\\theta)$ and $\\cos(2\\theta)$.",
            "I can rewrite reciprocal functions in sine and cosine.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Trig equations",
        [
            "Solving a trig equation on $[0,2\\pi)$ means finding every angle on one lap of the circle that "
            "satisfies the equation. Isolate a single trig function when you can, find the reference angle, then "
            "list every quadrant (or every period) that matches the sign.",
            "Linear examples: $\\sin\\theta=1/2$ gives $\\theta=\\pi/6$ and $5\\pi/6$. $\\cos\\theta=0$ gives "
            "$\\pi/2$ and $3\\pi/2$. $\\tan\\theta=1$ gives $\\pi/4$ and $5\\pi/4$ because tangent’s period is $\\pi$. "
            "If the right-hand side is outside $[-1,1]$ for sine or cosine, there is no solution.",
            "When a multiple angle appears, solve for the inner angle first, then divide. $\\sin(3\\theta)=1/2$ "
            "has the $3\\theta$ solutions on $[0,6\\pi)$, which is three times as many, then divide by $3$. "
            "Count: two solutions per sine period times three periods is six solutions in $[0,2\\pi)$.",
            "Quadratic in form: $\\cos(2\\theta)=\\cos\\theta$ becomes $2\\cos^2\\theta-\\cos\\theta-1=0$ after a "
            "double-angle substitution. Factor, solve for $\\cos\\theta$, then finish as a linear trig equation. "
            "Do not divide by a trig function; factor so you keep the extra roots.",
            "General solutions on $\\mathbb{R}$ add $2\\pi n$ (or $\\pi n$ for tangent). A problem that specifies "
            "an interval wants the finite list; a problem that says “find all real solutions” wants the $n\\in\\mathbb{Z}$ form.",
            "Always check candidates in the original equation when you have squared or used an identity that "
            "might not be reversible. Inverse trig will give one solution; the circle (or the period) gives the rest.",
        ],
        "Trig equations are the algebraic payoff of the unit circle. Inverse trig in the next lesson produces "
        "one answer; this lesson produces the family.",
        "Isolate, reference angle, quadrants, then adjust for a coefficient $B$ in $\\sin(Bx)$. Factor rather "
        "than divide. Count solutions by “how many periods fit in the interval.”",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#4f46e5", sample_curve(lambda x: math.sin(x), 0, 2 * math.pi)),
                    ("#dc2626", sample_curve(lambda x: 0.5, 0, 2 * math.pi)),
                ],
                points=[(math.pi / 6, 0.5, "\u03c0/6"), (5 * math.pi / 6, 0.5, "5\u03c0/6")],
                xlim=(-0.5, 7), ylim=(-1.5, 1.5),
            ),
            "$\\sin\\theta=1/2$ on $[0,2\\pi)$: two intersections",
            "The horizontal line $y=1/2$ meets one period of sine twice, in quadrants I and II.",
        )
        + solved(
            10, "Solve $\\sin\\theta=1/2$ on $[0,2\\pi)$.",
            ["Reference $\\pi/6$, sine positive in I and II.",
             "$\\theta=\\pi/6$ and $\\theta=5\\pi/6$.",
             "No other solutions in one full period."],
            "$\\pi/6,\\ 5\\pi/6$", "", "Easy",
        )
        + solved(
            11, "Solve $2\\cos\\theta-1=0$ on $[0,2\\pi)$.",
            ["$\\cos\\theta=1/2$.",
             "Quadrants I and IV: $\\pi/3$ and $5\\pi/3$.",
             "Check: $\\cos(\\pi/3)=1/2$ and $\\cos(5\\pi/3)=1/2$."],
            "$\\pi/3,\\ 5\\pi/3$", "", "Medium",
        )
        + solved(
            12, "How many solutions does $\\sin(3\\theta)=1/2$ have in $[0,2\\pi)$?",
            ["$3\\theta$ runs through $[0,6\\pi)$, three full sine periods.",
             "Each period contributes two solutions of $\\sin=1/2$.",
             "Total $6$ solutions."],
            "6", "Divide each $3\\theta$ solution by $3$ to list them if asked.", "Hard",
        ),
        ("Reporting only the inverse-trig button’s answer",
         "$\\arcsin(1/2)=\\pi/6$ is one solution, not the full set. The circle always asks “where else does "
         "this y-coordinate occur?” For sine, look in quadrant II as well."),
        ("Period counting",
         "If the argument is $B\\theta$ and you want $\\theta\\in[0,2\\pi)$, the inner angle runs through an "
         "interval of length $2\\pi|B|$. Divide that length by the function’s period to count cycles, then "
         "multiply by solutions per cycle."),
        [
            "I can solve $\\sin\\theta=k$ and $\\cos\\theta=k$ on $[0,2\\pi)$.",
            "I can handle a multiple angle by stretching the interval.",
            "I can factor a quadratic-in-form trig equation.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Inverse trig",
        [
            "Sine, cosine, and tangent are not one-to-one on their natural domains, so we restrict them before "
            "inverting — the same Unit 1 idea that made $\\sqrt{x}$ the inverse of $x^2$ on $[0,\\infty)$. "
            "Standard ranges: $\\arcsin x\\in[-\\pi/2,\\pi/2]$, $\\arccos x\\in[0,\\pi]$, $\\arctan x\\in(-\\pi/2,\\pi/2)$.",
            "Domain of $\\arcsin$ and $\\arccos$ is $[-1,1]$; domain of $\\arctan$ is all reals. "
            "$\\arcsin(1/2)=\\pi/6$, not $5\\pi/6$, because $5\\pi/6$ is outside the inverse-sine range. "
            "$\\arccos(-1)=\\pi$, not $-\\pi$, because inverse cosine lives on $[0,\\pi]$.",
            "Composition traps: $\\arcsin(\\sin\\theta)$ is not always $\\theta$. It is the unique angle in "
            "$[-\\pi/2,\\pi/2]$ with the same sine. So $\\arcsin(\\sin(3\\pi/2))=-\\pi/2$, not $3\\pi/2$. "
            "Draw the circle, drop to the matching y-coordinate in the inverse range, and read that angle.",
            "Right-triangle evaluations: if $\\theta=\\arcsin(3/5)$, then $\\sin\\theta=3/5$ with $\\theta$ in "
            "quadrant I (since $3/5>0$). A $3$-$4$-$5$ triangle gives $\\cos\\theta=4/5$ and $\\tan\\theta=3/4$. "
            "If the original inverse produced a negative angle, put the triangle in quadrant IV.",
            "The identity $\\arcsin x+\\arccos x=\\pi/2$ for $x\\in[-1,1]$ is the cofunction relationship for "
            "inverses. It is a favorite stretch item because it looks like it needs a calculator and does not.",
            "On a test, inverse trig is often the “one particular solution” that you then expand into a general "
            "solution using the previous lesson. Keep the roles straight: inverse names one angle; the period "
            "names the family.",
        ],
        "Inverse trig is how you extract an angle from a ratio, in geometry, in parametric motion, and in calculus "
        "when you integrate $1/\\sqrt{1-x^2}$. The restricted ranges are part of the definition, not optional style.",
        "Ask: which range am I forced into? Then find the unique angle in that range with the given sine, cosine, "
        "or tangent. For compositions, evaluate the inner trig function first, then apply the inverse to that number.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: math.asin(x) if -1 <= x <= 1 else 1e9, -1, 1))],
                points=[(0.5, math.pi / 6, "arcsin(1/2)=\u03c0/6")],
                xlim=(-1.5, 1.5), ylim=(-2, 2),
            ),
            "$y=\\arcsin x$ on $[-1,1]$, range $[-\\pi/2,\\pi/2]$",
            "The output $\\pi/6$ is the unique inverse-sine angle with sine $1/2$. $5\\pi/6$ is not on this graph.",
        )
        + solved(
            13, "Evaluate $\\arcsin(1/2)$.",
            ["Need $\\sin\\theta=1/2$ with $\\theta\\in[-\\pi/2,\\pi/2]$.",
             "That angle is $\\pi/6$, not $5\\pi/6$.",
             "So $\\arcsin(1/2)=\\pi/6$."],
            "$\\pi/6$", "", "Easy",
        )
        + solved(
            14, "Evaluate $\\arccos(-1)$.",
            ["Need $\\cos\\theta=-1$ with $\\theta\\in[0,\\pi]$.",
             "That is $\\theta=\\pi$.",
             "$-\\pi$ is the wrong range."],
            "$\\pi$", "", "Medium",
        )
        + solved(
            15, "Simplify $\\arcsin(\\sin(3\\pi/2))$.",
            ["Inner: $\\sin(3\\pi/2)=-1$.",
             "Then $\\arcsin(-1)=-\\pi/2$, the unique inverse-sine angle with sine $-1$.",
             "The original $3\\pi/2$ is not in $[-\\pi/2,\\pi/2]$, so it is not returned."],
            "$-\\pi/2$", "Evaluate inside-out; do not cancel $\\arcsin\\circ\\sin$ blindly.", "Hard",
        ),
        ("Returning a quadrant-II angle from $\\arcsin$",
         "Inverse sine never outputs $5\\pi/6$. If a problem wants every angle with sine $1/2$, that is a trig "
         "equation, not a single inverse evaluation."),
        ("Inner function first",
         "For $\\arcsin(\\sin\\theta)$ or $\\tan(\\arctan x)$, compute the inner value as a number, then apply "
         "the outer inverse (or trig) using its range. Cancellation only holds on the restricted domain."),
        [
            "I know the ranges of arcsin, arccos, and arctan.",
            "I can evaluate inverse trig at exact values.",
            "I can simplify $\\arcsin(\\sin\\theta)$ by landing in the inverse range.",
        ],
        21,
    )

    tide = sample_curve(lambda t: 4 + 3 * math.sin(math.pi * t / 6), -1, 14)
    c6 = concept_block(
        "6. Modeling with sine",
        [
            "Periodic phenomena — tides, temperature over a year, a Ferris wheel’s height, sound — are modeled "
            "by $h(t)=D+A\\sin(B(t-C))$ or cosine. The four parameters have meaning: $D$ midline (average), "
            "$|A|$ amplitude (distance from average to extreme), period $2\\pi/|B|$ (time per cycle), and $C$ "
            "the phase (when the sine’s standard pattern begins).",
            "From data, midline is $(\\text{max}+\\text{min})/2$ and amplitude is $(\\text{max}-\\text{min})/2$. "
            "Period is the time from peak to peak (or the stated cycle length). Then $B=2\\pi/\\text{period}$. "
            "Whether you use sine or cosine is a phase choice: cosine is convenient when $t=0$ is a maximum.",
            "A Ferris wheel of radius $8$ whose center is $10$ off the ground and which starts at the bottom "
            "can be written $h=10-8\\cos(\\omega t)$ if $t=0$ is boarding at the bottom (because $-\\cos$ starts "
            "at $-1$, so height $10-8=2$). The first maximum occurs when $-\\cos$ is maximized, which is when "
            "$\\cos$ is minimized, i.e. $\\cos=-1$, at $\\omega t=\\pi$.",
            "Units matter. If time is in seconds and the wheel has period $32$ seconds, then $B=2\\pi/32=\\pi/16$. "
            "If a tide problem uses hours and a $12$-hour cycle, $B=2\\pi/12=\\pi/6$. Write the units next to "
            "the period before you compute $B$.",
            "Max and min are midline $\\pm$ amplitude, independent of $B$ and $C$. A question that only asks "
            "for the highest tide does not need the phase. A question that asks “when is the tide first high?” does.",
            "Sine models close the trig-for-precalculus unit by using every earlier lesson: the wave from graphs, "
            "the period formula, inverse trig to solve $h(t)=k$, and the unit circle to interpret a cosine of $-1$.",
        ],
        "If you can turn a paragraph about a wheel or a tide into $A,B,C,D$, you can model any sinusoidal SAT "
        "story and you are ready for harmonic motion in physics and calculus.",
        "Compute midline and amplitude from max/min. Compute $B$ from the period. Choose sine versus cosine "
        "from the starting point. Then, if asked for a time, solve using inverse trig and add periods as needed.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", tide)],
                dashes=[("h", 4, "midline 4")],
                points=[(3, 7, "crest"), (9, 1, "trough")],
                xlim=(-1, 14), ylim=(-1, 9),
            ),
            "Tide model $h=4+3\\sin(\\pi t/6)$: midline $4$, amplitude $3$, period $12$",
            "The wave oscillates between $1$ and $7$. One full cycle takes $12$ time units.",
        )
        + solved(
            16, "For $h=4+3\\sin(\\pi t/6)$, find midline, amplitude, and period.",
            ["Midline $D=4$.",
             "Amplitude $|3|=3$.",
             "Period $2\\pi/(\\pi/6)=12$."],
            "midline $4$, amp $3$, period $12$", "", "Easy",
        )
        + solved(
            17, "A Ferris wheel $h=10-8\\cos(\\pi t/16)$: find the boarding height at $t=0$.",
            ["$\\cos0=1$, so $h(0)=10-8=2$.",
             "That is center minus radius: the bottom.",
             "The top would be $10+8=18$."],
            "$2$", "", "Medium",
        )
        + solved(
            18, "A sine model has max $18$, min $2$, period $10$. Write one equation using sine with no phase shift.",
            ["Midline $(18+2)/2=10$, amplitude $(18-2)/2=8$.",
             "$B=2\\pi/10=\\pi/5$.",
             "One model is $h=10+8\\sin(\\pi t/5)$ (starts at the midline going up)."],
            "$h=10+8\\sin(\\pi t/5)$", "Cosine with a phase could match the same data.", "Hard",
        ),
        ("Using the radius as the midline",
         "On a wheel, the midline is the height of the center, not the radius. Amplitude is the radius. Mixing "
         "those two numbers swaps the whole graph vertically."),
        ("Max/min first, phase last",
         "If a question only needs the highest value, you are done after midline plus amplitude. Save inverse "
         "trig for “when” questions."),
        [
            "I can read $A$, $D$, and period from a sine model.",
            "I can write a model from max, min, and period.",
            "I can interpret $t=0$ for a Ferris-wheel cosine.",
        ],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title, AUDIENCE, concepts, body, practice_slots(31, 25, STRETCH_LABEL),
    )
    return title, description, content, _u4_questions()
