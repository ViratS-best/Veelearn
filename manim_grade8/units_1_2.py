"""Curriculum beats and worked examples for all eight Grade 8 units."""

U1 = {
    "num": 1,
    "title": "Exponents and Scientific Notation",
    "subtitle": "Powers, roots, and numbers written with 10",
    "file": "unit-1-exponents",
    "parts": [
        {
            "title": "What an exponent does",
            "visual": "exponent",
            "beats": [
                "aⁿ means n factors of a.  5³ = 5 × 5 × 5 = 125.",
                "(-4)² = 16 because the minus is inside the power.",
                "-4² = -16 because you square 4 first, then apply the minus.",
                "A square root undoes a square: √64 = 8 because 8² = 64.",
                "√7 is irrational. √49 = 7 is rational.",
            ],
            "examples": [
                {
                    "problem": "Compare (-4)² and -4².",
                    "steps": [
                        "(-4)² = (-4) × (-4) = 16",
                        "-4² = -(4 × 4) = -16",
                        "Parentheses decide whether the minus is powered.",
                    ],
                    "answer": "16 versus -16",
                },
                {
                    "problem": "Evaluate 2⁴ and 5³.",
                    "steps": [
                        "2⁴ = 2 × 2 × 2 × 2 = 16",
                        "5³ = 5 × 5 × 5 = 125",
                        "The exponent counts factors, not 'times 4' or 'times 3'.",
                    ],
                    "answer": "16 and 125",
                },
                {
                    "problem": "A cube has volume 27. What is the edge length?",
                    "steps": [
                        "Volume of a cube is (edge)³",
                        "3³ = 27",
                        "The edge is 3.",
                    ],
                    "answer": "3",
                },
            ],
        },
        {
            "title": "Product, quotient, and power rules",
            "visual": "exponent",
            "beats": [
                "Same base, multiply: add exponents.  4² × 4³ = 4⁵.",
                "Same base, divide: subtract exponents.  6⁸ ÷ 6⁵ = 6³.",
                "Power of a power: multiply exponents.  (3²)⁵ = 3¹⁰.",
                "A bare x is x¹, so x⁴ · x = x⁵.",
                "Coefficients multiply separately: (3x²)(4x⁵) = 12x⁷.",
            ],
            "examples": [
                {
                    "problem": "Simplify 4² × 4³.",
                    "steps": [
                        "Same base, multiplying: add the exponents",
                        "2 + 3 = 5",
                        "Keep the base 4. Not 4^6.",
                    ],
                    "answer": "4⁵",
                },
                {
                    "problem": "Simplify 6⁸ ÷ 6⁵.",
                    "steps": [
                        "Same base, dividing: subtract exponents",
                        "8 - 5 = 3",
                        "6³, not 6¹³.",
                    ],
                    "answer": "6³",
                },
                {
                    "problem": "Simplify (3x²)(4x⁵).",
                    "steps": [
                        "Numbers: 3 × 4 = 12",
                        "Variables: x² · x⁵ = x⁷",
                        "Write them together.",
                    ],
                    "answer": "12x⁷",
                },
            ],
        },
        {
            "title": "Zero and negative exponents",
            "visual": "sci",
            "beats": [
                "Any nonzero number to the 0 power is 1.  9⁰ = 1.",
                "A negative exponent is a reciprocal: 3⁻² = 1 / 3² = 1/9.",
                "Do not read 3⁻² as -9. The minus lives in the exponent.",
                "(2/5)⁻¹ = 5/2. You flip the fraction.",
                "10⁻³ = 0.001, which is 1 × 10⁻³. Negative powers of 10 slide left.",
            ],
            "examples": [
                {
                    "problem": "Write 3⁻² as a fraction.",
                    "steps": [
                        "Negative exponent means reciprocal",
                        "3² = 9",
                        "So 3⁻² = 1/9",
                    ],
                    "answer": "1/9",
                },
                {
                    "problem": "Evaluate 5⁻² and 8⁰.",
                    "steps": [
                        "5⁻² = 1 / 5² = 1/25",
                        "8⁰ = 1",
                        "Zero power is 1; negative power is a fraction.",
                    ],
                    "answer": "1/25 and 1",
                },
                {
                    "problem": "Simplify (2/5)⁻¹.",
                    "steps": [
                        "A -1 exponent flips the fraction",
                        "2/5 flipped is 5/2",
                        "Leave it as 5/2",
                    ],
                    "answer": "5/2",
                },
            ],
        },
        {
            "title": "Scientific notation",
            "visual": "sci",
            "beats": [
                "Scientific notation is a × 10ⁿ with 1 ≤ |a| < 10.  8.4 × 10⁶ is in that form.",
                "2.7 × 10⁵ = 270000. A positive exponent makes a large number.",
                "6.1 × 10⁻³ = 0.0061. A negative exponent makes a small number.",
                "0.00045 = 4.5 × 10⁻⁴. Count hops of the decimal point.",
                "Compare exponents first: 2.8 × 10⁶ beats 9.9 × 10⁵.",
            ],
            "examples": [
                {
                    "problem": "Write 2.7 × 10⁵ in standard form.",
                    "steps": [
                        "The exponent 5 means five hops right",
                        "2.7 → 27 → 270 → 2700 → 27000 → 270000",
                        "Fill extra places with zeros.",
                    ],
                    "answer": "270000",
                },
                {
                    "problem": "Write 0.00045 in scientific notation.",
                    "steps": [
                        "Move the point to sit after 4: 4.5",
                        "You hopped 4 places left, so the exponent is -4",
                        "Check: 4.5 × 10⁻⁴ = 0.00045",
                    ],
                    "answer": "4.5 × 10⁻⁴",
                },
                {
                    "problem": "Which is larger: 9.9 × 10⁵ or 2.8 × 10⁶?",
                    "steps": [
                        "Compare the powers of 10 first",
                        "10⁶ is ten times 10⁵",
                        "So 2.8 × 10⁶ is larger, even though 2.8 < 9.9",
                    ],
                    "answer": "2.8 × 10⁶",
                },
            ],
        },
        {
            "title": "Compute in scientific notation",
            "visual": "sci",
            "beats": [
                "Multiply: (4 × 10³)(2 × 10⁴) = 8 × 10⁷.",
                "Divide: (9 × 10⁶) / (3 × 10²) = 3 × 10⁴.",
                "When you multiply, add the exponents. When you divide, subtract them.",
                "If the leading part leaves 1-to-10, adjust: 30 × 10⁴ = 3 × 10⁵.",
                "(6 × 10⁻⁴)(5 × 10⁷) = 30 × 10³.",
            ],
            "examples": [
                {
                    "problem": "Compute (4 × 10³)(2 × 10⁴).",
                    "steps": [
                        "Coefficients: 4 × 2 = 8",
                        "Exponents: 3 + 4 = 7",
                        "Write 8 × 10⁷",
                    ],
                    "answer": "8 × 10⁷",
                },
                {
                    "problem": "Compute (9 × 10⁶) ÷ (3 × 10²).",
                    "steps": [
                        "Coefficients: 9 ÷ 3 = 3",
                        "Exponents: 6 - 2 = 4",
                        "Write 3 × 10⁴",
                    ],
                    "answer": "3 × 10⁴",
                },
                {
                    "problem": "Rewrite 30 × 10⁴ in proper scientific notation.",
                    "steps": [
                        "30 is not between 1 and 10",
                        "30 = 3 × 10¹",
                        "3 × 10¹ × 10⁴ = 3 × 10⁵",
                    ],
                    "answer": "3 × 10⁵",
                },
            ],
        },
        {
            "title": "Roots on the number line",
            "visual": "roots",
            "beats": [
                "Perfect squares: 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121.",
                "√25 is not √9 + √16. Adding the roots: 3 + 4 = 7.",
                "√40 sits just past 6 because 6² = 36 and 7² = 49.",
                "Leave √11 as √11 when the problem wants an exact length.",
                "A hypotenuse can stay √89 if 89 is not a perfect square.",
            ],
            "examples": [
                {
                    "problem": "Between which two whole numbers is √40?",
                    "steps": [
                        "6² = 36 and 7² = 49",
                        "40 is just after 36",
                        "So √40 is between 6 and 7",
                    ],
                    "answer": "6 and 7",
                },
                {
                    "problem": "Evaluate √9 + √16.",
                    "steps": [
                        "√9 = 3 and √16 = 4",
                        "Add 3 + 4",
                        "Do not add under one root: that would be √25 = 5, which is different",
                    ],
                    "answer": "7",
                },
                {
                    "problem": "Is √144 rational?",
                    "steps": [
                        "12 × 12 = 144",
                        "√144 = 12, a whole number",
                        "Whole numbers are rational",
                    ],
                    "answer": "yes, 12",
                },
            ],
        },
    ],
}

U2 = {
    "num": 2,
    "title": "Linear Equations in One Variable",
    "subtitle": "Distribute, both sides, identities, and stories",
    "file": "unit-2-equations",
    "parts": [
        {
            "title": "Multi-step with distribute",
            "visual": "balance",
            "beats": [
                "Clear parentheses first. Both sides of an equation stay equal.",
                "3(2x − 1) − 4 = 5x + 7 becomes 6x − 3 − 4 = 5x + 7.",
                "A minus in front of a group hits every term: −(x − 4) = −x + 4.",
                "Combine like terms, then move pieces across the equals sign.",
                "Always check in the original equation.",
            ],
            "examples": [
                {
                    "problem": "Solve 3(2x − 1) − 4 = 5x + 7.",
                    "steps": [
                        "Distribute: 6x − 3 − 4 = 5x + 7",
                        "6x − 7 = 5x + 7, so x − 7 = 7",
                        "x = 14. Check: both sides equal 77",
                    ],
                    "answer": "x = 14",
                },
                {
                    "problem": "Solve 2(x − 3) = x + 5.",
                    "steps": [
                        "2x − 6 = x + 5",
                        "Subtract x: x − 6 = 5",
                        "x = 11",
                    ],
                    "answer": "x = 11",
                },
                {
                    "problem": "Solve −(x − 4) = 10.",
                    "steps": [
                        "−x + 4 = 10",
                        "−x = 6",
                        "x = −6",
                    ],
                    "answer": "x = −6",
                },
            ],
        },
        {
            "title": "Variables on both sides",
            "visual": "balance",
            "beats": [
                "Collect the x terms on one side and the numbers on the other.",
                "4(x + 1) = 2(x + 7) → 4x + 4 = 2x + 14 → 2x = 10 → x = 5.",
                "−3x + 8 = 2x − 7 → 8 + 7 = 5x → x = 3.",
                "If the x terms cancel and numbers match, every x works.",
                "If they cancel and numbers disagree, nothing works.",
            ],
            "examples": [
                {
                    "problem": "Solve 4(x + 1) = 2(x + 7).",
                    "steps": [
                        "4x + 4 = 2x + 14",
                        "2x = 10",
                        "x = 5",
                    ],
                    "answer": "x = 5",
                },
                {
                    "problem": "Solve −3x + 8 = 2x − 7.",
                    "steps": [
                        "Add 3x to both sides: 8 = 5x − 7",
                        "Add 7: 15 = 5x",
                        "x = 3",
                    ],
                    "answer": "x = 3",
                },
                {
                    "problem": "Solve 2(3x + 1) = 4x + 10.",
                    "steps": [
                        "6x + 2 = 4x + 10",
                        "2x = 8",
                        "x = 4",
                    ],
                    "answer": "x = 4",
                },
            ],
        },
        {
            "title": "Fractions and decimals",
            "visual": "balance",
            "beats": [
                "Clear a denominator by multiplying both sides.",
                "(x + 2)/3 = 4 → x + 2 = 12 → x = 10.",
                "x/4 + 3 = 7 → x/4 = 4 → x = 16.",
                "0.5x = 9 → x = 18. Multiplying by 2 clears the decimal.",
                "Whatever you do to one side, do to the other.",
            ],
            "examples": [
                {
                    "problem": "Solve (x + 2)/3 = 4.",
                    "steps": [
                        "Multiply both sides by 3",
                        "x + 2 = 12",
                        "x = 10",
                    ],
                    "answer": "x = 10",
                },
                {
                    "problem": "Solve x/2 − 3 = 1.",
                    "steps": [
                        "Add 3: x/2 = 4",
                        "Multiply by 2",
                        "x = 8",
                    ],
                    "answer": "x = 8",
                },
                {
                    "problem": "Solve 0.5x = 9.",
                    "steps": [
                        "0.5 is one half",
                        "Multiply both sides by 2",
                        "x = 18",
                    ],
                    "answer": "x = 18",
                },
            ],
        },
        {
            "title": "Identities and contradictions",
            "visual": "balance",
            "beats": [
                "An identity is true for every x. After simplifying you get 4 = 4.",
                "A contradiction is never true. You get 4 = 9 or −2 = −3.",
                "(2x − 4)/2 = x − 3 simplifies to x − 2 = x − 3, so −2 = −3. None.",
                "3x + 2 = 3x − 5 becomes 2 = −5. No solution.",
                "If a check fails for one number, that value is not a solution. An identity is true for every x.",
            ],
            "examples": [
                {
                    "problem": "How many solutions: (2x − 4)/2 = x − 3?",
                    "steps": [
                        "Left side: x − 2",
                        "x − 2 = x − 3 becomes −2 = −3",
                        "That is never true",
                    ],
                    "answer": "no solution",
                },
                {
                    "problem": "How many solutions: 3x + 2 = 3x − 5?",
                    "steps": [
                        "Subtract 3x: 2 = −5",
                        "A false number sentence",
                        "No value of x can fix it",
                    ],
                    "answer": "no solution",
                },
                {
                    "problem": "How many solutions: 2(x + 3) = 2x + 6?",
                    "steps": [
                        "2x + 6 = 2x + 6",
                        "0 = 0, always true",
                        "Every real number works",
                    ],
                    "answer": "infinitely many",
                },
            ],
        },
        {
            "title": "Hidden grouping",
            "visual": "balance",
            "beats": [
                "Minus a group: 2x − (x − 5) = 2x − x + 5.",
                "5 − 2(x + 1) = 5 − 2x − 2 = 3 − 2x.",
                "Distribute before you move terms.",
                "Hidden grouping is the usual source of a sign error.",
                "Rewrite the line with every sign attached to its term.",
            ],
            "examples": [
                {
                    "problem": "Solve 2x − (x − 5) = 9.",
                    "steps": [
                        "2x − x + 5 = 9",
                        "x + 5 = 9",
                        "x = 4",
                    ],
                    "answer": "x = 4",
                },
                {
                    "problem": "Solve 5 − 2(x + 1) = 9.",
                    "steps": [
                        "5 − 2x − 2 = 9",
                        "3 − 2x = 9, so −2x = 6",
                        "x = −3",
                    ],
                    "answer": "x = −3",
                },
                {
                    "problem": "Solve 2(x + 4) − x = 9.",
                    "steps": [
                        "2x + 8 − x = 9",
                        "x + 8 = 9",
                        "x = 1",
                    ],
                    "answer": "x = 1",
                },
            ],
        },
        {
            "title": "Linear-equation stories",
            "visual": "balance",
            "beats": [
                "Let x be the unknown. Write one equation from the sentences.",
                "Half of a number minus 4 is 6, so x/2 - 4 = 6, so x = 20.",
                "A number plus twice itself is 24 → x + 2x = 24 → x = 8.",
                "Check the story, not just the algebra: does 20 make sense?",
                "Units stay outside the algebra until the last sentence.",
            ],
            "examples": [
                {
                    "problem": "Half of a number minus 4 is 6. Find the number.",
                    "steps": [
                        "x/2 - 4 = 6",
                        "x/2 = 10",
                        "x = 20",
                    ],
                    "answer": "20",
                },
                {
                    "problem": "Three copies of a number add to 24. Find it.",
                    "steps": [
                        "x + x + x = 24",
                        "3x = 24",
                        "x = 8",
                    ],
                    "answer": "8",
                },
                {
                    "problem": "5 more than twice a number is 17. Find the number.",
                    "steps": [
                        "2x + 5 = 17",
                        "2x = 12",
                        "x = 6",
                    ],
                    "answer": "6",
                },
            ],
        },
    ],
}
