"""
Python Dijkstra's Shortest Path Algorithm
DSA Practice

Purpose:
Find the shortest distance from a source vertex
to every other reachable vertex in a weighted graph.

Requirements:
- Edge weights must be non-negative.
- Graph is represented as an adjacency list.

Time Complexity: O((V + E) log V) with a binary heap.
"""

import heapq


def dijkstra(graph, start):
    """Return shortest distances from start to all vertices."""

    if start not in graph:
        raise ValueError("Start vertex does not exist in the graph")

    # Validate edge weights and destination vertices.
    for vertex, edges in graph.items():
        for neighbor, weight in edges:
            if neighbor not in graph:
                raise ValueError(
                    f"Vertex {neighbor!r} referenced by {vertex!r} "
                    "is missing from the graph"
                )

            if weight < 0:
                raise ValueError("Dijkstra does not support negative weights")

    distances = {vertex: float("inf") for vertex in graph}
    distances[start] = 0

    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # Ignore outdated queue entries.
        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex]:
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

    return distances


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    # Each edge is represented as (neighbor, weight).
    graph = {
        "A": [("B", 4), ("C", 2)],
        "B": [("A", 4), ("C", 1), ("D", 5)],
        "C": [("A", 2), ("B", 1), ("D", 8), ("E", 10)],
        "D": [("B", 5), ("C", 8), ("E", 2)],
        "E": [("C", 10), ("D", 2)],
        "F": []  # Unreachable vertex
    }

    source = "A"
    shortest_distances = dijkstra(graph, source)

    print(f"Shortest distances from {source}:\n")

    for vertex, distance in shortest_distances.items():
        if distance == float("inf"):
            print(f"{source} -> {vertex}: Unreachable")
        else:
            print(f"{source} -> {vertex}: {distance}")
