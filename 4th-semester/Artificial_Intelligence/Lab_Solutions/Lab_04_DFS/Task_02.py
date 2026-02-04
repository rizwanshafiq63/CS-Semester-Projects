from collections import deque
from typing import Dict, List, Tuple, Set

# ---------- Graph (Romania map) ----------
Graph = Dict[str, List[Tuple[str, int]]]
romania: Graph = {
    "Arad": [("Zerind", 75), ("Sibiu", 140), ("Timisoara", 118)],
    "Zerind": [("Arad", 75), ("Oradea", 71)],
    "Oradea": [("Zerind", 71), ("Sibiu", 151)],
    "Timisoara": [("Arad", 118), ("Lugoj", 111)],
    "Lugoj": [("Timisoara", 111), ("Mehadia", 70)],
    "Mehadia": [("Lugoj", 70), ("Drobeta", 75)],
    "Drobeta": [("Mehadia", 75), ("Craiova", 120)],
    "Craiova": [("Drobeta", 120), ("Rimnicu Vilcea", 146), ("Pitesti", 138)],
    "Sibiu": [("Arad", 140), ("Oradea", 151), ("Fagaras", 99), ("Rimnicu Vilcea", 80)],
    "Fagaras": [("Sibiu", 99), ("Bucharest", 211)],
    "Rimnicu Vilcea": [("Sibiu", 80), ("Craiova", 146), ("Pitesti", 97)],
    "Pitesti": [("Rimnicu Vilcea", 97), ("Craiova", 138), ("Bucharest", 101)],
    "Bucharest": [("Fagaras", 211), ("Pitesti", 101), ("Giurgiu", 90), ("Urziceni", 85)],
    "Giurgiu": [("Bucharest", 90)],
    "Urziceni": [("Bucharest", 85), ("Hirsova", 98), ("Vaslui", 142)],
    "Hirsova": [("Urziceni", 98), ("Eforie", 86)],
    "Eforie": [("Hirsova", 86)],
    "Vaslui": [("Urziceni", 142), ("Iasi", 92)],
    "Iasi": [("Vaslui", 92), ("Neamt", 87)],
    "Neamt": [("Iasi", 87)],
}

# deterministic neighbor order (alphabetical by city name)
def nbrs(u: str) -> List[str]:
    return [v for v, _ in sorted(romania[u], key=lambda x: x[0])]

# ---------- BFS (records visit order & path) ----------
def bfs(start: str, goal: str):
    visited: Set[str] = set([start])
    q = deque([[start]])
    visit_order: List[str] = []
    while q:
        path = q.popleft()
        u = path[-1]
        visit_order.append(u)
        if u == goal:
            return path, visit_order
        for v in nbrs(u):
            if v not in visited:
                visited.add(v)
                q.append(path + [v])
    return None, visit_order

# ---------- DFS (recursive; first-found path; records visit order) ----------
def dfs(start: str, goal: str):
    visited: Set[str] = set()
    visit_order: List[str] = []
    path: List[str] = []

    def rec(u: str) -> bool:
        visited.add(u)
        visit_order.append(u)
        path.append(u)
        if u == goal:
            return True
        for v in nbrs(u):
            if v not in visited:
                if rec(v):
                    return True
                path.pop()  # backtrack
        return False

    found = rec(start)
    return (path if found else None), visit_order

# ---------- Helper to run and print a comparison ----------
def run_case(start: str, goal: str):
    bpath, bord = bfs(start, goal)
    dpath, dord = dfs(start, goal)

    print(f"\n=== Start: {start}  Goal: {goal} ===")
    print(f"BFS visited: {len(bord)}  | order: {bord}")
    print(f"DFS visited: {len(dord)}  | order: {dord}")
    print(f"BFS path: {bpath}")
    print(f"DFS path: {dpath}")

# ---------- Task 2 Demonstrations ----------

# Case A: BFS visits fewer nodes than DFS
# Reason: goal is one step away from start, but DFS first dives into a different branch (alphabetical order picks 'Arad' before 'Lugoj').
run_case("Timisoara", "Lugoj")

# Case B: BFS visits more nodes than DFS
# Reason: DFS goes straight down a chain to the goal, while BFS fans out layer by layer first.
run_case("Arad", "Bucharest")
