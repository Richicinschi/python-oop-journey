"""Tests for Problem 08: Predicate Combiner."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day05.problem_08_predicate_combiner import (
    negate,
    both,
    either,
    all_of,
    any_of,
    none_of,
    filter_with_predicate,
)


class TestNegate:
    """Tests for negate function."""

    def test_negate_true(self) -> None:
        """Test negating a predicate that returns True."""
        is_even = lambda x: x % 2 == 0
        is_odd = negate(is_even)

        assert is_odd(3) is True
        assert is_odd(4) is False

    def test_negate_false(self) -> None:
        """Test negating a predicate that returns False."""
        is_negative = lambda x: x < 0
        is_non_negative = negate(is_negative)

        assert is_non_negative(5) is True
        assert is_non_negative(0) is True
        assert is_non_negative(-1) is False

    def test_double_negation(self) -> None:
        """Test that double negation returns original behavior."""
        is_positive = lambda x: x > 0
        is_positive_again = negate(negate(is_positive))

        assert is_positive_again(5) is True
        assert is_positive_again(-5) is False


class TestBoth:
    """Tests for both function."""

    def test_both_true(self) -> None:
        """Test when both predicates are true."""
        is_positive = lambda x: x > 0
        is_even = lambda x: x % 2 == 0
        is_positive_even = both(is_positive, is_even)

        assert is_positive_even(4) is True

    def test_both_first_false(self) -> None:
        """Test when first predicate is false."""
        is_positive = lambda x: x > 0
        is_even = lambda x: x % 2 == 0
        is_positive_even = both(is_positive, is_even)

        assert is_positive_even(-4) is False

    def test_both_second_false(self) -> None:
        """Test when second predicate is false."""
        is_positive = lambda x: x > 0
        is_even = lambda x: x % 2 == 0
        is_positive_even = both(is_positive, is_even)

        assert is_positive_even(3) is False

    def test_both_false(self) -> None:
        """Test when both predicates are false."""
        is_positive = lambda x: x > 0
        is_even = lambda x: x % 2 == 0
        is_positive_even = both(is_positive, is_even)

        assert is_positive_even(-3) is False


class TestEither:
    """Tests for either function."""

    def test_either_both_true(self) -> None:
        """Test when both predicates are true."""
        is_negative = lambda x: x < 0
        is_zero = lambda x: x == 0
        is_non_positive = either(is_negative, is_zero)

        assert is_non_positive(-5) is True

    def test_either_first_true(self) -> None:
        """Test when first predicate is true."""
        is_negative = lambda x: x < 0
        is_zero = lambda x: x == 0
        is_non_positive = either(is_negative, is_zero)

        assert is_non_positive(-1) is True

    def test_either_second_true(self) -> None:
        """Test when second predicate is true."""
        is_negative = lambda x: x < 0
        is_zero = lambda x: x == 0
        is_non_positive = either(is_negative, is_zero)

        assert is_non_positive(0) is True

    def test_either_both_false(self) -> None:
        """Test when both predicates are false."""
        is_negative = lambda x: x < 0
        is_zero = lambda x: x == 0
        is_non_positive = either(is_negative, is_zero)

        assert is_non_positive(5) is False


class TestAllOf:
    """Tests for all_of function."""

    def test_all_of_all_true(self) -> None:
        """Test when all predicates are true."""
        p = all_of(
            lambda x: x > 0,
            lambda x: x < 10,
            lambda x: x % 2 == 0
        )

        assert p(4) is True
        assert p(8) is True

    def test_all_of_one_false(self) -> None:
        """Test when one predicate is false."""
        p = all_of(
            lambda x: x > 0,
            lambda x: x < 10,
            lambda x: x % 2 == 0
        )

        assert p(11) is False  # Fails < 10
        assert p(3) is False   # Fails even
        assert p(-2) is False  # Fails > 0

    def test_all_of_no_predicates(self) -> None:
        """Test with no predicates."""
        p = all_of()

        # With no predicates, all(vacuously) is True
        assert p(5) is True
        assert p("anything") is True

    def test_all_of_single_predicate(self) -> None:
        """Test with single predicate."""
        p = all_of(lambda x: x > 0)

        assert p(5) is True
        assert p(-1) is False


class TestAnyOf:
    """Tests for any_of function."""

    def test_any_of_one_true(self) -> None:
        """Test when one predicate is true."""
        p = any_of(
            lambda x: x < 0,
            lambda x: x > 100,
            lambda x: x == 50
        )

        assert p(-5) is True
        assert p(150) is True
        assert p(50) is True

    def test_any_of_all_false(self) -> None:
        """Test when all predicates are false."""
        p = any_of(
            lambda x: x < 0,
            lambda x: x > 100,
            lambda x: x == 50
        )

        assert p(25) is False
        assert p(75) is False

    def test_any_of_no_predicates(self) -> None:
        """Test with no predicates."""
        p = any_of()

        # With no predicates, any(vacuously) is False
        assert p(5) is False
        assert p("anything") is False

    def test_any_of_all_true(self) -> None:
        """Test when all predicates are true."""
        p = any_of(
            lambda x: x > 0,
            lambda x: x > 1,
            lambda x: x > 2
        )

        assert p(10) is True


class TestNoneOf:
    """Tests for none_of function."""

    def test_none_of_all_false(self) -> None:
        """Test when all predicates are false."""
        p = none_of(
            lambda x: x < 0,
            lambda x: x > 100
        )

        assert p(50) is True
        assert p(0) is True
        assert p(100) is True

    def test_none_of_one_true(self) -> None:
        """Test when one predicate is true."""
        p = none_of(
            lambda x: x < 0,
            lambda x: x > 100
        )

        assert p(-5) is False
        assert p(150) is False

    def test_none_of_no_predicates(self) -> None:
        """Test with no predicates."""
        p = none_of()

        # With no predicates, none(vacuously) is True
        assert p(5) is True


class TestFilterWithPredicate:
    """Tests for filter_with_predicate function."""

    def test_filter_numbers(self) -> None:
        """Test filtering numbers."""
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        evens = filter_with_predicate(numbers, lambda x: x % 2 == 0)

        assert evens == [2, 4, 6, 8, 10]

    def test_filter_strings(self) -> None:
        """Test filtering strings."""
        words = ["apple", "banana", "cherry", "apricot"]
        starts_with_a = filter_with_predicate(words, lambda w: w.startswith("a"))

        assert starts_with_a == ["apple", "apricot"]

    def test_filter_empty_list(self) -> None:
        """Test filtering empty list."""
        result = filter_with_predicate([], lambda x: True)
        assert result == []

    def test_filter_no_matches(self) -> None:
        """Test when nothing matches."""
        numbers = [1, 3, 5, 7]
        evens = filter_with_predicate(numbers, lambda x: x % 2 == 0)

        assert evens == []

    def test_filter_all_match(self) -> None:
        """Test when everything matches."""
        numbers = [2, 4, 6, 8]
        evens = filter_with_predicate(numbers, lambda x: x % 2 == 0)

        assert evens == [2, 4, 6, 8]

    def test_filter_with_combined_predicate(self) -> None:
        """Test filtering with a combined predicate."""
        numbers = list(range(-10, 11))

        # Filter for positive even numbers
        is_positive = lambda x: x > 0
        is_even = lambda x: x % 2 == 0
        is_positive_even = both(is_positive, is_even)

        result = filter_with_predicate(numbers, is_positive_even)
        assert result == [2, 4, 6, 8, 10]
