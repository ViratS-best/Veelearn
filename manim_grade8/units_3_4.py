"""Units 3–4: slope and functions."""

U3 = {
    "num": 3,
    "title": "Slope and Linear Graphs",
    "subtitle": "Rise over run, y = mx + b, and parallel lines",
    "file": "unit-3-slope",
    "parts": [
        {
            "title": "Slope is rise over run",
            "visual": "slope",
            "beats": [
                "Slope m is rise over run: change in y divided by change in x.",
                "From (2, 3) to (4, 4): rise 1, run 2, so m = 1/2.",
                "Positive slope climbs left to right. Negative slope falls.",
                "A horizontal line has slope 0. A vertical line has undefined slope.",
                "Count the grid: up 1, right 2 is the same as up 2, right 4.",
            ],
            "examples": [
                {
                    "problem": "Find the slope from (2, 3) to (4, 4).",
                    "steps": [
                        "Rise = 4 − 3 = 1",
                        "Run = 4 − 2 = 2",
                        "m = 1/2",
                    ],
                    "answer": "1/2",
                },
                {
                    "problem": "Find the slope from (1, 5) to (3, 1).",
                    "steps": [
                        "Rise = 1 − 5 = −4",
                        "Run = 3 − 1 = 2",
                        "m = −2",
                    ],
                    "answer": "−2",
                },
                {
                    "problem": "What is the slope of a horizontal line through (0, 4)?",
                    "steps": [
                        "y never changes, so rise = 0",
                        "Run can be any nonzero number",
                        "0 divided by a number is 0",
                    ],
                    "answer": "0",
                },
            ],
        },
        {
            "title": "y = mx + b",
            "visual": "slope",
            "beats": [
                "m is the slope. b is the y-intercept, where the line crosses the y-axis.",
                "y = (1/2)x + 2 crosses at (0, 2) and climbs 1 for every run of 2.",
                "If b is missing, the intercept is 0: y = 3x goes through the origin.",
                "x = 4 is vertical. y = −1 is horizontal.",
                "You can graph from b, then use m to step to the next point.",
            ],
            "examples": [
                {
                    "problem": "For y = (1/2)x + 2, name m and b.",
                    "steps": [
                        "The number in front of x is the slope",
                        "The constant is the intercept",
                        "m = 1/2, b = 2",
                    ],
                    "answer": "m = 1/2, b = 2",
                },
                {
                    "problem": "Where does y = −3x + 5 cross the y-axis?",
                    "steps": [
                        "Set x = 0",
                        "y = 5",
                        "The point is (0, 5)",
                    ],
                    "answer": "(0, 5)",
                },
                {
                    "problem": "Write y = 3x in slope-intercept form and name b.",
                    "steps": [
                        "It is already y = mx + b with b = 0",
                        "m = 3",
                        "The line goes through the origin",
                    ],
                    "answer": "b = 0",
                },
            ],
        },
        {
            "title": "Equation from two points",
            "visual": "slope",
            "beats": [
                "Find m from two points, then plug one point into y = mx + b to get b.",
                "Through (0, 4) with slope −2: already have b, so y = −2x + 4.",
                "Through (2, 3) and (4, 7): m = 2, then 3 = 2(2) + b, so b = −1.",
                "A graph is just the picture of that equation.",
                "Check the second point in the finished equation.",
            ],
            "examples": [
                {
                    "problem": "A line has slope −2 and y-intercept 4. Write y = mx + b.",
                    "steps": [
                        "m = −2, b = 4",
                        "Substitute into the template",
                        "y = −2x + 4",
                    ],
                    "answer": "y = −2x + 4",
                },
                {
                    "problem": "A line goes through (2, 3) and (4, 7). Find the equation.",
                    "steps": [
                        "m = (7 − 3)/(4 − 2) = 4/2 = 2",
                        "3 = 2(2) + b, so b = −1",
                        "y = 2x − 1",
                    ],
                    "answer": "y = 2x − 1",
                },
                {
                    "problem": "A line through (0, −3) with slope 1/3. Equation?",
                    "steps": [
                        "The point (0, −3) is the intercept",
                        "b = −3, m = 1/3",
                        "y = (1/3)x − 3",
                    ],
                    "answer": "y = (1/3)x − 3",
                },
            ],
        },
        {
            "title": "Parallel and perpendicular",
            "visual": "slope",
            "beats": [
                "Parallel lines have equal slopes and never meet.",
                "Perpendicular lines have slopes that are negative reciprocals: 2 and −1/2.",
                "y = 2x + 1 is parallel to y = 2x − 4.",
                "y = 2x + 1 is perpendicular to y = (−1/2)x + 5.",
                "A horizontal line is perpendicular to a vertical line.",
            ],
            "examples": [
                {
                    "problem": "Is y = 2x + 1 parallel to y = 2x − 4?",
                    "steps": [
                        "Both slopes are 2",
                        "Intercepts differ, so they are not the same line",
                        "Equal slopes, different b, so parallel",
                    ],
                    "answer": "yes, parallel",
                },
                {
                    "problem": "A line perpendicular to y = 2x + 1 has what slope?",
                    "steps": [
                        "The given slope is 2",
                        "Negative reciprocal: flip 2 to 1/2, then minus",
                        "m = −1/2",
                    ],
                    "answer": "−1/2",
                },
                {
                    "problem": "Are y = 3x and y = −3x perpendicular?",
                    "steps": [
                        "Negative reciprocal of 3 is −1/3, not −3",
                        "These slopes are opposites, not flips",
                        "They are not perpendicular",
                    ],
                    "answer": "no",
                },
            ],
        },
        {
            "title": "Intercepts and special lines",
            "visual": "slope",
            "beats": [
                "y-intercept: set x = 0. x-intercept: set y = 0 and solve.",
                "For 2x + 4y = 8: y-intercept (0, 2), x-intercept (4, 0).",
                "x = 3 is a vertical line. Slope is undefined.",
                "y = −2 is a horizontal line. Slope is 0.",
                "Intercepts are the fastest two points to plot from standard form.",
            ],
            "examples": [
                {
                    "problem": "Find both intercepts of 2x + 4y = 8.",
                    "steps": [
                        "x = 0, so 4y = 8, y = 2, and the point is (0, 2)",
                        "y = 0, so 2x = 8, x = 4, and the point is (4, 0)",
                        "Those two points draw the line",
                    ],
                    "answer": "(0, 2) and (4, 0)",
                },
                {
                    "problem": "Describe the graph of x = 3.",
                    "steps": [
                        "x is always 3, y can be anything",
                        "A vertical line through 3 on the x-axis",
                        "Slope is undefined",
                    ],
                    "answer": "vertical line x = 3",
                },
                {
                    "problem": "Describe the graph of y = −2.",
                    "steps": [
                        "y is always −2",
                        "A horizontal line",
                        "Slope is 0",
                    ],
                    "answer": "horizontal line y = −2",
                },
            ],
        },
        {
            "title": "Linear graphs in stories",
            "visual": "slope",
            "beats": [
                "A phone plan: y = 20 + 5x. 20 dollars start, 5 dollars per extra gig.",
                "m is the rate. b is the starting amount.",
                "When two plans are graphed, the meeting point is a system.",
                "A negative slope in a story often means something is draining.",
                "Read a point as a pair: after 3 hours, the tank has 12 liters.",
            ],
            "examples": [
                {
                    "problem": "A plan costs 20 dollars plus 5 dollars per gig. Write y = mx + b.",
                    "steps": [
                        "Start is 20, so b = 20",
                        "Rate is 5 per gig, so m = 5",
                        "y = 5x + 20",
                    ],
                    "answer": "y = 5x + 20",
                },
                {
                    "problem": "A tank starts at 40 L and drains 4 L per hour. Equation?",
                    "steps": [
                        "b = 40, m = −4",
                        "y = −4x + 40",
                        "After 3 hours: y = 28 L",
                    ],
                    "answer": "y = −4x + 40",
                },
                {
                    "problem": "What does the point (2, 30) mean on y = 5x + 20?",
                    "steps": [
                        "x = 2, y = 30",
                        "Check: 5(2)+20 = 30, it sits on the line",
                        "After 2 gigs, the cost is 30 dollars",
                    ],
                    "answer": "2 gigs cost 30 dollars",
                },
            ],
        },
    ],
}

U4 = {
    "num": 4,
    "title": "Functions",
    "subtitle": "One input, one output, linear vs nonlinear",
    "file": "unit-4-functions",
    "parts": [
        {
            "title": "One input, one output",
            "visual": "function",
            "beats": [
                "A function assigns each input exactly one output.",
                "A vertical line that hits a graph twice means it is not a function.",
                "Tables: if an x shows two different y values, it is not a function.",
                "Machines, graphs, and equations can all be functions, or fail the test.",
                "The set of allowed inputs is the domain. Outputs are the range.",
            ],
            "examples": [
                {
                    "problem": "Is {(1, 2), (1, 5), (3, 4)} a function?",
                    "steps": [
                        "Input 1 is paired with both 2 and 5",
                        "One input, two outputs",
                        "Not a function",
                    ],
                    "answer": "no",
                },
                {
                    "problem": "Is {(1, 4), (2, 4), (3, 5)} a function?",
                    "steps": [
                        "Each x appears once",
                        "Two different x values may share a y",
                        "Yes, it is a function",
                    ],
                    "answer": "yes",
                },
                {
                    "problem": "A circle fails the vertical-line test. Why?",
                    "steps": [
                        "A vertical line through the middle hits twice",
                        "Those two points share an x",
                        "Two outputs for one input",
                    ],
                    "answer": "two y-values for one x",
                },
            ],
        },
        {
            "title": "Function notation",
            "visual": "function",
            "beats": [
                "f(x) means the output when the input is x. It is not f times x.",
                "If f(x) = 2x - 1, then f(3) = 5 and f(0) = -1.",
                "To solve f(x) = 7, set 2x - 1 = 7.",
                "g(t) is the same idea with a different letter.",
                "Read f(3) as 'f of 3'.",
            ],
            "examples": [
                {
                    "problem": "f(x) = 2x - 1. Find f(3).",
                    "steps": [
                        "Replace every x with 3",
                        "2(3) - 1 = 6 - 1",
                        "f(3) = 5",
                    ],
                    "answer": "5",
                },
                {
                    "problem": "f(x) = 2x - 1. Solve f(x) = 7.",
                    "steps": [
                        "2x - 1 = 7",
                        "2x = 8",
                        "x = 4",
                    ],
                    "answer": "x = 4",
                },
                {
                    "problem": "f(x) = x² - 1. Find f(-3).",
                    "steps": [
                        "(-3)² - 1",
                        "9 - 1 = 8",
                        "The input can be negative",
                    ],
                    "answer": "8",
                },
            ],
        },
        {
            "title": "Linear functions",
            "visual": "function",
            "beats": [
                "A linear function has a constant rate. Its graph is a straight line.",
                "f(x) = mx + b. Equal x-steps produce equal y-steps.",
                "In a table, first differences of y are constant when x-steps are 1.",
                "f(x) = 3 is linear with slope 0, a horizontal line.",
                "Not every formula is linear. x² bends.",
            ],
            "examples": [
                {
                    "problem": "Is f(x) = 3x - 2 linear?",
                    "steps": [
                        "It matches mx + b with m = 3, b = -2",
                        "The graph is a straight line",
                        "Yes",
                    ],
                    "answer": "yes",
                },
                {
                    "problem": "Table: x = 0,1,2 and y = 4,7,10. Linear?",
                    "steps": [
                        "y jumps +3, then +3",
                        "Constant first differences",
                        "Yes, slope 3, intercept 4",
                    ],
                    "answer": "yes, f(x) = 3x + 4",
                },
                {
                    "problem": "Is f(x) = 3 a linear function?",
                    "steps": [
                        "y = 0·x + 3",
                        "Slope 0, still a line",
                        "Yes, a constant function is linear",
                    ],
                    "answer": "yes, horizontal",
                },
            ],
        },
        {
            "title": "Nonlinear functions",
            "visual": "function",
            "beats": [
                "Nonlinear graphs bend, jump, or curve.",
                "f(x) = x² is a parabola. First differences are not constant.",
                "f(x) = 2ˣ grows by multiplying, not by adding a fixed amount.",
                "A V-shape like |x| is nonlinear even though each piece is a line.",
                "If a table’s y-jumps keep changing, it is not linear.",
            ],
            "examples": [
                {
                    "problem": "Is f(x) = x² linear?",
                    "steps": [
                        "Inputs 1, 2, 3 give 1, 4, 9",
                        "Jumps of +3 then +5, not constant",
                        "The graph is a parabola",
                    ],
                    "answer": "no",
                },
                {
                    "problem": "Is f(x) = 2ˣ linear?",
                    "steps": [
                        "x = 1, 2, 3 give 2, 4, 8",
                        "Jumps double each time",
                        "Exponential, not a line",
                    ],
                    "answer": "no",
                },
                {
                    "problem": "Table: 1, 4, 9, 16 for x = 1, 2, 3, 4. Linear?",
                    "steps": [
                        "Differences: 3, 5, 7",
                        "Those are not equal",
                        "Nonlinear (squares)",
                    ],
                    "answer": "no",
                },
            ],
        },
        {
            "title": "Machines, tables, graphs",
            "visual": "function",
            "beats": [
                "The same function can be a machine, a table, a graph, or a formula.",
                "To move from a graph to a table, read points that sit on the curve.",
                "To move from a table to a graph, plot the pairs.",
                "A closed circle is on the graph. An open circle is not.",
                "Match all three pictures before you trust a rule.",
            ],
            "examples": [
                {
                    "problem": "A machine doubles, then subtracts 1. Write f(x).",
                    "steps": [
                        "Double: 2x",
                        "Then subtract 1",
                        "f(x) = 2x - 1",
                    ],
                    "answer": "f(x) = 2x - 1",
                },
                {
                    "problem": "From the table (0, 1), (1, 3), (2, 5), guess a linear rule.",
                    "steps": [
                        "Slope = 2",
                        "When x = 0, y = 1, so b = 1",
                        "f(x) = 2x + 1",
                    ],
                    "answer": "f(x) = 2x + 1",
                },
                {
                    "problem": "f(x) = 2x - 1. Fill f(0), f(1), f(2).",
                    "steps": [
                        "f(0) = -1",
                        "f(1) = 1",
                        "f(2) = 3",
                    ],
                    "answer": "-1, 1, 3",
                },
            ],
        },
        {
            "title": "Functions in context",
            "visual": "function",
            "beats": [
                "C(n) = 8n + 12 might be a club fee: 12 dollars start, 8 per person.",
                "The input must make sense: n is a count of people, not -3.5.",
                "f(0) is the start. The slope is the extra cost per extra person.",
                "A nonlinear context: area of a square is s².",
                "Always name the units of the output.",
            ],
            "examples": [
                {
                    "problem": "C(n) = 8n + 12. What is C(5)?",
                    "steps": [
                        "8(5) + 12 = 40 + 12",
                        "C(5) = 52",
                        "Five people cost 52 dollars",
                    ],
                    "answer": "52 dollars",
                },
                {
                    "problem": "What does C(0) = 12 mean in that club story?",
                    "steps": [
                        "n = 0 people",
                        "You still pay the 12-dollar start",
                        "It is the intercept, the starting fee",
                    ],
                    "answer": "starting fee of 12 dollars",
                },
                {
                    "problem": "Area A(s) = s². Find A(6).",
                    "steps": [
                        "6² = 36",
                        "The output is square units",
                        "A side of 6 gives area 36",
                    ],
                    "answer": "36 square units",
                },
            ],
        },
    ],
}
