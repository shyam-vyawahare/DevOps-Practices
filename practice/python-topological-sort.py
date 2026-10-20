"""
Python Topological Sort
DSA Practice

Algorithms:
1. Kahn's Algorithm (BFS)
2. DFS-Based Topological Sort

Purpose:
Order vertices in a Directed Acyclic Graph (DAG) so that
for every edge u -> v, u appears before v.

Applications:
- Task scheduling
- Course prerequisites
- Build systems
- CI/CD pipeline dependencies

Note:
Topological sorting is possible only for a DAG.
"""

from collections import deque


def topological_sort_kahn(graph):
    """
    Topological sort using Kahn's algorithm.

    Returns a list of vertices or raises ValueError if
    the graph contains a directed cycle.
    """

    indegree = {vertex: 0 for vertex in graph}

    # Calculate incoming edges for each vertex.
    for vertex in graph:
        for neighbor in graph[vertex]:
            if neighbor not in indegree:
                raise ValueError(f"Unknown vertex: {neighbor}")

            indegree[neighbor] += 1

    # Start with vertices that have no incoming edges.
    queue = deque(
        vertex for vertex in graph if indegree[vertex] == 0
    )

    order = []

    while queue:
        vertex = queue.popleft()
        order.append(vertex)

        for neighbor in graph[vertex]:
            indegree[neighbor] -= 1

            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(graph):
        raise ValueError("Graph contains a directed cycle")

    return order


def topological_sort_dfs(graph):
    """
    Topological sort using DFS.

    Returns a list of vertices or raises ValueError if
    the graph contains a directed cycle.
    """

    # 0 = unvisited, 1 = visiting, 2 = visited
    state = {vertex: 0 for vertex in graph}
    order = []

    def dfs(vertex):
        if state[vertex] == 1:
            raise ValueError("Graph contains a directed cycle")

        if state[vertex] == 2:
            return

        state[vertex] = 1

        for neighbor in graph[vertex]:
            if neighbor not in state:
                raise ValueError(f"Unknown vertex: {neighbor}")

            dfs(neighbor)

        state[vertex] = 2
        order.append(vertex)

    for vertex in graph:
        if state[vertex] == 0:
            dfs(vertex)

    order.reverse()
    return order


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    # Example: task dependencies in a CI/CD pipeline.
    # Each edge means the first task must run before the second.
    graph = {
        "Checkout": ["Test"],
        "Test": ["Build"],
        "Build": ["Security Scan", "Deploy"],
        "Security Scan": ["Deploy"],
        "Deploy": [],
        "Documentation": []
    }

    print("Kahn's Algorithm:")
    print(topological_sort_kahn(graph))

    print("\nDFS-Based Topological Sort:")
    print(topological_sort_dfs(graph))

    # Example of a graph containing a cycle.
    cyclic_graph = {
        "A": ["B"],
        "B": ["C"],
        "C": ["A"]
    }

    print("\nCycle Detection:")

    try:
        print(topological_sort_kahn(cyclic_graph))
    except ValueError as error:
        print(error)
