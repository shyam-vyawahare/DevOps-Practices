"""
Python Kadane's Algorithm
DSA Practice

Problems:
1. Maximum Subarray Sum
2. Find the Start and End Indices of the Maximum Subarray

Time Complexity: O(n)
Space Complexity: O(1)

Kadane's Algorithm finds the maximum sum of a
non-empty contiguous subarray, even with negative numbers.
"""


def max_subarray_sum(numbers):
    """Return the maximum sum of a non-empty subarray."""

    if not numbers:
        raise ValueError("Input list must not be empty")

    current_sum = numbers[0]
    max_sum = numbers[0]

    for number in numbers[1:]:
        current_sum = max(number, current_sum + number)
        max_sum = max(max_sum, current_sum)

    return max_sum


def max_subarray_details(numbers):
    """
    Return (maximum_sum, start_index, end_index)
    for the maximum-sum contiguous subarray.
    """

    if not numbers:
        raise ValueError("Input list must not be empty")

    current_sum = numbers[0]
    max_sum = numbers[0]

    current_start = 0
    best_start = 0
    best_end = 0

    for index in range(1, len(numbers)):
        number = numbers[index]

        if number > current_sum + number:
            current_sum = number
            current_start = index
        else:
            current_sum += number

        if current_sum > max_sum:
            max_sum = current_sum
            best_start = current_start
            best_end = index

    return max_sum, best_start, best_end


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    numbers = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

    print("Array:", numbers)

    # 1. Maximum Subarray Sum
    result = max_subarray_sum(numbers)
    print("Maximum Subarray Sum:", result)

    # 2. Subarray Details
    total, start, end = max_subarray_details(numbers)

    print("Maximum Sum:", total)
    print("Start Index:", start)
    print("End Index:", end)
    print("Subarray:", numbers[start:end + 1])

    # 3. All-negative array
    negative_numbers = [-8, -3, -6, -2, -5]

    print(
        "\nMaximum sum for all-negative array:",
        max_subarray_sum(negative_numbers)
    )
