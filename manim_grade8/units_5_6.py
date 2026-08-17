"""Units 5–6: complex two-variable systems."""

U5 = {
    "num": 5,
    "title": "Systems by Substitution",
    "subtitle": "Two equations, two unknowns: isolate, then plug in",
    "file": "unit-5-substitution",
    "parts": [
        {
            "title": "A system is two equations",
            "visual": "system",
            "beats": [
                "A 2-variable system is two equations sharing x and y.",
                "The solution is an ordered pair like (2, 3) that sits on both lines.",
                "Graphically: the meeting point. Algebraically: substitution or elimination.",
                "Still only two letters. Eighth grade makes the algebra heavier, not a third variable.",
                "Always check the pair in both original equations. (2, 3) fits 3x + 2y = 12.",
            ],
            "examples": [
                {
                    "problem": "Does (2, 3) solve 3x + 2y = 12 and 2x + 5y = 19?",
                    "steps": [
                        "3(2) + 2(3) = 6 + 6 = 12",
                        "2(2) + 5(3) = 4 + 15 = 19",
                        "Both true, so yes",
                    ],
                    "answer": "yes",
                },
                {
                    "problem": "Does (0, 0) solve 3x + 2y = 12?",
                    "steps": [
                        "0 + 0 = 0",
                        "0 is not 12",
                        "The origin is not on that line",
                    ],
                    "answer": "no",
                },
                {
                    "problem": "Two crossing lines have how many solutions?",
                    "steps": [
                        "They meet at exactly one point",
                        "That point is one ordered pair",
                        "One solution",
                    ],
                    "answer": "one ordered pair",
                },
            ],
        },
        {
            "title": "Substitute when y is solved",
            "visual": "system",
            "beats": [
                "If one equation is already y equals an expression, plug that expression into the other.",
                "y = 2x − 1 into 2(x + 3) + 3y = 11 → 2x + 6 + 6x − 3 = 11 → x = 1, y = 1.",
                "y = 3x + 1 into x + 2y = 16 → x + 6x + 2 = 16 → x = 2, y = 7.",
                "After you find x = 3, go back to y = 4x − 3 to get y = 9, so (3, 9).",
                "Write the ordered pair (6, 2), not just the x value.",
            ],
            "examples": [
                {
                    "problem": "y = 2x − 1 and 2(x + 3) + 3y = 11. Find the pair.",
                    "steps": [
                        "2x + 6 + 3(2x − 1) = 11",
                        "2x + 6 + 6x − 3 = 11 → 8x = 8 → x = 1",
                        "y = 2(1) − 1 = 1",
                    ],
                    "answer": "(1, 1)",
                },
                {
                    "problem": "y = 3x + 1 and x + 2y = 16. Find x and y.",
                    "steps": [
                        "x + 2(3x + 1) = 16",
                        "x + 6x + 2 = 16 → 7x = 14 → x = 2",
                        "y = 3(2) + 1 = 7",
                    ],
                    "answer": "(2, 7)",
                },
                {
                    "problem": "y = 4x − 3 into 2x + y = 15. Find x.",
                    "steps": [
                        "2x + (4x − 3) = 15",
                        "6x − 3 = 15 → 6x = 18",
                        "x = 3, then y = 9",
                    ],
                    "answer": "(3, 9)",
                },
            ],
        },
        {
            "title": "Isolate first, then substitute",
            "visual": "system",
            "beats": [
                "If nothing is isolated, solve the easier equation for one letter first.",
                "x = 4 − 2y into 3x + y = 7 → 12 − 6y + y = 7 → y = 1, x = 2.",
                "y = x/2 into x + 2y = 12 → x + x = 12 → x = 6, y = 3.",
                "Distribute after you substitute. y = x + 1 into 2(3x − y) = 10 gives (3, 4).",
                "Fractions are legal. A pair like (3.5, 1) can be a solution.",
            ],
            "examples": [
                {
                    "problem": "x = 4 − 2y and 3x + y = 7. Find y.",
                    "steps": [
                        "3(4 − 2y) + y = 7",
                        "12 − 6y + y = 7 → −5y = −5",
                        "y = 1, so x = 2",
                    ],
                    "answer": "(2, 1)",
                },
                {
                    "problem": "2(3x − y) = 10 and y = x + 1. Find the pair.",
                    "steps": [
                        "6x − 2(x + 1) = 10",
                        "6x − 2x − 2 = 10 → 4x = 12 → x = 3",
                        "y = 4",
                    ],
                    "answer": "(3, 4)",
                },
                {
                    "problem": "3(y − 2) = x and x + y = 8. Find y.",
                    "steps": [
                        "x = 3y − 6",
                        "3y − 6 + y = 8 → 4y = 14",
                        "y = 3.5, x = 4.5",
                    ],
                    "answer": "(4.5, 3.5)",
                },
            ],
        },
        {
            "title": "Fractions inside a system",
            "visual": "system",
            "beats": [
                "Clear small denominators before or after substituting.",
                "y = 5 − x/2 into x − 4y = −2 → x − 20 + 2x = −2 → (6, 2).",
                "Then x − 4(5 − x/2) = −2 → x − 20 + 2x = −2 → 3x = 18 → (6, 2).",
                "(x + y)/2 = 4 and y = x → x = 4, y = 4.",
                "A fractional pair is fine if both originals check.",
            ],
            "examples": [
                {
                    "problem": "x/2 + y = 5 and x − 4y = −2. Find the pair.",
                    "steps": [
                        "y = 5 − x/2",
                        "x − 4(5 − x/2) = −2 → 3x = 18 → x = 6",
                        "y = 5 − 3 = 2",
                    ],
                    "answer": "(6, 2)",
                },
                {
                    "problem": "(x + y)/2 = 4 and y = x. Find x.",
                    "steps": [
                        "(x + x)/2 = 4",
                        "x = 4",
                        "y = 4",
                    ],
                    "answer": "(4, 4)",
                },
                {
                    "problem": "y = x/2 and x + 2y = 12. Find the pair.",
                    "steps": [
                        "x + 2(x/2) = 12",
                        "x + x = 12 → 2x = 12 → x = 6",
                        "y = 3",
                    ],
                    "answer": "(6, 3)",
                },
            ],
        },
        {
            "title": "No solution or infinitely many",
            "visual": "system",
            "beats": [
                "After substituting, 0 = 5 means parallel lines: no solution.",
                "0 = 0 means the same line: infinitely many solutions.",
                "x = 2y + 1 into 3x − 6y = 8 → 6 = 8, none.",
                "The same x into 3x − 6y = 3 → 3 = 3, infinitely many.",
                "Do not list one sample point as 'the' answer when there are infinitely many.",
            ],
            "examples": [
                {
                    "problem": "x = 2y + 1 and 3x − 6y = 8. How many solutions?",
                    "steps": [
                        "3(2y + 1) − 6y = 8",
                        "6y + 3 − 6y = 8 → 3 = 8",
                        "Contradiction: no solution",
                    ],
                    "answer": "no solution",
                },
                {
                    "problem": "x = 2y + 1 and 3x − 6y = 3. How many solutions?",
                    "steps": [
                        "3(2y + 1) − 6y = 3",
                        "6y + 3 − 6y = 3 → 3 = 3",
                        "Identity: infinitely many",
                    ],
                    "answer": "infinitely many",
                },
                {
                    "problem": "If substitution yields 0 = 0, what should you write?",
                    "steps": [
                        "The two equations are the same line",
                        "Every point on that line works",
                        "Say infinitely many solutions",
                    ],
                    "answer": "infinitely many solutions",
                },
            ],
        },
        {
            "title": "Two-unknown stories",
            "visual": "system",
            "beats": [
                "Two unknowns need two independent facts.",
                "Adults a dollars 8, children c dollars 5, with two purchase totals, is a system.",
                "If a story gives y = 2x + 1 and y = −x + 7, set the y's equal: (2, 5).",
                "Let the letters be counts or prices, but stay consistent.",
                "Finish with a sentence: 7 adults at 8 dollars and 3 children at 5 dollars.",
            ],
            "examples": [
                {
                    "problem": "y = 2x + 1 and y = −x + 7. Find the meeting point.",
                    "steps": [
                        "Set 2x + 1 = −x + 7",
                        "3x = 6 → x = 2",
                        "y = 5",
                    ],
                    "answer": "(2, 5)",
                },
                {
                    "problem": "Tickets: a + c = 10 and 8a + 5c = 71. Find a.",
                    "steps": [
                        "c = 10 − a",
                        "8a + 5(10 − a) = 71 → 3a = 21 → a = 7",
                        "c = 3",
                    ],
                    "answer": "7 adult, 3 child",
                },
                {
                    "problem": "Two numbers sum to 14 and the larger is 2 more than the smaller.",
                    "steps": [
                        "x + y = 14 and x = y + 2",
                        "(y + 2) + y = 14 → y = 6",
                        "x = 8",
                    ],
                    "answer": "8 and 6",
                },
            ],
        },
    ],
}

U6 = {
    "num": 6,
    "title": "Systems by Elimination",
    "subtitle": "Scale, add, and cancel a variable",
    "file": "unit-6-elimination",
    "parts": [
        {
            "title": "Add to cancel a variable",
            "visual": "system",
            "beats": [
                "Line the equations up. Add or subtract so one variable disappears.",
                "x + y = 10 and x − y = 2. Add: 2x = 12, x = 6, y = 4.",
                "5x − 2y = 4 and 3x + 2y = 12. Add: 8x = 16, x = 2, y = 3.",
                "Opposites (2y and −2y) cancel when you add.",
                "Write the ordered pair and check both originals.",
            ],
            "examples": [
                {
                    "problem": "Solve x + y = 10 and x − y = 2.",
                    "steps": [
                        "Add: 2x = 12, so x = 6",
                        "10 − 6 = 4, so y = 4",
                        "Check: 6+4=10 and 6−4=2",
                    ],
                    "answer": "(6, 4)",
                },
                {
                    "problem": "Solve 5x − 2y = 4 and 3x + 2y = 12.",
                    "steps": [
                        "Add: 8x = 16, x = 2",
                        "3(2) + 2y = 12 → y = 3",
                        "Pair (2, 3)",
                    ],
                    "answer": "(2, 3)",
                },
                {
                    "problem": "Solve 3x + 2y = 16 and x − 2y = 0.",
                    "steps": [
                        "Add: 4x = 16, x = 4",
                        "4 − 2y = 0 → y = 2",
                        "Pair (4, 2)",
                    ],
                    "answer": "(4, 2)",
                },
            ],
        },
        {
            "title": "Multiply first so coefficients match",
            "visual": "system",
            "beats": [
                "If nothing cancels yet, multiply one or both equations.",
                "3x + 2y = 12 and 2x + 5y = 19. ×5 and ×2 so both have 10y, then subtract.",
                "x = 2, y = 3. That pair is heavier arithmetic, same two letters.",
                "Multiply every term, including the constant.",
                "Pick the variable whose coefficients have a small common multiple.",
            ],
            "examples": [
                {
                    "problem": "Solve 3x + 2y = 12 and 2x + 5y = 19.",
                    "steps": [
                        "×5 and ×2: 15x+10y=60 and 4x+10y=38",
                        "Subtract: 11x = 22, x = 2",
                        "3(2)+2y=12, y=3",
                    ],
                    "answer": "(2, 3)",
                },
                {
                    "problem": "Multiply x + 3y = 7 by 2.",
                    "steps": [
                        "Every term ×2",
                        "2x + 6y = 14",
                        "Same line, just scaled",
                    ],
                    "answer": "2x + 6y = 14",
                },
                {
                    "problem": "Solve 2x + 3y = −1 and 4x − y = 5.",
                    "steps": [
                        "×3 on the second: 12x − 3y = 15",
                        "Add to 2x+3y=−1: 14x=14, x=1",
                        "4(1)−y=5, y=−1",
                    ],
                    "answer": "(1, −1)",
                },
            ],
        },
        {
            "title": "Negatives and mixed signs",
            "visual": "system",
            "beats": [
                "Keep the minus attached to its term when you add.",
                "4x − 3y = 11 and 2x + 3y = 7. Add: 6x = 18, x = 3.",
                "Then 2(3)+3y=7, y = 1/3. A fraction pair is legal.",
                "If you need −3y and already have +3y, add.",
                "A sign error here is the usual way to lose the solution.",
            ],
            "examples": [
                {
                    "problem": "Solve 2x + 3y = −1 and 4x − y = 5.",
                    "steps": [
                        "×3 on the second: 12x − 3y = 15",
                        "Add: 14x = 14, x = 1",
                        "y = −1",
                    ],
                    "answer": "(1, −1)",
                },
                {
                    "problem": "Solve 4x − 3y = 11 and 2x + 3y = 7. Find x.",
                    "steps": [
                        "Add: 6x = 18",
                        "x = 3",
                        "Then 6 + 3y = 7, y = 1/3",
                    ],
                    "answer": "(3, 1/3)",
                },
                {
                    "problem": "Solve x + y = 14 and 2x + 3y = 31. Find y.",
                    "steps": [
                        "From the first, x = 14 − y",
                        "2(14 − y) + 3y = 31 → y = 3",
                        "x = 11",
                    ],
                    "answer": "(11, 3)",
                },
            ],
        },
        {
            "title": "Same line or parallel",
            "visual": "system",
            "beats": [
                "2x + 4y = 10 and x + 2y = 5: first is 2× the second. Infinitely many.",
                "2x + 4y = 10 and x + 2y = 6: same slopes, different constants. No solution.",
                "After adding, 0 = 0 means infinitely many. 0 = 4 means none.",
                "Graph: stacked lines vs two rails that never meet.",
                "Do not list one sample point when there are infinitely many.",
            ],
            "examples": [
                {
                    "problem": "2x + 4y = 10 and x + 2y = 6. How many solutions?",
                    "steps": [
                        "×2 on the second: 2x + 4y = 12",
                        "That cannot equal 2x + 4y = 10",
                        "Parallel: no solution",
                    ],
                    "answer": "no solution",
                },
                {
                    "problem": "2x + 4y = 10 and x + 2y = 5. How many solutions?",
                    "steps": [
                        "×2 on the second gives the first equation",
                        "Same line",
                        "Infinitely many solutions",
                    ],
                    "answer": "infinitely many",
                },
                {
                    "problem": "x − 2y = 3 and 3x − 6y = 10. How many solutions?",
                    "steps": [
                        "3× the first would be 3x − 6y = 9",
                        "The second says = 10, not 9",
                        "Parallel: none",
                    ],
                    "answer": "no solution",
                },
            ],
        },
        {
            "title": "Two-unknown mix stories",
            "visual": "system",
            "beats": [
                "Two equations: 3a + 2c = 34 and a + 4c = 28.",
                "×3 the second, subtract: 3a + 2c = 34 and 3a + 12c = 84 give 10c = 50, c = 5, a = 8.",
                "Read the pair in words: a = 8, c = 5.",
                "Two ticket types, two snack mixes, two phone plans: same pattern.",
                "The graph of 3a + 2c = 34 and a + 4c = 28 meets at (8, 5).",
            ],
            "examples": [
                {
                    "problem": "3a + 2c = 34 and a + 4c = 28. Find a and c.",
                    "steps": [
                        "×3: 3a + 12c = 84",
                        "Subtract 3a + 2c = 34: 10c = 50, c = 5",
                        "a + 20 = 28, a = 8",
                    ],
                    "answer": "a = 8, c = 5",
                },
                {
                    "problem": "x + y = 14 and 2x + 3y = 31. Find the pair.",
                    "steps": [
                        "x = 14 − y",
                        "2(14 − y) + 3y = 31 → y = 3",
                        "x = 11",
                    ],
                    "answer": "(11, 3)",
                },
                {
                    "problem": "3 bags and 2 boxes cost 26 dollars; 1 bag and 4 boxes cost 22. Find bag price.",
                    "steps": [
                        "3b + 2x = 26, b + 4x = 22",
                        "×3: 3b + 12x = 66, subtract: 10x = 40, x = 4",
                        "b + 16 = 22, b = 6",
                    ],
                    "answer": "bag 6 dollars, box 4 dollars",
                },
            ],
        },
        {
            "title": "Choose substitution or elimination",
            "visual": "system",
            "beats": [
                "If y is already isolated, substitute. If coefficients match easily, eliminate.",
                "The pair should come out the same either way. That is your check.",
                "A graph is a third check: the meeting point should be that pair.",
                "When a story gives two y = mx + b plans, set the y's equal.",
                "High school will add more variables. The two-variable engine stays the same.",
            ],
            "examples": [
                {
                    "problem": "y = x − 1 and 3x − y = 7. Find the pair.",
                    "steps": [
                        "y is already isolated → substitute",
                        "3x − (x − 1) = 7 → 2x = 6 → x = 3",
                        "y = 2",
                    ],
                    "answer": "(3, 2) by substitution",
                },
                {
                    "problem": "3x + 2y = 16 and x − 2y = 0. Which method, and the pair?",
                    "steps": [
                        "The 2y and −2y already oppose → eliminate",
                        "Add: 4x = 16, x = 4",
                        "y = 2",
                    ],
                    "answer": "(4, 2) by elimination",
                },
                {
                    "problem": "y = 2x + 1 and y = −x + 7. Solve.",
                    "steps": [
                        "Set the two expressions for y equal",
                        "2x + 1 = −x + 7 → x = 2",
                        "y = 5",
                    ],
                    "answer": "(2, 5)",
                },
            ],
        },
    ],
}
