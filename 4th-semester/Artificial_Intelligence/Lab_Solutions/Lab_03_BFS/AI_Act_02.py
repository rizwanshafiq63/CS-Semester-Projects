from collections import deque
from typing import Dict, List, Tuple, Optional

# ----- Graph setup (undirected, weighted) -----
# Adjacency list: each node maps to a list of (neighbor, weight)
Graph = Dict[str, List[Tuple[str, int]]]

graph: Graph = {
    "A": [("B", 6), ("C", 9), ("E", 1)],
    "B": [("A", 6), ("E", 4), ("D", 3)],
    "C": [("A", 9), ("F", 2), ("G", 3), ("E", 6)],
    "D": [("B", 3), ("E", 5), ("F", 7)],
    "E": [("A", 1), ("B", 4), ("D", 5), ("F", 6), ("C", 6)],
    "F": [("C", 2), ("E", 6), ("D", 7), ("G", 3)],
    "G": [("C", 3), ("F", 3)],
}

# ----- BFS for fewest-edges path -----
def bfs_shortest_path(graph: Graph, start: str, goal: str) -> Optional[List[str]]:
    """Return a shortest (fewest-edges) path from start to goal using BFS, or None if unreachable."""
    if start == goal:
        return [start]

    visited = set([start])
    parent: Dict[str, Optional[str]] = {start: None}
    q = deque([start])

    while q:
        u = q.popleft()
        for v, _w in graph.get(u, []):
            if v not in visited:
                visited.add(v)
                parent[v] = u
                if v == goal:
                    # reconstruct path
                    path = [v]
                    while parent[path[-1]] is not None:
                        path.append(parent[path[-1]])
                    path.reverse()
                    return path
                q.append(v)
    return None

# ----- Sum edge weights along a given path -----
def path_cost(graph: Graph, path: List[str]) -> int:
    """Sum weights along a path using the graph's edge weights (assumes edges exist)."""
    total = 0
    for u, v in zip(path, path[1:]):
        # find the weight u->v
        for nbr, w in graph[u]:
            if nbr == v:
                total += w
                break
        else:
            raise ValueError(f"No edge between {u} and {v}")
    return total

# ----- Example run (A -> G) -----
if __name__ == "__main__":
    start, goal = "A", "G"
    path = bfs_shortest_path(graph, start, goal)
    if path is None:
        print(f"No path from {start} to {goal}.")
    else:
        cost = path_cost(graph, path)
        print("BFS path:", " -> ".join(path))
        print("Total cost:", cost)
