"""Reference solution for Problem 08: Analyze Log."""

from __future__ import annotations

from pathlib import Path


def analyze_log(filepath: str | Path) -> dict[str, int]:
    """Analyze a log file and return level statistics.

    Args:
        filepath: Path to the log file.

    Returns:
        Dictionary with counts for ERROR, WARNING, INFO, DEBUG,
        total_lines, and unknown_lines. Returns dict with all zeros
        for non-existent files.
    """
    path = Path(filepath)
    
    result = {
        'ERROR': 0,
        'WARNING': 0,
        'INFO': 0,
        'DEBUG': 0,
        'total_lines': 0,
        'unknown_lines': 0
    }
    
    if not path.exists():
        return result
    
    levels = ['ERROR', 'WARNING', 'INFO', 'DEBUG']
    
    with open(path, 'r') as f:
        for line in f:
            result['total_lines'] += 1
            line_stripped = line.strip()
            
            if not line_stripped:
                result['unknown_lines'] += 1
                continue
            
            matched = False
            for level in levels:
                upper_line = line_stripped.upper()
                # Check if line starts with level followed by space, colon, or hyphen
                if upper_line.startswith(level):
                    remainder = line_stripped[len(level):]
                    if remainder and remainder[0] in (' ', ':', '-'):
                        result[level] += 1
                        matched = True
                        break
                    elif not remainder:  # Line is exactly the level
                        result[level] += 1
                        matched = True
                        break
            
            if not matched:
                result['unknown_lines'] += 1
    
    return result
