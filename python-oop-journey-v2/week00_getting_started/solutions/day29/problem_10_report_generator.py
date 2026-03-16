"""Reference solution for Problem 10: Report Generator."""

from __future__ import annotations

import csv
import os


def format_table(headers: list[str], rows: list[list[str]]) -> str:
    """Format data as an aligned text table.

    Args:
        headers: Column headers
        rows: List of row data

    Returns:
        Formatted table string with aligned columns
    """
    if not headers:
        return ""

    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))

    # Format header
    header_cells = [headers[i].ljust(col_widths[i]) for i in range(len(headers))]
    header_line = " | ".join(header_cells)

    # Format separator
    separator_cells = ["-" * col_widths[i] for i in range(len(headers))]
    separator_line = "-+-".join(separator_cells)

    # Format rows
    row_lines = []
    for row in rows:
        row_cells = [
            str(row[i]).ljust(col_widths[i]) if i < len(row) else " " * col_widths[i]
            for i in range(len(headers))
        ]
        row_lines.append(" | ".join(row_cells))

    return "\n".join([header_line, separator_line] + row_lines)


def generate_summary_report(title: str, data: dict[str, list[int]]) -> str:
    """Generate a text summary report from data.

    Args:
        title: Report title
        data: Dictionary mapping category names to lists of values

    Returns:
        Formatted multi-line report string
    """
    lines = [f"=== {title} ===", ""]
    
    if not data:
        return "\n".join(lines)
    
    for category, values in data.items():
        total = sum(values)
        lines.append(f"{category}: Total={total}")
    
    return "\n".join(lines)


def generate_statistics_report(title: str, values: list[int | float]) -> str:
    """Generate a statistics report for a list of numbers.

    Args:
        title: Report title
        values: List of numeric values

    Returns:
        Formatted statistics report string
    """
    lines = [f"=== {title} ===", ""]
    
    if not values:
        lines.append("No data available (N/A)")
        return "\n".join(lines)
    
    count = len(values)
    total = sum(values)
    average = total / count
    min_val = min(values)
    max_val = max(values)
    
    lines.append(f"Count: {count}")
    lines.append(f"Sum: {total}")
    lines.append(f"Average: {average:.2f}")
    lines.append(f"Min: {min_val}")
    lines.append(f"Max: {max_val}")
    
    return "\n".join(lines)


def generate_csv_report(filepath: str, headers: list[str], rows: list[list[str]]) -> bool:
    """Write data to a CSV file.

    Args:
        filepath: Path to output CSV file
        headers: Column headers
        rows: List of row data

    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        return True
    except (IOError, OSError, PermissionError):
        return False
