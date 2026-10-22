"""
Python Monotonic Stack
DSA Practice

Problems:
1. Next Greater Element
2. Next Smaller Element
3. Stock Span Problem

A monotonic stack maintains elements in increasing
or decreasing order to solve certain array problems
efficiently.

Time Complexity: O(n) for each algorithm.
"""


def next_greater_elements(numbers):
    """Return the next greater element for each number."""

    result = [-1] * len(numbers)
    stack = []

    for index, number in enumerate(numbers):
        while stack and numbers[stack[-1]] < number:
            previous_index = stack.pop()
            result[previous_index] = number

        stack.append(index)

    return result


def next_smaller_elements(numbers):
    """Return the next smaller element for each number."""

    result = [-1] * len(numbers)
    stack = []

    for index, number in enumerate(numbers):
        while stack and numbers[stack[-1]] > number:
            previous_index = stack.pop()
            result[previous_index] = number

        stack.append(index)

    return result


def stock_span(prices):
    """
    Calculate the stock span for each day.

    Span = number of consecutive days, including today,
    with prices less than or equal to today's price.
    """

    spans = [0] * len(prices)
    stack = []

    for index, price in enumerate(prices):
        while stack and prices[stack[-1]] <= price:
            stack.pop()

        spans[index] = index + 1 if not stack else index - stack[-1]
        stack.append(index)

    return spans


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    numbers = [4, 5, 2, 10, 8]

    print("Array:", numbers)
    print("Next Greater Elements:", next_greater_elements(numbers))
    print("Next Smaller Elements:", next_smaller_elements(numbers))

    prices = [100, 80, 60, 70, 60, 75, 85]

    print("\nStock Prices:", prices)
    print("Stock Span:", stock_span(prices))
