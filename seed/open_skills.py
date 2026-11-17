"""Skills and tracks for the imported + generated question bank.

The curated bank (`seed/qbank*.py`) is hand-written and small. This module defines
the *bulk* bank: questions imported from openly licensed datasets (MMLU, OpenBookQA,
GSM8K) and questions generated procedurally by `tools/build_open_bank.py`.

Every skill here is a plain data row, so `build_session_seed.py` validates it with
the same rules as the hand-written ones (intro, misconceptions, dot target, and a
prerequisite that lives in the same track).

Attribution rules live in one place (`import_bank.py`): a skill only exists if the
dataset rows behind it carry a real licence line, because the loader copies that
line onto every `qbank_items` row it writes.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Generated (procedural) skills. Each family in tools/gen_bank.py emits its items
# under one of these codes.
# --------------------------------------------------------------------------- #

GENERATED_SKILLS = [
    # code, track, name, grade, intro, misconception 1, misconception 2
    ("gen.k5.arith", "math.elem", "Whole-number arithmetic (practice)", 3,
     "Addition, subtraction, multiplication and division with whole numbers. Work from the place values; check a division by multiplying back.",
     "Adding the digits of a product instead of multiplying", "Borrowing without changing the next column"),
    ("gen.k5.fractions", "math.elem", "Fraction practice", 4,
     "Rename fractions to a common denominator before adding or comparing them, and simplify by the greatest common factor.",
     "Adding numerators and denominators separately", "Comparing fractions by denominator size alone"),
    ("gen.mid.percent", "math.elem", "Percent practice", 6,
     "Percent means per hundred. Find the part, the whole or the rate, and for a change divide by the *original* amount.",
     "Subtracting a percent as a flat amount", "Dividing the change by the new value"),
    ("gen.mid.ratio", "math.elem", "Rate and proportion practice", 6,
     "Find the unit rate first, then scale it. In a proportion, cross-multiply or divide both sides by the same factor.",
     "Scaling only one side of a proportion", "Using the wrong base for a rate"),
    ("gen.geometry.mensuration", "math.elem", "Area, perimeter and volume practice", 6,
     "Pick the formula that matches the shape: rectangle lw, triangle ½bh, circle πr², and volume = base area × height.",
     "Using base × height for a triangle", "Confusing radius and diameter"),
    ("gen.probability.basic", "math.elem", "Probability practice", 6,
     "Probability is favourable outcomes over total outcomes. Independent events multiply; 'not A' is 1 − P(A).",
     "Adding probabilities for 'and'", "Forgetting to subtract from 1 for 'not'"),
    ("gen.algebra.linear", "algebra1", "Linear equations and slope (practice)", 9,
     "Undo operations in reverse order to isolate the variable, and remember slope = change in y over change in x.",
     "Doing the same operation to only one side", "Flipping the slope ratio"),
    ("gen.sat.math", "sat.math", "SAT-style math practice", 11,
     "SAT math rewards clean setup: translate the sentence into an equation, then solve the equation you wrote.",
     "Answering the wrong quantity", "Forgetting to convert units"),
    ("gen.act.math", "act", "ACT-style math practice", 11,
     "ACT math is fast: estimate first, then check the exact answer. Watch units and averages.",
     "Averaging averages of unequal groups", "Using the wrong time conversion"),
    ("gen.contest.amc8", "amc8", "AMC 8-style practice", 8,
     "AMC 8 problems are short but exact: count carefully, look for a pattern, and check the answer against the question asked.",
     "Counting the same item twice", "Solving for a quantity nobody asked for"),
    ("gen.contest.amc10", "amc10", "AMC 10-style practice", 10,
     "Choose counting tools by whether order matters, and use modular arithmetic for remainders.",
     "Using combinations when order matters", "Forgetting that 0 and 1 are special cases"),
    ("gen.contest.amc12", "amc12", "AMC 12-style practice", 12,
     "Logs turn products into sums, and sequences need the right formula before any numbers go in.",
     "Treating a geometric sequence as arithmetic", "Using log base 10 where base 2 is required"),
    ("gen.contest.aime", "aime", "AIME-style practice", 10,
     "AIME answers are integers: factor, count with inclusion–exclusion, and reduce every step to a whole number.",
     "Counting divisors without the exponent rule", "Adding counts without removing overlap"),
    ("gen.contest.usamo", "usamo", "USAMO-style practice", 11,
     "Olympiad algebra is about structure: symmetric expressions in sums and products, and careful case counts.",
     "Squaring a sum without the cross term", "Forgetting the negative case in an absolute value"),
    ("gen.contest.imo", "imo", "IMO-style practice", 12,
     "Use AM-GM for minimums with equality at equal terms, and angle/circle facts for geometry.",
     "Applying AM-GM to non-positive numbers", "Assuming equality away from the equal case"),
    ("gen.code.python", "coding", "Python output and semantics", 13,
     "Trace the code with real values, one line at a time. Watch integer division, slicing and 0-based indexing.",
     "Assuming / is integer division", "Forgetting that slices exclude the end index"),
    ("gen.code.cpp", "coding", "C++ output and semantics", 13,
     "C++ integer division truncates toward zero, and arrays are 0-based. Trace the loop bounds exactly.",
     "Expecting integer division to produce a decimal", "Using <= where the loop needs <"),
    ("gen.code.java", "coding", "Java output and semantics", 13,
     "In Java, int division truncates and + concatenates when either side is a String. Trace types as well as values.",
     "Adding a String and an int numerically", "Expecting int division to round"),
    ("gen.sat.rw.grammar", "sat.rw", "SAT-style grammar and usage", 11,
     "Check the subject and verb agree, keep commas from joining two sentences, and make pronouns point at one clear noun.",
     "Matching a verb to the nearest noun", "Joining two sentences with a comma"),
    ("gen.act.english", "act", "ACT-style English usage", 11,
     "Read the whole sentence before choosing: agreement, tense and punctuation are where ACT English lives.",
     "Changing tense without a time cue", "Using an apostrophe for a plural"),
]

GENERATED_TRACKS = []  # generated families live in tracks the curated bank already has

# --------------------------------------------------------------------------- #
# Imported datasets. Each entry is one skill; `dataset` + `subject` select the
# rows in tools/build_open_bank.py.
# --------------------------------------------------------------------------- #

MMLU_TRACKS = [
    {"id": "ap.math", "name": "AP & college math (open bank)", "order": 23},
    {"id": "ap.sci", "name": "AP & college science (open bank)", "order": 24},
    {"id": "ap.humanities", "name": "AP humanities & social science (open bank)", "order": 25},
]

# MMLU subjects, grouped by the track they belong to. The first element is the
# MMLU subject id; the rest is what a learner sees.
MMLU_GROUPS = {
    "ap.math": [
        ("college_mathematics", "College mathematics"),
        ("abstract_algebra", "Abstract algebra"),
        ("high_school_mathematics", "High-school mathematics"),
        ("elementary_mathematics", "Elementary mathematics"),
        ("high_school_statistics", "High-school statistics"),
        ("formal_logic", "Formal logic"),
    ],
    "ap.sci": [
        ("college_physics", "College physics"),
        ("high_school_physics", "High-school physics"),
        ("conceptual_physics", "Conceptual physics"),
        ("college_chemistry", "College chemistry"),
        ("high_school_chemistry", "High-school chemistry"),
        ("college_biology", "College biology"),
        ("high_school_biology", "High-school biology"),
        ("astronomy", "Astronomy"),
        ("anatomy", "Anatomy"),
        ("clinical_knowledge", "Clinical knowledge"),
        ("college_medicine", "College medicine"),
        ("professional_medicine", "Professional medicine"),
        ("medical_genetics", "Medical genetics"),
        ("nutrition", "Nutrition"),
        ("virology", "Virology"),
        ("human_aging", "Human ageing"),
    ],
    "ap.humanities": [
        ("high_school_psychology", "High-school psychology"),
        ("professional_psychology", "Professional psychology"),
        ("high_school_macroeconomics", "High-school macroeconomics"),
        ("high_school_microeconomics", "High-school microeconomics"),
        ("econometrics", "Econometrics"),
        ("high_school_us_history", "US history"),
        ("high_school_world_history", "World history"),
        ("high_school_european_history", "European history"),
        ("high_school_geography", "Geography"),
        ("high_school_government_and_politics", "Government and politics"),
        ("philosophy", "Philosophy"),
        ("moral_disputes", "Moral disputes"),
        ("moral_scenarios", "Moral scenarios"),
        ("world_religions", "World religions"),
        ("sociology", "Sociology"),
        ("prehistory", "Prehistory"),
        ("security_studies", "Security studies"),
        ("public_relations", "Public relations"),
        ("international_law", "International law"),
        ("jurisprudence", "Jurisprudence"),
        ("logical_fallacies", "Logical fallacies"),
        ("management", "Management"),
        ("marketing", "Marketing"),
        ("business_ethics", "Business ethics"),
        ("professional_accounting", "Professional accounting"),
        ("professional_law", "Professional law"),
        ("human_sexuality", "Human sexuality"),
        ("miscellaneous", "General knowledge"),
        ("global_facts", "Global facts"),
        ("us_foreign_policy", "US foreign policy"),
    ],
}

# MMLU subjects that are computer science / engineering, so they land in the
# engineering and coding tracks instead of the science one.
MMLU_ENGINEERING = [
    ("electrical_engineering", "Electrical engineering"),
    ("college_computer_science", "College computer science"),
    ("high_school_computer_science", "High-school computer science"),
    ("machine_learning", "Machine learning"),
    ("computer_security", "Computer security"),
]

OPEN_SKILLS = [
    # code, track, name, grade, intro, misconception 1, misconception 2
    ("open.word.problems", "math.elem", "Multi-step word problems (GSM8K)", 6,
     "Word problems from the GSM8K set, written in plain everyday contexts. Name each step before computing it.",
     "Skipping the second step of the problem", "Answering a quantity the question did not ask for"),
    ("open.elem.science", "science.all", "Everyday science (OpenBookQA)", 5,
     "Short science questions about the everyday world, from the OpenBookQA set. Eliminate the options that contradict what you know.",
     "Choosing a true statement that does not answer the question", "Confusing cause with effect"),
]

MMLU_PREFIX = {
    "ap.math": "mmlu.math",
    "ap.sci": "mmlu.sci",
    "ap.humanities": "mmlu.hum",
}
ENGINEERING_PREFIX = "mmlu.eng"


def _mmlu_skill_code(track, subject):
    return f"{MMLU_PREFIX[track]}.{subject}".replace("-", "_")


def build_tracks():
    return list(MMLU_TRACKS)


def build_skills():
    """Every imported/generated skill as a skill_tree-shaped dict."""
    out = []

    for code, track, name, grade, intro, m1, m2 in GENERATED_SKILLS:
        out.append(
            {
                "code": code,
                "track": track,
                "name": name,
                "grade_band": grade,
                "order": 90,
                "prereq": None,
                "dot_target": 2,
                "intro": intro,
                "misconceptions": [m1, m2],
                "bulk": True,
            }
        )

    for track, subjects in MMLU_GROUPS.items():
        for i, (subject, label) in enumerate(subjects):
            out.append(
                {
                    "code": _mmlu_skill_code(track, subject),
                    "track": track,
                    "name": label,
                    "bulk": True,
                    "grade_band": 13 if track != "ap.humanities" else 12,
                    "order": i + 1,
                    "prereq": None,
                    "dot_target": 2,
                    "intro": (
                        f"{label}: multiple-choice questions from the MMLU bank (MIT licence). "
                        "Read the stem once for the subject, then eliminate the options that "
                        "misstate a definition or a fact."
                    ),
                    "misconceptions": [
                        "Recognising a term but not checking it answers the question",
                        "Choosing the most familiar option instead of the correct one",
                    ],
                }
            )
    for subject, label in MMLU_ENGINEERING:
        track = "coding" if "computer" in subject or subject in ("machine_learning", "computer_security") else "college.eng"
        out.append(
            {
                "code": f"{ENGINEERING_PREFIX}.{subject}".replace("-", "_"),
                "track": track,
                "name": label,
                "bulk": True,
                "grade_band": 13,
                "order": 95,
                "prereq": None,
                "dot_target": 2,
                "intro": (
                    f"{label}: multiple-choice questions from the MMLU bank (MIT licence). "
                    "Work from the definition, then check the option against the units or the "
                    "specific mechanism the stem describes."
                ),
                "misconceptions": [
                    "Matching a keyword without checking the mechanism",
                    "Mixing up two related quantities",
                ],
            }
        )

    for code, track, name, grade, intro, m1, m2 in OPEN_SKILLS:
        out.append(
            {
                "code": code,
                "track": track,
                "name": name,
                "grade_band": grade,
                "order": 96,
                "prereq": None,
                "dot_target": 2,
                "intro": intro,
                "misconceptions": [m1, m2],
                "bulk": True,
            }
        )
    return out


def mmlu_subject_skill(subject):
    """Map an MMLU subject id to the skill code it feeds."""
    for track, subjects in MMLU_GROUPS.items():
        for subj, _label in subjects:
            if subj == subject:
                return _mmlu_skill_code(track, subj)
    for subj, _label in MMLU_ENGINEERING:
        if subj == subject:
            return f"{ENGINEERING_PREFIX}.{subj}".replace("-", "_")
    return None


TRACKS = build_tracks()
SKILLS = build_skills()
