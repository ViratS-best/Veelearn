"""Fourth Grade Math units 5–8: decimals, geometry, angles, protractor lab, plus master page."""

import math

from curriculum_kit import (
    lesson_figure, svg_dots, svg_number_line, svg_rect, svg_fraction_bar,
    svg_tape, svg_circle, svg_triangle, svg_plane, svg_percent_bar,
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
    protractor_box,
    page_break,
    mq,
    renumber,
)


def _hundredths_grid(n, color="#a78bfa"):
    n = max(0, min(int(n), 100))
    cells = []
    for i in range(100):
        r, c = divmod(i, 10)
        fill = color if i < n else "#f8fafc"
        cells.append(
            f'<rect x="{8 + c * 16}" y="{8 + r * 16}" width="16" height="16" fill="{fill}" stroke="#0f172a"/>'
        )
    return f'<svg viewBox="0 0 176 176" width="100%" style="max-width:200px" role="img">{"".join(cells)}</svg>'


def _angle_svg(deg, label=None, color="#6366f1"):
    cx, cy, r = 100, 118, 86
    rad = math.radians(deg)
    x2 = cx + r * math.cos(rad)
    y2 = cy - r * math.sin(rad)
    sweep = 0
    large = 1 if deg > 180 else 0
    xe = cx + 32 * math.cos(rad)
    ye = cy - 32 * math.sin(rad)
    lab = label or f"{deg}°"
    lx = cx + 48 * math.cos(math.radians(deg / 2))
    ly = cy - 48 * math.sin(math.radians(deg / 2))
    return f'''<svg viewBox="0 0 220 150" width="100%" style="max-width:240px" role="img">
  <line x1="{cx - 80}" y1="{cy}" x2="{cx + r}" y2="{cy}" stroke="#94a3b8" stroke-width="2"/>
  <line x1="{cx}" y1="{cy}" x2="{cx + r}" y2="{cy}" stroke="#0f172a" stroke-width="3"/>
  <line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#0f172a" stroke-width="3"/>
  <path d="M {cx + 32} {cy} A 32 32 0 {large} {sweep} {xe:.1f} {ye:.1f}" fill="{color}" fill-opacity="0.25" stroke="{color}" stroke-width="2"/>
  <circle cx="{cx}" cy="{cy}" r="4" fill="#0f172a"/>
  <text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-size="14" font-weight="700" fill="#312e81">{lab}</text>
</svg>'''


def _adjacent_angles(d1, d2, lab1=None, lab2=None):
    cx, cy, r = 110, 122, 90
    t1 = math.radians(d1)
    t2 = math.radians(d1 + d2)
    x1, y1 = cx + r * math.cos(t1), cy - r * math.sin(t1)
    x2, y2 = cx + r * math.cos(t2), cy - r * math.sin(t2)
    p1 = (cx + 28 * math.cos(t1), cy - 28 * math.sin(t1))
    p2 = (cx + 28 * math.cos(t2), cy - 28 * math.sin(t2))
    m1 = math.radians(d1 / 2)
    m2 = math.radians(d1 + d2 / 2)
    return f'''<svg viewBox="0 0 240 160" width="100%" style="max-width:260px" role="img">
  <line x1="{cx}" y1="{cy}" x2="{cx + r}" y2="{cy}" stroke="#0f172a" stroke-width="3"/>
  <line x1="{cx}" y1="{cy}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#0f172a" stroke-width="3"/>
  <line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#0f172a" stroke-width="3"/>
  <path d="M {cx} {cy} L {cx + 28} {cy} A 28 28 0 0 0 {p1[0]:.1f} {p1[1]:.1f} Z" fill="#93c5fd" fill-opacity="0.8" stroke="#1d4ed8"/>
  <path d="M {cx} {cy} L {p1[0]:.1f} {p1[1]:.1f} A 28 28 0 0 0 {p2[0]:.1f} {p2[1]:.1f} Z" fill="#fde68a" fill-opacity="0.8" stroke="#b45309"/>
  <circle cx="{cx}" cy="{cy}" r="4" fill="#0f172a"/>
  <text x="{cx + 50 * math.cos(m1):.1f}" y="{cy - 50 * math.sin(m1):.1f}" text-anchor="middle" font-size="13" font-weight="700">{lab1 or str(d1) + "°"}</text>
  <text x="{cx + 50 * math.cos(m2):.1f}" y="{cy - 50 * math.sin(m2):.1f}" text-anchor="middle" font-size="13" font-weight="700">{lab2 or str(d2) + "°"}</text>
</svg>'''


def _line_figures():
    return '''<svg viewBox="0 0 460 150" width="100%" style="max-width:460px" role="img">
  <circle cx="36" cy="28" r="5" fill="#dc2626"/>
  <text x="50" y="32" font-size="12">point A</text>
  <line x1="180" y1="28" x2="430" y2="28" stroke="#0f172a" stroke-width="2"/>
  <polygon points="180,28 190,24 190,32" fill="#0f172a"/>
  <polygon points="430,28 420,24 420,32" fill="#0f172a"/>
  <text x="280" y="18" font-size="12">line AB</text>
  <circle cx="36" cy="78" r="4" fill="#0f172a"/>
  <circle cx="150" cy="78" r="4" fill="#0f172a"/>
  <line x1="36" y1="78" x2="150" y2="78" stroke="#0f172a" stroke-width="3"/>
  <text x="160" y="82" font-size="12">segment CD (2 endpoints)</text>
  <circle cx="36" cy="124" r="4" fill="#0f172a"/>
  <line x1="36" y1="124" x2="200" y2="124" stroke="#0f172a" stroke-width="3"/>
  <polygon points="200,124 190,120 190,128" fill="#0f172a"/>
  <text x="210" y="128" font-size="12">ray EF (1 endpoint)</text>
</svg>'''


def _para_perp():
    return '''<svg viewBox="0 0 440 150" width="100%" style="max-width:440px" role="img">
  <line x1="20" y1="40" x2="200" y2="40" stroke="#1d4ed8" stroke-width="3"/>
  <line x1="20" y1="80" x2="200" y2="80" stroke="#1d4ed8" stroke-width="3"/>
  <polygon points="90,40 96,36 96,44" fill="#1d4ed8"/>
  <polygon points="90,80 96,76 96,84" fill="#1d4ed8"/>
  <text x="70" y="128" font-size="12">parallel — never meet</text>
  <line x1="260" y1="120" x2="400" y2="120" stroke="#0f172a" stroke-width="3"/>
  <line x1="330" y1="30" x2="330" y2="120" stroke="#0f172a" stroke-width="3"/>
  <rect x="330" y="104" width="16" height="16" fill="none" stroke="#b91c1c" stroke-width="2"/>
  <text x="268" y="24" font-size="12">perpendicular — 90°</text>
</svg>'''


def _fill(qs, need, factory):
    while len(qs) < need:
        qs.append(factory(len(qs) + 1))
    return renumber(qs[:need])


# ===========================================================================
# UNIT 5: Decimals — tenths and hundredths
# ===========================================================================

def _u5_questions():
    qs = []
    idx = 1

    tenths = [
        ("3/10 as a decimal is…", "0.3", ["3.0", "0.03", "3.10"], "3 tenths = 0.3."),
        ("0.7 as a fraction is…", "7/10", ["7/100", "70/10", "1/7"], "Seven tenths."),
        ("1/10 as a decimal is…", "0.1", ["1.0", "0.01", "10.1"], "One tenth."),
        ("0.9 = how many tenths?", 9, ["0.9", "90", "1"], "0.9 is 9 tenths."),
        ("10/10 as a decimal is…", "1.0", ["0.10", "0.1", "10.0"], "Ten tenths is 1 whole."),
        ("4 tenths + 3 tenths = ?", "0.7", ["0.43", "7.0", "0.07"], "0.4+0.3=0.7."),
        ("Which is greater: 0.4 or 0.39?", "0.4", ["0.39", "same", "0.04"], "0.4 = 0.40, and 40 hundredths > 39 hundredths."),
        ("0.5 of a whole is the same as…", "1/2", ["1/5", "5/10 only as 5", "0.05"], "5/10 = 1/2 = 0.5."),
    ]
    for text, ans, dist, expl in tenths:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    hundredths = [
        ("25/100 as a decimal is…", "0.25", ["2.5", "0.025", "25.0"], "25 hundredths = 0.25."),
        ("0.07 as a fraction is…", "7/100", ["7/10", "70/100", "0.7"], "7 hundredths."),
        ("1/100 as a decimal is…", "0.01", ["0.1", "1.00", "0.001"], "One hundredth."),
        ("0.40 is how many hundredths?", 40, ["4", "400", "0.4"], "40 hundredths. Also 4 tenths."),
        ("0.4 = 0.40 because they are…", "equal", ["0.4 greater", "0.40 greater", "unrelated"], "4 tenths = 40 hundredths."),
        ("3/100 + 2/100 = ?", "0.05", ["0.32", "5.00", "0.5"], "5 hundredths."),
        ("Which is greater: 0.2 or 0.05?", "0.2", ["0.05", "same", "0.02"], "0.20 vs 0.05. 20 hundredths > 5."),
        ("0.25 of a whole is the same as…", "1/4", ["1/25", "25/10", "2/5"], "25/100 = 1/4."),
    ]
    for text, ans, dist, expl in hundredths:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    money = [
        ("$0.35 is 35…", "cents", ["dollars", "tenths only", "mills"], "A cent is a hundredth of a dollar."),
        ("3 dimes as a decimal dollar amount?", "0.30", ["0.03", "3.00", "0.3 dimes"], "30 cents = $0.30 = 3 tenths of a dollar."),
        ("$1.00 is how many hundredths of a dollar?", 100, ["10", "1", "1000"], "100 cents."),
        ("$0.07 + $0.05 = ?", "0.12", ["0.12 dollars as 12 cents", "0.57", "1.2"], "7+5=12 cents = $0.12."),
        ("Which is more money: $0.40 or $0.08?", "0.40", ["0.08", "same", "0.04"], "40 cents > 8 cents."),
        ("A nickel is $0.05, which is 5/100 of a dollar. True?", "true", ["false", "a dime", "a dollar"], "5 hundredths."),
    ]
    for text, ans, dist, expl in money:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    compare = [
        ("Order from least to greatest: 0.3, 0.03, 0.30. Which is least?", "0.03", ["0.3", "0.30", "they equal"], "3 hundredths is least."),
        ("0.3 compared with 0.30 is…", "equal", ["0.3 greater", "0.30 greater", "cannot say"], "A trailing zero in hundredths does not change tenths."),
        ("0.8 compared with 0.79 is…", "0.8 greater", ["0.79 greater", "equal", "0.08 greater"], "0.80 > 0.79."),
        ("0.09 compared with 0.1 is…", "0.1 greater", ["0.09 greater", "equal", "0.90 greater"], "0.10 > 0.09."),
        ("Write 0.6 as hundredths.", "0.60", ["0.06", "6.00", "0.006"], "6 tenths = 60 hundredths."),
        ("Write 40 hundredths as tenths.", "0.4", ["0.04", "4.0", "0.040"], "40/100 = 4/10 = 0.4."),
        ("Which decimal is 6/10?", "0.6", ["0.06", "6.10", "0.16"], "Six tenths."),
        ("Which decimal is 6/100?", "0.06", ["0.6", "6.00", "0.60"], "Six hundredths."),
    ]
    for text, ans, dist, expl in compare:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    add = [
        ("0.2 + 0.3 = ?", "0.5", ["0.23", "5.0", "0.05"], "2 tenths + 3 tenths = 5 tenths."),
        ("0.25 + 0.10 = ?", "0.35", ["0.2510", "0.26", "2.5"], "25+10=35 hundredths."),
        ("0.4 + 0.4 = ?", "0.8", ["0.44", "0.08", "8.0"], "8 tenths."),
        ("1.0 − 0.3 = ?", "0.7", ["0.7 tenths as 0.07", "1.3", "0.4"], "10 tenths minus 3 tenths."),
        ("0.50 − 0.05 = ?", "0.45", ["0.55", "0.45 tenths", "5.0"], "50−5=45 hundredths."),
        ("0.09 + 0.01 = ?", "0.10", ["0.010", "0.9", "0.19"], "10 hundredths = 1 tenth."),
    ]
    for text, ans, dist, expl in add:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"{1 + (i % 9)}/10 as a decimal is…",
        f"0.{1 + (i % 9)}",
        f"{1 + (i % 9)} tenths is 0.{1 + (i % 9)}.",
        i,
        distractors=[f"0.0{1 + (i % 9)}", f"{1 + (i % 9)}.0", f"0.{1 + (i % 9)}0 extra"],
    ))


def build_unit5():
    title = "Fourth Grade Math Unit 5: Decimals — Tenths and Hundredths"
    description = (
        "Read tenths and hundredths, connect them to fractions and money, compare decimals, and add or subtract like decimal places."
    )

    c1 = concept_block(
        "1. Tenths",
        [
            "A tenth is 1/10 of a whole. As a decimal we write 0.1.",
            "The first place to the right of the decimal point is tenths.",
            "0.3 is 3/10. 0.7 is 7/10. 1.0 is 10/10, a whole.",
            "A number line from 0 to 1 split into 10 equal parts shows tenths.",
            "0.5 is 5/10, which equals 1/2.",
            "Say 'three tenths,' not 'point three' only — the word tenths keeps the place honest.",
        ],
        lesson_figure(
            svg_fraction_bar(3, 10, "#38bdf8")
            + svg_number_line(0, 10, marks=[(3, "0.3")]),
            "3/10 is 0.3",
            "The bar is one whole split into 10 tenths, with 3 shaded. On the number line each tick is one tenth, so 3 marks 0.3.",
        )
        + solved(1, "Write 3/10 as a decimal.",
               ["3 tenths.",
                "The tenths place is the first digit after the point.",
                "0.3."],
               "0.3")
        + matching(
            [("1/10", "0.1"), ("7/10", "0.7"), ("10/10", "1.0"), ("5/10", "0.5")],
            vid="g4u5-c1-match",
        ),
        kid_tip("Point then place", "The decimal point is the fence. First house on the right is tenths."),
        1,
    )

    c2 = concept_block(
        "2. Hundredths",
        [
            "A hundredth is 1/100 of a whole. As a decimal: 0.01.",
            "The second place to the right is hundredths.",
            "0.25 is 25/100. 0.07 is 7/100 — the 0 in tenths holds that place.",
            "100 hundredths make 1 whole. 10 hundredths make 1 tenth.",
            "0.25 equals 1/4. 0.50 equals 1/2.",
            "Money uses hundredths: 1 cent is $0.01.",
        ],
        lesson_figure(
            _hundredths_grid(7),
            "7/100 is 0.07",
            "A 10-by-10 grid is 100 hundredths. Seven squares shaded is 0.07 — the 0 holds the tenths place.",
        )
        + solved(1, "Write 7/100 as a decimal.",
               ["7 hundredths.",
                "Tenths place is 0. Hundredths place is 7.",
                "0.07."],
               "0.07")
        + solved(2, "Write 0.40 as hundredths.",
                 ["40 hundredths.",
                  "Also 4 tenths. Same amount."],
                 "40 hundredths")
        + phet_box("area_dec"),
        watch_out("Reading 0.07 as 7 tenths",
                  "0.07 is seven hundredths. 0.7 is seven tenths. That extra zero changes the place."),
        6,
    )

    c3 = concept_block(
        "3. Tenths and hundredths together",
        [
            "4 tenths = 40 hundredths. So 0.4 = 0.40.",
            "You can write extra zeros on the right in the hundredths place without changing the value: 0.3 = 0.30.",
            "You cannot move a digit. 0.3 is not 0.03.",
            "A grid of 100 squares: shade 40 squares for 0.40, which is also 4 columns of 10 for 0.4.",
            "Expanded: 0.25 = 2 tenths + 5 hundredths = 0.2 + 0.05.",
            "This is place value again, just on the other side of the point.",
        ],
        lesson_figure(
            svg_fraction_bar(4, 10, "#38bdf8") + _hundredths_grid(40, "#a78bfa"),
            "0.4 = 0.40",
            "4 tenths on the bar is the same amount as 40 hundredths on the grid. Extra zeros on the right do not change the value.",
        )
        + solved(1, "Are 0.4 and 0.40 equal?",
               ["0.4 = 4/10 = 40/100 = 0.40.",
                "Yes. Equal."],
               "yes")
        + step_reveal(
            ["Write both decimals with two places.",
             "0.4 becomes 0.40.",
             "Compare hundredths.",
             "If the digits match, the amounts match."],
            vid="g4u5-c3-steps",
        ),
        try_this("Money check", "40 cents is $0.40. 4 dimes is also $0.40. Same money, two writings."),
        11,
    )

    c4 = concept_block(
        "4. Compare decimals",
        [
            "Line up the decimal points. Compare tenths first, then hundredths.",
            "0.8 vs 0.79: tenths 8 vs 7. 0.8 is greater (0.80 > 0.79).",
            "0.09 vs 0.1: write 0.10. 10 hundredths > 9 hundredths. 0.1 is greater.",
            "0.3 vs 0.30 are equal.",
            "A number line from 0 to 1 makes comparison visual: farther right is greater.",
            "Do not think 'longer decimal means bigger.' 0.09 has more digits than 0.1 but is smaller.",
        ],
        lesson_figure(
            svg_number_line(0, 10, marks=[(2, "0.2"), (0.5, "0.05")]),
            "0.2 versus 0.05",
            "Each tick is one tenth. 0.2 sits at 2 tenths. 0.05 sits at half a tenth. Farther right is greater, so 0.2 > 0.05.",
        )
        + solved(1, "Which is greater, 0.2 or 0.05?",
               ["Write 0.20 and 0.05.",
                "20 hundredths > 5 hundredths.",
                "0.2."],
               "0.2")
        + matching(
            [("0.4 vs 0.40", "equal"), ("0.8 vs 0.79", "0.8 greater"),
             ("0.09 vs 0.1", "0.1 greater"), ("0.03 vs 0.3", "0.3 greater")],
            vid="g4u5-c4-match",
        ),
        kid_tip("Equal length first", "Give both decimals the same number of places, then compare digits from the left."),
        16,
    )

    c5 = concept_block(
        "5. Add and subtract tenths or hundredths",
        [
            "Add like places. 0.2 + 0.3 = 0.5. 0.25 + 0.10 = 0.35.",
            "Line up the points. Tenths under tenths. Hundredths under hundredths.",
            "10 hundredths make 1 tenth, so 0.09 + 0.01 = 0.10.",
            "1.0 − 0.3 = 0.7 because 10 tenths minus 3 tenths.",
            "0.50 − 0.05 = 0.45.",
            "This matches adding 2/10 + 3/10 or 25/100 + 10/100.",
        ],
        lesson_figure(
            _hundredths_grid(25, "#93c5fd") + _hundredths_grid(35, "#86efac"),
            "0.25 + 0.10 = 0.35",
            "25 hundredths plus 10 hundredths is 35 hundredths. Line up the decimal points so hundredths sit under hundredths.",
        )
        + solved(1, "0.25 + 0.10 = ?",
               ["25 hundredths + 10 hundredths = 35 hundredths.",
                "0.35."],
               "0.35")
        + solved(2, "1.0 − 0.3 = ?",
                 ["10 tenths − 3 tenths = 7 tenths.",
                  "0.7."],
                 "0.7")
        + watch_out("Lining up from the left instead of the point",
                    "0.25 + 0.3 is 0.55, not 0.28. Line up the decimal points."),
        21,
    )

    c6 = concept_block(
        "6. Decimals in money and measurement",
        [
            "A dollar is the whole. Cents are hundredths. $0.35 is 35/100 of a dollar.",
            "A dime is $0.10, one tenth. A nickel is $0.05, five hundredths.",
            "Meters and centimeters show up in later grades. Money is the everyday model now.",
            "Adding money is adding hundredths: $0.07 + $0.05 = $0.12.",
            "Comparing prices is comparing decimals.",
            "Write the dollar sign and the point: $0.40, not 40 alone, when the unit is dollars.",
        ],
        lesson_figure(
            svg_tape([1, 1, 1], labels=["dime", "dime", "dime"])
            + svg_number_line(0, 10, marks=[(3, "$0.30")]),
            "3 dimes = $0.30",
            "Each dime is one tenth of a dollar. Three dimes are 30 cents, written $0.30 — 3 tenths of a dollar.",
        )
        + solved(1, "3 dimes as a decimal dollar amount?",
               ["3 dimes = 30 cents.",
                "$0.30."],
               "0.30")
        + phet_box("area_dec"),
        try_this("Say cents, then dollars", "35 cents is $0.35. The words keep tenths and hundredths from swapping."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Read and write tenths",
            "Read and write hundredths",
            "Rename tenths as hundredths",
            "Compare decimals",
            "Add and subtract like decimal places",
            "Use money as hundredths of a dollar",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u5_questions()


# ===========================================================================
# UNIT 6: Geometry — points, lines, rays
# ===========================================================================

def _u6_questions():
    qs = []
    idx = 1

    names = [
        ("A point names a…", "location", ["length", "angle", "area"], "A point has position, not size."),
        ("A line goes on forever in how many directions?", 2, ["1", "0", "360"], "Both ways. Arrowheads on both ends."),
        ("A line segment has how many endpoints?", 2, ["1", "0", "3"], "It starts and stops."),
        ("A ray has how many endpoints?", 1, ["2", "0", "3"], "It starts at a point and goes on forever the other way."),
        ("Two rays that share an endpoint form an…", "angle", ["line always", "segment", "area"], "The shared point is the vertex."),
        ("An angle's vertex is the…", "shared endpoint", ["longest ray", "number of degrees only", "area"], "Vertex = corner point."),
        ("A straight line measures how many degrees?", 180, ["90", "360", "45"], "A straight angle is 180°."),
        ("A right angle measures how many degrees?", 90, ["45", "180", "60"], "Square corner. 90°."),
    ]
    for text, ans, dist, expl in names:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    # The loop above is messy - names already has dist as third. Let me just use names directly - I already did a weird unpack. It should work: text, ans, dist, expl.

    rel = [
        ("Two lines that never meet and stay the same distance are…", "parallel", ["perpendicular", "intersecting", "rays"], "Parallel lines do not cross."),
        ("Two lines that meet at a right angle are…", "perpendicular", ["parallel", "curved", "skew in this plane"], "They form 90°."),
        ("Two lines that cross at any angle are…", "intersecting", ["always parallel", "always perpendicular", "points"], "They share a point."),
        ("The symbol ⊥ means…", "perpendicular", ["parallel", "equal length", "greater"], "A little square at the meeting point also marks a right angle."),
        ("The symbol ∥ means…", "parallel", ["perpendicular", "intersect", "degree"], "Two marks on the lines can show they are parallel."),
        ("A rectangle's opposite sides are…", "parallel", ["perpendicular only", "curved", "rays"], "They also meet the adjacent sides at right angles."),
        ("The hands of a clock at 3:00 form a…", "right angle", ["straight angle", "acute always", "circle"], "Hour at 3, minute at 12. 90°."),
        ("A plus sign + is a model of…", "perpendicular lines", ["parallel lines", "a ray only", "a segment only"], "The two bars meet at 90°."),
    ]
    for text, ans, dist, expl in rel:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    angles = [
        ("An angle smaller than 90° is…", "acute", ["obtuse", "right", "straight"], "Acute = sharp, less than a square corner."),
        ("An angle greater than 90° and less than 180° is…", "obtuse", ["acute", "right", "straight"], "Obtuse is wider than a square corner but not a straight line."),
        ("A 90° angle is…", "right", ["acute", "obtuse", "straight"], "Right angle."),
        ("A 180° angle is…", "straight", ["right", "acute", "obtuse"], "A straight line."),
        ("45° is…", "acute", ["obtuse", "right", "straight"], "45 < 90."),
        ("120° is…", "obtuse", ["acute", "right", "straight"], "90 < 120 < 180."),
        ("90° is…", "right", ["acute", "obtuse", "straight"], "Exactly 90."),
        ("179° is…", "obtuse", ["straight", "acute", "right"], "Still less than 180."),
        ("1° is…", "acute", ["obtuse", "right", "straight"], "Tiny but still an angle."),
        ("A square has how many right angles?", 4, "Four square corners."),
    ]
    for item in angles:
        if len(item) == 4:
            qs.append(mq(item[0], item[1], item[3], idx, distractors=item[2]))
        else:
            qs.append(mq(item[0], item[1], item[2], idx))
        idx += 1

    more = [
        ("How many degrees in a full turn around a point?", 360, "A full circle is 360°."),
        ("Two right angles make a…", "straight angle", ["acute angle", "full turn", "ray"], "90+90=180."),
        ("Half of a straight angle is…", 90, "180÷2=90."),
        ("A triangle can have at most how many right angles in grade-4 drawings?", 1, "A right triangle has one right angle."),
        ("Points A, B, C with vertex B. The angle is named…", "angle ABC", ["segment AC only", "line AC", "ray BA only"], "The vertex letter sits in the middle."),
        ("A ray named ray AB starts at…", "A", ["B", "the midpoint", "infinity"], "The first letter is the endpoint."),
        ("Parallel lines in a plane have how many intersection points?", 0, "They never meet."),
        ("Perpendicular lines intersect in how many points?", 1, "They cross once, at 90°."),
    ]
    for item in more:
        if len(item) == 4:
            qs.append(mq(item[0], item[1], item[3], idx, distractors=item[2]))
        else:
            qs.append(mq(item[0], item[1], item[2], idx))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"Is {20 + (i % 50)}° acute, right, or obtuse?" if (20 + (i % 50)) != 90 else "Is 90° acute, right, or obtuse?",
        "right" if (20 + (i % 50)) == 90 else ("acute" if (20 + (i % 50)) < 90 else "obtuse"),
        "Acute < 90, right = 90, obtuse between 90 and 180.",
        i,
        distractors=["acute", "right", "obtuse"] if False else (
            ["right", "obtuse", "straight"] if (20 + (i % 50)) < 90 else (
                ["acute", "right", "straight"] if (20 + (i % 50)) > 90 else ["acute", "obtuse", "straight"]
            )
        ),
    ))


def build_unit6():
    title = "Fourth Grade Math Unit 6: Points, Lines, and Angle Types"
    description = (
        "Name points, lines, segments, and rays. Identify parallel and perpendicular lines. Classify acute, right, obtuse, and straight angles."
    )

    c1 = concept_block(
        "1. Points, lines, segments, rays",
        [
            "A point is a location. We name it with a capital letter: point A.",
            "A line goes forever in two directions. Draw arrows on both ends.",
            "A line segment has two endpoints. It is a piece of a line. Segment AB.",
            "A ray has one endpoint and goes forever the other way. Ray AB starts at A and passes through B.",
            "Two rays with the same endpoint make an angle. That shared point is the vertex.",
            "Draw neatly. The picture is the definition you will measure later.",
        ],
        lesson_figure(
            _line_figures(),
            "Point, line, segment, ray",
            "A point is a location. A line has two arrows. A segment has two endpoints. A ray has one endpoint and one arrow.",
        )
        + solved(1, "How many endpoints does a ray have?",
               ["It starts at one point.",
                "The other side never stops.",
                "1 endpoint."],
               "1")
        + matching(
            [("point", "a location"), ("line", "two arrows"),
             ("segment", "two endpoints"), ("ray", "one endpoint")],
            vid="g4u6-c1-match",
        ),
        kid_tip("Name from the start", "Ray AB starts at A. Angle ABC has vertex B in the middle."),
        1,
    )

    c2 = concept_block(
        "2. Parallel and perpendicular",
        [
            "Parallel lines never meet. They stay the same distance apart, like railroad rails.",
            "We mark parallel with arrows on the lines, or write AB ∥ CD.",
            "Perpendicular lines meet at a right angle, 90°. A tiny square at the corner shows it. Symbol: ⊥.",
            "Intersecting lines meet at a point. They might or might not be perpendicular.",
            "A rectangle has opposite sides parallel and adjacent sides perpendicular.",
            "A plus sign is a picture of perpendicular lines.",
        ],
        lesson_figure(
            _para_perp(),
            "Parallel versus perpendicular",
            "Parallel lines never meet. Perpendicular lines meet at a square corner (90°). A tiny square marks that right angle.",
        )
        + solved(1, "Two lines meet at a square corner. What are they?",
               ["A square corner is 90°.",
                "The lines are perpendicular."],
               "perpendicular")
        + matching(
            [("never meet", "parallel"), ("meet at 90°", "perpendicular"),
             ("meet at a point", "intersecting"), ("clock at 3:00", "right angle")],
            vid="g4u6-c2-match",
        ),
        try_this("Book edge test", "A book corner is 90°. Hold it on two lines. If it fits, they are perpendicular."),
        6,
    )

    c3 = concept_block(
        "3. What is an angle?",
        [
            "An angle is two rays that share an endpoint (the vertex).",
            "We measure angles in degrees. A tiny turn is 1°. A full spin around a point is 360°.",
            "A square corner is 90°. A straight line is 180°. Two 90° angles make a straight line.",
            "The size of an angle is the amount of turn, not how long the rays are drawn.",
            "Name an angle with three letters, vertex in the middle: ∠ABC.",
            "Longer rays do not make a bigger angle. Only the opening matters.",
        ],
        lesson_figure(
            _angle_svg(90, "90°"),
            "A right angle is a square corner",
            "Two rays share a vertex. The opening is the turn, not how long you draw the rays. A square corner measures 90°.",
        )
        + solved(1, "How many degrees is a right angle?",
               ["A square corner.",
                "90°."],
               "90")
        + watch_out("Thinking long rays mean a big angle",
                    "You can draw tiny rays on a 120° angle and long rays on a 20° angle. Measure the opening."),
        11,
    )

    c4 = concept_block(
        "4. Acute, right, obtuse, straight",
        [
            "Acute: less than 90°. Sharp, like a slice of pizza that is skinny.",
            "Right: exactly 90°. Square corner.",
            "Obtuse: more than 90° and less than 180°. Wider than a square corner.",
            "Straight: exactly 180°. A straight line.",
            "Compare to a book corner. Smaller → acute. Fits → right. Bigger but not a line → obtuse.",
            "45° acute. 90° right. 120° obtuse. 180° straight.",
        ],
        lesson_figure(
            _angle_svg(45, "45° acute", "#22c55e")
            + _angle_svg(90, "90° right")
            + _angle_svg(120, "120° obtuse", "#f59e0b"),
            "Compare each opening to a square corner",
            "45° is smaller than 90° (acute). 90° fits a book corner (right). 120° is wider than 90° but not a line (obtuse).",
        )
        + solved(1, "Is 120° acute, right, or obtuse?",
               ["120 is more than 90 and less than 180.",
                "Obtuse."],
               "obtuse")
        + matching(
            [("45°", "acute"), ("90°", "right"), ("120°", "obtuse"), ("180°", "straight")],
            vid="g4u6-c4-match",
        ),
        kid_tip("Book corner", "Hold a book on the angle. Smaller than the book is acute. Fits is right. Bigger is obtuse."),
        16,
    )

    c5 = concept_block(
        "5. Benchmark angles",
        [
            "Memorize the landmarks: 0° (no opening), 90°, 180°, 360° (full turn).",
            "45° is half of a right angle. 135° is a right angle plus 45°.",
            "Clock: 12 to 3 is 90°. 12 to 6 is 180°. Each hour mark is 30° (360÷12).",
            "These landmarks help you estimate before you pick up a protractor.",
            "If an angle looks a little less than a square corner, it might be 80°, not 20°.",
            "Estimate first. Then measure in the next units.",
        ],
        lesson_figure(
            _adjacent_angles(90, 90, "90°", "90°") + svg_circle(r=1, show_r=False),
            "Landmarks: 90°, 180°, 360°",
            "Two right angles make a straight 180° line. A full spin around a point is 360°. Half of 180° is 90°.",
        )
        + solved(1, "Half of a straight angle is how many degrees?",
               ["Straight is 180°.",
                "Half is 90°."],
               "90")
        + step_reveal(
            ["Find a nearby landmark: 90 or 180.",
             "Ask: smaller, equal, or larger?",
             "Name the type.",
             "Guess a number nearby, then measure later."],
            vid="g4u6-c5-steps",
        ),
        try_this("Body angles", "Arms straight out is about 180°. One arm up, one out is about 90°."),
        21,
    )

    c6 = concept_block(
        "6. Draw and name",
        [
            "To draw ray AB, put a point A, a point B, connect them, and add one arrow past B.",
            "To draw ∠ABC, draw ray BA and ray BC from B.",
            "Mark a right angle with a small square. Mark parallel with arrows.",
            "Keep letters outside the picture so they stay readable.",
            "A triangle is three segments. It has three angles. We classify those angles too.",
            "Neat drawings make measuring with a protractor much easier.",
        ],
        lesson_figure(
            _angle_svg(60, "∠ABC") + svg_triangle(3, 4, 5, right=True),
            "Name the vertex in the middle",
            "Angle ABC has vertex B — the middle letter. A triangle is three segments and three angles. The square marks a right angle.",
        )
        + solved(1, "Angle ABC has vertex…",
               ["The middle letter is the vertex.",
                "Vertex B."],
               "B")
        + matching(
            [("ray AB starts at", "A"), ("∠ABC vertex", "B"),
             ("right-angle mark", "small square"), ("parallel mark", "arrows")],
            vid="g4u6-c6-match",
        ),
        kid_tip("Vertex in the middle", "The name ∠ABC is a sandwich. B is the filling — the vertex."),
        26,
    )

    # Fix c4 - I used kid_tip("Book corner") with one argument. Need to patch after... I'll strreplace.

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Name points, lines, segments, and rays",
            "Spot parallel and perpendicular",
            "Define an angle and a degree",
            "Classify acute, right, obtuse, straight",
            "Use 90° and 180° as landmarks",
            "Draw and name figures",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u6_questions()


# ===========================================================================
# UNIT 7: Degrees and additive angles
# ===========================================================================

def _u7_questions():
    qs = []
    idx = 1

    types = [
        (15, "acute"), (30, "acute"), (45, "acute"), (60, "acute"), (89, "acute"),
        (90, "right"), (91, "obtuse"), (120, "obtuse"), (135, "obtuse"), (150, "obtuse"),
        (180, "straight"),
    ]
    for deg, kind in types:
        qs.append(mq(
            f"{deg}° is what kind of angle?",
            kind,
            f"{deg}° is {kind}.",
            idx,
            distractors=[x for x in ["acute", "right", "obtuse", "straight"] if x != kind][:3],
        ))
        idx += 1

    add = [
        ("A 40° angle and a 50° angle sit side by side and make one larger angle. The large angle is…", 90,
         "40+50=90. Adjacent angles add."),
        ("30° + 60° = ?", 90, "They make a right angle."),
        ("90° + 90° = ?", 180, "Two right angles make a straight angle."),
        ("20° + 70° = ?", 90, "Complement to 90 if they sit on a square corner."),
        ("45° + 45° = ?", 90, "Two equal acutes make a right angle."),
        ("100° + 80° = ?", 180, "They make a straight line."),
        ("A 35° piece is cut from a 90° angle. What is left?", 55, "90−35=55."),
        ("A 120° angle is split into 50° and ___.", 70, "120−50=70."),
        ("Three angles 30°, 30°, and 30° make…", 90, "30+30+30=90."),
        ("From a straight line, one angle is 110°. The adjacent angle on the line is…", 70, "180−110=70."),
    ]
    for text, ans, expl in add:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    measure_read = [
        ("A protractor reading of 0 to 55 on the inner scale, with 0 on one ray, measures…", 55, "Read the number on the other ray."),
        ("If you lined up 0 on the outer scale and the other ray hits 130, the angle is…", 130, "Use the scale that starts at 0 on your ray."),
        ("A right angle should read…", 90, "90° on either scale when lined up."),
        ("An angle that looks acute cannot be…", 120, "Acute is less than 90. 120 is obtuse."),
        ("If both scales show 40 and 140, and the angle is acute, the measure is…", 40,
         "Pick the number that matches the type. Acute → 40, not 140."),
        ("If both scales show 40 and 140, and the angle is obtuse, the measure is…", 140,
         "Obtuse → the larger reading."),
        ("Nearest degree: the ray sits a hair past 64, closer to 64 than 65. Measure?", 64, "Choose the closer tick."),
        ("A full turn is 360°. A quarter turn is…", 90, "360÷4=90."),
    ]
    for text, ans, expl in measure_read:
        qs.append(mq(text, ans, expl, idx))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"{10 + (i % 8) * 5}° + {20 + (i % 5) * 5}° = ?",
        10 + (i % 8) * 5 + 20 + (i % 5) * 5,
        "Adjacent angles add when they make one larger angle.",
        i,
    ))


def build_unit7():
    title = "Fourth Grade Math Unit 7: Measuring Turns in Degrees"
    description = (
        "Use degrees as a turn, add adjacent angles, subtract a piece from a larger angle, and choose the correct protractor scale."
    )

    c1 = concept_block(
        "1. A degree is a tiny turn",
        [
            "Imagine spinning around a point. One full spin is 360°.",
            "A degree is 1/360 of that spin. Small, but we can count them.",
            "90° is a quarter turn. 180° is a half turn. 270° is three quarters. 360° is all the way around.",
            "Angle measure tells how far one ray has turned from the other.",
            "We write a little circle after the number: 45°.",
            "Fourth grade measures whole-number degrees.",
        ],
        lesson_figure(
            _angle_svg(90, "quarter turn") + svg_circle(r=1, show_r=False),
            "A degree is 1/360 of a full spin",
            "The circle is one full turn, 360°. A quarter of that spin is 90°. We write the little circle: 90°.",
        )
        + solved(1, "How many degrees in a quarter turn?",
               ["A full turn is 360°.",
                "360 ÷ 4 = 90.",
                "90°."],
               "90")
        + matching(
            [("full turn", "360°"), ("half turn", "180°"),
             ("quarter turn", "90°"), ("tiny unit", "1°")],
            vid="g4u7-c1-match",
        ),
        kid_tip("Spin in your chair", "A quarter turn left is about 90°. A half turn faces the opposite way — 180°."),
        1,
    )

    c2 = concept_block(
        "2. Adjacent angles add",
        [
            "If two angles sit side by side and share a ray, they are adjacent.",
            "Their measures add to make the larger angle.",
            "40° + 50° = 90° when they sit on a square corner.",
            "You can split a 120° angle into 50° and 70° because 50+70=120.",
            "This is like adding like fractions: same kind of unit (degrees), add the counts.",
            "Draw the shared ray. Label each piece. Add to check the whole.",
        ],
        lesson_figure(
            _adjacent_angles(35, 55, "35°", "55°"),
            "A 35° piece cut from 90°",
            "The two openings sit side by side and share a ray. 35° + 55° = 90°. Subtract a piece from the whole, or add the pieces to check.",
        )
        + solved(1, "A 35° angle is cut from a 90° angle. What is left?",
               ["90 − 35 = 55.",
                "The leftover angle is 55°."],
               "55")
        + step_reveal(
            ["Find the whole angle.",
             "Find the known piece.",
             "Add pieces to make the whole, or subtract a piece from the whole.",
             "Check: pieces sum to the whole."],
            vid="g4u7-c2-steps",
        ),
        try_this("Puzzle pieces", "Adjacent angles are puzzle pieces of the larger opening."),
        6,
    )

    c3 = concept_block(
        "3. Angles on a straight line",
        [
            "Angles that sit together on a straight line add to 180°.",
            "If one is 110°, the other is 70° because 180 − 110 = 70.",
            "Two right angles on a line: 90 + 90 = 180. That checks.",
            "This helps you find a missing angle without a protractor sometimes.",
            "Make sure the picture really is a straight line, not a bent one.",
            "Then measure with the protractor to confirm.",
        ],
        lesson_figure(
            _adjacent_angles(125, 55, "125°", "55°"),
            "Angles on a straight line add to 180°",
            "The two rays make a line. If one angle is 125°, the neighbor is 180 − 125 = 55°. Check: 125 + 55 = 180.",
        )
        + solved(1, "On a straight line, one angle is 125°. The adjacent angle is…",
               ["Straight is 180°.",
                "180 − 125 = 55."],
               "55")
        + matching(
            [("90+90", "180"), ("110 + ?", "70"), ("straight", "180°"), ("two right angles", "a line")],
            vid="g4u7-c3-match",
        ),
        watch_out("Using 90 when the picture is a line",
                  "A straight line totals 180, not 90. 90 is only the square corner."),
        11,
    )

    c4 = concept_block(
        "4. Two scales on a protractor",
        [
            "A protractor has two sets of numbers. One runs 0 to 180 left to right. The other runs the opposite way.",
            "Always start from the 0 that sits on your ray.",
            "If the angle is acute, you want a reading less than 90. If obtuse, more than 90.",
            "If you see 40 and 140, the type tells you which is true.",
            "Line up the little hole or cross at the vertex first. Then the baseline. Then read.",
            "Practice this in Protractor Lab. The tool glows when you are lined up.",
        ],
        lesson_figure(
            _angle_svg(40, "acute 40°", "#22c55e"),
            "Pick the scale that matches the type",
            "This opening is skinny — acute — so it cannot be 140°. When the protractor shows 40 and 140, choose 40°.",
        )
        + solved(1, "The scales show 40 and 140. The angle looks acute. What is the measure?",
               ["Acute means less than 90.",
                "Choose 40°, not 140°."],
               "40")
        + protractor_box(
            "Put the hole on the vertex. Line 0 with one ray. Read the other ray. If the angle looks acute, pick the number under 90.",
            angle=40,
            show=True,
        ),
        kid_tip("Type first, then the number", "Guess acute or obtuse with your eyes. Then the wrong scale is obvious."),
        16,
    )

    c5 = concept_block(
        "5. Estimate, then measure",
        [
            "Before you read the protractor, estimate.",
            "Less than a square corner? Maybe 30, 45, 60.",
            "More than a square corner but not a line? Maybe 110, 135, 150.",
            "Your estimate catches a scale mix-up. If you guessed 50 and the protractor says 130, you used the wrong zero.",
            "Measure to the nearest degree. If the ray sits between ticks, pick the closer one.",
            "Write the unit: 64°, not 64.",
        ],
        lesson_figure(
            _angle_svg(80, "about 80°"),
            "Estimate first, then measure",
            "This opening is a little less than a square corner, so guess near 80°, not 100°. Then pick the protractor reading that matches the estimate.",
        )
        + solved(1, "You estimated 80°. The scales show 80 and 100. Which reading fits?",
               ["80 is near your estimate and is acute-ish, almost right.",
                "100 would be obtuse. The estimate picks 80°."],
               "80")
        + protractor_box(
            "New angle. Estimate first: acute, right, or obtuse? Then measure.",
            angle=75,
        ),
        try_this("Say the type out loud", "Acute, right, or obtuse. Then pick up the protractor."),
        21,
    )

    c6 = concept_block(
        "6. Put it together",
        [
            "Name the figure. Classify the angle. Estimate. Measure. Check that the number matches the type.",
            "If two adjacent angles are given, add them. If a whole and a piece are given, subtract.",
            "A missing angle on a line is 180 minus the one you know.",
            "Keep drawings large enough that the protractor can sit on them.",
            "The next unit is all measuring practice in the lab.",
            "Hearts still help. A wrong scale is the most common miss — slow down for that step.",
        ],
        lesson_figure(
            _adjacent_angles(30, 60, "30°", "60°"),
            "30° and 60° make a right angle",
            "Adjacent pieces add: 30 + 60 = 90. Name the type (right), then the number must match — not 270° from a wrong scale.",
        )
        + solved(1, "Two adjacent angles are 30° and 60°. What do they make?",
               ["30+60=90.",
                "A right angle."],
               "90")
        + matching(
            [("acute + wrong scale", "might read 140 instead of 40"),
             ("angles on a line", "sum 180"),
             ("adjacent pieces", "add"),
             ("piece from a whole", "subtract")],
            vid="g4u7-c6-match",
        ),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "See a degree as a tiny turn",
            "Add adjacent angles",
            "Use 180° on a straight line",
            "Choose the correct protractor scale",
            "Estimate before you measure",
            "Check type against the number",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u6_questions()


# ===========================================================================
# UNIT 8: Protractor lab
# ===========================================================================

def _u8_questions():
    qs = []
    idx = 1

    steps = [
        ("First, put the protractor's center hole on the…", "vertex",
         ["end of a ray far away", "middle of a ray", "number 90"],
         "The origin sits on the vertex."),
        ("Next, line the baseline up with…", "one ray",
         ["both rays at once always", "the number 90 only", "a grid line far away"],
         "One ray should sit on 0."),
        ("Then you read the number where…", "the other ray crosses the scale",
         ["the vertex sits", "your pencil is", "180 always"],
         "That number is the measure."),
        ("Use the scale whose 0 sits on…", "the ray you lined up",
         ["the other unused side only", "90 always", "the table"],
         "0 on the ray. Then follow that row of numbers."),
        ("An acute angle's reading is…", "less than 90",
         ["always 90", "more than 90", "180"],
         "If you got 140 on an acute drawing, you used the wrong 0."),
    ]
    for text, ans, dist, expl in steps:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    measures = [
        (20, "acute"), (35, "acute"), (45, "acute"), (70, "acute"), (90, "right"),
        (110, "obtuse"), (125, "obtuse"), (135, "obtuse"), (160, "obtuse"), (180, "straight"),
    ]
    for deg, kind in measures:
        qs.append(mq(f"You measure {deg}°. What type is that?", kind, f"{deg}° is {kind}.", idx,
                     distractors=[x for x in ["acute", "right", "obtuse", "straight"] if x != kind][:3]))
        idx += 1
        qs.append(mq(f"A drawing is a {kind} angle. Which reading fits: {deg} or {180 - deg if deg != 90 else 0}?",
                     deg if deg != 90 else 90,
                     f"Match the type to the scale. {kind} → {deg}°.",
                     idx,
                     distractors=[180 - deg if deg != 90 else 0, 180, 0]))
        idx += 1

    tools = [
        ("Snap to vertex means…", "move the hole onto the vertex",
         ["change the angle", "erase a ray", "add 90"],
         "In Protractor Lab, Snap puts the origin on the point."),
        ("Line up a ray means…", "rotate so 0 sits on one ray",
         ["change the measure", "flip the paper only", "hide the angle"],
         "The baseline matches one side of the angle."),
        ("If the hole is off the vertex, your reading will be…", "wrong",
         ["still perfect", "always 90", "always 0"],
         "The center must sit on the vertex."),
        ("A protractor is shaped like a…", "half circle",
         ["full cube", "triangle only", "number line only"],
         "0 to 180 around a semicircle."),
        ("The numbers on a protractor go up to…", 180, "A half-circle protractor measures to 180°."),
        ("To measure 90°, the other ray should pass through…", 90,
         "The middle of the arc, labeled 90."),
        ("Dragging the rim of the protractor in the lab…", "rotates it",
         ["deletes a ray", "changes the problem number", "adds a grid"],
         "Rim = rotate. Body = slide."),
        ("If your guess is 2 degrees off, you are…", "very close",
         ["using area", "done with multiplication", "on a line always"],
         "The lab counts within 2° as very close."),
    ]
    for item in tools:
        if len(item) == 4:
            qs.append(mq(item[0], item[1], item[3], idx, distractors=item[2]))
        else:
            qs.append(mq(item[0], item[1], item[2], idx))
        idx += 1

    combo = [
        ("Measure 45°, then 45° more adjacent. The large angle is…", 90, "45+45=90."),
        ("You read 70° and 110° on the two scales. The drawing is obtuse. Measure?", 110, "Obtuse → 110."),
        ("You read 70° and 110°. The drawing is acute. Measure?", 70, "Acute → 70."),
        ("A 90° angle split into 25° and ___.", 65, "90−25=65."),
        ("Straight line, one angle 95°. Other angle?", 85, "180−95=85."),
        ("Quarter turn measure?", 90, "90°."),
        ("The ray sits on 48°, a little closer to 48 than 49. Record…", 48, "Nearest degree."),
        ("After measuring, write…", "the number and the degree mark",
         ["only a fraction", "a decimal money amount", "perimeter"],
         "64° not 64 square units."),
    ]
    for item in combo:
        if len(item) == 4:
            qs.append(mq(item[0], item[1], item[3], idx, distractors=item[2]))
        else:
            qs.append(mq(item[0], item[1], item[2], idx))
        idx += 1

    return _fill(qs, 55, lambda i: mq(
        f"An angle measures {15 + (i % 15) * 5}°. Is it acute, right, or obtuse?"
        if 15 + (i % 15) * 5 != 90 else "An angle measures 90°. Is it acute, right, or obtuse?",
        "right" if 15 + (i % 15) * 5 == 90 else ("acute" if 15 + (i % 15) * 5 < 90 else "obtuse"),
        "Compare with 90°.",
        i,
        distractors=["acute", "right", "obtuse"],
    ))


def build_unit8():
    title = "Fourth Grade Math Unit 8: Protractor Lab"
    description = (
        "Practice placing, lining up, and reading a protractor. Use the interactive Protractor Lab to measure acute, right, and obtuse angles."
    )

    c1 = concept_block(
        "1. Meet the protractor",
        [
            "A protractor is a half-circle tool for measuring angles in degrees.",
            "Find the origin: a small hole or cross at the middle of the flat edge. That sits on the vertex.",
            "The flat edge is the baseline. It should sit on one ray, with 0 at that ray.",
            "Numbers run 0 to 180 along the curve. There are two rows, running opposite ways.",
            "You will drag this tool in Protractor Lab. Grab the middle to slide. Grab the rim to rotate.",
            "Real plastic protractors work the same way on paper.",
        ],
        lesson_figure(
            _angle_svg(60, "60°"),
            "Hole on the vertex, then read",
            "The two rays meet at the vertex. That is where the protractor hole goes. This starter angle is 60° — use the lab below to practice placing the tool.",
        )
        + solved(1, "Where does the hole of the protractor go?",
               ["On the vertex, where the two rays meet."],
               "vertex")
        + protractor_box(
            "Drag the protractor. Snap to vertex. Line up a ray. This starter angle is 60°.",
            angle=60,
            show=True,
        ),
        kid_tip("Hole first", "If the hole is not on the vertex, every reading will be off. Snap, then rotate."),
        1,
    )

    c2 = concept_block(
        "2. Line up 0",
        [
            "After the hole is on the vertex, rotate until the baseline covers one ray.",
            "That ray should pass through 0 (and 180 on the other scale).",
            "Now look at the second ray. See which number it crosses on the scale that started at 0.",
            "In the lab, Line up a ray does this for you once, so you can practice reading.",
            "Then try it by hand: New angle, Snap, rotate yourself.",
            "When it is lined up, the lab can flash Lined up — read ___.",
        ],
        lesson_figure(
            _angle_svg(45, "0° on one ray → 45°"),
            "Line 0 up with one ray, then read the other",
            "After the hole is on the vertex, rotate until one ray sits on 0. The other ray of this angle crosses 45° on that same scale.",
        )
        + solved(1, "Which scale do you read?",
               ["The scale whose 0 sits on the ray you lined up."],
               "the 0-on-the-ray scale")
        + protractor_box(
            "Line up a ray, then read. Hide measure and type your reading. Check.",
            angle=45,
        ),
        try_this("Zero on the ray you can see clearly", "Pick the less crowded ray for 0 when you can."),
        6,
    )

    c3 = concept_block(
        "3. Acute angles",
        [
            "Acute openings are less than 90°. On the protractor they sit before the 90 mark if 0 is lined up.",
            "Common practice angles: 20°, 30°, 45°, 60°, 75°.",
            "If you read 120° on a skinny angle, you started from the wrong 0. Use 60° instead (because 180−120=60, and 60 looks acute).",
            "Estimate skinny vs square corner first.",
            "Type your reading in the lab. Check. Within 2° is very close.",
            "Draw an acute angle on paper too, then measure it with a real protractor if you have one.",
        ],
        lesson_figure(
            _angle_svg(30, "acute 30°", "#22c55e"),
            "A skinny angle is less than 90°",
            "If you see 30 and 150, the skinny opening takes 30°, not 150°. The two protractor numbers add to 180 — acute takes the small one.",
        )
        + solved(1, "You see 30 and 150. The angle is skinny. Measure?",
               ["Skinny means acute.",
                "30°."],
               "30")
        + protractor_box("Measure this acute angle. Estimate, then check.", angle=30),
        watch_out("Reading the inner 150 on a small opening",
                  "The two numbers on a protractor add to 180. Acute takes the small one."),
        11,
    )

    c4 = concept_block(
        "4. Right angles",
        [
            "A right angle hits 90 on both scales when you are lined up — 90 is in the middle.",
            "The square-corner mark on a drawing should match a 90° reading.",
            "If you measure 88° or 92°, your hole or baseline slipped. Snap and line up again.",
            "Clock hands at 3:00 are a right angle. So is a book corner.",
            "Practice 90° until lining up feels automatic.",
            "Then you can split a right angle into 30°+60° and check they add.",
        ],
        lesson_figure(
            _angle_svg(90, "90°"),
            "A square corner hits 90 on both scales",
            "When you are lined up, a right angle's second ray passes through 90 — the middle of the arc. If you read 88° or 92°, snap and line up again.",
        )
        + solved(1, "A square corner should measure…",
               ["90°."],
               "90")
        + protractor_box("This one is a right angle. Line it up. The other ray should pass through 90.", angle=90, show=True),
        kid_tip("90 is the peak", "On a half-circle protractor, 90 sits at the top of the arc when the baseline is flat."),
        16,
    )

    c5 = concept_block(
        "5. Obtuse angles",
        [
            "Obtuse openings are wider than a square corner. Readings sit past 90: 110°, 135°, 160°.",
            "If you lined up 0 and the other ray is on the far side of 90, you are in obtuse territory.",
            "The wrong-scale trap here is reading 50° when it is really 130°.",
            "Eyes first: is it wider than a book corner? Then the number must be greater than 90.",
            "Straight 180° is the end of the protractor. The two rays make a line.",
            "New angle in the lab until you get several obtuse ones.",
        ],
        lesson_figure(
            _angle_svg(130, "obtuse 130°", "#f59e0b"),
            "Wider than a square corner — read past 90°",
            "Scales show 50 and 130. Eyes first: this opening is obtuse, so the measure is 130°, not 50°.",
        )
        + solved(1, "Scales show 50 and 130. The angle is wider than a square corner. Measure?",
               ["Obtuse → 130°."],
               "130")
        + protractor_box("Measure this obtuse angle. It should read more than 90°.", angle=130),
        try_this("Compare to 90 on the tool", "If the second ray is past the 90 tick, you are obtuse. Read the big number."),
        21,
    )

    c6 = concept_block(
        "6. Lab practice round",
        [
            "Hit New angle many times. For each: estimate type, snap, line up, read, type, check.",
            "Then hide the measure and do it from sight.",
            "Mix adjacent-angle math: measure two pieces that make a right or straight angle.",
            "Write a small table: estimate, measure, type. See if they agree.",
            "When paper and lab agree, you can trust your hands.",
            "You are a fourth-grade angle measurer. That is a real math tool skill.",
        ],
        lesson_figure(
            _angle_svg(80, "estimate ~80°"),
            "Estimate, measure, match the type",
            "Guess a little less than 90°. If the scales show 80 and 100, 80° matches the estimate. Then hit New angle in the lab and repeat.",
        )
        + solved(1, "Estimate 80°, scales 80 and 100. Record…",
               ["The estimate matches 80°.",
                "80°."],
               "80")
        + protractor_box("Free practice. Press New angle. Snap. Line up. Type your reading. Check.")
        + protractor_box("Another round — this time a 135° obtuse angle.", angle=135)
        + matching(
            [("hole", "vertex"), ("0", "one ray"), ("read", "the other ray"),
             ("acute vs 40/140", "40")],
            vid="g4u8-c6-match",
        ),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Place the protractor on the vertex",
            "Line 0 up with one ray",
            "Measure acute angles",
            "Measure right angles",
            "Measure obtuse angles",
            "Practice in Protractor Lab",
        ],
        body,
        practice_slots(31, 25),
    )
    return title, description, content, _u8_questions()


def build_master():
    return f"""
<h1>Fourth Grade Math</h1>
<p>This is a full fourth-grade math path. We use <strong>short words</strong>, pictures, tools, and lots of practice.</p>
<p>You will work with numbers to one million, multiply and divide large numbers, add and subtract fractions with the same denominator, read tenths and hundredths, name lines and angles, and measure with a protractor. After each idea there are 5 quick questions. At the end of a unit there are 50 more. Hearts help you. Take your time.</p>
{page_break()}
<h2>The eight units</h2>
<ol>
<li>Unit 1 — Place Value to One Million</li>
<li>Unit 2 — Multi-Digit Multiplication</li>
<li>Unit 3 — Multi-Digit Division</li>
<li>Unit 4 — Add and Subtract Fractions</li>
<li>Unit 5 — Decimals: Tenths and Hundredths</li>
<li>Unit 6 — Points, Lines, and Angle Types</li>
<li>Unit 7 — Measuring Turns in Degrees</li>
<li>Unit 8 — Protractor Lab</li>
</ol>
<p>Start with place value. Multiplication and division grow from there. Fractions and decimals are two ways to name parts of a whole. Geometry ends with a real tool: the protractor.</p>
{page_break()}
<h2>How to learn</h2>
<p>Keep digits in their places. Draw area models for two-digit × two-digit. Check division with multiplication. Add fraction tops when bottoms match. Line up decimal points. Estimate an angle, then measure it in Protractor Lab.</p>
<p>If a question feels hard, try a smaller number first. Then come back. You are building number sense — a feeling for how numbers work.</p>
"""
