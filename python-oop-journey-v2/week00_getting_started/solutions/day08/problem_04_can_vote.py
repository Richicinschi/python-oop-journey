"""Reference solution for Problem 04: Can Vote."""

from __future__ import annotations


def can_vote(age: int, is_citizen: bool, is_special_election: bool = False) -> bool:
    """Determine if a person can vote.

    Args:
        age: The person's age in years
        is_citizen: Whether the person is a citizen
        is_special_election: Whether it's a special election (16+ can vote)

    Returns:
        True if the person can vote, False otherwise
    """
    # Regular election: 18+ and citizen
    if age >= 18 and is_citizen:
        return True

    # Special election: 16+ (citizenship requirement may vary, here we require it)
    if is_special_election and age >= 16 and is_citizen:
        return True

    return False
