"""Reference solution for Problem 05: Filter Lines."""

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
    input_path = Path(input_file)
    output_path = Path(output_file)
    
    if not input_path.exists():
        return -1
    
    match_count = 0
    
    with open(input_path, 'r') as in_f, open(output_path, 'w') as out_f:
        for line in in_f:
            if pattern in line:
                out_f.write(line)
                match_count += 1
    
    return match_count
