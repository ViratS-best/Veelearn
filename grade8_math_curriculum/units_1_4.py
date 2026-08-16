"""Eighth Grade Math units 1–4: exponents, linear equations, slope, functions."""

from .common import (
    concept_block, solved, practice_slots, unit_shell, kid_tip, watch_out, try_this,
    step_reveal, matching, phet_box, balance_scale, sci_shift, slope_line,
    four_quadrant_plane, mq, renumber,
)


def _fill(qs, need, factory):
    while len(qs) < need:
        qs.append(factory(len(qs) + 1))
    return renumber(qs[:need])


def _pack(items):
    return [mq(t, a, e, i, distractors=d) for i, (t, a, d, e) in enumerate(items, 1)]


def _u1_questions():
    items = [
        ("3² × 3⁴ = ?", "3⁶", ["3⁸", "3²", "9⁶"], "Add exponents: 2+4=6."),
        ("5⁷ ÷ 5³ = ?", "5⁴", ["5¹⁰", "5³", "5²¹"], "Subtract exponents."),
        ("(2³)⁴ = ?", "2¹²", ["2⁷", "8⁴", "2⁶⁴"], "Multiply exponents: 3×4=12."),
        ("7⁰ = ?", "1", ["0", "7", "70"], "Nonzero number to the 0 power is 1."),
        ("2⁻³ = ?", "1/8", ["−8", "8", "−1/8"], "2⁻³ = 1/2³ = 1/8."),
        ("(3 × 10⁴)(2 × 10³) = ?", "6 × 10⁷", ["5 × 10⁷", "6 × 10¹²", "6 × 10¹"], "3×2 and 4+3."),
        ("4.5 × 10³ in standard form?", "4500", ["45", "0.0045", "450"], "Move 3 places right."),
        ("0.0032 in scientific notation?", "3.2 × 10⁻³", ["3.2 × 10³", "32 × 10⁻⁴", "0.32 × 10⁻²"], "3.2 and three left hops."),
        ("√81 = ?", "9", ["8", "40.5", "18"], "9×9=81."),
        ("√50 is between…", "7 and 8", ["5 and 6", "8 and 9", "6 and 7"], "7²=49, 8²=64."),
        ("Which is irrational?", "√2", ["√16", "0.25", "3/5"], "√2 does not terminate or repeat."),
        ("4³ = ?", "64", ["12", "16", "81"], "4×4×4."),
        ("x⁵ · x = ?", "x⁶", ["x⁵", "x⁴", "5x"], "x is x¹."),
        ("(10²)³ = ?", "10⁶", ["10⁵", "10⁸", "1000"], "2×3=6."),
        ("3.2 × 10⁴ = ?", "32000", ["3200", "0.00032", "32"], "Four places right."),
        ("6.1 × 10⁻² = ?", "0.061", ["610", "0.61", "6.1"], "Two places left."),
        ("(4 × 10⁵) ÷ (2 × 10²) = ?", "2 × 10³", ["2 × 10⁷", "8 × 10³", "2 × 10²·⁵"], "4/2 and 5−2."),
        ("5⁻² = ?", "1/25", ["−25", "25", "−1/25"], "1/5²."),
        ("√121 = ?", "11", ["12", "60.5", "21"], "11×11."),
        ("2⁴ = ?", "16", ["8", "6", "32"], "2×2×2×2."),
        ("(−3)² = ?", "9", ["−9", "6", "−6"], "Parentheses wrap the negative."),
        ("−3² = ?", "−9", ["9", "6", "−6"], "Square 3 first, then the minus."),
        ("10⁰ = ?", "1", ["0", "10", "100"], "Same rule as 7⁰."),
        ("Which is larger: 4.1×10³ or 3.9×10⁴?", "3.9 × 10⁴", ["4.1 × 10³", "they are equal", "cannot tell"], "Compare exponents first."),
        ("√9 + √16 = ?", "7", ["5", "25", "√25"], "3+4."),
        ("(2x³)(5x²) = ?", "10x⁵", ["7x⁵", "10x⁶", "10x"], "2×5 and 3+2."),
        ("x⁸ ÷ x² = ?", "x⁶", ["x⁴", "x¹⁰", "x¹⁶"], "8−2."),
        ("A cube's volume 8 has edge…", "2", ["4", "16", "64"], "2³=8."),
        ("3.0 × 10⁸ is about the speed of light in m/s. That is…", "300,000,000", ["30,000,000", "0.00000003", "3,080"], "Eight places."),
        ("(1/2)⁻¹ = ?", "2", ["−2", "1/2", "−1/2"], "Flip the fraction."),
    ]
    return _fill(_pack(items), 80, lambda i: mq(
        f"What is 2^{i % 4 + 2}?",
        2 ** (i % 4 + 2),
        "Repeated multiplication of 2.",
        i,
        distractors=[2 * (i % 4 + 2), (i % 4 + 2) ** 2, 2 ** (i % 4 + 2) + 2],
    ))


def build_unit1():
    title = "Eighth Grade Math Unit 1: Exponents and Scientific Notation"
    description = "Use exponent laws, square roots, and scientific notation for very large and very small numbers."
    c1 = concept_block(
        "1. What an exponent does",
        ["aⁿ means n factors of a. 4³ = 4×4×4 = 64. 2⁴ = 16.",
         "(−3)² = 9 because the negative is inside the power. −3² = −9 because you square 3 first.",
         "A square root undoes a square: √81 = 9 because 9² = 81. √121 = 11.",
         "√50 sits between 7 and 8 because 7² = 49 and 8² = 64.",
         "√2 is irrational: it does not terminate or repeat. √16 is 4, which is rational.",
         "A cube with volume 8 has edge 2, because 2³ = 8."],
        solved(1, "Compare (−3)² and −3².",
               ["(−3)² = (−3)×(−3) = 9.", "−3² = −(3×3) = −9.", "Parentheses change the sign story."],
               "9 versus −9")
        + matching([("4³", "64"), ("2⁴", "16"), ("√81", "9"), ("7⁰", "1")], vid="g8u1-c1-match"),
        kid_tip("Read the parentheses", "The minus is only powered if it is inside."),
        1)
    c2 = concept_block(
        "2. Product, quotient, and power rules",
        ["Same base, multiply: add exponents. 3² × 3⁴ = 3⁶.",
         "Same base, divide: subtract exponents. 5⁷ ÷ 5³ = 5⁴.",
         "A power of a power: multiply exponents. (2³)⁴ = 2¹².",
         "x⁵ · x = x⁶ because a bare x is x¹.",
         "(2x³)(5x²) = 10x⁵. Multiply the coefficients, add the exponents.",
         "x⁸ ÷ x² = x⁶. These rules are how algebra compresses repeated multiplication."],
        solved(1, "Simplify (2³)⁴.",
               ["Power of a power: multiply 3×4.", "That is 12.", "2¹², not 2⁷."], "2¹²")
        + step_reveal(["Check the bases match.", "Decide: × add, ÷ subtract, power multiply.",
                       "Handle coefficients separately.", "Write one base with one exponent."],
                      vid="g8u1-c2-steps")
        + phet_box("expr"),
        6)
    c3 = concept_block(
        "3. Zero and negative exponents",
        ["Any nonzero number to the 0 power is 1. 7⁰ = 1 and 10⁰ = 1.",
         "A negative exponent is a reciprocal: 2⁻³ = 1/2³ = 1/8. 5⁻² = 1/25.",
         "(1/2)⁻¹ = 2. You flip the fraction.",
         "Do not treat 2⁻³ as −8. The minus is in the exponent, not in front of the 8.",
         "x⁻n = 1/xⁿ only when x is not 0.",
         "These two rules let scientific notation slide left and right."],
        solved(1, "Write 2⁻³ as a fraction.",
               ["Negative exponent means reciprocal.", "2³ = 8.", "1/8."], "1/8")
        + watch_out("A negative exponent is not a negative answer", "2⁻³ is 1/8, not −8."),
        11)
    c4 = concept_block(
        "4. Scientific notation",
        ["Scientific notation is a × 10ⁿ where 1 ≤ |a| < 10.",
         "3.2 × 10⁴ = 32,000. A positive exponent on 10 makes a large number.",
         "3.2 × 10⁻² = 0.032. A negative exponent makes a small number.",
         "0.0032 = 3.2 × 10⁻³. Count the hops of the decimal point.",
         "3.0 × 10⁸ is 300,000,000 — about the speed of light in meters per second.",
         "Compare 4.1×10³ and 3.9×10⁴ by the exponent first. 10⁴ wins."],
        sci_shift()
        + solved(1, "Write 4.5 × 10³ in standard form.",
                 ["Positive 3: three hops right.", "4.5 → 45 → 450 → 4500.", "4500."], "4500"),
        16)
    c5 = concept_block(
        "5. Compute in scientific notation",
        ["Multiply: (3×10⁴)(2×10³) = 6×10⁷. Multiply the leading numbers, add the exponents.",
         "Divide: (4×10⁵)÷(2×10²) = 2×10³. Divide leadings, subtract exponents.",
         "If the leading part leaves the 1-to-10 window, adjust: 12×10³ = 1.2×10⁴.",
         "This is how you handle planets, cells, and computer bits without a wall of zeros.",
         "Keep one digit (plus decimals) in front of the ×10.",
         "Estimate first: 10⁴ times 10³ is about 10⁷."],
        solved(1, "Compute (3 × 10⁴)(2 × 10³).",
               ["3×2=6.", "4+3=7.", "6 × 10⁷."], "6 × 10⁷")
        + matching([("(3×10⁴)(2×10³)", "6×10⁷"), ("(4×10⁵)÷(2×10²)", "2×10³"),
                    ("4.5×10³", "4500"), ("3.2×10⁻³", "0.0032")], vid="g8u1-c5-match"),
        21)
    c6 = concept_block(
        "6. Roots on the number line",
        ["Perfect squares: 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121.",
         "√9 + √16 = 3+4 = 7, not √25.",
         "Numbers like √2 and √10 are irrational. You can still place them between two integers.",
         "√50 is just past 7, because 49 is 7².",
         "In later units, c = √(a²+b²) for a right triangle. The root has to make sense as a length.",
         "A calculator decimal is an approximation. Leave √2 as √2 when the problem wants exact."],
        solved(1, "Between which two whole numbers is √50?",
               ["7²=49 and 8²=64.", "50 is just after 49.", "Between 7 and 8."], "7 and 8")
        + try_this("Bracket the square", "Find two perfect squares that trap the number, then name those roots."),
        26)
    content = unit_shell(
        title,
        ["Powers and roots", "Product, quotient, power rules", "Zero and negative exponents",
         "Scientific notation", "Compute with 10ⁿ", "Place roots on the number line"],
        c1 + c2 + c3 + c4 + c5 + c6, practice_slots(31, 50), "unit-1-exponents.mp4")


def _u2_questions():
    items = [
        ("3(2x − 1) − 4 = 5x + 7. x = ?", "14", ["7", "11", "4"], "6x−7=5x+7, x=14."),
        ("(x + 2)/3 = 4. x = ?", "10", ["6", "12", "2"], "x+2=12."),
        ("2(x − 3) = x + 5. x = ?", "11", ["2", "8", "−1"], "2x−6=x+5."),
        ("5 − 2(x + 1) = 9. x = ?", "−3", ["3", "2", "−2"], "5−2x−2=9."),
        ("x/4 + 3 = 7. x = ?", "16", ["4", "10", "28"], "x/4=4."),
        ("4(x + 1) = 2(x + 7). x = ?", "5", ["3", "6", "11"], "4x+4=2x+14."),
        ("−3x + 8 = 2x − 7. x = ?", "3", ["−3", "15", "1"], "8+7=5x."),
        ("(2x − 4)/2 = x − 3. How many solutions?", "none", ["infinitely many", "one: x=1", "two"],
         "(2x−4)/2 = x−2, so x−2 = x−3, which is −2 = −3. Contradiction."),
        ("A number is a solution when…", "it makes the equation true", ["it is positive", "it is x", "it is even"], "Substitute to check."),
        ("2x + 3x − 7 = 18. x = ?", "5", ["25", "11", "3"], "5x=25."),
        ("3 − x = 2x + 9. x = ?", "−2", ["2", "6", "−6"], "3−9=3x."),
        ("0.5x = 9. x = ?", "18", ["4.5", "9.5", "8.5"], "×2."),
        ("2(3x + 1) = 4x + 10. x = ?", "4", ["2", "8", "5"], "6x+2=4x+10."),
        ("x/2 − 3 = 1. x = ?", "8", ["−4", "2", "4"], "x/2=4."),
        ("5(x − 2) = 3x + 4. x = ?", "7", ["2", "6", "9"], "5x−10=3x+4."),
        ("If both sides become 4=4, the equation has…", "infinitely many solutions", ["no solution", "x=4 only", "x=0"], "An identity."),
        ("If both sides become 4=9, the equation has…", "no solution", ["infinitely many", "x=4", "x=9"], "A contradiction."),
        ("Clear (x+1)/2 = 5 by…", "multiplying both sides by 2", ["dividing by 2", "adding 2", "×1/2"], "Undo the denominator."),
        ("−(x − 4) = 10. x = ?", "−6", ["6", "14", "−14"], "−x+4=10."),
        ("6 = 2(x − 1) + 4. x = ?", "2", ["5", "3", "1"], "6=2x−2+4."),
        ("3x + 2 = 3x − 5 has…", "no solution", ["every x", "x=0", "x=7/0"], "2=−5 is false."),
        ("2(x + 4) − x = 9. x = ?", "1", ["5", "17", "−1"], "x+8=9."),
        ("(3x)/5 = 6. x = ?", "10", ["2", "15", "18"], "3x=30."),
        ("4 − 3x = x + 16. x = ?", "−3", ["3", "5", "−5"], "4−16=4x."),
        ("A two-step check for x=14 in 6x−7 vs 5x+7: 77 and…", "77", ["70", "84", "14"], "Both sides 77."),
        ("Distribute −2(x+1).", "−2x − 2", ["−2x + 1", "2x − 2", "−2x + 2"], "Minus hits both terms."),
        ("7 = 7 is true for…", "every number", ["no number", "only 7", "only 0"], "Identity."),
        ("x + x + x = 24. x = ?", "8", ["24", "12", "6"], "3x=24."),
        ("2x − (x − 5) = 9. x = ?", "4", ["14", "2", "7"], "2x−x+5=9."),
        ("Half of (x−4) is 6. x = ?", "16", ["8", "2", "10"], "x−4=12."),
    ]
    return _fill(_pack(items), 80, lambda i: mq(
        f"Solve 3x − 1 = {3 * (i % 7 + 2) - 1}.",
        i % 7 + 2,
        "Add 1, then divide by 3.",
        i,
    ))


def build_unit2():
    title = "Eighth Grade Math Unit 2: Linear Equations in One Variable"
    description = "Solve multi-step linear equations with distribute, fractions, and variables on both sides. Detect identities and contradictions."
    c1 = concept_block(
        "1. Multi-step with distribute",
        ["Clear parentheses first. 3(2x − 1) − 4 = 5x + 7 becomes 6x − 3 − 4 = 5x + 7.",
         "6x − 7 = 5x + 7. Subtract 5x: x − 7 = 7. Add 7: x = 14.",
         "2(x − 3) = x + 5 → 2x − 6 = x + 5 → x = 11.",
         "Minus in front of a group hits every term: −(x − 4) = −x + 4.",
         "Combine like terms before you move pieces across the equals sign.",
         "Check in the original, not in a half-simplified line."],
        balance_scale("3(2x − 1) − 4", "5x + 7", title="Both sides stay equal")
        + solved(1, "Solve 3(2x − 1) − 4 = 5x + 7.",
                 ["Distribute: 6x − 3 − 4 = 5x + 7.", "6x − 7 = 5x + 7, so x = 14.",
                  "Check: 6(14)−7=77 and 5(14)+7=77."], "14")
        + phet_box("eq"),
        kid_tip("Distribute the minus", "−2(x+1) is −2x − 2, not −2x + 1."),
        1)
    c2 = concept_block(
        "2. Variables on both sides",
        ["Collect x-terms on one side and numbers on the other.",
         "−3x + 8 = 2x − 7 → add 3x: 8 = 5x − 7 → 15 = 5x → x = 3.",
         "4(x + 1) = 2(x + 7) → 4x + 4 = 2x + 14 → 2x = 10 → x = 5.",
         "3 − x = 2x + 9 → 3 − 9 = 3x → x = −2.",
         "Move the smaller x-coefficient when you want a positive coefficient.",
         "A check that fails means a combine or a sign slipped."],
        solved(1, "Solve 4(x + 1) = 2(x + 7).",
               ["4x + 4 = 2x + 14.", "2x = 10.", "x = 5."], "5")
        + matching([("−3x+8=2x−7", "x=3"), ("2(x−3)=x+5", "x=11"),
                    ("3−x=2x+9", "x=−2"), ("x/4+3=7", "x=16")], vid="g8u2-c2-match"),
        6)
    c3 = concept_block(
        "3. Fractions and decimals",
        ["Clear a denominator by multiplying both sides. (x+2)/3 = 4 → x+2 = 12 → x = 10.",
         "(3x)/5 = 6 → 3x = 30 → x = 10.",
         "x/2 − 3 = 1 → x/2 = 4 → x = 8.",
         "0.5x = 9 → x = 18. Decimals are fractions in a different outfit.",
         "If two denominators appear, multiply by a common multiple so they both vanish.",
         "Do not divide only one term of a sum."],
        solved(1, "Solve (x + 2)/3 = 4.",
               ["Multiply both sides by 3.", "x + 2 = 12.", "x = 10."], "10")
        + step_reveal(["Clear parentheses.", "Clear denominators.", "Collect x.", "Check."],
                      vid="g8u2-c3-steps"),
        11)
    c4 = concept_block(
        "4. Identities and contradictions",
        ["Sometimes the x-terms cancel.",
         "If you are left with 7 = 7, every number works: infinitely many solutions. The two sides were the same expression.",
         "If you are left with 4 = 9, no number works: no solution. The sides cannot be equal.",
         "(2x − 4)/2 = x − 3 simplifies to x − 2 = x − 3, so −2 = −3. No solution.",
         "3x + 2 = 3x − 5 is also no solution.",
         "One solution is still the usual case. Name which of the three you have."],
        solved(1, "(2x − 4)/2 = x − 3. How many solutions?",
               ["Left side is x − 2.", "x − 2 = x − 3 becomes −2 = −3.", "That is never true: no solution."],
               "no solution")
        + watch_out("Canceling x and stopping", "After x vanishes you still have a true or false number sentence. That sentence is the answer."),
        16)
    c5 = concept_block(
        "5. Hidden grouping",
        ["2x − (x − 5) = 9. The minus hits the 5 too: 2x − x + 5 = 9 → x = 4.",
         "5 − 2(x + 1) = 9 → 5 − 2x − 2 = 9 → −2x + 3 = 9 → x = −3.",
         "6 = 2(x − 1) + 4 → 6 = 2x + 2 → x = 2.",
         "Write a new line after you distribute. Do not skip that line in your head.",
         "Half of (x − 4) is 6 means (x − 4)/2 = 6, so x − 4 = 12, x = 16.",
         "Grouping is the difference between −x − 5 and −x + 5."],
        solved(1, "Solve 5 − 2(x + 1) = 9.",
               ["5 − 2x − 2 = 9.", "−2x + 3 = 9, so −2x = 6.", "x = −3."], "−3"),
        21)
    c6 = concept_block(
        "6. Linear-equation stories",
        ["Let x be the unknown. Translate, then use the machine from this unit.",
         "A number times 3, minus 1, is 14: 3x − 1 = 14, x = 5.",
         "Two expressions for the same quantity become one equation.",
         "If a story cannot be true (a contradiction), say so. If it is true for every input, say infinitely many.",
         "Define x in a sentence. Then write the equation. Then solve. Then read the number back in words.",
         "This one-variable skill is the engine inside a two-variable system next."],
        solved(1, "Half of a number minus 4 is 6. What is the number?",
               ["(x − 4)/2 = 6, or half of (x−4) is 6.", "x − 4 = 12.", "x = 16."], "16")
        + try_this("Name x first", "A sentence 'let x be…' stops you from solving for the wrong quantity."),
        26)
    content = unit_shell(
        title,
        ["Distribute in a multi-step equation", "Variables on both sides", "Fractions and decimals",
         "Infinitely many or none", "Hidden grouping", "Translate stories"],
        c1 + c2 + c3 + c4 + c5 + c6, practice_slots(31, 50), "unit-2-equations.mp4")


def _u3_questions():
    items = [
        ("In y = mx + b, m is the…", "slope", ["y-intercept", "x-intercept", "origin"], "Steepness."),
        ("In y = mx + b, b is the…", "y-intercept", ["slope", "run", "origin only"], "Where the line hits the y-axis."),
        ("y = (1/2)x + 2. Slope?", "1/2", ["2", "1", "−1/2"], "m is the coefficient of x."),
        ("y = (1/2)x + 2. y-intercept?", "2", ["1/2", "0", "4"], "b=2, point (0, 2)."),
        ("Slope through (1, 2) and (3, 6)?", "2", ["4", "1/2", "3"], "(6−2)/(3−1)=4/2."),
        ("A horizontal line has slope…", "0", ["undefined", "1", "infinity"], "Rise 0."),
        ("A vertical line has slope…", "undefined", ["0", "1", "−1"], "Run 0."),
        ("y = −3x + 1. The line…", "falls left to right", ["rises left to right", "is horizontal", "is vertical"], "Negative slope."),
        ("Parallel lines have…", "equal slopes", ["opposite slopes", "slopes that multiply to −1", "the same intercept"], "Same steepness."),
        ("Perpendicular slopes multiply to…", "−1", ["1", "0", "2"], "Negative reciprocal."),
        ("Slope of y = 4 − 2x?", "−2", ["4", "2", "−4"], "Rewrite y=−2x+4."),
        ("A line through (0, 3) with slope 2. Equation?", "y = 2x + 3", ["y = 3x + 2", "y = 2x − 3", "y = x + 3"], "m=2, b=3."),
        ("When x=4 on y=(1/2)x+2, y=?", "4", ["2", "6", "8"], "2+2."),
        ("Rise 3, run 6. Slope?", "1/2", ["2", "9", "3"], "3/6."),
        ("The graph of a linear function is…", "a straight line", ["a U", "a V", "a circle"], "Constant slope."),
        ("x-intercept of y=2x−6?", "3", ["−6", "2", "−3"], "Set y=0: 2x=6."),
        ("Two points (0, 1) and (2, 5). Slope?", "2", ["4", "1/2", "3"], "4/2."),
        ("y = 5 is…", "horizontal, slope 0", ["vertical", "slope 5", "through origin only"], "Every x, y stays 5."),
        ("x = −2 is…", "vertical, undefined slope", ["horizontal", "y=−2", "slope −2"], "Every y, x stays −2."),
        ("m = 3/4 means…", "up 3, right 4", ["up 4, right 3", "down 3, left 4 only", "b=3/4"], "Rise over run."),
        ("A line with slope 2/3 through (0, −1)?", "y = (2/3)x − 1", ["y = −x + 2/3", "y = (3/2)x − 1", "y = 2x − 3"], "m and b."),
        ("If m=0 and b=4, the equation is…", "y = 4", ["x = 4", "y = 4x", "y = 0"], "Horizontal."),
        ("From (2, 3) using slope 1/2, a next point is…", "(4, 4)", ["(3, 5)", "(2, 3.5)", "(1, 2)"], "Right 2, up 1."),
        ("y − 2 = 3(x − 1) in slope-intercept?", "y = 3x − 1", ["y = 3x + 2", "y = 3x − 3", "y = x − 1"], "y=3x−3+2."),
        ("The slope between (4, 1) and (4, 7) is…", "undefined", ["0", "6", "1.5"], "Vertical: run 0."),
        ("b is the value of y when…", "x = 0", ["y = 0", "x = 1", "m = 0"], "Y-intercept."),
        ("A rate of 60 km/h as slope is…", "60", ["1/60", "0", "−60"], "Rise in km, run in hours."),
        ("y = x has slope…", "1", ["0", "undefined", "x"], "Up 1, right 1."),
        ("If two lines have slopes 2 and −1/2 they are…", "perpendicular", ["parallel", "the same line", "horizontal"], "2×(−1/2)=−1."),
        ("To graph y=2x−1, start at…", "(0, −1), then up 2 right 1", ["(2, −1)", "(0, 2)", "the origin only"], "b then m."),
    ]
    return _fill(_pack(items), 80, lambda i: mq(
        f"On y = 2x + 1, when x = {i % 5 + 1}, y = ?",
        2 * (i % 5 + 1) + 1,
        "Double x, then add 1.",
        i,
    ))


def build_unit3():
    title = "Eighth Grade Math Unit 3: Slope and Linear Graphs"
    description = "Graph linear functions in slope-intercept form. Find slope from two points. Identify intercepts, parallel, and perpendicular."
    c1 = concept_block(
        "1. Slope is rise over run",
        ["Slope m = (y₂ − y₁)/(x₂ − x₁). From (1, 2) to (3, 6): (6−2)/(3−1) = 2.",
         "Positive slope rises left to right. Negative slope falls. Slope 0 is horizontal. Vertical is undefined (run 0).",
         "Rise 3, run 6 is slope 1/2. Reduce the fraction.",
         "A rate like 60 km per hour is a slope: kilometers on y, hours on x.",
         "The slope between (4, 1) and (4, 7) is undefined: x did not change.",
         "Count a grid triangle: up 1, right 2 is m = 1/2."],
        slope_line(0.5, 2, title="y = (1/2)x + 2",
                   caption="From (2, 3) to (4, 4): run 2, rise 1, so m = 1/2. The line hits the y-axis at 2.")
        + solved(1, "Find the slope through (1, 2) and (3, 6).",
                 ["Subtract y's: 6 − 2 = 4.", "Subtract x's: 3 − 1 = 2.", "4/2 = 2."], "2")
        + phet_box("slope"),
        1)
    c2 = concept_block(
        "2. y = mx + b",
        ["m is slope. b is the y-intercept — the line hits the y-axis at (0, b).",
         "y = (1/2)x + 2 has slope 1/2 and intercept 2.",
         "Rewrite y = 4 − 2x as y = −2x + 4 so you can see m = −2 and b = 4.",
         "To graph: plot (0, b), then use rise/run to a second point, then draw the line.",
         "When x = 4 on y = (1/2)x + 2, y = 2 + 2 = 4. The point (4, 4) must sit on the graph.",
         "x-intercept: set y = 0. For y = 2x − 6, 0 = 2x − 6, x = 3."],
        solved(1, "Graph-read y = (1/2)x + 2. What is b, and what is y when x = 4?",
               ["b is 2, so (0, 2).", "(1/2)×4 + 2 = 4.", "Point (4, 4)."], "b=2; y=4")
        + matching([("m in y=mx+b", "slope"), ("b", "y-intercept"),
                    ("horizontal", "m=0"), ("vertical", "undefined slope")], vid="g8u3-c2-match"),
        kid_tip("Start at b", "Plot (0, b) first. Then walk the slope."),
        6)
    c3 = concept_block(
        "3. Write the equation from a graph or points",
        ["Read b from the y-axis. Read m from a slope triangle. Write y = mx + b.",
         "A line through (0, 3) with slope 2 is y = 2x + 3.",
         "From two points: find m, then plug one point to find b. Or use point-slope: y − y₁ = m(x − x₁).",
         "y − 2 = 3(x − 1) becomes y = 3x − 3 + 2, so y = 3x − 1.",
         "y = 5 is horizontal. x = −2 is vertical and is not a function of x in the usual y= form.",
         "A table with constant change in y for constant change in x is linear."],
        four_quadrant_plane([(0, 2, "b"), (2, 3, ""), (4, 4, "")], lim=5,
                            title="Points on y = (1/2)x + 2",
                            caption="(0, 2) is the intercept. (2, 3) and (4, 4) sit on the same slope 1/2.")
        + solved(1, "A line through (0, 3) has slope 2. Equation?",
                 ["b = 3.", "m = 2.", "y = 2x + 3."], "y = 2x + 3")
        + phet_box("lines"),
        11)
    c4 = concept_block(
        "4. Parallel and perpendicular",
        ["Parallel lines have equal slopes and different intercepts. They never meet.",
         "Perpendicular slopes are negative reciprocals: they multiply to −1. Example: 2 and −1/2.",
         "A line perpendicular to y = (1/2)x + 2 has slope −2.",
         "Same slope and same intercept means the same line, not two parallel lines.",
         "Vertical is perpendicular to horizontal.",
         "These facts are how you write a line through a point, parallel to a given line: copy m, change b."],
        solved(1, "A line has slope 2. What slope is perpendicular?",
               ["Negative reciprocal.", "Flip 2 to 1/2, then minus.", "−1/2. Check: 2×(−1/2)=−1."], "−1/2"),
        16)
    c5 = concept_block(
        "5. Intercepts and special lines",
        ["Y-intercept: x = 0. X-intercept: y = 0.",
         "y = 2x − 6 hits y at −6 and x at 3.",
         "y = 4 is a horizontal line through 4 on the y-axis. Slope 0.",
         "x = −2 is a vertical line. It is not y = mx + b.",
         "The origin (0, 0) is on the line only when b = 0, like y = 3x. That is also a proportional relationship.",
         "Sketch both intercepts, then connect. That is often faster than a slope walk."],
        solved(1, "Find the x-intercept of y = 2x − 6.",
               ["Set y = 0.", "2x = 6.", "x = 3. Point (3, 0)."], "3")
        + watch_out("Mixing intercepts", "b is where x is 0, not where y is 0."),
        21)
    c6 = concept_block(
        "6. Linear graphs in stories",
        ["A taxi: 3 dollars plus 2 dollars per mile is y = 2x + 3. Slope is the rate. b is the start fee.",
         "A tank losing 4 liters per minute from 40 liters: y = −4x + 40.",
         "Read a graph: the intercept is the starting amount; the slope is how fast it changes.",
         "If two plans are two lines, the meeting point is a system — Unit 5.",
         "Units on slope must match: dollars per mile, not miles per dollar, unless you mean the reciprocal.",
         "Write y = mx + b, then name m and b in words."],
        solved(1, "A ride costs 3 dollars plus 2 dollars per mile. Write y in terms of miles x.",
               ["Start fee is b = 3.", "Rate is m = 2.", "y = 2x + 3."], "y = 2x + 3")
        + try_this("Name rate and start", "m is the per-one change. b is the amount when x is 0."),
        26)
    content = unit_shell(
        title,
        ["Slope as rise over run", "y = mx + b", "Write an equation from points",
         "Parallel and perpendicular", "Intercepts and special lines", "Linear stories"],
        c1 + c2 + c3 + c4 + c5 + c6, practice_slots(31, 50), "unit-3-slope.mp4")


def _u4_questions():
    items = [
        ("A function assigns…", "exactly one output to each input", ["two outputs to one input", "no outputs", "only x=0"], "Vertical line test."),
        ("The vertical line test fails when…", "a vertical line hits the graph twice", ["the slope is 0", "b is negative", "x is 0"], "Two y's for one x."),
        ("f(3) for f(x)=2x−1?", "5", ["6", "2", "3"], "2×3−1."),
        ("A table 1→3, 2→5, 3→7 is…", "linear, slope 2", ["not a function", "quadratic", "slope 1"], "+2 each time."),
        ("y = x² is…", "nonlinear", ["linear", "a horizontal line", "undefined slope"], "U shape."),
        ("y = 2x + 1 is…", "linear", ["a parabola", "a circle", "not a function"], "Constant slope."),
        ("Domain is…", "the allowed inputs", ["the outputs", "the slope", "b"], "x-values."),
        ("Range is…", "the outputs that actually happen", ["the inputs", "m", "the origin"], "y-values."),
        ("f(x)=x². f(−3)=?", "9", ["−9", "6", "−6"], "(−3)×(−3)."),
        ("Which relation is not a function? x → y: 2 maps to both 5 and 7", "not a function", ["function", "linear", "slope 2"], "One input, two outputs."),
        ("A circle fails the…", "vertical line test", ["slope test", "exponent rule", "Pythagorean theorem"], "Two y's."),
        ("Linear vs nonlinear: constant first differences means…", "linear", ["quadratic", "exponential always", "not a function"], "Even steps in y."),
        ("g(x)=−x+4. g(0)=?", "4", ["0", "−4", "1"], "The intercept."),
        ("If f(x)=3x, f(a+1)=?", "3a+3", ["3a+1", "a+3", "3a"], "3(a+1)."),
        ("A function machine: ×2 then +1. Input 5. Output?", "11", ["10", "6", "7"], "10+1."),
        ("y = 1/x (x≠0) is…", "nonlinear, still a function", ["linear", "not a function", "a circle"], "One y per x."),
        ("The graph of f(x)=|x| is…", "a V, still a function", ["a circle", "not a function", "a horizontal line"], "Each x has one y."),
        ("If two points have the same x and different y…", "it is not a function", ["slope is 0", "it is linear", "b=0"], "Vertical pair."),
        ("f(x)=2x−1. Solve f(x)=9. x=?", "5", ["8", "11", "4"], "2x=10."),
        ("A sequence 2, 5, 8, 11 has common difference…", "3", ["2", "5", "1"], "Linear pattern."),
        ("Exponential 2, 4, 8, 16 is…", "not linear", ["slope 2", "slope 4", "y=mx+b with m=2"], "Multiply, don't add."),
        ("f(2)=7 and f is linear with slope 3. f(3)=?", "10", ["9", "13", "6"], "+3."),
        ("Independent variable is usually…", "x, the input", ["y, the output", "m", "b"], "You choose x."),
        ("Dependent variable is usually…", "y, the output", ["x", "the slope", "the axis"], "It depends on x."),
        ("A graph that passes the vertical line test…", "is a function", ["must be linear", "must pass through origin", "has slope 1"], "One y per x."),
        ("f(x)=x³. f(2)=?", "8", ["6", "9", "4"], "2×2×2."),
        ("Constant function f(x)=5. Slope?", "0", ["5", "undefined", "1"], "Horizontal."),
        ("To show nonlinear from a table, look for…", "changing differences", ["one output per input", "integers only", "a y-intercept"], "First differences not constant."),
        ("f(x)=2x+1 and g(x)=2x+1 are…", "the same function", ["perpendicular", "parallel lines with different b", "not functions"], "Same rule."),
        ("If f(0)=b, that value is…", "the y-intercept of the graph", ["the slope", "the domain", "undefined"], "x=0."),
    ]
    return _fill(_pack(items), 80, lambda i: mq(
        f"If f(x) = 2x + 3, what is f({i % 6 + 1})?",
        2 * (i % 6 + 1) + 3,
        "Replace x, then multiply by 2 and add 3.",
        i,
    ))


def build_unit4():
    title = "Eighth Grade Math Unit 4: Functions"
    description = "Define a function, use function notation, compare linear and nonlinear, and read tables and graphs."
    c1 = concept_block(
        "1. One input, one output",
        ["A function assigns exactly one output to each input. f(3) is 'the output when the input is 3.'",
         "The vertical line test: if a vertical line hits a graph twice, that x has two y's — not a function.",
         "A circle fails. y = x² passes (a U). y = |x| passes (a V).",
         "A mapping 2 → 5 and 2 → 7 is not a function.",
         "y = 1/x (x ≠ 0) is a function even though it is not a line.",
         "Domain: allowed inputs. Range: outputs that actually happen."],
        solved(1, "Is a circle a function of x?",
               ["A vertical line through the center hits twice.", "Two y-values for one x.",
                "It fails the vertical line test."], "no")
        + matching([("function", "one output per input"), ("vertical line test fail", "not a function"),
                    ("domain", "inputs"), ("range", "outputs")], vid="g8u4-c1-match")
        + phet_box("func"),
        1)
    c2 = concept_block(
        "2. Function notation",
        ["f(x) = 2x − 1. Then f(3) = 5. You replace every x with 3.",
         "f(x) = x². f(−3) = 9, not −9.",
         "g(x) = −x + 4. g(0) = 4, which is the intercept of that line.",
         "Solving f(x) = 9 for f(x) = 2x − 1 means 2x − 1 = 9, so x = 5. That is an input that produces 9.",
         "f(a+1) when f(x)=3x is 3(a+1)=3a+3. Substitute the whole blob.",
         "Independent variable is the input (usually x). Dependent is the output (usually y or f(x))."],
        solved(1, "If f(x) = 2x − 1, find f(3) and the x that makes f(x) = 9.",
               ["f(3)=6−1=5.", "2x−1=9 → 2x=10.", "x=5."], "f(3)=5; x=5 when f(x)=9"),
        kid_tip("Parentheses mean 'plug in'", "f(3) is not f times 3 unless the rule says so."),
        6)
    c3 = concept_block(
        "3. Linear functions",
        ["A linear function has a constant rate. Its graph is a straight line: f(x) = mx + b.",
         "A table 1→3, 2→5, 3→7 adds 2 each time. Slope 2. f(x)=2x+1.",
         "If f(2)=7 and slope is 3, then f(3)=10.",
         "A constant function f(x)=5 is linear with slope 0.",
         "First differences in y (for even x-steps) stay the same if and only if the function is linear.",
         "y = 2x + 1 and f(x) = 2x + 1 are the same rule."],
        slope_line(2, 1, title="f(x) = 2x + 1", caption="Each step of 1 in x adds 2 to the output. That constant add is the slope.")
        + solved(1, "A table goes 1→3, 2→5, 3→7. Write f(x).",
                 ["y increases by 2 when x increases by 1.", "m=2.", "When x=1, y=3 so 2(1)+b=3, b=1. f(x)=2x+1."],
                 "f(x)=2x+1"),
        11)
    c4 = concept_block(
        "4. Nonlinear functions",
        ["If first differences change, it is not linear. 2, 4, 8, 16 multiplies by 2 — exponential, not a line.",
         "y = x²: second differences are constant, graph is a U.",
         "y = x³: f(2)=8. It is a function, not a line.",
         "A V (absolute value) is nonlinear but still a function.",
         "Do not call every curve 'not a function.' Functions can bend. They just cannot fork vertically.",
         "In a table, if +2 then +4 then +8, slope is not constant."],
        solved(1, "The sequence 2, 4, 8, 16: linear or not?",
               ["Ratios, not equal adds.", "Each term ×2.", "Nonlinear (exponential pattern)."], "not linear")
        + watch_out("Curve vs not-a-function", "A U can be a function. Two y's for one x cannot."),
        16)
    c5 = concept_block(
        "5. Machines, tables, graphs",
        ["A function machine: ×2 then +1. Input 5 → 10 → 11. That is f(x)=2x+1.",
         "Read a graph: f(0) is the y-intercept. f(2) is the height at x=2.",
         "A sequence 2, 5, 8, 11 has common difference 3. An arithmetic sequence is a linear function on whole-number inputs.",
         "Sketch: linear is a line, quadratic a U, exponential a rapid climb.",
         "To show a table is a function, check that no x repeats with a new y.",
         "To show it is linear, check equal steps."],
        solved(1, "A machine multiplies by 2 then adds 1. What is the output for 5?",
               ["5×2=10.", "10+1=11.", "f(5)=11."], "11")
        + step_reveal(["Ask: is it a function?", "Ask: are first differences constant?",
                       "If yes, write y=mx+b.", "If no, name the shape (U, exponential, V)."],
                      vid="g8u4-c5-steps"),
        21)
    c6 = concept_block(
        "6. Functions in context",
        ["Cost y in dollars for x shirts at 12 dollars each plus 5 dollars shipping: y=12x+5. Linear.",
         "Area of a square of side x is x². Nonlinear.",
         "The independent variable is the one you choose (shirts, side length). The dependent is what you get (cost, area).",
         "f(0) often means the start: empty cart, zero seconds, intercept.",
         "Two functions can be compared: which plan is cheaper after 10 items? That comparison is a system in the next units.",
         "Write the rule, name domain sense (you cannot buy −3 shirts), then evaluate."],
        solved(1, "Shirts cost 12 dollars each plus 5 dollars shipping. Write f(x) for x shirts.",
               ["12 per shirt is the slope.", "5 is the start fee.", "f(x)=12x+5."], "f(x)=12x+5")
        + try_this("Input in words", "Say 'x is the number of shirts' before you write f(x)."),
        26)
    content = unit_shell(
        title,
        ["One input, one output", "Function notation", "Linear functions",
         "Nonlinear functions", "Machines, tables, graphs", "Functions in context"],
        c1 + c2 + c3 + c4 + c5 + c6, practice_slots(31, 50), "unit-4-functions.mp4")
