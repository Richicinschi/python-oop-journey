"""Reference solution for Problem 07: Running Total Generator."""

from __future__ import annotations
from typing import Generator


def running_total_generator(numbers: list[int]) -> Generator[int, None, None]:
    """Yield running totals of the input sequence.

    Uses a generator with yield to produce running totals lazily.
    Maintains state (running sum) between yields.

    Args:
        numbers: A list of integers.

    Yields:
        The running total after each number is added.
    """
    total = 0
    for num in numbers:
        total += num
        yield total
