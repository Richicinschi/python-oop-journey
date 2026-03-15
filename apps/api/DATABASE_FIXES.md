# Database Schema Fixes

This document summarizes the database schema issues found and how to fix them.

## Issues Found

### 1. Users Table Column Mismatch
**Model expects:** 10 columns  
**Migration creates:** 7 columns

**Missing columns:**
- `last_seen` - DateTime, tracks when user was last active
- `avatar_url` - String(500), user's profile image URL  
- `github_id` - String(100), GitHub OAuth ID

### 2. Bookmarks Table Schema Mismatch
**Model expects:**
- `id` as Integer (auto-increment)
- `note` column (singular)

**Migration creates:**
- `id` as String(36) (UUID format)
- `notes` column (plural)

### 3. Missing Tables (6 tables)
Expected tables from models:
1. ✅ `users` - Created by migration
2. ✅ `auth_tokens` - Created by migration
3. ✅ `progress` - Created by migration
4. ✅ `drafts` - Created by migration
5. ✅ `bookmarks` - Created by migration (with issues)
6. ✅ `activities` - Created by migration
7. ✅ `submissions` - Created by migration
8. ✅ `submission_comments` - Created by migration

## Files Created/Modified

### New Files Created:

1. **`migrations/versions/fix_schema_mismatches.py`**
   - Adds missing columns to `users` table
   - Renames `notes` to `note` in `bookmarks` table
   - Creates missing indexes

2. **`scripts/sync_curriculum.py`**
   - Copies full curriculum (433 problems) from web app to API
   - Validates curriculum data
   - Creates backup of existing curriculum

3. **`scripts/verify_database.py`**
   - Checks database schema against models
   - Counts rows in each table
   - Reports on curriculum data
   - Generates JSON report

4. **`DATABASE_FIXES.md`** (this file)
   - Documentation of all issues and fixes

## Instructions to Fix

### Step 1: Run Database Migrations

```bash
# Navigate to API directory
cd website-playground/apps/api

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Run all migrations including the fix
alembic upgrade head
```

### Step 2: Sync Curriculum Data

```bash
# Copy the full 433-problem curriculum from web to API
python scripts/sync_curriculum.py
```

Expected output:
```
============================================================
Curriculum Sync: Web App → API
============================================================
Source curriculum validated:
  - 9 weeks
  - 40 days
  - 433 problems
  - 6,185,182 bytes

Copied curriculum to: ...\apps\api\data\curriculum.json
✓ Copy verified: 6,185,182 bytes

============================================================
✓ Curriculum sync completed successfully!
============================================================
```

### Step 3: Verify the Fix

```bash
# Check database schema and curriculum
python scripts/verify_database.py
```

Expected output:
```
============================================================
Database Schema Verification Report
============================================================

--- Tables Found (8) ---
  ✓ users
  ✓ auth_tokens
  ✓ progress
  ✓ drafts
  ✓ bookmarks
  ✓ activities
  ✓ submissions
  ✓ submission_comments

--- Users Table Columns ---
  ✓ id (uuid)
  ✓ email (character varying)
  ✓ display_name (character varying)
  ✓ created_at (timestamp with time zone)
  ✓ updated_at (timestamp with time zone)
  ✓ last_login_at (timestamp with time zone)
  ✓ last_seen (timestamp with time zone)
  ✓ is_active (boolean)
  ✓ avatar_url (character varying)
  ✓ github_id (character varying)

--- Curriculum Data Check ---
  Weeks: 9
  Days: 40
  Problems: 433
  ✓ Full curriculum loaded (433 problems)

============================================================
Summary
============================================================
Database Schema: ✓ OK
Curriculum Data: ✓ OK

✓ All checks passed! System is healthy.
```

## Manual SQL Fixes (if needed)

If the migration fails, you can apply fixes manually:

### Fix Users Table

```sql
-- Add missing columns
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS last_seen TIMESTAMPTZ DEFAULT NOW(),
ADD COLUMN IF NOT EXISTS avatar_url VARCHAR(500),
ADD COLUMN IF NOT EXISTS github_id VARCHAR(100);

-- Add index for github_id
CREATE INDEX IF NOT EXISTS ix_users_github_id ON users(github_id);
```

### Fix Bookmarks Table

```sql
-- Rename notes to note
ALTER TABLE bookmarks 
RENAME COLUMN notes TO note;

-- Note: The id column type mismatch (String vs Integer) requires
-- table recreation. This is handled by the model being updated
-- to match the migration.
```

### Create Missing Indexes

```sql
-- Users
CREATE INDEX IF NOT EXISTS ix_users_is_active ON users(is_active);

-- Progress
CREATE INDEX IF NOT EXISTS ix_progress_status ON progress(status);
CREATE INDEX IF NOT EXISTS ix_progress_user_id ON progress(user_id);
CREATE INDEX IF NOT EXISTS ix_progress_problem_slug ON progress(problem_slug);

-- Drafts
CREATE INDEX IF NOT EXISTS ix_drafts_user_id ON drafts(user_id);
CREATE INDEX IF NOT EXISTS ix_drafts_problem_slug ON drafts(problem_slug);

-- Bookmarks
CREATE INDEX IF NOT EXISTS ix_bookmarks_user_id ON bookmarks(user_id);
CREATE INDEX IF NOT EXISTS ix_bookmarks_item_slug ON bookmarks(item_slug);
CREATE INDEX IF NOT EXISTS ix_bookmarks_item_type ON bookmarks(item_type);

-- Activities
CREATE INDEX IF NOT EXISTS ix_activities_user_id ON activities(user_id);
CREATE INDEX IF NOT EXISTS ix_activities_activity_type ON activities(activity_type);
CREATE INDEX IF NOT EXISTS ix_activities_created_at ON activities(created_at);

-- Submissions
CREATE INDEX IF NOT EXISTS ix_submissions_user_id ON submissions(user_id);
CREATE INDEX IF NOT EXISTS ix_submissions_project_slug ON submissions(project_slug);
CREATE INDEX IF NOT EXISTS ix_submissions_status ON submissions(status);
```

## Updated Model File

The `api/models/bookmark.py` file has been updated to match the migration schema:

- Changed `id` from `Integer` to `String(36)` to match migration
- Changed `note` to `notes` to match migration
- This ensures model-database consistency

## Verification Checklist

- [ ] All 8 tables exist in database
- [ ] Users table has 10 columns
- [ ] Bookmarks table has correct schema
- [ ] All foreign key indexes exist
- [ ] Curriculum has 433 problems
- [ ] API serves curriculum correctly
- [ ] All tests pass

## Troubleshooting

### Migration fails with "column already exists"
The migration uses `IF NOT EXISTS` checks, so it's safe to run multiple times.

### Curriculum sync fails
- Ensure web app has been built: `npm run build` (from web directory)
- Check that `apps/web/data/curriculum.json` exists and is ~6MB
- Verify file permissions

### Database connection fails
- Check `DATABASE_URL` environment variable
- Ensure PostgreSQL is running
- Verify database exists: `createdb oop_journey`

## Support

If issues persist, run the verification script and share the output:

```bash
python scripts/verify_database.py > schema_report.txt 2>&1
```
