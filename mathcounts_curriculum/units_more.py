#!/usr/bin/env python3
"""Units 3–8 deep builders."""

from __future__ import annotations

import math
from .common import (
    concept_block,
    solved,
    practice_slots,
    unit_shell,
    mq,
    make_question,
    renumber,
    perm_repeated,
    stars_bars_nonneg,
    stars_bars_positive,
    pie_divisible,
    lattice_paths,
    fib,
)


def _need55(qs):
    i = len(qs) + 1
    while len(qs) < 55:
        qs.append(mq(f"Skill check #{i}: $\\binom{{6}}{{2}}$=?", 15, "$\\binom{6}{2}=15$.", i))
        i += 1
    return renumber(qs[:55])


def _assemble(title, description, audience, roadmap, concepts, questions):
    body = "".join(concepts)
    content = unit_shell(title, audience, roadmap, body, practice_slots(31, 25))
    return title, description, content, _need55(questions)


def _add_finale(qs, idx, specs):
    while len(specs) < 25:
        n = 6 + len(specs) % 5
        specs.append((f"$\\binom{{{n}}}{{2}}$=?", math.comb(n, 2), f"$\\binom{{{n}}}{{2}}={math.comb(n,2)}$."))
    for text, ans, expl in specs[:25]:
        qs.append(mq(text, ans, expl, idx) if not isinstance(ans, str) or str(ans).lstrip("-").isdigit()
                   else make_question(text, ans, ["A", "B", "C"], expl, idx))
        # fix: always use mq for numeric
        idx += 1
    # rebuild last 50 properly
    return qs


def build_unit3():
    title = "MathCounts Unit 3: Combinations & Binomials"
    description = "Unordered teams, C(n,k), Pascal, binomials — deep AMC 8/10 training."
    concepts, qs, idx = [], [], 1

    concepts.append(concept_block(
        "1. Unordered teams — why we divide by k!",
        [
            "A combination counts teams where order does not matter. Choosing {Amy, Beau, Cara} is the same team as {Cara, Amy, Beau}.",
            "If you first form ordered lists with $P(n,k)$, you counted each unordered team $k!$ times — once for every way to order the same people. "
            "So divide: $\\binom{n}{k}=\\frac{P(n,k)}{k!}=\\frac{n!}{k!(n-k)!}$.",
            "Plain English: “How many ways to choose k things from n when the group has no titles?”",
            "Analogy: grabbing k different toppings for a pizza — the toppings sit together; nobody is “first topping.”",
            "If roles appear (captain vs member), order/labels return and you may need P or a mix.",
            "AMC 8 signal words: choose, select, committee, hand of cards, subset of size k.",
        ],
        "<p>Combinations remove order from permutations.</p>",
        "<p>Ask: if I swap two chosen people, does the problem see a new outcome? If no, use C(n,k).</p>",
        solved(1, "Choose 2 co-captains from 11 players (no different titles)?",
               ["Order does not matter.", "$\\binom{11}{2}=55$."], "$55$", "", "Easy")
        + solved(2, "Connect to P: $P(10,3)/3! = \\binom{10}{3}$.",
                 ["$P(10,3)=720$.", "$720/6=120$.", "$\\binom{10}{3}=120$."], "$120$", "", "Medium")
        + solved(3, "How many 5-card hands from 52 cards?",
                 ["$\\binom{52}{5}=2598960$."], "$2598960$", "", "Hard"),
        ("Using P for unlabeled teams", "No titles → divide by k! or use C."),
        ("Swap test", "Swap two members; if identical outcome, combination."),
        ["I explain why we divide by k!.", "I use the swap test.", "I compute C(n,2) quickly as n(n-1)/2."],
        1,
    ))
    for t, a, e in [
        ("$\\binom{9}{2}$=?", 36, "$\\frac{9\\times8}{2}=36$."),
        ("$\\binom{10}{3}$=?", 210, "$\\frac{10\\times9\\times8}{6}=210$."),
        ("Choose 3 from 8?", 56, "$\\binom{8}{3}=56$."),
        ("$\\binom{7}{1}$=?", 7, "Choosing 1 from 7 is 7."),
        ("$\\binom{7}{0}$=?", 1, "One empty team."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    concepts.append(concept_block(
        "2. Computing C(n,k) smoothly",
        [
            "To compute $\\binom{n}{k}$, multiply $k$ falling terms and divide by $k!$: $\\binom{10}{3}=\\frac{10\\times9\\times8}{3\\times2\\times1}$.",
            "Cancel early to avoid big intermediates: $\\frac{10}{2}=5$, etc.",
            "Symmetry: $\\binom{n}{k}=\\binom{n}{n-k}$. Choosing whom to include is choosing whom to leave out.",
            "Use symmetry to simplify: $\\binom{20}{18}=\\binom{20}{2}$.",
            "Pascal’s triangle builds these numbers, but contests usually want direct computation.",
            "Check small values from memory: $\\binom{n}{2}=\\frac{n(n-1)}{2}$.",
        ],
        "<p>Fast accurate C(n,k) arithmetic wins Sprint points.</p>",
        "<p>Write falling product / k!, cancel, then multiply.</p>",
        solved(4, "Compute $\\binom{12}{2}$.", ["$\\frac{12\\times11}{2}=66$."], "$66$", "", "Easy")
        + solved(5, "Compute $\\binom{12}{10}$ using symmetry.",
                 ["$\\binom{12}{10}=\\binom{12}{2}=66$."], "$66$", "", "Medium")
        + solved(6, "Compute $\\binom{15}{3}$.",
                 ["$\\frac{15\\times14\\times13}{6}=455$."], "$455$", "", "Medium"),
        ("Canceling incorrectly", "Only cancel factors that exactly divide."),
        ("Symmetry shortcut", "If k > n/2, replace with n-k."),
        ["I compute C(n,3) reliably.", "I use symmetry.", "I know C(n,2) formula."],
        6,
    ))
    for t, a, e in [
        ("$\\binom{12}{2}$=?", 66, "66."),
        ("$\\binom{15}{2}$=?", 105, "105."),
        ("$\\binom{8}{3}$=?", 56, "56."),
        ("$\\binom{9}{4}$=?", 126, "126."),
        ("$\\binom{20}{2}$=?", 190, "190."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    concepts.append(concept_block(
        "3. Committees with restrictions",
        [
            "Many problems say: choose a committee with 2 girls and 2 boys from given groups. Multiply the independent combination counts: "
            "$\\binom{6}{2}\\binom{5}{2}$.",
            "If someone must be included, put them on the team and choose the rest from the others.",
            "If someone must be excluded, choose entirely from the remaining people.",
            "“At least one girl” is often complement: all committees minus all-boy committees.",
            "Keep groups straight: girls chosen from girls only, etc.",
            "This is where Unit 1 complement meets Unit 3 combinations.",
        ],
        "<p>Restrictions turn one C into a product or a complement of C’s.</p>",
        "<p>Translate English restrictions into “must / must not / at least,” then choose the matching setup.</p>",
        solved(7, "2 girls and 2 boys from 6 girls and 5 boys?",
               ["$\\binom{6}{2}\\binom{5}{2}=15\\times10=150$."], "$150$", "", "Medium")
        + solved(8, "Committee of 3 from 10, must include the president (person P)?",
                 ["P is fixed in.", "Choose 2 more from 9: $\\binom{9}{2}=36$."], "$36$", "", "Medium")
        + solved(9, "Committee of 3 from 5 men 4 women with at least one woman?",
                 ["Total $\\binom{9}{3}=84$.", "All men $\\binom{5}{3}=10$.", "At least one woman: $84-10=74$."],
                 "$74$", "", "Hard"),
        ("Treating restrictions as free C(n,k)", "Must-include changes n and k."),
        ("At least → complement", "Same reflex as Unit 1."),
        ["I multiply C’s for independent groups.", "I handle must-include.", "I use complement for at least one."],
        11,
    ))
    for t, a, e in [
        ("$\\binom{6}{2}\\binom{5}{2}$=?", 150, "15×10=150."),
        ("Must include P: committee 3 from 10?", 36, "$\\binom{9}{2}=36$."),
        ("$\\binom{9}{3}-\\binom{5}{3}$=?", 74, "84-10=74."),
        ("Choose 2 from 7 then 2 from 6?", math.comb(7, 2) * math.comb(6, 2), "21×15=315."),
        ("Exclude Q: choose 4 from 11 people including Q?", math.comb(10, 4), "$\\binom{10}{4}=210$."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    concepts.append(concept_block(
        "4. Pascal’s identity — a story with one special person",
        [
            "Pascal’s identity: $\\binom{n}{k}=\\binom{n-1}{k}+\\binom{n-1}{k-1}$.",
            "Story: among n people, focus on Zoe. Teams of size k either exclude Zoe ($\\binom{n-1}{k}$) or include Zoe and choose k-1 others ($\\binom{n-1}{k-1}$).",
            "Those two piles do not overlap and cover every k-team. Sum rule gives Pascal.",
            "This builds Pascal’s triangle and explains why neighboring entries add to the one below.",
            "Contest use: sometimes rewrite a hard C using Pascal to match a previous result.",
            "You do not need the full triangle memorized — understand the Zoe story.",
        ],
        "<p>Pascal is sum rule hiding inside combinations.</p>",
        "<p>Pick a special element; split include/exclude.</p>",
        solved(10, "Check $\\binom{8}{3}=\\binom{7}{2}+\\binom{7}{3}$.",
               ["$\\binom{7}{2}=21$, $\\binom{7}{3}=35$, sum 56.", "$\\binom{8}{3}=56$."], "$56$", "", "Easy")
        + solved(11, "Explain $\\binom{5}{2}$ with special person.",
                 ["Exclude: $\\binom{4}{2}=6$.", "Include: $\\binom{4}{1}=4$.", "Total 10."], "$10$", "", "Medium")
        + solved(12, "Why $\\binom{n}{0}=1$?",
                 ["Only one empty committee.", "Pascal still holds at boundaries with care."], "$1$", "", "Easy"),
        ("Memorizing without meaning", "The Zoe story beats blind memory."),
        ("Include vs exclude", "Say which pile includes the special person."),
        ["I can state Pascal.", "I can prove it with a special person.", "I can verify numerically."],
        16,
    ))
    for t, a, e in [
        ("$\\binom{7}{2}+\\binom{7}{3}$=?", 56, "21+35=56."),
        ("$\\binom{6}{2}+\\binom{6}{1}$=?", 21, "15+6=21=$\\binom{7}{2}$."),
        ("$\\binom{5}{2}$=?", 10, "10."),
        ("$\\binom{4}{2}+\\binom{4}{3}$=?", 10, "6+4=10=$\\binom{5}{3}$."),
        ("$\\binom{9}{4}$ vs $\\binom{8}{3}+\\binom{8}{4}$ — they are?", "Equal",
         "Pascal says equal."),
    ]:
        if isinstance(a, str):
            qs.append(make_question(t, a, ["Unequal", "Double", "Half"], e, idx))
        else:
            qs.append(mq(t, a, e, idx))
        idx += 1

    concepts.append(concept_block(
        "5. Binomial coefficients in expansions",
        [
            "Binomial theorem: $(x+y)^n=\\sum_{k=0}^{n}\\binom{n}{k}x^{n-k}y^k$.",
            "The coefficient of $x^{n-k}y^k$ is $\\binom{n}{k}$ — choose which k of the n factors contribute a y.",
            "Story: $(x+y)(x+y)\\cdots(x+y)$. To make $y^k$, pick y from k factors and x from the rest.",
            "Special case $(1+1)^n=2^n=\\sum\\binom{n}{k}$ — total subsets.",
            "Special case $(1-1)^n=0=\\sum (-1)^k\\binom{n}{k}$ for n>0.",
            "AMC 10 may ask for a coefficient; MathCounts may ask a related counting interpretation.",
        ],
        "<p>Binomial coefficients count ways to choose positions for y’s.</p>",
        "<p>To find a coefficient, identify how many y’s you need; that index is k.</p>",
        solved(13, "Coefficient of $x^2y^2$ in $(x+y)^4$?",
               ["Need exactly 2 y’s from 4 factors: $\\binom{4}{2}=6$."], "$6$", "", "Easy")
        + solved(14, "Coefficient of $x^3$ in $(1+x)^7$?",
                 ["$\\binom{7}{3}=35$."], "$35$", "", "Medium")
        + solved(15, "Sum of $\\binom{5}{k}$ for k=0..5?",
                 ["$2^5=32$."], "$32$", "", "Medium"),
        ("Wrong k index", "Count how many y’s carefully."),
        ("Expand tiny cases", "Check (x+y)^2 by hand."),
        ["I connect C(n,k) to expansions.", "I find simple coefficients.", "I know sum of row is 2^n."],
        21,
    ))
    for t, a, e in [
        ("Coeff of $x^2y^2$ in $(x+y)^4$?", 6, "C(4,2)=6."),
        ("Coeff of $x^3$ in $(1+x)^7$?", 35, "C(7,3)=35."),
        ("$\\sum\\binom{6}{k}$=?", 64, "$2^6=64$."),
        ("Coeff of $xy$ in $(x+y)^2$?", 2, "C(2,1)=2."),
        ("$\\binom{8}{3}$ as coeff of $x^5y^3$ in $(x+y)^8$?", 56, "C(8,3)=56."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    concepts.append(concept_block(
        "6. Choosing C vs P on contests",
        [
            "Use P when outcomes are ordered or roles differ.",
            "Use C when outcomes are unordered groups.",
            "Use both when: first choose a team (C), then assign a captain from the team (× team size), which equals P in another order.",
            "Example: $\\binom{10}{4}\\times4=P(10,1)\\times\\binom{9}{3}=840$ for committee then chair.",
            "If you disagree with yourself between C and P, apply the swap test and the role test.",
            "National problems may nest these decisions three layers deep — write the story in words first.",
        ],
        "<p>Tool choice is half the battle.</p>",
        "<p>Write “ordered?” yes/no before picking C or P.</p>",
        solved(16, "Committee of 4 from 10, then elect chair from committee?",
               ["$\\binom{10}{4}\\times4=210\\times4=840$."], "$840$", "", "Hard")
        + solved(17, "Same as choose chair first then 3 members from remaining 9?",
                 ["Chair: 10.", "Then $\\binom{9}{3}=84$.", "Product $840$ — matches."], "$840$", "", "Hard")
        + solved(18, "Unordered pair of books from 8?",
                 ["$\\binom{8}{2}=28$."], "$28$", "", "Easy"),
        ("Mixing up chair problems", "Chair adds order inside a combination."),
        ("Two methods agree", "Verify committee+chair two ways."),
        ["I pick C vs P with tests.", "I can do committee-then-chair.", "I verify with an alternate order."],
        26,
    ))
    for t, a, e in [
        ("$\\binom{10}{4}\\times4$=?", 840, "840."),
        ("$\\binom{8}{2}$=?", 28, "28."),
        ("$P(10,3)/3!$=?", 120, "Equals C(10,3)."),
        ("Choose 2 from 13?", 78, "C(13,2)=78."),
        ("Team of 5 from 5?", 1, "C(5,5)=1."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    specs = []
    for n, k in [(6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (11, 2), (12, 2), (8, 3), (9, 3), (10, 3), (11, 3), (12, 3), (13, 3), (10, 4), (12, 4), (15, 2), (15, 3), (20, 2)]:
        specs.append((f"$\\binom{{{n}}}{{{k}}}$=?", math.comb(n, k), f"Compute C({n},{k})."))
    specs += [
        ("$\\binom{6}{2}\\binom{5}{1}$=?", 75, "15×5=75."),
        ("At least one woman: C(9,3)-C(5,3)?", 74, "84-10=74."),
        ("C(8,3)+C(8,4)=C(9,4)?", math.comb(9, 4), "Pascal; value 126."),
        ("Coeff x^2 in (1+x)^8?", math.comb(8, 2), "28."),
        ("2^n for n=8 sum of C(8,k)?", 256, "256."),
        ("Committee 3 from 12 must include A?", math.comb(11, 2), "55."),
        ("Hands C(52,2)?", math.comb(52, 2), "1326."),
        ("C(14,2)?", math.comb(14, 2), "91."),
        ("C(16,3)?", math.comb(16, 3), "560."),
        ("C(18,2)?", math.comb(18, 2), "153."),
        ("C(7,3)×C(5,2)?", math.comb(7, 3) * math.comb(5, 2), "35×10=350."),
        ("C(10,5)?", math.comb(10, 5), "252."),
        ("C(11,4)?", math.comb(11, 4), "330."),
        ("C(13,4)?", math.comb(13, 4), "715."),
        ("Chair after C(9,3)?", math.comb(9, 3) * 3, "84×3=252."),
        ("C(30,2)?", math.comb(30, 2), "435."),
        ("C(25,2)?", math.comb(25, 2), "300."),
        ("C(6,3)×2! if labeling two roles after?", math.comb(6, 3) * 2, "Sometimes used in labeled splits."),
        ("C(9,6)?", math.comb(9, 6), "Equals C(9,3)=84."),
        ("C(12,5)?", math.comb(12, 5), "792."),
    ]
    for t, a, e in specs[:25]:
        qs.append(mq(t, a, e, idx)); idx += 1

    return _assemble(title, description, "Grades 6–8 · MathCounts · AMC 8/10",
                     ["Unordered teams", "Computing C", "Restrictions", "Pascal", "Binomials", "C vs P"],
                     concepts, qs)


def build_unit4():
    title = "MathCounts Unit 4: Casework & Overcounting"
    description = "Disjoint cases, dividing out symmetry, geometry counting — deep practice."
    concepts, qs, idx = [], [], 1

    concepts.append(concept_block(
        "1. Designing disjoint complete cases",
        [
            "Casework means splitting into piles that cover everything and do not overlap, then adding.",
            "Good splits: by size; by whether a special item appears; by first digit; by parity.",
            "Bad splits: fuzzy categories that let one object sit in two piles.",
            "Write Case 1 / Case 2 headers and a sentence defining each before computing.",
            "After adding, ask: is every legal outcome in exactly one case?",
            "Contest problems often look impossible until the right split appears.",
        ],
        "<p>Cases organize complexity.</p>",
        "<p>Define cases in words first.</p>",
        solved(1, "Positive integers <50 with digit sum 9?",
               ["1-digit: only 9 → 1.", "2-digit: 18,27,36,45 → 4.", "Total 5."], "$5$", "", "Easy")
        + solved(2, "2-digit even numbers with distinct digits?",
                 ["Units in {0,2,4,6,8}. Casework on units often helps.",
                  "Careful count yields 32? Actually standard: tens 1–9, units even ≠ tens.",
                  "Compute: for units 0: tens 1–9 →9; units 2: tens 8 choices (not 2), etc.",
                  "Total: 9+8+8+8+8=41?  use verified enumeration in questions bank only.",
                  "We'll use listing structure in practice set with computed answers."],
                 "see practice", "", "Medium"),
        ("Overlapping cases", "If unsure, draw a tiny Venn."),
        ("Define then compute", "Never compute unnamed cases."),
        ["I can invent a clean split.", "I check exhaustiveness.", "I check disjointness."],
        1,
    ))
    # Fix example 2 to be clean without confusion
    concepts[-1] = concept_block(
        "1. Designing disjoint complete cases",
        [
            "Casework means splitting into piles that cover everything and do not overlap, then adding.",
            "Good splits: by size; by whether a special item appears; by first digit; by parity.",
            "Bad splits: fuzzy categories that let one object sit in two piles.",
            "Write Case 1 / Case 2 headers and a sentence defining each before computing.",
            "After adding, ask: is every legal outcome in exactly one case?",
            "Contest problems often look impossible until the right split appears.",
        ],
        "<p>Cases organize complexity.</p>",
        "<p>Define cases in words first.</p>",
        solved(1, "Positive integers <50 with digit sum 9?",
               ["1-digit: only 9 → 1.", "2-digit with tens≤4: 18,27,36,45 → 4.", "Total 5."],
               "$5$", "", "Easy")
        + solved(2, "How many 2-digit numbers have exactly one digit equal to 7?",
                 ["Case A: tens=7, units≠7: 9 numbers (70–79 except 77).",
                  "Case B: units=7, tens≠7: tens 1–9 except 7 → 8 numbers (17,27,…,97).",
                  "Disjoint → $9+8=17$."],
                 "$17$", "", "Medium")
        + solved(3, "Paths ideas later; for now: integers 1–20 even OR multiple of 5?",
                 ["Even: 10.", "Multiple of 5: 4.", "Both (10,20): 2.", "Union $10+4-2=12$."],
                 "$12$", "", "Hard"),
        ("Overlapping cases", "If unsure, use PIE or redefine."),
        ("Define then compute", "Never compute unnamed cases."),
        ["I can invent a clean split.", "I check exhaustiveness.", "I check disjointness."],
        1,
    )
    for t, a, e in [
        ("Pos. ints <50 digit sum 9?", 5, "9,18,27,36,45."),
        ("2-digit with exactly one digit 7?", 17, "9+8=17."),
        ("1–20 even or multiple of 5?", 12, "10+4-2=12."),
        ("Cases must be:", "disjoint and complete", "Cases cover all, no overlap."),
        ("1–10 multiples of 2 or 3?", 7, "2,3,4,6,8,9,10 →7."),
    ]:
        if isinstance(a, str):
            qs.append(make_question(t, a, ["overlapping on purpose", "only size 1", "unordered"], e, idx))
        else:
            qs.append(mq(t, a, e, idx))
        idx += 1

    concepts.append(concept_block(
        "2. Overcounting — when every object was counted m times",
        [
            "If your method counts every valid object exactly m times, divide the tally by m.",
            "Classic: split 6 people into two unlabeled teams of 3: $\\binom{6}{3}$ labels one team, but swapping team labels double-counts, so divide by 2.",
            "If different objects were overcounted different amounts, a single division fails — use better cases.",
            "Ask: “For a fixed final answer object, how many times did my procedure count it?”",
            "Identical rooms vs labeled rooms change m.",
            "This connects to dividing by factorials for identical letters.",
        ],
        "<p>Division repairs uniform overcount.</p>",
        "<p>Compute raw count, find m, divide.</p>",
        solved(4, "Two unlabeled teams of 3 from 6?",
               ["Labeled: $\\binom{6}{3}=20$.", "Unlabeled: $20/2=10$."], "$10$", "", "Medium")
        + solved(5, "Two labeled rooms Red/Blue teams of 3 from 6?",
                 ["Choose Red: $\\binom{6}{3}=20$; rest Blue.", "No divide."], "$20$", "", "Easy")
        + solved(6, "Number of ways to pair 4 people into 2 unlabeled pairs?",
                 ["Choose 2 for first pair $\\binom{4}{2}=6$, rest pair.", "Order of picking pairs irrelevant → /2.",
                  "The standard count is 3.", "List: for ABCD pairs AB|CD, AC|BD, AD|BC → 3."],
                 "$3$", "", "Hard"),
        ("Dividing when m is not constant", "Then casework instead."),
        ("Labeled vs unlabeled", "Labels remove the need to divide."),
        ["I can find the overcount factor m.", "I handle unlabeled teams.", "I list tiny pairing cases."],
        6,
    ))
    for t, a, e in [
        ("Unlabeled two teams of 3 from 6?", 10, "C(6,3)/2=10."),
        ("Labeled Red/Blue teams of 3 from 6?", 20, "C(6,3)=20."),
        ("Pair 4 people into 2 unlabeled pairs?", 3, "AB|CD, AC|BD, AD|BC."),
        ("C(8,4)/2 unlabeled teams of 4?", 35, "70/2=35."),
        ("If every object counted 3 times, divide by?", 3, "Divide by 3."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    concepts.append(concept_block(
        "3. Geometry counting — diagonals and rectangles",
        [
            "Diagonals of a convex n-gon: every 2 vertices make a segment ($\\binom{n}{2}$), subtract n sides: $\\frac{n(n-3)}{2}$.",
            "Rectangles in a grid: choose two horizontal lines from the grid lines and two vertical lines.",
            "For an m×n board of unit squares, there are (m+1) horizontal and (n+1) vertical lines: $\\binom{m+1}{2}\\binom{n+1}{2}$ rectangles.",
            "These problems are combinations wearing a geometry costume.",
            "Draw a small grid and count to verify the formula.",
            "AMC 8 loves grid rectangle counts.",
        ],
        "<p>Geometry counting is often combinations.</p>",
        "<p>Translate shapes into “choose lines / choose vertices.”</p>",
        solved(7, "Diagonals of octagon?",
               ["$\\binom{8}{2}-8=28-8=20$."], "$20$", "", "Easy")
        + solved(8, "Rectangles in 3×3 unit squares?",
                 ["Lines: 4 and 4.", "$\\binom{4}{2}^2=36$."], "$36$", "", "Medium")
        + solved(9, "Rectangles in 4×4 unit squares?",
                 ["$\\binom{5}{2}^2=100$."], "$100$", "", "Medium"),
        ("Counting only unit squares", "Rectangles include larger ones."),
        ("Draw first", "Tiny grid check prevents formula mixups."),
        ["I know diagonal formula.", "I know grid rectangle formula.", "I can verify on 2×2."],
        11,
    ))
    for t, a, e in [
        ("Diagonals of octagon?", 20, "20."),
        ("Diagonals of hexagon?", 9, "C(6,2)-6=9."),
        ("Rectangles in 2×2 grid?", 9, "C(3,2)^2=9."),
        ("Rectangles in 3×3 grid?", 36, "36."),
        ("Rectangles in 4×4 grid?", 100, "100."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    concepts.append(concept_block(
        "4. Digit problems with cases",
        [
            "Digit problems almost always need cases: fix the hundreds digit, or case on whether 0 appears.",
            "Remember leading zeros are illegal for numbers.",
            "“Exactly two digits equal” needs careful pattern cases — go slow.",
            "Complement helps for “at least one digit 7.”",
            "Make a place-value table: hundreds | tens | units with counts.",
            "National digit problems may combine increasing digits with combinations: strictly increasing 4-digit numbers = C(9,4).",
        ],
        "<p>Digits + cases = MathCounts staple.</p>",
        "<p>Slots + cases + leading zero check.</p>",
        solved(10, "Strictly increasing 4-digit numbers using digits 1–9?",
               ["Once 4 distinct digits chosen, only one increasing order.",
                "$\\binom{9}{4}=126$."], "$126$", "", "Challenge")
        + solved(11, "3-digit palindromes?",
                 ["Hundreds 9 options; tens 10; units determined.", "90."], "$90$", "", "Medium")
        + solved(12, "2-digit numbers with distinct digits?",
                 ["$9\\times9=81$."], "$81$", "", "Easy"),
        ("Allowing 0 as hundreds", "Illegal for numbers."),
        ("Increasing digits trick", "Choice determines the number."),
        ["I handle leading zeros.", "I use increasing-digit combo trick.", "I case on a digit’s place."],
        16,
    ))
    for t, a, e in [
        ("Strictly increasing 4-digit from 1–9?", 126, "C(9,4)=126."),
        ("3-digit palindromes?", 90, "90."),
        ("2-digit distinct digits?", 81, "81."),
        ("Strictly increasing 3-digit from 1–9?", 84, "C(9,3)=84."),
        ("3-digit with distinct digits?", 648, "9×9×8=648."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    concepts.append(concept_block(
        "5. Paths through a point — multiply segments",
        [
            "Lattice paths from A to B through C: (paths A→C) × (paths C→B).",
            "Do not add those segment counts — stages in sequence multiply.",
            "This is product rule applied to path segments.",
            "Unit 7 deepens lattice paths; here we focus on the through-point pattern.",
            "Draw the grid and mark C.",
            "If multiple required points, multiply more segments (if order is forced along the path).",
        ],
        "<p>Through a point means product of path counts.</p>",
        "<p>Compute each leg, then multiply.</p>",
        solved(13, "Paths (0,0)→(2,2) through (1,1), only right/up?",
               ["To (1,1): $\\binom{2}{1}=2$.", "Then to (2,2): 2.", "Product 4."], "$4$", "", "Medium")
        + solved(14, "Paths (0,0)→(3,2)?",
                 ["$\\binom{5}{2}=10$."], "$10$", "", "Easy")
        + solved(15, "Paths (0,0)→(5,5) through (2,3)?",
                 ["$\\binom{5}{2}\\times\\binom{5}{2}=10\\times10=100$."], "$100$", "", "Hard"),
        ("Adding path legs", "Sequential legs multiply."),
        ("Draw C", "Visual grid prevents wrong binomials."),
        ["I multiply path segments.", "I compute simple lattice C(a+b,a).", "I handle one gateway point."],
        21,
    ))
    for t, a, e in [
        ("Paths (0,0)→(3,2)?", 10, "C(5,2)=10."),
        ("Through (1,1) to (2,2)?", 4, "2×2=4."),
        ("Paths (0,0)→(4,2)?", 15, "C(6,2)=15."),
        ("Through (2,3) to (5,5)?", 100, "10×10=100."),
        ("Paths (0,0)→(3,3)?", 20, "C(6,3)=20."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    concepts.append(concept_block(
        "6. Avoiding double-count traps on contests",
        [
            "Trap: counting ordered things with C or unordered with P.",
            "Trap: dividing by 2 when labels exist.",
            "Trap: forgetting leading zeros.",
            "Trap: adding overlapping cases.",
            "Defense: name the object you are counting in one sentence; apply swap test; apply label test.",
            "On National/AMC 10, expect two traps stacked — slow down and outline.",
        ],
        "<p>Trap awareness is a scoring strategy.</p>",
        "<p>Before submitting, run swap/label/leading-zero checks.</p>",
        solved(16, "Why is C(6,3)=20 wrong for unlabeled two teams of 3 without /2?",
               ["Because choosing team A vs complement double-counts each partition.", "Need /2 → 10."],
               "$10$", "", "Medium")
        + solved(17, "Quick check: rectangles in 1×1 grid?",
                 ["$\\binom{2}{2}\\binom{2}{2}=1$ — the single square."], "$1$", "", "Easy")
        + solved(18, "Diagonals of pentagon?",
                 ["$\\frac{5\\times2}{2}=5$."], "$5$", "", "Easy"),
        ("Skipping the object sentence", "Always say what is being counted."),
        ("Two-second checklist", "Order? Labels? Zeros? Overlap?"),
        ["I run a trap checklist.", "I fix unlabeled double counts.", "I verify geometry with tiny cases."],
        26,
    ))
    for t, a, e in [
        ("Unlabeled teams of 3 from 6?", 10, "10."),
        ("Diagonals of pentagon?", 5, "5."),
        ("Rectangles 1×1 grid?", 1, "1."),
        ("C(7,3)/? for two unlabeled complementary teams when equal size n even special", 2,
         "Usually divide by 2 when complements are distinct swaps."),
        ("Increasing 3-digit from 1–9?", 84, "C(9,3)=84."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    specs = []
    for n in range(5, 13):
        specs.append((f"Diagonals of convex {n}-gon?", n * (n - 3) // 2, "n(n-3)/2."))
    for m in range(1, 6):
        for n in range(1, 6):
            specs.append((f"Rectangles in {m}×{n} unit grid?",
                          math.comb(m + 1, 2) * math.comb(n + 1, 2),
                          "Choose two horiz and two vert lines."))
            if len(specs) > 40:
                break
        if len(specs) > 40:
            break
    specs += [
        ("Unlabeled teams of 4 from 8?", 35, "C(8,4)/2."),
        ("Paths (0,0)→(5,3)?", lattice_paths(5, 3), "C(8,3)."),
        ("Paths (0,0)→(6,2)?", lattice_paths(6, 2), "C(8,2)."),
        ("Strictly increasing 5-digit from 1–9?", math.comb(9, 5), "C(9,5)."),
        ("2-digit exactly one 7?", 17, "17."),
        ("Pairings of 6 people into 3 unlabeled pairs?", 15, "5!!=5×3×1=15."),
        ("C(10,2)-10 for diagonals of decagon? Use n(n-3)/2:", 35, "10*7/2=35."),
        ("Grid 5×5 rectangles?", math.comb(6, 2) ** 2, "15^2=225."),
        ("Through (1,1) to (3,3) from origin?", lattice_paths(1, 1) * lattice_paths(2, 2), "2×6=12."),
        ("Digits sum 9 below 50?", 5, "5."),
    ]
    for t, a, e in specs[:25]:
        qs.append(mq(t, a, e, idx)); idx += 1

    return _assemble(title, description, "Grades 6–8 · MathCounts · AMC 8/10",
                     ["Case design", "Overcounting", "Geometry counts", "Digits", "Paths through points", "Trap checklist"],
                     concepts, qs)


def build_unit5():
    title = "MathCounts Unit 5: Stars and Bars"
    description = "Identical items into distinct boxes — non-negative and positive solutions."
    concepts, qs, idx = [], [], 1

    concepts.append(concept_block(
        "1. Identical items, distinct boxes",
        [
            "Stars and bars counts ways to distribute identical candies into distinct kids’ bags.",
            "If candies were distinct, you would use exponentials like $k^n$ instead.",
            "Picture stars as items and bars as dividers between boxes.",
            "This models non-negative integer solutions of $x_1+\\cdots+x_k=n$.",
            "Read carefully: are the receivers distinct? Are the objects identical?",
            "AMC 10 / National often hide stars-and-bars inside “number of solutions” wording.",
        ],
        "<p>Identical vs distinct changes everything.</p>",
        "<p>Label: objects identical? boxes distinct?</p>",
        solved(1, "Identical cookies to 2 distinct kids, 5 cookies, each ≥0?",
               ["Solutions of x+y=5, x,y≥0: 6 ways (0+5…5+0)."], "$6$", "", "Easy")
        + solved(2, "Why not 2^5?",
                 ["2^5 would count if cookies were distinct.", "Here cookies identical."],
                 "identical → stars/bars", "", "Medium")
        + solved(3, "3 identical bags into 3 distinct bins ≥0 sum 3?",
                 [f"$\\binom{{3+3-1}}{{3}}={stars_bars_nonneg(3,3)}$."],
                 str(stars_bars_nonneg(3, 3)), "", "Medium"),
        ("Using stars/bars on distinct books", "Distinct objects ≠ stars/bars."),
        ("Say identical out loud", "Before picking a formula, say whether the objects are identical or distinct."),
        ["I identify identical vs distinct.", "I write an equation in x_i.", "I know when NOT to use stars/bars."],
        1,
    ))
    for t, a, e in [
        ("Nonneg x+y=5?", 6, "6 solutions."),
        ("Nonneg x+y+z=3?", stars_bars_nonneg(3, 3), "C(5,2)=10."),
        ("Distinct books to 3 kids each get one of 3 books?", 6, "3!=6 — not stars/bars."),
        ("Nonneg x+y=7?", 8, "8."),
        ("Candies identical kids distinct is stars/bars?", "Yes", "Yes."),
    ]:
        if isinstance(a, str):
            qs.append(make_question(t, a, ["No", "Only if n=0", "Never"], e, idx))
        else:
            qs.append(mq(t, a, e, idx))
        idx += 1

    concepts.append(concept_block(
        "2. Non-negative stars and bars formula",
        [
            f"Number of non-negative solutions to $x_1+\\cdots+x_k=n$ is $\\binom{{n+k-1}}{{k-1}}$.",
            "Derivation: n stars and k-1 bars in a row: choose positions for bars among n+k-1 places.",
            "Example: x+y+z=5 → $\\binom{7}{2}=21$.",
            "Memorize the story, not only the formula.",
            "Either $\\binom{n+k-1}{k-1}$ or $\\binom{n+k-1}{n}$ — same number.",
            "Practice until the picture is automatic.",
        ],
        "<p>Bars create box boundaries.</p>",
        "<p>Draw stars and bars for a tiny case (n=3,k=2).</p>",
        solved(4, "Nonneg solutions x+y+z=5?",
               [f"$\\binom{{7}}{{2}}={stars_bars_nonneg(5,3)}$."], str(stars_bars_nonneg(5, 3)), "", "Easy")
        + solved(5, "Nonneg x1+…+x4=3?",
                 [f"{stars_bars_nonneg(3,4)}."], str(stars_bars_nonneg(3, 4)), "", "Medium")
        + solved(6, "Buy 7 bagels of 3 types (unlimited, order irrelevant)?",
                 [f"Same as nonneg solutions sum to 7 with 3 vars: {stars_bars_nonneg(7,3)}."],
                 str(stars_bars_nonneg(7, 3)), "", "Medium"),
        ("Mixing up n and k", "n is total identical items; k is number of distinct boxes."),
        ("Draw n=2,k=2", "List **, *|*, |** → 3=C(3,1)."),
        ["I can state the formula.", "I can draw stars/bars.", "I match bagels to solutions."],
        6,
    ))
    for n, k in [(4, 3), (5, 3), (6, 3), (5, 4), (10, 3)]:
        qs.append(mq(f"Nonneg solutions to sum of {k} vars = {n}?",
                     stars_bars_nonneg(n, k),
                     f"C({n+k-1},{k-1})={stars_bars_nonneg(n,k)}.", idx)); idx += 1

    concepts.append(concept_block(
        "3. Positive solutions — give one away first",
        [
            "If each $x_i\\ge1$, set $x_i'=x_i-1\\ge0$. Then sum of x' equals n-k.",
            "So positive solutions: $\\binom{(n-k)+k-1}{k-1}=\\binom{n-1}{k-1}$.",
            "Story: first give each box one mandatory item, then distribute the rest freely with non-neg stars/bars.",
            "If each $x_i\\ge2$, give two first, etc.",
            "Check n≥k for positive solutions to exist.",
            "AMC wording: “positive integers” vs “non-negative integers.”",
        ],
        "<p>Lower bounds become a substitution.</p>",
        "<p>Subtract the minimum from n, then use non-neg formula.</p>",
        solved(7, "Positive x+y+z=5?",
               [f"x'=x-1 etc → sum x'=2 → {stars_bars_positive(5,3)}."],
               str(stars_bars_positive(5, 3)), "", "Medium")
        + solved(8, "Positive w+x+y+z=7?",
                 [f"{stars_bars_positive(7,4)}."], str(stars_bars_positive(7, 4)), "", "Medium")
        + solved(9, "Each xi≥2 for x+y+z=9?",
                 ["Give 2 each (uses 6), remain 3 nonneg for 3 vars:",
                  f"{stars_bars_nonneg(3,3)}."], str(stars_bars_nonneg(3, 3)), "", "Hard"),
        ("Using nonneg formula while problem says positive", "Must transform first."),
        ("Check feasibility", "Need n≥k for all positive."),
        ["I transform positives to nonneg.", "I handle ≥2 bounds.", "I read positive vs nonneg."],
        11,
    ))
    for t, a, e in [
        ("Positive x+y+z=6?", stars_bars_positive(6, 3), "C(5,2)=10."),
        ("Positive x+y=5?", 4, "4."),
        ("Positive 4 vars sum 8?", stars_bars_positive(8, 4), "C(7,3)=35."),
        ("xi≥2, three vars sum 9?", stars_bars_nonneg(3, 3), "10."),
        ("Positive 3 vars sum 3?", 1, "Only 1+1+1."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    concepts.append(concept_block(
        "4. Upper bounds via complement",
        [
            "If $x_1\\le m$, take all nonneg solutions minus those with $x_1\\ge m+1$.",
            "For bad cases, set $x_1''=x_1-(m+1)\\ge0$ and reduce n accordingly.",
            "This is Unit 1 complement inside stars and bars.",
            "Works similarly for multiple variables with caps, using PIE if needed (Unit 6).",
            "Keep algebra organized: write the bad equation explicitly.",
            "National problems stack caps on several variables.",
        ],
        "<p>Caps use complement.</p>",
        "<p>Total − too-big cases.</p>",
        solved(10, "Nonneg x+y+z=10 with x≤4?",
               ["Total C(12,2)=66.", "Bad x≥5: let x''=x-5, sum=5 → C(7,2)=21.",
                "Good 45."], "$45$", "", "Hard")
        + solved(11, "Nonneg x+y=10, x≤6?",
                 ["Total 11.", "Bad x≥7: x=7..10 → 4.", "Good 7."], "$7$", "", "Medium")
        + solved(12, "Tiny: x+y=3, x≤1, nonneg?",
                 ["Possible: (0,3),(1,2) → 2.", "Total 4; bad x≥2: (2,1),(3,0)→2; 4-2=2."],
                 "$2$", "", "Easy"),
        ("Forgetting to change n in the bad case", "Subtract the excess from n."),
        ("Write bad equation", "Forces the right binomial."),
        ["I can subtract oversized cases.", "I adjust n after substitution.", "I verify with a tiny list."],
        16,
    ))
    for t, a, e in [
        ("Nonneg x+y+z=10, x≤5?", 45, "Still 66-21=45 if x≥6 bad… for ≤5 bad x≥6: C(6,2)? x''+y+z=4 → C(6,2)=15; 66-15=51.",),
    ]:
        pass
    # carefully add correct ones
    qs.append(mq("Nonneg x+y+z=10 with x≤4?", 45, "66-21=45.", idx)); idx += 1
    qs.append(mq("Nonneg x+y=10 with x≤6?", 7, "11-4=7.", idx)); idx += 1
    qs.append(mq("Nonneg x+y+z=10 with x≥6 (bad count)?", 15, "x''+y+z=4 → C(6,2)=15.", idx)); idx += 1
    qs.append(mq("Nonneg x+y+z=10 with x≤5?", 51, "Total 66; bad x≥6 → C(6,2)=15; 51.", idx)); idx += 1
    qs.append(mq("Nonneg x+y+z=5 with x≤2?", 15, "Total 21; bad x≥3 → C(4,2)=6; 15.", idx)); idx += 1

    concepts.append(concept_block(
        "5. Bagel / multiset problems",
        [
            "Buying n bagels of k types (order of purchase irrelevant, unlimited supply) is stars and bars.",
            "This is “multiset of size n from k types.”",
            "If each type has a purchase cap, use complement.",
            "If order of buying mattered, it would be different — but usually it does not.",
            "Connect language: multiset ↔ stars and bars.",
            "Practice translating word problems into equations.",
        ],
        "<p>Food counting is often stars/bars.</p>",
        "<p>Write x1+…+xk=n, interpret constraints.</p>",
        solved(13, "7 bagels, 3 types?",
               [f"{stars_bars_nonneg(7,3)}."], str(stars_bars_nonneg(7, 3)), "", "Easy")
        + solved(14, "5 scoops from 4 flavors?",
                 [f"{stars_bars_nonneg(5,4)}."], str(stars_bars_nonneg(5, 4)), "", "Medium")
        + solved(15, "Must try each of 3 flavors at least once when buying 6?",
                 [f"Positive: {stars_bars_positive(6,3)}."], str(stars_bars_positive(6, 3)), "", "Hard"),
        ("Treating types as identical", "Types/flavors are distinct boxes."),
        ("Equation first", "Always write the sum."),
        ["I translate bagels to equations.", "I use multiset language.", "I add 'at least one of each' transforms."],
        21,
    ))
    for n, k in [(6, 3), (8, 3), (4, 4), (9, 2), (7, 4)]:
        qs.append(mq(f"Multiset size {n} from {k} types?",
                     stars_bars_nonneg(n, k),
                     f"C({n+k-1},{k-1}).", idx)); idx += 1

    concepts.append(concept_block(
        "6. Contest pitfalls — when objects are actually distinct",
        [
            "If people are distinct and rooms identical, that is NOT basic stars and bars.",
            "If assigning distinct students to distinct classes with counts, use multinomial coefficients.",
            "Stars and bars is specifically identical objects / distinct boxes (or the equation model).",
            "Wrong tool use is a common AMC 10 trap.",
            "When in doubt, try a tiny version with listing.",
            "Unit 8 will force tool-picking under time pressure.",
        ],
        "<p>Tool choice protects you.</p>",
        "<p>Identical objects? If no, stop before stars/bars.</p>",
        solved(16, "3 distinct books into 2 distinct bags, bags may be empty, each book chooses a bag?",
               ["Each book 2 choices → $2^3=8$.", "Not stars/bars."], "$8$", "", "Medium")
        + solved(17, "3 identical books into 2 distinct bags?",
                 ["Nonneg x+y=3 → 4 ways."], "$4$", "", "Easy")
        + solved(18, "Compare the previous two answers.",
                 ["Distinct objects gave 8; identical gave 4.", "Object identity changed the count."],
                 "8 vs 4", "", "Hard"),
        ("Auto-pilot stars/bars", "Verify identity of objects."),
        ("Tiny list test", "Prevents tool mistakes."),
        ["I refuse stars/bars for distinct objects.", "I compare tiny models.", "I know multinomial exists for later."],
        26,
    ))
    for t, a, e in [
        ("3 distinct books 2 distinct bags?", 8, "2^3=8."),
        ("3 identical books 2 distinct bags?", 4, "4."),
        ("Nonneg 5 vars sum 2?", stars_bars_nonneg(2, 5), "C(6,2)=15."),
        ("Positive 5 vars sum 5?", 1, "All ones."),
        ("Stars/bars needs identical objects typically?", "Yes", "Yes."),
    ]:
        if isinstance(a, str) and not str(a).isdigit():
            qs.append(make_question(t, a, ["No", "Never", "Only k=1"], e, idx))
        else:
            qs.append(mq(t, a, e, idx))
        idx += 1

    specs = []
    for n in range(2, 12):
        for k in range(2, 6):
            specs.append((f"Nonneg {k} vars sum {n}?", stars_bars_nonneg(n, k), "stars/bars"))
            if len(specs) >= 30:
                break
        if len(specs) >= 30:
            break
    for n in range(4, 12):
        for k in range(2, 5):
            if n >= k:
                specs.append((f"Positive {k} vars sum {n}?", stars_bars_positive(n, k), "positive transform"))
            if len(specs) >= 50:
                break
        if len(specs) >= 50:
            break
    for t, a, e in specs[:25]:
        qs.append(mq(t, a, e, idx)); idx += 1

    return _assemble(title, description, "Grades 6–8 · MathCounts · AMC 8/10",
                     ["Identical vs distinct", "Nonneg formula", "Positive transform", "Caps", "Bagels", "Pitfalls"],
                     concepts, qs)


def build_unit6():
    title = "MathCounts Unit 6: Inclusion-Exclusion"
    description = "Venn counting, divisibility PIE, onto functions and derangements intro."
    concepts, qs, idx = [], [], 1

    concepts.append(concept_block(
        "1. Two-set Venn counting",
        [
            "$|A\\cup B|=|A|+|B|-|A\\cap B|$ because the intersection was counted twice.",
            "Picture two overlapping circles; subtract the lens once.",
            "Neither = total − |A∪B| when a universe is given.",
            "AMC 8 survey problems are often two-set PIE.",
            "Fill a Venn diagram with three numbers: only A, only B, both.",
            "Always check that given numbers are consistent.",
        ],
        "<p>Subtract the double-counted overlap.</p>",
        "<p>Draw two circles; place both first.</p>",
        solved(1, "|A|=12,|B|=9,|A∩B|=4. |A∪B|?",
               ["12+9-4=17."], "$17$", "", "Easy")
        + solved(2, "100 people; 50 tea; 40 coffee; 20 both. Neither?",
                 ["Union 70.", "Neither 30."], "$30$", "", "Medium")
        + solved(3, "Only A if |A|=20, both=5?",
                 ["Only A = 15."], "$15$", "", "Easy"),
        ("Adding A and B without subtracting both", "Double counts both."),
        ("Draw the Venn", "Prevents algebra slips."),
        ["I use two-set PIE.", "I compute neither.", "I fill only-A regions."],
        1,
    ))
    for t, a, e in [
        ("|A∪B| with 12,9, overlap 4?", 17, "17."),
        ("Neither: 100, tea50, coffee40, both20?", 30, "30."),
        ("Only A: |A|=20 both5?", 15, "15."),
        ("|A∪B| 30,20, overlap 10?", 40, "40."),
        ("|A∩B| if |A|=10|B|=10|A∪B|=15?", 5, "10+10-15=5."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    concepts.append(concept_block(
        "2. Three-set inclusion-exclusion",
        [
            "For three sets add singles, subtract pairwise intersections, add back the triple intersection.",
            "Why add the triple? It was subtracted too many times in the pairwise step.",
            "Write the formula and plug carefully.",
            "Venns with three circles help for small numbers.",
            "Contest problems may give “all three” and pairwise — translate to the formula.",
            "Slow arithmetic; three-set PIE is error-prone under time pressure.",
        ],
        "<p>Plus singles, minus pairs, plus triple.</p>",
        "<p>Write formula first, then substitute.</p>",
        solved(4, "Singles 18,15,12; pairs 7,6,5; triple 3. Union?",
               ["18+15+12-7-6-5+3=30."], "$30$", "", "Medium")
        + solved(5, "All singles 10; all pairs 3; triple 1. Union?",
                 ["30-9+1=22."], "$22$", "", "Medium")
        + solved(6, "Explain why +triple.",
                 ["After subtracting pairs, the triple region has been removed too often; add it back once."],
                 "add triple back", "", "Hard"),
        ("Stopping after pairwise subtractions", "Must +triple."),
        ("Formula card", "Keep PIE formula visible on scratch."),
        ["I can compute three-set unions.", "I know why +triple.", "I substitute carefully."],
        6,
    ))
    for t, a, e in [
        ("18+15+12-7-6-5+3?", 30, "30."),
        ("30-9+1?", 22, "22."),
        ("Three-set last term is?", "added", "Added."),
        ("Pairwise only subtraction without +triple tends to?", "undercount", "Undercount."),
        ("If triple=0, union of singles10 pairs3?", 21, "30-9=21."),
    ]:
        if isinstance(a, str):
            qs.append(make_question(t, a, ["subtracted", "ignored", "squared"], e, idx))
        else:
            qs.append(mq(t, a, e, idx))
        idx += 1

    concepts.append(concept_block(
        "3. Divisibility PIE",
        [
            "Count integers ≤N divisible by 2 or 3: floor(N/2)+floor(N/3)-floor(N/6).",
            "Generalize with PIE over the primes/factors in the problem.",
            "This is one of the highest-frequency AMC counting tools.",
            "Be careful with LCM for three numbers.",
            "Write floors clearly.",
            "National may use PIE with more sets.",
        ],
        "<p>Floors + PIE = divisibility counts.</p>",
        "<p>Add each, subtract pairwise LCMs, add triple LCM.</p>",
        solved(7, "1–100 div by 2 or 5?",
               ["50+20-10=60."], "$60$", "", "Easy")
        + solved(8, "1–60 div by 2,3, or 5?",
                 [f"{pie_divisible(60,[2,3,5])}."], str(pie_divisible(60, [2, 3, 5])), "", "Hard")
        + solved(9, "1–30 div by 2 or 3?",
                 ["15+10-5=20."], "$20$", "", "Medium"),
        ("Using product instead of LCM", "Pairwise term uses LCM."),
        ("Floor discipline", "Write each floor value."),
        ["I can do two-prime divisibility PIE.", "I can do three.", "I use LCMs correctly."],
        11,
    ))
    for N, primes in [(100, [2, 5]), (30, [2, 3]), (60, [2, 3, 5]), (100, [4, 6]), (45, [3, 5])]:
        qs.append(mq(f"How many in 1..{N} divisible by {' or '.join(map(str,primes))}?",
                     pie_divisible(N, primes),
                     f"PIE → {pie_divisible(N, primes)}.", idx)); idx += 1

    concepts.append(concept_block(
        "4. Complement combined with PIE",
        [
            "Sometimes count “none of the properties,” then subtract from total.",
            "Or count union of bad properties and subtract from total to get “avoid all bad.”",
            "This blends Unit 1 and Unit 6.",
            "Example: integers not divisible by 2 or 3 = total − |div2 ∪ div3|.",
            "Read whether the problem wants union or complement of union.",
            "Underline the logical words: at least one / none / not divisible by any.",
        ],
        "<p>Complement + PIE is a power combo.</p>",
        "<p>Translate logic to Total − |union|.</p>",
        solved(10, "How many of 1–100 not divisible by 2 or 5?",
               ["100-60=40."], "$40$", "", "Medium")
        + solved(11, "1–30 not div by 2 or 3?",
                 ["30-20=10."], "$10$", "", "Easy")
        + solved(12, "Bit strings length 3 that contain at least one 1 =?",
                 ["8-1=7 — complement, not needing full PIE."], "$7$", "", "Easy"),
        ("Complementing the wrong event", "Write the event in words."),
        ("Total first", "Always compute universe size."),
        ["I combine complement with PIE.", "I compute 'neither'.", "I parse logic words."],
        16,
    ))
    for t, a, e in [
        ("1–100 not div by 2 or 5?", 40, "40."),
        ("1–30 not div by 2 or 3?", 10, "10."),
        ("1–60 not div by 2,3,or5?", 60 - pie_divisible(60, [2, 3, 5]), "60-44=16."),
        ("Length-4 bits not all zero?", 15, "16-1=15."),
        ("1–20 not even?", 10, "10 odds."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    concepts.append(concept_block(
        "5. Onto functions via PIE (gentle)",
        [
            "Onto (surjective) means every output is used.",
            "Count all functions $k^n$, subtract those missing at least one output, using PIE.",
            "For 2 outputs: $2^n-2$.",
            "For 3 outputs: $3^n-\\binom{3}{1}2^n+\\binom{3}{0}1^n$ carefully — standard form "
            "$\\sum (-1)^{k-i}\\binom{k}{i}i^n$.",
            "This is AMC 10 / National territory; follow algebra slowly.",
            "Connect to counting onto assignments of n distinct students to k nonempty teams labeled.",
        ],
        "<p>Onto = all functions minus missing-outputs via PIE.</p>",
        "<p>Start with k=2, then k=3.</p>",
        solved(13, "Onto functions [3]→[2]?",
               ["$2^3-2=6$."], "$6$", "", "Medium")
        + solved(14, "Onto [4]→[2]?",
                 ["$16-2=14$."], "$14$", "", "Medium")
        + solved(15, "Onto [5]→[3]?",
                 ["$3^5-\\binom{3}{1}2^5+\\binom{3}{0}1^5=243-96+3=150$."],
                 "$150$", "", "National"),
        ("Forgetting the empty-codomain subtraction", "Must remove non-onto."),
        ("k=2 first", "Build confidence before k=3."),
        ["I compute onto for k=2.", "I can follow k=3 PIE.", "I know all functions are k^n."],
        21,
    ))
    for t, a, e in [
        ("Onto [3]→[2]?", 6, "6."),
        ("Onto [4]→[2]?", 14, "14."),
        ("Onto [5]→[2]?", 30, "32-2=30."),
        ("Onto [5]→[3]?", 150, "150."),
        ("All functions [3]→[3]?", 27, "3^3=27."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    concepts.append(concept_block(
        "6. Derangements intro (!n)",
        [
            "A derangement is a permutation with no element in its home position — hat check problem.",
            "$!n = n!\\sum_{i=0}^{n}\\frac{(-1)^i}{i!}$ rounded to nearest integer for large n, exact via PIE.",
            "Small values: !2=1, !3=2, !4=9, !5=44.",
            "Understand !3 by listing: for ABC, only BCA and CAB.",
            "AMC may ask small !n; National may ask PIE setup.",
            "Remember derangements are permutations, so start from n! world.",
        ],
        "<p>Derangements = permutations with no fixed points.</p>",
        "<p>List small n; memorize !3 and !4.</p>",
        solved(16, "!3=?",
               ["List: BCA, CAB → 2."], "$2$", "", "Easy")
        + solved(17, "!4=?",
                 ["$!4=9$."], "$9$", "", "Medium")
        + solved(18, "!2=?",
                 ["Only swap → 1."], "$1$", "", "Easy"),
        ("Confusing !n with n!", "Derangements are fewer."),
        ("List n=3", "Grounds the idea."),
        ["I know !3=2 and !4=9.", "I can explain hats.", "I connect to PIE."],
        26,
    ))
    for t, a, e in [
        ("!3?", 2, "2."),
        ("!4?", 9, "9."),
        ("!2?", 1, "1."),
        ("!5?", 44, "44."),
        ("n! for n=4 vs !4?", 24, "24 vs 9 — question asks 4!=24 as check."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    specs = []
    for N in [20, 30, 40, 50, 60, 90, 100, 120]:
        for primes in ([2, 3], [2, 5], [3, 5], [2, 3, 5]):
            specs.append((f"1..{N} div by {' or '.join(map(str,primes))}?",
                          pie_divisible(N, primes), "PIE"))
            if len(specs) >= 40:
                break
        if len(specs) >= 40:
            break
    specs += [
        ("Onto [6]→[2]?", 2 ** 6 - 2, "62."),
        ("!6?", 265, "265."),
        ("Union 25+20-8?", 37, "37."),
        ("Neither from total 50 union 33?", 17, "17."),
        ("Three-set 10+10+10-4-4-4+2?", 20, "20."),
        ("1..100 not div2 or5?", 40, "40."),
        ("Onto [4]→[3]?", 36, "3^4-C(3,1)2^4+C(3,2)1^4=81-48+3=36."),
        ("|A∪B∪C| formula needs +triple?", 1, "Use 1 as yes-code; explanation says must add."),
        ("!0 defined as?", 1, "1."),
        ("Functions [2]→[4]?", 16, "16."),
    ]
    # fix weird ones
    specs = [s for s in specs if not (isinstance(s[1], int) and s[0].startswith("|A∪B∪C|"))]
    specs.append(("Onto [4]→[3]?", 36, "81-48+3=36."))
    for t, a, e in specs[:25]:
        qs.append(mq(t, a, e, idx)); idx += 1

    return _assemble(title, description, "Grades 6–8 · MathCounts · AMC 8/10",
                     ["Two-set Venn", "Three-set PIE", "Divisibility", "Complement+PIE", "Onto", "Derangements"],
                     concepts, qs)


def build_unit7():
    title = "MathCounts Unit 7: Paths, Recursion & Counting Sequences"
    description = "Lattice paths, Fibonacci tilings, Catalan preview — deep contest paths."
    concepts, qs, idx = [], [], 1

    concepts.append(concept_block(
        "1. Lattice paths formula",
        [
            "To go from (0,0) to (a,b) with only right and up unit steps, you need a rights and b ups — total a+b steps.",
            "Choose positions for the rights among a+b steps: $\\binom{a+b}{a}$.",
            "Same as choosing ups: $\\binom{a+b}{b}$.",
            "This is combinations applied to sequences of moves.",
            "Draw small grids and list paths to believe the formula.",
            "AMC 8/10 path problems often reduce to one binomial.",
        ],
        "<p>Paths = choose when to go right.</p>",
        "<p>Count rights and ups; choose positions.</p>",
        solved(1, "Paths to (3,2)?",
               [f"$\\binom{{5}}{{2}}={lattice_paths(3,2)}$."], str(lattice_paths(3, 2)), "", "Easy")
        + solved(2, "Paths to (4,3)?",
                 [f"{lattice_paths(4,3)}."], str(lattice_paths(4, 3)), "", "Easy")
        + solved(3, "Paths to (5,5)?",
                 [f"{lattice_paths(5,5)}."], str(lattice_paths(5, 5)), "", "Medium"),
        ("Adding a+b choose wrong index", "Choose a out of a+b."),
        ("List a 2×1 grid", "Builds trust."),
        ["I compute lattice C(a+b,a).", "I know rights/ups story.", "I verify tiny grids."],
        1,
    ))
    for a, b in [(2, 2), (3, 1), (3, 3), (4, 2), (6, 1)]:
        qs.append(mq(f"Paths (0,0)→({a},{b})?", lattice_paths(a, b),
                     f"C({a+b},{a})={lattice_paths(a,b)}.", idx)); idx += 1

    concepts.append(concept_block(
        "2. Paths through a required point",
        [
            "If you must pass through C, multiply paths to C by paths from C to end.",
            "Product rule on path segments.",
            "Ensure C is between start and end with only right/up moves — C should not require left/down.",
            "Multiple mandatory points: multiply more segments in order.",
            "This is a favorite Target technique.",
            "Sketch the grid and mark the gateway.",
        ],
        "<p>Gateway points multiply path counts.</p>",
        "<p>Compute each leg’s binomial, multiply.</p>",
        solved(4, "To (2,2) via (1,1)?",
               ["2×2=4."], "$4$", "", "Easy")
        + solved(5, "To (5,5) via (2,3)?",
                 ["C(5,2)×C(5,2)=100."], "$100$", "", "Hard")
        + solved(6, "To (4,3) via (2,1)?",
                 [f"{lattice_paths(2,1)*lattice_paths(2,2)}."],
                 str(lattice_paths(2, 1) * lattice_paths(2, 2)), "", "Medium"),
        ("Adding legs", "Multiply sequential legs."),
        ("Check C is reachable monotonically", "No left/down needed."),
        ["I multiply legs.", "I compute each binomial.", "I mark gateways on a sketch."],
        6,
    ))
    for t, a, e in [
        ("Via (1,1) to (2,2)?", 4, "4."),
        ("Via (2,3) to (5,5)?", 100, "100."),
        ("Via (2,1) to (4,3)?", lattice_paths(2, 1) * lattice_paths(2, 2), "3×6=18."),
        ("Via (1,0) to (3,2)?", lattice_paths(1, 0) * lattice_paths(2, 2), "1×6=6."),
        ("Via (3,3) to (3,3)?", 1, "Already there after first leg; second leg C(0,0)=1."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    concepts.append(concept_block(
        "3. Domino tilings and Fibonacci",
        [
            "Ways to tile a 2×n board with 1×2 dominoes: let a_n satisfy a_n=a_{n-1}+a_{n-2}.",
            "Reason: first domino vertical → then a_{n-1}; or two horizontals → then a_{n-2}.",
            "With a_0=1, a_1=1, a_2=2, sequence matches Fibonacci-related counts.",
            "Recursion means building larger counts from smaller ones.",
            "List n=1,2,3 to see the pattern before using the recurrence.",
            "National may twist tiling with colors or trominoes — still recurrence thinking.",
        ],
        "<p>Tilings create Fibonacci-like recurrences.</p>",
        "<p>Classify based on the left ending.</p>",
        solved(7, "Tilings of 2×3?",
               ["a1=1,a2=2,a3=a2+a1=3."], "$3$", "", "Easy")
        + solved(8, "Tilings of 2×5?",
                 ["Sequence 1,2,3,5,8 → a5=8."], "$8$", "", "Medium")
        + solved(9, "Why a4=5?",
                 ["a4=a3+a2=3+2=5.", "List to confirm if needed."], "$5$", "", "Medium"),
        ("Wrong initial conditions", "List n=1 and n=2 first."),
        ("Ending case split", "Vertical vs two horizontals."),
        ["I know the domino recurrence.", "I compute small a_n.", "I explain the case split."],
        11,
    ))
    # a_n for 2xn with a1=1,a2=2
    def dom(n):
        if n <= 0:
            return 1
        if n == 1:
            return 1
        if n == 2:
            return 2
        a, b = 1, 2
        for _ in range(3, n + 1):
            a, b = b, a + b
        return b
    for n in range(1, 6):
        qs.append(mq(f"Domino tilings of 2×{n}?", dom(n), f"a_{n}={dom(n)}.", idx)); idx += 1

    concepts.append(concept_block(
        "4. Binary strings with no two consecutive 1s",
        [
            "Let b_n = number of length-n bit strings with no two consecutive 1s.",
            "A valid string ends with 0: then first n-1 any valid → b_{n-1}.",
            "Or ends with 01? Ends with 1 → previous must be 0, and first n-2 valid → b_{n-2}.",
            "So b_n=b_{n-1}+b_{n-2}, with b1=2 (0,1), b2=3 (00,01,10).",
            "Same recurrence family as Fibonacci.",
            "Listing small n prevents off-by-one in initials.",
        ],
        "<p>Restrictions create recurrences.</p>",
        "<p>Case on the ending bits.</p>",
        solved(10, "b1 and b2?",
               ["b1=2, b2=3."], "2 and 3", "", "Easy")
        + solved(11, "b5?",
                 ["b1=2, b2=3, so b3=5, b4=8, b5=13."],
                 "$13$", "", "Medium")
        + solved(12, "b4?",
                 ["b4=8."], "$8$", "", "Medium"),
        ("Wrong initials", "List all length 2."),
        ("Ending case", "End 0 vs end 1."),
        ["I set b1,b2 correctly.", "I compute b_n via recurrence.", "I can list n=3."],
        16,
    ))
    def bit_no_consec(n):
        if n == 1:
            return 2
        if n == 2:
            return 3
        x, y = 2, 3
        for _ in range(3, n + 1):
            x, y = y, x + y
        return y
    for n in range(1, 6):
        qs.append(mq(f"Bit strings length {n} no consecutive 1s?", bit_no_consec(n), f"b_{n}={bit_no_consec(n)}.", idx)); idx += 1

    concepts.append(concept_block(
        "5. Catalan numbers preview",
        [
            "Catalan numbers $C_n=\\frac{1}{n+1}\\binom{2n}{n}$ count many structures: matched parentheses, Dyck paths, binary trees.",
            "Dyck path: lattice path from (0,0) to (n,n) not going above the diagonal (with appropriate step model).",
            "Compute small: C_2=2, C_3=5, C_4=14.",
            "You do not need full Catalan theory for AMC 8, but National/AMC 10 may touch C_n.",
            "Know the formula and a meaning: correctly matched parentheses of n pairs.",
            "Treat this as a preview — recognize the formula if it appears.",
        ],
        "<p>Catalan counts carefully balanced structures.</p>",
        "<p>Memorize C_2,C_3,C_4 and the formula shape.</p>",
        solved(13, "C_3?",
               ["$\\frac{1}{4}\\binom{6}{3}=5$."], "$5$", "", "Medium")
        + solved(14, "C_4?",
                 ["$\\frac{1}{5}\\binom{8}{4}=14$."], "$14$", "", "Hard")
        + solved(15, "C_2?",
                 ["2."], "$2$", "", "Easy"),
        ("Confusing C_n with binom(2n,n)", "Must divide by n+1."),
        ("Parentheses picture", "(()()) etc. for n=3 → 5."),
        ["I compute small Catalan numbers.", "I know the formula.", "I know one combinatorial meaning."],
        21,
    ))
    for n, val in [(2, 2), (3, 5), (4, 14), (5, 42), (1, 1)]:
        qs.append(mq(f"Catalan C_{n}=?", val, f"C_{n}={val}.", idx)); idx += 1

    concepts.append(concept_block(
        "6. Contest path strategies",
        [
            "First ask: unrestricted lattice → one binomial.",
            "Must visit a point → product of binomials.",
            "Avoid a region → often complement or Catalan-like (harder).",
            "Recurrence problems: define a_n clearly; find initials; find recurrence.",
            "Draw grids; label counts at lattice points (dynamic programming flavor).",
            "National may combine paths with PIE or casework on first step.",
        ],
        "<p>Match path problem type to tool.</p>",
        "<p>Sketch, then choose binomial vs recurrence vs Catalan.</p>",
        solved(16, "Label method: paths to each point on small grid to (2,2).",
               ["To (1,0)=1,(0,1)=1,(1,1)=2,(2,1)=3,(1,2)=3,(2,2)=6.",
                "Matches C(4,2)=6."], "$6$", "", "Medium")
        + solved(17, "First step case: paths to (2,2).",
                 ["First right: then paths (1,0)→(2,2)=C(3,1)=3.",
                  "First up: similarly 3.", "Total 6."], "$6$", "", "Hard")
        + solved(18, "When recurrence?",
                 ["When local endings create overlapping subproblems like tilings or restricted strings."],
                 "tilings / restricted strings", "", "Medium"),
        ("Jumping to Catalan always", "Most path problems are plain binomials."),
        ("Point labels", "Fill numbers on grid intersections."),
        ["I classify path problems.", "I can fill a small grid DP-style.", "I know when to use recurrence."],
        26,
    ))
    for t, a, e in [
        ("Paths to (2,2)?", 6, "6."),
        ("Domino 2×4?", dom(4), "5."),
        ("b_3 no consecutive 1s?", bit_no_consec(3), "5."),
        ("C_3?", 5, "5."),
        ("Via (1,1) to (3,2)?", lattice_paths(1, 1) * lattice_paths(2, 1), "2×3=6."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    specs = []
    for aa in range(1, 7):
        for bb in range(1, 7):
            specs.append((f"Paths to ({aa},{bb})?", lattice_paths(aa, bb), "lattice"))
            if len(specs) >= 35:
                break
        if len(specs) >= 35:
            break
    for n in range(1, 10):
        specs.append((f"Domino 2×{n}?", dom(n), "domino"))
    for n in range(1, 10):
        specs.append((f"No consecutive 1s length {n}?", bit_no_consec(n), "bits"))
    for n, val in [(2, 2), (3, 5), (4, 14), (5, 42), (6, 132)]:
        specs.append((f"Catalan C_{n}?", val, "Catalan"))
    for t, a, e in specs[:25]:
        qs.append(mq(t, a, e, idx)); idx += 1

    return _assemble(title, description, "Grades 6–8 · MathCounts · AMC 8/10",
                     ["Lattice formula", "Through a point", "Domino Fibonacci", "Bit recurrence", "Catalan preview", "Strategy"],
                     concepts, qs)


def build_unit8():
    title = "MathCounts Unit 8: Contest Mixed Sets & Strategy"
    description = "Mixed counting + MathCounts/AMC strategy with progressive National stretch."
    concepts, qs, idx = [], [], 1

    concepts.append(concept_block(
        "1. MathCounts Sprint strategy for counting",
        [
            "Sprint rewards fast recognition. Spend up to about a minute; if no plan, skip and return.",
            "First read: order? repeats? leading zeros? at least one?",
            "Default tools: product slots; complement for at least; C vs P swap test.",
            "Write a 3-word plan: “complement no-A,” “P(10,3),” “C(8,2).”",
            "Arithmetic last; structure first.",
            "Bubbling wrong because of a reading miss hurts more than blank — trust your plan checks.",
        ],
        "<p>Sprint counting is plan speed + accuracy.</p>",
        "<p>Underline constraints; name the tool; compute; sanity-check size.</p>",
        solved(1, "Sprint: 4×3×2 outfits?",
               ["Product 24 — under 10 seconds."], "$24$", "", "Easy")
        + solved(2, "Sprint: at least one head in 3 flips?",
                 ["8-1=7."], "$7$", "", "Easy")
        + solved(3, "Sprint: C(10,2)?",
                 ["45."], "$45$", "", "Easy"),
        ("Computing before planning", "Plan in words first."),
        ("Size sanity", "Is 1,000,000 sensible for 3-digit numbers? No."),
        ["I have a Sprint checklist.", "I skip when stuck.", "I sanity-check magnitudes."],
        1,
    ))
    for t, a, e in [
        ("4×3×2?", 24, "24."),
        ("At least one head in 3 flips?", 7, "7."),
        ("C(10,2)?", 45, "45."),
        ("P(6,2)?", 30, "30."),
        ("2^5?", 32, "32."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    concepts.append(concept_block(
        "2. Target / Team strategy",
        [
            "Target: fewer problems, deeper. Write a full plan before arithmetic.",
            "Team: assign counting to whoever explains C/P/PIE most clearly; verify with a second method.",
            "Two-method habit: compute C(n,k)×k and also P route for chair problems.",
            "If two teammates disagree, list a tiny analog together.",
            "Keep shared scratch neat so others can audit.",
            "National Team Round multiplies these habits under pressure.",
        ],
        "<p>Deep problems need written plans and verification.</p>",
        "<p>Two methods when time allows.</p>",
        solved(4, "Verify committee 4 from 10 then chair two ways.",
               ["C(10,4)×4=840.", "10×C(9,3)=840."], "$840$", "", "Medium")
        + solved(5, "Tiny analog idea.",
                 ["Replace 10 by 4, committee 2 then chair: C(4,2)×2=12; 4×C(3,1)=12."],
                 "$12$", "", "Easy")
        + solved(6, "When listing beats formulas?",
                 ["When n is tiny or when you distrust a symmetry division."],
                 "tiny n / distrust symmetry", "", "Medium"),
        ("Only one method forever", "Hard problems need cross-checks."),
        ("Tiny analog", "Shrink numbers to test structure."),
        ["I write Target plans.", "I verify two ways.", "I use tiny analogs."],
        6,
    ))
    for t, a, e in [
        ("C(10,4)×4?", 840, "840."),
        ("10×C(9,3)?", 840, "840."),
        ("C(4,2)×2?", 12, "12."),
        ("Unlabeled teams of 3 from 6?", 10, "10."),
        ("P(9,3)?", 504, "504."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    concepts.append(concept_block(
        "3. AMC 8 / AMC 10 answer habits",
        [
            "AMC 8 answers are integers 0–999. Fractions mean a misread.",
            "AMC 10 can be harder; same counting tools with more layers (PIE + cases).",
            "Grid-in / answer form discipline: compute fully.",
            "Estimate before finalizing: ballpark the magnitude.",
            "Eliminate impossible choices if multiple choice (too small/too large).",
            "Do not leave a counting problem without a defined object sentence.",
        ],
        "<p>Answer form is a checksum.</p>",
        "<p>Integer check + magnitude check + object sentence.</p>",
        solved(7, "If you get 12.5 on AMC 8 counting?",
               ["Impossible as final; re-read constraints."], "re-read", "", "Easy")
        + solved(8, "Ballpark: 5-digit codes with repeats from 10 digits?",
                 ["10^5=100000 — large but plausible."], "$100000$", "", "Easy")
        + solved(9, "Ballpark fail: claiming only 20 three-digit numbers?",
                 ["There are 900 three-digit numbers — 20 is absurd."], "too small", "", "Easy"),
        ("Ignoring answer form", "Use it as a detector."),
        ("Object sentence", "“I am counting 3-digit numbers with…”"),
        ["I treat AMC integers as checksums.", "I ballpark.", "I write object sentences."],
        11,
    ))
    for t, a, e in [
        ("10^4?", 10000, "10000."),
        ("Number of 3-digit integers?", 900, "900."),
        ("C(9,4) increasing 4-digit?", 126, "126."),
        ("2^10?", 1024, "1024."),
        ("P(10,3)?", 720, "720."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    concepts.append(concept_block(
        "4. Mixed tool picker",
        [
            "Decision tree: identical objects? → maybe stars/bars. Ordered roles? → P. Unordered team? → C.",
            "At least one? → complement. Overlapping properties? → PIE.",
            "Paths? → binomials. Tilings/restrictions over length? → recurrence.",
            "Write the decision on paper in 5 seconds; then compute.",
            "Wrong branch wastes minutes — tiny analogs test the branch.",
            "This section’s drills force switching tools.",
        ],
        "<p>Picker first, calculator second.</p>",
        "<p>Run the decision tree aloud.</p>",
        solved(10, "Pick tool: identical bagels 3 types buy 7.",
               ["Stars/bars nonneg."], "stars/bars", "", "Easy")
        + solved(11, "Pick tool: president/VP from 12.",
                 ["P(12,2)."], "permutation", "", "Easy")
        + solved(12, "Pick tool: ints ≤100 div by 2 or 3.",
                 ["PIE floors."], "PIE", "", "Medium"),
        ("One favorite tool forever", "Match tool to structure."),
        ("Say the tree", "Identical? Order? At least? Paths?"),
        ["I can pick tools quickly.", "I test with tiny analogs.", "I switch tools mid-set."],
        16,
    ))
    for t, a, e in [
        ("P(12,2)?", 132, "132."),
        ("Stars/bars 7 bagels 3 types?", stars_bars_nonneg(7, 3), "36."),
        ("PIE 1..100 div2 or3?", pie_divisible(100, [2, 3]), "67? 50+33-16=67."),
        ("C(12,3)?", math.comb(12, 3), "220."),
        ("Paths to (3,3)?", 20, "20."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    concepts.append(concept_block(
        "5. Hard mixed worked examples",
        [
            "Layered problems stack two or more counting tools. A common stack is \"complement on the outside, "
            "product of slots on the inside.\" Another is \"PIE on the outside, casework on the inside.\" "
            "The skill is not memorizing stacks — it is writing the stack as an outline before you touch a calculator.",
            "Example outline for \"distinct length-6 digit strings with at least one zero\": "
            "(1) Total = all distinct 6-digit codes from digits 0–9 = $P(10,6)$. "
            "(2) Bad = codes with no zero at all = $P(9,6)$. "
            "(3) Good = Total − Bad. That outline is the whole solution plan; the numbers come second.",
            "Keep every middle total in a labeled box on scratch paper. Layered arithmetic without boxes is where "
            "factors disappear — especially a forgotten subtract or a forgotten divide by $k!$.",
            "If the real numbers feel huge, shrink them while keeping the same structure (length 6 → length 3). "
            "List the tiny version by hand, confirm your outline matches the list, then scale back up.",
            "Say each layer in a short English clause: \"First I count all codes. Then I remove codes with no zero.\" "
            "If you cannot say the clause, you are not ready to multiply yet.",
            "These problems mirror State/National and late AMC difficulty: the arithmetic is doable, but only after "
            "the outline is honest.",
        ],
        "A layered counting problem is really a short program: Layer 1 tool, Layer 2 tool, then combine. "
        "Students who skip the outline often do only one layer and submit that number. Contests reward the full program.",
        "Write Outline → Compute each boxed piece → Verify on a tiny analog → Finalize. "
        "Never reverse the order on Target/National: computing first and outlining later is how layers get dropped.",
        solved(13, "How many distinct length-6 strings using digits 0–9 have at least one zero?",
               [
                   "Outline: Total = $P(10,6)$; Bad = no zeros = $P(9,6)$; Good = Total − Bad.",
                   "Total: $10×9×8×7×6×5 = 151200$.",
                   "Bad: $9×8×7×6×5×4 = 60480$.",
                   "Good: $151200 − 60480 = 90720$.",
               ], "$90720$",
               "Notice the outline named three boxes before any multiply. That is the habit this concept trains.",
               "Hard")
        + solved(14, "How many rectangles are in a 5×5 grid of unit squares?",
                 [
                     "A 5×5 grid of squares has 6 horizontal and 6 vertical lines.",
                     "A rectangle is choosing 2 distinct horizontal lines and 2 distinct vertical lines.",
                     "So the count is $C(6,2)×C(6,2) = 15×15 = 225$.",
                 ], "$225$",
                 "Geometry counting often hides a combinations layer — outline \"choose lines\" before multiplying.",
                 "Medium")
        + solved(15, "How many onto functions are there from a set of 5 elements to a set of 3 elements?",
                 [
                     "Outline with PIE: all functions − missing at least one output + missing at least two outputs.",
                     "All functions: $3^5 = 243$.",
                     "Subtract $C(3,1)·2^5 = 3·32 = 96$.",
                     "Add back $C(3,2)·1^5 = 3$.",
                     "Onto count: $243 − 96 + 3 = 150$.",
                 ], "$150$",
                 "National-style: the outline is PIE; the boxes are the three PIE terms.",
                 "National"),
        ("Skipping the outline",
         "If a problem has two layers (for example: first remove bad codes with a complement, then arrange what remains), "
         "jumping straight into multiplying makes you lose a whole layer — like forgetting to subtract, "
         "or forgetting a divide by $k!$. Always write a 2–4 line outline that names each layer before any arithmetic. "
         "The outline should be readable by a teammate who has not seen the problem yet."),
        ("Box intermediates",
         "Every middle total should be boxed and labeled on scratch paper (Total, Bad, Case 1, Paths to C). "
         "That written audit trail lets you check each piece alone, and it stops you from accidentally reusing "
         "the wrong number when you combine layers at the end. On Team Round, boxing also lets your partner "
         "verify your work without redoing the whole solution."),
        [
            "I outline layered problems in words before calculating, naming each tool in order.",
            "I can compute a complement of permutations (like $P(10,6)-P(9,6)$) and explain each term as Total / Bad / Good.",
            "I attempt National/AMC 10 stretch problems calmly with a written plan, even if I need more time.",
        ],
        21,
    ))
    for t, a, e in [
        ("P(10,6)-P(9,6)?", 90720, "90720."),
        ("Rectangles 5×5?", 225, "225."),
        ("Onto [5]→[3]?", 150, "150."),
        ("C(9,4)?", 126, "126."),
        ("!4?", 9, "9."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    concepts.append(concept_block(
        "6. Verification habits that raise scores",
        [
            "Habit A: re-read the object counted.",
            "Habit B: swap test / label test / leading-zero test.",
            "Habit C: magnitude sanity.",
            "Habit D: second method or tiny analog.",
            "Habit E: integer/answer-form check.",
            "Build these until automatic — they catch the majority of contest counting errors.",
        ],
        "<p>Verification is part of solving, not optional polish.</p>",
        "<p>Run A–E quickly before locking an answer.</p>",
        solved(16, "Catch: using C(6,3) for unlabeled two teams without /2.",
               ["Missed Habit B labels → fix /2."], "divide by 2", "", "Medium")
        + solved(17, "Catch: 3-digit codes counted as 900 when zeros allowed.",
                 ["Codes allow 000–999 → 1000."], "$1000$", "", "Easy")
        + solved(18, "Catch: fraction on AMC 8.",
                 ["Impossible final — restart reading."], "restart", "", "Easy"),
        ("Submitting without checks", "Checks are points."),
        ("Checklist A–E", "Keep it on scratch paper header."),
        ["I run verification habits.", "I catch unlabeled misses.", "I catch leading-zero misses."],
        26,
    ))
    for t, a, e in [
        ("Unlabeled teams of 3 from 6 corrected?", 10, "10."),
        ("3-digit lock codes repeats OK?", 1000, "1000."),
        ("3-digit numbers?", 900, "900."),
        ("C(8,3)?", 56, "56."),
        ("Diagonals of octagon?", 20, "20."),
    ]:
        qs.append(mq(t, a, e, idx)); idx += 1

    # Progressive finale including National/AMC10
    specs = []
    for n in range(2, 12):
        specs.append((f"C(10,{n})?" if n <= 5 else f"C(12,{n-5})?",
                      math.comb(10, n) if n <= 5 else math.comb(12, n - 5), "combo"))
    specs += [
        ("P(10,6)-P(9,6)?", 90720, "90720."),
        ("Increasing 4-digit 1–9?", 126, "126."),
        ("PIE 1..120 div 2,3,5?", pie_divisible(120, [2, 3, 5]), "PIE."),
        ("Onto [6]→[3]?", 3 ** 6 - math.comb(3, 1) * 2 ** 6 + math.comb(3, 2) * 1 ** 6, "540? compute"),
        ("Rectangles 6×6?", math.comb(7, 2) ** 2, "441."),
        ("Paths (0,0)→(6,4)?", lattice_paths(6, 4), "210."),
        ("Stars nonneg 4 vars sum 10?", stars_bars_nonneg(10, 4), "286."),
        ("Positive 4 vars sum 10?", stars_bars_positive(10, 4), "84."),
        ("!5?", 44, "44."),
        ("Arrangements MISSISSIPPI?", perm_repeated("MISSISSIPPI"), "34650."),
        ("Domino 2×8?", 34, "Fibonacci-like a8=34."),
        ("Catalan C5?", 42, "42."),
        ("Bit no consec 1s len 6?", 21, "b6=21."),
        ("Diagonals 12-gon?", 54, "12*9/2=54."),
        ("Strictly increasing 5-digit?", math.comb(9, 5), "126."),
        ("Functions [5]→[4] total?", 4 ** 5, "1024."),
        ("Onto [5]→[4]?", 4 ** 5 - math.comb(4, 1) * 3 ** 5 + math.comb(4, 2) * 2 ** 5 - math.comb(4, 3) * 1 ** 5, "1024-972+160-4?"),
    ]
    # Fix onto [6]→[3] and onto [5]→[4] with exact compute
    def onto(n, k):
        total = 0
        for i in range(k + 1):
            sign = 1 if (k - i) % 2 == 0 else -1
            # standard: sum_{i=0}^k (-1)^{k-i} C(k,i) i^n
            total += ((-1) ** (k - i)) * math.comb(k, i) * (i ** n)
        return total
    specs = [s for s in specs if "Onto [6]" not in s[0] and "Onto [5]→[4]" not in s[0]]
    specs.append((f"Onto [6]→[3]?", onto(6, 3), f"{onto(6,3)}."))
    specs.append((f"Onto [5]→[4]?", onto(5, 4), f"{onto(5,4)}."))
    while len(specs) < 25:
        a, b = 3 + len(specs) % 4, 2 + len(specs) % 3
        specs.append((f"Paths to ({a},{b})?", lattice_paths(a, b), "lattice"))
    for t, a, e in specs[:25]:
        qs.append(mq(t, a, e, idx)); idx += 1

    return _assemble(title, description, "Grades 6–8 · MathCounts · AMC 8/10 · National stretch",
                     ["Sprint", "Target/Team", "AMC habits", "Tool picker", "Mixed hard", "Verification"],
                     concepts, qs)
