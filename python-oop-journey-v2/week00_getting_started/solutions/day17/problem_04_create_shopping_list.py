"""Problem 04: Create Shopping List - Solution."""

from __future__ import annotations


def create_shopping_list(
    item: str,
    items: list[str] | None = None,
) -> list[str]:
    """Add an item to a shopping list.

    IMPORTANT: Do NOT use a mutable default value for items parameter.
    Use None as the default and create a new list inside the function.

    Args:
        item: The item to add to the list.
        items: Existing list of items (optional). If None, create new list.

    Returns:
        The updated shopping list with the new item added.
    """
    if items is None:
        items = []
    items.append(item)
    return items
