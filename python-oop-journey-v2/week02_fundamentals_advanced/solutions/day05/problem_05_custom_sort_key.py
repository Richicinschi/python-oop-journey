"""Problem 05: Custom Sort Key - Solution

Implement custom sorting functionality using key functions
to sort complex data structures in various ways.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional, TypeVar

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
    def combined_key(item: T) -> tuple:
        return tuple(key_func(item) for key_func in key_funcs)

    return sorted(items, key=combined_key)


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
    if reverse_flags is None:
        reverse_flags = [False] * len(key_funcs)

    def sort_key(item: T) -> tuple:
        keys = []
        for key_func, reverse in zip(key_funcs, reverse_flags):
            value = key_func(item)
            # For reverse sorting, we negate numeric values or use a trick for strings
            if reverse:
                if isinstance(value, (int, float)):
                    keys.append(-value)
                else:
                    # For strings, we can't negate, so we use a workaround
                    # by creating a sortable representation
                    keys.append((True, value))
            else:
                if isinstance(value, (int, float)):
                    keys.append(value)
                else:
                    keys.append((False, value))
        return tuple(keys)

    return sort_key


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
    query_lower = query.lower()

    def relevance_key(product: Product) -> tuple[int, float]:
        name_lower = product.name.lower()
        category_lower = product.category.lower()

        if name_lower.startswith(query_lower):
            score = 0
        elif query_lower in name_lower:
            score = 1
        elif category_lower == query_lower:
            score = 2
        else:
            score = 3

        return (score, product.price)

    return sorted(products, key=relevance_key)


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
    sorted_items = sorted(items, key=key_func, reverse=reverse)
    return sorted_items[:n]
