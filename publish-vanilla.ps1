$ErrorActionPreference = "Stop"
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Publishing Veelearn Vanilla Frontend" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

$scriptPath = $MyInvocation.MyCommand.Path
if ($scriptPath) {
    Set-Location (Split-Path $scriptPath)
}

$frontendDir = "veelearn-frontend"
$outputDir = "docs"

if (!(Test-Path $frontendDir)) {
    Write-Error "Vanilla frontend directory '$frontendDir' not found."
    exit 1
}

Write-Host "Preparing build output..." -ForegroundColor Cyan
if (Test-Path $outputDir) {
    Remove-Item -Path "$outputDir/*" -Recurse -Force
} else {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

Write-Host "Copying vanilla frontend files..." -ForegroundColor Cyan
Copy-Item -Path "$frontendDir/*" -Destination $outputDir -Recurse -Force

Write-Host "Set up CNAME 'veelearn.org'..." -ForegroundColor Green
"veelearn.org" | Out-File -FilePath "$outputDir/CNAME" -Encoding ascii

Write-Host "Deploying to GitHub Pages..." -ForegroundColor Cyan
try {
    git add $outputDir
    $gitStatus = git status --porcelain $outputDir
    if ($gitStatus) {
        Write-Host "Committing changes..." -ForegroundColor Yellow
        git commit -m "Auto-deploy: Reverting to full-featured vanilla frontend"
    } else {
        Write-Host "No changes to deploy." -ForegroundColor Yellow
    }
    
    $tree_hash = git rev-parse "HEAD:$outputDir"
    $commit_hash = git commit-tree $tree_hash -m "Auto-deploy Veelearn vanilla frontend to GitHub pages"
    
    Write-Host "Pushing to 'gh-pages' branch..." -ForegroundColor Cyan
    git push origin "$commit_hash`:refs/heads/gh-pages" --force
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "=========================================" -ForegroundColor Green
        Write-Host "  Success! Full vanilla frontend deployed." -ForegroundColor Green
        Write-Host "=========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "GitHub Pages will deploy in ~1-2 minutes." -ForegroundColor Yellow
    } else {
        Write-Error "Failed to push to GitHub Pages."
    }
} catch {
    Write-Error "Deploy failed: $_"
}
