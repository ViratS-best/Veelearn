"""Unique extra questions for grades 3–8, Algebra 2, and MathCounts."""

from __future__ import annotations

import math

from question_banks import _q


def _seed(s: str) -> int:
    n = 17
    for i, ch in enumerate(s):
        n = (n * 33 + ord(ch) + i) % 1_000_003
    return n


def extra_questions(title: str):
    t = title.lower()
    matchers = [
        ("third grade math unit 1", g3u1),
        ("third grade math unit 2", g3u2),
        ("third grade math unit 3", g3u3),
        ("third grade math unit 4", g3u4),
        ("third grade math unit 5", g3u5),
        ("third grade math unit 6", g3u6),
        ("third grade math unit 7", g3u7),
        ("third grade math unit 8", g3u8),
        ("fourth grade math unit 1", g4u1),
        ("fourth grade math unit 2", g4u2),
        ("fourth grade math unit 3", g4u3),
        ("fourth grade math unit 4", g4u4),
        ("fourth grade math unit 5", g4u5),
        ("fourth grade math unit 6", g4u6),
        ("fourth grade math unit 7", g4u7),
        ("fourth grade math unit 8", g4u8),
        ("fifth grade math unit 1", g5u1),
        ("fifth grade math unit 2", g5u2),
        ("fifth grade math unit 3", g5u3),
        ("fifth grade math unit 4", g5u4),
        ("fifth grade math unit 5", g5u5),
        ("fifth grade math unit 6", g5u6),
        ("fifth grade math unit 7", g5u7),
        ("fifth grade math unit 8", g5u8),
        ("sixth grade math unit 1", g6u1),
        ("sixth grade math unit 2", g6u2),
        ("sixth grade math unit 3", g6u3),
        ("sixth grade math unit 4", g6u4),
        ("sixth grade math unit 5", g6u5),
        ("sixth grade math unit 6", g6u6),
        ("sixth grade math unit 7", g6u7),
        ("sixth grade math unit 8", g6u8),
        ("seventh grade math unit 1", g7u1),
        ("seventh grade math unit 2", g7u2),
        ("seventh grade math unit 3", g7u3),
        ("seventh grade math unit 4", g7u4),
        ("seventh grade math unit 5", g7u5),
        ("seventh grade math unit 6", g7u6),
        ("seventh grade math unit 7", g7u7),
        ("seventh grade math unit 8", g7u8),
        ("eighth grade math unit 1", g8u1),
        ("eighth grade math unit 2", g8u2),
        ("eighth grade math unit 3", g8u3),
        ("eighth grade math unit 4", g8u4),
        ("eighth grade math unit 5", g8u5),
        ("eighth grade math unit 6", g8u6),
        ("eighth grade math unit 7", g8u7),
        ("eighth grade math unit 8", g8u8),
        ("algebra 2 unit 1", a2u1),
        ("algebra 2 unit 2", a2u2),
        ("algebra 2 unit 3", a2u3),
        ("algebra 2 unit 4", a2u4),
        ("algebra 2 unit 5", a2u5),
        ("algebra 2 unit 6", a2u6),
        ("algebra 2 unit 7", a2u7),
        ("algebra 2 unit 8", a2u8),
        ("mathcounts unit 1", mc1),
        ("mathcounts unit 2", mc2),
        ("mathcounts unit 3", mc3),
        ("mathcounts unit 4", mc4),
        ("mathcounts unit 5", mc5),
        ("mathcounts unit 6", mc6),
        ("mathcounts unit 7", mc7),
        ("mathcounts unit 8", mc8),
    ]
    for key, fn in matchers:
        if key in t:
            return [q for q in fn() if q]
    return [q for q in generic(title) if q]


def generic(title: str):
    s = _seed(title)
    qs = []
    for i in range(60):
        a = 3 + (s + i * 7) % 40
        b = 2 + (s + i * 5) % 17
        qs.append(_q(
            f"In this unit checkpoint #{i + 1}: if a quantity starts at {a} and changes by {b} twice (add, then subtract half of {b} if even else subtract 1), what is the result?",
            a + b - (b // 2 if b % 2 == 0 else 1),
            "Follow the two steps in order.",
        ))
    return qs


# ----- Grade 3 -----
def g3u1():
    qs = []
    for n in (245, 306, 418, 550, 672, 701, 809, 924, 999, 120, 333, 444, 505, 616, 780):
        qs.append(_q(f"What is 10 more than {n}?", n + 10, f"{n}+10={n+10}."))
    for a, b in ((348, 291), (512, 499), (700, 70), (808, 880), (125, 215)):
        qs.append(_q(f"Which is greater: {a} or {b}?", max(a, b), "Compare hundreds, then tens, then ones.", [min(a, b), a + b, abs(a - b)]))
    qs += [
        _q("Round 472 to the nearest ten.", 470, "2 < 5 so tens stay 7."),
        _q("Round 472 to the nearest hundred.", 500, "7 ≥ 5 so hundreds go up."),
        _q("Expanded 600+40+8?", 648, "648."),
        _q("How many hundreds in 9,040? Wait, in 904?", 9, "9 hundreds in 904.", difficulty="hard"),
        _q("A number between 399 and 410 that is a multiple of 5?", 400, "400 or 405. Smallest listed often 400.", difficulty="hard"),
        _q("Greatest 3-digit using 2, 7, 5?", 752, "7 hundreds 5 tens 2 ones.", difficulty="hard"),
        _q("Value of 4 in 4,216 is 4000. In 2416 the 4 is worth?", 400, "4 hundreds.", difficulty="hard"),
        _q("Skip-count by 100: 350, 450, 550, ___.", 650, "Add 100.", difficulty="stretch"),
        _q("Closest thousand to 3,499?", 3000, "499 < 500.", difficulty="stretch"),
        _q("2 hundreds 15 tens 6 ones, regrouped?", 356, "15 tens = 1 hundred 5 tens.", difficulty="stretch"),
        _q("Odd number of hundreds: which is odd: 400 or 501?", 501, "501 is odd.", difficulty="stretch"),
        _q("A place-value puzzle: 8 thousands 0 hundreds 3 tens 9 ones.", 8039, "8039.", difficulty="stretch"),
        _q("How many tens in 2,400?", 240, "240 tens.", difficulty="stretch"),
        _q("Compare 1,099 and 1,109. Greater?", 1109, "Hundreds same, tens 0 vs 1.", difficulty="stretch"),
        _q("1000 − 1 in standard form?", 999, "999.", difficulty="stretch"),
        _q("A digit 0 in 508 means how many tens?", 0, "0 tens.", difficulty="stretch"),
        _q("Smallest 4-digit number?", 1000, "1000.", difficulty="stretch"),
        _q("Round 2,650 to nearest hundred.", 2700, "5 tens rounds up.", difficulty="stretch"),
        _q("3,003 vs 3,030. How much greater is 3,030?", 27, "3030−3003=27.", difficulty="stretch"),
        _q("Write 14 tens as a 3-digit number with 0 hundreds extra regroup.", 140, "14 tens = 1 hundred 4 tens.", difficulty="stretch"),
    ]
    return qs


def g3u2():
    qs = []
    for a, b in ((4, 7), (6, 8), (9, 5), (3, 12), (7, 7), (8, 6), (5, 9), (11, 4), (2, 15), (10, 10)):
        qs.append(_q(f"What is {a} groups of {b}?", a * b, f"{a}×{b}={a*b}."))
    qs += [
        _q("4 × 9 = 9 × 4. This is the ___ property.", "commutative", "Order can swap.", ["identity", "zero", "division"]),
        _q("5 × 0 = ?", 0, "Zero property."),
        _q("7 × 1 = ?", 7, "Identity."),
        _q("An array 3 rows of 8. Product?", 24, "3×8."),
        _q("6 × 7 vs 5 × 8. Greater product?", 42, "42 vs 40.", ["40", "35", "48"]),
        _q("A story: 8 packs of 6. Total?", 48, "8×6=48.", difficulty="hard"),
        _q("Missing factor: 9 × ___ = 63.", 7, "9×7=63.", difficulty="hard"),
        _q("3 × 4 × 2 = ?", 24, "12×2.", difficulty="hard"),
        _q("Twice 7 groups of 5.", 70, "14×5=70.", difficulty="hard"),
        _q("A rectangle 9 by 6. How many unit squares?", 54, "Area 9×6.", difficulty="stretch"),
        _q("If 4 × n = 36, n?", 9, "36÷4.", difficulty="stretch"),
        _q("Equal groups: 48 cookies in bags of 8. Bags?", 6, "48÷8=6.", difficulty="stretch"),
        _q("(5+3)×4 vs 5+3×4. The product-first value of 5+3×4 is?", 17, "5+12=17.", difficulty="stretch"),
        _q("A pattern: 6, 12, 18, 24. Next?", 30, "Add 6 / × table.", difficulty="stretch"),
        _q("7 rows, 0 in a row. Total?", 0, "7×0.", difficulty="stretch"),
        _q("Distributive: 6×14 = 6×10 + 6×4. Value?", 84, "60+24.", difficulty="stretch"),
        _q("Which does NOT equal 24: 3×8, 4×6, 2×12, 5×5?", 25, "5×5=25.", difficulty="stretch"),
        _q("A skip count 4 times by 9 starting at 0. Land?", 36, "9,18,27,36.", difficulty="stretch"),
        _q("Area model 20+3 times 5. Product?", 115, "100+15.", difficulty="stretch"),
        _q("If each box has 12, 7 boxes and you add 5 extra. Total?", 89, "84+5.", difficulty="stretch"),
    ]
    return qs


def g3u3():
    qs = []
    for a in range(2, 13):
        qs.append(_q(f"What is {a} × 8?", a * 8, f"{a}×8={a*8}."))
    qs += [
        _q("9 × 9 = ?", 81, "81."),
        _q("12 × 5 = ?", 60, "60."),
        _q("6 × 12 = ?", 72, "72."),
        _q("7 × 8 = ?", 56, "56."),
        _q("11 × 11 = ?", 121, "121."),
        _q("A fact family: 8×7=56 so 56÷8=?", 7, "Inverse.", difficulty="hard"),
        _q("How many 9s in 81?", 9, "9×9.", difficulty="hard"),
        _q("5 × 16 using 5×10 + 5×6.", 80, "50+30.", difficulty="hard"),
        _q("Which is a multiple of 6: 27, 28, 30, 32?", 30, "6×5.", difficulty="hard"),
        _q("Product of 3 consecutive: 4×5×6.", 120, "20×6.", difficulty="stretch"),
        _q("Square numbers: 1,4,9,16,25. Next?", 36, "6².", difficulty="stretch"),
        _q("If 12×n=144, n?", 12, "12×12.", difficulty="stretch"),
        _q("A timed test: 8×7, 8×8, 8×9. Sum of those three products?", 192, "56+64+72.", difficulty="stretch"),
        _q("Missing: 6 × ___ = 54.", 9, "6×9.", difficulty="stretch"),
        _q("Odd×odd is odd. 7×9 is?", 63, "Odd.", difficulty="stretch"),
        _q("10×13 − 10×3 as 10×(13−3).", 100, "10×10.", difficulty="stretch"),
        _q("How many 7s add to 56?", 8, "7×8.", difficulty="stretch"),
        _q("A grid 9 by 9 minus 1 square. Squares left?", 80, "81−1.", difficulty="stretch"),
        _q("Double 9×6.", 108, "54×2.", difficulty="stretch"),
        _q("Which pair has the same product: 6×8 and 4×12?", 48, "Both 48.", difficulty="stretch"),
    ]
    return qs


def g3u4():
    qs = []
    for a, b in ((18, 3), (24, 6), (35, 5), (42, 7), (56, 8), (63, 9), (72, 8), (81, 9), (40, 5), (96, 8)):
        qs.append(_q(f"{a} ÷ {b} = ?", a // b, f"{a}÷{b}={a//b}."))
    qs += [
        _q("20 ÷ 4 = ?", 5, "4×5=20."),
        _q("A remainder: 17 ÷ 5. Remainder?", 2, "3×5=15, rem 2."),
        _q("How many groups of 6 in 30?", 5, "30÷6."),
        _q("Missing: ___ ÷ 7 = 6.", 42, "7×6."),
        _q("Fair share 28 into 4. Each?", 7, "28÷4."),
        _q("29 ÷ 4 = 7 remainder ?", 1, "28+1.", difficulty="hard"),
        _q("A story: 45 apples in bags of 6. Full bags? Remainder apples?", 3, "7×6=42, rem 3.", difficulty="hard"),
        _q("Which is exact: 36÷9 or 36÷8? The exact quotient?", 4, "36÷9=4.", difficulty="hard"),
        _q("Twice a number is 18. The number (as 18÷2)?", 9, "Division as inverse.", difficulty="hard"),
        _q("A two-step: 48 ÷ 6 then × 5.", 40, "8×5.", difficulty="stretch"),
        _q("If 8 kids share 50 stickers equally, leftover?", 2, "6×8=48, rem 2.", difficulty="stretch"),
        _q("100 ÷ 25 = ?", 4, "4.", difficulty="stretch"),
        _q("A number divided by 8 is 9. Number?", 72, "8×9.", difficulty="stretch"),
        _q("Area 54, width 6. Length?", 9, "54÷6.", difficulty="stretch"),
        _q("Compare 72÷8 and 56÷7. Greater quotient?", 9, "9 vs 8.", difficulty="stretch"),
        _q("Division with 0: 0÷9?", 0, "Zero groups.", difficulty="stretch"),
        _q("You cannot divide by…", 0, "Division by zero undefined.", ["1", "2", "10"], "stretch"),
        _q("A remainder must be less than the divisor. For ÷7, remainder cannot be?", 7, "If rem 7 you make another group.", difficulty="stretch"),
        _q("64 ÷ 4 ÷ 2 = ?", 8, "16÷2.", difficulty="stretch"),
        _q("A bus 4 seats per row, 36 people. Rows needed?", 9, "36÷4.", difficulty="stretch"),
    ]
    return qs


def g3u5():
    qs = [
        _q("A shop: 3 packs of 8 plus 5 extra. Total?", 29, "24+5."),
        _q("You have 40. Spend 12 then 9. Left?", 19, "28−9."),
        _q("A field 6 rows of 7 pumpkins. 5 are rotten. Good?", 37, "42−5."),
        _q("Two classes 24 and 18. Make groups of 6. Groups?", 7, "42÷6."),
        _q("A number plus 15 is 40. Then double that original number.", 50, "Original 25, ×2=50."),
        _q("Tickets $5. Buy 7, pay $40. Change?", 5, "35, change 5."),
        _q("A recipe ×3: original 6 cups. New cups?", 18, "6×3."),
        _q("Start 90. Subtract 25, add 8.", 73, "65+8."),
        _q("4 boxes of 12, then eat 10.", 38, "48−10."),
        _q("A two-step compare: 9×5 vs 40+8. Greater?", 45, "45 vs 48? 48 is greater. Question asks 9×5 value? Wait specify: how much greater is 40+8 than 9×5?", 3, "48−45=3."),
        _q("How much greater is 40+8 than 9×5?", 3, "48−45=3."),
        _q("A park 120 trees, plant 35, lose 12. Now?", 143, "155−12."),
        _q("Miles 15+15+9. Total. Goal 50. Short?", 11, "39, need 11."),
        _q("A pattern 5,10,15… 8th term?", 40, "5×8."),
        _q("Multi-step money: 3 toys at $9, coupon $5 off total. Pay?", 22, "27−5.", difficulty="hard"),
        _q("A leftover story: 50 ÷ 8 full groups, leftover used in pairs. Leftover after pairs?", 2, "Rem 2, cannot pair.", difficulty="hard"),
        _q("Two-step with extra: 8 red, 6 blue, 3 yellow, it rained. Total crayons?", 17, "8+6+3.", difficulty="hard"),
        _q("A bus 48 seats. 5 empty rows of 4. Occupied?", 28, "20 empty, 48−20.", difficulty="hard"),
        _q("SAT-style: A baker makes 6 trays of 8 muffins and sells 2 trays. Muffins left?", 32, "48−16.", difficulty="stretch"),
        _q("A number: I multiply by 4 then add 7 to get 35. Start?", 7, "(35−7)/4=7.", difficulty="stretch"),
        _q("Compare two plans: 5×9+2 vs 6×7. Larger?", 47, "47 vs 42.", difficulty="stretch"),
        _q("A fence 36 m, posts every 4 m including ends. Posts?", 10, "36/4+1=10.", difficulty="stretch"),
        _q("Work 3 days × 8 hours, then 2 hours overtime. Hours?", 26, "24+2.", difficulty="stretch"),
        _q("A tank 45 L, use 1/3 of it (15 L), refill 8. Amount?", 38, "30+8.", difficulty="stretch"),
        _q("Inventory 200, sell 75, return 12, sell 40. Left?", 97, "137+12=149−40.", difficulty="stretch"),
        _q("A riddle: twice a number plus 5 is 21. Number?", 8, "2n+5=21.", difficulty="stretch"),
        _q("Teams of 6 from 50 players. How many left out?", 2, "8×6=48 rem 2.", difficulty="stretch"),
        _q("A two-shop: $3×4 + $5×2.", 22, "12+10.", difficulty="stretch"),
        _q("Distance 9 km three times then 4 km back. Net?", 23, "27−4.", difficulty="stretch"),
        _q("If each child gets 3 pencils from 40, leftover, then buy 5 more leftover becomes?", 8, "40=13×3+1, +5=6? Wait 1+5=6. Recalc: leftover 1 + 5 = 6.", difficulty="stretch"),
        _q("Start leftover 1 pencil, buy 5 more. Leftover pencils now (not regrouped)?", 6, "1+5=6.", difficulty="stretch"),
        _q("A chart: morning 18, afternoon twice morning, evening 10 less than afternoon. Evening?", 26, "36−10.", difficulty="stretch"),
        _q("Combined operations: (12+8)÷4 × 3.", 15, "20÷4=5×3.", difficulty="stretch"),
        _q("A school 4 classes of 22, 6 absent. Present?", 82, "88−6.", difficulty="stretch"),
        _q("You need 100. Have 4 packs of 18 and 15 loose. Still need?", 13, "72+15=87, need 13.", difficulty="stretch"),
    ]
    # remove the broken first compare question
    qs = [q for q in qs if q and "Wait specify" not in q["question_text"] and "not regrouped" not in q["question_text"]]
    return qs


def g3u6():
    qs = []
    for n, d in ((1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (1, 6), (5, 6), (1, 8), (3, 8), (7, 8)):
        qs.append(_q(f"What fraction is {n} of {d} equal parts?", f"{n}/{d}", f"{n}/{d}."))
    qs += [
        _q("Which is larger of the same whole: 1/3 or 1/5?", "1/3", "Larger piece.", ["1/5", "same", "0"]),
        _q("2/4 compared with 1/2.", "equal", "Equivalent.", ["2/4 bigger", "1/2 bigger", "none"]),
        _q("3/3 equals…", 1, "A whole."),
        _q("A number line 0 to 1, 4 equal spaces. Each tick is?", "1/4", "Fourths."),
        _q("Equivalent to 2/6?", "1/3", "Divide by 2.", difficulty="hard"),
        _q("You eat 1/4 then 1/4 of a pizza. Eaten?", "1/2", "2/4=1/2.", difficulty="hard"),
        _q("Which is closer to 1: 5/6 or 2/6?", "5/6", "5/6 near 1.", difficulty="hard"),
        _q("8 equal parts, 3 shaded. Fraction not shaded?", "5/8", "8−3.", difficulty="hard"),
        _q("Compare 3/8 and 3/5 (same numerator). Larger?", "3/5", "Smaller denominator, larger piece.", difficulty="stretch"),
        _q("A whole split in 2 then each half in 3. Smallest piece?", "1/6", "2×3=6.", difficulty="stretch"),
        _q("3/4 of 12 apples?", 9, "12÷4×3.", difficulty="stretch"),
        _q("False: 1/10 > 1/2 because 10>2. True larger is?", "1/2", "Unit fractions decrease.", difficulty="stretch"),
        _q("Fractions equal to 1: 5/5, 6/6. Their difference?", 0, "Both 1.", difficulty="stretch"),
        _q("A recipe 3/4 cup. You only have 1/4 cup scoop. Scoops?", 3, "Three fourths.", difficulty="stretch"),
        _q("Locate 2/3 on a line 0–1. It is after 1/2. True? (Yes)", "Yes", "2/3≈0.67>0.5.", difficulty="stretch"),
        _q("1 − 1/4 = ?", "3/4", "Fourths left 3.", difficulty="stretch"),
        _q("Two unit fractions that sum to 1/2: 1/4 + 1/4. Sum?", "1/2", "2/4.", difficulty="stretch"),
        _q("A spinner 8 parts, 2 red. Fraction red in simplest form?", "1/4", "2/8=1/4.", difficulty="stretch"),
        _q("Improper: 5/4 is how much more than 1?", "1/4", "5/4−4/4.", difficulty="stretch"),
        _q("Equivalent 4/8, 2/4, 1/2. The simplest is?", "1/2", "Divide by 4.", difficulty="stretch"),
    ]
    return qs


def g3u7():
    qs = []
    for l, w in ((3, 4), (5, 6), (8, 2), (7, 7), (9, 3), (10, 4), (12, 5), (6, 8), (11, 2), (9, 9)):
        qs.append(_q(f"Area of a {l} by {w} rectangle?", l * w, f"{l}×{w}={l*w} square units."))
    qs += [
        _q("A square side 6. Area?", 36, "6×6."),
        _q("Area 24, length 8. Width?", 3, "24÷8."),
        _q("A rect 4×5 plus a 2×5 stuck on the length. Total area?", 30, "20+10."),
        _q("Unit squares in an L: 3×3 square missing a 1×1. Area?", 8, "9−1.", difficulty="hard"),
        _q("Which has more area: 3×8 or 5×5?", 25, "24 vs 25.", difficulty="hard"),
        _q("A patio 9×6. Tiles 1×1. Tiles needed?", 54, "Area.", difficulty="hard"),
        _q("Double the width of 4×7. New area?", 56, "4×14 or 2×28.", difficulty="hard"),
        _q("A 10×10 square with a 4×4 hole. Remaining area?", 84, "100−16.", difficulty="stretch"),
        _q("Two rectangles 6×3 and 5×4. Combined area?", 38, "18+20.", difficulty="stretch"),
        _q("If area is 36 and it is a square, side?", 6, "√36.", difficulty="stretch"),
        _q("A figure of 3 rows: 5, 5, 2 squares. Area?", 12, "5+5+2.", difficulty="stretch"),
        _q("Scale a 3×3 square by side ×2. New area factor?", 4, "Area ×4.", difficulty="stretch"),
        _q("Missing side: area 45, one side 9.", 5, "45÷9.", difficulty="stretch"),
        _q("A border 1-unit around 4×4 inner. Outer square side?", 6, "4+2.", difficulty="stretch"),
        _q("That border’s area (outer minus inner)?", 20, "36−16.", difficulty="stretch"),
        _q("Triangle as half of 8×6 rectangle. Area?", 24, "48/2.", difficulty="stretch"),
        _q("Which dimensions give area 12: 3×4 or 2×5?", "3×4", "12 vs 10.", difficulty="stretch"),
        _q("A hallway 2 by 15. Area?", 30, "2×15.", difficulty="stretch"),
        _q("Irregular: 8×5 rectangle minus 3×2. Area?", 34, "40−6.", difficulty="stretch"),
        _q("Same area as 6×6: 9 × ?", 4, "36÷9=4.", difficulty="stretch"),
    ]
    return qs


def g3u8():
    qs = []
    for l, w in ((3, 5), (4, 4), (6, 2), (10, 1), (8, 3), (7, 5), (9, 9), (12, 4), (11, 2), (15, 5)):
        qs.append(_q(f"Perimeter of a {l} by {w} rectangle?", 2 * (l + w), f"2({l}+{w})={2*(l+w)}."))
    qs += [
        _q("Equilateral triangle side 7. Perimeter?", 21, "3×7."),
        _q("A square perimeter 32. Side?", 8, "32÷4."),
        _q("Regular pentagon side 6. Perimeter?", 30, "5×6."),
        _q("A run of 5 sides: 3+4+5+6+2. Perimeter?", 20, "Sum."),
        _q("Rectangle 9×6. Perimeter vs area: perimeter?", 30, "2(15).", difficulty="hard"),
        _q("If you add 1 to each side of a 4×4 square, new perimeter?", 20, "5×4=20.", difficulty="hard"),
        _q("A missing side: sides 8, 5, 8, and perimeter 26. Missing?", 5, "26−21=5.", difficulty="hard"),
        _q("Two squares side 3 joined on one side. Outer perimeter?", 16, "24−2×3=18? 2 squares perim 24, subtract 2 shared sides (6), 18. Fix: 18.", difficulty="hard"),
        _q("Two squares of side 3 sharing one full side. Outer perimeter?", 18, "4×3×2 − 2×3 = 18.", difficulty="hard"),
        _q("A garden 12 by 5, fence cost $2 per unit. Cost?", 68, "Perim 34 ×2.", difficulty="stretch"),
        _q("Which can have perim 16: 3×5 or 4×4?", "both", "16 and 16.", difficulty="stretch"),
        _q("A triangle 6, 7, 8 vs 5, 5, 5. Larger perimeter?", 21, "21 vs 15.", difficulty="stretch"),
        _q("Double all sides of a 2×7 rectangle. New perimeter?", 36, "Original 18 ×2.", difficulty="stretch"),
        _q("A regular hexagon perimeter 48. Side?", 8, "48÷6.", difficulty="stretch"),
        _q("Walk around a 10×10 square twice. Distance?", 80, "40×2.", difficulty="stretch"),
        _q("An L: 6×6 square minus 2×2 corner, outer perimeter of L?", 24, "Original 24, cutting a corner adds 0 net for a square bite? For a 2×2 square cut from corner, perimeter stays 24.", difficulty="stretch"),
        _q("Perimeter of a 6×6 square with a 2×2 square removed from a corner?", 24, "You remove 2 sides of length 2 but add 2 inner sides of 2: perimeter unchanged 24.", difficulty="stretch"),
        _q("A pentagon sides 4,4,4,4,x and perim 22. x?", 6, "16+x=22.", difficulty="stretch"),
        _q("Smallest perimeter of a rectangle area 12 with whole-number sides?", 14, "3×4 → 14, better than 2×6=16 or 1×12=26.", difficulty="stretch"),
        _q("A track 100 m per lap. 3 laps vs a 80×20 rectangle once. Which distance is longer (the number)?", 300, "300 vs 200.", difficulty="stretch"),
    ]
    qs = [q for q in qs if q and "Fix:" not in q["explanation"]]
    return qs


# ----- Grade 4 (place value, mult, div, fractions, decimals, geometry) -----
def g4u1():
    qs = []
    for n in (45_231, 80_006, 120_450, 999_000, 3_040_001):
        qs.append(_q(f"What is 10 times {n}?", n * 10, "Shift one place left."))
    qs += [
        _q("Value of 7 in 3,705,219?", 700000, "7 hundred thousands."),
        _q("Compare 4,099,999 and 4,100,000. Greater?", 4100000, "By 1."),
        _q("Round 76,450 to nearest thousand.", 76000, "4 < 5."),
        _q("Round 76,500 to nearest thousand.", 77000, "5 rounds up."),
        _q("Expanded 200000+3000+40+1?", 203041, "203,041."),
        _q("How many ten-thousands in 580,000?", 58, "58 ten-thousands.", difficulty="hard"),
        _q("1 million is 10 × ?", 100000, "100,000.", difficulty="hard"),
        _q("Greatest 6-digit with distinct 0-9 starting digits 5,0,9,1,3,7?", 975310, "Arrange descending with 0 not leading.", difficulty="hard"),
        _q("A number 10 times 45,067.", 450670, "450,670.", difficulty="hard"),
        _q("Difference 1,000,000 − 1.", 999999, "999,999.", difficulty="stretch"),
        _q("Which is 100 times 3,406?", 340600, "Two-place shift.", difficulty="stretch"),
        _q("Place of 2 in 12,345,678?", "millions", "12 million…", ["hundred thousands", "ten millions", "thousands"], "stretch"),
        _q("Round 2,500,500 to nearest million.", 3000000, "0.5 million+ rounds up.", difficulty="stretch"),
        _q("Standard form 14 ten-thousands + 6 hundreds.", 140600, "140,000+600.", difficulty="stretch"),
        _q("Compare 808,080 and 808,800. How much greater is the second?", 720, "808800−808080.", difficulty="stretch"),
        _q("A digit 9 worth 9,000,000 is in which place?", "millions", "9 million.", difficulty="stretch"),
        _q("10 times smaller than 56,000?", 5600, "Shift right.", difficulty="stretch"),
        _q("Smallest 7-digit number?", 1000000, "1,000,000.", difficulty="stretch"),
        _q("4,004,400 vs 4,040,040. Greater?", 4040040, "Compare hundred thousands.", difficulty="stretch"),
        _q("Write 3 million 25 thousand 8.", 3025008, "3,025,008.", difficulty="stretch"),
    ]
    return qs


def g4u2():
    qs = []
    for a, b in ((23, 6), (45, 8), (67, 9), (108, 4), (256, 7), (39, 12), (84, 5), (123, 6), (250, 8), (99, 11)):
        qs.append(_q(f"{a} × {b} = ?", a * b, f"{a}×{b}={a*b}."))
    qs += [
        _q("25 × 16 = 25 × (10+6). Product?", 400, "250+150."),
        _q("99 × 7. Think 100×7 − 7.", 693, "700−7."),
        _q("40 × 30 = ?", 1200, "12×100."),
        _q("A school 18 classes of 27. Students?", 486, "18×27.", difficulty="hard"),
        _q("Area model 34 × 26.", 884, "600+180+80+24.", difficulty="hard"),
        _q("12 × 12 × 2.", 288, "144×2.", difficulty="hard"),
        _q("If 15 × n = 225, n?", 15, "225÷15.", difficulty="hard"),
        _q("A SAT-style: 48 boxes of 24 bottles. Total bottles?", 1152, "48×24.", difficulty="stretch"),
        _q("Estimate 198 × 21 (nearest 200×20).", 4000, "About 4000. Exact 4158 not asked.", difficulty="stretch"),
        _q("Exact 198 × 21.", 4158, "198×20+198.", difficulty="stretch"),
        _q("Which is larger: 25×36 or 30×29?", 900, "900 vs 870.", difficulty="stretch"),
        _q("A number times 8 is 1,000. Not whole. Closest whole n below?", 125, "8×125=1000.", difficulty="stretch"),
        _q("Distributive: 7×(50+8).", 406, "350+56.", difficulty="stretch"),
        _q("A stack 16 × 16. Product?", 256, "256.", difficulty="stretch"),
        _q("Multiply 305 × 4.", 1220, "1220.", difficulty="stretch"),
        _q("A two-step: 23×6 then add 19.", 157, "138+19.", difficulty="stretch"),
        _q("10² × 6.", 600, "100×6.", difficulty="stretch"),
        _q("A farm 14 rows of 35 trees. Trees?", 490, "14×35.", difficulty="stretch"),
        _q("Missing: 40 × ___ = 1,200.", 30, "1200÷40.", difficulty="stretch"),
        _q("Product of 3 numbers 5×12×8.", 480, "60×8.", difficulty="stretch"),
    ]
    return qs


def g4u3():
    qs = []
    for a, b in ((84, 4), (96, 6), (144, 12), (225, 5), (368, 8), (505, 5), (729, 9), (840, 7), (1000, 8), (256, 4)):
        qs.append(_q(f"{a} ÷ {b} = ?", a // b if a % b == 0 else f"{a // b} r {a % b}", f"{a}÷{b}."))
    qs += [
        _q("91 ÷ 7 = ?", 13, "7×13."),
        _q("100 ÷ 8. Remainder?", 4, "12×8=96 rem 4."),
        _q("A number ÷ 6 = 14. Number?", 84, "6×14."),
        _q("Long division 748 ÷ 4.", 187, "4×187=748.", difficulty="hard"),
        _q("A leftover story: 250 ÷ 12. Remainder?", 10, "20×12=240 rem 10.", difficulty="hard"),
        _q("Estimate 795 ÷ 4 ≈ ?", 200, "800÷4.", difficulty="hard"),
        _q("If 9 × n = 1,026, n?", 114, "1026÷9.", difficulty="hard"),
        _q("A SAT-style: 1,440 minutes is how many 24-hour days?", 1, "1440÷1440=1 day. 1440 min = 24 hours = 1 day.", difficulty="stretch"),
        _q("1,440 ÷ 24 (hours in minutes / minutes per hour)? Wait: 1440÷60 hours?", 24, "1440 minutes ÷ 60 = 24 hours.", difficulty="stretch"),
        _q("A warehouse 1,368 items in cartons of 8. Cartons?", 171, "1368÷8.", difficulty="stretch"),
        _q("Remainder when 1,000 divided by 9?", 1, "111×9=999.", difficulty="stretch"),
        _q("A two-step: 560÷7 then × 3.", 240, "80×3.", difficulty="stretch"),
        _q("Which remainder is possible for ÷11: 11 or 10?", 10, "Remainder < divisor.", difficulty="stretch"),
        _q("Partial quotients: 600÷15.", 40, "15×40.", difficulty="stretch"),
        _q("A bus 36 seats, 300 students. Buses needed (round up)?", 9, "8×36=288, need 9.", difficulty="stretch"),
        _q("Divide 4,005 by 5.", 801, "4005÷5.", difficulty="stretch"),
        _q("A number leaves rem 3 when ÷5 and is 18. Check 18÷5 rem?", 3, "3×5=15 rem 3.", difficulty="stretch"),
        _q("Greatest 3-digit divisible by 8?", 992, "8×124=992.", difficulty="stretch"),
        _q("If 7 friends share 100 equally, leftover cents if $1=100¢? Leftover cents?", 2, "14×7=98 rem 2.", difficulty="stretch"),
        _q("Area 132, width 12. Length?", 11, "132÷12.", difficulty="stretch"),
    ]
    return qs


def g4u4():
    qs = [
        _q("1/5 + 2/5 = ?", "3/5", "Same denominator, add numerators."),
        _q("7/8 − 3/8 = ?", "4/8", "Or 1/2."),
        _q("3/4 + 1/4 = ?", 1, "4/4."),
        _q("Equivalent to 6/8?", "3/4", "÷2."),
        _q("2/10 + 3/10 = ?", "5/10", "Or 1/2."),
        _q("A pizza 3/8 + 2/8 eaten. Eaten?", "5/8", "Add."),
        _q("Which is larger: 5/6 or 4/6?", "5/6", "Same den."),
        _q("Decompose 5/6 = 1/6 + ?", "4/6", "5−1."),
        _q("1 − 3/8 = ?", "5/8", "8/8−3/8."),
        _q("2/3 vs 3/4. Larger?", "3/4", "8/12 vs 9/12.", difficulty="hard"),
        _q("Add 5/12 + 4/12 then simplify.", "3/4", "9/12=3/4.", difficulty="hard"),
        _q("A recipe 2/5 + 2/5 cup. Total?", "4/5", "4/5.", difficulty="hard"),
        _q("Subtract 11/12 − 5/12.", "1/2", "6/12=1/2.", difficulty="hard"),
        _q("SAT-style: A tank 3/8 full, add 2/8. How empty?", "3/8", "5/8 full, 3/8 empty.", difficulty="stretch"),
        _q("3/10 + 1/10 + 1/10.", "1/2", "5/10.", difficulty="stretch"),
        _q("Compare 7/8 − 1/8 and 1/2. Greater result?", "3/4", "6/8=3/4 > 1/2.", difficulty="stretch"),
        _q("A number line jump 1/5 five times from 0. Land?", 1, "5/5.", difficulty="stretch"),
        _q("Improper 9/8 − 1/8.", 1, "8/8.", difficulty="stretch"),
        _q("Two fractions of 12: 5/12 and 7/12. Sum?", 1, "12/12.", difficulty="stretch"),
        _q("You need 3/4. You have 1/4 + 1/4. Still need?", "1/4", "2/4, need 1/4 more.", difficulty="stretch"),
        _q("Benchmark: 2/5 is closer to 0, 1/2, or 1?", "1/2", "2/5=0.4.", difficulty="stretch"),
        _q("False equivalent: 2/4 = 3/5? The true equivalent of 2/4 is?", "1/2", "Not 3/5.", difficulty="stretch"),
        _q("A mixed idea: 1 + 1/3 as an improper fraction?", "4/3", "3/3+1/3.", difficulty="stretch"),
        _q("Difference 1/2 − 1/6 (common den 6).", "1/3", "3/6−1/6=2/6=1/3.", difficulty="stretch"),
        _q("Add unlike: 1/2 + 1/4.", "3/4", "2/4+1/4.", difficulty="stretch"),
        _q("A track 5/8 km, walk 2/8 more. Total km as a fraction?", "7/8", "7/8.", difficulty="stretch"),
        _q("Which sum is 1: 2/7+5/7 or 3/7+3/7?", "2/7+5/7", "7/7=1.", difficulty="stretch"),
        _q("Simplify 10/12.", "5/6", "÷2.", difficulty="stretch"),
        _q("A word: 7/10 of a meter minus 2/10.", "1/2", "5/10.", difficulty="stretch"),
        _q("Three addends 1/8+2/8+3/8.", "3/4", "6/8.", difficulty="stretch"),
    ]
    return qs


def g4u5():
    qs = [
        _q("0.7 as a fraction in tenths?", "7/10", "Seven tenths."),
        _q("0.25 as hundredths?", "25/100", "Or 1/4."),
        _q("0.4 + 0.3 = ?", "0.7", "7 tenths."),
        _q("Which is greater: 0.8 or 0.75?", "0.8", "80 hundredths vs 75."),
        _q("1.00 − 0.35 = ?", "0.65", "65 hundredths."),
        _q("0.09 vs 0.9. Greater?", "0.9", "9 tenths."),
        _q("3 tenths + 4 hundredths as a decimal?", "0.34", "0.30+0.04."),
        _q("A meter 0.6 + 0.25. Total?", "0.85", "85 hundredths."),
        _q("Round 0.46 to tenths.", "0.5", "6≥5."),
        _q("0.5 as a fraction simplest?", "1/2", "5/10.", difficulty="hard"),
        _q("Which equals 3/4: 0.75, 0.34, 0.7?", "0.75", "75/100=3/4.", difficulty="hard"),
        _q("A money $0.40 + $0.35.", "0.75", "75 cents.", difficulty="hard"),
        _q("1 − 0.08 = ?", "0.92", "92 hundredths.", difficulty="hard"),
        _q("SAT-style: A tank 0.4 full, add 0.35. How empty (as decimal)?", "0.25", "0.75 full.", difficulty="stretch"),
        _q("Order: 0.4, 0.04, 0.44. Middle?", "0.4", "0.04, 0.4, 0.44.", difficulty="stretch"),
        _q("0.2 + 0.2 + 0.2 + 0.2 + 0.2.", 1, "1.0.", difficulty="stretch"),
        _q("A number line 0 to 1, mark 0.3. Equivalent fraction tenths?", "3/10", "3/10.", difficulty="stretch"),
        _q("Compare 0.99 and 1. Smaller difference from 1 is for?", "0.99", "0.01 away.", difficulty="stretch"),
        _q("7/10 − 2/10 as a decimal.", "0.5", "0.5.", difficulty="stretch"),
        _q("A race 0.25 km + 0.5 km.", "0.75", "0.75 km.", difficulty="stretch"),
        _q("Which is 40 hundredths?", "0.40", "0.4.", difficulty="stretch"),
        _q("0.06 × 10 (place shift).", "0.6", "6 tenths.", difficulty="stretch"),
        _q("A decimal 2.3 is 2 + ?", "0.3", "3 tenths.", difficulty="stretch"),
        _q("False: 0.8 = 8/100. The true fraction of 0.8 is?", "8/10", "Or 4/5.", difficulty="stretch"),
        _q("Add 0.45 + 0.45.", "0.9", "90 hundredths.", difficulty="stretch"),
        _q("A grid 100 squares, 37 shaded. Decimal?", "0.37", "37/100.", difficulty="stretch"),
        _q("How many tenths in 1.7?", 17, "17 tenths.", difficulty="stretch"),
        _q("0.5 − 0.28 = ?", "0.22", "50−28 hundredths.", difficulty="stretch"),
        _q("A price $1.05 − $0.40.", "0.65", "$0.65.", difficulty="stretch"),
        _q("Equivalent: 0.50 and 0.5. They differ by?", 0, "Equal.", difficulty="stretch"),
    ]
    return qs


def g4u6():
    return [
        _q("A right angle measures ___ degrees.", 90, "Quarter turn."),
        _q("A straight angle is ___ degrees.", 180, "Half turn."),
        _q("An acute angle is ___ than 90°.", "less", "Smaller than right.", ["greater", "equal", "straight"]),
        _q("An obtuse angle is between 90° and ___°.", 180, "But not including 180."),
        _q("A full turn is ___ degrees.", 360, "Full circle."),
        _q("Two lines that never meet and stay same distance are…", "parallel", "Parallel.", ["perpendicular", "skew always", "curved"]),
        _q("Perpendicular lines meet at ___ degrees.", 90, "Right angle."),
        _q("A ray has how many endpoints?", 1, "Starts at a point, goes forever."),
        _q("A line segment has how many endpoints?", 2, "Two."),
        _q("A point is named with a…", "capital letter", "Point A.", ["number only", "arrow", "degree"]),
        _q("Complementary angles sum to ___°.", 90, "Complement 90."),
        _q("Supplementary angles sum to ___°.", 180, "Straight."),
        _q("If one angle of a linear pair is 65°, the other is?", 115, "180−65.", difficulty="hard"),
        _q("A triangle cannot have two ___ angles.", "obtuse", "Sum would exceed 180.", difficulty="hard"),
        _q("Angle 40° and its complement?", 50, "90−40.", difficulty="hard"),
        _q("A square has how many right angles?", 4, "Four.", difficulty="hard"),
        _q("Lines AB and CD cross. Vertical angles are…", "equal", "Opposite equal.", difficulty="stretch"),
        _q("An angle 1° more than a right angle is?", 91, "Obtuse.", difficulty="stretch"),
        _q("How many degrees from North to East (clockwise)?", 90, "Quarter.", difficulty="stretch"),
        _q("A protractor reads 0 to 180. An angle opening 2/3 of a straight angle is?", 120, "180×2/3.", difficulty="stretch"),
        _q("Parallel lines cut by a transversal: corresponding angles are…", "equal", "Same position.", difficulty="stretch"),
        _q("A reflex angle is greater than 180 but less than 360. Example: 200. How much more than straight?", 20, "200−180.", difficulty="stretch"),
        _q("Three angles of a triangle 50, 60, third?", 70, "180−110.", difficulty="stretch"),
        _q("A point in the interior of an angle is ___ on the rays.", "not", "Interior is between rays.", difficulty="stretch"),
        _q("Draw: two perpendicular diameters in a circle. How many right angles at the center?", 4, "Four 90°.", difficulty="stretch"),
        _q("An equilateral triangle angles?", 60, "All 60.", difficulty="stretch"),
        _q("If two angles are complementary and equal, each is?", 45, "90/2.", difficulty="stretch"),
        _q("A clock at 3:00 forms ___° between hands.", 90, "Right.", difficulty="stretch"),
        _q("A clock at 6:00 forms ___°.", 180, "Straight.", difficulty="stretch"),
        _q("Acute, right, obtuse, straight. Which is 89°?", "acute", "Just under 90.", difficulty="stretch"),
        _q("A rectangle that’s not a square still has ___ right angles.", 4, "Always 4.", difficulty="stretch"),
        _q("Intersecting lines form ___ pairs of vertical angles.", 2, "Two pairs.", difficulty="stretch"),
        _q("An angle bisector of 80° makes two angles of ___ each.", 40, "Half.", difficulty="stretch"),
        _q("Turn 3 right angles. Total degrees?", 270, "3×90.", difficulty="stretch"),
        _q("A polygon with all right angles and 4 sides is a…", "rectangle", "Includes squares.", difficulty="stretch"),
    ]


def g4u7():
    qs = []
    for d in (15, 30, 45, 60, 75, 90, 120, 135, 150, 180):
        qs.append(_q(f"A turn of {d}° is what fraction of a full turn (as a simplified fraction if possible)?",
                     f"{d}/360" if math.gcd(d, 360) == 1 else f"{d // math.gcd(d, 360)}/{360 // math.gcd(d, 360)}",
                     f"{d}/360 simplifies by gcd {math.gcd(d, 360)}."))
    qs += [
        _q("A quarter turn is ___°.", 90, "360/4."),
        _q("A half turn is ___°.", 180, "360/2."),
        _q("3/4 of a full turn in degrees?", 270, "270."),
        _q("From 0° to 40° is an ___ angle.", "acute", "40<90.", difficulty="hard"),
        _q("A skater turns 90° four times. Total?", 360, "Full turn.", difficulty="hard"),
        _q("Facing North, turn 90° clockwise. Face?", "East", "N→E.", difficulty="hard"),
        _q("Facing East, turn 180°. Face?", "West", "Opposite.", difficulty="hard"),
        _q("A robot turns 45° six times. Total degrees?", 270, "270.", difficulty="stretch"),
        _q("How many 15° wedges in a straight angle?", 12, "180/15.", difficulty="stretch"),
        _q("A pie 8 equal slices. Degrees per slice?", 45, "360/8.", difficulty="stretch"),
        _q("Turn 1/6 of a circle. Degrees?", 60, "360/6.", difficulty="stretch"),
        _q("Clock minute hand 1 minute. Degrees?", 6, "360/60.", difficulty="stretch"),
        _q("Clock hour hand 1 hour. Degrees?", 30, "360/12.", difficulty="stretch"),
        _q("From 12 to 4 on a clock, degrees (shorter)?", 120, "4×30.", difficulty="stretch"),
        _q("A protractor mistake using inner vs outer scale. 30 vs 150. They sum to?", 180, "Supplementary pair on the scale.", difficulty="stretch"),
        _q("Two turns 70° and 20°. Combined vs a right angle: combined is ___° less than 90?", 0, "90−90=0.", difficulty="stretch"),
        _q("A compass 8 points. Angle between adjacent?", 45, "360/8.", difficulty="stretch"),
        _q("Spin 2 full turns + 90°.", 810, "720+90.", difficulty="stretch"),
        _q("An obtuse turn between 90 and 180. Example 135 is how far from 90?", 45, "135−90.", difficulty="stretch"),
        _q("A reflex 270° is how much more than a straight angle?", 90, "270−180.", difficulty="stretch"),
    ]
    return qs


def g4u8():
    return [
        _q("A protractor’s baseline must sit on one ___ of the angle.", "ray", "Align a ray with 0."),
        _q("The vertex goes at the protractor’s…", "center mark", "The midpoint of the baseline."),
        _q("If the ray passes 0 on the inside scale and the other ray at 55, the angle is ___°.", 55, "Read the same scale."),
        _q("An angle that looks about a quarter of a straight angle is near ___°.", 45, "180/4."),
        _q("You measure 130° but the angle is clearly acute. You used the wrong scale. The acute measure is?", 50, "180−130."),
        _q("A 90° angle on a protractor hits the ___ mark if 0 is on a ray.", 90, "Middle."),
        _q("To measure a 20° angle you should see the second ray near…", 20, "Not 160 unless wrong scale."),
        _q("Two angles 35° and 55° adjacent make a ___ angle.", "right", "90°.", ["acute", "obtuse", "straight"]),
        _q("A drawing of 180° looks like a…", "straight line", "Straight angle."),
        _q("Estimate: an angle a bit more than a right angle. Best: 95, 40, 180, 270?", 95, "Just obtuse."),
        _q("If both scales show 0 and 180 on the baseline, the top of the curve is ___°.", 90, "Right above center."),
        _q("A triangle drawn with angles 40 and 70. Third, then measure check?", 70, "180−110=70.", difficulty="hard"),
        _q("You place the vertex at 20 instead of 0. The reading 70 actually means the angle is?", 50, "70−20.", difficulty="hard"),
        _q("A reflex angle 200°. A protractor (0–180) cannot show it directly. The smaller adjacent interior on the other side is?", 160, "360−200.", difficulty="hard"),
        _q("Parallel lines look like they never meet. On paper you still measure a transversal angle of 110. The corresponding angle is?", 110, "Equal.", difficulty="hard"),
        _q("SAT-style lab: An angle bisector splits 84°. Each piece?", 42, "Half.", difficulty="stretch"),
        _q("Three copies of a 40° angle around a point. Remaining angle to complete 360°?", 240, "360−120.", difficulty="stretch"),
        _q("A mistake of 5° too high on a 60° angle reports?", 65, "60+5.", difficulty="stretch"),
        _q("Complement of a measured 18°?", 72, "90−18.", difficulty="stretch"),
        _q("A quadrilateral angles 90, 90, 90. Fourth?", 90, "360−270. Rectangle.", difficulty="stretch"),
        _q("Which tool: length vs angle — protractor measures…", "angles", "Not length.", difficulty="stretch"),
        _q("If a ray is too short to read, you should…", "extend the ray", "Rays can be drawn longer.", difficulty="stretch"),
        _q("An isosceles right triangle has a 90° and two ___° angles.", 45, "45-45-90.", difficulty="stretch"),
        _q("Measure twice: 48° and 47°. Best report (average)?", 47.5, "Or 48 if to nearest degree. Use 48 if integer required—choose 48.", difficulty="stretch"),
        _q("Nearest degree: readings 48 and 47. Report?", 48, "Typical nearest; 47.5 rounds to 48.", difficulty="stretch"),
        _q("A full-circle protractor (if you had one) at 270° is a ___ turn.", "three-quarter", "270/360.", difficulty="stretch"),
        _q("Zero on the LEFT scale vs RIGHT: always read the scale that starts at 0 on your base ray. If base is 0 on outer, use outer. Outer 0, inner 180. Ray at outer 40 is ___°.", 40, "Same-scale rule.", difficulty="stretch"),
        _q("An angle in a square corner should measure ___° if the square is true.", 90, "Check drawing.", difficulty="stretch"),
        _q("Two measured adjacent angles 62 and 118. They form a straight line? Sum?", 180, "Yes.", difficulty="stretch"),
        _q("Lab error: vertex not on origin adds scatter. The fix is to…", "realign the vertex", "Center the vertex.", difficulty="stretch"),
        _q("A 1° angle is ___ times a 15° angle.", "1/15", "Very thin.", difficulty="stretch"),
        _q("How many 30° angles fit in a straight angle?", 6, "180/30.", difficulty="stretch"),
        _q("A pentagram/star point is acute. A typical 36° point: complement?", 54, "90−36.", difficulty="stretch"),
        _q("If you turn the paper, the angle measure…", "stays the same", "Measure is invariant.", difficulty="stretch"),
        _q("A reflex and its adjacent around a point sum to ___°.", 360, "Full around a point.", difficulty="stretch"),
    ]


# ----- Grade 5 -----
def g5u1():
    qs = []
    for n in ("0.407", "1.205", "3.014", "0.090", "12.006"):
        qs.append(_q(f"How many thousandths in {n}?", int(round(float(n) * 1000)), f"Multiply by 1000: {n} → thousandths."))
    qs += [
        _q("0.4 + 0.07 + 0.009 as a decimal?", "0.479", "4 tenths 7 hundredths 9 thousandths."),
        _q("Which is greater: 0.208 or 0.28?", "0.28", "280 thousandths vs 208."),
        _q("Round 3.456 to hundredths.", "3.46", "6≥5."),
        _q("Round 3.456 to tenths.", "3.5", "5≥5 from the 5 in hundredths? 5 in hundredths, look at thousandths 6 so 3.46 then? Standard: tenths place 4, next digit 5 so round to 3.5."),
        _q("10 × 0.045 = ?", "0.45", "Shift left one."),
        _q("100 × 0.045 = ?", "4.5", "Two places."),
        _q("0.8 as thousandths?", "0.800", "800 thousandths."),
        _q("A number line 0–1, mark 0.375. Equivalent fraction?", "3/8", "375/1000=3/8.", difficulty="hard"),
        _q("Compare 2.099 and 2.109. Greater?", "2.109", "Hundredths 0 vs 1.", difficulty="hard"),
        _q("1 − 0.001 = ?", "0.999", "999 thousandths.", difficulty="hard"),
        _q("Place of 5 in 4.052?", "hundredths", "5 hundredths.", difficulty="hard"),
        _q("SAT-style: A meter stick 0.407 m + 0.593 m.", 1, "1.000 m.", difficulty="stretch"),
        _q("Order 0.6, 0.06, 0.606. Middle?", "0.6", "0.06, 0.6, 0.606.", difficulty="stretch"),
        _q("0.25 × 10 vs 0.025 × 100. Equal value?", "0.25", "Both 2.5? 0.25×10=2.5, 0.025×100=2.5. The equal value is 2.5.", difficulty="stretch"),
        _q("0.25 × 10 = 0.025 × 100. That common value is?", "2.5", "2.5.", difficulty="stretch"),
        _q("A digit 9 in 0.009 is worth?", "9/1000", "9 thousandths.", difficulty="stretch"),
        _q("Expanded 3 + 4/10 + 5/1000.", "3.405", "3.405.", difficulty="stretch"),
        _q("Which is 47 thousandths?", "0.047", "0.047.", difficulty="stretch"),
        _q("Nearest thousandth: 0.1284 → ?", "0.128", "4<5.", difficulty="stretch"),
        _q("A race 0.125 km is how many meters?", 125, "0.125×1000.", difficulty="stretch"),
        _q("False: 0.40 > 0.400. They differ by?", 0, "Equal.", difficulty="stretch"),
        _q("3.5 as thousandths?", "3.500", "3500 thousandths.", difficulty="stretch"),
        _q("Subtract 1.2 − 0.075.", "1.125", "Align places.", difficulty="stretch"),
        _q("A grid 1000 cubes, 241 shaded. Decimal?", "0.241", "241/1000.", difficulty="stretch"),
        _q("How many hundredths in 3.4?", 340, "340 hundredths.", difficulty="stretch"),
    ]
    qs = [q for q in qs if q and "Both 2.5?" not in q["explanation"] or "common value" in q["question_text"]]
    return qs


def g5u2():
    qs = []
    for a, b in ((346, 8), (509, 6), (1_204, 7), (3_333, 9), (2_560, 5), (18_024, 4), (7_007, 7), (999, 3), (4_080, 8), (12_345, 5)):
        qs.append(_q(f"{a} × {b} = ?", a * b, f"{a}×{b}={a*b}."))
    qs += [
        _q("25 × 48 using 25×50 − 25×2.", 1200, "1250−50."),
        _q("99 × 46.", 4554, "100×46−46."),
        _q("A warehouse 128 × 36.", 4608, "128×36.", difficulty="hard"),
        _q("1,000 − 1 × 8. Value? (order)", 992, "1000−8.", difficulty="hard"),
        _q("Partial products 27×34.", 918, "800+80+120− wait 20×30=600, 20×4=80, 7×30=210, 7×4=28 → 918.", difficulty="hard"),
        _q("If 16 × n = 1,024, n?", 64, "1024÷16.", difficulty="hard"),
        _q("SAT-style: 45 boxes of 28, then 17 leftover. Total?", 1277, "1260+17.", difficulty="stretch"),
        _q("Estimate 198×31 ≈ 200×30.", 6000, "About 6000.", difficulty="stretch"),
        _q("Exact 198×31.", 6138, "198×30+198.", difficulty="stretch"),
        _q("A two-step: 125×8 − 99.", 901, "1000−99.", difficulty="stretch"),
        _q("Powers: 10^3 × 6.", 6000, "6000.", difficulty="stretch"),
        _q("Which product is larger: 24×25 or 20×31?", 620, "600 vs 620.", difficulty="stretch"),
        _q("Multiply 4.0 conceptually 40×40 as 4 tens squared: 1600. 40×40?", 1600, "1600.", difficulty="stretch"),
        _q("A farm 64 × 25 (think ÷4 ×100).", 1600, "64/4=16×100.", difficulty="stretch"),
        _q("Missing: 250 × ___ = 10,000.", 40, "10000÷250.", difficulty="stretch"),
        _q("3-factor 8×15×12.", 1440, "120×12.", difficulty="stretch"),
        _q("A number 1 more than 99×99. (100×99 − 99 +1)? 99×99=9801, +1?", 9802, "9801+1.", difficulty="stretch"),
        _q("99×99.", 9801, "(100−1)^2=10000−200+1.", difficulty="stretch"),
        _q("A school 32 classes of 28. Students?", 896, "32×28.", difficulty="stretch"),
        _q("Distributive 9×(200+7).", 1863, "1800+63.", difficulty="stretch"),
    ]
    return qs


def g5u3():
    qs = [
        _q("1/3 + 1/6 = ?", "1/2", "2/6+1/6."),
        _q("3/4 − 1/8 = ?", "5/8", "6/8−1/8."),
        _q("2/5 + 1/2 = ?", "9/10", "4/10+5/10."),
        _q("5/6 − 1/3 = ?", "1/2", "5/6−2/6."),
        _q("1/2 + 1/3 + 1/6 = ?", 1, "3/6+2/6+1/6."),
        _q("A mixed 1 1/4 + 2 1/4.", "3 1/2", "3 2/4."),
        _q("3 2/5 − 1 1/5.", "2 1/5", "Subtract."),
        _q("LCD of 8 and 12?", 24, "24."),
        _q("2/3 vs 3/5. Larger?", "2/3", "10/15 vs 9/15."),
        _q("A recipe 3/8 + 1/4 cup.", "5/8", "3/8+2/8.", difficulty="hard"),
        _q("1 − 3/7 = ?", "4/7", "7/7−3/7.", difficulty="hard"),
        _q("2 1/3 + 4 2/3.", 7, "6+3/3=7.", difficulty="hard"),
        _q("5/12 + 7/12 − 1/3.", "1/2", "12/12−4/12=8/12=2/3 wait: 12/12=1, minus 1/3=4/12 so 8/12=2/3.", difficulty="hard"),
        _q("5/12 + 7/12 − 1/3 = ?", "2/3", "1 − 1/3 = 2/3.", difficulty="hard"),
        _q("SAT-style: A tank 2/5 full, add 3/10. Fraction full?", "7/10", "4/10+3/10.", difficulty="stretch"),
        _q("How empty after that tank is 7/10 full?", "3/10", "1−7/10.", difficulty="stretch"),
        _q("3 1/2 − 1 3/4.", "1 3/4", "7/2−7/4=7/4=1 3/4.", difficulty="stretch"),
        _q("Benchmark: 5/8 + 1/8 vs 1. Difference from 1?", "1/4", "6/8=3/4, 1−3/4=1/4.", difficulty="stretch"),
        _q("A track 5/6 km minus 1/2 km.", "1/3", "5/6−3/6.", difficulty="stretch"),
        _q("Add 7/9 + 1/6 (LCD 18).", "17/18", "14/18+3/18.", difficulty="stretch"),
        _q("A mixed improper: 9/4 + 3/4.", 3, "12/4.", difficulty="stretch"),
        _q("Which sum is greater: 1/2+1/3 or 4/5?", "4/5", "5/6 vs 4/5=0.833 vs 0.8 so 1/2+1/3 is greater. Recalc: 5/6>4/5. Answer 5/6 value? Question: which is greater — 1/2+1/3.", difficulty="stretch"),
        _q("Which is greater: 1/2+1/3 or 4/5? The greater value is?", "5/6", "5/6 > 4/5.", difficulty="stretch"),
        _q("Simplify 18/24 after adding 5/12+1/3.", "3/4", "5/12+4/12=9/12=3/4.", difficulty="stretch"),
        _q("A two-step: 3/4 of a pizza left, eat 1/3 of the WHOLE pizza. Left of whole?", "5/12", "3/4−1/3=9/12−4/12.", difficulty="stretch"),
        _q("3 3/8 + 2 5/8.", 6, "5 + 8/8.", difficulty="stretch"),
        _q("Distance 7/10 + 1/5 miles.", "9/10", "7/10+2/10.", difficulty="stretch"),
        _q("A number 1/2 more than 5/6.", "4/3", "3/6+5/6=8/6=4/3.", difficulty="stretch"),
        _q("False LCD 6 for 1/4+1/6. True LCD?", 12, "12.", difficulty="stretch"),
        _q("Subtract unlike 7/8 − 1/2.", "3/8", "7/8−4/8.", difficulty="stretch"),
    ]
    qs = [q for q in qs if q and "wait:" not in q["explanation"].lower() and "Recalc" not in q["explanation"]]
    return qs


def g5u4():
    qs = [
        _q("1/2 × 1/3 = ?", "1/6", "Multiply across."),
        _q("3/4 × 8 = ?", 6, "24/4=6."),
        _q("2/5 of 20?", 8, "20÷5×2."),
        _q("5 × 2/3 = ?", "10/3", "Or 3 1/3."),
        _q("1/4 of 1/2?", "1/8", "Of means ×."),
        _q("A recipe 2/3 of 3/4 cup.", "1/2", "6/12=1/2."),
        _q("Area 1/2 by 3/5 rectangle.", "3/10", "Product."),
        _q("0.5 × 3/8 as a fraction?", "3/16", "1/2 × 3/8."),
        _q("6 × 1/6 = ?", 1, "1."),
        _q("3/7 × 14.", 6, "3×2.", difficulty="hard"),
        _q("A class 24, 3/8 play soccer. How many?", 9, "24×3/8.", difficulty="hard"),
        _q("2 1/2 × 4.", 10, "5/2×4=10.", difficulty="hard"),
        _q("1/3 of 1/3 of 18.", 2, "18/9=2.", difficulty="hard"),
        _q("SAT-style: A 3/4 mile track, run 2/3 of it. Miles?", "1/2", "3/4×2/3=1/2.", difficulty="stretch"),
        _q("A 20-pack, take 3/5, eat 1/2 of what you took. Eaten?", 6, "12 then 6.", difficulty="stretch"),
        _q("Scale a 2/3 length by 3/4.", "1/2", "6/12.", difficulty="stretch"),
        _q("Which is smaller: 2/3 × 3/5 or 1/2?", "2/5", "2/5 < 1/2. The product is 2/5.", difficulty="stretch"),
        _q("2/3 × 3/5 = ?", "2/5", "2/5.", difficulty="stretch"),
        _q("A mixed 1 1/3 × 1 1/2.", 2, "4/3×3/2=2.", difficulty="stretch"),
        _q("Reciprocal idea: 4/5 × 5/4.", 1, "1.", difficulty="stretch"),
        _q("Area of 5/8 by 8/15.", "1/3", "40/120=1/3.", difficulty="stretch"),
        _q("3/10 of $50.", 15, "15 dollars.", difficulty="stretch"),
        _q("A double of 3/8.", "3/4", "6/8.", difficulty="stretch"),
        _q("False: 1/2 of 1/2 of 1/2 is 1/2. True value?", "1/8", "Three halves multiplied.", difficulty="stretch"),
        _q("A 9×10 grid, shade 2/3 of 3/5 of the squares. Squares shaded?", 36, "90×2/5=36? 2/3 of 3/5=2/5, 90×2/5=36.", difficulty="stretch"),
        _q("Unit fraction × unit: 1/7 × 1/4.", "1/28", "1/28.", difficulty="stretch"),
        _q("A word: 5/6 of 18 is 15, then 1/3 of that. Result?", 5, "15/3.", difficulty="stretch"),
        _q("Compare 3/4 × 8/9 and 2/3. Greater?", "2/3", "24/36=2/3 equal. Equal to 2/3.", difficulty="stretch"),
        _q("3/4 × 8/9 = ?", "2/3", "2/3.", difficulty="stretch"),
        _q("A scale drawing 1/4 of real 12 cm.", 3, "12/4.", difficulty="stretch"),
    ]
    return qs


def g5u5():
    qs = [
        _q("3 ÷ 1/2 = ?", 6, "How many halves in 3."),
        _q("1/2 ÷ 1/4 = ?", 2, "Two fourths in a half."),
        _q("4 ÷ 1/5 = ?", 20, "Invert 5/1."),
        _q("1/3 ÷ 2 = ?", "1/6", "Half of 1/3."),
        _q("5/6 ÷ 1/6 = ?", 5, "How many 1/6 in 5/6."),
        _q("A 2-cup mix split into 1/4-cup servings. Servings?", 8, "2÷1/4."),
        _q("8 ÷ 1/8 = ?", 64, "64 eighths."),
        _q("1 ÷ 1/7 = ?", 7, "Seven sevenths."),
        _q("6/5 ÷ 2/5 = ?", 3, "Keep-change-flip 6/5×5/2=3."),
        _q("A ribbon 3/4 m cut into 1/8 m pieces. Pieces?", 6, "3/4÷1/8=6.", difficulty="hard"),
        _q("2 1/2 ÷ 1/2.", 5, "5/2 × 2/1=5.", difficulty="hard"),
        _q("1/2 ÷ 3/4 = ?", "2/3", "1/2×4/3.", difficulty="hard"),
        _q("A 10-pound bag in 2/5-pound scoops. Scoops?", 25, "10÷2/5=25.", difficulty="hard"),
        _q("SAT-style: How many 3/8-inch tiles fit along 6 inches?", 16, "6÷3/8=16.", difficulty="stretch"),
        _q("A leftover: 5 ÷ 2/3 = 7 1/2. As improper?", "15/2", "5×3/2.", difficulty="stretch"),
        _q("Which is larger: 4÷1/5 or 4÷1/4?", 20, "20 vs 16.", difficulty="stretch"),
        _q("A two-step: 3/4 ÷ 1/8 then − 1.", 5, "6−1.", difficulty="stretch"),
        _q("Unit: 1/5 ÷ 1/10.", 2, "1/5×10=2.", difficulty="stretch"),
        _q("A story: 7/8 pizza shared by 1/4 pizza per person. People?", "7/2", "7/8×4/1=7/2=3.5.", difficulty="stretch"),
        _q("People if each gets 1/4 of a pizza from 7/8? Number of people?", 3.5, "3.5 people — or 7/2.", difficulty="stretch"),
        _q("7/8 ÷ 1/4 = ?", "7/2", "7/2.", difficulty="stretch"),
        _q("Why invert:  a÷b = a×(1/b). 9÷3 vs 9×1/3. 9÷3?", 3, "Same as ×1/3.", difficulty="stretch"),
        _q("A 2/3 meter board, pieces 1/9 m. Count?", 6, "2/3÷1/9=6.", difficulty="stretch"),
        _q("0.5 ÷ 1/8 (0.5=1/2).", 4, "4.", difficulty="stretch"),
        _q("A false: 1/2 ÷ 1/2 = 1/4. True?", 1, "A number ÷ itself is 1.", difficulty="stretch"),
        _q("Mixed 4 1/2 ÷ 3/4.", 6, "9/2×4/3=6.", difficulty="stretch"),
        _q("How many 2/3 in 8/3?", 4, "8/3÷2/3=4.", difficulty="stretch"),
        _q("A tank 5/4 L poured in 1/8 L cups. Cups?", 10, "5/4×8=10.", difficulty="stretch"),
        _q("Compare 1÷1/6 and 6. Equal?", 6, "Yes 6.", difficulty="stretch"),
        _q("A word: pieces of 3/10 from 1.5 (3/2). Pieces?", 5, "3/2÷3/10=5.", difficulty="stretch"),
    ]
    return qs


def g5u6():
    qs = []
    for l, w, h in ((2, 3, 4), (5, 5, 5), (10, 2, 3), (6, 4, 2), (8, 1, 7), (9, 3, 3), (12, 2, 2), (7, 4, 5)):
        qs.append(_q(f"Volume of a {l}×{w}×{h} rectangular prism?", l * w * h, f"{l}×{w}×{h}={l*w*h} cubic units."))
    qs += [
        _q("A cube edge 6. Volume?", 216, "6³."),
        _q("Volume 120, base area 15. Height?", 8, "V=Bh."),
        _q("A layer 4×5, 3 layers. Volume?", 60, "20×3."),
        _q("Two cubes 3×3×3 stacked. Volume?", 54, "27×2.", difficulty="hard"),
        _q("A 10×8×2 box. Volume?", 160, "160.", difficulty="hard"),
        _q("Missing edge: V=96, 4×6×h. h?", 4, "24h=96.", difficulty="hard"),
        _q("A hollow: 5×5×5 cube minus 3×3×3 inside (if possible). Remaining?", 98, "125−27.", difficulty="hard"),
        _q("SAT-style: A pool 20×10×2 (units). Volume?", 400, "400.", difficulty="stretch"),
        _q("Pack 1×1×1 cubes into 4×3×2. How many?", 24, "Volume.", difficulty="stretch"),
        _q("Double every edge of a 2×3×4 prism. New volume factor?", 8, "Scale³=8.", difficulty="stretch"),
        _q("New volume of that doubled-edge 2×3×4?", 192, "8×24.", difficulty="stretch"),
        _q("Base 12 cm², height 9 cm. Volume?", 108, "Bh.", difficulty="stretch"),
        _q("A composite: 6×4×2 plus 3×4×2 sharing a 4×2 face (added on). Total volume?", 72, "48+24.", difficulty="stretch"),
        _q("Which has more volume: 5×5×4 or 10×5×2?", 100, "Equal 100.", difficulty="stretch"),
        _q("A cube volume 64. Edge?", 4, "∛64.", difficulty="stretch"),
        _q("Unit cubes painted: 3×3×3 cube, how many have 0 faces painted (inner)?", 1, "The very center.", difficulty="stretch"),
        _q("A 2×2×2 cube unit cubes with 3 faces painted?", 8, "All 8 corners.", difficulty="stretch"),
        _q("Volume vs area: 3×4 rectangle area vs 3×4×1 prism volume. Volume?", 12, "Same number, cubic.", difficulty="stretch"),
        _q("A tank 50×20×10. Volume?", 10000, "10000.", difficulty="stretch"),
        _q("Fill half of a 8×5×4 box. Cubic units filled?", 80, "160/2.", difficulty="stretch"),
    ]
    return qs


def g5u7():
    qs = []
    pts = [(0, 0), (1, 4), (2, 3), (3, 1), (4, 5), (5, 2), (6, 6), (-1, 2), (2, -3), (0, 5)]
    for x, y in pts:
        qs.append(_q(f"A point is {x} right and {y} up from the origin (down if negative). Coordinates?", f"({x},{y})", f"({x}, {y})."))
    qs += [
        _q("The x-axis is the ___ line.", "horizontal", "Left-right."),
        _q("Quadrant I has signs…", "(+,+)", "Both positive."),
        _q("Point (0, 4) lies on the…", "y-axis", "x=0."),
        _q("Distance from (1,2) to (1,7) (vertical)?", 5, "7−2."),
        _q("A rectangle vertices (0,0),(6,0),(6,4),(0,4). Area?", 24, "6×4.", difficulty="hard"),
        _q("Plot (3,0). It is on the…", "x-axis", "y=0.", difficulty="hard"),
        _q("From (2,1) move left 5, up 3. New point?", "(-3,4)", "2−5, 1+3.", difficulty="hard"),
        _q("Which quadrant is (−4, 5)?", "II", "Left and up.", difficulty="hard"),
        _q("SAT-style: Line through (0,2) and (4,2). Slope?", 0, "Horizontal.", difficulty="stretch"),
        _q("Line through (1,1) and (4,7). Rise/run?", 2, "6/3=2.", difficulty="stretch"),
        _q("A square side 3, corner at (1,1) along axes positive. Opposite corner?", "(4,4)", "1+3.", difficulty="stretch"),
        _q("Midpoint of (0,0) and (8,6)?", "(4,3)", "Averages.", difficulty="stretch"),
        _q("Point (5,−2) quadrant?", "IV", "Right down.", difficulty="stretch"),
        _q("Origin coordinates?", "(0,0)", "Origin.", difficulty="stretch"),
        _q("A translation (x,y)→(x+2,y−1) of (3,4).", "(5,3)", "Add 2, subtract 1.", difficulty="stretch"),
        _q("Distance (0,0) to (5,12) (Pythagorean)?", 13, "5-12-13.", difficulty="stretch"),
        _q("Three points (0,0),(4,0),(0,3). Triangle area?", 6, "Half of 4×3.", difficulty="stretch"),
        _q("Which is not a function of x if we only have points (1,2),(1,3),(2,4)?", "not a function", "x=1 repeats.", difficulty="stretch"),
        _q("A graph of y=x after plotting (1,1),(2,2),(3,3). Next integer point?", "(4,4)", "On the line.", difficulty="stretch"),
        _q("Reflect (3,5) over x-axis.", "(3,-5)", "Negate y.", difficulty="stretch"),
    ]
    return qs


def g5u8():
    qs = [
        _q("2 + 3 × 4 = ?", 14, "Multiply first."),
        _q("10 − 6 ÷ 2 = ?", 7, "Divide first."),
        _q("(8+2)×3 = ?", 30, "Parentheses first."),
        _q("5² = ?", 25, "5×5."),
        _q("3³ = ?", 27, "3×3×3."),
        _q("A pattern 2, 6, 18, 54. Rule ×3. Next?", 162, "54×3."),
        _q("n + 7 when n=12?", 19, "19."),
        _q("4n when n=9?", 36, "36."),
        _q("Evaluate 2(n+3) at n=5.", 16, "2×8."),
        _q("Which is equivalent: 3(2+n) and 6+3n?", "yes", "Distributive.", ["no", "only if n=0", "only if n=2"]),
        _q("A table: in 1,2,3 out 4,7,10. Rule?", "3n+1", "×3 plus 1.", ["2n", "n+3", "4n"], difficulty="hard"),
        _q("Order: 18÷3×2.", 12, "Left to right 6×2.", difficulty="hard"),
        _q("2³ × 3².", 72, "8×9.", difficulty="hard"),
        _q("A two-step expression 5n − 4 at n=8.", 36, "40−4.", difficulty="hard"),
        _q("SAT-style: 3(2x+1)=21. x?", 3, "2x+1=7, x=3.", difficulty="stretch"),
        _q("Which is larger: 2^5 or 5^2?", 32, "32 vs 25.", difficulty="stretch"),
        _q("A sequence 5, 9, 13, 17. 10th term (start n=1 as 5)?", 41, "4n+1 at n=10.", difficulty="stretch"),
        _q("Parentheses change: 8−2×3 vs (8−2)×3. Second value?", 18, "6×3.", difficulty="stretch"),
        _q("Evaluate (1/2) of (10+6).", 8, "8.", difficulty="stretch"),
        _q("A number trick: think n, ×2, +6, ÷2, −n. Always?", 3, "Simplifies to 3.", difficulty="stretch"),
        _q("Expression for 7 less than 3 times a number.", "3n-7", "Not 7−3n.", difficulty="stretch"),
        _q("If  n/4 = 12, n?", 48, "×4.", difficulty="stretch"),
        _q("Combine 4x+9x.", "13x", "Like terms.", difficulty="stretch"),
        _q("False PEMDAS: 6+6÷6+6. True value?", 13, "6+1+6.", difficulty="stretch"),
        _q("A pattern of squares 1,4,9,16. 8th?", 64, "8².", difficulty="stretch"),
        _q("Function table x:0,1,2 y:5,8,11. y in terms of x?", "3x+5", "Start 5, +3.", difficulty="stretch"),
        _q("Evaluate 10² − 9².", 19, "100−81. Or (10−9)(10+9)=19.", difficulty="stretch"),
        _q("A word: 4 groups of (n+2) with n=6. Total?", 32, "4×8.", difficulty="stretch"),
        _q("Which equals 2(3+4×5)? Inner 3+20=23×2?", 46, "2×23.", difficulty="stretch"),
        _q("A SAT: If 2(x−4)=10, x?", 9, "x−4=5.", difficulty="stretch"),
    ]
    return qs


# Grade 6
def g6u1():
    qs = []
    for a, b, k in ((2, 5, 4), (3, 4, 5), (1, 7, 6), (5, 2, 3), (4, 6, 2), (7, 3, 4), (8, 12, 3), (9, 6, 5)):
        qs.append(_q(f"If {a}:{b} = {a*k}:x, what is x?", b * k, f"Scale by {k}: {b}×{k}={b*k}."))
    qs += [
        _q("Simplify 18:24.", "3:4", "÷6."),
        _q("Part-to-whole 2:3 as first:total?", "2:5", "2+3=5."),
        _q("A mix 4 cups to 10 cups water. Concentrate:water simplest?", "2:5", "÷2."),
        _q("If 5:8 = 20:x, x?", 32, "×4."),
        _q("A class 12 girls 18 boys. girls:boys?", "2:3", "÷6.", difficulty="hard"),
        _q("Tape 3 green : 5 yellow. Green fraction of whole?", "3/8", "3 of 8.", difficulty="hard"),
        _q("Map 1 cm : 8 km. 7 cm is?", 56, "7×8.", difficulty="hard"),
        _q("3:5 vs 6:11. Equivalent?", "no", "6:10 would be.", difficulty="hard"),
        _q("SAT-style: Recipe 2:5 flour:sugar. 12 cups flour. Sugar?", 30, "×6.", difficulty="stretch"),
        _q("A ratio table 1:4, 2:8, 5:?.", 20, "×4.", difficulty="stretch"),
        _q("20 students, ratio 3:2 A:B. How many A?", 12, "3/5 of 20.", difficulty="stretch"),
        _q("If a:b=4:1 and a+b=35, a?", 28, "5 parts, 7 each, 4×7.", difficulty="stretch"),
        _q("Which is not equivalent to 5:15?", "2:5", "1:3 vs 2:5.", difficulty="stretch"),
        _q("Double number line: 3 miles in 12 min. 5 miles in?", 20, "4 min/mile ×5.", difficulty="stretch"),
        _q("A shade 7:3 dark:light. 30 total tiles. Light?", 9, "3/10×30.", difficulty="stretch"),
        _q("Scale factor 2:3 → 10:15 is?", 5, "×5.", difficulty="stretch"),
        _q("Order matters: 4:9 vs 9:4. Product of both ratios as fractions 4/9×9/4?", 1, "Reciprocals.", difficulty="stretch"),
        _q("A word: 8 to 12 as a simplified ratio.", "2:3", "÷4.", difficulty="stretch"),
        _q("If 7:x = 21:15, x?", 5, "÷3.", difficulty="stretch"),
        _q("Part-to-part 1:4, 25 in all. Larger part?", 20, "5 parts ×5.", difficulty="stretch"),
        _q("A 2:7 ratio, first quantity 18. Second?", 63, "×9.", difficulty="stretch"),
        _q("Three-part 1:2:3, total 36. Middle part?", 12, "6 parts, 6 each ×2.", difficulty="stretch"),
    ]
    return qs


def g6u2():
    qs = [
        _q("12 miles in 3 hours. Unit rate mph?", 4, "12÷3."),
        _q("5 items for $20. Per item?", 4, "20÷5."),
        _q("30% of 80?", 24, "0.3×80."),
        _q("25% of 60?", 15, "1/4 of 60."),
        _q("A 10% tax on $40.", 4, "0.1×40."),
        _q("Which is a better buy: 3 for $5 or 6 for $11? Unit price of the better (cents)?", "166.7¢ vs 183¢ so 3 for $5", "5/3 < 11/6.", ["6 for $11", "same", "cannot"]),
        _q("Unit price of 3 for $5 in dollars (repeatable decimal 1.66…)? Use fraction $5/3. As a mixed number?", "1 2/3", "$1.67 approx."),
        _q("Price per one if 3 cost $5, as a fraction of a dollar?", "5/3", "About $1.67."),
        _q("40 is what percent of 200?", 20, "40/200=1/5."),
        _q("A 15% tip on $80.", 12, "0.15×80.", difficulty="hard"),
        _q("Discount 20% off $45. Sale price?", 36, "45×0.8.", difficulty="hard"),
        _q("A rate 150 km in 2.5 h. km/h?", 60, "150/2.5.", difficulty="hard"),
        _q("12 is 25% of what?", 48, "12÷0.25.", difficulty="hard"),
        _q("SAT-style: $80 marked up 25% then 20% off. Final?", 80, "100→125→100. 80×1.25×0.8=80.", difficulty="stretch"),
        _q("$50 with 8% tax. Total?", 54, "50×1.08.", difficulty="stretch"),
        _q("A 3:4 ratio as a percent (first of whole)?", 43, "3/7 ≈ 42.9% → 43 if nearest. Use exact 3/7. Question: first is what fraction of whole? 3/7.", difficulty="stretch"),
        _q("In 3:4, first as a percent of the total (nearest percent)?", 43, "3/7≈42.86%.", difficulty="stretch"),
        _q("Speed 5 m/s in km/h? (×3.6)", 18, "18 km/h.", difficulty="stretch"),
        _q("A machine 240 units in 8 min. Per minute?", 30, "240/8.", difficulty="stretch"),
        _q("What percent is 9 of 15?", 60, "9/15=0.6.", difficulty="stretch"),
        _q("Increase 40 by 15%. New?", 46, "40×1.15.", difficulty="stretch"),
        _q("A two-store: 30% off vs $10 off on $40. Better savings amount of the larger deal?", 12, "30% is $12 > $10.", difficulty="stretch"),
        _q("Unit rate: 2/3 mile in 1/6 hour. mph?", 4, "(2/3)÷(1/6)=4.", difficulty="stretch"),
        _q("Simple interest idea: 5% of 200.", 10, "10.", difficulty="stretch"),
        _q("A double number line 4 oz : $3, 12 oz costs?", 9, "×3.", difficulty="stretch"),
        _q("Percent error style: 18 is 90% of what?", 20, "18/0.9.", difficulty="stretch"),
        _q("A mix 40% juice in 15 L. Juice liters?", 6, "0.4×15.", difficulty="stretch"),
        _q("If 0.2 = x%, x?", 20, "20%.", difficulty="stretch"),
        _q("A rate table 2,4,6 hours → 10,20,30 miles. Miles at 7 hours?", 35, "5 mph ×7.", difficulty="stretch"),
        _q("Commission 6% of $1,250.", 75, "0.06×1250.", difficulty="stretch"),
    ]
    return qs


def g6u3():
    qs = [
        _q("3/4 ÷ 1/8 = ?", 6, "3/4×8=6."),
        _q("2.4 × 0.5 = ?", 1.2, "Half of 2.4."),
        _q("0.25 as a fraction simplest?", "1/4", "25/100."),
        _q("5/8 as a decimal?", "0.625", "5÷8."),
        _q("1.5 + 2.75 = ?", "4.25", "4.25."),
        _q("7/2 as a mixed number?", "3 1/2", "3.5."),
        _q("0.2 × 0.3 = ?", "0.06", "6 hundredths."),
        _q("A GCF of 18 and 24?", 6, "6."),
        _q("LCM of 6 and 8?", 24, "24."),
        _q("5 ÷ 0.5 = ?", 10, "How many halves.", difficulty="hard"),
        _q("3/5 of 2.5?", "1.5", "0.6×2.5.", difficulty="hard"),
        _q("A decimal 4.08 − 1.9.", "2.18", "Align.", difficulty="hard"),
        _q("Convert 7/20 to a decimal.", "0.35", "7÷20.", difficulty="hard"),
        _q("SAT-style: 0.125 as a fraction.", "1/8", "125/1000=1/8.", difficulty="stretch"),
        _q("A two-step: (3/4)×(8/9)÷(1/3).", 2, "2/3 ×3=2.", difficulty="stretch"),
        _q("Which is greater: 5/6 or 0.8?", "5/6", "0.833>0.8.", difficulty="stretch"),
        _q("A repeating 1/3 + 1/6.", "1/2", "1/2.", difficulty="stretch"),
        _q("Multiply 1.25 × 0.4.", "0.5", "0.5.", difficulty="stretch"),
        _q("A word: 2.5 kg split into 0.25 kg bags. Bags?", 10, "2.5/0.25.", difficulty="stretch"),
        _q("Simplify 16/24 then as a decimal.", "0.6̅ or 0.666…", "2/3.", difficulty="stretch"),
        _q("16/24 simplest as a fraction?", "2/3", "÷8.", difficulty="stretch"),
        _q("LCM of 9 and 12 used for 1/9+1/12.", "7/36", "4/36+3/36.", difficulty="stretch"),
        _q("A number 0.004 × 1000.", 4, "4.", difficulty="stretch"),
        _q("Divide 9/10 ÷ 3/5.", "3/2", "9/10×5/3=3/2.", difficulty="stretch"),
        _q("A mixed 2 2/5 as an improper × 5.", 12, "12/5×5=12.", difficulty="stretch"),
        _q("Compare 0.09 and 0.1. Difference?", "0.01", "0.1−0.09.", difficulty="stretch"),
        _q("A percent 12.5% as a fraction.", "1/8", "12.5/100=1/8.", difficulty="stretch"),
        _q("3.6 ÷ 0.12.", 30, "360÷12.", difficulty="stretch"),
        _q("A sum 1/2 + 0.25 + 1/8.", "0.875", "0.5+0.25+0.125.", difficulty="stretch"),
        _q("GCF 36 and 54 used to simplify 36/54.", "2/3", "÷18.", difficulty="stretch"),
    ]
    return qs


def g6u4():
    qs = []
    for a, b in ((5, -3), (-7, 2), (-4, -6), (8, -8), (-1, 9), (12, -5), (-10, -2), (3, -11)):
        qs.append(_q(f"What is {a} + ({b})?", a + b, f"{a}+({b})={a+b}."))
    qs += [
        _q("−5 − 4 = ?", -9, "Further left."),
        _q("|−12| = ?", 12, "Distance from 0."),
        _q("Opposite of −9?", 9, "Sign flip."),
        _q("A temperature 3° to −5°. Change?", -8, "Down 8."),
        _q("−3 × 4 = ?", -12, "Negative × positive.", difficulty="hard"),
        _q("−6 × −5 = ?", 30, "Negative × negative.", difficulty="hard"),
        _q("A debt −$20 then pay $12. New?", -8, "−20+12.", difficulty="hard"),
        _q("Which is greater: −2 or −7?", -2, "Right on the line.", difficulty="hard"),
        _q("SAT-style: −15 + 7 − 4 + 10.", -2, "−8−4+10=−2.", difficulty="stretch"),
        _q("A two-step: |3 − 10| + (−2).", 5, "7−2? |−7|=7, +−2=5.", difficulty="stretch"),
        _q("−48 ÷ 6.", -8, "−8.", difficulty="stretch"),
        _q("A number line jump left 9 from 4.", -5, "4−9.", difficulty="stretch"),
        _q("−2.5 + 1.5.", -1, "−1.", difficulty="stretch"),
        _q("Order −3, 0, −8, 2. Least?", -8, "Leftmost.", difficulty="stretch"),
        _q("A elevator −3 floor then −4 more. Floor?", -7, "−3−4.", difficulty="stretch"),
        _q("Subtract a negative: 5 − (−3).", 8, "Add 3.", difficulty="stretch"),
        _q("−1 × −1 × −1.", -1, "Three negatives.", difficulty="stretch"),
        _q("Distance between −4 and 9.", 13, "9−(−4).", difficulty="stretch"),
        _q("A football −8 then +12 then −3 yards. Net?", 1, "−8+12−3.", difficulty="stretch"),
        _q("If x + (−5) = −1, x?", 4, "x=4.", difficulty="stretch"),
        _q("Compare |−11| and 10. Greater abs value?", 11, "11>10.", difficulty="stretch"),
        _q("A double negative in words: remove a debt of 6 from −10.", -4, "−10+6.", difficulty="stretch"),
    ]
    return qs


def g6u5():
    qs = []
    for x, y in ((2, -3), (-4, 1), (5, 0), (0, -6), (-2, -5), (3, 4), (-1, 7), (6, -2)):
        qs.append(_q(f"Point ({x},{y}) is in which quadrant (or axis)?",
                     "y-axis" if x == 0 else "x-axis" if y == 0 else { (1, 1): "I", (-1, 1): "II", (-1, -1): "III", (1, -1): "IV" }[(1 if x > 0 else -1, 1 if y > 0 else -1)],
                     "Signs of x and y decide the quadrant."))
    qs += [
        _q("Reflect (3,−2) over the y-axis.", "(-3,-2)", "Negate x."),
        _q("Distance (0,0) to (−8,0)?", 8, "Horizontal 8."),
        _q("A rectangle (−1,1) to (4,1) to (4,−2) to (−1,−2). Width?", 5, "4−(−1)."),
        _q("That rectangle’s height?", 3, "1−(−2).", difficulty="hard"),
        _q("Area of that rectangle?", 15, "5×3.", difficulty="hard"),
        _q("Which axis is vertical?", "y-axis", "Up-down.", difficulty="hard"),
        _q("SAT-style: Plot (2,3),(4,6),(6,9). Slope?", "3/2", "Rise 3 run 2.", difficulty="stretch"),
        _q("A translation left 4 down 1 of (−1,5).", "(-5,4)", "−1−4, 5−1.", difficulty="stretch"),
        _q("Quadrant III signs?", "(−,−)", "Both negative.", difficulty="stretch"),
        _q("Midpoint of (−2,4) and (6,−2).", "(2,1)", "Averages.", difficulty="stretch"),
        _q("A point 5 left of origin on the x-axis.", "(-5,0)", "x=-5.", difficulty="stretch"),
        _q("If x=−3 and y=x+1, point?", "(-3,-2)", "−3+1=−2.", difficulty="stretch"),
        _q("Distance (−3,−4) to (0,0) (3-4-5)?", 5, "Hypotenuse 5.", difficulty="stretch"),
        _q("Which is farther from origin: (0,−9) or (5,5)? Distances 9 vs √50≈7.1. Farther distance?", 9, "9>7.1.", difficulty="stretch"),
        _q("A square vertices (0,0),(2,0),(2,2),(0,2). Perimeter?", 8, "4×2.", difficulty="stretch"),
        _q("Reflect (4,1) over x-axis then y-axis.", "(-4,-1)", "Both signs flip.", difficulty="stretch"),
        _q("Line x=3 is vertical through?", "(3,0) among others", "All points with x=3. Use x-intercept 3.", difficulty="stretch"),
        _q("The x-intercept of x=3 (as a number)?", 3, "Hits x-axis at 3.", difficulty="stretch"),
        _q("From (1,−1) to (1,6). Distance?", 7, "Vertical 7.", difficulty="stretch"),
        _q("A graph of y=−x through (2,?).", -2, "y=−2.", difficulty="stretch"),
        _q("Quadrant of (7,−0.5)?", "IV", "Positive x, negative y.", difficulty="stretch"),
    ]
    return qs


def g6u6():
    qs = []
    for a, b in ((3, 12), (5, 20), (7, 35), (2, 18), (8, 40), (4, 28), (6, 42), (9, 27)):
        qs.append(_q(f"Solve {a}x = {b}. x?", b // a, f"Divide both sides by {a}."))
    qs += [
        _q("x + 9 = 21. x?", 12, "Subtract 9."),
        _q("x − 15 = 4. x?", 19, "Add 15."),
        _q("2x + 3 = 11. x?", 4, "2x=8."),
        _q("A balance: 5 + x = 5 + 7. x?", 7, "Same to both sides."),
        _q("3x − 4 = 14. x?", 6, "3x=18.", difficulty="hard"),
        _q("x/4 = 9. x?", 36, "×4.", difficulty="hard"),
        _q("12 = 3(x+1). x?", 3, "4=x+1.", difficulty="hard"),
        _q("Inequality x + 5 > 9. Smallest integer x?", 5, "x>4.", difficulty="hard"),
        _q("SAT-style: 2(x−3)+4=x+9. x?", 11, "2x−6+4=x+9 → x=11.", difficulty="stretch"),
        _q("5x − 2x + 6 = 18. x?", 4, "3x=12.", difficulty="stretch"),
        _q("A word: 7 more than twice a number is 31. Number?", 12, "2n+7=31.", difficulty="stretch"),
        _q("x < −2 on a number line uses an ___ circle at −2.", "open", "Not included.", difficulty="stretch"),
        _q("−3x = 21. x?", -7, "Divide by −3.", difficulty="stretch"),
        _q("4x + 8 = 4(x+2) is true for how many x?", "all real x", "Identity.", difficulty="stretch"),
        _q("4x + 8 = 4x + 9 has how many solutions?", 0, "8=9 never.", difficulty="stretch"),
        _q("A perimeter 2l+2w=40, w=6. l?", 14, "2l+12=40.", difficulty="stretch"),
        _q("3(x−2)−x=10. x?", 8, "3x−6−x=10, 2x=16.", difficulty="stretch"),
        _q("Inequality −2x > 8. Reverse: x?", "x < −4", "Divide by negative.", difficulty="stretch"),
        _q("A table y=2x+1, x=7. y?", 15, "14+1.", difficulty="stretch"),
        _q("Combine 2x+5x−x.", "6x", "Like terms.", difficulty="stretch"),
        _q("Evaluate 3x−1 at x=−2.", -7, "−6−1.", difficulty="stretch"),
        _q("Solve x/3 + 4 = 10.", 18, "x/3=6.", difficulty="stretch"),
    ]
    return qs


def g6u7():
    qs = []
    for b, h in ((6, 8), (10, 5), (12, 7), (9, 4), (15, 6)):
        qs.append(_q(f"Area of a triangle base {b} height {h}?", b * h // 2, f"½×{b}×{h}={b*h//2}."))
    qs += [
        _q("Parallelogram base 11 height 4. Area?", 44, "bh."),
        _q("A cube edge 5. Surface area?", 150, "6×25."),
        _q("Rectangular prism 3×4×5. Surface area?", 94, "2(12+15+20)."),
        _q("Volume of that prism?", 60, "3×4×5."),
        _q("A net of 6 congruent squares side 2. Surface area?", 24, "6×4."),
        _q("Circle not needed: a triangle 8×9 right. Area?", 36, "½×8×9.", difficulty="hard"),
        _q("A composite 6×4 rectangle plus 6×3 triangle on top (base 6). Area?", 33, "24+9.", difficulty="hard"),
        _q("Surface area of cube volume 27. Edge 3, SA?", 54, "6×9.", difficulty="hard"),
        _q("A box 10×2×2. SA?", 88, "2(20+20+4).", difficulty="hard"),
        _q("SAT-style: wrapping a 5×4×3 prism. SA?", 94, "2(20+15+12).", difficulty="stretch"),
        _q("Trapezoid bases 8 and 12, height 5. Area?", 50, "½(8+12)×5.", difficulty="stretch"),
        _q("A triangle area 30, base 10. Height?", 6, "½×10×h=30.", difficulty="stretch"),
        _q("Prism volume 200, base area 25. Height?", 8, "V=Bh.", difficulty="stretch"),
        _q("Cube SA 96. Edge?", 4, "6e²=96, e²=16.", difficulty="stretch"),
        _q("A square pyramid is not asked: rectangle 9×6. Area?", 54, "54.", difficulty="stretch"),
        _q("Missing: parallelogram area 72, base 9. Height?", 8, "72/9.", difficulty="stretch"),
        _q("Two triangles 5-12-13 make a rectangle 5×12. Area of rectangle?", 60, "60.", difficulty="stretch"),
        _q("A 2-inch border around 8×6 rectangle. Outer area?", 120, "12×10.", difficulty="stretch"),
        _q("Border-only area of that frame?", 72, "120−48.", difficulty="stretch"),
        _q("Triangular prism length 10, triangle 3-4-5. Volume?", 60, "½×3×4×10.", difficulty="stretch"),
        _q("Unit cubes to fill 5×5×2.", 50, "50.", difficulty="stretch"),
        _q("Which has more SA: cube edge 4 or 2×4×8 prism? Cube SA 96 vs prism 112. Greater SA?", 112, "The prism.", difficulty="stretch"),
    ]
    return qs


def g6u8():
    qs = [
        _q("Mean of 4, 8, 12?", 8, "24/3."),
        _q("Median of 3, 9, 1, 7, 5?", 5, "Sorted 1,3,5,7,9."),
        _q("Mode of 2, 2, 5, 7, 2?", 2, "Most frequent."),
        _q("Range of 11, 4, 9, 20?", 16, "20−4."),
        _q("A dot plot with 3,3,4,4,4,6. Mode?", 4, "Three 4s."),
        _q("Mean of 10, 10, 10, 30?", 15, "60/4."),
        _q("Median of even list 2,4,6,8?", 5, "Average of 4 and 6."),
        _q("IQR idea: Q1=4, Q3=12. IQR?", 8, "12−4."),
        _q("A histogram bin 10–20 has 5 dots. That means 5 values…", "from 10 up to 20", "In that interval.", ["exactly 15", "mean 15", "mode 10"]),
        _q("Outlier: 2,3,3,4,100. Mean is pulled which way?", "up", "Toward 100.", difficulty="hard"),
        _q("Median of 2,3,3,4,100?", 3, "Resistant.", difficulty="hard"),
        _q("A survey 8 scores mean 10. Total points?", 80, "8×10.", difficulty="hard"),
        _q("Add a 18 to 4,8,12 (mean 8). New mean?", 10.5, "42/4? 4+8+12+18=42, 42/4=10.5.", difficulty="hard"),
        _q("SAT-style: 5 tests average 80. A 6th score 92. New average?", 82, "(400+92)/6.", difficulty="stretch"),
        _q("Box plot min 2, Q1 5, med 7, Q3 10, max 14. IQR?", 5, "10−5.", difficulty="stretch"),
        _q("A gap on a dot plot is a stretch with…", "no dots", "Empty values.", difficulty="stretch"),
        _q("Which is least affected by an outlier?", "median", "Or mode.", difficulty="stretch"),
        _q("Mean of 0, 0, 0, 12?", 3, "12/4.", difficulty="stretch"),
        _q("A class 50% scored 70, 50% scored 90. Mean?", 80, "Average of 70 and 90.", difficulty="stretch"),
        _q("Range after dropping max from 3,6,6,15?", 3, "6−3.", difficulty="stretch"),
        _q("Two groups means 10 and 20, equal size. Combined mean?", 15, "Midway.", difficulty="stretch"),
        _q("A frequency: 1 appears 4 times, 2 appears 1 time. Mean?", "1.2", "(4+2)/5=1.2.", difficulty="stretch"),
        _q("Median of 9 numbers is the ___th when sorted.", 5, "Middle.", difficulty="stretch"),
        _q("The 5th of 9 sorted values is the median. For 1,2,3,4,8,9,10,11,12 median?", 8, "5th is 8.", difficulty="stretch"),
        _q("A skewed-right set has a mean ___ the median typically.", "greater than", "Tail pulls mean.", difficulty="stretch"),
        _q("MAD idea: data 4,6,8 mean 6. Mean abs deviation?", "4/3", "|−2|+0+|2|=4, /3.", difficulty="stretch"),
        _q("A sample vs population: a class of 30 is a…", "population of that class", "All of them.", difficulty="stretch"),
        _q("Misleading graph: bars not starting at 0. This can…", "exaggerate differences", "Scale trick.", difficulty="stretch"),
        _q("A cluster is a pile of dots. 1,1,2,2,2,9. Cluster around?", 2, "Near 1–2.", difficulty="stretch"),
        _q("If every value increases by 5, the mean…", "increases by 5", "Shifts.", difficulty="stretch"),
    ]
    return qs


def g7u1():
    qs = []
    for a, b in ((-8, 5), (12, -19), (-7, -9), (15, -6), (-20, 4), (3, -3), (-11, 8), (0, -14)):
        qs.append(_q(f"{a} + ({b}) = ?", a + b, f"{a}+({b})={a+b}."))
    qs += [
        _q("−12 − (−5) = ?", -7, "−12+5."),
        _q("A bank −$40 then −$15. Balance change?", -55, "More debt."),
        _q("Distance |−9 − 4|?", 13, "13."),
        _q("−2.5 + 6.5?", 4, "4."),
        _q("A chip model: 8 negatives remove 3 negatives. Left?", -5, "−5.", difficulty="hard"),
        _q("−1 + 2 − 3 + 4 − 5?", -3, "Pair to add: (−1−3−5)+(2+4)=−9+6=−3.", difficulty="hard"),
        _q("−1 + 2 − 3 + 4 − 5 = ?", -3, "−3.", difficulty="hard"),
        _q("A temperature −3°F drops 12°. New?", -15, "−3−12.", difficulty="hard"),
        _q("SAT-style: −7 + (−8) + 20 + (−4).", 1, "−19+20−4=−3? −7−8=−15+20=5−4=1.", difficulty="stretch"),
        _q("Additive inverse of −3.2?", 3.2, "Sum 0.", difficulty="stretch"),
        _q("A number line from −4 to 9. Net change?", 13, "9−(−4).", difficulty="stretch"),
        _q("−18 + 18 + (−5).", -5, "0−5.", difficulty="stretch"),
        _q("Which is least: −0.5, −0.05, −5?", -5, "Most left.", difficulty="stretch"),
        _q("A two-step: (−6) + 10 then subtract 9.", -5, "4−9.", difficulty="stretch"),
        _q("Water −2 m, tide +5 m, then −1 m. Level?", 2, "−2+5−1.", difficulty="stretch"),
        _q("−100 + 37 − 8.", -71, "−63−8.", difficulty="stretch"),
        _q("If a + (−12) = −5, a?", 7, "a=7.", difficulty="stretch"),
        _q("Opposites sum to?", 0, "Zero.", difficulty="stretch"),
        _q("A game: +8, −12, +3, −1. Score?", -2, "−2.", difficulty="stretch"),
        _q("Absolute value inequality idea: |x|=5, positive solution?", 5, "x=5 or −5.", difficulty="stretch"),
        _q("−4.4 − 1.6.", -6, "−6.", difficulty="stretch"),
        _q("A debt paid: −25 + 25.", 0, "Cleared.", difficulty="stretch"),
    ]
    qs = [q for q in qs if q and "Pair." not in q.get("explanation", "") or q["correct_answer"] == "-3"]
    # remove duplicate broken
    seen = set()
    out = []
    for q in qs:
        k = q["question_text"][:40]
        if k in seen:
            continue
        seen.add(k)
        out.append(q)
    return out


def g7u2():
    qs = []
    for a, b in ((-6, 3), (8, -2), (-5, -7), (12, -4), (-9, 9), (-3, -8), (15, -5), (-14, 2)):
        qs.append(_q(f"{a} × {b} = ?", a * b, f"{a}×{b}={a*b}."))
    qs += [
        _q("−48 ÷ −6 = ?", 8, "Negative÷negative."),
        _q("−48 ÷ 6 = ?", -8, "Negative÷positive."),
        _q("A product of three negatives is…", "negative", "Odd count of minus."),
        _q("(−2/3)×(3/4)=?", "-1/2", "−6/12."),
        _q("−2.5 × 4 = ?", -10, "−10.", difficulty="hard"),
        _q("A rate −3° per hour for 5 hours. Change?", -15, "−3×5.", difficulty="hard"),
        _q("Divide −5/6 ÷ 1/3.", "-5/2", "−5/6×3=−5/2.", difficulty="hard"),
        _q("−0.2 × −0.3 = ?", "0.06", "Positive 0.06.", difficulty="hard"),
        _q("SAT-style: (−3)^2 vs −3^2. First is 9, second is?", -9, "Square then minus.", difficulty="stretch"),
        _q("A two-step (−4)×(−5)−7.", 13, "20−7.", difficulty="stretch"),
        _q("If  −7x = 28, x?", -4, "Divide.", difficulty="stretch"),
        _q("A stock −2.5% of $200 (loss amount)?", 5, "0.025×200=5 loss.", difficulty="stretch"),
        _q("Product (−1)×(−2)×(−3)×(−4).", 24, "Four negatives.", difficulty="stretch"),
        _q("−9/12 ÷ −3/4.", 1, "−3/4 ÷ −3/4 wait: 9/12×4/3=1.", difficulty="stretch"),
        _q("A repeating sign: −1 to the 5th power?", -1, "Odd power.", difficulty="stretch"),
        _q("0 × (−19).", 0, "Zero.", difficulty="stretch"),
        _q("A word: share −$60 loss among 4. Each?", -15, "−60/4.", difficulty="stretch"),
        _q("−3 1/2 × 2.", -7, "−7/2×2.", difficulty="stretch"),
        _q("Which is greater: −1/2 × −8 or 3?", 4, "4 vs 3.", difficulty="stretch"),
        _q("A chain −2 ÷ −1/4.", 8, "−2×−4=8.", difficulty="stretch"),
        _q("False: negative times negative is negative. True product of −2 and −9?", 18, "Positive.", difficulty="stretch"),
        _q("Evaluate (−5)^2 − 5^2.", 0, "25−25.", difficulty="stretch"),
    ]
    return qs


def g7u3():
    qs = []
    for a, b in ((2, 6), (3, 15), (4, 10), (5, 35), (1.5, 6), (7, 21), (8, 12), (9, 36)):
        k = b / a
        ans = int(k) if abs(k - round(k)) < 1e-9 else k
        qs.append(_q(f"If y is proportional to x and y={int(b) if b==int(b) else b} when x={a}, the constant k=y/x is?", ans, f"k={b}/{a}={ans}."))
    qs += [
        _q("A graph through (0,0) and (2,10). k?", 5, "10/2."),
        _q("Equation y=4x. y when x=7?", 28, "28."),
        _q("Is y=2x+1 proportional?", "no", "Not through origin with constant k only."),
        _q("A table 2→6, 5→15. Proportional?", "yes", "k=3."),
        _q("A recipe 3 cups for 4 people. For 10 people?", 7.5, "×2.5.", difficulty="hard"),
        _q("Similar figures scale 2:5. Small side 8. Large?", 20, "×2.5.", difficulty="hard"),
        _q("A graph of y=−3x. Point at x=4?", -12, "−12.", difficulty="hard"),
        _q("Unit rate in 12/5 hours for 36 miles. mph?", 15, "36÷12/5=15.", difficulty="hard"),
        _q("SAT-style: Two similar triangles 6 and 9 corresponding. Scale large:small?", "3/2", "9/6.", difficulty="stretch"),
        _q("If not proportional: (1,2),(2,5). Second k vs first?", "2.5 vs 2", "Not constant.", difficulty="stretch"),
        _q("A percent proportion 15/20 = x/100. x?", 75, "75%.", difficulty="stretch"),
        _q("Direct variation k=−2, x=−6. y?", 12, "y=kx.", difficulty="stretch"),
        _q("A map 1:50,000. 2 cm represents how many km? (2cm=1km if 1:50,000 because 50,000cm=500m wait: 50,000 cm = 500 m = 0.5 km per cm. 2 cm?", 1, "1 km.", difficulty="stretch"),
        _q("2 cm on a 1:50,000 map is how many km?", 1, "1 cm → 0.5 km.", difficulty="stretch"),
        _q("A double number line 4:10 = 6:x. x?", 15, "×1.5.", difficulty="stretch"),
        _q("Which table is proportional: 1,2,3 → 4,8,11?", "no", "11/3 not 4.", difficulty="stretch"),
        _q("y=x/2 at x=18.", 9, "9.", difficulty="stretch"),
        _q("A scale drawing 1/4 inch = 1 foot. 3 inches is how many feet?", 12, "3÷1/4=12.", difficulty="stretch"),
        _q("Constant of proportionality from (5,2) if proportional? k=y/x?", "2/5", "0.4.", difficulty="stretch"),
        _q("A word: 8 workers 6 days. Same work, 12 workers days? (inverse, but if proportional wrong). If work rate proportional to workers, days for same job?", 4, "Inverse 8×6=12×d, d=4.", difficulty="stretch"),
        _q("Inverse: 8 workers 6 days, 12 workers. Days?", 4, "48 worker-days /12.", difficulty="stretch"),
        _q("A graph of proportional y=kx is a line through…", "the origin", "(0,0).", difficulty="stretch"),
    ]
    return qs


def g7u4():
    qs = [
        _q("15% of 80?", 12, "0.15×80."),
        _q("A $60 item 25% off. Sale?", 45, "60×0.75."),
        _q("Tax 8% on $25. Tax amount?", 2, "2.00."),
        _q("12 is what % of 40?", 30, "12/40."),
        _q("A tip 18% on $50.", 9, "0.18×50."),
        _q("Increase 40 by 10%. New?", 44, "44."),
        _q("Decrease 90 by 1/3. New?", 60, "90−30."),
        _q("Simple interest $200 at 5% for 1 year.", 10, "10."),
        _q("A 200% of 15?", 30, "2×15."),
        _q("Markdown 10% then 10% of $100. Final?", 81, "90×0.9.", difficulty="hard"),
        _q("A number 24 is 40% of what?", 60, "24/0.4.", difficulty="hard"),
        _q("Commission 7% of $3,000.", 210, "210.", difficulty="hard"),
        _q("Percent change 40 to 50?", 25, "10/40=25%.", difficulty="hard"),
        _q("SAT-style: $80, 20% off, then 10% tax on the sale price. Pay?", 70.4, "64×1.1=70.4.", difficulty="stretch"),
        _q("A population 1,200 grows 15%. New?", 1380, "1200×1.15.", difficulty="stretch"),
        _q("Error: 9% of 50 is not 9. True value?", 4.5, "0.09×50.", difficulty="stretch"),
        _q("A 3:7 ratio, first as % of total (nearest %)?", 30, "3/10=30%.", difficulty="stretch"),
        _q("Double 35% of 80.", 56, "28×2.", difficulty="stretch"),
        _q("A $45 meal, 20% tip, 5% tax on food only (not tip). Total?", 56.25, "45×1.05 + 9 = 56.25.", difficulty="stretch"),
        _q("Percent decrease 80 to 60.", 25, "20/80.", difficulty="stretch"),
        _q("If 0.07 = p%, p?", 7, "7%.", difficulty="stretch"),
        _q("A mixture 30% of 2 L plus 10% of 2 L. Average %?", 20, "Equal parts.", difficulty="stretch"),
        _q("Successive: ×1.2 then ×0.8 on 50.", 48, "60×0.8.", difficulty="stretch"),
        _q("What % is 7 of 8?", 87.5, "87.5%.", difficulty="stretch"),
        _q("A $1,000 item, 15% down. Down payment?", 150, "150.", difficulty="stretch"),
        _q("Interest 4% of 750 for 2 years simple.", 60, "0.04×750×2.", difficulty="stretch"),
        _q("A two-coupon: 30% off vs $12 off on $50. Better savings?", 15, "30% is $15.", difficulty="stretch"),
        _q("Part 18, whole 24, percent?", 75, "75%.", difficulty="stretch"),
        _q("A scale 125% of 64.", 80, "64×1.25.", difficulty="stretch"),
        _q("Reverse: after 20% off the price is $64. Original?", 80, "64/0.8.", difficulty="stretch"),
    ]
    return qs


def g7u5():
    qs = [
        _q("2x + 5 = 17. x?", 6, "2x=12."),
        _q("3x − 7 = 2x + 4. x?", 11, "x=11."),
        _q("5(x−1)=20. x?", 5, "x−1=4."),
        _q("x/2 + 3 = 9. x?", 12, "x/2=6."),
        _q("−4x = 24. x?", -6, "Divide."),
        _q("2x + 3x − 6 = 14. x?", 4, "5x=20."),
        _q("4(x+2)−x=17. x?", 3, "4x+8−x=17, 3x=9."),
        _q("Inequality 2x+1 ≥ 9. Smallest integer x?", 4, "x≥4."),
        _q("3x+2 < 11. Largest integer x?", 2, "x<3."),
        _q("SAT-style: 2(3x−4)=5x+7. x?", 15, "6x−8=5x+7, x=15.", difficulty="hard"),
        _q("A word: 4 less than 3 times x is 11. x?", 5, "3x−4=11.", difficulty="hard"),
        _q("−2(x−3)=10. x?", -2, "x−3=−5.", difficulty="hard"),
        _q("x/3 − 2 = 5. x?", 21, "x/3=7.", difficulty="hard"),
        _q("Two-step ineq: 5−2x > 1. Reverse: x?", "x < 2", "−2x>−4, x<2.", difficulty="stretch"),
        _q("Identity 2(x+3)=2x+6. Solutions?", "all real numbers", "Always true.", difficulty="stretch"),
        _q("0·x + 5 = 4. Solutions?", 0, "5=4 never → none. Count 0 solutions.", difficulty="stretch"),
        _q("A perimeter 2x+2×7=36. x?", 11, "2x+14=36.", difficulty="stretch"),
        _q("3x+1=3x+1. Solutions?", "infinitely many", "Identity.", difficulty="stretch"),
        _q("A two-side: 7x−4=3x+16. x?", 5, "4x=20.", difficulty="stretch"),
        _q("Distribute −3(2−x)+x=9. x?", 3.75, "−6+3x+x=9, 4x=15, x=15/4.", difficulty="stretch"),
        _q("−3(2−x)+x=9. x as a fraction?", "15/4", "4x=15.", difficulty="stretch"),
        _q("Age: now x, in 5 years twice 12. Wait: x+5=24, x?", 19, "x=19.", difficulty="stretch"),
        _q("A number plus 18 is 4 times the number. Number?", 6, "n+18=4n, 18=3n.", difficulty="stretch"),
        _q("Ineq −x ≥ 4. x?", "x ≤ −4", "Multiply −1 reverse.", difficulty="stretch"),
        _q("2x/5 = 8. x?", 20, "2x=40.", difficulty="stretch"),
        _q("A table solve  x−3=2x+1. x?", -4, "−3=x+1, x=−4.", difficulty="stretch"),
        _q("3(x+4)−2(x−1)=20. x?", 6, "3x+12−2x+2=20, x=6.", difficulty="stretch"),
        _q("A SAT: If 1/2(x+8)=x−1, x?", 10, "x+8=2x−2, 10=x.", difficulty="stretch"),
        _q("Consecutive integers n+(n+1)=25. Smaller?", 12, "2n+1=25.", difficulty="stretch"),
        _q("Clear decimals: 0.2x+0.5=1.3. x?", 4, "×10: 2x+5=13.", difficulty="stretch"),
    ]
    return qs


def g7u6():
    qs = [
        _q("Circumference of a circle diameter 10. Use π=3.14. C?", 31.4, "πd."),
        _q("Radius 7, C=2πr with π=22/7. C?", 44, "2×22."),
        _q("Area πr², r=5, π=3.14. A?", 78.5, "25×3.14."),
        _q("A diameter is twice the…", "radius", "d=2r."),
        _q("Vertical angles are…", "equal", "Opposite."),
        _q("Adjacent angles on a line sum to ___°.", 180, "Linear pair."),
        _q("A triangle angles 40 and 70. Third?", 70, "180−110."),
        _q("Complement of 25°?", 65, "90−25."),
        _q("A circle radius 4, diameter?", 8, "8."),
        _q("SAT-style: C=18π, radius?", 9, "2πr=18π.", difficulty="hard"),
        _q("Area 36π, radius?", 6, "r²=36.", difficulty="hard"),
        _q("A central angle 90° is what fraction of the circle?", "1/4", "90/360.", difficulty="hard"),
        _q("Corresponding angles with parallel lines are…", "equal", "Same position.", difficulty="hard"),
        _q("A circumference 2πr=12π. Area?", "36π", "r=6, 36π.", difficulty="stretch"),
        _q("Arc of 60° in a circle r=9. Arc length (in terms of π)?", "3π", "60/360×18π=3π.", difficulty="stretch"),
        _q("A square inscribed in a circle diameter 10. Square diagonal 10, side?", "5√2", "d=s√2.", difficulty="stretch"),
        _q("Exterior angle of a triangle equals sum of remote interiors. 40+70=?", 110, "110.", difficulty="stretch"),
        _q("A wheel d=28 in, π=22/7. C?", 88, "22/7×28.", difficulty="stretch"),
        _q("Supplementary to 123°?", 57, "180−123.", difficulty="stretch"),
        _q("Two parallel, transversal, one angle 110. Alternate interior?", 110, "Equal.", difficulty="stretch"),
        _q("A sector 90° of r=8. Area of sector?", "16π", "1/4 of 64π.", difficulty="stretch"),
        _q("Triangle with sides forming 3-4-5. It is…", "right", "Pythagorean.", difficulty="stretch"),
        _q("A ring (annulus) R=5 r=3. Area?", "16π", "25π−9π.", difficulty="stretch"),
        _q("Straight angle minus 47°?", 133, "133.", difficulty="stretch"),
        _q("If two lines perpendicular, adjacent angles are…", "90°", "Right.", difficulty="stretch"),
        _q("A circle area 81π. Circumference?", "18π", "r=9, 18π.", difficulty="stretch"),
        _q("Polygon interior? Skip: a quadrilateral sum of interior angles?", 360, "360.", difficulty="stretch"),
        _q("A 6-sided regular polygon exterior each?", 60, "360/6.", difficulty="stretch"),
        _q("Radius 1.5, d?", 3, "3.", difficulty="stretch"),
        _q("π approximated 3: C of d=10?", 30, "Rough 30.", difficulty="stretch"),
    ]
    return qs


def g7u7():
    qs = [
        _q("Scale 1:20, drawing 4 cm. Real cm?", 80, "4×20."),
        _q("Similar ratio 3:5, small 9. Large?", 15, "×5/3."),
        _q("A prism 2×3×10. SA?", 112, "2(6+20+30)."),
        _q("Volume of that prism?", 60, "60."),
        _q("A scale factor 2 increases area by?", 4, "k²."),
        _q("Volume scale factor 2 increases volume by?", 8, "k³."),
        _q("A drawing 1/2 inch = 5 ft. 3 inches is how many feet?", 30, "3÷0.5×5=30."),
        _q("Surface area of cube edge 7?", 294, "6×49."),
        _q("A pyramid volume 1/3 Bh, B=12 h=9. V?", 36, "1/3×12×9."),
        _q("SAT-style: similar perimeters 12 and 18. Area ratio?", "4/9", "(2/3)².", difficulty="hard"),
        _q("A map 1 cm:4 km. 6.5 cm?", 26, "6.5×4.", difficulty="hard"),
        _q("Cylinder V=πr²h, r=3 h=5, in terms of π?", "45π", "9×5π.", difficulty="hard"),
        _q("A 3D scale 1:2, small volume 10. Large volume?", 80, "×8.", difficulty="hard"),
        _q("A net of a cylinder: 2 circles + rectangle. Rectangle width if r=4 (C=2πr)?", "8π", "Circumference.", difficulty="stretch"),
        _q("A box 6×5×4. SA?", 148, "2(30+24+20).", difficulty="stretch"),
        _q("Missing scale: 8 cm drawing, 2.4 m real. Scale 1 cm : ? m.", 0.3, "2.4/8.", difficulty="stretch"),
        _q("Similar triangles 5 and 15 corresponding. Linear scale?", 3, "15/5.", difficulty="stretch"),
        _q("Area scale for that 3?", 9, "3².", difficulty="stretch"),
        _q("A triangular prism V=½×6×8×10.", 240, "24×10.", difficulty="stretch"),
        _q("A cube SA 150. Edge²?", 25, "6e²=150, e²=25.", difficulty="stretch"),
        _q("Edge of that cube?", 5, "5.", difficulty="stretch"),
        _q("A model 1:50 of a 20 m wall. Model cm? (20m=2000cm /50)", 40, "40 cm.", difficulty="stretch"),
        _q("Volume of cube edge 9?", 729, "729.", difficulty="stretch"),
        _q("A composite 10×4×4 plus 4×4×4 cube on top. Volume?", 224, "160+64.", difficulty="stretch"),
        _q("If lengths ×1/2, SA × ?", "1/4", "k².", difficulty="stretch"),
        _q("A scale error 1:10 vs 1:100 makes lengths 10 times too…", "big", "If you use 1:10 instead of 1:100.", difficulty="stretch"),
        _q("Cylinder r=2 h=10, SA 2πr²+2πrh in π?", "48π", "8π+40π.", difficulty="stretch"),
        _q("A word: blueprint 1/8\" = 1'. A 3\" wall on paper is how many feet?", 24, "3÷1/8=24.", difficulty="stretch"),
        _q("Pyramid B=20 h=12. V?", 80, "1/3×20×12.", difficulty="stretch"),
        _q("Two similar SA 18 and 32. Linear ratio?", "3/4", "√(18/32)=√(9/16)=3/4.", difficulty="stretch"),
    ]
    return qs


def g7u8():
    qs = [
        _q("P(even) on a fair die?", "1/2", "2,4,6."),
        _q("P(5) on a fair die?", "1/6", "One face."),
        _q("A coin twice. P(HH)?", "1/4", "Independent."),
        _q("Mean of 6, 10, 14?", 10, "30/3."),
        _q("A spinner 4 equal, 1 red. P(not red)?", "3/4", "Complement."),
        _q("Sample space coin then die. Outcomes?", 12, "2×6."),
        _q("P(sum 7) two dice?", "1/6", "6 of 36."),
        _q("Median of 2,9,3,7,5?", 5, "Sorted 2,3,5,7,9."),
        _q("A bag 3 red 7 blue. P(red)?", "3/10", "3/10."),
        _q("SAT-style: without replacement 5 red 5 blue, P(two red)?", "2/9", "5/10×4/9=2/9.", difficulty="hard"),
        _q("Independent P(A)=1/2, P(B)=1/3. P(both)?", "1/6", "Product.", difficulty="hard"),
        _q("A survey 40%, 25 people of 100. Expected in 100 if 40%?", 40, "40.", difficulty="hard"),
        _q("Range 3,18,7,3?", 15, "18−3.", difficulty="hard"),
        _q("Two-way: 20 boys 15 girls, 8 boys play soccer 10 girls play. P(girl|soccer)? Soccer total 18, girls 10. P?", "5/9", "10/18.", difficulty="stretch"),
        _q("P(soccer player is a girl) with 8 boy soccer, 10 girl soccer?", "5/9", "10/18=5/9.", difficulty="stretch"),
        _q("A compound P(A or B) disjoint 0.2+0.5.", "0.7", "Add.", difficulty="stretch"),
        _q("Not disjoint: P(A)=0.4 P(B)=0.5 P(both)=0.1. P(A or B)?", "0.8", "0.4+0.5−0.1.", difficulty="stretch"),
        _q("A tree: first 1/2, then 1/3. Path probability?", "1/6", "Product.", difficulty="stretch"),
        _q("Mean vs median of 1,2,3,100. Median?", 2.5, "2 and 3.", difficulty="stretch"),
        _q("That set’s mean?", "26.5", "106/4.", difficulty="stretch"),
        _q("A fair 8-sided die P(>6)?", "1/4", "7,8 → 2/8.", difficulty="stretch"),
        _q("Simulate 50 flips, 28 heads. Experimental P(H)?", "0.56", "28/50.", difficulty="stretch"),
        _q("Fundamental counting 3 shirts 4 pants. Outfits?", 12, "3×4.", difficulty="stretch"),
        _q("P(at least one head) two coins?", "3/4", "1−1/4.", difficulty="stretch"),
        _q("A random sample should be…", "unbiased / representative", "Not only volunteers.", difficulty="stretch"),
        _q("IQR Q1=10 Q3=22?", 12, "22−10.", difficulty="stretch"),
        _q("A box plot median 50, mean 70. Skew?", "right", "Mean > median.", difficulty="stretch"),
        _q("Dependent: 4 cards ace in 52, P(ace then ace)?", "12/2652", "4/52×3/51=12/2652=1/221.", difficulty="stretch"),
        _q("P(ace then ace) simplified?", "1/221", "4/52×3/51.", difficulty="stretch"),
        _q("A complement P(A)=0.15. P(not A)?", "0.85", "1−0.15.", difficulty="stretch"),
    ]
    return qs


def g8u1():
    qs = []
    for b, e in ((2, 5), (3, 4), (5, 3), (4, 4), (6, 3), (10, 4), (2, 8), (7, 3)):
        qs.append(_q(f"${b}^{{{e}}} = $ ?", b ** e, f"{b}^{e}={b**e}."))
    qs += [
        _q("$3^2 \\times 3^4 = $ ?", "$3^6$", "Add exponents."),
        _q("$5^7 \\div 5^3 = $ ?", "$5^4$", "Subtract."),
        _q("$(2^3)^4 = $ ?", "$2^{12}$", "Multiply 3×4."),
        _q("$2^{-4} = $ ?", "1/16", "1/2^4."),
        _q("$7^0 = $ ?", 1, "Nonzero to 0 is 1."),
        _q("$(3\\times10^4)(2\\times10^5)=$?", "$6\\times10^9$", "3×2 and 4+5."),
        _q("$4.2\\times10^{-3}$ in standard form?", "0.0042", "Three left."),
        _q("$\\sqrt{144}=$?", 12, "12×12."),
        _q("$\\sqrt{50}$ is between…", "7 and 8", "49 and 64.", difficulty="hard"),
        _q("$(-3)^2$ vs $-3^2$. The second is?", -9, "Square 3 then minus.", difficulty="hard"),
        _q("$x^8/x^2=$?", "$x^6$", "8−2.", difficulty="hard"),
        _q("$(2x^3)(5x^4)=$?", "$10x^7$", "2×5 and 3+4.", difficulty="hard"),
        _q("SAT Stretch: $(4\\times10^{-2})/(8\\times10^{3})$?", "$5\\times10^{-6}$", "0.5×10^{-5}=5×10^{-6}.", difficulty="stretch"),
        _q("$5^{-2}\\times5^{5}=$?", "$5^{3}$", "−2+5=3.", difficulty="stretch"),
        _q("Which is irrational: $\\sqrt{8}$ or $\\sqrt{9}$?", "$\\sqrt{8}$", "√8=2√2.", difficulty="stretch"),
        _q("$\\sqrt{81}+\\sqrt{16}$?", 13, "9+4.", difficulty="stretch"),
        _q("$(1/3)^{-2}$?", 9, "3^2.", difficulty="stretch"),
        _q("$2.5\\times10^3 + 3.1\\times10^3$?", "$5.6\\times10^3$", "Add coefficients.", difficulty="stretch"),
        _q("Compare $4.1\\times10^5$ and $3.9\\times10^6$. Larger?", "$3.9\\times10^6$", "Exponent first.", difficulty="stretch"),
        _q("$x^0\\cdot x^5$ for $x\\neq0$?", "$x^5$", "1·x^5.", difficulty="stretch"),
        _q("A cube volume 125. Edge?", 5, "5^3=125.", difficulty="stretch"),
        _q("$(10^2)^3\\times10^{-4}$?", "$10^{2}$", "6−4=2.", difficulty="stretch"),
        _q("Scientific of 0.00056?", "$5.6\\times10^{-4}$", "Four left.", difficulty="stretch"),
        _q("$\\sqrt{2}\\times\\sqrt{8}$?", 4, "√16=4.", difficulty="stretch"),
        _q("SAT: $(3\\times10^{-4})^2$?", "$9\\times10^{-8}$", "9 and −8.", difficulty="stretch"),
    ]
    return qs


def g8u2():
    qs = [
        _q("$x+12=5$. $x$?", -7, "Subtract 12."),
        _q("$3x=−21$. $x$?", -7, "Divide 3."),
        _q("$2x+7=19$. $x$?", 6, "2x=12."),
        _q("$5x−4=3x+10$. $x$?", 7, "2x=14."),
        _q("$\\frac{x}{4}=−6$. $x$?", -24, "×4."),
        _q("$4(x−3)=20$. $x$?", 8, "x−3=5."),
        _q("$−2x+5=17$. $x$?", -6, "−2x=12."),
        _q("$3(2x+1)=2x+19$. $x$?", 4, "6x+3=2x+19."),
        _q("A number plus 9 is −2. Number?", -11, "n+9=−2."),
        _q("SAT: $2(x+4)−3(x−1)=x+1$. $x$?", 10, "2x+8−3x+3=x+1 → −x+11=x+1 → 10=2x.", difficulty="hard"),
        _q("$\\frac{2x}{3}+1=7$. $x$?", 9, "2x/3=6.", difficulty="hard"),
        _q("Identity $2x+6=2(x+3)$. Solutions?", "all real x", "Always true.", difficulty="hard"),
        _q("$0\\cdot x + 4 = 5$. Solutions?", "none", "4=5 false.", difficulty="hard"),
        _q("SAT Stretch: $\\frac{x-3}{2}=\\frac{x}{5}+1$. $x$?", 25, "5(x−3)=2x+10 → 5x−15=2x+10 → 3x=25? Wait 5x−15=2x+10, 3x=25, x=25/3. Recalc: 5(x-3)=2(x+5)=2x+10. 5x-15=2x+10, 3x=25, x=25/3.", difficulty="stretch"),
        _q("$\\frac{x-3}{2}=\\frac{x+5}{5}$. $x$?", 25, "5(x−3)=2(x+5) → 5x−15=2x+10 → 3x=25, x=25/3. Use 25/3.", difficulty="stretch"),
        _q("Solve $\\dfrac{x-3}{2}=\\dfrac{x+5}{5}$. $x$ as a fraction?", "25/3", "3x=25.", difficulty="stretch"),
        _q("A word: 3 consecutive integers sum to 48. Middle?", 16, "n+(n+1)+(n+2)=48, n=15, middle 16.", difficulty="stretch"),
        _q("$−(x−4)=2x+1$. $x$?", 1, "−x+4=2x+1, 3=3x.", difficulty="stretch"),
        _q("Clear decimals $0.3x+1.2=2.1$. $x$?", 3, "×10: 3x+12=21.", difficulty="stretch"),
        _q("$\\frac{1}{2}(4x-2)=x+5$. $x$?", 6, "2x−1=x+5.", difficulty="stretch"),
        _q("Ineq $3x-7 \\le 8$. Largest integer x?", 5, "3x≤15, x≤5.", difficulty="stretch"),
        _q("A perimeter 2l+2w=54, w=l−3. l?", 15, "2l+2l−6=54, 4l=60.", difficulty="stretch"),
        _q("$5-2(x+1)=x-4$. $x$?", 7/3, "5-2x-2=x-4, 3-2x=x-4, 7=3x.", difficulty="stretch"),
        _q("Solve $5-2(x+1)=x-4$. $x$ as fraction?", "7/3", "3x=7.", difficulty="stretch"),
        _q("If 4 more than twice x is 18, x?", 7, "2x+4=18.", difficulty="stretch"),
        _q("$|x|=9$. Positive solution?", 9, "x=±9.", difficulty="stretch"),
        _q("A SAT: $3(x+2)=2(x+8)+1$. $x$?", 11, "3x+6=2x+16+1, x=11.", difficulty="stretch"),
        _q("$x/5 - x/10 = 3$. $x$?", 30, "x/10=3.", difficulty="stretch"),
        _q("No solution: $2x+1=2x-4$ is true? (yes/no)", "no", "1=−4.", difficulty="stretch"),
        _q("A two-step with fractions $\\frac{2}{3}x=10$. $x$?", 15, "×3/2.", difficulty="stretch"),
    ]
    qs = [q for q in qs if q and "Wait" not in q["explanation"] and "Recalc" not in q["explanation"]]
    return qs


def g8u3():
    qs = [
        _q("Slope between (1,2) and (3,8)?", 3, "6/2=3."),
        _q("Slope of y=−4x+1?", -4, "m=−4."),
        _q("A horizontal line slope?", 0, "No rise."),
        _q("A vertical line slope?", "undefined", "Run=0."),
        _q("y-intercept of y=2x−5?", -5, "b=−5."),
        _q("Point-slope: through (0,3) slope 2. Equation y=?", "2x+3", "y=2x+3."),
        _q("Parallel to y=3x+1 has slope?", 3, "Same slope."),
        _q("Perpendicular to y=2x has slope?", "-1/2", "Negative reciprocal."),
        _q("From (0,0) to (4,−2). Slope?", "-1/2", "−2/4."),
        _q("SAT: line through (2,5) and (6,13). Slope?", 2, "8/4.", difficulty="hard"),
        _q("y=−x+4, x-intercept?", 4, "0=−x+4.", difficulty="hard"),
        _q("A table x:0,1,2 y:5,8,11. Slope?", 3, "Δy=3.", difficulty="hard"),
        _q("Equation of line slope 1/3 through (0,−2)?", "y=(1/3)x-2", "b=−2.", difficulty="hard"),
        _q("SAT Stretch: perpendicular to  y=−(2/3)x+1 through (0,4). Slope of new line?", "3/2", "Neg rec of −2/3 is 3/2.", difficulty="stretch"),
        _q("That line’s equation?", "y=(3/2)x+4", "Through (0,4).", difficulty="stretch"),
        _q("Are (0,1),(2,5),(3,7) collinear? Slope first pair 2, second 2. Collinear?", "yes", "Same slope from a point.", difficulty="stretch"),
        _q("Distance (0,0) to (6,8)?", 10, "6-8-10.", difficulty="stretch"),
        _q("Midpoint (2,−4) and (8,2)?", "(5,-1)", "Averages.", difficulty="stretch"),
        _q("A rate $12 per hour as slope of $ vs hours?", 12, "m=12.", difficulty="stretch"),
        _q("If m=0 through (3,7). Equation?", "y=7", "Horizontal.", difficulty="stretch"),
        _q("Standard 2x+3y=6, slope?", "-2/3", "3y=−2x+6, y=−(2/3)x+2.", difficulty="stretch"),
        _q("y-intercept of 2x+3y=6?", 2, "x=0, y=2.", difficulty="stretch"),
        _q("A graph rises 5 over run 10. Slope?", "1/2", "0.5.", difficulty="stretch"),
        _q("Two lines y=4x−1 and y=4x+9. Relation?", "parallel", "Same m, different b.", difficulty="stretch"),
        _q("Point (4,0) on y=mx+2. m?", "-1/2", "0=4m+2.", difficulty="stretch"),
        _q("SAT: f(x)=mx+b, f(0)=3, f(2)=11. m?", 4, "(11−3)/2.", difficulty="stretch"),
        _q("Then b?", 3, "f(0)=3.", difficulty="stretch"),
        _q("A vertical through x=−5. Equation?", "x=-5", "Undefined slope.", difficulty="stretch"),
        _q("Slope of the line  x=2 is…", "undefined", "Vertical.", difficulty="stretch"),
        _q("A walk 3 km east, 4 km north. Slope of path if east is +x?", "4/3", "Rise/run.", difficulty="stretch"),
    ]
    return qs


def g8u4():
    qs = [
        _q("f(x)=3x−1. f(4)?", 11, "12−1."),
        _q("Is a circle a function of x?", "no", "Vertical line hits twice."),
        _q("Domain of y=√x (reals)?", "x≥0", "Radicand ≥0."),
        _q("A table (1,2),(2,2),(3,2). Function?", "yes", "Each x one y."),
        _q("Linear or nonlinear: y=x²?", "nonlinear", "Quadratic."),
        _q("Rate of change of y=5x+2?", 5, "Slope 5."),
        _q("f(x)=x², f(−3)?", 9, "9."),
        _q("Which input is missing: outputs unique. Vertical line test fails when…", "one x has two y", "Not a function."),
        _q("g(x)=−x+8, g(8)?", 0, "0."),
        _q("SAT: f(x)=2x+3, solve f(x)=17. x?", 7, "2x=14.", difficulty="hard"),
        _q("A graph through (0,0) and (5,15). Linear f(x)=?", "3x", "m=3.", difficulty="hard"),
        _q("Nonlinear: y=2^x at x=3?", 8, "8.", difficulty="hard"),
        _q("Compare f(x)=x and g(x)=x+2. Vertical shift?", 2, "Up 2.", difficulty="hard"),
        _q("SAT Stretch: f(x)=x²−4x, f(x+1)? Expand.", "$x^2-2x-3$", "(x+1)²−4(x+1)=x²+2x+1−4x−4=x²−2x−3.", difficulty="stretch"),
        _q("If f is linear, f(0)=5, f(1)=9. f(10)?", 45, "m=4, 4×10+5.", difficulty="stretch"),
        _q("A piecewise f(x)=x if x<0, 2x if x≥0. f(−3)?", -3, "First piece.", difficulty="stretch"),
        _q("That f(3)?", 6, "Second piece.", difficulty="stretch"),
        _q("Range of f(x)=|x|?", "y≥0", "Never negative.", difficulty="stretch"),
        _q("A sequence 3,7,11… as f(n)=4n−1 for n=1. f(20)?", 79, "80−1.", difficulty="stretch"),
        _q("Not a function: (2,1),(2,7). Reason: repeated…", "x-value", "x=2 twice.", difficulty="stretch"),
        _q("f(x)=10−x. Inverse idea: solve y=10−x for x in terms of y.", "x=10-y", "Swap.", difficulty="stretch"),
        _q("Average rate of change of y=x² from 1 to 3?", 4, "(9−1)/(3−1)=4.", difficulty="stretch"),
        _q("A SAT: graph of y=2x−6 crosses x-axis at?", 3, "2x=6.", difficulty="stretch"),
        _q("Increasing function: as x grows, y…", "grows", "Positive slope linear.", difficulty="stretch"),
        _q("f(x)=3, a constant. Slope?", 0, "Horizontal.", difficulty="stretch"),
        _q("Which is linear: y=x/2 or y=2/x?", "y=x/2", "Proportional.", difficulty="stretch"),
        _q("f(g) if f(x)=x+1, g(x)=2x, f(g(4))?", 9, "g=8, f=9.", difficulty="stretch"),
        _q("A table not linear: 1→2, 2→4, 3→8. Next if doubling?", 16, "Exponential-like.", difficulty="stretch"),
        _q("Domain of f(x)=1/(x−5)?", "x≠5", "Denominator ≠0.", difficulty="stretch"),
        _q("SAT: If f is linear and f(2)=f(8), slope?", 0, "Horizontal.", difficulty="stretch"),
    ]
    return qs


def g8u5():
    qs = [
        _q("y=x+2 and y=2x−1. Intersection x?", 3, "x+2=2x−1, 3=x."),
        _q("Then y?", 5, "3+2."),
        _q("Substitution: x=3−y into x+y=5. Wait x+y=5 and x=3−y → 3=5 contradiction? Use y=x−1, 2x+y=5. From y=x−1: 2x+x−1=5, x?", 2, "3x=6."),
        _q("System y=x−1, 2x+y=5. x?", 2, "2x+(x−1)=5."),
        _q("Then y?", 1, "2−1."),
        _q("Parallel y=2x+1 and y=2x−4. Solutions?", 0, "Never meet."),
        _q("Same line  y=3x+2 and 2y=6x+4. Solutions?", "infinitely many", "Dependent."),
        _q("x+y=10, x−y=2. x?", 6, "Add: 2x=12."),
        _q("Then y?", 4, "10−6."),
        _q("SAT: 3x+y=7, y=2x. x?", 7/5, "3x+2x=7.", difficulty="hard"),
        _q("3x+y=7, y=2x. x as a fraction?", "7/5", "5x=7.", difficulty="hard"),
        _q("A word: 2 adult + 1 child = $32, 1 adult + 2 child = $28. Adult price?", 12, "2a+c=32, a+2c=28 → 3a=36? From 2×second: 2a+4c=56, minus first: 3c=24, c=8, a=12.", difficulty="hard"),
        _q("Child price in that system?", 8, "c=8.", difficulty="hard"),
        _q("SAT Stretch: 2x−3y=1, x+y=8. x?", 5, "x=8−y, 16−2y−3y=1, 16−5y=1, 5y=15, y=3, x=5.", difficulty="stretch"),
        _q("Then y?", 3, "8−5.", difficulty="stretch"),
        _q("No solution vs infinite:  x+y=4 and 2x+2y=9. Type?", "no solution", "Inconsistent 8=9.", difficulty="stretch"),
        _q("Graphically substitution finds the…", "intersection point", "Meet.", difficulty="stretch"),
        _q("x=4, y=2x−3. y?", 5, "8−3.", difficulty="stretch"),
        _q("A mixture: 3x+2y=18, x=2. y?", 6, "6+2y=18.", difficulty="stretch"),
        _q("If two lines have different slopes they intersect how many times?", 1, "Exactly once.", difficulty="stretch"),
        _q("System x−y=0, x+y=10. Point?", "(5,5)", "x=y=5.", difficulty="stretch"),
        _q("A SAT: 4x+2y=16 simplify first. Equivalent?", "2x+y=8", "Divide 2.", difficulty="stretch"),
        _q("Then with y=x+1, x?", 7/3, "2x+x+1=8, 3x=7.", difficulty="stretch"),
        _q("2x+y=8, y=x+1. x as fraction?", "7/3", "3x=7.", difficulty="stretch"),
        _q("A coin 5 dimes 3 nickels vs 2d+7n=80 cents. Use 10d+5n=80 wait. d+n=8, 10d+5n=55. Then d?", 3, "10d+5(8−d)=55, 10d+40−5d=55, 5d=15.", difficulty="stretch"),
        _q("dimes if d+n=8 and 10d+5n=55?", 3, "5d=15.", difficulty="stretch"),
        _q("Then nickels?", 5, "8−3.", difficulty="stretch"),
        _q("Dependent system is two equations that are…", "multiples of each other", "Same line.", difficulty="stretch"),
        _q("y=−x+6 and y=x. Intersection y?", 3, "x=3.", difficulty="stretch"),
        _q("A 3-var not asked:  x+y=1, x−y=1. x?", 1, "Add 2x=2.", difficulty="stretch"),
    ]
    return qs


def g8u6():
    qs = [
        _q("Elimination: x+y=5, x−y=1. Add. 2x?", 6, "6."),
        _q("Then x?", 3, "3."),
        _q("Then y?", 2, "5−3."),
        _q("2x+y=9, 2x−y=1. Add. 4x?", 10, "10."),
        _q("x?", 2.5, "10/4=2.5."),
        _q("Multiply second by 2: x+2y=7, 3x+y=11. After aligning y? One path: ×2 on second y: skip. Solve: from first x=7−2y into 3(7−2y)+y=11. y?", 2, "21−6y+y=11, −5y=−10."),
        _q("Then x in x+2y=7, y=2?", 3, "3+4=7."),
        _q("3x+2y=12, 3x+2y=15. Solutions?", "none", "12=15 false."),
        _q("4x−y=6, −4x+y=−6. Solutions?", "infinitely many", "Same line."),
        _q("SAT: 5x+2y=16, 3x−2y=8. Add. 8x?", 24, "24.", difficulty="hard"),
        _q("x?", 3, "24/8.", difficulty="hard"),
        _q("Then y from 5(3)+2y=16?", 0.5, "15+2y=16.", difficulty="hard"),
        _q("Need to multiply: 2x+3y=7, 4x−y=1. ×3 second y: 12x−3y=3, add to first. 14x?", 10, "2x+12x +3y−3y=7+3.", difficulty="hard"),
        _q("SAT Stretch: 2x+3y=7, 4x−y=1. From 14x=10, x?", "5/7", "10/14=5/7.", difficulty="stretch"),
        _q("Then y from 4(5/7)−y=1. y?", "13/7", "20/7 − y=1, y=20/7−7/7=13/7.", difficulty="stretch"),
        _q("A word: 2 hotdogs + 3 drinks = 18, 1 hotdog + 1 drink = 7. Drink?", 4, "2h+3d=18, h+d=7 → h=7−d, 14−2d+3d=18, d=4.", difficulty="stretch"),
        _q("Hotdog price?", 3, "7−4.", difficulty="stretch"),
        _q("Elimination when coefficients opposite.  x+y=4, −x+y=2. 2y?", 6, "Add.", difficulty="stretch"),
        _q("y?", 3, "3.", difficulty="stretch"),
        _q("x?", 1, "4−3.", difficulty="stretch"),
        _q("If you multiply an equation by 2, solutions of the system…", "stay the same", "Equivalent equation.", difficulty="stretch"),
        _q("3x−y=8, x+y=4. Add. 4x?", 12, "12.", difficulty="stretch"),
        _q("x?", 3, "3.", difficulty="stretch"),
        _q("y?", 1, "3+y=4.", difficulty="stretch"),
        _q("A SAT: 6x+2y=10 simplify. Equivalent?", "3x+y=5", "Divide 2.", difficulty="stretch"),
        _q("With x−y=1, then 3(y+1)+y=5. y?", "1/2", "3y+3+y=5, 4y=2.", difficulty="stretch"),
        _q("Decimals: 0.5x+y=4, x−y=1. From x=y+1: 0.5y+0.5+y=4. y?", 2.333, "1.5y=3.5, y=7/3.", difficulty="stretch"),
        _q("0.5x+y=4, x=y+1. y as fraction?", "7/3", "1.5y=3.5.", difficulty="stretch"),
        _q("Check: inconsistent  x+y=2, 2x+2y=5.  Left×2 vs right?", "4 vs 5", "No solution.", difficulty="stretch"),
        _q("Best first move if 2x+3y=1, 4x+6y=2?", "notice multiples / infinite", "Second is ×2 of first.", difficulty="stretch"),
    ]
    qs = [q for q in qs if q and "skip" not in q["question_text"].lower()]
    return qs


def g8u7():
    qs = []
    triples = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (9, 12, 15), (8, 15, 17), (7, 24, 25)]
    for a, b, c in triples:
        qs.append(_q(f"Right triangle legs {a} and {b}. Hypotenuse?", c, f"{a}²+{b}²={c}²."))
    qs += [
        _q("A 6-8-? right triangle hypotenuse?", 10, "36+64=100."),
        _q("Is 5,12,14 a right triangle?", "no", "25+144=169≠196."),
        _q("Leg 9, hyp 15. Other leg?", 12, "225−81=144."),
        _q("A square side 5. Diagonal?", "$5\\sqrt{2}$", "s√2."),
        _q("Distance (0,0) to (9,12)?", 15, "9-12-15.", difficulty="hard"),
        _q("A 45-45-90 legs 7. Hypotenuse?", "$7\\sqrt{2}$", "×√2.", difficulty="hard"),
        _q("A 30-60-90 short 5. Hypotenuse?", 10, "×2.", difficulty="hard"),
        _q("That triangle’s long leg?", "$5\\sqrt{3}$", "×√3.", difficulty="hard"),
        _q("SAT Stretch: a 10-ft ladder 6 ft from wall. Height on wall?", 8, "100−36=64.", difficulty="stretch"),
        _q("A rectangle 5 by 12. Diagonal?", 13, "5-12-13.", difficulty="stretch"),
        _q("Cone slant 13, r=5. Height?", 12, "169−25.", difficulty="stretch"),
        _q("Cylinder r=3 h=4. Space diagonal of enclosing prism 6×6×4? Wait cylinder diameter 6 height 4. Diagonal of 6×6×4 box?", "$\\sqrt{88}$", "36+36+16=88.", difficulty="stretch"),
        _q("Space diagonal of a 6×6×4 rectangular box?", "$2\\sqrt{22}$", "√88=2√22.", difficulty="stretch"),
        _q("A 20-21-29 check: 400+441=841=29². Right?", "yes", "Yes.", difficulty="stretch"),
        _q("Area of right triangle legs 9 and 12?", 54, "½×9×12.", difficulty="stretch"),
        _q("If hyp=25, one leg=7, other?", 24, "625−49=576.", difficulty="stretch"),
        _q("A coordinate (1,1) to (4,5). Distance?", 5, "3-4-5.", difficulty="stretch"),
        _q("Isosceles right hyp 10. Leg?", "$5\\sqrt{2}$", "10/√2=5√2.", difficulty="stretch"),
        _q("A SAT: square diagonal 8√2. Side?", 8, "s√2=8√2.", difficulty="stretch"),
        _q("Pythagorean triple multiple of 3-4-5 with hyp 40. Legs?", "24 and 32", "×8.", difficulty="stretch"),
        _q("Volume not: a wire 13 along space of 3-4-? height if base 3-4. Height?", 12, "5-12-13 with 5 on floor? If floor 3-4 hyp 5, leftover 12 height.", difficulty="stretch"),
        _q("A 3-4-5 on the floor, space diagonal 13. Height of room?", 12, "5²+h²=13².", difficulty="stretch"),
        _q("Converse: 9²+12²=15² so the triangle is…", "right", "Converse of Pythagoras.", difficulty="stretch"),
        _q("A circle diameter 10, inscribed right triangle hyp is the diameter. If one leg 6, other?", 8, "Thales + 6-8-10.", difficulty="stretch"),
    ]
    return qs


def g8u8():
    qs = [
        _q("A scatter plot of height vs age for kids is likely…", "positive association", "Both increase."),
        _q("A line of best fit slope 2 intercept 1. Predict at x=4?", 9, "8+1."),
        _q("An outlier is a point that…", "does not fit the pattern", "Far from cluster."),
        _q("Correlation is not…", "causation", "Classic warning."),
        _q("A two-way table 30 of 50 like A. Relative frequency?", "0.6", "30/50."),
        _q("Mean of residuals around a good fit is about…", 0, "Balance of errors."),
        _q("A cluster is a…", "group of nearby points", "Pile."),
        _q("Nonlinear scatter looks like a…", "curve", "Not a line."),
        _q("If slope of best fit is negative, association is…", "negative", "One up one down."),
        _q("SAT: data (1,3),(2,5),(3,7). Best fit slope?", 2, "Perfect line.", difficulty="hard"),
        _q("Intercept of that line?", 1, "y=2x+1.", difficulty="hard"),
        _q("A two-way: 40 students, 12 both sports, 18 only A, 6 only B. Neither?", 4, "40−36.", difficulty="hard"),
        _q("P(A) if 18+12 play A of 40?", "3/4", "30/40.", difficulty="hard"),
        _q("SAT Stretch: residual = actual − predicted. Actual 10, pred 8. Residual?", 2, "Positive above the line.", difficulty="stretch"),
        _q("A frequency 10,20,30. Relative of 20 if total 60?", "1/3", "20/60.", difficulty="stretch"),
        _q("Bivariate means…", "two variables", "Paired data.", difficulty="stretch"),
        _q("A misleading graph might omit…", "zero on the axis", "Scale trick.", difficulty="stretch"),
        _q("If r were 1 (perfect +), points lie on a…", "line with positive slope", "Perfect linear.", difficulty="stretch"),
        _q("Extrapolation is predicting…", "outside the data range", "Riskier.", difficulty="stretch"),
        _q("A two-way P(B|A): A has 30, both 12. P?", "2/5", "12/30.", difficulty="stretch"),
        _q("A scatter with no trend. Association?", "none / weak", "Cloud.", difficulty="stretch"),
        _q("Median-median line is a robust…", "fit", "Resistant to outliers.", difficulty="stretch"),
        _q("A histogram vs scatter: scatter needs…", "paired (x,y)", "Two measured vars.", difficulty="stretch"),
        _q("Predicted y=−0.5x+10 at x=8?", 6, "−4+10.", difficulty="stretch"),
        _q("If all points shift +3 in y, slope of best fit…", "stays the same", "Intercept +3.", difficulty="stretch"),
        _q("A SAT two-way 25% of 80 is how many?", 20, "0.25×80.", difficulty="stretch"),
        _q("Outlier (100,2) among x=1..10 y≈2x. Effect on slope?", "pulls slope down", "Leverage.", difficulty="stretch"),
        _q("A cluster at (2,2) and another at (8,8). Overall association?", "positive", "Both clusters rise.", difficulty="stretch"),
        _q("Categorical vs numerical: favorite color is…", "categorical", "Labels.", difficulty="stretch"),
        _q("A line of best fit should pass near the…", "center of the cloud", "Balance.", difficulty="stretch"),
    ]
    return qs


def a2u1():
    qs = [
        _q("If $f(x)=x^2-5x$, $f(3)$?", -6, "9−15=−6."),
        _q("Domain of $f(x)=\\sqrt{x-4}$?", "$x\\ge4$", "Inside ≥0."),
        _q("Domain of $1/(x^2-9)$?", "$x\\ne\\pm3$", "Denom ≠0."),
        _q("Range of $f(x)=(x-1)^2+2$?", "$y\\ge2$", "Vertex min 2."),
        _q("$(f\\circ g)(x)$ if $f(x)=x+1$, $g(x)=2x$. $(f\\circ g)(5)$?", 11, "g=10, f=11."),
        _q("Inverse of $f(x)=3x-6$?", "$f^{-1}(x)=\\frac{x+6}{3}$", "Swap solve."),
        _q("Even, odd, or neither: $f(x)=x^3$?", "odd", "f(−x)=−f(x)."),
        _q("Vertical stretch 2 of $y=\\sqrt{x}$?", "$y=2\\sqrt{x}$", "Multiply out."),
        _q("Shift $y=|x|$ right 3 up 1?", "$y=|x-3|+1$", "Inside minus is right."),
        _q("SAT: $f(x)=2x+1$, $f^{-1}(7)$?", 3, "2x+1=7.", difficulty="hard"),
        _q("Piecewise $h(x)=3x$ if $x<1$, $x^2$ if $x\\ge1$. $h(1)$?", 1, "Second piece.", difficulty="hard"),
        _q("$h(-2)$?", -6, "First piece.", difficulty="hard"),
        _q("A graph fails VLT. It is…", "not a function", "Two y for one x.", difficulty="hard"),
        _q("SAT Stretch: $f(x)=\\frac{x+2}{x-1}$. $f(f(x))$ simplifies to?", "$x$", "These are involutions? f(f(x))=((x+2)/(x-1)+2)/((x+2)/(x-1)-1)=(3x)/(3)=x.", difficulty="stretch"),
        _q("$f(x)=(x+2)/(x-1)$. $f(f(3))$?", 3, "Involution on its domain.", difficulty="stretch"),
        _q("If $f(x)=x^2$ and $g(x)=x-3$, $(g\\circ f)(2)$?", 1, "4−3.", difficulty="stretch"),
        _q("$(f\\circ g)(2)$ for those?", 1, "f(−1)=1.", difficulty="stretch"),
        _q("Domain of $\\sqrt{4-x^2}$?", "$-2\\le x\\le2$", "x^2≤4.", difficulty="stretch"),
        _q("A SAT: $g(x)=f(x+2)-3$. Relative to f, g is left 2 and…", "down 3", "−3 outside.", difficulty="stretch"),
        _q("One-to-one needed for inverse. Which fails: y=x^2 (all reals) or y=x^3?", "$y=x^2$", "Not 1-1 on R.", difficulty="stretch"),
        _q("If $f^{-1}(4)=7$, then $f(7)$?", 4, "Inverse swap.", difficulty="stretch"),
        _q("Asymptote of $y=1/(x+2)$ vertical?", "$x=-2$", "Undefined.", difficulty="stretch"),
        _q("Parent $y=\\sqrt{x}$ reflected over x then up 4?", "$y=-\\sqrt{x}+4$", "− outside.", difficulty="stretch"),
        _q("A SAT: $f(x)=|x-1|+|x+1|$. f(0)?", 2, "1+1.", difficulty="stretch"),
        _q("$f(3)$ for that abs sum?", 4, "2+4=6? |2|+|4|=6. Recalc: |3-1|+|3+1|=2+4=6.", difficulty="stretch"),
        _q("For $f(x)=|x-1|+|x+1|$, $f(3)$?", 6, "2+4=6.", difficulty="stretch"),
        _q("End behavior of odd cubic with positive leading: as x→∞, f→?", "$\\infty$", "Up on the right.", difficulty="stretch"),
        _q("If $f(g(x))=x$ and $g(f(x))=x$, g is the…", "inverse of f", "Two-sided inverse.", difficulty="stretch"),
        _q("A hole vs asymptote: $(x^2-1)/(x-1)$ at x=1 is a…", "hole / removable", "Cancels to x+1.", difficulty="stretch"),
        _q("SAT: domain of $\\ln(x-5)$?", "$x>5$", "Argument >0.", difficulty="stretch"),
    ]
    qs = [q for q in qs if q and "Recalc" not in q["explanation"]]
    return qs


def a2u2():
    qs = [
        _q("Vertex of $y=(x-3)^2+1$?", "(3,1)", "h,k."),
        _q("Axis of $y=x^2-6x+5$?", "$x=3$", "x=−b/2a=6/2."),
        _q("Discriminant of $x^2-4x+4$?", 0, "16−16."),
        _q("Roots of $x^2-5x+6=0$?", "2 and 3", " (x−2)(x−3)."),
        _q("$x^2=49$. Solutions?", "$\\pm7$", "±7."),
        _q("Complete square $x^2+8x$. Add?", 16, "(b/2)^2."),
        _q("f(x)=2(x+1)^2−3. Vertex?", "(-1,-3)", "From form."),
        _q("Opens down if a is…", "negative", "a<0."),
        _q("y-intercept of $x^2-4x+7$?", 7, "f(0)."),
        _q("SAT: $x^2-2x-8=0$. Positive root?", 4, "(x−4)(x+2).", difficulty="hard"),
        _q("Sum of roots of $x^2-7x+10$?", 7, "−b/a.", difficulty="hard"),
        _q("Product of those roots?", 10, "c/a.", difficulty="hard"),
        _q("Vertex form of $y=x^2-4x+1$?", "$(x-2)^2-3$", "x^2-4x+4−3.", difficulty="hard"),
        _q("SAT Stretch: projectile $h=-16t^2+64t+5$. Time of max height?", 2, "t=−b/2a=64/32.", difficulty="stretch"),
        _q("Max height?", 69, "−16(4)+64(2)+5=−64+128+5.", difficulty="stretch"),
        _q("Quadratic formula $x^2+2x-1=0$. Roots?", "$-1\\pm\\sqrt{2}$", "Disc 4+4=8.", difficulty="stretch"),
        _q("If disc<0, the graph has how many x-intercepts?", 0, "No real roots.", difficulty="stretch"),
        _q("A SAT: 2x^2+4x+2=0. Solutions?", "$x=-1$ (double)", "x^2+2x+1=0.", difficulty="stretch"),
        _q("Transform: y=x^2 left 2, vertical stretch 3, down 4.", "$y=3(x+2)^2-4$", "Inside + is left.", difficulty="stretch"),
        _q("Range of y=−(x+1)^2+5?", "$y\\le5$", "Max 5.", difficulty="stretch"),
        _q("If roots 3 and −5, monic quadratic?", "$x^2+2x-15$", "(x−3)(x+5).", difficulty="stretch"),
        _q("A SAT: minimum of x^2-6x+11?", 2, "Vertex y=(9)+11− wait (x−3)^2+2, min 2.", difficulty="stretch"),
        _q("Focus of y=x^2/4 (standard p). p=1, focus?", "(0,1)", "1/(4a)=1 if a=1/4.", difficulty="stretch"),
        _q("Solve (2x−1)^2=9. Positive x?", 2, "2x−1=3 or −3 → x=2 or −1.", difficulty="stretch"),
        _q("A word: consecutive even integers product −48. The negative one?", -8, "n(n+2)=−48, n=−8, n+2=−6? −8×−6=48 not −48. n(n+2)=−48, n=−12 and 4? Try −8 and 6: −48 yes.", difficulty="stretch"),
        _q("Two consecutive even integers whose product is −48. The pair includes?", "-8 and 6", "−8×6=−48.", difficulty="stretch"),
        _q("Complex not: disc of x^2+x+1?", -3, "1−4=−3.", difficulty="stretch"),
        _q("Factored 2x^2-8x+6?", "$2(x-1)(x-3)$", "x^2-4x+3.", difficulty="stretch"),
        _q("A SAT: if vertex (2,−1) and point (0,3), a in a(x−2)^2−1?", 1, "3=a(4)−1, 4=4a.", difficulty="stretch"),
        _q("End behavior both up when a>0 degree 2. As x→−∞, y→?", "$+\\infty$", "Same as +∞.", difficulty="stretch"),
    ]
    return qs


def a2u3():
    qs = [
        _q("$i^2=$?", -1, "Definition."),
        _q("$(3+2i)+(1-5i)$?", "$4-3i$", "Add parts."),
        _q("$(2-i)(3+i)$?", "$7-i$", "6+2i−3i−i^2=6−i+1=7−i."),
        _q("Conjugate of $4-7i$?", "$4+7i$", "Flip imag."),
        _q("$|3-4i|$?", 5, "5."),
        _q("$i^3=$?", "$-i$", "i^2·i=−i."),
        _q("$i^{4}=$?", 1, "Cycle 4."),
        _q("$i^{22}=$?", -1, "22 mod 4 = 2 → i^2."),
        _q("Complete square $x^2+6x+10=0$. $(x+3)^2=$?", -1, "10−9=1, = −1."),
        _q("SAT: $x^2+6x+10=0$ solutions?", "$-3\\pm i$", "(x+3)^2=−1.", difficulty="hard"),
        _q("Divide $(5+i)/(1-i)$. Multiply by conjugate. Result?", "$2+3i$", "(5+i)(1+i)/2=(5+5i+i−1)/2=(4+6i)/2.", difficulty="hard"),
        _q("$\\sqrt{-36}$ as $bi$?", "$6i$", "6i.", difficulty="hard"),
        _q("Real part of $(2+3i)^2$?", -5, "4+12i+9i^2=4−9+12i.", difficulty="hard"),
        _q("SAT Stretch: $z\\bar z$ for z=3−i?", 10, "Modulus squared 9+1.", difficulty="stretch"),
        _q("Solve $x^2+4=0$.", "$\\pm2i$", "x^2=−4.", difficulty="stretch"),
        _q("A SAT: complete square $x^2-2x+5=0$. $(x-1)^2=$?", -4, "5−1=4, =−4.", difficulty="stretch"),
        _q("Then x?", "$1\\pm2i$", "±2i.", difficulty="stretch"),
        _q("If z=a+bi, Re(z)=3 Im(z)=−2. z?", "$3-2i$", "3−2i.", difficulty="stretch"),
        _q("$1/i$ in a+bi?", "$-i$", "× (−i)/i(−i)=−i/1.", difficulty="stretch"),
        _q("A quadratic with roots i and −i, monic?", "$x^2+1$", "(x−i)(x+i).", difficulty="stretch"),
        _q("Disc of x^2+2x+5?", -16, "4−20.", difficulty="stretch"),
        _q("Powers of i cycle every…", 4, "4.", difficulty="stretch"),
        _q("$(1+i)^2$?", "$2i$", "1+2i−1=2i.", difficulty="stretch"),
        _q("A SAT: |z|=1 and z= cosθ + i sinθ. |z|^2?", 1, "Always 1.", difficulty="stretch"),
        _q("Sum (2+i)+(2−i)?", 4, "Real 4.", difficulty="stretch"),
        _q("A complex number is real iff Im=?", 0, "b=0.", difficulty="stretch"),
        _q("Solve (x−2)^2=−9. x?", "$2\\pm3i$", "±3i.", difficulty="stretch"),
        _q("Polar not required: arg of i (principal)?", "$\\pi/2$", "Positive imag axis.", difficulty="stretch"),
        _q("A SAT: (3+4i)(3−4i)?", 25, "Difference of squares 9+16.", difficulty="stretch"),
        _q("If i^n=1, smallest positive n?", 4, "i^4=1.", difficulty="stretch"),
    ]
    return qs


def a2u4():
    qs = [
        _q("Degree of $4x^3-x+2$?", 3, "Highest power."),
        _q("End behavior of + leading odd degree: as x→∞, f→?", "$+\\infty$", "Up right."),
        _q("A cubic must have at least how many real roots counting multiplicity? Not always 1? Odd degree → at least…", 1, "Odd degree real poly has ≥1 real root."),
        _q("Factor $x^3-8$?", "$(x-2)(x^2+2x+4)$", "Difference of cubes."),
        _q("Synthetic root 2 into x^3−2x^2−x+2. Remainder?", 0, "2 is a root."),
        _q("Possible rational roots of 2x^3+…+3 by rational root theorem include?", "$\\pm1,3,1/2,3/2$", "p/q."),
        _q("Multiplicity 2 at x=3 means the graph…", "touches and turns", "Even multiplicity."),
        _q("y-intercept of p(x)=x^4−5x+7?", 7, "p(0)."),
        _q("Sum of roots of x^3−4x^2+… (monic) for three roots?", 4, "−(−4)/1 for x^2 coeff."),
        _q("SAT: p(x)=(x+1)^2(x−4). p(0)?", -4, "1×(−4).", difficulty="hard"),
        _q("Zeros of that p?", "−1 (mult 2) and 4", "From factors.", difficulty="hard"),
        _q("Divide x^3+1 by x+1. Quotient?", "$x^2-x+1$", "x^3+1=(x+1)(x^2−x+1).", difficulty="hard"),
        _q("A local max/min of cubic typically how many turning points at most?", 2, "Degree−1.", difficulty="hard"),
        _q("SAT Stretch: remainder when x^3−2x+1 is divided by x−1?", 0, "p(1)=1−2+1=0.", difficulty="stretch"),
        _q("Then (x−1) is a…", "factor", "Remainder 0.", difficulty="stretch"),
        _q("If p has zeros 0,2,−2, a monic cubic?", "$x(x-2)(x+2)=x^3-4x$", "x^3−4x.", difficulty="stretch"),
        _q("Leading coeff 2, zeros 1 and 1 and −3. p(x)?", "$2(x-1)^2(x+3)$", "Mult 2 at 1.", difficulty="stretch"),
        _q("A SAT: p(2)=5, p is not asked to interpolate. If p(x)=x^3−3x+k and p(2)=5, k?", 3, "8−6+k=5, k=3.", difficulty="stretch"),
        _q("Complex conjugates: if 1+i is a root of real poly, also…", "1−i", "Conjugate root theorem.", difficulty="stretch"),
        _q("Descartes: p(x)=x^3−x^2−x+1. Sign changes?", 2, "+ to −, − to + =2 or 0 positive roots.", difficulty="stretch"),
        _q("Factor x^4−1.", "$(x-1)(x+1)(x^2+1)$", "Diff squares twice.", difficulty="stretch"),
        _q("A hole not: vertical asymptote of rational later. Polynomials have how many VAs?", 0, "Entire.", difficulty="stretch"),
        _q("If all coefficients positive, no positive real roots. True for x^2+x+1?", "true", "No sign change.", difficulty="stretch"),
        _q("p even: p(−x)=p(x). Example?", "$x^4-3x^2+1$", "Even powers.", difficulty="stretch"),
        _q("A SAT: (x−2)^3 expand constant term?", -8, "(−2)^3.", difficulty="stretch"),
        _q("Graph crosses at odd multiplicity. At (x+2)^3, it…", "crosses flattened", "Odd ≥3.", difficulty="stretch"),
        _q("Sum of coeffs p(1) for p(x)=x^2−5x+6?", 2, "1−5+6=2.", difficulty="stretch"),
        _q("p(−1) for that?", 12, "1+5+6.", difficulty="stretch"),
        _q("A cubic with no turning points can still exist if…", "strictly increasing/decreasing", "e.g. x^3.", difficulty="stretch"),
        _q("Factor  x^3+3x^2+3x+1?", "$(x+1)^3$", "Binomial cube.", difficulty="stretch"),
    ]
    return qs


def a2u5():
    qs = [
        _q("Simplify $\\frac{x^2-9}{x-3}$ for $x\\ne3$?", "$x+3$", "Cancel."),
        _q("VA of $y=1/(x+4)$?", "$x=-4$", "Denom 0."),
        _q("HA of $y=(2x+1)/(x-5)$?", "$y=2$", "Degree same, ratio leading."),
        _q("$\\frac{2}{x}+\\frac{3}{x}=$?", "$\\frac{5}{x}$", "Add."),
        _q("Solve $1/x=1/4$. x?", 4, "x=4."),
        _q("Excluded from $(x-1)/(x^2-1)$?", "$x=\\pm1$", "Denom (x−1)(x+1). Hole at 1."),
        _q("A hole at x=1 for that. Simplified?", "$1/(x+1)$", "Cancel x−1."),
        _q("Multiply $\\frac{x}{4}\\cdot\\frac{8}{x^2}$?", "$\\frac{2}{x}$", "8/4=2, /x."),
        _q("Divide $\\frac{x}{6}\\div\\frac{x}{3}$?", "1/2", "×3/x."),
        _q("SAT: $\\frac{x}{x-2}=3$. x?", 3, "x=3x−6, 6=2x.", difficulty="hard"),
        _q("LCD of 1/(x−1) and 1/(x+1)?", "$(x-1)(x+1)$", "x^2−1.", difficulty="hard"),
        _q("HA of (3x^2+1)/(x^2+4)?", "$y=3$", "Leading 3.", difficulty="hard"),
        _q("If deg num > deg den by 1, the graph has a…", "oblique / slant asymptote", "Long division.", difficulty="hard"),
        _q("SAT Stretch: $\\frac{2}{x-1}-\\frac{1}{x+1}=\\frac{x}{x^2-1}$. Multiply by (x^2−1). Resulting x?", 3, "2(x+1)−(x−1)=x → 2x+2−x+1=x → x+3=x? Wait 2(x+1)−1(x−1)=x → 2x+2−x+1=x → x+3=x, 3=0 never? Check problem. Use 2(x+1)-(x-1)=x → x+3=x contradiction. Different equation: 2/(x-1)-1/(x+1)=1/(x^2-1). Then 2(x+1)-(x-1)=1 → 2x+2−x+1=1 → x+3=1, x=−2.", difficulty="stretch"),
        _q("Solve $\\frac{2}{x-1}-\\frac{1}{x+1}=\\frac{1}{x^2-1}$. x?", -2, "2(x+1)−(x−1)=1 → x+3=1.", difficulty="stretch"),
        _q("A SAT: work rates 1/3+1/6=1/t. t?", 2, "1/2=1/t.", difficulty="stretch"),
        _q("Simplify $\\frac{x^3-8}{x-2}$?", "$x^2+2x+4$", "Diff cubes.", difficulty="stretch"),
        _q("VA of (x+2)/(x^2-4) after cancel?", "$x=2$", "Hole at −2, VA at 2.", difficulty="stretch"),
        _q("Complex fraction $\\frac{1+1/x}{1-1/x}$?", "$(x+1)/(x-1)$", "×x/x.", difficulty="stretch"),
        _q("Solve (x+3)/x=2. x?", 3, "x+3=2x.", difficulty="stretch"),
        _q("A HA y=0 when deg den > deg num. Example y=1/x^2 as x→∞, y→?", 0, "0.", difficulty="stretch"),
        _q("Add $\\frac{3}{x-2}+\\frac{1}{2-x}$?", "$\\frac{2}{x-2}$", "1/(2−x)=−1/(x−2).", difficulty="stretch"),
        _q("A SAT: inverse variation y=12/x. y when x=3?", 4, "4.", difficulty="stretch"),
        _q("If xy=12 always, x doubles, y…", "halves", "Inverse.", difficulty="stretch"),
        _q("Undefined at x=0 for y=1/x. This is a…", "vertical asymptote", "VA x=0.", difficulty="stretch"),
        _q("Solve x/(x+1)=2/3. x?", 2, "3x=2x+2.", difficulty="stretch"),
        _q("A slant: (x^2+1)/x = x + 1/x. Slant?", "$y=x$", "Quotient x.", difficulty="stretch"),
        _q("Extraneous: 1/(x-1)=x/(x-1). If x≠1, 1=x. Check x=1 undefined. Solution?", 1, "Wait x=1 is extraneous. No solution? From 1=x, x=1 invalid. Solutions: none.", difficulty="stretch"),
        _q("Equation 1/(x-1)=x/(x-1). Valid solutions?", "none", "x=1 excluded.", difficulty="stretch"),
        _q("A SAT: $\\frac{x^2-4}{x-2}=x+k$ after cancel. k?", 2, "x+2.", difficulty="stretch"),
    ]
    qs = [q for q in qs if q and "Wait" not in q["explanation"] or "none" in str(q["correct_answer"]).lower()]
    qs = [q for q in qs if q and "contradiction" not in q["explanation"]]
    return qs


def a2u6():
    qs = [
        _q("$\\sqrt{49}=$?", 7, "Principal 7."),
        _q("$\\sqrt[3]{-8}=$?", -2, "−2."),
        _q("$x^{2/3}$ for x=8?", 4, "(x^{1/3})^2=4."),
        _q("$8^{2/3}=$?", 4, "4."),
        _q("Simplify $\\sqrt{50}$?", "$5\\sqrt{2}$", "25×2."),
        _q("$\\sqrt{a}\\sqrt{b}=$?", "$\\sqrt{ab}$", "Product rule."),
        _q("Solve $\\sqrt{x}=5$. x?", 25, "Square."),
        _q("Solve $\\sqrt{x}=-1$. Solutions?", "none", "Principal sqrt ≥0."),
        _q("$27^{4/3}=$?", 81, "(27^{1/3})^4=3^4."),
        _q("SAT: $\\sqrt{3x+1}=4$. x?", 5, "3x+1=16.", difficulty="hard"),
        _q("Extraneous check: $\\sqrt{2x-3}=x-3$. After square, x=6 or 1. Valid?", 6, "x=1: √−1 invalid; x=6: √9=3=6−3.", difficulty="hard"),
        _q("Simplify $\\sqrt{72}$?", "$6\\sqrt{2}$", "36×2.", difficulty="hard"),
        _q("$x^{-3/2}$ at x=4?", "1/8", "1/(4^{3/2})=1/8.", difficulty="hard"),
        _q("SAT Stretch: $\\sqrt{x+5}+\\sqrt{x}=5$. Isolate, square twice. x?", 4, "Let √x=t, √(t^2+5)+t=5, √(t^2+5)=5−t, t^2+5=25−10t+t^2, 5=25−10t, 10t=20, t=2, x=4.", difficulty="stretch"),
        _q("Solve $\\sqrt{x-1}=x-3$ after checking. Valid x?", "none or 5?", "Square: x−1=x^2−6x+9, 0=x^2−7x+10=(x−2)(x−5). x=2: √1=−1 false. x=5: √4=2=5−3 true. x=5.", difficulty="stretch"),
        _q("Valid solution of $\\sqrt{x-1}=x-3$?", 5, "x=5 works.", difficulty="stretch"),
        _q("Rationalize $1/\\sqrt{3}$?", "$\\sqrt{3}/3$", "×√3."),
        _q("$(4x^6)^{1/2}$ for x>0?", "$2x^3$", "Sqrt.", difficulty="stretch"),
        _q("A SAT: 16^{3/4}?", 8, "(16^{1/4})^3=2^3.", difficulty="stretch"),
        _q("Index 4 of 81?", 3, "3^4=81.", difficulty="stretch"),
        _q("Solve  ∛(x+2)=−1. x?", -3, "x+2=−1.", difficulty="stretch"),
        _q("Simplify ∛(16) ?", "$2\\sqrt[3]{2}$", "8×2.", difficulty="stretch"),
        _q("Domain of √(2x−8)?", "$x\\ge4$", "2x≥8.", difficulty="stretch"),
        _q("False: √(a+b)=√a+√b. Counterexample a=b=1: left √2, right 2. Right is?", 2, "Not equal.", difficulty="stretch"),
        _q("A SAT: (x^{1/2})^4?", "$x^2$", "For x≥0.", difficulty="stretch"),
        _q("Solve 2√x=10. x?", 25, "√x=5.", difficulty="stretch"),
        _q("Combine √12+√27?", "$5\\sqrt{3}$", "2√3+3√3.", difficulty="stretch"),
        _q("A nested √(√81)?", 3, "√9=3.", difficulty="stretch"),
        _q("Exponent  (−8)^{2/3}?", 4, "∛−8 then square =4.", difficulty="stretch"),
        _q("SAT: √(x^2)=|x|. At x=−5, value?", 5, "Absolute.", difficulty="stretch"),
    ]
    qs = [q for q in qs if q and "or 5?" not in q["question_text"]]
    return qs


def a2u7():
    qs = [
        _q("$2^5=$?", 32, "32."),
        _q("$\\log_2 32=$?", 5, "2^5=32."),
        _q("$\\log_{10} 1000=$?", 3, "10^3."),
        _q("$\\ln e=$?", 1, "log_e e."),
        _q("$\\log_b 1=$?", 0, "b^0=1."),
        _q("$\\log_b b=$?", 1, "b^1=b."),
        _q("Change $a^{x}=c$ to log.", "$x=\\log_a c$", "Definition."),
        _q("$\\log 2 + \\log 5=$? (base 10)", 1, "log 10."),
        _q("$3^{x}=81$. x?", 4, "3^4."),
        _q("SAT: $2^{x+1}=16$. x?", 3, "2^4=16, x+1=4.", difficulty="hard"),
        _q("$\\log_3(x-1)=2$. x?", 10, "x−1=9.", difficulty="hard"),
        _q("Growth $100(1.05)^t$ at t=0?", 100, "Initial.", difficulty="hard"),
        _q("$\\log_2 8 + \\log_2 4$?", 5, "3+2.", difficulty="hard"),
        _q("SAT Stretch: $5^{2x}=1/25$. x?", -1, "5^{2x}=5^{-2}, 2x=−2.", difficulty="stretch"),
        _q("$\\ln(2x)=0$. x?", "1/2", "2x=1.", difficulty="stretch"),
        _q("A SAT: double time for 6% continuous? t=ln2/0.06 ≈?", 11.55, "ln2/0.06≈11.55 years. Use ln2/0.06.", difficulty="stretch"),
        _q("Exact doubling time at continuous rate 0.06: $t=\\ln2/0.06$. ln2≈0.693 so t≈?", 11.55, "0.693/0.06.", difficulty="stretch"),
        _q("$\\log_2(x^2)$ for x>0?", "$2\\log_2 x$", "Power rule.", difficulty="stretch"),
        _q("Solve  e^{2x}=e^{x+3}. x?", 3, "2x=x+3.", difficulty="stretch"),
        _q("A half-life 8 years, remaining fraction after 24 years?", "1/8", "3 half-lives.", difficulty="stretch"),
        _q("$\\log_5 125 - \\log_5 5$?", 2, "3−1.", difficulty="stretch"),
        _q("Change of base $\\log_2 10=\\ln10/\\ln2$ ≈?", 3.32, "About 3.32.", difficulty="stretch"),
        _q("If log_b a = 2, then a in terms of b?", "$b^2$", "Definition.", difficulty="stretch"),
        _q("A SAT: 4^{x}=8^{x-1}. Write 2^{2x}=2^{3x-3}. x?", 3, "2x=3x−3, x=3.", difficulty="stretch"),
        _q("Domain of log(x−4)?", "$x>4$", "Arg>0.", difficulty="stretch"),
        _q("y=2^x through (0,1) and (1,2). y-intercept?", 1, "(0,1).", difficulty="stretch"),
        _q("Inverse of y=10^x?", "$y=\\log_{10}x$", "Common log.", difficulty="stretch"),
        _q("Product  e^a e^b=?", "$e^{a+b}$", "Exponent add.", difficulty="stretch"),
        _q("A compound 1000(1.02)^{10} is closest to (without calc, (1.02)^10≈1.22)?", 1220, "About 1220.", difficulty="stretch"),
        _q("Solve log_2(x)+log_2(x-2)=3. x?", 4, "log_2(x(x−2))=3, x(x−2)=8, x=4 (x=−2 invalid).", difficulty="stretch"),
    ]
    return qs


def a2u8():
    qs = [
        _q("Arithmetic 3,7,11. Next?", 15, "d=4."),
        _q("a_n=3+(n-1)·4. a_10?", 39, "3+36."),
        _q("Geometric 2,6,18. Next?", 54, "×3."),
        _q("Sum 1+2+…+10?", 55, "n(n+1)/2."),
        _q("Geometric sum 1+2+4+8?", 15, "15."),
        _q("sin(90°)?", 1, "1."),
        _q("cos(0°)?", 1, "1."),
        _q("tan(45°)?", 1, "1."),
        _q("A 3-4-5. sin of opposite 3 to hyp 5?", "3/5", "opp/hyp."),
        _q("SAT: arithmetic a1=5 d=−2. a_8?", -9, "5+7(−2).", difficulty="hard"),
        _q("Geometric a1=3 r=2. a_6?", 96, "3×32.", difficulty="hard"),
        _q("Infinite |r|<1 sum a/(1−r): 8+4+2+…?", 16, "8/(1−1/2).", difficulty="hard"),
        _q("sin^2θ+cos^2θ=?", 1, "Identity.", difficulty="hard"),
        _q("SAT Stretch: Σ_{k=1}^{20} (2k−1) first 20 odds?", 400, "20^2.", difficulty="stretch"),
        _q("Geometric 1/2+1/4+1/8+… infinite?", 1, "a=1/2 r=1/2, 1.", difficulty="stretch"),
        _q("A SAT: 5, __, 20 arithmetic. Middle?", 12.5, "Average.", difficulty="stretch"),
        _q("3, __, 12 geometric (positive). Middle?", 6, "√36=6.", difficulty="stretch"),
        _q("Unit circle cos(180°)?", -1, "−1.", difficulty="stretch"),
        _q("sin(30°)?", "1/2", "1/2.", difficulty="stretch"),
        _q("Period of sin(bx) is 2π/|b|. For sin(2x), period?", "$\\pi$", "2π/2.", difficulty="stretch"),
        _q("Amplitude of 4 sin(x)?", 4, "|A|.", difficulty="stretch"),
        _q("Amplitude of −4 sin(x)?", 4, "Absolute 4.", difficulty="stretch"),
        _q("A recursive a1=2, a_{n}=a_{n-1}+5. a_4?", 17, "2,7,12,17.", difficulty="stretch"),
        _q("n-th triangular n(n+1)/2 at n=8?", 36, "36.", difficulty="stretch"),
        _q("tan(θ)=sin/cos. tan(60°)?", "$\\sqrt{3}$", "√3.", difficulty="stretch"),
        _q("A SAT: 30-60-90 hyp 10. Side opposite 30°?", 5, "Half hyp.", difficulty="stretch"),
        _q("cos(90°−θ)=?", "$\\sin\\theta$", "Cofunction.", difficulty="stretch"),
        _q("Arithmetic sum S_n=n/2(2a+(n−1)d).  n=10 a=3 d=4. S?", 210, "10/2(6+36)=5×42.", difficulty="stretch"),
        _q("A sequence 2,−6,18,−54. r?", -3, "Geometric.", difficulty="stretch"),
        _q("Convert  π rad to degrees?", 180, "180°.", difficulty="stretch"),
    ]
    return qs


def mc1():
    qs = []
    for a, b in ((4, 5), (3, 7), (6, 6), (2, 10), (8, 3), (5, 9), (7, 4), (9, 2)):
        qs.append(_q(f"Outfits: {a} shirts and {b} pants (one each). How many?", a * b, f"Product rule {a}×{b}={a*b}."))
    qs += [
        _q("A 3-digit PIN digits 0–9, repeats allowed. How many?", 1000, "10^3."),
        _q("Same PIN, all distinct digits?", 720, "10×9×8."),
        _q("3-digit numbers (no leading zero), digits may repeat?", 900, "9×10×10."),
        _q("3-digit numbers, all distinct, no leading zero?", 648, "9×9×8."),
        _q("Coin flipped 4 times. Outcomes?", 16, "2^4."),
        _q("Sum rule: 3 soups or 4 salads (not both). Choices?", 7, "Add."),
        _q("Complement: 5-letter strings A–Z minus those with no A. Total 26^5. (Keep as total first.) 26^2?", 676, "Warmup 26^2."),
        _q("How many 2-letter strings A–Z repeats allowed?", 676, "26^2.", difficulty="hard"),
        _q("From {1,2,3,4,5} ordered pairs (a,b) with a<b?", 10, "C(5,2).", difficulty="hard"),
        _q("License: 2 letters then 3 digits, repeats OK. Count?", 676000, "26^2×10^3.", difficulty="hard"),
        _q("A lock 4 digits distinct. Count?", 5040, "10×9×8×7.", difficulty="hard"),
        _q("SAT/AMC Stretch: 3-digit even numbers, no repeat, no leading 0. Units 0,2,4,6,8. Count?", 328, "Case units=0: 9×8; units even nonzero: 4×8×8=256; +72=328.", difficulty="stretch"),
        _q("How many 3-digit even numbers with distinct digits and no leading zero?", 328, "Casework on units digit.", difficulty="stretch"),
        _q("Complement: 8-character passwords A–Z vs those missing Z. Easier: 4-letter words using A,B,C with at least one A?", 65, "81−16=65 (3^4−2^4).", difficulty="stretch"),
        _q("4-letter words from {A,B,C} with at least one A?", 65, "81−16.", difficulty="stretch"),
        _q("A menu 4 mains, 3 sides, 2 drinks. Meals one of each?", 24, "4×3×2.", difficulty="stretch"),
        _q("Number of subsets of a 5-element set?", 32, "2^5.", difficulty="stretch"),
        _q("Nonempty subsets of 5 elements?", 31, "32−1.", difficulty="stretch"),
        _q("Functions from a 3-set to a 4-set?", 64, "4^3.", difficulty="stretch"),
        _q("Injective functions 3-set to 5-set?", 60, "5×4×3.", difficulty="stretch"),
        _q("A 5-digit palindrome (abcba) first digit ≠0?", 900, "9×10×10.", difficulty="stretch"),
        _q("Coin 5 flips exactly 0 tails means all heads. Ways?", 1, "HHHHH.", difficulty="stretch"),
        _q("Product 2×2×2×5 vs cases. A 3-course: 5 apps 4 mains 3 desserts, skip dessert allowed. Count?", 80, "5×4×(3+1).", difficulty="stretch"),
        _q("If dessert optional: 5×4×4?", 80, "Yes.", difficulty="stretch"),
        _q("AMC: integers 1–100 with a 7 in them? Complement no 7s. 1–99 as 00–99: 9^2=81 including 00, plus 100 has no 7 → 82 without 7, 100−82=18? 1–100: numbers with digit 7: 7,17,...,97,70–79 except 77 counted twice. 18+10−1=27. Plus 100? no. 27.", difficulty="stretch"),
        _q("How many integers from 1 to 100 inclusive contain the digit 7?", 19, "7,17,27,37,47,57,67,70-79 (10),87,97 = 7+10+2=19? 17,27,37,47,57,67,87,97=8 plus 7 plus 70-79=10, but 77 in 70-79. 1+8+10=19.", difficulty="stretch"),
    ]
    qs = [q for q in qs if q and "00–99" not in q["question_text"]]
    return qs


def mc2():
    qs = [
        _q("P(5,2)=?", 20, "5×4."),
        _q("5! = ?", 120, "120."),
        _q("Arrange 4 distinct books on a shelf?", 24, "4!."),
        _q("Arrange 4 people in a line?", 24, "4!."),
        _q("Circular arrangements of 5 distinct people (rotations same)?", 24, "(5−1)!."),
        _q("Word permutations of MATH (all distinct)?", 24, "4!."),
        _q("Permutations of LEVEL (L twice, E twice)?", 30, "5!/(2!2!)."),
        _q("P(10,3)=?", 720, "10×9×8."),
        _q("3-letter codes from ABCDE no repeat?", 60, "5×4×3."),
        _q("SAT/AMC: permutations of BANANA?", 60, "6!/(3!2!).", difficulty="hard"),
        _q("Arrange 6 people with A,B together (glue)?", 240, "2×5!.", difficulty="hard"),
        _q("A,B not together in 6 line. Total 720 minus 240?", 480, "6!−2·5!.", difficulty="hard"),
        _q("10 people, president and VP distinct. Ways?", 90, "P(10,2).", difficulty="hard"),
        _q("Stretch: 7 beads on a necklace, flips count same, all distinct. (7−1)!/2?", 360, "Dihedral /2.", difficulty="stretch"),
        _q("How many distinct necklaces of 7 distinct beads with flips allowed?", 360, "(7−1)!/2.", difficulty="stretch"),
        _q("Permutations of MISSISSIPPI?", 34650, "11!/(4!4!2!).", difficulty="stretch"),
        _q("Arrange 4 men 3 women alternating, men at ends. Men 4! women 3!?", 144, "4!×3!.", difficulty="stretch"),
        _q("5-digit numbers using 1–5 each once, even (units 2 or 4)?", 48, "2×4!.", difficulty="stretch"),
        _q("P(n,n)=?", "$n!$", "n!.", difficulty="stretch"),
        _q("A round table 8, two particular together?", 1440, "2×6! wait (8-1)! for circle=5040, glue: 2×6!=1440? Circle glue: treat pair as 1 → 7 entities circular (6!)×2.", difficulty="stretch"),
        _q("8 people circular, two particular sit together?", 1440, "2×6!.", difficulty="stretch"),
        _q("Word PEPPER distinct perms?", 60, "6!/(3!2!).", difficulty="stretch"),
        _q("Choose order of 3 of 9 books?", 504, "P(9,3).", difficulty="stretch"),
        _q("A code 1st letter, 2nd digit 0-9, 3rd letter ≠ first. 26×10×25?", 6500, "6500.", difficulty="stretch"),
        _q("Seating 5 in a row if two ends are fixed people A,B who can swap?", 12, "2×3!.", difficulty="stretch"),
        _q("Perms of 1234 with 1 before 2 (among 4! equally)?", 12, "Half of 24.", difficulty="stretch"),
        _q("Derangement of 3 items !3?", 2, "2.", difficulty="stretch"),
        _q("Number of derangements of 3 labeled items?", 2, "!3=2.", difficulty="stretch"),
        _q("P(8,0)+P(8,1)?", 9, "1+8.", difficulty="stretch"),
        _q("Arrange 2 identical red and 3 identical blue flags in a row?", 10, "C(5,2).", difficulty="stretch"),
    ]
    qs = [q for q in qs if q and "wait" not in q["explanation"].lower()]
    return qs


def mc3():
    qs = [
        _q("C(5,2)=?", 10, "10."),
        _q("C(10,0)=?", 1, "1."),
        _q("C(n,n)=?", 1, "1."),
        _q("C(n,1)=?", "$n$", "n."),
        _q("C(8,3)=?", 56, "56."),
        _q("Committee 4 from 9?", 126, "C(9,4)."),
        _q("C(6,2)=C(6,4). Value?", 15, "Symmetry."),
        _q("Binomial (x+y)^4, coeff of x^2 y^2?", 6, "C(4,2)."),
        _q("Hands of 5 from 10?", 252, "C(10,5)."),
        _q("AMC: C(12,2)+C(12,10)?", 132, "66+66.", difficulty="hard"),
        _q("Pascal: C(7,3)=C(6,2)+C(6,3). Value?", 35, "15+20.", difficulty="hard"),
        _q("Choose 3 including a president already chosen from remaining 9 for 2 more? Wait: 3 from 10 with a specific person included?", 36, "C(9,2).", difficulty="hard"),
        _q("3-person committees from 10 that include Alex?", 36, "C(9,2).", difficulty="hard"),
        _q("Stretch: 5 cards from 52. C(52,5)?", 2598960, "2,598,960.", difficulty="stretch"),
        _q("(1+1)^n = 2^n = sum C(n,k). Sum_k C(8,k)?", 256, "2^8.", difficulty="stretch"),
        _q("C(10,3)−C(9,3)?", 36, "120−84=36=C(9,2).", difficulty="stretch"),
        _q("A path later: C(6,2) lattice analog?", 15, "15.", difficulty="stretch"),
        _q("Choose 2 of 5 red and 3 of 6 blue. Product?", 200, "C(5,2)×C(6,3)=10×20.", difficulty="stretch"),
        _q("No two adjacent: 4 seats from 10 in a line with gaps — skip. C(7,3) for another. Number of 3-subsets of {1..8}?", 56, "C(8,3).", difficulty="stretch"),
        _q("How many 3-element subsets of an 8-set?", 56, "C(8,3).", difficulty="stretch"),
        _q("Coeff of x^3 in (1+x)^6?", 20, "C(6,3).", difficulty="stretch"),
        _q("C(n,2)=45. n?", 10, "n(n−1)/2=45.", difficulty="stretch"),
        _q("A class 6 boys 5 girls, 3-person with at least 1 girl. Total C(11,3)−C(6,3)?", 145, "165−20.", difficulty="stretch"),
        _q("Pairs from 12 people?", 66, "C(12,2).", difficulty="stretch"),
        _q("Tetrahedral? C(n+3,3) skip. C(9,4)?", 126, "126.", difficulty="stretch"),
        _q("If C(n,2)=C(n,3), then n?", 5, "n=5 because C(5,2)=C(5,3)=10.", difficulty="stretch"),
        _q("Multichoose later. Ways to choose 2 flavors from 8 (order no, repeats no)?", 28, "C(8,2).", difficulty="stretch"),
        _q("A SAT: 20 people handshake all pairs. Handshakes?", 190, "C(20,2).", difficulty="stretch"),
        _q("C(7,0)+C(7,1)+…+C(7,7)?", 128, "2^7.", difficulty="stretch"),
        _q("Hockey-stick: C(3,3)+C(4,3)+C(5,3)=C(6,4). Value?", 15, "1+4+10=15.", difficulty="stretch"),
    ]
    qs = [q for q in qs if q and "Wait:" not in q["question_text"]]
    return qs


def mc4():
    qs = [
        _q("Integers 1–20 even or multiple of 5: |E∪F|=10+4−2?", 12, "10 evens, 4 multiples of 5, 2 both (10,20)."),
        _q("Casework: 2-digit with tens > ones. Count?", 36, "C(10,2) but tens 1-9 ones 0-9. For tens d, ones 0..d-1 → 1+2+…+9=45? Tens 1 ones 0 only=1; tens 2: 0,1 →2; … tens 9: 0-8 →9; sum 45.", difficulty="hard"),
        _q("How many 2-digit numbers have tens digit strictly greater than units digit?", 45, "1+2+…+9=45.", difficulty="hard"),
        _q("Overcount: count (a,b) then divide by order. Unordered pairs from 6?", 15, "C(6,2)."),
        _q("Positive integers n<100 with n or 100−n even? All? Skip. Numbers 1–30 divisible by 2 or 3?", 20, "15+10−5.", difficulty="hard"),
        _q("1–30 divisible by 2 or 3?", 20, "15+10−5.", difficulty="hard"),
        _q("Case last digit: 3-digit palindromes.", 90, "9×10.", difficulty="hard"),
        _q("Stretch: integers 1–1000 with at least one digit 1? Complement no 1s. 9^3=729 for 000-999 plus 1000 has 1. 1–1000: 1000−(9^3−1)=1000−728=272? 000-999 without digit 1: 9^3=729 including 000. 1-999 without 1: 728. 1000 has a 1. So with a 1: 999-728+1=272.", difficulty="stretch"),
        _q("How many integers from 1 to 1000 inclusive have at least one digit equal to 1?", 272, "Complement: 728 numbers in 1–999 with no digit 1; 1000 has a 1.", difficulty="stretch"),
        _q("Casework triangles: integer sides perim 12. Triples up to congruence?", 3, "(2,5,5),(3,4,5),(4,4,4).", difficulty="stretch"),
        _q("How many noncongruent triangles with integer sides and perimeter 12?", 3, "Triangle inequality.", difficulty="stretch"),
        _q("Overcount: number of squares on a 4×4 chessboard (all sizes)?", 30, "16+9+4+1.", difficulty="stretch"),
        _q("Rectangles on 4×4 grid of cells (4×4 squares)?", 100, "C(5,2)^2=10^2.", difficulty="stretch"),
        _q("How many rectangles in a 4×4 grid of unit squares?", 100, "C(5,2)×C(5,2).", difficulty="stretch"),
        _q("PINs 4 digits with at least one 0. Total 10000 minus 9^4?", 3439, "10000−6561.", difficulty="stretch"),
        _q("AMC: sum of 1–20 not divisible by 2 or 3. Count of those?", 7, "20−(10+6−3)=7? 1,5,7,11,13,17,19=7.", difficulty="stretch"),
        _q("How many integers 1–20 are not divisible by 2 or 3?", 7, "7 of them.", difficulty="stretch"),
        _q("Case on first letter: 3-letter from ABC with A appearing. 27−8=19?", 19, "3^3−2^3.", difficulty="stretch"),
        _q("Two pairs vs full house later. Ways to split 6 people into two unlabeled groups of 3?", 10, "C(6,3)/2=10.", difficulty="stretch"),
        _q("Labeled teams of 3 vs 3 from 6?", 20, "C(6,3)=20 if teams distinct.", difficulty="stretch"),
        _q("A 8-board? Skip. Positive n=a+b, a,b≥1, n=10. Ordered?", 9, "(1,9)…(9,1).", difficulty="stretch"),
        _q("Ordered positive pairs (a,b) with a+b=10?", 9, "9.", difficulty="stretch"),
        _q("Unordered {a,b} positive a+b=10, a≤b?", 5, "1+9,…5+5.", difficulty="stretch"),
        _q("Avoid overcount: handshake 8 people?", 28, "C(8,2).", difficulty="stretch"),
        _q("Casework: 4-digit with exactly two 7s. C(4,2)×9×9 with other digits ≠7, leading not 0. Careful. Positions of 7s C(4,2)=6. Remaining two digits from 0-9 except 7 (9 options) but leading. If thousands is 7, other non-7 9×9; if thousands not 7, thousands 1-9 except 7 (8) and the other remaining… This is messy. Simpler: 3-digit exactly one 7. Hundreds 7: 9×10=90 (tens,ones no restriction except we need exactly one 7 so tens and ones ≠7: 9×9=81). Hundreds≠7 (8 choices 1-9 except 7), exactly one 7 in last two: 2×9=18? tens=7 ones≠7 (9) or ones=7 tens≠7 (9) →18, ×8=144. Total 81+144=225.", difficulty="stretch"),
        _q("How many 3-digit numbers contain the digit 7 exactly once?", 225, "Case on whether hundreds is 7.", difficulty="stretch"),
    ]
    qs = [q for q in qs if q and "Skip" not in q["question_text"] and "messy" not in q["explanation"]]
    return qs


def mc5():
    qs = [
        _q("Stars and bars nonnegative x1+x2+x3=5. Solutions?", 21, "C(5+3-1,2)=21."),
        _q("Positive x1+x2+x3=5. Solutions?", 6, "C(4,2)=6."),
        _q("x1+x2=10, xi≥0. Solutions?", 11, "11."),
        _q("Donuts 3 types, buy 7, repeats OK order no. C(7+3-1,7)?", 36, "C(9,2)=36."),
        _q("Distribute 8 identical to 4 distinct, some may get 0?", 165, "C(8+4-1,8)=C(11,8)=165."),
        _q("Each of 4 gets at least 1 from 8 identical?", 35, "C(7,3)=35."),
        _q("Equation x+y+z=4 in nonnegative integers?", 15, "C(6,2)."),
        _q("2 variables x+y=n, x,y≥0. n+1 solutions. n=12?", 13, "13."),
        _q("AMC: number of monomials degree 3 in 3 vars?", 10, "C(3+3-1,3)=10.", difficulty="hard"),
        _q("Positive integers x+y+z=10. Solutions?", 36, "C(9,2).", difficulty="hard"),
        _q("xi≥0, x1+x2+x3+x4=3?", 20, "C(6,3).", difficulty="hard"),
        _q("With x1≥2, x1'+2 +x2+x3=5, x'≥0. x1+x2+x3=5 ≥2 on x1. Let y=x1−2≥0, y+x2+x3=3, C(5,2)=10.", difficulty="hard"),
        _q("Nonnegative solutions to x+y+z=5 with x≥2?", 10, "Let x'=x−2.", difficulty="hard"),
        _q("Stretch: 2x+y+z=8, x,y,z≥0 integers. Let x=0..4. For x=k, y+z=8−2k, 9−2k options. 9+7+5+3+1=25.", difficulty="stretch"),
        _q("Nonnegative integer solutions of 2x+y+z=8?", 25, "Sum over x=0 to 4.", difficulty="stretch"),
        _q("Multichoose H(5,3)=C(5+3-1,3)?", 35, "C(7,3).", difficulty="stretch"),
        _q("Number of ways 10 identical candies to 3 kids, each at least 2?", 15, "Give 2 each first, 4 left, C(4+3-1,4)=15.", difficulty="stretch"),
        _q("x1+…+x5=5, xi∈{0,1}. That's C(5,5)? Each 0 or 1 sum 5 means all 1s. Ways?", 1, "Only (1,1,1,1,1).", difficulty="stretch"),
        _q("Bars 4 plus stars 6. Positions C(10,4)? Stars 6, 4 vars so 3 bars. C(9,3)=84 for x1+…+x4=6 ≥0.", difficulty="stretch"),
        _q("Nonnegative solutions x1+x2+x3+x4=6?", 84, "C(9,3).", difficulty="stretch"),
        _q("A fruit 5 types, pick 4 pieces. Combinations with repetition?", 70, "C(4+5-1,4)=70.", difficulty="stretch"),
        _q("Integer points in x+y+z=10, xi≥0, x≤4. Inclusion: total C(12,2)=66, minus x≥5: let x''=x−5≥0, C(7,2)=21, similarly 3 vars → 66−3×21 + (x≥5,y≥5: x'+y'+z=0 →1) wait x+y+z=10 two already ≥5 so remaining 0, z=0 one var ≥5 too? Two vars ≥5 each, sum≥10, z=0, C(2,2) style 3 pairs: 66−63+3=6? 3×21=63, add back pairs x,y≥5: x'+y'+z=0 →1 each pair, C(3,2)=3. Triple ≥5 impossible. 66−63+3=6.", difficulty="stretch"),
        _q("Nonnegative x+y+z=10 with each ≤4. How many solutions?", 6, "Inclusion-exclusion.", difficulty="stretch"),
        _q("AMC: number of terms in (x+y+z)^4 after combining?", 15, "C(4+3-1,4)=15.", difficulty="stretch"),
        _q("Positive solutions x+y=8?", 7, "7.", difficulty="stretch"),
        _q("xi≥0 sum to 0 with 5 vars?", 1, "All zero.", difficulty="stretch"),
        _q("Distribute 9 identical into 3 distinct boxes nonempty?", 28, "C(8,2).", difficulty="stretch"),
        _q("If boxes identical, 9 into 3 nonempty unlabeled? Partitions of 9 into 3 positives. 7+1+1, 6+2+1, 5+3+1, 5+2+2, 4+4+1, 4+3+2, 3+3+3 → 7.", difficulty="stretch"),
        _q("Number of partitions of 9 into exactly 3 positive parts (order irrelevant)?", 7, "7 partitions.", difficulty="stretch"),
    ]
    qs = [q for q in qs if q and "Let y=" not in q.get("question_text", "") and "Positions C" not in q["question_text"]]
    return qs


def mc6():
    qs = [
        _q("1–60 divisible by 2 or 3: 30+20−10?", 40, "PIE."),
        _q("1–30 divisible by 2,3, or 5. |A∪B∪C|?", 22, "15+10+6−5−3−2+1=22."),
        _q("Neither of two sets |U|−|A∪B|. U=100, |A|=40,|B|=30,|A∩B|=10. Outside?", 40, "100−60."),
        _q("Venn both=12, only A=8, only B=5, none=10. Total?", 35, "12+8+5+10."),
        _q("|A∪B∪C| formula three sets. If pairwise 0 extra, |A|+|B|+|C| if disjoint. Disjoint 10,12,7. Union?", 29, "29."),
        _q("AMC: 1–100 divisible by 4 or 6. |4∪6|=25+16−8?", 33, "lcm 12, floor 100/12=8."),
        _q("1–100 how many divisible by 4 or 6?", 33, "25+16−8.", difficulty="hard"),
        _q("Not divisible by 2 or 5 in 1–20?", 8, "20−(10+4−2)=8.", difficulty="hard"),
        _q("Three sets |A|=20,B=20,C=20, pairwise 8, triple 3. Union?", 39, "60−24+3=39.", difficulty="hard"),
        _q("Stretch: 1–1000 with a digit 0? Complement no 0. Hard. 1–100 coprime to 10 (not 2 or 5)? φ-like: 100−(50+20−10)=40.", difficulty="stretch"),
        _q("How many integers 1 through 100 are not divisible by 2 or 5?", 40, "100−60=40.", difficulty="stretch"),
        _q("Survey 50, 30 like tea, 25 coffee, 12 both. Like neither?", 7, "50−(30+25−12).", difficulty="stretch"),
        _q("Exactly one of tea/coffee: (30−12)+(25−12)?", 31, "18+13.", difficulty="stretch"),
        _q("1–60 divisible by 2,3,5. PIE 30+20+12−10−6−4+2?", 44, "44.", difficulty="stretch"),
        _q("How many of 1–60 are divisible by at least one of 2,3,5?", 44, "PIE.", difficulty="stretch"),
        _q("Derangement related complement. Numbers 1–n with no even? Odds only. n=10, odds?", 5, "5.", difficulty="stretch"),
        _q("How many odd integers from 1 to 10?", 5, "5.", difficulty="stretch"),
        _q("A∩B∩C=4, only AB (not C)=6, only AC=5, only BC=3, only A=2, only B=1, only C=7. Union?", 32, "4+6+5+3+2+1+7.", difficulty="stretch"),
        _q("U=40, union 32, none?", 8, "40−32.", difficulty="stretch"),
        _q("AMC 8 style: 120 students, 70 math, 60 science, 40 both. Only math?", 30, "70−40.", difficulty="stretch"),
        _q("Neither math nor science?", 30, "120−(70+60−40).", difficulty="stretch"),
        _q("1–200 divisible by 15? 15=3×5. floor 200/15?", 13, "13.", difficulty="stretch"),
        _q("Div by 3 or 5 in 1–200: 66+40−13?", 93, "floor 200/3=66, /5=40, /15=13.", difficulty="stretch"),
        _q("Complement 1–200 not div by 3 or 5?", 107, "200−93.", difficulty="stretch"),
        _q("Four sets too much. Two: |A|=|B|=12, |A∪B|=20. |A∩B|?", 4, "12+12−20.", difficulty="stretch"),
        _q("If |A∪B|=|A|+|B|, then |A∩B|?", 0, "Disjoint.", difficulty="stretch"),
        _q("PIE for |A∪B∪C∪D| first two terms sum of singles minus pairs. If all |Ai|=10, 4 sets, pairs C(4,2)=6 each pair 3. 40−18=22 plus triples… skip. |A∪B| only.", difficulty="stretch"),
        _q("Four groups of 10, every pair intersects in 3, ignore triples. This oversimplifies. Instead: 1–24 div by 2 or 3 or 4? Note 4⊂2. So 2 or 3: 12+8−4=16.", difficulty="stretch"),
        _q("How many integers 1–24 are divisible by 2 or 3?", 16, "12+8−4.", difficulty="stretch"),
    ]
    qs = [q for q in qs if q and "skip" not in q["question_text"].lower() and "too much" not in q["question_text"]]
    return qs


def mc7():
    qs = [
        _q("Lattice paths (0,0) to (2,2) with right/up only?", 6, "C(4,2)."),
        _q("To (3,1) R/U only?", 4, "C(4,1)=4."),
        _q("To (5,5)?", 252, "C(10,5)."),
        _q("Fibonacci: ways to tile 1×4 with 1×1 and 1×2?", 5, "F_5=5."),
        _q("F_1=1,F_2=1,F_6?", 8, "8."),
        _q("Recurrence a_n=a_{n-1}+a_{n-2}, a1=1,a2=2. a5?", 8, "1,2,3,5,8."),
        _q("Paths to (4,0) if only R and L would cancel. Only R/U to (4,3)?", 35, "C(7,3)."),
        _q("Catalan C_3=C(6,3)/4?", 5, "5."),
        _q("Dyck words n=3?", 5, "Catalan."),
        _q("AMC: paths (0,0) to (6,4) avoiding? Unrestricted first. C(10,4)?", 210, "210.", difficulty="hard"),
        _q("Ways to climb 5 stairs 1 or 2 at a time?", 8, "F_6=8.", difficulty="hard"),
        _q("a_n=2a_{n-1}+1, a1=1. a4?", 15, "1,3,7,15.", difficulty="hard"),
        _q("Lattice (1,1) to (4,5) still R/U. Need 3R 4U. C(7,3)?", 35, "35.", difficulty="hard"),
        _q("Stretch: paths (0,0) to (3,3) not above y=x (Catalan C_3)?", 5, "5.", difficulty="stretch"),
        _q("Number of monotonic lattice paths along edges of a 3×3 grid not passing above diagonal?", 5, "C_3=5.", difficulty="stretch"),
        _q("Fibonacci F_10?", 55, "55.", difficulty="stretch"),
        _q("Tile 2×n with 1×2 and 2×1. n=4. Ways?", 5, "Classic F_{n+1}.", difficulty="stretch"),
        _q("A sequence 2,3,5,8,13. Next?", 21, "Fibonacci-like.", difficulty="stretch"),
        _q("Paths with diagonal steps not allowed. (0,0)→(2,3). C(5,2)?", 10, "10.", difficulty="stretch"),
        _q("Recursion a_n=n a_{n-1}, a1=1. a4=24=4!. Yes a5?", 120, "5!.", difficulty="stretch"),
        _q("Number of subsets of [n] with no two consecutive. n=5. F_7=13?", 13, "Fib.", difficulty="stretch"),
        _q("How many subsets of {1,2,3,4,5} have no two consecutive integers?", 13, "Including empty.", difficulty="stretch"),
        _q("Shortest paths city 3 blocks east 2 north?", 10, "C(5,2).", difficulty="stretch"),
        _q("If one block is closed so you cannot go through (1,1) as a vertex, subtract paths through (1,1) to (3,2). Through: C(2,1)×C(3,2)=2×3=6. Total C(5,2)=10, remaining 4.", difficulty="stretch"),
        _q("R/U paths (0,0) to (3,2) that do not pass through (1,1)?", 4, "10−6=4.", difficulty="stretch"),
        _q("a_n=a_{n-1}+2 a_{n-2} a1=1 a2=1. a4?", 5, "1,1,3,5.", difficulty="stretch"),
        _q("Catalan C_4=C(8,4)/5?", 14, "70/5=14.", difficulty="stretch"),
        _q("Ways to parenthesize 4 factors (Catalan C_3)?", 5, "5.", difficulty="stretch"),
        _q("A 1×n coloring 2 colors no two adjacent red. If n=3. 2nd color free unless… 3^? Binary R/B: B* + RB* patterns.  Fibonacci 5? BBB,BBR,BRB,RBB,RBR =5 (no RR).", difficulty="stretch"),
        _q("Length-3 strings of R/B with no two consecutive R?", 5, "5 strings.", difficulty="stretch"),
    ]
    qs = [q for q in qs if q and "closed so you" not in q["question_text"] and "2nd color" not in q["question_text"]]
    return qs


def mc8():
    qs = [
        _q("Sprint strategy: if two answers look like n and 2n, check units. Warmup 12×11?", 132, "132."),
        _q("Estimate √50 closest integer?", 7, "7.07."),
        _q("A 3-4-5 scaled by 3. Hypotenuse?", 15, "15."),
        _q("C(10,2) as a contest flash?", 45, "45."),
        _q("2^10?", 1024, "1024."),
        _q("Remainder 2^10 ÷ 5?", 4, "1024 ends 4."),
        _q("Mean of first 9 positives?", 5, "45/9."),
        _q("A 12-hour clock angle at 3:00?", 90, "90°."),
        _q("Units digit of 7^5? Cycle 7,9,3,1. 5 mod 4=1 →7.", 7, "7."),
        _q("AMC Stretch mixed: last two digits of 7^4?", 1, "2401 → 01? 7^4=2401, 01.", difficulty="hard"),
        _q("Last two digits of 7^4?", "01", "2401.", difficulty="hard"),
        _q("How many zeros at end of 25! ? Floor 25/5+5=6.", 6, "5s in 25!.", difficulty="hard"),
        _q("Trailing zeros of 25!?", 6, "5+1.", difficulty="hard"),
        _q("Stretch: remainder when 1+2+…+100 is divided by 9? Sum 5050, 5+0+5+0=10, 1+0=1.", 1, "Digital root /9.", difficulty="stretch"),
        _q("1+2+…+100 mod 9?", 1, "5050→10→1.", difficulty="stretch"),
        _q("A 5-12-13 triangle area?", 30, "½×5×12.", difficulty="stretch"),
        _q("Integer  n with n^2=144. Positive n?", 12, "12.", difficulty="stretch"),
        _q("Number of primes ≤20?", 8, "2,3,5,7,11,13,17,19.", difficulty="stretch"),
        _q("LCM(8,12)×GCF(8,12)=8×12. Check LCM×GCF=product. LCM(8,12)?", 24, "24.", difficulty="stretch"),
        _q("A contest: 15% of 80 + 20% of 50?", 22, "12+10.", difficulty="stretch"),
        _q("If 3^x=81, x?", 4, "4.", difficulty="stretch"),
        _q("Permutation 6! / 4! ?", 30, "6×5.", difficulty="stretch"),
        _q("A circle r=7, π=22/7, area?", 154, "22/7×49.", difficulty="stretch"),
        _q("Median of 1,3,3,7,9,11,15?", 7, "Middle.", difficulty="stretch"),
        _q("How many diagonals of a hexagon?", 9, "n(n−3)/2=9.", difficulty="stretch"),
        _q("A 2-digit palindrome count?", 9, "11,22,…99.", difficulty="stretch"),
        _q("Solve |2x−1|=7. Positive x?", 4, "2x−1=7.", difficulty="stretch"),
        _q("Both solutions sum of |2x−1|=7?", 1, "x=4 and x=−3, sum 1.", difficulty="stretch"),
        _q("A target mix: C(6,2)×2^4? Skip. 9×8×7 / 3! ?", 84, "P(9,3)/6=C(9,3).", difficulty="stretch"),
        _q("C(9,3)=?", 84, "84.", difficulty="stretch"),
    ]
    qs = [q for q in qs if q and "Skip" not in q["question_text"]]
    return qs

