"""Second bank module: elementary & high-school math, AP Calculus and AP Statistics.

Same anatomy as the rest of the bank (four options, a `why` on every distractor,
a two-step hint ladder, solution steps), and every item is written for Veelearn.
Contest and admissions exams are copyrighted and their problems are actively
used for scoring, so nothing here is copied: these are original questions in the
style of each exam.

`M()` is the compact form used below — the right answer first, then the three
distractors with the misconception each one catches. The options are rotated
deterministically so the key is not always A.

Diagrams are authored SVGs (`visual = {"svg": ..., "alt": ...}`); the seed
builder checks every one of them for safety before it can reach the database.
"""

from __future__ import annotations

from seed.qbank_exams import Q

INK = "#334155"
ACCENT = "#ea580c"


def svg(body, alt):
    return {
        "svg": (
            "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 200' role='img' "
            "aria-label='" + alt + "' font-family='Nunito, Arial, sans-serif'>" + body + "</svg>"
        ),
        "alt": alt,
    }


def M(skill, tier, stem, correct, wrongs, hints, steps, visual=None):
    """Compact question: right answer, then (text, why) for each distractor."""
    opts = [(correct, 1, "")] + [(t, 0, w) for t, w in wrongs]
    i = (sum(ord(c) for c in stem) + tier) % 4
    opts = opts[-i:] + opts[:-i]
    return Q(skill, tier, stem, opts, hints, steps, visual=visual)


# --------------------------------------------------------------------------- #
# Diagram builders. Each takes the numbers the question is about, so a picture
# can never disagree with the stem.
# --------------------------------------------------------------------------- #


def frac_bars(parts, filled, alt, label=""):
    w = 260.0 / parts
    body = "<g stroke='%s' fill='none' stroke-width='1.4'>" % INK
    for i in range(parts + 1):
        x = 30 + i * w
        body += "<path d='M%.1f 60 V140'/>" % x
    body += "<path d='M30 60 H290 M30 140 H290'/></g>"
    for i in range(filled):
        body += "<rect x='%.1f' y='60' width='%.1f' height='80' fill='%s' fill-opacity='0.26'/>" % (
            30 + i * w,
            w,
            ACCENT,
        )
    if label:
        body += "<text x='30' y='168' font-size='13' fill='%s'>%s</text>" % (INK, label)
    return svg(body, alt)


def bars(pairs, alt, width=190.0):
    """Horizontal bar chart: pairs of (label, value)."""
    top = 30.0
    gap = 34.0
    body = ""
    for i, (label, value) in enumerate(pairs):
        y = top + i * gap
        w = width * value
        body += "<text x='20' y='%.1f' font-size='13' fill='%s'>%s</text>" % (y + 12, INK, label)
        body += "<rect x='95' y='%.1f' width='%.1f' height='18' rx='4' fill='%s' fill-opacity='0.28' stroke='%s' stroke-width='1.2'/>" % (
            y,
            w,
            ACCENT,
            INK,
        )
        body += "<text x='%.1f' y='%.1f' font-size='12' fill='%s'>%s</text>" % (100 + w, y + 13, INK, value)
    return svg(body, alt)


def triangle_right(leg_label, other_label, hyp_label, alt):
    body = (
        "<path d='M60 160 L60 60 L240 160 Z' fill='none' stroke='%s' stroke-width='2'/>"
        "<path d='M60 146 H74 V160' fill='none' stroke='%s' stroke-width='1.4'/>"
        "<text x='34' y='114' font-size='14' fill='%s'>%s</text>"
        "<text x='140' y='182' font-size='14' fill='%s'>%s</text>"
        "<text x='160' y='102' font-size='14' fill='%s'>%s</text>" % (INK, INK, INK, leg_label, INK, other_label, INK, hyp_label)
    )
    return svg(body, alt)


def rect_labelled(w_text, h_text, alt):
    body = (
        "<rect x='50' y='60' width='200' height='100' fill='none' stroke='%s' stroke-width='2'/>"
        "<text x='142' y='182' font-size='14' fill='%s'>%s</text>"
        "<text x='256' y='118' font-size='14' fill='%s'>%s</text>" % (INK, INK, w_text, INK, h_text)
    )
    return svg(body, alt)


def circle_r(label, alt, r=58):
    body = (
        "<circle cx='160' cy='98' r='%d' fill='none' stroke='%s' stroke-width='2'/>"
        "<path d='M160 98 L%d 98' stroke='%s' stroke-width='1.5' stroke-dasharray='5 4'/>"
        "<circle cx='160' cy='98' r='3' fill='%s'/>"
        "<text x='%d' y='92' font-size='14' fill='%s'>%s</text>" % (r, INK, 160 + r, INK, INK, 164 + r // 2, INK, label)
    )
    return svg(body, alt)


def numline(labels, alt, ticks=None):
    """labels: list of (position 0..1, text)."""
    body = "<path d='M30 110 H290' stroke='%s' stroke-width='2'/>" % INK
    for i in range(11):
        x = 30 + i * 26
        body += "<path d='M%.1f 104 V116' stroke='%s' stroke-width='1.4'/>" % (x, INK)
    for pos, label in labels:
        x = 30 + pos * 260
        body += "<text x='%.1f' y='140' font-size='12' fill='%s' text-anchor='middle'>%s</text>" % (x, INK, label)
    return svg(body, alt)


def table(headers, rows, alt):
    cols = len(headers)
    cw = 260.0 / cols
    body = "<rect x='30' y='46' width='260' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (
        34 + 28 * len(rows),
        INK,
    )
    for i, h in enumerate(headers):
        body += "<text x='%.1f' y='68' font-size='12.5' font-weight='700' fill='%s'>%s</text>" % (
            38 + i * cw,
            INK,
            h,
        )
    body += "<path d='M30 78 H290' stroke='%s' stroke-width='1.2'/>" % INK
    for r, row in enumerate(rows):
        y = 102 + r * 28
        for i, cell in enumerate(row):
            body += "<text x='%.1f' y='%d' font-size='12.5' fill='%s'>%s</text>" % (38 + i * cw, y, INK, cell)
        if r < len(rows) - 1:
            body += "<path d='M30 %d H290' stroke='%s' stroke-width='0.8' stroke-opacity='0.5'/>" % (y + 10, INK)
    return svg(body, alt)


def grid(n, m, alt):
    body = "<g stroke='%s' stroke-width='1.3' fill='none'>" % INK
    for i in range(n + 1):
        x = 60 + i * (200.0 / n)
        body += "<path d='M%.1f 40 V160'/>" % x
    for j in range(m + 1):
        y = 160 - j * (120.0 / m)
        body += "<path d='M60 %.1f H260'/>" % y
    body += "</g><circle cx='60' cy='160' r='4' fill='%s'/><circle cx='260' cy='40' r='4' fill='%s'/>" % (ACCENT, ACCENT)
    return svg(body, alt)


def code_block(lines, alt):
    body = "<rect x='18' y='24' width='284' height='%d' rx='8' fill='#0f172a'/>" % (40 + 22 * len(lines))
    for i, line in enumerate(lines):
        body += "<text x='34' y='%d' font-size='13' fill='#e2e8f0' xml:space='preserve'>%s</text>" % (
            50 + i * 22,
            line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"),
        )
    return svg(body, alt)


def parabola(alt):
    body = (
        "<path d='M40 160 H280 M160 170 V30' stroke='%s' stroke-width='1.5'/>"
        "<path d='M60 40 Q160 190 260 40' fill='none' stroke='%s' stroke-width='2.4'/>"
        "<circle cx='160' cy='118' r='4' fill='%s'/>"
        "<text x='168' y='132' font-size='12' fill='%s'>vertex</text>" % (INK, ACCENT, ACCENT, INK)
    )
    return svg(body, alt)


def area_under(alt):
    body = (
        "<path d='M40 160 H280 M60 170 V40' stroke='%s' stroke-width='1.5'/>"
        "<path d='M60 60 Q170 40 260 150' fill='none' stroke='%s' stroke-width='2.2'/>"
        "<path d='M60 60 Q170 40 260 150 L260 160 H60 Z' fill='%s' fill-opacity='0.22'/>" % (INK, ACCENT, ACCENT)
    )
    return svg(body, alt)


def wave_diagram(alt):
    body = (
        "<path d='M30 100 C70 40 110 40 150 100 C190 160 230 160 290 100' fill='none' stroke='%s' stroke-width='2.4'/>"
        "<path d='M30 100 H290' stroke='%s' stroke-width='1' stroke-dasharray='4 4'/>" % (ACCENT, INK)
    )
    return svg(body, alt)


# --------------------------------------------------------------------------- #
# Grades 1-8 math
# --------------------------------------------------------------------------- #

_ME = [
    # ----------------------------------------------------------- me.place
    M("me.place", 1,
      "In the number 47,382, what is the value of the digit 7?",
      "7,000",
      [("700", "That is the hundreds place, two places to the right of the 7."),
       ("70", "That is the tens place, three places to the right."),
       ("700,000", "That is six places, so you moved the wrong way through the places.")],
      ["Read the places from the right: ones, tens, hundreds, thousands.", "The 7 sits in the thousands place."],
      ["The digit 7 is in the thousands place.", "So its value is 7 × 1,000 = 7,000."],
      visual=table(["Place", "Digit"], [["thousands", "7"], ["hundreds", "3"], ["tens", "8"], ["ones", "2"]],
                   "Place-value table for 47,382 showing 7 in the thousands place")),

    M("me.place", 2,
      "Round 6,847 to the nearest hundred.",
      "6,800",
      [("6,900", "That rounds up, but the tens digit 4 is below 5, so the hundreds digit stays."),
       ("6,000", "That is rounding to the nearest thousand, not hundred."),
       ("6,850", "Rounding to a place value never leaves a nonzero digit to its right.")],
      ["Underline the hundreds digit, then look at the tens digit.", "The tens digit is 4, which is less than 5."],
      ["The hundreds digit is 8 and the tens digit is 4.", "Since 4 < 5, keep 8 and write zeros: 6,800."]),

    M("me.place", 2,
      "Which digit is in the thousands place of 305,918?",
      "5",
      [("3", "That is the hundred-thousands place, the leftmost digit."),
       ("0", "That is the ten-thousands place."),
       ("9", "That is the hundreds place, on the other side of the comma.")],
      ["Count the places from the right: ones, tens, hundreds, then thousands.", "The comma after 305 marks the thousands."],
      ["From the right: 8 ones, 1 ten, 9 hundreds, 5 thousands.", "So the thousands digit is 5."]),

    M("me.place", 3,
      "A whole number rounds to 500 when rounded to the nearest hundred. Which number could it be?",
      "461",
      [("441", "441 rounds down to 400 because the tens digit is 4."),
       ("552", "552 rounds up to 600 because the tens digit is 5."),
       ("405", "405 rounds down to 400 because the tens digit is 0.")],
      ["A number rounds to 500 if it is at least 450 and less than 550.", "Check which option sits inside that range."],
      ["461 is between 450 and 549.", "So 461 rounds to 500."]),

    M("me.place", 4,
      "What is 8,000 + 40 + 6 written in standard form?",
      "8,046",
      [("846", "That drops the thousands and tens places entirely."),
       ("8,460", "That puts the 4 in the hundreds place instead of the tens."),
       ("84,006", "That moves the 4 into the ten-thousands place.")],
      ["Each addend fills one place value: thousands, tens, ones.", "Write a 0 in the hundreds place."],
      ["8,000 + 0 hundreds + 40 + 6.", "So the number is 8,046."]),

    # -------------------------------------------------------- me.multdiv
    M("me.multdiv", 1,
      "What is 7 × 8?",
      "56",
      [("54", "That is 6 × 9, one row short of the 7-row table."),
       ("48", "That is 6 × 8, so you used one group too few."),
       ("64", "That is 8 × 8, one group too many.")],
      ["Think of seven groups of eight.", "5 × 8 = 40 and 2 × 8 = 16."],
      ["Split 7 into 5 + 2.", "40 + 16 = 56."]),

    M("me.multdiv", 2,
      "A rectangle of tiles has 6 rows with 4 tiles in each row. How many tiles are there?",
      "24",
      [("10", "That adds the rows and columns instead of multiplying them."),
       ("20", "That is 5 rows of 4, one row short."),
       ("28", "That is 7 rows of 4, one row too many.")],
      ["Each row holds 4 tiles and there are 6 rows.", "Repeated addition is multiplication: 4 + 4 + 4 + 4 + 4 + 4."],
      ["6 rows × 4 tiles per row.", "6 × 4 = 24 tiles."],
      visual=grid(6, 4, "Six by four array of tiles")),

    M("me.multdiv", 2,
      "What is 63 ÷ 9?",
      "7",
      [("6", "6 × 9 = 54, which is 9 short of 63."),
       ("8", "8 × 9 = 72, which is past 63."),
       ("9", "That is the divisor, not the quotient.")],
      ["Ask: 9 times what number gives 63?", "Use the 9s facts you know."],
      ["9 × 7 = 63.", "So 63 ÷ 9 = 7."]),

    M("me.multdiv", 3,
      "Each box holds 12 pencils. How many pencils are in 7 boxes?",
      "84",
      [("72", "That is 6 boxes, one box short."),
       ("96", "That is 8 boxes, one box too many."),
       ("74", "That adds 7 and 12 instead of multiplying.")],
      ["Multiply the number of boxes by pencils per box.", "12 × 7 = 12 × 5 + 12 × 2."],
      ["12 × 5 = 60 and 12 × 2 = 24.", "60 + 24 = 84 pencils."]),

    M("me.multdiv", 4,
      "A number multiplied by 8 gives 96. What is the number?",
      "12",
      [("11", "11 × 8 = 88, which is 8 short."),
       ("13", "13 × 8 = 104, which is 8 too many."),
       ("88", "That is 96 − 8, subtracting instead of dividing.")],
      ["Turn the multiplication around into a division.", "96 ÷ 8 = ?"],
      ["96 ÷ 8 = 12.", "Check: 12 × 8 = 96."]),

    # ------------------------------------------------------- me.fractions
    M("me.fractions", 1,
      "Which fraction is equivalent to 1/2?",
      "3/6",
      [("2/3", "That is more than 1/2 because the numerator is more than half the denominator."),
       ("4/6", "That is 2/3, bigger than 1/2."),
       ("1/3", "That is smaller than 1/2.")],
      ["Multiply the top and bottom by the same number.", "1/2 = 2/4 = 3/6."],
      ["1 × 3 = 3 and 2 × 3 = 6.", "So 1/2 = 3/6."],
      visual=frac_bars(6, 3, "A bar split into six equal parts with three shaded", label="3 of 6 parts shaded")),

    M("me.fractions", 2,
      "Which is larger, 3/5 or 5/8?",
      "5/8",
      [("3/5", "3/5 = 0.6, which is smaller than 5/8 = 0.625."),
       ("They are equal", "3/5 = 24/40 and 5/8 = 25/40, so they are close but not equal."),
       ("You cannot compare them", "Any two fractions can be compared over a common denominator.")],
      ["Use a common denominator of 40, or turn both into decimals.", "3/5 = 24/40 and 5/8 = 25/40."],
      ["25/40 > 24/40.", "So 5/8 is the larger fraction."],
      visual=frac_bars(8, 5, "A bar split into eight equal parts with five shaded", label="5/8 shaded")),

    M("me.fractions", 2,
      "Simplify 12/18.",
      "2/3",
      [("3/2", "That flips the fraction upside down."),
       ("6/9", "That divides by 2 only; both parts still share a factor of 3."),
       ("4/9", "That divides the numerator and denominator by different numbers.")],
      ["Find the biggest number that divides both 12 and 18.", "6 divides both."],
      ["12 ÷ 6 = 2 and 18 ÷ 6 = 3.", "So 12/18 = 2/3."]),

    M("me.fractions", 3,
      "Order these from least to greatest: 2/3, 3/5, 7/10.",
      "3/5, 2/3, 7/10",
      [("2/3, 3/5, 7/10", "That keeps the written order, but 3/5 is smaller than 2/3."),
       ("7/10, 2/3, 3/5", "That is greatest to least, the reverse order."),
       ("3/5, 7/10, 2/3", "7/10 = 0.7 is bigger than 2/3 ≈ 0.667, so the last two are swapped.")],
      ["Write each as a decimal or over a denominator of 30.", "2/3 ≈ 0.67, 3/5 = 0.6, 7/10 = 0.7."],
      ["3/5 = 0.6, 2/3 ≈ 0.667, 7/10 = 0.7.", "Least to greatest: 3/5, 2/3, 7/10."]),

    M("me.fractions", 4,
      "A recipe uses 3/4 cup of sugar for 12 cookies. How much sugar is needed for 8 cookies?",
      "1/2 cup",
      [("3/8 cup", "That halves the numerator but keeps the full denominator, so it is far too small."),
       ("2/3 cup", "That is a rough guess, not the proportional amount."),
       ("1/4 cup", "That is a third of the recipe, but 8 cookies is two thirds of 12.")],
      ["Find the sugar per cookie, or scale by 8/12.", "8/12 = 2/3, so take two thirds of 3/4."],
      ["Sugar per cookie: (3/4) ÷ 12 = 1/16 cup.", "For 8 cookies: 8/16 = 1/2 cup."]),

    # ------------------------------------------------------ me.decpercent
    M("me.decpercent", 1,
      "Write 0.35 as a percent.",
      "35%",
      [("3.5%", "You divided by 10 instead of multiplying by 100."),
       ("350%", "You multiplied by 1,000, moving the decimal one place too far."),
       ("0.35%", "That just keeps the decimal and adds a percent sign.")],
      ["Percent means out of 100.", "Multiply the decimal by 100."],
      ["0.35 × 100 = 35.", "So 0.35 = 35%."]),

    M("me.decpercent", 2,
      "What is 25% of 80?",
      "20",
      [("25", "That copies the percent instead of applying it."),
       ("40", "That is 50% of 80."),
       ("15", "That is about 20% of 80, not 25%.")],
      ["25% is one quarter.", "Divide 80 by 4."],
      ["80 ÷ 4 = 20.", "So 25% of 80 is 20."]),

    M("me.decpercent", 2,
      "Which number is greater, 0.6 or 0.58?",
      "0.6",
      [("0.58", "More digits does not mean a bigger number; compare place by place."),
       ("They are equal", "0.6 = 0.60, which is bigger than 0.58."),
       ("You cannot compare them", "Decimals compare place value by place value.")],
      ["Write 0.6 as 0.60 so both have two decimal places.", "Compare the hundredths digits."],
      ["0.6 = 0.60.", "0.60 > 0.58, so 0.6 is greater."]),

    M("me.decpercent", 3,
      "A $40 jacket is 15% off. What is the sale price?",
      "$34",
      [("$25", "That subtracts 15 dollars instead of 15 percent."),
       ("$36", "That is only 10% off."),
       ("$6", "That is the discount itself, not the price you pay.")],
      ["First find 15% of 40, then subtract it.", "10% of 40 is 4 and 5% is 2."],
      ["15% of 40 = 6.", "40 − 6 = $34."]),

    M("me.decpercent", 4,
      "A price rises from $25 to $30. What is the percent increase?",
      "20%",
      [("5%", "That is the dollar increase, not the percent."),
       ("25%", "That divides the change by the new price instead of the original."),
       ("16.7%", "That is 5/30, using the new price as the base.")],
      ["Percent change = change ÷ original × 100.", "The change is 5 and the original is 25."],
      ["5 ÷ 25 = 0.2.", "0.2 × 100 = 20%."]),

    # ----------------------------------------------------------- me.ratio
    M("me.ratio", 1,
      "Simplify the ratio 12 : 18.",
      "2 : 3",
      [("3 : 2", "That reverses the order of the two quantities."),
       ("4 : 6", "That divides by 3 only; 4 and 6 still share a factor of 2."),
       ("6 : 9", "That divides by 2 only; 6 and 9 still share a factor of 3.")],
      ["Divide both parts by the same number.", "The greatest common factor of 12 and 18 is 6."],
      ["12 ÷ 6 = 2 and 18 ÷ 6 = 3.", "So the ratio is 2 : 3."]),

    M("me.ratio", 2,
      "If 3 pens cost $4.50, how much do 5 pens cost?",
      "$7.50",
      [("$6.00", "That is the price of 4 pens."),
       ("$9.00", "That is the price of 6 pens."),
       ("$7.00", "That is a guess that ignores the unit price.")],
      ["Find the cost of one pen first.", "$4.50 ÷ 3 = ?"],
      ["One pen costs $1.50.", "5 × $1.50 = $7.50."]),

    M("me.ratio", 2,
      "A car travels 150 miles in 3 hours. What is its average speed?",
      "50 mph",
      [("45 mph", "That divides 150 by 3.33, not 3."),
       ("75 mph", "That halves the distance instead of dividing it by the time."),
       ("100 mph", "That divides 300 by 3.")],
      ["Speed is distance divided by time.", "150 ÷ 3 = ?"],
      ["150 ÷ 3 = 50.", "So the average speed is 50 mph."]),

    M("me.ratio", 3,
      "The ratio of red to blue marbles is 3 : 5. If there are 24 red marbles, how many blue marbles are there?",
      "40",
      [("32", "That uses a ratio of 3 : 4."),
       ("45", "That scales the 5 by 9, but 24 ÷ 3 = 8, not 9."),
       ("15", "That is the number of blues if there were 9 reds.")],
      ["Find the scale factor from 3 red to 24 red.", "24 ÷ 3 = 8, so scale everything by 8."],
      ["Scale factor is 8.", "5 × 8 = 40 blue marbles."],
      visual=bars([("red", 24), ("blue", 40)], "Bar model showing 24 red marbles and 40 blue marbles")),

    M("me.ratio", 4,
      "A recipe for 4 servings needs 6 cups of flour. How many cups are needed for 10 servings?",
      "15",
      [("12", "That is 8 servings, not 10."),
       ("10", "That copies the number of servings instead of the flour."),
       ("16", "That is 10 servings at 1.6 cups each, which is not the recipe's rate.")],
      ["Find the flour per serving.", "6 ÷ 4 = 1.5 cups per serving."],
      ["1.5 cups per serving.", "10 × 1.5 = 15 cups."]),

    # -------------------------------------------------------- me.geometry
    M("me.geometry", 1,
      "What is the area of a rectangle 8 cm by 3 cm?",
      "24 cm²",
      [("11 cm²", "That adds the sides; area multiplies them."),
       ("22 cm²", "That is the perimeter, not the area."),
       ("48 cm²", "That doubles the product.")],
      ["Area of a rectangle is length × width.", "8 × 3 = ?"],
      ["8 × 3 = 24.", "The area is 24 cm²."],
      visual=rect_labelled("8 cm", "3 cm", "Rectangle eight centimetres wide and three centimetres tall")),

    M("me.geometry", 2,
      "What is the perimeter of a square with side length 7 m?",
      "28 m",
      [("49 m", "That is the area: 7 × 7."),
       ("21 m", "That adds three sides instead of four."),
       ("14 m", "That adds only two sides.")],
      ["A square has four equal sides.", "Perimeter = 4 × side."],
      ["4 × 7 = 28.", "The perimeter is 28 m."]),

    M("me.geometry", 2,
      "What is the area of a triangle with base 10 and height 6?",
      "30",
      [("60", "That is base × height; a triangle is half of that rectangle."),
       ("16", "That adds the base and the height."),
       ("36", "That is 6², using the height as a side of a square.")],
      ["Area of a triangle is half of base × height.", "(10 × 6) ÷ 2 = ?"],
      ["10 × 6 = 60.", "Half of 60 is 30."],
      visual=triangle_right("6", "10", "", "Triangle with a height of six on a base of ten")),

    M("me.geometry", 3,
      "What is the volume of a box that is 2 × 3 × 4 units?",
      "24 cubic units",
      [("9 cubic units", "That adds the three dimensions."),
       ("12 cubic units", "That multiplies only two dimensions."),
       ("26 cubic units", "That adds the product of two sides to the third.")],
      ["Volume of a box is length × width × height.", "2 × 3 = 6 first."],
      ["2 × 3 = 6.", "6 × 4 = 24 cubic units."]),

    M("me.geometry", 4,
      "A circle has radius 5. Its area is about…",
      "78.5",
      [("31.4", "That is the circumference, 2πr."),
       ("15.7", "That is half the circumference."),
       ("50", "That is r² without multiplying by π.")],
      ["Area of a circle is πr².", "5² = 25, and π ≈ 3.14."],
      ["25 × 3.14 = 78.5.", "So the area is about 78.5 square units."],
      visual=circle_r("5", "Circle with radius five")),
]

# --------------------------------------------------------------------------- #
# High school math
# --------------------------------------------------------------------------- #

_HS = [
    # ------------------------------------------------------- hs.quadratics
    M("hs.quadratics", 1,
      "Factor x² − 9.",
      "(x − 3)(x + 3)",
      [("(x − 9)(x + 1)", "That expands to x² − 8x − 9, which has a middle term."),
       ("(x − 3)²", "That expands to x² − 6x + 9, with a middle term and +9."),
       ("(x + 9)(x − 1)", "That expands to x² + 8x − 9.")],
      ["This is a difference of two squares.", "x² − 9 = x² − 3²."],
      ["a² − b² = (a − b)(a + b).", "So x² − 9 = (x − 3)(x + 3)."]),

    M("hs.quadratics", 2,
      "Solve x² − 5x + 6 = 0.",
      "x = 2 or x = 3",
      [("x = 1 or x = 6", "Those multiply to 6 but add to 7, not 5."),
       ("x = −2 or x = −3", "Those add to −5; the middle term here is −5x but the product must be +6."),
       ("x = 0 or x = 5", "That ignores the constant term.")],
      ["Find two numbers that multiply to 6 and add to −5.", "Both numbers are negative."],
      ["−2 × −3 = 6 and −2 + −3 = −5.", "(x − 2)(x − 3) = 0, so x = 2 or x = 3."]),

    M("hs.quadratics", 2,
      "The vertex of y = (x − 2)² + 3 is…",
      "(2, 3)",
      [("(−2, 3)", "The sign inside the bracket flips: x − 2 puts the vertex at +2."),
       ("(2, −3)", "The +3 outside moves the graph up, not down."),
       ("(3, 2)", "That swaps the coordinates.")],
      ["Vertex form is y = (x − h)² + k with vertex (h, k).", "Read h from inside the bracket and k from outside."],
      ["h = 2 and k = 3.", "The vertex is (2, 3)."],
      visual=parabola("Parabola with its vertex marked")),

    M("hs.quadratics", 3,
      "What is the discriminant of x² + 4x + 8 = 0, and what does it tell you?",
      "−16, so there are no real roots",
      [("48, so there are two real roots", "That is 16 − 4·8 with a sign error in the last term."),
       ("16, so there is one repeated root", "The discriminant is b² − 4ac = 16 − 32, not 16."),
       ("0, so the roots are equal", "That would need 4ac = 16, but 4ac = 32.")],
      ["The discriminant is b² − 4ac.", "Here a = 1, b = 4, c = 8."],
      ["16 − 4(1)(8) = 16 − 32 = −16.", "A negative discriminant means no real roots."]),

    M("hs.quadratics", 4,
      "The equation 2x² − 8x + 6 = 0 has two roots. What do they add up to?",
      "4",
      [("−4", "The sum is −b/a, and b is already negative here, so it becomes positive."),
       ("3", "That is the product of the roots, c/a."),
       ("8", "That is b, without dividing by a.")],
      ["Sum of roots = −b/a.", "a = 2 and b = −8."],
      ["−(−8)/2 = 8/2 = 4.", "The two roots are 1 and 3, and they add to 4."]),

    # -------------------------------------------------------- hs.functions
    M("hs.functions", 1,
      "Evaluate f(3) for the function f(x) = 2x + 1.",
      "7",
      [("6", "That is 2 × 3 without adding 1."),
       ("5", "That is f(2)."),
       ("8", "That is 2 × 3 + 2.")],
      ["Replace every x with 3.", "2(3) + 1."],
      ["2 × 3 = 6.", "6 + 1 = 7."]),

    M("hs.functions", 2,
      "If f(x) = x² and g(x) = x + 1, what is f(g(2))?",
      "9",
      [("5", "That is g(f(2)); composition is not commutative."),
       ("7", "That adds the two results instead of composing them."),
       ("8", "That is 2³, mixing up the operations.")],
      ["Work from the inside out: g(2) first.", "Then put that result into f."],
      ["g(2) = 3.", "f(3) = 9."]),

    M("hs.functions", 2,
      "Compared with y = f(x), the graph of y = f(x) + 4 is shifted…",
      "up 4 units",
      [("down 4 units", "Adding outside the function moves the output up, not down."),
       ("left 4 units", "Horizontal shifts come from changes inside the brackets."),
       ("right 4 units", "That would be f(x − 4).")],
      ["A change outside f affects the y-values.", "+4 raises every output by 4."],
      ["Every point (x, y) becomes (x, y + 4).", "So the graph moves up 4 units."]),

    M("hs.functions", 3,
      "What is the inverse of f(x) = 3x − 6?",
      "(x + 6)/3",
      [("(x − 6)/3", "That subtracts before dividing; the inverse needs the opposite operation order."),
       ("3x + 6", "That is not an inverse at all — no division by 3."),
       ("x/3 + 6", "That divides only the x and then adds 6 instead of adding first.")],
      ["Swap x and y, then solve for y.", "x = 3y − 6."],
      ["x + 6 = 3y.", "y = (x + 6)/3."]),

    M("hs.functions", 4,
      "If f(x) = |x|, what is f(−4) + f(2)?",
      "6",
      [("2", "That is f(2) alone, ignoring the first term."),
       ("−2", "Absolute value is never negative, so that cannot be the sum."),
       ("8", "That treats f(−4) as 4 twice.")],
      ["Absolute value is the distance from zero.", "f(−4) = 4 and f(2) = 2."],
      ["f(−4) = 4.", "4 + 2 = 6."]),

    # ------------------------------------------------------------- hs.logs
    M("hs.logs", 1,
      "What is log₂ 8?",
      "3",
      [("2", "2² = 4, not 8."),
       ("4", "2⁴ = 16, too big."),
       ("8", "That is the argument, not the exponent.")],
      ["Ask: 2 to what power gives 8?", "2³ = 8."],
      ["2³ = 8, so log₂ 8 = 3."]),

    M("hs.logs", 2,
      "What is log₁₀ 1000?",
      "3",
      [("2", "10² = 100, one zero short."),
       ("100", "That is the argument divided by 10."),
       ("10", "That is the base.")],
      ["Count the zeros in 1000.", "Each zero is a factor of 10."],
      ["1000 = 10³.", "So log₁₀ 1000 = 3."]),

    M("hs.logs", 2,
      "Simplify log(a) + log(b).",
      "log(ab)",
      [("log(a + b)", "Logs turn products into sums, not sums into sums."),
       ("log(a / b)", "That is log(a) − log(b)."),
       ("log(a) · log(b)", "Multiplying the logs is not the same as the log of a product.")],
      ["Adding logs of the same base multiplies the arguments.", "log(a) + log(b) = log(a × b)."],
      ["The product rule for logs.", "log(a) + log(b) = log(ab)."]),

    M("hs.logs", 3,
      "Solve 2ˣ = 32.",
      "5",
      [("4", "2⁴ = 16, which is half of 32."),
       ("6", "2⁶ = 64, too big."),
       ("16", "That is 32 ÷ 2, not a power.")],
      ["Write 32 as a power of 2.", "2⁵ = 32."],
      ["32 = 2⁵.", "So x = 5."]),

    M("hs.logs", 4,
      "Solve ln(x) = 0.",
      "1",
      [("0", "ln(0) is undefined, so it cannot be 0."),
       ("e", "ln(e) = 1, not 0."),
       ("It has no solution", "ln(1) = 0, so a solution exists.")],
      ["ln means log base e.", "e⁰ = 1."],
      ["ln(x) = 0 means e⁰ = x.", "e⁰ = 1, so x = 1."]),

    # ------------------------------------------------------- hs.sequences
    M("hs.sequences", 1,
      "What comes next: 3, 6, 9, 12, …?",
      "15",
      [("13", "That adds 1; the pattern adds 3 each time."),
       ("14", "That doubles the last digit; the step is 3."),
       ("16", "That is 12 + 4.")],
      ["Find the difference between consecutive terms.", "6 − 3 = 3 and 9 − 6 = 3."],
      ["Each term grows by 3.", "12 + 3 = 15."]),

    M("hs.sequences", 2,
      "An arithmetic sequence starts at 5 with common difference 4. What is the 10th term?",
      "41",
      [("40", "That is 10 × 4, forgetting the starting value of 5."),
       ("45", "That uses 11 terms instead of 10."),
       ("44", "That is 4 × 11.")],
      ["aₙ = a₁ + (n − 1)d.", "a₁ = 5, d = 4, n = 10."],
      ["5 + 9 × 4 = 5 + 36.", "So a₁₀ = 41."]),

    M("hs.sequences", 2,
      "What comes next: 2, 6, 18, …?",
      "54",
      [("36", "That adds 18; this sequence multiplies by 3."),
       ("24", "That adds 6."),
       ("48", "That doubles 24, which is not in the sequence.")],
      ["Find the ratio between terms.", "6 ÷ 2 = 3 and 18 ÷ 6 = 3."],
      ["Each term is 3 times the one before.", "18 × 3 = 54."]),

    M("hs.sequences", 3,
      "What is the sum of the first 10 positive integers?",
      "55",
      [("50", "That is 10 × 5 using the wrong pairing."),
       ("45", "That is the sum of the first 9 integers."),
       ("100", "That is 10², not a sum of the numbers.")],
      ["Pair the ends: 1 + 10, 2 + 9, and so on.", "Each pair sums to 11, and there are 5 pairs."],
      ["5 pairs × 11 = 55.", "So 1 + 2 + … + 10 = 55."]),

    M("hs.sequences", 4,
      "What is the sum of the infinite series 1 + 1/2 + 1/4 + …?",
      "2",
      [("3/2", "That stops after two terms."),
       ("It grows without bound", "The ratio 1/2 is less than 1, so the series converges."),
       ("4", "That adds the first two terms and doubles.")],
      ["This is geometric with ratio 1/2.", "Sum = a / (1 − r)."],
      ["a = 1, r = 1/2.", "1 / (1 − 1/2) = 2."]),

    # ------------------------------------------------------------ hs.trig
    M("hs.trig", 1,
      "What is sin(30°)?",
      "1/2",
      [("√3/2", "That is cos(30°)."),
       ("√2/2", "That is sin(45°)."),
       ("1", "That is sin(90°).")],
      ["Use the 30-60-90 triangle: sides 1, √3, 2.", "sin is opposite over hypotenuse."],
      ["Opposite = 1, hypotenuse = 2.", "sin(30°) = 1/2."],
      visual=triangle_right("√3", "1", "2", "Thirty-sixty-ninety triangle with sides one, root three and two")),

    M("hs.trig", 2,
      "What is cos(0°)?",
      "1",
      [("0", "That is sin(0°)."),
       ("1/2", "That is cos(60°)."),
       ("−1", "That is cos(180°).")],
      ["At angle 0 the point on the unit circle is (1, 0).", "cos is the x-coordinate."],
      ["The x-coordinate at 0° is 1.", "So cos(0°) = 1."]),

    M("hs.trig", 2,
      "Complete the identity: sin²θ + cos²θ = ?",
      "1",
      [("0", "The two squares are both positive and add to 1."),
       ("2", "Each square is at most 1, and they share the total 1."),
       ("tan θ", "Tangent is sin/cos, a ratio, not a sum of squares.")],
      ["This comes from the unit circle: x² + y² = 1.", "cos θ is x and sin θ is y."],
      ["Dividing x² + y² = 1 on the circle gives sin²θ + cos²θ = 1."]),

    M("hs.trig", 3,
      "In a right triangle the side opposite θ is 3 and the hypotenuse is 5. What is sin θ?",
      "3/5",
      [("4/5", "That is cos θ, the adjacent side over the hypotenuse."),
       ("5/3", "That is the reciprocal, and it is greater than 1 — impossible for a sine."),
       ("3/4", "That is tan θ.")],
      ["sin = opposite / hypotenuse.", "The opposite side is given as 3."],
      ["sin θ = 3/5.", "The missing leg is 4, so cos θ = 4/5."],
      visual=triangle_right("4", "3", "5", "Right triangle with legs three and four and hypotenuse five")),

    M("hs.trig", 4,
      "What is tan(45°)?",
      "1",
      [("0", "That is tan(0°)."),
       ("√3", "That is tan(60°)."),
       ("1/2", "That is sin(30°), not a tangent.")],
      ["tan = sin / cos.", "At 45° the sine and cosine are equal."],
      ["sin(45°) = cos(45°) = √2/2.", "So tan(45°) = 1."]),

    # --------------------------------------------------------- hs.vectors
    M("hs.vectors", 1,
      "What is the length of the vector (3, 4)?",
      "5",
      [("7", "That adds the components instead of using Pythagoras."),
       ("12", "That multiplies the components."),
       ("25", "That is the squared length, before the square root.")],
      ["Length is √(x² + y²).", "9 + 16 = 25."],
      ["√25 = 5.", "So the vector has length 5."]),

    M("hs.vectors", 2,
      "What is (2, 3) + (4, −1)?",
      "(6, 2)",
      [("(6, 4)", "That adds the x's but keeps 3 + (−1) wrong."),
       ("(2, 2)", "That subtracts the x-components."),
       ("(8, −3)", "That multiplies the components instead of adding them.")],
      ["Add corresponding components.", "x: 2 + 4, y: 3 + (−1)."],
      ["(2 + 4, 3 − 1).", "So the sum is (6, 2)."]),

    M("hs.vectors", 2,
      "What is the dot product of (1, 2) and (3, 4)?",
      "11",
      [("10", "That drops the y-terms and uses 2 × 3 + 4."),
       ("7", "That adds all four numbers instead of multiplying pairs."),
       ("12", "That is 3 × 4, the product of the second components.")],
      ["Dot product multiplies matching components, then adds.", "1·3 + 2·4."],
      ["1×3 = 3 and 2×4 = 8.", "3 + 8 = 11."]),

    M("hs.vectors", 3,
      "What is (5, 0) · (0, −2)?",
      "0",
      [("10", "That multiplies 5 by 2 and ignores the signs."),
       ("−10", "That computes 5 × −2, but 0 × −2 = 0 for the first term."),
       ("−2", "That keeps only the second component.")],
      ["Multiply matching components first.", "5 × 0 = 0 and 0 × (−2) = 0."],
      ["0 + 0 = 0.", "Perpendicular vectors have dot product 0."]),

    M("hs.vectors", 4,
      "What is the unit vector in the direction of (0, −7)?",
      "(0, −1)",
      [("(0, 1)", "That points the opposite way."),
       ("(0, −7)", "That is the original vector, not a unit vector."),
       ("(−1, 0)", "That points along the x-axis, but the vector is vertical.")],
      ["A unit vector is the vector divided by its length.", "The length is 7."],
      ["(0, −7) ÷ 7 = (0, −1).", "It has length 1 and the same direction."]),
]

# --------------------------------------------------------------------------- #
# AP Calculus AB / BC
# --------------------------------------------------------------------------- #

_APC = [
    # ---------------------------------------------------------- apc.limits
    M("apc.limits", 1,
      "What is lim(x→2) (3x + 1)?",
      "7",
      [("6", "That is 3 × 2 without the +1."),
       ("5", "That is the limit at x = 4/3, not 2."),
       ("8", "That is 3 × 2 + 2.")],
      ["This is a polynomial, so substitute directly.", "3(2) + 1."],
      ["3 × 2 = 6.", "6 + 1 = 7."]),

    M("apc.limits", 2,
      "What is lim(x→0) sin(x)/x?",
      "1",
      [("0", "0/0 is indeterminate; the limit is not the direct substitution."),
       ("∞", "The ratio approaches 1 from both sides, so it does not blow up."),
       ("It does not exist", "The two one-sided limits both equal 1.")],
      ["This is a standard limit you should recognise.", "At small x, sin(x) ≈ x."],
      ["sin(x)/x → 1 as x → 0.", "So the limit is 1."]),

    M("apc.limits", 2,
      "What is lim(x→3) (x² − 9)/(x − 3)?",
      "6",
      [("0", "Direct substitution gives 0/0, which is indeterminate, not the answer."),
       ("3", "That is the value of x, not the limit."),
       ("It does not exist", "The factor cancels, leaving a perfectly good limit.")],
      ["Factor the numerator as a difference of squares.", "(x − 3)(x + 3)/(x − 3)."],
      ["Cancel (x − 3).", "The limit is 3 + 3 = 6."]),

    M("apc.limits", 3,
      "A function jumps from 2 to 5 at x = 1. What can you say about its limit at x = 1?",
      "The limit does not exist",
      [("The limit is 2", "That is only the left-hand limit."),
       ("The limit is 5", "That is only the right-hand limit."),
       ("The limit is 3.5", "A limit is not an average of the two sides.")],
      ["Compare the left-hand and right-hand limits.", "They must agree for the limit to exist."],
      ["The left limit is 2 and the right limit is 5.", "Since they differ, the limit does not exist."]),

    M("apc.limits", 4,
      "What is lim(x→∞) (2x² + 1)/(x² − 3)?",
      "2",
      [("0", "That is what happens when the denominator's degree is higher."),
       ("∞", "Both degrees are 2, so the ratio settles at a finite value."),
       ("1", "That compares the constants, not the leading coefficients.")],
      ["Compare the highest powers of x on top and bottom.", "Both are x², so compare coefficients: 2/1."],
      ["Divide top and bottom by x².", "The limit is 2/1 = 2."]),

    # ----------------------------------------------------------- apc.deriv
    M("apc.deriv", 1,
      "What is d/dx (x³)?",
      "3x²",
      [("x²", "That divides by 3 instead of multiplying by the exponent."),
       ("3x", "That differentiates x², not x³."),
       ("x⁴/4", "That is the antiderivative.")],
      ["Power rule: bring the exponent down, then subtract one.", "3x³⁻¹."],
      ["d/dx x³ = 3x²."]),

    M("apc.deriv", 2,
      "What is d/dx (sin x)?",
      "cos x",
      [("−cos x", "That is the derivative of −sin x."),
       ("−sin x", "That is the derivative of cos x."),
       ("tan x", "tan x is a ratio of sine and cosine, not its derivative.")],
      ["Sine and cosine are derivatives of each other with signs.", "d/dx sin x = cos x."],
      ["Starting from sin x, the derivative is cos x."]),

    M("apc.deriv", 2,
      "What is d/dx (5x + 2)?",
      "5",
      [("5x", "That keeps the variable; the derivative of a linear term is constant."),
       ("2", "That is the derivative of the constant term."),
       ("7", "That adds the coefficient and the constant.")],
      ["The derivative of a constant is 0.", "The derivative of 5x is 5."],
      ["5 + 0 = 5."]),

    M("apc.deriv", 3,
      "What is d/dx (x² eˣ)?",
      "eˣ(x² + 2x)",
      [("2x eˣ", "That differentiates only the x² and forgets the product rule."),
       ("x² eˣ", "That is the original function, undifferentiated."),
       ("eˣ(x² − 2x)", "That uses the quotient-rule sign in a product.")],
      ["Use the product rule: u′v + uv′.", "u = x², v = eˣ."],
      ["2x·eˣ + x²·eˣ.", "Factor out eˣ: eˣ(x² + 2x)."]),

    M("apc.deriv", 4,
      "What is d/dx ln(x²)?",
      "2/x",
      [("1/x²", "That differentiates as if the argument were linear."),
       ("2x", "That is the derivative of x², before dividing by x²."),
       ("2 ln x", "That is a rewrite of the function, not its derivative.")],
      ["Use the chain rule: 1/(inside) × derivative of the inside.", "The inside is x²."],
      ["(1/x²) · 2x = 2/x.", "Equivalently, ln(x²) = 2 ln x, whose derivative is 2/x."]),

    # ------------------------------------------------------------- apc.opt
    M("apc.opt", 1,
      "A critical point of f is a point where…",
      "f′(x) = 0 or f′ is undefined",
      [("f(x) = 0", "That is a root of the function, not a critical point."),
       ("f″(x) = 0", "That points at possible inflection points."),
       ("f is increasing", "Increasing is about the sign of f′, not where it is zero.")],
      ["Critical points come from the first derivative.", "Set f′ to zero or find where it fails to exist."],
      ["Solve f′(x) = 0, plus any point where f′ is undefined.", "Those are the critical points."]),

    M("apc.opt", 2,
      "Where is the minimum of f(x) = x² − 4x?",
      "x = 2",
      [("x = 4", "That is where f(x) = 0, not where f′ = 0."),
       ("x = −2", "That is a local maximum of x² + 4x."),
       ("x = 0", "That is a critical point only if the linear term were absent.")],
      ["Differentiate and set it to zero.", "f′(x) = 2x − 4."],
      ["2x − 4 = 0 gives x = 2.", "f″ = 2 > 0, so it is a minimum."]),

    M("apc.opt", 2,
      "A ball's height is h(t) = −5t² + 20t. When is it highest?",
      "t = 2",
      [("t = 1", "That is the midpoint of the path but not the vertex."),
       ("t = 4", "That is when it lands."),
       ("t = 0", "That is the launch, when the height is zero.")],
      ["Set the derivative to zero.", "h′(t) = −10t + 20."],
      ["−10t + 20 = 0 gives t = 2.", "h(2) = 20, the maximum height."]),

    M("apc.opt", 3,
      "A square's side grows at 2 cm/s. How fast is the area growing when the side is 5 cm?",
      "20 cm²/s",
      [("10 cm²/s", "That is 2 × 5 without the factor of 2 in A = s²."),
       ("25 cm²/s", "That multiplies the side by itself."),
       ("4 cm²/s", "That is the rate of the side doubled, not the rate of the area.")],
      ["A = s², so dA/dt = 2s · ds/dt.", "s = 5 and ds/dt = 2."],
      ["dA/dt = 2(5)(2).", "So the area grows at 20 cm²/s."]),

    M("apc.opt", 4,
      "For f(x) = x³ − 3x, which point is a local maximum?",
      "x = −1",
      [("x = 1", "That is the local minimum."),
       ("x = 0", "The derivative there is −3, not zero."),
       ("x = 3", "That is not a critical point.")],
      ["f′(x) = 3x² − 3 = 3(x − 1)(x + 1).", "Check the sign of f″ at each critical point."],
      ["Critical points x = ±1.", "f″(−1) = −6 < 0, so x = −1 is a maximum."]),

    # -------------------------------------------------------- apc.integrals
    M("apc.integrals", 1,
      "What is ∫ 2x dx?",
      "x² + C",
      [("2 + C", "That differentiates the constant and drops the x power."),
       ("x²/2 + C", "That divides by 2 instead of by the new exponent 2 after the power rule."),
       ("2x² + C", "That forgets to divide by the exponent.")],
      ["Power rule for integrals: add one to the exponent, then divide.", "∫x dx = x²/2."],
      ["∫2x dx = 2 · x²/2.", "That simplifies to x² + C."]),

    M("apc.integrals", 2,
      "What is ∫₀¹ x dx?",
      "1/2",
      [("1", "That is x² evaluated without dividing by 2."),
       ("0", "The integrand is positive on that interval, so the area cannot be 0."),
       ("2", "That is the antiderivative's value at 2.")],
      ["The antiderivative of x is x²/2.", "Evaluate from 0 to 1."],
      ["1/2 − 0.", "So the integral is 1/2."],
      visual=area_under("Shaded area under a curve between two vertical limits")),

    M("apc.integrals", 2,
      "What is ∫ cos x dx?",
      "sin x + C",
      [("−sin x + C", "That is the integral of −cos x."),
       ("cos x + C", "That is the function itself, not its antiderivative."),
       ("tan x + C", "That is not an antiderivative of cosine.")],
      ["Which function differentiates to cos x?", "sin x does."],
      ["d/dx sin x = cos x, so ∫cos x dx = sin x + C."]),

    M("apc.integrals", 3,
      "What is the area under y = 4 − x² from x = 0 to x = 2?",
      "16/3",
      [("8/3", "That is the integral from −2 to 0, a different region."),
       ("4", "That is the height at the left endpoint."),
       ("8", "That is ∫₀² 4 dx, ignoring the −x² term.")],
      ["Antiderivative: 4x − x³/3.", "Evaluate 4(2) − 8/3."],
      ["8 − 8/3 = 16/3.", "So the area is 16/3."]),

    M("apc.integrals", 4,
      "What is d/dx ∫₀ˣ t² dt?",
      "x²",
      [("2x", "That differentiates x² instead of substituting x."),
       ("x³/3", "That is the integral, not the derivative."),
       ("0", "The integral depends on x, so its derivative is not zero.")],
      ["Fundamental Theorem of Calculus, part 1.", "Replace t with x in the integrand."],
      ["d/dx ∫₀ˣ f(t) dt = f(x).", "So the answer is x²."]),

    # ----------------------------------------------------------- apc.series
    M("apc.series", 1,
      "The series 1 + 1/2 + 1/4 + … is…",
      "geometric with ratio 1/2",
      [("arithmetic with difference 1/2", "Arithmetic would add 1/2 each time, but the terms halve."),
       ("harmonic", "The harmonic series is 1 + 1/2 + 1/3 + …."),
       ("divergent", "Each step halves the remaining gap, so the total is finite.")],
      ["Look at the ratio between consecutive terms.", "(1/2) ÷ 1 = 1/2."],
      ["Each term is 1/2 of the one before.", "So the series is geometric with ratio 1/2."]),

    M("apc.series", 2,
      "Which series diverges?",
      "1 + 1/2 + 1/3 + 1/4 + …",
      [("1 + 1/2 + 1/4 + 1/8 + …", "That geometric series has ratio 1/2, so it converges."),
       ("1 + 1/4 + 1/9 + 1/16 + …", "That p-series has p = 2 > 1, so it converges."),
       ("1/2 + 1/4 + 1/8 + …", "Ratio 1/2 as well, so it converges to 1.")],
      ["Compare with a p-series: ∑ 1/nᵖ converges only for p > 1.", "The first option is p = 1."],
      ["The harmonic series is the p = 1 case.", "It diverges even though its terms go to zero."]),

    M("apc.series", 2,
      "What is the radius of convergence of ∑ xⁿ from n = 0 to ∞?",
      "1",
      [("0", "That would mean only x = 0 works, but the series also converges for small x."),
       ("∞", "The terms grow once |x| > 1, so it cannot converge everywhere."),
       ("2", "The ratio test gives |x| < 1, not 2.")],
      ["Apply the ratio test: |aₙ₊₁/aₙ| → |x|.", "Convergence needs |x| < 1."],
      ["|x| < 1 for convergence.", "So the radius of convergence is 1."]),

    M("apc.series", 3,
      "The Maclaurin series for eˣ begins…",
      "1 + x + x²/2 + x³/6",
      [("x + x²/2 + x³/6", "That forgets the constant term, since e⁰ = 1."),
       ("1 − x + x²/2 − x³/6", "Those alternating signs belong to e⁻ˣ."),
       ("1 + x²/2 + x⁴/24", "That skips the odd powers, which belong to cosh, not eˣ.")],
      ["Every derivative of eˣ at 0 is 1.", "Coefficients are 1/n!."],
      ["1 + x + x²/2! + x³/3! + …", "So the first terms are 1 + x + x²/2 + x³/6."]),

    M("apc.series", 4,
      "What does ∑ (1/2)ⁿ from n = 0 to ∞ equal?",
      "2",
      [("1", "That is the sum starting from n = 1."),
       ("1/2", "That is only the first term after n = 0."),
       ("It diverges", "The ratio 1/2 is less than 1, so the sum is finite.")],
      ["Geometric sum: a/(1 − r).", "a = 1 and r = 1/2."],
      ["1/(1 − 1/2) = 2."]),
]

# --------------------------------------------------------------------------- #
# AP Statistics
# --------------------------------------------------------------------------- #

_APS = [
    # ------------------------------------------------------- aps.describe
    M("aps.describe", 1,
      "The median of a data set is…",
      "the middle value once the data are ordered",
      [("the most common value", "That is the mode."),
       ("the average of all values", "That is the mean."),
       ("the largest minus the smallest", "That is the range.")],
      ["Order the values from smallest to largest.", "Find the value in the middle position."],
      ["Sort the data, then take the middle value.", "That value is the median."]),

    M("aps.describe", 2,
      "What is the mean of 2, 4, 4, 6, 9?",
      "5",
      [("4", "That is the median and the mode, not the mean."),
       ("5.5", "That divides 27 by 5 but adds an extra 4."),
       ("6", "That is the largest value.")],
      ["Add the values, then divide by how many there are.", "The sum is 25 and there are 5 values."],
      ["2 + 4 + 4 + 6 + 9 = 25.", "25 ÷ 5 = 5."],
      visual=bars([("2", 2), ("4", 4), ("4", 4), ("6", 6), ("9", 9)], "Bar chart of the values two, four, four, six and nine")),

    M("aps.describe", 2,
      "What is the median of 2, 4, 4, 6, 9?",
      "4",
      [("5", "That is the mean, not the median."),
       ("6", "That is the fourth value, not the middle one."),
       ("4.5", "That averages the two middle values of an even-sized set; this set has five values.")],
      ["There are five values, so the middle one is the third.", "Ordered: 2, 4, 4, 6, 9."],
      ["The third value is 4.", "So the median is 4."]),

    M("aps.describe", 3,
      "Adding a very large outlier to a data set changes the mean ___ the median.",
      "more than",
      [("less than", "The mean uses every value, so an outlier pulls it far more."),
       ("exactly as much as", "The median depends on position, so it barely moves."),
       ("not at all, unlike", "The mean always changes when a value is added.")],
      ["The mean depends on the size of every value.", "The median depends on the middle position."],
      ["A single huge value drags the mean a lot.", "The median shifts by at most one position, so the mean changes more."]),

    M("aps.describe", 4,
      "Standard deviation measures…",
      "the typical distance of values from the mean",
      [("the middle value of the data", "That is the median."),
       ("the largest minus the smallest value", "That is the range."),
       ("how often each value occurs", "That is the frequency distribution.")],
      ["It is built from squared deviations from the mean.", "It summarises spread, not centre."],
      ["Average squared deviation, then square root.", "So it measures typical distance from the mean."]),

    # ------------------------------------------------------------ aps.prob
    M("aps.prob", 1,
      "What is the probability of rolling a 3 on a fair six-sided die?",
      "1/6",
      [("1/3", "That includes two faces, but only one shows a 3."),
       ("1/2", "That is the chance of an even number."),
       ("2/3", "That is more likely than not, which no single face can be.")],
      ["There is one favourable face out of six equally likely faces.", "P = favourable / total."],
      ["1 favourable outcome, 6 total.", "So P = 1/6."]),

    M("aps.prob", 2,
      "Two fair coins are flipped. What is the probability of two heads?",
      "1/4",
      [("1/2", "That is the probability of a head on one coin."),
       ("1/3", "There are four equally likely outcomes, not three."),
       ("3/4", "That is the probability of at least one head.")],
      ["List the outcomes: HH, HT, TH, TT.", "Only one of them is two heads."],
      ["1 favourable outcome out of 4.", "So P = 1/4."]),

    M("aps.prob", 2,
      "P(A) = 0.4, P(B) = 0.3 and A and B are independent. What is P(A and B)?",
      "0.12",
      [("0.7", "That adds the probabilities, which would double count overlapping events."),
       ("0.1", "That subtracts the probabilities."),
       ("0.4", "That keeps only P(A).")],
      ["For independent events, multiply.", "0.4 × 0.3."],
      ["0.4 × 0.3 = 0.12.", "So P(A and B) = 0.12."]),

    M("aps.prob", 3,
      "If P(A) = 0.5 and P(A | B) = 0.5, what does that tell you?",
      "A and B are independent",
      [("A and B are mutually exclusive", "Mutually exclusive events would give P(A | B) = 0."),
       ("A and B always happen together", "That would make P(A | B) = 1."),
       ("B cannot happen", "P(A | B) is defined, so B can happen.")],
      ["Compare P(A | B) with P(A).", "Knowing B did not change A's probability."],
      ["P(A | B) = P(A) = 0.5.", "That is the definition of independence."]),

    M("aps.prob", 4,
      "Two cards are drawn without replacement from a standard deck. What is P(both kings)?",
      "(4/52) × (3/51)",
      [("(4/52)²", "That assumes replacement, but the first king is not put back."),
       ("4/52", "That is the chance of one king on the first draw."),
       ("(4/52) × (4/51)", "After one king is gone only 3 remain.")],
      ["After drawing a king there are 3 kings left in 51 cards.", "Multiply the two probabilities."],
      ["First draw: 4/52.", "Second draw: 3/51, so the product is (4/52)(3/51)."]),
]

QUESTIONS = _ME + _HS + _APC + _APS
