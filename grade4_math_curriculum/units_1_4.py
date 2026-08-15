"""Fourth Grade Math units 1–4: millions, multi-digit × and ÷, like-denominator fractions."""

from .common import (
    concept_block,
    solved,
    practice_slots,
    unit_shell,
    kid_tip,
    watch_out,
    try_this,
    step_reveal,
    matching,
    phet_box,
    mq,
    renumber,
)


def _fill(qs, need, factory):
    while len(qs) < need:
        qs.append(factory(len(qs) + 1))
    return renumber(qs[:need])


# ===========================================================================
# UNIT 1: Place value to 1,000,000
# ===========================================================================

def _u1_questions():
    qs = []
    idx = 1

    for text, ans, expl in [
        ("In 4,582,136 what digit is in the millions place?", 4, "4,582,136 has 4 millions."),
        ("In 4,582,136 what digit is in the hundred thousands place?", 5, "The 5 is hundred thousands: 500,000."),
        ("In 4,582,136 what digit is in the ten thousands place?", 8, "The 8 is ten thousands: 80,000."),
        ("What is the value of the 2 in 4,582,136?", 2000, "The 2 is in the thousands place. 2,000."),
        ("How many thousands are in 1 million?", 1000, "1,000 thousands make 1,000,000."),
    ]:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    for text, ans, expl, dist in [
        ("Write 3,000,000 + 40,000 + 200 + 5 as a number.", "3,040,205",
         "3 millions, 4 ten thousands, 2 hundreds, 5 ones.", ["3,400,205", "3,042,005", "340,205"]),
        ("How do you write five hundred eight thousand sixty?", "508,060",
         "508 thousands and 60.", ["580,060", "50,860", "5,080,060"]),
        ("1,000 times as much as 45 is…", 45000, "Each place is 10 times the one on its right. Three places left is ×1,000.", ["450", "4,500", "450,000"]),
        ("1/10 of 7,000 is…", 700, "Move one place to the right. 7,000 ÷ 10 = 700.", ["70", "7,0000", "70,000"]),
        ("Which is greater: 809,412 or 890,124?", "890,124",
         "Hundred thousands: 8 vs 8. Ten thousands: 0 vs 9. 890,124 is greater.", ["809,412", "same", "80,941"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for n, nearest in [(34_499, 34_000), (34_500, 35_000), (128_360, 128_000), (999_400, 999_000), (2_501, 3_000)]:
        qs.append(mq(f"Round {n:,} to the nearest thousand.", nearest, f"Look at the hundreds digit. {n:,} rounds to {nearest:,}.", idx))
        idx += 1
    for n, nearest in [(34_499, 30_000), (36_000, 40_000), (125_000, 130_000), (84_999, 80_000), (250_000, 250_000)]:
        qs.append(mq(f"Round {n:,} to the nearest ten thousand.", nearest, f"Look at the thousands digit. {n:,} rounds to {nearest:,}.", idx))
        idx += 1
    for n, nearest in [(349_999, 300_000), (350_000, 400_000), (1_249_000, 1_200_000), (780_000, 800_000)]:
        qs.append(mq(f"Round {n:,} to the nearest hundred thousand.", nearest, f"Look at the ten-thousands digit. {n:,} rounds to {nearest:,}.", idx))
        idx += 1

    for a, b in [(458_216, 367_089), (900_000, 125_450), (1_250_000, 750_000)]:
        qs.append(mq(f"{a:,} + {b:,} = ?", a + b, f"Add by places. Sum is {a + b:,}.", idx))
        idx += 1
    for a, b in [(800_000, 256_173), (1_000_000, 408_250), (640_500, 125_075)]:
        qs.append(mq(f"{a:,} − {b:,} = ?", a - b, f"Subtract by places. Difference is {a - b:,}.", idx))
        idx += 1

    for n in [45, 70, 208, 1_500, 3_000]:
        qs.append(mq(f"What is 10 times {n:,}?", n * 10, f"Move one place left. {n:,} × 10 = {n * 10:,}.", idx))
        idx += 1
        qs.append(mq(f"What is 100 times {n:,}?", n * 100, f"{n:,} × 100 = {n * 100:,}.", idx))
        idx += 1

    return _fill(qs, 80, lambda i: mq(
        f"What is 10 times {1000 + i * 10}?",
        (1000 + i * 10) * 10,
        f"Move one place to the left. {(1000 + i * 10) * 10}.",
        i,
    ))


def build_unit1():
    title = "Fourth Grade Math Unit 1: Place Value to One Million"
    description = (
        "Read and write numbers to 1,000,000, use ×10 and ÷10 place relationships, round, compare, and add or subtract multi-digit numbers."
    )

    c1 = concept_block(
        "1. Places through millions",
        [
            "Fourth grade goes all the way to one million. 1,000,000 is a 1 followed by six zeros.",
            "Places from the right: ones, tens, hundreds, thousands, ten thousands, hundred thousands, millions.",
            "In 4,582,136 the 4 is millions (4,000,000). The 5 is hundred thousands (500,000).",
            "Commas group digits in threes so you can read them: 4 million, 582 thousand, 136.",
            "Each place is 10 times the place on its right. 10 hundred thousands make 1 million.",
            "A place-value chart keeps every digit in its home.",
        ],
        solved(1, "What is the value of the 8 in 4,582,136?",
               ["The 8 sits in the ten-thousands place.",
                "8 ten thousands = 80,000."],
               "80,000")
        + matching(
            [("millions", "1,000,000s"), ("hundred thousands", "100,000s"),
             ("ten thousands", "10,000s"), ("thousands", "1,000s")],
            vid="g4u1-c1-match",
        ),
        kid_tip("Read the commas", "Say the group, then the word: 4 million… 582 thousand… 136.")
        + phet_box("compare"),
        1,
    )

    c2 = concept_block(
        "2. Times ten, times one hundred, one tenth",
        [
            "Moving a digit one place to the left multiplies its value by 10.",
            "45 ones is 45. 45 tens is 450. That is 10 times as much.",
            "1,000 times as much as 45 is 45,000. You moved three places.",
            "Moving one place to the right is 1/10 as much. 1/10 of 7,000 is 700.",
            "This is why 6 in the thousands place is 10 times 6 in the hundreds place.",
            "Write a small arrow: ×10 left, ÷10 right.",
        ],
        solved(1, "The 3 in 3,000 is how many times the 3 in 300?",
               ["Thousands is one place left of hundreds.",
                "One place left is 10 times as much."],
               "10 times")
        + solved(2, "What is 100 times 208?",
                 ["208 × 100 = 20,800.",
                  "Stick two zeros, or move two places left."],
                 "20,800")
        + step_reveal(
            ["Find the digit.",
             "Count how many places it moved.",
             "Each place is ×10 (left) or ×1/10 (right).",
             "3 places left is ×1,000."],
            vid="g4u1-c2-steps",
        ),
        watch_out("Adding zeros without thinking about the digit",
                  "45 × 10 is 450, not 45,0. The 5 moves into tens."),
        6,
    )

    c3 = concept_block(
        "3. Read, write, and expand to a million",
        [
            "Standard form: 3,040,205.",
            "Word form: three million forty thousand two hundred five.",
            "Expanded form: 3,000,000 + 40,000 + 200 + 5.",
            "Zeros hold empty places. Do not drop them in standard form.",
            "508,060 is five hundred eight thousand sixty — not five hundred eighty thousand.",
            "Practice switching among the three forms until they feel like the same number.",
        ],
        solved(1, "Write 3,000,000 + 40,000 + 200 + 5 in standard form.",
               ["3 millions, 4 ten thousands, 2 hundreds, 5 ones.",
                "3,040,205."],
               "3,040,205")
        + matching(
            [("5,000,000 + 8,000 + 60", "5,008,060"), ("200,000 + 9", "200,009"),
             ("1,000,000 + 1,000", "1,001,000"), ("70,000 + 70", "70,070")],
            vid="g4u1-c3-match",
        ),
        try_this("Say it in chunks", "Millions, then thousands, then the last three. Pause at each comma."),
        11,
    )

    c4 = concept_block(
        "4. Compare and round big numbers",
        [
            "Compare from the left. The first place that differs decides.",
            "809,412 vs 890,124: hundred thousands match (8). Ten thousands 0 vs 9. 890,124 is greater.",
            "Round to nearest thousand: look at hundreds. 5 or more rounds up.",
            "Nearest ten thousand: look at thousands. Nearest hundred thousand: look at ten thousands.",
            "34,500 to the nearest thousand is 35,000. Halfway rounds up.",
            "Rounding helps you estimate a sum before you compute the exact answer.",
        ],
        solved(1, "Round 128,360 to the nearest thousand.",
               ["Hundreds digit is 3, less than 5.",
                "Keep 128 thousands. 128,000."],
               "128,000")
        + solved(2, "Round 350,000 to the nearest hundred thousand.",
                 ["Ten-thousands digit is 5, so round up.",
                  "300,000 becomes 400,000."],
                 "400,000")
        + kid_tip("Name the neighbor", "Nearest thousand? Neighbor is the hundreds digit. That neighbor votes up or stay."),
        16,
    )

    c5 = concept_block(
        "5. Add multi-digit numbers",
        [
            "Line up places. Add ones through millions. Regroup whenever a place hits 10 or more.",
            "Estimate first: 458,216 + 367,089 is near 460,000 + 370,000 = 830,000.",
            "Keep columns straight. A drifted digit becomes a wrong place in a million-size number.",
            "You can add in expanded form: add millions, then thousands, then the rest.",
            "Check by adding the other way, or by a reverse subtract.",
            "Sums can pass a million: 750,000 + 500,000 = 1,250,000.",
        ],
        solved(1, "458,216 + 367,089 = ?",
               ["Add place by place, regrouping as needed.",
                "Ones through hundred thousands.",
                "Sum 825,305."],
               "825,305")
        + phet_box("arith"),
        try_this("Estimate, then compute", "If the exact sum is far from the estimate, look at a regroup."),
        21,
    )

    c6 = concept_block(
        "6. Subtract multi-digit numbers",
        [
            "Subtract place by place. Borrow when a digit is too small.",
            "Zeros in the middle still need a chain of borrows, just like in third grade — more digits now.",
            "1,000,000 − 408,250 needs careful unbundling across zeros.",
            "Check with addition: difference + subtracted number = start.",
            "Stories: population, money, and distance use these large subtracts.",
            "Keep the greater number on top when finding how many more.",
        ],
        solved(1, "800,000 − 256,173 = ?",
               ["Borrow across the zeros.",
                "800,000 − 256,173 = 543,827."],
               "543,827")
        + watch_out("Skipping a zero when you borrow",
                    "If tens are 0, hundreds must feed tens, then tens feed ones. Do not jump a place."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Name places through one million",
            "Use ×10 and 1/10 place relationships",
            "Read, write, and expand large numbers",
            "Compare and round",
            "Add multi-digit numbers",
            "Subtract multi-digit numbers",
        ],
        body,
        practice_slots(31, 50),
    )
    return title, description, content, _u1_questions()


# ===========================================================================
# UNIT 2: Multi-digit multiplication
# ===========================================================================

def _u2_questions():
    qs = []
    idx = 1

    for a, b in [(23, 4), (45, 6), (37, 8), (56, 7), (82, 5), (19, 9), (64, 3), (70, 8)]:
        qs.append(mq(f"{a} × {b} = ?", a * b, f"{a} × {b} = {a * b}.", idx))
        idx += 1
    for a, b in [(128, 4), (205, 6), (317, 3), (450, 7), (1_024, 5), (2_106, 4), (3_008, 3), (1_250, 8)]:
        qs.append(mq(f"{a:,} × {b} = ?", a * b, f"Multiply 1-digit across each place. {a:,} × {b} = {a * b:,}.", idx))
        idx += 1
    for a, b in [(12, 14), (23, 15), (26, 14), (34, 12), (41, 21), (18, 16), (25, 25), (32, 14)]:
        qs.append(mq(f"{a} × {b} = ?", a * b, f"Use an area model or partial products. {a} × {b} = {a * b}.", idx))
        idx += 1

    stories = [
        ("A box holds 24 pencils. 6 boxes. How many pencils?", 144, "24 × 6 = 144."),
        ("A theater has 18 rows of 16 seats. How many seats?", 288, "18 × 16 = 288."),
        ("A pack has 125 stickers. 4 packs. How many stickers?", 500, "125 × 4 = 500."),
        ("Miles per hour 55. Drive 3 hours at that speed. How many miles?", 165, "55 × 3 = 165."),
        ("A crate has 36 bottles. 12 crates. How many bottles?", 432, "36 × 12 = 432."),
        ("Each book has 248 pages. 5 books. How many pages?", 1240, "248 × 5 = 1,240."),
    ]
    for text, ans, expl in stories:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    parts = [
        ("26 × 14. Partial products: 26 × 10 and 26 × 4. 260 + 104 = ?", 364, "Add the parts."),
        ("23 × 15 = 23 × 10 + 23 × 5. 230 + 115 = ?", 345, "Break 15 into 10 and 5."),
        ("45 × 6. 40 × 6 + 5 × 6 = 240 + 30 = ?", 270, "Break 45 into 40 and 5."),
        ("108 × 7. 100 × 7 + 8 × 7 = 700 + 56 = ?", 756, "Break apart by place."),
        ("30 × 14 = ?", 420, "3 × 14 = 42, then ×10 → 420."),
        ("25 × 20 = ?", 500, "25 × 2 × 10 = 500."),
    ]
    for text, ans, expl in parts:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    return _fill(qs, 80, lambda i: mq(
        f"{12 + (i % 20)} × {3 + (i % 8)} = ?",
        (12 + (i % 20)) * (3 + (i % 8)),
        f"Product is {(12 + (i % 20)) * (3 + (i % 8))}.",
        i,
    ))


def build_unit2():
    title = "Fourth Grade Math Unit 2: Multi-Digit Multiplication"
    description = (
        "Multiply up to four-digit by one-digit and two-digit by two-digit numbers using place value, area models, and partial products."
    )

    c1 = concept_block(
        "1. Multiply by a one-digit number",
        [
            "Start with two-digit × one-digit: 23 × 4.",
            "Break apart: 20 × 4 = 80, 3 × 4 = 12, total 92.",
            "Or use the standard algorithm: multiply ones, regroup, then tens.",
            "Estimate: 23 × 4 is near 20 × 4 = 80. Exact 92 is close. Good.",
            "Zeros help: 70 × 8 = 560 because 7 × 8 = 56, then one extra zero.",
            "Keep place value. 3 × 4 is 12 ones, not 12 tens.",
        ],
        solved(1, "45 × 6 = ?",
               ["40 × 6 = 240.",
                "5 × 6 = 30.",
                "240 + 30 = 270."],
               "270")
        + matching(
            [("23 × 4", "92"), ("56 × 7", "392"), ("82 × 5", "410"), ("70 × 8", "560")],
            vid="g4u2-c1-match",
        ),
        kid_tip("Estimate first", "Round the big number, multiply, then compute exact. The two answers should be neighbors."),
        1,
    )

    c2 = concept_block(
        "2. Three- and four-digit × one-digit",
        [
            "Same move, more places: 1,024 × 5.",
            "1,000 × 5 = 5,000. 20 × 5 = 100. 4 × 5 = 20. Sum 5,120.",
            "In the algorithm, regroup from ones to tens, tens to hundreds, and so on.",
            "317 × 3: 7×3=21 write 1 carry 2; 1×3+2=5; 3×3=9. Product 951.",
            "Watch zeros in the middle: 2,106 × 4. The 0 still needs a 0 in that place (plus any carry).",
            "Stories: packs, pages, and crates use these products.",
        ],
        solved(1, "128 × 4 = ?",
               ["100 × 4 = 400.",
                "20 × 4 = 80.",
                "8 × 4 = 32. Total 512."],
               "512")
        + solved(2, "2,106 × 4 = ?",
                 ["2,000 × 4 = 8,000.",
                  "100 × 4 = 400.",
                  "6 × 4 = 24. Total 8,424."],
                 "8,424")
        + phet_box("area_mult"),
        watch_out("Skipping a zero place",
                  "In 2,106 × 4, the hundreds digit is 1, not empty. Write every place."),
        6,
    )

    c3 = concept_block(
        "3. Area model for two-digit × two-digit",
        [
            "26 × 14 can be a rectangle 26 by 14.",
            "Split 26 into 20 and 6. Split 14 into 10 and 4. Four smaller rectangles.",
            "20×10=200, 20×4=80, 6×10=60, 6×4=24. Add: 364.",
            "The four partial products always add to the full product.",
            "This model is the same idea as (20+6)×(10+4).",
            "Draw the rectangle. Label the splits. Fill each area. Add.",
        ],
        solved(1, "23 × 15 with an area model.",
               ["20×10=200, 20×5=100, 3×10=30, 3×5=15.",
                "200+100+30+15=345."],
               "345")
        + step_reveal(
            ["Split each factor into tens and ones.",
             "Multiply the four pairs.",
             "Write each partial product in its rectangle.",
             "Add the four numbers."],
            vid="g4u2-c3-steps",
        ),
        try_this("Color the four parts", "Four colors, four products. Then one sum.")
        + phet_box("area_mult"),
        11,
    )

    c4 = concept_block(
        "4. Partial products and the algorithm",
        [
            "Partial products are the area-model numbers written in a list.",
            "26 × 14: 26×10=260 and 26×4=104. 260+104=364.",
            "The standard algorithm stacks those same pieces, with regrouping in columns.",
            "When you multiply by the tens digit, that partial product is really tens: 26×1 ten = 26 tens = 260.",
            "A placeholder zero in the ones place of that row reminds you.",
            "Both methods must match. If they do not, a place got lost.",
        ],
        solved(1, "34 × 12 = ?",
               ["34 × 10 = 340.",
                "34 × 2 = 68.",
                "340 + 68 = 408."],
               "408")
        + matching(
            [("12 × 14", "168"), ("25 × 25", "625"), ("32 × 14", "448"), ("41 × 21", "861")],
            vid="g4u2-c4-match",
        ),
        kid_tip("The blank zero", "When multiplying by tens, the ones place of that row is 0. That 0 is a place holder, not a decoration."),
        16,
    )

    c5 = concept_block(
        "5. Multiply by 10, 100, and 1,000",
        [
            "×10 moves digits one place left. ×100 two places. ×1,000 three places.",
            "25 × 20 = 25 × 2 × 10 = 50 × 10 = 500.",
            "30 × 14 = 3 × 14 × 10 = 42 × 10 = 420.",
            "This shortcut makes two-digit work faster when a factor ends in 0.",
            "40 × 15: 4 × 15 = 60, then ×10 → 600.",
            "Do not only stick zeros if the other factor also needs multiplying.",
        ],
        solved(1, "25 × 20 = ?",
               ["25 × 2 = 50.",
                "Times 10 because of the extra zero: 500."],
               "500")
        + watch_out("Sticking two zeros for ×20",
                    "20 is 2 × 10, not 100. 25 × 20 is 500, not 2,500."),
        21,
    )

    c6 = concept_block(
        "6. Multiplication stories",
        [
            "Equal groups that are large still use ×.",
            "18 rows of 16 seats: 18 × 16.",
            "5 books of 248 pages: 248 × 5.",
            "Write a sentence, estimate, then compute.",
            "Label the product: 288 seats, not a bare 288.",
            "If extras appear after the packs, that is a two-step story (× then +). We keep one-step here, then mix in later units.",
        ],
        solved(1, "A crate has 36 bottles. 12 crates. How many bottles?",
               ["36 × 12.",
                "36 × 10 = 360. 36 × 2 = 72.",
                "432 bottles."],
               "432")
        + try_this("Estimate with round numbers", "36 × 12 is near 40 × 10 = 400. Exact 432 sits nearby. Reasonable."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Multiply two-digit by one-digit",
            "Multiply three- and four-digit by one-digit",
            "Use an area model for two-digit × two-digit",
            "Write partial products",
            "Multiply by 10, 100, and 1,000",
            "Solve multiplication stories",
        ],
        body,
        practice_slots(31, 50),
    )
    return title, description, content, _u2_questions()


# ===========================================================================
# UNIT 3: Multi-digit division
# ===========================================================================

def _u3_questions():
    qs = []
    idx = 1

    for a, b in [(84, 4), (96, 6), (72, 8), (90, 5), (63, 7), (48, 3), (56, 4), (81, 9)]:
        qs.append(mq(f"{a} ÷ {b} = ?", a // b, f"{b} × {a // b} = {a}, so {a} ÷ {b} = {a // b}.", idx))
        idx += 1
    for a, b in [(365, 5), (248, 4), (936, 6), (507, 3), (840, 7), (1_248, 6), (2_025, 5), (1_008, 8)]:
        qs.append(mq(f"{a:,} ÷ {b} = ?", a // b, f"{a:,} ÷ {b} = {a // b:,}.", idx))
        idx += 1

    remainders = [
        ("17 ÷ 5 = 3 remainder ?", 2, "5×3=15. 17−15=2 left."),
        ("23 ÷ 4 = 5 remainder ?", 3, "4×5=20. 3 left."),
        ("50 ÷ 6 = 8 remainder ?", 2, "6×8=48. 2 left."),
        ("100 ÷ 9 = 11 remainder ?", 1, "9×11=99. 1 left."),
        ("29 ÷ 5. The quotient is 5 remainder 4. How many leftover?", 4, "Remainder 4."),
        ("A remainder must be smaller than the…", "divisor",
         "If remainder ≥ divisor, you can make another group.", ["quotient", "dividend", "million"]),
    ]
    for item in remainders:
        if len(item) == 4:
            text, ans, expl, dist = item
            qs.append(mq(text, ans, expl, idx, distractors=dist))
        else:
            text, ans, expl = item
            qs.append(mq(text, ans, expl, idx))
        idx += 1

    stories = [
        ("84 muffins in 4 boxes, equal. How many per box?", 21, "84 ÷ 4 = 21."),
        ("365 days shared into 5 equal groups of days. How many in each group?", 73, "365 ÷ 5 = 73."),
        ("1,248 cards in 6 equal packs. How many per pack?", 208, "1,248 ÷ 6 = 208."),
        ("A farmer packs 50 eggs into cartons of 6. How many full cartons?", 8, "50 ÷ 6 = 8 remainder 2. 8 full cartons."),
        ("Same 50 eggs. How many eggs left over?", 2, "Remainder 2."),
        ("936 stickers for 6 kids, equal. How many each?", 156, "936 ÷ 6 = 156."),
        ("You have 29 seats in rows of 5. How many full rows?", 5, "29 ÷ 5 = 5 remainder 4."),
        ("248 pages read in 4 days, same each day. Pages per day?", 62, "248 ÷ 4 = 62."),
    ]
    for text, ans, expl in stories:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    checks = [
        ("Check 84 ÷ 4 = 21. What is 21 × 4?", 84, "Multiply to check divide."),
        ("Check 365 ÷ 5 = 73. 73 × 5 = ?", 365, "73 × 5 = 365."),
        ("17 ÷ 5 = 3 R2. Check: 5×3 + 2 = ?", 17, "Quotient × divisor + remainder = dividend."),
        ("23 ÷ 4 = 5 R3. Check: 4×5 + 3 = ?", 23, "20 + 3 = 23."),
        ("If 6 × 208 = 1,248, then 1,248 ÷ 6 = ?", 208, "Division undoes multiplication."),
        ("Missing factor: 7 × ___ = 840. The missing number is…", 120, "840 ÷ 7 = 120."),
    ]
    for text, ans, expl in checks:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    return _fill(qs, 80, lambda i: mq(
        f"{(12 + i) * (3 + (i % 6))} ÷ {3 + (i % 6)} = ?",
        12 + i,
        f"Because {3 + (i % 6)} × {12 + i} = {(12 + i) * (3 + (i % 6))}.",
        i,
    ))


def build_unit3():
    title = "Fourth Grade Math Unit 3: Multi-Digit Division"
    description = (
        "Divide up to four-digit numbers by one-digit numbers, interpret remainders, and check with multiplication."
    )

    c1 = concept_block(
        "1. Divide with a × fact you know",
        [
            "84 ÷ 4 asks: 4 times what is 84?",
            "Think 4 × 20 = 80, then 4 × 1 = 4, so 21. 84 ÷ 4 = 21.",
            "Place value: 8 tens ÷ 4 = 2 tens, 4 ones ÷ 4 = 1 one.",
            "This is the start of long division: divide, multiply, subtract, bring down.",
            "Estimate first. 84 ÷ 4 is near 80 ÷ 4 = 20.",
            "Check always: quotient × divisor = dividend (when no remainder).",
        ],
        solved(1, "96 ÷ 6 = ?",
               ["6 × 10 = 60. Left 36.",
                "6 × 6 = 36.",
                "10 + 6 = 16."],
               "16")
        + matching(
            [("84 ÷ 4", "21"), ("72 ÷ 8", "9"), ("90 ÷ 5", "18"), ("63 ÷ 7", "9")],
            vid="g4u3-c1-match",
        ),
        kid_tip("Think times", "Every divide sentence is a multiply sentence with a hole.")
        + phet_box("arith"),
        1,
    )

    c2 = concept_block(
        "2. Long division, one digit at a time",
        [
            "For 365 ÷ 5, look at the first digit or first two digits.",
            "5 into 3? Too small. 5 into 36 is 7. 5×7=35. Subtract 1. Bring down 5 → 15. 5×3=15.",
            "Quotient 73.",
            "Write the quotient digits in the matching places. 7 is tens, 3 is ones.",
            "If a place is 0 in the quotient, write the 0. Do not skip it.",
            "1,248 ÷ 6: 6 into 12 is 2 (hundreds). Continue through tens and ones. Quotient 208 — that 0 matters.",
        ],
        solved(1, "365 ÷ 5 = ?",
               ["5 into 36 is 7, remainder 1.",
                "Bring down 5 → 15. 5 into 15 is 3.",
                "73."],
               "73")
        + step_reveal(
            ["Divide the leftmost part that is large enough.",
             "Multiply and subtract.",
             "Bring down the next digit.",
             "Repeat until no digits remain. Multiply to check."],
            vid="g4u3-c2-steps",
        ),
        watch_out("Dropping a zero in the quotient",
                  "1,248 ÷ 6 is 208, not 28. The tens place is 0 because 6 does not fit into the leftover 4 tens until you bring down."),
        6,
    )

    c3 = concept_block(
        "3. Four-digit ÷ one-digit",
        [
            "Same steps, one more digit: 2,025 ÷ 5 = 405.",
            "Keep a place-value table: thousands, hundreds, tens, ones.",
            "If the divisor does not fit, write 0 in that quotient place and bring down.",
            "Partial quotients is another path: subtract easy chunks (5×400, 5×5) until nothing remains.",
            "Both paths must match.",
            "Estimate with compatible numbers: 2,025 ÷ 5 is near 2,000 ÷ 5 = 400.",
        ],
        solved(1, "1,248 ÷ 6 = ?",
               ["6 × 200 = 1,200.",
                "Left 48. 6 × 8 = 48.",
                "200 + 8 = 208."],
               "208")
        + solved(2, "2,025 ÷ 5 = ?",
                 ["5 × 400 = 2,000.",
                  "Left 25. 5 × 5 = 25.",
                  "405."],
                 "405")
        + try_this("Partial quotients", "Subtract big friendly multiples first. Keep a running leftover. Add the chunks you used."),
        11,
    )

    c4 = concept_block(
        "4. Remainders",
        [
            "Sometimes the leftover is not 0. That leftover is the remainder.",
            "17 ÷ 5 = 3 remainder 2, because 5×3=15 and 2 are left.",
            "Write 3 R2. Check: 5×3 + 2 = 17.",
            "The remainder must be smaller than the divisor. If it is not, you can make another group.",
            "Stories care what the remainder means: leftover eggs, leftover seats, leftover days.",
            "Sometimes the question wants full groups only. Sometimes it wants leftovers only. Read it.",
        ],
        solved(1, "50 eggs packed 6 per carton. How many full cartons? How many left?",
               ["50 ÷ 6 = 8 remainder 2.",
                "8 full cartons. 2 eggs left."],
               "8 cartons, 2 left")
        + matching(
            [("17 ÷ 5", "3 R2"), ("23 ÷ 4", "5 R3"), ("100 ÷ 9", "11 R1"), ("check 5×3+2", "17")],
            vid="g4u3-c4-match",
        ),
        kid_tip("Remainder < divisor", "If you see remainder 6 when dividing by 5, you missed a group."),
        16,
    )

    c5 = concept_block(
        "5. What does the remainder mean?",
        [
            "A story decides how to use the remainder.",
            "Vans hold 5 kids. 23 kids. How many vans? You need 5 vans, because 4 leftover kids still need a van. Here you round the quotient up.",
            "How many leftover seats in rows of 5 from 29 seats? Remainder 4. Do not round up.",
            "How many full rows? Use the quotient only.",
            "Underline the question: full groups, leftovers, or enough containers for everyone?",
            "The math 29 ÷ 5 = 5 R4 stays the same. The answer you report changes.",
        ],
        solved(1, "29 seats in rows of 5. How many full rows?",
               ["29 ÷ 5 = 5 R4.",
                "Full rows: 5."],
               "5")
        + solved(2, "29 kids, 5 per row. How many kids in the leftover row?",
                 ["Remainder 4."],
                 "4")
        + watch_out("Always ignoring the leftover kids",
                    "If everyone needs a seat, leftovers mean one more van or row. If the question asks leftover only, report the remainder."),
        21,
    )

    c6 = concept_block(
        "6. Check division",
        [
            "No remainder: quotient × divisor = dividend.",
            "With remainder: quotient × divisor + remainder = dividend.",
            "If the check fails, a digit in the quotient is wrong, or the remainder is too big.",
            "Missing factor problems are divide problems: 7 × ___ = 840 → 840 ÷ 7.",
            "Fact families still work with larger numbers.",
            "Checking takes a minute and saves a wrong answer.",
        ],
        solved(1, "Check 23 ÷ 4 = 5 R3.",
               ["4 × 5 = 20.",
                "20 + 3 = 23. The check matches."],
               "yes")
        + matching(
            [("84 ÷ 4 check", "21 × 4 = 84"), ("17 ÷ 5 check", "5×3+2=17"),
             ("7 × ? = 840", "120"), ("zero remainder", "product equals dividend")],
            vid="g4u3-c6-match",
        ),
        try_this("Write the check under the problem", "Every divide gets a multiply sentence underneath before you move on."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Use a multiply fact to divide",
            "Divide one digit at a time",
            "Divide four-digit numbers",
            "Find remainders",
            "Interpret remainders in stories",
            "Check with multiplication",
        ],
        body,
        practice_slots(31, 50),
    )
    return title, description, content, _u3_questions()


# ===========================================================================
# UNIT 4: Add and subtract fractions (like denominators)
# ===========================================================================

def _u4_questions():
    qs = []
    idx = 1

    adds = [
        ("2/5 + 1/5 = ?", "3/5", "Same size pieces. Add the counts: 2+1=3 fifths."),
        ("3/8 + 2/8 = ?", "5/8", "3+2=5 eighths."),
        ("1/6 + 4/6 = ?", "5/6", "1+4=5 sixths."),
        ("4/10 + 3/10 = ?", "7/10", "4+3=7 tenths."),
        ("5/12 + 4/12 = ?", "9/12", "5+4=9 twelfths."),
        ("1/4 + 1/4 = ?", "2/4", "Two fourths. That equals 1/2."),
        ("3/4 + 3/4 = ?", "6/4", "6/4 is 1 2/4 or 1 1/2."),
        ("2/3 + 2/3 = ?", "4/3", "4/3 is 1 1/3."),
        ("0/5 + 3/5 = ?", "3/5", "Zero fifths plus three fifths."),
        ("7/8 + 1/8 = ?", "8/8", "8/8 = 1 whole."),
    ]
    for text, ans, expl in adds:
        qs.append(mq(text, ans, expl, idx, distractors=None if str(ans).isdigit() else ["1/5", "3/10", "1"]))
        idx += 1

    # Fix distractors for fraction adds - mq with string uses weak distractors. Provide real ones.
    # Too late for those already appended with None - make_question will use Not sure. Let me redo more carefully
    # Actually I passed distractors=None which triggers near_int only for digit strings. "3/5" goes to Not sure. That's OK-ish but let's add more with explicit dist.

    subs = [
        ("5/8 − 2/8 = ?", "3/8", ["1/8", "7/8", "3/16"], "Subtract the counts. Pieces stay eighths."),
        ("7/10 − 3/10 = ?", "4/10", ["10/10", "4/7", "1/10"], "7−3=4 tenths."),
        ("6/6 − 1/6 = ?", "5/6", ["5/5", "1/6", "7/6"], "A whole minus one sixth."),
        ("9/12 − 4/12 = ?", "5/12", ["13/12", "5/8", "4/12"], "9−4=5 twelfths."),
        ("3/4 − 1/4 = ?", "2/4", ["2/8", "4/4", "1/2"], "2/4 equals 1/2."),
        ("5/5 − 5/5 = ?", "0/5", ["1", "5/0", "1/5"], "All pieces gone. 0."),
        ("4/3 − 1/3 = ?", "3/3", ["3/0", "5/3", "1"], "3/3 = 1."),
        ("11/8 − 3/8 = ?", "8/8", ["8/5", "14/8", "1/8"], "8/8 = 1."),
    ]
    for text, ans, dist, expl in subs:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    decomp = [
        ("3/8 = 1/8 + 1/8 + ?", "1/8", ["3/8", "2/8", "8/8"], "Three copies of 1/8."),
        ("5/6 = 2/6 + ?", "3/6", ["5/12", "7/6", "1/6"], "2+3=5 sixths."),
        ("4/4 = 1/4 + 1/4 + 1/4 + ?", "1/4", ["4/1", "0", "2/4"], "Four fourths make a whole."),
        ("How many 1/5 pieces make 4/5?", 4, "4 copies of 1/5."),
        ("2/8 + 3/8 + 1/8 = ?", "6/8", ["6/24", "5/8", "2/3"], "2+3+1=6 eighths."),
    ]
    for item in decomp:
        if len(item) == 4:
            text, ans, expl = item[0], item[1], item[3] if isinstance(item[2], list) else item[2]
            dist = item[2] if isinstance(item[2], list) else None
            qs.append(mq(text, ans, expl, idx, distractors=dist))
        else:
            qs.append(mq(item[0], item[1], item[2], idx))
        idx += 1

    mixed = [
        ("1 2/5 + 2/5 = ?", "1 4/5", ["3 2/5", "1 4/10", "3/5"], "Add the fraction parts: 2/5+2/5=4/5. Whole 1 stays."),
        ("2 1/4 + 1/4 = ?", "2 2/4", ["3/4", "2 1/8", "3 1/4"], "1/4+1/4=2/4."),
        ("1 3/8 + 3/8 = ?", "1 6/8", ["6/8", "2 3/8", "1 6/16"], "3+3=6 eighths."),
        ("3/4 + 3/4 = 6/4 = ?", "1 2/4", ["6/8", "1/2", "3/2"], "4/4 is one whole, leftover 2/4."),
        ("1 5/6 − 2/6 = ?", "1 3/6", ["1 7/6", "3/6", "1 2/6"], "5/6−2/6=3/6."),
        ("2 − 1/4 = ?", "1 3/4", ["1 1/4", "2/4", "7/4"], "2 = 1 4/4. 1 4/4 − 1/4 = 1 3/4."),
        ("1 1/5 − 3/5 = ?", "3/5", ["1 2/5", "2/5", "4/5"], "Rename 1 1/5 as 6/5. 6/5−3/5=3/5."),
        ("Whole number 2 as fourths is…", "8/4", ["2/4", "4/2", "2/8"], "Each whole is 4/4. Two wholes = 8/4."),
    ]
    for text, ans, dist, expl in mixed:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    stories = [
        ("You walk 2/10 mile, then 3/10 mile. How far?", "5/10", ["5/20", "6/10", "1/10"], "2/10+3/10=5/10."),
        ("A pan is 3/4 full. You eat 1/4. What is left?", "2/4", ["4/4", "1/8", "2/8"], "3/4−1/4=2/4."),
        ("Two recipes each need 2/8 cup. Together?", "4/8", ["4/16", "2/16", "1/8"], "2/8+2/8=4/8."),
        ("A board is 5/6 yard. You cut off 1/6. Remaining?", "4/6", ["6/6", "4/12", "1/6"], "5/6−1/6=4/6."),
        ("Pizza: 3/8 + 3/8 eaten. Eaten in all?", "6/8", ["6/16", "3/16", "1"], "6/8 eaten."),
    ]
    for text, ans, dist, expl in stories:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    return _fill(qs, 80, lambda i: mq(
        f"{1 + (i % 4)}/8 + {1 + (i % 3)}/8 = ?",
        f"{(1 + (i % 4)) + (1 + (i % 3))}/8",
        f"Add the numerators. Denominator stays 8.",
        i,
        distractors=[
            f"{(1 + (i % 4)) + (1 + (i % 3))}/16",
            f"{abs((1 + (i % 4)) - (1 + (i % 3)))}/8",
            f"{1 + (i % 4)}/8",
        ],
    ))


def build_unit4():
    title = "Fourth Grade Math Unit 4: Add and Subtract Fractions"
    description = (
        "Add and subtract fractions with the same denominator, decompose fractions, and work with mixed numbers that share a denominator."
    )

    c1 = concept_block(
        "1. Same-size pieces",
        [
            "When denominators match, the pieces are the same size.",
            "2/5 + 1/5 means 2 fifths plus 1 fifth. Count the fifths: 3 fifths. Write 3/5.",
            "The denominator does not change. You are not making pieces smaller or bigger. You are counting them.",
            "A number line with fifths shows hops of 1/5.",
            "Unit fractions add: 1/8 + 1/8 + 1/8 = 3/8.",
            "This only works when the bottom numbers match.",
        ],
        solved(1, "2/5 + 1/5 = ?",
               ["Pieces are fifths.",
                "2 + 1 = 3 pieces.",
                "3/5."],
               "3/5")
        + matching(
            [("2/8 + 3/8", "5/8"), ("1/6 + 4/6", "5/6"),
             ("4/10 + 3/10", "7/10"), ("1/4 + 1/4", "2/4")],
            vid="g4u4-c1-match",
        ),
        kid_tip("Add the tops, keep the bottom", "The bottom names the piece. The top counts how many.")
        + phet_box("frac_intro"),
        1,
    )

    c2 = concept_block(
        "2. Subtract like fractions",
        [
            "5/8 − 2/8: you have 5 eighths, take 2 away. 3 eighths left. 3/8.",
            "Again the denominator stays. You remove some of the same-size pieces.",
            "A whole is n/n. 6/6 − 1/6 = 5/6.",
            "If you subtract all the pieces, you get 0: 5/5 − 5/5 = 0/5 = 0.",
            "Number-line hops backward work the same as minus.",
            "Check by adding the answer to the part you took. You should return to the start.",
        ],
        solved(1, "7/10 − 3/10 = ?",
               ["7 tenths take away 3 tenths.",
                "4 tenths. 4/10."],
               "4/10")
        + watch_out("Subtracting the denominators",
                    "7/10 − 3/10 is not 4/0 and not 4/20. The piece size stays tenths."),
        6,
    )

    c3 = concept_block(
        "3. Decompose a fraction",
        [
            "A fraction is a sum of unit fractions.",
            "3/8 = 1/8 + 1/8 + 1/8. Also 3/8 = 2/8 + 1/8.",
            "Decomposing helps you add in parts and see mixed numbers later.",
            "4/4 = 1/4 + 1/4 + 1/4 + 1/4, and that pile is 1 whole.",
            "Write at least two ways when you can.",
            "This is like breaking 9 into 5+4, but with pieces.",
        ],
        solved(1, "Write 5/6 as 2/6 plus something.",
               ["2/6 + ? = 5/6.",
                "? = 3/6."],
               "3/6")
        + step_reveal(
            ["Look at the numerator.",
             "Split that count into two (or more) friendly counts.",
             "Keep the same denominator on each part.",
             "Check by adding the parts."],
            vid="g4u4-c3-steps",
        ),
        try_this("Unit pile", "Draw the unit pieces. Circle groups. Each group is a smaller fraction with the same bottom.")
        + phet_box("build_frac"),
        11,
    )

    c4 = concept_block(
        "4. Mixed numbers with like denominators",
        [
            "A mixed number has wholes plus a fraction: 1 2/5.",
            "To add 1 2/5 + 2/5, add the fraction parts: 2/5+2/5=4/5. Keep the 1. Answer 1 4/5.",
            "If fraction parts make a whole or more, rename: 3/4+3/4=6/4=1 2/4.",
            "1 whole = 4/4 = 5/5 = 8/8, matching the denominator you are using.",
            "2 = 8/4. That rename helps when you subtract a fraction from a whole.",
            "2 − 1/4: think 1 4/4 − 1/4 = 1 3/4.",
        ],
        solved(1, "3/4 + 3/4 = ?",
               ["3+3=6 fourths. 6/4.",
                "4/4 is 1 whole, leftover 2/4.",
                "1 2/4."],
               "1 2/4")
        + matching(
            [("1 2/5 + 2/5", "1 4/5"), ("2 1/4 + 1/4", "2 2/4"),
             ("8/8", "1"), ("2 as fourths", "8/4")],
            vid="g4u4-c4-match",
        ),
        kid_tip("Wholes and pieces", "Add wholes with wholes. Add pieces with pieces. Then compose extra pieces into a whole if you can."),
        16,
    )

    c5 = concept_block(
        "5. Subtract mixed numbers (like denominators)",
        [
            "1 5/6 − 2/6: subtract pieces 5/6 − 2/6 = 3/6. Whole 1 stays. 1 3/6.",
            "If there are not enough pieces, unbundle a whole.",
            "1 1/5 − 3/5: you cannot take 3 fifths from 1 fifth. Change 1 1/5 into 6/5. Then 6/5 − 3/5 = 3/5.",
            "2 − 1/4 needs the whole written as 1 4/4 first.",
            "Check with addition.",
            "Keep the denominator. Only the numerator and the whole-number part change.",
        ],
        solved(1, "1 1/5 − 3/5 = ?",
               ["Rename 1 1/5 as 6/5.",
                "6/5 − 3/5 = 3/5."],
               "3/5")
        + step_reveal(
            ["Compare the fraction parts.",
             "If you need more pieces, rename one whole as n/n.",
             "Subtract numerators.",
             "Write mixed or proper, and check with plus."],
            vid="g4u4-c5-steps",
        ),
        watch_out("Subtracting the whole from the fraction",
                  "1 1/5 − 3/5 is not 1 − 3. Work in fifths, then see what is left."),
        21,
    )

    c6 = concept_block(
        "6. Fraction stories",
        [
            "Distance, recipes, pizza, and boards often use like fractions.",
            "Walk 2/10 then 3/10 → add. A pan 3/4, eat 1/4 → subtract.",
            "Write the sentence with the same denominator you see in the story.",
            "Label the answer: 5/10 mile, 2/4 of the pan.",
            "If two recipes each need 2/8 cup, that is 2/8 + 2/8, not 2 × 2/8 yet as a new operation — but 2 copies of 2/8 is the same add.",
            "Draw a bar split into equal parts. Shade, then add or cross out.",
        ],
        solved(1, "A board is 5/6 yard. You cut off 1/6 yard. How much remains?",
               ["5/6 − 1/6 = 4/6 yard."],
               "4/6")
        + phet_box("frac_eq"),
        try_this("Same whole in the picture", "Draw one bar as the whole. Both fractions in the story must fit that bar."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Add fractions with the same denominator",
            "Subtract fractions with the same denominator",
            "Decompose fractions into unit pieces",
            "Add mixed numbers",
            "Subtract mixed numbers",
            "Solve fraction stories",
        ],
        body,
        practice_slots(31, 50),
    )
    return title, description, content, _u4_questions()
