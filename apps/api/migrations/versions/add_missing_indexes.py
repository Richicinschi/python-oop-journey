"""Add missing database indexes for performance optimization.

Revision ID: add_missing_indexes
Revises: fix_schema_mismatches
Create Date: 2026-03-15
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = 'add_missing_indexes'
down_revision: Union[str, None] = 'fix_schema_mismatches'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def index_exists(table_name: str, index_name: str) -> bool:
    """Check if an index already exists."""
    bind = op.get_bind()
    inspector = inspect(bind)
    try:
        indexes = [idx['name'] for idx in inspector.get_indexes(table_name)]
        return index_name in indexes
    except Exception:
        return False


def upgrade() -> None:
    """Add missing indexes for optimized query performance."""
    
    # Progress table: unique index for user+problem lookup
    if not index_exists('progress', 'idx_progress_user_problem'):
        op.create_index(
            'idx_progress_user_problem', 
            'progress', 
            ['user_id', 'problem_slug'],
            unique=True
        )
    
    # Progress table: composite index for week/day filtering
    if not index_exists('progress', 'idx_progress_week_day'):
        op.create_index(
            'idx_progress_week_day', 
            'progress', 
            ['week_slug', 'day_slug']
        )
    
    # Progress table: composite index for user+status filtering
    if not index_exists('progress', 'idx_progress_user_status'):
        op.create_index(
            'idx_progress_user_status', 
            'progress', 
            ['user_id', 'status']
        )
    
    # Activity table: composite index for user+created_at sorting
    if not index_exists('activities', 'idx_activity_user_created'):
        op.create_index(
            'idx_activity_user_created', 
            'activities', 
            ['user_id', 'created_at']
        )
    
    # Activity table: composite index for user+activity_type filtering
    if not index_exists('activities', 'idx_activity_user_type'):
        op.create_index(
            'idx_activity_user_type', 
            'activities', 
            ['user_id', 'activity_type']
        )


def downgrade() -> None:
    """Remove the added indexes."""
    
    if index_exists('activities', 'idx_activity_user_type'):
        op.drop_index('idx_activity_user_type', table_name='activities')
    
    if index_exists('activities', 'idx_activity_user_created'):
        op.drop_index('idx_activity_user_created', table_name='activities')
    
    if index_exists('progress', 'idx_progress_user_status'):
        op.drop_index('idx_progress_user_status', table_name='progress')
    
    if index_exists('progress', 'idx_progress_week_day'):
        op.drop_index('idx_progress_week_day', table_name='progress')
    
    if index_exists('progress', 'idx_progress_user_problem'):
        op.drop_index('idx_progress_user_problem', table_name='progress')
