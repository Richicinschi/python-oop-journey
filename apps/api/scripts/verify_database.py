#!/usr/bin/env python3
"""
Database Schema Verification Script

Checks the database schema against the SQLAlchemy models and reports mismatches.

Usage:
    python scripts/verify_database.py
    
Environment:
    Set DATABASE_URL environment variable to point to your database.
    Default: postgresql+asyncpg://postgres:postgres@localhost:5432/oop_journey
"""

import asyncio
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

# Add the parent directory to path so we can import api
sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


async def check_database_schema():
    """Check database schema against models."""
    from sqlalchemy import inspect, text
    from sqlalchemy.ext.asyncio import create_async_engine
    from api.config import get_settings
    
    settings = get_settings()
    engine = create_async_engine(settings.database_url)
    
    issues = []
    tables_found = []
    
    try:
        async with engine.connect() as conn:
            # Get all tables
            result = await conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            db_tables = [row[0] for row in result.fetchall()]
            tables_found = db_tables
            
            logger.info("=" * 60)
            logger.info("Database Schema Verification Report")
            logger.info("=" * 60)
            logger.info(f"\nDatabase: {settings.database_url.split('@')[-1]}")
            logger.info(f"Timestamp: {datetime.now().isoformat()}")
            
            logger.info(f"\n--- Tables Found ({len(db_tables)}) ---")
            for table in db_tables:
                logger.info(f"  ✓ {table}")
            
            # Expected tables from models
            expected_tables = [
                'users',
                'auth_tokens',
                'progress',
                'drafts',
                'bookmarks',
                'activities',
                'submissions',
                'submission_comments',
            ]
            
            logger.info(f"\n--- Expected Tables ({len(expected_tables)}) ---")
            for table in expected_tables:
                if table in db_tables:
                    logger.info(f"  ✓ {table}")
                else:
                    logger.error(f"  ✗ {table} - MISSING!")
                    issues.append(f"Missing table: {table}")
            
            # Check users table columns
            if 'users' in db_tables:
                logger.info("\n--- Users Table Columns ---")
                result = await conn.execute(text("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = 'users' AND table_schema = 'public'
                    ORDER BY ordinal_position
                """))
                columns = {row[0]: {'type': row[1], 'nullable': row[2]} for row in result.fetchall()}
                
                expected_user_columns = [
                    'id', 'email', 'display_name', 'created_at', 'updated_at',
                    'last_login_at', 'last_seen', 'is_active', 'avatar_url', 'github_id'
                ]
                
                for col in expected_user_columns:
                    if col in columns:
                        logger.info(f"  ✓ {col} ({columns[col]['type']})")
                    else:
                        logger.error(f"  ✗ {col} - MISSING!")
                        issues.append(f"Missing column: users.{col}")
                
                # Check for unexpected columns
                for col in columns:
                    if col not in expected_user_columns:
                        logger.warning(f"  ? {col} (unexpected)")
            
            # Check bookmarks table
            if 'bookmarks' in db_tables:
                logger.info("\n--- Bookmarks Table Columns ---")
                result = await conn.execute(text("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = 'bookmarks' AND table_schema = 'public'
                    ORDER BY ordinal_position
                """))
                columns = {row[0]: {'type': row[1], 'nullable': row[2]} for row in result.fetchall()}
                
                for col, info in columns.items():
                    logger.info(f"  - {col} ({info['type']})")
                
                # Check for note vs notes mismatch
                if 'notes' in columns and 'note' not in columns:
                    logger.error("  ✗ Column name mismatch: 'notes' should be 'note'")
                    issues.append("bookmarks: column 'notes' should be 'note'")
                if 'note' in columns:
                    logger.info("  ✓ note column exists")
            
            # Check indexes
            logger.info("\n--- Indexes ---")
            result = await conn.execute(text("""
                SELECT tablename, indexname
                FROM pg_indexes
                WHERE schemaname = 'public'
                ORDER BY tablename, indexname
            """))
            indexes_by_table = {}
            for row in result.fetchall():
                table, index = row
                if table not in indexes_by_table:
                    indexes_by_table[table] = []
                indexes_by_table[table].append(index)
            
            for table, indexes in sorted(indexes_by_table.items()):
                logger.info(f"\n  {table}:")
                for idx in sorted(indexes):
                    if idx.endswith('_pkey') or idx.endswith('_key') or idx.endswith('_uniq'):
                        logger.info(f"    • {idx} (constraint)")
                    else:
                        logger.info(f"    • {idx}")
            
            # Count rows in each table
            logger.info("\n--- Table Row Counts ---")
            for table in sorted(db_tables):
                try:
                    result = await conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    logger.info(f"  {table}: {count:,} rows")
                except Exception as e:
                    logger.warning(f"  {table}: Error counting - {e}")
            
            # Summary
            logger.info("\n" + "=" * 60)
            if issues:
                logger.error(f"FOUND {len(issues)} ISSUE(S):")
                for issue in issues:
                    logger.error(f"  • {issue}")
                logger.info("=" * 60)
                return False, tables_found
            else:
                logger.info("✓ All schema checks passed!")
                logger.info("=" * 60)
                return True, tables_found
                
    finally:
        await engine.dispose()


async def check_curriculum_data():
    """Check if curriculum data is properly loaded."""
    from api.services.curriculum import get_curriculum_service
    
    logger.info("\n--- Curriculum Data Check ---")
    
    try:
        service = get_curriculum_service()
        curriculum = service.get_curriculum()
        
        week_count = len(curriculum.weeks)
        problem_count = 0
        day_count = 0
        
        for week in curriculum.weeks:
            for day in week.days:
                day_count += 1
                problem_count += len(day.problems)
        
        logger.info(f"  Weeks: {week_count}")
        logger.info(f"  Days: {day_count}")
        logger.info(f"  Problems: {problem_count}")
        
        if problem_count >= 400:
            logger.info(f"  ✓ Full curriculum loaded ({problem_count} problems)")
            return True
        elif problem_count > 0:
            logger.warning(f"  ⚠ Partial curriculum ({problem_count} problems, expected ~433)")
            return False
        else:
            logger.error(f"  ✗ No curriculum data found")
            return False
            
    except Exception as e:
        logger.error(f"  ✗ Error loading curriculum: {e}")
        return False


def generate_report(issues, tables_found):
    """Generate a JSON report of the verification."""
    report = {
        'timestamp': datetime.now().isoformat(),
        'tables_found': tables_found,
        'tables_expected': [
            'users', 'auth_tokens', 'progress', 'drafts', 
            'bookmarks', 'activities', 'submissions', 'submission_comments'
        ],
        'issues': issues,
        'status': 'healthy' if not issues else 'needs_attention'
    }
    
    report_path = Path(__file__).parent.parent / 'data' / 'schema_report.json'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    logger.info(f"\nReport saved to: {report_path}")


async def main():
    """Main verification function."""
    try:
        schema_ok, tables = await check_database_schema()
        curriculum_ok = await check_curriculum_data()
        
        logger.info("\n" + "=" * 60)
        logger.info("Summary")
        logger.info("=" * 60)
        logger.info(f"Database Schema: {'✓ OK' if schema_ok else '✗ ISSUES FOUND'}")
        logger.info(f"Curriculum Data: {'✓ OK' if curriculum_ok else '✗ NEEDS SYNC'}")
        
        if not schema_ok or not curriculum_ok:
            logger.info("\nRecommended actions:")
            if not schema_ok:
                logger.info("  1. Run migrations: alembic upgrade head")
                logger.info("  2. Fix schema: alembic upgrade fix_schema_mismatches")
            if not curriculum_ok:
                logger.info("  3. Sync curriculum: python scripts/sync_curriculum.py")
            return 1
        else:
            logger.info("\n✓ All checks passed! System is healthy.")
            return 0
            
    except Exception as e:
        logger.error(f"Verification failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
