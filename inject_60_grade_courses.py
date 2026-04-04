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
import re
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
    "connect_timeout": getenv_int("MYSQL_CONNECT_TIMEOUT", 60),
    "cursorclass": pymysql.cursors.DictCursor,
    "db": os.getenv("MYSQL_DATABASE") or os.getenv("AIVEN_DB", "defaultdb"),
    "host": os.getenv("MYSQLHOST") or os.getenv("AIVEN_HOST", "veelearndb-asterloop-483e.i.aivencloud.com"),
    "password": os.getenv("MYSQLPASSWORD") or os.getenv("AIVEN_PASSWORD", ""),
    "port": getenv_int("MYSQLPORT", getenv_int("AIVEN_PORT", 26399)),
    "user": os.getenv("MYSQLUSER") or os.getenv("AIVEN_USER", "avnadmin"),
    "read_timeout": getenv_int("MYSQL_READ_TIMEOUT", 180),
    "write_timeout": getenv_int("MYSQL_WRITE_TIMEOUT", 180),
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
                "description": f"Deep Grade {grade} {strand} course focused strictly on the title topic, with mass-detail explanations, drawings, solved walkthroughs, PhET labs, and tiered student problem sets.",
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


def course_topic(course):
    parts = course["title"].split(" ", 2)
    return parts[2] if len(parts) >= 3 else course["title"]


def topic_keywords(topic):
    stop = {"and", "the", "of", "with", "to", "for", "in", "on", "studio", "intro", "advanced", "basics"}
    words = [w for w in re.findall(r"[A-Za-z]+", topic.lower()) if w not in stop]
    return words[:5] if words else ["core", "concepts"]


def unit_roadmap(course, alignment):
    topic = course_topic(course)
    kws = topic_keywords(topic)
    k1 = kws[0].title()
    k2 = kws[1].title() if len(kws) > 1 else "Reasoning"
    k3 = kws[2].title() if len(kws) > 2 else "Applications"
    sim_a, sim_b = course["sims"][0], course["sims"][1]
    return [
        (f"Unit 1: Foundations of {topic}", f"Build precise definitions, vocabulary, and baseline models for {k1}."),
        (f"Unit 2: Representations and Explanations", f"Translate ideas among words, diagrams, tables, and equations using {k2}."),
        (f"Unit 3: Guided Problem Solving", f"Work through multi-step solved examples, then explain each step in plain language."),
        (f"Unit 4: Simulation Lab Cycle", f"Use {sim_a} and {sim_b} to test claims, collect evidence, and validate models."),
        (f"Unit 5: Transfer and Capstone", f"Apply {k3} ideas in new contexts with assumptions, limitations, and reflection."),
    ]


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

# --- Deep course content overrides (kept below legacy builders so these definitions take precedence) ---

TITLE_KEYWORD_GUIDE = {
    "number sense": ["count and compare quantities accurately", "justify operations with concrete models"],
    "place value": ["decompose/recompose numbers by place", "explain regrouping with base-ten structure"],
    "fractions": ["treat fractions as numbers on a number line", "reason with part-whole and quotient views"],
    "equivalent fractions": ["generate equivalent forms with visual and symbolic methods", "justify equivalence transformations"],
    "decimals": ["connect decimal notation to place value", "convert among fraction-decimal-percent forms"],
    "ratios": ["model multiplicative comparison", "use unit rates for decisions"],
    "linear": ["interpret slope as rate of change", "interpret intercepts in context"],
    "algebra": ["simplify expressions with structure", "solve equations with justification"],
    "trigonometric": ["link triangle geometry to trig ratios", "apply periodic reasoning in models"],
    "precalculus": ["analyze function families", "compare function behavior across representations"],
    "calculus": ["connect derivatives to rate and optimization", "connect integrals to accumulation"],
    "motion": ["separate force and motion ideas", "interpret acceleration from data"],
    "friction": ["model contact forces and direction", "connect friction to energy dissipation"],
    "energy": ["track transfer and transformation pathways", "use conservation logic"],
    "gravity": ["relate mass-distance to force trends", "connect orbital behavior to force/velocity"],
    "orbit": ["model circular/elliptic motion assumptions", "test orbital claims with evidence"],
    "waves": ["relate frequency, wavelength, and speed", "predict interference outcomes"],
    "sound": ["connect wave properties to perceived sound", "analyze medium effects on propagation"],
    "light": ["model reflection/refraction with diagrams", "connect wavelength/frequency to observations"],
    "pressure": ["compute force-area relationships", "interpret pressure in fluids/gases"],
    "buoyancy": ["compare weight and displaced-fluid force", "predict float/sink with density"],
    "collisions": ["apply momentum conservation", "separate elastic/inelastic outcomes"],
    "electricity": ["differentiate voltage/current/resistance", "analyze circuits with Ohm and Kirchhoff ideas"],
    "magnetism": ["connect field direction to force effects", "model induction conceptually and quantitatively"],
    "quantum": ["interpret probability-based outcomes", "contrast classical and quantum predictions"],
    "matter": ["connect macroscopic properties to particles", "classify physical vs chemical change"],
    "solutions": ["reason with concentration and dilution", "explain dissolving at particle level"],
    "atomic": ["connect subatomic structure to element identity", "reason with isotope and ion models"],
    "molecules": ["link bonding/shape/polarity to properties", "represent molecules in multiple formats"],
    "acids": ["classify acids/bases using pH and proton transfer", "justify neutralization outcomes"],
    "bases": ["classify acids/bases using pH and proton transfer", "justify neutralization outcomes"],
    "stoichiometry": ["connect balanced equations to mole ratios", "track limiting reagent and yield"],
    "thermochemistry": ["reason with energy changes in reactions", "compare kinetic and equilibrium perspectives"],
    "equilibrium": ["predict shift direction qualitatively/quantitatively", "analyze dynamic balance mechanisms"],
    "spectroscopy": ["connect electron transitions to spectral lines", "interpret spectra as model evidence"],
    "organic": ["reason with structure-reactivity relationships", "trace mechanism logic with electron flow"],
    "living": ["connect structure to organism function", "map habitat-resource-survival links"],
    "weather": ["differentiate weather and climate evidence", "connect atmosphere patterns to life impacts"],
    "climate": ["differentiate weather and climate evidence", "connect atmosphere patterns to life impacts"],
    "cells": ["map organelle functions to cell behavior", "connect transport/signaling to homeostasis"],
    "ecosystems": ["analyze interactions across trophic levels", "predict feedback effects in populations"],
    "adaptation": ["explain trait-environment fit", "separate adaptation from short-term acclimation"],
    "genetics": ["connect genotype probabilities to phenotype patterns", "interpret inheritance data mechanistically"],
    "physiology": ["connect organ systems with regulation loops", "interpret body-system data in context"],
    "evolution": ["justify claims with multiple evidence sources", "model selection pressure outcomes"],
    "genomics": ["connect sequence variation to phenotype trends", "evaluate data limits and uncertainty"],
    "engineering": ["frame constraints and criteria explicitly", "iterate design-test-revise cycles"],
    "coding": ["trace algorithm steps with test cases", "debug using evidence instead of guessing"],
    "data": ["summarize patterns with fit-for-purpose visuals", "evaluate data quality and bias"],
    "financial literacy": ["model tradeoffs in spending/saving", "reason with rate/percent effects over time"],
    "statistical": ["interpret center/spread and sampling behavior", "separate descriptive from inferential claims"],
    "optimization": ["define objective and constraints", "compare feasible strategies with sensitivity checks"],
    "research": ["design valid methods and controls", "report limitations transparently"],
    "capstone": ["integrate models, data, and communication", "defend decisions under critique"],
}


def depth_text(grade):
    if grade <= 2:
        return "small explicit steps, concrete visuals, and repeated language scaffolds"
    if grade <= 5:
        return "visual-to-symbolic transitions with full reasoning shown at each step"
    if grade <= 8:
        return "formal explanation, evidence checks, and misconception correction cycles"
    if grade <= 10:
        return "symbolic fluency, model comparison, and argument-backed conclusions"
    return "rigorous abstraction, derivation-level reasoning, and capstone synthesis"


def derive_alignment(course):
    title = course["title"].lower()
    strand = course["strand"]
    grade = course["grade"]
    found = []
    for key, points in TITLE_KEYWORD_GUIDE.items():
        if key in title:
            found.extend(points)
    defaults = {
        "math": ["translate among visual, verbal, tabular, and symbolic representations", "verify reasonableness before finalizing answers"],
        "physics": ["draw system diagrams before equations", "check units and sign conventions at every step"],
        "chemistry": ["track conservation of atoms and charge", "show all unit conversions and assumptions"],
        "bioearth": ["connect mechanism to evidence explicitly", "differentiate observation from inference"],
        "applied": ["make constraints explicit before solving", "justify tradeoffs using data and assumptions"],
    }
    for item in defaults[strand]:
        if item not in found:
            found.append(item)
    fallback = [
        "explain each step in plain language",
        "show work with a visual or table before symbolic compression",
        "verify final answers with reasonableness checks",
        "connect results back to real-world meaning",
    ]
    for item in fallback:
        if len(found) >= 4:
            break
        if item not in found:
            found.append(item)
    scope = found[:4]

    if grade <= 4:
        not_yet = ["formal proof frameworks", "high-abstraction symbolic shortcuts without meaning", "multi-variable optimization"]
    elif grade <= 8:
        not_yet = ["graduate-level derivations", "research-only modeling assumptions", "advanced proof-only treatments"]
    else:
        not_yet = ["doctoral-level specialization", "frontier research methods", "unintroduced notation outside this title scope"]

    return {"scope": scope, "not_yet": not_yet}


def render_sim_html(sim_names, title):
    parts = []
    for sim_name in sim_names:
        parts.append(
            "<div style=\"margin:18px 0; background:#ffffff; border:1px solid #dbe5ef; border-radius:12px; padding:14px;\">"
            f"<h4 style=\"margin:0 0 8px 0;\">PhET Lab: {sim_name}</h4>"
            f"<iframe src=\"{SIMS[sim_name]}\" width=\"100%\" height=\"560\" frameborder=\"0\" "
            "style=\"border:1px solid #d1d5db; border-radius:8px; background:#f8fafc;\"></iframe>"
            f"<p><strong>Lab focus:</strong> Investigate <em>{title}</em> with 3+ trials. Record variables, produce one graph/table, and write a CER paragraph.</p>"
            "<p><strong>Required writeup:</strong> hypothesis, method, data, interpretation, and one limitation.</p>"
            "</div>"
        )
    return "\n".join(parts)


def build_diagram_html(course):
    strand = course["strand"]
    if strand == "math":
        return (
            "<h3>Course Drawings</h3>"
            "<svg viewBox=\"0 0 760 180\" width=\"100%\" height=\"180\" style=\"border:1px solid #dbe5ef; border-radius:10px; background:#fff;\">"
            "<line x1=\"40\" y1=\"130\" x2=\"720\" y2=\"130\" stroke=\"#64748b\" stroke-width=\"2\"/>"
            "<circle cx=\"120\" cy=\"130\" r=\"7\" fill=\"#2563eb\"/><circle cx=\"300\" cy=\"100\" r=\"7\" fill=\"#0ea5e9\"/>"
            "<circle cx=\"470\" cy=\"75\" r=\"7\" fill=\"#16a34a\"/><circle cx=\"630\" cy=\"52\" r=\"7\" fill=\"#f59e0b\"/>"
            "<polyline points=\"120,130 300,100 470,75 630,52\" fill=\"none\" stroke=\"#1d4ed8\" stroke-width=\"3\"/>"
            "<text x=\"40\" y=\"28\" font-size=\"15\">Read this as representation -> pattern -> equation. Explain what each point means.</text>"
            "</svg>"
        )
    if strand == "physics":
        return (
            "<h3>Course Drawings</h3>"
            "<svg viewBox=\"0 0 760 220\" width=\"100%\" height=\"220\" style=\"border:1px solid #dbe5ef; border-radius:10px; background:#fff;\">"
            "<rect x=\"280\" y=\"110\" width=\"120\" height=\"60\" fill=\"#e2e8f0\" stroke=\"#64748b\"/>"
            "<line x1=\"170\" y1=\"140\" x2=\"280\" y2=\"140\" stroke=\"#ef4444\" stroke-width=\"4\"/>"
            "<line x1=\"400\" y1=\"140\" x2=\"520\" y2=\"140\" stroke=\"#22c55e\" stroke-width=\"4\"/>"
            "<line x1=\"340\" y1=\"110\" x2=\"340\" y2=\"42\" stroke=\"#0ea5e9\" stroke-width=\"4\"/>"
            "<line x1=\"340\" y1=\"170\" x2=\"340\" y2=\"208\" stroke=\"#111827\" stroke-width=\"4\"/>"
            "<text x=\"40\" y=\"28\" font-size=\"15\">Always sketch forces/system first. Then write equations using this picture.</text>"
            "</svg>"
        )
    if strand == "chemistry":
        return (
            "<h3>Course Drawings</h3>"
            "<svg viewBox=\"0 0 760 200\" width=\"100%\" height=\"200\" style=\"border:1px solid #dbe5ef; border-radius:10px; background:#fff;\">"
            "<rect x=\"30\" y=\"35\" width=\"290\" height=\"140\" fill=\"#f8fafc\" stroke=\"#94a3b8\"/>"
            "<rect x=\"440\" y=\"35\" width=\"290\" height=\"140\" fill=\"#f8fafc\" stroke=\"#94a3b8\"/>"
            "<text x=\"118\" y=\"58\" font-size=\"14\">Reactants</text><text x=\"538\" y=\"58\" font-size=\"14\">Products</text>"
            "<circle cx=\"100\" cy=\"100\" r=\"14\" fill=\"#38bdf8\"/><circle cx=\"136\" cy=\"100\" r=\"14\" fill=\"#34d399\"/>"
            "<circle cx=\"520\" cy=\"105\" r=\"14\" fill=\"#38bdf8\"/><circle cx=\"556\" cy=\"105\" r=\"14\" fill=\"#34d399\"/><circle cx=\"592\" cy=\"105\" r=\"14\" fill=\"#f97316\"/>"
            "<text x=\"40\" y=\"28\" font-size=\"15\">Count particles before/after. Conservation must hold every time.</text>"
            "</svg>"
        )
    if strand == "bioearth":
        return (
            "<h3>Course Drawings</h3>"
            "<svg viewBox=\"0 0 760 210\" width=\"100%\" height=\"210\" style=\"border:1px solid #dbe5ef; border-radius:10px; background:#fff;\">"
            "<rect x=\"70\" y=\"62\" width=\"150\" height=\"55\" rx=\"8\" fill=\"#dcfce7\" stroke=\"#16a34a\"/>"
            "<rect x=\"300\" y=\"42\" width=\"170\" height=\"55\" rx=\"8\" fill=\"#e0f2fe\" stroke=\"#0284c7\"/>"
            "<rect x=\"300\" y=\"132\" width=\"170\" height=\"55\" rx=\"8\" fill=\"#fef3c7\" stroke=\"#f59e0b\"/>"
            "<rect x=\"560\" y=\"87\" width=\"130\" height=\"55\" rx=\"8\" fill=\"#ede9fe\" stroke=\"#7c3aed\"/>"
            "<text x=\"94\" y=\"95\" font-size=\"14\">Environment</text><text x=\"348\" y=\"75\" font-size=\"14\">Organism</text>"
            "<text x=\"344\" y=\"165\" font-size=\"14\">Population</text><text x=\"594\" y=\"120\" font-size=\"14\">Outcome</text>"
            "<text x=\"34\" y=\"28\" font-size=\"15\">Use arrows to explain mechanism, not just correlation.</text>"
            "</svg>"
        )
    return (
        "<h3>Course Drawings</h3>"
        "<svg viewBox=\"0 0 760 180\" width=\"100%\" height=\"180\" style=\"border:1px solid #dbe5ef; border-radius:10px; background:#fff;\">"
        "<rect x=\"40\" y=\"68\" width=\"120\" height=\"48\" rx=\"8\" fill=\"#e0f2fe\" stroke=\"#0284c7\"/>"
        "<rect x=\"200\" y=\"68\" width=\"120\" height=\"48\" rx=\"8\" fill=\"#dcfce7\" stroke=\"#16a34a\"/>"
        "<rect x=\"360\" y=\"68\" width=\"120\" height=\"48\" rx=\"8\" fill=\"#fef3c7\" stroke=\"#f59e0b\"/>"
        "<rect x=\"520\" y=\"68\" width=\"120\" height=\"48\" rx=\"8\" fill=\"#ede9fe\" stroke=\"#7c3aed\"/>"
        "<text x=\"72\" y=\"97\" font-size=\"14\">Problem</text><text x=\"242\" y=\"97\" font-size=\"14\">Data</text>"
        "<text x=\"400\" y=\"97\" font-size=\"14\">Model</text><text x=\"554\" y=\"97\" font-size=\"14\">Decision</text>"
        "<text x=\"40\" y=\"28\" font-size=\"15\">Keep every decision traceable to data and assumptions.</text>"
        "</svg>"
    )


def solved_problem_bank(course):
    grade = course["grade"]
    strand = course["strand"]
    if strand == "physics":
        m = grade + 2
        f = 14 + 3 * grade
        v = grade + 4
        return [
            {"problem": f"Find acceleration for force {f} N on mass {m} kg.", "steps": ["Use F=ma.", "Rearrange a=F/m.", f"Substitute a={f}/{m}.", f"Compute a={f/m:.2f} m/s^2.", "Interpret as velocity change per second."], "answer": f"{f/m:.2f} m/s^2"},
            {"problem": f"Find kinetic energy for mass {m} kg at speed {v} m/s.", "steps": ["Use KE=1/2mv^2.", f"Compute v^2={v*v}.", f"KE=0.5*{m}*{v*v}.", "Attach joule unit.", "Reasonableness check with estimate."], "answer": f"{0.5*m*v*v:.2f} J"},
            {"problem": "Series circuit has V=12 V and R=4 ohms. Find current.", "steps": ["Use V=IR.", "I=V/R.", "I=12/4.", "I=3 A.", "Check by VI power relation."], "answer": "3 A"},
            {"problem": "Wave with f=5 Hz and wavelength 0.8 m. Find speed.", "steps": ["v=f*lambda.", "v=5*0.8.", "v=4.", "Use m/s.", "Interpret propagation meaning."], "answer": "4 m/s"},
            {"problem": "Pressure from F=90 N on A=0.30 m^2.", "steps": ["P=F/A.", "P=90/0.30.", "P=300.", "Use pascal unit.", "Explain how area affects pressure."], "answer": "300 Pa"},
            {"problem": "Momentum p=30 kg*m/s, mass=5 kg. Find velocity.", "steps": ["p=mv.", "v=p/m.", "v=30/5.", "v=6.", "Check p with back-substitution."], "answer": "6 m/s"},
        ]
    return None


def generic_solved_bank(course):
    g = course["grade"]
    strand = course["strand"]
    if strand == "math":
        return [
            {"problem": "Compute 3/4 + 5/8.", "steps": ["Common denominator 8.", "3/4=6/8.", "6/8+5/8=11/8.", "Convert to mixed number.", "Check with decimal estimate."], "answer": "1 3/8"},
            {"problem": "Solve 3x+7=31.", "steps": ["Subtract 7 from both sides.", "3x=24.", "Divide by 3.", "x=8.", "Substitute to verify."], "answer": "x=8"},
            {"problem": "Find unit rate for 42 km in 3.5 h.", "steps": ["Unit rate=distance/time.", "42/3.5=12.", "Units km/h.", "Interpret meaning.", "Check by multiplying back."], "answer": "12 km/h"},
            {"problem": "Solve x^2-7x+10=0.", "steps": ["Factor into (x-5)(x-2).", "Set each factor zero.", "x=5 or x=2.", "Substitute to verify.", "Report complete set."], "answer": "x=2,5"},
            {"problem": "Differentiate f(x)=3x^3-5x^2+2x-9.", "steps": ["Power rule term-by-term.", "Derivative terms: 9x^2, -10x, +2, 0.", "Combine.", "State final form.", "Quick coefficient sanity check."], "answer": "9x^2-10x+2"},
            {"problem": "Distance between (2,-1) and (8,7).", "steps": ["dx=6, dy=8.", "Use sqrt(dx^2+dy^2).", "sqrt(36+64)=sqrt(100).", "Distance=10.", "Interpret unit context."], "answer": "10"},
        ]
    if strand == "chemistry":
        n = 0.7 + 0.1 * g
        v = 1.1 + 0.2 * g
        return [
            {"problem": f"Molarity of {n:.2f} mol in {v:.2f} L.", "steps": ["M=n/V.", f"M={n:.2f}/{v:.2f}.", "Compute quotient.", "Attach mol/L.", "Check magnitude reasonableness."], "answer": f"{n/v:.3f} M"},
            {"problem": "Balance __H2 + __O2 -> __H2O.", "steps": ["Count atoms both sides.", "Set 2 before H2O.", "Set 2 before H2.", "Recount atoms.", "State balanced equation."], "answer": "2H2 + O2 -> 2H2O"},
            {"problem": "Classify pH=3.2 solution.", "steps": ["pH<7 means acidic.", "3.2 is below 7.", "Classify as acidic.", "Connect to proton concentration.", "State confidently."], "answer": "Acidic"},
            {"problem": "Dilution: 2.0 M stock to make 0.50 L of 0.40 M. Find stock volume.", "steps": ["M1V1=M2V2.", "V1=(M2V2)/M1.", "V1=(0.40*0.50)/2.0.", "V1=0.10 L.", "Convert to 100 mL if needed."], "answer": "0.10 L"},
            {"problem": "Boyle law: P1=1 atm, V1=2 L, V2=1 L. Find P2.", "steps": ["P1V1=P2V2.", "P2=(P1V1)/V2.", "P2=(1*2)/1.", "P2=2 atm.", "Explain inverse P-V relation."], "answer": "2 atm"},
            {"problem": "Average atomic mass: 75% of 20 amu, 25% of 22 amu.", "steps": ["Weighted average sum.", "0.75*20=15.", "0.25*22=5.5.", "Total 20.5 amu.", "Check weights sum to 1."], "answer": "20.5 amu"},
        ]
    if strand == "bioearth":
        start = 60 + 6 * g
        return [
            {"problem": f"Population {start} grows by 12% for one year. Next-year estimate?", "steps": ["Growth factor 1.12.", f"{start}*1.12.", "Compute and round by context.", "State assumption of constant rate.", "Interpret biological plausibility."], "answer": f"{int(round(start*1.12))} (approx)"},
            {"problem": "Cross Bb x Bb. Probability of bb?", "steps": ["Punnett square outcomes.", "Count bb outcomes.", "1 out of 4.", "Convert to percent.", "State probability."], "answer": "25%"},
            {"problem": "Concentration gradient from 18 to 6 units.", "steps": ["Subtract low from high.", "18-6=12.", "Direction high to low.", "Interpret diffusion tendency.", "Report with units."], "answer": "12 units"},
            {"problem": "Energy transfer: 1000 producer units, 10% to herbivore. Herbivore energy?", "steps": ["Multiply by 0.10.", "1000*0.10=100.", "State trophic transfer meaning.", "Connect to ecological efficiency.", "Check unit consistency."], "answer": "100 units"},
            {"problem": "CO2 rises 410 ppm to 451 ppm. Percent increase?", "steps": ["Change 41 ppm.", "41/410*100.", "Compute about 10%.", "State approximate nature.", "Interpret climate relevance."], "answer": "about 10%"},
            {"problem": "Conduction speed 40 m/s across 2 m path. Signal travel time?", "steps": ["t=d/v.", "2/40=0.05 s.", "Convert to 50 ms.", "Interpret response timing.", "Check units."], "answer": "0.05 s"},
        ]
    # applied default
    vals = [g + 3, g + 5, g + 8, g + 11, g + 13]
    avg = sum(vals) / len(vals)
    return [
        {"problem": f"Mean of {vals}.", "steps": [f"Sum={sum(vals)}.", f"Count={len(vals)}.", f"Mean={avg:.2f}.", "Interpret center.", "Check with deviations."], "answer": f"{avg:.2f}"},
        {"problem": "Budget $240, item costs $18. Max items?", "steps": ["Use integer division.", "240/18=13 remainder.", "Max whole=13.", "Check 13*18<=240.", "Report leftover."], "answer": "13"},
        {"problem": "Slope through (1,4) and (5,20).", "steps": ["(20-4)/(5-1).", "16/4=4.", "State slope.", "Interpret unit change.", "Check with line equation."], "answer": "4"},
        {"problem": "Weighted score: 0.4*7 + 0.6*9.", "steps": ["Multiply each weighted term.", "2.8 and 5.4.", "Add to 8.2.", "Interpret rank meaning.", "Compare to alternatives."], "answer": "8.2"},
        {"problem": "48 successes out of 120 trials. Empirical probability?", "steps": ["success/trials.", "48/120=0.4.", "Convert to 40%.", "Discuss uncertainty.", "Suggest larger sample."], "answer": "0.4"},
        {"problem": "Regression y=2.5x+6 at x=8.", "steps": ["Substitute x.", "2.5*8=20.", "20+6=26.", "Check domain validity.", "Interpret prediction."], "answer": "26"},
    ]


def practice_sets(course, alignment):
    scope = alignment["scope"]
    basic = [
        f"Define '{scope[0]}' in plain words and add one drawing/model.",
        f"Solve one on-topic problem using '{scope[1]}' with every step justified.",
        f"Create a table or diagram for '{scope[2]}' and explain how to read it.",
        f"Re-solve a worked example using a second strategy for '{scope[3]}'.",
        "Write a misconception and then correct it using evidence from this course.",
        "Build a short checklist to avoid the most common errors.",
    ]
    intermediate = [
        f"Combine two ideas from {course['title']} into one multi-step problem and solve it fully.",
        "Given a partly wrong solution, locate the first wrong step and repair the full path.",
        "Use a small dataset (6+ values) to support a claim and include one graph sketch.",
        "Translate verbal context -> model/equation -> solution -> interpretation.",
        "Compare two valid strategies and explain when each is better.",
        "Change one input and run a sensitivity explanation of output changes.",
    ]
    challenge = [
        "Design a transfer problem that combines this course with one earlier course, then solve it.",
        "Write a CER argument with one computed value and one visual model.",
        "Create a peer-teaching explanation that skips no intermediate reasoning.",
        "Invent a realistic bad-assumption scenario, then repair the assumption and solution.",
        "Produce one exam-quality item with full rubric and ideal solution.",
        "Write a capstone memo: assumptions, model, answer, limitation, and extension.",
    ]
    return {"basic": basic, "intermediate": intermediate, "challenge": challenge}


def render_solved_html(problems):
    out = []
    for i, p in enumerate(problems, 1):
        steps = "".join([f"<li>{s}</li>" for s in p["steps"]])
        out.append(
            "<div style=\"background:#ffffff; border:1px solid #dbe5ef; border-radius:12px; padding:16px; margin:14px 0;\">"
            f"<h4 style=\"margin-top:0;\">Solved Walkthrough {i}</h4>"
            f"<p><strong>Problem:</strong> {p['problem']}</p>"
            "<p><strong>Reasoning steps:</strong></p>"
            f"<ol>{steps}</ol>"
            f"<p><strong>Final answer:</strong> {p['answer']}</p>"
            "<p><strong>Check:</strong> verify units, logic, and context fit.</p>"
            "</div>"
        )
    return "".join(out)


def render_practice_html(sets):
    b = "".join([f"<li>{x}</li>" for x in sets["basic"]])
    m = "".join([f"<li>{x}</li>" for x in sets["intermediate"]])
    c = "".join([f"<li>{x}</li>" for x in sets["challenge"]])
    return (
        "<h3>Tier A - Foundation Practice</h3><ol>" + b + "</ol>"
        "<h3>Tier B - Intermediate Integration</h3><ol>" + m + "</ol>"
        "<h3>Tier C - Challenge and Transfer</h3><ol>" + c + "</ol>"
    )


def build_content(course):
    grade = course["grade"]
    title = course["title"]
    alignment = derive_alignment(course)
    solved = solved_problem_bank(course) or generic_solved_bank(course)
    practice = practice_sets(course, alignment)

    scope_html = "".join([f"<li>{x}</li>" for x in alignment["scope"]])
    out_scope_html = "".join([f"<li>{x}</li>" for x in alignment["not_yet"]])
    focus_html = "".join([
        f"<li><strong>{f.title()}:</strong> show reasoning and evidence, not final answer only.</li>"
        for f in course["focus_points"]
    ])

    explanation_cards = []
    for i, concept in enumerate(alignment["scope"], 1):
        confusion = alignment["not_yet"][i % len(alignment["not_yet"])]
        explanation_cards.append(
            "<div style=\"background:#ffffff; border:1px solid #dbe5ef; border-radius:12px; padding:16px; margin:14px 0;\">"
            f"<h4 style=\"margin-top:0;\">Concept {i}: {concept}</h4>"
            "<p><strong>Plain explanation:</strong> We unpack this concept in small language first so learners understand the idea before formulas. "
            "Students are expected to retell the meaning in their own words and map each step to a visual representation.</p>"
            "<p><strong>Technical explanation:</strong> We then formalize the same idea with explicit symbols, assumptions, and constraints. "
            "Every step is justified so students can see exactly why a method works.</p>"
            "<p><strong>How to show work:</strong> givens -> model/equation -> step-by-step operations -> unit/context check -> conclusion sentence.</p>"
            f"<p><strong>Misconception watch:</strong> Do not confuse this with <em>{confusion}</em>. "
            "This course keeps the title focus narrow and explicit to avoid topic drift.</p>"
            "</div>"
        )

    roadmap = unit_roadmap(course, alignment)
    roadmap_html = "".join([
        f"<li><strong>{title}:</strong> {desc}</li>"
        for title, desc in roadmap
    ])

    return (
        "<div style=\"background:#f8fafc; color:#0f172a; padding:8px;\">"
        f"<h1 style=\"color:#0f172a;\">{title}</h1>"
        f"<p><strong>Grade:</strong> {grade}</p>"
        f"<p><strong>Course Promise:</strong> {course['description']}</p>"
        f"<p><strong>Depth Standard:</strong> This course uses {depth_text(grade)}.</p>"
        "<hr>"
        "<h2>Module 1: Exact Title Scope (What We Teach)</h2>"
        f"<p>This course stays tightly focused on <strong>{title}</strong> and does not wander into unrelated topics.</p>"
        "<h3>In-Scope Targets</h3>"
        f"<ul>{scope_html}</ul>"
        "<h3>Out-of-Scope (Not Yet)</h3>"
        f"<ul>{out_scope_html}</ul>"
        "<h3>Reasoning Expectations</h3>"
        f"<ul>{focus_html}</ul>"
        "<h2>Module 1B: Course-Specific Unit Roadmap</h2>"
        "<p>This roadmap is customized to this exact course title, not a generic strand template.</p>"
        f"<ul>{roadmap_html}</ul>"
        "<h2>Module 2: Mass-Detail Explanations</h2>"
        f"{''.join(explanation_cards)}"
        "<h2>Module 3: Drawings and Visual Models</h2>"
        "<p>Students should refer to these visuals while solving problems.</p>"
        f"{build_diagram_html(course)}"
        "<h2>Module 4: Fully Solved Problems (No Step Skipped)</h2>"
        "<p>These walkthroughs are intentionally long and explicit so beginners can follow every move.</p>"
        f"{render_solved_html(solved)}"
        "<h2>Module 5: Interactive PhET Lab Studio</h2>"
        f"{render_sim_html(course['sims'], title)}"
        "<h2>Module 6: Student Problem Sets</h2>"
        "<p>Complete all tiers. Tier C is designed for transfer and deep mastery.</p>"
        f"{render_practice_html(practice)}"
        "<h2>Module 7: Error Analysis Clinic</h2>"
        "<ol>"
        "<li>Take one solved problem and intentionally insert a common error.</li>"
        "<li>Label the first wrong step and explain why it is wrong.</li>"
        "<li>Repair the full solution path with corrected reasoning.</li>"
        "<li>Write a short note: how to prevent this error in future work.</li>"
        "</ol>"
        "<h2>Module 8: Mastery Exit Task</h2>"
        "<p>Create one real-world, title-aligned case: assumptions, model, complete solution, visual drawing, and reflection on limitations.</p>"
        "</div>"
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
    title = course["title"]
    topic = course_topic(course)
    focus = course["focus_points"]
    alignment = derive_alignment(course)
    scope = alignment["scope"]
    seed = sum(ord(ch) for ch in title) + grade * 97 + len(topic) * 13
    rr = random.Random(seed)

    out = []
    def add(text, correct, wrongs, explanation):
        out.append(make_question(text, correct, wrongs, explanation, len(out) + 1))

    add(
        f"In {title}, what is the highest-priority target?",
        scope[0],
        [scope[1], "Unrelated topic expansion", "Skipping foundations for random advanced content"],
        "This course is intentionally title-aligned and starts with its core target."
    )
    add(
        f"In {title}, which statement best reflects '{focus[0]}'?",
        "Use evidence-backed reasoning, not answer-only responses.",
        ["Memorize and copy final answers only.", "Skip model selection and jump to arithmetic.", "Avoid explaining assumptions."],
        "Deep learning requires visible reasoning, evidence, and assumptions."
    )

    if strand == "math":
        if grade <= 4:
            a = rr.randint(20 + grade, 40 + grade * 2)
            b = rr.randint(10 + grade, 35 + grade * 2)
            c = rr.randint(30 + grade, 70 + grade * 2)
            d = rr.randint(8 + grade, 25 + grade)
            add(f"{title}: Compute {a} + {b}.", str(a + b), [str(a + b + 1), str(a + b - 1), str(a + b + 2)], "Use place-value decomposition and verify with estimation.")
            add(f"{title}: Solve subtraction {c} - {d}.", str(c - d), [str(c - d + 1), str(c - d - 2), str(c - d + 3)], "Regroup carefully and check by inverse addition.")
            add(f"In {title}, which representation should come before symbolic shortcuts?", "A visual/table model of the situation", ["A random formula guess", "Only the final numeric answer", "No representation"], "Visual structure reduces errors and supports understanding.")
        elif grade <= 8:
            num = rr.randint(8, 21)
            den = rr.randint(3, 9)
            add(f"{title}: Convert {num}/{den} to decimal (rounded to 2 decimals).", f"{num/den:.2f}", [f"{num/den + 0.1:.2f}", f"{num/den - 0.1:.2f}", f"{num/den + 0.2:.2f}"], "Fraction-decimal conversion should preserve value.")
            x = rr.randint(2, 7)
            rhs = rr.randint(18, 42)
            lhs_c = rr.randint(4, 12)
            add(f"{title}: Solve {x}n + {lhs_c} = {rhs}.", f"n = {(rhs-lhs_c)/x:.2f}" if (rhs - lhs_c) % x else f"n = {(rhs-lhs_c)//x}", [f"n = {(rhs-lhs_c)/x + 1:.2f}", f"n = {(rhs-lhs_c)/x - 1:.2f}", "n = 0"], "Isolate the variable with inverse operations.")
            add(f"For {title}, in proportional form y = kx, what does k represent?", "Constant of proportionality (unit rate)", ["Y-intercept", "Random offset", "Domain"], "k is the multiplicative scale factor.")
        else:
            m = rr.randint(2, 8)
            b = rr.randint(-6, 8)
            x = rr.randint(2, 6)
            add(f"{title}: For y = {m}x + ({b}), find y when x={x}.", str(m * x + b), [str(m * x + b + 2), str(m * x + b - 3), str(m * x + b + 5)], "Substitute then simplify carefully.")
            r1 = rr.randint(2, 8)
            r2 = rr.randint(1, 6)
            add(f"{title}: Roots are x={r1} and x={r2}. Which quadratic matches?", f"(x-{r1})(x-{r2}) = 0", [f"(x+{r1})(x-{r2}) = 0", f"(x-{r1})(x+{r2}) = 0", f"(x+{r1})(x+{r2}) = 0"], "Factor form encodes roots directly.")
            add(f"Before finalizing an answer in {title}, what must be checked?", "Domain, units/context, and reasonableness", ["Only algebraic formatting", "Only calculator output", "Nothing if the number looks large"], "Verification protects against hidden model errors.")

    elif strand == "physics":
        m = rr.randint(grade + 1, grade + 5)
        force = rr.randint(18 + grade, 55 + grade * 2)
        v = rr.randint(grade + 3, grade + 8)
        h = rr.randint(grade + 2, grade + 9)
        add(f"{title}: If F={force} N and m={m} kg, acceleration is:", f"{force/m:.2f} m/s^2", [f"{force/m + 0.8:.2f} m/s^2", f"{max(force/m - 0.8, 0):.2f} m/s^2", f"{(2*force)/m:.2f} m/s^2"], "Apply a=F/m with consistent units.")
        add(f"{title}: Kinetic energy for m={m} kg, v={v} m/s is:", f"{0.5*m*v*v:.2f} J", [f"{0.5*m*v*v + 8:.2f} J", f"{max(0.5*m*v*v - 8, 0):.2f} J", f"{m*v:.2f} J"], "Use KE = 1/2mv^2, not momentum.")
        add(f"{title}: Potential energy at height {h} m for mass {m} kg is:", f"{m*9.8*h:.2f} J", [f"{m*9.8*h + 10:.2f} J", f"{m*9.8*h/2:.2f} J", f"{m*9.8*(h+2):.2f} J"], "Use PE = mgh and keep unit J.")

    elif strand == "chemistry":
        moles = rr.uniform(0.8, 2.8)
        vol = rr.uniform(0.6, 2.4)
        ph = rr.uniform(2.2, 11.4)
        add(f"{title}: Molarity of {moles:.2f} mol in {vol:.2f} L is:", f"{moles/vol:.2f} M", [f"{moles/vol + 0.30:.2f} M", f"{max(moles/vol - 0.25, 0):.2f} M", f"{(moles*vol):.2f} M"], "Use M=n/V and preserve units.")
        acid_base = "Acidic" if ph < 7 else ("Basic" if ph > 7 else "Neutral")
        add(f"{title}: A sample has pH {ph:.1f}. Classification?", acid_base, ["Acidic" if acid_base != "Acidic" else "Basic", "Neutral" if acid_base != "Neutral" else "Basic", "Cannot classify from pH"], "pH<7 acid, pH=7 neutral, pH>7 base.")
        add(f"In {title}, why must equations be balanced before stoichiometric calculations?", "To conserve atoms (and charge when relevant)", ["To force products to appear", "To make numbers larger", "Because reactants disappear"], "Conservation is non-negotiable in chemical models.")

    elif strand == "bioearth":
        start = rr.randint(60 + grade * 3, 130 + grade * 5)
        growth = rr.randint(6, 18)
        next_pop = round(start * (1 + growth/100))
        add(f"{title}: Population {start} grows by {growth}%. Next year estimate?", str(next_pop), [str(next_pop + 5), str(max(next_pop - 6, 0)), str(start + growth)], "Use multiplicative growth factor 1+r.")
        add(f"In {title}, for genotype cross Bb x Bb, probability of bb is:", "25%", ["0%", "50%", "75%"], "Punnett square yields 1 of 4 bb outcomes.")
        add(f"For {title}, a strong bio/earth claim should include:", "Mechanism + measured evidence + interpretation", ["Opinion only", "One unlabeled image", "Conclusion without data"], "Scientific arguments require mechanism and evidence.")

    else:
        vals = [rr.randint(8, 30) for _ in range(5)]
        mean = sum(vals)/len(vals)
        add(f"{title}: Mean of dataset {vals} is:", f"{mean:.2f}", [f"{mean+1:.2f}", f"{max(mean-1,0):.2f}", f"{sum(vals):.2f}"], "Mean = total/count, then interpret in context.")
        cost = rr.randint(9, 24)
        budget = rr.randint(140, 320)
        add(f"{title}: Budget is ${budget}, each item costs ${cost}. Max whole items?", str(budget // cost), [str(budget // cost + 1), str(max(budget // cost - 1, 0)), str(round(budget / cost, 2))], "Use integer division when only whole items are feasible.")
        add(f"In {title}, what makes an applied model trustworthy?", "Explicit assumptions, tested fit, and interpretable output", ["Hidden assumptions and no validation", "Random parameter tuning only", "Ignoring uncertainty"], "Trustworthy models are transparent and validated.")

    solved = solved_problem_bank(course) or generic_solved_bank(course)
    solved_ans_1 = str(solved[0]["answer"])
    solved_ans_2 = str(solved[1]["answer"])
    add(f"{title}: In Solved Walkthrough 1, the final result is:", solved_ans_1, [solved_ans_2, "Not enough information", "The result is intentionally omitted"], "This checks whether students can trace full solutions, not just skim.")
    add(f"{title}: In Solved Walkthrough 2, the final result is:", solved_ans_2, [solved_ans_1, "No final result appears", "Answer cannot be determined"], "Reviewing complete solutions helps transfer to new problems.")

    add(
        f"In {title}, which simulations are embedded?",
        f"{course['sims'][0]} and {course['sims'][1]}",
        [f"{course['sims'][0]} and Arithmetic", "No simulations are used", "Only static diagrams"],
        "Each course uses two PhET sims tied to its title scope."
    )
    add(
        f"For {topic}, CER means:",
        "Claim, Evidence, Reasoning",
        ["Claim, Example, Revision", "Calculate, Estimate, Report", "Compare, Evaluate, Repeat"],
        "CER is the standard for evidence-backed explanations in this course."
    )
    add(
        f"When using {course['sims'][0]} in {title}, why run multiple trials?",
        "To identify stable patterns and reduce one-off noise",
        ["One trial is always enough", "To avoid recording data", "To force a preferred result"],
        "Replication improves reliability and strengthens conclusions."
    )
    add(
        f"In {title}, transfer of learning means:",
        f"Applying '{scope[0]}' correctly in a new context",
        ["Memorizing only one worked example", "Ignoring assumptions", "Skipping model setup"],
        "Mastery appears when students can adapt ideas beyond the original example."
    )
    add(
        f"For the {title} capstone, required evidence includes:",
        "Model, data, full reasoning path, and limitation analysis",
        ["Title and one final number", "Only equations without explanation", "One paragraph with no evidence"],
        "Capstones evaluate complete thinking, not answer snapshots."
    )
    add(
        f"Before submitting work in {title}, students should always:",
        "Check assumptions, units, and reasonableness",
        ["Skip checks to save time", "Only bold the final answer", "Delete intermediate work"],
        "Quality control catches hidden errors."
    )

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
        try:
            conn.rollback()
        except Exception:
            pass
        print(f"ERROR during injection: {exc}")
        return 1
    finally:
        conn.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
