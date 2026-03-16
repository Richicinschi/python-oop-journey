"""Tests for Problem 04: Map Filter Reduce Pipeline."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day05.problem_04_map_filter_reduce_pipeline import (
    process_numbers,
    analyze_products,
    pipeline_transform,
    count_by_predicate,
)


class TestProcessNumbers:
    """Tests for process_numbers function."""

    def test_basic_pipeline(self) -> None:
        """Test basic map-filter-reduce pipeline."""
        result = process_numbers(
            [1, 2, 3, 4, 5],
            lambda x: x * 2,  # map: [2, 4, 6, 8, 10]
            lambda x: x > 4,  # filter: [6, 8, 10]
            lambda a, b: a + b,  # reduce: 24
            0
        )
        assert result == 24

    def test_all_filtered_out(self) -> None:
        """Test when all items are filtered out."""
        result = process_numbers(
            [1, 2, 3],
            lambda x: x,
            lambda x: x > 10,  # Nothing passes
            lambda a, b: a + b,
            0
        )
        assert result == 0  # Initial value returned

    def test_empty_list(self) -> None:
        """Test with empty list."""
        result = process_numbers(
            [],
            lambda x: x,
            lambda x: True,
            lambda a, b: a + b,
            100
        )
        assert result == 100  # Initial value returned

    def test_multiply_reducer(self) -> None:
        """Test with multiply reducer."""
        result = process_numbers(
            [1, 2, 3, 4, 5],
            lambda x: x,
            lambda x: x > 2,  # [3, 4, 5]
            lambda a, b: a * b,  # 3 * 4 * 5 = 60
            1
        )
        assert result == 60

    def test_complex_transform(self) -> None:
        """Test with complex transform function."""
        result = process_numbers(
            [1, 2, 3, 4],
            lambda x: x ** 2,  # [1, 4, 9, 16]
            lambda x: x % 2 == 0,  # [4, 16]
            lambda a, b: a + b,
            0
        )
        assert result == 20


class TestAnalyzeProducts:
    """Tests for analyze_products function."""

    def test_empty_products(self) -> None:
        """Test with empty product list."""
        result = analyze_products([])
        assert result == {
            "total_value": 0.0,
            "expensive_count": 0,
            "avg_price": 0.0,
            "categories": set()
        }

    def test_single_product(self) -> None:
        """Test with single product."""
        products = [
            {"name": "Widget", "price": 50.0, "category": "Gadgets"}
        ]
        result = analyze_products(products)
        assert result["total_value"] == 50.0
        assert result["expensive_count"] == 0
        assert result["avg_price"] == 50.0
        assert result["categories"] == {"Gadgets"}

    def test_multiple_products(self) -> None:
        """Test with multiple products."""
        products = [
            {"name": "Cheap", "price": 20.0, "category": "A"},
            {"name": "Medium", "price": 75.0, "category": "B"},
            {"name": "Expensive", "price": 150.0, "category": "A"},
        ]
        result = analyze_products(products)
        assert result["total_value"] == 245.0
        assert result["expensive_count"] == 1
        assert result["avg_price"] == pytest.approx(81.67, 0.01)
        assert result["categories"] == {"A", "B"}

    def test_all_expensive(self) -> None:
        """Test when all products are expensive."""
        products = [
            {"name": "A", "price": 101.0, "category": "X"},
            {"name": "B", "price": 200.0, "category": "X"},
            {"name": "C", "price": 500.0, "category": "X"},
        ]
        result = analyze_products(products)
        assert result["expensive_count"] == 3
        assert result["total_value"] == 801.0

    def test_many_categories(self) -> None:
        """Test with many different categories."""
        products = [
            {"name": f"Product{i}", "price": float(i * 10), "category": f"Cat{i % 3}"}
            for i in range(10)
        ]
        result = analyze_products(products)
        assert result["categories"] == {"Cat0", "Cat1", "Cat2"}


class TestPipelineTransform:
    """Tests for pipeline_transform function."""

    def test_single_operation(self) -> None:
        """Test with single operation."""
        def double_all(nums: list[int]) -> list[int]:
            return [n * 2 for n in nums]

        result = pipeline_transform([1, 2, 3], double_all)
        assert result == [2, 4, 6]

    def test_multiple_operations(self) -> None:
        """Test with multiple operations."""
        def remove_negatives(nums: list[int]) -> list[int]:
            return [n for n in nums if n >= 0]

        def double_all(nums: list[int]) -> list[int]:
            return [n * 2 for n in nums]

        def take_first_three(nums: list[int]) -> list[int]:
            return nums[:3]

        result = pipeline_transform(
            [-5, 3, -2, 7, 0, 10, -1],
            remove_negatives,
            double_all,
            take_first_three
        )
        assert result == [6, 14, 0]

    def test_no_operations(self) -> None:
        """Test with no operations returns copy."""
        original = [1, 2, 3]
        result = pipeline_transform(original)
        assert result == original
        assert result is not original

    def test_with_strings(self) -> None:
        """Test with string operations."""
        def filter_long(words: list[str]) -> list[str]:
            return [w for w in words if len(w) > 3]

        def to_upper(words: list[str]) -> list[str]:
            return [w.upper() for w in words]

        def sort_desc(words: list[str]) -> list[str]:
            return sorted(words, reverse=True)

        result = pipeline_transform(
            ["a", "hello", "hi", "world", "cat"],
            filter_long,
            to_upper,
            sort_desc
        )
        assert result == ["WORLD", "HELLO"]


class TestCountByPredicate:
    """Tests for count_by_predicate function."""

    def test_single_predicate(self) -> None:
        """Test with single predicate."""
        result = count_by_predicate(
            [1, 2, 3, 4, 5, 6],
            [lambda x: x % 2 == 0]
        )
        assert result == {0: 3}  # 2, 4, 6 are even

    def test_multiple_predicates(self) -> None:
        """Test with multiple predicates."""
        result = count_by_predicate(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [
                lambda x: x % 2 == 0,  # even
                lambda x: x > 5,       # greater than 5
                lambda x: x < 4        # less than 4
            ]
        )
        assert result[0] == 5   # 2, 4, 6, 8, 10
        assert result[1] == 5   # 6, 7, 8, 9, 10
        assert result[2] == 3   # 1, 2, 3

    def test_empty_items(self) -> None:
        """Test with empty items list."""
        result = count_by_predicate(
            [],
            [lambda x: True, lambda x: False]
        )
        assert result == {0: 0, 1: 0}

    def test_no_predicates(self) -> None:
        """Test with no predicates."""
        result = count_by_predicate([1, 2, 3], [])
        assert result == {}

    def test_with_strings(self) -> None:
        """Test with string predicates."""
        words = ["apple", "banana", "apricot", "cherry", "avocado"]
        result = count_by_predicate(
            words,
            [
                lambda w: w.startswith("a"),
                lambda w: len(w) > 6,
                lambda w: "e" in w
            ]
        )
        assert result[0] == 3  # apple, apricot, avocado
        assert result[1] == 2  # apricot, avocado (len > 6)
        assert result[2] == 2  # apple, cherry
