"""
Python Two Pointers
DSA Practice

Problems:
1. Pair Sum in a Sorted Array
2. Reverse an Array In Place
3. Remove Duplicates from a Sorted Array
4. Check Palindrome

Two Pointers:
Use two indexes to process a sequence efficiently,
often reducing O(n²) solutions to O(n).
"""


def pair_sum_sorted(numbers, target):
    """
    Return the indices of two numbers that sum to target.
    Input must be sorted in ascending order.

    Time: O(n) | Space: O(1)
    """

    left = 0
    right = len(numbers) - 1

    while left < right:
        total = numbers[left] + numbers[right]

        if total == target:
            return [left, right]
        elif total < target:
            left += 1
        else:
            right -= 1

    return []


def reverse_array(numbers):
    """Reverse a list in place."""

    left = 0
    right = len(numbers) - 1

    while left < right:
        numbers[left], numbers[right] = numbers[right], numbers[left]
        left += 1
        right -= 1

    return numbers


def remove_duplicates_sorted(numbers):
    """
    Remove duplicates from a sorted list in place.
    Return the number of unique elements.

    The unique values occupy numbers[:count].
    """

    if not numbers:
        return 0

    write = 1

    for read in range(1, len(numbers)):
        if numbers[read] != numbers[write - 1]:
            numbers[write] = numbers[read]
            write += 1

    return write


def is_palindrome(text):
    """Check a string using two pointers."""

    left = 0
    right = len(text) - 1

    while left < right:
        if text[left] != text[right]:
            return False

        left += 1
        right -= 1

    return True


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    # 1. Pair Sum
    numbers = [1, 2, 4, 6, 8, 9]
    target = 10

    result = pair_sum_sorted(numbers, target)
    print("Pair Sum Indices:", result)

    if result:
        print("Pair:", numbers[result[0]], numbers[result[1]])

    # 2. Reverse Array
    values = [10, 20, 30, 40, 50]
    print("Reversed Array:", reverse_array(values))

    # 3. Remove Duplicates
    values = [1, 1, 2, 2, 3, 4, 4, 5]
    count = remove_duplicates_sorted(values)

    print("Unique Count:", count)
    print("Unique Values:", values[:count])

    # 4. Palindrome
    word = "racecar"
    print(f"Is '{word}' a palindrome?", is_palindrome(word))
