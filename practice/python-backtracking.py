"""
Python Backtracking
DSA Practice

Problems:
1. Generate All Subsets
2. Generate All Permutations
3. Solve the N-Queens Problem

Backtracking:
Build a solution step by step. If a choice cannot
lead to a valid solution, undo it and try another.
"""


def generate_subsets(numbers):
    """Generate all possible subsets."""

    result = []
    subset = []

    def backtrack(index):
        if index == len(numbers):
            result.append(subset.copy())
            return

        # Include the current element
        subset.append(numbers[index])
        backtrack(index + 1)

        # Exclude the current element
        subset.pop()
        backtrack(index + 1)

    backtrack(0)
    return result


def generate_permutations(numbers):
    """Generate all permutations of distinct elements."""

    result = []
    path = []
    used = [False] * len(numbers)

    def backtrack():
        if len(path) == len(numbers):
            result.append(path.copy())
            return

        for index in range(len(numbers)):
            if used[index]:
                continue

            used[index] = True
            path.append(numbers[index])

            backtrack()

            # Undo the choice
            path.pop()
            used[index] = False

    backtrack()
    return result


def solve_n_queens(n):
    """
    Return all valid N-Queens board configurations.

    Each board is a list of strings.
    'Q' represents a queen and '.' an empty square.
    """

    if n < 1:
        return []

    result = []
    board = [["."] * n for _ in range(n)]

    columns = set()
    diagonals = set()       # row - column
    anti_diagonals = set()  # row + column

    def backtrack(row):
        if row == n:
            result.append(["".join(line) for line in board])
            return

        for column in range(n):
            diagonal = row - column
            anti_diagonal = row + column

            if (
                column in columns
                or diagonal in diagonals
                or anti_diagonal in anti_diagonals
            ):
                continue

            # Place queen
            board[row][column] = "Q"
            columns.add(column)
            diagonals.add(diagonal)
            anti_diagonals.add(anti_diagonal)

            backtrack(row + 1)

            # Remove queen and restore state
            board[row][column] = "."
            columns.remove(column)
            diagonals.remove(diagonal)
            anti_diagonals.remove(anti_diagonal)

    backtrack(0)
    return result


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    # 1. Subsets
    numbers = [1, 2, 3]

    print("Subsets:")
    for subset in generate_subsets(numbers):
        print(subset)

    # 2. Permutations
    print("\nPermutations:")
    for permutation in generate_permutations([1, 2, 3]):
        print(permutation)

    # 3. N-Queens
    n = 4
    solutions = solve_n_queens(n)

    print(f"\nN-Queens solutions for n={n}: {len(solutions)}")

    for index, solution in enumerate(solutions, start=1):
        print(f"\nSolution {index}:")
        for row in solution:
            print(row)
