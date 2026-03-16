"""Problem 04: Merge Files

Topic: File I/O - Multiple file operations
Difficulty: Medium

Write a function that merges multiple text files into one output file.
Each file's content should be separated by a blank line.

Examples:
    >>> merge_files(["a.txt", "b.txt"], "output.txt")
    2  # number of files successfully merged
    >>> merge_files([], "output.txt")
    0
    >>> merge_files(["nonexistent.txt"], "output.txt")
    0

Requirements:
    - Skip files that don't exist (don't raise errors)
    - Return count of successfully merged files
    - Separate each file's content with a single blank line
    - Create output file if it doesn't exist, overwrite if it does
    - If all source files are empty or don't exist, create empty output file
"""

from __future__ import annotations

from pathlib import Path


def merge_files(source_files: list[str | Path], output_file: str | Path) -> int:
    """Merge multiple text files into one output file.

    Args:
        source_files: List of paths to source files.
        output_file: Path to the output file.

    Returns:
        Number of files successfully merged (existing files only).
    """
    raise NotImplementedError("Implement merge_files")
