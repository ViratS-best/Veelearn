#!/usr/bin/env python3
"""Units 2–8: deep lessons + 55 quizzes each (6×5 concept drills + 25 finale)."""

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
    near_int,
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
        qs.append(mq(f"Check computation #{i}: what is $3\\times4$?", 12, "Independent choices: $3\\times4=12$.", i))
        i += 1
    return renumber(qs[:55])


def _finale_progressive(start_specs):
    """Build up to 25 finale questions from list of (text, ans, expl)."""
    out = []
    for text, ans, expl in start_specs:
        if isinstance(ans, int) or (isinstance(ans, str) and str(ans).lstrip("-").isdigit()):
            out.append(mq(text, ans, expl, 0))
        else:
            out.append(make_question(text, ans, near_int(hash(text) % 50 + 3)[:3], expl, 0)
                       if False else make_question(text, str(ans), ["Option A", "Option B", "Option C"], expl, 0))
    return out


def _assemble(title, description, audience, roadmap, concepts, questions):
    """concepts: list of kwargs for concept_block in order with quiz_start 1,6,11,16,21,26."""
    body = "".join(concepts)
    content = unit_shell(title, audience, roadmap, body, practice_slots(31, 25))
    return title, description, content, _need55(questions)


# ========================= UNIT 2 =========================

def build_unit2():
    title = "MathCounts Unit 2: Permutations & Arrangements"
    description = "Factorials, P(n,k), identical letters, circles — deep contest training for grades 6–8."
    concepts = []
    qs = []
    idx = 1

    concepts.append(concept_block(
        "1. Factorials — arranging n different people in a line",
        [
            "A factorial is a short way to write a long product. The symbol $n!$ means $n\\times(n-1)\\times\\cdots\\times1$. "
            "For example $5!=5\\times4\\times3\\times2\\times1=120$.",
            "Why does arranging $n$ different people use $n!$? Put them in a line of $n$ chairs. "
            "The first chair has $n$ choices, the next has $n-1$ left, then $n-2$, and so on, down to $1$. Multiply those stage counts.",
            "Factorials grow quickly. $10!=3{,}628{,}800$. That is why contest answers sometimes look huge — and why you should estimate whether your answer size makes sense.",
            "We define $0!=1$. That is not a random rule; it makes formulas like $\\binom{n}{0}=1$ work cleanly. Think of it as “one way to arrange nothing.”",
            "On contests, $n!$ often appears when every object is distinct and every seat is ordered (a line, a ranked list, a password with all distinct symbols from a set of size n used fully).",
            "If some objects are identical, plain $n!$ overcounts. You will learn to divide in a later section of this unit.",
        ],
        "<p>Factorials are the backbone of ordered counting.</p>",
        "<p>Say: “first chair n ways, next n-1…” then multiply. That story is $n!$.</p>",
        solved(1, "How many ways to line up 4 different students?",
               ["Chair 1: 4 choices.", "Chair 2: 3.", "Chair 3: 2.", "Chair 4: 1.",
                "Product $4!=24$.", "List for 3 students to feel it: ABC,ACB,BAC,BCA,CAB,CBA → $3!=6$."],
               "$24$", "", "Easy")
        + solved(2, "Compute $6!$.",
                 ["$6\\times5=30$.", "$30\\times4=120$.", "$120\\times3=360$.", "$360\\times2=720$.", "$720\\times1=720$."],
                 "$720$", "", "Easy")
        + solved(3, "How many ways to arrange the letters in MATH (all distinct)?",
                 ["4 distinct letters.", "Arrangements: $4!=24$.",
                  "If the problem said “how many 4-letter words using each letter once,” same answer."],
                 "$24$", "", "Medium"),
        ("Using n! when letters repeat", "If a word has repeated letters, plain n! counts look-alike arrangements as different."),
        ("Build from chairs", "Always narrate chairs/slots before writing n!."),
        ["I can compute small factorials by hand.", "I explain why n people line up in n! ways.", "I know 0!=1."],
        1,
    ))
    for text, ans, expl in [
        ("Compute $5!$.", 120, "$5!=120$."),
        ("Arrange 3 distinct books on a shelf?", 6, "$3!=6$."),
        ("Arrange 7 distinct people in a line?", 5040, "$7!=5040$."),
        ("What is $0!$?", 1, "By definition $0!=1$."),
        ("Arrange letters of CODE (all distinct)?", 24, "$4!=24$."),
    ]:
        qs.append(mq(text, ans, expl, idx)); idx += 1

    concepts.append(concept_block(
        "2. Permutations P(n,k) — ordered selections",
        [
            "Sometimes you do not arrange everyone — you only choose $k$ people out of $n$ and put them in order "
            "(president, VP, secretary). That count is $P(n,k)=\\frac{n!}{(n-k)!}=n(n-1)\\cdots(n-k+1)$.",
            "Plain English: first role has $n$ choices, second has $n-1$, … for $k$ roles. Multiply those $k$ numbers.",
            "Order matters here because “A as president and B as VP” is different from “B as president and A as VP.”",
            "If the problem only needs an unordered team with no titles, do NOT use $P(n,k)$ — use combinations $\\binom{n}{k}$ (Unit 3).",
            "A quick test: Can I swap two chosen people and get a different outcome that the problem counts separately? If yes, think permutations.",
            "AMC 8 loves P(n,k) disguised as “assign different prizes” or “form a password with distinct digits.”",
        ],
        "<p>P(n,k) is the product rule with shrinking options for k slots.</p>",
        "<p>Ask: are there labeled roles or an ordered list? If yes, P(n,k).</p>",
        solved(4, "From 10 students, choose president, VP, secretary (all different)?",
               ["President: 10.", "VP: 9.", "Secretary: 8.", "$P(10,3)=720$."],
               "$720$", "", "Easy")
        + solved(5, "How many injective (one-to-one) functions from a 3-set to a 7-set?",
                 ["Image of first element: 7 choices.", "Second: 6.", "Third: 5.",
                  "$P(7,3)=210$.", "Injective means no two inputs share an output — like distinct assignments."],
                 "$210$", "", "Hard")
        + solved(6, "Distinct 4-digit codes from digits 0–9 with no repeats (codes, zeros OK anywhere)?",
                 ["$P(10,4)=10\\times9\\times8\\times7=5040$."],
                 "$5040$", "", "Medium"),
        ("Using C(n,k) for titled roles", "Titles make order matter — use P."),
        ("Say the roles", "Name role1/role2 to force the permutation story."),
        ["I compute P(n,k) as a falling product.", "I distinguish P from C.", "I use P for distinct-digit codes."],
        6,
    ))
    for text, ans, expl in [
        ("Compute $P(8,3)$.", 336, "$8\\times7\\times6=336$."),
        ("Prizes gold/silver/bronze among 9 runners?", 504, "$P(9,3)=504$."),
        ("$P(6,2)$=?", 30, "$6\\times5=30$."),
        ("$P(5,5)$=?", 120, "$5!=120$."),
        ("Ordered codes length 2 from 10 digits no repeat?", 90, "$P(10,2)=90$."),
    ]:
        qs.append(mq(text, ans, expl, idx)); idx += 1

    concepts.append(concept_block(
        "3. Identical letters — divide out the clones",
        [
            "If you arrange the letters of BALLOON, swapping the two L’s does not create a new visible word. "
            "Plain $7!$ pretends those swaps are different, so it overcounts.",
            "Fix: divide by the factorial of each repeated letter’s count. For BALLOON: $\\dfrac{7!}{2!\\,2!}$ because L repeats twice and O repeats twice.",
            "General rule: for a word with letter frequencies $n_1,n_2,\\ldots$, arrangements $=\\dfrac{n!}{n_1! n_2! \\cdots}$.",
            "Why divide by $2!$ for a double letter? The two identical letters can be swapped in $2!$ ways inside any arrangement, and those swaps look the same.",
            "MISSISSIPPI is a classic: $\\dfrac{11!}{4!4!2!}$ for I×4, S×4, P×2.",
            "This idea returns in combinations: dividing by $k!$ turns ordered lists into unordered teams.",
        ],
        "<p>Identical objects force you to remove fake distinctions.</p>",
        "<p>Count total letters, list repeat frequencies, write n! over those factorials.</p>",
        solved(7, "Distinct arrangements of BALL?",
               ["Letters B,A,L,L → 4 letters, L×2.", "$\\frac{4!}{2!}=12$."],
               "$12$", "", "Easy")
        + solved(8, "Distinct arrangements of BALLOON?",
                 ["7 letters; L×2, O×2.", "$\\frac{7!}{2!2!}=1260$."],
                 "$1260$", "", "Medium")
        + solved(9, "Distinct arrangements of MISSISSIPPI?",
                 ["11 letters; I×4, S×4, P×2, M×1.",
                  f"$\\frac{{11!}}{{4!4!2!}}={perm_repeated('MISSISSIPPI')}$."],
                 str(perm_repeated("MISSISSIPPI")), "", "Hard"),
        ("Forgetting to divide", "If two letters are the same, n! is too big."),
        ("Frequency table", "Write a tally of each letter before dividing."),
        ["I can build the divide-by-factorials formula.", "I handle two different repeated letters.", "I know MISSISSIPPI’s count."],
        11,
    ))
    for text, ans, expl in [
        ("Arrangements of LEVEL?", 30, "$\\frac{5!}{2!2!}=30$."),
        ("Arrangements of BOOK?", 12, "$\\frac{4!}{2!}=12$."),
        ("Arrangements of AAA?", 1, "All identical → only 1 distinct arrangement."),
        ("Arrangements of SUCCESS?", 420, f"{perm_repeated('SUCCESS')}."),
        ("Arrangements of TOOTH?", 30, f"{perm_repeated('TOOTH')}."),
    ]:
        qs.append(mq(text, ans, expl, idx)); idx += 1

    concepts.append(concept_block(
        "4. With repetition vs without repetition",
        [
            "With repetition allowed, ordered length-k codes from n symbols: $n^k$. Each slot keeps all n choices.",
            "Without repetition: $P(n,k)$. Slots shrink.",
            "Read the problem: “digits may be repeated” vs “all digits different.” That single phrase flips the formula.",
            "Phone number models, license plates, and PINs are common homes for this distinction.",
            "If the problem says “using each at most once,” think permutations. If “any digit any time,” think $n^k$.",
            "Mixed restrictions (first digit nonzero, others free) need custom slot counts — still product rule, not a blind formula.",
        ],
        "<p>Repetition rules change the slot numbers.</p>",
        "<p>Underline “repeated” or “distinct.” Then write slots.</p>",
        solved(10, "Length-3 codes from 0–9 with repeats OK?",
               ["$10^3=1000$."], "$1000$", "", "Easy")
        + solved(11, "Length-3 codes from 0–9 no repeats?",
                 ["$P(10,3)=720$."], "$720$", "", "Easy")
        + solved(12, "4-digit numbers with distinct digits?",
                 ["First digit 9 options (1–9).", "Next 9 (include 0 except used).", "Then 8, then 7.",
                  "$9\\times9\\times8\\times7=4536$."],
                 "$4536$", "", "Hard"),
        ("Using n^k when distinct is required", "Distinct means shrinking slots."),
        ("Custom first slot", "Numbers need nonzero leading digit."),
        ["I choose n^k vs P(n,k) correctly.", "I adjust leading digits for numbers.", "I can explain both models."],
        16,
    ))
    for text, ans, expl in [
        ("$5^3$ with repeats length-3 from 5 symbols?", 125, "$5^3=125$."),
        ("$P(5,3)$ no repeats?", 60, "$5\\times4\\times3=60$."),
        ("Bit strings length 6?", 64, "$2^6=64$."),
        ("Distinct length-2 from 26 letters?", 650, "$P(26,2)=650$."),
        ("Repeats OK length-2 from 26 letters?", 676, "$26^2=676$."),
    ]:
        qs.append(mq(text, ans, expl, idx)); idx += 1

    concepts.append(concept_block(
        "5. Circular arrangements — rotations look the same",
        [
            "Around a round table, rotating everyone one seat often counts as the same seating if seats are not labeled.",
            "Standard model for $n$ distinct people around a circle (rotations same): $(n-1)!$.",
            "Why: fix one person’s position to remove rotational twins, then arrange the other $n-1$ people in the remaining seats: $(n-1)!$.",
            "If reflections are also considered the same (necklace that can flip), you often divide by 2 more — only when the problem says flips count as identical.",
            "If seats are numbered (Seat 1 next to a window), it is a line-like problem: use $n!$, not $(n-1)!$.",
            "MathCounts states the table/necklace rules in words — trust the wording over memorized habits.",
        ],
        "<p>Circles remove a rotational symmetry.</p>",
        "<p>Ask: are seats labeled? Can we rotate? Can we flip?</p>",
        solved(13, "5 distinct people around an unlabeled round table (rotations same)?",
               ["$(5-1)!=24$."], "$24$", "", "Medium")
        + solved(14, "6 people around labeled seats numbered 1–6?",
                 ["Seats labeled → $6!=720$."], "$720$", "", "Easy")
        + solved(15, "8 beads on a necklace if rotations same but flips count as different?",
                 ["$(8-1)!=5040$."], "$5040$", "If flips also identical, often $\\frac{7!}{2}$.", "Hard"),
        ("Always dividing by n", "Only for unlabeled rotations; labeled seats differ."),
        ("Fix one person", "That picture explains (n-1)!."),
        ["I know when to use (n-1)!.", "I check labeled vs unlabeled.", "I only divide by 2 for flips when told."],
        21,
    ))
    for text, ans, expl in [
        ("Circular arrangements of 6 distinct people (rotations same)?", 120, "$(6-1)!=120$."),
        ("Circular arrangements of 4 distinct people?", 6, "$(4-1)!=6$."),
        ("7 people in labeled chairs?", 5040, "$7!=5040$."),
        ("$(8-1)!$=?", 5040, "$7!=5040$."),
        ("3 people round table rotations same?", 2, "$(3-1)!=2$."),
    ]:
        qs.append(mq(text, ans, expl, idx)); idx += 1

    concepts.append(concept_block(
        "6. Contest permutation patterns",
        [
            "Pattern A: distinct prizes / ranked places → $P(n,k)$.",
            "Pattern B: rearrange a word with repeats → divide factorials.",
            "Pattern C: PIN with/without repeats → $n^k$ or $P(n,k)$.",
            "Pattern D: round table → $(n-1)!$ if rotations identical.",
            "When stuck: rewrite the problem as slots with shrinking options. That almost always reveals the product.",
            "National/AMC 10 may combine circular ideas with restrictions (two people must sit together — glue them as a block).",
        ],
        "<p>Recognizing the pattern saves minutes on Sprint/AMC.</p>",
        "<p>Match the problem to A/B/C/D above before computing.</p>",
        solved(16, "Glue trick preview: 5 people in a line, A and B must be together?",
               ["Treat (AB) as one block → 4 entities: block,C,D,E → $4!$ ways.",
                "Block internal: AB or BA → $\\times2$.",
                "Total $4!\\times2=48$."],
               "$48$", "Block method is a National favorite.", "Challenge")
        + solved(17, "How many 5-letter strings from {A,B,C,D,E} with all distinct letters?",
                 ["$P(5,5)=120$."], "$120$", "", "Easy")
        + solved(18, "Arrangements of AAABBC?",
                 [f"$\\frac{{6!}}{{3!2!}}={perm_repeated('AAABBC')}$."],
                 str(perm_repeated("AAABBC")), "", "Medium"),
        ("Gluing without multiplying internal arrangements", "Blocks can often flip order inside."),
        ("Pattern label", "Write “Pattern B: repeated letters” on scratch paper."),
        ["I recognize P vs repeated-letter vs circle.", "I can use a glue block.", "I pick formulas from wording."],
        26,
    ))
    for text, ans, expl in [
        ("$P(7,3)$=?", 210, "$7\\times6\\times5=210$."),
        ("Arrangements of BOOKKEEPER? (approx structure)", perm_repeated("BOOKKEEPER"),
         f"Frequencies B1 O2 K2 E3 P1 R1 → {perm_repeated('BOOKKEEPER')}."),
        ("Line of 5 with two specific glued together?", 48, "$4!\\times2=48$."),
        ("$10!$ / $9!$ =?", 10, "Cancels to 10."),
        ("Circular 5 people rotations same?", 24, "$4!=24$."),
    ]:
        qs.append(mq(text, ans, expl, idx)); idx += 1

    # Finale 50
    finale_specs = []
    for n in range(3, 9):
        finale_specs.append((f"Compute ${n}!$.", math.factorial(n), f"${n}!={math.factorial(n)}$."))
    for n, k in [(9, 2), (9, 3), (10, 2), (10, 3), (10, 4), (12, 2), (7, 4), (8, 4)]:
        finale_specs.append((f"$P({n},{k})$=?", math.perm(n, k), f"$P({n},{k})={math.perm(n,k)}$."))
    for w in ["BALL", "LEVEL", "TOOTH", "SUCCESS", "BALLOON", "MISSISSIPPI"]:
        finale_specs.append((f"Distinct arrangements of {w}?", perm_repeated(w),
                             f"Divide by repeated-letter factorials → {perm_repeated(w)}."))
    for n in range(4, 9):
        finale_specs.append((f"Circular arrangements of {n} distinct people (rotations same)?",
                             math.factorial(n - 1), f"$({n}-1)!={math.factorial(n-1)}$."))
    finale_specs += [
        ("Length-4 codes digits 0–9 repeats OK?", 10000, "$10^4=10000$."),
        ("Length-4 codes digits 0–9 no repeats?", math.perm(10, 4), f"$P(10,4)={math.perm(10,4)}$."),
        ("4-digit numbers distinct digits?", 4536, "$9\\times9\\times8\\times7=4536$."),
        ("$P(6,6)$=?", 720, "$6!=720$."),
        ("Arrangements of AAA BBB?", math.comb(6, 3), "$\\frac{6!}{3!3!}=20$."),
        ("Injective functions [2]→[5]?", math.perm(5, 2), "$P(5,2)=20$."),
        ("5 people line, A,B together?", 48, "$4!\\times2=48$."),
        ("6 people line, A,B together?", 240, "$5!\\times2=240$."),
        ("Necklace 6 distinct beads rotations same flips different?", 120, "$5!=120$."),
        ("$7!/(5!)$=?", 42, "$7\\times6=42$."),
    ]
    while len(finale_specs) < 25:
        n = 5 + len(finale_specs) % 4
        finale_specs.append((f"$P({n+3},{2})$=?", math.perm(n + 3, 2), "Falling product of 2 terms."))
    for text, ans, expl in finale_specs[:25]:
        qs.append(mq(text, ans, expl, idx)); idx += 1

    return _assemble(
        title, description,
        "Grades 6–8 · MathCounts · AMC 8/10",
        ["Factorials", "P(n,k)", "Identical letters", "Repetition rules", "Circles", "Contest patterns"],
        concepts, qs,
    )
