#!/usr/bin/env python3
"""
Enhanced College-Level Course Injection Script - 65 Professional Courses

This script creates comprehensive, college-level courses for grades 1-13 across 5 strands:
- Mathematics (Advanced Theory & Applications)
- Physics (University-Level Mechanics & Modern Physics)
- Chemistry (Organic, Inorganic, Physical Chemistry)
- Biology & Earth Sciences (Molecular Biology to Ecology)
- Applied Sciences (Data Science, Engineering, Research Methods)

Features:
- Sophisticated, real-world problem sets
- Advanced mathematical modeling and computational thinking
- Research-based laboratory investigations
- Cross-disciplinary connections and applications
- Professional-level assessment questions
- Comprehensive learning outcomes and competencies

Usage (PowerShell):
  $env:MYSQLHOST="your-aiven-host"
  $env:MYSQLPASSWORD="your-aiven-password"
  python enhanced_college_injection.py

Requirements: pip install pymysql python-dotenv
"""

from __future__ import annotations

import json
import os
import random
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any

import pymysql

import inject_60_grade_courses as inj

# Enhanced college-level topics by strand and grade
COLLEGE_TOPICS = {
    "math": [
        "Foundational Number Theory & Mathematical Logic",  # Grade 1
        "Advanced Arithmetic Algorithms & Proof Techniques",  # Grade 2
        "Abstract Algebra: Group Theory Introduction",  # Grade 3
        "Real Analysis: Limits, Continuity & Differentiation",  # Grade 4
        "Linear Algebra: Vector Spaces & Linear Transformations",  # Grade 5
        "Multivariable Calculus & Vector Analysis",  # Grade 6
        "Differential Equations & Dynamical Systems",  # Grade 7
        "Complex Analysis & Conformal Mapping",  # Grade 8
        "Topology: Metric Spaces & Continuity",  # Grade 9
        "Abstract Algebra: Rings, Fields & Galois Theory",  # Grade 10
        "Functional Analysis & Hilbert Spaces",  # Grade 11
        "Differential Geometry & Manifold Theory",  # Grade 12
        "Advanced Mathematical Modeling & Research Seminar"  # Grade 13
    ],
    "physics": [
        "Classical Mechanics: Newtonian to Lagrangian Formulations",  # Grade 1
        "Thermodynamics & Statistical Mechanics Fundamentals",  # Grade 2
        "Electromagnetism: Maxwell's Equations & Applications",  # Grade 3
        "Wave Phenomena & Optics: Interference to Quantum",  # Grade 4
        "Quantum Mechanics: Wave Functions & Operators",  # Grade 5
        "Special Relativity & Spacetime Geometry",  # Grade 6
        "Nuclear Physics & Particle Interactions",  # Grade 7
        "Solid State Physics & Quantum Materials",  # Grade 8
        "Plasma Physics & Controlled Fusion",  # Grade 9
        "General Relativity & Cosmology",  # Grade 10
        "Quantum Field Theory & Particle Physics",  # Grade 11
        "Computational Physics & High-Performance Computing",  # Grade 12
        "Advanced Research Methods in Theoretical Physics"  # Grade 13
    ],
    "chemistry": [
        "General Chemistry: Atomic Structure & Periodicity",  # Grade 1
        "Chemical Bonding & Molecular Orbital Theory",  # Grade 2
        "Thermodynamics & Chemical Equilibrium",  # Grade 3
        "Chemical Kinetics & Reaction Mechanisms",  # Grade 4
        "Quantum Chemistry & Computational Methods",  # Grade 5
        "Organic Chemistry I: Structure & Mechanisms",  # Grade 6
        "Organic Chemistry II: Synthesis & Spectroscopy",  # Grade 7
        "Inorganic Chemistry: Coordination & Organometallics",  # Grade 8
        "Physical Chemistry: Statistical & Molecular Thermodynamics",  # Grade 9
        "Analytical Chemistry: Instrumentation & Methods",  # Grade 10
        "Biochemistry: Enzymes & Metabolic Pathways",  # Grade 11
        "Materials Chemistry & Nanotechnology",  # Grade 12
        "Advanced Chemical Research & Drug Discovery"  # Grade 13
    ],
    "bioearth": [
        "Cellular Biology: Membranes, Organelles & Transport",  # Grade 1
        "Molecular Genetics: DNA, RNA & Protein Synthesis",  # Grade 2
        "Evolutionary Biology: Population Genetics & Speciation",  # Grade 3
        "Ecology: Ecosystem Dynamics & Conservation Biology",  # Grade 4
        "Physiology: Homeostasis & Regulatory Mechanisms",  # Grade 5
        "Microbiology: Pathogens, Immunity & Virology",  # Grade 6
        "Biochemistry: Metabolic Pathways & Energy Transfer",  # Grade 7
        "Climate Science: Atmospheric Chemistry & Modeling",  # Grade 8
        "Geology: Plate Tectonics & Earth Systems",  # Grade 9
        "Oceanography: Marine Ecosystems & Biogeochemistry",  # Grade 10
        "Environmental Science: Pollution & Remediation",  # Grade 11
        "Astrobiology: Life in Extreme Environments",  # Grade 12
        "Systems Biology & Integrative Research Methods"  # Grade 13
    ],
    "applied": [
        "Introduction to Scientific Computing & Programming",  # Grade 1
        "Data Structures & Algorithms for Scientific Applications",  # Grade 2
        "Statistical Methods & Experimental Design",  # Grade 3
        "Machine Learning & Artificial Intelligence in Science",  # Grade 4
        "Computational Modeling & Simulation Techniques",  # Grade 5
        "Engineering Design: Systems Thinking & Optimization",  # Grade 6
        "Data Science: Big Data Analytics & Visualization",  # Grade 7
        "Operations Research & Decision Analysis",  # Grade 8
        "Scientific Communication & Technical Writing",  # Grade 9
        "Research Ethics & Scientific Integrity",  # Grade 10
        "Project Management & Research Collaboration",  # Grade 11
        "Innovation, Entrepreneurship & Technology Transfer",  # Grade 12
        "Capstone Research Project & Professional Development"  # Grade 13
    ]
}

# Enhanced learning competencies by strand
COMPETENCIES = {
    "math": [
        "Mathematical proof construction & logical reasoning",
        "Abstract mathematical thinking & generalization",
        "Computational mathematics & algorithmic problem-solving",
        "Mathematical modeling of complex systems"
    ],
    "physics": [
        "Theoretical analysis & mathematical formulation",
        "Experimental design & data interpretation",
        "Computational physics & numerical methods",
        "Cross-disciplinary application of physical principles"
    ],
    "chemistry": [
        "Molecular-level thinking & mechanistic reasoning",
        "Laboratory techniques & analytical methods",
        "Computational chemistry & molecular modeling",
        "Chemical synthesis & experimental design"
    ],
    "bioearth": [
        "Systems thinking in biological contexts",
        "Experimental design & statistical analysis",
        "Molecular techniques & biotechnology methods",
        "Environmental analysis & conservation strategies"
    ],
    "applied": [
        "Computational thinking & programming proficiency",
        "Data analysis & statistical reasoning",
        "Interdisciplinary problem-solving & innovation",
        "Scientific communication & collaboration"
    ]
}

def load_phet_titles_urls_from_script(script_path: Path) -> dict[str, str]:
    """Load PhET simulation titles and URLs from frontend script."""
    text = script_path.read_text(encoding="utf-8")
    pairs = re.findall(r'\{\s*title:\s*"([^"]+)",\s*url:\s*"([^"]+)"', text)
    return {t: u for t, u in pairs}

def create_enhanced_figure_gallery(strand: str, grade: int) -> str:
    """Create professional-grade reference figures with advanced concepts."""
    
    galleries = {
        "math": [
            ("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Mandelbrot_set_--_zoom_12.svg/640px-Mandelbrot_set_--_zoom_12.svg.png",
             "Complex fractal geometry: Mandelbrot set demonstrating self-similarity and mathematical beauty."),
            ("https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Euler%27s_formula.svg/500px-Euler%27s_formula.svg.png",
             "Euler's formula: e^(iπ) + 1 = 0, connecting five fundamental mathematical constants."),
            ("https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Calculus_infinitesimals.svg/480px-Calculus_infinitesimals.svg.png",
             "Differential calculus: Infinitesimal approach to rates of change and optimization.")
        ],
        "physics": [
            ("https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Spacetime_curvature.png/640px-Spacetime_curvature.png",
             "General relativity: Spacetime curvature around massive objects."),
            ("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Quantum_mechanics_double_slit_experiment.svg/500px-Quantum_mechanics_double_slit_experiment.svg.png",
             "Quantum mechanics: Wave-particle duality in the double-slit experiment."),
            ("https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Maxwell_equations.svg/600px-Maxwell_equations.svg.png",
             "Electromagnetism: Maxwell's equations unifying electric and magnetic phenomena.")
        ],
        "chemistry": [
            ("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/DNA_3D_structure.svg/500px-DNA_3D_structure.svg.png",
             "Molecular biology: Double helix structure of DNA with base pairing."),
            ("https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Periodic_table_large.svg/640px-Periodic_table_large.svg.png",
             "Periodic trends: Systematic organization of elements and their properties."),
            ("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Protein_folding.svg/500px-Protein_folding.svg.png",
             "Biochemistry: Protein folding pathways and molecular interactions.")
        ],
        "bioearth": [
            ("https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Carbon_cycle_with_budget_numbers.svg/640px-Carbon_cycle_with_budget_numbers.svg.png",
             "Biogeochemical cycles: Global carbon budget and fluxes between reservoirs."),
            ("https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Phylogenetic_tree.svg/500px-Phylogenetic_tree.svg.png",
             "Evolutionary biology: Phylogenetic relationships and common ancestry."),
            ("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Ecosystem_energy_flow.svg/500px-Ecosystem_energy_flow.svg.png",
             "Ecology: Energy flow through trophic levels and ecosystem productivity.")
        ],
        "applied": [
            ("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Machine_learning_workflow.svg/500px-Machine_learning_workflow.svg.png",
             "Data science: Machine learning pipeline from data to predictions."),
            ("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Systems_thinking_diagram.svg/500px-Systems_thinking_diagram.svg.png",
             "Systems engineering: Complex system interactions and feedback loops."),
            ("https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Scientific_method_flowchart.svg/500px-Scientific_method_flowchart.svg.png",
             "Research methodology: Systematic approach to scientific inquiry and validation.")
        ]
    }
    
    blocks = galleries.get(strand, galleries["applied"])
    figs = []
    
    for url, caption in blocks:
        safe_caption = caption.replace('"', "&quot;")
        figs.append(
            f'<figure style="margin:20px 0;text-align:center;background:#f8fafc;padding:16px;border-radius:12px;border:1px solid #e2e8f0;">'
            f'<img src="{url}" alt="{safe_caption}" loading="lazy" '
            f'style="max-width:100%;height:auto;border-radius:8px;box-shadow:0 4px 6px rgba(0,0,0,0.1);"/>'
            f'<figcaption style="font-size:0.9em;color:#334155;margin-top:12px;line-height:1.5;">{safe_caption} <strong>(Grade {grade} Advanced)</strong></figcaption>'
            f"</figure>"
        )
    
    return '<h2 style="color:#1e293b;border-bottom:2px solid #3b82f6;padding-bottom:8px;">Module 3A: Advanced Visual References & Conceptual Frameworks</h2>' + "".join(figs)

def build_enhanced_content(course: dict) -> str:
    """Build comprehensive college-level course content."""
    base_content = inj.build_content(course)
    enhanced_gallery = create_enhanced_figure_gallery(course["strand"], course["grade"])
    
    # Replace basic module with enhanced version
    enhanced_content = base_content.replace(
        "<h2>Module 3: Drawings and Visual Models</h2>", 
        enhanced_gallery + "<h2>Module 3: Advanced Theoretical Frameworks & Mathematical Models</h2>", 
        1
    )
    
    # Add college-level enhancements
    enhancements = f"""
    <div style="background:#f0f9ff;border-left:4px solid #0ea5e9;padding:16px;margin:20px 0;border-radius:8px;">
        <h3 style="color:#0c4a6e;margin-top:0;">College-Level Learning Outcomes</h3>
        <ul style="margin:8px 0;padding-left:20px;color:#1e293b;">
            {"".join([f'<li>{comp}</li>' for comp in COMPETENCIES[course["strand"]]])}
        </ul>
    </div>
    
    <div style="background:#fef3c7;border-left:4px solid #f59e0b;padding:16px;margin:20px 0;border-radius:8px;">
        <h3 style="color:#92400e;margin-top:0;">Professional Applications</h3>
        <p style="margin:8px 0;color:#78350f;">This course integrates theoretical knowledge with real-world applications, preparing students for advanced research and professional practice in {course["strand"]}.</p>
    </div>
    """
    
    return enhanced_content.replace(
        "<h2>Module 1: Foundations and Vocabulary</h2>",
        enhancements + "<h2>Module 1: Advanced Theoretical Foundations</h2>"
    )

def create_advanced_problem_set(strand: str, grade: int) -> List[Tuple[str, List[str], str]]:
    """Generate sophisticated, college-level problem sets."""
    
    rng = random.Random(grade * 100 + sum(ord(c) for c in strand))
    
    if strand == "math":
        if grade <= 4:
            return [
                ("Prove that the set of rational numbers is countable using Cantor's diagonal argument.", 
                 ["Construct injection Q → N", "Show bijection with N×Z", "Conclude countability"], 
                 "Countable infinity proof completed"),
                ("Find the limit of (1 + 1/n)^n as n → ∞ using natural logarithms and L'Hôpital's rule.",
                 ["Take ln of sequence", "Apply L'Hôpital's rule", "Exponentiate result"], 
                 "e (Euler's number)"),
                ("Show that the function f(x) = x²sin(1/x) for x≠0, f(0)=0 is differentiable everywhere.",
                 ["Check differentiability at x≠0", "Compute limit definition at x=0", "Verify continuity"], 
                 "Differentiable with f'(0)=0")
            ]
        elif grade <= 8:
            return [
                ("Find eigenvalues and eigenvectors of the matrix A = [[3,1],[2,2]].",
                 ["Solve det(A-λI)=0", "Find eigenvectors for each λ", "Normalize if needed"], 
                 "λ₁=4, λ₂=1 with corresponding eigenvectors"),
                ("Evaluate the triple integral ∫∫∫_E (x²+y²+z²) dV where E is the unit sphere.",
                 ["Convert to spherical coordinates", "Set up limits 0≤ρ≤1", "Integrate using symmetry"], 
                 "4π/5"),
                ("Solve the differential equation y'' + 4y' + 4y = e^(-2x) using variation of parameters.",
                 ["Find homogeneous solution", "Apply variation of parameters", "Determine particular solution"], 
                 "y = (C₁ + C₂x)e^(-2x) + x²e^(-2x)/2")
            ]
        else:
            return [
                ("Prove the Fundamental Theorem of Calculus using Riemann sums and continuity.",
                 ["Define Riemann integral", "Show F'(x) = f(x)", "Verify FTC conditions"], 
                 "Complete proof established"),
                ("Find the Fourier series expansion of f(x) = |x| on [-π,π].",
                 ["Compute coefficients a₀, aₙ, bₙ", "Apply even function properties", "Write series expansion"], 
                 "π/2 - 4/π Σ(cos((2n-1)x)/(2n-1)²)"),
                ("Use Green's Theorem to evaluate ∮_C (x²-y)dx + (y²+x)dy where C is the unit circle.",
                 ["Compute partial derivatives", "Apply Green's Theorem", "Integrate over unit disk"], 
                 "2π")
            ]
    
    elif strand == "physics":
        if grade <= 4:
            return [
                (f"Derive the escape velocity from Earth's surface using energy conservation.",
                 ["Set KE = PE at infinity", "Solve for v", "Substitute Earth's parameters"], 
                 "11.2 km/s"),
                (f"Calculate the de Broglie wavelength of an electron moving at 2×10⁶ m/s.",
                 ["Apply λ = h/p", "Calculate momentum p = mv", "Compute wavelength"], 
                 "3.64 × 10^-10 m"),
                (f"Find the magnetic field at the center of a circular coil with N=100 turns, R=0.1m, I=2A.",
                 ["Use B = μ₀NI/2R", "Substitute values", "Compute result"], 
                 "1.26 × 10^-3 T")
            ]
        elif grade <= 8:
            return [
                (f"Solve the time-independent Schrödinger equation for a particle in a 1D infinite well.",
                 ["Set up differential equation", "Apply boundary conditions", "Find energy eigenvalues"], 
                 "Eₙ = n²h²/(8mL²)"),
                (f"Derive the Stefan-Boltzmann law from Planck's radiation formula.",
                 ["Integrate spectral radiance", "Use u = aT⁴ relation", "Connect to σ"], 
                 "j* = σT⁴ where σ = 2π⁵k⁴/(15h³c²)"),
                (f"Calculate the binding energy per nucleon for ^56Fe using mass defect.",
                 ["Find mass difference", "Convert to energy", "Divide by nucleon number"], 
                 "8.8 MeV/nucleon")
            ]
        else:
            return [
                (f"Derive Einstein's field equations from the principle of least action.",
                 ["Write Einstein-Hilbert action", "Vary with respect to metric", "Obtain field equations"], 
                 "Gμν + Λgμν = 8πG/c⁴ Tμν"),
                (f"Calculate the cross-section for electron-positron annihilation to muons.",
                 ["Use QED matrix element", "Square and average over spins", "Integrate over phase space"], 
                 "σ = (4πα²/3s)(1 + 2mμ²/s)√(1-4mμ²/s)"),
                (f"Solve the Dirac equation for a free particle and interpret solutions.",
                 ["Write Dirac equation", "Find plane wave solutions", "Analyze spinors"], 
                 "ψ = u(p)e^(-ip·x) + v(p)e^(ip·x)")
            ]
    
    elif strand == "chemistry":
        if grade <= 4:
            return [
                (f"Calculate the pH of a 0.001 M solution of acetic acid (Ka = 1.8×10^-5).",
                 ["Set up ICE table", "Apply Ka expression", "Solve quadratic approximation"], 
                 "pH ≈ 3.9"),
                (f"Determine the rate law for reaction 2A + B → C given experimental data.",
                 ["Find reaction orders", "Write rate expression", "Calculate rate constant"], 
                 "Rate = k[A]²[B]"),
                (f"Calculate the standard Gibbs free energy change for cell with E° = 1.10 V.",
                 ["Use ΔG° = -nFE°", "Substitute n=2 electrons", "Compute ΔG°"], 
                 "-212.3 kJ/mol")
            ]
        elif grade <= 8:
            return [
                (f"Predict the major product of electrophilic aromatic substitution on nitrobenzene.",
                 ["Analyze directing effects", "Consider deactivating group", "Determine position"], 
                 "Meta substitution due to -NO₂ directing"),
                (f"Calculate the crystal field splitting energy for [Fe(CN)₆]³⁻ using spectroscopic data.",
                 ["Use λ = hc/ΔE", "Convert wavelength to energy", "Apply to complex"], 
                 "Δ₀ ≈ 350 kJ/mol (strong field)"),
                (f"Determine the molecular geometry and hybridization of SF₄ using VSEPR.",
                 ["Count electron domains", "Apply VSEPR model", "Predict geometry"], 
                 "See-saw geometry with sp³d hybridization")
            ]
        else:
            return [
                (f"Derive the rate equation for enzyme-catalyzed reaction using Michaelis-Menten mechanism.",
                 ["Apply steady-state approximation", "Solve for ES complex", "Derive v₀ equation"], 
                 "v₀ = Vmax[S]/(Km + [S])"),
                (f"Calculate the partition function for a diatomic molecule including translational, rotational, and vibrational contributions.",
                 ["Write Q = Q_trans × Q_rot × Q_vib", "Calculate each component", "Combine results"], 
                 "Complete statistical thermodynamic partition function"),
                (f"Use computational methods to predict the HOMO-LUMO gap of conjugated system.",
                 ["Apply Hückel MO theory", "Calculate energy levels", "Determine gap"], 
                 "ΔE ≈ 2βsin(π/(2N+2)) for N double bonds")
            ]
    
    elif strand == "bioearth":
        if grade <= 4:
            return [
                (f"Calculate the Hardy-Weinberg equilibrium frequencies for a population with p=0.7, q=0.3.",
                 ["Apply p², 2pq, q² formulas", "Calculate genotype frequencies", "Verify equilibrium"], 
                 "p²=0.49, 2pq=0.42, q²=0.09"),
                (f"Determine the water potential of a cell with Ψs = -0.7 MPa and Ψp = 0.3 MPa.",
                 ["Use Ψ = Ψs + Ψp", "Substitute values", "Calculate total"], 
                 "Ψ = -0.4 MPa"),
                (f"Calculate the rate of photosynthesis at different light intensities using the Michaelis-Menten model.",
                 ["Apply P = Pmax × I/(I + KI)", "Substitute parameters", "Compute rate"], 
                 "Rate in μmol CO₂/m²/s")
            ]
        elif grade <= 8:
            return [
                (f"Analyze the feedback loops in the lac operon system and predict gene expression patterns.",
                 ["Identify regulatory elements", "Map feedback mechanisms", "Predict expression"], 
                 "Inducible system with catabolite repression"),
                (f"Model population dynamics using the Lotka-Volterra equations.",
                 ["Write predator-prey equations", "Analyze equilibrium points", "Predict oscillations"], 
                 "Cyclic population dynamics"),
                (f"Calculate the carbon flux through the Calvin cycle under different environmental conditions.",
                 ["Map carbon flow", "Apply stoichiometric constraints", "Compute fluxes"], 
                 "3 CO₂ fixed per cycle with energy requirements")
            ]
        else:
            return [
                (f"Design a CRISPR-Cas9 gene editing strategy for a specific genetic mutation.",
                 ["Design guide RNA", "Check off-target effects", "Plan repair template"], 
                 "Complete gene editing protocol"),
                (f"Model climate feedback mechanisms using coupled atmosphere-ocean equations.",
                 ["Write coupled differential equations", "Include feedback terms", "Analyze stability"], 
                 "Climate sensitivity and tipping point analysis"),
                (f"Apply phylogenetic comparative methods to analyze trait evolution across species.",
                 ["Construct phylogenetic tree", "Apply comparative methods", "Test evolutionary hypotheses"], 
                 "Statistical analysis of evolutionary patterns")
            ]
    
    else:  # applied
        if grade <= 4:
            return [
                (f"Implement gradient descent algorithm to find minimum of f(x,y) = x² + 2y².",
                 ["Compute gradients", "Update rule: x_new = x_old - α∇f", "Iterate to convergence"], 
                 "Minimum at (0,0) with value 0"),
                (f"Design a hypothesis test comparing two population means with unequal variances.",
                 ["Formulate hypotheses", "Calculate test statistic", "Make decision"], 
                 "Welch's t-test with appropriate degrees of freedom"),
                (f"Create a machine learning pipeline for binary classification.",
                 ["Data preprocessing", "Model selection and training", "Performance evaluation"], 
                 "Complete ML workflow with cross-validation")
            ]
        elif grade <= 8:
            return [
                (f"Optimize a supply chain network using linear programming.",
                 ["Define decision variables", "Set up objective function", "Add constraints"], 
                 "Optimal solution with sensitivity analysis"),
                (f"Apply principal component analysis to reduce dimensionality of genomic data.",
                 ["Standardize data", "Compute covariance matrix", "Extract principal components"], 
                 "Reduced dimensional representation preserving variance"),
                (f"Design a Monte Carlo simulation for risk assessment in financial portfolio.",
                 ["Define probability distributions", "Generate random scenarios", "Analyze outcomes"], 
                 "Value at Risk (VaR) calculation with confidence intervals")
            ]
        else:
            return [
                (f"Develop a deep neural network architecture for image recognition.",
                 ["Design network layers", "Implement backpropagation", "Optimize hyperparameters"], 
                 "Convolutional Neural Network with transfer learning"),
                (f"Apply reinforcement learning to solve a complex control problem.",
                 ["Define Markov decision process", "Implement Q-learning or policy gradient", "Train and evaluate"], 
                 "Optimal policy with convergence analysis"),
                (f"Design a computational fluid dynamics simulation for aerodynamic optimization.",
                 ["Set up Navier-Stokes equations", "Apply numerical methods", "Validate results"], 
                 "CFD solution with mesh convergence study")
            ]

def build_enhanced_questions(course: dict) -> List[dict]:
    """Create sophisticated, college-level assessment questions."""
    grade = course["grade"]
    strand = course["strand"]
    title = course["title"]
    topic = course.get("display_topic") or inj.course_topic(course)
    focus = course["focus_points"]
    
    # Create deterministic random generator for consistent questions
    seed = sum(ord(ch) for ch in title) + grade * 131 + len(topic) * 17
    rng = random.Random(seed)
    
    questions = []
    
    def add_question(text, correct, wrongs, explanation, idx=None):
        questions.append(
            inj.make_question(
                text, correct, wrongs, explanation,
                idx if idx is not None else len(questions) + 1
            )
        )
    
    # Core competency questions
    add_question(
        f"({topic}) Which mathematical framework is most appropriate for analyzing this advanced topic?",
        ["Differential equations and dynamical systems", "Basic arithmetic operations", "Simple probability calculations", "Elementary geometry"][0],
        ["Basic arithmetic operations", "Simple probability calculations", "Elementary geometry"],
        "Advanced topics require sophisticated mathematical tools for proper analysis and prediction."
    )
    
    add_question(
        f"({topic}) In professional research, what is the primary purpose of developing theoretical models?",
        "To predict behavior, guide experiments, and provide mechanistic understanding",
        ["To memorize facts without application", "To avoid experimental validation", "To complicate simple problems"],
        "Theoretical models serve as predictive frameworks that connect fundamental principles to observable phenomena."
    )
    
    # Advanced problem-solving questions
    problems = create_advanced_problem_set(strand, grade)
    for i, (problem_text, steps, answer) in enumerate(problems[:2]):
        add_question(
            f"({topic}) Advanced Problem {i+1}: {problem_text}",
            answer,
            [f"Incorrect approach: {steps[0]}", "Partial solution", "Computational error"],
            f"Solution requires: {' → '.join(steps)}"
        )
    
    # Research methodology questions
    add_question(
        f"({topic}) When designing experiments at this level, which consideration is most critical?",
        "Control of confounding variables and statistical power analysis",
        ["Making results look impressive", "Using only one trial", "Ignoring uncertainty"],
        "Rigorous experimental design ensures validity and reproducibility of findings."
    )
    
    add_question(
        f"({topic}) How does computational modeling enhance understanding in {strand}?",
        "By enabling simulation of complex systems that are analytically intractable",
        ["By replacing all laboratory work", "By eliminating need for theory", "By simplifying problems excessively"],
        "Computational models provide insights into system behavior across multiple scales and conditions."
    )
    
    # Cross-disciplinary connections
    add_question(
        f"({topic}) Which mathematical concept from linear algebra is most applicable to this {strand} problem?",
        ["Eigenvalue problems and matrix transformations", "Basic arithmetic", "Simple counting", "Elementary fractions"][0],
        ["Basic arithmetic", "Simple counting", "Elementary fractions"],
        "Linear algebra provides powerful tools for analyzing multi-dimensional systems and transformations."
    )
    
    # Professional applications
    add_question(
        f"({topic}) In industry, what is the primary application of knowledge in this area?",
        "Development of new technologies and solutions to real-world problems",
        ["Academic exercises only", "Theoretical discussions without impact", "Memorization for tests"],
        "Advanced knowledge drives innovation and practical applications across multiple sectors."
    )
    
    # Data interpretation and analysis
    add_question(
        f"({topic}) When analyzing experimental data, which statistical approach is most appropriate for complex datasets?",
        "Multivariate analysis with proper uncertainty quantification",
        ["Looking only at averages", "Ignoring variability", "Using only visual inspection"],
        "Sophisticated statistical methods are necessary to extract meaningful insights from complex data."
    )
    
    # Ethical considerations
    add_question(
        f"({topic}) What ethical consideration is most important when conducting advanced research?",
        "Integrity in data reporting and appropriate attribution",
        ["Getting results quickly", "Minimizing costs regardless of quality", "Keeping all data secret"],
        "Research ethics ensure credibility, reproducibility, and responsible advancement of knowledge."
    )
    
    # Future directions and innovation
    add_question(
        f"({topic}) Which emerging technology will likely have the greatest impact on this field?",
        ["Artificial intelligence and machine learning integration", "Traditional methods only", "Manual calculations", "Basic tools"][0],
        ["Traditional methods only", "Manual calculations", "Basic tools"],
        "AI and machine learning are revolutionizing how we approach complex problems and data analysis."
    )
    
    # Simulation-specific questions
    sims = course["sims"]
    if len(sims) >= 2:
        add_question(
            f"({topic}) Which combination of simulations provides the most comprehensive understanding?",
            f"{sims[0]} and {sims[1]}",
            [f"{sims[0]} only", f"{sims[1]} only", "No simulations needed"],
            "Multiple simulations provide complementary perspectives on complex phenomena."
        )
    
    # Reorder questions
    for i, q in enumerate(questions, 1):
        q["order_index"] = i
    
    return questions

def make_enhanced_blueprints() -> List[dict]:
    """Create comprehensive course blueprints for all 65 courses."""
    courses = []
    
    for grade in range(1, 14):  # Grades 1-13
        grade_index = grade - 1
        
        for strand in inj.STRANDS:
            topic = COLLEGE_TOPICS[strand][grade_index]
            title = f"College Level {grade}: {strand.upper()} - {topic}"
            
            # Select appropriate simulations for this level
            sims = inj.pick_sims(strand, grade_index)
            if len(sims) < 2:
                # Add more simulations for college level
                extended_cycle = inj.SIM_CYCLES.get(strand, list(inj.SIMS.keys())[:20])
                while len(sims) < 3:
                    additional_sim = extended_cycle[(grade_index * 3 + len(sims)) % len(extended_cycle)]
                    if additional_sim not in sims:
                        sims.append(additional_sim)
            
            course = {
                "grade": grade,
                "strand": strand,
                "title": title,
                "display_topic": topic,
                "description": (
                    f"Advanced college-level {strand} course for Grade {grade} focusing on {topic}. "
                    f"This comprehensive course integrates theoretical foundations, computational methods, "
                    f"laboratory investigations, and real-world applications. Students develop professional-level "
                    f"competencies in {', '.join(COMPETENCIES[strand][:2])} and prepare for advanced research "
                    f"or industry careers. Includes interactive PhET simulations, rigorous problem sets, "
                    f"and research-based assessments."
                ),
                "focus_points": list(COMPETENCIES[strand]),
                "sims": sims[:3],  # Ensure exactly 3 sims
            }
            courses.append(course)
    
    return courses

def upsert_enhanced_course(cursor, course, creator_id, rng):
    """Insert or update enhanced college-level course."""
    title = course["title"]
    grade = course["grade"]
    content = build_enhanced_content(course)
    questions = build_enhanced_questions(course)
    
    # Check if course exists (will replace existing)
    cursor.execute(
        "SELECT id FROM courses WHERE title=%s AND grade_level=%s ORDER BY id ASC LIMIT 1",
        (title, grade),
    )
    row = cursor.fetchone()
    
    if row:
        course_id = row["id"]
        cursor.execute(
            "UPDATE courses SET title=%s, description=%s, content=%s, status='approved' WHERE id=%s",
            (title, course["description"], content, course_id),
        )
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
    
    # Delete existing questions and insert new ones
    cursor.execute("DELETE FROM course_questions WHERE course_id=%s", (course_id,))
    qids = []
    
    for raw_q in questions:
        q = inj.shuffle_options(raw_q, rng)
        cursor.execute(
            """
            INSERT INTO course_questions
            (course_id, question_text, question_type, options, correct_answer, explanation, points, order_index)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                course_id,
                q["question_text"],
                q["question_type"],
                json.dumps(q["options"]),
                q["correct_answer"],
                q["explanation"],
                q["points"],
                q["order_index"],
            ),
        )
        cursor.execute("SELECT LAST_INSERT_ID() AS id")
        qids.append(cursor.fetchone()["id"])
    
    # Hydrate content with question placeholders
    hydrated = content + "".join(
        [inj.placeholder_html(qid, idx) for idx, qid in enumerate(qids, 1)]
    )
    cursor.execute("UPDATE courses SET content=%s, status='approved' WHERE id=%s", (hydrated, course_id))
    
    return {
        "id": course_id, 
        "grade": grade, 
        "title": title, 
        "questions": len(qids), 
        "action": action
    }

def main() -> int:
    """Main execution function for enhanced college course injection."""
    
    # Load PhET simulations from frontend script
    script_js = Path(__file__).resolve().parent / "veelearn-frontend" / "script.js"
    if script_js.is_file():
        extra_sims = load_phet_titles_urls_from_script(script_js)
        before_count = len(inj.SIMS)
        inj.SIMS.update(extra_sims)
        print(f"Enhanced PhET library: +{len(inj.SIMS) - before_count} simulations (total: {len(inj.SIMS)})")
    else:
        print("WARNING: script.js not found - using built-in simulation library only")
    
    # Verify database configuration
    cfg = inj.AIVEN_CONFIG
    if not cfg.get("password"):
        print("ERROR: Set MYSQLPASSWORD environment variable with your database password")
        return 1
    
    # Generate enhanced course blueprints
    courses = make_enhanced_blueprints()
    if len(courses) != 65:
        print(f"ERROR: Expected 65 courses, generated {len(courses)}")
        return 1
    
    print(f"Generated {len(courses)} enhanced college-level courses")
    
    # Initialize random number generator
    rng = random.Random(int(os.getenv("COURSE_RANDOM_SEED", "20260405")))
    
    # Connect to database
    print("Connecting to MySQL database...")
    try:
        conn = pymysql.connect(**cfg)
        print("Database connection established successfully")
    except Exception as exc:
        print(f"Database connection failed: {exc}")
        return 1
    
    processed_courses = []
    
    try:
        cursor = conn.cursor()
        creator_id = inj.resolve_creator_id(cursor)
        print(f"Using creator_id: {creator_id}")
        
        # Process each course
        for i, course in enumerate(courses, 1):
            result = upsert_enhanced_course(cursor, course, creator_id, rng)
            processed_courses.append(result)
            
            print(
                f"[{i:02d}/65] Grade {result['grade']:02d} | {result['action'].upper()} | "
                f"ID {result['id']} | {result['questions']} questions | {course['strand']}"
            )
        
        # Commit all changes
        conn.commit()
        print("All courses successfully committed to database")
        
        # Verification
        course_ids = [x["id"] for x in processed_courses]
        verification_rows = inj.verify(cursor, course_ids)
        
        # Organize results by grade
        grade_stats = {}
        for row in verification_rows:
            grade = int(row["grade_level"])
            if grade not in grade_stats:
                grade_stats[grade] = {"courses": 0, "questions": 0, "placeholders": 0}
            grade_stats[grade]["courses"] += 1
            grade_stats[grade]["questions"] += int(row["q_count"])
            grade_stats[grade]["placeholders"] += int(row["p_count"])
        
        # Display comprehensive results
        print("\n" + "="*60)
        print("ENHANCED COLLEGE-LEVEL COURSE INJECTION COMPLETE")
        print("="*60)
        
        total_courses = 0
        total_questions = 0
        
        for grade in range(1, 14):
            stats = grade_stats.get(grade, {"courses": 0, "questions": 0, "placeholders": 0})
            total_courses += stats["courses"]
            total_questions += stats["questions"]
            
            print(f"Grade {grade:02d}: {stats['courses']} courses, {stats['questions']} questions, "
                  f"{stats['placeholders']} placeholders")
        
        print(f"\nTOTALS: {total_courses} courses, {total_questions} questions")
        
        # Validation checks
        expected_courses_per_grade = 5
        all_grades_complete = all(
            grade_stats.get(g, {}).get("courses") == expected_courses_per_grade 
            for g in range(1, 14)
        )
        
        questions_match_placeholders = all(
            grade_stats.get(g, {}).get("questions") == grade_stats.get(g, {}).get("placeholders")
            for g in range(1, 14)
        )
        
        print(f"All grades have {expected_courses_per_grade} courses: {'✓ PASS' if all_grades_complete else '✗ FAIL'}")
        print(f"Questions match placeholders: {'✓ PASS' if questions_match_placeholders else '✗ FAIL'}")
        
        if all_grades_complete and questions_match_placeholders:
            print("\n🎉 Enhanced college-level injection completed successfully!")
            print("All 65 courses have been updated with professional, comprehensive content.")
        else:
            print("\n⚠️ Some validation checks failed - please review the output above")
            
    except Exception as exc:
        try:
            conn.rollback()
            print("Database changes rolled back due to error")
        except Exception:
            pass
        print(f"ERROR during processing: {exc}")
        import traceback
        traceback.print_exc()
        return 1
        
    finally:
        conn.close()
        print("Database connection closed")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
