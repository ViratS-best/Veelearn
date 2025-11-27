# Update Quantum Physics course with full content

$baseUrl = "http://localhost:3000/api"
$courseId = 41

# Login
$loginBody = @{
    email = "viratsuper6@gmail.com"
    password = "Virat@123"
} | ConvertTo-Json

$loginResponse = Invoke-WebRequest -Uri "$baseUrl/login" `
    -Method POST `
    -ContentType "application/json" `
    -Body $loginBody `
    -ErrorAction Stop

$loginData = $loginResponse.Content | ConvertFrom-Json
$token = $loginData.data.token

Write-Host "Updating Quantum Physics course with full content..." -ForegroundColor Cyan

$fullContent = @"
<h2>Introduction to Quantum Physics</h2>
<p>Welcome to the most revolutionary physics course ever created! Quantum mechanics changed how we understand reality.</p>

<h3>Course Overview</h3>
<p>Quantum physics reveals that the universe operates very differently at atomic and subatomic scales. Learn the ideas that changed science forever.</p>

<hr>

<h3>Module 1: The Quantum Revolution - Historical Context</h3>
<p><strong>Duration:</strong> 1.5 hours</p>
<p>Why was quantum mechanics necessary? Classical physics worked perfectly for everyday objects, but failed at atomic scales:</p>
<ul>
  <li><strong>The Classical Problem:</strong> Why don't electrons fall into the nucleus?</li>
  <li><strong>The Color Problem:</strong> Why do heated materials emit specific colors of light?</li>
  <li><strong>The Stability Problem:</strong> How can atoms be stable if electrons are moving charges?</li>
</ul>
<p><strong>Key Scientists:</strong> Max Planck, Albert Einstein, Niels Bohr, Werner Heisenberg, Erwin Schrodinger</p>
<p>These brilliant minds developed the most successful theory in physics - it can predict anything about atoms with incredible accuracy!</p>

<hr>

<h3>Module 2: The Photoelectric Effect - Light is Quantized Energy</h3>
<p><strong>Duration:</strong> 2 hours</p>
<p>Einstein won the NOBEL PRIZE for explaining this phenomenon!</p>

<p><strong>The Mystery:</strong> When you shine light on metal, electrons escape. But here's what's weird:</p>
<ul>
  <li>Brighter light should give more energy, right? WRONG!</li>
  <li>Blue light ejects electrons, red light doesn't - even if red light is brighter</li>
  <li>Electrons escape INSTANTLY - there's no "charging time"</li>
</ul>

<p><strong>Classical Physics Says:</strong> Light is a continuous wave. The brighter the light, the more energy it carries. So bright red light should work better than dim blue light.</p>

<p><strong>Reality Says:</strong> NOPE! Blue light works, red light doesn't, no matter the brightness.</p>

<p><strong>Einstein's Revolutionary Idea (1905):</strong> Light doesn't come as continuous waves - it comes in PACKETS called PHOTONS!</p>

<p><strong>Key Insight:</strong> Each photon carries energy that depends on COLOR, not brightness!</p>

<p><strong>The Formula:</strong> E(photon) = h × f, where:</p>
<ul>
  <li>E = energy of one photon</li>
  <li>h = Planck's constant (6.626 × 10^-34 J·s) - smallest unit of action in universe</li>
  <li>f = frequency of light (blue light has HIGH frequency, red light has LOW frequency)</li>
</ul>

<p><strong>How It Works:</strong></p>
<ol>
  <li>One photon hits ONE electron in the metal</li>
  <li>ALL the photon's energy transfers to that ONE electron</li>
  <li>If energy is big enough (E > work function), electron escapes</li>
  <li>If energy is too small, NOTHING happens - no partial effects</li>
</ol>

<p><strong>Why Blue Works, Red Doesn't:</strong></p>
<ul>
  <li>Blue light: f = 6.5 × 10^14 Hz → E = 2.7 eV (high energy)</li>
  <li>Red light: f = 4.3 × 10^14 Hz → E = 1.8 eV (low energy)</li>
  <li>Metal requires 2.3 eV to release electron</li>
  <li>Result: Blue ejects electrons, red doesn't!</li>
</ul>

<p><strong>Real-World Applications:</strong> Solar cells, photodiodes, image sensors in cameras, motion sensors</p>

<p><strong>PhET Simulation: Photoelectric Effect</strong></p>
<p>When you use this simulation, try:</p>
<ul>
  <li>Increase intensity (brightness) - does it change if electrons are ejected?</li>
  <li>Change color to blue - electrons appear!</li>
  <li>Change color to red - electrons disappear!</li>
  <li>Check the stopping potential graph</li>
</ul>

<hr>

<h3>Module 3: Wave-Particle Duality - Everything is Both</h3>
<p><strong>Duration:</strong> 2.5 hours</p>
<p>This is where quantum mechanics gets STRANGE!</p>

<p><strong>The Fundamental Truth:</strong> EVERYTHING acts like BOTH a wave AND a particle!</p>

<p><strong>Light Double Identity:</strong></p>
<ul>
  <li>As a particle (photon): Carries energy, ejects electrons in photoelectric effect</li>
  <li>As a wave: Creates interference patterns, bends around obstacles</li>
  <li>The trick: It's BOTH, depending on how you measure it!</li>
</ul>

<p><strong>Electrons Have Secret Lives Too:</strong></p>
<ul>
  <li>We think electrons are tiny particles</li>
  <li>But they can interfere with THEMSELVES like waves!</li>
  <li>de Broglie equation: λ = h/p (wavelength = Planck's constant / momentum)</li>
</ul>

<p><strong>The Double Slit Experiment - Most Important Experiment in Physics:</strong></p>

<p>Setup: A wall with TWO slits, particles behind it, a detector screen:</p>

<p><strong>If electrons were ONLY particles:</strong></p>
<ul>
  <li>They go through slit 1 OR slit 2</li>
  <li>Screen should show TWO bright spots (one behind each slit)</li>
  <li>Simple and boring</li>
</ul>

<p><strong>If electrons were ONLY waves:</strong></p>
<ul>
  <li>They go through BOTH slits simultaneously</li>
  <li>Waves from each slit INTERFERE (overlap)</li>
  <li>Where waves reinforce → bright spots</li>
  <li>Where waves cancel → dark spots</li>
  <li>Screen shows MANY alternating bright and dark bands</li>
</ul>

<p><strong>What ACTUALLY Happens:</strong> BOTH behaviors at the same time!</p>

<p><strong>When you're NOT watching:</strong> Electrons act like waves, create interference pattern</p>

<p><strong>When you watch (measure):</strong> They act like particles, go through one slit or the other, create two spots</p>

<p><strong>This reveals the deepest mystery of quantum mechanics:</strong> OBSERVATION CHANGES REALITY!</p>

<p><strong>The Universe is probabilistic, not deterministic:</strong> We can't predict exactly where an electron will be - only the PROBABILITY of finding it.</p>

<p><strong>PhET Simulation: Quantum Wave Interference</strong></p>
<p>In this simulation:</p>
<ul>
  <li>See electrons create interference patterns (like waves)</li>
  <li>See what happens with one slit vs two slits</li>
  <li>Turn on measurement - pattern collapses!</li>
  <li>Real electron diffraction patterns from experiments</li>
</ul>

<hr>

<h3>Module 4: The Uncertainty Principle - Quantum Limits</h3>
<p><strong>Duration:</strong> 2 hours</p>

<p><strong>Heisenberg's Famous Principle:</strong> You CANNOT know both an electron's position and momentum precisely at the same time.</p>

<p><strong>The Tradeoff:</strong></p>
<ul>
  <li>Measure position very precisely → momentum becomes very uncertain</li>
  <li>Measure momentum very precisely → position becomes very uncertain</li>
  <li>It's IMPOSSIBLE to know both perfectly - this is physics, not measurement error!</li>
</ul>

<p><strong>The Formula:</strong> Δx × Δp ≥ h/4π</p>
<ul>
  <li>Δx = uncertainty in position</li>
  <li>Δp = uncertainty in momentum</li>
  <li>The product can NEVER be smaller than h/4π</li>
</ul>

<p><strong>Why does this matter?</strong> This is the reason atoms don't collapse!</p>

<p><strong>If electrons could be stationary:</strong></p>
<ul>
  <li>Position would be KNOWN (exact location in atom)</li>
  <li>Momentum would be ZERO (stationary)</li>
  <li>This would violate uncertainty principle!</li>
  <li>So electrons can never be stationary</li>
</ul>

<p><strong>Therefore:</strong> Electrons must constantly move inside atoms, preventing them from falling into nucleus!</p>

<p><strong>Energy-Time Uncertainty:</strong> ΔE × Δt ≥ h/4π</p>
<ul>
  <li>Energy can fluctuate for very short times</li>
  <li>This is why quantum tunneling is possible!</li>
</ul>

<hr>

<h3>Module 5: Quantum Tunneling - The Impossible Becomes Possible</h3>
<p><strong>Duration:</strong> 1.5 hours</p>

<p><strong>Classical Picture:</strong> A ball rolling towards a hill doesn't have enough energy to go over it? It stays in the valley forever.</p>

<p><strong>Quantum Picture:</strong> A particle approaches a barrier it classically can't overcome. It has a PROBABILITY of appearing on the other side!</p>

<p><strong>How is this possible?</strong></p>
<ul>
  <li>Particle is described by a wavefunction (probability wave)</li>
  <li>Wavefunction extends through the barrier</li>
  <li>Small probability the particle is found on the other side</li>
  <li>This happens even though it has insufficient energy!</li>
</ul>

<p><strong>Why doesn't this happen with macroscopic objects?</strong></p>
<ul>
  <li>Tunneling probability depends on barrier width and height</li>
  <li>For large objects: probability is ridiculously small (like 10^-1000000)</li>
  <li>You'd need to wait 10^1000000 seconds for it to happen once</li>
</ul>

<p><strong>Real-World Importance:</strong></p>
<ul>
  <li><strong>The Sun Shines Because:</strong> Protons in the sun's core can't classically fuse - no way they'd have enough energy. But quantum tunneling allows them to merge anyway, releasing energy through E=mc²</li>
  <li><strong>Radioactive Decay:</strong> Nuclei emit particles by tunneling through the strong nuclear force</li>
  <li><strong>Tunnel Diodes:</strong> Electronic components that use tunneling</li>
  <li><strong>Scanning Tunneling Microscopes:</strong> Can literally see individual atoms by measuring tunneling current!</li>
</ul>

<p><strong>PhET Simulation: Quantum Tunneling</strong></p>
<p>Visualize:</p>
<ul>
  <li>Particle's wavefunction approaching a barrier</li>
  <li>Probability of tunneling vs barrier height</li>
  <li>Probability of tunneling vs barrier width</li>
  <li>Energy levels and how they affect tunneling</li>
</ul>

<hr>

<h3>Module 6: Atomic Structure - Bohr's Model and Beyond</h3>
<p><strong>Duration:</strong> 2 hours</p>

<p><strong>Bohr's Model (1913):</strong> Semi-classical approach that actually worked!</p>

<p><strong>The Idea:</strong> Electrons orbit nucleus like planets orbit the sun, but with a quantum twist!</p>

<p><strong>Key Rules:</strong></p>
<ul>
  <li>Electrons can ONLY orbit at certain specific distances</li>
  <li>Only certain orbits have ALLOWED energy levels (quantized)</li>
  <li>Electrons can jump between levels by absorbing or emitting light</li>
  <li>Energy of emitted light = energy difference between levels</li>
  <li>Formula: E = hf, where f is frequency of emitted light</li>
</ul>

<p><strong>Why only certain orbits?</strong></p>
<ul>
  <li>Electron's de Broglie wavelength must fit perfectly around orbit</li>
  <li>Like standing waves on a guitar string</li>
  <li>Only wavelengths that "fit" are allowed</li>
</ul>

<p><strong>The Modern Picture (Schrodinger Equation):</strong></p>
<ul>
  <li>No definite orbital paths</li>
  <li>Instead: electron probability cloud (orbital)</li>
  <li>More accurate and explains why atoms work</li>
  <li>More complex mathematics</li>
</ul>

<p><strong>Key Consequences:</strong></p>
<ul>
  <li><strong>Discrete Spectral Lines:</strong> Atoms emit specific colors because energy levels are quantized</li>
  <li><strong>Atomic Stability:</strong> Atoms are stable because of quantized energy levels</li>
  <li><strong>Chemistry Works:</strong> Different shells of electrons explain periodic table</li>
  <li><strong>Bright Lines:</strong> Each element has unique "fingerprint" of spectral lines</li>
</ul>

<p><strong>PhET Simulation: Models of the Hydrogen Atom</strong></p>
<p>This shows:</p>
<ul>
  <li>Bohr's model with electron orbits</li>
  <li>Energy level transitions</li>
  <li>Photon absorption and emission</li>
  <li>Spectral lines matching real hydrogen data</li>
  <li>Why Bohr model has limitations</li>
</ul>

<hr>

<h3>Module 7: Blackbody Radiation - Where Quantum Started</h3>
<p><strong>Duration:</strong> 1.5 hours</p>

<p><strong>Historical Note:</strong> Planck's solution to this problem STARTED the entire quantum revolution!</p>

<p><strong>The Problem (Ultraviolet Catastrophe):</strong></p>
<ul>
  <li>Classical physics predicted hot objects should emit INFINITE energy at high frequencies (UV and beyond)</li>
  <li>But real objects don't do this</li>
  <li>Why? Classical physics couldn't explain it</li>
</ul>

<p><strong>Planck's Revolutionary Solution (1900):</strong> Energy is QUANTIZED!</p>

<p><strong>Key Equation:</strong> E = hf</p>
<ul>
  <li>h = Planck's constant</li>
  <li>f = frequency</li>
  <li>Objects can ONLY emit in multiples of hf</li>
  <li>This prevents infinite UV emission!</li>
</ul>

<p><strong>Why This Matters:</strong></p>
<ul>
  <li>Hot iron glows RED (low frequency)</li>
  <li>Hotter iron glows ORANGE (higher frequency)</li>
  <li>Even hotter iron glows YELLOW (even higher frequency)</li>
  <li>The sun glows YELLOW (because it's hot enough)</li>
  <li>A blue star is HOTTER than the sun</li>
</ul>

<p><strong>Wien's Law:</strong> λ_peak = 2.898 × 10^-3 / T (wavelength depends on temperature)</p>

<p><strong>Stefan-Boltzmann Law:</strong> P = σAT^4 (total power increases dramatically with temperature)</p>

<p><strong>Real-World Applications:</strong></p>
<ul>
  <li>Why objects glow different colors at different temperatures</li>
  <li>Why the sun is yellow, not blue or red</li>
  <li>Why the cosmic microwave background exists (relic of Big Bang)</li>
  <li>Thermal imaging cameras use this principle</li>
</ul>

<p><strong>PhET Simulation: Blackbody Spectrum</strong></p>
<p>Interact with:</p>
<ul>
  <li>Temperature slider - watch color change</li>
  <li>Intensity at different wavelengths</li>
  <li>Peak wavelength vs temperature (Wien's law in action)</li>
  <li>Total power vs temperature (Stefan-Boltzmann in action)</li>
</ul>

<hr>

<h3>Module 8: Quantum Superposition and the Measurement Problem</h3>
<p><strong>Duration:</strong> 2 hours</p>

<p><strong>Superposition:</strong> A quantum system can exist in MULTIPLE states simultaneously BEFORE measurement!</p>

<p><strong>Examples:</strong></p>
<ul>
  <li>An electron can spin UP and DOWN at the same time</li>
  <li>An electron can be in two places at once (double slit experiment)</li>
  <li>A particle can have multiple energy levels at once</li>
</ul>

<p><strong>The Measurement Problem - The Central Mystery of Quantum Mechanics:</strong></p>

<p><strong>Before Measurement:</strong> Electron exists in superposition of all possible states</p>

<p><strong>During Measurement:</strong> Wavefunction COLLAPSES to one definite state</p>

<p><strong>After Measurement:</strong> Electron is in that definite state</p>

<p><strong>The Mystery:</strong> HOW does measurement cause collapse? WHAT exactly is "measurement"?</p>

<p><strong>Schrödinger's Cat Paradox:</strong></p>
<ul>
  <li>Cat in sealed box with quantum-triggered poison device</li>
  <li>Before opening box: quantum state is "poison released AND poison not released"</li>
  <li>So cat is BOTH dead AND alive (superposition)</li>
  <li>Opening box (observing): superposition collapses</li>
  <li>Cat is either dead or alive, not both</li>
  <li><strong>Point:</strong> This shows the weirdness of applying quantum rules to macroscopic objects!</li>
</ul>

<p><strong>Why Macroscopic Objects Don't Show Superposition:</strong></p>
<ul>
  <li>Constant interaction with environment (decoherence)</li>
  <li>Temperature causes rapid measurements</li>
  <li>Superposition collapses before we can observe it</li>
</ul>

<p><strong>PhET Simulation: Stern-Gerlach Experiment</strong></p>
<p>Demonstrate:</p>
<ul>
  <li>Quantum spin measurement - one property at a time</li>
  <li>How repeated measurements give different results</li>
  <li>Superposition collapse in action</li>
  <li>Introduction to quantum entanglement</li>
</ul>

<hr>

<h3>Module 9: Quantum Applications - From Theory to Cutting-Edge Technology</h3>
<p><strong>Duration:</strong> 1.5 hours</p>

<p><strong>Semiconductors and Transistors:</strong></p>
<ul>
  <li>Based on quantum band structure of solids</li>
  <li>Quantum tunneling allows current flow</li>
  <li>Enables ALL modern electronics (phones, computers, internet)</li>
  <li>Without quantum mechanics, none of this technology exists!</li>
</ul>

<p><strong>Lasers:</strong></p>
<ul>
  <li>Based on stimulated emission (Bohr's atom transitions)</li>
  <li>Creates coherent light (all photons same phase)</li>
  <li>Used in: pointers, eye surgery, fiber optics, CD/DVD players, barcode scanners</li>
</ul>

<p><strong>Quantum Computing:</strong></p>
<ul>
  <li>Qubits use quantum superposition (can be 0 AND 1 simultaneously)</li>
  <li>Exponentially more powerful than classical bits</li>
  <li>Future of computing - breaking current encryption</li>
</ul>

<p><strong>Quantum Cryptography:</strong></p>
<ul>
  <li>Measurement collapses superposition</li>
  <li>Eavesdropping causes detectable changes</li>
  <li>Theoretically unhackable communication!</li>
</ul>

<p><strong>Medical Imaging:</strong></p>
<ul>
  <li>PET scans (Positron Emission Tomography)</li>
  <li>Uses antimatter annihilation (E=mc²)</li>
  <li>Detects cancer and other diseases</li>
</ul>

<p><strong>Nuclear Energy:</strong></p>
<ul>
  <li>Based on mass-energy equivalence (E=mc²)</li>
  <li>Nuclear fusion powers the sun</li>
  <li>Nuclear fission powers reactors</li>
</ul>

<hr>

<h3>Module 10: The Quantum-Classical Boundary</h3>
<p><strong>Duration:</strong> 1.5 hours</p>

<p><strong>The Big Question:</strong> Why don't we see quantum effects in everyday life?</p>

<p><strong>The Answer:</strong></p>

<p><strong>1. Size Effect:</strong></p>
<ul>
  <li>de Broglie wavelength = h/momentum</li>
  <li>Tennis ball: λ = 10^-33 meters (impossibly small!)</li>
  <li>Electron: λ = 10^-10 meters (observable)</li>
  <li>Larger objects = shorter wavelength = no wave effects</li>
</ul>

<p><strong>2. Temperature Effect (Decoherence):</strong></p>
<ul>
  <li>Thermal energy causes constant measurement</li>
  <li>Superposition collapses rapidly at room temperature</li>
  <li>Only at near absolute zero do quantum effects survive</li>
</ul>

<p><strong>3. Interaction with Environment:</strong></p>
<ul>
  <li>Quantum systems interact with surroundings</li>
  <li>This causes decoherence</li>
  <li>Destroys superposition and wave properties</li>
</ul>

<p><strong>The Correspondence Principle:</strong> At large scales, quantum results must approach classical predictions</p>

<p><strong>Open Questions in Quantum Physics:</strong></p>
<ul>
  <li>Where exactly is the quantum-classical boundary?</li>
  <li>Can we create superposition in larger objects?</li>
  <li>What really happens during measurement?</li>
  <li>Does consciousness affect measurement outcome?</li>
  <li>Can we merge quantum mechanics with gravity?</li>
</ul>

<hr>

<h3>Key Formulas - The Quantum Toolkit</h3>
<ul>
  <li><strong>Planck's equation:</strong> E = hf (energy of photon)</li>
  <li><strong>de Broglie wavelength:</strong> λ = h/p (wavelength of particle)</li>
  <li><strong>Uncertainty principle:</strong> Δx × Δp ≥ h/4π (position-momentum)</li>
  <li><strong>Energy-time uncertainty:</strong> ΔE × Δt ≥ h/4π</li>
  <li><strong>Einstein's energy-mass:</strong> E = mc² (mass converts to energy)</li>
  <li><strong>Photon momentum:</strong> p = h/λ = E/c</li>
  <li><strong>Wien's law:</strong> λ_peak = 2.898 × 10^-3 / T</li>
  <li><strong>Stefan-Boltzmann law:</strong> P = σAT^4</li>
</ul>

<hr>

<h3>Learning Tips for Success</h3>
<ol>
  <li><strong>Accept the Weirdness:</strong> Quantum mechanics is counter-intuitive - the universe IS weird at small scales</li>
  <li><strong>Use the Simulations:</strong> Visualizing concepts helps your brain understand abstract ideas</li>
  <li><strong>Focus on Concepts:</strong> Mathematics describes the behavior, physics explains the WHY</li>
  <li><strong>Don't Just Memorize:</strong> Understand the principles and you can derive anything</li>
  <li><strong>Question Everything:</strong> That's the scientific method - doubt is healthy!</li>
  <li><strong>Think in Probabilities:</strong> Quantum mechanics is fundamentally probabilistic</li>
</ol>

<hr>

<h3>Famous Quantum Quotes</h3>
<p><em>"If you think you understand quantum mechanics, you don't." - Richard Feynman (legendary physicist)</em></p>
<p><em>"God does not play dice." - Albert Einstein (objecting to quantum randomness)</em></p>
<p><em>"God plays not only with dice, he sometimes throws them where we can't see them." - Stephen Hawking (quantum compromise)</em></p>
<p><em>"The task is not so much to see what no one has yet seen, but to think what nobody has yet thought." - Erwin Schrodinger</em></p>
<p><em>"I don't like it, and I'm sorry I ever had anything to do with it." - Erwin Schrodinger (about wave-particle duality!)</em></p>

<hr>

<p style="margin-top: 30px; padding: 20px; background-color: #fff3cd; border-left: 4px solid #ff6b6b; border-radius: 4px;">
  <strong>Welcome to Quantum Physics!</strong> You are about to learn the most revolutionary physics discovered in the last 120 years. This knowledge shows that reality is fundamentally different from what we perceive. Atoms are mostly empty space. Particles can be in two places at once. The universe is probabilistic, not deterministic. And observation changes reality. <strong>Let the quantum journey begin!</strong> ⚛️✨
</p>
"@

$courseBody = @{
    title = "Quantum Physics: The Revolutionary Science"
    description = "Master quantum mechanics from photoelectric effect to modern quantum computing. Discover the weird world of atoms and subatomic particles."
    content = $fullContent
    status = "approved"
} | ConvertTo-Json -Depth 10

$courseResponse = Invoke-WebRequest -Uri "$baseUrl/courses/$courseId" `
    -Method PUT `
    -ContentType "application/json" `
    -Headers @{"Authorization" = "Bearer $token"} `
    -Body $courseBody `
    -ErrorAction Stop

$courseData = $courseResponse.Content | ConvertFrom-Json
if ($courseData.success) {
    Write-Host "Course updated successfully!" -ForegroundColor Green
    Write-Host "Course ID: $courseId" -ForegroundColor Cyan
    Write-Host "Full teaching content added with 10 detailed modules" -ForegroundColor Green
}
