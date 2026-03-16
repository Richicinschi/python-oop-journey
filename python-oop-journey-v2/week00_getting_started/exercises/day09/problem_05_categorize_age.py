"""Problem 05: Categorize Age

Topic: If Statements, Multiple conditions
Difficulty: Easy

Write a function that categorizes a person based on their age.

Age categories:
    Infant: 0-1 years
    Toddler: 2-3 years
    Child: 4-12 years
    Teenager: 13-19 years
    Adult: 20-64 years
    Senior: 65+ years

Examples:
    >>> categorize_age(0)
    'infant'
    >>> categorize_age(2)
    'toddler'
    >>> categorize_age(10)
    'child'
    >>> categorize_age(15)
    'teenager'
    >>> categorize_age(30)
    'adult'
    >>> categorize_age(70)
    'senior'

Requirements:
    - Use if-elif-else chain
    - Return lowercase category string
"""

from __future__ import annotations


def categorize_age(age: int) -> str:
    """Categorize a person by age.

    Args:
        age: Age in years

    Returns:
        Category string: 'infant', 'toddler', 'child', 'teenager', 'adult', or 'senior'
    """
    raise NotImplementedError("Implement categorize_age")
