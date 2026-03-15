"""SQLAlchemy async database configuration."""

import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql.base import PGDialect

from api.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Monkey-patch for CockroachDB compatibility
# CockroachDB reports version as "CockroachDB CCL v25.4.1..." 
# instead of "PostgreSQL 14.2..."
_original_get_server_version_info = PGDialect._get_server_version_info

def _patched_get_server_version_info(self, connection):
    """Patch to handle CockroachDB version strings."""
    try:
        return _original_get_server_version_info(self, connection)
    except AssertionError as e:
        # Check if this is a CockroachDB version string issue
        if "Could not determine version" in str(e):
            # Return a compatible PostgreSQL version tuple
            # This tells SQLAlchemy to treat it as PostgreSQL 14.x
            return (14, 0, 0)
        raise

PGDialect._get_server_version_info = _patched_get_server_version_info


# Use database URL directly without prepare_threshold modifications
# The prepare_threshold parameter was causing compatibility issues with
# certain PostgreSQL providers (Render, etc.) and asyncpg versions.
# CockroachDB compatibility is handled via monkey-patch above.
database_url = settings.database_url

# Create async engine with minimal connect_args
# prepare_threshold has been removed to fix compatibility issues
connect_args = {}
if "cockroach" in settings.database_url.lower():
    connect_args["server_settings"] = {"application_name": "oop-journey"}

logger.info(f"Initializing database engine with URL: {database_url.replace(settings.database_url.split('@')[0] if '@' in settings.database_url else database_url, '***')}")

engine = create_async_engine(
    database_url,
    echo=settings.debug,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    pool_pre_ping=True,
    connect_args=connect_args,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for declarative models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database sessions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Close database connections."""
    await engine.dispose()
