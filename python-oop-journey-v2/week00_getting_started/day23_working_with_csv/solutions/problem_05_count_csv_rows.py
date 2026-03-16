"""Reference solution for Problem 05: Count CSV Rows."""

from __future__ import annotations

import csv


def count_csv_rows(filepath: str, has_header: bool = True) -> int | None:
    """Count the number of data rows in a CSV file.

    Args:
        filepath: Path to the CSV file.
        has_header: If True, subtract 1 to exclude header row.

    Returns:
        The number of data rows, or None if file doesn't exist.
    """
    try:
        with open(filepath, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)
            count = len(rows)
            if has_header and count > 0:
                count -= 1
            return count
    except FileNotFoundError:
        return None
