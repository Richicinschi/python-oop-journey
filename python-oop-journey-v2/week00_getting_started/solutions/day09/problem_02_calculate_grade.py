"""Reference solution for Problem 02: Calculate Grade."""

from __future__ import annotations


def calculate_grade(score: int) -> str:
    """Convert numerical score to letter grade.

    Args:
        score: Numerical score (0-100)

    Returns:
        Letter grade: 'A', 'B', 'C', 'D', or 'F'
    """
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"
