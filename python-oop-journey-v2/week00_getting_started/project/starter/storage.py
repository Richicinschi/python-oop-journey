"""Storage module for file I/O operations.

Handles loading and saving tasks to/from JSON files.
"""

from __future__ import annotations

import json
import os
from typing import List

from .task import Task


def load_tasks(filepath: str) -> List[Task]:
    """Load tasks from a JSON file.

    Args:
        filepath: Path to the JSON file

    Returns:
        List of Task objects

    Raises:
        FileNotFoundError: If file doesn't exist (should return empty list instead)
        json.JSONDecodeError: If file contains invalid JSON
    """
    # TODO: Implement file loading with error handling
    raise NotImplementedError("Implement load_tasks")


def save_tasks(tasks: List[Task], filepath: str) -> bool:
    """Save tasks to a JSON file.

    Args:
        tasks: List of Task objects to save
        filepath: Path to the JSON file

    Returns:
        True if successful, False otherwise
    """
    # TODO: Implement file saving with error handling
    raise NotImplementedError("Implement save_tasks")


def ensure_directory_exists(filepath: str) -> None:
    """Ensure the directory for the given file path exists.

    Args:
        filepath: Path to a file
    """
    # TODO: Create parent directories if they don't exist
    raise NotImplementedError("Implement ensure_directory_exists")
