"""Sixth Grade Math units 1–4: ratios, rates and percents, divide fractions, integers."""

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
    tape_diagram,
    double_number_line,
    percent_bar,
    integer_line,
    fraction_divide_bars,
    mq,
    renumber,
)


def _fill(qs, need, factory):
    while len(qs) < need:
        qs.append(factory(len(qs) + 1))
    return renumber(qs[:need])


# ===========================================================================
# UNIT 1: Ratios
# ===========================================================================

def _u1_questions():
    qs = []
    idx = 1
    items = [
        ("A ratio 2:3 means…", "2 of the first for every 3 of the second", ["2 + 3", "2 × 3", "3 − 2"], "Order matters. First number matches the first quantity."),
        ("Juice mix 2 cups concentrate to 3 cups water. The ratio concentrate:water is…", "2:3", ["3:2", "2:5", "5:3"], "Concentrate first, then water."),
        ("The ratio 2:3 as a fraction of concentrate to water is…", "2/3", ["3/2", "2/5", "5/2"], "First:second as a fraction."),
        ("If there are 4 red and 6 blue, red:blue in simplest form is…", "2:3", ["4:6", "6:4", "4:10"], "Divide both by 2."),
        ("Part-to-whole for 2 concentrate and 3 water is concentrate:total…", "2:5", ["2:3", "3:5", "5:2"], "Total parts = 5."),
        ("2:3 is equivalent to…", "4:6", ["3:2", "2:6", "5:6"], "×2 on both parts."),
        ("5:10 is equivalent to…", "1:2", ["2:1", "5:2", "10:5"], "÷5 on both."),
        ("If 3:5 = 6:x then x = ?", "10", ["8", "9", "15"], "×2: 5×2=10."),
        ("If 2:7 = 8:x then x = ?", "28", ["14", "16", "21"], "×4: 7×4=28."),
        ("A table: 1,2,3 and 4,8,12. The ratio is…", "1:4", ["4:1", "1:3", "3:4"], "Each y is 4 times x."),
        ("3 cats to 5 dogs. For 9 cats, dogs = ?", "15", ["11", "12", "8"], "×3: 5×3=15."),
        ("Ratio of 12 to 18 in simplest form?", "2:3", ["12:18", "6:9", "3:2"], "÷6."),
        ("Which is NOT equivalent to 3:4?", "6:12", ["6:8", "9:12", "12:16"], "6:12 = 1:2, not 3:4."),
        ("A recipe 1:2 flour:sugar. For 3 cups flour, sugar = ?", "6 cups", ["5 cups", "4 cups", "3 cups"], "×3."),
        ("In 2:5, the first quantity is what fraction of the total?", "2/7", ["2/5", "5/7", "5/2"], "Total 7 parts."),
        ("Tape 2 green : 3 yellow. Green is what part of the tape?", "2/5", ["2/3", "3/5", "5/2"], "2 of 5 equal boxes."),
        ("If a:b = 4:1 and b = 5, then a = ?", "20", ["9", "4", "1"], "a is 4 times b."),
        ("The ratio 8:2 simplified is…", "4:1", ["8:2", "2:8", "6:0"], "÷2."),
        ("3:5 vs 5:3. They are…", "different ratios (order matters)", ["the same", "always equal", "not ratios"], "3:5 is not 5:3."),
        ("Double number line: 2 miles in 10 min, 4 miles in…", "20 min", ["12 min", "14 min", "8 min"], "Both scale by 2."),
        ("6:9 = 2:?", "3", ["6", "4", "9"], "÷3."),
        ("A class 10 girls and 15 boys. girls:boys = ?", "2:3", ["10:15", "3:2", "10:25"], "÷5."),
        ("Part-to-part 1:4. If there are 20 in all, the smaller part is…", "4", ["5", "16", "1"], "1+4=5 parts. 20/5=4 per part. 1 part = 4."),
        ("Scale factor from 2:5 to 10:25 is…", "5", ["2", "10", "20"], "2×5=10 and 5×5=25."),
        ("4/6 as a ratio in simplest form is…", "2:3", ["4:6", "4:2", "6:4"], "A fraction a/b is the ratio a:b."),
        ("If 5 packs cost the same ratio as 1 pack to $3, 5 packs cost…", "$15", ["$8", "$5", "$3"], "×5."),
        ("Ratio of 1 hour to 15 minutes as minutes is…", "60:15 → 4:1", ["1:15", "15:1", "1:4"], "Same units first."),
        ("Which pair is equivalent: 3:9 and…", "1:3", ["3:6", "9:3", "2:9"], "÷3."),
        ("A map 1 cm : 5 km. 4 cm on the map is…", "20 km", ["9 km", "5 km", "4 km"], "×4."),
        ("2:2 simplified is…", "1:1", ["2:2", "0:0", "4:4"], "Equal parts."),
    ]
    for text, ans, dist, expl in items:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1
    return _fill(qs, 55, lambda i: mq(
        f"If 2:5 = {2 * (i % 6 + 2)}:x, what is x?",
        5 * (i % 6 + 2),
        "Multiply both parts by the same number.",
        i,
    ))


def build_unit1():
    title = "Sixth Grade Math Unit 1: Ratios"
    description = (
        "Write ratios, find equivalent ratios, and use tape diagrams, tables, and double number lines."
    )
    c1 = concept_block(
        "1. What a ratio is",
        [
            "A ratio compares two quantities. 2:3 means 2 of the first for every 3 of the second.",
            "You can write a ratio as 2:3, 2 to 3, or 2/3 when you mean first compared with second.",
            "Order matters. Juice concentrate to water 2:3 is not the same as water to concentrate 3:2.",
            "Use the same kind of units when you can: minutes to minutes, cups to cups.",
            "A ratio is not a sum. 2:3 is not 5, though the total of the parts is 5.",
            "Part-to-part compares two groups. Part-to-whole compares one group with the total.",
        ],
        tape_diagram(
            [
                ("concentrate", [("#f97316", 2, "c")]),
                ("water", [("#38bdf8", 3, "w")]),
            ],
            title="Juice mix 2 : 3",
            caption="Two orange boxes for every three blue boxes. Concentrate:water = 2:3. Total parts = 5.",
        )
        + solved(1, "A mix uses 2 cups concentrate and 3 cups water. What is the ratio concentrate:water?",
                 ["Put concentrate first.",
                  "2 cups to 3 cups.",
                  "2:3."],
                 "2:3")
        + matching(
            [("2:3", "2 of first for 3 of second"), ("3:2", "the reverse order"),
             ("2:5", "part-to-whole for concentrate"), ("5:2", "whole-to-part")],
            vid="g6u1-c1-match",
        ),
        kid_tip("Name both parts", "Say the ratio in words: '2 concentrate to 3 water.' Then the symbols 2:3 make sense."),
        1,
    )
    c2 = concept_block(
        "2. Equivalent ratios",
        [
            "Equivalent ratios name the same comparison. 2:3 = 4:6 = 6:9.",
            "Multiply or divide both parts by the same nonzero number.",
            "Simplest form means the two numbers share no common factor other than 1. 4:6 becomes 2:3.",
            "If 3:5 = 6:x, then x = 10 because both parts were multiplied by 2.",
            "A ratio table lists equivalent pairs in columns. Each column is a scale-up or scale-down.",
            "If someone writes 6:12 for 3:4, that is not equivalent — check by simplifying.",
        ],
        tape_diagram(
            [
                ("first", [("#f87171", 2, "")]),
                ("second", [("#60a5fa", 7, "")]),
            ],
            title="2 : 7",
            caption="Two of the first for seven of the second. Scale by 4: 8 of the first for 28 of the second. 2:7 = 8:28.",
        )
        + double_number_line(
            "red", [2, 4, 6, 8],
            "blue", [3, 6, 9, 12],
            title="Equivalent ratios 2 : 3",
            caption="Each jump multiplies both colors by the same factor. 2:3 = 4:6 = 6:9 = 8:12.",
        )
        + solved(1, "Find x so that 2:7 = 8:x.",
                 ["8 is 2 × 4, so the scale factor is 4.",
                  "7 × 4 = 28.",
                  "x = 28."],
                 "28")
        + step_reveal(
            ["Write the two ratios.",
             "Find the factor that takes the first known part to the new first part.",
             "Multiply the other part by that same factor.",
             "Check by simplifying both ratios."],
            vid="g6u1-c2-steps",
        ),
        watch_out("Adding the same number to both parts",
                  "2:3 is not equivalent to 3:4. Adding 1 to each part changes the comparison. Multiply or divide, do not add."),
        6,
    )
    c3 = concept_block(
        "3. Tape diagrams",
        [
            "A tape diagram is a bar split into equal boxes. Each box is one part of the ratio.",
            "For 2:3, draw 2 boxes of one color and 3 of another. All boxes are the same size.",
            "If the total is 20 and the ratio is 1:4, there are 5 boxes. Each box is 4. The parts are 4 and 16.",
            "Tapes make part-to-whole easy: shaded boxes over all boxes.",
            "When a story gives one part, fill that many boxes, then fill the rest.",
            "Keep boxes equal. Unequal boxes would lie about the ratio.",
        ],
        tape_diagram(
            [
                ("girls", [("#f472b6", 2, "")]),
                ("boys", [("#60a5fa", 3, "")]),
            ],
            title="Class ratio girls : boys = 2 : 3",
            caption="5 equal boxes in all. If each box is 5 students, girls = 10 and boys = 15.",
        )
        + solved(1, "A class has girls:boys = 2:3 and 25 students. How many girls?",
                 ["2 + 3 = 5 parts.",
                  "25 ÷ 5 = 5 students per part.",
                  "Girls: 2 × 5 = 10."],
                 "10 girls"),
        try_this("Draw the boxes first", "Do not jump to the answer. Count parts, find the value of one box, then multiply."),
        11,
    )
    c4 = concept_block(
        "4. Ratio tables",
        [
            "A table with two rows (or two columns) can grow a ratio.",
            "Start with 1:4. Next columns: 2:8, 3:12, 4:16. You multiplied by 1, 2, 3, 4.",
            "You can also skip: ×10 gives 10:40 in one jump.",
            "Tables are handy for recipes, maps, and unit conversions once you have the ratio.",
            "Look down a column: those two numbers should simplify to the original ratio.",
            "If a column does not simplify to the same ratio, a multiply went wrong.",
        ],
        tape_diagram(
            [
                ("map cm", [("#fbbf24", 1, "1")]),
                ("real km", [("#34d399", 5, "5")]),
            ],
            title="Map key 1 cm : 5 km",
            caption="One yellow box pairs with five green boxes. Scale by 4: 4 cm on the map is 20 km in real life.",
        )
        + solved(1, "A map key is 1 cm : 5 km. Complete 4 cm on the map.",
               ["The ratio is 1:5.",
                "Scale by 4.",
                "4 cm represents 20 km."],
               "20 km")
        + matching(
            [("1:5", "4:20"), ("2:3", "10:15"), ("5:1", "20:4"), ("3:9", "1:3")],
            vid="g6u1-c4-match",
        ),
        kid_tip("Same factor", "Whatever you multiply the top by, multiply the bottom by. The ratio stays in lockstep."),
        16,
    )
    c5 = concept_block(
        "5. Double number lines",
        [
            "A double number line is two number lines stacked, with matching marks.",
            "If 2 miles take 10 minutes, then 4 miles take 20 minutes — both doubled.",
            "The marks line up because the ratio is constant.",
            "This picture is the cousin of a ratio table. Same numbers, stretched out.",
            "You can find in-between values if you split a jump into equal pieces.",
            "Label each line: miles on top, minutes on the bottom (or the other way). Keep the pairing.",
        ],
        double_number_line(
            "miles", [0, 2, 4, 6],
            "min", [0, 10, 20, 30],
            title="Constant speed 2 miles every 10 minutes",
            caption="Every 2 miles adds 10 minutes. The ratio miles:minutes stays 1:5.",
        )
        + solved(1, "A runner goes 2 miles in 10 minutes at a steady pace. How long for 6 miles?",
                 ["2 miles → 10 min.",
                  "6 miles is 3 times as far.",
                  "3 × 10 = 30 minutes."],
                 "30 minutes"),
        try_this("Start at zero", "Include 0:0 on both lines. It reminds you the lines are scaled together."),
        21,
    )
    c6 = concept_block(
        "6. Ratio stories",
        [
            "Recipes, maps, class votes, and mixes are ratio stories.",
            "Read which quantity is first. A:B is not B:A.",
            "Sometimes you must convert units first: 1 hour : 15 minutes → 60:15 → 4:1.",
            "If you know a total, use parts. If you know one quantity, scale from that.",
            "Write the ratio, pick a tool (tape, table, or double number line), then compute.",
            "End with a sentence that answers the question, with units.",
        ],
        tape_diagram(
            [
                ("blue", [("#3b82f6", 1, "")]),
                ("white", [("#e2e8f0", 4, "")]),
            ],
            title="Paint mix 1 : 4",
            caption="5 equal parts in all. 20 liters ÷ 5 = 4 liters per part. Blue is 1 part: 4 liters.",
        )
        + solved(1, "Paint mix is 1 part blue to 4 parts white. You want 20 liters in all. How much blue?",
               ["1 + 4 = 5 parts.",
                "20 ÷ 5 = 4 liters per part.",
                "Blue is 1 part: 4 liters."],
               "4 liters blue")
        + step_reveal(
            ["Underline the two quantities.",
             "Write the ratio in the asked order.",
             "Choose tape, table, or double number line.",
             "Scale or split into parts.",
             "Label the answer."],
            vid="g6u1-c6-steps",
        ),
        watch_out("Mixing units", "Do not write 1 hour : 15 minutes as 1:15 and stop. Convert so both are minutes or both are hours."),
        26,
    )
    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Write a ratio in order",
            "Find equivalent ratios",
            "Use tape diagrams",
            "Build ratio tables",
            "Read double number lines",
            "Solve ratio stories",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u1_questions()


# ===========================================================================
# UNIT 2: Unit rates and percents
# ===========================================================================

def _u2_questions():
    qs = []
    idx = 1
    items = [
        ("A unit rate is a rate with a denominator of…", "1", ["2", "100", "0"], "Per one: miles per 1 hour, price per 1 item."),
        ("180 miles in 3 hours. Miles per hour?", "60", ["540", "183", "30"], "180 ÷ 3 = 60."),
        ("$12 for 4 bottles. Price per bottle?", "$3", ["$16", "$8", "$48"], "12 ÷ 4 = 3."),
        ("2 pounds for $5. Cost per pound?", "$2.50", ["$10", "$3", "$2"], "5 ÷ 2 = 2.5."),
        ("Which is a better buy: 3 for $6 or 5 for $9?", "5 for $9", ["3 for $6", "same", "cannot tell"], "$2 each vs $1.80 each."),
        ("Percent means per…", "hundred", ["ten", "thousand", "one"], "25% = 25 per 100."),
        ("25% as a fraction is…", "1/4", ["25/10", "1/25", "4/1"], "25/100 = 1/4."),
        ("50% of 80 is…", "40", ["50", "30", "160"], "Half of 80."),
        ("10% of 90 is…", "9", ["10", "80", "900"], "Move the point one place left."),
        ("1% of 200 is…", "2", ["1", "20", "199"], "1/100 of 200."),
        ("What percent is 15 of 60?", "25%", ["15%", "60%", "45%"], "15/60 = 1/4 = 25%."),
        ("30 is 50% of what number?", "60", ["15", "80", "100"], "30 is half of 60."),
        ("A 20% tip on $40 is…", "$8", ["$20", "$4", "$12"], "0.20 × 40 = 8."),
        ("0.4 as a percent is…", "40%", ["4%", "0.4%", "400%"], "×100."),
        ("3/5 as a percent is…", "60%", ["35%", "3%", "5%"], "3÷5=0.6=60%."),
        ("120% of 50 is…", "60", ["12", "70", "100"], "1.2 × 50 = 60."),
        ("A rate 3/4 mile in 1/4 hour. Miles per hour?", "3", ["1", "12", "1/16"], "Divide: (3/4)÷(1/4)=3."),
        ("Unit rate of 9 pages in 3 minutes?", "3 pages per minute", ["9 per 3", "12 pages", "1/3 page"], "9÷3=3."),
        ("Which is greater: 2/5 or 40%?", "equal", ["2/5", "40%", "cannot compare"], "2/5=0.4=40%."),
        ("5% of 80 is…", "4", ["5", "16", "75"], "0.05×80=4."),
        ("75% of 40 is…", "30", ["75", "15", "35"], "3/4 of 40."),
        ("A shirt $20, 10% off. Sale price?", "$18", ["$10", "$2", "$19"], "Take off $2."),
        ("The whole is 100%. 1/2 is…", "50%", ["100%", "2%", "200%"], "Half of 100%."),
        ("If 8 apples cost $4, 1 apple costs…", "$0.50", ["$2", "$4", "$8"], "4÷8=0.5."),
        ("Speed 150 km in 2.5 h. km per hour?", "60", ["375", "152.5", "50"], "150÷2.5=60."),
        ("What percent is 7 of 10?", "70%", ["7%", "10%", "17%"], "7/10=0.7."),
        ("200% of 9 is…", "18", ["11", "209", "2"], "Double."),
        ("Find 15% of 80. 10% is 8, 5% is 4, so…", "12", ["15", "20", "8"], "8+4=12."),
        ("A ratio 3:100 as a percent is…", "3%", ["30%", "100%", "3:100%"], "Per hundred is percent."),
        ("If 1 item is $2.50, 6 items cost…", "$15", ["$8.50", "$12", "$2.50"], "Unit rate × 6."),
    ]
    for text, ans, dist, expl in items:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1
    return _fill(qs, 55, lambda i: mq(
        f"What is 10% of {10 * (i % 9 + 2)}?",
        i % 9 + 2,
        "10% is one tenth.",
        i,
    ))


def build_unit2():
    title = "Sixth Grade Math Unit 2: Unit Rates and Percents"
    description = (
        "Find unit rates, compare deals, and connect fractions, decimals, and percents."
    )
    c1 = concept_block(
        "1. Unit rate — per one",
        [
            "A rate compares two different units: miles per hour, dollars per bottle, pages per minute.",
            "A unit rate has a 1 on the bottom: 60 miles per 1 hour.",
            "To get a unit rate, divide. 180 miles in 3 hours → 180 ÷ 3 = 60 miles per hour.",
            "Price per one item is how you compare two deals of different sizes.",
            "Keep the units in the answer: not just 60, but 60 miles per hour.",
            "If the story is 'for every,' you are in rate territory.",
        ],
        double_number_line(
            "$", [0, 3, 6, 9, 12],
            "btl", [0, 1, 2, 3, 4],
            title="Unit rate $3 per bottle",
            caption="Each bottle adds $3. The unit rate is $3 per 1 bottle. 4 bottles cost $12.",
        )
        + solved(1, "A pack of 4 bottles costs $12. What is the price per bottle?",
                 ["Divide cost by number of bottles.",
                  "12 ÷ 4 = 3.",
                  "$3 per bottle."],
                 "$3 per bottle")
        + phet_box("unit_rates"),
        kid_tip("Divide to get to 1", "Whatever the 'how many' is, divide so that quantity becomes 1."),
        1,
    )
    c2 = concept_block(
        "2. Compare with unit rates",
        [
            "To compare two deals, find the unit price of each. The smaller unit price is the better buy (if quality is the same).",
            "3 for $6 is $2 each. 5 for $9 is $1.80 each. Five for $9 is the better buy.",
            "Speeds work the same: more miles per hour is faster.",
            "Be careful when packages have different sizes. Always go to per one (or per the same amount).",
            "Sometimes per 10 or per 100 is easier mental math — still a fair comparison if both use the same 'per.'",
            "Estimate first: if one deal is obviously about $2 and the other about $1.50, you already know the winner.",
        ],
        double_number_line(
            "$", [0, 2, 4, 6],
            "snacks", [0, 1, 2, 3],
            title="Deal A: 3 snacks for $6",
            caption="Each snack adds $2. Unit price is $2 per snack.",
        )
        + double_number_line(
            "$", [0, 9],
            "snacks", [0, 5],
            title="Deal B: 5 snacks for $9",
            caption="9 ÷ 5 = $1.80 per snack. $1.80 < $2, so 5 for $9 is the better buy.",
        )
        + solved(1, "Which is the better buy: 3 snacks for $6 or 5 snacks for $9?",
               ["3 for $6 → $2 each.",
                "5 for $9 → $1.80 each.",
                "$1.80 < $2, so 5 for $9."],
               "5 for $9")
        + matching(
            [("180 mi / 3 h", "60 mph"), ("$12 / 4", "$3 each"),
             ("9 pages / 3 min", "3 pages per min"), ("$5 / 2 lb", "$2.50 per lb")],
            vid="g6u2-c2-match",
        ),
        watch_out("Comparing totals instead of per one",
                  "$9 is more than $6, but you also get more snacks. Compare unit prices, not the sticker totals."),
        6,
    )
    c3 = concept_block(
        "3. Percent is per hundred",
        [
            "Percent means per 100. 25% is 25 out of every 100, which is 1/4.",
            "100% is the whole. 50% is half. 200% is two wholes.",
            "A percent bar is a tape that runs from 0% to 100%. Mark the percent you need.",
            "10% of a number is the number ÷ 10. 1% is the number ÷ 100.",
            "You can build other percents from 10% and 1%: 15% = 10% + 5%, and 5% is half of 10%.",
            "Fractions, decimals, and percents are three names for the same idea: 1/4 = 0.25 = 25%.",
        ],
        percent_bar(25, 80, title="25% of 80", caption="A quarter of the bar is shaded. 25% of 80 is 20.")
        + solved(1, "Find 25% of 80.",
                 ["25% = 1/4.",
                  "80 ÷ 4 = 20.",
                  "Or 0.25 × 80 = 20."],
                 "20")
        + matching(
            [("25%", "1/4"), ("50%", "1/2"), ("75%", "3/4"), ("10%", "1/10")],
            vid="g6u2-c3-match",
        ),
        try_this("Benchmark percents", "Memorize 1%, 10%, 25%, 50%, 75%, 100%. Most problems are combinations of these."),
        11,
    )
    c4 = concept_block(
        "4. Find the percent, the part, or the whole",
        [
            "Three related questions: What is 25% of 60? 15 is what percent of 60? 15 is 25% of what?",
            "Part = percent × whole. Percent = part ÷ whole. Whole = part ÷ percent.",
            "15 is what percent of 60? 15/60 = 0.25 = 25%.",
            "30 is 50% of what? 30 ÷ 0.5 = 60.",
            "A double number line with 0–100% on one line and 0–whole on the other keeps the three pieces honest.",
            "Always ask: did I find a part, a percent, or a whole?",
        ],
        percent_bar(25, 60, title="25% of 60", caption="15 is 25% of 60. Part ÷ whole = 15/60 = 0.25 = 25%.")
        + solved(1, "15 is what percent of 60?",
                 ["Part over whole: 15/60.",
                  "Simplify: 1/4.",
                  "1/4 = 25%."],
                 "25%")
        + step_reveal(
            ["Identify part, whole, and percent. Which is missing?",
             "Write part = percent × whole (percent as a decimal or fraction).",
             "Solve for the missing piece.",
             "Check with a benchmark (half, quarter, tenth)."],
            vid="g6u2-c4-steps",
        ),
        16,
    )
    c5 = concept_block(
        "5. Percent stories: tips, tax, discounts",
        [
            "A 20% tip on $40 is 0.20 × 40 = $8. You pay $48 in all if you add the tip.",
            "10% off a $20 shirt takes off $2. Sale price $18.",
            "Tax is added. Discount is subtracted. Read the story.",
            "120% of 50 is more than 50: 1.20 × 50 = 60.",
            "For mental math: 15% = 10% + 5%. 10% of 80 is 8, 5% is 4, total 12.",
            "Estimate: 19% of 50 is near 20% of 50 = 10.",
        ],
        percent_bar(20, 40, title="20% tip on $40", caption="20% of 40 is 8. The tip is $8. You pay $48 if you add the tip to the meal.")
        + solved(1, "A meal is $40. You leave a 20% tip. How much is the tip?",
               ["20% = 0.20.",
                "0.20 × 40 = 8.",
                "The tip is $8."],
               "$8")
        + matching(
            [("20% of $40", "$8"), ("10% off $20", "$2 off"),
             ("50% of 90", "45"), ("1% of 200", "2")],
            vid="g6u2-c5-match",
        ),
        watch_out("Taking a percent off and thinking the percent is the new price",
                  "10% off $20 is not $10. 10% of 20 is $2 off, so the sale price is $18."),
        21,
    )
    c6 = concept_block(
        "6. Rates that are fractions",
        [
            "Unit rates still work when the numbers are fractions.",
            "3/4 mile in 1/4 hour: divide (3/4) ÷ (1/4) = 3 miles per hour.",
            "Dividing fractions is the same skill you will polish in Unit 3: multiply by the reciprocal.",
            "A double number line can use fractional marks: 0, 1/4, 1/2, 3/4, 1.",
            "Keep asking 'per one hour' or 'per one mile' so the answer is a unit rate.",
            "Check by multiplying back: 3 miles per hour × 1/4 hour = 3/4 mile.",
        ],
        double_number_line(
            "mi", ["0", "1/4", "1/2", "3/4"],
            "h", ["0", "1/12", "1/6", "1/4"],
            title="Steady pace, fractional distances",
            caption="At 3 miles per hour, in 1/4 hour you cover 3/4 mile.",
        )
        + solved(1, "You walk 3/4 mile in 1/4 hour. What is your speed in miles per hour?",
                 ["Speed = distance ÷ time.",
                  "(3/4) ÷ (1/4) = (3/4) × 4 = 3.",
                  "3 miles per hour."],
                 "3 mph")
        + phet_box("arith"),
        26,
    )
    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Find a unit rate",
            "Compare deals with unit prices",
            "See percent as per 100",
            "Find part, percent, or whole",
            "Solve tip, tax, and discount stories",
            "Compute rates with fractions",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u2_questions()


# ===========================================================================
# UNIT 3: Divide fractions and rational numbers
# ===========================================================================

def _u3_questions():
    qs = []
    idx = 1
    items = [
        ("3 ÷ 1/2 = ?", "6", ["1.5", "3/2", "1/6"], "How many halves in 3? Six."),
        ("1/2 ÷ 4 = ?", "1/8", ["2", "4/2", "1/4"], "Split a half into 4."),
        ("2/3 ÷ 1/6 = ?", "4", ["2/18", "1/4", "3"], "How many 1/6s in 2/3? Four."),
        ("5/8 ÷ 1/8 = ?", "5", ["5/64", "6/8", "1"], "Same-size pieces: 5 of them."),
        ("To divide by a fraction, multiply by its…", "reciprocal", ["numerator", "percent", "opposite"], "Keep, change, flip."),
        ("The reciprocal of 2/5 is…", "5/2", ["2/5", "−2/5", "5"], "Flip top and bottom."),
        ("The reciprocal of 4 is…", "1/4", ["4", "−4", "4/1 only"], "4 = 4/1, flip to 1/4."),
        ("3/4 × 2/5 = ?", "6/20", ["5/9", "6/9", "5/20"], "6/20 = 3/10 after simplify."),
        ("1.5 + 2.25 = ?", "3.75", ["3.30", "4.75", "1.75"], "Line up points."),
        ("4.2 − 1.15 = ?", "3.05", ["3.15", "5.35", "3.00"], "4.20 − 1.15."),
        ("0.6 × 0.4 = ?", "0.24", ["1.0", "0.024", "2.4"], "Two decimal places."),
        ("7.2 ÷ 0.8 = ?", "9", ["0.9", "6.4", "8"], "72 ÷ 8 = 9."),
        ("1/2 + 1/3 = ?", "5/6", ["2/5", "1/5", "2/6"], "3/6+2/6."),
        ("5/6 − 1/2 = ?", "1/3", ["4/4", "4/6", "1/6"], "5/6−3/6=2/6=1/3."),
        ("How many 1/4 cups in 2 cups?", "8", ["2/4", "4", "1/8"], "2 ÷ 1/4 = 8."),
        ("A 3/4-pound bag split into 1/8-pound servings makes…", "6 servings", ["3/32", "2", "8"], "(3/4)÷(1/8)=6."),
        ("2 1/2 ÷ 1/2 = ?", "5", ["2", "1", "3"], "Five halves in two and a half."),
        ("0.25 as a fraction is…", "1/4", ["25/10", "1/25", "4"], "25/100=1/4."),
        ("3/5 as a decimal is…", "0.6", ["0.35", "3.5", "0.06"], "3÷5=0.6."),
        ("Which is least: 0.4, 2/5, 3/10?", "3/10", ["0.4", "2/5", "all equal"], "0.4=2/5=0.40; 3/10=0.30."),
        ("Which is greatest: 0.7, 3/4, 70%?", "3/4", ["0.7", "70%", "all equal"], "3/4=0.75."),
        ("1 ÷ 2/3 = ?", "3/2", ["2/3", "1/3", "5/3"], "× 3/2."),
        ("(2/3) ÷ (4/9) = ?", "3/2", ["8/27", "6/12", "2/3"], "2/3 × 9/4 = 18/12 = 3/2."),
        ("A recipe 2/3 cup, you make 1/2 recipe. Amount?", "1/3 cup", ["1/6 cup", "7/6 cup", "1 cup"], "(1/2)×(2/3)=1/3."),
        ("Multi-digit: 24.6 ÷ 3 = ?", "8.2", ["82", "7.6", "21.6"], "24÷3=8, 0.6÷3=0.2."),
        ("0.09 + 0.01 = ?", "0.10", ["0.08", "0.001", "0.9"], "10 hundredths."),
        ("Find 3/4 of 2/3.", "1/2", ["5/7", "6/7", "5/12"], "3/4 × 2/3 = 6/12 = 1/2."),
        ("6 ÷ 2/3 = ?", "9", ["4", "8/3", "1/9"], "6 × 3/2 = 9."),
        ("A number line from 0 to 1: 0.5 and 1/2 are…", "the same point", ["0.5 is farther", "1/2 is farther", "not on the line"], "Equal rational numbers."),
        ("Simplify 12/18.", "2/3", ["12/18", "6/9", "3/2"], "÷6."),
    ]
    for text, ans, dist, expl in items:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1
    return _fill(qs, 55, lambda i: mq(
        f"How many 1/2s in {i % 6 + 2}?",
        2 * (i % 6 + 2),
        "Multiply by 2.",
        i,
    ))


def build_unit3():
    title = "Sixth Grade Math Unit 3: Rational Numbers — Fractions and Decimals"
    description = (
        "Divide fractions using pictures and reciprocals. Compute with multi-digit decimals and compare rational numbers."
    )
    c1 = concept_block(
        "1. How many pieces fit?",
        [
            "3 ÷ 1/2 asks how many halves are in 3 wholes. Each whole holds 2 halves, so 6.",
            "2/3 ÷ 1/6 asks how many sixths are in two-thirds. Two-thirds is 4 sixths, so 4.",
            "Draw equal pieces. Count them. That count is the quotient.",
            "When the divisor is a unit fraction 1/n, dividing a whole number n-times-as-big is the usual picture.",
            "This is the same idea as fifth grade, now mixed with non-unit fraction divisors.",
            "Stories: servings, cutting ribbon, filling bags.",
        ],
        fraction_divide_bars(3, "1/2", title="How many 1/2s in 3?")
        + solved(1, "Find 2/3 ÷ 1/6.",
                 ["2/3 = 4/6.",
                  "How many 1/6 pieces in 4/6? Four.",
                  "Quotient 4."],
                 "4"),
        kid_tip("Same-size pieces", "Rewrite both fractions with a common denominator, then divide the numerators."),
        1,
    )
    c2 = concept_block(
        "2. Multiply by the reciprocal",
        [
            "The reciprocal of a/b is b/a. The reciprocal of 4 is 1/4.",
            "Dividing by a fraction is multiplying by its reciprocal. 3/4 ÷ 2/5 = 3/4 × 5/2.",
            "Keep the first number, change ÷ to ×, flip the second.",
            "Check with the picture: (2/3) ÷ (1/6) = (2/3)×6 = 4. Same 4 as counting sixths.",
            "A whole number is a fraction with bottom 1. 6 ÷ 2/3 = 6/1 × 3/2 = 9.",
            "Simplify before or after. Canceling common factors is just early simplifying.",
        ],
        tape_diagram(
            [
                ("2/3", [("#86efac", 4, "1/6")]),
            ],
            title="(2/3) ÷ (1/6) is keep, change, flip",
            caption="2/3 = 4/6, so four sixths fit. Keep 2/3, change ÷ to ×, flip 1/6 to 6: (2/3)×6 = 4. Same count.",
        )
        + solved(1, "Compute (2/3) ÷ (4/9).",
               ["Flip 4/9 to 9/4.",
                "2/3 × 9/4 = 18/12.",
                "18/12 = 3/2."],
               "3/2")
        + step_reveal(
            ["Write both as fractions.",
             "Keep the first.",
             "Change ÷ to × and flip the second.",
             "Multiply and simplify."],
            vid="g6u3-c2-steps",
        )
        + phet_box("build_frac"),
        watch_out("Flipping both fractions", "Only the divisor (the second number) flips. The first number stays."),
        6,
    )
    c3 = concept_block(
        "3. Fraction stories",
        [
            "How many 1/8-pound servings in a 3/4-pound bag? (3/4) ÷ (1/8) = 6 servings.",
            "Half of a 2/3-cup recipe is multiply, not divide: (1/2)×(2/3)=1/3 cup.",
            "Read 'how many fit' as divide. Read 'a fraction of' as multiply.",
            "2 1/2 ÷ 1/2 = 5: five half-cups in two and a half cups.",
            "Label servings, cups, miles — the unit proves you answered the question asked.",
            "If a check with multiplication fails, you likely chose × when you needed ÷ (or the reverse).",
        ],
        tape_diagram(
            [
                ("bag", [("#86efac", 6, "1/8")]),
            ],
            title="A 3/4-pound bag in 1/8-pound servings",
            caption="3/4 = 6/8, so six servings of 1/8 pound fill the bag.",
        )
        + solved(1, "A 3/4-pound bag is split into 1/8-pound servings. How many servings?",
                 ["This is how many fit: divide.",
                  "(3/4) ÷ (1/8) = (3/4)×8 = 6.",
                  "6 servings."],
                 "6 servings"),
        11,
    )
    c4 = concept_block(
        "4. Multi-digit decimals",
        [
            "Add and subtract by lining up decimal points. Annex zeros if you need matching places.",
            "Multiply as whole numbers, then count total decimal places for the point.",
            "Divide by making the divisor a whole number: multiply both numbers by 10, 100, or 1,000.",
            "7.2 ÷ 0.8 → 72 ÷ 8 = 9.",
            "Estimate: 24.6 ÷ 3 is near 24 ÷ 3 = 8, so 8.2 is reasonable.",
            "Place value still rules. 0.09 + 0.01 = 0.10, not 0.1 written carelessly as 0.010 unless you mean thousandths.",
        ],
        double_number_line(
            "amount", [0, 0.8, 7.2],
            "groups", [0, 1, 9],
            title="How many 0.8s fit in 7.2?",
            caption="Each group is 0.8. Nine groups make 7.2, so 7.2 ÷ 0.8 = 9. Same as 72 ÷ 8 after moving the point.",
        )
        + solved(1, "Find 7.2 ÷ 0.8.",
               ["Multiply both by 10: 72 ÷ 8.",
                "72 ÷ 8 = 9.",
                "Check: 9 × 0.8 = 7.2."],
               "9")
        + matching(
            [("1.5 + 2.25", "3.75"), ("4.2 − 1.15", "3.05"),
             ("0.6 × 0.4", "0.24"), ("7.2 ÷ 0.8", "9")],
            vid="g6u3-c4-match",
        ),
        try_this("Estimate the point", "If 0.6 × 0.4 came out 2.4, the point sat two places too far right."),
        16,
    )
    c5 = concept_block(
        "5. Fractions, decimals, percents together",
        [
            "A rational number can wear three outfits: 3/5 = 0.6 = 60%.",
            "To compare, convert to the same outfit. 0.7, 3/4, and 70%: 0.70, 0.75, 0.70. Greatest is 3/4.",
            "Least of 0.4, 2/5, 3/10: 0.40, 0.40, 0.30. Least is 3/10.",
            "Terminating decimals like 0.25 are 25/100 = 1/4. Repeating decimals like 1/3 = 0.333… are still rational.",
            "Simplify fractions. 12/18 = 2/3.",
            "On a number line from 0 to 1, equal numbers sit on the same point.",
        ],
        percent_bar(60, 1, title="60% of 1 whole", caption="60% = 0.6 = 3/5. Same amount, three names.")
        + solved(1, "Which is greatest: 0.7, 3/4, or 70%?",
                 ["0.7 = 0.70 = 70%.",
                  "3/4 = 0.75.",
                  "0.75 is greatest, so 3/4."],
                 "3/4"),
        watch_out("Comparing digit length", "0.30 looks 'longer' than 0.4 if you forget 0.4 = 0.40. Convert, then compare."),
        21,
    )
    c6 = concept_block(
        "6. Choose the operation",
        [
            "Of often means multiply: 3/4 of 2/3 is (3/4)×(2/3)=1/2.",
            "How many groups means divide.",
            "Join or leftover means add or subtract — with matching denominators or lined-up points.",
            "Write the expression before you compute. The story should match the symbols.",
            "A number line, a tape, or an area model can confirm the operation.",
            "Sixth grade fluency is not speed for its own sake. It is choosing the right tool quickly.",
        ],
        tape_diagram(
            [
                ("cup", [("#86efac", 2, "2/3"), ("#e2e8f0", 1, "")]),
            ],
            title="Half of a 2/3-cup mix",
            caption="The cup has 3 equal parts. 2/3 is two parts. Half of those two parts is one part: (1/2)×(2/3)=1/3 cup.",
        )
        + solved(1, "You have 2/3 cup of mix and use 1/2 of it. How much do you use?",
               ["'Half of' means multiply.",
                "(1/2)×(2/3)=1/3.",
                "1/3 cup."],
               "1/3 cup")
        + step_reveal(
            ["Underline the question.",
             "Is it of, how many, join, or leftover?",
             "Write ×, ÷, +, or −.",
             "Compute with a common form (fraction or decimal).",
             "Label units."],
            vid="g6u3-c6-steps",
        ),
        26,
    )
    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "See division of fractions as counting pieces",
            "Multiply by the reciprocal",
            "Solve fraction stories",
            "Compute with multi-digit decimals",
            "Compare fractions, decimals, and percents",
            "Choose the right operation",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u3_questions()


# ===========================================================================
# UNIT 4: Integers
# ===========================================================================

def _u4_questions():
    qs = []
    idx = 1
    items = [
        ("The opposite of 5 is…", "−5", ["5", "0", "1/5"], "Same distance from 0, other side."),
        ("The opposite of −3 is…", "3", ["−3", "0", "−1/3"], "Opposite of a negative is positive."),
        ("The opposite of 0 is…", "0", ["1", "−1", "10"], "Zero is its own opposite."),
        ("Absolute value of −7 is…", "7", ["−7", "0", "1/7"], "Distance from 0 is 7."),
        ("|4| = ?", "4", ["−4", "0", "1/4"], "Distance from 0."),
        ("Which is less: −2 or −5?", "−5", ["−2", "0", "they are equal"], "−5 is farther left."),
        ("Which is greater: −1 or 0?", "0", ["−1", "1", "cannot tell"], "Zero is to the right of −1."),
        ("On a number line, left of 0 is…", "negative", ["positive", "absolute value", "percent"], "Right is positive."),
        ("A temperature of −4°C is…", "4 degrees below 0", ["4 above 0", "hotter than 4", "absolute 0"], "Negative means below zero."),
        ("A bank debit of $12 can be written…", "−12", ["12", "1/12", "120"], "Owing is negative in this model."),
        ("|−9| compared with 9 is…", "equal", ["|−9| is less", "|−9| is greater", "cannot compare"], "Both distances are 9."),
        ("The integer 3 units left of 1 is…", "−2", ["4", "2", "−1"], "1 − 3 = −2."),
        ("Opposites add to…", "0", ["1", "their product", "2"], "5 + (−5) = 0."),
        ("Which is between −3 and −1?", "−2", ["0", "−4", "1"], "The integer in the gap."),
        ("A point 5 units from 0 could be…", "5 or −5", ["only 5", "only −5", "0"], "Two points at distance 5."),
        ("−8 is to the left of −3. So −8 is…", "less than −3", ["greater than −3", "equal", "not an integer"], "Farther left is smaller."),
        ("Elevation −20 m means…", "20 m below sea level", ["20 m above", "sea level", "20% down"], "Negative elevation is below 0."),
        ("The integers are…", "…−2, −1, 0, 1, 2…", ["only positives", "only negatives", "fractions"], "Whole numbers and their opposites."),
        ("|0| = ?", "0", ["1", "−1", "undefined"], "Zero is 0 away from zero."),
        ("Which list is in order from least to greatest?", "−3, −1, 2", ["2, −1, −3", "−1, −3, 2", "2, −3, −1"], "Left to right on the line."),
        ("A gain of 6 then a loss of 6 lands at…", "the start", ["12", "−12", "6"], "Opposites cancel."),
        ("The opposite of the opposite of 4 is…", "4", ["−4", "0", "8"], "Two flips return you."),
        ("−15 compared with −4: which has greater absolute value?", "−15", ["−4", "same", "0"], "|−15|=15 > 4."),
        ("A football loss of 7 yards is…", "−7 yards", ["7 yards", "0", "7%"], "Loss as negative."),
        ("Integers do NOT include…", "1/2", ["−3", "0", "8"], "1/2 is rational but not an integer."),
        ("The number 4 units right of −1 is…", "3", ["5", "−5", "0"], "−1 + 4 = 3."),
        ("If |n| = 6, n could be…", "6 or −6", ["only 6", "only −6", "0"], "Two solutions."),
        ("Sea level as an integer is…", "0", ["1", "−1", "100"], "The origin for elevation."),
        ("Which is closest to 0: −8, −1, 5?", "−1", ["−8", "5", "all equal"], "Smallest absolute value among them is 1."),
        ("Positive, negative, and zero together on a line show…", "all integers in view", ["only ratios", "only percents", "only area"], "The integer number line."),
    ]
    for text, ans, dist, expl in items:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1
    return _fill(qs, 55, lambda i: mq(
        f"What is the opposite of {i % 8 + 1}?",
        -(i % 8 + 1),
        "Same distance from 0, other side.",
        i,
        distractors=[i % 8 + 1, 0, (i % 8 + 1) + 1],
    ))


def build_unit4():
    title = "Sixth Grade Math Unit 4: Integers and the Number Line"
    description = (
        "Place integers on a number line. Use opposites, absolute value, and real-world positives and negatives."
    )
    c1 = concept_block(
        "1. Integers live on both sides of zero",
        [
            "Integers are … −3, −2, −1, 0, 1, 2, 3 … Whole numbers and their opposites.",
            "To the right of 0 is positive. To the left of 0 is negative.",
            "Zero is neither positive nor negative. It is the origin of the line.",
            "−5 is less than −2 because it sits farther left, even though 5 looks 'bigger' than 2.",
            "Read a temperature, an elevator, a bank account, or a football play: negatives show up in the world.",
            "Fractions like 1/2 are rational but not integers. Integers have no leftover fractional part.",
        ],
        integer_line(-6, 6, marks=[(-5, "−5"), (0, "0"), (3, "3")],
                     title="An integer number line",
                     caption="Left of zero is negative. Right is positive. −5 is less than 3 because it is farther left.")
        + solved(1, "Which is less, −2 or −5?",
                 ["Plot both.",
                  "−5 is to the left of −2.",
                  "Left means less. −5 is less."],
                 "−5")
        + phet_box("nl_int"),
        kid_tip("Think left and right, not 'bigger looking digits'", "On the number line, less is left. Always."),
        1,
    )
    c2 = concept_block(
        "2. Opposites",
        [
            "Opposites are the same distance from 0 on opposite sides. The opposite of 5 is −5.",
            "The opposite of −3 is 3. Two flips return you to the start: the opposite of the opposite of 4 is 4.",
            "The opposite of 0 is 0.",
            "Opposites add to 0. That is why a gain of 6 and a loss of 6 cancel.",
            "In a story, opposite often means 'the other direction': up/down, credit/debit, east/west.",
            "Writing −(−4) is another way to say the opposite of −4, which is 4.",
        ],
        integer_line(-6, 6, marks=[(-4, "−4"), (4, "4")],
                     title="Opposites: −4 and 4",
                     caption="Each is 4 units from 0. They sit as mirror images across zero.")
        + solved(1, "What is the opposite of −3?",
                 ["−3 is 3 units left of 0.",
                  "The mirror point is 3 units right.",
                  "The opposite is 3."],
                 "3")
        + matching(
            [("opposite of 5", "−5"), ("opposite of −2", "2"),
             ("opposite of 0", "0"), ("5 + (−5)", "0")],
            vid="g6u4-c2-match",
        ),
        6,
    )
    c3 = concept_block(
        "3. Absolute value is distance",
        [
            "Absolute value |n| is the distance from n to 0. Distances are never negative.",
            "|−7| = 7 and |4| = 4. |0| = 0.",
            "If |n| = 6, then n is 6 or −6. Two points sit at distance 6 from 0.",
            "A number can be smaller (farther left) and still have a larger absolute value: |−15| > |−4|.",
            "Absolute value answers 'how far?' not 'which way?'",
            "In a story, 'how many degrees below zero' is an absolute value. The sign tells you below.",
        ],
        integer_line(-6, 6, marks=[(-5, "|−5|=5"), (5, "|5|=5")],
                     title="Same distance, two directions",
                     caption="Both points are 5 units from 0. Absolute value cares about distance, not sign.")
        + solved(1, "Find |−7|.",
                 ["−7 is 7 units from 0.",
                  "Distance is 7.",
                  "|−7| = 7."],
                 "7"),
        watch_out("Thinking |−7| is −7", "The bars mean distance. Distance is 7, not −7."),
        11,
    )
    c4 = concept_block(
        "4. Compare and order integers",
        [
            "Plot, then read left to right: least to greatest.",
            "−3, −1, 2 is increasing order. 2, −1, −3 is the reverse.",
            "Any negative is less than 0, and 0 is less than any positive.",
            "Among negatives, the one farther from 0 is smaller: −8 < −3.",
            "Closest to 0 among −8, −1, 5 is −1 (absolute value 1).",
            "A table of elevations or scores becomes easy once you imagine the line.",
        ],
        integer_line(-6, 6, marks=[(-3, "−3"), (-1, "−1"), (2, "2")],
                     title="Order −3, −1, and 2",
                     caption="Read left to right for least to greatest: −3, then −1, then 2.")
        + solved(1, "Order −3, 2, and −1 from least to greatest.",
               ["Plot: −3, then −1, then 2.",
                "Least is leftmost: −3.",
                "Then −1, then 2."],
               "−3, −1, 2")
        + matching(
            [("least of −2, −5", "−5"), ("greatest of −1, 0", "0"),
             ("closest to 0 among −8, −1, 5", "−1"), ("between −3 and −1", "−2")],
            vid="g6u4-c4-match",
        ),
        try_this("Draw a tiny line", "Even a sketch from −5 to 5 prevents sign mix-ups."),
        16,
    )
    c5 = concept_block(
        "5. Integers in the world",
        [
            "Temperature: −4°C is 4 degrees below 0.",
            "Elevation: −20 m is 20 meters below sea level. Sea level is 0.",
            "Money: a debit of $12 can be −12 in a simple model. A credit is positive.",
            "Football: a loss of 7 yards is −7 yards from the line.",
            "The sign is direction. The absolute value is size.",
            "Write the integer, then say the sentence in words to check it matches the story.",
        ],
        integer_line(-6, 6, marks=[(-4, "−4°"), (2, "+2°")],
                     title="A thermometer as a number line",
                     caption="−4° is below zero. +2° is above. Zero is freezing on the Celsius scale.")
        + solved(1, "A submarine is 20 meters below sea level. Write the elevation as an integer.",
                 ["Below sea level is negative.",
                  "The size is 20.",
                  "Elevation −20 m."],
                 "−20 m")
        + step_reveal(
            ["Is the story above/below, gain/loss, credit/debit?",
             "Choose + or −.",
             "Write the size as the absolute value.",
             "Read the integer back in words."],
            vid="g6u4-c5-steps",
        ),
        21,
    )
    c6 = concept_block(
        "6. Moving on the line",
        [
            "Start at a point. Moving right adds a positive. Moving left adds a negative (or subtracts a positive).",
            "3 units left of 1 is −2. 4 units right of −1 is 3.",
            "A gain of 6 then a loss of 6 returns to the start — opposites.",
            "You do not need the full integer-operation rules of seventh grade yet. You do need to move and count.",
            "If |n| = 6, the two landings are 6 and −6. The story may pick one (only below zero, only a loss).",
            "Keep 0 in view. It is the landmark that makes 'left' and 'right' mean something.",
        ],
        integer_line(-6, 6, marks=[(1, "start"), (-2, "land")],
                     title="Start at 1, move 3 left",
                     caption="Left 3 units from 1 lands at −2. Moving left is toward the negatives.")
        + solved(1, "You start at 1 and move 3 units left. Where do you land?",
               ["Left means toward the negatives.",
                "1 − 3 = −2.",
                "You land at −2."],
               "−2")
        + matching(
            [("3 left of 1", "−2"), ("4 right of −1", "3"),
             ("gain 6 then lose 6", "start"), ("|n|=6", "n is 6 or −6")],
            vid="g6u4-c6-match",
        ),
        26,
    )
    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Place integers on a number line",
            "Name opposites",
            "Use absolute value as distance",
            "Compare and order integers",
            "Read integers in real stories",
            "Move left and right on the line",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u4_questions()
