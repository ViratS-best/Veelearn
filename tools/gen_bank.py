"""Procedural question families for the bulk bank.

Every item here is computed, not recalled: the answer comes from Python arithmetic
and the distractors are the specific wrong answers a learner actually produces
(dropping the second step, using the wrong base, integer division instead of true
division, and so on). That keeps a bank of tens of thousands of questions honest
without copying anyone's content.

`tools/build_open_bank.py` calls `build_generated()` and mixes these items with the
openly licensed datasets.
"""

from __future__ import annotations

import math
import random
from fractions import Fraction

LETTERS = "ABCD"


def fmt_num(value):
    """Plain display for an int/float, with no trailing .0 and no float noise."""
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)
    if isinstance(value, float) and abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    if isinstance(value, float):
        return ("%.2f" % value).rstrip("0").rstrip(".")
    return str(value)


def make(skill, tier, stem, correct, wrongs, hints, steps, rng):
    """Assemble one item with four distinct options and a rotated answer key."""
    options = [(fmt_num(correct), True, "")] + [(fmt_num(t), False, w) for t, w in wrongs]
    texts = [o[0] for o in options]
    if len(set(texts)) != 4 or not all(t.strip() for t in texts):
        return None
    rng.shuffle(options)
    out = []
    answer = None
    for i, (text, ok, why) in enumerate(options):
        key = LETTERS[i]
        out.append({"k": key, "t": text, "why": why})
        if ok:
            answer = key
    if answer is None:
        return None
    return {
        "skill": skill,
        "tier": tier,
        "stem": stem,
        "options": out,
        "answer": answer,
        "hints": hints,
        "steps": steps,
    }


# --------------------------------------------------------------------------- #
# Grades 1-8 arithmetic, fractions, percent, ratio, geometry, probability
# --------------------------------------------------------------------------- #


def arith(rng):
    kind = rng.choice(["mul", "add", "sub", "div"])
    if kind == "mul":
        a, b = rng.randint(3, 12), rng.randint(3, 12)
        return make(
            "gen.k5.arith", 1,
            f"What is {a} × {b}?",
            a * b,
            [(a * (b + 1), f"That is {a} × {b + 1}, one group too many."),
             ((a + 1) * b, f"That is {a + 1} × {b}, one group too many."),
             (a + b, "That adds the two numbers instead of multiplying.")],
            ["Split one factor into friendly parts.", f"Try {a} × {b} = {a} × {b - 1} + {a}."],
            [f"{a} × {b} = {a * b}."],
            rng,
        )
    if kind == "add":
        a, b = rng.randint(120, 980), rng.randint(120, 980)
        return make(
            "gen.k5.arith", 1,
            f"What is {a} + {b}?",
            a + b,
            [(a + b + 10, "That is ten too many — check the tens column."),
             (a + b - 10, "That is ten too few — check the tens column."),
             (a + b + 100, "That is a hundred too many — check the hundreds column.")],
            ["Add the ones, then the tens, then the hundreds.", "Line up the place values before adding."],
            [f"{a} + {b} = {a + b}."],
            rng,
        )
    if kind == "sub":
        a = rng.randint(400, 990)
        b = rng.randint(120, a - 50)
        return make(
            "gen.k5.arith", 1,
            f"What is {a} − {b}?",
            a - b,
            [(a - b + 10, "That is ten too many — you borrowed twice."),
             (a - b - 10, "That is ten too few — check the tens column."),
             (a + b, "That adds the numbers instead of subtracting.")],
            ["Subtract the ones first, borrowing if needed.", "Check by adding your answer back to the smaller number."],
            [f"{a} − {b} = {a - b}."],
            rng,
        )
    b = rng.randint(3, 12)
    q = rng.randint(3, 12)
    a = b * q
    return make(
        "gen.k5.arith", 1,
        f"What is {a} ÷ {b}?",
        q,
        [(q + 1, f"{b} × {q + 1} is {b * (q + 1)}, which is too big."),
         (q - 1, f"{b} × {q - 1} is {b * (q - 1)}, which is too small."),
         (a - b, "That subtracts the divisor instead of dividing.")],
        [f"Ask: {b} times what number gives {a}?", "Use the multiplication facts."],
        [f"{b} × {q} = {a}, so {a} ÷ {b} = {q}."],
        rng,
    )


def fractions(rng):
    kind = rng.choice(["add", "simplify", "of"])
    if kind == "add":
        b, d = rng.randint(2, 12), rng.randint(2, 12)
        a = rng.randint(1, b - 1)
        c = rng.randint(1, d - 1)
        correct = Fraction(a, b) + Fraction(c, d)
        wrong1 = Fraction(a + c, b + d)
        wrong2 = Fraction(a * c, b * d)
        wrong3 = Fraction(a + c, b)
        return make(
            "gen.k5.fractions", 2,
            f"What is {a}/{b} + {c}/{d}?",
            correct,
            [(wrong1, "That adds numerators and denominators separately — rename to a common denominator first."),
             (wrong2, "That multiplies the fractions instead of adding them."),
             (wrong3, f"That keeps the denominator {b} and adds only the numerators.")],
            [f"Rewrite each fraction with a common denominator.", f"Use {b * d} as the common denominator."],
            [f"{a}/{b} = {a * d}/{b * d} and {c}/{d} = {c * b}/{b * d}.",
             f"The sum is {correct}."],
            rng,
        )
    if kind == "simplify":
        base_b = rng.randint(2, 12)
        base_a = rng.randint(1, base_b - 1)
        while math.gcd(base_a, base_b) != 1:
            base_a = rng.randint(1, base_b - 1)
        k = rng.randint(2, 9)
        a, b = base_a * k, base_b * k
        correct = Fraction(base_a, base_b)
        return make(
            "gen.k5.fractions", 2,
            f"Simplify {a}/{b}.",
            correct,
            [(Fraction(base_b, base_a) if base_a > 0 else Fraction(1, 2), "That flips the fraction upside down."),
             (Fraction(a, base_b), "That divides only the denominator."),
             (Fraction(base_a, b), "That divides only the numerator.")],
            [f"What is the greatest common factor of {a} and {b}?", f"It is {math.gcd(a, b)}."],
            [f"{a} ÷ {math.gcd(a, b)} = {a // math.gcd(a, b)} and {b} ÷ {math.gcd(a, b)} = {b // math.gcd(a, b)}.",
             f"So the fraction is {correct}."],
            rng,
        )
    b = rng.randint(2, 9)
    a = rng.randint(1, b - 1)
    n = b * rng.randint(2, 20)
    correct = Fraction(a, b) * n
    return make(
        "gen.k5.fractions", 2,
        f"What is {a}/{b} of {n}?",
        correct,
        [(Fraction(a, n) * b if n else 0, "That divides by the wrong number."),
         (n // b, "That finds one part only, not the fraction asked for."),
         (Fraction(n, b) * (a + 1), "That takes one part too many.")],
        [f"Divide {n} into {b} equal parts.", f"Each part is {n // b}."],
        [f"{n} ÷ {b} = {n // b}.", f"Take {a} of those parts: {correct}."],
        rng,
    )


def percent(rng):
    kind = rng.choice(["of", "off", "change", "which"])
    p = rng.choice([5, 10, 12, 15, 18, 20, 24, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90])
    n = rng.randrange(20, 501, 5)
    if kind == "of":
        correct = p * n // 100
        return make(
            "gen.mid.percent", 2,
            f"What is {p}% of {n}?",
            correct,
            [(p, "That copies the percent instead of applying it."),
             (n - correct, "That is the part left over, not the part asked for."),
             (n // p if p else 0, "That divides by the percent instead of taking a percent.")],
            ["Percent means per hundred.", f"{p}% = {p / 100:g}, so multiply {n} by it."],
            [f"{p}/100 × {n} = {correct}."],
            rng,
        )
    if kind == "off":
        price = rng.randrange(20, 401, 10)
        disc = price * p // 100
        return make(
            "gen.mid.percent", 2,
            f"A ${price} item is {p}% off. What is the sale price?",
            price - disc,
            [(disc, "That is the discount itself, not the price you pay."),
             (price - p, "That subtracts the percent as if it were dollars."),
             (price - 2 * disc, "That subtracts the discount twice.")],
            [f"Find {p}% of {price} first.", f"It is ${disc}."],
            [f"{price} − {disc} = ${price - disc}."],
            rng,
        )
    if kind == "change":
        old = rng.randrange(10, 201, 5)
        new = old + rng.randint(1, old)
        correct = round((new - old) / old * 100)
        return make(
            "gen.mid.percent", 3,
            f"A price rises from ${old} to ${new}. What is the percent increase?",
            correct,
            [(new - old, "That is the dollar increase, not the percent."),
             (round((new - old) / new * 100), "That divides by the new price instead of the original."),
             (round(new / old * 100), "That is the new price as a percent of the old, not the increase.")],
            ["Percent change = change ÷ original × 100.", f"The change is ${new - old}."],
            [f"{new - old} ÷ {old} = {(new - old) / old:.3f}.", f"That is {correct}%."],
            rng,
        )
    whole = rng.randrange(40, 501, 10)
    part = rng.randint(4, whole // 2)
    correct = round(part / whole * 100)
    return make(
        "gen.mid.percent", 3,
        f"What percent of {whole} is {part}?",
        f"{correct}%",
        [(f"{part}%", "That copies the part instead of comparing it to the whole."),
         (f"{whole - part}%", "That is the share that is left."),
         (f"{round(whole / part * 100)}%", "That divides the whole by the part, the wrong way round.")],
        ["Put the part over the whole.", f"{part}/{whole} = ?"],
        [f"{part} ÷ {whole} = {part / whole:.3f}.", f"That is {correct}%."],
        rng,
    )


def ratio(rng):
    kind = rng.choice(["unit", "proportion", "ratio_given", "speed"])
    if kind == "unit":
        unit = rng.randint(2, 9)
        q = rng.randint(2, 15)
        total = unit * q
        want = rng.randint(2, 20)
        correct = unit * want
        return make(
            "gen.mid.ratio", 2,
            f"If {q} notebooks cost ${total}, how much do {want} notebooks cost?",
            f"${correct}",
            [(f"${total}", "That is the price of the first group."),
             (f"${total + want}", "That adds the count to the price."),
             (f"${unit}", "That is only one notebook.")],
            ["Find the price of one notebook.", f"${total} ÷ {q} = ${unit}."],
            [f"${unit} × {want} = ${correct}."],
            rng,
        )
    if kind == "proportion":
        a, b = rng.randint(2, 15), rng.randint(2, 20)
        mult = rng.randint(2, 9)
        c = b * mult
        correct = a * mult
        return make(
            "gen.mid.ratio", 2,
            f"Solve the proportion: {a}/{b} = x/{c}.",
            correct,
            [(a * c, "That multiplies the numerator by the new denominator instead of scaling."),
             (b * mult, "That is the scale factor times the denominator."),
             (c - a, "That subtracts instead of scaling.")],
            [f"How many times does {b} fit into {c}?", f"The scale factor is {mult}."],
            [f"x = {a} × {mult} = {correct}."],
            rng,
        )
    if kind == "ratio_given":
        r1, r2 = rng.randint(1, 9), rng.randint(1, 9)
        if r1 == r2 or r1 == 0:
            return None
        mult = rng.randint(2, 15)
        have = r1 * mult
        correct = r2 * mult
        return make(
            "gen.mid.ratio", 3,
            f"The ratio of red to blue marbles is {r1} : {r2}. If there are {have} red marbles, how many are blue?",
            correct,
            [(have + (r2 - r1), "That adds the difference instead of scaling."),
             (r2 * (mult + 1), "That uses one scale step too many."),
             (have, "That assumes both colours are equal.")],
            [f"Find the scale factor: {have} ÷ {r1}.", f"It is {mult}."],
            [f"{r2} × {mult} = {correct}."],
            rng,
        )
    dist = rng.choice([120, 150, 180, 240])
    hours = rng.choice([2, 3, 4, 5])
    correct = dist // hours
    return make(
        "gen.mid.ratio", 2,
        f"A train travels {dist} miles in {hours} hours. What is its average speed in miles per hour?",
        f"{correct} mph",
        [(f"{hours} mph", "That is the time, not the speed."),
         (f"{dist} mph", "That is the distance, not the speed."),
         (f"{correct * 2} mph", "That doubles the speed.")],
        ["Speed = distance ÷ time.", f"{dist} ÷ {hours}."],
        [f"{dist} ÷ {hours} = {correct} mph."],
        rng,
    )


def geometry(rng):
    kind = rng.choice(["rect", "tri", "circle", "pyth", "box"])
    if kind == "rect":
        w, h = rng.randint(2, 40), rng.randint(2, 40)
        ask_area = rng.random() < 0.5
        if ask_area:
            return make(
                "gen.geometry.mensuration", 2,
                f"What is the area of a rectangle {w} cm by {h} cm?",
                f"{w * h} cm²",
                [(f"{2 * (w + h)} cm²", "That is the perimeter."),
                 (f"{w + h} cm²", "That adds the sides instead of multiplying."),
                 (f"{2 * w * h} cm²", "That doubles the area.")],
                ["Area of a rectangle is length × width.", f"{w} × {h}."],
                [f"{w} × {h} = {w * h} cm²."],
                rng,
            )
        return make(
            "gen.geometry.mensuration", 2,
            f"What is the perimeter of a rectangle {w} cm by {h} cm?",
            f"{2 * (w + h)} cm",
            [(f"{w * h} cm", "That is the area."),
             (f"{w + h} cm", "That adds only two sides."),
             (f"{4 * (w + h)} cm", "That counts the sides twice over.")],
            ["Perimeter = 2(length + width).", f"2 × ({w} + {h})."],
            [f"2 × {w + h} = {2 * (w + h)} cm."],
            rng,
        )
    if kind == "tri":
        b, h = rng.randint(2, 40), rng.randint(2, 30)
        return make(
            "gen.geometry.mensuration", 2,
            f"What is the area of a triangle with base {b} and height {h}?",
            f"{b * h // 2} {'(half of ' + str(b * h) + ')' if (b * h) % 2 else ''}".strip(),
            [(f"{b * h}", "That is base × height; a triangle is half of that rectangle."),
             (f"{b + h}", "That adds the base and height."),
             (f"{2 * b * h}", "That doubles the rectangle instead of halving it.")],
            ["Area of a triangle is ½ × base × height.", f"½ × {b} × {h}."],
            [f"{b} × {h} = {b * h}, half of that is {b * h / 2:g}."],
            rng,
        )
    if kind == "circle":
        r = rng.randint(1, 25)
        ask_area = rng.random() < 0.5
        if ask_area:
            return make(
                "gen.geometry.mensuration", 2,
                f"What is the area of a circle with radius {r}? (Leave your answer in terms of π.)",
                f"{r * r}π",
                [(f"{2 * r}π", "That is the circumference, 2πr."),
                 (f"{r}π", "That is diameter × π."),
                 (f"{4 * r * r}π", "That treats the radius as a diameter.")],
                ["Area = πr².", f"r² = {r * r}."],
                [f"π × {r * r} = {r * r}π."],
                rng,
            )
        return make(
            "gen.geometry.mensuration", 2,
            f"What is the circumference of a circle with radius {r}? (Leave your answer in terms of π.)",
            f"{2 * r}π",
            [(f"{r * r}π", "That is the area, πr²."),
             (f"{r}π", "That is the diameter times π without doubling the radius."),
             (f"{4 * r}π", "That doubles the diameter.")],
            ["Circumference = 2πr.", f"2 × {r}."],
            [f"2π × {r} = {2 * r}π."],
            rng,
        )
    if kind == "pyth":
        triples = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (7, 24, 25), (9, 12, 15), (20, 21, 29),
                   (12, 16, 20), (15, 20, 25), (10, 24, 26), (18, 24, 30), (16, 30, 34), (21, 28, 35)]
        a, b, c = rng.choice(triples)
        return make(
            "gen.geometry.mensuration", 3,
            f"A right triangle has legs {a} and {b}. What is the length of the hypotenuse?",
            c,
            [(a + b, "That adds the legs instead of using Pythagoras."),
             (c + 1, "That is off by one — check the square root."),
             (abs(b - a) or a + b, "That subtracts the legs instead of adding their squares.")],
            ["Use a² + b² = c².", f"{a}² + {b}² = {a * a + b * b}."],
            [f"{a * a + b * b} has square root {c}.", f"So the hypotenuse is {c}."],
            rng,
        )
    l, w, h = rng.randint(2, 20), rng.randint(2, 20), rng.randint(2, 20)
    return make(
        "gen.geometry.mensuration", 3,
        f"What is the volume of a box {l} × {w} × {h}?",
        f"{l * w * h}",
        [(f"{l + w + h}", "That adds the three dimensions."),
         (f"{l * w}", "That multiplies only two dimensions."),
         (f"{2 * l * w * h}", "That doubles the volume.")],
        ["Volume = length × width × height.", f"{l} × {w} = {l * w}."],
        [f"{l * w} × {h} = {l * w * h}."],
        rng,
    )


def probability(rng):
    kind = rng.choice(["die", "sum", "coin", "marble"])
    if kind == "die":
        target = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        return make(
            "gen.probability.basic", 2,
            f"What is the probability of rolling a {target} on a fair six-sided die?",
            "1/6",
            [("1/3", "That counts two faces."),
             ("1/2", "That is the chance of an even number."),
             (f"{target}/6", "That puts the face value on top instead of 1.")],
            ["There are six equally likely faces.", "Only one of them shows the target."],
            ["1 favourable out of 6.", "So the probability is 1/6."],
            rng,
        )
    if kind == "sum":
        total = rng.choice([5, 6, 7, 8])
        ways = {5: 4, 6: 5, 7: 6, 8: 5}[total]
        correct = Fraction(ways, 36)
        return make(
            "gen.probability.basic", 3,
            f"Two fair dice are rolled. What is the probability that the sum is {total}?",
            f"{ways}/36",
            [(f"{ways}/12", "That divides by the faces of one die instead of all 36 pairs."),
             (f"{total}/36", "That counts the total instead of the pairs."),
             (f"{ways + 1}/36", "That counts one pair too many.")],
            ["There are 36 equally likely pairs.", f"Count the pairs that add to {total}."],
            [f"{ways} pairs out of 36.", f"That is {correct}, written as {ways}/36."],
            rng,
        )
    if kind == "coin":
        flips = rng.choice([2, 3])
        all_heads = Fraction(1, 2 ** flips)
        return make(
            "gen.probability.basic", 3,
            f"A fair coin is flipped {flips} times. What is the probability of heads every time?",
            f"1/{2 ** flips}",
            [(f"1/{flips}", "That divides by the number of flips instead of multiplying."),
             (f"{flips}/{2 ** flips}", "That counts flips instead of outcomes."),
             ("1/2", "That is the chance for a single flip.")],
            [f"Each flip has probability 1/2.", f"Multiply 1/2 by itself {flips} times."],
            [f"(1/2)^{flips} = 1/{2 ** flips}."],
            rng,
        )
    red, blue = rng.randint(2, 25), rng.randint(2, 25)
    return make(
        "gen.probability.basic", 2,
        f"A bag has {red} red and {blue} blue marbles. One marble is drawn at random. What is P(red)?",
        f"{red}/{red + blue}",
        [(f"{blue}/{red + blue}", "That is the probability of blue."),
         (f"{red}/{blue}", "That compares the counts instead of dividing by the total."),
         (f"1/{red}", "That assumes all marbles are distinct colours.")],
        [f"Count the total: {red} + {blue}.", "P(red) = red ÷ total."],
        [f"{red}/{red + blue}."],
        rng,
    )


# --------------------------------------------------------------------------- #
# Algebra, SAT-style and ACT-style
# --------------------------------------------------------------------------- #


def algebra(rng):
    kind = rng.choice(["linear", "two_step", "eval", "slope", "fraction"])
    if kind == "linear":
        a, x = rng.randint(2, 12), rng.randint(2, 30)
        b = rng.randint(1, 40)
        c = a * x + b
        return make(
            "gen.algebra.linear", 2,
            f"Solve for x: {a}x + {b} = {c}.",
            x,
            [(x + b, "That subtracts the constant from x instead of from both sides."),
             (c // a, "That divides before undoing the +" + str(b) + "."),
             (c - b, "That stops at " + str(c - b) + ", before dividing by " + str(a) + ".")],
            [f"First subtract {b} from both sides.", f"Then divide by {a}."],
            [f"{a}x = {c - b}.", f"x = {x}."],
            rng,
        )
    if kind == "two_step":
        a, x = rng.randint(2, 12), rng.randint(2, 25)
        b = rng.randint(1, 40)
        c = a * x - b
        return make(
            "gen.algebra.linear", 2,
            f"Solve for x: {a}x − {b} = {c}.",
            x,
            [(c + b, "That adds the constant instead of removing it."),
             (c // a, "That divides before adding " + str(b) + " back."),
             (x + 1, "That is one too many — check the division.")],
            [f"Add {b} to both sides.", f"Then divide by {a}."],
            [f"{a}x = {c + b}.", f"x = {x}."],
            rng,
        )
    if kind == "eval":
        m, b = rng.randint(2, 12), rng.randint(-20, 20)
        x = rng.randint(-12, 15)
        correct = m * x + b
        sign = "+" if b >= 0 else "−"
        return make(
            "gen.algebra.linear", 2,
            f"If f(x) = {m}x {sign} {abs(b)}, what is f({x})?",
            correct,
            [(m * x, "That forgets the constant term."),
             (m + x + b, "That adds the slope and the input instead of multiplying."),
             (correct + 2 * abs(b) if b else correct + m, "That applies the constant with the wrong sign.")],
            ["Substitute the value for x.", f"{m}({x}) {sign} {abs(b)}."],
            [f"{m * x} {sign} {abs(b)} = {correct}."],
            rng,
        )
    if kind == "slope":
        x1 = rng.randint(-12, 12)
        y1 = rng.randint(-15, 15)
        dx = rng.randint(1, 12)
        dy = rng.choice([-9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        x2, y2 = x1 + dx, y1 + dy
        correct = Fraction(dy, dx)
        return make(
            "gen.algebra.linear", 3,
            f"What is the slope of the line through ({x1}, {y1}) and ({x2}, {y2})?",
            correct,
            [(Fraction(dx, dy), "That is change in x over change in y, upside down."),
             (dy, "That is only the change in y."),
             (Fraction(dy, dx) + 1, "That adds 1 to the slope for no reason.")],
            ["Slope = change in y ÷ change in x.", f"Δy = {dy} and Δx = {dx}."],
            [f"{dy}/{dx} = {correct}."],
            rng,
        )
    den = rng.randint(2, 12)
    x = rng.randint(2, 15) * den
    k = rng.randint(1, 20)
    c = x // den + k
    return make(
        "gen.algebra.linear", 3,
        f"Solve for x: x/{den} + {k} = {c}.",
        x,
        [(c - k, "That stops before multiplying by the denominator."),
         (c * den, "That multiplies the whole right side instead of just the fraction."),
         (x + den, "That is one denominator too large.")],
        [f"Subtract {k} from both sides.", f"Then multiply by {den}."],
        [f"x/{den} = {c - k}.", f"x = {(c - k) * den}."],
        rng,
    )


def sat_math(rng):
    kind = rng.choice(["model", "percent", "average", "geometry", "system"])
    if kind == "model":
        rate = rng.randint(3, 25)
        start = rng.randint(10, 90)
        hours = rng.randint(2, 15)
        correct = start + rate * hours
        return make(
            "gen.sat.math", 3,
            f"A gym charges a ${start} joining fee plus ${rate} per month. What is the total cost for {hours} months?",
            f"${correct}",
            [(f"${rate * hours}", "That forgets the joining fee."),
             (f"${start * hours}", "That multiplies the joining fee by the months."),
             (f"${start + hours}", "That adds the months instead of the monthly charge.")],
            ["Total = joining fee + monthly rate × months.", f"{rate} × {hours} = {rate * hours}."],
            [f"{start} + {rate * hours} = {correct}."],
            rng,
        )
    if kind == "percent":
        price = rng.randrange(50, 501, 10)
        p = rng.choice([10, 15, 20, 25, 30, 35, 40])
        disc = price * p // 100
        tax = (price - disc) * 10 // 100
        return make(
            "gen.sat.math", 4,
            f"A ${price} item is {p}% off, and 10% tax is added to the sale price. What is the total?",
            f"${price - disc + tax}",
            [(f"${price - disc}", "That forgets the tax."),
             (f"${price - disc + price * 10 // 100}", "That applies tax to the original price instead of the sale price."),
             (f"${price - p}", "That treats the percent as dollars.")],
            [f"Sale price = {price} − {disc}.", f"Tax is 10% of the sale price."],
            [f"Sale price ${price - disc} + tax ${tax} = ${price - disc + tax}."],
            rng,
        )
    if kind == "average":
        n = rng.randint(3, 8)
        avg = rng.randint(10, 60)
        total = n * avg
        known = [rng.randint(5, 45) for _ in range(n - 1)]
        missing = total - sum(known)
        if missing < 0:
            return None
        return make(
            "gen.sat.math", 3,
            f"The average of {n} numbers is {avg}. {n - 1} of them are {', '.join(map(str, known))}. What is the missing number?",
            missing,
            [(total, "That is the sum of all the numbers, not the missing one."),
             (avg, "That is the average itself."),
             (missing + n, "That adds the count to the answer.")],
            [f"The sum of all {n} numbers is {avg} × {n} = {total}.", f"The known numbers add to {sum(known)}."],
            [f"{total} − {sum(known)} = {missing}."],
            rng,
        )
    if kind == "geometry":
        w = rng.randint(2, 30)
        h = rng.randint(2, 30)
        scale = rng.choice([2, 3, 4, 5])
        return make(
            "gen.sat.math", 3,
            f"A rectangle is {w} by {h}. If both sides are multiplied by {scale}, the area becomes how many times larger?",
            scale * scale,
            [(scale, "That is the factor for each side, not the area."),
             (2 * scale, "That adds the factors instead of multiplying them."),
             (scale * scale * 2, "That doubles the new area factor.")],
            ["Area scales with the square of the linear factor.", f"The linear factor is {scale}."],
            [f"{w} × {h} = {w * h} and the new area is {w * scale} × {h * scale} = {w * h * scale * scale}.", f"That is {scale * scale} times larger."],
            rng,
        )
    a = rng.randint(2, 12)
    b = rng.randint(1, 12)
    x = rng.randint(2, 15)
    y = rng.randint(1, 15)
    s = a * x + b * y
    d = a * x - b * y
    if d <= 0:
        return None
    return make(
        "gen.sat.math", 4,
        f"If {a}x + {b}y = {s} and {a}x − {b}y = {d}, what is x?",
        x,
        [(y, "That is the value of y, not x."),
         (s - d, "That is 2by, before dividing by anything."),
         (s // a, "That assumes b y is zero.")],
        ["Add the two equations to eliminate y.", f"You get {2 * a}x = {s + d}."],
        [f"x = {s + d} ÷ {2 * a} = {x}."],
        rng,
    )


def act_math(rng):
    kind = rng.choice(["avg", "convert", "interest", "area", "ratio"])
    if kind == "avg":
        a, b, c = rng.randint(5, 120), rng.randint(5, 120), rng.randint(5, 120)
        correct = Fraction(a + b + c, 3)
        return make(
            "gen.act.math", 2,
            f"What is the average of {a}, {b} and {c}?",
            correct,
            [(a + b + c, "That is the sum, not divided by the count."),
             (Fraction(a + b + c, 2), "That divides by 2 instead of 3."),
             (max(a, b, c), "That is the largest value, not the average.")],
            ["Add the values, then divide by how many there are.", "There are three values."],
            [f"{a + b + c} ÷ 3 = {correct}."],
            rng,
        )
    if kind == "convert":
        hours = rng.randint(1, 5)
        minutes = rng.choice([15, 20, 30, 45])
        total = hours * 60 + minutes
        return make(
            "gen.act.math", 2,
            f"How many minutes are there in {hours} hours and {minutes} minutes?",
            total,
            [(hours + minutes, "That adds unlike units."),
             (hours * 100 + minutes, "That treats an hour as 100 minutes."),
             (total - 60, "That is one hour too few.")],
            ["An hour is 60 minutes.", f"{hours} × 60 = {hours * 60}."],
            [f"{hours * 60} + {minutes} = {total} minutes."],
            rng,
        )
    if kind == "interest":
        principal = rng.randrange(200, 5001, 100)
        rate = rng.choice([2, 3, 4, 5, 6, 7, 8])
        years = rng.choice([2, 3, 4, 5, 6, 7, 8])
        interest = principal * rate * years // 100
        return make(
            "gen.act.math", 3,
            f"How much simple interest accrues on ${principal} at {rate}% per year for {years} years?",
            f"${interest}",
            [(f"${principal * rate // 100}", "That is only one year of interest."),
             (f"${principal + interest}", "That is the total balance, not the interest."),
             (f"${rate * years}", "That multiplies the percent by the years only.")],
            ["Simple interest = principal × rate × time.", f"{principal} × {rate / 100:g} × {years}."],
            [f"${interest}."],
            rng,
        )
    if kind == "area":
        b, h = rng.randint(6, 20), rng.randint(4, 14)
        return make(
            "gen.act.math", 2,
            f"A triangle has a base of {b} and a height of {h}. What is its area?",
            f"{b * h / 2:g}",
            [(f"{b * h}", "That is base × height without halving."),
             (f"{b + h}", "That adds the base and height."),
             (f"{2 * b * h}", "That doubles the rectangle.")],
            ["Area = ½bh.", f"½ × {b} × {h}."],
            [f"{b * h / 2:g}."],
            rng,
        )
    g, b = rng.choice([(2, 5), (3, 4), (4, 7), (5, 3)])
    total = (g + b) * rng.randint(2, 8)
    return make(
        "gen.act.math", 3,
        f"A bag has green and blue marbles in the ratio {g} : {b}. If there are {total} marbles in all, how many are green?",
        total * g // (g + b),
        [(total * b // (g + b), "That is the number of blue marbles."),
         (total // g, "That divides by the ratio number instead of by the total parts."),
         (total - g, "That subtracts the ratio number from the total.")],
        [f"There are {g + b} parts in all.", f"Each part is {total} ÷ {g + b}."],
        [f"Green is {g} parts: {total * g // (g + b)}."],
        rng,
    )


# --------------------------------------------------------------------------- #
# Contest-style (original problems in each contest's style, answers computed)
# --------------------------------------------------------------------------- #


def amc8(rng):
    kind = rng.choice(["divisible", "lcm", "consecutive", "digits"])
    if kind == "divisible":
        k = rng.randint(2, 12)
        lo = rng.randrange(1, 250)
        hi = lo + rng.randint(20, 300)
        correct = sum(1 for n in range(lo, hi + 1) if n % k == 0)
        return make(
            "gen.contest.amc8", 2,
            f"How many integers from {lo} to {hi} inclusive are divisible by {k}?",
            correct,
            [(hi // k, "That counts from 1, not from the lower bound."),
             (correct + 1, "That includes one extra multiple."),
             (correct - 1, "That misses one multiple.")],
            [f"Find the smallest multiple of {k} at or above {lo}.", f"It is {((lo + k - 1) // k) * k}."],
            [f"The multiples run up to {hi // k * k}.", f"That gives {correct} numbers."],
            rng,
        )
    if kind == "lcm":
        a, b = rng.randint(4, 26), rng.randint(4, 26)
        if math.gcd(a, b) == 1:
            return None
        correct = a * b // math.gcd(a, b)
        return make(
            "gen.contest.amc8", 2,
            f"What is the least common multiple of {a} and {b}?",
            correct,
            [(a * b, "That is the product, which is only the LCM when the numbers share no factor."),
             (math.gcd(a, b), "That is the greatest common divisor."),
             (correct * 2, "That is a common multiple, but not the least one.")],
            ["Factor both numbers.", "Take the highest power of each prime."],
            [f"lcm({a}, {b}) = {correct}."],
            rng,
        )
    if kind == "consecutive":
        n = rng.randint(2, 14)
        start = rng.randint(1, 80)
        total = sum(range(start, start + n))
        return make(
            "gen.contest.amc8", 3,
            f"What is the sum of the {n} consecutive integers starting at {start}?",
            total,
            [(start + n, "That is the last term, not the sum."),
             (start * n, "That multiplies the first term by the count."),
             (total - n, "That misses one term.")],
            ["List the terms, or use sum = count × (first + last)/2.", f"The last term is {start + n - 1}."],
            [f"{n} × ({start} + {start + n - 1}) ÷ 2 = {total}."],
            rng,
        )
    digits = rng.choice([2, 3, 4])
    lo = 10 ** (digits - 1)
    hi = 10 ** digits - 1
    d = rng.randint(0, 9)
    correct = sum(1 for n in range(lo, hi + 1) if str(d) in str(n))
    return make(
        "gen.contest.amc8", 4,
        f"How many {digits}-digit positive integers contain the digit {d}?",
        correct,
        [(correct + 1, "That counts one number twice."),
         ((hi - lo + 1) - correct, "That counts the numbers that do *not* contain the digit."),
         (digits * 9, "That is a guess about positions, not a count.")],
        ["Count the numbers that do not contain the digit, then subtract.", f"There are {hi - lo + 1} numbers in all."],
        [f"{hi - lo + 1} − {(hi - lo + 1) - correct} = {correct}."],
        rng,
    )


def amc10(rng):
    kind = rng.choice(["combo", "mod", "quadratic", "amgm"])
    if kind == "combo":
        n = rng.randint(5, 18)
        k = rng.randint(2, min(5, n - 1))
        correct = math.comb(n, k)
        return make(
            "gen.contest.amc10", 3,
            f"What is C({n}, {k})?",
            correct,
            [(math.perm(n, k), "That counts orderings; a combination ignores order."),
             (n * k, "That multiplies instead of choosing."),
             (correct // k, "That divides by k once too often.")],
            [f"C(n, k) = n! / (k!(n − k)!).", f"The product is {math.perm(n, k)}, then divide by {k}! = {math.factorial(k)}."],
            [f"{math.perm(n, k)} ÷ {math.factorial(k)} = {correct}."],
            rng,
        )
    if kind == "mod":
        a = rng.randint(2, 20)
        n = rng.randint(10, 200)
        m = rng.choice([3, 5, 7, 9, 11, 13, 17])
        correct = pow(a, n, m)
        return make(
            "gen.contest.amc10", 4,
            f"What is the remainder when {a}^{n} is divided by {m}?",
            correct,
            [(pow(a, n, m) + 1, "That is one more than the real remainder."),
             ((pow(a, n, m) - 1) % m, "That is one less than the real remainder."),
             (a % m, "That is the remainder of the base, not the power.")],
            [f"Find the cycle of {a} mod {m}.", "Reduce the exponent modulo the cycle length."],
            [f"{a}^{n} mod {m} = {correct}."],
            rng,
        )
    if kind == "quadratic":
        r = rng.randint(1, 15)
        s = rng.randint(r + 1, 25)
        b = -(r + s)
        c = r * s
        return make(
            "gen.contest.amc10", 3,
            f"What is the sum of the roots of x² {'+' if b >= 0 else '−'} {abs(b)}x + {c} = 0?",
            r + s,
            [(c, "That is the product of the roots."),
             (-(r + s), "That is −b, not −b/a with the sign applied to the sum."),
             (abs(b) + c, "That adds the coefficient and the constant.")],
            ["Sum of roots = −b/a.", f"b = {b} and a = 1."],
            [f"−({b}) = {r + s}."],
            rng,
        )
    x = rng.choice([2, 3, 4, 5, 6])
    k = rng.choice([4, 9, 16, 25, 36])
    correct = 2 * math.isqrt(k)
    return make(
        "gen.contest.amc10", 4,
        f"For positive x, what is the minimum value of x + {k}/x?",
        correct,
        [(math.isqrt(k), "That is the value at x = √k, not the sum there."),
         (k, "That is the constant, not the minimum of the whole expression."),
         (2 * k, "That doubles the constant instead of its square root.")],
        ["AM-GM: x + k/x ≥ 2√k.", f"√{k} = {math.isqrt(k)}."],
        [f"2 × {math.isqrt(k)} = {correct}, at x = {math.isqrt(k)}."],
        rng,
    )


def amc12(rng):
    kind = rng.choice(["log", "series", "trig", "complex"])
    if kind == "log":
        base = rng.randint(2, 10)
        exp = rng.randint(2, 5)
        value = base ** exp
        return make(
            "gen.contest.amc12", 3,
            f"What is log_{base}({value})?",
            exp,
            [(value // base, "That divides the argument by the base."),
             (base, "That is the base itself."),
             (exp + 1, "That is one power too many.")],
            [f"Ask: {base} to what power gives {value}?", f"{base}^{exp} = {value}."],
            [f"log_{base}({value}) = {exp}."],
            rng,
        )
    if kind == "series":
        a = rng.randint(1, 25)
        d = rng.randint(2, 12)
        n = rng.randint(5, 40)
        correct = n * (2 * a + (n - 1) * d) // 2
        return make(
            "gen.contest.amc12", 4,
            f"An arithmetic sequence starts at {a} with common difference {d}. What is the sum of the first {n} terms?",
            correct,
            [(n * (a + a + n * d) // 2, "That uses n terms after the first, one too many."),
             (a + (n - 1) * d, "That is the nth term, not the sum."),
             (n * a, "That ignores the common difference.")],
            ["Sum = n/2 × (first + last).", f"The last term is {a + (n - 1) * d}."],
            [f"{n}/2 × ({a} + {a + (n - 1) * d}) = {correct}."],
            rng,
        )
    if kind == "trig":
        angle, value = rng.choice([(0, 0), (30, "1/2"), (45, "√2/2"), (60, "√3/2"), (90, 1)])
        return make(
            "gen.contest.amc12", 3,
            f"What is sin({angle}°)?",
            value,
            [("√3/2", "That is sin(60°).") if angle != 60 else ("1/2", "That is sin(30°)."),
             ("0", "That is sin(0°).") if angle != 0 else ("1", "That is sin(90°)."),
             ("1", "That is sin(90°).") if angle != 90 else ("0", "That is sin(0°).")],
            ["Use the unit circle or the special triangles.", "Sine is the y-coordinate."],
            [f"sin({angle}°) = {value}."],
            rng,
        )
    a, b = rng.randint(1, 15), rng.randint(1, 15)
    return make(
        "gen.contest.amc12", 4,
        f"What is the modulus of the complex number {a} + {b}i?",
        fmt_num(math.sqrt(a * a + b * b)) if math.isqrt(a * a + b * b) ** 2 == a * a + b * b else f"√{a * a + b * b}",
        [(f"{a + b}", "That adds the parts instead of squaring."),
         (f"√{a + b}", "That puts the sum under the root."),
         (f"{a * a + b * b}", "That is the squared modulus.")],
        ["The modulus is √(a² + b²).", f"{a}² + {b}² = {a * a + b * b}."],
        [f"|{a} + {b}i| = √{a * a + b * b}."],
        rng,
    )


def aime(rng):
    kind = rng.choice(["divisors", "mod", "inclusion", "trailing"])
    if kind == "divisors":
        p, q = rng.sample([2, 3, 5, 7, 11], 2)
        a, b = rng.randint(1, 6), rng.randint(1, 5)
        n = p ** a * q ** b
        correct = (a + 1) * (b + 1)
        return make(
            "gen.contest.aime", 4,
            f"How many positive divisors does {n} have?",
            correct,
            [(a * b, "That multiplies the exponents instead of adding 1 to each."),
             (a + b, "That adds the exponents."),
             (correct + 1, "That counts one divisor twice.")],
            [f"Write {n} = {p}^{a} × {q}^{b}.", "The divisor count is (a + 1)(b + 1)."],
            [f"({a} + 1)({b} + 1) = {correct}."],
            rng,
        )
    if kind == "mod":
        a = rng.choice([2, 3, 5, 7, 11])
        m = rng.choice([7, 9, 11, 13, 17, 19])
        n = rng.randint(20, 300)
        correct = pow(a, n, m)
        return make(
            "gen.contest.aime", 4,
            f"What is the remainder when {a}^{n} is divided by {m}?",
            correct,
            [(correct + 1, "That is one more than the true remainder."),
             ((correct - 1) % m, "That is one less than the true remainder."),
             (n % m, "That is the exponent's remainder, not the power's.")],
            [f"The powers of {a} repeat modulo {m}.", "Reduce the exponent by the cycle length."],
            [f"{a}^{n} mod {m} = {correct}."],
            rng,
        )
    if kind == "inclusion":
        a = rng.randint(2, 12)
        b = rng.randint(a + 1, 15)
        N = rng.randrange(20, 500, 10)
        correct = N // a + N // b - N // (a * b // math.gcd(a, b))
        return make(
            "gen.contest.aime", 4,
            f"How many integers from 1 to {N} are divisible by {a} or {b}?",
            correct,
            [(N // a + N // b, "That counts the multiples of both twice."),
             (N // a, "That counts only the multiples of the first number."),
             (N // (a * b // math.gcd(a, b)), "That counts only the common multiples.")],
            ["Use inclusion–exclusion.", f"lcm({a}, {b}) = {a * b // math.gcd(a, b)}."],
            [f"{N // a} + {N // b} − {N // (a * b // math.gcd(a, b))} = {correct}."],
            rng,
        )
    n = rng.randint(5, 250)
    p = 5
    correct = 0
    k = p
    while k <= n:
        correct += n // k
        k *= p
    return make(
        "gen.contest.aime", 4,
        f"How many trailing zeros does {n}! have?",
        correct,
        [(correct + 1, "That counts one factor of 5 too many."),
             (n // 10, "That counts only the multiples of 10."),
             (max(1, correct - 1), "That misses one factor of 5.")],
        ["Each trailing zero needs a factor of 10, so count factors of 5.", f"⌊{n}/5⌋ first."],
        [f"⌊{n}/5⌋ + ⌊{n}/25⌋ + … = {correct}."],
        rng,
    )


def usamo(rng):
    kind = rng.choice(["reciprocal", "roots", "absolute", "product"])
    if kind == "reciprocal":
        k = rng.randint(2, 15)
        correct = k * k - 2
        return make(
            "gen.contest.usamo", 4,
            f"If x + 1/x = {k}, what is x² + 1/x²?",
            correct,
            [(k * k, "That squares the sum but forgets the cross term 2."),
             (k * k + 2, "That adds the cross term instead of subtracting it."),
             (k * k - 1, "That subtracts 1 instead of 2.")],
            ["Square both sides.", "(x + 1/x)² = x² + 2 + 1/x²."],
            [f"{k * k} − 2 = {correct}."],
            rng,
        )
    if kind == "roots":
        r = rng.randint(1, 15)
        s = rng.randint(r + 1, 25)
        correct = r * s
        b = -(r + s)
        return make(
            "gen.contest.usamo", 4,
            f"The roots of x² − {r + s}x + {r * s} = 0 are integers. What is their product?",
            correct,
            [(r + s, "That is the sum of the roots."),
             (-(r * s), "That flips the sign of the product."),
             (abs(r - s), "That is the difference of the roots.")],
            ["For x² + bx + c = 0, the product of the roots is c.", f"c = {r * s}."],
            [f"The product is {correct}, with roots {r} and {s}."],
            rng,
        )
    if kind == "absolute":
        a = rng.randint(1, 6)
        b = rng.randint(1, 12)
        c = rng.randint(2, 20)
        lo = Fraction(b - c, a)
        hi = Fraction(b + c, a)
        return make(
            "gen.contest.usamo", 3,
            f"Solve |{a}x − {b}| < {c}.",
            f"{lo} < x < {hi}",
            [(f"x < {hi}", "That keeps only one side of the inequality."),
             (f"x > {lo}", "That keeps only the other side."),
             (f"−{c} < x < {c}", "That ignores the {a}x − {b} inside the absolute value.")],
            [f"Write −{c} < {a}x − {b} < {c}.", f"Add {b} across, then divide by {a}."],
            [f"{lo} < x < {hi}."],
            rng,
        )
    a, b = rng.randint(2, 12), rng.randint(1, 11)
    total = a + b
    correct = a ** 3 + b ** 3
    return make(
        "gen.contest.usamo", 4,
        f"If a + b = {total} and ab = {a * b}, what is a³ + b³?",
        correct,
        [(total ** 3, "That is (a + b)³, ignoring the cross terms."),
             (total ** 3 - 3 * a * b, "That subtracts 3ab instead of 3ab(a + b)."),
             (total ** 2, "That is (a + b)².")],
        ["Use a³ + b³ = (a + b)³ − 3ab(a + b).", f"Substitute {total} and {a * b}."],
        [f"{total ** 3} − 3({a * b})({total}) = {correct}."],
        rng,
    )


def imo(rng):
    kind = rng.choice(["amgm", "crt", "angles", "ineq"])
    if kind == "amgm":
        k = rng.choice([4, 9, 16, 25, 36, 49, 64, 81])
        correct = 2 * math.isqrt(k)
        return make(
            "gen.contest.imo", 4,
            f"For positive x, the minimum of x + {k}/x is…",
            correct,
            [(math.isqrt(k), "That is x at the minimum, not the minimum value."),
             (k, "That is the constant term."),
             (2 * k, "That doubles the constant instead of its root.")],
            ["Apply AM-GM to the two terms.", f"The product of the terms is {k}."],
            [f"Minimum = 2√{k} = {correct}, at x = {math.isqrt(k)}."],
            rng,
        )
    if kind == "crt":
        m1, m2 = rng.choice([(3, 5), (4, 7), (5, 7), (3, 7), (4, 9), (5, 9), (7, 11), (8, 11)])
        for x in range(1, m1 * m2 + 1):
            if x % m1 == 1 and x % m2 == 2:
                correct = x
                break
        else:
            return None
        return make(
            "gen.contest.imo", 4,
            f"What is the smallest positive integer x with x ≡ 1 (mod {m1}) and x ≡ 2 (mod {m2})?",
            correct,
            [(m1 + 1, "That satisfies the first congruence only."),
             (m2 + 2, "That satisfies the second congruence only."),
             (correct + m1 * m2, "That is a solution, but not the smallest.")],
            [f"List the numbers ≡ 1 (mod {m1}).", "Check each against the second congruence."],
            [f"x = {correct}."],
            rng,
        )
    if kind == "angles":
        apex = rng.randrange(10, 161, 5)
        base = (180 - apex) // 2
        return make(
            "gen.contest.imo", 3,
            f"In triangle ABC, AB = AC and angle A = {apex}°. What is angle B?",
            f"{base}°",
            [(f"{apex}°", "The base angles equal each other, not the apex."),
             (f"{180 - apex}°", "That is the sum of the two base angles."),
             (f"{base + 10}°", "That would make the angles sum past 180°.")],
            ["An isosceles triangle has equal base angles.", f"180 − {apex} = {180 - apex}°."],
            [f"{180 - apex} ÷ 2 = {base}°."],
            rng,
        )
    a = rng.randint(2, 20)
    b = rng.randint(a + 1, 25)
    return make(
        "gen.contest.imo", 4,
        f"Which is larger: {b}/{a} or {a}/{b} (with a, b > 0)?",
        f"{b}/{a}",
        [(f"{a}/{b}", "That is the reciprocal, which is smaller when b > a."),
         ("They are equal", "They are only equal when a = b."),
         ("It depends on the values", "With both positive and b > a, the order is fixed.")],
        ["Compare the fractions by cross-multiplying.", f"{b} × {b} = {b * b} and {a} × {a} = {a * a}."],
        [f"Since {b * b} > {a * a}, {b}/{a} is larger."],
        rng,
    )


# --------------------------------------------------------------------------- #
# Coding: Python, C++, Java output
# --------------------------------------------------------------------------- #


def code_python(rng):
    kind = rng.choice(["sum", "slice", "div", "len", "str", "dict", "append"])
    if kind == "sum":
        n = rng.randint(4, 40)
        correct = n * (n + 1) // 2
        return make(
            "gen.code.python", 2,
            f"What does this print?\n\ntotal = 0\nfor i in range(1, {n + 1}):\n    total += i\nprint(total)",
            correct,
            [(n * (n - 1) // 2, "That misses the last value, because range stops before the end."),
             (n, "That is the number of passes, not the sum."),
             (n + 1, "That is the last value only.")],
            ["range(1, n+1) includes n.", "The loop adds 1 + 2 + … + n."],
            [f"1 + … + {n} = {correct}."],
            rng,
        )
    if kind == "slice":
        word = rng.choice(["python", "coding", "veeLearn", "science", "algorithm", "function", "variable", "compiler"])
        i = rng.randint(1, len(word) - 3)
        j = i + rng.randint(2, 3)
        correct = word[i:j]
        return make(
            "gen.code.python", 2,
            f"What does this print?\n\nword = '{word}'\nprint(word[{i}:{j}])",
            f"'{correct}'",
            [(f"'{word[i:j + 1]}'", "A slice excludes the end index, so j is not included."),
             (f"'{word[i - 1:j]}'", "Strings are 0-indexed, so i is the first character kept."),
             (f"'{word[j:i]}'", "A backwards slice is empty here, not reversed.")],
            ["The start index is included.", "The stop index is excluded."],
            [f"word[{i}:{j}] = '{correct}'."],
            rng,
        )
    if kind == "div":
        a, b = rng.randint(7, 200), rng.randint(2, 12)
        quotient = a // b
        exact = abs(a / b - quotient) < 1e-9
        return make(
            "gen.code.python", 2,
            f"What does this print?\n\nprint({a} // {b})",
            quotient,
            [(f"{a / b:g}", "That is true division with /, not floor division with //."),
             (f"{quotient + 1}", "That rounds up; // rounds down."),
             (f"{a % b}", "That is the remainder, not the quotient.")],
            ["// is floor division.", f"{a} ÷ {b} is about {a / b:g}."],
            [f"{a} // {b} = {quotient}."],
            rng,
        )
    if kind == "len":
        items = rng.randint(3, 30)
        return make(
            "gen.code.python", 1,
            f"What does this print?\n\nnums = list(range({items}))\nprint(len(nums))",
            items,
            [(items - 1, "range stops before its argument, but len counts the items it produced."),
             (items + 1, "That counts one item too many."),
             (0, "The list is not empty.")],
            [f"range({items}) gives 0 to {items - 1}.", "len counts the elements."],
            [f"len is {items}."],
            rng,
        )
    if kind == "str":
        word = rng.choice(["ha", "go", "be", "la", "py", "ok", "na", "do"])
        n = rng.randint(2, 6)
        correct = word * n
        return make(
            "gen.code.python", 2,
            f"What does this print?\n\nprint('{word}' * {n})",
            f"'{correct}'",
            [(f"'{word}'", "That ignores the multiplier."),
             (f"'{word * (n + 1)}'", "That repeats the word once too often."),
             (f"'{n}{word}'", "That prints the number and the word together.")],
            ["Multiplying a string repeats it.", f"The word is repeated {n} times."],
            [f"'{correct}'."],
            rng,
        )
    if kind == "dict":
        key = rng.choice(["a", "b", "c"])
        return make(
            "gen.code.python", 3,
            "What does this print?\n\nd = {'key': 0}\nprint(d.get('missing', 7))",
            "7",
            [("None", "The second argument to get() is the default, so it is not None."),
             ("0", "That is the value that exists, but the key asked for is missing."),
             ("KeyError", "get() never raises for a missing key.")],
            ["dict.get(key, default) returns the default when the key is absent.", "The default here is 7."],
            ["The key 'missing' is absent, so print 7."],
            rng,
        )
    items = rng.randint(2, 20)
    return make(
        "gen.code.python", 2,
        f"What does this print?\n\nnums = []\nfor i in range({items}):\n    nums.append(i * 2)\nprint(nums[-1])",
        (items - 1) * 2,
        [(items * 2, "The last value is (n − 1) × 2, not n × 2."),
         (items - 1, "That is the last index, not the value stored there."),
         (2, "That is the first doubled value.")],
        [f"The loop runs for i = 0 to {items - 1}.", "nums[-1] is the last element."],
        [f"The last element is {(items - 1) * 2}."],
        rng,
    )


def code_cpp(rng):
    kind = rng.choice(["div", "mod", "loop", "arr", "increment"])
    if kind == "div":
        a, b = rng.randint(5, 200), rng.randint(2, 15)
        return make(
            "gen.code.cpp", 2,
            f"What does this print?\n\nint a = {a}, b = {b};\ncout << a / b;",
            a // b,
            [(f"{a / b:g}", "int division truncates, so there is no decimal part."),
             (a // b + 1, "Integer division truncates toward zero; it does not round up."),
             (a % b, "That is the remainder.")],
            ["Both operands are int, so / is integer division.", f"{a} ÷ {b} truncates to {a // b}."],
            [f"{a} / {b} = {a // b} in C++."],
            rng,
        )
    if kind == "mod":
        a, b = rng.randint(10, 500), rng.randint(3, 17)
        return make(
            "gen.code.cpp", 2,
            f"What does this print?\n\nint a = {a}, b = {b};\ncout << a % b;",
            a % b,
            [(a // b, "That is the quotient, not the remainder."),
             (a % b + b, "That adds a full divisor to the remainder."),
             (b, "That is the divisor.")],
            ["% is the remainder operator.", f"{a} = {b} × {a // b} + {a % b}."],
            [f"{a} % {b} = {a % b}."],
            rng,
        )
    n = rng.randint(3, 25)
    limit = n + rng.randint(0, 1)
    correct = sum(range(n))
    return make(
        "gen.code.cpp", 2,
        f"What does this print?\n\nint total = 0;\nfor (int i = 0; i < {limit}; i++) total += i;\ncout << total;",
        correct if limit == n else sum(range(limit)),
        [(sum(range(limit + 1)), "That runs one pass too many."),
         (limit, "That is the number of passes, not the sum."),
         (sum(range(limit)) - limit, "That misses the last value added.")],
        ["Trace i from 0 up to the loop bound.", f"The loop runs while i < {limit}."],
        [f"The sum is {sum(range(limit))}."],
        rng,
    )
    if kind == "arr":
        size = rng.randint(3, 12)
        return make(
            "gen.code.cpp", 3,
            f"What does this print?\n\nint arr[{size}] = {{ {', '.join(str(i * i) for i in range(size))} }};\ncout << arr[{size - 1}];",
            (size - 1) * (size - 1),
            [(size * size, "That is the value one index past the end."),
             (size - 1, "That is the index, not the value."),
             (0, "That is the first element.")],
            ["Arrays are 0-indexed.", f"The last valid index is {size - 1}."],
            [f"arr[{size - 1}] = {(size - 1) ** 2}."],
            rng,
        )
    start = rng.randint(2, 50)
    return make(
        "gen.code.cpp", 3,
        f"What does this print?\n\nint x = {start};\ncout << x++ << ' ' << x;",
        f"{start} {start + 1}",
        [(f"{start + 1} {start + 1}", "Post-increment prints the old value first."),
         (f"{start + 1} {start}", "That is pre-increment order."),
         (f"{start} {start}", "x does change after the increment.")],
        ["x++ returns the old value, then increments.", "The second output sees the new value."],
        [f"It prints {start} then {start + 1}."],
        rng,
    )


def code_java(rng):
    kind = rng.choice(["div", "concat", "loop", "length", "mod"])
    if kind == "div":
        a, b = rng.randint(5, 200), rng.randint(2, 15)
        return make(
            "gen.code.java", 2,
            f"What does this print?\n\nint a = {a}, b = {b};\nSystem.out.println(a / b);",
            a // b,
            [(f"{a / b:g}", "int division truncates in Java too."),
             (a // b + 1, "It truncates; it does not round up."),
             (a % b, "That is the remainder.")],
            ["Both operands are int, so / is integer division.", f"{a} ÷ {b} truncates to {a // b}."],
            [f"It prints {a // b}."],
            rng,
        )
    if kind == "concat":
        variant = rng.choice(["str_first", "int_first"])
        a, b = rng.randint(1, 9), rng.randint(1, 9)
        if variant == "str_first":
            correct = f"{a}{b}"
            expr = f"\"\" + {a} + {b}"
            wrong1 = str(a + b)
            why1 = "The empty string makes the first + concatenate, so the second is text too."
        else:
            correct = str(a + b)
            expr = f"{a} + {b} + \"\""
            wrong1 = f"{a}{b}"
            why1 = "The numbers are added first, before the string joins in."
        return make(
            "gen.code.java", 3,
            f"What does this print?\n\nSystem.out.println({expr});",
            f"\"{correct}\"",
            [(f"\"{wrong1}\"", why1),
             (f"{a + b + 10}", "That adds 10 for no reason."),
             ("A compile error", "String concatenation with int is allowed in Java.")],
            ["Java evaluates left to right.", "Once one operand is a String, + concatenates."],
            [f"It prints \"{correct}\"."],
            rng,
        )
    n = rng.randint(3, 25)
    return make(
        "gen.code.java", 2,
        f"What does this print?\n\nint total = 0;\nfor (int i = 1; i <= {n}; i++) {{ total += i; }}\nSystem.out.println(total);",
        n * (n + 1) // 2,
        [(n * (n - 1) // 2, "The loop uses <=, so the last value is included."),
         (n, "That is the number of passes."),
         (n + 1, "That is the last value only.")],
        [f"The loop runs i = 1 to {n}.", "Sum = n(n + 1)/2."],
        [f"{n} × {n + 1} ÷ 2 = {n * (n + 1) // 2}."],
        rng,
    )
    if kind == "length":
        word = rng.choice(["java", "coder", "class", "array", "object", "method", "string", "loop"])
        return make(
            "gen.code.java", 1,
            f"What does this print?\n\nString s = \"{word}\";\nSystem.out.println(s.length());",
            len(word),
            [(len(word) - 1, "length() counts characters, and there is no terminator to subtract."),
             (len(word) + 1, "That adds a character that is not there."),
             (0, "The string is not empty.")],
            ["length() returns the number of characters.", f"Count the letters in \"{word}\"."],
            [f"It prints {len(word)}."],
            rng,
        )
    a, b = rng.randint(10, 500), rng.randint(3, 17)
    return make(
        "gen.code.java", 2,
        f"What does this print?\n\nint a = {a}, b = {b};\nSystem.out.println(a % b);",
        a % b,
        [(a // b, "That is the quotient."),
         (a % b + b, "That adds a whole divisor to the remainder."),
         (b, "That is the divisor.")],
        ["% gives the remainder.", f"{a} = {b} × {a // b} + {a % b}."],
        [f"It prints {a % b}."],
        rng,
    )


# --------------------------------------------------------------------------- #
# SAT / ACT English: fixed templates with a clear right answer
# --------------------------------------------------------------------------- #

GRAMMAR_TEMPLATES = [
    # (stem, correct, [(wrong, why) x3], explanation)
    ("The box of old photographs ___ on the top shelf.",
     "sits",
     [("sit", "The subject is 'box' (singular), not 'photographs'."),
      ("were sitting", "The verb must agree with the singular subject 'box'."),
      ("sit themselves", "The sentence needs a singular verb and no reflexive pronoun.")],
     "The subject is 'box', so the verb is singular: sits."),
    ("Each of the students ___ a locker.",
     "has",
     [("have", "'Each' is singular, so it takes 'has'."),
      ("are having", "The subject is singular, so the verb is 'has'."),
      ("have had", "'Each' takes a singular verb.")],
     "'Each' is singular: each … has."),
    ("The report, along with its appendices, ___ due on Friday.",
     "is",
     [("are", "The subject is 'report'; 'along with its appendices' does not change it."),
      ("were", "The sentence is about the present deadline."),
      ("have been", "The subject is singular.")],
     "The subject is 'report', so the verb is 'is'."),
    ("Neither the manager nor the employees ___ informed yet.",
     "were",
     [("was", "With 'neither … nor', the verb agrees with the nearer subject, 'employees'."),
      ("is", "'Employees' is plural, so the verb is plural."),
      ("has been", "The nearer subject is plural.")],
     "With neither/nor the verb agrees with the nearer subject, 'employees'."),
    ("If she ___ harder, she would have passed the exam.",
     "had studied",
     [("studied", "The result is 'would have passed', so the condition is past perfect."),
      ("would study", "'Would' does not belong in the if-clause."),
      ("studies", "That is present tense, which cannot pair with 'would have passed'.")],
     "A past unreal condition takes 'had studied'."),
    ("By the time the film started, we ___ for an hour.",
     "had waited",
     [("have waited", "The waiting finished before a past event, so it is past perfect."),
      ("wait", "That is present tense and does not mark the earlier action."),
      ("were waiting", "That suggests the waiting was interrupted, not completed.")],
     "Use past perfect for the action completed before another past action."),
    ("The team ___ its uniforms before every game.",
     "washes",
     [("wash", "'Team' is treated as one unit here, so the verb is singular."),
      ("are washing", "The sentence describes a routine, not a current action."),
      ("washing", "The sentence needs a finite verb.")],
     "'The team' as a unit takes a singular verb: washes."),
    ("Everyone who signed up ___ to bring a pencil.",
     "needs",
     [("need", "'Everyone' is singular."),
      ("are needing", "State verbs like 'need' are not used in the continuous form here."),
      ("have needed", "The sentence talks about a present requirement.")],
     "'Everyone' is singular: everyone … needs."),
    ("The novel, which ___ three awards, was written in a single year.",
     "won",
     [("win", "The novel won in the past, and the clause needs a past verb."),
      ("has won", "That would need a present perfect frame; the main clause is past."),
      ("winning", "A relative clause needs a finite verb.")],
     "The relative clause describes a past event: won."),
    ("Hiking through the canyon, ___.",
     "Maya saw three condors",
     [("three condors were seen by Maya", "The opening phrase must describe Maya, the hiker."),
      ("the heat was unbearable", "The heat was not hiking through the canyon."),
      ("it was a long day", "The modifier needs a subject who was hiking.")],
     "The introductory phrase modifies Maya, so Maya must be the subject."),
    ("Which sentence is punctuated correctly?",
     "We packed water, snacks, and a map.",
     [("We packed water snacks, and a map.", "Items in a series need commas between them."),
      ("We packed water, snacks and, a map.", "The comma before 'and' is misplaced."),
      ("We packed, water snacks and a map.", "That comma separates the verb from its objects.")],
     "Items in a series are separated by commas."),
    ("Which sentence avoids a comma splice?",
     "The lab was closed, so we met in the library.",
     [("The lab was closed, we met in the library.", "Two independent clauses joined by only a comma is a splice."),
      ("The lab was closed we met in the library.", "Two independent clauses need a conjunction or punctuation."),
      ("The lab was closed; and we met in the library.", "A semicolon and a conjunction are used together here.")],
     "Join two independent clauses with a comma and a conjunction."),
    ("Each of the runners ___ her own water bottle.",
     "carries",
     [("carry", "'Each' is singular, so the verb is 'carries'."),
      ("are carrying", "The subject is singular, and this is a general statement."),
      ("carrying", "The sentence needs a finite verb.")],
     "'Each' is singular: carries."),
    ("The data ___ collected over six months.",
     "were",
     [("was", "'Data' is plural in this construction."),
      ("is being", "The collection finished in the past."),
      ("has", "The plural subject needs a plural verb.")],
     "'Data' takes a plural verb here: were collected."),
    ("Neither of the answers ___ correct.",
     "is",
     [("are", "'Neither' is singular."),
      ("were", "The statement is about the present."),
      ("be", "The sentence needs a finite verb.")],
     "'Neither' is singular: neither … is."),
]

ACT_ENGLISH_EXTRA = [
    ("The museum's new wing, ___ opened last spring, features local artists.",
     "which",
     [("that", "A non-essential clause takes 'which', not 'that'."),
      ("who", "'Who' refers to people, not a wing."),
      ("what", "'What' cannot introduce this relative clause.")],
     "A non-essential clause is introduced by 'which'."),
    ("She finished the experiment, ___ she wrote up the results.",
     "then",
     [("than", "'Than' is for comparisons."),
      ("them", "'Them' is a pronoun, not a connector."),
      ("their", "'Their' is possessive.")],
     "The sentence needs the time connector 'then'."),
    ("The students ___ projects were chosen presented first.",
     "whose",
     [("who's", "'Who's' means 'who is'."),
      ("which", "'Which' cannot show possession for people here."),
      ("whom", "'Whom' is an object pronoun, not possessive.")],
     "Possession for people takes 'whose'."),
    ("The lab is cleaned ___ every experiment.",
     "after",
     [("afterwards", "'Afterwards' is an adverb and cannot take an object."),
      ("afterward", "The same problem: it cannot be followed by 'every experiment'."),
      ("after the fact of", "That is wordy and ungrammatical here.")],
     "'After' can take the noun phrase 'every experiment'."),
]


SING_THINGS = ["box", "crate", "list", "bundle", "stack", "basket", "folder", "carton", "envelope", "tray"]
PLURALS = ["photos", "tools", "letters", "samples", "tickets", "coins", "files", "notebooks", "badges", "maps"]
ACT_SING_THINGS = ["jar", "drawer", "shelf", "packet", "barrel", "suitcase", "container", "album"]
ACT_PLURALS = ["receipts", "marbles", "candles", "buttons", "postcards", "seeds", "clips", "labels"]
SERIES = ["water", "snacks", "a map", "tape", "gloves", "a compass", "rope", "a whistle", "batteries", "sunscreen"]
BELONGINGS = ["notebook", "badge", "lunch", "calculator", "pencil case", "permission slip"]
EVENTS = ["film", "meeting", "concert", "lecture", "game", "play"]


def grammar(rng, skill):
    """Agreement, punctuation and tense items built from a small grammar model.

    The subject and the verb are chosen together, so varying the nouns varies the
    sentence without ever producing a sentence with two possible answers.
    """
    act = skill == "gen.act.english"
    kinds = ["agreement", "plural_subject", "each", "along", "neither", "pronoun", "tense"]
    if not act:
        kinds.append("punct")
    kind = rng.choice(kinds)
    single = rng.choice(ACT_SING_THINGS if act else SING_THINGS)
    plural = rng.choice(ACT_PLURALS if act else PLURALS)
    tier = 3 if skill == "gen.sat.rw.grammar" else 2
    # ACT English is passage based, so its prompt names the task; the wording also
    # keeps these stems distinct from the SAT ones (qbank_items.stem_hash is unique).
    lead = "Read the sentence and choose the word or phrase that belongs in the blank.\n\n" if act else ""
    hints = ["Find the real subject, ignoring phrases that come between it and the verb.",
             "Read the whole sentence before you choose; the error is usually near the blank."]

    if kind == "agreement":
        return make(
            skill, tier,
            lead + f"The {single} of {plural} ___ on the shelf.",
            "is",
            [("are", f"The subject is '{single}' (singular); '{plural}' sits in a prepositional phrase."),
             ("were", "The sentence is present tense, and the subject is singular."),
             ("have", "A singular subject takes 'has', not 'have'.")],
            hints,
            [f"The subject is '{single}', so the verb is 'is'."],
            rng,
        )
    if kind == "plural_subject":
        return make(
            skill, tier,
            lead + f"{plural[0].upper() + plural[1:]} ___ to the library every Saturday.",
            "go",
            [("goes", f"'{plural}' is plural, so the verb does not take -s."),
             ("is going", "The subject is plural, so the verb would be 'are going'."),
             ("gone", "The sentence needs a present-tense finite verb.")],
            hints,
            [f"'{plural}' is plural, so use 'go'."],
            rng,
        )
    if kind == "each":
        item = rng.choice(BELONGINGS)
        return make(
            skill, tier,
            lead + f"Each of the {plural} ___ a {item}.",
            "has",
            [("have", "'Each' is singular, so it takes 'has'."),
             ("are having", "'Each' is singular, and this is a general statement."),
             ("have had", "'Each' takes a singular verb.")],
            hints,
            ["'Each' is singular: each … has."],
            rng,
        )
    if kind == "along":
        return make(
            skill, tier,
            lead + f"The {single}, along with the {plural}, ___ ready for the trip.",
            "is",
            [("are", f"'Along with the {plural}' does not change the subject '{single}'."),
             ("were", "The sentence is about the present, and the subject is singular."),
             ("have been", "The subject is singular, so the verb is 'is'.")],
            hints,
            [f"The subject is '{single}', so the verb is 'is'."],
            rng,
        )
    if kind == "neither":
        other = rng.choice(SING_THINGS)
        return make(
            skill, tier,
            lead + f"Neither the {other} nor the {plural} ___ in the cupboard.",
            "are",
            [("is", "With 'neither … nor', the verb agrees with the nearer subject, which is plural here."),
             ("was", f"'{plural}' is plural, so the verb is 'are'."),
             ("has been", "The nearer subject is plural, so the verb is plural.")],
            hints,
            [f"With neither/nor the verb agrees with the nearer subject, '{plural}'."],
            rng,
        )
    if kind == "punct":
        a, b, c = rng.sample(SERIES, 3)
        return make(
            "gen.sat.rw.grammar", 3,
            "Which sentence is punctuated correctly?",
            f"We packed {a}, {b}, and {c}.",
            [(f"We packed {a} {b}, and {c}.", "Items in a series need commas between all of them."),
             (f"We packed {a}, {b} and, {c}.", "The comma before 'and' is misplaced."),
             (f"We packed, {a} {b} and {c}.", "That comma separates the verb from its objects.")],
            hints,
            ["Items in a series are separated by commas, and the last comma comes before 'and'."],
            rng,
        )
    if kind == "pronoun":
        item = rng.choice(BELONGINGS)
        whose = rng.choice(["her", "his"])
        return make(
            skill, tier,
            lead + f"Each of the {plural} brought ___ own {item}.",
            whose,
            [("their", "'Each' is singular, so the pronoun is singular."),
             ("they're", "'They're' means 'they are', not a possessive."),
             ("there", "'There' is a place word, not a possessive.")],
            hints,
            [f"'Each' is singular, so the possessive is '{whose}'."],
            rng,
        )
    event = rng.choice(EVENTS)
    return make(
        skill, tier,
        lead + f"By the time we arrived, the {event} ___.",
        "had started",
        [("has started", "The arriving is past, so the earlier action needs past perfect."),
         ("starts", "Present tense cannot describe an action before a past event."),
         ("starting", "The sentence needs a finite verb.")],
        hints,
        ["Use past perfect for the action finished before another past action."],
        rng,
    )


def grammar_sat(rng):
    return grammar(rng, "gen.sat.rw.grammar")


def grammar_act(rng):
    return grammar(rng, "gen.act.english")


# --------------------------------------------------------------------------- #
# Runner
# --------------------------------------------------------------------------- #

COUNTS = {
    "gen.k5.arith": 2500,
    "gen.k5.fractions": 1500,
    "gen.mid.percent": 1500,
    "gen.mid.ratio": 1200,
    "gen.geometry.mensuration": 1500,
    "gen.probability.basic": 600,
    "gen.algebra.linear": 2000,
    "gen.sat.math": 1500,
    "gen.act.math": 1200,
    "gen.contest.amc8": 1200,
    "gen.contest.amc10": 900,
    "gen.contest.amc12": 700,
    "gen.contest.aime": 500,
    "gen.contest.usamo": 300,
    "gen.contest.imo": 250,
    "gen.code.python": 1200,
    "gen.code.cpp": 800,
    "gen.code.java": 800,
    "gen.sat.rw.grammar": 600,
    "gen.act.english": 400,
}

FAMILIES = {
    "gen.k5.arith": arith,
    "gen.k5.fractions": fractions,
    "gen.mid.percent": percent,
    "gen.mid.ratio": ratio,
    "gen.geometry.mensuration": geometry,
    "gen.probability.basic": probability,
    "gen.algebra.linear": algebra,
    "gen.sat.math": sat_math,
    "gen.act.math": act_math,
    "gen.contest.amc8": amc8,
    "gen.contest.amc10": amc10,
    "gen.contest.amc12": amc12,
    "gen.contest.aime": aime,
    "gen.contest.usamo": usamo,
    "gen.contest.imo": imo,
    "gen.code.python": code_python,
    "gen.code.cpp": code_cpp,
    "gen.code.java": code_java,
    "gen.sat.rw.grammar": grammar_sat,
    "gen.act.english": grammar_act,
}


def build_generated(seed=20261117):
    """Yield items for every family, up to its target count (deduped by stem)."""
    rng = random.Random(seed)
    seen = set()
    out = []
    for skill, target in COUNTS.items():
        family = FAMILIES[skill]
        made = 0
        attempts = 0
        limits = attempts_limit = target * 12
        while made < target and attempts < limits:
            attempts += 1
            item = family(rng)
            if item is None:
                continue
            if item["skill"] != skill and skill in ("gen.sat.rw.grammar", "gen.act.english"):
                # `grammar` chooses its own skill; only count the ones that match.
                continue
            key = f"{item['skill']}|{' '.join(item['stem'].lower().split())}"
            if key in seen:
                continue
            seen.add(key)
            out.append(item)
            made += 1
    return out
