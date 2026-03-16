"""Reference solution for Problem 01: Tuple Unpacking."""

from __future__ import annotations


def unpack_coordinates(point: tuple[int, int]) -> dict[str, int]:
    """Unpack a 2D coordinate tuple into a dictionary.

    Args:
        point: A tuple containing (x, y) coordinates

    Returns:
        A dictionary with keys 'x' and 'y'
    """
    x, y = point
    return {"x": x, "y": y}
