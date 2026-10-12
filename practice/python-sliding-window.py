"""
Python Sliding Window
DSA Practice

Problems:
1. Maximum Sum Subarray of Size K
2. Average of Every Window of Size K
3. Longest Substring Without Repeating Characters

Sliding Window:
Maintain a moving range over a sequence to avoid
recalculating results for every possible subarray.
"""


def max_sum_subarray(numbers, k):
    """
    Find the maximum sum of a subarray of size k.

    Time: O(n) | Space: O(1)
    """

    if k <= 0 or k > len(numbers):
        raise ValueError("k must be between 1 and the list length")

    window_sum = sum(numbers[:k])
    max_sum = window_sum

    for right in range(k, len(numbers)):
        window_sum += numbers[right]
        window_sum -= numbers[right - k]
        max_sum = max(max_sum, window_sum)

    return max_sum


def window_averages(numbers, k):
    """Calculate the average of each window of size k."""

    if k <= 0 or k > len(numbers):
        raise ValueError("k must be between 1 and the list length")

    window_sum = sum(numbers[:k])
    averages = [window_sum / k]

    for right in range(k, len(numbers)):
        window_sum += numbers[right] - numbers[right - k]
        averages.append(window_sum / k)

    return averages


def longest_unique_substring(text):
    """
    Find the length of the longest substring without
    repeating characters.

    Time: O(n) | Space: O(n)
    """

    last_seen = {}
    left = 0
    max_length = 0

    for right, char in enumerate(text):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1

        last_seen[char] = right
        max_length = max(max_length, right - left + 1)

    return max_length


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    numbers = [2, 1, 5, 1, 3, 2]

    # 1. Maximum Sum Subarray
    k = 3
    print("Numbers:", numbers)
    print(f"Maximum sum (window size {k}):", max_sum_subarray(numbers, k))

    # 2. Window Averages
    print(f"Averages (window size {k}):", window_averages(numbers, k))

    # 3. Longest Unique Substring
    text = "abcabcbb"
    print("String:", text)
    print("Longest unique substring length:", longest_unique_substring(text))
