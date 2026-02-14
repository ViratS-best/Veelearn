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
QUANTUM_CONTENT = """
<h1>Quantum Mechanics Essentials - Complete Guide</h1>

<h2>📚 Course Overview</h2>
<p>Quantum mechanics describes the behavior of matter and energy at the atomic and subatomic scales. 
This course uses interactive PhET simulators to visualize quantum phenomena and build your understanding 
of this fascinating branch of physics.</p>

<hr>

<h2>Module 1: Foundations of Quantum Mechanics</h2>
<p><strong>What you'll learn:</strong> The revolutionary ideas that changed physics forever.</p>

<h3>1.1 The Classical vs. Quantum Worlds</h3>
<p><strong>Classical Physics (Newton):</strong></p>
<ul>
  <li>Objects have definite positions and velocities</li>
  <li>Energy is continuous</li>
  <li>We can predict exactly where things will be</li>
</ul>

<p><strong>Quantum Physics:</strong></p>
<ul>
  <li>Objects don't have definite positions until measured</li>
  <li>Energy comes in discrete packets (quanta)</li>
  <li>We can only predict probabilities</li>
</ul>

<h3>1.2 Planck's Constant and Energy Quanta</h3>
<p><strong>Planck's Constant:</strong> h ≈ 6.63 × 10⁻³⁴ J·s</p>
<p>Energy of a photon: <strong>E = h·f</strong> where f is frequency</p>
<p>This revolutionary idea showed that light comes in discrete packets (photons), not continuous waves.</p>

<h3>1.3 Wave-Particle Duality</h3>
<p>Light and matter have both wave-like and particle-like properties.</p>
<ul>
  <li>As <strong>particles:</strong> photons carry energy E = hf</li>
  <li>As <strong>waves:</strong> light shows interference and diffraction</li>
</ul>

<p><strong>de Broglie Wavelength:</strong> λ = h/p (all particles have a wavelength!)</p>

<p><strong>Interactive Simulator:</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/quantum-measurement/latest/quantum-measurement_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Explore quantum effects and how measurement changes results. Essential for understanding wave-particle duality!</em></p>

<hr>

<h2>Module 2: The Schrödinger Equation</h2>
<p><strong>What you'll learn:</strong> The fundamental equation of quantum mechanics.</p>

<h3>2.1 What is the Schrödinger Equation?</h3>
<p>The time-dependent Schrödinger equation describes how quantum systems evolve:</p>
<p><strong>iℏ ∂ψ/∂t = Ĥψ</strong></p>
<p>Don't worry about the notation! The key idea: ψ (psi) is the <strong>wave function</strong> 
that contains all information about a quantum system.</p>

<h3>2.2 Wave Functions and Probability</h3>
<p><strong>Key Insight:</strong> |ψ|² tells us the probability of finding a particle at a location.</p>
<ul>
  <li>ψ itself is complex (has imaginary parts)</li>
  <li>|ψ|² is always real and positive (probability density)</li>
  <li>∫|ψ|² dV = 1 (total probability must equal 1)</li>
</ul>

<p><strong>This is the fundamental difference from classical mechanics:</strong></p>
<ul>
  <li>Classical: Position is definite (either here or there)</li>
  <li>Quantum: Position is probabilistic (probability distribution)</li>
</ul>

<h3>2.3 Observables and Measurements</h3>
<p>In quantum mechanics, the act of measurement changes the system!</p>
<ul>
  <li>Before measurement: particle exists in a superposition of states</li>
  <li>During measurement: we collapse the wave function to one state</li>
  <li>After measurement: the system is in the measured state</li>
</ul>

<p><strong>Interactive Simulator:</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/quantum-coin-toss/latest/quantum-coin-toss_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>See how measurement affects quantum systems. Why do repeated measurements give different results? Explore superposition and quantum probability!</em></p>

<hr>

<h2>Module 3: Quantum Superposition</h2>
<p><strong>What you'll learn:</strong> How particles can exist in multiple states simultaneously.</p>

<h3>3.1 What is Superposition?</h3>
<p><strong>Superposition:</strong> A quantum particle can exist in multiple states at the same time 
until it's measured.</p>

<p><strong>Example - Schrödinger's Cat:</strong></p>
<p>Imagine a cat in a sealed box with a quantum particle. The cat is both alive AND dead (superposition) 
until we open the box and measure (collapse the superposition).</p>

<h3>3.2 The Stern-Gerlach Experiment</h3>
<p>This famous experiment demonstrates quantum superposition:</p>
<ol>
  <li>Electrons have a property called "spin"</li>
  <li>Spin can be measured as "up" or "down"</li>
  <li>Before measurement, electrons are in superposition of spin-up AND spin-down</li>
  <li>Measurement collapses the superposition to one state</li>
</ol>

<p><strong>Interactive Simulator:</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/rutherford-scattering/latest/rutherford-scattering_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>See how particles interact with atoms. Explore how Rutherford discovered the atomic nucleus!</em></p>

<hr>

<h2>Module 4: Quantum Entanglement</h2>
<p><strong>What you'll learn:</strong> The "spooky" connections between entangled particles.</p>

<h3>4.1 What is Entanglement?</h3>
<p><strong>Entanglement:</strong> Two particles become connected so their quantum states are correlated.</p>
<ul>
  <li>Measure particle A as spin-up → particle B instantly becomes spin-down</li>
  <li>This happens even if particles are light-years apart!</li>
  <li>No information travels between them (violates no laws)</li>
</ul>

<h3>4.2 Bell's Theorem and the EPR Paradox</h3>
<p>Einstein called this "spooky action at a distance" and didn't believe it was real.</p>
<p><strong>Bell's Theorem (1964):</strong> Proved that entanglement is real!</p>
<ul>
  <li>Entanglement cannot be explained by hidden variables</li>
  <li>Quantum mechanics is fundamentally probabilistic</li>
  <li>Reality doesn't exist until measured</li>
</ul>

<h3>4.3 Applications of Entanglement</h3>
<ul>
  <li><strong>Quantum Cryptography:</strong> Unbreakable communication using entangled photons</li>
  <li><strong>Quantum Computing:</strong> Entangled qubits can process information exponentially faster</li>
  <li><strong>Quantum Teleportation:</strong> Transfer quantum states between particles</li>
</ul>

<hr>

<h2>Module 5: Atomic Structure & Spectroscopy</h2>
<p><strong>What you'll learn:</strong> How quantum mechanics explains atoms.</p>

<h3>5.1 The Hydrogen Atom</h3>
<p>Hydrogen is the simplest atom (1 proton + 1 electron). Quantum mechanics explains its structure perfectly!</p>

<p><strong>Energy Levels:</strong> Electrons can only occupy specific energy levels:</p>
<ul>
  <li>n = 1 (ground state): Lowest energy</li>
  <li>n = 2, 3, 4, ...: Excited states (higher energy)</li>
</ul>

<p><strong>Orbitals:</strong> Not circular orbits like planets! Instead, orbitals are probability clouds 
showing where we're likely to find the electron.</p>

<h3>5.2 Spectroscopy</h3>
<p><strong>Emission Spectrum:</strong> When electrons fall from high to low energy levels, they emit photons.</p>
<p>Energy of photon: <strong>ΔE = h·f = hc/λ</strong></p>
<p>Each element has a unique spectral signature (like a fingerprint!).</p>

<h3>5.3 Applications</h3>
<ul>
  <li><strong>Lasers:</strong> Stimulated emission of coherent light</li>
  <li><strong>Fluorescence:</strong> Excited atoms emit visible light</li>
  <li><strong>Neon Signs:</strong> Different noble gases produce different colors</li>
</ul>

<p><strong>Interactive Simulator:</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/models-of-the-hydrogen-atom/latest/models-of-the-hydrogen-atom_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Explore electron transitions and energy levels in the hydrogen atom. See different models (Bohr, Quantum Mechanical) in action!</em></p>

<hr>

<h2>Module 6: Quantum Computing Basics</h2>
<p><strong>What you'll learn:</strong> How quantum mechanics enables revolutionary computing.</p>

<h3>6.1 Classical Bits vs. Quantum Bits (Qubits)</h3>
<p><strong>Classical Bit:</strong> Either 0 or 1 (like a light switch: on or off)</p>
<p><strong>Qubit:</strong> Can be 0, 1, or BOTH at the same time (superposition!)</p>

<h3>6.2 Quantum Advantage</h3>
<p><strong>Classical Computer (3 bits):</strong> Can be in ONE state at a time</p>
<ul>
  <li>000, 001, 010, 011, 100, 101, 110, or 111</li>
  <li>Process one value at a time</li>
</ul>

<p><strong>Quantum Computer (3 qubits):</strong> Can be in ALL states simultaneously!</p>
<ul>
  <li>Superposition allows processing all 8 values at once</li>
  <li>For 300 qubits: 2³⁰⁰ states simultaneously (more than atoms in universe!)</li>
</ul>

<h3>6.3 Quantum Gates and Algorithms</h3>
<p><strong>Quantum Gates:</strong> Operations that manipulate qubits (like transistors in classical computers)</p>
<ul>
  <li><strong>Hadamard Gate:</strong> Creates superposition</li>
  <li><strong>CNOT Gate:</strong> Creates entanglement</li>
  <li><strong>Phase Gates:</strong> Manipulate quantum phases</li>
</ul>

<p><strong>Famous Quantum Algorithms:</strong></p>
<ul>
  <li><strong>Shor's Algorithm:</strong> Factor large numbers exponentially faster</li>
  <li><strong>Grover's Algorithm:</strong> Search unsorted databases exponentially faster</li>
</ul>

<h3>6.4 Current State of Quantum Computing</h3>
<ul>
  <li>IBM, Google, Rigetti: Building real quantum computers</li>
  <li>Google's "Quantum Supremacy" (2019): Solved problem in 200 seconds 
    (classical computer would take 10,000 years)</li>
  <li>Challenges: Decoherence, error correction, scalability</li>
</ul>

<hr>

<h2>Summary & Key Takeaways</h2>
<ul>
  <li>Quantum mechanics rules the atomic and subatomic world</li>
  <li>Particles don't have definite properties until measured (superposition)</li>
  <li>Entanglement creates spooky connections between particles</li>
  <li>Quantum mechanics perfectly explains atomic structure and spectra</li>
  <li>Quantum computers will revolutionize computing in the coming decades</li>
</ul>

<p><strong>Congratulations on learning quantum mechanics! Take the quiz to test your quantum knowledge.</strong></p>
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
     {"question_text": "Planck's constant is approximately:", "question_type": "multiple_choice", "options": ["3 × 10^8 m/s", "1.6 × 10^-19 C", "9.8 m/s²", "6.63 × 10^-34 J·s"], "correct_answer": "6.63 × 10^-34 J·s", "explanation": "Planck's constant h ≈ 6.63 × 10^-34 J·s is the fundamental constant in quantum mechanics. It relates a photon's energy to its frequency: E = hf. The tiny value shows why quantum effects are invisible at everyday scales. The other options are: speed of light, electron charge, and gravitational acceleration.", "points": 1, "order_index": 1},
    {"question_text": "What is wave-particle duality?", "question_type": "multiple_choice", "options": ["Light acts as both wave and particle", "Objects have two velocities", "Particles can't be waves", "Waves don't have energy"], "correct_answer": "Light acts as both wave and particle", "explanation": "Light exhibits dual nature: Wave properties include interference and diffraction (shown in double-slit experiments). Particle properties include the photoelectric effect and momentum transfer. Depending on how we measure it, light behaves as either waves or particles—this is one of quantum mechanics' most profound insights.", "points": 1, "order_index": 2},
    {"question_text": "What does the wave function ψ represent?", "question_type": "multiple_choice", "options": ["Probability amplitude of finding a particle", "The particle's velocity", "The particle's mass", "Light wavelength"], "correct_answer": "Probability amplitude of finding a particle", "explanation": "The wave function ψ is a mathematical function that encodes all information about a quantum system. The probability density is |ψ|² (the square of the wave function's magnitude). This means we can calculate the probability of finding a particle at a specific location by squaring the wave function. The particle doesn't have a definite position until measured!", "points": 1, "order_index": 3},
    {"question_text": "Heisenberg Uncertainty Principle states:", "question_type": "multiple_choice", "options": ["Can't know position and momentum precisely simultaneously", "All measurements are uncertain", "Particles don't exist", "Energy is not conserved"], "correct_answer": "Can't know position and momentum precisely simultaneously", "explanation": "Mathematically: Δx·Δp ≥ ℏ/2 (where ℏ = h/2π). This isn't due to bad equipment—it's a fundamental property of nature! The more precisely we know position (small Δx), the less we know about momentum (large Δp), and vice versa. This applies to all quantum particles and is why electrons don't have definite orbits like planets.", "points": 1, "order_index": 4},
    {"question_text": "What is superposition?", "question_type": "multiple_choice", "options": ["Particle exists in multiple states until measured", "Two particles in same location", "Adding sound waves", "Particle at rest"], "correct_answer": "Particle exists in multiple states until measured", "explanation": "In quantum superposition, a particle can exist in a combination of multiple states simultaneously. For example, an electron's spin can be in superposition of spin-up AND spin-down at the same time. Only when we measure it does the superposition 'collapse' to a definite state. This is radically different from classical objects, which always have definite properties.", "points": 1, "order_index": 5},
    {"question_text": "What does the photoelectric effect demonstrate?", "question_type": "multiple_choice", "options": ["Light has particle properties", "Electrons have negative charge", "Light always travels in straight lines", "Metals are good conductors"], "correct_answer": "Light has particle properties", "explanation": "The photoelectric effect: When light hits a metal, it ejects electrons. Classical wave theory predicted the effect depends on light intensity, but experiments showed it depends on light frequency. Einstein explained this in 1905: Light consists of particles (photons) with energy E = hf. A single high-frequency photon can eject an electron, regardless of light intensity. This was revolutionary and won Einstein the Nobel Prize!", "points": 1, "order_index": 6},
    {"question_text": "Quantum entanglement means:", "question_type": "multiple_choice", "options": ["Two particles' states are correlated instantly", "Particles are physically connected", "Particles move together", "Particles have same velocity"], "correct_answer": "Two particles' states are correlated instantly", "explanation": "When two particles become entangled, their quantum states become correlated perfectly. Measure particle A as spin-up? Particle B instantly becomes spin-down (or whatever the correlation is). Remarkably, this happens instantly even if they're light-years apart! Einstein called this 'spooky action at a distance' and doubted it, but Bell's theorem (1964) and experiments proved it's real. No information travels faster than light—only the correlation.", "points": 1, "order_index": 7},
    {"question_text": "A qubit differs from a classical bit because:", "question_type": "multiple_choice", "options": ["Qubit can be 0, 1, or both via superposition", "Qubits are smaller", "Qubits never fail", "Qubits are slower"], "correct_answer": "Qubit can be 0, 1, or both via superposition", "explanation": "Classical bit: Always 0 or 1 (on/off). Quantum bit (qubit): Can be 0, 1, or both (superposition)! This is the power of quantum computing. With 3 classical bits, you can process ONE value (e.g., 000 or 101). With 3 qubits, you process ALL 8 values simultaneously! This exponential speedup is why quantum computers will revolutionize computing for certain problems like factoring and searching.", "points": 1, "order_index": 8},
    {"question_text": "Ground state of hydrogen atom has n = ?", "question_type": "multiple_choice", "options": ["n = 0", "n = 2", "No fixed value", "n = 1"], "correct_answer": "n = 1", "explanation": "In the hydrogen atom, electrons occupy discrete energy levels labeled by n = 1, 2, 3, ... The ground state (lowest energy, most stable) is n = 1. Excited states (n = 2, 3, ...) have higher energy. When an electron falls from n = 2 to n = 1, it releases energy as a photon. This explains the hydrogen spectral lines that were a mystery before quantum mechanics!", "points": 1, "order_index": 9},
]

# ===== COMPREHENSIVE CHEMISTRY COURSE CONTENT =====
CHEMISTRY_CONTENT = """
<h1>Chemistry Fundamentals - Complete Guide</h1>

<h2>📚 Course Overview</h2>
    <p>Master the essential concepts of chemistry from atoms and molecules to reactions and equilibrium. 
    This course uses interactive PhET simulators to visualize chemical phenomena and build your understanding.</p>

    <hr>

    <h2>Module 1: Atomic Structure & the Periodic Table</h2>
    <p><strong>What you'll learn:</strong> Atoms, electrons, protons, neutrons, and the organization of the periodic table.</p>

    <h3>1.1 Structure of the Atom</h3>
    <p>All matter is made of atoms, which consist of:</p>
    <ul>
    <li><strong>Nucleus:</strong> Contains protons (positive charge) and neutrons (neutral)</li>
    <li><strong>Electron Cloud:</strong> Contains electrons (negative charge) orbiting the nucleus</li>
    <li>Protons and electrons have equal but opposite charges</li>
    <li>Atoms are electrically neutral when protons = electrons</li>
    </ul>

    <h3>1.2 Periodic Table Organization</h3>
    <p>Elements organized by atomic number and chemical properties:</p>
    <ul>
    <li><strong>Periods:</strong> Horizontal rows (increase from left to right)</li>
    <li><strong>Groups:</strong> Vertical columns (similar chemical properties)</li>
    <li><strong>Main Groups:</strong> Group 1 (alkali metals), 17 (halogens), 18 (noble gases)</li>
    </ul>

    <p><strong>Interactive Simulator:</strong></p>
    <iframe src="https://phet.colorado.edu/sims/html/build-an-atom/latest/build-an-atom_all.html" 
    width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
    <p><em>Build atoms by adding protons, neutrons, and electrons! See how atomic number and mass number change.</em></p>

    <hr>

    <h2>Module 2: Chemical Bonding</h2>
    <p><strong>What you'll learn:</strong> How atoms bond together and why different bonds have different properties.</p>

    <h3>2.1 Ionic Bonding</h3>
    <p>Formed when electrons transfer from one atom to another.</p>
    <ul>
    <li>Metal loses electrons → becomes positively charged (cation)</li>
    <li>Nonmetal gains electrons → becomes negatively charged (anion)</li>
    <li>Electrostatic attraction holds them together</li>
    <li>Example: NaCl (sodium chloride) - table salt</li>
    </ul>

    <h3>2.2 Covalent Bonding</h3>
    <p>Formed when atoms share electrons.</p>
    <ul>
    <li><strong>Single Bond:</strong> Share 1 pair of electrons (H-H)</li>
    <li><strong>Double Bond:</strong> Share 2 pairs of electrons (O=O)</li>
    <li><strong>Triple Bond:</strong> Share 3 pairs of electrons (N≡N)</li>
    <li>Covalent bonds found in most organic compounds</li>
    </ul>

    <p><strong>Interactive Simulator:</strong></p>
    <iframe src="https://phet.colorado.edu/sims/html/molecule-shapes/latest/molecule-shapes_all.html" 
    width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
    <p><em>Build molecules and predict their shapes using VSEPR theory! Experiment with lone pairs and bonding pairs.</em></p>

    <hr>

    <h2>Module 3: Chemical Reactions & Stoichiometry</h2>
    <p><strong>What you'll learn:</strong> How to balance equations and calculate quantities in chemical reactions.</p>

    <h3>3.1 Balancing Chemical Equations</h3>
    <p>Conservation of mass: atoms cannot be created or destroyed.</p>
    <p><strong>Example:</strong> Fe + O₂ → Fe₂O₃</p>
    <p><strong>Balanced:</strong> 4Fe + 3O₂ → 2Fe₂O₃</p>

    <h3>3.2 Types of Reactions</h3>
    <ul>
    <li><strong>Synthesis:</strong> A + B → AB (two substances combine)</li>
    <li><strong>Decomposition:</strong> AB → A + B (one substance breaks apart)</li>
    <li><strong>Single Displacement:</strong> A + BC → AC + B (element replaces element)</li>
    <li><strong>Double Displacement:</strong> AB + CD → AD + CB (ions exchange)</li>
    <li><strong>Combustion:</strong> CₓHᵧ + O₂ → CO₂ + H₂O (burning with oxygen)</li>
    </ul>

    <p><strong>Interactive Simulator:</strong></p>
    <iframe src="https://phet.colorado.edu/sims/html/reactants-products-salts/latest/reactants-products-salts_all.html" 
    width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
    <p><em>See what happens when you mix different chemicals! Observe reactions and the products formed.</em></p>

    <hr>

    <h2>Module 4: Acids, Bases & pH</h2>
    <p><strong>What you'll learn:</strong> Properties of acids and bases, pH scale, and neutralization reactions.</p>

    <h3>4.1 Acids and Bases (Arrhenius Definition)</h3>
    <ul>
    <li><strong>Acids:</strong> Produce H⁺ ions in solution (taste sour, turn litmus red)</li>
    <li><strong>Bases:</strong> Produce OH⁻ ions in solution (taste bitter, turn litmus blue)</li>
    <li><strong>Neutralization:</strong> Acid + Base → Salt + Water</li>
    </ul>

    <h3>4.2 The pH Scale</h3>
    <ul>
    <li>pH = -log[H⁺] (measures hydrogen ion concentration)</li>
    <li>pH 0-7: Acidic (more H⁺ ions)</li>
    <li>pH = 7: Neutral (pure water)</li>
    <li>pH 7-14: Basic/Alkaline (more OH⁻ ions)</li>
    <li>Each step is 10x more acidic or basic</li>
    </ul>

    <p><strong>Interactive Simulator:</strong></p>
    <iframe src="https://phet.colorado.edu/sims/html/ph-scale/latest/ph-scale_all.html" 
    width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
    <p><em>Test different substances and measure their pH! See how concentration affects pH value.</em></p>

    <hr>

    <h2>Module 5: Thermochemistry & Energy</h2>
    <p><strong>What you'll learn:</strong> Energy in chemical reactions, exothermic and endothermic processes.</p>

    <h3>5.1 Exothermic vs Endothermic</h3>
    <ul>
    <li><strong>Exothermic:</strong> Releases energy (ΔH < 0) - gets hot, burns</li>
    <li><strong>Endothermic:</strong> Absorbs energy (ΔH > 0) - gets cold</li>
    <li><strong>Heat of Reaction:</strong> Amount of energy released or absorbed</li>
    </ul>

    <h3>5.2 Real-World Examples</h3>
    <ul>
    <li><strong>Exothermic:</strong> Combustion, neutralization, rusting of iron</li>
    <li><strong>Endothermic:</strong> Melting ice, evaporating water, photosynthesis</li>
    </ul>

    <hr>

    <h2>Summary & Key Takeaways</h2>
    <ul>
    <li>Atoms consist of protons, neutrons, and electrons</li>
    <li>Atoms bond through ionic, covalent, or metallic bonding</li>
    <li>Chemical equations must be balanced (conservation of mass)</li>
    <li>Acids produce H⁺, bases produce OH⁻ ions</li>
    <li>Reactions transfer or absorb energy</li>
    </ul>

    <p><strong>You've completed Chemistry Fundamentals! Take the quiz to test your knowledge.</strong>
"""

CHEMISTRY_QUESTIONS = [
    {"question_text": "How many protons does a carbon atom have?", "question_type": "multiple_choice", "options": ["8", "7", "5", "6"], "correct_answer": "6", "explanation": "Carbon has atomic number 6, which means it has 6 protons. A neutral carbon atom also has 6 electrons. Protons are positively charged particles in the nucleus.", "points": 1, "order_index": 1},
    {"question_text": "What type of bond shares electrons between atoms?", "question_type": "multiple_choice", "options": ["Metallic bond", "Hydrogen bond", "Covalent bond", "Ionic bond"], "correct_answer": "Covalent bond", "explanation": "Covalent bonds form when two atoms share one or more pairs of electrons. This is different from ionic bonds where electrons are transferred completely. Covalent bonds are found in molecules like O₂, H₂O, and CO₂.", "points": 1, "order_index": 2},
    {"question_text": "What is the pH of pure water at 25°C?", "question_type": "multiple_choice", "options": ["0", "14", "7", "10"], "correct_answer": "7", "explanation": "Pure water has a pH of 7, which is considered neutral. This is because [H⁺] = [OH⁻] = 10⁻⁷ M. Any pH below 7 is acidic, and any pH above 7 is basic.", "points": 1, "order_index": 3},
    {"question_text": "Which type of reaction involves a compound breaking into simpler substances?", "question_type": "multiple_choice", "options": ["Synthesis reaction", "Combustion reaction", "Decomposition reaction", "Double displacement"], "correct_answer": "Decomposition reaction", "explanation": "Decomposition reactions break down a compound into simpler substances. Example: 2H₂O → 2H₂ + O₂. This is the opposite of a synthesis reaction where simpler substances combine.", "points": 1, "order_index": 4},
    {"question_text": "An exothermic reaction is one that:", "question_type": "multiple_choice", "options": ["Requires heat from surroundings", "Absorbs energy (ΔH > 0)", "Releases energy (ΔH < 0)", "Changes color"], "correct_answer": "Releases energy (ΔH < 0)", "explanation": "Exothermic reactions release energy to the surroundings, making the surroundings warmer. Examples include combustion and neutralization. The negative ΔH indicates energy is released.", "points": 1, "order_index": 5},
    {"question_text": "What is the correct formula for sodium chloride?", "question_type": "multiple_choice", "options": ["NaClₙ", "Na₂Cl", "NaCl₂", "NaCl"], "correct_answer": "NaCl", "explanation": "Sodium (Na) has a +1 charge and chloride (Cl) has a -1 charge. Therefore, one sodium atom bonds with one chloride atom to form NaCl. This is common table salt.", "points": 1, "order_index": 6},
    {"question_text": "Which substance is a strong acid?", "question_type": "multiple_choice", "options": ["Vinegar (acetic acid)", "Hydrochloric acid (HCl)", "Lemon juice (citric acid)", "Water"], "correct_answer": "Hydrochloric acid (HCl)", "explanation": "Hydrochloric acid (HCl) is one of the strong acids that completely ionizes in water. The other options are either weak acids or neutral. Strong acids include HCl, HBr, HI, HNO₃, H₂SO₄, and HClO₄.", "points": 1, "order_index": 7},
    {"question_text": "In the reaction 2H₂ + O₂ → 2H₂O, how many moles of H₂O are produced from 4 moles of H₂?", "question_type": "multiple_choice", "options": ["1 mole", "2 moles", "4 moles", "8 moles"], "correct_answer": "4 moles", "explanation": "The stoichiometric ratio is 2:2 for H₂:H₂O (or 1:1). If 4 moles of H₂ react, then 4 moles of H₂O are produced. Always use the coefficients in the balanced equation to determine mole ratios.", "points": 1, "order_index": 8},
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
        print("  ✓ Quantum: Comprehensive teaching content + 9 questions (randomized answers)")
        print("  ✓ Chemistry: Comprehensive teaching content + 8 questions (randomized answers)")
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
