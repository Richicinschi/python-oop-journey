"""Problem 10: Lazy Filter Map

Topic: Generator Expressions, Lazy Evaluation, Chaining
Difficulty: Hard

Chain filter and map operations lazily using generator expressions.
This demonstrates memory-efficient data processing pipelines.

Hints:
    * Hint 1: The key insight is "lazy" - you must use generators/yields
      to process one element at a time, never storing the whole sequence.
      Look at generator expressions: (x for x in iterable if condition)
    
    * Hint 2: Chain the operations conceptually:
      - Iterate through the data
      - For each item: check predicate, if True then apply transform and yield
      - Single loop with both operations, yield one result at a time
    
    * Hint 3: Generator expressions can be nested:
      (transform(x) for x in data if predicate(x))
      Or use a regular loop with yield inside

Debugging Tips:
    - "Out of memory": You're creating lists instead of generators.
      Use () for generator expressions, not [] for list comprehensions
    - "Results are empty": Check your filter predicate - is it too
      restrictive? Print/debug intermediate values
    - "Wrong results": Verify operation order - filter then map is
      different than map then filter
    - Generator consumed: Remember generators are single-use. If you
      need to iterate multiple times, you need to recreate the generator
"""

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

    This function creates a generator pipeline that first filters
    items based on a predicate, then transforms the remaining items.
    The operations are performed lazily (one item at a time).

    Args:
        data: The input data list.
        predicate: A function that returns True for items to keep.
        transform: A function to transform each kept item.

    Yields:
        Transformed values for items that passed the filter.

    Example:
        >>> data = [1, 2, 3, 4, 5, 6]
        >>> pred = lambda x: x % 2 == 0  # Keep evens
        >>> trans = lambda x: x * x      # Square them
        >>> list(lazy_filter_map(data, pred, trans))
        [4, 16, 36]
    """
    raise NotImplementedError("Implement lazy_filter_map")
