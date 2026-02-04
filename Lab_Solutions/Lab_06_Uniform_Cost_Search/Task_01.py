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
# Uniform Cost Search Function (ROMANIA MAP)
# ---------------------------------------------
def UCS():
    initialState = 'Arad'
    goalState = 'Bucharest'

    # Romania Map Data (as Node Objects)
    graph = {
        'Arad': Node('Arad', None, [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)], 0),
        'Zerind': Node('Zerind', None, [('Arad', 75), ('Oradea', 71)], 0),
        'Oradea': Node('Oradea', None, [('Zerind', 71), ('Sibiu', 151)], 0),
        'Timisoara': Node('Timisoara', None, [('Arad', 118), ('Lugoj', 111)], 0),
        'Lugoj': Node('Lugoj', None, [('Timisoara', 111), ('Mehadia', 70)], 0),
        'Mehadia': Node('Mehadia', None, [('Lugoj', 70), ('Drobeta', 75)], 0),
        'Drobeta': Node('Drobeta', None, [('Mehadia', 75), ('Craiova', 120)], 0),
        'Craiova': Node('Craiova', None, [('Drobeta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)], 0),
        'Sibiu': Node('Sibiu', None, [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)], 0),
        'Fagaras': Node('Fagaras', None, [('Sibiu', 99), ('Bucharest', 211)], 0),
        'Rimnicu Vilcea': Node('Rimnicu Vilcea', None, [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)], 0),
        'Pitesti': Node('Pitesti', None, [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)], 0),
        'Bucharest': Node('Bucharest', None, [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90), ('Urziceni', 85)], 0),
        'Giurgiu': Node('Giurgiu', None, [('Bucharest', 90)], 0),
        'Urziceni': Node('Urziceni', None, [('Bucharest', 85), ('Hirsova', 98), ('Vaslui', 142)], 0),
        'Hirsova': Node('Hirsova', None, [('Urziceni', 98), ('Eforie', 86)], 0),
        'Eforie': Node('Eforie', None, [('Hirsova', 86)], 0),
        'Vaslui': Node('Vaslui', None, [('Urziceni', 142), ('Iasi', 92)], 0),
        'Iasi': Node('Iasi', None, [('Vaslui', 92), ('Neamt', 87)], 0),
        'Neamt': Node('Neamt', None, [('Iasi', 87)], 0),
    }

    frontier = dict()
    frontier[initialState] = (None, 0)
    explored = []

    while len(frontier) != 0:
        currentNode = findMin(frontier)
        parent, currentCost = frontier[currentNode]
        del frontier[currentNode]

        if graph[currentNode].state == goalState:
            return actionSequence(graph, initialState, goalState), currentCost

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
    result = UCS()
    if result:
        path, cost = result
        print("UCS Path:", " -> ".join(path))
        print("Total Cost:", cost)
    else:
        print("No Path Found")
