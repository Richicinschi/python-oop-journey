"""Add progress, drafts, bookmarks, and activity tables

Revision ID: add_progress_drafts_bookmarks_activity
Revises: add_users_and_auth_tokens
Create Date: 2026-03-13 01:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'add_progress_drafts_bookmarks_activity'
down_revision: Union[str, None] = 'add_users_and_auth_tokens'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum types if they don't exist (idempotent)
    op.execute("DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'problemstatus') THEN CREATE TYPE problemstatus AS ENUM ('NOT_STARTED', 'IN_PROGRESS', 'SOLVED', 'NEEDS_REVIEW'); END IF; END $$;")
    op.execute("DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'itemtype') THEN CREATE TYPE itemtype AS ENUM ('PROBLEM', 'DAY', 'WEEK', 'THEORY'); END IF; END $$;")
    op.execute("DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'activitytype') THEN CREATE TYPE activitytype AS ENUM ('STARTED_PROBLEM', 'SOLVED_PROBLEM', 'ATTEMPTED_PROBLEM', 'VIEWED_THEORY', 'VIEWED_WEEK', 'VIEWED_DAY', 'SAVED_DRAFT', 'CREATED_BOOKMARK', 'DELETED_BOOKMARK', 'LOGIN', 'LOGOUT'); END IF; END $$;")
    
    # Create progress table
    op.create_table(
        'progress',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('problem_slug', sa.String(100), nullable=False),
        sa.Column('week_slug', sa.String(100), nullable=True),
        sa.Column('day_slug', sa.String(100), nullable=True),
        sa.Column('status', sa.Enum('NOT_STARTED', 'IN_PROGRESS', 'SOLVED', 'NEEDS_REVIEW', name='problemstatus'), nullable=False),
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
    
    # Create drafts table
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
    
    # Create bookmarks table
    op.create_table(
        'bookmarks',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('item_type', sa.Enum('PROBLEM', 'DAY', 'WEEK', 'THEORY', name='itemtype'), nullable=False),
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
    
    # Create activities table
    op.create_table(
        'activities',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('activity_type', sa.Enum(
            'STARTED_PROBLEM', 'SOLVED_PROBLEM', 'ATTEMPTED_PROBLEM',
            'VIEWED_THEORY', 'VIEWED_WEEK', 'VIEWED_DAY',
            'SAVED_DRAFT', 'CREATED_BOOKMARK', 'DELETED_BOOKMARK',
            'LOGIN', 'LOGOUT',
            name='activitytype'
        ), nullable=False),
        sa.Column('item_slug', sa.String(100), nullable=True),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
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
    # Drop indexes and tables in reverse order
    op.drop_index('ix_activities_created_at', table_name='activities')
    op.drop_index('ix_activities_item_slug', table_name='activities')
    op.drop_index('ix_activities_activity_type', table_name='activities')
    op.drop_index('ix_activities_user_id', table_name='activities')
    op.drop_table('activities')
    
    op.drop_index('ix_bookmarks_item_slug', table_name='bookmarks')
    op.drop_index('ix_bookmarks_user_id', table_name='bookmarks')
    op.drop_table('bookmarks')
    
    op.drop_index('ix_drafts_problem_slug', table_name='drafts')
    op.drop_index('ix_drafts_user_id', table_name='drafts')
    op.drop_table('drafts')
    
    op.drop_index('ix_progress_status', table_name='progress')
    op.drop_index('ix_progress_day_slug', table_name='progress')
    op.drop_index('ix_progress_week_slug', table_name='progress')
    op.drop_index('ix_progress_problem_slug', table_name='progress')
    op.drop_index('ix_progress_user_id', table_name='progress')
    op.drop_table('progress')
    
    # Drop enum types
    op.execute('DROP TYPE IF EXISTS activitytype')
    op.execute('DROP TYPE IF EXISTS itemtype')
    op.execute('DROP TYPE IF EXISTS problemstatus')
