"""Problem 09: Chunked Iterator

Topic: Generators, itertools, Batch Processing
Difficulty: Medium

Yield fixed-size chunks from an iterable, with the last chunk
containing any remaining items.

Hints:
    * Hint 1: Think of this as a sliding window that moves chunk_size
      elements at a time. You'll need to collect elements into a batch,
      yield when full, then start a new batch.
    
    * Hint 2: One approach using range/step:
      - Validate chunk_size is positive (raise ValueError if not)
      - Loop with for i in range(0, len(iterable), chunk_size):
        - Slice: iterable[i:i + chunk_size]
        - Yield the slice
    
    * Hint 3: Alternatively, use iter() with a sentinel:
      - Create an iterator from the list: it = iter(iterable)
      - While True: slice list(itertools.islice(it, chunk_size))
      - If slice is empty, break; else yield slice

Debugging Tips:
    - "Index out of range": Using indexing? Ensure your slice uses
      min() or Python's automatic slice clamping
    - "Only getting first chunk": Check your loop - are you breaking
      too early or not looping at all?
    - Empty chunks in output: Make sure to check for empty list before
      yielding, especially with the islice approach
    - Last chunk wrong size: This is expected for uneven divisions!
      The last chunk can have 1 to chunk_size elements
"""

from __future__ import annotations
from typing import Generator, TypeVar

T = TypeVar("T")


def chunked_iterator(iterable: list[T], chunk_size: int) -> Generator[list[T], None, None]:
    """Yield successive chunks of a specified size from an iterable.

    Args:
        iterable: A list of items to chunk.
        chunk_size: The size of each chunk (must be positive).

    Yields:
        Lists containing up to chunk_size items each.

    Raises:
        ValueError: If chunk_size is not positive.

    Example:
        >>> list(chunked_iterator([1, 2, 3, 4, 5, 6], 2))
        [[1, 2], [3, 4], [5, 6]]
        >>> list(chunked_iterator([1, 2, 3, 4, 5], 2))
        [[1, 2], [3, 4], [5]]
        >>> list(chunked_iterator([1, 2, 3], 5))
        [[1, 2, 3]]
    """
    raise NotImplementedError("Implement chunked_iterator")
