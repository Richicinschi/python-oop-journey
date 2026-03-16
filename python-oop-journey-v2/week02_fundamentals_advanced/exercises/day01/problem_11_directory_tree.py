"""Problem 11: Directory Tree

Topic: pathlib, recursion
Difficulty: Medium

Write a function that generates a directory tree structure as a string,
similar to the Unix 'tree' command. Only include files matching given patterns.

Examples:
    >>> print(directory_tree(".", include=["*.py"]))
    .
    ├── file1.py
    └── subdir
        └── file2.py
    
    2 files, 1 directories
    >>> directory_tree("nonexistent")
    ""

Requirements:
    - Return empty string for non-existent directories
    - Use Unicode box-drawing characters: ├──, └──, │
    - Show file/directory count summary at the end
    - include parameter is a list of glob patterns (e.g., ["*.py", "*.txt"])
    - If include is empty, include all files
    - Sort entries alphabetically (directories first, then files)
    - Each level is indented with 4 spaces
"""

from __future__ import annotations

from pathlib import Path


def directory_tree(
    root_path: str | Path, 
    include: list[str] | None = None
) -> str:
    """Generate a directory tree structure as a string.

    Args:
        root_path: Path to the root directory.
        include: List of glob patterns to include (e.g., ["*.py"]).
                 If None or empty, include all files.

    Returns:
        String representation of the directory tree, or empty string
        if root_path doesn't exist.
    """
    raise NotImplementedError("Implement directory_tree")
