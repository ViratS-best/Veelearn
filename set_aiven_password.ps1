# Windows PowerShell Script to Set Aiven Password
# Run this before running Python scripts: .\set_aiven_password.ps1

param(
    [string]$Password
)

if (-not $Password) {
    Write-Host "Aiven Database Password Setup" -ForegroundColor Cyan
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host ""
    $Password = Read-Host "Enter Aiven Database Password" -AsSecureString
    $Password = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToCoTaskMemUni($Password))
}

# Set environment variable for this session
$env:AIVEN_PASSWORD = $Password
$env:AIVEN_HOST = "veelearndb-asterloop-483e.i.aivencloud.com"
$env:AIVEN_PORT = "26399"
$env:AIVEN_USER = "avnadmin"
$env:AIVEN_DB = "defaultdb"

Write-Host ""
Write-Host "✅ Environment variables set!" -ForegroundColor Green
Write-Host ""
Write-Host "You can now run:" -ForegroundColor Cyan
Write-Host "  python3 create_courses_aiven.py" -ForegroundColor Yellow
Write-Host "  python3 add_phet_simulators.py" -ForegroundColor Yellow
Write-Host "  python3 verify_courses_aiven.py" -ForegroundColor Yellow
Write-Host ""
