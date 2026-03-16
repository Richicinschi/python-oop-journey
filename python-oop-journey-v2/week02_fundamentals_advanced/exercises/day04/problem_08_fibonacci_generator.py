"""Problem 08: Fibonacci Generator

Topic: Generators, Infinite Sequences, yield
Difficulty: Medium

Create an infinite Fibonacci sequence generator using yield.

Hints:
    * Hint 1: The Fibonacci sequence starts 0, 1, 1, 2, 3, 5, 8...
      Each number is the sum of the two preceding ones.
      You need to track two values that update each iteration.
    
    * Hint 2: Structure your generator like this:
      - Initialize a, b = 0, 1
      - Loop forever (while True):
        - yield the current value (a)
        - Update a, b = b, a + b
    
    * Hint 3: The generator should be infinite - don't try to return
      all values at once. The caller controls how many values to consume
      using next() or itertools.islice().

Debugging Tips:
    - "Generator is empty": Did you forget the yield statement or
      put a return before it?
    - "Wrong sequence starting": First yield should be 0, not 1
    - "Generator exhausted": Fibonacci should be infinite - check for
      an accidental termination condition or return statement
    - Using list(generator): This will hang/infinite loop! Use islice
      to limit how many values you extract when testing
"""

from __future__ import annotations
from typing import Generator


def fibonacci_generator() -> Generator[int, None, None]:
    """Generate an infinite Fibonacci sequence.

    Yields:
        The next Fibonacci number (0, 1, 1, 2, 3, 5, 8, 13, ...).

    Example:
        >>> gen = fibonacci_generator()
        >>> next(gen)
        0
        >>> next(gen)
        1
        >>> next(gen)
        1
        >>> [next(gen) for _ in range(5)]
        [2, 3, 5, 8, 13]
    """
    raise NotImplementedError("Implement fibonacci_generator")
