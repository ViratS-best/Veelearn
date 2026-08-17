"""First Grade Math units 5–8: stories, time, measuring, shapes, plus master page."""

from __future__ import annotations

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
# UNIT 5: Number stories and missing numbers
# ===========================================================================

def _u5_questions():
    qs = []
    idx = 1

    stories_add = [
        ("Sam has 4 cars. Mia gives him 3 more. How many cars now?", 7, "4 + 3 = 7. Put together."),
        ("A nest has 5 eggs. 2 more eggs. How many eggs?", 7, "5 + 2 = 7."),
        ("You pick 6 flowers, then 4 more. How many flowers?", 10, "6 + 4 = 10. A nice ten."),
        ("3 red fish and 8 blue fish. How many fish in all?", 11, "3 + 8 = 11. Count on from 8."),
        ("A box has 9 crayons. You put in 6. How many crayons?", 15, "9 + 6 = 15. Make a ten: 9 + 1 + 5."),
    ]
    for text, ans, expl in stories_add:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    stories_sub = [
        ("10 birds sit. 3 fly away. How many birds are left?", 7, "10 − 3 = 7. Take away."),
        ("You have 8 grapes. You eat 2. How many grapes left?", 6, "8 − 2 = 6."),
        ("12 balloons. 5 pop. How many balloons left?", 7, "12 − 5 = 7."),
        ("15 kids play. 6 go home. How many kids still play?", 9, "15 − 6 = 9."),
        ("20 stickers. You give away 4. How many stickers left?", 16, "20 − 4 = 16."),
    ]
    for text, ans, expl in stories_sub:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    missing = [
        ("7 + ___ = 10. What number goes in the box?", 3, "7 + 3 = 10. The missing part is 3."),
        ("___ + 5 = 12. What number is missing?", 7, "7 + 5 = 12."),
        ("9 − ___ = 4. What number is missing?", 5, "9 − 5 = 4."),
        ("___ − 3 = 8. What number is missing?", 11, "11 − 3 = 8. The whole is 11."),
        ("6 + 6 = ___. What number is missing?", 12, "Double 6 is 12."),
    ]
    for text, ans, expl in missing:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    true_false = [
        ("Is 4 + 5 = 9 true?", "true", "4 + 5 is 9. The sentence is true.", ["false", "maybe", "4"]),
        ("Is 8 − 3 = 6 true?", "false", "8 − 3 is 5, not 6. The sentence is false.", ["true", "8", "3"]),
        ("Is 10 = 7 + 3 true?", "true", "Both sides are 10. Equal means the same amount.", ["false", "13", "7"]),
        ("Is 2 + 2 + 2 = 8 true?", "false", "2 + 2 + 2 = 6, not 8.", ["true", "2", "4"]),
        ("Is 6 + 4 = 5 + 5 true?", "true", "Both sides make 10. They are equal.", ["false", "9", "11"]),
    ]
    for text, ans, expl, dist in true_false:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    equal = [
        ("Which makes the same amount as 8? 5 + 3 or 5 + 2?", "5 + 3",
         "5 + 3 = 8. 5 + 2 = 7. Only 5 + 3 matches 8.", ["5 + 2", "2 + 2", "8 + 8"]),
        ("7 = 10 − ___. What goes in the blank?", 3, "10 − 3 = 7.", None),
        ("Which is equal to 9 + 1?", 10, "9 + 1 = 10.", ["11", "8", "91"]),
        ("4 + 6 is the same as 3 + ___.", 7, "4 + 6 = 10, so 3 + 7 = 10.", None),
        ("Does 12 = 12?", "yes", "A number is always equal to itself.", ["no", "maybe", "0"]),
    ]
    for row in equal:
        text, ans, expl = row[0], row[1], row[2]
        dist = row[3] if len(row) > 3 else None
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    compare_ops = [
        ("Which is more: 6 + 2 or 6 + 5?", "6 + 5", "6 + 5 = 11 and 6 + 2 = 8. 11 is more.",
         ["6 + 2", "same", "6"]),
        ("Which is less: 9 − 1 or 9 − 4?", "9 − 4", "9 − 4 = 5 and 9 − 1 = 8. 5 is less.",
         ["9 − 1", "same", "9"]),
        ("3 + 7 compared to 10. Are they equal?", "yes", "3 + 7 = 10. Equal.", ["no", "3 is more", "7 is more"]),
        ("Which sum is greater: 8 + 3 or 8 + 8?", "8 + 8", "11 vs 16. 16 is greater.", ["8 + 3", "same", "8"]),
        ("You have 5. A friend has 5 + 0. Who has more?", "same", "5 + 0 = 5. Same amount.",
         ["you", "friend", "0"]),
    ]
    for text, ans, expl, dist in compare_ops:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    extra_stories = [
        ("2 cats sit. 9 more cats come. How many cats?", 11, "2 + 9 = 11."),
        ("14 cookies. 6 are eaten. How many left?", 8, "14 − 6 = 8."),
        ("A tank has 7 fish, then 7 more. How many fish?", 14, "Double 7 is 14."),
        ("20 pencils. 9 are broken. How many are not broken?", 11, "20 − 9 = 11."),
        ("1 + 8 + 1 = ?", 10, "1 + 1 = 2, then 2 + 8 = 10. Or 8 + 2 = 10."),
        ("___ + 4 = 11.", 7, "7 + 4 = 11."),
        ("16 − 8 = ?", 8, "Double: 8 + 8 = 16, so 16 − 8 = 8."),
        ("There are 13 hats. 4 are red. How many are not red?", 9, "13 − 4 = 9."),
        ("5 + 5 + 5 = ?", 15, "Three fives. 10 + 5 = 15."),
        ("9 kids. 9 more kids. How many kids?", 18, "9 + 9 = 18."),
        ("18 − 9 = ?", 9, "Fact family of 9 + 9 = 18."),
        ("A box needs 10 toys. It has 6. How many more toys?", 4, "6 + 4 = 10. Missing part is 4."),
        ("3 + ___ = 3.", 0, "Adding 0 does not change the number."),
        ("12 − 0 = ?", 12, "Take away nothing. Still 12."),
        ("8 birds in a tree. 7 more land. How many birds?", 15, "8 + 7 = 15. Near double of 8 + 8."),
        ("Is 9 + 2 = 10 + 1 true?", "true", "Both sides are 11.", ["false", "12", "9"]),
        ("Which is true: 7 − 7 = 0 or 7 − 7 = 7?", "7 − 7 = 0", "All gone is 0.", ["7 − 7 = 7", "7 − 0 = 0", "7 + 7 = 0"]),
        ("4 red, 4 blue, 4 green blocks. How many blocks?", 12, "4 + 4 + 4 = 12."),
        ("You need 20. You have 15. How many more?", 5, "15 + 5 = 20."),
        ("11 − 5 = ?", 6, "5 + 6 = 11."),
        ("A shop has 8 buns. They bake 8 more. How many buns?", 16, "8 + 8 = 16."),
        ("19 − 10 = ?", 9, "Take 1 ten from 19. 9 ones left."),
        ("6 + 9 = ?", 15, "Make a ten: 6 + 4 = 10, then +5."),
        ("There were 17 grapes. 8 were eaten. How many left?", 9, "17 − 8 = 9."),
        ("___ − 6 = 6.", 12, "12 − 6 = 6. A double family."),
        ("2 + 2 + 6 = ?", 10, "2 + 2 = 4, then 4 + 6 = 10."),
        ("A team scores 5, then 6. How many points?", 11, "5 + 6 = 11."),
        ("14 kids. 7 are girls. How many boys if the rest are boys?", 7, "14 − 7 = 7."),
        ("Is 4 + 4 + 1 = 9 true?", "true", "8 + 1 = 9.", ["false", "8", "4"]),
        ("You have 3. You need 10. How many more?", 7, "3 + 7 = 10."),
        ("20 − 20 = ?", 0, "Take all away. 0 left."),
        ("9 + 0 + 8 = ?", 17, "9 + 8 = 17. Zero changes nothing."),
        ("A jar has 16 buttons. 9 fall out. How many in the jar?", 7, "16 − 9 = 7."),
        ("5 + 8 = ?", 13, "5 + 5 = 10, plus 3 more is 13. Or 8 + 5."),
        ("___ + 9 = 18.", 9, "9 + 9 = 18."),
        ("13 − 9 = ?", 4, "Count up from 9 to 13: 4 jumps."),
        ("1 + 2 + 3 + 4 = ?", 10, "1+4=5 and 2+3=5. 5+5=10."),
        ("There are 11 cups. You wash 2. How many still dirty?", 9, "11 − 2 = 9."),
        ("7 + 7 + 1 = ?", 15, "14 + 1 = 15."),
        ("A puzzle has 20 pieces. You placed 12. How many not placed?", 8, "20 − 12 = 8."),
        ("Is 6 + 7 = 7 + 6 true?", "true", "Turn-around facts. Both are 13.", ["false", "67", "76"]),
        ("8 − 8 + 5 = ?", 5, "8 − 8 = 0, then +5 = 5."),
        ("A pack has 10 cards. You get 4 more cards. How many cards?", 14,
         "10 + 4 = 14."),
        ("9 frogs. 3 hop away. 2 more hop away. How many frogs left?", 4, "9 − 3 = 6, then 6 − 2 = 4."),
        ("4 + 5 + 6 = ?", 15, "4 + 6 = 10, then +5 = 15."),
        ("You read 8 pages, then 7 pages. How many pages?", 15, "8 + 7 = 15."),
        ("16 − 7 = ?", 9, "7 + 9 = 16."),
        ("A bowl has 2 apples. Mom adds 9. How many apples?", 11, "2 + 9 = 11."),
        ("___ − 1 = 19.", 20, "20 − 1 = 19."),
        ("Equal or not: 9 − 2 and 6 + 1?", "equal", "Both are 7.", ["not equal", "9", "6"]),
    ]
    for row in extra_stories:
        text, ans, expl = row[0], row[1], row[2]
        dist = row[3] if len(row) > 3 else None
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"You have {i % 9 + 2} toys. You get 2 more. How many toys?",
        (i % 9 + 2) + 2,
        f"Put together: {(i % 9 + 2)} + 2 = {(i % 9 + 2) + 2}.",
        i,
    ))


def build_unit5():
    title = "First Grade Math Unit 5: Number Stories"
    description = (
        "Solve plus and minus stories, find missing numbers, tell if a number sentence is true, "
        "and know that equal means the same amount."
    )

    c1 = concept_block(
        "1. Plus stories",
        [
            "A plus story puts groups together. Look for words like more, and, in all, total.",
            "Find the two parts. Add them. That is how many in all.",
            "Write a number sentence: 4 + 3 = 7.",
            "Draw the story if the words feel long. Dots work. Circles work.",
            "The numbers can hide in names: Sam has 4. Mia has 3. Still 4 + 3.",
            "Check: does your answer make a bigger group? Plus stories grow the first amount.",
        ],
        lesson_figure(
            svg_dots(5, color="#6366f1", label="5 shells")
            + svg_dots(4, color="#f59e0b", label="4 more"),
            "Lila finds 4 more shells",
            "Start with 5. Add 4. Together: 5 + 4 = 9 shells.",
        )
        + solved(1, "Lila has 5 shells. She finds 4 more. How many shells?",
               ["Start amount: 5.",
                "More: 4.",
                "More means add. 5 + 4 = 9."],
               "9")
        + matching(
            [("more", "add"), ("in all", "add"), ("total", "add"), ("and then some more", "add")],
            vid="g1u5-c1-match",
        ),
        kid_tip("Underline the numbers", "Find the two amounts. Write them. Put a plus between them."),
        1,
    )

    c2 = concept_block(
        "2. Minus stories",
        [
            "A minus story takes some away, or compares, or finds a leftover part.",
            "Look for words like left, fly away, give away, eat, pop, how many more.",
            "How many left? Start with the whole. Take away. Count what remains.",
            "How many more? Find the difference. Subtract the smaller from the bigger.",
            "Write 10 − 3 = 7.",
            "Check: does your answer make sense? You should have less than you started, if things went away.",
        ],
        lesson_figure(
            svg_dots(7, color="#6366f1", label="7 left")
            + svg_dots(4, color="#cbd5e1", label="4 eaten"),
            "11 cupcakes, 4 eaten",
            "Gray dots are gone. Purple dots remain: 7. So 11 − 4 = 7.",
        )
        + solved(1, "There are 11 cupcakes. The class eats 4. How many cupcakes are left?",
               ["Whole: 11.",
                "Ate: 4. That part is gone.",
                "11 − 4 = 7 left."],
               "7")
        + step_reveal(
            ["Read the story twice.",
             "Circle the whole (how many at the start).",
             "Circle how many go away.",
             "Write a minus sentence.",
             "Solve. Check that the leftover is smaller."],
            vid="g1u5-c2-steps",
        ),
        watch_out("Adding on a take-away story",
                  "If things leave, pop, or get eaten, you subtract. Do not add those numbers together."),
        6,
    )

    c3 = concept_block(
        "3. Missing numbers in a box",
        [
            "Sometimes a number is hiding. 6 + ___ = 10.",
            "Ask: what plus 6 makes 10? Count up: 7, 8, 9, 10. That is 4 jumps. The box is 4.",
            "For ___ − 2 = 5, think: some number, take 2, land on 5. So the whole is 7. Because 5 + 2 = 7.",
            "Use a fact family. The three numbers belong together.",
            "You can draw a bar. Whole on top. Parts under it. One part missing.",
            "The equal sign still means both sides match.",
        ],
        lesson_figure(
            svg_number_line(8, 13, marks=[(8, "8"), (13, "13")], highlight=13),
            "Missing addend: 8 + ? = 13",
            "Start at 8. Count up to 13: five hops. The box is 5. Check: 8 + 5 = 13.",
        )
        + solved(1, "8 + ___ = 13.",
               ["Start at 8. Count up to 13.",
                "9, 10, 11, 12, 13. Five jumps.",
                "The missing number is 5. Check: 8 + 5 = 13."],
               "5")
        + solved(2, "___ − 4 = 9.",
                 ["The leftover is 9 after taking 4.",
                  "So the whole is 9 + 4 = 13.",
                  "Check: 13 − 4 = 9."],
                 "13")
        + try_this("Count up", "For a missing addend, start at the known part and count up to the whole."),
        11,
    )

    c4 = concept_block(
        "4. True or false number sentences",
        [
            "A number sentence can be true or false.",
            "4 + 2 = 6 is true. Both sides are 6.",
            "4 + 2 = 7 is false. The sides do not match.",
            "Work each side. Then compare.",
            "True means yes, it matches. False means no, it does not.",
            "Later we write 4 + 2 = 3 + 3. Both sides are 6. Still true!",
        ],
        lesson_figure(
            svg_dots(5, color="#6366f1", label="9 − 4 = 5")
            + svg_dots(6, color="#f59e0b", label="claimed 6"),
            "Is 9 − 4 = 6 true?",
            "Left group is 5 (the real take-away). Right group is 6. They do not match, so the sentence is false.",
        )
        + solved(1, "Is 9 − 4 = 6 true?",
               ["Work the left side: 9 − 4 = 5.",
                "5 is not 6.",
                "The sentence is false."],
               "false")
        + matching(
            [("3 + 3 = 6", "true"), ("10 − 1 = 8", "false"),
             ("5 = 5", "true"), ("2 + 2 = 22", "false")],
            vid="g1u5-c4-match",
        ),
        kid_tip("Do both sides", "Never guess. Solve, then look. Matching sides → true."),
        16,
    )

    c5 = concept_block(
        "5. Equal means the same amount",
        [
            "The equal sign is not a bell that means “now write the answer.”",
            "Equal means the same amount on both sides.",
            "You can write 7 = 7. You can write 10 = 6 + 4. You can write 5 + 5 = 3 + 7.",
            "Think of a balance scale. Both sides should weigh the same.",
            "If one side is more, they are not equal.",
            "This idea helps all of math, even when you are older.",
        ],
        lesson_figure(
            svg_tape([8, 2], labels=["8", "2"])
            + svg_tape([5, 5], labels=["5", "5"]),
            "8 + 2 and 5 + 5",
            "Both bars make 10. Same amount on each side, so they are equal.",
        )
        + solved(1, "Does 8 + 2 equal 5 + 5?",
               ["Left: 8 + 2 = 10.",
                "Right: 5 + 5 = 10.",
                "Same amount. Yes, they are equal."],
               "yes")
        + step_reveal(
            ["Look at both sides of =.",
             "Find the amount on the left.",
             "Find the amount on the right.",
             "If they match, write equal. If not, not equal."],
            vid="g1u5-c5-steps",
        ),
        phet_box("compare"),
        21,
    )

    c6 = concept_block(
        "6. Compare with plus and minus",
        [
            "You can compare answers of two problems.",
            "Which is more: 6 + 4 or 6 + 2? Work both. 10 is more than 8.",
            "Which is less: 12 − 1 or 12 − 5? 11 is more than 7, so 12 − 5 is less.",
            "If one addend stays the same and the other grows, the sum grows.",
            "If you subtract more, the leftover gets smaller.",
            "Use this to check stories: does “more kids came” make a bigger number? It should.",
        ],
        lesson_figure(
            svg_tape([9, 3], labels=["9", "+3"])
            + svg_tape([9, 8], labels=["9", "+8"]),
            "Compare 9 + 3 and 9 + 8",
            "Both start with 9. Adding 8 makes a longer bar than adding 3. 17 is greater than 12.",
        )
        + solved(1, "Which is greater: 9 + 3 or 9 + 8?",
               ["9 + 3 = 12.",
                "9 + 8 = 17.",
                "17 is greater. So 9 + 8 is greater."],
               "9 + 8")
        + watch_out("Comparing the small numbers only",
                    "Do not say 3 is less than 8 so you are done — unless the other number is the same. Work the whole sentence."),
        try_this("Same start", "If both problems start with 9, the one that adds more ends bigger."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Solve plus stories",
            "Solve minus stories",
            "Find a missing number",
            "Tell true from false",
            "Know what equal means",
            "Compare two number sentences",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u5_questions()


# ===========================================================================
# UNIT 6: Time
# ===========================================================================

def _u6_questions():
    qs = []
    idx = 1

    parts = [
        ("The short hand on a clock tells the:", "hour",
         "The short hand is the hour hand. It points to the hour.",
         ["minute", "second", "day"]),
        ("The long hand on a clock tells the:", "minutes",
         "The long hand is the minute hand.",
         ["hour", "year", "month"]),
        ("How many numbers are around a clock face?", 12,
         "A clock has numbers 1 to 12.", ["10", "24", "60"]),
        ("When the long hand points to 12, it is:", "o'clock",
         "Long hand on 12 means 0 minutes. It is something o'clock.",
         ["half past", "night", "zero hour"]),
        ("A clock has two main hands. How many hands is that?", 2,
         "Short hour hand and long minute hand. Two hands.", ["1", "3", "12"]),
    ]
    for text, ans, expl, dist in parts:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    hours = [
        ("The short hand is on 3. The long hand is on 12. What time?", "3:00",
         "Long hand on 12 means o'clock. Short hand on 3 means 3:00.",
         ["3:30", "12:03", "2:00"]),
        ("What time is 7 o'clock?", "7:00", "7 o'clock is 7:00. Minute hand on 12.", ["7:30", "12:07", "6:00"]),
        ("Short hand on 9, long hand on 12. Time?", "9:00", "9 o'clock.", ["9:30", "12:09", "10:00"]),
        ("Which time is noon on a school clock that shows 12 o'clock?", "12:00",
         "12:00 is twelve o'clock.", ["12:30", "1:00", "11:00"]),
        ("Short hand on 1, long hand on 12. Time?", "1:00", "1 o'clock.", ["1:30", "12:01", "2:00"]),
    ]
    for text, ans, expl, dist in hours:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    half = [
        ("Long hand on 6 means the minutes are:", "30",
         "From 12 to 6 is halfway around. That is 30 minutes. We say half past.",
         ["0", "6", "60"]),
        ("Short hand a little past 4, long hand on 6. Time?", "4:30",
         "Half past 4 is 4:30.", ["4:00", "6:04", "5:30"]),
        ("What time is half past 2?", "2:30", "Half past 2 is 2:30.", ["2:00", "3:30", "2:15"]),
        ("Half past 10 is:", "10:30", "The hour is 10. Thirty minutes.", ["10:00", "11:30", "12:10"]),
        ("Long hand on 6, short hand between 7 and 8. Time?", "7:30",
         "Halfway from 7 to 8. Half past 7. 7:30.", ["8:30", "7:00", "6:07"]),
    ]
    for text, ans, expl, dist in half:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    mix = [
        ("Which time is later: 2:00 or 2:30?", "2:30", "2:30 is half an hour after 2:00.", ["2:00", "same", "12:00"]),
        ("Which time is earlier: 5:00 or 5:30?", "5:00", "5:00 comes first. Then 5:30.", ["5:30", "same", "6:00"]),
        ("From 3:00 to 3:30, how many minutes pass?", 30, "Half an hour is 30 minutes.", ["12", "60", "3"]),
        ("From 8:00 to 9:00, how many minutes pass?", 60, "One whole hour is 60 minutes.", ["30", "12", "8"]),
        ("The clock shows 6:00. What will it show in 30 minutes?", "6:30",
         "Add a half hour. 6:00 becomes 6:30.", ["7:00", "6:00", "5:30"]),
    ]
    for text, ans, expl, dist in mix:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    digital = [
        ("A digital clock shows 4:00. That is:", "4 o'clock",
         "The number before the dots is the hour. 4:00 is 4 o'clock.",
         ["4:30", "12:04", "40 o'clock"]),
        ("A digital clock shows 4:30. That is:", "half past 4",
         ":30 means 30 minutes. Half past 4.", ["4 o'clock", "half past 3", "30 o'clock"]),
        ("Which digital time matches 9 o'clock?", "9:00", "O'clock is :00.", ["9:30", "12:09", "6:00"]),
        ("Which digital time matches half past 11?", "11:30", "Half past is :30.", ["11:00", "12:11", "10:30"]),
        ("On a digital clock, the two dots sit between the hour and the minutes. In 2:30 the hour is:", 2,
         "The first number is the hour. 2:30 starts with 2.", ["30", "5", "12"]),
    ]
    for text, ans, expl, dist in digital:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    order = [
        ("Which comes first in a school day: morning or afternoon?", "morning",
         "Morning is the start of the day. Afternoon is later.", ["afternoon", "midnight only", "both at once"]),
        ("Lunch is usually in the:", "afternoon or midday",
         "Lunch is around the middle of the day, often after morning lessons.",
         ["midnight", "only at 9:00", "never"]),
        ("If bedtime is 8:00 at night, is that morning?", "no",
         "Night and morning are different. 8:00 at night is evening.", ["yes", "maybe", "noon"]),
        ("You wake up, eat breakfast, then go to school. What time of day is breakfast?", "morning",
         "Breakfast is a morning meal.", ["afternoon", "midnight", "next week"]),
        ("Recess after lunch is in the:", "afternoon",
         "After lunch is afternoon.", ["morning", "before sunrise", "year"]),
    ]
    for text, ans, expl, dist in order:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    more_hours = [1, 2, 4, 5, 6, 8, 10, 11]
    for h in more_hours:
        qs.append(mq(
            f"Short hand on {h}, long hand on 12. What time?",
            f"{h}:00",
            f"O'clock. The hour is {h}. Write {h}:00.",
            idx,
            distractors=[f"{h}:30", f"12:{h:02d}", f"{h + 1}:00"],
        ))
        idx += 1
        qs.append(mq(
            f"What time is half past {h}?",
            f"{h}:30",
            f"Half past {h} is {h}:30. Minute hand on 6.",
            idx,
            distractors=[f"{h}:00", f"{h + 1}:30", f"6:{h:02d}"],
        ))
        idx += 1

    later = [(1, "1:00", "1:30"), (3, "3:00", "3:30"), (6, "6:30", "7:00"), (9, "9:00", "9:30"),
             (11, "11:30", "12:00"), (12, "12:00", "12:30"), (2, "2:30", "3:00"), (5, "5:30", "6:00"),
             (8, "8:00", "8:30"), (10, "10:30", "11:00")]
    for _h, start, nxt in later:
        qs.append(mq(
            f"The clock shows {start}. What time is 30 minutes later?",
            nxt,
            f"Add a half hour to {start}. Next is {nxt}.",
            idx,
            distractors=[start, "12:00", "6:00"],
        ))
        idx += 1

    words = [
        ("We say 5:00 as:", "five o'clock", " :00 is o'clock.", ["five thirty", "half past five", "fifty"]),
        ("We say 5:30 as:", "half past five", " :30 is half past.", ["five o'clock", "five twelve", "half past six"]),
        ("Minute hand on 12 means how many minutes?", 0, "O'clock. Zero extra minutes.", ["30", "12", "60"]),
        ("Minute hand on 6 means how many minutes?", 30, "Halfway. 30 minutes.", ["6", "0", "60"]),
        ("How many minutes in one hour?", 60, "A full trip around the clock is 60 minutes.", ["30", "12", "24"]),
        ("How many hours on a clock face?", 12, "Numbers 1 through 12.", ["24", "60", "10"]),
        ("The hour hand is shorter. True?", "true", "Short = hour. Long = minutes.", ["false", "same size", "no hands"]),
        ("At 12:00 the hands stack on 12. What time is that?", "12:00", "Both on 12 is 12 o'clock.", ["6:00", "12:30", "1:00"]),
        ("Which is closer to the next hour: 4:00 or 4:30?", "4:30", "4:30 is halfway to 5:00.", ["4:00", "same", "3:00"]),
        ("School starts at 8:00. That is:", "8 o'clock", "8:00 = 8 o'clock.", ["8:30", "half past 8", "18 o'clock"]),
        ("Half past 12 is:", "12:30", "12:30, often lunch time.", ["12:00", "1:30", "6:00"]),
        ("If it is 9:30 now, 30 minutes ago it was:", "9:00", "Back a half hour from 9:30 is 9:00.", ["10:00", "9:30", "8:30"]),
        ("Digital 7:00 matches analog hands at:", "7 o'clock", "Hour 7, minutes 00.", ["7:30", "12:07", "6:00"]),
        ("The long hand is on 12. The short hand is on 6. Time?", "6:00", "6 o'clock.", ["6:30", "12:06", "12:00"]),
        ("We sleep at night. A common bedtime like 8:00 at night is written:", "8:00",
         "The clock still shows 8:00. Night or morning is about the day, not the numbers.",
         ["8:30 only", "20 toys", "0:08"]),
        ("From 1:30 to 2:00, how many minutes?", 30, "Half an hour.", ["60", "1", "12"]),
        ("A clock that shows only 3:30 is at:", "half past 3", "3:30 = half past 3.", ["3 o'clock", "half past 4", "6:03"]),
        ("Which hand moves faster, the long one or the short one?", "long",
         "The minute hand (long) goes around faster than the hour hand.", ["short", "they never move", "the numbers"]),
        ("If the short hand is almost on 5 and the long hand is on 6, the hour is still:", 4,
         "At 4:30 the hour hand is halfway to 5, but the hour is still 4 until 5:00.",
         ["5", "6", "12"]),
        ("Write half past 1 in digital form.", "1:30", "Half past 1 = 1:30.", ["1:00", "2:30", "1:15"]),
    ]
    for row in words:
        qs.append(mq(row[0], row[1], row[2], idx, distractors=row[3] if len(row) > 3 else None))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"What time is {1 + (i % 12)} o'clock?",
        f"{1 + (i % 12)}:00",
        f"O'clock means :00. So {1 + (i % 12)}:00.",
        i,
        distractors=[f"{1 + (i % 12)}:30", "12:00", f"{((i % 12) + 2)}:00"],
    ))


def build_unit6():
    title = "First Grade Math Unit 6: Telling Time"
    description = (
        "Clock hands, time to the hour, time to the half hour, digital clocks, and putting events in order."
    )

    c1 = concept_block(
        "1. Parts of a clock",
        [
            "A clock face has numbers 1 to 12 in a circle.",
            "The short hand is the hour hand. It tells the hour.",
            "The long hand is the minute hand. It tells the minutes.",
            "When we say o'clock, the long hand points to 12.",
            "The hands move to the right (clockwise).",
            "There are 60 minutes in one hour. The long hand goes all the way around in 60 minutes.",
        ],
        lesson_figure(
            svg_clock(3, 0),
            "A clock at 3:00",
            "The short blue hand is the hour hand (on 3). The long red hand is the minute hand (on 12). Long hand on 12 means o'clock.",
        )
        + solved(1, "Which hand tells the hour?",
               ["Hour is a short word. The hour hand is the short hand.",
                "Minutes need a longer trip around the clock. That hand is long."],
               "the short hand")
        + matching(
            [("short hand", "hours"), ("long hand", "minutes"),
             ("12 at the top", "o'clock when the long hand is there"), ("6 at the bottom", "half past when the long hand is there")],
            vid="g1u6-c1-match",
        ),
        kid_tip("Short hour, long minutes", "Remember: the short hand is in charge of the hour number."),
        1,
    )

    c2 = concept_block(
        "2. Time to the hour",
        [
            "O'clock means the long hand is on 12.",
            "Look at the short hand. That number is the hour.",
            "Short hand on 2, long hand on 12 → 2:00. We say two o'clock.",
            "We write hour, then two dots, then 00. Like 2:00.",
            "The short hand points right at the number at o'clock times.",
            "Practice every hour you see: 1:00, 2:00, 3:00… 12:00.",
        ],
        lesson_figure(
            svg_clock(8, 0),
            "Eight o'clock",
            "Short hand on 8. Long hand on 12. Write 8:00.",
        )
        + solved(1, "Short hand on 8. Long hand on 12. What time?",
               ["Long hand on 12 means o'clock.",
                "Short hand on 8 means 8.",
                "The time is 8:00. Eight o'clock."],
               "8:00")
        + step_reveal(
            ["Find the long hand first.",
             "Is it on 12? Then it is an o'clock time.",
             "Find the short hand.",
             "Read that hour number.",
             "Write it like 5:00."],
            vid="g1u6-c2-steps",
        ),
        try_this("Say it two ways", "Say “four o'clock” and write 4:00. Both are the same time."),
        6,
    )

    c3 = concept_block(
        "3. Time to the half hour",
        [
            "Half past means 30 minutes after the hour. The long hand points to 6.",
            "Why 6? Because 6 is halfway around the clock from 12.",
            "Half of 60 minutes is 30 minutes. We write :30.",
            "At half past, the short hand is halfway to the next hour. It is not still sitting on the number.",
            "Half past 4 is 4:30. The hour is still 4 until we reach 5:00.",
            "We say half past four, or four thirty.",
        ],
        lesson_figure(
            svg_clock(2, 30),
            "Half past 2",
            "Long hand points down at 6 (30 minutes). Short hand sits between 2 and 3. The hour is still 2: 2:30.",
        )
        + solved(1, "Long hand on 6. Short hand between 2 and 3. What time?",
               ["Long hand on 6 means 30 minutes. Half past.",
                "The hour we just passed is 2.",
                "Time is 2:30. Half past 2."],
               "2:30")
        + matching(
            [("long hand on 12", "o'clock / :00"), ("long hand on 6", "half past / :30"),
             ("2:00", "two o'clock"), ("2:30", "half past two")],
            vid="g1u6-c3-match",
        ),
        watch_out("Reading the next hour too soon",
                  "At 4:30 the short hand looks near 5. The hour is still 4. It becomes 5 only at 5:00."),
        11,
    )

    c4 = concept_block(
        "4. Hour vs half hour",
        [
            "Two pictures can look alike. Check the long hand.",
            "Long hand up (12) → o'clock. Long hand down (6) → half past.",
            "2:00 and 2:30 are 30 minutes apart.",
            "2:30 is later than 2:00. 3:00 is later than 2:30.",
            "A full hour later than 2:00 is 3:00. A half hour later than 2:00 is 2:30.",
            "Use this to talk about “in 30 minutes” and “in one hour.”",
        ],
        lesson_figure(
            svg_clock(5, 0) + svg_clock(5, 30),
            "5:00 then 5:30",
            "Left: minute hand up is 5:00. Right: minute hand down is 5:30. Half an hour later.",
        )
        + solved(1, "It is 5:00. What time is it in 30 minutes?",
               ["Start at 5:00.",
                "Add a half hour.",
                "Land on 5:30."],
               "5:30")
        + solved(2, "It is 5:30. What time is it in 30 minutes?",
                 ["Start at 5:30.",
                  "Add another half hour. That finishes the hour.",
                  "Land on 6:00."],
                 "6:00")
        + kid_tip("Up or down", "Minute hand up = o'clock. Minute hand down = half past."),
        16,
    )

    c5 = concept_block(
        "5. Digital clocks",
        [
            "A digital clock shows numbers, not hands.",
            "The first number is the hour. Then two dots. Then the minutes.",
            "7:00 is seven o'clock. 7:30 is half past seven.",
            "The two dots are just a separator. They are not a plus sign.",
            "Match analog and digital. Same time, two looks.",
            "If you see 12:30, that is half past 12.",
        ],
        lesson_figure(
            svg_clock(10, 30),
            "Digital 10:30 on an analog clock",
            "Hour 10, minutes 30. Same time as the digits 10:30. We say half past ten.",
        )
        + solved(1, "A digital clock shows 10:30. Say it in words.",
               ["Hour is 10.",
                "Minutes are 30.",
                "Half past ten, or ten thirty."],
               "half past 10")
        + matching(
            [("1:00", "1 o'clock"), ("1:30", "half past 1"),
             ("12:00", "12 o'clock"), ("12:30", "half past 12")],
            vid="g1u6-c5-match",
        ),
        try_this("Copy the clock", "When you see a wall clock, write the digital time on paper."),
        21,
    )

    c6 = concept_block(
        "6. Morning, afternoon, and order",
        [
            "Time is also about order. What happens first? Next? Last?",
            "Morning is the first part of the day. We wake up. We eat breakfast. We go to school.",
            "Afternoon is after lunch. Recess after lunch is afternoon.",
            "Night is for dinner, stories, and sleep.",
            "A clock number can happen two times in a full day (morning 8:00 and evening 8:00). First grade names the part of the day with words.",
            "Put events in order: wake up → school → lunch → home → bed.",
        ],
        lesson_figure(
            '''<svg viewBox="0 0 460 80" width="100%" style="max-width:460px" role="img">
  <rect x="8" y="24" width="140" height="36" fill="#fde68a" stroke="#0f172a"/>
  <text x="78" y="47" text-anchor="middle" font-size="13" font-weight="700">morning</text>
  <rect x="148" y="24" width="160" height="36" fill="#93c5fd" stroke="#0f172a"/>
  <text x="228" y="47" text-anchor="middle" font-size="13" font-weight="700">afternoon</text>
  <rect x="308" y="24" width="140" height="36" fill="#c4b5fd" stroke="#0f172a"/>
  <text x="378" y="47" text-anchor="middle" font-size="13" font-weight="700">night</text>
  <text x="78" y="18" text-anchor="middle" font-size="11">breakfast</text>
  <text x="228" y="18" text-anchor="middle" font-size="11">lunch later</text>
  <text x="378" y="18" text-anchor="middle" font-size="11">bed</text>
</svg>''',
            "A day in order",
            "Breakfast is in the morning bar. Lunch comes later. Morning happens first.",
        )
        + solved(1, "Which comes first: lunch or breakfast?",
               ["Breakfast is a morning meal.",
                "Lunch is later, near the middle of the day.",
                "Breakfast comes first."],
               "breakfast")
        + step_reveal(
            ["Think about your day.",
             "Morning: wake, breakfast, school start.",
             "Midday: lunch.",
             "Afternoon: more school, then home.",
             "Night: dinner and bed."],
            vid="g1u6-c6-steps",
        ),
        watch_out("Only looking at the number",
                  "8:00 in the morning is not bedtime. Use morning, afternoon, or night words with the clock time."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Name hour and minute hands",
            "Read o'clock times",
            "Read half-past times",
            "Tell hour times from half-hour times",
            "Read a digital clock",
            "Put events in day order",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u6_questions()


# ===========================================================================
# UNIT 7: Measuring length
# ===========================================================================

def _u7_questions():
    qs = []
    idx = 1

    compare = [
        ("A crayon is shorter than a broom. Which is longer?", "broom",
         "The broom is longer. The crayon is shorter.", ["crayon", "same", "a button"]),
        ("A mouse is shorter than a cat. Which is shorter?", "mouse",
         "Shorter means less length. The mouse is shorter.", ["cat", "same", "a bus"]),
        ("Two pencils are the same length. We say they are:", "equal in length",
         "Same length means equal length.", ["one is longer", "broken", "heavier"]),
        ("A paper clip is shorter than a shoe. Which is longer?", "shoe",
         "The shoe is longer.", ["paper clip", "same", "an ant"]),
        ("If stick A is longer than stick B, then stick B is:", "shorter",
         "Longer and shorter are partners.", ["longer too", "heavier", "a circle"]),
    ]
    for text, ans, expl, dist in compare:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    cubes = [
        ("A pencil is 6 cubes long. A crayon is 4 cubes long. Which is longer?", "pencil",
         "6 cubes is more than 4 cubes. The pencil is longer.", ["crayon", "same", "2 cubes"]),
        ("A book is 8 cubes long. How many cubes long is the book?", 8,
         "The measure is 8 cubes. Count the cubes that fit along the side.", ["80", "1", "18"]),
        ("A ribbon is 10 cubes long. A string is 7 cubes long. How many cubes longer is the ribbon?", 3,
         "10 − 7 = 3. The ribbon is 3 cubes longer.", ["17", "7", "10"]),
        ("You line up 5 cubes along a marker. The marker is how many cubes long?", 5,
         "The count of cubes is the length in cubes.", ["1", "50", "6"]),
        ("A path is 12 cubes long. You used 12 cubes with no gaps. Is that a fair measure?", "yes",
         "Same-size cubes, no gaps, no overlaps. Fair.", ["no", "only if they are different sizes", "never"]),
    ]
    for text, ans, expl, dist in cubes:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    clips = [
        ("A card is 7 paper clips long. How long is the card in paper clips?", 7,
         "Count the paper clips lined up end to end.", ["1", "70", "8"]),
        ("A bookmark is 4 clips. A ruler drawing is 9 clips. Which is longer?", "ruler drawing",
         "9 is more than 4.", ["bookmark", "same", "clips cannot measure"]),
        ("You need 6 clips to measure a toy. The toy is ___ clips long.", 6,
         "The number of units is the length.", ["1", "60", "5"]),
        ("Two kids measure a book. One uses 5 big clips. One uses 8 tiny clips. Can the numbers differ?", "yes",
         "Different size units give different counts. That is why we use same-size units.",
         ["no, always 5", "no, always 8", "length changed"]),
        ("Line clips with no gaps. Why?", "so the measure is fair",
         "Gaps skip space. Then the count is too small.", ["to make it pretty only", "because clips are circles", "no reason"]),
    ]
    for text, ans, expl, dist in clips:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    units = [
        ("Should you mix giant cubes and tiny cubes in one measure?", "no",
         "Use the same size unit all the way along the object.", ["yes", "only on Tuesdays", "maybe"]),
        ("If your cubes have big gaps, your count will be:", "too small",
         "You skipped space, so you used fewer cubes than you should.", ["too big", "perfect", "zero"]),
        ("If cubes overlap a lot, your count will be:", "too big",
         "You counted the same space more than once.", ["too small", "perfect", "negative"]),
        ("A fair measure uses:", "same-size units with no gaps",
         "Same size, end to end, start at one end, stop at the other.",
         ["random toys", "only one cube ever", "circles only"]),
        ("Why might two friends get different counts for the same desk?", "they used different size units",
         "Bigger units mean a smaller count. Smaller units mean a bigger count.",
         ["the desk grew", "counting is impossible", "desks have no length"]),
    ]
    for text, ans, expl, dist in units:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    order = [
        ("Order from shortest to longest: bus, bike, crayon.", "crayon, bike, bus",
         "Crayon is shortest. Then bike. Bus is longest.",
         ["bus, bike, crayon", "bike, bus, crayon", "crayon, bus, bike"]),
        ("Order from longest to shortest: ant, cat, car.", "car, cat, ant",
         "Car is longest. Ant is shortest.",
         ["ant, cat, car", "cat, car, ant", "ant, car, cat"]),
        ("A straw is 9 cubes. A stick is 9 cubes. Which is longer?", "same length",
         "Equal cube counts mean equal length (same cubes).", ["straw", "stick", "cannot tell"]),
        ("Three ribbons: 3 cubes, 10 cubes, 6 cubes. Which is longest?", "10 cubes",
         "The biggest count is the longest if units match.", ["3 cubes", "6 cubes", "none"]),
        ("Shortest of 2 cubes, 8 cubes, 5 cubes?", "2 cubes",
         "Smallest count is shortest.", ["8 cubes", "5 cubes", "15 cubes"]),
    ]
    for text, ans, expl, dist in order:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    estimate = [
        ("A new pencil looks about 7 cubes long. You measure and get 7. Your estimate was:", "close",
         "A good estimate is near the real count.", ["way off", "exact magic only", "wrong always"]),
        ("You guess a book is 3 cubes. You measure 12 cubes. The guess was:", "too small",
         "3 is much less than 12.", ["too big", "perfect", "not a length"]),
        ("Before you measure, it helps to:", "guess, then check",
         "Estimate first. Then line up units. Compare.", ["never guess", "only close your eyes", "skip measuring"]),
        ("A door is much taller than a cup. A smart guess: the door is ___ cubes than the cup.", "many more",
         "Taller/longer things need more of the same unit.", ["fewer", "zero", "the same always"]),
        ("You estimate 10 clips. You measure 9 clips. That estimate is:", "very close",
         "Off by 1 is close.", ["terrible", "off by 100", "not math"]),
    ]
    for text, ans, expl, dist in estimate:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    more = [
        (3, 5, "A toy is 3 cubes. A box is 5 cubes. Which is longer?", "box", "5 > 3."),
        (8, 8, "Both sides of a square tile are 8 cubes. Are the sides equal?", "yes", "8 = 8."),
        (11, 4, "A snake drawing is 11 cubes. A worm drawing is 4 cubes. How many cubes longer is the snake?", 7, "11 − 4 = 7."),
        (2, 9, "A key is 2 clips. A brush is 9 clips. Which is shorter?", "key", "2 is less than 9."),
        (6, 10, "A belt is 10 cubes. A strap is 6 cubes. Which is longer?", "belt", "10 cubes is longer."),
        (1, 7, "How many more cubes is 7 than 1?", 6, "7 − 1 = 6."),
        (12, 12, "Two strings are each 12 clips. Equal length?", "yes", "Same count, same unit."),
        (4, 14, "A path is 14 cubes. You walked 4 cubes. How many cubes left?", 10, "14 − 4 = 10."),
        (5, 5, "A side is 5 paper clips with no gaps. Length?", 5, "5 clips long."),
        (9, 3, "Three sticks: 9, 3, and 6 cubes. Longest?", 9, "9 is the biggest count."),
        (15, 10, "A rope is 15 cubes. A shorter rope is 10 cubes. Difference?", 5, "15 − 10 = 5."),
        (8, 2, "You need a stick longer than 8 cubes. Is 2 cubes long enough?", "no", "2 is shorter than 8."),
        (20, 1, "A wall is 20 cubes. A tile is 1 cube. The wall is much:", "longer", "20 vs 1."),
        (7, 6, "Almost the same: 7 cubes and 6 cubes. Which is a tiny bit longer?", 7, "7 is one more."),
        (13, 13, "Measure twice. First 13, then 13. The length is likely:", 13, "Same result twice is a good check."),
        (4, 8, "If you use cubes twice as long, the count gets:", "smaller", "Bigger units → smaller count."),
        (10, 5, "Half of a 10-cube stick, in cubes, is:", 5, "10 split in two equal parts is 5."),
        (16, 4, "A board is 16 cubes. Each small block is 4 cubes. How many blocks fit in a line?", 4, "16 ÷ 4 = 4. Four blocks."),
        (9, 12, "Order 9 cubes and 12 cubes: shorter first.", "9 then 12", "9 is shorter."),
        (18, 20, "Which is closer to 20 cubes: 18 cubes or 2 cubes?", 18, "18 is near 20."),
    ]
    for a, b, text, ans, expl in more:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    extras = [
        ("Start measuring at the end of the object, not past it. True?", "true",
         "Line the first unit up with the start.", ["false", "start in the middle", "skip the ends"]),
        ("A giant's foot and your cube will give the same count. True?", "false",
         "Different units, different counts.", ["true", "always 10", "length disappears"]),
        ("Cover a rectangle with same-size squares. Counting the squares tells how much space. This is like:",
         "using same-size units",
         "Same-size pieces let you count length or cover.", ["guessing colors", "telling time", "skip counting by 7 only"]),
        ("A straw is longer than a toothpick. The toothpick is:", "shorter",
         "Longer/shorter pair.", ["longer", "a clock", "3D only"]),
        ("You should not stretch a floppy string when you measure. Why?", "stretching changes the length",
         "Keep it straight but do not stretch.", ["strings have no length", "only cubes work", "clocks measure string"]),
        ("A table is about 15 pencils long. A book is about 3 pencils long. The table is:", "longer",
         "15 is more than 3.", ["shorter", "the same", "not comparable"]),
        ("Count units: 1, 2, 3, 4 along a stick. The stick is 4 units if they fit exactly. True?", "true",
         "The last number is the length.", ["false", "the length is 1", "the length is 5"]),
        ("Which tool is a same-size unit you can repeat?", "cubes of one size",
         "Repeat one unit end to end.", ["a mix of huge and tiny toys", "a clock hand", "a story problem"]),
        ("If three worms are 2, 5, and 9 cubes, the middle length is:", 5, "Order 2, 5, 9. Middle is 5.", ["2", "9", "16"]),
        ("A fair line of 8 clips has how many gaps between clips if they touch?", 0,
         "Touching means no gaps.", ["8", "7", "1"]),
        ("Estimate first when the object looks a little longer than 10 cubes. A smart guess might be:", 12,
         "A little more than 10, so near 11–13.", ["2", "100", "0"]),
        ("A square's sides are all the same length. If one side is 4 cubes, each side is:", 4,
         "Same length on every side of a square.", ["1", "8", "16"]),
        ("Longer means more length. Shorter means:", "less length",
         "Opposite words.", ["more length", "heavier only", "later on a clock"]),
        ("You measure a shoe with clips from heel to toe. That is the shoe's:", "length",
         "End to end is length.", ["time", "shape name only", "temperature"]),
        ("Two measures of the same pencil: 6 cubes and 6 cubes. You can trust:", 6,
         "Repeat measure matches.", ["16", "0", "60"]),
        ("A train of 1 cube is shorter than a train of 9 cubes. True?", "true", "1 < 9.", ["false", "same", "cannot say"]),
        ("Put objects in a line to compare length. Line up one end. Then look at the other end. True?", "true",
         "Fair compare: same starting line.", ["false", "start at different ends", "only weigh them"]),
        ("A paper clip chain of 11 vs a chain of 4. Longer chain?", 11, "More clips, longer chain (same clips).", ["4", "7", "0"]),
        ("Why do we learn to measure? To:", "tell how long things are with numbers",
         "Numbers let us compare and share length.", ["only to draw", "to tell 3:00", "to skip counting forever"]),
        ("If your unit is tiny, you will need:", "more units",
         "Small units fill the length with a bigger count.", ["fewer units always", "zero units", "clocks"]),
    ]
    for row in extras:
        qs.append(mq(row[0], row[1], row[2], idx, distractors=row[3] if len(row) > 3 else None))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"A stick is {3 + (i % 10)} cubes long. A straw is {2 + (i % 8)} cubes long. How many cubes is the stick?",
        3 + (i % 10),
        f"The stick's measure is {3 + (i % 10)} cubes.",
        i,
    ))


def build_unit7():
    title = "First Grade Math Unit 7: Measuring Length"
    description = (
        "Compare longer and shorter, measure with cubes and paper clips, use same-size units, "
        "order objects, and estimate then check."
    )

    c1 = concept_block(
        "1. Longer and shorter",
        [
            "Length is how long something is from end to end.",
            "Longer means more length. Shorter means less length.",
            "To compare two things, line up one end. Look at the other end.",
            "The one that sticks out farther is longer.",
            "If both ends match, they are the same length. Equal.",
            "Words: long, longer, longest. Short, shorter, shortest.",
        ],
        lesson_figure(
            '''<svg viewBox="0 0 400 90" width="100%" style="max-width:400px" role="img">
  <rect x="20" y="20" width="280" height="22" fill="#93c5fd" stroke="#1e3a8a"/>
  <text x="24" y="16" font-size="12">spoon — longer</text>
  <rect x="20" y="58" width="90" height="22" fill="#fde68a" stroke="#92400e"/>
  <text x="24" y="54" font-size="12">toothpick — shorter</text>
</svg>''',
            "Line up one end",
            "Both start at the same left edge. The spoon sticks out farther, so the spoon is longer.",
        )
        + solved(1, "A spoon and a toothpick. Which is usually longer?",
               ["Line them up in your mind at one end.",
                "The spoon sticks out farther.",
                "The spoon is longer. The toothpick is shorter."],
               "spoon")
        + matching(
            [("longer", "more length"), ("shorter", "less length"),
             ("same length", "equal"), ("line up one end", "fair compare")],
            vid="g1u7-c1-match",
        ),
        kid_tip("Same start", "Always start both objects at the same line. Then the other end tells the truth."),
        1,
    )

    c2 = concept_block(
        "2. Measure with cubes",
        [
            "We can count how many same-size cubes fit along an object.",
            "That count is the length in cubes.",
            "Start at one end. Place cubes end to end. No gaps. No overlaps.",
            "Stop at the other end. The last number you say is the length.",
            "A pencil might be 7 cubes long. A crayon might be 5 cubes long.",
            "Then you can say the pencil is 2 cubes longer. 7 − 5 = 2.",
        ],
        lesson_figure(
            svg_dots(6, color="#38bdf8", per_row=6, label="6 cubes along the marker"),
            "A marker is 6 cubes long",
            "Same-size cubes, end to end, no gaps. Count 1 through 6. The marker measures 6 cubes.",
        )
        + solved(1, "A marker fits 6 cubes along it. How long is the marker?",
               ["Cubes are the unit.",
                "Count: 1, 2, 3, 4, 5, 6.",
                "The marker is 6 cubes long."],
               "6 cubes")
        + step_reveal(
            ["Pick one cube size.",
             "Line the first cube with the start of the object.",
             "Place the next cube touching the first.",
             "Keep going with no gaps.",
             "Count the cubes. That is the length."],
            vid="g1u7-c2-steps",
        ),
        try_this("Write the unit", "Do not just write 6. Write 6 cubes. The unit matters."),
        6,
    )

    c3 = concept_block(
        "3. Measure with paper clips",
        [
            "Paper clips can be units too. So can tiles, or your thumb, if they are the same size.",
            "Line clips end to end along the object.",
            "A bookmark might be 4 paper clips long.",
            "If you use bigger clips, you will need fewer of them.",
            "If you use tiny clips, you will need more of them.",
            "The object did not change. The unit size changed. The count changed.",
        ],
        lesson_figure(
            svg_dots(7, color="#a78bfa", per_row=7, label="card: 7 clips")
            + svg_dots(4, color="#f59e0b", per_row=4, label="photo: 4 clips"),
            "Same unit: paper clips",
            "7 is more than 4, so the card is longer than the photo. Both used the same clip size.",
        )
        + solved(1, "A card is 7 paper clips long. A photo is 4 paper clips long. Which is longer?",
               ["Same unit: paper clips.",
                "7 is more than 4.",
                "The card is longer."],
               "card")
        + matching(
            [("more clips (same size)", "longer object"), ("fewer clips (same size)", "shorter object"),
             ("bigger unit", "smaller count"), ("smaller unit", "bigger count")],
            vid="g1u7-c3-match",
        ),
        watch_out("Mixing clip sizes",
                  "Do not mix giant clips and tiny clips in one line. Pick one size."),
        11,
    )

    c4 = concept_block(
        "4. Same-size units",
        [
            "A fair measure uses the same unit all the way.",
            "No gaps: you would skip space and get a count that is too small.",
            "No overlaps: you would count space twice and get a count that is too big.",
            "Start at the end, not past the end, and not after a hole.",
            "This is why rulers have equal spaces. First grade uses cubes and clips to feel that idea.",
            "Friends can get different numbers if they pick different units. That is okay if they name the unit.",
        ],
        lesson_figure(
            svg_dots(4, color="#38bdf8", per_row=4, label="4 big cubes")
            + svg_dots(12, color="#fbbf24", per_row=12, label="12 tiny cubes"),
            "Same pencil, different units",
            "Four big cubes cover the pencil. Twelve tiny cubes cover the same pencil. The object did not change. The unit size did.",
        )
        + solved(1, "Kai uses big cubes and gets 4. Ana uses tiny cubes and gets 12. Same pencil. Why?",
               ["The pencil is one length.",
                "Big cubes cover more length each, so fewer cubes.",
                "Tiny cubes cover less each, so more cubes.",
                "Both can be right for their unit."],
               "different size units")
        + kid_tip("Say the unit", "4 big cubes is not the same sentence as 12 tiny cubes. Always name what you used.")
        + phet_box("area"),
        16,
    )

    c5 = concept_block(
        "5. Order three objects",
        [
            "You can put three things in order by length.",
            "Shortest to longest. Or longest to shortest.",
            "Compare two first. Then compare the winner with the third.",
            "Or measure all three with the same unit. Then order the numbers.",
            "Example: 3 cubes, 9 cubes, 6 cubes → 3, 6, 9 from shortest to longest.",
            "The middle one is in between.",
        ],
        lesson_figure(
            '''<svg viewBox="0 0 420 130" width="100%" style="max-width:420px" role="img">
  <rect x="20" y="18" width="80" height="20" fill="#86efac" stroke="#0f172a"/>
  <text x="24" y="14" font-size="12">A — 4 cubes (shortest)</text>
  <rect x="20" y="58" width="140" height="20" fill="#93c5fd" stroke="#0f172a"/>
  <text x="24" y="54" font-size="12">C — 7 cubes</text>
  <rect x="20" y="98" width="200" height="20" fill="#c4b5fd" stroke="#0f172a"/>
  <text x="24" y="94" font-size="12">B — 10 cubes (longest)</text>
</svg>''',
            "Three ribbons, shortest to longest",
            "Line up the left ends. Order by how far they stick out: A (4), then C (7), then B (10).",
        )
        + solved(1, "Ribbon A is 4 cubes, B is 10 cubes, C is 7 cubes. Order shortest to longest.",
               ["Smallest number: 4. That is A.",
                "Next: 7. That is C.",
                "Biggest: 10. That is B.",
                "Order: A, C, B."],
               "A, C, B")
        + step_reveal(
            ["Use the same unit for all three.",
             "Write the three lengths.",
             "Find the smallest. That is shortest.",
             "Find the biggest. That is longest.",
             "The leftover is in the middle."],
            vid="g1u7-c5-steps",
        ),
        try_this("Line them up", "Put all three on a table. Line up one end. The other ends show the order."),
        21,
    )

    c6 = concept_block(
        "6. Estimate then check",
        [
            "Estimate means a smart guess before you measure.",
            "Look at the object. Think of a cube train you know, like 10 cubes.",
            "Is it about 10? A little more? A lot less?",
            "Then measure. See how close you were.",
            "Close guesses get better with practice. You are training your eyes.",
            "If you are way off, ask: did I pick a bad unit picture in my head?",
        ],
        lesson_figure(
            svg_dots(10, color="#cbd5e1", per_row=10, label="10-cube train in your head")
            + svg_dots(7, color="#38bdf8", per_row=7, label="measured: 7 cubes"),
            "Guess, then check",
            "The pencil looked a bit less than 10. A guess of 8 is close to the true 7 cubes.",
        )
        + solved(1, "A new pencil looks a bit less than 10 cubes. You guess 8. You measure 7. How was the guess?",
               ["7 is the true length in cubes.",
                "8 is only 1 away.",
                "That is a close estimate. Nice work."],
               "close")
        + watch_out("Skipping the measure",
                    "An estimate is not the final answer. Always check with real units when you can."),
        kid_tip("Ten-cube train", "Keep a train of 10 cubes in mind. Compare new objects to that train."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Compare longer and shorter",
            "Measure with cubes",
            "Measure with paper clips",
            "Use same-size units with no gaps",
            "Order three lengths",
            "Estimate, then measure",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u7_questions()


# ===========================================================================
# UNIT 8: 2D and 3D shapes
# ===========================================================================

def _u8_questions():
    qs = []
    idx = 1

    names = [
        ("A shape with 3 sides is a:", "triangle",
         "Tri means three. A triangle has 3 sides and 3 corners.",
         ["square", "circle", "cube"]),
        ("A shape that is round and has no sides is a:", "circle",
         "A circle is curved all the way. No corners.",
         ["square", "triangle", "rectangle"]),
        ("A square has how many sides?", 4,
         "A square has 4 equal sides and 4 square corners.", ["3", "5", "0"]),
        ("A rectangle has how many sides?", 4,
         "A rectangle has 4 sides and 4 square corners. Opposite sides match.",
         ["3", "8", "2"]),
        ("Which shape looks like a stop sign's cousin but with 4 equal sides? A:", "square",
         "Four equal sides. Four corners.", ["circle", "triangle", "sphere"]),
    ]
    for text, ans, expl, dist in names:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    sides = [
        ("How many corners does a triangle have?", 3, "3 sides, 3 corners.", ["4", "0", "5"]),
        ("How many corners does a square have?", 4, "4 corners, all square corners.", ["3", "8", "1"]),
        ("How many corners does a circle have?", 0, "A circle has no corners and no sides.", ["1", "2", "4"]),
        ("A rectangle has 4 corners. How many sides?", 4, "4 sides go with 4 corners.", ["3", "6", "0"]),
        ("Two sides meet at a:", "corner", "A corner is where sides meet.", ["circle", "sphere", "hour"]),
    ]
    for text, ans, expl, dist in sides:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    closed = [
        ("A closed shape has no gaps in the outline. A square is:", "closed",
         "You can color inside. The line meets itself.", ["open", "a clock", "3D only"]),
        ("A line that does not meet itself is:", "open",
         "Open shapes have ends that do not join.", ["closed", "a cube", "always a circle"]),
        ("Can you color inside a closed triangle without crossing a gap?", "yes",
         "Closed means the inside is trapped.", ["no", "only on Mondays", "only 3D"]),
        ("Which is closed?", "circle", "A circle joins all the way around.", ["a C shape", "a U shape", "a stray line"]),
        ("Sides of a rectangle make a closed path. True?", "true", "Four sides join end to end.", ["false", "open always", "no sides"]),
    ]
    for text, ans, expl, dist in closed:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    solid = [
        ("A ball is shaped like a:", "sphere",
         "A sphere is round like a ball. It rolls.", ["cube", "cone", "square"]),
        ("A dice is shaped like a:", "cube",
         "A cube has 6 square faces. Like a box with equal sides.", ["sphere", "circle", "triangle"]),
        ("An ice cream cone is shaped like a:", "cone",
         "A cone has a circle face and a point.", ["cube", "sphere", "rectangle"]),
        ("A can of soup is shaped like a:", "cylinder",
         "A cylinder has two circle faces and a curved side.", ["triangle", "square", "pyramid"]),
        ("Which solid can roll in any direction easily?", "sphere",
         "A sphere rolls every way. A cylinder rolls one way.", ["cube", "box", "book"]),
    ]
    for text, ans, expl, dist in solid:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    faces = [
        ("How many faces does a cube have?", 6, "A cube has 6 square faces. Like a die.", ["4", "8", "1"]),
        ("A cube's faces are what shape?", "squares", "Each face is a square.", ["circles", "triangles", "spheres"]),
        ("A cylinder has how many circle faces?", 2, "Top and bottom circles.", ["6", "0", "4"]),
        ("A cone has how many circle faces?", 1, "One circle on the bottom. A point on top.", ["2", "6", "3"]),
        ("Does a sphere have flat faces?", "no", "A sphere is curved all over. No flat faces.", ["yes, 6", "yes, 1", "yes, 4"]),
    ]
    for text, ans, expl, dist in faces:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    halves = [
        ("Two equal parts of a shape are called:", "halves",
         "Half and half. Two matching pieces.", ["fourths", "thirds", "hours"]),
        ("Four equal parts of a shape are called:", "fourths",
         "Fourths are also called quarters. Four matching pieces.", ["halves", "tens", "sides"]),
        ("If you share a sandwich into 2 equal parts, each part is:", "one half",
         "Two equal shares → halves.", ["one fourth", "the whole", "a cube"]),
        ("A square cut on both middle lines into 4 equal squares shows:", "fourths",
         "Four equal parts.", ["halves only", "circles", "hours"]),
        ("Are two parts always halves if they are not equal?", "no",
         "Halves must be equal. Same size.", ["yes", "only on circles", "only on cubes"]),
    ]
    for text, ans, expl, dist in halves:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    more = [
        ("A door looks most like a:", "rectangle", "Tall rectangle.", ["circle", "triangle", "sphere"]),
        ("A clock face looks most like a:", "circle", "Round face.", ["square only", "cube", "cone"]),
        ("A slice of pizza often looks like a:", "triangle", "Three sides, pointy piece.", ["cube", "sphere", "cylinder"]),
        ("A book looks most like a:", "rectangular prism / box", "A box shape with rectangle faces.", ["sphere", "cone", "circle"]),
        ("How many sides does a circle have?", 0, "No straight sides.", ["1", "4", "100"]),
        ("A square is a special rectangle because all sides are:", "equal",
         "Rectangle with 4 equal sides is a square.", ["curved", "open", "spheres"]),
        ("Count sides: a triangle has fewer sides than a square. True?", "true", "3 < 4.", ["false", "same", "0"]),
        ("Which solid has a point and can stack poorly on that point?", "cone",
         "The pointy end does not stack well.", ["cube", "box", "book"]),
        ("Which solid stacks well?", "cube", "Flat faces stack.", ["sphere", "ball", "soft blob"]),
        ("A soup can rolls. It is a:", "cylinder", "Circle ends, rolls sideways.", ["cube", "pyramid", "square"]),
        ("Corners on a rectangle:", 4, "Four corners.", ["3", "0", "6"]),
        ("A hexagon is not a first-grade must, but a square has how many fewer sides than 6?", 2,
         "6 − 4 = 2. A square has 4 sides.", ["6", "4", "8"]),
        ("Fold a paper square in half. Each part is a:", "half", "Two equal parts.", ["fourth only", "cube", "hour"]),
        ("Fold that half in half again. Now you have:", "fourths", "Four equal parts.", ["halves only", "tens", "circles"]),
        ("A pattern block triangle has 3 corners. Count them: 1, 2, 3. How many?", 3, "Three corners.", ["4", "5", "0"]),
        ("Which is 2D (flat)?", "circle", "You can draw it on paper. Flat.", ["sphere", "ball", "can"]),
        ("Which is 3D (solid)?", "cube", "You can hold it. It has faces.", ["square drawing", "triangle drawing", "circle drawing"]),
        ("A box of tissues is most like a:", "rectangular prism", "A box.", ["sphere", "cone", "circle"]),
        ("Put 2 same triangles together. They can make a:", "diamond or bigger triangle or rectangle",
         "Shapes compose. Two triangles can make a new shape.", ["a clock", "an hour", "a ten"]),
        ("A square has equal sides. If one side is 4 cubes, the opposite side is:", 4,
         "Opposite sides of a square match. All four match.", ["2", "8", "0"]),
        ("Does a triangle have a curved side? (basic triangle)", "no",
         "Basic triangles have 3 straight sides.", ["yes", "always a circle", "6 faces"]),
        ("A party hat is like a:", "cone", "Circle base and a point.", ["cube", "sphere", "square"]),
        ("Marbles are like:", "spheres", "Balls.", ["cubes", "cones", "rectangles"]),
        ("Building blocks that stack are often:", "cubes", "Cubes stack on square faces.", ["spheres", "water", "clocks"]),
        ("How many equal parts in halves?", 2, "Two equal parts.", ["4", "3", "10"]),
        ("How many equal parts in fourths?", 4, "Four equal parts.", ["2", "3", "8"]),
        ("One half plus one half makes:", "one whole", "Two halves = the whole shape.", ["one fourth", "zero", "four"]),
        ("Color 1 of 4 equal parts. You colored:", "one fourth", "1 out of 4 equal pieces.", ["one half", "the whole", "three fourths"]),
        ("A rectangle window has 4 sides. Two long, two short. Still a rectangle?", "yes",
         "Opposite sides equal. 4 square corners.", ["no, only squares", "only if it is a circle", "only 3D"]),
        ("The corner of a room is like a square corner. A square has corners that look:", "square / like an L",
         "Square corners are like the corner of a book.", ["round", "pointy like a spike only", "missing"]),
        ("Open shape example: the letter C. Closed shape example:", "O or a circle",
         "O is closed. C is open.", ["C also", "a stray dash", "the letter L"]),
        ("Count faces on a die (cube): 1,2,3,4,5,6. Total?", 6, "Six faces.", ["4", "8", "12"]),
        ("A cylinder standing up looks like a circle from the top. That top is a:", "face",
         "The circle is a flat face.", ["sphere", "hour", "ten"]),
        ("You cannot stack spheres easily because they:", "roll / are curved",
         "No flat face to sit still.", ["have 6 squares", "are triangles", "tell time"]),
        ("A picture of a square is 2D. A wooden block cube is:", "3D",
         "Solid. You can pick it up.", ["2D", "a number", "an hour"]),
        ("Sides of a square are equal. Corners of a square are:", "all the same square corners",
         "Four matching corners.", ["all different", "zero", "circles"]),
        ("A triangle cannot be a circle because a circle has:", "no straight sides",
         "Different defining parts.", ["3 sides too", "4 sides", "6 faces"]),
        ("Compose: 4 small squares can make one bigger:", "square",
         "Two by two small squares make a bigger square.", ["circle", "sphere", "hour"]),
        ("Split a rectangle through the middle the long way. Two parts are:", "halves if equal",
         "Equal areas/pieces → halves.", ["always fourths", "cubes", "minutes"]),
        ("Which has more sides, square or triangle?", "square", "4 vs 3.", ["triangle", "same", "circle"]),
        ("A cone has a curved surface and a:", "point and a circle face",
         "Point + circle.", ["six squares", "two balls", "12 hours"]),
        ("If both halves of a sandwich are the same size, sharing is:", "fair",
         "Equal parts are fair shares.", ["unfair", "3D only", "a clock"]),
        ("A stop-sign is not our main shape, but a square has ___ equal sides.", 4, "Four.", ["3", "0", "8"]),
        ("Find the shape with 0 corners:", "circle", "No corners.", ["square", "triangle", "rectangle"]),
        ("Find the solid that is round like a globe:", "sphere", "Globe = sphere.", ["cube", "box", "cone hat"]),
        ("A brick is most like a:", "box / rectangular prism", "Not a cube if sides differ, still a box.", ["sphere", "circle", "triangle"]),
        ("When we cover a shape with same-size squares, we are composing. True?", "true",
         "Putting shapes together.", ["false", "that is time", "that is subtraction only"]),
        ("A square cut into 2 equal triangles. Each triangle is:", "one half of the square",
         "Two equal parts of the whole square.", ["the whole square", "a cube", "one fourth of a circle"]),
        ("How many corners on a cube? (a cube has corners called vertices) First-grade count of pointy corners:", 8,
         "A cube has 8 corners. You can touch them.", ["6", "4", "1"]),
        ("A circle has ___ corners.", 0, "Zero corners.", ["4", "3", "2"]),
    ]
    for row in more:
        qs.append(mq(row[0], row[1], row[2], idx, distractors=row[3] if len(row) > 3 else None))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        "How many sides does a triangle have?",
        3,
        "A triangle has 3 sides.",
        i,
        distractors=["4", "0", "6"],
    ))


def build_unit8():
    title = "First Grade Math Unit 8: Shapes"
    description = (
        "Name 2D shapes, count sides and corners, know closed shapes, name 3D solids, "
        "count faces, and find halves and fourths."
    )

    c1 = concept_block(
        "1. Circles, squares, triangles, rectangles",
        [
            "Flat shapes live on paper. We call them 2D shapes.",
            "A circle is round. No sides. No corners.",
            "A triangle has 3 straight sides and 3 corners.",
            "A square has 4 equal sides and 4 square corners.",
            "A rectangle has 4 sides and 4 square corners. Opposite sides match. A square is a special rectangle.",
            "Look around the room. Windows, clocks, and signs hide these shapes.",
        ],
        lesson_figure(
            '''<svg viewBox="0 0 420 130" width="100%" style="max-width:420px" role="img">
  <circle cx="50" cy="56" r="36" fill="#e0e7ff" stroke="#312e81" stroke-width="2"/>
  <text x="50" y="112" text-anchor="middle" font-size="12">circle</text>
  <rect x="108" y="20" width="72" height="72" fill="#bbf7d0" stroke="#166534" stroke-width="2"/>
  <text x="144" y="112" text-anchor="middle" font-size="12">square</text>
  <polygon points="248,20 286,92 210,92" fill="#fde68a" stroke="#92400e" stroke-width="2"/>
  <text x="248" y="112" text-anchor="middle" font-size="12">triangle</text>
  <rect x="318" y="36" width="90" height="48" fill="#fecaca" stroke="#991b1b" stroke-width="2"/>
  <text x="363" y="112" text-anchor="middle" font-size="12">rectangle</text>
</svg>''',
            "Four flat shapes",
            "A yield sign is the triangle: 3 straight sides. Circle has none. Square and rectangle have 4.",
        )
        + solved(1, "A yield sign (the down triangle) has how many sides?",
               ["Look at the outline.",
                "Three straight sides.",
                "It is a triangle. 3 sides."],
               "3")
        + matching(
            [("circle", "round, no corners"), ("triangle", "3 sides"),
             ("square", "4 equal sides"), ("rectangle", "4 sides, opposite sides match")],
            vid="g1u8-c1-match",
        ),
        kid_tip("Count sides out loud", "Touch each side. Say 1, 2, 3… The last number names the shape family."),
        1,
    )

    c2 = concept_block(
        "2. Sides and corners",
        [
            "A side is a straight edge.",
            "A corner is where two sides meet. It is a pointy place (or a square corner).",
            "Triangles: 3 and 3. Squares: 4 and 4. Rectangles: 4 and 4. Circles: 0 and 0.",
            "If you know the sides, you often know the corners for these shapes.",
            "Do not count a curved circle as having sides. Sides here mean straight sides.",
            "Trace with a finger. Pause at each corner.",
        ],
        lesson_figure(
            '''<svg viewBox="0 0 280 140" width="100%" style="max-width:280px" role="img">
  <rect x="40" y="28" width="200" height="80" fill="#bfdbfe" stroke="#1e3a8a" stroke-width="3"/>
  <circle cx="40" cy="28" r="6" fill="#dc2626"/>
  <circle cx="240" cy="28" r="6" fill="#dc2626"/>
  <circle cx="40" cy="108" r="6" fill="#dc2626"/>
  <circle cx="240" cy="108" r="6" fill="#dc2626"/>
  <text x="140" y="20" text-anchor="middle" font-size="12">4 sides</text>
  <text x="140" y="132" text-anchor="middle" font-size="12">4 red corners</text>
</svg>''',
            "A rectangle's corners",
            "Each red dot is where two sides meet. Count the dots: 4 corners.",
        )
        + solved(1, "How many corners on a rectangle?",
               ["A rectangle has 4 sides.",
                "Each pair of sides meets at a corner.",
                "4 corners."],
               "4")
        + step_reveal(
            ["Point to a starting corner.",
             "Move along a side.",
             "Each time you turn, count a corner.",
             "Stop when you return to the start.",
             "That count is the number of corners."],
            vid="g1u8-c2-steps",
        ),
        try_this("Corners = turns", "Every time the pencil turns, you found a corner."),
        6,
    )

    c3 = concept_block(
        "3. Closed shapes",
        [
            "A closed shape has no gaps. The line comes back to the start.",
            "You can color inside a closed shape.",
            "An open shape has a gap, like the letter C.",
            "Squares, triangles, rectangles, and circles are closed.",
            "If there is a hole in the outline, it is not closed.",
            "Building shapes with sticks: every stick end must meet another stick end.",
        ],
        lesson_figure(
            '''<svg viewBox="0 0 320 130" width="100%" style="max-width:320px" role="img">
  <rect x="24" y="24" width="80" height="80" fill="#bbf7d0" stroke="#166534" stroke-width="3"/>
  <text x="64" y="120" text-anchor="middle" font-size="12">closed square</text>
  <path d="M200,40 A40,40 0 1,1 200,104" fill="none" stroke="#b91c1c" stroke-width="6" stroke-linecap="round"/>
  <text x="232" y="120" text-anchor="middle" font-size="12">open like C</text>
</svg>''',
            "Closed vs open",
            "The square comes back to the start — no gap. The C has a gap, so it is open. A square is closed.",
        )
        + solved(1, "Is a square closed?",
               ["Follow the four sides.",
                "You return to the start.",
                "No gap. Closed."],
               "yes, closed")
        + matching(
            [("O", "closed"), ("C", "open"), ("square", "closed"), ("U", "open")],
            vid="g1u8-c3-match",
        ),
        watch_out("Almost closed",
                  "If two ends almost touch but do not, the shape is still open. Close the gap."),
        11,
    )

    c4 = concept_block(
        "4. 3D shapes: cube, sphere, cone, cylinder",
        [
            "Solid shapes are 3D. You can hold them. They are not just drawings.",
            "A cube is like a dice. Six square faces. Stacks well.",
            "A sphere is like a ball. Curved all around. Rolls every way.",
            "A cone is like an ice cream cone or a party hat. One circle face and a point.",
            "A cylinder is like a can. Two circle faces. Rolls sideways.",
            "Sort toys: balls, blocks, cans, hats.",
        ],
        lesson_figure(
            '''<svg viewBox="0 0 440 140" width="100%" style="max-width:440px" role="img">
  <rect x="24" y="36" width="56" height="56" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>
  <polygon points="80,36 96,24 96,80 80,92" fill="#bfdbfe" stroke="#1e3a8a"/>
  <polygon points="24,36 40,24 96,24 80,36" fill="#dbeafe" stroke="#1e3a8a"/>
  <text x="52" y="124" text-anchor="middle" font-size="12">cube</text>
  <circle cx="160" cy="64" r="32" fill="#fecaca" stroke="#991b1b" stroke-width="2"/>
  <text x="160" y="124" text-anchor="middle" font-size="12">sphere</text>
  <polygon points="250,24 286,96 214,96" fill="#fde68a" stroke="#92400e" stroke-width="2"/>
  <ellipse cx="250" cy="96" rx="36" ry="8" fill="#fef3c7" stroke="#92400e"/>
  <text x="250" y="124" text-anchor="middle" font-size="12">cone</text>
  <ellipse cx="370" cy="36" rx="28" ry="10" fill="#bbf7d0" stroke="#166534"/>
  <rect x="342" y="36" width="56" height="56" fill="#86efac" stroke="#166534"/>
  <ellipse cx="370" cy="92" rx="28" ry="10" fill="#bbf7d0" stroke="#166534"/>
  <text x="370" y="124" text-anchor="middle" font-size="12">cylinder</text>
</svg>''',
            "Four solids you can hold",
            "A tennis ball matches the sphere: round all around, no flat faces, rolls every way.",
        )
        + solved(1, "What solid is a tennis ball?",
               ["It is round all around.",
                "It rolls in any direction.",
                "It is a sphere."],
               "sphere")
        + matching(
            [("dice", "cube"), ("ball", "sphere"), ("party hat", "cone"), ("soup can", "cylinder")],
            vid="g1u8-c4-match",
        ),
        kid_tip("Roll or stack?", "Spheres roll. Cubes stack. Cylinders roll sideways and can stand on a circle."),
        16,
    )

    c5 = concept_block(
        "5. Faces of solid shapes",
        [
            "A face is a flat side of a solid.",
            "A cube has 6 faces. All squares.",
            "A cylinder has 2 flat circle faces. The side is curved.",
            "A cone has 1 flat circle face. The rest comes to a point.",
            "A sphere has 0 flat faces.",
            "You can feel faces with your hand. Flat vs curved.",
        ],
        lesson_figure(
            '''<svg viewBox="0 0 280 200" width="100%" style="max-width:240px" role="img">
  <rect x="100" y="16" width="52" height="52" fill="#c7d2fe" stroke="#312e81" stroke-width="2"/>
  <rect x="48" y="68" width="52" height="52" fill="#c7d2fe" stroke="#312e81" stroke-width="2"/>
  <rect x="100" y="68" width="52" height="52" fill="#a5b4fc" stroke="#312e81" stroke-width="2"/>
  <rect x="152" y="68" width="52" height="52" fill="#c7d2fe" stroke="#312e81" stroke-width="2"/>
  <rect x="204" y="68" width="52" height="52" fill="#c7d2fe" stroke="#312e81" stroke-width="2"/>
  <rect x="100" y="120" width="52" height="52" fill="#c7d2fe" stroke="#312e81" stroke-width="2"/>
  <text x="140" y="190" text-anchor="middle" font-size="12">cube net — 6 square faces</text>
</svg>''',
            "Six faces of a cube",
            "Unfold a dice. Top, bottom, and four around: 6 square faces.",
        )
        + solved(1, "How many flat faces on a cube?",
               ["Think of a die.",
                "Top, bottom, and four around.",
                "6 faces."],
               "6")
        + step_reveal(
            ["Pick up a block (cube).",
             "Color or touch the top. That is 1.",
             "Touch the bottom. That is 2.",
             "Touch the four sides. 3, 4, 5, 6.",
             "Six square faces."],
            vid="g1u8-c5-steps",
        ),
        try_this("Trace a face", "Put a cube on paper. Trace around it. You drew a square."),
        21,
    )

    c6 = concept_block(
        "6. Halves and fourths",
        [
            "We can split a shape into equal parts.",
            "Two equal parts are halves. Each part is one half of the whole.",
            "Four equal parts are fourths (quarters). Each part is one fourth.",
            "Equal means the same size. If one piece is bigger, they are not halves.",
            "A sandwich cut down the middle can be two halves.",
            "A square window with a plus-sign cut can show four fourths.",
        ],
        lesson_figure(
            svg_fraction_bar(1, 2, color="#86efac")
            + svg_fraction_bar(1, 4, color="#a78bfa"),
            "Halves and fourths",
            "Top bar: 2 equal parts — each is one half. Bottom bar: 4 equal parts — each is one fourth. Equal size matters.",
        )
        + solved(1, "A square is cut into 2 equal triangles. What is each piece?",
               ["Two pieces.",
                "They match in size.",
                "Each is one half of the square."],
               "one half")
        + matching(
            [("2 equal parts", "halves"), ("4 equal parts", "fourths"),
             ("the whole", "all the parts together"), ("unequal parts", "not halves")],
            vid="g1u8-c6-match",
        )
        + phet_box("area"),
        watch_out("Two pieces that are not equal",
                  "Two pieces are not automatically halves. They must be the same size."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Name circle, square, triangle, rectangle",
            "Count sides and corners",
            "Tell closed from open",
            "Name cube, sphere, cone, cylinder",
            "Count faces",
            "Find halves and fourths",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u8_questions()


def build_master():
    return f"""
<h1>First Grade Math</h1>
<p>This is a full first-grade math path. We use <strong>short words</strong>, pictures, and lots of practice.</p>
<p>You will count, add, subtract, tell time, measure, and name shapes. After each idea there are 5 quick questions. At the end of a unit there are 50 more. Hearts help you. Take your time.</p>
{page_break()}
<h2>The eight units</h2>
<ol>
<li>Unit 1 — Counting to 120</li>
<li>Unit 2 — Tens and Ones</li>
<li>Unit 3 — Addition to 20</li>
<li>Unit 4 — Subtraction to 20</li>
<li>Unit 5 — Number Stories</li>
<li>Unit 6 — Telling Time</li>
<li>Unit 7 — Measuring Length</li>
<li>Unit 8 — Shapes</li>
</ol>
<p>Start with counting. Tens and ones help you add and subtract. Stories use plus and minus. Time, measuring, and shapes are the last three adventures.</p>
{page_break()}
<h2>How to learn</h2>
<p>Touch and count. Say numbers out loud. Use fingers. Draw dots. Play the number games when you see them.</p>
<p>If a question feels hard, try a smaller number first. Then come back. You are building number sense — a feeling for how numbers work.</p>
"""
