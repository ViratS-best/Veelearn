# Quick fix: Just the chemistry course content without indentation

CHEMISTRY_CONTENT = """
<h1>Chemistry Fundamentals - Complete Guide</h1>

<h2>📚 Course Overview</h2>
<p>Master the essential concepts of chemistry from atoms and molecules to reactions and equilibrium. This course uses interactive PhET simulators to visualize chemical phenomena.</p>

<hr>

<h2>Module 1: Atomic Structure & Periodic Table</h2>
<p><strong>What you'll learn:</strong> Atoms, electrons, protons, neutrons, and periodic table organization.</p>

<h3>1.1 Structure of the Atom</h3>
<p>All matter is made of atoms with:</p>
<ul>
<li><strong>Nucleus:</strong> Contains protons and neutrons</li>
<li><strong>Electron Cloud:</strong> Contains electrons</li>
<li>Atoms are electrically neutral when protons = electrons</li>
</ul>

<p><strong>Interactive Simulator:</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/build-an-atom/latest/build-an-atom_all.html" width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>

<hr>

<h2>Module 2: Chemical Bonding</h2>

<h3>2.1 Ionic vs Covalent Bonding</h3>
<p><strong>Ionic:</strong> Electrons transfer completely. <strong>Covalent:</strong> Electrons are shared.</p>

<p><strong>Interactive Simulator:</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/molecule-shapes/latest/molecule-shapes_all.html" width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>

<hr>

<h2>Module 3: Chemical Reactions</h2>

<p><strong>Types:</strong> Synthesis, Decomposition, Displacement, Combustion</p>

<p><strong>Interactive Simulator:</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/reactants-products-salts/latest/reactants-products-salts_all.html" width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>

<hr>

<h2>Module 4: Acids, Bases & pH</h2>

<h3>The pH Scale</h3>
<ul>
<li>pH 0-7: Acidic</li>
<li>pH = 7: Neutral</li>
<li>pH 7-14: Basic</li>
</ul>

<p><strong>Interactive Simulator:</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/ph-scale/latest/ph-scale_all.html" width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>

<hr>

<h2>Module 5: Thermochemistry</h2>

<ul>
<li><strong>Exothermic:</strong> Releases energy</li>
<li><strong>Endothermic:</strong> Absorbs energy</li>
</ul>

<p><strong>You've completed Chemistry! Take the quiz to test your knowledge.</strong>
"""

CHEMISTRY_QUESTIONS = [
    {"question_text": "How many protons does a carbon atom have?", "question_type": "multiple_choice", "options": ["8", "7", "5", "6"], "correct_answer": "6", "explanation": "Carbon has atomic number 6, so 6 protons.", "points": 1, "order_index": 1},
    {"question_text": "What type of bond shares electrons between atoms?", "question_type": "multiple_choice", "options": ["Metallic bond", "Hydrogen bond", "Covalent bond", "Ionic bond"], "correct_answer": "Covalent bond", "explanation": "Covalent bonds form when atoms share electrons.", "points": 1, "order_index": 2},
    {"question_text": "What is the pH of pure water at 25°C?", "question_type": "multiple_choice", "options": ["0", "14", "7", "10"], "correct_answer": "7", "explanation": "Pure water has a pH of 7 (neutral).", "points": 1, "order_index": 3},
    {"question_text": "Which type of reaction involves a compound breaking into simpler substances?", "question_type": "multiple_choice", "options": ["Synthesis reaction", "Combustion reaction", "Decomposition reaction", "Double displacement"], "correct_answer": "Decomposition reaction", "explanation": "Decomposition breaks down compounds into simpler substances.", "points": 1, "order_index": 4},
    {"question_text": "An exothermic reaction is one that:", "question_type": "multiple_choice", "options": ["Requires heat from surroundings", "Absorbs energy (ΔH > 0)", "Releases energy (ΔH < 0)", "Changes color"], "correct_answer": "Releases energy (ΔH < 0)", "explanation": "Exothermic reactions release energy to surroundings.", "points": 1, "order_index": 5},
    {"question_text": "What is the correct formula for sodium chloride?", "question_type": "multiple_choice", "options": ["NaClₙ", "Na₂Cl", "NaCl₂", "NaCl"], "correct_answer": "NaCl", "explanation": "Na⁺ bonds with Cl⁻ to form NaCl (table salt).", "points": 1, "order_index": 6},
    {"question_text": "Which substance is a strong acid?", "question_type": "multiple_choice", "options": ["Vinegar (acetic acid)", "Hydrochloric acid (HCl)", "Lemon juice (citric acid)", "Water"], "correct_answer": "Hydrochloric acid (HCl)", "explanation": "HCl is a strong acid that completely ionizes in water.", "points": 1, "order_index": 7},
    {"question_text": "In the reaction 2H₂ + O₂ → 2H₂O, how many moles of H₂O are produced from 4 moles of H₂?", "question_type": "multiple_choice", "options": ["1 mole", "2 moles", "4 moles", "8 moles"], "correct_answer": "4 moles", "explanation": "The stoichiometric ratio is 2:2 (or 1:1) for H₂:H₂O.", "points": 1, "order_index": 8},
]
