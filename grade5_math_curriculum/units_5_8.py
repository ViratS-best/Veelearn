"""Fifth Grade Math units 5–8: divide fractions, volume, coordinate plane, expressions — plus master page."""

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
    volume_prism,
    coordinate_plane,
    page_break,
    mq,
    renumber,
)


def _fill(qs, need, factory):
    while len(qs) < need:
        qs.append(factory(len(qs) + 1))
    return renumber(qs[:need])


# ===========================================================================
# UNIT 5: Divide unit fractions
# ===========================================================================

def _u5_questions():
    qs = []
    idx = 1

    for text, ans, dist, expl in [
        ("6 ÷ 1/2 = ?", "12", ["3", "6", "1/12"], "How many halves in 6? Twelve."),
        ("4 ÷ 1/2 = ?", "8", ["2", "4", "1/8"], "Eight halves make 4."),
        ("3 ÷ 1/3 = ?", "9", ["1", "3", "1/9"], "Nine thirds make 3."),
        ("5 ÷ 1/4 = ?", "20", ["1.25", "9", "1/20"], "Twenty fourths make 5."),
        ("8 ÷ 1/2 = ?", "16", ["4", "8", "1/16"], "Sixteen halves."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, dist, expl in [
        ("1/2 ÷ 4 = ?", "1/8", ["2", "4/2", "1/4"], "Split a half into 4 equal parts."),
        ("1/3 ÷ 2 = ?", "1/6", ["2/3", "1/5", "3/2"], "Half of a third is a sixth."),
        ("1/4 ÷ 3 = ?", "1/12", ["3/4", "1/7", "4/3"], "A fourth split 3 ways is twelfths."),
        ("1/5 ÷ 4 = ?", "1/20", ["4/5", "1/9", "5/4"], "Four equal pieces of a fifth."),
        ("1/2 ÷ 5 = ?", "1/10", ["5/2", "1/7", "2/5"], "A half split into 5 is tenths."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, dist, expl in [
        ("How many 1/2-cup servings in 3 cups?", "6", ["3/2", "1.5", "1/6"], "3 ÷ 1/2 = 6."),
        ("How many 1/4-hour slots in 2 hours?", "8", ["2/4", "4", "1/8"], "2 ÷ 1/4 = 8."),
        ("A 1/2 sandwich shared by 2 people: each gets…", "1/4", ["1", "1/2", "2"], "1/2 ÷ 2 = 1/4."),
        ("Ribbon is 1/3 yard. Cut into 4 equal pieces. Each piece?", "1/12 yard", ["4/3 yard", "1/7 yard", "3/4 yard"], "1/3 ÷ 4 = 1/12."),
        ("How many 1/3s in 5?", "15", ["5/3", "8", "1/15"], "5 ÷ 1/3 = 15."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, dist, expl in [
        ("Dividing by 1/2 is the same as multiplying by…", "2", ["1/2", "0.5", "1"], "÷ 1/2 = × 2."),
        ("1/3 ÷ 4 = 1/3 × ?", "1/4", ["4", "3", "1/3"], "Dividing by 4 is × 1/4."),
        ("6 ÷ 1/2 = 6 × ?", "2", ["1/2", "6", "1"], "Flip 1/2 to 2/1."),
        ("1/4 ÷ 2 = 1/4 × ?", "1/2", ["2", "4", "1"], "Flip 2 to 1/2."),
        ("To divide fractions you can multiply by the…", "reciprocal", ["numerator only", "denominator only", "sum"], "Flip the second fraction, then multiply."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    more = [
        ("2 ÷ 1/2 = ?", "4", ["1", "2", "1/4"], "Four halves make 2."),
        ("9 ÷ 1/3 = ?", "27", ["3", "9", "1/27"], "Twenty-seven thirds."),
        ("10 ÷ 1/5 = ?", "50", ["2", "15", "1/50"], "Fifty fifths make 10."),
        ("1 ÷ 1/4 = ?", "4", ["1/4", "5", "1"], "Four fourths make 1."),
        ("1/2 ÷ 2 = ?", "1/4", ["1", "1/2", "4"], "Half of a half."),
        ("1/3 ÷ 3 = ?", "1/9", ["1", "1/6", "3"], "A third split 3 ways."),
        ("1/8 ÷ 2 = ?", "1/16", ["1/6", "1/4", "2/8"], "Half of an eighth."),
        ("Check: 12 × 1/2 = 6, so 6 ÷ 1/2 = ?", "12", ["3", "6", "24"], "Division undoes the multiply."),
        ("Check: 8 × 1/4 = 2, so 2 ÷ 1/4 = ?", "8", ["2", "4", "1/8"], "Inverse operations."),
        ("7 ÷ 1/2 = ?", "14", ["3.5", "7", "1/14"], "Fourteen halves."),
        ("1/6 ÷ 2 = ?", "1/12", ["1/8", "1/3", "2/6"], "Half of a sixth."),
        ("How many 1/8s in 1?", "8", ["1/8", "9", "1"], "Eight eighths."),
        ("How many 1/8s in 3?", "24", ["3/8", "11", "1/24"], "3 × 8 = 24."),
        ("A 4-pint pitcher poured in 1/2-pint cups fills…", "8 cups", ["2 cups", "4 cups", "1/8 cup"], "4 ÷ 1/2 = 8."),
        ("Split 1/2 hour among 3 tasks equally. Each task?", "1/6 hour", ["3/2 hour", "1/5 hour", "2/3 hour"], "1/2 ÷ 3 = 1/6."),
        ("1/2 ÷ 1 is…", "1/2", ["2", "1", "0"], "Dividing by 1 leaves it the same."),
        ("5 ÷ 1/5 = ?", "25", ["1", "10", "1/25"], "Twenty-five fifths."),
        ("1/4 ÷ 4 = ?", "1/16", ["1", "1/8", "1"], "A fourth of a fourth."),
        ("12 ÷ 1/3 = ?", "36", ["4", "15", "1/36"], "Thirty-six thirds."),
        ("1/5 ÷ 5 = ?", "1/25", ["1", "1/10", "25"], "A fifth split into 5."),
    ]
    for text, ans, dist, expl in more:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    return _fill(qs, 80, lambda i: mq(
        f"How many 1/2s are in {i % 8 + 2}?",
        str(2 * (i % 8 + 2)),
        f"Multiply by 2. {i % 8 + 2} ÷ 1/2 = {2 * (i % 8 + 2)}.",
        i,
        distractors=[str(i % 8 + 2), str((i % 8 + 2) // 2 or 1), "1"],
    ))


def build_unit5():
    title = "Fifth Grade Math Unit 5: Divide Unit Fractions"
    description = (
        "Divide whole numbers by unit fractions and unit fractions by whole numbers. Use pictures and the reciprocal."
    )

    c1 = concept_block(
        "1. Whole number ÷ unit fraction",
        [
            "A unit fraction has 1 on top: 1/2, 1/3, 1/4.",
            "6 ÷ 1/2 asks: how many halves are in 6 wholes?",
            "Each whole holds 2 halves, so 6 wholes hold 12 halves. 6 ÷ 1/2 = 12.",
            "3 ÷ 1/3 = 9 because each whole holds 3 thirds.",
            "The quotient is larger than the starting whole number. That feels surprising until you picture the pieces.",
            "Think of a pizza: 4 pizzas cut into halves make 8 half-pizzas.",
        ],
        solved(1, "Find 6 ÷ 1/2.",
               ["Each 1 holds two 1/2 pieces.",
                "6 wholes × 2 pieces each = 12.",
                "There are 12 halves in 6."],
               "12")
        + matching(
            [("4 ÷ 1/2", "8"), ("3 ÷ 1/3", "9"), ("5 ÷ 1/4", "20"), ("1 ÷ 1/5", "5")],
            vid="g5u5-c1-match",
        ),
        kid_tip("How many pieces?", "÷ 1/n means 'how many 1/n pieces fit?' Each whole holds n of them."),
        1,
    )

    c2 = concept_block(
        "2. Unit fraction ÷ whole number",
        [
            "1/2 ÷ 4 asks: split one half into 4 equal parts. Each part is 1/8.",
            "You are sharing a small piece among more people, so each share gets smaller.",
            "1/3 ÷ 2 = 1/6. Half of a third is a sixth.",
            "A picture: a bar split into 3, shade one third, then cut that third in half.",
            "The quotient is smaller than the unit fraction you started with.",
            "Ribbon 1/3 yard cut into 4 equal pieces: each piece is 1/12 yard.",
        ],
        solved(1, "Find 1/2 ÷ 4.",
               ["Start with one half.",
                "Cut it into 4 equal shares.",
                "Each share is 1/8 of the original whole."],
               "1/8")
        + step_reveal(
            ["Draw the whole.",
             "Shade the unit fraction.",
             "Split that shaded piece into equal shares.",
             "Name one share."],
            vid="g5u5-c2-steps",
        ),
        watch_out("Switching the numbers", "1/2 ÷ 4 is not 4 ÷ 1/2. One is 1/8. The other is 8."),
        6,
    )

    c3 = concept_block(
        "3. Pictures: how many fit?",
        [
            "For whole ÷ unit fraction, draw wholes and mark the unit pieces. Count them.",
            "3 cups, 1/2-cup servings: draw 3 cups, each split in half, count 6 servings.",
            "2 hours in 1/4-hour slots: each hour has 4 quarters, so 8 slots.",
            "For unit fraction ÷ whole, draw the small piece and split it.",
            "If you can count the pieces, you can name the quotient.",
            "Stories about servings, time slots, and cutting ribbon all use this picture.",
        ],
        solved(1, "How many 1/2-cup servings are in 3 cups?",
               ["Each cup makes 2 half-cup servings.",
                "3 cups make 6 servings.",
                "3 ÷ 1/2 = 6."],
               "6 servings")
        + phet_box("build_frac"),
        try_this("Sketch cups", "Even messy cups with a line down the middle make the count obvious."),
        11,
    )

    c4 = concept_block(
        "4. Multiply by the reciprocal",
        [
            "The reciprocal of 1/2 is 2 (which is 2/1). Flip the fraction.",
            "Dividing by a fraction is the same as multiplying by its reciprocal.",
            "6 ÷ 1/2 = 6 × 2 = 12.",
            "1/3 ÷ 4 = 1/3 × 1/4 = 1/12.",
            "This rule matches the pictures. Use pictures until the rule feels honest.",
            "Keep, change, flip is a memory phrase: keep the first number, change ÷ to ×, flip the second.",
        ],
        solved(1, "Rewrite 6 ÷ 1/2 as a multiply, then compute.",
               ["Reciprocal of 1/2 is 2/1.",
                "6 × 2/1 = 12.",
                "Same answer as counting halves."],
               "12")
        + matching(
            [("÷ 1/2", "× 2"), ("÷ 1/3", "× 3"), ("÷ 4", "× 1/4"), ("÷ 2", "× 1/2")],
            vid="g5u5-c4-match",
        ),
        kid_tip("Flip the second number only", "Do not flip both. The first number stays. The second number flips."),
        16,
    )

    c5 = concept_block(
        "5. Divide-fraction stories",
        [
            "How many servings? That is usually whole ÷ unit fraction.",
            "Share one piece among people? That is usually unit fraction ÷ whole.",
            "A 4-pint pitcher poured into 1/2-pint cups fills 8 cups.",
            "Split 1/2 hour among 3 equal tasks: each task is 1/6 hour.",
            "Write the equation from the story before you compute.",
            "Label servings, hours, yards — the unit tells you that you answered the right question.",
        ],
        solved(1, "Ribbon is 1/3 yard long. Cut into 4 equal pieces. How long is each piece?",
               ["This is 1/3 ÷ 4.",
                "1/3 × 1/4 = 1/12.",
                "Each piece is 1/12 yard."],
               "1/12 yard")
        + step_reveal(
            ["Is it 'how many fit' or 'share this piece'?",
             "Write ÷.",
             "Use a picture or the reciprocal.",
             "Label the unit."],
            vid="g5u5-c5-steps",
        ),
        try_this("Name the type", "Say out loud: packing small pieces into a big amount, or splitting a small amount into groups."),
        21,
    )

    c6 = concept_block(
        "6. Check with multiplication",
        [
            "Division and multiplication undo each other.",
            "If 6 ÷ 1/2 = 12, then 12 × 1/2 should be 6. It is.",
            "If 1/2 ÷ 4 = 1/8, then 1/8 × 4 should be 1/2. It is.",
            "Always have a way to look back. The check catches a flipped pair.",
            "1/2 ÷ 4 and 4 ÷ 1/2 are different. The check tells you which one you actually solved.",
            "When the check fails, look at whether you flipped the correct number.",
        ],
        solved(1, "Check: is 8 a reasonable answer for 2 ÷ 1/4?",
               ["2 ÷ 1/4 should be 8.",
                "Check: 8 × 1/4 = 2.",
                "Yes. The check matches."],
               "yes, 8 × 1/4 = 2")
        + watch_out("Checking with the wrong pair",
                    "Do not multiply the two original numbers and hope. Multiply the quotient by the divisor."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Divide a whole number by a unit fraction",
            "Divide a unit fraction by a whole number",
            "Use pictures to count pieces",
            "Multiply by the reciprocal",
            "Solve divide-fraction stories",
            "Check with multiplication",
        ],
        body,
        practice_slots(31, 50),
    )
    return title, description, content, _u5_questions()


# ===========================================================================
# UNIT 6: Volume
# ===========================================================================

def _u6_questions():
    qs = []
    idx = 1

    for text, ans, dist, expl in [
        ("A box packed with 24 unit cubes has volume…", "24 cubic units", ["24 square units", "8 cubes only", "12 cubic units"], "Volume is the count of unit cubes."),
        ("A layer is 5 cubes by 3 cubes. One layer has…", "15 cubes", ["8", "2", "30"], "5×3=15."),
        ("Two layers of 15 cubes each make volume…", "30", ["17", "15", "45"], "15×2=30."),
        ("A unit cube has side length 1. Its volume is…", "1 cubic unit", ["1 square unit", "3", "6"], "1×1×1=1."),
        ("Volume is measured in…", "cubic units", ["square units", "degrees", "tenths"], "Three dimensions: length, width, height."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for l, w, h in [(4, 3, 2), (5, 2, 3), (6, 4, 1), (3, 3, 3), (10, 2, 2)]:
        qs.append(mq(
            f"A prism is {l} by {w} by {h}. Volume?",
            l * w * h,
            f"{l}×{w}×{h} = {l * w * h} cubic units.",
            idx,
        ))
        idx += 1

    for b, h in [(12, 5), (20, 3), (15, 4), (8, 6), (18, 2)]:
        qs.append(mq(
            f"Base area is {b} square units and height is {h}. Volume?",
            b * h,
            f"V = B × h = {b} × {h} = {b * h}.",
            idx,
        ))
        idx += 1

    # composite volumes
    for a, b, total in [((4, 3, 2), (2, 2, 3), 36), ((5, 1, 2), (3, 3, 2), 28), ((6, 2, 2), (4, 4, 1), 40)]:
        va = a[0] * a[1] * a[2]
        vb = b[0] * b[1] * b[2]
        qs.append(mq(
            f"One prism {a[0]}×{a[1]}×{a[2]} and another {b[0]}×{b[1]}×{b[2]}. Total volume?",
            va + vb,
            f"{va} + {vb} = {va + vb} cubic units.",
            idx,
        ))
        idx += 1

    for text, ans, dist, expl in [
        ("V = 48, l = 4, w = 3. Height?", "4", ["48", "12", "7"], "4×3×h=48 → 12h=48 → h=4."),
        ("V = 60, B = 12. Height?", "5", ["72", "48", "6"], "12×h=60 → h=5."),
        ("V = 100, l = 5, h = 4. Width?", "5", ["80", "20", "9"], "5×w×4=100 → 20w=100 → w=5."),
        ("A cube with edge 4 has volume…", "64", ["16", "12", "48"], "4×4×4=64."),
        ("A cube with edge 5 has volume…", "125", ["25", "15", "100"], "5×5×5=125."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    more = [
        ("4×3×5 = ?", 60, None, "60 cubic units."),
        ("2×8×3 = ?", 48, None, "48 cubic units."),
        ("1×1×12 = ?", 12, None, "A stick of 12 cubes."),
        ("7×2×2 = ?", 28, None, "28 cubic units."),
        ("9×3×1 = ?", 27, None, "27 cubic units."),
        ("Base 6×5, height 2. Volume?", 60, None, "30×2=60."),
        ("Base 4×4, height 4. Volume?", 64, None, "A cube of edge 4."),
        ("3 layers of 8 cubes. Volume?", 24, None, "8×3=24."),
        ("A box 10 by 10 by 2. Volume?", 200, None, "100×2=200."),
        ("Missing height: 5×2×h=50. h=?", 5, None, "10h=50."),
        ("Missing length: l×3×3=36. l=?", 4, None, "9l=36."),
        ("Two 3×3×3 cubes together. Volume?", 54, None, "27+27=54."),
        ("A 6×1×1 prism next to a 2×2×2 cube. Total?", 14, None, "6+8=14."),
        ("Packing a 4×3×2 box with 1-cm cubes needs how many cubes?", 24, None, "24 cubes."),
        ("If each cube is 1 inch on a side, 24 cubes fill…", "24 cubic inches", ["24 square inches", "24 inches", "8 cubic inches"], "Unit cubes of 1 inch give cubic inches."),
        ("Area of a 4-by-3 rectangle is…", "12 square units", ["12 cubic units", "7", "24 square units"], "Area is 2D. Volume needs height too."),
        ("Volume vs area: 4×3×2 volume is 24. The 4×3 face area is…", "12", ["24", "6", "9"], "One face is length × width."),
        ("A pool 5 m by 4 m by 2 m holds…", "40 cubic meters", ["40 square meters", "11 meters", "20 cubic meters"], "5×4×2=40."),
        ("Triple the height of a 4×3×2 prism. New volume?", 72, None, "Height 6: 4×3×6=72."),
        ("Same base 12, height from 3 to 6. Volume from 36 to…", 72, None, "Double height doubles volume."),
    ]
    for text, ans, dist, expl in more:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    return _fill(qs, 80, lambda i: mq(
        f"A prism is 2 by 2 by {i % 6 + 1}. Volume?",
        4 * (i % 6 + 1),
        f"2×2×{i % 6 + 1} = {4 * (i % 6 + 1)}.",
        i,
    ))


def build_unit6():
    title = "Fifth Grade Math Unit 6: Volume"
    description = (
        "Measure volume with unit cubes. Use V = l × w × h and V = B × h. Add volumes of rectangular prisms."
    )

    c1 = concept_block(
        "1. Volume as unit cubes",
        [
            "Volume is how much space a solid takes up.",
            "A unit cube is 1 by 1 by 1. Its volume is 1 cubic unit.",
            "If you pack a box with unit cubes and fill it with no gaps, the count of cubes is the volume.",
            "You can build volume in layers. A 5-by-3 layer has 15 cubes. Two such layers make 30.",
            "Area is about covering a flat face (square units). Volume is about filling space (cubic units).",
            "Leave no air pockets in the packing picture. Volume counts every cube inside.",
        ],
        solved(1, "A box holds 2 layers of 5-by-3 unit cubes. What is the volume?",
               ["One layer: 5 × 3 = 15 cubes.",
                "Two layers: 15 × 2 = 30.",
                "Volume = 30 cubic units."],
               "30 cubic units")
        + matching(
            [("unit cube", "1 cubic unit"), ("layer 5×3", "15 cubes"),
             ("2 layers of 15", "30 cubes"), ("area of a face", "square units")],
            vid="g5u6-c1-match",
        ),
        kid_tip("Layers", "Find how many cubes in one layer. Multiply by how many layers (the height)."),
        1,
    )

    c2 = concept_block(
        "2. V = length × width × height",
        [
            "A rectangular prism has three edge lengths: length, width, and height.",
            "Volume = length × width × height. You can multiply in any order.",
            "A 4-by-3-by-2 prism has volume 4 × 3 × 2 = 24 cubic units.",
            "That matches packing: a 4-by-3 layer (12 cubes) stacked 2 high.",
            "Keep the units cubic: cubic centimeters, cubic inches, cubic meters.",
            "A cube is a special prism with all edges equal. Edge 4 → 4×4×4=64.",
        ],
        volume_prism(4, 3, 2)
        + solved(1, "Find the volume of a 4 by 3 by 2 rectangular prism.",
                 ["Multiply the three edges.",
                  "4 × 3 = 12 (one layer).",
                  "12 × 2 = 24."],
                 "24 cubic units"),
        try_this("Any order", "2 × 4 × 3 is the same 24. Associative and commutative properties still work."),
        6,
    )

    c3 = concept_block(
        "3. V = B × h (base area times height)",
        [
            "B stands for the area of the base. For a rectangular base, B = length × width.",
            "Then volume is B × height. Same formula, grouped differently.",
            "If the base is 12 square units and the height is 5, volume is 60 cubic units.",
            "This version is handy when someone already tells you the base area.",
            "It also prepares you for later prisms whose bases are not rectangles.",
            "Check: a 4-by-3 base has B=12. Height 2 → 24, matching l×w×h.",
        ],
        solved(1, "Base area is 12 square units. Height is 5. Volume?",
               ["V = B × h.",
                "12 × 5 = 60.",
                "60 cubic units."],
               "60 cubic units")
        + step_reveal(
            ["Find the base area B (or use the B you are given).",
             "Find the height.",
             "Multiply B × h.",
             "Label cubic units."],
            vid="g5u6-c3-steps",
        ),
        watch_out("Leaving volume in square units", "B is square units. After × height, the answer is cubic."),
        11,
    )

    c4 = concept_block(
        "4. Add volumes (composite solids)",
        [
            "Some shapes are two rectangular prisms stuck together.",
            "Find each volume, then add.",
            "A 4×3×2 prism (24) joined to a 2×2×3 prism (12) has total volume 36.",
            "Do not add the edges as if they were one longer prism unless they truly share a full face and line up that way.",
            "A sketch helps you see the two boxes.",
            "This is like adding areas of two rectangles, one dimension up.",
        ],
        solved(1, "Prism A is 4×3×2. Prism B is 2×2×3. Total volume?",
               ["A: 4×3×2 = 24.",
                "B: 2×2×3 = 12.",
                "24+12 = 36 cubic units."],
               "36 cubic units")
        + matching(
            [("4×3×2", "24"), ("2×2×3", "12"), ("24+12", "36"), ("3×3×3 + 3×3×3", "54")],
            vid="g5u6-c4-match",
        ),
        kid_tip("Split, then add", "If the solid looks like an L, split it into two boxes you can measure."),
        16,
    )

    c5 = concept_block(
        "5. Missing dimensions",
        [
            "If you know volume and two edges, you can find the third.",
            "4 × 3 × h = 48 means 12h = 48, so h = 4.",
            "If you know V and B, then h = V ÷ B. 60 ÷ 12 = 5.",
            "This is division undoing multiplication — the same relationship as always.",
            "A cube: if volume is 64, the edge is 4 because 4×4×4=64.",
            "Check by multiplying back. The three edges times each other must return V.",
        ],
        solved(1, "Volume is 48. Length 4, width 3. What is the height?",
               ["4 × 3 × h = 48.",
                "12 × h = 48.",
                "h = 4."],
               "4")
        + try_this("Divide the known product", "Peel off the factors you already have. Volume ÷ (length × width) = height."),
        21,
    )

    c6 = concept_block(
        "6. Volume stories",
        [
            "A box, a pool, a fish tank, a packing crate — all rectangular prisms in stories.",
            "A pool 5 m by 4 m by 2 m holds 40 cubic meters of water (if filled to the top).",
            "Packing a 4×3×2 box with 1-cm cubes needs 24 cubes.",
            "If you triple only the height, volume triples. 4×3×2=24 becomes 4×3×6=72.",
            "Read which lengths are given. Sometimes a story gives base area instead of both base edges.",
            "Include cubic units so the answer is a volume, not an area or a length.",
        ],
        solved(1, "A tank is 5 m long, 4 m wide, and 2 m high. How much space inside?",
               ["V = 5 × 4 × 2.",
                "20 × 2 = 40.",
                "40 cubic meters."],
               "40 cubic meters")
        + step_reveal(
            ["Sketch the box and label l, w, h.",
             "Choose l×w×h or B×h.",
             "Multiply.",
             "Write cubic units."],
            vid="g5u6-c6-steps",
        ),
        watch_out("Adding 5+4+2", "That would be a perimeter-style mix-up. Volume multiplies the three edges."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Count unit cubes",
            "Use V = l × w × h",
            "Use V = B × h",
            "Add two prism volumes",
            "Find a missing edge",
            "Solve volume stories",
        ],
        body,
        practice_slots(31, 50),
    )
    return title, description, content, _u6_questions()


# ===========================================================================
# UNIT 7: Coordinate plane
# ===========================================================================

def _u7_questions():
    qs = []
    idx = 1

    for text, ans, dist, expl in [
        ("The point (0, 0) is called the…", "origin", ["x-axis", "y-axis", "quadrant"], "Both coordinates are 0."),
        ("The horizontal axis is the…", "x-axis", ["y-axis", "origin", "diagonal"], "x runs left-right. In grade 5 we go right."),
        ("The vertical axis is the…", "y-axis", ["x-axis", "origin", "width"], "y runs up-down. In grade 5 we go up."),
        ("In (3, 5), the 3 is the…", "x-coordinate", ["y-coordinate", "origin", "area"], "First number is x (right)."),
        ("In (3, 5), the 5 is the…", "y-coordinate", ["x-coordinate", "origin", "volume"], "Second number is y (up)."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, dist, expl in [
        ("From (0, 0) go right 4, up 1. The point is…", "(4, 1)", ["(1, 4)", "(4, 0)", "(0, 1)"], "x=4, y=1."),
        ("From (0, 0) go right 2, up 5. The point is…", "(2, 5)", ["(5, 2)", "(2, 0)", "(0, 5)"], "x first."),
        ("Point (0, 3) sits on the…", "y-axis", ["x-axis", "origin only", "line y=0"], "x=0 means on the y-axis."),
        ("Point (5, 0) sits on the…", "x-axis", ["y-axis", "origin only", "line x=0"], "y=0 means on the x-axis."),
        ("(3, 3) is…", "right 3 and up 3", ["right 0 up 3", "right 6", "left 3"], "Equal coordinates still use over-then-up."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, dist, expl in [
        ("To plot (4, 2) you…", "right 4, then up 2", ["up 4, then right 2", "right 2, up 4", "right 6"], "x then y."),
        ("(1, 6) is farthest in which direction from the origin?", "up", ["right", "left", "down"], "y=6 is a long way up; x is only 1."),
        ("Which point is farther right: (2, 9) or (7, 1)?", "(7, 1)", ["(2, 9)", "same", "(0, 0)"], "Compare x: 7 > 2."),
        ("Which point is higher: (2, 9) or (7, 1)?", "(2, 9)", ["(7, 1)", "same", "(0, 9)"], "Compare y: 9 > 1."),
        ("The pair (x, y) is called an…", "ordered pair", ["sum", "volume", "improper fraction"], "Order matters: (2, 5) ≠ (5, 2)."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, dist, expl in [
        ("A table: x=1, y=2; x=2, y=4; x=3, y=?", "6", ["5", "3", "9"], "y = 2x, so 2×3=6."),
        ("A table: x=0, y=1; x=1, y=3; x=2, y=?", "5", ["4", "2", "6"], "y goes up by 2 each time."),
        ("If y = x + 1 and x = 4, then y =", "5", ["4", "3", "1"], "4+1=5."),
        ("If y = 2x and x = 5, then y =", "10", ["7", "3", "25"], "2×5=10."),
        ("Points (1, 1), (2, 2), (3, 3) lie on a…", "diagonal line", ["horizontal line", "vertical line", "circle only"], "y = x."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    more = [
        ("Distance from (2, 3) to (2, 7) is…", "4", ["5", "2", "10"], "Same x. Subtract y: 7−3=4."),
        ("Distance from (1, 4) to (6, 4) is…", "5", ["4", "10", "1"], "Same y. Subtract x: 6−1=5."),
        ("(4, 1) vs (1, 4): they are…", "different points", ["the same point", "both the origin", "not ordered pairs"], "Order matters."),
        ("A map: library is (3, 2). From origin you go…", "right 3, up 2", ["right 2, up 3", "left 3", "up 5"], "x then y."),
        ("School is (0, 5). It is on the…", "y-axis", ["x-axis", "origin", "line y=x"], "x=0."),
        ("Park is (6, 0). It is on the…", "x-axis", ["y-axis", "origin", "line x=6 only as vertical"], "y=0."),
        ("From (3, 1) to (3, 5) you move…", "up 4", ["right 4", "up 2", "left 4"], "x stays 3."),
        ("From (2, 2) to (5, 2) you move…", "right 3", ["up 3", "right 2", "down 3"], "y stays 2."),
        ("The first number in (8, 0) tells you…", "how far right", ["how far up", "the volume", "the area"], "x-coordinate."),
        ("Which is the origin?", "(0, 0)", ["(1, 0)", "(0, 1)", "(1, 1)"], "Zero right, zero up."),
        ("Plotting (0, 0), then (1, 2), (2, 4): y is…", "double x", ["half x", "x + 4", "always 2"], "0, 2, 4 when x is 0, 1, 2."),
        ("If x=3 and the rule is y=x+4, y=?", "7", ["1", "12", "4"], "3+4=7."),
        ("A vertical grid line through (4, 0) also holds…", "(4, 2)", ["(2, 4)", "(0, 4)", "(5, 1)"], "Same x=4."),
        ("A horizontal grid line through (0, 3) also holds…", "(5, 3)", ["(3, 5)", "(3, 0)", "(0, 5)"], "Same y=3."),
        ("(2, 5) is 2 units right of…", "(0, 5)", ["(2, 0)", "(5, 2)", "(0, 0)"], "Keep y, set x=0."),
        ("Grade 5 graphing uses which quadrant?", "first (right and up)", ["all four", "left only", "down only"], "Both coordinates are 0 or positive."),
        ("The axes meet at…", "(0, 0)", ["(1, 1)", "(0, 1)", "(1, 0)"], "The origin."),
        ("To name a point you write…", "(x, y)", ["(y, x)", "{x, y}", "x + y"], "Parentheses, x first."),
        ("(9, 2) compared with (2, 9) is farther…", "right", ["up", "left", "down"], "Larger x."),
        ("A city block map with (4, 3) means…", "4 east, 3 north (on this grid)", ["7 blocks of volume", "4×3 area only", "the origin"], "Ordered pair as a location."),
    ]
    for text, ans, dist, expl in more:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    return _fill(qs, 80, lambda i: mq(
        f"If you go right {i % 5 + 1} and up 0, the point is…",
        f"({i % 5 + 1}, 0)",
        "y=0 means on the x-axis.",
        i,
        distractors=[f"(0, {i % 5 + 1})", f"({i % 5 + 1}, {i % 5 + 1})", "(0, 0)"],
    ))


def build_unit7():
    title = "Fifth Grade Math Unit 7: The Coordinate Plane"
    description = (
        "Name and plot ordered pairs in the first quadrant. Read axes, graph tables, and find grid distances."
    )

    c1 = concept_block(
        "1. Axes, origin, and ordered pairs",
        [
            "The coordinate plane is two number lines that cross.",
            "The horizontal number line is the x-axis. The vertical one is the y-axis.",
            "They meet at the origin: (0, 0).",
            "An ordered pair (x, y) names one point. Order matters: (2, 5) is not (5, 2).",
            "In fifth grade we use the first quadrant: right and up, so both numbers are 0 or positive.",
            "x tells you how far right. y tells you how far up.",
        ],
        coordinate_plane(title="A blank first-quadrant grid")
        + solved(1, "What do we call (0, 0)?",
                 ["x is 0 and y is 0.",
                  "That is where the axes meet.",
                  "The origin."],
                 "the origin")
        + matching(
            [("x-axis", "horizontal"), ("y-axis", "vertical"), ("(0, 0)", "origin"), ("(x, y)", "ordered pair")],
            vid="g5u7-c1-match",
        ),
        kid_tip("x then y", "Say 'over, then up' as you write (x, y). The first number is never 'up'."),
        1,
    )

    c2 = concept_block(
        "2. Plot points: over, then up",
        [
            "Start at the origin every time.",
            "Move right x units. Then move up y units. Mark the point.",
            "(4, 1) is 4 right and 1 up. (1, 4) is 1 right and 4 up. Different spots.",
            "If y is 0, you stay on the x-axis. If x is 0, you stay on the y-axis.",
            "Count the grid squares. Do not guess between lines unless the number is not a whole.",
            "Label the point with its pair so you can check later.",
        ],
        coordinate_plane(
            points=[(2, 5, "A (2, 5)"), (5, 2, "B (5, 2)"), (4, 4, "C (4, 4)")],
            title="Three points on the same grid",
            caption="A is up more. B is right more. C is equally over and up. (2, 5) is not the same as (5, 2).",
        )
        + solved(1, "How do you plot (4, 1)?",
                 ["Start at (0, 0).",
                  "Right 4 (x).",
                  "Up 1 (y).",
                  "Mark (4, 1)."],
                 "right 4, then up 1"),
        watch_out("Flipping the pair", "Going up first plots (y, x) by mistake. Always over, then up."),
        6,
    )

    c3 = concept_block(
        "3. Read a point from a grid",
        [
            "To name a plotted point, drop a line down to the x-axis to read x.",
            "Then go across to the y-axis to read y. Write (x, y).",
            "A point on the x-axis has y = 0. A point on the y-axis has x = 0.",
            "Which is farther right? Compare x. Which is higher? Compare y.",
            "(7, 1) is farther right than (2, 9). (2, 9) is higher.",
            "Practice until your eyes go over-then-up without thinking about it.",
        ],
        solved(1, "A point is 2 right of the origin and 5 up. Name it.",
               ["Right is x = 2.",
                "Up is y = 5.",
                "The point is (2, 5)."],
               "(2, 5)")
        + matching(
            [("(5, 0)", "on the x-axis"), ("(0, 3)", "on the y-axis"),
             ("(3, 3)", "on y = x"), ("(0, 0)", "origin")],
            vid="g5u7-c3-match",
        ),
        try_this("Finger path", "Put a finger on the origin. Slide right, then up. That path is the ordered pair."),
        11,
    )

    c4 = concept_block(
        "4. Graph a table of values",
        [
            "A rule can make pairs: if y = 2x, then x=1 → y=2, x=2 → y=4, x=3 → y=6.",
            "List the pairs in a table, then plot each pair as a point.",
            "When x goes up by 1 and y goes up by the same amount each time, the points line up.",
            "y = x + 1 gives (0, 1), (1, 2), (2, 3), (3, 4).",
            "Graphing a pattern is how algebra starts to look like geometry.",
            "If a point does not fit the line of the others, check the table.",
        ],
        solved(1, "The rule is y = 2x. What is y when x = 3? What point do you plot?",
               ["y = 2 × 3 = 6.",
                "The pair is (3, 6).",
                "Right 3, up 6."],
               "(3, 6)")
        + step_reveal(
            ["Write the rule.",
             "Pick x values (0, 1, 2, 3…).",
             "Compute y.",
             "Plot each (x, y)."],
            vid="g5u7-c4-steps",
        ),
        kid_tip("Table first", "Fill three or four rows before you plot. A table catches arithmetic slips."),
        16,
    )

    c5 = concept_block(
        "5. Distance on a grid",
        [
            "If two points have the same x, they sit on a vertical line. Subtract the y values.",
            "(2, 3) to (2, 7) is |7 − 3| = 4 units up.",
            "If two points have the same y, they sit on a horizontal line. Subtract the x values.",
            "(1, 4) to (6, 4) is 5 units right.",
            "Grade 5 distance on the plane stays on these grid lines (no diagonal shortcut formula yet).",
            "You can walk a city-block path: right, then up, counting squares.",
        ],
        solved(1, "How far is (2, 3) from (2, 7)?",
               ["The x-coordinates match, so it is a vertical segment.",
                "Subtract: 7 − 3 = 4.",
                "4 units."],
               "4 units")
        + matching(
            [("(2, 3) to (2, 7)", "4 up"), ("(1, 4) to (6, 4)", "5 right"),
             ("(0, 0) to (0, 5)", "5 up"), ("(0, 0) to (3, 0)", "3 right")],
            vid="g5u7-c5-match",
        ),
        watch_out("Diagonal counting as one step per square corner",
                  "On a diagonal you are changing x and y at once. In this unit, measure along the axes, one direction at a time."),
        21,
    )

    c6 = concept_block(
        "6. Maps and real grids",
        [
            "A classroom map, a park map, or a simple city grid can use (x, y) as an address.",
            "If the library is (3, 2), start at the origin on the map, go 3 east (right) and 2 north (up).",
            "School at (0, 5) is on the y-axis. Park at (6, 0) is on the x-axis.",
            "Agree on what one grid unit means: 1 block, 1 km, 1 tile on the floor.",
            "The same ordered-pair rules work whether the story is a treasure map or a science graph.",
            "Always check which axis is which. Maps should label x and y or east and north.",
        ],
        solved(1, "On a block map the museum is (4, 3). How do you walk from the origin?",
               ["x = 4 means 4 blocks right (east on this map).",
                "y = 3 means 3 blocks up (north).",
                "Right 4, then up 3."],
               "right 4, up 3")
        + try_this("Make a tiny map", "On paper, plot home (1, 1), school (5, 2), and the park (3, 4). Tell the path in ordered pairs."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Name axes, origin, and ordered pairs",
            "Plot points: over, then up",
            "Read points from a grid",
            "Graph a table from a rule",
            "Find horizontal and vertical distances",
            "Use grids as maps",
        ],
        body,
        practice_slots(31, 50),
    )
    return title, description, content, _u7_questions()


# ===========================================================================
# UNIT 8: Expressions and patterns
# ===========================================================================

def _u8_questions():
    qs = []
    idx = 1

    for text, ans, dist, expl in [
        ("3 + 4 × 2 = ?", "11", ["14", "10", "24"], "Multiply first: 4×2=8, then 3+8=11."),
        ("(3 + 4) × 2 = ?", "14", ["11", "10", "9"], "Parentheses first: 7×2=14."),
        ("10 − 3 × 2 = ?", "4", ["14", "7", "6"], "3×2=6, then 10−6=4."),
        ("(10 − 3) × 2 = ?", "14", ["4", "7", "16"], "7×2=14."),
        ("2 × (5 + 1) = ?", "12", ["11", "7", "8"], "2×6=12."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, dist, expl in [
        ("8 ÷ 2 × 4 = ?", "16", ["1", "8", "4"], "Left to right: 4×4=16."),
        ("8 ÷ (2 × 4) = ?", "1", ["16", "8", "4"], "2×4=8, then 8÷8=1."),
        ("5 + 5 + 5 = ?", "15", ["555", "10", "25"], "Three fives."),
        ("3² means…", "9", ["6", "32", "5"], "3×3=9. Grade 5 may see a small exponent as repeated multiply."),
        ("4 × 0 + 7 = ?", "7", ["28", "0", "11"], "4×0=0, then +7."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, dist, expl in [
        ("'3 more than a number n' as an expression:", "n + 3", ["3n", "n − 3", "3 − n"], "More than means add."),
        ("'twice a number n' is…", "2n", ["n + 2", "n²", "2 + 2 + n"], "Twice means ×2."),
        ("'5 less than n' is…", "n − 5", ["5 − n", "5n", "n + 5"], "Start with n, take 5 away."),
        ("'the product of 4 and n' is…", "4n", ["4 + n", "4 − n", "n/4"], "Product means multiply."),
        ("If n = 6, then n + 3 = ?", "9", ["18", "3", "6"], "6+3=9."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    for text, ans, dist, expl in [
        ("Pattern: 3, 6, 9, 12… next term?", "15", ["13", "14", "18"], "Add 3 each time."),
        ("Pattern: 2, 4, 8, 16… next term?", "32", ["18", "24", "20"], "Multiply by 2."),
        ("Two rules: x grows by 1, y = 2x. When x=4, y=?", "8", ["6", "5", "16"], "2×4=8."),
        ("Terms: 5, 8, 11, 14. The rule is…", "add 3", ["add 5", "multiply by 3", "add 2"], "Constant difference 3."),
        ("Starting at 1, add 4 four times. You land on…", "17", ["16", "20", "5"], "1+4+4+4+4=17."),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    more = [
        ("6 + 2 × 5 = ?", "16", ["40", "13", "17"], "2×5=10, then 6+10."),
        ("(6 + 2) × 5 = ?", "40", ["16", "13", "30"], "8×5=40."),
        ("20 − 4 × 3 = ?", "8", ["48", "16", "12"], "4×3=12, 20−12=8."),
        ("(20 − 4) × 3 = ?", "48", ["8", "16", "23"], "16×3=48."),
        ("12 ÷ 3 + 1 = ?", "5", ["3", "4", "12"], "4+1=5."),
        ("12 ÷ (3 + 1) = ?", "3", ["5", "4", "16"], "12÷4=3."),
        ("7 × (2 + 3) = ?", "35", ["17", "21", "13"], "7×5=35."),
        ("'n plus 8' when n=10?", "18", ["80", "2", "8"], "10+8=18."),
        ("'product of n and 5' when n=4?", "20", ["9", "1", "45"], "4×5=20."),
        ("If 2n + 1 = 9, a value that works for n is…", "4", ["9", "8", "3"], "2×4+1=9."),
        ("Pattern 40, 35, 30, 25… next?", "20", ["15", "26", "45"], "Subtract 5."),
        ("Pattern 1, 3, 9, 27… next?", "81", ["30", "36", "54"], "×3 each time."),
        ("x: 1,2,3  y: 4,5,6. The rule could be…", "y = x + 3", ["y = 3x", "y = x − 3", "y = 4x"], "Each y is 3 more than x."),
        ("x: 1,2,3  y: 2,4,6. The rule could be…", "y = 2x", ["y = x + 2", "y = x − 1", "y = 3x"], "y is double x."),
        ("Parentheses change 3+4×2 from 11 into 14 if you write…", "(3+4)×2", ["3+(4×2)", "3×4+2", "3+4+2"], "Force the add first."),
        ("1 + 2 × 3 + 4 = ?", "11", ["21", "13", "10"], "2×3=6, then 1+6+4=11."),
        ("5 × 3 − 5 = ?", "10", ["0", "15", "25"], "15−5=10."),
        ("5 × (3 − 1) = ?", "10", ["14", "15", "4"], "5×2=10. Same 10, different path."),
        ("Twice n plus 1, for n=7?", "15", ["14", "8", "71"], "2×7+1=15."),
        ("The expression 4n means…", "4 times n", ["4 plus n", "4 minus n", "n to the 4"], "A number against n means multiply."),
    ]
    for text, ans, dist, expl in more:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1

    return _fill(qs, 80, lambda i: mq(
        f"What is 2 × ({i % 7 + 1} + 0)?",
        2 * (i % 7 + 1),
        "Parentheses first, then multiply by 2.",
        i,
    ))


def build_unit8():
    title = "Fifth Grade Math Unit 8: Expressions and Patterns"
    description = (
        "Use parentheses and order of operations. Write simple expressions. Extend numerical patterns and connect them to graphs."
    )

    c1 = concept_block(
        "1. Parentheses first",
        [
            "Parentheses are a grouping symbol. Do whatever is inside them first.",
            "3 + 4 × 2 is 11 because you multiply first. (3 + 4) × 2 is 14 because the parentheses force the add first.",
            "The two answers are both correct for their own expressions. The parentheses change the problem.",
            "2 × (5 + 1) = 2 × 6 = 12. Without parentheses, 2 × 5 + 1 = 11.",
            "When you write an expression from a story, parentheses help you show what is grouped.",
            "If there are nested groups, start in the innermost pair.",
        ],
        solved(1, "Compare 3 + 4 × 2 and (3 + 4) × 2.",
               ["Without parentheses, × before +: 4×2=8, 3+8=11.",
                "With parentheses: 3+4=7, 7×2=14.",
                "Same digits, two different values."],
               "11 and 14")
        + matching(
            [("3+4×2", "11"), ("(3+4)×2", "14"), ("10−3×2", "4"), ("(10−3)×2", "14")],
            vid="g5u8-c1-match",
        ),
        kid_tip("The ( ) are a fence", "Finish everything inside the fence before you use that result outside."),
        1,
    )

    c2 = concept_block(
        "2. Order of operations",
        [
            "A common order: parentheses, then multiply and divide (left to right), then add and subtract (left to right).",
            "10 − 3 × 2 = 4, not 14. The multiply happens before the subtract.",
            "8 ÷ 2 × 4: there is no extra parentheses, so go left to right: 4 × 4 = 16.",
            "8 ÷ (2 × 4) = 1. The parentheses changed everything.",
            "4 × 0 + 7 = 7, not 0. Multiply first.",
            "This order is a shared agreement so everyone gets the same value from the same expression.",
        ],
        solved(1, "Evaluate 6 + 2 × 5.",
               ["Multiply first: 2 × 5 = 10.",
                "Then add: 6 + 10 = 16.",
                "Not 40 — that would be (6+2)×5."],
               "16")
        + step_reveal(
            ["Circle parentheses and do them.",
             "Do × and ÷ from left to right.",
             "Do + and − from left to right.",
             "Write the value."],
            vid="g5u8-c2-steps",
        ),
        watch_out("Always going left to right ignoring ×",
                  "3 + 4 × 2 is not 14. Multiply and divide bind more tightly than add and subtract, unless parentheses say otherwise."),
        6,
    )

    c3 = concept_block(
        "3. Write expressions from words",
        [
            "A letter like n can stand for a number we have not chosen yet. That letter is a variable.",
            "'3 more than n' is n + 3. 'Twice n' is 2n. '5 less than n' is n − 5.",
            "'The product of 4 and n' is 4n. Writing a number next to a letter means multiply.",
            "Watch the order on 'less than': 5 less than n is n − 5, not 5 − n.",
            "If n = 6, then n + 3 = 9. Substitute, then use order of operations.",
            "Expressions do not have equals signs. Equations do. 2n + 1 is an expression. 2n + 1 = 9 is an equation.",
        ],
        solved(1, "Write an expression for 'twice a number n, plus 1.' Then find the value when n = 7.",
               ["Twice n is 2n. Plus 1 is 2n + 1.",
                "Substitute 7: 2×7 + 1.",
                "14 + 1 = 15."],
               "2n + 1; when n=7 the value is 15")
        + matching(
            [("3 more than n", "n + 3"), ("twice n", "2n"),
             ("5 less than n", "n − 5"), ("product of 4 and n", "4n")],
            vid="g5u8-c3-match",
        ),
        try_this("Swap in a small number", "If the words feel foggy, try n = 10 and see whether your expression matches the English."),
        11,
    )

    c4 = concept_block(
        "4. Numerical patterns",
        [
            "A pattern follows a rule again and again.",
            "3, 6, 9, 12… add 3 each time. Next is 15.",
            "2, 4, 8, 16… multiply by 2 each time. Next is 32.",
            "40, 35, 30, 25… subtract 5. Next is 20.",
            "Name the rule in words, then generate the next two or three terms to prove you have it.",
            "Some problems give two patterns that work together — that is the bridge to graphing.",
        ],
        solved(1, "The pattern is 5, 8, 11, 14, … What is the rule, and what comes next?",
               ["Each term is 3 more than the one before.",
                "Rule: add 3.",
                "Next term: 17."],
               "add 3; next is 17")
        + matching(
            [("3, 6, 9, 12", "add 3"), ("2, 4, 8, 16", "×2"),
             ("40, 35, 30", "subtract 5"), ("1, 3, 9, 27", "×3")],
            vid="g5u8-c4-match",
        ),
        kid_tip("Check two steps", "A rule should work from the first term to the second and from the second to the third."),
        16,
    )

    c5 = concept_block(
        "5. Two rules and a graph",
        [
            "Sometimes x follows one rule (like 'add 1') and y follows another (like 'double x').",
            "Make a table: x = 1, 2, 3, 4 and y = 2, 4, 6, 8 when y = 2x.",
            "Each row is an ordered pair you can plot on the coordinate plane from Unit 7.",
            "If y = x + 3, the pairs are (1, 4), (2, 5), (3, 6). They form a line of points going up as you move right.",
            "The graph is a picture of the rule. The table is a list of the rule. The expression is the rule in symbols.",
            "When x=4 and y=2x, you plot (4, 8).",
        ],
        solved(1, "x grows 1, 2, 3, 4. y = 2x. What point do you plot when x = 4?",
               ["y = 2 × 4 = 8.",
                "The ordered pair is (4, 8).",
                "Right 4, up 8."],
               "(4, 8)")
        + step_reveal(
            ["Write the two rules.",
             "Build a table of x and y.",
             "Turn each row into (x, y).",
             "Plot. Look for a line of points."],
            vid="g5u8-c5-steps",
        ),
        try_this("Three representations", "Words, table, graph. If they disagree, one of them has a slip."),
        21,
    )

    c6 = concept_block(
        "6. Properties that make algebra easier",
        [
            "Commutative: 3 + 4 = 4 + 3 and 3 × 4 = 4 × 3. Order can swap for + and ×.",
            "Associative: (2 + 3) + 4 = 2 + (3 + 4). Grouping can change for + and ×.",
            "Distributive: 3 × (2 + 5) = 3×2 + 3×5. A factor outside a sum can be shared.",
            "These are not tricks. They are reasons you can rearrange expressions without changing the value.",
            "5 × (3 − 1) = 5×3 − 5×1 = 15 − 5 = 10, same as 5 × 2.",
            "You will use these constantly in middle school. Fifth grade is the handshake.",
        ],
        solved(1, "Use the distributive property to compute 5 × (3 + 2).",
               ["5×3 + 5×2.",
                "15 + 10 = 25.",
                "Check: 5 × 5 = 25."],
               "25")
        + matching(
            [("3+4 = 4+3", "commutative +"), ("3×4 = 4×3", "commutative ×"),
             ("3(2+5)=6+15", "distributive"), ("(2+3)+4 = 2+(3+4)", "associative +")],
            vid="g5u8-c6-match",
        ),
        watch_out("Swapping in subtraction", "7 − 2 is not 2 − 7. Commutative is for + and ×, not for − or ÷."),
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Use parentheses",
            "Follow order of operations",
            "Write expressions from words",
            "Extend numerical patterns",
            "Connect two rules to a graph",
            "Use commutative, associative, and distributive properties",
        ],
        body,
        practice_slots(31, 50),
    )
    return title, description, content, _u8_questions()


def build_master():
    return f"""
<h1>Fifth Grade Math</h1>
<p>This is a full fifth-grade math path. We use <strong>short, clear words</strong>, a few careful diagrams, and lots of practice. You are building a strong base for middle school.</p>
<p>You will work with decimals to the thousandths place, multi-digit operations, fractions (add, subtract, multiply, and divide unit fractions), volume of rectangular prisms, the coordinate plane, and introductory algebra: expressions, order of operations, and patterns. After each idea there are 5 quick questions. At the end of a unit there are 50 more. Hearts help you. Take your time.</p>
{page_break()}
<h2>The eight units</h2>
<ol>
<li>Unit 1 — Decimals to Thousandths</li>
<li>Unit 2 — Multi-Digit Operations</li>
<li>Unit 3 — Add and Subtract Fractions</li>
<li>Unit 4 — Multiply Fractions</li>
<li>Unit 5 — Divide Unit Fractions</li>
<li>Unit 6 — Volume</li>
<li>Unit 7 — The Coordinate Plane</li>
<li>Unit 8 — Expressions and Patterns</li>
</ol>
<p>Start with place value for tiny decimal pieces. Operations with whole numbers and decimals sit on that. Fractions are the heart of fifth grade. Volume brings in three dimensions. The coordinate plane and expressions open the door to algebra.</p>
{page_break()}
<h2>How to learn</h2>
<p>Line up decimal points. Make fraction bottoms match before you add. Multiply tops and bottoms when you multiply fractions. For volume, count cubes or use V = l × w × h. On a grid, go over, then up. In an expression, do parentheses, then × and ÷, then + and −.</p>
<p>If a question feels hard, try a smaller number first. Then come back. You are building number sense — a feeling for how numbers work.</p>
"""
