"""Reference solution for Problem 03: Safe File Reader with Statistics."""

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
    numbers = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                numbers.append(float(line))
            except ValueError:
                continue
    return numbers


def compute_file_stats(filepath: str) -> dict:
    """Compute statistics from a numeric file.

    Args:
        filepath: Path to the file to analyze

    Returns:
        Dictionary with file statistics
    """
    result = {
        "success": False,
        "count": 0,
        "sum": 0.0,
        "average": None,
        "min": None,
        "max": None,
        "invalid_lines": 0,
        "error": None,
    }

    try:
        numbers = []
        invalid_count = 0

        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    numbers.append(float(line))
                except ValueError:
                    invalid_count += 1

        result["invalid_lines"] = invalid_count

        if not numbers:
            return None

        result["success"] = True
        result["count"] = len(numbers)
        result["sum"] = sum(numbers)
        result["average"] = sum(numbers) / len(numbers)
        result["min"] = min(numbers)
        result["max"] = max(numbers)

    except FileNotFoundError:
        result["error"] = f"File not found: {filepath}"
    except PermissionError:
        result["error"] = f"Permission denied: {filepath}"
    except Exception as e:
        result["error"] = str(e)

    return result
