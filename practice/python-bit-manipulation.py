"""
Python Bit Manipulation
DSA Practice

Topics:
1. Check Even or Odd
2. Check if a Number Is a Power of Two
3. Count Set Bits
4. Find the Unique Element
5. Set, Clear, and Toggle a Bit
"""


def is_even(number):
    """Check even/odd using the least significant bit."""
    return (number & 1) == 0


def is_power_of_two(number):
    """Check whether a positive number is a power of two."""
    return number > 0 and (number & (number - 1)) == 0


def count_set_bits(number):
    """Count 1s in the binary representation of a non-negative integer."""
    if number < 0:
        raise ValueError("Number must be non-negative")

    count = 0

    while number:
        number &= number - 1
        count += 1

    return count


def find_unique(numbers):
    """Find the element appearing once when others appear twice."""
    unique = 0

    for number in numbers:
        unique ^= number

    return unique


def set_bit(number, position):
    """Set a bit to 1."""
    return number | (1 << position)


def clear_bit(number, position):
    """Set a bit to 0."""
    return number & ~(1 << position)


def toggle_bit(number, position):
    """Flip a bit."""
    return number ^ (1 << position)


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    number = 12

    print("Number:", number)
    print("Binary:", bin(number))
    print("Is even:", is_even(number))
    print("Is power of two:", is_power_of_two(number))
    print("Set bits:", count_set_bits(number))

    numbers = [4, 1, 2, 1, 2]
    print("Unique element:", find_unique(numbers))

    value = 10  # Binary: 1010
    position = 0

    print("\nOriginal:", value, bin(value))
    print("Set bit:", set_bit(value, position))
    print("Clear bit:", clear_bit(value, 1))
    print("Toggle bit:", toggle_bit(value, position))
