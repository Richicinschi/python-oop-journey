"""Add users and auth_tokens tables

Revision ID: add_users_and_auth_tokens
Revises: 
Create Date: 2026-03-12 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_users_and_auth_tokens'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create auth_tokens table
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
    
    # Add new columns to users table
    op.add_column('users', sa.Column('display_name', sa.String(100), nullable=True))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.add_column('users', sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    # Drop auth_tokens table
    op.drop_index('ix_auth_tokens_user_id_created_at', table_name='auth_tokens')
    op.drop_index('ix_auth_tokens_token_hash', table_name='auth_tokens')
    op.drop_table('auth_tokens')
    
    # Remove new columns from users table
    op.drop_column('users', 'last_login_at')
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'display_name')
