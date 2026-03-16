"""Reference solution for Problem 06: CSV Column Sum."""

from __future__ import annotations

import csv
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
    path = Path(filepath)
    
    if not path.exists():
        return 0.0
    
    total = 0.0
    column_exists = False
    
    with open(path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            if column_name not in row:
                return 0.0
            
            column_exists = True
            value = row[column_name]
            
            try:
                total += float(value)
            except ValueError:
                # Skip non-numeric values
                continue
    
    return total if column_exists else 0.0
