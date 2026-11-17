"""Skill tree for Veelearn AI sessions (Phase 1 seed).

Four tracks, 23 skills, with prerequisite chains and a short authored intro per
skill. `build_session_seed.py` turns this into `veelearn-backend/seed/session_seed.json`
which `session-schema.js` loads once, on boot, when the `skills` table is empty.

Rules kept deliberately simple for phase 1:
  - one prerequisite per skill (`prereq`), which is what the focus planner gates on
  - `dot_target` is how many of the four mastery dots a single session tries to fill
  - `grade_band` is the grade a learner is normally in when they meet this skill
"""

TRACKS = [
    {"id": "math.g8", "name": "Grade 8 Math", "order": 1},
    {"id": "algebra1", "name": "Algebra 1", "order": 2},
    {"id": "apcmech", "name": "AP Physics C: Mechanics", "order": 3},
    {"id": "sat.math", "name": "SAT Math", "order": 4},
    # Exam and subject tracks (seed/qbank_exams.py supplies their questions).
    {"id": "stem.sci", "name": "STEM Science", "order": 5},
    {"id": "english", "name": "English", "order": 6},
    {"id": "sat.rw", "name": "SAT Reading & Writing", "order": 7},
    {"id": "act", "name": "ACT", "order": 8},
    {"id": "mathcounts", "name": "MATHCOUNTS", "order": 9},
    {"id": "amc8", "name": "AMC 8", "order": 10},
    {"id": "amc10", "name": "AMC 10", "order": 11},
    {"id": "amc12", "name": "AMC 12", "order": 12},
    # Grades 1-8, high school, AP math, the olympiad ladder, all-grade science,
    # college engineering and coding (seed/qbank_more.py, seed/qbank_more2.py).
    {"id": "math.elem", "name": "Grades 1-8 Math", "order": 13},
    {"id": "math.hs", "name": "High School Math", "order": 14},
    {"id": "apcalc", "name": "AP Calculus AB/BC", "order": 15},
    {"id": "apstats", "name": "AP Statistics", "order": 16},
    {"id": "aime", "name": "AIME", "order": 17},
    {"id": "usamo", "name": "USAMO", "order": 18},
    {"id": "imo", "name": "IMO", "order": 19},
    {"id": "science.all", "name": "Science (all grades)", "order": 20},
    {"id": "college.eng", "name": "College Engineering", "order": 21},
    {"id": "coding", "name": "Coding", "order": 22},
]

SKILLS = [
    # ---------------------------------------------------------------- grade 8
    {
        "code": "g8.exponents",
        "track": "math.g8",
        "name": "Laws of exponents",
        "grade_band": 8,
        "order": 1,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "When you multiply powers with the same base you add the exponents; when you divide them "
            "you subtract; when a power is raised to a power you multiply."
        ),
        "misconceptions": [
            "Multiplying the exponents when multiplying powers",
            "Applying the exponent to the coefficient only"
        ],
    },
    {
        "code": "g8.sci.not",
        "track": "math.g8",
        "name": "Scientific notation",
        "grade_band": 8,
        "order": 2,
        "prereq": "g8.exponents",
        "dot_target": 2,
        "intro": (
            "Scientific notation writes a number as a value between 1 and 10 times a power of ten. "
            "A positive exponent means a big number, a negative exponent means a small one."
        ),
        "misconceptions": [
            "Keeping the decimal in the wrong place (the first factor must be 1 to 10)",
            "Sign error when moving the decimal to the right"
        ],
    },
    {
        "code": "g8.linear.expressions",
        "track": "math.g8",
        "name": "Simplifying linear expressions",
        "grade_band": 8,
        "order": 3,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "Combine like terms by adding their coefficients, and use the distributive property to "
            "remove brackets before combining."
        ),
        "misconceptions": [
            "Distributing to the first term only",
            "Dropping the sign in front of a subtracted bracket"
        ],
    },
    {
        "code": "g8.linear.equations",
        "track": "math.g8",
        "name": "Equations with variables on both sides",
        "grade_band": 8,
        "order": 4,
        "prereq": "g8.linear.expressions",
        "dot_target": 2,
        "intro": (
            "Move every variable term to one side and every constant to the other, then divide by "
            "the coefficient. Whatever you do to one side you must do to the other."
        ),
        "misconceptions": [
            "Moving a term without changing its sign",
            "Dividing only one side by the coefficient"
        ],
    },
    {
        "code": "g8.systems.substitution",
        "track": "math.g8",
        "name": "Solving systems by substitution",
        "grade_band": 8,
        "order": 5,
        "prereq": "g8.linear.equations",
        "dot_target": 2,
        "intro": (
            "When one equation already gives you y (or x) in terms of the other variable, replace "
            "that variable in the second equation. You get one equation with one unknown."
        ),
        "misconceptions": [
            "Substituting into the same equation instead of the other one",
            "Stopping after finding one variable and forgetting the other"
        ],
    },
    {
        "code": "g8.pythagoras",
        "track": "math.g8",
        "name": "The Pythagorean theorem",
        "grade_band": 8,
        "order": 6,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "In a right triangle the two legs satisfy a² + b² = c², where c is always the side "
            "across from the right angle (the longest side)."
        ),
        "misconceptions": [
            "Putting a leg where the hypotenuse belongs",
            "Adding the squares instead of subtracting to find a missing leg"
        ],
    },

    # ---------------------------------------------------------------- algebra 1
    {
        "code": "alg1.linear.one",
        "track": "algebra1",
        "name": "Solving one-variable equations",
        "grade_band": 9,
        "order": 1,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "Undo operations in reverse order: first the addition or subtraction, then the "
            "multiplication or division, working towards x on its own."
        ),
        "misconceptions": [
            "Dividing before undoing the constant",
            "Losing the negative sign when dividing"
        ],
    },
    {
        "code": "alg1.linear.bothsides",
        "track": "algebra1",
        "name": "Linear equations with variables on both sides",
        "grade_band": 9,
        "order": 2,
        "prereq": "alg1.linear.one",
        "dot_target": 2,
        "intro": (
            "Collect the variable terms on one side and the numbers on the other. If brackets are "
            "involved, distribute first."
        ),
        "misconceptions": [
            "Distributing to only one term in the bracket",
            "Sign errors when a bracket is subtracted"
        ],
    },
    {
        "code": "alg1.inequalities",
        "track": "algebra1",
        "name": "Linear inequalities",
        "grade_band": 9,
        "order": 3,
        "prereq": "alg1.linear.bothsides",
        "dot_target": 2,
        "intro": (
            "Solve inequalities like equations, with one exception: multiplying or dividing both "
            "sides by a negative number flips the inequality sign."
        ),
        "misconceptions": [
            "Forgetting to flip the sign when dividing by a negative",
            "Treating 'at most' as a strict inequality"
        ],
    },
    {
        "code": "alg1.slope",
        "track": "algebra1",
        "name": "Slope and intercepts",
        "grade_band": 9,
        "order": 4,
        "prereq": "alg1.linear.bothsides",
        "dot_target": 2,
        "intro": (
            "Slope is rise over run: (y₂ − y₁) / (x₂ − x₁). In y = mx + b, m is the slope and b is "
            "the y-intercept."
        ),
        "misconceptions": [
            "Putting the change in x on top",
            "Reading the intercept as a point instead of the y-value"
        ],
    },
    {
        "code": "alg1.systems.substitution",
        "track": "algebra1",
        "name": "Systems of equations by substitution",
        "grade_band": 9,
        "order": 5,
        "prereq": "alg1.linear.bothsides",
        "dot_target": 2,
        "intro": (
            "Solve one equation for a variable, substitute it into the other, solve, then back-"
            "substitute to find the second variable."
        ),
        "misconceptions": [
            "Substituting back into the rearranged equation",
            "Reporting only one of the two values"
        ],
    },
    {
        "code": "alg1.quadratics.factor",
        "track": "algebra1",
        "name": "Factoring quadratics",
        "grade_band": 9,
        "order": 6,
        "prereq": "alg1.linear.bothsides",
        "dot_target": 2,
        "intro": (
            "For x² + bx + c, find two numbers that multiply to c and add to b. Those become the "
            "two constants in the factored form."
        ),
        "misconceptions": [
            "Choosing numbers that multiply to b instead of c",
            "Losing a sign when c is negative"
        ],
    },

    # ---------------------------------------------------------------- AP Physics C
    {
        "code": "apcmech.kinematics.1d",
        "track": "apcmech",
        "name": "One-dimensional kinematics",
        "grade_band": 12,
        "order": 1,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "The four constant-acceleration equations connect v, v₀, a, t and Δx. Pick the one that "
            "contains what you know and what you need."
        ),
        "misconceptions": [
            "Using a constant-acceleration equation when the acceleration changes",
            "Sign errors from mixing up v and v₀"
        ],
    },
    {
        "code": "apcmech.newton.second",
        "track": "apcmech",
        "name": "Newton's second law",
        "grade_band": 12,
        "order": 2,
        "prereq": "apcmech.kinematics.1d",
        "dot_target": 2,
        "intro": (
            "ΣF = ma uses the net force, not one force. Draw the free-body diagram first, then add "
            "the components along the direction of motion."
        ),
        "misconceptions": [
            "Using the applied force instead of the net force",
            "Forgetting that the normal force is not always mg"
        ],
    },
    {
        "code": "apcmech.work.constant",
        "track": "apcmech",
        "name": "Work done by a constant force",
        "grade_band": 12,
        "order": 3,
        "prereq": "apcmech.newton.second",
        "dot_target": 2,
        "intro": (
            "W = F d cos θ uses the component of the force along the displacement. A force "
            "perpendicular to the motion does no work."
        ),
        "misconceptions": [
            "Ignoring the angle and using F·d",
            "Counting friction as positive work"
        ],
    },
    {
        "code": "apcmech.work.variable",
        "track": "apcmech",
        "name": "Work done by a varying force",
        "grade_band": 12,
        "order": 4,
        "prereq": "apcmech.work.constant",
        "dot_target": 3,
        "intro": (
            "When the force changes, work is the area under the force-versus-position graph, not "
            "force times distance."
        ),
        "misconceptions": [
            "Using the final force for the whole distance",
            "Treating a triangular area as a rectangle"
        ],
    },
    {
        "code": "apcmech.energy.theorem",
        "track": "apcmech",
        "name": "The work-energy theorem",
        "grade_band": 12,
        "order": 5,
        "prereq": "apcmech.work.variable",
        "dot_target": 3,
        "intro": (
            "The net work done on an object equals its change in kinetic energy: W_net = ΔK. "
            "It is often easier than tracking forces through time."
        ),
        "misconceptions": [
            "Using only one force's work for W_net",
            "Forgetting that friction does negative work"
        ],
    },
    {
        "code": "apcmech.momentum.1d",
        "track": "apcmech",
        "name": "Momentum and impulse in one dimension",
        "grade_band": 12,
        "order": 6,
        "prereq": "apcmech.newton.second",
        "dot_target": 2,
        "intro": (
            "p = mv, and impulse J = FΔt equals the change in momentum. In a collision with no "
            "external force, total momentum is conserved."
        ),
        "misconceptions": [
            "Forgetting that momentum is a vector",
            "Using kinetic energy conservation for every collision"
        ],
    },

    # ---------------------------------------------------------------- SAT math
    {
        "code": "sat.math.linear",
        "track": "sat.math",
        "name": "Linear equations and systems",
        "grade_band": 11,
        "order": 1,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "SAT linear questions reward translating words into equations and solving systems "
            "efficiently rather than elegantly."
        ),
        "misconceptions": [
            "Solving for x when the question asks for an expression",
            "One solution when the system has two unknowns"
        ],
    },
    {
        "code": "sat.math.percent",
        "track": "sat.math",
        "name": "Percent change and percent of",
        "grade_band": 11,
        "order": 2,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "Percent change is (new − old) / old × 100. A percent decrease multiplies by "
            "(1 − rate); a percent increase multiplies by (1 + rate)."
        ),
        "misconceptions": [
            "Dividing by the new value instead of the original",
            "Adding successive percentages instead of multiplying the factors"
        ],
    },
    {
        "code": "sat.math.ratios",
        "track": "sat.math",
        "name": "Ratios, rates and proportions",
        "grade_band": 11,
        "order": 3,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "Set up a proportion with matching units, then cross-multiply. For part-to-whole ratios, "
            "the total is the sum of the parts."
        ),
        "misconceptions": [
            "Mixing units in the two sides of a proportion",
            "Treating a part-to-part ratio as part-to-whole"
        ],
    },
    {
        "code": "sat.math.geometry.area",
        "track": "sat.math",
        "name": "Area and perimeter",
        "grade_band": 11,
        "order": 4,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "Know the rectangle, triangle and circle formulas cold, and split composite shapes into "
            "pieces you can measure."
        ),
        "misconceptions": [
            "Using the diameter instead of the radius",
            "Forgetting to halve for a triangle's area"
        ],
    },
    {
        "code": "sat.math.functions",
        "track": "sat.math",
        "name": "Function notation and composition",
        "grade_band": 11,
        "order": 5,
        "prereq": "sat.math.linear",
        "dot_target": 2,
        "intro": (
            "f(3) means substitute 3 for x. f(g(2)) means evaluate g(2) first, then put that result "
            "into f."
        ),
        "misconceptions": [
            "Multiplying f by the input instead of substituting",
            "Evaluating the outer function first in a composition"
        ],
    },

    # ------------------------------------------------------------- STEM science
    {
        "code": "sci.bio.cell",
        "track": "stem.sci",
        "name": "Cell structure and function",
        "grade_band": 9,
        "order": 1,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "Each organelle does one job well: mitochondria make ATP, the rough ER builds proteins "
            "for export, and the cell wall lets a plant cell take on water without bursting."
        ),
        "misconceptions": [
            "Treating the ribosome as the cell's energy source",
            "Forgetting that a plant cell has both a membrane and a wall"
        ],
    },
    {
        "code": "sci.chem.moles",
        "track": "stem.sci",
        "name": "Bonding and the mole",
        "grade_band": 10,
        "order": 2,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "Moles are just a count: moles = mass ÷ molar mass, and one mole always holds "
            "6.0 × 10²³ particles. Ionic bonds transfer electrons; covalent bonds share them."
        ),
        "misconceptions": [
            "Multiplying mass by molar mass instead of dividing",
            "Confusing the number of molecules with the number of atoms"
        ],
    },

    {
        "code": "sci.elem.concepts",
        "track": "stem.sci",
        "name": "Everyday science concepts",
        "grade_band": 7,
        "order": 3,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "Everyday science asks you to reason from what you already know: what things are made of, "
            "which changes create a new substance, and how the world behaves."
        ),
        "misconceptions": [
            "Calling a mixture a chemical change",
            "Judging hardness from how an object looks instead of from a scratch test"
        ],
    },

    # ------------------------------------------------------------------ English
    {
        "code": "eng.grammar.boundaries",
        "track": "english",
        "name": "Commas and sentence boundaries",
        "grade_band": 9,
        "order": 1,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "Two complete sentences cannot be joined by a comma alone. Use a semicolon, a period, "
            "or a comma plus a coordinating conjunction — and use a semicolon, never a comma, "
            "before a conjunctive adverb like 'however'."
        ),
        "misconceptions": [
            "Joining two complete sentences with only a comma",
            "Putting a semicolon before a coordinating conjunction"
        ],
    },
    {
        "code": "eng.read.inference",
        "track": "english",
        "name": "Inference in a short passage",
        "grade_band": 9,
        "order": 2,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "An inference is the smallest conclusion the details support. Name the detail that "
            "changed, then ask what that change would cause."
        ),
        "misconceptions": [
            "Choosing a statement the passage never implies",
            "Confusing what happened with why it happened"
        ],
    },

    # ------------------------------------------------------ SAT Reading & Writing
    {
        "code": "sat.rw.words",
        "track": "sat.rw",
        "name": "Words in context",
        "grade_band": 11,
        "order": 1,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "Cover the blank and predict your own word from the sentence's logic, especially "
            "contrast words like 'although' and 'rather than'. Then pick the choice closest to it."
        ),
        "misconceptions": [
            "Picking a word that sounds impressive but ignores the contrast",
            "Using a familiar meaning that does not fit this sentence"
        ],
    },
    {
        "code": "sat.rw.boundaries",
        "track": "sat.rw",
        "name": "Sentence boundaries on the SAT",
        "grade_band": 11,
        "order": 2,
        "prereq": "sat.rw.words",
        "dot_target": 2,
        "intro": (
            "Most boundary questions come down to one test: could each side of the punctuation stand "
            "alone as a sentence? If both can, you need a semicolon or a period."
        ),
        "misconceptions": [
            "Choosing a colon after a fragment",
            "Splitting a subject from its verb with a semicolon"
        ],
    },

    # ---------------------------------------------------------------------- ACT
    {
        "code": "act.math.rates",
        "track": "act",
        "name": "Rates and percents",
        "grade_band": 11,
        "order": 1,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "Find the unit rate first, then scale. Successive percent discounts multiply "
            "(0.75 × 0.90), they never add to a single 35% cut."
        ),
        "misconceptions": [
            "Adding successive percentages instead of multiplying factors",
            "Dividing distance by the wrong time"
        ],
    },
    {
        "code": "act.science.data",
        "track": "act",
        "name": "ACT science: reading data",
        "grade_band": 11,
        "order": 2,
        "prereq": "act.math.rates",
        "dot_target": 2,
        "intro": (
            "ACT science rarely asks for outside knowledge. Read the axes and table headers, find "
            "the trend, then answer exactly what the question asks about that trend."
        ),
        "misconceptions": [
            "Reading a data table as if the rows were time order when the header says otherwise",
            "Answering from general science knowledge instead of the figure"
        ],
    },
    {
        "code": "act.english.usage",
        "track": "act",
        "name": "Usage and punctuation",
        "grade_band": 11,
        "order": 3,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "Find the real subject before choosing the verb form — words like 'each', 'every' and "
            "'the team' are singular even when they are followed by a plural noun."
        ),
        "misconceptions": [
            "Matching the verb to the nearest noun instead of the subject",
            "Putting the apostrophe in the wrong place for a plural possessive"
        ],
    },

    # ---------------------------------------------------------------- MATHCOUNTS
    {
        "code": "mc.counting",
        "track": "mathcounts",
        "name": "Casework and counting",
        "grade_band": 7,
        "order": 1,
        "prereq": None,
        "dot_target": 3,
        "intro": (
            "Counting is organisation: multiply independent choices, divide out repeats, and count "
            "paths by choosing which steps are the horizontal ones."
        ),
        "misconceptions": [
            "Forgetting to divide by repeated letters",
            "Adding counts for overlapping sets instead of subtracting the overlap"
        ],
    },
    {
        "code": "mc.numbertheory",
        "track": "mathcounts",
        "name": "Divisibility and primes",
        "grade_band": 8,
        "order": 2,
        "prereq": "mc.counting",
        "dot_target": 3,
        "intro": (
            "Prime factorisation answers divisor-count and remainder questions. For factorials, "
            "count each prime's multiples, then its squares, then its cubes."
        ),
        "misconceptions": [
            "Counting divisors without adding one to each exponent",
            "Missing the 9s and 27s when counting powers in a factorial"
        ],
    },

    {
        "code": "mc.wordproblems",
        "track": "mathcounts",
        "name": "Multi-step word problems",
        "grade_band": 7,
        "order": 3,
        "prereq": "mc.counting",
        "dot_target": 3,
        "intro": (
            "Word problems are a chain of small steps. Name what each sentence asks you to compute, "
            "keep the units with the numbers, and only then do the arithmetic."
        ),
        "misconceptions": [
            "Answering with the last number computed instead of the quantity requested",
            "Mixing units such as minutes and hours in the same product"
        ],
    },

    # -------------------------------------------------------------------- AMC 8
    {
        "code": "amc8.geometry",
        "track": "amc8",
        "name": "AMC 8 geometry",
        "grade_band": 8,
        "order": 1,
        "prereq": None,
        "dot_target": 3,
        "intro": (
            "Most AMC 8 geometry is one formula plus one right triangle: know the Pythagorean "
            "triples, the triangle area formula and 2πr."
        ),
        "misconceptions": [
            "Using the diameter as the radius",
            "Forgetting the ½ in the triangle area formula"
        ],
    },
    {
        "code": "amc8.counting",
        "track": "amc8",
        "name": "AMC 8 counting and logic",
        "grade_band": 8,
        "order": 2,
        "prereq": "amc8.geometry",
        "dot_target": 3,
        "intro": (
            "Organise by cases or by size. Count small squares before big ones, and remove double "
            "counting whenever two lists overlap."
        ),
        "misconceptions": [
            "Counting only unit squares in a grid question",
            "Forgetting to subtract the overlap in 'divisible by 3 or 5' problems"
        ],
    },

    # ------------------------------------------------------------------- AMC 10
    {
        "code": "amc10.algebra",
        "track": "amc10",
        "name": "AMC 10 algebra",
        "grade_band": 10,
        "order": 1,
        "prereq": None,
        "dot_target": 3,
        "intro": (
            "Work with the expression the question asks about rather than solving for x. Squaring "
            "a sum like x + 1/x, and Vieta's sum −b/a, do most of the work."
        ),
        "misconceptions": [
            "Squaring a sum without the cross term",
            "Using b instead of −b/a for the sum of roots"
        ],
    },
    {
        "code": "amc10.geometry",
        "track": "amc10",
        "name": "AMC 10 geometry",
        "grade_band": 10,
        "order": 2,
        "prereq": "amc10.algebra",
        "dot_target": 3,
        "intro": (
            "Drop a perpendicular: a chord of a circle becomes a right triangle with half the chord "
            "as one leg. Split regular hexagons into six equilateral triangles."
        ),
        "misconceptions": [
            "Using half the chord as the distance to the centre",
            "Using the side length as the height of an equilateral triangle"
        ],
    },

    # ------------------------------------------------------------------- AMC 12
    {
        "code": "amc12.functions",
        "track": "amc12",
        "name": "AMC 12 functions and trig",
        "grade_band": 12,
        "order": 1,
        "prereq": None,
        "dot_target": 3,
        "intro": (
            "Function questions are about structure: sin(kx) has period 2π/k, a quadratic's minimum "
            "sits at its vertex, and an inverse undoes the original equation."
        ),
        "misconceptions": [
            "Reading f⁻¹(7) as f(7)",
            "Multiplying the period by k instead of dividing"
        ],
    },
    {
        "code": "amc12.combinatorics",
        "track": "amc12",
        "name": "AMC 12 combinatorics",
        "grade_band": 12,
        "order": 2,
        "prereq": "amc12.functions",
        "dot_target": 3,
        "intro": (
            "Choose whether order matters before you compute anything, and use 'at least one' = "
            "'all' − 'none' when the direct count is messy."
        ),
        "misconceptions": [
            "Using permutations when only the group matters",
            "Counting each handshake twice"
        ],
    },
    # ------------------------------------------------- grades 1-8 math
    {
        "code": "me.place",
        "track": "math.elem",
        "name": "Place value and rounding",
        "grade_band": 3,
        "order": 1,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "Every digit has a value set by its place: ones, tens, hundreds, thousands. "
            "Round by looking at the digit to the right of the place you are keeping."
        ),
        "misconceptions": [
            "Reading a digit as its face value instead of its place value",
            "Rounding up when the next digit is 4 or less"
        ],
    },
    {
        "code": "me.multdiv",
        "track": "math.elem",
        "name": "Multiplication and division",
        "grade_band": 3,
        "order": 2,
        "prereq": "me.place",
        "dot_target": 2,
        "intro": (
            "Multiplication is repeated equal groups; division asks how many groups fit. "
            "Arrays and area models show both at once."
        ),
        "misconceptions": [
            "Adding the groups instead of multiplying",
            "Mixing up the divisor with the quotient"
        ],
    },
    {
        "code": "me.fractions",
        "track": "math.elem",
        "name": "Fractions and how to compare them",
        "grade_band": 4,
        "order": 3,
        "prereq": "me.multdiv",
        "dot_target": 2,
        "intro": (
            "A fraction is a number of equal parts of a whole. Multiply top and bottom by the same "
            "number to rename it, and compare fractions over a common denominator."
        ),
        "misconceptions": [
            "Thinking a bigger denominator means a bigger fraction",
            "Adding numerators and denominators separately"
        ],
    },
    {
        "code": "me.decpercent",
        "track": "math.elem",
        "name": "Decimals and percent",
        "grade_band": 6,
        "order": 4,
        "prereq": "me.fractions",
        "dot_target": 2,
        "intro": (
            "Percent means out of 100, so 35% is 0.35. Percent change is the change divided by the "
            "original amount, not by the new one."
        ),
        "misconceptions": [
            "Subtracting a percent as if it were a dollar amount",
            "Dividing the change by the new price"
        ],
    },
    {
        "code": "me.ratio",
        "track": "math.elem",
        "name": "Ratios, rates and proportion",
        "grade_band": 6,
        "order": 5,
        "prereq": "me.decpercent",
        "dot_target": 2,
        "intro": (
            "A ratio compares two amounts; a rate compares amounts with different units. Find the "
            "unit rate, then scale it to the quantity you need."
        ),
        "misconceptions": [
            "Adding the same amount to both parts of a ratio",
            "Using the wrong base when scaling"
        ],
    },
    {
        "code": "me.geometry",
        "track": "math.elem",
        "name": "Area, perimeter and volume",
        "grade_band": 6,
        "order": 6,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "Perimeter is distance around, area is space covered (length × width, half for a triangle, "
            "πr² for a circle) and volume is space inside a solid."
        ),
        "misconceptions": [
            "Using base × height for a triangle without halving",
            "Confusing area with perimeter"
        ],
    },
    # --------------------------------------------------- high school math
    {
        "code": "hs.quadratics",
        "track": "math.hs",
        "name": "Quadratics",
        "grade_band": 10,
        "order": 1,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "Factor first, then use vertex form (x − h)² + k for the turning point. The discriminant "
            "b² − 4ac tells you how many real roots exist."
        ),
        "misconceptions": [
            "Reading the vertex sign from (x − h)² the wrong way",
            "Forgetting the quadratic has two roots"
        ],
    },
    {
        "code": "hs.functions",
        "track": "math.hs",
        "name": "Functions, composition and inverses",
        "grade_band": 10,
        "order": 2,
        "prereq": "hs.quadratics",
        "dot_target": 2,
        "intro": (
            "A function maps inputs to outputs. Compose inside-out, and remember that changes inside "
            "the brackets shift horizontally while changes outside shift vertically."
        ),
        "misconceptions": [
            "Composing in the wrong order (g(f(x)) instead of f(g(x)))",
            "Shifting left/right when the change is outside the function"
        ],
    },
    {
        "code": "hs.logs",
        "track": "math.hs",
        "name": "Exponents and logarithms",
        "grade_band": 10,
        "order": 3,
        "prereq": "hs.functions",
        "dot_target": 2,
        "intro": (
            "A logarithm answers 'what exponent gives this number?'. Adding logs multiplies their "
            "arguments; subtracting logs divides them."
        ),
        "misconceptions": [
            "Thinking log(a + b) = log a + log b",
            "Multiplying logs instead of adding them"
        ],
    },
    {
        "code": "hs.sequences",
        "track": "math.hs",
        "name": "Sequences and series",
        "grade_band": 10,
        "order": 4,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "Arithmetic sequences add a constant difference; geometric sequences multiply by a "
            "constant ratio. An infinite geometric series converges only when |r| < 1."
        ),
        "misconceptions": [
            "Treating a geometric sequence as arithmetic",
            "Forgetting the a in a/(1 − r)"
        ],
    },
    {
        "code": "hs.trig",
        "track": "math.hs",
        "name": "Trigonometry",
        "grade_band": 11,
        "order": 5,
        "prereq": "hs.functions",
        "dot_target": 3,
        "intro": (
            "SOH-CAH-TOA for right triangles, and the unit circle for every angle. The identity "
            "sin²θ + cos²θ = 1 links the two."
        ),
        "misconceptions": [
            "Swapping sine and cosine ratios",
            "Using degrees when radians are required"
        ],
    },
    {
        "code": "hs.vectors",
        "track": "math.hs",
        "name": "Vectors",
        "grade_band": 11,
        "order": 6,
        "prereq": "hs.trig",
        "dot_target": 2,
        "intro": (
            "A vector has size and direction. Add component by component, take the length with "
            "Pythagoras, and use the dot product to test perpendicularity."
        ),
        "misconceptions": [
            "Adding lengths instead of components",
            "Confusing the dot product with multiplication"
        ],
    },
    # ------------------------------------------------------------- AP math
    {
        "code": "apc.limits",
        "track": "apcalc",
        "name": "Limits and continuity",
        "grade_band": 12,
        "order": 1,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "A limit is where the function is heading, not where it lands. Factor or divide by the "
            "dominant power when direct substitution gives 0/0 or ∞/∞."
        ),
        "misconceptions": [
            "Reading 0/0 as zero",
            "Assuming a limit exists when the two sides disagree"
        ],
    },
    {
        "code": "apc.deriv",
        "track": "apcalc",
        "name": "Derivative rules",
        "grade_band": 12,
        "order": 2,
        "prereq": "apc.limits",
        "dot_target": 3,
        "intro": (
            "The power rule brings the exponent down; the product, quotient and chain rules cover "
            "combined functions. A derivative is a rate of change."
        ),
        "misconceptions": [
            "Differentiating a product as the product of derivatives",
            "Forgetting the inner derivative in the chain rule"
        ],
    },
    {
        "code": "apc.opt",
        "track": "apcalc",
        "name": "Optimisation and related rates",
        "grade_band": 12,
        "order": 3,
        "prereq": "apc.deriv",
        "dot_target": 3,
        "intro": (
            "Set the derivative to zero to find candidates, then check the endpoints and the second "
            "derivative. In related-rates problems, differentiate the relationship with respect to time."
        ),
        "misconceptions": [
            "Checking only f′ = 0 and ignoring endpoints",
            "Differentiating a related-rates equation with respect to the wrong variable"
        ],
    },
    {
        "code": "apc.integrals",
        "track": "apcalc",
        "name": "Integrals and the fundamental theorem",
        "grade_band": 12,
        "order": 4,
        "prereq": "apc.deriv",
        "dot_target": 3,
        "intro": (
            "An integral accumulates area. Add one to the exponent and divide by the new exponent, "
            "then evaluate the antiderivative at the limits."
        ),
        "misconceptions": [
            "Forgetting +C on an indefinite integral",
            "Substituting limits before finding the antiderivative"
        ],
    },
    {
        "code": "apc.series",
        "track": "apcalc",
        "name": "Sequences and series (BC)",
        "grade_band": 12,
        "order": 5,
        "prereq": "apc.integrals",
        "dot_target": 3,
        "intro": (
            "Use the ratio test for a radius of convergence. Geometric series sum to a/(1 − r), and "
            "the harmonic series is the classic divergent case."
        ),
        "misconceptions": [
            "Assuming terms going to zero makes a series converge",
            "Summing a geometric series without checking |r| < 1"
        ],
    },
    {
        "code": "aps.describe",
        "track": "apstats",
        "name": "Describing data",
        "grade_band": 12,
        "order": 1,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "Centre (mean, median) and spread (range, standard deviation) describe a data set. "
            "Outliers move the mean far more than the median."
        ),
        "misconceptions": [
            "Confusing the median with the mean",
            "Thinking standard deviation is a centre"
        ],
    },
    {
        "code": "aps.prob",
        "track": "apstats",
        "name": "Probability and independence",
        "grade_band": 12,
        "order": 2,
        "prereq": "aps.describe",
        "dot_target": 3,
        "intro": (
            "Multiply probabilities for independent events, and never forget the denominator drops "
            "when you draw without replacement."
        ),
        "misconceptions": [
            "Adding probabilities for 'and' events",
            "Forgetting that without replacement changes the total"
        ],
    },
    # -------------------------------------------------- olympiad ladder
    {
        "code": "aime.nt",
        "track": "aime",
        "name": "AIME number theory",
        "grade_band": 10,
        "order": 1,
        "prereq": None,
        "dot_target": 3,
        "intro": (
            "Prime factorise first: divisor counts and gcds fall out of the exponents. Modular "
            "arithmetic solves repeated-power remainders."
        ),
        "misconceptions": [
            "Counting divisors without the (a + 1)(b + 1) rule",
            "Adding counts in an inclusion-exclusion problem without subtracting the overlap"
        ],
    },
    {
        "code": "aime.combo",
        "track": "aime",
        "name": "AIME combinatorics",
        "grade_band": 10,
        "order": 2,
        "prereq": "aime.nt",
        "dot_target": 3,
        "intro": (
            "Decide whether order matters before writing anything. Round tables divide out the "
            "rotations; paths on a grid are a choice of steps."
        ),
        "misconceptions": [
            "Using permutations when only the set matters",
            "Forgetting to divide out rotational symmetry"
        ],
    },
    {
        "code": "aime.geo",
        "track": "aime",
        "name": "AIME geometry",
        "grade_band": 10,
        "order": 3,
        "prereq": None,
        "dot_target": 3,
        "intro": (
            "Look for a right triangle you can use: 5-12-13, 6-8-10, tangents perpendicular to "
            "radii. Area formulas often beat coordinate work."
        ),
        "misconceptions": [
            "Using the hypotenuse as a leg",
            "Forgetting that a tangent is perpendicular to the radius"
        ],
    },
    {
        "code": "usamo.algebra",
        "track": "usamo",
        "name": "USAMO algebra",
        "grade_band": 11,
        "order": 1,
        "prereq": None,
        "dot_target": 3,
        "intro": (
            "Symmetric expressions can be rewritten in terms of sums and products. Squaring an "
            "equation usually brings a helpful cross term."
        ),
        "misconceptions": [
            "Squaring a sum and ignoring the 2ab term",
            "Forgetting that a factored product is prime only when one factor is 1"
        ],
    },
    {
        "code": "usamo.nt",
        "track": "usamo",
        "name": "USAMO number theory",
        "grade_band": 11,
        "order": 2,
        "prereq": "usamo.algebra",
        "dot_target": 3,
        "intro": (
            "Count factors of 5 for trailing zeros, factor n² − 1 into consecutive numbers, and "
            "check parity before anything else."
        ),
        "misconceptions": [
            "Counting factors of 2 instead of 5 for trailing zeros",
            "Assuming n² − 1 is never divisible by 8"
        ],
    },
    {
        "code": "imo.geo",
        "track": "imo",
        "name": "IMO geometry",
        "grade_band": 12,
        "order": 1,
        "prereq": None,
        "dot_target": 3,
        "intro": (
            "Circle theorems do most of the work: opposite angles in a cyclic quadrilateral are "
            "supplementary, and tangents meet radii at right angles."
        ),
        "misconceptions": [
            "Treating every cyclic quadrilateral as a rectangle",
            "Confusing interior and exterior angle sums"
        ],
    },
    {
        "code": "imo.ineq",
        "track": "imo",
        "name": "IMO inequalities",
        "grade_band": 12,
        "order": 2,
        "prereq": "imo.geo",
        "dot_target": 3,
        "intro": (
            "AM-GM is the first tool: for positive numbers the arithmetic mean is at least the "
            "geometric mean, with equality when the numbers are equal."
        ),
        "misconceptions": [
            "Applying AM-GM to numbers that are not positive",
            "Assuming equality can happen with unequal numbers"
        ],
    },
    {
        "code": "mc.sprint",
        "track": "mathcounts",
        "name": "MATHCOUNTS sprint round",
        "grade_band": 7,
        "order": 10,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "The sprint round rewards clean arithmetic under time: unit rates, percent change and "
            "counting digits are all one-step ideas if you set them up right."
        ),
        "misconceptions": [
            "Adding percentages instead of applying them to a base",
            "Counting a digit twice in a 'contains' question"
        ],
    },
    {
        "code": "mc.target",
        "track": "mathcounts",
        "name": "MATHCOUNTS target round",
        "grade_band": 8,
        "order": 11,
        "prereq": "mc.sprint",
        "dot_target": 3,
        "intro": (
            "Target problems take two or three steps: factor, count with care, then check the "
            "last digit or the end of the number."
        ),
        "misconceptions": [
            "Using 5 choices per digit when only odd digits are allowed",
            "Counting trailing zeros from multiples of 10 only"
        ],
    },
    {
        "code": "amc8.geo",
        "track": "amc8",
        "name": "AMC 8 geometry",
        "grade_band": 8,
        "order": 10,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "AMC 8 geometry is mostly formulas used exactly once: Pythagoras, perimeter, angle sums, "
            "circumference."
        ),
        "misconceptions": [
            "Adding sides instead of squaring them for a diagonal",
            "Using the radius where the diameter is given"
        ],
    },
    {
        "code": "amc10.count",
        "track": "amc10",
        "name": "AMC 10 counting",
        "grade_band": 10,
        "order": 10,
        "prereq": None,
        "dot_target": 3,
        "intro": (
            "Choose between combinations and permutations by asking whether order matters, and "
            "count half of a symmetric set when the question asks for even numbers or sums."
        ),
        "misconceptions": [
            "Counting orderings when only the group matters",
            "Forgetting that a subset can be empty"
        ],
    },
    {
        "code": "amc12.trig",
        "track": "amc12",
        "name": "AMC 12 trigonometry",
        "grade_band": 12,
        "order": 10,
        "prereq": None,
        "dot_target": 3,
        "intro": (
            "Use the unit-circle values, the double-angle identities and the period 2π/k for "
            "sin(kx). Quadrant signs decide whether an answer is positive."
        ),
        "misconceptions": [
            "Ignoring the quadrant sign",
            "Using 2π as the period regardless of the coefficient"
        ],
    },
    # --------------------------------------------------- science (grades)
    {
        "code": "sci.living",
        "track": "science.all",
        "name": "Living things",
        "grade_band": 4,
        "order": 1,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "Living things grow, reproduce and use energy. Plants make food by photosynthesis; "
            "fungi decompose; animals are consumers."
        ),
        "misconceptions": [
            "Thinking anything that moves is alive",
            "Believing fungi are plants"
        ],
    },
    {
        "code": "sci.matter",
        "track": "science.all",
        "name": "Matter and changes",
        "grade_band": 5,
        "order": 2,
        "prereq": "sci.living",
        "dot_target": 2,
        "intro": (
            "Matter is solid, liquid or gas. A physical change keeps the same substance; a chemical "
            "change makes a new one."
        ),
        "misconceptions": [
            "Mixing up the Celsius and Fahrenheit freezing points",
            "Calling dissolving a chemical change"
        ],
    },
    {
        "code": "sci.force",
        "track": "science.all",
        "name": "Forces and motion",
        "grade_band": 6,
        "order": 3,
        "prereq": "sci.matter",
        "dot_target": 2,
        "intro": (
            "A force changes motion. Weight is the pull of gravity (mass × g), and Newton's third "
            "law pairs equal, opposite forces."
        ),
        "misconceptions": [
            "Confusing mass with weight",
            "Thinking a moving object needs a constant force"
        ],
    },
    {
        "code": "sci.earth",
        "track": "science.all",
        "name": "Earth and space",
        "grade_band": 6,
        "order": 4,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "Earth spins for day and night and orbits the Sun for the year. The tilted axis gives "
            "the seasons; the Moon's phases cycle about every 29.5 days."
        ),
        "misconceptions": [
            "Explaining seasons with distance from the Sun",
            "Thinking the Moon makes its own light"
        ],
    },
    {
        "code": "sci.energy",
        "track": "science.all",
        "name": "Energy",
        "grade_band": 7,
        "order": 5,
        "prereq": "sci.force",
        "dot_target": 2,
        "intro": (
            "Energy is stored (potential, chemical) or moving (kinetic). It is transferred and "
            "transformed, never created or destroyed."
        ),
        "misconceptions": [
            "Thinking energy disappears when something stops",
            "Confusing energy with force"
        ],
    },
    {
        "code": "sci.waves",
        "track": "science.all",
        "name": "Waves and sound",
        "grade_band": 7,
        "order": 6,
        "prereq": "sci.energy",
        "dot_target": 2,
        "intro": (
            "Waves carry energy without carrying matter. Sound needs a medium, and higher frequency "
            "means higher pitch."
        ),
        "misconceptions": [
            "Thinking sound can travel through a vacuum",
            "Confusing volume with pitch"
        ],
    },
    # ------------------------------------------------ college engineering
    {
        "code": "eng.statics",
        "track": "college.eng",
        "name": "Statics and equilibrium",
        "grade_band": 13,
        "order": 1,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "A body in equilibrium has zero net force and zero net moment. Moments are force times "
            "perpendicular distance."
        ),
        "misconceptions": [
            "Checking forces but forgetting moments",
            "Using the total load as one support reaction"
        ],
    },
    {
        "code": "eng.circuits",
        "track": "college.eng",
        "name": "Circuits and Ohm's law",
        "grade_band": 13,
        "order": 2,
        "prereq": "eng.statics",
        "dot_target": 2,
        "intro": (
            "V = IR relates voltage, current and resistance. Series resistances add; parallel ones "
            "combine reciprocally. Power is I²R."
        ),
        "misconceptions": [
            "Adding parallel resistances directly",
            "Using V = IR as the power formula"
        ],
    },
    {
        "code": "eng.thermo",
        "track": "college.eng",
        "name": "Thermodynamics",
        "grade_band": 13,
        "order": 3,
        "prereq": "eng.circuits",
        "dot_target": 2,
        "intro": (
            "Energy is conserved and entropy of an isolated system never decreases. Carnot efficiency "
            "is 1 − T_cold/T_hot."
        ),
        "misconceptions": [
            "Computing efficiency as T_cold/T_hot",
            "Thinking heat flows from cold to hot on its own"
        ],
    },
    {
        "code": "eng.materials",
        "track": "college.eng",
        "name": "Materials and stress",
        "grade_band": 13,
        "order": 4,
        "prereq": "eng.statics",
        "dot_target": 2,
        "intro": (
            "Stress is force over area and strain is change in length over original length. Young's "
            "modulus is the slope of the elastic part of the stress-strain curve."
        ),
        "misconceptions": [
            "Multiplying stress by area",
            "Calling yielding a reversible change"
        ],
    },
    {
        "code": "eng.fluids",
        "track": "college.eng",
        "name": "Fluids",
        "grade_band": 13,
        "order": 5,
        "prereq": "eng.materials",
        "dot_target": 2,
        "intro": (
            "Pressure grows with depth (p = ρgh). Bernoulli links faster flow to lower pressure, and "
            "an object floats when it is less dense than the fluid."
        ),
        "misconceptions": [
            "Thinking pressure depends on container shape",
            "Believing heavier objects always sink"
        ],
    },
    # -------------------------------------------------------- coding
    {
        "code": "code.vars",
        "track": "coding",
        "name": "Variables and types",
        "grade_band": 13,
        "order": 1,
        "prereq": None,
        "dot_target": 2,
        "intro": (
            "A variable names a value; its type decides what the operators do. Assignment happens "
            "left to right, and the right side is evaluated first."
        ),
        "misconceptions": [
            "Expecting 3 / 2 to be integer division",
            "Thinking a tuple assignment overwrites one value at a time"
        ],
    },
    {
        "code": "code.loops",
        "track": "coding",
        "name": "Loops and ranges",
        "grade_band": 13,
        "order": 2,
        "prereq": "code.vars",
        "dot_target": 2,
        "intro": (
            "range(start, stop) includes start and excludes stop. A while loop repeats while its "
            "condition holds, so the step size decides how many passes happen."
        ),
        "misconceptions": [
            "Including the stop value of a range",
            "Miscounting the passes of a while loop with a step larger than 1"
        ],
    },
    {
        "code": "code.funcs",
        "track": "coding",
        "name": "Functions and scope",
        "grade_band": 13,
        "order": 3,
        "prereq": "code.loops",
        "dot_target": 2,
        "intro": (
            "A function takes arguments, runs its body and returns a value (None if there is no "
            "return). Names created inside stay inside."
        ),
        "misconceptions": [
            "Assuming a function returns 0 by default",
            "Expecting a local variable to exist outside its function"
        ],
    },
    {
        "code": "code.lists",
        "track": "coding",
        "name": "Lists and slicing",
        "grade_band": 13,
        "order": 4,
        "prereq": "code.funcs",
        "dot_target": 2,
        "intro": (
            "Lists are indexed from 0. append adds to the end and a slice [a:b] keeps items from a "
            "up to but not including b."
        ),
        "misconceptions": [
            "Assuming lists are 1-indexed",
            "Including the end index of a slice"
        ],
    },
    {
        "code": "code.recursion",
        "track": "coding",
        "name": "Recursion",
        "grade_band": 13,
        "order": 5,
        "prereq": "code.lists",
        "dot_target": 3,
        "intro": (
            "A recursive function calls itself on a smaller input and stops at a base case. Trace it "
            "from the base case upward."
        ),
        "misconceptions": [
            "Writing the recursive call without shrinking the input",
            "Tracing from the top instead of from the base case"
        ],
    },
    {
        "code": "code.complexity",
        "track": "coding",
        "name": "Big-O and efficiency",
        "grade_band": 13,
        "order": 6,
        "prereq": "code.recursion",
        "dot_target": 2,
        "intro": (
            "Big-O counts how work grows with input size: one loop is O(n), nested loops O(n²), "
            "halving each step O(log n)."
        ),
        "misconceptions": [
            "Counting two sequential loops as O(n²)",
            "Thinking a hash lookup is linear"
        ],
    },
]


# --------------------------------------------------------------------------- #
# Bulk bank: skills for the imported datasets (MMLU, OpenBookQA, GSM8K) and the
# procedurally generated practice families. They are defined as data in
# seed/open_skills.py so this file stays readable.
# --------------------------------------------------------------------------- #

from seed.open_skills import TRACKS as _OPEN_TRACKS, SKILLS as _OPEN_SKILLS  # noqa: E402

TRACKS = TRACKS + _OPEN_TRACKS
SKILLS = SKILLS + _OPEN_SKILLS
