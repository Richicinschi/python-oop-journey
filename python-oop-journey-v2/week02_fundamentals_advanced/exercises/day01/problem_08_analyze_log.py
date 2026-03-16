"""Problem 08: Analyze Log

Topic: Log file analysis
Difficulty: Medium

Write a function that analyzes a log file and returns statistics.
The function should count occurrences of different log levels
(ERROR, WARNING, INFO, DEBUG) and return totals.

Examples:
    >>> analyze_log("app.log")
    {
        'ERROR': 5,
        'WARNING': 12,
        'INFO': 150,
        'DEBUG': 0,
        'total_lines': 167,
        'unknown_lines': 0
    }

Requirements:
    - Log levels are case-insensitive (e.g., "error" and "ERROR" both count)
    - A line matches if it starts with the log level followed by space or colon
    - Return counts for all four standard levels plus total_lines
    - unknown_lines counts lines that don't match any log level format
    - Return empty dict with all zeros for non-existent files
    - Lines are considered to match a level if they start with 
      LEVEL followed by space, colon, or hyphen (e.g., "ERROR:", "INFO -", "DEBUG ")
"""

from __future__ import annotations

from pathlib import Path


def analyze_log(filepath: str | Path) -> dict[str, int]:
    """Analyze a log file and return level statistics.

    Args:
        filepath: Path to the log file.

    Returns:
        Dictionary with counts for ERROR, WARNING, INFO, DEBUG,
        total_lines, and unknown_lines. Returns dict with all zeros
        for non-existent files.
    """
    raise NotImplementedError("Implement analyze_log")
