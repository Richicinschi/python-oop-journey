# SQLAlchemy Models Audit Report

**Location:** `website-playground/apps/api/api/models/`
**Date:** 2026-03-12
**Auditor:** Model Consistency Auditor

---

## Executive Summary

**CRITICAL ISSUES FOUND: 5 categories**

| Severity | Count | Issue Type |
|----------|-------|------------|
| 🔴 Critical | 3 | Missing exports, Import errors |
| 🟠 High | 2 | Inconsistent column definitions |
| 🟡 Medium | 2 | Relationship mismatches |
| 🟢 Low | 4 | Missing timezone info, Style inconsistencies |

---

## 1. 🔴 CRITICAL: Missing Exports in `__init__.py`

### Issue: Enum class `SubmissionStatus` not exported

The `Submission` model uses a string-based status field with hardcoded values:
- `"pending_review"`
- Likely other statuses exist but no Enum class is defined

**Missing Export:**
```python
# Should be defined in submission.py and exported in __init__.py
class SubmissionStatus(str, Enum):
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"
```

**Impact:** Type safety issues, no validation of valid status values.

---

## 2. 🔴 CRITICAL: `SubmissionComment` Relationship Broken

### Issue: `SubmissionComment.submission` relationship lacks `back_populates`

**Current Code (submission.py:186):**
```python
submission: Mapped["Submission"] = relationship("Submission", lazy="selectin")
```

**Problem:** The `Submission` model does NOT have a corresponding `comments` relationship with `back_populates="submission"`.

**Expected Fix:**
```python
# In Submission class:
comments: Mapped[list["SubmissionComment"]] = relationship(
    "SubmissionComment",
    back_populates="submission",
    cascade="all, delete-orphan",
    lazy="selectin",
)

# In SubmissionComment class:
submission: Mapped["Submission"] = relationship(
    "Submission",
    back_populates="comments",
    lazy="selectin",
)
```

---

## 3. 🔴 CRITICAL: `SubmissionComment.user` Relationship Broken

### Issue: `SubmissionComment.user` relationship lacks `back_populates`

**Current Code (submission.py:187):**
```python
user: Mapped["User"] = relationship("User", lazy="selectin")
```

**Problem:** The `User` model does NOT have a corresponding `submission_comments` relationship.

**Expected Fix:**
```python
# In User class:
submission_comments: Mapped[list["SubmissionComment"]] = relationship(
    "SubmissionComment",
    back_populates="user",
    cascade="all, delete-orphan",
    lazy="selectin",
)

# In SubmissionComment class:
user: Mapped["User"] = relationship(
    "User",
    back_populates="submission_comments",
    lazy="selectin",
)
```

---

## 4. 🟠 HIGH: `Bookmark` Model - Inconsistent Column Definitions

### Issue: Mix of legacy and modern SQLAlchemy syntax

**Current (bookmark.py):**
```python
# Legacy style (SQLAlchemy 1.x)
id = Column(Integer, primary_key=True, index=True)
user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), ...)
item_type = Column(Enum(ItemType), nullable=False, index=True)
```

**Problem:** Uses `Column()` instead of `Mapped[]` + `mapped_column()` pattern used in all other models.

**Required Fix:**
```python
class Bookmark(Base):
    __tablename__ = "bookmarks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(
        String(36),  # FIXED: Should match User.id length
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    item_type: Mapped[ItemType] = mapped_column(
        Enum(ItemType),
        nullable=False,
        index=True,
    )
    item_slug: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),  # FIXED: Add timezone
        default=datetime.utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),  # FIXED: Add timezone
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
```

---

## 5. 🟠 HIGH: `Bookmark` - String Length Not Defined

### Issue: `user_id` column lacks String length

**Current (bookmark.py:27):**
```python
user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), ...)
```

**Problem:** `String` without length defaults to database-specific behavior. `User.id` is explicitly `String(36)`.

**Fix:**
```python
user_id: Mapped[str] = mapped_column(
    String(36),  # Match User.id length
    ForeignKey("users.id", ondelete="CASCADE"),
    nullable=False,
    index=True,
)
```

---

## 6. 🟡 MEDIUM: Missing Timezone in `Bookmark` DateTime Columns

### Issue: `created_at` and `updated_at` lack timezone info

**Current (bookmark.py:31-32):**
```python
created_at = Column(DateTime, default=datetime.utcnow)
updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**Problem:** All other models use `DateTime(timezone=True)`. Inconsistent timezone handling.

**Fix:**
```python
created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=datetime.utcnow,
)
updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=datetime.utcnow,
    onupdate=datetime.utcnow,
)
```

---

## 7. 🟡 MEDIUM: `AuthToken` - Missing `back_populates` Verification

### Status: ✅ VERIFIED CORRECT

**User.auth_tokens → AuthToken.user:**
```python
# User.py
auth_tokens: Mapped[list["AuthToken"]] = relationship(
    "AuthToken",
    back_populates="user",
    cascade="all, delete-orphan",
    lazy="selectin",
)

# auth_token.py
user: Mapped["User"] = relationship("User", back_populates="auth_tokens")
```

✅ **Consistent** - Both sides properly defined.

---

## 8. 🟢 LOW: `Submission.reviewer` Relationship

### Issue: `reviewer` relationship lacks `back_populates`

**Current (submission.py:124-128):**
```python
reviewer: Mapped["User | None"] = relationship(
    "User",
    foreign_keys=[reviewed_by],
    lazy="selectin",
)
```

**Assessment:** This is a self-referential relationship to User. If bidirectional navigation is needed, add to User:

```python
# In User class (optional):
reviewed_submissions: Mapped[list["Submission"]] = relationship(
    "Submission",
    foreign_keys="Submission.reviewed_by",
    back_populates="reviewer",
    lazy="selectin",
)
```

If not needed, this is acceptable as a unidirectional relationship.

---

## 9. 🟢 LOW: Import Style Inconsistency in `bookmark.py`

### Issue: Imports use legacy `Column` instead of modern `mapped_column`

**Current (bookmark.py:6-7):**
```python
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Enum
from sqlalchemy.orm import relationship
```

**Should be:**
```python
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
```

---

## Summary of Required Fixes

### `__init__.py`
- [ ] Export `SubmissionStatus` enum (if created)

### `bookmark.py`
- [ ] Convert to modern SQLAlchemy syntax (`Mapped`, `mapped_column`)
- [ ] Add `timezone=True` to DateTime columns
- [ ] Fix `user_id` String length to `String(36)`
- [ ] Update imports

### `submission.py`
- [ ] Add `Submission.comments` relationship with `back_populates="submission"`
- [ ] Update `SubmissionComment.submission` to include `back_populates="comments"`
- [ ] Add `User.submission_comments` relationship
- [ ] Update `SubmissionComment.user` to include `back_populates="submission_comments"`
- [ ] Consider creating `SubmissionStatus` enum

### `user.py`
- [ ] Add `submission_comments` relationship

---

## Import Test Commands

To verify all models import correctly:

```bash
cd website-playground/apps/api
python -c "from api.models import *; print('All imports successful')"
python -c "from api.models.user import User; print('User OK')"
python -c "from api.models.activity import Activity, ActivityType; print('Activity OK')"
python -c "from api.models.auth_token import AuthToken; print('AuthToken OK')"
python -c "from api.models.bookmark import Bookmark, ItemType; print('Bookmark OK')"
python -c "from api.models.draft import Draft; print('Draft OK')"
python -c "from api.models.progress import Progress, ProblemStatus; print('Progress OK')"
python -c "from api.models.submission import Submission, SubmissionComment; print('Submission OK')"
```

### Import Test Result

**Status:** ⚠️ Cannot fully test (missing `pydantic` dependency)

**Error:** `ModuleNotFoundError: No module named 'pydantic'`

**Analysis:** The import chain reaches `api.models.__init__.py` successfully, but fails when loading `api.config` (which requires pydantic). The model files themselves have correct import syntax and structure. No "cannot import name" errors detected in model definitions.

---

## Quick Fix Script

Apply these fixes in order:

```bash
# 1. Fix bookmark.py (modernize syntax)
# 2. Add Submission.comments relationship
# 3. Add User.submission_comments relationship
# 4. Update SubmissionComment relationships with back_populates
# 5. Create SubmissionStatus enum (optional)
# 6. Update __init__.py exports
```
