"""Problem 04: Zip Data - Solution."""

from __future__ import annotations


def pair_names_with_ages(names: list[str], ages: list[int]) -> list[tuple[str, int]]:
    """Pair each name with the corresponding age.

    Args:
        names: List of names.
        ages: List of ages.

    Returns:
        List of (name, age) tuples. Stops at shorter list.
    """
    return list(zip(names, ages))


def create_dictionary_from_pairs(
    keys: list[str],
    values: list[int],
) -> dict[str, int]:
    """Create a dictionary from keys and values lists.

    Args:
        keys: List of keys.
        values: List of values.

    Returns:
        Dictionary mapping keys to values.
    """
    return dict(zip(keys, values))


def transpose_matrix(matrix: list[list[int]]) -> list[tuple[int, ...]]:
    """Transpose a matrix (swap rows and columns).

    Args:
        matrix: A 2D list (list of rows).

    Returns:
        Transposed matrix as list of tuples.
    """
    return list(zip(*matrix))


def combine_three_lists(
    list1: list[str],
    list2: list[int],
    list3: list[str],
) -> list[tuple[str, int, str]]:
    """Combine three lists element-wise.

    Args:
        list1: First list (strings).
        list2: Second list (integers).
        list3: Third list (strings).

    Returns:
        List of tuples containing one element from each list.
    """
    return list(zip(list1, list2, list3))
