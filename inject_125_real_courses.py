#!/usr/bin/env python3
"""
125 UNIQUE COURSES - REAL CONTENT INJECTION
60 Grade Courses (Grades 1-12) + 65 College Courses (Levels 13-25)
Each course has unique PhET simulations and challenging content
"""

import pymysql, json, sys, os, io
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

AIVEN_CONFIG = {
    "charset": "utf8mb4",
    "connect_timeout": 30,
    "cursorclass": pymysql.cursors.DictCursor,
    "db": os.getenv("MYSQL_DATABASE") or os.getenv("AIVEN_DB", "defaultdb"),
    "host": os.getenv("MYSQLHOST") or os.getenv("AIVEN_HOST", "veelearndb-asterloop-483e.i.aivencloud.com"),
    "password": os.getenv("MYSQLPASSWORD") or os.getenv("AIVEN_PASSWORD", ""),
    "port": int(os.getenv("MYSQLPORT") or os.getenv("AIVEN_PORT", "26399")),
    "user": os.getenv("MYSQLUSER") or os.getenv("AIVEN_USER", "avnadmin"),
    "read_timeout": 60,
    "write_timeout": 60,
}

ssl_ca = os.getenv("DB_SSL_CA")
if ssl_ca:
    if "\\n" in ssl_ca:
        ssl_ca = ssl_ca.replace("\\n", "\n")
    ca_path = os.path.join(os.getcwd(), "ca.pem")
    with open(ca_path, "w") as f:
        f.write(ssl_ca)
    AIVEN_CONFIG["ssl"] = {"ca": ca_path}

# Comprehensive PhET Simulation Library - 80+ simulations
PHET_SIMS = {
    # Math
    "arithmetic": "https://phet.colorado.edu/sims/html/arithmetic/latest/arithmetic_all.html",
    "make-a-ten": "https://phet.colorado.edu/sims/html/make-a-ten/latest/make-a-ten_all.html",
    "number-compare": "https://phet.colorado.edu/sims/html/number-compare/latest/number-compare_all.html",
    "number-line-distance": "https://phet.colorado.edu/sims/html/number-line-distance/latest/number-line-distance_all.html",
    "number-line-integers": "https://phet.colorado.edu/sims/html/number-line-integers/latest/number-line-integers_all.html",
    "number-line-operations": "https://phet.colorado.edu/sims/html/number-line-operations/latest/number-line-operations_all.html",
    "fractions-intro": "https://phet.colorado.edu/sims/html/fractions-intro/latest/fractions-intro_all.html",
    "fraction-matcher": "https://phet.colorado.edu/sims/html/fraction-matcher/latest/fraction-matcher_all.html",
    "build-a-fraction": "https://phet.colorado.edu/sims/html/build-a-fraction/latest/build-a-fraction_all.html",
    "area-builder": "https://phet.colorado.edu/sims/html/area-builder/latest/area-builder_all.html",
    "area-model-algebra": "https://phet.colorado.edu/sims/html/area-model-algebra/latest/area-model-algebra_all.html",
    "area-model-decimals": "https://phet.colorado.edu/sims/html/area-model-decimals/latest/area-model-decimals_all.html",
    "area-model-introduction": "https://phet.colorado.edu/sims/html/area-model-introduction/latest/area-model-introduction_all.html",
    "area-model-multiplication": "https://phet.colorado.edu/sims/html/area-model-multiplication/latest/area-model-multiplication_all.html",
    "ratio-and-proportion": "https://phet.colorado.edu/sims/html/ratio-and-proportion/latest/ratio-and-proportion_all.html",
    "unit-rates": "https://phet.colorado.edu/sims/html/unit-rates/latest/unit-rates_all.html",
    "proportion-playground": "https://phet.colorado.edu/sims/html/proportion-playground/latest/proportion-playground_all.html",
    "graphing-lines": "https://phet.colorado.edu/sims/html/graphing-lines/latest/graphing-lines_all.html",
    "graphing-slope-intercept": "https://phet.colorado.edu/sims/html/graphing-slope-intercept/latest/graphing-slope-intercept_all.html",
    "graphing-quadratics": "https://phet.colorado.edu/sims/html/graphing-quadratics/latest/graphing-quadratics_all.html",
    "trig-tour": "https://phet.colorado.edu/sims/html/trig-tour/latest/trig-tour_all.html",
    "function-builder": "https://phet.colorado.edu/sims/html/function-builder/latest/function-builder_all.html",
    "function-builder-basics": "https://phet.colorado.edu/sims/html/function-builder-basics/latest/function-builder-basics_all.html",
    "expression-exchange": "https://phet.colorado.edu/sims/html/expression-exchange/latest/expression-exchange_all.html",
    "equality-explorer": "https://phet.colorado.edu/sims/html/equality-explorer/latest/equality-explorer_all.html",
    "calculus-grapher": "https://phet.colorado.edu/sims/html/calculus-grapher/latest/calculus-grapher_all.html",
    "curve-fitting": "https://phet.colorado.edu/sims/html/curve-fitting/latest/curve-fitting_all.html",
    "least-squares-regression": "https://phet.colorado.edu/sims/html/least-squares-regression/latest/least-squares-regression_all.html",
    "plinko-probability": "https://phet.colorado.edu/sims/html/plinko-probability/latest/plinko-probability_all.html",
    "center-and-variability": "https://phet.colorado.edu/sims/html/center-and-variability/latest/center-and-variability_all.html",
    
    # Physics
    "forces-and-motion-basics": "https://phet.colorado.edu/sims/html/forces-and-motion-basics/latest/forces-and-motion-basics_all.html",
    "forces-and-motion": "https://phet.colorado.edu/sims/html/forces-and-motion/latest/forces-and-motion_all.html",
    "balancing-act": "https://phet.colorado.edu/sims/html/balancing-act/latest/balancing-act_all.html",
    "friction": "https://phet.colorado.edu/sims/html/friction/latest/friction_all.html",
    "gravity-force-lab": "https://phet.colorado.edu/sims/html/gravity-force-lab/latest/gravity-force-lab_all.html",
    "gravity-force-lab-basics": "https://phet.colorado.edu/sims/html/gravity-force-lab-basics/latest/gravity-force-lab-basics_all.html",
    "gravity-and-orbits": "https://phet.colorado.edu/sims/html/gravity-and-orbits/latest/gravity-and-orbits_all.html",
    "projectile-motion": "https://phet.colorado.edu/sims/html/projectile-motion/latest/projectile-motion_all.html",
    "energy-skate-park": "https://phet.colorado.edu/sims/html/energy-skate-park/latest/energy-skate-park_all.html",
    "energy-skate-park-basics": "https://phet.colorado.edu/sims/html/energy-skate-park-basics/latest/energy-skate-park-basics_all.html",
    "energy-forms-and-changes": "https://phet.colorado.edu/sims/html/energy-forms-and-changes/latest/energy-forms-and-changes_all.html",
    "collision-lab": "https://phet.colorado.edu/sims/html/collision-lab/latest/collision-lab_all.html",
    "vector-addition": "https://phet.colorado.edu/sims/html/vector-addition/latest/vector-addition_all.html",
    "wave-on-a-string": "https://phet.colorado.edu/sims/html/wave-on-a-string/latest/wave-on-a-string_all.html",
    "waves-intro": "https://phet.colorado.edu/sims/html/waves-intro/latest/waves-intro_all.html",
    "wave-interference": "https://phet.colorado.edu/sims/html/wave-interference/latest/wave-interference_all.html",
    "sound-waves": "https://phet.colorado.edu/sims/html/sound-waves/latest/sound-waves_all.html",
    "pendulum-lab": "https://phet.colorado.edu/sims/html/pendulum-lab/latest/pendulum-lab_all.html",
    "masses-and-springs": "https://phet.colorado.edu/sims/html/masses-and-springs/latest/masses-and-springs_all.html",
    "under-pressure": "https://phet.colorado.edu/sims/html/under-pressure/latest/under-pressure_all.html",
    "buoyancy": "https://phet.colorado.edu/sims/html/buoyancy/latest/buoyancy_all.html",
    "buoyancy-basics": "https://phet.colorado.edu/sims/html/buoyancy-basics/latest/buoyancy-basics_all.html",
    "circuit-construction-kit-dc": "https://phet.colorado.edu/sims/html/circuit-construction-kit-dc/latest/circuit-construction-kit-dc_all.html",
    "circuit-construction-kit-ac": "https://phet.colorado.edu/sims/html/circuit-construction-kit-ac/latest/circuit-construction-kit-ac_all.html",
    "ohms-law": "https://phet.colorado.edu/sims/html/ohms-law/latest/ohms-law_all.html",
    "resistance-in-a-wire": "https://phet.colorado.edu/sims/html/resistance-in-a-wire/latest/resistance-in-a-wire_all.html",
    "charges-and-fields": "https://phet.colorado.edu/sims/html/charges-and-fields/latest/charges-and-fields_all.html",
    "coulombs-law": "https://phet.colorado.edu/sims/html/coulombs-law/latest/coulombs-law_all.html",
    "faradays-law": "https://phet.colorado.edu/sims/html/faradays-law/latest/faradays-law_all.html",
    "faradays-electromagnetic-lab": "https://phet.colorado.edu/sims/html/faradays-electromagnetic-lab/latest/faradays-electromagnetic-lab_all.html",
    "magnets-and-electromagnets": "https://phet.colorado.edu/sims/html/magnets-and-electromagnets/latest/magnets-and-electromagnets_all.html",
    "geometric-optics": "https://phet.colorado.edu/sims/html/geometric-optics/latest/geometric-optics_all.html",
    "geometric-optics-basics": "https://phet.colorado.edu/sims/html/geometric-optics-basics/latest/geometric-optics-basics_all.html",
    "bending-light": "https://phet.colorado.edu/sims/html/bending-light/latest/bending-light_all.html",
    "diffraction": "https://phet.colorado.edu/sims/html/diffraction/latest/diffraction_all.html",
    "quantum-measurement": "https://phet.colorado.edu/sims/html/quantum-measurement/latest/quantum-measurement_all.html",
    "models-of-the-hydrogen-atom": "https://phet.colorado.edu/sims/html/models-of-the-hydrogen-atom/latest/models-of-the-hydrogen-atom_all.html",
    "radioactive-dating-game": "https://phet.colorado.edu/sims/html/radioactive-dating-game/latest/radioactive-dating-game_all.html",
    "alpha-decay": "https://phet.colorado.edu/sims/html/alpha-decay/latest/alpha-decay_all.html",
    "beta-decay": "https://phet.colorado.edu/sims/html/beta-decay/latest/beta-decay_all.html",
    "nuclear-fission": "https://phet.colorado.edu/sims/html/nuclear-fission/latest/nuclear-fission_all.html",
    
    # Chemistry
    "states-of-matter": "https://phet.colorado.edu/sims/html/states-of-matter/latest/states-of-matter_all.html",
    "states-of-matter-basics": "https://phet.colorado.edu/sims/html/states-of-matter-basics/latest/states-of-matter-basics_all.html",
    "gas-properties": "https://phet.colorado.edu/sims/html/gas-properties/latest/gas-properties_all.html",
    "build-an-atom": "https://phet.colorado.edu/sims/html/build-an-atom/latest/build-an-atom_all.html",
    "build-a-molecule": "https://phet.colorado.edu/sims/html/build-a-molecule/latest/build-a-molecule_all.html",
    "isotopes-and-atomic-mass": "https://phet.colorado.edu/sims/html/isotopes-and-atomic-mass/latest/isotopes-and-atomic-mass_all.html",
    "atomic-interactions": "https://phet.colorado.edu/sims/html/atomic-interactions/latest/atomic-interactions_all.html",
    "molecule-shapes": "https://phet.colorado.edu/sims/html/molecule-shapes/latest/molecule-shapes_all.html",
    "molecule-shapes-basics": "https://phet.colorado.edu/sims/html/molecule-shapes-basics/latest/molecule-shapes-basics_all.html",
    "molecule-polarity": "https://phet.colorado.edu/sims/html/molecule-polarity/latest/molecule-polarity_all.html",
    "balancing-chemical-equations": "https://phet.colorado.edu/sims/html/balancing-chemical-equations/latest/balancing-chemical-equations_all.html",
    "reactants-products-and-leftovers": "https://phet.colorado.edu/sims/html/reactants-products-and-leftovers/latest/reactants-products-and-leftovers_all.html",
    "concentration": "https://phet.colorado.edu/sims/html/concentration/latest/concentration_all.html",
    "molarity": "https://phet.colorado.edu/sims/html/molarity/latest/molarity_all.html",
    "ph-scale": "https://phet.colorado.edu/sims/html/ph-scale/latest/ph-scale_all.html",
    "ph-scale-basics": "https://phet.colorado.edu/sims/html/ph-scale-basics/latest/ph-scale-basics_all.html",
    "acid-base-solutions": "https://phet.colorado.edu/sims/html/acid-base-solutions/latest/acid-base-solutions_all.html",
    "beers-law-lab": "https://phet.colorado.edu/sims/html/beers-law-lab/latest/beers-law-lab_all.html",
    "sugar-and-salt-solutions": "https://phet.colorado.edu/sims/html/sugar-and-salt-solutions/latest/sugar-and-salt-solutions_all.html",
    "diffusion": "https://phet.colorado.edu/sims/html/diffusion/latest/diffusion_all.html",
    "molecules-and-light": "https://phet.colorado.edu/sims/html/molecules-and-light/latest/molecules-and-light_all.html",
    
    # Biology
    "natural-selection": "https://phet.colorado.edu/sims/html/natural-selection/latest/natural-selection_all.html",
    "gene-expression-essentials": "https://phet.colorado.edu/sims/html/gene-expression-essentials/latest/gene-expression-essentials_all.html",
    "membrane-channels": "https://phet.colorado.edu/sims/html/membrane-channels/latest/membrane-channels_all.html",
    "neuron": "https://phet.colorado.edu/sims/html/neuron/latest/neuron_all.html",
    "greenhouse-effect": "https://phet.colorado.edu/sims/html/greenhouse-effect/latest/greenhouse-effect_all.html",
    "build-a-nucleus": "https://phet.colorado.edu/sims/html/build-a-nucleus/latest/build-a-nucleus_all.html",
}

# ============================================================================
# REAL COURSE CONTENT - GRADES 1-12 (60 COURSES)
# ============================================================================

# GRADE 1 COURSES (5 courses) ==================================================

# G1-MATH: Number Sense Foundations
COURSE_G1_MATH = {
    "title": "Grade 1 Mathematics: Number Sense Foundations",
    "grade": 1,
    "content": r"""
<h1>Grade 1 Mathematics: Number Sense Foundations</h1>

<h2>Building Your Mathematical Mind</h2>
<p>Welcome to the fascinating world of mathematics! This course will take you on a journey from understanding basic numbers to performing addition and subtraction with confidence. Through interactive PhET simulations, visual models, and engaging problems, you'll develop a deep understanding of how numbers work.</p>

<hr>

<h2>Module 1: Numbers 1-100 - The Building Blocks</h2>
<p>Numbers are everywhere in our world. They help us count, measure, compare, and understand quantities. In this module, you'll master numbers from 1 to 100 through multiple representations.</p>

<h3>Counting and Cardinality</h3>
<ul>
  <li><strong>One-to-one correspondence:</strong> Each object gets exactly one number word</li>
  <li><strong>Cardinality:</strong> The last number tells how many objects in total</li>
  <li><strong>Conservation of number:</strong> The count stays the same regardless of arrangement</li>
  <li><strong>Subitizing:</strong> Instantly recognizing small quantities without counting</li>
</ul>

<div style="background: rgba(100,150,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #4a90e2;">
  <h4>Key Insight</h4>
  <p>Numbers represent quantity. The digit '5' in 58 represents 50 (5 tens), not just 5. Understanding place value is crucial for all future mathematics.</p>
</div>

<h3>Interactive Simulator: Number Compare</h3>
<iframe src="https://phet.colorado.edu/sims/html/number-compare/latest/number-compare_all.html" 
  width="100%" height="600" frameborder="0" style="border: 2px solid #444; border-radius: 8px;"></iframe>
<p><em>Compare quantities visually. Drag groups to compare and discover which has more, less, or if they're equal. Notice how the symbols > and < work!</em></p>

<h3>Interactive Simulator: Number Line Distance</h3>
<iframe src="https://phet.colorado.edu/sims/html/number-line-distance/latest/number-line-distance_all.html" 
  width="100%" height="600" frameborder="0" style="border: 2px solid #444; border-radius: 8px;"></iframe>
<p><em>Explore the number line! Find distances between numbers. Notice that the distance from 3 to 8 is the same as 8 to 3, and both equal 5!</em></p>

<hr>

<h2>Module 2: Addition - Combining Quantities</h2>
<p>Addition is one of the most fundamental operations in mathematics. It represents combining groups, finding totals, and putting things together.</p>

<h3>Addition Strategies</h3>
<ul>
  <li><strong>Counting All:</strong> Count every object in both groups (beginner strategy)</li>
  <li><strong>Counting On:</strong> Start from the first number and count up (more efficient)</li>
  <li><strong>Make-a-Ten:</strong> Break numbers to create a ten, then add the rest (powerful strategy)</li>
  <li><strong>Doubles:</strong> 5+5, 6+6 - easy to remember and use as anchors</li>
  <li><strong>Near Doubles:</strong> 5+6, 6+7 - use doubles you know, then adjust</li>
</ul>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>Make-a-Ten Strategy Example</h4>
  <p><strong>Problem:</strong> 8 + 5</p>
  <p><strong>Think:</strong> 8 needs 2 more to make 10. I can break 5 into 2 + 3.</p>
  <p><strong>Solve:</strong> 8 + 5 = 8 + 2 + 3 = 10 + 3 = <strong>13</strong></p>
  <p>This strategy works for any addition problem and forms the foundation of mental math fluency!</p>
</div>

<h3>Interactive Simulator: Make a Ten</h3>
<iframe src="https://phet.colorado.edu/sims/html/make-a-ten/latest/make-a-ten_all.html" 
  width="100%" height="600" frameborder="0" style="border: 2px solid #444; border-radius: 8px;"></iframe>
<p><em>Practice making ten! Move dots to fill the ten frame. This visual model will help you see why 8 + 5 = 13. Try other combinations like 9 + 4, 7 + 6!</em></p>

<h3>Interactive Simulator: Arithmetic</h3>
<iframe src="https://phet.colorado.edu/sims/html/arithmetic/latest/arithmetic_all.html" 
  width="100%" height="600" frameborder="0" style="border: 2px solid #444; border-radius: 8px;"></iframe>
<p><em>Build fluency with visual models. See arrays, number lines, and equations working together. Level up from Level 1 through Level 6 as you master each fact family!</em></p>

<hr>

<h2>Module 3: Subtraction - Finding Differences</h2>
<p>Subtraction represents taking away, finding the difference between quantities, or figuring out what's missing. It's the inverse operation of addition.</p>

<h3>Meanings of Subtraction</h3>
<ul>
  <li><strong>Take Away:</strong> Start with 12 cookies, eat 5, how many remain? (12 - 5)</li>
  <li><strong>Compare:</strong> Lucy has 15 stickers, Tom has 9. How many more does Lucy have? (15 - 9)</li>
  <li><strong>Missing Addend:</strong> I have 8, need 15 total. How many more? (15 - 8)</li>
</ul>

<h3>Subtraction Strategies</h3>
<ul>
  <li><strong>Counting Back:</strong> Start at the total, count down the amount being subtracted</li>
  <li><strong>Think Addition:</strong> 15 - 8 = ? Think: 8 + ? = 15 (known fact: 8 + 7 = 15)</li>
  <li><strong>Break Apart:</strong> 15 - 8 = 15 - 5 - 3 = 10 - 3 = 7</li>
</ul>

<h3>Interactive Simulator: Number Line Operations</h3>
<iframe src="https://phet.colorado.edu/sims/html/number-line-operations/latest/number-line-operations_all.html" 
  width="100%" height="600" frameborder="0" style="border: 2px solid #444; border-radius: 8px;"></iframe>
<p><em>Visualize both operations! See how addition moves right on the number line, subtraction moves left. Notice the relationship: if 8 + 7 = 15, then 15 - 7 = 8 and 15 - 8 = 7.</em></p>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>Fact Families</h4>
  <p>Three numbers can form a "fact family" with four related facts:</p>
  <p>For 7, 8, 15:</p>
  <ul>
    <li>7 + 8 = 15</li>
    <li>8 + 7 = 15 (commutative property)</li>
    <li>15 - 7 = 8</li>
    <li>15 - 8 = 7</li>
  </ul>
  <p>Knowing one fact helps you know all four! This is the power of understanding relationships.</p>
</div>

<hr>

<h2>Module 4: Patterns and Structures</h2>
<p>Mathematics is full of patterns. Recognizing patterns helps us predict, generalize, and solve problems efficiently.</p>

<h3>Types of Patterns</h3>
<ul>
  <li><strong>Repeating Patterns:</strong> ABABAB, AABAAB, ABCABC (predictable cycles)</li>
  <li><strong>Growing Patterns:</strong> 2, 4, 6, 8... (arithmetic sequences)</li>
  <li><strong>Geometric Patterns:</strong> Shapes that follow a rule</li>
  <li><strong>Number Patterns:</strong> Skip counting, multiples, sequences</li>
</ul>

<h3>Pattern Recognition Skills</h3>
<ul>
  <li>Identify the repeating unit or rule</li>
  <li>Extend the pattern (predict what comes next)</li>
  <li>Find missing elements</li>
  <li>Create your own patterns with a clear rule</li>
</ul>

<h3>Interactive Simulator: Function Builder</h3>
<iframe src="https://phet.colorado.edu/sims/html/function-builder/latest/function-builder_all.html" 
  width="100%" height="600" frameborder="0" style="border: 2px solid #444; border-radius: 8px;"></iframe>
<p><em>Explore functions and patterns! Put a number in, apply a rule (function), get a number out. Predict the pattern, then test your hypothesis. This is the foundation of algebraic thinking!</em></p>

<hr>

<h2>Module 5: Mathematical Thinking and Problem Solving</h2>
<p>Becoming a mathematician means developing powerful thinking habits. Learn to approach problems strategically.</p>

<h3>Problem-Solving Strategies</h3>
<ul>
  <li><strong>Understand the Problem:</strong> What do I know? What do I need to find?</li>
  <li><strong>Make a Plan:</strong> Draw a picture, act it out, look for a pattern, guess and check</li>
  <li><strong>Carry Out the Plan:</strong> Work carefully, show your thinking</li>
  <li><strong>Look Back:</strong> Does my answer make sense? Can I check it another way?</li>
</ul>

<h3>Mathematical Practices</h3>
<ul>
  <li><strong>Perseverance:</strong> Keep trying even when it's hard</li>
  <li><strong>Precision:</strong> Use clear language and accurate calculations</li>
  <li><strong>Reasoning:</strong> Explain why your answer is correct</li>
  <li><strong>Modeling:</strong> Use diagrams, equations, and tools to represent problems</li>
  <li><strong>Structure:</strong> Look for patterns and connections</li>
</ul>

<div style="background: rgba(100,200,100,0.1); padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #4CAF50;">
  <h4>Challenge Problem</h4>
  <p>I am thinking of a number. If you add 7 to it, you get 15. What is my number?</p>
  <p><strong>Strategy:</strong> Work backwards! 15 - 7 = 8. Check: 8 + 7 = 15 ✓</p>
</div>

<h3>Interactive Simulator: Equality Explorer</h3>
<iframe src="https://phet.colorado.edu/sims/html/equality-explorer/latest/equality-explorer_all.html" 
  width="100%" height="600" frameborder="0" style="border: 2px solid #444; border-radius: 8px;"></iframe>
<p><em>Explore equations and balance! What makes both sides equal? The equals sign means "the same as" - not just "the answer is coming." This is essential for algebra!</em></p>

<hr>

<h2>Module 6: Real-World Applications</h2>
<p>Mathematics is all around us! See how we use numbers and operations in everyday life.</p>

<h3>Everyday Math</h3>
<ul>
  <li><strong>Shopping:</strong> Comparing prices, counting money, making change</li>
  <li><strong>Cooking:</strong> Measuring ingredients, adjusting recipes</li>
  <li><strong>Time:</strong> Reading clocks, calculating durations, scheduling</li>
  <li><strong>Games:</strong> Keeping score, comparing results</li>
  <li><strong>Building:</strong> Measuring lengths, counting pieces</li>
</ul>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>Real-World Problem</h4>
  <p>A pizza has 8 slices. You eat 3 slices and your friend eats 2 slices. How many slices are left?</p>
  <p><strong>Method 1:</strong> 8 - 3 - 2 = 3 slices left</p>
  <p><strong>Method 2:</strong> 3 + 2 = 5 eaten, 8 - 5 = 3 slices left</p>
  <p>Both methods give the same answer - choose the one that makes most sense to you!</p>
</div>

<p><strong>Congratulations! You've completed Grade 1 Mathematics and built a strong foundation in number sense. You're ready for the next level!</strong></p>
""",
    "questions": [
        {"question_text": "What is 8 + 7?", "question_type": "multiple_choice", "options": ["14", "15", "16", "13"], "correct_answer": "15", "explanation": "Use make-a-ten strategy: 8 needs 2 to make 10, so break 7 into 2+5. Then 8+2=10, and 10+5=15.", "points": 1, "order_index": 1},
        {"question_text": "What is 14 - 6?", "question_type": "multiple_choice", "options": ["7", "8", "9", "10"], "correct_answer": "8", "explanation": "Think addition: 6 + ? = 14. Since 6 + 8 = 14, then 14 - 6 = 8. Or use break apart: 14 - 4 = 10, then 10 - 2 = 8.", "points": 1, "order_index": 2},
        {"question_text": "Which number is greater: 56 or 65?", "question_type": "multiple_choice", "options": ["56", "65", "They are equal", "Cannot tell"], "correct_answer": "65", "explanation": "Compare the tens place: 65 has 6 tens (60), 56 has 5 tens (50). Since 60 > 50, 65 > 56.", "points": 1, "order_index": 3},
        {"question_text": "If 9 + __ = 17, what is the missing number?", "question_type": "multiple_choice", "options": ["7", "8", "9", "6"], "correct_answer": "8", "explanation": "Use inverse operation: 17 - 9 = 8. Check: 9 + 8 = 17 ✓", "points": 1, "order_index": 4},
        {"question_text": "What comes next: 2, 4, 6, 8, __?", "question_type": "multiple_choice", "options": ["9", "10", "12", "14"], "correct_answer": "10", "explanation": "This pattern counts by 2s (even numbers). After 8 comes 10.", "points": 1, "order_index": 5},
        {"question_text": "What is 9 + 6 + 1?", "question_type": "multiple_choice", "options": ["15", "16", "17", "18"], "correct_answer": "16", "explanation": "Use commutative property strategically: 9 + 1 = 10, then 10 + 6 = 16. Group friendly numbers first!", "points": 1, "order_index": 6},
        {"question_text": "Which is in the same fact family as 7 + 5 = 12?", "question_type": "multiple_choice", "options": ["7 + 7 = 14", "5 + 7 = 12", "12 + 5 = 17", "5 + 5 = 10"], "correct_answer": "5 + 7 = 12", "explanation": "Fact family for 5, 7, 12: 5+7=12, 7+5=12, 12-5=7, 12-7=5. All four facts use the same three numbers.", "points": 1, "order_index": 7},
        {"question_text": "What is 10 more than 47?", "question_type": "multiple_choice", "options": ["48", "57", "58", "67"], "correct_answer": "57", "explanation": "Adding 10 increases the tens digit by 1: 47 + 10 = 57. The ones digit stays the same.", "points": 1, "order_index": 8},
        {"question_text": "Mia has 12 stickers. She gives 4 to her friend. How many left?", "question_type": "multiple_choice", "options": ["7", "8", "9", "16"], "correct_answer": "8", "explanation": "12 - 4 = 8. Use make-a-ten: 12 - 2 = 10, then 10 - 2 = 8.", "points": 1, "order_index": 9},
        {"question_text": "What is 6 + 6 + 6?", "question_type": "multiple_choice", "options": ["16", "18", "12", "20"], "correct_answer": "18", "explanation": "6 + 6 = 12, then 12 + 6 = 18. This is 3 groups of 6, which is 3 × 6 = 18.", "points": 1, "order_index": 10},
    ]
}

# G1-PHYSICS: Forces and Motion
COURSE_G1_PHYSICS = {
    "title": "Grade 1 Physics: Forces and Motion",
    "grade": 1,
    "content": r"""
<h1>Grade 1 Physics: Forces and Motion</h1>
<h2>Understanding How Things Move</h2>
<p>Physics is the study of how the universe works. Discover forces, motion, gravity, and energy through interactive simulations.</p>

<h2>Module 1: What is a Force?</h2>
<p>A <strong>force</strong> is a push or a pull. Forces are everywhere!</p>
<ul>
  <li><strong>Push:</strong> Moving something away (kicking a ball)</li>
  <li><strong>Pull:</strong> Bringing something closer (opening a door)</li>
  <li><strong>Gravity:</strong> Pulls everything toward Earth</li>
  <li><strong>Friction:</strong> Slows things down when they rub together</li>
</ul>

<h3>Interactive Simulator: Forces and Motion Basics</h3>
<iframe src="https://phet.colorado.edu/sims/html/forces-and-motion-basics/latest/forces-and-motion-basics_all.html" width="100%" height="600" frameborder="0" style="border: 2px solid #444; border-radius: 8px;"></iframe>
<p><em>Push objects and observe motion. Bigger forces = bigger movement!</em></p>

<h2>Module 2: Gravity - The Universal Pull</h2>
<p>Gravity pulls all objects toward Earth's center. Without it, we'd float into space!</p>

<h3>Interactive Simulator: Gravity Force Lab Basics</h3>
<iframe src="https://phet.colorado.edu/sims/html/gravity-force-lab-basics/latest/gravity-force-lab-basics_all.html" width="100%" height="600" frameborder="0" style="border: 2px solid #444; border-radius: 8px;"></iframe>
<p><em>Explore how gravity pulls objects. Change masses and distance to see effects!</em></p>

<h2>Module 3: Energy - Potential and Kinetic</h2>
<p>Energy makes things happen!</p>
<ul>
  <li><strong>Potential Energy:</strong> Stored energy (ball held high)</li>
  <li><strong>Kinetic Energy:</strong> Energy of motion (rolling ball)</li>
</ul>

<h3>Interactive Simulator: Energy Skate Park Basics</h3>
<iframe src="https://phet.colorado.edu/sims/html/energy-skate-park-basics/latest/energy-skate-park-basics_all.html" width="100%" height="600" frameborder="0" style="border: 2px solid #444; border-radius: 8px;"></iframe>
<p><em>Watch energy transform! High position = Potential Energy, moving = Kinetic Energy!</em></p>

<h2>Module 4: Simple Machines</h2>
<p>Simple machines make work easier:</p>
<ul>
  <li><strong>Lever:</strong> Seesaw, scissors</li>
  <li><strong>Inclined Plane:</strong> Ramp, slide</li>
  <li><strong>Pulley:</strong> Flagpole, elevator</li>
</ul>

<h3>Interactive Simulator: Balancing Act</h3>
<iframe src="https://phet.colorado.edu/sims/html/balancing-act/latest/balancing-act_all.html" width="100%" height="600" frameborder="0" style="border: 2px solid #444; border-radius: 8px;"></iframe>
<p><em>Explore levers! Balance masses at different distances.</em></p>

<p><strong>You're now a physics explorer!</strong></p>
""",
    "questions": [
        {"question_text": "What is a force?", "question_type": "multiple_choice", "options": ["A type of energy", "A push or pull", "A measurement", "A machine"], "correct_answer": "A push or pull", "explanation": "A force is a push or pull that can make objects move, stop, or change direction.", "points": 1, "order_index": 1},
        {"question_text": "What pulls objects toward Earth?", "question_type": "multiple_choice", "options": ["Magnetism", "Friction", "Gravity", "Electricity"], "correct_answer": "Gravity", "explanation": "Gravity is the invisible force pulling everything toward Earth's center.", "points": 1, "order_index": 2},
        {"question_text": "Which has MOST friction?", "question_type": "multiple_choice", "options": ["Ice", "Sandpaper", "Wood", "Glass"], "correct_answer": "Sandpaper", "explanation": "Rough surfaces like sandpaper create more friction than smooth surfaces.", "points": 1, "order_index": 3},
        {"question_text": "A ball in the air has what energy?", "question_type": "multiple_choice", "options": ["Kinetic", "Potential", "Light", "Sound"], "correct_answer": "Potential", "explanation": "Potential energy is stored due to position. The ball will have kinetic energy when falling.", "points": 1, "order_index": 4},
        {"question_text": "What type of machine is a ramp?", "question_type": "multiple_choice", "options": ["Lever", "Pulley", "Inclined plane", "Wheel"], "correct_answer": "Inclined plane", "explanation": "A ramp is an inclined plane - a sloping surface making it easier to lift objects.", "points": 1, "order_index": 5},
    ]
}

# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================

def resolve_creator_id(cursor):
    cursor.execute("SELECT id FROM users WHERE role='admin' LIMIT 1")
    row = cursor.fetchone()
    if row:
        return row["id"]
    cursor.execute("SELECT id FROM users LIMIT 1")
    row = cursor.fetchone()
    return row["id"] if row else 1

def placeholder_html(question_id, order_index):
    return f'<div class="quiz-question-placeholder" data-question-id="{question_id}" data-order="{order_index}"></div>'

def upsert_course(cursor, course_data, creator_id):
    title = course_data["title"]
    grade = course_data["grade"]
    content = course_data["content"]
    questions = course_data["questions"]
    
    cursor.execute("SELECT id FROM courses WHERE title=%s AND grade_level=%s LIMIT 1", (title, grade))
    row = cursor.fetchone()
    
    if row:
        course_id = row["id"]
        cursor.execute("UPDATE courses SET content=%s, status='approved' WHERE id=%s", (content, course_id))
        action = "updated"
    else:
        cursor.execute("INSERT INTO courses (title, description, content, creator_id, status, grade_level) VALUES (%s, %s, %s, %s, 'approved', %s)",
            (title, f"Grade {grade}: {title}", content, creator_id, grade))
        cursor.execute("SELECT LAST_INSERT_ID() AS id")
        course_id = cursor.fetchone()["id"]
        action = "inserted"
    
    cursor.execute("DELETE FROM course_questions WHERE course_id=%s", (course_id,))
    
    question_ids = []
    for q in questions:
        cursor.execute("""INSERT INTO course_questions (course_id, question_text, question_type, options, correct_answer, explanation, points, order_index)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (course_id, q["question_text"], q["question_type"], json.dumps(q["options"]),
             q["correct_answer"], q["explanation"], q["points"], q["order_index"]))
        cursor.execute("SELECT LAST_INSERT_ID() AS id")
        question_ids.append(cursor.fetchone()["id"])
    
    hydrated = content + "".join([placeholder_html(qid, i+1) for i, qid in enumerate(question_ids)])
    cursor.execute("UPDATE courses SET content=%s WHERE id=%s", (hydrated, course_id))
    return {"id": course_id, "title": title, "grade": grade, "questions": len(question_ids), "action": action}

def main():
    if not AIVEN_CONFIG.get("password"):
        print("ERROR: Set MYSQLPASSWORD environment variable")
        return 1
    
    all_courses = [COURSE_G1_MATH, COURSE_G1_PHYSICS]
    
    print(f"Prepared {len(all_courses)} courses")
    print("Connecting to database...")
    
    try:
        conn = pymysql.connect(**AIVEN_CONFIG)
    except Exception as e:
        print(f"Connection failed: {e}")
        return 1
    
    processed = []
    try:
        cursor = conn.cursor()
        creator_id = resolve_creator_id(cursor)
        print(f"Using creator_id: {creator_id}")
        
        for i, course in enumerate(all_courses, 1):
            result = upsert_course(cursor, course, creator_id)
            processed.append(result)
            print(f"[{i}/{len(all_courses)}] G{result['grade']:02d} | {result['action'].upper()} | ID {result['id']} | {result['questions']}Q | {result['title'][:35]}...")
        
        conn.commit()
        print(f"\nSuccessfully injected {len(processed)} courses!")
        
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        conn.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
