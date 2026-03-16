"""Problem 05: Filter and Sort Mixed Data

Topic: Lists, sorting, filtering, type checking
Difficulty: Medium

Create functions to filter and sort mixed data types intelligently.

Required functions:
- filter_by_type(data, type_): Filter list to items of specific type
- sort_mixed_numbers(data): Sort numeric values, exclude non-numeric
- find_extremes(data): Find min and max of numeric values
- group_by_type(data): Group items by their type name

Rules:
- filter_by_type: Return only items matching the exact type
- sort_mixed_numbers: Extract all numbers (int, float), sort ascending
- find_extremes: Return (min, max) for numeric values, or (None, None)
- group_by_type: Return dict with type names as keys, lists as values

Example:
    >>> data = [1, "hello", 3.5, "world", 2, None, 4.0]
    >>> filter_by_type(data, int)
    [1, 2]
    >>> sort_mixed_numbers(data)
    [1, 2, 3.5, 4.0]
    >>> find_extremes(data)
    (1, 4.0)
    >>> group_by_type(data)
    {'int': [1, 2], 'str': ['hello', 'world'], 'float': [3.5, 4.0], 'NoneType': [None]}
"""

from __future__ import annotations


def filter_by_type(data: list, type_: type) -> list:
    """Filter list to include only items of the specified type.

    Args:
        data: Mixed list of items
        type_: The type to filter for

    Returns:
        List containing only items of the specified type
    """
    raise NotImplementedError("Implement filter_by_type")


def sort_mixed_numbers(data: list) -> list[int | float]:
    """Extract and sort all numeric values from mixed data.

    Args:
        data: Mixed list containing numbers and other types

    Returns:
        Sorted list of all int and float values (ascending)
    """
    raise NotImplementedError("Implement sort_mixed_numbers")


def find_extremes(data: list) -> tuple[int | float | None, int | float | None]:
    """Find minimum and maximum numeric values.

    Args:
        data: Mixed list containing numbers and other types

    Returns:
        Tuple of (min, max) numeric values, or (None, None) if no numbers
    """
    raise NotImplementedError("Implement find_extremes")


def group_by_type(data: list) -> dict[str, list]:
    """Group items by their type name.

    Args:
        data: Mixed list of items

    Returns:
        Dictionary with type names as keys, lists of items as values
    """
    raise NotImplementedError("Implement group_by_type")
