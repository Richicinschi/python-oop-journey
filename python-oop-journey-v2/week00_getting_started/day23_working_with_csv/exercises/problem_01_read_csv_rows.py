"""Problem 01: Read CSV Rows

Topic: CSV - Reading Data
Difficulty: Easy

Write a function that reads a CSV file and returns its contents as a list of lists.

Function Signature:
    def read_csv_rows(filepath: str) -> list[list[str]] | None

Requirements:
    - Read the CSV file and return data as list of rows
    - Each row is a list of string values
    - Return None if file doesn't exist
    - Return empty list for empty file
    - Use the csv module

Behavior Notes:
    - Each row is a list of strings
    - Header row is included as first row (if present)
    - Return None for FileNotFoundError
    - Empty file returns [] (not [[]])

Examples:
    CSV file:
        name,age,city
        Alice,30,NYC
        Bob,25,LA
    
    >>> read_csv_rows("data.csv")
    [['name', 'age', 'city'], ['Alice', '30', 'NYC'], ['Bob', '25', 'LA']]
    
    File doesn't exist:
    >>> read_csv_rows("missing.csv")
    None
    
    Empty file:
    >>> read_csv_rows("empty.csv")
    []

Input Validation:
    - You may assume filepath is a valid string
    - Return None for non-existent files

Implementation Hint:
    - Use csv.reader()
    - Remember to open file with newline=''

"""

from __future__ import annotations

import csv


def read_csv_rows(filepath: str) -> list[list[str]] | None:
    """Read a CSV file and return its contents as a list of lists.

    Args:
        filepath: Path to the CSV file.

    Returns:
        List of rows (each row is a list of strings), or None if file not found.
    """
    raise NotImplementedError("Implement read_csv_rows")
