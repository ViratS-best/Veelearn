"""Unique extra questions for grade 1–8, MathCounts counting, and Algebra 2.

Each bank is ordered Easy → Medium → Hard → Stretch so polish_questions can fill
the 50-problem finale without repeating stems.
"""

from __future__ import annotations

import math


def _q(text, ans=None, expl="", dist=None, difficulty=None):
    if ans is None:
        return None
    if dist is not None and not isinstance(dist, (list, tuple)):
        dist = None
    item = {
        "question_text": text,
        "correct_answer": str(ans),
        "explanation": expl or "",
    }
    if dist is not None:
        item["distractors"] = [str(d) for d in dist]
    if difficulty:
        item["difficulty"] = difficulty
    return item


def _near(ans, alts):
    return [a for a in alts if str(a) != str(ans)][:3]


# ---------------------------------------------------------------------------
# Grade 1
# ---------------------------------------------------------------------------

def g1u1():
    qs = []
    for n in (6, 11, 14, 17, 23, 28, 35, 41, 47, 52, 68, 79, 84, 91, 99):
        qs.append(_q(f"What number comes after {n}?", n + 1, f"{n}, then {n + 1}."))
    for a, b in ((12, 21), (30, 13), (45, 54), (70, 17), (101, 110)):
        qs.append(_q(f"Which is greater: {a} or {b}?", max(a, b), f"{max(a, b)} is farther along when we count.", [min(a, b), abs(a - b), 0]))
    for start, hop in ((18, 4), (26, 5), (33, 7), (49, 6), (88, 5)):
        qs.append(_q(f"Start at {start}. Count on {hop}. Where do you land?", start + hop, f"{start} plus {hop} is {start + hop}."))
    qs.append(_q("A box shows 10 + 10 + 7. What number is that?", 27, "Two tens and 7 ones is 27."))
    qs.append(_q("Count by tens: 40, 50, 60, ___.", 70, "Each jump is 10."))
    qs.append(_q("Maya counts 96, 97, 98, 99. What is next?", 100, "After 99 comes 100."))
    qs.append(_q("There are 8 red cubes and 9 blue cubes. How many cubes in all?", 17, "8 + 9 = 17.", difficulty="hard"))
    qs.append(_q("A number line jumps 10, 20, 30, 40. What is 3 jumps after 40?", 70, "50, 60, 70.", difficulty="hard"))
    qs.append(_q("Sam has 15 stickers, gets 6 more, then gives 4 away. How many now?", 17, "15+6=21, 21−4=17.", difficulty="hard"))
    qs.append(_q("Which missing number: 108, 109, ___, 111?", 110, "Count by ones through 110.", difficulty="hard"))
    qs.append(_q("A train of 3 cars has 4 windows each. How many windows?", 12, "3 × 4 = 12. Count 4 three times.", difficulty="stretch"))
    qs.append(_q("You need 20 crayons. You have 12. How many more?", 8, "20 − 12 = 8.", difficulty="stretch"))
    qs.append(_q("Count back: 15, 14, 13, ___.", 12, "One less than 13 is 12.", difficulty="stretch"))
    qs.append(_q("Two tens-frames show 10 and 7 filled. Total?", 17, "10 + 7 = 17.", difficulty="stretch"))
    qs.append(_q("What is 10 more than 54?", 64, "Adding a ten: 5 tens become 6 tens.", difficulty="stretch"))
    qs.append(_q("A path has 9 stepping stones. You stand on stone 1. How many steps to stone 9?", 8, "From 1 to 9 is 8 steps.", difficulty="stretch"))
    qs.append(_q("Which pair makes 10: 7 and ___?", 3, "7 + 3 = 10.", difficulty="stretch"))
    qs.append(_q("There are 11 birds. 2 fly away, then 5 more land. How many birds now?", 14, "11−2=9, 9+5=14.", difficulty="stretch"))
    qs.append(_q("100 is how many tens?", 10, "10 tens make 100.", difficulty="stretch"))
    qs.append(_q("A chart shows 5 rows of 10 dots and 3 extra. How many dots?", 53, "50 + 3 = 53.", difficulty="stretch"))
    return qs


def g1u2():
    qs = []
    for t, o in ((3, 4), (5, 2), (7, 0), (6, 8), (9, 1), (2, 9), (8, 5), (4, 7), (1, 6), (0, 9)):
        qs.append(_q(f"{t} tens and {o} ones is what number?", 10 * t + o, f"{t} tens is {10*t}. Plus {o} ones is {10*t+o}."))
    for n in (47, 58, 63, 81, 94, 36, 29, 70, 15, 42):
        qs.append(_q(f"How many tens are in {n}?", n // 10, f"{n} is {n//10} tens and {n%10} ones."))
    qs += [
        _q("What is 10 more than 38?", 48, "The tens digit goes up by 1."),
        _q("What is 10 less than 90?", 80, "9 tens become 8 tens."),
        _q("42 = ___ tens + 2 ones. Missing tens?", 4, "4 tens and 2 ones."),
        _q("A number has 6 tens and 0 ones. What number?", 60, "6 tens is 60."),
        _q("Which is greater: 3 tens 9 ones or 4 tens 0 ones?", 40, "40 > 39.", ["39", "30", "9"], difficulty="hard"),
        _q("You have 5 tens. You add 12 ones. What number? (make a new ten)", 62, "12 ones = 1 ten + 2. 6 tens and 2 ones.", difficulty="hard"),
        _q("27 + 10 + 10 = ?", 47, "Two tens added: 27, 37, 47.", difficulty="hard"),
        _q("A bundle of 10 sticks plus 10 more bundles of 10. How many sticks?", 110, "11 tens = 110.", difficulty="hard"),
        _q("Write 8 tens and 14 ones as a standard number.", 94, "14 ones = 1 ten + 4, so 9 tens 4 ones.", difficulty="stretch"),
        _q("Which shows 53? 4 tens and 13 ones, or 5 tens and 3 ones? Both equal 53. How many tens after regrouping 4 tens 13 ones?", 5, "13 ones make 1 more ten.", difficulty="stretch"),
        _q("70 is the same as ___ + 20.", 50, "50 + 20 = 70.", difficulty="stretch"),
        _q("A number is 1 ten less than 100 and 3 ones more than 87. What number?", 90, "90 is 10 less than 100. 87+3=90.", difficulty="stretch"),
        _q("How many ones to go from 6 tens 8 ones to the next ten?", 2, "68 + 2 = 70.", difficulty="stretch"),
        _q("2 tens + 3 tens + 4 ones = ?", 54, "5 tens and 4 ones.", difficulty="stretch"),
        _q("The tens digit of 81 is 8. If you swap tens and ones, what number?", 18, "8 ones and 1 ten is 18.", difficulty="stretch"),
        _q("A chart: 40 + 9. What number?", 49, "4 tens 9 ones.", difficulty="stretch"),
        _q("99 is ___ tens and ___ ones. How many tens?", 9, "9 tens and 9 ones.", difficulty="stretch"),
        _q("You pack 35 ones into tens. How many leftover ones?", 5, "3 tens leftover 5.", difficulty="stretch"),
    ]
    return qs


def g1u3():
    qs = []
    for a, b in ((4, 5), (6, 7), (8, 3), (9, 9), (2, 8), (7, 6), (5, 9), (8, 8), (1, 12), (11, 4)):
        qs.append(_q(f"{a} + {b} = ?", a + b, f"{a} + {b} = {a+b}."))
    qs += [
        _q("9 + 6. Make a ten. 9 needs 1 more. Then 5 left. What is the sum?", 15, "10 + 5 = 15."),
        _q("8 + 7. Make a ten. Answer?", 15, "8 + 2 = 10, plus 5 is 15."),
        _q("A double: 6 + 6 = ?", 12, "Double 6 is 12."),
        _q("Double plus one: 7 + 8 = ?", 15, "7+7=14, plus 1 is 15."),
        _q("13 + 5 = ?", 18, "13, 14, 15, 16, 17, 18."),
        _q("There are 9 red and 8 blue. Total?", 17, "9+8=17.", difficulty="hard"),
        _q("You have 6. You get 7 more, then 2 more. Total?", 15, "6+7=13, +2=15.", difficulty="hard"),
        _q("Which pair makes 20: 12 + ___?", 8, "12+8=20.", difficulty="hard"),
        _q("A ten-frame is full and another shows 4. Add 3 more. Total?", 17, "10+4+3=17.", difficulty="hard"),
        _q("9 + 9 + 2 = ?", 20, "18+2=20.", difficulty="stretch"),
        _q("A story: 5 birds, 7 more, then 4 more. How many?", 16, "5+7+4=16.", difficulty="stretch"),
        _q("You need 20. You have 11 and 6. How many still needed?", 3, "17, need 3 more.", difficulty="stretch"),
        _q("Make 10 twice: (6+4) + (8+2) = ?", 20, "10+10=20.", difficulty="stretch"),
        _q("15 + 6 = ? (think 15+5+1)", 21, "20+1=21.", difficulty="stretch"),
        _q("A box of 10 plus a box of 8. Then you add 5 from a third box. Total?", 23, "10+8+5=23.", difficulty="stretch"),
        _q("7 + 5 + 7 = ?", 19, "7+7=14, +5=19.", difficulty="stretch"),
        _q("What addend is missing: 9 + ___ = 17?", 8, "9+8=17.", difficulty="stretch"),
        _q("Two teams score 8 and 9. Combined score?", 17, "8+9=17.", difficulty="stretch"),
        _q("Count on from 14 by 3 hops of 2. Land on?", 20, "16, 18, 20.", difficulty="stretch"),
        _q("A number sentence 4 + 4 + 4 + 4. Sum?", 16, "Four 4s is 16.", difficulty="stretch"),
    ]
    return qs


def g1u4():
    qs = []
    for a, b in ((9, 4), (12, 5), (15, 7), (18, 9), (11, 3), (14, 6), (16, 8), (20, 4), (13, 8), (17, 9)):
        qs.append(_q(f"{a} − {b} = ?", a - b, f"{a} − {b} = {a-b}."))
    qs += [
        _q("10 − 6 = ?", 4, "6 and 4 make 10."),
        _q("You have 15. Give away 8. Left?", 7, "15−8=7."),
        _q("Count back 3 from 12.", 9, "11, 10, 9."),
        _q("What is the missing number: 14 − ___ = 6?", 8, "14−8=6."),
        _q("A related fact: 9 + 7 = 16, so 16 − 7 = ?", 9, "Subtraction undoes addition."),
        _q("20 − 11 = ?", 9, "20−10=10, then one more is 9.", difficulty="hard"),
        _q("There were 18 cookies. 9 eaten, then 2 more eaten. Left?", 7, "18−9=9, 9−2=7.", difficulty="hard"),
        _q("How much more is 16 than 9?", 7, "16−9=7.", difficulty="hard"),
        _q("A ten-frame of 10 and 3 extra. Remove 5. Left?", 8, "13−5=8.", difficulty="hard"),
        _q("Start at 19. Subtract 4, then subtract 6. Where?", 9, "15, then 9.", difficulty="stretch"),
        _q("You need 12. You have 20. Extra?", 8, "20−12=8 extra.", difficulty="stretch"),
        _q("15 − 8 − 3 = ?", 4, "7−3=4.", difficulty="stretch"),
        _q("A bus has 16 kids. 7 get off, 2 get on. How many now?", 11, "16−7=9, +2=11.", difficulty="stretch"),
        _q("Which is greater: 14−5 or 12−4?", 9, "9 vs 8.", ["8", "7", "10"], "stretch"),
        _q("Missing: ___ − 6 = 9.", 15, "15−6=9.", difficulty="stretch"),
        _q("A jump back of 10 from 17 lands on?", 7, "17−10=7.", difficulty="stretch"),
        _q("Two-step: 13 − 5 + 4 = ?", 12, "8+4=12.", difficulty="stretch"),
        _q("If 8 + x = 15, then 15 − 8 = x. What is x?", 7, "Related facts.", difficulty="stretch"),
        _q("A pile of 20 minus two piles of 6. Left?", 8, "20−12=8.", difficulty="stretch"),
        _q("Count back by 2s: 14, 12, 10, ___.", 8, "Next is 8.", difficulty="stretch"),
    ]
    return qs


def g1u5():
    qs = []
    stories = [
        ("6 frogs on a log. 5 jump on. How many frogs?", 11, "6+5=11."),
        ("There are 9 balloons. 4 pop. How many left?", 5, "9−4=5."),
        ("A box has 7 toys. Another has 8. Total toys?", 15, "7+8=15."),
        ("12 birds. 3 fly away. How many stay?", 9, "12−3=9."),
        ("4 red cars and 6 blue cars. How many cars?", 10, "4+6=10."),
        ("You read 5 pages, then 9 more. Pages in all?", 14, "5+9=14."),
        ("A team scores 8 then 7. Total points?", 15, "8+7=15."),
        ("10 stickers. You use 6. Left?", 4, "10−6=4."),
        ("3 cats, 5 dogs, 2 birds. How many animals?", 10, "3+5+2=10."),
        ("A shelf holds 16 books. 9 are taken. Left?", 7, "16−9=7."),
        ("Morning: 8 apples. Afternoon: 8 more. Total?", 16, "Double 8."),
        ("A class of 18. 6 leave for music. How many stay?", 12, "18−6=12."),
        ("You save 5, then 5, then 4. Total saved?", 14, "10+4=14."),
        ("A puzzle has 20 pieces. 7 are placed. Not placed?", 13, "20−7=13."),
        ("Two baskets: 9 and 11. Combined?", 20, "9+11=20."),
    ]
    for args in stories:
        qs.append(_q(*args))
    qs += [
        _q("A story with extra news: 7 ducks, 4 geese, and it is raining. How many birds?", 11, "7+4=11. Weather does not change the count.", difficulty="hard"),
        _q("Lia has 14 crayons. She gives 5 to Jo and 3 to Sam. Left?", 6, "14−8=6.", difficulty="hard"),
        _q("A bus seats 20. 12 sit down. Empty seats?", 8, "20−12=8.", difficulty="hard"),
        _q("You need 15 cups. You have 6 red and 4 blue. Still need?", 5, "10, need 5 more.", difficulty="hard"),
        _q("Farm: 8 cows, 7 sheep, 5 of the cows are brown. How many animals?", 15, "Color is extra. 8+7=15.", difficulty="stretch"),
        _q("A game: start 10 points, lose 3, win 8. Score?", 15, "7+8=15.", difficulty="stretch"),
        _q("Boxes of 5, 5, and 6 muffins. Total muffins?", 16, "10+6=16.", difficulty="stretch"),
        _q("Compare: 9+6 versus 20−6. Which total is bigger?", 15, "15 vs 14.", ["14", "9", "20"], "stretch"),
        _q("Three friends share. Ana 4, Ben 5, Cora 7. Combined snacks?", 16, "4+5+7=16.", difficulty="stretch"),
        _q("A two-step story: 13 fish, 4 swim away, 2 join. How many?", 11, "9+2=11.", difficulty="stretch"),
        _q("You buy 2 packs of 6 pencils. How many pencils?", 12, "6+6=12.", difficulty="stretch"),
        _q("A number story: some + 9 = 17. Some is?", 8, "17−9=8.", difficulty="stretch"),
        _q("Park: 10 kids, 6 more come, 4 leave. Kids now?", 12, "16−4=12.", difficulty="stretch"),
        _q("Which story matches 12−7: 12 birds, 7 fly away. How many left?", 5, "12−7=5.", difficulty="stretch"),
        _q("A tray of 18 cookies. You eat 9. Friend eats 4. Left for later?", 5, "18−13=5.", difficulty="stretch"),
        _q("Double a story: 7 + 7, then subtract 3.", 11, "14−3=11.", difficulty="stretch"),
        _q("There were some. After adding 6 there are 14. Some was?", 8, "14−6=8.", difficulty="stretch"),
        _q("A pictograph shows 4 smiles then 5 more. Total smiles?", 9, "4+5=9.", difficulty="stretch"),
        _q("Two-step with tens: 10 + 8 − 5 = ?", 13, "18−5=13.", difficulty="stretch"),
        _q("A riddle: I am 3 more than 9 + 4. What number?", 16, "13+3=16.", difficulty="stretch"),
    ]
    return qs


def g1u6():
    qs = []
    for h in range(1, 12):
        qs.append(_q(f"The hour hand points to {h} and the minute hand points to 12. What time?", f"{h}:00", f"That is {h} o'clock.", [f"{h}:30", f"{h+1}:00", f"{h}:15"]))
    qs += [
        _q("Minute hand on 6, hour hand between 2 and 3. Time?", "2:30", "6 means 30 minutes.", ["2:00", "3:00", "6:00"]),
        _q("How many minutes in 1 hour?", 60, "A clock has 60 minutes."),
        _q("How many hours from 1:00 to 4:00?", 3, "1 to 4 is 3 hours."),
        _q("Half past 7 is…", "7:30", "Half past means 30 minutes.", ["7:00", "8:00", "6:30"]),
        _q("School starts at 9:00. It is 8:00. How many hours to wait?", 1, "One hour.", difficulty="hard"),
        _q("A movie is 2 hours. It starts at 3:00. When does it end?", "5:00", "3+2=5.", ["4:00", "6:00", "2:00"], difficulty="hard"),
        _q("From 2:00 to 2:30 is how many minutes?", 30, "Half an hour.", difficulty="hard"),
        _q("The minute hand on 3 means how many minutes?", 15, "Each number is 5 minutes. 3×5=15.", difficulty="hard"),
        _q("A clock shows 4:00. What time in 3 hours?", "7:00", "4+3=7.", difficulty="stretch"),
        _q("It is 10:00. Recess is at 10:30. How many minutes?", 30, "Half an hour.", difficulty="stretch"),
        _q("Hour hand on 12, minute hand on 12. Time?", "12:00", "Noon or midnight.", ["12:30", "1:00", "6:00"], "stretch"),
        _q("Which is later: 6:00 or 5:00?", "6:00", "6 comes after 5.", ["5:00", "4:00", "same"], "stretch"),
        _q("A show lasts 1 hour 30 minutes. That is how many minutes?", 90, "60+30=90.", difficulty="stretch"),
        _q("If the minute hand moves from 12 to 6, how many minutes passed?", 30, "Half the clock.", difficulty="stretch"),
        _q("Breakfast at 7:00, school at 9:00. Hours between?", 2, "7 to 9.", difficulty="stretch"),
        _q("A clock is 1 hour fast. It shows 4:00. Real time?", "3:00", "Subtract one hour.", difficulty="stretch"),
        _q("Quarter past 1 is…", "1:15", "Quarter of 60 is 15.", ["1:30", "1:45", "1:00"], "stretch"),
        _q("How many times does the hour hand go around in 24 hours?", 2, "Twice around a 12-hour clock.", difficulty="stretch"),
        _q("From 11:00 to 1:00 is how many hours?", 2, "11 to 12 to 1.", difficulty="stretch"),
        _q("Minute hand on 9 means ___ minutes.", 45, "9×5=45.", difficulty="stretch"),
    ]
    return qs


def g1u7():
    qs = []
    for a, b in ((3, 5), (8, 2), (10, 7), (4, 4), (12, 9), (15, 6), (20, 11), (9, 13), (1, 8), (16, 16)):
        longer = max(a, b)
        qs.append(_q(f"A worm is {a} cubes long. A stick is {b} cubes. Which length is longer (in cubes)?", longer, f"{longer} cubes is longer.", [min(a, b), a + b, abs(a - b)]))
    qs += [
        _q("A pencil is 6 cubes. A pen is 2 cubes longer. Pen length?", 8, "6+2=8."),
        _q("A ribbon is 12 cubes. You cut 4 cubes off. Left?", 8, "12−4=8."),
        _q("Two rods of 5 cubes joined end to end. Total length?", 10, "5+5=10."),
        _q("Which unit is better for a room: cubes or footsteps?", "footsteps", "A room is long. Footsteps fit better.", ["cubes", "paper clips", "grains of rice"]),
        _q("A path is 9 steps. You already walked 4. Steps left?", 5, "9−4=5."),
        _q("A string is 14 cm. Another is 8 cm. Difference?", 6, "14−8=6.", difficulty="hard"),
        _q("Three cubes, then four more in a train. How long?", 7, "3+4=7.", difficulty="hard"),
        _q("A desk is 10 spans. A book is 3 spans. How many books fit end to end?", 3, "3+3+3=9, leftover 1, so 3 books.", difficulty="hard"),
        _q("Measure twice: 8 cubes then 8 cubes in a line. Total?", 16, "8+8=16.", difficulty="hard"),
        _q("A fence is 20 units. Posts every 5 units, including both ends. How many posts?", 5, "0,5,10,15,20 → 5 posts.", difficulty="stretch"),
        _q("You line up 4 pencils of 5 cubes. Train length?", 20, "4×5=20.", difficulty="stretch"),
        _q("A snake is 11 cubes. It grows 6. New length?", 17, "11+6=17.", difficulty="stretch"),
        _q("Shorter by 3 than 15 is?", 12, "15−3=12.", difficulty="stretch"),
        _q("Two paths: 7+5 versus 10+1. Which is longer (the length)?", 12, "12 vs 11.", ["11", "10", "7"], "stretch"),
        _q("A ruler starts at 2 and the object ends at 9. Length?", 7, "9−2=7, not 9.", difficulty="stretch"),
        _q("If 1 paper clip is 3 cubes, 4 paper clips are how many cubes?", 12, "4×3=12.", difficulty="stretch"),
        _q("A table is 16 cubes. A mat covers 9. Uncovered?", 7, "16−9=7.", difficulty="stretch"),
        _q("Order from short to long: 4, 9, 6. Middle length?", 6, "4, 6, 9.", difficulty="stretch"),
        _q("You need 18 cubes to match a rope. You have 10. Need how many more?", 8, "18−10=8.", difficulty="stretch"),
        _q("A broken ruler starts at 5. Object ends at 12. True length?", 7, "Always subtract start from end.", difficulty="stretch"),
    ]
    return qs


def g1u8():
    qs = []
    qs += [
        _q("A triangle has how many sides?", 3, "Tri means three."),
        _q("A square has how many equal sides?", 4, "All four sides match."),
        _q("A rectangle has how many corners?", 4, "Four square corners."),
        _q("A circle has how many corners?", 0, "A circle is round. No corners."),
        _q("A hexagon has how many sides?", 6, "Hex means six."),
        _q("Which shape has 5 sides?", "pentagon", "Penta means five.", ["hexagon", "square", "triangle"]),
        _q("A cube has faces that are…", "squares", "Each face is a square.", ["circles", "triangles", "rectangles only"]),
        _q("A rhombus looks like a pushed square. How many sides?", 4, "Four equal sides."),
        _q("Two triangles make a…", "diamond or quadrilateral", "Two 3-sides can make 4 sides.", ["circle", "hexagon", "one side"]),
        _q("A stop-sign shape is an octagon. Sides?", 8, "Octo means eight."),
        _q("Closed shape with 3 corners. Name?", "triangle", "3 corners, 3 sides.", ["square", "circle", "oval"]),
        _q("Which is NOT a rectangle: a square or a circle?", "circle", "A square is a special rectangle. A circle is not.", ["square", "both", "neither"]),
        _q("A pattern: triangle, square, triangle, square. Next?", "triangle", "It repeats.", ["circle", "hexagon", "line"]),
        _q("How many triangles in a square cut by one diagonal?", 2, "The diagonal splits it into 2."),
        _q("A cylinder looks like a can. Its bases are…", "circles", "Top and bottom are circles.", ["squares", "triangles", "points"]),
        _q("A cone has how many flat faces?", 1, "One circle face, plus a curved surface.", difficulty="hard"),
        _q("A rectangular prism (box) has how many faces?", 6, "Like a dice without the dots: 6 faces.", difficulty="hard"),
        _q("Compose: 2 squares side by side. The new shape is a…", "rectangle", "2×1 squares make a rectangle.", difficulty="hard"),
        _q("A shape has 4 sides, only one pair parallel. It is a…", "trapezoid", "Exactly one pair of parallel sides.", ["square", "circle", "triangle"], difficulty="hard"),
        _q("How many edges does a cube have?", 12, "4 on top, 4 on bottom, 4 upright.", difficulty="stretch"),
        _q("A pentagon plus a triangle sharing a side. How many outer sides if they share 1 full side?", 6, "5+3−2=6 outer sides.", difficulty="stretch"),
        _q("Which solid can roll and also stand on a flat face?", "cone or cylinder", "Both have a circle face.", ["cube", "pyramid only", "square"], "stretch"),
        _q("A square has perimeter 12 (sides 3). One side length?", 3, "12÷4=3.", difficulty="stretch"),
        _q("Sort: 3-sided vs 4-sided. A rhombus goes with…", "4-sided", "Four sides.", difficulty="stretch"),
        _q("A circle is cut into 2 equal pieces. Each is a…", "half circle / semicircle", "Two equal arcs.", difficulty="stretch"),
        _q("Count vertices of a triangular pyramid (tetrahedron).", 4, "4 corners.", difficulty="stretch"),
        _q("A pattern of shapes: 4 sides, 3 sides, 4 sides. Next number of sides?", 3, "Alternating.", difficulty="stretch"),
        _q("Which has more sides: hexagon or pentagon?", "hexagon", "6 > 5.", difficulty="stretch"),
        _q("A cube net needs how many squares?", 6, "Six faces.", difficulty="stretch"),
        _q("Two congruent right triangles make a…", "rectangle or isosceles triangle depending on join", "Often a rectangle.", difficulty="stretch"),
        _q("A shape with no straight sides is a…", "circle", "Only a curve.", difficulty="stretch"),
        _q("How many right angles in a rectangle?", 4, "All corners are square.", difficulty="stretch"),
        _q("A stop sign vs a square: the octagon has how many more sides?", 4, "8−4=4.", difficulty="stretch"),
        _q("Build a house: square + triangle on top. How many outer sides if they share 1 side?", 5, "4+3−2=5 (a pentagon house).", difficulty="stretch"),
        _q("A sphere (ball) has how many edges?", 0, "No edges.", difficulty="stretch"),
    ]
    return qs


def _loop_add(pairs, tmpl, expl_fn):
    return [_q(tmpl.format(a=a, b=b), expl_fn(a, b)[0], expl_fn(a, b)[1]) for a, b in pairs]


# ---------------------------------------------------------------------------
# Grade 2–5 compact numeric banks
# ---------------------------------------------------------------------------

def g2u1():
    qs = []
    for n in (105, 199, 250, 307, 416, 580, 642, 701, 888, 999, 120, 234, 345, 456, 567):
        qs.append(_q(f"What number is 1 more than {n}?", n + 1, f"{n}+1={n+1}."))
    for n in (240, 350, 410, 500, 670):
        qs.append(_q(f"What is 10 more than {n}?", n + 10, "Add one ten."))
    for n in (300, 450, 620, 800, 190):
        qs.append(_q(f"What is 100 more than {n}?", n + 100, "Add one hundred."))
    qs += [
        _q("Write 4 hundreds, 0 tens, 7 ones.", 407, "407."),
        _q("Which is greater: 702 or 720?", 720, "Compare tens: 2 vs 0 in the tens? 720 has 2 tens.", ["702", "700", "722"]),
        _q("399 + 1 = ?", 400, "Next hundred.", difficulty="hard"),
        _q("A number has digits 5, 8, 2 from hundreds to ones. Number?", 582, "5 hundreds 8 tens 2 ones.", difficulty="hard"),
        _q("Skip count by 5s: 485, 490, 495, ___.", 500, "Next is 500.", difficulty="hard"),
        _q("How many hundreds in 840?", 8, "8 hundreds.", difficulty="hard"),
        _q("The value of 6 in 645 is?", 600, "6 hundreds.", difficulty="stretch"),
        _q("Closest hundred to 278?", 300, "278 is nearer 300 than 200.", difficulty="stretch"),
        _q("Expanded: 300+40+9. Standard form?", 349, "Add the parts.", difficulty="stretch"),
        _q("A chart: 7 hundreds 14 tens 3 ones. Regroup. Number?", 843, "14 tens = 1 hundred 4 tens → 8 hundreds 4 tens 3 ones.", difficulty="stretch"),
        _q("Compare 505 and 550 using place value. Greater?", 550, "Tens place 5 vs 0.", difficulty="stretch"),
        _q("Count by 10s from 960. Two jumps. Land?", 980, "970 then 980.", difficulty="stretch"),
        _q("Smallest 3-digit number with digits 2, 0, 8?", 208, "Do not put 0 first.", difficulty="stretch"),
        _q("1000 is 1 more than…", 999, "Last 3-digit number.", difficulty="stretch"),
        _q("How many tens in 230?", 23, "23 tens make 230.", difficulty="stretch"),
        _q("A number between 348 and 352 that is even?", 350, "348,349,350,351,352.", difficulty="stretch"),
        _q("Round 67 to the nearest ten.", 70, "7 ones rounds up.", difficulty="stretch"),
        _q("2 hundreds + 12 tens = ?", 320, "12 tens = 1 hundred 2 tens → 3 hundreds 2 tens.", difficulty="stretch"),
        _q("Which is 10 less than 1000?", 990, "Subtract a ten.", difficulty="stretch"),
        _q("Place-value puzzle: I have 9 hundreds, 0 tens, 9 ones.", 909, "909.", difficulty="stretch"),
    ]
    return qs


def g2u2():
    qs = []
    for a, b in ((34, 27), (58, 16), (47, 38), (69, 25), (125, 48), (208, 37), (156, 79), (333, 48), (270, 35), (419, 82)):
        qs.append(_q(f"{a} + {b} = ?", a + b, f"{a}+{b}={a+b}. Regroup if ones ≥ 10."))
    qs += [
        _q("99 + 6 = ?", 105, "9+6=15 ones → 10 tens 5 ones plus 9 tens = 105."),
        _q("45 + 45 = ?", 90, "Double 45."),
        _q("199 + 2 = ?", 201, "Across 200."),
        _q("136 + 50 = ?", 186, "Add 5 tens."),
        _q("7 + 8 + 9 + 6 = ?", 30, "15+15=30.", difficulty="hard"),
        _q("A store: 48 red + 37 blue shirts. Total?", 85, "48+37=85.", difficulty="hard"),
        _q("Add 246 + 178.", 424, "Regroup ones and tens.", difficulty="hard"),
        _q("Three addends: 19+26+15.", 60, "45+15=60.", difficulty="hard"),
        _q("You have 275. You get 48 more. Total?", 323, "275+48=323.", difficulty="stretch"),
        _q("A two-step: 59+18 then add 7.", 84, "77+7=84.", difficulty="stretch"),
        _q("Closest estimate of 398+205?", 600, "400+200.", difficulty="stretch"),
        _q("Missing addend: 67 + ___ = 100.", 33, "67+33=100.", difficulty="stretch"),
        _q("4 tens 8 ones + 5 tens 7 ones. Sum?", 105, "48+57=105.", difficulty="stretch"),
        _q("A page of 3 numbers: 125, 125, 50. Total?", 300, "250+50.", difficulty="stretch"),
        _q("Add across 10 twice: 8+7+6+5.", 26, "15+11=26.", difficulty="stretch"),
        _q("508 + 97 = ?", 605, "508+100−3=605.", difficulty="stretch"),
        _q("A fundraiser: $129 + $86.", 215, "129+86=215.", difficulty="stretch"),
        _q("Which sum is odd: 24+18 or 24+19?", 43, "24+19=43 odd.", ["42", "24", "19"], "stretch"),
        _q("Mental: 199+199.", 398, "200+200−2.", difficulty="stretch"),
        _q("Column add 456+277.", 733, "Regroup all places.", difficulty="stretch"),
    ]
    return qs


def g2u3():
    qs = []
    for a, b in ((50, 18), (80, 27), (63, 29), (91, 47), (100, 36), (200, 45), (152, 78), (340, 65), (415, 89), (500, 123)):
        qs.append(_q(f"{a} − {b} = ?", a - b, f"{a}−{b}={a-b}. Regroup if needed."))
    qs += [
        _q("70 − 1 = ?", 69, "Across a ten."),
        _q("103 − 8 = ?", 95, "Regroup a ten."),
        _q("How much more is 90 than 47?", 43, "90−47=43."),
        _q("A jump back of 30 from 85.", 55, "85−30=55."),
        _q("200 − 58 = ?", 142, "Regroup hundreds.", difficulty="hard"),
        _q("A shop: 120 stickers, sell 47. Left?", 73, "120−47=73.", difficulty="hard"),
        _q("Subtract twice: 95 − 20 − 15.", 60, "75−15=60.", difficulty="hard"),
        _q("Missing: 81 − ___ = 39.", 42, "81−39=42.", difficulty="hard"),
        _q("A two-step: 84 − 19 + 6.", 71, "65+6=71.", difficulty="stretch"),
        _q("Estimate 398−201.", 200, "About 400−200.", difficulty="stretch"),
        _q("1000 − 1 = ?", 999, "One less than 1000.", difficulty="stretch"),
        _q("A number minus 29 is 71. Number?", 100, "71+29=100.", difficulty="stretch"),
        _q("Column: 503 − 278.", 225, "Regroup across 0.", difficulty="stretch"),
        _q("Difference of 640 and 275.", 365, "640−275=365.", difficulty="stretch"),
        _q("You need 250. You have 178. Still need?", 72, "250−178=72.", difficulty="stretch"),
        _q("Subtract 99 from 400 by subtracting 100 then adding 1.", 301, "300+1=301.", difficulty="stretch"),
        _q("A game score 205 minus penalty 47.", 158, "205−47=158.", difficulty="stretch"),
        _q("Which difference is larger: 90−41 or 80−28?", 52, "49 vs 52.", ["49", "41", "28"], "stretch"),
        _q("Three-digit: 711 − 86.", 625, "Regroup tens.", difficulty="stretch"),
        _q("A riddle: I am 40 less than 125.", 85, "125−40=85.", difficulty="stretch"),
    ]
    return qs


def g2u4():
    qs = [
        _q("You have 18 marbles. You win 7 then lose 9. How many?", 16, "25−9=16."),
        _q("A class of 24. 6 leave, 5 return. Now?", 23, "18+5=23."),
        _q("Boxes of 10: 3 boxes plus 8 extra, then use 12. Left?", 26, "38−12=26."),
        _q("A book: 15 pages Monday, 18 Tuesday. Total so far. 40-page book. Left?", 7, "33, 40−33=7."),
        _q("Stickers 9+9. Give 6 away. Left?", 12, "18−6=12."),
        _q("A two-step shop: $20. Buy a $8 toy and a $5 snack. Left?", 7, "13, 20−13=7."),
        _q("Team A 14 points, Team B 9, then A scores 6. A’s score?", 20, "14+6=20."),
        _q("35 birds, 12 fly, 8 land. Birds now?", 31, "23+8=31."),
        _q("You need 50. Have 28, get 15 more. Still need?", 7, "43, need 7."),
        _q("A bus 40 seats. 22 sit, 9 more sit. Empty?", 9, "31 sitting, 9 empty."),
        _q("Morning 16 tasks, finish 9, get 5 new. Remaining?", 12, "7+5=12."),
        _q("Double 12 then subtract 5.", 19, "24−5=19."),
        _q("A recipe 2 cups + 3 cups, then you use 4. Left?", 1, "5−4=1."),
        _q("Scores 8, 7, 9. Total. Goal 30. Short by?", 6, "24, 30−24=6."),
        _q("A park 27 trees, plant 14, cut 6. Trees now?", 35, "41−6=35."),
        _q("Two-step money: 50 cents, spend 18, find 10. Cents now?", 42, "32+10=42.", difficulty="hard"),
        _q("A puzzle: 13 + 8 − 11 + 4.", 14, "21−11=10, +4=14.", difficulty="hard"),
        _q("Kids 18. Groups of 5 play. Remainder play tag. How many tag?", 3, "15 in groups, 3 left.", difficulty="hard"),
        _q("You walk 400 m, back 150 m, then 80 m more forward. Net from start?", 330, "400−150+80=330.", difficulty="hard"),
        _q("A store: 120 pencils, sell 45, get a box of 24. Stock?", 99, "75+24=99.", difficulty="stretch"),
        _q("Compare two stories: 20−6+3 vs 20−9. Larger result?", 17, "17 vs 11.", ["11", "14", "20"], "stretch"),
        _q("Start 100. Subtract 27, add 8, subtract 10.", 71, "73+8=81, −10=71.", difficulty="stretch"),
        _q("A two-step with extra info: 16 red, 9 blue, it is Tuesday. How many more red than blue?", 7, "16−9=7.", difficulty="stretch"),
        _q("Packs of 6: 4 packs, eat 5 cookies. Left?", 19, "24−5=19.", difficulty="stretch"),
        _q("Goal 80 points. Scores 25, 25, 18. Still need?", 12, "68, need 12.", difficulty="stretch"),
        _q("A number: add 15 to 28 then take away 9.", 34, "43−9=34.", difficulty="stretch"),
        _q("Library: 45 books out, 12 returned, 7 more out. Out now?", 40, "33+7=40.", difficulty="stretch"),
        _q("Two-step compare: Ali 19 stickers, Bo 12, Ali gives Bo 4. Ali now has how many more than Bo?", 0, "15 vs 16? Wait Ali 15, Bo 16, Ali has 0 more (Bo has more). Actually Ali−Bo = −1. Question: Ali now has how many more? 0 if not more.", difficulty="stretch"),
        _q("Ali 19, Bo 12. Ali gives Bo 4. How many does Ali have now?", 15, "19−4=15.", difficulty="stretch"),
        _q("A tank 36 L, use 9 L, refill 5 L. Amount?", 32, "27+5=32.", difficulty="stretch"),
        _q("Three stops: +18, −7, +9 from 20.", 40, "38−7=31, +9=40.", difficulty="stretch"),
        _q("A riddle: I add 8 to a number and get 25, then subtract 6. End?", 19, "Start 17, 25−6=19.", difficulty="stretch"),
        _q("Tickets 60. Sell 24 morning, 17 afternoon. Left?", 19, "36−17=19.", difficulty="stretch"),
        _q("Double a two-step: (9+6)×2? Wait: 9+6 then double.", 30, "15×2=30.", difficulty="stretch"),
        _q("A map: 15 km, then 8 km back, then 20 km on. From start?", 27, "7+20=27.", difficulty="stretch"),
    ]
    # Fix the confusing Ali question - already have a clean follow-up. Remove bad one by filtering
    qs = [q for q in qs if q and "how many more than Bo" not in q["question_text"]]
    return qs


def g2u5():
    qs = []
    for h, m in ((1, 5), (2, 10), (3, 15), (4, 20), (5, 25), (6, 30), (7, 35), (8, 40), (9, 45), (10, 50), (11, 55), (12, 0)):
        qs.append(_q(f"A clock shows hour {h} and {m} minutes. What time?", f"{h}:{m:02d}", f"That is {h}:{m:02d}.", [f"{h}:00", f"{h}:30", f"{(h % 12) + 1}:{m:02d}"]))
    qs += [
        _q("How many minutes from 3:10 to 3:25?", 15, "25−10=15."),
        _q("Half past 8 is…", "8:30", "30 minutes.", ["8:00", "9:00", "8:15"]),
        _q("Quarter to 5 is…", "4:45", "15 minutes before 5.", ["5:15", "5:45", "4:15"]),
        _q("A show starts 2:15 and lasts 30 min. End?", "2:45", "15+30=45.", difficulty="hard"),
        _q("From 9:50 to 10:10 is how many minutes?", 20, "10 to 10:00 is 10, plus 10.", difficulty="hard"),
        _q("Elapsed: 1:20 to 2:05.", 45, "40 min to 2:00 plus 5.", difficulty="hard"),
        _q("A clock 15 minutes slow shows 4:00. Real time?", "4:15", "Add 15.", difficulty="hard"),
        _q("How many 5-minute marks from 12 to 9 on the clock?", 9, "9×5=45 minutes, 9 marks.", difficulty="stretch"),
        _q("A class 45 minutes starting 1:10. End?", "1:55", "10+45=55.", difficulty="stretch"),
        _q("Which is later: 7:45 or 8:05? How many minutes later is 8:05?", 20, "15 to 8:00 plus 5.", difficulty="stretch"),
        _q("Two hours 10 minutes in minutes?", 130, "120+10.", difficulty="stretch"),
        _q("A train 1:55, delay 20 min. New time?", "2:15", "55+20=75 → 2:15.", difficulty="stretch"),
        _q("From 11:40 to 12:15 minutes?", 35, "20+15.", difficulty="stretch"),
        _q("If minute hand on 4, minutes past the hour?", 20, "4×5=20.", difficulty="stretch"),
        _q("A 90-minute movie starts 3:30. End?", "5:00", "3:30+1:30=5:00.", difficulty="stretch"),
        _q("Time until 6:00 if now 5:35?", 25, "25 minutes.", difficulty="stretch"),
        _q("Quarter past 11 plus 20 minutes?", "11:35", "15+20=35.", difficulty="stretch"),
        _q("How many hours and minutes in 150 minutes?", "2 hours 30 minutes", "120+30.", ["2:00", "3:00", "1:50"], "stretch"),
        _q("A clock hands swap? If it looks like 3:00, hour at 3 minute at 12. After 15 min?", "3:15", "Minute on 3.", difficulty="stretch"),
        _q("Elapsed work: 8:45 to 10:00.", 75, "15+60=75 minutes.", difficulty="stretch"),
    ]
    return qs


def g2u6():
    qs = [
        _q("A dime is worth how many cents?", 10, "10 cents."),
        _q("A quarter is how many cents?", 25, "25 cents."),
        _q("3 nickels = ? cents", 15, "3×5=15."),
        _q("2 dimes + 1 nickel = ?", 25, "20+5=25."),
        _q("4 quarters = ? dollars", 1, "100 cents = $1.", ["2", "4", "0"]),
        _q("A dollar is how many cents?", 100, "100 cents."),
        _q("6 dimes = ?", 60, "6×10."),
        _q("1 quarter + 2 dimes + 1 nickel + 4 pennies = ?", 54, "25+20+5+4."),
        _q("How many nickels in a quarter?", 5, "25÷5=5."),
        _q("How many dimes in 80 cents?", 8, "8×10."),
        _q("You have 3 quarters. Cents?", 75, "3×25."),
        _q("A toy is 40¢. You pay 2 dimes and 3 nickels. Enough? Total paid?", 35, "20+15=35, not enough.", difficulty="hard"),
        _q("Item 70¢. You pay $1. Change?", 30, "100−70.", difficulty="hard"),
        _q("Fewest coins to make 30¢ using dimes and nickels? Number of coins?", 3, "3 dimes.", difficulty="hard"),
        _q("2 dollars and 35 cents in cents?", 235, "200+35.", difficulty="hard"),
        _q("A combo: 1 half-dollar (50) + 1 quarter + 1 dime. Total?", 85, "50+25+10.", difficulty="stretch"),
        _q("You buy two 45¢ items. Pay $1. Change?", 10, "90, change 10.", difficulty="stretch"),
        _q("Which is more: 3 quarters or 8 dimes?", 80, "75 vs 80.", ["75", "3", "8"], "stretch"),
        _q("Make $1 with quarters. How many?", 4, "4×25=100.", difficulty="stretch"),
        _q("A piggy: 5 dimes, 4 nickels, 7 pennies. Total cents?", 77, "50+20+7.", difficulty="stretch"),
        _q("Price $1.15. You have 4 quarters. Need how many more cents?", 15, "100, need 15.", difficulty="stretch"),
        _q("Smallest number of coins for 40¢ (quarters/dimes/nickels/pennies)?", 3, "1 quarter + 1 dime + 1 nickel.", difficulty="stretch"),
        _q("Twice 35 cents in cents?", 70, "70¢.", difficulty="stretch"),
        _q("A sandwich $2.50, juice 75¢. Total cents?", 325, "250+75.", difficulty="stretch"),
        _q("Pay $5 for $3.80. Change in cents?", 120, "$1.20.", difficulty="stretch"),
        _q("Count: quarter, quarter, dime, dime, penny.", 61, "50+20+1.", difficulty="stretch"),
        _q("How many nickels equal 3 dimes?", 6, "30 cents / 5.", difficulty="stretch"),
        _q("A mistake: counting a dime as 5¢ undercounts 40¢ of dimes by how much if 4 dimes?", 20, "Each dime short 5, ×4=20.", difficulty="stretch"),
        _q("2 dollars − 65 cents = ? cents", 135, "200−65.", difficulty="stretch"),
        _q("Equal money: 10 dimes vs 2 quarters. Which is more (cents of the greater)?", 100, "100 vs 50.", difficulty="stretch"),
        _q("A vending item 55¢. You insert 2 quarters. Need?", 5, "50, need a nickel.", difficulty="stretch"),
        _q("Roll of 40 nickels in dollars?", 2, "200 cents.", difficulty="stretch"),
        _q("3 dollars 4 dimes 2 pennies in cents?", 342, "300+40+2.", difficulty="stretch"),
        _q("Change from $10 for $6.25?", 375, "$3.75.", difficulty="stretch"),
        _q("If pennies only, 1 dollar needs how many pennies?", 100, "100 pennies.", difficulty="stretch"),
    ]
    return qs


def g2u7():
    return [
        _q("A triangle has ___ sides.", 3, "Three sides."),
        _q("A hexagon has ___ sides.", 6, "Six."),
        _q("A cube has ___ faces.", 6, "Six square faces."),
        _q("A rectangle has ___ right angles.", 4, "Four."),
        _q("Parallel sides never…", "meet", "They stay the same distance.", ["cross", "curve", "end"]),
        _q("A quadrilateral has how many sides?", 4, "Quad means four."),
        _q("Which solid has a circular base and a point: cone or cube?", "cone", "A cone tapers to a point.", ["cube", "sphere", "box"]),
        _q("A pentagon vertices?", 5, "Five corners."),
        _q("Faces of a rectangular prism?", 6, "A box has 6 faces."),
        _q("Edges of a triangular prism?", 9, "Two triangles + 3 rectangles: 9 edges."),
        _q("A circle’s distance through the center is the…", "diameter", "Twice the radius.", ["radius", "chord", "arc"]),
        _q("Two faces of a cube meet at an…", "edge", "An edge is a line segment.", ["vertex only", "curve", "area"]),
        _q("A square is a rectangle: true? (Yes/No as Yes)", "Yes", "All angles 90°, opposite sides equal.", ["No", "Sometimes", "Never"]),
        _q("How many triangular faces on a square pyramid?", 4, "4 triangles + 1 square base."),
        _q("An octagon has how many more sides than a pentagon?", 3, "8−5=3."),
        _q("A net of 6 equal squares can fold to a…", "cube", "Six faces.", difficulty="hard"),
        _q("Count right angles in an L made of two rectangles sharing a side (outer path). Outer right angles?", 6, "Walk the L: 6 outer 90° typically.", difficulty="hard"),
        _q("A shape with 1 pair of parallel sides.", "trapezoid", "Exactly one pair.", difficulty="hard"),
        _q("Vertices of a cube?", 8, "8 corners.", difficulty="hard"),
        _q("A triangular pyramid (tetrahedron) faces?", 4, "4 triangles.", difficulty="stretch"),
        _q("Compose 2 congruent right triangles into a rectangle. Area vs one triangle?", "double", "Rectangle is twice one triangle.", difficulty="stretch"),
        _q("A cylinder nets to 2 circles and a…", "rectangle", "The side unwraps to a rectangle.", difficulty="stretch"),
        _q("How many edges does a square pyramid have?", 8, "4 base + 4 up to apex.", difficulty="stretch"),
        _q("A regular hexagon can be split into how many equilateral triangles?", 6, "From the center.", difficulty="stretch"),
        _q("Which has more edges: cube or square pyramid?", "cube", "12 vs 8.", difficulty="stretch"),
        _q("A closed 4-sided shape with no right angles and one pair parallel is still a…", "trapezoid", "Parallel defines it.", difficulty="stretch"),
        _q("Sphere edges?", 0, "No edges.", difficulty="stretch"),
        _q("A stop-sign octagon lines of symmetry?", 8, "Regular octagon.", difficulty="stretch"),
        _q("Prism vs pyramid: a prism has two ___ faces.", "congruent parallel", "Bases.", difficulty="stretch"),
        _q("Draw a diagonal in a rectangle. How many triangles?", 2, "One diagonal → 2 triangles.", difficulty="stretch"),
        _q("A cube painted, cut 3×3×3. How many small cubes have 3 faces painted?", 8, "The 8 corners.", difficulty="stretch"),
        _q("Name a 3D shape that rolls in any direction.", "sphere", "A ball.", difficulty="stretch"),
        _q("A rhombus with a right angle is a…", "square", "Equal sides + 90°.", difficulty="stretch"),
        _q("How many faces does a pentagonal prism have?", 7, "5 rectangles + 2 pentagons.", difficulty="stretch"),
        _q("An angle smaller than a right angle is…", "acute", "Less than 90°.", difficulty="stretch"),
    ]


def g2u8():
    qs = []
    for n, d in ((1, 2), (1, 4), (3, 4), (1, 3), (2, 3), (1, 8), (3, 8), (1, 6), (5, 6), (2, 5)):
        qs.append(_q(f"A bar split into {d} equal parts with {n} shaded. What fraction?", f"{n}/{d}", f"{n} of {d} equal parts.", [f"{d}/{n}" if n else "1", f"{n}/{d+1}", "1"]))
    qs += [
        _q("Two halves make…", 1, "2/2=1."),
        _q("Which is larger: 1/2 or 1/4 of the same whole?", "1/2", "Fewer pieces means each is bigger.", ["1/4", "same", "0"]),
        _q("3/4 means 3 parts of size…", "1/4", "Unit fraction 1/4.", ["1/3", "3", "4"]),
        _q("A sandwich cut into 4. You eat 1. Left as a fraction?", "3/4", "3 of 4 left."),
        _q("Equal shares: 2 of 2 is…", "1 whole", "2/2=1."),
        _q("Which equals one whole: 4/4 or 3/4?", "4/4", "All parts.", difficulty="hard"),
        _q("Compare 2/4 and 1/2 of the same bar.", "equal", "2/4=1/2.", ["2/4 bigger", "1/2 bigger", "cannot"], difficulty="hard"),
        _q("A pizza 8 slices, eat 3. Fraction eaten?", "3/8", "3 of 8.", difficulty="hard"),
        _q("Shade 1/2 of 8 boxes. How many boxes shaded?", 4, "Half of 8.", difficulty="hard"),
        _q("Which is closer to 1: 3/4 or 1/4?", "3/4", "3/4 is nearer a whole.", difficulty="stretch"),
        _q("2/2 vs 4/4. Greater?", "equal", "Both 1.", difficulty="stretch"),
        _q("A chocolate 6 squares, eat 1/3. Squares eaten?", 2, "6÷3=2.", difficulty="stretch"),
        _q("Unit fraction with 5 equal parts?", "1/5", "One of five.", difficulty="stretch"),
        _q("False: 1/8 > 1/3 because 8>3. The larger fraction is…", "1/3", "Larger denominator → smaller unit piece.", difficulty="stretch"),
        _q("3 halves of the same cake is how many cakes?", "1 and 1/2", "3/2.", difficulty="stretch"),
        _q("A rectangle split in 2 then each half in 2. Each small is…", "1/4", "Halves of halves.", difficulty="stretch"),
        _q("You need 1/2 cup. You have a 1/4 cup scoop. How many scoops?", 2, "Two fourths.", difficulty="stretch"),
        _q("Fraction of a dozen that is 3 eggs?", "1/4", "3/12=1/4.", difficulty="stretch"),
        _q("If 4/4 is a whole, 5/4 is…", "more than 1", "Improper.", difficulty="stretch"),
        _q("Two students share a candy bar equally. Each gets…", "1/2", "Two equal shares.", difficulty="stretch"),
        _q("A spinner 4 equal parts, 1 red. P(red) as a fraction?", "1/4", "One of four.", difficulty="stretch"),
        _q("Which pair is equal: 2/6 and 1/3?", "yes they are equal", "2/6=1/3.", difficulty="stretch"),
        _q("Leftover: 5/8 eaten, fraction left?", "3/8", "8−5=3.", difficulty="stretch"),
        _q("A number line from 0 to 1 with 4 ticks in between (fifths). First tick after 0 is…", "1/5", "Five equal spaces.", difficulty="stretch"),
        _q("3 people share 1 whole equally. Each?", "1/3", "Three equal parts.", difficulty="stretch"),
    ]
    return qs


def extra_questions(title: str):
    """Return unique extra items for a unit title (Easy→Stretch order)."""
    from question_banks_more import extra_questions as more

    t = title.lower()
    table = [
        ("first grade math unit 1", g1u1),
        ("first grade math unit 2", g1u2),
        ("first grade math unit 3", g1u3),
        ("first grade math unit 4", g1u4),
        ("first grade math unit 5", g1u5),
        ("first grade math unit 6", g1u6),
        ("first grade math unit 7", g1u7),
        ("first grade math unit 8", g1u8),
        ("second grade math unit 1", g2u1),
        ("second grade math unit 2", g2u2),
        ("second grade math unit 3", g2u3),
        ("second grade math unit 4", g2u4),
        ("second grade math unit 5", g2u5),
        ("second grade math unit 6", g2u6),
        ("second grade math unit 7", g2u7),
        ("second grade math unit 8", g2u8),
    ]
    for key, fn in table:
        if key in t:
            return [q for q in fn() if q]
    return [q for q in more(title) if q]

