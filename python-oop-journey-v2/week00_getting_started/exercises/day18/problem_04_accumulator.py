"""Problem 04: Accumulator with Closure

Topic: Variable Scope - Closures
Difficulty: Medium

Create an accumulator function using closure.

Function Signature:
    def make_accumulator(start: int = 0) -> callable

Requirements:
    - Return a function that maintains internal state
    - The returned function adds its argument to the accumulated total
    - Each call updates and returns the new total

Behavior Notes:
    - A closure is a function that remembers values from its enclosing scope
    - The inner function maintains access to 'total' even after make_accumulator returns
    - Each accumulator has its own independent state

Examples:
    >>> acc = make_accumulator(10)
    >>> acc(5)
    15
    >>> acc(3)
    18
    >>> acc(-2)
    16
    
    Multiple accumulators are independent:
    >>> acc1 = make_accumulator(0)
    >>> acc2 = make_accumulator(100)
    >>> acc1(10)
    10
    >>> acc2(10)
    110

Input Validation:
    - You may assume start is an integer
    - The returned function takes an integer argument

"""

from __future__ import annotations


def make_accumulator(start: int = 0) -> callable:
    """Create an accumulator function with closure.

    Args:
        start: The initial value (default 0).

    Returns:
        A function that adds to and returns the accumulated total.
    """
    raise NotImplementedError("Implement make_accumulator")
