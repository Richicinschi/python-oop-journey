"""Reference solution for Problem 02: Append and Get Length."""

from __future__ import annotations


def append_and_count(items: list[str], new_item: str) -> tuple[list[str], int]:
    """Append a new item to the list and return the updated list and its length.

    Args:
        items: A list of strings
        new_item: The item to append

    Returns:
        A tuple containing (updated_list, new_length)
    """
    items.append(new_item)
    return items, len(items)
