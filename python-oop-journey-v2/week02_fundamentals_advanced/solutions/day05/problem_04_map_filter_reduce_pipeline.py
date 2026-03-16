"""Problem 04: Map Filter Reduce Pipeline - Solution

Implement data processing pipelines using map, filter, and reduce
to transform and analyze collections of data.
"""

from __future__ import annotations

from functools import reduce
from typing import Callable, List, TypeVar

T = TypeVar("T")
U = TypeVar("U")


def process_numbers(
    numbers: list[int],
    transform: Callable[[int], int],
    predicate: Callable[[int], bool],
    reducer: Callable[[int, int], int],
    initial: int
) -> int:
    """Process numbers through a map-filter-reduce pipeline.

    First applies transform to all numbers, then filters by predicate,
    then reduces using the reducer function.

    Args:
        numbers: Input list of integers.
        transform: Function to transform each number.
        predicate: Function to filter transformed numbers.
        reducer: Function to combine two values.
        initial: Initial value for reduction.

    Returns:
        The result of the reduce operation.

    Example:
        >>> process_numbers(
        ...     [1, 2, 3, 4, 5],
        ...     lambda x: x * 2,
        ...     lambda x: x > 4,
        ...     lambda a, b: a + b,
        ...     0
        ... )
        24  # (2*3=6, 2*4=8, 2*5=10) -> 6+8+10 = 24
    """
    # Apply transformation
    transformed = map(transform, numbers)
    # Filter results
    filtered = filter(predicate, transformed)
    # Reduce to single value
    result = reduce(reducer, filtered, initial)
    return result


def analyze_products(products: list[dict]) -> dict:
    """Analyze a list of product dictionaries.

    Expected product format: {"name": str, "price": float, "category": str}

    Returns a dictionary with:
    - "total_value": sum of all prices
    - "expensive_count": count of products over $100
    - "avg_price": average price (0 if no products)
    - "categories": set of unique categories

    Args:
        products: List of product dictionaries.

    Returns:
        Dictionary with analysis results.
    """
    if not products:
        return {
            "total_value": 0.0,
            "expensive_count": 0,
            "avg_price": 0.0,
            "categories": set()
        }

    # Extract prices using map
    prices = list(map(lambda p: p["price"], products))

    # Calculate total value using reduce
    total_value = reduce(lambda a, b: a + b, prices, 0.0)

    # Count expensive products using filter
    expensive_count = len(list(filter(lambda p: p["price"] > 100, products)))

    # Calculate average
    avg_price = total_value / len(products)

    # Get unique categories using reduce
    categories = reduce(
        lambda cats, p: cats | {p["category"]},
        products,
        set()
    )

    return {
        "total_value": round(total_value, 2),
        "expensive_count": expensive_count,
        "avg_price": round(avg_price, 2),
        "categories": categories
    }


def pipeline_transform(
    data: list[T],
    *operations: Callable[[list[T]], list[T]]
) -> list[T]:
    """Apply a series of list transformations in sequence.

    Args:
        data: Initial list.
        *operations: Functions that transform a list to another list.

    Returns:
        The transformed list.
    """
    result = data.copy()
    for operation in operations:
        result = operation(result)
    return result


def count_by_predicate(
    items: list[T],
    predicates: list[Callable[[T], bool]]
) -> dict[int, int]:
    """Count items that match each predicate.

    Args:
        items: List of items to analyze.
        predicates: List of predicate functions.

    Returns:
        Dictionary mapping predicate index to count.

    Example:
        >>> count_by_predicate(
        ...     [1, 2, 3, 4, 5, 6],
        ...     [lambda x: x % 2 == 0, lambda x: x > 3]
        ... )
        {0: 3, 1: 3}  # 3 even numbers, 3 numbers > 3
    """
    return {
        i: len(list(filter(pred, items)))
        for i, pred in enumerate(predicates)
    }
