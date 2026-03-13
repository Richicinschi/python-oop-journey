# Alembic Migration Chain Audit Report

**Audit Date:** 2026-03-12  
**Auditor:** Migration Chain Auditor  
**Location:** `website-playground/apps/api/migrations/versions/`

---

## Executive Summary

**Status:** ⚠️ **NEEDS ATTENTION** - Critical model-migration mismatches detected

The migration chain is **linear and correctly ordered**, but there are **data type mismatches** and **missing columns** between migrations and models that will cause runtime errors.

---

## 1. Migration Chain Visualization

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MIGRATION CHAIN (LINEAR)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────┐                                               │
│  │ add_users_and_auth_     │  ← First migration (down_revision: None)      │
│  │ _tokens                 │                                               │
│  │ Revision: add_users_    │                                               │
│  │ and_auth_tokens         │                                               │
│  └───────────┬─────────────┘                                               │
│              │ down_revision                                               │
│              ▼                                                              │
│  ┌─────────────────────────┐                                               │
│  │ add_progress_drafts_    │  ← Second migration                           │
│  │ bookmarks_activity      │                                               │
│  │ Revision: add_progress_ │                                               │
│  │ drafts_bookmarks_       │                                               │
│  │ activity                │                                               │
│  └───────────┬─────────────┘                                               │
│              │ down_revision                                               │
│              ▼                                                              │
│  ┌─────────────────────────┐                                               │
│  │ add_submissions         │  ← Third migration                            │
│  │ Revision: add_          │                                               │
│  │ submissions             │                                               │
│  └───────────┬─────────────┘                                               │
│              │ down_revision                                               │
│              ▼                                                              │
│  ┌─────────────────────────┐                                               │
│  │ add_performance_indexes │  ← Fourth migration (HEAD)                    │
│  │ Revision: add_          │                                               │
│  │ performance_indexes     │                                               │
│  └─────────────────────────┘                                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Chain Verification

| Migration File | Revision ID | down_revision | Status |
|----------------|-------------|---------------|--------|
| `add_users_and_auth_tokens.py` | `add_users_and_auth_tokens` | `None` | ✅ Base |
| `add_progress_drafts_bookmarks_activity.py` | `add_progress_drafts_bookmarks_activity` | `add_users_and_auth_tokens` | ✅ Correct |
| `add_submissions.py` | `add_submissions` | `add_progress_drafts_bookmarks_activity` | ✅ Correct |
| `add_performance_indexes.py` | `add_performance_indexes` | `add_submissions` | ✅ Correct |

**Result:** Chain is linear with no branches or multiple heads. ✅

---

## 2. Table Creation Order Analysis

### Dependency Graph

```
                    ┌─────────────┐
                    │    users    │ ← Root table (created first)
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┬──────────────────┐
        │                  │                  │                  │
        ▼                  ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  auth_tokens  │  │   progress    │  │    drafts     │  │  bookmarks    │
│  (user_id FK) │  │  (user_id FK) │  │  (user_id FK) │  │  (user_id FK) │
└───────────────┘  └───────────────┘  └───────────────┘  └───────────────┘
        │
        │           ┌───────────────┐  ┌───────────────┐
        │           │  activities   │  │  submissions  │
        │           │  (user_id FK) │  │ (user_id FK)  │
        │           └───────────────┘  └───────┬───────┘
        │                                      │
        │                                      ▼
        │                              ┌───────────────┐
        │                              │submission_    │
        │                              │  comments     │
        │                              │(submission_id │
        │                              │   FK)         │
        │                              │(user_id FK)   │
        │                              └───────────────┘
        ▼
┌─────────────────────────────────────────────────────────────────┐
│              PERFORMANCE INDEXES (Final Migration)                │
│  - idx_progress_user_problem    (on progress table)               │
│  - idx_progress_status          (on progress table)               │
│  - idx_activity_user_created    (on activities table)             │
│  - idx_bookmarks_user_type      (on bookmarks table)              │
└─────────────────────────────────────────────────────────────────┘
```

### Table Creation Order by Migration

| Migration | Tables Created | Dependencies | Status |
|-----------|----------------|--------------|--------|
| 1. `add_users_and_auth_tokens` | `users`, `auth_tokens` | users before auth_tokens | ✅ Correct |
| 2. `add_progress_drafts_bookmarks_activity` | `progress`, `drafts`, `bookmarks`, `activities` | All depend on `users` | ✅ Correct |
| 3. `add_submissions` | `submissions`, `submission_comments` | submissions before submission_comments | ✅ Correct |
| 4. `add_performance_indexes` | Indexes only | Tables must exist first | ✅ Correct |

---

## 3. Idempotency Analysis

### Operations Review

| Migration | Operation | Idempotent? | Issue |
|-----------|-----------|-------------|-------|
| 1. `add_users_and_auth_tokens` | `op.create_table('users')` | ❌ **NO** | No `IF NOT EXISTS` |
| 1. `add_users_and_auth_tokens` | `op.create_index('ix_users_email')` | ❌ **NO** | No `IF NOT EXISTS` |
| 1. `add_users_and_auth_tokens` | `op.create_table('auth_tokens')` | ❌ **NO** | No `IF NOT EXISTS` |
| 2. `add_progress_drafts_bookmarks_activity` | Multiple `create_table` | ❌ **NO** | No `IF NOT EXISTS` |
| 2. `add_progress_drafts_bookmarks_activity` | Multiple `create_index` | ❌ **NO** | No `IF NOT EXISTS` |
| 3. `add_submissions` | `create_table` with inline index | ❌ **NO** | No `IF NOT EXISTS` |
| 4. `add_performance_indexes` | `op.create_index()` | ❌ **NO** | No `IF NOT EXISTS` |

### Risk Assessment

**⚠️ CRITICAL:** None of the migrations use `IF NOT EXISTS` clauses. If migrations are run twice:
- **PostgreSQL:** Will fail with "relation already exists" error
- **CockroachDB:** Will fail with "relation already exists" error

### Recommended Fixes

For PostgreSQL/CockroachDB compatibility, wrap operations:

```python
# Instead of:
op.create_table('users', ...)

# Use:
from sqlalchemy import inspect
conn = op.get_bind()
inspector = inspect(conn)
if 'users' not in inspector.get_table_names():
    op.create_table('users', ...)
```

Or use raw SQL with `IF NOT EXISTS`:

```python
op.execute("""
    CREATE TABLE IF NOT EXISTS users (
        ...
    )
""")
```

---

## 4. Model-Migration Synchronization Issues

### Critical Mismatches

#### 4.1 Bookmark Model - Primary Key Type Mismatch ⚠️ **CRITICAL**

| Source | Column | Type |
|--------|--------|------|
| **Migration** | `id` | `sa.String(36)` |
| **Model** | `id` | `Integer` |

**Issue:** Migration creates String UUID, model expects auto-increment Integer.

**File:** `api/models/bookmark.py` line 26

```python
# Model has:
id = Column(Integer, primary_key=True, index=True)

# Migration creates:
sa.Column('id', sa.String(36), nullable=False)  # UUID
```

**Impact:** ORM will fail when saving bookmarks - type mismatch.

---

#### 4.2 Bookmark Model - Column Name Mismatch ⚠️ **CRITICAL**

| Source | Column | Name |
|--------|--------|------|
| **Migration** | notes column | `notes` |
| **Model** | notes column | `note` (singular) |

**Issue:** Migration creates `notes`, model has `note`.

**Files:**
- Migration: `add_progress_drafts_bookmarks_activity.py` line 76
- Model: `api/models/bookmark.py` line 30

```python
# Model has:
note = Column(Text, nullable=True)

# Migration creates:
sa.Column('notes', sa.Text, nullable=True)
```

**Impact:** ORM will fail - column not found.

---

#### 4.3 Activity Model - Column Name Mismatch ⚠️ **CRITICAL**

| Source | Column | Name |
|--------|--------|------|
| **Migration** | metadata column | `meta_data` |
| **Model** | metadata column | `meta_data` (but uses `metadata` as column name with `metadata` reserved word conflict) |

**Issue:** Model uses reserved word `metadata` as column name.

**Files:**
- Migration: `add_progress_drafts_bookmarks_activity.py` line 94
- Model: `api/models/activity.py` line 56-60

```python
# Model has:
meta_data: Mapped[dict | None] = mapped_column(
    "metadata",  # Uses "metadata" as DB column name (reserved word!)
    JSONB,
    nullable=True,
)

# Migration creates:
sa.Column('meta_data', postgresql.JSONB(...), nullable=True)
```

**Impact:** Model maps to column `metadata` (reserved word), migration creates `meta_data`.

---

#### 4.4 User Model - Missing Column ⚠️ **MEDIUM**

| Source | Column | Status |
|--------|--------|--------|
| **Model** | `last_seen` | Present |
| **Migration** | `last_seen` | **MISSING** |

**File:** `api/models/user.py` line 47-52

```python
# Model has:
last_seen: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=datetime.utcnow,
    onupdate=datetime.utcnow,
    nullable=False,
)

# Migration missing this column entirely
```

**Impact:** Application may fail when accessing `user.last_seen`.

---

#### 4.5 Progress Model - Status Type Mismatch ⚠️ **LOW**

| Source | Column | Type |
|--------|--------|------|
| **Migration** | `status` | `sa.String(50)` |
| **Model** | `status` | `Enum(ProblemStatus)` |

**Issue:** Migration uses plain String for CockroachDB compatibility, model uses Python Enum.

**Note:** This may be intentional for CockroachDB compatibility, but verify data consistency.

---

#### 4.6 Activity Model - activity_type Type Mismatch ⚠️ **LOW**

| Source | Column | Type |
|--------|--------|------|
| **Migration** | `activity_type` | `sa.String(50)` |
| **Model** | `activity_type` | `ActivityType` enum mapped to String |

**Note:** Model uses `String(50)` storage, so this is acceptable.

---

### Summary of Model-Migration Issues

| Priority | Issue | Migration | Model | Fix Required |
|----------|-------|-----------|-------|--------------|
| 🔴 HIGH | Bookmark.id type | String(36) | Integer | **YES** |
| 🔴 HIGH | Bookmark.notes name | `notes` | `note` | **YES** |
| 🔴 HIGH | Activity.meta_data name | `meta_data` | `metadata` | **YES** |
| 🟡 MEDIUM | User.last_seen column | **MISSING** | Present | **YES** |
| 🟢 LOW | Progress.status type | String | Enum | Verify intent |
| 🟢 LOW | Activity.activity_type | String | Enum→String | Acceptable |

---

## 5. Foreign Key Dependency Analysis

### All Foreign Key Constraints

| Table | Column | References | On Delete | Migration | Status |
|-------|--------|------------|-----------|-----------|--------|
| `auth_tokens` | `user_id` | `users.id` | `CASCADE` | 1 | ✅ Valid |
| `progress` | `user_id` | `users.id` | `CASCADE` | 2 | ✅ Valid |
| `drafts` | `user_id` | `users.id` | `CASCADE` | 2 | ✅ Valid |
| `bookmarks` | `user_id` | `users.id` | `CASCADE` | 2 | ✅ Valid |
| `activities` | `user_id` | `users.id` | `CASCADE` | 2 | ✅ Valid |
| `submissions` | `user_id` | `users.id` | `CASCADE` | 3 | ✅ Valid |
| `submissions` | `reviewed_by` | `users.id` | `SET NULL` | 3 | ✅ Valid |
| `submission_comments` | `submission_id` | `submissions.id` | `CASCADE` | 3 | ✅ Valid |
| `submission_comments` | `user_id` | `users.id` | `CASCADE` | 3 | ✅ Valid |

**Result:** All foreign keys reference tables created in prior migrations. ✅

---

## 6. Index Analysis

### Duplicate/Redundant Indexes

| Table | Column | Migration 2 Index | Migration 4 Index | Issue |
|-------|--------|-------------------|-------------------|-------|
| `progress` | `user_id` + `problem_slug` | `uq_user_problem_progress` (unique) | `idx_progress_user_problem` | **Duplicate coverage** |
| `progress` | `status` | `ix_progress_status` | `idx_progress_status` | **DUPLICATE** |

**Issue:** Migration 4 creates `idx_progress_status` but Migration 2 already creates `ix_progress_status` on the same column.

### All Indexes by Table

| Table | Index Name | Columns | Migration | Type |
|-------|------------|---------|-----------|------|
| `users` | `ix_users_email` | `email` | 1 | Unique |
| `auth_tokens` | `ix_auth_tokens_token_hash` | `token_hash` | 1 | Index |
| `auth_tokens` | `ix_auth_tokens_user_id_created_at` | `user_id`, `created_at` | 1 | Index |
| `progress` | `ix_progress_user_id` | `user_id` | 2 | Index |
| `progress` | `ix_progress_problem_slug` | `problem_slug` | 2 | Index |
| `progress` | `ix_progress_week_slug` | `week_slug` | 2 | Index |
| `progress` | `ix_progress_day_slug` | `day_slug` | 2 | Index |
| `progress` | `ix_progress_status` | `status` | 2 | Index |
| `progress` | `uq_user_problem_progress` | `user_id`, `problem_slug` | 2 | Unique |
| `progress` | `idx_progress_user_problem` | `user_id`, `problem_slug` | 4 | **REDUNDANT** |
| `progress` | `idx_progress_status` | `status` | 4 | **DUPLICATE** |
| `drafts` | `ix_drafts_user_id` | `user_id` | 2 | Index |
| `drafts` | `ix_drafts_problem_slug` | `problem_slug` | 2 | Index |
| `drafts` | `uq_user_problem_draft` | `user_id`, `problem_slug` | 2 | Unique |
| `bookmarks` | `ix_bookmarks_user_id` | `user_id` | 2 | Index |
| `bookmarks` | `ix_bookmarks_item_slug` | `item_slug` | 2 | Index |
| `bookmarks` | `uq_user_bookmark` | `user_id`, `item_type`, `item_slug` | 2 | Unique |
| `bookmarks` | `idx_bookmarks_user_type` | `user_id`, `item_type` | 4 | Index |
| `activities` | `ix_activities_user_id` | `user_id` | 2 | Index |
| `activities` | `ix_activities_activity_type` | `activity_type` | 2 | Index |
| `activities` | `ix_activities_item_slug` | `item_slug` | 2 | Index |
| `activities` | `ix_activities_created_at` | `created_at` | 2 | Index |
| `activities` | `idx_activity_user_created` | `user_id`, `created_at` | 4 | Index |
| `submissions` | (inline) | `user_id` | 3 | Index |
| `submissions` | (inline) | `project_slug` | 3 | Index |
| `submissions` | (inline) | `week_slug` | 3 | Index |
| `submissions` | (inline) | `day_slug` | 3 | Index |
| `submissions` | (inline) | `status` | 3 | Index |
| `submission_comments` | (inline) | `submission_id` | 3 | Index |
| `submission_comments` | (inline) | `user_id` | 3 | Index |

---

## 7. Recommended Fixes

### Priority 1: Fix Critical Model-Migration Mismatches

#### Fix 1: Align Bookmark Model with Migration

**File:** `api/models/bookmark.py`

```python
# Change from:
id = Column(Integer, primary_key=True, index=True)
note = Column(Text, nullable=True)

# To:
id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid4()))
notes = Column(Text, nullable=True)  # Changed from 'note' to 'notes'
```

#### Fix 2: Align Activity Model with Migration

**File:** `api/models/activity.py`

```python
# Change from:
meta_data: Mapped[dict | None] = mapped_column(
    "metadata",  # Reserved word issue
    JSONB,
    nullable=True,
)

# To:
meta_data: Mapped[dict | None] = mapped_column(
    "meta_data",  # Match migration column name
    JSONB,
    nullable=True,
)
```

#### Fix 3: Add Missing Column to Migration

**File:** `migrations/versions/add_users_and_auth_tokens.py`

Add to `users` table creation:

```python
sa.Column('last_seen', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
```

Also update `downgrade()` to drop this column.

### Priority 2: Fix Duplicate Indexes

**File:** `migrations/versions/add_performance_indexes.py`

Remove duplicate index:

```python
# Remove this - already exists as ix_progress_status:
op.create_index(
    'idx_progress_status', 
    'progress', 
    ['status']
)
```

### Priority 3: Add Idempotency Checks (Optional)

For safer migrations, add existence checks:

```python
def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()
    
    if 'users' not in tables:
        op.create_table('users', ...)
```

---

## 8. Root Cause of "Relation Does Not Exist" Errors

The "relation does not exist" errors mentioned in the audit request were likely caused by:

1. **Missing `down_revision` links** (Already fixed - chain is now linear)
2. **Foreign key constraints referencing non-existent tables** (All FKs reference prior migrations)
3. **Migrations running out of order** (Chain is now correctly ordered)

**Current Status:** The migration chain itself is correct and should not cause "relation does not exist" errors if run sequentially from an empty database.

---

## 9. Verification Commands

To verify the migration chain after fixes:

```bash
# Check migration history
alembic history --verbose

# Check for multiple heads
alembic heads

# Check current revision
alembic current

# Dry-run upgrade
alembic upgrade head --sql

# Test upgrade on fresh database
alembic upgrade head
```

---

## 10. Summary

| Category | Status | Notes |
|----------|--------|-------|
| Migration Chain | ✅ **PASS** | Linear, no branches |
| Table Order | ✅ **PASS** | Dependencies satisfied |
| Foreign Keys | ✅ **PASS** | All reference prior tables |
| Idempotency | ⚠️ **WARNING** | No IF NOT EXISTS checks |
| Model Sync | ❌ **FAIL** | 3 critical mismatches |
| Duplicate Indexes | ⚠️ **WARNING** | 1 duplicate index |

### Action Items

1. [ ] Fix Bookmark model ID type (Integer → String)
2. [ ] Fix Bookmark model column name (note → notes)
3. [ ] Fix Activity model column name (metadata → meta_data)
4. [ ] Add last_seen column to users migration
5. [ ] Remove duplicate idx_progress_status index
6. [ ] Run full migration test on fresh database
7. [ ] Verify ORM operations work correctly

---

**End of Audit Report**
