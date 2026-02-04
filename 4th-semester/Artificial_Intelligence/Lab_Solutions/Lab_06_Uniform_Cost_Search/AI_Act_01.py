import math

# ---------------------------------------------
# Function to find the node in the frontier with the lowest cost
# ---------------------------------------------
def findMin(frontier):
    minV = math.inf
    node = ''
    for i in frontier:
        if minV > frontier[i][1]:
            minV = frontier[i][1]
            node = i
    return node

# ---------------------------------------------
# Function to backtrack from goal to start (build final solution path)
# ---------------------------------------------
def actionSequence(graph, initialState, goalState):
    solution = [goalState]
    currentParent = graph[goalState].parent
    while currentParent != None:
        solution.append(currentParent)
        currentParent = graph[currentParent].parent
    solution.reverse()
    return solution

# ---------------------------------------------
# Node Class Definition
# ---------------------------------------------
class Node:
    def __init__(self, state, parent, actions, totalCost):
        self.state = state
        self.parent = parent
        self.actions = actions  # List of tuples: [(Child, Cost), ...]
        self.totalCost = totalCost

# ---------------------------------------------
# Uniform Cost Search Function
# ---------------------------------------------
def UCS():
    initialState = 'C'
    goalState = 'B'

    # Graph is represented as Node objects in a dictionary
    graph = {
        'A': Node('A', None, [('B', 6), ('C', 9), ('E', 1)], 0),
        'B': Node('B', None, [('A', 6), ('D', 3), ('E', 4)], 0),
        'C': Node('C', None, [('A', 9), ('F', 2), ('G', 3)], 0),
        'D': Node('D', None, [('B', 3), ('E', 5), ('F', 7)], 0),
        'E': Node('E', None, [('A', 1), ('B', 4), ('D', 5), ('F', 6)], 0),
        'F': Node('F', None, [('C', 2), ('E', 6), ('D', 7)], 0),
        'G': Node('G', None, [('C', 3)], 0),
    }

    frontier = dict()
    frontier[initialState] = (None, 0)  # {state: (parent, totalCost)}
    explored = []

    while len(frontier) != 0:
        currentNode = findMin(frontier)
        parent, currentCost = frontier[currentNode]
        del frontier[currentNode]

        if graph[currentNode].state == goalState:
            return actionSequence(graph, initialState, goalState)

        explored.append(currentNode)

        for child, cost in graph[currentNode].actions:
            newCost = currentCost + cost

            if (child not in frontier) and (child not in explored):
                frontier[child] = (currentNode, newCost)
                graph[child].parent = currentNode
                graph[child].totalCost = newCost

            elif child in frontier:
                if frontier[child][1] > newCost:
                    frontier[child] = (currentNode, newCost)
                    graph[child].parent = currentNode
                    graph[child].totalCost = newCost

    return None

# ---------------------------------------------
# Run UCS
# ---------------------------------------------
if __name__ == "__main__":
    path = UCS()
    print("UCS Path:", " -> ".join(path) if path else "No Path Found")
