"""Reference solution for Problem 04: Merge Files."""

from __future__ import annotations

from pathlib import Path
from typing import List


def merge_files(source_files: list[str | Path], output_file: str | Path) -> int:
    """Merge multiple text files into one output file.

    Args:
        source_files: List of paths to source files.
        output_file: Path to the output file.

    Returns:
        Number of files successfully merged (existing files only).
    """
    output_path = Path(output_file)
    merged_count = 0
    first_file = True
    
    with open(output_path, 'w') as out_f:
        for source in source_files:
            source_path = Path(source)
            if not source_path.exists():
                continue
            
            # Add blank line separator between files (not before first)
            if not first_file:
                out_f.write('\n')
            first_file = False
            
            with open(source_path, 'r') as in_f:
                content = in_f.read()
                out_f.write(content)
            
            merged_count += 1
    
    return merged_count
