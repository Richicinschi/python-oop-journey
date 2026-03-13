"""Add performance indexes for frequently queried fields.

Revision ID: add_performance_indexes
Revises: add_submissions
Create Date: 2026-03-12
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'add_performance_indexes'
down_revision: Union[str, None] = 'add_submissions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add performance indexes for frequently queried fields."""
    
    # Progress table indexes
    op.create_index(
        'idx_progress_user_problem', 
        'progress', 
        ['user_id', 'problem_slug']
    )
    op.create_index(
        'idx_progress_status', 
        'progress', 
        ['status']
    )
    
    # Activity table indexes
    op.create_index(
        'idx_activity_user_created', 
        'activities', 
        ['user_id', 'created_at']
    )
    
    # Bookmark table indexes
    op.create_index(
        'idx_bookmarks_user_type', 
        'bookmarks', 
        ['user_id', 'item_type']
    )


def downgrade() -> None:
    """Remove performance indexes."""
    op.drop_index('idx_bookmarks_user_type', table_name='bookmarks')
    op.drop_index('idx_activity_user_created', table_name='activities')
    op.drop_index('idx_progress_status', table_name='progress')
    op.drop_index('idx_progress_user_problem', table_name='progress')
