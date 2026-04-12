"""
Per-module academic content for UNIV 2026 courses (college / early university level).
Each strand has exactly 13 entries aligned with univ_65_definitions.UNIV_MODULES order within that strand.
"""

from __future__ import annotations

# Curated Wikimedia / educational figures (HTTPS, stable paths). Index by strand.
WIKI_BY_STRAND: dict[str, list[tuple[str, str]]] = {
    "math": [
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Pythagorean.svg/500px-Pythagorean.svg.png",
            "Geometric rigor: from diagrams to symbolic proof culture.",
        ),
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cartesian-coordinate-system.svg/480px-Cartesian-coordinate-system.svg.png",
            "Coordinate systems underpin calculus and linear models.",
        ),
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Epsilon-neighbourhood.svg/440px-Epsilon-neighbourhood.svg.png",
            "ε-neighborhood view of limits (standard analysis picture).",
        ),
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Riemann_sum_convergence.png/500px-Riemann_sum_convergence.png",
            "Riemann sums approaching the definite integral.",
        ),
    ],
    "physics": [
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Free_body.svg/500px-Free_body.svg.png",
            "Free-body diagrams precede any equation in mechanics.",
        ),
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Simple_harmonic_motion_animation.gif/320px-Simple_harmonic_motion_animation.gif",
            "Simple harmonic motion links restoring force to sinusoidal time dependence.",
        ),
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Refraction_photo.png/500px-Refraction_photo.png",
            "Snell’s law describes measurable bending at interfaces.",
        ),
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Electromagnetic_wave.png/500px-Electromagnetic_wave.png",
            "Electromagnetic wave schematic: coupled E and B fields.",
        ),
    ],
    "chemistry": [
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Electron_shell_011_Sodium_-_no_label.svg/480px-Electron_shell_011_Sodium_-_no_label.svg.png",
            "Aufbau and shell structure explain periodic trends.",
        ),
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Water_molecule_3D.svg/400px-Water_molecule_3D.svg.png",
            "Molecular geometry controls polarity and intermolecular forces.",
        ),
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Reaction_coordinate.svg/500px-Reaction_coordinate.svg.png",
            "Reaction coordinate diagrams connect kinetics to thermodynamics qualitatively.",
        ),
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Acetic_acid_dissociation.png/440px-Acetic_acid_dissociation.png",
            "Weak-acid equilibrium in aqueous environment.",
        ),
    ],
    "biology": [
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/DNA_double_helix_horizontal.png/500px-DNA_double_helix_horizontal.png",
            "DNA structure underlies replication and expression fidelity.",
        ),
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Punnett_square.svg/440px-Punnett_square.svg.png",
            "Mendelian probability structures extend to population thinking.",
        ),
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Carbon_cycle-cute_diagram.svg/500px-Carbon_cycle-cute_diagram.svg.png",
            "Ecosystem-scale biogeochemical framing.",
        ),
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Neuron_Hand-tuned.svg/480px-Neuron_Hand-tuned.svg.png",
            "Neuron morphology supports cable and synaptic models.",
        ),
    ],
    "computing": [
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Binary_tree.png/400px-Binary_tree.png",
            "Tree structures underpin many efficient algorithms.",
        ),
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Complexity_classes.svg/500px-Complexity_classes.svg.png",
            "Asymptotic growth classes organize algorithm comparison.",
        ),
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Linear_regression.svg/480px-Linear_regression.svg.png",
            "Regression as projection / least squares in feature space.",
        ),
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Stemplot_basics.svg/500px-Stemplot_basics.svg.png",
            "Exploratory plots precede formal modeling.",
        ),
    ],
}


def wiki_pair(strand: str, module_index: int) -> list[tuple[str, str]]:
    pool = WIKI_BY_STRAND[strand]
    return [pool[module_index % len(pool)], pool[(module_index + 2) % len(pool)]]


# --- Strand-specific PhET rotations (titles must exist in merged SIMS) ---
PHET_MATH = [
    ["Calculus Grapher", "Graphing Quadratics", "Trig Tour"],
    ["Calculus Grapher", "Graphing Slope-Intercept", "Function Builder"],
    ["Graphing Quadratics", "Calculus Grapher", "Curve Fitting"],
    ["Calculus Grapher", "Function Builder", "Graphing Lines"],
    ["Calculus Grapher", "Function Builder", "Curve Fitting"],
    ["Trig Tour", "Fourier: Making Waves", "Calculus Grapher"],
    ["Calculus Grapher", "Trig Tour", "Fourier: Making Waves"],
    ["Vector Addition", "Vector Addition: Equations", "Trig Tour"],
    ["Area Model Algebra", "Graphing Lines", "Expression Exchange"],
    ["Graphing Lines", "Graphing Slope-Intercept", "Equality Explorer"],
    ["Graphing Quadratics", "Calculus Grapher", "Least-Squares Regression"],
    ["Calculus Grapher", "Masses and Springs", "Pendulum Lab"],
    ["Plinko Probability", "Least-Squares Regression", "Center and Variability"],
]

PHET_PHYS = [
    ["Forces and Motion: Basics", "Projectile Motion", "Vector Addition"],
    ["Forces and Motion: Basics", "Friction", "Collision Lab"],
    ["Energy Skate Park", "Masses and Springs", "Pendulum Lab"],
    ["Collision Lab", "Forces and Motion: Basics", "Energy Skate Park"],
    ["Balancing Act", "Masses and Springs", "Energy Skate Park"],
    ["Gravity and Orbits", "My Solar System", "Kepler's Laws"],
    ["Masses and Springs", "Pendulum Lab", "Wave on a String"],
    ["Wave Interference", "Waves Intro", "Sound Waves"],
    ["Charges and Fields", "Coulomb's Law", "Capacitor Lab: Basics"],
    ["Circuit Construction Kit (DC)", "Ohm's Law", "Resistance in a Wire"],
    ["Faraday's Law", "Magnets and Electromagnets", "Generator"],
    ["Geometric Optics", "Bending Light", "Color Vision"],
    ["Blackbody Spectrum", "Models of the Hydrogen Atom", "Quantum Measurement"],
]
PHET_CHEM = [
    ["Models of the Hydrogen Atom", "Blackbody Spectrum", "Rutherford Scattering"],
    ["Molecule Shapes", "Molecule Polarity", "Build a Molecule"],
    ["Molarity", "Concentration", "Reactants, Products and Leftovers"],
    ["Gas Properties", "States of Matter", "Diffusion"],
    ["Energy Forms and Changes", "States of Matter", "Reactions"],
    ["Reactions", "Energy Forms and Changes", "States of Matter"],
    ["Acid-Base Solutions", "pH Scale", "Concentration"],
    ["Acid-Base Solutions", "pH Scale", "Beer's Law Lab"],
    ["Faraday's Law", "Circuit Construction Kit (DC)", "Capacitor Lab: Basics"],
    ["Balancing Chemical Equations", "Concentration", "Molecules and Light"],
    ["Molecule Shapes", "Build a Molecule", "Balancing Chemical Equations"],
    ["Molecules and Light", "Beer's Law Lab", "Blackbody Spectrum"],
    ["Beer's Law Lab", "Molecules and Light", "Blackbody Spectrum"],
]
# Fix invalid "Reactions" - use Reactants Products Leftovers + Balancing
PHET_CHEM[5] = ["Balancing Chemical Equations", "Energy Forms and Changes", "States of Matter"]
PHET_CHEM[4] = ["States of Matter", "Gas Properties", "Energy Forms and Changes"]
PHET_CHEM[8] = ["Acid-Base Solutions", "Concentration", "Beer's Law Lab"]

PHET_BIO = [
    ["Gene Expression Essentials", "Build a Nucleus", "Build an Atom"],
    ["Membrane Transport", "Neuron", "Diffusion"],
    ["Gene Expression Essentials", "Molecules and Light", "Neuron"],
    ["Gene Expression Essentials", "Natural Selection", "Neuron"],
    ["Natural Selection", "Gene Expression Essentials", "Membrane Transport"],
    ["Natural Selection", "Gene Expression Essentials", "Greenhouse Effect"],
    ["Natural Selection", "Greenhouse Effect", "Membrane Transport"],
    ["Natural Selection", "Greenhouse Effect", "Gene Expression Essentials"],
    ["Greenhouse Effect", "Membrane Transport", "Natural Selection"],
    ["Neuron", "Membrane Transport", "Gene Expression Essentials"],
    ["Natural Selection", "Gene Expression Essentials", "Neuron"],
    ["Gene Expression Essentials", "Natural Selection", "Build a Nucleus"],
    ["Gene Expression Essentials", "Natural Selection", "Build a Nucleus"],
]

PHET_COMP = [
    ["Equality Explorer", "Expression Exchange", "Function Builder"],
    ["Function Builder", "Graphing Lines", "Curve Fitting"],
    ["Function Builder", "Graphing Lines", "Equality Explorer"],
    ["Unit Rates", "Graphing Slope-Intercept", "Area Model Multiplication"],
    ["Function Builder", "Graphing Lines", "Expression Exchange"],
    ["Plinko Probability", "Least-Squares Regression", "Center and Variability"],
    ["Curve Fitting", "Least-Squares Regression", "Graphing Lines"],
    ["Least-Squares Regression", "Curve Fitting", "Plinko Probability"],
    ["Calculus Grapher", "Graphing Slope-Intercept", "Curve Fitting"],
    ["Plinko Probability", "Center and Variability", "Curve Fitting"],
    ["Center and Variability", "Plinko Probability", "Least-Squares Regression"],
    ["Least-Squares Regression", "Curve Fitting", "Plinko Probability"],
    ["Equality Explorer", "Expression Exchange", "Graphing Lines"],
]


def phet_trio(strand: str, i: int) -> list[str]:
    tab = {
        "math": PHET_MATH,
        "physics": PHET_PHYS,
        "chemistry": PHET_CHEM,
        "biology": PHET_BIO,
        "computing": PHET_COMP,
    }[strand]
    return tab[i % 13]


# --- Academic prose + formal notes per (strand, index) ---
def snippet(strand: str, idx: int) -> dict:
    """Returns keys: overview, formal, pitfall, lab_prompt (HTML-safe plain text; outer layer escapes)."""
    S = SNIPPET_TABLE[strand][idx]
    return S


def _M(
    overview: str,
    formal: str,
    pitfall: str,
    lab: str,
) -> dict:
    return {
        "overview": overview,
        "formal": formal,
        "pitfall": pitfall,
        "lab_prompt": lab,
    }


SNIPPET_TABLE: dict[str, list[dict]] = {}

# ==================== MATHEMATICS (13) ====================
SNIPPET_TABLE["math"] = [
    _M(
        "This module treats the limit as the organizing idea of analysis: you learn to read 'arbitrarily close' "
        "language (ε–δ) as a contract about error control, not as a symbol shuffle. We emphasize sequential limits "
        "as intuition and ε–δ limits as certification, then connect both to continuity and to the failure modes "
        "that appear in removable, jump, and oscillatory discontinuities.",
        "<strong>Core definitions.</strong> Intuitively, lim<sub>x→a</sub> f(x) = L means: for every ε &gt; 0 there exists δ &gt; 0 such that "
        "0 &lt; |x−a| &lt; δ implies |f(x)−L| &lt; ε. Continuity at a requires lim<sub>x→a</sub> f(x) = f(a). "
        "Sequential characterization (Heine): f is continuous at a iff for every sequence x<sub>n</sub>→a with x<sub>n</sub>≠a, f(x<sub>n</sub>)→f(a).",
        "Students often treat limits as 'plugging in' values. That only works when continuity is already established; "
        "otherwise you must argue from inequalities, squeeze bounds, or known limit theorems.",
        "Use Calculus Grapher to zoom on candidate points; pair with algebraic ε–δ scratch work for one rational example.",
    ),
    _M(
        "Differentiation is introduced as linear local approximation: the derivative at a point is the slope of the unique best "
        "linear map approximating incremental change. The chain rule encodes composition; the product and quotient rules encode "
        "bilinear structure. Related rates force you to bind variables with a constraint equation before differentiating implicitly.",
        "<strong>Key results.</strong> (f+g)' = f'+g'; (fg)' = f'g+fg'; (f/g)' = (f'g−fg')/g²; (f∘g)' = (f'∘g)·g'. "
        "Linearization: L(x)=f(a)+f'(a)(x−a). Mean value theorem prerequisites appear next module.",
        "A classic error is differentiating without tracking independent variable: in related rates, differentiate with respect to time t after "
        "writing a single equation tying quantities.",
        "Graph several compositions in Function Builder; verify chain-rule slopes numerically on Graphing Slope-Intercept overlays.",
    ),
    _M(
        "Between derivatives and shape of graphs lies the Mean Value Theorem: existence of an interior slope matching secant slope. "
        "From it you derive monotonicity tests, concavity via second derivative, and first-pass optimization with critical points and endpoints.",
        "<strong>MVT.</strong> If f is continuous on [a,b] and differentiable on (a,b), ∃c∈(a,b) with f'(c)=(f(b)−f(a))/(b−a). "
        "If f'&gt;0 on an interval, f is increasing there; f''&gt;0 implies convex (concave up) graph.",
        "Do not confuse f' = 0 with extremum: inflection and plateau counterexamples exist; classify with sign changes or higher-order tests.",
        "Use Graphing Quadratics and Calculus Grapher to mark tangent lines whose slopes match secants on an interval.",
    ),
    _M(
        "The integral begins as a limit of Riemann sums over partitions; the Fundamental Theorem links antiderivatives to accumulation. "
        "You interpret ∫<sub>a</sub><sup>b</sup> f as signed area when f is integrable and as net change when f models a rate.",
        "<strong>FTC (Part 1).</strong> If F(x)=∫<sub>a</sub><sup>x</sup> f(t)dt and f is continuous, then F'(x)=f(x). "
        "<strong>FTC (Part 2).</strong> If F'=f, then ∫<sub>a</sub><sup>b</sup> f = F(b)−F(a).",
        "Mixing up the variable of integration with limit variables is common; the dummy variable inside the integral is bound.",
        "Visualize partitions with Calculus Grapher; compare left/right/mid sums for the same function on [0,1].",
    ),
    _M(
        "Techniques—substitution, parts, partial fractions, trig identities—are bookkeeping tools justified by reversing the chain/product rules. "
        "Improper integrals extend domains via limits; convergence parallels series tests in spirit.",
        "∫ u dv = uv − ∫ v du. Partial fractions require proper rational degree first. For ∫<sub>1</sub><sup>∞</sup> f, study lim<sub>b→∞</sub> ∫<sub>1</sub><sup>b</sup> f.",
        "Applying integration by parts without a plan for simplifying ∫ v du often loops endlessly; choose u to differentiate toward polynomials/logs.",
        "Use Function Builder to differentiate candidate antiderivatives and confirm they recover the integrand.",
    ),
    _M(
        "Sequences are functions ℕ→ℝ; series are sequence of partial sums. Convergence tests (comparison, ratio, root, alternating) are a toolkit "
        "with different hypotheses—no single test is universal. Taylor series package smooth functions as power series on intervals of convergence.",
        "Geometric series ∑ r<sup>n</sup> converges iff |r|&lt;1. Ratio test looks at lim |a<sub>n+1</sub>/a<sub>n</sub>|. Taylor: f(x)=∑ f<sup>(n)</sup>(a)/n! (x−a)<sup>n</sup> with remainder estimates.",
        "Confusing absolute vs conditional convergence leads to illegal rearrangements; alternating series need Leibniz hypotheses separately.",
        "Explore periodic components with Fourier: Making Waves; relate partial sums to graph shape on Trig Tour.",
    ),
    _M(
        "Taylor polynomials approximate smooth functions; remainder forms quantify error. Analyticity on an interval means the Taylor series converges "
        "back to the function there—stronger than mere differentiability.",
        "Lagrange remainder: R<sub>n</sub>(x)=f<sup>(n+1)</sup>(ξ)/(n+1)! (x−a)<sup>n+1</sup> for some ξ between a and x. Radius of convergence from ratio/root limits on coefficients.",
        "Assuming equality f(x)=Taylor series without checking remainder→0 is a frequent unjustified leap.",
        "Overlay increasing-degree Taylor approximations in Calculus Grapher for e<sup>x</sup>, sin x, and log(1+x) near 0.",
    ),
    _M(
        "Vectors in ℝ<sup>3</sup> support lines (parametric), planes (normal equation), distances, and angles via dot product. Cross product encodes area and orientation; "
        "triple products encode volumes.",
        "Line: r(t)=r<sub>0</sub>+t v. Plane: n·(x−x<sub>0</sub>)=0. Distance point–plane |n·(p−x<sub>0</sub>|/||n||. Cross product magnitude ||a×b||=||a||||b||sin θ.",
        "Normalizing vectors incorrectly (forgetting magnitude) breaks projection formulas; always separate direction from length.",
        "Build resultants with Vector Addition; verify parallelogram law numerically with Vector Addition: Equations.",
    ),
    _M(
        "Matrices encode linear systems Ax=b. Row reduction reveals rank, pivots, and solution structure. Invertibility ⇔ trivial nullspace for square A; "
        "inverse solves systems when conditioning permits.",
        "Elementary row ops = left multiplication by elementary matrices. If A row-reduces to I, A is invertible. LU factorization (when stable) speeds repeated solves.",
        "Treating non-invertible matrices as if Gaussian elimination always yields a unique solution causes contradictions; check consistency of augmented [A|b].",
        "Use Equality Explorer: Two Variables for small systems intuition; scale up symbolically on paper.",
    ),
    _M(
        "Abstract vector spaces axiomatize closure under addition/scalar multiplication. Subspaces must contain 0. Bases provide unique coordinates; dimension is invariant. "
        "Linear maps preserve linear structure; matrix representation depends on basis choice.",
        "A set is a basis if independent and spanning. Rank-nullity: dim ker(T)+dim im(T)=dim domain. Change-of-basis uses invertible transition matrices.",
        "Declaring a set a basis without proving both independence and spanning is incomplete.",
        "Relate linear transformations to matrix columns as images of basis vectors; verify with Graphing Lines for ℝ² projections.",
    ),
    _M(
        "Eigenvalues λ solve det(A−λI)=0; eigenvectors span invariant directions. Diagonalization A=PDP<sup>−1</sup> simplifies powers and differential systems ẋ=Ax when a full eigenbasis exists.",
        "Characteristic polynomial roots (with multiplicity) locate eigenvalues. Defective matrices need Jordan blocks (intro mention). Stability of linear ODEs ties to Re(λ).",
        "Diagonalizing without enough independent eigenvectors fails silently if you ignore algebraic vs geometric multiplicity.",
        "Use Least-Squares Regression as a least-squares eigenproblem analogy in data; pair with Graphing Quadratics for quadratic forms intuition.",
    ),
    _M(
        "First-order ODEs: separable, linear integrating factor, autonomous phase-line reasoning. Second-order constant-coefficient equations solve via characteristic polynomials; "
        "spring-mass-damper analogies carry physical meaning.",
        "Linear first-order: y'+P(t)y=Q(t) with μ=exp(∫P). Simple harmonic: y''+ω²y=0 has y=A cos ωt+B sin ωt. Damping adds exponential envelopes.",
        "Forgetting initial conditions or superposition principles in homogeneous vs particular splits causes sign/phase errors.",
        "Simulate Masses and Springs and Pendulum Lab; compare small-angle period prediction to measured period in PhET.",
    ),
    _M(
        "Probability spaces, σ-algebras (informally), random variables, expectation linearity, variance sums (with independence). Intro inference: estimators, sampling distributions, "
        "central limit theorem intuition, hypothesis tests as decision rules with error tradeoffs.",
        "E[aX+b]=aE[X]+b. Var(X)=E[X²]−E[X]². For independent X,Y, Var(X+Y)=Var(X)+Var(Y). CLT: standardized means approximate N(0,1) for large n under mild conditions.",
        "Treating dependent variables as independent when computing variance double-counts covariance structure.",
        "Run Plinko Probability; connect empirical histogram to CLT; use Center and Variability for mean vs median robustness discussion.",
    ),
]

# ==================== PHYSICS (13) ====================
SNIPPET_TABLE["physics"] = [
    _M(
        "Kinematics describes motion without insisting on causes. Position, velocity, acceleration relate by differentiation; projectile problems split into orthogonal "
        "components with independent constant acceleration in each direction when air resistance is neglected.",
        "v(t)=dr/dt; a(t)=dv/dt. Constant a: r=r<sub>0</sub>+v<sub>0</sub>t+½at². Range formulas assume g constant near Earth surface.",
        "Mixing vector components across axes (using v<sub>x</sub> where v<sub>y</sub> belongs) is the dominant sign error source.",
        "Projectile Motion + Vector Addition: predict range from launch speed/angle; compare to PhET readouts.",
    ),
    _M(
        "Newton's laws connect forces to motion in inertial frames. Free-body diagrams externalize the force inventory before ΣF=ma. Friction models (static/kinetic) are phenomenological bounds, "
        "not fundamental symmetries.",
        "ΣF=ma in vector form. Static friction |f<sub>s</sub>|≤μ<sub>s</sub>N; kinetic f<sub>k</sub>=μ<sub>k</sub>N. Always draw normal forces perpendicular to surfaces first.",
        "Double-counting action-reaction pairs on the same body violates Newton's third law usage; pairs act on different bodies.",
        "Forces and Motion: Basics with Friction: compare net force readings to predicted acceleration.",
    ),
    _M(
        "Work–energy theorems trade path integrals of force for changes in kinetic energy. Conservative forces admit potential energy; non-conservative forces (friction) dissipate mechanical energy to thermal modes.",
        "W=∫F·dr; ΔK=W<sub>net</sub>. Conservative: F=−∇U, so ΔU=−W<sub>cons</sub>. Power P=dW/dt=F·v for particle models.",
        "Confusing work done by a single force with net work on the object leads to wrong ΔK.",
        "Energy Skate Park: track bar charts across loops; compare mechanical energy with/without friction.",
    ),
    _M(
        "Momentum p=mv is conserved for isolated systems (vector conservation). Collisions partition into elastic (kinetic energy conserved) and inelastic (not); center-of-mass frame simplifies bookkeeping.",
        "Impulse J=∫F dt=Δp. 1D elastic: relative speed reversal. Explosion problems use initial rest → CM remains fixed.",
        "Using scalar addition for momenta in 2D without components causes direction loss.",
        "Collision Lab: verify momentum row sums before and after; vary elasticity slider.",
    ),
    _M(
        "Rigid-body rotation parallels translation: τ=Iα, L=Iω, with direction via right-hand rule. Rolling combines translation of CM with rotation about CM; non-slipping adds kinematic link v=ωR.",
        "τ=r×F; I=∫ r² dm. Parallel-axis: I=I<sub>cm</sub>+Md². Work in rotation: W=∫τ dθ=ΔK<sub>rot</sub>.",
        "Applying point-mass formulas to extended objects without integrating inertia yields wrong α.",
        "Balancing Act + Masses and Springs: build torque intuition before symbolic wheel problems.",
    ),
    _M(
        "Newtonian gravitation F=Gm₁m₂/r² produces elliptical orbits under inverse-square central force; energy and angular momentum classify bound vs unbound trajectories. "
        "Virial ideas connect ⟨K⟩ and ⟨U⟩ for circular orbits.",
        "Circular orbit speed v=√(GM/r); period T²∝r³ for Kepler third law in Newtonian limit. Total E bound orbits &lt;0.",
        "Confusing g (surface field strength) with G (universal constant) breaks unit checks.",
        "Gravity and Orbits + Kepler's Laws: vary semi-major axis; read off period scaling.",
    ),
    _M(
        "Small oscillations about stable equilibria are harmonic with ω=√(k/m) for ideal springs. Damping adds exponential envelopes; driven oscillators show resonance when drive frequency matches natural frequency.",
        "SHM: x''+ω²x=0. Light damping: underdamped decaying sinusoid. Quality factor Q relates bandwidth to resonance sharpness qualitatively.",
        "Using energy amplitude relations without checking small-angle validity (pendulum) overstates frequency at large θ.",
        "Pendulum Lab + Masses and Springs: measure period vs amplitude; discuss breakdown of linear model.",
    ),
    _M(
        "Waves transport energy, not bulk matter (in linear media). Superposition explains interference; standing waves arise from boundary reflections. Sound vs light share wave mathematics with different dispersions.",
        "y(x,t)=f(x−vt) solves wave equation classically. Standing wave: spatial sinusoid × temporal sinusoid with nodes at fixed positions.",
        "Adding amplitudes without phase awareness misses destructive interference regions.",
        "Wave Interference + Sound Waves: path-length difference to predict loud/quiet zones.",
    ),
    _M(
        "Electrostatics begins with Coulomb's law and superposition; Gauss's law simplifies highly symmetric charge distributions. Electric potential is path-independent for static fields: E=−∇V.",
        "∮E·dA=Q<sub>enc</sub>/ε₀. Point charge V=kQ/r. Capacitors store energy U=½CV² in ideal models.",
        "Using Gauss's law with wrong symmetry surfaces gives incorrect enclosed flux accounting.",
        "Charges and Fields + Coulomb's Law: map field lines; compare to textbook dipole sketches.",
    ),
    _M(
        "Steady DC circuits obey Kirchhoff's junction and loop rules. Ohm's law is material constitutive relation, not a fundamental axiom. Capacitors in series/parallel invert rules compared to resistors.",
        "Series resistors add; parallel inverses add. RC time constant τ=RC governs charging curves. Power in resistor P=I²R=IV.",
        "Treating ideal wires as having voltage drops contradicts Kirchhoff assumptions.",
        "Circuit Construction Kit (DC) + Ohm's Law: build series/parallel; measure I,V consistency.",
    ),
    _M(
        "Magnetic forces on charges qv×B bend trajectories; currents in wires feel forces from external B. Faraday's law: changing flux induces emf; Lenz's law gives opposition sign. "
        "Induction underlies generators and inductors in circuits.",
        "Φ=∫B·dA; emf=−dΦ/dt. Ideal solenoid B≈μ₀nI. Transformers (AC) rely on mutual flux linkage.",
        "Using Faraday without tracking orientation of area vector flips emf sign randomly.",
        "Faraday's Law + Generator: change flux rate; correlate bulb brightness with |dΦ/dt| qualitatively.",
    ),
    _M(
        "Ray optics models reflection/refraction with Snell's law and thin-lens/mirror equations. Image types (real/virtual) depend on sign conventions; paraxial assumption underpins lensmaker simplifications.",
        "n₁ sin θ₁=n₂ sin θ₂. Thin lens 1/f=1/s<sub>o</sub>+1/s<sub>i</sub>. Magnification m=−s<sub>i</sub>/s<sub>o</sub>.",
        "Sign errors on object/image distances propagate wrong orientation predictions.",
        "Geometric Optics + Bending Light: verify Snell at air/glass; predict image location for converging lens.",
    ),
    _M(
        "Photoelectric effect and quantization motivate photon energy E=hf. Atomic spectra and simplest quantum models (particle in a box, hydrogen toy models) illustrate discrete states vs classical continua.",
        "Photon momentum p=E/c in vacuum for electromagnetic quanta. de Broglie λ=h/p links matter waves qualitatively.",
        "Applying classical orbit pictures inside atoms without probability interpretation misleads about stability.",
        "Blackbody Spectrum + Models of the Hydrogen Atom: connect spectral lines to quantized transitions; discuss classical ultraviolet catastrophe failure.",
    ),
]

# ==================== CHEMISTRY (13) — continue in same list pattern ====================
SNIPPET_TABLE["chemistry"] = [
    _M(
        "Quantum-mechanical atoms explain periodicity: orbitals are probability amplitudes, not classical orbits. Quantum numbers (n, l, m<sub>l</sub>, m<sub>s</sub>) index solutions; Aufbau and Hund's rules predict ground configurations.",
        "Radial probability differs from |ψ|² slices; shielding and penetration make 4s fill before 3d in potassium/calcium anomalies worth discussing.",
        "Drawing electrons as fixed paths rather than distributions invites wrong ionization reasoning.",
        "Models of the Hydrogen Atom + Blackbody Spectrum: relate spectral lines to energy-level differences.",
    ),
    _M(
        "Lewis structures encode valence electron bookkeeping; VSEPR predicts geometry from electron domains. Polarity emerges from vector sum of bond dipoles and symmetry.",
        "Formal charge FC=V−N−B/2 helps choose major resonance contributors. Electronegativity trends increase toward upper-right (F reference).",
        "Ignoring resonance when multiple equivalent structures lower energy misestimates bond order.",
        "Molecule Shapes + Build a Molecule: predict angles; compare to VSEPR table.",
    ),
    _M(
        "Stoichiometry converts balanced equations to mole bridges. Limiting reagent problems exhaust the scarcest participant first. Solution chemistry adds M = mol/L; dilutions use M₁V₁=M₂V₂ only when moles conserved in that step.",
        "Percent yield = actual/theoretical ×100%. Always convert masses→moles via molar mass before ratio steps.",
        "Using volumes without converting to moles in gas/solution contexts breaks proportionality.",
        "Reactants, Products and Leftovers + Molarity: run limiting-reagent sandwiches; titrate concentration puzzles.",
    ),
    _M(
        "Ideal gas law PV=nRT aggregates kinetic theory assumptions (point particles, elastic collisions, negligible volume). Deviations at high P or low T signal real gas corrections (van der Waals intuition).",
        "Kinetic theory: average translational KE ∝ T. Partial pressures in mixtures add in ideal limit (Dalton).",
        "Confusing R units (L·atm vs J) causes magnitude errors by orders of magnitude.",
        "Gas Properties + States of Matter: compress/heat; relate PV tracks to nRT checks.",
    ),
    _M(
        "Enthalpy H=U+PV tracks heat flow at constant pressure in many lab settings. Hess's law cycles unknown reaction enthalpies via known steps; formation enthalpies reference elements in standard states.",
        "ΔH<sub>rxn</sub>=ΣνΔH<sub>f</sub>(products)−ΣνΔH<sub>f</sub>(reactants). Calorimetry q=mcΔT approximates ΔH under assumptions.",
        "Treating bond enthalpy estimates as exact reaction enthalpies ignores environment and state details.",
        "Energy Forms and Changes + States of Matter: track energy bar charts for phase + reaction sketches.",
    ),
    _M(
        "Second law introduces entropy; Gibbs G=H−TS decides spontaneity at constant T,P. Coupled reactions can drive non-spontaneous steps (ATP hydrolysis paradigm in biochemistry).",
        "ΔG=ΔH−TΔS. ΔG&lt;0 spontaneous forward; ΔG=0 equilibrium. ΔG°=−RT ln K links to equilibrium constants.",
        "Using ΔH alone to argue spontaneity ignores entropy (e.g., ice melting above 0°C).",
        "States of Matter + Energy Forms and Changes: discuss disorder arguments qualitatively before numbers.",
    ),
    _M(
        "Equilibrium constants K express ratio of activities at balance; Q compares to K to predict direction. Le Châtelier predicts qualitative shifts under stress (concentration, pressure for gases, temperature).",
        "K<sub>p</sub> vs K<sub>c</sub> tied by (RT)<sup>Δn</sup>. Catalysts speed both directions without changing K.",
        "Adding solids does not shift K expressions written without solid activities (heterogeneous equilibria).",
        "Acid-Base Solutions + Concentration: tie common-ion effect to Q vs K thinking.",
    ),
    _M(
        "Brønsted–Lowry acids donate protons; conjugate pairs differ by one H⁺. pH=−log a(H⁺) (approximate with concentration in intro). Buffers resist pH via Henderson–Hasselbalch when both weak acid and conjugate base significant.",
        "For HA ⇌ H⁺+A⁻, K<sub>a</sub> quantifies strength. Strong acids assumed fully dissociated in dilute aqueous intro models.",
        "Diluting a buffer without changing ratio much vs diluting acid alone are different stories—students conflate.",
        "pH Scale + Acid-Base Solutions: titration curve sketch vs simulation.",
    ),
    _M(
        "Galvanic cells separate half-reactions spatially; standard potentials E° rank intrinsic oxidizing/reducing power under standard states. Nernst equation adds concentration dependence; electrolysis drives non-spontaneous cells with external voltage.",
        "ΔG°=−nFE°. Nernst: E=E°−(RT/nF) ln Q. Overpotential and kinetics matter in real electrolysis cells.",
        "Reversing cathode/anode labels breaks cell direction and sign of E<sub>cell</sub>.",
        "Faraday's Law demo parallels electron stoichiometry; use Circuit Construction Kit for conceptual voltage loops.",
    ),
    _M(
        "Rates measure how concentrations change; orders are empirical exponents in rate laws. Arrhenius k=Ae<sup>−Ea/RT</sup> links temperature to exponential growth of successful collisions (qualitative). "
        "Mechanisms propose elementary steps whose orders match molecularity only if single-step.",
        "Integrated laws for zero/first order give linearized plots. Pre-equilibrium and steady-state approximations appear in advanced mechanisms.",
        "Equating overall order to stoichiometric coefficients without experiment is invalid.",
        "Molecules and Light + Concentration: photochemical rate sensitivity to intensity (conceptual).",
    ),
    _M(
        "Organic nomenclature (IUPAC) encodes longest chain, substituents, functional groups. Isomers (constitutional, stereochemical) have distinct properties; chirality matters for biological recognition.",
        "Functional group priority determines suffix/parent chain. Newman projections visualize staggered/eclipsed conformations.",
        "Naming by common names only blocks communication in technical settings.",
        "Build a Molecule + Molecule Shapes: build ethanol vs dimethyl ether (isomers).",
    ),
    _M(
        "SN1/SN2/E1/E2 compete based on substrate, nucleophile strength, temperature, and solvent polarity. Rate laws differ: SN1/E1 show first order in substrate; SN2 is bimolecular.",
        "Polar protic solvents stabilize carbocations (SN1 risk); polar aprotic can accelerate SN2. Zaitsev vs Hofmann eliminations appear with base bulk.",
        "Assuming SN2 always because 'nucleophile present' ignores tertiary substrate blocking.",
        "Molecule Polarity + Build a Molecule: discuss how solvent polarity stabilizes charges in transition states.",
    ),
    _M(
        "IR probes bond stretches/bends; characteristic frequencies group-identify functionalities. UV-Vis often involves π→π* or n→π* with conjugation lowering energy gaps (color shifts). Beer–Lambert A=εlc links absorbance to concentration.",
        "Selection rules and linewidth broaden peaks; hydrogen bonding shifts OH stretches dramatically.",
        "Treating absorbance as linear without checking concentration range violates Beer–Lambert validity.",
        "Beer's Law Lab + Molecules and Light: tie path length and concentration to absorbance.",
    ),
]

# ==================== BIOLOGY (13) ====================
SNIPPET_TABLE["biology"] = [
    _M(
        "Thermodynamics constrains life: ΔG&lt;0 processes can drive work when coupled. Water's polarity enables solvation, hydrogen bonding, and hydrophobic effect organizing macromolecules.",
        "ΔG=ΔH−TΔS. High heat capacity of water buffers temperature; pH affects ionizable side chains.",
        "Confusing ΔG° with ΔG under cellular non-standard conditions misjudges reaction direction.",
        "Membrane Transport + States of Matter: diffusion vs active transport energy accounting.",
    ),
    _M(
        "Lipid bilayers self-assemble; proteins carry transport, enzymatic, and signaling roles. Electrochemical gradients store free energy for secondary active transport and excitable cells.",
        "Nernst equation for single-ion equilibrium potential; Goldman-style combinations approximate resting potential in models.",
        "Assuming all channels are always open ignores gating and regulation.",
        "Membrane Transport + Neuron: set gradients; observe driving forces on ion flow.",
    ),
    _M(
        "Michaelis–Menten kinetics model saturation: v=Vmax[S]/(K<sub>m</sub>+[S]). Competitive inhibitors raise apparent K<sub>m</sub>; noncompetitive lower V<sub>max</sub>. Allosteric regulation shifts activity curves.",
        "Lineweaver–Burk plots linearize data but amplify error at low v—awareness for lab critique.",
        "Treating reversible reactions as one-way because enzyme present ignores cellular steady states.",
        "Gene Expression Essentials: tie enzyme abundance control to transcription/translation themes.",
    ),
    _M(
        "Central dogma: DNA→RNA→protein with directionality and proofreading at each stage. Operons and eukaryotic chromatin regulation show how expression context differs across domains.",
        "Replication needs primers, leading/lagging strands, and telomere exceptions. Genetic code degeneracy buffers some mutations.",
        "Confusing transcription factors with ribosomes mixes regulation and translation machinery.",
        "Gene Expression Essentials + Build a Nucleus: connect information storage to expression logistics.",
    ),
    _M(
        "Mendel's laws assume independent assortment (unlinked loci) and complete dominance in simplest forms. Extensions: incomplete dominance, codominance, epistasis, linkage, and sex-linked inheritance.",
        "χ² tests can check segregation ratios under experimental design discipline.",
        "Applying independent assortment when genes are linked on same chromosome without recombination yields wrong ratios.",
        "Punnett square exercises + Natural Selection: link allele frequency change to selection (preview Hardy–Weinberg).",
    ),
    _M(
        "Hardy–Weinberg provides null model for allele frequencies: random mating, no selection/mutation/migration/drift, infinite population. Violations become hypotheses to test with data.",
        "p+q=1; p²+2pq+q²=1 for two alleles. Inbreeding increases homozygosity quantified by F.",
        "Using HW after strong selection in the same generation without updating p is inconsistent.",
        "Natural Selection + Gene Expression Essentials: discuss heritable variation prerequisites.",
    ),
    _M(
        "Selection, drift, gene flow, and mutation reshape allele frequencies. Speciation modes (allopatric, sympatric) differ by geography and reproductive isolation mechanisms.",
        "Phylogenies are hypotheses inferred from character data; bootstrap support communicates uncertainty.",
        "Equating 'survival of the fittest' to intentional optimization misrepresents undirected variation.",
        "Natural Selection + Greenhouse Effect: optional discussion of climate-driven selection pressures.",
    ),
    _M(
        "Exponential and logistic models capture idealized population growth; carrying capacity emerges from resource limits. Life tables and R<sub>0</sub> formalize demography.",
        "Discrete logistic maps can show chaos—bridge to mathematical biology reading.",
        "Assuming exponential growth indefinitely ignores density dependence.",
        "Natural Selection + Greenhouse Effect: population bottlenecks and recovery scenarios.",
    ),
    _M(
        "Species interactions: predation, competition, mutualism, parasitism alter population trajectories. Lotka–Volterra models are caricatures with equilibrium and cycle behavior.",
        "Trophic cascades show indirect effects; keystone species disproportionately impact communities.",
        "Confusing correlation in field surveys with mechanistic interaction without experiments.",
        "Natural Selection + Membrane Transport: metaphorical 'competition' vs physical transport analogies—keep distinct.",
    ),
    _M(
        "Energy enters ecosystems via primary production; nutrients cycle (C, N, P) while energy dissipates as heat. Biogeochemistry links organisms to planetary reservoirs.",
        "Pyramid of energy narrows by ~10% rule heuristically; efficiencies vary widely by ecosystem.",
        "Claiming nutrients are destroyed violates conservation; they change chemical form/location.",
        "Greenhouse Effect + Natural Selection: carbon cycle coupling to productivity.",
    ),
    _M(
        "Action potentials arise from voltage-gated Na⁺/K⁺ dynamics; myelination increases conduction via saltatory propagation. Synapses convert electrical signals to chemical signals with quantal release.",
        "Temporal and spatial summation integrate inputs; long-term plasticity underlies learning models.",
        "Treating all synapses as excitatory ignores inhibition shaping network behavior.",
        "Neuron + Membrane Transport: threshold and refractory period demos.",
    ),
    _M(
        "Innate vs adaptive immunity: barriers, phagocytes, complement vs lymphocytes with specificity and memory. Vaccination trains adaptive memory without full disease risk.",
        "MHC presentation connects intracellular/extracellular antigen pathways; autoimmunity arises from tolerance failures.",
        "Antibodies neutralize but do not necessarily kill pathogens alone—effector cells complement functions.",
        "Natural Selection + Gene Expression Essentials: antigenic variation in pathogens.",
    ),
    _M(
        "Genomes are sequenced, assembled, annotated; variation (SNPs, indels, CNVs) underlies traits and disease risk. Intro pipelines: reads → alignment → variant calling with error models.",
        "Ethics: ancestry inference, privacy, consent in biobanks.",
        "Treating p-values from many tests without multiple comparison control inflates false positives.",
        "Gene Expression Essentials + Natural Selection: connect SNPs to expression QTL concepts qualitatively.",
    ),
]

# ==================== COMPUTING & APPLIED MATH (13) ====================
SNIPPET_TABLE["computing"] = [
    _M(
        "Propositional logic and quantifiers underpin specifications and proofs. Proof techniques: direct, contrapositive, contradiction, induction on ℕ, strong induction, structural induction on trees.",
        "Induction requires base case + inductive step with clear hypothesis scope; off-by-one errors break validity.",
        "Treating empirical testing as proof for infinite domains is invalid.",
        "Equality Explorer + Expression Exchange: algebraic invariants as analogies to logical equivalence.",
    ),
    _M(
        "Asymptotic notation O, Ω, Θ hides constants but preserves growth rates. Recurrences like T(n)=2T(n/2)+O(n) solve via master theorem cases; understand overhead terms in mergesort vs quicksort worst case.",
        "Substitution and tree methods verify intuition when master theorem borderlines fail.",
        "Confusing best-case runtime with worst-case guarantees invalidates complexity claims.",
        "Graphing Lines + Function Builder: plot n vs n log n vs n² qualitatively.",
    ),
    _M(
        "Graphs model relationships; BFS layers shortest paths in unweighted graphs; DFS supports connectivity and topological sorting on DAGs. Dijkstra adds non-negative edge weights.",
        "Representations: adjacency list vs matrix trade memory vs query time.",
        "Running BFS without marking visited revisits nodes exponentially.",
        "Graphing Lines as ℝ² grid intuition; Function Builder for path length toy models.",
    ),
    _M(
        "Greedy algorithms choose locally optimal steps; correctness needs exchange argument or matroid structure. Counterexamples when greedy fails motivate dynamic programming.",
        "Activity selection classic; Huffman coding greedy on trees with optimal substructure proof.",
        "Assuming greedy works because examples succeed invites silent failures on hidden cases.",
        "Unit Rates + Graphing Slope-Intercept: greedy slope choices on piecewise linear costs.",
    ),
    _M(
        "Dynamic programming memoizes overlapping subproblems; optimal substructure lets reconstruct solutions. Bottom-up vs top-down trades recursion depth for table fill order.",
        "Knapsack variants differ subtlely (0/1 vs unbounded); state definitions must encode constraints.",
        "Storing insufficient state in DP table loses optimality.",
        "Expression Exchange: expand recurrent formulas symbolically before coding.",
    ),
    _M(
        "Hashing maps keys to buckets; universal hash families reduce collision probability in expectation. Load factor α=n/m affects average probes; open addressing vs chaining tradeoffs.",
        "Birthday paradox governs collision likelihood; expected probes under simple uniform hashing models scale with load factor; separate chaining vs linear probing alter constants sharply.",
        "Assuming a non-cryptographic hash 'behaves randomly' without a family argument invites false Big-O claims for worst-case inputs.",
        "Plinko Probability: use balls-into-bins intuition for collision rates versus table size.",
    ),
    _M(
        "Floating point is finite precision; rounding errors accumulate. Conditioning measures sensitivity of output to input perturbations; stability measures algorithmic error amplification.",
        "Catastrophic cancellation in subtracting similar large numbers; prefer algebraic rearrangements.",
        "Trusting floating equality without tolerances is fragile.",
        "Curve Fitting + Least-Squares Regression: ill-conditioned design matrices when features correlate.",
    ),
    _M(
        "Least squares minimizes ‖Ax−b‖₂; normal equations A<sup>T</sup>Ax=A<sup>T</sup>b (when A<sup>T</sup>A invertible). QR/SVD viewpoints improve stability vs naive Gaussian elimination on Gram matrix.",
        "Projection interpretation: ŷ is closest vector in column space of A to b.",
        "Squaring condition numbers by forming A<sup>T</sup>A explicitly can destroy accuracy.",
        "Least-Squares Regression + Curve Fitting: compare polynomial degree effects.",
    ),
    _M(
        "Gradient descent on convex smooth functions decreases f along −∇f with appropriate step sizes. Learning rates too large oscillate; too small crawl. Stochastic variants trade noise for speed.",
        "Lipschitz gradients imply descent lemmas in introductory analyses.",
        "Treating non-convex landscapes as if one global minimum is obvious misleads optimization narratives.",
        "Calculus Grapher + Graphing Slope-Intercept: visualize slope along a curve as derivative.",
    ),
    _M(
        "Monte Carlo estimates expectations by sample averages; variance shrinks as 1/√N typically. Importance sampling reduces variance when proposal matches target regions.",
        "PRNG seeds affect reproducibility; not cryptographically secure by default.",
        "Using too few samples without confidence intervals hides uncertainty.",
        "Plinko Probability + Center and Variability: empirical mean vs true mean convergence.",
    ),
    _M(
        "Experiments need controls, randomization, and blinding when feasible. Confounders bias causal claims; observational studies require explicit assumptions (e.g., ignorability) for adjustment methods.",
        "p-hacking and multiple testing inflate false discoveries; preregistration mitigates.",
        "Correlation does not imply causation—cliché but routinely forgotten under narrative pressure.",
        "Center and Variability + Plinko Probability: simulate A/B tests under null.",
    ),
    _M(
        "Linear regression with L2 penalty (ridge) shrinks coefficients; L1 (lasso) promotes sparsity. Bias–variance tradeoff explains validation curves; cross-validation estimates generalization error.",
        "Overfitting fits noise; regularization and simpler models combat it when data limited.",
        "Evaluating on training set only inflates performance estimates.",
        "Least-Squares Regression + Curve Fitting: train/validation split intuition on noisy data.",
    ),
    _M(
        "Reproducible research ties code, data, environment, and narrative. Peer review critiques methods, claims, and limitations. Ethical obligations: authorship, plagiarism, dual use in sensitive models.",
        "Version control and documentation are professional standards, not extras.",
        "Cherry-picking plots without sharing underlying data undermines trust.",
        "Equality Explorer + Expression Exchange: symbolic consistency checks before publication-grade writeups.",
    ),
]

# Validate shapes
for s, n in [("math", 13), ("physics", 13), ("chemistry", 13), ("biology", 13), ("computing", 13)]:
    assert len(SNIPPET_TABLE[s]) == n, (s, len(SNIPPET_TABLE[s]))
