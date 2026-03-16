"""Reference solution for Problem 10: Zigzag Conversion."""

from __future__ import annotations


def zigzag_conversion(s: str, num_rows: int) -> str:
    """Convert a string to zigzag pattern and read row by row.
    
    Uses a list of strings to represent each row. Characters are distributed
    by calculating which row they belong to based on the zigzag pattern cycle.
    
    Args:
        s: The input string.
        num_rows: The number of rows in the zigzag pattern.
        
    Returns:
        The string read row by row from the zigzag pattern.
    """
    # Edge cases
    if num_rows == 1 or num_rows >= len(s):
        return s
    
    # Create a list for each row
    rows: list[list[str]] = [[] for _ in range(num_rows)]
    
    # Track current row and direction
    current_row = 0
    going_down = False
    
    for char in s:
        rows[current_row].append(char)
        
        # Change direction at the top or bottom row
        if current_row == 0 or current_row == num_rows - 1:
            going_down = not going_down
        
        # Move to next row
        current_row += 1 if going_down else -1
    
    # Concatenate all rows
    return "".join("".join(row) for row in rows)
