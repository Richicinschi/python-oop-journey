"""Tests for Problem 01: Chain Operations."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day05.problem_01_chain_operations import (
    chain_operations,
    create_pipeline,
    apply_transformations,
)


class TestChainOperations:
    """Tests for chain_operations function."""

    def test_single_operation(self) -> None:
        """Test with a single operation."""
        def add_one(x: int) -> int:
            return x + 1

        result = chain_operations(5, add_one)
        assert result == 6

    def test_multiple_operations(self) -> None:
        """Test chaining multiple operations."""
        def add_one(x: int) -> int:
            return x + 1

        def double(x: int) -> int:
            return x * 2

        def negate(x: int) -> int:
            return -x

        result = chain_operations(5, add_one, double, negate)
        # 5 + 1 = 6, 6 * 2 = 12, -12 = -12
        assert result == -12

    def test_no_operations(self) -> None:
        """Test with no operations returns initial value."""
        result = chain_operations(42)
        assert result == 42

    def test_string_operations(self) -> None:
        """Test with string operations."""
        def strip(s: str) -> str:
            return s.strip()

        def upper(s: str) -> str:
            return s.upper()

        def exclaim(s: str) -> str:
            return s + "!"

        result = chain_operations("  hello  ", strip, upper, exclaim)
        assert result == "HELLO!"

    def test_with_lambda(self) -> None:
        """Test with lambda functions."""
        result = chain_operations(
            10,
            lambda x: x + 5,
            lambda x: x * 2,
            lambda x: x - 3
        )
        # 10 + 5 = 15, 15 * 2 = 30, 30 - 3 = 27
        assert result == 27


class TestCreatePipeline:
    """Tests for create_pipeline function."""

    def test_single_operation_pipeline(self) -> None:
        """Test pipeline with single operation."""
        pipeline = create_pipeline(str.strip)
        assert pipeline("  hello  ") == "hello"

    def test_multiple_operations_pipeline(self) -> None:
        """Test pipeline with multiple operations."""
        pipeline = create_pipeline(str.strip, str.upper)
        assert pipeline("  hello  ") == "HELLO"

    def test_complex_pipeline(self) -> None:
        """Test complex string processing pipeline."""
        def remove_vowels(s: str) -> str:
            return ''.join(c for c in s if c.lower() not in 'aeiou')

        pipeline = create_pipeline(str.strip, str.lower, remove_vowels)
        assert pipeline("  HELLO WORLD  ") == "hll wrld"

    def test_pipeline_reusability(self) -> None:
        """Test that pipeline can be reused."""
        pipeline = create_pipeline(str.strip, str.title)
        assert pipeline("  alice  ") == "Alice"
        assert pipeline("  bob  ") == "Bob"
        assert pipeline("  charlie  ") == "Charlie"

    def test_empty_pipeline(self) -> None:
        """Test empty pipeline returns input unchanged."""
        pipeline = create_pipeline()
        assert pipeline("hello") == "hello"


class TestApplyTransformations:
    """Tests for apply_transformations function."""

    def test_single_transformation(self) -> None:
        """Test with single transformation."""
        def double_all(nums: list[int]) -> list[int]:
            return [n * 2 for n in nums]

        result = apply_transformations([1, 2, 3], double_all)
        assert result == [2, 4, 6]

    def test_multiple_transformations(self) -> None:
        """Test with multiple transformations."""
        def remove_negatives(nums: list[int]) -> list[int]:
            return [n for n in nums if n >= 0]

        def double_all(nums: list[int]) -> list[int]:
            return [n * 2 for n in nums]

        result = apply_transformations([-5, -2, 3, 7, -1], remove_negatives, double_all)
        assert result == [6, 14]

    def test_no_transformations(self) -> None:
        """Test with no transformations returns copy."""
        original = [1, 2, 3]
        result = apply_transformations(original)
        assert result == original
        assert result is not original  # Should be a copy

    def test_filter_and_sort(self) -> None:
        """Test filtering and sorting pipeline."""
        def remove_small(nums: list[int]) -> list[int]:
            return [n for n in nums if n > 5]

        def sort_descending(nums: list[int]) -> list[int]:
            return sorted(nums, reverse=True)

        result = apply_transformations([3, 8, 1, 9, 2, 10], remove_small, sort_descending)
        assert result == [10, 9, 8]

    def test_original_list_unchanged(self) -> None:
        """Test that original list is not modified."""
        def double_all(nums: list[int]) -> list[int]:
            return [n * 2 for n in nums]

        original = [1, 2, 3]
        apply_transformations(original, double_all)
        assert original == [1, 2, 3]  # Original unchanged
