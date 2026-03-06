$ErrorActionPreference = "Stop"
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Publishing Veelearn Frontend to gh-pages" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Ensure we are in the project's root directory
$scriptPath = $MyInvocation.MyCommand.Path
if ($scriptPath) {
    $dir = Split-Path $scriptPath
    Set-Location $dir
}

$frontendDir = "veelearn-frontend"

if (!(Test-Path $frontendDir)) {
    Write-Error "Frontend directory '$frontendDir' not found."
    exit 1
}

# Write the Custom Domain CNAME file
# This prevents GitHub Pages from resetting the domain on every push!
$cnameFile = Join-Path $frontendDir "CNAME"
"veelearn.org" | Out-File -FilePath $cnameFile -Encoding ascii
Write-Host "Set up CNAME 'veelearn.org' to automatically configure the custom domain..." -ForegroundColor Green

# Ensure it is committed to avoid issues
git add $frontendDir/CNAME
$gitStatus = git status --porcelain $frontendDir/CNAME
if ($gitStatus) {
    Write-Host "Committing CNAME file to the repository..."
    git commit -m "Auto-deploy: setup CNAME for custom domain"
}

Write-Host "Creating instantaneous deployment commit..." -ForegroundColor Cyan
try {
    # 1. Get the tree-hash of the frontend directory
    $tree_hash = git rev-parse "HEAD:$frontendDir"
    
    # 2. Create a fresh commit just for this tree
    $commit_hash = git commit-tree $tree_hash -m "Auto-deploy $frontendDir to GitHub pages"
    
    # 3. Force push this commit to the gh-pages branch on origin
    Write-Host "Pushing to 'gh-pages' branch on origin..." -ForegroundColor Cyan
    git push origin "$($commit_hash):refs/heads/gh-pages" --force
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "=========================================" -ForegroundColor Green
        Write-Host "  Success! Frontend has been published." -ForegroundColor Green
        Write-Host "=========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "GitHub Pages will build and deploy https://veelearn.org/ in ~1 minute." -ForegroundColor Yellow
        Write-Host "You do NOT need to manually configure the custom domain anymore!" -ForegroundColor Yellow
    }
    else {
        Write-Error "Failed to push to GitHub Pages. Ensure you have the right git permissions."
    }
}
catch {
    Write-Error "An error occurred during deployment: $_"
}
