"""Third Grade Math units 1–4: multi-digit numbers, multiplication, division within 100."""

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
# UNIT 1: Multi-digit numbers
# ===========================================================================

def _u1_questions():
    qs = []
    idx = 1

    for text, ans, expl in [
        ("In 4,582, what digit is in the thousands place?", 4, "4,582 has 4 thousands, 5 hundreds, 8 tens, and 2 ones."),
        ("In 4,582, what digit is in the hundreds place?", 5, "The hundreds digit is 5."),
        ("In 7,306, what digit is in the tens place?", 0, "7,306 has 0 tens. The 0 holds that place."),
        ("How many thousands are in 9,000?", 9, "9,000 is 9 thousands."),
        ("What is the value of the 6 in 6,140?", 6000, "The 6 is in thousands. 6 thousands = 6,000."),
    ]:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    for text, ans, expl, dist in [
        ("Write 5,000 + 300 + 20 + 4 as a number.", 5324,
         "5 thousands, 3 hundreds, 2 tens, 4 ones = 5,324.", ["5234", "53024", "5342"]),
        ("Write 2,000 + 80 + 9 as a number.", 2089,
         "2 thousands, 0 hundreds, 8 tens, 9 ones = 2,089.", ["289", "2809", "2098"]),
        ("How do you write three thousand sixty?", 3060,
         "3 thousands, 0 hundreds, 6 tens, 0 ones = 3,060.", ["360", "3600", "306"]),
        ("What is 4,107 in expanded form?", "4,000 + 100 + 7",
         "4 thousands + 1 hundred + 7 ones. No extra tens.", ["4,000 + 107", "400 + 100 + 7", "4,100 + 7"]),
        ("Which number is greater: 3,199 or 3,201?", 3201,
         "Thousands are the same. Hundreds: 1 vs 2. 3,201 is greater.", ["3199", "199", "same"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for n, nearest in [(34, 30), (36, 40), (85, 90), (21, 20), (75, 80), (142, 140), (148, 150), (250, 250)]:
        qs.append(mq(
            f"Round {n} to the nearest ten.",
            nearest,
            f"Look at the ones. 5 or more rounds up. Less than 5 stays. {n} rounds to {nearest}.",
            idx,
        ))
        idx += 1

    for n, nearest in [(340, 300), (360, 400), (850, 900), (249, 200), (751, 800), (1_050, 1_000), (1_499, 1_500)]:
        qs.append(mq(
            f"Round {n} to the nearest hundred.",
            nearest,
            f"Look at the tens digit. 5 or more rounds the hundreds up. {n} rounds to {nearest}.",
            idx,
        ))
        idx += 1

    for a, b in [(458, 367), (620, 185), (900, 274), (1_204, 318), (2_050, 1_025)]:
        qs.append(mq(f"{a} + {b} = ?", a + b, f"Add by places. {a} + {b} = {a + b}.", idx))
        idx += 1
    for a, b in [(800, 256), (1_000, 473), (642, 178), (5_000, 1_250), (3_406, 1_128)]:
        qs.append(mq(f"{a} − {b} = ?", a - b, f"Subtract by places. {a} − {b} = {a - b}.", idx))
        idx += 1

    for n in [2_400, 3_050, 4_199, 5_555, 6_080]:
        qs.append(mq(f"What is 10 more than {n}?", n + 10, f"{n} + 10 = {n + 10}.", idx))
        idx += 1
        qs.append(mq(f"What is 100 more than {n}?", n + 100, f"{n} + 100 = {n + 100}.", idx))
        idx += 1
        qs.append(mq(f"What is 1,000 more than {n}?", n + 1000, f"{n} + 1,000 = {n + 1000}.", idx))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"Round {20 + i} to the nearest ten.",
        int(round((20 + i) / 10.0) * 10) if (20 + i) % 10 != 5 else (20 + i) + 5,
        f"Use the ones digit to round {20 + i} to the nearest ten.",
        i,
    ))


def build_unit1():
    title = "Third Grade Math Unit 1: Multi-Digit Numbers"
    description = (
        "Read and write multi-digit numbers, use place value through thousands, round to 10 or 100, "
        "and add and subtract larger numbers."
    )

    c1 = concept_block(
        "1. Place value through thousands",
        [
            "Third grade works with multi-digit numbers. A four-digit number has thousands, hundreds, tens, and ones.",
            "In 4,582 the 4 means 4,000. The 5 means 500. The 8 means 80. The 2 means 2.",
            "A comma can help you read: 4,582 is four thousand five hundred eighty-two.",
            "Zero still holds a place. 7,306 has no extra tens, so a 0 sits in tens.",
            "Each place is 10 times the place to its right. 10 hundreds make 1 thousand.",
            "Think of a thousands cube as 10 hundreds flats stacked together.",
        ],
        solved(1, "What is the value of the 3 in 3,241?",
               ["The 3 is in the thousands place.",
                "3 thousands = 3,000."],
               "3,000")
        + solved(2, "In 5,070, which digit is in the tens place?",
                 ["Write places: thousands | hundreds | tens | ones.",
                  "5 | 0 | 7 | 0. Tens digit is 7."],
                 "7")
        + matching(
            [("thousands", "1,000s"), ("hundreds", "100s"),
             ("4 in 4,200", "4,000"), ("0 in 3,056", "holds the tens place")],
            vid="g3u1-c1-match",
        ),
        kid_tip("Read in chunks", "Say the thousands, then the rest: five thousand… three hundred twelve.")
        + phet_box("compare"),
        1,
    )

    c2 = concept_block(
        "2. Read, write, and expand",
        [
            "Standard form uses digits: 2,089.",
            "Word form uses words: two thousand eighty-nine.",
            "Expanded form shows values: 2,000 + 80 + 9.",
            "If a place is empty, skip it in expanded form, but keep the 0 in standard form.",
            "3,060 is three thousand sixty, not three thousand six. The 6 is tens, not ones.",
            "Practice all three forms. They are the same number wearing different outfits.",
        ],
        solved(1, "Write 5,000 + 300 + 20 + 4 in standard form.",
               ["5 thousands, 3 hundreds, 2 tens, 4 ones.",
                "5,324."],
               "5,324")
        + solved(2, "Write two thousand eighty-nine in digits.",
                 ["2 thousands, 0 hundreds, 8 tens, 9 ones.",
                  "2,089."],
                 "2,089")
        + matching(
            [("4,000 + 100 + 7", "4,107"), ("3,000 + 60", "3,060"),
             ("9,000 + 9", "9,009"), ("1,000 + 200 + 30 + 5", "1,235")],
            vid="g3u1-c2-match",
        ),
        watch_out("Dropping zeros",
                  "Two thousand eighty-nine is 2,089, not 289. The hundreds 0 must stay."),
        6,
    )

    c3 = concept_block(
        "3. Compare and order",
        [
            "Start at the left. Compare thousands first, then hundreds, then tens, then ones.",
            "3,201 > 3,199 because hundreds 2 beats hundreds 1.",
            "If all digits match, the numbers are equal.",
            "Order three numbers by lining them up by place. Find the greatest, then the middle, then the least.",
            "A number line also orders numbers. Farther right is greater.",
            "Use > < = and the words greater than, less than, equal to.",
        ],
        solved(1, "Which is greater: 4,080 or 4,800?",
               ["Thousands are both 4.",
                "Hundreds: 0 vs 8. 8 hundreds is more.",
                "4,800 is greater."],
               "4,800")
        + step_reveal(
            ["Line the numbers up by place.",
             "Compare the left-most place that is different.",
             "The number with the larger digit there is greater.",
             "If you are ordering three numbers, repeat with the leftovers."],
            vid="g3u1-c3-steps",
        ),
        try_this("Same number of digits", "If one number has more digits, it is greater: 1,000 > 999."),
        11,
    )

    c4 = concept_block(
        "4. Round to the nearest ten",
        [
            "Rounding finds a nearby friendly number. It helps you estimate.",
            "To round to the nearest ten, look at the ones digit.",
            "If ones are 0, 1, 2, 3, or 4, the tens digit stays. 34 rounds to 30.",
            "If ones are 5, 6, 7, 8, or 9, the tens digit goes up by 1. 36 rounds to 40. 75 rounds to 80.",
            "A 5 rounds up. That is the rule we use.",
            "148 to the nearest ten is 150. The ones 8 says round the 4 tens up to 5 tens.",
        ],
        solved(1, "Round 34 to the nearest ten.",
               ["Ones digit is 4. That is less than 5.",
                "Tens stay 3. Ones become 0.",
                "30."],
               "30")
        + solved(2, "Round 85 to the nearest ten.",
                 ["Ones digit is 5, so round up.",
                  "8 tens become 9 tens.",
                  "90."],
                 "90")
        + matching(
            [("21 → nearest ten", "20"), ("36 → nearest ten", "40"),
             ("75 → nearest ten", "80"), ("250 → nearest ten", "250")],
            vid="g3u1-c4-match",
        ),
        kid_tip("Halfway goes up", "35 is halfway from 30 to 40. We round 35 to 40."),
        16,
    )

    c5 = concept_block(
        "5. Round to the nearest hundred",
        [
            "To round to the nearest hundred, look at the tens digit (the neighbor on the right).",
            "Tens 0–4: hundreds stay. 340 rounds to 300.",
            "Tens 5–9: hundreds go up. 360 rounds to 400. 850 rounds to 900.",
            "1,050 to the nearest hundred: tens digit is 5, so hundreds go up. 1,050 rounds to 1,100.",
            "Rounding is not the exact amount. It is a nearby landmark.",
        ],
        solved(1, "Round 249 to the nearest hundred.",
               ["Tens digit is 4. Stay.",
                "249 is closer to 200 than to 300.",
                "200."],
               "200")
        + solved(2, "Round 751 to the nearest hundred.",
                 ["Tens digit is 5. Round up.",
                  "7 hundreds become 8 hundreds.",
                  "800."],
                 "800")
        + watch_out("Looking at the wrong digit",
                    "Nearest ten: look at ones. Nearest hundred: look at tens. Do not mix them."),
        21,
    )

    c6 = concept_block(
        "6. Add and subtract multi-digit numbers",
        [
            "Line up places. Add or subtract ones, then tens, then hundreds, then thousands.",
            "Regroup when a place is 10 or more (add) or too small (subtract).",
            "Estimate first by rounding. 458 + 367 is near 500 + 400 = 900. The exact sum should be close.",
            "Fluency within 1,000 still matters. Bigger numbers use the same moves.",
            "Check subtraction with addition.",
            "Keep columns straight. A drifted digit becomes a wrong place.",
        ],
        solved(1, "458 + 367 = ?",
               ["Ones: 8+7=15. Write 5, carry 1 ten.",
                "Tens: 5+6+1=12. Write 2, carry 1 hundred.",
                "Hundreds: 4+3+1=8. Sum 825."],
               "825")
        + solved(2, "800 − 256 = ?",
                 ["Borrow across zeros: hundreds 7, tens 9, ones 10.",
                  "10−6=4, 9−5=4, 7−2=5.",
                  "544."],
                 "544")
        + try_this("Estimate, then compute", "If your exact answer is far from the estimate, look at regrouping.")
        + phet_box("arith"),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Use thousands, hundreds, tens, and ones",
            "Read, write, and expand multi-digit numbers",
            "Compare and order",
            "Round to the nearest ten",
            "Round to the nearest hundred",
            "Add and subtract multi-digit numbers",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u1_questions()


# ===========================================================================
# UNIT 2: What multiplication means
# ===========================================================================

def _u2_questions():
    qs = []
    idx = 1

    groups = [
        ("3 groups of 4. How many in all?", 12, "3 × 4 = 12. Or 4 + 4 + 4 = 12."),
        ("5 groups of 2. How many in all?", 10, "5 × 2 = 10."),
        ("4 groups of 6. How many in all?", 24, "4 × 6 = 24."),
        ("6 groups of 3. How many in all?", 18, "6 × 3 = 18."),
        ("2 groups of 9. How many in all?", 18, "2 × 9 = 18."),
        ("7 groups of 5. How many in all?", 35, "7 × 5 = 35."),
        ("8 groups of 2. How many in all?", 16, "8 × 2 = 16."),
        ("10 groups of 4. How many in all?", 40, "10 × 4 = 40."),
        ("1 group of 7. How many in all?", 7, "1 × 7 = 7. One group is just itself."),
        ("0 groups of 5. How many in all?", 0, "Zero groups means nothing. 0 × 5 = 0."),
    ]
    for text, ans, expl in groups:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    arrays = [
        ("An array has 3 rows of 5. How many?", 15, "3 × 5 = 15."),
        ("4 rows of 4. How many?", 16, "4 × 4 = 16. A square array."),
        ("2 rows of 8. How many?", 16, "2 × 8 = 16."),
        ("5 rows of 6. How many?", 30, "5 × 6 = 30."),
        ("6 rows of 7. How many?", 42, "6 × 7 = 42."),
        ("3 rows of 9. How many?", 27, "3 × 9 = 27."),
        ("1 row of 12. How many?", 12, "1 × 12 = 12."),
        ("9 rows of 3. How many?", 27, "9 × 3 = 27. Same as 3 rows of 9."),
    ]
    for text, ans, expl in arrays:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    repeated = [
        ("5 + 5 + 5 + 5 is the same as…", "4 × 5",
         "Four fives. 4 × 5 = 20.", ["5 × 5", "4 + 5", "9 × 1"]),
        ("3 + 3 + 3 is the same as…", "3 × 3",
         "Three threes. 3 × 3 = 9.", ["3 + 3", "6 × 3", "2 × 3"]),
        ("2 + 2 + 2 + 2 + 2 + 2 is…", "6 × 2",
         "Six twos.", ["2 × 2", "6 + 2", "8 × 2"]),
        ("Write 7 × 4 as repeated addition. How many 4s?", 7,
         "7 groups of 4 means seven 4s added.", None),
        ("4 + 4 + 4 + 4 + 4 = ?", 20, "Five 4s. 5 × 4 = 20.", None),
    ]
    for item in repeated:
        if len(item) == 4:
            text, ans, expl, dist = item
            qs.append(mq(text, ans, expl, idx, distractors=dist))
        else:
            text, ans, expl = item
            qs.append(mq(text, ans, expl, idx))
        idx += 1

    skip = [
        ("Skip-count by 4s: 4, 8, 12, ___. Next?", 16, "Add 4. 12 + 4 = 16."),
        ("Skip-count by 3s: 3, 6, 9, 12, ___. Next?", 15, "12 + 3 = 15."),
        ("Skip-count by 6s four times from 0. Where do you land?", 24, "6, 12, 18, 24."),
        ("5, 10, 15, 20, 25 is skip-counting by…", 5, "Each jump adds 5.", None),
        ("The 4th jump of 8 starting at 0 is…", 32, "8, 16, 24, 32.", None),
    ]
    for item in skip:
        if len(item) == 4:
            text, ans, expl, dist = item
            qs.append(mq(text, ans, expl, idx, distractors=dist))
        else:
            text, ans, expl = item
            qs.append(mq(text, ans, expl, idx))
        idx += 1

    sentences = [
        ("3 × 5 = 15. The 3 and 5 are called…", "factors",
         "Factors are the numbers you multiply. 15 is the product.", ["products", "sums", "differences"]),
        ("In 4 × 6 = 24, the product is…", 24, "The product is the answer to multiply.", None),
        ("6 × 7 and 7 × 6 both equal…", 42, "Turn-around facts. Order does not change the product.", None),
        ("Which equation matches 5 bags with 3 apples each?", "5 × 3 = 15",
         "5 groups of 3.", ["5 + 3 = 8", "3 × 3 = 9", "5 × 5 = 25"]),
        ("8 × 1 = ?", 8, "Any number times 1 is itself.", None),
        ("9 × 0 = ?", 0, "Any number times 0 is 0.", None),
        ("Turn around 3 × 8. What is 8 × 3?", 24, "Same product: 24.", None),
        ("4 × 9 = 36, so 9 × 4 = ?", 36, "Commutative property.", None),
    ]
    for item in sentences:
        if len(item) == 4:
            text, ans, expl, dist = item
            qs.append(mq(text, ans, expl, idx, distractors=dist))
        else:
            text, ans, expl = item
            qs.append(mq(text, ans, expl, idx))
        idx += 1

    for a, b in [(3, 4), (5, 5), (6, 2), (7, 3), (8, 4), (9, 2), (4, 7), (6, 6), (2, 12), (3, 8)]:
        qs.append(mq(f"{a} × {b} = ?", a * b, f"{a} groups of {b} is {a * b}.", idx))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"{2 + (i % 8)} × {3 + (i % 5)} = ?",
        (2 + (i % 8)) * (3 + (i % 5)),
        f"Equal groups: {(2 + (i % 8)) * (3 + (i % 5))}.",
        i,
    ))


def build_unit2():
    title = "Third Grade Math Unit 2: What Multiplication Means"
    description = (
        "See multiplication as equal groups, arrays, and repeated addition. Write × sentences and use turn-around facts."
    )

    c1 = concept_block(
        "1. Equal groups",
        [
            "Multiplication is a fast way to count equal groups.",
            "3 groups of 4 is 3 × 4. That is 12 in all.",
            "The first number often tells how many groups. The second tells how many in each group.",
            "The groups must be equal. 3, 4, and 5 toys in three bags is not 3 × 4.",
            "Zero groups of anything is 0. One group of 7 is 7.",
            "Draw circles of dots. Count by the group size.",
        ],
        solved(1, "4 bags with 6 apples each. How many apples?",
               ["4 equal groups of 6.",
                "6 + 6 + 6 + 6 = 24, or 4 × 6 = 24."],
               "24")
        + matching(
            [("3 groups of 4", "3 × 4"), ("5 groups of 2", "5 × 2"),
             ("0 groups of 9", "0"), ("1 group of 8", "8")],
            vid="g3u2-c1-match",
        ),
        kid_tip("Same size groups", "If the groups are not the same size, add instead of multiplying."),
        1,
    )

    c2 = concept_block(
        "2. Arrays",
        [
            "An array is equal rows of the same number of items.",
            "3 rows of 5 is a 3-by-5 array. 3 × 5 = 15.",
            "You can also say 5 columns of 3. Same 15. That is why 3 × 5 = 5 × 3.",
            "Eggs in a carton, seats in a grid, and window panes are arrays in real life.",
            "A square array has the same number of rows and columns: 4 × 4.",
            "Build arrays with tiles. Seeing the rectangle makes the product feel solid.",
        ],
        solved(1, "An array has 4 rows of 6 stamps. How many stamps?",
               ["4 × 6.",
                "6 + 6 + 6 + 6 = 24."],
               "24")
        + solved(2, "2 rows of 8. How many?",
                 ["2 × 8 = 16.",
                  "Turned: 8 rows of 2 is also 16."],
                 "16")
        + phet_box("area_model"),
        try_this("Turn the paper", "Rotate an array. Rows become columns. The total stays the same."),
        6,
    )

    c3 = concept_block(
        "3. Repeated addition",
        [
            "Multiplication is repeated addition of the same number.",
            "4 × 5 means 5 + 5 + 5 + 5 (four fives) or 4 + 4 + 4 + 4 + 4 (five fours).",
            "Both match 20.",
            "If you write 5 + 5 + 5 + 5, count how many 5s. That number is a factor.",
            "Repeated addition is slow for 9 × 8, so we also learn facts. But it proves what × means.",
            "Do not mix different addends and call it multiply: 3 + 4 + 5 is just add.",
        ],
        solved(1, "Write 3 × 6 as repeated addition and find the sum.",
               ["Three 6s: 6 + 6 + 6.",
                "12 + 6 = 18.",
                "3 × 6 = 18."],
               "18")
        + matching(
            [("4 × 5", "5+5+5+5"), ("2 × 9", "9+9"),
             ("6 × 1", "1+1+1+1+1+1"), ("3 × 3", "3+3+3")],
            vid="g3u2-c3-match",
        ),
        watch_out("Counting the addends wrong",
                  "5 + 5 + 5 is 3 × 5, not 5 × 5. Count how many times the number appears."),
        11,
    )

    c4 = concept_block(
        "4. Skip-count to multiply",
        [
            "Skip-counting is hopping by the same size.",
            "To find 4 × 6, skip-count by 6 four times: 6, 12, 18, 24.",
            "Or skip-count by 4 six times: 4, 8, 12, 16, 20, 24. Same landing.",
            "Fives and tens are friendly: 5, 10, 15, 20… and 10, 20, 30…",
            "Twos are even numbers: 2, 4, 6, 8, 10…",
            "Use skip-counting on fingers: one finger per hop. Stop at the first factor.",
        ],
        solved(1, "Skip-count by 4s to find 5 × 4.",
               ["Four hops? No: 5 hops of 4.",
                "4, 8, 12, 16, 20.",
                "5 × 4 = 20."],
               "20")
        + step_reveal(
            ["Pick the group size as your hop.",
             "Hop as many times as the number of groups.",
             "The last number you say is the product.",
             "Check with an array if you can."],
            vid="g3u2-c4-steps",
        ),
        kid_tip("Fingers are hops", "For 6 × 3, put up 6 fingers. Count 3, 6, 9, 12, 15, 18."),
        16,
    )

    c5 = concept_block(
        "5. Multiplication sentences",
        [
            "A multiplication sentence looks like 3 × 5 = 15.",
            "3 and 5 are factors. 15 is the product.",
            "The × sign means 'groups of' or 'times'.",
            "Match a story: 5 bags with 3 apples → 5 × 3 = 15 apples.",
            "The units go on the product: 15 apples, not 15 bags-apples.",
            "You can write factors in either order. The story order often matches groups × size.",
        ],
        solved(1, "There are 6 packs of 4 crayons. Write a sentence and the product.",
               ["6 groups of 4.",
                "6 × 4 = 24 crayons."],
               "24")
        + matching(
            [("factors of 3 × 8 = 24", "3 and 8"), ("product of 3 × 8", "24"),
             ("7 × 1", "7"), ("9 × 0", "0")],
            vid="g3u2-c5-match",
        ),
        try_this("Label the product", "Always name what you counted: 24 crayons, 15 apples, 12 seats."),
        21,
    )

    c6 = concept_block(
        "6. Turn-around facts",
        [
            "The commutative property says a × b = b × a.",
            "3 × 8 = 24 and 8 × 3 = 24. Same product, turned-around factors.",
            "If you know one fact, you get its partner for free.",
            "Arrays prove it: 3 rows of 8 turned sideways is 8 rows of 3.",
            "This cuts the number of facts you must memorize almost in half.",
            "0 × n = n × 0 = 0. 1 × n = n × 1 = n.",
        ],
        solved(1, "You know 4 × 9 = 36. What is 9 × 4?",
               ["Turn the factors.",
                "Same product: 36."],
               "36")
        + solved(2, "7 × 0 = ?",
                 ["Zero groups, or groups of zero.",
                  "The product is 0."],
                 "0")
        + phet_box("area_model"),
        watch_out("Thinking order always changes the answer",
                  "In addition and multiplication, order does not change the total. In subtraction and division, it does."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Count equal groups",
            "Read arrays as rows times columns",
            "Connect × to repeated addition",
            "Skip-count to find a product",
            "Write factors and products",
            "Use turn-around facts",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u2_questions()


# ===========================================================================
# UNIT 3: Multiplication facts within 100
# ===========================================================================

def _u3_questions():
    qs = []
    idx = 1

    facts = []
    for a, b in [
        (2, 3), (2, 7), (2, 9), (5, 4), (5, 6), (5, 8), (5, 9), (10, 3), (10, 7), (10, 9),
        (0, 6), (0, 12), (1, 8), (1, 11), (3, 3), (3, 4), (3, 6), (3, 7), (3, 8), (3, 9),
        (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
        (6, 6), (6, 7), (6, 8), (6, 9),
        (7, 7), (7, 8), (7, 9),
        (8, 8), (8, 9), (9, 9),
        (6, 3), (7, 5), (8, 2), (9, 4), (8, 6), (9, 5),
    ]:
        facts.append((a, b, a * b))

    for a, b, p in facts:
        qs.append(mq(f"{a} × {b} = ?", p, f"{a} × {b} = {p}.", idx))
        idx += 1

    patterns = [
        ("Any number times 10 ends with a…", "0",
         "10 × 7 = 70. Stick a 0 on the other factor.", ["1", "5", "2"]),
        ("5 × even number ends with…", "0",
         "5 × 4 = 20, 5 × 6 = 30. Even × 5 ends in 0.", ["5", "2", "1"]),
        ("5 × odd number ends with…", "5",
         "5 × 3 = 15, 5 × 7 = 35.", ["0", "2", "1"]),
        ("9 × 4 = 36 and 9 × 5 = 45. The digits of 36 add to…", 9,
         "3 + 6 = 9. Many 9s facts have digits that add to 9.", None),
        ("6 × 7 = 6 × 5 + 6 × 2. That is 30 + 12 = ?", 42,
         "Break 7 into 5 and 2. Distribute.", None),
        ("8 × 6 = 8 × 5 + 8 × 1 = 40 + 8 = ?", 48, "Break 6 into 5 and 1.", None),
        ("7 × 8. Think 7 × 10 − 7 × 2. 70 − 14 = ?", 56, "8 is 10 minus 2.", None),
        ("A square fact: 8 × 8 = ?", 64, "8 eights are 64.", None),
    ]
    for item in patterns:
        if len(item) == 4:
            text, ans, expl, dist = item
            qs.append(mq(text, ans, expl, idx, distractors=dist))
        else:
            text, ans, expl = item
            qs.append(mq(text, ans, expl, idx))
        idx += 1

    stories = [
        ("6 kids each have 4 pencils. How many pencils?", 24, "6 × 4 = 24."),
        ("A muffin tin has 3 rows of 4. How many muffins?", 12, "3 × 4 = 12."),
        ("9 packs of 5 cards. How many cards?", 45, "9 × 5 = 45."),
        ("7 days in a week. How many days in 8 weeks?", 56, "8 × 7 = 56."),
        ("A box holds 6 cans. 9 boxes. How many cans?", 54, "9 × 6 = 54."),
    ]
    for text, ans, expl in stories:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"{3 + (i % 7)} × {4 + (i % 6)} = ?",
        (3 + (i % 7)) * (4 + (i % 6)),
        f"Product is {(3 + (i % 7)) * (4 + (i % 6))}.",
        i,
    ))


def build_unit3():
    title = "Third Grade Math Unit 3: Multiplication Facts Within 100"
    description = (
        "Build fluency with ×0 through ×10, use patterns for 2s, 5s, 9s, and 10s, and break apart factors to find products."
    )

    c1 = concept_block(
        "1. Twos, fives, and tens",
        [
            "Start with the friendliest facts.",
            "×2 is doubles: 2 × 8 = 16. Even numbers.",
            "×5 ends in 0 or 5. Even factor → 0. Odd factor → 5.",
            "×10 sticks a zero on the other factor: 10 × 7 = 70. (That works for whole numbers here.)",
            "Skip-count these until they are automatic.",
            "If you know 5 × 8 = 40, you also know 8 × 5 = 40.",
        ],
        solved(1, "5 × 8 = ?",
               ["Skip-count by 5 eight times, or by 8 five times.",
                "5, 10, 15, 20, 25, 30, 35, 40.",
                "40."],
               "40")
        + solved(2, "10 × 9 = ?",
                 ["Nine tens.",
                  "90."],
                 "90")
        + matching(
            [("2 × 7", "14"), ("5 × 6", "30"), ("10 × 4", "40"), ("5 × 9", "45")],
            vid="g3u3-c1-match",
        ),
        kid_tip("Clock and coins", "Fives match minutes on a clock and nickels. Tens match dimes.")
        + phet_box("arith"),
        1,
    )

    c2 = concept_block(
        "2. Zero and one",
        [
            "The identity property: a × 1 = a. One group of 8 is 8. Eight groups of 1 is 8.",
            "The zero property: a × 0 = 0. Zero groups, or groups with nothing in them, make nothing.",
            "Do not mix this with addition. 8 + 0 = 8, but 8 × 0 = 0.",
            "1 × 1 = 1. 0 × 0 = 0.",
            "These facts are quick wins. Lock them in so they never steal hearts.",
            "In a story, 'none in each box' means × 0.",
        ],
        solved(1, "1 × 12 = ?",
               ["One group of 12, or twelve 1s.",
                "12."],
               "12")
        + solved(2, "0 × 9 = ?",
                 ["Zero nines.",
                  "0."],
                 "0")
        + watch_out("Adding instead of multiplying by 0",
                    "8 + 0 is 8. 8 × 0 is 0. Plus keeps the number. Times zero wipes it out."),
        6,
    )

    c3 = concept_block(
        "3. Threes and fours",
        [
            "×3: skip-count 3, 6, 9, 12, 15, 18, 21, 24, 27, 30.",
            "A triangle has 3 sides. 5 triangles have 5 × 3 = 15 sides.",
            "×4 is double-double. 4 × 7: double 7 is 14, double 14 is 28.",
            "A square has 4 sides. 6 squares have 24 sides.",
            "3 × 4 = 12. That fact is a helper for many others (dozen, clock).",
            "Practice until 3 × 8 and 4 × 9 pop out without skip-counting every time.",
        ],
        solved(1, "3 × 8 = ?",
               ["8 + 8 + 8 = 24.",
                "Or skip-count: 3, 6, 9, 12, 15, 18, 21, 24."],
               "24")
        + solved(2, "4 × 7 using double-double.",
                 ["Double 7 = 14.",
                  "Double 14 = 28.",
                  "4 × 7 = 28."],
                 "28")
        + matching(
            [("3 × 6", "18"), ("3 × 9", "27"), ("4 × 5", "20"), ("4 × 8", "32")],
            vid="g3u3-c3-match",
        ),
        try_this("Double-double for 4s", "Times 4 means times 2, then times 2 again."),
        11,
    )

    c4 = concept_block(
        "4. Sixes and nines",
        [
            "×6 is ×5 plus one more group. 6 × 7 = 5 × 7 + 7 = 35 + 7 = 42.",
            "That is the distributive property: break a factor into parts you know.",
            "×9: the digits of the product often add to 9. 9 × 4 = 36 and 3+6=9. 9 × 6 = 54 and 5+4=9.",
            "Another 9s trick: 9 × 7 = 10 × 7 − 7 = 70 − 7 = 63.",
            "6 × 6 = 36. 9 × 9 = 81. Square facts are landmarks.",
            "Use a fact you know nearby, then add or subtract one group.",
        ],
        solved(1, "6 × 8. Use 5 × 8 plus one more 8.",
               ["5 × 8 = 40.",
                "40 + 8 = 48.",
                "6 × 8 = 48."],
               "48")
        + solved(2, "9 × 6. Use 10 × 6 minus 6.",
                 ["10 × 6 = 60.",
                  "60 − 6 = 54."],
                 "54")
        + step_reveal(
            ["Pick a nearby fact you know (×5 or ×10).",
             "Add or subtract one group of the other factor.",
             "Write the new product.",
             "Say the new fact out loud."],
            vid="g3u3-c4-steps",
        ),
        kid_tip("Hands for 9s", "Hold 10 fingers up. Fold finger number n. Left of the fold is tens, right is ones. 9 × 4: fold finger 4 → 3 tens and 6 ones = 36."),
        16,
    )

    c5 = concept_block(
        "5. Sevens and eights",
        [
            "Sevens and eights feel harder because they are less skip-counted in daily life.",
            "Use break-apart: 7 × 8 = 7 × 5 + 7 × 3 = 35 + 21 = 56.",
            "Or 8 × 7 = 8 × 5 + 8 × 2 = 40 + 16 = 56.",
            "Square facts: 7 × 7 = 49. 8 × 8 = 64.",
            "Once you know 7 × 8, you also know 8 × 7.",
            "A calendar helps 7s: 4 weeks is 28 days. 8 weeks is 56 days.",
        ],
        solved(1, "7 × 8 = ?",
               ["7 × 5 = 35. 7 × 3 = 21.",
                "35 + 21 = 56."],
               "56")
        + solved(2, "8 × 8 = ?",
                 ["8 × 10 = 80. Too big by two 8s.",
                  "80 − 16 = 64.",
                  "Or 8 × 4 = 32, double that is 64."],
                 "64")
        + matching(
            [("7 × 6", "42"), ("7 × 7", "49"), ("8 × 5", "40"), ("8 × 9", "72")],
            vid="g3u3-c5-match",
        ),
        try_this("One new fact a day", "Pick 7 × 8. Write it, draw an array, say it, and use it in a story."),
        21,
    )

    c6 = concept_block(
        "6. Break apart (distributive property)",
        [
            "You can split a factor, multiply the parts, then add.",
            "6 × 7 = 6 × (5 + 2) = 6 × 5 + 6 × 2 = 30 + 12 = 42.",
            "This is how later you will multiply bigger numbers, like 6 × 17.",
            "An area model shows it: a 6-by-7 rectangle splits into 6-by-5 and 6-by-2.",
            "Split the factor you know less well. Keep the other factor whole.",
            "Check by skip-counting or turning the fact around.",
        ],
        solved(1, "8 × 6 using 5 + 1.",
               ["8 × 5 = 40.",
                "8 × 1 = 8.",
                "40 + 8 = 48."],
               "48")
        + phet_box("area_model"),
        watch_out("Forgetting to multiply both parts",
                  "If you split 7 into 5 and 2, you must do 6×5 and 6×2, then add. Not 6×5 plus 2."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Master 2s, 5s, and 10s",
            "Use ×0 and ×1",
            "Learn 3s and 4s (double-double)",
            "Learn 6s and 9s with patterns",
            "Learn 7s and 8s with break-apart",
            "Use the distributive property",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u3_questions()


# ===========================================================================
# UNIT 4: Division within 100
# ===========================================================================

def _u4_questions():
    qs = []
    idx = 1

    share = [
        ("12 cookies shared equally by 3 kids. How many each?", 4, "12 ÷ 3 = 4. 3 × 4 = 12."),
        ("20 stickers shared by 5 kids. How many each?", 4, "20 ÷ 5 = 4."),
        ("18 pencils in 6 equal packs. How many in each pack?", 3, "18 ÷ 6 = 3."),
        ("24 seats in 4 equal rows. How many seats per row?", 6, "24 ÷ 4 = 6."),
        ("30 apples in 5 bags, equal. How many per bag?", 6, "30 ÷ 5 = 6."),
        ("16 crayons for 2 boxes, equal. How many per box?", 8, "16 ÷ 2 = 8."),
        ("9 muffins for 3 plates, equal. How many per plate?", 3, "9 ÷ 3 = 3."),
        ("40 cards for 8 kids, equal. How many each?", 5, "40 ÷ 8 = 5."),
        ("15 grapes for 5 kids. How many each?", 3, "15 ÷ 5 = 3."),
        ("28 days in 4 weeks. How many days per week?", 7, "28 ÷ 4 = 7."),
    ]
    for text, ans, expl in share:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    groups = [
        ("How many groups of 4 fit in 12?", 3, "12 ÷ 4 = 3. Measurement division."),
        ("How many groups of 5 fit in 30?", 6, "30 ÷ 5 = 6."),
        ("How many 2s in 18?", 9, "18 ÷ 2 = 9."),
        ("How many 10s in 70?", 7, "70 ÷ 10 = 7."),
        ("How many 6s in 24?", 4, "24 ÷ 6 = 4."),
        ("How many 8s in 32?", 4, "32 ÷ 8 = 4."),
        ("How many 3s in 27?", 9, "27 ÷ 3 = 9."),
        ("How many 7s in 56?", 8, "56 ÷ 7 = 8."),
        ("How many 9s in 45?", 5, "45 ÷ 9 = 5."),
        ("How many 4s in 36?", 9, "36 ÷ 4 = 9."),
    ]
    for text, ans, expl in groups:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    facts = [(a, b) for a in range(2, 11) for b in range(2, 11) if a * b <= 100]
    for a, b in facts[:25]:
        qs.append(mq(f"{a * b} ÷ {a} = ?", b, f"Because {a} × {b} = {a * b}, so {a * b} ÷ {a} = {b}.", idx))
        idx += 1

    families = [
        ("4 × 6 = 24. What is 24 ÷ 6?", 4, "Division undoes multiplication."),
        ("7 × 5 = 35. What is 35 ÷ 7?", 5, "35 ÷ 7 = 5."),
        ("8 × 8 = 64. What is 64 ÷ 8?", 8, "A number divided by itself in this square fact is 8."),
        ("9 × 4 = 36. What is 36 ÷ 9?", 4, "36 ÷ 9 = 4."),
        ("0 ÷ 5 = ?", 0, "Zero shared among 5 is 0 each. 5 × 0 = 0."),
        ("7 ÷ 1 = ?", 7, "Dividing by 1 leaves the number. 1 × 7 = 7."),
        ("If 6 × ___ = 42, the missing factor is…", 7, "42 ÷ 6 = 7."),
        ("If ___ × 8 = 56, the missing factor is…", 7, "56 ÷ 8 = 7."),
    ]
    for text, ans, expl in families:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"{(3 + (i % 8)) * (4 + (i % 6))} ÷ {3 + (i % 8)} = ?",
        4 + (i % 6),
        f"{3 + (i % 8)} × {4 + (i % 6)} = {(3 + (i % 8)) * (4 + (i % 6))}, so divide to get {4 + (i % 6)}.",
        i,
    ))


def build_unit4():
    title = "Third Grade Math Unit 4: Division Within 100"
    description = (
        "Share equally, find how many groups, use fact families, and find missing factors. Whole-number quotients within 100."
    )

    c1 = concept_block(
        "1. Sharing equally (partitive)",
        [
            "Division can mean sharing a total into equal groups.",
            "12 cookies, 3 kids, equal shares: 12 ÷ 3 = 4 cookies each.",
            "The total is the dividend. The number of groups is the divisor. Each share is the quotient.",
            "You can deal like cards: one for you, one for you, one for you, repeat until gone.",
            "If it shares evenly, nothing is left over. In this unit we stay with even shares.",
            "Check: groups × share = total. 3 × 4 = 12.",
        ],
        solved(1, "20 stickers shared by 5 kids. How many each?",
               ["20 ÷ 5.",
                "5 × 4 = 20, so each kid gets 4."],
               "4")
        + matching(
            [("12 ÷ 3", "4 each"), ("18 ÷ 6", "3 each"),
             ("30 ÷ 5", "6 each"), ("check 4 × 5", "20")],
            vid="g3u4-c1-match",
        ),
        kid_tip("Deal them out", "Use counters. Make the same number of piles as kids. Deal until gone.")
        + phet_box("arith"),
        1,
    )

    c2 = concept_block(
        "2. How many groups (measurement)",
        [
            "Division can also mean: how many groups of this size fit in the total?",
            "How many groups of 4 fit in 12? 12 ÷ 4 = 3 groups.",
            "Think skip-counting: 4, 8, 12. Three hops.",
            "Or subtract 4 again and again: 12 − 4 = 8, 8 − 4 = 4, 4 − 4 = 0. Three subtracts.",
            "Same equation 12 ÷ 4 = 3, different picture: 3 groups of 4, not 4 shares of 3 — actually 12÷4=3 could be either, depending on the story.",
            "Read the story. 'How many each' vs 'how many groups'.",
        ],
        solved(1, "A box holds 6 cans. You have 24 cans. How many boxes?",
               ["How many 6s in 24?",
                "24 ÷ 6 = 4 boxes.",
                "Check: 4 × 6 = 24."],
               "4")
        + step_reveal(
            ["Find the total.",
             "Find the size of one group.",
             "Ask how many of those groups fit.",
             "Skip-count or use a × fact to find the quotient."],
            vid="g3u4-c2-steps",
        ),
        try_this("Skip-count up", "To do 36 ÷ 4, count 4, 8, 12… until 36. Count the hops. That is 9."),
        6,
    )

    c3 = concept_block(
        "3. Fact families",
        [
            "Multiply and divide belong together, like plus and minus.",
            "For 3, 5, and 15: 3×5=15, 5×3=15, 15÷5=3, 15÷3=5.",
            "If you know one, you can write the other three.",
            "Division undoes multiplication. That is why we learn them in the same grade.",
            "A triangle of three numbers is a family. The biggest number is the product (and the dividend).",
            "0 and 1 have special families: 7×1=7, 7÷1=7, 7÷7=1. And 0÷5=0 because 5×0=0.",
        ],
        solved(1, "4 × 6 = 24. What is 24 ÷ 6?",
               ["24 is the product.",
                "Divide by one factor to get the other.",
                "24 ÷ 6 = 4."],
               "4")
        + matching(
            [("3, 8, 24", "24 ÷ 8 = 3"), ("5, 7, 35", "35 ÷ 5 = 7"),
             ("9, 9, 81", "81 ÷ 9 = 9"), ("2, 12, 24", "24 ÷ 2 = 12")],
            vid="g3u4-c3-match",
        ),
        watch_out("Dividing the small by the big",
                  "In these families the dividend is the largest number. 24 ÷ 6, not 6 ÷ 24, for whole-number facts within 100."),
        11,
    )

    c4 = concept_block(
        "4. Use a multiply fact to divide",
        [
            "When you see 56 ÷ 7, ask: 7 times what is 56?",
            "That missing factor is the quotient.",
            "This is why memorizing × facts makes ÷ faster.",
            "If you cannot recall, skip-count by 7 until you hit 56, or break 56 apart.",
            "56 ÷ 7: maybe 7×5=35, leftover 21, 7×3=21, so 5+3=8. Quotient 8.",
            "Check by multiplying quotient × divisor. You must get the dividend.",
        ],
        solved(1, "56 ÷ 7 = ?",
               ["7 × ? = 56.",
                "7 × 8 = 56.",
                "Quotient 8."],
               "8")
        + solved(2, "45 ÷ 9 = ?",
                 ["9 × 5 = 45.",
                  "5."],
                 "5")
        + kid_tip("Think times", "Every divide problem is a multiply problem with a hole in it."),
        16,
    )

    c5 = concept_block(
        "5. Missing factors",
        [
            "Sometimes a sentence looks like 6 × ___ = 42.",
            "The hole is a missing factor. Fill it with division: 42 ÷ 6 = 7.",
            "___ × 8 = 56 → 56 ÷ 8 = 7.",
            "Unknown number of groups, or unknown group size — both are missing factors.",
            "Write the related divide sentence under the multiply sentence.",
            "Then check by putting the number back: 6 × 7 = 42. Yes.",
        ],
        solved(1, "6 × ___ = 42. What number is missing?",
               ["42 ÷ 6 = 7.",
                "Check: 6 × 7 = 42."],
               "7")
        + step_reveal(
            ["Find the product (the known whole).",
             "Find the known factor.",
             "Divide to get the missing factor.",
             "Multiply to check."],
            vid="g3u4-c5-steps",
        ),
        try_this("Box the hole", "Draw a box around the missing number. The other two numbers tell you how to divide."),
        21,
    )

    c6 = concept_block(
        "6. Division stories",
        [
            "Stories use share, each, split equally, how many groups, packed into…",
            "Write a ÷ sentence. Then solve with a × fact.",
            "Label the quotient: 4 cookies each, or 4 boxes — depending on the question.",
            "If leftover would happen, we are not covering that yet. These stories share evenly.",
            "Two kinds: 24 ÷ 6 might be 6 kids get 4, or 4 boxes of 6. Read what is asked.",
            "Draw equal groups or an array. Arrays work both ways: 4 rows of 6 is 24, so 24 ÷ 6 = 4 rows.",
        ],
        solved(1, "32 seats. 8 seats per row. How many rows?",
               ["How many 8s in 32?",
                "32 ÷ 8 = 4 rows.",
                "Check: 4 × 8 = 32."],
               "4")
        + solved(2, "32 seats in 4 equal rows. How many seats per row?",
                 ["Share 32 into 4 rows.",
                  "32 ÷ 4 = 8 seats per row."],
                 "8")
        + matching(
            [("share 12 among 3", "4 each"), ("how many 4s in 12", "3 groups"),
             ("missing factor 6 × ? = 42", "7"), ("check divide", "multiply back")],
            vid="g3u4-c6-match",
        ),
        watch_out("Mixing 'each' and 'how many groups'",
                  "Both use ÷. The question sentence tells you which number is the answer."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Share a total into equal groups",
            "Find how many groups fit",
            "Write multiply-divide fact families",
            "Use a × fact to divide",
            "Find a missing factor",
            "Solve division stories",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u4_questions()
