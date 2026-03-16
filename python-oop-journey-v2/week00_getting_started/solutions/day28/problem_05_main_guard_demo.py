"""Reference solution for Problem 05: Main Guard Pattern Module."""

from __future__ import annotations


def double(x: int | float) -> int | float:
    """Return the double of x."""
    return x * 2


def triple(x: int | float) -> int | float:
    """Return the triple of x."""
    return x * 3


def square(x: int | float) -> int | float:
    """Return the square of x."""
    return x * x


def power(base: int | float, exp: int) -> int | float:
    """Return base raised to the power of exp."""
    result = 1
    for _ in range(exp):
        result *= base
    return result


if __name__ == "__main__":
    print("Running math_demo module directly")
    print(f"double(5) = {double(5)}")
    print(f"triple(3) = {triple(3)}")
    print(f"square(4) = {square(4)}")
    print(f"power(2, 8) = {power(2, 8)}")
