"""Problem 07: Running Total Generator

Topic: Generators, yield, State Management
Difficulty: Medium

Create a generator that yields running totals of a sequence of numbers.
"""

from __future__ import annotations
from typing import Generator


def running_total_generator(numbers: list[int]) -> Generator[int, None, None]:
    """Yield running totals of the input sequence.

    Args:
        numbers: A list of integers.

    Yields:
        The running total after each number is added.

    Example:
        >>> list(running_total_generator([1, 2, 3, 4]))
        [1, 3, 6, 10]
        >>> list(running_total_generator([5, -2, 7]))
        [5, 3, 10]
        >>> list(running_total_generator([]))
        []
    """
    raise NotImplementedError("Implement running_total_generator")
