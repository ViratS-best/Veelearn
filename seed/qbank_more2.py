"""Third bank module: olympiad and contest styles, all-grade science, college
engineering and coding.

The contest tracks (MATHCOUNTS, AMC 8/10/12, AIME, USAMO, IMO) are *original*
questions written in the style of each contest. Nothing is copied from MAA or
MATHCOUNTS: those problems are copyrighted and the contests are still used for
scoring. The same goes for SAT/ACT material.

Every item keeps the bank anatomy: four options, a specific `why` on each
distractor, two hints and solution steps. Diagrams are authored SVGs.
"""

from __future__ import annotations

from seed.qbank_more import (
    ACCENT,
    INK,
    M,
    bars,
    circle_r,
    code_block,
    grid,
    numline,
    svg,
    table,
    triangle_right,
    wave_diagram,
)


# --------------------------------------------------------------------------- #
# Extra diagram builders for this module
# --------------------------------------------------------------------------- #


def circuit(alt, r_label="4 Ω", v_label="12 V"):
    body = (
        "<g fill='none' stroke='%s' stroke-width='2'>"
        "<path d='M60 150 V70 H130'/><path d='M190 70 H260 V150'/><path d='M60 150 H260'/>"
        "<path d='M130 60 H190 V80 H130 Z' fill='#fffdf9'/></g>"
        "<text x='140' y='75' font-size='12' fill='%s'>%s</text>"
        "<text x='30' y='105' font-size='12' fill='%s'>%s</text>"
        "<path d='M48 92 H72 M60 80 V104' stroke='%s' stroke-width='2'/>" % (INK, INK, r_label, INK, v_label, ACCENT)
    )
    return svg(body, alt)


def beam(alt, load="20 N", span="4 m"):
    body = (
        "<path d='M40 120 H280' stroke='%s' stroke-width='3'/>"
        "<path d='M40 120 L30 140 H50 Z' fill='%s'/>"
        "<path d='M280 120 L270 140 H290 Z' fill='%s'/>"
        "<path d='M160 60 V116' stroke='%s' stroke-width='2'/>"
        "<path d='M152 60 H168' stroke='%s' stroke-width='2'/>"
        "<text x='172' y='78' font-size='12' fill='%s'>%s</text>"
        "<text x='140' y='162' font-size='12' fill='%s'>%s</text>" % (INK, ACCENT, ACCENT, INK, INK, INK, load, INK, span)
    )
    return svg(body, alt)


def stress_strain(alt):
    body = (
        "<path d='M50 160 H280 M50 160 V40' stroke='%s' stroke-width='1.5'/>"
        "<path d='M50 160 L180 50 L250 60' fill='none' stroke='%s' stroke-width='2.4'/>"
        "<circle cx='180' cy='50' r='4' fill='%s'/>"
        "<text x='188' y='44' font-size='12' fill='%s'>yield</text>"
        "<text x='210' y='182' font-size='12' fill='%s'>strain</text>"
        "<text x='20' y='40' font-size='12' fill='%s'>stress</text>" % (INK, ACCENT, ACCENT, INK, INK, INK)
    )
    return svg(body, alt)


def force_arrow(alt, label="10 N"):
    body = (
        "<rect x='120' y='84' width='80' height='40' rx='6' fill='%s' fill-opacity='0.15' stroke='%s' stroke-width='2'/>"
        "<path d='M200 104 H270' stroke='%s' stroke-width='3'/>"
        "<path d='M270 104 L258 97 V111 Z' fill='%s'/>"
        "<text x='222' y='94' font-size='12' fill='%s'>%s</text>" % (INK, INK, ACCENT, ACCENT, INK, label)
    )
    return svg(body, alt)


def cell_diagram(alt):
    body = (
        "<rect x='60' y='40' width='200' height='120' rx='16' fill='%s' fill-opacity='0.08' stroke='%s' stroke-width='2'/>"
        "<circle cx='130' cy='100' r='26' fill='%s' fill-opacity='0.2' stroke='%s' stroke-width='1.6'/>"
        "<text x='112' y='104' font-size='11' fill='%s'>nucleus</text>"
        "<path d='M60 130 Q90 118 118 130 T176 130 T236 130' fill='none' stroke='%s' stroke-width='1.6'/>"
        "<text x='180' y='52' font-size='11' fill='%s'>membrane</text>" % (ACCENT, INK, ACCENT, INK, INK, INK, INK)
    )
    return svg(body, alt)


def phases(alt):
    body = "<text x='30' y='100' font-size='13' fill='%s'></text>" % INK
    labels = ["solid", "liquid", "gas"]
    for i, label in enumerate(labels):
        x = 48 + i * 90
        body += "<rect x='%d' y='70' width='60' height='54' rx='8' fill='%s' fill-opacity='%.2f' stroke='%s' stroke-width='1.6'/>" % (
            x,
            ACCENT,
            0.1 + 0.12 * i,
            INK,
        )
        body += "<text x='%d' y='146' font-size='11.5' fill='%s'>%s</text>" % (x + 8, INK, label)
    return svg(body, alt)


# --------------------------------------------------------------------------- #
# Olympiad style: AIME
# --------------------------------------------------------------------------- #

_AIME = [
    # ------------------------------------------------------------ aime.nt
    M("aime.nt", 3,
      "How many positive divisors does 72 have?",
      "12",
      [("6", "That counts only the divisors of 2³ or only those of 3²."),
       ("8", "That multiplies 4 by 2 instead of by 3."),
       ("9", "That uses the exponents 3 and 3 instead of 3 and 2.")],
      ["Write 72 = 2ᵃ · 3ᵇ.", "The divisor count is (a + 1)(b + 1)."],
      ["72 = 2³ · 3².", "(3 + 1)(2 + 1) = 12 divisors."]),

    M("aime.nt", 4,
      "What is the remainder when 3¹⁰⁰ is divided by 7?",
      "4",
      [("1", "That is the remainder of 3⁹⁶, not 3¹⁰⁰."),
       ("2", "That comes from using 3⁵ ≡ 5 mod 7 and then slipping a step."),
       ("6", "That is the remainder of 3³.")],
      ["Powers of 3 mod 7 repeat every 6 steps.", "100 = 6 × 16 + 4, so 3¹⁰⁰ ≡ 3⁴."],
      ["3⁴ = 81.", "81 = 11 × 7 + 4, so the remainder is 4."]),

    M("aime.nt", 4,
      "How many integers from 1 to 100 are divisible by 2 or by 5?",
      "60",
      [("50", "That counts only the multiples of 2."),
       ("70", "That adds 50 and 20 without removing the overlap."),
       ("55", "That double counts some multiples of 10 and misses others.")],
      ["Inclusion–exclusion: |A ∪ B| = |A| + |B| − |A ∩ B|.", "Multiples of 10 are counted twice."],
      ["50 + 20 − 10.", "That gives 60."]),

    M("aime.nt", 3,
      "What is gcd(84, 126)?",
      "42",
      [("21", "21 divides both, but 84/21 = 4 and 126/21 = 6 still share a factor of 2."),
       ("14", "126/14 = 9 and 84/14 = 6, so it works, but it is smaller than the true gcd."),
       ("84", "84 does not divide 126.")],
      ["Use Euclid: 126 − 84 = 42.", "Then check 84 ÷ 42."],
      ["126 = 84 + 42 and 84 = 2 × 42.", "So gcd(84, 126) = 42."]),

    M("aime.nt", 4,
      "What is the smallest positive integer with exactly 6 positive divisors?",
      "12",
      [("6", "6 has only 4 divisors: 1, 2, 3, 6."),
       ("8", "8 has 4 divisors: 1, 2, 4, 8."),
       ("16", "16 has 5 divisors: 1, 2, 4, 8, 16.")],
      ["Six divisors means a prime power p⁵ or a product p²q.", "Try the smallest primes."],
      ["2² × 3 = 12 gives (2 + 1)(1 + 1) = 6 divisors.", "12 is smaller than 2⁵ = 32."],
      visual=bars([("6", 4), ("8", 4), ("12", 6), ("16", 5)], "Divisor counts for 6, 8, 12 and 16")),

    # --------------------------------------------------------- aime.combo
    M("aime.combo", 3,
      "How many 3-letter strings can be made from the letters A, B, C, D if repeats are allowed?",
      "64",
      [("24", "That is the count without repeats."),
       ("12", "That is 4 × 3, treating only two positions."),
       ("81", "That uses 3 choices per position instead of 4.")],
      ["Each of the three positions has 4 independent choices.", "Multiply: 4 × 4 × 4."],
      ["4³ = 64.", "So there are 64 strings."]),

    M("aime.combo", 4,
      "In how many ways can 5 people sit around a round table, counting arrangements that differ only by rotation as the same?",
      "24",
      [("120", "That is 5!, which counts every rotation as a different arrangement."),
       ("12", "That halves 24 for reflection, which round-table seating does not do."),
       ("60", "That divides 120 by 2 for no reason.")],
      ["Fix one person to remove the rotational symmetry.", "The other four can be arranged in 4! ways."],
      ["4! = 24.", "So there are 24 distinct seatings."]),

    M("aime.combo", 4,
      "How many diagonals does a convex octagon have?",
      "20",
      [("16", "That is the number of sides plus 8, mixing edges and diagonals."),
       ("28", "That is C(8,2), which counts the sides as well."),
       ("24", "That is 3 × 8, the count for a hexagon scaled up.")],
      ["Each vertex connects to 5 non-adjacent vertices.", "That counts every diagonal twice."],
      ["8 × 5 = 40, then divide by 2.", "So there are 20 diagonals."]),

    M("aime.combo", 3,
      "What is C(7, 2)?",
      "21",
      [("14", "That is 7 × 2, ignoring the division by 2!."),
       ("42", "That is 7 × 6 without dividing by 2."),
       ("49", "That is 7².")],
      ["C(n, k) = n! / (k!(n − k)!).", "C(7, 2) = 7 × 6 / 2."],
      ["42 / 2 = 21.", "So C(7, 2) = 21."]),

    M("aime.combo", 4,
      "A robot walks on a 3 × 3 grid from the bottom-left corner to the top-right, moving only right or up. How many routes are there?",
      "20",
      [("6", "That counts only the routes with no repeated direction."),
       ("9", "That is the number of grid squares, not routes."),
       ("12", "That is the number of edges in the grid.")],
      ["Every route is 3 rights and 3 ups in some order.", "Choose which 3 of the 6 steps are rights."],
      ["C(6, 3) = 20.", "So there are 20 routes."],
      visual=grid(3, 3, "A three by three grid with the start and end corners marked")),

    # ----------------------------------------------------------- aime.geo
    M("aime.geo", 3,
      "What is the area of a triangle with sides 5, 12 and 13?",
      "30",
      [("60", "That is base × height without halving for a triangle."),
       ("65", "That is the product of the two shorter sides without halving."),
       ("78", "That is the perimeter plus the hypotenuse.")],
      ["5-12-13 is a right triangle, so the legs are perpendicular.", "Area = ½ × 5 × 12."],
      ["5² + 12² = 169 = 13², so the legs are 5 and 12.", "½ × 60 = 30."]),

    M("aime.geo", 4,
      "A circle has circumference 12π. What is its area?",
      "36π",
      [("12π", "That is the circumference, not the area."),
       ("24π", "That is 2πr with r = 12."),
       ("144π", "That uses the diameter as the radius.")],
      ["Find the radius from C = 2πr.", "12π = 2πr gives r = 6."],
      ["Area = πr² = 36π."]),

    M("aime.geo", 4,
      "What is the sum of the interior angles of a hexagon?",
      "720°",
      [("540°", "That is the pentagon, one side fewer."),
       ("900°", "That is the heptagon, one side more."),
       ("360°", "That is the exterior angle sum for any convex polygon.")],
      ["Interior sum = (n − 2) × 180°.", "A hexagon has n = 6."],
      ["(6 − 2) × 180° = 4 × 180°.", "That is 720°."]),

    M("aime.geo", 3,
      "In a 6-8-10 right triangle, what is the altitude drawn to the hypotenuse?",
      "4.8",
      [("6", "That is one of the legs, not the altitude."),
       ("5", "That is half the hypotenuse, which is the median, not the altitude."),
       ("8", "That is the other leg.")],
      ["Area = ½ × 6 × 8 = ½ × 10 × h.", "Solve for h."],
      ["24 = ½ × 10 × h = 5h.", "h = 4.8."],
      visual=triangle_right("6", "8", "10", "Right triangle with legs six and eight and hypotenuse ten")),

    M("aime.geo", 4,
      "Two circles with radii 3 and 5 are externally tangent. What is the distance between their centres?",
      "8",
      [("2", "That is the difference of the radii, which would be internal tangency."),
       ("4", "That is only the smaller radius plus one."),
       ("15", "That is the product of the radii.")],
      ["External tangency means the circles touch outside each other.", "The centres are one radius plus the other apart."],
      ["3 + 5 = 8.", "So the centres are 8 apart."]),
]

# --------------------------------------------------------------------------- #
# USAMO / IMO style
# --------------------------------------------------------------------------- #

_OLY = [
    # ------------------------------------------------------- usamo.algebra
    M("usamo.algebra", 3,
      "Given x + 1/x = 3, find x² + 1/x².",
      "7",
      [("9", "That squares the equation but forgets to subtract the cross term 2."),
       ("6", "That subtracts 3 instead of 2."),
       ("11", "That adds the cross term instead of subtracting it.")],
      ["Square both sides of x + 1/x = 3.", "(a + b)² = a² + 2ab + b² with ab = 1."],
      ["x² + 2 + 1/x² = 9.", "So x² + 1/x² = 7."]),

    M("usamo.algebra", 4,
      "For how many positive integers n is n² + n a prime number?",
      "1",
      [("0", "n = 1 gives 2, which is prime."),
       ("2", "n = 2 gives 6, which is not prime."),
       ("Infinitely many", "n² + n always factors as n(n + 1).")],
      ["Factor n² + n.", "A product of two positive integers is prime only if one of them is 1."],
      ["n² + n = n(n + 1).", "Only n = 1 makes the product 1 × 2 = 2 prime."]),

    M("usamo.algebra", 4,
      "If a + b = 5 and ab = 6, what is a³ + b³?",
      "35",
      [("65", "That is (a + b)³, ignoring the cross terms."),
       ("125", "That is 5³, which assumes a and b add without any product."),
       ("95", "That subtracts 3ab instead of 3ab(a + b).")],
      ["Use a³ + b³ = (a + b)³ − 3ab(a + b).", "Substitute 5 and 6."],
      ["125 − 3(6)(5) = 125 − 90.", "That gives 35."]),

    M("usamo.algebra", 3,
      "Solve |x − 2| < 5.",
      "−3 < x < 7",
      [("x < 7", "That keeps only one side of the absolute value."),
       ("x > −3", "That keeps only the other side."),
       ("−7 < x < 3", "That centres the interval on 0 instead of 2.")],
      ["|x − 2| < 5 means the distance from x to 2 is under 5.", "Write −5 < x − 2 < 5."],
      ["Add 2 across: −3 < x < 7."],
      visual=numline([(0.14, "−3"), (0.6, "7")], "Number line showing the interval from minus three to seven")),

    M("usamo.algebra", 4,
      "What is the smallest positive integer x with x ≡ 3 (mod 4) and x ≡ 5 (mod 7)?",
      "19",
      [("11", "11 ≡ 3 (mod 4) but 11 ≡ 4 (mod 7)."),
       ("23", "23 ≡ 2 (mod 7)."),
       ("15", "15 ≡ 3 (mod 4) but 15 ≡ 1 (mod 7).")],
      ["Numbers ≡ 3 (mod 4) are 3, 7, 11, 15, 19, ….", "Check each against mod 7."],
      ["19 = 4 × 4 + 3 and 19 = 2 × 7 + 5.", "So x = 19."]),

    # ---------------------------------------------------------- usamo.nt
    M("usamo.nt", 3,
      "How many trailing zeros does 20! have?",
      "4",
      [("2", "That counts only the factor 100 inside 20!."),
       ("3", "That counts the multiples of 5 but stops one short."),
       ("5", "That counts 5, 10, 15, 20 and then adds an extra.")],
      ["Each trailing zero needs a factor of 10 = 2 × 5.", "Count factors of 5 in 20!."],
      ["⌊20/5⌋ = 4 and ⌊20/25⌋ = 0.", "So there are 4 trailing zeros."]),

    M("usamo.nt", 4,
      "What is 2¹⁰ mod 1000?",
      "24",
      [("124", "That subtracts 900 instead of 1000."),
       ("512", "That is 2⁹, one power short."),
       ("1024", "That is 2¹⁰ itself, not its remainder mod 1000.")],
      ["2¹⁰ = 1024, then subtract the largest multiple of 1000.", "1024 − 1000 = 24."],
      ["1024 mod 1000.", "That leaves 24."]),

    M("usamo.nt", 4,
      "How many primes are there between 90 and 100?",
      "1",
      [("0", "97 is prime, so the count is not zero."),
       ("2", "99 = 9 × 11, so it is not prime."),
       ("3", "91 = 7 × 13 and 93 = 3 × 31 are not prime.")],
      ["Test each number: 91, 92, 93, 94, 95, 96, 97, 98, 99.", "Primes are not divisible by 2, 3, 5 or 7."],
      ["91 = 7 × 13, 93 = 3 × 31, 95 = 5 × 19, 99 = 9 × 11.", "Only 97 is prime."]),

    M("usamo.nt", 3,
      "What is the largest prime factor of 210?",
      "7",
      [("5", "5 is a factor, but 7 is larger."),
       ("3", "3 is a factor, but smaller than 7."),
       ("11", "11 does not divide 210.")],
      ["Factor 210 into primes.", "210 = 2 × 3 × 5 × 7."],
      ["The prime factors are 2, 3, 5 and 7.", "The largest is 7."]),

    M("usamo.nt", 4,
      "For how many integers n from 1 to 30 is n² − 1 divisible by 8?",
      "15",
      [("10", "That counts only multiples of 4."),
       ("12", "That counts even n, but even n give n² − 1 odd."),
       ("30", "n² − 1 is not divisible by 8 for every n.")],
      ["n² − 1 = (n − 1)(n + 1), a product of two numbers two apart.", "Check odd and even n separately."],
      ["For odd n, n − 1 and n + 1 are consecutive even numbers, so one is divisible by 4.", "Half of 1…30 is odd: 15 values."]),

    # ------------------------------------------------------------ imo.geo
    M("imo.geo", 3,
      "In a cyclic quadrilateral, opposite angles are…",
      "supplementary",
      [("equal", "That is true for a parallelogram, not for every cyclic quadrilateral."),
       ("complementary", "Complementary angles add to 90°, which would force a right angle pair."),
       ("always right angles", "Only a rectangle inscribed in a circle has all right angles.")],
      ["Use the inscribed angle theorem.", "Opposite angles subtend arcs that add to the whole circle."],
      ["Together the two arcs are 360°, so the angles add to 180°.", "That means they are supplementary."]),

    M("imo.geo", 4,
      "What is the area of an equilateral triangle with side 6?",
      "9√3",
      [("18√3", "That uses ½ × 6 × 6√3, which double counts the height."),
       ("36", "That is the square of the side."),
       ("12√3", "That uses side 4√3 in the area formula.")],
      ["Area = (√3/4) × side².", "6² = 36."],
      ["(√3/4) × 36 = 9√3."]),

    M("imo.geo", 4,
      "From a point 10 cm from the centre of a circle of radius 6, a tangent is drawn. How long is the tangent segment?",
      "8",
      [("4", "That subtracts the radius from the distance instead of using Pythagoras."),
       ("6", "That is the radius."),
       ("10", "That is the distance to the centre.")],
      ["The radius meets the tangent at a right angle.", "Use 10² = 6² + t²."],
      ["100 − 36 = 64.", "t = 8."]),
]


# --------------------------------------------------------------------------- #
# More MATHCOUNTS and AMC items (the existing skills keep their questions)
# --------------------------------------------------------------------------- #

_CONTEST = [
    # ---------------------------------------------------------- mc.sprint
    M("mc.sprint", 2,
      "What is 15% of 60?",
      "9",
      [("6", "That is 10% of 60."),
       ("12", "That is 20% of 60."),
       ("15", "That copies the percent instead of applying it.")],
      ["10% of 60 is 6 and 5% is 3.", "Add them."],
      ["6 + 3 = 9."]),

    M("mc.sprint", 2,
      "How many minutes are there from 2:45 to 3:20?",
      "35",
      [("25", "That subtracts 20 from 45 and ignores the hour change."),
       ("45", "That adds the minutes instead of finding the gap."),
       ("55", "That counts a full hour and subtracts the wrong way.")],
      ["Count up to 3:00 first.", "2:45 to 3:00 is 15 minutes."],
      ["15 + 20 = 35 minutes."]),

    M("mc.sprint", 3,
      "The average of five numbers is 12. What is their sum?",
      "60",
      [("55", "That is the average of the first ten integers, not this sum."),
       ("17", "That adds the count to the average."),
       ("12", "That is the average itself.")],
      ["Sum = average × count.", "12 × 5."],
      ["12 × 5 = 60."]),

    M("mc.sprint", 3,
      "A shirt costs $24 after a 20% discount. What was the original price?",
      "$30",
      [("$28.80", "That adds 20% of the sale price, which is not the same base."),
       ("$32", "That is a 25% discount from $32."),
       ("$44", "That adds the 20 dollars of discount twice.")],
      ["The sale price is 80% of the original.", "Divide 24 by 0.8."],
      ["24 ÷ 0.8 = 30.", "Check: 30 − 6 = 24."]),

    M("mc.sprint", 4,
      "How many two-digit positive integers contain the digit 7?",
      "18",
      [("10", "That counts only the 70s and misses 17, 27, …."),
       ("19", "That counts 77 twice."),
       ("20", "That includes 07, which is not a two-digit number.")],
      ["Count the 70s, then the numbers ending in 7.", "77 is in both groups."],
      ["10 numbers in the 70s, plus 8 more ending in 7 outside the 70s (17, 27, 37, 47, 57, 67, 87, 97).", "10 + 8 = 18."]),

    # ---------------------------------------------------------- mc.target
    M("mc.target", 3,
      "How many three-digit numbers can be made using only odd digits, if repeats are allowed?",
      "125",
      [("60", "That is the count without repeats."),
       ("100", "That uses 5 choices for two positions and 4 for the third."),
       ("64", "That uses 4 digits per position.")],
      ["The odd digits are 1, 3, 5, 7, 9.", "Each of the three positions has 5 choices."],
      ["5 × 5 × 5 = 125."]),

    M("mc.target", 4,
      "The product of three consecutive integers is 120. What is the largest of the three?",
      "6",
      [("5", "4 × 5 × 6 = 120, and 5 is the middle number, not the largest."),
       ("8", "6 × 7 × 8 is far more than 120."),
       ("10", "8 × 9 × 10 is much more than 120.")],
      ["The cube root of 120 is about 5, so the middle number is near 5.", "Try 4 × 5 × 6."],
      ["4 × 5 × 6 = 120.", "The largest is 6."]),

    M("mc.target", 4,
      "How many zeros are at the end of 15!?",
      "3",
      [("2", "That counts only multiples of 10."),
       ("4", "That is the count for 20!."),
       ("1", "That counts only the number 10 itself.")],
      ["Count factors of 5 in 15!.", "⌊15/5⌋ = 3."],
      ["5, 10 and 15 each bring a factor of 5, and there are plenty of 2s.", "So there are 3 trailing zeros."]),

    M("mc.target", 3,
      "A cube has edges of length 3 cm. What is its total surface area?",
      "54 cm²",
      [("27 cm²", "That is the volume, 3³."),
       ("36 cm²", "That counts four faces instead of six."),
       ("18 cm²", "That is 2 × 3², only two faces.")],
      ["A cube has 6 square faces.", "Each face is 3 × 3."],
      ["6 × 9 = 54 cm²."]),

    M("mc.target", 4,
      "What is the units digit of 7²⁵?",
      "7",
      [("1", "That is the units digit when the exponent is a multiple of 4."),
       ("3", "That is 7³'s units digit."),
       ("9", "That is 7²'s units digit.")],
      ["The units digits of powers of 7 repeat 7, 9, 3, 1.", "25 mod 4 = 1."],
      ["25 = 4 × 6 + 1, so the pattern lands on its first entry.", "The units digit is 7."]),

    # ----------------------------------------------------------- amc8.geo
    M("amc8.geo", 2,
      "A rectangle is 7 cm by 4 cm. What is the square of its diagonal?",
      "65",
      [("33", "That adds the sides and then adds 11 again."),
       ("11", "That adds the sides instead of squaring them."),
       ("28", "That is the area, not the diagonal.")],
      ["Diagonal² = length² + width².", "49 + 16."],
      ["49 + 16 = 65."],
      visual=triangle_right("4", "7", "?", "Right triangle with legs four and seven and an unknown hypotenuse")),

    M("amc8.geo", 3,
      "A square has area 64. What is its perimeter?",
      "32",
      [("16", "That is twice the side, not four times it."),
       ("64", "That is the area."),
       ("24", "That is three sides of length 8.")],
      ["Find the side length first.", "8² = 64, so the side is 8."],
      ["4 × 8 = 32."]),

    M("amc8.geo", 3,
      "A triangle has angles 2x, 3x and 5x. What is x?",
      "18°",
      [("20°", "That makes the angles add to 200°."),
       ("15°", "That makes the angles add to 150°."),
       ("30°", "That makes the angles add to 300°.")],
      ["The angles of a triangle add to 180°.", "2x + 3x + 5x = 10x."],
      ["10x = 180, so x = 18."]),

    M("amc8.geo", 2,
      "How many edges does a cube have?",
      "12",
      [("6", "That is the number of faces."),
       ("8", "That is the number of vertices."),
       ("24", "That counts each edge twice, once per face.")],
      ["Count the edges around the top, the bottom, and the vertical ones.", "4 + 4 + 4."],
      ["4 top, 4 bottom, 4 vertical.", "That is 12 edges."]),

    M("amc8.geo", 3,
      "A circle has diameter 10. What is its circumference?",
      "10π",
      [("5π", "That uses the radius instead of the diameter."),
       ("25π", "That is the area."),
       ("20π", "That doubles the diameter.")],
      ["C = πd.", "The diameter is 10."],
      ["C = 10π."],
      visual=circle_r("5", "Circle with radius five, diameter ten")),

    # -------------------------------------------------------- amc10.count
    M("amc10.count", 3,
      "How many ways can 3 students be chosen from a group of 8?",
      "56",
      [("24", "That is 8 × 3, which overcounts and ignores order."),
       ("336", "That is 8 × 7 × 6, which counts orderings."),
       ("512", "That is 8³.")],
      ["Order does not matter, so this is a combination.", "C(8, 3) = 8 × 7 × 6 / 6."],
      ["336 ÷ 6 = 56."]),

    M("amc10.count", 4,
      "How many three-digit positive integers are even?",
      "450",
      [("400", "That uses 4 hundreds digits and 100 endings."),
       ("500", "That assumes half of 1000, including one- and two-digit numbers."),
       ("900", "That is the count of all three-digit numbers.")],
      ["Three-digit numbers run from 100 to 999: 900 of them.", "Exactly half are even."],
      ["900 ÷ 2 = 450."]),

    M("amc10.count", 3,
      "How many subsets does a 5-element set have?",
      "32",
      [("10", "That counts only pairs."),
       ("25", "That is 5², treating choices as dependent."),
       ("16", "That is the count for a 4-element set.")],
      ["Each element is either in or out.", "That gives 2⁵."],
      ["2⁵ = 32."]),

    M("amc10.count", 4,
      "Two fair dice are rolled. What is the probability that the sum is 7?",
      "1/6",
      [("1/12", "That counts only half of the six winning pairs."),
       ("7/36", "That counts 7 pairs instead of 6."),
       ("1/9", "That is 4/36, the chance of a sum of 5.")],
      ["List the pairs that sum to 7: (1,6), (2,5), (3,4) and reverses.", "There are 6 winning pairs out of 36."],
      ["6/36 = 1/6."],
      visual=table(["sum", "pairs"], [["7", "6"], ["all", "36"]], "Table showing six pairs sum to seven out of thirty-six")),

    M("amc10.count", 4,
      "In how many different orders can 4 distinct books be placed on a shelf?",
      "24",
      [("4", "That is the number of books."),
       ("16", "That is 4²."),
       ("64", "That is 4³.")],
      ["Use the factorial of the number of books.", "4! = 4 × 3 × 2 × 1."],
      ["4! = 24."]),

    # --------------------------------------------------------- amc12.trig
    M("amc12.trig", 2,
      "What is sin(90°)?",
      "1",
      [("0", "That is sin(0°)."),
       ("1/2", "That is sin(30°)."),
       ("−1", "That is sin(270°).")],
      ["At 90° the unit-circle point is (0, 1).", "sin is the y-coordinate."],
      ["sin(90°) = 1."]),

    M("amc12.trig", 3,
      "If sin θ = 3/5 and θ is in the first quadrant, what is cos θ?",
      "4/5",
      [("3/4", "That is tan θ, not cos θ."),
       ("5/4", "That is greater than 1, impossible for a cosine."),
       ("−4/5", "In the first quadrant the cosine is positive.")],
      ["Use sin²θ + cos²θ = 1.", "cos²θ = 1 − 9/25."],
      ["cos²θ = 16/25, so cos θ = 4/5."],
      visual=triangle_right("4", "3", "5", "Right triangle with legs three and four and hypotenuse five")),

    M("amc12.trig", 3,
      "Which expression equals cos(2θ)?",
      "1 − 2 sin²θ",
      [("1 + 2 sin²θ", "The double-angle identity subtracts the sine term."),
       ("2 sin²θ − 1", "That is the negative of cos(2θ)."),
       ("2 cos²θ", "The identity is 2cos²θ − 1, not 2cos²θ.")],
      ["Use cos(2θ) = 1 − 2 sin²θ, or 2cos²θ − 1.", "Both are standard double-angle forms."],
      ["cos(2θ) = 1 − 2 sin²θ."]),

    M("amc12.trig", 4,
      "What is the period of sin(3x)?",
      "2π/3",
      [("2π", "That is the period of sin x, before compressing."),
       ("π/3", "That divides by 6 instead of 3."),
       ("6π", "That multiplies by 3 instead of dividing.")],
      ["The period of sin(kx) is 2π/k.", "k = 3."],
      ["2π/3."],
      visual=wave_diagram("A sine wave with its period marked")),

    M("amc12.trig", 4,
      "If tan θ = 3/4 and θ is in the first quadrant, what is sin θ?",
      "3/5",
      [("4/5", "That is cos θ."),
       ("5/3", "That is the reciprocal of sin θ."),
       ("4/3", "That is the reciprocal of tan θ.")],
      ["Tangent is opposite/adjacent, so use a 3-4-5 triangle.", "The hypotenuse is 5."],
      ["sin θ = opposite/hypotenuse = 3/5."]),
]

# --------------------------------------------------------------------------- #
# Science (all grades)
# --------------------------------------------------------------------------- #

_SCI = [
    # ---------------------------------------------------------- sci.living
    M("sci.living", 1,
      "Which of these is a living thing?",
      "A mushroom",
      [("A rock", "Rocks do not grow, reproduce or use energy."),
       ("A cloud", "Clouds are water droplets, not organisms."),
       ("A river", "A river moves, but it is not alive.")],
      ["Living things grow, reproduce and need energy.", "Which option is an organism?"],
      ["A mushroom is a fungus, which is an organism.", "So it is the living thing."],
      visual=cell_diagram("A cell with its nucleus and membrane labelled")),

    M("sci.living", 2,
      "Plants make their own food using sunlight. This process is called…",
      "photosynthesis",
      [("respiration", "Respiration releases energy from food; it does not make food."),
       ("digestion", "Plants do not digest food the way animals do."),
       ("transpiration", "Transpiration is water leaving the leaves.")],
      ["The word starts with 'photo', meaning light.", "Plants combine sunlight, water and carbon dioxide."],
      ["Photosynthesis turns light energy into chemical energy in sugar."]),

    M("sci.living", 2,
      "Which part of a plant takes up water from the soil?",
      "the roots",
      [("the leaves", "Leaves lose water and make food; they do not absorb soil water."),
       ("the flowers", "Flowers are for reproduction."),
       ("the seeds", "Seeds store food for a new plant.")],
      ["It is the part underground.", "Root hairs absorb water and minerals."],
      ["Roots take up water from the soil."]),

    M("sci.living", 3,
      "Fungi get their energy by…",
      "breaking down dead material",
      [("photosynthesis", "Fungi have no chlorophyll, so they cannot photosynthesise."),
       ("hunting prey", "Most fungi do not hunt."),
       ("filtering water", "Fungi are not filter feeders.")],
      ["Think of mould on bread.", "They are decomposers."],
      ["Fungi absorb nutrients from dead matter, which recycles it into the soil."]),

    M("sci.living", 4,
      "An animal that eats only plants is a…",
      "herbivore",
      [("carnivore", "Carnivores eat other animals."),
       ("omnivore", "Omnivores eat both plants and animals."),
       ("decomposer", "Decomposers break down dead matter.")],
      ["The prefix 'herbi' relates to plants.", "Cows and rabbits are examples."],
      ["Plant-only eaters are herbivores."]),

    M("sci.matter", 1,
      "Which of these is a state of matter?",
      "Solid",
      [("Energy", "Energy is not a state of matter."),
       ("Force", "Force is an interaction, not a form of matter."),
       ("Sound", "Sound is a wave travelling through matter.")],
      ["Matter comes in solid, liquid and gas.", "Which option names one of them?"],
      ["Solid is a state of matter."]),

    M("sci.matter", 2,
      "Water freezes into ice at…",
      "0 °C",
      [("100 °C", "That is the boiling point of water."),
       ("32 °C", "That is the freezing point in degrees Fahrenheit, not Celsius."),
       ("−100 °C", "That is far below water's freezing point.")],
      ["The Celsius scale puts freezing at zero.", "Boiling is 100 °C."],
      ["Water freezes at 0 °C."],
      visual=phases("Solid, liquid and gas shown side by side")),

    M("sci.matter", 3,
      "Salt dissolved in water can be recovered by…",
      "evaporating the water",
      [("filtering the mixture", "A dissolved solid passes straight through filter paper."),
       ("using a magnet", "Salt is not magnetic."),
       ("freezing the mixture", "Freezing separates ice from salt water only partly, and leaves brine behind.")],
      ["Dissolved salt is not a separate solid you can catch.", "Remove the water and the salt stays behind."],
      ["Evaporation leaves the salt crystals.", "That is how sea salt is made."]),

    M("sci.matter", 4,
      "In a chemical change…",
      "new substances form",
      [("only the shape changes", "Shape changes are physical changes."),
       ("no energy is involved", "Chemical reactions absorb or release energy."),
       ("matter disappears", "Mass is conserved in a chemical change.")],
      ["Look for a new substance with new properties.", "Burning, rusting and baking are examples."],
      ["A chemical change produces new substances.", "The atoms are rearranged, not destroyed."]),

    # ----------------------------------------------------------- sci.force
    M("sci.force", 1,
      "Force is measured in…",
      "newtons",
      [("joules", "Joules measure energy."),
       ("watts", "Watts measure power."),
       ("metres", "Metres measure length.")],
      ["The unit is named after the scientist who wrote the laws of motion.", "Newton."],
      ["Force is measured in newtons (N)."],
      visual=force_arrow("A block with a ten newton force arrow", "10 N")),

    M("sci.force", 2,
      "Newton's first law says an object at rest…",
      "stays at rest unless a force acts on it",
      [("speeds up by itself", "Motion does not appear without a force."),
       ("needs a constant force to stay still", "Rest is the natural state without a net force."),
       ("always falls", "Gravity is a force, not a rule about all objects.")],
      ["Things keep doing what they are doing.", "A change needs a net force."],
      ["No net force means no change in motion."]),

    M("sci.force", 3,
      "A 10 kg mass on Earth, where g ≈ 10 N/kg, weighs about…",
      "100 N",
      [("10 N", "That uses the mass as the weight."),
       ("1 N", "That divides by 10 twice."),
       ("0 N", "The mass is on Earth, so gravity acts on it.")],
      ["Weight = mass × gravitational field strength.", "10 × 10."],
      ["10 kg × 10 N/kg = 100 N."]),

    M("sci.force", 4,
      "Action and reaction forces are…",
      "equal in size and opposite in direction",
      [("unequal, with the bigger object winning", "The forces are always equal in size."),
       ("in the same direction", "They act in opposite directions."),
       ("only present in space", "They act everywhere, including on the ground.")],
      ["Newton's third law.", "The two forces act on different objects."],
      ["Every action has an equal and opposite reaction.", "So the pair is equal and opposite."]),

    # ----------------------------------------------------------- sci.earth
    M("sci.earth", 1,
      "Earth orbits…",
      "the Sun",
      [("the Moon", "The Moon orbits Earth, not the other way round."),
       ("Mars", "Mars is a separate planet in its own orbit."),
       ("itself", "Orbiting itself is not a thing.")],
      ["Which body is at the centre of our solar system?", "The star we see in the daytime sky."],
      ["Earth orbits the Sun once a year."]),

    M("sci.earth", 2,
      "Day and night are caused by…",
      "Earth rotating on its axis",
      [("Earth orbiting the Sun", "The orbit causes the year and the seasons, not day and night."),
       ("the Moon blocking the Sun", "That only happens during a solar eclipse."),
       ("the Sun moving around Earth", "The Sun does not orbit Earth.")],
      ["One full spin takes about 24 hours.", "The side facing the Sun has day."],
      ["Rotation brings each side into sunlight and then into shadow."]),

    M("sci.earth", 3,
      "Seasons happen because…",
      "Earth's axis is tilted",
      [("Earth is closer to the Sun in summer", "The distance change is small and not the cause."),
       ("the Sun gets hotter in summer", "The Sun's output does not change with our seasons."),
       ("the Moon pulls on the seasons", "The Moon drives tides, not seasons.")],
      ["The tilt changes how directly sunlight hits each hemisphere.", "That changes day length and heating."],
      ["A tilted axis gives longer, more direct sunlight in summer.", "So the seasons follow the tilt."]),

    M("sci.earth", 4,
      "The Moon's phases repeat about every…",
      "29.5 days",
      [("24 hours", "That is Earth's rotation."),
       ("365 days", "That is Earth's orbit around the Sun."),
       ("7 days", "A week is a human invention, not a lunar cycle.")],
      ["Track new moon to new moon.", "It is about a month."],
      ["The synodic month is about 29.5 days."]),

    # ---------------------------------------------------------- sci.energy
    M("sci.energy", 1,
      "The energy stored in food is…",
      "chemical energy",
      [("sound energy", "Sound is a wave, not how food stores energy."),
       ("light energy", "Food does not store light directly."),
       ("nuclear energy", "Digestion does not split atoms.")],
      ["Food releases energy when its bonds break.", "That is a chemical store."],
      ["Food stores chemical energy."]),

    M("sci.energy", 2,
      "A moving ball has…",
      "kinetic energy",
      [("only potential energy", "A moving object has kinetic energy."),
       ("no energy", "Motion is energy."),
       ("only electrical energy", "A rolling ball is not a circuit.")],
      ["Kinetic energy depends on mass and speed.", "Movement means kinetic."],
      ["The ball has kinetic energy, ½mv²."]),

    M("sci.energy", 3,
      "Energy cannot be…",
      "created or destroyed",
      [("transferred", "Energy is transferred all the time."),
       ("transformed", "Energy changes form constantly."),
       ("stored", "Batteries and food store energy.")],
      ["The law of conservation of energy.", "It only changes form."],
      ["Energy is conserved: it moves and changes form but is not created or destroyed."]),

    M("sci.energy", 4,
      "A roller coaster at the top of a hill has mostly…",
      "gravitational potential energy",
      [("kinetic energy", "At the top it is nearly stopped, so kinetic energy is smallest."),
       ("sound energy", "Sound is a by-product, not the main store."),
       ("chemical energy", "The car is not burning fuel at the top.")],
      ["Height gives a store of energy.", "As it drops, that store becomes kinetic."],
      ["High up means large gravitational potential energy."]),

    # ----------------------------------------------------------- sci.waves
    M("sci.waves", 1,
      "Sound travels as…",
      "a wave",
      [("a stream of particles", "Sound moves energy, not matter, across the room."),
       ("a straight line of light", "Light and sound are different."),
       ("heat only", "Sound is mechanical, not just heat.")],
      ["Sound is a vibration travelling through a medium.", "It is a wave."],
      ["Sound is a longitudinal wave."],
      visual=wave_diagram("A wave travelling along an axis")),

    M("sci.waves", 2,
      "Sound cannot travel through…",
      "a vacuum",
      [("water", "Sound travels faster in water than in air."),
       ("steel", "Sound travels very fast in steel."),
       ("air", "Air is the usual medium for sound.")],
      ["Sound needs particles to vibrate.", "A vacuum has none."],
      ["No particles means nothing to vibrate, so no sound."]),

    M("sci.waves", 3,
      "A higher-frequency sound has…",
      "a higher pitch",
      [("a lower pitch", "Lower frequency gives lower pitch."),
       ("a louder volume", "Volume is amplitude, not frequency."),
       ("a longer wavelength", "Higher frequency means shorter wavelength at the same speed.")],
      ["Frequency is vibrations per second.", "Pitch is how high or low a note sounds."],
      ["More vibrations per second = higher pitch."]),

    M("sci.waves", 4,
      "Which of these is a transverse wave?",
      "Light",
      [("Sound in air", "Sound in air is longitudinal."),
       ("A sound wave in water", "Sound is longitudinal in water too."),
       ("A compression wave", "Compression waves are longitudinal by definition.")],
      ["In a transverse wave the vibration is perpendicular to travel.", "Light is electromagnetic and transverse."],
      ["Light's electric and magnetic fields oscillate across the direction of travel."]),
]

# --------------------------------------------------------------------------- #
# College engineering
# --------------------------------------------------------------------------- #

_ENG = [
    M("eng.statics", 1,
      "The SI unit of force is the…",
      "newton",
      [("joule", "A joule is a unit of energy."),
       ("pascal", "A pascal is pressure: force per area."),
       ("watt", "A watt is power.")],
      ["Force is mass × acceleration.", "kg·m/s² has its own name."],
      ["1 N = 1 kg·m/s²."]),

    M("eng.statics", 2,
      "A beam is in static equilibrium when…",
      "the net force and the net moment are both zero",
      [("only the net force is zero", "A couple can still rotate the beam with zero net force."),
       ("it does not move sideways", "It could still rotate or move vertically."),
       ("it is supported at both ends", "Support is not the condition for equilibrium.")],
      ["Equilibrium needs no translation and no rotation.", "Two equations: ΣF = 0 and ΣM = 0."],
      ["ΣF = 0 and ΣM = 0 together mean equilibrium."]),

    M("eng.statics", 3,
      "A 100 N load acts 2 m from a pivot. What moment does it create?",
      "200 N·m",
      [("50 N·m", "That divides by the distance instead of multiplying."),
       ("100 N·m", "That ignores the distance."),
       ("400 N·m", "That doubles the distance.")],
      ["Moment = force × perpendicular distance.", "100 × 2."],
      ["100 N × 2 m = 200 N·m."]),

    M("eng.statics", 3,
      "A simply supported beam of span 4 m carries a 20 N load at midspan. What is the reaction at each support?",
      "10 N",
      [("20 N", "That would double the total load."),
       ("5 N", "That divides by 4 instead of by 2."),
       ("40 N", "That doubles the load.")],
      ["The load is symmetric, so each support takes half.", "20 ÷ 2."],
      ["Total load 20 N splits equally.", "Each reaction is 10 N."],
      visual=beam("A beam on two supports with a load at midspan", "20 N", "4 m")),

    M("eng.statics", 4,
      "Just before a block slips, the static friction force equals…",
      "μN",
      [("N", "The normal force alone is not friction."),
       ("μ/N", "That divides by the normal force instead of multiplying."),
       ("mg, always", "That is weight, which equals N only on level ground.")],
      ["The friction limit is the coefficient times the normal force.", "f_max = μN."],
      ["At the point of slipping, friction reaches μN."]),

    M("eng.circuits", 1,
      "Ohm's law is…",
      "V = IR",
      [("V = I/R", "That would make voltage fall as resistance grows."),
       ("I = VR", "Current would grow with resistance, which is backwards."),
       ("R = VI", "Resistance is not the product of voltage and current.")],
      ["Voltage drives current through resistance.", "V = I × R."],
      ["V = IR."],
      visual=circuit("A battery and a resistor in a simple circuit", "4 Ω", "12 V")),

    M("eng.circuits", 2,
      "A 12 V source is connected across a 4 Ω resistor. What current flows?",
      "3 A",
      [("48 A", "That multiplies instead of dividing."),
       ("0.33 A", "That divides the resistance by the voltage."),
       ("16 A", "That adds the voltage and resistance.")],
      ["I = V / R.", "12 ÷ 4."],
      ["12 ÷ 4 = 3 A."]),

    M("eng.circuits", 3,
      "Two 4 Ω resistors in series have a total resistance of…",
      "8 Ω",
      [("2 Ω", "That is the parallel value."),
       ("4 Ω", "Series resistances add, they do not stay the same."),
       ("16 Ω", "That multiplies the resistances.")],
      ["Series resistances add.", "4 + 4."],
      ["4 + 4 = 8 Ω."]),

    M("eng.circuits", 4,
      "Two 4 Ω resistors in parallel have a total resistance of…",
      "2 Ω",
      [("8 Ω", "That is the series value."),
       ("4 Ω", "Parallel combinations are always smaller than the smallest branch."),
       ("16 Ω", "That multiplies the resistances.")],
      ["1/R = 1/R₁ + 1/R₂.", "1/4 + 1/4 = 1/2."],
      ["R = 2 Ω."]),

    M("eng.circuits", 4,
      "How much power does a 3 A current dissipate in a 5 Ω resistor?",
      "45 W",
      [("15 W", "That is V = IR, not power."),
       ("8 W", "That adds current and resistance."),
       ("225 W", "That is I²R², squaring twice.")],
      ["P = I²R.", "9 × 5."],
      ["9 × 5 = 45 W."]),

    M("eng.thermo", 1,
      "The first law of thermodynamics says that energy is…",
      "conserved",
      [("always lost", "Some energy becomes unusable, but it is not destroyed."),
       ("created by heat engines", "Engines convert, they do not create energy."),
       ("equal to entropy", "Entropy measures disorder, not energy.")],
      ["Energy in = energy out + change in internal energy.", "It is a conservation law."],
      ["ΔU = Q − W keeps energy accounted for."]),

    M("eng.thermo", 2,
      "Heat flows spontaneously from…",
      "hot to cold",
      [("cold to hot", "That needs work input, like a fridge."),
       ("always upwards", "Direction depends on temperature, not height."),
       ("nowhere", "Heat flows whenever there is a temperature difference.")],
      ["The second law of thermodynamics.", "Heat moves toward equilibrium."],
      ["Heat flows from higher to lower temperature."]),

    M("eng.thermo", 3,
      "A Carnot engine runs between 500 K and 300 K. What is its efficiency?",
      "40%",
      [("60%", "That is 300/500, the fraction rejected, not the efficiency."),
       ("20%", "That uses the temperature difference over 1000."),
       ("67%", "That is 500/300, which is above 1 and impossible.")],
      ["η = 1 − T_cold/T_hot.", "1 − 300/500."],
      ["1 − 0.6 = 0.4.", "That is 40%."]),

    M("eng.thermo", 4,
      "The entropy of an isolated system…",
      "never decreases",
      [("always decreases", "That would violate the second law."),
       ("stays constant", "It stays constant only for reversible processes."),
       ("is always zero", "Entropy is zero only at absolute zero for a perfect crystal.")],
      ["Look at the second law.", "Real processes increase entropy."],
      ["For an isolated system, ΔS ≥ 0."]),

    M("eng.materials", 1,
      "Stress is…",
      "force per unit area",
      [("strain per unit length", "That mixes strain with length."),
       ("load times area", "That would grow with area, which is backwards."),
       ("work per second", "That is power.")],
      ["σ = F/A.", "Think of pressure, but inside a material."],
      ["Stress = force / area."],
      visual=stress_strain("A stress-strain curve with the yield point marked")),

    M("eng.materials", 2,
      "Strain is…",
      "change in length divided by original length",
      [("force per unit area", "That is stress."),
       ("mass per unit volume", "That is density."),
       ("stress times time", "That is not a standard quantity.")],
      ["ε = ΔL/L.", "It is dimensionless."],
      ["Strain = ΔL / L."]),

    M("eng.materials", 3,
      "A 200 N load acts on an area of 0.01 m². What is the stress?",
      "20 kPa",
      [("2 kPa", "That divides by 0.1 instead of 0.01."),
       ("200 kPa", "That multiplies by 10 instead of dividing."),
       ("20 Pa", "That is 200/10, off by a factor of 1000.")],
      ["σ = F/A.", "200 ÷ 0.01 = 20,000 Pa."],
      ["20,000 Pa = 20 kPa."]),

    M("eng.materials", 4,
      "A brittle material…",
      "fractures with little plastic deformation",
      [("stretches a lot before breaking", "That describes a ductile material."),
       ("returns to shape after yielding", "Yielding is permanent deformation."),
       ("never breaks", "Every material has a failure point.")],
      ["Brittle means little warning before failure.", "Glass and ceramics are examples."],
      ["Brittle materials show almost no plastic strain before fracture."]),

    M("eng.fluids", 1,
      "Pressure in a fluid increases with…",
      "depth",
      [("colour", "Colour has nothing to do with pressure."),
       ("speed only", "Speed relates to dynamic pressure, not depth."),
       ("surface area", "Pressure is force per area; area does not set it.")],
      ["Deeper water pushes harder.", "p = ρgh."],
      ["Pressure grows with depth."]),

    M("eng.fluids", 2,
      "Bernoulli's principle links pressure to…",
      "flow speed",
      [("colour", "Not a fluid property that affects pressure."),
       ("temperature only", "Temperature matters, but Bernoulli's relation is about speed."),
       ("viscosity only", "Bernoulli assumes inviscid flow.")],
      ["Faster flow means lower pressure in a streamline.", "That is how wings and carburettors work."],
      ["Higher speed gives lower static pressure."]),

    M("eng.fluids", 3,
      "Water has a density of 1000 kg/m³. What is the mass of 0.5 m³?",
      "500 kg",
      [("2000 kg", "That divides by 0.5 instead of multiplying."),
       ("5000 kg", "That multiplies by 5."),
       ("0.5 kg", "That copies the volume.")],
      ["m = ρV.", "1000 × 0.5."],
      ["1000 × 0.5 = 500 kg."]),

    M("eng.fluids", 4,
      "A block floats when its density is…",
      "less than the fluid's density",
      [("greater than the fluid's density", "Denser objects sink."),
       ("exactly 1000 kg/m³, whatever the fluid", "The fluid's own density is what matters."),
       ("zero", "Some floating objects are only slightly less dense.")],
      ["Buoyancy supports weight when displaced fluid weighs enough.", "Compare densities."],
      ["Floating needs ρ_object < ρ_fluid."]),
]

# --------------------------------------------------------------------------- #
# Coding
# --------------------------------------------------------------------------- #

_CODE = [
    M("code.vars", 1,
      "In Python, what type is `count = 3`?",
      "an integer",
      [("a string", "Strings are quoted, as in '3'."),
       ("a boolean", "Booleans are True or False."),
       ("a float", "A float would be written 3.0.")],
      ["Look at the value: no quotes and no decimal point.", "Whole numbers are integers."],
      ["3 is a whole number.", "So `count` is an int."],
      visual=code_block(["count = 3", "print(type(count))"], "Python code showing count assigned three and its type printed")),

    M("code.vars", 2,
      "After this code runs, what is x?\n\nx = 5\nx = x + 2",
      "7",
      [("5", "The second line overwrites the first value."),
       ("2", "That is only the value added."),
       ("52", "The + is arithmetic, not string joining.")],
      ["The assignment happens in order.", "Start from 5 and add 2."],
      ["x = 5, then x = 5 + 2.", "So x is 7."]),

    M("code.vars", 2,
      "In Python, what does `3 / 2` evaluate to?",
      "1.5",
      [("1", "That is what integer division // gives."),
       ("2", "That is rounding rather than dividing."),
       ("0", "3/2 is not zero.")],
      ["A single slash means true division in Python 3.", "The result can be a float."],
      ["3 / 2 = 1.5."]),

    M("code.vars", 3,
      "What does `a, b = 1, 2; a, b = b, a` leave in a and b?",
      "a is 2 and b is 1",
      [("a is 1 and b is 2", "That ignores the swap on the second line."),
       ("a is 2 and b is 2", "The tuple assignment keeps both old values."),
       ("It raises an error", "Tuple assignment swaps values safely.")],
      ["The right side is evaluated before assignment.", "Both old values are captured first."],
      ["Right side is (2, 1).", "So a = 2 and b = 1."]),

    M("code.vars", 4,
      "Which name is a valid Python variable?",
      "total_score",
      [("2nd_score", "Names cannot start with a digit."),
       ("total-score", "Hyphens are not allowed in names."),
       ("class", "`class` is a reserved keyword.")],
      ["Names use letters, digits and underscores, and cannot start with a digit.", "Keywords are reserved."],
      ["`total_score` follows the rules."]),

    M("code.loops", 1,
      "How many times does the body of `for i in range(3)` run?",
      "3",
      [("2", "range(3) gives 0, 1, 2 — three values."),
       ("4", "It stops before 3."),
       ("0", "range(3) is not empty.")],
      ["range(n) counts from 0 up to but not including n.", "0, 1, 2."],
      ["Three values, so three iterations."],
      visual=code_block(["for i in range(3):", "    print(i)"], "A Python for loop over range of three")),

    M("code.loops", 2,
      "What values does `range(1, 5)` produce?",
      "1, 2, 3, 4",
      [("1, 2, 3, 4, 5", "The stop value is excluded."),
       ("0, 1, 2, 3, 4", "The start value is included, and it is 1."),
       ("2, 3, 4, 5", "It starts at 1, not 2.")],
      ["range(start, stop) includes start and excludes stop.", "Start 1, stop 5."],
      ["1, 2, 3, 4."]),

    M("code.loops", 2,
      "Which loop repeats while its condition stays true?",
      "while",
      [("for", "A for loop walks over a sequence."),
       ("if", "An if statement runs at most once."),
       ("def", "def defines a function.")],
      ["It checks the condition before each pass.", "The keyword is while."],
      ["`while` loops repeat while the condition is true."]),

    M("code.loops", 3,
      "What is `total` after this runs?\n\ntotal = 0\nfor n in [2, 4, 6]:\n    total += n",
      "12",
      [("6", "That is the last value only."),
       ("10", "That drops the 2."),
       ("24", "That multiplies instead of adding.")],
      ["+= adds to the running total.", "0 + 2 + 4 + 6."],
      ["0 + 2 = 2, + 4 = 6, + 6 = 12."]),

    M("code.loops", 4,
      "Starting from i = 0, how many times does `while i < 10: i += 3` run?",
      "4",
      [("3", "That stops at i = 9, missing the last pass."),
       ("10", "The step is 3, not 1."),
       ("5", "The loop body runs at i = 0, 3, 6, 9 — four times.")],
      ["List the values of i at the start of each pass.", "0, 3, 6, 9 are all below 10."],
      ["Four passes: i = 0, 3, 6, 9.", "After the fourth, i = 12, so the loop ends."]),

    M("code.funcs", 1,
      "Given:\n\ndef add(a, b):\n    return a + b\n\nWhat is add(2, 3)?",
      "5",
      [("23", "That joins text; these are numbers."),
       ("6", "That is 2 × 3."),
       ("It raises an error", "The call passes two arguments, matching the parameters.")],
      ["The function returns a + b.", "2 + 3."],
      ["2 + 3 = 5."],
      visual=code_block(["def add(a, b):", "    return a + b", "", "print(add(2, 3))"], "Python function add that returns the sum of two numbers")),

    M("code.funcs", 2,
      "In Python, a function with no return statement returns…",
      "None",
      [("0", "Python does not default to zero."),
       ("False", "None is not the same as False."),
       ("an error", "Returning nothing is allowed.")],
      ["Python has a special value for 'no value'.", "It is None."],
      ["Without return, the function returns None."]),

    M("code.funcs", 3,
      "Given `def f(x): return x * 2`, what is f(f(3))?",
      "12",
      [("6", "That is only the inner call."),
       ("9", "That squares 3."),
       ("18", "That multiplies by 3 twice.")],
      ["Work from the inside out.", "f(3) = 6, then f(6)."],
      ["f(3) = 6, f(6) = 12."]),

    M("code.funcs", 4,
      "A local variable…",
      "exists only inside the function where it was created",
      [("is always global", "That is only true without the function scope or a global keyword."),
       ("cannot be changed", "Locals can be reassigned freely."),
       ("must be a number", "Locals can hold any type.")],
      ["Scope decides where a name is visible.", "Names created in a function stay there."],
      ["Locals live in the function's scope."]),

    M("code.lists", 1,
      "For `nums = [1, 2, 3]`, what is `nums[0]`?",
      "1",
      [("2", "That is index 1."),
       ("3", "That is index 2."),
       ("0", "That is the index, not the value.")],
      ["Python indexing starts at 0.", "Index 0 is the first element."],
      ["nums[0] = 1."]),

    M("code.lists", 2,
      "What is `len([4, 5, 6, 7])`?",
      "4",
      [("3", "That is the last index, not the length."),
       ("7", "That is the last value."),
       ("10", "That is the sum.")],
      ["len counts the elements.", "There are four numbers."],
      ["len returns 4."]),

    M("code.lists", 3,
      "What does `nums.append(9)` do?",
      "adds 9 to the end of the list",
      [("adds 9 to the front", "That would be insert(0, 9)."),
       ("replaces the whole list", "append adds one element."),
       ("sorts the list", "That is sort().")],
      ["append grows the list by one.", "The new item goes last."],
      ["The list gains 9 at the end."]),

    M("code.lists", 4,
      "What is `[1, 2, 3][1:]`?",
      "[2, 3]",
      [("[1, 2]", "That is the slice [:-1]."),
       ("[3]", "That is the slice [2:]."),
       ("[1, 2, 3]", "The slice starts at index 1, so it drops the first item.")],
      ["A slice from index 1 keeps everything from there.", "Index 1 is the value 2."],
      ["[2, 3]."]),

    M("code.recursion", 1,
      "Every recursive function needs a…",
      "base case",
      [("for loop", "Recursion does not need a loop."),
       ("global variable", "Recursion can be written without globals."),
       ("print statement", "Output is unrelated to stopping.")],
      ["Something must stop the calls.", "That stop is the base case."],
      ["Without a base case the calls never stop."]),

    M("code.recursion", 2,
      "Given `def f(n): return 1 if n <= 1 else n * f(n - 1)`, what is f(3)?",
      "6",
      [("3", "That returns n without multiplying by the smaller calls."),
       ("9", "That squares 3."),
       ("12", "That is f(4).")],
      ["This is factorial.", "3 × 2 × 1."],
      ["f(3) = 3 × f(2) = 3 × 2 × 1.", "So f(3) = 6."],
      visual=code_block(["def f(n):", "    return 1 if n <= 1 else n * f(n - 1)", "", "f(3)  # 6"], "Recursive factorial function in Python")),

    M("code.recursion", 3,
      "Without a base case, recursion…",
      "never stops and eventually overflows the stack",
      [("runs exactly once", "That would need a condition."),
       ("becomes faster", "More calls means more work."),
       ("returns None immediately", "It never reaches a return.")],
      ["Each call adds a stack frame.", "With no stop, frames pile up."],
      ["The stack fills and Python raises RecursionError."]),

    M("code.recursion", 4,
      "With f(0) = 0 and f(1) = 1 and f(n) = f(n − 1) + f(n − 2), what is f(5)?",
      "5",
      [("3", "That is f(4)."),
       ("8", "That is f(6)."),
       ("13", "That is f(7).")],
      ["Build the sequence upward.", "0, 1, 1, 2, 3, 5, …"],
      ["f(2) = 1, f(3) = 2, f(4) = 3, f(5) = 5."]),

    M("code.complexity", 1,
      "Binary search on a sorted list of n items runs in…",
      "O(log n)",
      [("O(n)", "That is a linear scan."),
       ("O(1)", "Every step is constant time, but the number of steps grows."),
       ("O(n²)", "That is a nested-loop cost.")],
      ["Each step halves what is left.", "Halving n times is logarithmic."],
      ["log₂(n) steps, so O(log n)."]),

    M("code.complexity", 2,
      "A single loop over n items is…",
      "O(n)",
      [("O(log n)", "That is halving, not one pass per item."),
       ("O(1)", "Visiting every item cannot be constant time."),
       ("O(n²)", "That needs two nested loops.")],
      ["Count the work per item.", "One pass touches each item once."],
      ["n steps, so O(n)."],
      visual=code_block(["for x in items:", "    print(x)"], "A single loop over a list of items")),

    M("code.complexity", 3,
      "Two nested loops each over n items cost…",
      "O(n²)",
      [("O(n)", "Nesting multiplies the work."),
       ("O(2n)", "That is two separate loops side by side."),
       ("O(log n)", "Nested loops do not halve the input.")],
      ["For each of n outer steps you do n inner steps.", "n × n."],
      ["n² steps, so O(n²)."]),

    M("code.complexity", 4,
      "Which function grows slowest as n gets large?",
      "log n",
      [("n", "A straight line grows faster than a logarithm."),
       ("n log n", "That is larger than n."),
       ("n²", "That is the fastest of these choices.")],
      ["Compare the shapes for large n.", "A logarithm flattens out."],
      ["log n < n < n log n < n²."]),
]


# Recall openers for the contest and olympiad skills. The engine always starts a
# skill on a tier-1 item, so every one of these tracks needs one.
_OPENERS = [
    M("aime.nt", 1,
      "How many positive divisors does a prime number have?",
      "2",
      [("1", "A prime always has itself as a divisor as well as 1."),
       ("3", "A prime has no third divisor, or it would not be prime."),
       ("It depends on the prime", "Every prime has exactly the same two divisors.")],
      ["List the divisors of 7.", "1 and 7 are the only ones."],
      ["Every prime has divisors 1 and itself.", "So the count is always 2."]),

    M("aime.combo", 1,
      "How many ways can 3 distinct books be arranged in a row?",
      "6",
      [("3", "That is the number of books, not the orderings."),
       ("9", "That is 3², which double counts."),
       ("27", "That is 3³, as if each book had three positions.")],
      ["The first position has 3 choices, then 2, then 1.", "Multiply them."],
      ["3 × 2 × 1 = 6."]),

    M("aime.geo", 1,
      "What is the sum of the interior angles of a triangle?",
      "180°",
      [("90°", "That is one right angle, not all three angles."),
       ("360°", "That is the sum around a full turn."),
       ("270°", "That is three right angles.")],
      ["Tear the corners off any triangle and put them together.", "They form a straight line."],
      ["The three angles form a straight line.", "So they add to 180°."]),

    M("usamo.algebra", 1,
      "Factor a² − b².",
      "(a − b)(a + b)",
      [("(a − b)²", "That expands to a² − 2ab + b², with a middle term."),
       ("(a + b)²", "That expands to a² + 2ab + b²."),
       ("a(a − b)", "That expands to a² − ab, missing the b² term.")],
      ["This is the difference of two squares.", "Multiply (a − b)(a + b) out to check."],
      ["a² − b² = (a − b)(a + b)."]),

    M("usamo.nt", 1,
      "Which of these numbers is prime?",
      "17",
      [("21", "21 = 3 × 7."),
       ("27", "27 = 3 × 9."),
       ("33", "33 = 3 × 11.")],
      ["A prime has no factors besides 1 and itself.", "Check divisibility by 2, 3 and 5."],
      ["17 is not divisible by 2, 3 or 5, and 17 is below 5².", "So 17 is prime."]),

    M("imo.geo", 1,
      "Angles on a straight line add up to…",
      "180°",
      [("90°", "That is a right angle, half of a straight line."),
       ("270°", "That is three quarters of a turn."),
       ("360°", "That is a full turn.")],
      ["A straight line is half of a full turn.", "Half of 360°."],
      ["180°."]),

    M("mc.sprint", 1,
      "What is 25% of 40?",
      "10",
      [("4", "That is 10% of 40."),
       ("15", "That is 37.5% of 40."),
       ("20", "That is 50% of 40.")],
      ["25% is one quarter.", "Divide 40 by 4."],
      ["40 ÷ 4 = 10."]),

    M("mc.target", 1,
      "What is the units digit of 6²?",
      "6",
      [("2", "6 × 6 is 36, so the units digit is not 2."),
       ("3", "That is the tens digit of 36."),
       ("0", "Only multiples of 10 end in 0.")],
      ["Compute 6 × 6 first.", "36 ends in 6."],
      ["6² = 36.", "The units digit is 6."]),

    M("amc8.geo", 1,
      "How many faces does a cube have?",
      "6",
      [("8", "That is the number of vertices."),
       ("12", "That is the number of edges."),
       ("4", "A cube has four side faces plus top and bottom.")],
      ["Count the flat surfaces: top, bottom and four sides.", "2 + 4."],
      ["6 faces."]),

    M("amc10.count", 1,
      "A fair coin is flipped twice. How many different outcomes are possible?",
      "4",
      [("2", "That is the number of outcomes for one flip only."),
       ("3", "There are four ordered outcomes, including two heads."),
       ("8", "That would be three flips.")],
      ["Each flip has 2 outcomes, and they are independent.", "2 × 2."],
      ["HH, HT, TH, TT — four outcomes."]),

    M("amc12.trig", 1,
      "What is the value of cos 0°?",
      "1",
      [("0", "That is sin(0°)."),
       ("1/2", "That is cos(60°)."),
       ("−1", "That is cos(180°).")],
      ["At 0° the unit-circle point is (1, 0).", "Cosine is the x-coordinate."],
      ["cos(0°) = 1."]),

    # ----------------------------------------------- imo.geo, two more shapes
    M("imo.geo", 2,
      "What is the exterior angle of a regular pentagon?",
      "72°",
      [("108°", "That is the interior angle, supplementary to the exterior one."),
       ("60°", "That is the exterior angle of an equilateral triangle."),
       ("45°", "That is the exterior angle of a regular octagon.")],
      ["Exterior angles of any convex polygon add to 360°.", "Divide by 5."],
      ["360 ÷ 5 = 72°."]),

    M("imo.geo", 2,
      "In triangle ABC, AB = AC and angle A = 40°. What is angle B?",
      "70°",
      [("40°", "Then the angles would add to only 120°."),
       ("100°", "That is the sum of B and C, not one of them."),
       ("50°", "That would leave 90° for C.")],
      ["The base angles of an isosceles triangle are equal.", "180 − 40 = 140, then halve it."],
      ["B = C and B + C = 140°.", "So B = 70°."]),

    # ---------------------------------------------------------- imo.ineq
    M("imo.ineq", 1,
      "Which of these is never negative for a real number x?",
      "x²",
      [("x", "x can be negative."),
       ("x³", "A negative x gives a negative cube."),
       ("2x − 1", "That is negative whenever x < 0.5.")],
      ["A square multiplies a number by itself.", "Two negatives make a positive."],
      ["x² ≥ 0 for every real x."]),

    M("imo.ineq", 2,
      "For positive x, the smallest possible value of x + 1/x is…",
      "2",
      [("1", "At x = 1 the sum is already 2."),
       ("0", "Both terms are positive, so the sum cannot be 0."),
       ("It has no minimum", "The expression is bounded below by 2.")],
      ["Try x = 1, then x = 2.", "At x = 1 the sum is 2, and larger x only adds more."],
      ["x + 1/x ≥ 2 by AM-GM, with equality at x = 1."]),

    M("imo.ineq", 3,
      "If 0 < x < 1, which of these is largest?",
      "1/x",
      [("x", "x is smaller than 1 here."),
       ("x²", "Squaring a number below 1 makes it smaller."),
       ("x³", "That is even smaller than x².")],
      ["Pick x = 1/2 and compute each option.", "1 ÷ (1/2) = 2."],
      ["With x = 1/2: x³ = 1/8, x² = 1/4, x = 1/2 and 1/x = 2.", "So 1/x is largest."]),

    M("imo.ineq", 4,
      "For positive a and b with ab = 16, the smallest possible value of a + b is…",
      "8",
      [("4", "That is 2√ab only if you forget the factor 2."),
       ("16", "One of a or b could be 1, which gives 17."),
       ("32", "That is 2ab, not a + b.")],
      ["AM-GM: a + b ≥ 2√(ab).", "√16 = 4."],
      ["a + b ≥ 2 × 4 = 8, at a = b = 4."]),

    M("imo.ineq", 4,
      "For positive x, the smallest possible value of x + 4/x is…",
      "4",
      [("2", "At x = 2 the expression is 2 + 2 = 4, not 2."),
       ("8", "That is twice the minimum."),
       ("16", "That is 4x at the minimum, not the whole expression.")],
      ["AM-GM: x + 4/x ≥ 2√(x · 4/x).", "The product inside is 4."],
      ["2√4 = 4, at x = 2."]),
]

QUESTIONS = _AIME + _OLY + _CONTEST + _SCI + _ENG + _CODE + _OPENERS
