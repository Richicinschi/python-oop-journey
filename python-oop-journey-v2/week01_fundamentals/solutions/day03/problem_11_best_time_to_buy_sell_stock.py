"""Reference solution for Problem 11: Best Time to Buy and Sell Stock."""

from __future__ import annotations


def max_profit(prices: list[int]) -> int:
    """Calculate maximum profit from single buy-sell transaction.

    Algorithm:
    - Track the minimum price seen so far (best day to buy)
    - For each day, calculate profit if we sell today
    - Update maximum profit

    Key insight: The maximum profit on day i is prices[i] - min_price_before_i

    Args:
        prices: List of stock prices where prices[i] is price on day i.

    Returns:
        Maximum profit achievable, or 0 if no profit possible.

    Time Complexity: O(n) - single pass
    Space Complexity: O(1) - only tracking min price and max profit
    """
    if not prices or len(prices) < 2:
        return 0

    min_price = prices[0]
    max_profit_val = 0

    for price in prices[1:]:
        # Calculate profit if we sell at current price
        profit = price - min_price

        # Update maximum profit
        if profit > max_profit_val:
            max_profit_val = profit

        # Update minimum price seen so far
        if price < min_price:
            min_price = price

    return max_profit_val


def max_profit_brute_force(prices: list[int]) -> int:
    """Brute force solution for comparison (O(n^2)).

    Args:
        prices: List of stock prices.

    Returns:
        Maximum profit.
    """
    n = len(prices)
    max_profit_val = 0

    for i in range(n):
        for j in range(i + 1, n):
            profit = prices[j] - prices[i]
            max_profit_val = max(max_profit_val, profit)

    return max_profit_val


def max_profit_with_days(prices: list[int]) -> tuple[int, int, int]:
    """Extended version that also returns buy and sell days.

    Args:
        prices: List of stock prices.

    Returns:
        Tuple of (max_profit, buy_day, sell_day).
    """
    if not prices or len(prices) < 2:
        return 0, -1, -1

    min_price = prices[0]
    min_day = 0
    max_profit_val = 0
    buy_day = sell_day = 0

    for day, price in enumerate(prices[1:], start=1):
        profit = price - min_price

        if profit > max_profit_val:
            max_profit_val = profit
            buy_day = min_day
            sell_day = day

        if price < min_price:
            min_price = price
            min_day = day

    return max_profit_val, buy_day, sell_day
