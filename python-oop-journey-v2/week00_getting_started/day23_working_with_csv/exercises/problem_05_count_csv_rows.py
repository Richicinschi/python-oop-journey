"""Problem 05: Count CSV Rows

Topic: CSV - Data Analysis
Difficulty: Easy

Write a function that counts the number of data rows in a CSV file (excluding header).

Function Signature:
    def count_csv_rows(filepath: str) -> int | None

Requirements:
    - Return the number of data rows (excluding header)
    - Return None if file doesn't exist
    - Return 0 for empty file or file with only header
    - Assume first row is header

Behavior Notes:
    - First row is assumed to be header (not counted)
    - All subsequent rows are counted as data
    - Empty lines at end may or may not be counted (csv module handles this)

Examples:
    CSV file:
        name,age
        Alice,30
        Bob,25
    
    >>> count_csv_rows("data.csv")
    2
    
    Header only:
    >>> count_csv_rows("header_only.csv")
    0
    
    Empty file:
    >>> count_csv_rows("empty.csv")
    0
    
    File doesn't exist:
    >>> count_csv_rows("missing.csv")
    None

Input Validation:
    - You may assume filepath is a valid string
    - Return None for non-existent files

Implementation Hint:
    - Read with csv.reader and count rows, subtract 1 for header
    - Or use len(list(reader)) - 1

"""

from __future__ import annotations

import csv


def count_csv_rows(filepath: str) -> int | None:
    """Count the number of data rows in a CSV file (excluding header).

    Args:
        filepath: Path to the CSV file.

    Returns:
        Number of data rows, or None if file not found.
    """
    raise NotImplementedError("Implement count_csv_rows")
