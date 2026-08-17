"""Second Grade Math units 5–8: time, money, geometry, fractions, plus master page."""

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
    page_break,
    mq,
    renumber,
)


def _fill(qs, need, factory):
    while len(qs) < need:
        qs.append(factory(len(qs) + 1))
    return renumber(qs[:need])


# ===========================================================================
# UNIT 5: Time to the nearest five minutes
# ===========================================================================

def _u5_questions():
    qs = []
    idx = 1

    hands = [
        ("The short hand on a clock tells the…", "hour",
         "The short hand is the hour hand.", ["minute", "second", "day"]),
        ("The long hand on a clock tells the…", "minute",
         "The long hand is the minute hand.", ["hour", "year", "week"]),
        ("When the long hand points to 12, the time is __ o'clock.", "something",
         "Long hand on 12 means 0 minutes. It is an hour time, like 3:00.", ["half past", "quarter past", "quarter to"]),
        ("There are how many minutes in one hour?", 60,
         "A clock is 60 minutes around. 12 numbers × 5 minutes = 60.", ["12", "24", "100"]),
        ("The numbers on a clock go from 1 to…", 12,
         "A clock face has 12 hour marks.", ["10", "24", "60"]),
    ]
    # Fix the third question - "something" is a bad answer. Let me use "o'clock"
    hands[2] = (
        "When the long hand points to 12, the minutes are…",
        0,
        "Long hand on 12 means 0 minutes. The time is __:00.",
        ["15", "30", "45"],
    )
    for text, ans, expl, dist in hands:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    by_fives = [
        ("The long hand on 1 means how many minutes?", 5, "Each number is 5 minutes. 1 × 5 = 5."),
        ("The long hand on 2 means how many minutes?", 10, "2 × 5 = 10 minutes."),
        ("The long hand on 3 means how many minutes?", 15, "3 × 5 = 15. That is a quarter hour."),
        ("The long hand on 6 means how many minutes?", 30, "6 × 5 = 30. That is half past."),
        ("The long hand on 9 means how many minutes?", 45, "9 × 5 = 45. A quarter to the next hour."),
        ("The long hand on 4 means how many minutes?", 20, "4 × 5 = 20."),
        ("The long hand on 5 means how many minutes?", 25, "5 × 5 = 25."),
        ("The long hand on 8 means how many minutes?", 40, "8 × 5 = 40."),
        ("The long hand on 10 means how many minutes?", 50, "10 × 5 = 50."),
        ("The long hand on 11 means how many minutes?", 55, "11 × 5 = 55."),
    ]
    for text, ans, expl in by_fives:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    times = [
        ("Short hand on 3, long hand on 12. What time?", "3:00",
         "Hour 3, 0 minutes. 3:00.", ["3:12", "12:03", "3:30"]),
        ("Short hand a little past 4, long hand on 6. What time?", "4:30",
         "Long hand on 6 is 30 minutes. Half past 4 is 4:30.", ["4:06", "6:04", "4:00"]),
        ("Short hand past 2, long hand on 3. What time?", "2:15",
         "Long hand on 3 is 15 minutes. 2:15.", ["2:03", "3:10", "2:30"]),
        ("Short hand near 7, long hand on 9. What time?", "6:45",
         "Long hand on 9 is 45 minutes. The hour is still 6 until 7:00. 6:45.", ["7:45", "9:06", "6:09"]),
        ("Short hand past 10, long hand on 4. What time?", "10:20",
         "4 × 5 = 20 minutes. 10:20.", ["10:04", "4:10", "10:40"]),
        ("What time is 15 minutes after 3:00?", "3:15",
         "3:00 plus 15 minutes is 3:15.", ["3:50", "4:15", "2:15"]),
        ("What time is 5 minutes after 1:20?", "1:25",
         "Count 5 more minutes. 1:25.", ["1:30", "1:15", "2:25"]),
        ("What time is 5 minutes before 8:00?", "7:55",
         "Back 5 minutes from 8:00 is 7:55.", ["8:05", "7:50", "8:55"]),
        ("Half past 9 is…", "9:30",
         "Half an hour is 30 minutes. 9:30.", ["9:15", "9:45", "8:30"]),
        ("Quarter past 5 is…", "5:15",
         "A quarter of 60 minutes is 15. 5:15.", ["5:30", "5:45", "5:00"]),
        ("Quarter to 2 is…", "1:45",
         "Quarter to 2 means 15 minutes before 2:00, which is 1:45.", ["2:15", "2:45", "1:15"]),
        ("The clock shows 11:50. In 10 minutes it will be…", "12:00",
         "11:50 + 10 minutes = 12:00.", ["11:60", "12:50", "11:40"]),
    ]
    for text, ans, expl, dist in times:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    ampm = [
        ("Breakfast time is usually…", "AM",
         "AM is morning, from midnight to noon.", ["PM", "noon only", "midnight only"]),
        ("After-school soccer at 4:00 is…", "PM",
         "Afternoon and evening are PM.", ["AM", "noon", "midnight"]),
        ("Noon is 12:00…", "PM",
         "12:00 noon starts PM. Midnight is 12:00 AM.", ["AM", "neither", "both"]),
        ("A clock showing 7:00 could be morning or evening. Morning 7:00 is…", "AM",
         "7:00 in the morning is 7:00 AM.", ["PM", "noon", "none"]),
        ("Lights-out at 8:00 at night is…", "PM",
         "Night is PM (until midnight).", ["AM", "noon", "morning"]),
    ]
    for text, ans, expl, dist in ampm:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    elapsed = [
        ("A show starts at 2:00 and lasts 1 hour. When does it end?", "3:00",
         "2:00 plus 60 minutes is 3:00.", ["2:60", "1:00", "2:01"]),
        ("You start at 4:10 and play for 15 minutes. What time do you stop?", "4:25",
         "4:10 + 15 = 4:25.", ["4:15", "4:35", "5:10"]),
        ("Recess is 20 minutes. It starts at 10:05. When does it end?", "10:25",
         "10:05 + 20 minutes = 10:25.", ["10:15", "10:45", "11:05"]),
        ("A bus ride is 30 minutes. It leaves at 8:00. Arrival time?", "8:30",
         "8:00 + 30 = 8:30.", ["8:03", "9:00", "7:30"]),
        ("From 1:45 to 2:00 is how many minutes?", 15,
         "From 45 to 60 is 15 minutes.", ["45", "5", "30"]),
        ("From 3:20 to 3:35 is how many minutes?", 15,
         "Count by fives: 20, 25, 30, 35. That is 15 minutes.", ["5", "10", "20"]),
        ("From 6:00 to 6:05 is how many minutes?", 5,
         "One jump of 5 minutes.", ["1", "10", "60"]),
        ("A class is 45 minutes. It starts at 9:00. When does it end?", "9:45",
         "9:00 + 45 minutes is 9:45.", ["9:15", "10:00", "8:45"]),
    ]
    for text, ans, expl, dist in elapsed:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    # more five-minute times
    for hour, num in [(1, 2), (2, 5), (3, 8), (4, 1), (5, 7), (6, 10), (8, 3), (9, 6), (11, 4), (12, 9)]:
        mins = num * 5
        clock = f"{hour}:{mins:02d}"
        qs.append(mq(
            f"Short hand near {hour}, long hand on {num}. What time?",
            clock,
            f"Minute hand on {num} means {mins} minutes. The time is {clock}.",
            idx,
            distractors=[f"{hour}:{num:02d}", f"{num}:{hour:02d}", f"{hour}:{(mins + 5) % 60:02d}"],
        ))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"The long hand is on {1 + (i % 11)}. How many minutes is that?",
        (1 + (i % 11)) * 5,
        f"Each number is 5 minutes. {1 + (i % 11)} × 5 = {(1 + (i % 11)) * 5}.",
        i,
    ))


def build_unit5():
    title = "Second Grade Math Unit 5: Time to Five Minutes"
    description = (
        "Read analog clocks to the nearest five minutes, use half past and quarter times, AM/PM, and simple elapsed time."
    )

    c1 = concept_block(
        "1. Hour hand and minute hand",
        [
            "A clock has a short hand and a long hand.",
            "The short hand tells the hour. It moves slowly from number to number.",
            "The long hand tells the minutes. It moves all the way around in 60 minutes.",
            "When the long hand is on 12, the minutes are 00. We say o'clock: 4:00 is four o'clock.",
            "The short hand also creeps forward as minutes pass. At 4:30 it sits between 4 and 5.",
            "Read the hour first from the short hand, then the minutes from the long hand.",
        ],
        lesson_figure(
            svg_clock(2, 0),
            "Short hand on 2, long hand on 12",
            "The short hand names the hour 2. The long hand on 12 means 0 minutes. The time is 2:00.",
        )
        + solved(1, "Short hand on 2, long hand on 12. What time?",
               ["Short hand on 2 → hour is 2.",
                "Long hand on 12 → 0 minutes.",
                "2:00."],
               "2:00")
        + matching(
            [("short hand", "hour"), ("long hand", "minute"),
             ("long hand on 12", "00 minutes"), ("clock numbers", "1 to 12")],
            vid="g2u5-c1-match",
        ),
        kid_tip("Short then long", "Say the hour from the short hand first. Then count minutes from the long hand."),
        1,
    )

    c2 = concept_block(
        "2. Count by fives around the clock",
        [
            "Each number the long hand points to is worth 5 minutes.",
            "1 → 5, 2 → 10, 3 → 15, 4 → 20, 5 → 25, 6 → 30, 7 → 35, 8 → 40, 9 → 45, 10 → 50, 11 → 55, 12 → 00.",
            "Skip-count by 5s as you hop from number to number.",
            "This is why second grade skip-counts by 5s. Clocks need it.",
            "Marks between numbers are 1 minute each, but we read to the nearest five minutes here.",
            "If the long hand is on 8, do not say 8 minutes. Say 40 minutes.",
        ],
        lesson_figure(
            svg_clock(3, 20),
            "Long hand on 4",
            "Each number is 5 minutes. Count 5, 10, 15, 20. The 4 means 20 minutes.",
        )
        + solved(1, "The long hand points to 4. How many minutes?",
               ["Count by fives: 5, 10, 15, 20.",
                "Number 4 means 20 minutes."],
               "20")
        + solved(2, "The long hand points to 7. How many minutes?",
                 ["5, 10, 15, 20, 25, 30, 35.",
                  "Number 7 means 35 minutes."],
                 "35")
        + step_reveal(
            ["Put your finger on 12. That is 0 minutes.",
             "Hop to 1 and say 5.",
             "Hop to 2 and say 10.",
             "Keep hopping by 5s until you land on the minute hand."],
            vid="g2u5-c2-steps",
        ),
        watch_out("Reading the minute number as minutes",
                  "The 3 is not 3 minutes. It is 15 minutes. Multiply the number by 5."),
        6,
    )

    c3 = concept_block(
        "3. Time to five minutes",
        [
            "To write the time: hour, colon, two-digit minutes.",
            "If minutes are 5, write :05, not :5. We use two minute digits.",
            "At 10:20 the short hand sits a little past 10. The long hand is on 4 (20 minutes).",
            "When minutes are 45 or more, the short hand looks close to the next hour. The hour is still the one it just passed.",
            "6:45 is not 7:45. The hour becomes 7 only at 7:00.",
            "Practice saying times two ways: 4:20 and twenty minutes past 4.",
        ],
        lesson_figure(
            svg_clock(10, 20),
            "10:20",
            "The hour is still 10. The long hand on 4 is 20 minutes, so the time is 10:20.",
        )
        + solved(1, "Short hand past 10, long hand on 4. What time?",
               ["Hour is 10 (it has not reached 11).",
                "Minute number 4 → 20 minutes.",
                "10:20."],
               "10:20")
        + solved(2, "Short hand near 7, long hand on 9. What time?",
                 ["Long hand on 9 → 45 minutes.",
                  "The short hand is close to 7, so the hour is still 6.",
                  "6:45."],
                 "6:45")
        + matching(
            [("long hand on 1", "5 minutes"), ("long hand on 5", "25 minutes"),
             ("2:15", "quarter past 2"), ("11:50", "10 minutes to 12")],
            vid="g2u5-c3-match",
        ),
        try_this("Write the colon", "Always two minute digits: 1:05, 1:10, 1:15. That keeps 5 from looking like 50."),
        11,
    )

    c4 = concept_block(
        "4. Half past, quarter past, quarter to",
        [
            "Half past means 30 minutes. The long hand is on 6. Half past 9 is 9:30.",
            "Quarter past means 15 minutes. The long hand is on 3. Quarter past 5 is 5:15.",
            "Quarter to means 15 minutes before the next hour. The long hand is on 9. Quarter to 2 is 1:45.",
            "A quarter of 60 is 15. Two quarters are 30. Three quarters are 45.",
            "These names are shortcuts. You can always say the digital time instead.",
            "Quarter to is the one kids mix up. Think: almost the next hour, minus 15 minutes.",
        ],
        lesson_figure(
            svg_clock(4, 30),
            "Half past 4",
            "Half past means 30 minutes, so the long hand sits on 6. Half past 4 is 4:30.",
        )
        + solved(1, "What time is half past 4?",
               ["Half past → 30 minutes.",
                "Hour 4. Write 4:30."],
               "4:30")
        + solved(2, "What time is quarter to 2?",
                 ["Quarter to 2 is 15 minutes before 2:00.",
                  "2:00 minus 15 minutes is 1:45."],
                 "1:45")
        + matching(
            [("half past 8", "8:30"), ("quarter past 1", "1:15"),
             ("quarter to 6", "5:45"), ("o'clock 12", "12:00")],
            vid="g2u5-c4-match",
        ),
        kid_tip("Hand on 6, 3, 9", "6 → half past. 3 → quarter past. 9 → quarter to."),
        16,
    )

    c5 = concept_block(
        "5. AM and PM",
        [
            "A clock face does not tell morning from night by itself. We use AM and PM.",
            "AM is from midnight to just before noon. Breakfast, school start, and morning recess are AM.",
            "PM is from noon to just before midnight. Lunch after noon, afternoon, evening, and night are PM.",
            "12:00 noon is 12:00 PM. 12:00 midnight is 12:00 AM.",
            "7:00 could be waking up (AM) or dinner time (PM). The story tells you which.",
            "Write the letters after the time: 8:15 AM.",
        ],
        lesson_figure(
            svg_clock(4, 0),
            "4:00 after school",
            "The clock shows 4:00. After school is afternoon, so soccer practice is 4:00 PM.",
        )
        + solved(1, "Soccer practice at 4:00 after school. AM or PM?",
               ["After school is afternoon.",
                "Afternoon is PM."],
               "PM")
        + solved(2, "The bus comes at 7:30 in the morning. AM or PM?",
                 ["Morning is AM.",
                  "7:30 AM."],
                 "AM")
        + watch_out("Thinking 12:00 is always midnight",
                    "Noon and midnight both say 12:00. Noon is PM. Midnight is AM."),
        21,
    )

    c6 = concept_block(
        "6. How much time passed?",
        [
            "Elapsed time is how long something lasted.",
            "If you start at 4:10 and stop at 4:25, count by fives: 10 to 15 to 20 to 25. That is 15 minutes.",
            "If a show is 1 hour from 2:00, it ends at 3:00.",
            "When minutes pass 60, the hour ticks forward. 11:50 + 10 minutes = 12:00, not 11:60.",
            "Draw a tiny clock or a number line of minutes if counting in your head is messy.",
            "Start time + duration = end time. End time − start time = duration.",
        ],
        lesson_figure(
            svg_clock(10, 25),
            "Recess ends at 10:25",
            "Start at 10:05 and count 20 minutes by fives: 10:10, 10:15, 10:20, 10:25.",
        )
        + solved(1, "Recess starts at 10:05 and lasts 20 minutes. When does it end?",
               ["Count 20 minutes from 10:05.",
                "10:05, 10:10, 10:15, 10:20, 10:25.",
                "It ends at 10:25."],
               "10:25")
        + solved(2, "From 1:45 to 2:00, how many minutes pass?",
                 ["From 45 to 60 is 15 minutes.",
                  "The hour changes to 2:00 at 60 minutes."],
                 "15")
        + step_reveal(
            ["Mark the start time.",
             "Skip-count by 5s until you reach the end time.",
             "Each hop is 5 minutes. Count the hops.",
             "Hops × 5 is the elapsed time."],
            vid="g2u5-c6-steps",
        ),
        try_this("Never write :60", "There is no 11:60. After 11:55 comes 12:00."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Name the hour hand and the minute hand",
            "Count by 5s around the clock",
            "Read time to the nearest five minutes",
            "Use half past, quarter past, and quarter to",
            "Choose AM or PM",
            "Find simple elapsed time",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u5_questions()


# ===========================================================================
# UNIT 6: Counting money
# ===========================================================================

def _u6_questions():
    qs = []
    idx = 1

    coins = [
        ("A penny is worth how many cents?", 1, "A penny = 1¢.", None),
        ("A nickel is worth how many cents?", 5, "A nickel = 5¢.", None),
        ("A dime is worth how many cents?", 10, "A dime = 10¢.", None),
        ("A quarter is worth how many cents?", 25, "A quarter = 25¢.", None),
        ("A dollar is worth how many cents?", 100, "One dollar = 100 cents.", None),
        ("How many pennies equal 1 nickel?", 5, "5 pennies = 1 nickel.", None),
        ("How many nickels equal 1 dime?", 2, "2 nickels = 10¢ = 1 dime.", None),
        ("How many dimes equal 1 dollar?", 10, "10 × 10¢ = 100¢ = $1.", None),
        ("How many quarters equal 1 dollar?", 4, "4 × 25¢ = 100¢ = $1.", None),
        ("How many nickels equal 1 quarter?", 5, "5 × 5¢ = 25¢.", None),
    ]
    for text, ans, expl, dist in coins:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    counts = [
        ("3 dimes. How many cents?", 30, "3 × 10 = 30 cents."),
        ("4 nickels. How many cents?", 20, "4 × 5 = 20 cents."),
        ("2 quarters. How many cents?", 50, "2 × 25 = 50 cents."),
        ("1 quarter and 1 dime. How many cents?", 35, "25 + 10 = 35 cents."),
        ("1 quarter, 1 dime, 1 nickel. How many cents?", 40, "25 + 10 + 5 = 40 cents."),
        ("2 dimes and 3 pennies. How many cents?", 23, "20 + 3 = 23 cents."),
        ("3 quarters. How many cents?", 75, "3 × 25 = 75 cents."),
        ("1 dollar and 1 quarter. How many cents?", 125, "100 + 25 = 125 cents."),
        ("5 dimes and 2 nickels. How many cents?", 60, "50 + 10 = 60 cents."),
        ("1 quarter and 4 pennies. How many cents?", 29, "25 + 4 = 29 cents."),
        ("2 nickels and 2 dimes. How many cents?", 30, "10 + 20 = 30 cents."),
        ("4 quarters. How many cents?", 100, "4 × 25 = 100 cents, which is $1."),
        ("6 dimes. How many cents?", 60, "6 × 10 = 60 cents."),
        ("1 nickel and 8 pennies. How many cents?", 13, "5 + 8 = 13 cents."),
        ("2 quarters and 1 nickel. How many cents?", 55, "50 + 5 = 55 cents."),
    ]
    for text, ans, expl in counts:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    make = [
        ("Which set makes 25 cents?", "1 quarter",
         "A quarter is 25¢ by itself.", ["2 dimes", "3 nickels", "1 dime"]),
        ("Which set also makes 25 cents?", "2 dimes and 1 nickel",
         "20 + 5 = 25. Same amount, different coins.", ["1 dime", "1 nickel", "3 pennies"]),
        ("10 cents can be 1 dime or…", "2 nickels",
         "2 × 5 = 10.", ["1 nickel", "1 quarter", "3 nickels"]),
        ("40 cents could be 4 dimes or…", "1 quarter and 3 nickels",
         "25 + 15 = 40.", ["1 nickel", "1 dime", "2 pennies"]),
        ("$1.00 is 100 cents. That could be…", "4 quarters",
         "4 × 25 = 100.", ["3 quarters", "2 dimes", "1 nickel"]),
    ]
    for text, ans, expl, dist in make:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    buy = [
        ("A pencil costs 18¢. You pay with 2 dimes. How much change?", 2,
         "20 − 18 = 2 cents.", None),
        ("An eraser costs 25¢. You pay with 1 quarter. How much change?", 0,
         "Exact pay. No change.", None),
        ("A sticker costs 30¢. You pay with 1 quarter and 1 dime. How much change?", 5,
         "25 + 10 = 35 paid. 35 − 30 = 5 cents change.", None),
        ("A snack costs 40¢. You have 3 dimes. Can you buy it?", "no",
         "3 dimes = 30¢. That is not enough.", ["yes", "maybe", "exact"]),
        ("A snack costs 40¢. You have 2 quarters. Can you buy it?", "yes",
         "2 quarters = 50¢. 50 is more than 40.", ["no", "only if tax", "never"]),
        ("You have 55¢. A toy is 50¢. Change?", 5, "55 − 50 = 5 cents.", None),
        ("You have 1 dollar. A book is 75¢. Change in cents?", 25, "100 − 75 = 25 cents.", None),
        ("Two items: 12¢ and 15¢. Total cost?", 27, "12 + 15 = 27 cents.", None),
        ("Two items: 20¢ and 35¢. Total cost?", 55, "20 + 35 = 55 cents.", None),
        ("You pay 50¢ for items that cost 27¢. Change?", 23, "50 − 27 = 23 cents.", None),
    ]
    for text, ans, expl, dist in buy:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    mixed = [
        (1, 2, 0, 0),  # 1Q 2D
        (0, 3, 2, 1),
        (2, 1, 1, 4),
        (0, 0, 4, 10),
        (1, 0, 2, 3),
        (0, 5, 1, 0),
        (3, 0, 0, 5),
        (1, 1, 1, 1),
    ]
    for q, d, n, p in mixed:
        total = 25 * q + 10 * d + 5 * n + p
        qs.append(mq(
            f"{q} quarter(s), {d} dime(s), {n} nickel(s), {p} pennies. How many cents?",
            total,
            f"25×{q} + 10×{d} + 5×{n} + {p} = {total} cents.",
            idx,
        ))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"How many cents are {(i % 6) + 1} dimes?",
        10 * ((i % 6) + 1),
        f"{(i % 6) + 1} × 10 = {10 * ((i % 6) + 1)} cents.",
        i,
    ))


def build_unit6():
    title = "Second Grade Math Unit 6: Counting Money"
    description = (
        "Name pennies, nickels, dimes, quarters, and dollars. Count mixed coins, make the same amount two ways, and make change."
    )

    c1 = concept_block(
        "1. Pennies, nickels, and dimes",
        [
            "A penny is 1 cent. We write 1¢ or $0.01.",
            "A nickel is 5 cents. Five pennies make a nickel.",
            "A dime is 10 cents. Two nickels make a dime. Ten pennies make a dime.",
            "Count dimes by 10s: 10, 20, 30, 40…",
            "Count nickels by 5s: 5, 10, 15, 20… Same skip-count as the clock.",
            "Start with the bigger coins when you count a mixed pile.",
        ],
        lesson_figure(
            svg_coins([("10¢", 3, "#e2e8f0"), ("5¢", 2, "#94a3b8")]),
            "3 dimes and 2 nickels",
            "3 dimes are 30 cents. 2 nickels are 10 cents. 30 + 10 = 40 cents.",
        )
        + solved(1, "You have 3 dimes and 2 nickels. How many cents?",
               ["3 dimes = 30 cents.",
                "2 nickels = 10 cents.",
                "30 + 10 = 40 cents."],
               "40")
        + matching(
            [("penny", "1¢"), ("nickel", "5¢"), ("dime", "10¢"), ("10 pennies", "1 dime")],
            vid="g2u6-c1-match",
        ),
        kid_tip("Biggest first", "Count quarters, then dimes, then nickels, then pennies. The jumps get smaller."),
        1,
    )

    c2 = concept_block(
        "2. Quarters and dollars",
        [
            "A quarter is 25 cents. Four quarters make 100 cents, which is 1 dollar.",
            "Count quarters: 25, 50, 75, 100.",
            "A dollar can be a bill or 100 cents in coins. We write $1 or $1.00.",
            "125 cents is 1 dollar and 25 cents. You can write $1.25.",
            "In this unit we often keep answers in cents so adding stays whole numbers.",
            "Remember: the dollar is 100, not 10. A dime is 10.",
        ],
        lesson_figure(
            svg_coins([("25¢", 3, "#a8a29e")]),
            "3 quarters",
            "Count 25, 50, 75. Three quarters are 75 cents.",
        )
        + solved(1, "3 quarters. How many cents?",
               ["25 + 25 = 50.",
                "50 + 25 = 75 cents."],
               "75")
        + solved(2, "4 quarters. How many cents?",
                 ["25, 50, 75, 100.",
                  "100 cents = 1 dollar."],
                 "100")
        + matching(
            [("quarter", "25¢"), ("dollar", "100¢"), ("2 quarters", "50¢"), ("4 quarters", "$1")],
            vid="g2u6-c2-match",
        ),
        watch_out("Dime vs quarter",
                  "A dime is smaller than a nickel but worth more than a nickel. Size is not value. A quarter is 25, a dime is 10."),
        6,
    )

    c3 = concept_block(
        "3. Count mixed coins",
        [
            "Dump a pile. Sort by type. Count each type. Add the totals.",
            "Example: 1 quarter, 1 dime, 1 nickel, 4 pennies → 25+10+5+4 = 44 cents.",
            "You can also skip-count: 25, 35 (dime), 40 (nickel), 41, 42, 43, 44 (pennies).",
            "Write a running total so you do not lose a coin.",
            "If you reach 100 cents, that is a dollar. You can trade for a dollar bill in real life.",
            "Touch each coin as you add it. Same rule as counting objects.",
        ],
        lesson_figure(
            svg_coins([("10¢", 2, "#e2e8f0"), ("5¢", 3, "#94a3b8"), ("1¢", 1, "#c2410c")]),
            "2 dimes, 3 nickels, 1 penny",
            "2 dimes = 20, 3 nickels = 15, 1 penny = 1. 20 + 15 + 1 = 36 cents.",
        )
        + solved(1, "2 dimes, 3 nickels, 1 penny. How many cents?",
               ["2 dimes = 20.",
                "3 nickels = 15.",
                "20 + 15 + 1 = 36 cents."],
               "36")
        + step_reveal(
            ["Sort the coins.",
             "Count quarters by 25s.",
             "Count dimes by 10s from that total.",
             "Count nickels by 5s, then pennies by 1s."],
            vid="g2u6-c3-steps",
        ),
        try_this("Skip-count out loud", "Say 25… 35… 40… 41. Hearing the total catches mistakes."),
        11,
    )

    c4 = concept_block(
        "4. The same amount, different coins",
        [
            "25 cents can be 1 quarter, or 2 dimes and 1 nickel, or 5 nickels, or 25 pennies.",
            "Different coins, same value. That is making an amount in two ways.",
            "Stores do not care which coins you use, as long as the total matches the price.",
            "Try to use fewer coins when you can. 1 quarter is easier to hold than 25 pennies.",
            "10 cents: 1 dime, or 2 nickels, or 1 nickel and 5 pennies.",
            "Trade: 2 nickels for 1 dime. 4 quarters for 1 dollar.",
        ],
        lesson_figure(
            svg_coins([("10¢", 4, "#e2e8f0")]),
            "4 dimes make 40 cents",
            "4 dimes = 40 cents. 1 quarter and 3 nickels is 25 + 5 + 5 + 5 = 40 cents too. Same amount.",
        )
        + solved(1, "Show 40 cents two ways: 4 dimes, or 1 quarter and 3 nickels. Do they match?",
               ["4 dimes = 40.",
                "25 + 5 + 5 + 5 = 40.",
                "Yes. Same amount."],
               "yes")
        + matching(
            [("25¢ way A", "1 quarter"), ("25¢ way B", "2 dimes + 1 nickel"),
             ("10¢ way A", "1 dime"), ("100¢", "4 quarters")],
            vid="g2u6-c4-match",
        ),
        kid_tip("Trade even", "You may trade coins only when the values match. 3 dimes is 30, not a quarter."),
        16,
    )

    c5 = concept_block(
        "5. Buy and make change",
        [
            "Price is how much it costs. You pay with coins or bills. Change is what you get back if you pay extra.",
            "Change = money you paid − price.",
            "If you pay with exact coins, change is 0.",
            "If you do not have enough, you cannot buy it yet.",
            "Example: pencil 18¢, you pay 2 dimes (20¢). Change 2¢.",
            "Add two prices first if you buy two things. Then subtract from what you paid.",
        ],
        lesson_figure(
            svg_coins([("25¢", 1, "#a8a29e"), ("10¢", 1, "#e2e8f0")]),
            "Pay 1 quarter and 1 dime",
            "You paid 25 + 10 = 35 cents for a 30¢ sticker. Change is 35 − 30 = 5 cents.",
        )
        + solved(1, "A sticker is 30¢. You pay 1 quarter and 1 dime. How much change?",
               ["You paid 25 + 10 = 35 cents.",
                "35 − 30 = 5 cents change."],
               "5")
        + solved(2, "You have 3 dimes. A snack is 40¢. Can you buy it?",
                 ["3 dimes = 30 cents.",
                  "30 is less than 40. Not enough."],
                 "no")
        + step_reveal(
            ["Find the price.",
             "Count the money you pay.",
             "If pay is less than price, you cannot buy it.",
             "If pay is more, subtract: pay minus price is change."],
            vid="g2u6-c5-steps",
        ),
        watch_out("Subtracting the wrong way",
                  "Always paid amount minus price. Not price minus paid, unless you are finding how much more you need."),
        21,
    )

    c6 = concept_block(
        "6. Money stories",
        [
            "Money stories use plus and minus, just like number stories.",
            "Two items: add the prices.",
            "After you spend: subtract from what you had.",
            "You can mix coins and a dollar: $1 and 1 quarter is 125 cents.",
            "Keep units the same. If the question asks for cents, answer in cents.",
            "Two-step money stories: add two prices, then make change from a dollar.",
        ],
        lesson_figure(
            svg_tape([12, 15], ["12¢", "15¢"]),
            "Two prices, then change from 50¢",
            "12 + 15 = 27 cents cost. Pay 50 cents, so change is 50 − 27 = 23 cents.",
        )
        + solved(1, "Two items cost 12¢ and 15¢. You pay 50¢. How much change?",
               ["Step 1: 12 + 15 = 27 cents cost.",
                "Step 2: 50 − 27 = 23 cents change."],
               "23")
        + solved(2, "You have 1 dollar. A book is 75¢. Change?",
                 ["1 dollar = 100 cents.",
                  "100 − 75 = 25 cents."],
                 "25")
        + try_this("Switch to cents", "If you see $1, think 100 cents. Then add and subtract with whole numbers."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Know penny, nickel, and dime values",
            "Know quarter and dollar values",
            "Count mixed coins",
            "Make the same amount with different coins",
            "Make change",
            "Solve money stories",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u6_questions()


# ===========================================================================
# UNIT 7: Geometry
# ===========================================================================

def _u7_questions():
    qs = []
    idx = 1

    shapes2d = [
        ("A triangle has how many sides?", 3, "Tri means three. 3 sides, 3 corners.", None),
        ("A square has how many sides?", 4, "A square has 4 equal sides and 4 square corners.", None),
        ("A rectangle has how many sides?", 4, "4 sides. Opposite sides are equal.", None),
        ("A pentagon has how many sides?", 5, "Penta means five.", None),
        ("A hexagon has how many sides?", 6, "Hex means six.", None),
        ("A circle has how many straight sides?", 0, "A circle is curved. No straight sides.", None),
        ("A square is a special…", "rectangle",
         "A square is a rectangle with all sides equal.", ["circle", "triangle", "hexagon"]),
        ("All 4 sides equal and 4 square corners. What shape?", "square",
         "That is the definition of a square.", ["rhombus only", "circle", "oval"]),
        ("3 sides, 3 corners. What shape?", "triangle",
         "3 of each. Triangle.", ["square", "pentagon", "cube"]),
        ("A quadrilateral has how many sides?", 4, "Quad means four. Squares and rectangles are quadrilaterals.", None),
    ]
    for text, ans, expl, dist in shapes2d:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    shapes3d = [
        ("A cube has how many faces?", 6, "Like a dice. 6 square faces.", None),
        ("A cube has how many edges?", 12, "12 edges where faces meet.", None),
        ("A cube has how many corners (vertices)?", 8, "8 corners on a cube.", None),
        ("A sphere is shaped like a…", "ball",
         "A sphere is round like a ball. No faces or edges.", ["box", "can", "pyramid"]),
        ("A cylinder has how many flat faces?", 2,
         "Top and bottom circles. The side is curved.", ["0", "6", "1"]),
        ("A cone has how many flat faces?", 1, "One circular base. The rest comes to a point.", None),
        ("A rectangular prism is shaped like a…", "box",
         "A cereal box is a rectangular prism.", ["ball", "ice cream cone", "tube"]),
        ("Which shape can roll in any direction?", "sphere",
         "A ball rolls every way. A cylinder rolls only sideways.", ["cube", "pyramid", "box"]),
        ("A pyramid with a square base has how many triangular faces?", 4,
         "4 triangles meet at the top, plus the square base.", ["3", "6", "1"]),
        ("Faces are the…", "flat surfaces",
         "A face is a flat side of a solid.", ["edges", "corners", "curves"]),
    ]
    for text, ans, expl, dist in shapes3d:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    attrib = [
        ("A square corner is also called a right…", "angle",
         "A square corner is a right angle.", ["side", "face", "edge"]),
        ("An angle is made when two sides…", "meet",
         "Two sides meet at a corner and make an angle.", ["curve", "roll", "stack"]),
        ("How many right angles does a rectangle have?", 4,
         "Every corner of a rectangle is a square corner.", None),
        ("A triangle can have a right angle. How many right angles can it have at most in second grade drawings?", 1,
         "A right triangle has one square corner.", ["3", "4", "0 always"]),
        ("Sides are the…", "straight edges of a 2D shape",
         "Count sides around the outside.", ["inside colors", "faces of a ball", "minutes"]),
    ]
    for text, ans, expl, dist in attrib:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    arrays = [
        ("An array has 3 rows of 4 squares. How many squares?", 12, "3 × 4 = 12. Or 4 + 4 + 4 = 12."),
        ("2 rows of 5. How many in all?", 10, "2 × 5 = 10."),
        ("4 rows of 3. How many in all?", 12, "4 × 3 = 12."),
        ("5 rows of 5. How many in all?", 25, "5 × 5 = 25."),
        ("1 row of 8. How many?", 8, "One row is just 8."),
        ("3 rows of 6. How many?", 18, "6 + 6 + 6 = 18."),
        ("A rectangle is split into 2 rows and 3 columns. How many equal squares?", 6, "2 × 3 = 6."),
        ("Rows go across. Columns go…", "up and down",
         "Rows are horizontal. Columns are vertical.", ["in a circle", "diagonal only", "nowhere"]),
    ]
    for item in arrays:
        if len(item) == 4:
            text, ans, expl, dist = item
            qs.append(mq(text, ans, expl, idx, distractors=dist))
        else:
            text, ans, expl = item
            qs.append(mq(text, ans, expl, idx))
        idx += 1

    compose = [
        ("Two identical right triangles can make a…", "rectangle",
         "Put the long sides together. You get a rectangle.", ["circle", "pentagon", "sphere"]),
        ("A hexagon can be made of 6…", "triangles",
         "Six equal triangles can fill a hexagon.", ["circles", "cubes", "ovals"]),
        ("Four small squares can make one…", "bigger square",
         "2 by 2 squares make a larger square.", ["triangle", "circle", "pentagon"]),
        ("A square cut on the diagonal makes 2…", "triangles",
         "The cut from corner to corner makes two right triangles.", ["circles", "pentagons", "ovals"]),
        ("You can put two squares side by side to make a…", "rectangle",
         "The new shape has 2 equal long sides and 2 equal short sides.", ["circle", "triangle", "sphere"]),
    ]
    for text, ans, expl, dist in compose:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    equal_shares = [
        ("A rectangle cut into 2 equal shares. Each share is a…", "half",
         "2 equal parts are halves.", ["third", "fourth", "whole"]),
        ("A square cut into 4 equal squares. Each is a…", "fourth",
         "4 equal parts are fourths, or quarters.", ["half", "third", "tenth"]),
        ("Equal shares must be the same…", "size",
         "Equal means same amount of the whole.", ["color", "name", "border only"]),
        ("3 equal parts of a whole are called…", "thirds",
         "Thirds come in three.", ["halves", "fourths", "wholes"]),
        ("If shares are not the same size, they are not…", "equal",
         "Unequal parts are not fair shares.", ["shapes", "sides", "corners"]),
    ]
    for text, ans, expl, dist in equal_shares:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"A shape with {3 + (i % 4)} sides is a polygon with how many sides?",
        3 + (i % 4),
        f"Count the sides. There are {3 + (i % 4)}.",
        i,
        distractors=[str(2 + (i % 4)), str(4 + (i % 4)), str(6)],
    ))


def build_unit7():
    title = "Second Grade Math Unit 7: Geometry"
    description = (
        "Name 2D and 3D shapes, count sides, angles, faces, and edges, build arrays, and make equal shares."
    )

    c1 = concept_block(
        "1. Two-dimensional shapes",
        [
            "Flat shapes live on paper. We call them 2D.",
            "Triangle: 3 sides. Quadrilateral: 4 sides. Pentagon: 5. Hexagon: 6.",
            "A square has 4 equal sides and 4 square corners. A rectangle has 4 square corners. Opposite sides match.",
            "A square is a special rectangle because it has square corners and opposite sides equal (in fact all sides equal).",
            "A circle is round. It has no straight sides.",
            "Name a shape by its sides and corners, not only by how it is turned. A square on a point is still a square.",
        ],
        lesson_figure(
            '<svg viewBox="0 0 160 150" width="140" role="img">'
            '<polygon points="80,12 138,45 138,105 80,138 22,105 22,45" fill="#bfdbfe" stroke="#1e3a8a" stroke-width="2"/>'
            '<text x="80" y="82" text-anchor="middle" font-size="13" font-weight="700">6 sides</text></svg>',
            "A hexagon",
            "Hex means six. A shape with 6 straight sides is a hexagon.",
        )
        + solved(1, "A shape has 6 straight sides. What is it?",
               ["6 sides → hexagon.",
                "Hex means six."],
               "hexagon")
        + matching(
            [("triangle", "3 sides"), ("rectangle", "4 square corners"),
             ("pentagon", "5 sides"), ("circle", "0 straight sides")],
            vid="g2u7-c1-match",
        ),
        kid_tip("Turn it", "Rotate a shape. If the sides and corners stay the same, the name stays the same.")
        + phet_box("area"),
        1,
    )

    c2 = concept_block(
        "2. Three-dimensional shapes",
        [
            "Solid shapes take up space. We call them 3D.",
            "Cube: like a dice. 6 square faces, 12 edges, 8 corners.",
            "Rectangular prism: like a box. Faces are rectangles (some may be squares).",
            "Sphere: like a ball. Curved. No faces, no edges.",
            "Cylinder: like a can. 2 flat circle faces and a curved side.",
            "Cone: like a party hat. 1 circle face and a point.",
        ],
        lesson_figure(
            '<svg viewBox="0 0 160 150" width="140" role="img">'
            '<polygon points="40,52 100,52 100,112 40,112" fill="#93c5fd" stroke="#0f172a"/>'
            '<polygon points="100,52 130,34 130,94 100,112" fill="#60a5fa" stroke="#0f172a"/>'
            '<polygon points="40,52 70,34 130,34 100,52" fill="#bfdbfe" stroke="#0f172a"/>'
            '<text x="80" y="140" text-anchor="middle" font-size="12">6 square faces</text></svg>',
            "A cube like a dice",
            "A cube has 6 square faces, one on each side of a dice.",
        )
        + solved(1, "How many faces does a cube have?",
               ["A dice has a number on each flat side.",
                "There are 6 faces."],
               "6")
        + solved(2, "Which solid looks like a ball?",
                 ["A ball is a sphere.",
                  "It rolls in every direction."],
                 "sphere")
        + matching(
            [("cube", "dice"), ("sphere", "ball"), ("cylinder", "can"), ("cone", "party hat")],
            vid="g2u7-c2-match",
        ),
        watch_out("Calling every box a cube",
                  "A cube's faces are all squares. A long box is a rectangular prism, not a cube."),
        6,
    )

    c3 = concept_block(
        "3. Sides, corners, and angles",
        [
            "A side is a straight edge of a 2D shape.",
            "A corner (vertex) is where two sides meet.",
            "The meeting makes an angle. A square corner is a right angle. It looks like the corner of a book.",
            "A rectangle has 4 right angles. A square does too.",
            "On solids, faces meet at edges, and edges meet at vertices (corners).",
            "Count carefully. Trace the shape with a finger so you do not double-count.",
        ],
        lesson_figure(
            svg_rect(5, 3),
            "A rectangle",
            "Every corner of a rectangle is a square corner, so a rectangle has 4 right angles.",
        )
        + solved(1, "How many right angles does a rectangle have?",
               ["Each corner is a square corner.",
                "There are 4 corners. 4 right angles."],
               "4")
        + step_reveal(
            ["Pick a shape.",
             "Trace each side and tally.",
             "Touch each corner and tally.",
             "Check that a closed shape has the same number of sides and corners."],
            vid="g2u7-c3-steps",
        ),
        try_this("Book test", "Hold a book corner on a shape's corner. If they match, it is a right angle."),
        11,
    )

    c4 = concept_block(
        "4. Rows, columns, and arrays",
        [
            "An array is equal rows of the same number of squares.",
            "Rows go across. Columns go up and down.",
            "3 rows of 4 is 4 + 4 + 4 = 12. Turn the array: that is also 4 columns of 3. Same 12.",
            "Second grade uses arrays to see equal groups. This later becomes multiplication.",
            "A rectangle split into same-size squares is an array.",
            "Count one row, then skip-count that number for each row.",
        ],
        lesson_figure(
            svg_dots(12, per_row=4, label="3 rows of 4"),
            "3 rows of 4 squares",
            "One row is 4. Skip-count 4, 8, 12. The array has 12 squares.",
        )
        + solved(1, "An array has 3 rows of 4 squares. How many squares?",
               ["One row is 4.",
                "Three rows: 4, 8, 12.",
                "12 squares."],
               "12")
        + solved(2, "2 rows of 5. How many?",
                 ["5 + 5 = 10."],
                 "10")
        + matching(
            [("3 rows of 4", "12"), ("2 rows of 5", "10"),
             ("4 rows of 3", "12"), ("5 rows of 5", "25")],
            vid="g2u7-c4-match",
        ),
        kid_tip("Same total both ways", "3 rows of 4 and 4 rows of 3 both make 12. The array is just turned."),
        16,
    )

    c5 = concept_block(
        "5. Equal shares of shapes",
        [
            "You can cut a whole into equal shares.",
            "2 equal shares are halves. 3 equal shares are thirds. 4 equal shares are fourths (quarters).",
            "Equal means same size, not only same shape look. Two halves of a rectangle can be two smaller rectangles.",
            "If one piece is bigger, the shares are not equal.",
            "This idea connects to fractions in the next unit.",
            "Fold paper to test. If the fold pieces match, the shares are equal.",
        ],
        lesson_figure(
            svg_fraction_bar(1, 4),
            "4 equal shares",
            "A square cut into 4 equal parts makes fourths. Each share is one fourth.",
        )
        + solved(1, "A square cut into 4 equal little squares. What is each share called?",
               ["4 equal parts.",
                "Each is a fourth."],
               "fourth")
        + phet_box("area"),
        watch_out("Same number of pieces but different sizes",
                  "Three pieces are not thirds unless they are the same size."),
        21,
    )

    c6 = concept_block(
        "6. Put shapes together",
        [
            "You can join shapes to make new shapes.",
            "Two identical right triangles make a rectangle (or a bigger triangle, depending how you join them).",
            "Four small squares make a bigger square.",
            "Pattern blocks: hexagons fill with triangles or diamonds.",
            "When you join, sides that touch should match so there is no gap.",
            "Taking shapes apart is the reverse. A rectangle split on the diagonal becomes two triangles.",
        ],
        lesson_figure(
            '<svg viewBox="0 0 240 120" width="100%" style="max-width:240px" role="img">'
            '<rect x="20" y="18" width="70" height="70" fill="#93c5fd" stroke="#0f172a" stroke-width="2"/>'
            '<rect x="90" y="18" width="70" height="70" fill="#86efac" stroke="#0f172a" stroke-width="2"/>'
            '<text x="90" y="108" text-anchor="middle" font-size="12">two squares make a rectangle</text></svg>',
            "Two squares side by side",
            "The new outline has 4 sides, opposite sides equal, and square corners. That is a rectangle.",
        )
        + solved(1, "Two squares side by side make what 2D shape?",
               ["The new outline has 4 sides. Opposite sides equal. Square corners.",
                "It is a rectangle (longer than a square unless you stacked differently)."],
               "rectangle")
        + matching(
            [("2 right triangles", "can make a rectangle"),
             ("4 small squares", "can make a bigger square"),
             ("square cut on a diagonal", "2 triangles"),
             ("no gaps", "sides must match")],
            vid="g2u7-c6-match",
        ),
        try_this("Trace then cut", "Trace two triangles. Cut them. Fit them into a rectangle. Seeing beats guessing."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Name flat 2D shapes by sides and corners",
            "Name solid 3D shapes",
            "Count sides, corners, faces, and right angles",
            "Build arrays with rows and columns",
            "Make equal shares",
            "Compose and take apart shapes",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u7_questions()


# ===========================================================================
# UNIT 8: Fractions
# ===========================================================================

def _u8_questions():
    qs = []
    idx = 1

    equal = [
        ("Equal parts of a whole are the same…", "size",
         "Equal parts cover the same amount of the whole.", ["color", "name only", "border"]),
        ("A whole split into 2 equal parts makes…", "halves",
         "Two equal shares are halves.", ["thirds", "fourths", "wholes"]),
        ("A whole split into 3 equal parts makes…", "thirds",
         "Three equal shares are thirds.", ["halves", "fourths", "fifths"]),
        ("A whole split into 4 equal parts makes…", "fourths",
         "Four equal shares are fourths.", ["halves", "thirds", "wholes"]),
        ("If one piece is bigger than the others, the parts are…", "not equal",
         "Unequal pieces are not fair shares.", ["still halves", "always thirds", "fine"]),
    ]
    for text, ans, expl, dist in equal:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    halves = [
        ("How many halves make one whole?", 2, "2/2 = 1 whole. Two halves fill the shape.", None),
        ("One half is written…", "1/2",
         "1 part out of 2 equal parts.", ["1/3", "1/4", "2/1"]),
        ("A sandwich cut down the middle into 2 equal pieces. Each piece is…", "1/2",
         "Two equal parts. Each is one half.", ["1/3", "1/4", "2/2"]),
        ("If you eat 1 of 2 equal parts, what fraction did you eat?", "1/2",
         "1 out of 2.", ["2/2", "1/4", "0"]),
        ("2/2 is the same as…", "1 whole",
         "Both halves together are the whole.", ["1/2", "nothing", "1/4"]),
    ]
    for text, ans, expl, dist in halves:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    thirds = [
        ("How many thirds make one whole?", 3, "3/3 = 1 whole.", None),
        ("One third is written…", "1/3",
         "1 part out of 3 equal parts.", ["1/2", "1/4", "3/1"]),
        ("You shade 1 of 3 equal pieces. The fraction shaded is…", "1/3",
         "1 out of 3.", ["1/2", "2/3", "3/3"]),
        ("You shade 2 of 3 equal pieces. The fraction shaded is…", "2/3",
         "2 out of 3.", ["1/3", "2/2", "3/2"]),
        ("3/3 is the same as…", "1 whole",
         "All three thirds fill the whole.", ["1/3", "2/3", "0"]),
    ]
    for text, ans, expl, dist in thirds:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    fourths = [
        ("How many fourths make one whole?", 4, "4/4 = 1 whole.", None),
        ("One fourth is written…", "1/4",
         "1 part out of 4 equal parts. Also called one quarter.", ["1/2", "1/3", "4/1"]),
        ("A pizza cut into 4 equal slices. One slice is…", "1/4",
         "1 out of 4.", ["1/3", "1/2", "4/4"]),
        ("You shade 3 of 4 equal pieces. The fraction shaded is…", "3/4",
         "3 out of 4.", ["1/4", "3/3", "4/3"]),
        ("2/4 of the same whole is the same amount as…", "1/2",
         "Two fourths fill the same as one half.", ["1/4", "1/3", "2/2"]),
        ("4/4 is the same as…", "1 whole",
         "All four fourths fill the whole.", ["1/4", "2/4", "0"]),
    ]
    for text, ans, expl, dist in fourths:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    names = [
        ("In 1/4, the 4 tells how many…", "equal parts in the whole",
         "The bottom number is the denominator. It names the size of the parts.", ["parts you colored", "wholes you have", "sides"]),
        ("In 1/4, the 1 tells how many…", "parts you count",
         "The top number is the numerator. It counts the pieces you mean.", ["parts in the whole", "shapes nearby", "hours"]),
        ("Which fraction is larger if both are parts of the same whole: 1/2 or 1/4?", "1/2",
         "Halves are bigger pieces than fourths. 1/2 covers more.", ["1/4", "same", "1/8"]),
        ("Which is larger of the same whole: 1/2 or 1/3?", "1/2",
         "Fewer equal parts means each part is bigger. 1/2 > 1/3.", ["1/3", "same", "2/3"]),
        ("Which is larger of the same whole: 1/3 or 1/4?", "1/3",
         "Thirds are bigger pieces than fourths.", ["1/4", "same", "1/2"]),
        ("1/2 and 2/4 of the same sandwich are…", "equal",
         "They cover the same amount.", ["1/2 bigger", "2/4 bigger", "cannot say"]),
        ("You cannot compare 1/2 of a tiny cookie and 1/2 of a huge cake as the same size because…", "the wholes are different",
         "Fractions need the same whole to compare fairly.", ["halves are always equal objects", "cakes are thirds", "cookies are fourths"]),
        ("3/4 compared with 1/4 of the same pizza. Which is more?", "3/4",
         "3 pieces beat 1 piece of the same size.", ["1/4", "same", "1/2"]),
    ]
    for text, ans, expl, dist in names:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    pics = [
        ("A rectangle split into 2 equal parts, 1 shaded. Fraction?", "1/2",
         "1 of 2.", ["1/3", "2/2", "1/4"]),
        ("A circle split into 4 equal parts, 1 shaded. Fraction?", "1/4",
         "1 of 4.", ["1/2", "1/3", "4/1"]),
        ("A bar split into 3 equal parts, 1 shaded. Fraction?", "1/3",
         "1 of 3.", ["1/2", "2/3", "3/1"]),
        ("A bar split into 4 equal parts, 2 shaded. Fraction?", "2/4",
         "2 of 4, which equals 1/2.", ["2/2", "1/4", "4/2"]),
        ("A circle split into 3 equal parts, 3 shaded. Fraction?", "3/3",
         "The whole circle is shaded.", ["1/3", "0", "2/3"]),
        ("A square split into 4 equal parts, 4 shaded. Fraction?", "4/4",
         "The whole square is shaded.", ["1/4", "0", "2/4"]),
        ("No parts shaded of 4 equal parts. Fraction shaded?", "0/4",
         "Zero parts out of 4. That is none of the whole.", ["1/4", "4/0", "1/0"]),
        ("A hexagon split into 6 equal triangles, 1 shaded. That is one…", "sixth",
         "6 equal parts are sixths. Grade 2 focuses on halves, thirds, fourths, but 1 of 6 is a sixth.", ["half", "third", "fourth"]),
    ]
    for text, ans, expl, dist in pics:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    more = [
        ("Two halves of the same apple. How many wholes?", 1, "2/2 = 1.", None),
        ("Four fourths of the same pie. How many wholes?", 1, "4/4 = 1.", None),
        ("You need 2 halves to make how many wholes?", 1, "2 halves = 1 whole.", None),
        ("You need 3 thirds to make how many wholes?", 1, "3 thirds = 1 whole.", None),
        ("A whole is split into halves. Each half is bigger than each fourth of the same whole. True?", "true",
         "Bigger pieces when there are fewer cuts.", ["false", "sometimes", "never"]),
    ]
    for text, ans, expl, dist in more:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"A whole is split into {2 + (i % 3)} equal parts. How many parts make the whole?",
        2 + (i % 3),
        f"All {2 + (i % 3)} equal parts together make 1 whole.",
        i,
    ))


def build_unit8():
    title = "Second Grade Math Unit 8: Fractions"
    description = (
        "Make equal shares, name halves, thirds, and fourths, write simple fractions, and compare them on the same whole."
    )

    c1 = concept_block(
        "1. Equal parts of a whole",
        [
            "A fraction names equal parts of one whole.",
            "The whole might be a sandwich, a pizza, a rectangle, or a group later on. Here we use one shape as the whole.",
            "Cut or fold so every piece is the same size. Then the parts are equal.",
            "If pieces are different sizes, you cannot name them with a fair fraction yet.",
            "The more equal parts you make, the smaller each part is.",
            "Say: this is the whole. Then: these are the equal parts.",
        ],
        lesson_figure(
            '<svg viewBox="0 0 240 80" width="100%" style="max-width:240px" role="img">'
            '<rect x="8" y="12" width="150" height="40" fill="#a78bfa" stroke="#0f172a"/>'
            '<rect x="158" y="12" width="50" height="40" fill="#f8fafc" stroke="#0f172a"/>'
            '<text x="120" y="70" text-anchor="middle" font-size="12">unequal pieces are not halves</text></svg>',
            "Two pieces, not the same size",
            "Halves must be equal. If one piece is much bigger, the cut is not halves.",
        )
        + solved(1, "A square is cut into 2 pieces, but one piece is much bigger. Are they halves?",
               ["Halves must be equal.",
                "These pieces are not the same size.",
                "They are not halves."],
               "no")
        + matching(
            [("2 equal parts", "halves"), ("3 equal parts", "thirds"),
             ("4 equal parts", "fourths"), ("unequal parts", "not fair shares")],
            vid="g2u8-c1-match",
        ),
        kid_tip("Fold to test", "Fold the paper. If the parts match, they are equal.")
        + phet_box("frac_intro"),
        1,
    )

    c2 = concept_block(
        "2. Halves",
        [
            "Two equal parts are halves. Each part is one half, written 1/2.",
            "The top number (1) counts the parts you mean. The bottom number (2) tells how many equal parts make the whole.",
            "Two halves make one whole: 2/2 = 1.",
            "A sandwich cut down the middle is a classic half.",
            "Half past on a clock is related: the hour is split into two 30-minute halves.",
            "Shade 1 of 2 equal parts to show 1/2.",
        ],
        lesson_figure(
            svg_fraction_bar(1, 2),
            "One half",
            "Two equal parts make the whole. One part shaded is 1/2.",
        )
        + solved(1, "How do we write one half?",
               ["1 part counted.",
                "2 equal parts in the whole.",
                "1/2."],
               "1/2")
        + solved(2, "How many halves make a whole?",
                 ["Fill both parts.",
                  "2 halves."],
                 "2")
        + phet_box("build_frac"),
        watch_out("Writing 2/1",
                  "1/2 is one out of two. 2/1 would mean two wholes, which is not one half."),
        6,
    )

    c3 = concept_block(
        "3. Thirds",
        [
            "Three equal parts are thirds. One part is 1/3.",
            "Two parts are 2/3. All three parts are 3/3, which is one whole.",
            "Thirds are smaller than halves of the same whole, because you split into more pieces.",
            "A rectangle can be cut into three equal strips.",
            "Do not call three random pieces thirds. Size must match.",
            "Shade 1 of 3 to show 1/3. Shade 2 of 3 to show 2/3.",
        ],
        lesson_figure(
            svg_fraction_bar(2, 3),
            "2 of 3 equal pieces",
            "The whole has 3 equal parts. 2 parts shaded is 2/3.",
        )
        + solved(1, "You shade 2 of 3 equal pieces. What fraction is shaded?",
               ["Parts counted: 2.",
                "Equal parts in the whole: 3.",
                "2/3."],
               "2/3")
        + matching(
            [("1/3", "one third"), ("2/3", "two thirds"),
             ("3/3", "one whole"), ("thirds vs halves", "thirds are smaller pieces of the same whole")],
            vid="g2u8-c3-match",
        ),
        try_this("Same whole", "Draw one rectangle. Split it into 2, and another copy into 3. See that 1/2 is a bigger bite than 1/3."),
        11,
    )

    c4 = concept_block(
        "4. Fourths",
        [
            "Four equal parts are fourths, also called quarters.",
            "One part is 1/4. Two parts are 2/4. Three parts are 3/4. Four parts are 4/4 = 1.",
            "2/4 covers the same amount as 1/2 of the same whole. They are equal fractions.",
            "A pizza often comes in fourths. One slice of four is 1/4.",
            "Money: a quarter coin is 1/4 of a dollar, because 4 quarters make $1. That is the same idea.",
            "Clock: quarter past is 1/4 of an hour (15 minutes).",
        ],
        lesson_figure(
            svg_fraction_bar(1, 4),
            "1 of 4 pizza slices",
            "4 equal slices make the whole pizza. Eating 1 slice is 1/4.",
        )
        + solved(1, "A pizza has 4 equal slices. You eat 1 slice. What fraction did you eat?",
               ["1 slice out of 4 equal slices.",
                "1/4."],
               "1/4")
        + solved(2, "Is 2/4 the same amount as 1/2 of the same pizza?",
                 ["2 out of 4 is half of the slices.",
                  "Yes. Equal amounts."],
                 "yes")
        + phet_box("frac_match"),
        kid_tip("Quarter words", "Fourth, quarter, and 1/4 can name the same size part."),
        16,
    )

    c5 = concept_block(
        "5. Write and read a fraction",
        [
            "A fraction has two numbers with a bar between them.",
            "Bottom number: how many equal parts in the whole. Top number: how many of those parts you mean.",
            "Read 3/4 as three fourths. Read 1/3 as one third.",
            "0/4 means none of the parts. The whole is still there, just not shaded.",
            "The whole must be clear. 1/2 of a cracker is not the same size as 1/2 of a cake.",
            "Point to the picture. Count equal parts. Count shaded parts. Write shaded over total.",
        ],
        lesson_figure(
            svg_fraction_bar(3, 4),
            "3 of 4 parts shaded",
            "Count 4 equal parts on the bottom. Count 3 shaded parts on the top. Write 3/4.",
        )
        + solved(1, "A bar has 4 equal parts. 3 are shaded. Write the fraction.",
               ["Shaded = 3. Total equal parts = 4.",
                "Write 3/4."],
               "3/4")
        + step_reveal(
            ["Find the whole.",
             "Count the equal parts. That number is the bottom.",
             "Count the parts you mean (often the shaded ones). That number is the top.",
             "Write top / bottom and say it out loud."],
            vid="g2u8-c5-steps",
        ),
        watch_out("Flipping the numbers",
                  "If 1 part is shaded out of 4, write 1/4, not 4/1."),
        21,
    )

    c6 = concept_block(
        "6. Compare fractions of the same whole",
        [
            "You can compare fractions when they talk about the same whole.",
            "If the bottom numbers match, more parts on top means more: 3/4 > 1/4.",
            "If the top is 1, a smaller bottom number means a bigger piece: 1/2 > 1/3 > 1/4.",
            "Think: fewer cuts, bigger pieces.",
            "1/2 and 2/4 of the same whole are equal.",
            "Do not compare 1/2 of a tiny cookie with 1/2 of a giant cake and call them the same size. The wholes differ.",
        ],
        lesson_figure(
            svg_fraction_bar(1, 2) + svg_fraction_bar(1, 4),
            "Same whole: 1/2 and 1/4",
            "Fewer cuts make bigger pieces. One half of the same pizza is more than one fourth.",
        )
        + solved(1, "Same pizza. Which is more, 1/2 or 1/4?",
               ["Halves are bigger pieces than fourths.",
                "1/2 is more."],
               "1/2")
        + solved(2, "Same sandwich. 1/2 and 2/4. Compare.",
                 ["Two fourths fill the same as one half.",
                  "They are equal."],
                 "equal")
        + matching(
            [("same whole, 1/2 vs 1/4", "1/2 is more"),
             ("same whole, 1/3 vs 1/4", "1/3 is more"),
             ("same whole, 3/4 vs 1/4", "3/4 is more"),
             ("same whole, 1/2 vs 2/4", "equal")],
            vid="g2u8-c6-match",
        ),
        try_this("Draw both", "Sketch the same rectangle twice. Shade 1/2 on one and 1/4 on the other. Your eyes check the comparison.")
        + phet_box("frac_match"),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Make equal parts of a whole",
            "Name and write halves",
            "Name and write thirds",
            "Name and write fourths",
            "Read the top and bottom of a fraction",
            "Compare fractions of the same whole",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u8_questions()


def build_master():
    return f"""
<h1>Second Grade Math</h1>
<p>This is a full second-grade math path. We use <strong>short words</strong>, pictures, and lots of practice.</p>
<p>You will work with numbers to 1,000, add and subtract with regrouping, solve two-step stories, tell time to five minutes, count money, name shapes, and explore fractions. After each idea there are 5 quick questions. At the end of a unit there are 50 more. Hearts help you. Take your time.</p>
{page_break()}
<h2>The eight units</h2>
<ol>
<li>Unit 1 — Numbers to 1,000</li>
<li>Unit 2 — Addition with Regrouping</li>
<li>Unit 3 — Subtraction with Regrouping</li>
<li>Unit 4 — Two-Step Word Problems</li>
<li>Unit 5 — Time to Five Minutes</li>
<li>Unit 6 — Counting Money</li>
<li>Unit 7 — Geometry</li>
<li>Unit 8 — Fractions</li>
</ol>
<p>Start with place value. Addition and subtraction use that skill. Stories put the operations together. Time, money, shapes, and fractions are the last four adventures.</p>
{page_break()}
<h2>How to learn</h2>
<p>Line up hundreds, tens, and ones. Say numbers out loud. Draw coins and clock hops of five. Fold paper for fractions.</p>
<p>If a question feels hard, try a smaller number first. Then come back. You are building number sense — a feeling for how numbers work.</p>
"""
