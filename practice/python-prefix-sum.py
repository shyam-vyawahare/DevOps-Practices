"""
Python Prefix Sum
DSA Practice

Problems:
1. Build a Prefix Sum Array
2. Range Sum Query
3. Subarray Sum Equals K

Prefix Sum:
Store cumulative sums to answer range-sum queries
efficiently.

Range Sum Query: O(1)
Subarray Sum Equals K: O(n) average time
"""


def build_prefix_sum(numbers):
    """Build cumulative sums with a leading zero."""

    prefix = [0]

    for number in numbers:
        prefix.append(prefix[-1] + number)

    return prefix


def range_sum(prefix, left, right):
    """
    Return the sum from index left to right, inclusive.
    Uses zero-based indexes.
    """

    if left < 0 or right < left or right >= len(prefix) - 1:
        raise ValueError("Invalid range")

    return prefix[right + 1] - prefix[left]


def subarray_sum_equals_k(numbers, target):
    """
    Count contiguous subarrays whose sum equals target.

    Works with positive, zero, and negative numbers.
    """

    prefix_count = {0: 1}
    current_sum = 0
    count = 0

    for number in numbers:
        current_sum += number

        count += prefix_count.get(current_sum - target, 0)

        prefix_count[current_sum] = (
            prefix_count.get(current_sum, 0) + 1
        )

    return count


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    numbers = [2, 4, 1, 7, 3, 6]

    # 1. Build Prefix Sum
    prefix = build_prefix_sum(numbers)

    print("Numbers:", numbers)
    print("Prefix Sum:", prefix)

    # 2. Range Sum Query
    left, right = 1, 4

    print(
        f"Sum from index {left} to {right}:",
        range_sum(prefix, left, right)
    )

    # 3. Subarray Sum Equals K
    values = [1, 2, 3, -2, 2]
    target = 3

    print("Array:", values)
    print(f"Subarrays with sum {target}:",
          subarray_sum_equals_k(values, target))
