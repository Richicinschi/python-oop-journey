"""Add progress, drafts, bookmarks, and activity tables

Revision ID: add_progress_drafts_bookmarks_activity
Revises: add_users_and_auth_tokens
Create Date: 2026-03-13 01:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = '002_add_progress'
down_revision: Union[str, None] = '001_add_users'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def table_exists(table_name: str) -> bool:
    """Check if a table already exists."""
    bind = op.get_bind()
    inspector = inspect(bind)
    return table_name in inspector.get_table_names()


def index_exists(table_name: str, index_name: str) -> bool:
    """Check if an index already exists."""
    bind = op.get_bind()
    inspector = inspect(bind)
    indexes = [idx['name'] for idx in inspector.get_indexes(table_name)]
    return index_name in indexes


def upgrade() -> None:
    # Create progress table (if not exists)
    if not table_exists('progress'):
        op.create_table(
            'progress',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('user_id', sa.String(36), nullable=False),
            sa.Column('problem_slug', sa.String(100), nullable=False),
            sa.Column('week_slug', sa.String(100), nullable=True),
            sa.Column('day_slug', sa.String(100), nullable=True),
            sa.Column('status', sa.String(50), nullable=False, server_default='NOT_STARTED'),
            sa.Column('attempts_count', sa.Integer, nullable=False, server_default='0'),
            sa.Column('solved_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('first_attempted_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('last_attempted_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('time_spent_seconds', sa.Integer, nullable=False, server_default='0'),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
            sa.UniqueConstraint('user_id', 'problem_slug', name='uq_user_problem_progress'),
        )
        
        # Create indexes for progress
        op.create_index('ix_progress_user_id', 'progress', ['user_id'])
        op.create_index('ix_progress_problem_slug', 'progress', ['problem_slug'])
        op.create_index('ix_progress_week_slug', 'progress', ['week_slug'])
        op.create_index('ix_progress_day_slug', 'progress', ['day_slug'])
        op.create_index('ix_progress_status', 'progress', ['status'])
    
    # Create drafts table (if not exists)
    if not table_exists('drafts'):
        op.create_table(
            'drafts',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('user_id', sa.String(36), nullable=False),
            sa.Column('problem_slug', sa.String(100), nullable=False),
            sa.Column('code', sa.Text, nullable=False, server_default=''),
            sa.Column('saved_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column('is_auto_save', sa.Boolean, nullable=False, server_default='false'),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
            sa.UniqueConstraint('user_id', 'problem_slug', name='uq_user_problem_draft'),
        )
        
        # Create indexes for drafts
        op.create_index('ix_drafts_user_id', 'drafts', ['user_id'])
        op.create_index('ix_drafts_problem_slug', 'drafts', ['problem_slug'])
    
    # Create bookmarks table (if not exists)
    if not table_exists('bookmarks'):
        op.create_table(
            'bookmarks',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('user_id', sa.String(36), nullable=False),
            sa.Column('item_type', sa.String(50), nullable=False),
            sa.Column('item_slug', sa.String(100), nullable=False),
            sa.Column('notes', sa.Text, nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
            sa.UniqueConstraint('user_id', 'item_type', 'item_slug', name='uq_user_bookmark'),
        )
        
        # Create indexes for bookmarks
        op.create_index('ix_bookmarks_user_id', 'bookmarks', ['user_id'])
        op.create_index('ix_bookmarks_item_slug', 'bookmarks', ['item_slug'])
    
    # Create activities table (if not exists)
    if not table_exists('activities'):
        op.create_table(
            'activities',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('user_id', sa.String(36), nullable=False),
            sa.Column('activity_type', sa.String(50), nullable=False),
            sa.Column('item_slug', sa.String(100), nullable=True),
            sa.Column('meta_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        )
        
        # Create indexes for activities
        op.create_index('ix_activities_user_id', 'activities', ['user_id'])
        op.create_index('ix_activities_activity_type', 'activities', ['activity_type'])
        op.create_index('ix_activities_item_slug', 'activities', ['item_slug'])
        op.create_index('ix_activities_created_at', 'activities', ['created_at'])


def downgrade() -> None:
    # Drop tables in reverse order (only if they exist)
    if table_exists('activities'):
        op.drop_index('ix_activities_created_at', table_name='activities')
        op.drop_index('ix_activities_item_slug', table_name='activities')
        op.drop_index('ix_activities_activity_type', table_name='activities')
        op.drop_index('ix_activities_user_id', table_name='activities')
        op.drop_table('activities')
    
    if table_exists('bookmarks'):
        op.drop_index('ix_bookmarks_item_slug', table_name='bookmarks')
        op.drop_index('ix_bookmarks_user_id', table_name='bookmarks')
        op.drop_table('bookmarks')
    
    if table_exists('drafts'):
        op.drop_index('ix_drafts_problem_slug', table_name='drafts')
        op.drop_index('ix_drafts_user_id', table_name='drafts')
        op.drop_table('drafts')
    
    if table_exists('progress'):
        op.drop_index('ix_progress_status', table_name='progress')
        op.drop_index('ix_progress_day_slug', table_name='progress')
        op.drop_index('ix_progress_week_slug', table_name='progress')
        op.drop_index('ix_progress_problem_slug', table_name='progress')
        op.drop_index('ix_progress_user_id', table_name='progress')
        op.drop_table('progress')
