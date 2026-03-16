"""Problem 05: Parameter Scope

Topic: Variable Scope - Parameters vs Local Variables
Difficulty: Easy

Write a function that demonstrates parameter and local variable scope.

Function Signature:
    def calculate_area_with_margin(width: int, height: int, margin: int = 0) -> int

Requirements:
    - Calculate area as (width + margin) * (height + margin)
    - Create a local variable to store the result
    - Return the result

Behavior Notes:
    - Parameters are like local variables initialized with argument values
    - Local variables exist only during function execution
    - Modifying parameters doesn't affect the caller

Examples:
    >>> calculate_area_with_margin(5, 3)
    15  # (5+0) * (3+0)
    
    >>> calculate_area_with_margin(5, 3, 1)
    24  # (5+1) * (3+1)
    
    >>> calculate_area_with_margin(10, 10, 5)
    225  # (10+5) * (10+5)

Input Validation:
    - You may assume all arguments are non-negative integers

"""

from __future__ import annotations


def calculate_area_with_margin(width: int, height: int, margin: int = 0) -> int:
    """Calculate area with added margin.

    Args:
        width: Base width.
        height: Base height.
        margin: Extra space to add to each dimension (default 0).

    Returns:
        The calculated area.
    """
    raise NotImplementedError("Implement calculate_area_with_margin")
