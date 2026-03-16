"""Problem 05: Parameter Scope - Solution."""

from __future__ import annotations


def double_value(x: int) -> int:
    """Return double the input value.

    The parameter 'x' is a local variable.

    Args:
        x: The number to double.

    Returns:
        The doubled value (x * 2).
    """
    return x * 2


def triple_in_place(numbers: list[int]) -> None:
    """Triple each number in the list in-place.

    Note: This modifies the list that is passed in.
    The parameter 'numbers' is local, but the list it refers to
    is modified in-place.

    Args:
        numbers: A list of integers to modify.
    """
    for i in range(len(numbers)):
        numbers[i] = numbers[i] * 3


def get_final_value(initial: int, operations: list[str]) -> int:
    """Apply operations to an initial value.

    Args:
        initial: The starting value.
        operations: List of operations as strings.
                   "+" adds 1, "-" subtracts 1, "*" multiplies by 2.

    Returns:
        The final value after all operations.
    """
    current = initial
    for op in operations:
        if op == "+":
            current += 1
        elif op == "-":
            current -= 1
        elif op == "*":
            current *= 2
    return current
