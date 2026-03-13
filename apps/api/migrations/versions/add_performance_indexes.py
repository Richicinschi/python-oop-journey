"""Add performance indexes for frequently queried fields.

Revision ID: add_performance_indexes
Revises: add_submissions
Create Date: 2026-03-12
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = 'add_performance_indexes'
down_revision: Union[str, None] = 'add_submissions'
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
    """Add performance indexes for frequently queried fields."""
    
    # Progress table indexes
    if not index_exists('progress', 'idx_progress_user_problem'):
        op.create_index(
            'idx_progress_user_problem', 
            'progress', 
            ['user_id', 'problem_slug']
        )
    if not index_exists('progress', 'idx_progress_status'):
        op.create_index(
            'idx_progress_status', 
            'progress', 
            ['status']
        )
    
    # Activity table indexes
    if not index_exists('activities', 'idx_activity_user_created'):
        op.create_index(
            'idx_activity_user_created', 
            'activities', 
            ['user_id', 'created_at']
        )
    
    # Bookmark table indexes
    if not index_exists('bookmarks', 'idx_bookmarks_user_type'):
        op.create_index(
            'idx_bookmarks_user_type', 
            'bookmarks', 
            ['user_id', 'item_type']
        )


def downgrade() -> None:
    """Remove performance indexes."""
    if index_exists('bookmarks', 'idx_bookmarks_user_type'):
        op.drop_index('idx_bookmarks_user_type', table_name='bookmarks')
    if index_exists('activities', 'idx_activity_user_created'):
        op.drop_index('idx_activity_user_created', table_name='activities')
    if index_exists('progress', 'idx_progress_status'):
        op.drop_index('idx_progress_status', table_name='progress')
    if index_exists('progress', 'idx_progress_user_problem'):
        op.drop_index('idx_progress_user_problem', table_name='progress')
