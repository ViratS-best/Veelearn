# University-tier curriculum index: 65 modules (13 per strand × 5 strands).
# Titles are first-year / sophomore college level — NOT elementary grade bands.
# Injected with prefix UNIV 2026 — (additive; does not delete CC+ or K–12 rows).

STRANDS_ORDER = ("math", "physics", "chemistry", "biology", "computing")

# (strand, short_title) — full DB title becomes: UNIV 2026 — {Strand} — {short_title}
UNIV_MODULES: list[tuple[str, str]] = [
    # Mathematics (13)
    ("math", "Limits, Continuity, and Rigorous Definitions"),
    ("math", "Differentiation: Rules, Linearization, and Related Rates"),
    ("math", "Mean Value Theorem and Curve Sketching with Calculus"),
    ("math", "Integration, Riemann Sums, and the Fundamental Theorem"),
    ("math", "Techniques of Integration and Improper Integrals"),
    ("math", "Sequences, Series, and Convergence Tests"),
    ("math", "Taylor Series and Power-Series Representations"),
    ("math", "Vectors, Lines, and Planes in ℝ³"),
    ("math", "Matrix Algebra and Linear Systems"),
    ("math", "Vector Spaces, Bases, and Linear Transformations"),
    ("math", "Eigenvalues, Diagonalization, and Dynamical Systems"),
    ("math", "First- and Second-Order Ordinary Differential Equations"),
    ("math", "Probability, Expectation, and Introductory Inference"),
    # Physics (13)
    ("physics", "Vectors, Kinematics, and Frames of Reference"),
    ("physics", "Newton's Laws, Free-Body Diagrams, and Friction"),
    ("physics", "Work, Kinetic Energy, and Conservative Forces"),
    ("physics", "Momentum, Impulse, and Collision Analysis"),
    ("physics", "Rotation, Torque, and Angular Momentum"),
    ("physics", "Gravitation, Kepler Problems, and Orbital Energy"),
    ("physics", "Oscillations, Damping, and Resonance"),
    ("physics", "Traveling Waves, Standing Waves, and Superposition"),
    ("physics", "Electric Fields, Gauss's Law, and Potential"),
    ("physics", "Capacitance, Current, and DC Circuit Models"),
    ("physics", "Magnetic Fields, Forces, and Faraday Induction"),
    ("physics", "Geometric Optics: Lenses, Mirrors, and Instruments"),
    ("physics", "Photons, Quantization, and Introductory Quantum Models"),
    # Chemistry (13)
    ("chemistry", "Quantum Numbers, Orbitals, and Periodic Trends"),
    ("chemistry", "Lewis Structures, VSEPR, and Molecular Polarity"),
    ("chemistry", "Stoichiometry, Limiting Reagent, and Solution Concentration"),
    ("chemistry", "Gas Laws, Kinetic Theory, and Non-Ideal Corrections"),
    ("chemistry", "Thermochemistry, Enthalpy, and Hess Cycles"),
    ("chemistry", "Entropy, Gibbs Free Energy, and Spontaneity"),
    ("chemistry", "Chemical Equilibrium and Le Châtelier Analysis"),
    ("chemistry", "Acid–Base Equilibria, pH, and Buffer Design"),
    ("chemistry", "Electrochemistry: Cells, Nernst, and Electrolysis"),
    ("chemistry", "Reaction Rates, Orders, and Arrhenius Thinking"),
    ("chemistry", "Intro Organic: Functional Groups and Nomenclature"),
    ("chemistry", "Stereochemistry, SN1/SN2, and E1/E2 Reasoning"),
    ("chemistry", "Intro Spectroscopy: IR and UV-Vis Concepts"),
    # Biology (13)
    ("biology", "Macromolecules, Water, and Thermodynamics of Life"),
    ("biology", "Membrane Structure, Transport, and Membrane Potential"),
    ("biology", "Enzyme Kinetics and Metabolic Pathway Logic"),
    ("biology", "Gene Expression: Replication, Transcription, Translation"),
    ("biology", "Mendelian Genetics, Extensions, and Pedigree Reasoning"),
    ("biology", "Population Genetics and Hardy–Weinberg Equilibrium"),
    ("biology", "Natural Selection, Drift, and Speciation Mechanisms"),
    ("biology", "Population Ecology: Growth, Regulation, and Life Tables"),
    ("biology", "Community Ecology: Competition, Predation, and Networks"),
    ("biology", "Ecosystem Energy Flow and Nutrient Cycling"),
    ("biology", "Neurophysiology: Action Potentials and Synapses"),
    ("biology", "Immune Recognition, Memory, and Vaccination Logic"),
    ("biology", "Genomics, Variation, and Introductory Bioinformatics"),
    # Computing & applied math (13)
    ("computing", "Logic, Sets, and Proof Strategies for CS"),
    ("computing", "Asymptotic Growth, Recurrences, and Master Theorem"),
    ("computing", "Graphs: BFS, DFS, and Shortest-Path Foundations"),
    ("computing", "Greedy Algorithms and Exchange Arguments"),
    ("computing", "Dynamic Programming: Subproblems and Optimal Substructure"),
    ("computing", "Hashing, Universality, and Expected Analysis"),
    ("computing", "Floating Point, Conditioning, and Numerical Stability"),
    ("computing", "Linear Least Squares and Normal Equations"),
    ("computing", "Gradient Descent and Convex Optimization Intuition"),
    ("computing", "Monte Carlo Methods and Uncertainty Quantification"),
    ("computing", "Experimental Design, Bias, and Causal Skepticism"),
    ("computing", "Linear Regression, Regularization, and Generalization"),
    ("computing", "Technical Writing, Reproducibility, and Peer Review"),
]


def strand_label(s: str) -> str:
    return {
        "math": "Mathematics",
        "physics": "Physics",
        "chemistry": "Chemistry",
        "biology": "Molecular & Organismal Biology",
        "computing": "Computing & Applied Mathematics",
    }[s]


def full_title(strand: str, short: str) -> str:
    return f"UNIV 2026 — {strand_label(strand)} — {short}"


def validate_count():
    assert len(UNIV_MODULES) == 65, len(UNIV_MODULES)
    by = {}
    for st, _ in UNIV_MODULES:
        by[st] = by.get(st, 0) + 1
    assert all(by[s] == 13 for s in STRANDS_ORDER), by
