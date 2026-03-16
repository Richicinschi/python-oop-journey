"""Problem 01: Trace Debug

Topic: Debugging Basics
Difficulty: Easy

Write a function that traces the execution of a simple calculation.

The function should return a list showing the values at each step:
1. Initial value
2. After first operation
3. After second operation
4. Final result

This simulates what you'd see with print debugging.

Examples:
    >>> trace_calculation(5)
    ['start: 5', 'after_add: 10', 'after_multiply: 20', 'final: 20']

The calculation steps are:
1. Start with input value
2. Add 5
3. Multiply by 2
4. Return result

Requirements:
    - Return a list of strings showing each step
    - Format: "step_name: value"
"""

from __future__ import annotations


def trace_calculation(value: int) -> list:
    """Trace a calculation and return debug information.

    Args:
        value: The starting value

    Returns:
        A list of trace strings
    """
    raise NotImplementedError("Implement trace_calculation")
