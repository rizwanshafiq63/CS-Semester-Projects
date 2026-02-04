
def bfs_traversal(graph, start, goal):

    opened = [start]
    closed = []

    while opened:
        node = opened.pop(0)
        if node == goal:
            closed.append(node)
            return "Goal Reached", closed
        else:
            closed.append(node)
            children = graph.get(node, [])
            opened = opened + [child for child in children
                               if child not in opened and child not in closed
                               and child in graph]
    return "GOAL Not FOUND", []



graph = {
    'A' : ['B', 'F', 'I'],
    'B' : ['A', 'C', 'E'],
    'C' : ['B', 'E', 'D'],
    'D' : ['C', 'G', 'H'],
    'E' : ['B', 'C', 'G'],
    'F' : ['A', 'G'],
    'G' : ['D', 'E', 'F'],
    'H' : ['D'],
    'I' : ['A'],
}

# #  graph
msg, traversal = bfs_traversal(graph, 'A', 'H')
if (traversal == []):
    print(msg)
else:
    print("Traversal Order = ", traversal)


