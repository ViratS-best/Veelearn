"""Sixth Grade Math units 5–8: four-quadrant plane, algebra, geometry, data — plus master page."""

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
    four_quadrant_plane,
    balance_scale,
    inequality_line,
    parallelogram_area,
    triangle_area,
    prism_net,
    volume_prism,
    dot_plot,
    histogram,
    box_plot,
    page_break,
    mq,
    renumber,
)


def _fill(qs, need, factory):
    while len(qs) < need:
        qs.append(factory(len(qs) + 1))
    return renumber(qs[:need])


# ===========================================================================
# UNIT 5: Four-quadrant coordinate plane
# ===========================================================================

def _u5_questions():
    qs = []
    idx = 1
    items = [
        ("Quadrant I has signs…", "(+, +)", ["(−, +)", "(−, −)", "(+, −)"], "Right and up."),
        ("Quadrant II has signs…", "(−, +)", ["(+, +)", "(−, −)", "(+, −)"], "Left and up."),
        ("Quadrant III has signs…", "(−, −)", ["(+, +)", "(−, +)", "(+, −)"], "Left and down."),
        ("Quadrant IV has signs…", "(+, −)", ["(+, +)", "(−, +)", "(−, −)"], "Right and down."),
        ("The origin is…", "(0, 0)", ["(1, 1)", "(0, 1)", "(1, 0)"], "Axes meet there."),
        ("Point (−3, 2) is in quadrant…", "II", ["I", "III", "IV"], "x negative, y positive."),
        ("Point (4, −1) is in quadrant…", "IV", ["I", "II", "III"], "x positive, y negative."),
        ("Point (−2, −5) is in quadrant…", "III", ["I", "II", "IV"], "Both negative."),
        ("Point (0, −3) lies on the…", "y-axis", ["x-axis", "origin only", "quadrant I"], "x = 0."),
        ("Point (5, 0) lies on the…", "x-axis", ["y-axis", "origin only", "quadrant II"], "y = 0."),
        ("To plot (−4, 1) you go…", "left 4, up 1", ["right 4, up 1", "left 4, down 1", "right 4, down 1"], "Negative x is left."),
        ("The reflection of (3, 2) across the y-axis is…", "(−3, 2)", ["(3, −2)", "(−3, −2)", "(2, 3)"], "x flips sign."),
        ("The reflection of (3, 2) across the x-axis is…", "(3, −2)", ["(−3, 2)", "(−3, −2)", "(2, 3)"], "y flips sign."),
        ("Distance from (2, −1) to (2, 4) is…", "5", ["3", "6", "2"], "Same x. |4 − (−1)| = 5."),
        ("Distance from (−3, 5) to (1, 5) is…", "4", ["8", "5", "2"], "Same y. |1 − (−3)| = 4."),
        ("(−2, 3) vs (3, −2): they are…", "different points", ["the same", "both origin", "both quadrant I"], "Order and signs both matter."),
        ("A point with x = 0 and y > 0 is…", "on the positive y-axis", ["quadrant I", "quadrant II", "origin"], "Up from origin."),
        ("From (0, 0) to (−5, 0) you move…", "left 5", ["right 5", "up 5", "down 5"], "Negative x."),
        ("Which quadrant is never used in grade-5-only graphing?", "II, III, and IV (grade 5 was I only)", ["only III", "none — grade 5 used all", "only the origin"], "Grade 6 opens all four."),
        ("The axes split the plane into…", "four quadrants", ["two halves only", "six regions", "circles"], "I, II, III, IV counterclockwise from top-right."),
        ("Plot (0, 0), then (−1, −1). You are in…", "quadrant III after the second point", ["still origin", "quadrant I", "quadrant IV"], "Both coordinates negative."),
        ("A map: west is −x, north is +y. A point west and north is…", "quadrant II", ["I", "III", "IV"], "(−, +)."),
        ("Vertices of a rectangle: (1,1), (1,−2), (−4,1), (−4,−2). Width?", "5", ["3", "4", "6"], "|1 − (−4)| = 5."),
        ("Same rectangle. Height?", "3", ["5", "2", "4"], "|1 − (−2)| = 3."),
        ("The point opposite (2, −3) through the origin is…", "(−2, 3)", ["(2, 3)", "(−2, −3)", "(3, −2)"], "Both signs flip."),
        ("If y = −x and x = 4, the point is…", "(4, −4)", ["(4, 4)", "(−4, 4)", "(−4, −4)"], "Quadrant IV."),
        ("Horizontal line y = −2 holds…", "(5, −2)", ["(−2, 5)", "(2, 0)", "(0, 2)"], "Every point has y = −2."),
        ("Vertical line x = −1 holds…", "(−1, 4)", ["(4, −1)", "(1, −4)", "(0, −1)"], "Every point has x = −1."),
        ("From (−2, −2) to (−2, 3) you move…", "up 5", ["down 5", "left 5", "right 5"], "y from −2 to 3."),
        ("An ordered pair is written…", "(x, y)", ["(y, x)", "{x, y}", "x + y"], "x first, even when negative."),
    ]
    for text, ans, dist, expl in items:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1
    return _fill(qs, 80, lambda i: mq(
        f"In which quadrant is ({-1 if i % 2 else 1}, {1 if i % 3 else -2})? Use I, II, III, or IV.",
        {(-1, 1): "II", (1, 1): "I", (-1, -2): "III", (1, -2): "IV"}[(-1 if i % 2 else 1, 1 if i % 3 else -2)],
        "Signs of (x, y) name the quadrant.",
        i,
        distractors=["I", "II", "III", "IV"],
    ))


def build_unit5():
    title = "Sixth Grade Math Unit 5: Four-Quadrant Coordinate Plane"
    description = (
        "Plot and read ordered pairs in all four quadrants. Reflect across axes and find grid distances."
    )
    c1 = concept_block(
        "1. Four quadrants",
        [
            "Grade 5 used the first quadrant: right and up. Grade 6 uses the whole plane.",
            "The axes cross at the origin (0, 0) and split the plane into four quadrants.",
            "I: (+, +) top-right. II: (−, +) top-left. III: (−, −) bottom-left. IV: (+, −) bottom-right.",
            "Negative x is left. Negative y is down.",
            "Points on an axis are not inside a quadrant. (5, 0) is on the x-axis. (0, −3) is on the y-axis.",
            "Say 'over, then up' still — but over can be left, and up can be down when the number is negative.",
        ],
        four_quadrant_plane(title="The four quadrants")
        + solved(1, "Which quadrant is (−3, 2) in?",
                 ["x is negative → left.",
                  "y is positive → up.",
                  "Left and up is quadrant II."],
                 "II")
        + matching(
            [("I", "(+, +)"), ("II", "(−, +)"), ("III", "(−, −)"), ("IV", "(+, −)")],
            vid="g6u5-c1-match",
        ),
        kid_tip("Signs first", "Before you count squares, look at the signs. They tell you the quadrant."),
        1,
    )
    c2 = concept_block(
        "2. Plot points in every quadrant",
        [
            "Start at the origin. Move x first (right if +, left if −). Then move y (up if +, down if −).",
            "(−4, 1): left 4, up 1. (4, −1): right 4, down 1.",
            "Count grid units. Label the point with its pair, including the minus signs.",
            "(−2, 3) is not (3, −2). Order still matters.",
            "A set of vertices can make a polygon that crosses axes. Plot carefully, then connect.",
            "If a point looks wrong, check whether you moved x and y in the right order.",
        ],
        four_quadrant_plane(
            points=[(3, 2, "A"), (-3, 2, "B"), (-2, -4, "C"), (4, -1, "D")],
            title="One point in each quadrant",
            caption="A is I, B is II, C is III, D is IV. Same grid, four sign patterns.",
        )
        + solved(1, "How do you plot (−4, 1)?",
                 ["Start at (0, 0).",
                  "Left 4 because x = −4.",
                  "Up 1 because y = 1."],
                 "left 4, up 1"),
        watch_out("Going down for a negative x", "Negative x is left, not down. Down is negative y."),
        6,
    )
    c3 = concept_block(
        "3. Reflect across an axis",
        [
            "A reflection across the y-axis flips the sign of x: (3, 2) → (−3, 2).",
            "A reflection across the x-axis flips the sign of y: (3, 2) → (3, −2).",
            "The point opposite through the origin flips both signs: (2, −3) → (−2, 3).",
            "Reflections keep distances to the axis the same. The image is a mirror.",
            "On a map, reflecting across a river drawn as an axis is the same idea.",
            "Check: the original and the image should be the same distance from the mirror line, on opposite sides.",
        ],
        four_quadrant_plane(
            points=[(3, 2, "P"), (-3, 2, "P′")],
            title="Reflect P(3, 2) across the y-axis",
            caption="P′ is (−3, 2). The y-axis is the mirror. Height stays 2. Left-right flips.",
        )
        + solved(1, "Reflect (3, 2) across the x-axis.",
                 ["The x-axis is the mirror.",
                  "x stays 3. y becomes −2.",
                  "(3, −2)."],
                 "(3, −2)")
        + matching(
            [("across y-axis", "flip x"), ("across x-axis", "flip y"),
             ("through origin", "flip both"), ("(3, 2) across y", "(−3, 2)")],
            vid="g6u5-c3-match",
        ),
        11,
    )
    c4 = concept_block(
        "4. Distance on a grid",
        [
            "If two points share an x, subtract the y-values and take the positive difference.",
            "(2, −1) to (2, 4): |4 − (−1)| = 5.",
            "If they share a y, subtract the x-values: (−3, 5) to (1, 5) is 4.",
            "A rectangle with vertices (1, 1), (1, −2), (−4, 1), (−4, −2) has width 5 and height 3.",
            "City-block paths still go along the grid: right/left, then up/down.",
            "Absolute value is the tool that makes 'difference' positive when negatives are involved.",
        ],
        solved(1, "How far is (2, −1) from (2, 4)?",
               ["Same x, so vertical segment.",
                "|4 − (−1)| = |5| = 5.",
                "5 units."],
               "5 units")
        + step_reveal(
            ["Do they share x or share y?",
             "Subtract those coordinates.",
             "Take the absolute value.",
             "Label units."],
            vid="g6u5-c4-steps",
        ),
        try_this("Draw the segment", "A vertical or horizontal line on the grid makes the count obvious."),
        16,
    )
    c5 = concept_block(
        "5. Horizontal and vertical lines",
        [
            "x = −1 is a vertical line. Every point on it has x-coordinate −1, like (−1, 4).",
            "y = −2 is a horizontal line. Every point on it has y-coordinate −2, like (5, −2).",
            "y = −x is a diagonal of points such as (4, −4) and (−3, 3).",
            "These equations are a first look at graphing relationships — Unit 6 will write more of them.",
            "If a table follows y = −x, the points fall on that diagonal.",
            "Name one more point on the line to prove you see the pattern.",
        ],
        four_quadrant_plane(
            points=[(-1, 4, "A"), (-1, -2, "B"), (-1, 0, "C")],
            title="The vertical line x = −1",
            caption="A, B, and C all have x = −1. They stack on a vertical line left of the y-axis.",
        )
        + solved(1, "Give a point on the line y = −2.",
                 ["Every point needs y = −2.",
                  "Pick a convenient x, say 5.",
                  "(5, −2)."],
                 "(5, −2) (any x works)"),
        21,
    )
    c6 = concept_block(
        "6. Maps with signed directions",
        [
            "Agree: east is +x, west is −x, north is +y, south is −y — or label your own map.",
            "A point west and north is quadrant II: (−, +).",
            "Treasure maps, city grids, and science graphs all use the same ordered pairs.",
            "A rectangle on a map has a width and height you can read from vertices in different quadrants.",
            "Keep the scale: one grid unit might be 1 km or 1 block.",
            "The origin is a landmark you choose: a town square, a lab, sea level crossed with a pier.",
        ],
        solved(1, "West is −x and north is +y. A cabin is west and north of camp (the origin). Which quadrant?",
               ["West → x negative.",
                "North → y positive.",
                "Quadrant II."],
               "II")
        + matching(
            [("east, north", "I"), ("west, north", "II"),
             ("west, south", "III"), ("east, south", "IV")],
            vid="g6u5-c6-match",
        ),
        26,
    )
    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Name the four quadrants",
            "Plot points with negative coordinates",
            "Reflect across axes",
            "Find horizontal and vertical distances",
            "Recognize x = a and y = b",
            "Use signed map directions",
        ],
        body,
        practice_slots(31, 50),
    )
    return title, description, content, _u5_questions()


# ===========================================================================
# UNIT 6: Expressions, equations, inequalities
# ===========================================================================

def _u6_questions():
    qs = []
    idx = 1
    items = [
        ("3x + 2x = ?", "5x", ["6x", "5x²", "3x2"], "Like terms: 3+2=5, keep x."),
        ("4n − n = ?", "3n", ["4", "5n", "4n²"], "4−1=3."),
        ("2(x + 4) = ?", "2x + 8", ["2x + 4", "x + 8", "2x + 6"], "Distribute 2."),
        ("The coefficient in 7y is…", "7", ["y", "1", "0"], "The number multiplied by the variable."),
        ("A constant in 3x + 5 is…", "5", ["3x", "3", "x"], "The term with no variable."),
        ("If x = 4, then 2x + 1 = ?", "9", ["8", "7", "5"], "8+1=9."),
        ("Solve x + 5 = 12.", "7", ["17", "5", "12"], "Subtract 5 from both sides."),
        ("Solve 3x = 18.", "6", ["15", "21", "3"], "Divide both sides by 3."),
        ("Solve x − 4 = 9.", "13", ["5", "36", "−4"], "Add 4 to both sides."),
        ("Solve x/2 = 7.", "14", ["3.5", "9", "5"], "Multiply both sides by 2."),
        ("Which is an equation?", "x + 3 = 11", ["x + 3", "11", "x +"], "An equation has an equals sign."),
        ("Which is an expression?", "2n + 1", ["2n + 1 = 9", "n = 4", "2 + 1 = 3"], "No equals sign."),
        ("x > 3 means x is…", "greater than 3", ["less than 3", "equal to 3", "3 only"], "Open ray to the right."),
        ("x ≥ 3 includes…", "3 and everything greater", ["only numbers > 3", "only 3", "numbers < 3"], "Filled circle at 3."),
        ("x < −1 is true for…", "−2", ["0", "1", "−1"], "−2 is left of −1."),
        ("If 2x + 1 = 9, then x = ?", "4", ["5", "8", "10"], "2x=8, x=4."),
        ("'5 more than n' is…", "n + 5", ["5n", "5 − n", "n − 5"], "Add 5."),
        ("'twice n minus 3' is…", "2n − 3", ["2(n − 3) only", "n − 6", "3 − 2n"], "Twice first, then minus."),
        ("Like terms have the same…", "variable part", ["coefficients only", "constants only", "exponents of 10"], "3x and 5x are like."),
        ("3x and 3y are…", "not like terms", ["like terms", "always equal", "constants"], "Different variables."),
        ("A solution of x + 2 = 6 is…", "4", ["8", "2", "6"], "4+2=6."),
        ("Which does NOT solve x + 2 = 6?", "5", ["4", "4.0", "8/2"], "5+2=7, not 6."),
        ("6 = 2x is the same as…", "x = 3", ["x = 8", "x = 4", "x = 12"], "Divide by 2."),
        ("To undo +7, you…", "subtract 7", ["add 7 more", "multiply by 7", "divide by 7"], "Inverse operations."),
        ("To undo ×5, you…", "divide by 5", ["subtract 5", "add 5", "multiply by 5"], "Keep the balance."),
        ("x + 3 > 5 means x > ?", "2", ["8", "3", "5"], "Subtract 3 from both sides (same direction)."),
        ("An open circle on 4 for x > 4 means…", "4 is not included", ["4 is included", "only 4", "x = 4"], "Greater than, not equal."),
        ("2(3 + x) when x=1 is…", "8", ["7", "5", "6"], "2×4=8."),
        ("Combine 2a + 5 + 3a − 1.", "5a + 4", ["5a + 6", "6a + 4", "5a − 4"], "2a+3a=5a, 5−1=4."),
        ("If n is a number of packs, 4n is…", "4 times as many", ["n plus 4", "n minus 4", "4 only"], "Coefficient 4."),
        ("Solve 2x + 1 = 9.", "4", ["8", "5", "10"], "Subtract 1, divide by 2."),
        ("Solve 5x − 2 = 18.", "4", ["16", "20", "3"], "Add 2, divide by 5."),
        ("Solve x/3 + 1 = 5.", "12", ["2", "4", "15"], "Subtract 1, multiply by 3."),
        ("Solve 4x + 3 = 19.", "4", ["16", "22", "5"], "4x=16."),
        ("Solve 3x − 5 = 10.", "5", ["15", "2", "8"], "3x=15."),
        ("Solve 2x − 1 = 11.", "6", ["12", "5", "10"], "2x=12."),
        ("A number times 2, plus 3, is 11. The number?", "4", ["7", "8", "14"], "2n+3=11."),
        ("Solve 6 = 2x + 2.", "2", ["4", "8", "1"], "4=2x."),
        ("Solve x/2 − 3 = 1.", "8", ["−4", "2", "4"], "x/2=4."),
        ("Solve 7x = 21.", "3", ["14", "28", "7"], "Divide by 7."),
        ("Undo +3 then ×2 by…", "subtract 3, then divide by 2", ["divide first", "add 3, then ×2", "subtract 2"], "Peel the last operation first."),
    ]
    for text, ans, dist, expl in items:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1
    return _fill(qs, 80, lambda i: mq(
        f"Solve 2x + 1 = {2 * (i % 8 + 2) + 1}.",
        i % 8 + 2,
        "Subtract 1, then divide by 2.",
        i,
        distractors=[2 * (i % 8 + 2) + 1, i % 8 + 3, (i % 8 + 2) * 2],
    ))


def build_unit6():
    title = "Sixth Grade Math Unit 6: Expressions, Equations, and Inequalities"
    description = (
        "Write and evaluate expressions, solve one-step and two-step single-variable equations, and graph simple inequalities."
    )
    c1 = concept_block(
        "1. Expressions and like terms",
        [
            "An expression is a combination of numbers, variables, and operations with no equals sign: 2n + 1.",
            "A coefficient is the number multiplied by a variable: 7 in 7y.",
            "A constant is a term with no variable: 5 in 3x + 5.",
            "Like terms have the same variable part. 3x + 2x = 5x. 3x and 3y are not like.",
            "The distributive property: 2(x + 4) = 2x + 8.",
            "Combining like terms is cleaning an expression so it is easier to evaluate or solve.",
        ],
        solved(1, "Simplify 3x + 2x + 5.",
               ["3x and 2x are like terms.",
                "3x + 2x = 5x.",
                "The 5 stays: 5x + 5."],
               "5x + 5")
        + matching(
            [("3x + 2x", "5x"), ("2(x + 4)", "2x + 8"),
             ("4n − n", "3n"), ("coefficient of 7y", "7")],
            vid="g6u6-c1-match",
        )
        + phet_box("expr"),
        kid_tip("Only like with like", "You can add 3 apples to 2 apples. You cannot mash apples and bananas into one pile and call it 5 apples."),
        1,
    )
    c2 = concept_block(
        "2. Write expressions from words",
        [
            "'5 more than n' is n + 5. 'Twice n minus 3' is 2n − 3.",
            "'5 less than n' is n − 5, not 5 − n.",
            "A number next to a letter means multiply: 4n is four times n.",
            "Parentheses show grouping: twice the quantity n minus 3 is 2(n − 3), which is different from 2n − 3.",
            "If n = 4, then 2n + 1 = 9. Substitute, then use order of operations.",
            "Expressions name a quantity. Equations (next) say two quantities are equal.",
        ],
        solved(1, "Write 'twice n minus 3,' then evaluate at n = 5.",
               ["Twice n is 2n. Minus 3 is 2n − 3.",
                "2×5 − 3 = 10 − 3 = 7.",
                "The value is 7."],
               "2n − 3; value 7 when n=5")
        + matching(
            [("5 more than n", "n + 5"), ("twice n", "2n"),
             ("5 less than n", "n − 5"), ("product of 4 and n", "4n")],
            vid="g6u6-c2-match",
        ),
        watch_out("Less than reversal", "5 less than n starts with n. It is n − 5."),
        6,
    )
    c3 = concept_block(
        "3. Equations keep a balance",
        [
            "An equation says two expressions are equal: x + 3 = 11.",
            "A solution is a number that makes the equation true. For x + 3 = 11, x = 8 because 8 + 3 = 11.",
            "Whatever you do to one side, do to the other, so the two sides stay equal.",
            "Undo addition with subtraction. Undo multiplication with division.",
            "Check by substituting your answer back in.",
            "x + 5 = 12 → subtract 5 → x = 7. 3x = 18 → divide by 3 → x = 6.",
        ],
        balance_scale("x + 3", "11", title="x + 3 = 11 stays balanced")
        + solved(1, "Solve x + 5 = 12.",
                 ["Subtract 5 from both sides.",
                  "x = 7.",
                  "Check: 7 + 5 = 12."],
                 "7")
        + solved(2, "Solve 2x + 1 = 9.",
                 ["Subtract 1: 2x = 8.",
                  "Divide by 2: x = 4.",
                  "Check: 2×4 + 1 = 9."],
                 "4")
        + step_reveal(
            ["Look at what is done to x.",
             "Do the inverse to both sides.",
             "Simplify.",
             "Substitute to check."],
            vid="g6u6-c3-steps",
        ),
        11,
    )
    c4 = concept_block(
        "4. One-step and two-step equations",
        [
            "x + a = b → subtract a. x − a = b → add a.",
            "ax = b → divide by a. x/a = b → multiply by a.",
            "x − 4 = 9 → x = 13. x/2 = 7 → x = 14.",
            "Two-step: undo add/subtract first, then undo multiply/divide. 2x + 1 = 9 → x = 4. 5x − 2 = 18 → x = 4. x/3 + 1 = 5 → x = 12.",
            "Fractions and decimals are allowed: the same inverse still works.",
            "If both sides are swapped, 6 = 2x is still x = 3.",
        ],
        solved(1, "Solve 3x = 18.",
               ["x is multiplied by 3.",
                "Divide both sides by 3.",
                "x = 6. Check: 3×6=18."],
               "6")
        + solved(2, "Solve 5x − 2 = 18.",
                 ["Add 2: 5x = 20.",
                  "Divide by 5: x = 4.",
                  "Check: 5×4 − 2 = 18."],
                 "4")
        + matching(
            [("x + 5 = 12", "x = 7"), ("3x = 18", "x = 6"),
             ("2x + 1 = 9", "x = 4"), ("x/3 + 1 = 5", "x = 12")],
            vid="g6u6-c4-match",
        ),
        try_this("Name the inverse out loud", "Say 'this equation adds 5, so I subtract 5 from both sides.'"),
        16,
    )
    c5 = concept_block(
        "5. Inequalities",
        [
            "An inequality compares with <, >, ≤, or ≥ instead of =.",
            "x > 3 means every number greater than 3. 3 itself is not included (open circle).",
            "x ≥ 3 includes 3 (filled circle) and everything to the right.",
            "x < −1 is true for −2, not for 0.",
            "You can still add or subtract on both sides. x + 3 > 5 becomes x > 2.",
            "Many numbers can be solutions. An equation usually has one; an inequality has a set.",
        ],
        inequality_line(">", 3, title="Graph of x > 3")
        + inequality_line("≥", 3, title="Graph of x ≥ 3",
                          caption="Filled circle at 3: 3 is a solution, and so is every number to the right.")
        + solved(1, "Does x = −2 satisfy x < −1?",
                 ["−2 is to the left of −1.",
                  "Left means less.",
                  "Yes, −2 < −1."],
                 "yes"),
        watch_out("Open vs filled", "Greater than (>) does not include the endpoint. Greater than or equal (≥) does."),
        21,
    )
    c6 = concept_block(
        "6. Algebra stories",
        [
            "Let n be the unknown. Translate, then solve.",
            "'A number plus 5 is 12' → n + 5 = 12 → n = 7.",
            "'Four packs cost $18' is not 4n = 18 if the story is price per pack — read carefully. If 4 packs cost $18 and packs are equal, 4n = 18, n = 4.50.",
            "Inequalities appear as 'at least,' 'more than,' 'no more than.'",
            "Define the variable in a sentence: 'Let x be the number of tickets.'",
            "A check in the original story is better than a check in the symbols alone.",
        ],
        balance_scale("4n", "18", title="Four equal packs cost $18")
        + solved(1, "A number plus 5 is 12. What is the number?",
                 ["n + 5 = 12.",
                  "n = 7.",
                  "7 + 5 = 12."],
                 "7")
        + step_reveal(
            ["Define the variable.",
             "Write an equation or inequality.",
             "Solve with inverse operations.",
             "Check in the story."],
            vid="g6u6-c6-steps",
        ),
        26,
    )
    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Simplify expressions and like terms",
            "Write expressions from words",
            "See equations as a balance",
            "Solve one-step and two-step equations",
            "Graph inequalities",
            "Translate algebra stories",
        ],
        body,
        practice_slots(31, 50),
    )
    return title, description, content, _u6_questions()


# ===========================================================================
# UNIT 7: Geometry — area, surface area, volume
# ===========================================================================

def _u7_questions():
    qs = []
    idx = 1
    items = [
        ("Area of a parallelogram, base 6, height 4?", "24", ["10", "20", "12"], "6×4=24."),
        ("Area of a triangle, base 6, height 4?", "12", ["24", "10", "18"], "½×6×4=12."),
        ("A triangle is half of a parallelogram with the same…", "base and height", ["perimeter", "volume", "angles always"], "That is why the ½ is there."),
        ("Area of a rectangle 5 by 9?", "45", ["14", "28", "54"], "5×9."),
        ("A right triangle with legs 3 and 4. Area?", "6", ["12", "7", "5"], "½×3×4=6."),
        ("Surface area of a rectangular prism 4×3×2?", "52", ["24", "48", "36"], "2(12+8+6)=2×26=52."),
        ("Volume of a 4×3×2 prism?", "24", ["52", "18", "9"], "lwh=24."),
        ("A net is…", "a 2-D unfolding of a 3-D solid", ["a ratio table", "a percent", "an integer"], "Faces laid flat."),
        ("A rectangular prism has how many faces?", "6", ["4", "8", "12"], "Front, back, left, right, top, bottom."),
        ("Volume units are…", "cubic", ["square", "linear only", "percent"], "Three dimensions."),
        ("Area units are…", "square", ["cubic", "degrees", "m/s"], "Two dimensions."),
        ("Decompose a polygon means…", "split it into rectangles and triangles", ["find its volume", "reflect it", "take absolute value"], "Add the piece areas."),
        ("Base 8, height 5, parallelogram area?", "40", ["13", "26", "20"], "8×5."),
        ("Triangle base 10, height 3. Area?", "15", ["30", "13", "7"], "½×10×3."),
        ("Cube edge 3. Volume?", "27", ["9", "18", "12"], "3×3×3."),
        ("Cube edge 3. Surface area?", "54", ["27", "18", "9"], "6×9=54."),
        ("V = 48, B = 12. Height?", "4", ["36", "60", "6"], "48÷12=4."),
        ("Missing height: triangle area 20, base 8. h=?", "5", ["160", "12", "2.5"], "½×8×h=20 → 4h=20."),
        ("A shape made of a 3×4 rectangle and a triangle base 4 height 3. Total area?", "18", ["12", "6", "24"], "12+6=18."),
        ("Lateral faces of a rectangular prism are…", "the four walls (not top/bottom)", ["only the top", "the volume", "the net only"], "Often rectangles."),
        ("2(lw+lh+wh) with l=5,w=2,h=3?", "62", ["30", "31", "10"], "2(10+15+6)=2×31."),
        ("If you double only the height of a 4×3×2 prism, volume becomes…", "48", ["24", "96", "12"], "Height 4: 4×3×4=48."),
        ("Area does not change if you…", "slide the parallelogram (same base and height)", ["change the height", "cut a piece off", "scale all lengths by 2"], "Shear keeps base and height."),
        ("A pentagon can be split into…", "triangles (and maybe a rectangle)", ["only cubes", "integers", "percents"], "Add those areas."),
        ("Units for surface area of a box in cm?", "square centimeters", ["cubic centimeters", "cm", "percent"], "Nets are 2-D."),
        ("Volume of a box 10×2×2?", "40", ["14", "20", "24"], "40 cubic units."),
        ("Triangle with base 7 and height 0 has area…", "0", ["7", "3.5", "1"], "No height, no area."),
        ("A net must fold to…", "the solid without extra overlap of faces", ["a number line", "a ratio", "a histogram"], "That's the test of a correct net."),
        ("B is base area. V = B × h. If B=15 and h=4, V=?", "60", ["19", "11", "30"], "Same as prisms in grade 5, still true."),
        ("Half of 24 square units (a parallelogram) as a triangle is…", "12 square units", ["24", "48", "6"], "½ the parallelogram."),
    ]
    for text, ans, dist, expl in items:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1
    return _fill(qs, 80, lambda i: mq(
        f"A parallelogram has base {i % 6 + 3} and height 4. Area?",
        4 * (i % 6 + 3),
        "Area = base × height.",
        i,
    ))


def build_unit7():
    title = "Sixth Grade Math Unit 7: Area, Surface Area, and Volume"
    description = (
        "Find area of triangles and parallelograms, use nets for surface area, and compute prism volume."
    )
    c1 = concept_block(
        "1. Area of a parallelogram",
        [
            "A parallelogram has two pairs of parallel sides.",
            "Area = base × height. The height is perpendicular to the base, not a slanted side.",
            "You can imagine shearing a parallelogram into a rectangle with the same base and height.",
            "Base 6 and height 4 → area 24 square units.",
            "If you only add base and height, you have mixed up perimeter thinking with area.",
            "Any side can be a base if you use the matching perpendicular height.",
        ],
        parallelogram_area(6, 4)
        + solved(1, "A parallelogram has base 6 and height 4. Find the area.",
                 ["Area = base × height.",
                  "6 × 4 = 24.",
                  "24 square units."],
                 "24 square units")
        + phet_box("area"),
        kid_tip("Height is straight down", "The dashed altitude, not the slanted edge, is the height."),
        1,
    )
    c2 = concept_block(
        "2. Area of a triangle",
        [
            "A triangle is half of a parallelogram with the same base and height.",
            "Area = ½ × base × height.",
            "Base 6 and height 4 → ½ × 24 = 12 square units.",
            "A right triangle can use the two legs as base and height: legs 3 and 4 → area 6.",
            "If you forget the ½, you have the parallelogram, not the triangle.",
            "The height must be perpendicular to the chosen base — it might sit outside an obtuse triangle.",
        ],
        triangle_area(6, 4)
        + solved(1, "Find the area of a triangle with base 6 and height 4.",
                 ["Area = ½ × 6 × 4.",
                  "½ × 24 = 12.",
                  "12 square units."],
                 "12 square units")
        + matching(
            [("parallelogram 6×4", "24"), ("triangle 6×4", "12"),
             ("right triangle 3 and 4", "6"), ("½ of 24", "12")],
            vid="g6u7-c2-match",
        ),
        6,
    )
    c3 = concept_block(
        "3. Decompose polygons",
        [
            "Irregular shapes can be split into rectangles and triangles you already know.",
            "Find each piece's area, then add.",
            "A 3-by-4 rectangle (12) plus a triangle base 4 height 3 (6) totals 18.",
            "Sometimes you subtract a missing corner instead of adding pieces.",
            "Sketch the split. Label bases and heights on the sketch.",
            "This is the same composition idea as volume of two prisms, but in 2-D.",
        ],
        solved(1, "A shape is a 3-by-4 rectangle attached to a triangle with base 4 and height 3. Total area?",
               ["Rectangle: 12.",
                "Triangle: ½×4×3=6.",
                "12+6=18 square units."],
               "18 square units")
        + step_reveal(
            ["Draw a split into known shapes.",
             "Find each area.",
             "Add (or subtract a hole).",
             "Keep square units."],
            vid="g6u7-c3-steps",
        ),
        try_this("Mark the extra height", "When a triangle sits on a rectangle, the triangle's height is the extra stick-out, not the whole figure's height."),
        11,
    )
    c4 = concept_block(
        "4. Nets and surface area",
        [
            "A net is a 2-D unfolding of a 3-D solid. For a rectangular prism, six rectangular faces.",
            "Surface area is the total of the faces. Formula: 2(lw + lh + wh).",
            "A 4-by-3-by-2 prism: 2(12 + 8 + 6) = 2×26 = 52 square units.",
            "A cube with edge 3: six faces of 9 → surface area 54. Volume is 27 — different measures.",
            "A correct net folds to the box without extra overlapping faces.",
            "Units are square, because you are covering, not filling.",
        ],
        prism_net(4, 3, 2)
        + solved(1, "Find the surface area of a 4×3×2 rectangular prism.",
                 ["Faces: 4×3=12, 4×2=8, 3×2=6.",
                  "Two of each: 2(12+8+6)=52.",
                  "52 square units."],
                 "52 square units"),
        watch_out("Reporting volume as surface area", "24 cubic units fills the box. 52 square units wraps the box. Ask: fill or wrap?"),
        16,
    )
    c5 = concept_block(
        "5. Volume of a prism",
        [
            "Volume still equals length × width × height, or base area × height.",
            "A 4×3×2 prism has volume 24 cubic units.",
            "If V = 48 and B = 12, then h = 4.",
            "Doubling only the height doubles the volume: 4×3×2=24 becomes 4×3×4=48.",
            "A cube of edge 3 has volume 27.",
            "Cubic units fill space. Keep them distinct from the square units on the net.",
        ],
        volume_prism(4, 3, 2)
        + solved(1, "A prism has base area 12 and height 4. Volume?",
                 ["V = B × h.",
                  "12 × 4 = 48.",
                  "48 cubic units."],
                 "48 cubic units")
        + matching(
            [("4×3×2 volume", "24"), ("4×3×2 surface area", "52"),
             ("cube edge 3 volume", "27"), ("cube edge 3 SA", "54")],
            vid="g6u7-c5-match",
        ),
        21,
    )
    c6 = concept_block(
        "6. Geometry stories",
        [
            "A park path as a parallelogram, a sail as a triangle, a shipping box as a prism.",
            "Read whether the question wants area (cover), surface area (wrap), or volume (fill).",
            "A missing height: triangle area 20, base 8 → ½×8×h=20 → h=5.",
            "Include units that match the measure.",
            "A sketch with labels is part of the work, not extra.",
            "If two shapes share a side, do not count that side twice in a perimeter — but this unit's focus is area and 3-D measures.",
        ],
        solved(1, "A triangular sail has area 20 square meters and base 8 m. What is the height?",
               ["½ × 8 × h = 20.",
                "4h = 20.",
                "h = 5 m."],
               "5 m")
        + step_reveal(
            ["Cover, wrap, or fill?",
             "Pick the formula.",
             "Substitute.",
             "Solve for the missing number.",
             "Write units."],
            vid="g6u7-c6-steps",
        ),
        26,
    )
    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Find parallelogram area",
            "Find triangle area",
            "Decompose polygons",
            "Use nets for surface area",
            "Compute prism volume",
            "Solve geometry stories",
        ],
        body,
        practice_slots(31, 50),
    )
    return title, description, content, _u7_questions()


# ===========================================================================
# UNIT 8: Data analysis
# ===========================================================================

def _u8_questions():
    qs = []
    idx = 1
    items = [
        ("A statistical question is one that…", "expects a variety of answers", ["has one exact number", "is never numeric", "cannot be graphed"], "How old are the students in this class?"),
        ("Which is statistical?", "How many pets do students in our class have?", ["How many minutes in an hour?", "What is 2+2?", "How many wheels on a bike?"], "You expect different numbers."),
        ("The mean is the…", "average (sum ÷ count)", ["middle value", "most frequent", "largest minus smallest"], "Balance point of the data."),
        ("Mean of 2, 4, 6?", "4", ["3", "6", "12"], "12÷3=4."),
        ("The median is the…", "middle value when ordered", ["average", "mode", "range"], "Order first."),
        ("Median of 1, 3, 8?", "3", ["1", "8", "4"], "Already ordered; middle is 3."),
        ("Median of 1, 3, 7, 8?", "5", ["3", "7", "4"], "Average of 3 and 7."),
        ("The mode is the…", "most frequent value", ["middle", "mean", "range"], "It can have more than one mode."),
        ("Mode of 2, 2, 3, 5?", "2", ["3", "5", "4"], "2 appears twice."),
        ("Range is…", "max − min", ["mean", "median", "sum"], "Spread from smallest to largest."),
        ("Range of 3, 10, 4?", "7", ["17", "4", "3"], "10−3=7."),
        ("A dot plot shows…", "each value as a dot", ["only the mean", "bins without dots", "a net of a cube"], "Stacks show repeats."),
        ("A histogram groups data into…", "intervals (bins)", ["exact dots only", "quadrants", "ratios"], "Bar height is the count in the bin."),
        ("A box plot shows…", "min, Q1, median, Q3, max", ["only the mean", "each individual dot", "surface area"], "Five-number summary."),
        ("Q1 is the…", "median of the lower half", ["smallest value", "mean", "range"], "25% of data at or below Q1."),
        ("Q3 is the…", "median of the upper half", ["largest value", "mode", "mean"], "75% of data at or below Q3."),
        ("IQR is…", "Q3 − Q1", ["max − min", "mean", "median"], "The width of the box."),
        ("Mean of 5, 5, 5, 9?", "6", ["5", "9", "24"], "24÷4=6."),
        ("If every value increases by 2, the mean…", "increases by 2", ["stays", "doubles", "drops by 2"], "The balance point shifts."),
        ("An outlier is…", "a value far from the others", ["the median always", "Q1", "the mode"], "It can pull the mean."),
        ("Which is more affected by an outlier?", "mean", ["median", "mode always", "the count of values"], "The mean uses every number, including the extreme."),
    ]
    items += [
        ("Data 1, 2, 2, 3. How many dots at 2?", "2", ["1", "3", "4"], "Two observations of 2."),
        ("A cluster on a dot plot is…", "a group of dots bunched together", ["a gap", "the range", "Q3"], "Where the data pile up."),
        ("A gap on a dot plot is…", "a stretch with no dots", ["the mean", "a bin", "Q1"], "Empty values between data."),
        ("Five-number summary needs…", "min, Q1, median, Q3, max", ["only mean and mode", "only range", "the net"], "That is what a box plot displays."),
        ("If the box is wide, the middle 50% is…", "more spread out", ["a single number", "the mode", "always 50 people"], "IQR is large."),
        ("Histogram bin 0–10 has 4 students, 10–20 has 7. Which bin is taller?", "10–20", ["0–10", "same", "cannot tell"], "7 > 4."),
        ("Mean of 0, 10, 20?", "10", ["30", "20", "0"], "30÷3=10."),
        ("Median of 0, 10, 20?", "10", ["0", "20", "15"], "Middle value."),
        ("Mode of 4, 4, 4, 7, 9?", "4", ["7", "9", "none"], "4 appears most."),
        ("Not a statistical question: 'How many inches in a foot?' because…", "there is one exact answer", ["it uses data", "it needs a histogram", "it has variability"], "No variability expected."),
    ]
    for text, ans, dist, expl in items:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1
    return _fill(qs, 80, lambda i: mq(
        f"What is the mean of {i % 5 + 1}, {i % 5 + 1}, {i % 5 + 7}?",
        (i % 5 + 1) + 2,
        "Add the three numbers and divide by 3.",
        i,
        distractors=[i % 5 + 1, i % 5 + 7, 3],
    ))


def build_unit8():
    title = "Sixth Grade Math Unit 8: Data Analysis"
    description = (
        "Ask statistical questions. Find mean, median, mode, and range. Read dot plots, histograms, and box plots."
    )
    c1 = concept_block(
        "1. Statistical questions",
        [
            "A statistical question expects variability — a spread of answers, not one fact.",
            "'How many pets do students in our class have?' is statistical. People differ.",
            "'How many minutes are in an hour?' is not. There is one exact answer.",
            "You collect data, then describe the distribution: shape, center, and spread.",
            "A good question names the group and the measure: students in this class, number of pets.",
            "If every person must give the same answer, you are not doing statistics yet.",
        ],
        solved(1, "Which is statistical: 'How many wheels on a bicycle?' or 'How many books did students read this month?'",
               ["Wheels on a bicycle: one typical answer, 2.",
                "Books read: students differ.",
                "The books question is statistical."],
               "How many books did students read this month?")
        + matching(
            [("pets in our class", "statistical"), ("minutes in an hour", "not statistical"),
             ("2 + 2", "not statistical"), ("hours of sleep last night", "statistical")],
            vid="g6u8-c1-match",
        ),
        kid_tip("Listen for variety", "If you can imagine different people giving different numbers, it is probably statistical."),
        1,
    )
    c2 = concept_block(
        "2. Mean, median, mode, range",
        [
            "Mean: add the values, divide by how many. 2, 4, 6 → 12/3 = 4. The mean is a balance point.",
            "Median: order the values, pick the middle. For an even count, average the two middles.",
            "Mode: the value that appears most. There may be more than one mode, or none that stands out.",
            "Range: maximum minus minimum. It is a simple measure of spread.",
            "An outlier (a far-away value) pulls the mean more than the median.",
            "If every value increases by 2, the mean and median increase by 2. The range stays the same.",
        ],
        solved(1, "For 1, 3, 7, 8 find the median.",
               ["Already ordered.",
                "Two middles: 3 and 7.",
                "Average: 5."],
               "5")
        + matching(
            [("mean", "sum ÷ count"), ("median", "middle when ordered"),
             ("mode", "most frequent"), ("range", "max − min")],
            vid="g6u8-c2-match",
        ),
        watch_out("Averaging without ordering for the median",
                  "Median is not the mean. Line the numbers up first, then take the middle."),
        6,
    )
    c3 = concept_block(
        "3. Dot plots",
        [
            "A dot plot shows each observation as a dot above a number line.",
            "A stack means that value happened more than once. Two dots at 2 means two people (or two trials) got 2.",
            "Look for clusters (piles), gaps (empty stretches), and outliers (lonely far dots).",
            "You can still find mean, median, mode, and range from the dots — they are the data.",
            "Dot plots are best when the values are discrete and not too many different numbers.",
            "Count the dots to know the sample size n.",
        ],
        dot_plot([1, 2, 2, 2, 3, 3, 5, 5, 5, 5, 6], title="Books read last month",
                 caption="Most students read 5 books (the tallest stack). There is a small gap at 4.")
        + solved(1, "On a dot plot of 1, 2, 2, 3, how many dots sit at 2?",
                 ["The value 2 appears twice.",
                  "Two dots stack at 2.",
                  "2 dots."],
                 "2"),
        try_this("Read shape first", "Before you compute, say: clustered on the right, a gap in the middle, one low outlier…"),
        11,
    )
    c4 = concept_block(
        "4. Histograms",
        [
            "A histogram groups values into intervals called bins. The bar height is how many land in that bin.",
            "Unlike a dot plot, you do not see each exact value — you see a range, like 10–20 pages.",
            "Taller bar means more data in that interval.",
            "Bin widths should be equal so the picture is fair.",
            "Use a histogram when there are many different values (heights in centimeters, times in seconds).",
            "You can still talk about center and spread, but the mean needs the original numbers or careful estimates from bins.",
        ],
        histogram(
            [("0–10", 3), ("10–20", 7), ("20–30", 5), ("30–40", 1)],
            title="Minutes of practice",
            caption="The 10–20 minute bin is the tallest. Most students practiced between 10 and 20 minutes.",
        )
        + solved(1, "Bin 0–10 has 4 students and bin 10–20 has 7. Which bar is taller?",
                 ["7 is more than 4.",
                  "The 10–20 bar is taller.",
                  "More students in 10–20."],
                 "10–20"),
        16,
    )
    c5 = concept_block(
        "5. Box plots and the five-number summary",
        [
            "The five-number summary is minimum, Q1, median, Q3, maximum.",
            "Q1 is the median of the lower half. Q3 is the median of the upper half.",
            "IQR = Q3 − Q1, the width of the box — the middle 50% of the data.",
            "Whiskers reach the min and max (in this course's simple box plots).",
            "A wide box means the middle 50% is spread out. A skinny box means the middle is packed.",
            "The median line inside the box is not always in the center of the box — that tells you skew.",
        ],
        box_plot(2, 4, 6, 9, 12, title="Five-number summary on a box plot",
                 caption="Min 2, Q1 4, median 6, Q3 9, max 12. The box from 4 to 9 is the middle half of the data.")
        + solved(1, "If Q1 = 4 and Q3 = 9, what is the IQR?",
                 ["IQR = Q3 − Q1.",
                  "9 − 4 = 5.",
                  "The middle 50% spans 5 units."],
                 "5")
        + matching(
            [("min", "left whisker tip"), ("Q1", "left edge of box"),
             ("median", "line inside box"), ("Q3", "right edge of box")],
            vid="g6u8-c5-match",
        ),
        21,
    )
    c6 = concept_block(
        "6. Choose a display and describe the data",
        [
            "Dot plot: few distinct values, you want to see every point.",
            "Histogram: many values, you want bins.",
            "Box plot: you want to compare center and spread quickly, or compare two groups.",
            "Always mention center (mean or median), spread (range or IQR), and shape (cluster, gap, outlier, skew).",
            "The mean can lie. One huge outlier drags it. Report the median too when the shape is lopsided.",
            "A sentence beats a lone number: 'Typical student read about 5 books; one student read 12, far above the cluster.'",
        ],
        solved(1, "Why might you prefer the median over the mean for house prices on a street with one mansion?",
               ["The mansion is an outlier.",
                "The mean gets pulled toward that huge price.",
                "The median stays with the typical houses."],
               "the median resists the outlier")
        + step_reveal(
            ["Name the variable and the group.",
             "Choose dot plot, histogram, or box plot.",
             "Find a center and a spread.",
             "Mention shape: cluster, gap, outlier.",
             "Write a sentence in context."],
            vid="g6u8-c6-steps",
        ),
        26,
    )
    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        [
            "Ask statistical questions",
            "Compute mean, median, mode, and range",
            "Read dot plots",
            "Read histograms",
            "Read box plots",
            "Describe data in context",
        ],
        body,
        practice_slots(31, 50),
    )
    return title, description, content, _u8_questions()


def build_master():
    return f"""
<h1>Sixth Grade Math</h1>
<p>This is a full sixth-grade math path. Sixth grade <strong>bridges elementary arithmetic and middle-school algebra</strong>. We use clear words, plenty of diagrams, and lots of practice.</p>
<p>You will work with ratios and rates, percents, rational numbers (including dividing fractions), integers, the four-quadrant coordinate plane, expressions and equations, geometry (area, surface area, volume), and data. After each idea there are 5 quick questions. At the end of a unit there are 50 more. Hearts help you. Take your time.</p>
{page_break()}
<h2>The eight units</h2>
<ol>
<li>Unit 1 — Ratios</li>
<li>Unit 2 — Unit Rates and Percents</li>
<li>Unit 3 — Rational Numbers (Fractions and Decimals)</li>
<li>Unit 4 — Integers and the Number Line</li>
<li>Unit 5 — Four-Quadrant Coordinate Plane</li>
<li>Unit 6 — Expressions, Equations, and Inequalities</li>
<li>Unit 7 — Area, Surface Area, and Volume</li>
<li>Unit 8 — Data Analysis</li>
</ol>
<p>Ratios open the year. Integers and the full coordinate plane stretch the number line in both directions. Algebra is a balance scale and a few inverse operations. Geometry wraps and fills boxes. Data asks questions that have many answers.</p>
{page_break()}
<h2>How to learn</h2>
<p>Draw the tape, the double number line, or the grid. Keep both sides of an equation equal. Height in area is perpendicular, not slanted. For data, say center, spread, and shape — not just one number.</p>
<p>If a question feels hard, try a smaller example first. Then come back. You are building the habits middle school will run on.</p>
"""
