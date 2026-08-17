"""Seventh Grade Math units 1–4: negatives, rational operations, proportions, percents."""

from curriculum_kit import lesson_figure, svg_fraction_bar

from .common import (
    concept_block, solved, practice_slots, unit_shell, kid_tip, watch_out, try_this,
    step_reveal, matching, phet_box, hops_line, integer_line, tape_diagram,
    double_number_line, percent_bar, proportional_graph, scale_drawing, mq, renumber,
)


def _fill(qs, need, factory):
    while len(qs) < need:
        qs.append(factory(len(qs) + 1))
    return renumber(qs[:need])


def _pack(items):
    qs = []
    for i, (text, ans, dist, expl) in enumerate(items, 1):
        qs.append(mq(text, ans, expl, i, distractors=dist))
    return qs


# UNIT 1

def _u1_questions():
    items = [
        ("3 + (−5) = ?", "−2", ["8", "2", "−8"], "Start at 3, hop left 5."),
        ("−4 + (−2) = ?", "−6", ["−2", "2", "6"], "Both hops left."),
        ("−4 + 7 = ?", "3", ["−11", "11", "−3"], "Left 4, then right 7."),
        ("6 − 9 = ?", "−3", ["3", "15", "−15"], "6 + (−9) = −3."),
        ("5 − (−3) = ?", "8", ["2", "−8", "−2"], "Minus a negative is plus."),
        ("−2 − 5 = ?", "−7", ["3", "7", "−3"], "−2 + (−5) = −7."),
        ("The additive inverse of −8 is…", "8", ["−8", "0", "1/8"], "Adds to 0."),
        ("−3.5 + 1.2 = ?", "−2.3", ["−4.7", "2.3", "4.7"], "Negative piece is larger."),
        ("1/2 + (−1/4) = ?", "1/4", ["−1/4", "3/4", "−3/4"], "2/4 − 1/4."),
        ("−4° rises 10°. New temp?", "6°", ["−14°", "4°", "−6°"], "−4+10=6."),
        ("Gain 12 then lose 15. Net?", "−3", ["3", "27", "−27"], "12+(−15)."),
        ("Distance between −2 and 5?", "7", ["3", "−7", "10"], "|5−(−2)|."),
        ("−10 + 10 = ?", "0", ["20", "−20", "1"], "Opposites cancel."),
        ("0 − 8 = ?", "−8", ["8", "0", "1"], "From 0, left 8."),
        ("−1 + (−1) + (−1) = ?", "−3", ["−1", "3", "1"], "Three steps left."),
        ("7 + (−2) + (−5) = ?", "0", ["14", "−14", "4"], "7−2−5=0."),
        ("−6.1 − 2.4 = ?", "−8.5", ["−3.7", "8.5", "3.7"], "Both left."),
        ("3/4 − 5/4 = ?", "−1/2", ["2", "1/2", "8/4"], "−2/4 = −1/2."),
        ("Which is true?", "−7 < −2", ["−7 > −2", "−7 = −2", "−7 > 0"], "Farther left is less."),
        ("|−4 + 1| = ?", "3", ["−3", "5", "4"], "|−3|=3."),
        ("−$20 then +$8. Net?", "−$12", ["$12", "−$28", "$28"], "−20+8."),
        ("5 − 5 − 5 = ?", "−5", ["5", "0", "15"], "5−10=−5."),
        ("−2.5 + 2.5 = ?", "0", ["5", "−5", "2.5"], "Opposites."),
        ("A number plus 4 is 1. The number?", "−3", ["5", "3", "−5"], "1−4=−3."),
        ("−8 − (−3) = ?", "−5", ["−11", "11", "5"], "−8+3."),
        ("4 + (−4) lands at…", "0", ["8", "−8", "4"], "Origin."),
        ("−1/2 − 1/2 = ?", "−1", ["0", "1", "−1/4"], "Two halves left."),
        ("−7 yd then +3 yd. Net?", "−4 yards", ["10 yards", "4 yards", "−10 yards"], "−7+3."),
        ("Which sum is positive?", "−3 + 8", ["−3 + (−8)", "−8 + 3", "−1 + (−1)"], "8 wins."),
        ("−12 + 5 + (−1) = ?", "−8", ["−18", "8", "6"], "−7 then −8."),
    ]
    return _fill(_pack(items), 55, lambda i: mq(
        f"What is {i % 6} + (−{i % 5 + 1})?",
        (i % 6) - (i % 5 + 1),
        "Adding a negative is a hop left.",
        i,
        distractors=[(i % 6) + (i % 5 + 1), -(i % 6), i % 5 + 1],
    ))


def build_unit1():
    title = "Seventh Grade Math Unit 1: Adding and Subtracting Negative Numbers"
    description = "Add and subtract integers and rational numbers. Subtracting is adding the opposite."
    c1 = concept_block(
        "1. Adding on a number line",
        ["Positive hops go right. Negative hops go left.",
         "3 + (−5) means start at 3, then hop left 5. You land at −2.",
         "−4 + (−2) is two hops left: land at −6. Same signs, add the sizes, keep the sign.",
         "−4 + 7 is left 4, then right 7. The right hop is longer, so you finish at +3.",
         "Different signs: subtract the sizes, keep the sign of the number with the larger absolute value.",
         "Zero is the landmark. Opposites such as −10 + 10 meet there."],
        hops_line(3, [-5], title="3 + (−5)", caption="Start at 3. A hop of −5 goes left. You land at −2.")
        + solved(1, "Find 3 + (−5).", ["Start at 3.", "Adding −5 is five units left.", "Land at −2."], "−2")
        + phet_box("nl_int"),
        kid_tip("Same sign, add. Different signs, subtract sizes.",
                "Then attach the sign of the number with the larger absolute value."),
        1)
    c2 = concept_block(
        "2. Subtracting means add the opposite",
        ["a − b is the same as a + (−b). So 6 − 9 = 6 + (−9) = −3.",
         "Subtracting a negative flips twice: 5 − (−3) = 5 + 3 = 8.",
         "−2 − 5 = −2 + (−5) = −7. −8 − (−3) = −8 + 3 = −5.",
         "Rewrite every subtraction as addition, then use the hop rules.",
         "Keep each sign glued to its number.",
         "Minus a minus is plus. Do not drop a sign in the rewrite."],
        hops_line(5, [3], title="5 − (−3) = 5 + 3",
                  caption="Subtracting −3 is a hop of +3. You move right and land at 8.")
        + solved(1, "Compute 5 − (−3).", ["Rewrite: 5 + 3.", "Hop right 3 from 5.", "8."], "8")
        + matching([("6 − 9", "−3"), ("5 − (−3)", "8"), ("−2 − 5", "−7"), ("−8 − (−3)", "−5")], vid="g7u1-c2-match"),
        watch_out("Dropping a sign", "5 − (−3) is not 2. The two minus signs together make addition."),
        6)
    c3 = concept_block(
        "3. Rational numbers, not just integers",
        ["The same rules work for decimals and fractions.",
         "−3.5 + 1.2 = −2.3. 1/2 + (−1/4) = 1/4.",
         "Line up decimal points. Use a common denominator for fractions.",
         "3/4 − 5/4 = −2/4 = −1/2.",
         "Absolute value still means distance: |−4 + 1| = |−3| = 3.",
         "Estimate the sign first. If the negative piece is larger, the sum is negative."],
        lesson_figure(
            svg_fraction_bar(1, 2, "#86efac") + svg_fraction_bar(1, 4, "#fca5a5"),
            "1/2 + (−1/4)",
            "1/2 is two fourths. Adding −1/4 leaves 1/4.")
        + solved(1, "Find 1/2 + (−1/4).", ["Common denominator 4: 2/4 + (−1/4).", "2/4 − 1/4 = 1/4.", "Positive one-fourth."], "1/4")
        + step_reveal(["Rewrite subtraction as adding the opposite if needed.",
                       "Match places or denominators.", "Add using sign rules.", "Simplify."], vid="g7u1-c3-steps"),
        try_this("Guess the sign", "Before you compute −6.1 − 2.4, you already know it is more negative than −6."),
        11)
    c4 = concept_block(
        "4. Distance on the line",
        ["Distance between two numbers is the absolute value of their difference.",
         "Distance between −2 and 5 is |5 − (−2)| = 7. Distance is never negative.",
         "A rise of 10° from −4° lands at 6°. The change is +10; the distance is 10.",
         "From −7 to −2 is 5 units right. From −2 to −7 is 5 units left.",
         "Direction is the sign. Size is the absolute value.",
         "This is sixth-grade absolute value put to work in addition stories."],
        integer_line(-6, 6, marks=[(-2, "−2"), (5, "5")], title="Distance between −2 and 5",
                     caption="The points are 7 units apart. |5 − (−2)| = 7.")
        + solved(1, "How far apart are −2 and 5?", ["5 − (−2) = 7.", "Absolute value 7.", "7 units."], "7 units"),
        16)
    c5 = concept_block(
        "5. Real-world signed sums",
        ["Money: a debit of $20 then a deposit of $8 is −20 + 8 = −12.",
         "Football: −7 yards then +3 yards is −4 yards net.",
         "Elevation, temperature, and scores all use the same hops.",
         "Write each event as a signed number, then add.",
         "A gain of 12 then a loss of 15 is 12 + (−15) = −3.",
         "The story should still make sense: a net loss of 3, not a mystery 27."],
        hops_line(-7, [3], title="−7 yards then +3 yards",
                  caption="Start at −7. Hop right 3. Net is −4 yards.")
        + solved(1, "An account changes by −$20 then +$8. Net change?",
               ["−20 + 8 = −12.", "Net change is −$12.", "The account is $12 lower."], "−$12")
        + matching([("−4° then +10°", "6°"), ("−7 yd then +3 yd", "−4 yd"),
                    ("−$20 then +$8", "−$12"), ("+12 then −15", "−3")], vid="g7u1-c5-match"),
        21)
    c6 = concept_block(
        "6. Combining several signed numbers",
        ["Add left to right, or group positives and negatives, then combine.",
         "7 + (−2) + (−5) = 0. −12 + 5 + (−1) = −8.",
         "Keep a running total. A number-line sketch catches a dropped sign.",
         "If a number plus 4 is 1, the number is −3.",
         "Precision matters: −2.5 + 2.5 is exactly 0.",
         "Each sign stays with its number. 7 + 2 + 5 = 14 is a different problem."],
        hops_line(7, [-2, -5], title="7 + (−2) + (−5)", caption="From 7, left 2 to 5, then left 5 to 0.")
        + solved(1, "Find 7 + (−2) + (−5).", ["7 + (−2) = 5.", "5 + (−5) = 0.", "The sum is 0."], "0")
        + watch_out("Adding all the digits and guessing a sign", "Keep each sign glued to its number."),
        26)
    content = unit_shell(
        title,
        ["Add integers on a number line", "Rewrite subtraction as adding the opposite",
         "Include decimals and fractions", "Find distance with absolute value",
         "Solve signed stories", "Add a chain of signed numbers"],
        c1 + c2 + c3 + c4 + c5 + c6, practice_slots(31, 25))
    return title, description, content, _u1_questions()


# UNIT 2

def _u2_questions():
    items = [
        ("(−3) × 4 = ?", "−12", ["12", "−7", "1"], "Neg × pos = neg."),
        ("(−3) × (−4) = ?", "12", ["−12", "−7", "1"], "Neg × neg = pos."),
        ("5 × (−2) = ?", "−10", ["10", "3", "−7"], "Pos × neg = neg."),
        ("(−12) ÷ 3 = ?", "−4", ["4", "−15", "9"], "Neg ÷ pos = neg."),
        ("(−12) ÷ (−3) = ?", "4", ["−4", "36", "−15"], "Neg ÷ neg = pos."),
        ("12 ÷ (−3) = ?", "−4", ["4", "9", "−15"], "Pos ÷ neg = neg."),
        ("Two negatives multiply to a…", "positive", ["negative", "zero", "undefined"], "Two sign flips."),
        ("(−1)×(−1)×(−1) = ?", "−1", ["1", "0", "3"], "Odd count stays negative."),
        ("(−2/3)×(3/4) = ?", "−1/2", ["1/2", "−9/8", "6/12"], "Then apply the sign."),
        ("(−5)² = ?", "25", ["−25", "10", "−10"], "(−5)(−5)=25."),
        ("−5² = ?", "−25", ["25", "10", "−10"], "−(5²)=−25."),
        ("(−0.5)×8 = ?", "−4", ["4", "−8.5", "3.5"], "Half of 8, negative."),
        ("18 ÷ (−0.5) = ?", "−36", ["36", "−9", "9"], "÷ 1/2 doubles, then sign."),
        ("Stock drops $3/day for 4 days?", "−$12", ["$12", "−$7", "$1"], "4×(−3)."),
        ("(−2)×(−2)×(−2) = ?", "−8", ["8", "−6", "6"], "Three negatives."),
        ("0 × (−17) = ?", "0", ["−17", "17", "1"], "Zero times anything is 0."),
        ("(−9) ÷ 9 = ?", "−1", ["1", "0", "−9"], "Same size, different signs."),
        ("1/2 ÷ (−1/4) = ?", "−2", ["2", "−1/8", "1/8"], "(1/2)×(−4)."),
        ("(−3/5) ÷ (2/5) = ?", "−3/2", ["3/2", "−6/25", "−1"], "× 5/2."),
        ("If 3x = −12, x = ?", "−4", ["4", "−36", "9"], "Divide by 3."),
        ("Reciprocal of −2/5?", "−5/2", ["5/2", "2/5", "−2/5"], "Flip, keep the sign."),
        ("(−1.5)×(−2) = ?", "3", ["−3", "−0.5", "0.5"], "Neg × neg."),
        ("Descend 200 ft/min for 3 min?", "−600 ft", ["600 ft", "−203 ft", "200 ft"], "3×(−200)."),
        ("(−8) ÷ 2 ÷ (−2) = ?", "2", ["−2", "8", "−8"], "−4 then ÷ −2."),
        ("Which product is positive?", "(−4)×(−5)", ["(−4)×5", "4×(−5)", "(−1)×1"], "Two negatives."),
        ("−3 × 0.1 = ?", "−0.3", ["0.3", "−3.1", "2.9"], "Tenth of −3."),
        ("(−2/7)×(7/2) = ?", "−1", ["1", "−4/14", "0"], "Product −1."),
        ("4 × (−1/4) = ?", "−1", ["1", "0", "−4"], "Four negative fourths."),
        ("Pattern −2, 4, −8, 16. Next?", "−32", ["32", "−16", "8"], "×(−2)."),
        ("Same signs in a product give a…", "positive product", ["negative product", "zero", "undefined"], "Different signs: negative."),
    ]
    return _fill(_pack(items), 55, lambda i: mq(
        f"What is (−{i % 5 + 2}) × {i % 4 + 1}?",
        -(i % 5 + 2) * (i % 4 + 1),
        "Negative times positive is negative.",
        i,
        distractors=[(i % 5 + 2) * (i % 4 + 1), i % 5 + 2, -(i % 5 + 2)],
    ))


def build_unit2():
    title = "Seventh Grade Math Unit 2: Multiplying and Dividing Rational Numbers"
    description = "Multiply and divide integers and rationals, including negatives."
    c1 = concept_block(
        "1. Sign rules for multiply",
        ["Positive × positive is positive. Negative × negative is positive.",
         "Different signs make a negative product. (−3)×4 = −12.",
         "4 × (−3) is four hops of −3 starting at 0: land at −12.",
         "Even number of negative factors → positive. Odd → negative.",
         "(−1)×(−1)×(−1) = −1. Zero times anything is 0.",
         "The size is ordinary multiplication. The sign is a separate decision."],
        hops_line(0, [-3, -3, -3, -3], title="4 × (−3) as hops",
                  caption="Four hops of −3 starting at 0. You land at −12.")
        + solved(1, "Find (−3) × (−4).", ["Two negatives.", "Sizes: 12.", "Same signs → 12."], "12")
        + matching([("neg × pos", "negative"), ("neg × neg", "positive"),
                    ("pos × pos", "positive"), ("odd count of −", "negative product")], vid="g7u2-c1-match"),
        1)
    c2 = concept_block(
        "2. Sign rules for divide",
        ["Division uses the same sign rules as multiplication.",
         "(−12)÷3=−4. 12÷(−3)=−4. (−12)÷(−3)=4.",
         "Dividing is multiplying by the reciprocal.",
         "The reciprocal of −2/5 is −5/2. Keep the sign when you flip.",
         "(−9)÷9 = −1. Check by multiplying back.",
         "4 × (−3) = −12, so (−12) ÷ (−3) = 4."],
        hops_line(0, [-3, -3, -3, -3], title="(−12) ÷ (−3) = 4",
                  caption="Four hops of −3 make −12. So (−12) ÷ (−3) = 4.")
        + solved(1, "Find (−12) ÷ (−3).", ["Same signs → positive.", "12 ÷ 3 = 4.", "Check: 4 × (−3) = −12."], "4")
        + watch_out("Parentheses and exponents", "(−5)² is 25. −5² is −(5²) = −25."),
        6)
    c3 = concept_block(
        "3. Fractions and decimals with signs",
        ["(−2/3)×(3/4)=−1/2. Multiply tops and bottoms, then apply the sign.",
         "1/2 ÷ (−1/4) = (1/2)×(−4) = −2.",
         "(−0.5)×8 = −4. 18 ÷ (−0.5) = −36.",
         "Convert mixed numbers to improper fractions first.",
         "Cancel: (−2/7)×(7/2) = −1.",
         "Size is fraction arithmetic. Sign is the count of negatives."],
        lesson_figure(
            svg_fraction_bar(1, 2, "#86efac") + svg_fraction_bar(1, 4, "#fca5a5"),
            "1/2 ÷ (−1/4)",
            "1/2 is two copies of 1/4. Dividing by −1/4 gives −2.")
        + solved(1, "Compute (1/2) ÷ (−1/4).",
               ["Keep, change, flip: (1/2)×(−4/1).", "2, then the negative.", "−2."], "−2")
        + step_reveal(["Decide the sign.", "Multiply or divide the sizes.", "Attach the sign.", "Check."],
                      vid="g7u2-c3-steps"),
        11)
    c4 = concept_block(
        "4. Exponents and patterns",
        ["(−5)² = 25. −5² = −25 unless parentheses wrap the −5.",
         "Pattern −2, 4, −8, 16, … multiplies by −2. Next is −32.",
         "Repeated multiplication by a negative alternates the sign.",
         "This matters when you substitute a negative into x² versus −x².",
         "Write parentheses around a negative base for a power.",
         "Two negatives in a square make a positive."],
        integer_line(-8, 8, marks=[(-2, "−2"), (4, "4"), (-8, "−8")],
                     title="Pattern −2, 4, −8, …",
                     caption="Each term multiplies by −2. Next is 16, then −32.")
        + solved(1, "Compare (−5)² and −5².", ["(−5)² = 25.", "−5² = −25.", "They are opposites."], "25 versus −25")
        + matching([("(−5)²", "25"), ("−5²", "−25"), ("(−2)³", "−8"), ("four factors of −2", "16")], vid="g7u2-c4-match"),
        16)
    c5 = concept_block(
        "5. Signed rates in stories",
        ["A stock drops $3 per day for 4 days: 4×(−3)=−$12.",
         "A plane descends 200 ft/min for 3 min: −600 ft.",
         "Rates can be negative when the quantity decreases.",
         "If 3x = −12, then x = −4.",
         "Write the rate with a sign, then multiply by time.",
         "Four days of −3 should feel like a $12 loss, not a gain."],
        hops_line(0, [-3, -3, -3, -3], title="A stock drops $3 per day for 4 days",
                  caption="Four hops of −3. The change is −$12.")
        + solved(1, "A submarine dives 40 m/min for 5 min. Change in elevation?",
               ["Rate −40 m/min.", "5×(−40)=−200.", "−200 m."], "−200 m")
        + kid_tip("Rate × time", "Keep the sign on the rate. Time is usually positive."),
        21)
    c6 = concept_block(
        "6. Mix the four operations",
        ["(−8)÷2÷(−2) = (−4)÷(−2)=2. Left to right for × and ÷.",
         "4×(−1/4)=−1. (−1.5)×(−2)=3.",
         "Parentheses, then ×÷, then +− — same order as sixth grade.",
         "A long expression is a chain of small signed steps.",
         "If a result surprises you, count the negative signs.",
         "Even count in a pure product → positive. Odd → negative."],
        integer_line(-8, 8, marks=[(-8, "−8"), (-4, "÷2"), (2, "÷(−2)")],
                     title="(−8) ÷ 2 ÷ (−2)",
                     caption="Left to right: −8÷2=−4, then −4÷(−2)=2.")
        + solved(1, "Evaluate (−8) ÷ 2 ÷ (−2).", ["−8÷2=−4.", "−4÷−2=2.", "2."], "2")
        + try_this("Count the minuses", "Even count in a pure product → positive. Odd → negative."),
        26)
    content = unit_shell(
        title,
        ["Multiply with sign rules", "Divide with sign rules", "Include fractions and decimals",
         "Handle exponents and patterns", "Use signed rates", "Mix operations with negatives"],
        c1 + c2 + c3 + c4 + c5 + c6, practice_slots(31, 25))
    return title, description, content, _u2_questions()


# UNIT 3

def _u3_questions():
    items = [
        ("Proportional means…", "y = kx (through the origin)", ["any straight line", "any table", "only percents"], "k = y/x."),
        ("If y = 2x, k is…", "2", ["1/2", "0", "x"], "k = y/x."),
        ("A proportion graph goes through…", "(0, 0)", ["(1, 0)", "(0, 1)", "(1, 1)"], "Zero maps to zero."),
        ("3/4 = 9/x. x = ?", "12", ["7", "36", "13"], "Scale by 3."),
        ("2/5 = 8/x. x = ?", "20", ["11", "10", "40"], "2x=40."),
        ("180 km in 3 h. Unit rate?", "60 km/h", ["540 km/h", "183 km/h", "30 km/h"], "180÷3."),
        ("4 items cost $10. 10 items cost…", "$25", ["$14", "$40", "$20"], "$2.50 each."),
        ("k = 3, x = 5. y = ?", "15", ["8", "3/5", "2"], "y=kx."),
        ("(1,4), (2,8), (3,12). k = ?", "4", ["2", "3", "1"], "y/x=4."),
        ("NOT proportional?", "(1,3), (2,5)", ["(1,2),(2,4)", "(3,6),(5,10)", "(0,0),(4,8)"], "3≠2.5."),
        ("Map 1 cm : 8 km. 5 cm is…", "40 km", ["13 km", "8 km", "5 km"], "×8."),
        ("Recipe 2:3. 10 cups flour → sugar?", "15 cups", ["13 cups", "6 cups", "5 cups"], "×5."),
        ("5/8 = n/24. n = ?", "15", ["29", "8", "40"], "5×24=8n."),
        ("y=10 when x=2, proportional. y at x=7?", "35", ["15", "12", "70"], "k=5."),
        ("Line through (0,2) and (1,4) is…", "not proportional", ["proportional", "a circle", "k=0"], "Misses origin."),
        ("50 mph for 3 hours. Distance?", "150 miles", ["53 miles", "47 miles", "15 miles"], "d=rt."),
        ("Scale 1:20. 4 cm drawing is…", "80 cm real", ["24 cm", "5 cm", "16 cm"], "×20."),
        ("5 lb for $12. Per pound?", "$2.40", ["$17", "$2", "$0.42"], "12÷5."),
        ("Which is proportional?", "y = 0.5x", ["y = 0.5x + 1", "y = x²", "y = 5 + x"], "No extra constant."),
        ("(2,10) and (5,y) proportional. y=?", "25", ["13", "15", "7"], "k=5."),
        ("Scale by 2.5. 8 oz becomes…", "20 oz", ["10.5 oz", "16 oz", "5.5 oz"], "×2.5."),
        ("4/6 = 10/15 because both equal…", "2/3", ["4/10", "6/15", "1"], "Simplify."),
        ("8 pencils for $6. One costs…", "$0.75", ["$2", "$14", "$6"], "6÷8."),
        ("(0,0), (2,6), (4,12). k=?", "3", ["6", "2", "12"], "6/2=3."),
        ("7/x = 21/15. x=?", "5", ["3", "21", "35"], "7×15=21x."),
        ("A unit rate is per…", "one", ["hundred", "ten", "zero"], "Per 1 hour, per 1 item."),
        ("Double x in a proportion and y…", "doubles", ["stays", "halves", "adds 2"], "Constant ratio."),
        ("2 L every 5 min. In 20 min?", "8 L", ["7 L", "10 L", "40 L"], "×4."),
        ("4/x = 10/25. x=?", "10", ["39", "4", "2.5"], "4×25=10x."),
        ("$3 per mile, no extra fee, 6 miles?", "$18", ["$21", "$9", "$3"], "Pure proportion."),
    ]
    return _fill(_pack(items), 55, lambda i: mq(
        f"If y = 3x and x = {i % 8 + 1}, what is y?",
        3 * (i % 8 + 1), "Multiply x by 3.", i))


def build_unit3():
    title = "Seventh Grade Math Unit 3: Proportional Relationships"
    description = "Identify proportions, find unit rates and k, and solve proportions."
    c1 = concept_block(
        "1. What proportional means",
        ["Two quantities are proportional when y/x is constant: y = kx.",
         "k is the constant of proportionality — the unit rate when x is 1.",
         "(1,4), (2,8), (3,12) has k=4. (1,3), (2,5) does not.",
         "y=0.5x is proportional. y=0.5x+1 is not.",
         "If you double x, y doubles.",
         "A (0,0) pair always fits a true proportion."],
        proportional_graph(2, title="y = 2x goes through the origin")
        + solved(1, "Table (1,4), (2,8), (3,12). What is k?", ["k=y/x.", "4/1=8/2=12/3=4.", "k=4."], "4")
        + phet_box("prop"),
        kid_tip("Check y ÷ x", "If two rows match, check a third."),
        1)
    c2 = concept_block(
        "2. Graphs through the origin",
        ["A proportional graph is a straight line through (0,0).",
         "Steepness is k. Steeper means a larger unit rate.",
         "A line through (0,2) is not proportional.",
         "(0,0), (2,6), (4,12) lie on y=3x.",
         "Read k from a point: k=y/x (x≠0).",
         "The origin is required, not optional."],
        proportional_graph(3, title="k = 3", caption="(1,3), (2,6), (3,9) sit on a line through the origin.")
        + matching([("y=2x", "k=2"), ("through (0,0)", "proportional graph"),
                    ("y=2x+1", "not proportional"), ("(2,10) with k=5", "y=5x")], vid="g7u3-c2-match"),
        watch_out("Any straight line", "A line that misses the origin is not a proportion."),
        6)
    c3 = concept_block(
        "3. Unit rates",
        ["A unit rate is the amount per 1. 180 km in 3 h → 60 km/h.",
         "5 lb for $12 → $2.40 per pound.",
         "Unit rate is k. Write the units.",
         "8 pencils for $6 is $0.75 each.",
         "If it is not yet per 1, divide.",
         "Unit rates compare deals and speeds fairly."],
        double_number_line("km", [0, 60, 120, 180], "h", [0, 1, 2, 3],
                           title="Constant speed 60 km per hour",
                           caption="Every hour adds 60 km. The unit rate is 60 km/h.")
        + solved(1, "180 km in 3 hours. Unit rate?", ["180÷3=60.", "Per 1 hour.", "60 km/h."], "60 km/h")
        + phet_box("unit_rates"),
        11)
    c4 = concept_block(
        "4. Solving proportions",
        ["A proportion is two equal ratios: 3/4=9/x.",
         "Scale: 3×3=9 so 4×3=12. Or cross-multiply: 3x=36.",
         "5/8=n/24 → n=15. 7/x=21/15 → x=5.",
         "Keep quantities in the same order on both sides.",
         "Check by simplifying both ratios.",
         "Recipes and maps are almost always proportions."],
        tape_diagram([("small", [("#818cf8", 3, "3")]), ("scaled", [("#6366f1", 9, "9")])],
                     title="3 scales to 9 (factor 3)", caption="Multiply the 4 by the same 3. x=12.")
        + solved(1, "Solve 3/4 = 9/x.", ["Factor from 3 to 9 is 3.", "4×3=12.", "x=12."], "12")
        + step_reveal(["Write equal ratios.", "Scale or cross-multiply.", "Solve.", "Check."], vid="g7u3-c4-steps"),
        16)
    c5 = concept_block(
        "5. Scale drawings and recipes",
        ["Map 1 cm : 8 km. 5 cm → 40 km.",
         "Scale 1:20 means real = 20 × drawing.",
         "Recipe 2:3, 10 cups flour → 15 cups sugar.",
         "Factor 2.5 turns 8 oz into 20 oz.",
         "Every length multiplies by the same k.",
         "1:n means the real object is n times larger."],
        scale_drawing("Scale factor 4",
                      "Every length multiplies by the same k. A map 1 cm : 8 km uses k=8, so 5 cm is 40 km.")
        + solved(1, "Map 1 cm : 8 km. How far is 5 cm?", ["×8.", "5×8=40.", "40 km."], "40 km")
        + matching([("1 cm:8 km, 5 cm", "40 km"), ("1:20, 4 cm", "80 cm real"),
                    ("2:3 and 10 flour", "15 sugar"), ("k=2.5 on 8 oz", "20 oz")], vid="g7u3-c5-match"),
        21)
    c6 = concept_block(
        "6. Constant-rate stories",
        ["d = rt when speed is constant: 50 mph × 3 h = 150 miles.",
         "2 L every 5 min → 8 L in 20 min.",
         "If y=10 when x=2, then k=5, so x=7 gives y=35.",
         "Write y=kx, find k, then evaluate.",
         "A taxi with a $2 flag drop plus $3/mile is not proportional.",
         "Ask: constant per one, and nothing extra at zero?"],
        double_number_line("mi", [0, 50, 100, 150], "h", [0, 1, 2, 3],
                           title="Constant speed 50 miles per hour",
                           caption="50 mph for 3 hours is 150 miles. Distance = rate × time.")
        + solved(1, "y proportional to x. y=10 when x=2. Find y when x=7.",
               ["k=10/2=5.", "y=5x.", "y=35."], "35")
        + try_this("Zero test", "If x is 0, is y 0? If not, it is not a proportion."),
        26)
    content = unit_shell(
        title,
        ["Know what proportional means", "Read graphs through the origin", "Find unit rates",
         "Solve proportions", "Use scales and recipes", "Model constant-rate stories"],
        c1 + c2 + c3 + c4 + c5 + c6, practice_slots(31, 25))
    return title, description, content, _u3_questions()


# UNIT 4

def _u4_questions():
    items = [
        ("25% of 80 is…", "20", ["25", "105", "4"], "0.25×80."),
        ("$40 item, 20% off. Discount?", "$8", ["$20", "$32", "$48"], "0.2×40."),
        ("Sale price after 20% off $40?", "$32", ["$8", "$20", "$48"], "40−8."),
        ("8% tax on $50. Tax amount?", "$4", ["$8", "$54", "$42"], "0.08×50."),
        ("Total with 8% tax on $50?", "$54", ["$4", "$58", "$42"], "50+4."),
        ("40 to 50. Percent increase?", "25%", ["10%", "125%", "20%"], "10/40."),
        ("50 to 40. Percent decrease?", "20%", ["25%", "10%", "80%"], "10/50."),
        ("Simple interest $200 at 5% for 3 years?", "$30", ["$15", "$230", "$8"], "I=Prt."),
        ("30% markup on $20. Selling price?", "$26", ["$6", "$50", "$23"], "20+6."),
        ("12% of $400 commission?", "$48", ["$12", "$388", "$52"], "0.12×400."),
        ("15 is what percent of 60?", "25%", ["15%", "45%", "60%"], "15/60."),
        ("30 is 25% of what?", "120", ["7.5", "55", "100"], "30÷0.25."),
        ("10% increase on 80?", "88", ["90", "70", "8"], "80+8."),
        ("10% decrease on 80?", "72", ["70", "88", "8"], "80−8."),
        ("Error 2 cm on 50 cm. Percent error?", "4%", ["2%", "25%", "52%"], "2/50."),
        ("15% tip on $80?", "$12", ["$15", "$8", "$68"], "0.15×80."),
        ("Double is a…", "100% increase", ["200% increase", "50% increase", "2% increase"], "Change equals original."),
        ("Half off is a…", "50% decrease", ["100% decrease", "2% decrease", "150% off"], "You pay 50%."),
        ("×1.08 means…", "an 8% increase", ["108% off", "8% off", "a decrease"], "100%+8%."),
        ("×0.75 means…", "25% off", ["75% off", "0.75% off", "an increase"], "You pay 75%."),
        ("$60 after 25% off. Original?", "$80", ["$45", "$85", "$15"], "60 is 75%."),
        ("Interest on $500 at 4% for 1 year?", "$20", ["$4", "$480", "$524"], "500×0.04."),
        ("Two 10% increases on 100?", "121", ["120", "110", "100"], "×1.1×1.1."),
        ("20% of 20% of 100?", "4", ["40", "20", "80"], "0.2×0.2×100."),
        ("Population 200 grows 15%. New size?", "230", ["215", "185", "30"], "200+30."),
        ("$12 off $48 is what percent?", "25%", ["12%", "36%", "52%"], "12/48."),
        ("1% of 450?", "4.5", ["45", "1", "449"], "÷100."),
        ("5% of 80?", "4", ["8", "5", "40"], "Half of 10%."),
        ("6% tax on $25. Total?", "$26.50", ["$1.50", "$31", "$24"], "25+1.50."),
        ("9 is what percent of 12?", "75%", ["9%", "12%", "25%"], "9/12."),
    ]
    return _fill(_pack(items), 55, lambda i: mq(
        f"What is 10% of {10 * (i % 9 + 2)}?", i % 9 + 2, "10% is one tenth.", i))


def build_unit4():
    title = "Seventh Grade Math Unit 4: Percents in the Real World"
    description = "Percent increase and decrease, tax, tips, markup, simple interest, and percent error."
    c1 = concept_block(
        "1. Percent of a number",
        ["Part = percent × whole. 25% of 80 is 20.",
         "15 is what percent of 60? 25%. 30 is 25% of what? 120.",
         "1% is ÷100. 10% is ÷10. 5% is half of 10%.",
         "75% is 3/4. 9 is 75% of 12.",
         "Write the percent as a decimal or fraction first.",
         "A percent bar still helps you see part versus whole."],
        percent_bar(25, 80, title="25% of 80")
        + solved(1, "Find 15% of $80.", ["10% of 80 is 8. 5% is 4.", "8+4=12.", "$12."], "$12"),
        kid_tip("Build from 10% and 1%", "Most common percents are combinations of those two."),
        1)
    c2 = concept_block(
        "2. Percent increase and decrease",
        ["Percent change = (new − original) / original.",
         "40 to 50 is 10/40 = 25% increase.",
         "50 to 40 is 10/50 = 20% decrease. The bases differ.",
         "10% up on 80 is 88. 10% down on 80 is 72.",
         "Double is a 100% increase. Half off is a 50% decrease.",
         "×1.08 for an 8% increase. ×0.75 for 25% off."],
        percent_bar(25, 40, title="A $10 rise on $40 is 25%",
                    caption="Change 10, original 40. 10÷40=25%.")
        + solved(1, "Price from $40 to $50. Percent increase?", ["Change 10.", "10/40=0.25.", "25%."], "25%")
        + watch_out("Using the new amount as the base", "50 to 40 is 20%, not 25%. Divide by the original."),
        6)
    c3 = concept_block(
        "3. Tax, tips, and discounts",
        ["Tax and tip are added. Discount is subtracted.",
         "8% tax on $50 is $4. Total $54.",
         "20% off $40 → sale $32. Or ×0.80.",
         "15% tip on $80 is $12.",
         "Paid $60 after 25% off → original $80, because 60 is 75%.",
         "Ask: extra amount, or new total?"],
        percent_bar(20, 40, title="20% off $40",
                    caption="20% of $40 is $8. Sale price 40 − 8 = $32.")
        + solved(1, "$40 shirt, 20% off. Sale price?", ["0.20×40=8.", "40−8=32.", "Or 40×0.8=32."], "$32")
        + matching([("20% off $40", "$32"), ("8% tax on $50", "$54 total"),
                    ("15% of $80", "$12"), ("paid $60 after 25% off", "original $80")], vid="g7u4-c3-match"),
        11)
    c4 = concept_block(
        "4. Markup, markdown, commission",
        ["Markup from cost: 30% on $20 → selling price $26.",
         "Markdown from list: $12 off $48 is 25%.",
         "Commission 12% of $400 is $48.",
         "Same percent-of skill, business words.",
         "Name the original (cost or list) before you compute.",
         "Selling price = cost × (1 + markup rate)."],
        percent_bar(30, 20, title="30% markup on $20",
                    caption="30% of $20 is $6. Selling price 20 + 6 = $26.")
        + solved(1, "30% markup on a $20 cost. Selling price?",
               ["30% of 20 is 6.", "20+6=26.", "$26."], "$26")
        + step_reveal(["Name the original.", "Find that percent.", "Add or subtract.", "Label money."], vid="g7u4-c4-steps"),
        16)
    c5 = concept_block(
        "5. Simple interest",
        ["I = P × r × t. r is a decimal. t is years.",
         "$200 at 5% for 3 years: I=200×0.05×3=$30.",
         "$500 at 4% for 1 year: $20. Total value is P+I.",
         "6 months is t=0.5 year.",
         "Simple interest does not compound.",
         "5% inside the formula is 0.05, not 5."],
        percent_bar(5, 200, title="5% of $200 is one year's interest",
                    caption="Three years of simple interest: three copies of $10, so $30.")
        + solved(1, "Interest on $200 at 5% for 3 years?", ["r=0.05.", "I=200×0.05×3=30.", "$30."], "$30"),
        try_this("Percent to decimal", "5% is 0.05 inside I=Prt."),
        21)
    c6 = concept_block(
        "6. Percent error and chained percents",
        ["Percent error = |measured−actual| / actual. 2 cm off 50 cm is 4%.",
         "Two 10% increases on 100: 100×1.1×1.1=121, not 120.",
         "20% of 20% of 100 is 4, not 40.",
         "200 grows 15% → 230.",
         "Write each chained step as ×(1±p).",
         "Two 10% bumps land a little above 120."],
        percent_bar(4, 50, title="2 cm off 50 cm is 4% error",
                    caption="Percent error = 2 ÷ 50 = 4%.")
        + solved(1, "2 cm off a 50 cm true length. Percent error?", ["2/50=0.04.", "4%.", "Size over actual."], "4%")
        + watch_out("Adding chained percents", "10% then 10% is ×1.1 twice = 21% more, not 20%."),
        26)
    content = unit_shell(
        title,
        ["Find a percent of a number", "Percent increase and decrease", "Tax, tips, discounts",
         "Markup, markdown, commission", "Simple interest", "Percent error and chained percents"],
        c1 + c2 + c3 + c4 + c5 + c6, practice_slots(31, 25))
    return title, description, content, _u4_questions()



