"""Third Grade Math units 5–8: multi-step stories, fractions, area, perimeter, plus master page."""

from curriculum_kit import (
    lesson_figure, svg_dots, svg_number_line, svg_rect, svg_fraction_bar,
    svg_tape, svg_circle, svg_triangle, svg_clock, svg_base10,
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


def _frac_line(den, num):
    w, h, y = 460, 78, 36
    left, right = 28, w - 28
    bits = [
        f'<line x1="{left}" y1="{y}" x2="{right}" y2="{y}" stroke="#0f172a" stroke-width="2"/>'
    ]
    for i in range(den + 1):
        x = left + i * (right - left) / den
        lab = "0" if i == 0 else ("1" if i == den else f"{i}/{den}")
        bits.append(
            f'<line x1="{x:.1f}" y1="{y - 7}" x2="{x:.1f}" y2="{y + 7}" stroke="#0f172a" stroke-width="2"/>'
        )
        bits.append(
            f'<text x="{x:.1f}" y="{y + 22}" text-anchor="middle" font-size="11">{lab}</text>'
        )
    x = left + num * (right - left) / den
    bits.append(f'<circle cx="{x:.1f}" cy="{y}" r="7" fill="#dc2626"/>')
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'{"".join(bits)}</svg>'
    )


def _fill(qs, need, factory):
    while len(qs) < need:
        qs.append(factory(len(qs) + 1))
    return renumber(qs[:need])


# ===========================================================================
# UNIT 5: Multi-step word problems
# ===========================================================================

def _u5_questions():
    qs = []
    idx = 1

    two_addsub = [
        ("A shop had 48 apples. It sold 19, then got 25 more. How many apples now?", 54,
         "48 − 19 = 29. Then 29 + 25 = 54."),
        ("Mia has 36 stickers. She gets 18, then gives 12 away. How many stickers?", 42,
         "36 + 18 = 54. Then 54 − 12 = 42."),
        ("A library has 120 books. 45 are checked out. Then 30 come back. How many books are in now?", 105,
         "120 − 45 = 75. Then 75 + 30 = 105."),
        ("You score 14, then 9, then 8. Total points?", 31, "14 + 9 + 8 = 31."),
        ("200 kids. 75 leave on a bus, then 40 leave on another bus. How many kids stay?", 85,
         "75 + 40 = 115 leave. 200 − 115 = 85."),
    ]
    for text, ans, expl in two_addsub:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    mul_mix = [
        ("4 packs of 6 crayons. Then you buy 3 more crayons. How many crayons?", 27,
         "4 × 6 = 24. Then 24 + 3 = 27."),
        ("5 bags of 8 apples. You eat 6 apples. How many apples left?", 34,
         "5 × 8 = 40. Then 40 − 6 = 34."),
        ("3 rows of 7 seats. 5 seats are empty. How many seats are filled?", 16,
         "3 × 7 = 21. Then 21 − 5 = 16."),
        ("A box has 9 packs of 4 cards. Then 2 extra cards. How many cards?", 38,
         "9 × 4 = 36. Then 36 + 2 = 38."),
        ("6 kids each bring 5 snacks. They eat 8 snacks. How many snacks left?", 22,
         "6 × 5 = 30. Then 30 − 8 = 22."),
        ("2 shelves with 12 books each. You add 7 books. How many books?", 31,
         "2 × 12 = 24. Then 24 + 7 = 31."),
        ("8 packs of 3 muffins. 5 muffins are sold. How many muffins left?", 19,
         "8 × 3 = 24. Then 24 − 5 = 19."),
        ("7 days, 4 problems each day, plus 2 bonus. How many problems?", 30,
         "7 × 4 = 28. Then 28 + 2 = 30."),
    ]
    for text, ans, expl in mul_mix:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    div_mix = [
        ("24 stickers shared by 4 kids. Then each kid gets 2 more. How many does each have now?", 8,
         "24 ÷ 4 = 6. Then 6 + 2 = 8."),
        ("36 muffins in 6 boxes, equal. You add 1 muffin to a box. How many in that box?", 7,
         "36 ÷ 6 = 6 per box. Then 6 + 1 = 7."),
        ("40 cards dealt to 5 players, equal. One player gives away 3. How many does that player have?", 5,
         "40 ÷ 5 = 8. Then 8 − 3 = 5."),
        ("18 pencils in 3 cups, equal. You put the cups together and add 4 pencils. How many pencils?", 22,
         "The 18 are already the total. Adding 4 makes 22. (Or 18 ÷ 3 = 6 each, 3×6=18, +4=22.)"),
        ("56 seats in 7 equal rows. 2 rows are empty. How many seats are filled?", 40,
         "56 ÷ 7 = 8 per row. 5 rows filled: 5 × 8 = 40. Or 56 − 16 = 40."),
        ("30 apples in 5 bags. You take 1 bag away. How many apples left?", 24,
         "30 ÷ 5 = 6 per bag. 4 bags left: 4 × 6 = 24."),
        ("48 photos in 8 albums, equal. You add a 9th album with 3 photos. Total photos?", 51,
         "48 + 3 = 51."),
        ("27 kids in 9 equal teams. 2 teams leave. How many kids stay?", 21,
         "27 ÷ 9 = 3 per team. 7 teams stay: 7 × 3 = 21."),
    ]
    for text, ans, expl in div_mix:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    four_ops = [
        ("3 packs of 5 stickers and 2 packs of 4 stickers. How many stickers?", 23,
         "3×5=15. 2×4=8. 15+8=23."),
        ("A farmer has 4 rows of 6 plants and 3 extra plants. How many plants?", 27,
         "4×6=24. 24+3=27."),
        ("You buy 2 toys for 8 dollars each and a 5-dollar game. How many dollars?", 21,
         "2×8=16. 16+5=21."),
        ("There are 5 boxes of 10 pencils. 12 pencils are used. How many pencils left?", 38,
         "5×10=50. 50−12=38."),
        ("Sam has 9 bags of 3 marbles. He gives 10 marbles away. How many marbles left?", 17,
         "9×3=27. 27−10=17."),
        ("A tray holds 8 cookies. 4 trays. Kids eat 15 cookies. How many cookies left?", 17,
         "4×8=32. 32−15=17."),
        ("Lila reads 5 pages a day for 6 days, then 4 more pages. How many pages?", 34,
         "5×6=30. 30+4=34."),
        ("A class of 28 splits into 4 equal groups. Then 2 kids join one group. How many in that group?", 9,
         "28÷4=7. 7+2=9."),
    ]
    for text, ans, expl in four_ops:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    choose = [
        ("Equal groups, then some extra. First operation is usually…", "multiply",
         "Equal groups → ×. Then add or subtract the extra.", ["add only", "divide only", "round"]),
        ("A total split equally, then some leave one share. First operation is usually…", "divide",
         "Split equally → ÷. Then subtract from one share.", ["multiply", "round", "compare"]),
        ("Two different equal-group piles joined. You…", "multiply twice, then add",
         "Find each pile with ×, then add the piles.", ["add only", "divide twice", "subtract twice"]),
        ("Estimate 5 × 8 + 3. A nearby estimate is…", 43,
         "Exact is 40+3=43. Estimate might be 40+0=40, but 43 is exact here.", ["5", "8", "3"]),
        ("If your answer is smaller than one of the starting packs in a 'how many in all' story, you probably…", "missed a step",
         "In-all answers should make sense next to the story numbers.", ["rounded", "multiplied extra", "done"]),
    ]
    for text, ans, expl, dist in choose:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"{3 + (i % 5)} packs of {4 + (i % 4)} items, then {2 + (i % 3)} more items. How many items?",
        (3 + (i % 5)) * (4 + (i % 4)) + (2 + (i % 3)),
        f"Multiply packs, then add the extra. {(3 + (i % 5)) * (4 + (i % 4)) + (2 + (i % 3))}.",
        i,
    ))


def build_unit5():
    title = "Third Grade Math Unit 5: Multi-Step Word Problems"
    description = (
        "Solve stories with two or more steps using add, subtract, multiply, and divide. Plan with bars and check if the answer makes sense."
    )

    c1 = concept_block(
        "1. Two-step add and subtract",
        [
            "Some stories still use only plus and minus, but they need two moves.",
            "A shop had 48 apples, sold 19, then got 25 more. First take away, then add.",
            "Write step 1. Use that answer in step 2. Do not jump.",
            "Bar drawings help: start with a bar, shrink it, then grow it.",
            "Words like then, after that, and next often start the second step.",
            "Check: reread the last question. Does your number answer that sentence?",
        ],
        lesson_figure(
            svg_tape([36, 18], labels=["had 36", "gets 18"]),
            "Mia's stickers, two steps",
            "First join 36 and 18 to get 54. Then take 12 away: 54 − 12 = 42 stickers now.",
        )
        + solved(1, "Mia has 36 stickers. She gets 18, then gives 12 away. How many now?",
               ["36 + 18 = 54 after getting more.",
                "54 − 12 = 42 after giving some away.",
                "42 stickers."],
               "42")
        + step_reveal(
            ["Underline the two actions.",
             "Solve action 1. Box that number.",
             "Use the boxed number in action 2.",
             "Label the final answer."],
            vid="g3u5-c1-steps",
        ),
        kid_tip("Two actions, two sentences", "If two things happen, write two number sentences."),
        1,
    )

    c2 = concept_block(
        "2. Multiply, then add or subtract",
        [
            "Equal groups plus extras is a classic third-grade story.",
            "4 packs of 6 crayons, then 3 more crayons: 4 × 6 = 24, then 24 + 3 = 27.",
            "Equal groups minus some used: 5 bags of 8, eat 6: 40 − 6 = 34.",
            "Multiply the equal groups first. The extra is usually not another full pack.",
            "If the extra is also equal groups, you may multiply twice (next lessons).",
            "Estimate: 4 × 6 is about 4 × 5 = 20, plus a few. 27 is reasonable.",
        ],
        lesson_figure(
            svg_tape([34, 6], labels=["left 34", "eaten 6"]),
            "5 bags of 8, then eat 6",
            "Equal groups first: 5 × 8 = 40. The tape splits 40 into 34 left and 6 eaten.",
        )
        + solved(1, "5 bags of 8 apples. You eat 6. How many apples left?",
               ["5 × 8 = 40 apples.",
                "40 − 6 = 34 left."],
               "34")
        + solved(2, "7 days, 4 problems each day, plus 2 bonus. How many problems?",
                 ["7 × 4 = 28.",
                  "28 + 2 = 30."],
                 "30")
        + matching(
            [("packs then extras", "× then +"), ("packs then some eaten", "× then −"),
             ("4 × 6 + 3", "27"), ("5 × 8 − 6", "34")],
            vid="g3u5-c2-match",
        ),
        watch_out("Adding the pack count instead of multiplying",
                  "4 packs of 6 is not 4 + 6. It is 4 × 6."),
        6,
    )

    c3 = concept_block(
        "3. Divide, then add or subtract",
        [
            "Share first, then change one share — or share, then remove some groups.",
            "24 stickers, 4 kids, then each gets 2 more: 24 ÷ 4 = 6, 6 + 2 = 8 each.",
            "30 apples in 5 bags, take 1 bag away: 6 per bag, 4 bags left → 24, or 30 − 6 = 24.",
            "56 seats, 7 rows, 2 rows empty: 8 per row, 5 rows filled → 40.",
            "Decide whether the second step changes one group or the whole leftover.",
            "Draw the equal groups. Cross out or add on the picture.",
        ],
        lesson_figure(
            svg_tape([8, 8, 8, 8, 8], labels=["8", "8", "8", "8", "8"]),
            "40 cards to 5 players",
            "Share first: 40 ÷ 5 = 8 each. Then one player gives away 3, so that player has 8 − 3 = 5.",
        )
        + solved(1, "40 cards to 5 players, equal. One player gives away 3. How many does that player have?",
               ["40 ÷ 5 = 8 each.",
                "8 − 3 = 5 for that player."],
               "5")
        + solved(2, "27 kids in 9 teams. 2 teams leave. How many kids stay?",
                 ["27 ÷ 9 = 3 per team.",
                  "7 teams stay: 7 × 3 = 21."],
                 "21")
        + try_this("Picture the piles", "Draw the equal piles from step 1. Then change the picture for step 2."),
        11,
    )

    c4 = concept_block(
        "4. All four operations",
        [
            "Some stories mix two different equal-group piles.",
            "3 packs of 5 and 2 packs of 4: 15 + 8 = 23. Multiply twice, then add.",
            "Money: 2 toys at 8 dollars and a 5-dollar game: 16 + 5 = 21.",
            "You might × then −, or ÷ then × (remaining groups).",
            "Name the operations before you compute: ×, ×, +.",
            "If a number in the story is not used, you used the wrong plan — or the story had a distractor. Third-grade stories here use every needed number, not extra traps.",
        ],
        lesson_figure(
            svg_tape([15, 8], labels=["3 × 5 = 15", "2 × 4 = 8"]),
            "Two kinds of packs",
            "Multiply each kind of pack, then add the products: 15 + 8 = 23 stickers.",
        )
        + solved(1, "3 packs of 5 stickers and 2 packs of 4. How many stickers?",
               ["3 × 5 = 15.",
                "2 × 4 = 8.",
                "15 + 8 = 23."],
               "23")
        + solved(2, "5 boxes of 10 pencils. 12 used. How many left?",
                 ["5 × 10 = 50.",
                  "50 − 12 = 38."],
                 "38")
        + matching(
            [("two kinds of packs", "× , × , then +"),
             ("equal groups then used", "× then −"),
             ("split then change one group", "÷ then + or −"),
             ("2 × 8 + 5", "21")],
            vid="g3u5-c4-match",
        ),
        kid_tip("List the operations", "Write × then + in the margin before you touch the numbers."),
        16,
    )

    c5 = concept_block(
        "5. Draw a bar to plan",
        [
            "A tape or bar shows the whole and the parts.",
            "For equal groups, you can split a bar into equal pieces, or draw several same-size bars.",
            "For extras, add a small bar on the end. For used amounts, shade and cut a piece off.",
            "Label each bar with a number or a question mark.",
            "The ? sits on what the question asks, not on a leftover fact.",
            "If you cannot draw it, the operations are not clear yet. Reread.",
        ],
        lesson_figure(
            svg_tape([6, 6, 6, 6, 3], labels=["6", "6", "6", "6", "3"]),
            "4 packs of 6 plus 3 extra",
            "Four equal bars of 6 make 24. A small bar of 3 joins them: 24 + 3 = 27 crayons.",
        )
        + solved(1, "4 packs of 6 crayons plus 3 extra. Draw, then solve.",
               ["Four bars of 6, or one bar of 24.",
                "A small bar of 3 joins them.",
                "24 + 3 = 27."],
               "27")
        + step_reveal(
            ["What is the first whole or first set of equal groups?",
             "Draw it and label.",
             "How does the second action change the drawing?",
             "Write the second sentence. That answer is the ?."],
            vid="g3u5-c5-steps",
        ),
        try_this("Bars before numbers", "Sketch first for 20 seconds. Then compute. The sketch catches mix-ups."),
        21,
    )

    c6 = concept_block(
        "6. Does the answer make sense?",
        [
            "After you compute, ask: is this reasonable?",
            "If the story is 'how many in all' and your answer is smaller than one pack, a step was missed.",
            "Round to estimate: 5 bags of 8 is about 5 × 10 = 50, minus 6 is about 44. Exact 34 is a bit lower because 8 is less than 10 — still in the right neighborhood if you used 5×8=40.",
            "Check multiply with divide, and divide with multiply.",
            "Reread the question sentence only. Answer that, not a middle step.",
            "Hearts are for misses. Reasonableness saves hearts.",
        ],
        lesson_figure(
            svg_tape([22, 8], labels=["left 22", "ate 8"]),
            "30 snacks, then eat 8",
            "6 × 5 = 30 snacks in all. 30 − 8 = 22 leftover. 22 is less than 30 and more than 0, so it fits.",
        )
        + solved(1, "6 kids bring 5 snacks each. They eat 8. Could 22 leftover be right?",
               ["6 × 5 = 30 snacks.",
                "30 − 8 = 22.",
                "22 is less than 30 and more than 0. It fits."],
               "yes")
        + watch_out("Reporting the first product as the final answer",
                    "40 apples after multiplying is a stepping stone if some get eaten. Keep going."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Solve two-step + and − stories",
            "Multiply, then add or subtract",
            "Divide, then add or subtract",
            "Mix all four operations",
            "Plan with a bar drawing",
            "Check that the answer makes sense",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u5_questions()


# ===========================================================================
# UNIT 6: Fractions
# ===========================================================================

def _u6_questions():
    qs = []
    idx = 1

    unit_frac = [
        ("A whole split into 4 equal parts. One part is…", "1/4",
         "A unit fraction has 1 on top. 1/4 is one of 4 equal parts.", ["4/1", "1/2", "4/4"]),
        ("A whole split into 8 equal parts. One part is…", "1/8",
         "1/8 is one eighth.", ["1/4", "8/1", "1/3"]),
        ("A whole split into 3 equal parts. One part is…", "1/3",
         "1/3 is one third.", ["1/2", "3/1", "1/6"]),
        ("1/6 means 1 out of how many equal parts?", 6,
         "The bottom number names how many equal parts make the whole.", None),
        ("Which is a unit fraction?", "1/5",
         "Unit fractions have 1 as the numerator.", ["2/5", "3/4", "5/5"]),
    ]
    for text, ans, expl, dist in unit_frac:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    copies = [
        ("2/3 is how many copies of 1/3?", 2, "2/3 = 1/3 + 1/3. Two copies."),
        ("3/4 is how many copies of 1/4?", 3, "Three fourths means three 1/4 pieces."),
        ("5/6 is how many copies of 1/6?", 5, "Five sixths."),
        ("4/4 is how many copies of 1/4?", 4, "Four fourths fill the whole."),
        ("1/2 + 1/2 = ?", "1",
         "Two halves make 1 whole.", ["1/4", "2/4", "0"]),
        ("1/4 + 1/4 + 1/4 = ?", "3/4",
         "Three copies of 1/4.", ["1/4", "1/3", "4/4"]),
        ("2/5 means…", "two fifths",
         "2 copies of 1/5.", ["two halves", "five seconds", "one fifth"]),
        ("The top number of a fraction counts…", "how many unit pieces",
         "Numerator = how many copies of 1/b.", ["the size of the whole only", "place value", "hours"]),
    ]
    for item in copies:
        if len(item) == 4:
            text, ans, expl, dist = item
            qs.append(mq(text, ans, expl, idx, distractors=dist))
        else:
            text, ans, expl = item
            qs.append(mq(text, ans, expl, idx))
        idx += 1

    number_line = [
        ("On a number line from 0 to 1 split into 4 equal jumps, the first jump lands on…", "1/4",
         "Each jump is 1/4.", ["1", "4/1", "0"]),
        ("The second jump of 1/4 lands on…", "2/4",
         "Two jumps of 1/4 is 2/4, which equals 1/2.", ["1/4", "4/2", "3/4"]),
        ("The fourth jump of 1/4 lands on…", "1",
         "4/4 = 1.", ["1/4", "2/4", "0"]),
        ("A line from 0 to 1 split into 3 equal parts. The point after two jumps is…", "2/3",
         "Two thirds of the way from 0 to 1.", ["1/3", "3/2", "1"]),
        ("0/4 on a number line is at…", "0",
         "Zero fourths is the start.", ["1", "1/4", "4"]),
        ("3/3 on a 0-to-1 thirds line is at…", "1",
         "Three thirds fill the whole.", ["0", "1/3", "2/3"]),
        ("Which is farther from 0 on the same 0-to-1 line: 1/2 or 1/4?", "1/2",
         "1/2 is halfway. 1/4 is only a quarter of the way.", ["1/4", "same", "0"]),
        ("Marks at 0, 1/2, and 1. Halfway from 0 to 1 is…", "1/2",
         "The middle mark is 1/2.", ["0", "1", "2"]),
    ]
    for text, ans, expl, dist in number_line:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    equiv = [
        ("2/4 of the same whole equals…", "1/2",
         "Two fourths cover the same as one half.", ["1/4", "2/2", "1/8"]),
        ("2/6 of the same whole equals…", "1/3",
         "Two sixths match one third.", ["2/3", "1/6", "3/6"]),
        ("3/6 of the same whole equals…", "1/2",
         "Three sixths is half.", ["1/6", "3/3", "2/6"]),
        ("4/8 of the same whole equals…", "1/2",
         "Four eighths is half.", ["1/8", "4/4", "2/8"]),
        ("2/2 equals…", "1",
         "Two halves fill the whole.", ["1/2", "2/4", "0"]),
        ("3/3 equals…", "1",
         "Three thirds fill the whole.", ["1/3", "2/3", "0"]),
        ("4/4 equals…", "1",
         "Four fourths fill the whole.", ["1/4", "2/4", "0"]),
        ("6/6 equals…", "1",
         "A whole number 1 can be written as n/n.", ["1/6", "6", "0"]),
        ("The whole number 2 as halves is…", "4/2",
         "Two wholes = four halves. 2 = 2/1 = 4/2.", ["2/2", "1/2", "2/4"]),
        ("3 as thirds is…", "9/3",
         "Three wholes = nine thirds.", ["3/3", "1/3", "3/1"]),
        ("3/1 equals the whole number…", 3,
         "3/1 means three wholes.", ["1", "1/3", "0"]),
        ("1/1 equals…", 1, "One whole.", None),
    ]
    for item in equiv:
        if len(item) == 4:
            text, ans, expl, dist = item
            qs.append(mq(text, ans, expl, idx, distractors=dist))
        else:
            text, ans, expl = item
            qs.append(mq(text, ans, expl, idx))
        idx += 1

    compare = [
        ("Same whole. 3/8 vs 5/8. Which is greater?", "5/8",
         "Same size pieces (eighths). More pieces means more. 5 > 3.", ["3/8", "same", "1"]),
        ("Same whole. 1/6 vs 1/2. Which is greater?", "1/2",
         "Same numerator 1. Fewer pieces in the whole means each piece is bigger. Halves beat sixths.", ["1/6", "same", "1/8"]),
        ("Same whole. 1/3 vs 1/4. Which is greater?", "1/3",
         "Thirds are bigger pieces than fourths.", ["1/4", "same", "1"]),
        ("Same whole. 2/5 vs 4/5. Which is greater?", "4/5",
         "Same denominator. 4 pieces > 2 pieces.", ["2/5", "same", "1/5"]),
        ("Same whole. 1/8 vs 1/4. Which is greater?", "1/4",
         "1/4 = 2/8, which is more than 1/8.", ["1/8", "same", "0"]),
        ("Same pizza. 3/4 vs 1/4. Which is more?", "3/4",
         "Three slices vs one slice of the same size.", ["1/4", "same", "1/2"]),
        ("You cannot fairly compare 1/2 of a tiny cracker and 1/2 of a huge cake because…", "the wholes are different",
         "Fractions need the same whole to compare size.", ["halves are always equal objects", "cakes are thirds", "crackers are eighths"]),
        ("Same whole. 2/6 vs 1/3. Compare.", "equal",
         "2/6 = 1/3.", ["2/6 greater", "1/3 greater", "cannot say"]),
    ]
    for text, ans, expl, dist in compare:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"How many copies of 1/{2 + (i % 5)} make {(1 + (i % 3))}/{2 + (i % 5)}?",
        1 + (i % 3),
        f"The top number counts copies of the unit fraction. {(1 + (i % 3))}/{2 + (i % 5)} is {1 + (i % 3)} copies of 1/{2 + (i % 5)}.",
        i,
    ))


def build_unit6():
    title = "Third Grade Math Unit 6: Fractions"
    description = (
        "Name unit fractions, build fractions as copies of unit fractions, place them on a number line, "
        "find equivalents, write wholes as fractions, and compare on the same whole."
    )

    c1 = concept_block(
        "1. Unit fractions",
        [
            "A unit fraction names one equal piece of a whole: 1/2, 1/3, 1/4, 1/6, 1/8.",
            "The bottom number (denominator) tells how many equal parts make the whole.",
            "The top number (numerator) is 1 for a unit fraction. It counts one piece.",
            "More parts mean smaller pieces. 1/8 is smaller than 1/4 of the same whole.",
            "Fold a paper into equal parts. One part is the unit fraction.",
            "Every other fraction is built from unit fractions.",
        ],
        lesson_figure(
            svg_fraction_bar(1, 8),
            "One of 8 equal pieces",
            "A sandwich cut into 8 equal parts. One piece is the unit fraction 1/8.",
        )
        + solved(1, "A sandwich is cut into 8 equal pieces. What is one piece called?",
               ["8 equal parts → eighths.",
                "One piece is 1/8."],
               "1/8")
        + matching(
            [("1/2", "one half"), ("1/3", "one third"),
             ("1/4", "one fourth"), ("1/8", "one eighth")],
            vid="g3u6-c1-match",
        ),
        kid_tip("Bottom = how many pieces in the whole", "If the whole is cut into 6 equal parts, unit pieces are sixths.")
        + phet_box("frac_intro"),
        1,
    )

    c2 = concept_block(
        "2. Fractions as copies of a unit fraction",
        [
            "3/4 means three copies of 1/4. 1/4 + 1/4 + 1/4 = 3/4.",
            "The numerator counts how many unit pieces you have.",
            "5/6 is five sixths, not five wholes.",
            "If the numerator equals the denominator, you have the whole: 4/4 = 1.",
            "If the numerator is 0, you have none of the parts: 0/4 = 0.",
            "Shade unit pieces one by one to build the fraction.",
        ],
        lesson_figure(
            svg_fraction_bar(3, 4),
            "Three copies of 1/4",
            "3/4 means three of four equal pieces: 1/4 + 1/4 + 1/4. The numerator counts unit pieces.",
        )
        + solved(1, "What is 3/4 in unit pieces?",
               ["Unit piece is 1/4.",
                "Take 3 copies: 1/4 + 1/4 + 1/4.",
                "That is 3/4."],
               "3 copies of 1/4")
        + solved(2, "2/5 means how many fifths?",
                 ["Numerator 2.",
                  "Two fifths."],
                 "2")
        + phet_box("build_frac"),
        try_this("Say it in units", "Read 5/6 as 'five copies of one sixth' until it feels natural."),
        6,
    )

    c3 = concept_block(
        "3. Fractions on a number line",
        [
            "A number line from 0 to 1 can show fractions of one whole.",
            "Split the segment into equal jumps. Each jump is a unit fraction.",
            "Four equal jumps: 0, 1/4, 2/4, 3/4, 1.",
            "2/4 sits at the same point as 1/2. That is equivalence on a line.",
            "The fraction is the point you land on, not the tick count alone — count the jumps from 0.",
            "You can also go past 1: 5/4 is one whole and one fourth more. We focus near 0 to 1, plus wholes as fractions.",
        ],
        lesson_figure(
            _frac_line(3, 2),
            "2/3 on a 0-to-1 line",
            "Three equal jumps from 0 to 1. Each jump is 1/3. Two jumps land on 2/3.",
        )
        + solved(1, "A 0-to-1 line is split into 3 equal jumps. Where is 2/3?",
               ["Each jump is 1/3.",
                "Two jumps from 0 land on 2/3."],
               "2/3")
        + step_reveal(
            ["Mark 0 and 1.",
             "Cut the space into b equal lengths.",
             "Each length is 1/b.",
             "Count a jumps to plot a/b."],
            vid="g3u6-c3-steps",
        ),
        watch_out("Counting tick marks instead of spaces",
                  "Four equal parts need four gaps, which make five marks (including 0 and 1). Count the spaces."),
        11,
    )

    c4 = concept_block(
        "4. Equivalent fractions",
        [
            "Equivalent fractions name the same amount of the same whole.",
            "1/2 = 2/4 = 3/6 = 4/8. Same area, different slice size.",
            "You can see this by stacking pictures or by matching points on a number line.",
            "Cutting every piece into 2 makes twice as many pieces: 1/2 → 2/4.",
            "The number looks different. The amount is the same.",
            "Use Fraction Matcher to pair pictures that match.",
        ],
        lesson_figure(
            svg_fraction_bar(2, 4) + svg_fraction_bar(1, 2),
            "2/4 and 1/2 of the same whole",
            "Two of four equal parts cover half the bar. Same amount, different slice size: 2/4 = 1/2.",
        )
        + solved(1, "Does 2/4 equal 1/2 of the same sandwich?",
               ["Two of four equal parts cover half.",
                "Yes. 2/4 = 1/2."],
               "yes")
        + matching(
            [("1/2", "2/4"), ("1/3", "2/6"), ("1/4", "2/8"), ("1", "4/4")],
            vid="g3u6-c4-match",
        ),
        phet_box("frac_match"),
        16,
    )

    c5 = concept_block(
        "5. Whole numbers as fractions",
        [
            "A whole can be written as a fraction.",
            "1 = 2/2 = 3/3 = 4/4 = 6/6. Any n/n is 1 whole.",
            "2 = 2/1 (two wholes). Also 2 = 4/2 (four halves).",
            "3 = 3/1 = 6/2 = 9/3.",
            "The fraction bar means 'divided by', so 6/2 is 6 ÷ 2 = 3. That matches.",
            "Seeing 4/4 as 1 helps you know when a shape is fully shaded.",
        ],
        lesson_figure(
            svg_fraction_bar(4, 4),
            "Four fourths make 1",
            "When the numerator equals the denominator, every piece is shaded. 4/4 = 1 whole.",
        )
        + solved(1, "Write 1 as fourths.",
               ["Four fourths fill one whole.",
                "1 = 4/4."],
               "4/4")
        + solved(2, "3/1 is the whole number…",
                 ["Three copies of 1 whole.",
                  "3."],
                 "3")
        + kid_tip("n/n is 1", "If top and bottom match, you have exactly one whole."),
        21,
    )

    c6 = concept_block(
        "6. Compare fractions (same whole)",
        [
            "Compare fractions only when they describe the same whole.",
            "Same denominator: the larger numerator is greater. 5/8 > 3/8 because more same-size pieces.",
            "Same numerator 1: the smaller denominator is greater. 1/3 > 1/4 because fewer cuts make bigger pieces.",
            "Use a number line: farther right is greater (between 0 and 1).",
            "Equivalent fractions compare as equal: 2/6 = 1/3.",
            "Do not compare 1/2 of a cracker with 1/2 of a cake as the same size. Different wholes.",
        ],
        lesson_figure(
            svg_fraction_bar(5, 8) + svg_fraction_bar(3, 8),
            "Same pizza, more eighths",
            "Pieces are the same size (eighths). 5 shaded > 3 shaded, so 5/8 > 3/8.",
        )
        + solved(1, "Same pizza. 3/8 or 5/8 — which is more?",
               ["Pieces are the same size (eighths).",
                "5 pieces > 3 pieces.",
                "5/8."],
               "5/8")
        + solved(2, "Same whole. 1/6 or 1/2 — which is more?",
                 ["Unit fractions: bigger piece has smaller bottom number.",
                  "1/2 is larger."],
                 "1/2")
        + matching(
            [("same bottom, 4/5 vs 2/5", "4/5 greater"),
             ("same top 1, 1/3 vs 1/4", "1/3 greater"),
             ("2/4 vs 1/2", "equal"),
             ("need the same", "whole")],
            vid="g3u6-c6-match",
        ),
        try_this("Draw both on one rectangle", "Same-size rectangle twice. Shade each fraction. Your eyes compare.")
        + phet_box("frac_match"),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Name unit fractions 1/b",
            "Build a/b as copies of 1/b",
            "Place fractions on a number line",
            "Recognize equivalent fractions",
            "Write whole numbers as fractions",
            "Compare fractions of the same whole",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u6_questions()


# ===========================================================================
# UNIT 7: Area
# ===========================================================================

def _u7_questions():
    qs = []
    idx = 1

    count = [
        ("A rectangle is covered by 8 unit squares. What is the area?", 8,
         "Area is the number of unit squares that cover the shape."),
        ("3 rows of 4 unit squares. Area?", 12, "3 × 4 = 12 square units."),
        ("2 rows of 6 unit squares. Area?", 12, "2 × 6 = 12."),
        ("5 rows of 5 unit squares. Area?", 25, "5 × 5 = 25."),
        ("1 row of 9 unit squares. Area?", 9, "1 × 9 = 9."),
        ("4 rows of 3 unit squares. Area?", 12, "4 × 3 = 12."),
        ("6 rows of 2 unit squares. Area?", 12, "6 × 2 = 12."),
        ("A shape made of 11 unit squares. Area?", 11, "Count the squares: 11."),
        ("If each square is 1 square centimeter, 3×4 rectangle area is how many square cm?", 12,
         "12 square centimeters."),
        ("Unit squares must be the same…", "size",
         "Area uses same-size units.", ["color", "name", "border only"]),
    ]
    for item in count:
        if len(item) == 4:
            text, ans, expl, dist = item
            qs.append(mq(text, ans, expl, idx, distractors=dist))
        else:
            text, ans, expl = item
            qs.append(mq(text, ans, expl, idx))
        idx += 1

    lw = [
        (5, 4), (6, 3), (7, 2), (8, 4), (9, 3), (10, 5), (6, 6), (8, 3), (7, 5), (4, 9),
        (12, 3), (11, 2), (8, 5), (9, 4), (7, 6),
    ]
    for L, W in lw:
        qs.append(mq(
            f"A rectangle is {L} units long and {W} units wide. Area?",
            L * W,
            f"Area = length × width = {L} × {W} = {L * W} square units.",
            idx,
        ))
        idx += 1

    missing = [
        ("Area 24. Width 4. Length?", 6, "24 ÷ 4 = 6. Because 6 × 4 = 24."),
        ("Area 18. Length 6. Width?", 3, "18 ÷ 6 = 3."),
        ("Area 35. Length 7. Width?", 5, "35 ÷ 7 = 5."),
        ("Area 40. Width 5. Length?", 8, "40 ÷ 5 = 8."),
        ("Area 16. It is a square. Side length?", 4, "4 × 4 = 16."),
        ("Area 36. Square side?", 6, "6 × 6 = 36."),
        ("Area 21. Width 3. Length?", 7, "21 ÷ 3 = 7."),
        ("Area 32. Length 8. Width?", 4, "32 ÷ 8 = 4."),
    ]
    for text, ans, expl in missing:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    additive = [
        ("A big rectangle 4×6 plus a 2×3 stuck on. Total area?", 30,
         "24 + 6 = 30 square units."),
        ("L-shape: 3×5 rectangle and 2×2 square attached with no overlap. Area?", 19,
         "15 + 4 = 19."),
        ("Two 3×3 squares side by side, no overlap. Area?", 18,
         "9 + 9 = 18."),
        ("A 5×5 square with a 1×1 square cut out. Area left?", 24,
         "25 − 1 = 24."),
        ("Rectilinear: 10 + 8 unit squares joined. Area?", 18,
         "Add the areas: 18."),
        ("Split a 6×4 rectangle into two 6×2. Each small area?", 12,
         "6 × 2 = 12. Together 24, which matches 6×4."),
        ("Areas 12 and 9 joined with no overlap. Total?", 21, "12 + 9 = 21."),
        ("Whole 30. A 10-square-unit hole. Remaining area?", 20, "30 − 10 = 20."),
    ]
    for text, ans, expl in additive:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    stories = [
        ("A rug is 8 feet by 3 feet. Area in square feet?", 24, "8 × 3 = 24."),
        ("A garden is 5 m by 6 m. Area?", 30, "5 × 6 = 30 square meters."),
        ("Tiles are 1 square foot. A floor needs 7 rows of 9 tiles. How many tiles?", 63, "7 × 9 = 63."),
        ("A card is 4 cm by 6 cm. Area?", 24, "4 × 6 = 24 square cm."),
        ("Two same 3-by-4 paintings. Total area?", 24, "12 + 12 = 24."),
    ]
    for text, ans, expl in stories:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"A rectangle is {3 + (i % 6)} by {2 + (i % 5)}. Area?",
        (3 + (i % 6)) * (2 + (i % 5)),
        f"Multiply side lengths. Area is {(3 + (i % 6)) * (2 + (i % 5))} square units.",
        i,
    ))


def build_unit7():
    title = "Third Grade Math Unit 7: Area"
    description = (
        "Measure area with unit squares, use length × width for rectangles, find a missing side, and add areas of rectilinear shapes."
    )

    c1 = concept_block(
        "1. What is area?",
        [
            "Area is how much flat space a shape covers.",
            "We measure area in square units: unit squares that are all the same size.",
            "Cover the shape with unit squares. Count them. That count is the area.",
            "We say 12 square units, not just 12. The word square matters.",
            "A square centimeter is a tiny square 1 cm on each side. A square foot is 1 foot on each side.",
            "Gaps and overlaps ruin the count. Tiles should fit edge to edge.",
        ],
        lesson_figure(
            svg_rect(4, 2),
            "8 unit squares",
            "A 4-by-2 rectangle holds 8 same-size squares with no gaps. Area = 8 square units.",
        )
        + solved(1, "A shape is covered by 8 unit squares with no gaps. Area?",
               ["Count the squares.",
                "Area = 8 square units."],
               "8 square units")
        + matching(
            [("area", "space a shape covers"), ("unit square", "1 by 1 square"),
             ("8 squares cover it", "area 8"), ("say the unit", "square units")],
            vid="g3u7-c1-match",
        ),
        kid_tip("Cover, then count", "If you can tile it, you can measure it.")
        + phet_box("area"),
        1,
    )

    c2 = concept_block(
        "2. Count unit squares in arrays",
        [
            "When unit squares make an array, skip-count rows.",
            "3 rows of 4 squares: 4, 8, 12. Area 12.",
            "That is multiplication: rows × squares in each row.",
            "Turning the array does not change area. 3×4 and 4×3 both cover 12.",
            "Odd shapes: count every square. Some shapes are not full rectangles.",
            "Color a row, then skip-count to avoid double-counting.",
        ],
        lesson_figure(
            svg_rect(5, 5),
            "5 rows of 5 unit squares",
            "An array of squares: 5 × 5 = 25. Turning it does not change the area.",
        )
        + solved(1, "5 rows of 5 unit squares. Area?",
               ["5 × 5 = 25.",
                "A 5-by-5 square."],
               "25")
        + solved(2, "2 rows of 6. Area?",
                 ["2 × 6 = 12."],
                 "12")
        + phet_box("area_model"),
        try_this("Skip-count a row", "Count one row. Then hop that number for each extra row."),
        6,
    )

    c3 = concept_block(
        "3. Area of a rectangle: length × width",
        [
            "For a rectangle, area = length × width (or base × height).",
            "A 7-by-4 rectangle has area 28 square units.",
            "You are multiplying the two side lengths, which match the array.",
            "Units: if sides are in meters, area is square meters.",
            "A square is a rectangle with equal sides. Area = side × side.",
            "This formula only works for rectangles (and squares). Odd shapes need counting or splitting.",
        ],
        lesson_figure(
            svg_rect(8, 3),
            "Length 8, width 3",
            "For a rectangle, area = length × width. 8 × 3 = 24 square units.",
        )
        + solved(1, "A rectangle is 8 units long and 3 units wide. Area?",
               ["8 × 3 = 24 square units."],
               "24")
        + solved(2, "A square has side 6. Area?",
                 ["6 × 6 = 36 square units."],
                 "36")
        + matching(
            [("5 by 4", "20"), ("9 by 3", "27"), ("6 by 6", "36"), ("10 by 2", "20")],
            vid="g3u7-c3-match",
        ),
        watch_out("Adding the sides",
                  "5 + 4 is perimeter thinking. Area multiplies 5 × 4."),
        11,
    )

    c4 = concept_block(
        "4. Area is additive",
        [
            "You can split a shape into rectangles, find each area, then add.",
            "An L-shape might be a 3×5 and a 2×2. Areas 15 + 4 = 19 if they do not overlap.",
            "You can also find a big rectangle and subtract a missing piece.",
            "5×5 square minus a 1×1 hole: 25 − 1 = 24.",
            "No overlap, no gap, when you add pieces.",
            "This is how we find area of rectilinear figures (shapes made of rectangles).",
        ],
        lesson_figure(
            svg_rect(6, 4) + svg_rect(3, 2),
            "Two rectangles, no overlap",
            "A 4×6 piece is 24 square units. A 2×3 piece is 6. Add: 24 + 6 = 30.",
        )
        + solved(1, "A 4×6 rectangle with a 2×3 rectangle attached, no overlap. Total area?",
               ["4 × 6 = 24.",
                "2 × 3 = 6.",
                "24 + 6 = 30."],
               "30")
        + step_reveal(
            ["Draw a line to split the shape into rectangles.",
             "Find each rectangle's area with ×.",
             "Add those areas.",
             "If a piece is missing, subtract it from a larger rectangle."],
            vid="g3u7-c4-steps",
        ),
        kid_tip("Cut on graph paper", "The split line should follow the grid. Then multiply each part."),
        16,
    )

    c5 = concept_block(
        "5. Missing side",
        [
            "If you know area and one side, divide to find the other side.",
            "Area 24, width 4 → length 24 ÷ 4 = 6. Because 6 × 4 = 24.",
            "This uses the missing-factor idea from division.",
            "A square with area 16 has side 4, because 4 × 4 = 16.",
            "Check: multiply the sides you now have. You must get the area back.",
            "Stories: a garden of 35 square meters, one side 7 m → other side 5 m.",
        ],
        lesson_figure(
            svg_rect(8, 5),
            "Area 40, width 5",
            "One side is 5. The other side is the missing factor: 40 ÷ 5 = 8. Check: 8 × 5 = 40.",
        )
        + solved(1, "Area 40 square units. Width 5. Length?",
               ["40 ÷ 5 = 8.",
                "Check: 8 × 5 = 40."],
               "8")
        + solved(2, "A square has area 36. Side length?",
                 ["What times itself is 36?",
                  "6 × 6 = 36."],
                 "6")
        + try_this("Area ÷ known side", "The unknown side is the missing factor."),
        21,
    )

    c6 = concept_block(
        "6. Area stories",
        [
            "Rugs, gardens, tiles, and cards are area stories.",
            "Find two side lengths. Multiply. Label square units.",
            "Tile stories: rows × tiles per row = tiles needed (each tile is 1 square unit).",
            "Two paintings: find each area, then add.",
            "If the story gives area and one side, divide.",
            "Sketch a labeled rectangle. It keeps length and width from swapping with perimeter.",
        ],
        lesson_figure(
            svg_rect(8, 3),
            "Rug 8 ft by 3 ft",
            "Multiply the side lengths. Area = 8 × 3 = 24 square feet — not 24 feet.",
        )
        + solved(1, "A rug is 8 feet by 3 feet. Area?",
               ["8 × 3 = 24.",
                "24 square feet."],
               "24")
        + matching(
            [("garden 5 m by 6 m", "30 square m"), ("7 rows of 9 tiles", "63 tiles"),
             ("card 4 cm by 6 cm", "24 square cm"), ("two 3-by-4 paintings", "24")],
            vid="g3u7-c6-match",
        ),
        watch_out("Forgetting 'square'",
                  "24 feet would be a length. 24 square feet is an area. Write the full unit."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Define area with unit squares",
            "Count arrays of squares",
            "Use length × width",
            "Add areas of rectangle pieces",
            "Find a missing side from area",
            "Solve area stories",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u7_questions()


# ===========================================================================
# UNIT 8: Perimeter
# ===========================================================================

def _u8_questions():
    qs = []
    idx = 1

    add_sides = [
        ("A triangle has sides 3, 4, and 5. Perimeter?", 12, "3+4+5=12. Perimeter is the distance around."),
        ("A square has side 6. Perimeter?", 24, "6+6+6+6=24, or 4×6=24."),
        ("A rectangle is 5 by 3. Perimeter?", 16, "5+3+5+3=16, or 2×(5+3)=16."),
        ("Sides 2, 2, 2, 2, 2. Perimeter of this pentagon?", 10, "5×2=10."),
        ("A rectangle 8 by 1. Perimeter?", 18, "8+1+8+1=18."),
        ("Equilateral triangle side 7. Perimeter?", 21, "3×7=21."),
        ("Sides 10, 4, 10, 4. Perimeter?", 28, "A rectangle 10 by 4: 28."),
        ("A regular hexagon side 3. Perimeter?", 18, "6×3=18."),
        ("Sides 9, 6, 4. Perimeter?", 19, "9+6+4=19."),
        ("Square side 9. Perimeter?", 36, "4×9=36."),
    ]
    for text, ans, expl in add_sides:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    rect = [
        (7, 2), (9, 5), (10, 3), (6, 6), (12, 4), (8, 5), (11, 2), (15, 1), (9, 9), (4, 7),
    ]
    for L, W in rect:
        qs.append(mq(
            f"Rectangle {L} by {W}. Perimeter?",
            2 * (L + W),
            f"2 × ({L} + {W}) = {2 * (L + W)}.",
            idx,
        ))
        idx += 1

    vs_area = [
        ("A 4-by-4 square. Area?", 16, "4×4=16 square units."),
        ("A 4-by-4 square. Perimeter?", 16, "4×4=16 units around. Same number, different meaning."),
        ("A 6-by-2 rectangle. Area?", 12, "6×2=12 square units."),
        ("A 6-by-2 rectangle. Perimeter?", 16, "6+2+6+2=16 units."),
        ("Which measures the fence around a garden?", "perimeter",
         "Around the outside is perimeter.", ["area", "volume", "weight"]),
        ("Which measures the grass covering the garden?", "area",
         "The covering is area.", ["perimeter", "length only", "time"]),
        ("Two rectangles can have the same area and different perimeters. 6×2 area 12, perimeter 16. 4×3 area 12, perimeter?", 14,
         "4+3+4+3=14. Same area, shorter fence."),
        ("A 1-by-8 rectangle. Area 8. Perimeter?", 18, "1+8+1+8=18. Long and skinny has a large perimeter."),
    ]
    for item in vs_area:
        if len(item) == 4:
            text, ans, expl, dist = item
            qs.append(mq(text, ans, expl, idx, distractors=dist))
        else:
            text, ans, expl = item
            qs.append(mq(text, ans, expl, idx))
        idx += 1

    missing = [
        ("Perimeter 18. Rectangle width 3. Length?", 6,
         "2×(L+3)=18 → L+3=9 → L=6."),
        ("Perimeter 20. Square. Side?", 5, "4 × side = 20. Side 5."),
        ("Perimeter 24. Rectangle length 8. Width?", 4,
         "2×(8+W)=24 → 8+W=12 → W=4."),
        ("A triangle, two sides 5 and 7, perimeter 20. Third side?", 8,
         "5+7+? =20 → ?=8."),
        ("Perimeter 16. Square side?", 4, "16÷4=4."),
        ("Perimeter 30. Rectangle length 9. Width?", 6,
         "2×(9+W)=30 → 9+W=15 → W=6."),
        ("Regular pentagon perimeter 25. Side?", 5, "25÷5=5."),
        ("Perimeter 14. Rectangle 5 by ___. Width?", 2,
         "2×(5+W)=14 → 5+W=7 → W=2."),
    ]
    for text, ans, expl in missing:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    stories = [
        ("A playground is 10 m by 6 m. How much fence to go around once?", 32,
         "2×(10+6)=32 meters of fence."),
        ("A picture frame is 8 in by 5 in. Trim around the outside?", 26,
         "8+5+8+5=26 inches."),
        ("A square sandbox side 7 ft. Border length?", 28, "4×7=28 feet."),
        ("You walk around a 9-by-3 rectangle. How far?", 24, "2×(9+3)=24."),
        ("Three sides of a triangle are 6, 6, and 4. Distance around?", 16, "6+6+4=16."),
        ("A garden 12 by 4. Fence around. Length of fence?", 32, "2×(12+4)=32."),
        ("A sticker is 2 cm by 2 cm. Distance around?", 8, "4×2=8 cm."),
        ("Two same 3-by-3 squares sitting apart. Total perimeter of both?", 24,
         "Each perimeter 12. 12+12=24."),
    ]
    for text, ans, expl in stories:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"A rectangle is {5 + (i % 6)} by {2 + (i % 4)}. Perimeter?",
        2 * ((5 + (i % 6)) + (2 + (i % 4))),
        f"Add all four sides, or 2 × (length + width) = {2 * ((5 + (i % 6)) + (2 + (i % 4)))}.",
        i,
    ))


def build_unit8():
    title = "Third Grade Math Unit 8: Perimeter"
    description = (
        "Find distance around a shape, use rectangle and square formulas, compare perimeter with area, and find a missing side."
    )

    c1 = concept_block(
        "1. What is perimeter?",
        [
            "Perimeter is the distance around a shape.",
            "Walk the outline. Add the side lengths you travel.",
            "A fence around a garden, a frame around a picture, a border around a sticker — those are perimeters.",
            "Units are length units: cm, m, ft, in. Not square units.",
            "If a side is missing on the drawing, you may still know it from parallel sides of a rectangle.",
            "Trace with a finger. Count each side once.",
        ],
        lesson_figure(
            svg_triangle(3, 4, 5),
            "Sides 3, 4, and 5",
            "Perimeter is the distance around. Add every side once: 3 + 4 + 5 = 12.",
        )
        + solved(1, "A triangle has sides 3, 4, and 5. Perimeter?",
               ["Add the sides: 3 + 4 + 5.",
                "12."],
               "12")
        + matching(
            [("perimeter", "distance around"), ("area", "space inside"),
             ("fence", "perimeter"), ("grass cover", "area")],
            vid="g3u8-c1-match",
        ),
        kid_tip("Around, not inside", "Perimeter is the path. Area is the filling."),
        1,
    )

    c2 = concept_block(
        "2. Add all the sides",
        [
            "Polygon perimeter = sum of all sides.",
            "A pentagon with sides 2, 2, 2, 2, 2 has perimeter 10.",
            "A regular shape has equal sides: multiply side × number of sides.",
            "Regular hexagon side 3: 6 × 3 = 18.",
            "Equilateral triangle side 7: 3 × 7 = 21.",
            "List the sides and add. Check that you used every side once.",
        ],
        lesson_figure(
            svg_rect(6, 6),
            "Square with side 6",
            "Four equal sides. Walk the outline: 6 + 6 + 6 + 6 = 24, or 4 × 6 = 24.",
        )
        + solved(1, "A square has side 6. Perimeter?",
               ["Four equal sides.",
                "6 + 6 + 6 + 6 = 24, or 4 × 6 = 24."],
               "24")
        + solved(2, "Sides 9, 6, and 4. Perimeter?",
                 ["9 + 6 + 4 = 19."],
                 "19")
        + matching(
            [("square side 9", "36"), ("regular hexagon side 3", "18"),
             ("equilateral triangle side 7", "21"), ("sides 10 and 4, rectangle", "28")],
            vid="g3u8-c2-match",
        ),
        try_this("Tick each side", "Put a small tick as you add a side so you do not skip or double."),
        6,
    )

    c3 = concept_block(
        "3. Perimeter of a rectangle",
        [
            "A rectangle has two lengths and two widths.",
            "Perimeter = length + width + length + width, or 2 × (length + width).",
            "5 by 3: 5+3+5+3=16. Also 2×(5+3)=2×8=16.",
            "A square is a special rectangle: 2×(s+s)=4s.",
            "You only need two measurements: one length and one width. Opposite sides match.",
            "If a drawing shows only two sides, you can still find perimeter of a rectangle.",
        ],
        lesson_figure(
            svg_rect(8, 5),
            "Rectangle 8 by 5",
            "Two lengths and two widths. Perimeter = 2 × (8 + 5) = 2 × 13 = 26. (8 × 5 = 40 would be area.)",
        )
        + solved(1, "A rectangle is 8 by 5. Perimeter?",
               ["2 × (8 + 5) = 2 × 13 = 26."],
               "26")
        + solved(2, "A rectangle is 10 by 3. Perimeter?",
                 ["10 + 3 + 10 + 3 = 26."],
                 "26")
        + step_reveal(
            ["Write L and W.",
             "Add L + W.",
             "Double that sum.",
             "Label the unit (cm, m, ft…)."],
            vid="g3u8-c3-steps",
        ),
        watch_out("Using × like area",
                  "8 × 5 = 40 is the area. Perimeter doubles the sum 8+5."),
        11,
    )

    c4 = concept_block(
        "4. Perimeter vs area",
        [
            "Area fills. Perimeter wraps.",
            "A 4-by-4 square has area 16 square units and perimeter 16 units. Same number, different jobs.",
            "A 6-by-2 rectangle has area 12 and perimeter 16. A 4-by-3 rectangle has area 12 and perimeter 14.",
            "Same area, different perimeters. Skinny rectangles have more fence for the same filling.",
            "A garden's grass is area. The fence is perimeter.",
            "Always ask: around or inside?",
        ],
        lesson_figure(
            svg_rect(6, 2),
            "6-by-2: fill vs wrap",
            "Area fills: 6 × 2 = 12 square units. Perimeter wraps: 6+2+6+2 = 16 units. Same shape, different jobs.",
        )
        + solved(1, "A 6-by-2 rectangle. Give area and perimeter.",
               ["Area: 6 × 2 = 12 square units.",
                "Perimeter: 6+2+6+2 = 16 units."],
               "area 12, perimeter 16")
        + matching(
            [("fence", "perimeter"), ("paint the floor", "area"),
             ("6×2 area", "12"), ("6×2 perimeter", "16")],
            vid="g3u8-c4-match",
        ),
        kid_tip("Units tell you", "Square units → area. Plain length units around a shape → perimeter.")
        + phet_box("area"),
        16,
    )

    c5 = concept_block(
        "5. Missing side from perimeter",
        [
            "If you know perimeter and some sides, you can find a missing side.",
            "Square, perimeter 20: 20 ÷ 4 = 5. Each side is 5.",
            "Rectangle, perimeter 18, width 3: 2×(L+3)=18 → L+3=9 → L=6.",
            "Triangle, sides 5 and 7, perimeter 20: third side 20 − 12 = 8.",
            "Subtract the sides you know from the perimeter. Watch the 2× for rectangles.",
            "Check by adding all sides again, including the new one.",
        ],
        lesson_figure(
            svg_rect(8, 4),
            "Perimeter 24, length 8",
            "2 × (8 + W) = 24, so 8 + W = 12 and W = 4. Opposite sides of a rectangle match.",
        )
        + solved(1, "Perimeter 24. Rectangle length 8. Width?",
               ["2 × (8 + W) = 24.",
                "8 + W = 12.",
                "W = 4."],
               "4")
        + solved(2, "A square has perimeter 16. Side?",
                 ["16 ÷ 4 = 4."],
                 "4")
        + try_this("Halve first for rectangles", "Perimeter 30 → half is 15 → that is L+W. If L is 9, W is 6."),
        21,
    )

    c6 = concept_block(
        "6. Perimeter stories",
        [
            "Fence, trim, border, walk around, ribbon around — those words hint perimeter.",
            "A playground 10 m by 6 m needs 32 m of fence: 2×(10+6)=32.",
            "A square sandbox side 7 ft needs 28 ft of border.",
            "If you walk around twice, double the perimeter. (We keep one loop here.)",
            "Sketch and label L and W before you add.",
            "If the story asks how much grass, that is area, not fence.",
        ],
        lesson_figure(
            svg_rect(8, 5),
            "Picture 8 in by 5 in",
            "Trim goes around the outside. Add the sides: 8+5+8+5 = 26 inches of trim.",
        )
        + solved(1, "A picture is 8 in by 5 in. How much trim around the outside?",
               ["Perimeter: 8+5+8+5=26 inches of trim."],
               "26")
        + solved(2, "A garden is 12 by 4. Fence around once. How long?",
                 ["2 × (12 + 4) = 2 × 16 = 32."],
                 "32")
        + matching(
            [("playground fence 10 by 6", "32"), ("square sandbox side 7", "28"),
             ("walk 9 by 3 once", "24"), ("sticker 2 by 2", "8")],
            vid="g3u8-c6-match",
        ),
        watch_out("Fencing the area number",
                  "Do not use 10×6=60 as fence. 60 would be square meters of grass, not meters of fence."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Define perimeter as distance around",
            "Add all sides of a polygon",
            "Use 2 × (length + width) for rectangles",
            "Tell perimeter apart from area",
            "Find a missing side from perimeter",
            "Solve fence and border stories",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u8_questions()


def build_master():
    return f"""
<h1>Third Grade Math</h1>
<p>This is a full third-grade math path. We use <strong>short words</strong>, pictures, and lots of practice.</p>
<p>You will work with multi-digit numbers, multiply and divide within 100, solve multi-step stories, explore fractions, and measure area and perimeter. After each idea there are 5 quick questions. At the end of a unit there are 50 more. Hearts help you. Take your time.</p>
{page_break()}
<h2>The eight units</h2>
<ol>
<li>Unit 1 — Multi-Digit Numbers</li>
<li>Unit 2 — What Multiplication Means</li>
<li>Unit 3 — Multiplication Facts Within 100</li>
<li>Unit 4 — Division Within 100</li>
<li>Unit 5 — Multi-Step Word Problems</li>
<li>Unit 6 — Fractions</li>
<li>Unit 7 — Area</li>
<li>Unit 8 — Perimeter</li>
</ol>
<p>Start with place value and rounding. Multiplication and division are the big new operations. Stories mix them. Fractions, area, and perimeter finish the year.</p>
{page_break()}
<h2>How to learn</h2>
<p>Draw equal groups and arrays. Use a fact you know, then break a factor apart. Fold paper for fractions. Tile rectangles for area. Walk the outline for perimeter.</p>
<p>If a question feels hard, try a smaller number first. Then come back. You are building number sense — a feeling for how numbers work.</p>
"""
