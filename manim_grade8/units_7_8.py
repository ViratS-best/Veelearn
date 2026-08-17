"""Units 7–8: Pythagoras, cylinders, scatter plots."""

U7 = {
    "num": 7,
    "title": "Pythagorean Theorem and Cylinders",
    "subtitle": "a² + b² = c², distance, and V = πr²h",
    "file": "unit-7-pythagoras",
    "parts": [
        {
            "title": "a² + b² = c²",
            "visual": "pythag",
            "beats": [
                "A right triangle has one 90° angle. Legs a and b meet there. c is the hypotenuse.",
                "Pythagoras: a² + b² = c². Legs 3 and 4: 9 + 16 = 25, so c = 5.",
                "5-12-13 and 8-15-17 are other famous triples.",
                "If you know c and one leg, subtract, then take a square root.",
                "The little square in the corner marks the right angle.",
            ],
            "examples": [
                {
                    "problem": "Legs 6 and 8. Find the hypotenuse.",
                    "steps": [
                        "This is 3-4-5 with every side ×2",
                        "6² + 8² = 36 + 64 = 100",
                        "c = 10",
                    ],
                    "answer": "10",
                },
                {
                    "problem": "Legs 5 and 12. Find the hypotenuse.",
                    "steps": [
                        "5² + 12² = 25 + 144 = 169",
                        "13² = 169",
                        "c = 13",
                    ],
                    "answer": "13",
                },
                {
                    "problem": "Hypotenuse 13, one leg 5. Find the other leg.",
                    "steps": [
                        "a² + 25 = 169",
                        "a² = 144",
                        "a = 12",
                    ],
                    "answer": "12",
                },
            ],
        },
        {
            "title": "The converse: is it right?",
            "visual": "pythag",
            "beats": [
                "If three sides already satisfy a² + b² = c², the triangle is right.",
                "3, 4, 5: 9 + 16 = 25. Right. 6, 8, 10 is the same family ×2.",
                "2, 3, 4: 4 + 9 = 13, and 4² = 16. Not equal, so not right.",
                "Always test the two shorter sides against the longest.",
                "A 13 ft ladder to a 12 ft wall needs 5 ft of ground: 5-12-13 standing up.",
            ],
            "examples": [
                {
                    "problem": "Do sides 6, 8, and 10 make a right triangle?",
                    "steps": [
                        "Longest is 10, so c = 10",
                        "6² + 8² = 100 = 10²",
                        "Yes: a scaled 3-4-5",
                    ],
                    "answer": "yes",
                },
                {
                    "problem": "Do sides 2, 3, and 4 make a right triangle?",
                    "steps": [
                        "Longest is 4",
                        "2² + 3² = 4 + 9 = 13",
                        "4² = 16, and 13 ≠ 16",
                    ],
                    "answer": "no",
                },
                {
                    "problem": "A 13 ft ladder reaches 12 ft up a wall. Ground distance?",
                    "steps": [
                        "Hypotenuse 13, one leg 12",
                        "169 - 144 = 25",
                        "Ground leg 5 ft",
                    ],
                    "answer": "5 ft",
                },
            ],
        },
        {
            "title": "Distance is Pythagoras on a graph",
            "visual": "pythag",
            "beats": [
                "From (1, 2) to (4, 6) the run is 3 and the rise is 4. Distance = 5.",
                "Formula: sqrt((x2 - x1)^2 + (y2 - y1)^2). Same theorem, coordinate clothes.",
                "From (0, 0) to (6, 8) is 10. From (0, 0) to (5, 12) is 13.",
                "If points share an x, the segment is vertical: just |y2 - y1|.",
                "Signs square away: (-3)^2 is 9. Distance is never negative.",
            ],
            "examples": [
                {
                    "problem": "Distance from (1, 2) to (4, 6).",
                    "steps": [
                        "dx = 3, dy = 4",
                        "3² + 4² = 25",
                        "Distance 5",
                    ],
                    "answer": "5",
                },
                {
                    "problem": "Distance from (0, 0) to (6, 8).",
                    "steps": [
                        "Another 3-4-5 scaled by 2",
                        "36 + 64 = 100",
                        "Distance 10",
                    ],
                    "answer": "10",
                },
                {
                    "problem": "Distance from (-1, 4) to (2, 8).",
                    "steps": [
                        "dx = 3, dy = 4",
                        "9 + 16 = 25",
                        "Distance 5",
                    ],
                    "answer": "5",
                },
            ],
        },
        {
            "title": "Cylinders: V = πr²h",
            "visual": "cylinder",
            "beats": [
                "A cylinder has two circular bases and a straight height.",
                "Volume is base area times height. The base is a circle, so V = πr²h.",
                "Use 3.14 for π unless a problem says otherwise.",
                "r = 2, h = 5 → 3.14 × 4 × 5 = 62.8 cubic units.",
                "Square r first, then multiply by π, then by h.",
            ],
            "examples": [
                {
                    "problem": "Use 3.14. Radius 2, height 5. Volume?",
                    "steps": [
                        "r² = 4",
                        "3.14 × 4 = 12.56",
                        "12.56 × 5 = 62.8",
                    ],
                    "answer": "62.8",
                },
                {
                    "problem": "Use 3.14. Radius 3, height 4. Volume?",
                    "steps": [
                        "r² = 9",
                        "3.14 × 9 = 28.26",
                        "28.26 × 4 = 113.04",
                    ],
                    "answer": "113.04",
                },
                {
                    "problem": "Use 3.14. Radius 5, height 2. Volume?",
                    "steps": [
                        "r² = 25",
                        "3.14 × 25 = 78.5",
                        "78.5 × 2 = 157",
                    ],
                    "answer": "157",
                },
            ],
        },
        {
            "title": "Radius, diameter, and π ≈ 3.14",
            "visual": "cylinder",
            "beats": [
                "Diameter is twice the radius. Never plug the diameter into r².",
                "Diameter 6 means r = 3. With h = 5: 3.14 × 9 × 5 = 141.3.",
                "(πr)²h would be wrong. Square r alone.",
                "If height doubles and r stays put, volume doubles.",
                "If r doubles, r² quadruples, so volume ×4.",
            ],
            "examples": [
                {
                    "problem": "A tank has diameter 6 and height 5. Use 3.14. Volume?",
                    "steps": [
                        "r = 3, not 6",
                        "r² = 9",
                        "3.14 × 9 × 5 = 141.3",
                    ],
                    "answer": "141.3",
                },
                {
                    "problem": "r = 4, h = 3, π = 3.14. Volume?",
                    "steps": [
                        "r² = 16",
                        "3.14 × 16 = 50.24",
                        "50.24 × 3 = 150.72",
                    ],
                    "answer": "150.72",
                },
                {
                    "problem": "r = 1, h = 10, π = 3.14. Volume?",
                    "steps": [
                        "r² = 1",
                        "3.14 × 1 × 10",
                        "31.4",
                    ],
                    "answer": "31.4",
                },
            ],
        },
        {
            "title": "Ladders, maps, and cans",
            "visual": "pythag",
            "beats": [
                "Name the shape first: right triangle or cylinder.",
                "A bird flying diagonally uses the hypotenuse. A street grid might not.",
                "A grain silo is a cylinder. Match units before you use 3.14.",
                "If numbers look like 6-8-10 or 9-12-15, you have a scaled triple.",
                "High school will add cones and spheres. πr²h is the first curved solid.",
            ],
            "examples": [
                {
                    "problem": "A 13 ft ladder reaches 12 ft up a wall. How far is the base?",
                    "steps": [
                        "Right triangle, not a cylinder",
                        "169 - 144 = 25",
                        "5 ft from the wall",
                    ],
                    "answer": "5 ft",
                },
                {
                    "problem": "Map points (0, 0) and (9, 12). Straight-line distance?",
                    "steps": [
                        "9-12-15 triple",
                        "81 + 144 = 225",
                        "Distance 15",
                    ],
                    "answer": "15",
                },
                {
                    "problem": "A can has r = 2 and h = 5. Use 3.14. How much does it hold?",
                    "steps": [
                        "Cylinder: V = πr²h",
                        "3.14 × 4 × 5",
                        "62.8 cubic units",
                    ],
                    "answer": "62.8",
                },
            ],
        },
    ],
}

U8 = {
    "num": 8,
    "title": "Scatter Plots and Data",
    "subtitle": "Association, best-fit lines, tables, and two groups",
    "file": "unit-8-data",
    "parts": [
        {
            "title": "Scatter plots and association",
            "visual": "scatter",
            "beats": [
                "A scatter plot is a cloud of (x, y) points, one pair per person or object.",
                "Positive association: the cloud climbs as you move right.",
                "Negative association: the cloud falls as you move right.",
                "No association: a shapeless blob. x does not help you guess y.",
                "Clusters: two separate clumps, not one sloping cloud.",
                "A tight cigar is strong. A wide spray that still slopes is weak.",
            ],
            "examples": [
                {
                    "problem": "Study hours vs scores trend up. What association is that?",
                    "steps": [
                        "Both variables tend to increase together",
                        "That is the definition of positive association",
                        "The cloud can still be messy",
                    ],
                    "answer": "positive association",
                },
                {
                    "problem": "Car age vs value trends down. Association?",
                    "steps": [
                        "Age up, value down",
                        "One increases while the other decreases",
                        "Negative association",
                    ],
                    "answer": "negative association",
                },
                {
                    "problem": "Shoe size vs test score looks like a blob. Association?",
                    "steps": [
                        "No climb and no fall",
                        "x does not help predict y",
                        "No association",
                    ],
                    "answer": "no association",
                },
            ],
        },
        {
            "title": "Line of best fit",
            "visual": "scatter",
            "beats": [
                "A line of best fit follows the trend. It does not need to hit every point.",
                "Slope 2 means y tends to rise about 2 when x rises 1.",
                "Interpolation: use the line between the smallest and largest data x.",
                "Extrapolation: go outside that range. Riskier.",
                "You cannot read one person's exact y from the line. It is a typical path.",
            ],
            "examples": [
                {
                    "problem": "A fitted line has slope 2. What does that say?",
                    "steps": [
                        "Slope is rise over run for the model",
                        "When x increases by 1, y tends to increase by 2",
                        "Individual points still scatter",
                    ],
                    "answer": "y tends to rise 2 when x rises 1",
                },
                {
                    "problem": "Should a best-fit line hit every point?",
                    "steps": [
                        "Points sit above and below the trend",
                        "Forcing every point would zigzag, not model",
                        "No — it is a compromise",
                    ],
                    "answer": "no",
                },
                {
                    "problem": "Using the line past the last data x is called…",
                    "steps": [
                        "Inside the x-range is interpolation",
                        "Outside is extrapolation",
                        "Extrapolation carries extra risk",
                    ],
                    "answer": "extrapolation",
                },
            ],
        },
        {
            "title": "Outliers and reading a model",
            "visual": "scatter",
            "beats": [
                "An outlier sits far from the rest of the cloud.",
                "It can pull the fitted line toward itself.",
                "A strong association looks tight around the trend.",
                "If a proposed line floats far above most points, question the line.",
                "A scatter needs two numeric measurements. Names vs scores is the wrong picture.",
            ],
            "examples": [
                {
                    "problem": "Why can't you read one exact score from a fitted line?",
                    "steps": [
                        "Points vary around the trend",
                        "The line is a model of typical change",
                        "A new student can sit above or below it",
                    ],
                    "answer": "points vary around the trend",
                },
                {
                    "problem": "A point far from the cluster is called an…",
                    "steps": [
                        "It does not follow the cloud",
                        "It can tug the slope",
                        "Outlier",
                    ],
                    "answer": "outlier",
                },
                {
                    "problem": "A weak positive association looks like…",
                    "steps": [
                        "The cloud still rises to the right",
                        "But the points are spread",
                        "Trend is there, noisy",
                    ],
                    "answer": "rising, but spread out",
                },
            ],
        },
        {
            "title": "Two-way tables",
            "visual": "scatter",
            "beats": [
                "A two-way table counts two categorical variables.",
                "Rows might be sport / no sport. Columns might be band / no band.",
                "Each cell is a joint count: that row and that column together.",
                "Relative frequency is a count divided by the grand total. 12 of 40 is 12/40 = 30%.",
                "Among soccer players vs among all students are different questions.",
                "15 of 50 is the same idea: 15/50 = 0.3.",
            ],
            "examples": [
                {
                    "problem": "18 play soccer, 10 of those also play basketball. Soccer only?",
                    "steps": [
                        "18 - 10 = 8",
                        "Those 8 play soccer but not basketball",
                        "8 students",
                    ],
                    "answer": "8",
                },
                {
                    "problem": "12 of 40 students play band. Relative frequency?",
                    "steps": [
                        "Part over total",
                        "12/40",
                        "That is 30%",
                    ],
                    "answer": "12/40 or 30%",
                },
                {
                    "problem": "15 of 50 is what decimal relative frequency?",
                    "steps": [
                        "15 / 50",
                        "0.3",
                        "Same idea as 30%",
                    ],
                    "answer": "0.3",
                },
            ],
        },
        {
            "title": "Compare two groups",
            "visual": "scatter",
            "beats": [
                "Two box plots on one scale compare a typical value and spread.",
                "Group A median 8 vs Group B median 7: A is typically a bit higher.",
                "That is not 'every A score beats every B score.' Overlap is normal.",
                "A longer box means more spread in the middle 50%. IQR = Q3 - Q1.",
                "Write two sentences: one about center, one about spread.",
            ],
            "examples": [
                {
                    "problem": "Group A median 8, Group B median 7. What can you say?",
                    "steps": [
                        "Medians describe a typical value",
                        "8 is higher than 7",
                        "A is typically higher; check spread separately",
                    ],
                    "answer": "A is typically higher",
                },
                {
                    "problem": "Q1 = 6 and Q3 = 11. IQR?",
                    "steps": [
                        "IQR = Q3 - Q1",
                        "11 - 6 = 5",
                        "That is the middle-50% width",
                    ],
                    "answer": "5",
                },
                {
                    "problem": "A longer box on a box plot means…",
                    "steps": [
                        "The box runs from Q1 to Q3",
                        "A longer box is a larger IQR",
                        "More spread in the middle 50%",
                    ],
                    "answer": "more spread",
                },
            ],
        },
        {
            "title": "Choose a display and a sentence",
            "visual": "scatter",
            "beats": [
                "Hours vs score → scatter. Band vs sport → two-way table.",
                "Two classes' test scores → side-by-side box plots.",
                "Relative frequency lets you compare groups of different sizes.",
                "Finish with a sentence a person could use.",
                "Match the data type to the picture, then say what the picture means.",
            ],
            "examples": [
                {
                    "problem": "Hours studied and quiz scores for 30 students. Best display?",
                    "steps": [
                        "Two numeric variables",
                        "A scatter plot, then a line of best fit if it trends",
                        "A two-way table would need categories",
                    ],
                    "answer": "a scatter plot",
                },
                {
                    "problem": "Band vs no-band, and sport vs no-sport. Best display?",
                    "steps": [
                        "Two categorical variables",
                        "Counts in rows and columns",
                        "A two-way table",
                    ],
                    "answer": "a two-way table",
                },
                {
                    "problem": "Two classes' test scores. Best display?",
                    "steps": [
                        "One numeric measure, two groups",
                        "Compare center and spread",
                        "Side-by-side box plots",
                    ],
                    "answer": "two box plots",
                },
            ],
        },
    ],
}
