"""
Python Graph Implementation
DevOps / DSA Practice

Representation:
- Adjacency List

Algorithms:
- Add vertex
- Add edge
- Display graph
- BFS traversal
- DFS traversal
"""

from collections import deque


class Graph:
    def __init__(self):
        self.graph = {}

    def add_vertex(self, vertex):
        """Add a vertex to the graph."""

        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, vertex1, vertex2):
        """Add an undirected edge."""

        self.add_vertex(vertex1)
        self.add_vertex(vertex2)

        self.graph[vertex1].append(vertex2)
        self.graph[vertex2].append(vertex1)

    def display(self):
        """Display the adjacency list."""

        for vertex, neighbors in self.graph.items():
            print(f"{vertex} -> {neighbors}")

    def bfs(self, start):
        """Breadth-First Search."""

        if start not in self.graph:
            return []

        visited = set()
        queue = deque([start])
        result = []

        visited.add(start)

        while queue:
            vertex = queue.popleft()
            result.append(vertex)

            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return result

    def dfs(self, start):
        """Depth-First Search."""

        if start not in self.graph:
            return []

        visited = set()
        result = []

        def traverse(vertex):
            visited.add(vertex)
            result.append(vertex)

            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    traverse(neighbor)

        traverse(start)

        return result


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    graph = Graph()

    graph.add_edge("Git", "Docker")
    graph.add_edge("Git", "Jenkins")
    graph.add_edge("Docker", "Kubernetes")
    graph.add_edge("Jenkins", "AWS")
    graph.add_edge("Kubernetes", "AWS")

    print("Graph:")
    graph.display()

    print("\nBFS:")
    print(graph.bfs("Git"))

    print("\nDFS:")
    print(graph.dfs("Git"))
