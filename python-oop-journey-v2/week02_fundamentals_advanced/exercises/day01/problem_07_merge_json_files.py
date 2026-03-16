"""Problem 07: Merge JSON Files

Topic: JSON processing
Difficulty: Medium

Write a function that merges multiple JSON files into a single dictionary.
Each JSON file should contain a dictionary. Values from later files
override values from earlier files for duplicate keys.

Examples:
    >>> merge_json_files(["config1.json", "config2.json"])
    {'name': 'app', 'debug': False, 'port': 8080}
    >>> merge_json_files(["empty.json"])
    {}
    >>> merge_json_files([])
    {}

Requirements:
    - Skip files that don't exist or contain invalid JSON
    - Later files override earlier files for duplicate keys
    - Return empty dict if no valid files or empty list
    - Return the count of successfully merged files (as '_merged_count' key)
    - Assume each JSON file contains a dictionary at the root
"""

from __future__ import annotations

import json
from pathlib import Path


def merge_json_files(filepaths: list[str | Path]) -> dict:
    """Merge multiple JSON files into a single dictionary.

    Args:
        filepaths: List of paths to JSON files.

    Returns:
        Merged dictionary with values from later files taking precedence.
        Includes '_merged_count' key with count of successfully merged files.
    """
    raise NotImplementedError("Implement merge_json_files")
