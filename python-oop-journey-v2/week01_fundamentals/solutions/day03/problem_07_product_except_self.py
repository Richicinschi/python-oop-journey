"""Reference solution for Problem 07: Product of Array Except Self."""

from __future__ import annotations


def product_except_self(nums: list[int]) -> list[int]:
    """Return array where each element is product of all others.

    Uses prefix and suffix products approach:
    - First pass: compute prefix products (left to right)
    - Second pass: compute suffix products and combine (right to left)

    For position i:
    - prefix[i] = product of all elements before i
    - suffix[i] = product of all elements after i
    - answer[i] = prefix[i] * suffix[i]

    Args:
        nums: List of integers.

    Returns:
        List where answer[i] equals product of all elements except nums[i].

    Time Complexity: O(n) - two passes through array
    Space Complexity: O(1) extra (excluding output array)
    """
    n = len(nums)
    answer = [1] * n

    # First pass: compute prefix products
    # answer[i] will hold product of all elements before i
    prefix = 1
    for i in range(n):
        answer[i] = prefix
        prefix *= nums[i]

    # Second pass: compute suffix products and combine
    # Multiply answer[i] by product of all elements after i
    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]

    return answer


def product_except_self_with_arrays(nums: list[int]) -> list[int]:
    """Alternative solution using separate prefix and suffix arrays.

    More explicit but uses O(n) extra space.

    Args:
        nums: List of integers.

    Returns:
        List where answer[i] equals product of all elements except nums[i].
    """
    n = len(nums)

    # prefix[i] = product of nums[0] * nums[1] * ... * nums[i-1]
    prefix = [1] * n
    for i in range(1, n):
        prefix[i] = prefix[i - 1] * nums[i - 1]

    # suffix[i] = product of nums[i+1] * nums[i+2] * ... * nums[n-1]
    suffix = [1] * n
    for i in range(n - 2, -1, -1):
        suffix[i] = suffix[i + 1] * nums[i + 1]

    # answer[i] = prefix[i] * suffix[i]
    return [prefix[i] * suffix[i] for i in range(n)]
