# GitHub Repository Setup Guide

Step-by-step guide to create your GitHub repo and commit the right files.

---

## What You Need to Commit

### ✅ DO Commit These:

```
website-playground/
├── apps/
│   ├── web/                    # Next.js frontend
│   │   ├── app/               # Pages
│   │   ├── components/        # React components
│   │   ├── hooks/             # Custom hooks
│   │   ├── lib/               # Utilities
│   │   ├── types/             # TypeScript types
│   │   ├── public/            # Static files
│   │   ├── next.config.js     # Build config
│   │   ├── package.json       # Dependencies
│   │   └── tsconfig.json      # TypeScript config
│   │
│   └── api/                    # FastAPI backend
│       ├── api/               # API code
│       │   ├── models/        # Database models
│       │   ├── routers/       # API endpoints
│       │   ├── services/      # Business logic
│       │   └── middleware/    # Middleware
│       ├── migrations/        # Database migrations
│       ├── tests/             # Test files
│       ├── Dockerfile         # Docker config
│       ├── fly.toml           # Fly.io config (if using Fly)
│       ├── requirements.txt   # Python dependencies
│       └── alembic.ini        # Migration config
│
├── packages/                   # Shared packages
│   ├── shared/                # TypeScript types
│   ├── ui/                    # UI components
│   └── curriculum/            # Content ingestion
│
├── docs/                       # Documentation
├── scripts/                    # Deployment scripts
├── package.json               # Root package.json
├── turbo.json                 # Monorepo config
└── README.md                  # Project readme
```

### ❌ DO NOT Commit These:

```
# Secrets & Environment files (NEVER!)
.env
.env.local
.env.production
apps/api/.env
apps/web/.env.local

# Dependencies (they get installed)
node_modules/
__pycache__/
*.pyc
.pytest_cache/
.venv/
venv/

# Build outputs (generated automatically)
dist/
build/
.next/
out/

# Local databases
*.db
*.sqlite
*.sqlite3

# IDE files
.vscode/
.idea/
*.swp
*.swo
*~

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Testing
coverage/
.nyc_output/

# Temporary files
*.tmp
*.temp
cache/
```

---

## Step 1: Create .gitignore File

**Create this file in your project root:** `website-playground/.gitignore`

```gitignore
# See https://help.github.com/articles/ignoring-files/ for more about ignoring files.

# Dependencies
node_modules
.pnp
.pnp.js
.yarn/install-state.gz

# Testing
coverage
*.lcov
.nyc_output

# Build outputs
.next/
out/
dist/
build/
.turbo

# Environment files (NEVER COMMIT THESE!)
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
.pytest_cache/
.mypy_cache/
.dmypy.json
dmypy.json
*.mo
*.pot
*.log
local_settings.py
instance/
.webassets-cache
.scrapy
docs/_build/
target/
.ipynb_checkpoints
profile_default/
ipython_config.py
.python-version

# Database
*.db
*.sqlite
*.sqlite3

# IDE
.vscode/*
!.vscode/extensions.json
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
ehthumbs.db
Desktop.ini
$RECYCLE.BIN/

# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*
.pnpm-debug.log*

# Misc
.cache
.temp
.tmp
*.pid
*.seed
*.pid.lock

# Render/Fly local files
.fly/
render.yaml

# Local development
*.local
```

---

## Step 2: Initialize Git Repository

Open terminal/command prompt in your project folder:

```bash
# Navigate to your project folder
cd C:\Users\digitalnomad\Documents\oopkimi\website-playground

# Initialize git
git init

# Check status (see what files are ready to commit)
git status
```

You should see a lot of "untracked files" - this is good!

---

## Step 3: Add Files to Git

```bash
# Add all files (except those in .gitignore)
git add .

# Check what's being added
git status
```

Make sure you see:
- ✅ Green files = will be committed
- ❌ No .env files (should be ignored)
- ❌ No node_modules (should be ignored)

---

## Step 4: Create First Commit

```bash
# Create the first commit
git commit -m "Initial commit - Python OOP Journey platform"

# Check commit was created
git log
```

You should see your commit in the log.

---

## Step 5: Create GitHub Repository

### 5.1 Create Repo on GitHub

1. Go to https://github.com/new
2. Fill in:
   - **Repository name:** `python-oop-journey`
   - **Description:** `Python OOP learning platform with interactive coding`
   - **Visibility:** Public (or Private - your choice)
   - ✅ **Initialize with README:** NO (you already have one)
   - ✅ **Add .gitignore:** NO (you already created one)
   - ✅ **Choose a license:** NO
3. Click **"Create repository"**

### 5.2 Get Your Repo URL

After creation, you'll see:

```
https://github.com/YOUR_USERNAME/python-oop-journey.git
```

**Copy this URL!**

---

## Step 6: Push to GitHub

Back in your terminal:

```bash
# Add the GitHub remote (use YOUR actual URL)
git remote add origin https://github.com/YOUR_USERNAME/python-oop-journey.git

# Verify remote was added
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

Enter your GitHub username and password/token when prompted.

---

## Step 7: Verify on GitHub

1. Go to https://github.com/YOUR_USERNAME/python-oop-journey
2. You should see all your files!
3. Check that `.env` files are NOT there (they shouldn't be)
4. Check that `node_modules` is NOT there

---

## What Files Should Be on GitHub?

### ✅ Good - These SHOULD be there:
- `apps/web/app/` (your pages)
- `apps/web/components/` (React components)
- `apps/api/api/` (backend code)
- `package.json` files
- `README.md`
- `requirements.txt`
- `Dockerfile`

### ❌ Bad - These should NOT be there:
- `.env` files (secrets!)
- `node_modules/` folders
- `__pycache__/` folders
- `.next/` folders
- `dist/` folders

---

## Common Issues

### Issue: "fatal: not a git repository"
**Fix:** You ran `git init` in the wrong folder. Navigate to the correct folder first:
```bash
cd C:\Users\digitalnomad\Documents\oopkimi\website-playground
git init
```

### Issue: ".env file is being committed"
**Fix:** You created .gitignore AFTER adding files. Do this:
```bash
git rm --cached .env
git rm --cached apps/api/.env
git rm --cached apps/web/.env.local
git commit -m "Remove env files"
```

### Issue: "node_modules is too big"
**Fix:** Make sure .gitignore includes `node_modules` BEFORE adding files.

### Issue: "Permission denied" on push
**Fix:** You need a GitHub token instead of password:
1. Go to https://github.com/settings/tokens
2. Generate new token (classic)
3. Select "repo" scope
4. Copy token and use as password

---

## Quick Reference Commands

```bash
# Check status
git status

# Add new files
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push

# Pull latest changes
git pull

# View commit history
git log --oneline

# Undo last commit (if needed)
git reset --soft HEAD~1
```

---

## After GitHub Setup

Once your code is on GitHub, you can:
1. ✅ Connect Render to your repo (auto-deploy)
2. ✅ Connect Cloudflare Pages to your repo (auto-deploy)
3. ✅ Share the project with others

---

**Next Step:** Create the .gitignore file, then run the git commands above!
