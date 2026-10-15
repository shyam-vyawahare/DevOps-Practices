"""
Python Binary Search Patterns
DSA Practice

Problems:
1. Find First Occurrence
2. Find Last Occurrence
3. Search in Rotated Sorted Array
4. Find Square Root (Integer)
5. Find Peak Element

Time Complexity: O(log n)
Space Complexity: O(1)
"""


def first_occurrence(arr, target):
    """Find the first occurrence in a sorted array."""

    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            result = mid
            right = mid - 1

        elif arr[mid] < target:
            left = mid + 1

        else:
            right = mid - 1

    return result


def last_occurrence(arr, target):
    """Find the last occurrence in a sorted array."""

    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            result = mid
            left = mid + 1

        elif arr[mid] < target:
            left = mid + 1

        else:
            right = mid - 1

    return result


def search_rotated(arr, target):
    """
    Search in a rotated sorted array.
    Assumes all elements are distinct.
    """

    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid

        # Left half is sorted
        if arr[left] <= arr[mid]:

            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1

        # Right half is sorted
        else:
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1


def integer_square_root(number):
    """Find floor(sqrt(number)) using binary search."""

    if number < 0:
        raise ValueError("Number must be non-negative")

    left, right = 0, number
    answer = 0

    while left <= right:
        mid = (left + right) // 2

        if mid * mid <= number:
            answer = mid
            left = mid + 1
        else:
            right = mid - 1

    return answer


def find_peak_element(arr):
    """
    Find the index of a peak element.
    Adjacent elements must be unequal.

    A peak is greater than its existing neighbors.
    """

    if not arr:
        return -1

    left, right = 0, len(arr) - 1

    while left < right:
        mid = (left + right) // 2

        if arr[mid] < arr[mid + 1]:
            left = mid + 1
        else:
            right = mid

    return left


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    # 1. First and Last Occurrence
    numbers = [1, 2, 2, 2, 3, 4, 5]

    print("Array:", numbers)
    print("First occurrence of 2:", first_occurrence(numbers, 2))
    print("Last occurrence of 2:", last_occurrence(numbers, 2))

    # 2. Rotated Sorted Array
    rotated = [4, 5, 6, 7, 0, 1, 2]

    print("\nRotated Array:", rotated)
    print("Index of 0:", search_rotated(rotated, 0))

    # 3. Integer Square Root
    number = 27

    print("\nNumber:", number)
    print("Integer Square Root:", integer_square_root(number))

    # 4. Peak Element
    values = [1, 2, 3, 1]

    peak_index = find_peak_element(values)

    print("\nArray:", values)
    print("Peak Index:", peak_index)
    print("Peak Value:", values[peak_index])
