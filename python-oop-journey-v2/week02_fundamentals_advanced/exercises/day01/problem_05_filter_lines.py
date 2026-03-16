"""Problem 05: Filter Lines

Topic: File I/O - Pattern matching
Difficulty: Medium

Write a function that filters lines from a file based on a pattern.
Lines containing the pattern are written to the output file.

Examples:
    >>> filter_lines("log.txt", "output.txt", "ERROR")
    5  # number of matching lines written
    >>> filter_lines("log.txt", "output.txt", "NONEXISTENT")
    0

Requirements:
    - Pattern matching is case-sensitive
    - Return count of lines written to output
    - Create empty output file if no lines match
    - Handle non-existent input file by returning -1
    - Preserve original line endings (newlines)
"""

from __future__ import annotations

from pathlib import Path


def filter_lines(
    input_file: str | Path, 
    output_file: str | Path, 
    pattern: str
) -> int:
    """Filter lines containing pattern from input to output file.

    Args:
        input_file: Path to the input file.
        output_file: Path to the output file.
        pattern: String pattern to search for in each line.

    Returns:
        Number of matching lines written, or -1 if input file doesn't exist.
    """
    raise NotImplementedError("Implement filter_lines")
