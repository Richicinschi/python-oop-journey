"""Reference solution for Problem 11: Directory Tree."""

from __future__ import annotations

from pathlib import Path
from typing import List


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
    root = Path(root_path)
    
    if not root.exists() or not root.is_dir():
        return ""
    
    if include is None:
        include = []
    
    file_count = 0
    dir_count = 0
    lines: list[str] = []
    
    def _should_include(path: Path) -> bool:
        """Check if a file should be included based on patterns."""
        if not include or path.is_dir():
            return True
        for pattern in include:
            if path.match(pattern):
                return True
        return False
    
    def _tree(dir_path: Path, prefix: str = "") -> None:
        """Recursively build tree structure."""
        nonlocal file_count, dir_count
        
        # Get entries and sort (dirs first, then files)
        try:
            entries = sorted(dir_path.iterdir(), 
                           key=lambda p: (not p.is_dir(), p.name.lower()))
        except (PermissionError, OSError):
            return
        
        # Filter files based on include patterns
        filtered_entries = []
        for entry in entries:
            if entry.is_dir():
                filtered_entries.append(entry)
            elif _should_include(entry):
                filtered_entries.append(entry)
        
        for i, entry in enumerate(filtered_entries):
            is_last = i == len(filtered_entries) - 1
            
            if entry.is_dir():
                dir_count += 1
                connector = "└── " if is_last else "├── "
                lines.append(f"{prefix}{connector}{entry.name}")
                
                extension = "    " if is_last else "│   "
                _tree(entry, prefix + extension)
            else:
                file_count += 1
                connector = "└── " if is_last else "├── "
                lines.append(f"{prefix}{connector}{entry.name}")
    
    # Start with root name
    lines.append(root.name)
    _tree(root)
    
    # Add summary
    lines.append("")
    lines.append(f"{file_count} file{'s' if file_count != 1 else ''}, "
                f"{dir_count} director{'ies' if dir_count != 1 else 'y'}")
    
    return "\n".join(lines)
