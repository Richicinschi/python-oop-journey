# Alembic Migration Guide

## Overview

Alembic is our database migration tool for SQLAlchemy. It tracks database schema changes.

## Migration Chain

Current order:
```
1. add_users_and_auth_tokens
       ↓
2. add_progress_drafts_bookmarks_activity
       ↓
3. add_submissions
       ↓
4. add_performance_indexes
```

## Key Concepts

### Revision ID
Unique identifier for each migration (e.g., `add_users_and_auth_tokens`)

### down_revision
Points to the previous migration. First migration has `None`.

### upgrade()
Commands to apply the migration (create tables, add columns, etc.)

### downgrade()
Commands to reverse the migration (drop tables, remove columns)

## Creating a New Migration

```bash
cd apps/api

# Auto-generate from model changes
alembic revision --autogenerate -m "Add new table"

# Create empty migration
alembic revision -m "Manual migration"
```

## Running Migrations

```bash
# Upgrade to latest
alembic upgrade head

# Upgrade one step
alembic upgrade +1

# Downgrade one step
alembic downgrade -1

# Downgrade to beginning
alembic downgrade base

# Check current version
alembic current

# View history
alembic history
```

## Common Operations

### Create Table
```python
def upgrade():
    op.create_table(
        'my_table',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

def downgrade():
    op.drop_table('my_table')
```

### Add Column
```python
def upgrade():
    op.add_column('users', sa.Column('avatar', sa.String(255), nullable=True))

def downgrade():
    op.drop_column('users', 'avatar')
```

### Create Index
```python
def upgrade():
    op.create_index('idx_name', 'users', ['name'])

def downgrade():
    op.drop_index('idx_name', table_name='users')
```

### Add Foreign Key
```python
def upgrade():
    op.create_foreign_key(
        'fk_user_profile',
        'profiles', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )
```

## Common Errors

### "Multiple head revisions"
**Cause:** Two migrations have same `down_revision`

**Fix:** Update `down_revision` to create linear chain

### "relation 'X' does not exist"
**Cause:** Creating table B that references table A, but A doesn't exist yet

**Fix:** Ensure table A is created in earlier migration

### "Cannot add foreign key"
**Cause:** Referenced table/column doesn't exist

**Fix:** Create referenced table first

## Best Practices

1. **Always test migrations locally first**
2. **Keep migrations linear** - Avoid branches
3. **Make migrations reversible** - Always write `downgrade()`
4. **Don't modify existing migrations** - Create new ones instead
5. **Check model imports** - All models must be imported in `env.py`
6. **Use explicit column types** - Don't rely on defaults

## Migration Template

```python
"""Description

Revision ID: unique_name
Revises: previous_migration
Create Date: YYYY-MM-DD HH:MM:SS

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'unique_name'
down_revision: Union[str, None] = 'previous_migration'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
```
