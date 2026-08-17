"""Second Grade Math units 1–4: numbers to 1,000, regrouping add/sub, two-step stories."""

from curriculum_kit import (
    lesson_figure,
    svg_dots,
    svg_ten_frame,
    svg_number_line,
    svg_clock,
    svg_tape,
    svg_coins,
    svg_base10,
    svg_rect,
    svg_fraction_bar,
    svg_balance,
)

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
# UNIT 1: Numbers to 1,000
# ===========================================================================

def _u1_questions():
    qs = []
    idx = 1

    for text, ans, expl, dist in [
        ("Count by ones: 198, 199, ___. What is next?", 200,
         "After 199 we make a new hundred. Next is 200.", None),
        ("What number comes after 999?", 1000,
         "999 + 1 = 1,000. That is ten hundreds, or one thousand.", ["999", "1001", "900"]),
        ("What number comes before 500?", 499,
         "One less than 500 is 499.", None),
        ("Count by tens: 340, 350, 360, ___. What is next?", 370,
         "Each jump adds 10. 360 + 10 = 370.", None),
        ("Count by hundreds: 200, 300, 400, ___. What is next?", 500,
         "Each jump adds 100. Next is 500.", None),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, expl in [
        ("In 347, what digit is in the hundreds place?", 3, "347 has 3 hundreds, 4 tens, and 7 ones."),
        ("In 347, what digit is in the tens place?", 4, "The middle digit is tens. 4 tens."),
        ("In 347, what digit is in the ones place?", 7, "The last digit is ones. 7 ones."),
        ("How many hundreds are in 800?", 8, "800 is 8 hundreds. 8 × 100 = 800."),
        ("How many tens are in 60?", 6, "60 is 6 tens."),
    ]:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    for text, ans, expl, dist in [
        ("Write 300 + 40 + 5 as a number.", 345,
         "3 hundreds, 4 tens, 5 ones. That is 345.", ["354", "435", "305"]),
        ("Write 700 + 20 + 9 as a number.", 729,
         "7 hundreds, 2 tens, 9 ones = 729.", ["792", "279", "709"]),
        ("What is 246 in expanded form?", "200 + 40 + 6",
         "2 hundreds + 4 tens + 6 ones.", ["200 + 46", "20 + 40 + 6", "246"]),
        ("How do you write four hundred twelve?", 412,
         "4 hundreds, 1 ten, 2 ones. 412.", ["420", "402", "421"]),
        ("How do you write six hundred eight?", 608,
         "6 hundreds, 0 tens, 8 ones. 608. The 0 holds the tens place.", ["680", "68", "618"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for a, b in [(412, 421), (305, 350), (199, 200), (870, 807), (555, 505), (999, 909)]:
        bigger = max(a, b)
        qs.append(mq(
            f"Which number is greater: {a} or {b}?",
            bigger,
            f"Compare hundreds first, then tens, then ones. {bigger} is greater.",
            idx,
            distractors=[min(a, b), str(abs(a - b)), "same"],
        ))
        idx += 1

    for n in [234, 450, 701, 888, 199, 560, 325, 640]:
        qs.append(mq(f"What is 10 more than {n}?", n + 10, f"Add 1 ten. {n} + 10 = {n + 10}.", idx))
        idx += 1
    for n in [234, 450, 711, 888, 205, 560]:
        qs.append(mq(f"What is 10 less than {n}?", n - 10, f"Take 1 ten. {n} − 10 = {n - 10}.", idx))
        idx += 1
    for n in [234, 450, 701, 199, 560, 325, 640, 100]:
        qs.append(mq(f"What is 100 more than {n}?", n + 100, f"Add 1 hundred. {n} + 100 = {n + 100}.", idx))
        idx += 1
    for n in [234, 450, 701, 888, 560, 325]:
        qs.append(mq(f"What is 100 less than {n}?", n - 100, f"Take 1 hundred. {n} − 100 = {n - 100}.", idx))
        idx += 1

    for n in [250, 400, 550, 700, 850]:
        qs.append(mq(f"Count by fifties. What comes after {n}?", n + 50, f"{n} + 50 = {n + 50}.", idx))
        idx += 1

    skip100 = [100, 200, 300, 400, 500, 600, 700, 800]
    for n in skip100:
        qs.append(mq(f"Count by hundreds. What comes after {n}?", n + 100, f"{n} + 100 = {n + 100}.", idx))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"What is 10 more than {200 + i}?",
        210 + i,
        f"Add one ten: {200 + i} + 10 = {210 + i}.",
        i,
    ))


def build_unit1():
    title = "Second Grade Math Unit 1: Numbers to 1,000"
    description = (
        "Count to 1,000, use hundreds-tens-ones, write expanded form, compare three-digit numbers, "
        "and jump 10 or 100 more and less."
    )

    c1 = concept_block(
        "1. Count to 1,000",
        [
            "In second grade we count much farther. We go all the way to 1,000.",
            "After 99 we say 100. After 199 we say 200. After 999 we say 1,000.",
            "One thousand is ten hundreds. It is also 100 tens.",
            "Count by ones near a new hundred: 398, 399, 400. The ones roll over, then the tens roll over.",
            "Skip-count to move faster: by 5s, 10s, and 100s.",
            "Say numbers out loud. Big numbers feel friendly when you hear them.",
        ],
        lesson_figure(
            svg_number_line(196, 204, marks=[(199, "199"), (200, "200")], highlight=200),
            "199 then 200",
            "199 has 9 tens and 9 ones. One more rolls the ones and tens into a new hundred: 200.",
        )
        + solved(1, "What comes after 199?",
               ["199 is 1 hundred, 9 tens, and 9 ones.",
                "One more one makes 10 ones, which become 1 more ten. Now you have 10 tens.",
                "10 tens make 1 more hundred. So 199 + 1 = 200."],
               "200")
        + solved(2, "Count by hundreds: 400, 500, 600, ___. What is next?",
                 ["Each jump adds 100.",
                  "600 + 100 = 700."],
                 "700")
        + matching(
            [("100", "one hundred"), ("500", "five hundred"),
             ("1,000", "one thousand"), ("250", "two hundred fifty")],
            vid="g2u1-c1-match",
        ),
        kid_tip("New hundred", "When you hear ninety-nine, the next number starts a new hundred: 199 then 200.")
        + phet_box("compare"),
        1,
    )

    c2 = concept_block(
        "2. Hundreds, tens, and ones",
        [
            "A three-digit number has three places: hundreds, tens, and ones.",
            "In 582, the 5 is hundreds, the 8 is tens, and the 2 is ones.",
            "5 hundreds = 500. 8 tens = 80. 2 ones = 2. Together: 582.",
            "The place of a digit matters more than the digit itself. 5 in hundreds is 500. 5 in ones is just 5.",
            "Zero can hold a place. 704 has 0 tens. Do not skip that 0 when you write it.",
            "Think of base-ten blocks: flats for hundreds, rods for tens, little cubes for ones.",
        ],
        lesson_figure(
            '<svg viewBox="0 0 220 64" width="220" role="img">'
            '<rect x="8" y="8" width="44" height="44" fill="#7dd3fc" stroke="#0c4a6e"/>'
            '<rect x="58" y="8" width="44" height="44" fill="#7dd3fc" stroke="#0c4a6e"/>'
            '<rect x="108" y="8" width="44" height="44" fill="#7dd3fc" stroke="#0c4a6e"/>'
            '<rect x="158" y="8" width="44" height="44" fill="#7dd3fc" stroke="#0c4a6e"/>'
            '<text x="110" y="60" text-anchor="middle" font-size="11">4 hundreds</text></svg>'
            + svg_base10(6, 1),
            "461 as hundreds, tens, and ones",
            "Four flats are 4 hundreds. Six rods are 6 tens. One cube is 1 one. The hundreds digit is 4.",
        )
        + solved(1, "What is the hundreds digit in 461?",
               ["Write 461 with places: hundreds | tens | ones.",
                "4 is in hundreds, 6 in tens, 1 in ones.",
                "The hundreds digit is 4."],
               "4")
        + solved(2, "How much is the 7 worth in 270?",
                 ["The 7 is in the tens place.",
                  "7 tens = 70."],
                 "70")
        + step_reveal(
            ["Look at 835.",
             "Hundreds digit: 8 → 800.",
             "Tens digit: 3 → 30.",
             "Ones digit: 5 → 5.",
             "800 + 30 + 5 = 835."],
            prompt="What is 8 worth in 835?",
            vid="g2u1-c2-steps",
            answer="800",
        ),
        watch_out("Mixing 405 and 450",
                  "405 has 4 hundreds, 0 tens, 5 ones. 450 has 4 hundreds, 5 tens, 0 ones. The zero sits in a different place."),
        6,
    )

    c3 = concept_block(
        "3. Read and write numbers to 1,000",
        [
            "We say a number in words and write it with digits.",
            "412 is four hundred twelve. 420 is four hundred twenty. Listen for twelve vs twenty.",
            "If there are no tens, say the hundreds and then the ones: 608 is six hundred eight.",
            "1,000 is one thousand. Some people write 1000 without a comma. Both mean the same amount.",
            "Expanded form shows the value of each digit: 412 = 400 + 10 + 2.",
            "Practice reading a number, then writing it, then expanding it.",
        ],
        lesson_figure(
            svg_tape([300, 40, 6], ["300", "40", "6"]),
            "Three hundred forty-six",
            "Three hundred puts 3 in hundreds, forty puts 4 in tens, six puts 6 in ones. Write 346.",
        )
        + solved(1, "How do we write three hundred forty-six?",
               ["Three hundred → 3 in hundreds.",
                "Forty → 4 in tens.",
                "Six → 6 in ones. Write 346."],
               "346")
        + solved(2, "Write 500 + 9 as a three-digit number.",
                 ["5 hundreds, 0 tens, 9 ones.",
                  "The 0 must stay in the tens place.",
                  "Write 509."],
                 "509")
        + matching(
            [("200 + 30 + 4", "234"), ("600 + 8", "608"),
             ("900 + 90 + 9", "999"), ("100 + 50", "150")],
            vid="g2u1-c3-match",
        ),
        try_this("Say it in parts", "Say hundreds, then tens, then ones. Four hundred… fifty… two. Then write 452."),
        11,
    )

    c4 = concept_block(
        "4. Compare three-digit numbers",
        [
            "To compare, start at the left. Look at hundreds first.",
            "If hundreds are different, the number with more hundreds is greater. 512 > 498 because 5 hundreds beat 4 hundreds.",
            "If hundreds are the same, compare tens. If tens are the same, compare ones.",
            "The symbols: > means greater than. < means less than. = means equal.",
            "The open mouth of > or < faces the bigger number. 800 > 799.",
            "Equal numbers match in every place: 707 = 707.",
        ],
        lesson_figure(
            '<svg viewBox="0 0 320 150" width="100%" style="max-width:320px" role="img">'
            '<rect x="36" y="16" width="56" height="104" fill="#86efac" stroke="#0f172a"/>'
            '<text x="64" y="72" text-anchor="middle" font-size="13" font-weight="700">671</text>'
            '<text x="64" y="138" text-anchor="middle" font-size="11">7 tens</text>'
            '<rect x="130" y="64" width="56" height="56" fill="#93c5fd" stroke="#0f172a"/>'
            '<text x="158" y="96" text-anchor="middle" font-size="13" font-weight="700">617</text>'
            '<text x="158" y="138" text-anchor="middle" font-size="11">1 ten</text>'
            '<text x="250" y="80" text-anchor="middle" font-size="16" font-weight="700">671 &gt; 617</text></svg>',
            "Compare 671 and 617",
            "Hundreds are both 6, so look at tens. 7 tens beat 1 ten, so 671 is greater.",
        )
        + solved(1, "Which is greater: 671 or 617?",
               ["Hundreds are both 6. Same.",
                "Tens: 7 vs 1. 7 tens is more.",
                "671 is greater."],
               "671")
        + solved(2, "True or not: 409 < 490?",
                 ["Hundreds are both 4.",
                  "Tens: 0 vs 9. 9 tens is more, so 490 is greater.",
                  "Yes, 409 is less than 490."],
                 "true")
        + matching(
            [("812 compared with 781", "812 is greater"), ("305 compared with 350", "305 is less"),
             ("444 compared with 444", "equal"), ("199 compared with 200", "199 is less")],
            vid="g2u1-c4-match",
        ),
        kid_tip("Start left", "Always compare hundreds first. Do not look at the ones until the left digits are the same.")
        + phet_box("compare"),
        16,
    )

    c5 = concept_block(
        "5. Ten more, ten less, 100 more, 100 less",
        [
            "Adding 10 changes the tens digit (unless you make a new hundred).",
            "10 more than 346 is 356. The 4 tens become 5 tens. Ones stay 6. Hundreds stay 3.",
            "10 less than 346 is 336.",
            "Adding 100 changes the hundreds digit. 100 more than 346 is 446.",
            "100 less than 346 is 246.",
            "These jumps help you move on a number line without counting by ones.",
        ],
        lesson_figure(
            svg_number_line(590, 600, marks=[(590, "590"), (600, "+10")], highlight=600),
            "10 more than 590",
            "590 already has 9 tens. One more ten makes 10 tens, which become the next hundred: 600.",
        )
        + solved(1, "What is 10 more than 590?",
               ["590 has 9 tens. One more ten makes 10 tens.",
                "10 tens become 1 extra hundred.",
                "590 + 10 = 600."],
               "600")
        + solved(2, "What is 100 less than 702?",
                 ["Take 1 hundred from 7 hundreds.",
                  "Tens and ones stay 0 and 2.",
                  "702 − 100 = 602."],
                 "602")
        + step_reveal(
            ["Start at 245.",
             "10 more → 255.",
             "100 more from there → 355.",
             "10 less from 355 → 345."],
            vid="g2u1-c5-steps",
        ),
        watch_out("Only one place changes… except when it rolls over",
                  "Usually 10 more changes tens only. But 590 + 10 rolls into 600. Watch for 9 tens or 9 hundreds."),
        21,
    )

    c6 = concept_block(
        "6. Skip-count by 5s, 10s, and 100s",
        [
            "Skip-counting is counting with a steady jump.",
            "By 5s: 5, 10, 15, 20… This later helps with clocks and money.",
            "By 10s: 230, 240, 250… The ones digit stays the same.",
            "By 100s: 100, 200, 300… up to 1,000.",
            "You can start in the middle: 465, 475, 485 if you jump by tens.",
            "Clap the jumps. A beat helps your brain remember the pattern.",
        ],
        lesson_figure(
            svg_tape([10, 10, 10], ["670 to 680", "680 to 690", "690 to 700"]),
            "Skip-count by tens to 700",
            "Each hop adds 10. The ones digit stays 0. 690 + 10 rolls into 700.",
        )
        + solved(1, "Count by tens: 670, 680, 690, ___. Next?",
               ["Add 10 each time.",
                "690 + 10 = 700."],
               "700")
        + solved(2, "Count by fives: 85, 90, 95, ___. Next?",
                 ["Add 5.",
                  "95 + 5 = 100."],
                 "100")
        + matching(
            [("jump 5 from 40", "45"), ("jump 10 from 390", "400"),
             ("jump 100 from 250", "350"), ("jump 5 from 115", "120")],
            vid="g2u1-c6-match",
        ),
        try_this("Same ones digit", "When you skip-count by 10, the ones digit does not change: 403, 413, 423 all end with 3."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Count to 1,000, including past 199, 299, and 999",
            "Name hundreds, tens, and ones",
            "Read, write, and expand numbers",
            "Compare three-digit numbers",
            "Find 10 or 100 more and less",
            "Skip-count by 5s, 10s, and 100s",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u1_questions()


# ===========================================================================
# UNIT 2: Addition with regrouping
# ===========================================================================

def _u2_questions():
    qs = []
    idx = 1

    for a, b in [(23, 14), (41, 35), (50, 28), (62, 17), (34, 22)]:
        qs.append(mq(f"{a} + {b} = ?", a + b, f"Add ones, then tens. {a} + {b} = {a + b}.", idx))
        idx += 1

    for a, b in [(27, 15), (38, 27), (46, 19), (59, 18), (67, 25)]:
        qs.append(mq(
            f"{a} + {b} = ? (you will regroup ones)",
            a + b,
            f"Ones: {a % 10}+{b % 10} = {a % 10 + b % 10}. That is 1 ten and {(a + b) % 10} ones. Total {a + b}.",
            idx,
        ))
        idx += 1

    for a, b in [(48, 36), (57, 28), (69, 17), (35, 47), (26, 58)]:
        qs.append(mq(f"{a} + {b} = ?", a + b, f"Regroup ones into a ten. {a} + {b} = {a + b}.", idx))
        idx += 1

    for a, b in [(125, 134), (240, 318), (402, 155), (216, 243), (330, 120)]:
        qs.append(mq(f"{a} + {b} = ?", a + b, f"Add ones, tens, hundreds. {a} + {b} = {a + b}.", idx))
        idx += 1

    for a, b in [(158, 167), (275, 148), (369, 257), (486, 129), (199, 126)]:
        qs.append(mq(
            f"{a} + {b} = ? (regroup if you need to)",
            a + b,
            f"Line up places. Regroup 10 ones as 1 ten, and 10 tens as 1 hundred if needed. {a}+{b}={a+b}.",
            idx,
        ))
        idx += 1

    for a, b, c in [(12, 23, 14), (25, 25, 25), (40, 18, 11), (19, 19, 19), (30, 20, 15)]:
        qs.append(mq(f"{a} + {b} + {c} = ?", a + b + c, f"Add two first, then the third. Sum is {a + b + c}.", idx))
        idx += 1

    for n in [45, 70, 123, 208, 350, 499]:
        qs.append(mq(f"What is {n} + 10?", n + 10, f"{n} + 10 = {n + 10}.", idx))
        idx += 1
        qs.append(mq(f"What is {n} + 100?", n + 100, f"{n} + 100 = {n + 100}.", idx))
        idx += 1

    stories = [
        ("A box has 28 crayons. You put in 17 more. How many crayons?", 45, "28 + 17 = 45. Regroup 15 ones as 1 ten and 5 ones."),
        ("Mia has 136 stickers. Sam gives her 48. How many stickers now?", 184, "136 + 48 = 184."),
        ("A school has 215 kids in grade 1 and 188 in grade 2. How many kids in both grades?", 403, "215 + 188 = 403."),
        ("You read 47 pages, then 36 more. How many pages?", 83, "47 + 36 = 83."),
        ("A jar has 250 beans. You add 175. How many beans?", 425, "250 + 175 = 425."),
    ]
    for text, ans, expl in stories:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"{30 + i} + {15 + (i % 9)} = ?",
        30 + i + 15 + (i % 9),
        f"Add the two numbers. The sum is {30 + i + 15 + (i % 9)}.",
        i,
    ))


def build_unit2():
    title = "Second Grade Math Unit 2: Addition with Regrouping"
    description = (
        "Add two-digit and three-digit numbers. Regroup 10 ones as 1 ten, and 10 tens as 1 hundred."
    )

    c1 = concept_block(
        "1. Add two-digit numbers without regrouping",
        [
            "Line the numbers up. Ones under ones. Tens under tens.",
            "Add the ones first. Then add the tens.",
            "If ones add to 9 or less, you do not regroup. 32 + 45: 2+5=7 ones, 3+4=7 tens. Sum 77.",
            "Zeros are easy: 40 + 23 = 63. The ones are just 3.",
            "You can also add tens first in your head: 30+40=70, then 2+5=7, total 77.",
            "Check by adding the other way: 45 + 32 should match.",
        ],
        lesson_figure(
            svg_base10(4, 1) + svg_base10(2, 6),
            "41 + 26 with tens rods and ones",
            "4 tens and 1 one plus 2 tens and 6 ones. Ones: 1+6=7. Tens: 4+2=6. Sum 67.",
        )
        + solved(1, "41 + 26 = ?",
               ["Ones: 1 + 6 = 7.",
                "Tens: 4 + 2 = 6.",
                "Write 67."],
               "67")
        + solved(2, "50 + 18 = ?",
                 ["Ones: 0 + 8 = 8.",
                  "Tens: 5 + 1 = 6.",
                  "68."],
                 "68")
        + matching(
            [("22 + 33", "55"), ("40 + 19", "59"), ("61 + 17", "78"), ("15 + 70", "85")],
            vid="g2u2-c1-match",
        ),
        kid_tip("Line up", "If the digits drift, you add the wrong places. Keep ones in a straight column.")
        + phet_box("ten"),
        1,
    )

    c2 = concept_block(
        "2. Regroup ones into a ten",
        [
            "Sometimes ones add to 10 or more. Then we regroup.",
            "Regroup means: 10 ones become 1 ten. Write the leftover ones. Carry the new ten to the tens place.",
            "Example: 27 + 15. Ones: 7+5=12. That is 1 ten and 2 ones. Write 2. Add the extra ten with the tens.",
            "Tens: 2 + 1 + 1 (the new ten) = 4 tens. Answer 42.",
            "People also call this carrying. Same idea: you carry a ten next door.",
            "Play Make a Ten. When you snap 10 ones together, that is regrouping.",
        ],
        lesson_figure(
            svg_ten_frame(15),
            "Ones 8 + 7 = 15",
            "15 ones fill one ten-frame and leave 5. Write 5 in ones and carry the new ten. 38 + 27 = 65.",
        )
        + solved(1, "38 + 27 = ?",
               ["Ones: 8 + 7 = 15. Write 5. Carry 1 ten.",
                "Tens: 3 + 2 + 1 = 6.",
                "65."],
               "65")
        + step_reveal(
            ["Look at 46 + 19.",
             "Add ones: 6 + 9 = 15.",
             "15 = 1 ten + 5 ones. Write 5 in ones.",
             "Add tens: 4 + 1 + the new 1 = 6.",
             "The sum is 65."],
            prompt="What do you write in the ones place?",
            vid="g2u2-c2-steps",
            answer="5",
        ),
        watch_out("Forgetting the new ten",
                  "If ones make 15 and you write 5 but forget to add the extra ten, your answer is 10 too small."),
        6,
    )

    c3 = concept_block(
        "3. Two-digit plus two-digit with regrouping",
        [
            "Practice until regrouping feels normal.",
            "Always ones first. Always check if ones are 10 or more.",
            "If ones are 9 or less, just write them. If 10–18, regroup.",
            "The biggest ones you meet with two digits is 9+9=18. That is 1 ten and 8 ones.",
            "You can estimate first: 48 + 36 is near 50 + 40 = 90. The exact sum should be close.",
            "Draw tens rods and ones cubes if the paper feels crowded.",
        ],
        lesson_figure(
            svg_base10(5, 7) + svg_base10(2, 8),
            "57 + 28 with tens and ones",
            "Ones 7+8=15, so write 5 and carry 1 ten. Tens 5+2+1=8. Sum 85.",
        )
        + solved(1, "57 + 28 = ?",
               ["Ones: 7+8=15. Write 5, carry 1.",
                "Tens: 5+2+1=8.",
                "85."],
               "85")
        + solved(2, "69 + 14 = ?",
                 ["Ones: 9+4=13. Write 3, carry 1.",
                  "Tens: 6+1+1=8.",
                  "83."],
                 "83")
        + matching(
            [("25 + 18", "43"), ("47 + 36", "83"), ("59 + 22", "81"), ("38 + 45", "83")],
            vid="g2u2-c3-match",
        ),
        try_this("Make a ten first", "38 + 27: take 2 from 27 to make 38 into 40. Then 40 + 25 = 65. Same answer, different path.")
        + phet_box("arith"),
        11,
    )

    c4 = concept_block(
        "4. Three-digit addition",
        [
            "Same rules, one more place: hundreds.",
            "Add ones, then tens, then hundreds. Regroup whenever a place hits 10 or more.",
            "You might regroup ones, or tens, or both.",
            "Example: 158 + 167. Ones 8+7=15 → write 5, carry 1 ten. Tens 5+6+1=12 → write 2, carry 1 hundred. Hundreds 1+1+1=3. Sum 325.",
            "Keep columns straight. Three-digit numbers need three columns.",
            "If a place is 0, it is still a place. 204 + 158 still has a tens column.",
        ],
        lesson_figure(
            svg_tape([246, 135], ["246", "135"]),
            "246 + 135",
            "Add ones, then tens, then hundreds. Ones 6+5=11, so write 1 and carry a ten. Sum 381.",
        )
        + solved(1, "246 + 135 = ?",
               ["Ones: 6+5=11. Write 1, carry 1 ten.",
                "Tens: 4+3+1=8.",
                "Hundreds: 2+1=3. Sum 381."],
               "381")
        + solved(2, "275 + 148 = ?",
                 ["Ones: 5+8=13. Write 3, carry 1.",
                  "Tens: 7+4+1=12. Write 2, carry 1 hundred.",
                  "Hundreds: 2+1+1=4. Sum 423."],
                 "423")
        + step_reveal(
            ["Write 369 + 257 in columns.",
             "Ones: 9+7=16. Write 6, carry 1 ten.",
             "Tens: 6+5+1=12. Write 2, carry 1 hundred.",
             "Hundreds: 3+2+1=6.",
             "Answer 626."],
            vid="g2u2-c4-steps",
        ),
        kid_tip("One place at a time", "Do not add all the digits in a jumble. Finish ones. Then tens. Then hundreds."),
        16,
    )

    c5 = concept_block(
        "5. Add three numbers",
        [
            "Sometimes you add three two-digit numbers: 25 + 18 + 32.",
            "Add two of them first. Then add the third.",
            "Look for a ten: 8 and 2 make 10, so 18 + 32 is easy: 50, then +25 = 75.",
            "You can stack all three and add the ones column, then the tens column. Regroup the same way.",
            "Ones might make 20 or more. Then you carry 2 tens, not just 1.",
            "Check by adding in a different order. The sum should match.",
        ],
        lesson_figure(
            svg_tape([16, 27, 14], ["16", "27", "14"]),
            "16 + 27 + 14",
            "Pair 16 and 14 to make 30, then add 27. The three parts total 57.",
        )
        + solved(1, "16 + 27 + 14 = ?",
               ["16 + 14 = 30 (nice tens).",
                "30 + 27 = 57."],
               "57")
        + solved(2, "40 + 25 + 25 = ?",
                 ["25 + 25 = 50.",
                  "50 + 40 = 90."],
                 "90")
        + matching(
            [("10 + 20 + 30", "60"), ("15 + 15 + 15", "45"),
             ("22 + 22 + 11", "55"), ("9 + 9 + 9", "27")],
            vid="g2u2-c5-match",
        ),
        try_this("Friendly pairs", "Hunt for numbers that make 10 or 100. Add those first. The leftover is easier."),
        21,
    )

    c6 = concept_block(
        "6. Addition stories",
        [
            "A story that puts groups together is addition.",
            "Words like more, in all, together, total, and both often mean add.",
            "Write a number sentence: 28 + 17 = ?",
            "Then solve with regrouping if you need to.",
            "Label the answer: 45 crayons, not just 45. The label tells what you counted.",
            "If the story only adds once, it is a one-step story. Two-step stories come in Unit 4.",
        ],
        lesson_figure(
            svg_tape([46, 38], ["46 books", "38 books"]),
            "46 books and 38 more",
            "Together means add. Ones 6+8=14, so write 4 and carry 1 ten. 46 + 38 = 84 books.",
        )
        + solved(1, "A shelf has 46 books. You add 38 books. How many books now?",
               ["Together means add: 46 + 38.",
                "Ones: 6+8=14. Write 4, carry 1.",
                "Tens: 4+3+1=8. Answer 84 books."],
               "84")
        + solved(2, "Camp has 125 tents. 87 more tents arrive. How many tents?",
                 ["125 + 87.",
                  "Ones 5+7=12. Tens 2+8+1=11. Hundreds 1+1=2.",
                  "212 tents."],
                 "212")
        + watch_out("Adding the wrong thing",
                    "Read who has what. Add the two amounts that join. Do not add a leftover number from the next sentence."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Add two-digit numbers in columns",
            "Regroup 10 ones as 1 ten",
            "Add two-digit numbers that need regrouping",
            "Add three-digit numbers",
            "Add three numbers",
            "Solve one-step addition stories",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u2_questions()


# ===========================================================================
# UNIT 3: Subtraction with regrouping (borrowing)
# ===========================================================================

def _u3_questions():
    qs = []
    idx = 1

    for a, b in [(48, 13), (76, 40), (59, 22), (80, 30), (65, 14)]:
        qs.append(mq(f"{a} − {b} = ?", a - b, f"Subtract ones, then tens. {a} − {b} = {a - b}.", idx))
        idx += 1

    for a, b in [(52, 18), (71, 26), (40, 17), (63, 29), (85, 47)]:
        qs.append(mq(
            f"{a} − {b} = ? (you will regroup / borrow)",
            a - b,
            f"Ones in {a} are too small. Borrow 1 ten. Then subtract. {a} − {b} = {a - b}.",
            idx,
        ))
        idx += 1

    for a, b in [(91, 38), (60, 24), (73, 45), (82, 57), (54, 19)]:
        qs.append(mq(f"{a} − {b} = ?", a - b, f"Borrow a ten if ones need it. {a} − {b} = {a - b}.", idx))
        idx += 1

    for a, b in [(486, 152), (750, 230), (908, 104), (635, 412), (399, 120)]:
        qs.append(mq(f"{a} − {b} = ?", a - b, f"Subtract each place. {a} − {b} = {a - b}.", idx))
        idx += 1

    for a, b in [(400, 175), (500, 268), (300, 142), (200, 87), (600, 359)]:
        qs.append(mq(
            f"{a} − {b} = ? (watch the zeros)",
            a - b,
            f"You may need to borrow across a zero. {a} − {b} = {a - b}.",
            idx,
        ))
        idx += 1

    for a, b in [(523, 147), (641, 258), (812, 369), (734, 186), (905, 278)]:
        qs.append(mq(f"{a} − {b} = ?", a - b, f"Regroup tens and hundreds as needed. {a} − {b} = {a - b}.", idx))
        idx += 1

    stories = [
        ("72 balloons. 28 pop. How many balloons are left?", 44, "72 − 28 = 44. Borrow 1 ten so 12 − 8 = 4 ones."),
        ("A library has 415 books. Kids check out 138. How many books stay?", 277, "415 − 138 = 277."),
        ("You have 90 cents. You spend 47 cents. How many cents left?", 43, "90 − 47 = 43."),
        ("500 stickers. You give away 175. How many stickers left?", 325, "500 − 175 = 325."),
        ("There are 264 kids. 89 go to lunch. How many kids are still in class?", 175, "264 − 89 = 175."),
    ]
    for text, ans, expl in stories:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    checks = [
        ("Does 45 + 28 = 73 check 73 − 28 = 45?", "yes", "Addition undoes subtraction. 45 + 28 = 73, so the minus is right.", ["no", "maybe", "73"]),
        ("You got 52 − 19 = 33. Check: 33 + 19 = ?", 52, "33 + 19 = 52. The subtraction checks out.", None),
        ("You got 80 − 25 = 65. Check: 65 + 25 = ?", 90, "65 + 25 = 90, not 80. The minus answer was wrong.", None),
    ]
    for text, ans, expl, dist in checks:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"{80 + i} − {12 + (i % 8)} = ?",
        80 + i - (12 + (i % 8)),
        f"Subtract. The difference is {80 + i - (12 + (i % 8))}.",
        i,
    ))


def build_unit3():
    title = "Second Grade Math Unit 3: Subtraction with Regrouping"
    description = (
        "Subtract two-digit and three-digit numbers. Borrow a ten or a hundred when a place is too small."
    )

    c1 = concept_block(
        "1. Subtract without regrouping",
        [
            "Line up ones under ones and tens under tens.",
            "Subtract ones first. Then tens. Then hundreds if you have them.",
            "If every top digit is big enough, you do not borrow. 86 − 42: 6−2=4, 8−4=4. Difference 44.",
            "Zero on top in ones is fine if you do not need to subtract more than 0… but 50 − 3 needs regrouping. We get to that next.",
            "Minus means take away, find the difference, or how many more.",
            "Check by adding the answer to the number you subtracted. You should get back to the start.",
        ],
        lesson_figure(
            svg_base10(5, 7),
            "57 take away 23",
            "5 tens and 7 ones. Remove 2 tens and 3 ones. Ones 7−3=4, tens 5−2=3. Difference 34.",
        )
        + solved(1, "57 − 23 = ?",
               ["Ones: 7 − 3 = 4.",
                "Tens: 5 − 2 = 3.",
                "34."],
               "34")
        + solved(2, "90 − 40 = ?",
                 ["Ones: 0 − 0 = 0.",
                  "Tens: 9 − 4 = 5.",
                  "50."],
                 "50")
        + matching(
            [("48 − 15", "33"), ("76 − 30", "46"), ("59 − 21", "38"), ("88 − 44", "44")],
            vid="g2u3-c1-match",
        ),
        kid_tip("Check with plus", "After 57 − 23 = 34, add 34 + 23. If you get 57, you are right.")
        + phet_box("arith"),
        1,
    )

    c2 = concept_block(
        "2. Borrow a ten (regroup)",
        [
            "If the ones on top are smaller than the ones you subtract, you cannot take them yet.",
            "Borrow 1 ten from the tens place. That ten becomes 10 ones. Add them to the ones you already have.",
            "Example: 52 − 18. Top ones are 2. You need 8. Borrow: tens become 4, ones become 12. Then 12 − 8 = 4. Tens: 4 − 1 = 3. Answer 34.",
            "People also say regrouping or unbundling a ten. Same move.",
            "Cross out the old tens digit. Write the new tens digit. Write the new ones as a two-digit number like 12.",
            "Never skip crossing out. It keeps the new amounts clear.",
        ],
        lesson_figure(
            svg_ten_frame(11),
            "Borrow to make 11 ones",
            "71 has only 1 one, less than 6. Borrow a ten: ones become 11, tens become 6. Then 11−6=5 and 6−2=4, so 45.",
        )
        + solved(1, "71 − 26 = ?",
               ["Ones: 1 is less than 6. Borrow 1 ten. Ones become 11. Tens become 6.",
                "11 − 6 = 5. Tens: 6 − 2 = 4.",
                "45."],
               "45")
        + step_reveal(
            ["Look at 40 − 17.",
             "Ones: 0 is less than 7. Borrow 1 ten from 4 tens.",
             "Tens become 3. Ones become 10.",
             "10 − 7 = 3. Tens: 3 − 1 = 2.",
             "Answer 23."],
            prompt="After you borrow, how many ones do you have?",
            vid="g2u3-c2-steps",
            answer="10",
        ),
        watch_out("Borrowing but not giving the ones",
                  "If you change 5 tens to 4 tens but forget to make ones into 12, the ones subtract will be wrong."),
        6,
    )

    c3 = concept_block(
        "3. Two-digit subtraction with regrouping",
        [
            "Practice borrowing until your pencil knows the path.",
            "Ask: are top ones enough? If yes, subtract. If no, borrow first.",
            "After borrowing, subtract ones, then subtract tens.",
            "Stories: left, remain, how many more, difference — often minus.",
            "Estimate: 81 − 39 is near 80 − 40 = 40. Exact should be close to 40.",
            "If your answer is bigger than the starting number, you added by mistake.",
        ],
        lesson_figure(
            svg_tape([34, 29], ["34 left", "29"]),
            "63 − 29",
            "3 ones are not enough, so borrow. Ones 13−9=4, tens 5−2=3. Difference 34.",
        )
        + solved(1, "63 − 29 = ?",
               ["3 < 9, so borrow. Ones 13 − 9 = 4. Tens 5 − 2 = 3.",
                "34."],
               "34")
        + solved(2, "85 − 47 = ?",
                 ["5 < 7, borrow. Ones 15 − 7 = 8. Tens 7 − 4 = 3.",
                  "38."],
                 "38")
        + matching(
            [("51 − 18", "33"), ("70 − 26", "44"), ("92 − 35", "57"), ("44 − 19", "25")],
            vid="g2u3-c3-match",
        ),
        try_this("Count up instead", "For 63 − 29, count up from 29 to 63: +1 to 30, +33 to 63. Total added 34. Same answer."),
        11,
    )

    c4 = concept_block(
        "4. Three-digit subtraction",
        [
            "Same borrowing, more places.",
            "Start at ones. If you cannot subtract, borrow from tens. If tens are 0, you may need to borrow from hundreds first.",
            "Example: 523 − 147. Ones 3 < 7, borrow from 2 tens → 13 − 7 = 6, tens now 1. Tens 1 < 4, borrow from hundreds → 11 − 4 = 7, hundreds 4 − 1 = 3. Answer 376.",
            "Keep the crossing-outs neat. Messy marks hide a leftover ten.",
            "Check with addition: 376 + 147 should return 523.",
            "Line up hundreds carefully. A drifted 5 becomes a wrong place.",
        ],
        lesson_figure(
            svg_tape([383, 258], ["383 left", "258"]),
            "641 split as 383 and 258",
            "Borrow from tens, then from hundreds. 641 − 258 = 383.",
        )
        + solved(1, "641 − 258 = ?",
               ["Ones: 1 < 8, borrow. 11 − 8 = 3. Tens now 3.",
                "Tens: 3 < 5, borrow from 6 hundreds. 13 − 5 = 8. Hundreds 5 − 2 = 3.",
                "383."],
               "383")
        + solved(2, "812 − 369 = ?",
                 ["Ones: 2 < 9 → 12 − 9 = 3, tens 0.",
                  "Tens: 0 < 6, borrow from 8. 10 − 6 = 4, hundreds 7 − 3 = 4.",
                  "443."],
                 "443")
        + step_reveal(
            ["Write 734 − 186.",
             "Ones need a borrow: 14 − 6 = 8. Tens now 2.",
             "Tens need a borrow: 12 − 8 = 4. Hundreds now 6.",
             "Hundreds: 6 − 1 = 5.",
             "Difference 548."],
            vid="g2u3-c4-steps",
        ),
        kid_tip("Start small", "Always begin at the ones place, even with huge numbers."),
        16,
    )

    c5 = concept_block(
        "5. Subtract across zeros",
        [
            "Zeros on top are the trickiest. You cannot borrow from 0 tens until that 0 gets tens from hundreds.",
            "Look at 400 − 175. Hundreds 4, tens 0, ones 0.",
            "Borrow from hundreds: 4 hundreds become 3 hundreds, and the tens become 10 tens. Then borrow 1 of those tens for the ones: tens 9, ones 10.",
            "Now subtract: 10 − 5 = 5 ones, 9 − 7 = 2 tens, 3 − 1 = 2 hundreds. Answer 225.",
            "Think: you unbundle 1 hundred into 10 tens, then unbundle 1 ten into 10 ones.",
            "Write every new digit. Do not try to hold three new numbers only in your head.",
        ],
        lesson_figure(
            svg_tape([232, 268], ["232", "268"]),
            "500 as 232 and 268",
            "Unbundle 1 hundred into 10 tens, then 1 ten into 10 ones. Then 500 − 268 = 232.",
        )
        + solved(1, "500 − 268 = ?",
               ["Borrow across zeros: hundreds 4, tens 9, ones 10.",
                "10 − 8 = 2. 9 − 6 = 3. 4 − 2 = 2.",
                "232."],
               "232")
        + solved(2, "300 − 142 = ?",
                 ["Hundreds 2, tens 9, ones 10.",
                  "10 − 2 = 8. 9 − 4 = 5. 2 − 1 = 1.",
                  "158."],
                 "158")
        + watch_out("Stopping after one borrow",
                    "If the tens are 0, one borrow is not enough. The hundred must feed the tens, then a ten must feed the ones."),
        21,
    )

    c6 = concept_block(
        "6. Subtraction stories and checks",
        [
            "Stories that take away, compare, or find how many left use minus.",
            "Write the bigger amount first (the whole), then subtract the part.",
            "How many more also means difference: 90 − 47.",
            "After you subtract, add to check. If the check fails, look at your borrows.",
            "A check that is 10 or 100 off often means a forgotten regroup.",
            "Label the answer with the thing in the story: balloons, books, cents.",
        ],
        lesson_figure(
            svg_balance("175 + 89", "264"),
            "Check 264 − 89",
            "89 fish move, so 264 − 89 = 175 stay. Add to check: 175 + 89 balances 264.",
        )
        + solved(1, "A tank holds 264 fish. 89 fish are moved. How many fish stay?",
               ["Stay means take away: 264 − 89.",
                "Borrow as needed. 264 − 89 = 175.",
                "Check: 175 + 89 = 264."],
               "175")
        + matching(
            [("72 − 28 checks with", "44 + 28 = 72"), ("90 − 47 checks with", "43 + 47 = 90"),
             ("500 − 175 checks with", "325 + 175 = 500"), ("40 − 17 checks with", "23 + 17 = 40")],
            vid="g2u3-c6-match",
        ),
        try_this("Circle the whole", "In a story, circle the starting amount. Underline what leaves. The leftover is the answer."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Subtract when every top digit is big enough",
            "Borrow a ten for the ones",
            "Subtract two-digit numbers with regrouping",
            "Subtract three-digit numbers",
            "Subtract across zeros",
            "Check subtraction with addition",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u3_questions()


# ===========================================================================
# UNIT 4: Two-step word problems
# ===========================================================================

def _u4_questions():
    qs = []
    idx = 1

    two_step = [
        ("Sam has 12 apples. He buys 9 more, then eats 4. How many apples now?", 17, "12 + 9 = 21. Then 21 − 4 = 17."),
        ("Mia has 20 stickers. She gives 6 away, then gets 8 more. How many stickers?", 22, "20 − 6 = 14. Then 14 + 8 = 22."),
        ("A box has 35 crayons. You add 18, then take out 10. How many crayons?", 43, "35 + 18 = 53. Then 53 − 10 = 43."),
        ("There are 40 kids. 15 leave. Then 9 more leave. How many kids stay?", 16, "40 − 15 = 25. Then 25 − 9 = 16."),
        ("You save 25 cents, then 30 cents, then spend 10 cents. How many cents left?", 45, "25 + 30 = 55. Then 55 − 10 = 45."),
        ("A shelf has 50 books. You add 24. Then 12 are borrowed. How many books on the shelf?", 62, "50 + 24 = 74. 74 − 12 = 62."),
        ("Liam has 18 marbles. He wins 7, then loses 5. How many marbles?", 20, "18 + 7 = 25. 25 − 5 = 20."),
        ("A team scores 14 points, then 9, then the other team takes 6 away from the board. Points left?", 17, "14 + 9 = 23. 23 − 6 = 17."),
        ("You bake 36 cookies. You give 12 to a friend and 8 to a neighbor. How many cookies left?", 16, "12 + 8 = 20 given away. 36 − 20 = 16."),
        ("There are 28 birds. 11 fly away. 6 come back. How many birds now?", 23, "28 − 11 = 17. 17 + 6 = 23."),
        ("A jar has 100 beads. You add 45. Then you use 20. How many beads left?", 125, "100 + 45 = 145. 145 − 20 = 125."),
        ("Nia has 15 red buttons and 17 blue. She uses 9 buttons. How many buttons left?", 23, "15 + 17 = 32. 32 − 9 = 23."),
        ("A bus has 40 seats. 18 kids sit, then 13 more sit. How many seats are empty?", 9, "18 + 13 = 31 sitting. 40 − 31 = 9 empty."),
        ("You have 70 pages to read. You read 25, then 30. How many pages left?", 15, "25 + 30 = 55 read. 70 − 55 = 15 left."),
        ("A store had 80 toys. It sold 24 in the morning and 19 in the afternoon. How many toys left?", 37, "24 + 19 = 43 sold. 80 − 43 = 37."),
    ]
    for text, ans, expl in two_step:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    choose_ops = [
        ("First you put groups together, then some leave. Which pair of operations?", "add then subtract",
         "Together is plus. Leave is minus.", ["subtract then add", "add then add", "subtract then subtract"]),
        ("Some leave, then more arrive. Which pair?", "subtract then add",
         "Leave first, then add the new group.", ["add then subtract", "add then add", "multiply then add"]),
        ("Two groups join, then another group joins. Which pair?", "add then add",
         "Both steps put amounts together.", ["add then subtract", "subtract then subtract", "subtract then add"]),
        ("A starting amount, two groups leave one after another. Which pair?", "subtract then subtract",
         "Take away, then take away again.", ["add then add", "add then subtract", "subtract then add"]),
        ("You find how many in all, then how many are left after using some. First step is usually…", "add",
         "In all means add the parts first.", ["subtract", "skip", "match"]),
    ]
    for text, ans, expl, dist in choose_ops:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    missing_step = [
        ("12 + 9 = 21. Then 21 − 4. What is the final answer?", 17, "Second step: 21 − 4 = 17."),
        ("20 − 6 = 14. Then 14 + 8. What is the final answer?", 22, "14 + 8 = 22."),
        ("35 + 18 = 53. Then 53 − 10. Final?", 43, "53 − 10 = 43."),
        ("40 − 15 = 25. Then 25 − 9. Final?", 16, "25 − 9 = 16."),
        ("25 + 30 = 55. Then 55 − 10. Final?", 45, "55 − 10 = 45."),
    ]
    for text, ans, expl in missing_step:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    bar = [
        ("A bar shows 30 in all. One part is 12. The other part is the rest. Then 5 more join the rest. Rest at first?", 18,
         "30 − 12 = 18 for the other part.", None),
        ("Whole 50. Two equal parts leave: 10 and 10. What is left in the whole?", 30,
         "10 + 10 = 20 leave. 50 − 20 = 30.", None),
        ("Parts 14 and 9 make a whole. Then 6 leave the whole. What is the whole first?", 23,
         "14 + 9 = 23.", None),
        ("You need two steps. Step 1 answer is 21. Step 2 is minus 4. Final?", 17, "21 − 4 = 17.", None),
        ("Step 1 is 18 + 13. Step 2 is 40 minus that sum. Empty seats?", 9, "18+13=31. 40−31=9.", None),
    ]
    for text, ans, expl, dist in bar:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    more = [
        (16, 9, 5, "add-sub"),
        (30, 11, 8, "sub-add"),
        (22, 22, 10, "add-sub"),
        (45, 20, 7, "sub-sub"),
        (13, 13, 13, "add-add"),
        (60, 15, 15, "sub-sub"),
        (100, 25, 10, "add-sub"),
        (8, 7, 6, "add-add"),
    ]
    for a, b, c, kind in more:
        if kind == "add-sub":
            qs.append(mq(
                f"You have {a}. You get {b} more, then give away {c}. How many now?",
                a + b - c,
                f"{a} + {b} = {a + b}. Then {a + b} − {c} = {a + b - c}.",
                idx,
            ))
        elif kind == "sub-add":
            qs.append(mq(
                f"You have {a}. {b} leave, then {c} come back. How many now?",
                a - b + c,
                f"{a} − {b} = {a - b}. Then {a - b} + {c} = {a - b + c}.",
                idx,
            ))
        elif kind == "sub-sub":
            qs.append(mq(
                f"You have {a}. First {b} leave, then {c} more leave. How many left?",
                a - b - c,
                f"{a} − {b} = {a - b}. Then {a - b} − {c} = {a - b - c}.",
                idx,
            ))
        else:
            qs.append(mq(
                f"A pile has {a}, then {b} more, then {c} more. How many in all?",
                a + b + c,
                f"{a} + {b} + {c} = {a + b + c}.",
                idx,
            ))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"Start with {20 + i}. Add {5 + (i % 6)}, then subtract 3. How many?",
        20 + i + 5 + (i % 6) - 3,
        f"First add, then subtract 3. Land on {20 + i + 5 + (i % 6) - 3}.",
        i,
    ))


def build_unit4():
    title = "Second Grade Math Unit 4: Two-Step Word Problems"
    description = (
        "Solve stories that need two operations: add then subtract, subtract then add, or two of the same."
    )

    c1 = concept_block(
        "1. What is a two-step story?",
        [
            "A one-step story needs one plus or one minus. A two-step story needs two moves.",
            "You do the first move. That makes a new number. Then you use that number in the second move.",
            "Clue: the story has two actions. Buys more AND then eats some. Leaves AND then more leave.",
            "Do not jump to the end. Write step 1, then step 2.",
            "A tape or bar drawing helps. Show the first change, then the second.",
            "If you only do one step, your answer is usually too big or too small.",
        ],
        lesson_figure(
            svg_tape([12, 9], ["12 apples", "buys 9"]),
            "Sam buys 9 more apples",
            "First join 12 and 9 to make 21. Then 4 are eaten, so 21 − 4 = 17 apples left.",
        )
        + solved(1, "Sam has 12 apples. He buys 9 more, then eats 4. How many apples now?",
               ["Step 1: 12 + 9 = 21 apples after buying.",
                "Step 2: 21 − 4 = 17 after eating.",
                "He has 17 apples."],
               "17")
        + step_reveal(
            ["Underline the two actions.",
             "Decide plus or minus for action 1. Solve it.",
             "Use that answer as the start of action 2.",
             "Solve action 2. Label the answer."],
            vid="g2u4-c1-steps",
        ),
        kid_tip("Two sentences, two steps", "If two things happen, you probably need two number sentences."),
        1,
    )

    c2 = concept_block(
        "2. Add, then subtract",
        [
            "A common pattern: more things arrive, then some go away.",
            "Put together first. Then take away.",
            "Example: 35 crayons, add 18, take out 10. 35+18=53. 53−10=43.",
            "The middle number (53) is not the final answer. Keep going.",
            "Check: does the story end with less than the middle amount? Then step 2 was minus.",
            "Write both sentences: 35 + 18 = 53 and 53 − 10 = 43.",
        ],
        lesson_figure(
            svg_tape([50, 24], ["50 books", "add 24"]),
            "Add 24 books, then borrow 12",
            "50 + 24 = 74 on the shelf. Then 12 are borrowed: 74 − 12 = 62 remain.",
        )
        + solved(1, "A shelf has 50 books. You add 24. Then 12 are borrowed. How many books remain?",
               ["50 + 24 = 74 on the shelf.",
                "74 − 12 = 62 after borrowing.",
                "62 books."],
               "62")
        + solved(2, "You have 16 cards. You get 9 more, then give away 5. How many cards?",
                 ["16 + 9 = 25.",
                  "25 − 5 = 20."],
                 "20")
        + matching(
            [("get more, then give some", "add then subtract"),
             ("12 + 9, then minus 4", "17"),
             ("middle number 21, minus 4", "17"),
             ("final is after both steps", "do not stop at step 1")],
            vid="g2u4-c2-match",
        ),
        watch_out("Stopping after the plus",
                  "The number after the first add is a stepping stone. The story is not done yet."),
        6,
    )

    c3 = concept_block(
        "3. Subtract, then add",
        [
            "The other common pattern: some leave, then more arrive.",
            "Take away first. Then put the new group with what is left.",
            "Example: 20 stickers, give 6 away, get 8 more. 20−6=14. 14+8=22.",
            "You do not add 6 and 8 to 20. The 6 left. Only the 8 joined later.",
            "Order in the story is the order of the math.",
            "If you mix the order, you tell a different story.",
        ],
        lesson_figure(
            svg_tape([17, 11], ["17 still sit", "11 flew"]),
            "28 birds, then 11 fly away",
            "First 28 − 11 = 17. Then 6 come back: 17 + 6 = 23 birds.",
        )
        + solved(1, "28 birds sit. 11 fly away. 6 come back. How many birds now?",
               ["28 − 11 = 17 after they fly.",
                "17 + 6 = 23 after some return.",
                "23 birds."],
               "23")
        + solved(2, "Mia has 30 beads. She uses 11, then finds 8 more. How many beads?",
                 ["30 − 11 = 19.",
                  "19 + 8 = 27."],
                 "27")
        + try_this("Act it out", "Use counters. Take some away. Then add some. The pile at the end is the answer."),
        11,
    )

    c4 = concept_block(
        "4. Two adds, or two subtracts",
        [
            "Sometimes both steps are plus: 15 red and 17 blue, then 9 green. That is three groups. Add twice.",
            "Sometimes both steps are minus: 80 toys, sell 24, then sell 19. Take away twice.",
            "You can add the two leaving groups first, then subtract once: 24+19=43 sold, 80−43=37 left. Still two steps.",
            "Choose the path that feels clear. Both paths should match.",
            "Empty seats: fill some, fill more, then subtract from the total seats.",
            "Pages left: add pages already read, subtract that from the book length.",
        ],
        lesson_figure(
            svg_tape([12, 8, 16], ["12 friend", "8 neighbor", "16 left"]),
            "36 cookies given away",
            "12 + 8 = 20 given away. Then 36 − 20 = 16 cookies left.",
        )
        + solved(1, "You bake 36 cookies. Give 12 to a friend and 8 to a neighbor. How many left?",
               ["12 + 8 = 20 given away.",
                "36 − 20 = 16 left.",
                "Or 36 − 12 = 24, then 24 − 8 = 16. Same."],
               "16")
        + solved(2, "A bus has 40 seats. 18 kids sit, then 13 more sit. How many seats are empty?",
                 ["18 + 13 = 31 sitting.",
                  "40 − 31 = 9 empty."],
                 "9")
        + matching(
            [("two groups leave", "subtract twice, or add the leaving then subtract"),
             ("three groups join", "add twice"),
             ("empty seats", "add sitters, subtract from seats"),
             ("pages left", "add pages read, subtract from total")],
            vid="g2u4-c4-match",
        ),
        kid_tip("Same answer, two paths", "36 − 12 − 8 and 36 − (12 + 8) are friends. Pick one and stick with it."),
        16,
    )

    c5 = concept_block(
        "5. Draw a bar to plan",
        [
            "A bar (tape) is a long rectangle that stands for the whole.",
            "Split the bar into parts. Label the parts you know. The empty part is a question mark.",
            "For two steps, you may draw two bars, or change the bar after step 1.",
            "Example: 15 red + 17 blue is a whole of 32. Then 9 used: cut 9 off the 32 bar. 23 left.",
            "Drawing slows you down in a good way. You see plus vs minus.",
            "If you cannot draw the story, read it again. Find the whole.",
        ],
        lesson_figure(
            svg_tape([15, 17], ["15 red", "17 blue"]),
            "Bar for 15 and 17 buttons",
            "The bar shows 15 + 17 = 32 buttons in all. Then 9 are used, so 32 − 9 = 23 left.",
        )
        + solved(1, "Nia has 15 red buttons and 17 blue. She uses 9. How many buttons left?",
               ["Bar 1: 15 + 17 = 32 buttons in all.",
                "Bar 2: 32 with 9 used. 32 − 9 = 23 left."],
               "23")
        + step_reveal(
            ["Draw a bar for the first whole or first change.",
             "Write the step 1 number.",
             "Draw how step 2 changes that bar.",
             "Write the step 2 number. That is the answer."],
            vid="g2u4-c5-steps",
        ),
        try_this("Question mark last", "The ? goes on the amount the story asks for, not on a leftover fact."),
        21,
    )

    c6 = concept_block(
        "6. Choose the operations",
        [
            "Before you compute, name the two operations: add then subtract, and so on.",
            "Together, more, in all → plus. Left, give away, fly away, spend → minus.",
            "Then → often starts the second step.",
            "If the story asks how many empty, you will subtract from a total after you add the used parts.",
            "Check reasonableness: can you have more cookies left than you baked? No. Then a step is wrong.",
            "Read the question sentence last. It tells you which number to report.",
        ],
        lesson_figure(
            svg_tape([25, 30], ["25 pages", "30 pages"]),
            "Pages already read",
            "Add the pages read: 25 + 30 = 55. Then 70 − 55 = 15 pages left.",
        )
        + solved(1, "You have 70 pages. You read 25, then 30. How many pages left?",
               ["Operations: add the pages read, then subtract from 70.",
                "25 + 30 = 55 read.",
                "70 − 55 = 15 left."],
               "15")
        + watch_out("Using every number once in a jumble",
                    "Do not add all numbers just because they are there. 70 + 25 + 30 would be a different story."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Spot a story that needs two moves",
            "Add, then subtract",
            "Subtract, then add",
            "Add twice or subtract twice",
            "Plan with a bar drawing",
            "Name the operations before you compute",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u4_questions()
