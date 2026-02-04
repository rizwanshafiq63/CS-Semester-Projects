# ---------- Romania road graph (edge weights = distances in km) ----------
ROMANIA = {
    "Arad": {"Zerind": 75, "Sibiu": 140, "Timisoara": 118},
    "Zerind": {"Arad": 75, "Oradea": 71},
    "Oradea": {"Zerind": 71, "Sibiu": 151},
    "Timisoara": {"Arad": 118, "Lugoj": 111},
    "Lugoj": {"Timisoara": 111, "Mehadia": 70},
    "Mehadia": {"Lugoj": 70, "Drobeta": 75},
    "Drobeta": {"Mehadia": 75, "Craiova": 120},
    "Craiova": {"Drobeta": 120, "Rimnicu Vilcea": 146, "Pitesti": 138},
    "Sibiu": {"Arad": 140, "Oradea": 151, "Fagaras": 99, "Rimnicu Vilcea": 80},
    "Fagaras": {"Sibiu": 99, "Bucharest": 211},
    "Rimnicu Vilcea": {"Sibiu": 80, "Pitesti": 97, "Craiova": 146},
    "Pitesti": {"Rimnicu Vilcea": 97, "Craiova": 138, "Bucharest": 101},
    "Bucharest": {"Fagaras": 211, "Pitesti": 101, "Giurgiu": 90, "Urziceni": 85},
    "Giurgiu": {"Bucharest": 90},
    "Urziceni": {"Bucharest": 85, "Hirsova": 98, "Vaslui": 142},
    "Hirsova": {"Urziceni": 98, "Eforie": 86},
    "Eforie": {"Hirsova": 86},
    "Vaslui": {"Urziceni": 142, "Iasi": 92},
    "Iasi": {"Vaslui": 92, "Neamt": 87},
    "Neamt": {"Iasi": 87},
}

def ida_star_min_cost(start: str, goal: str, graph=ROMANIA):
    """
    Iterative deepening on PATH COST (IDA* with h=0).
    Returns (path, total_cost) for a minimum-distance route from start to goal.
    """

    def h(_city: str) -> int:
        # zero heuristic -> pure cost-bounded iterative deepening (optimal and admissible)
        return 0

    # Depth-first search bounded by f = g + h <= bound
    def dfs(path: list[str], g: int, bound: int):
        """
        path: cities visited so far (last = current)
        g   : cost so far
        bound: current f-cost bound
        Returns:
          - if found: (path_copy, total_cost), bound
          - if not:   (None, smallest_f_exceeding_bound)  -> used to raise the next bound
        """
        city = path[-1]
        f = g + h(city)
        if f > bound:
            return None, f
        if city == goal:
            return (path[:], g), f

        min_excess = float("inf")
        for nxt, w in graph[city].items():
            if nxt in path:  # avoid cycles
                continue
            res, t = dfs(path + [nxt], g + w, bound)
            if res is not None:
                return res, t
            if t < min_excess:
                min_excess = t
        return None, min_excess

    # Start from heuristic bound (0 here) and increase to the smallest over-limit each time
    bound = h(start)
    path = [start]
    while True:
        result, t = dfs(path, 0, bound)
        if result is not None:
            return result  # (path, cost)
        if t == float("inf"):
            return None
        bound = t  # next bound = smallest f-cost that exceeded the previous bound


# ---- Demo: Arad -> Bucharest ----
best = ida_star_min_cost("Arad", "Bucharest")
if best:
    route, dist = best
    print("Optimal route:", " -> ".join(route))
    print("Total distance:", dist, "km")
else:
    print("No route found.")
    
# ==== ID_DFS ====
def iddfs_edges(start, goal, graph, max_depth=50):
    """Iterative Deepening on EDGE DEPTH (fewest hops). Returns first path found."""
    def dls(node, goal, limit, path, onpath):
        if node == goal:
            return path[:]
        if limit == 0:
            return None
        for nxt in graph[node]:
            if nxt in onpath:   # avoid cycles
                continue
            onpath.add(nxt); path.append(nxt)
            res = dls(nxt, goal, limit-1, path, onpath)
            if res: return res
            path.pop(); onpath.remove(nxt)
        return None

    for depth in range(max_depth + 1):
        res = dls(start, goal, depth, [start], {start})
        if res: return res
    return None

def path_cost(path, graph):
    return sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))

# Run pure ID-DFS (fewest edges)
path = iddfs_edges("Arad", "Bucharest", ROMANIA)
print("ID-DFS path (fewest edges):", " -> ".join(path))
print("Total km on that path:", path_cost(path, ROMANIA))
