"""Problem 06: Safe JSON Loader

Topic: File I/O Exception Handling
Difficulty: Medium

Implement a function to safely load JSON files with error handling.

Examples:
    # Assuming 'valid.json' contains {"key": "value"}
    >>> safe_json_loader("valid.json")  # doctest: +SKIP
    {'key': 'value'}
    
    # Assuming 'missing.json' does not exist
    >>> safe_json_loader("missing.json")  # doctest: +SKIP
    {}
    
    # Assuming 'invalid.json' contains invalid JSON
    >>> safe_json_loader("invalid.json")  # doctest: +SKIP
    {}

Requirements:
    - Return the parsed JSON as a dictionary on success
    - Return an empty dict if file doesn't exist
    - Return an empty dict if JSON is malformed
    - Return an empty dict if file cannot be read
    - The function should never raise an exception
"""

from __future__ import annotations

from pathlib import Path


def safe_json_loader(filepath: str | Path) -> dict:
    """Safely load a JSON file, returning empty dict on any error.

    Args:
        filepath: Path to the JSON file

    Returns:
        The parsed JSON as a dictionary, or empty dict on error
    """
    raise NotImplementedError("Implement safe_json_loader")
