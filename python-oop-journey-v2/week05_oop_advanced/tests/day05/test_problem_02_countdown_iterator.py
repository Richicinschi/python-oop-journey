"""Tests for Problem 02: Countdown Iterator."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day05.problem_02_countdown_iterator import (
    Countdown, CountdownWithMessage
)


class TestCountdown:
    """Tests for the Countdown class."""
    
    def test_countdown_basic(self) -> None:
        cd = Countdown(5)
        result = list(cd)
        assert result == [5, 4, 3, 2, 1, 0]
    
    def test_countdown_from_zero(self) -> None:
        cd = Countdown(0)
        result = list(cd)
        assert result == [0]
    
    def test_countdown_from_one(self) -> None:
        cd = Countdown(1)
        result = list(cd)
        assert result == [1, 0]
    
    def test_countdown_negative_start_raises_error(self) -> None:
        with pytest.raises(ValueError, match="non-negative"):
            Countdown(-1)
    
    def test_countdown_reusable(self) -> None:
        cd = Countdown(3)
        first = list(cd)
        second = list(cd)
        assert first == second == [3, 2, 1, 0]
    
    def test_countdown_iter_returns_self(self) -> None:
        cd = Countdown(5)
        assert iter(cd) is cd
    
    def test_countdown_next_values(self) -> None:
        cd = Countdown(3)
        assert next(cd) == 3
        assert next(cd) == 2
        assert next(cd) == 1
        assert next(cd) == 0
    
    def test_countdown_stop_iteration(self) -> None:
        cd = Countdown(1)
        next(cd)
        next(cd)
        with pytest.raises(StopIteration):
            next(cd)


class TestCountdownWithMessage:
    """Tests for the CountdownWithMessage class."""
    
    def test_countdown_with_message_basic(self) -> None:
        cd = CountdownWithMessage(3)
        result = list(cd)
        assert result == ["T-minus 3", "T-minus 2", "T-minus 1", "Liftoff!"]
    
    def test_countdown_with_message_from_zero(self) -> None:
        cd = CountdownWithMessage(0)
        result = list(cd)
        assert result == ["Liftoff!"]
    
    def test_countdown_with_message_from_one(self) -> None:
        cd = CountdownWithMessage(1)
        result = list(cd)
        assert result == ["T-minus 1", "Liftoff!"]
    
    def test_countdown_with_message_negative_start_raises_error(self) -> None:
        with pytest.raises(ValueError, match="non-negative"):
            CountdownWithMessage(-5)
    
    def test_countdown_with_message_reusable(self) -> None:
        cd = CountdownWithMessage(2)
        first = list(cd)
        second = list(cd)
        assert first == second == ["T-minus 2", "T-minus 1", "Liftoff!"]
    
    def test_countdown_with_message_stop_iteration_after_liftoff(self) -> None:
        cd = CountdownWithMessage(0)
        next(cd)  # Get "Liftoff!"
        with pytest.raises(StopIteration):
            next(cd)
    
    def test_countdown_with_message_exhausted_after_iteration(self) -> None:
        cd = CountdownWithMessage(2)
        list(cd)  # Exhaust the iterator
        with pytest.raises(StopIteration):
            next(cd)


class TestCountdownComparison:
    """Comparative tests between Countdown and CountdownWithMessage."""
    
    def test_same_number_of_yields_for_start_5(self) -> None:
        cd_numbers = Countdown(5)
        cd_messages = CountdownWithMessage(5)
        
        numbers_count = sum(1 for _ in cd_numbers)
        messages_count = sum(1 for _ in cd_messages)
        
        assert numbers_count == messages_count == 6
    
    def test_both_can_be_used_in_for_loops(self) -> None:
        cd_numbers = Countdown(3)
        cd_messages = CountdownWithMessage(3)
        
        numbers_result = []
        for n in cd_numbers:
            numbers_result.append(n)
        
        messages_result = []
        for m in cd_messages:
            messages_result.append(m)
        
        assert numbers_result == [3, 2, 1, 0]
        assert messages_result == ["T-minus 3", "T-minus 2", "T-minus 1", "Liftoff!"]
