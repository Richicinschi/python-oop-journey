"""Problem 04: Debug Values

Topic: Debugging Basics
Difficulty: Medium

Write a function that simulates debugging by tracking how a value
changes through a series of operations.

Given a starting value and a list of operations, return the value
after each operation along with the operation name.

Operations:
- "add_X": add X to the value
- "sub_X": subtract X from the value
- "mul_X": multiply value by X
- "div_X": divide value by X (integer division)

Return a list of tuples: (operation, value_after)

Examples:
    >>> debug_operations(10, ["add_5", "mul_2"])
    [('add_5', 15), ('mul_2', 30)]
    >>> debug_operations(100, ["sub_20", "div_4"])
    [('sub_20', 80), ('div_4', 20)]

Requirements:
    - Apply each operation in order
    - Return list of (operation, result) tuples
    - Use integer division for div operations
    - If division by zero would occur, stop and return current results
"""

from __future__ import annotations


def debug_operations(start: int, operations: list) -> list:
    """Track value changes through a series of operations.

    Args:
        start: The starting value
        operations: List of operation strings

    Returns:
        List of (operation, value_after) tuples
    """
    raise NotImplementedError("Implement debug_operations")
