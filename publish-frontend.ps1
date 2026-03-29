$ErrorActionPreference = "Stop"
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Publishing Veelearn React Frontend" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Ensure we are in the project's root directory
$scriptPath = $MyInvocation.MyCommand.Path
if ($scriptPath) {
    $dir = Split-Path $scriptPath
    Set-Location $dir
}

$reactDir = "veelearn-react"
$outputDir = "docs"

if (!(Test-Path $reactDir)) {
    Write-Error "React frontend directory '$reactDir' not found."
    exit 1
}

# Check if Node.js is available
$nodeCheck = Get-Command node -ErrorAction SilentlyContinue
if (!$nodeCheck) {
    Write-Error "Node.js is not installed or not in PATH. Please install Node.js first."
    exit 1
}

# Step 1: Install dependencies if node_modules doesn't exist
Write-Host "Checking dependencies..." -ForegroundColor Cyan
if (!(Test-Path "$reactDir/node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    Push-Location $reactDir
    npm install
    if ($LASTEXITCODE -ne 0) {
        Pop-Location
        Write-Error "Failed to install dependencies."
        exit 1
    }
    Pop-Location
}

# Step 2: Build the React project
Write-Host "Building React application..." -ForegroundColor Cyan
Push-Location $reactDir
npm run build
if ($LASTEXITCODE -ne 0) {
    Pop-Location
    Write-Error "Build failed. Check the errors above."
    exit 1
}
Pop-Location

# Step 3: Clean and prepare output directory
Write-Host "Preparing build output..." -ForegroundColor Cyan
if (Test-Path $outputDir) {
    Remove-Item -Path "$outputDir/*" -Recurse -Force
}
New-Item -ItemType Directory -Path $outputDir | Out-Null

# Copy the built React files
Write-Host "Copying React build..." -ForegroundColor Cyan
Copy-Item -Path "$reactDir/dist/*" -Destination $outputDir -Recurse

# Only copy the simulator JS files (not HTML - React handles those now)
Write-Host "Copying simulator libraries..." -ForegroundColor Cyan
$simulatorJsFiles = @(
    "block-templates-unified.js",
    "block-physics-engine.js",
    "block-renderer-system.js",
    "block-animation.js",
    "block-execution-engine.js"
)

$oldFrontend = "veelearn-frontend"
foreach ($file in $simulatorJsFiles) {
    $src = Join-Path $oldFrontend $file
    if (Test-Path $src) {
        Copy-Item -Path $src -Destination $outputDir -Force
        Write-Host "  Copied $file" -ForegroundColor Green
    }
}

# Copy simulators folder from React build
if (Test-Path "$reactDir/dist/simulators") {
    Copy-Item -Path "$reactDir/dist/simulators" -Destination $outputDir -Recurse -Force
}

# Write the Custom Domain CNAME file
$cnameFile = Join-Path $outputDir "CNAME"
"veelearn.org" | Out-File -FilePath $cnameFile -Encoding ascii
Write-Host "Set up CNAME 'veelearn.org'..." -ForegroundColor Green

# Step 4: Commit and push
Write-Host "Deploying to GitHub Pages..." -ForegroundColor Cyan
try {
    git add $outputDir
    $gitStatus = git status --porcelain $outputDir
    if ($gitStatus) {
        Write-Host "Committing changes..." -ForegroundColor Yellow
        git commit -m "Auto-deploy: Veelearn React frontend build"
    } else {
        Write-Host "No changes to deploy." -ForegroundColor Yellow
    }
    
    $tree_hash = git rev-parse "HEAD:$outputDir"
    $commit_hash = git commit-tree $tree_hash -m "Auto-deploy Veelearn to GitHub pages"
    
    Write-Host "Pushing to 'gh-pages' branch..." -ForegroundColor Cyan
    git push origin "$($commit_hash):refs/heads/gh-pages" --force
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "=========================================" -ForegroundColor Green
        Write-Host "  Success! Frontend has been published." -ForegroundColor Green
        Write-Host "=========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "GitHub Pages will deploy in ~1-2 minutes." -ForegroundColor Yellow
    }
    else {
        Write-Error "Failed to push to GitHub Pages."
    }
}
catch {
    Write-Error "An error occurred: $_"
}
