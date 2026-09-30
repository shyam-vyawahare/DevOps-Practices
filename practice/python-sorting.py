"""
Python Sorting Algorithms
DevOps / DSA Practice

Algorithms:
1. Bubble Sort
2. Selection Sort
3. Insertion Sort

All three algorithms have:
Average/Worst-case Time Complexity → O(n²)
"""


def bubble_sort(arr):
    """Sort a list using Bubble Sort."""

    arr = arr.copy()

    for i in range(len(arr)):
        swapped = False

        for j in range(0, len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break

    return arr


def selection_sort(arr):
    """Sort a list using Selection Sort."""

    arr = arr.copy()

    for i in range(len(arr)):
        min_index = i

        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j

        arr[i], arr[min_index] = arr[min_index], arr[i]

    return arr


def insertion_sort(arr):
    """Sort a list using Insertion Sort."""

    arr = arr.copy()

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    numbers = [64, 25, 12, 22, 11]

    print("Original:", numbers)

    print("Bubble Sort:", bubble_sort(numbers))

    print("Selection Sort:", selection_sort(numbers))

    print("Insertion Sort:", insertion_sort(numbers))
