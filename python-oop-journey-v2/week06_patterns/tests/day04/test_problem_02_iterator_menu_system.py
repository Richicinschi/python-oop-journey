"""Tests for Problem 02: Iterator Menu System."""

from __future__ import annotations

import pytest

from week06_patterns.solutions.day04.problem_02_iterator_menu_system import (
    MenuItem,
    Menu,
    MenuIterator,
    PriceSortedIterator,
    CategoryFilterIterator,
)


class TestMenuItem:
    """Tests for MenuItem class."""
    
    def test_menu_item_creation(self) -> None:
        """MenuItem can be created with name, price, category."""
        item = MenuItem("Burger", 9.99, "main")
        assert item.name == "Burger"
        assert item.price == 9.99
        assert item.category == "main"
    
    def test_menu_item_repr(self) -> None:
        """MenuItem has useful repr."""
        item = MenuItem("Salad", 5.50, "appetizer")
        repr_str = repr(item)
        assert "Salad" in repr_str
        assert "5.50" in repr_str
        assert "appetizer" in repr_str
    
    def test_menu_item_equality(self) -> None:
        """MenuItems with same values are equal."""
        item1 = MenuItem("A", 1.0, "cat")
        item2 = MenuItem("A", 1.0, "cat")
        assert item1 == item2
    
    def test_menu_item_inequality(self) -> None:
        """MenuItems with different values are not equal."""
        item1 = MenuItem("A", 1.0, "cat")
        item2 = MenuItem("B", 1.0, "cat")
        assert item1 != item2


class TestMenu:
    """Tests for Menu collection class."""
    
    def test_empty_menu_length(self) -> None:
        """Empty menu has length 0."""
        menu = Menu()
        assert len(menu) == 0
    
    def test_menu_add_item_increases_length(self) -> None:
        """Adding items increases length."""
        menu = Menu()
        menu.add_item(MenuItem("A", 1.0, "main"))
        assert len(menu) == 1
        menu.add_item(MenuItem("B", 2.0, "dessert"))
        assert len(menu) == 2
    
    def test_default_iteration_order(self) -> None:
        """Default iteration is in insertion order."""
        menu = Menu()
        items = [
            MenuItem("First", 1.0, "main"),
            MenuItem("Second", 2.0, "dessert"),
            MenuItem("Third", 3.0, "beverage"),
        ]
        for item in items:
            menu.add_item(item)
        
        result = list(menu)
        assert result == items


class TestMenuIterator:
    """Tests for MenuIterator class."""
    
    def test_iterator_yields_all_items(self) -> None:
        """Iterator yields all menu items."""
        items = [MenuItem(f"Item{i}", float(i), "main") for i in range(5)]
        iterator = MenuIterator(items)
        result = list(iterator)
        assert len(result) == 5
    
    def test_iterator_is_iterable(self) -> None:
        """Iterator returns self from __iter__."""
        items = [MenuItem("A", 1.0, "main")]
        iterator = MenuIterator(items)
        assert iter(iterator) is iterator
    
    def test_iterator_raises_stop_iteration(self) -> None:
        """Iterator raises StopIteration when exhausted."""
        items = [MenuItem("A", 1.0, "main")]
        iterator = MenuIterator(items)
        next(iterator)  # Get the one item
        with pytest.raises(StopIteration):
            next(iterator)


class TestPriceSortedIterator:
    """Tests for PriceSortedIterator class."""
    
    def test_items_sorted_by_price_ascending(self) -> None:
        """Iterator yields items sorted by price low to high."""
        items = [
            MenuItem("Expensive", 20.0, "main"),
            MenuItem("Cheap", 5.0, "appetizer"),
            MenuItem("Medium", 12.0, "main"),
        ]
        iterator = PriceSortedIterator(items)
        result = list(iterator)
        
        assert result[0].name == "Cheap"
        assert result[1].name == "Medium"
        assert result[2].name == "Expensive"
    
    def test_same_price_maintains_order(self) -> None:
        """Items with same price maintain relative order."""
        items = [
            MenuItem("First", 10.0, "main"),
            MenuItem("Second", 10.0, "dessert"),
        ]
        iterator = PriceSortedIterator(items)
        result = list(iterator)
        
        assert result[0].name == "First"
        assert result[1].name == "Second"


class TestCategoryFilterIterator:
    """Tests for CategoryFilterIterator class."""
    
    def test_filters_by_category(self) -> None:
        """Iterator yields only matching category items."""
        items = [
            MenuItem("Steak", 25.0, "main"),
            MenuItem("Salad", 8.0, "appetizer"),
            MenuItem("Pasta", 18.0, "main"),
            MenuItem("Cake", 7.0, "dessert"),
        ]
        iterator = CategoryFilterIterator(items, "main")
        result = list(iterator)
        
        assert len(result) == 2
        assert all(item.category == "main" for item in result)
    
    def test_no_matches_returns_empty(self) -> None:
        """Empty result when no items match category."""
        items = [
            MenuItem("Steak", 25.0, "main"),
            MenuItem("Pasta", 18.0, "main"),
        ]
        iterator = CategoryFilterIterator(items, "beverage")
        result = list(iterator)
        
        assert len(result) == 0
    
    def test_skips_non_matching_items(self) -> None:
        """Iterator correctly skips non-matching items."""
        items = [
            MenuItem("A", 1.0, "other"),
            MenuItem("B", 2.0, "target"),
            MenuItem("C", 3.0, "other"),
            MenuItem("D", 4.0, "target"),
        ]
        iterator = CategoryFilterIterator(items, "target")
        result = list(iterator)
        
        assert len(result) == 2
        assert result[0].name == "B"
        assert result[1].name == "D"


class TestMenuIterationMethods:
    """Tests for Menu's iteration method conveniences."""
    
    def test_by_price_returns_price_sorted_iterator(self) -> None:
        """Menu.by_price() returns PriceSortedIterator."""
        menu = Menu()
        menu.add_item(MenuItem("A", 5.0, "main"))
        
        iterator = menu.by_price()
        assert isinstance(iterator, PriceSortedIterator)
    
    def test_by_category_returns_filter_iterator(self) -> None:
        """Menu.by_category() returns CategoryFilterIterator."""
        menu = Menu()
        menu.add_item(MenuItem("A", 5.0, "main"))
        
        iterator = menu.by_category("main")
        assert isinstance(iterator, CategoryFilterIterator)
    
    def test_multiple_iterators_independent(self) -> None:
        """Multiple iterators on same menu are independent."""
        menu = Menu()
        menu.add_item(MenuItem("Cheap", 5.0, "main"))
        menu.add_item(MenuItem("Expensive", 20.0, "main"))
        
        price_iter = menu.by_price()
        default_iter = iter(menu)
        
        price_first = next(price_iter)
        default_first = next(default_iter)
        
        assert price_first.name == "Cheap"
        assert default_first.name == "Cheap"  # Both first in their order


class TestIteratorProtocol:
    """Tests verifying iterator protocol compliance."""
    
    def test_menu_is_iterable(self) -> None:
        """Menu can be used in for loops."""
        menu = Menu()
        menu.add_item(MenuItem("A", 1.0, "main"))
        
        items = []
        for item in menu:
            items.append(item)
        
        assert len(items) == 1
    
    def test_for_loop_with_price_iterator(self) -> None:
        """Price iterator works in for loops."""
        menu = Menu()
        menu.add_item(MenuItem("B", 10.0, "main"))
        menu.add_item(MenuItem("A", 5.0, "main"))
        
        names = [item.name for item in menu.by_price()]
        assert names == ["A", "B"]
