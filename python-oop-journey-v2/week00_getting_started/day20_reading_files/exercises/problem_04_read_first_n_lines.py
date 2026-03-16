"""Problem 04: Read First N Lines

Topic: File I/O - Partial Reading
Difficulty: Easy

Write a function that reads the first n lines of a file.

Function Signature:
    def read_first_n_lines(filepath: str, n: int) -> list[str] | None

Requirements:
    - Return a list of the first n lines from the file
    - Return None if the file does not exist
    - If n is greater than total lines, return all lines
    - If n is 0 or negative, return an empty list []
    - Remove trailing newlines from each line

Behavior Notes:
    - Each line in the returned list should not have trailing '\n'
    - Lines should be in the same order as in the file
    - Handle edge cases: n=0, n<0, n>total_lines

Examples:
    File with 5 lines, requesting first 3:
    >>> read_first_n_lines("five_lines.txt", 3)
    ['Line 1', 'Line 2', 'Line 3']
    
    Requesting 10 lines from a 5-line file:
    >>> read_first_n_lines("five_lines.txt", 10)
    ['Line 1', 'Line 2', 'Line 3', 'Line 4', 'Line 5']
    
    n = 0:
    >>> read_first_n_lines("any.txt", 0)
    []
    
    File doesn't exist:
    >>> read_first_n_lines("missing.txt", 5)
    None

Input Validation:
    - You may assume filepath is a valid string
    - n may be any integer (positive, zero, or negative)

"""

from __future__ import annotations


def read_first_n_lines(filepath: str, n: int) -> list[str] | None:
    """Read the first n lines of a file.

    Args:
        filepath: Path to the file to read.
        n: Number of lines to read.

    Returns:
        List of lines (without trailing newlines), or None if file doesn't exist.
    """
    raise NotImplementedError("Implement read_first_n_lines")
