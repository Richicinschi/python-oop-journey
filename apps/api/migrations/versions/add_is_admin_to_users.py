"""Add is_admin column to users table

Revision ID: add_is_admin_to_users
Revises: fix_schema_mismatches
Create Date: 2026-03-15

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = 'add_is_admin_to_users'
down_revision: Union[str, None] = 'fix_schema_mismatches'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def column_exists(table_name: str, column_name: str) -> bool:
    """Check if a column already exists in a table."""
    bind = op.get_bind()
    inspector = inspect(bind)
    try:
        columns = [col['name'] for col in inspector.get_columns(table_name)]
        return column_name in columns
    except Exception:
        return False


def upgrade() -> None:
    """Add is_admin column to users table."""
    if not column_exists('users', 'is_admin'):
        op.add_column(
            'users',
            sa.Column('is_admin', sa.Boolean(), nullable=False, server_default='false')
        )
        print("Added column: users.is_admin")
    else:
        print("Column already exists: users.is_admin")


def downgrade() -> None:
    """Remove is_admin column from users table."""
    if column_exists('users', 'is_admin'):
        op.drop_column('users', 'is_admin')
        print("Dropped column: users.is_admin")
    else:
        print("Column does not exist: users.is_admin")
