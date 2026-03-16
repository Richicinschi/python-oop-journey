"""Tests for Problem 04: Can Vote."""

from __future__ import annotations

from week00_getting_started.solutions.day08.problem_04_can_vote import can_vote


def test_can_vote_regular_adult_citizen() -> None:
    """Test eligible regular voters."""
    assert can_vote(18, True) is True
    assert can_vote(25, True) is True
    assert can_vote(100, True) is True


def test_can_vote_regular_adult_non_citizen() -> None:
    """Test ineligible non-citizens."""
    assert can_vote(18, False) is False
    assert can_vote(25, False) is False
    assert can_vote(100, False) is False


def test_can_vote_underage_citizen() -> None:
    """Test ineligible underage citizens."""
    assert can_vote(17, True) is False
    assert can_vote(16, True) is False
    assert can_vote(0, True) is False


def test_can_vote_special_election() -> None:
    """Test special election eligibility."""
    assert can_vote(16, True, True) is True
    assert can_vote(17, True, True) is True
    assert can_vote(18, True, True) is True  # Also eligible


def test_can_vote_special_election_non_citizen() -> None:
    """Test special election ineligibility for non-citizens."""
    assert can_vote(16, False, True) is False
    assert can_vote(17, False, True) is False


def test_can_vote_special_election_too_young() -> None:
    """Test special election ineligibility for too young."""
    assert can_vote(15, True, True) is False
    assert can_vote(10, True, True) is False
