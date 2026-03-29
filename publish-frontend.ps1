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

# Step 3: Ensure output directory exists and copy built files
Write-Host "Preparing build output..." -ForegroundColor Cyan
if (Test-Path $outputDir) {
    Remove-Item -Path "$outputDir/*" -Recurse -Force
} else {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

# Copy the built files from React dist to docs
Copy-Item -Path "$reactDir/dist/*" -Destination $outputDir -Recurse

# Also copy the simulator files from the old frontend
$oldFrontend = "veelearn-frontend"
if (Test-Path $oldFrontend) {
    Write-Host "Copying simulator files..." -ForegroundColor Cyan
    
    # Copy HTML files that need to be available
    $simulatorFiles = @(
        "block-simulator.html",
        "visual-simulator.html",
        "simulator-marketplace.html",
        "simulator-view.html",
        "simulator-execute.html"
    )
    
    foreach ($file in $simulatorFiles) {
        $src = Join-Path $oldFrontend $file
        if (Test-Path $src) {
            Copy-Item -Path $src -Destination $outputDir -Force
            Write-Host "  Copied $file" -ForegroundColor Green
        }
    }
    
    # Copy JS files needed for simulators
    $jsFiles = Get-ChildItem -Path $oldFrontend -Filter "*.js"
    foreach ($file in $jsFiles) {
        Copy-Item -Path $file.FullName -Destination $outputDir -Force
    }
    
    # Copy CSS
    $cssFiles = Get-ChildItem -Path $oldFrontend -Filter "*.css"
    foreach ($file in $cssFiles) {
        Copy-Item -Path $file.FullName -Destination $outputDir -Force
    }
}

# Write the Custom Domain CNAME file
$cnameFile = Join-Path $outputDir "CNAME"
"veelearn.org" | Out-File -FilePath $cnameFile -Encoding ascii
Write-Host "Set up CNAME 'veelearn.org'..." -ForegroundColor Green

# Step 4: Commit and push
Write-Host "Deploying to GitHub Pages..." -ForegroundColor Cyan
try {
    # Add all changes
    git add $outputDir
    
    # Check if there are changes to commit
    $gitStatus = git status --porcelain $outputDir
    if ($gitStatus) {
        Write-Host "Committing changes..." -ForegroundColor Yellow
        git commit -m "Auto-deploy: Veelearn React frontend build"
    } else {
        Write-Host "No changes to deploy." -ForegroundColor Yellow
    }
    
    # Push to gh-pages
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
        Write-Host "GitHub Pages will deploy https://veelearn.org/ in ~1-2 minutes." -ForegroundColor Yellow
    }
    else {
        Write-Error "Failed to push to GitHub Pages."
    }
}
catch {
    Write-Error "An error occurred: $_"
}
