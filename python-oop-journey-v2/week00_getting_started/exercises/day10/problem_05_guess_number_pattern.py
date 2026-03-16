"""Problem 05: Guess Number Pattern

Topic: While Loops, Break, Infinite Loops
Difficulty: Easy

Write a function that simulates a number guessing game pattern.
Given a list of guesses, the target number, and a max attempts limit,
return the number of attempts made and whether the target was found.

The function iterates through guesses (simulating user input) and stops when:
- The target is found (correct guess)
- Or max attempts reached
- Or guesses list is exhausted

Examples:
    >>> guess_number_pattern([5, 10, 15, 20], 15, 5)
    (3, True)   # Found on 3rd attempt
    >>> guess_number_pattern([1, 2, 3], 5, 5)
    (3, False)  # Exhausted guesses, not found
    >>> guess_number_pattern([5, 10, 15, 20], 20, 2)
    (2, False)  # Hit max attempts before finding

Requirements:
    - Use a while loop
    - Use break when target is found
    - Track attempts and found status
"""

from __future__ import annotations


def guess_number_pattern(
    guesses: list[int], target: int, max_attempts: int
) -> tuple[int, bool]:
    """Simulate a number guessing game pattern.

    Args:
        guesses: List of guesses to try (simulating user inputs)
        target: The number to find
        max_attempts: Maximum number of attempts allowed

    Returns:
        Tuple of (attempts_made, was_found)
    """
    raise NotImplementedError("Implement guess_number_pattern")
