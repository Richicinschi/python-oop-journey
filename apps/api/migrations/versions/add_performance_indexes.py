"""Add performance indexes for frequently queried fields.

Revision ID: add_performance_indexes
Revises: add_progress_drafts_bookmarks_activity
Create Date: 2026-03-12
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_performance_indexes'
down_revision = 'add_progress_drafts_bookmarks_activity'
branch_labels = None
depends_on = None


def upgrade():
    """Add performance indexes for frequently queried fields."""
    
    # Progress table indexes
    op.create_index(
        'idx_progress_user_problem', 
        'progress', 
        ['user_id', 'problem_slug'],
        unique=False
    )
    op.create_index(
        'idx_progress_user_status', 
        'progress', 
        ['user_id', 'status'],
        unique=False
    )
    op.create_index(
        'idx_progress_solved_at', 
        'progress', 
        ['solved_at'],
        unique=False,
        postgresql_where=sa.text('solved_at IS NOT NULL')
    )
    
    # Activity table indexes
    op.create_index(
        'idx_activity_user_created', 
        'activity', 
        ['user_id', 'created_at'],
        unique=False
    )
    op.create_index(
        'idx_activity_type_created', 
        'activity', 
        ['activity_type', 'created_at'],
        unique=False
    )
    op.create_index(
        'idx_activity_item', 
        'activity', 
        ['item_type', 'item_id'],
        unique=False
    )
    
    # Bookmarks table indexes
    op.create_index(
        'idx_bookmarks_user_type', 
        'bookmarks', 
        ['user_id', 'item_type'],
        unique=False
    )
    op.create_index(
        'idx_bookmarks_user_created', 
        'bookmarks', 
        ['user_id', 'created_at'],
        unique=False
    )
    
    # Drafts table indexes
    op.create_index(
        'idx_drafts_user_problem', 
        'drafts', 
        ['user_id', 'problem_slug'],
        unique=False
    )
    op.create_index(
        'idx_drafts_updated_at', 
        'drafts', 
        ['updated_at'],
        unique=False
    )
    
    # Submissions table indexes (if exists)
    try:
        op.create_index(
            'idx_submissions_user_problem', 
            'submissions', 
            ['user_id', 'problem_slug'],
            unique=False
        )
        op.create_index(
            'idx_submissions_status', 
            'submissions', 
            ['status', 'submitted_at'],
            unique=False
        )
        op.create_index(
            'idx_submissions_verified', 
            'submissions', 
            ['is_verified', 'verified_at'],
            unique=False,
            postgresql_where=sa.text('is_verified = true')
        )
    except Exception:
        # Submissions table might not exist yet
        pass
    
    # Users table indexes
    try:
        op.create_index(
            'idx_users_email', 
            'users', 
            ['email'],
            unique=False
        )
        op.create_index(
            'idx_users_github_id', 
            'users', 
            ['github_id'],
            unique=False,
            postgresql_where=sa.text('github_id IS NOT NULL')
        )
    except Exception:
        pass
    
    # Auth tokens indexes
    try:
        op.create_index(
            'idx_auth_tokens_user', 
            'auth_tokens', 
            ['user_id', 'token_type'],
            unique=False
        )
        op.create_index(
            'idx_auth_tokens_expires', 
            'auth_tokens', 
            ['expires_at'],
            unique=False
        )
    except Exception:
        pass


def downgrade():
    """Remove performance indexes."""
    
    # Drop progress indexes
    op.drop_index('idx_progress_user_problem', table_name='progress')
    op.drop_index('idx_progress_user_status', table_name='progress')
    op.drop_index('idx_progress_solved_at', table_name='progress')
    
    # Drop activity indexes
    op.drop_index('idx_activity_user_created', table_name='activity')
    op.drop_index('idx_activity_type_created', table_name='activity')
    op.drop_index('idx_activity_item', table_name='activity')
    
    # Drop bookmarks indexes
    op.drop_index('idx_bookmarks_user_type', table_name='bookmarks')
    op.drop_index('idx_bookmarks_user_created', table_name='bookmarks')
    
    # Drop drafts indexes
    op.drop_index('idx_drafts_user_problem', table_name='drafts')
    op.drop_index('idx_drafts_updated_at', table_name='drafts')
    
    # Drop submissions indexes
    try:
        op.drop_index('idx_submissions_user_problem', table_name='submissions')
        op.drop_index('idx_submissions_status', table_name='submissions')
        op.drop_index('idx_submissions_verified', table_name='submissions')
    except Exception:
        pass
    
    # Drop users indexes
    try:
        op.drop_index('idx_users_email', table_name='users')
        op.drop_index('idx_users_github_id', table_name='users')
    except Exception:
        pass
    
    # Drop auth tokens indexes
    try:
        op.drop_index('idx_auth_tokens_user', table_name='auth_tokens')
        op.drop_index('idx_auth_tokens_expires', table_name='auth_tokens')
    except Exception:
        pass
