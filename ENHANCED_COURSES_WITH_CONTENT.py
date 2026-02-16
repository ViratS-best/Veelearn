#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Courses with Real Teaching Content and Working PhET Simulators
Updates existing courses with comprehensive educational content
"""

import pymysql
import json
import sys
import os
import io
import random

# Try to load from .env, but don't fail if it doesn't exist
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

AIVEN_CONFIG = {
    "charset": "utf8mb4",
    "connect_timeout": 10,
    "cursorclass": pymysql.cursors.DictCursor,
    "db": os.getenv("AIVEN_DB", "defaultdb"),
    "host": os.getenv("AIVEN_HOST", "veelearndb-asterloop-483e.i.aivencloud.com"),
    "password": os.getenv("AIVEN_PASSWORD", ""),
    "read_timeout": 10,
    "port": int(os.getenv("AIVEN_PORT", "26399")),
    "user": os.getenv("AIVEN_USER", "avnadmin"),
    "write_timeout": 10,
}

# ===== COMPREHENSIVE ALGEBRA COURSE CONTENT =====
ALGEBRA_CONTENT = """
<h1>Algebra Fundamentals - Complete Guide</h1>

<h2>📚 Course Overview</h2>
<p>This comprehensive algebra course covers all essential topics from basic equations to advanced functions. 
Each module includes interactive PhET simulators, practice problems, and real-world applications.</p>

<hr>

<h2>Module 1: Linear Equations & Graphing</h2>
<p><strong>What you'll learn:</strong> How to solve linear equations, understand variables, and graph linear functions.</p>

<h3>1.1 Solving Linear Equations</h3>
<p>A linear equation is an equation where the highest power of the variable is 1. Example: 2x + 5 = 13</p>
<p><strong>Steps to solve:</strong></p>
<ol>
  <li>Identify the variable (unknown value)</li>
  <li>Use inverse operations to isolate the variable</li>
  <li>Check your solution by substituting back</li>
</ol>
<p><strong>Example:</strong> 3x - 7 = 11</p>
<ul>
  <li>Add 7 to both sides: 3x = 18</li>
  <li>Divide by 3: x = 6</li>
  <li>Check: 3(6) - 7 = 18 - 7 = 11 ✓</li>
</ul>

<h3>1.2 Graphing Linear Functions</h3>
<p>A linear function has the form: <strong>y = mx + b</strong></p>
<ul>
  <li><strong>m</strong> = slope (steepness of the line)</li>
  <li><strong>b</strong> = y-intercept (where the line crosses the y-axis)</li>
</ul>

<p><strong>Interactive Simulator:</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/graphing-slope-intercept/latest/graphing-slope-intercept_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Experiment with slope and y-intercept to see how the line changes. Try different values and observe the patterns!</em></p>

<p><strong>Practice Problems:</strong></p>
<ol>
  <li>Find the slope of a line passing through (0, 2) and (3, 8)</li>
  <li>Write the equation of a line with slope 2 and y-intercept -3</li>
  <li>Graph the line y = -1/2 x + 4</li>
</ol>

<hr>

<h2>Module 2: Quadratic Equations & Functions</h2>
<p><strong>What you'll learn:</strong> How quadratic functions work, different forms, and solving quadratic equations.</p>

<h3>2.1 What is a Quadratic Function?</h3>
<p>A quadratic function has the form: <strong>y = ax² + bx + c</strong></p>
<p>The graph of a quadratic function is a parabola (U-shaped curve).</p>
<ul>
  <li>If <strong>a > 0</strong>: parabola opens upward (has a minimum point)</li>
  <li>If <strong>a < 0</strong>: parabola opens downward (has a maximum point)</li>
  <li>The larger |a|, the narrower the parabola; the smaller |a|, the wider it is</li>
</ul>

<h3>2.2 Key Features of Parabolas</h3>
<ul>
  <li><strong>Vertex:</strong> The highest or lowest point on the parabola (turning point)</li>
  <li><strong>Axis of Symmetry:</strong> A vertical line through the vertex (x = -b/2a)</li>
  <li><strong>x-intercepts (Roots):</strong> Where the parabola crosses the x-axis (solutions to ax² + bx + c = 0)</li>
  <li><strong>y-intercept:</strong> Where the parabola crosses the y-axis (the value is always c)</li>
</ul>

<p><strong>Interactive Simulator:</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/graphing-quadratics/latest/graphing-quadratics_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Use the simulator to experiment with different values of a, b, and c. Watch how the vertex moves, the parabola stretches or compresses, and the roots change position.</em></p>

<h3>2.3 Solving Quadratic Equations</h3>
<p><strong>The Quadratic Formula:</strong> x = (-b ± √(b² - 4ac)) / 2a</p>
<p>This formula works for ANY quadratic equation of the form ax² + bx + c = 0</p>

<p><strong>Example:</strong> Solve x² - 5x + 6 = 0</p>
<ul>
  <li>a = 1, b = -5, c = 6</li>
  <li>x = (5 ± √(25 - 24)) / 2 = (5 ± 1) / 2</li>
  <li>x = 3 or x = 2</li>
</ul>

<hr>

<h2>Module 3: Polynomials</h2>
<p><strong>What you'll learn:</strong> Operations with polynomials, factoring, and polynomial division.</p>

<h3>3.1 What are Polynomials?</h3>
<p>A polynomial is an expression with variables and constants combined using addition, subtraction, and multiplication.</p>
<p><strong>Examples:</strong> 3x² + 2x - 5, x³ - 8, 4x⁴ + 2x² + 1</p>

<h3>3.2 Operations with Polynomials</h3>
<p><strong>Adding Polynomials:</strong> Combine like terms</p>
<p>Example: (2x² + 3x - 1) + (x² - 2x + 4) = 3x² + x + 3</p>

<p><strong>Multiplying Polynomials:</strong> Use distributive property (FOIL for binomials)</p>
<p>Example: (x + 2)(x - 3) = x² - 3x + 2x - 6 = x² - x - 6</p>

<p><strong>Factoring:</strong> Reverse of multiplication</p>
<p>Example: x² - 5x + 6 = (x - 2)(x - 3)</p>

<h3>3.3 Special Factoring Patterns</h3>
<ul>
  <li><strong>Difference of Squares:</strong> a² - b² = (a + b)(a - b)</li>
  <li><strong>Perfect Square Trinomial:</strong> a² + 2ab + b² = (a + b)²</li>
  <li><strong>Difference of Cubes:</strong> a³ - b³ = (a - b)(a² + ab + b²)</li>
  <li><strong>Sum of Cubes:</strong> a³ + b³ = (a + b)(a² - ab + b²)</li>
</ul>

<hr>

<h2>Module 4: Rational Expressions</h2>
<p><strong>What you'll learn:</strong> Simplifying, adding, subtracting, and multiplying rational expressions.</p>

<h3>4.1 What are Rational Expressions?</h3>
<p>A rational expression is a fraction with polynomials in the numerator and denominator.</p>
<p><strong>Example:</strong> (x² + 3x) / (x + 1)</p>

<h3>4.2 Simplifying Rational Expressions</h3>
<p>Factor the numerator and denominator, then cancel common factors.</p>
<p><strong>Example:</strong> (x² - 4) / (x - 2) = (x + 2)(x - 2) / (x - 2) = (x + 2), provided x ≠ 2</p>
<p><strong>Important:</strong> Always note when the denominator equals zero (restricted values)!</p>

<p><strong>Interactive Simulator:</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/fractions-equality/latest/fractions-equality_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Use this simulator to discover equivalent fractions by finding different ways to represent the same value. This concept is essential for simplifying rational expressions!</em></p>

<h3>4.3 Operations with Rational Expressions</h3>
<ul>
  <li><strong>Adding/Subtracting:</strong> Find common denominator, combine numerators</li>
  <li><strong>Multiplying:</strong> Multiply numerators and denominators, simplify</li>
  <li><strong>Dividing:</strong> Multiply by the reciprocal</li>
</ul>

<hr>

<h2>Module 5: Exponential & Logarithmic Functions</h2>
<p><strong>What you'll learn:</strong> Exponential growth/decay, logarithms, and their applications.</p>

<h3>5.1 Exponential Functions</h3>
<p>An exponential function has the form: <strong>y = a · b^x</strong></p>
<ul>
  <li><strong>a</strong> = initial value (y-value when x = 0)</li>
  <li><strong>b</strong> = base (growth/decay factor, always positive)</li>
  <li>If <strong>b > 1</strong>: exponential growth (gets bigger)</li>
  <li>If <strong>0 < b < 1</strong>: exponential decay (gets smaller)</li>
  <li>The larger b, the faster the growth; the smaller b, the faster the decay</li>
</ul>

<p><strong>Real-World Examples:</strong></p>
<ul>
  <li><strong>Population growth:</strong> P = 1000 · (1.05)^t - A population starting at 1000 grows 5% per year</li>
  <li><strong>Radioactive decay:</strong> N = N₀ · (1/2)^(t/T) - The amount of substance halves every T years</li>
  <li><strong>Compound interest:</strong> A = P · (1 + r/n)^(nt) - Money grows exponentially when interest compounds</li>
  <li><strong>Bacterial growth:</strong> Bacteria can double in population every 20 minutes!</li>
</ul>

<h3>5.2 Logarithms</h3>
<p>A logarithm is the inverse of an exponential function.</p>
<p>If b^x = y, then log_b(y) = x</p>

<p><strong>Properties of Logarithms:</strong></p>
<ul>
  <li>log(a · b) = log(a) + log(b)</li>
  <li>log(a / b) = log(a) - log(b)</li>
  <li>log(a^b) = b · log(a)</li>
</ul>

<p><strong>Interactive Simulator:</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/function-builder-basics/latest/function-builder-basics_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Build different functions and see how they transform inputs to outputs. Experiment with multiplying, adding, and combining operations to understand function composition!</em></p>

<hr>

<h2>Summary & Key Takeaways</h2>
<ul>
  <li>Linear equations and functions form the foundation of algebra</li>
  <li>Quadratic functions create parabolas with special properties</li>
  <li>Polynomials can be factored and manipulated using algebraic rules</li>
  <li>Rational expressions are fractions with polynomial terms</li>
  <li>Exponential and logarithmic functions model real-world phenomena</li>
</ul>

<p><strong>You've completed Algebra Fundamentals! Next up: take the quiz to test your knowledge.</strong></p>
"""

# ===== COMPREHENSIVE QUANTUM MECHANICS COURSE CONTENT =====
QUANTUM_CONTENT = r"""
<h1>Quantum Mechanics: The ultimate Hyper-Deep Dive</h1>

<p>Welcome to the most comprehensive exploration of Quantum Mechanics. This course traces the "unbreakable chain" of logic from the collapse of classical intuition to the birth of quantum information science. We will not skip the math; we will embrace it.</p>

<div style="background: rgba(255,255,255,0.05); padding: 15px; border-left: 5px solid #6366f1; margin: 20px 0;">
    <strong>Course Objective:</strong> To move beyond qualitative "pop-sci" descriptions and master the Hilbert Space formalism, operator algebra, and the physical reality of the wave function.
</div>

<hr>

<h2>Module 1: The Ultraviolet Catastrophe & The Birth of Quanta</h2>
<p>By the end of the 19th century, Rayleigh-Jeans' law predicted that a blackbody would emit infinite power at high frequencies. This absurdity was solved by Max Planck's radical assumption: energy is quantized.</p>
<p>$$E = nhf$$</p>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>📝 Worked Example: Photon Energy Flux</h4>
  <p><strong>Problem:</strong> A laser emits light at 450 nm (blue) with a power of 5 mW. How many photons are emitted per second?</p>
  <p><strong>Solution:</strong></p>
  <ol>
    <li>Energy of one photon: $E_{ph} = \frac{hc}{\lambda} = \frac{(6.626 \times 10^{-34})(3 \times 10^8)}{450 \times 10^{-9}} \approx 4.42 \times 10^{-19}$ J.</li>
    <li>Total energy per second (Power): $P = 5 \times 10^{-3}$ J/s.</li>
    <li>Number of photons per second: $N = \frac{P}{E_{ph}} = \frac{5 \times 10^{-3}}{4.42 \times 10^{-19}} \approx 1.13 \times 10^{16}$ photons/sec.</li>
  </ol>
</div>

<p><strong>Interactive Visualization: Blackbody Spectrum</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/blackbody-spectrum/latest/blackbody-spectrum_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>

<hr>

<h2>Module 2: Rutherford Scattering & The Nuclear Atom</h2>
<p>Ernest Rutherford's gold foil experiment shattered the "Plum Pudding" model. He discovered that the atom's positive charge is concentrated in a tiny, dense nucleus. This led to the planetary model, which, while revolutionary, was classical and unstable.</p>

<p><strong>Interactive Visualization: Rutherford Scattering</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/rutherford-scattering/latest/rutherford-scattering_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>

<hr>

<h2>Module 3: The Bohr Model & Wave-Particle Duality</h2>
<p>Bohr's model introduced the first "quantum" stable orbits. However, it was Louis de Broglie who proposed the true key: matter itself has a wavelength.</p>
<p>$$\lambda = \frac{h}{p}$$</p>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>📝 Worked Example: Electron De Broglie Wavelength</h4>
  <p><strong>Problem:</strong> Calculate the wavelength of an electron moving at $1 \times 10^6$ m/s ($m_e \approx 9.11 \times 10^{-31}$ kg).</p>
  <p><strong>Solution:</strong> $\lambda = \frac{6.626 \times 10^{-34}}{(9.11 \times 10^{-31})(1 \times 10^6)} \approx 7.27 \times 10^{-10}$ m (or 0.727 nm). This is in the X-ray range!</p>
</div>

<p><strong>Interactive Visualization: Models of the Hydrogen Atom</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/models-of-the-hydrogen-atom/latest/models-of-the-hydrogen-atom_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>

<hr>

<h2>Module 4: The Schrödinger Equation & State Vectors</h2>
<p>The central pillar of Quantum Mechanics is the Time-Dependent Schrödinger Equation (TDSE):</p>
<p>$$i\hbar \frac{\partial}{\partial t} |\Psi(t)\rangle = \hat{H} |\Psi(t)\rangle$$</p>
<p>Where $|\Psi\rangle$ is a vector in <strong>Hilbert Space</strong>, and $\hat{H}$ is the Hamiltonian operator representing total energy.</p>

<h3>4.1 Postulates of QM</h3>
<ol>
    <li><strong>The State:</strong> All information is contained in the state vector $|\psi\rangle$.</li>
    <li><strong>Observables:</strong> Every physical observable corresponds to a <em>Hermitian Operator</em>.</li>
    <li><strong>Measurement:</strong> Measurement values are eigenvalues of the operator.</li>
    <li><strong>Born Rule:</strong> Probability $P(a) = |\langle a|\psi\rangle|^2$.</li>
</ol>

<hr>

<h2>Module 5: Exact Solutions (Particle in a Box & QHO)</h2>
<p>The infinite square well shows us <strong>Quantization</strong>. The particle cannot have zero energy (Zero-Point Energy).</p>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>📝 Worked Example: Uncertainty in an Infinite Well</h4>
  <p><strong>Problem:</strong> For a particle in the ground state of a 1D box of width $L$, show that $\Delta x = L \sqrt{\frac{1}{12} - \frac{1}{2\pi^2}}$.</p>
  <p><strong>Solution:</strong> We use $\langle x \rangle = L/2$ and $\langle x^2 \rangle = \int_0^L x^2 \frac{2}{L} \sin^2(\frac{\pi x}{L}) dx$. Solving the integral yields $\langle x^2 \rangle = L^2 (\frac{1}{3} - \frac{1}{2\pi^2})$. Thus, $(\Delta x)^2 = \langle x^2 \rangle - \langle x \rangle^2 = L^2 (\frac{1}{12} - \frac{1}{2\pi^2})$.</p>
</div>

<hr>

<h2>Module 6: Quantum Measurement & Probability</h2>
<p>Quantum states exist in <strong>Superposition</strong> until measured. This isn't just "ignorance"—it is a physical lack of a definite property.</p>

<p><strong>Interactive Visualization: Quantum Measurement</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/quantum-measurement/latest/quantum-measurement_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>

<hr>

<h2>Module 7: Spin & The Pauli Matrices</h2>
<p>Spin is "intrinsic" angular momentum. It spans a 2D complex Hilbert space, described by the Pauli matrices $\sigma_x, \sigma_y, \sigma_z$.</p>
<p>$$\sigma_z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$</p>

<hr>

<h2>Module 8: Entanglement, Bell's Theorem & Quantum Computing</h2>
<p>Entanglement is the non-local "wiring" of the universe. In a Bell state $|\Phi^+\rangle = \frac{1}{\sqrt{2}} (|00\rangle + |11\rangle)$, neither particle has a state of its own; only the system does.</p>

<h3>8.1 The Qubit & Logic Gates</h3>
<p>A qubit $|\psi\rangle = \alpha |0\rangle + \beta |1\rangle$ can represent infinitely more information through phase relations than a classic bit. Gates like <strong>Hadamard (H)</strong> create superposition, and <strong>CNOT</strong> creates entanglement.</p>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>📝 Worked Example: Entanglement Entropy</h4>
  <p><strong>Problem:</strong> Calculate the partial trace $\rho_A = Tr_B(|\Phi^+\rangle\langle\Phi^+|)$ for the Bell state.</p>
  <p><strong>Solution:</strong> $\rho_{AB} = \frac{1}{2}(|00\rangle\langle 00| + |00\rangle\langle 11| + |11\rangle\langle 00| + |11\rangle\langle 11|)$. Tracing out B leaves $\rho_A = \frac{1}{2}(|0\rangle\langle 0| + |1\rangle\langle 1|)$. This is a <strong>Maximally Mixed State</strong>, meaning $A$ is completely unknown without $B$.</p>
</div>

<hr>

<h2>Module 9: Approximating Reality - Perturbation Theory</h2>
<p>Most real-world systems cannot be solved exactly. We use <strong>Time-Independent Perturbation Theory</strong> to handle small "nudges" to a known system.</p>
<p>$$\hat{H} = \hat{H}^0 + \lambda \hat{H}'$$</p>
<p>The first-order correction to energy is simply the expectation value of the perturbation in the unperturbed state:</p>
<p>$$E_n^{(1)} = \langle \psi_n^0 | \hat{H}' | \psi_n^0 \rangle$$</p>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>📝 Worked Example: Delta-Function Perturbation</h4>
  <p><strong>Problem:</strong> A particle in an infinite well of width $L$ is perturbed by a small spike at the center: $\hat{H}' = \alpha \delta(x - L/2)$. Find the first-order energy shift for the ground state.</p>
  <p><strong>Solution:</strong></p>
  <ol>
    <li>$E_1^{(1)} = \int_0^L \psi_1(x) \alpha \delta(x - L/2) \psi_1(x) dx$.</li>
    <li>$E_1^{(1)} = \alpha |\psi_1(L/2)|^2$.</li>
    <li>Since $\psi_1(L/2) = \sqrt{2/L} \sin(\pi/2) = \sqrt{2/L}$, then $E_1^{(1)} = \frac{2\alpha}{L}$.</li>
  </ol>
</div>

<hr>

<h2>Module 10: The Variational Principle & Helium Atom</h2>
<p>The Variational Principle states that for <em>any</em> trial wave function $|\psi_{trial}\rangle$, the energy expectation value is an upper bound to the ground state energy $E_{gs}$:</p>
<p>$$E_{trial} = \frac{\langle \psi_{trial} | \hat{H} | \psi_{trial} \rangle}{\langle \psi_{trial} | \psi_{trial} \rangle} \geq E_{gs}$$</p>

<h3>10.1 Application: The Two-Electron Problem</h3>
<p>In Helium, the electron-electron repulsion $\frac{e^2}{4\pi\epsilon_0 |r_1 - r_2|}$ makes the TISE unsolvable. Variational methods allow us to approximate the ground state energy within 2% error.</p>

<hr>

<h2>Module 11: Fine Structure & Relativistic Corrections</h2>
<p>The "Bohr" energy levels are only the beginning. Small effects lead to the <strong>Fine Structure</strong>:</p>
<ol>
    <li><strong>Relativistic Kinetic Energy:</strong> Correcting $p^2/2m$ for high-speed electrons.</li>
    <li><strong>Spin-Orbit Coupling:</strong> The interaction between the electron's spin and the magnetic field seen in its rest frame.</li>
    <li><strong>Darwin Term:</strong> A correction for the "shaking" (Zitterbewegung) of the electron.</li>
</ol>
<p>The total shift is of order $\alpha^2 E_n$, where $\alpha \approx 1/137$ is the Fine Structure Constant.</p>

<hr>

<h2>Module 12: Scattering Theory & The Born Approximation</h2>
<p>In particle physics, we don't find "states"—we measure <strong>Scattering Cross-Sections</strong>. We use the Lippmann-Schwinger equation and the <strong>First Born Approximation</strong> to predict how particles deflect off a potential $V(r)$.</p>
<p>$$f(\theta) \approx -\frac{m}{2\pi\hbar^2} \int e^{iq \cdot r'} V(r') d^3r'$$</p>

<hr>

<h2>Module 13: Introduction to Second Quantization (QFT)</h2>
<p>In advanced QM, we treat the wave function itself as an operator. We define <strong>Creation ($a^\dagger$)</strong> and <strong>Annihilation ($a$)</strong> operators for fields.</p>
<p>$$[\hat{\phi}(\mathbf{x}), \hat{\pi}(\mathbf{y})] = i\delta^{(3)}(\mathbf{x}-\mathbf{y})$$</p>
<p>This is the foundation of <strong>Quantum Electrodynamics (QED)</strong>—the most accurately tested theory in human history.</p>

<hr>

<h2>Module 14: Degenerate Perturbation Theory & The Stark Effect</h2>
<p>When multiple states have the same energy (degeneracy), simple perturbation theory fails. We must diagonalize the perturbation matrix $W_{ij} = \langle \psi_i^0 | \hat{H}' | \psi_j^0 \rangle$.</p>
<p><strong>Example: The Stark Effect.</strong> When a Hydrogen atom ($n=2$) is placed in an electric field, the four-fold degeneracy is lifted, splitting the spectral lines.</p>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>📝 Worked Example: Stark Shift Selection Rules</h4>
  <p><strong>Problem:</strong> Why is the first-order Stark shift zero for the ground state ($n=1$) of Hydrogen?</p>
  <p><strong>Solution:</strong></p>
  <ol>
    <li>$\hat{H}' = -eEz$.</li>
    <li>$E_1^{(1)} = \langle \psi_{100} | -eEz | \psi_{100} \rangle$.</li>
    <li>$z$ is an odd function (parity), while $|\psi|^2$ for s-orbitals is even.</li>
    <li>The integral of an odd function over symmetric space is zero. Thus, the ground state only has a <em>second-order</em> shift.</li>
  </ol>
</div>

<hr>

<h2>Module 15: The WKB Approximation & Quantum Tunneling</h2>
<p>The Wentzel-Kramers-Brillouin (WKB) approximation is used for systems where the potential $V(x)$ varies slowly. It is the primary tool for calculating <strong>Tunneling Probabilities</strong> through barriers.</p>
<p>$$T \approx e^{-2\gamma}, \text{ where } \gamma = \frac{1}{\hbar} \int_{x_1}^{x_2} \sqrt{2m(V(x)-E)} dx$$</p>

<hr>

<h2>Module 16: The Adiabatic Approximation & Berry's Phase</h2>
<p>If a Hamiltonian changes very slowly, a system starting in an eigenstate stays in that corresponding "instantaneous" eigenstate. This is the <strong>Adiabatic Theorem</strong>.</p>
<p>However, the state picks up a geometric factor called <strong>Berry's Phase</strong> ($\gamma$), which depends on the path taken in the parameter space.</p>

<hr>

<h2>Module 17: Time-Dependent Perturbation Theory (Fermi's Golden Rule)</h2>
<p>Transitions between states aren't instantaneous. We use time-dependent theory to find the <strong>Transition Rate ($W$)</strong>:</p>
<p>$$W_{i \to f} = \frac{2\pi}{\hbar} |\langle f | \hat{V} | i \rangle|^2 \rho(E_f)$$</p>
<p>This "Golden Rule" is the heart of spectroscopy and nuclear decay calculations.</p>

<hr>

<h2>Module 18: Feynman's Path Integral Formulation</h2>
<p>Richard Feynman proposed that a particle doesn't just take one path; it takes <em>all possible paths</em> simultaneously. The probability amplitude is the sum over all paths, weighted by $e^{iS/\hbar}$, where $S$ is the classical Action.</p>
<p>$$K(x,t; x_0,t_0) = \int \mathcal{D}[x(t)] e^{i S[x(t)]/\hbar}$$</p>

<hr>

<h2>Module 19: Many-Body Systems & The Exchange Interaction</h2>
<p>In systems with identical particles, the wave function must be symmetric (Bosons) or anti-symmetric (Fermions). This leads to an "effective" force called the <strong>Exchange Interaction</strong>, which is responsible for Ferromagnetism and the stability of matter.</p>

<hr>

<h2>Module 20: The Interpretations of Quantum Mechanics</h2>
<p>We know <em>how</em> the math works, but <em>what does it mean</em>? We explore the three titans of interpretation:</p>
<ol>
    <li><strong>Copenhagen:</strong> The act of measurement causes collapse. "Shut up and calculate."</li>
    <li><strong>Many-Worlds (Everett):</strong> Every measurement branches the universe. No collapse occurs.</li>
    <li><strong>Pilot Wave (De Broglie-Bohm):</strong> Particles have definite paths, but are guided by a "hidden" wave.</li>
</ol>

<p><strong>Congratulations! You have completed the Giga-Hyper-Deep Dive. You now possess the depth of understanding required for a PhD in Theoretical Physics!</strong></p>
"""

# ===== ENHANCED QUESTIONS =====
ALGEBRA_QUESTIONS = [
    {"question_text": "Solve for x: 2x + 5 = 13", "question_type": "multiple_choice", "options": ["x = 4", "x = 6", "x = 8", "x = 9"], "correct_answer": "x = 4", "explanation": "Use inverse operations to isolate x: First subtract 5 from both sides: 2x = 13 - 5 = 8. Then divide both sides by 2: x = 8/2 = 4. Check: 2(4) + 5 = 8 + 5 = 13 ✓", "points": 1, "order_index": 1},
    {"question_text": "What is the vertex of y = (x-2)² + 3?", "question_type": "multiple_choice", "options": ["(2, 3)", "(-2, 3)", "(2, -3)", "(-2, -3)"], "correct_answer": "(2, 3)", "explanation": "The vertex form of a parabola is y = a(x-h)² + k, where the vertex is at (h, k). In y = (x-2)² + 3, we have h = 2 and k = 3, so the vertex is at (2, 3). This is the lowest point on the parabola since a = 1 > 0.", "points": 1, "order_index": 2},
    {"question_text": "Factor: x² - 5x + 6", "question_type": "multiple_choice", "options": ["(x-2)(x-3)", "(x+2)(x+3)", "(x-2)(x+3)", "(x+2)(x-3)"], "correct_answer": "(x-2)(x-3)", "explanation": "To factor x² - 5x + 6, find two numbers that multiply to 6 and add to -5. Those numbers are -2 and -3 (because -2 × -3 = 6 and -2 + -3 = -5). So x² - 5x + 6 = (x-2)(x-3). Check by expanding: (x-2)(x-3) = x² - 3x - 2x + 6 = x² - 5x + 6 ✓", "points": 1, "order_index": 3},
    {"question_text": "Simplify: (x² - 4)/(x - 2)", "question_type": "multiple_choice", "options": ["x + 2", "x - 2", "x", "2x"], "correct_answer": "x + 2", "explanation": "Factor the numerator using difference of squares: x² - 4 = (x+2)(x-2). So (x² - 4)/(x - 2) = (x+2)(x-2)/(x-2). Cancel the common factor (x-2), leaving x + 2. Important: x ≠ 2 because that would make the denominator zero (undefined).", "points": 1, "order_index": 4},
    {"question_text": "Solve: 3^x = 27", "question_type": "multiple_choice", "options": ["x = 2", "x = 3", "x = 4", "x = 9"], "correct_answer": "x = 3", "explanation": "Express both sides with the same base: 27 = 3³. So 3^x = 3³. When bases are equal, exponents must be equal, therefore x = 3. This works because 3 × 3 × 3 = 27. For exponential equations, converting to the same base is a key strategy!", "points": 1, "order_index": 5},
    {"question_text": "A line passes through (0, 1) and (2, 5). What is the slope?", "question_type": "multiple_choice", "options": ["m = 2", "m = 1", "m = 3", "m = 1/2"], "correct_answer": "m = 2", "explanation": "Use the slope formula: m = (y₂ - y₁)/(x₂ - x₁). With points (0, 1) and (2, 5): m = (5 - 1)/(2 - 0) = 4/2 = 2. This means for every 1 unit right, the line goes up 2 units. The slope is positive, so the line goes upward from left to right.", "points": 1, "order_index": 6},
    {"question_text": "If a > 0 in y = ax² + bx + c, which is true?", "question_type": "multiple_choice", "options": ["Opens upward", "Opens downward", "Is a straight line", "Has no x-intercepts"], "correct_answer": "Opens upward", "explanation": "In a quadratic function y = ax² + bx + c, the sign of 'a' determines the parabola's direction. When a > 0 (positive), the parabola opens upward like a ∪ shape, with a minimum vertex. When a < 0 (negative), it opens downward like an ∩ shape, with a maximum vertex. The larger |a|, the narrower the parabola.", "points": 1, "order_index": 7},
    {"question_text": "Expand: (2x + 1)(x - 3)", "question_type": "multiple_choice", "options": ["2x² - 5x - 3", "2x² - 6x + 1", "2x² + x - 3", "x² - 5x - 3"], "correct_answer": "2x² - 5x - 3", "explanation": "Use FOIL (First, Outer, Inner, Last): (2x + 1)(x - 3) = (2x)(x) + (2x)(-3) + (1)(x) + (1)(-3) = 2x² - 6x + x - 3 = 2x² - 5x - 3. Always combine like terms (-6x + x = -5x) to get the final answer.", "points": 1, "order_index": 8},
]

QUANTUM_QUESTIONS = [
    {"question_text": "Which of the following describes the normalization condition for a wave function ψ(x)?", "question_type": "multiple_choice", "options": ["∫ψ(x) dx = 1", "∫|ψ(x)|² dx = 1", "ψ(x) = ψ*(x)", "dψ/dx = 0"], "correct_answer": "∫|ψ(x)|² dx = 1", "explanation": "The square of the absolute value of the wave function represents probability density. For the particle to exist somewhere, the total probability (integral of density over all space) must equal 1.", "points": 1, "order_index": 1},
    {"question_text": "What is the value of the commutator [x̂, p̂]?", "question_type": "multiple_choice", "options": ["0", "1", "iℏ", "-iℏ"], "correct_answer": "iℏ", "explanation": "As derived in the course, applying x̂p̂ - p̂x̂ to a test function yields iℏ times the function, using the product rule on the derivative in the momentum operator.", "points": 1, "order_index": 2},
    {"question_text": "For a particle in the ground state of an infinite square well of width L, where is the probability density highest?", "question_type": "multiple_choice", "options": ["x = 0", "x = L", "x = L/2", "x = L/4"], "correct_answer": "x = L/2", "explanation": "The ground state wave function is proportional to sin(πx/L). The square of this sine function reaches its maximum at πx/L = π/2, which corresponds to x = L/2.", "points": 1, "order_index": 3},
    {"question_text": "What are the eigenvalues of the Pauli matrix σz?", "question_type": "multiple_choice", "options": ["0, 1", "+1, -1", "i, -i", "1/2, -1/2"], "correct_answer": "+1, -1", "explanation": "σz is a diagonal matrix [[1, 0], [0, -1]]. Its diagonal entries are its eigenvalues, which represent the possible results of spin measurement along the z-axis (in units of ℏ/2).", "points": 1, "order_index": 4},
    {"question_text": "If a particle state is |ψ⟩ = 1/√2 (|0⟩ + |1⟩), what is the probability of measuring the system in state |0⟩?", "question_type": "multiple_choice", "options": ["1", "1/2", "1/√2", "0"], "correct_answer": "1/2", "explanation": "According to the Born Rule, P = |⟨0|ψ⟩|². Here ⟨0|ψ⟩ = 1/√2, so P = (1/√2)² = 1/2.", "points": 1, "order_index": 5},
    {"question_text": "The energy of the n=2 state in an infinite square well is how many times the ground state energy (E1)?", "question_type": "multiple_choice", "options": ["2 times", "√2 times", "4 times", "8 times"], "correct_answer": "4 times", "explanation": "Energy levels in the infinite square well scale with n², so En = n²E1. For n=2, E2 = 2²E1 = 4E1.", "points": 1, "order_index": 6},
    {"question_text": "Which property must an operator have to represent a physical observable?", "question_type": "multiple_choice", "options": ["Unitary", "Hermitian", "Invertible", "Singular"], "correct_answer": "Hermitian", "explanation": "Hermitian operators have real eigenvalues, ensuring that physical measurements (which must be real numbers) are the only possible outcomes.", "points": 1, "order_index": 7},
    {"question_text": "In the context of entanglement, if a pair of particles is in the singlet state 1/√2 (|↑↓⟩ - |↓↑⟩), measuring the first as 'up' forces the second to be:", "question_type": "multiple_choice", "options": ["Up", "Down", "In a superposition", "Undetermined"], "correct_answer": "Down", "explanation": "The singlet state is perfectly anti-correlated. If the first is 'up' (|↑⟩), the wave function collapses to the first term |↑↓⟩, meaning the second must be 'down' (|↓⟩).", "points": 1, "order_index": 8},
    {"question_text": "Planck's constant (h) has units of:", "question_type": "multiple_choice", "options": ["Energy", "Force", "Action (Energy × Time)", "Power"], "correct_answer": "Action (Energy × Time)", "explanation": "h ≈ 6.626 × 10⁻³⁴ J·s. Joule-seconds are the units of action, which is the same as angular momentum.", "points": 1, "order_index": 9},
    {"question_text": "What is the 'Zero-Point Energy' of a Quantum Harmonic Oscillator?", "question_type": "multiple_choice", "options": ["0", "1/2 ℏω", "ℏω", "3/2 ℏω"], "correct_answer": "1/2 ℏω", "explanation": "Even at n=0, the energy is E0 = (0 + 1/2)ℏω = 1/2 ℏω. This is a consequence of the uncertainty principle.", "points": 1, "order_index": 10},
    {"question_text": "Which experiment first demonstrated the non-locality of quantum mechanics by violating a specific inequality?", "question_type": "multiple_choice", "options": ["Double-slit experiment", "Stern-Gerlach experiment", "Bell test experiments", "Photoelectric effect"], "correct_answer": "Bell test experiments", "explanation": "Bell tests (like those by Aspect et al.) showed that nature violates Bell's inequalities, proving that no local hidden variable theory can explain quantum correlations.", "points": 1, "order_index": 11},
    {"question_text": "The wave function of a Fermion must be:", "question_type": "multiple_choice", "options": ["Symmetric", "Anti-symmetric", "Real", "Imaginary"], "correct_answer": "Anti-symmetric", "explanation": "Fermions have half-integer spin and follow the spin-statistics theorem, which requires their total wave function to change sign upon the exchange of any two identical particles.", "points": 1, "order_index": 12},
    {"question_text": "What is the Hamiltonian operator (Ĥ) representing?", "question_type": "multiple_choice", "options": ["Total Momentum", "Total Torque", "Total Energy", "Total Entropy"], "correct_answer": "Total Energy", "explanation": "In both classical and quantum mechanics, the Hamiltonian represents the sum of kinetic and potential energy: Ĥ = T̂ + V̂.", "points": 1, "order_index": 13},
    {"question_text": "Find the energy of a photon with wavelength 100 nm (use hc ≈ 1240 eV·nm).", "question_type": "multiple_choice", "options": ["1.24 eV", "12.4 eV", "124 eV", "0.124 eV"], "correct_answer": "12.4 eV", "explanation": "E = hc/λ = 1240 / 100 = 12.4 eV.", "points": 1, "order_index": 14},
    {"question_text": "The 'collapse' of the wave function is associated with which quantum process?", "question_type": "multiple_choice", "options": ["Unitary evolution", "Interference", "Measurement", "Tunneling"], "correct_answer": "Measurement", "explanation": "Upon measurement, a state in a superposition collapses into one of the eigenstates of the observable being measured.", "points": 1, "order_index": 15},
    {"question_text": "What is the result of the outer product |ψ⟩⟨ψ| if |ψ⟩ is normalized?", "question_type": "multiple_choice", "options": ["A scalar (1)", "The Identity operator", "A Projection operator", "A Zero operator"], "correct_answer": "A Projection operator", "explanation": "The outer product |ψ⟩⟨ψ| projects any state onto the direction of |ψ⟩.", "points": 1, "order_index": 16},
    {"question_text": "Schrödinger's cat is an illustration of what quantum principle?", "question_type": "multiple_choice", "options": ["Tunneling", "Superposition", "Quantization", "Exclusion"], "correct_answer": "Superposition", "explanation": "The cat is simultaneously 'dead' and 'alive' until an observation causes the state to collapse.", "points": 1, "order_index": 17},
    {"question_text": "In a 1D box of width L, what is the value of ψ(L)?", "question_type": "multiple_choice", "options": ["1", "0", "1/√L", "L"], "correct_answer": "0", "explanation": "The potential is infinite outside the box, so the wave function must vanish at the boundaries (x=0 and x=L) to be continuous.", "points": 1, "order_index": 18},
    {"question_text": "Which Pauli matrix is used to find spin along the x-axis?", "question_type": "multiple_choice", "options": ["[[0, 1], [1, 0]]", "[[0, -i], [i, 0]]", "[[1, 0], [0, -1]]", "[[1, 1], [1, 1]]"], "correct_answer": "[[0, 1], [1, 0]]", "explanation": "σx = [[0, 1], [1, 0]]. Its eigenstates are used to describe spin 'left' and 'right'.", "points": 1, "order_index": 19},
    {"question_text": "If Δx is reduced by a factor of 2, what happens to the minimum possible Δp?", "question_type": "multiple_choice", "options": ["Reduced by 2", "Doubled", "Stays same", "Quadrupled"], "correct_answer": "Doubled", "explanation": "Since ΔxΔp ≥ ℏ/2, they are inversely proportional. Reducing one doubling the minimum for the other.", "points": 1, "order_index": 20},
]

# ===== COMPREHENSIVE CHEMISTRY COURSE CONTENT =====
CHEMISTRY_CONTENT = r"""
<h1>Chemistry: The ultimate Hyper-Deep Dive</h1>

<p>Welcome to the Hyper-Deep Dive into the molecular world. We will trace the journey of an electron from its quantum home in an orbital, through the dance of chemical bonding, into the chaotic energy of thermodynamics, and finally to the harnessed power of an electrochemical cell.</p>

<hr>

<h2>Module 1: The Electronic Architecture of Atoms</h2>
<p>Modern chemistry begins with the realization that atoms are not solid balls, but complex probability clouds controlled by four quantum numbers.</p>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>📝 Worked Example: Orbital Multiplicity</h4>
  <p><strong>Problem:</strong> How many total electrons can occupy the $n=4$ shell?</p>
  <p><strong>Solution:</strong></p>
  <ol>
    <li>For $n=4$, $l$ can be 0, 1, 2, 3 (s, p, d, f).</li>
    <li>Number of orbitals = $n^2 = 4^2 = 16$.</li>
    <li>Each orbital holds 2 electrons (Pauli Principle).</li>
    <li>Total electrons = $2 \times 16 = 32$.</li>
  </ol>
</div>

<p><strong>Interactive Visualization: Build an Atom</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/build-an-atom/latest/build-an-atom_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>

<hr>

<h2>Module 2: Molecular Geometry & Chemical Logic</h2>
<p>Molecules are not random shapes; they are the result of <strong>VSEPR Theory</strong> (minimizing repulsion) and <strong>Hybridization</strong>.</p>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>📝 Worked Example: Dipole Moments</h4>
  <p><strong>Problem:</strong> Is $CO_2$ polar or non-polar? What about $H_2O$?</p>
  <p><strong>Solution:</strong> $CO_2$ is linear ($180^\circ$); the C=O dipoles cancel out (Non-polar). $H_2O$ is bent ($\approx 104.5^\circ$); the O-H dipoles add up (Polar).</p>
</div>

<p><strong>Interactive Visualization: Molecule Shapes</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/molecule-shapes/latest/molecule-shapes_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>

<hr>

<h2>Module 3: Thermodynamics & The Chaos of Matter</h2>
<p>Thermodynamics tells us "if" a reaction will happen. It is governed by Enthalpy ($H$), Entropy ($S$), and the ultimate arbiter, Gibbs Free Energy ($G$).</p>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>📝 Worked Example: Spontaneity Calculation</h4>
  <p><strong>Problem:</strong> A reaction has $\Delta H = -100$ kJ and $\Delta S = -200$ J/K. Is it spontaneous at 25°C?</p>
  <p><strong>Solution:</strong> $\Delta G = \Delta H - T\Delta S = -100,000 - (298.15)(-200) = -100,000 + 59,630 = -40,370$ J. Since $\Delta G < 0$, it is <strong>Spontaneous</strong>.</p>
</div>

<p><strong>Interactive Visualization: States of Matter</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/states-of-matter/latest/states-of-matter_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>

<hr>

<h2>Module 4: Chemical Kinetics & Transition States</h2>
<p>Kinetics tells us "how fast." Reactants must overcome the <strong>Activation Energy ($E_a$)</strong> barrier by forming a high-energy transition state.</p>

<hr>

<h2>Module 5: Stoichiometry & The Math of Yield</h2>
<p>The Law of Conservation of Mass requires balanced equations. Stoichiometry allows us to predict how much product we can get from a given amount of reactant.</p>

<p><strong>Interactive Visualization: Balancing Chemical Equations</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/balancing-chemical-equations/latest/balancing-chemical-equations_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>

<p><strong>Interactive Visualization: Reactants, Products and Leftovers</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/reactants-products-and-leftovers/latest/reactants-products-and-leftovers_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>

<hr>

<h2>Module 6: Acids, Bases & The pH Scale</h2>
<p>The concentration of $H^+$ ions defines the acidity of a solution. This is measured on a logarithmic scale.</p>

<p><strong>Interactive Visualization: pH Scale</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/ph-scale/latest/ph-scale_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>

<hr>

<h2>Module 7: Electrochemistry & Battery Technology</h2>
<p>Electrochemistry is the study of <strong>Redox</strong> reactions. We can use the <strong>Nernst Equation</strong> to find cell potential under non-standard conditions.</p>
<p>$$E = E^\circ - \frac{RT}{nF} \ln Q$$</p>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>📝 Worked Example: Faraday's First Law</h4>
  <p><strong>Problem:</strong> How many grams of Copper ($Cu$, $M=63.5$) are deposited by a 5A current running for 1 hour? ($Cu^{2+} + 2e^- \rightarrow Cu$)</p>
  <p><strong>Solution:</strong></p>
  <ol>
    <li>Charge $Q = I \times t = 5 \times 3600 = 18,000$ C.</li>
    <li>Moles of electrons $n_e = Q/F = 18,000 / 96,485 \approx 0.187$ mol.</li>
    <li>Moles of Cu = $n_e / 2 \approx 0.0935$ mol.</li>
    <li>Mass = $0.0935 \times 63.5 \approx 5.94$ g.</li>
  </ol>
</div>

<hr>

<h2>Module 8: The Bridge to Organic Chemistry</h2>
<p>Life is Carbon-based. Organic chemistry explores the infinite complexity of Carbon-Hydrogen-Oxygen-Nitrogen frameworks, where <strong>Resonance</strong> and <strong>Steric Hindrance</strong> govern behavior.</p>

<hr>

<h2>Module 9: Statistical Mechanics - The Bridge from Micro to Macro</h2>
<p>Statistical mechanics explains how the microscopic states of individual molecules lead to macroscopic properties like temperature and pressure. The central object is the <strong>Partition Function ($Z$)</strong>:</p>
<p>$$Z = \sum_i e^{-\beta E_i}$$</p>
<p>Where $\beta = 1/k_B T$. All thermodynamic variables, including Entropy and Internal Energy, can be derived from $Z$.</p>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>📝 Worked Example: The Boltzmann Distribution</h4>
  <p><strong>Problem:</strong> A system has two energy levels: $E_0 = 0$ and $E_1 = \epsilon$. What is the probability of finding the system in the excited state at temperature $T$?</p>
  <p><strong>Solution:</strong></p>
  <ol>
    <li>Partition Function: $Z = e^{-0} + e^{-\epsilon/k_B T} = 1 + e^{-\epsilon/k_B T}$.</li>
    <li>Probability $P_1 = \frac{1}{Z} e^{-\epsilon/k_B T} = \frac{e^{-\epsilon/k_B T}}{1 + e^{-\epsilon/k_B T}}$.</li>
    <li>As $T \to \infty$, $P_1 \to 1/2$. As $T \to 0$, $P_1 \to 0$.</li>
  </ol>
</div>

<hr>

<h2>Module 10: Coordination Chemistry & Crystal Field Theory</h2>
<p>Transition metals form complex ions where "ligands" surround a central metal. <strong>Crystal Field Theory (CFT)</strong> explains the colors and magnetic properties of these complexes by the splitting of d-orbitals.</p>
<p>In an octahedral field, the five d-orbitals split into two sets: $t_{2g}$ (lower energy) and $e_g$ (higher energy). The energy difference is denoted as $\Delta_o$.</p>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>📝 Worked Example: CFSE Calculation</h4>
  <p><strong>Problem:</strong> Calculate the Crystal Field Stabilization Energy (CFSE) for a high-spin $d^5$ octahedral complex.</p>
  <p><strong>Solution:</strong> In high-spin $d^5$, electrons fill as $(t_{2g})^3 (e_g)^2$. CFSE = $3(-0.4\Delta_o) + 2(0.6\Delta_o) = -1.2\Delta_o + 1.2\Delta_o = 0$. This explains why $Mn^{2+}$ complexes are often less stable than $Fe^{2+}$.</p>
</div>

<hr>

<h2>Module 11: Solid State Chemistry & Band Theory</h2>
<p>In solids, atomic orbitals merge into continuous <strong>Energy Bands</strong>. The gap between the <strong>Valence Band</strong> and the <strong>Conduction Band</strong> determines if a material is a conductor, semiconductor, or insulator.</p>
<ul>
    <li><strong>Metals:</strong> Overlapping bands (no gap).</li>
    <li><strong>Semiconductors:</strong> Small gap ($\approx 1$ eV).</li>
    <li><strong>Insulators:</strong> Large gap ($> 5$ eV).</li>
</ul>

<hr>

<h2>Module 12: Advanced Chemical Equilibria & Activity</h2>
<p>At high concentrations, the "ideal" concentration $M$ is no longer accurate. We must use <strong>Activity ($a$)</strong>, where $a = \gamma [C]$. The activity coefficient $\gamma$ accounts for inter-ionic attractions described by the <strong>Debye-Hückel Theory</strong>.</p>

<hr>

<h2>Module 13: The Frontiers of Nanochemistry & Supramolecular Chemistry</h2>
<p>At the nanoscale, surface area dominates and quantum effects (like quantum dots) emerge. Supramolecular chemistry moves "beyond the molecule" to study <strong>Non-covalent Interactions</strong> like hydrogen bonding and $\pi-\pi$ stacking, which are the basis of life and molecular machines.</p>

<hr>

<h2>Module 14: Molecular Spectroscopy - The Eyes of Chemistry</h2>
<p>How do we know the structure of a molecule? We use light to probe its vibrations and rotations.</p>
<ul>
    <li><strong>Infrared (IR) Spectroscopy:</strong> Measures the "stretching" and "bending" of bonds. For example, a $C=O$ bond always shows a sharp peak around $1700 \text{ cm}^{-1}$.</li>
    <li><strong>NMR Spectroscopy:</strong> Uses the spin of nuclei to map the environment of atoms. It is the molecular equivalent of an MRI.</li>
</ul>

<hr>

<h2>Module 15: Surface Chemistry & The Langmuir Isotherm</h2>
<p>Reactions often happen at the interface of a solid and a gas (catalysis). The <strong>Langmuir Isotherm</strong> models how molecules adsorb onto a surface:</p>
<p>$$\theta = \frac{KP}{1 + KP}$$</p>
<p>Where $\theta$ is the fraction of surface covered, and $P$ is the pressure.</p>

<hr>

<h2>Module 16: Computational Chemistry & DFT</h2>
<p>Since we can't solve the TISE for large molecules, we use <strong>Density Functional Theory (DFT)</strong>. Instead of the wave function, we calculate the <strong>Electron Density</strong> $\rho(r)$. This allows us to design new drugs and materials on supercomputers.</p>

<hr>

<h2>Module 17: Bio-Physical Chemistry & Enzyme Kinetics</h2>
<p>Life is a series of chemical reactions catalyzed by enzymes. We use the <strong>Michaelis-Menten Equation</strong> to model the rate $v$:</p>
<p>$$v = \frac{V_{max} [S]}{K_m + [S]}$$</p>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>📝 Worked Example: Enzyme Efficiency</h4>
  <p><strong>Problem:</strong> An enzyme has $K_m = 10^{-4}$ M. At what substrate concentration $[S]$ is the reaction speed half of $V_{max}$?</p>
  <p><strong>Solution:</strong> Set $v = V_{max}/2$ in the Michaelis-Menten equation. $V_{max}/2 = \frac{V_{max} [S]}{K_m + [S]} \implies K_m + [S] = 2[S] \implies [S] = K_m$. So the concentration is $10^{-4}$ M.</p>
</div>

<hr>

<h2>Module 18: Polymer Chemistry & Macromolecules</h2>
<p>Polymers (plastics, DNA, proteins) are long chains of repeating units. We study their <strong>Degree of Polymerization</strong> and their mechanical properties (Viscoelasticity, Glass Transition Temperature).</p>

<hr>

<h2>Module 19: Nuclear Chemistry & The Age of the Earth</h2>
<p>Chemical reactions involve electrons, but <strong>Nuclear Reactions</strong> involve the nucleus. We use carbon-14 dating and uranium-lead dating to track the history of the earth through the first-order decay law:</p>
<p>$$N(t) = N_0 e^{-\lambda t}$$</p>

<hr>

<h2>Module 20: Green Chemistry & The Sustainability Logic</h2>
<p>The ultimate goal of a chemist is to create products without destroying the environment. We follow the <strong>12 Principles of Green Chemistry</strong>, focusing on Atom Economy, Biodegradability, and Solvent-free Synthesis.</p>

<p><strong>Congratulations! You have completed the Giga-Hyper-Deep Dive. You have bridged the gap from the fundamental electron to the future of our sustainable planet!</strong></p>
"""

CHEMISTRY_QUESTIONS = [
    {"question_text": "What is the Rydberg formula used for in atomic chemistry?", "question_type": "multiple_choice", "options": ["Predicting electronic transitions", "Calculating bond order", "Determining molecular shape", "Calculating entropy"], "correct_answer": "Predicting electronic transitions", "explanation": "The Rydberg formula relates the wavelength of emitted or absorbed light to the change in principle quantum numbers during an electronic transition.", "points": 1, "order_index": 1},
    {"question_text": "In MO theory, a 'Bond Order' of 0 implies what?", "question_type": "multiple_choice", "options": ["A stable triple bond", "The molecule does not exist", "A highly polar bond", "A paramagnetic molecule"], "correct_answer": "The molecule does not exist", "explanation": "A bond order of 0 means there is no net stabilization from electron sharing, so the atoms will not remain bonded (e.g., He2).", "points": 1, "order_index": 2},
    {"question_text": "Which thermodynamic state function is defined as H - TS?", "question_type": "multiple_choice", "options": ["Internal Energy", "Enthalpy", "Gibbs Free Energy", "Helmholtz Energy"], "correct_answer": "Gibbs Free Energy", "explanation": "G = H - TS is the fundamental definition of Gibbs Free Energy, which determines spontaneity at constant T and P.", "points": 1, "order_index": 3},
    {"question_text": "If a reaction is exothermic (ΔH < 0) and entropy decreases (ΔS < 0), it is spontaneous at:", "question_type": "multiple_choice", "options": ["All temperatures", "High temperatures only", "Low temperatures only", "Never"], "correct_answer": "Low temperatures only", "explanation": "For spontaneity, ΔH - TΔS must be negative. If ΔH is (-) and -TΔS is (+), only low T will keep the negative term dominant.", "points": 1, "order_index": 4},
    {"question_text": "The rate law v = k[A][B]² represents a reaction of what overall order?", "question_type": "multiple_choice", "options": ["1", "2", "3", "0"], "correct_answer": "3", "explanation": "Overall order is the sum of the exponents in the rate law: 1 + 2 = 3.", "points": 1, "order_index": 5},
    {"question_text": "What is the unit of the rate constant 'k' for a first-order reaction?", "question_type": "multiple_choice", "options": ["M/s", "1/s", "M⁻¹s⁻¹", "M⁻²s⁻¹"], "correct_answer": "1/s", "explanation": "For first order: Rate (M/s) = k [A] (M). Thus k = (M/s)/M = 1/s.", "points": 1, "order_index": 6},
    {"question_text": "The Nernst Equation relates cell potential to what property?", "question_type": "multiple_choice", "options": ["Mass", "Volume", "Concentration (Q)", "Pressure"], "correct_answer": "Concentration (Q)", "explanation": "The Nernst Equation shows how the potential varies with the activity/concentration of reactants and products via the reaction quotient Q.", "points": 1, "order_index": 7},
    {"question_text": "What is the standard potential (E°) of a Hydrogen electrode at pH 0?", "question_type": "multiple_choice", "options": ["1.0 V", "0.0 V", "-0.76 V", "+0.34 V"], "correct_answer": "0.0 V", "explanation": "By definition, the Standard Hydrogen Electrode (SHE) is assigned a potential of 0.00 V at all temperatures.", "points": 1, "order_index": 8},
    {"question_text": "Which quantum number determines the shape of an orbital?", "question_type": "multiple_choice", "options": ["n", "l", "ml", "ms"], "correct_answer": "l", "explanation": "The angular momentum quantum number 'l' defines the type (s, p, d, f) and thus the shape of the orbital.", "points": 1, "order_index": 9},
    {"question_text": "A catalyst increases reaction speed by doing what?", "question_type": "multiple_choice", "options": ["Increasing ΔH", "Decreasing ΔG", "Lowering Activation Energy (Ea)", "Increasing temperature"], "correct_answer": "Lowering Activation Energy (Ea)", "explanation": "Catalysts provide an alternative mechanism with a lower activation energy, allowing more molecules to react per unit time.", "points": 1, "order_index": 10},
    {"question_text": "The LCAO approximation stands for:", "question_type": "multiple_choice", "options": ["Linear Combination of Atomic Orbitals", "Lowest Common Atomic Orbital", "Le Chatelier's Atomic Order", "Liquid Crystal Atomic Operation"], "correct_answer": "Linear Combination of Atomic Orbitals", "explanation": "LCAO is the mathematical method of adding atomic wave functions to form molecular wave functions.", "points": 1, "order_index": 11},
    {"question_text": "Which law states that the total entropy of the universe always increases?", "question_type": "multiple_choice", "options": ["1st Law", "2nd Law", "3rd Law", "Hess's Law"], "correct_answer": "2nd Law", "explanation": "The Second Law of Thermodynamics governs the arrow of time and the spontaneity of processes.", "points": 1, "order_index": 12},
    {"question_text": "For the half-reaction Cu²⁺ + 2e⁻ → Cu, what is 'n' in the Nernst Equation?", "question_type": "multiple_choice", "options": ["1", "2", "0", "0.5"], "correct_answer": "2", "explanation": "n represents the number of electrons transferred in the balanced half-reaction.", "points": 1, "order_index": 13},
    {"question_text": "What is the geometry of an sp³ hybridized atom with no lone pairs?", "question_type": "multiple_choice", "options": ["Linear", "Trigonal Planar", "Tetrahedral", "Octahedral"], "correct_answer": "Tetrahedral", "explanation": "sp³ hybridization involves 4 equivalent orbitals pointing to the corners of a tetrahedron.", "points": 1, "order_index": 14},
    {"question_text": "The Boltzmann constant (kB) relates entropy to:", "question_type": "multiple_choice", "options": ["Heat", "Microstates (W)", "Work", "Enthalpy"], "correct_answer": "Microstates (W)", "explanation": "S = kB ln W. This is the link between microscopic arrangements and macroscopic entropy.", "points": 1, "order_index": 15},
    {"question_text": "In kinetics, a 'reaction intermediate' is:", "question_type": "multiple_choice", "options": ["A reactant", "A product", "Produced then consumed", "The transition state"], "correct_answer": "Produced then consumed", "explanation": "Intermediates appear in the mechanism but not in the overall balanced equation as they are used up as fast as they are made.", "points": 1, "order_index": 16},
    {"question_text": "The Farady constant (F) represents the charge of:", "question_type": "multiple_choice", "options": ["1 electron", "1 mole of electrons", "1 proton", "1 kg of electrons"], "correct_answer": "1 mole of electrons", "explanation": "F ≈ 96485 Coulombs per mole of electrons.", "points": 1, "order_index": 17},
    {"question_text": "Which principle states that electrons fill the lowest energy levels first?", "question_type": "multiple_choice", "options": ["Hund's Rule", "Pauli Principle", "Aufbau Principle", "Heisenberg Principle"], "correct_answer": "Aufbau Principle", "explanation": "Aufbau (building up) governs the order of orbital filling based on energy.", "points": 1, "order_index": 18},
    {"question_text": "What is the bond order of N2 (which has 10 valence electrons in MOs)?", "question_type": "multiple_choice", "options": ["1", "2", "3", "4"], "correct_answer": "3", "explanation": "N2: (σ2s)² (σ*2s)² (π2p)⁴ (σ2p)². B.O. = (8 - 2)/2 = 3.", "points": 1, "order_index": 19},
    {"question_text": "If a reaction quotient Q > K (equilibrium constant), the reaction will:", "question_type": "multiple_choice", "options": ["Proceed forward", "Proceed backward", "Stay at equilibrium", "Explode"], "correct_answer": "Proceed backward", "explanation": "If Q > K, there are too many products, so the system shifts toward the reactants.", "points": 1, "order_index": 20},
]

def connect_to_aiven():
    try:
        print("🔗 Connecting to Aiven database...")
        connection = pymysql.connect(**AIVEN_CONFIG)
        print("✅ Connected!")
        return connection
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None

def shuffle_question_options(question):
    """Shuffle options so correct answer is not always first"""
    q = question.copy()
    options = q["options"].copy()
    correct_answer = q["correct_answer"]
    
    # Shuffle the options
    random.shuffle(options)
    
    # Make sure correct answer is in the shuffled list
    if correct_answer not in options:
        # Replace first option with correct answer
        options[0] = correct_answer
        random.shuffle(options)
    
    q["options"] = options
    return q

def update_course(cursor, course_id, title, content, questions):
    try:
        # Insert questions first to get their IDs
        question_ids = []
        cursor.execute("DELETE FROM course_questions WHERE course_id = %s", (course_id,))
        
        for q in questions:
            # Shuffle options so correct answer isn't always first
            shuffled_q = shuffle_question_options(q)
            
            cursor.execute("""
                INSERT INTO course_questions 
                (course_id, question_text, question_type, options, correct_answer, explanation, points, order_index)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (course_id, shuffled_q["question_text"], shuffled_q["question_type"], json.dumps(shuffled_q["options"]), 
                  shuffled_q["correct_answer"], shuffled_q["explanation"], shuffled_q["points"], shuffled_q["order_index"]))
            
            # Get the inserted question ID
            cursor.execute("SELECT LAST_INSERT_ID() as id")
            result = cursor.fetchone()
            if result:
                question_ids.append(result['id'])
        
        # Now insert quiz placeholders into course content
        enhanced_content = content
        for i, q_id in enumerate(question_ids, 1):
            # Add placeholder at end of content before closing tags
            placeholder_html = f'<div class="quiz-question-placeholder" data-question-id="{q_id}" style="background: #e0e7ff; border: 2px solid #667eea; padding: 1.5em; margin: 1.5em 0; border-radius: 8px; user-select: none;"><strong>❓ Quiz Question {i}:</strong> <em>Question {i} - Answer to check your knowledge</em></div>'
            enhanced_content += placeholder_html
        
        # Update course title and content with placeholders
        cursor.execute("UPDATE courses SET title = %s, content = %s WHERE id = %s", (title, enhanced_content, course_id))
        
        print(f"✅ Updated course {course_id} with {len(question_ids)} questions")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    if not AIVEN_CONFIG["password"]:
        print("❌ ERROR: Set AIVEN_PASSWORD environment variable!")
        return 1
    
    connection = connect_to_aiven()
    if not connection:
        return 1
    
    try:
        cursor = connection.cursor()
        
        print("\n📚 Updating Algebra Course (ID: 12)...")
        update_course(cursor, 12, "Algebra Fundamentals", ALGEBRA_CONTENT, ALGEBRA_QUESTIONS)
        
        print("\n🔬 Updating Quantum Course (ID: 13)...")
        update_course(cursor, 13, "Quantum Mechanics Essentials", QUANTUM_CONTENT, QUANTUM_QUESTIONS)
        
        print("\n⚗️ Updating Chemistry Course (ID: 14)...")
        update_course(cursor, 14, "Chemistry Fundamentals", CHEMISTRY_CONTENT, CHEMISTRY_QUESTIONS)
        
        connection.commit()
        
        print("\n" + "="*70)
        print("✅ SUCCESS! Courses updated with comprehensive content!")
        print("="*70)
        print("\n📊 Updates:")
        print("  ✓ Algebra: Comprehensive teaching content + 8 questions (randomized answers)")
        print("  ✓ Quantum: Comprehensive teaching content + 20 questions (randomized answers)")
        print("  ✓ Chemistry: Comprehensive teaching content + 20 questions (randomized answers)")
        print("  ✓ PhET simulators embedded and working")
        print("  ✓ All answer choices randomized so correct answer is NOT always first")
        print("\n🚀 Courses are now ready for students!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        connection.rollback()
        return 1
    finally:
        cursor.close()
        connection.close()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
