#!/usr/bin/env python3
"""Inject 4 new courses with PhET sims and quiz questions into Veelearn database."""

import pymysql, json, sys, os, io, random

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
    "db": os.getenv("MYSQL_DATABASE") or os.getenv("AIVEN_DB", "defaultdb"),
    "host": os.getenv("MYSQLHOST") or os.getenv("AIVEN_HOST", "veelearndb-asterloop-483e.i.aivencloud.com"),
    "password": os.getenv("MYSQLPASSWORD") or os.getenv("AIVEN_PASSWORD", ""),
    "port": int(os.getenv("MYSQLPORT") or os.getenv("AIVEN_PORT", "26399")),
    "user": os.getenv("MYSQLUSER") or os.getenv("AIVEN_USER", "avnadmin"),
    "read_timeout": 10,
    "write_timeout": 10,
}

# SSL Configuration for Aiven
ssl_ca = os.getenv("DB_SSL_CA")
if ssl_ca:
    if "\\n" in ssl_ca:
        ssl_ca = ssl_ca.replace("\\n", "\n")
    ca_path = os.path.join(os.getcwd(), "ca.pem")
    with open(ca_path, "w") as f:
        f.write(ssl_ca)
    AIVEN_CONFIG["ssl"] = {"ca": ca_path}

# =====================================================================
# COURSE 1: Physics - Forces, Motion & Energy
# =====================================================================
PHYSICS_CONTENT = r"""
<h1>Physics: Forces, Motion & Energy</h1>

<h2>Course Overview</h2>
<p>Explore the fundamental laws that govern how objects move. From Newton's revolutionary insights to the conservation of energy, this course brings physics to life with interactive simulations and real-world examples.</p>

<hr>

<h2>Module 1: Newton's First Law - Inertia</h2>
<p><strong>An object at rest stays at rest, and an object in motion stays in motion at constant velocity, unless acted upon by a net external force.</strong></p>
<p>This is the law of <strong>inertia</strong>. Inertia is the tendency of an object to resist changes in its state of motion. The more massive an object, the greater its inertia.</p>
<ul>
  <li>A hockey puck slides across ice for a long time because friction is very small</li>
  <li>Passengers lurch forward when a car brakes suddenly — their body wants to keep moving</li>
  <li>A tablecloth can be pulled from under dishes if done quickly enough</li>
</ul>

<h3>1.1 Mass vs. Weight</h3>
<p><strong>Mass</strong> (kg) is the amount of matter — it doesn't change with location. <strong>Weight</strong> (N) is the gravitational force on an object: $W = mg$, where $g \approx 9.8 \text{ m/s}^2$ on Earth.</p>

<hr>

<h2>Module 2: Newton's Second Law - F = ma</h2>
<p>The acceleration of an object is directly proportional to the net force and inversely proportional to its mass:</p>
<p>$$\vec{F}_{net} = m\vec{a}$$</p>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>Worked Example: Pushing a Box</h4>
  <p><strong>Problem:</strong> A 10 kg box is pushed with a force of 50 N across a frictionless surface. What is the acceleration?</p>
  <p><strong>Solution:</strong> $a = F/m = 50/10 = 5 \text{ m/s}^2$</p>
</div>

<p><strong>Interactive Simulator: Forces and Motion</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/forces-and-motion-basics/latest/forces-and-motion-basics_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Apply forces to objects and observe how mass and force affect acceleration. Try the friction tab!</em></p>

<hr>

<h2>Module 3: Newton's Third Law - Action & Reaction</h2>
<p><strong>For every action, there is an equal and opposite reaction.</strong></p>
<p>When you push on a wall, the wall pushes back on you with equal force. When a rocket expels gas downward, the gas pushes the rocket upward.</p>
<ul>
  <li>Walking: Your foot pushes backward on the ground; the ground pushes you forward</li>
  <li>Swimming: Your hands push water backward; the water pushes you forward</li>
  <li>Rockets: Exhaust goes down; rocket goes up</li>
</ul>

<hr>

<h2>Module 4: Gravity - The Universal Force</h2>
<p>Newton's Law of Universal Gravitation states that every mass attracts every other mass:</p>
<p>$$F = G \frac{m_1 m_2}{r^2}$$</p>
<p>Where $G = 6.674 \times 10^{-11} \text{ N m}^2/\text{kg}^2$</p>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>Worked Example: Gravitational Force</h4>
  <p><strong>Problem:</strong> Find the gravitational force between two 1000 kg cars separated by 5 meters.</p>
  <p><strong>Solution:</strong> $F = (6.674 \times 10^{-11})(1000)(1000)/(5^2) = 2.67 \times 10^{-6}$ N. Incredibly small — gravity is only noticeable for massive objects like planets!</p>
</div>

<p><strong>Interactive Simulator: Gravity Force Lab</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/gravity-force-lab/latest/gravity-force-lab_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Change the masses and distance to see how gravitational force changes. Notice the inverse-square relationship!</em></p>

<hr>

<h2>Module 5: Energy - Kinetic & Potential</h2>
<p>Energy is the ability to do work. It comes in two main mechanical forms:</p>
<ul>
  <li><strong>Kinetic Energy:</strong> $KE = \frac{1}{2}mv^2$ — energy of motion</li>
  <li><strong>Potential Energy:</strong> $PE = mgh$ — energy of position (height)</li>
</ul>
<p>The <strong>Law of Conservation of Energy</strong> states: energy cannot be created or destroyed, only transformed. At any point: $KE + PE = \text{constant}$ (ignoring friction).</p>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>Worked Example: Roller Coaster Energy</h4>
  <p><strong>Problem:</strong> A 500 kg cart starts from rest at height 20 m. What is its speed at the bottom?</p>
  <p><strong>Solution:</strong> $mgh = \frac{1}{2}mv^2 \Rightarrow v = \sqrt{2gh} = \sqrt{2(9.8)(20)} = \sqrt{392} \approx 19.8$ m/s</p>
</div>

<p><strong>Interactive Simulator: Energy Skate Park</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/energy-skate-park-basics/latest/energy-skate-park-basics_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Watch the skater convert between kinetic and potential energy. Turn on the energy bar graph to visualize the transformation!</em></p>

<hr>

<h2>Module 6: Projectile Motion</h2>
<p>A projectile is any object launched into the air with only gravity acting on it. The key insight: <strong>horizontal and vertical motions are independent.</strong></p>
<ul>
  <li>Horizontal: constant velocity ($v_x = v_0 \cos\theta$)</li>
  <li>Vertical: accelerated by gravity ($v_y = v_0 \sin\theta - gt$)</li>
</ul>
<p>Range: $R = \frac{v_0^2 \sin(2\theta)}{g}$ — Maximum range occurs at $\theta = 45°$.</p>

<p><strong>Interactive Simulator: Projectile Motion</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/projectile-motion/latest/projectile-motion_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Launch projectiles at different angles and speeds. Find the angle that gives maximum range!</em></p>

<p><strong>Congratulations! You've completed Physics: Forces, Motion & Energy. Take the quiz to test your knowledge!</strong></p>
"""

PHYSICS_DESC = "Master Newton's Laws, gravity, energy conservation, and projectile motion with interactive PhET simulations."

PHYSICS_QUESTIONS = [
    {"question_text": "According to Newton's First Law, what happens to a moving object if no net force acts on it?", "question_type": "multiple_choice", "options": ["It accelerates", "It stops immediately", "It continues at constant velocity", "It changes direction"], "correct_answer": "It continues at constant velocity", "explanation": "Newton's First Law (Law of Inertia) states that an object in motion stays in motion at constant velocity unless acted upon by a net external force.", "points": 1, "order_index": 1},
    {"question_text": "A 5 kg object is pushed with a net force of 20 N. What is its acceleration?", "question_type": "multiple_choice", "options": ["2 m/s²", "4 m/s²", "10 m/s²", "100 m/s²"], "correct_answer": "4 m/s²", "explanation": "Using F = ma: a = F/m = 20/5 = 4 m/s².", "points": 1, "order_index": 2},
    {"question_text": "Which of the following is an example of Newton's Third Law?", "question_type": "multiple_choice", "options": ["A ball rolling downhill", "A book sitting on a table", "A rocket expelling gas to move forward", "A car slowing down due to friction"], "correct_answer": "A rocket expelling gas to move forward", "explanation": "The rocket pushes gas backward (action), and the gas pushes the rocket forward (reaction) — a classic Newton's Third Law pair.", "points": 1, "order_index": 3},
    {"question_text": "If you double the distance between two masses, the gravitational force becomes:", "question_type": "multiple_choice", "options": ["Half as strong", "Twice as strong", "One-quarter as strong", "Four times as strong"], "correct_answer": "One-quarter as strong", "explanation": "Gravity follows an inverse-square law: F ∝ 1/r². Doubling r means F becomes 1/(2²) = 1/4 of the original.", "points": 1, "order_index": 4},
    {"question_text": "A 2 kg ball moves at 3 m/s. What is its kinetic energy?", "question_type": "multiple_choice", "options": ["3 J", "6 J", "9 J", "18 J"], "correct_answer": "9 J", "explanation": "KE = ½mv² = ½(2)(3²) = ½(2)(9) = 9 J.", "points": 1, "order_index": 5},
    {"question_text": "At what angle does a projectile achieve maximum range (ignoring air resistance)?", "question_type": "multiple_choice", "options": ["30°", "45°", "60°", "90°"], "correct_answer": "45°", "explanation": "Range R = v₀²sin(2θ)/g is maximized when sin(2θ) = 1, which means 2θ = 90°, so θ = 45°.", "points": 1, "order_index": 6},
    {"question_text": "A ball is thrown straight up. At the highest point, what is its velocity?", "question_type": "multiple_choice", "options": ["Maximum", "9.8 m/s", "Zero", "Equal to initial velocity"], "correct_answer": "Zero", "explanation": "At the highest point, the ball momentarily stops before falling back down. Its velocity is zero, but acceleration due to gravity is still 9.8 m/s² downward.", "points": 1, "order_index": 7},
    {"question_text": "The unit of force in the SI system is:", "question_type": "multiple_choice", "options": ["Joule", "Watt", "Newton", "Pascal"], "correct_answer": "Newton", "explanation": "The Newton (N) is the SI unit of force. 1 N = 1 kg·m/s².", "points": 1, "order_index": 8},
    {"question_text": "A 10 kg object is lifted 5 meters. What is its gravitational potential energy? (g = 10 m/s²)", "question_type": "multiple_choice", "options": ["50 J", "100 J", "250 J", "500 J"], "correct_answer": "500 J", "explanation": "PE = mgh = (10)(10)(5) = 500 J.", "points": 1, "order_index": 9},
    {"question_text": "What does the slope of a velocity-time graph represent?", "question_type": "multiple_choice", "options": ["Distance", "Speed", "Acceleration", "Force"], "correct_answer": "Acceleration", "explanation": "The slope of a v-t graph is Δv/Δt, which is the definition of acceleration.", "points": 1, "order_index": 10},
]

# =====================================================================
# COURSE 2: Electricity & Circuits
# =====================================================================
ELECTRICITY_CONTENT = r"""
<h1>Electricity & Circuits</h1>

<h2>Course Overview</h2>
<p>Understand the invisible force that powers our modern world. From the flow of electrons through wires to designing complex circuits, this course covers everything from basic charge to practical circuit analysis.</p>

<hr>

<h2>Module 1: Electric Charge & Current</h2>
<p>All matter contains electric charges. <strong>Protons</strong> are positive, <strong>electrons</strong> are negative. Like charges repel, opposite charges attract.</p>
<p><strong>Electric current</strong> is the flow of electric charge through a conductor:</p>
<p>$$I = \frac{Q}{t}$$</p>
<p>Where $I$ = current (Amperes), $Q$ = charge (Coulombs), $t$ = time (seconds).</p>
<ul>
  <li>1 Ampere = 1 Coulomb per second</li>
  <li>Conventional current flows from + to − (opposite to electron flow)</li>
  <li>In metals, it's the electrons that actually move</li>
</ul>

<p><strong>Interactive Simulator: Charges and Fields</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/charges-and-fields/latest/charges-and-fields_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Place positive and negative charges and observe the electric field lines and equipotential surfaces.</em></p>

<hr>

<h2>Module 2: Voltage (Potential Difference)</h2>
<p><strong>Voltage</strong> is the "push" that drives current through a circuit. It's the energy per unit charge:</p>
<p>$$V = \frac{W}{Q}$$</p>
<p>Think of voltage as the height difference in a waterfall — the greater the height (voltage), the more energy the water (charge) has.</p>
<ul>
  <li>A 9V battery gives 9 Joules of energy to each Coulomb of charge</li>
  <li>Voltage is measured with a <strong>voltmeter</strong> connected in parallel</li>
  <li>Voltage sources: batteries, generators, solar cells</li>
</ul>

<hr>

<h2>Module 3: Resistance & Ohm's Law</h2>
<p><strong>Resistance</strong> ($R$) opposes the flow of current. Measured in Ohms ($\Omega$).</p>
<p><strong>Ohm's Law</strong> — the most important equation in circuit analysis:</p>
<p>$$V = IR$$</p>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>Worked Example: Finding Current</h4>
  <p><strong>Problem:</strong> A 12V battery is connected to a 4Ω resistor. What current flows?</p>
  <p><strong>Solution:</strong> $I = V/R = 12/4 = 3$ Amperes</p>
</div>

<p><strong>Interactive Simulator: Ohm's Law</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/ohms-law/latest/ohms-law_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Adjust voltage and resistance to see how current changes. Notice the linear relationship!</em></p>

<h3>3.1 What Affects Resistance?</h3>
<p>Resistance depends on: material, length, cross-sectional area, and temperature.</p>
<p>$$R = \rho \frac{L}{A}$$</p>

<p><strong>Interactive Simulator: Resistance in a Wire</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/resistance-in-a-wire/latest/resistance-in-a-wire_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>

<hr>

<h2>Module 4: Series & Parallel Circuits</h2>
<h3>Series Circuits</h3>
<ul>
  <li>Components connected end-to-end (one path for current)</li>
  <li>Same current through all: $I_{total} = I_1 = I_2 = I_3$</li>
  <li>Voltages add up: $V_{total} = V_1 + V_2 + V_3$</li>
  <li>Resistances add up: $R_{total} = R_1 + R_2 + R_3$</li>
</ul>

<h3>Parallel Circuits</h3>
<ul>
  <li>Components connected side-by-side (multiple paths)</li>
  <li>Same voltage across all: $V_{total} = V_1 = V_2 = V_3$</li>
  <li>Currents add up: $I_{total} = I_1 + I_2 + I_3$</li>
  <li>$\frac{1}{R_{total}} = \frac{1}{R_1} + \frac{1}{R_2} + \frac{1}{R_3}$</li>
</ul>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>Worked Example: Parallel Resistance</h4>
  <p><strong>Problem:</strong> Two resistors of 6Ω and 3Ω are connected in parallel. What is the total resistance?</p>
  <p><strong>Solution:</strong> $\frac{1}{R_T} = \frac{1}{6} + \frac{1}{3} = \frac{1}{6} + \frac{2}{6} = \frac{3}{6} = \frac{1}{2}$, so $R_T = 2\Omega$</p>
</div>

<p><strong>Interactive Simulator: Circuit Construction Kit</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/circuit-construction-kit-dc/latest/circuit-construction-kit-dc_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Build your own circuits! Try series vs parallel and measure voltage and current with the virtual meters.</em></p>

<hr>

<h2>Module 5: Electrical Power & Energy</h2>
<p>Electrical power is the rate at which electrical energy is converted:</p>
<p>$$P = IV = I^2R = \frac{V^2}{R}$$</p>
<p>Energy consumed: $E = Pt$ (in Joules, or kilowatt-hours for your electricity bill).</p>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>Worked Example: Power Bill</h4>
  <p><strong>Problem:</strong> A 100W light bulb runs for 10 hours. How many kWh is that?</p>
  <p><strong>Solution:</strong> $E = 100W \times 10h = 1000 Wh = 1 kWh$. At $0.12/kWh, that costs 12 cents.</p>
</div>

<p><strong>Congratulations! You've completed Electricity & Circuits. Take the quiz below!</strong></p>
"""

ELECTRICITY_DESC = "Master electric charge, Ohm's Law, series and parallel circuits, and electrical power with hands-on PhET simulations."

ELECTRICITY_QUESTIONS = [
    {"question_text": "What is the SI unit of electric current?", "question_type": "multiple_choice", "options": ["Volt", "Ohm", "Ampere", "Watt"], "correct_answer": "Ampere", "explanation": "The Ampere (A) is the SI unit of current. 1 A = 1 Coulomb/second.", "points": 1, "order_index": 1},
    {"question_text": "According to Ohm's Law, if voltage doubles and resistance stays the same, the current:", "question_type": "multiple_choice", "options": ["Halves", "Doubles", "Stays the same", "Quadruples"], "correct_answer": "Doubles", "explanation": "V = IR. If V doubles and R is constant, I must also double.", "points": 1, "order_index": 2},
    {"question_text": "Three 6Ω resistors are connected in series. What is the total resistance?", "question_type": "multiple_choice", "options": ["2 Ω", "6 Ω", "12 Ω", "18 Ω"], "correct_answer": "18 Ω", "explanation": "In series: R_total = R1 + R2 + R3 = 6 + 6 + 6 = 18 Ω.", "points": 1, "order_index": 3},
    {"question_text": "Two 10Ω resistors are connected in parallel. The total resistance is:", "question_type": "multiple_choice", "options": ["20 Ω", "10 Ω", "5 Ω", "2.5 Ω"], "correct_answer": "5 Ω", "explanation": "1/R = 1/10 + 1/10 = 2/10 = 1/5, so R = 5 Ω. Parallel resistance is always less than the smallest individual resistor.", "points": 1, "order_index": 4},
    {"question_text": "In a series circuit, what stays the same through all components?", "question_type": "multiple_choice", "options": ["Voltage", "Current", "Resistance", "Power"], "correct_answer": "Current", "explanation": "In a series circuit there is only one path for current, so the same current flows through every component.", "points": 1, "order_index": 5},
    {"question_text": "A 60W light bulb operates at 120V. What current does it draw?", "question_type": "multiple_choice", "options": ["0.5 A", "2 A", "60 A", "7200 A"], "correct_answer": "0.5 A", "explanation": "P = IV, so I = P/V = 60/120 = 0.5 A.", "points": 1, "order_index": 6},
    {"question_text": "Which of these increases the resistance of a wire?", "question_type": "multiple_choice", "options": ["Shorter length", "Larger cross-section", "Longer length", "Lower temperature"], "correct_answer": "Longer length", "explanation": "R = ρL/A. Longer wire (larger L) means more resistance. Thicker wire (larger A) means less resistance.", "points": 1, "order_index": 7},
    {"question_text": "A voltmeter should be connected in _____ with the component being measured.", "question_type": "multiple_choice", "options": ["Series", "Parallel", "Neither", "Both"], "correct_answer": "Parallel", "explanation": "Voltmeters measure potential difference across a component and must be connected in parallel. Ammeters go in series.", "points": 1, "order_index": 8},
    {"question_text": "What happens to the brightness of bulbs in a series circuit when you add more bulbs?", "question_type": "multiple_choice", "options": ["Gets brighter", "Gets dimmer", "Stays the same", "Some get brighter, others dimmer"], "correct_answer": "Gets dimmer", "explanation": "Adding bulbs in series increases total resistance, reducing current. Less current means less power to each bulb, so they dim.", "points": 1, "order_index": 9},
    {"question_text": "The power dissipated by a 4Ω resistor carrying 3A of current is:", "question_type": "multiple_choice", "options": ["12 W", "36 W", "7 W", "144 W"], "correct_answer": "36 W", "explanation": "P = I²R = (3)²(4) = 9 × 4 = 36 W.", "points": 1, "order_index": 10},
]

# =====================================================================
# COURSE 3: Waves, Sound & Light
# =====================================================================
WAVES_CONTENT = r"""
<h1>Waves, Sound & Light</h1>

<h2>Course Overview</h2>
<p>Waves are everywhere — from the sound of music to the light from stars. This course explores the physics of oscillations, sound waves, the electromagnetic spectrum, and the behavior of light.</p>

<hr>

<h2>Module 1: Wave Fundamentals</h2>
<p>A <strong>wave</strong> is a disturbance that transfers energy without transferring matter.</p>
<h3>Key Properties</h3>
<ul>
  <li><strong>Amplitude (A):</strong> Maximum displacement from equilibrium — determines loudness/brightness</li>
  <li><strong>Wavelength (λ):</strong> Distance between consecutive identical points (crest to crest)</li>
  <li><strong>Frequency (f):</strong> Number of complete cycles per second (measured in Hz)</li>
  <li><strong>Period (T):</strong> Time for one complete cycle: $T = 1/f$</li>
</ul>
<p>The <strong>wave equation</strong> relates speed, frequency, and wavelength:</p>
<p>$$v = f\lambda$$</p>

<h3>Transverse vs. Longitudinal</h3>
<ul>
  <li><strong>Transverse:</strong> Oscillation perpendicular to wave direction (light, water waves)</li>
  <li><strong>Longitudinal:</strong> Oscillation parallel to wave direction (sound waves)</li>
</ul>

<p><strong>Interactive Simulator: Wave on a String</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/wave-on-a-string/latest/wave-on-a-string_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Change amplitude, frequency, and damping. Switch between manual, oscillate, and pulse modes!</em></p>

<hr>

<h2>Module 2: Sound Waves</h2>
<p>Sound is a <strong>longitudinal wave</strong> that travels through compressions and rarefactions in a medium (air, water, solids).</p>
<ul>
  <li>Speed of sound in air: ~343 m/s (at 20°C)</li>
  <li>Speed increases in denser media: water (~1480 m/s), steel (~5960 m/s)</li>
  <li>Sound cannot travel through a vacuum</li>
</ul>

<h3>2.1 Pitch and Loudness</h3>
<ul>
  <li><strong>Pitch</strong> = frequency. Higher frequency → higher pitch</li>
  <li><strong>Loudness</strong> = amplitude. Larger amplitude → louder sound</li>
  <li>Human hearing range: 20 Hz to 20,000 Hz</li>
</ul>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>Worked Example: Sound Wavelength</h4>
  <p><strong>Problem:</strong> Middle C has a frequency of 262 Hz. What is its wavelength in air?</p>
  <p><strong>Solution:</strong> $\lambda = v/f = 343/262 \approx 1.31$ meters</p>
</div>

<hr>

<h2>Module 3: Wave Interference & Superposition</h2>
<p>When two waves meet, they <strong>superpose</strong> — their displacements add together:</p>
<ul>
  <li><strong>Constructive interference:</strong> Waves in phase → bigger amplitude (crests align)</li>
  <li><strong>Destructive interference:</strong> Waves out of phase → smaller amplitude (crest meets trough)</li>
</ul>
<p><strong>Standing waves</strong> form when two identical waves travel in opposite directions, creating nodes (no motion) and antinodes (maximum motion).</p>

<p><strong>Interactive Simulator: Wave Interference</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/wave-interference/latest/wave-interference_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Explore single and double slit interference. Switch between water, sound, and light waves!</em></p>

<hr>

<h2>Module 4: Light & The Electromagnetic Spectrum</h2>
<p>Light is an <strong>electromagnetic wave</strong> — it doesn't need a medium. All EM waves travel at the speed of light: $c = 3 \times 10^8$ m/s.</p>
<p>The EM spectrum (from longest to shortest wavelength):</p>
<ol>
  <li>Radio waves (meters)</li>
  <li>Microwaves (centimeters)</li>
  <li>Infrared (micrometers)</li>
  <li><strong>Visible light</strong> (400-700 nm): Red → Orange → Yellow → Green → Blue → Violet</li>
  <li>Ultraviolet</li>
  <li>X-rays</li>
  <li>Gamma rays (picometers)</li>
</ol>

<p><strong>Interactive Simulator: Color Vision</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/color-vision/latest/color-vision_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Mix red, green, and blue light to see how colors combine. Try the single-bulb and RGB modes!</em></p>

<hr>

<h2>Module 5: Reflection & Refraction</h2>
<h3>Reflection</h3>
<p>When light hits a surface, it bounces off. The <strong>Law of Reflection</strong>: angle of incidence = angle of reflection ($\theta_i = \theta_r$).</p>

<h3>Refraction</h3>
<p>When light passes from one medium to another, it bends. Described by <strong>Snell's Law</strong>:</p>
<p>$$n_1 \sin\theta_1 = n_2 \sin\theta_2$$</p>
<p>Where $n$ is the refractive index (glass ≈ 1.5, water ≈ 1.33, air ≈ 1.0).</p>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>Worked Example: Snell's Law</h4>
  <p><strong>Problem:</strong> Light goes from air (n=1) into glass (n=1.5) at 30°. What is the refraction angle?</p>
  <p><strong>Solution:</strong> $\sin\theta_2 = (n_1/n_2)\sin\theta_1 = (1/1.5)\sin 30° = (0.667)(0.5) = 0.333$. So $\theta_2 = \sin^{-1}(0.333) \approx 19.5°$</p>
</div>

<p><strong>Interactive Simulator: Bending Light</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/bending-light/latest/bending-light_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Shine light between different materials and observe how it bends. Find the critical angle for total internal reflection!</em></p>

<p><strong>Congratulations! You've completed Waves, Sound & Light. Take the quiz below!</strong></p>
"""

WAVES_DESC = "Explore wave properties, sound, the electromagnetic spectrum, reflection, and refraction with interactive simulations."

WAVES_QUESTIONS = [
    {"question_text": "What is the relationship between wave speed, frequency, and wavelength?", "question_type": "multiple_choice", "options": ["v = f/λ", "v = fλ", "v = λ/f", "f = vλ"], "correct_answer": "v = fλ", "explanation": "The wave equation: speed equals frequency times wavelength.", "points": 1, "order_index": 1},
    {"question_text": "Sound waves are:", "question_type": "multiple_choice", "options": ["Transverse waves", "Longitudinal waves", "Electromagnetic waves", "Standing waves"], "correct_answer": "Longitudinal waves", "explanation": "Sound travels as compressions and rarefactions — the oscillation is parallel to the wave direction (longitudinal).", "points": 1, "order_index": 2},
    {"question_text": "What determines the pitch of a sound?", "question_type": "multiple_choice", "options": ["Amplitude", "Speed", "Frequency", "Wavelength"], "correct_answer": "Frequency", "explanation": "Higher frequency = higher pitch. A violin string vibrating faster produces a higher note.", "points": 1, "order_index": 3},
    {"question_text": "When two wave crests meet at the same point, this is called:", "question_type": "multiple_choice", "options": ["Destructive interference", "Constructive interference", "Diffraction", "Refraction"], "correct_answer": "Constructive interference", "explanation": "When crests align (in phase), amplitudes add up — this is constructive interference, producing a larger wave.", "points": 1, "order_index": 4},
    {"question_text": "Which color of visible light has the longest wavelength?", "question_type": "multiple_choice", "options": ["Violet", "Blue", "Green", "Red"], "correct_answer": "Red", "explanation": "Red light has wavelengths around 620-750 nm, the longest in the visible spectrum. Violet is shortest (~380-450 nm).", "points": 1, "order_index": 5},
    {"question_text": "The speed of light in a vacuum is approximately:", "question_type": "multiple_choice", "options": ["343 m/s", "1500 m/s", "3 × 10⁶ m/s", "3 × 10⁸ m/s"], "correct_answer": "3 × 10⁸ m/s", "explanation": "c = 3 × 10⁸ m/s (300 million meters per second). 343 m/s is the speed of sound in air.", "points": 1, "order_index": 6},
    {"question_text": "According to the law of reflection:", "question_type": "multiple_choice", "options": ["Angle of incidence > angle of reflection", "Angle of incidence = angle of reflection", "Angle of incidence < angle of reflection", "There is no specific relationship"], "correct_answer": "Angle of incidence = angle of reflection", "explanation": "The law of reflection states θᵢ = θᵣ, measured from the normal to the surface.", "points": 1, "order_index": 7},
    {"question_text": "When light passes from air into water, it:", "question_type": "multiple_choice", "options": ["Speeds up and bends away from normal", "Slows down and bends toward normal", "Speeds up and bends toward normal", "Doesn't change direction"], "correct_answer": "Slows down and bends toward normal", "explanation": "Water has a higher refractive index than air. Light slows down and bends toward the normal when entering a denser medium.", "points": 1, "order_index": 8},
    {"question_text": "Which type of electromagnetic radiation has the highest frequency?", "question_type": "multiple_choice", "options": ["Radio waves", "Microwaves", "Visible light", "Gamma rays"], "correct_answer": "Gamma rays", "explanation": "Gamma rays have the shortest wavelength and highest frequency in the EM spectrum, carrying the most energy per photon.", "points": 1, "order_index": 9},
    {"question_text": "A wave has a frequency of 500 Hz and a wavelength of 0.68 m. What is its speed?", "question_type": "multiple_choice", "options": ["735 m/s", "340 m/s", "500 m/s", "170 m/s"], "correct_answer": "340 m/s", "explanation": "v = fλ = 500 × 0.68 = 340 m/s. This is approximately the speed of sound in air!", "points": 1, "order_index": 10},
]

# =====================================================================
# COURSE 4: Biology - Natural Selection & Genetics
# =====================================================================
BIOLOGY_CONTENT = r"""
<h1>Biology: Natural Selection & Genetics</h1>

<h2>Course Overview</h2>
<p>How did the incredible diversity of life on Earth arise? This course explores DNA, genes, heredity, and Charles Darwin's revolutionary theory of natural selection. Understand how organisms evolve and adapt through interactive simulations.</p>

<hr>

<h2>Module 1: DNA - The Blueprint of Life</h2>
<p><strong>DNA (Deoxyribonucleic Acid)</strong> is a double-helix molecule that stores all the genetic instructions for building and maintaining an organism.</p>
<h3>Structure</h3>
<ul>
  <li><strong>Sugar-Phosphate backbone:</strong> The "rails" of the DNA ladder</li>
  <li><strong>Nitrogenous bases:</strong> The "rungs" — Adenine (A), Thymine (T), Guanine (G), Cytosine (C)</li>
  <li><strong>Base pairing rules:</strong> A pairs with T, G pairs with C (complementary base pairing)</li>
  <li>The sequence of bases encodes genetic information</li>
</ul>

<h3>1.1 From DNA to Protein</h3>
<ol>
  <li><strong>Transcription:</strong> DNA → mRNA (in the nucleus)</li>
  <li><strong>Translation:</strong> mRNA → Protein (at ribosomes)</li>
  <li>Every 3 bases (codon) codes for one amino acid</li>
</ol>

<p><strong>Interactive Simulator: Gene Expression Essentials</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/gene-expression-essentials/latest/gene-expression-essentials_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Watch transcription and translation in action! See how RNA polymerase reads DNA and ribosomes build proteins.</em></p>

<hr>

<h2>Module 2: Genes, Alleles & Traits</h2>
<p>A <strong>gene</strong> is a segment of DNA that codes for a specific protein (and thus a trait). <strong>Alleles</strong> are different versions of a gene.</p>
<ul>
  <li><strong>Homozygous:</strong> Two identical alleles (BB or bb)</li>
  <li><strong>Heterozygous:</strong> Two different alleles (Bb)</li>
  <li><strong>Dominant:</strong> Expressed when one or two copies present (B)</li>
  <li><strong>Recessive:</strong> Only expressed when two copies present (bb)</li>
</ul>

<h3>2.1 Genotype vs. Phenotype</h3>
<ul>
  <li><strong>Genotype:</strong> The genetic makeup (e.g., Bb)</li>
  <li><strong>Phenotype:</strong> The observable trait (e.g., brown eyes)</li>
</ul>

<hr>

<h2>Module 3: Punnett Squares - Predicting Offspring</h2>
<p>A <strong>Punnett Square</strong> is a tool to predict the probability of offspring genotypes from a cross.</p>

<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #444;">
  <h4>Worked Example: Monohybrid Cross</h4>
  <p><strong>Problem:</strong> Cross two heterozygous brown-eyed parents (Bb × Bb). What fraction of offspring will have blue eyes?</p>
  <p><strong>Solution:</strong></p>
  <table style="border-collapse: collapse; margin: 10px 0; color: #fff;">
    <tr><td style="border: 1px solid #666; padding: 8px;"></td><td style="border: 1px solid #666; padding: 8px;"><strong>B</strong></td><td style="border: 1px solid #666; padding: 8px;"><strong>b</strong></td></tr>
    <tr><td style="border: 1px solid #666; padding: 8px;"><strong>B</strong></td><td style="border: 1px solid #666; padding: 8px;">BB</td><td style="border: 1px solid #666; padding: 8px;">Bb</td></tr>
    <tr><td style="border: 1px solid #666; padding: 8px;"><strong>b</strong></td><td style="border: 1px solid #666; padding: 8px;">Bb</td><td style="border: 1px solid #666; padding: 8px;">bb</td></tr>
  </table>
  <p>Ratio: 1 BB : 2 Bb : 1 bb → 25% blue eyes (bb), 75% brown eyes (BB or Bb)</p>
</div>

<hr>

<h2>Module 4: Natural Selection</h2>
<p>Charles Darwin's theory of <strong>Natural Selection</strong> explains how populations evolve over time:</p>
<ol>
  <li><strong>Variation:</strong> Individuals in a population have different traits</li>
  <li><strong>Inheritance:</strong> Traits are passed from parents to offspring</li>
  <li><strong>Selection:</strong> Some traits give survival/reproduction advantages</li>
  <li><strong>Time:</strong> Over many generations, advantageous traits become more common</li>
</ol>
<p><strong>"Survival of the fittest"</strong> doesn't mean strongest — it means best adapted to the environment.</p>

<h3>4.1 Types of Selection</h3>
<ul>
  <li><strong>Directional:</strong> One extreme phenotype is favored (e.g., longer beaks in drought)</li>
  <li><strong>Stabilizing:</strong> Average phenotype is favored (e.g., average birth weight)</li>
  <li><strong>Disruptive:</strong> Both extremes are favored over the middle</li>
</ul>

<p><strong>Interactive Simulator: Natural Selection</strong></p>
<iframe src="https://phet.colorado.edu/sims/html/natural-selection/latest/natural-selection_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Watch rabbits evolve! Add selective pressures (wolves, food shortage) and introduce mutations. See how allele frequencies change over generations.</em></p>

<hr>

<h2>Module 5: Evidence for Evolution</h2>
<p>Multiple independent lines of evidence support evolution:</p>
<ul>
  <li><strong>Fossil Record:</strong> Shows gradual changes in organisms over millions of years</li>
  <li><strong>Comparative Anatomy:</strong> Homologous structures (same bones, different functions) in related species</li>
  <li><strong>DNA Comparison:</strong> More similar DNA = more closely related species</li>
  <li><strong>Biogeography:</strong> Similar environments on different continents produce similar adaptations</li>
  <li><strong>Embryology:</strong> Similar embryonic development stages across vertebrates</li>
</ul>

<h3>5.1 Speciation</h3>
<p>When populations are separated (geographic isolation) and evolve independently, they may eventually become different species that can no longer interbreed.</p>

<p><strong>Congratulations! You've completed Biology: Natural Selection & Genetics. Take the quiz below!</strong></p>
"""

BIOLOGY_DESC = "Discover DNA, genes, Punnett squares, and natural selection. Watch evolution happen in real-time with interactive simulations."

BIOLOGY_QUESTIONS = [
    {"question_text": "What are the four nitrogenous bases found in DNA?", "question_type": "multiple_choice", "options": ["A, T, G, C", "A, U, G, C", "A, T, G, U", "T, U, G, C"], "correct_answer": "A, T, G, C", "explanation": "DNA contains Adenine, Thymine, Guanine, and Cytosine. RNA has Uracil (U) instead of Thymine (T).", "points": 1, "order_index": 1},
    {"question_text": "In DNA, Adenine always pairs with:", "question_type": "multiple_choice", "options": ["Guanine", "Cytosine", "Thymine", "Uracil"], "correct_answer": "Thymine", "explanation": "Base pairing rules: A-T and G-C. Adenine forms 2 hydrogen bonds with Thymine.", "points": 1, "order_index": 2},
    {"question_text": "An organism with genotype Bb is:", "question_type": "multiple_choice", "options": ["Homozygous dominant", "Homozygous recessive", "Heterozygous", "Codominant"], "correct_answer": "Heterozygous", "explanation": "Heterozygous means having two different alleles (one dominant B, one recessive b).", "points": 1, "order_index": 3},
    {"question_text": "In a cross Bb × Bb, what percentage of offspring are expected to be homozygous recessive (bb)?", "question_type": "multiple_choice", "options": ["0%", "25%", "50%", "75%"], "correct_answer": "25%", "explanation": "The Punnett square gives: 1 BB : 2 Bb : 1 bb. So 1/4 = 25% are bb.", "points": 1, "order_index": 4},
    {"question_text": "Which process converts DNA to mRNA?", "question_type": "multiple_choice", "options": ["Translation", "Replication", "Transcription", "Mutation"], "correct_answer": "Transcription", "explanation": "Transcription occurs in the nucleus where RNA polymerase reads DNA and creates a complementary mRNA strand.", "points": 1, "order_index": 5},
    {"question_text": "Natural selection requires all of the following EXCEPT:", "question_type": "multiple_choice", "options": ["Variation in traits", "Inheritance of traits", "Intentional breeding by humans", "Differential survival/reproduction"], "correct_answer": "Intentional breeding by humans", "explanation": "Natural selection is a natural process. Intentional breeding is artificial selection, which is a different mechanism.", "points": 1, "order_index": 6},
    {"question_text": "'Survival of the fittest' best means:", "question_type": "multiple_choice", "options": ["The strongest survive", "The fastest survive", "The best adapted to their environment survive", "The largest survive"], "correct_answer": "The best adapted to their environment survive", "explanation": "'Fitness' in biology means reproductive success — how well an organism is adapted to produce offspring in its environment.", "points": 1, "order_index": 7},
    {"question_text": "Homologous structures provide evidence for evolution because they:", "question_type": "multiple_choice", "options": ["Have the same function", "Look identical", "Share a common ancestor with similar bone structure", "Are found only in mammals"], "correct_answer": "Share a common ancestor with similar bone structure", "explanation": "Homologous structures (e.g., human arm, whale flipper, bat wing) have similar bone structure but different functions, indicating common ancestry.", "points": 1, "order_index": 8},
    {"question_text": "What is a codon?", "question_type": "multiple_choice", "options": ["A single nucleotide", "A sequence of 3 bases coding for an amino acid", "A type of protein", "A chromosome section"], "correct_answer": "A sequence of 3 bases coding for an amino acid", "explanation": "A codon is a triplet of mRNA bases that specifies one amino acid during translation. There are 64 possible codons.", "points": 1, "order_index": 9},
    {"question_text": "When populations are geographically separated and evolve into different species, this is called:", "question_type": "multiple_choice", "options": ["Natural selection", "Genetic drift", "Allopatric speciation", "Codominance"], "correct_answer": "Allopatric speciation", "explanation": "Allopatric speciation occurs when a population is split by a geographic barrier, and the separated groups evolve independently until they can no longer interbreed.", "points": 1, "order_index": 10},
]

# =====================================================================
# Database functions
# =====================================================================

COURSES = [
    {"title": "Physics: Forces, Motion & Energy", "desc": PHYSICS_DESC, "content": PHYSICS_CONTENT, "questions": PHYSICS_QUESTIONS, "grade": 9},
    {"title": "Electricity & Circuits", "desc": ELECTRICITY_DESC, "content": ELECTRICITY_CONTENT, "questions": ELECTRICITY_QUESTIONS, "grade": 10},
    {"title": "Waves, Sound & Light", "desc": WAVES_DESC, "content": WAVES_CONTENT, "questions": WAVES_QUESTIONS, "grade": 10},
    {"title": "Biology: Natural Selection & Genetics", "desc": BIOLOGY_DESC, "content": BIOLOGY_CONTENT, "questions": BIOLOGY_QUESTIONS, "grade": 9},
]

def shuffle_options(question):
    q = question.copy()
    opts = q["options"].copy()
    random.shuffle(opts)
    if q["correct_answer"] not in opts:
        opts[0] = q["correct_answer"]
        random.shuffle(opts)
    q["options"] = opts
    return q

def inject_course(cursor, course):
    # Insert the course
    cursor.execute("""
        INSERT INTO courses (title, description, content, creator_id, status, grade_level)
        VALUES (%s, %s, %s, 1, 'approved', %s)
    """, (course["title"], course["desc"], course["content"], course["grade"]))
    cursor.execute("SELECT LAST_INSERT_ID() as id")
    course_id = cursor.fetchone()["id"]
    print(f"  Inserted course ID: {course_id}")

    # Insert questions and collect IDs
    question_ids = []
    for q in course["questions"]:
        sq = shuffle_options(q)
        cursor.execute("""
            INSERT INTO course_questions
            (course_id, question_text, question_type, options, correct_answer, explanation, points, order_index)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (course_id, sq["question_text"], sq["question_type"], json.dumps(sq["options"]),
              sq["correct_answer"], sq["explanation"], sq["points"], sq["order_index"]))
        cursor.execute("SELECT LAST_INSERT_ID() as id")
        question_ids.append(cursor.fetchone()["id"])

    # Append quiz placeholders to content
    enhanced = course["content"]
    for i, qid in enumerate(question_ids, 1):
        enhanced += f'<div class="quiz-question-placeholder" data-question-id="{qid}" style="background: #e0e7ff; border: 2px solid #667eea; padding: 1.5em; margin: 1.5em 0; border-radius: 8px; user-select: none;"><strong>Quiz Question {i}</strong></div>'

    cursor.execute("UPDATE courses SET content = %s WHERE id = %s", (enhanced, course_id))
    print(f"  Added {len(question_ids)} quiz questions with placeholders")
    return course_id

def main():
    if not AIVEN_CONFIG["password"]:
        print("Set AIVEN_PASSWORD environment variable first!")
        return 1

    print("Connecting to Aiven database...")
    try:
        conn = pymysql.connect(**AIVEN_CONFIG)
    except Exception as e:
        print(f"Connection failed: {e}")
        return 1

    print("Connected!\n")
    cursor = conn.cursor()
    created = []

    try:
        for c in COURSES:
            print(f"Creating: {c['title']} (Grade {c['grade']})...")
            cid = inject_course(cursor, c)
            created.append((cid, c["title"]))

        conn.commit()
        print("\n" + "=" * 60)
        print("ALL COURSES CREATED SUCCESSFULLY!")
        print("=" * 60)
        for cid, title in created:
            print(f"  ID {cid}: {title}")
        print(f"\nTotal: {len(created)} courses with {sum(len(c['questions']) for c in COURSES)} quiz questions")
        print("Status: approved | PhET sims embedded | Quiz placeholders added")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        return 1
    finally:
        cursor.close()
        conn.close()

    return 0

if __name__ == "__main__":
    sys.exit(main())
