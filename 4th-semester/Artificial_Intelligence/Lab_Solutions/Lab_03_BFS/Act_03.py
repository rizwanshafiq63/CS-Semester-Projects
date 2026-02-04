# BFS Implementation for the figure's graph

graph = {
    'A': ['B', 'E', 'C'],   # A connects to B, E, C
    'B': ['A', 'D', 'E'],   # B connects to A, D, E
    'C': ['A', 'F', 'G'],   # C connects to A, F, G
    'D': ['B'],             # D connects to B
    'E': ['A', 'B'],        # E connects to A, B
    'F': ['C'],             # F connects to C
    'G': ['C']              # G connects to C
}

visited = []   # List for visited nodes
queue = []     # Initialize a queue

def bfs(visited, graph, node):  # function for BFS
    visited.append(node)
    queue.append(node)
    while queue:                # visit each node
        m = queue.pop(0)
        print(m, end=" ")
        for neighbour in graph[m]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)

# Driver Code
print("Following is the Breadth-First Search")
bfs(visited, graph, 'A')   # start at A
