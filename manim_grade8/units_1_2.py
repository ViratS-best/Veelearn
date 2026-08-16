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
                "aⁿ means n factors of a.  4³ = 4 × 4 × 4 = 64.",
                "(−3)² = 9 because the minus is inside the power.",
                "−3² = −9 because you square 3 first, then apply the minus.",
                "A square root undoes a square: √81 = 9 because 9² = 81.",
                "√2 is irrational. √16 = 4 is rational.",
            ],
            "examples": [
                {
                    "problem": "Compare (−3)² and −3².",
                    "steps": [
                        "(−3)² = (−3) × (−3) = 9",
                        "−3² = −(3 × 3) = −9",
                        "Parentheses decide whether the minus is powered.",
                    ],
                    "answer": "9 versus −9",
                },
                {
                    "problem": "Evaluate 2⁴ and 4³.",
                    "steps": [
                        "2⁴ = 2 × 2 × 2 × 2 = 16",
                        "4³ = 4 × 4 × 4 = 64",
                        "The exponent counts factors, not 'times 4' or 'times 3'.",
                    ],
                    "answer": "16 and 64",
                },
                {
                    "problem": "A cube has volume 8. What is the edge length?",
                    "steps": [
                        "Volume of a cube is (edge)³",
                        "2³ = 8",
                        "The edge is 2.",
                    ],
                    "answer": "2",
                },
            ],
        },
        {
            "title": "Product, quotient, and power rules",
            "visual": "exponent",
            "beats": [
                "Same base, multiply: add exponents.  3² × 3⁴ = 3⁶.",
                "Same base, divide: subtract exponents.  5⁷ ÷ 5³ = 5⁴.",
                "Power of a power: multiply exponents.  (2³)⁴ = 2¹².",
                "A bare x is x¹, so x⁵ · x = x⁶.",
                "Coefficients multiply separately: (2x³)(5x²) = 10x⁵.",
            ],
            "examples": [
                {
                    "problem": "Simplify (2³)⁴.",
                    "steps": [
                        "Power of a power: multiply 3 × 4",
                        "That product is 12",
                        "Keep the base 2.",
                    ],
                    "answer": "2¹²",
                },
                {
                    "problem": "Simplify 5⁷ ÷ 5³.",
                    "steps": [
                        "Same base, dividing: subtract exponents",
                        "7 − 3 = 4",
                        "5⁴, not 5¹⁰.",
                    ],
                    "answer": "5⁴",
                },
                {
                    "problem": "Simplify (2x³)(5x²).",
                    "steps": [
                        "Numbers: 2 × 5 = 10",
                        "Variables: x³ · x² = x⁵",
                        "Write them together.",
                    ],
                    "answer": "10x⁵",
                },
            ],
        },
        {
            "title": "Zero and negative exponents",
            "visual": "sci",
            "beats": [
                "Any nonzero number to the 0 power is 1.  7⁰ = 1.",
                "A negative exponent is a reciprocal: 2⁻³ = 1 / 2³ = 1/8.",
                "Do not read 2⁻³ as −8. The minus lives in the exponent.",
                "(1/2)⁻¹ = 2. You flip the fraction.",
                "These rules are how scientific notation slides left and right.",
            ],
            "examples": [
                {
                    "problem": "Write 2⁻³ as a fraction.",
                    "steps": [
                        "Negative exponent means reciprocal",
                        "2³ = 8",
                        "So 2⁻³ = 1/8",
                    ],
                    "answer": "1/8",
                },
                {
                    "problem": "Evaluate 5⁻² and 10⁰.",
                    "steps": [
                        "5⁻² = 1 / 5² = 1/25",
                        "10⁰ = 1",
                        "Zero power is 1; negative power is a fraction.",
                    ],
                    "answer": "1/25 and 1",
                },
                {
                    "problem": "Simplify (1/2)⁻¹.",
                    "steps": [
                        "A −1 exponent flips the fraction",
                        "1/2 flipped is 2/1",
                        "That is 2",
                    ],
                    "answer": "2",
                },
            ],
        },
        {
            "title": "Scientific notation",
            "visual": "sci",
            "beats": [
                "Scientific notation is a × 10ⁿ with 1 ≤ |a| < 10.",
                "3.2 × 10⁴ = 32,000. A positive exponent makes a large number.",
                "3.2 × 10⁻² = 0.032. A negative exponent makes a small number.",
                "0.0032 = 3.2 × 10⁻³. Count hops of the decimal point.",
                "Compare exponents first: 3.9 × 10⁴ beats 4.1 × 10³.",
            ],
            "examples": [
                {
                    "problem": "Write 4.5 × 10³ in standard form.",
                    "steps": [
                        "The exponent 3 means three hops right",
                        "4.5 → 45 → 450 → 4500",
                        "Fill extra places with zeros.",
                    ],
                    "answer": "4500",
                },
                {
                    "problem": "Write 0.0032 in scientific notation.",
                    "steps": [
                        "Move the point to sit after 3: 3.2",
                        "You hopped 3 places left, so the exponent is −3",
                        "Check: 3.2 × 10⁻³ = 0.0032",
                    ],
                    "answer": "3.2 × 10⁻³",
                },
                {
                    "problem": "Which is larger: 4.1 × 10³ or 3.9 × 10⁴?",
                    "steps": [
                        "Compare the powers of 10 first",
                        "10⁴ is ten times 10³",
                        "So 3.9 × 10⁴ is larger, even though 3.9 < 4.1",
                    ],
                    "answer": "3.9 × 10⁴",
                },
            ],
        },
        {
            "title": "Compute in scientific notation",
            "visual": "sci",
            "beats": [
                "Multiply: (3 × 10⁴)(2 × 10³) = 6 × 10⁷.",
                "Divide: (4 × 10⁵) ÷ (2 × 10²) = 2 × 10³.",
                "Add the exponents when you multiply. Subtract when you divide.",
                "If the leading part leaves 1-to-10, adjust: 12 × 10³ = 1.2 × 10⁴.",
                "This is how science handles planets, cells, and bits.",
            ],
            "examples": [
                {
                    "problem": "Compute (3 × 10⁴)(2 × 10³).",
                    "steps": [
                        "Leadings: 3 × 2 = 6",
                        "Exponents: 4 + 3 = 7",
                        "Write 6 × 10⁷",
                    ],
                    "answer": "6 × 10⁷",
                },
                {
                    "problem": "Compute (4 × 10⁵) ÷ (2 × 10²).",
                    "steps": [
                        "Leadings: 4 ÷ 2 = 2",
                        "Exponents: 5 − 2 = 3",
                        "Write 2 × 10³",
                    ],
                    "answer": "2 × 10³",
                },
                {
                    "problem": "Rewrite 12 × 10³ in proper scientific notation.",
                    "steps": [
                        "12 is not between 1 and 10",
                        "12 = 1.2 × 10¹",
                        "1.2 × 10¹ × 10³ = 1.2 × 10⁴",
                    ],
                    "answer": "1.2 × 10⁴",
                },
            ],
        },
        {
            "title": "Roots on the number line",
            "visual": "roots",
            "beats": [
                "Perfect squares: 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121.",
                "√9 + √16 = 3 + 4 = 7, not √25.",
                "√50 sits just past 7 because 7² = 49 and 8² = 64.",
                "Leave √2 as √2 when the problem wants an exact length.",
                "Later, a hypotenuse is √(a² + b²). The root must make sense as a length.",
            ],
            "examples": [
                {
                    "problem": "Between which two whole numbers is √50?",
                    "steps": [
                        "7² = 49 and 8² = 64",
                        "50 is just after 49",
                        "So √50 is between 7 and 8",
                    ],
                    "answer": "7 and 8",
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
                    "problem": "Is √121 rational?",
                    "steps": [
                        "11 × 11 = 121",
                        "√121 = 11, a whole number",
                        "Whole numbers are rational",
                    ],
                    "answer": "yes, 11",
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
                "If a check fails for one number, it may still be an identity — simplify fully.",
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
                "Half of (x − 4) is 6 → (x − 4)/2 = 6 → x = 16.",
                "A number plus twice itself is 24 → x + 2x = 24 → x = 8.",
                "Check the story, not just the algebra: does 16 make sense?",
                "Units stay outside the algebra until the last sentence.",
            ],
            "examples": [
                {
                    "problem": "Half of a number minus 4 is 6. Find the number.",
                    "steps": [
                        "(x − 4)/2 = 6",
                        "x − 4 = 12",
                        "x = 16",
                    ],
                    "answer": "16",
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
