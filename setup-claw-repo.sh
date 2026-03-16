#!/bin/bash
# Setup script for creating a new GitHub repo for CLAW
# This gives CLAW its own copy to work on with full permissions

set -e

echo "==================================="
echo "CLAW Repository Setup Script"
echo "==================================="
echo ""

# Configuration
NEW_REPO_NAME="${1:-python-oop-journey-claw}"
GITHUB_USER="${2:-Richicinschi}"
SOURCE_DIR="$(pwd)"
TEMP_DIR="/tmp/claw-repo-setup"

echo "Configuration:"
echo "  New Repo Name: $NEW_REPO_NAME"
echo "  GitHub User: $GITHUB_USER"
echo "  Source: $SOURCE_DIR"
echo ""

# Step 1: Create temporary directory
echo "[1/6] Creating temporary directory..."
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR"

# Step 2: Initialize git repo
echo "[2/6] Initializing git repository..."
git init
git config user.name "CLAW Bot"
git config user.email "claw@oop-journey.local"

# Step 3: Copy all files
echo "[3/6] Copying files from source..."
# Use rsync if available, otherwise cp -r
if command -v rsync &> /dev/null; then
    rsync -av --exclude='.git' --exclude='node_modules' --exclude='__pycache__' \
          --exclude='.next' --exclude='*.pyc' --exclude='venv' \
          "$SOURCE_DIR/" "$TEMP_DIR/"
else
    cp -r "$SOURCE_DIR"/* "$TEMP_DIR/" 2>/dev/null || true
    cp -r "$SOURCE_DIR"/.* "$TEMP_DIR/" 2>/dev/null || true
fi

# Step 4: Create CLAW-specific .gitignore additions
echo "[4/6] Creating CLAW-specific configurations..."

# Update AGENTS.md to remove git push restrictions
cat >> AGENTS.md << 'EOF'

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
EOF

# Create CLAW git config
cat > .claw/git-config.yaml << EOF
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
    origin: "https://github.com/$GITHUB_USER/$NEW_REPO_NAME.git"
EOF

# Step 5: Commit all files
echo "[5/6] Committing files..."
git add -A
git commit -m "Initial commit: CLAW workspace for Python OOP Journey

- Full website (Next.js + FastAPI)
- Complete curriculum (9 weeks, 453 exercises)
- Agency agents library
- CLAW memory files configured for website repair
- 7,456+ tests passing

This is a dedicated workspace for CLAW to fix the website."

# Step 6: Instructions for GitHub setup
echo ""
echo "[6/6] Setup complete!"
echo ""
echo "==================================="
echo "NEXT STEPS:"
echo "==================================="
echo ""
echo "1. Create new GitHub repository:"
echo "   https://github.com/new"
echo "   Name: $NEW_REPO_NAME"
echo "   Visibility: Public (or Private)"
echo "   ❌ DO NOT initialize with README"
echo ""
echo "2. Push to GitHub:"
echo "   cd $TEMP_DIR"
echo "   git remote add origin https://github.com/$GITHUB_USER/$NEW_REPO_NAME.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Connect Kimi Claw:"
echo "   - Go to Kimi Claw dashboard"
echo "   - Connect: github.com/$GITHUB_USER/$NEW_REPO_NAME"
echo "   - CLAW will auto-detect .claw/soul.yaml"
echo ""
echo "4. CLAW will:"
echo "   - Read AGENTS.md (now with push permissions)"
echo "   - Read all memory files"
echo "   - Start fixing the 500 errors"
echo "   - Push commits as it progresses"
echo ""
echo "==================================="
echo "TEMP DIRECTORY: $TEMP_DIR"
echo "==================================="
