"""Problem 05: Custom Sort Key

Implement custom sorting functionality using key functions
to sort complex data structures in various ways.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, TypeVar

T = TypeVar("T")


@dataclass
class Product:
    """A product with name, price, and category."""
    name: str
    price: float
    category: str


def sort_by_multiple_keys(
    items: list[T],
    *key_funcs: Callable[[T], str | int | float]
) -> list[T]:
    """Sort items by multiple key functions in order of priority.

    Args:
        items: List of items to sort.
        *key_funcs: Key functions, applied in order of priority.

    Returns:
        New list sorted by the key functions.

    Example:
        >>> items = [("b", 2), ("a", 1), ("a", 3)]
        >>> sort_by_multiple_keys(items, lambda x: x[0], lambda x: x[1])
        [("a", 1), ("a", 3), ("b", 2)]
    """
    raise NotImplementedError("Implement sort_by_multiple_keys")


def create_sort_key(
    *key_funcs: Callable[[T], str | int | float],
    reverse_flags: list[bool] | None = None
) -> Callable[[T], tuple]:
    """Create a composite sort key function.

    Args:
        *key_funcs: Functions to extract sort keys.
        reverse_flags: Optional list of booleans indicating reverse for each key.

    Returns:
        A function that returns a tuple of sort keys.

    Example:
        >>> data = [("a", 5), ("b", 3), ("a", 3)]
        >>> key = create_sort_key(lambda x: x[0], lambda x: x[1])
        >>> sorted(data, key=key)
        [("a", 3), ("a", 5), ("b", 3)]
    """
    raise NotImplementedError("Implement sort_by_multiple_keys")


def sort_products_by_relevance(
    products: list[Product],
    query: str
) -> list[Product]:
    """Sort products by relevance to a search query.

    Relevance score:
    - Name starts with query: score 0
    - Name contains query: score 1
    - Category matches query: score 2
    - No match: score 3

    Within same score, sort by price ascending.

    Args:
        products: List of products to sort.
        query: Search query string.

    Returns:
        Products sorted by relevance.
    """
    raise NotImplementedError("Implement sort_by_multiple_keys")


def get_top_n_by_criteria(
    items: list[T],
    n: int,
    key_func: Callable[[T], str | int | float],
    reverse: bool = True
) -> list[T]:
    """Get the top N items by a criteria.

    Args:
        items: List of items.
        n: Number of top items to return.
        key_func: Function to extract comparison key.
        reverse: If True, highest values first; else lowest first.

    Returns:
        List of top N items.
    """
    raise NotImplementedError("Implement sort_by_multiple_keys")
