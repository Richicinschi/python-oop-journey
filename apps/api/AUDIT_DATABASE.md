# CockroachDB Compatibility Audit Report

**Audit Date:** 2026-03-12  
**Auditor:** Database Compatibility Auditor  
**Scope:** `website-playground/apps/api` - Models and Migrations  
**Target Database:** CockroachDB (PostgreSQL-compatible)

---

## Executive Summary

This audit identified **5 CRITICAL** and **3 HIGH** priority issues that will cause deployment failures on CockroachDB. The primary issues stem from:

1. SQLAlchemy `Enum` types (not supported by CockroachDB's `CREATE TYPE`)
2. PostgreSQL-specific `JSONB` dialect usage
3. Reserved word column names (`metadata`)
4. Model/migration column name mismatches

---

## CRITICAL Issues (Will Cause Deployment Failure)

### 1. Enum Usage in Models (CockroachDB Doesn't Support CREATE TYPE)

#### Issue 1.1: `bookmark.py` - Enum Column
**File:** `api/models/bookmark.py`  
**Line:** 28  
**Priority:** CRITICAL

```python
# PROBLEMATIC CODE (Line 28):
item_type = Column(Enum(ItemType), nullable=False, index=True)
```

**Problem:** Uses SQLAlchemy's `Enum` type which generates `CREATE TYPE` statements. CockroachDB doesn't support user-defined types.

**Migration Status:** The migration file correctly uses `String(50)` instead of Enum, but the **model is out of sync** with the migration.

**Suggested Fix:**
```python
# Change from:
item_type = Column(Enum(ItemType), nullable=False, index=True)

# To:
item_type = Column(String(50), nullable=False, index=True)
```

---

#### Issue 1.2: `progress.py` - Enum Column
**File:** `api/models/progress.py`  
**Line:** 56-60  
**Priority:** CRITICAL

```python
# PROBLEMATIC CODE (Lines 56-60):
status: Mapped[ProblemStatus] = mapped_column(
    Enum(ProblemStatus),
    default=ProblemStatus.NOT_STARTED,
    nullable=False,
    index=True,
)
```

**Problem:** Same Enum issue as above. Migration uses `String(50)` but model declares `Enum(ProblemStatus)`.

**Suggested Fix:**
```python
# Change from:
status: Mapped[ProblemStatus] = mapped_column(
    Enum(ProblemStatus),
    default=ProblemStatus.NOT_STARTED,
    nullable=False,
    index=True,
)

# To:
status: Mapped[str] = mapped_column(
    String(50),
    default=ProblemStatus.NOT_STARTED.value,
    nullable=False,
    index=True,
)
```

---

### 2. Reserved Word Column Names

#### Issue 2.1: `activity.py` - `metadata` Column Name
**File:** `api/models/activity.py`  
**Line:** 56-60  
**Priority:** CRITICAL

```python
# PROBLEMATIC CODE (Lines 56-60):
meta_data: Mapped[dict | None] = mapped_column(
    "metadata",  # <-- Reserved word!
    JSONB,
    nullable=True,
)
```

**Problem:** The column is aliased as `"metadata"` in the database, which is a **SQL reserved word**. This can cause syntax errors in queries.

**Migration Status:** The migration uses `meta_data` (line 94 in migration), which is correct. The model is out of sync.

**Suggested Fix:**
```python
# Change from:
meta_data: Mapped[dict | None] = mapped_column(
    "metadata",
    JSONB,
    nullable=True,
)

# To:
meta_data: Mapped[dict | None] = mapped_column(
    JSONB,
    nullable=True,
)
# OR explicitly name it:
meta_data: Mapped[dict | None] = mapped_column(
    "meta_data",  # Consistent with migration
    JSONB,
    nullable=True,
)
```

---

### 3. PostgreSQL-Specific JSONB Usage

#### Issue 3.1: Migration Uses `postgresql.JSONB`
**File:** `migrations/versions/add_progress_drafts_bookmarks_activity.py`  
**Line:** 94  
**Priority:** CRITICAL

```python
# PROBLEMATIC CODE (Line 94):
sa.Column('meta_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
```

**Problem:** Uses PostgreSQL-specific dialect type. While CockroachDB supports JSONB, the `astext_type=sa.Text()` parameter and `postgresql` dialect import may cause issues.

**Model Status:** Model also imports from `postgresql` dialect (line 8 in activity.py).

**Suggested Fix:**
```python
# Change from:
from sqlalchemy.dialects.postgresql import JSONB
# ...
sa.Column('meta_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),

# To:
from sqlalchemy import JSON  # Generic JSON type
# ...
sa.Column('meta_data', JSON, nullable=True),  # Generic type works on both
```

**Note:** If JSONB-specific features (like indexing) are needed, keep JSONB but test thoroughly on CockroachDB.

---

## HIGH Priority Issues (May Cause Runtime Errors)

### 4. Model/Migration Column Name Mismatch

#### Issue 4.1: `bookmarks` - `note` vs `notes`
**File:** `api/models/bookmark.py` (Line 30) vs Migration (Line 76)  
**Priority:** HIGH

```python
# MODEL (bookmark.py, Line 30):
note = Column(Text, nullable=True)  # Singular

# MIGRATION (add_progress_drafts_bookmarks_activity.py, Line 76):
sa.Column('notes', sa.Text, nullable=True),  # Plural!
```

**Problem:** Model expects column `note` but migration creates `notes`. This will cause runtime errors when accessing the attribute.

**Suggested Fix:** Align both to use the same name:
```python
# Option 1: Change model to match migration
notes = Column(Text, nullable=True)

# Option 2: Change migration to match model (safer - won't break existing DB)
sa.Column('note', sa.Text, nullable=True),
```

---

#### Issue 4.2: `activities` - `meta_data` Model vs Migration Column Name
**File:** `api/models/activity.py` vs Migration (Line 94)  
**Priority:** HIGH

```python
# MODEL (activity.py):
meta_data: Mapped[dict | None] = mapped_column(
    "metadata",  # DB column named "metadata"
    JSONB,
    nullable=True,
)

# MIGRATION (Line 94):
sa.Column('meta_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),  # Named "meta_data"
```

**Problem:** Model writes to `"metadata"` column, migration creates `"meta_data"` column.

**Suggested Fix:** Use consistent naming throughout (recommend `meta_data`):
```python
# In model:
meta_data: Mapped[dict | None] = mapped_column(
    "meta_data",  # Match migration
    JSONB,
    nullable=True,
)
```

---

### 5. String Length Mismatch Between Model and Migration

#### Issue 5.1: Primary Key and Foreign Key String Lengths
**Files:** Multiple model files vs migrations  
**Priority:** HIGH

**Inconsistencies Found:**

| Table | Model | Migration | Status |
|-------|-------|-----------|--------|
| `bookmarks.id` | `Integer` | `String(36)` | **MISMATCH** |
| `bookmarks.user_id` | `String` (no length) | `String(36)` | Potential mismatch |

**Specific Code:**

```python
# MODEL (bookmark.py, Lines 26-27):
id = Column(Integer, primary_key=True, index=True)  # INTEGER!
user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), ...)  # No length

# MIGRATION (Lines 72-73):
sa.Column('id', sa.String(36), nullable=False),  # STRING!
sa.Column('user_id', sa.String(36), nullable=False),
```

**Problem:** Model uses `Integer` for `id`, migration uses `String(36)`. This is a fundamental type mismatch.

**Suggested Fix:**
```python
# Change model to match migration:
id: Mapped[str] = mapped_column(
    String(36),
    primary_key=True,
    default=lambda: str(uuid4()),  # Add uuid import
    index=True,
)
user_id: Mapped[str] = mapped_column(
    String(36),
    ForeignKey("users.id", ondelete="CASCADE"),
    nullable=False,
    index=True,
)
```

---

## MEDIUM Priority Issues (Best Practice)

### 6. Boolean Default Values Inconsistent

#### Issue 6.1: Boolean Defaults in Migrations vs Models
**Priority:** MEDIUM

The migration uses `server_default='true'` while models use Python `default=True`. This is generally fine but can cause subtle issues.

**Example from migration:**
```python
sa.Column('is_auto_save', sa.Boolean, nullable=False, server_default='false'),
```

**Recommended:** Ensure consistency between model defaults and database defaults.

---

### 7. Foreign Key Constraint Verification

**Status:** ✅ **ALL FOREIGN KEYS VERIFIED** - No issues found.

All foreign key constraints properly reference existing tables:

| Table | Foreign Key | References | On Delete | Status |
|-------|-------------|------------|-----------|--------|
| `auth_tokens` | `user_id` | `users.id` | CASCADE | ✅ Valid |
| `progress` | `user_id` | `users.id` | CASCADE | ✅ Valid |
| `drafts` | `user_id` | `users.id` | CASCADE | ✅ Valid |
| `bookmarks` | `user_id` | `users.id` | CASCADE | ✅ Valid |
| `activities` | `user_id` | `users.id` | CASCADE | ✅ Valid |
| `submissions` | `user_id` | `users.id` | CASCADE | ✅ Valid |
| `submissions` | `reviewed_by` | `users.id` | SET NULL | ✅ Valid |
| `submission_comments` | `submission_id` | `submissions.id` | CASCADE | ✅ Valid |
| `submission_comments` | `user_id` | `users.id` | CASCADE | ✅ Valid |

---

## LOW Priority Issues (Observations)

### 8. CockroachDB Version Patching

**File:** `api/database.py`  
**Lines:** 17-34  
**Status:** ✅ Already patched

The database module includes monkey-patching for CockroachDB version compatibility. This is correctly implemented.

```python
# Lines 17-34 in database.py - Already handles CockroachDB version strings
def _patched_get_server_version_info(self, connection):
    ...
```

---

## Summary of Issues by Priority

| Priority | Count | Issues |
|----------|-------|--------|
| **CRITICAL** | 4 | Enum in bookmark.py, Enum in progress.py, metadata reserved word, postgresql.JSONB |
| **HIGH** | 3 | note/notes mismatch, meta_data naming, String/Integer type mismatch |
| **MEDIUM** | 1 | Boolean defaults |
| **LOW** | 0 | None |
| **PASS** | 2 | Foreign keys, CockroachDB patching |

---

## Quick Fix Checklist

To make the codebase CockroachDB-compatible, apply these changes in order:

### Step 1: Fix CRITICAL Enum Issues
1. [ ] `api/models/bookmark.py` line 28: Change `Enum(ItemType)` to `String(50)`
2. [ ] `api/models/progress.py` lines 56-60: Change `Enum(ProblemStatus)` to `String(50)`

### Step 2: Fix Reserved Word Issues
3. [ ] `api/models/activity.py` lines 56-60: Remove `"metadata"` alias or change to `"meta_data"`

### Step 3: Fix PostgreSQL-Specific Types
4. [ ] `migrations/versions/add_progress_drafts_bookmarks_activity.py` line 94: Change `postgresql.JSONB` to generic `JSON`
5. [ ] `api/models/activity.py` line 8: Change import from `postgresql.JSONB` to `JSON`

### Step 4: Fix Model/Migration Mismatches
6. [ ] `api/models/bookmark.py` line 30: Change `note` to `notes` (or update migration)
7. [ ] `api/models/bookmark.py` lines 26-27: Change `id` from `Integer` to `String(36)`
8. [ ] `api/models/bookmark.py` line 27: Change `String` to `String(36)` for user_id

### Step 5: Verify and Test
9. [ ] Run `alembic upgrade head` on a test CockroachDB instance
10. [ ] Verify all tables created successfully
11. [ ] Run application smoke tests

---

## Migration Files Status

| Migration File | Status | Notes |
|----------------|--------|-------|
| `add_users_and_auth_tokens.py` | ✅ Compatible | Uses String types correctly |
| `add_progress_drafts_bookmarks_activity.py` | ⚠️ Needs Fix | Uses `postgresql.JSONB` |
| `add_submissions.py` | ✅ Compatible | Uses generic JSON type |
| `add_performance_indexes.py` | ✅ Compatible | Only creates indexes |

---

## Appendix: Files Audited

### Models (8 files)
- `api/models/__init__.py`
- `api/models/activity.py`
- `api/models/auth_token.py`
- `api/models/bookmark.py`
- `api/models/draft.py`
- `api/models/progress.py`
- `api/models/submission.py`
- `api/models/user.py`

### Migrations (4 files)
- `migrations/versions/add_users_and_auth_tokens.py`
- `migrations/versions/add_progress_drafts_bookmarks_activity.py`
- `migrations/versions/add_submissions.py`
- `migrations/versions/add_performance_indexes.py`

### Database Configuration (1 file)
- `api/database.py`

---

*End of Audit Report*
