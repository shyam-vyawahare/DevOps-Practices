"""
Python Union-Find (Disjoint Set Union)
DSA Practice

Operations:
1. Find the representative of a set
2. Union two sets
3. Check whether elements are connected
4. Count connected components

Optimizations:
- Path Compression
- Union by Rank

Applications:
- Cycle detection
- Network connectivity
- Kruskal's Minimum Spanning Tree
"""


class UnionFind:
    def __init__(self, size):
        if size < 0:
            raise ValueError("Size must be non-negative")

        self.parent = list(range(size))
        self.rank = [0] * size
        self.components = size

    def find(self, item):
        """Find the root representative with path compression."""

        if item < 0 or item >= len(self.parent):
            raise IndexError("Item index out of range")

        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])

        return self.parent[item]

    def union(self, first, second):
        """
        Merge two sets.
        Return True if they were separate; otherwise False.
        """

        root_first = self.find(first)
        root_second = self.find(second)

        if root_first == root_second:
            return False

        # Union by rank
        if self.rank[root_first] < self.rank[root_second]:
            root_first, root_second = root_second, root_first

        self.parent[root_second] = root_first

        if self.rank[root_first] == self.rank[root_second]:
            self.rank[root_first] += 1

        self.components -= 1
        return True

    def connected(self, first, second):
        """Check whether two elements belong to the same set."""

        return self.find(first) == self.find(second)

    def count_components(self):
        """Return the number of separate components."""

        return self.components


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    # Elements: 0, 1, 2, 3, 4, 5
    uf = UnionFind(6)

    print("Initial components:", uf.count_components())

    # Merge sets
    uf.union(0, 1)
    uf.union(1, 2)
    uf.union(3, 4)

    print("After unions:", uf.count_components())

    # Connectivity checks
    print("0 and 2 connected:", uf.connected(0, 2))
    print("0 and 3 connected:", uf.connected(0, 3))
    print("3 and 4 connected:", uf.connected(3, 4))

    # Merge two previously separate components
    uf.union(2, 4)

    print("After merging components:", uf.count_components())
    print("0 and 4 connected:", uf.connected(0, 4))
