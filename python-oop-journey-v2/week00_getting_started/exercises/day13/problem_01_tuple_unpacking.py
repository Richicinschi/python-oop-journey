"""Problem 01: Tuple Unpacking

Topic: Tuples - Unpacking
Difficulty: Easy

Write a function that unpacks a tuple into individual variables.

Function Signature:
    def unpack_coordinates(coords: tuple[float, float]) -> dict[str, float]

Requirements:
    - Unpack the tuple into x and y coordinates
    - Return a dictionary with keys 'x' and 'y'
    - Tuple always has exactly 2 elements

Behavior Notes:
    - Tuple unpacking: x, y = coords
    - Return dict with coordinate names
    - Tuple is immutable but unpacking creates new variables

Examples:
    >>> unpack_coordinates((3.5, 4.2))
    {'x': 3.5, 'y': 4.2}
    
    >>> unpack_coordinates((0.0, 0.0))
    {'x': 0.0, 'y': 0.0}
    
    Negative coordinates:
    >>> unpack_coordinates((-1.5, 2.5))
    {'x': -1.5, 'y': 2.5}

Input Validation:
    - You may assume coords is a tuple of exactly 2 floats
    - No need to handle invalid tuple sizes

"""

from __future__ import annotations


def unpack_coordinates(coords: tuple[float, float]) -> dict[str, float]:
    """Unpack a coordinate tuple into x and y values.

    Args:
        coords: A tuple of (x, y) coordinates.

    Returns:
        A dictionary with 'x' and 'y' keys.
    """
    raise NotImplementedError("Implement unpack_coordinates")
