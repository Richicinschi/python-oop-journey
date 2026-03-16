"""File persistence operations for the library system.

This module handles saving and loading library data to/from JSON files.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from week02_fundamentals_advanced.project.reference_solution.exceptions import StorageError


def save_library(library: dict[str, Any], filepath: str) -> None:
    """Save library data to a JSON file.
    
    Uses atomic write: writes to a temporary file first, then renames
    to prevent data corruption if the operation is interrupted.
    
    Args:
        library: Dictionary mapping ISBNs to book dictionaries
        filepath: Path to the output JSON file
        
    Returns:
        None
        
    Raises:
        StorageError: If the file cannot be written
    """
    path = Path(filepath)
    
    try:
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to temporary file in the same directory for atomic rename
        temp_fd, temp_path = tempfile.mkstemp(
            dir=path.parent,
            prefix=f".{path.name}.tmp_"
        )
        
        try:
            with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                json.dump(library, f, indent=2, ensure_ascii=False)
            
            # Atomic rename
            os.replace(temp_path, filepath)
            
        except Exception:
            # Clean up temp file on error
            try:
                os.unlink(temp_path)
            except OSError:
                pass
            raise
            
    except (OSError, IOError) as e:
        raise StorageError(
            f"Failed to save library: {e}",
            filepath
        ) from e
    except Exception as e:
        raise StorageError(
            f"Unexpected error saving library: {e}",
            filepath
        ) from e


def load_library(filepath: str) -> dict[str, Any]:
    """Load library data from a JSON file.
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        Dictionary mapping ISBNs to book dictionaries.
        Returns empty dict if file doesn't exist.
        
    Raises:
        StorageError: If the file exists but cannot be read or parsed
    """
    path = Path(filepath)
    
    if not path.exists():
        return {}
    
    if not path.is_file():
        raise StorageError(
            f"Path exists but is not a file",
            filepath
        )
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, dict):
            raise StorageError(
                f"Invalid library format: expected object, got {type(data).__name__}",
                filepath
            )
        
        return data
        
    except json.JSONDecodeError as e:
        raise StorageError(
            f"Invalid JSON: {e}",
            filepath
        ) from e
    except (OSError, IOError) as e:
        raise StorageError(
            f"Failed to read file: {e}",
            filepath
        ) from e


def library_exists(filepath: str) -> bool:
    """Check if a library file exists.
    
    Args:
        filepath: Path to check
        
    Returns:
        True if file exists and is a file, False otherwise
    """
    return Path(filepath).is_file()


def backup_library(filepath: str, backup_suffix: str = ".backup") -> str:
    """Create a backup of a library file.
    
    Args:
        filepath: Path to the library file
        backup_suffix: Suffix to append to filename
        
    Returns:
        Path to the backup file
        
    Raises:
        StorageError: If backup cannot be created
    """
    source = Path(filepath)
    backup_path = str(source) + backup_suffix
    
    if not source.exists():
        raise StorageError(
            "Cannot backup: source file does not exist",
            filepath
        )
    
    try:
        import shutil
        shutil.copy2(filepath, backup_path)
        return backup_path
    except (OSError, IOError) as e:
        raise StorageError(
            f"Failed to create backup: {e}",
            filepath
        ) from e
