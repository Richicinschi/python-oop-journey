"""Reference solution for Problem 03: Read CSV as Dict."""

from __future__ import annotations

import csv


def read_csv_dict(filepath: str) -> list[dict[str, str]] | None:
    """Read CSV file as a list of dictionaries using DictReader.

    Args:
        filepath: Path to the CSV file.

    Returns:
        A list of dictionaries where keys are column headers,
        or None if the file doesn't exist.
    """
    try:
        with open(filepath, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        return None
