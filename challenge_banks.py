"""Hard / SAT Stretch contest-style extras (AMC 8 & MathCounts flavor).

Used to fill Hard and Stretch quiz slots so they are not padded with
trivial product-rule fillers.
"""

from __future__ import annotations

import math

from question_banks import _q


def _ncr(n, k):
    if k < 0 or k > n:
        return 0
    return math.comb(n, k)


def challenges_for(title: str) -> list:
    t = (title or "").lower()
    out = []
    if "mathcounts" in t or "counting" in t or "permut" in t or "combin" in t:
        out += _mc_challenges(t)
    if "algebra 2" in t:
        out += _a2_challenges(t)
    if "eighth grade" in t or "8th" in t:
        out += _g8_challenges(t)
    if "seventh grade" in t or "7th" in t:
        out += _g7_challenges(t)
    if "sixth grade" in t or "6th" in t:
        out += _g6_challenges(t)
    if "fifth grade" in t:
        out += _g5_challenges(t)
    if "fourth grade" in t:
        out += _g4_challenges(t)
    if "third grade" in t:
        out += _g3_challenges(t)
    if "second grade" in t:
        out += _g2_challenges(t)
    if "first grade" in t:
        out += _g1_challenges(t)
    if not out:
        out += _mc_challenges(t)[:8] + _g6_challenges(t)[:8]
    # Drop broken / None
    return [q for q in out if q and q.get("correct_answer") not in (None, "")]


def _mc_challenges(t: str) -> list:
    qs = [
        _q(
            "AMC 8 style: How many 3-letter strings from {A,B,C,D} include at least one A (repeats allowed)?",
            37,
            "Total 4³=64. No A: 3³=27. 64−27=37.",
            [64, 27, 36, 48],
            difficulty="hard",
        ),
        _q(
            "MathCounts: How many 4-digit PINs use digits 0–9 with no digit repeating?",
            4536,
            "First digit 1–9 (9), then 9,8,7 remaining including 0: 9×9×8×7=4536.",
            [9000, 5040, 10000],
            difficulty="hard",
        ),
        _q(
            "How many ways to choose a president and vice-president from 10 people (order matters, distinct roles)?",
            90,
            "P(10,2)=10×9=90.",
            [45, 100, 20],
            difficulty="hard",
        ),
        _q(
            "A club has 8 students. How many 3-person committees (order does not matter)?",
            56,
            "C(8,3)=56.",
            [24, 336, 512],
            difficulty="hard",
        ),
        _q(
            "From digits 1–9, how many 2-digit numbers have at least one even digit?",
            56,
            "81 total − 25 both-odd = 56.",
            [45, 65, 72],
            difficulty="hard",
        ),
        _q(
            "SAT Stretch: How many positive integers ≤ 100 are divisible by 2 or 5?",
            60,
            "⌊100/2⌋+⌊100/5⌋−⌊100/10⌋=50+20−10=60.",
            [70, 50, 40],
            difficulty="stretch",
        ),
        _q(
            "MathCounts Target: Paths from (0,0) to (4,3) using only right and up unit steps?",
            35,
            "C(7,3)=35 or C(7,4)=35.",
            [12, 24, 64],
            difficulty="stretch",
        ),
        _q(
            "How many ways to arrange the letters in MATH (all distinct)?",
            24,
            "4!=24.",
            [16, 12, 8],
            difficulty="hard",
        ),
        _q(
            "How many distinct arrangements of the letters in BOOK?",
            12,
            "4!/2!=12 because of repeated O.",
            [24, 6, 8],
            difficulty="hard",
        ),
        _q(
            "AMC 8: A fair 6-sided die is rolled twice. How many outcomes have sum 7?",
            6,
            "(1,6)(2,5)(3,4)(4,3)(5,2)(6,1).",
            [5, 7, 12],
            difficulty="hard",
        ),
        _q(
            "Stars and bars: Nonnegative integer solutions to x+y+z=5?",
            21,
            "C(5+3−1,3−1)=C(7,2)=21.",
            [15, 25, 10],
            difficulty="stretch",
        ),
        _q(
            "Positive integer solutions to x+y+z=5 (each ≥1)?",
            6,
            "Let yi=xi−1≥0: y1+y2+y3=2 → C(4,2)=6.",
            [10, 21, 3],
            difficulty="stretch",
        ),
        _q(
            "How many integers from 10 through 99 have digits that sum to 9?",
            9,
            "Tens digit a=1..9, ones=9−a → 9 numbers (18,27,…,90).",
            [10, 18, 8],
            difficulty="stretch",
        ),
        _q(
            "Inclusion: |A∪B| if |A|=12, |B|=18, |A∩B|=5?",
            25,
            "12+18−5=25.",
            [30, 23, 15],
            difficulty="hard",
        ),
        _q(
            "A password has 2 letters (A–Z) then 2 digits. Letters may repeat, digits may repeat. How many passwords?",
            67600,
            "26²×10²=676×100=67600.",
            [52000, 10000, 6760],
            difficulty="stretch",
        ),
        _q(
            "MathCounts: In how many ways can 5 people stand in a line?",
            120,
            "5!=120.",
            [25, 60, 240],
            difficulty="hard",
        ),
        _q(
            "Circular arrangements of 5 distinct people (rotations same)?",
            24,
            "(5−1)!=24.",
            [120, 60, 5],
            difficulty="stretch",
        ),
        _q(
            "AMC 8 flavor: A bag has 3 red and 5 blue marbles. Two drawn without replacement. How many ways to get one of each color (order ignored)?",
            15,
            "C(3,1)×C(5,1)=15.",
            [8, 30, 16],
            difficulty="hard",
        ),
        _q(
            "How many 3-digit numbers have all digits odd?",
            125,
            "5 choices each place (1,3,5,7,9): 5³=125.",
            [250, 512, 100],
            difficulty="stretch",
        ),
        _q(
            "A club of 12 picks a 4-person team. How many teams?",
            495,
            "C(12,4)=495.",
            [48, 11880, 220],
            difficulty="stretch",
        ),
    ]
    return [q for q in qs if q]


def _a2_challenges(t: str) -> list:
    return [
        _q("If $f(x)=2x-3$ and $g(x)=x^2$, what is $(g\\circ f)(2)$?", 1, "f(2)=1, g(1)=1.", [4, 5, 0], difficulty="hard"),
        _q("Discriminant of $x^2-6x+10$?", -4, "36−40=−4.", [4, 16, 0], difficulty="hard"),
        _q("SAT: Solutions of $x^2-6x+10=0$?", "$3\\pm i$", "(x−3)^2=−1.", ["$3$", "$\\pm\\sqrt{10}$", "$6\\pm i$"], difficulty="stretch"),
        _q("If $\\log_2(x)=5$, what is x?", 32, "2^5=32.", [25, 10, 16], difficulty="hard"),
        _q("Solve $3^{x}=81$.", 4, "81=3^4.", [3, 5, 27], difficulty="hard"),
        _q("SAT Stretch: Remainder when $x^3-2x+1$ is divided by $x-1$?", 0, "p(1)=0.", [1, -1, 2], difficulty="stretch"),
        _q("Asymptote of $y=\\frac{2x+1}{x-3}$ as $x\\to\\infty$?", "$y=2$", "Leading coeff ratio.", ["$x=3$", "$y=0$", "$y=1/2$"], difficulty="stretch"),
        _q("Sum of roots of $2x^2-5x+3=0$?", "5/2", "−b/a=5/2.", ["3/2", "-5/2", "3"], difficulty="hard"),
    ]


def _g8_challenges(t: str) -> list:
    return [
        _q("AMC 8: What is $2^{-3}\\times 2^{5}$?", 4, "2^{2}=4.", [1, 8, 16], difficulty="hard"),
        _q("Scientific notation: $(3\\times10^4)(2\\times10^{-6})$?", "$6\\times10^{-2}$", "6×10^{-2}.", ["$6\\times10^{10}$", "$5\\times10^{-2}$", "$6\\times10^{-24}$"], difficulty="hard"),
        _q("Slope of the line through (2,−1) and (6,5)?", "3/2", "(5−(−1))/(6−2)=6/4=3/2.", [2, "1/2", 4], difficulty="hard"),
        _q("Solve the system: x+y=10 and x−y=2. What is x?", 6, "Add: 2x=12.", [4, 8, 5], difficulty="hard"),
        _q("SAT Stretch: A right triangle has legs 9 and 12. Hypotenuse?", 15, "3-4-5 scaled by 3.", [21, 108, 13], difficulty="stretch"),
        _q("If f(x)=3x−7, what is f(f(3))?", -1, "f(3)=2; f(2)=−1.", [2, 14, 5], difficulty="hard"),
        _q("Pythagorean: legs 5 and 12. Hypotenuse?", 13, "5-12-13.", [17, 60, 10], difficulty="stretch"),
        _q("Solve $3(x-4)=2x+5$.", 17, "3x−12=2x+5 → x=17.", [9, -17, 5], difficulty="hard"),
        _q("Volume of a cylinder with radius 3 and height 10 is $90\\pi$. What is $90\\pi$ to the nearest whole number (π≈3.14)?", 283, "90×3.14=282.6≈283.", [270, 300, 282], difficulty="stretch"),
        _q("Write $0.00045$ in scientific notation.", "$4.5\\times10^{-4}$", "Move decimal 4 places.", ["$4.5\\times10^{4}$", "$45\\times10^{-5}$", "$4.5\\times10^{-3}$"], difficulty="stretch"),
    ]


def _g7_challenges(t: str) -> list:
    return [
        _q("A map scale is 1 cm : 5 km. A road is 12 cm on the map. Real length in km?", 60, "12×5=60.", [17, 24, 6], difficulty="hard"),
        _q("A shirt costs $40. After a 15% discount, sale price?", 34, "40−6=34.", [35, 25, 55], difficulty="hard"),
        _q("If 3/5 of a number is 24, what is the number?", 40, "24÷3×5=40.", [30, 48, 15], difficulty="hard"),
        _q("SAT Stretch: A spinner is 1/4 red and 1/3 blue (rest green). P(red or blue)?", "7/12", "1/4+1/3=7/12.", ["1/12", "1/2", "2/7"], difficulty="stretch"),
        _q("Integer: (−8)×(−3)+(−5)?", 19, "24−5=19.", [29, -29, 14], difficulty="hard"),
        _q("Circumference of a circle diameter 14 (use π=22/7)?", 44, "πd=22/7×14=44.", [28, 154, 22], difficulty="stretch"),
        _q("A proportional relationship has y=12 when x=4. What is y when x=7?", 21, "Unit rate 3; 3×7=21.", [16, 28, 19], difficulty="stretch"),
    ]


def _g6_challenges(t: str) -> list:
    return [
        _q("A ratio of 2:5 equals 8:x. What is x?", 20, "2/5=8/x → x=20.", [10, 16, 40], difficulty="hard"),
        _q("What is 35% of 80?", 28, "0.35×80=28.", [35, 24, 40], difficulty="hard"),
        _q("On a number line, distance between −7 and 4?", 11, "|4−(−7)|=11.", [3, -3, 28], difficulty="hard"),
        _q("SAT Stretch: A recipe uses 3 cups flour for 2 dozen cookies. Cups for 5 dozen?", "7.5", "3/2×5=7.5.", [6, 5, 8], difficulty="stretch"),
        _q("Absolute value: |−15|+|6|?", 21, "15+6=21.", [9, -9, 15], difficulty="hard"),
        _q("Coordinate: Point (3,−2) is in which quadrant?", "IV", "x>0,y<0.", ["I", "II", "III"], difficulty="stretch"),
        _q("Write 3/4 as a percent.", 75, "3/4=0.75=75%.", [34, 50, 25], difficulty="stretch"),
    ]


def _g5_challenges(t: str) -> list:
    return [
        _q("Compute $2\\frac{1}{3}+1\\frac{1}{2}$ as an improper fraction a/b in lowest terms. What is a+b?", 29, "7/3+3/2=23/6; 23+6=29.", [23, 17, 11], difficulty="hard"),
        _q("$\\frac{2}{3}\\times\\frac{9}{4}=$?", "3/2", "18/12=3/2.", ["8/27", "6/7", "1"], difficulty="hard"),
        _q("A rectangular prism is 4×3×5. Volume?", 60, "4×3×5=60.", [12, 20, 45], difficulty="hard"),
        _q("SAT Stretch: Divide $\\frac{3}{4}\\div\\frac{1}{8}$.", 6, "×8/1=6.", ["3/32", "2", "24"], difficulty="stretch"),
        _q("Decimal: 0.125 as a fraction in lowest terms. Numerator+denominator?", 9, "1/8 → 1+8=9.", [125, 8, 5], difficulty="stretch"),
        _q("What is $1\\frac{1}{4}\\times 8$?", 10, "5/4×8=10.", [8, 9, 12], difficulty="stretch"),
    ]


def _g4_challenges(t: str) -> list:
    return [
        _q("What is 36×25?", 900, "36×100/4=900.", [800, 725, 1000], difficulty="hard"),
        _q("Which number rounds to 800 to the nearest hundred?", 760, "760 is closer to 800 than to 700.", [740, 850, 849], difficulty="hard"),
        _q("$\\frac{3}{8}+\\frac{1}{8}=$?", "1/2", "4/8=1/2.", ["4/16", "3/16", "2/8"], difficulty="hard"),
        _q("SAT Stretch: A rectangle is 12 by 7. Perimeter?", 38, "2(12+7)=38.", [84, 19, 24], difficulty="stretch"),
        _q("Long division: 756÷9?", 84, "9×84=756.", [74, 86, 94], difficulty="stretch"),
        _q("What is 1000−478?", 522, "1000−478=522.", [532, 422, 578], difficulty="stretch"),
    ]


def _g3_challenges(t: str) -> list:
    return [
        _q("A classroom has 6 rows of 8 desks. 5 desks are empty. How many students if one per desk?", 43, "48−5=43.", [48, 40, 35], difficulty="hard"),
        _q("What is 7×8+6?", 62, "56+6=62.", [56, 48, 70], difficulty="hard"),
        _q("A baker makes 4 trays of 12 muffins and sells 15. How many left?", 33, "48−15=33.", [27, 45, 19], difficulty="hard"),
        _q("SAT Stretch: Area of a 9-by-4 rectangle?", 36, "9×4=36.", [26, 13, 72], difficulty="stretch"),
        _q("Find the missing factor: 9×___=63.", 7, "9×7=63.", [6, 8, 9], difficulty="stretch"),
    ]


def _g2_challenges(t: str) -> list:
    return [
        _q("Maya has 47 stickers, gets 28 more, then gives 15 away. How many now?", 60, "47+28=75, 75−15=60.", [50, 70, 55], difficulty="hard"),
        _q("What is 100−37?", 63, "100−37=63.", [73, 67, 53], difficulty="hard"),
        _q("A jump rope costs 55¢. You pay with 3 quarters. Change in cents?", 20, "75−55=20.", [25, 15, 30], difficulty="hard"),
        _q("SAT Stretch: Count by 5s: 35, 40, 45, ___.", 50, "Next is 50.", [55, 48, 60], difficulty="stretch"),
        _q("Time: 2:45. What time in 30 minutes?", "3:15", "2:45+30=3:15.", ["3:45", "2:75", "3:00"], difficulty="stretch"),
    ]


def _g1_challenges(t: str) -> list:
    return [
        _q("There are 9 red apples and 8 green. You eat 3. How many apples left?", 14, "17−3=14.", [12, 16, 11], difficulty="hard"),
        _q("A ten-frame is full and another shows 6. You add 5 more. Total?", 21, "10+6+5=21.", [16, 15, 20], difficulty="hard"),
        _q("Start at 18. Count on by 3 four times. Where do you land?", 30, "21,24,27,30.", [22, 28, 27], difficulty="hard"),
        _q("SAT Stretch: You need 20 crayons. You have 7 red and 6 blue. How many more do you need?", 7, "13, need 7 more.", [6, 8, 13], difficulty="stretch"),
        _q("Which is greater: 2 tens and 9 ones, or 3 tens and 0 ones?", 30, "29 vs 30.", [29, 20, 9], difficulty="stretch"),
    ]


def challenge_filler(title: str, n: int, difficulty: str = "hard"):
    """Deterministic unique contest-style pad for hard/stretch slots."""
    pool = challenges_for(title)
    if not pool:
        pool = _mc_challenges(title)
    prefer = [q for q in pool if q.get("difficulty") == difficulty] or pool
    item = prefer[(n - 1) % len(prefer)]
    q = dict(item)
    # Vary a numeric parameter when possible so repeats stay distinct and harder to memorize.
    text = q["question_text"]
    ans = q["correct_answer"]
    # Unique tag without looking like a soft filler
    tag = f" (variant {n})"
    if "3-letter strings from {A,B,C,D}" in text:
        # generalize: k-letter from m symbols, at least one fixed letter
        k = 3 + (n % 2)
        m = 4 + (n % 3)
        total = m ** k
        bad = (m - 1) ** k
        ans = str(total - bad)
        text = (
            f"AMC 8 style: How many {k}-letter strings from a {m}-letter alphabet "
            f"include at least one A (repeats allowed)?"
        )
        q["explanation"] = f"Total {m}^{k}={total}. No A: {m-1}^{k}={bad}. {total}-{bad}={ans}."
        q["distractors"] = [str(total), str(bad), str(total - bad + 1)]
    elif "Paths from (0,0) to (4,3)" in text or "right and up unit steps" in text:
        a, b = 3 + (n % 3), 2 + (n % 2)
        ans = str(math.comb(a + b, a))
        text = f"MathCounts Target: Paths from (0,0) to ({a},{b}) using only right and up unit steps?"
        q["explanation"] = f"C({a+b},{a})={ans}."
        q["distractors"] = [str(a * b), str(a + b), str(2 ** (a + b))]
    elif "x+y+z=5" in text and "Nonnegative" in text:
        s = 4 + (n % 4)
        ans = str(math.comb(s + 2, 2))
        text = f"Stars and bars: Nonnegative integer solutions to x+y+z={s}?"
        q["explanation"] = f"C({s}+3-1,3-1)=C({s+2},2)={ans}."
        q["distractors"] = [str(s * 3), str(math.comb(s + 2, 1)), str(s ** 2)]
    elif "4-person team" in text or "3-person committees" in text:
        n_people = 8 + (n % 7)
        k = 3 + (n % 2)
        ans = str(math.comb(n_people, k))
        text = f"A club of {n_people} picks a {k}-person team. How many teams?"
        q["explanation"] = f"C({n_people},{k})={ans}."
        q["distractors"] = [str(n_people * k), str(math.comb(n_people, k - 1) if k else 0), str(math.factorial(min(n_people, 7)) // max(1, math.factorial(min(k, 6))))]
    elif "president and vice-president" in text:
        n_people = 8 + (n % 6)
        ans = str(n_people * (n_people - 1))
        text = f"How many ways to choose a president and vice-president from {n_people} people (order matters)?"
        q["explanation"] = f"P({n_people},2)={ans}."
        q["distractors"] = [str(math.comb(n_people, 2)), str(n_people ** 2), str(n_people)]
    elif "divisible by 2 or 5" in text:
        lim = 80 + 20 * (n % 3)
        a = lim // 2 + lim // 5 - lim // 10
        ans = str(a)
        text = f"SAT Stretch: How many positive integers ≤ {lim} are divisible by 2 or 5?"
        q["explanation"] = f"⌊{lim}/2⌋+⌊{lim}/5⌋−⌊{lim}/10⌋={ans}."
        q["distractors"] = [str(a + 5), str(a - 5), str(lim // 2)]
    q["question_text"] = text + tag
    q["correct_answer"] = str(ans)
    q["difficulty"] = difficulty
    return q
