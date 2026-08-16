"""First Grade Math units 1–4: counting, place value, addition, subtraction."""

from __future__ import annotations

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
    make_question,
    renumber,
)


def _fill(qs, need, factory):
    while len(qs) < need:
        qs.append(factory(len(qs) + 1))
    return renumber(qs[:need])


# ===========================================================================
# UNIT 1: Counting to 120
# ===========================================================================

def _u1_questions():
    qs = []
    idx = 1

    for text, ans, expl, dist in [
        ("Count the stars: ⭐⭐⭐⭐⭐  How many stars?", 5,
         "Point to each star. Say 1, 2, 3, 4, 5. There are 5 stars.", None),
        ("What number comes after 7?", 8,
         "After 7 we say 8. Count: 6, 7, 8.", None),
        ("What number comes before 10?", 9,
         "The number just before 10 is 9. Count: 8, 9, 10.", None),
        ("Count the apples: 🍎🍎🍎  How many apples?", 3,
         "Three apples. 1, 2, 3.", None),
        ("Which number is bigger: 4 or 9?", 9,
         "9 is more than 4. Nine is farther along when we count.", ["4", "0", "1"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, expl in [
        ("What number comes after 19?", 20, "After 19 we go to 20. That is two tens."),
        ("What number comes after 29?", 30, "After 29 comes 30. We start a new ten."),
        ("Count by ones: 48, 49, ___. What is next?", 50, "48, 49, 50. Fifty comes after 49."),
        ("What number comes before 100?", 99, "99 is one less than 100. Ninety-nine."),
        ("Which is more: 40 or 14?", 40, "40 has 4 tens. 14 has 1 ten. 40 is more."),
    ]:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    for text, ans, expl in [
        ("What number comes after 109?", 110, "109, then 110. One hundred ten."),
        ("What number comes after 119?", 120, "119, then 120. We made it to 120!"),
        ("Count: 97, 98, 99, ___. What is next?", 100, "After 99 we say 100. One hundred."),
        ("What number comes before 120?", 119, "One less than 120 is 119."),
        ("Which is more: 112 or 102?", 112, "112 has 11 tens and 2 ones. 102 has 10 tens. 112 is more."),
    ]:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    for text, ans, expl in [
        ("Start at 6. Count on 3 more. What number do you land on?", 9,
         "Start at 6. Then 7, 8, 9. You land on 9."),
        ("Start at 15. Count on 2 more. Where do you land?", 17,
         "15, then 16, 17."),
        ("There are 8 cookies. You get 1 more. How many now?", 9,
         "Count on from 8: 9. Eight and one more is nine."),
        ("Start at 27. Count on 3. What number?", 30,
         "27, 28, 29, 30."),
        ("A box has 11 crayons. You add 4. How many crayons?", 15,
         "Count on from 11: 12, 13, 14, 15."),
    ]:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    for text, ans, expl in [
        ("Count by tens: 10, 20, 30, ___. What is next?", 40, "Tens: 10, 20, 30, 40."),
        ("Count by tens: 50, 60, 70, ___. What is next?", 80, "50, 60, 70, 80."),
        ("How many tens are in 40?", 4, "40 is 4 tens. 10 + 10 + 10 + 10 = 40."),
        ("Start at 20. Jump 10 more. Where do you land?", 30, "20 and 10 more is 30."),
        ("Count by tens from 0. What is the 6th number? (0, 10, 20…)", 50,
         "0, 10, 20, 30, 40, 50. The sixth jump lands on 50."),
    ]:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    for text, ans, expl, dist in [
        ("How do you write the number twelve?", 12,
         "Twelve is 1 ten and 2 ones. We write 12.", ["21", "20", "2"]),
        ("How do you write the number twenty?", 20,
         "Twenty is 2 tens and 0 ones. We write 20.", ["12", "2", "22"]),
        ("The number 35 is thirty-____.", "five",
         "35 is thirty-five. The ones digit is 5.", ["three", "fifty", "eight"]),
        ("Which number is one hundred five?", 105,
         "One hundred five is 105. A 1 in hundreds, 0 tens, 5 ones.", ["150", "115", "15"]),
        ("Read this number: 118. What do we say?", "one hundred eighteen",
         "118 is one hundred eighteen. 11 tens and 8 ones, or 100 + 18.",
         ["one hundred eighty", "eighty-one", "one hundred eight"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    afters = [4, 8, 11, 16, 22, 33, 44, 55, 66, 77, 88, 99, 101, 110, 118]
    for n in afters:
        qs.append(mq(
            f"What number comes after {n}?",
            n + 1,
            f"Count one more: {n}, then {n + 1}.",
            idx,
        ))
        idx += 1

    befores = [6, 10, 15, 21, 30, 50, 80, 100, 111, 120]
    for n in befores:
        qs.append(mq(
            f"What number comes before {n}?",
            n - 1,
            f"One less than {n} is {n - 1}.",
            idx,
        ))
        idx += 1

    tens_more = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    for n in tens_more:
        qs.append(mq(
            f"What is 10 more than {n}?",
            n + 10,
            f"{n} and one more ten is {n + 10}.",
            idx,
        ))
        idx += 1

    compares = [(7, 3), (12, 21), (45, 54), (99, 89), (108, 118), (30, 13), (67, 76), (2, 20)]
    for a, b in compares:
        bigger = max(a, b)
        qs.append(mq(
            f"Which number is bigger: {a} or {b}?",
            bigger,
            f"{bigger} is farther when we count. {a} and {b} — the bigger one is {bigger}.",
            idx,
            distractors=[min(a, b), str(abs(a - b)), "same"],
        ))
        idx += 1

    skip = [10, 20, 30, 40, 50, 60, 70]
    for n in skip:
        qs.append(mq(
            f"Count by tens. What comes after {n}?",
            n + 10,
            f"A ten-jump from {n} lands on {n + 10}.",
            idx,
        ))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"What number comes after {i + 20}?",
        i + 21,
        f"One more than {i + 20} is {i + 21}.",
        i,
    ))


def build_unit1():
    title = "First Grade Math Unit 1: Counting to 120"
    description = (
        "Count to 120, count on from any number, skip-count by tens, and read and write numbers. "
        "Short words, lots of pictures, and five quick checks after each idea."
    )

    c1 = concept_block(
        "1. Count from 1 to 20",
        [
            "We count to know how many. Point to each thing. Say one number for each thing.",
            "Do not skip. Do not count the same thing two times.",
            "The last number you say is how many there are. That is the total.",
            "Numbers in order: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20.",
            "After 10, the teen numbers start: eleven, twelve, thirteen… up to twenty.",
            "Practice every day. Count toys. Count steps. Count snacks.",
        ],
        solved(1, "How many dots? • • • •",
               ["Point to the first dot. Say 1.",
                "Point to the next. Say 2. Then 3. Then 4.",
                "The last number is 4. There are 4 dots."],
               "4", "The last number you say is how many.")
        + solved(2, "What comes after 9?",
                 ["Count: 7, 8, 9…",
                  "The next number is 10.",
                  "10 is one ten."],
                 "10")
        + matching(
            [("1", "one"), ("5", "five"), ("10", "ten"), ("20", "twenty")],
            vid="g1u1-c1-match",
        ),
        kid_tip("Slow and sure", "Touch each thing. Say the number out loud. Slow counting is smart counting.")
        + phet_box("play"),
        1,
    )

    c2 = concept_block(
        "2. Count to 100",
        [
            "After 20 we keep going. 21, 22, 23… all the way to 100.",
            "A hundred chart has 10 rows. Each row has 10 numbers.",
            "When a row ends in 0, like 30 or 40, the next row starts a new ten.",
            "The number 100 is one hundred. It is 10 tens.",
            "If you get stuck, go back ten and count up again.",
            "You can count by ones: 56, 57, 58, 59, 60.",
        ],
        solved(1, "What comes after 49?",
               ["49 is 4 tens and 9 ones.",
                "One more one makes 5 tens and 0 ones.",
                "That number is 50."],
               "50")
        + solved(2, "What comes before 100?",
                 ["Count near the end: 97, 98, 99, 100.",
                  "The number just before 100 is 99."],
                 "99")
        + step_reveal(
            ["Find 40 on a hundred chart.",
             "Move right: 41, 42, 43.",
             "Keep going to the end of the row: 50.",
             "50 starts the next row of tens."],
            prompt="What number do you think comes after 49?",
            vid="g1u1-c2-steps",
            answer="50",
        ),
        try_this("Use a chart", "A hundred chart is a map of numbers. Move right to add 1. Move down to add 10.")
        + phet_box("compare"),
        6,
    )

    c3 = concept_block(
        "3. Count to 120",
        [
            "First grade also counts past 100. We go to 120.",
            "After 100: 101, 102, 103… like counting from 1 again, but we say one hundred first.",
            "111 is one hundred eleven. 120 is one hundred twenty.",
            "Think: 100 and then some more. 100 + 20 = 120.",
            "120 is 12 tens. It is also 100 and 2 tens.",
            "This helps you later with bigger numbers.",
        ],
        solved(1, "What comes after 109?",
               ["Say: one hundred nine.",
                "One more: one hundred ten.",
                "We write 110."],
               "110")
        + solved(2, "What comes after 119?",
                 ["119 is 100 + 19.",
                  "One more is 100 + 20.",
                  "That is 120."],
                 "120", "You made it to 120!")
        + matching(
            [("100", "one hundred"), ("110", "one hundred ten"),
             ("115", "one hundred fifteen"), ("120", "one hundred twenty")],
            vid="g1u1-c3-match",
        ),
        watch_out("Mixing 101 and 110",
                  "101 is one hundred one (a tiny bit more than 100). 110 is one hundred ten (a whole ten more). They look alike. Say them slowly."),
        11,
    )

    c4 = concept_block(
        "4. Count on from any number",
        [
            "You do not always start at 1. You can start in the middle.",
            "If you have 8 and get 2 more, start at 8. Then say 9, 10.",
            "Hold the first number in your head. Count the new things on your fingers.",
            "This is faster than counting all over again from 1.",
            "Count on when you add. Count back when you take away (we learn that later).",
            "Try starting at 14 and counting on 3: 15, 16, 17.",
        ],
        solved(1, "You have 6 stickers. You get 3 more. How many now?",
               ["Keep 6 in your head. Do not start at 1.",
                "Count on: 7, 8, 9.",
                "You land on 9."],
               "9")
        + step_reveal(
            ["See the first pile: 11 blocks.",
             "Do not recount the 11.",
             "Put up 4 fingers for the new blocks.",
             "Count on: 12, 13, 14, 15.",
             "The total is 15."],
            vid="g1u1-c4-steps",
        ),
        kid_tip("Start big", "Start with the bigger number. Count on the smaller number. It is quicker."),
        16,
    )

    c5 = concept_block(
        "5. Skip count by tens",
        [
            "Skip counting by tens is a big jump: 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120.",
            "Each jump is one bundle of ten.",
            "On a hundred chart, a ten-jump is one row down.",
            "If the ones digit stays the same, you added tens. 23, 33, 43 all end with 3.",
            "Skip counting helps you add 10 fast.",
            "Clap on each ten. It makes a beat.",
        ],
        solved(1, "Count by tens: 10, 20, 30, ___. What is next?",
               ["Each jump adds 10.",
                "30 + 10 = 40.",
                "Next is 40."],
               "40")
        + solved(2, "Start at 40. Jump 10 three times. Where do you land?",
                 ["40 + 10 = 50.",
                  "50 + 10 = 60.",
                  "60 + 10 = 70."],
                 "70")
        + matching(
            [("1 ten", "10"), ("3 tens", "30"), ("7 tens", "70"), ("10 tens", "100")],
            vid="g1u1-c5-match",
        ),
        try_this("Fingers are tens", "Each finger can be a ten. 4 fingers = 40. 8 fingers = 80."),
        21,
    )

    c6 = concept_block(
        "6. Read and write numbers",
        [
            "Every number has a name we say and a way we write it.",
            "12 is twelve. 20 is twenty. They swap the digits! Look carefully.",
            "Teen numbers: 13 thirteen, 14 fourteen, 15 fifteen, 16 sixteen, 17 seventeen, 18 eighteen, 19 nineteen.",
            "Tens names: 30 thirty, 40 forty, 50 fifty, 60 sixty, 70 seventy, 80 eighty, 90 ninety.",
            "Two-digit numbers: tens name + ones name. 42 is forty-two.",
            "Past 100 we say one hundred, then the rest: 107 is one hundred seven.",
        ],
        solved(1, "How do we write forty-five?",
               ["Forty means 4 tens.",
                "Five means 5 ones.",
                "Write 45."],
               "45")
        + solved(2, "Read 103.",
                 ["The 1 means one hundred.",
                  "The 0 means no extra tens in the tens place after that hundred.",
                  "The 3 means three ones. Say: one hundred three."],
                 "one hundred three")
        + matching(
            [("12", "twelve"), ("21", "twenty-one"), ("15", "fifteen"), ("50", "fifty")],
            vid="g1u1-c6-match",
        ),
        watch_out("12 and 21",
                  "12 is twelve (1 ten and 2 ones). 21 is twenty-one (2 tens and 1 one). Check which digit is first."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Count from 1 to 20 without skipping",
            "Count to 100 using a hundred chart in your mind",
            "Count to 120 past one hundred",
            "Count on from any number",
            "Skip count by tens to 120",
            "Read and write number names",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u1_questions()


# ===========================================================================
# UNIT 2: Tens and ones
# ===========================================================================

def _u2_questions():
    qs = []
    idx = 1

    for text, ans, expl in [
        ("How many ones make 1 ten?", 10, "Ten ones snap into 1 ten. 10 ones = 1 ten."),
        ("You have 10 ones. How many tens is that?", 1, "10 ones make 1 ten."),
        ("You have 2 tens. How many ones is that?", 20, "2 tens = 20 ones."),
        ("A bundle has 10 sticks. You have 3 bundles. How many sticks?", 30, "3 tens = 30."),
        ("How many ones are left if you make 1 ten from 14 ones?", 4, "10 make a ten. 4 ones are left. 14 = 1 ten and 4 ones."),
    ]:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    for text, ans, expl in [
        ("The number 27 has how many tens?", 2, "27 is 2 tens and 7 ones."),
        ("The number 27 has how many ones?", 7, "The ones digit is 7."),
        ("What number is 4 tens and 1 one?", 41, "4 tens = 40. Plus 1 is 41."),
        ("What number is 6 tens and 0 ones?", 60, "6 tens and no leftover ones is 60."),
        ("58 is 5 tens and ___ ones.", 8, "The ones digit of 58 is 8."),
    ]:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    for text, ans, expl, dist in [
        ("How many tens and ones in 13?", "1 ten and 3 ones",
         "13 is a teen. 1 ten and 3 ones.", ["3 tens and 1 one", "13 ones only", "1 ten and 13 ones"]),
        ("How many tens and ones in 18?", "1 ten and 8 ones",
         "18 = 10 + 8.", ["8 tens and 1 one", "1 ten and 18 ones", "2 tens"]),
        ("11 is 1 ten and ___ ones.", 1, "Eleven is 10 + 1.", None),
        ("What number is 1 ten and 9 ones?", 19, "10 + 9 = 19. Nineteen.", None),
        ("Which is a teen number?", 16, "Teen numbers are 11 to 19.", ["20", "30", "10"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, expl in [
        ("What number is 3 tens and 5 ones?", 35, "30 + 5 = 35."),
        ("What number is 9 tens and 9 ones?", 99, "90 + 9 = 99."),
        ("72 is ___ tens and 2 ones.", 7, "72 has 7 in the tens place."),
        ("What number is 8 tens and 0 ones?", 80, "80 is eight tens."),
        ("40 + 6 = ?", 46, "4 tens and 6 ones make 46."),
    ]:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    for text, ans, expl, dist in [
        ("Which is more: 34 or 43?", 43, "43 has 4 tens. 34 has 3 tens. More tens wins.", ["34", "same", "7"]),
        ("Which is less: 19 or 91?", 19, "19 has 1 ten. 91 has 9 tens. 19 is less.", ["91", "same", "100"]),
        ("Compare 50 and 48. Which is greater?", 50, "50 is 5 tens. 48 is 4 tens and 8 ones. 50 is greater.", ["48", "same", "8"]),
        ("Is 25 equal to 25?", "yes", "Same tens and same ones. They are equal.", ["no", "maybe", "25 is less"]),
        ("Which is greater: 70 or 67?", 70, "7 tens beat 6 tens.", ["67", "same", "3"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, expl in [
        ("What is 10 more than 23?", 33, "Add 1 ten. Tens digit goes 2 → 3. 33."),
        ("What is 10 less than 45?", 35, "Take 1 ten away. 4 tens become 3 tens. 35."),
        ("What is 10 more than 90?", 100, "9 tens plus 1 ten is 10 tens. That is 100."),
        ("What is 10 less than 70?", 60, "7 tens minus 1 ten is 6 tens. 60."),
        ("What is 10 more than 108?", 118, "108 + 10 = 118. The tens digit grew."),
    ]:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    place = [(24, 2, 4), (31, 3, 1), (56, 5, 6), (80, 8, 0), (99, 9, 9),
             (12, 1, 2), (47, 4, 7), (63, 6, 3), (75, 7, 5), (18, 1, 8)]
    for n, t, o in place:
        qs.append(mq(f"How many tens in {n}?", t, f"{n} is {t} tens and {o} ones.", idx))
        idx += 1
        qs.append(mq(f"How many ones in {n}?", o, f"The ones digit of {n} is {o}.", idx))
        idx += 1

    builds = [(2, 8), (5, 0), (7, 3), (4, 4), (9, 1), (3, 9), (6, 6), (1, 7), (8, 2), (0, 9)]
    for t, o in builds:
        n = 10 * t + o
        qs.append(mq(
            f"What number is {t} tens and {o} ones?",
            n,
            f"{t} tens is {10 * t}. Plus {o} ones is {n}.",
            idx,
        ))
        idx += 1

    more10 = [11, 22, 34, 41, 55, 66, 79, 88, 93, 101]
    for n in more10:
        qs.append(mq(f"What is 10 more than {n}?", n + 10, f"{n} + 10 = {n + 10}.", idx))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"What number is 1 ten and {i % 9 + 1} ones?",
        10 + (i % 9 + 1),
        f"1 ten and {i % 9 + 1} ones make {10 + (i % 9 + 1)}.",
        i,
    ))


def build_unit2():
    title = "First Grade Math Unit 2: Tens and Ones"
    description = (
        "Place value for first grade: ten ones make a ten, teen numbers, two-digit numbers, "
        "compare with tens, and 10 more / 10 less."
    )

    c1 = concept_block(
        "1. Ten ones make a ten",
        [
            "Ones are little. Tens are bundles of ten ones.",
            "When you have 10 ones, trade them for 1 ten. They are the same amount.",
            "Think of 10 fingers. Two hands make 1 ten.",
            "A ten-stick is 10 cubes stuck together.",
            "We write tens on the left and ones on the right. In 10, the 1 is the ten.",
            "This idea is the start of place value. Place means where the digit sits.",
        ],
        solved(1, "You have 10 ones. How many tens?",
               ["Count the ones: 10.",
                "10 ones snap into 1 bundle.",
                "That is 1 ten."],
               "1 ten")
        + step_reveal(
            ["Put out 10 cubes.",
             "Line them up.",
             "Snap them into one stick.",
             "Now you have 1 ten and 0 leftover ones.",
             "Write 10."],
            vid="g1u2-c1-steps",
        ),
        kid_tip("Same amount", "1 ten and 10 ones are equal. They look different. They are worth the same.")
        + phet_box("ten"),
        1,
    )

    c2 = concept_block(
        "2. Tens and leftover ones",
        [
            "A two-digit number has tens and ones.",
            "Look at 34. The 3 is tens. The 4 is ones.",
            "3 tens = 30. Plus 4 ones = 34.",
            "If there are 0 ones, like 50, we still write the 0. It holds the ones place.",
            "You can draw sticks for tens and dots for ones.",
            "Always check both places. Do not only look at one digit.",
        ],
        solved(1, "Break apart 26.",
               ["The left digit is 2. That is 2 tens.",
                "2 tens = 20.",
                "The right digit is 6 ones.",
                "20 + 6 = 26."],
               "2 tens and 6 ones")
        + matching(
            [("23", "2 tens 3 ones"), ("40", "4 tens 0 ones"),
             ("17", "1 ten 7 ones"), ("55", "5 tens 5 ones")],
            vid="g1u2-c2-match",
        ),
        try_this("Draw it", "Draw a stick for each ten. Draw a dot for each one. Then count."),
        6,
    )

    c3 = concept_block(
        "3. Teen numbers 11 to 19",
        [
            "Teen numbers are 11, 12, 13, 14, 15, 16, 17, 18, 19.",
            "Each teen is 1 ten and some extra ones.",
            "13 is 1 ten and 3 ones. Not 3 tens!",
            "The word teen sounds like ten. That is a hint.",
            "Eleven and twelve have special names. They are still 1 ten and extra ones.",
            "Teens are the first two-digit numbers you meet.",
        ],
        solved(1, "What is 1 ten and 4 ones?",
               ["1 ten = 10.",
                "4 ones = 4.",
                "10 + 4 = 14. Fourteen."],
               "14")
        + solved(2, "Break apart 19.",
                 ["19 is a teen.",
                  "1 ten and 9 ones.",
                  "10 + 9 = 19."],
                 "1 ten and 9 ones")
        + watch_out("13 vs 30",
                    "13 is thirteen (1 ten, 3 ones). 30 is thirty (3 tens, 0 ones). Listen for teen vs ty."),
        phet_box("play"),
        11,
    )

    c4 = concept_block(
        "4. Numbers to 99 as tens and ones",
        [
            "Any number from 10 to 99 is tens + ones.",
            "47 = 4 tens + 7 ones = 40 + 7.",
            "90 = 9 tens + 0 ones.",
            "You can write 47 as 40 + 7. That is expanded form, in kid words: break-apart form.",
            "When we add later, we add ones with ones and tens with tens.",
            "Practice until you can see 63 and think “six tens and three.”",
        ],
        solved(1, "What number is 7 tens and 2 ones?",
               ["7 tens = 70.",
                "Plus 2 ones.",
                "70 + 2 = 72."],
               "72")
        + matching(
            [("30 + 4", "34"), ("50 + 9", "59"), ("80 + 0", "80"), ("20 + 1", "21")],
            vid="g1u2-c4-match",
        ),
        kid_tip("Left is tens", "The digit on the left is worth more. It is tens. The digit on the right is ones."),
        16,
    )

    c5 = concept_block(
        "5. Compare two-digit numbers",
        [
            "To see which number is bigger, look at tens first.",
            "More tens means a bigger number. 51 beats 49 because 5 tens beat 4 tens.",
            "If tens are the same, look at ones. 38 is more than 32 because 8 ones beat 2 ones.",
            "We can say greater than, less than, or equal.",
            "Equal means the same amount. 25 = 25.",
            "Play with two groups of toys. Which group has more?",
        ],
        solved(1, "Which is greater: 36 or 63?",
               ["36 has 3 tens.",
                "63 has 6 tens.",
                "6 tens is more. 63 is greater."],
               "63")
        + step_reveal(
            ["Write the two numbers.",
             "Look at the tens digits.",
             "If one tens digit is bigger, that number wins.",
             "If tens are the same, look at ones.",
             "If both match, the numbers are equal."],
            vid="g1u2-c5-steps",
        ),
        phet_box("compare"),
        21,
    )

    c6 = concept_block(
        "6. Ten more and ten less",
        [
            "Ten more means add 1 ten. The ones digit stays the same.",
            "23 + 10 = 33. The 2 becomes 3. The 3 ones stay.",
            "Ten less means take away 1 ten. 45 − 10 = 35.",
            "On a hundred chart, ten more is the number under you. Ten less is the number above you.",
            "This is a fast trick. You do not count 10 ones.",
            "Near 100: 95 + 10 = 105. Now you need three digits.",
        ],
        solved(1, "What is 10 more than 48?",
               ["Keep the 8 ones.",
                "Change 4 tens to 5 tens.",
                "48 + 10 = 58."],
               "58")
        + solved(2, "What is 10 less than 70?",
                 ["70 is 7 tens.",
                  "Take away 1 ten. 6 tens left.",
                  "70 − 10 = 60."],
                 "60")
        + try_this("Chart jump", "Move down one row for +10. Move up one row for −10."),
        watch_out("Adding 1 instead of 10",
                  "10 more than 48 is 58, not 49. You add a ten, not a one."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Trade 10 ones for 1 ten",
            "Name tens and leftover ones",
            "Break apart teen numbers",
            "Build numbers to 99",
            "Compare using tens first",
            "Find 10 more and 10 less",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u2_questions()


# ===========================================================================
# UNIT 3: Addition within 20
# ===========================================================================

def _add_fact(a, b, idx, story=None):
    s = a + b
    text = story or f"{a} + {b} = ?"
    expl = f"{a} plus {b} is {s}. You can count on: start at {max(a, b)}, then add {min(a, b)}."
    return mq(text, s, expl, idx)


def _u3_questions():
    qs = []
    idx = 1

    for a, b in [(2, 3), (4, 1), (5, 2), (1, 6), (3, 3)]:
        qs.append(_add_fact(a, b, idx, f"You have {a} 🍎 and get {b} more. How many apples?"))
        idx += 1

    for a, b in [(8, 2), (9, 3), (7, 4), (6, 5), (12, 3)]:
        qs.append(_add_fact(a, b, idx, f"Start at {a}. Count on {b}. Where do you land?"))
        idx += 1

    for a, b in [(9, 4), (8, 5), (7, 6), (9, 7), (8, 3)]:
        qs.append(_add_fact(a, b, idx, f"Make a ten: {a} + {b} = ?"))
        idx += 1

    for n in [4, 5, 6, 7, 8]:
        qs.append(_add_fact(n, n, idx, f"Double {n}. What is {n} + {n}?"))
        idx += 1

    for a, b in [(6, 7), (7, 8), (8, 9), (5, 6), (4, 5)]:
        qs.append(_add_fact(a, b, idx, f"Near double: {a} + {b} = ?"))
        idx += 1

    for a, b, c in [(2, 3, 4), (1, 5, 2), (4, 4, 2), (3, 3, 3), (6, 1, 1)]:
        s = a + b + c
        qs.append(mq(
            f"{a} + {b} + {c} = ?",
            s,
            f"Add two first: {a} + {b} = {a + b}. Then {a + b} + {c} = {s}.",
            idx,
        ))
        idx += 1

    facts = [
        (1, 8), (2, 7), (3, 6), (4, 5), (0, 9), (5, 5), (6, 6), (7, 2), (8, 8), (9, 1),
        (9, 9), (9, 6), (8, 7), (8, 6), (7, 7), (7, 5), (6, 4), (5, 8), (4, 9), (3, 9),
        (2, 9), (1, 9), (10, 5), (10, 8), (11, 4), (12, 5), (13, 2), (14, 3), (15, 4), (16, 3),
        (17, 2), (18, 1), (11, 6), (12, 7), (13, 5), (4, 8), (5, 9), (6, 8), (3, 8), (2, 6),
        (4, 7), (5, 7), (6, 9), (7, 9), (3, 7), (1, 7), (2, 8), (0, 12), (4, 6), (9, 8),
    ]
    for a, b in facts:
        if a + b > 20:
            continue
        qs.append(_add_fact(a, b, idx))
        idx += 1

    return _fill(qs, 55, lambda i: _add_fact(i % 9 + 1, (i % 7) + 1, i))


def build_unit3():
    title = "First Grade Math Unit 3: Addition to 20"
    description = (
        "Add within 20: putting together, counting on, making a ten, doubles, near doubles, "
        "and adding three numbers."
    )

    c1 = concept_block(
        "1. Put together to add",
        [
            "Add means put groups together. Find how many in all.",
            "The plus sign + means and. The equal sign = means is the same as.",
            "3 + 2 = 5. Three and two more make five.",
            "You can add in any order. 3 + 2 is the same as 2 + 3. That is a turn-around fact.",
            "Zero plus a number stays the same. 5 + 0 = 5.",
            "Use toys, fingers, or drawings. Then try it in your head.",
        ],
        solved(1, "4 birds sit. 2 more land. How many birds?",
               ["First group: 4.",
                "Second group: 2.",
                "Put together: 4 + 2 = 6."],
               "6")
        + matching(
            [("2 + 3", "5"), ("4 + 4", "8"), ("1 + 6", "7"), ("5 + 0", "5")],
            vid="g1u3-c1-match",
        ),
        kid_tip("Turn around", "If 8 + 2 is hard, try 2 + 8. Count on from 8. Same answer!")
        + phet_box("pairs"),
        1,
    )

    c2 = concept_block(
        "2. Count on to add",
        [
            "Put the bigger number in your head.",
            "Count on the smaller number with fingers.",
            "For 9 + 3, think 9… then 10, 11, 12.",
            "Do not start at 1. That is slow.",
            "Counting on works great when one number is 1, 2, or 3.",
            "Check by drawing if you want. Then try without the drawing.",
        ],
        solved(1, "8 + 3 = ?",
               ["Bigger number is 8. Hold 8.",
                "Put up 3 fingers.",
                "Count on: 9, 10, 11.",
                "Land on 11."],
               "11")
        + step_reveal(
            ["See 7 + 2.",
             "Hold 7 in your head.",
             "Count on two: 8, 9.",
             "7 + 2 = 9."],
            prompt="What do you think 7 + 2 is?",
            vid="g1u3-c2-steps",
            answer="9",
        ),
        try_this("Bigger first", "Always start with the bigger addend. Counting on is shorter."),
        6,
    )

    c3 = concept_block(
        "3. Make a ten",
        [
            "Ten is a friendly number. We like to make 10, then add the rest.",
            "For 9 + 4, take 1 from the 4 to make 9 into 10. Then 10 + 3 = 13.",
            "For 8 + 5, take 2 from the 5 to make 10. Then 10 + 3 = 13.",
            "This uses place value. You already know tens!",
            "Number pairs that make 10 help: 1+9, 2+8, 3+7, 4+6, 5+5.",
            "Play until those pairs are fast.",
        ],
        solved(1, "8 + 6 = ?",
               ["8 needs 2 more to make 10.",
                "Split 6 into 2 and 4.",
                "8 + 2 = 10. Then 10 + 4 = 14."],
               "14")
        + matching(
            [("9 + 1", "10"), ("7 + 3", "10"), ("6 + 4", "10"), ("5 + 5", "10")],
            vid="g1u3-c3-match",
        ),
        phet_box("ten"),
        11,
    )

    c4 = concept_block(
        "4. Doubles",
        [
            "A double is a number plus itself. 4 + 4, 6 + 6, 8 + 8.",
            "Doubles are easy to remember. They make a pattern: 2, 4, 6, 8, 10, 12, 14, 16, 18, 20.",
            "Think of two hands: 5 + 5 = 10.",
            "Think of two rows of the same number of dots.",
            "If you know doubles, near doubles get easy next.",
            "Say them like a song.",
        ],
        solved(1, "7 + 7 = ?",
               ["This is a double.",
                "7 and 7.",
                "7 + 7 = 14."],
               "14")
        + matching(
            [("3 + 3", "6"), ("5 + 5", "10"), ("8 + 8", "16"), ("10 + 10", "20")],
            vid="g1u3-c4-match",
        ),
        kid_tip("Picture twins", "Doubles are twins. Two same groups. Two same numbers."),
        16,
    )

    c5 = concept_block(
        "5. Near doubles",
        [
            "A near double is a double plus one more, or minus one.",
            "6 + 7 is like 6 + 6, then one more. 12 + 1 = 13.",
            "8 + 7 is like 8 + 8, then one less. 16 − 1 = 15. Or 7 + 7 + 1 = 15.",
            "This is a smart shortcut. You use a fact you already know.",
            "Look for numbers that sit next to each other, like 4 and 5.",
            "If it helps, draw the double first, then add the extra dot.",
        ],
        solved(1, "5 + 6 = ?",
               ["5 + 5 is 10. That is the double.",
                "6 is one more than 5.",
                "So 5 + 6 = 10 + 1 = 11."],
               "11")
        + step_reveal(
            ["Look at 9 + 8.",
             "Think of 8 + 8 = 16.",
             "9 is one more than 8.",
             "16 + 1 = 17.",
             "So 9 + 8 = 17."],
            vid="g1u3-c5-steps",
        ),
        try_this("Find the twin", "See the close pair. Make a double. Then add or take one."),
        21,
    )

    c6 = concept_block(
        "6. Add three numbers",
        [
            "You can add three numbers. Add two first. Then add the last one.",
            "Look for a 10. In 6 + 4 + 3, add 6 + 4 first because that is 10. Then 10 + 3 = 13.",
            "Look for a double. In 5 + 5 + 2, add 5 + 5 first.",
            "You can add in any order. Pick the easy pair.",
            "Keep the running total in your head or on paper.",
            "Check by adding a different pair first. Same answer? Good.",
        ],
        solved(1, "3 + 7 + 2 = ?",
               ["3 + 7 = 10. Nice ten!",
                "10 + 2 = 12."],
               "12")
        + solved(2, "4 + 4 + 5 = ?",
                 ["4 + 4 is a double: 8.",
                  "8 + 5 = 13."],
                 "13")
        + watch_out("Forgetting one number",
                    "When there are three numbers, check you used all three. Circle each after you add it."),
        phet_box("pairs"),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Put groups together",
            "Count on from the bigger number",
            "Make a ten to add",
            "Use doubles",
            "Use near doubles",
            "Add three numbers",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u3_questions()


# ===========================================================================
# UNIT 4: Subtraction within 20
# ===========================================================================

def _sub_fact(a, b, idx, story=None):
    s = a - b
    text = story or f"{a} − {b} = ?"
    expl = f"{a} take away {b} is {s}. You can count back {b} from {a}, or think {b} + ? = {a}."
    return mq(text, s, expl, idx)


def _u4_questions():
    qs = []
    idx = 1

    for a, b in [(5, 2), (8, 3), (6, 1), (9, 4), (7, 7)]:
        qs.append(_sub_fact(a, b, idx, f"You have {a} cookies. You eat {b}. How many are left?"))
        idx += 1

    for a, b in [(10, 2), (12, 3), (9, 1), (15, 4), (11, 2)]:
        qs.append(_sub_fact(a, b, idx, f"Start at {a}. Count back {b}. Where do you land?"))
        idx += 1

    for a, b in [(9, 5), (8, 3), (12, 4), (7, 2), (15, 6)]:
        qs.append(mq(
            f"What plus {b} makes {a}? Then {a} − {b} = ?",
            a - b,
            f"{b} + {a - b} = {a}, so {a} − {b} = {a - b}. Subtraction undoes addition.",
            idx,
        ))
        idx += 1

    for a, b in [(10, 3), (10, 7), (10, 1), (10, 6), (10, 4)]:
        qs.append(_sub_fact(a, b, idx, f"Take from ten: {a} − {b} = ?"))
        idx += 1

    for whole, part in [(8, 3), (9, 5), (12, 7), (14, 6), (11, 4)]:
        missing = whole - part
        qs.append(mq(
            f"A story has {whole} in all. {part} are red. How many are not red?",
            missing,
            f"The parts add to the whole: {part} + {missing} = {whole}. So {whole} − {part} = {missing}.",
            idx,
        ))
        idx += 1

    for a, b in [(6, 2), (8, 5), (9, 4), (7, 3), (5, 1)]:
        qs.append(mq(
            f"Fact family: {a} + {b} = {a + b}. What is {a + b} − {a}?",
            b,
            f"The family is {a} + {b} = {a + b} and {a + b} − {a} = {b} and {a + b} − {b} = {a}.",
            idx,
        ))
        idx += 1

    facts = [
        (6, 4), (8, 2), (9, 6), (7, 5), (10, 8), (10, 5), (11, 5), (12, 6), (13, 4), (14, 8),
        (15, 7), (16, 9), (17, 8), (18, 9), (19, 10), (20, 5), (20, 11), (13, 8), (14, 5), (15, 9),
        (16, 7), (12, 9), (11, 8), (9, 9), (8, 8), (20, 1), (18, 6), (17, 9), (16, 8), (15, 3),
        (14, 7), (13, 6), (12, 8), (11, 3), (10, 9), (9, 2), (8, 6), (7, 1), (6, 3), (20, 8),
        (19, 7), (18, 4), (17, 5), (16, 4), (15, 8), (14, 9), (13, 9), (12, 4), (11, 7), (20, 15),
    ]
    for a, b in facts:
        if a < b or a > 20:
            continue
        qs.append(_sub_fact(a, b, idx))
        idx += 1

    return _fill(qs, 55, lambda i: _sub_fact(12 + (i % 8), 1 + (i % 6), i))


def build_unit4():
    title = "First Grade Math Unit 4: Subtraction to 20"
    description = (
        "Subtract within 20: take away, count back, use plus facts, subtract from 10, "
        "find a missing part, and fact families."
    )

    c1 = concept_block(
        "1. Take away",
        [
            "Subtract means take some away. Find how many are left.",
            "The minus sign − means take away.",
            "8 − 3 = 5. Eight, take away three, five left.",
            "You cannot take away more than you have in these problems. We stay at 0 or more.",
            "A number minus itself is 0. 7 − 7 = 0. All gone.",
            "A number minus 0 stays the same. 6 − 0 = 6.",
        ],
        solved(1, "There are 9 balloons. 4 pop. How many are left?",
               ["Start with 9.",
                "Take away 4.",
                "9 − 4 = 5."],
               "5")
        + matching(
            [("5 − 2", "3"), ("6 − 6", "0"), ("8 − 1", "7"), ("4 − 0", "4")],
            vid="g1u4-c1-match",
        ),
        kid_tip("Cross them out", "Draw the group. Cross out the ones you take away. Count what is left.")
        + phet_box("pairs"),
        1,
    )

    c2 = concept_block(
        "2. Count back",
        [
            "Start at the first number. Count back the second number.",
            "For 11 − 3, start at 11. Count back: 10, 9, 8.",
            "Use fingers for the counts back.",
            "Counting back is great when you subtract 1, 2, or 3.",
            "If you subtract a big number, another way may be faster (next ideas).",
            "Say the start number, then whisper the counts back.",
        ],
        solved(1, "12 − 2 = ?",
               ["Start at 12.",
                "Count back 2: 11, 10.",
                "Land on 10."],
               "10")
        + step_reveal(
            ["See 9 − 3.",
             "Put 9 in your head.",
             "Count back three times: 8, 7, 6.",
             "9 − 3 = 6."],
            vid="g1u4-c2-steps",
        ),
        try_this("Small take-aways", "If you subtract 1, 2, or 3, count back. It is quick."),
        6,
    )

    c3 = concept_block(
        "3. Think of the plus fact",
        [
            "Subtraction undoes addition. They are partners.",
            "If 6 + 3 = 9, then 9 − 3 = 6 and 9 − 6 = 3.",
            "When you see 14 − 8, think: 8 plus what makes 14?",
            "Count up from 8 to 14: 9, 10, 11, 12, 13, 14. That is 6 jumps. So 14 − 8 = 6.",
            "This is often easier than counting all the way back.",
            "Plus facts you know make minus facts you know.",
        ],
        solved(1, "13 − 6 = ?",
               ["Think: 6 + ? = 13.",
                "6 + 7 = 13. You know that plus fact.",
                "So 13 − 6 = 7."],
               "7")
        + matching(
            [("5 + 4 = 9", "9 − 4 = 5"), ("7 + 3 = 10", "10 − 3 = 7"),
             ("8 + 8 = 16", "16 − 8 = 8"), ("9 + 6 = 15", "15 − 6 = 9")],
            vid="g1u4-c3-match",
        ),
        phet_box("ten"),
        11,
    )

    c4 = concept_block(
        "4. Subtract from 10",
        [
            "Facts from 10 are special. 10 − 1 = 9, 10 − 2 = 8, 10 − 3 = 7… down to 10 − 9 = 1.",
            "Ten fingers help. Put up 10. Fold down some. Count what is still up.",
            "These facts help make-a-ten later, and they help bigger minus problems.",
            "For 14 − 6 you can think: 10 − 6 = 4, then add the extra 4 from 14. 4 + 4 = 8.",
            "That is an advanced trick. Use it when you are ready.",
            "Master the ten facts first. They show up everywhere.",
        ],
        solved(1, "10 − 7 = ?",
               ["Ten fingers up.",
                "Fold down 7.",
                "3 fingers still up. 10 − 7 = 3."],
               "3")
        + solved(2, "10 − 4 = ?",
                 ["What plus 4 makes 10? 6.",
                  "So 10 − 4 = 6."],
                 "6")
        + kid_tip("Ten frame", "A ten-frame has 10 boxes. Fill some. The empty boxes show the minus answer."),
        16,
    )

    c5 = concept_block(
        "5. Missing part",
        [
            "Sometimes you know the whole and one part. You need the other part.",
            "There are 12 crayons. 5 are blue. How many are not blue?",
            "That is 12 − 5, or 5 + ? = 12.",
            "Both ways ask for the missing part.",
            "Draw a bar: whole on top, two parts under it. One part is known.",
            "Number stories often hide a missing part. Find the whole first.",
        ],
        solved(1, "9 kids. 4 have hats. How many have no hat?",
               ["Whole is 9.",
                "One part is 4 (hats).",
                "Missing part: 9 − 4 = 5."],
               "5")
        + step_reveal(
            ["Find the whole. How many in all?",
             "Find the part you know.",
             "Take the part from the whole, or count up from the part.",
             "The leftover is the missing part."],
            vid="g1u4-c5-steps",
        ),
        watch_out("Adding by mistake",
                  "If the story says how many in all and how many of one kind, you subtract to find the other kind. You do not add."),
        21,
    )

    c6 = concept_block(
        "6. Fact families",
        [
            "A fact family uses the same three numbers in plus and minus sentences.",
            "For 3, 5, and 8: 3+5=8, 5+3=8, 8−5=3, 8−3=5.",
            "Four sentences. Same three friends.",
            "If you know one, you can write the other three.",
            "Fact families prove that plus and minus belong together.",
            "Pick any plus fact you love and write its family.",
        ],
        solved(1, "Numbers 4, 6, 10. What is 10 − 4?",
               ["These three numbers make a family.",
                "4 + 6 = 10.",
                "So 10 − 4 = 6."],
               "6")
        + matching(
            [("2, 8, 10", "2 + 8 = 10"), ("4, 4, 8", "8 − 4 = 4"),
             ("9, 1, 10", "10 − 1 = 9"), ("7, 6, 13", "7 + 6 = 13")],
            vid="g1u4-c6-match",
        ),
        try_this("Write all four", "After any plus fact, write the turn-around plus and the two minus facts."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Take away to subtract",
            "Count back 1, 2, or 3",
            "Use a plus fact to subtract",
            "Subtract from 10",
            "Find a missing part",
            "Write fact families",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u4_questions()
