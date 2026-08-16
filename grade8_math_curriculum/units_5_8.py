"""Eighth Grade Math units 5–8: complex systems, Pythagoras, data — plus master."""

from .common import (
    concept_block, solved, practice_slots, unit_shell, kid_tip, watch_out, try_this,
    step_reveal, matching, phet_box, balance_scale, system_graph, slope_line,
    pythag_triangle, scatter_plot, cylinder_figure, two_box_plots, page_break,
    four_quadrant_plane, mq, renumber,
)


def _fill(qs, need, factory):
    while len(qs) < need:
        qs.append(factory(len(qs) + 1))
    return renumber(qs[:need])


def _pack(items):
    return [mq(t, a, e, i, distractors=d) for i, (t, a, d, e) in enumerate(items, 1)]


def _u5_questions():
    items = [
        ("y = 2x − 1 and 2(x + 3) + 3y = 11. x = ?", "1", ["3", "2", "5"], "2x+6+6x−3=11, 8x=8."),
        ("Same system. y = ?", "1", ["−1", "2", "3"], "y=2(1)−1."),
        ("The solution of a 2-variable system is…", "an ordered pair", ["only x", "a slope", "a percent"], "(x, y)."),
        ("y = 3x + 1 and x + 2y = 16. x = ?", "2", ["16", "5", "3"], "x+6x+2=16, 7x=14."),
        ("Same system. y = ?", "7", ["6", "2", "16"], "3(2)+1."),
        ("3(y − 2) = x and x + y = 8. y = ?", "3.5", ["2", "8", "5"], "3y−6+y=8, 4y=14."),
        ("x = 4 − 2y and 3x + y = 7. y = ?", "1", ["4", "7", "−1"], "12−6y+y=7, −5y=−5."),
        ("Does (2, 3) solve 3x+2y=12 and 2x+5y=19?", "yes", ["no", "only the first", "only the second"], "6+6=12, 4+15=19."),
        ("Does (0, 0) solve 3x+2y=12?", "no", ["yes", "sometimes", "if y=6"], "0≠12."),
        ("y = −x + 5 and 2x − y = 4. x = ?", "3", ["5", "4", "1"], "2x−(−x+5)=4, 3x=9."),
        ("Same system. y = ?", "2", ["−2", "5", "8"], "−3+5."),
        ("Substitute y=4x − 3 into 2x + y = 15. x = ?", "3", ["15", "4", "6"], "2x+4x−3=15, 6x=18."),
        ("x/2 + y = 5 and x − 4y = −2. x = ?", "6", ["5", "2", "10"], "Clear halves, then eliminate."),
        ("Same system. y = ?", "2", ["6", "5", "−2"], "3+2=5."),
        ("If a system graphs as two crossing lines…", "one solution", ["none", "infinitely many", "two y-intercepts only"], "One point."),
        ("To substitute, you need…", "one variable isolated (or easy to isolate)", ["both already graphed", "three equations", "slope 0"], "Plug into the other."),
        ("2y = 6 − x plugged into 4x + 3y = 8, first write y as…", "y = 3 − x/2", ["y=6−x", "y=2x", "y=8"], "Divide by 2."),
        ("x = 2y + 1 and 3x − 6y = 8 has…", "no solution", ["(1, 0)", "infinitely many", "x=2"], "3(2y+1)−6y=8 → 6=8."),
        ("x = 2y + 1 and 3x − 6y = 3 has…", "infinitely many solutions", ["none", "(1, 0) only", "x=3"], "3(2y+1)−6y=3 → 3=3."),
        ("After substituting you must still find…", "the other variable", ["only m", "only b", "the domain"], "A pair, not a single number."),
        ("2(3x − y) = 10 and y = x + 1. x = ?", "3", ["5", "2", "4"], "6x−2(x+1)=10, 4x=12."),
        ("Same system. y = ?", "4", ["5", "6", "3"], "y=3+1."),
        ("Fractional: (x+y)/2 = 4 and y = x. x = ?", "4", ["8", "2", "0"], "x=4, y=4."),
        ("Check (1, 1) in y=2x−1?", "true, 2(1)−1=1", ["false", "undefined", "only if x=0"], "It sits on that line."),
        ("A story with two unknowns needs…", "two independent facts", ["one equation", "only a graph", "three variables"], "Two equations."),
        ("Isolate y in 2x + 4y = 12.", "y = 3 − x/2", ["y=12−2x", "y=3x", "y=2x+4"], "4y=12−2x."),
        ("If substitution yields 0=5, the system has…", "no solution", ["one solution", "infinitely many", "x=5"], "Contradiction."),
        ("If substitution yields 0=0, the system has…", "infinitely many solutions", ["none", "only (0,0)", "slope 0"], "Identity: same line."),
        ("3x − y = 7, y = x − 1. x = ?", "3", ["7", "4", "2"], "3x−(x−1)=7, 2x+1=7, 2x=6."),
        ("The pair that sits on both lines is…", "the solution", ["the slope", "the intercept only", "undefined"], "Intersection."),
    ]
    return _fill(_pack(items), 55, lambda i: mq(
        f"y = 2x and x + y = {3 * (i % 5 + 2)}. What is x?",
        i % 5 + 2,
        "x + 2x = 3x. Divide the total by 3.",
        i,
        distractors=[2 * (i % 5 + 2), 3 * (i % 5 + 2), (i % 5 + 2) + 1],
    ))


def build_unit5():
    title = "Eighth Grade Math Unit 5: Systems by Substitution"
    description = "Solve two-variable linear systems by substitution, including distribute, fractions, and special cases."
    c1 = concept_block(
        "1. A system is two equations, two unknowns",
        ["You still have only x and y — but both equations must be true at once.",
         "The solution is an ordered pair (x, y). On a graph it is where two lines meet.",
         "Seventh grade used friendly numbers. Eighth grade keeps two variables and adds distribute, fractions, and messy intercepts.",
         "Check a pair in BOTH originals. (2, 3) fits 3x+2y=12 and 2x+5y=19 because 6+6=12 and 4+15=19.",
         "(0, 0) almost never fits a system unless both constants are 0.",
         "If the lines are parallel, there is no pair. If they are the same line, every point on the line works."],
        system_graph()
        + solved(1, "Does (2, 3) solve 3x + 2y = 12 and 2x + 5y = 19?",
                 ["3(2)+2(3)=6+6=12. First equation holds.", "2(2)+5(3)=4+15=19. Second holds.",
                  "Yes: (2, 3) is the solution."], "yes")
        + phet_box("lines"),
        1)
    c2 = concept_block(
        "2. Substitute when y is already solved",
        ["If y = 2x − 1, replace every y in the other equation with 2x − 1.",
         "2(x + 3) + 3y = 11 and y = 2x − 1 → 2x + 6 + 3(2x − 1) = 11 → 2x + 6 + 6x − 3 = 11 → 8x = 8 → x = 1, y = 1.",
         "y = 3x + 1 and x + 2y = 16 → x + 2(3x + 1) = 16 → 7x + 2 = 16 → x = 2, y = 7.",
         "y = −x + 5 and 2x − y = 4 → 2x − (−x + 5) = 4 → 3x − 5 = 4 → x = 3, y = 2.",
         "Distribute the 3 or the minus before you combine.",
         "Always back-substitute to get the second coordinate."],
        solved(1, "Solve y = 2x − 1 and 2(x + 3) + 3y = 11.",
               ["Replace y: 2x + 6 + 3(2x − 1) = 11.", "2x + 6 + 6x − 3 = 11, so 8x + 3 = 11.",
                "8x = 8, x = 1, y = 1. Pair (1, 1)."], "(1, 1)")
        + step_reveal(["Isolate one variable if needed.", "Substitute into the other equation.",
                       "Solve the one-variable equation (distribute first).",
                       "Back-substitute and check both originals."], vid="g8u5-c2-steps"),
        kid_tip("Replace the whole expression", "If y = 2x − 1, write (2x − 1), not 2x, and not −1 alone."),
        6)
    c3 = concept_block(
        "3. Isolate first, then substitute",
        ["If neither equation is solved, pick the easier variable. 2x + 4y = 12 → y = 3 − x/2.",
         "x = 4 − 2y into 3x + y = 7: 3(4 − 2y) + y = 7 → 12 − 6y + y = 7 → y = 1, x = 2.",
         "3x − y = 7 and y = x − 1: 3x − (x − 1) = 7 → 2x + 1 = 7 → x = 3, y = 2.",
         "2(3x − y) = 10 and y = x + 1: 6x − 2(x + 1) = 10 → 6x − 2x − 2 = 10 → x = 3, y = 4.",
         "Watch the minus: 3x − (x − 1) is 3x − x + 1.",
         "Fractions: (x + y)/2 = 4 and y = x → x = 4, y = 4."],
        solved(1, "Solve x = 4 − 2y and 3x + y = 7.",
               ["3(4 − 2y) + y = 7.", "12 − 6y + y = 7, so −5y = −5, y = 1.",
                "x = 4 − 2 = 2. Pair (2, 1)."], "(2, 1)")
        + matching([("y=2x−1 into 2(x+3)+3y=11", "(1, 1)"), ("x=4−2y into 3x+y=7", "(2, 1)"),
                    ("y=x−1 into 3x−y=7", "(3, 2)"), ("y=x+1 into 2(3x−y)=10", "(3, 4)")],
                   vid="g8u5-c3-match"),
        11)
    c4 = concept_block(
        "4. Fractions inside a system",
        ["Clear a denominator before or after you substitute. x/2 + y = 5 and x − 4y = −2.",
         "Multiply the first by 2: x + 2y = 10. Pair with x − 4y = −2. Subtract: 6y = 12, y = 2, x = 6.",
         "Check: 6/2 + 2 = 5, and 6 − 8 = −2.",
         "A half in front of x is a 1/2 coefficient, not a comment.",
         "If both equations have denominators, multiply each by its own denominator.",
         "Finish with a pair. A fraction coordinate is allowed: y = 3.5 happened when 4y = 14."],
        solved(1, "Solve x/2 + y = 5 and x − 4y = −2.",
               ["×2 on the first: x + 2y = 10.", "Subtract x − 4y = −2: 6y = 12, y = 2.",
                "x + 4 = 10, x = 6. Pair (6, 2)."], "(6, 2)")
        + watch_out("Leaving a denominator in place", "Clear it. Then substitution or elimination is ordinary algebra."),
        16)
    c5 = concept_block(
        "5. No solution or infinitely many",
        ["x = 2y + 1 into 3x − 6y = 8: 3(2y + 1) − 6y = 8 → 6y + 3 − 6y = 8 → 3 = 8. False. No solution. Parallel lines.",
         "The same x = 2y + 1 into 3x − 6y = 3: 6y + 3 − 6y = 3 → 3 = 3. Always true. Infinitely many. Same line.",
         "0 = 5 means none. 0 = 0 means infinitely many. x = 4 means one (then find y).",
         "Same slope, different intercepts → none. Same slope and intercept → infinitely many.",
         "Do not invent a pair when the algebra has already spoken.",
         "Write the three-way label: one, none, or infinitely many."],
        slope_line(2, 1, title="Same slope, different intercepts never meet",
                   caption="y = 2x + 1 and y = 2x + 4 are parallel. Substitution would end as a false number sentence.")
        + solved(1, "x = 2y + 1 and 3x − 6y = 8. How many solutions?",
                 ["Substitute: 3(2y+1)−6y=8.", "6y+3−6y=8, so 3=8.", "Never true: no solution."], "no solution"),
        21)
    c6 = concept_block(
        "6. Two-unknown stories with substitution",
        ["Let x be adults and y be children, or let x and y be two unknown numbers.",
         "A number is 1 more than another and twice the first plus the second is 10: y = x + 1, 2x + y = 10 → 3x + 1 = 10 → x = 3, y = 4.",
         "That is the same system as 2(3x − y) = 10 with y = x + 1, just dressed as a sentence.",
         "Two plans: y = 2x + 3 and y = x + 6 meet when 2x + 3 = x + 6, x = 3, y = 9. After 3 miles both taxis cost 9 dollars.",
         "Define both letters. Write both facts. Substitute. Read the pair in words.",
         "Unit 6 will cancel variables by adding. Same pairs, different engine."],
        balance_scale("2x + y", "10", title="One equation is not enough; the second fact is y = x + 1")
        + solved(1, "A number y is 1 more than x, and 2x + y = 10. Find the pair.",
                 ["y = x + 1.", "2x + (x + 1) = 10, so 3x = 9, x = 3.", "y = 4. Pair (3, 4)."], "(3, 4)")
        + try_this("Two sentences, two equations", "If you only wrote one equation, you are not done."),
        26)
    content = unit_shell(
        title,
        ["Two equations, one pair", "Substitute a solved y", "Isolate, then substitute",
         "Fractions in a system", "None or infinitely many", "Stories"],
        c1 + c2 + c3 + c4 + c5 + c6, practice_slots(31, 25), "unit-5-substitution.mp4")
    return title, description, content, _u5_questions()


def _u6_questions():
    items = [
        ("3x + 2y = 12 and 2x + 5y = 19. x = ?", "2", ["12", "5", "3"], "×5 and ×2 so y coefficients match, then subtract."),
        ("Same system. y = ?", "3", ["2", "19", "4"], "3(2)+2y=12, y=3."),
        ("x + y = 10 and x − y = 2. Add to get…", "2x = 12", ["2y=12", "x=10", "y=2"], "y's cancel."),
        ("Then x = ?", "6", ["8", "4", "12"], "12/2."),
        ("Then y = ?", "4", ["6", "8", "2"], "10−6."),
        ("2x + 3y = −1 and 4x − y = 5. x = ?", "1", ["5", "2", "0"], "×3 on second, add to cancel y."),
        ("Same system. y = ?", "−1", ["1", "5", "3"], "4(1)−y=5, y=−1."),
        ("To cancel 2y and 4y you can…", "multiply the first equation by 2, then subtract", ["add as written", "divide y", "set y=0"], "Match coefficients."),
        ("3x + 2y = 16 and x − 2y = 0. Add. x = ?", "4", ["16", "8", "2"], "4x=16."),
        ("Same system. y = ?", "2", ["4", "0", "8"], "x=4, 4−2y=0."),
        ("2x + 4y = 10 and x + 2y = 5 are…", "the same line", ["parallel", "perpendicular", "one point only"], "Second ×2 is the first."),
        ("2x + 4y = 10 and x + 2y = 6 have…", "no solution", ["infinitely many", "(1, 2)", "(5, 0)"], "Parallel."),
        ("Multiply x + 3y = 7 by 2.", "2x + 6y = 14", ["2x+3y=14", "x+6y=14", "2x+6y=7"], "Every term."),
        ("Elimination needs…", "matching or opposite coefficients", ["a graph always", "three variables", "slope first"], "Then add or subtract."),
        ("3 adults at 8 dollars and 2 children at 5 dollars cost…", "34 dollars", ["13 dollars", "40 dollars", "16 dollars"], "24+10."),
        ("3a + 2c = 34 and a + 4c = 28. c = ?", "5", ["8", "4", "2"], "×3: 3a+12c=84, subtract, 10c=50."),
        ("Same system. a = ?", "8", ["5", "10", "6"], "a+20=28."),
        ("If adding gives 0=4, the system has…", "no solution", ["one pair", "infinitely many", "a=4"], "Contradiction."),
        ("If adding gives 0=0, the system has…", "infinitely many solutions", ["none", "only origin", "a=0"], "Same line."),
        ("5x − 2y = 4 and 3x + 2y = 12. Add. x = ?", "2", ["8", "16", "4"], "8x=16."),
        ("Same system. y = ?", "3", ["2", "12", "1"], "3(2)+2y=12."),
        ("Scaling an equation by 3 is…", "the same line, scaled", ["a new unrelated line", "changing the slope only", "illegal"], "Equals stay equal."),
        ("x − 2y = 3 and 3x − 6y = 9 has…", "infinitely many solutions", ["none", "(3, 0) only", "x=3 only"], "Second is 3× the first."),
        ("x − 2y = 3 and 3x − 6y = 10 has…", "no solution", ["infinitely many", "(3,0)", "x=10"], "3× first would be 9, not 10."),
        ("Best first move for 2x+3y=7 and 4x−y=5?", "multiply the second by 3, then add", ["guess (0,0)", "divide by 5", "graph only"], "3y and −3y."),
        ("After 11x = 22, x = ?", "2", ["11", "22", "33"], "Divide."),
        ("x + y = 14 and 2x + 3y = 31. y = ?", "3", ["14", "17", "8"], "2(14−y)+3y=31, y=3."),
        ("Use elimination when…", "coefficients are easy to match", ["y is already isolated", "there is only one equation", "the graph is a circle"], "Add or subtract."),
        ("The ordered pair is written…", "(x, y)", ["(y, x)", "x+y", "m, b"], "x first."),
        ("4x − 3y = 11 and 2x + 3y = 7. Add. x = ?", "3", ["18", "4", "1"], "6x=18."),
    ]
    return _fill(_pack(items), 55, lambda i: mq(
        f"x + y = {2 * (i % 5 + 3)} and x − y = 2. What is x?",
        i % 5 + 3 + 1,
        "Add: 2x is the even sum plus 2. Then divide by 2.",
        i,
        distractors=[2 * (i % 5 + 3), i % 5 + 3, (i % 5 + 3) - 1 if (i % 5 + 3) > 1 else 9],
    ))


def build_unit6():
    title = "Eighth Grade Math Unit 6: Systems by Elimination"
    description = "Solve two-variable systems by scaling and adding. Handle special cases and two-unknown stories."
    c1 = concept_block(
        "1. Add to cancel a variable",
        ["Line the equations up. Add or subtract so one variable disappears.",
         "x + y = 10 and x − y = 2. Add: 2x = 12, x = 6, y = 4.",
         "5x − 2y = 4 and 3x + 2y = 12. Add: 8x = 16, x = 2, y = 3.",
         "3x + 2y = 16 and x − 2y = 0. Add: 4x = 16, x = 4, y = 2.",
         "Opposites (2y and −2y) cancel when you add. Matches cancel when you subtract.",
         "Write the ordered pair and check both originals."],
        system_graph("Two lines, one pair", "Elimination finds the same meeting point a graph would show. Here (2, 3) sits on both lines.")
        + solved(1, "Solve x + y = 10 and x − y = 2.",
               ["Add: 2x = 12, so x = 6.", "10 − 6 = 4, so y = 4.", "Check: 6+4=10 and 6−4=2."], "(6, 4)")
        + matching([("add x+y=10 and x−y=2", "2x=12"), ("5x−2y=4 plus 3x+2y=12", "8x=16"),
                    ("same line twice", "infinitely many"), ("parallel lines", "no solution")],
                   vid="g8u6-c1-match"),
        1)
    c2 = concept_block(
        "2. Multiply first so coefficients match",
        ["If nothing cancels yet, multiply one or both equations.",
         "3x + 2y = 12 and 2x + 5y = 19. Multiply first by 5 and second by 2: 15x + 10y = 60 and 4x + 10y = 38. Subtract: 11x = 22, x = 2, y = 3.",
         "2x + 3y = −1 and 4x − y = 5. Multiply the second by 3: 12x − 3y = 15. Add to the first: 14x = 14, x = 1, y = −1.",
         "Multiply every term, including the constant.",
         "x + 3y = 7 multiplied by 2 is 2x + 6y = 14. Same line, just scaled.",
         "Pick the variable whose coefficients have a small common multiple."],
        solved(1, "Solve 3x + 2y = 12 and 2x + 5y = 19.",
               ["×5 and ×2 so both have 10y.", "15x+10y=60 and 4x+10y=38. Subtract: 11x=22, x=2.",
                "3(2)+2y=12, y=3. Pair (2, 3)."], "(2, 3)")
        + step_reveal(["Choose a variable to cancel.", "Multiply so coefficients match or oppose.",
                       "Add or subtract.", "Back-solve and check."], vid="g8u6-c2-steps"),
        kid_tip("Scale the whole equation", "If you ×3, the 7 on the right becomes 21 too."),
        6)
    c3 = concept_block(
        "3. Negatives and mixed signs",
        ["4x − 3y = 11 and 2x + 3y = 7. Add: 6x = 18, x = 3. Then 2(3)+3y=7, y = 1/3. A fraction pair is legal.",
         "Keep the minus attached to its term when you add.",
         "If you need −3y and already have +3y, add. If you have two +3y's, subtract or multiply by −1 first.",
         "Best first move for 2x+3y=7 and 4x−y=5: multiply the second by 3, then add (3y and −3y).",
         "A sign error here is the usual way to lose the solution.",
         "Check with the originals, not with a scaled copy only."],
        solved(1, "Solve 2x + 3y = −1 and 4x − y = 5.",
               ["×3 on the second: 12x − 3y = 15.", "Add to 2x+3y=−1: 14x=14, x=1.",
                "4(1)−y=5, y=−1. Pair (1, −1)."], "(1, −1)")
        + watch_out("Subtracting in the wrong order", "Write both scaled equations, then subtract the one that actually cancels."),
        11)
    c4 = concept_block(
        "4. Same line or parallel",
        ["2x + 4y = 10 and x + 2y = 5: the first is exactly 2 times the second. Infinitely many solutions.",
         "2x + 4y = 10 and x + 2y = 6: same slopes, different constants. 2×(x+2y=6) is 2x+4y=12, not 10. No solution.",
         "x − 2y = 3 and 3x − 6y = 9: same line. x − 2y = 3 and 3x − 6y = 10: parallel, none.",
         "After adding, 0=0 means infinitely many. 0=4 means none.",
         "Graph: stacked lines vs two rails that never meet.",
         "Do not list one sample point as 'the' answer when there are infinitely many — say infinitely many."],
        solved(1, "How many solutions: 2x + 4y = 10 and x + 2y = 6?",
               ["×2 on the second: 2x+4y=12.", "That cannot equal 2x+4y=10.", "No solution. Parallel."],
               "no solution"),
        16)
    c5 = concept_block(
        "5. Two-unknown money and mix stories",
        ["Adults a dollars 8, children c dollars 5. Three adults and two children cost 34 dollars: 3a+2c=34. One adult and four children cost 28: a+4c=28.",
         "×3 the second: 3a+12c=84. Subtract the first: 10c=50, c=5, a=8.",
         "x + y = 14 and 2x + 3y = 31 → y = 3, x = 11.",
         "Two tickets types, two snack mixes, two phone plans: same pattern.",
         "Let the letters be the counts, not the prices, or the other way around — but be consistent.",
         "Read the pair in words: 8-dollar adults and 5-dollar children, 3 and 2 of them."],
        solved(1, "3a + 2c = 34 and a + 4c = 28. Find a and c.",
               ["×3: 3a+12c=84.", "Subtract 3a+2c=34: 10c=50, c=5.", "a+20=28, a=8."], "a=8, c=5")
        + try_this("Label before you write", "'a is the adult price in dollars' saves a flipped pair."),
        21)
    c6 = concept_block(
        "6. Choose substitution or elimination",
        ["If y is already isolated, substitute (Unit 5). If coefficients are easy to match, eliminate.",
         "The pair should come out the same either way. That is your check.",
         "A graph is a third check: the meeting point should be that pair.",
         "Still only two variables. Harder arithmetic, not a third letter.",
         "When a story gives y = mx + b for two plans, set the y's equal — that is substitution in disguise.",
         "High school will add more variables. The two-variable engine stays the same."],
        solved(1, "x + y = 14 and 2x + 3y = 31. Prefer elimination or substitution, and find y.",
               ["From the first, x=14−y (easy isolate).", "2(14−y)+3y=31 → 28−2y+3y=31.",
                "y=3, x=11. Pair (11, 3)."], "y=3")
        + phet_box("eq"),
        26)
    content = unit_shell(
        title,
        ["Add to cancel", "Multiply first", "Negatives", "Same line or parallel",
         "Mix stories", "Pick a method"],
        c1 + c2 + c3 + c4 + c5 + c6, practice_slots(31, 25), "unit-6-elimination.mp4")
    return title, description, content, _u6_questions()


def _u7_questions():
    items = [
        ("In a right triangle, a² + b² = ?", "c²", ["c", "2c", "ab"], "c is the hypotenuse."),
        ("Legs 3 and 4. Hypotenuse?", "5", ["7", "12", "25"], "9+16=25."),
        ("Legs 5 and 12. Hypotenuse?", "13", ["17", "60", "169"], "25+144=169."),
        ("Legs 6 and 8. Hypotenuse?", "10", ["14", "48", "100"], "Scaled 3-4-5."),
        ("Legs 8 and 15. Hypotenuse?", "17", ["23", "120", "289"], "64+225=289."),
        ("Hypotenuse 13, one leg 5. Other leg?", "12", ["8", "18", "65"], "169−25=144."),
        ("The hypotenuse is…", "the side opposite the right angle", ["a leg next to the right angle", "always 5", "the shortest side"], "Longest side."),
        ("3, 4, 5 is a right triangle because…", "9+16=25", ["3+4=5", "3×4=12", "angles add to 90"], "Converse of Pythagoras."),
        ("2, 3, 4 is a right triangle?", "no", ["yes", "only if scaled", "sometimes"], "4+9=13, not 16."),
        ("Distance from (1, 2) to (4, 6)?", "5", ["5 units on a slant", "7", "12"], "Δx=3, Δy=4."),
        ("Distance from (0, 0) to (6, 8)?", "10", ["14", "48", "2"], "Another 3-4-5 scaled."),
        ("Distance from (0, 0) to (5, 12)?", "13", ["17", "60", "7"], "5-12-13."),
        ("Vertical distance from (2, 3) to (2, 8)?", "5", ["0", "10", "13"], "Same x, |8−3|."),
        ("Distance on the plane is…", "Pythagoras on Δx and Δy", ["just x1+x2", "slope", "area"], "A right triangle of run and rise."),
        ("Legs 1 and 1. Hypotenuse?", "√2", ["2", "1", "√1"], "1+1=2."),
        ("A 6-8-10 triangle is…", "a scaled 3-4-5", ["not right", "equilateral", "a 5-12-13"], "×2."),
        ("If a²+b²=c², the triangle is…", "right", ["acute always", "obtuse always", "equilateral"], "Converse."),
        ("Cylinder volume formula?", "V = πr²h", ["2πr", "πr²", "πdh"], "Circle base times height."),
        ("Use 3.14. r=2, h=5. Volume?", "62.8", ["31.4", "15.7", "10"], "3.14×4×5."),
        ("Use 3.14. r=3, h=4. Volume?", "113.04", ["37.68", "12", "75.36"], "3.14×9×4."),
        ("Diameter 6 so r = ?", "3", ["6", "12", "π"], "Half the diameter."),
        ("Use 3.14. diameter 6, h=5. Volume?", "141.3", ["282.6", "94.2", "30"], "3.14×9×5."),
        ("r=5, h=2, π=3.14. Volume?", "157", ["31.4", "78.5", "10"], "3.14×25×2."),
        ("r=1, h=10, π=3.14. Volume?", "31.4", ["3.14", "10", "62.8"], "3.14×1×10."),
        ("Volume of a cylinder is measured in…", "cubic units", ["square units", "degrees", "only π"], "Filling space."),
        ("The right-angle mark sits…", "between the two legs", ["on the hypotenuse", "at the midpoint of c", "outside the triangle"], "Legs meet at 90°."),
        ("A ladder 13 ft, wall 12 ft. Ground distance?", "5 ft", ["1 ft", "25 ft", "13 ft"], "169−144=25."),
        ("(−1, 4) to (2, 8). Distance?", "5", ["7", "3", "11"], "Δx=3, Δy=4."),
        ("If you only know three side lengths, Pythagoras tells you…", "whether the triangle is right", ["the area only", "the slope", "π"], "Check a²+b² against c²."),
        ("r=4, h=3, π=3.14. Volume?", "150.72", ["37.68", "12", "75.36"], "3.14×16×3."),
    ]
    return _fill(_pack(items), 55, lambda i: mq(
        f"A right triangle has legs {3 * (i % 5 + 1)} and {4 * (i % 5 + 1)}. Hypotenuse?",
        5 * (i % 5 + 1),
        "This is a 3-4-5 triangle scaled by a whole number.",
        i,
        distractors=[
            3 * (i % 5 + 1) + 4 * (i % 5 + 1),
            9 * (i % 5 + 1),
            (3 * (i % 5 + 1)) * (4 * (i % 5 + 1)),
        ],
    ))


def build_unit7():
    title = "Eighth Grade Math Unit 7: Pythagorean Theorem and Cylinders"
    description = "Use a²+b²=c², distance on the plane, and cylinder volume V=πr²h with π≈3.14."
    c1 = concept_block(
        "1. a² + b² = c²",
        ["A right triangle has one 90° angle. The two sides that make that angle are legs a and b. The side across from 90° is the hypotenuse c — always the longest.",
         "Pythagoras: a² + b² = c². Legs 3 and 4: 9+16=25, so c=5. That 3-4-5 family shows up all year.",
         "5 and 12: 25+144=169=13². 8 and 15: 64+225=289=17². 7 and 24: 49+576=625=25².",
         "If you know c and one leg: subtract, then take a square root. Hypotenuse 13, leg 5 → 169−25=144, other leg 12.",
         "Legs 1 and 1 give hypotenuse √2, which is irrational. Leave it as √2 unless the problem asks for a decimal.",
         "The little square in the corner marks the right angle. Put a and b on those two sides, c on the slant."],
        pythag_triangle(3, 4, 5, "A 3-4-5 right triangle",
                        "The square on the hypotenuse matches the two smaller squares together: 9+16=25.")
        + solved(1, "Legs 6 and 8. Find the hypotenuse.",
                 ["This is 3-4-5 with every side ×2.", "6²+8²=36+64=100.", "c=10."], "10")
        + matching([("3 and 4", "5"), ("5 and 12", "13"), ("6 and 8", "10"), ("8 and 15", "17")],
                   vid="g8u7-c1-match"),
        kid_tip("Square, add, then unsquare", "Do not add 3+4 and call it the hypotenuse."),
        1)
    c2 = concept_block(
        "2. The converse: is it right?",
        ["Turn the theorem around. If three side lengths already satisfy a²+b²=c² (with c the longest), the triangle is right.",
         "3, 4, 5: 9+16=25. Right. 6, 8, 10 is the same family scaled by 2, still right.",
         "2, 3, 4: 4+9=13, and 4²=16. 13≠16, so not right.",
         "If a²+b² is less than c², the angle opposite c is obtuse. If a²+b² is more than c², that angle is acute. Eighth grade mainly cares about the equal case: right or not.",
         "Always test the two shorter sides against the longest. Mixing which side is c breaks the test.",
         "A ladder 13 ft leaning so it reaches 12 ft up a wall needs 5 ft of ground — that is 5-12-13 standing up."],
        solved(1, "Do sides 6, 8, and 10 make a right triangle?",
               ["Longest is 10, so c=10.", "6²+8²=36+64=100=10².", "Yes: a scaled 3-4-5."], "yes")
        + watch_out("Adding the sides", "Pythagoras uses squares, not 6+8=14."),
        6)
    c3 = concept_block(
        "3. Distance is Pythagoras on a graph",
        ["From (1, 2) to (4, 6) the run is 4−1=3 and the rise is 6−2=4. Those are legs of a right triangle. Distance = 5.",
         "From (0, 0) to (6, 8) is 10. From (0, 0) to (5, 12) is 13. From (−1, 4) to (2, 8) is still 3 and 4, so 5.",
         "If the points share an x-coordinate, the segment is vertical: (2, 3) to (2, 8) is just |8−3|=5. Same for a horizontal run.",
         "Formula: distance = √[(x₂−x₁)² + (y₂−y₁)²]. Same theorem, coordinate clothes.",
         "Signs square away: (−3)² is 9. Distance is never negative.",
         "Sketch the two points, drop a right angle, label Δx and Δy, then square-add-root."],
        four_quadrant_plane([(1, 2), (4, 6)], lim=7, title="Distance as a right triangle",
                            caption="From (1, 2) to (4, 6) the run is 3 and the rise is 4. The slant is the hypotenuse 5.")
        + solved(1, "Find the distance from (1, 2) to (4, 6).",
                 ["Δx=3, Δy=4.", "3²+4²=9+16=25.", "Distance 5."], "5")
        + step_reveal(["Plot both points.", "Find the horizontal and vertical changes.",
                       "Those are legs. Square, add, take the root.", "Label units if the story has them."],
                      vid="g8u7-c3-steps"),
        11)
    c4 = concept_block(
        "4. Cylinders: V = πr²h",
        ["A cylinder has two circular bases and a straight height. Volume is base area times height.",
         "The base is a circle, so B = πr² and V = πr²h.",
         "Use 3.14 for π unless a problem says otherwise. r=2, h=5 → 3.14×4×5 = 62.8 cubic units.",
         "r=3, h=4 → 3.14×9×4 = 113.04. r=5, h=2 → 3.14×25×2 = 157. r=1, h=10 → 31.4.",
         "If you are given the diameter, cut it in half first. Diameter 6 means r=3. Then with h=5: 3.14×9×5 = 141.3.",
         "r=4, h=3 → 3.14×16×3 = 150.72. Keep cubic units. Surface wrapping would be a different formula — this unit is fill, not wrap."],
        cylinder_figure("A cylinder", "Circle base × height. Radius r goes from the center to the rim. Height h stands between the bases.")
        + solved(1, "Use 3.14. A cylinder has radius 2 and height 5. Volume?",
                 ["V=πr²h.", "r²=4, so 3.14×4=12.56.", "12.56×5=62.8."], "62.8")
        + matching([("r=2, h=5", "62.8"), ("r=3, h=4", "113.04"), ("r=5, h=2", "157"),
                    ("diameter 6, h=5", "141.3")], vid="g8u7-c4-match"),
        16)
    c5 = concept_block(
        "5. Radius, diameter, and π ≈ 3.14",
        ["Diameter is twice the radius. Never plug the diameter into r².",
         "π is a little more than 3. 3.14 is the eighth-grade workhorse. 22/7 is another estimate; stick to 3.14 here.",
         "Order of operations: square r first, then multiply by π, then by h. (πr)²h would be wrong.",
         "If height doubles and r stays put, volume doubles. If r doubles, r² quadruples, so volume ×4.",
         "A can, a pipe, a tank: same formula. Name what r and h are in the picture before you multiply.",
         "Compare two cans by computing both volumes, not by glancing at height alone — a short fat can can hold more."],
        solved(1, "A tank has diameter 6 and height 5. Use 3.14. Volume?",
               ["r=3, not 6.", "r²=9.", "3.14×9×5=141.3."], "141.3")
        + watch_out("Using the diameter as r", "r² with 6 would give four times too much volume."),
        21)
    c6 = concept_block(
        "6. Mix: ladders, maps, and cans",
        ["A 13 ft ladder reaching 12 ft up a wall sits 5 ft from the wall. Pythagoras, not a cylinder.",
         "A map distance between two grid points is the slant if you can travel diagonally, or the taxi path if you must stay on streets. This unit wants the slant: Pythagoras.",
         "A grain silo is a cylinder. Find r and h in the same unit before you use 3.14.",
         "If a story gives two legs of a right triangle and asks how far a bird flies, that is hypotenuse. If it asks how far along the ground, that is a leg.",
         "Check with a known triple when numbers look like 6-8-10 or 9-12-15.",
         "High school will add cones and spheres. The cylinder is the first curved solid with a simple πr²h."],
        solved(1, "A ladder is 13 ft. It reaches 12 ft up the wall. How far is the base from the wall?",
               ["Hypotenuse 13, one leg 12.", "169−144=25.", "Ground leg 5 ft."], "5 ft")
        + try_this("Name the shape first", "Right triangle or cylinder? That picks a²+b²=c² or πr²h."),
        26)
    content = unit_shell(
        title,
        ["a² + b² = c²", "The converse", "Distance on the plane",
         "Cylinder volume", "Radius vs diameter", "Ladders, maps, and cans"],
        c1 + c2 + c3 + c4 + c5 + c6, practice_slots(31, 25), "unit-7-pythagoras.mp4")
    return title, description, content, _u7_questions()


def _u8_questions():
    items = [
        ("Points that trend up and right show…", "positive association", ["negative association", "no association", "a circle"], "Both increase together."),
        ("Points that trend down and right show…", "negative association", ["positive association", "no association", "a cylinder"], "y falls as x rises."),
        ("A shapeless cloud of points shows…", "no association", ["perfect positive", "slope 1", "a function always"], "x does not help predict y."),
        ("A line of best fit…", "follows the trend, not every point", ["hits every point", "is always y=x", "is the y-axis"], "Some points sit off the line."),
        ("A point far from the cluster is an…", "outlier", ["intercept", "median always", "scale factor"], "It can tug a fitted line."),
        ("As study hours go up, scores tend to go up. Association?", "positive", ["negative", "none", "circular"], "Both rise."),
        ("As car age goes up, value tends to go down. Association?", "negative", ["positive", "none", "vertical"], "One up, one down."),
        ("Shoe size vs test score for a class is often…", "no association", ["perfect positive", "perfect negative", "a 3-4-5"], "Unrelated."),
        ("A two-way table organizes…", "two categorical variables", ["only means", "only scatter x-y", "π and r"], "Rows and columns of categories."),
        ("12 of 40 students play band. Relative frequency?", "12/40", ["12", "40", "28"], "Part over total."),
        ("12/40 as a percent?", "30%", ["12%", "40%", "70%"], "12÷40=0.3."),
        ("In a two-way table, a cell is…", "a joint count", ["always the mean", "the hypotenuse", "πr²"], "One row and one column."),
        ("To compare two groups, look at…", "center and spread of both", ["only the tallest value", "only one mean", "a scatter always"], "Two distributions."),
        ("A box plot's middle line is the…", "median", ["mean", "mode", "range"], "Q2."),
        ("IQR is…", "Q3 − Q1", ["max − min", "mean − median", "Q1 + Q3"], "Middle 50% width."),
        ("Group A median 8, Group B median 7. A is…", "typically higher", ["every score higher", "more spread always", "biased"], "Compare centers."),
        ("A longer box means…", "more spread in the middle 50%", ["a higher median always", "fewer people", "zero IQR"], "Variability."),
        ("Relative frequency 15/50 = ?", "0.3", ["15", "50", "0.15"], "15÷50."),
        ("If a fitted line is far above most points, you should…", "question the line", ["force it through (0,0)", "delete the axis", "use π"], "The line should follow the cloud."),
        ("Extrapolation is…", "predicting outside the data's x-range", ["reading a point you measured", "finding IQR", "using a²+b²"], "Riskier than interpolating."),
        ("Interpolation is…", "predicting inside the data's x-range", ["guessing past the last x", "a two-way cell", "volume"], "On the fitted line between points."),
        ("A strong association looks…", "tight around a trend", ["a perfect rectangle of points", "one lonely point", "a cylinder"], "Little scatter off the line."),
        ("A weak positive association…", "rises, but points are spread", ["falls tightly", "is a function with slope 0", "has IQR 0"], "Trend is there, noisy."),
        ("You cannot read a person's exact y from a scatter because…", "points vary around the trend", ["x is never known", "medians forbid it", "π is involved"], "The line is a model."),
        ("Rows: sport / no sport. Columns: band / no band. This is…", "a two-way table", ["a box plot", "a system of equations", "scientific notation"], "Two categories."),
        ("18 play soccer, 10 of those also play basketball, 40 students total. Soccer only?", "8", ["10", "18", "40"], "18−10."),
        ("Same numbers. Relative frequency who play soccer?", "18/40", ["10/40", "8/18", "40/18"], "Soccer row total over 40."),
        ("An outlier on a scatter can…", "pull the fitted line toward itself", ["erase association always", "change π", "make a triangle right"], "One far point has leverage."),
        ("Comparing two classes' scores, a scatter of (name, score) is a poor fit because…", "names are not a numeric x", ["scores cannot be compared", "you need π", "medians are illegal"], "Use box plots or two-way counts."),
        ("A line of best fit with slope 2 means…", "y tends to rise 2 when x rises 1", ["every point rises exactly 2", "IQR is 2", "r=2 for a cylinder"], "The model's rate."),
    ]
    return _fill(_pack(items), 55, lambda i: mq(
        f"{10 + i % 5} of {40} students are in band. Relative frequency in band?",
        f"{10 + i % 5}/40",
        "Relative frequency is the count divided by the total.",
        i,
        distractors=[str(10 + i % 5), "40", f"{30 - i % 5}/40"],
    ))


def build_unit8():
    title = "Eighth Grade Math Unit 8: Scatter Plots and Data"
    description = "Read association on scatter plots, use a line of best fit, and compare groups with two-way tables and box plots."
    c1 = concept_block(
        "1. Scatter plots and association",
        ["A scatter plot is a cloud of (x, y) points. Each point is one pair: hours studied and a quiz score, car age and price, temperature and ice-cream sales.",
         "Positive association: the cloud climbs as you move right. Study hours up, scores tend to go up.",
         "Negative association: the cloud falls as you move right. Car age up, value tends to go down.",
         "No association: a shapeless blob. Shoe size vs test score is often like that — x does not help you guess y.",
         "Strength: a tight cigar is strong. A wide spray that still slopes is weak. Strength is not the same as positive vs negative.",
         "Association is not a proof that x causes y. A third hidden factor can lift both."],
        scatter_plot("Positive association",
                     "These points climb to the right. A dashed line of best fit follows the trend without hitting every dot.")
        + solved(1, "Study hours vs scores trend up. What association is that?",
                 ["Both variables tend to increase together.", "That is the definition of positive association.",
                  "The cloud can still be messy."], "positive association")
        + matching([("up and right", "positive"), ("down and right", "negative"),
                    ("shapeless cloud", "none"), ("far-off point", "outlier")], vid="g8u8-c1-match"),
        1)
    c2 = concept_block(
        "2. Line of best fit",
        ["A line of best fit is a straight model through the cloud. It does not need to hit every point. Some points sit above, some below.",
         "Slope tells the typical change: slope 2 means y tends to rise about 2 when x rises 1.",
         "The intercept is where the model crosses the y-axis. It may or may not make sense in the story (negative hours, for example).",
         "Interpolation: use the line for an x between the smallest and largest data x. Extrapolation: go outside that range. Extrapolation is shakier.",
         "An outlier far from the cluster can pull the line toward itself. Ask whether that point is a real measurement or a glitch before you trust the slope.",
         "You cannot read one person's exact y from the line. The line is a typical path, not a promise."],
        solved(1, "A fitted line has slope 2. What does that say?",
               ["Slope is rise over run for the model.", "When x increases by 1, y tends to increase by 2.",
                "Individual points still scatter."], "y tends to rise 2 when x rises 1")
        + phet_box("curve")
        + watch_out("Forcing the line through every point", "Best fit is a compromise, not connect-the-dots."),
        6)
    c3 = concept_block(
        "3. Outliers and reading a model",
        ["An outlier sits far from the rest of the cloud. It can be a true unusual case or a typing error.",
         "If you drop a high-right outlier from a positive cloud, the slope often gets a little gentler. If you keep it, the line leans toward it.",
         "A strong association looks tight around the trend. A weak positive association still rises, but the points are spread.",
         "If a proposed line floats far above most points, question the line, not the students.",
         "Always name the variables in words: 'for these cars, age vs value,' not just x and y.",
         "A scatter needs two numeric measurements. Names vs scores is the wrong picture — use a box plot or a table instead."],
        solved(1, "Why can't you read one exact score from a scatter's fitted line?",
               ["Points vary around the trend.", "The line is a model of typical change.",
                "A new student can sit above or below it."], "points vary around the trend")
        + try_this("Cover one point", "Ask: if this dot vanished, would the slope still look like that?"),
        11)
    c4 = concept_block(
        "4. Two-way tables",
        ["A two-way table counts two categorical variables. Rows might be sport / no sport. Columns might be band / no band.",
         "Each cell is a joint count: how many are in that row and that column together.",
         "Relative frequency is a cell or a row total divided by the grand total. 12 of 40 in band is 12/40 = 30%.",
         "15 of 50 is 0.3. Same idea, different total.",
         "18 play soccer, 10 of those also play basketball, 40 students in all. Soccer only: 18−10=8. Relative frequency who play soccer: 18/40.",
         "You can compare 'among soccer players, what fraction also play basketball?' (10/18) with 'among all students' (maybe 10/40). Those are different questions."],
        solved(1, "12 of 40 students play band. Relative frequency?",
               ["Part over total.", "12/40.", "That is 30%."], "12/40")
        + matching([("12 of 40", "12/40"), ("15 of 50", "0.3"), ("cell", "joint count"),
                    ("two categories", "two-way table")], vid="g8u8-c4-match"),
        16)
    c5 = concept_block(
        "5. Compare two groups",
        ["Two box plots on one scale let you compare a typical value (median) and spread (IQR, whiskers).",
         "Group A median 8 vs Group B median 7: A is typically a bit higher. That is not 'every A score beats every B score.'",
         "A longer box means more spread in the middle 50%. Long whiskers mean more extreme values.",
         "IQR = Q3 − Q1. The middle line of the box is the median, not the mean.",
         "Overlap is normal. Write two sentences: one about center, one about spread.",
         "Pick the display that matches the data: scatter for two numeric measures, two-way table for two categories, box plots for one numeric measure in two groups."],
        two_box_plots("Two groups on one scale",
                      "Group A has median 8. Group B has median 7 and a longer high whisker. Compare both center and spread.")
        + solved(1, "Group A median is 8 and Group B median is 7. What can you say?",
                 ["Medians describe a typical value.", "8 is higher than 7.",
                  "A is typically higher; check spread separately."], "A is typically higher")
        + step_reveal(["Put both groups on the same number line.", "Compare medians.",
                       "Compare IQR or whiskers.", "Write center, then spread."], vid="g8u8-c5-steps"),
        21)
    c6 = concept_block(
        "6. Choose a display and a sentence",
        ["Hours vs score → scatter and maybe a line of best fit. Band vs sport → two-way table. Two classes' test scores → side-by-side box plots.",
         "A fitted slope is a rate in the model, not a promise for every person.",
         "Relative frequency lets you compare groups of different sizes. Raw counts alone can mislead if one class is twice as big.",
         "Extrapolation past the last data x is a guess with extra risk. Interpolation stays inside the x-range you actually measured.",
         "Finish with a sentence a person could use: 'Older cars in this set tend to cost less' or 'Band students in this sample are 30% of the grade.'",
         "High school stats will add correlation numbers. The pictures you can already read are the foundation."],
        solved(1, "You have hours studied and quiz scores for 30 students. Best display?",
               ["Two numeric variables.", "A scatter plot, then a line of best fit if the cloud has a trend.",
                "A two-way table would need categories, not hours."], "a scatter plot")
        + kid_tip("Match the data type", "Numbers vs numbers: scatter. Categories vs categories: table. One number, two groups: box plots."),
        26)
    content = unit_shell(
        title,
        ["Scatter and association", "Line of best fit", "Outliers",
         "Two-way tables", "Compare two groups", "Pick a display"],
        c1 + c2 + c3 + c4 + c5 + c6, practice_slots(31, 25), "unit-8-data.mp4")
    return title, description, content, _u8_questions()


def build_master():
    return f"""
<h1>Eighth Grade Math</h1>
<p>This is a full eighth-grade math path. Eighth grade is <strong>pre-algebra</strong>: exponents and scientific notation, linear equations, functions and slope, complex two-variable systems, the Pythagorean theorem, and data. High school algebra sits on these habits.</p>
<p>After each idea there are 5 quick questions. At the end of a unit there are 50 more. Hearts help you. Take your time.</p>
{page_break()}
<h2>The eight units</h2>
<ol>
<li>Unit 1 — Exponents and Scientific Notation</li>
<li>Unit 2 — Linear Equations in One Variable</li>
<li>Unit 3 — Slope and Linear Graphs</li>
<li>Unit 4 — Functions</li>
<li>Unit 5 — Systems by Substitution</li>
<li>Unit 6 — Systems by Elimination</li>
<li>Unit 7 — Pythagorean Theorem and Cylinders</li>
<li>Unit 8 — Scatter Plots and Data</li>
</ol>
<p>Exponents compress huge and tiny numbers. A line is a rate and a start. A function is a rule with one output. A system is two equations and one ordered pair — still two letters, but with fractions, distributing, and special cases. Pythagoras turns a right triangle into distance. A scatter tells whether two measures move together.</p>
{page_break()}
<h2>How to learn</h2>
<p>Keep both sides of an equation equal. Isolate one variable before you substitute. Scale a whole equation before you add to eliminate. Use 3.14 for π unless a problem says otherwise. Distance on a graph is a²+b²=c² with run and rise. For data, name the association, then say how strong it looks.</p>
<p>If a question feels hard, try a smaller example first — a 3-4-5 triangle, a 2x+3y system you can check, a five-point scatter. Then come back. You are building the habits algebra will run on.</p>
"""
