# Simple Quantum Physics course creation

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

Write-Host "Creating Quantum Physics course..." -ForegroundColor Cyan

# Create course with simpler content
$courseBody = @{
    title = "Quantum Physics: The Revolutionary Science"
    description = "Master quantum mechanics from photoelectric effect to modern quantum computing. Discover the weird world of atoms and subatomic particles."
    content = "<h2>Quantum Physics Course</h2><p>This course teaches the fundamentals of quantum mechanics, the most successful physics theory ever created.</p><h3>Modules</h3><ul><li>Photoelectric Effect - Einstein's light quanta</li><li>Wave-Particle Duality - Everything is both wave and particle</li><li>Uncertainty Principle - Physical limits of knowledge</li><li>Quantum Tunneling - The impossible becomes possible</li><li>Atomic Structure - Bohr model and beyond</li><li>Blackbody Radiation - Planck's quantum solution</li><li>Superposition - Schrödinger's cat paradox</li><li>Modern Applications - Lasers, transistors, quantum computers</li></ul>"
    status = "approved"
} | ConvertTo-Json

$courseResponse = Invoke-WebRequest -Uri "$baseUrl/courses" `
    -Method POST `
    -ContentType "application/json" `
    -Headers @{"Authorization" = "Bearer $token"} `
    -Body $courseBody `
    -ErrorAction Stop

$courseData = $courseResponse.Content | ConvertFrom-Json
$courseId = $courseData.data.id

Write-Host "Course created: ID $courseId" -ForegroundColor Green

Write-Host "`nRECOMMENDED PhET SIMULATORS FOR QUANTUM COURSE" -ForegroundColor Magenta
Write-Host "=" * 60

Write-Host @"

Module 1: PHOTOELECTRIC EFFECT
  Simulator: Photoelectric Effect
  URL: https://phet.colorado.edu/sims/html/photoelectric-effect/latest/photoelectric-effect_en.html
  Why: Shows electrons being ejected from metal by light photons
  Concepts: E=hf, photon energy, threshold frequency, stopping potential
  Learn: Why blue light works but red light doesn't

Module 2: WAVE-PARTICLE DUALITY
  Simulator: Quantum Wave Interference
  URL: https://phet.colorado.edu/sims/html/quantum-wave-interference/latest/quantum-wave-interference_en.html
  Why: Classic double-slit experiment with electrons
  Concepts: Interference patterns, superposition, measurement collapse
  Learn: How observation changes reality

Module 3: UNCERTAINTY PRINCIPLE
  Simulator: Davisson-Germer Experiment (or Quantum Wave Interference)
  URL: https://phet.colorado.edu/sims/html/quantum-wave-interference/latest/quantum-wave-interference_en.html
  Why: Shows electron diffraction patterns proving wave nature
  Concepts: de Broglie wavelength, momentum-position uncertainty
  Learn: Why atoms don't collapse

Module 4: QUANTUM TUNNELING
  Simulator: Quantum Tunneling and Wave Packets
  URL: https://phet.colorado.edu/sims/html/quantum-tunneling/latest/quantum-tunneling_en.html
  Why: Particles tunneling through barriers classically forbidden
  Concepts: Tunneling probability, barrier height and width effects
  Learn: Why nuclear fusion happens in the sun

Module 5: ATOMIC STRUCTURE
  Simulator: Models of the Hydrogen Atom
  URL: https://phet.colorado.edu/sims/html/models-of-the-hydrogen-atom/latest/models-of-the-hydrogen-atom_en.html
  Why: Bohr model with electron transitions and spectral lines
  Concepts: Quantized energy levels, photon emission/absorption
  Learn: Why atoms emit discrete colors of light

Module 6: BLACKBODY RADIATION
  Simulator: Blackbody Spectrum
  URL: https://phet.colorado.edu/sims/html/blackbody-spectrum/latest/blackbody-spectrum_en.html
  Why: How hot objects emit different wavelengths at different temperatures
  Concepts: Wien's law, Stefan-Boltzmann law, Planck's quantization
  Learn: Why the sun is yellow, not blue or red

Module 7: SUPERPOSITION
  Simulator: Stern-Gerlach Experiment
  URL: https://phet.colorado.edu/sims/html/stern-gerlach-experiment/latest/stern-gerlach-experiment_en.html
  Why: Quantum spin measurement and superposition collapse
  Concepts: Quantum superposition, measurement problem, entanglement
  Learn: Why measurement affects quantum systems

Module 8: ADDITIONAL
  Simulator: Electron Diffraction
  URL: https://phet.colorado.edu/sims/html/electron-diffraction/latest/electron-diffraction_en.html
  Why: Real-world application showing electron wavelike properties
  Concepts: Diffraction patterns, electron microscopy
  Learn: How we see atoms and molecules

HOW TO ADD THESE TO YOUR COURSE:
================================

1. Open browser: http://localhost:5000
2. Login to dashboard
3. Go to "My Courses"
4. Find "Quantum Physics: The Revolutionary Science"
5. Click "Edit" button
6. In course editor, click "⚛️ PhET Simulator" button
7. A modal will open - search for simulator name
8. Click to select and add to course
9. Repeat for all 8 simulators
10. Click "Save as Draft"

KEY LEARNING OUTCOMES:
======================
By the end of this course, students will:
✓ Understand wave-particle duality
✓ Explain the photoelectric effect
✓ Know why atoms are stable (uncertainty principle)
✓ Understand quantum tunneling
✓ Know how atomic spectra work
✓ Understand quantum superposition
✓ Learn applications in technology

COURSE ID: $courseId
STATUS: PUBLISHED & APPROVED
READY FOR: Student enrollment and learning

"@ -ForegroundColor Green
