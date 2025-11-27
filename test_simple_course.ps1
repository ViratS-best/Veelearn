# Test with simple content

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

Write-Host "Testing course creation..." -ForegroundColor Cyan

$simpleContent = "<h2>Quantum Physics</h2><h3>Module 1: Photoelectric Effect</h3><p>Einstein won Nobel Prize explaining light as photons. Formula: E = hf</p><h3>Module 2: Wave-Particle Duality</h3><p>Everything acts as both wave and particle depending on measurement.</p><h3>Module 3: Uncertainty Principle</h3><p>Cannot know position and momentum precisely at same time.</p><h3>Module 4: Quantum Tunneling</h3><p>Particles tunnel through barriers. Enables nuclear fusion in sun.</p><h3>Module 5: Atomic Structure</h3><p>Bohr model with quantized energy levels and electron transitions.</p><h3>Module 6: Superposition</h3><p>Systems in multiple states before measurement. Measurement collapses wavefunction.</p><h3>Module 7: Blackbody Radiation</h3><p>Planck quantization explains energy emission from hot objects.</p><h3>Module 8: Applications</h3><p>Lasers, transistors, quantum computers, quantum cryptography, medical imaging.</p>"

$courseBody = @{
    title = "Quantum Physics: The Revolutionary Science"
    description = "Master quantum mechanics - photoelectric effect, wave-particle duality, uncertainty principle, quantum tunneling, and more."
    content = $simpleContent
    status = "approved"
} | ConvertTo-Json

Write-Host "Sending request..." -ForegroundColor Yellow

try {
    $courseResponse = Invoke-WebRequest -Uri "$baseUrl/courses" `
        -Method POST `
        -ContentType "application/json" `
        -Headers @{"Authorization" = "Bearer $token"} `
        -Body $courseBody `
        -ErrorAction Stop

    $courseData = $courseResponse.Content | ConvertFrom-Json
    $courseId = $courseData.data.id

    Write-Host "SUCCESS! Course created with ID: $courseId" -ForegroundColor Green
    Write-Host "`nQuantum Physics course is now LIVE!" -ForegroundColor Cyan
} catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
}
