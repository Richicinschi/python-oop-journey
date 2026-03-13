"""SQLAlchemy async database configuration."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql.base import PGDialect

from api.config import get_settings

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

# Create async engine with CockroachDB compatibility
connect_args = {"prepare_threshold": None}
if "cockroach" in settings.database_url.lower():
    connect_args["server_settings"] = {"application_name": "oop-journey"}

engine = create_async_engine(
    settings.database_url,
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
