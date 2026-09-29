"""
Python Searching Algorithms
DevOps / DSA Practice

Algorithms:
1. Linear Search
2. Binary Search

Time Complexity:
Linear Search  → O(n)
Binary Search  → O(log n)

Note:
Binary Search requires a sorted list.
"""


def linear_search(arr, target):
    """Search for target using Linear Search."""

    for index, value in enumerate(arr):
        if value == target:
            return index

    return -1


def binary_search(arr, target):
    """Search for target using Binary Search."""

    left = 0
    right = len(arr) - 1

    while left <= right:
        middle = (left + right) // 2

        if arr[middle] == target:
            return middle

        if arr[middle] < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    numbers = [10, 20, 30, 40, 50, 60, 70]
    target = 50

    # Linear Search
    result = linear_search(numbers, target)

    if result != -1:
        print("Linear Search: Found at index", result)
    else:
        print("Linear Search: Not found")

    # Binary Search
    result = binary_search(numbers, target)

    if result != -1:
        print("Binary Search: Found at index", result)
    else:
        print("Binary Search: Not found")
