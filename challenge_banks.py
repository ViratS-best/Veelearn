"""Unit-topic Hard / Stretch challenges (AMC 8 & MathCounts flavor).

Each helper is keyed to a unit theme so Grade 8 Unit 1 (exponents) never
pulls Pythagorean-theorem items, etc.
"""

from __future__ import annotations

import math
import re

from question_banks import _q


def challenges_for(title: str) -> list:
    t = (title or "").lower()
    out = []

    # --- High school (check before Algebra 2 / grade bands) ---
    if "ap calculus bc" in t or "calculus bc" in t:
        out += _bc(t)
        return [q for q in out if q]
    if "ap calculus ab" in t or "calculus ab" in t:
        out += _ab()
        return [q for q in out if q]
    if "precalculus" in t or "precalc" in t:
        out += _precalc(t)
        return [q for q in out if q]
    if t.startswith("trigonometry") or "trigonometry unit" in t:
        out += _trig(t)
        return [q for q in out if q]
    if t.startswith("geometry") or "geometry unit" in t:
        out += _geo(t)
        return [q for q in out if q]
    if "algebra 1" in t:
        out += _a1(t)
        return [q for q in out if q]

    # --- MathCounts ---
    if "mathcounts" in t:
        if "permut" in t or "arrangement" in t:
            out += _mc_perm()
        elif "combin" in t or "binomial" in t:
            out += _mc_comb()
        elif "casework" in t or "overcount" in t:
            out += _mc_case()
        elif "stars" in t or "bars" in t:
            out += _mc_stars()
        elif "inclusion" in t:
            out += _mc_pie()
        elif "path" in t or "recursion" in t or "sequence" in t:
            out += _mc_paths()
        elif "mixed" in t or "contest" in t or "strategy" in t:
            out += _mc_mixed()
        else:
            out += _mc_counting()
        return [q for q in out if q]

    # --- Algebra 2 ---
    if "algebra 2" in t:
        if "quadratic" in t:
            out += _a2_quad()
        elif "complex" in t:
            out += _a2_complex()
        elif "polynomial" in t:
            out += _a2_poly()
        elif "rational" in t:
            out += _a2_rat()
        elif "radical" in t:
            out += _a2_rad()
        elif "exponential" in t or "log" in t:
            out += _a2_explog()
        elif "sequence" in t or "trig" in t:
            out += _a2_seq()
        else:
            out += _a2_functions()
        return [q for q in out if q]

    # --- Grade 8 ---
    if "eighth" in t or "8th" in t:
        if "exponent" in t or "scientific" in t:
            out += _g8_exponents()
        elif "linear equation" in t or "one variable" in t:
            out += _g8_equations()
        elif "slope" in t or "linear graph" in t:
            out += _g8_slope()
        elif "function" in t and "quadratic" not in t:
            out += _g8_functions()
        elif "substitution" in t:
            out += _g8_systems()
        elif "elimination" in t:
            out += _g8_systems()
        elif "pythag" in t or "cylinder" in t:
            out += _g8_pythag()
        elif "scatter" in t or "data" in t:
            out += _g8_data()
        else:
            out += _g8_exponents()
        return [q for q in out if q]

    # --- Grade 7 ---
    if "seventh" in t or "7th" in t:
        if "negative" in t or "add" in t and "subtract" in t:
            out += _g7_integers()
        elif "multiplying" in t or "dividing" in t:
            out += _g7_rational_ops()
        elif "proportional" in t:
            out += _g7_prop()
        elif "percent" in t:
            out += _g7_percent()
        elif "equation" in t or "inequal" in t:
            out += _g7_equations()
        elif "circle" in t or "angle" in t:
            out += _g7_geometry()
        elif "scale" in t or "surface" in t or "volume" in t:
            out += _g7_scale()
        else:
            out += _g7_stats()
        return [q for q in out if q]

    # --- Grade 6 ---
    if "sixth" in t or "6th" in t:
        if "ratio" in t and "rational" not in t:
            out += _g6_ratios()
        elif "percent" in t or "unit rate" in t:
            out += _g6_rates()
        elif "rational" in t or "fraction" in t:
            out += _g6_rational()
        elif "integer" in t or "number line" in t:
            out += _g6_integers()
        elif "coordinate" in t or "quadrant" in t:
            out += _g6_coord()
        elif "expression" in t or "equation" in t:
            out += _g6_expr()
        elif "area" in t or "volume" in t or "surface" in t:
            out += _g6_area()
        else:
            out += _g6_data()
        return [q for q in out if q]

    # --- Grades 1–5: stay grade-appropriate and unit-ish ---
    if "fifth" in t:
        out += _g5()
    elif "fourth" in t:
        out += _g4()
    elif "third" in t:
        out += _g3()
    elif "second" in t:
        out += _g2()
    elif "first" in t:
        out += _g1()
    else:
        out += _g6_ratios()[:6]

    return [q for q in out if q]


def challenge_filler(title: str, n: int, difficulty: str = "hard"):
    pool = challenges_for(title)
    if not pool:
        pool = _g8_exponents() if "exponent" in (title or "").lower() else _mc_counting()
    prefer = [q for q in pool if q.get("difficulty") == difficulty] or pool
    item = prefer[(n - 1) % len(prefer)]
    q = dict(item)
    text = q["question_text"]
    ans = q["correct_answer"]
    dist = list(q.get("distractors") or [])

    # Topic-preserving numeric variants
    if "scientific notation" in text.lower() or re.search(r"0\.0+\d+", text):
        # Vary the decimal
        decimals = [0.00056, 0.00034, 0.0045, 0.000078, 0.0000091]
        val = decimals[n % len(decimals)]
        # convert to sci
        exp = 0
        coef = val
        while coef < 1:
            coef *= 10
            exp -= 1
        while coef >= 10:
            coef /= 10
            exp += 1
        coef = round(coef, 4)
        ans = f"{coef} × 10^{exp}"
        text = f"Write {val} in scientific notation."
        dist = [
            f"{coef} × 10^{exp + 1}",
            f"{coef} × 10^{exp - 1}",
            f"{coef * 10} × 10^{exp - 1}",
        ]
    elif re.search(r"\d+\^\d+", text) or "exponent" in text.lower():
        bases = [2, 3, 4, 5, 6]
        b = bases[n % len(bases)]
        e1, e2 = 2 + (n % 3), 3 + (n % 2)
        ans = f"{b}^{e1 + e2}"
        text = f"Simplify {b}^{e1} × {b}^{e2}."
        dist = [f"{b}^{e1 * e2}", f"{b}^{e1 - e2}", f"{b * b}^{e1 + e2}"]
    elif "paths from (0,0)" in text.lower():
        a, b = 3 + (n % 3), 2 + (n % 2)
        ans = str(math.comb(a + b, a))
        text = f"Paths from (0,0) to ({a},{b}) using only right and up unit steps?"
        dist = [str(a * b), str(a + b), str(2 ** (a + b))]
    elif "nonnegative" in text.lower() and "x+y+z" in text.lower():
        s = 4 + (n % 4)
        ans = str(math.comb(s + 2, 2))
        text = f"Nonnegative integer solutions to x+y+z={s}?"
        dist = [str(s * 3), str(math.comb(s + 2, 1)), str(s ** 2)]

    q["question_text"] = f"{text} (variant {n})"
    q["correct_answer"] = str(ans)
    q["distractors"] = [str(d) for d in dist[:3]] if dist else None
    q["difficulty"] = difficulty
    return q


# ----- banks -----

def _mc_counting():
    return [
        _q("AMC 8 style: How many 3-letter strings from {A,B,C,D} include at least one A (repeats OK)?", 37, "4³−3³=64−27=37.", [64, 27, 48], "hard"),
        _q("How many 4-digit PINs use digits 0–9 with no repeat (first digit ≠0)?", 4536, "9×9×8×7=4536.", [9000, 5040, 10000], "hard"),
        _q("How many outcomes when a fair die is rolled twice have sum 7?", 6, "Six ordered pairs.", [5, 7, 12], "hard"),
        _q("SAT Stretch: Integers 1–100 divisible by 2 or 5?", 60, "50+20−10=60.", [70, 50, 40], "stretch"),
        _q("Product rule: 3 shirts and 4 pants (one each). Outfits?", 12, "3×4=12.", [7, 14, 24], "hard"),
        _q("Complement: 2-digit numbers from digits 1–9 with at least one even digit?", 56, "81−25=56.", [45, 65, 72], "stretch"),
    ]


def _mc_perm():
    return [
        _q("Arrangements of MATH?", 24, "4!=24.", [16, 12, 8], "hard"),
        _q("Distinct arrangements of BOOK?", 12, "4!/2!=12.", [24, 6, 8], "hard"),
        _q("P(10,2) president and VP from 10?", 90, "10×9=90.", [45, 100, 20], "hard"),
        _q("Circular arrangements of 5 distinct people?", 24, "(5−1)!=24.", [120, 60, 5], "stretch"),
        _q("SAT Stretch: How many injections from a 3-set into a 5-set?", 60, "P(5,3)=60.", [10, 125, 15], "stretch"),
    ]


def _mc_comb():
    return [
        _q("C(8,3) committees?", 56, "56.", [24, 336, 512], "hard"),
        _q("C(12,4)?", 495, "495.", [48, 11880, 220], "hard"),
        _q("Binomial C(6,2)?", 15, "15.", [12, 30, 64], "hard"),
        _q("SAT Stretch: Ways to choose 2 co-captains from 9 (unordered)?", 36, "C(9,2)=36.", [72, 18, 81], "stretch"),
    ]


def _mc_case():
    return [
        _q("Integers 10–99 with digit sum 9?", 9, "18,27,…,90.", [10, 18, 8], "hard"),
        _q("How many 3-digit numbers have all odd digits?", 125, "5³=125.", [250, 512, 100], "stretch"),
        _q("Casework: sums on two dice equal to 8?", 5, "Five ordered pairs? (2,6)(3,5)(4,4)(5,3)(6,2)=5.", [6, 4, 7], "hard"),
    ]


def _mc_stars():
    return [
        _q("Nonnegative solutions x+y+z=5?", 21, "C(7,2)=21.", [15, 25, 10], "hard"),
        _q("Positive solutions x+y+z=5?", 6, "C(4,2)=6.", [10, 21, 3], "hard"),
        _q("SAT Stretch: Nonneg x+y=7?", 8, "8 solutions.", [7, 14, 6], "stretch"),
    ]


def _mc_pie():
    return [
        _q("|A∪B| if |A|=12,|B|=18,|A∩B|=5?", 25, "12+18−5.", [30, 23, 15], "hard"),
        _q("1–100 divisible by 4 or 6?", 33, "25+16−8.", [41, 25, 16], "hard"),
        _q("SAT Stretch: 1–200 divisible by 3 or 5?", 93, "66+40−13.", [106, 80, 100], "stretch"),
    ]


def _mc_paths():
    return [
        _q("Paths (0,0)→(4,3) right/up only?", 35, "C(7,3)=35.", [12, 24, 64], "hard"),
        _q("Ways to climb 5 stairs taking 1 or 2 at a time?", 8, "Fibonacci.", [5, 16, 10], "hard"),
        _q("SAT Stretch: Paths (0,0)→(3,3) not above diagonal (Catalan C_3)?", 5, "5.", [6, 9, 20], "stretch"),
    ]


def _mc_mixed():
    return _mc_counting() + _mc_perm()[:2] + _mc_comb()[:2]


def _a2_functions():
    return [
        _q("If f(x)=2x−3 and g(x)=x², (g∘f)(2)?", 1, "f(2)=1; g(1)=1.", [4, 5, 0], "hard"),
        _q("Domain of √(x−4)?", "x≥4", "", ["x>4", "x≤4", "all real"], "hard"),
        _q("SAT Stretch: If f(x)=3x−7, f(f(3))?", -1, "f(3)=2; f(2)=−1.", [2, 14, 5], "stretch"),
    ]


def _a2_quad():
    return [
        _q("Discriminant of x²−6x+10?", -4, "36−40.", [4, 16, 0], "hard"),
        _q("Sum of roots of 2x²−5x+3=0?", "5/2", "−b/a.", ["3/2", "-5/2", "3"], "hard"),
        _q("SAT Stretch: Solutions of x²−6x+10=0?", "3±i", "(x−3)²=−1.", ["3", "±√10", "6±i"], "stretch"),
    ]


def _a2_complex():
    return [
        _q("|3−4i|?", 5, "5.", [7, 1, 12], "hard"),
        _q("i²²?", -1, "22 mod 4 = 2.", [1, "i", "-i"], "hard"),
        _q("SAT Stretch: (5+i)/(1−i)?", "2+3i", "Multiply by conjugate.", ["3+2i", "5−i", "1+i"], "stretch"),
    ]


def _a2_poly():
    return [
        _q("Remainder of x³−2x+1 divided by x−1?", 0, "p(1)=0.", [1, -1, 2], "hard"),
        _q("Factor x³−8?", "(x−2)(x²+2x+4)", "", ["(x−2)³", "(x+2)(x²−4)", "x³−2³ wrong"], "hard"),
        _q("SAT Stretch: Monic cubic with zeros 0,2,−2?", "x³−4x", "", ["x³−4", "x(x−2)²", "x³+4x"], "stretch"),
    ]


def _a2_rat():
    return [
        _q("Solve x/(x−2)=3.", 3, "x=3x−6.", [2, 6, -3], "hard"),
        _q("HA of (2x+1)/(x−3)?", "y=2", "Leading ratio.", ["x=3", "y=0", "y=1/2"], "hard"),
        _q("SAT Stretch: Solve 2/(x−1)−1/(x+1)=1/(x²−1).", -2, "Clear denom.", [2, 1, 0], "stretch"),
    ]


def _a2_rad():
    return [
        _q("Simplify √48?", "4√3", "", ["√16·3", "2√12", "8√3"], "hard"),
        _q("Solve √(x+3)=5.", 22, "x+3=25.", [2, 8, 15], "hard"),
        _q("SAT Stretch: (x^{1/3})² for x=8?", 4, "2²=4.", [2, 16, 1], "stretch"),
    ]


def _a2_explog():
    return [
        _q("log₂(x)=5 ⇒ x?", 32, "2⁵.", [25, 10, 16], "hard"),
        _q("3ˣ=81 ⇒ x?", 4, "3⁴.", [3, 5, 27], "hard"),
        _q("SAT Stretch: log₃(81)?", 4, "3⁴=81.", [3, 27, 2], "stretch"),
    ]


def _a2_seq():
    return [
        _q("Arithmetic: a₁=3,d=4. a₅?", 19, "3+4·4.", [15, 23, 7], "hard"),
        _q("Geometric: 2,6,18,… next?", 54, "×3.", [36, 24, 72], "hard"),
        _q("SAT Stretch: Sum 1+2+…+20?", 210, "n(n+1)/2.", [200, 220, 190], "stretch"),
    ]


def _g8_exponents():
    return [
        _q("Simplify 2⁵ × 2³.", "2⁸", "Add exponents.", ["2¹⁵", "2²", "4⁸"], "hard"),
        _q("Write 0.00056 in scientific notation.", "5.6 × 10⁻⁴", "Four places left.", ["5.6 × 10⁴", "56 × 10⁻⁵", "0.56 × 10⁻³"], "hard"),
        _q("Simplify (3 × 10⁴)(2 × 10⁻⁶).", "6 × 10⁻²", "Multiply coeffs; add exponents.", ["6 × 10¹⁰", "5 × 10⁻²", "6 × 10⁻²⁴"], "hard"),
        _q("What is 2⁻³ × 2⁵?", 4, "2²=4.", [1, 8, 16], "hard"),
        _q("SAT Stretch: (4.5 × 10³) ÷ (1.5 × 10⁻²)?", "3 × 10⁵", "4.5/1.5 and 3−(−2).", ["3 × 10¹", "6 × 10⁵", "3 × 10⁻⁵"], "stretch"),
        _q("SAT Stretch: Which is larger: 4.1×10³ or 3.9×10⁴?", "3.9 × 10⁴", "Compare exponents first.", ["4.1 × 10³", "equal", "cannot tell"], "stretch"),
        _q("Simplify (2³)⁴.", "2¹²", "Multiply exponents.", ["2⁷", "8⁴", "2⁶⁴"], "hard"),
        _q("5⁰ = ?", 1, "Nonzero to the 0 is 1.", [0, 5, 50], "hard"),
    ]


def _g8_equations():
    return [
        _q("Solve 3(x−4)=2x+5.", 17, "3x−12=2x+5.", [9, -17, 5], "hard"),
        _q("Solve 2x−7=11.", 9, "2x=18.", [2, 18, 4], "hard"),
        _q("SAT Stretch: Solve (x/3)+4=10.", 18, "x/3=6.", [6, 2, 30], "stretch"),
    ]


def _g8_slope():
    return [
        _q("Slope through (2,−1) and (6,5)?", "3/2", "6/4.", [2, "1/2", 4], "hard"),
        _q("y-intercept of y=−2x+7?", 7, "b=7.", [-2, 2, 0], "hard"),
        _q("SAT Stretch: Line through (0,3) slope 2. y when x=4?", 11, "3+8.", [8, 5, 14], "stretch"),
    ]


def _g8_functions():
    return [
        _q("If f(x)=3x−7, f(5)?", 8, "15−7.", [15, -2, 22], "hard"),
        _q("Is the relation {(1,2),(1,3)} a function?", "No", "", ["Yes", "Only at x=1", "Cannot tell"], "hard"),
        _q("SAT Stretch: f(x)=3x−7. f(f(3))?", -1, "f(3)=2; f(2)=−1.", [2, 14, 5], "stretch"),
    ]


def _g8_systems():
    return [
        _q("x+y=10 and x−y=2. Find x.", 6, "Add → 2x=12.", [4, 8, 5], "hard"),
        _q("2x+y=11 and x−y=1. Find y.", 3, "x=4 from add/sub; y=3.", [4, 5, 1], "hard"),
        _q("SAT Stretch: 3x+2y=16 and x−y=1. Find x.", "18/5", "From x=y+1 into first.", [3, 4, 2], "stretch"),
    ]


def _g8_pythag():
    return [
        _q("Legs 9 and 12. Hypotenuse?", 15, "3-4-5 ×3.", [13, 21, 108], "hard"),
        _q("Legs 5 and 12. Hypotenuse?", 13, "5-12-13.", [17, 60, 10], "hard"),
        _q("SAT Stretch: Cylinder r=3 h=10. Volume in terms of π?", "90π", "πr²h.", ["30π", "60π", "9π"], "stretch"),
    ]


def _g8_data():
    return [
        _q("Mean of 2,4,6,8,10?", 6, "30/5.", [5, 8, 10], "hard"),
        _q("Median of 3,1,7,5,9?", 5, "Sorted 1,3,5,7,9.", [3, 7, 9], "hard"),
        _q("SAT Stretch: If a scatterplot trend is positive, as x increases y tends to…", "increase", "", ["decrease", "stay flat", "become random"], "stretch"),
    ]


def _g7_integers():
    return [
        _q("(−8)×(−3)+(−5)?", 19, "24−5.", [29, -29, 14], "hard"),
        _q("−12−(−5)?", -7, "−12+5.", [7, -17, 17], "hard"),
        _q("SAT Stretch: Absolute distance −7 to 4?", 11, "|4−(−7)|.", [3, -3, 28], "stretch"),
    ]


def _g7_rational_ops():
    return [
        _q("(-3/4)×(8/9)?", "-2/3", "Simplify.", ["-32/36", "2/3", "-3/9"], "hard"),
        _q("Divide −6 ÷ 2/3.", -9, "×3/2.", [9, -4, 4], "hard"),
        _q("SAT Stretch: (−2/5)÷(−4/15)?", "3/2", "×−15/−4.", ["8/75", "-3/2", "2/3"], "stretch"),
    ]


def _g7_prop():
    return [
        _q("Map 1 cm : 5 km. 12 cm → ? km", 60, "12×5.", [17, 24, 6], "hard"),
        _q("y=12 when x=4. y when x=7?", 21, "Unit rate 3.", [16, 28, 19], "hard"),
        _q("SAT Stretch: 3/5 of a number is 24. Number?", 40, "24÷3×5.", [30, 48, 15], "stretch"),
    ]


def _g7_percent():
    return [
        _q("$40 shirt, 15% off. Sale price?", 34, "40−6.", [35, 25, 55], "hard"),
        _q("35% of 80?", 28, "0.35×80.", [35, 24, 40], "hard"),
        _q("SAT Stretch: Tax 8% on $50. Total?", 54, "50+4.", [58, 42, 4], "stretch"),
    ]


def _g7_equations():
    return [
        _q("Solve 2x+5=17.", 6, "2x=12.", [11, 7, 22], "hard"),
        _q("Solve 3x−4>8. Smallest integer x?", 5, "3x>12 → x>4.", [4, 3, 6], "hard"),
        _q("SAT Stretch: Solve x/4 − 3 = 1.", 16, "x/4=4.", [4, 8, 12], "stretch"),
    ]


def _g7_geometry():
    return [
        _q("Circumference diameter 14 (π=22/7)?", 44, "πd.", [28, 154, 22], "hard"),
        _q("Adjacent angles on a line: one is 110°. Other?", 70, "180−110.", [90, 40, 250], "hard"),
        _q("SAT Stretch: Area of circle r=7 (π=22/7)?", 154, "πr².", [44, 49, 22], "stretch"),
    ]


def _g7_scale():
    return [
        _q("Scale 1:20. Drawing 3 cm → real cm?", 60, "3×20.", [23, 17, 6], "hard"),
        _q("Box 2×3×4. Surface area?", 52, "2(6+8+12).", [24, 48, 36], "hard"),
        _q("SAT Stretch: Volume of 2×3×4 box?", 24, "lwh.", [9, 18, 12], "stretch"),
    ]


def _g7_stats():
    return [
        _q("P(red or blue) if 1/4 red and 1/3 blue?", "7/12", "Add.", ["1/12", "1/2", "2/7"], "hard"),
        _q("Mean of 4,6,10,12?", 8, "32/4.", [6, 10, 7], "hard"),
        _q("SAT Stretch: P(even) on fair die?", "1/2", "2,4,6.", ["1/3", "1/6", "2/3"], "stretch"),
    ]


def _g6_ratios():
    return [
        _q("2:5 = 8:x. x?", 20, "Cross multiply.", [10, 16, 40], "hard"),
        _q("Simplify 12:18.", "2:3", "÷6.", ["3:2", "4:6", "1:2"], "hard"),
        _q("SAT Stretch: 3 cups flour / 2 dozen → cups for 5 dozen?", "7.5", "Unit rate.", [6, 5, 8], "stretch"),
    ]


def _g6_rates():
    return [
        _q("35% of 80?", 28, "", [35, 24, 40], "hard"),
        _q("Unit rate: $12 for 4 lb. Per lb?", 3, "", [2, 4, 8], "hard"),
        _q("SAT Stretch: 3/4 as a percent?", 75, "", [34, 50, 25], "stretch"),
    ]


def _g6_rational():
    return [
        _q("2/3 + 1/6?", "5/6", "", ["3/9", "1/2", "1"], "hard"),
        _q("5/8 − 1/4?", "3/8", "", ["4/4", "1/8", "6/8"], "hard"),
        _q("SAT Stretch: 0.125 as fraction lowest terms. num+den?", 9, "1/8.", [125, 8, 5], "stretch"),
    ]


def _g6_integers():
    return [
        _q("|−15|+|6|?", 21, "", [9, -9, 15], "hard"),
        _q("Distance −7 to 4?", 11, "", [3, -3, 28], "hard"),
        _q("SAT Stretch: (−3)+(−8)?", -11, "", [11, -5, 5], "stretch"),
    ]


def _g6_coord():
    return [
        _q("Point (3,−2) quadrant?", "IV", "", ["I", "II", "III"], "hard"),
        _q("Reflect (2,5) over x-axis?", "(2,−5)", "", ["(−2,5)", "(−2,−5)", "(5,2)"], "hard"),
        _q("SAT Stretch: Distance (0,0) to (3,4)?", 5, "3-4-5.", [7, 12, 1], "stretch"),
    ]


def _g6_expr():
    return [
        _q("Evaluate 3x+2 when x=4.", 14, "", [12, 10, 20], "hard"),
        _q("Solve x+7=15.", 8, "", [22, 7, 15], "hard"),
        _q("SAT Stretch: 2(x−3)=10. x?", 8, "", [5, 2, 13], "stretch"),
    ]


def _g6_area():
    return [
        _q("Rectangle 12 by 7. Area?", 84, "", [19, 38, 24], "hard"),
        _q("Rectangle 12 by 7. Perimeter?", 38, "", [84, 19, 24], "hard"),
        _q("SAT Stretch: Cube edge 3. Volume?", 27, "", [9, 18, 6], "stretch"),
    ]


def _g6_data():
    return [
        _q("Mean of 5,7,9?", 7, "", [5, 9, 21], "hard"),
        _q("Mode of 2,2,3,4?", 2, "", [3, 4, "none"], "hard"),
        _q("SAT Stretch: Range of 3,10,6?", 7, "10−3.", [4, 13, 6], "stretch"),
    ]


def _g5():
    return [
        _q("2⅓ + 1½ as improper a/b. a+b?", 29, "23/6.", [23, 17, 11], "hard"),
        _q("(2/3)×(9/4)?", "3/2", "", ["8/27", "6/7", "1"], "hard"),
        _q("Prism 4×3×5 volume?", 60, "", [12, 20, 45], "hard"),
        _q("SAT Stretch: (3/4)÷(1/8)?", 6, "", ["3/32", "2", "24"], "stretch"),
    ]


def _g4():
    return [
        _q("36×25?", 900, "", [800, 725, 1000], "hard"),
        _q("Which rounds to 800 (nearest hundred)?", 760, "", [740, 850, 849], "hard"),
        _q("3/8+1/8?", "1/2", "", ["4/16", "3/16", "2/8"], "hard"),
        _q("SAT Stretch: 756÷9?", 84, "", [74, 86, 94], "stretch"),
    ]


def _g3():
    return [
        _q("6 rows of 8 desks, 5 empty. Students?", 43, "48−5.", [48, 40, 35], "hard"),
        _q("7×8+6?", 62, "", [56, 48, 70], "hard"),
        _q("SAT Stretch: Area 9-by-4 rectangle?", 36, "", [26, 13, 72], "stretch"),
    ]


def _g2():
    return [
        _q("47 stickers +28 −15?", 60, "", [50, 70, 55], "hard"),
        _q("100−37?", 63, "", [73, 67, 53], "hard"),
        _q("SAT Stretch: 2:45 plus 30 minutes?", "3:15", "", ["3:45", "2:75", "3:00"], "stretch"),
    ]


def _g1():
    return [
        _q("9 red + 8 green, eat 3. Left?", 14, "17−3.", [12, 16, 11], "hard"),
        _q("Full ten-frame +6, add 5. Total?", 21, "", [16, 15, 20], "hard"),
        _q("SAT Stretch: Need 20 crayons; have 7+6. How many more?", 7, "", [6, 8, 13], "stretch"),
    ]


def _a1(t):
    if "quadratic" in t:
        return [
            _q("Vertex of y=(x-3)^2+2?", "(3,2)", "h,k from vertex form.", ["(−3,2)", "(3,−2)", "(2,3)"], "hard"),
            _q("SAT Stretch: Roots of x²−5x+6=0?", "2 and 3", "Factor (x−2)(x−3).", ["−2 and −3", "5 and 6", "1 and 6"], "stretch"),
            _q("SAT Stretch: Max of h=−16t²+64t?", 64, "Vertex t=2; h=64.", [32, 16, 48], "stretch"),
        ]
    if "system" in t:
        return [
            _q("x+y=10, x−y=2. x?", 6, "Add: 2x=12.", [4, 8, 5], "hard"),
            _q("SAT Stretch: 3x+2y=16, x−y=1. x?", "18/5", "x=y+1 into first.", [3, 4, 2], "stretch"),
        ]
    if "exponent" in t:
        return _g8_exponents()
    if "factor" in t or "polynomial" in t:
        return [
            _q("Factor x²+5x+6.", "(x+2)(x+3)", "(x+2)(x+3).", ["(x+6)(x+1)", "(x+5)(x+1)", "x(x+5)+6"], "hard"),
            _q("SAT Stretch: Factor 2x²+7x+3.", "(2x+1)(x+3)", "(2x+1)(x+3).", ["(2x+3)(x+1)", "(2x+7)(x+3)", "(x+1)(x+3)"], "stretch"),
        ]
    if "inequal" in t or "equation" in t:
        return _g8_equations() + [
            _q("SAT Stretch: |2x−3|=7. Sum of solutions?", 3, "2x−3=±7 → x=5 or x=−2; sum 3.", [7, 5, 10], "stretch"),
        ]
    if "linear function" in t or "graph" in t:
        return _g8_slope()
    if "data" in t or "sequence" in t:
        return _g8_data() + [
            _q("SAT Stretch: Arithmetic a1=7, d=4. a20?", 83, "7+19·4.", [80, 87, 27], "stretch"),
        ]
    return _g8_equations() + _g8_slope()[:2]


def _geo(t):
    if "circle" in t:
        return [
            _q("Inscribed angle intercepting a 80° arc?", 40, "Half the arc.", [80, 160, 100], "hard"),
            _q("SAT Stretch: Sector area r=6, θ=60°. In terms of π?", "6π", "60/360·π·36=6π.", ["36π", "12π", "3π"], "stretch"),
        ]
    if "similar" in t:
        return [
            _q("Triangles similar with ratio 2:5. Area ratio?", "4:25", "Squares of sides.", ["2:5", "8:125", "4:5"], "hard"),
            _q("SAT Stretch: Shadow 8 ft, pole 6 ft, tree shadow 20 ft. Tree height?", 15, "6/8=h/20.", [12, 18, 14], "stretch"),
        ]
    if "right" in t or "trig" in t or "pythag" in t:
        return _g8_pythag() + [
            _q("SAT Stretch: 30-60-90 short leg 5. Hypotenuse?", 10, "2×short.", ["5√3", 15, "5√2"], "stretch"),
        ]
    if "volume" in t or "area" in t or "coordinate" in t:
        return [
            _q("Prism 4×3×5 volume?", 60, "lwh.", [12, 24, 47], "hard"),
            _q("SAT Stretch: Sphere r=3. Volume in terms of π?", "36π", "4/3πr³=36π.", ["12π", "9π", "108π"], "stretch"),
        ]
    if "congruence" in t:
        return [
            _q("Which is NOT a congruence shortcut?", "SSA", "SSA is ambiguous.", ["SAS", "ASA", "HL"], "hard"),
            _q("SAT Stretch: HL applies only to…", "right triangles", "Right triangles only.", ["all triangles", "isosceles only", "obtuse only"], "stretch"),
        ]
    return [
        _q("Vertical angles are…", "congruent", "Vertical angles are congruent.", ["supplementary always", "complementary", "adjacent"], "hard"),
        _q("SAT Stretch: Parallel lines, corresponding angles 3x+10 and 70. x?", 20, "3x+10=70.", [30, 20 / 3, 80], "stretch"),
    ]


def _trig(t):
    if "unit circle" in t or "radian" in t:
        return [
            _q("cos(2π/3)?", "-1/2", "120° in QII.", ["1/2", "√3/2", "−√3/2"], "hard"),
            _q("SAT Stretch: Arc length r=6, θ=2π/3?", "4π", "s=rθ=4π.", ["2π", "12π", "π"], "stretch"),
        ]
    if "identity" in t:
        return [
            _q("1+tan²θ = ?", "sec²θ", "Pythagorean.", ["csc²θ", "cos²θ", "1"], "hard"),
            _q("SAT Stretch: sin(2θ) if sinθ=3/5, θ in QI?", "24/25", "2sin cos; cos=4/5.", ["6/5", "7/25", "12/25"], "stretch"),
        ]
    if "law of" in t or "sine" in t and "cosine" in t:
        return [
            _q("SSA ambiguous: a=8, A=30°, b=10. How many triangles?", 2, "a>b sin A and a<b.", [0, 1, 3], "hard"),
            _q("SAT Stretch: SAS a=7,b=8,C=60°. c²?", 57, "49+64−2·7·8·1/2=57.", ["113", "15", "64"], "stretch"),
        ]
    if "inverse" in t or "equation" in t:
        return [
            _q("arcsin(1/2) in radians?", "π/6", "Range of arcsin.", ["π/3", "5π/6", "π/2"], "hard"),
            _q("SAT Stretch: Solutions of sin θ=1/2 on [0,2π)?", "π/6 and 5π/6", "Q1 and Q2.", ["π/6 only", "π/3 and 2π/3", "π/6 and 7π/6"], "stretch"),
        ]
    return [
        _q("sin 30°?", "1/2", "", ["√3/2", "√2/2", "1"], "hard"),
        _q("SAT Stretch: Period of y=3 sin(2x)?", "π", "2π/|b|.", ["2π", "4π", "3"], "stretch"),
        _q("SAT Stretch: Amplitude of y=−4 cos(x−π)+1?", 4, "Absolute value of coeff.", [-4, 1, 5], "stretch"),
    ]


def _precalc(t):
    if "conic" in t:
        return [
            _q("x²/9+y²/4=1. Semi-major?", 3, "a=3 along x.", [2, 9, 4], "hard"),
            _q("SAT Stretch: xy=0 is which degenerate conic idea?", "the axes (two lines)", "The coordinate axes.", ["a circle", "a parabola", "a hyperbola"], "stretch"),
        ]
    if "polar" in t or "analytic" in t:
        return [
            _q("Rectangular for r=2, θ=π/3?", "(1, √3)", "x=r cos, y=r sin.", ["(2, π/3)", "(√3, 1)", "(1, 1)"], "hard"),
            _q("SAT Stretch: r=2a cos θ is a circle of diameter…", "2a", "Through origin.", ["a", "4a", "a/2"], "stretch"),
        ]
    if "sequence" in t or "limit" in t:
        return [
            _q("Sum of infinite 1/2+1/4+1/8+…?", 1, "a/(1−r).", ["2", "1/2", "∞"], "hard"),
            _q("SAT Stretch: lim x→0 (sin 3x)/x ?", 3, "3·sinc.", [1, 0, "3x"], "stretch"),
        ]
    if "vector" in t or "matrix" in t or "parametric" in t:
        return [
            _q("Dot product <3,4>·<4,-3>?", 0, "12-12.", [7, 25, -7], "hard"),
            _q("SAT Stretch: Inverse of [[1,1],[0,1]]?", "[[1,−1],[0,1]]", "Shear inverse.", ["[[1,0],[1,1]]", "[[1,1],[0,1]]", "no inverse"], "stretch"),
        ]
    return _a2_explog() + _a2_poly()[:2]


def _ab():
    return [
        _q("lim x→0 (sin x)/x ?", 1, "Standard limit.", [0, "∞", "x"], "hard"),
        _q("d/dx [x³]?", "3x²", "Power rule.", ["3x", "x²", "3x³"], "hard"),
        _q("d/dx [sin x]?", "cos x", "", ["−cos x", "sin x", "−sin x"], "hard"),
        _q("AP Stretch: d/dx [x² sin x]?", "2x sin x + x² cos x", "Product rule.", ["2x cos x", "2x sin x", "x² cos x"], "stretch"),
        _q("AP Stretch: ∫ 2x dx from 0 to 3?", 9, "x² from 0 to 3.", [6, 3, 18], "stretch"),
        _q("AP Stretch: Average value of x² on [0,3]?", 3, "(1/3)∫x²=9/3=3.", [9, 1, 6], "stretch"),
        _q("AP Stretch: If f'(x)>0 on (a,b), f is…", "increasing", ["concave up", "decreasing", "constant"], "stretch"),
        _q("MVT: f(0)=1, f(2)=7. Some c in (0,2) with f'(c)=?", 3, "(7−1)/2.", [6, 4, 8], "hard"),
        _q("AP Stretch: Volume of y=x rotated about x-axis on [0,2] (disks, π)?", "8π/3", "π∫x² dx=π(8/3).", ["4π", "2π", "16π/3"], "stretch"),
    ]


def _bc(t=""):
    """Unit-specific BC padding so series never lands on polar (and vice versa)."""
    t = (t or "").lower()
    if "euler" in t or "logistic" in t or "mixed frq" in t:
        return [
            _q("Euler: y'=y, y(0)=1, h=0.5. After one step y₁ is?", 1.5, "y+hy'=1+0.5.", [2, 0.5, 1.25], "hard"),
            _q("If dy/dt=2y(5−y), the carrying capacity is?", 5, "Equilibrium y=L.", [2, 10, 0], "hard"),
            _q("AP Stretch: Two Euler steps for y'=x+y, y(0)=1, h=0.1 give y(0.2)≈?", 1.22, "y1=1.1, y2=1.22.", [1.2, 1.21, 1.3], "stretch"),
        ]
    if "polar area" in t or "parametric applications" in t:
        return [
            _q("Polar area of r=2 on [0,π/2] is?", "π", "(1/2)∫4 dθ=π.", ["2π", "4", "π/2"], "hard"),
            _q("One petal of r=cos 2θ has area?", "π/8", "(1/2)∫ cos²2θ on a petal.", ["π/4", "π/2", "π/16"], "hard"),
            _q("AP Stretch: Polar area of one petal of the rose r=2 cos 2θ?", "π/2", "a=2 so πa²/8=π/2.", ["π", "π/4", "π/8"], "stretch"),
        ]
    if "taylor" in t or "maclaurin" in t:
        return [
            _q("Maclaurin for e^x through degree 2?", "1+x+x²/2", "1+x+x²/2!.", ["1+x+x²", "1+x²/2", "x+x²/2"], "hard"),
            _q("AP Stretch: Lagrange bound |R₂(1)| for e^x on [0,1] is at most?", "e/6", "M=e, 1³/3!=e/6.", ["1/6", "e/2", "e"], "stretch"),
        ]
    if "power series" in t or "ratio, root" in t:
        return [
            _q("Radius of Σ x^n/n! is?", "∞", "Ratio limit 0.", [1, 0, "1/e"], "hard"),
            _q("AP Stretch: Interval of Σ (x−2)^n/n is?", "[1,3)", "Radius 1; ln at x=3 diverges, x=1 converges.", ["(1,3)", "[1,3]", "(1,3]"], "stretch"),
        ]
    if "sequences" in t or "series tests" in t:
        return [
            _q("Geometric Σ (1/3)^n from n=0 to ∞ equals?", "3/2", "1/(1−1/3).", ["1/3", "1", "3"], "hard"),
            _q("AP Stretch: Σ (−1)^{n+1}/n^2 converges…", "absolutely", "p=2>1.", ["conditionally", "diverges", "to 0"], "stretch"),
        ]
    if "arc length" in t and "polar" not in t:
        return [
            _q("Arc length of y=x on [0,1] is?", "√2", "∫√(1+1) dx.", ["1", "2", "π/4"], "hard"),
            _q("AP Stretch: Surface of y=x on [0,1] about the x-axis?", "π√2", "2π∫x√2 dx=π√2.", ["2π", "π", "√2"], "stretch"),
        ]
    if "advanced integration" in t:
        return [
            _q("∫ x e^x dx (parts, +C)?", "e^x(x−1)+C", "u=x, dv=e^x dx.", ["e^x + C", "x e^x + C", "e^x(x+1)+C"], "hard"),
            _q("AP Stretch: ∫_1^∞ dx/x^2 equals?", 1, "lim b→∞ (1−1/b)=1.", [0, "∞", "1/2"], "stretch"),
        ]
    return [
        _q("If x=t², y=t³ (t≠0), dy/dx equals?", "3t/2", "(3t²)/(2t).", ["3t", "2t/3", "t"], "hard"),
        _q("Speed of r(t)=⟨t,t²⟩ at t=1?", "√5", "|⟨1,2⟩|.", ["5", "3", "√2"], "hard"),
        _q("AP Stretch: Polar dy/dx for r=2 cos θ at θ=π/4?", 0, "Numerator of dy/dθ vanishes.", [1, "undefined", "√2"], "stretch"),
    ]

