# -------- Lab 3 • Task 2 (BFS Maze) --------
# Follows the same conventions as Labs 1–3:
# - Node(state, parent, actions, total_cost)
# - Graph as a dict: state -> Node
# - BFS with a FIFO frontier and parent backpointers

from collections import deque

# ----- Node definition (as in Lab 3) -----
class Node:
    def __init__(self, state, parent=None, actions=None, total_cost=0):
        self.state = state          # here: (x, y) grid coordinate or goal's coordinate
        self.parent = parent        # parent Node for backtracking
        self.actions = actions or []  # list of neighbor states
        self.total_cost = total_cost

# ----- Build the maze graph to match the figure -----
# Coordinates: x = 0..5 left→right, y = 0..5 top→bottom
# The goal is above (4,0), so we model it at (4, -1) and link it to (4,0).

START = (2, 2)
GOAL  = (4, -1)

def make_maze_graph():
    graph = {}

    def ensure(state):
        if state not in graph:
            graph[state] = Node(state)
        return graph[state]

    def connect(a, b):
        A, B = ensure(a), ensure(b)
        if b not in A.actions: 
            A.actions.append(b)
        if a not in B.actions:
            B.actions.append(a)

    # Outer ring (square)
    for x in range(5): 
        connect((x, 0), (x + 1, 0))  # top edge
    for y in range(5):
        connect((5, y), (5, y + 1))  # right edge
    for x in range(5): 
        connect((x, 5), (x + 1, 5))  # bottom edge
    for y in range(5): 
        connect((0, y), (0, y + 1))  # left edge

    # Vertical corridor under the start
    connect((2, 2), (2, 3))
    connect((2, 3), (2, 4))
    connect((2, 4), (2, 5))

    # Right-side extras from the figure
    connect((4, 2), (5, 2))               # small dead-end spur in the middle right
    connect((4, 5), (4, 4))               # bottom-right 2x2 block
    connect((4, 4), (5, 4))
    connect((4, 5), (5, 5))

    # Goal node above the top row at column x=4
    connect(GOAL, (4, 0))

    # Make sure START exists
    ensure(START)

    return graph

# ----- BFS exactly as in Lab 3 (frontier queue + parent links) -----
def bfs(graph, start, goal):
    # reset parents (good practice if you reuse the graph)
    for node in graph.values():
        node.parent = None

    frontier = deque([start])
    visited = {start}
    graph[start].parent = None

    while frontier:
        current = frontier.popleft()
        if current == goal:
            break
        for child in graph[current].actions:
            if child not in visited:
                visited.add(child)
                graph[child].parent = graph[current]
                frontier.append(child)

    # Reconstruct path (states) from goal back to start
    if graph.get(goal) is None or graph[goal].parent is None and goal != start:
        return None  # no path

    path = []
    node = graph[goal]
    while node is not None:
        path.append(node.state)
        node = node.parent
    path.reverse()
    return path

# ----- Convert a path of coordinates to U/D/L/R moves -----
def to_moves(path):
    moves = []
    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        if x2 == x1 and y2 == y1 + 1: 
            moves.append("D")
        elif x2 == x1 and y2 == y1 - 1: 
            moves.append("U")
        elif y2 == y1 and x2 == x1 + 1: 
            moves.append("R")
        elif y2 == y1 and x2 == x1 - 1:
            moves.append("L")
        else:
            moves.append("?")  # safety
    return moves

# ----- Run it -----
graph = make_maze_graph()
path  = bfs(graph, START, GOAL)
moves = to_moves(path) if path else None

print("Path (states):", path)
print("Moves:", moves)
print("Steps:", len(moves) if moves else 0)
