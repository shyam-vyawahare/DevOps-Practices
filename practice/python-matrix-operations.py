"""
Python Matrix Operations
DSA Practice

Problems:
1. Matrix Transpose
2. Rotate Matrix 90 Degrees Clockwise
3. Spiral Traversal
4. Search in a Row-Wise and Column-Wise Sorted Matrix

Note:
These functions assume rectangular matrices.
"""


def transpose_matrix(matrix):
    """Convert rows into columns."""

    if not matrix:
        return []

    return [list(row) for row in zip(*matrix)]


def rotate_matrix_clockwise(matrix):
    """Rotate a square matrix 90 degrees clockwise."""

    if not matrix:
        return []

    n = len(matrix)

    if any(len(row) != n for row in matrix):
        raise ValueError("Matrix must be square")

    return [
        [matrix[n - 1 - row][col] for row in range(n)]
        for col in range(n)
    ]


def spiral_traversal(matrix):
    """Return matrix elements in spiral order."""

    if not matrix or not matrix[0]:
        return []

    top = 0
    bottom = len(matrix) - 1
    left = 0
    right = len(matrix[0]) - 1

    result = []

    while top <= bottom and left <= right:

        # Traverse from left to right
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1

        # Traverse from top to bottom
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1

        # Traverse from right to left
        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1

        # Traverse from bottom to top
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1

    return result


def search_sorted_matrix(matrix, target):
    """
    Search a matrix sorted by rows and columns.
    Return (row, column), or None if not found.
    """

    if not matrix or not matrix[0]:
        return None

    rows = len(matrix)
    cols = len(matrix[0])

    if any(len(row) != cols for row in matrix):
        raise ValueError("Matrix must be rectangular")

    row = 0
    col = cols - 1

    while row < rows and col >= 0:
        value = matrix[row][col]

        if value == target:
            return row, col

        if value > target:
            col -= 1
        else:
            row += 1

    return None


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    print("Original Matrix:")
    for row in matrix:
        print(row)

    print("\nTranspose:")
    for row in transpose_matrix(matrix):
        print(row)

    print("\nRotated 90 Degrees Clockwise:")
    for row in rotate_matrix_clockwise(matrix):
        print(row)

    print("\nSpiral Traversal:")
    print(spiral_traversal(matrix))

    sorted_matrix = [
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9]
    ]

    target = 6

    print(f"\nPosition of {target}:")
    print(search_sorted_matrix(sorted_matrix, target))
