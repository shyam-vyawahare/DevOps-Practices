"""
Python Dynamic Programming
DSA Practice

Problems:
1. Fibonacci with Memoization
2. Climbing Stairs
3. 0/1 Knapsack

Dynamic Programming (DP):
Solve overlapping subproblems and store results
to avoid repeated calculations.
"""


from functools import lru_cache


@lru_cache(maxsize=None)
def fibonacci(n):
    """Calculate Fibonacci using memoization."""

    if n < 0:
        raise ValueError("n must be non-negative")

    if n <= 1:
        return n

    return fibonacci(n - 1) + fibonacci(n - 2)


def climbing_stairs(n):
    """
    Count ways to climb n stairs using steps of 1 or 2.

    Time Complexity: O(n)
    Space Complexity: O(1)
    """

    if n < 0:
        return 0

    if n <= 1:
        return 1

    previous, current = 1, 1

    for _ in range(2, n + 1):
        previous, current = current, previous + current

    return current


def knapsack_01(weights, values, capacity):
    """
    Return maximum value for the 0/1 Knapsack problem.

    Each item can be selected at most once.

    Time Complexity: O(n * capacity)
    Space Complexity: O(capacity)
    """

    if len(weights) != len(values):
        raise ValueError("Weights and values must have equal lengths")

    if capacity < 0 or any(weight <= 0 for weight in weights):
        raise ValueError("Capacity must be non-negative and weights positive")

    dp = [0] * (capacity + 1)

    for weight, value in zip(weights, values):
        for current_capacity in range(capacity, weight - 1, -1):
            dp[current_capacity] = max(
                dp[current_capacity],
                value + dp[current_capacity - weight]
            )

    return dp[capacity]


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    # 1. Fibonacci
    n = 10
    print(f"Fibonacci({n}):", fibonacci(n))

    # 2. Climbing Stairs
    stairs = 5
    print(
        f"Ways to climb {stairs} stairs:",
        climbing_stairs(stairs)
    )

    # 3. 0/1 Knapsack
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    capacity = 7

    print(
        "Maximum knapsack value:",
        knapsack_01(weights, values, capacity)
    )
