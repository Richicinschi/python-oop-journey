"""Reference solution for Problem 09: Chunked Iterator."""

from __future__ import annotations
from typing import Generator, TypeVar

T = TypeVar("T")


def chunked_iterator(iterable: list[T], chunk_size: int) -> Generator[list[T], None, None]:
    """Yield successive chunks of a specified size from an iterable.

    Uses a generator to yield chunks lazily. Validates chunk_size
    and yields remaining items in the final chunk.

    Args:
        iterable: A list of items to chunk.
        chunk_size: The size of each chunk (must be positive).

    Yields:
        Lists containing up to chunk_size items each.

    Raises:
        ValueError: If chunk_size is not positive.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    for i in range(0, len(iterable), chunk_size):
        yield iterable[i : i + chunk_size]
