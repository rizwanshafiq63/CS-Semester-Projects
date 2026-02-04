from typing import Dict, List, Tuple, Set

Graph = Dict[str, List[Tuple[str, int]]]

romania_graph: Graph = {
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

def dfs_path(graph: Graph, start: str, goal: str) -> Tuple[List[str], int, List[str]]:
    visited: Set[str] = set()
    visit_order: List[str] = []
    path: List[str] = []
    total_cost = 0

    # Deterministic neighbor order
    sorted_graph: Graph = {u: sorted(v, key=lambda x: x[0]) for u, v in graph.items()}
    # sorted_graph = graph

    def dfs(u: str) -> bool:
        nonlocal total_cost
        visited.add(u)
        visit_order.append(u)
        path.append(u)
        if u == goal:
            return True
        for v, w in sorted_graph[u]:
            if v not in visited:
                total_cost += w
                if dfs(v):
                    return True
                # backtrack
                total_cost -= w
                path.pop()
        return False

    found = dfs(start)
    if not found:
        return [], 0, visit_order
    return path, total_cost, visit_order

if __name__ == "__main__":
    path, cost, order = dfs_path(romania_graph, "Arad", "Bucharest")
    print("DFS visit order:")
    print(" -> ".join(order))
    print("\nPath from Arad to Bucharest (DFS first-found):")
    print(" -> ".join(path) if path else "No path found")
    print(f"Total distance along this DFS path: {cost}")
