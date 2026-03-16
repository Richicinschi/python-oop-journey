"""Problem 03: Pure Counter

Topic: Variable Scope - Pure Functions
Difficulty: Easy

Write a pure function that increments a counter without side effects.

Function Signature:
    def pure_counter(current: int, increment: int = 1) -> int

Requirements:
    - Return current + increment
    - Do NOT modify any external state
    - Same inputs always produce same outputs

Behavior Notes:
    - Pure functions have no side effects
    - They don't modify global variables
    - They don't modify mutable arguments
    - They only use their parameters

Examples:
    >>> pure_counter(5)
    6
    
    >>> pure_counter(10, 3)
    13
    
    >>> pure_counter(0, 5)
    5
    
    Multiple calls produce same result:
    >>> pure_counter(5, 2)
    7
    >>> pure_counter(5, 2)
    7  # Same result every time

Input Validation:
    - You may assume current and increment are integers

"""

from __future__ import annotations


def pure_counter(current: int, increment: int = 1) -> int:
    """Increment a counter purely (no side effects).

    Args:
        current: The current counter value.
        increment: How much to increment (default 1).

    Returns:
        The new counter value (current + increment).
    """
    raise NotImplementedError("Implement pure_counter")
