"""Problem 02: Calculate Rectangle Area

Topic: Functions - Parameters and Return
Difficulty: Easy

Write a function that calculates the area of a rectangle.

Function Signature:
    def calculate_rectangle_area(width: float, height: float) -> float

Requirements:
    - Return the area (width * height)
    - Return 0 if either dimension is negative
    - Works with integers and floats

Behavior Notes:
    - Area = width * height
    - Negative dimensions are invalid (return 0)
    - Return type is float to handle decimal results

Examples:
    >>> calculate_rectangle_area(5.0, 3.0)
    15.0
    
    >>> calculate_rectangle_area(4, 4)
    16.0
    
    Negative width:
    >>> calculate_rectangle_area(-5.0, 3.0)
    0
    
    Negative height:
    >>> calculate_rectangle_area(5.0, -3.0)
    0

Input Validation:
    - You may assume width and height are numbers (int or float)
    - Return 0 for any negative dimension

"""

from __future__ import annotations


def calculate_rectangle_area(width: float, height: float) -> float:
    """Calculate the area of a rectangle.

    Args:
        width: The width of the rectangle.
        height: The height of the rectangle.

    Returns:
        The area (width * height), or 0 if any dimension is negative.
    """
    raise NotImplementedError("Implement calculate_rectangle_area")
