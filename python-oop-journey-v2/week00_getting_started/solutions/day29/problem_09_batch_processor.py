"""Reference solution for Problem 09: Batch Processor with Error Handling."""

from __future__ import annotations
from typing import Callable


def process_batch(items: list, processor: Callable) -> dict:
    """Process a batch of items with individual error handling.

    Args:
        items: List of items to process
        processor: Function to apply to each item

    Returns:
        Dictionary with success, failed, and stats
    """
    success = []
    failed = []

    for item in items:
        try:
            result = processor(item)
            success.append((item, result))
        except Exception as e:
            failed.append((item, f"{type(e).__name__}: {e}"))

    return {
        "success": success,
        "failed": failed,
        "stats": {
            "total": len(items),
            "success_count": len(success),
            "failure_count": len(failed),
        },
    }


def safe_divide_batch(numbers: list[float], divisor: float) -> list[float | None]:
    """Safely divide all numbers by divisor.

    Args:
        numbers: List of numbers to divide
        divisor: Number to divide by

    Returns:
        List of results, with None for division by zero cases
    """
    if divisor == 0:
        return [None] * len(numbers)

    return [num / divisor for num in numbers]


def parse_int_batch(strings: list[str]) -> dict:
    """Parse multiple strings to integers.

    Args:
        strings: List of string representations of integers

    Returns:
        Dictionary with values, failed, and indices
    """
    values = []
    failed = []
    indices = []

    for i, s in enumerate(strings):
        try:
            values.append(int(s))
        except ValueError as e:
            failed.append((s, str(e)))
            indices.append(i)

    return {"values": values, "failed": failed, "indices": indices}


def batch_statistics(results: dict) -> dict:
    """Generate statistics from batch processing results.

    Args:
        results: Results dictionary from process_batch or similar

    Returns:
        Dictionary with statistics
    """
    stats = results.get("stats", {})
    total = stats.get("total", 0)
    success_count = stats.get("success_count", 0)

    if total == 0:
        return {"total": 0, "success_rate": 0.0, "failure_rate": 0.0}

    return {
        "total": total,
        "success_rate": round((success_count / total) * 100, 2),
        "failure_rate": round(((total - success_count) / total) * 100, 2),
    }
