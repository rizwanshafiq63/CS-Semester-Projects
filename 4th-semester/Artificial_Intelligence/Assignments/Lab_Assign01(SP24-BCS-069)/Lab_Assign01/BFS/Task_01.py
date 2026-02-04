from collections import deque
from typing import Dict, List, Tuple, Optional

# ---------- Graph (undirected, weighted) ----------
# Each city maps to a list of (neighbor, distance) pairs
Graph = Dict[str, List[Tuple[str, int]]]

romania: Graph = {
    "Arad":       [("Zerind", 75), ("Timisoara", 118), ("Sibiu", 140)],
    "Zerind":     [("Arad", 75), ("Oradea", 71)],
    "Oradea":     [("Zerind", 71), ("Sibiu", 151)],
    "Sibiu":      [("Arad", 140), ("Oradea", 151), ("Fagaras", 99), ("Rimnicu Vilcea", 80)],
    "Timisoara":  [("Arad", 118), ("Lugoj", 111)],
    "Lugoj":      [("Timisoara", 111), ("Mehadia", 70)],
    "Mehadia":    [("Lugoj", 70), ("Drobeta", 75)],
    "Drobeta":    [("Mehadia", 75), ("Craiova", 120)],
    "Craiova":    [("Drobeta", 120), ("Rimnicu Vilcea", 146), ("Pitesti", 138)],
    "Rimnicu Vilcea": [("Sibiu", 80), ("Craiova", 146), ("Pitesti", 97)],
    "Fagaras":    [("Sibiu", 99), ("Bucharest", 211)],
    "Pitesti":    [("Rimnicu Vilcea", 97), ("Craiova", 138), ("Bucharest", 101)],
    "Bucharest":  [("Fagaras", 211), ("Pitesti", 101), ("Giurgiu", 90), ("Urziceni", 85)],
    "Giurgiu":    [("Bucharest", 90)],
    "Urziceni":   [("Bucharest", 85), ("Hirsova", 98), ("Vaslui", 142)],
    "Hirsova":    [("Urziceni", 98), ("Eforie", 86)],
    "Eforie":     [("Hirsova", 86)],
    "Vaslui":     [("Urziceni", 142), ("Iasi", 92)],
    "Iasi":       [("Vaslui", 92), ("Neamt", 87)],
    "Neamt":      [("Iasi", 87)],
}

# ---------- BFS: fewest-edges path ----------
def bfs_path(graph: Graph, start: str, goal: str) -> Optional[List[str]]:
    if start == goal:
        return [start]

    visited = set([start])
    parent: Dict[str, Optional[str]] = {start: None}
    q = deque([start])

    while q:
        u = q.popleft()
        for v, _w in graph.get(u, []):  # ignore weights in BFS
            if v not in visited:
                visited.add(v)
                parent[v] = u
                if v == goal:
                    # reconstruct path from goal back to start
                    path = [v]
                    while parent[path[-1]] is not None:
                        path.append(parent[path[-1]])
                    path.reverse()
                    return path
                q.append(v)
    return None

# ---------- Sum distances along the path ----------
def path_distance(graph: Graph, path: List[str]) -> int:
    total = 0
    for u, v in zip(path, path[1:]):
        for nbr, d in graph[u]:
            if nbr == v:
                total += d
                break
        else:
            raise ValueError(f"No road between {u} and {v}")
    return total

# ---------- Demo: Arad -> Bucharest ----------
if __name__ == "__main__":
    start, goal = "Arad", "Bucharest"
    path = bfs_path(romania, start, goal)
    if path is None:
        print(f"No path found from {start} to {goal}.")
    else:
        dist = path_distance(romania, path)
        print("BFS path (fewest cities):", " -> ".join(path))
        print("Total distance on that path:", dist, "km")
