"""
Python String Manipulation
DevOps / DSA Practice

Common string operations:
- Reverse a string
- Check palindrome
- Count characters
- Count vowels
- Remove duplicate characters
- Check anagrams
"""


def reverse_string(text):
    """Return the reversed string."""
    return text[::-1]


def is_palindrome(text):
    """Check whether a string is a palindrome."""
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


def character_frequency(text):
    """Return the frequency of each character."""
    frequency = {}

    for char in text:
        frequency[char] = frequency.get(char, 0) + 1

    return frequency


def count_vowels(text):
    """Count vowels in a string."""
    vowels = "aeiou"
    count = 0

    for char in text.lower():
        if char in vowels:
            count += 1

    return count


def remove_duplicates(text):
    """Remove duplicate characters while preserving order."""
    result = set()
    output = []

    for char in text:
        if char not in result:
            result.add(char)
            output.append(char)

    return "".join(output)


def are_anagrams(first, second):
    """Check whether two strings are anagrams."""

    first = first.replace(" ", "").lower()
    second = second.replace(" ", "").lower()

    return sorted(first) == sorted(second)


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    text = "DevOps"

    print("Original:", text)
    print("Reversed:", reverse_string(text))

    palindrome_text = "Madam"
    print(
        "Is palindrome:",
        is_palindrome(palindrome_text)
    )

    print(
        "Character frequency:",
        character_frequency(text)
    )

    print("Vowel count:", count_vowels(text))

    duplicate_text = "programming"
    print(
        "Without duplicates:",
        remove_duplicates(duplicate_text)
    )

    print(
        "Are anagrams:",
        are_anagrams("listen", "silent")
    )
