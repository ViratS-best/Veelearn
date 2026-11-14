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
]
