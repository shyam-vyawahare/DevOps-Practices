"""
Python Hashing / Hash Map Practice
DevOps / DSA Practice

Python dictionaries provide hash-map functionality.

Common patterns:
- Key-value lookup
- Frequency counting
- Duplicate detection
- Two Sum
- Grouping values
"""


def frequency_count(items):
    """Count the frequency of each item."""

    frequency = {}

    for item in items:
        frequency[item] = frequency.get(item, 0) + 1

    return frequency


def find_duplicates(items):
    """Return duplicate values from a list."""

    seen = set()
    duplicates = set()

    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)

    return list(duplicates)


def two_sum(numbers, target):
    """
    Find indices of two numbers whose sum equals target.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """

    seen = {}

    for index, number in enumerate(numbers):
        complement = target - number

        if complement in seen:
            return [seen[complement], index]

        seen[number] = index

    return []


def first_non_repeating_character(text):
    """Return the first character that appears only once."""

    frequency = frequency_count(text)

    for char in text:
        if frequency[char] == 1:
            return char

    return None


def group_by_length(words):
    """Group words according to their length."""

    groups = {}

    for word in words:
        length = len(word)

        if length not in groups:
            groups[length] = []

        groups[length].append(word)

    return groups


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    numbers = [1, 2, 2, 3, 4, 4, 4, 5]

    print("Numbers:", numbers)

    # Frequency counting
    print("Frequency:", frequency_count(numbers))

    # Duplicate detection
    print("Duplicates:", find_duplicates(numbers))

    # Two Sum
    values = [2, 7, 11, 15]
    target = 9

    print(
        "Two Sum:",
        two_sum(values, target)
    )

    # First non-repeating character
    text = "swiss"

    print(
        "First non-repeating character:",
        first_non_repeating_character(text)
    )

    # Grouping
    words = [
        "cat",
        "dog",
        "apple",
        "bat",
        "banana"
    ]

    print(
        "Grouped by length:",
        group_by_length(words)
    )
