"""Tests for Problem 05: Custom Sort Key."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day05.problem_05_custom_sort_key import (
    Product,
    sort_by_multiple_keys,
    create_sort_key,
    sort_products_by_relevance,
    get_top_n_by_criteria,
)


class TestSortByMultipleKeys:
    """Tests for sort_by_multiple_keys function."""

    def test_single_key(self) -> None:
        """Test sorting by single key."""
        items = [("c", 1), ("a", 3), ("b", 2)]
        result = sort_by_multiple_keys(items, lambda x: x[0])
        assert result == [("a", 3), ("b", 2), ("c", 1)]

    def test_multiple_keys(self) -> None:
        """Test sorting by multiple keys."""
        items = [("b", 2), ("a", 1), ("a", 3), ("b", 1)]
        result = sort_by_multiple_keys(
            items,
            lambda x: x[0],
            lambda x: x[1]
        )
        assert result == [("a", 1), ("a", 3), ("b", 1), ("b", 2)]

    def test_empty_list(self) -> None:
        """Test with empty list."""
        result = sort_by_multiple_keys([], lambda x: x)
        assert result == []

    def test_three_keys(self) -> None:
        """Test sorting by three keys."""
        items = [
            ("a", "x", 3),
            ("a", "y", 1),
            ("b", "x", 2),
            ("a", "x", 1),
        ]
        result = sort_by_multiple_keys(
            items,
            lambda x: x[0],
            lambda x: x[1],
            lambda x: x[2]
        )
        assert result == [
            ("a", "x", 1),
            ("a", "x", 3),
            ("a", "y", 1),
            ("b", "x", 2),
        ]


class TestCreateSortKey:
    """Tests for create_sort_key function."""

    def test_single_key(self) -> None:
        """Test with single key."""
        data = [("c", 1), ("a", 3), ("b", 2)]
        key = create_sort_key(lambda x: x[0])
        result = sorted(data, key=key)
        assert result == [("a", 3), ("b", 2), ("c", 1)]

    def test_multiple_keys(self) -> None:
        """Test with multiple keys."""
        data = [("b", 2), ("a", 1), ("a", 3)]
        key = create_sort_key(lambda x: x[0], lambda x: x[1])
        result = sorted(data, key=key)
        assert result == [("a", 1), ("a", 3), ("b", 2)]

    def test_with_reverse(self) -> None:
        """Test with reverse flag for numeric values."""
        data = [("a", 5), ("a", 3), ("b", 10)]
        # Sort by first element ascending, second descending
        key = create_sort_key(
            lambda x: x[0],
            lambda x: x[1],
            reverse_flags=[False, True]
        )
        result = sorted(data, key=key)
        assert result == [("a", 5), ("a", 3), ("b", 10)]

    def test_all_reverse(self) -> None:
        """Test with all keys reversed."""
        data = [1, 2, 3, 4, 5]
        key = create_sort_key(lambda x: x, reverse_flags=[True])
        result = sorted(data, key=key)
        assert result == [5, 4, 3, 2, 1]


class TestSortProductsByRelevance:
    """Tests for sort_products_by_relevance function."""

    def test_name_starts_with_query(self) -> None:
        """Test products with name starting with query are most relevant."""
        products = [
            Product("Apple Juice", 5.0, "Beverages"),
            Product("Banana", 1.0, "Fruit"),
            Product("Apple Pie", 8.0, "Desserts"),
        ]
        result = sort_products_by_relevance(products, "apple")
        # Both start with "apple", should be first two, sorted by price
        assert result[0].name == "Apple Juice"
        assert result[1].name == "Apple Pie"

    def test_name_contains_query(self) -> None:
        """Test products with name containing query are second most relevant."""
        products = [
            Product("Pineapple", 3.0, "Fruit"),
            Product("Apple", 1.0, "Fruit"),
            Product("Crabapple", 2.0, "Fruit"),
        ]
        result = sort_products_by_relevance(products, "apple")
        # "Apple" starts with query, others contain it
        assert result[0].name == "Apple"
        # "Crabapple" and "Pineapple" both contain, sorted by price
        assert result[1].name == "Crabapple"
        assert result[2].name == "Pineapple"

    def test_category_matches(self) -> None:
        """Test category matches are third most relevant."""
        products = [
            Product("Water", 1.0, "Drinks"),
            Product("Beer", 5.0, "Drinks"),
            Product("Soda", 2.0, "Drinks"),
            Product("Drinkware Set", 15.0, "Kitchen"),  # Name contains but different category
        ]
        result = sort_products_by_relevance(products, "drinks")
        # All three beverages should come before kitchen item
        assert result[0].category == "Drinks"
        assert result[1].category == "Drinks"
        assert result[2].category == "Drinks"
        assert result[3].name == "Drinkware Set"

    def test_no_match(self) -> None:
        """Test no matches are last."""
        products = [
            Product("Orange", 2.0, "Fruit"),
            Product("Apple", 1.0, "Fruit"),
            Product("Pear", 3.0, "Fruit"),
        ]
        result = sort_products_by_relevance(products, "banana")
        # No matches, all should be score 3, sorted by price
        assert result[0].name == "Apple"
        assert result[1].name == "Orange"
        assert result[2].name == "Pear"

    def test_empty_query(self) -> None:
        """Test with empty query."""
        products = [
            Product("Apple", 5.0, "Fruit"),
            Product("Banana", 1.0, "Fruit"),
        ]
        result = sort_products_by_relevance(products, "")
        # Empty string matches start of all names
        # All should have score 0, sorted by price
        assert result[0].name == "Banana"
        assert result[1].name == "Apple"


class TestGetTopNByCriteria:
    """Tests for get_top_n_by_criteria function."""

    def test_top_n_numeric(self) -> None:
        """Test getting top N by numeric criteria."""
        items = [10, 5, 20, 3, 15]
        result = get_top_n_by_criteria(items, 3, lambda x: x)
        assert result == [20, 15, 10]

    def test_top_n_with_reverse_false(self) -> None:
        """Test getting lowest N items."""
        items = [10, 5, 20, 3, 15]
        result = get_top_n_by_criteria(items, 3, lambda x: x, reverse=False)
        assert result == [3, 5, 10]

    def test_n_larger_than_list(self) -> None:
        """Test when N is larger than list size."""
        items = [1, 2, 3]
        result = get_top_n_by_criteria(items, 10, lambda x: x)
        assert result == [3, 2, 1]

    def test_with_products(self) -> None:
        """Test with Product objects."""
        products = [
            Product("A", 50.0, "X"),
            Product("B", 100.0, "X"),
            Product("C", 25.0, "X"),
            Product("D", 75.0, "X"),
        ]
        result = get_top_n_by_criteria(products, 2, lambda p: p.price)
        assert len(result) == 2
        assert result[0].price == 100.0
        assert result[1].price == 75.0

    def test_with_strings(self) -> None:
        """Test sorting by string length."""
        words = ["a", "hello", "hi", "worldwide", "cat"]
        result = get_top_n_by_criteria(words, 2, lambda w: len(w))
        assert result == ["worldwide", "hello"]

    def test_empty_list(self) -> None:
        """Test with empty list."""
        result = get_top_n_by_criteria([], 5, lambda x: x)
        assert result == []
