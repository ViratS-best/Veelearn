# Update course 42 with full Quantum Physics content - NO SPECIAL CHARS

$baseUrl = "http://localhost:3000/api"
$courseId = 42

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

Write-Host "Updating Quantum Physics course with comprehensive content..." -ForegroundColor Cyan

$fullContent = "<h2>Introduction to Quantum Physics</h2><p>Welcome to the most revolutionary physics course! Quantum mechanics changed how we understand reality.</p><h3>Module 1: The Quantum Revolution</h3><p>Why was quantum mechanics necessary? Classical physics failed at atomic scales:</p><ul><li>Why don't electrons fall into nucleus?</li><li>Why do heated materials emit specific colors?</li><li>How are atoms stable with moving charges?</li></ul><p>Key scientists: Planck, Einstein, Bohr, Heisenberg, Schrodinger</p><h3>Module 2: The Photoelectric Effect</h3><p><strong>Einstein won Nobel Prize for this!</strong> When light hits metal, electrons escape. But:</p><ul><li>Brighter light doesnt always work</li><li>Blue light works, red doesn't - even if red is brighter</li><li>Electrons escape INSTANTLY</li></ul><p><strong>Einstein's Idea:</strong> Light comes in PACKETS called PHOTONS!</p><p><strong>Formula:</strong> E = h times f, where h is Planck's constant and f is frequency</p><p><strong>How it works:</strong> One photon transfers ALL energy to ONE electron. If energy enough, electron escapes. If not, nothing happens.</p><h3>Module 3: Wave-Particle Duality</h3><p><strong>Fundamental Truth:</strong> EVERYTHING acts like BOTH a wave AND a particle!</p><p><strong>Light Double Identity:</strong></p><ul><li>As particle (photon): Carries energy, ejects electrons</li><li>As wave: Creates interference patterns</li><li>BOTH, depending on how you measure it!</li></ul><p><strong>The Double Slit Experiment:</strong> Most important experiment in physics!</p><p>When NOT watching: Electrons act like waves, create interference pattern</p><p>When watching (measuring): They act like particles, go through one slit</p><p><strong>KEY INSIGHT:</strong> OBSERVATION CHANGES REALITY!</p><h3>Module 4: The Uncertainty Principle</h3><p><strong>Heisenberg's Principle:</strong> Cannot know position AND momentum precisely at same time.</p><p><strong>Why matters:</strong> This is why atoms don't collapse!</p><ul><li>If electrons could be stationary (known position, zero momentum) = violates principle</li><li>So electrons must constantly move inside atoms</li><li>This prevents them falling into nucleus</li></ul><h3>Module 5: Quantum Tunneling</h3><p><strong>Classical Picture:</strong> Ball without enough energy can't go over hill. Stays in valley.</p><p><strong>Quantum Picture:</strong> Particles tunnel THROUGH barriers classically impossible!</p><p><strong>Real-World Importance:</strong></p><ul><li><strong>The Sun Shines:</strong> Protons tunnel and fuse, releasing energy via E=mc²</li><li><strong>Radioactive Decay:</strong> Nuclei emit particles by tunneling</li><li><strong>Scanning Tunneling Microscopes:</strong> See individual atoms by measuring tunneling current!</li></ul><h3>Module 6: Atomic Structure - Bohr Model</h3><p><strong>Bohr's Model (1913):</strong> Electrons orbit nucleus like planets, but only at SPECIFIC distances!</p><p><strong>Key Rules:</strong></p><ul><li>Electrons ONLY at certain distances</li><li>Only certain orbits have ALLOWED energy levels (quantized)</li><li>Electrons jump between levels by absorbing/emitting light</li><li>Energy of light = energy difference: E = hf</li></ul><p><strong>Why only certain orbits?</strong> Electron's de Broglie wavelength must fit like standing wave on guitar string!</p><p><strong>Consequences:</strong></p><ul><li>Atoms emit SPECIFIC colors (discrete spectral lines)</li><li>Atoms are STABLE (no collapse)</li><li>Chemistry works (electron shells)</li></ul><h3>Module 7: Blackbody Radiation</h3><p><strong>Planck's Solution (1900):</strong> Energy is QUANTIZED! E = hf</p><p><strong>This STARTED the quantum revolution!</strong></p><p><strong>Why This Matters:</strong></p><ul><li>Hot iron glows RED (low frequency)</li><li>Hotter iron glows ORANGE (higher frequency)</li><li>Even hotter iron glows YELLOW</li><li>Sun glows YELLOW (correct temperature)</li><li>Blue star is HOTTER than sun</li></ul><h3>Module 8: Superposition and Measurement</h3><p><strong>Superposition:</strong> System exists in MULTIPLE states simultaneously BEFORE measurement!</p><p><strong>Examples:</strong></p><ul><li>Electron spin UP and DOWN at same time</li><li>Electron in two places at once</li><li>Particle with multiple energy levels</li></ul><p><strong>The Measurement Problem - Central Mystery:</strong></p><ul><li><strong>Before Measurement:</strong> Superposition of all states</li><li><strong>During Measurement:</strong> Wavefunction COLLAPSES</li><li><strong>After Measurement:</strong> One definite state</li></ul><p><strong>Schrodinger's Cat Paradox:</strong> Cat in sealed box with quantum poison. Before opening: BOTH dead AND alive. After opening: collapses to one state.</p><h3>Module 9: Quantum Applications</h3><p><strong>All modern technology depends on quantum mechanics!</strong></p><ul><li><strong>Semiconductors:</strong> All electronics - phones, computers, internet</li><li><strong>Lasers:</strong> Eye surgery, fiber optics, CD players, barcode scanners</li><li><strong>Quantum Computing:</strong> Qubits in superposition = exponential power</li><li><strong>Quantum Cryptography:</strong> Unhackable communication</li><li><strong>Medical Imaging:</strong> PET scans use antimatter annihilation</li></ul><h3>Module 10: The Quantum-Classical Boundary</h3><p><strong>Why don't we see quantum effects?</strong></p><ul><li>Larger objects = shorter wavelength = no wave effects</li><li>Temperature causes decoherence (rapid measurement)</li><li>Interaction with environment destroys superposition</li></ul><p><strong>Open Questions:</strong></p><ul><li>Where is quantum-classical boundary?</li><li>Can we create superposition in larger objects?</li><li>What really happens during measurement?</li><li>Can we merge quantum mechanics with gravity?</li></ul><h3>Key Formulas</h3><ul><li>Planck: E = hf</li><li>de Broglie: wavelength = h/p</li><li>Uncertainty: position times momentum greater than h/4pi</li><li>Einstein: E = mc squared</li></ul><p style='margin-top: 30px; padding: 20px; background-color: #fff3cd; border-left: 4px solid #ff6b6b; border-radius: 4px;'><strong>Welcome to Quantum Physics!</strong> You are learning the most revolutionary physics of the last 120 years. Reality is fundamentally different from what we perceive. Atoms are mostly empty space. Particles can be in two places at once. The universe is probabilistic. And observation changes reality. Let the quantum journey begin! Atoms at scale!</p>"

$courseBody = @{
    title = "Quantum Physics: The Revolutionary Science"
    description = "Master quantum mechanics - photoelectric effect, wave-particle duality, uncertainty principle, quantum tunneling, and more."
    content = $fullContent
    status = "approved"
} | ConvertTo-Json -Depth 10

try {
    $courseResponse = Invoke-WebRequest -Uri "$baseUrl/courses/$courseId" `
        -Method PUT `
        -ContentType "application/json" `
        -Headers @{"Authorization" = "Bearer $token"} `
        -Body $courseBody `
        -ErrorAction Stop

    $courseData = $courseResponse.Content | ConvertFrom-Json
    if ($courseData.success) {
        Write-Host "SUCCESS!" -ForegroundColor Green
        Write-Host "Course $courseId updated with FULL Quantum Physics content" -ForegroundColor Cyan
        Write-Host "`nCourse is now LIVE with comprehensive teaching material!" -ForegroundColor Green
        Write-Host "`nRECOMMENDED PhET SIMULATORS TO ADD:" -ForegroundColor Magenta
        Write-Host "  1. Photoelectric Effect" -ForegroundColor Yellow
        Write-Host "  2. Quantum Wave Interference (Double Slit)" -ForegroundColor Yellow
        Write-Host "  3. Quantum Tunneling" -ForegroundColor Yellow
        Write-Host "  4. Models of the Hydrogen Atom" -ForegroundColor Yellow
        Write-Host "  5. Blackbody Spectrum" -ForegroundColor Yellow
        Write-Host "  6. Stern-Gerlach Experiment" -ForegroundColor Yellow
    }
} catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
}
