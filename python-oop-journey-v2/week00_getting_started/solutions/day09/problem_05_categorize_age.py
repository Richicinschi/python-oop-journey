"""Reference solution for Problem 05: Categorize Age."""

from __future__ import annotations


def categorize_age(age: int) -> str:
    """Categorize a person by age.

    Args:
        age: Age in years

    Returns:
        Category string: 'infant', 'toddler', 'child', 'teenager', 'adult', or 'senior'
    """
    if age <= 1:
        return "infant"
    elif age <= 3:
        return "toddler"
    elif age <= 12:
        return "child"
    elif age <= 19:
        return "teenager"
    elif age <= 64:
        return "adult"
    else:
        return "senior"
