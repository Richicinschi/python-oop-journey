"""Solution for Problem 06: Safe JSON Loader."""

from __future__ import annotations

import json
from pathlib import Path


def safe_json_loader(filepath: str | Path) -> dict:
    """Safely load a JSON file, returning empty dict on any error.

    Args:
        filepath: Path to the JSON file

    Returns:
        The parsed JSON as a dictionary, or empty dict on error
    """
    try:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            return {}
    except (FileNotFoundError, json.JSONDecodeError, PermissionError, OSError):
        return {}
