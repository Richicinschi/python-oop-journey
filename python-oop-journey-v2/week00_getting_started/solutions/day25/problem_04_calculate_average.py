"""Reference solution for Problem 04: Calculate Average."""

from __future__ import annotations


def calculate_average(numbers: list) -> float:
    """Calculate the average of a list of numbers.

    Args:
        numbers: A list containing numbers (and possibly other types)

    Returns:
        The average as a float, or 0 if no valid numbers
    """
    if not numbers:
        return 0.0
    
    valid_numbers = []
    for item in numbers:
        try:
            # Check if it's a number (int or float, but not bool)
            if isinstance(item, (int, float)) and not isinstance(item, bool):
                valid_numbers.append(float(item))
        except (TypeError, ValueError):
            continue
    
    if not valid_numbers:
        return 0.0
    
    return sum(valid_numbers) / len(valid_numbers)
