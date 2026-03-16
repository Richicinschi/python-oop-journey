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
        List of Task objects. Returns empty list if file doesn't exist.

    Raises:
        json.JSONDecodeError: If file contains invalid JSON
    """
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            return []

        return [Task.from_dict(item) for item in data if isinstance(item, dict)]
    except json.JSONDecodeError:
        raise
    except (IOError, OSError):
        return []


def save_tasks(tasks: List[Task], filepath: str) -> bool:
    """Save tasks to a JSON file.

    Args:
        tasks: List of Task objects to save
        filepath: Path to the JSON file

    Returns:
        True if successful, False otherwise
    """
    try:
        ensure_directory_exists(filepath)

        data = [task.to_dict() for task in tasks]

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return True
    except (IOError, OSError, TypeError):
        return False


def ensure_directory_exists(filepath: str) -> None:
    """Ensure the directory for the given file path exists.

    Args:
        filepath: Path to a file
    """
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
