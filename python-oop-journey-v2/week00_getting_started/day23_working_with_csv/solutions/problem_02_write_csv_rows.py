"""Reference solution for Problem 02: Write CSV Rows."""

from __future__ import annotations

import csv


def write_csv_rows(filepath: str, rows: list[list[str]]) -> bool:
    """Write rows to a CSV file.

    Args:
        filepath: Path to the CSV file to write.
        rows: List of rows, where each row is a list of strings.

    Returns:
        True if write was successful, False otherwise.
    """
    try:
        with open(filepath, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        return True
    except (PermissionError, IOError):
        return False
