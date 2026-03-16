"""Problem 01: FizzBuzz

Topic: Conditionals, loops
Difficulty: Easy

Write a function that returns a list of strings representing the numbers from 1 to n.
But for multiples of 3, use "Fizz" instead of the number,
for multiples of 5, use "Buzz",
and for multiples of both 3 and 5, use "FizzBuzz".
"""

from __future__ import annotations


def fizz_buzz(n: int) -> list[str]:
    """Return FizzBuzz sequence from 1 to n.

    Args:
        n: The upper bound of the sequence (inclusive).

    Returns:
        A list of strings where multiples of 3 are "Fizz",
        multiples of 5 are "Buzz", multiples of both are "FizzBuzz",
        and other numbers are represented as strings.

    Example:
        >>> fizz_buzz(5)
        ['1', '2', 'Fizz', '4', 'Buzz']
        >>> fizz_buzz(15)[-1]
        'FizzBuzz'
    """
    raise NotImplementedError("Implement fizz_buzz")
