"""Reference solution for Problem 07: Merge JSON Files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List


def merge_json_files(filepaths: list[str | Path]) -> dict:
    """Merge multiple JSON files into a single dictionary.

    Args:
        filepaths: List of paths to JSON files.

    Returns:
        Merged dictionary with values from later files taking precedence.
        Includes '_merged_count' key with count of successfully merged files.
    """
    result: dict = {}
    merged_count = 0
    
    for filepath in filepaths:
        path = Path(filepath)
        
        if not path.exists():
            continue
        
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                
            if isinstance(data, dict):
                result.update(data)
                merged_count += 1
        except (json.JSONDecodeError, IOError):
            # Skip invalid JSON or unreadable files
            continue
    
    result['_merged_count'] = merged_count
    return result
