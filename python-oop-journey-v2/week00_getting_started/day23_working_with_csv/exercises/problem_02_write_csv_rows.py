"""Problem 02: Write CSV Rows

Topic: CSV - Writing Data
Difficulty: Easy

Write a function that writes a list of lists to a CSV file.

Function Signature:
    def write_csv_rows(filepath: str, rows: list[list[str]]) -> bool

Requirements:
    - Write the data to a CSV file
    - Overwrite if file exists
    - Return True if successful
    - Return False on permission/IO errors
    - Use the csv module

Behavior Notes:
    - Each inner list becomes one row
    - All values are written as strings
    - Overwrites existing files
    - Empty list creates empty file

Examples:
    Write data:
    >>> data = [['name', 'age'], ['Alice', '30'], ['Bob', '25']]
    >>> write_csv_rows("output.csv", data)
    True
    # File contains:
    # name,age
    # Alice,30
    # Bob,25
    
    Empty data:
    >>> write_csv_rows("empty.csv", [])
    True
    # File is created but empty
    
    Permission error:
    >>> write_csv_rows("/root/protected.csv", [["test"]])
    False

Input Validation:
    - You may assume filepath is a valid string
    - You may assume rows is a list of lists
    - Handle permission errors by returning False

Implementation Hint:
    - Use csv.writer()
    - Remember to open file with newline=''

"""

from __future__ import annotations

import csv


def write_csv_rows(filepath: str, rows: list[list[str]]) -> bool:
    """Write a list of lists to a CSV file.

    Args:
        filepath: Path to the CSV file.
        rows: List of rows to write.

    Returns:
        True if successful, False on error.
    """
    raise NotImplementedError("Implement write_csv_rows")
