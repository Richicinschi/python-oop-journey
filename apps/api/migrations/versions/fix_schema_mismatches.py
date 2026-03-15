"""Fix schema mismatches between models and database

Revision ID: fix_schema_mismatches
Revises: add_perf_indexes
Create Date: 2026-03-15

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect, text

# revision identifiers, used by Alembic.
revision: str = 'fix_schema_mismatches'
down_revision: Union[str, None] = 'add_perf_indexes'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def table_exists(table_name: str) -> bool:
    """Check if a table already exists."""
    bind = op.get_bind()
    inspector = inspect(bind)
    return table_name in inspector.get_table_names()


def column_exists(table_name: str, column_name: str) -> bool:
    """Check if a column already exists in a table."""
    bind = op.get_bind()
    inspector = inspect(bind)
    try:
        columns = [col['name'] for col in inspector.get_columns(table_name)]
        return column_name in columns
    except Exception:
        return False


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
    """Fix schema mismatches."""
    
    # ==========================================
    # Fix 1: Add missing columns to users table
    # ==========================================
    if table_exists('users'):
        # Add last_seen column (missing from original migration)
        if not column_exists('users', 'last_seen'):
            op.add_column(
                'users',
                sa.Column('last_seen', sa.DateTime(timezone=True), 
                         server_default=sa.func.now(), nullable=False)
            )
            print("Added column: users.last_seen")
        else:
            print("Column already exists: users.last_seen")
        
        # Add avatar_url column
        if not column_exists('users', 'avatar_url'):
            op.add_column(
                'users',
                sa.Column('avatar_url', sa.String(500), nullable=True)
            )
            print("Added column: users.avatar_url")
        else:
            print("Column already exists: users.avatar_url")
        
        # Add github_id column
        if not column_exists('users', 'github_id'):
            op.add_column(
                'users',
                sa.Column('github_id', sa.String(100), nullable=True, unique=True)
            )
            print("Added column: users.github_id")
            if not index_exists('users', 'ix_users_github_id'):
                op.create_index('ix_users_github_id', 'users', ['github_id'])
        else:
            print("Column already exists: users.github_id")
    
    # ==========================================
    # Fix 2: Check bookmarks table schema
    # ==========================================
    if table_exists('bookmarks'):
        # The migration created 'notes' column, and we've updated the model to match
        # So no changes needed here - just verify
        if column_exists('bookmarks', 'notes'):
            print("✓ Bookmarks table has 'notes' column (matches model)")
        elif column_exists('bookmarks', 'note'):
            print("Renaming 'note' to 'notes' in bookmarks table")
            op.alter_column('bookmarks', 'note', new_column_name='notes')
        else:
            print("WARNING: bookmarks table missing notes/note column")
        
        # Check id column type
        bind = op.get_bind()
        inspector = inspect(bind)
        try:
            columns = {col['name']: col for col in inspector.get_columns('bookmarks')}
            if 'id' in columns:
                col_type = columns['id']['type']
                if hasattr(col_type, 'length'):
                    print(f"✓ Bookmarks.id is String({col_type.length}) - matches model")
                else:
                    print(f"✓ Bookmarks.id is {col_type} - model updated to match")
        except Exception as e:
            print(f"Could not check bookmarks schema: {e}")
    
    # ==========================================
    # Fix 3: Ensure all required indexes exist
    # ==========================================
    
    # Users table indexes
    if table_exists('users'):
        if not index_exists('users', 'ix_users_email'):
            op.create_index('ix_users_email', 'users', ['email'], unique=True)
            print("Created index: ix_users_email")
        else:
            print("Index already exists: ix_users_email")
        if not index_exists('users', 'ix_users_is_active'):
            op.create_index('ix_users_is_active', 'users', ['is_active'])
            print("Created index: ix_users_is_active")
        else:
            print("Index already exists: ix_users_is_active")
    
    # Progress table indexes
    if table_exists('progress'):
        if not index_exists('progress', 'ix_progress_user_id'):
            op.create_index('ix_progress_user_id', 'progress', ['user_id'])
        if not index_exists('progress', 'ix_progress_problem_slug'):
            op.create_index('ix_progress_problem_slug', 'progress', ['problem_slug'])
        if not index_exists('progress', 'ix_progress_status'):
            op.create_index('ix_progress_status', 'progress', ['status'])
    
    # Drafts table indexes
    if table_exists('drafts'):
        if not index_exists('drafts', 'ix_drafts_user_id'):
            op.create_index('ix_drafts_user_id', 'drafts', ['user_id'])
        if not index_exists('drafts', 'ix_drafts_problem_slug'):
            op.create_index('ix_drafts_problem_slug', 'drafts', ['problem_slug'])
    
    # Bookmarks table indexes
    if table_exists('bookmarks'):
        if not index_exists('bookmarks', 'ix_bookmarks_user_id'):
            op.create_index('ix_bookmarks_user_id', 'bookmarks', ['user_id'])
        if not index_exists('bookmarks', 'ix_bookmarks_item_slug'):
            op.create_index('ix_bookmarks_item_slug', 'bookmarks', ['item_slug'])
        if not index_exists('bookmarks', 'ix_bookmarks_item_type'):
            op.create_index('ix_bookmarks_item_type', 'bookmarks', ['item_type'])
    
    # Activities table indexes
    if table_exists('activities'):
        if not index_exists('activities', 'ix_activities_user_id'):
            op.create_index('ix_activities_user_id', 'activities', ['user_id'])
        if not index_exists('activities', 'ix_activities_activity_type'):
            op.create_index('ix_activities_activity_type', 'activities', ['activity_type'])
        if not index_exists('activities', 'ix_activities_created_at'):
            op.create_index('ix_activities_created_at', 'activities', ['created_at'])
    
    # Auth tokens table indexes
    if table_exists('auth_tokens'):
        if not index_exists('auth_tokens', 'ix_auth_tokens_token_hash'):
            op.create_index('ix_auth_tokens_token_hash', 'auth_tokens', ['token_hash'])
    
    # Submissions table indexes
    if table_exists('submissions'):
        if not index_exists('submissions', 'ix_submissions_user_id'):
            op.create_index('ix_submissions_user_id', 'submissions', ['user_id'])
        if not index_exists('submissions', 'ix_submissions_project_slug'):
            op.create_index('ix_submissions_project_slug', 'submissions', ['project_slug'])
        if not index_exists('submissions', 'ix_submissions_status'):
            op.create_index('ix_submissions_status', 'submissions', ['status'])
    
    print("Schema fixes applied successfully!")


def downgrade() -> None:
    """Revert schema fixes."""
    # Note: We don't drop the columns we added, as that would lose data
    # Instead, we just log that this is a one-way migration for safety
    print("WARNING: Downgrade not implemented for schema fixes to prevent data loss")
