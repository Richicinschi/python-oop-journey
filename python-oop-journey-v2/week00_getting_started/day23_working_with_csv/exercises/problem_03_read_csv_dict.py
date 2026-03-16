"""Problem 03: Read CSV as Dictionary

Topic: CSV - DictReader
Difficulty: Easy

Write a function that reads a CSV file and returns its contents as a list of dictionaries.

Function Signature:
    def read_csv_dict(filepath: str) -> list[dict[str, str]] | None

Requirements:
    - Use csv.DictReader to read the file
    - First row is treated as header (column names)
    - Return list of dictionaries (one per row)
    - Return None if file doesn't exist
    - Each dict maps column name to value

Behavior Notes:
    - First row becomes dictionary keys
    - Subsequent rows become dict values
    - Return None for FileNotFoundError
    - Empty file (no header) returns []

Examples:
    CSV file:
        name,age,city
        Alice,30,NYC
        Bob,25,LA
    
    >>> read_csv_dict("data.csv")
    [{'name': 'Alice', 'age': '30', 'city': 'NYC'}, 
     {'name': 'Bob', 'age': '25', 'city': 'LA'}]
    
    File doesn't exist:
    >>> read_csv_dict("missing.csv")
    None
    
    Empty file:
    >>> read_csv_dict("empty.csv")
    []

Input Validation:
    - You may assume filepath is a valid string
    - Return None for non-existent files

Implementation Hint:
    - Use csv.DictReader()
    - Convert reader to list to return all rows

"""

from __future__ import annotations

import csv


def read_csv_dict(filepath: str) -> list[dict[str, str]] | None:
    """Read a CSV file and return as list of dictionaries.

    Args:
        filepath: Path to the CSV file.

    Returns:
        List of dictionaries, or None if file not found.
    """
    raise NotImplementedError("Implement read_csv_dict")
