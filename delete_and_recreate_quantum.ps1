# Delete old quantum course and create new one with full content

$baseUrl = "http://localhost:3000/api"

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

Write-Host "Deleting old course..." -ForegroundColor Yellow

# Delete course 41
$deleteResponse = Invoke-WebRequest -Uri "$baseUrl/courses/41" `
    -Method DELETE `
    -Headers @{"Authorization" = "Bearer $token"} `
    -ErrorAction Stop

Write-Host "Old course deleted" -ForegroundColor Green

Write-Host "Creating new Quantum Physics course with full content..." -ForegroundColor Cyan

$fullContent = @"
<h2>Introduction to Quantum Physics</h2>
<p>Welcome to the most revolutionary physics course ever created! Quantum mechanics changed how we understand reality.</p>
<h3>Course Overview</h3>
<p>Quantum physics reveals that the universe operates very differently at atomic and subatomic scales. Learn the ideas that changed science forever.</p>
<h3>Module 1: The Quantum Revolution - Historical Context</h3>
<p><strong>Duration:</strong> 1.5 hours</p>
<p>Why was quantum mechanics necessary? Classical physics worked perfectly for everyday objects, but failed at atomic scales:</p>
<ul><li><strong>The Classical Problem:</strong> Why don't electrons fall into the nucleus?</li><li><strong>The Color Problem:</strong> Why do heated materials emit specific colors of light?</li><li><strong>The Stability Problem:</strong> How can atoms be stable if electrons are moving charges?</li></ul>
<p><strong>Key Scientists:</strong> Max Planck, Albert Einstein, Niels Bohr, Werner Heisenberg, Erwin Schrodinger</p>
<h3>Module 2: The Photoelectric Effect - Light is Quantized Energy</h3>
<p><strong>Duration:</strong> 2 hours</p>
<p>Einstein won the NOBEL PRIZE for explaining this phenomenon!</p>
<p><strong>The Mystery:</strong> When you shine light on metal, electrons escape. But here's what's weird:</p>
<ul><li>Brighter light should give more energy, right? WRONG!</li><li>Blue light ejects electrons, red light doesn't - even if red light is brighter</li><li>Electrons escape INSTANTLY - there's no "charging time"</li></ul>
<p><strong>Einstein's Revolutionary Idea (1905):</strong> Light doesn't come as continuous waves - it comes in PACKETS called PHOTONS!</p>
<p><strong>Key Formula:</strong> E(photon) = h × f</p>
<ul><li>E = energy of one photon</li><li>h = Planck's constant (6.626 × 10^-34 J·s)</li><li>f = frequency of light</li></ul>
<h3>Module 3: Wave-Particle Duality - Everything is Both</h3>
<p><strong>Duration:</strong> 2.5 hours</p>
<p>This is where quantum mechanics gets STRANGE!</p>
<p><strong>The Fundamental Truth:</strong> EVERYTHING acts like BOTH a wave AND a particle!</p>
<p><strong>Light Double Identity:</strong></p>
<ul><li>As a particle (photon): Carries energy, ejects electrons</li><li>As a wave: Creates interference patterns</li><li>The trick: It's BOTH, depending on how you measure it!</li></ul>
<p><strong>The Double Slit Experiment - Most Important Experiment in Physics:</strong></p>
<p>When you're NOT watching: Electrons act like waves, create interference pattern</p>
<p>When you watch (measure): They act like particles, go through one slit or the other</p>
<p><strong>This reveals the deepest mystery:</strong> OBSERVATION CHANGES REALITY!</p>
<h3>Module 4: The Uncertainty Principle - Quantum Limits</h3>
<p><strong>Duration:</strong> 2 hours</p>
<p><strong>Heisenberg's Famous Principle:</strong> You CANNOT know both an electron's position and momentum precisely at the same time.</p>
<p><strong>Formula:</strong> Δx × Δp ≥ h/4π</p>
<p><strong>Why does this matter?</strong> This is the reason atoms don't collapse! If electrons could be stationary (known position, zero momentum), they would violate this principle.</p>
<h3>Module 5: Quantum Tunneling - The Impossible Becomes Possible</h3>
<p><strong>Duration:</strong> 1.5 hours</p>
<p>In quantum physics, particles can tunnel THROUGH barriers they classically can't overcome!</p>
<p><strong>Real-World Importance:</strong></p>
<ul><li><strong>The Sun Shines Because:</strong> Protons tunnel through the strong nuclear force to fuse</li><li><strong>Radioactive Decay:</strong> Nuclei emit particles by tunneling</li><li><strong>Scanning Tunneling Microscopes:</strong> Can see individual atoms!</li></ul>
<h3>Module 6: Atomic Structure - Bohr and Beyond</h3>
<p><strong>Duration:</strong> 2 hours</p>
<p><strong>Bohr's Model (1913):</strong> Electrons orbit nucleus like planets orbit the sun, but only at specific distances!</p>
<p><strong>Key Rules:</strong></p>
<ul><li>Electrons can ONLY orbit at certain specific distances</li><li>Only certain orbits have ALLOWED energy levels (quantized)</li><li>Electrons jump between levels by absorbing or emitting light</li><li>Energy of emitted light = energy difference between levels</li></ul>
<p><strong>Consequences:</strong></p>
<ul><li>Discrete Spectral Lines: Atoms emit specific colors because energy levels are quantized</li><li>Atomic Stability: Atoms are stable because of quantized energy levels</li><li>Chemistry Works: Different shells explain the periodic table</li></ul>
<h3>Module 7: Blackbody Radiation - Where Quantum Started</h3>
<p><strong>Duration:</strong> 1.5 hours</p>
<p><strong>Planck's Revolutionary Solution (1900):</strong> Energy is QUANTIZED! E = hf</p>
<p><strong>Why This Matters:</strong></p>
<ul><li>Hot iron glows RED (low frequency)</li><li>Hotter iron glows ORANGE (higher frequency)</li><li>Even hotter iron glows YELLOW (even higher frequency)</li><li>The sun glows YELLOW (because it's hot enough)</li></ul>
<p><strong>Wien's Law:</strong> λ_peak = 2.898 × 10^-3 / T</p>
<h3>Module 8: Quantum Superposition and the Measurement Problem</h3>
<p><strong>Duration:</strong> 2 hours</p>
<p><strong>Superposition:</strong> A quantum system can exist in MULTIPLE states simultaneously BEFORE measurement!</p>
<p><strong>The Measurement Problem - The Central Mystery of Quantum Mechanics:</strong></p>
<ul><li>Before Measurement: Electron exists in superposition of all possible states</li><li>During Measurement: Wavefunction COLLAPSES to one definite state</li><li>After Measurement: Electron is in that definite state</li></ul>
<p><strong>Schrödinger's Cat Paradox:</strong> Cat in sealed box with quantum-triggered poison device. Before opening: cat is BOTH dead AND alive. After opening: collapse to one state.</p>
<h3>Module 9: Quantum Applications - Technology and Future</h3>
<p><strong>Duration:</strong> 1.5 hours</p>
<ul><li><strong>Semiconductors:</strong> All modern electronics based on quantum band structure</li><li><strong>Lasers:</strong> Based on stimulated emission and quantum transitions</li><li><strong>Quantum Computing:</strong> Qubits use superposition for exponential power</li><li><strong>Quantum Cryptography:</strong> Unhackable communication using quantum mechanics</li><li><strong>Medical Imaging:</strong> PET scans use antimatter annihilation (E=mc²)</li></ul>
<h3>Module 10: The Quantum-Classical Boundary</h3>
<p><strong>Duration:</strong> 1.5 hours</p>
<p><strong>Why don't we see quantum effects in everyday life?</strong></p>
<ul><li>Larger objects have shorter de Broglie wavelengths</li><li>Temperature causes decoherence (rapid measurement)</li><li>Interaction with environment destroys superposition</li></ul>
<p><strong>Open Questions:</strong></p>
<ul><li>Where exactly is the quantum-classical boundary?</li><li>Can we create superposition in larger objects?</li><li>What really happens during measurement?</li><li>Can we merge quantum mechanics with gravity?</li></ul>
<h3>Key Formulas</h3>
<ul><li>Planck's equation: E = hf</li><li>de Broglie wavelength: λ = h/p</li><li>Uncertainty principle: Δx × Δp ≥ h/4π</li><li>Einstein's energy-mass: E = mc²</li><li>Photon momentum: p = h/λ = E/c</li></ul>
<p style="margin-top: 30px; padding: 20px; background-color: #fff3cd; border-left: 4px solid #ff6b6b; border-radius: 4px;"><strong>Welcome to Quantum Physics!</strong> You are about to learn the most revolutionary physics discovered in the last 120 years. Reality is fundamentally different from what we perceive. ⚛️</p>
"@

$courseBody = @{
    title = "Quantum Physics: The Revolutionary Science"
    description = "Master quantum mechanics from photoelectric effect to modern quantum computing. Discover the weird world of atoms and subatomic particles."
    content = $fullContent
    status = "approved"
} | ConvertTo-Json -Depth 10

$courseResponse = Invoke-WebRequest -Uri "$baseUrl/courses" `
    -Method POST `
    -ContentType "application/json" `
    -Headers @{"Authorization" = "Bearer $token"} `
    -Body $courseBody `
    -ErrorAction Stop

$courseData = $courseResponse.Content | ConvertFrom-Json
$courseId = $courseData.data.id

Write-Host "New course created with ID: $courseId" -ForegroundColor Green
Write-Host "`nFull Quantum Physics content is now live!" -ForegroundColor Cyan
