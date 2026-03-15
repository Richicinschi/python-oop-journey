#!/usr/bin/env python3
"""
Curriculum Sync Script

Copies the full curriculum data from the web app to the API.
The web app has the complete 433-problem curriculum (6MB),
while the API only has sample data (5KB).

Usage:
    python scripts/sync_curriculum.py
    
Or from the API directory:
    python -m scripts.sync_curriculum
"""

import json
import logging
import shutil
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def get_project_root() -> Path:
    """Get the project root directory."""
    # We're in website-playground/apps/api/scripts
    return Path(__file__).parent.parent.parent.parent


def sync_curriculum():
    """Copy curriculum from web app to API."""
    project_root = get_project_root()
    
    # Source: web app data
    web_data_path = project_root / "apps" / "web" / "data" / "curriculum.json"
    
    # Destination: API data
    api_data_dir = project_root / "apps" / "api" / "data"
    api_data_path = api_data_dir / "curriculum.json"
    
    # Ensure API data directory exists
    api_data_dir.mkdir(parents=True, exist_ok=True)
    
    if not web_data_path.exists():
        logger.error(f"Source curriculum not found: {web_data_path}")
        logger.error("Make sure the web app has been built and has curriculum data")
        return False
    
    # Get file sizes for comparison
    web_size = web_data_path.stat().st_size
    
    # Load and validate the curriculum
    try:
        with open(web_data_path, 'r', encoding='utf-8') as f:
            curriculum = json.load(f)
        
        # Count problems
        problem_count = 0
        week_count = len(curriculum.get('weeks', []))
        day_count = 0
        
        for week in curriculum.get('weeks', []):
            for day in week.get('days', []):
                day_count += 1
                problem_count += len(day.get('problems', []))
        
        logger.info(f"Source curriculum validated:")
        logger.info(f"  - {week_count} weeks")
        logger.info(f"  - {day_count} days")
        logger.info(f"  - {problem_count} problems")
        logger.info(f"  - {web_size:,} bytes")
        
        if problem_count < 400:
            logger.warning(f"Expected ~433 problems, found {problem_count}")
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in source curriculum: {e}")
        return False
    except Exception as e:
        logger.error(f"Error validating curriculum: {e}")
        return False
    
    # Copy the file
    try:
        shutil.copy2(web_data_path, api_data_path)
        logger.info(f"\nCopied curriculum to: {api_data_path}")
        
        # Verify the copy
        api_size = api_data_path.stat().st_size
        if api_size == web_size:
            logger.info(f"✓ Copy verified: {api_size:,} bytes")
            return True
        else:
            logger.error(f"Size mismatch: expected {web_size}, got {api_size}")
            return False
            
    except Exception as e:
        logger.error(f"Failed to copy curriculum: {e}")
        return False


def create_backup():
    """Create a backup of the existing API curriculum."""
    project_root = get_project_root()
    api_data_path = project_root / "apps" / "api" / "data" / "curriculum.json"
    backup_path = project_root / "apps" / "api" / "data" / "curriculum.json.backup"
    
    if api_data_path.exists():
        shutil.copy2(api_data_path, backup_path)
        logger.info(f"Backup created: {backup_path}")
        return backup_path
    return None


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Curriculum Sync: Web App → API")
    logger.info("=" * 60)
    
    # Create backup
    backup = create_backup()
    
    # Sync curriculum
    success = sync_curriculum()
    
    if success:
        logger.info("\n" + "=" * 60)
        logger.info("✓ Curriculum sync completed successfully!")
        logger.info("=" * 60)
        logger.info("\nNext steps:")
        logger.info("1. Restart the API server to load the new curriculum")
        logger.info("2. Verify at: http://localhost:8000/api/v1/curriculum/problems")
        exit(0)
    else:
        logger.error("\n" + "=" * 60)
        logger.error("✗ Curriculum sync failed!")
        logger.error("=" * 60)
        if backup:
            logger.info(f"\nRestore backup with:")
            logger.info(f"  cp {backup} {backup.parent / 'curriculum.json'}")
        exit(1)
