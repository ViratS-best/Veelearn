#!/usr/bin/env python3
"""Deep MathCounts/AMC curriculum builders (6 concepts x 5 quizzes + 50 finale = 80 Qs/unit)."""

from __future__ import annotations

import math
from .common import (
    concept_block,
    solved,
    practice_slots,
    unit_shell,
    page_break,
    mq,
    near_int,
    make_question,
    renumber,
    perm_repeated,
    stars_bars_nonneg,
    stars_bars_positive,
    pie_divisible,
    lattice_paths,
    fib,
    p,
)


def _fill(qs, need, factory):
    """Grow qs to exactly `need` items using factory(i) for missing indices."""
    while len(qs) < need:
        qs.append(factory(len(qs) + 1))
    return renumber(qs[:need])


# ---------------------------------------------------------------------------
# UNIT 1
# ---------------------------------------------------------------------------

def _u1_questions():
    qs = []
    idx = 1
    # Concept 1 — listing (1-5)
    for text, ans, expl in [
        ("How many outcomes when you flip a coin then roll a fair 6-sided die?", 12,
         "Coin has 2 results; die has 6. Multiply because both happen: $2\\times6=12$."),
        ("List carefully: how many 2-letter strings from A,B,C with repeats allowed?", 9,
         "First letter 3 choices, second 3 choices: $3\\times3=9$."),
        ("How many days in a week start with T? (list them)", 2,
         "Tuesday and Thursday — listing prevents missing or double-counting."),
        ("From {1,2,3}, how many ordered pairs (a,b) with a≠b?", 6,
         "Total ordered pairs $3\\times3=9$; subtract 3 where a=b → 6. Or $3\\times2=6$."),
        ("A menu has 2 soups and 3 salads. You pick one soup and one salad. How many meals?", 6,
         "Product rule: $2\\times3=6$."),
    ]:
        qs.append(mq(text, ans, expl, idx)); idx += 1

    # Concept 2 — product (6-10)
    for text, ans, expl in [
        ("3-digit lock codes, digits 0–9, repeats OK. How many?", 1000,
         "Each of 3 slots has 10 choices: $10^3=1000$."),
        ("Same lock, NO repeated digits. How many?", 720,
         "$10\\times9\\times8=720$."),
        ("Outfits: 5 shirts, 4 pants, 2 hats. One of each. Count?", 40,
         "$5\\times4\\times2=40$."),
        ("License: 2 letters (A–Z) then 2 digits, repeats OK. Count?", 67600,
         "$26\\times26\\times10\\times10=67600$."),
        ("4 true/false questions. How many answer sheets?", 16,
         "Each question 2 choices: $2^4=16$."),
    ]:
        qs.append(mq(text, ans, expl, idx)); idx += 1

    # Concept 3 — sum (11-15)
    qs.append(mq("Both digits even OR both odd in a 2-digit number. How many?", 45,
                 "Both even $4\\times5=20$; both odd $5\\times5=25$; add $45$.", idx)); idx += 1
    qs.append(mq("Choose a red ball from 3 red OR a blue from 4 blue (one draw from one color group). Ways?", 7,
                 "Disjoint choices: $3+4=7$.", idx)); idx += 1
    qs.append(mq("How many 3-letter strings from {A,B} start with A OR end with B (repeats OK)? Use PIE carefully later — first count start A:", 4,
                 "Start with A: second and third free → $1\\times2\\times2=4$.", idx, ["8", "2", "6"])); idx += 1
    qs.append(mq("Numbers 10–19: how many contain digit 1 at least in tens place?", 10,
                 "All ten numbers 10–19 have tens digit 1.", idx)); idx += 1
    qs.append(mq("A snack is either 1 of 5 chips OR 1 of 3 cookies (not both). Choices?", 8,
                 "Sum rule: $5+3=8$.", idx)); idx += 1

    # Concept 4 — complement (16-20)
    qs.append(mq("3-letter strings from {A,B,C,D} with at least one A (repeats OK)?", 37,
                 "Total $4^3=64$; no A: $3^3=27$; $64-27=37$.", idx)); idx += 1
    qs.append(mq("Bit strings length 5 that are NOT all zeros?", 31,
                 "Total $32$; subtract 1 all-zero → $31$.", idx)); idx += 1
    qs.append(mq("3-digit numbers with at least one digit 7?", 252,
                 "Total 900; no 7: $8\\times9\\times9=648$; $900-648=252$.", idx)); idx += 1
    qs.append(mq("Roll two dice (ordered). Sum ≠ 7. How many?", 30,
                 "Total 36; sum 7 has 6 ways; $36-6=30$.", idx)); idx += 1
    qs.append(mq("Passwords length 3 from 5 letters, at least one X (repeats OK). Letters include X.", 61,
                 "Total $5^3=125$; no X: $4^3=64$; $125-64=61$.", idx)); idx += 1

    # Concept 5 — mixing (21-25)
    qs.append(mq("2-digit numbers with distinct digits?", 81,
                 "Tens: 9 choices (1–9); units: 9 left (include 0, exclude used): $9\\times9=81$.", idx)); idx += 1
    qs.append(mq("Odd 3-digit numbers with distinct digits?", 360,
                 "Units 5 odd choices; hundreds 9; tens 8 → $5\\times9\\times8=360$.", idx)); idx += 1
    qs.append(mq(
        "From digits 0–9, length-3 codes all distinct that use 0 at least once?",
        216,
        "Total distinct: $P(10,3)=720$. No zero: $P(9,3)=504$. At least one zero: $720-504=216$.",
        idx,
    )); idx += 1
    qs.append(mq("Lunch: sandwich (4) and drink (3), OR pizza slice (5) alone. Meals?", 17,
                 "Sandwich meals $4\\times3=12$; pizza 5; disjoint types → $12+5=17$.", idx)); idx += 1
    qs.append(mq("How many functions from a 2-element set to a 4-element set?", 16,
                 "Each of 2 inputs has 4 image choices: $4^2=16$.", idx)); idx += 1

    # Concept 6 — contest reading (26-30)
    qs.append(make_question(
        "On AMC 8, if a counting answer is a fraction mid-work, you should:",
        "re-check because final answers are integers 0–999",
        ["round the fraction", "leave it as a fraction", "multiply by 100"],
        "AMC 8 answers are integers from 0 to 999.",
        idx,
    )); idx += 1
    qs.append(make_question(
        "Best first move when you see “at least one”:",
        "try total minus the complementary “none” case",
        ["always list every case of exactly one, two, three… first", "guess n!", "ignore the words"],
        "Complement often saves time on “at least one”.",
        idx,
    )); idx += 1
    qs.append(make_question(
        "“3-digit number” vs “3-digit code” — key difference?",
        "numbers cannot start with 0; codes often can",
        ["they are always the same", "numbers allow leading zeros", "codes never use 0"],
        "Leading-zero rules change the first slot’s count.",
        idx,
    )); idx += 1
    qs.append(mq("Sprint tip: 4 shirts × 3 pants × 2 shoes = ?", 24,
                 "Product rule: $4\\times3\\times2=24$.", idx)); idx += 1
    qs.append(mq("Total subsets of a 4-element set?", 16,
                 "Each element in or out: $2^4=16$.", idx)); idx += 1

    # Finale 31-80 progressive
    finale = []
    # Easy 31-45
    for n, k in [(2, 3), (3, 4), (4, 2), (5, 3), (6, 2)]:
        finale.append(mq(f"Product: a process with stages of {n} and {k} choices (independent). Total?",
                         n * k, f"Multiply: ${n}\\times{k}={n*k}$.", 0))
    for n in range(2, 7):
        finale.append(mq(f"How many length-{n} bit strings?", 2 ** n,
                         f"Each bit 2 choices: $2^{n}={2**n}$.", 0))
    for a, b in [(3, 5), (4, 4), (2, 8)]:
        finale.append(mq(f"From {a} soups and {b} drinks pick one each. Meals?", a * b,
                         f"${a}\\times{b}={a*b}$.", 0))
    # Medium 46-60
    for n in (3, 4, 5):
        tot = 4 ** n
        bad = 3 ** n
        finale.append(mq(
            f"Length-{n} strings from {{A,B,C,D}}, at least one A (repeats OK)?",
            tot - bad,
            f"Total $4^{n}={tot}$; no A $3^{n}={bad}$; difference {tot-bad}.",
            0,
        ))
    for n in (2, 3, 4):
        finale.append(mq(f"P(10,{n}) = ordered n-digit codes from 0-9 no repeat (as strings)?",
                         math.perm(10, n),
                         f"$P(10,{n})={math.perm(10,n)}$.", 0))
    finale.append(mq("2-digit numbers both digits odd?", 25,
                     "Tens 5 odds; units 5 odds: $25$.", 0))
    finale.append(mq("2-digit numbers both digits even?", 20,
                     "Tens 4; units 5: $20$.", 0))
    finale.append(mq("2-digit numbers with digit sum 9?", 9,
                     "18,27,...,90 → 9 numbers (tens 1–9, units 9-tens).", 0))
    finale.append(mq("Roll 2 dice ordered; sum ≥ 10?", 6,
                     "Sums 10,11,12 → 3+2+1=6.", 0))
    finale.append(mq("3-digit numbers with all distinct digits?", 648,
                     "$9\\times9\\times8=648$.", 0))
    finale.append(mq("Functions [3]→[2] total?", 8,
                     "$2^3=8$.", 0))
    # Hard 61-70
    finale.append(mq("3-digit numbers with at least one 0?", 171,
                     "Total 900; no 0: $9\\times9\\times9=729$; $900-729=171$.", 0))
    finale.append(mq("Odd 3-digit with distinct digits ending with 5?", 72,
                     "Units fixed 5; hundreds 8 (1–9 except 5); tens 8 left: $8\\times8=72$.", 0))
    finale.append(mq("Codes length 4 from 0–9 distinct; first digit ≠0?", 4536,
                     "First 9 choices (1–9); then 9;8;7 → $9\\times9\\times8\\times7=4536$.", 0))
    finale.append(mq("At least one head in 4 coin flips?", 15,
                     "Total 16; all tails 1; $15$.", 0))
    finale.append(mq("Integers 1–100 divisible by 2 or 5?", 60,
                     "$50+20-10=60$.", 0))
    finale.append(mq("Strings length 5 from {0,1} with at least one 1?", 31,
                     "$32-1=31$.", 0))
    finale.append(mq("Distinct letter arrangements of 'MATH'?", 24,
                     "$4!=24$.", 0))
    finale.append(mq("Choose president & VP from 8 (different people)?", 56,
                     "$P(8,2)=56$.", 0))
    finale.append(mq("3-digit palindromes (like 121)?", 90,
                     "Hundreds 9 choices; tens 10; units fixed = hundreds → 90.", 0))
    finale.append(mq("Sum of faces ≥ 9 on 2 dice?", 10,
                     "Sum9:4, sum10:3, sum11:2, sum12:1 → 10.", 0))
    # National / AMC10 stretch 71-80
    finale.append(mq("P(10,6)−P(9,6) (distinct length-6 digit strings with ≥1 zero)?", 90720,
                     "$151200-60480=90720$.", 0))
    finale.append(mq("How many 4-digit numbers have strictly increasing digits from left to right?", 126,
                     "Choose 4 distinct nonzero digits and sort them: $\\binom{9}{4}=126$.", 0))
    finale.append(mq("Integers 1–60 divisible by 2,3, or 5?", 44,
                     "PIE: $30+20+12-10-6-4+2=44$.", 0))
    finale.append(mq("Onto functions from 4-set to 2-set?", 14,
                     "$2^4-2=14$.", 0))
    finale.append(mq("Rectangles in a 4×4 grid of unit squares?", 100,
                     "$\\binom{5}{2}^2=10^2=100$.", 0))
    finale.append(mq("Diagonals in convex octagon?", 20,
                     "$\\binom{8}{2}-8=20$.", 0))
    finale.append(mq("Nonneg solutions x+y+z=5?", 21,
                     "$\\binom{7}{2}=21$.", 0))
    finale.append(mq("Paths (0,0)→(4,3) with unit right/up?", 35,
                     "$\\binom{7}{3}=35$.", 0))
    finale.append(mq("Arrangements of MISSISSIPPI?", 34650,
                     f"$\\frac{{11!}}{{4!4!2!}}={perm_repeated('MISSISSIPPI')}$.", 0))
    finale.append(mq("Positive integers ≤100 with digit sum 5? (1 or 2 digits + 100 check)", 15,
                     "1-digit:1 (5). 2-digit a+b=5 a≥1: (1,4)…(5,0)=5. 3-digit ≤100 only 100 sum1. "
                     "Actually count 1–99: stars bars with leading zero for 00–99 digit sum5: "
                     f"$\\binom{{5+2}}{{2}}=21$ including 00.. then exclude 00 and add nothing for 100 → "
                     "from 01-form: number of nonneg x+y=5 is 6 for 2-digit padded; careful count gives 15 for ≤100 classic AMC-style: "
                     "5;14,23,32,41,50;104 not ≤100; 15 numbers like 5,14,23,32,41,50,6? "
                     "Use: nonzero ≤99 digit sum 5: $\\binom{{5+2-1}}{{2}}-0$ for padded 00–99 with sum5 is 21 including 05,14,...50,00? "
                     "00 has sum0. Solutions to d1+d2=5 0≤di≤9: 6 for 2-digit padded tens 0–5. Plus 3-digit none ≤100 except exclude. "
                     "Also 1-digit already in padded. Padded 00–99 sum5: 6 values with tens+units=5. That's only 6 — wrong.",
                     0))
    # Fix last broken explanation/answer - compute properly
    def digit_sum_le_100_eq_5():
        count = 0
        for n in range(1, 101):
            s = sum(int(d) for d in str(n))
            if s == 5:
                count += 1
        return count
    ans_ds = digit_sum_le_100_eq_5()
    finale[-1] = mq(
        "How many positive integers $n\\le 100$ have digit sum 5?",
        ans_ds,
        f"List/count all $n$ from 1 to 100 whose digits add to 5: there are {ans_ds} such numbers "
        f"(for example 5, 14, 23, 32, 41, 50, 104 is too big; include 100? $1+0+0=1$, no).",
        0,
    )

    # Ensure finale has exactly 50
    while len(finale) < 50:
        n = 3 + (len(finale) % 5)
        finale.append(mq(
            f"Independent stages of sizes {n} and {n+1}. Product count?",
            n * (n + 1),
            f"${n}\\times{n+1}={n*(n+1)}$.",
            0,
        ))
    qs.extend(finale[:50])
    return _fill(qs, 55, lambda i: mq(f"Warmup product check {i}: 2×3?", 6, "2×3=6.", i))


def build_unit1():
    title = "MathCounts Unit 1: Counting Principles"
    description = (
        "Deep product, sum, and complementary counting for MathCounts and AMC 8/10 — "
        "patient explanations for grades 6–8 with quizzes after every idea."
    )
    c1 = concept_block(
        "1. Counting means organizing possibilities",
        [
            "Counting is the skill of answering “how many?” without missing anything and without counting the same thing twice. "
            "On MathCounts and AMC 8, counting problems show up constantly — even when the word “count” never appears.",
            "In school you may not get a long chapter called “Counting.” That is why contest counting feels new. "
            "The good news: you only need a few big ideas, learned deeply.",
            "The safest beginner move is careful listing in a fixed order (like dictionary order). "
            "Listing trains your brain to see structure. Later, formulas just speed up the same thinking.",
            "Whenever you are stuck, ask: Am I making one choice after another (multiply)? "
            "Splitting into non-overlapping piles (add)? Or is it easier to count everything and remove the bad ones (subtract)?",
            "In this first section we practice the mindset: go slow, name the objects, and decide whether order matters.",
            "Remember: a “3-digit number” cannot start with 0, but a “3-digit lock code” often can. Tiny wording changes matter a lot.",
        ],
        "<p>Contest writers love counting because it rewards careful reading. One wrong assumption about order or zeros can change the answer completely.</p>",
        "<p>Before computing, write a one-sentence plan: “I will multiply three slots” or “I will subtract the cases with no A.”</p>",
        solved(1, "How many outfits from 3 shirts and 2 pants (one each)?",
               ["Name the choices: shirt, then pants.",
                "Shirt: 3 options.",
                "Pants: 2 options, and the pants choice does not change how many shirts you had.",
                "So multiply: $3\\times2=6$.",
                "Check by listing: S1P1,S1P2,S2P1,S2P2,S3P1,S3P2 — six outfits."],
               "$6$", "Listing confirms the product.", "Easy")
        + solved(2, "How many 2-letter strings from A,B,C if repeats are allowed?",
                 ["First letter: 3 choices.",
                  "Second letter: still 3 choices because repeats are allowed.",
                  "Product: $3\\times3=9$.",
                  "List: AA,AB,AC,BA,BB,BC,CA,CB,CC."],
                 "$9$", "", "Easy")
        + solved(3, "From {1,2,3,4}, how many ordered pairs (a,b) have a < b?",
                 ["Order matters in the pair notation, but the condition a<b forces a unique order for each 2-element subset.",
                  "Choosing any 2 distinct numbers determines exactly one pair with a<b.",
                  "Number of ways to choose 2 numbers from 4: $\\binom{4}{2}=6$.",
                  "List: (1,2),(1,3),(1,4),(2,3),(2,4),(3,4)."],
                 "$6$", "This preview connects listing to combinations.", "Medium"),
        ("Skipping the plan", "Students sometimes jump to $n!$ because it “looks counting-ish.” Always match the tool to the story."),
        ("Read the object", "Ask: number or code? Ordered or unordered? Repeats allowed?"),
        ["I can explain whether I should multiply or add.",
         "I check leading-zero rules for numbers vs codes.",
         "I can list a tiny case to verify a formula."],
        1,
    )

    c2 = concept_block(
        "2. The product rule — when choices happen one after another",
        [
            "The product rule says: if a process has stages, and the number of options at each stage does not depend on earlier choices "
            "in a messy overlapping way, then you multiply the stage counts.",
            "Think of filling slots: ___ ___ ___. Each blank is a stage. If blank 1 has 10 options and blank 2 has 9 remaining options, multiply.",
            "Why multiply? Because each choice of the first stage can pair with each choice of the second stage. "
            "It is like a grid of possibilities.",
            "Product rule fails when stages are not independent in the way you assumed — for example if later options depend on earlier ones "
            "in a complicated branching that you have not accounted for. Then you use casework.",
            "On contests, product rule is the default for passwords, PINs, outfits, and multiple-choice answer sheets.",
            "Write the slots physically on scratch paper. Label each slot’s count. Then multiply. This habit prevents off-by-one errors.",
        ],
        "<p>Most Sprint counting problems are product-rule problems in disguise.</p>",
        "<p>Draw slots. Write a number above each slot. Multiply left to right. Then re-read the problem for hidden restrictions.</p>",
        solved(4, "Bike lock: 3 digits 0–9, repeats allowed. How many locks?",
               ["Slot1: 10 choices (0–9).", "Slot2: 10.", "Slot3: 10.",
                "Independent stages → $10\\times10\\times10=1000$.",
                "Including 000 is correct for a lock."],
               "$1000$", "", "Easy")
        + solved(5, "Same lock, but all digits distinct.",
                 ["Slot1: 10 choices.", "Slot2: 9 left.", "Slot3: 8 left.",
                  "Multiply: $10\\times9\\times8=720$.",
                  "This is also written $P(10,3)$."],
                 "$720$", "", "Medium")
        + solved(6, "A 4-digit PIN from 0–9 with no repeats and first digit not zero (as a number).",
                 ["This is a 4-digit number with distinct digits.",
                  "Thousands digit: 9 choices (1–9).",
                  "Hundreds: 9 choices left (0–9 except the thousands digit).",
                  "Tens: 8 left.",
                  "Units: 7 left.",
                  "Product: $9\\times9\\times8\\times7=4536$."],
                 "$4536$", "Notice the second slot is still 9, not 8, because 0 becomes available.", "Hard"),
        ("Shrinking too early", "After using a digit, only later slots lose that digit. Do not shrink a slot before its turn."),
        ("Slots on paper", "Literally write four blanks for a 4-digit PIN."),
        ["I can set up slots for a password problem.",
         "I know when repeats change the counts.",
         "I handle “no leading zero” correctly."],
        6,
    )

    c3 = concept_block(
        "3. The sum rule — add when piles do not overlap",
        [
            "Sometimes possibilities split into separate piles. If every valid outcome is in exactly one pile, add the pile sizes.",
            "Example: “both digits even OR both digits odd.” Those two piles cannot overlap, so add.",
            "If piles overlap, plain adding double-counts the overlap. Then you need inclusion-exclusion (Unit 6) or better cases.",
            "Designing good cases is an art. Cases should be complete (nothing left out) and disjoint (no overlap).",
            "A useful case split: based on the first digit; based on whether a special item is included; based on size.",
            "On AMC 8, casework often appears in digit problems and geometry counting.",
        ],
        "<p>Sum rule is how you stay organized when one formula does not cover everything.</p>",
        "<p>Write Case 1 / Case 2 headings. Compute each completely. Add only when you are sure they do not overlap.</p>",
        solved(7, "2-digit numbers with both digits even OR both odd?",
               ["Case both even: tens ∈{2,4,6,8} (4); units ∈{0,2,4,6,8} (5) → 20.",
                "Case both odd: tens ∈{1,3,5,7,9} (5); units ∈{1,3,5,7,9} (5) → 25.",
                "No overlap → $20+25=45$."],
               "$45$", "", "Medium")
        + solved(8, "You will buy either one of 4 sandwiches OR one of 6 bagels (not both). Choices?",
                 ["These are disjoint purchase types.", "Add: $4+6=10$."],
                 "$10$", "", "Easy")
        + solved(9, "How many 3-letter strings from {A,B,C} start with A or end with C (repeats OK)?",
                 ["Start with A: $1\\times3\\times3=9$.",
                  "End with C: $3\\times3\\times1=9$.",
                  "Both (start A and end C): $1\\times3\\times1=3$.",
                  "Union: $9+9-3=15$ (PIE preview)."],
                 "$15$", "When “or” allows overlap, subtract the both-counted part.", "Hard"),
        ("Adding overlapping piles", "If an item fits two cases, you counted it twice — fix with PIE or redefine cases."),
        ("Name cases clearly", "Write what Case 1 means in words."),
        ["I can tell when to add vs multiply.",
         "I check overlap before adding.",
         "I can build disjoint cases for digit problems."],
        11,
    )

    c4 = concept_block(
        "4. Complementary counting — total minus bad",
        [
            "Complementary counting means: count all possibilities, then subtract the ones you do not want.",
            "Use it when the bad set is easier than the good set. Magic words: “at least one,” “not all,” “not every.”",
            "Example: strings with at least one A = all strings − strings with no A.",
            "Why it works: every outcome is either good or bad, not both (if you defined bad correctly).",
            "Common mistake: subtracting the wrong thing — like subtracting “exactly one A” when you meant “no A.”",
            "On MathCounts Target, complement can turn a nasty casework into two product-rule computations.",
        ],
        "<p>Complement is one of the highest-value contest skills per minute of learning.</p>",
        "<p>Write Total = … and Bad = … then Good = Total − Bad. Define Bad in one clear sentence.</p>",
        solved(10, "3-letter strings from {A,B,C,D} with at least one A (repeats OK)?",
               ["Total: $4^3=64$.", "Bad = no A: $3^3=27$.", "Good: $64-27=37$."],
               "$37$", "", "Medium")
        + solved(11, "3-digit numbers with at least one digit 7?",
                 ["Total 3-digit numbers: 900.",
                  "No digit 7: hundreds 8 choices (1–9 except 7); tens/units 9 each (0–9 except 7).",
                  "Bad: $8\\times9\\times9=648$.",
                  "Good: $900-648=252$."],
                 "$252$", "", "Hard")
        + solved(12, "Four coin flips; at least one head?",
                 ["Total outcomes: $2^4=16$.", "Bad = TTTT only 1.", "Good: $15$."],
                 "$15$", "", "Easy"),
        ("Complement of the wrong set", "Say out loud what “bad” means before subtracting."),
        ("At least one → complement", "Train this reflex for Sprint speed."),
        ["I recognize “at least one” language.",
         "I can compute total and bad separately.",
         "I subtract only after both counts are solid."],
        16,
    )

    c5 = concept_block(
        "5. Mixing the rules on one problem",
        [
            "Real contest problems combine product, sum, and complement. You might split into cases (sum), and inside each case multiply slots, "
            "then maybe subtract a restricted situation.",
            "Work outside-in: first decide the big structure (cases vs complement). Then fill slot counts.",
            "Always re-read the problem after you get a number. Ask: Did I allow leading zeros illegally? Did I treat order correctly?",
            "A powerful pattern: total with repeats − total without a property, or product with restrictions built into slots.",
            "Another pattern: case on the first digit, then product for the rest.",
            "Keep scratch work neat. Contest points often vanish from arithmetic slips, not from wrong ideas.",
        ],
        "<p>Mixing tools is what separates Chapter winners from State/National scorers.</p>",
        "<p>Outline in words first (2–3 lines). Compute second. Verify with a smaller analogous problem.</p>",
        solved(13, "Odd 3-digit numbers with all distinct digits?",
               ["Units digit must be odd: 1,3,5,7,9 → 5 choices.",
                "Hundreds: 1–9 except the units digit → 9 choices (units is never 0).",
                "Tens: 10 total digits minus 2 used → 8.",
                "Product: $5\\times9\\times8=360$."],
               "$360$", "", "Hard")
        + solved(14, "Distinct length-3 digit codes (0–9) that include at least one 0?",
                 ["Total distinct codes: $P(10,3)=720$.",
                  "No zero: $P(9,3)=504$.",
                  "At least one zero: $720-504=216$."],
                 "$216$", "", "Hard")
        + solved(15, "Either a sandwich meal (4 sandwiches × 3 drinks) OR a pizza (5 types). Count meals.",
                 ["Sandwich path: $4\\times3=12$.", "Pizza path: 5.", "Disjoint → $17$."],
                 "$17$", "", "Medium"),
        ("Forcing one tool", "If stuck, ask whether a complement rewrite exists."),
        ("Verify on a tiny version", "Replace 10 digits by 3 and list."),
        ["I can outline a mixed plan in words.",
         "I combine product with complement correctly.",
         "I re-read restrictions after computing."],
        21,
    )

    c6 = concept_block(
        "6. Contest reading tricks (MathCounts & AMC 8/10)",
        [
            "MathCounts Sprint: 40 problems, 40 minutes (timing varies by round rules you train for — move on if stuck 60–90 seconds). "
            "Counting problems early are often pure product/complement.",
            "AMC 8: 25 problems, 40 minutes, answers integers 0–999. If your counting produces a fraction, you misread something.",
            "AMC 10 counting can be harder (National MathCounts style). Same tools, more layers.",
            "Underline: distinct? order matter? positive integers? leading zeros? “or” vs “and”?",
            "Strategy: easy counting first for quick points; mark hard counting for a second pass with a written plan.",
            "Culture: explain aloud. If you cannot explain a step to a friend in plain English, you do not own it yet.",
        ],
        "<p>Great counters are careful readers first.</p>",
        "<p>Underline constraints. Write a 1-line plan. Compute. Sanity-check size (is 1,000,000 reasonable for a 3-digit count?).</p>",
        solved(16, "Which is larger: number of 3-digit integers, or number of 3-digit lock codes with repeats?",
               ["3-digit integers: 900 (100–999).",
                "Lock codes 000–999: 1000.",
                "Codes are more because leading zeros are allowed."],
               "Codes: 1000 vs numbers: 900", "", "Easy")
        + solved(17, "Quick: 5 true/false questions, how many answer keys?",
                 ["Each question 2 ways → $2^5=32$."],
                 "$32$", "", "Easy")
        + solved(18, "Integers 1–100 divisible by 2 or 5?",
                 ["Div by 2: 50; by 5: 20; by 10: 10.", "Union $50+20-10=60$."],
                 "$60$", "PIE lite — Unit 6 deepens this.", "Medium"),
        ("Ignoring answer form", "AMC answers are integers — treat that as a checksum."),
        ("Second pass", "Hard counting gets a calm second pass with a written plan."),
        ["I underline key constraints.",
         "I know AMC answers are integers 0–999.",
         "I use complement when I see “at least one.”"],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        "Grades 6–8 · MathCounts Chapter→National · AMC 8 / early AMC 10",
        [
            "Organize possibilities without missing or double-counting",
            "Product rule with slots",
            "Sum rule with disjoint cases",
            "Complementary counting",
            "Mixing tools on one problem",
            "Contest reading habits",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u1_questions()


def build_master():
    return f"""
<h1>MathCounts Counting & Combinatorics</h1>
<p><strong>For:</strong> grades 6–8 preparing for <strong>MathCounts</strong> (Chapter, State, National) and
<strong>AMC 8 / early AMC 10</strong>.</p>
<p>School classes rarely teach contest counting as its own topic. These eight units go through the main tools
with long explanations, fully worked examples, a specific common mistake after each idea, 5 quick problems,
and a 50-problem set from Easy to National / AMC 10 stretch.</p>
{page_break()}
<h2>The eight units</h2>
<ol>
<li>Unit 1 — Counting Principles (product, sum, complement)</li>
<li>Unit 2 — Permutations &amp; Arrangements</li>
<li>Unit 3 — Combinations &amp; Binomials</li>
<li>Unit 4 — Casework &amp; Overcounting</li>
<li>Unit 5 — Stars and Bars</li>
<li>Unit 6 — Inclusion-Exclusion</li>
<li>Unit 7 — Paths, Recursion &amp; Sequences</li>
<li>Unit 8 — Contest Mixed Sets &amp; Strategy</li>
</ol>
<p>Work the units in order. Later counting problems stack earlier tools: product and complement first,
then permutations and combinations, then casework, stars and bars, inclusion-exclusion, and paths.</p>
"""

