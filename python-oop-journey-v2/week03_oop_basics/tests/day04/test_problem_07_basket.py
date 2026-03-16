"""Tests for Problem 07: Basket."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day04.problem_07_basket import Basket, Item


class TestItemInit:
    """Test Item initialization."""
    
    def test_init_basic(self) -> None:
        item = Item("Apple", 0.50, 3)
        assert item.name == "Apple"
        assert item.price == 0.50
        assert item.quantity == 3
    
    def test_init_default_quantity(self) -> None:
        item = Item("Apple", 0.50)
        assert item.quantity == 1


class TestItemTotalPrice:
    """Test Item total price calculation."""
    
    def test_total_price(self) -> None:
        item = Item("Apple", 0.50, 3)
        assert item.total_price() == 1.50
    
    def test_total_price_quantity_one(self) -> None:
        item = Item("Apple", 0.50, 1)
        assert item.total_price() == 0.50


class TestItemEquality:
    """Test Item equality."""
    
    def test_equal_same_name_and_price(self) -> None:
        i1 = Item("Apple", 0.50, 3)
        i2 = Item("Apple", 0.50, 5)
        assert i1 == i2  # Quantity doesn't matter for equality
    
    def test_not_equal_different_name(self) -> None:
        i1 = Item("Apple", 0.50)
        i2 = Item("Banana", 0.50)
        assert i1 != i2
    
    def test_not_equal_different_price(self) -> None:
        i1 = Item("Apple", 0.50)
        i2 = Item("Apple", 0.60)
        assert i1 != i2


class TestBasketInit:
    """Test Basket initialization."""
    
    def test_init_empty(self) -> None:
        basket = Basket()
        assert len(basket) == 0


class TestBasketAddItem:
    """Test adding items to basket."""
    
    def test_add_item(self) -> None:
        basket = Basket()
        item = Item("Apple", 0.50, 3)
        basket.add_item(item)
        assert len(basket) == 1
    
    def test_add_multiple_items(self) -> None:
        basket = Basket()
        basket.add_item(Item("Apple", 0.50, 3))
        basket.add_item(Item("Banana", 0.30, 2))
        assert len(basket) == 2


class TestBasketIAdd:
    """Test Basket += operator."""
    
    def test_iadd_adds_item(self) -> None:
        basket = Basket()
        basket += Item("Apple", 0.50, 3)
        assert len(basket) == 1
    
    def test_iadd_returns_basket(self) -> None:
        basket = Basket()
        result = basket.__iadd__(Item("Apple", 0.50))
        assert result is basket
    
    def test_iadd_chainable(self) -> None:
        basket = Basket()
        basket += Item("Apple", 0.50)
        basket += Item("Banana", 0.30)
        assert len(basket) == 2


class TestBasketAdd:
    """Test Basket + operator."""
    
    def test_add_two_baskets(self) -> None:
        basket1 = Basket()
        basket1 += Item("Apple", 0.50, 2)
        
        basket2 = Basket()
        basket2 += Item("Banana", 0.30, 3)
        
        combined = basket1 + basket2
        assert len(combined) == 2
        assert len(basket1) == 1  # Original unchanged
        assert len(basket2) == 1
    
    def test_add_returns_new_basket(self) -> None:
        basket1 = Basket()
        basket2 = Basket()
        combined = basket1 + basket2
        assert combined is not basket1
        assert combined is not basket2
    
    def test_add_non_basket_returns_not_implemented(self) -> None:
        basket = Basket()
        result = basket.__add__("not a basket")
        assert result is NotImplemented


class TestBasketLen:
    """Test Basket length."""
    
    def test_len_empty(self) -> None:
        basket = Basket()
        assert len(basket) == 0
    
    def test_len_with_items(self) -> None:
        basket = Basket()
        basket += Item("Apple", 0.50, 3)
        basket += Item("Banana", 0.30, 2)
        assert len(basket) == 2  # Two distinct items, not total quantity


class TestBasketIteration:
    """Test Basket iteration."""
    
    def test_iteration(self) -> None:
        basket = Basket()
        item = Item("Apple", 0.50, 3)
        basket += item
        items = list(basket)
        assert items == [item]
    
    def test_iteration_empty(self) -> None:
        basket = Basket()
        items = list(basket)
        assert items == []


class TestBasketContains:
    """Test Basket membership testing."""
    
    def test_contains_true(self) -> None:
        basket = Basket()
        basket += Item("Apple", 0.50, 3)
        assert "Apple" in basket
    
    def test_contains_false(self) -> None:
        basket = Basket()
        basket += Item("Apple", 0.50, 3)
        assert "Banana" not in basket
    
    def test_contains_empty(self) -> None:
        basket = Basket()
        assert "Apple" not in basket


class TestBasketTotal:
    """Test Basket total calculation."""
    
    def test_total_empty(self) -> None:
        basket = Basket()
        assert basket.total() == 0.0
    
    def test_total_with_items(self) -> None:
        basket = Basket()
        basket += Item("Apple", 0.50, 3)  # 1.50
        basket += Item("Banana", 0.30, 2)  # 0.60
        assert basket.total() == 2.10


class TestBasketItemCount:
    """Test Basket item count."""
    
    def test_item_count_empty(self) -> None:
        basket = Basket()
        assert basket.item_count() == 0
    
    def test_item_count_with_quantities(self) -> None:
        basket = Basket()
        basket += Item("Apple", 0.50, 3)
        basket += Item("Banana", 0.30, 2)
        assert basket.item_count() == 5  # Total quantity
