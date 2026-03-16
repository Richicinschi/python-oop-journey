"""Reference solution for Problem 02: Find Longest Line."""

from __future__ import annotations

from pathlib import Path


def find_longest_line(filepath: str | Path) -> tuple[str, int]:
    """Find the longest line in a text file.

    Args:
        filepath: Path to the text file.

    Returns:
        Tuple of (longest_line_content, line_number). Returns ('', 0) for
        empty or non-existent files. Line numbers are 1-based.
    """
    path = Path(filepath)
    
    if not path.exists():
        return ('', 0)
    
    longest_line = ''
    longest_number = 0
    
    with open(path, 'r') as f:
        for line_number, line in enumerate(f, start=1):
            content = line.rstrip('\n\r')
            if len(content) > len(longest_line):
                longest_line = content
                longest_number = line_number
    
    return (longest_line, longest_number)
