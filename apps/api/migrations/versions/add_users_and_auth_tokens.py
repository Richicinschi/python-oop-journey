"""Add users and auth_tokens tables

Revision ID: add_users_and_auth_tokens
Revises: 
Create Date: 2026-03-12 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = '001_add_users'
down_revision: Union[str, None] = None
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


def upgrade() -> None:
    # Create users table FIRST (if not exists)
    if not table_exists('users'):
        op.create_table(
            'users',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('email', sa.String(255), nullable=False),
            sa.Column('display_name', sa.String(100), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email'),
        )
        
        # Create indexes for users
        op.create_index('ix_users_email', 'users', ['email'], unique=True)
    
    # Create auth_tokens table SECOND (after users exists, if not exists)
    if not table_exists('auth_tokens'):
        op.create_table(
            'auth_tokens',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('user_id', sa.String(36), nullable=False),
            sa.Column('token_hash', sa.String(255), nullable=False),
            sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
            sa.Column('used_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        )
        
        # Create indexes for auth_tokens
        op.create_index('ix_auth_tokens_token_hash', 'auth_tokens', ['token_hash'])
        op.create_index('ix_auth_tokens_user_id_created_at', 'auth_tokens', ['user_id', 'created_at'])


def downgrade() -> None:
    # Drop auth_tokens first (depends on users)
    if table_exists('auth_tokens'):
        op.drop_index('ix_auth_tokens_user_id_created_at', table_name='auth_tokens')
        op.drop_index('ix_auth_tokens_token_hash', table_name='auth_tokens')
        op.drop_table('auth_tokens')
    
    # Drop users table last
    if table_exists('users'):
        op.drop_index('ix_users_email', table_name='users')
        op.drop_table('users')
