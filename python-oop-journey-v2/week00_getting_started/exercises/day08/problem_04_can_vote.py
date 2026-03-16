"""Problem 04: Can Vote

Topic: Boolean Logic, Complex Conditions
Difficulty: Easy

Write a function that determines if a person can vote based on their age and citizenship.
A person can vote if they are:
- 18 years or older AND a citizen
- OR 16+ years old in a special election (is_special_election=True)

Examples:
    >>> can_vote(20, True)
    True
    >>> can_vote(20, False)
    False
    >>> can_vote(17, True)
    False
    >>> can_vote(16, False, True)  # Special election
    True
    >>> can_vote(15, True, True)   # Too young even for special
    False

Requirements:
    - Use default parameter for is_special_election
    - Combine conditions with logical operators
    - Handle all edge cases
"""

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
    raise NotImplementedError("Implement can_vote")
