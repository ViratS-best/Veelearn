#!/usr/bin/env python3
"""Inject 60 comprehensive courses (5 per grade, grades 1-12) into Veelearn Aiven DB.

- Uses env vars at runtime for secrets.
- Uses proven quiz hydration flow with quiz-question-placeholder + data-question-id.
- Idempotent by (title, grade_level): update in place on reruns.
"""

import io
import json
import os
import random
import sys
from collections import defaultdict

import pymysql

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def getenv_int(name, default):
    value = os.getenv(name)
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


AIVEN_CONFIG = {
    "charset": "utf8mb4",
    "connect_timeout": 20,
    "cursorclass": pymysql.cursors.DictCursor,
    "db": os.getenv("MYSQL_DATABASE") or os.getenv("AIVEN_DB", "defaultdb"),
    "host": os.getenv("MYSQLHOST") or os.getenv("AIVEN_HOST", "veelearndb-asterloop-483e.i.aivencloud.com"),
    "password": os.getenv("MYSQLPASSWORD") or os.getenv("AIVEN_PASSWORD", ""),
    "port": getenv_int("MYSQLPORT", getenv_int("AIVEN_PORT", 26399)),
    "user": os.getenv("MYSQLUSER") or os.getenv("AIVEN_USER", "avnadmin"),
    "read_timeout": 30,
    "write_timeout": 30,
}

ssl_ca = os.getenv("DB_SSL_CA")
if ssl_ca:
    ca_path = os.path.join(os.getcwd(), "ca.pem")
    with open(ca_path, "w", encoding="utf-8") as f:
        f.write(ssl_ca.replace("\\n", "\n"))
    AIVEN_CONFIG["ssl"] = {"ca": ca_path}


SIMS = {
    "Arithmetic": "https://phet.colorado.edu/sims/html/arithmetic/latest/arithmetic_all.html",
    "Make a Ten": "https://phet.colorado.edu/sims/html/make-a-ten/latest/make-a-ten_all.html",
    "Number Compare": "https://phet.colorado.edu/sims/html/number-compare/latest/number-compare_all.html",
    "Number Line: Operations": "https://phet.colorado.edu/sims/html/number-line-operations/latest/number-line-operations_all.html",
    "Fractions: Intro": "https://phet.colorado.edu/sims/html/fractions-intro/latest/fractions-intro_all.html",
    "Fraction Matcher": "https://phet.colorado.edu/sims/html/fraction-matcher/latest/fraction-matcher_all.html",
    "Area Builder": "https://phet.colorado.edu/sims/html/area-builder/latest/area-builder_all.html",
    "Area Model Multiplication": "https://phet.colorado.edu/sims/html/area-model-multiplication/latest/area-model-multiplication_all.html",
    "Area Model Decimals": "https://phet.colorado.edu/sims/html/area-model-decimals/latest/area-model-decimals_all.html",
    "Ratio and Proportion": "https://phet.colorado.edu/sims/html/ratio-and-proportion/latest/ratio-and-proportion_all.html",
    "Unit Rates": "https://phet.colorado.edu/sims/html/unit-rates/latest/unit-rates_all.html",
    "Proportion Playground": "https://phet.colorado.edu/sims/html/proportion-playground/latest/proportion-playground_all.html",
    "Graphing Slope-Intercept": "https://phet.colorado.edu/sims/html/graphing-slope-intercept/latest/graphing-slope-intercept_all.html",
    "Expression Exchange": "https://phet.colorado.edu/sims/html/expression-exchange/latest/expression-exchange_all.html",
    "Graphing Quadratics": "https://phet.colorado.edu/sims/html/graphing-quadratics/latest/graphing-quadratics_all.html",
    "Trig Tour": "https://phet.colorado.edu/sims/html/trig-tour/latest/trig-tour_all.html",
    "Function Builder": "https://phet.colorado.edu/sims/html/function-builder/latest/function-builder_all.html",
    "Calculus Grapher": "https://phet.colorado.edu/sims/html/calculus-grapher/latest/calculus-grapher_all.html",
    "Forces and Motion: Basics": "https://phet.colorado.edu/sims/html/forces-and-motion-basics/latest/forces-and-motion-basics_all.html",
    "Balancing Act": "https://phet.colorado.edu/sims/html/balancing-act/latest/balancing-act_all.html",
    "Friction": "https://phet.colorado.edu/sims/html/friction/latest/friction_all.html",
    "Energy Skate Park: Basics": "https://phet.colorado.edu/sims/html/energy-skate-park-basics/latest/energy-skate-park-basics_all.html",
    "Energy Forms and Changes": "https://phet.colorado.edu/sims/html/energy-forms-and-changes/latest/energy-forms-and-changes_all.html",
    "Gravity Force Lab: Basics": "https://phet.colorado.edu/sims/html/gravity-force-lab-basics/latest/gravity-force-lab-basics_all.html",
    "Gravity and Orbits": "https://phet.colorado.edu/sims/html/gravity-and-orbits/latest/gravity-and-orbits_all.html",
    "Waves Intro": "https://phet.colorado.edu/sims/html/waves-intro/latest/waves-intro_all.html",
    "Sound Waves": "https://phet.colorado.edu/sims/html/sound-waves/latest/sound-waves_all.html",
    "Under Pressure": "https://phet.colorado.edu/sims/html/under-pressure/latest/under-pressure_all.html",
    "Buoyancy: Basics": "https://phet.colorado.edu/sims/html/buoyancy-basics/latest/buoyancy-basics_all.html",
    "Collision Lab": "https://phet.colorado.edu/sims/html/collision-lab/latest/collision-lab_all.html",
    "Vector Addition": "https://phet.colorado.edu/sims/html/vector-addition/latest/vector-addition_all.html",
    "Circuit Construction Kit (DC)": "https://phet.colorado.edu/sims/html/circuit-construction-kit-dc/latest/circuit-construction-kit-dc_all.html",
    "Magnets and Electromagnets": "https://phet.colorado.edu/sims/html/magnets-and-electromagnets/latest/magnets-and-electromagnets_all.html",
    "Projectile Motion": "https://phet.colorado.edu/sims/html/projectile-motion/latest/projectile-motion_all.html",
    "Energy Skate Park": "https://phet.colorado.edu/sims/html/energy-skate-park/latest/energy-skate-park_all.html",
    "Ohm's Law": "https://phet.colorado.edu/sims/html/ohms-law/latest/ohms-law_all.html",
    "Faraday's Electromagnetic Lab": "https://phet.colorado.edu/sims/html/faradays-electromagnetic-lab/latest/faradays-electromagnetic-lab_all.html",
    "Wave Interference": "https://phet.colorado.edu/sims/html/wave-interference/latest/wave-interference_all.html",
    "Geometric Optics": "https://phet.colorado.edu/sims/html/geometric-optics/latest/geometric-optics_all.html",
    "Quantum Measurement": "https://phet.colorado.edu/sims/html/quantum-measurement/latest/quantum-measurement_all.html",
    "Models of the Hydrogen Atom": "https://phet.colorado.edu/sims/html/models-of-the-hydrogen-atom/latest/models-of-the-hydrogen-atom_all.html",
    "States of Matter: Basics": "https://phet.colorado.edu/sims/html/states-of-matter-basics/latest/states-of-matter-basics_all.html",
    "Concentration": "https://phet.colorado.edu/sims/html/concentration/latest/concentration_all.html",
    "Build an Atom": "https://phet.colorado.edu/sims/html/build-an-atom/latest/build-an-atom_all.html",
    "Atomic Interactions": "https://phet.colorado.edu/sims/html/atomic-interactions/latest/atomic-interactions_all.html",
    "Build a Molecule": "https://phet.colorado.edu/sims/html/build-a-molecule/latest/build-a-molecule_all.html",
    "Balancing Chemical Equations": "https://phet.colorado.edu/sims/html/balancing-chemical-equations/latest/balancing-chemical-equations_all.html",
    "pH Scale: Basics": "https://phet.colorado.edu/sims/html/ph-scale-basics/latest/ph-scale-basics_all.html",
    "Acid-Base Solutions": "https://phet.colorado.edu/sims/html/acid-base-solutions/latest/acid-base-solutions_all.html",
    "Molarity": "https://phet.colorado.edu/sims/html/molarity/latest/molarity_all.html",
    "Reactants, Products and Leftovers": "https://phet.colorado.edu/sims/html/reactants-products-and-leftovers/latest/reactants-products-and-leftovers_all.html",
    "Molecule Shapes: Basics": "https://phet.colorado.edu/sims/html/molecule-shapes-basics/latest/molecule-shapes-basics_all.html",
    "Molecule Polarity": "https://phet.colorado.edu/sims/html/molecule-polarity/latest/molecule-polarity_all.html",
    "Gas Properties": "https://phet.colorado.edu/sims/html/gas-properties/latest/gas-properties_all.html",
    "Beer's Law Lab": "https://phet.colorado.edu/sims/html/beers-law-lab/latest/beers-law-lab_all.html",
    "Isotopes and Atomic Mass": "https://phet.colorado.edu/sims/html/isotopes-and-atomic-mass/latest/isotopes-and-atomic-mass_all.html",
    "Molecules and Light": "https://phet.colorado.edu/sims/html/molecules-and-light/latest/molecules-and-light_all.html",
    "Natural Selection": "https://phet.colorado.edu/sims/html/natural-selection/latest/natural-selection_all.html",
    "Greenhouse Effect": "https://phet.colorado.edu/sims/html/greenhouse-effect/latest/greenhouse-effect_all.html",
    "Membrane Transport": "https://phet.colorado.edu/sims/html/membrane-transport/latest/membrane-transport_all.html",
    "Neuron": "https://phet.colorado.edu/sims/html/neuron/latest/neuron_all.html",
    "Gene Expression Essentials": "https://phet.colorado.edu/sims/html/gene-expression-essentials/latest/gene-expression-essentials_all.html",
    "Build a Nucleus": "https://phet.colorado.edu/sims/html/build-a-nucleus/latest/build-a-nucleus_all.html",
    "Center and Variability": "https://phet.colorado.edu/sims/html/center-and-variability/latest/center-and-variability_all.html",
    "Plinko Probability": "https://phet.colorado.edu/sims/html/plinko-probability/latest/plinko-probability_all.html",
    "Curve Fitting": "https://phet.colorado.edu/sims/html/curve-fitting/latest/curve-fitting_all.html",
    "Least-Squares Regression": "https://phet.colorado.edu/sims/html/least-squares-regression/latest/least-squares-regression_all.html",
}

STRANDS = ["math", "physics", "chemistry", "bioearth", "applied"]

TOPICS = {
    "math": ["Number Sense and Addition Stories", "Place Value and Subtraction Strategies", "Fractions and Multiplication Foundations", "Equivalent Fractions and Area Models", "Decimals, Volume, and Data Modeling", "Ratios, Rates, and Percent Reasoning", "Proportional Geometry and Probability", "Linear Models and Function Thinking", "Algebra I: Expressions, Equations, and Systems", "Algebra II and Trigonometric Modeling", "Precalculus, Sequences, and Advanced Functions", "Calculus and Optimization Studio"],
    "physics": ["Motion and Push-Pull Science", "Friction, Ramps, and Simple Machines", "Energy in Motion", "Gravity and Orbit Explorers", "Waves, Sound, and Light Foundations", "Pressure, Buoyancy, and Density", "Mechanics and Collisions", "Electricity and Magnetism Basics", "Classical Mechanics with Modeling", "Electromagnetic Systems and Circuits", "Waves, Optics, and Modern Physics", "Quantum and Relativistic Perspectives"],
    "chemistry": ["Matter Around Us", "Solutions and Mixing", "Atomic Building Blocks", "Molecules and Chemical Change", "Acids, Bases, and Indicators", "Concentration and Reaction Yield", "Molecular Geometry and Polarity", "Gas Laws and Particle Dynamics", "Stoichiometry and Solution Chemistry", "Thermochemistry and Equilibrium", "Atomic Theory and Spectroscopy", "Advanced Physical and Organic Chemistry"],
    "bioearth": ["Living Things and Habitats", "Weather, Climate, and Life", "Cells and Body Systems Intro", "Ecosystems and Adaptation", "Earth Systems and Human Impact", "Genetics and Heredity Foundations", "Ecology and Population Change", "Human Physiology and Signaling", "Molecular Biology and Evolution", "Biotechnology and Systems Biology", "Neurobiology and Advanced Physiology", "Genomics, Evolution, and Climate Connections"],
    "applied": ["Pattern Games and Data Stories", "Engineering Design Starters", "Intro Coding Logic and Debugging", "Data Investigation Lab", "Applied Problem Solving Studio", "Financial Literacy and Decision Math", "Statistical Thinking and Sampling", "Computational Modeling and Simulation", "Engineering Systems and Optimization", "Data Science with Regression and Uncertainty", "Research Methods and Experimental Design", "Capstone Modeling and Decision Analytics"],
}

FOCUS = {
    "math": ["representation", "reasoning", "fluency", "modeling"],
    "physics": ["forces", "energy", "systems", "evidence"],
    "chemistry": ["particles", "conservation", "reactions", "quantification"],
    "bioearth": ["systems", "adaptation", "data interpretation", "mechanisms"],
    "applied": ["decision making", "constraints", "optimization", "communication"],
}

SIM_CYCLES = {
    "math": ["Arithmetic", "Make a Ten", "Number Compare", "Number Line: Operations", "Fractions: Intro", "Fraction Matcher", "Area Model Multiplication", "Area Builder", "Area Model Decimals", "Ratio and Proportion", "Unit Rates", "Proportion Playground", "Graphing Slope-Intercept", "Expression Exchange", "Graphing Quadratics", "Trig Tour", "Function Builder", "Calculus Grapher"],
    "physics": ["Forces and Motion: Basics", "Balancing Act", "Friction", "Energy Skate Park: Basics", "Energy Forms and Changes", "Gravity Force Lab: Basics", "Gravity and Orbits", "Waves Intro", "Sound Waves", "Under Pressure", "Buoyancy: Basics", "Collision Lab", "Vector Addition", "Circuit Construction Kit (DC)", "Magnets and Electromagnets", "Projectile Motion", "Energy Skate Park", "Ohm's Law", "Faraday's Electromagnetic Lab", "Wave Interference", "Geometric Optics", "Quantum Measurement", "Models of the Hydrogen Atom"],
    "chemistry": ["States of Matter: Basics", "Concentration", "Build an Atom", "Atomic Interactions", "Build a Molecule", "Balancing Chemical Equations", "pH Scale: Basics", "Acid-Base Solutions", "Molarity", "Reactants, Products and Leftovers", "Molecule Shapes: Basics", "Molecule Polarity", "Gas Properties", "Beer's Law Lab", "Isotopes and Atomic Mass", "Molecules and Light"],
    "bioearth": ["Natural Selection", "Greenhouse Effect", "Membrane Transport", "Neuron", "Gene Expression Essentials", "Build a Nucleus"],
    "applied": ["Center and Variability", "Plinko Probability", "Curve Fitting", "Least-Squares Regression", "Function Builder", "Unit Rates", "Area Builder", "Graphing Slope-Intercept"],
}


def pick_sims(strand, grade_index):
    cycle = SIM_CYCLES[strand]
    a = (grade_index * 2) % len(cycle)
    b = (grade_index * 2 + 1) % len(cycle)
    return [cycle[a], cycle[b]]


def make_blueprints():
    courses = []
    for grade in range(1, 13):
        gi = grade - 1
        for strand in STRANDS:
            courses.append({
                "grade": grade,
                "strand": strand,
                "title": f"Grade {grade} {TOPICS[strand][gi]}",
                "description": f"Comprehensive Grade {grade} {strand} course with deep instruction, solved examples, PhET labs, and independent student problem sets.",
                "focus_points": list(FOCUS[strand]),
                "sims": pick_sims(strand, gi),
            })
    return courses


def depth_text(grade):
    if grade <= 2:
        return "concrete visuals, guided language, and step-by-step routines"
    if grade <= 5:
        return "model-based reasoning with increasingly complex multi-step tasks"
    if grade <= 8:
        return "formal structure, comparative reasoning, and evidence-backed explanation"
    if grade <= 10:
        return "symbolic fluency, analytical argumentation, and cross-topic transfer"
    return "advanced abstraction, mathematically rigorous justification, and capstone-level synthesis"


def strand_examples(strand, grade):
    if strand == "math":
        return [
            ("Compute 38 + 27 using place-value decomposition.", ["Break into tens/ones", "Add tens and ones", "Recombine for final sum"], "65"),
            ("Find 3/4 + 1/8.", ["Common denominator 8", "3/4 = 6/8", "6/8 + 1/8 = 7/8"], "7/8"),
            ("Solve 4(x - 3) = 2x + 10.", ["Expand", "Collect x terms", "Isolate x"], "x = 11"),
        ]
    if strand == "physics":
        m = 2 + grade
        f = 12 + 3 * grade
        return [
            (f"Find acceleration for force {f} N on mass {m} kg.", ["Use a=F/m", "Substitute values", "Compute with units"], f"{f/m:.2f} m/s^2"),
            (f"Find kinetic energy for mass {m} kg moving at {grade+3} m/s.", ["Use KE=1/2mv^2", "Substitute values", "Calculate"], f"{0.5*m*(grade+3)**2:.1f} J"),
            (f"Find potential energy for mass {m} kg at height {grade+4} m.", ["Use PE=mgh", "Substitute g=9.8", "Compute"], f"{m*9.8*(grade+4):.1f} J"),
        ]
    if strand == "chemistry":
        n = 0.6 + grade * 0.1
        v = 1.2 + grade * 0.2
        return [
            (f"Find molarity of {n:.2f} mol in {v:.2f} L.", ["Use M=n/V", "Substitute", "Compute"], f"{n/v:.2f} M"),
            ("Balance: __ H2 + __ O2 -> __ H2O.", ["Balance oxygen", "Balance hydrogen", "Check both sides"], "2 H2 + O2 -> 2 H2O"),
            ("Classify a solution with pH 3.2.", ["Recall pH<7 acidic", "Compare with 7", "State class"], "Acidic"),
        ]
    if strand == "bioearth":
        start = 50 + 5 * grade
        return [
            (f"Population starts at {start} and grows by 10%. Next year estimate?", ["Multiply by 1.10", "Compute", "Round if needed"], str(int(round(start * 1.10)))),
            ("For Bb x Bb, probability of bb?", ["Draw Punnett square", "Count favorable outcomes", "Convert to percent"], "25%"),
            ("Concentration drops from 18 to 6 across a membrane. Gradient?", ["Subtract low from high", "Interpret driving force", "Report"], "12"),
        ]
    values = [grade + 2, grade + 4, grade + 6, grade + 8, grade + 10]
    avg = sum(values) / len(values)
    return [
        (f"Find the mean of dataset {values}.", ["Add all values", "Divide by count", "State mean"], f"{avg:.1f}"),
        (f"Budget is $120 and each item costs ${grade+5}. Max whole items?", ["Use integer division", "Ignore fractional item", "Report count"], str(120 // (grade + 5))),
        ("Why compare multiple models before a decision?", ["Check fit", "Check assumptions", "Compare risk"], "To balance accuracy, assumptions, and risk"),
    ]

def practice_prompts(strand, grade, focus):
    prompts = [
        f"Explain '{focus[0]}' with a model and one real-world example for Grade {grade}.",
        f"Solve a multi-step task involving '{focus[1]}' and justify every step.",
        f"Create your own problem using '{focus[2]}' and solve it completely.",
        f"Use a table or graph to analyze a pattern related to '{focus[3]}'.",
        "Identify one common misconception and correct it using evidence.",
        "Design a mini-investigation with hypothesis, variables, and expected result.",
        "Compare two solution strategies and defend your preferred method.",
        "Write one transfer challenge that combines at least two course concepts.",
    ]
    if strand == "physics":
        prompts[1] = "Compute force, energy, or pressure from data and explain the physical meaning."
    elif strand == "chemistry":
        prompts[1] = "Compute concentration, pH, or stoichiometric quantity and explain assumptions."
    elif strand == "bioearth":
        prompts[1] = "Interpret a biology/climate dataset and justify a claim with evidence."
    elif strand == "applied":
        prompts[1] = "Make a data-driven decision under constraints and explain trade-offs."
    return prompts


def render_sim_html(sim_names):
    html_parts = []
    for sim_name in sim_names:
        html_parts.append(
            f"<div style=\"margin:16px 0;\"><h4>PhET Lab: {sim_name}</h4>"
            f"<iframe src=\"{SIMS[sim_name]}\" width=\"100%\" height=\"560\" frameborder=\"0\" "
            f"style=\"border:1px solid #d1d5db; border-radius:8px;\"></iframe>"
            "<p><em>Lab Prompt:</em> Run three trials, record data, and write a claim-evidence-reasoning summary.</p></div>"
        )
    return "\n".join(html_parts)


def build_content(course):
    grade = course["grade"]
    strand = course["strand"]
    focus = course["focus_points"]
    examples = strand_examples(strand, grade)
    walkthrough_examples = list(reversed(examples[:2]))

    ex_html = []
    for i, (problem, steps, answer) in enumerate(examples, 1):
        steps_html = "".join([f"<li>{s}</li>" for s in steps])
        ex_html.append(
            f"<div style=\"background:#f4f8ff; border:1px solid #c9def4; border-radius:10px; padding:16px; margin:14px 0;\">"
            f"<h4>Worked Example {i}</h4><p><strong>Problem:</strong> {problem}</p><ol>{steps_html}</ol>"
            f"<p><strong>Answer:</strong> {answer}</p></div>"
        )

    walkthrough_html = []
    for i, (problem, steps, answer) in enumerate(walkthrough_examples, 1):
        custom_steps = list(steps) + [
            "Check the result with a second method or reasonableness estimate.",
            "Write one sentence connecting the result to a real-world interpretation."
        ]
        steps_html = "".join([f"<li>{s}</li>" for s in custom_steps])
        walkthrough_html.append(
            f"<div style=\"background:#fff9ef; border:1px solid #f7d08a; border-radius:10px; padding:16px; margin:14px 0;\">"
            f"<h4>Practice Walkthrough {i} (Solved)</h4><p><strong>Problem:</strong> {problem}</p><ol>{steps_html}</ol>"
            f"<p><strong>Final Answer:</strong> {answer}</p></div>"
        )

    focus_html = "".join([f"<li><strong>{f.title()}</strong>: apply with evidence and clear explanation.</li>" for f in focus])
    practice_html = "".join([f"<li>{p}</li>" for p in practice_prompts(strand, grade, focus)])

    return (
        f"<h1>{course['title']}</h1>"
        f"<p><strong>Grade:</strong> {grade}</p><p>{course['description']}</p>"
        f"<p>This course is intentionally deep and comprehensive using {depth_text(grade)}.</p><hr>"
        f"<h2>Module 1: Big Ideas and Targets</h2><ul>{focus_html}</ul>"
        "<h2>Module 2: Concept Development</h2>"
        "<p>Students build precise definitions, representations, and transfer strategies. Every lesson expects reasoning, not only answers.</p>"
        f"<h2>Module 3: Fully Solved Example Problems</h2>{''.join(ex_html)}"
        f"<h2>Module 4: Interactive PhET Investigation Studio</h2>{render_sim_html(course['sims'])}"
        f"<h2>Module 5: Student Problems to Solve</h2><ol>{practice_html}</ol>"
        f"<h2>Module 6: Deep Practice Walkthroughs (Solved)</h2>{''.join(walkthrough_html)}"
        "<h2>Module 7: Capstone Challenge</h2>"
        "<p>Create a real-world case study integrating at least two course ideas. Include model, data, complete solution path, and reflection on assumptions/limits.</p>"
    )

def make_question(text, correct, distractors, explanation, idx):
    opts = [correct] + distractors[:3]
    unique = []
    for opt in opts:
        if opt not in unique:
            unique.append(opt)
    while len(unique) < 4:
        unique.append(f"Option {len(unique)+1}")
    return {
        "question_text": text,
        "question_type": "multiple_choice",
        "options": unique,
        "correct_answer": correct,
        "explanation": explanation,
        "points": 1,
        "order_index": idx,
    }


def build_questions(course):
    grade = course["grade"]
    strand = course["strand"]
    focus = course["focus_points"]
    out = [
        make_question(
            f"Which statement best describes '{focus[0]}' in this course?",
            "It is a core concept used to model and explain outcomes with evidence.",
            ["It is optional vocabulary only.", "It replaces reasoning steps.", "It applies only to memorization."],
            "Core concepts drive reasoning and transfer.",
            1,
        )
    ]

    if strand == "math":
        a, b = grade + 6, grade + 4
        out += [
            make_question(f"Compute {a} + {b}.", str(a + b), [str(a + b + 1), str(a + b - 1), str(a + b + 2)], "Arithmetic fluency supports complex tasks.", 2),
            make_question("In y = mx + b, m is:", "Slope", ["Y-intercept", "Domain", "Range"], "Slope is rate of change.", 3),
            make_question("A strong multi-step math solution includes:", "Model, steps, and justification", ["Final answer only", "Guess only", "No units"], "Reasoning must be visible.", 4),
        ]
    elif strand == "physics":
        m, f = grade + 2, 12 + 3 * grade
        out += [
            make_question(f"If F={f} N and m={m} kg, acceleration is:", f"{f/m:.2f} m/s^2", [f"{f/m+1:.2f} m/s^2", f"{f/m-1:.2f} m/s^2", f"{2*f/m:.2f} m/s^2"], "Use a=F/m.", 2),
            make_question("In a closed system, which is conserved?", "Total energy", ["Velocity", "Temperature", "Pressure"], "Energy conservation is fundamental.", 3),
            make_question("Slope of a velocity-time graph gives:", "Acceleration", ["Distance", "Mass", "Power"], "Slope of v-t graph is acceleration.", 4),
        ]
    elif strand == "chemistry":
        n, v = 0.6 + grade * 0.1, 1.2 + grade * 0.2
        out += [
            make_question(f"Molarity of {n:.2f} mol in {v:.2f} L is:", f"{n/v:.2f} M", [f"{n/v+0.5:.2f} M", f"{n/v-0.2:.2f} M", f"{2*n/v:.2f} M"], "M=n/V.", 2),
            make_question("Balanced equations are required because:", "Atoms and charge are conserved", ["Mass is created", "Reactants vanish", "Products decide coefficients"], "Conservation laws must hold.", 3),
            make_question("A solution with pH 2.9 is:", "Acidic", ["Basic", "Neutral", "Unknown"], "pH below 7 is acidic.", 4),
        ]
    elif strand == "bioearth":
        out += [
            make_question("For Bb x Bb, probability of bb is:", "25%", ["0%", "50%", "75%"], "Punnett square gives 1/4 bb.", 2),
            make_question("Natural selection works through:", "Differential survival and reproduction", ["Instant replacement", "No inherited variation", "Random grading"], "Selection acts on heritable variation.", 3),
            make_question("Strong scientific claims require:", "Measured evidence and mechanism", ["Opinion only", "Anecdote only", "Single unlabeled image"], "Evidence + mechanism are required.", 4),
        ]
    else:
        out += [
            make_question("What makes a model useful for decisions?", "Testable assumptions and interpretable outputs", ["Never changing rules", "No data", "Random formulas"], "Useful models are validated and interpretable.", 2),
            make_question("Why compare two strategies?", "To evaluate efficiency and assumptions", ["To avoid evidence", "To increase confusion", "Because both must disagree"], "Comparison improves decision quality.", 3),
            make_question("Sampling bias causes:", "Misleading conclusions", ["Perfect certainty", "Guaranteed causality", "Lower uncertainty"], "Bias skews inference.", 4),
        ]

    out += [
        make_question("Which simulations are embedded in this course?", f"{course['sims'][0]} and {course['sims'][1]}", [f"{course['sims'][0]} and Arithmetic", "No simulations are used", "Only static diagrams"], "Every course includes two PhET labs.", 5),
        make_question("What is expected in student submissions?", "Steps, reasoning, and clear conclusions", ["Only final answer", "No explanation needed", "One-word response"], "Mastery requires transparent reasoning.", 6),
        make_question("CER stands for:", "Claim, Evidence, Reasoning", ["Claim, Example, Revision", "Calculate, Estimate, Report", "Compare, Evaluate, Repeat"], "CER is a standard explanation framework.", 7),
        make_question("Why run multiple simulation trials?", "To detect patterns and reduce one-off error", ["One trial is always wrong", "To avoid data recording", "To force one outcome"], "Replication improves reliability.", 8),
        make_question("Transfer of learning means:", "Applying ideas in a new context", ["Memorizing only", "Copying exact examples only", "Ignoring constraints"], "Transfer shows deeper understanding.", 9),
        make_question("Capstone should include:", "Model, data, full solution path, and reflection", ["Title only", "Single numeric answer", "Formula list without context"], "Capstones assess synthesis and communication.", 10),
    ]
    return out


def shuffle_options(question, rng):
    q = dict(question)
    options = list(q["options"])
    rng.shuffle(options)
    if q["correct_answer"] not in options:
        options[0] = q["correct_answer"]
        rng.shuffle(options)
    q["options"] = options
    return q


def resolve_creator_id(cursor):
    preferred = os.getenv("COURSE_CREATOR_ID")
    if preferred and preferred.isdigit():
        cursor.execute("SELECT id FROM users WHERE id=%s LIMIT 1", (int(preferred),))
        row = cursor.fetchone()
        if row:
            return row["id"]
    cursor.execute("SELECT id FROM users WHERE role IN ('superadmin','admin') ORDER BY id ASC LIMIT 1")
    row = cursor.fetchone()
    if row:
        return row["id"]
    cursor.execute("SELECT id FROM users ORDER BY id ASC LIMIT 1")
    row = cursor.fetchone()
    return row["id"] if row else None


def placeholder_html(question_id, idx):
    return (
        f'<div class="quiz-question-placeholder" data-question-id="{question_id}" '
        f'style="background: #e0e7ff; border: 2px solid #667eea; padding: 1.5em; margin: 1.5em 0; '
        f'border-radius: 8px; user-select: none;"><strong>Quiz Question {idx}</strong></div>'
    )

def upsert_course(cursor, course, creator_id, rng):
    title = course["title"]
    grade = course["grade"]
    content = build_content(course)
    questions = build_questions(course)

    cursor.execute("SELECT id FROM courses WHERE title=%s AND grade_level=%s ORDER BY id ASC LIMIT 1", (title, grade))
    row = cursor.fetchone()
    if row:
        course_id = row["id"]
        cursor.execute("UPDATE courses SET description=%s, content=%s, status='approved' WHERE id=%s", (course["description"], content, course_id))
        action = "updated"
    else:
        cursor.execute(
            """
            INSERT INTO courses (title, description, content, creator_id, status, grade_level)
            VALUES (%s, %s, %s, %s, 'approved', %s)
            """,
            (title, course["description"], content, creator_id, grade),
        )
        cursor.execute("SELECT LAST_INSERT_ID() AS id")
        course_id = cursor.fetchone()["id"]
        action = "inserted"

    cursor.execute("DELETE FROM course_questions WHERE course_id=%s", (course_id,))

    qids = []
    for raw_q in questions:
        q = shuffle_options(raw_q, rng)
        cursor.execute(
            """
            INSERT INTO course_questions
            (course_id, question_text, question_type, options, correct_answer, explanation, points, order_index)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (course_id, q["question_text"], q["question_type"], json.dumps(q["options"]), q["correct_answer"], q["explanation"], q["points"], q["order_index"]),
        )
        cursor.execute("SELECT LAST_INSERT_ID() AS id")
        qids.append(cursor.fetchone()["id"])

    hydrated = content + "".join([placeholder_html(qid, idx) for idx, qid in enumerate(qids, 1)])
    cursor.execute("UPDATE courses SET content=%s, status='approved' WHERE id=%s", (hydrated, course_id))
    return {"id": course_id, "grade": grade, "title": title, "questions": len(qids), "action": action}


def verify(cursor, ids):
    if not ids:
        return []
    placeholders = ",".join(["%s"] * len(ids))
    cursor.execute(
        f"""
        SELECT c.id, c.grade_level, c.title,
               COUNT(q.id) AS q_count,
               (LENGTH(c.content)-LENGTH(REPLACE(c.content, 'quiz-question-placeholder', ''))) /
               LENGTH('quiz-question-placeholder') AS p_count
        FROM courses c
        LEFT JOIN course_questions q ON q.course_id = c.id
        WHERE c.id IN ({placeholders})
        GROUP BY c.id, c.grade_level, c.title, c.content
        ORDER BY c.grade_level, c.title
        """,
        ids,
    )
    return cursor.fetchall()


def main():
    if not AIVEN_CONFIG["password"]:
        print("ERROR: Set AIVEN_PASSWORD (or MYSQLPASSWORD) env var before running.")
        return 1

    courses = make_blueprints()
    if len(courses) != 60:
        print(f"ERROR: expected 60 courses, got {len(courses)}")
        return 1

    rng = random.Random(getenv_int("COURSE_RANDOM_SEED", 20260403))

    print("Connecting to Aiven/MySQL...")
    try:
        conn = pymysql.connect(**AIVEN_CONFIG)
    except Exception as exc:
        print(f"Connection failed: {exc}")
        return 1

    processed = []
    try:
        cursor = conn.cursor()
        creator_id = resolve_creator_id(cursor)
        print(f"Using creator_id: {creator_id}")

        for i, course in enumerate(courses, 1):
            result = upsert_course(cursor, course, creator_id, rng)
            processed.append(result)
            print(f"[{i:02d}/60] Grade {result['grade']} | {result['action'].upper()} | ID {result['id']} | Q {result['questions']}")

        conn.commit()

        rows = verify(cursor, [x["id"] for x in processed])
        by_grade = defaultdict(lambda: {"courses": 0, "questions": 0, "placeholders": 0})
        for row in rows:
            g = int(row["grade_level"])
            by_grade[g]["courses"] += 1
            by_grade[g]["questions"] += int(row["q_count"])
            by_grade[g]["placeholders"] += int(row["p_count"])

        inserted = sum(1 for x in processed if x["action"] == "inserted")
        updated = sum(1 for x in processed if x["action"] == "updated")
        print("\n=== COMPLETE ===")
        print(f"Processed: {len(processed)} | Inserted: {inserted} | Updated: {updated}")
        print(f"Quiz rows inserted: {sum(x['questions'] for x in processed)}")

        for grade in range(1, 13):
            stats = by_grade[grade]
            print(f"Grade {grade:02d}: courses={stats['courses']} questions={stats['questions']} placeholders={stats['placeholders']}")

        ok_courses = all(by_grade[g]["courses"] == 5 for g in range(1, 13))
        ok_hydration = all(by_grade[g]["questions"] == by_grade[g]["placeholders"] for g in range(1, 13))
        if ok_courses and ok_hydration:
            print("Status: SUCCESS - 5 courses/grade and quiz hydration verified.")
        else:
            print("Status: WARNING - verification mismatch detected.")

    except Exception as exc:
        conn.rollback()
        print(f"ERROR during injection: {exc}")
        return 1
    finally:
        conn.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
