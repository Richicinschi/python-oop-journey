-- =============================================================================
-- Database Initialization Script
-- =============================================================================
-- This script runs when the PostgreSQL container starts for the first time.
-- =============================================================================

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search

-- Create roles (if needed)
-- CREATE ROLE oopjourney_app WITH LOGIN PASSWORD 'change-me';

-- Grant privileges
-- GRANT ALL PRIVILEGES ON DATABASE oopjourney TO oopjourney_app;

-- Note: Application tables are managed by Alembic migrations
-- Do not create tables here - use migrations instead
