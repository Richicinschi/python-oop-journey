"""Problem 05: Main Guard Pattern Module

Topic: __name__ == "__main__" pattern
Difficulty: Medium

Create a module that demonstrates proper use of the __main__ guard pattern.
This module should provide utility functions AND include test/demo code
that only runs when the file is executed directly.

Required functions:
- double(x): Return x * 2
- triple(x): Return x * 3
- square(x): Return x ** 2
- power(base, exp): Return base raised to exp

The __main__ block should:
1. Print "Running math_demo module directly"
2. Run a few test cases demonstrating each function
3. Print formatted results

Example direct execution:
    $ python problem_05_main_guard_demo.py
    Running math_demo module directly
    double(5) = 10
    triple(3) = 9
    square(4) = 16
    power(2, 8) = 256

When imported, nothing should print automatically:
    >>> from main_guard_demo import double
    >>> double(5)
    10
"""

from __future__ import annotations


def double(x: int | float) -> int | float:
    """Return the double of x."""
    raise NotImplementedError("Implement double")


def triple(x: int | float) -> int | float:
    """Return the triple of x."""
    raise NotImplementedError("Implement triple")


def square(x: int | float) -> int | float:
    """Return the square of x."""
    raise NotImplementedError("Implement square")


def power(base: int | float, exp: int) -> int | float:
    """Return base raised to the power of exp."""
    raise NotImplementedError("Implement power")


# TODO: Add the if __name__ == "__main__": block here
# It should demonstrate the functions with test cases
