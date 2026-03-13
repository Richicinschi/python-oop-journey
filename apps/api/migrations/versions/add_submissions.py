"""Add submissions and submission comments tables

Revision ID: add_submissions
Revises: add_progress_drafts_bookmarks_activity
Create Date: 2026-03-12 18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = 'add_submissions'
down_revision: Union[str, None] = 'add_progress_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def table_exists(table_name: str) -> bool:
    """Check if a table already exists."""
    bind = op.get_bind()
    inspector = inspect(bind)
    return table_name in inspector.get_table_names()


def upgrade() -> None:
    """Create submissions tables."""
    # Create submissions table (if not exists)
    if not table_exists('submissions'):
        op.create_table(
            'submissions',
            sa.Column('id', sa.String(36), primary_key=True),
            sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
            sa.Column('project_slug', sa.String(100), nullable=False, index=True),
            sa.Column('week_slug', sa.String(100), nullable=True, index=True),
            sa.Column('day_slug', sa.String(100), nullable=True, index=True),
            sa.Column('files', sa.JSON, nullable=False, default=dict),
            sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=False),
            sa.Column('status', sa.String(20), nullable=False, default='pending_review', index=True),
            sa.Column('reviewer_notes', sa.Text, nullable=True),
            sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('reviewed_by', sa.String(36), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
            sa.Column('test_results', sa.JSON, nullable=False, default=dict),
            sa.Column('metrics', sa.JSON, nullable=False, default=dict),
            sa.Column('is_exemplary', sa.Boolean, default=False, nullable=False),
            sa.Column('showcase_opt_in', sa.Boolean, default=False, nullable=False),
            sa.Column('notification_sent', sa.Boolean, default=False, nullable=False),
            sa.Column('notification_sent_at', sa.DateTime(timezone=True), nullable=True),
        )
    
    # Create submission_comments table (if not exists)
    if not table_exists('submission_comments'):
        op.create_table(
            'submission_comments',
            sa.Column('id', sa.String(36), primary_key=True),
            sa.Column('submission_id', sa.String(36), sa.ForeignKey('submissions.id', ondelete='CASCADE'), nullable=False, index=True),
            sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
            sa.Column('content', sa.Text, nullable=False),
            sa.Column('line_number', sa.Integer, nullable=True),
            sa.Column('file_path', sa.String(255), nullable=True),
            sa.Column('is_review', sa.Boolean, default=False, nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        )


def downgrade() -> None:
    """Drop submissions tables."""
    if table_exists('submission_comments'):
        op.drop_table('submission_comments')
    
    if table_exists('submissions'):
        op.drop_table('submissions')
