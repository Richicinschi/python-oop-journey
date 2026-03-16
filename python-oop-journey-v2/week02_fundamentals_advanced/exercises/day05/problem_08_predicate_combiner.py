"""Problem 08: Predicate Combiner

Implement utilities to combine multiple predicate functions
using logical operations (AND, OR, NOT).

Hints:
    * Hint 1: A predicate is a function that returns bool. To combine them,
      write functions that return NEW functions. The new function calls
      the original predicates and combines results with logical operators.
    
    * Hint 2: For negate(predicate): return lambda x: not predicate(x)
      For both(p1, p2): return lambda x: p1(x) and p2(x)
      For all_of(*preds): return lambda x: all(p(x) for p in preds)
    
    * Hint 3: Lambda captures variables by reference, not by value.
      If you create lambdas in a loop, they'll all see the final value.
      But here predicates are passed as arguments, so they're bound correctly.

Debugging Tips:
    - "Predicates always return False": Check your logic - 'and' vs 'or'
      can be confusing when negating. Draw a truth table if needed.
    - "any_of returns True unexpectedly": any() returns True if ANY
      predicate returns True (including just one). Check your predicates.
    - Type errors: Ensure all predicates accept the same argument type.
      The combined predicate passes the same x to all predicates.
    - Empty predicates list: all_of() with no predicates should return
      a function that returns True (vacuous truth), any_of() returns False
"""

from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")

Predicate = Callable[[T], bool]


def negate(predicate: Predicate[T]) -> Predicate[T]:
    """Create a predicate that is the negation of the input.

    Args:
        predicate: The predicate to negate.

    Returns:
        A new predicate that returns the opposite result.

    Example:
        >>> is_even = lambda x: x % 2 == 0
        >>> is_odd = negate(is_even)
        >>> is_odd(3)
        True
    """
    raise NotImplementedError("Implement negate")


def both(pred1: Predicate[T], pred2: Predicate[T]) -> Predicate[T]:
    """Create a predicate that is true only when both predicates are true.

    Args:
        pred1: First predicate.
        pred2: Second predicate.

    Returns:
        A new predicate that implements logical AND.

    Example:
        >>> is_positive = lambda x: x > 0
        >>> is_even = lambda x: x % 2 == 0
        >>> is_positive_even = both(is_positive, is_even)
        >>> is_positive_even(4)
        True
        >>> is_positive_even(-4)
        False
        >>> is_positive_even(3)
        False
    """
    raise NotImplementedError("Implement negate")


def either(pred1: Predicate[T], pred2: Predicate[T]) -> Predicate[T]:
    """Create a predicate that is true when at least one predicate is true.

    Args:
        pred1: First predicate.
        pred2: Second predicate.

    Returns:
        A new predicate that implements logical OR.

    Example:
        >>> is_negative = lambda x: x < 0
        >>> is_zero = lambda x: x == 0
        >>> is_non_positive = either(is_negative, is_zero)
        >>> is_non_positive(-5)
        True
        >>> is_non_positive(0)
        True
        >>> is_non_positive(5)
        False
    """
    raise NotImplementedError("Implement negate")


def all_of(*predicates: Predicate[T]) -> Predicate[T]:
    """Create a predicate that is true only when all predicates are true.

    Args:
        *predicates: Variable number of predicates.

    Returns:
        A new predicate that implements n-ary AND.

    Example:
        >>> p = all_of(lambda x: x > 0, lambda x: x < 10, lambda x: x % 2 == 0)
        >>> p(4)
        True
        >>> p(11)
        False
    """
    raise NotImplementedError("Implement negate")


def any_of(*predicates: Predicate[T]) -> Predicate[T]:
    """Create a predicate that is true when any predicate is true.

    Args:
        *predicates: Variable number of predicates.

    Returns:
        A new predicate that implements n-ary OR.

    Example:
        >>> p = any_of(lambda x: x < 0, lambda x: x > 100)
        >>> p(-5)
        True
        >>> p(50)
        False
        >>> p(150)
        True
    """
    raise NotImplementedError("Implement negate")


def none_of(*predicates: Predicate[T]) -> Predicate[T]:
    """Create a predicate that is true only when none of the predicates are true.

    Args:
        *predicates: Variable number of predicates.

    Returns:
        A new predicate that returns True only when all predicates return False.

    Example:
        >>> p = none_of(lambda x: x < 0, lambda x: x > 100)
        >>> p(50)
        True
        >>> p(-5)
        False
    """
    raise NotImplementedError("Implement negate")


def filter_with_predicate(items: list[T], predicate: Predicate[T]) -> list[T]:
    """Filter a list using a predicate function.

    Args:
        items: List of items to filter.
        predicate: Function to test each item.

    Returns:
        List of items for which predicate returns True.
    """
    raise NotImplementedError("Implement negate")
