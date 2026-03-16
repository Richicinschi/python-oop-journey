"""Reference solution for Problem 09: Three Sum."""

from __future__ import annotations


def three_sum(nums: list[int]) -> list[list[int]]:
    """Find all unique triplets that sum to zero.

    Algorithm:
    1. Sort the array
    2. For each element nums[i], use two pointers to find pairs that sum to -nums[i]
    3. Skip duplicates to avoid duplicate triplets

    Args:
        nums: List of integers.

    Returns:
        List of unique triplets [a, b, c] where a + b + c = 0.

    Time Complexity: O(n^2) - sorting is O(n log n), then O(n^2) for two-pointer
    Space Complexity: O(1) extra (excluding output), or O(n) for sorting
    """
    result: list[list[int]] = []
    nums.sort()
    n = len(nums)

    for i in range(n - 2):
        # Skip duplicate values for the first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        # Early termination: if smallest possible sum > 0, break
        if nums[i] + nums[i + 1] + nums[i + 2] > 0:
            break

        # Early termination: if largest possible sum < 0, continue to next i
        if nums[i] + nums[n - 2] + nums[n - 1] < 0:
            continue

        # Two pointers for the remaining two elements
        left, right = i + 1, n - 1

        while left < right:
            total = nums[i] + nums[left] + nums[right]

            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                # Found a triplet
                result.append([nums[i], nums[left], nums[right]])

                # Skip duplicates for second element
                while left < right and nums[left] == nums[left + 1]:
                    left += 1

                # Skip duplicates for third element
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1

                left += 1
                right -= 1

    return result
