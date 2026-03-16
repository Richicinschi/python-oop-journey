"""Problem 03: Safe File Reader with Statistics

Topic: File I/O, error handling, statistics
Difficulty: Medium

Create a safe file reader that reads numeric data from a file and computes
statistics, handling all potential errors gracefully.

Required functions:
- read_numbers_from_file(filepath): Read numbers, skip invalid lines
- compute_file_stats(filepath): Return statistics dict or error info

File format:
- One number per line (int or float)
- Empty lines should be skipped
- Lines with non-numeric content should be skipped

Error handling:
- FileNotFoundError: Return appropriate error message
- PermissionError: Return appropriate error message
- Empty file: Return stats with zeros/empty values

Statistics to compute:
- count: Number of valid numbers read
- sum: Sum of all numbers
- average: Mean of numbers
- min: Minimum value
- max: Maximum value
- invalid_lines: Count of lines that couldn't be parsed

Example file content:
    10
    20.5
    
    abc
    30

Should process: 10, 20.5, 30 (skipping empty and "abc")
"""

from __future__ import annotations


def read_numbers_from_file(filepath: str) -> list[float]:
    """Read numeric data from a file, skipping invalid lines.

    Args:
        filepath: Path to the file to read

    Returns:
        List of valid numbers found in the file

    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If file cannot be read
    """
    raise NotImplementedError("Implement read_numbers_from_file")


def compute_file_stats(filepath: str) -> dict:
    """Compute statistics from a numeric file.

    Args:
        filepath: Path to the file to analyze

    Returns:
        Dictionary with keys:
            - success: Boolean indicating if operation succeeded
            - count: Number of valid numbers
            - sum: Sum of numbers (0 if none)
            - average: Mean of numbers (None if none)
            - min: Minimum value (None if none)
            - max: Maximum value (None if none)
            - invalid_lines: Count of unparsable lines
            - error: Error message if file couldn't be read
    """
    raise NotImplementedError("Implement compute_file_stats")
