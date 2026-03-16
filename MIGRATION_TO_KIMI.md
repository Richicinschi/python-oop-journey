# Migration Guide: Your AI Setup → Kimi Code CLI

## Current State → Target State Mapping

| Your Current File | Kimi Equivalent | Status |
|-------------------|-----------------|--------|
| `AGENTS.md` | `AGENTS.md` | ✅ Compatible (keep as-is) |
| `IDENTITY.md` | `USER.md` + `.claw/personality.yaml` | ⚠️ Needs conversion |
| `SOUL.md` | `USER.md` + `.claw/personality.yaml` | ⚠️ Needs conversion |
| `USER.md` | `USER.md` | ⚠️ Merge into Kimi format |
| `MEMORY.md` | `memory.md` | ✅ Already exists |
| `BOOTSTRAP.md` | Not needed | ❌ Discard (Kimi has its own) |
| `HEARTBEAT.md` | Part of `memory.md` | ⚠️ Consolidate |
| `TOOLS.md` | `.claw/tools.yaml` | ⚠️ Needs conversion |

## Migration Steps

### Step 1: Copy Your Core Files to Kimi Workspace

```bash
# Copy these files to your oopkimi workspace:
cp AGENTS.md ~/oopkimi/AGENTS.md.backup
cp IDENTITY.md ~/oopkimi/USER_IDENTITY.md
cp SOUL.md ~/oopkimi/USER_SOUL.md
cp USER.md ~/oopkimi/USER_PREFERENCES.md
cp MEMORY.md ~/oopkimi/MEMORY_BACKUP.md
cp TOOLS.md ~/oopkimi/USER_TOOLS.md
cp HEARTBEAT.md ~/oopkimi/HEARTBEAT_BACKUP.md
```

### Step 2: Run the Migration Script

I've created a migration script that will:
1. Merge your IDENTITY + SOUL + USER into Kimi's USER.md format
2. Convert TOOLS.md to .claw/tools.yaml
3. Set up the .claw/ directory structure
4. Keep your MEMORY intact

### Step 3: Give Kimi Claw Access to Your Website

After migration, you'll have:
- `.claw/soul.yaml` - Already created
- `.claw/instructions.md` - Setup guide
- `.claw/personality.yaml` - Your character/personality
- `.claw/tools.yaml` - Your environment tools
- `USER.md` - Your identity + user notes merged
- `HEARTBEAT.md` - Periodic tasks (if any)

### Step 4: Deploy to Claw

Once files are in place:
1. Push to GitHub
2. Connect to Kimi Claw
3. The `.claw/` folder auto-configures the environment
4. Claw reads your personality and acts accordingly

## What Stays the Same

- Your project structure
- Your git history
- Your code
- Your curriculum (python-oop-journey-v2)

## What Changes

- AI personality is now configured via `.claw/` files
- USER.md format changes (Kimi-specific)
- No more BOOTSTRAP (Kimi handles initialization)
- HEARTBEAT tasks become entries in memory.md

## Post-Migration Workflow

```
1. Start Kimi Code CLI
2. Kimi reads AGENTS.md → knows how to work
3. Kimi reads USER.md → knows your preferences
4. Kimi reads .claw/personality.yaml → knows your character
5. Kimi reads memory.md → knows project state
6. You're ready to work
```

## Files You Need to Provide

Please share the contents of:
1. **IDENTITY.md** - Your name, vibe, chuunibyou guardian thing
2. **SOUL.md** - Personality, taste, speech patterns
3. **USER.md** - Notes about me (the user)
4. **TOOLS.md** - Cameras, SSH hosts, environment notes
5. **HEARTBEAT.md** - Any periodic check tasks

I'll convert them to Kimi format.
