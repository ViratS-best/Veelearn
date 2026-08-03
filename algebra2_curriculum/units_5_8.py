#!/usr/bin/env python3
"""Deep Algebra 2 (grade 10) curriculum builders — Units 5-8.

Each unit: 6 concept_block sections (quiz_start 1,6,11,16,21,26; 5 questions each = 30),
plus a 50-question finale (Easy 31-45, Medium 46-60, Hard 61-70, Stretch 71-80) = 80 total.
"""

from __future__ import annotations

from .common import (
    concept_block,
    solved,
    practice_slots,
    unit_shell,
    page_break,
    mq,
    make_question,
    renumber,
    near_str,
    p,
    why_box,
    think_box,
)


def _fill80(qs):
    """Guarantee exactly 80 questions; pad defensively if a count ever drifts."""
    while len(qs) < 80:
        n = len(qs) + 1
        qs.append(mq(f"Review check {n}: simplify $\\frac{{2n}}{{4}}$ for $n=2$.", "1",
                      "Substitute and reduce: $\\frac{2(2)}{4}=\\frac{4}{4}=1$.", n,
                      distractors=["2", "4", "1/2"]))
    return renumber(qs[:80])


AUDIENCE = "Grade 10 Algebra 2"


# =====================================================================================
# UNIT 5: Rational Expressions & Equations
# =====================================================================================

def _u5_questions():
    qs = []

    # Concept 1 — Simplify rational expressions (1-5)
    qs.append(mq(
        "Simplify $\\dfrac{x^2-16}{x^2+7x+12}$ (state the reduced form).",
        "(x-4)/(x+3)",
        "Factor: $\\frac{(x-4)(x+4)}{(x+3)(x+4)}$. Cancel the common factor $(x+4)$ to get $\\frac{x-4}{x+3}$, "
        "with $x\\neq -3,-4$.",
        1, distractors=["(x-4)/(x-3)", "x-4", "(x+4)/(x+3)"]))
    qs.append(mq(
        "Simplify $\\dfrac{x^2-25}{x-5}$.",
        "x+5",
        "Factor the numerator as a difference of squares: $\\frac{(x-5)(x+5)}{x-5}=x+5$, with $x\\neq5$.",
        2, distractors=["x-5", "5", "x^2+5"]))
    qs.append(mq(
        "Simplify $\\dfrac{3x^2-12}{x^2-4x+4}$.",
        "3(x+2)/(x-2)",
        "Factor: $\\frac{3(x-2)(x+2)}{(x-2)^2}$. Cancel one $(x-2)$: $\\frac{3(x+2)}{x-2}$, with $x\\neq2$.",
        3, distractors=["3(x-2)/(x+2)", "3(x+2)", "(x+2)/(x-2)"]))
    qs.append(mq(
        "Simplify $\\dfrac{x^2+5x+6}{x^2+4x+3}$.",
        "(x+2)/(x+1)",
        "Factor: $\\frac{(x+2)(x+3)}{(x+1)(x+3)}$. Cancel $(x+3)$: $\\frac{x+2}{x+1}$, with $x\\neq-1,-3$.",
        4, distractors=["(x+2)/(x+3)", "(x+3)/(x+1)", "x+2"]))
    qs.append(mq(
        "Simplify $\\dfrac{x^3-8}{x^2-4}$.",
        "(x^2+2x+4)/(x+2)",
        "Factor the numerator as a difference of cubes: $(x-2)(x^2+2x+4)$. The denominator factors as "
        "$(x-2)(x+2)$. Cancel $(x-2)$: $\\frac{x^2+2x+4}{x+2}$, with $x\\neq2,-2$.",
        5, distractors=["(x^2-2x+4)/(x+2)", "x^2+2x+4", "(x-2)/(x+2)"]))

    # Concept 2 — Multiply / divide rationals (6-10)
    qs.append(mq(
        "Multiply $\\dfrac{x^2-4}{x+5}\\cdot\\dfrac{x+5}{x+2}$.",
        "x-2",
        "The factor $(x+5)$ cancels directly: $\\frac{(x-2)(x+2)}{x+5}\\cdot\\frac{x+5}{x+2}=x-2$, with "
        "$x\\neq-5,-2$.",
        6, distractors=["x+2", "x-5", "(x-2)(x+2)"]))
    qs.append(mq(
        "Multiply $\\dfrac{x+3}{x^2-9}\\cdot(x-3)$.",
        "1",
        "Rewrite $\\frac{x+3}{(x-3)(x+3)}=\\frac{1}{x-3}$, then multiply by $(x-3)$ to get $1$, with "
        "$x\\neq3,-3$.",
        7, distractors=["x-3", "x+3", "0"]))
    qs.append(mq(
        "Divide $\\dfrac{x^2-1}{x+2}\\div\\dfrac{x+1}{x+2}$.",
        "x-1",
        "Multiply by the reciprocal: $\\frac{(x-1)(x+1)}{x+2}\\cdot\\frac{x+2}{x+1}=x-1$, with "
        "$x\\neq-2,-1$.",
        8, distractors=["x+1", "(x-1)(x+2)", "1"]))
    qs.append(mq(
        "Multiply $\\dfrac{3x}{x-4}\\cdot\\dfrac{x-4}{6}$.",
        "x/2",
        "The factor $(x-4)$ cancels: $\\frac{3x}{6}=\\frac{x}{2}$, with $x\\neq4$.",
        9, distractors=["3x/6", "2x", "x/6"]))
    qs.append(mq(
        "Divide $\\dfrac{x^2-16}{x}\\div\\dfrac{x-4}{3x}$.",
        "3(x+4)",
        "Multiply by the reciprocal: $\\frac{(x-4)(x+4)}{x}\\cdot\\frac{3x}{x-4}=3(x+4)$, with $x\\neq0,4$.",
        10, distractors=["3(x-4)", "(x+4)/3", "3x+4"]))

    # Concept 3 — Add / subtract rationals with LCD (11-15)
    qs.append(mq(
        "Add $\\dfrac{1}{x}+\\dfrac{2}{x}$.",
        "3/x",
        "Same denominator, so combine numerators directly: $\\frac{1+2}{x}=\\frac{3}{x}$.",
        11, distractors=["3/(2x)", "2/x", "3/x^2"]))
    qs.append(mq(
        "Add $\\dfrac{2}{x-1}+\\dfrac{3}{x+1}$.",
        "(5x-1)/(x^2-1)",
        "LCD is $(x-1)(x+1)$: $\\frac{2(x+1)+3(x-1)}{(x-1)(x+1)}=\\frac{2x+2+3x-3}{x^2-1}=\\frac{5x-1}{x^2-1}$.",
        12, distractors=["5x/(x^2-1)", "(5x+1)/(x^2-1)", "5/(x^2-1)"]))
    qs.append(mq(
        "Subtract $\\dfrac{5}{x+3}-\\dfrac{1}{x-3}$.",
        "(4x-18)/(x^2-9)",
        "LCD is $(x+3)(x-3)$: $\\frac{5(x-3)-(x+3)}{x^2-9}=\\frac{5x-15-x-3}{x^2-9}=\\frac{4x-18}{x^2-9}$.",
        13, distractors=["(4x-12)/(x^2-9)", "4/(x^2-9)", "(6x-18)/(x^2-9)"]))
    qs.append(mq(
        "Add $\\dfrac{x}{x-2}+1$.",
        "2(x-1)/(x-2)",
        "Write $1=\\frac{x-2}{x-2}$, so the sum is $\\frac{x+x-2}{x-2}=\\frac{2x-2}{x-2}=\\frac{2(x-1)}{x-2}$.",
        14, distractors=["(x-1)/(x-2)", "x-1", "2x/(x-2)"]))
    qs.append(mq(
        "Add $\\dfrac{1}{x^2-4}+\\dfrac{1}{x-2}$.",
        "(x+3)/(x^2-4)",
        "Rewrite over the LCD $(x-2)(x+2)$: $\\frac{1+(x+2)}{(x-2)(x+2)}=\\frac{x+3}{x^2-4}$, with $x\\neq2,-2$.",
        15, distractors=["(x+1)/(x^2-4)", "1/(x-2)", "(x+3)/(x-2)"]))

    # Concept 4 — Complex fractions (16-20)
    qs.append(mq(
        "Simplify $\\dfrac{3/x}{9/x^2}$.",
        "x/3",
        "Multiply by the reciprocal: $\\frac{3}{x}\\cdot\\frac{x^2}{9}=\\frac{3x^2}{9x}=\\frac{x}{3}$, with $x\\neq0$.",
        16, distractors=["3/x", "x/9", "3x"]))
    qs.append(mq(
        "Simplify $\\dfrac{1/2+1/x}{1/2-1/x}$.",
        "(x+2)/(x-2)",
        "Multiply top and bottom by the LCD $2x$: $\\frac{(x+2)}{(x-2)}$, with $x\\neq0,2$.",
        17, distractors=["(x-2)/(x+2)", "(2+x)/(2-x)", "2/x"]))
    qs.append(mq(
        "Simplify $\\dfrac{1/x-1/2}{1/x+1/2}$.",
        "(2-x)/(2+x)",
        "Multiply top and bottom by $2x$: $\\frac{2-x}{2+x}$, with $x\\neq0,-2$.",
        18, distractors=["(x-2)/(x+2)", "(2+x)/(2-x)", "-1"]))
    qs.append(mq(
        "Simplify $\\dfrac{x/(x+1)}{x^2/(x+1)^2}$.",
        "(x+1)/x",
        "Multiply by the reciprocal: $\\frac{x}{x+1}\\cdot\\frac{(x+1)^2}{x^2}=\\frac{x+1}{x}$, with $x\\neq0,-1$.",
        19, distractors=["x/(x+1)", "(x+1)^2/x", "1/x"]))
    qs.append(mq(
        "Simplify $\\dfrac{1+1/x}{1-1/x}$.",
        "(x+1)/(x-1)",
        "Multiply top and bottom by $x$: $\\frac{x+1}{x-1}$, with $x\\neq0,1$.",
        20, distractors=["(x-1)/(x+1)", "x+1", "1/(x-1)"]))

    # Concept 5 — Solve rational equations + extraneous solutions (21-25)
    qs.append(mq(
        "Solve $\\dfrac{3}{x}=\\dfrac{6}{x+1}$.",
        "x=1",
        "Cross multiply: $3(x+1)=6x \\Rightarrow 3x+3=6x \\Rightarrow 3=3x \\Rightarrow x=1$. Check the domain "
        "($x\\neq0,-1$): valid.",
        21, distractors=["x=2", "x=-1", "x=3"]))
    qs.append(mq(
        "Solve $\\dfrac{x}{x-3}=\\dfrac{3}{x-3}+2$.",
        "No solution (x=3 is extraneous)",
        "Multiply by $(x-3)$: $x=3+2(x-3)=2x-3 \\Rightarrow -x=-3 \\Rightarrow x=3$. Since $x=3$ makes the "
        "original denominator zero, it must be rejected — there is no valid solution.",
        22, distractors=["x=3", "x=0", "x=-3"]))
    qs.append(mq(
        "Solve $\\dfrac{1}{x-2}+\\dfrac{1}{x+2}=\\dfrac{4}{x^2-4}$.",
        "No solution (x=2 is extraneous)",
        "Multiply every term by $(x-2)(x+2)$: $(x+2)+(x-2)=4 \\Rightarrow 2x=4 \\Rightarrow x=2$. This value "
        "makes the original denominators zero, so it is rejected.",
        23, distractors=["x=2", "x=4", "x=-2"]))
    qs.append(mq(
        "Solve $\\dfrac{5}{x}-1=\\dfrac{4}{x}$.",
        "x=1",
        "Multiply by $x$: $5-x=4 \\Rightarrow x=1$. Check the domain ($x\\neq0$): valid.",
        24, distractors=["x=5", "x=4", "x=-1"]))
    qs.append(mq(
        "Solve $\\dfrac{2x}{x+1}=1+\\dfrac{1}{x+1}$.",
        "x=2",
        "Multiply by $(x+1)$: $2x=(x+1)+1=x+2 \\Rightarrow x=2$. Check the domain ($x\\neq-1$): valid.",
        25, distractors=["x=1", "x=-2", "x=0"]))

    # Concept 6 — Applications: work rate, similar triangles (26-30)
    qs.append(mq(
        "Pipe A fills a pool in 3 hours; pipe B fills it in 6 hours. Working together, how many hours "
        "does it take to fill the pool?",
        "2",
        "Add rates: $\\frac{1}{3}+\\frac{1}{6}=\\frac{2}{6}+\\frac{1}{6}=\\frac{3}{6}=\\frac{1}{2}$ pool per "
        "hour, so the time is $2$ hours.",
        26))
    qs.append(mq(
        "Two triangles are similar with $\\dfrac{x}{4}=\\dfrac{9}{6}$. Find $x$.",
        "6",
        "Cross multiply: $6x=36 \\Rightarrow x=6$.",
        27))
    qs.append(mq(
        "Painter A can paint a room in 4 hours; painter B can paint it in 12 hours. Working together, how "
        "many hours does it take?",
        "3",
        "Add rates: $\\frac{1}{4}+\\frac{1}{12}=\\frac{3}{12}+\\frac{1}{12}=\\frac{4}{12}=\\frac{1}{3}$ per "
        "hour, so the time is $3$ hours.",
        28))
    qs.append(mq(
        "Similar triangles give the proportion $\\dfrac{x+2}{5}=\\dfrac{8}{10}$. Find $x$.",
        "2",
        "Cross multiply: $10(x+2)=40 \\Rightarrow x+2=4 \\Rightarrow x=2$.",
        29))
    qs.append(mq(
        "Two workers finish a job together in 6 hours. The faster worker alone takes $x$ hours and the "
        "slower worker alone takes $2x$ hours. Find $x$.",
        "9",
        "Add rates: $\\frac{1}{x}+\\frac{1}{2x}=\\frac{1}{6}$. Combine the left side: "
        "$\\frac{2+1}{2x}=\\frac{3}{2x}=\\frac{1}{6}$, so $2x=18 \\Rightarrow x=9$.",
        30))

    finale = []

    # Easy 31-45
    for a in (1, 2, 3, 4, 5):
        finale.append(mq(
            f"Simplify $\\dfrac{{x^2-{a*a}}}{{x-{a}}}$.",
            f"x+{a}",
            f"Difference of squares: $\\frac{{(x-{a})(x+{a})}}{{x-{a}}}=x+{a}$, with $x\\neq{a}$.",
            0, distractors=[f"x-{a}", str(a), f"x+{a+3}"]))
    for n, m in [(2, 6), (4, 8), (3, 12), (6, 9), (5, 15)]:
        from math import gcd
        g = gcd(n, m)
        rn, rm = n // g, m // g
        finale.append(mq(
            f"Multiply $\\dfrac{{{n}}}{{x}}\\cdot\\dfrac{{x}}{{{m}}}$ and reduce (state the numeric result).",
            f"{rn}/{rm}",
            f"The $x$'s cancel, leaving $\\frac{{{n}}}{{{m}}}$, which reduces to $\\frac{{{rn}}}{{{rm}}}$.",
            0, distractors=[f"{n}/{m}", f"{rm}/{rn}", f"{n+m}"]))
    for aa, bb in [(1, 2), (2, 3), (1, 4), (3, 5), (2, 7)]:
        finale.append(mq(
            f"Add $\\dfrac{{{aa}}}{{x}}+\\dfrac{{{bb}}}{{x}}$.",
            f"{aa+bb}/x",
            f"Same denominator: $\\frac{{{aa}+{bb}}}{{x}}=\\frac{{{aa+bb}}}{{x}}$.",
            0, distractors=[f"{aa+bb}/(2x)", f"{aa*bb}/x", f"{abs(aa-bb)}/x"]))

    # Medium 46-60
    for a, b in [(2, 3), (1, 4), (3, 5), (2, 6), (4, 7)]:
        finale.append(mq(
            f"Simplify $\\dfrac{{x^2-{a+b}x+{a*b}}}{{x-{a}}}$.",
            f"x-{b}",
            f"Factor the numerator: $(x-{a})(x-{b})$. Cancel $(x-{a})$ to get $x-{b}$, with $x\\neq{a}$.",
            0, distractors=[f"x+{b}", f"x-{a}", f"x-{a+b}"]))
    for a in (1, 2, 3, 4, 5):
        finale.append(mq(
            f"Add $\\dfrac{{1}}{{x-{a}}}+\\dfrac{{1}}{{x+{a}}}$.",
            f"2x/(x^2-{a*a})",
            f"LCD is $(x-{a})(x+{a})$: $\\frac{{(x+{a})+(x-{a})}}{{x^2-{a*a}}}=\\frac{{2x}}{{x^2-{a*a}}}$.",
            0, distractors=[f"2/(x^2-{a*a})", f"2x/(x-{a})", f"x/(x^2-{a*a})"]))
    for text, ans, expl, dis in [
        ("Solve $\\dfrac{4}{x}=\\dfrac{2}{x+1}$.", "x=-2",
         "Cross multiply: $4(x+1)=2x \\Rightarrow 4x+4=2x \\Rightarrow 2x=-4 \\Rightarrow x=-2$.",
         ["x=2", "x=-1", "x=4"]),
        ("Solve $\\dfrac{3}{x}=\\dfrac{9}{x+2}$.", "x=1",
         "Cross multiply: $3(x+2)=9x \\Rightarrow 3x+6=9x \\Rightarrow 6x=6 \\Rightarrow x=1$.",
         ["x=2", "x=-1", "x=3"]),
        ("Solve $\\dfrac{5}{x-1}=\\dfrac{10}{x+1}$.", "x=3",
         "Cross multiply: $5(x+1)=10(x-1) \\Rightarrow 5x+5=10x-10 \\Rightarrow 15=5x \\Rightarrow x=3$.",
         ["x=1", "x=5", "x=-3"]),
        ("Solve $\\dfrac{2}{x+3}=\\dfrac{6}{x+5}$.", "x=-2",
         "Cross multiply: $2(x+5)=6(x+3) \\Rightarrow 2x+10=6x+18 \\Rightarrow -8=4x \\Rightarrow x=-2$.",
         ["x=2", "x=-4", "x=1"]),
        ("Solve $\\dfrac{6}{x}=\\dfrac{3}{x-3}$.", "x=6",
         "Cross multiply: $6(x-3)=3x \\Rightarrow 6x-18=3x \\Rightarrow 3x=18 \\Rightarrow x=6$.",
         ["x=3", "x=-6", "x=9"]),
    ]:
        finale.append(mq(text, ans, expl, 0, distractors=dis))

    # Hard 61-70
    for text, ans, expl, dis in [
        ("Simplify $\\dfrac{x^3-8}{x^2-2x}$.", "(x^2+2x+4)/x",
         "Factor the numerator (difference of cubes) as $(x-2)(x^2+2x+4)$ and the denominator as $x(x-2)$. "
         "Cancel $(x-2)$: $\\frac{x^2+2x+4}{x}$, with $x\\neq0,2$.",
         ["(x^2-2x+4)/x", "x^2+2x+4", "(x+2)/x"]),
        ("Solve $\\dfrac{x}{x-4}=\\dfrac{4}{x-4}+3$.", "No solution (x=4 is extraneous)",
         "Multiply by $(x-4)$: $x=4+3(x-4)=3x-8 \\Rightarrow -2x=-8 \\Rightarrow x=4$, which is excluded from "
         "the domain, so there is no solution.",
         ["x=4", "x=8", "x=-4"]),
        ("Simplify $\\dfrac{1/(x-3)+1/3}{1/(x-3)-1/3}$.", "x/(6-x)",
         "Combine each level over $3(x-3)$: the top becomes $\\frac{x}{3(x-3)}$ and the bottom becomes "
         "$\\frac{6-x}{3(x-3)}$. Dividing gives $\\frac{x}{6-x}$, with $x\\neq3,6$.",
         ["x/(x-6)", "(6-x)/x", "3x/(6-x)"]),
        ("Pump A fills a tank in 6 hours; pump B fills it in 10 hours. Working together, how many hours "
         "does it take (as a decimal)?", "3.75",
         "Add rates: $\\frac{1}{6}+\\frac{1}{10}=\\frac{5}{30}+\\frac{3}{30}=\\frac{8}{30}=\\frac{4}{15}$ "
         "per hour, so the time is $\\frac{15}{4}=3.75$ hours.",
         ["4", "3.5", "8"]),
        ("Similar triangles: $\\dfrac{x}{x+4}=\\dfrac{3}{5}$. Find $x$.", "6",
         "Cross multiply: $5x=3(x+4)=3x+12 \\Rightarrow 2x=12 \\Rightarrow x=6$.",
         ["4", "8", "12"]),
        ("Solve $\\dfrac{1}{x-2}+\\dfrac{1}{x+2}=\\dfrac{6}{x^2-4}$.", "x=3",
         "Multiply by $(x-2)(x+2)$: $(x+2)+(x-2)=6 \\Rightarrow 2x=6 \\Rightarrow x=3$. Check the domain "
         "($x\\neq2,-2$): valid.",
         ["x=6", "x=2", "x=-3"]),
        ("Add $\\dfrac{3}{2x}+\\dfrac{1}{3x}$.", "11/(6x)",
         "LCD is $6x$: $\\frac{9}{6x}+\\frac{2}{6x}=\\frac{11}{6x}$.",
         ["4/(5x)", "11/(5x)", "9/(6x)"]),
        ("Divide $\\dfrac{x^2-1}{x^2-4}\\div\\dfrac{x+1}{x-2}$.", "(x-1)/(x+2)",
         "Multiply by the reciprocal: $\\frac{(x-1)(x+1)}{(x-2)(x+2)}\\cdot\\frac{x-2}{x+1}=\\frac{x-1}{x+2}$, "
         "with $x\\neq2,-2,-1$.",
         ["(x+1)/(x+2)", "(x-1)/(x-2)", "x-1"]),
        ("Solve $\\dfrac{x}{x-1}=\\dfrac{x+2}{x+1}$.", "No solution",
         "Cross multiply: $x(x+1)=(x+2)(x-1) \\Rightarrow x^2+x=x^2+x-2 \\Rightarrow 0=-2$, which is never "
         "true, so there is no solution for any $x$.",
         ["x=1", "x=-1", "x=2"]),
        ("A map uses the scale 2 cm : 5 miles. Two cities are $x$ cm apart on the map and 45 miles apart "
         "in reality. Find $x$.", "18",
         "Set up the proportion $\\frac{2}{5}=\\frac{x}{45}$. Cross multiply: $5x=90 \\Rightarrow x=18$.",
         ["20", "16", "22"]),
    ]:
        finale.append(mq(text, ans, expl, 0, distractors=dis))

    # Stretch 71-80
    for text, ans, expl, dis in [
        ("Simplify $\\dfrac{x^2-5x+6}{x^2-9}\\cdot\\dfrac{x+3}{x-2}$.", "1",
         "Factor everything: $\\frac{(x-2)(x-3)}{(x-3)(x+3)}\\cdot\\frac{x+3}{x-2}$. Every factor cancels, "
         "leaving $1$, with $x\\neq3,-3,2$.",
         ["x-2", "x+3", "0"]),
        ("Solve $\\dfrac{2}{x-3}-\\dfrac{3}{x+3}=\\dfrac{12}{x^2-9}$.", "No solution (x=3 is extraneous)",
         "Multiply by $(x-3)(x+3)$: $2(x+3)-3(x-3)=12 \\Rightarrow 2x+6-3x+9=12 \\Rightarrow -x+15=12 "
         "\\Rightarrow x=3$, which is excluded from the domain.",
         ["x=3", "x=-3", "x=1"]),
        ("Simplify $\\dfrac{x-1/x}{1-1/x}$.", "x+1",
         "Write the top as $\\frac{x^2-1}{x}$ and the bottom as $\\frac{x-1}{x}$. Dividing gives "
         "$\\frac{x^2-1}{x-1}=x+1$, with $x\\neq0,1$.",
         ["x-1", "x^2+1", "1/(x-1)"]),
        ("A and B finish a job together in 4 hours. Alone, A takes 6 hours more than B. If B alone takes "
         "$x$ hours, find $x$.", "6",
         "Set up $\\frac{1}{x}+\\frac{1}{x+6}=\\frac{1}{4}$. Multiplying through and simplifying gives "
         "$x^2-2x-24=0$, which factors as $(x-6)(x+4)=0$, so $x=6$ (rejecting the negative root).",
         ["4", "8", "12"]),
        ("Solve $\\dfrac{x+2}{x-2}=5$.", "x=3",
         "Cross multiply: $x+2=5(x-2)=5x-10 \\Rightarrow 12=4x \\Rightarrow x=3$.",
         ["x=2", "x=4", "x=-3"]),
        ("Solve $\\dfrac{x}{x-1}-\\dfrac{2}{x+1}=1$.", "x=3",
         "Multiply by $(x-1)(x+1)$: $x(x+1)-2(x-1)=x^2-1 \\Rightarrow x^2-x+2=x^2-1 \\Rightarrow -x=-3 "
         "\\Rightarrow x=3$. Check the domain ($x\\neq1,-1$): valid.",
         ["x=1", "x=-3", "x=2"]),
        ("Similar triangles: $\\dfrac{x+1}{4}=\\dfrac{x+4}{10}$. Find $x$.", "1",
         "Cross multiply: $10(x+1)=4(x+4) \\Rightarrow 10x+10=4x+16 \\Rightarrow 6x=6 \\Rightarrow x=1$.",
         ["2", "3", "4"]),
        ("If 3 workers finish a job in 8 hours (all working at the same rate), how many hours would 4 "
         "workers need for the same job?", "6",
         "The job takes $3\\times8=24$ worker-hours total. With 4 workers, the time is "
         "$\\frac{24}{4}=6$ hours.",
         ["8", "5", "24"]),
        ("If $f(x)=\\dfrac{x^2-1}{x-1}$ for $x\\neq1$, find $f(5)$.", "6",
         "$f(x)$ simplifies to $x+1$ for $x\\neq1$, so $f(5)=6$.",
         ["4", "24", "5"]),
        ("Solve $\\dfrac{x-1}{x+1}=\\dfrac{x+1}{x-1}$.", "x=0",
         "Cross multiply: $(x-1)^2=(x+1)^2 \\Rightarrow x^2-2x+1=x^2+2x+1 \\Rightarrow -4x=0 \\Rightarrow x=0$. "
         "Check the domain ($x\\neq1,-1$): valid.",
         ["x=1", "x=-1", "No solution"]),
    ]:
        finale.append(mq(text, ans, expl, 0, distractors=dis))

    qs.extend(finale[:50])
    return _fill80(qs)


def build_unit5():
    title = "Algebra 2 Unit 5: Rational Expressions & Equations"
    description = (
        "Deep, patient coverage of rational expressions for grade 10 Algebra 2 — simplifying, multiplying, "
        "dividing, adding, subtracting, complex fractions, solving rational equations with extraneous-root "
        "checks, and real applications like work rate and similar triangles."
    )

    c1 = concept_block(
        "1. Simplifying rational expressions — factor first, cancel factors (never terms)",
        [
            "A rational expression is a fraction whose numerator and denominator are polynomials, such as "
            "$\\frac{x^2-9}{x+3}$. Every habit you already trust with numeric fractions — finding common "
            "factors, reducing to lowest terms, and never dividing by zero — carries over directly. The only "
            "difference is that the numbers on top and bottom are now expressions built from $x$.",
            "The single most important rule in this section is <strong>factor first, cancel second</strong>. "
            "You are only ever allowed to cancel a factor that multiplies the <em>entire</em> numerator and the "
            "<em>entire</em> denominator. An $x$ that appears inside a sum, like the $x$ in $x+9$, is a term, not "
            "a factor, and it cannot be crossed out even though it looks tempting.",
            "Before you cancel anything, you must record the domain restrictions. Look at the <em>original</em>, "
            "unsimplified denominator, set it equal to zero, and solve. Those excluded values travel with the "
            "simplified expression forever, even after the offending factor has disappeared from view.",
            "Factoring completely means using every tool from earlier in Algebra 2: pull out the greatest "
            "common factor first, then look for a difference of squares, a difference or sum of cubes, or a "
            "trinomial that factors into two binomials. Skipping a factoring step is the most common reason a "
            "rational expression looks unsimplified when it is graded.",
            "This skill becomes the backbone of the rest of the unit. Multiplying, dividing, adding, and solving "
            "rational equations are all much easier once simplifying is automatic, and the same factor-then-"
            "cancel logic reappears later when you study limits and holes in graphs in future math courses.",
        ],
        "Rational expressions look intimidating only because the numbers have been replaced by letters. Every "
        "reduction rule from numeric fractions is still true here — you just need to factor before you can see "
        "the common pieces to cancel.",
        "Factor the numerator completely. Factor the denominator completely. Write down every value that makes "
        "the original denominator zero. Cancel only matching factors that appear in both the top and the "
        "bottom. Rewrite the simplified expression together with its domain restriction.",
        solved(1, "Simplify $\\dfrac{x^2-9}{x^2+5x+6}$.",
               ["Factor the numerator as a difference of squares: $(x-3)(x+3)$.",
                "Factor the denominator as a trinomial: $(x+2)(x+3)$.",
                "The original denominator is zero when $x=-2$ or $x=-3$, so those values are excluded.",
                "Cancel the common factor $(x+3)$: $\\dfrac{(x-3)(x+3)}{(x+2)(x+3)}=\\dfrac{x-3}{x+2}$."],
               "$\\dfrac{x-3}{x+2}$, with $x\\neq-2,-3$", "", "Easy")
        + solved(2, "Simplify $\\dfrac{2x^2-8}{x^2-4x+4}$.",
                 ["Factor out the GCF from the numerator: $2(x^2-4)=2(x-2)(x+2)$.",
                  "Factor the denominator as a perfect square: $(x-2)^2$.",
                  "The original denominator is zero only when $x=2$, so that value is excluded.",
                  "Cancel one factor of $(x-2)$: $\\dfrac{2(x-2)(x+2)}{(x-2)^2}=\\dfrac{2(x+2)}{x-2}$."],
                 "$\\dfrac{2(x+2)}{x-2}$, with $x\\neq2$", "", "Medium")
        + solved(3, "Simplify $\\dfrac{x^3-27}{x^2-9}$.",
                 ["The numerator is a difference of cubes: $x^3-27=(x-3)(x^2+3x+9)$.",
                  "The denominator is a difference of squares: $x^2-9=(x-3)(x+3)$.",
                  "The original denominator is zero when $x=3$ or $x=-3$, so those values are excluded.",
                  "Cancel the common factor $(x-3)$: $\\dfrac{(x-3)(x^2+3x+9)}{(x-3)(x+3)}=\\dfrac{x^2+3x+9}{x+3}$.",
                  "Notice that $x^2+3x+9$ does not factor further with real integer roots, so this is the final form."],
                 "$\\dfrac{x^2+3x+9}{x+3}$, with $x\\neq3,-3$",
                 "The remaining quadratic in the numerator cannot be simplified against the linear denominator.",
                 "Hard"),
        ("Canceling terms instead of factors",
         "In $\\dfrac{x+3}{x+9}$ there is no common factor, so nothing cancels — the $x$'s are terms buried "
         "inside sums, not factors multiplying the whole numerator and denominator, and treating them as "
         "cancellable produces a wrong simplified form."),
        ("Factor completely, then cancel",
         "Factor the top and bottom all the way — greatest common factor first, then difference of squares or "
         "trinomial patterns — before you ever look for something to cancel."),
        ["I factor the numerator and denominator completely before canceling anything.",
         "I state the domain restrictions from the original denominator before simplifying.",
         "I can explain why $\\dfrac{x+3}{x+9}$ cannot be reduced by canceling the $x$'s."],
        1,
    )

    c2 = concept_block(
        "2. Multiplying and dividing rational expressions",
        [
            "Multiplying rational expressions works exactly like multiplying numeric fractions: multiply the "
            "numerators together, multiply the denominators together, and simplify. The one extra step in "
            "Algebra 2 is that every numerator and denominator must be factored first, because most of the "
            "canceling opportunities are hidden inside unfactored polynomials.",
            "Dividing rational expressions always turns into multiplication. To divide by a fraction, you "
            "multiply by its reciprocal — flip the second fraction upside down and multiply. This single rule "
            "means you never actually need a separate division procedure; you only need to be careful about "
            "which fraction gets flipped.",
            "Once a division problem has been rewritten as multiplication, treat it exactly like the previous "
            "concept: factor every polynomial completely, then cancel any factor that appears in a numerator and "
            "a denominator anywhere in the product, even if they started in different original fractions.",
            "Domain restrictions in a division problem include values from <em>both</em> original denominators "
            "<em>and</em> the numerator of the fraction you flipped, because dividing by zero happens if that "
            "flipped denominator (the original numerator) could equal zero.",
            "Watch for expressions that cancel almost completely, leaving a constant. That is not a sign of a "
            "mistake — some rational expressions really do simplify all the way down to a number, which is a "
            "satisfying check that your factoring was correct.",
        ],
        "Multiplying and dividing rational expressions is where factoring pays off the most: a problem that "
        "looks like a wall of polynomials can collapse into something short once everything is factored and the "
        "matching pieces cancel.",
        "Rewrite any division as multiplication by the reciprocal first. Factor every numerator and denominator "
        "completely. Cancel matching factors across the whole product, not just within one original fraction. "
        "Multiply what remains and record every excluded value.",
        solved(1, "Multiply $\\dfrac{x^2-1}{x^2-4}\\cdot\\dfrac{x+2}{x+1}$.",
               ["Factor everything first: $\\dfrac{(x-1)(x+1)}{(x-2)(x+2)}\\cdot\\dfrac{x+2}{x+1}$.",
                "Cancel $(x+1)$ from the first numerator with $(x+1)$ in the second denominator.",
                "Cancel $(x+2)$ from the first denominator with $(x+2)$ in the second numerator.",
                "What remains is $\\dfrac{x-1}{x-2}$."],
               "$\\dfrac{x-1}{x-2}$, with $x\\neq2,-2,-1$", "", "Easy")
        + solved(2, "Divide $\\dfrac{x^2-9}{x+4}\\div\\dfrac{x-3}{x^2-16}$.",
                 ["Rewrite the division as multiplication by the reciprocal: "
                  "$\\dfrac{x^2-9}{x+4}\\cdot\\dfrac{x^2-16}{x-3}$.",
                  "Factor everything: $\\dfrac{(x-3)(x+3)}{x+4}\\cdot\\dfrac{(x-4)(x+4)}{x-3}$.",
                  "Cancel $(x-3)$ and cancel $(x+4)$.",
                  "What remains is $(x+3)(x-4)$."],
                 "$(x+3)(x-4)$, with $x\\neq4,-4,3$",
                 "Domain values come from every original denominator and from the flipped numerator $x-3$.",
                 "Medium")
        + solved(3, "Multiply $\\dfrac{2x^2+2x}{x^2-1}\\cdot\\dfrac{x-1}{4x}$.",
                 ["Factor the first numerator: $2x^2+2x=2x(x+1)$.",
                  "Factor the first denominator as a difference of squares: $x^2-1=(x-1)(x+1)$.",
                  "So the product is $\\dfrac{2x(x+1)}{(x-1)(x+1)}\\cdot\\dfrac{x-1}{4x}$.",
                  "Cancel $(x+1)$, then cancel $(x-1)$, then cancel $x$ from $2x$ and $4x$.",
                  "What remains is $\\dfrac{2}{4}=\\dfrac{1}{2}$."],
                 "$\\dfrac{1}{2}$, with $x\\neq0,1,-1$",
                 "Every variable factor cancelled, leaving a pure number — a good sign the factoring was correct.",
                 "Hard"),
        ("Dropping the reciprocal step when dividing",
         "Dividing by a rational expression means multiplying by its reciprocal. Skipping that flip and "
         "cross-cancelling the original fractions as though they were already being multiplied produces the "
         "wrong expression."),
        ("Flip, factor, cancel",
         "Rewrite every division as multiplication by the reciprocal first, then factor each piece completely "
         "before canceling across the whole product."),
        ["I rewrite every division as multiplication by the reciprocal before doing anything else.",
         "I factor every numerator and denominator completely before looking for cancellations.",
         "I include domain restrictions from the flipped numerator, not just the original denominators."],
        6,
    )

    c3 = concept_block(
        "3. Adding and subtracting rational expressions using the LCD",
        [
            "Adding or subtracting rational expressions requires a common denominator, exactly like adding "
            "numeric fractions such as $\\frac{1}{4}+\\frac{1}{6}$. The least common denominator (LCD) is built "
            "from the factored form of every denominator in the problem, using each distinct factor the highest "
            "number of times it appears in any single denominator.",
            "Once you have the LCD, rewrite each fraction as an equivalent fraction over that LCD by multiplying "
            "its numerator and denominator by whatever factor is missing. Only after every fraction shares the "
            "same denominator can you combine the numerators into a single numerator.",
            "Combining numerators means adding or subtracting the entire top expressions, being especially "
            "careful with subtraction: distribute the negative sign across every term of the numerator you are "
            "subtracting, not just the first term.",
            "After combining, factor the resulting numerator if possible and check whether anything cancels "
            "with the LCD. Many problems do not simplify further, and that is a perfectly normal final answer as "
            "long as the domain restrictions from the original denominators are still recorded.",
            "This section rewards writing everything in factored form immediately. Trying to guess the LCD from "
            "unfactored denominators is the most common source of wrong answers, because hidden common factors "
            "get missed.",
        ],
        "Fraction addition rules do not change just because the denominators contain variables — you still need "
        "a shared denominator before you can combine numerators, and skipping that step produces an expression "
        "that is not actually equal to the original sum.",
        "Factor every denominator. Build the LCD from those factored pieces. Rewrite each fraction over the LCD. "
        "Combine numerators carefully, distributing any subtraction sign across every term. Simplify the result "
        "if possible.",
        solved(1, "Add $\\dfrac{1}{x}+\\dfrac{1}{x+1}$.",
               ["The denominators share no common factor, so the LCD is $x(x+1)$.",
                "Rewrite each fraction: $\\dfrac{x+1}{x(x+1)}+\\dfrac{x}{x(x+1)}$.",
                "Combine numerators: $\\dfrac{(x+1)+x}{x(x+1)}=\\dfrac{2x+1}{x(x+1)}$."],
               "$\\dfrac{2x+1}{x(x+1)}$, with $x\\neq0,-1$", "", "Easy")
        + solved(2, "Subtract $\\dfrac{3}{x-2}-\\dfrac{2}{x+2}$.",
                 ["The LCD is $(x-2)(x+2)$.",
                  "Rewrite each fraction: $\\dfrac{3(x+2)}{(x-2)(x+2)}-\\dfrac{2(x-2)}{(x-2)(x+2)}$.",
                  "Distribute in each numerator: $3(x+2)=3x+6$ and $2(x-2)=2x-4$.",
                  "Subtract carefully: $(3x+6)-(2x-4)=3x+6-2x+4=x+10$.",
                  "The combined fraction is $\\dfrac{x+10}{(x-2)(x+2)}=\\dfrac{x+10}{x^2-4}$."],
                 "$\\dfrac{x+10}{x^2-4}$, with $x\\neq2,-2$",
                 "Distributing the negative sign across the entire second numerator is the step most often "
                 "skipped.", "Medium")
        + solved(3, "Add $\\dfrac{x}{x^2-9}+\\dfrac{2}{x-3}$.",
                 ["Factor the first denominator: $x^2-9=(x-3)(x+3)$, so the LCD is $(x-3)(x+3)$.",
                  "Rewrite the second fraction over the LCD: $\\dfrac{2(x+3)}{(x-3)(x+3)}$.",
                  "Combine numerators: $\\dfrac{x+2(x+3)}{(x-3)(x+3)}=\\dfrac{x+2x+6}{(x-3)(x+3)}=\\dfrac{3x+6}{(x-3)(x+3)}$.",
                  "Factor the numerator: $3x+6=3(x+2)$, giving $\\dfrac{3(x+2)}{(x-3)(x+3)}$."],
                 "$\\dfrac{3(x+2)}{(x-3)(x+3)}$, with $x\\neq3,-3$",
                 "Factoring the final numerator is worth checking every time, even when it does not cancel.",
                 "Hard"),
        ("Adding numerators without a common denominator",
         "You cannot add fractions with different denominators by adding numerators directly. The denominators "
         "must match, built through the LCD, before the numerators are allowed to combine."),
        ("Build the LCD from factored denominators",
         "Factor every denominator first, build the LCD from those factors, rewrite each fraction over that "
         "LCD, and only then combine numerators."),
        ["I factor every denominator before building the LCD.",
         "I rewrite each fraction completely over the LCD before combining numerators.",
         "I distribute a subtraction sign across every term of the numerator being subtracted."],
        11,
    )

    c4 = concept_block(
        "4. Simplifying complex fractions",
        [
            "A complex fraction is a fraction that contains one or more fractions inside its numerator, its "
            "denominator, or both — something like $\\dfrac{1/x+1/2}{1/x-1/2}$. These look intimidating, but "
            "there are only two clean methods for simplifying them, and both rely on skills you already have.",
            "Method one: combine the small fractions in the numerator into a single fraction, combine the small "
            "fractions in the denominator into a single fraction, and then divide the resulting numerator "
            "fraction by the resulting denominator fraction using the multiply-by-the-reciprocal rule.",
            "Method two, often faster: find the LCD of every small fraction anywhere inside the complex "
            "fraction, and multiply the entire top and the entire bottom of the big fraction by that LCD. This "
            "clears every small denominator in one move, leaving a simpler expression to finish simplifying.",
            "Whichever method you use, be careful to multiply the LCD by <em>every</em> term in the numerator "
            "and <em>every</em> term in the denominator of the big fraction, not just the fractional pieces. "
            "Missing a term is the most common error in this section.",
            "Complex fractions appear constantly in later math, including in the definition of a derivative in "
            "calculus, so building comfort with them now pays off well beyond this unit.",
        ],
        "Complex fractions feel harder only because there are two layers of fractions to track at once. Once "
        "you clear the inner fractions using the LCD, the problem collapses back into ordinary rational "
        "expression simplification.",
        "Identify every small fraction inside the complex fraction and find their overall LCD. Multiply the "
        "entire top and the entire bottom of the big fraction by that LCD, distributing across every term. "
        "Simplify what remains and record domain restrictions from every denominator you saw along the way.",
        solved(1, "Simplify $\\dfrac{2/x}{4/x^2}$.",
               ["Multiply by the reciprocal of the bottom fraction: $\\dfrac{2}{x}\\cdot\\dfrac{x^2}{4}$.",
                "Multiply straight across: $\\dfrac{2x^2}{4x}$.",
                "Cancel common factors of $2$ and $x$: $\\dfrac{2x^2}{4x}=\\dfrac{x}{2}$."],
               "$\\dfrac{x}{2}$, with $x\\neq0$", "", "Easy")
        + solved(2, "Simplify $\\dfrac{1/x+1/y}{1/x-1/y}$.",
                 ["Combine the top over the LCD $xy$: $\\dfrac{y+x}{xy}$.",
                  "Combine the bottom over the LCD $xy$: $\\dfrac{y-x}{xy}$.",
                  "Divide by multiplying by the reciprocal: $\\dfrac{y+x}{xy}\\cdot\\dfrac{xy}{y-x}$.",
                  "The $xy$ cancels, leaving $\\dfrac{x+y}{y-x}$."],
                 "$\\dfrac{x+y}{y-x}$, with $x\\neq0,y\\neq0,x\\neq y$",
                 "This is method one — combine each layer, then divide.", "Medium")
        + solved(3, "Simplify $\\dfrac{1-1/x}{1-1/x^2}$.",
                 ["Multiply the entire top and bottom by the overall LCD, $x^2$.",
                  "Top becomes $x^2\\left(1-\\dfrac1x\\right)=x^2-x$.",
                  "Bottom becomes $x^2\\left(1-\\dfrac1{x^2}\\right)=x^2-1$.",
                  "So the expression is $\\dfrac{x^2-x}{x^2-1}=\\dfrac{x(x-1)}{(x-1)(x+1)}$.",
                  "Cancel $(x-1)$: $\\dfrac{x}{x+1}$."],
                 "$\\dfrac{x}{x+1}$, with $x\\neq0,1,-1$",
                 "This is method two — clear every inner denominator at once using the overall LCD.", "Hard"),
        ("Multiplying by the wrong denominator when clearing a complex fraction",
         "Complex fractions have two layers. Multiplying only part of the expression by the LCD, instead of "
         "every term in both the entire top and the entire bottom, leaves fragments that are not actually "
         "simplified."),
        ("Multiply every term by the overall LCD",
         "Find the LCD of every small fraction inside the complex fraction, multiply the whole top and the "
         "whole bottom by it, distributing across every term, and simplify what remains."),
        ["I find the overall LCD of every small fraction before doing anything else.",
         "I multiply every single term in the top and bottom by that LCD, not just the fractional terms.",
         "I can simplify a complex fraction using either the combine-then-divide method or the clear-the-LCD method."],
        16,
    )

    c5 = concept_block(
        "5. Solving rational equations and rejecting extraneous solutions",
        [
            "A rational equation is any equation containing at least one variable in a denominator, such as "
            "$\\dfrac{3}{x}+\\dfrac{1}{2}=\\dfrac{6}{x}$. The core strategy is to clear every denominator by "
            "multiplying both sides of the equation by the LCD, turning the rational equation into a simpler "
            "polynomial equation that you already know how to solve.",
            "Before doing any algebra, write down the domain: every value of $x$ that would make any original "
            "denominator equal zero. These values are permanently forbidden as solutions, no matter what the "
            "cleared equation eventually produces.",
            "After multiplying by the LCD and simplifying, solve the resulting linear or quadratic equation "
            "using ordinary methods — combining like terms, factoring, or the quadratic formula.",
            "The final and most important step is to compare every candidate solution against the domain you "
            "wrote at the beginning. Any candidate equal to a forbidden value is called an <strong>extraneous "
            "solution</strong> and must be discarded, even though it satisfies the cleared polynomial equation.",
            "Extraneous solutions happen because multiplying both sides by an expression containing the variable "
            "can introduce new solutions that were never valid for the original fractions. This is a completely "
            "normal and expected part of solving rational equations, not a sign that the algebra itself failed.",
        ],
        "Clearing denominators makes a rational equation easy to solve, but it can silently introduce solutions "
        "that never belonged to the original equation. The domain check at the end is not optional — it is the "
        "step that makes the final answer trustworthy.",
        "List every value forbidden by the original denominators. Multiply both sides by the LCD to clear "
        "fractions. Solve the resulting equation. Compare every candidate to the forbidden list and discard any "
        "match as extraneous.",
        solved(1, "Solve $\\dfrac{1}{x}+\\dfrac{1}{2}=\\dfrac{3}{x}$.",
               ["Domain: $x\\neq0$.",
                "Multiply every term by the LCD, $2x$: $2+x=6$.",
                "Solve: $x=4$.",
                "Check against the domain: $4\\neq0$, so the solution is valid."],
               "$x=4$", "", "Easy")
        + solved(2, "Solve $\\dfrac{x}{x-2}=\\dfrac{2}{x-2}+3$.",
                 ["Domain: $x\\neq2$.",
                  "Multiply every term by the LCD, $x-2$: $x=2+3(x-2)$.",
                  "Distribute and simplify: $x=2+3x-6=3x-4$.",
                  "Solve: $x-3x=-4 \\Rightarrow -2x=-4 \\Rightarrow x=2$.",
                  "Check against the domain: $x=2$ is forbidden, so this candidate is extraneous and rejected."],
                 "No solution",
                 "The equation has no valid solution because the only candidate makes an original denominator "
                 "zero.", "Medium")
        + solved(3, "Solve $\\dfrac{2}{x-1}-\\dfrac{1}{x+1}=\\dfrac{3}{x^2-1}$.",
                 ["Factor the denominator on the right: $x^2-1=(x-1)(x+1)$. Domain: $x\\neq1,-1$.",
                  "Multiply every term by the LCD, $(x-1)(x+1)$: $2(x+1)-(x-1)=3$.",
                  "Distribute: $2x+2-x+1=3 \\Rightarrow x+3=3$.",
                  "Solve: $x=0$.",
                  "Check against the domain: $0\\neq1,-1$, so the solution is valid."],
                 "$x=0$", "", "Hard"),
        ("Accepting every algebraic solution without checking the original equation",
         "Clearing denominators can introduce values that make an original denominator zero. Those values must "
         "be rejected as extraneous even though they solve the cleared polynomial equation perfectly."),
        ("List the domain before you solve, check every candidate after",
         "Write down every value that would zero a denominator before starting any algebra. Once you have "
         "candidate solutions, test each one against that list, not just against the cleared equation."),
        ["I write the domain restrictions before I start clearing denominators.",
         "I multiply every single term in the equation by the LCD, not just some of them.",
         "I check every candidate solution against the original denominators before finalizing my answer."],
        21,
    )

    c6 = concept_block(
        "6. Applications: work-rate problems and similar-triangle proportions",
        [
            "Rational equations are not just an abstract algebra exercise — they model real situations, and two "
            "of the most common are work-rate problems (how long does a task take when multiple workers or "
            "machines act together) and proportions from similar geometric figures.",
            "The key idea in work-rate problems is that <strong>rates</strong> add, not times. If a worker "
            "finishes a job alone in $a$ hours, their rate is $\\dfrac{1}{a}$ of the job per hour. When two "
            "workers act together, their rates add: $\\dfrac{1}{a}+\\dfrac{1}{b}=\\dfrac{1}{t}$, where $t$ is "
            "the time to finish the job together.",
            "Solving a work-rate equation almost always means clearing denominators exactly the way you did in "
            "the previous concept, then solving the resulting equation for the unknown time or rate.",
            "Similar triangles (and other similar figures) have corresponding sides that are proportional. "
            "Setting up the correct proportion — matching corresponding sides carefully — turns a geometry "
            "problem into the same cross-multiplication process you used to solve rational equations.",
            "In both types of application, the hardest part is usually the setup, not the algebra. Take time to "
            "translate the words into a rational equation before solving, and always ask whether your final "
            "answer makes sense in context (a time cannot be negative, and a triangle side cannot be negative "
            "either).",
        ],
        "Work-rate and proportion problems show why rational expressions matter outside of a textbook: they "
        "model real combined effort and real geometric scaling, and the same LCD and cross-multiplication tools "
        "you have been practicing solve them directly.",
        "Identify whether the situation is a rate (write $\\dfrac{1}{\\text{time}}$ for each worker or machine "
        "and add the rates) or a proportion (match corresponding sides and cross multiply). Set up the equation "
        "carefully in words first, then solve using the LCD or cross multiplication, and check that the answer "
        "makes sense in context.",
        solved(1, "Pipe A fills a tank in 4 hours; pipe B fills the same tank in 6 hours. How long does it "
                  "take working together?",
               ["Write each rate as a fraction of the tank per hour: A's rate is $\\dfrac14$, B's rate is "
                "$\\dfrac16$.",
                "Add the rates and set equal to $\\dfrac1t$: $\\dfrac14+\\dfrac16=\\dfrac1t$.",
                "Find the LCD of $4$, $6$, and $t$: it is $12t$. Clearing denominators gives $3t+2t=12$.",
                "Solve: $5t=12 \\Rightarrow t=\\dfrac{12}{5}=2.4$ hours."],
               "$2.4$ hours", "", "Easy")
        + solved(2, "In similar triangles, a side of length $x$ corresponds to a side of length $6$, and "
                    "another pair of corresponding sides are $8$ and $12$. Find $x$.",
                 ["Set up the proportion matching corresponding sides: $\\dfrac{x}{6}=\\dfrac{8}{12}$.",
                  "Cross multiply: $12x=48$.",
                  "Solve: $x=4$."],
                 "$x=4$", "", "Medium")
        + solved(3, "Worker A alone takes 5 hours to finish a job. Working with worker B, the two finish "
                    "together in 2 hours. How long would worker B need alone?",
                 ["Let $x$ be the number of hours worker B needs alone. B's rate is $\\dfrac1x$.",
                  "Set up the combined-rate equation: $\\dfrac15+\\dfrac1x=\\dfrac12$.",
                  "Multiply every term by the LCD, $10x$: $2x+10=5x$.",
                  "Solve: $10=3x \\Rightarrow x=\\dfrac{10}{3}$ hours.",
                  "As a check, $\\dfrac{10}{3}\\approx3.33$ hours is longer than the combined 2 hours, which "
                  "makes sense because working alone should take longer than working with a partner."],
                 "$\\dfrac{10}{3}$ hours (about $3.33$ hours)", "", "Hard"),
        ("Setting up a work-rate proportion backwards",
         "Rates add as 'fraction of the job per hour,' not as raw time. Adding the two workers' times together "
         "directly gives a number far larger than the true combined time, which should always be shorter than "
         "either individual time."),
        ("Write rates as 1/time and add the rates",
         "For work problems, write each worker's rate as $1$ divided by their alone-time, add the rates "
         "together, and solve $\\dfrac1{\\text{time}_1}+\\dfrac1{\\text{time}_2}=\\dfrac1{\\text{time together}}$."),
        ["I write each worker's rate as 1 divided by their alone-time before adding anything.",
         "I set up similar-triangle proportions by matching corresponding sides, not just any two sides.",
         "I check that a work-rate or proportion answer makes sense in context (positive, and shorter than "
         "either individual time)."],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        AUDIENCE,
        [
            "Simplify rational expressions by factoring first and canceling only matching factors",
            "Multiply and divide rational expressions, including flipping for division",
            "Add and subtract rational expressions using a properly built LCD",
            "Simplify complex fractions using either the combine-and-divide or clear-the-LCD method",
            "Solve rational equations and identify extraneous solutions",
            "Apply rational equations to work-rate problems and similar-triangle proportions",
        ],
        body,
        practice_slots(31, 50),
    )
    return title, description, content, _u5_questions()


# =====================================================================================
# UNIT 6: Radical Functions & Rational Exponents
# =====================================================================================

def _u6_questions():
    qs = []

    # Concept 1 — nth roots & principal roots (1-5)
    qs.append(mq("Evaluate $\\sqrt[3]{8}$.", "2",
                 "$2^3=8$, so the principal cube root of $8$ is $2$.", 1))
    qs.append(mq("Evaluate $\\sqrt[3]{-64}$.", "-4",
                 "$(-4)^3=-64$, and odd-index roots of negative numbers are real, so $\\sqrt[3]{-64}=-4$.", 2))
    qs.append(mq("Evaluate $\\sqrt[4]{81}$.", "3",
                 "$3^4=81$, so the principal fourth root of $81$ is $3$.", 3))
    qs.append(mq("Evaluate $\\sqrt[5]{-32}$.", "-2",
                 "$(-2)^5=-32$, and odd-index roots of negative numbers are real, so $\\sqrt[5]{-32}=-2$.", 4))
    qs.append(mq("Which expression is undefined among the real numbers: $\\sqrt{-16}$ or $\\sqrt[3]{-16}$?",
                 "sqrt(-16)",
                 "No real number squared equals a negative number, so $\\sqrt{-16}$ is undefined among reals, "
                 "while $\\sqrt[3]{-16}$ is a real (negative, irrational) number.",
                 5, distractors=["cbrt(-16)", "Both are undefined", "Neither is undefined"]))

    # Concept 2 — rational exponents (6-10)
    qs.append(mq("Evaluate $4^{3/2}$.", "8",
                 "Take the root first: $\\sqrt4=2$. Then apply the power: $2^3=8$.", 6))
    qs.append(mq("Evaluate $9^{3/2}$.", "27",
                 "Take the root first: $\\sqrt9=3$. Then apply the power: $3^3=27$.", 7))
    qs.append(mq("Evaluate $32^{2/5}$.", "4",
                 "Take the root first: $\\sqrt[5]{32}=2$. Then apply the power: $2^2=4$.", 8))
    qs.append(mq("Evaluate $25^{-1/2}$.", "1/5",
                 "$25^{1/2}=5$, and the negative exponent means the reciprocal: $25^{-1/2}=\\dfrac15$.",
                 9, distractors=["-5", "5", "1/25"]))
    qs.append(mq("Evaluate $81^{3/4}$.", "27",
                 "Take the root first: $\\sqrt[4]{81}=3$. Then apply the power: $3^3=27$.", 10))

    # Concept 3 — simplify radicals with variables (11-15)
    qs.append(mq("Simplify $\\sqrt{72}$.", "6√2",
                 "Write $72=36\\cdot2$: $\\sqrt{72}=\\sqrt{36}\\cdot\\sqrt2=6\\sqrt2$.",
                 11, distractors=["8√2", "36√2", "2√18"]))
    qs.append(mq("Simplify $\\sqrt{x^4}$.", "x^2",
                 "Since $x^4=(x^2)^2$ and $x^2$ is always nonnegative, $\\sqrt{x^4}=x^2$ with no absolute value "
                 "needed.", 12, distractors=["|x|^2", "x^4", "x"]))
    qs.append(mq("Simplify $\\sqrt{x^2}$.", "|x|",
                 "The principal square root is never negative, so $\\sqrt{x^2}=|x|$ to guarantee a nonnegative "
                 "result even when $x$ is negative.", 13, distractors=["x", "-x", "x^2"]))
    qs.append(mq("Simplify $\\sqrt[3]{27x^3}$.", "3x",
                 "Cube roots do not need absolute value: $\\sqrt[3]{27x^3}=\\sqrt[3]{27}\\cdot\\sqrt[3]{x^3}=3x$.",
                 14, distractors=["3|x|", "9x", "27x"]))
    qs.append(mq("Simplify $\\sqrt{48x^2}$.", "4|x|√3",
                 "Write $48x^2=16x^2\\cdot3$: $\\sqrt{16x^2}\\cdot\\sqrt3=4|x|\\sqrt3$.",
                 15, distractors=["4x√3", "16|x|√3", "4|x|√6"]))

    # Concept 4 — operations with radicals (16-20)
    qs.append(mq("Simplify $4\\sqrt5-\\sqrt5$.", "3√5",
                 "These are like radicals, so combine coefficients: $4\\sqrt5-1\\sqrt5=3\\sqrt5$.",
                 16, distractors=["3", "4√4", "3√10"]))
    qs.append(mq("Multiply $\\sqrt2\\cdot\\sqrt8$.", "4",
                 "$\\sqrt2\\cdot\\sqrt8=\\sqrt{16}=4$.", 17, distractors=["16", "2√2", "√10"]))
    qs.append(mq("Rationalize $\\dfrac{1}{\\sqrt5}$.", "√5/5",
                 "Multiply top and bottom by $\\sqrt5$: $\\dfrac{\\sqrt5}{5}$.",
                 18, distractors=["1/5", "5/√5", "√5"]))
    qs.append(mq("Multiply $2\\sqrt3\\cdot3\\sqrt3$.", "18",
                 "Multiply coefficients and radicals separately: $2\\cdot3=6$ and $\\sqrt3\\cdot\\sqrt3=3$, so "
                 "$6\\cdot3=18$.", 19, distractors=["6√3", "36", "9"]))
    qs.append(mq("Rationalize $\\dfrac{2}{\\sqrt7-1}$.", "(√7+1)/3",
                 "Multiply top and bottom by the conjugate $\\sqrt7+1$: $\\dfrac{2(\\sqrt7+1)}{7-1}"
                 "=\\dfrac{2(\\sqrt7+1)}{6}=\\dfrac{\\sqrt7+1}{3}$.",
                 20, distractors=["(√7-1)/3", "2(√7+1)/6", "√7+1"]))

    # Concept 5 — solving radical equations (21-25)
    qs.append(mq("Solve $\\sqrt{x-2}=5$.", "x=27",
                 "Square both sides: $x-2=25 \\Rightarrow x=27$.", 21, distractors=["x=23", "x=25", "x=7"]))
    qs.append(mq("Solve $\\sqrt{3x+1}=x-1$.", "x=5",
                 "Domain requires $x\\ge1$. Squaring gives $3x+1=x^2-2x+1 \\Rightarrow 0=x^2-5x \\Rightarrow "
                 "x=0$ or $x=5$. Since $x=0$ fails the domain $x\\ge1$, it is extraneous; $x=5$ checks correctly.",
                 22, distractors=["x=0", "x=1", "No solution"]))
    qs.append(mq("Solve $\\sqrt{x+4}=x-2$.", "x=5",
                 "Domain requires $x\\ge2$. Squaring gives $x+4=x^2-4x+4 \\Rightarrow 0=x^2-5x \\Rightarrow "
                 "x=0$ or $x=5$. Since $x=0$ fails the domain, it is extraneous; $x=5$ checks correctly.",
                 23, distractors=["x=0", "x=4", "No solution"]))
    qs.append(mq("Solve $\\sqrt{2x+3}=3$.", "x=3",
                 "Square both sides: $2x+3=9 \\Rightarrow 2x=6 \\Rightarrow x=3$.",
                 24, distractors=["x=6", "x=4.5", "x=1.5"]))
    qs.append(mq("Solve $\\sqrt{x+1}+1=x$.", "x=3",
                 "Isolate the radical: $\\sqrt{x+1}=x-1$, requiring $x\\ge1$. Squaring gives "
                 "$x+1=x^2-2x+1 \\Rightarrow 0=x^2-3x \\Rightarrow x=0$ or $x=3$. Since $x=0$ fails the domain, "
                 "it is extraneous; $x=3$ checks correctly.",
                 25, distractors=["x=0", "x=1", "No solution"]))

    # Concept 6 — graphing radical functions (26-30)
    qs.append(mq("For $y=\\sqrt{x-5}+2$, what is the domain?", "x≥5",
                 "The radicand must be nonnegative: $x-5\\ge0 \\Rightarrow x\\ge5$.",
                 26, distractors=["x≥2", "x≥0", "x≥-5"]))
    qs.append(mq("For $y=\\sqrt{x+4}-1$, what is the starting point of the graph?", "(-4,-1)",
                 "The parent point $(0,0)$ shifts left 4 and down 1.",
                 27, distractors=["(4,-1)", "(-4,1)", "(4,1)"]))
    qs.append(mq("For $y=-\\sqrt{x-1}$, what is the range?", "y≤0",
                 "Reflecting the parent square-root graph over the $x$-axis flips its usual nonnegative range "
                 "to nonpositive: $y\\le0$.",
                 28, distractors=["y≥0", "x≤0", "All reals"]))
    qs.append(mq("For $y=\\sqrt[3]{x-3}+4$, what is the inflection (center) point of the graph?", "(3,4)",
                 "The parent cube-root point $(0,0)$ shifts right 3 and up 4.",
                 29, distractors=["(-3,4)", "(3,-4)", "(4,3)"]))
    qs.append(mq("Which transformation turns $y=\\sqrt{x}$ into $y=\\sqrt{x+6}$?", "Shift left 6",
                 "Adding inside the radicand shifts the graph horizontally in the opposite direction of the "
                 "sign, so $+6$ inside shifts the graph left 6 units.",
                 30, distractors=["Shift right 6", "Shift up 6", "Shift down 6"]))

    finale = []

    # Easy 31-45
    for n in (1, 2, 3, 4, 5):
        finale.append(mq(f"Evaluate $\\sqrt[3]{{{n**3}}}$.", str(n),
                         f"${n}^3={n**3}$, so $\\sqrt[3]{{{n**3}}}={n}$.", 0))
    for n in (2, 3, 4, 5, 6):
        finale.append(mq(f"Evaluate $\\sqrt{{{n*n}}}$.", str(n),
                         f"${n}^2={n*n}$, so $\\sqrt{{{n*n}}}={n}$.", 0))
    for a in (2, 3, 4, 5, 6):
        finale.append(mq(f"Simplify $\\sqrt{{{a*a}x^2}}$.", f"{a}|x|",
                         f"$\\sqrt{{{a*a}x^2}}=\\sqrt{{{a*a}}}\\cdot\\sqrt{{x^2}}={a}|x|$.",
                         0, distractors=[f"{a}x", f"{a*a}|x|", f"{a}x^2"]))

    # Medium 46-60
    for rad, coef, inside in [(12, 2, 3), (20, 2, 5), (45, 3, 5), (72, 6, 2), (98, 7, 2)]:
        finale.append(mq(f"Simplify $\\sqrt{{{rad}}}$.", f"{coef}√{inside}",
                         f"Factor out the largest perfect-square factor: $\\sqrt{{{rad}}}={coef}\\sqrt{{{inside}}}$.",
                         0, distractors=[f"{inside}√{coef}", f"{coef+1}√{inside}", f"√{rad}"]))
    for base, exp_num, exp_den, ans in [(8, 2, 3, 4), (27, 2, 3, 9), (16, 3, 4, 8), (32, 4, 5, 16),
                                          (64, 2, 3, 16)]:
        finale.append(mq(f"Evaluate ${base}^{{{exp_num}/{exp_den}}}$.", str(ans),
                         f"Take the root first (${exp_den}$th root of {base}), then raise to the "
                         f"${exp_num}$ power to get {ans}.",
                         0, distractors=[str(ans*2), str(ans//2 if ans % 2 == 0 else ans+1), str(ans+4)]))
    for text, ans, expl, dis in [
        ("Solve $\\sqrt{x-1}=3$.", "x=10", "Square both sides: $x-1=9 \\Rightarrow x=10$.",
         ["x=9", "x=8", "x=4"]),
        ("Solve $\\sqrt{x+2}=4$.", "x=14", "Square both sides: $x+2=16 \\Rightarrow x=14$.",
         ["x=16", "x=12", "x=2"]),
        ("Solve $\\sqrt{2x}=6$.", "x=18", "Square both sides: $2x=36 \\Rightarrow x=18$.",
         ["x=36", "x=12", "x=3"]),
        ("Solve $\\sqrt{x-4}=2$.", "x=8", "Square both sides: $x-4=4 \\Rightarrow x=8$.",
         ["x=6", "x=4", "x=16"]),
        ("Solve $\\sqrt{3x+4}=5$.", "x=7", "Square both sides: $3x+4=25 \\Rightarrow 3x=21 \\Rightarrow x=7$.",
         ["x=21", "x=3", "x=9"]),
    ]:
        finale.append(mq(text, ans, expl, 0, distractors=dis))

    # Hard 61-70
    for text, ans, expl, dis in [
        ("Solve $\\sqrt{x+5}=x-1$.", "x=4",
         "Domain requires $x\\ge1$. Squaring gives $x+5=x^2-2x+1 \\Rightarrow 0=x^2-3x-4 \\Rightarrow "
         "(x-4)(x+1)=0$. Since $x=-1$ fails the domain, it is extraneous; $x=4$ checks correctly.",
         ["x=-1", "x=1", "No solution"]),
        ("Simplify $\\sqrt{75x^3}$ (assume $x\\ge0$).", "5x√(3x)",
         "Write $75x^3=25x^2\\cdot3x$: $\\sqrt{25x^2}\\cdot\\sqrt{3x}=5x\\sqrt{3x}$, and $x\\ge0$ removes the "
         "need for absolute value.",
         ["5x^2√3", "25x√(3x)", "5√(3x^3)"]),
        ("Rationalize $\\dfrac{3}{\\sqrt5+\\sqrt2}$.", "√5-√2",
         "Multiply by the conjugate $\\sqrt5-\\sqrt2$: $\\dfrac{3(\\sqrt5-\\sqrt2)}{5-2}"
         "=\\dfrac{3(\\sqrt5-\\sqrt2)}{3}=\\sqrt5-\\sqrt2$.",
         ["√5+√2", "3(√5-√2)", "(√5-√2)/3"]),
        ("Simplify $\\sqrt8+\\sqrt{18}$.", "5√2",
         "Simplify each radical first: $\\sqrt8=2\\sqrt2$ and $\\sqrt{18}=3\\sqrt2$. Add like radicals: "
         "$2\\sqrt2+3\\sqrt2=5\\sqrt2$.",
         ["√26", "5√4", "6√2"]),
        ("Solve $\\sqrt{x+1}-\\sqrt{x-4}=1$.", "x=8",
         "Isolate: $\\sqrt{x+1}=1+\\sqrt{x-4}$, requiring $x\\ge4$. Squaring gives "
         "$x+1=1+2\\sqrt{x-4}+x-4 \\Rightarrow 4=2\\sqrt{x-4} \\Rightarrow \\sqrt{x-4}=2 \\Rightarrow x=8$.",
         ["x=5", "x=4", "x=13"]),
        ("Evaluate $\\left(\\dfrac18\\right)^{-2/3}$.", "4",
         "A negative exponent flips to the reciprocal: $8^{2/3}=(\\sqrt[3]8)^2=2^2=4$.",
         ["1/4", "64", "2"]),
        ("For $y=2\\sqrt{x-3}+1$, find the domain and range.", "domain x≥3, range y≥1",
         "The radicand requires $x-3\\ge0 \\Rightarrow x\\ge3$. Since the square root output is always "
         "$\\ge0$ and is scaled by 2 then shifted up 1, the range is $y\\ge1$.",
         ["domain x≥1, range y≥3", "domain x≥3, range y≥0", "domain x≥0, range y≥1"]),
        ("Simplify $\\sqrt[3]{16x^4}$.", "2x·∛(2x)",
         "Write $16x^4=8x^3\\cdot2x$: $\\sqrt[3]{8x^3}\\cdot\\sqrt[3]{2x}=2x\\sqrt[3]{2x}$ (cube roots need no "
         "absolute value).",
         ["4x·∛(2x)", "2x^2·∛2", "8x·∛(2x)"]),
        ("Multiply $(\\sqrt{x}+3)(\\sqrt{x}-3)$.", "x-9",
         "This is a difference of squares: $(\\sqrt x)^2-3^2=x-9$, with $x\\ge0$.",
         ["x-6", "x+9", "x^2-9"]),
        ("A wave speed formula gives $v=\\sqrt{9.8h}$ (h in meters). If $v=14$, find $h$ to the nearest "
         "whole number.", "20",
         "Square both sides: $196=9.8h \\Rightarrow h=20$.",
         ["14", "9.8", "196"]),
    ]:
        finale.append(mq(text, ans, expl, 0, distractors=dis))

    # Stretch 71-80
    for text, ans, expl, dis in [
        ("Solve $x^{2/3}=4$ for $x>0$.", "x=8",
         "Raise both sides to the $\\frac32$ power: $x=4^{3/2}=(\\sqrt4)^3=2^3=8$.",
         ["x=64", "x=6", "x=16"]),
        ("Solve $\\sqrt{x^2-9}=x-1$.", "x=5",
         "Square both sides: $x^2-9=x^2-2x+1 \\Rightarrow -9=-2x+1 \\Rightarrow -10=-2x \\Rightarrow x=5$. "
         "Checking: $\\sqrt{25-9}=\\sqrt{16}=4=5-1$.",
         ["x=9", "x=3", "x=10"]),
        ("Rationalize $\\dfrac{\\sqrt x-2}{\\sqrt x+2}$.", "(x-4√x+4)/(x-4)",
         "Multiply top and bottom by the conjugate $\\sqrt x-2$: the numerator becomes "
         "$(\\sqrt x-2)^2=x-4\\sqrt x+4$ and the denominator becomes $x-4$.",
         ["(x+4√x+4)/(x-4)", "(x-4)/(x-4√x+4)", "√x-2"]),
        ("Solve $(x-1)^{3/2}=8$.", "x=5",
         "Raise both sides to the $\\frac23$ power: $x-1=8^{2/3}=(\\sqrt[3]8)^2=4 \\Rightarrow x=5$.",
         ["x=9", "x=3", "x=17"]),
        ("Solve $\\sqrt{2x+3}=x$.", "x=3",
         "Domain requires $x\\ge0$. Squaring gives $2x+3=x^2 \\Rightarrow x^2-2x-3=0 \\Rightarrow "
         "(x-3)(x+1)=0$. Since $x=-1$ fails the domain, only $x=3$ is valid.",
         ["x=-1", "x=1", "No solution"]),
        ("Simplify $(\\sqrt3+\\sqrt2)^2$.", "5+2√6",
         "Expand like a binomial square: $3+2\\sqrt3\\sqrt2+2=5+2\\sqrt6$.",
         ["5+√6", "5+2√5", "6+2√6"]),
        ("Solve $x^{-1/2}=\\dfrac15$.", "x=25",
         "Take the reciprocal of both sides: $x^{1/2}=5 \\Rightarrow x=25$.",
         ["x=5", "x=1/25", "x=1/5"]),
        ("Solve $\\sqrt[3]{2x-1}=3$.", "x=14",
         "Cube both sides: $2x-1=27 \\Rightarrow 2x=28 \\Rightarrow x=14$.",
         ["x=13", "x=28", "x=41"]),
        ("Evaluate $\\sqrt{50}\\cdot\\sqrt2$.", "10",
         "$\\sqrt{50}\\cdot\\sqrt2=\\sqrt{100}=10$.",
         ["100", "√100", "25"]),
        ("Find the distance between $(1,2)$ and $(4,6)$.", "5",
         "Distance formula: $\\sqrt{(4-1)^2+(6-2)^2}=\\sqrt{9+16}=\\sqrt{25}=5$.",
         ["7", "√13", "25"]),
    ]:
        finale.append(mq(text, ans, expl, 0, distractors=dis))

    qs.extend(finale[:50])
    return _fill80(qs)


def build_unit6():
    title = "Algebra 2 Unit 6: Radical Functions & Rational Exponents"
    description = (
        "Deep, patient coverage of radicals for grade 10 Algebra 2 — nth roots, rational exponents, simplifying "
        "radicals with variables, radical arithmetic and rationalizing, solving radical equations with "
        "extraneous-root checks, and graphing square-root and cube-root transformations."
    )

    c1 = concept_block(
        "1. nth roots and the principal root",
        [
            "An $n$th root of a number $a$ is a value that, when raised to the $n$th power, gives back $a$. "
            "Written as $\\sqrt[n]{a}$, the small number $n$ tucked into the radical is called the index, and "
            "when no index is written, it is assumed to be $2$ (a square root).",
            "When the index is <strong>even</strong> (square root, fourth root, and so on), the radicand must "
            "be nonnegative for the result to be a real number, and the <strong>principal root</strong> is "
            "defined to be the nonnegative one. This is why $\\sqrt{16}=4$ and never $-4$, even though "
            "$(-4)^2=16$ as well.",
            "When the index is <strong>odd</strong> (cube root, fifth root, and so on), every real number has "
            "exactly one real $n$th root, and that root carries the same sign as the original number. Negative "
            "numbers under an odd root are completely normal and produce real, often negative, answers.",
            "This even-versus-odd distinction is the single most important idea in this concept, and it resurfaces "
            "constantly: it explains why $\\sqrt{-9}$ has no real value while $\\sqrt[3]{-27}=-3$ works "
            "perfectly fine, and it will govern domain restrictions for every radical function you graph later "
            "in this unit.",
            "Building fluency with perfect powers — squares, cubes, fourth powers — for small integers makes "
            "every later section faster, because simplifying a radical almost always starts with spotting a "
            "perfect-power factor hiding inside a larger number.",
        ],
        "Roots are the inverse operation of exponents, and the even/odd split in how many real roots exist is "
        "the reason square-root graphs only exist for $x\\ge0$ while cube-root graphs stretch across every real "
        "number.",
        "Identify the index first. If it is even, check that the radicand is nonnegative before evaluating, and "
        "always take the nonnegative principal root. If it is odd, evaluate directly and let the sign of the "
        "answer match the sign of the radicand.",
        solved(1, "Evaluate $\\sqrt[3]{-27}$.",
               ["The index is odd, so a negative radicand is completely acceptable.",
                "Ask: what number cubed gives $-27$?",
                "$(-3)^3=-27$, so the cube root is $-3$."],
               "$-3$", "", "Easy")
        + solved(2, "Evaluate $\\sqrt[4]{16}$.",
                 ["The index is even, so only the nonnegative principal root is valid.",
                  "Ask: what nonnegative number to the fourth power gives $16$?",
                  "$2^4=16$, so the principal fourth root is $2$ (not $-2$, even though $(-2)^4=16$ too)."],
                 "$2$", "", "Medium")
        + solved(3, "Compare $-\\sqrt{49}$ and $\\sqrt{-49}$.",
                 ["$-\\sqrt{49}$ means take the principal (nonnegative) square root of $49$ first, then apply "
                  "the negative sign outside: $\\sqrt{49}=7$, so $-\\sqrt{49}=-7$, a real number.",
                  "$\\sqrt{-49}$ means take the square root of a negative number directly. No real number "
                  "squared gives $-49$, so this expression is undefined among the reals.",
                  "The placement of the negative sign — inside versus outside the radical — completely changes "
                  "whether the expression is defined."],
                 "$-\\sqrt{49}=-7$ (real); $\\sqrt{-49}$ is undefined among the reals",
                 "This distinction between a negative result and an undefined result trips up many students at "
                 "first.", "Hard"),
        ("Assuming every even root of a negative number exists in the reals",
         "$\\sqrt{-16}$ is undefined among real numbers because no real number squared gives a negative result, "
         "while an odd root like $\\sqrt[3]{-16}$ is perfectly defined and real."),
        ("Check index parity before you evaluate",
         "Before evaluating any root, ask whether the index is even or odd and whether the radicand is "
         "negative. That single check tells you immediately whether a real answer exists."),
        ["I know that even-index roots require a nonnegative radicand to be real.",
         "I know that odd-index roots are defined for every real number, positive or negative.",
         "I can explain the difference between $-\\sqrt{49}$ and $\\sqrt{-49}$."],
        1,
    )

    c2 = concept_block(
        "2. Rational exponents and converting between exponent and radical form",
        [
            "A rational exponent like $a^{m/n}$ is just another way of writing a radical: $a^{m/n}=\\left(\\sqrt[n]{a}\\right)^m"
            "=\\sqrt[n]{a^m}$. The denominator of the exponent, $n$, tells you which root to take, and the "
            "numerator, $m$, tells you which power to apply.",
            "In almost every case, it is easier to take the root first (using the small root number, $n$) and "
            "then raise that already-simplified result to the power $m$, rather than raising $a$ to the large "
            "power $m$ first and then trying to find the $n$th root of a huge number.",
            "Negative rational exponents behave exactly like negative integer exponents: $a^{-m/n}=\\dfrac{1}"
            "{a^{m/n}}$. Take the reciprocal of the base (or of the final answer) whenever you see a negative "
            "exponent, and then proceed with the root-then-power process as usual.",
            "Rational exponents obey the same exponent rules you already know from earlier in Algebra 2 — "
            "product rule, quotient rule, power of a power — which makes them far more convenient than radical "
            "notation whenever an expression needs to be simplified algebraically rather than evaluated.",
            "Being fluent in both directions — converting a radical into a rational exponent and a rational "
            "exponent back into a radical — will matter constantly in this unit, especially when solving "
            "equations that mix the two notations.",
        ],
        "Rational exponents are simply radicals written in exponent form, and switching between the two "
        "notations lets you use whichever set of tools (root rules or exponent rules) is more convenient for a "
        "given problem.",
        "Identify $m$ (the power) and $n$ (the root) in $a^{m/n}$. Take the $n$th root of $a$ first, using small "
        "friendly numbers whenever possible, and then raise that result to the $m$ power. Flip to a reciprocal "
        "first if the exponent is negative.",
        solved(1, "Evaluate $8^{2/3}$.",
               ["The denominator, $3$, tells you to take a cube root; the numerator, $2$, tells you to square "
                "the result.",
                "Take the cube root first: $\\sqrt[3]8=2$.",
                "Raise that result to the power $2$: $2^2=4$."],
               "$4$", "", "Easy")
        + solved(2, "Evaluate $16^{3/4}$.",
                 ["The denominator, $4$, means take a fourth root; the numerator, $3$, means cube the result.",
                  "Take the fourth root first: $\\sqrt[4]{16}=2$.",
                  "Raise that result to the power $3$: $2^3=8$."],
                 "$8$", "", "Medium")
        + solved(3, "Evaluate $27^{-2/3}$.",
                 ["The negative exponent means take the reciprocal after evaluating the positive exponent.",
                  "Evaluate $27^{2/3}$ first: take the cube root, $\\sqrt[3]{27}=3$, then square it, $3^2=9$.",
                  "Apply the reciprocal for the negative sign: $27^{-2/3}=\\dfrac{1}{9}$."],
                 "$\\dfrac19$",
                 "Handle the negative sign last, after the root-then-power evaluation, to avoid sign confusion.",
                 "Hard"),
        ("Applying the wrong exponent to the wrong root",
         "In $a^{m/n}$, the denominator $n$ is the root and the numerator $m$ is the power. Swapping them — "
         "for example taking an $m$th root instead of an $n$th root — changes the answer completely."),
        ("Root on the bottom, power on top — take the root first",
         "Rewrite $a^{m/n}$ as $\\left(\\sqrt[n]{a}\\right)^m$, take the small, friendly root first, and only "
         "then raise that small result to the power."),
        ["I know that the denominator of a rational exponent tells me which root to take.",
         "I take the root before applying the power, so the numbers stay small and manageable.",
         "I handle a negative rational exponent by taking a reciprocal, either before or after evaluating."],
        6,
    )

    c3 = concept_block(
        "3. Simplifying radicals, including variables and absolute value",
        [
            "Simplifying a numeric radical means pulling out the largest possible perfect-power factor that "
            "matches the index. For a square root, look for the largest perfect-square factor; for a cube root, "
            "look for the largest perfect-cube factor, and so on.",
            "When variables are involved, the same idea applies to exponents: a factor like $x^{2}$ pulls out "
            "cleanly from under a square root, while $x^{3}$ does not pull out cleanly (it leaves one extra "
            "factor of $x$ under the radical).",
            "The trickiest part of this concept is deciding when an absolute value is required. Because the "
            "principal even-index root is always nonnegative, simplifying $\\sqrt{x^2}$ must produce $|x|$, "
            "not $x$, since $x$ itself could be negative while $\\sqrt{x^2}$ cannot be.",
            "However, if the simplified variable expression is itself guaranteed to be nonnegative — like "
            "$\\sqrt{x^4}=x^2$, where $x^2$ can never be negative regardless of the sign of $x$ — then no "
            "absolute value bars are needed, because the result is automatically nonnegative already.",
            "Odd-index roots never need absolute value bars, because an odd root can legitimately produce a "
            "negative output when the radicand is negative; there is no principal-root sign restriction to "
            "protect.",
        ],
        "Simplifying radicals with variables is mostly the same factoring skill as simplifying numeric radicals, "
        "with one extra layer: deciding whether the leftover variable expression could be negative, which "
        "determines whether absolute value bars are required.",
        "Split the radicand into perfect-power factors matching the index and leftover factors. Pull out the "
        "perfect-power part. If the index is even and the pulled-out variable expression could be negative on "
        "its own, wrap it in absolute value bars; otherwise leave it as is.",
        solved(1, "Simplify $\\sqrt{50}$.",
               ["Find the largest perfect-square factor of $50$: $50=25\\cdot2$.",
                "Split the radical: $\\sqrt{25}\\cdot\\sqrt2$.",
                "Simplify the perfect square: $5\\sqrt2$."],
               "$5\\sqrt2$", "", "Easy")
        + solved(2, "Simplify $\\sqrt{x^6}$.",
                 ["Rewrite $x^6=(x^3)^2$, a perfect square.",
                  "Taking the square root gives $|x^3|$, because $x^3$ can be negative on its own (for example, "
                  "when $x$ is negative), so the absolute value is required to guarantee a nonnegative result."],
                 "$|x^3|$", "", "Medium")
        + solved(3, "Simplify $\\sqrt{18x^4}$.",
                 ["Split the radicand into perfect-square and leftover pieces: $18x^4=9x^4\\cdot2$.",
                  "Take the square root of the perfect-square part: $\\sqrt{9x^4}=3x^2$.",
                  "Since $x^2$ is automatically nonnegative for any real $x$, no absolute value bars are "
                  "needed on that piece.",
                  "The remaining factor stays under the radical: $3x^2\\sqrt2$."],
                 "$3x^2\\sqrt2$",
                 "Compare this to $\\sqrt{x^6}=|x^3|$: the exponent on the pulled-out variable being even "
                 "(here, $2$) is exactly what removes the need for absolute value.", "Hard"),
        ("Forgetting absolute value when simplifying an even root of an even power variable",
         "$\\sqrt{x^2}$ equals $|x|$, not simply $x$, because the principal square root is never negative even "
         "when $x$ itself could be negative."),
        ("Even index and an odd leftover power means absolute value might be needed",
         "Whenever an even-index root simplifies a variable that ends up raised to an odd total power outside "
         "the radical, wrap that piece in absolute value bars unless the problem already guarantees the "
         "variable is nonnegative."),
        ["I pull out the largest perfect-power factor matching the index before doing anything else.",
         "I add absolute value bars only when the pulled-out variable expression could be negative on its own.",
         "I know that odd-index roots never need absolute value bars."],
        11,
    )

    c4 = concept_block(
        "4. Operations with radicals: adding, multiplying, and rationalizing",
        [
            "Radicals add and subtract exactly like like terms in polynomials: only radicals with the "
            "<strong>same index and same radicand</strong> can be combined, and you combine them by adding or "
            "subtracting their coefficients while leaving the radical part untouched.",
            "Before deciding whether two radicals are 'like,' simplify each one completely. Two radicals that "
            "look different at first — such as $\\sqrt8$ and $\\sqrt{18}$ — often become identical once fully "
            "simplified, revealing that they actually can combine.",
            "Multiplying radicals with the same index uses the rule $\\sqrt[n]{a}\\cdot\\sqrt[n]{b}=\\sqrt[n]{ab}$: "
            "multiply the radicands together under one radical, then simplify the result.",
            "A fraction with a radical left in the denominator is considered unsimplified. To "
            "<strong>rationalize</strong> a single-term radical denominator, multiply top and bottom by that "
            "same radical. To rationalize a two-term denominator like $\\sqrt3+\\sqrt2$ or $\\sqrt5-1$, multiply "
            "top and bottom by its <strong>conjugate</strong> (the same two terms with the middle sign flipped), "
            "which uses the difference-of-squares pattern to eliminate the radicals below the fraction bar.",
            "Rationalizing does not change the value of the expression — it only rewrites it in a preferred, "
            "cleaner form, the same way reducing a numeric fraction to lowest terms does not change its value.",
        ],
        "Radical arithmetic borrows directly from polynomial arithmetic: combining like radicals mirrors "
        "combining like terms, and rationalizing a denominator mirrors clearing a fraction, both aimed at "
        "producing one clean, standard final form.",
        "Simplify every radical completely first. Combine only radicals sharing the same index and radicand by "
        "adding coefficients. For multiplication, combine radicands under one radical and simplify. For "
        "rationalizing, multiply by the radical itself (one term) or by the conjugate (two terms) to clear the "
        "denominator.",
        solved(1, "Simplify $3\\sqrt2+5\\sqrt2$.",
               ["Both terms already have the same radical, $\\sqrt2$, so they are like radicals.",
                "Add the coefficients: $3+5=8$.",
                "The result is $8\\sqrt2$."],
               "$8\\sqrt2$", "", "Easy")
        + solved(2, "Multiply $\\sqrt3\\cdot\\sqrt{12}$.",
                 ["Combine the radicands under one radical: $\\sqrt{3\\cdot12}=\\sqrt{36}$.",
                  "Simplify the perfect square: $\\sqrt{36}=6$."],
                 "$6$", "", "Medium")
        + solved(3, "Rationalize $\\dfrac{1}{\\sqrt3+1}$.",
                 ["Identify the conjugate of the denominator, $\\sqrt3+1$, which is $\\sqrt3-1$.",
                  "Multiply top and bottom by that conjugate: $\\dfrac{1\\cdot(\\sqrt3-1)}{(\\sqrt3+1)(\\sqrt3-1)}$.",
                  "The denominator becomes a difference of squares: $(\\sqrt3)^2-1^2=3-1=2$.",
                  "The result is $\\dfrac{\\sqrt3-1}{2}$, with no radical left in the denominator."],
                 "$\\dfrac{\\sqrt3-1}{2}$", "", "Hard"),
        ("Combining unlike radicals as if they were like terms",
         "$\\sqrt2+\\sqrt3$ cannot be added into a single radical. Only radicals with the exact same index and "
         "radicand combine, just as only true like terms combine in polynomial addition."),
        ("Simplify first, then look for matching radicals",
         "Simplify every radical completely before adding or subtracting. Two radicals that look different at "
         "first often turn out to be identical once fully simplified, which is when they can finally combine."),
        ["I simplify every radical completely before trying to add or subtract them.",
         "I combine radicands under one radical when multiplying two radicals with the same index.",
         "I rationalize a two-term radical denominator by multiplying by its conjugate."],
        16,
    )

    c5 = concept_block(
        "5. Solving radical equations and checking for extraneous solutions",
        [
            "A radical equation contains the variable inside a radical, such as $\\sqrt{x+3}=4$. The standard "
            "strategy is to isolate the radical completely on one side of the equation, then raise both sides to "
            "a power matching the index to eliminate the radical.",
            "Raising both sides to an even power (like squaring) is a legal algebraic move, but unlike most "
            "algebra steps, it is not guaranteed to produce an equivalent equation — it can introduce new "
            "solutions that satisfy the squared equation without satisfying the original radical equation.",
            "If more than one radical appears, you may need to isolate and square more than once: isolate one "
            "radical, square, simplify, and if a radical remains, isolate it and square again before finishing "
            "with ordinary algebra.",
            "After solving the polynomial equation that results from squaring, every candidate solution must be "
            "substituted back into the <strong>original</strong> radical equation — not the squared version — to "
            "confirm both sides actually match. Any candidate that fails this check is extraneous and must be "
            "discarded.",
            "It also helps to note the implied domain before squaring: if the equation is $\\sqrt{\\text{stuff}}"
            "=x-2$, the right-hand side must be nonnegative for a solution to be possible, since a principal "
            "square root can never equal a negative number.",
        ],
        "Squaring both sides of a radical equation is a powerful tool for removing a radical, but it can create "
        "solutions that never belonged to the original equation. Verifying every candidate in the untouched "
        "original equation is what makes the final answer trustworthy.",
        "Isolate the radical completely. Raise both sides to the matching power. Solve the resulting equation. "
        "Substitute every candidate back into the original radical equation and discard anything that fails.",
        solved(1, "Solve $\\sqrt{x+3}=4$.",
               ["The radical is already isolated.",
                "Square both sides: $x+3=16$.",
                "Solve: $x=13$.",
                "Check: $\\sqrt{13+3}=\\sqrt{16}=4$, which matches, so the solution is valid."],
               "$x=13$", "", "Easy")
        + solved(2, "Solve $\\sqrt{2x-1}=x-2$.",
                 ["The right side must be nonnegative for a solution to exist, so the domain requires $x\\ge2$.",
                  "Square both sides: $2x-1=(x-2)^2=x^2-4x+4$.",
                  "Simplify: $0=x^2-6x+5=(x-1)(x-5)$, so $x=1$ or $x=5$.",
                  "Check $x=1$ against the domain $x\\ge2$: it fails, so it is extraneous.",
                  "Check $x=5$: $\\sqrt{9}=3$ and $5-2=3$, which matches, so it is valid."],
                 "$x=5$",
                 "The domain check ($x\\ge2$) catches the extraneous root before even substituting back in.",
                 "Medium")
        + solved(3, "Solve $\\sqrt{x+7}-\\sqrt{x}=1$.",
                 ["Isolate one radical: $\\sqrt{x+7}=1+\\sqrt{x}$.",
                  "Square both sides: $x+7=1+2\\sqrt{x}+x$.",
                  "Simplify: $7=1+2\\sqrt{x} \\Rightarrow 6=2\\sqrt{x} \\Rightarrow \\sqrt{x}=3$.",
                  "Square again: $x=9$.",
                  "Check: $\\sqrt{16}-\\sqrt9=4-3=1$, which matches, so the solution is valid."],
                 "$x=9$",
                 "This problem needed two separate isolate-and-square rounds because two radicals were present.",
                 "Hard"),
        ("Squaring both sides and skipping the check",
         "Squaring both sides of a radical equation can introduce extraneous solutions because squaring "
         "destroys sign information. Every candidate must be substituted back into the original, unsquared "
         "equation before it is accepted."),
        ("Isolate the radical, then square, then verify",
         "Get the radical completely alone on one side before squaring, and after solving, substitute every "
         "candidate back into the original radical equation before accepting it."),
        ["I isolate the radical completely before squaring either side.",
         "I check every candidate solution in the original radical equation, not just the squared version.",
         "I note the implied domain (like $x-2\\ge0$) before squaring, so I can spot extraneous roots early."],
        21,
    )

    c6 = concept_block(
        "6. Graphing square-root and cube-root functions and their transformations",
        [
            "The parent square-root function $y=\\sqrt{x}$ starts at the point $(0,0)$ and only exists for "
            "$x\\ge0$, since the radicand cannot be negative. Its graph curves upward and to the right, growing "
            "more and more slowly as $x$ increases.",
            "The parent cube-root function $y=\\sqrt[3]{x}$ behaves very differently: because odd roots accept "
            "any real number, this graph stretches across every real $x$-value, passing through the origin with "
            "an S-shaped curve that flattens briefly at $(0,0)$.",
            "Transformations of these parent graphs follow the same rules as every other function family you "
            "have studied: $y=\\sqrt{x-h}+k$ shifts the starting point of the square-root graph to $(h,k)$, and "
            "$y=\\sqrt[3]{x-h}+k$ shifts the inflection point of the cube-root graph to $(h,k)$.",
            "A negative sign in front of the radical, as in $y=-\\sqrt{x}$, reflects the graph over the "
            "$x$-axis, flipping its usual nonnegative output into a nonpositive one. A negative sign inside the "
            "radicand, as in $y=\\sqrt{-x}$, reflects the graph over the $y$-axis instead, changing which side "
            "of the starting point the graph exists on.",
            "To sketch any transformed radical graph quickly, first locate the shifted starting or inflection "
            "point, then plug in two or three convenient $x$-values near that point to see which direction and "
            "how steeply the curve moves.",
        ],
        "Radical graphs are restricted or reshaped versions of two simple parent curves, and every "
        "transformation you already know from linear and quadratic graphing — shifts, reflections, stretches — "
        "applies here in exactly the same way.",
        "Identify the parent function (square root or cube root). Find the shifted starting or inflection point "
        "from the horizontal and vertical shift values. Determine whether there is a reflection from a negative "
        "sign, then plot two or three additional points to complete the sketch.",
        solved(1, "Describe the graph of $y=\\sqrt{x-2}+3$.",
               ["Compare to the parent form $y=\\sqrt{x-h}+k$: here $h=2$ and $k=3$.",
                "The starting point shifts from $(0,0)$ to $(2,3)$.",
                "The domain becomes $x\\ge2$ and the range becomes $y\\ge3$."],
               "Starting point $(2,3)$, domain $x\\ge2$, range $y\\ge3$", "", "Easy")
        + solved(2, "Describe the graph of $y=-\\sqrt{x}$.",
                 ["The negative sign is outside the radical, so this reflects the parent graph over the "
                  "$x$-axis.",
                  "The domain stays the same as the parent graph, $x\\ge0$, since the radicand was not changed.",
                  "The range flips from $y\\ge0$ to $y\\le0$."],
                 "Domain $x\\ge0$, range $y\\le0$ (reflection of the parent graph over the $x$-axis)",
                 "", "Medium")
        + solved(3, "Describe the graph of $y=\\sqrt[3]{x+1}-2$.",
                 ["Compare to the parent form $y=\\sqrt[3]{x-h}+k$: here $h=-1$ and $k=-2$.",
                  "The inflection point shifts from $(0,0)$ to $(-1,-2)$.",
                  "Because this is a cube-root graph, the domain and range remain all real numbers even after "
                  "the shift, unlike a square-root graph."],
                 "Inflection point $(-1,-2)$, domain all reals, range all reals",
                 "Cube-root graphs never have a restricted domain the way square-root graphs do.", "Hard"),
        ("Forgetting that square-root graphs start rather than extend infinitely in both directions",
         "The parent graph $y=\\sqrt{x}$ only exists for $x\\ge0$, so shifts change where that starting point "
         "sits rather than producing a graph over all real numbers the way a cube-root graph does."),
        ("Find the starting point first, then plot two more points",
         "Locate the domain-restricted starting point (or the inflection point for cube-root graphs) from the "
         "horizontal and vertical shifts, then plug in two convenient $x$-values to sketch the curve's "
         "direction."),
        ["I can find the shifted starting point of a square-root graph from $h$ and $k$.",
         "I know cube-root graphs have domain and range of all real numbers, unlike square-root graphs.",
         "I can tell whether a negative sign reflects a radical graph over the $x$-axis or the $y$-axis."],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        AUDIENCE,
        [
            "Evaluate nth roots and understand the principal root, including even vs. odd index behavior",
            "Convert between rational exponents and radical notation, and evaluate both forms",
            "Simplify radicals with variables, using absolute value correctly when the index is even",
            "Add, subtract, multiply, and rationalize radical expressions",
            "Solve radical equations and identify extraneous solutions",
            "Graph square-root and cube-root functions and their transformations",
        ],
        body,
        practice_slots(31, 50),
    )
    return title, description, content, _u6_questions()


# =====================================================================================
# UNIT 7: Exponential & Logarithmic Functions
# =====================================================================================

def _u7_questions():
    qs = []

    # Concept 1 — exponential growth/decay models (1-5)
    qs.append(mq("For $P(t)=200(1.1)^t$, find $P(2)$.", "242",
                 "$P(2)=200(1.1)^2=200(1.21)=242$.", 1, distractors=["220", "240", "244"]))
    qs.append(mq("For $A(t)=1000(0.5)^t$, find $A(2)$.", "250",
                 "$A(2)=1000(0.5)^2=1000(0.25)=250$.", 2, distractors=["500", "125", "200"]))
    qs.append(mq("For $y=100(1.05)^x$, is this growth or decay, and by what percent?", "Growth, 5%",
                 "Since the base $1.05>1$, this is growth, and the rate is $1.05-1=0.05=5\\%$.",
                 3, distractors=["Decay, 5%", "Growth, 105%", "Decay, 95%"]))
    qs.append(mq("For $y=80(0.75)^x$, is this growth or decay, and by what percent?", "Decay, 25%",
                 "Since the base $0.75<1$, this is decay, and the rate is $1-0.75=0.25=25\\%$.",
                 4, distractors=["Growth, 25%", "Decay, 75%", "Growth, 75%"]))
    qs.append(mq("A population starts at 300 and grows 20% per year. Write the model $P(t)$.",
                 "P(t)=300(1.2)^t",
                 "Growth factor is $1+0.20=1.2$, so $P(t)=300(1.2)^t$.",
                 5, distractors=["P(t)=300(0.2)^t", "P(t)=300(1.2)t", "P(t)=300+1.2t"]))

    # Concept 2 — properties of exponents review (6-10)
    qs.append(mq("Solve $2^x=16$.", "x=4",
                 "$16=2^4$, so $x=4$.", 6, distractors=["x=8", "x=2", "x=3"]))
    qs.append(mq("Solve $5^x=125$.", "x=3",
                 "$125=5^3$, so $x=3$.", 7, distractors=["x=5", "x=2", "x=25"]))
    qs.append(mq("Solve $3^{2x}=81$.", "x=2",
                 "$81=3^4$, so $2x=4 \\Rightarrow x=2$.", 8, distractors=["x=4", "x=1", "x=8"]))
    qs.append(mq("Solve $9^x=27$.", "x=3/2",
                 "Rewrite with base $3$: $9^x=3^{2x}$ and $27=3^3$, so $2x=3 \\Rightarrow x=\\dfrac32$.",
                 9, distractors=["x=3", "x=2/3", "x=9/2"]))
    qs.append(mq("Solve $2^{x+3}=4^x$.", "x=3",
                 "Rewrite with base $2$: $4^x=2^{2x}$, so $x+3=2x \\Rightarrow x=3$.",
                 10, distractors=["x=6", "x=1", "x=-3"]))

    # Concept 3 — definition of logarithms (11-15)
    qs.append(mq("Convert $10^3=1000$ to logarithmic form.", "log_10(1000)=3",
                 "The base stays the base, the exponent becomes the log's value: $\\log_{10}1000=3$.",
                 11, distractors=["log_1000(10)=3", "log_10(3)=1000", "log_3(10)=1000"]))
    qs.append(mq("Convert $\\log_2 8=3$ to exponential form.", "2^3=8",
                 "The base stays the base, the log's value becomes the exponent: $2^3=8$.",
                 12, distractors=["8^3=2", "3^2=8", "2^8=3"]))
    qs.append(mq("Evaluate $\\log_4 64$.", "3",
                 "Since $4^3=64$, $\\log_4 64=3$.", 13, distractors=["4", "16", "2"]))
    qs.append(mq("Evaluate $\\log_6 1$.", "0",
                 "Any nonzero base raised to the $0$ power is $1$, so $\\log_6 1=0$.",
                 14, distractors=["1", "6", "-1"]))
    qs.append(mq("Evaluate $\\log_2\\left(\\dfrac18\\right)$.", "-3",
                 "Since $2^{-3}=\\dfrac18$, $\\log_2\\dfrac18=-3$.", 15, distractors=["3", "-8", "1/3"]))

    # Concept 4 — log properties (16-20)
    qs.append(mq("Evaluate $\\log_2 4+\\log_2 8$.", "5",
                 "Use the product rule: $\\log_2(4\\cdot8)=\\log_2 32=5$.", 16, distractors=["6", "12", "32"]))
    qs.append(mq("Evaluate $\\log_3 27-\\log_3 3$.", "2",
                 "Use the quotient rule: $\\log_3\\dfrac{27}{3}=\\log_3 9=2$.", 17, distractors=["3", "9", "1"]))
    qs.append(mq("Evaluate $2\\log_2 8$.", "6",
                 "Use the power rule: $2\\log_2 8=2(3)=6$.", 18, distractors=["3", "16", "8"]))
    qs.append(mq("Evaluate $\\log_{10}100+\\log_{10}10$.", "3",
                 "Use the product rule: $\\log_{10}(100\\cdot10)=\\log_{10}1000=3$.",
                 19, distractors=["2", "1000", "20"]))
    qs.append(mq("Evaluate $\\log_4 64-\\log_4 4$.", "2",
                 "Use the quotient rule: $\\log_4\\dfrac{64}{4}=\\log_4 16=2$.", 20, distractors=["3", "16", "1"]))

    # Concept 5 — solving exponential & log equations (21-25)
    qs.append(mq("Solve $\\log_5 x=3$.", "x=125",
                 "Convert to exponential form: $x=5^3=125$.", 21, distractors=["x=15", "x=25", "x=8"]))
    qs.append(mq("Solve $\\log_2(x+3)=4$.", "x=13",
                 "Convert to exponential form: $x+3=2^4=16 \\Rightarrow x=13$.",
                 22, distractors=["x=16", "x=5", "x=11"]))
    qs.append(mq("Solve $\\log_4(2x)=2$.", "x=8",
                 "Convert to exponential form: $2x=4^2=16 \\Rightarrow x=8$.",
                 23, distractors=["x=16", "x=4", "x=6"]))
    qs.append(mq("Solve $3^x=20$ using logs (round to the nearest hundredth).", "2.73",
                 "Take $\\log$ of both sides: $x=\\dfrac{\\log20}{\\log3}\\approx2.73$.",
                 24, distractors=["2.50", "3.00", "1.82"]))
    qs.append(mq("Solve $\\log(x)+\\log(x-3)=1$ (base 10).", "x=5",
                 "Domain requires $x>3$. Combine: $\\log(x(x-3))=1 \\Rightarrow x(x-3)=10 \\Rightarrow "
                 "x^2-3x-10=0 \\Rightarrow (x-5)(x+2)=0$. Since $x=-2$ fails the domain, $x=5$ is the only "
                 "valid solution.",
                 25, distractors=["x=-2", "x=10", "x=2"]))

    # Concept 6 — change of base & applications (26-30)
    qs.append(mq("Use change of base to evaluate $\\log_3 50$ (round to 2 decimal places).", "3.56",
                 "$\\log_3 50=\\dfrac{\\log 50}{\\log 3}\\approx\\dfrac{1.699}{0.477}\\approx3.56$.",
                 26, distractors=["3.91", "2.56", "16.67"]))
    qs.append(mq("Compound interest: $P=500$, $r=0.04$, $n=1$, $t=5$. Find $A$ (nearest cent).", "608.33",
                 "$A=500(1.04)^5\\approx500(1.2166529)\\approx608.33$.",
                 27, distractors=["600.00", "520.00", "625.00"]))
    qs.append(mq("A substance with half-life 3 hours starts at 200 mg. Find the amount after 9 hours.", "25",
                 "Nine hours is $9/3=3$ half-lives: $200\\left(\\dfrac12\\right)^3=200\\left(\\dfrac18\\right)=25$.",
                 28, distractors=["50", "100", "12.5"]))
    qs.append(mq("If $[H^+]=10^{-4}$, find the pH using $\\text{pH}=-\\log[H^+]$.", "4",
                 "$\\text{pH}=-\\log(10^{-4})=4$.", 29, distractors=["-4", "10", "0.4"]))
    qs.append(mq("Continuous growth $A=A_0e^{rt}$: $A_0=100$, $r=0.03$, $t=10$. Find $A$ to the nearest whole "
                 "number.", "135",
                 "$A=100e^{0.3}\\approx100(1.34986)\\approx135$.",
                 30, distractors=["130", "103", "300"]))

    finale = []

    # Easy 31-45
    for n in (1, 2, 3, 4, 5):
        finale.append(mq(f"Evaluate $2^{n}$.", str(2 ** n),
                         f"$2^{n}={2**n}$.", 0))
    for base, exp, val in [(2, 3, 8), (3, 2, 9), (5, 2, 25), (10, 3, 1000), (4, 3, 64)]:
        finale.append(mq(
            f"Since ${base}^{exp}={val}$, what is $\\log_{{{base}}}{val}$?", str(exp),
            f"By definition, $\\log_{{{base}}}{val}={exp}$ because ${base}^{exp}={val}$.",
            0, distractors=[str(base), str(val), str(exp + 1)]))
    for base, val, ans in [(2, 8, 3), (3, 9, 2), (5, 125, 3), (10, 100, 2), (4, 16, 2)]:
        cand_nums = [val, base, ans + 1, ans + 2, ans - 1 if ans > 1 else ans + 4]
        dis = []
        for c in cand_nums:
            s = f"x={c}"
            if c != ans and s not in dis:
                dis.append(s)
            if len(dis) == 3:
                break
        finale.append(mq(f"Solve ${base}^x={val}$.", f"x={ans}",
                         f"${val}={base}^{ans}$, so $x={ans}$.", 0, distractors=dis))

    # Medium 46-60
    for a, b, prod, ans in [(4, 16, 64, 3), (9, 3, 27, 3), (5, 25, 125, 3), (8, 2, 16, 4), (10, 10, 100, 2)]:
        base = {64: 2, 27: 3, 125: 5, 16: 2, 100: 10}[prod]
        finale.append(mq(
            f"Evaluate $\\log_{{{base}}}{a}+\\log_{{{base}}}{b}$.", str(ans),
            f"Use the product rule: $\\log_{{{base}}}({a}\\cdot{b})=\\log_{{{base}}}{prod}={ans}$.",
            0, distractors=[str(ans + 1), str(a + b), str(prod)]))
    for text, ans, expl, dis in [
        ("Solve $2^{x+1}=32$.", "x=4", "$32=2^5$, so $x+1=5 \\Rightarrow x=4$.", ["x=5", "x=3", "x=16"]),
        ("Solve $5^{x-1}=25$.", "x=3", "$25=5^2$, so $x-1=2 \\Rightarrow x=3$.", ["x=2", "x=1", "x=5"]),
        ("Solve $2^{3x}=64$.", "x=2", "$64=2^6$, so $3x=6 \\Rightarrow x=2$.", ["x=6", "x=3", "x=1"]),
        ("Solve $4^x=32$.", "x=5/2",
         "Rewrite with base $2$: $4^x=2^{2x}$ and $32=2^5$, so $2x=5 \\Rightarrow x=\\dfrac52$.",
         ["x=8", "x=2", "x=4"]),
        ("Solve $9^x=27$ (rewrite with base 3).", "x=3/2",
         "$9^x=3^{2x}$ and $27=3^3$, so $2x=3 \\Rightarrow x=\\dfrac32$.", ["x=3", "x=2/3", "x=1"]),
    ]:
        finale.append(mq(text, ans, expl, 0, distractors=dis))
    for text, ans, expl, dis in [
        ("Solve $\\log_2 x=6$.", "x=64", "Convert: $x=2^6=64$.", ["x=12", "x=32", "x=36"]),
        ("Solve $\\log_3 x=4$.", "x=81", "Convert: $x=3^4=81$.", ["x=12", "x=64", "x=27"]),
        ("Solve $\\log x=2$ (base 10).", "x=100", "Convert: $x=10^2=100$.", ["x=20", "x=10", "x=200"]),
        ("Solve $\\log_5 x=0$.", "x=1", "Convert: $x=5^0=1$.", ["x=0", "x=5", "x=-1"]),
        ("Solve $\\log_4 x=-1$.", "x=1/4", "Convert: $x=4^{-1}=\\dfrac14$.", ["x=-4", "x=4", "x=1/16"]),
    ]:
        finale.append(mq(text, ans, expl, 0, distractors=dis))

    # Hard 61-70
    for text, ans, expl, dis in [
        ("Solve $\\log_2(x+1)+\\log_2(x-1)=3$.", "x=3",
         "Domain requires $x>1$. Combine: $\\log_2((x+1)(x-1))=3 \\Rightarrow x^2-1=8 \\Rightarrow x^2=9 "
         "\\Rightarrow x=3$ (rejecting $x=-3$, which fails the domain).",
         ["x=-3", "x=9", "x=8"]),
        ("Solve $2^{3x-1}=4^{x+2}$.", "x=5",
         "Rewrite the right side: $4^{x+2}=2^{2(x+2)}=2^{2x+4}$. Set exponents equal: $3x-1=2x+4 "
         "\\Rightarrow x=5$.",
         ["x=3", "x=-5", "x=2"]),
        ("Solve $\\log_4 x+\\log_4(x-6)=2$.", "x=8",
         "Domain requires $x>6$. Combine: $\\log_4(x(x-6))=2 \\Rightarrow x^2-6x=16 \\Rightarrow "
         "x^2-6x-16=0 \\Rightarrow (x-8)(x+2)=0 \\Rightarrow x=8$ (rejecting $x=-2$).",
         ["x=-2", "x=16", "x=4"]),
        ("An investment grows by $A=P(1+r)^t$ with $P=1000$, $r=0.1$, and $A=1331$. Find $t$.", "3",
         "$1.1^t=1.331$. Since $1.1^3=1.331$, $t=3$ years.",
         ["2", "4", "1.331"]),
        ("A substance decays by half-life. Starting at 100, after 4 hours it is 25. Find the half-life "
         "(hours).", "2",
         "$25=100(1/2)^{4/h} \\Rightarrow \\dfrac14=(1/2)^{4/h} \\Rightarrow (1/2)^2=(1/2)^{4/h} "
         "\\Rightarrow 2=4/h \\Rightarrow h=2$.",
         ["4", "1", "8"]),
        ("Solve $\\log_x 81=4$ for a positive base $x$.", "x=3",
         "Convert: $x^4=81 \\Rightarrow x=81^{1/4}=3$.",
         ["x=9", "x=4", "x=81"]),
        ("Simplify $\\log_2 32-\\log_2 4+\\log_2 2$.", "4",
         "Evaluate each term: $5-2+1=4$.",
         ["3", "5", "6"]),
        ("Solve $e^{2x}=20$ (round to the nearest hundredth).", "1.50",
         "Take $\\ln$ of both sides: $2x=\\ln20\\approx2.9957 \\Rightarrow x\\approx1.50$.",
         ["1.33", "3.00", "2.99"]),
        ("If pH $=3$, find $[H^+]$ using $\\text{pH}=-\\log[H^+]$.", "10^-3",
         "Solve for the concentration: $[H^+]=10^{-\\text{pH}}=10^{-3}$.",
         ["10^3", "3", "-3"]),
        ("An investment modeled by $y=250(1.15)^t$ is evaluated at $t=4$ years. Find the value to the "
         "nearest dollar.", "437",
         "$250(1.15)^4=250(1.74900625)\\approx437.25\\approx437$.",
         ["400", "460", "375"]),
    ]:
        finale.append(mq(text, ans, expl, 0, distractors=dis))

    # Stretch 71-80
    for text, ans, expl, dis in [
        ("Solve $4^x-2^x-2=0$.", "x=1",
         "Let $u=2^x$: $u^2-u-2=0 \\Rightarrow (u-2)(u+1)=0 \\Rightarrow u=2$ (rejecting the negative root). "
         "Then $2^x=2 \\Rightarrow x=1$.",
         ["x=2", "x=-1", "x=0"]),
        ("Solve $\\log_2 x+\\log_2(x+2)=3$.", "x=2",
         "Domain requires $x>0$. Combine: $\\log_2(x(x+2))=3 \\Rightarrow x^2+2x=8 \\Rightarrow "
         "x^2+2x-8=0 \\Rightarrow (x+4)(x-2)=0 \\Rightarrow x=2$ (rejecting $x=-4$).",
         ["x=-4", "x=4", "x=8"]),
        ("Evaluate $\\log_8 32$ exactly (as a fraction).", "5/3",
         "Rewrite both numbers as powers of $2$: $8=2^3$, $32=2^5$, so $\\log_8 32=\\dfrac{5}{3}$.",
         ["3/5", "5/8", "8/5"]),
        ("Solve $9^x=3^{x+3}\\cdot3^{0}$ (i.e., $9^x=3^{x+3}$).", "x=3",
         "Rewrite the left side: $9^x=3^{2x}$. Set exponents equal: $2x=x+3 \\Rightarrow x=3$.",
         ["x=6", "x=1", "x=9"]),
        ("Find the continuous interest rate $r$ so that money doubles in 10 years, using $A=A_0e^{rt}$ "
         "(round to 4 decimal places).", "0.0693",
         "$2=e^{10r} \\Rightarrow 10r=\\ln2 \\Rightarrow r=\\dfrac{\\ln2}{10}\\approx0.0693$.",
         ["0.6931", "0.0301", "0.6900"]),
        ("Solve $\\log_3(x^2)=4$.", "x=9 or x=-9",
         "Convert: $x^2=3^4=81 \\Rightarrow x=\\pm9$, and both satisfy the domain $x\\neq0$.",
         ["x=9", "x=81", "x=3"]),
        ("If $5^a=25$ and $5^b=125$, find $a+b$.", "5",
         "$a=2$ and $b=3$, so $a+b=5$.",
         ["6", "125", "8"]),
        ("Solve $\\log_2(3x-1)=\\log_2(x+5)$.", "x=3",
         "Equal logs with the same base mean equal arguments: $3x-1=x+5 \\Rightarrow 2x=6 \\Rightarrow x=3$. "
         "Both arguments are positive, so the domain checks out.",
         ["x=5", "x=6", "x=-3"]),
        ("A substance decays continuously with half-life 10 years, using $A=A_0e^{-kt}$. Find $k$ (round to "
         "4 decimal places).", "0.0693",
         "$\\dfrac12=e^{-10k} \\Rightarrow -10k=\\ln\\dfrac12=-\\ln2 \\Rightarrow k=\\dfrac{\\ln2}{10}"
         "\\approx0.0693$.",
         ["0.6931", "0.1000", "0.3010"]),
        ("Evaluate $\\log_{1/2}8$ without a calculator.", "-3",
         "Since $\\left(\\dfrac12\\right)^{-3}=8$, $\\log_{1/2}8=-3$.",
         ["3", "-8", "8"]),
    ]:
        finale.append(mq(text, ans, expl, 0, distractors=dis))

    qs.extend(finale[:50])
    return _fill80(qs)


def build_unit7():
    title = "Algebra 2 Unit 7: Exponential & Logarithmic Functions"
    description = (
        "Deep, patient coverage of exponential and logarithmic functions for grade 10 Algebra 2 — growth and "
        "decay models, exponent-rule review for solving, the definition of a logarithm, log properties, solving "
        "exponential and log equations, and change of base with interest, half-life, and pH-style applications."
    )

    c1 = concept_block(
        "1. Exponential growth and decay models: $y=a\\cdot b^x$",
        [
            "An exponential function has the form $y=a\\cdot b^x$, where $a$ is the starting value (at $x=0$) "
            "and $b$ is the growth or decay factor. Unlike a linear function, which adds the same amount every "
            "step, an exponential function multiplies by the same factor every step, which is why it can grow "
            "(or shrink) so quickly.",
            "When $b>1$, the function models <strong>growth</strong>: quantities like population, investments, "
            "or bacteria colonies that increase by a repeated percentage. When $0<b<1$, the function models "
            "<strong>decay</strong>: quantities like radioactive substances, depreciating value, or cooling "
            "temperatures that decrease by a repeated percentage.",
            "It is essential to separate the growth <strong>factor</strong>, $b$, from the growth "
            "<strong>rate</strong>, which is a percentage. If a population grows by $8\\%$ per year, the factor "
            "is $b=1+0.08=1.08$, not $8$ or $0.08$ by itself. If a substance decays by $8\\%$ per year, the "
            "factor is $b=1-0.08=0.92$.",
            "Evaluating these models is a direct substitution problem once the model is written correctly: plug "
            "in the given value of $x$ (often representing time), compute the power, and multiply by $a$.",
            "Reading a model correctly also means being able to state, in words, whether it represents growth or "
            "decay and by what percent, simply by inspecting whether $b$ is greater than or less than $1$ and "
            "computing $b-1$ or $1-b$ as appropriate.",
        ],
        "Exponential models describe an enormous range of real phenomena — population, money, radioactive "
        "decay, viral spread — because repeated percentage change, not repeated fixed change, is how those "
        "quantities actually behave in the real world.",
        "Identify $a$ (starting value) and $b$ (growth or decay factor) from the given rate. If the rate is a "
        "growth percent $r$, use $b=1+r$; if it is a decay percent $r$, use $b=1-r$. Substitute the given "
        "$x$-value and compute.",
        solved(1, "For $P(t)=500(1.08)^t$, find $P(3)$ (round to the nearest whole number).",
               ["Substitute $t=3$: $P(3)=500(1.08)^3$.",
                "Compute the power: $1.08^3\\approx1.259712$.",
                "Multiply: $500\\times1.259712\\approx629.86$.",
                "Round to the nearest whole number: $630$."],
               "$630$", "", "Easy")
        + solved(2, "A population of 400 decays by 15% per year. Write the model and find the population "
                    "after 5 years (nearest whole number).",
                 ["A $15\\%$ decay means the factor is $b=1-0.15=0.85$.",
                  "The model is $P(t)=400(0.85)^t$.",
                  "Substitute $t=5$: $P(5)=400(0.85)^5$.",
                  "Compute the power: $0.85^5\\approx0.4437$.",
                  "Multiply: $400\\times0.4437\\approx177.5$, which rounds to $178$."],
                 "$178$", "", "Medium")
        + solved(3, "An investment of $2000$ grows at $6\\%$ annually. In which year does the model first "
                    "predict the investment exceeds $3000$ (test whole years)?",
                 ["The model is $A(t)=2000(1.06)^t$.",
                  "Test $t=7$: $A(7)=2000(1.06)^7\\approx2000(1.5036)\\approx3007$, which exceeds $3000$.",
                  "Test $t=6$: $A(6)=2000(1.06)^6\\approx2000(1.4185)\\approx2837$, which does not yet exceed "
                  "$3000$.",
                  "So the investment first exceeds $3000$ during year $7$."],
                 "Year $7$",
                 "This kind of testing previews the log-equation solving method from later in the unit, which "
                 "finds the exact crossing time instead of testing whole years.", "Hard"),
        ("Confusing the growth factor with the growth rate",
         "In $y=a\\cdot b^x$, $b$ is the growth factor (like $1.08$), not the percent rate. The rate is $b-1$ "
         "expressed as a percent, and mixing the two produces answers off by roughly a factor of 100."),
        ("Write rate, then factor, then plug in $t$",
         "Convert a stated percent rate $r$ into the growth factor $b=1+r$ (growth) or $b=1-r$ (decay) before "
         "writing the model, and substitute the value of $t$ last, after the model is fully built."),
        ["I can convert a stated percent growth or decay rate into the correct factor $b$.",
         "I substitute the given $x$-value only after the model $y=a\\cdot b^x$ is completely written.",
         "I can tell whether a given model represents growth or decay just by comparing $b$ to $1$."],
        1,
    )

    c2 = concept_block(
        "2. Properties of exponents review, applied to solving equations",
        [
            "Solving an exponential equation like $2^x=32$ or $4^{x+1}=8^x$ almost always starts with rewriting "
            "every term so that both sides use the <strong>same base</strong>. Once both sides share a base, the "
            "exponents themselves must be equal, turning the problem into an ordinary linear (or occasionally "
            "quadratic) equation.",
            "Rewriting to a common base uses the exponent rules from earlier in Algebra 2: recognizing that "
            "$4=2^2$, $8=2^3$, $9=3^2$, $16=2^4$, and similar relationships, and then applying the power-of-a-"
            "power rule, $(a^m)^n=a^{mn}$, to rewrite the whole expression.",
            "A common mistake is rewriting the base correctly but forgetting to distribute the new exponent "
            "across an existing exponent expression — for example, $4^{x+1}$ becomes $2^{2(x+1)}$, not "
            "$2^{2x+1}$, because the entire exponent $(x+1)$ must be multiplied by $2$, not just the $x$ term.",
            "Once both sides are written with the same base, drop the base entirely and set the exponents equal "
            "to each other, then solve that simpler equation using standard linear or quadratic techniques.",
            "This method only works when a common base is easy to find. When the numbers involved are not "
            "clean powers of the same base — like solving $3^x=20$ — you will need logarithms instead, which is "
            "covered later in this unit.",
        ],
        "Exponential equations become simple once both sides share a base, because exponential functions are "
        "one-to-one: equal outputs from the same base force equal exponents, with no other possibilities to "
        "consider.",
        "Rewrite every term so both sides use the same base, distributing carefully across any existing "
        "exponent expression. Set the exponents equal to each other. Solve the resulting equation using "
        "ordinary algebra.",
        solved(1, "Solve $2^x=32$.",
               ["Rewrite $32$ as a power of $2$: $32=2^5$.",
                "Since both sides share base $2$, set the exponents equal: $x=5$."],
               "$x=5$", "", "Easy")
        + solved(2, "Solve $3^{2x}=27$.",
                 ["Rewrite $27$ as a power of $3$: $27=3^3$.",
                  "Since both sides share base $3$, set the exponents equal: $2x=3$.",
                  "Solve: $x=\\dfrac32$."],
                 "$x=\\dfrac32$", "", "Medium")
        + solved(3, "Solve $4^{x+1}=8^x$.",
                 ["Rewrite both sides with base $2$: $4^{x+1}=(2^2)^{x+1}=2^{2(x+1)}=2^{2x+2}$, and "
                  "$8^x=(2^3)^x=2^{3x}$.",
                  "Since both sides now share base $2$, set the exponents equal: $2x+2=3x$.",
                  "Solve: $2=x$, so $x=2$."],
                 "$x=2$",
                 "Distributing the outer exponent across $(x+1)$ before dropping the base is essential here.",
                 "Hard"),
        ("Adding exponents when bases are different sizes of the same base",
         "Rewriting $4^{x}$ as $2^{2x}$ requires multiplying the exponent by the power used to rewrite the "
         "base. Copying the exponent over unchanged, as in treating $4^x$ like $2^x$, produces a wrong "
         "equation."),
        ("Rewrite every side with the same base first",
         "Before comparing exponents, rewrite both sides of an exponential equation as powers of the same base, "
         "distributing carefully across any parentheses, then set the exponents equal."),
        ["I rewrite both sides of an exponential equation using the same base before comparing exponents.",
         "I distribute an outer exponent across an entire expression like $(x+1)$, not just part of it.",
         "I recognize when a common base is not available and logarithms will be needed instead."],
        6,
    )

    c3 = concept_block(
        "3. The definition of a logarithm and converting between exponential and log form",
        [
            "A logarithm answers the question: 'to what power must the base be raised to produce this number?' "
            "The statement $\\log_b v=n$ means exactly the same thing as the exponential statement $b^n=v$ — "
            "they are two different notations for the identical relationship between $b$, $n$, and $v$.",
            "In $\\log_b v=n$, the subscript $b$ is the <strong>base</strong>, $v$ is the <strong>argument</strong> "
            "(the number you are taking the log of), and $n$ is the <strong>exponent</strong> that the "
            "statement is solving for. Keeping these three roles straight is the entire foundation of working "
            "with logarithms.",
            "Converting from exponential form to log form, or log form to exponential form, is purely a "
            "rewriting exercise: identify the base, the exponent, and the result in whichever form you are "
            "given, then place those same three numbers into the matching positions of the other form.",
            "Evaluating a logarithm like $\\log_5 125$ means asking 'five to what power gives 125?' Since "
            "$5^3=125$, the answer is $3$. This mental habit — restating the log as a question about the base "
            "— is faster and more reliable than memorizing a formula.",
            "Two special logarithm values are worth memorizing directly: $\\log_b 1=0$ for any valid base "
            "(since $b^0=1$), and $\\log_b b=1$ for any valid base (since $b^1=b$).",
        ],
        "Logarithms are not a new operation — they are exponents in disguise, asking the reverse question of "
        "exponentiation. Every log statement can be rewritten as an exponential statement, and switching "
        "between the two forms is the key skill of this concept.",
        "Identify the three roles — base, exponent, argument — in whichever form (exponential or log) you are "
        "given. Rewrite those same three values into the matching positions of the other form. For evaluating, "
        "ask 'base to what power gives the argument?'",
        solved(1, "Convert $2^5=32$ to logarithmic form.",
               ["Identify the base ($2$), the exponent ($5$), and the result ($32$).",
                "In log form, the base stays the base, and the equation reads: $\\log_2 32=5$."],
               "$\\log_2 32=5$", "", "Easy")
        + solved(2, "Convert $\\log_3 81=4$ to exponential form.",
                 ["Identify the base ($3$), the exponent ($4$), and the argument/result ($81$).",
                  "In exponential form, the base stays the base and the log's value becomes the exponent: "
                  "$3^4=81$."],
                 "$3^4=81$", "", "Medium")
        + solved(3, "Evaluate $\\log_5 125$.",
                 ["Restate the question: five to what power gives $125$?",
                  "Test powers of $5$: $5^1=5$, $5^2=25$, $5^3=125$.",
                  "The exponent that works is $3$."],
                 "$3$", "", "Hard"),
        ("Mixing up which number is the base in $\\log_b(v)=n$",
         "In $\\log_b v=n$, $b$ is the base, $v$ is the argument, and $n$ is the exponent. Writing the "
         "conversion $b^n=v$ backwards — for example swapping $b$ and $n$ — is one of the most common early "
         "mistakes with logarithms."),
        ("Say the log sentence in words before converting",
         "Read $\\log_b v=n$ as 'b raised to what power gives v, and the answer is n,' then write the "
         "exponential form $b^n=v$ directly from that sentence."),
        ["I can convert any exponential equation into logarithmic form and back.",
         "I can identify the base, exponent, and argument in a log statement without confusing their roles.",
         "I know that $\\log_b 1=0$ and $\\log_b b=1$ for any valid base $b$."],
        11,
    )

    c4 = concept_block(
        "4. Log properties: product, quotient, and power rules",
        [
            "The three core logarithm properties translate operations inside a logarithm into simpler "
            "operations outside of it. The <strong>product rule</strong>, $\\log_b(mn)=\\log_b m+\\log_b n$, "
            "turns multiplication inside the log into addition outside. The <strong>quotient rule</strong>, "
            "$\\log_b\\left(\\dfrac{m}{n}\\right)=\\log_b m-\\log_b n$, turns division inside into subtraction "
            "outside.",
            "The <strong>power rule</strong>, $\\log_b(m^p)=p\\log_b m$, lets you pull an exponent on the "
            "argument out to the front of the logarithm as a multiplier. This rule is especially useful when "
            "solving equations where the variable sits in an exponent inside a logarithm.",
            "These properties can be read in either direction: you can combine several logs into one using "
            "product/quotient rules in reverse, which is exactly the technique needed to solve equations with "
            "multiple log terms, or you can expand a single complicated log into several simpler ones.",
            "A critical warning: these three rules apply only to logs of a <strong>product</strong>, "
            "<strong>quotient</strong>, or <strong>power</strong>. There is no rule for the log of a "
            "<strong>sum</strong> or <strong>difference</strong> — $\\log_b(m+n)$ cannot be split into "
            "$\\log_b m+\\log_b n$, and treating it that way is one of the most common algebra errors involving "
            "logs.",
            "Matching the operation you actually see inside the logarithm to the correct property — "
            "multiplication to addition, division to subtraction, exponent to multiplier — is the entire skill "
            "of this concept, and it becomes automatic with repetition.",
        ],
        "Log properties are the reason logarithms are useful at all: they convert the hard operations of "
        "multiplication, division, and exponentiation into the easy operations of addition, subtraction, and "
        "multiplication, which is exactly what made logarithms valuable for calculation long before calculators "
        "existed.",
        "Look at the operation inside the logarithm. Multiplication becomes addition outside (product rule). "
        "Division becomes subtraction outside (quotient rule). An exponent on the argument becomes a multiplier "
        "out front (power rule). Apply only the property matching what you actually see.",
        solved(1, "Evaluate $\\log_2 8+\\log_2 4$ using the product rule.",
               ["Recognize the sum-of-logs pattern, which corresponds to the product rule in reverse.",
                "Combine into one log: $\\log_2(8\\cdot4)=\\log_2 32$.",
                "Evaluate: since $2^5=32$, the result is $5$."],
               "$5$", "", "Easy")
        + solved(2, "Evaluate $\\log_3 81-\\log_3 9$ using the quotient rule.",
                 ["Recognize the difference-of-logs pattern, which corresponds to the quotient rule in reverse.",
                  "Combine into one log: $\\log_3\\left(\\dfrac{81}{9}\\right)=\\log_3 9$.",
                  "Evaluate: since $3^2=9$, the result is $2$."],
                 "$2$", "", "Medium")
        + solved(3, "Evaluate $\\log_5(25^3)$ using the power rule.",
                 ["Apply the power rule to pull the exponent out front: $\\log_5(25^3)=3\\log_5 25$.",
                  "Evaluate the remaining log: since $5^2=25$, $\\log_5 25=2$.",
                  "Multiply: $3\\times2=6$."],
                 "$6$",
                 "This is much faster than computing $25^3=15625$ first and then evaluating a huge logarithm "
                 "directly.", "Hard"),
        ("Splitting a log of a sum into a sum of logs",
         "$\\log_b(m+n)$ is not equal to $\\log_b m+\\log_b n$. The product and quotient rules only apply to "
         "logs of a product or a quotient, never to logs of a sum or difference of arguments."),
        ("Match the operation inside the log to the property",
         "Multiplication inside the log becomes addition outside, division becomes subtraction, and an "
         "exponent inside becomes a multiplier outside — apply only the single property that actually matches "
         "what you see."),
        ["I can combine a sum of two logs (same base) into a single log using the product rule.",
         "I can combine a difference of two logs (same base) into a single log using the quotient rule.",
         "I know that $\\log_b(m+n)$ can never be split into $\\log_b m+\\log_b n$."],
        16,
    )

    c5 = concept_block(
        "5. Solving exponential and logarithmic equations",
        [
            "Solving an exponential equation where a common base is not available, such as $2^x=10$, requires "
            "taking a logarithm of both sides. Because logarithms are one-to-one functions, taking the same log "
            "of both sides of a true equation preserves the equation, letting you use the power rule to bring "
            "the variable exponent down where it can be isolated algebraically.",
            "Solving a logarithmic equation typically means isolating a single logarithm expression (using log "
            "properties to combine multiple log terms into one, if needed), and then converting that log "
            "equation into exponential form to remove the logarithm entirely.",
            "Just like with radical equations, converting a log equation into exponential form can occasionally "
            "produce a candidate solution that makes one of the original logarithm's <strong>arguments</strong> "
            "zero or negative. Since logarithms are only defined for positive arguments, any such candidate must "
            "be rejected as extraneous.",
            "The safest habit is to write the domain restriction — every argument must be strictly positive — "
            "before solving, exactly the way you wrote domain restrictions before solving rational and radical "
            "equations earlier this year.",
            "Whether an equation is exponential or logarithmic, the general pattern is the same: isolate the "
            "hard part (the exponential or the log expression), apply the inverse operation to undo it, solve "
            "what remains, and check the result against the required domain.",
        ],
        "Exponential and logarithmic equations are inverses of each other, and solving each type relies on "
        "applying the other operation to undo it — logs undo exponentials, and exponentiating undoes logs — "
        "always followed by a domain check on any log arguments involved.",
        "Isolate the exponential or logarithmic expression. Apply the inverse operation (take a log, or "
        "exponentiate) to undo it. Solve the resulting equation. Confirm every log argument in your candidate "
        "solutions stays positive.",
        solved(1, "Solve $\\log_2 x=5$.",
               ["The log is already isolated.",
                "Convert to exponential form: $x=2^5$.",
                "Evaluate: $x=32$."],
               "$x=32$", "", "Easy")
        + solved(2, "Solve $\\log_3(x-1)=2$.",
                 ["Domain requires the argument to be positive: $x-1>0 \\Rightarrow x>1$.",
                  "Convert to exponential form: $x-1=3^2=9$.",
                  "Solve: $x=10$.",
                  "Check the domain: $10>1$, so the solution is valid."],
                 "$x=10$", "", "Medium")
        + solved(3, "Solve $2^x=10$ using logarithms (round to the nearest hundredth).",
                 ["Take $\\log$ (or $\\ln$) of both sides: $\\log(2^x)=\\log(10)$.",
                  "Apply the power rule on the left: $x\\log2=\\log10$.",
                  "Solve for $x$: $x=\\dfrac{\\log10}{\\log2}$.",
                  "Compute: $x\\approx\\dfrac{1}{0.30103}\\approx3.32$."],
                 "$x\\approx3.32$",
                 "This same change-of-base pattern is generalized in the next concept.", "Hard"),
        ("Forgetting the domain of the argument when solving log equations",
         "A logarithm's argument must be strictly positive, so any candidate solution that makes an argument "
         "zero or negative must be rejected as extraneous, even though it solves the cleared exponential "
         "equation."),
        ("Isolate, exponentiate or take logs, then check the domain",
         "Isolate the log or exponential expression first, undo it with the matching inverse operation, and "
         "finish by confirming every argument stays positive for your candidate answers."),
        ["I isolate the log or exponential expression before applying the inverse operation.",
         "I convert a log equation to exponential form (or vice versa) to solve for the variable.",
         "I check that every logarithm argument stays positive for any candidate solution before accepting it."],
        21,
    )

    c6 = concept_block(
        "6. Change of base and real-world applications: interest, half-life, and pH",
        [
            "Most calculators only compute $\\log_{10}$ (common log) and $\\ln$ (natural log, base $e$) "
            "directly. The <strong>change-of-base formula</strong>, $\\log_b v=\\dfrac{\\log v}{\\log b}"
            "=\\dfrac{\\ln v}{\\ln b}$, lets you evaluate a logarithm with any base by rewriting it using "
            "whichever of those two the calculator supports.",
            "Compound interest is modeled by $A=P\\left(1+\\dfrac{r}{n}\\right)^{nt}$, where $P$ is the "
            "starting principal, $r$ is the annual interest rate (as a decimal), $n$ is the number of times "
            "interest compounds per year, and $t$ is time in years. Continuous compounding uses the related "
            "formula $A=Pe^{rt}$.",
            "Half-life problems use the decay pattern $A=A_0\\left(\\dfrac12\\right)^{t/h}$, where $A_0$ is the "
            "starting amount and $h$ is the half-life. The exponent $t/h$ simply counts how many half-lives have "
            "passed, which may be a non-whole number.",
            "pH-style problems use logarithms because the underlying quantity (like hydrogen ion concentration) "
            "spans an enormous range of magnitudes; a formula like $\\text{pH}=-\\log[H^+]$ compresses that huge "
            "range into small, easy-to-compare numbers. Solving for the concentration given a pH just means "
            "reversing the log with an exponential step.",
            "In every application, the real challenge is matching the words of the problem to the correct "
            "formula and correctly labeling every letter (principal, rate, compounding frequency, time, initial "
            "amount, half-life) before substituting numbers.",
        ],
        "Change of base and the growth/decay/pH application formulas are where logarithms stop being an "
        "abstract algebra topic and start describing money, medicine, chemistry, and physics in the real world.",
        "For change of base, rewrite $\\log_b v$ as $\\dfrac{\\log v}{\\log b}$ and evaluate with a calculator. "
        "For applications, identify which formula fits the situation, label every variable with its given "
        "value and units, and substitute carefully, keeping percentages as decimals.",
        solved(1, "Use change of base to evaluate $\\log_5 40$ (round to 2 decimal places).",
               ["Apply the change-of-base formula: $\\log_5 40=\\dfrac{\\log 40}{\\log 5}$.",
                "Compute each common log: $\\log40\\approx1.602$ and $\\log5\\approx0.699$.",
                "Divide: $\\dfrac{1.602}{0.699}\\approx2.29$."],
               "$\\approx2.29$", "", "Easy")
        + solved(2, "Find the balance after 10 years for $P=1000$ invested at $r=5\\%$ annually, compounded "
                    "once per year (nearest cent).",
                 ["Identify the formula and label the variables: $A=P(1+r)^t$ with $P=1000$, $r=0.05$, $t=10$.",
                  "Substitute: $A=1000(1.05)^{10}$.",
                  "Compute the power: $1.05^{10}\\approx1.628895$.",
                  "Multiply: $A\\approx1628.89$."],
                 "$\\$1628.89$", "", "Medium")
        + solved(3, "A radioactive sample starts at 80 grams with a half-life of 5 days. Find the amount "
                    "remaining after 15 days.",
                 ["Identify the formula: $A=A_0\\left(\\dfrac12\\right)^{t/h}$ with $A_0=80$, $t=15$, $h=5$.",
                  "Compute the exponent: $t/h=15/5=3$ half-lives.",
                  "Substitute: $A=80\\left(\\dfrac12\\right)^3=80\\left(\\dfrac18\\right)$.",
                  "Compute: $A=10$ grams."],
                 "$10$ grams",
                 "Fifteen days is exactly three half-lives, so this could also be checked step by step: "
                 "$80\\to40\\to20\\to10$.", "Hard"),
        ("Plugging percentages into formulas as whole numbers",
         "A $5\\%$ rate must be entered as $0.05$ in growth, decay, and interest formulas. Using $5$ instead of "
         "$0.05$ inflates the answer by roughly a factor of 100 or more."),
        ("Identify the formula pieces before you substitute",
         "Write down which formula applies (compound interest, continuous growth, or half-life decay), label "
         "each letter with its value including units, and substitute only after every piece is labeled."),
        ["I can rewrite $\\log_b v$ using the change-of-base formula and evaluate it with common or natural log.",
         "I convert a stated percent rate into a decimal before substituting it into any growth or decay "
         "formula.",
         "I can identify which formula (compound interest, continuous growth, half-life) matches a word "
         "problem before substituting numbers."],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        AUDIENCE,
        [
            "Build and evaluate exponential growth/decay models $y=a\\cdot b^x$",
            "Review exponent properties to solve exponential equations with a common base",
            "Define logarithms and convert freely between exponential and logarithmic form",
            "Apply the product, quotient, and power properties of logarithms",
            "Solve exponential and logarithmic equations, checking log-argument domains",
            "Use change of base and apply logs/exponentials to interest, half-life, and pH problems",
        ],
        body,
        practice_slots(31, 50),
    )
    return title, description, content, _u7_questions()


# =====================================================================================
# UNIT 8: Sequences, Series & Trig Foundations
# =====================================================================================

def _u8_questions():
    qs = []

    # Concept 1 — arithmetic sequences & series (1-5)
    qs.append(mq("An arithmetic sequence has $a_1=2$, $d=5$. Find $a_8$.", "37",
                 "$a_8=a_1+7d=2+7(5)=37$.", 1, distractors=["35", "42", "40"]))
    qs.append(mq("An arithmetic sequence has $a_1=10$, $d=-3$. Find $a_6$.", "-5",
                 "$a_6=a_1+5d=10+5(-3)=-5$.", 2, distractors=["5", "-2", "-8"]))
    qs.append(mq("Find the sum of the first 6 terms of $4,9,14,19,\\ldots$", "99",
                 "$a_1=4$, $d=5$, $a_6=4+5(5)=29$. $S_6=\\dfrac{6}{2}(4+29)=3(33)=99$.",
                 3, distractors=["87", "108", "93"]))
    qs.append(mq("An arithmetic sequence has $a_1=7$ and $a_5=23$. Find $d$.", "4",
                 "$23=7+4d \\Rightarrow 16=4d \\Rightarrow d=4$.", 4, distractors=["3", "5", "16"]))
    qs.append(mq("An arithmetic sequence has $a_1=1$, $d=3$, and $a_n=40$. Find $n$.", "14",
                 "$40=1+(n-1)(3) \\Rightarrow 39=3(n-1) \\Rightarrow n-1=13 \\Rightarrow n=14$.",
                 5, distractors=["13", "39", "12"]))

    # Concept 2 — geometric sequences & series (6-10)
    qs.append(mq("A geometric sequence has $a_1=3$, $r=2$. Find $a_5$.", "48",
                 "$a_5=a_1r^4=3(16)=48$.", 6, distractors=["24", "96", "16"]))
    qs.append(mq("A geometric sequence has $a_1=100$, $r=1/2$. Find $a_4$.", "12.5",
                 "$a_4=a_1r^3=100\\left(\\dfrac18\\right)=12.5$.", 7, distractors=["25", "6.25", "50"]))
    qs.append(mq("Find the sum of the first 4 terms of $1,3,9,27,\\ldots$", "40",
                 "$S_4=1\\cdot\\dfrac{1-3^4}{1-3}=\\dfrac{1-81}{-2}=\\dfrac{-80}{-2}=40$.",
                 8, distractors=["27", "81", "30"]))
    qs.append(mq("Find the sum of the infinite geometric series with $a_1=5$, $r=1/5$.", "6.25",
                 "$S_\\infty=\\dfrac{a_1}{1-r}=\\dfrac{5}{1-1/5}=\\dfrac{5}{4/5}=\\dfrac{25}{4}=6.25$.",
                 9, distractors=["25", "5", "1.25"]))
    qs.append(mq("Find the sum of the infinite geometric series with $a_1=12$, $r=-1/3$.", "9",
                 "$S_\\infty=\\dfrac{a_1}{1-r}=\\dfrac{12}{1-(-1/3)}=\\dfrac{12}{4/3}=9$.",
                 10, distractors=["16", "8", "4"]))

    # Concept 3 — sigma notation basics (11-15)
    qs.append(mq("Evaluate $\\sum_{k=1}^{6}k$.", "21",
                 "$1+2+3+4+5+6=21$.", 11, distractors=["15", "20", "36"]))
    qs.append(mq("Evaluate $\\sum_{k=1}^{4}3k$.", "30",
                 "$3(1+2+3+4)=3(10)=30$.", 12, distractors=["10", "24", "36"]))
    qs.append(mq("Evaluate $\\sum_{k=1}^{5}(k+2)$.", "25",
                 "$(1+2+3+4+5)+5(2)=15+10=25$.", 13, distractors=["15", "10", "35"]))
    qs.append(mq("Evaluate $\\sum_{k=1}^{4}k^2$.", "30",
                 "$1+4+9+16=30$.", 14, distractors=["16", "10", "36"]))
    qs.append(mq("Evaluate $\\sum_{k=0}^{3}2^k$.", "15",
                 "$1+2+4+8=15$.", 15, distractors=["16", "14", "8"]))

    # Concept 4 — right triangle trig (16-20)
    qs.append(mq("A right triangle has legs 6 and 8, hypotenuse 10. Find $\\sin\\theta$ for the angle "
                 "opposite the leg of length 6.", "3/5",
                 "$\\sin\\theta=\\dfrac{\\text{opposite}}{\\text{hypotenuse}}=\\dfrac{6}{10}=\\dfrac35$.",
                 16, distractors=["4/5", "3/4", "5/3"]))
    qs.append(mq("Using the same triangle (legs 6, 8, hyp 10), find $\\cos\\theta$ for the same angle.", "4/5",
                 "$\\cos\\theta=\\dfrac{\\text{adjacent}}{\\text{hypotenuse}}=\\dfrac{8}{10}=\\dfrac45$.",
                 17, distractors=["3/5", "3/4", "4/3"]))
    qs.append(mq("Using the same triangle, find $\\tan\\theta$ for the same angle.", "3/4",
                 "$\\tan\\theta=\\dfrac{\\text{opposite}}{\\text{adjacent}}=\\dfrac{6}{8}=\\dfrac34$.",
                 18, distractors=["4/3", "3/5", "4/5"]))
    qs.append(mq("A right triangle has legs 9 and 12, hypotenuse 15. Find $\\sin\\theta$ for the angle "
                 "opposite the leg of length 9.", "3/5",
                 "$\\sin\\theta=\\dfrac{9}{15}=\\dfrac35$.", 19, distractors=["4/5", "9/15", "3/4"]))
    qs.append(mq("A right triangle has legs 5 and 12, hypotenuse 13. Find $\\tan\\theta$ for the angle "
                 "opposite the leg of length 12.", "12/5",
                 "$\\tan\\theta=\\dfrac{12}{5}$.", 20, distractors=["5/12", "12/13", "5/13"]))

    # Concept 5 — unit circle intro (21-25)
    qs.append(mq("Convert $90°$ to radians.", "π/2",
                 "$90\\times\\dfrac{\\pi}{180}=\\dfrac{\\pi}{2}$.", 21, distractors=["π", "π/4", "π/3"]))
    qs.append(mq("Convert $270°$ to radians.", "3π/2",
                 "$270\\times\\dfrac{\\pi}{180}=\\dfrac{3\\pi}{2}$.", 22, distractors=["π/2", "2π", "3π/4"]))
    qs.append(mq("Convert $\\dfrac{\\pi}{6}$ radians to degrees.", "30°",
                 "$\\dfrac{\\pi}{6}\\times\\dfrac{180}{\\pi}=30°$.", 23, distractors=["45°", "60°", "20°"]))
    qs.append(mq("Evaluate $\\sin(60°)$.", "√3/2",
                 "This is a key unit-circle value: $\\sin(60°)=\\dfrac{\\sqrt3}{2}$.",
                 24, distractors=["1/2", "√2/2", "1"]))
    qs.append(mq("Evaluate $\\cos(30°)$.", "√3/2",
                 "This is a key unit-circle value: $\\cos(30°)=\\dfrac{\\sqrt3}{2}$.",
                 25, distractors=["1/2", "√2/2", "1"]))

    # Concept 6 — graphing sine/cosine basics (26-30)
    qs.append(mq("Find the amplitude of $y=5\\sin(x)$.", "5",
                 "The amplitude is $|A|=|5|=5$.", 26, distractors=["1", "10", "2.5"]))
    qs.append(mq("Find the period of $y=\\sin(3x)$.", "2π/3",
                 "Period $=\\dfrac{2\\pi}{B}=\\dfrac{2\\pi}{3}$.", 27, distractors=["3", "6π", "2π"]))
    qs.append(mq("Find the period of $y=\\cos(x/2)$.", "4π",
                 "Period $=\\dfrac{2\\pi}{B}=\\dfrac{2\\pi}{1/2}=4\\pi$.", 28, distractors=["π", "2π", "π/2"]))
    qs.append(mq("Describe the vertical shift of $y=\\sin(x)-4$.", "Down 4",
                 "Subtracting $4$ outside the trig function shifts the entire graph down $4$ units.",
                 29, distractors=["Up 4", "Left 4", "Right 4"]))
    qs.append(mq("Find the amplitude and period of $y=4\\cos(2x)$.", "amplitude 4, period π",
                 "Amplitude is $|A|=4$. Period is $\\dfrac{2\\pi}{B}=\\dfrac{2\\pi}{2}=\\pi$.",
                 30, distractors=["amplitude 2, period 4π", "amplitude 4, period 2π",
                                  "amplitude 2, period π"]))

    finale = []

    # Easy 31-45
    for a1, d, n, ans in [(1, 2, 5, 9), (3, 4, 6, 23), (5, 3, 4, 14), (2, 5, 7, 32), (10, -2, 5, 2)]:
        finale.append(mq(
            f"Arithmetic: $a_1={a1}$, $d={d}$. Find $a_{{{n}}}$.", str(ans),
            f"$a_{{{n}}}=a_1+({n}-1)d={a1}+{n-1}({d})={ans}$.",
            0, distractors=[str(ans + d), str(ans - d), str(a1 * n)]))
    for a1, r, n, ans in [(2, 2, 4, 16), (1, 3, 4, 27), (5, 2, 3, 20), (3, 3, 3, 27), (1, 2, 6, 32)]:
        finale.append(mq(
            f"Geometric: $a_1={a1}$, $r={r}$. Find $a_{{{n}}}$.", str(ans),
            f"$a_{{{n}}}=a_1r^{{{n-1}}}={a1}({r})^{{{n-1}}}={ans}$.",
            0, distractors=[str(ans * r), str(ans // r if isinstance(ans // r, int) else ans), str(a1 * n)]))
    for n in (3, 4, 5, 6, 7):
        total = n * (n + 1) // 2
        finale.append(mq(f"Evaluate $\\sum_{{k=1}}^{{{n}}}k$.", str(total),
                         f"Sum of the first {n} positive integers: $\\dfrac{{{n}({n}+1)}}{{2}}={total}$.",
                         0, distractors=[str(total + 1), str(total - 1), str(n * n)]))

    # Medium 46-60
    for a1, d, n in [(1, 1, 10), (2, 3, 8), (5, 2, 6), (3, 4, 5), (0, 5, 7)]:
        an = a1 + (n - 1) * d
        sn = n * (a1 + an) // 2
        finale.append(mq(
            f"Find $S_{{{n}}}$ for the arithmetic sequence with $a_1={a1}$, $d={d}$.", str(sn),
            f"$a_{{{n}}}={a1}+({n}-1)({d})={an}$. Then $S_{{{n}}}=\\dfrac{{{n}}}{{2}}({a1}+{an})={sn}$.",
            0, distractors=[str(sn + n), str(an), str(sn - d)]))
    for legs in [(3, 4), (5, 12), (8, 15), (7, 24), (9, 12)]:
        a, b = legs
        hyp = int((a * a + b * b) ** 0.5)
        from math import gcd
        g = gcd(a, hyp)
        finale.append(mq(
            f"A right triangle has legs {a} and {b}. Find $\\sin\\theta$ for the angle opposite the leg of "
            f"length {a} (hypotenuse is {hyp}).", f"{a//g}/{hyp//g}",
            f"By the Pythagorean theorem the hypotenuse is {hyp}. $\\sin\\theta=\\dfrac{{{a}}}{{{hyp}}}"
            f"=\\dfrac{{{a//g}}}{{{hyp//g}}}$.",
            0, distractors=[f"{b}/{hyp}", f"{a}/{b}", f"{hyp}/{a}"]))
    for text, ans, expl, dis in [
        ("Evaluate $\\sin(45°)$.", "√2/2", "This is a key unit-circle value.", ["1/2", "1", "√3/2"]),
        ("Evaluate $\\cos(60°)$.", "1/2", "This is a key unit-circle value.", ["√3/2", "√2/2", "1"]),
        ("Evaluate $\\tan(45°)$.", "1", "This is a key unit-circle value.", ["√2", "1/2", "0"]),
        ("Evaluate $\\sin(90°)$.", "1", "This is a key unit-circle value.", ["0", "1/2", "-1"]),
        ("Evaluate $\\cos(0°)$.", "1", "This is a key unit-circle value.", ["0", "-1", "1/2"]),
    ]:
        finale.append(mq(text, ans, expl, 0, distractors=dis))

    # Hard 61-70
    for text, ans, expl, dis in [
        ("Find the sum $2+5+8+\\cdots+50$.", "442",
         "Here $a_1=2$, $d=3$. Find $n$: $50=2+(n-1)(3) \\Rightarrow n=17$. Then "
         "$S_{17}=\\dfrac{17}{2}(2+50)=17(26)=442$.",
         ["408", "425", "459"]),
        ("A geometric sequence has $a_4=54$ and $r=3$. Find $a_1$.", "2",
         "$a_4=a_1r^3 \\Rightarrow 54=a_1(27) \\Rightarrow a_1=2$.",
         ["6", "18", "3"]),
        ("An infinite geometric series has $S_\\infty=20$ and $r=1/4$. Find $a_1$.", "15",
         "$a_1=S_\\infty(1-r)=20\\left(\\dfrac34\\right)=15$.",
         ["5", "16", "25"]),
        ("Evaluate $\\sum_{k=1}^{5}(3k-2)$.", "35",
         "The terms are $1,4,7,10,13$, which sum to $35$.",
         ["30", "40", "25"]),
        ("A 13-foot ladder leans against a wall with its base 5 feet from the wall. Find $\\sin\\theta$, "
         "where $\\theta$ is the angle between the ladder and the ground.", "12/13",
         "The height is $\\sqrt{13^2-5^2}=\\sqrt{144}=12$. The angle at the base has the height as its "
         "opposite side: $\\sin\\theta=\\dfrac{12}{13}$.",
         ["5/13", "5/12", "12/5"]),
        ("Evaluate $\\sin(120°)$ using a reference angle.", "√3/2",
         "The reference angle is $180°-120°=60°$, and sine is positive in the second quadrant: "
         "$\\sin(120°)=\\sin(60°)=\\dfrac{\\sqrt3}{2}$.",
         ["-√3/2", "1/2", "-1/2"]),
        ("Evaluate $\\cos(210°)$ using a reference angle.", "-√3/2",
         "The reference angle is $210°-180°=30°$, and cosine is negative in the third quadrant: "
         "$\\cos(210°)=-\\cos(30°)=-\\dfrac{\\sqrt3}{2}$.",
         ["√3/2", "-1/2", "1/2"]),
        ("For $y=-2\\sin(x)+3$, find the maximum and minimum values.", "max 5, min 1",
         "Amplitude is $2$ and vertical shift is $3$: max $=3+2=5$, min $=3-2=1$.",
         ["max 3, min -3", "max 2, min -2", "max 5, min -1"]),
        ("Insert one arithmetic mean between 8 and 20 (find the middle term).", "14",
         "The arithmetic mean of the two surrounding terms is $\\dfrac{8+20}{2}=14$.",
         ["12", "16", "10"]),
        ("A ball dropped from 100 ft bounces back to 60% of its previous height each time. Find the height "
         "after the 3rd bounce.", "21.6",
         "$100(0.6)^3=100(0.216)=21.6$ ft.",
         ["36", "60", "16.2"]),
    ]:
        finale.append(mq(text, ans, expl, 0, distractors=dis))

    # Stretch 71-80
    for text, ans, expl, dis in [
        ("Express the repeating decimal $0.\\overline{3}$ as a fraction using an infinite geometric series.",
         "1/3",
         "Write $0.3+0.03+0.003+\\cdots$ with $a_1=0.3$, $r=0.1$: $S_\\infty=\\dfrac{0.3}{1-0.1}"
         "=\\dfrac{0.3}{0.9}=\\dfrac13$.",
         ["3/10", "1/9", "1/30"]),
        ("An arithmetic sequence has $a_3=11$ and $a_7=23$. Find $a_1$.", "5",
         "$d=\\dfrac{23-11}{7-3}=3$. Then $a_1=a_3-2d=11-6=5$.",
         ["8", "2", "3"]),
        ("Express $3+6+9+12+15$ in sigma notation and evaluate.", "45",
         "This is $\\sum_{k=1}^{5}3k=3(1+2+3+4+5)=3(15)=45$.",
         ["36", "30", "50"]),
        ("In a right triangle, $\\sin\\theta=\\dfrac{7}{25}$. Find $\\cos\\theta$ (θ acute).", "24/25",
         "The sides form a $7$-$24$-$25$ right triangle, so $\\cos\\theta=\\dfrac{24}{25}$.",
         ["7/24", "24/7", "18/25"]),
        ("Find all $\\theta$ in $[0°,360°)$ where $\\sin\\theta=\\dfrac12$.", "30° or 150°",
         "Sine is positive in quadrants I and II. Reference angle $30°$ gives $\\theta=30°$ and "
         "$\\theta=180°-30°=150°$.",
         ["30° or 210°", "60° or 120°", "150° or 210°"]),
        ("A Ferris wheel's height is modeled by $h(t)=25\\sin\\left(\\dfrac{\\pi}{6}t\\right)+30$. Find the "
         "period (minutes) and maximum height (feet).", "period 12 min, max height 55 ft",
         "Period $=\\dfrac{2\\pi}{\\pi/6}=12$ minutes. Maximum height $=30+25=55$ ft.",
         ["period 6 min, max height 55 ft", "period 12 min, max height 25 ft",
          "period 24 min, max height 30 ft"]),
        ("An infinite geometric series has $a_1=27$ and $S_\\infty=45$. Find $r$.", "2/5",
         "$27/(1-r)=45 \\Rightarrow 1-r=\\dfrac{27}{45}=\\dfrac35 \\Rightarrow r=\\dfrac25$.",
         ["3/5", "1/5", "4/5"]),
        ("Find the sum of all multiples of 7 between 1 and 100.", "735",
         "First term $7$, last term $98$, $d=7$, $n=\\dfrac{98-7}{7}+1=14$. "
         "$S_{14}=\\dfrac{14}{2}(7+98)=7(105)=735$.",
         ["700", "749", "693"]),
        ("Evaluate $\\sum_{k=1}^{10}k-\\sum_{k=1}^{5}k$.", "40",
         "$55-15=40$.",
         ["45", "30", "35"]),
        ("Convert $\\dfrac{5\\pi}{4}$ radians to degrees and evaluate $\\tan$ at that angle.",
         "225°, tan=1",
         "$\\dfrac{5\\pi}{4}\\times\\dfrac{180}{\\pi}=225°$. The reference angle is $45°$, and tangent is "
         "positive in the third quadrant, so $\\tan(225°)=1$.",
         ["225°, tan=-1", "180°, tan=1", "225°, tan=√2"]),
    ]:
        finale.append(mq(text, ans, expl, 0, distractors=dis))

    qs.extend(finale[:50])
    return _fill80(qs)


def build_unit8():
    title = "Algebra 2 Unit 8: Sequences, Series & Trig Foundations"
    description = (
        "Deep, patient coverage of sequences, series, and introductory trigonometry for grade 10 Algebra 2 — "
        "arithmetic and geometric sequences and series, sigma notation, right-triangle trig, the unit circle, "
        "and the basics of graphing sine and cosine."
    )

    c1 = concept_block(
        "1. Arithmetic sequences and series",
        [
            "An arithmetic sequence is a list of numbers that changes by the same fixed amount, called the "
            "<strong>common difference</strong> $d$, from one term to the next. If the first term is $a_1$, the "
            "$n$th term is found with $a_n=a_1+(n-1)d$, because you add $d$ exactly $n-1$ times to get from the "
            "first term to the $n$th term.",
            "Finding $d$ from two known terms is just as important as finding a term from $d$: subtract any two "
            "terms and divide by how many steps apart they are, $d=\\dfrac{a_m-a_k}{m-k}$, to recover the common "
            "difference.",
            "A series is the <strong>sum</strong> of the terms of a sequence, not the list of terms itself. The "
            "arithmetic series formula, $S_n=\\dfrac{n}{2}(a_1+a_n)$, comes from pairing the first and last "
            "terms, the second and second-to-last terms, and so on, noticing that every pair adds to the same "
            "total, $a_1+a_n$.",
            "If you do not already know the last term $a_n$, you can substitute the term formula directly into "
            "the sum formula to get $S_n=\\dfrac{n}{2}\\big[2a_1+(n-1)d\\big]$, which only requires the first "
            "term, the common difference, and the number of terms.",
            "Word problems about arithmetic sequences and series often disguise the vocabulary: 'the amount "
            "saved each month increases by the same fixed amount' describes $d$, and 'total saved after $n$ "
            "months' describes $S_n$, so translating carefully from words to the two formulas is the real skill "
            "being tested.",
        ],
        "Arithmetic sequences model any quantity that changes by the same fixed amount every step — evenly "
        "spaced seating, steadily increasing savings, or a steadily rising temperature — and the term and sum "
        "formulas let you jump directly to any term or any running total without listing every value by hand.",
        "Identify whether you need a single term (use $a_n=a_1+(n-1)d$) or a running total (use "
        "$S_n=\\dfrac{n}{2}(a_1+a_n)$). If the last term is unknown, find it first using the term formula before "
        "computing the sum.",
        solved(1, "Find the 10th term of $3,7,11,15,\\ldots$",
               ["Identify $a_1=3$ and $d=4$.",
                "Apply the term formula: $a_{10}=a_1+9d=3+9(4)=3+36$.",
                "Simplify: $a_{10}=39$."],
               "$a_{10}=39$", "", "Easy")
        + solved(2, "Find the sum of the first 10 terms of $3,7,11,15,\\ldots$",
                 ["From the previous example, $a_{10}=39$.",
                  "Apply the sum formula: $S_{10}=\\dfrac{10}{2}(a_1+a_{10})=5(3+39)$.",
                  "Simplify: $S_{10}=5(42)=210$."],
                 "$S_{10}=210$", "", "Medium")
        + solved(3, "An arithmetic sequence has $a_1=5$ and $d=-2$. Find $S_{15}$.",
                 ["Find the last term first: $a_{15}=5+14(-2)=5-28=-23$.",
                  "Apply the sum formula: $S_{15}=\\dfrac{15}{2}(a_1+a_{15})=\\dfrac{15}{2}(5+(-23))$.",
                  "Simplify inside the parentheses: $5-23=-18$.",
                  "Multiply: $S_{15}=\\dfrac{15}{2}(-18)=15(-9)=-135$."],
                 "$S_{15}=-135$",
                 "A negative sum is completely normal here, since the terms themselves become negative partway "
                 "through the sequence.", "Hard"),
        ("Mixing up the term formula with the sum formula",
         "$a_n=a_1+(n-1)d$ finds one single term, while $S_n=\\dfrac{n}{2}(a_1+a_n)$ finds a running total. "
         "Using the term formula when a sum is requested, or the reverse, gives a completely different kind of "
         "answer."),
        ("Find the needed term first, then the sum",
         "If a problem asks for a sum, first find $a_1$ and the last term $a_n$ using the term formula, then "
         "plug both into the sum formula."),
        ["I can find any term of an arithmetic sequence using $a_n=a_1+(n-1)d$.",
         "I can find the sum of the first $n$ terms using $S_n=\\dfrac{n}{2}(a_1+a_n)$.",
         "I can find the common difference $d$ from any two given terms of the sequence."],
        1,
    )

    c2 = concept_block(
        "2. Geometric sequences and series, including an infinite-series introduction",
        [
            "A geometric sequence is a list of numbers that changes by the same fixed <strong>ratio</strong> "
            "$r$, rather than a fixed difference, from one term to the next. If the first term is $a_1$, the "
            "$n$th term is found with $a_n=a_1r^{n-1}$, since you multiply by $r$ exactly $n-1$ times to reach "
            "the $n$th term.",
            "A quick test to tell arithmetic and geometric sequences apart: divide consecutive terms. A "
            "constant result means the sequence is geometric (that constant is $r$); a constant "
            "<strong>difference</strong> instead means the sequence is arithmetic.",
            "The finite geometric series formula, $S_n=a_1\\cdot\\dfrac{1-r^n}{1-r}$ (for $r\\neq1$), gives the "
            "sum of the first $n$ terms directly, without needing to find the last term separately the way the "
            "arithmetic formula sometimes requires.",
            "When $|r|<1$, an <strong>infinite</strong> geometric series actually settles down to a finite total "
            "as more and more terms are added, because each new term shrinks toward zero. That total is given by "
            "$S_\\infty=\\dfrac{a_1}{1-r}$, one of the most surprising and useful results in this unit.",
            "If $|r|\\ge1$, the infinite sum has no finite value — the terms either stay the same size or grow "
            "without bound, so the infinite-sum formula only applies in the $|r|<1$ case, and checking that "
            "condition first is essential before ever using it.",
        ],
        "Geometric sequences model repeated multiplicative change — compound growth, repeated halving, bouncing "
        "ball heights — and the surprising fact that infinitely many shrinking terms can add to a single finite "
        "number connects directly to ideas you will revisit in calculus.",
        "Check whether consecutive terms share a constant ratio (geometric) rather than a constant difference "
        "(arithmetic). Use $a_n=a_1r^{n-1}$ for a single term, the finite sum formula for a fixed number of "
        "terms, and the infinite sum formula only when $|r|<1$.",
        solved(1, "Find the 6th term of $2,6,18,54,\\ldots$",
               ["Identify $a_1=2$ and $r=3$ (each term is $3$ times the previous term).",
                "Apply the term formula: $a_6=a_1r^5=2(3^5)=2(243)$.",
                "Simplify: $a_6=486$."],
               "$a_6=486$", "", "Easy")
        + solved(2, "Find the sum of the first 5 terms of $2,6,18,54,\\ldots$",
                 ["Identify $a_1=2$ and $r=3$.",
                  "Apply the finite sum formula: $S_5=2\\cdot\\dfrac{1-3^5}{1-3}=2\\cdot\\dfrac{1-243}{-2}$.",
                  "Simplify the fraction: $\\dfrac{-242}{-2}=121$.",
                  "Multiply: $S_5=2(121)=242$."],
                 "$S_5=242$", "", "Medium")
        + solved(3, "Find the sum of the infinite geometric series $8+4+2+1+\\cdots$",
                 ["Identify $a_1=8$ and $r=\\dfrac12$ (each term is half the previous term).",
                  "Check the condition for an infinite sum: $|r|=\\dfrac12<1$, so the formula applies.",
                  "Apply the infinite sum formula: $S_\\infty=\\dfrac{a_1}{1-r}=\\dfrac{8}{1-1/2}=\\dfrac{8}{1/2}$.",
                  "Simplify: $S_\\infty=16$."],
                 "$S_\\infty=16$",
                 "Even though this series never stops adding terms, the running total gets closer and closer "
                 "to $16$ without ever exceeding it.", "Hard"),
        ("Using the arithmetic sum formula on a geometric sequence",
         "Geometric sequences grow by a common ratio, not a common difference, so the arithmetic averaging "
         "formula $\\dfrac{n}{2}(a_1+a_n)$ does not apply. A geometric sum needs the ratio-based formula "
         "instead."),
        ("Check for a common ratio before choosing a formula",
         "Divide consecutive terms. A constant ratio means geometric formulas apply, while a constant "
         "difference means arithmetic formulas apply."),
        ["I can find any term of a geometric sequence using $a_n=a_1r^{n-1}$.",
         "I can find the sum of a finite geometric series using $S_n=a_1\\dfrac{1-r^n}{1-r}$.",
         "I know the infinite sum formula $S_\\infty=\\dfrac{a_1}{1-r}$ only applies when $|r|<1$."],
        6,
    )

    c3 = concept_block(
        "3. Sigma notation basics",
        [
            "Sigma notation, $\\sum_{k=\\text{start}}^{\\text{end}}(\\text{expression in }k)$, is a compact way "
            "to write a sum without listing every term. The Greek letter $\\Sigma$ means 'add up,' the bottom "
            "number tells you the first value of $k$ to plug in, and the top number tells you the last value.",
            "Reading a sigma expression means substituting each whole-number value of $k$, from the lower limit "
            "to the upper limit inclusive, into the expression, and then adding all of those resulting values "
            "together.",
            "The safest way to evaluate an unfamiliar sigma expression is to write out the first two or three "
            "terms by hand. This confirms exactly what the notation is describing before you commit to a "
            "shortcut formula, and it quickly reveals mistakes in reading the limits.",
            "Sigma notation connects directly to the sequence and series formulas from the previous two "
            "concepts: $\\sum_{k=1}^{n}\\big[a_1+(k-1)d\\big]$ is exactly the arithmetic series $S_n$ written in "
            "sigma form, and a similar connection exists for geometric series.",
            "A useful shortcut worth memorizing: $\\sum_{k=1}^{n}k=\\dfrac{n(n+1)}{2}$, the sum of the first $n$ "
            "positive integers, which appears constantly both inside and outside of sigma-notation problems.",
        ],
        "Sigma notation is shorthand, not a new type of math — every sigma sum can be unpacked into an ordinary "
        "addition problem by substituting each value of $k$ in turn, which is exactly what makes it worth "
        "learning to read fluently.",
        "Identify the lower and upper limits of $k$. Substitute each whole-number value of $k$ into the "
        "expression, from the lower limit through the upper limit. Add all the resulting values together, "
        "checking your work by writing out at least the first two or three terms explicitly.",
        solved(1, "Evaluate $\\sum_{k=1}^{5}k$.",
               ["Substitute $k=1,2,3,4,5$ into the expression $k$ itself: $1,2,3,4,5$.",
                "Add the terms: $1+2+3+4+5=15$."],
               "$15$", "", "Easy")
        + solved(2, "Evaluate $\\sum_{k=1}^{4}(2k+1)$.",
                 ["Substitute $k=1,2,3,4$: $2(1)+1=3$, $2(2)+1=5$, $2(3)+1=7$, $2(4)+1=9$.",
                  "Add the terms: $3+5+7+9=24$."],
                 "$24$", "", "Medium")
        + solved(3, "Evaluate $\\sum_{k=1}^{3}2^k$.",
                 ["Substitute $k=1,2,3$: $2^1=2$, $2^2=4$, $2^3=8$.",
                  "Add the terms: $2+4+8=14$."],
                 "$14$",
                 "Notice the lower limit starts at $k=1$, so the term $2^0=1$ is not included here.", "Hard"),
        ("Misreading the starting index in sigma notation",
         "$\\sum_{k=1}^{n}$ and $\\sum_{k=0}^{n}$ do not produce the same list of terms. The lower limit tells "
         "you the very first value of $k$ to substitute, and starting from the wrong value shifts every term in "
         "the sum."),
        ("Write out the first two or three terms by hand",
         "Before trusting a formula shortcut, substitute the first two or three values of $k$ directly into "
         "the summand to make sure the pattern matches what the notation actually describes."),
        ["I can substitute each value of $k$ into the summand and add the resulting terms.",
         "I pay attention to whether the lower limit of a sigma sum starts at $0$ or at $1$.",
         "I know the shortcut $\\sum_{k=1}^{n}k=\\dfrac{n(n+1)}{2}$ for the sum of the first $n$ positive "
         "integers."],
        11,
    )

    c4 = concept_block(
        "4. Right-triangle trigonometry review: sine, cosine, and tangent",
        [
            "In a right triangle, the three basic trig ratios compare the lengths of two sides relative to one "
            "of the acute angles, usually called $\\theta$. The mnemonic <strong>SOHCAHTOA</strong> summarizes "
            "all three: Sine is Opposite over Hypotenuse, Cosine is Adjacent over Hypotenuse, and Tangent is "
            "Opposite over Adjacent.",
            "The hypotenuse is always the longest side, opposite the right angle, and it never changes roles no "
            "matter which acute angle you are using. The opposite and adjacent legs, however, <strong>do</strong> "
            "switch roles depending on which acute angle is marked: a leg that is opposite one angle is "
            "adjacent to the other angle in the same triangle.",
            "If only two side lengths are known, the Pythagorean theorem, $a^2+b^2=c^2$, finds the missing "
            "third side before any trig ratio can be computed, since all three ratios need the specific side "
            "lengths involved.",
            "Trig ratios are reciprocal-related to the sides in a very literal sense: if you know one full ratio "
            "(like $\\sin\\theta=\\dfrac{5}{13}$), you actually know the shape of the entire right triangle, and "
            "can find every other ratio using the Pythagorean theorem to get the missing side.",
            "This right-triangle approach only works for acute angles inside an actual right triangle. In the "
            "next concept, the unit circle extends these same three ratios to any angle, including angles "
            "larger than $90°$.",
        ],
        "SOHCAHTOA gives you a direct bridge between the geometry of a right triangle and the trigonometric "
        "ratios used throughout the rest of the unit, and mastering it here makes the upcoming unit-circle "
        "extension feel like a natural next step rather than an entirely new topic.",
        "Label the hypotenuse first (always opposite the right angle). Relative to the marked angle, label the "
        "touching leg as adjacent and the far leg as opposite. Use the Pythagorean theorem for any missing side, "
        "then apply SOHCAHTOA for the requested ratio.",
        solved(1, "A right triangle has legs 3 and 4 and hypotenuse 5. Find $\\sin\\theta$, $\\cos\\theta$, "
                  "and $\\tan\\theta$ for the angle opposite the leg of length 3.",
               ["Label the sides relative to $\\theta$: opposite $=3$, adjacent $=4$, hypotenuse $=5$.",
                "$\\sin\\theta=\\dfrac{\\text{opposite}}{\\text{hypotenuse}}=\\dfrac35$.",
                "$\\cos\\theta=\\dfrac{\\text{adjacent}}{\\text{hypotenuse}}=\\dfrac45$.",
                "$\\tan\\theta=\\dfrac{\\text{opposite}}{\\text{adjacent}}=\\dfrac34$."],
               "$\\sin\\theta=\\dfrac35$, $\\cos\\theta=\\dfrac45$, $\\tan\\theta=\\dfrac34$", "", "Easy")
        + solved(2, "Given $\\tan\\theta=\\dfrac{5}{12}$, find $\\sin\\theta$ and $\\cos\\theta$.",
                 ["Since $\\tan\\theta=\\dfrac{\\text{opposite}}{\\text{adjacent}}=\\dfrac{5}{12}$, treat these "
                  "as leg lengths $5$ and $12$.",
                  "Find the hypotenuse with the Pythagorean theorem: $\\sqrt{5^2+12^2}=\\sqrt{25+144}"
                  "=\\sqrt{169}=13$.",
                  "$\\sin\\theta=\\dfrac{5}{13}$ and $\\cos\\theta=\\dfrac{12}{13}$."],
                 "$\\sin\\theta=\\dfrac{5}{13}$, $\\cos\\theta=\\dfrac{12}{13}$", "", "Medium")
        + solved(3, "A right triangle has hypotenuse 10 and one leg 6. Find all three ratios for the angle "
                    "opposite the leg of length 6.",
                 ["Find the missing leg with the Pythagorean theorem: $\\sqrt{10^2-6^2}=\\sqrt{100-36}"
                  "=\\sqrt{64}=8$.",
                  "Relative to $\\theta$ (opposite the leg of $6$): opposite $=6$, adjacent $=8$, "
                  "hypotenuse $=10$.",
                  "$\\sin\\theta=\\dfrac{6}{10}=\\dfrac35$, $\\cos\\theta=\\dfrac{8}{10}=\\dfrac45$, "
                  "$\\tan\\theta=\\dfrac{6}{8}=\\dfrac34$."],
                 "$\\sin\\theta=\\dfrac35$, $\\cos\\theta=\\dfrac45$, $\\tan\\theta=\\dfrac34$",
                 "This is the same $3$-$4$-$5$ family of ratios as the first example, just scaled up.", "Hard"),
        ("Mixing up which side is opposite versus adjacent",
         "SOHCAHTOA depends on which acute angle you are using. A leg that is opposite one angle is adjacent to "
         "the other angle in the very same right triangle."),
        ("Label the triangle relative to the marked angle first",
         "Before writing any ratio, label the hypotenuse, then label the leg touching the marked angle as "
         "adjacent and the leg across from it as opposite."),
        ["I can label the opposite, adjacent, and hypotenuse sides correctly for a marked acute angle.",
         "I use the Pythagorean theorem to find a missing side before computing a trig ratio.",
         "I can find all three trig ratios once I know just one ratio and the triangle's side lengths."],
        16,
    )

    c5 = concept_block(
        "5. Introduction to the unit circle: degrees, radians, and key angles",
        [
            "The unit circle is a circle of radius $1$ centered at the origin, and it extends the right-triangle "
            "trig ratios to work for <strong>any</strong> angle, not just acute angles inside a triangle. For "
            "now, the most important skills are converting between degrees and radians and recalling the trig "
            "values at a handful of key angles.",
            "Degrees and radians are two different units for measuring the same angle, connected by the fact "
            "that a full circle is both $360°$ and $2\\pi$ radians. To convert degrees to radians, multiply by "
            "$\\dfrac{\\pi}{180}$; to convert radians to degrees, multiply by $\\dfrac{180}{\\pi}$.",
            "Radian measure will become the standard unit in Precalculus and Calculus, so building comfort with "
            "it now — recognizing that $\\pi$ radians is a half turn ($180°$) and $\\dfrac{\\pi}{2}$ radians is "
            "a quarter turn ($90°$) — pays off well beyond this course.",
            "A small set of key angles ($0°,30°,45°,60°,90°$, and their radian equivalents) have "
            "exact, memorable sine and cosine values built from the $30$-$60$-$90$ and $45$-$45$-$90$ right "
            "triangles you already know. Memorizing this short list unlocks a huge number of trig problems "
            "without a calculator.",
            "These key-angle values become even more powerful once you can find a <strong>reference angle</strong> "
            "for any angle in any quadrant, which is where the next steps of unit-circle work (covered in more "
            "depth in Precalculus) will take you.",
        ],
        "The unit circle unifies right-triangle trig with angles beyond $90°$, and degree-radian conversion is "
        "simply a change of measuring units for the exact same rotation, just like converting between inches "
        "and centimeters measures the exact same length.",
        "To convert degrees to radians, multiply by $\\dfrac{\\pi}{180}$; to convert radians to degrees, "
        "multiply by $\\dfrac{180}{\\pi}$. For key angles, recall the exact sine and cosine values from the "
        "$30$-$60$-$90$ and $45$-$45$-$90$ triangles rather than estimating with a calculator.",
        solved(1, "Convert $180°$ to radians.",
               ["Multiply by the conversion factor: $180\\times\\dfrac{\\pi}{180}$.",
                "The $180$'s cancel, leaving $\\pi$ radians."],
               "$\\pi$ radians", "", "Easy")
        + solved(2, "Convert $\\dfrac{\\pi}{3}$ radians to degrees.",
                 ["Multiply by the conversion factor: $\\dfrac{\\pi}{3}\\times\\dfrac{180}{\\pi}$.",
                  "The $\\pi$'s cancel, leaving $\\dfrac{180}{3}=60°$."],
                 "$60°$", "", "Medium")
        + solved(3, "Evaluate $\\sin(30°)$, $\\cos(45°)$, and $\\tan(60°)$ from memory.",
                 ["Recall the $30$-$60$-$90$ triangle ratios: $\\sin(30°)=\\dfrac12$.",
                  "Recall the $45$-$45$-$90$ triangle ratios: $\\cos(45°)=\\dfrac{\\sqrt2}{2}$.",
                  "Recall the $30$-$60$-$90$ triangle ratios: $\\tan(60°)=\\sqrt3$."],
                 "$\\sin(30°)=\\dfrac12$, $\\cos(45°)=\\dfrac{\\sqrt2}{2}$, $\\tan(60°)=\\sqrt3$",
                 "These three values, together with their partners at $0°,60°,90°$, cover nearly every "
                 "no-calculator trig question in this course.", "Hard"),
        ("Using the wrong reference angle in a non-first quadrant",
         "Key angle values like $\\sin(30°)=\\dfrac12$ only transfer directly to other quadrants through the "
         "reference angle, and the sign of the answer must match the quadrant, not just the reference-angle "
         "magnitude."),
        ("Find the quadrant, the reference angle, then the sign",
         "Identify which quadrant the angle lands in, subtract to the nearest axis to get the reference angle, "
         "evaluate using the key-angle value, then attach the correct sign for that quadrant."),
        ["I can convert an angle between degrees and radians in either direction.",
         "I can recall the exact sine, cosine, and tangent values at $0°,30°,45°,60°,90°$.",
         "I know that a full circle is both $360°$ and $2\\pi$ radians."],
        21,
    )

    c6 = concept_block(
        "6. Graphing sine and cosine: amplitude, period, and shift",
        [
            "The parent graphs $y=\\sin(x)$ and $y=\\cos(x)$ are smooth, repeating waves that oscillate between "
            "$-1$ and $1$, completing one full cycle every $2\\pi$ radians (or $360°$). Every transformed sine "
            "or cosine graph you will see in Algebra 2 is built from stretching, compressing, and shifting these "
            "two parent waves.",
            "In the general form $y=A\\sin(Bx-C)+D$ (or the same form with cosine), the "
            "<strong>amplitude</strong> is $|A|$, describing how far the wave stretches above and below its "
            "midline. A larger $|A|$ makes taller, more dramatic waves, while a smaller $|A|$ flattens the wave "
            "closer to a straight line.",
            "The <strong>period</strong>, the horizontal length of one complete cycle, is given by "
            "$\\dfrac{2\\pi}{B}$, not by $B$ itself. This inverse relationship means a larger $B$ actually "
            "squeezes the wave into a shorter period, packing more cycles into the same horizontal distance.",
            "The <strong>phase shift</strong>, $\\dfrac{C}{B}$, slides the wave left or right, and the "
            "<strong>vertical shift</strong> $D$ raises or lowers the entire wave's midline. These four "
            "quantities — amplitude, period, phase shift, and vertical shift — completely describe any "
            "transformed sine or cosine graph.",
            "To sketch a transformed graph efficiently, find the midline (from $D$), mark the maximum and "
            "minimum heights (using the amplitude above and below the midline), and mark the horizontal length "
            "of one cycle (using the period), then sketch the characteristic wave shape connecting those "
            "landmarks.",
        ],
        "Sine and cosine graphs model anything that repeats in a smooth, periodic cycle — sound waves, seasonal "
        "temperature, the height of a point on a rotating wheel — and reading amplitude, period, and shift "
        "directly from an equation is what lets you sketch or interpret those real cycles quickly.",
        "Identify $A$, $B$, $C$, and $D$ from the equation. Compute amplitude $|A|$, period $\\dfrac{2\\pi}{B}$, "
        "phase shift $\\dfrac{C}{B}$, and vertical shift $D$ separately, then use the midline, maximum, minimum, "
        "and period length together to sketch the wave.",
        solved(1, "Describe the graph of $y=3\\sin(x)$.",
               ["Compare to the parent form: $A=3$, $B=1$, no horizontal or vertical shift.",
                "Amplitude is $|A|=3$, so the wave reaches up to $3$ and down to $-3$.",
                "Period is $\\dfrac{2\\pi}{1}=2\\pi$, the same as the parent graph."],
               "Amplitude $3$, period $2\\pi$, midline $y=0$", "", "Easy")
        + solved(2, "Describe the graph of $y=\\sin(2x)$.",
                 ["Compare to the parent form: $A=1$, $B=2$.",
                  "Amplitude is $|A|=1$, unchanged from the parent graph.",
                  "Period is $\\dfrac{2\\pi}{2}=\\pi$, so this wave completes a full cycle twice as fast as the "
                  "parent graph."],
                 "Amplitude $1$, period $\\pi$",
                 "The graph is compressed horizontally, not stretched, even though $B$ is bigger than $1$.",
                 "Medium")
        + solved(3, "Describe the graph of $y=2\\cos\\left(x-\\dfrac{\\pi}{2}\\right)+1$.",
                 ["Compare to the general form: $A=2$, $B=1$, $C=\\dfrac{\\pi}{2}$, $D=1$.",
                  "Amplitude is $|A|=2$.",
                  "Period is $\\dfrac{2\\pi}{1}=2\\pi$, unchanged from the parent graph.",
                  "Phase shift is $\\dfrac{C}{B}=\\dfrac{\\pi/2}{1}=\\dfrac{\\pi}{2}$ to the right.",
                  "Vertical shift is $D=1$, so the midline moves from $y=0$ to $y=1$."],
                 "Amplitude $2$, period $2\\pi$, phase shift $\\dfrac{\\pi}{2}$ right, midline $y=1$",
                 "With the midline at $y=1$ and amplitude $2$, this wave reaches up to $3$ and down to $-1$.",
                 "Hard"),
        ("Reading period directly off of B without dividing",
         "In $y=A\\sin(Bx)$, the period is $\\dfrac{2\\pi}{B}$, not $B$ itself. A larger $B$ actually produces a "
         "shorter, more compressed period, which feels backwards until you remember to divide."),
        ("Compute amplitude, period, and shift separately before sketching",
         "Pull out $|A|$ for amplitude, compute $\\dfrac{2\\pi}{B}$ for period, and identify the phase and "
         "vertical shifts separately, then use all of them together to place key points on the graph."),
        ["I can find the amplitude, period, phase shift, and vertical shift from a sine or cosine equation.",
         "I know the period formula is $\\dfrac{2\\pi}{B}$, so a larger $B$ means a shorter period.",
         "I can find the maximum and minimum values of a sine or cosine graph from its midline and amplitude."],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        AUDIENCE,
        [
            "Find terms and sums of arithmetic sequences and series",
            "Find terms and sums (finite and infinite) of geometric sequences and series",
            "Read and evaluate sums written in sigma notation",
            "Review right-triangle trigonometry (sine, cosine, tangent) using SOHCAHTOA",
            "Convert between degrees and radians and recall key unit-circle angle values",
            "Identify amplitude, period, and shifts to graph sine and cosine functions",
        ],
        body,
        practice_slots(31, 50),
    )
    return title, description, content, _u8_questions()


# =====================================================================================
# MASTER COURSE OVERVIEW
# =====================================================================================

def build_master():
    return f"""
<h1>Algebra 2 Complete</h1>
<p><strong>For:</strong> <strong>grade 10 Algebra 2</strong> students who want a deep, patient path through the
full year — every idea explained in plain language with LaTeX, every concept followed by quick practice, and
every unit finished off with a 50-problem set that climbs from Easy to Stretch/Honors difficulty.</p>
{why_box("Why this master course exists",
    "<p>Algebra 2 is the bridge between the procedures you memorized in Algebra 1 and the reasoning you will "
    "need in Precalculus, Calculus, and standardized tests like the SAT and ACT. Many classes move quickly and "
    "leave gaps in rational expressions, radicals, logarithms, and trig foundations. This path goes slowly and "
    "thoroughly on purpose: after every idea you get quick practice checks, and every unit ends with a full "
    "50-problem set from easy to honors-level stretch.</p>")}
{page_break()}
<h2>How to use the eight units</h2>
<ol>
<li>Unit 1 — Functions, Domain &amp; Transformations</li>
<li>Unit 2 — Quadratic Functions &amp; Equations</li>
<li>Unit 3 — Complex Numbers &amp; Completing the Square</li>
<li>Unit 4 — Polynomial Functions &amp; Factoring</li>
<li>Unit 5 — Rational Expressions &amp; Equations</li>
<li>Unit 6 — Radical Functions &amp; Rational Exponents</li>
<li>Unit 7 — Exponential &amp; Logarithmic Functions</li>
<li>Unit 8 — Sequences, Series &amp; Trig Foundations</li>
</ol>
<p>The units build on each other in a deliberate order. Factoring and equation-solving from Units 1–4 support
the rational-expression work in Unit 5, and radicals in Unit 6 lead naturally into rational exponents, which
connect directly to the exponential functions in Unit 7. Unit 8 closes the year by previewing sequences, series,
and the trigonometry that will anchor Precalculus.</p>
{think_box("Study plan",
    "<p>Work through one concept per sitting: read every paragraph slowly, study each solved example until you "
    "can reteach it out loud without looking, and only then attempt the 5 quick practice problems for that "
    "concept. End each week by finishing that unit's 50-problem set — pace yourself through Easy and Medium "
    "first, then return for Hard and Stretch once the ideas feel solid. A realistic pace is one unit every "
    "one to two weeks, depending on how much time you have outside of class.</p>")}
{page_break()}
<h2>Mindset for a full year of Algebra 2</h2>
<p>Algebra 2 rewards patience far more than speed. Every new topic — rational expressions, radicals, logarithms,
sequences, trigonometry — is built from a small number of core moves you already know: factor, find a common
denominator, isolate a variable, check a candidate solution against a domain. Recognizing those familiar moves
underneath unfamiliar-looking notation is what separates students who feel like every unit is a fresh mountain
from students who feel like every unit is the same mountain in slightly different clothing.</p>
<p>Extraneous solutions show up in rational equations, radical equations, and logarithmic equations throughout
this course. Get comfortable with the habit of writing down domain restrictions before you solve and checking
every candidate afterward — it is not extra work bolted onto the "real" algebra, it is a core part of solving
these equation types correctly.</p>
<p>Finally, explain your steps out loud, especially on the solved examples. If you can teach a concept to an
imaginary classmate in plain language, including naming the tool you used and why each step was legal, you own
that skill well enough to use it under test pressure. If you cannot yet explain a step, that is exactly the
sign to reread that section before moving on to the practice problems.</p>
"""


__all__ = [
    "build_unit5",
    "build_unit6",
    "build_unit7",
    "build_unit8",
    "build_master",
]
