"""
Python Greedy Algorithms
DSA Practice

Problems:
1. Coin Change (Greedy)
2. Activity Selection
3. Fractional Knapsack

Note:
A greedy algorithm makes the best local choice at each step.
Greedy does not guarantee an optimal answer for every problem.
"""


def coin_change(coins, amount):
    """Find coins using a greedy strategy."""

    coins = sorted(coins, reverse=True)
    result = []

    for coin in coins:
        count = amount // coin

        if count > 0:
            result.extend([coin] * count)
            amount %= coin

    if amount != 0:
        return None

    return result


def activity_selection(activities):
    """
    Select the maximum number of non-overlapping activities.

    Each activity is (start, finish).
    """

    activities = sorted(activities, key=lambda item: item[1])

    selected = []
    last_finish = float("-inf")

    for start, finish in activities:
        if start >= last_finish:
            selected.append((start, finish))
            last_finish = finish

    return selected


def fractional_knapsack(items, capacity):
    """
    Maximize value by taking whole or fractional items.

    Each item is (value, weight).
    """

    items = sorted(
        items,
        key=lambda item: item[0] / item[1],
        reverse=True
    )

    total_value = 0.0
    selected = []

    for value, weight in items:
        if capacity <= 0:
            break

        if weight <= capacity:
            selected.append((value, weight, 1.0))
            total_value += value
            capacity -= weight
        else:
            fraction = capacity / weight
            selected.append((value, weight, fraction))
            total_value += value * fraction
            capacity = 0

    return total_value, selected


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    # 1. Coin Change
    coins = [1, 5, 10, 25]
    amount = 63

    print("Coin Change:", coin_change(coins, amount))

    # 2. Activity Selection
    activities = [
        (1, 3),
        (2, 5),
        (4, 7),
        (1, 8),
        (8, 9),
    ]

    selected = activity_selection(activities)

    print("Selected Activities:", selected)
    print("Number Selected:", len(selected))

    # 3. Fractional Knapsack
    items = [
        (60, 10),
        (100, 20),
        (120, 30),
    ]

    capacity = 50

    value, selected_items = fractional_knapsack(items, capacity)

    print("Maximum Knapsack Value:", value)
    print("Selected Items:", selected_items)
