"""Problem 05: Fix Off By One

Topic: Debugging Basics
Difficulty: Medium

The function below has an off-by-one bug. Identify and fix it.

The function should return the sum of all even numbers from 0 to n (inclusive).

Examples:
    >>> sum_evens(4)  # 0 + 2 + 4 = 6
    6
    >>> sum_evens(5)  # 0 + 2 + 4 = 6
    6
    >>> sum_evens(10)  # 0 + 2 + 4 + 6 + 8 + 10 = 30
    30

Current buggy behavior:
    >>> sum_evens(4)  # Bug: excludes 0 and/or n
    # Bug present - returns wrong value

Requirements:
    - Include 0 and n if even
    - Return correct sum for all inputs >= 0
    - Return 0 for negative inputs

HINTS:
    Hint 1 (Conceptual): Off-by-one errors usually happen at the boundaries.
        Check both the start and end of your range carefully.

    Hint 2 (Structural): The range() function has three forms:
        - range(stop): starts at 0, goes to stop-1
        - range(start, stop): starts at start, goes to stop-1
        - range(start, stop, step): with a step value
        Which one should you use to include both 0 and n?

    Hint 3 (Edge Case): Test with small values:
        sum_evens(0) should return 0 (only even number is 0)
        sum_evens(1) should return 0 (only even number is 0)
        sum_evens(2) should return 2 (0 + 2)

DEBUGGING TIPS:
    - Add print(f"i = {i}") inside the loop to see what values are being processed
    - Check if 0 is being included: print(f"First i: {i}") before the if statement
    - Check if n is being included: print(f"Last i: {i}") inside the loop
    - Remember: range(1, n) excludes both 0 and n!
    - Common fix: range(0, n + 1) to include both endpoints
"""

from __future__ import annotations


def sum_evens(n: int) -> int:
    """Sum all even numbers from 0 to n (inclusive).

    Args:
        n: The upper bound (inclusive)

    Returns:
        Sum of even numbers from 0 to n
    """
    # Bug: There's an off-by-one error in this implementation
    total = 0
    for i in range(1, n):  # <-- Bug is here (two issues)
        if i % 2 == 0:
            total += i
    return total
