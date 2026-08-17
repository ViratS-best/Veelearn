"""Fifth Grade Math units 1–4: thousandths, multi-digit ops, unlike-denominator fractions, multiply fractions."""

from curriculum_kit import (
    lesson_figure,
    svg_rect,
    svg_tape,
    svg_dots,
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
    place_value_thousandths,
    fraction_bars,
    decimal_number_line,
    double_number_line,
    hundredths_grid,
    area_model,
    fraction_area_model,
    mq,
    renumber,
)


def _fill(qs, need, factory):
    while len(qs) < need:
        qs.append(factory(len(qs) + 1))
    return renumber(qs[:need])


# ===========================================================================
# UNIT 1: Decimals to thousandths
# ===========================================================================

def _u1_questions():
    qs = []
    idx = 1

    for text, ans, dist, expl in [
        ("In 2.407, the 4 is in which place?", "tenths", ["hundredths", "thousandths", "ones"], "Right after the point is tenths."),
        ("In 2.407, the 0 is in which place?", "hundredths", ["tenths", "thousandths", "ones"], "Two places after the point is hundredths."),
        ("In 2.407, the 7 is in which place?", "thousandths", ["tenths", "hundredths", "ones"], "Three places after the point is thousandths."),
        ("What is the value of the 7 in 2.407?", "0.007", ["0.07", "0.7", "7"], "7 thousandths = 0.007."),
        ("0.001 is one…", "thousandth", ["tenth", "hundredth", "thousand"], "Three places after the point."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, dist, expl in [
        ("Write 2 + 4/10 + 7/1000 as a decimal.", "2.407", ["2.47", "2.047", "24.07"], "4 tenths and 7 thousandths. Hundredths is 0."),
        ("Write two and three hundred five thousandths.", "2.305", ["2.035", "2.350", "23.05"], "305 thousandths is 0.305."),
        ("0.40 is the same as…", "0.400", ["0.040", "4.00", "0.004"], "Zeros at the end after the point do not change the value."),
        ("Which is greater: 0.8 or 0.79?", "0.8", ["0.79", "same", "0.08"], "0.8 = 0.800, and 800 thousandths > 790 thousandths."),
        ("Which is less: 3.206 or 3.26?", "3.206", ["3.26", "same", "3.260"], "3.26 = 3.260. Hundredths: 0 vs 6."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for n, place, ans, expl in [
        ("1.456", "nearest tenth", "1.5", "Look at hundredths: 5, so 1.4 rounds up to 1.5."),
        ("1.456", "nearest hundredth", "1.46", "Look at thousandths: 6 ≥ 5, so 1.45 rounds up to 1.46."),
        ("2.304", "nearest tenth", "2.3", "Hundredths is 0, so stay at 2.3."),
        ("0.995", "nearest hundredth", "1.00", "Thousandths is 5, so 0.99 rounds up to 1.00."),
        ("7.841", "nearest thousandth", "7.841", "It is already to the thousandth."),
    ]:
        qs.append(mq(f"Round {n} to the {place}.", ans, expl, idx, distractors=["1.4", "1.45", "2.31"] if ans not in ("1.4", "1.45", "2.31") else ["0.9", "2.0", "7.8"]))
        idx += 1

    for a, b, op, ans in [
        (0.6, 10, "×", "6"),
        (0.6, 100, "×", "60"),
        (0.6, 1000, "×", "600"),
        (4.5, 10, "÷", "0.45"),
        (4.5, 100, "÷", "0.045"),
    ]:
        symbol = "×" if op == "×" else "÷"
        qs.append(mq(
            f"What is {a} {symbol} {b}?",
            ans,
            f"Each ×10 moves the point one place right. Each ÷10 moves it one place left. {a} {symbol} {b} = {ans}.",
            idx,
            distractors=["0.06", "45", "0.006"] if ans not in ("0.06", "45", "0.006") else ["6", "0.45", "60"],
        ))
        idx += 1

    for text, ans, dist, expl in [
        ("3.07 compared with 3.070 is…", "equal", ["3.07 is greater", "3.070 is greater", "cannot tell"], "A zero at the end after the point does not change the value."),
        ("Which digit makes 5.2_6 greater than 5.246? The blank is thousandths.", "7", ["4", "3", "1"], "7 thousandths > 6 thousandths."),
        ("How many thousandths are in 1 tenth?", "100", ["10", "1000", "1"], "0.1 = 0.100, so 100 thousandths."),
        ("How many thousandths are in 1 hundredth?", "10", ["100", "1", "1000"], "0.01 = 0.010."),
        ("0.009 is how many thousandths?", "9", ["90", "900", "0.9"], "Nine thousandths."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    extras = [
        ("In 8.153 the 1 is…", "tenths", ["hundredths", "thousandths", "ones"], "First digit after the point."),
        ("In 8.153 the 5 is…", "hundredths", ["tenths", "thousandths", "ones"], "Second digit after the point."),
        ("In 8.153 the 3 is…", "thousandths", ["tenths", "hundredths", "ones"], "Third digit after the point."),
        ("Write 7/1000 as a decimal.", "0.007", ["0.07", "0.7", "7.000"], "7 thousandths."),
        ("Write 23/100 as a decimal.", "0.23", ["0.023", "2.3", "0.2300 only as 2300"], "23 hundredths = 0.23."),
        ("Write 0.6 as thousandths.", "0.600", ["0.006", "0.060", "6.00"], "6 tenths = 600 thousandths."),
        ("Which is greater: 0.099 or 0.1?", "0.1", ["0.099", "same", "0.09"], "0.1 = 0.100."),
        ("Which is less: 4.08 or 4.8?", "4.08", ["4.8", "same", "4.80"], "Tenths: 0 vs 8."),
        ("Round 6.251 to the nearest tenth.", "6.3", ["6.2", "6.25", "6.0"], "Hundredths is 5, so 6.2 rounds up."),
        ("Round 9.994 to the nearest hundredth.", "9.99", ["10.00", "9.9", "9.90"], "Thousandths is 4, so stay."),
        ("0.25 × 10 = ?", "2.5", ["0.025", "25", "0.250"], "Point moves one place right."),
        ("3.6 ÷ 10 = ?", "0.36", ["36", "0.036", "3.06"], "Point moves one place left."),
        ("12.4 × 100 = ?", "1240", ["124", "1.24", "12.400"], "Two places right. Fill with a zero."),
        ("0.07 × 1000 = ?", "70", ["7", "0.70", "700"], "Three places right."),
        ("Which expanded form matches 4.206?", "4 + 2/10 + 6/1000", ["4 + 2/10 + 6/100", "4 + 20/10 + 6/1000", "4 + 2/100 + 6/1000"], "2 tenths and 6 thousandths."),
        ("0.5, 0.50, and 0.500 are…", "equal", ["getting smaller", "getting bigger", "not decimals"], "Trailing zeros after the point do not change value."),
        ("The digit 9 in 0.009 has value…", "0.009", ["0.09", "0.9", "9"], "Thousandths place."),
        ("Between 2.3 and 2.4, a number to the thousandth could be…", "2.351", ["2.4", "2.3000 only if equal to 2.3", "23.51"], "2.351 is between them."),
        ("1.002 compared with 1.02 is…", "1.02 is greater", ["1.002 is greater", "equal", "cannot tell"], "1.02 = 1.020. Hundredths: 0 vs 2."),
        ("Write four and twelve thousandths.", "4.012", ["4.12", "4.120", "40.12"], "12 thousandths needs a 0 in hundredths."),
    ]
    for text, ans, dist, expl in extras:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"What is 0.{i:03d} as thousandths? (the digits after the point)",
        str(i) if i <= 9 else str(i),
        f"Read the last place as thousandths when there are three digits.",
        i,
        distractors=[str(i * 10), f"0.{i}", str(i + 3)],
    ))


def build_unit1():
    title = "Fifth Grade Math Unit 1: Decimals to Thousandths"
    description = (
        "Read, write, compare, and round decimals through the thousandths place. Use ×10 and ÷10 with the decimal point."
    )

    c1 = concept_block(
        "1. Places through thousandths",
        [
            "Fifth grade decimals go three places after the point: tenths, hundredths, thousandths.",
            "In 2.407 the 2 is ones, the 4 is tenths, the 0 is hundredths, and the 7 is thousandths.",
            "0.007 is seven thousandths. That is a tiny slice of one whole — one of a thousand equal parts.",
            "Each place is 10 times the place on its right. Ten thousandths make one hundredth. Ten hundredths make one tenth.",
            "A place-value chart keeps every digit in its home, including the zeros.",
            "Zeros in the middle matter. 2.407 is not the same as 2.47.",
        ],
        place_value_thousandths()
        + solved(1, "What is the value of the 7 in 2.407?",
                 ["The 7 sits three places after the point.",
                  "That place is thousandths.",
                  "7 thousandths = 0.007."],
                 "0.007")
        + matching(
            [("tenths", "0.1"), ("hundredths", "0.01"), ("thousandths", "0.001"), ("ones", "1")],
            vid="g5u1-c1-match",
        ),
        kid_tip("Count the places", "One place after the point: tenths. Two: hundredths. Three: thousandths."),
        1,
    )

    c2 = concept_block(
        "2. Read, write, and expand",
        [
            "Standard form: 2.407.",
            "Word form: two and four hundred seven thousandths.",
            "Expanded form: 2 + 4/10 + 0/100 + 7/1000, or 2 + 0.4 + 0.007.",
            "The word and marks the decimal point: two and four tenths is 2.4.",
            "Twelve thousandths is 0.012, not 0.12. You need a zero in the tenths or hundredths if that place is empty.",
            "Practice switching among the three forms until they feel like the same number.",
        ],
        place_value_thousandths("2", "3", "0", "5")
        + solved(1, "Write two and three hundred five thousandths.",
               ["Two ones, then 305 thousandths.",
                "305 thousandths is 0.305.",
                "Put them together: 2.305."],
               "2.305")
        + matching(
            [("4 + 2/10 + 6/1000", "4.206"), ("7 + 12/1000", "7.012"),
             ("3/10 + 9/1000", "0.309"), ("5 + 8/100", "5.08")],
            vid="g5u1-c2-match",
        ),
        try_this("Say the last place", "If you stop at thousandths, read the digits after the point as a whole number, then say thousandths: 407 thousandths."),
        6,
    )

    c3 = concept_block(
        "3. Compare decimals",
        [
            "Line up the decimal points. Compare from the left, place by place.",
            "If one number has fewer digits, you may write extra zeros on the right: 0.8 = 0.800.",
            "Those extra zeros do not change the value. They only help you compare.",
            "0.8 is greater than 0.79 because 0.800 > 0.790.",
            "3.206 is less than 3.26 because 3.206 vs 3.260 — hundredths 0 vs 6.",
            "Do not compare by 'which looks longer.' 0.099 looks long, but 0.1 is greater.",
        ],
        decimal_number_line(
            0.7, 0.9,
            marks=[(0.79, "0.79"), (0.8, "0.80")],
            tick_step=0.05,
            title="Compare 0.79 and 0.80",
            caption="0.8 = 0.80. On the line, 0.80 sits to the right of 0.79, so 0.8 is greater.",
        )
        + solved(1, "Which is greater: 0.8 or 0.79?",
               ["Write 0.8 as 0.800.",
                "Compare thousandths: 800 vs 790.",
                "800 thousandths is more."],
               "0.8")
        + step_reveal(
            ["Line up the points.",
             "Fill trailing zeros so both have the same number of places.",
             "Compare ones, then tenths, then hundredths, then thousandths.",
             "The first place that differs decides."],
            vid="g5u1-c3-steps",
        ),
        watch_out("Thinking more digits means bigger",
                  "0.099 has three digits after the point, but 0.1 is still greater. Compare places, not digit count."),
        11,
    )

    c4 = concept_block(
        "4. Round decimals",
        [
            "Rounding to a place means looking at the digit one place to its right.",
            "If that digit is 5 or more, round up. If it is 4 or less, stay.",
            "1.456 to the nearest tenth: look at hundredths (5) → 1.5.",
            "1.456 to the nearest hundredth: look at thousandths (6) → 1.46.",
            "Sometimes rounding up rolls into the next whole: 0.995 to the nearest hundredth is 1.00.",
            "Rounding is a close neighbor, not the exact number. Use it to estimate.",
        ],
        decimal_number_line(
            1.40, 1.50,
            marks=[(1.456, "1.456"), (1.46, "1.46")],
            tick_step=0.02,
            title="Round 1.456 to the nearest hundredth",
            caption="Thousandths is 6, so 1.45 rounds up. The nearest hundredth tick is 1.46.",
        )
        + solved(1, "Round 1.456 to the nearest hundredth.",
               ["Hundredths is the 5.",
                "Look at thousandths: 6.",
                "6 ≥ 5, so 1.45 rounds up to 1.46."],
               "1.46")
        + solved(2, "Round 2.304 to the nearest tenth.",
                 ["Tenths is 3.",
                  "Hundredths is 0, which is less than 5.",
                  "Stay at 2.3."],
                 "2.3"),
        kid_tip("Underline the place", "Underline the digit you are rounding to. Circle the neighbor on its right. That neighbor decides."),
        16,
    )

    c5 = concept_block(
        "5. Times ten and one tenth with decimals",
        [
            "×10 moves the decimal point one place to the right. 0.6 × 10 = 6.",
            "×100 moves it two places. 0.6 × 100 = 60.",
            "×1,000 moves it three places. 0.6 × 1,000 = 600.",
            "÷10 moves the point one place to the left. 4.5 ÷ 10 = 0.45.",
            "You may need to write extra zeros: 4.5 ÷ 100 = 0.045.",
            "This is the same place-value idea as whole numbers, now with digits after the point.",
        ],
        double_number_line(
            "value", ["0.07", "0.7", "7", "70"],
            "×", ["×1", "×10", "×100", "×1,000"],
            title="0.07 × 10, 100, and 1,000",
            caption="Each ×10 moves the decimal point one place right: 0.07 → 0.7 → 7 → 70.",
        )
        + solved(1, "What is 0.07 × 1,000?",
               ["Move the point three places right.",
                "0.07 → 0.7 → 7 → 70.",
                "Fill the empty ones place with a zero if you need it."],
               "70")
        + phet_box("area_dec"),
        try_this("Count the zeros", "The number of zeros in 10, 100, or 1,000 tells you how many places the point moves."),
        21,
    )

    c6 = concept_block(
        "6. Same value, different looks",
        [
            "0.5, 0.50, and 0.500 are equal. They are five tenths, fifty hundredths, and five hundred thousandths.",
            "Equivalent decimals name the same amount with extra zeros on the right.",
            "You can also write 0.5 as 1/2 or 5/10. Decimals and fractions are two languages for parts.",
            "On a number line, 0.400 and 0.4 land on the same tick.",
            "Use this when you compare, add, or subtract: make the number of places match first.",
            "Do not add zeros in the middle. 0.05 is not 0.5.",
        ],
        place_value_thousandths("3", "0", "7", "0")
        + solved(1, "Is 3.07 equal to 3.070?",
               ["3.07 is 3 ones and 7 hundredths.",
                "3.070 is 3 ones, 7 hundredths, and 0 thousandths.",
                "Zero thousandths does not change the amount. They are equal."],
               "equal")
        + matching(
            [("0.4", "0.400"), ("0.25", "0.250"), ("1.5", "1.50"), ("0.07", "0.070")],
            vid="g5u1-c6-match",
        ),
        watch_out("Zeros in the middle", "0.05 is five hundredths. 0.5 is five tenths. Only zeros at the far right after the point are 'free'."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Name tenths, hundredths, and thousandths",
            "Read, write, and expand decimals",
            "Compare by lining up points",
            "Round to a given place",
            "Multiply and divide by 10, 100, and 1,000",
            "See equivalent decimals",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u1_questions()


# ===========================================================================
# UNIT 2: Multi-digit operations
# ===========================================================================

def _u2_questions():
    qs = []
    idx = 1

    for a, b in [(24, 36), (18, 45), (32, 28), (15, 67), (40, 25)]:
        qs.append(mq(f"{a} × {b} = ?", a * b, f"{a} × {b} = {a * b}.", idx))
        idx += 1

    for a, b in [(144, 12), (225, 15), (384, 16), (560, 14), (1008, 24)]:
        qs.append(mq(f"{a} ÷ {b} = ?", a // b, f"{b} × {a // b} = {a}, so the quotient is {a // b}.", idx))
        idx += 1

    for text, ans, dist, expl in [
        ("3.25 + 1.4 = ?", "4.65", ["4.29", "4.65 0", "5.65"], "Line up points: 3.25 + 1.40 = 4.65."),
        ("6.8 − 2.35 = ?", "4.45", ["4.55", "8.45", "4.4"], "6.80 − 2.35 = 4.45."),
        ("0.7 + 0.25 + 0.05 = ?", "1.00", ["0.97", "1.10", "0.325"], "0.70 + 0.25 + 0.05 = 1.00."),
        ("10 − 3.06 = ?", "6.94", ["7.94", "6.04", "13.06"], "10.00 − 3.06 = 6.94."),
        ("2.5 + 2.5 + 2.5 = ?", "7.5", ["6.5", "7.0", "5.5"], "Three groups of 2.5 is 7.5."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, dist, expl in [
        ("0.4 × 0.3 = ?", "0.12", ["0.12 0", "1.2", "0.07"], "4 × 3 = 12, two decimal places → 0.12."),
        ("1.5 × 4 = ?", "6", ["5.5", "0.6", "2.0"], "1.5 four times is 6."),
        ("0.25 × 8 = ?", "2", ["0.2", "20", "1.25"], "A quarter of 8 is 2."),
        ("2.5 × 0.4 = ?", "1.0", ["1.00 as 10", "0.1", "6.0"], "2.5 × 4 tenths = 1."),
        ("0.6 × 0.05 = ?", "0.03", ["0.3", "0.003", "3.0"], "6 × 5 = 30, three decimal places → 0.030 = 0.03."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, dist, expl in [
        ("3.6 ÷ 0.4 = ?", "9", ["0.9", "90", "8"], "How many 0.4s in 3.6? Nine."),
        ("4.8 ÷ 6 = ?", "0.8", ["8", "0.08", "1.2"], "4.8 shared 6 ways is 0.8."),
        ("0.9 ÷ 0.3 = ?", "3", ["0.3", "6", "0.6"], "Three tenths fit into nine tenths three times."),
        ("5 ÷ 0.5 = ?", "10", ["1", "25", "0.1"], "How many halves in 5? Ten."),
        ("1.2 ÷ 0.06 = ?", "20", ["2", "0.2", "200"], "1.20 ÷ 0.06 = 120 ÷ 6 = 20."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    more = [
        ("47 × 26 = ?", 1222, None, "40×26=1,040 and 7×26=182. Sum 1,222."),
        ("108 × 9 = ?", 972, None, "100×9=900 and 8×9=72."),
        ("250 × 12 = ?", 3000, None, "25×12=300, then ×10 = 3,000."),
        ("816 ÷ 8 = ?", 102, None, "800÷8=100 and 16÷8=2."),
        ("945 ÷ 15 = ?", 63, None, "15×60=900, 15×3=45."),
        ("1,200 ÷ 25 = ?", 48, None, "25×48=1,200."),
        ("7.2 + 0.85 = ?", "8.05", ["8.05", "7.105", "15.7"][1:], "7.20 + 0.85 = 8.05."),
        ("9.01 − 0.2 = ?", "8.81", ["8.81", "8.99", "9.21"][1:], "9.01 − 0.20 = 8.81."),
        ("0.125 + 0.375 = ?", "0.5", ["0.5", "0.490", "1.25"][1:], "500 thousandths = 0.5."),
        ("3 × 1.25 = ?", "3.75", ["3.75", "4.25", "3.25"][1:], "Three copies of 1.25."),
        ("0.8 × 0.8 = ?", "0.64", ["0.64", "1.6", "0.16"][1:], "64 hundredths."),
        ("12.6 ÷ 3 = ?", "4.2", ["4.2", "42", "3.6"][1:], "12÷3=4 and 0.6÷3=0.2."),
        ("0.48 ÷ 0.08 = ?", "6", ["6", "0.6", "60"][1:], "48÷8=6."),
        ("Estimate 49 × 21 by rounding.", "1,000", ["1,000", "70", "490"][1:], "50×20=1,000."),
        ("Estimate 7.9 + 2.2 by rounding to ones.", "10", ["10", "9", "11"][1:], "8+2=10."),
    ]
    for row in more:
        text, ans, dist, expl = row
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for a, b in [(13, 17), (22, 19), (31, 14), (45, 18), (50, 16)]:
        qs.append(mq(f"{a} × {b} = ?", a * b, f"Product is {a * b}.", idx))
        idx += 1
    for a, b in [(196, 14), (288, 18), (432, 16), (675, 25), (840, 21)]:
        qs.append(mq(f"{a} ÷ {b} = ?", a // b, f"Quotient is {a // b}.", idx))
        idx += 1

    dec_add = [
        ("4.6 + 3.25 = ?", "7.85", ["7.85", "7.31", "8.85"][1:]),
        ("0.09 + 0.01 = ?", "0.10", ["0.1", "0.001", "0.08"][:3]),
        ("5 − 0.25 = ?", "4.75", ["4.75", "5.25", "4.25"][1:]),
        ("2.004 + 0.12 = ?", "2.124", ["2.124", "2.016", "3.204"][1:]),
        ("8.5 − 8.05 = ?", "0.45", ["0.45", "0.55", "1.45"][1:]),
    ]
    for text, ans, dist in dec_add:
        qs.append(mq(text, ans, f"Line up the points. Answer is {ans}.", idx, distractors=dist))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"What is {20 + i} × 10?",
        (20 + i) * 10,
        f"Times 10 moves one place left. {(20 + i) * 10}.",
        i,
    ))


def build_unit2():
    title = "Fifth Grade Math Unit 2: Multi-Digit Operations"
    description = (
        "Multiply and divide multi-digit whole numbers. Add, subtract, multiply, and divide decimals using place value."
    )

    c1 = concept_block(
        "1. Multiply multi-digit whole numbers",
        [
            "You can split a factor into tens and ones, multiply each part, then add. That is the area model.",
            "24 × 36: 20×30, 20×6, 4×30, 4×6. Then add the four products.",
            "The standard algorithm does the same work in a compact stack.",
            "Estimate first: 24×36 is near 20×40 = 800, so your exact answer should be near 800.",
            "Zeros at the end are friends: 40×25 = 1,000 because 4×25=100 and one extra zero.",
            "Keep places lined up when you add the partial products.",
        ],
        area_model(
            [20, 4], [30, 6],
            title="Area model for 24 × 36",
            caption="Split 24 into 20+4 and 36 into 30+6. Add the four products: 600+120+120+24 = 864.",
        )
        + solved(1, "Find 24 × 36.",
               ["20×30 = 600.",
                "20×6 = 120.",
                "4×30 = 120.",
                "4×6 = 24.",
                "600+120+120+24 = 864."],
               "864")
        + phet_box("area_mult"),
        kid_tip("Estimate first", "Round, multiply, then compute the exact product. If they are far apart, check your places."),
        1,
    )

    c2 = concept_block(
        "2. Divide multi-digit numbers",
        [
            "Division asks: how many groups? Or: how many in each group?",
            "Check with multiplication: if 144 ÷ 12 = 12, then 12 × 12 must be 144.",
            "A two-digit divisor takes patience. Estimate: 384 ÷ 16 is near 400 ÷ 16 = 25, then adjust.",
            "Remainders still mean leftover. In fifth grade many problems divide evenly so you can focus on the method.",
            "You can also think of 816 ÷ 8 as sharing 8 hundreds, 1 ten, and 6 ones.",
            "If a step feels stuck, try a smaller related fact: 16×20=320, then see how much is left.",
        ],
        lesson_figure(
            svg_rect(16, 24),
            "384 ÷ 16 as an area",
            "A 16-by-24 rectangle has area 384, so 384 ÷ 16 = 24 groups.",
        )
        + solved(1, "Find 384 ÷ 16.",
               ["16×20 = 320.",
                "384 − 320 = 64.",
                "16×4 = 64.",
                "20+4 = 24 groups."],
               "24")
        + step_reveal(
            ["Estimate how many times the divisor fits.",
             "Multiply.",
             "Subtract.",
             "Bring down the next digit (or leftover).",
             "Check the quotient by multiplying."],
            vid="g5u2-c2-steps",
        ),
        watch_out("Skipping the check", "Multiply quotient × divisor. You should get back the original number (when there is no remainder)."),
        6,
    )

    c3 = concept_block(
        "3. Add and subtract decimals",
        [
            "Line up the decimal points. Then add or subtract as with whole numbers.",
            "Write extra zeros so both numbers have the same places: 6.8 − 2.35 becomes 6.80 − 2.35.",
            "Bring the decimal point straight down into the answer.",
            "10 − 3.06 is 10.00 − 3.06 = 6.94.",
            "Adding tenths, hundredths, and thousandths only works when you respect their places.",
            "A sum like 0.7 + 0.25 + 0.05 should make 1.00 — a whole.",
        ],
        decimal_number_line(
            0, 8,
            marks=[(2.35, "2.35"), (6.8, "6.80")],
            tick_step=1,
            title="Subtract on a decimal number line",
            caption="Line up places: 6.80 − 2.35. The jump from 2.35 to 6.80 is 4.45.",
        )
        + solved(1, "Compute 6.8 − 2.35.",
               ["Write 6.80.",
                "Subtract hundredths: 80 − 35 = 45 hundredths, after regrouping tenths if needed.",
                "Ones: 6 − 2 = 4.",
                "Difference: 4.45."],
               "4.45")
        + matching(
            [("3.25 + 1.40", "4.65"), ("10.00 − 3.06", "6.94"),
             ("0.70 + 0.30", "1.00"), ("2.004 + 0.120", "2.124")],
            vid="g5u2-c3-match",
        ),
        try_this("Make the places match", "Annex zeros on the right after the point until both numbers look the same length."),
        11,
    )

    c4 = concept_block(
        "4. Multiply decimals",
        [
            "Multiply as if the numbers were whole, then place the point.",
            "Count the total decimal places in the factors. That many places go in the product.",
            "0.4 × 0.3: 4×3=12, two places → 0.12.",
            "0.6 × 0.05: 6×5=30, three places → 0.030, which is 0.03.",
            "A whole number times a decimal is repeated addition: 4 × 1.5 = 6.",
            "Estimate: 2.5 × 0.4 should be near 2 × 0.5 = 1.",
        ],
        hundredths_grid(
            cols=4, rows=3,
            title="0.4 × 0.3 on a hundredths grid",
            caption="4 tenths by 3 tenths shades 12 hundredths. 0.4 × 0.3 = 0.12.",
        )
        + solved(1, "Find 0.4 × 0.3.",
               ["Ignore points for a moment: 4 × 3 = 12.",
                "0.4 has one place. 0.3 has one place. Total: two places.",
                "12 with two places is 0.12."],
               "0.12")
        + phet_box("arith"),
        kid_tip("Count the places", "Tenths × tenths is hundredths. Tenths × hundredths is thousandths."),
        16,
    )

    c5 = concept_block(
        "5. Divide decimals",
        [
            "You can think: how many of these fit into that?",
            "3.6 ÷ 0.4 asks how many 0.4s are in 3.6. There are 9.",
            "A useful move: multiply dividend and divisor by the same 10, 100, or 1,000 so the divisor becomes a whole number.",
            "1.2 ÷ 0.06 → multiply both by 100 → 120 ÷ 6 = 20.",
            "4.8 ÷ 6 is sharing 4.8 into 6 equal parts: 0.8 each.",
            "Check with multiplication: 9 × 0.4 = 3.6.",
        ],
        double_number_line(
            "dividend", ["1.2", "12", "120"],
            "divisor", ["0.06", "0.6", "6"],
            title="1.2 ÷ 0.06 — move both points",
            caption="×10, then ×10 again, so both numbers ×100. Now 120 ÷ 6 = 20.",
        )
        + solved(1, "Find 1.2 ÷ 0.06.",
               ["Multiply both numbers by 100 to move the points.",
                "Now it is 120 ÷ 6.",
                "120 ÷ 6 = 20.",
                "Check: 20 × 0.06 = 1.20."],
               "20")
        + step_reveal(
            ["Make the divisor a whole number by ×10, ×100, or ×1,000.",
             "Do the same to the dividend.",
             "Divide the new whole-number problem.",
             "Check by multiplying."],
            vid="g5u2-c5-steps",
        ),
        watch_out("Moving only one point", "Whatever you do to the divisor, do to the dividend. They must stay in balance."),
        21,
    )

    c6 = concept_block(
        "6. Estimate, then compute",
        [
            "Estimation tells you if an exact answer is reasonable.",
            "49 × 21 is near 50 × 20 = 1,000. The exact product 1,029 sits close by.",
            "7.9 + 2.2 is near 8 + 2 = 10.",
            "If you get 102.9 for 49 × 21, the point (or a zero) is in the wrong place.",
            "Compatible numbers help division: 1,198 ÷ 25 is near 1,200 ÷ 25 = 48.",
            "Use rounding to a place that makes mental math easy, then go back for the exact value.",
        ],
        area_model(
            [50], [20],
            title="Estimate 49 × 21 as 50 × 20",
            caption="50 × 20 = 1,000. The exact product 1,029 sits close to that estimate.",
        )
        + solved(1, "Estimate 49 × 21, then decide if 1,029 is reasonable.",
               ["Round to 50 × 20 = 1,000.",
                "1,029 is close to 1,000.",
                "Yes — the exact product is reasonable."],
               "reasonable, near 1,000")
        + matching(
            [("49 × 21 near", "1,000"), ("7.9 + 2.2 near", "10"),
             ("1,198 ÷ 25 near", "48"), ("0.48 × 0.5 near", "0.25")],
            vid="g5u2-c6-match",
        ),
        try_this("Ask 'about how many?'", "If the story is about money or distance, an estimate can catch a point in the wrong place."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Multiply multi-digit whole numbers",
            "Divide with one- and two-digit divisors",
            "Add and subtract decimals",
            "Multiply decimals",
            "Divide decimals",
            "Estimate to check reasonableness",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u2_questions()


# ===========================================================================
# UNIT 3: Add and subtract unlike-denominator fractions
# ===========================================================================

def _u3_questions():
    qs = []
    idx = 1

    for text, ans, dist, expl in [
        ("1/2 = ?/6", "3", ["2", "4", "6"], "Multiply top and bottom by 3."),
        ("1/3 = ?/12", "4", ["3", "6", "9"], "×4 on top and bottom."),
        ("2/5 = ?/10", "4", ["2", "8", "5"], "×2: 4/10."),
        ("3/4 = ?/8", "6", ["3", "7", "8"], "×2: 6/8."),
        ("Which is equal to 2/3?", "4/6", ["3/4", "2/6", "5/6"], "×2 on top and bottom."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, dist, expl in [
        ("1/2 + 1/3 = ?", "5/6", ["2/5", "1/5", "2/6"], "3/6 + 2/6 = 5/6."),
        ("1/4 + 1/2 = ?", "3/4", ["2/6", "1/6", "2/4"], "1/4 + 2/4 = 3/4."),
        ("2/5 + 1/10 = ?", "1/2", ["3/15", "3/10", "2/10"], "4/10 + 1/10 = 5/10 = 1/2."),
        ("1/3 + 1/6 = ?", "1/2", ["2/9", "2/6", "1/9"], "2/6 + 1/6 = 3/6 = 1/2."),
        ("3/8 + 1/4 = ?", "5/8", ["4/12", "4/8", "1/8"], "3/8 + 2/8 = 5/8."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, dist, expl in [
        ("5/6 − 1/3 = ?", "1/2", ["4/3", "4/6", "1/6"], "5/6 − 2/6 = 3/6 = 1/2."),
        ("3/4 − 1/2 = ?", "1/4", ["2/2", "1/2", "2/4"], "3/4 − 2/4 = 1/4."),
        ("7/10 − 2/5 = ?", "3/10", ["5/5", "5/10", "9/10"], "7/10 − 4/10 = 3/10."),
        ("5/8 − 1/4 = ?", "3/8", ["4/4", "4/8", "6/8"], "5/8 − 2/8 = 3/8."),
        ("2/3 − 1/6 = ?", "1/2", ["1/3", "1/6", "3/6"], "4/6 − 1/6 = 3/6 = 1/2."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, dist, expl in [
        ("1 1/2 + 1 1/4 = ?", "2 3/4", ["2 1/4", "2 2/6", "3 3/4"], "1/2+1/4=3/4, plus 2 wholes."),
        ("2 1/3 + 1 1/6 = ?", "3 1/2", ["3 2/9", "3 1/6", "3 1/3"], "2/6+1/6=3/6=1/2, plus 3 wholes."),
        ("3 3/4 − 1 1/2 = ?", "2 1/4", ["2 2/2", "4 1/4", "2 1/2"], "3/4−2/4=1/4, plus 2 wholes."),
        ("4 − 1 2/5 = ?", "2 3/5", ["3 2/5", "5 2/5", "2 2/5"], "4 = 3 5/5. 3 5/5 − 1 2/5 = 2 3/5."),
        ("1 3/8 + 2 1/8 = ?", "3 1/2", ["3 4/8", "3 4/16", "4 1/2"], "3 + 4/8 = 3 1/2."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    more = [
        ("A common denominator for 1/4 and 1/6 is…", "12", ["10", "24 only", "8"], "12 is a common multiple of 4 and 6."),
        ("A common denominator for 1/3 and 1/5 is…", "15", ["8", "30 only", "10"], "3×5=15."),
        ("1/5 + 2/5 = ?", "3/5", ["3/10", "2/5", "1/5"], "Same bottoms: add tops."),
        ("1/2 + 1/4 + 1/4 = ?", "1", ["3/4", "1/8", "3/2"], "2/4+1/4+1/4=4/4=1."),
        ("Which is closer to 1: 5/6 or 2/3?", "5/6", ["2/3", "same", "1/2"], "5/6 is 1/6 from 1. 2/3 is 1/3 from 1."),
        ("Which is greater: 3/5 or 1/2?", "3/5", ["1/2", "same", "2/5"], "3/5=0.6, 1/2=0.5."),
        ("2/3 + 1/4 = ?", "11/12", ["3/7", "3/12", "2/12"], "8/12+3/12=11/12."),
        ("5/12 + 1/3 = ?", "3/4", ["6/15", "6/12", "5/15"], "5/12+4/12=9/12=3/4."),
        ("7/8 − 1/2 = ?", "3/8", ["6/6", "6/8", "8/8"], "7/8−4/8=3/8."),
        ("5/6 − 1/2 = ?", "1/3", ["4/4", "4/6", "1/6"], "5/6−3/6=2/6=1/3."),
        ("1/8 + 3/8 + 1/4 = ?", "3/4", ["5/8", "5/20", "1/2"], "1/8+3/8+2/8=6/8=3/4."),
        ("You walk 2/5 mile then 1/10 mile. Total?", "1/2 mile", ["3/15 mile", "3/10 mile", "2/10 mile"], "4/10+1/10=5/10=1/2."),
        ("A recipe needs 3/4 cup. You poured 1/3 cup. How much more?", "5/12 cup", ["2/1 cup", "2/12 cup", "4/7 cup"], "9/12−4/12=5/12."),
        ("1 2/3 + 2 1/2 = ?", "4 1/6", ["3 3/5", "3 1/6", "4 3/6"], "2/3+1/2=4/6+3/6=7/6=1 1/6, plus 3 wholes = 4 1/6."),
        ("Simplify 4/8.", "1/2", ["2/4 only", "4/4", "8/4"], "Divide top and bottom by 4."),
        ("Simplify 6/9.", "2/3", ["3/6", "6/6", "1/3"], "Divide by 3."),
        ("3/5 + 3/5 = ?", "6/5", ["6/10", "3/10", "1"], "6/5 = 1 1/5, but 6/5 is exact."),
        ("1 − 3/8 = ?", "5/8", ["3/8", "4/8", "1/8"], "8/8 − 3/8 = 5/8."),
        ("2/9 + 1/3 = ?", "5/9", ["3/12", "3/9", "1/6"], "2/9+3/9=5/9."),
        ("5/6 − 5/12 = ?", "5/12", ["0", "10/18", "5/6"], "10/12−5/12=5/12."),
    ]
    for text, ans, dist, expl in more:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"What is 1/{2 + (i % 5)} + 0? (the fraction itself)",
        f"1/{2 + (i % 5)}",
        "Adding 0 does not change the fraction.",
        i,
        distractors=["0", "1", f"{2 + (i % 5)}"],
    ))


def build_unit3():
    title = "Fifth Grade Math Unit 3: Add and Subtract Fractions"
    description = (
        "Find equivalent fractions and add or subtract fractions and mixed numbers with unlike denominators."
    )

    c1 = concept_block(
        "1. Equivalent fractions and common denominators",
        [
            "Equivalent fractions name the same amount: 1/2 = 2/4 = 3/6.",
            "To make an equivalent fraction, multiply (or divide) the top and the bottom by the same number.",
            "To add fractions with different bottoms, first make the bottoms match. That matching bottom is a common denominator.",
            "A common denominator is a common multiple of the two denominators. 4 and 6 both fit into 12.",
            "1/2 becomes 3/6 when you ×3. 1/3 becomes 2/6 when you ×2.",
            "Once bottoms match, you are ready to add or subtract the tops.",
        ],
        fraction_bars(
            [("1/2", 1, 2, "#6366f1"), ("3/6", 3, 6, "#6366f1"),
             ("1/3", 1, 3, "#f59e0b"), ("2/6", 2, 6, "#f59e0b")],
            "1/2 = 3/6 and 1/3 = 2/6. Same-size wholes, now both in sixths.",
        )
        + solved(1, "Write 1/2 and 1/3 with denominator 6.",
               ["1/2 × 3/3 = 3/6.",
                "1/3 × 2/2 = 2/6.",
                "Now both are sixths."],
               "3/6 and 2/6")
        + phet_box("frac_eq"),
        kid_tip("Same number, top and bottom", "Whatever you multiply the denominator by, multiply the numerator by too. The value stays put."),
        1,
    )

    c2 = concept_block(
        "2. Add unlike denominators",
        [
            "1/2 + 1/3 is not 2/5. You cannot add tops and bottoms as if they were two separate whole-number problems.",
            "Change to sixths: 3/6 + 2/6 = 5/6.",
            "The pieces must be the same size before you count how many you have.",
            "2/5 + 1/10 = 4/10 + 1/10 = 5/10, which simplifies to 1/2.",
            "Sometimes the sum is greater than 1: 3/5 + 3/5 = 6/5.",
            "Simplify when you can, but an unsimplified equivalent is still the same amount.",
        ],
        fraction_bars(
            [("1/2", 1, 2, "#6366f1"), ("1/3", 1, 3, "#f59e0b"), ("5/6", 5, 6, "#10b981")],
            "The two top bars together fill five of the six equal pieces on the bottom bar. 1/2 + 1/3 = 5/6.",
        )
        + solved(1, "Add 1/2 + 1/3.",
                 ["Common denominator 6.",
                  "1/2 = 3/6. 1/3 = 2/6.",
                  "3/6 + 2/6 = 5/6."],
                 "5/6"),
        watch_out("Adding the bottoms", "1/2 + 1/3 is not 2/5. Bottoms tell piece size. Only add the tops after the bottoms match."),
        6,
    )

    c3 = concept_block(
        "3. Subtract unlike denominators",
        [
            "Same idea as adding: make bottoms match, then subtract the tops.",
            "5/6 − 1/3 = 5/6 − 2/6 = 3/6 = 1/2.",
            "3/4 − 1/2 = 3/4 − 2/4 = 1/4.",
            "If you subtract from a whole, write 1 as a fraction with the needed bottom: 1 = 8/8, so 1 − 3/8 = 5/8.",
            "Check by adding the difference back to the number you subtracted. You should get the start.",
            "Keep the pieces the same size. 7/10 − 2/5 is 7/10 − 4/10, not 5/5.",
        ],
        fraction_bars(
            [("5/6", 5, 6, "#6366f1"), ("1/3", 1, 3, "#f59e0b"),
             ("2/6", 2, 6, "#f59e0b"), ("3/6 left", 3, 6, "#10b981")],
            "5/6 − 2/6 = 3/6, which is 1/2. Same-size sixths before you subtract.",
        )
        + solved(1, "Find 5/6 − 1/3.",
               ["1/3 = 2/6.",
                "5/6 − 2/6 = 3/6.",
                "3/6 = 1/2."],
               "1/2")
        + matching(
            [("3/4 − 1/2", "1/4"), ("7/8 − 1/2", "3/8"),
             ("5/6 − 1/2", "1/3"), ("1 − 3/8", "5/8")],
            vid="g5u3-c3-match",
        ),
        try_this("Add to check", "Difference + subtracted number should equal the starting number."),
        11,
    )

    c4 = concept_block(
        "4. Mixed numbers",
        [
            "A mixed number is wholes plus a leftover fraction: 1 1/2.",
            "Add wholes and fractions separately, then combine. 1 1/2 + 1 1/4 = (1+1) + (1/2+1/4) = 2 3/4.",
            "If the leftover fractions make more than a whole, regroup: 7/6 = 1 1/6.",
            "Subtracting mixed numbers may need regrouping. 4 − 1 2/5: write 4 as 3 5/5, then subtract.",
            "You can also write mixed numbers as improper fractions, compute, then convert back.",
            "Keep units in word problems: 2 1/3 cups plus 1 1/6 cups is 3 1/2 cups.",
        ],
        fraction_bars(
            [("1/2", 1, 2, "#6366f1"), ("1/4", 1, 4, "#f59e0b"), ("3/4", 3, 4, "#10b981")],
            "The leftover parts: 1/2 + 1/4 = 3/4. Add the two wholes to get 2 3/4.",
        )
        + solved(1, "Add 1 1/2 + 1 1/4.",
               ["Wholes: 1 + 1 = 2.",
                "Fractions: 1/2 + 1/4 = 2/4 + 1/4 = 3/4.",
                "Together: 2 3/4."],
               "2 3/4")
        + phet_box("frac_mixed"),
        kid_tip("Wholes, then parts", "Park the whole numbers. Make the fraction bottoms match. Then put the pile back together."),
        16,
    )

    c5 = concept_block(
        "5. Fraction stories",
        [
            "Read the story. Are you joining amounts (add) or taking away / comparing (subtract)?",
            "A walk of 2/5 mile then 1/10 mile is 4/10 + 1/10 = 1/2 mile.",
            "A recipe needs 3/4 cup. You poured 1/3 cup. How much more? 3/4 − 1/3 = 9/12 − 4/12 = 5/12 cup.",
            "Write the equation before you compute. The numbers should match the story.",
            "Label the answer with the unit: miles, cups, hours.",
            "If both numbers are mixed, keep them mixed or convert — pick one path and stay on it.",
        ],
        fraction_bars(
            [("3/4", 9, 12, "#6366f1"), ("1/3", 4, 12, "#f59e0b"), ("need", 5, 12, "#10b981")],
            "3/4 = 9/12 and 1/3 = 4/12. You still need 5/12 cup.",
        )
        + solved(1, "You need 3/4 cup of milk. You poured 1/3 cup. How much more?",
               ["This is subtract: 3/4 − 1/3.",
                "Common denominator 12.",
                "9/12 − 4/12 = 5/12."],
               "5/12 cup")
        + step_reveal(
            ["Underline the question.",
             "Decide add or subtract.",
             "Write the fractions.",
             "Common denominator, then compute.",
             "Label the unit."],
            vid="g5u3-c5-steps",
        ),
        try_this("Sketch the cups", "A quick bar for 3/4 and a bar for 1/3 makes the leftover visible."),
        21,
    )

    c6 = concept_block(
        "6. Benchmarks: 0, 1/2, and 1",
        [
            "Benchmarks help you judge size without a calculator.",
            "A fraction is near 0 when the top is much smaller than the bottom: 1/8.",
            "Near 1/2: top is about half the bottom: 3/7, 5/10, 4/9.",
            "Near 1: top is close to the bottom: 5/6, 7/8, 9/10.",
            "5/6 is closer to 1 than 2/3 is, because 5/6 is only 1/6 away and 2/3 is 1/3 away.",
            "Use benchmarks to check whether a sum like 1/2 + 1/3 ≈ 0.8 makes sense (yes, 5/6).",
        ],
        decimal_number_line(
            0, 1,
            marks=[(0, "0"), (0.5, "1/2"), (2 / 3, "2/3"), (5 / 6, "5/6"), (1, "1")],
            tick_step=0.5,
            title="Benchmarks 0, 1/2, and 1",
            caption="5/6 is only 1/6 from 1. 2/3 is 1/3 from 1. So 5/6 is closer to 1.",
        )
        + solved(1, "Which is closer to 1: 5/6 or 2/3?",
               ["Distance from 1: 1 − 5/6 = 1/6.",
                "1 − 2/3 = 1/3.",
                "1/6 is smaller, so 5/6 is closer to 1."],
               "5/6")
        + matching(
            [("1/8", "near 0"), ("3/7", "near 1/2"), ("7/8", "near 1"), ("4/9", "near 1/2")],
            vid="g5u3-c6-match",
        ),
        watch_out("Bigger bottom means bigger fraction", "1/8 is smaller than 1/2. More pieces means each piece is smaller."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Make equivalent fractions",
            "Add unlike denominators",
            "Subtract unlike denominators",
            "Work with mixed numbers",
            "Solve fraction stories",
            "Use 0, 1/2, and 1 as benchmarks",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u3_questions()


# ===========================================================================
# UNIT 4: Multiply fractions
# ===========================================================================

def _u4_questions():
    qs = []
    idx = 1

    for text, ans, dist, expl in [
        ("3 × 2/5 = ?", "6/5", ["6/15", "5/6", "2/15"], "3 groups of 2/5 is 6/5."),
        ("4 × 1/3 = ?", "4/3", ["4/12", "1/12", "5/3"], "4 thirds."),
        ("5 × 3/4 = ?", "15/4", ["8/4", "15/20", "3/20"], "5 groups of 3/4."),
        ("1/2 of 8 = ?", "4", ["16", "2", "8"], "Half of 8 is 4."),
        ("1/4 of 12 = ?", "3", ["48", "8", "16"], "12÷4=3."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, dist, expl in [
        ("2/3 × 4/5 = ?", "8/15", ["6/8", "8/8", "6/15"], "Multiply tops, multiply bottoms."),
        ("1/2 × 1/4 = ?", "1/8", ["1/6", "2/6", "1/4"], "A half of a fourth is an eighth."),
        ("3/4 × 2/5 = ?", "6/20", ["5/9", "6/9", "5/20"], "6/20 = 3/10 after simplify. 6/20 is exact."),
        ("1/3 × 1/5 = ?", "1/15", ["2/8", "1/8", "2/15"], "One of 15 equal parts."),
        ("2/5 × 5/6 = ?", "1/3", ["10/11", "7/30", "2/6"], "10/30 = 1/3."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, dist, expl in [
        ("A 1/2 by 1/3 rectangle has area…", "1/6", ["2/5", "1/5", "1/3"], "Area = length × width = 1/6."),
        ("A 2/3 by 3/4 rectangle has area…", "1/2", ["5/7", "6/7", "5/12"], "6/12 = 1/2."),
        ("A 4 by 1/2 rectangle has area…", "2", ["4.5", "8", "1/2"], "4 half-units make 2."),
        ("If you take 1/2 of 1/2 of a pan, you have…", "1/4", ["1", "1/2", "2/2"], "Half of a half."),
        ("3/4 of a 2-by-1 rectangle (area 2) is…", "3/2", ["5/4", "3/4", "6/4 as 6"], "3/4 × 2 = 6/4 = 3/2."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, dist, expl in [
        ("1/2 × 8 compared with 8 is…", "smaller", ["larger", "equal", "8 times as big"], "A factor less than 1 shrinks."),
        ("3 × 2/5 compared with 2/5 is…", "larger", ["smaller", "equal", "always 1"], "A whole-number factor greater than 1 stretches."),
        ("4/4 × 7/8 = ?", "7/8", ["28/8", "11/8", "1"], "4/4 is 1, so the product is unchanged."),
        ("1/5 of a number is less than the number when the number is…", "greater than 0", ["zero only", "negative only", "always 5"], "A proper fraction of a positive amount is smaller."),
        ("2/3 × 9 = ?", "6", ["18/3 as 27", "11/3", "2"], "2/3 of 9 is 6."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    more = [
        ("1 1/2 × 4 = ?", "6", ["5 1/2", "4 1/2", "8"], "Three halves × 4 = 12/2 = 6."),
        ("2 1/3 × 3 = ?", "7", ["6 1/3", "5", "8"], "7/3 × 3 = 7."),
        ("1/2 × 1 1/2 = ?", "3/4", ["2/2", "1", "1/4"], "1/2 × 3/2 = 3/4."),
        ("A recipe for 6 is cut in half. 3/4 cup becomes…", "3/8 cup", ["3/2 cup", "6/4 cup", "1/4 cup"], "1/2 × 3/4 = 3/8."),
        ("You have 12 stickers. You give away 2/3. How many given?", "8", ["4", "6", "10"], "2/3 of 12 = 8."),
        ("You have 12 stickers. You keep 1/3. How many kept?", "4", ["8", "3", "9"], "1/3 of 12 = 4."),
        ("5/6 × 2/5 = ?", "1/3", ["7/11", "10/30 as 10", "2/6"], "10/30 = 1/3."),
        ("3/8 × 4/9 = ?", "1/6", ["7/17", "12/17", "12/72 as 12"], "12/72 = 1/6."),
        ("7 × 1/7 = ?", "1", ["7", "1/49", "8/7"], "7 sevenths make 1."),
        ("0 × 3/4 = ?", "0", ["3/4", "1", "3"], "Zero groups is zero."),
        ("2/2 × 5/9 = ?", "5/9", ["10/9", "7/11", "1"], "2/2 = 1."),
        ("3/5 of 20 = ?", "12", ["15", "8", "23"], "3/5 × 20 = 12."),
        ("1/8 of 32 = ?", "4", ["8", "3", "40"], "32÷8=4."),
        ("4/5 × 10 = ?", "8", ["40/5 as 50", "14/5", "4"], "40/5 = 8."),
        ("A 1/4-mile track, run 3 times: distance?", "3/4 mile", ["3/4 as 3", "1/12 mile", "4/3 mile"], "3 × 1/4 = 3/4."),
        ("Simplify 6/20.", "3/10", ["6/10", "3/20", "1/4"], "Divide by 2."),
        ("2/7 × 7/2 = ?", "1", ["4/9", "9/14", "4/14"], "Tops and bottoms cancel to 1."),
        ("1 1/4 × 2/5 = ?", "1/2", ["3/9", "2/9", "7/4"], "5/4 × 2/5 = 10/20 = 1/2."),
        ("3 × 1 2/3 = ?", "5", ["4 2/3", "3 2/3", "6"], "3 × 5/3 = 5."),
        ("Half of 2/3 is…", "1/3", ["3/5", "1/6", "4/3"], "1/2 × 2/3 = 1/3."),
    ]
    for text, ans, dist, expl in more:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"What is 1/2 of {2 * (i % 10 + 1)}?",
        str(i % 10 + 1),
        "Half of an even number is that number divided by 2.",
        i,
        distractors=[str(2 * (i % 10 + 1)), str(i % 10 + 3), "0"],
    ))


def build_unit4():
    title = "Fifth Grade Math Unit 4: Multiply Fractions"
    description = (
        "Multiply whole numbers by fractions, fractions by fractions, and mixed numbers. Use area and scaling."
    )

    c1 = concept_block(
        "1. A whole number times a fraction",
        [
            "3 × 2/5 means three groups of two-fifths, which is 6/5.",
            "You can think of it as (3 × 2)/5.",
            "1/2 of 8 is the same as 1/2 × 8. Half of 8 is 4.",
            "Of often means multiply: 1/4 of 12 = 3.",
            "A whole number greater than 1 makes a proper fraction grow (unless the fraction is 0).",
            "Write mixed when it helps: 6/5 = 1 1/5, but 6/5 is a fine exact answer.",
        ],
        fraction_bars(
            [("group 1", 2, 5, "#6366f1"), ("group 2", 2, 5, "#6366f1"),
             ("group 3", 2, 5, "#6366f1")],
            "Three groups of 2/5 is 6/5.",
        )
        + solved(1, "Find 3 × 2/5.",
               ["Three groups of 2 fifths is 6 fifths.",
                "6/5.",
                "That is also 1 1/5."],
               "6/5")
        + matching(
            [("1/2 of 8", "4"), ("1/4 of 12", "3"), ("3 × 1/5", "3/5"), ("5 × 1/5", "1")],
            vid="g5u4-c1-match",
        ),
        kid_tip("'Of' means ×", "1/3 of 15 is 1/3 × 15. Split 15 into 3 equal parts."),
        1,
    )

    c2 = concept_block(
        "2. A fraction times a fraction",
        [
            "Multiply the numerators. Multiply the denominators. 2/3 × 4/5 = 8/15.",
            "A picture: take 2/3 of a bar, then take 4/5 of that piece.",
            "1/2 × 1/4 = 1/8. Half of a fourth is an eighth.",
            "You may simplify before or after. 2/5 × 5/6 = 10/30 = 1/3.",
            "Crossing out common factors is just simplifying early: the 5s in 2/5 × 5/6.",
            "The product of two proper fractions is smaller than either factor.",
        ],
        fraction_area_model(
            2, 3, 4, 5,
            title="Area model for 2/3 × 4/5",
            caption="A 3-by-5 grid. Shade 2 of 3 rows and 4 of 5 columns. The overlap is 8/15.",
        )
        + solved(1, "Find 2/3 × 4/5.",
               ["Tops: 2 × 4 = 8.",
                "Bottoms: 3 × 5 = 15.",
                "Product: 8/15."],
               "8/15")
        + step_reveal(
            ["Write the two fractions.",
             "Multiply tops.",
             "Multiply bottoms.",
             "Simplify if you can."],
            vid="g5u4-c2-steps",
        ),
        watch_out("Adding instead of multiplying", "2/3 × 4/5 is not 6/8. Multiplication of fractions is tops×tops and bottoms×bottoms."),
        6,
    )

    c3 = concept_block(
        "3. Area with fractional sides",
        [
            "Area of a rectangle is length × width, even when the sides are fractions.",
            "A 1/2-by-1/3 rectangle has area 1/6 square unit.",
            "Imagine a 1-by-1 square. Cut it into a 2-by-3 grid. One cell is 1/6.",
            "A 2/3-by-3/4 rectangle has area 6/12 = 1/2 square unit.",
            "This is why fraction multiplication shows up in measurement, not only in 'naked' number problems.",
            "Units: if sides are in inches, area is in square inches.",
        ],
        fraction_area_model(
            1, 2, 1, 3,
            title="A 1/2-by-1/3 rectangle",
            caption="Split a unit square into a 2-by-3 grid. One cell is 1/6 square unit.",
        )
        + solved(1, "A rectangle is 1/2 unit by 1/3 unit. What is its area?",
               ["Area = length × width.",
                "1/2 × 1/3 = 1/6.",
                "One-sixth square unit."],
               "1/6 square unit")
        + try_this("Draw the unit square", "Sketch a square, split it into the denominator grid, and shade the product cell."),
        11,
    )

    c4 = concept_block(
        "4. Scaling: shrinking and stretching",
        [
            "Multiplying by a number greater than 1 stretches. Multiplying by a number between 0 and 1 shrinks.",
            "1/2 × 8 = 4, which is smaller than 8.",
            "3 × 2/5 = 6/5, which is larger than 2/5.",
            "Multiplying by 1 (or 4/4, or 7/7) leaves the amount the same.",
            "This is the idea of scaling, which you will use again in middle-school ratios.",
            "Ask: is my factor more than 1, equal to 1, or less than 1? Then predict bigger, same, or smaller.",
        ],
        lesson_figure(
            svg_dots(8, color="#6366f1", label="8")
            + svg_dots(4, color="#10b981", label="1/2 × 8 = 4"),
            "Scaling: 1/2 × 8 shrinks 8 to 4",
            "A factor less than 1 makes a positive amount smaller.",
        )
        + solved(1, "Is 1/2 × 8 smaller or larger than 8?",
               ["1/2 is less than 1.",
                "A factor less than 1 shrinks a positive number.",
                "4 is smaller than 8."],
               "smaller")
        + matching(
            [("× 3", "stretches"), ("× 1/4", "shrinks"), ("× 1", "stays"), ("× 5/5", "stays")],
            vid="g5u4-c4-match",
        ),
        kid_tip("Predict first", "Before you compute, say bigger, smaller, or the same. Then see if the product agrees."),
        16,
    )

    c5 = concept_block(
        "5. Mixed numbers and multiplication",
        [
            "Write the mixed number as an improper fraction, then multiply.",
            "1 1/2 × 4 = 3/2 × 4/1 = 12/2 = 6.",
            "1/2 × 1 1/2 = 1/2 × 3/2 = 3/4.",
            "You can also distribute: 1 1/2 × 4 = (1×4) + (1/2×4) = 4 + 2 = 6.",
            "Distribution is handy when one factor is a whole number.",
            "Simplify at the end. Check with an estimate: 1 1/2 × 4 is a little more than 4, actually 6.",
        ],
        lesson_figure(
            svg_tape([1, 1, 1, 1], ["1½", "1½", "1½", "1½"]),
            "Four copies of 1 1/2",
            "1 1/2 four times is 6. Or: 4 wholes + 4 halves = 4 + 2 = 6.",
        )
        + solved(1, "Find 1 1/2 × 4.",
               ["1 1/2 = 3/2.",
                "3/2 × 4/1 = 12/2 = 6.",
                "Or: 4 wholes plus 4 halves = 4+2=6."],
               "6")
        + phet_box("build_frac"),
        try_this("Distribute the whole", "a b/c × n = (a×n) + (b/c × n). Two smaller products, then add."),
        21,
    )

    c6 = concept_block(
        "6. Multiply-fraction stories",
        [
            "A recipe for 6 cut in half: every amount is × 1/2. 3/4 cup becomes 3/8 cup.",
            "You have 12 stickers and give away 2/3 of them: 2/3 × 12 = 8 stickers given.",
            "A 1/4-mile track, run 3 times: 3 × 1/4 = 3/4 mile.",
            "Write 'of' as multiplication when a fraction acts on a quantity.",
            "Keep the unit in the answer so the story still makes sense.",
            "If you keep 1/3 of 12, that is the leftover after giving 2/3 — a useful check: 4 + 8 = 12.",
        ],
        fraction_area_model(
            1, 2, 3, 4,
            title="Half of 3/4 cup",
            caption="1/2 × 3/4: a 2-by-4 grid, overlap 3/8. That is the half-recipe amount.",
        )
        + solved(1, "A recipe uses 3/4 cup. You make half the recipe. How much do you use?",
               ["Half the recipe means × 1/2.",
                "1/2 × 3/4 = 3/8.",
                "3/8 cup."],
               "3/8 cup")
        + step_reveal(
            ["Find the quantity.",
             "Find the fraction (or whole number) acting on it.",
             "Write a multiplication.",
             "Compute and label."],
            vid="g5u4-c6-steps",
        ),
        watch_out("Halving by subtracting 1/2", "Half of 3/4 is not 3/4 − 1/2. Half means multiply by 1/2."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Multiply a whole number by a fraction",
            "Multiply a fraction by a fraction",
            "Find area with fractional sides",
            "See scaling (shrink and stretch)",
            "Multiply mixed numbers",
            "Solve multiply-fraction stories",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u4_questions()
