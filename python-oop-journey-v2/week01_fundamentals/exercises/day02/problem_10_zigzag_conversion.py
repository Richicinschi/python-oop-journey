"""Problem 10: Zigzag Conversion

Topic: Strings
Difficulty: Medium

The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this:

P   A   H   N
A P L S I I G
Y   I   R

And then read line by line: "PAHNAPLSIIGYIR"

Write the code that will take a string and make this conversion given a number of rows.
"""

from __future__ import annotations


def zigzag_conversion(s: str, num_rows: int) -> str:
    """Convert a string to zigzag pattern and read row by row.
    
    The string is written in a zigzag pattern going down and then up diagonally,
    then read row by row from top to bottom.
    
    Args:
        s: The input string.
        num_rows: The number of rows in the zigzag pattern.
        
    Returns:
        The string read row by row from the zigzag pattern.
        
    Examples:
        >>> zigzag_conversion("PAYPALISHIRING", 3)
        'PAHNAPLSIIGYIR'
        >>> zigzag_conversion("PAYPALISHIRING", 4)
        'PINALSIGYAHRPI'
        >>> zigzag_conversion("A", 1)
        'A'
        >>> zigzag_conversion("AB", 1)
        'AB'
        
    Note:
        If num_rows is 1 or greater/equal to string length, return string as is.
    """
    raise NotImplementedError("Implement zigzag_conversion")
