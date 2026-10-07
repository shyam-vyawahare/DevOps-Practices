"""
Python Heap Implementation
DevOps / DSA Practice

Python's heapq provides a Min Heap.

Operations:
- Push
- Pop minimum
- Peek minimum
- Heapify

Max Heap:
Python does not provide a direct Max Heap,
so negative values can be used.
"""

import heapq


def min_heap_example():
    """Demonstrate Min Heap operations."""

    heap = []

    # Insert elements
    heapq.heappush(heap, 40)
    heapq.heappush(heap, 10)
    heapq.heappush(heap, 30)
    heapq.heappush(heap, 20)

    print("Min Heap:", heap)

    # Peek minimum
    print("Minimum:", heap[0])

    # Remove minimum
    print("Removed:", heapq.heappop(heap))

    print("After pop:", heap)


def max_heap_example():
    """Demonstrate Max Heap using negative values."""

    heap = []

    values = [40, 10, 30, 20]

    for value in values:
        heapq.heappush(heap, -value)

    print("\nMax Heap:", [-value for value in heap])

    # Peek maximum
    print("Maximum:", -heap[0])

    # Remove maximum
    maximum = -heapq.heappop(heap)

    print("Removed:", maximum)
    print("After pop:", [-value for value in heap])


def heapify_example():
    """Convert an existing list into a Min Heap."""

    numbers = [40, 10, 30, 20, 5]

    print("\nOriginal list:", numbers)

    heapq.heapify(numbers)

    print("Heapified list:", numbers)
    print("Minimum:", numbers[0])


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    min_heap_example()

    max_heap_example()

    heapify_example()
