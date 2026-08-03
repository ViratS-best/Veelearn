#!/usr/bin/env python3
"""Deep Algebra 2 curriculum builders (6 concepts x 5 quizzes + 50 finale = 80 Qs/unit)."""

from __future__ import annotations

import math

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
)


def _fill(qs, need, factory):
    """Grow qs to exactly `need` items using factory(i) for missing indices."""
    while len(qs) < need:
        qs.append(factory(len(qs) + 1))
    return renumber(qs[:need])


def _synthetic_divide(coeffs, root):
    """Synthetic division of a polynomial (highest degree first) by (x - root)."""
    out = [coeffs[0]]
    for c in coeffs[1:]:
        out.append(out[-1] * root + c)
    return out[:-1], out[-1]


# ===========================================================================
# UNIT 1: Functions, Domain & Transformations
# ===========================================================================

def _u1_questions():
    qs = []
    idx = 1

    # Concept 1 (1-5): function notation & vertical line test
    for text, ans, expl, dist in [
        ("If $f(x)=2x+3$, what is $f(5)$?", 13,
         "Substitute $x=5$: $f(5)=2(5)+3=10+3=13$.", None),
        ("If $f(x)=x^2-4$, what is $f(-3)$?", 5,
         "Substitute $x=-3$: $f(-3)=(-3)^2-4=9-4=5$.", None),
        ("If $g(x)=4x-9$ and $g(x)=7$, what is $x$?", 4,
         "Set $4x-9=7$, so $4x=16$, so $x=4$.", None),
        ("A graph contains the points $(2,1)$, $(2,6)$, and $(5,3)$. Is this graph a function?", "No",
         "The input $x=2$ produces two different outputs, $1$ and $6$. A vertical line at $x=2$ crosses the graph "
         "twice, so it fails the vertical line test and is not a function.",
         ["Yes", "Cannot tell without a picture", "Only if the point $(2,6)$ is removed"]),
        ("If $f(x)=\\sqrt{x+5}$, what is $f(4)$?", 3,
         "Substitute $x=4$: $f(4)=\\sqrt{4+5}=\\sqrt{9}=3$.", None),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Concept 2 (6-10): domain & range
    for text, ans, expl, dist in [
        ("What is the domain of $f(x)=\\dfrac{1}{x-7}$?", "x\u22607",
         "The denominator cannot equal $0$, so $x-7\\neq0$, which means $x\\neq7$.",
         ["x=7", "x\u2265 7", "all real numbers"]),
        ("What is the domain of $f(x)=\\sqrt{x-2}$?", "x\u22652",
         "The expression under an even root must be $\\geq 0$: $x-2\\geq0$, so $x\\geq2$.",
         ["x\u22642", "x>2", "all real numbers"]),
        ("What is the domain of $f(x)=\\dfrac{1}{x^2-16}$?", "x\u22604 and x\u2260-4",
         "The denominator is zero when $x^2=16$, so $x=4$ or $x=-4$ are excluded from the domain.",
         ["x\u22604 only", "x\u2260-4 only", "x\u226016"]),
        ("What is the range of $f(x)=x^2+3$?", "y\u22653",
         "$x^2$ is never negative, so the smallest output happens at $x=0$, giving $y=3$. Every output is $3$ or larger.",
         ["y\u2264 3", "y\u2260 3", "all real numbers"]),
        ("What is the domain of $f(x)=\\sqrt{16-x^2}$?", "-4\u2264x\u22644",
         "We need $16-x^2\\geq0$, which means $x^2\\leq16$, which means $-4\\leq x\\leq4$.",
         ["x\u22654 or x\u2264-4", "x\u22650", "-16\u2264x\u226416"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Concept 3 (11-15): parent functions
    for text, ans, expl, dist in [
        ("The parent function $f(x)=|x|$ is called the:", "absolute value function",
         "Its graph is a V shape formed by two rays meeting at the origin; it is the absolute value parent function.",
         ["quadratic function", "square root function", "reciprocal function"]),
        ("The reciprocal parent function $f(x)=\\dfrac{1}{x}$ has a vertical asymptote at:", "x=0",
         "Division by $0$ is undefined, so the graph never touches the vertical line $x=0$; it is a vertical asymptote.",
         ["x=1", "y=0", "x=-1"]),
        ("The parent square root function $f(x)=\\sqrt{x}$ has domain:", "x\u22650",
         "You cannot take the square root of a negative real number, so only $x\\geq0$ is allowed.",
         ["x\u22640", "all real numbers", "x>0 only"]),
        ("What is the vertex of the parent quadratic function $f(x)=x^2$?", "(0,0)",
         "$f(x)=x^2$ has its minimum point exactly at the origin, $(0,0)$.",
         ["(1,0)", "(0,1)", "(1,1)"]),
        ("The range of the reciprocal parent function $f(x)=\\dfrac{1}{x}$ excludes which value?", "y=0",
         "No matter what $x$ you plug in, $\\dfrac{1}{x}$ can never equal $0$, so $y=0$ is never in the range.",
         ["y=1", "y=-1", "no values are excluded"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Concept 4 (16-20): transformations
    for text, ans, expl, dist in [
        ("$g(x)=(x-3)^2+2$ is a transformation of $f(x)=x^2$. Describe it.", "right 3, up 2",
         "Inside the parentheses, $x-3$ shifts the graph right $3$; the $+2$ outside shifts it up $2$.",
         ["left 3, up 2", "right 3, down 2", "left 3, down 2"]),
        ("$g(x)=-2x^2$ compared to $f(x)=x^2$ is best described as:", "reflect over the x-axis and vertical stretch by 2",
         "The negative sign flips the parabola upside down (reflection over the x-axis), and the factor of $2$ makes it narrower (vertical stretch by 2).",
         ["reflect over the y-axis only", "vertical shrink by 2", "horizontal shift right 2"]),
        ("If $f(x)=\\sqrt{x}$ and $g(x)=\\sqrt{x+4}-1$, what is $g(5)$?", 2,
         "$g(5)=\\sqrt{5+4}-1=\\sqrt{9}-1=3-1=2$.", None),
        ("The graph of $y=f(x-2)$ is the graph of $y=f(x)$ shifted:", "right 2",
         "Replacing $x$ with $x-2$ inside the function shifts every point on the graph $2$ units to the right.",
         ["left 2", "up 2", "down 2"]),
        ("If $f(x)=|2x|$, what is $f(3)$?", 6,
         "$f(3)=|2(3)|=|6|=6$.", None),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Concept 5 (21-25): piecewise, g(x) = 2x if x<=1, x+3 if x>1
    for text, ans, expl in [
        ("For $g(x)=\\begin{cases}2x & x\\leq1\\\\ x+3 & x>1\\end{cases}$, find $g(1)$.", 2,
         "Since $1\\leq1$, use the first piece: $g(1)=2(1)=2$."),
        ("For $g(x)=\\begin{cases}2x & x\\leq1\\\\ x+3 & x>1\\end{cases}$, find $g(4)$.", 7,
         "Since $4>1$, use the second piece: $g(4)=4+3=7$."),
        ("For $g(x)=\\begin{cases}2x & x\\leq1\\\\ x+3 & x>1\\end{cases}$, find $g(-3)$.", -6,
         "Since $-3\\leq1$, use the first piece: $g(-3)=2(-3)=-6$."),
        ("For $g(x)=\\begin{cases}2x & x\\leq1\\\\ x+3 & x>1\\end{cases}$, find $g(0)$.", 0,
         "Since $0\\leq1$, use the first piece: $g(0)=2(0)=0$."),
        ("For $g(x)=\\begin{cases}2x & x\\leq1\\\\ x+3 & x>1\\end{cases}$, find $g(2)$.", 5,
         "Since $2>1$, use the second piece: $g(2)=2+3=5$."),
    ]:
        qs.append(mq(text, ans, expl, idx)); idx += 1

    # Concept 6 (26-30): inverse functions
    for text, ans, expl, dist in [
        ("If $f(x)=2x+6$, what is $f^{-1}(x)$?", "(x-6)/2",
         "Write $y=2x+6$, swap $x$ and $y$ to get $x=2y+6$, then solve for $y$: $y=\\dfrac{x-6}{2}$.",
         ["(x+6)/2", "2x-6", "(x-6)\u00d72"]),
        ("If $f(x)=3x-1$, what is $f^{-1}(5)$?", 2,
         "Solve $3x-1=5$: $3x=6$, so $x=2$. That means $f^{-1}(5)=2$.", None),
        ("If $f(2)=9$ and $f$ has an inverse, what is $f^{-1}(9)$?", 2,
         "The inverse undoes $f$, so if $f$ sends $2$ to $9$, then $f^{-1}$ sends $9$ back to $2$.", None),
        ("If $f(x)=x^2$ with domain $x\\geq0$, what is $f^{-1}(16)$?", 4,
         "Restricting to $x\\geq0$ makes $f$ one-to-one. Its inverse is $f^{-1}(x)=\\sqrt{x}$, so $f^{-1}(16)=\\sqrt{16}=4$.", None),
        ("The graph of the inverse of $y=f(x)$ is obtained from the original graph by:", "reflecting over the line y=x",
         "Swapping $x$ and $y$ in the equation corresponds geometrically to reflecting every point over the line $y=x$.",
         ["reflecting over the x-axis", "reflecting over the y-axis", "shifting up 1 unit"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Finale (31-80): 50 progressive problems
    finale = []

    # A. Evaluate linear functions (10)
    for a, b, x in [(2, 5, 3), (4, -3, 5), (-2, 7, 4), (3, 0, 6), (-1, 10, 4),
                    (6, -5, 2), (2, -8, 10), (-3, 1, -2), (5, 2, -3), (1, -1, 20)]:
        val = a * x + b
        finale.append(mq(
            f"If $f(x)={a}x{'+' if b >= 0 else ''}{b}$, what is $f({x})$?",
            val,
            f"Substitute $x={x}$: $f({x})={a}({x}){'+' if b >= 0 else ''}{b}={val}$.",
            0,
        ))

    # B. Evaluate quadratic functions (8)
    for b, c, x in [(-2, 1, 3), (3, -4, 2), (0, 5, -3), (-5, 6, 1),
                    (4, 0, -2), (1, -6, 5), (-3, -4, 0), (2, 1, -4)]:
        val = x * x + b * x + c
        finale.append(mq(
            f"If $f(x)=x^2{'+' if b >= 0 else ''}{b}x{'+' if c >= 0 else ''}{c}$, what is $f({x})$?",
            val,
            f"Substitute $x={x}$: $({x})^2{'+' if b >= 0 else ''}{b}({x}){'+' if c >= 0 else ''}{c}={val}$.",
            0,
        ))

    # C. Domain of 1/(x-k) (6)
    for k in [3, -2, 7, 0, -5, 10]:
        neg = -k
        finale.append(mq(
            f"What is the domain of $f(x)=\\dfrac{{1}}{{x-({k})}}$?",
            f"x\u2260{k}",
            f"The denominator cannot be $0$, so $x\\neq{k}$.",
            0,
            distractors=[f"x\u2260{neg}", f"x={k}", "all real numbers"],
        ))

    # D. Domain of sqrt(x-k) (6)
    for k in [5, -3, 8, 0, -6, 2]:
        finale.append(mq(
            f"What is the domain of $f(x)=\\sqrt{{x-({k})}}$?",
            f"x\u2265{k}",
            f"We need $x-({k})\\geq0$, so $x\\geq{k}$.",
            0,
            distractors=[f"x\u2264{k}", f"x\u2265{-k}", "all real numbers"],
        ))

    # E. Transformation evaluation g(x)=(x-h)^2+k (5)
    for h, k, x0 in [(2, 3, 5), (5, -1, 5), (-3, 4, 0), (-2, -6, -2), (7, 0, 10)]:
        val = (x0 - h) ** 2 + k
        finale.append(mq(
            f"If $g(x)=(x-({h}))^2+({k})$, what is $g({x0})$?",
            val,
            f"Substitute: $(({x0})-({h}))^2+({k})={val}$.",
            0,
        ))

    # F. Piecewise evaluation h(x) = 3x if x<2, x^2+1 if x>=2 (5)
    for x0 in [-1, 0, 2, 5, -4]:
        val = 3 * x0 if x0 < 2 else x0 * x0 + 1
        piece = "3x" if x0 < 2 else "x^2+1"
        finale.append(mq(
            f"For $h(x)=\\begin{{cases}}3x & x<2\\\\ x^2+1 & x\\geq2\\end{{cases}}$, find $h({x0})$.",
            val,
            f"Since ${x0}$ falls in the piece ${piece}$, $h({x0})={val}$.",
            0,
        ))

    # G. Inverse of linear functions (5)
    for a, b, c in [(2, 3, 11), (5, -4, 16), (3, 7, 19), (-2, 5, -1), (4, -9, 15)]:
        val = (c - b) // a
        finale.append(mq(
            f"If $f(x)={a}x{'+' if b >= 0 else ''}{b}$, what value of $x$ gives $f(x)={c}$? (This is $f^{{-1}}({c})$.)",
            val,
            f"Solve ${a}x{'+' if b >= 0 else ''}{b}={c}$: $x=\\dfrac{{{c}-({b})}}{{{a}}}={val}$.",
            0,
        ))

    # H. Composite functions f(g(x)) (5), f(x)=x+3, g(x)=2x
    for x0 in [4, -2, 0, 5, -6]:
        g_val = 2 * x0
        f_val = g_val + 3
        finale.append(mq(
            f"If $f(x)=x+3$ and $g(x)=2x$, what is $f(g({x0}))$?",
            f_val,
            f"First $g({x0})=2({x0})={g_val}$. Then $f({g_val})={g_val}+3={f_val}$.",
            0,
        ))

    while len(finale) < 50:
        n = len(finale) + 1
        finale.append(mq(
            f"If $f(x)=x+{n}$, what is $f(0)$?",
            n,
            f"$f(0)=0+{n}={n}$.",
            0,
        ))

    qs.extend(finale[:50])
    return _fill(qs, 80, lambda i: mq(f"If $f(x)=2x$, what is $f({i})$?", 2 * i, f"$f({i})=2({i})={2*i}$.", i))


def build_unit1():
    title = "Algebra 2 Unit 1: Functions, Domain & Transformations"
    description = (
        "A deep, patient introduction to function notation, domain and range, the five key parent "
        "functions, transformations, piecewise functions, and inverse functions — with five quick "
        "checks after every idea and a 50-problem practice set to finish."
    )

    c1 = concept_block(
        "1. Function notation, inputs, outputs, and the vertical line test",
        [
            "A function is a rule that connects every allowed input to exactly one output. No matter how many "
            "times you use the same input, a true function always hands back the same answer.",
            "We write $f(x)$ to mean “the output of the function $f$ when the input is $x$.” The letter inside "
            "the parentheses is not multiplication; it is naming which input goes into the machine.",
            "Evaluating a function means substituting a specific number, or even an expression, for $x$ and then "
            "simplifying carefully, one operation at a time, in the correct order.",
            "The vertical line test is a graphical shortcut for deciding whether a graph represents a function: "
            "if any vertical line crosses the graph more than once, that input has two different outputs, so the "
            "graph fails to be a function.",
            "Function notation is the language of the rest of Algebra 2. Quadratics, polynomials, and later "
            "exponential and logarithmic rules are all simply specific families of functions written this way.",
            "Getting comfortable now with $f(x)$, $f(a+1)$, and solving equations like $f(x)=k$ will make every "
            "later unit in this course read far more smoothly.",
        ],
        "Function notation is the shared language of the rest of Algebra 2 and Precalculus. Misreading "
        "$f(x+2)$ as $f(x)+2$ is a small mistake that quietly causes wrong answers for years if it is never fixed.",
        "Read $f(x)$ like a machine: whatever sits inside the parentheses gets substituted for every single "
        "$x$ in the rule, and only then do you simplify, left to right, following order of operations.",
        solved(1, "If $f(x)=2x+3$, find $f(4)$.",
               ["Substitute $4$ for every $x$ in the rule: $f(4)=2(4)+3$.",
                "Multiply first: $2(4)=8$.",
                "Add: $8+3=11$."],
               "$11$", "", "Easy")
        + solved(2, "If $f(x)=x^2-5x+1$, find $f(-2)$.",
                 ["Substitute $-2$ for every $x$: $f(-2)=(-2)^2-5(-2)+1$.",
                  "Square first: $(-2)^2=4$.",
                  "Multiply: $-5(-2)=10$.",
                  "Add everything: $4+10+1=15$."],
                 "$15$", "Notice the double negative from $-5$ times $-2$ becomes a positive $10$.", "Medium")
        + solved(3, "If $f(x)=x^2+1$, find $f(a+1)$ in terms of $a$.",
                 ["Substitute the entire expression $a+1$ for every $x$: $f(a+1)=(a+1)^2+1$.",
                  "Expand the square carefully: $(a+1)^2=a^2+2a+1$.",
                  "Add the $+1$ from the original rule: $a^2+2a+1+1=a^2+2a+2$."],
                 "$a^2+2a+2$", "This kind of substitution shows up constantly once you study rates of change.", "Hard"),
        ("Confusing $f(x+2)$ with $f(x)+2$",
         "These look similar but mean completely different things. $f(x+2)$ means substitute the whole "
         "expression $x+2$ everywhere an $x$ appears in the rule, before you simplify anything. $f(x)+2$ means "
         "evaluate $f$ at $x$ first, using the original rule, and only add $2$ to that result afterward. Mixing "
         "these up is one of the most common early Algebra 2 mistakes, and it silently breaks every later "
         "transformation and composition problem that depends on reading notation correctly."),
        ("Circle every $x$ before you substitute",
         "Before touching the algebra, physically circle or highlight each occurrence of $x$ in the rule. Then "
         "write the new input in every circled spot at the same time, using parentheses around it. This habit "
         "prevents you from accidentally leaving one $x$ un-substituted, especially in longer rules with an $x$ "
         "appearing two or three times."),
        [
            "I can evaluate $f(x)$ at a specific number by substituting carefully and simplifying in order.",
            "I can evaluate an expression like $f(a+1)$ by substituting the whole expression for every $x$.",
            "I can use the vertical line test to decide whether a graph represents a function.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Domain and range from equations and graphs",
        [
            "The domain of a function is the complete set of allowed input values; the range is the complete "
            "set of output values the function actually produces.",
            "Two situations create restrictions you must watch for in Algebra 2: a denominator that could "
            "become $0$, and an even root (like a square root) whose inside expression could become negative.",
            "For a fraction like $\\dfrac{1}{x-4}$, the domain excludes any $x$ that makes the denominator "
            "exactly $0$, because division by zero is undefined.",
            "For a square root like $\\sqrt{x-5}$, the domain requires the expression underneath the radical to "
            "be greater than or equal to $0$, since square roots of negative real numbers are not real numbers.",
            "Range questions are often easier to answer from a graph or from a rewritten form, such as vertex "
            "form for a parabola, which instantly reveals the lowest or highest output value.",
            "Whenever a function combines several pieces, write down every restriction separately first, then "
            "combine them at the very end into one final domain statement.",
        ],
        "Every later topic — rational expressions, radicals, logarithms — inherits this exact idea of restricted "
        "domain. If you build the habit now of checking denominators and even roots first, later units feel familiar "
        "instead of frightening.",
        "Before solving anything else, ask two questions: is there a denominator that could be zero, and is "
        "there an even root whose inside could be negative? Write each restriction as its own inequality, then "
        "combine them.",
        solved(4, "Find the domain of $f(x)=\\dfrac{1}{x-4}$.",
               ["The denominator cannot equal $0$: set $x-4\\neq0$.",
                "Solve: $x\\neq4$.",
                "Every other real number is allowed."],
               "$x\\neq4$", "", "Easy")
        + solved(5, "Find the domain of $f(x)=\\sqrt{x-5}$.",
                 ["The inside of an even root must be $\\geq0$: $x-5\\geq0$.",
                  "Solve: $x\\geq5$."],
                 "$x\\geq5$", "", "Medium")
        + solved(6, "Find the domain of $f(x)=\\dfrac{1}{\\sqrt{9-x^2}}$.",
                 ["This function has both a denominator and a square root, and the root is itself in the denominator, "
                  "so the inside must be strictly positive, not just $\\geq0$.",
                  "Set $9-x^2>0$.",
                  "Rewrite as $x^2<9$.",
                  "Solve: $-3<x<3$."],
                 "$-3<x<3$", "Because the root sits under the fraction bar, equality is not allowed — it would still "
                             "make the denominator $0$.", "Hard"),
        ("Allowing the denominator to equal zero",
         "Students sometimes solve the “bad” equation (like $x-4=0$) and then forget to exclude that value, "
         "accidentally leaving it inside the domain. Division by zero is always undefined, with no exceptions, "
         "so any value that zeroes out a denominator must be removed from the domain, every single time."),
        ("Write two rules before combining them",
         "When a function mixes a denominator and an even root, resist the urge to solve everything in one "
         "messy step. Write the denominator-not-zero rule on one line and the root-nonnegative rule on another "
         "line, solve each completely, and only then merge them into a single domain statement."),
        [
            "I can find the domain of a rational function by setting the denominator not equal to zero.",
            "I can find the domain of a square-root function by requiring the inside to be nonnegative.",
            "I can combine two restrictions into one correct domain statement.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Parent functions: linear, quadratic, absolute value, square root, and reciprocal",
        [
            "A parent function is the simplest version of a family of functions — no shifts, no stretches, "
            "just the basic shape you build every transformation from later in this unit.",
            "The linear parent function $f(x)=x$ is a straight line through the origin with slope $1$; every "
            "other line is a transformation of this shape.",
            "The quadratic parent function $f(x)=x^2$ is a U-shaped parabola with its lowest point, the vertex, "
            "at the origin $(0,0)$.",
            "The absolute value parent function $f(x)=|x|$ makes a V shape, since it reflects every negative "
            "output back to positive, meeting at a sharp corner at the origin.",
            "The square root parent function $f(x)=\\sqrt{x}$ only exists for $x\\geq0$ and grows more and more "
            "slowly as $x$ increases, curving gently upward from the origin.",
            "The reciprocal parent function $f(x)=\\dfrac{1}{x}$ has two separate branches that approach, but "
            "never touch, the vertical line $x=0$ and the horizontal line $y=0$.",
        ],
        "Once you know these five shapes cold, every transformed graph in this unit becomes a matter of "
        "shifting, stretching, or reflecting a shape you already recognize instantly, instead of plotting points "
        "from scratch.",
        "For any new function, first ask which parent family it belongs to. Then picture that parent shape in "
        "your head before applying any shifts, stretches, or reflections on top of it.",
        solved(7, "For the parent quadratic $f(x)=x^2$, find $f(-3)$ and state the vertex.",
               ["Substitute $x=-3$: $f(-3)=(-3)^2=9$.",
                "The vertex of $f(x)=x^2$ is the lowest point of the U shape, which is $(0,0)$."],
               "$f(-3)=9$; vertex $(0,0)$", "", "Easy")
        + solved(8, "For the absolute value parent function $f(x)=|x|$, find $f(-7)$ and describe the graph shape.",
                 ["Substitute $x=-7$: $f(-7)=|-7|=7$.",
                  "The graph is a V shape with its corner (vertex) at the origin, opening upward."],
                 "$f(-7)=7$; V shape", "", "Medium")
        + solved(9, "For the reciprocal parent function $f(x)=\\dfrac{1}{x}$, find $f(2)$ and describe both asymptotes.",
                 ["Substitute $x=2$: $f(2)=\\dfrac{1}{2}$.",
                  "The vertical asymptote is at $x=0$, since the function is undefined there.",
                  "The horizontal asymptote is at $y=0$, since $\\dfrac{1}{x}$ gets closer and closer to $0$ but "
                  "never reaches it as $x$ grows large in either direction."],
                 "$f(2)=\\dfrac{1}{2}$; asymptotes $x=0$ and $y=0$", "", "Honors"),
        ("Mixing up the square root and reciprocal shapes",
         "Both the square root parent function and the reciprocal parent function look unfamiliar compared to "
         "lines and parabolas, and students sometimes swap their key features. The square root graph starts at "
         "the origin and only exists for $x\\geq0$; the reciprocal graph never touches either axis and exists on "
         "both sides of $x=0$, split into two separate curved branches."),
        ("Memorize five tiny reference sketches",
         "Draw a small thumbnail of each of the five parent functions — line, parabola, V shape, square root "
         "curve, and reciprocal branches — on an index card or in the front of your notebook. Glancing at these "
         "five shapes before a transformation problem turns a confusing graph into a quick shift-and-stretch "
         "exercise."),
        [
            "I can name and sketch the five parent functions from memory.",
            "I can evaluate any parent function at a given input.",
            "I can describe the domain, range, and key features of each parent function.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Transformations: $y=a\\,f(b(x-h))+k$ in the correct order",
        [
            "A transformation takes a parent function and shifts, stretches, or reflects its graph without "
            "changing its basic family shape.",
            "In the form $y=a\\,f(b(x-h))+k$, the number $h$ shifts the graph horizontally, $k$ shifts it "
            "vertically, $a$ stretches or reflects it vertically, and $b$ stretches or reflects it horizontally.",
            "A common early confusion is the sign inside the parentheses: $x-h$ shifts the graph right by $h$ "
            "when $h$ is positive, even though it looks like subtraction should move things left.",
            "Negative values of $a$ flip the graph upside down (a reflection over the x-axis); values of $|a|$ "
            "greater than $1$ stretch the graph vertically, while values between $0$ and $1$ compress it.",
            "The safest strategy is to handle transformations in a fixed order every time: horizontal shift and "
            "horizontal stretch/reflection first (since they happen to $x$ before anything else), then vertical "
            "stretch/reflection, then vertical shift last.",
            "Once you can read a transformed equation and immediately picture the graph, you save enormous time "
            "on graphing problems throughout Algebra 2 and Precalculus.",
        ],
        "Nearly every family of function you study from here forward — quadratics, absolute value, radicals, "
        "later exponentials and logarithms — gets graphed using this exact same transformation language.",
        "List the transformations in words first: “shift right $h$, stretch vertically by $a$, shift up $k$.” "
        "Only after that sentence is correct should you plot points or sketch the curve.",
        solved(10, "$f(x)=x^2$. Describe the transformation to $g(x)=(x-3)^2+2$ and find $g(3)$.",
               ["Compare to the parent form $a\\,f(b(x-h))+k$: here $h=3$ and $k=2$.",
                "So the graph shifts right $3$ and up $2$ from the parent parabola.",
                "Evaluate: $g(3)=(3-3)^2+2=0+2=2$."],
               "Right 3, up 2; $g(3)=2$", "", "Easy")
        + solved(11, "$f(x)=\\sqrt{x}$. Describe and evaluate $g(x)=-\\sqrt{x+4}-1$ at $x=0$.",
                 ["Rewrite $x+4$ as $x-(-4)$, so $h=-4$: shift left $4$.",
                  "The negative sign in front means reflect over the x-axis.",
                  "The $-1$ at the end shifts down $1$.",
                  "Evaluate: $g(0)=-\\sqrt{0+4}-1=-\\sqrt{4}-1=-2-1=-3$."],
                 "Left 4, reflect over x-axis, down 1; $g(0)=-3$", "", "Medium")
        + solved(12, "$f(x)=|x|$. Describe and evaluate $g(x)=2|x-1|-5$ at $x=4$.",
                 ["Here $h=1$ (shift right $1$), $a=2$ (vertical stretch by factor $2$), $k=-5$ (shift down $5$).",
                  "Evaluate step by step: $g(4)=2|4-1|-5$.",
                  "Simplify inside the absolute value: $|3|=3$.",
                  "Multiply: $2(3)=6$.",
                  "Subtract: $6-5=1$."],
                 "Right 1, stretch by 2, down 5; $g(4)=1$", "", "Hard"),
        ("Reading the horizontal shift direction backwards",
         "Because the rule uses $x-h$, students very often think a plus sign inside means “shift right” and a "
         "minus sign means “shift left,” which is exactly backwards. Rewrite every horizontal shift in the form "
         "$x-h$ first: if you see $x+4$, rewrite it as $x-(-4)$ so $h=-4$, confirming a shift left by $4$, not right."),
        ("List transformations in a fixed order",
         "Always process horizontal changes (shift and stretch, since they act on $x$ before the function is "
         "applied) before vertical changes (stretch and shift, which act on the output afterward). Writing this "
         "list out in words every time — even for “easy” problems — prevents small order-of-operations mistakes "
         "on quiz day."),
        [
            "I can identify $h$, $k$, and $a$ from a transformed equation.",
            "I can describe a transformation in words: shift, stretch, and reflect, in the correct order.",
            "I can evaluate a transformed function at a specific input.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Piecewise functions and evaluating them correctly",
        [
            "A piecewise function is defined by different rules on different parts of its domain, so the very "
            "first step in evaluating one is always deciding which rule applies to your specific input.",
            "Piecewise functions appear constantly in real life: tax brackets, shipping costs, and speed limits "
            "that change by zone are all naturally piecewise.",
            "The boundary between two pieces is usually marked with an inequality symbol, and whether that symbol "
            "is strict ($<$, $>$) or includes equality ($\\leq$, $\\geq$) decides exactly which rule owns that "
            "boundary point.",
            "A safe habit is to underline or circle every inequality symbol in the piecewise definition before "
            "you substitute any numbers, so you do not accidentally use the wrong rule at a boundary value.",
            "Only one rule should ever apply to any single input value; if your piecewise definition seems to "
            "allow two rules at the same point, double check the inequality symbols for a mistake.",
            "Piecewise functions build directly toward absolute value functions (which are secretly piecewise) "
            "and later toward step functions and other real-world modeling tools.",
        ],
        "Piecewise thinking — “which rule applies here?” — becomes essential later when you study inequalities, "
        "absolute value equations, and real-world models with changing rates.",
        "Before evaluating, write the input number next to each inequality in the definition and decide, on "
        "paper, which single inequality is true. Only then substitute into that one rule.",
        solved(13, "For $f(x)=\\begin{cases}x+1 & x<0\\\\ x^2 & 0\\leq x<3\\\\ 2x-1 & x\\geq3\\end{cases}$, find $f(-2)$.",
               ["Check which piece applies: is $-2<0$? Yes.",
                "Use the first rule: $f(-2)=-2+1=-1$."],
               "$-1$", "", "Easy")
        + solved(14, "Using the same $f$ from above, find $f(2)$.",
                 ["Check the pieces: is $2<0$? No. Is $0\\leq2<3$? Yes.",
                  "Use the second rule: $f(2)=2^2=4$."],
                 "$4$", "", "Medium")
        + solved(15, "Using the same $f$ from above, find $f(3)$.",
                 ["Check the pieces carefully at the boundary: is $3<0$? No. Is $0\\leq3<3$? No, because $3$ is "
                  "not strictly less than $3$.",
                  "So the third piece owns $x=3$: is $3\\geq3$? Yes.",
                  "Use the third rule: $f(3)=2(3)-1=5$."],
                 "$5$", "Boundary values are exactly where careless reading causes mistakes — always check the "
                        "symbol, not just the number.", "Hard"),
        ("Using the wrong boundary piece",
         "When the input equals a boundary number exactly, it is tempting to plug it into whichever rule looks "
         "closest or easiest, instead of checking the inequality symbols. A boundary point belongs to exactly "
         "one rule, decided by whether that rule’s inequality includes equality ($\\leq$ or $\\geq$) or not."),
        ("Underline the inequality symbols first",
         "Before evaluating, underline every $<$, $\\leq$, $>$, and $\\geq$ in the piecewise definition. Then "
         "write the input value beside each underlined inequality and mark true or false. This turns a confusing "
         "boundary case into a simple true/false check."),
        [
            "I can identify which rule of a piecewise function applies to a given input.",
            "I can evaluate piecewise functions correctly at boundary values.",
            "I can explain why only one rule should ever apply to a single input.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Inverse functions: swap x and y, restrict domain when needed",
        [
            "The inverse of a function undoes what the original function did: if $f$ sends $2$ to $9$, then "
            "$f^{-1}$ sends $9$ back to $2$.",
            "The standard process is to write $y=f(x)$, swap the letters $x$ and $y$, and then solve the new "
            "equation for $y$; the result is $f^{-1}(x)$.",
            "For an inverse to be a true function itself, the original function must be one-to-one, meaning no "
            "two different inputs ever produce the same output.",
            "Functions like $f(x)=x^2$ are not one-to-one over all real numbers, since both $2$ and $-2$ give "
            "the same output $4$; restricting the domain to $x\\geq0$ fixes this so an inverse function can exist.",
            "You can always check an inverse by composing it with the original function: if $f^{-1}(f(x))=x$ for "
            "every allowed $x$, the inverse is correct.",
            "Graphically, the graph of $f^{-1}$ is always the reflection of the graph of $f$ over the line $y=x$.",
        ],
        "Inverse functions are the key idea behind solving equations by “undoing” operations, and they return "
        "in force when you study logarithms as the official inverse of exponential functions.",
        "Write $y=f(x)$, swap $x$ and $y$, then solve for $y$ using the same algebra tools (adding, dividing, "
        "square rooting) you already know, one step at a time.",
        solved(16, "Find the inverse of $f(x)=2x+6$.",
               ["Write $y=2x+6$.",
                "Swap $x$ and $y$: $x=2y+6$.",
                "Solve for $y$: subtract $6$ from both sides, $x-6=2y$.",
                "Divide by $2$: $y=\\dfrac{x-6}{2}$."],
               "$f^{-1}(x)=\\dfrac{x-6}{2}$", "Check: $f(f^{-1}(x))=2\\left(\\dfrac{x-6}{2}\\right)+6=x-6+6=x$. ✓", "Easy")
        + solved(17, "If $f(x)=3x-1$, find $f^{-1}(5)$.",
                 ["You want the input that makes $f(x)=5$: solve $3x-1=5$.",
                  "Add $1$: $3x=6$.",
                  "Divide by $3$: $x=2$."],
                 "$f^{-1}(5)=2$", "", "Medium")
        + solved(18, "If $f(x)=x^2$ with domain restricted to $x\\geq0$, find and evaluate $f^{-1}(16)$.",
                 ["Because the domain is restricted to $x\\geq0$, $f$ is one-to-one and has an inverse.",
                  "Write $y=x^2$, swap: $x=y^2$, and solve for $y$ using only the positive branch: $y=\\sqrt{x}$.",
                  "So $f^{-1}(x)=\\sqrt{x}$.",
                  "Evaluate: $f^{-1}(16)=\\sqrt{16}=4$."],
                 "$f^{-1}(16)=4$", "Without the domain restriction, $x^2$ is not one-to-one and would not have a "
                                   "single inverse function.", "Hard"),
        ("Forgetting to restrict the domain first",
         "Functions like $f(x)=x^2$ send two different inputs, such as $3$ and $-3$, to the same output, $9$. "
         "Without restricting the domain to remove one of those branches, there is no way to “undo” the function "
         "uniquely, so the inverse would not itself be a function. Always check whether the original function is "
         "one-to-one before writing an inverse with confidence."),
        ("Check your inverse by composing",
         "After finding $f^{-1}(x)$, pick a convenient input, run it through $f$, then run the result through "
         "$f^{-1}$, and confirm you land back on the original number. This ten-second check catches algebra "
         "mistakes made while swapping and solving."),
        [
            "I can find the inverse of a linear function by swapping and solving.",
            "I can explain why some functions need a restricted domain before they have an inverse.",
            "I can check whether an inverse is correct by composing it with the original function.",
        ],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        "Grade 10 Algebra 2",
        [
            "Read and evaluate function notation, and use the vertical line test",
            "Find the domain and range of equations and graphs",
            "Recognize the five key parent functions",
            "Graph transformations using $y=a\\,f(b(x-h))+k$",
            "Evaluate piecewise functions correctly at every input, including boundaries",
            "Find and verify inverse functions, restricting domain when needed",
        ],
        body,
        practice_slots(31, 50),
    )
    return title, description, content, _u1_questions()


# ===========================================================================
# UNIT 2: Quadratic Functions & Equations
# ===========================================================================

def _u2_questions():
    qs = []
    idx = 1

    # Concept 1 (1-5): forms of a quadratic
    for text, ans, expl, dist in [
        ("Expand $y=(x-3)^2+5$ into standard form.", "x^2-6x+14",
         "Expand the square: $(x-3)^2=x^2-6x+9$. Add the $5$: $x^2-6x+9+5=x^2-6x+14$.",
         ["x^2-6x+5", "x^2+6x+14", "x^2-3x+14"]),
        ("Find the vertex of $y=(x+2)^2-9$ (vertex form).", "(-2,-9)",
         "Vertex form is $a(x-h)^2+k$ with vertex $(h,k)$. Here $x+2=x-(-2)$, so $h=-2$ and $k=-9$.",
         ["(2,-9)", "(-2,9)", "(2,9)"]),
        ("Convert $y=x^2-4x+7$ to vertex form.", "(x-2)^2+3",
         "The vertex's $x$-coordinate is $h=-\\dfrac{b}{2a}=-\\dfrac{-4}{2}=2$. Then $k=f(2)=4-8+7=3$, so vertex "
         "form is $(x-2)^2+3$.",
         ["(x+2)^2+3", "(x-2)^2-3", "(x-4)^2+7"]),
        ("Write the intercept form of a quadratic with $x$-intercepts $3$ and $-5$ and leading coefficient $1$.",
         "y=(x-3)(x+5)",
         "Intercept form is $y=a(x-p)(x-q)$ where $p,q$ are the $x$-intercepts, so $y=(x-3)(x-(-5))=(x-3)(x+5)$.",
         ["y=(x+3)(x-5)", "y=(x-3)(x-5)", "y=(x+3)(x+5)"]),
        ("Expand $y=3(x-1)(x+2)$ into standard form.", "3x^2+3x-6",
         "First multiply $(x-1)(x+2)=x^2+x-2$. Then distribute the $3$: $3x^2+3x-6$.",
         ["3x^2-3x-6", "x^2+x-2", "3x^2+3x+6"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Concept 2 (6-10): graphing features
    for text, ans, expl, dist in [
        ("What is the axis of symmetry of $y=x^2-8x+12$?", "x=4",
         "The axis of symmetry is $x=-\\dfrac{b}{2a}=-\\dfrac{-8}{2}=4$.",
         ["x=-4", "x=8", "x=6"]),
        ("What is the $y$-intercept of $y=2x^2+5x-3$?", -3,
         "The $y$-intercept is the value when $x=0$: $2(0)^2+5(0)-3=-3$.", None),
        ("What are the $x$-intercepts of $y=x^2-5x+6$?", "2,3",
         "Factor: $x^2-5x+6=(x-2)(x-3)$, so the $x$-intercepts are $x=2$ and $x=3$.",
         ["-2,-3", "1,6", "2,-3"]),
        ("What is the vertex of $y=(x-5)^2+7$?", "(5,7)",
         "In vertex form $a(x-h)^2+k$, the vertex is $(h,k)=(5,7)$.",
         ["(-5,7)", "(5,-7)", "(-5,-7)"]),
        ("As $x\\to\\infty$, what happens to $y=-x^2+4$?", "y\u2192-\u221e",
         "Because the leading coefficient is negative and the degree is even, both ends of the parabola point "
         "downward, so $y\\to-\\infty$ as $x\\to\\infty$.",
         ["y\u2192\u221e", "y\u21920", "y\u21924"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Concept 3 (11-15): solving by factoring
    for text, ans, expl, dist in [
        ("Solve $x^2-5x+6=0$ by factoring.", "x=2,3",
         "Factor: $(x-2)(x-3)=0$. By the zero product property, $x=2$ or $x=3$.",
         ["x=-2,-3", "x=1,6", "x=-2,3"]),
        ("Solve $x^2-9=0$ by factoring.", "x=3,-3",
         "This is a difference of squares: $(x-3)(x+3)=0$, so $x=3$ or $x=-3$.",
         ["x=9,-9", "x=3", "x=-3"]),
        ("Solve $2x^2+7x+3=0$ by factoring.", "x=-3,-1/2",
         "Factor: $(2x+1)(x+3)=0$. Setting each factor to $0$: $x=-\\dfrac{1}{2}$ or $x=-3$.",
         ["x=3,1/2", "x=-3,1/2", "x=3,-1/2"]),
        ("Solve $x^2+4x=0$ by factoring.", "x=0,-4",
         "Factor out the GCF: $x(x+4)=0$, so $x=0$ or $x=-4$.",
         ["x=0,4", "x=4", "x=-4"]),
        ("Solve $x^2-2x-15=0$ by factoring.", "x=5,-3",
         "Factor: $(x-5)(x+3)=0$, so $x=5$ or $x=-3$.",
         ["x=-5,3", "x=5,3", "x=-5,-3"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Concept 4 (16-20): quadratic formula & discriminant
    for text, ans, expl, dist in [
        ("Find the discriminant of $x^2+2x+5=0$.", -16,
         "Discriminant $=b^2-4ac=(2)^2-4(1)(5)=4-20=-16$.", None),
        ("Solve $x^2-4x+1=0$ using the quadratic formula. Express as $h\\pm\\sqrt{d}$.", "2\u00b1\u221a3",
         "$x=\\dfrac{4\\pm\\sqrt{16-4}}{2}=\\dfrac{4\\pm\\sqrt{12}}{2}=\\dfrac{4\\pm2\\sqrt{3}}{2}=2\\pm\\sqrt{3}$.",
         ["2\u00b1\u221a5", "4\u00b1\u221a3", "-2\u00b1\u221a3"]),
        ("Find the discriminant of $2x^2-3x+5=0$.", -31,
         "Discriminant $=(-3)^2-4(2)(5)=9-40=-31$.", None),
        ("If the discriminant of a quadratic equation is negative, how many real solutions does it have?",
         "no real solutions",
         "A negative discriminant means $\\sqrt{b^2-4ac}$ is not a real number, so there are no real solutions "
         "(the parabola never crosses the x-axis).",
         ["exactly one real solution", "two real solutions", "infinitely many solutions"]),
        ("Solve $x^2+6x+9=0$ using the quadratic formula.", "x=-3",
         "Discriminant $=36-36=0$, so there is one repeated real solution: $x=\\dfrac{-6\\pm0}{2}=-3$.",
         ["x=3", "x=-3,3", "x=-9"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Concept 5 (21-25): applications
    for text, ans, expl in [
        ("A ball's height is $h(t)=-16t^2+64t$. At what time $t$ does it reach maximum height?", 2,
         "Maximum height occurs at the vertex: $t=-\\dfrac{b}{2a}=-\\dfrac{64}{2(-16)}=2$."),
        ("For $h(t)=-16t^2+64t$, what is the maximum height reached?", 64,
         "Substitute $t=2$ (the vertex time): $h(2)=-16(4)+64(2)=-64+128=64$."),
        ("A rectangle has length $x$ and width $x+3$. If its area is $40$, find $x$ (the positive solution).", 5,
         "Set up $x(x+3)=40$, so $x^2+3x-40=0$. Factor: $(x+8)(x-5)=0$. Since length must be positive, $x=5$."),
        ("A ball's height is $h(t)=-16t^2+96t$. At what positive time $t$ does it hit the ground?", 6,
         "Set $h(t)=0$: $-16t^2+96t=0$, so $-16t(t-6)=0$. The positive solution is $t=6$."),
        ("Revenue is $R(x)=-5x^2+200x$. What value of $x$ maximizes revenue?", 20,
         "Maximum occurs at the vertex: $x=-\\dfrac{200}{2(-5)}=20$."),
    ]:
        qs.append(mq(text, ans, expl, idx)); idx += 1

    # Concept 6 (26-30): quadratic inequalities
    for text, ans, expl, dist in [
        ("Solve $x^2-5x+6>0$.", "x<2 or x>3",
         "Factor: $(x-2)(x-3)>0$. The roots split the number line into three intervals; testing shows the "
         "product is positive when $x<2$ or $x>3$.",
         ["2<x<3", "x<-2 or x>-3", "-3<x<-2"]),
        ("Solve $x^2-9\\leq0$.", "-3\u2264x\u22643",
         "Factor: $(x-3)(x+3)\\leq0$. Testing intervals shows the product is $\\leq0$ between the roots, "
         "so $-3\\leq x\\leq3$.",
         ["x\u2264-3 or x\u22653", "-9\u2264x\u22649", "x\u22643"]),
        ("Solve $x^2+x-6<0$.", "-3<x<2",
         "Factor: $(x+3)(x-2)<0$. Testing intervals shows the product is negative between the roots, "
         "so $-3<x<2$.",
         ["x<-3 or x>2", "-2<x<3", "2<x<3"]),
        ("Solve $x^2-4x\\geq0$.", "x\u22640 or x\u22654",
         "Factor: $x(x-4)\\geq0$. Testing intervals shows the product is $\\geq0$ outside the roots, "
         "so $x\\leq0$ or $x\\geq4$.",
         ["0\u2264x\u22644", "x\u22650 or x\u22644", "x\u2264-4 or x\u22650"]),
        ("Solve $(x-1)(x+5)>0$.", "x<-5 or x>1",
         "The factors are already given. Testing intervals around the roots $x=1$ and $x=-5$ shows the "
         "product is positive when $x<-5$ or $x>1$.",
         ["-5<x<1", "x<-1 or x>5", "1<x<5"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Finale (31-80): 50 progressive problems
    finale = []

    # A. Solve by factoring, integer roots (10)
    for r1, r2 in [(2, 9), (4, 5), (-2, 6), (-5, -1), (7, -3),
                   (1, -8), (10, -2), (-4, -6), (9, 1), (3, -7)]:
        b = -(r1 + r2)
        c = r1 * r2
        b_str = f"{'+' if b >= 0 else ''}{b}x" if b != 0 else ""
        c_str = f"{'+' if c >= 0 else ''}{c}" if c != 0 else ""
        finale.append(mq(
            f"Solve $x^2{b_str}{c_str}=0$ by factoring.",
            f"x={r1},{r2}",
            f"This factors as $(x-({r1}))(x-({r2}))=0$, so $x={r1}$ or $x={r2}$.",
            0,
            distractors=[f"x={-r1},{-r2}", f"x={r1},{-r2}", f"x={r1*2},{r2}"],
        ))

    # B. Quadratic formula with clean radical roots x = h +/- sqrt(d) (8)
    for h, d in [(1, 2), (3, 5), (2, 7), (-1, 3), (4, 10), (0, 6), (5, 2), (-3, 11)]:
        b = -2 * h
        c = h * h - d
        b_str = f"{'+' if b >= 0 else ''}{b}x" if b != 0 else ""
        c_str = f"{'+' if c >= 0 else ''}{c}" if c != 0 else ""
        ans = f"{h}\u00b1\u221a{d}" if h != 0 else f"\u00b1\u221a{d}"
        finale.append(mq(
            f"Solve $x^2{b_str}{c_str}=0$ using the quadratic formula. Express as $h\\pm\\sqrt{{d}}$.",
            ans,
            f"Discriminant $=({b})^2-4(1)({c})={b*b-4*c}$. $x=\\dfrac{{{-b}\\pm\\sqrt{{{b*b-4*c}}}}}{{2}}={ans}$.",
            0,
            distractors=[f"{h}\u00b1\u221a{d+2}", f"{-h}\u00b1\u221a{d}", f"{h+1}\u00b1\u221a{d}"],
        ))

    # C. Discriminant only (6)
    for a, b, c in [(1, 3, -4), (2, -5, 3), (1, 0, 9), (3, 2, 1), (1, -6, 9), (1, 1, 1)]:
        disc = b * b - 4 * a * c
        finale.append(mq(
            f"Find the discriminant of ${a}x^2{'+' if b >= 0 else ''}{b}x{'+' if c >= 0 else ''}{c}=0$.",
            disc,
            f"Discriminant $=b^2-4ac=({b})^2-4({a})({c})={disc}$.",
            0,
        ))

    # D. Vertex from standard form (6)
    for a, b, c in [(1, -6, 8), (1, 4, 1), (1, -10, 21), (2, -8, 3), (2, 12, 7), (3, -12, 5)]:
        h = -b // (2 * a) if (b % (2 * a) == 0) else -b / (2 * a)
        k = a * h * h + b * h + c
        finale.append(mq(
            f"Find the vertex of $y={a}x^2{'+' if b >= 0 else ''}{b}x{'+' if c >= 0 else ''}{c}$.",
            f"({h},{k})",
            f"$h=-\\dfrac{{b}}{{2a}}=-\\dfrac{{{b}}}{{2({a})}}={h}$. Then $k=f({h})={k}$.",
            0,
            distractors=[f"({-h},{k})", f"({h},{-k})", f"({-h},{-k})"],
        ))

    # E. Y-intercept from intercept form (6)
    for pfac, qfac in [(2, 5), (-3, 4), (1, -6), (-2, -7), (0, 5), (3, 3)]:
        yint = pfac * qfac
        finale.append(mq(
            f"For $y=(x-({pfac}))(x-({qfac}))$, what is the $y$-intercept?",
            yint,
            f"Substitute $x=0$: $y=(0-({pfac}))(0-({qfac}))=({-pfac})({-qfac})={yint}$.",
            0,
        ))

    # F. Applications (5)
    for text, ans, expl in [
        ("A ball's height is $h(t)=-16t^2+96t$. At what time does it reach maximum height?", 3,
         "$t=-\\dfrac{96}{2(-16)}=3$."),
        ("A rectangle has length $x$ and width $x+5$. If the area is $84$, find $x$.", 7,
         "$x(x+5)=84 \\Rightarrow x^2+5x-84=0 \\Rightarrow (x+12)(x-7)=0$; the positive root is $x=7$."),
        ("A ball's height is $h(t)=-16t^2+64t+80$. At what positive time does it hit the ground?", 5,
         "Set $h(t)=0$: divide by $-16$ to get $t^2-4t-5=0$, which factors as $(t-5)(t+1)=0$; the positive "
         "root is $t=5$."),
        ("Revenue is $R(x)=-4x^2+240x$. What value of $x$ maximizes revenue?", 30,
         "$x=-\\dfrac{240}{2(-4)}=30$."),
        ("A rectangle has perimeter $40$, so its area is $A(x)=x(20-x)$. What value of $x$ maximizes area?", 10,
         "$A(x)=-x^2+20x$, so $x=-\\dfrac{20}{2(-1)}=10$ (this also matches the symmetric square case)."),
    ]:
        qs_answer = ans
        finale.append(mq(text, ans, expl, 0))

    # G. Inequalities (5)
    for text, ans, expl, dist in [
        ("Solve $x^2-7x+10<0$.", "2<x<5",
         "Factor: $(x-2)(x-5)<0$, so the solution is between the roots: $2<x<5$.",
         ["x<2 or x>5", "-5<x<-2", "x<-2 or x>-5"]),
        ("Solve $x^2-16\\geq0$.", "x\u2264-4 or x\u22654",
         "Factor: $(x-4)(x+4)\\geq0$, so the solution is outside the roots: $x\\leq-4$ or $x\\geq4$.",
         ["-4\u2264x\u22644", "x\u22654", "x\u2264-4"]),
        ("Solve $x^2+3x-10>0$.", "x<-5 or x>2",
         "Factor: $(x+5)(x-2)>0$, so the solution is outside the roots: $x<-5$ or $x>2$.",
         ["-5<x<2", "x<2 or x>5", "-2<x<5"]),
        ("Solve $x^2-6x+8\\leq0$.", "2\u2264x\u22644",
         "Factor: $(x-2)(x-4)\\leq0$, so the solution is between the roots: $2\\leq x\\leq4$.",
         ["x\u22642 or x\u22654", "-4\u2264x\u2264-2", "x\u22648"]),
        ("Solve $x^2+7x+12<0$.", "-4<x<-3",
         "Factor: $(x+4)(x+3)<0$, so the solution is between the roots: $-4<x<-3$.",
         ["x<-4 or x>-3", "3<x<4", "x<-12"]),
    ]:
        finale.append(mq(text, ans, expl, 0, distractors=dist))

    # H. End behavior from leading coefficient (4)
    for a, desc in [(3, "both ends go to +\u221e"), (-5, "both ends go to -\u221e"),
                    (1, "both ends go to +\u221e"), (-2, "both ends go to -\u221e")]:
        finale.append(mq(
            f"For $y={a}x^2+3x-1$, describe the end behavior of both ends of the graph.",
            desc,
            f"The degree is even, so both ends point the same direction as the sign of the leading coefficient "
            f"${a}$: {desc}.",
            0,
            distractors=["one end up, one end down", "both ends flatten toward y=0", "the graph has no end behavior"],
        ))

    while len(finale) < 50:
        n = len(finale) + 1
        finale.append(mq(
            f"Solve $x^2-{n}x=0$ for $x$.",
            f"x=0,{n}",
            f"Factor: $x(x-{n})=0$, so $x=0$ or $x={n}$.",
            0,
        ))

    qs.extend(finale[:50])
    return _fill(qs, 80, lambda i: mq(f"Find the discriminant of $x^2+{i}x+1=0$.", i * i - 4,
                                       f"$({i})^2-4(1)(1)={i*i-4}$.", i))


def build_unit2():
    title = "Algebra 2 Unit 2: Quadratic Functions & Equations"
    description = (
        "A thorough study of quadratic forms, graphing, factoring, the quadratic formula and discriminant, "
        "real-world applications, and quadratic inequalities — patient explanations, worked examples, and "
        "sixty combined practice problems."
    )

    c1 = concept_block(
        "1. Standard, vertex, and intercept forms of a quadratic",
        [
            "Every quadratic function can be written in three equivalent forms, and each one instantly reveals "
            "a different useful feature of the parabola.",
            "Standard form, $y=ax^2+bx+c$, is easiest for reading the $y$-intercept directly (it is $c$) and "
            "for using the quadratic formula.",
            "Vertex form, $y=a(x-h)^2+k$, immediately reveals the vertex $(h,k)$ without any extra computation "
            "at all.",
            "Intercept form, $y=a(x-p)(x-q)$, immediately reveals the $x$-intercepts $p$ and $q$, which is "
            "exactly the information factoring produces.",
            "Being able to translate fluently between these three forms means you always have the fastest tool "
            "available for whatever the question is actually asking.",
            "This unit builds the graphing, factoring, and formula skills you will lean on constantly for the "
            "rest of Algebra 2, including later work with polynomials and conics.",
        ],
        "Quadratics are the first family of nonlinear functions you master deeply in Algebra 2, and the three "
        "forms are the toolkit you reuse in every later chapter that touches parabolas.",
        "Ask what the question wants: vertex → use vertex form; intercepts → use intercept form; y-intercept or "
        "formula work → use standard form. Convert to whichever form answers the question fastest.",
        solved(1, "Expand $y=(x-3)^2+5$ into standard form.",
               ["Expand the squared binomial: $(x-3)^2=x^2-6x+9$.",
                "Add the constant outside: $x^2-6x+9+5=x^2-6x+14$."],
               "$y=x^2-6x+14$", "", "Easy")
        + solved(2, "Convert $y=x^2-6x+5$ to vertex form.",
                 ["Find $h$: $h=-\\dfrac{b}{2a}=-\\dfrac{-6}{2}=3$.",
                  "Find $k$ by evaluating at $h$: $k=f(3)=9-18+5=-4$.",
                  "Write vertex form: $y=(x-3)^2-4$."],
                 "$y=(x-3)^2-4$", "", "Medium")
        + solved(3, "Expand $y=2(x-1)(x+3)$ into standard form.",
                 ["Multiply the two binomials first: $(x-1)(x+3)=x^2+2x-3$.",
                  "Distribute the leading coefficient $2$: $2(x^2+2x-3)=2x^2+4x-6$."],
                 "$y=2x^2+4x-6$", "Always multiply the binomials completely before distributing a leading "
                                  "coefficient in front.", "Hard"),
        ("Mixing up the sign of $h$ in vertex form",
         "Vertex form is written $a(x-h)^2+k$, so a rule like $(x+4)^2$ actually means $h=-4$, not $h=4$, "
         "because $x+4=x-(-4)$. Always rewrite a plus sign as subtracting a negative number before reading off "
         "the vertex, or you will get the horizontal position backwards every time."),
        ("Use the vertex formula as a shortcut and a check",
         "The vertex $x$-coordinate is always $h=-\\dfrac{b}{2a}$ directly from standard form, without completing "
         "the square. Compute $h$ this way first, then find $k=f(h)$; use this as a fast check whenever you "
         "convert forms by another method, like completing the square."),
        [
            "I can convert between standard, vertex, and intercept form.",
            "I can identify the vertex directly from vertex form.",
            "I can identify the x-intercepts directly from intercept form.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Graphing quadratics: vertex, axis of symmetry, intercepts, and end behavior",
        [
            "A complete quadratic graph is built from just a few key features: the vertex, the axis of "
            "symmetry, the $y$-intercept, the $x$-intercepts (if real), and the end behavior.",
            "The axis of symmetry is the vertical line $x=-\\dfrac{b}{2a}$ that passes through the vertex; the "
            "left and right halves of the parabola mirror each other across this line.",
            "The $y$-intercept is always easy to find: substitute $x=0$ into the equation, which in standard "
            "form is simply the constant term $c$.",
            "The $x$-intercepts, when they exist, come from solving the equation set equal to $0$, whether by "
            "factoring or the quadratic formula covered later in this unit.",
            "End behavior for every quadratic depends only on the sign of the leading coefficient $a$: positive "
            "$a$ means both ends of the graph point upward, negative $a$ means both ends point downward.",
            "Following the same five-step routine every time — vertex, axis, y-intercept, x-intercepts, end "
            "behavior — turns graphing from guesswork into a reliable checklist.",
        ],
        "A clean, correctly labeled graph often earns as much credit on assessments as the algebra that "
        "produced it, and a systematic routine prevents you from forgetting a key feature under time pressure.",
        "Work through the same five steps every single time: find the vertex, draw the axis of symmetry, plot "
        "the y-intercept, find the x-intercepts if they exist, and state the end behavior last.",
        solved(4, "Analyze $y=x^2-8x+12$: find the vertex, axis of symmetry, and y-intercept.",
               ["Axis of symmetry: $x=-\\dfrac{-8}{2}=4$.",
                "Vertex height: $f(4)=16-32+12=-4$, so the vertex is $(4,-4)$.",
                "Y-intercept: substitute $x=0$: $f(0)=12$."],
               "Vertex $(4,-4)$, axis $x=4$, y-intercept $12$", "", "Easy")
        + solved(5, "Analyze $y=-2x^2+8x-3$: find the vertex and describe end behavior.",
                 ["Axis of symmetry: $x=-\\dfrac{8}{2(-2)}=2$.",
                  "Vertex height: $f(2)=-2(4)+8(2)-3=-8+16-3=5$, so the vertex is $(2,5)$.",
                  "Since $a=-2<0$, the parabola opens downward, so both ends of the graph go to $-\\infty$."],
                 "Vertex $(2,5)$; both ends go to $-\\infty$", "", "Medium")
        + solved(6, "Fully analyze $y=x^2-2x-8$: vertex, axis, x-intercepts, and y-intercept.",
                 ["Factor to find x-intercepts: $x^2-2x-8=(x-4)(x+2)$, so x-intercepts are $x=4$ and $x=-2$.",
                  "Axis of symmetry: $x=-\\dfrac{-2}{2}=1$.",
                  "Vertex height: $f(1)=1-2-8=-9$, so the vertex is $(1,-9)$.",
                  "Y-intercept: $f(0)=-8$."],
                 "Vertex $(1,-9)$, axis $x=1$, x-intercepts $4,-2$, y-intercept $-8$", "",
                "SAT"),
        ("Guessing end behavior from the vertex direction alone",
         "End behavior depends only on the sign of the leading coefficient $a$, not on where the vertex happens "
         "to sit. A parabola can have a vertex high above the x-axis and still open downward toward $-\\infty$ on "
         "both ends if $a$ is negative — always check the sign of $a$ directly, never guess from the vertex's "
         "height alone."),
        ("Follow the same five-step checklist every time",
         "Vertex, axis of symmetry, y-intercept, x-intercepts, end behavior — in that order, every single "
         "problem. Writing this checklist at the top of your paper before you start prevents skipped steps "
         "on timed assessments."),
        [
            "I can find the vertex and axis of symmetry from standard form.",
            "I can find the x-intercepts and y-intercept of a quadratic.",
            "I can determine end behavior from the sign of the leading coefficient.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Solving quadratics by factoring",
        [
            "Factoring turns a quadratic equation into a product of two simpler expressions set equal to zero, "
            "which is exactly what the zero product property needs to work.",
            "The zero product property says that if $A\\cdot B=0$, then $A=0$ or $B=0$ (or both); this only "
            "applies when one side of the equation is exactly $0$.",
            "Before factoring anything else, always check for a greatest common factor (GCF) among every term "
            "in the equation.",
            "For trinomials with leading coefficient $1$, look for two numbers that multiply to $c$ and add to "
            "$b$; for leading coefficients other than $1$, more careful trial or grouping is needed.",
            "Special patterns — difference of squares, and perfect square trinomials — can be factored "
            "instantly once you recognize their shape, saving significant time.",
            "Factoring only works cleanly when the roots are rational numbers; irrational or complex roots need "
            "the quadratic formula, covered next in this unit.",
        ],
        "Factoring is usually the fastest solving method when it applies, and recognizing when a quadratic "
        "factors nicely (versus needing the formula) is itself an important skill you build with practice.",
        "First move everything to one side so the equation equals $0$. Then check for a GCF, then look for a "
        "recognizable pattern or trial-and-check the factors of $c$ that add to $b$.",
        solved(7, "Solve $x^2-5x+6=0$ by factoring.",
               ["Look for two numbers that multiply to $6$ and add to $-5$: those numbers are $-2$ and $-3$.",
                "Write the factored form: $(x-2)(x-3)=0$.",
                "Apply the zero product property: $x=2$ or $x=3$."],
               "$x=2,3$", "", "Easy")
        + solved(8, "Solve $2x^2+7x+3=0$ by factoring.",
                 ["With a leading coefficient other than $1$, look for factors of $(2)(3)=6$ that add to $7$: "
                  "those are $6$ and $1$.",
                  "Rewrite the middle term and factor by grouping: $2x^2+6x+x+3=2x(x+3)+1(x+3)=(2x+1)(x+3)$.",
                  "Apply the zero product property: $2x+1=0$ gives $x=-\\dfrac{1}{2}$; $x+3=0$ gives $x=-3$."],
                 "$x=-3,-\\dfrac{1}{2}$", "", "Medium")
        + solved(9, "Solve $3x^2-14x-5=0$ by factoring.",
                 ["Look for factors of $(3)(-5)=-15$ that add to $-14$: those are $-15$ and $1$.",
                  "Rewrite and group: $3x^2-15x+x-5=3x(x-5)+1(x-5)=(3x+1)(x-5)$.",
                  "Apply the zero product property: $3x+1=0$ gives $x=-\\dfrac{1}{3}$; $x-5=0$ gives $x=5$."],
                 "$x=5,-\\dfrac{1}{3}$", "Check by expanding $(3x+1)(x-5)$ to confirm you recover the original "
                                        "trinomial.", "Hard"),
        ("Forgetting to set the equation equal to zero first",
         "The zero product property only works when one side of the equation is exactly $0$. If a quadratic "
         "equation is written as $x^2-5x=6$ or $(x-2)(x-3)=4$, you must move every term to one side and simplify "
         "before factoring — factoring a side that is not equal to zero and then setting each piece to zero "
         "gives completely wrong solutions."),
        ("Always check for a GCF before trying anything fancier",
         "A surprising number of “hard” trinomials become easy the moment you factor out a GCF first. Before "
         "hunting for factor pairs of $b$ and $c$, scan every term for a common factor and pull it out — this "
         "also shrinks the numbers you work with, making later steps far less error-prone."),
        [
            "I can factor a trinomial with leading coefficient 1.",
            "I can factor a trinomial with a leading coefficient other than 1 using grouping.",
            "I can apply the zero product property correctly to find every solution.",
        ],
        11,
    )

    c4 = concept_block(
        "4. The quadratic formula and the discriminant",
        [
            "The quadratic formula, $x=\\dfrac{-b\\pm\\sqrt{b^2-4ac}}{2a}$, solves any quadratic equation "
            "$ax^2+bx+c=0$, even when factoring is difficult or impossible.",
            "The expression under the radical, $b^2-4ac$, is called the discriminant, and its sign alone tells "
            "you what kind of solutions to expect before you even finish the computation.",
            "A positive discriminant means two distinct real solutions; a discriminant of exactly $0$ means one "
            "repeated real solution; a negative discriminant means no real solutions (the roots are complex, "
            "covered fully in the next unit).",
            "Computing the discriminant first, before plugging everything into the full formula, saves time and "
            "prevents wasted effort chasing real solutions that do not exist.",
            "Careless sign errors on $-b$ or on the discriminant itself are the most common mistakes with this "
            "formula — writing every value in parentheses before substituting helps enormously.",
            "The quadratic formula is the most powerful and most general tool in this unit, since it works on "
            "every quadratic equation, without exception.",
        ],
        "The quadratic formula is the tool that always works, no matter how ugly the numbers are, which makes "
        "it the reliable fallback whenever factoring feels difficult or impossible.",
        "Identify $a$, $b$, and $c$ carefully, writing each in parentheses. Compute the discriminant first and "
        "decide what kind of solutions to expect, then finish substituting into the formula.",
        solved(10, "Solve $x^2-4x+1=0$ using the quadratic formula.",
               ["Identify $a=1$, $b=-4$, $c=1$.",
                "Compute the discriminant: $(-4)^2-4(1)(1)=16-4=12$.",
                "Substitute into the formula: $x=\\dfrac{4\\pm\\sqrt{12}}{2}$.",
                "Simplify the radical: $\\sqrt{12}=2\\sqrt{3}$, so $x=\\dfrac{4\\pm2\\sqrt{3}}{2}=2\\pm\\sqrt{3}$."],
               "$x=2\\pm\\sqrt{3}$", "", "Easy")
        + solved(11, "Solve $2x^2-3x-5=0$ using the quadratic formula.",
                 ["Identify $a=2$, $b=-3$, $c=-5$.",
                  "Compute the discriminant: $(-3)^2-4(2)(-5)=9+40=49$, a perfect square.",
                  "Substitute: $x=\\dfrac{3\\pm\\sqrt{49}}{4}=\\dfrac{3\\pm7}{4}$.",
                  "Split into two solutions: $x=\\dfrac{10}{4}=\\dfrac{5}{2}$ or $x=\\dfrac{-4}{4}=-1$."],
                 "$x=\\dfrac{5}{2},-1$", "A perfect square discriminant means the formula produces rational "
                                        "answers you could also have reached by factoring.", "Medium")
        + solved(12, "Analyze $3x^2+2x+5=0$ using the discriminant.",
                 ["Identify $a=3$, $b=2$, $c=5$.",
                  "Compute the discriminant: $(2)^2-4(3)(5)=4-60=-56$.",
                  "Since the discriminant is negative, there are no real solutions."],
                 "No real solutions", "This equation's parabola never crosses the x-axis; its solutions are "
                                      "complex numbers, which the next unit explores in full.", "Hard"),
        ("Forgetting the $\\pm$ sign or dropping the negative on $b$",
         "The formula requires $-b$, not $b$, and it requires both the $+$ and $-$ branches to capture every "
         "solution. When $b$ is already negative, $-b$ becomes positive — write every substitution in "
         "parentheses, like $-(-4)$, to avoid losing a sign in the rush of computation."),
        ("Compute the discriminant before finishing the formula",
         "Find $b^2-4ac$ first, by itself, and decide what kind of answer to expect: two real, one real, or "
         "no real. This upfront check catches sign errors early and tells you whether to expect a clean integer, "
         "a radical, or a complex-number answer before you commit to the rest of the computation."),
        [
            "I can identify a, b, and c and apply the quadratic formula correctly.",
            "I can compute the discriminant and predict the type of solutions before finishing.",
            "I can simplify radical answers from the quadratic formula completely.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Applications: projectiles, area, and optimization",
        [
            "Quadratic functions model many real situations where a rate of change itself changes steadily, "
            "such as the height of a thrown object under constant gravity.",
            "For projectile motion problems, the vertex of $h(t)=-16t^2+v_0t+h_0$ gives the time and value of "
            "the maximum height, using the exact same vertex formula from earlier in this unit.",
            "For area and geometry problems, translate the words into an equation first — often by naming one "
            "side $x$ and the other side in terms of $x$ — before applying any algebra tool.",
            "Optimization problems (maximizing area, revenue, or profit) almost always reduce to finding the "
            "vertex of a quadratic, since the vertex is exactly the highest or lowest point on the graph.",
            "After solving, always check that your answer makes sense in context: negative time, negative "
            "length, or negative width are not valid answers, even if they solve the equation algebraically.",
            "These application problems are exactly where all three earlier skills — forms, graphing, and "
            "solving — come together into genuinely useful mathematics.",
        ],
        "Applications are where quadratics stop being an abstract exercise and start describing real falling "
        "objects, real gardens, and real business decisions — the algebra is identical, only the story changes.",
        "Translate the words into an equation first. Decide whether the question wants a maximum/minimum "
        "(use the vertex) or a specific value (solve the equation). Always check your answer against the "
        "real-world context at the end.",
        solved(13, "A ball's height is $h(t)=-16t^2+64t$. Find the time of maximum height and the height itself.",
               ["Maximum height occurs at the vertex: $t=-\\dfrac{64}{2(-16)}=2$.",
                "Substitute $t=2$: $h(2)=-16(4)+64(2)=-64+128=64$."],
               "Max height $64$ at $t=2$", "", "Easy")
        + solved(14, "A rectangle has length $x$ and width $x+3$. If the area is $40$, find the dimensions.",
                 ["Set up the area equation: $x(x+3)=40$.",
                  "Expand and set to zero: $x^2+3x-40=0$.",
                  "Factor: $(x+8)(x-5)=0$, giving $x=-8$ or $x=5$.",
                  "Reject $x=-8$ since length cannot be negative; the length is $5$ and the width is $5+3=8$."],
                 "Length $5$, width $8$", "", "Medium")
        + solved(15, "A ball's height is $h(t)=-16t^2+80t+96$. Find when it hits the ground.",
                 ["Set $h(t)=0$: $-16t^2+80t+96=0$.",
                  "Divide every term by $-16$ to simplify: $t^2-5t-6=0$.",
                  "Factor: $(t-6)(t+1)=0$, giving $t=6$ or $t=-1$.",
                  "Reject the negative time; the ball hits the ground at $t=6$."],
                 "$t=6$", "Dividing by the leading coefficient before factoring often turns an ugly equation "
                          "into a friendly one.", "Challenge"),
        ("Keeping a negative time or negative length as a valid answer",
         "The algebra of the quadratic formula or factoring does not know anything about physical reality; it "
         "happily hands back negative solutions whenever they satisfy the equation. Always reread the original "
         "context after solving and discard any answer that would mean negative time, negative length, or "
         "negative width — those are algebraic solutions to the equation, not answers to the real question."),
        ("Translate words to equations one phrase at a time",
         "Read the problem sentence by sentence, writing an expression for each described quantity as you go: "
         "“length is $x$,” “width is $3$ more than length” becomes $x+3$, “area is 40” becomes setting the "
         "product equal to $40$. Building the equation piece by piece avoids the common trap of misreading a "
         "relationship."),
        [
            "I can set up a quadratic equation from a word problem.",
            "I can use the vertex to solve maximum/minimum application problems.",
            "I can check whether an algebraic solution makes sense in the real-world context.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Quadratic inequalities on the number line",
        [
            "A quadratic inequality asks not for the exact points where a parabola crosses the x-axis, but for "
            "the entire range of $x$-values where the parabola sits above or below the axis.",
            "The first step is always the same as solving the related equation: factor (or use the quadratic "
            "formula) to find the boundary points, called critical values.",
            "Those critical values split the number line into separate intervals, and within each interval the "
            "expression is entirely positive or entirely negative — it cannot change sign without crossing zero.",
            "Testing one convenient point from each interval in the original inequality tells you whether that "
            "whole interval is part of the solution.",
            "When the inequality includes equality ($\\leq$ or $\\geq$), the boundary points themselves are "
            "included in the solution using closed circles or square brackets; strict inequalities exclude them.",
            "A quick sketch of the parabola, showing where it is above or below the x-axis, is often the fastest "
            "way to confirm your interval answer makes sense.",
        ],
        "Quadratic inequalities connect graphing and solving into a single skill, and the same interval-testing "
        "method you learn here reappears for rational and polynomial inequalities in later units.",
        "Find the critical values first by solving the related equation. Mark them on a number line, test one "
        "point from each resulting interval in the original inequality, and shade the intervals that work.",
        solved(16, "Solve $x^2-5x+6>0$.",
               ["Find the critical values by solving the related equation: $x^2-5x+6=0$ factors as "
                "$(x-2)(x-3)=0$, giving $x=2$ and $x=3$.",
                "These values split the number line into three intervals: $x<2$, $2<x<3$, and $x>3$.",
                "Test a point from each: at $x=0$, $(0-2)(0-3)=6>0$ ✓; at $x=2.5$, $(0.5)(-0.5)=-0.25<0$ ✗; "
                "at $x=4$, $(2)(1)=2>0$ ✓."],
               "$x<2$ or $x>3$", "", "Easy")
        + solved(17, "Solve $x^2-9\\leq0$.",
                 ["Find the critical values: $x^2-9=0$ factors as $(x-3)(x+3)=0$, giving $x=3$ and $x=-3$.",
                  "Test a point between them, like $x=0$: $(0)^2-9=-9\\leq0$ ✓, so the middle interval works.",
                  "Since the inequality includes equality, the boundary points are included too."],
                 "$-3\\leq x\\leq3$", "", "Medium")
        + solved(18, "Solve $-x^2+4x+5\\geq0$.",
                 ["A negative leading coefficient is easier to work with after multiplying both sides by $-1$, "
                  "which flips the inequality: $x^2-4x-5\\leq0$.",
                  "Factor: $(x-5)(x+1)\\leq0$, giving critical values $x=5$ and $x=-1$.",
                  "Test the middle interval, like $x=0$: $(0-5)(0+1)=-5\\leq0$ ✓, so the middle interval works, "
                  "including both endpoints."],
                 "$-1\\leq x\\leq5$", "Multiplying or dividing an inequality by a negative number always flips "
                                     "the inequality symbol.", "Hard"),
        ("Forgetting to flip the inequality sign",
         "Multiplying or dividing both sides of an inequality by a negative number reverses the direction of "
         "the inequality symbol. This is easy to forget when simplifying a quadratic with a negative leading "
         "coefficient — always flip the symbol the moment you multiply or divide by anything negative, and "
         "double-check by testing a point afterward."),
        ("Test points in the original inequality, not the factored equation",
         "After finding critical values, always substitute a test point back into the ORIGINAL inequality "
         "(before you set it equal to zero), not just into the factored expression from the related equation. "
         "This final check catches sign-flip mistakes and confirms which intervals truly satisfy the inequality."),
        [
            "I can find the critical values of a quadratic inequality by solving the related equation.",
            "I can test intervals to determine which ones satisfy the inequality.",
            "I can correctly include or exclude boundary points based on the inequality symbol.",
        ],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        "Grade 10 Algebra 2",
        [
            "Convert between standard, vertex, and intercept forms",
            "Graph quadratics using vertex, axis, intercepts, and end behavior",
            "Solve quadratic equations by factoring",
            "Solve using the quadratic formula and interpret the discriminant",
            "Model and solve projectile, area, and optimization applications",
            "Solve and graph quadratic inequalities on a number line",
        ],
        body,
        practice_slots(31, 50),
    )
    return title, description, content, _u2_questions()


# ===========================================================================
# UNIT 3: Complex Numbers & Completing the Square
# ===========================================================================

def _u3_questions():
    qs = []
    idx = 1

    # Concept 1 (1-5): imaginary unit and powers of i
    for text, ans, expl, dist in [
        ("Simplify $i^2$.", -1, "By definition, $i^2=-1$.", None),
        ("Simplify $i^3$.", "-i", "$i^3=i^2\\cdot i=(-1)(i)=-i$.", ["i", "1", "-1"]),
        ("Simplify $i^4$.", 1, "$i^4=(i^2)^2=(-1)^2=1$.", None),
        ("Simplify $i^7$.", "-i", "$7=4(1)+3$, so $i^7=i^4\\cdot i^3=(1)(-i)=-i$.", ["i", "1", "-1"]),
        ("Simplify $\\sqrt{-16}$.", "4i", "$\\sqrt{-16}=\\sqrt{16}\\cdot\\sqrt{-1}=4i$.", ["-4i", "16i", "4"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Concept 2 (6-10): complex arithmetic
    for text, ans, expl, dist in [
        ("Simplify $(3+2i)+(1-5i)$.", "4-3i", "Add real parts: $3+1=4$. Add imaginary parts: $2-5=-3$.",
         ["4+3i", "-4-3i", "4-7i"]),
        ("Simplify $(5-i)-(2+3i)$.", "3-4i", "Subtract real parts: $5-2=3$. Subtract imaginary parts: $-1-3=-4$.",
         ["3+4i", "7+2i", "3-2i"]),
        ("Simplify $(2+i)(3-i)$.", "7+i",
         "FOIL: $(2)(3)+(2)(-i)+(i)(3)+(i)(-i)=6-2i+3i-i^2=6+i+1=7+i$.",
         ["7-i", "5+i", "6+i"]),
        ("Simplify $(1+i)^2$.", "2i", "$(1+i)^2=1+2i+i^2=1+2i-1=2i$.", ["2", "1+2i", "-2i"]),
        ("Simplify $3i(2-4i)$.", "12+6i", "$3i(2-4i)=6i-12i^2=6i+12=12+6i$.", ["6i+12", "12-6i", "-12+6i"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Concept 3 (11-15): conjugates & division
    for text, ans, expl, dist in [
        ("What is the complex conjugate of $5-3i$?", "5+3i", "The conjugate flips the sign of the imaginary part "
         "only: $5-3i \\to 5+3i$.", ["-5+3i", "-5-3i", "3-5i"]),
        ("Simplify $(2+3i)(2-3i)$.", 13,
         "This is a complex number times its conjugate: $(2)^2-(3i)^2=4-9i^2=4+9=13$.", None),
        ("Simplify $\\dfrac{4+2i}{1-i}$.", "1+3i",
         "Multiply top and bottom by the conjugate $1+i$: numerator $(4+2i)(1+i)=4+4i+2i+2i^2=2+6i$; "
         "denominator $(1-i)(1+i)=1+1=2$. So $\\dfrac{2+6i}{2}=1+3i$.",
         ["1-3i", "2+3i", "6+2i"]),
        ("Find $|3-4i|$.", 5, "The modulus is $\\sqrt{3^2+4^2}=\\sqrt{9+16}=\\sqrt{25}=5$.", None),
        ("Simplify $\\dfrac{2+3i}{i}$.", "3-2i",
         "Multiply top and bottom by $-i$: numerator $(2+3i)(-i)=-2i-3i^2=3-2i$; denominator $i(-i)=-i^2=1$. "
         "So the result is $3-2i$.",
         ["3+2i", "-3+2i", "2-3i"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Concept 4 (16-20): completing the square
    for text, ans, expl, dist in [
        ("Complete the square: $x^2+8x=(x+4)^2-\\text{___}$. Find the missing number.", 16,
         "Take half of $8$ (getting $4$), then square it: $4^2=16$. This confirms $(x+4)^2=x^2+8x+16$, so we "
         "subtract $16$ to keep the expression equal.", None),
        ("Solve $x^2-6x+2=0$ by completing the square.", "3\u00b1\u221a7",
         "Move the constant: $x^2-6x=-2$. Add $9$ (half of $-6$, squared) to both sides: $(x-3)^2=7$. "
         "Take the square root: $x-3=\\pm\\sqrt{7}$, so $x=3\\pm\\sqrt{7}$.",
         ["3\u00b1\u221a2", "-3\u00b1\u221a7", "6\u00b1\u221a7"]),
        ("Write $x^2+10x+21$ in the form $(x+5)^2-k$. Find $k$.", 4,
         "$(x+5)^2=x^2+10x+25$. Since the original expression is $x^2+10x+21$, we need $25-k=21$, so $k=4$.",
         None),
        ("Solve $x^2+4x-5=0$ by completing the square.", "x=1,-5",
         "Move the constant: $x^2+4x=5$. Add $4$ (half of $4$, squared) to both sides: $(x+2)^2=9$. "
         "Take the square root: $x+2=\\pm3$, so $x=1$ or $x=-5$.",
         ["x=-1,5", "x=1,5", "x=-1,-5"]),
        ("Convert $y=x^2-4x+7$ to vertex form by completing the square.", "(x-2)^2+3",
         "Half of $-4$ is $-2$, squared is $4$. Write $x^2-4x+4-4+7=(x-2)^2+3$.",
         ["(x+2)^2+3", "(x-2)^2-3", "(x-4)^2+7"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Concept 5 (21-25): solving quadratics with complex roots
    for text, ans, expl, dist in [
        ("Solve $x^2+4=0$.", "\u00b12i", "$x^2=-4$, so $x=\\pm\\sqrt{-4}=\\pm2i$.", ["\u00b14i", "\u00b12", "\u00b1\u221a4"]),
        ("Solve $x^2-2x+5=0$.", "1\u00b12i",
         "Discriminant $=4-20=-16$. $x=\\dfrac{2\\pm\\sqrt{-16}}{2}=\\dfrac{2\\pm4i}{2}=1\\pm2i$.",
         ["2\u00b12i", "1\u00b14i", "-1\u00b12i"]),
        ("Solve $x^2+2x+10=0$.", "-1\u00b13i",
         "Discriminant $=4-40=-36$. $x=\\dfrac{-2\\pm\\sqrt{-36}}{2}=\\dfrac{-2\\pm6i}{2}=-1\\pm3i$.",
         ["1\u00b13i", "-1\u00b16i", "-2\u00b13i"]),
        ("Solve $x^2-6x+13=0$.", "3\u00b12i",
         "Discriminant $=36-52=-16$. $x=\\dfrac{6\\pm\\sqrt{-16}}{2}=\\dfrac{6\\pm4i}{2}=3\\pm2i$.",
         ["-3\u00b12i", "3\u00b14i", "6\u00b12i"]),
        ("Solve $x^2+9=0$.", "\u00b13i", "$x^2=-9$, so $x=\\pm\\sqrt{-9}=\\pm3i$.", ["\u00b19i", "\u00b13", "\u00b1\u221a9"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Concept 6 (26-30): discriminant & graph relation
    for text, ans, expl, dist in [
        ("Find the discriminant of $x^2-4x+4=0$.", 0, "$(-4)^2-4(1)(4)=16-16=0$.", None),
        ("Find the discriminant of $x^2+x+1=0$.", -3, "$(1)^2-4(1)(1)=1-4=-3$.", None),
        ("Find the discriminant of $x^2-5x+6=0$.", 1, "$(-5)^2-4(1)(6)=25-24=1$.", None),
        ("Does the graph of $y=x^2+2x+5$ cross the x-axis?", "No",
         "Discriminant $=4-20=-16<0$, so there are no real roots, which means the graph never crosses the "
         "x-axis.",
         ["Yes, twice", "Yes, once", "Cannot be determined"]),
        ("Find the discriminant of $3x^2+2x+7=0$.", -80, "$(2)^2-4(3)(7)=4-84=-80$.", None),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Finale (31-80): 50 progressive problems
    finale = []

    def isimp(n):
        r = n % 4
        return {0: "1", 1: "i", 2: "-1", 3: "-i"}[r]

    # A. Powers of i (6)
    for n in [5, 6, 7, 8, 11, 15]:
        val = isimp(n)
        finale.append(mq(
            f"Simplify $i^{{{n}}}$.",
            val,
            f"${n}$ divided by $4$ leaves remainder ${n % 4}$, so $i^{{{n}}}=i^{{{n % 4}}}={val}$.",
            0,
            distractors=near_str(val, ["1", "i", "-1", "-i"]),
        ))

    # B. Complex addition/subtraction (6)
    for a1, b1, a2, b2, op in [(6, 2, 1, -5, "+"), (5, -1, 2, 3, "-"), (-2, 4, 6, -1, "+"),
                               (7, 0, 2, 5, "-"), (0, 3, 4, 4, "+"), (-3, -2, -1, 4, "-")]:
        if op == "+":
            rr, ri = a1 + a2, b1 + b2
            symbol = "+"
        else:
            rr, ri = a1 - a2, b1 - b2
            symbol = "-"
        ans = f"{rr}{'+' if ri >= 0 else ''}{ri}i"
        finale.append(mq(
            f"Simplify $({a1}{'+' if b1 >= 0 else ''}{b1}i){symbol}({a2}{'+' if b2 >= 0 else ''}{b2}i)$.",
            ans,
            f"Combine real and imaginary parts separately to get ${ans}$.",
            0,
            distractors=[f"{-rr}{'+' if ri >= 0 else ''}{ri}i", f"{rr}{'+' if -ri >= 0 else ''}{-ri}i",
                         f"{rr+1}{'+' if ri >= 0 else ''}{ri}i"],
        ))

    # C. Complex multiplication (6)
    mult_pairs = [
        ((2, 1), (3, -2), "8-i", ["8+i", "2-i", "1-i"]),
        ((1, 1), (1, 1), "2i", ["2", "1+2i", "-2i"]),
        ((3, -2), (1, 1), "5+i", ["5-i", "1+i", "7-i"]),
        ((4, 1), (-2, 1), "-9+2i", ["-9-2i", "9+2i", "-7+2i"]),
        ((3, 4), (3, -4), "25", ["9-16i", "-25", "9+16i"]),
        ((-1, 1), (2, -1), "-1+3i", ["-1-3i", "1+3i", "-3+i"]),
    ]
    for (a1, b1), (a2, b2), ans, dist in mult_pairs:
        finale.append(mq(
            f"Simplify $({a1}{'+' if b1 >= 0 else ''}{b1}i)({a2}{'+' if b2 >= 0 else ''}{b2}i)$.",
            ans,
            f"FOIL and use $i^2=-1$ to simplify to ${ans}$.",
            0,
            distractors=dist,
        ))

    # D. Modulus (Pythagorean triples) (6)
    for a, b in [(3, 4), (5, 12), (8, 6), (7, 24), (9, 12), (20, 21)]:
        mod = int(round(math.sqrt(a * a + b * b)))
        finale.append(mq(
            f"Find $|{a}+{b}i|$.",
            mod,
            f"$|{a}+{b}i|=\\sqrt{{{a}^2+{b}^2}}=\\sqrt{{{a*a+b*b}}}={mod}$.",
            0,
        ))

    # E. Complex division (6)
    div_items = [
        ("3+i", "2-i", "1+i"),
        ("7-4i", "3+2i", "1-2i"),
        ("-3+4i", "i", "4+3i"),
        ("6-8i", "2i", "-4-3i"),
        ("1+7i", "3+i", "1+2i"),
        ("7+i", "1-i", "3+4i"),
    ]
    for num, den, ans in div_items:
        finale.append(mq(
            f"Simplify $\\dfrac{{{num}}}{{{den}}}$.",
            ans,
            f"Multiply numerator and denominator by the conjugate of the denominator, then simplify, "
            f"to get ${ans}$.",
            0,
            distractors=near_str(ans, ["1+i", "1-2i", "4+3i", "-4-3i", "1+2i", "3+4i", "2-i", "-1+i"]),
        ))

    # F. Completing the square, real irrational roots (6)
    csq_items = [(4, 10), (2, 13), (5, 3), (1, 6), (-3, 5), (-2, 11)]
    for h, k in csq_items:
        b = 2 * h
        c = h * h - k
        b_str = f"{'+' if b >= 0 else ''}{b}x" if b != 0 else ""
        c_str = f"{'+' if c >= 0 else ''}{c}" if c != 0 else ""
        ans = f"{-h}\u00b1\u221a{k}"
        finale.append(mq(
            f"Solve $x^2{b_str}{c_str}=0$ by completing the square.",
            ans,
            f"$(x+({h}))^2={k}$, so $x=-{h}\\pm\\sqrt{{{k}}}={ans}$.",
            0,
            distractors=[f"{h}\u00b1\u221a{k}", f"{-h}\u00b1\u221a{k+2}", f"{-h+1}\u00b1\u221a{k}"],
        ))

    # G. Complex roots via completing the square (6)
    cplx_items = [(1, 5), (2, 3), (-1, 2), (0, 5), (3, 1), (-2, 4)]
    for h, d in cplx_items:
        b = -2 * h
        c = h * h + d * d
        b_str = f"{'+' if b >= 0 else ''}{b}x" if b != 0 else ""
        c_str = f"{'+' if c >= 0 else ''}{c}"
        ans = f"{h}\u00b1{d}i" if h != 0 else f"\u00b1{d}i"
        finale.append(mq(
            f"Solve $x^2{b_str}{c_str}=0$.",
            ans,
            f"Discriminant $=({b})^2-4({c})={b*b-4*c}$, which is negative. "
            f"$x=\\dfrac{{{-b}\\pm\\sqrt{{{b*b-4*c}}}}}{{2}}={ans}$.",
            0,
            distractors=[f"{h}\u00b1{d+1}i", f"{-h}\u00b1{d}i", f"{h}\u00b1{d*2}i"],
        ))

    # H. Discriminant classification (8)
    for a, b, c in [(1, -7, 10), (1, -6, 9), (1, 2, 5), (2, 3, -2),
                    (1, 4, 4), (3, 2, 4), (1, -3, -10), (2, -4, 10)]:
        disc = b * b - 4 * a * c
        if disc > 0:
            cls = "two distinct real roots"
        elif disc == 0:
            cls = "one repeated real root"
        else:
            cls = "two complex conjugate roots"
        finale.append(mq(
            f"Classify the roots of ${a}x^2{'+' if b >= 0 else ''}{b}x{'+' if c >= 0 else ''}{c}=0$ using the "
            f"discriminant.",
            cls,
            f"Discriminant $=({b})^2-4({a})({c})={disc}$, which gives {cls}.",
            0,
            distractors=near_str(cls, ["two distinct real roots", "one repeated real root",
                                        "two complex conjugate roots"]),
        ))

    while len(finale) < 50:
        n = len(finale) + 1
        finale.append(mq(f"Simplify $i^{{{4*n}}}$.", 1, f"Any multiple of $4$ as an exponent of $i$ gives $1$.", 0))

    qs.extend(finale[:50])
    return _fill(qs, 80, lambda i: mq(f"Simplify $i^{{{4*i+1}}}$.", "i", "The exponent leaves remainder 1, so the result is $i$.", i))


def build_unit3():
    title = "Algebra 2 Unit 3: Complex Numbers & Completing the Square"
    description = (
        "A careful introduction to the imaginary unit, complex arithmetic and conjugates, completing the "
        "square, and solving quadratics with complex roots, tied together through the discriminant — with "
        "quick checks after every idea and a 50-problem finale."
    )

    c1 = concept_block(
        "1. The imaginary unit $i$ and powers of $i$",
        [
            "For centuries, mathematicians treated $\\sqrt{-1}$ as meaningless, since no real number squared "
            "gives a negative result. Algebra 2 introduces a new number, $i$, defined exactly so that $i^2=-1$.",
            "Every power of $i$ cycles through only four possible values, in order: $i^1=i$, $i^2=-1$, "
            "$i^3=-i$, $i^4=1$, and then the pattern repeats forever.",
            "Because the pattern repeats every four powers, you can simplify any power of $i$ by dividing the "
            "exponent by $4$ and using only the remainder.",
            "Negative numbers under a square root, like $\\sqrt{-16}$, are simplified by pulling out the "
            "negative sign as $i$: $\\sqrt{-16}=\\sqrt{16}\\cdot\\sqrt{-1}=4i$.",
            "The imaginary unit is not a strange trick invented to make problems harder; it completes the "
            "number system so that every quadratic equation, without exception, has a solution.",
            "This concept is the foundation for everything else in this unit: arithmetic with $i$, dividing "
            "complex numbers, and solving quadratics whose discriminant is negative.",
        ],
        "Complex numbers complete the number system: every quadratic equation now has a solution, real or "
        "complex, and this completeness matters again later when you study polynomial roots in Unit 4.",
        "Treat $i$ like a variable in every computation, then substitute $i^2=-1$ at the very end to simplify. "
        "For high powers, divide the exponent by $4$ and use only the remainder.",
        solved(1, "Simplify $i^2$.",
               ["By the definition of the imaginary unit, $i^2=-1$."],
               "$-1$", "", "Easy")
        + solved(2, "Simplify $i^{10}$.",
                 ["Divide the exponent by $4$: $10=4(2)+2$, so the remainder is $2$.",
                  "$i^{10}=i^2=-1$."],
                 "$-1$", "", "Medium")
        + solved(3, "Simplify $i^{23}$.",
                 ["Divide the exponent by $4$: $23=4(5)+3$, so the remainder is $3$.",
                  "$i^{23}=i^3=-i$."],
                 "$-i$", "This shortcut works for any exponent, no matter how large.", "Hard"),
        ("Treating $i$ like a normal variable you can cancel or ignore",
         "It is tempting to treat $i$ as just another letter and cancel it out of equations the way you cancel "
         "an ordinary variable, but $i$ has the very specific property $i^2=-1$ that ordinary variables do not "
         "have. Whenever $i^2$ appears in a computation, you must replace it with $-1$ before simplifying "
         "further — skipping this step is the single most common error with complex numbers."),
        ("Reduce the exponent modulo 4 first",
         "For any power of $i$, divide the exponent by $4$ and keep only the remainder (0, 1, 2, or 3). That "
         "remainder tells you the simplified value instantly: remainder $0$ gives $1$, remainder $1$ gives $i$, "
         "remainder $2$ gives $-1$, and remainder $3$ gives $-i$. This turns even huge exponents into a "
         "two-second calculation."),
        [
            "I can state the definition $i^2=-1$ and use it to simplify expressions.",
            "I can simplify any power of $i$ by reducing the exponent modulo 4.",
            "I can simplify the square root of a negative number using $i$.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Complex number arithmetic: addition, subtraction, and multiplication",
        [
            "A complex number has the form $a+bi$, where $a$ is called the real part and $b$ is called the "
            "imaginary part; both $a$ and $b$ are ordinary real numbers.",
            "Adding or subtracting complex numbers works exactly like combining like terms: combine the real "
            "parts together, and separately combine the imaginary parts together.",
            "Multiplying two complex numbers uses the same distributive property (FOIL) you already know from "
            "multiplying binomials, with one extra step: replace $i^2$ with $-1$ at the end.",
            "A very common special case is squaring a complex number, like $(1+i)^2$, which expands using the "
            "same pattern as squaring any binomial, followed by the $i^2=-1$ substitution.",
            "Complex number arithmetic feels almost identical to polynomial arithmetic with one new rule bolted "
            "on, which is exactly why practicing it now pays off quickly.",
            "Every result of adding, subtracting, or multiplying two complex numbers is itself another complex "
            "number, written in the same $a+bi$ form.",
        ],
        "Complex arithmetic is the toolkit you need before you can divide complex numbers, solve quadratics "
        "with complex roots, or eventually study complex numbers in Precalculus and beyond.",
        "Treat $i$ as a variable throughout the distributing or combining step, and only substitute $i^2=-1$ "
        "as your very last simplification move.",
        solved(4, "Simplify $(4+3i)+(2-6i)$.",
               ["Combine the real parts: $4+2=6$.",
                "Combine the imaginary parts: $3+(-6)=-3$."],
               "$6-3i$", "", "Easy")
        + solved(5, "Simplify $(5-2i)(3+i)$.",
                 ["FOIL: $(5)(3)+(5)(i)+(-2i)(3)+(-2i)(i)=15+5i-6i-2i^2$.",
                  "Combine the middle terms: $5i-6i=-i$.",
                  "Replace $i^2$ with $-1$: $-2i^2=-2(-1)=2$.",
                  "Combine everything: $15-i+2=17-i$."],
                 "$17-i$", "", "Medium")
        + solved(6, "Simplify $(2-i)^2$.",
                 ["Expand like any binomial square: $(2-i)^2=4-4i+i^2$.",
                  "Replace $i^2$ with $-1$: $4-4i+(-1)$.",
                  "Combine real terms: $4-1=3$."],
                 "$3-4i$", "Squaring a complex number always uses the same binomial pattern you already know.", "Hard"),
        ("Forgetting that $i^2=-1$ when multiplying",
         "When multiplying two complex numbers, every $i\\times i$ term produces $i^2$, and it is easy to leave "
         "that term as $-1\\cdot(\\text{stuff})$ without actually substituting the $-1$ in, or to forget the "
         "term entirely. Always write out $i^2$ explicitly during FOIL, then replace it with $-1$ as a separate, "
         "visible step before combining real and imaginary parts."),
        ("Treat $i$ as a variable, then substitute at the end",
         "Multiply and distribute complex numbers exactly as you would with any two binomials in $x$, keeping "
         "$i$ symbolic the whole time. Only after every term is expanded do you go back and replace every "
         "instance of $i^2$ with $-1$, then combine the real and imaginary parts separately."),
        [
            "I can add and subtract complex numbers by combining real and imaginary parts.",
            "I can multiply complex numbers using FOIL and simplify using $i^2=-1$.",
            "I can square a complex number correctly.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Complex conjugates and dividing complex numbers",
        [
            "The complex conjugate of $a+bi$ is $a-bi$: the real part stays the same, and the sign of the "
            "imaginary part flips.",
            "Multiplying a complex number by its own conjugate always produces a real number, because the "
            "imaginary terms cancel: $(a+bi)(a-bi)=a^2+b^2$.",
            "This cancellation is exactly the trick used to divide complex numbers: multiply both the numerator "
            "and denominator by the conjugate of the denominator, which turns the denominator into a real number.",
            "The modulus, or absolute value, of a complex number $a+bi$ is $|a+bi|=\\sqrt{a^2+b^2}$, which "
            "measures its distance from the origin if you picture the complex plane.",
            "Dividing complex numbers takes more steps than adding, subtracting, or multiplying, but it always "
            "follows the exact same multiply-by-the-conjugate routine, without exception.",
            "Conjugates reappear constantly later in this unit, since the two complex solutions of a quadratic "
            "equation with a negative discriminant are always conjugates of each other.",
        ],
        "Conjugates and division are the tools that let you fully simplify any complex expression, and the "
        "conjugate-pair pattern you learn here directly explains why complex quadratic roots always come in "
        "pairs.",
        "For division, multiply the top and bottom by the conjugate of the denominator. This always turns the "
        "denominator into a real number, after which the division becomes simple arithmetic.",
        solved(7, "Find the conjugate of $7+2i$ and compute the product $(7+2i)(7-2i)$.",
               ["The conjugate flips the sign of the imaginary part: $7+2i \\to 7-2i$.",
                "Multiply: $(7+2i)(7-2i)=7^2-(2i)^2=49-4i^2=49+4=53$."],
               "Conjugate $7-2i$; product $53$", "", "Easy")
        + solved(8, "Simplify $\\dfrac{3+i}{2-i}$.",
                 ["Multiply top and bottom by the conjugate of the denominator, $2+i$.",
                  "Numerator: $(3+i)(2+i)=6+3i+2i+i^2=6+5i-1=5+5i$.",
                  "Denominator: $(2-i)(2+i)=4+1=5$.",
                  "Divide every term by $5$: $\\dfrac{5+5i}{5}=1+i$."],
                 "$1+i$", "", "Medium")
        + solved(9, "Simplify $\\dfrac{7-4i}{3+2i}$.",
                 ["Multiply top and bottom by the conjugate $3-2i$.",
                  "Numerator: $(7-4i)(3-2i)=21-14i-12i+8i^2=21-26i-8=13-26i$.",
                  "Denominator: $(3+2i)(3-2i)=9+4=13$.",
                  "Divide every term by $13$: $\\dfrac{13-26i}{13}=1-2i$."],
                 "$1-2i$", "The denominator is chosen so that it divides the numerator evenly — always check "
                          "whether your final fraction simplifies completely.", "Hard"),
        ("Dividing without multiplying by the conjugate",
         "It is not mathematically valid to “divide by $i$” or divide by a complex number directly the way you "
         "divide real numbers. You must first multiply both the numerator and the denominator by the conjugate "
         "of the denominator; skipping this step leaves an imaginary number in the denominator, which is not "
         "considered simplified."),
        ("Multiply top and bottom by the conjugate — always",
         "No matter what the denominator looks like, identify its conjugate, multiply both numerator and "
         "denominator by that conjugate, simplify the denominator (it will always become real), and then divide "
         "each term of the numerator by that real number."),
        [
            "I can find the complex conjugate of any complex number.",
            "I can explain why a complex number times its conjugate is always real.",
            "I can divide two complex numbers by multiplying by the conjugate.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Completing the square carefully",
        [
            "Completing the square rewrites a quadratic expression as a perfect square binomial plus (or "
            "minus) a constant, which is useful both for solving equations and for converting to vertex form.",
            "The core move is: take half of the coefficient of $x$, square that result, and add it to the "
            "expression — this exact number is what turns $x^2+bx$ into a perfect square trinomial.",
            "Whatever you add to one side of an equation, you must add to the other side as well, to keep the "
            "equation balanced and mathematically true.",
            "Once the left side is a perfect square binomial, you can take the square root of both sides to "
            "solve, remembering to include both the positive and negative square root.",
            "Completing the square works on every quadratic, including ones that do not factor nicely, and it "
            "sets up the entire derivation of the quadratic formula itself.",
            "This same technique is exactly what you will use in the very next concept to solve quadratics "
            "whose solutions are complex numbers.",
        ],
        "Completing the square is not just an alternate solving method; it is literally how the quadratic "
        "formula was derived, and it is the technique you lean on for circles and other conic sections later "
        "in math.",
        "Move the constant to the other side first. Take half of the $x$-coefficient, square it, and add that "
        "number to both sides. Then factor the perfect square and take the square root of both sides.",
        solved(10, "Complete the square for $x^2+8x$.",
               ["Take half of $8$: $4$.",
                "Square that result: $4^2=16$.",
                "Add and subtract $16$ to keep the expression equivalent: $x^2+8x+16-16=(x+4)^2-16$."],
               "$(x+4)^2-16$", "", "Easy")
        + solved(11, "Solve $x^2-6x+2=0$ by completing the square.",
                 ["Move the constant to the other side: $x^2-6x=-2$.",
                  "Take half of $-6$ (getting $-3$) and square it: $9$. Add $9$ to both sides: $x^2-6x+9=-2+9$.",
                  "Factor the left side as a perfect square: $(x-3)^2=7$.",
                  "Take the square root of both sides: $x-3=\\pm\\sqrt{7}$, so $x=3\\pm\\sqrt{7}$."],
                 "$x=3\\pm\\sqrt{7}$", "", "Medium")
        + solved(12, "Convert $y=x^2-4x+7$ to vertex form by completing the square.",
                 ["Focus on the $x^2-4x$ part. Take half of $-4$ (getting $-2$) and square it: $4$.",
                  "Add and subtract $4$ inside the expression: $x^2-4x+4-4+7$.",
                  "Factor the perfect square: $(x-2)^2-4+7$.",
                  "Combine constants: $(x-2)^2+3$."],
                 "$y=(x-2)^2+3$", "The vertex is $(2,3)$, and since it sits above the x-axis with the parabola "
                                  "opening upward, this quadratic has no real roots — matching a negative "
                                  "discriminant.", "Hard"),
        ("Forgetting to add the same constant to both sides",
         "When you add a number to complete the square on one side of an equation, you must add that exact "
         "same number to the other side too, or the equation is no longer true. A very common shortcut mistake "
         "is adding the number only inside the expression being rewritten and forgetting the balancing add on "
         "the other side of the equals sign."),
        ("Take half of $b$, then square it — every single time",
         "The number you need to complete the square is always $\\left(\\dfrac{b}{2}\\right)^2$, where $b$ is "
         "the coefficient of $x$ after the leading coefficient has been factored out to $1$. Write this "
         "computation as its own line every time, rather than trying to do it in your head, to avoid arithmetic "
         "slips."),
        [
            "I can complete the square for an expression of the form $x^2+bx$.",
            "I can solve a quadratic equation by completing the square.",
            "I can convert a quadratic from standard form to vertex form by completing the square.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Solving quadratics with complex roots",
        [
            "When a quadratic equation has a negative discriminant, its two solutions are complex numbers "
            "instead of real numbers, but the exact same quadratic formula (or completing the square) still "
            "produces them correctly.",
            "The key extra step is recognizing $\\sqrt{-k}$ (for positive $k$) as $i\\sqrt{k}$, using the "
            "imaginary unit from earlier in this unit.",
            "Complex solutions to a quadratic with real coefficients always come in conjugate pairs, written as "
            "$p+qi$ and $p-qi$, because the $\\pm$ in the quadratic formula only ever changes the sign of the "
            "imaginary part.",
            "There is no need to stop or say a problem has “no solution” just because the discriminant is "
            "negative; instead, continue the same steps and express the answer using $i$.",
            "Solving with complex roots is really just an extension of everything from the earlier concepts in "
            "this unit: powers of $i$, complex arithmetic, and completing the square, all combined into one "
            "process.",
            "This skill also finishes the story started in Unit 2: with complex numbers available, every "
            "quadratic equation now has exactly two solutions, real or complex.",
        ],
        "With complex numbers, every quadratic equation always has exactly two solutions — this completeness "
        "is one of the most satisfying ideas in all of algebra, and it removes the need to ever say “no "
        "solution” for a quadratic again.",
        "Compute the discriminant first. If it is negative, keep going anyway: rewrite the negative square "
        "root using $i$, and simplify the two conjugate solutions completely.",
        solved(13, "Solve $x^2+4=0$.",
               ["Isolate the squared term: $x^2=-4$.",
                "Take the square root of both sides, remembering both signs: $x=\\pm\\sqrt{-4}$.",
                "Rewrite using $i$: $\\sqrt{-4}=\\sqrt{4}\\cdot i=2i$, so $x=\\pm2i$."],
               "$x=\\pm2i$", "", "Easy")
        + solved(14, "Solve $x^2-2x+5=0$.",
                 ["Identify $a=1$, $b=-2$, $c=5$. Compute the discriminant: $(-2)^2-4(1)(5)=4-20=-16$.",
                  "Substitute into the quadratic formula: $x=\\dfrac{2\\pm\\sqrt{-16}}{2}$.",
                  "Rewrite the radical using $i$: $\\sqrt{-16}=4i$, so $x=\\dfrac{2\\pm4i}{2}$.",
                  "Simplify each term by dividing by $2$: $x=1\\pm2i$."],
                 "$x=1\\pm2i$", "", "Medium")
        + solved(15, "Solve $3x^2-6x+6=0$.",
                 ["Notice every term shares a factor of $3$; divide the whole equation by $3$ first: $x^2-2x+2=0$.",
                  "Compute the discriminant: $(-2)^2-4(1)(2)=4-8=-4$.",
                  "Substitute: $x=\\dfrac{2\\pm\\sqrt{-4}}{2}=\\dfrac{2\\pm2i}{2}$.",
                  "Simplify: $x=1\\pm i$."],
                 "$x=1\\pm i$", "Simplifying the leading coefficient first, before applying the formula, keeps "
                               "the numbers much smaller.", "Challenge"),
        ("Stopping at a negative discriminant instead of continuing with $i$",
         "A negative discriminant does not mean the equation has no answer at all — it only means the answer "
         "is not a real number. Continue the exact same quadratic formula steps, rewrite the negative square "
         "root using $i$, and finish simplifying to find the two complex solutions."),
        ("Write the discriminant first, then finish the formula",
         "Compute $b^2-4ac$ on its own line before substituting into the rest of the quadratic formula. If it "
         "is negative, rewrite it as $i\\sqrt{|\\text{discriminant}|}$ immediately, so the rest of the "
         "simplification proceeds exactly like the real-root case, just with an $i$ attached."),
        [
            "I can solve a quadratic equation whose discriminant is negative.",
            "I can rewrite $\\sqrt{-k}$ using the imaginary unit $i$.",
            "I can explain why complex roots always come in conjugate pairs for real-coefficient equations.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Relating the discriminant to real/complex roots and the graph",
        [
            "The discriminant, $b^2-4ac$, connects three different views of the same quadratic equation: the "
            "algebra of solving it, the type of number the solutions are, and the picture of its graph.",
            "A positive discriminant means two distinct real solutions, which corresponds to a parabola that "
            "crosses the x-axis at two separate points.",
            "A discriminant of exactly $0$ means one repeated real solution, which corresponds to a parabola "
            "whose vertex sits exactly on the x-axis, touching it at a single point.",
            "A negative discriminant means two complex conjugate solutions, which corresponds to a parabola "
            "that never touches the x-axis at all — it stays entirely above or entirely below it.",
            "This connection means you can predict a graph's relationship to the x-axis without graphing "
            "anything, just by computing one number from the equation.",
            "Understanding this three-way link between discriminant, root type, and graph behavior ties "
            "together everything from Units 2 and 3 into one coherent picture of quadratics.",
        ],
        "This single number, the discriminant, unifies algebra (solving) and geometry (graphing) into one "
        "coherent idea, which is exactly the kind of connection that makes later math — like analyzing "
        "polynomial graphs in Unit 4 — much easier to understand.",
        "Compute the discriminant. Positive means two real crossings, zero means one tangent touch, negative "
        "means no crossing at all (complex roots). Picture the parabola matching that description before "
        "moving on.",
        solved(16, "For $x^2-4x+4=0$, find the discriminant and describe the graph's relationship to the x-axis.",
               ["Compute the discriminant: $(-4)^2-4(1)(4)=16-16=0$.",
                "A discriminant of $0$ means one repeated real root, so the parabola's vertex touches the "
                "x-axis at exactly one point, without crossing through it."],
               "Discriminant $0$; touches the x-axis once", "", "Easy")
        + solved(17, "For $x^2+x+1=0$, find the discriminant and describe the graph's relationship to the x-axis.",
                 ["Compute the discriminant: $(1)^2-4(1)(1)=1-4=-3$.",
                  "A negative discriminant means two complex conjugate roots, so the parabola never touches or "
                  "crosses the x-axis at all."],
                 "Discriminant $-3$; never touches the x-axis", "", "Medium")
        + solved(18, "For $2x^2-5x-3=0$, find the discriminant, solve the equation, and describe the graph.",
                 ["Compute the discriminant: $(-5)^2-4(2)(-3)=25+24=49$, a perfect square.",
                  "Since the discriminant is positive, expect two distinct real roots.",
                  "Solve: $x=\\dfrac{5\\pm7}{4}$, giving $x=3$ or $x=-\\dfrac{1}{2}$.",
                  "Because the discriminant is positive, the parabola crosses the x-axis at exactly these two "
                  "points."],
                 "Discriminant $49$; roots $x=3,-\\dfrac{1}{2}$; crosses the x-axis twice", "",
                 "Hard"),
        ("Assuming a negative discriminant means “no solutions” instead of “no real solutions”",
         "A negative discriminant only rules out real-number solutions; the equation still has exactly two "
         "complex solutions, which are just as valid mathematically. Always say “no real solutions” rather than "
         "“no solutions” to keep this distinction clear, especially once complex numbers are part of your toolkit."),
        ("Match the discriminant's sign to a mental picture of the parabola",
         "Build the habit of picturing the graph the instant you compute the discriminant: positive means "
         "picture two crossing points, zero means picture the vertex resting exactly on the x-axis, negative "
         "means picture the whole parabola floating above or below the x-axis without touching it."),
        [
            "I can compute a discriminant and classify the root type instantly.",
            "I can connect discriminant sign to how many times a parabola touches the x-axis.",
            "I can solve a quadratic and explain its graph's relationship to the x-axis in one connected answer.",
        ],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        "Grade 10 Algebra 2",
        [
            "Simplify powers of the imaginary unit i",
            "Add, subtract, and multiply complex numbers",
            "Use conjugates to divide complex numbers and find the modulus",
            "Complete the square carefully for any quadratic",
            "Solve quadratic equations with complex roots",
            "Connect the discriminant to real/complex roots and the graph",
        ],
        body,
        practice_slots(31, 50),
    )
    return title, description, content, _u3_questions()


# ===========================================================================
# UNIT 4: Polynomial Functions & Factoring
# ===========================================================================

def _u4_questions():
    qs = []
    idx = 1

    # Concept 1 (1-5): polynomial vocabulary
    for text, ans, expl, dist in [
        ("What is the degree of $3x^4-2x^2+7$?", 4, "The degree is the highest exponent on $x$, which is $4$.", None),
        ("What is the leading coefficient of $-5x^3+2x-1$?", -5,
         "The leading coefficient is the number in front of the highest-degree term, which is $-5$.", None),
        ("Describe the end behavior of $f(x)=-2x^3+5x$ as $x\\to\\infty$.", "f(x)\u2192-\u221e",
         "The degree is odd and the leading coefficient is negative, so as $x\\to\\infty$, the graph falls: "
         "$f(x)\\to-\\infty$.",
         ["f(x)\u2192\u221e", "f(x)\u21920", "f(x)\u2192-5"]),
        ("Describe the end behavior of $f(x)=x^4-3x^2$ as $x\\to-\\infty$.", "f(x)\u2192\u221e",
         "The degree is even and the leading coefficient is positive, so both ends rise: as $x\\to-\\infty$, "
         "$f(x)\\to\\infty$.",
         ["f(x)\u2192-\u221e", "f(x)\u21920", "f(x)\u21921"]),
        ("What is the maximum possible number of turning points for a degree-5 polynomial?", 4,
         "A polynomial of degree $n$ has at most $n-1$ turning points, so degree $5$ gives at most $4$.", None),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Concept 2 (6-10): factoring strategies
    for text, ans, expl, dist in [
        ("Factor $6x^3-9x^2$ completely.", "3x^2(2x-3)",
         "The GCF of $6x^3$ and $9x^2$ is $3x^2$. Factor it out: $3x^2(2x-3)$.",
         ["3x(2x^2-3x)", "3x^2(2x+3)", "x^2(6x-9)"]),
        ("Factor $x^3+3x^2+2x+6$ completely.", "(x^2+2)(x+3)",
         "Group in pairs: $x^2(x+3)+2(x+3)$. Factor out the common binomial: $(x^2+2)(x+3)$.",
         ["(x^2-2)(x+3)", "(x^2+2)(x-3)", "(x+2)(x^2+3)"]),
        ("Factor $4x^2-25$ completely.", "(2x-5)(2x+5)",
         "This is a difference of squares: $(2x)^2-(5)^2=(2x-5)(2x+5)$.",
         ["(4x-25)(x+1)", "(2x-5)^2", "(4x-5)(x+5)"]),
        ("Factor $x^3+8$ completely.", "(x+2)(x^2-2x+4)",
         "This is a sum of cubes with $a=x$, $b=2$: $(a+b)(a^2-ab+b^2)=(x+2)(x^2-2x+4)$.",
         ["(x+2)(x^2+2x+4)", "(x-2)(x^2+2x+4)", "(x+2)^3"]),
        ("Factor $27x^3-1$ completely.", "(3x-1)(9x^2+3x+1)",
         "This is a difference of cubes with $a=3x$, $b=1$: $(a-b)(a^2+ab+b^2)=(3x-1)(9x^2+3x+1)$.",
         ["(3x-1)(9x^2-3x+1)", "(3x+1)(9x^2-3x+1)", "(3x-1)^3"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Concept 3 (11-15): division
    for text, ans, expl, dist in [
        ("Divide $x^3-4x^2+5x-2$ by $(x-1)$. Find the quotient.", "x^2-3x+2",
         "Synthetic division with root $1$ on coefficients $1,-4,5,-2$ gives quotient coefficients $1,-3,2$ "
         "and remainder $0$.",
         ["x^2+3x+2", "x^2-3x-2", "x^2-4x+2"]),
        ("Divide $2x^3+3x^2-4x+5$ by $(x+2)$. Find the remainder.", 9,
         "Synthetic division with root $-2$ on coefficients $2,3,-4,5$ gives quotient $2,-1,-2$ and "
         "remainder $9$.", None),
        ("Divide $x^4-1$ by $(x-1)$. Find the quotient.", "x^3+x^2+x+1",
         "Synthetic division with root $1$ on coefficients $1,0,0,0,-1$ gives quotient coefficients "
         "$1,1,1,1$ and remainder $0$.",
         ["x^3-x^2+x-1", "x^3+x^2+x-1", "x^3+x+1"]),
        ("Divide $x^3+2x^2-5x+1$ by $(x-2)$. Find the remainder.", 7,
         "Synthetic division with root $2$ on coefficients $1,2,-5,1$ gives quotient $1,4,3$ and remainder $7$.",
         None),
        ("Divide $x^3-27$ by $(x-3)$. Find the quotient.", "x^2+3x+9",
         "Synthetic division with root $3$ on coefficients $1,0,0,-27$ gives quotient coefficients $1,3,9$ "
         "and remainder $0$.",
         ["x^2-3x+9", "x^2+3x-9", "x^2+9x+3"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Concept 4 (16-20): remainder & factor theorems
    for text, ans, expl, dist in [
        ("Is $(x-3)$ a factor of $x^3-2x^2-5x+6$?", "Yes",
         "By the factor theorem, check $f(3)=27-18-15+6=0$. Since the remainder is $0$, $(x-3)$ is a factor.",
         ["No", "Cannot be determined", "Only if x=3 is excluded"]),
        ("Is $(x+1)$ a factor of $x^3+3x^2+3x+1$?", "Yes",
         "By the factor theorem, check $f(-1)=-1+3-3+1=0$. Since the remainder is $0$, $(x+1)$ is a factor.",
         ["No", "Cannot be determined", "Only for x>0"]),
        ("Find $k$ so that $(x-2)$ is a factor of $x^3-3x^2+kx-4$.", 4,
         "By the factor theorem, $f(2)=0$: $8-12+2k-4=0$, so $2k-8=0$, giving $k=4$.", None),
        ("Find the remainder when $x^4+2x^3-x+5$ is divided by $(x+1)$.", 5,
         "By the remainder theorem, the remainder equals $f(-1)=1-2+1+5=5$.", None),
        ("If $f(x)=2x^3-5x^2+ax+6$ and $f(1)=0$, find $a$.", -3,
         "$f(1)=2-5+a+6=a+3=0$, so $a=-3$.", None),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Concept 5 (21-25): zeros & rational root theorem
    for text, ans, expl, dist in [
        ("Find all zeros of $x^3-6x^2+11x-6=0$.", "1,2,3",
         "Testing rational root candidates from $\\pm1,\\pm2,\\pm3,\\pm6$, all of $1$, $2$, and $3$ work: the "
         "polynomial factors as $(x-1)(x-2)(x-3)$.",
         ["-1,-2,-3", "1,2,6", "2,3,6"]),
        ("Given that $x^3-2x^2-5x+6=0$ has a root at $x=1$, find the other two roots.", "3,-2",
         "Dividing by $(x-1)$ gives $x^2-x-6=(x-3)(x+2)$, so the other roots are $x=3$ and $x=-2$.",
         ["-3,2", "3,2", "-3,-2"]),
        ("What is the maximum number of real zeros a degree-4 polynomial can have?", 4,
         "A degree-$n$ polynomial has at most $n$ real zeros, so degree $4$ allows at most $4$.", None),
        ("Find all real solutions of $x^3-x=0$.", "0,1,-1",
         "Factor: $x(x^2-1)=x(x-1)(x+1)=0$, giving $x=0$, $x=1$, and $x=-1$.",
         ["0,1", "1,-1", "0,-1"]),
        ("Find the real zeros of $x^4-16=0$.", "2,-2",
         "Factor: $(x^2-4)(x^2+4)=0$. The factor $x^2-4=0$ gives real zeros $x=2,-2$; the factor $x^2+4=0$ "
         "gives only complex zeros $\\pm2i$.",
         ["2,-2,2i,-2i", "4,-4", "16,-16"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Concept 6 (26-30): multiplicity
    for text, ans, expl, dist in [
        ("In $x^2(x-3)=0$, what is the multiplicity of the root $x=0$?", 2,
         "The factor $x$ appears as $x^2$, so its exponent, $2$, is the multiplicity of the root $x=0$.", None),
        ("For $y=(x-2)^3(x+1)$, does the graph cross or touch the x-axis at $x=2$?", "crosses",
         "The multiplicity of $x=2$ is $3$, which is odd, so the graph crosses the x-axis there (though it "
         "flattens slightly due to the higher odd power).",
         ["touches (turns around)", "neither crosses nor touches", "the graph is undefined there"]),
        ("For $y=(x+4)^2(x-1)$, does the graph cross or touch the x-axis at $x=-4$?", "touches (turns around)",
         "The multiplicity of $x=-4$ is $2$, which is even, so the graph touches the x-axis and turns back, "
         "without crossing through it.",
         ["crosses", "neither crosses nor touches", "the graph is undefined there"]),
        ("Solve $x^3-4x^2+4x=0$, listing each distinct root once.", "0,2",
         "Factor: $x(x^2-4x+4)=x(x-2)^2=0$, giving distinct roots $x=0$ and $x=2$ (with $x=2$ having "
         "multiplicity $2$).",
         ["0,2,4", "0,-2", "2,4"]),
        ("Solve $x^4-5x^2+4=0$ for all real $x$.", "1,-1,2,-2",
         "Let $u=x^2$: $u^2-5u+4=(u-1)(u-4)=0$, so $u=1$ or $u=4$. Then $x^2=1$ gives $x=\\pm1$, and "
         "$x^2=4$ gives $x=\\pm2$.",
         ["1,2", "-1,-2", "1,4"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    # Finale (31-80): 50 progressive problems
    finale = []

    # A. Degree, leading coefficient, end behavior facts (8)
    poly_facts = [
        ("4x^5-3x^2+1", "the degree", 5),
        ("-3x^4+2x-7", "the leading coefficient", -3),
        ("5x^3-x", "the degree", 3),
        ("-x^6+4x^2", "the leading coefficient", -1),
        ("2x^7-5x^3", "the degree", 7),
        ("-4x^3+2x^2-1", "the leading coefficient", -4),
        ("6x^2-3x+9", "the degree", 2),
        ("-2x^5+3x", "the leading coefficient", -2),
    ]
    for expr, ask, val in poly_facts:
        finale.append(mq(
            f"For $f(x)={expr}$, what is {ask}?",
            val,
            f"Reading the term with the highest exponent gives {ask} as ${val}$.",
            0,
        ))

    # B. Factoring (8)
    factor_items = [
        ("8x^4-12x^3", "4x^3(2x-3)", "GCF is $4x^3$."),
        ("x^3+5x^2+2x+10", "(x^2+2)(x+5)", "Group as $x^2(x+5)+2(x+5)$."),
        ("9x^2-49", "(3x-7)(3x+7)", "Difference of squares with $3x$ and $7$."),
        ("25x^2-1", "(5x-1)(5x+1)", "Difference of squares with $5x$ and $1$."),
        ("x^3+27", "(x+3)(x^2-3x+9)", "Sum of cubes with $a=x$, $b=3$."),
        ("8x^3-1", "(2x-1)(4x^2+2x+1)", "Difference of cubes with $a=2x$, $b=1$."),
        ("2x^3+3x^2+4x+6", "(x^2+2)(2x+3)", "Group as $x^2(2x+3)+2(2x+3)$."),
        ("15x^5+10x^3", "5x^3(3x^2+2)", "GCF is $5x^3$."),
    ]
    for expr, ans, expl in factor_items:
        finale.append(mq(
            f"Factor ${expr}$ completely.",
            ans,
            expl,
            0,
            distractors=near_str(ans, [it[1] for it in factor_items]),
        ))

    # C. Synthetic division remainders (8)
    div_cases = [
        ([1, -4, 5, -2], 1), ([2, 3, -4, 5], -2), ([1, 0, 0, 0, -1], 1), ([1, 2, -5, 1], 2),
        ([1, 2, 0, -1, 5], -1), ([1, -6, 11, -6], 1), ([2, -5, 0, 6], 1), ([1, -3, 0, -4], 2),
    ]
    for coeffs, root in div_cases:
        quotient, remainder = _synthetic_divide(coeffs, root)
        degree = len(coeffs) - 1
        terms = []
        for power, c in zip(range(degree, -1, -1), coeffs):
            if power == 0:
                terms.append(f"{'+' if c >= 0 else ''}{c}")
            elif power == 1:
                terms.append(f"{c}x" if terms == [] else f"{'+' if c >= 0 else ''}{c}x")
            else:
                terms.append(f"{c}x^{power}" if terms == [] else f"{'+' if c >= 0 else ''}{c}x^{power}")
        poly_str = "".join(terms)
        finale.append(mq(
            f"Find the remainder when ${poly_str}$ is divided by $(x{'-' if root >= 0 else '+'}{abs(root)})$.",
            remainder,
            f"By the remainder theorem, the remainder equals the polynomial evaluated at $x={root}$, which is "
            f"${remainder}$.",
            0,
        ))

    # D. Factor theorem yes/no (8)
    factor_theorem_cases = [
        ([1, -2, -5, 6], 1, True), ([1, 3, 3, 1], -1, True), ([1, 0, -1, -6], 2, True),
        ([1, 2, -1, -2], 1, True), ([1, 0, -4, 1], 1, False), ([1, 1, -4, -4], -2, True),
        ([1, -3, 0, 4], -1, True), ([1, 0, 2, -5], 1, False),
    ]
    for coeffs, root, is_factor in factor_theorem_cases:
        _, remainder = _synthetic_divide(coeffs, root)
        degree = len(coeffs) - 1
        terms = []
        for power, c in zip(range(degree, -1, -1), coeffs):
            if c == 0:
                continue
            if power == 0:
                terms.append(f"{'+' if c >= 0 else ''}{c}")
            elif power == 1:
                terms.append(f"{c}x" if terms == [] else f"{'+' if c >= 0 else ''}{c}x")
            else:
                terms.append(f"{c}x^{power}" if terms == [] else f"{'+' if c >= 0 else ''}{c}x^{power}")
        poly_str = "".join(terms)
        ans = "Yes" if is_factor else "No"
        finale.append(mq(
            f"Is $(x{'-' if root >= 0 else '+'}{abs(root)})$ a factor of ${poly_str}$?",
            ans,
            f"By the factor theorem, evaluate at $x={root}$: the remainder is ${remainder}$, so the answer "
            f"is {'yes, it is a factor' if is_factor else 'no, it is not a factor'}.",
            0,
            distractors=["No", "Cannot be determined", "Only for negative x"] if is_factor
            else ["Yes", "Cannot be determined", "Only for positive x"],
        ))

    # E. Zeros / rational root theorem (10)
    zero_items = [
        ("x^3-6x^2+11x-6=0", "1,2,3"),
        ("x^3-2x^2-5x+6=0 (given root x=1)", "3,-2 (the other two roots)"),
        ("x^3-4x=0", "0,2,-2"),
        ("x^4-16=0", "2,-2 (real zeros)"),
        ("x^3+x^2-4x-4=0", "-2,-1,2"),
        ("x^3-3x^2+4=0", "-1,2,2"),
        ("x^3-6x^2+12x-8=0", "2,2,2"),
        ("x^4-5x^2+4=0", "1,-1,2,-2"),
        ("x^3+2x^2-x-2=0", "1,-1,-2"),
        ("x^3-7x-6=0", "-1,3,-2"),
    ]
    for eq, ans in zero_items:
        finale.append(mq(
            f"Find all real solutions of ${eq}$.",
            ans,
            "Test small rational root candidates, divide out each confirmed root with synthetic division, "
            "and factor the remaining quotient completely to find every solution.",
            0,
            distractors=near_str(ans, [it[1] for it in zero_items]),
        ))

    # F. Multiplicity (8)
    mult_items = [
        ("x^2(x-3)=0", "what is the multiplicity of x=0?", 2),
        ("(x-2)^3(x+1)=0", "does the graph cross or touch at x=2?", "crosses"),
        ("(x+4)^2(x-1)=0", "does the graph cross or touch at x=-4?", "touches (turns around)"),
        ("x^3+2x^2+x=0", "what is the multiplicity of x=-1?", 2),
        ("(x-5)(x+2)^4=0", "what is the multiplicity of x=-2?", 4),
        ("y=(x+3)^3", "does the graph cross or touch at x=-3?", "crosses"),
        ("x^4-8x^2+16=0", "what is the multiplicity of x=2?", 2),
        ("x^2(x+5)^2=0", "what is the multiplicity of x=0?", 2),
    ]
    for eq, ask, val in mult_items:
        if isinstance(val, int):
            finale.append(mq(f"For ${eq}$, {ask}", val, "Read the exponent on the matching factor directly as "
                                                          "the multiplicity of that root.", 0))
        else:
            finale.append(mq(f"For ${eq}$, {ask}", val,
                              "Odd multiplicity means the graph crosses the x-axis; even multiplicity means it "
                              "touches and turns around without crossing.", 0,
                              distractors=near_str(val, ["crosses", "touches (turns around)"])))

    while len(finale) < 50:
        n = len(finale) + 1
        finale.append(mq(f"What is the degree of $x^{n % 6 + 2}-1$?", n % 6 + 2,
                          f"The highest exponent is ${n % 6 + 2}$.", 0))

    qs.extend(finale[:50])
    return _fill(qs, 80, lambda i: mq(f"What is the leading coefficient of ${i}x^3-1$?", i,
                                       f"The coefficient in front of the highest-degree term is ${i}$.", i))


def build_unit4():
    title = "Algebra 2 Unit 4: Polynomial Functions & Factoring"
    description = (
        "A deep study of polynomial vocabulary, advanced factoring strategies, long and synthetic division, "
        "the remainder and factor theorems, the rational root theorem, and multiplicity — with quick checks "
        "after every idea and a 50-problem finale."
    )

    c1 = concept_block(
        "1. Polynomial vocabulary: degree, leading coefficient, and end behavior",
        [
            "A polynomial is a sum of terms, each a coefficient times a nonnegative integer power of $x$; there "
            "are no square roots of $x$, no $x$ in a denominator, and no negative exponents on $x$.",
            "The degree of a polynomial is the highest exponent appearing on $x$; it is the single most "
            "important number for predicting the overall shape of the graph.",
            "The leading coefficient is the number multiplying the highest-degree term; together with the "
            "degree, it completely determines the polynomial's end behavior.",
            "End behavior describes what the graph does far to the left and far to the right: odd-degree "
            "polynomials have opposite behavior on each end, while even-degree polynomials have matching "
            "behavior on both ends.",
            "A degree-$n$ polynomial can have at most $n-1$ turning points (places where the graph changes from "
            "rising to falling or vice versa) and at most $n$ real zeros.",
            "Learning to read degree, leading coefficient, and end behavior at a glance is the foundation for "
            "every other skill in this unit, from factoring to sketching complete graphs.",
        ],
        "Degree and leading coefficient are like a polynomial's fingerprint: from just these two facts, you can "
        "immediately sketch the rough shape of the whole graph before doing any other work.",
        "Find the term with the highest exponent first. Its exponent is the degree; its coefficient is the "
        "leading coefficient. Use both together to state the end behavior on each side.",
        solved(1, "Identify the degree and leading coefficient of $f(x)=5x^4-3x^2+2$.",
               ["Find the term with the highest exponent: $5x^4$.",
                "The exponent, $4$, is the degree.",
                "The coefficient of that term, $5$, is the leading coefficient."],
               "Degree $4$, leading coefficient $5$", "", "Easy")
        + solved(2, "Describe the end behavior of $f(x)=-3x^5+2x^2$.",
                 ["The degree is $5$, which is odd. The leading coefficient is $-3$, which is negative.",
                  "For an odd-degree polynomial with a negative leading coefficient, the ends point in opposite "
                  "directions, with the left end rising and the right end falling.",
                  "As $x\\to\\infty$, $f(x)\\to-\\infty$. As $x\\to-\\infty$, $f(x)\\to\\infty$."],
                 "Rises left, falls right", "", "Medium")
        + solved(3, "For $f(x)=2x^6-5x^4+x$, find the degree, leading coefficient, end behavior, and the "
                    "maximum number of turning points.",
                 ["Degree is $6$ (even); leading coefficient is $2$ (positive).",
                  "Even degree with positive leading coefficient means both ends rise: as $x\\to\\pm\\infty$, "
                  "$f(x)\\to\\infty$.",
                  "Maximum turning points is $\\text{degree}-1=6-1=5$."],
                 "Degree 6, leading coeff 2, both ends rise, at most 5 turning points", "",
                "SAT"),
        ("Confusing the constant term with the leading coefficient",
         "The leading coefficient always belongs to the term with the highest exponent, not the term listed "
         "first if the polynomial happens to be written out of order, and definitely not the constant term at "
         "the end. Always scan for the highest exponent first, then read its coefficient, no matter what order "
         "the polynomial is written in."),
        ("Always look at the highest-exponent term first",
         "Before analyzing anything else about a polynomial, find and circle the term with the largest "
         "exponent. That single term controls the degree, the leading coefficient, and therefore the entire "
         "end behavior — everything else in the polynomial only affects the graph's shape in the middle."),
        [
            "I can identify the degree and leading coefficient of any polynomial.",
            "I can determine end behavior from the degree and leading coefficient.",
            "I can state the maximum number of turning points for a given degree.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Factoring strategies: GCF, grouping, and special products",
        [
            "Factoring a polynomial completely almost always starts the same way: pull out the greatest common "
            "factor (GCF) shared by every single term, before trying any other method.",
            "Factoring by grouping works on four-term polynomials by splitting them into two pairs, factoring "
            "each pair separately, and then factoring out the common binomial that remains.",
            "The difference of squares pattern, $a^2-b^2=(a-b)(a+b)$, factors instantly once you recognize both "
            "terms as perfect squares connected by subtraction.",
            "The sum of cubes pattern, $a^3+b^3=(a+b)(a^2-ab+b^2)$, and the difference of cubes pattern, "
            "$a^3-b^3=(a-b)(a^2+ab+b^2)$, look intimidating at first but are simple to apply once memorized.",
            "A useful memory trick for the cubes patterns: the binomial factor always matches the sign of the "
            "original expression, and the sign inside the trinomial factor is always the opposite.",
            "Recognizing which pattern applies, quickly and correctly, is the single most valuable skill for "
            "moving efficiently through this entire unit.",
        ],
        "Factoring is the master key that unlocks solving polynomial equations, finding zeros, and simplifying "
        "rational expressions in every unit that follows this one.",
        "Always check for a GCF first. Then count the terms: two terms suggests a difference of squares or "
        "cubes pattern; four terms suggests grouping; three terms suggests a trinomial factoring method.",
        solved(4, "Factor $6x^3-9x^2$ completely.",
               ["Find the GCF of $6x^3$ and $9x^2$: it is $3x^2$.",
                "Factor it out: $3x^2(2x-3)$."],
               "$3x^2(2x-3)$", "", "Easy")
        + solved(5, "Factor $x^3+3x^2+2x+6$ completely by grouping.",
                 ["Split into two pairs: $(x^3+3x^2)+(2x+6)$.",
                  "Factor each pair: $x^2(x+3)+2(x+3)$.",
                  "Factor out the common binomial $(x+3)$: $(x^2+2)(x+3)$."],
                 "$(x^2+2)(x+3)$", "", "Medium")
        + solved(6, "Factor $8x^3-125$ completely.",
                 ["Recognize this as a difference of cubes: $8x^3=(2x)^3$ and $125=5^3$.",
                  "Apply the pattern $a^3-b^3=(a-b)(a^2+ab+b^2)$ with $a=2x$, $b=5$.",
                  "Substitute: $(2x-5)((2x)^2+(2x)(5)+5^2)=(2x-5)(4x^2+10x+25)$."],
                 "$(2x-5)(4x^2+10x+25)$", "Double-check the middle sign of the trinomial matches the pattern "
                                          "exactly — it is always the opposite sign from the binomial.", "Hard"),
        ("Forgetting to check for a GCF before trying anything fancier",
         "Skipping the GCF step means the numbers you work with in later steps are needlessly large and messy, "
         "and sometimes a hidden GCF is the only thing standing between you and a pattern you would otherwise "
         "miss entirely. Make checking for a GCF the very first, automatic move on every factoring problem."),
        ("Always pull the GCF first, every single time",
         "Before counting terms or hunting for a special pattern, scan every term for a shared factor "
         "(numbers, variables, or both) and pull it out completely. Only after the GCF is gone should you "
         "decide whether the remaining expression is a difference of squares, a sum/difference of cubes, or a "
         "candidate for grouping."),
        [
            "I can factor out the greatest common factor from any polynomial.",
            "I can factor a four-term polynomial by grouping.",
            "I can recognize and apply the difference of squares and sum/difference of cubes patterns.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Polynomial long division and synthetic division",
        [
            "Dividing polynomials works very much like long division with numbers: divide, multiply, subtract, "
            "and bring down the next term, repeated until nothing more can be divided.",
            "Synthetic division is a faster shortcut for dividing by a linear factor of the form $(x-r)$, using "
            "only the coefficients and the value $r$, without writing the variable $x$ at all.",
            "Before dividing (by either method), every missing degree term must be written with a coefficient "
            "of $0$, as a placeholder, or the division will produce incorrect results.",
            "The very last number produced by synthetic division is always the remainder; every number before "
            "it becomes a coefficient of the quotient, one degree lower than the original polynomial.",
            "Synthetic division only works directly when dividing by a linear expression $(x-r)$; dividing by "
            "anything more complicated requires full long division instead.",
            "Both division methods connect directly to the remainder theorem and factor theorem covered next in "
            "this unit, so mastering the mechanics here pays off immediately.",
        ],
        "Polynomial division is the mechanical engine behind finding zeros, verifying factors, and simplifying "
        "rational expressions — nearly every later polynomial skill depends on being able to divide cleanly and "
        "correctly.",
        "Write every missing-degree placeholder with coefficient $0$ first. Then divide (synthetically for "
        "linear divisors), tracking coefficients carefully, and read the quotient and remainder from the "
        "bottom row.",
        solved(7, "Use synthetic division to divide $x^3-4x^2+5x-2$ by $(x-1)$.",
               ["Write the coefficients: $1,-4,5,-2$, using root $r=1$.",
                "Bring down the first coefficient: $1$.",
                "Multiply by $1$ and add: $-4+1(1)=-3$; then $5+(-3)(1)=2$; then $-2+2(1)=0$.",
                "Read the results: quotient coefficients $1,-3,2$ and remainder $0$."],
               "Quotient $x^2-3x+2$, remainder $0$", "", "Easy")
        + solved(8, "Use synthetic division to divide $2x^3+3x^2-4x+5$ by $(x+2)$.",
                 ["Write the coefficients: $2,3,-4,5$, using root $r=-2$ (since $x+2=x-(-2)$).",
                  "Bring down $2$. Multiply by $-2$ and add: $3+2(-2)=-1$; then $-4+(-1)(-2)=-2$; then "
                  "$5+(-2)(-2)=9$.",
                  "Read the results: quotient coefficients $2,-1,-2$ and remainder $9$."],
                 "Quotient $2x^2-x-2$, remainder $9$", "", "Medium")
        + solved(9, "Use synthetic division to divide $x^4-1$ by $(x-1)$, being careful with placeholder zeros.",
                 ["Write every missing degree with a $0$ coefficient: $1,0,0,0,-1$, using root $r=1$.",
                  "Bring down $1$. Multiply and add repeatedly: $0+1(1)=1$; $0+1(1)=1$; $0+1(1)=1$; "
                  "$-1+1(1)=0$.",
                  "Read the results: quotient coefficients $1,1,1,1$ and remainder $0$."],
                 "Quotient $x^3+x^2+x+1$, remainder $0$", "A remainder of $0$ confirms $(x-1)$ is a factor of "
                                                          "$x^4-1$.", "Hard"),
        ("Leaving out a placeholder zero for a missing-degree term",
         "If a polynomial like $x^4-1$ skips the $x^3$, $x^2$, and $x^1$ terms entirely, you must still write "
         "coefficient $0$ for each of those missing degrees before dividing. Skipping a placeholder shifts every "
         "later coefficient into the wrong column and produces a completely wrong quotient."),
        ("Write missing-degree placeholders before you divide",
         "Before setting up either long division or synthetic division, write out the full list of "
         "coefficients from the highest degree down to the constant, inserting a $0$ for every degree that does "
         "not appear in the original polynomial. This one habit prevents the majority of division mistakes."),
        [
            "I can perform synthetic division by a linear factor $(x-r)$.",
            "I can read the quotient and remainder correctly from the result.",
            "I can insert placeholder zeros for missing-degree terms before dividing.",
        ],
        11,
    )

    c4 = concept_block(
        "4. The remainder theorem and factor theorem",
        [
            "The remainder theorem states that dividing a polynomial $f(x)$ by $(x-r)$ always leaves a "
            "remainder equal to $f(r)$ — the value you get from directly substituting $r$ into the polynomial.",
            "This means you never actually have to perform division just to find a remainder; you can instead "
            "evaluate the polynomial at $r$ directly, which is often much faster.",
            "The factor theorem is a direct consequence: $(x-r)$ is a factor of $f(x)$ exactly when $f(r)=0$, "
            "meaning the remainder theorem gives $0$.",
            "These two theorems together let you confirm or rule out a suspected factor in seconds, without "
            "writing out a full synthetic division unless you also need the quotient.",
            "The factor theorem is also the tool behind “finding an unknown coefficient”: if you are told a "
            "specific factor exists, set $f(r)=0$ and solve for the unknown.",
            "Both theorems are simply the remainder theorem in disguise; mastering one number, $f(r)$, unlocks "
            "both ideas at once.",
        ],
        "These two theorems turn “is this a factor?” from a division problem into a simple substitution "
        "problem, which is exactly the kind of shortcut that speeds up every later factoring and zero-finding "
        "task.",
        "Ask yourself which question is being asked: “what is the remainder” (use the remainder theorem: "
        "compute $f(r)$) or “is this a factor” (use the factor theorem: check whether $f(r)=0$).",
        solved(10, "Use the remainder theorem to find the remainder when $x^3+2x^2-5x+1$ is divided by $(x-2)$.",
               ["By the remainder theorem, the remainder equals $f(2)$.",
                "Substitute: $f(2)=8+8-10+1=7$."],
               "$7$", "", "Easy")
        + solved(11, "Use the factor theorem to determine whether $(x+1)$ is a factor of $x^3+3x^2+3x+1$.",
                 ["By the factor theorem, check $f(-1)$.",
                  "Substitute: $f(-1)=-1+3-3+1=0$.",
                  "Since the remainder is $0$, $(x+1)$ is a factor."],
                 "Yes, $(x+1)$ is a factor", "", "Medium")
        + solved(12, "Find $k$ so that $(x-2)$ is a factor of $x^3-3x^2+kx-4$.",
                 ["By the factor theorem, $(x-2)$ is a factor exactly when $f(2)=0$.",
                  "Substitute $x=2$: $f(2)=8-12+2k-4=2k-8$.",
                  "Set the remainder equal to $0$: $2k-8=0$.",
                  "Solve: $k=4$."],
                 "$k=4$", "Always substitute the known root into the polynomial and set the whole expression "
                          "equal to $0$ when solving for an unknown coefficient.", "Hard"),
        ("Confusing the remainder theorem with the factor theorem",
         "The remainder theorem answers “what number is left over,” while the factor theorem answers a "
         "yes-or-no question: “is the remainder exactly zero.” Every factor theorem question is really a "
         "remainder theorem computation followed by one extra check — always compute $f(r)$ first, then decide "
         "what the question is actually asking you to report."),
        ("Ask two separate questions, in order",
         "First: what is $f(r)$? Compute that number carefully by direct substitution. Second: is that number "
         "exactly zero? If the problem only asks for the remainder, stop after the first question; if it asks "
         "about a factor, answer using the second question."),
        [
            "I can use the remainder theorem to find $f(r)$ without dividing.",
            "I can use the factor theorem to determine whether a given binomial is a factor.",
            "I can find an unknown coefficient using the factor theorem.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Finding zeros with the rational root theorem and sketching",
        [
            "The rational root theorem gives a finite list of every possible rational zero of a polynomial with "
            "integer coefficients, dramatically narrowing down what to test.",
            "The theorem says any rational zero must be of the form $\\dfrac{p}{q}$, where $p$ is a factor of "
            "the constant term and $q$ is a factor of the leading coefficient.",
            "Once you have the candidate list, test the smallest and simplest numbers first, using the "
            "remainder theorem (or synthetic division) to check each one quickly.",
            "The moment you confirm one real zero, divide it out using synthetic division; the resulting "
            "quotient is a lower-degree polynomial that is much easier to factor or solve completely.",
            "For polynomials that reduce to a quadratic-like pattern (such as $x^4-5x^2+4$), substituting "
            "$u=x^2$ turns the problem back into ordinary quadratic factoring.",
            "Finding every zero, one at a time by dividing down to lower and lower degree, is the core "
            "technique for fully solving and sketching higher-degree polynomials.",
        ],
        "This “test, confirm, divide down” process is how you crack open any polynomial equation that does not "
        "factor by inspection, and it is a skill that scales up to any degree polynomial you might encounter.",
        "List rational root candidates using $\\dfrac{p}{q}$. Test the smallest ones first. The instant one "
        "works, divide it out and repeat the process on the smaller quotient.",
        solved(13, "List the possible rational roots of $x^3-6x^2+11x-6$, then find all actual roots.",
               ["The constant term is $-6$, with factors $\\pm1,\\pm2,\\pm3,\\pm6$. The leading coefficient is "
                "$1$, with factor $\\pm1$, so the candidate list is $\\pm1,\\pm2,\\pm3,\\pm6$.",
                "Test $x=1$: $1-6+11-6=0$. It works.",
                "Divide by $(x-1)$: quotient is $x^2-5x+6=(x-2)(x-3)$.",
                "The full set of roots is $x=1,2,3$."],
               "$x=1,2,3$", "", "Easy")
        + solved(14, "Given that $x^3-2x^2-5x+6=0$ has a root at $x=1$, find the remaining roots.",
                 ["Divide by $(x-1)$ using synthetic division on coefficients $1,-2,-5,6$ with root $1$.",
                  "The quotient coefficients are $1,-1,-6$, meaning $x^2-x-6$.",
                  "Factor the quotient: $x^2-x-6=(x-3)(x+2)$.",
                  "The remaining roots are $x=3$ and $x=-2$."],
                 "$x=3,-2$", "", "Medium")
        + solved(15, "Find all real solutions of $x^4-5x^2+4=0$.",
                 ["This equation only has even powers of $x$, so substitute $u=x^2$: the equation becomes "
                  "$u^2-5u+4=0$.",
                  "Factor: $(u-1)(u-4)=0$, giving $u=1$ or $u=4$.",
                  "Undo the substitution: $x^2=1$ gives $x=\\pm1$; $x^2=4$ gives $x=\\pm2$."],
                 "$x=1,-1,2,-2$", "The $u$-substitution turns a degree-4 equation back into familiar quadratic "
                                  "factoring.", "Hard"),
        ("Assuming every candidate on the rational root list is an actual root",
         "The rational root theorem only narrows down the possibilities; it does not guarantee that every "
         "listed candidate actually works. You must still test each candidate using substitution or synthetic "
         "division, and stop as soon as you have found enough roots to fully factor the polynomial."),
        ("Test small candidates first",
         "Values like $\\pm1$ and $\\pm2$ are the fastest to test by hand and are correct surprisingly often in "
         "textbook and course problems. Testing the smallest candidates first typically finds a working root "
         "more quickly, letting you divide down to a lower-degree, easier polynomial sooner."),
        [
            "I can list all possible rational roots using the rational root theorem.",
            "I can test candidates and divide out confirmed roots to find every zero.",
            "I can use a substitution like $u=x^2$ to solve quadratic-like higher-degree equations.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Solving polynomial equations and understanding multiplicity",
        [
            "Solving a polynomial equation means finding every value of $x$ that makes it equal to $0$, which "
            "is exactly the same as finding every zero (or root) of the polynomial.",
            "Multiplicity describes how many times a particular factor repeats: if $(x-r)^k$ appears in the "
            "factored form, the root $x=r$ has multiplicity $k$.",
            "Multiplicity connects directly to graph behavior: an odd multiplicity means the graph crosses "
            "straight through the x-axis at that root, while an even multiplicity means the graph only touches "
            "the x-axis and turns back around.",
            "Higher odd multiplicities (like $3$ or $5$) still cross the x-axis, but the graph flattens out "
            "noticeably near that point, almost pausing before continuing through.",
            "When solving, always report a repeated root's multiplicity if asked, rather than just listing the "
            "distinct value once and moving on.",
            "This concept ties every earlier idea in the unit together: factoring reveals the factors, "
            "division and the rational root theorem find the roots, and multiplicity explains exactly how the "
            "graph behaves at each one.",
        ],
        "Multiplicity is the final piece that connects algebra (the factored equation) to geometry (the exact "
        "shape of the graph at each root), completing the full picture of a polynomial that this unit builds "
        "toward.",
        "Factor completely first. For each distinct factor, read its exponent as the multiplicity. Then decide "
        "cross (odd) or touch (even) for each root before sketching or describing the graph.",
        solved(16, "Solve $x^2(x-3)=0$ and state the multiplicity of each root.",
               ["The equation is already factored: $x^2(x-3)=0$.",
                "The factor $x^2$ gives root $x=0$ with multiplicity $2$ (even).",
                "The factor $(x-3)$ gives root $x=3$ with multiplicity $1$ (odd)."],
               "$x=0$ (multiplicity 2), $x=3$ (multiplicity 1)", "", "Easy")
        + solved(17, "Solve $x^3-4x^2+4x=0$ and describe the graph's behavior at each root.",
                 ["Factor out the GCF first: $x(x^2-4x+4)=0$.",
                  "Factor the remaining trinomial: $x(x-2)^2=0$.",
                  "Roots are $x=0$ (multiplicity $1$, odd, so the graph crosses) and $x=2$ (multiplicity $2$, "
                  "even, so the graph touches and turns around)."],
                 "$x=0$ (crosses), $x=2$ (touches)", "", "Medium")
        + solved(18, "For $y=(x-2)^3(x+1)$, solve for the roots and fully describe the graph's behavior at "
                     "each one.",
                 ["The equation is already factored: $(x-2)^3(x+1)=0$.",
                  "Root $x=2$ has multiplicity $3$ (odd), so the graph crosses the x-axis there, but flattens "
                  "out noticeably near the crossing because the multiplicity is higher than $1$.",
                  "Root $x=-1$ has multiplicity $1$ (odd), so the graph crosses normally, without flattening."],
                 "$x=2$ (crosses, flattened), $x=-1$ (crosses normally)", "Higher odd multiplicities still "
                "cross, but the higher the odd power, the flatter the crossing looks near that point.", "Honors"),
        ("Writing a repeated root only once and losing its multiplicity",
         "It is easy to simplify $(x-2)^2$ down to just “$x=2$” and forget to also report that this root has "
         "multiplicity $2$, especially when a question only asks you to “solve.” Whenever a factor is raised to "
         "a power greater than $1$, always state both the root and its multiplicity, since the multiplicity "
         "changes how the graph behaves there."),
        ("Match each factor's exponent to cross or touch",
         "For every distinct factor in a fully factored polynomial, look at its exponent: odd exponents always "
         "mean the graph crosses the x-axis at that root, and even exponents always mean the graph touches the "
         "x-axis and turns back without crossing. Apply this rule to every root separately before sketching."),
        [
            "I can solve a factored polynomial equation and identify every root.",
            "I can state the multiplicity of a repeated root from its factored form.",
            "I can predict whether a graph crosses or touches the x-axis based on multiplicity.",
        ],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        "Grade 10 Algebra 2",
        [
            "Identify degree, leading coefficient, and end behavior",
            "Factor using GCF, grouping, and special products (squares and cubes)",
            "Divide polynomials using long division and synthetic division",
            "Apply the remainder theorem and factor theorem",
            "Find zeros using the rational root theorem, including u-substitution",
            "Solve polynomial equations and interpret multiplicity on the graph",
        ],
        body,
        practice_slots(31, 50),
    )
    return title, description, content, _u4_questions()
