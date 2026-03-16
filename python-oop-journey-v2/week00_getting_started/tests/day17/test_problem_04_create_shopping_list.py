"""Tests for Problem 04: Create Shopping List."""

from __future__ import annotations

from week00_getting_started.solutions.day17.problem_04_create_shopping_list import create_shopping_list


def test_create_new_list() -> None:
    """Test creating a new shopping list."""
    result = create_shopping_list("apples")
    assert result == ["apples"]


def test_add_to_existing_list() -> None:
    """Test adding to an existing shopping list."""
    existing = ["milk", "bread"]
    result = create_shopping_list("eggs", existing)
    assert result == ["milk", "bread", "eggs"]


def test_no_mutable_default_bug() -> None:
    """Test that the mutable default bug is avoided."""
    # Call multiple times without providing items
    list1 = create_shopping_list("apples")
    list2 = create_shopping_list("bananas")
    list3 = create_shopping_list("oranges")

    # Each should be a separate list with just that item
    assert list1 == ["apples"]
    assert list2 == ["bananas"]
    assert list3 == ["oranges"]

    # They should be different list objects
    assert list1 is not list2
    assert list2 is not list3


def test_add_multiple_to_same_list() -> None:
    """Test adding multiple items to the same list."""
    items: list[str] = []
    create_shopping_list("milk", items)
    create_shopping_list("bread", items)
    create_shopping_list("eggs", items)
    assert items == ["milk", "bread", "eggs"]
