"""Problem 06: CSV Column Sum

Topic: CSV processing
Difficulty: Medium

Write a function that sums numeric values from a specific column in a CSV file.
The CSV has a header row with column names.

Examples:
    >>> csv_column_sum("data.csv", "price")
    150.5  # sum of all values in 'price' column
    >>> csv_column_sum("data.csv", "nonexistent")
    0.0

Requirements:
    - Return 0.0 if column doesn't exist or file doesn't exist
    - Handle numeric values (int or float)
    - Skip rows with non-numeric values in the target column
    - Use csv module for proper CSV parsing
    - Assume the first row is a header with column names
"""

from __future__ import annotations

from pathlib import Path


def csv_column_sum(filepath: str | Path, column_name: str) -> float:
    """Sum numeric values from a specific column in a CSV file.

    Args:
        filepath: Path to the CSV file.
        column_name: Name of the column to sum.

    Returns:
        Sum of numeric values in the column, or 0.0 if column
        doesn't exist or file is not found.
    """
    raise NotImplementedError("Implement csv_column_sum")
