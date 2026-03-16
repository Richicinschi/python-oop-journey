"""Reference solution for Problem 10: Lazy Filter Map."""

from __future__ import annotations
from typing import Callable, Generator, TypeVar

T = TypeVar("T")
U = TypeVar("U")


def lazy_filter_map(
    data: list[T],
    predicate: Callable[[T], bool],
    transform: Callable[[T], U],
) -> Generator[U, None, None]:
    """Lazily filter and then transform data.

    Creates a generator pipeline using generator expression.
    Operations are performed on-demand, one item at a time.

    Args:
        data: The input data list.
        predicate: A function that returns True for items to keep.
        transform: A function to transform each kept item.

    Yields:
        Transformed values for items that passed the filter.
    """
    return (transform(item) for item in data if predicate(item))
