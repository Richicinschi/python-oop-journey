"""Reference solution for Problem 08: Fibonacci Generator."""

from __future__ import annotations
from typing import Generator


def fibonacci_generator() -> Generator[int, None, None]:
    """Generate an infinite Fibonacci sequence.

    Uses a generator with yield to produce Fibonacci numbers lazily.
    Maintains state (previous two numbers) between yields.
    Can generate values indefinitely without memory issues.

    Yields:
        The next Fibonacci number in the sequence.
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
