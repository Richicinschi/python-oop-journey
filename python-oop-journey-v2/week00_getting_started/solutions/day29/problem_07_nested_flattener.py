"""Reference solution for Problem 07: Nested Data Flattener."""

from __future__ import annotations


def flatten_list(nested: list) -> list:
    """Flatten a nested list structure to a single level.

    Args:
        nested: A list potentially containing nested lists

    Returns:
        Flattened list with all non-list elements
    """
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result


def flatten_dict(nested: dict, prefix: str = "") -> dict[str, any]:
    """Flatten a nested dictionary using dot notation for keys.

    Args:
        nested: A potentially nested dictionary
        prefix: Prefix for keys (used in recursion)

    Returns:
        Flattened dictionary with dot-separated keys
    """
    result = {}
    for key, value in nested.items():
        new_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            result.update(flatten_dict(value, new_key))
        else:
            result[new_key] = value
    return result


def flatten_mixed(data: list) -> list:
    """Flatten list structures, preserving non-list items.

    Flattens nested lists but keeps dictionaries and other types as-is.

    Args:
        data: A list potentially containing nested lists and other types

    Returns:
        List with nested lists flattened, other types preserved
    """
    result = []
    for item in data:
        if isinstance(item, list):
            result.extend(flatten_mixed(item))
        else:
            result.append(item)
    return result
