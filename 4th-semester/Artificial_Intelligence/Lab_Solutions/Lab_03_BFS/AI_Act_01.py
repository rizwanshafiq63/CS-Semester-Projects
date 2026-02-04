from collections import deque

# ----- Node definition -----
class Node:
    def __init__(self, state, parent=None, actions=None, total_cost=0):
        self.state = state
        self.parent = parent
        self.actions = actions or []    # neighbors (for BFS)
        self.total_cost = total_cost

# ----- Graph (state-space) -----
# Matches the toy graph used in the lab (undirected edges represented as neighbor lists)
graph = {
    'A': Node('A', actions=['B', 'C', 'E']),
    'B': Node('B', actions=['A', 'D', 'E']),
    'C': Node('C', actions=['A', 'F', 'G']),
    'D': Node('D', actions=['B', 'E']),
    'E': Node('E', actions=['A', 'B','D']),
    'F': Node('F', actions=['C']),
}

def action_sequence(graph, start, goal):
    """Backtrack from goal to start using parent links, then reverse."""
    path = []
    current = graph[goal]
    while current is not None:
        path.append(current.state)
        current = current.parent
    path.reverse()
    return path

def bfs(graph, start, goal):
    # reset parents (useful if you call bfs multiple times)
    for node in graph.values():
        node.parent = None

    frontier = deque([start])
    explored = set([start])  # mark when enqueued (classic BFS)
    graph[start].parent = None

    while frontier:
        current_state = frontier.popleft()
        if current_state == goal:
            return action_sequence(graph, start, goal)

        for child in graph[current_state].actions:
            if child not in explored:
                explored.add(child)
                graph[child].parent = graph[current_state]   # crucial parent link
                frontier.append(child)

    return None  # no path

# Run Activity 1-b: from A to F
solution_A_to_F = bfs(graph, 'A', 'F')
print(solution_A_to_F)  # -> ['A', 'C', 'F']
