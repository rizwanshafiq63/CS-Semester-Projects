
def bfs_traversal(graph, start, goal):
    if start not in graph or goal not in graph:
        return "INVALID START/GOAL", [], []

    opened = [start]
    closed = []
    parent = {start: None}  # addition so we can reconstruct the path

    while opened:
        #Remove leftmost child from the opened list and call it node
        node = opened.pop(0)
        #If node is goal then return SUCCESS alogn with the traversal sequence.
        if node == goal:
            closed.append(node)
            path = []
            cur = node
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return "SUCCESS", path
        else:
            # Add node to closed (visited order)
            closed.append(node)
            # Generate children of node. If new, push to right end of opened.
            children = graph.get(node, [])
            opened = opened + [child for child in children
                               if child not in opened and child not in closed
                               and child in graph]  # guard for unknown names
            # record parents (only first time seen)
            for child in children:
                if child not in parent and child in graph:
                    parent[child] = node

    return "GOAL Not FOUND", []


def print_bfs_result(msg, path):
    print(msg)
    if path:
        print("Path:", " -> ".join(path))
    else:
        print("Path: (none)")


romania_graph = {
    "Arad": ["Zerind", "Timisoara", "Sibiu"],
    "Zerind": ["Arad", "Oradea"],
    "Oradea": ["Zerind", "Sibiu"],
    "Sibiu": ["Arad", "Oradea", "Fagaras", "Rimnicu Vilcea"],
    "Fagaras": ["Sibiu", "Bucharest"],
    "Rimnicu Vilcea": ["Sibiu", "Pitesti", "Craiova"],
    "Pitesti": ["Rimnicu Vilcea", "Craiova", "Bucharest"],
    "Craiova": ["Rimnicu Vilcea", "Pitesti", "Drobeta"],
    "Drobeta": ["Craiova", "Mehadia"],
    "Mehadia": ["Drobeta", "Lugoj"],
    "Lugoj": ["Mehadia", "Timisoara"],
    "Timisoara": ["Lugoj", "Arad"],
    "Bucharest": ["Fagaras", "Pitesti", "Giurgiu", "Urziceni"],
    "Giurgiu": ["Bucharest"],
    "Urziceni": ["Bucharest", "Vaslui", "Hirsova"],
    "Hirsova": ["Urziceni", "Eforie"],
    "Eforie": ["Hirsova"],
    "Vaslui": ["Urziceni", "Iasi"],
    "Iasi": ["Vaslui", "Neamt"],
    "Neamt": ["Iasi"],
}

print("\nRomania graph (adjacency list):")
for k in sorted(romania_graph.keys()):
    print(f"  {k}: {romania_graph[k]}")

# Prompt on Romania graph
print("\n=== STEP 1: Romania map  ===")
s1 = input("Enter START city (e.g., Arad): ").strip()
g1 = input("Enter GOAL city  (e.g., Bucharest): ").strip()
msg, path = bfs_traversal(romania_graph, s1, g1)
print_bfs_result(msg, path)

# print("\n=== STEP 2: BFS again on Romania map (choose other cities) ===")
# s2 = input("Enter START city: ").strip()
# g2 = input("Enter GOAL city: ").strip()
# msg, path = bfs_traversal(romania_graph, s2, g2)
# print_bfs_result(msg, path)

# Build a graph from user input, then run BFS
print("\n=== STEP 3: Build your own graph and run BFS ===")
try:
    n = int(input("How many vertices? ").strip())
except ValueError:
    n = 0

user_graph = {}

# read vertices
for i in range(n):
    v = input(f"  Vertex #{i+1} name: ").strip()
    if v == "":
        print("    (empty name ignored)")
        continue
    if v not in user_graph:
        user_graph[v] = []

# read edges
def add_undirected_edge(G, u, v):
    # ensure endpoints exist
    if u not in G:
        G[u] = []
    if v not in G:
        G[v] = []

    # reject self-loop
    if u == v:
        print("    Self-loop not allowed.")
        new = input("    Enter a different edge (u v): ").strip().split()
        if len(new) != 2:
            print("    Please enter exactly two vertex names.")
            return add_undirected_edge(G, u, v)  # ask again
        return add_undirected_edge(G, new[0], new[1])

    # check if the edge already exists (either direction)
    if v in G[u] and u in G[v]:
        print(f"    Edge '{u} {v}' already exists.")
        new = input("    Enter a different edge (u v): ").strip().split()
        if len(new) != 2:
            print("    Please enter exactly two vertex names.")
            return add_undirected_edge(G, u, v)  # ask again
        return add_undirected_edge(G, new[0], new[1])

    # add undirected edge
    G[u].append(v)
    G[v].append(u)
    print(f"    Added: {u} — {v}")


try:
    m = int(input("How many edges? (undirected) ").strip())
except ValueError:
    m = 0

print("Enter each edge as: u v")
for i in range(m):
    parts = input(f"  Edge #{i+1}: ").strip().split()
    if len(parts) != 2:
        print("    Skipped (please enter exactly two vertex names).")
        continue
    u, v = parts
    add_undirected_edge(user_graph, u, v)

print("\nYour graph (adjacency list):")
for k in sorted(user_graph.keys()):
    print(f"  {k}: {user_graph[k]}")

# run BFS on the user graph
s3 = input("\nEnter START vertex: ").strip()
g3 = input("Enter GOAL vertex: ").strip()
msg, path = bfs_traversal(user_graph, s3, g3)
print_bfs_result(msg, path)