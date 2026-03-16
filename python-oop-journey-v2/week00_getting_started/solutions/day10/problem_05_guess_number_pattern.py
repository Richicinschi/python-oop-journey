"""Reference solution for Problem 05: Guess Number Pattern."""

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
    attempts = 0
    index = 0

    while attempts < max_attempts and index < len(guesses):
        attempts += 1
        if guesses[index] == target:
            return attempts, True
        index += 1

    return attempts, False
