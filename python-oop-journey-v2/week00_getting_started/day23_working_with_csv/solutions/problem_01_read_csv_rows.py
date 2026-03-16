"""Reference solution for Problem 01: Read CSV Rows."""

from __future__ import annotations

import csv


def read_csv_rows(filepath: str) -> list[list[str]] | None:
    """Read all rows from a CSV file.

    Args:
        filepath: Path to the CSV file.

    Returns:
        A list of rows, where each row is a list of strings,
        or None if the file doesn't exist.
    """
    try:
        with open(filepath, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            return list(reader)
    except FileNotFoundError:
        return None
