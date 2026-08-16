"""Seventh Grade Math units 5–8: equations, circles, surface area, probability — plus master."""

from .common import (
    concept_block, solved, practice_slots, unit_shell, kid_tip, watch_out, try_this,
    step_reveal, matching, phet_box, balance_scale, inequality_line, circle_figure,
    angle_pair, scale_drawing, prism_net, volume_prism, spinner, probability_tree,
    two_box_plots, system_graph, page_break, mq, renumber,
)


def _fill(qs, need, factory):
    while len(qs) < need:
        qs.append(factory(len(qs) + 1))
    return renumber(qs[:need])


def _pack(items):
    return [mq(t, a, e, i, distractors=d) for i, (t, a, d, e) in enumerate(items, 1)]


def _u5_questions():
    items = [
        ("2x + 5 = 17. x = ?", "6", ["12", "22", "7"], "Subtract 5, divide by 2."),
        ("5x − 4 = 3x + 8. x = ?", "6", ["4", "12", "2"], "2x=12."),
        ("A system is…", "two equations with the same two unknowns", ["one equation", "only a graph with no numbers", "a percent"], "You need both true at once."),
        ("The solution of a 2-variable system is…", "an ordered pair (x, y)", ["only x", "only y", "a percent"], "One pair that fits both."),
        ("y = x + 1 and x + y = 5. The meeting point is…", "(2, 3)", ["(3, 2)", "(1, 5)", "(0, 5)"], "x=2, y=3."),
        ("Does (2, 3) solve x + y = 5?", "yes, 2+3=5", ["no", "only if y=2", "only if x=3"], "Plug in."),
        ("Does (1, 1) solve both y=x+1 and x+y=5?", "no", ["yes", "only the first", "only the second"], "1≠2, so it misses y=x+1."),
        ("y = 2x and x + y = 9. x = ?", "3", ["9", "6", "2"], "x+2x=9, x=3."),
        ("y = 2x and x + y = 9. y = ?", "6", ["3", "9", "18"], "y=2×3."),
        ("x + y = 10 and x − y = 2. x = ?", "6", ["8", "4", "12"], "Add: 2x=12."),
        ("x + y = 10 and x − y = 2. y = ?", "4", ["6", "8", "2"], "10−6=4."),
        ("If x = 2 in 2x + y = 7, y = ?", "3", ["5", "9", "11"], "4+y=7."),
        ("Substitution: from y=3x into x+y=8. x = ?", "2", ["8", "3", "5"], "x+3x=8."),
        ("Elimination: 2x+y=8 and 2x+3y=12. Subtract. y = ?", "2", ["4", "8", "1"], "2y=4."),
        ("After y=2 in 2x+y=8, x = ?", "3", ["6", "4", "10"], "2x=6."),
        ("Parallel lines (same slope, different intercepts) have…", "no solution", ["one solution", "infinitely many", "exactly two"], "They never meet."),
        ("The same line twice has…", "infinitely many solutions", ["no solution", "one solution", "x=0 only"], "Every point on the line works."),
        ("Two crossing lines have…", "exactly one solution", ["none", "infinitely many", "three"], "One meeting point."),
        ("3x + 2y = 12 and y = 3. x = ?", "2", ["3", "6", "9"], "3x+6=12."),
        ("Adult tickets $8, child $5, 3 adults and c children cost $34. c = ?", "2", ["5", "8", "4"], "24+5c=34."),
        ("x + 2y = 11, x = 3. y = ?", "4", ["8", "7", "14"], "3+2y=11."),
        ("2x − y = 5, y = x. x = ?", "5", ["2", "10", "0"], "2x−x=5."),
        ("x + y = 0, y = −3. x = ?", "3", ["−3", "0", "−6"], "x−3=0."),
        ("To substitute y=4x into 3x+y=20 you write…", "3x+4x=20", ["3x+y=4x", "y=20", "3+4=20"], "Replace y."),
        ("Add x+y=7 and x−y=1. You get…", "2x=8", ["2y=8", "2x=6", "x=7"], "y's cancel."),
        ("The pair (0, 5) on x+y=5 means…", "x=0 and y=5", ["x=5 and y=0", "both zero", "x=5"], "Order is (x, y)."),
        ("If 2x+3y=12 and x=0, y=?", "4", ["12", "6", "3"], "3y=12."),
        ("A graph solution is where the lines…", "cross", ["are parallel", "end", "turn into a circle"], "The shared point."),
        ("x=4, y=1. Check  x−y=3?", "yes, 4−1=3", ["no", "4+1=5", "only if y=4"], "It fits."),
        ("Two numbers sum to 12 and differ by 4. Larger?", "8", ["4", "6", "16"], "x+y=12, x−y=4."),
    ]
    return _fill(_pack(items), 55, lambda i: mq(
        f"y = 2x and x + y = {3 * (i % 6 + 2)}. What is x?",
        i % 6 + 2,
        "x + 2x is 3x. Divide the total by 3.",
        i,
        distractors=[2 * (i % 6 + 2), 3 * (i % 6 + 2), (i % 6 + 2) + 1],
    ))


def build_unit5():
    title = "Seventh Grade Math Unit 5: Multi-Step Equations and Inequalities"
    description = (
        "Solve multi-step one-variable equations, then systems of two equations in two variables "
        "by graphing, substitution, and elimination."
    )
    c1 = concept_block(
        "1. Multi-step one-variable equations",
        ["Undo in reverse order: peel addition/subtraction, then undo multiply/divide.",
         "2x + 5 = 17 → subtract 5 → 2x=12 → x=6.",
         "5x − 4 = 3x + 8 → subtract 3x → 2x − 4 = 8 → x=6.",
         "You need this skill before a system, because substitution turns two variables into one.",
         "Check by substituting. 2(6)+5 should be 17.",
         "Keep both sides balanced."],
        balance_scale("2x + 5", "17", title="2x + 5 = 17")
        + solved(1, "Solve 2x + 5 = 17.", ["Subtract 5: 2x=12.", "Divide by 2: x=6.", "Check: 12+5=17."], "6")
        + phet_box("expr"),
        kid_tip("One variable first", "A system will collapse to this kind of equation after you substitute."),
        1)
    c2 = concept_block(
        "2. What a system is",
        ["A system is two equations that must both be true, usually with x and y.",
         "A solution is an ordered pair (x, y) that works in both equations at the same time.",
         "Example: y = x + 1 and x + y = 5. The pair (2, 3) works: 3=2+1 and 2+3=5.",
         "(1, 1) fits neither both: 1 is not 1+1.",
         "On a graph, each equation is a line. The solution is where the two lines meet.",
         "Two crossing lines → one solution. Parallel → none. Same line → infinitely many."],
        system_graph()
        + solved(1, "y = x + 1 and x + y = 5. Find the solution pair.",
                 ["From the first, y is one more than x.", "Then x + (x+1) = 5, so 2x=4, x=2.",
                  "y=3. The pair is (2, 3)."], "(2, 3)")
        + matching([("solution of a system", "(x, y) pair"), ("two crossing lines", "one solution"),
                    ("parallel lines", "no solution"), ("same line twice", "infinitely many")], vid="g7u5-c2-match"),
        6)
    c3 = concept_block(
        "3. Substitution",
        ["If one equation already says y = …, plug that into the other equation.",
         "y = 2x and x + y = 9 → x + 2x = 9 → 3x = 9 → x = 3, y = 6.",
         "If you know x = 2 in 2x + y = 7, then 4 + y = 7, y = 3.",
         "You are turning two variables into one, then finishing with a one-variable equation.",
         "Always find both x and y. An answer that is only x is half-done.",
         "Check the pair in BOTH original equations."],
        solved(1, "Solve y = 2x and x + y = 9.",
               ["Replace y: x + 2x = 9.", "3x = 9, so x = 3.", "y = 2×3 = 6. Pair (3, 6)."], "(3, 6)")
        + step_reveal(["Solve one equation for a variable (or use it if it already is).",
                       "Substitute into the other equation.", "Solve the one-variable equation.",
                       "Back-substitute and check both originals."], vid="g7u5-c3-steps"),
        11)
    c4 = concept_block(
        "4. Elimination",
        ["Line the equations up. Add or subtract so one variable cancels.",
         "x + y = 10 and x − y = 2. Add: 2x = 12, so x = 6. Then y = 4.",
         "2x + y = 8 and 2x + 3y = 12. Subtract: 2y = 4, so y = 2. Then 2x + 2 = 8, x = 3.",
         "If the coefficients do not match, multiply one equation first so they do.",
         "Adding cancels opposites (y and −y). Subtracting cancels matching terms (2x and 2x).",
         "Write the ordered pair and check."],
        solved(1, "Solve x + y = 10 and x − y = 2.",
               ["Add to cancel y: 2x = 12.", "x = 6.", "6 + y = 10, so y = 4. Pair (6, 4)."], "(6, 4)")
        + watch_out("Stopping after one variable", "Elimination gives x or y first. You still owe the other coordinate."),
        16)
    c5 = concept_block(
        "5. How many solutions?",
        ["Graph picture: crossing, parallel, or stacked on the same line.",
         "After substitution or elimination, 3 = 3 with no variable left means infinitely many (same line).",
         "3 = 7 with no variable left means no solution (parallel, never meet).",
         "A leftover x = 4 means exactly one solution. Find y too.",
         "Two numbers that sum to 12 and differ by 4: x+y=12, x−y=4 → (8, 4).",
         "Always name the pair, or say none, or say infinitely many."],
        inequality_line(">", 5, title="One-variable reminder: x > 5 is a set, not a pair",
                        caption="Inequalities in one variable are rays. A 2-variable system solution is a point.")
        + solved(1, "Two lines have the same slope but different intercepts. How many solutions?",
                 ["Same steepness, shifted.", "They never meet.", "No solution."], "no solution"),
        21)
    c6 = concept_block(
        "6. Two-variable stories",
        ["Let x be adults and y be children, or let x and y be two unknown numbers.",
         "Adults 8 dollars, children 5 dollars: 3 adults and c children cost 34 dollars → 24 + 5c = 34 → c = 2.",
         "Sum 12 and difference 4 is a system: x+y=12, x−y=4.",
         "A graph check: does the story pair sit on both lines?",
         "Define both variables in sentences before you write equations.",
         "Finish with a pair that you can read back in words: 6 adults and 4 children, not just x=6."],
        balance_scale("x + y", "10", title="x + y = 10 is one equation; you still need a second")
        + solved(1, "Two numbers sum to 12 and differ by 4. What is the larger number?",
                 ["x+y=12 and x−y=4.", "Add: 2x=16, x=8.", "y=4. Larger is 8."], "8")
        + try_this("Two letters, two facts", "Each sentence in the story becomes one equation."),
        26)
    content = unit_shell(
        title,
        ["Multi-step one-variable equations", "What a system is", "Substitution",
         "Elimination", "How many solutions", "Two-variable stories"],
        c1 + c2 + c3 + c4 + c5 + c6, practice_slots(31, 25))
    return title, description, content, _u5_questions()


def _u6_questions():
    items = [
        ("Diameter is…", "2 × radius", ["half the radius", "πr²", "the area"], "d=2r."),
        ("Radius 5. Diameter?", "10", ["5", "15", "25"], "2×5."),
        ("C = 2πr. r=5, use 3.14. C≈?", "31.4", ["15.7", "78.5", "10"], "2×3.14×5."),
        ("A = πr². r=5, use 3.14. A≈?", "78.5", ["31.4", "15.7", "25"], "3.14×25."),
        ("r=10, use 3.14. C≈?", "62.8", ["31.4", "314", "20"], "2×3.14×10."),
        ("r=10, use 3.14. A≈?", "314", ["62.8", "31.4", "100"], "3.14×100."),
        ("Circumference is a…", "length around the circle", ["area inside", "radius", "volume"], "C=2πr."),
        ("Area of a circle is…", "π times radius squared", ["2πr", "πd", "2r"], "A=πr²."),
        ("d=14, r=?", "7", ["28", "14π", "21"], "Half of 14."),
        ("Supplementary angles add to…", "180°", ["90°", "360°", "45°"], "A straight line."),
        ("Complementary angles add to…", "90°", ["180°", "360°", "45°"], "A right angle."),
        ("110° and ? are supplementary.", "70°", ["20°", "90°", "250°"], "180−110."),
        ("35° and ? are complementary.", "55°", ["145°", "35°", "90°"], "90−35."),
        ("Vertical angles are…", "equal", ["supplementary always", "90°", "adjacent only"], "Across from each other."),
        ("Neighbors on a straight line add to…", "180°", ["90°", "equal", "360°"], "Adjacent supplementary."),
        ("A triangle's angles add to…", "180°", ["90°", "360°", "270°"], "Interior sum."),
        ("Angles 50° and 60° in a triangle. Third?", "70°", ["110°", "90°", "180°"], "180−110."),
        ("π is about…", "3.14", ["2.14", "4.14", "1.14"], "C/d for any circle."),
        ("If C=2πr and C=10π, r=?", "5", ["10", "20", "2π"], "2r=10."),
        ("A radius is a segment from…", "center to a point on the circle", ["side to side through center", "around the rim", "center to a square"], "Half a diameter."),
        ("Two vertical angles measure 40° and…", "40°", ["140°", "50°", "90°"], "They match."),
        ("Adjacent to 40° on a straight line?", "140°", ["40°", "50°", "90°"], "180−40."),
        ("A right triangle with 35°. Other acute?", "55°", ["145°", "90°", "35°"], "90−35."),
        ("Area uses r, not d, unless you write r=d/2. d=10, A≈?", "78.5", ["31.4", "314", "100"], "r=5."),
        ("Scale a radius ×2 and area…", "×4", ["×2", "×8", "stays"], "r²."),
        ("Scale a radius ×2 and circumference…", "×2", ["×4", "×8", "stays"], "C is linear in r."),
        ("A full turn is…", "360°", ["180°", "90°", "100°"], "Around a point."),
        ("If two lines cross and one angle is 80°, the opposite is…", "80°", ["100°", "10°", "180°"], "Vertical."),
        ("The adjacent to that 80° is…", "100°", ["80°", "10°", "360°"], "Supplementary."),
        ("r=7, use 22/7. C=?", "44", ["22", "154", "14"], "2×22/7×7=44."),
    ]
    return _fill(_pack(items), 55, lambda i: mq(
        f"A radius is {i % 6 + 2}. Diameter?",
        2 * (i % 6 + 2), "Diameter is twice the radius.", i))


def build_unit6():
    title = "Seventh Grade Math Unit 6: Circles and Angle Relationships"
    description = "Circumference and area of circles. Complementary, supplementary, and vertical angles."
    c1 = concept_block(
        "1. Radius, diameter, circumference",
        ["Radius r is center to rim. Diameter d = 2r goes all the way across.",
         "Circumference is the distance around. C = 2πr, or C = πd.",
         "π is a little more than 3. We often use 3.14, or 22/7 when r is a multiple of 7.",
         "r=5 → C ≈ 2×3.14×5 = 31.4. r=10 → C ≈ 62.8.",
         "r=7 with 22/7: C = 2×22/7×7 = 44.",
         "Circumference is a length, so the units are linear: cm, m, in."],
        circle_figure(5, show="both", title="Radius, diameter, and the rim")
        + solved(1, "Radius 5. Using 3.14, find C.", ["C=2πr.", "2×3.14×5=31.4.", "About 31.4 units."], "31.4"),
        kid_tip("d = 2r", "If a problem gives diameter, halve it before you use A=πr²."),
        1)
    c2 = concept_block(
        "2. Area of a circle",
        ["Area is the space inside. A = πr² — radius squared, then times π.",
         "r=5 → A ≈ 3.14×25 = 78.5 square units.",
         "r=10 → A ≈ 3.14×100 = 314.",
         "If you double r, circumference doubles, but area ×4, because of the square.",
         "Do not use diameter in r² unless you first write r=d/2.",
         "Area units are square: cm², m²."],
        circle_figure(5, show="area", title="Area uses r²",
                      caption="The shaded disk has area πr². For r=5 and π≈3.14, A≈78.5.")
        + solved(1, "Radius 5. Using 3.14, find area.", ["r²=25.", "3.14×25=78.5.", "78.5 square units."], "78.5")
        + matching([("C", "2πr"), ("A", "πr²"), ("d", "2r"), ("r=5, C≈", "31.4")], vid="g7u6-c2-match"),
        watch_out("Squaring 2r by mistake", "A is πr², not π(2r)² unless you really meant diameter as the radius."),
        6)
    c3 = concept_block(
        "3. Supplementary and complementary",
        ["Supplementary angles add to 180° — a straight line. 110° + 70° = 180°.",
         "Complementary angles add to 90° — a right angle. 35° + 55° = 90°.",
         "If one angle on a straight line is 40°, its neighbor is 140°.",
         "A right triangle with a 35° acute angle has the other acute 55°.",
         "These are relationships, not a type of triangle by themselves.",
         "Write 180 − known, or 90 − known."],
        angle_pair("supplementary")
        + angle_pair("complementary")
        + solved(1, "An angle is 110°. What is its supplement?", ["180−110=70.", "They make a straight line.", "70°."], "70°"),
        11)
    c4 = concept_block(
        "4. Vertical angles",
        ["When two lines cross, the angles across from each other are vertical. They are equal.",
         "The neighbors are adjacent and supplementary: they add to 180°.",
         "If one angle is 80°, the opposite is 80° and each neighbor is 100°.",
         "A full turn around the point is 360°.",
         "Vertical does not mean 'up and down.' It means 'across the vertex.'",
         "Mark equal angles with the same letter."],
        angle_pair("vertical")
        + solved(1, "Two lines cross. One angle is 80°. The opposite angle is…",
                 ["Vertical angles are equal.", "Opposite is also 80°.", "Neighbors are 100°."], "80°"),
        16)
    c5 = concept_block(
        "5. Angles in a triangle",
        ["The three interior angles of a triangle add to 180°.",
         "50° and 60° leave 70° for the third.",
         "A right triangle already used 90°, so the two acutes add to 90° (they are complementary).",
         "This pairs with the circle and line facts: 90, 180, 360 are the landmark sums.",
         "If a number would force a third angle of 0° or negative, the given measures cannot make a triangle.",
         "Sketch and label before you subtract from 180."],
        solved(1, "A triangle has angles 50° and 60°. The third?",
               ["Sum is 180°.", "50+60=110.", "180−110=70°."], "70°")
        + step_reveal(["Write the landmark sum (90, 180, or 360).", "Subtract the known pieces.",
                       "Name the relationship.", "Label degrees."], vid="g7u6-c5-steps"),
        21)
    c6 = concept_block(
        "6. Circle and angle stories",
        ["A wheel with radius 10 cm has C≈62.8 cm. That is one roll's distance.",
         "A circular rug with r=5 ft covers about 78.5 ft².",
         "A ramp angle of 35° has complement 55° if you need the other acute in a right triangle.",
         "Read whether the story wants around (C), inside (A), or a leftover angle.",
         "Using 3.14 is an approximation. Exact answers can stay in terms of π: C=10π when r=5.",
         "Keep square units on area and degree marks on angles."],
        solved(1, "A circular path has radius 10 m. Using 3.14, about how far is one lap?",
               ["That is circumference.", "2×3.14×10=62.8.", "About 62.8 m."], "62.8 m")
        + try_this("Name the measure", "Around, inside, leftover to 90, leftover to 180 — pick the formula from that word."),
        26)
    content = unit_shell(
        title,
        ["Radius, diameter, circumference", "Area of a circle", "Supplementary and complementary",
         "Vertical angles", "Angles in a triangle", "Circle and angle stories"],
        c1 + c2 + c3 + c4 + c5 + c6, practice_slots(31, 25))
    return title, description, content, _u6_questions()


def _u7_questions():
    items = [
        ("Scale factor 4. A 4 cm side becomes…", "16 cm", ["8 cm", "12 cm", "4 cm"], "4×4."),
        ("Scale 4. A 4-by-3 rectangle becomes…", "16 by 12", ["8 by 6", "4 by 12", "16 by 3"], "Each length ×4."),
        ("Corresponding lengths in similar figures…", "are proportional", ["are equal always", "add to 180", "are areas"], "Same scale factor."),
        ("Scale factor 1/2. A 10 in side becomes…", "5 in", ["20 in", "10 in", "2 in"], "Half as long."),
        ("If lengths ×k, areas ×…", "k²", ["k", "k³", "2k"], "Two dimensions."),
        ("Scale 4. Area 12 becomes…", "192", ["48", "16", "36"], "12×16."),
        ("A map scale 1 cm : 5 km. 4 cm on the map is…", "20 km", ["9 km", "5 km", "4 km"], "4×5."),
        ("A net is…", "a flat unfolding of a 3-D shape", ["the volume", "a circle", "an angle"], "All faces laid out."),
        ("A rectangular prism has how many faces?", "6", ["4", "8", "12"], "Top, bottom, and four sides."),
        ("SA of 4×3×2 prism?", "52", ["24", "48", "36"], "2(12+8+6)=52."),
        ("Volume of 4×3×2 prism?", "24", ["52", "18", "9"], "4×3×2."),
        ("Volume of a right prism is…", "B × h", ["2(lw+lh+wh)", "πr²", "2πr"], "Base area times height."),
        ("Surface area is measured in…", "square units", ["cubic units", "degrees", "only meters"], "Faces are 2-D."),
        ("Volume is measured in…", "cubic units", ["square units", "degrees", "π"], "Filling space."),
        ("Triangular base ½×6×4=12. Prism height 5. Volume?", "60", ["30", "15", "120"], "12×5."),
        ("A cube of edge 3. Volume?", "27", ["9", "18", "54"], "3³."),
        ("A cube of edge 3. SA?", "54", ["27", "9", "18"], "6×9."),
        ("Scale 2. A 5 cm drawing of a 10 cm object is…", "half size (scale 1/2)", ["double", "same", "scale 2"], "Drawing/actual=1/2."),
        ("Missing length: 3 cm corresponds to 12 cm. Scale?", "4", ["3", "9", "15"], "12÷3."),
        ("Paint the outside of a box. You need…", "surface area", ["volume", "circumference", "median"], "The faces."),
        ("Fill a tank. You need…", "volume", ["surface area", "scale factor", "probability"], "The space inside."),
        ("2(lw+lh+wh) with l=5, w=2, h=3?", "62", ["30", "31", "10"], "2(10+15+6)."),
        ("l=5, w=2, h=3. Volume?", "30", ["62", "10", "15"], "5×2×3."),
        ("A scale drawing keeps…", "shape, not always size", ["only color", "only area", "angles of 90 only"], "Similar figures."),
        ("If k=3, a 2-by-5 photo becomes…", "6 by 15", ["5 by 8", "3 by 5", "2 by 15"], "Each side ×3."),
        ("Nets that fold to a box cannot…", "have overlapping faces when folded", ["show all 6 faces", "be rectangles", "include a bottom"], "They must wrap without clash."),
        ("A right prism's sides are…", "rectangles standing on the base", ["circles", "only triangles", "curved"], "Height is perpendicular."),
        ("Double every edge of a cube. Volume ×?", "8", ["2", "4", "6"], "k³=8."),
        ("Double every edge of a cube. SA ×?", "4", ["2", "8", "6"], "k²=4."),
        ("1 in : 4 ft. A 6 in plan length is…", "24 ft", ["10 ft", "4 ft", "6 ft"], "6×4."),
    ]
    return _fill(_pack(items), 55, lambda i: mq(
        f"A rectangular prism is {i % 4 + 2} by 3 by 2. Volume?",
        (i % 4 + 2) * 3 * 2,
        "Volume is length × width × height.",
        i))


def build_unit7():
    title = "Seventh Grade Math Unit 7: Scale Drawings, Surface Area, and Volume"
    description = "Use scale factors. Find surface area from nets and volume of right prisms."
    c1 = concept_block(
        "1. Scale drawings",
        ["A scale drawing is the same shape, larger or smaller. Every length is multiplied by the same scale factor k.",
         "k=4 turns a 4-by-3 rectangle into a 16-by-12 rectangle. Corresponding sides stay in the same ratio.",
         "k=1/2 shrinks. A 10 in side becomes 5 in.",
         "Find k by dividing a new length by the matching old length: 12÷3=4.",
         "Maps use a scale such as 1 cm : 5 km. Four centimeters on the map means 20 km on the ground.",
         "Angles stay the same. That is why the copy still looks like the original."],
        scale_drawing("Scale factor 4", "The small 4-by-3 rectangle is copied with every length ×4. The large copy is 16 by 12.")
        + solved(1, "A sketch is 4 cm by 3 cm. Scale factor 4. What are the actual lengths?",
                 ["Multiply each length by 4.", "4×4=16 and 3×4=12.", "16 cm by 12 cm."], "16 by 12")
        + matching([("k=4, 4 cm", "16 cm"), ("k=1/2, 10 in", "5 in"), ("1 cm : 5 km, 4 cm", "20 km"),
                    ("12 cm from 3 cm", "k=4")], vid="g7u7-c1-match"),
        kid_tip("Same factor on every length", "Do not add 4. Multiply by 4."),
        1)
    c2 = concept_block(
        "2. Area and volume scale with powers of k",
        ["Lengths ×k. Areas ×k² because area has two dimensions.",
         "Scale 4: k²=16. An area of 12 becomes 12×16=192.",
         "Volumes ×k³. Double every edge of a cube (k=2) and volume ×8, surface area ×4.",
         "A photo 2 by 5 with k=3 becomes 6 by 15. The area goes from 10 to 90, which is ×9.",
         "If a drawing is half as long as the object, k=1/2, and the drawing's area is 1/4 of the object's area.",
         "Always ask: am I scaling a length, an area, or a volume?"],
        solved(1, "A rectangle has area 12. Scale factor 4. New area?",
               ["Areas scale by k².", "4²=16.", "12×16=192."], "192")
        + watch_out("Using k on area", "A scale of 4 on lengths is not ×4 on area. Square the scale factor first."),
        6)
    c3 = concept_block(
        "3. Nets and surface area",
        ["A net is a flat unfolding that folds into the 3-D shape with no overlapping faces.",
         "A rectangular prism has 6 rectangular faces: top, bottom, front, back, left, right.",
         "Surface area is the total of those face areas. SA = 2(lw + lh + wh).",
         "For 4×3×2: 2(12 + 8 + 6) = 2×26 = 52 square units.",
         "A cube of edge 3 has SA = 6×9 = 54.",
         "Painting a box, wrapping a gift, or covering with stickers all use surface area."],
        prism_net(4, 3, 2, title="Net of a 4 by 3 by 2 prism")
        + solved(1, "Find the surface area of a 4 by 3 by 2 rectangular prism.",
                 ["Faces: 4×3, 4×2, and 3×2.", "Those areas: 12, 8, and 6.", "2(12+8+6)=52."], "52")
        + phet_box("area"),
        11)
    c4 = concept_block(
        "4. Volume of a rectangular prism",
        ["Volume is how much space is inside. V = l × w × h.",
         "4×3×2 = 24 cubic units. You can picture 24 unit cubes stacked in the box.",
         "l=5, w=2, h=3 → V=30. SA of that same prism is 2(10+15+6)=62. Volume and surface area are different numbers.",
         "A cube of edge 3 has volume 27.",
         "Filling a tank, packing a crate, or pouring water uses volume.",
         "Keep cubic units on volume. Square units belong to surface area."],
        volume_prism(4, 3, 2)
        + solved(1, "A box is 4 by 3 by 2. What is its volume?",
                 ["Multiply the three edges.", "4×3=12.", "12×2=24 cubic units."], "24")
        + matching([("Fill a tank", "volume"), ("Paint the outside", "surface area"),
                    ("4×3×2 volume", "24"), ("4×3×2 SA", "52")], vid="g7u7-c4-match"),
        16)
    c5 = concept_block(
        "5. Volume of any right prism: V = B × h",
        ["A right prism has two matching bases and rectangular sides standing straight up.",
         "B is the area of one base. h is the height of the prism (the distance between the bases).",
         "A triangular base with base 6 and height 4 has B = ½×6×4 = 12. If the prism is 5 units long, V = 12×5 = 60.",
         "For a rectangular prism, B is already l×w, so V = (lw)×h, the same formula as before.",
         "The height in B for a triangle is the perpendicular height of the triangle, not the prism's length.",
         "Sketch the base first, find B, then multiply by the prism height."],
        solved(1, "A triangular prism has base ½×6×4 = 12 and prism height 5. Volume?",
               ["V = B × h.", "B is already 12.", "12×5=60."], "60")
        + step_reveal(["Draw the base.", "Find base area B.", "Multiply by the prism height.",
                       "Label cubic units."], vid="g7u7-c5-steps"),
        21)
    c6 = concept_block(
        "6. Choose scale, wrap, or fill",
        ["A plan that is 6 in long with scale 1 in : 4 ft means 24 ft in real life.",
         "If the story is wrapping, use surface area. If it is filling, use volume. If it is a drawing, use the scale factor on lengths.",
         "A 5 cm drawing of a 10 cm object has scale 1/2, not 2 — k is drawing ÷ actual when you describe the drawing.",
         "Doubling every edge of a cube multiplies volume by 8 and surface area by 4.",
         "Nets that cannot fold without overlapping faces are not nets of that prism.",
         "Write the formula, substitute, then name the unit type."],
        solved(1, "A plan uses 1 in : 4 ft. A wall is 6 in on the plan. How long is the wall?",
               ["Each inch stands for 4 feet.", "6×4=24.", "24 ft."], "24 ft")
        + try_this("Name the job", "Wrap, fill, or enlarge? That one word picks SA, volume, or scale."),
        26)
    content = unit_shell(
        title,
        ["Scale drawings", "How area and volume scale", "Nets and surface area",
         "Volume of a rectangular prism", "Any right prism: V = Bh", "Wrap, fill, or enlarge"],
        c1 + c2 + c3 + c4 + c5 + c6, practice_slots(31, 25))
    return title, description, content, _u7_questions()


def _u8_questions():
    items = [
        ("A sample is…", "a part of the population", ["the whole group", "always biased", "only the mean"], "Used to learn about everyone."),
        ("A fair four-section spinner. P(A)=?", "1/4", ["1/2", "1", "4"], "One of four equal parts."),
        ("P(event) = …", "favorable ÷ total", ["total ÷ favorable", "mean − median", "area × height"], "Count, then divide."),
        ("Two fair coins. P(both heads)=?", "1/4", ["1/2", "1", "0"], "(1/2)×(1/2)."),
        ("Independent events: P(A and B)=?", "P(A)×P(B)", ["P(A)+P(B)", "P(A)−P(B)", "1"], "Multiply along the tree."),
        ("P(not A) when P(A)=1/4?", "3/4", ["1/4", "1", "0"], "1 − 1/4."),
        ("Theoretical probability is from…", "equally likely outcomes", ["one lucky trial", "the median", "surface area"], "Count the sample space."),
        ("Experimental probability uses…", "what actually happened in trials", ["only a formula", "scale factor k", "πr²"], "Frequency ÷ trials."),
        ("Median of 2, 5, 7, 9, 11?", "7", ["5", "9", "6.8"], "The middle value."),
        ("Mean of 2, 4, 6, 8?", "5", ["4", "6", "20"], "20÷4."),
        ("IQR is…", "Q3 − Q1", ["max − min", "mean − median", "Q1 + Q3"], "The box width."),
        ("A box plot's middle line is the…", "median", ["mean", "mode", "range"], "Q2."),
        ("Group A median 8, Group B median 7. A is…", "typically higher", ["always larger every value", "more spread", "biased"], "Compare centers."),
        ("A longer box and whiskers means…", "more spread", ["a higher median always", "fewer people", "zero range"], "Variability."),
        ("Random sample is better because…", "every member had a chance", ["you pick only friends", "you skip half the list on purpose", "you use only the max"], "Less bias."),
        ("A spinner with 4 equal colors. P(red or blue)=?", "1/2", ["1/4", "1", "2"], "2/4."),
        ("P(H then T) on two coins?", "1/4", ["1/2", "3/4", "1"], "One of four paths."),
        ("Range of 3, 5, 7, 16?", "13", ["4", "7", "16"], "16−3."),
        ("Q1=6, Q3=11. IQR?", "5", ["17", "11", "6"], "11−6."),
        ("If 8 of 40 spins land on A, experimental P(A)≈?", "1/5", ["8", "40", "1/8"], "8/40=1/5."),
        ("A population is…", "the whole group you care about", ["one trial", "only the sample", "a spinner"], "The sample comes from it."),
        ("Compound independent: coin then spinner 1/4. P(H and A)=?", "1/8", ["1/4", "1/2", "5/4"], "(1/2)×(1/4)."),
        ("Outcomes HH, HT, TH, TT are…", "equally likely", ["all the same event", "impossible", "biased"], "Four paths of 1/4."),
        ("Comparing two classes, use…", "center and spread of both", ["only the tallest student", "only one mean", "a scale drawing"], "Two distributions."),
        ("A filled box from 6 to 11 means…", "the middle 50% lies there", ["everyone scored 6 or 11", "the mean is 6", "no outliers"], "Q1 to Q3."),
        ("P(sure event)=?", "1", ["0", "1/2", "2"], "It always happens."),
        ("P(impossible)=?", "0", ["1", "1/2", "−1"], "It never happens."),
        ("Mean is pulled by…", "extreme values", ["only the median", "scale factor", "vertical angles"], "Outliers tug the average."),
        ("A fair coin. P(heads)=?", "1/2", ["1/4", "1", "0"], "Two equally likely sides."),
        ("Tree diagrams help you…", "multiply along a path", ["find surface area", "solve 2x+5=17", "draw a circle"], "Each branch is a factor."),
    ]
    return _fill(_pack(items), 55, lambda i: mq(
        f"A fair spinner has {i % 3 + 2} equal sections. P(one marked section)?",
        f"1/{i % 3 + 2}",
        "One favorable out of equally likely sections.",
        i,
        distractors=["1", f"{i % 3 + 2}", f"1/{i % 3 + 3}"]))


def build_unit8():
    title = "Seventh Grade Math Unit 8: Statistics and Probability"
    description = "Compare two groups with center and spread. Find simple and compound independent probabilities."
    c1 = concept_block(
        "1. Samples, populations, and fair chance",
        ["A population is the whole group you care about. A sample is the part you actually measure.",
         "A random sample gives every member a chance to be picked. That cuts bias.",
         "Picking only friends, or only the front row, can tilt the results.",
         "Use a sample to infer about the population, then say how sure you are by looking at size and spread.",
         "Larger random samples tend to sit closer to the population story, but they are still not the whole group.",
         "Ask: who was left out?"],
        solved(1, "You want to know typical seventh-grade sleep hours at a school. Which sample is fairer?",
               ["Give every student a chance, not just one friend group.", "A random sample from the whole grade.",
                "Then report center and spread."], "a random sample of the grade")
        + watch_out("Sampling only the easy people", "A lunch table is a cluster of friends, not the whole school."),
        1)
    c2 = concept_block(
        "2. Center and spread",
        ["Mean is the balance point: add, then divide. 2, 4, 6, 8 → 20÷4=5.",
         "Median is the middle after you order the list. 2, 5, 7, 9, 11 → 7.",
         "Range is max − min. 3, 5, 7, 16 → 13. IQR is Q3 − Q1, the width of the middle half.",
         "A mean can be pulled by one extreme value. The median often holds still.",
         "Spread tells whether the group is tight or mixed. A long box and long whiskers mean more variability.",
         "Always name both a center and a spread. One number is not the whole story."],
        solved(1, "Find the median of 2, 5, 7, 9, 11.",
               ["Order is already done.", "The middle of five values is the third.", "7."], "7")
        + matching([("mean of 2,4,6,8", "5"), ("median of 2,5,7,9,11", "7"),
                    ("IQR", "Q3 − Q1"), ("range", "max − min")], vid="g7u8-c2-match"),
        6)
    c3 = concept_block(
        "3. Compare two groups",
        ["Put two box plots on the same scale. Compare medians (typical value) and IQR or whiskers (spread).",
         "Group A median 8 vs Group B median 7: A is typically a bit higher.",
         "If B's whisker stretches to 16 while A stops at 14, B has more extreme high values.",
         "Overlap is normal. 'Typically higher' is not 'every person is higher.'",
         "Write two sentences: one about center, one about spread.",
         "This is how you compare two classes, two sports, or two years of data."],
        two_box_plots("Two groups on one scale",
                      "Group A has median 8. Group B has median 7 and a longer high whisker. Compare both center and spread.")
        + solved(1, "Group A median is 8 and Group B median is 7. What can you say?",
                 ["Medians describe a typical value.", "8 is higher than 7.",
                  "A is typically higher; check spread separately."], "A is typically higher")
        + try_this("Two sentences", "First: which group is typically larger? Second: which is more spread out?"),
        11)
    c4 = concept_block(
        "4. Simple probability",
        ["P = (number of favorable outcomes) ÷ (number of equally likely outcomes).",
         "A fair four-color spinner: P(A)=1/4. P(red or blue)=2/4=1/2.",
         "P(not A) = 1 − P(A). If P(A)=1/4, then P(not A)=3/4.",
         "A sure event has probability 1. An impossible event has probability 0.",
         "Theoretical probability comes from the sample space. Experimental probability comes from trials: 8 A-lands in 40 spins is 8/40=1/5.",
         "A fair coin has P(heads)=1/2."],
        spinner(title="Four equal sections", caption="Each color is equally likely. P(any one color) = 1/4. P(two named colors) = 1/2.")
        + solved(1, "A fair spinner has four equal sections A, B, C, D. What is P(A)?",
                 ["Four equally likely outcomes.", "One favorable.", "1/4."], "1/4")
        + phet_box("plinko"),
        kid_tip("Count first", "Write favorable over total before you simplify."),
        16)
    c5 = concept_block(
        "5. Compound independent events",
        ["Independent means the first outcome does not change the second chance. Two coin flips are independent.",
         "P(A and B) = P(A)×P(B) when the events are independent.",
         "Two fair coins: P(both heads)=(1/2)×(1/2)=1/4. The four outcomes HH, HT, TH, TT are equally likely.",
         "A coin then a 1/4 spinner: P(heads and A)=(1/2)×(1/4)=1/8.",
         "A tree diagram shows every path. Multiply the fractions along a path. Add paths that match the event you want.",
         "Do not add the two probabilities when you need 'and' for independent events."],
        probability_tree("Two coin flips", "Four equally likely leaves. Each path multiplies to 1/4.")
        + solved(1, "Two fair coins. What is P(both heads)?",
                 ["Independent, so multiply.", "(1/2)×(1/2)=1/4.", "That is the HH leaf."], "1/4")
        + step_reveal(["List the sample space or draw a tree.", "Mark the favorable paths.",
                       "Multiply along a path.", "Add paths if more than one matches."], vid="g7u8-c5-steps"),
        21)
    c6 = concept_block(
        "6. Data and chance stories",
        ["A class comparison wants two box plots, not one lucky score.",
         "A game spinner wants a probability. If you spin many times, the experimental fraction should sit near the theoretical one.",
         "Mean is useful when values are bunched. Median is sturdier when one score is extreme.",
         "P(sure)=1 and P(impossible)=0 are landmarks, just like 90°, 180°, and 360° were for angles.",
         "Write the sample space in words: 'four spinner colors' or 'HH, HT, TH, TT.'",
         "Finish with a sentence: what the number means for the people or the game."],
        solved(1, "A coin, then a four-section spinner. P(heads and A)?",
               ["Independent events.", "(1/2)×(1/4)=1/8.", "One of eight equally likely combined outcomes."], "1/8")
        + watch_out("Adding instead of multiplying", "For independent 'and', multiply. Adding 1/2 + 1/4 would be a different question."),
        26)
    content = unit_shell(
        title,
        ["Samples and populations", "Center and spread", "Compare two groups",
         "Simple probability", "Compound independent events", "Data and chance stories"],
        c1 + c2 + c3 + c4 + c5 + c6, practice_slots(31, 25))
    return title, description, content, _u8_questions()


def build_master():
    return f"""
<h1>Seventh Grade Math</h1>
<p>This is a full seventh-grade math path. Seventh grade <strong>builds a bridge from arithmetic to early algebra</strong>. You will work with negative numbers, two-variable systems, unit rates and proportions, circle measure, surface area, and chance.</p>
<p>After each idea there are 5 quick questions. At the end of a unit there are 50 more. Hearts help you. Take your time.</p>
{page_break()}
<h2>The eight units</h2>
<ol>
<li>Unit 1 — Adding and Subtracting Negative Numbers</li>
<li>Unit 2 — Multiplying and Dividing Rational Numbers</li>
<li>Unit 3 — Proportional Relationships</li>
<li>Unit 4 — Percents</li>
<li>Unit 5 — Multi-Step Equations and Two-Variable Systems</li>
<li>Unit 6 — Circles and Angle Relationships</li>
<li>Unit 7 — Scale Drawings, Surface Area, and Volume</li>
<li>Unit 8 — Statistics and Probability</li>
</ol>
<p>Negatives stretch the number line. Proportions lock two quantities together. A system is two equations and one ordered pair. Circles bring π. Nets wrap boxes. Probability counts what can happen.</p>
{page_break()}
<h2>How to learn</h2>
<p>Hop on a number line. Keep both sides of an equation equal. Flip an inequality when you multiply by a negative. Use 3.14 for π unless a problem says otherwise. For chance, write favorable over total, then multiply along a tree for independent events.</p>
<p>If a question feels hard, try a smaller example first. Then come back. You are building the habits algebra will run on.</p>
"""


