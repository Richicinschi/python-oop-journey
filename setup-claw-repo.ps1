# CLAW Repository Setup Script for Windows PowerShell
# Run this in PowerShell to create a new GitHub repo for CLAW

param(
    [string]$NewRepoName = "python-oop-journey-claw",
    [string]$GitHubUser = "Richicinschi"
)

Write-Host "===================================" -ForegroundColor Cyan
Write-Host "CLAW Repository Setup Script" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

$SourceDir = Get-Location
$TempDir = "$env:TEMP\claw-repo-setup"

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  New Repo Name: $NewRepoName"
Write-Host "  GitHub User: $GitHubUser"
Write-Host "  Source: $SourceDir"
Write-Host "  Temp: $TempDir"
Write-Host ""

# Step 1: Create temporary directory
Write-Host "[1/6] Creating temporary directory..." -ForegroundColor Green
if (Test-Path $TempDir) {
    Remove-Item -Recurse -Force $TempDir
}
New-Item -ItemType Directory -Path $TempDir | Out-Null
Set-Location $TempDir

# Step 2: Initialize git repo
Write-Host "[2/6] Initializing git repository..." -ForegroundColor Green
git init
git config user.name "CLAW Bot"
git config user.email "claw@oop-journey.local"

# Step 3: Copy all files (excluding git, node_modules, etc.)
Write-Host "[3/6] Copying files from source..." -ForegroundColor Green
Write-Host "      This may take a few minutes..." -ForegroundColor Gray

$ExcludePatterns = @(
    '.git',
    'node_modules',
    '__pycache__',
    '.next',
    '*.pyc',
    'venv',
    '.venv',
    'dist',
    'build'
)

function Copy-Filtered {
    param([string]$Source, [string]$Dest)
    
    Get-ChildItem $Source -Force | ForEach-Object {
        $name = $_.Name
        if ($ExcludePatterns -contains $name) {
            return
        }
        
        $destPath = Join-Path $Dest $name
        if ($_.PSIsContainer) {
            New-Item -ItemType Directory -Path $destPath -Force | Out-Null
            Copy-Filtered -Source $_.FullName -Dest $destPath
        } else {
            Copy-Item $_.FullName $destPath -Force
        }
    }
}

Copy-Filtered -Source $SourceDir -Dest $TempDir

# Step 4: Update AGENTS.md with CLAW permissions
Write-Host "[4/6] Creating CLAW-specific configurations..." -ForegroundColor Green

$GitPermissions = @"

## CLAW-Specific Permissions (Remote Instance)

Since this is a dedicated CLAW workspace:

✅ **CLAW CAN:**
- Push commits to this repository
- Create and merge pull requests
- Modify git configuration
- Force push (when necessary)
- Delete branches
- Manage releases

**Git Workflow:**
1. Create feature branch: `git checkout -b fix/week-page-500`
2. Make fixes
3. Commit: `git commit -m "Fix: week detail page 500 error"`
4. Push: `git push origin fix/week-page-500`
5. Merge to main when verified

**Emergency Actions:**
If CLAW needs to reset:
- `git reset --hard HEAD~5` (last 5 commits)
- `git push --force` (if needed)
- All actions are logged in MEMORY.md
"@

Add-Content -Path "AGENTS.md" -Value $GitPermissions

# Create CLAW git config
$GitConfigContent = @"
# CLAW Git Configuration
git:
  user:
    name: "CLAW"
    email: "claw@oop-journey.ai"
  
  permissions:
    push: true
    force_push: true
    merge: true
    delete_branch: true
    create_tag: true
  
  workflow:
    branch_prefix: "claw/"
    commit_prefix: "[CLAW]"
    auto_commit_frequency: "on_success"
  
  remotes:
    origin: "https://github.com/$GitHubUser/$NewRepoName.git"
"@

New-Item -ItemType Directory -Path ".claw" -Force | Out-Null
Set-Content -Path ".claw/git-config.yaml" -Value $GitConfigContent

# Step 5: Commit all files
Write-Host "[5/6] Committing files..." -ForegroundColor Green
Write-Host "      This may take a few minutes for large repos..." -ForegroundColor Gray

git add -A
$CommitMessage = @"
Initial commit: CLAW workspace for Python OOP Journey

- Full website (Next.js + FastAPI)
- Complete curriculum (9 weeks, 453 exercises)
- Agency agents library
- CLAW memory files configured for website repair
- 7,456+ tests passing

This is a dedicated workspace for CLAW to fix the website.
"@
git commit -m $CommitMessage

# Step 6: Instructions
Write-Host ""
Write-Host "[6/6] Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "===================================" -ForegroundColor Cyan
Write-Host "NEXT STEPS:" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Create new GitHub repository:" -ForegroundColor Yellow
Write-Host "   https://github.com/new"
Write-Host "   Name: $NewRepoName"
Write-Host "   Visibility: Public (or Private)"
Write-Host "   DO NOT initialize with README"
Write-Host ""
Write-Host "2. Push to GitHub:" -ForegroundColor Yellow
Write-Host "   cd $TempDir"
Write-Host "   git remote add origin https://github.com/$GitHubUser/$NewRepoName.git"
Write-Host "   git branch -M main"
Write-Host "   git push -u origin main"
Write-Host ""
Write-Host "3. Connect Kimi Claw:" -ForegroundColor Yellow
Write-Host "   - Go to Kimi Claw dashboard"
Write-Host "   - Connect: github.com/$GitHubUser/$NewRepoName"
Write-Host "   - CLAW will auto-detect .claw/soul.yaml"
Write-Host ""
Write-Host "4. CLAW will:" -ForegroundColor Yellow
Write-Host "   - Read AGENTS.md (now with push permissions)"
Write-Host "   - Read all memory files"
Write-Host "   - Start fixing the 500 errors"
Write-Host "   - Push commits as it progresses"
Write-Host ""
Write-Host "===================================" -ForegroundColor Cyan
Write-Host "TEMP DIRECTORY: $TempDir" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan

# Return to original directory
Set-Location $SourceDir
