"""Reference solution for Problem 04: Write CSV from Dict."""

from __future__ import annotations

import csv


def write_csv_dict(
    filepath: str, data: list[dict[str, str]], fieldnames: list[str]
) -> bool:
    """Write a list of dictionaries to a CSV file.

    Args:
        filepath: Path to the CSV file to write.
        data: List of dictionaries to write.
        fieldnames: List of field names (column headers).

    Returns:
        True if write was successful, False otherwise.
    """
    try:
        with open(filepath, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        return True
    except (PermissionError, IOError):
        return False
