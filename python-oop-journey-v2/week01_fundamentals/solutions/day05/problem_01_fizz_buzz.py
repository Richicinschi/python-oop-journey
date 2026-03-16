"""Reference solution for Problem 01: FizzBuzz."""

from __future__ import annotations


def fizz_buzz(n: int) -> list[str]:
    """Return FizzBuzz sequence from 1 to n.

    Args:
        n: The upper bound of the sequence (inclusive).

    Returns:
        A list of strings where multiples of 3 are "Fizz",
        multiples of 5 are "Buzz", multiples of both are "FizzBuzz",
        and other numbers are represented as strings.
    """
    result: list[str] = []
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result
