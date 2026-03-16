"""Problem 02: Calculate Grade

Topic: If Statements, Elif chains
Difficulty: Easy

Write a function that converts a numerical score to a letter grade.

Grading scale:
    A: 90-100
    B: 80-89
    C: 70-79
    D: 60-69
    F: Below 60

Examples:
    >>> calculate_grade(95)
    'A'
    >>> calculate_grade(85)
    'B'
    >>> calculate_grade(75)
    'C'
    >>> calculate_grade(65)
    'D'
    >>> calculate_grade(55)
    'F'

Requirements:
    - Use if-elif-else chain
    - Assume score is between 0 and 100
"""

from __future__ import annotations


def calculate_grade(score: int) -> str:
    """Convert numerical score to letter grade.

    Args:
        score: Numerical score (0-100)

    Returns:
        Letter grade: 'A', 'B', 'C', 'D', or 'F'
    """
    raise NotImplementedError("Implement calculate_grade")
