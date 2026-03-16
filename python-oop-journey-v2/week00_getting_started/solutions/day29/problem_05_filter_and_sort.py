"""Reference solution for Problem 05: Filter and Sort Mixed Data."""

from __future__ import annotations


def filter_by_type(data: list, type_: type) -> list:
    """Filter list to include only items of the specified type.

    Args:
        data: Mixed list of items
        type_: The type to filter for

    Returns:
        List containing only items of the specified type
    """
    return [item for item in data if isinstance(item, type_)]


def sort_mixed_numbers(data: list) -> list[int | float]:
    """Extract and sort all numeric values from mixed data.

    Args:
        data: Mixed list containing numbers and other types

    Returns:
        Sorted list of all int and float values (ascending)
    """
    numbers = [item for item in data if isinstance(item, (int, float))]
    return sorted(numbers)


def find_extremes(data: list) -> tuple[int | float | None, int | float | None]:
    """Find minimum and maximum numeric values.

    Args:
        data: Mixed list containing numbers and other types

    Returns:
        Tuple of (min, max) numeric values, or (None, None) if no numbers
    """
    numbers = [item for item in data if isinstance(item, (int, float))]
    if not numbers:
        return None, None
    return min(numbers), max(numbers)


def group_by_type(data: list) -> dict[str, list]:
    """Group items by their type name.

    Args:
        data: Mixed list of items

    Returns:
        Dictionary with type names as keys, lists of items as values
    """
    result: dict[str, list] = {}
    for item in data:
        type_name = type(item).__name__
        if type_name not in result:
            result[type_name] = []
        result[type_name].append(item)
    return result
