"""
Python Recursion Practice
DevOps / DSA Practice

Recursion:
A function calling itself to solve a smaller version
of the same problem.

Examples:
- Factorial
- Fibonacci
- Sum of digits
- Power
- Reverse a string
- Recursive countdown
"""


def factorial(n):
    """Return factorial of n."""

    if n == 0 or n == 1:
        return 1

    return n * factorial(n - 1)


def fibonacci(n):
    """Return the nth Fibonacci number."""

    if n <= 1:
        return n

    return fibonacci(n - 1) + fibonacci(n - 2)


def sum_of_digits(n):
    """Return the sum of digits of a number."""

    n = abs(n)

    if n == 0:
        return 0

    return (n % 10) + sum_of_digits(n // 10)


def power(base, exponent):
    """Calculate base raised to exponent."""

    if exponent == 0:
        return 1

    return base * power(base, exponent - 1)


def reverse_string(text):
    """Reverse a string recursively."""

    if len(text) <= 1:
        return text

    return reverse_string(text[1:]) + text[0]


def countdown(n):
    """Print a countdown recursively."""

    if n <= 0:
        print("Done!")
        return

    print(n)
    countdown(n - 1)


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    print("Factorial of 5:", factorial(5))

    print("10th Fibonacci number:", fibonacci(10))

    print("Sum of digits of 12345:", sum_of_digits(12345))

    print("2^5:", power(2, 5))

    print(
        "Reversed:",
        reverse_string("DevOps")
    )

    print("\nCountdown:")
    countdown(5)
