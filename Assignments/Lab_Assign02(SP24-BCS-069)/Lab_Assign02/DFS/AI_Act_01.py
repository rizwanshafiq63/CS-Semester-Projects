class Node:
    # Node definition with state, parent, actions, and cost
    def __init__(self, state, parent, actions, totalCost):
        self.state = state
        self.parent = parent
        self.actions = actions    # only output states of those actions
        self.totalCost = totalCost


def actionSequence(graph, initialState, goalState):
    # returns a list of states starting from goal state moving upwards
    # parents until root node is reached
    solution = [goalState]
    currentParent = graph[goalState].parent

    while currentParent is not None:
        solution.append(currentParent)
        currentParent = graph[currentParent].parent

    solution.reverse()
    return solution


def DFS():
    initialState = 'A'
    goalState = 'D'

    # State space graph
    graph = {
        'A': Node('A', None, ['B', 'E', 'C'], None),
        'B': Node('B', None, ['D', 'E', 'A'], None),
        'C': Node('C', None, ['A', 'F', 'G'], None),
        'D': Node('D', None, ['B', 'E'], None),
        'E': Node('E', None, ['A', 'B', 'D'], None),
        'F': Node('F', None, ['C'], None),
        'G': Node('G', None, ['C'], None)
    }

    frontier = [initialState]  # stack (LIFO)
    explored = []

    while len(frontier) != 0:
        currentNode = frontier.pop(len(frontier) - 1)   # LIFO pop
        print("Current Node:", currentNode)
        explored.append(currentNode)
        currentChildren = 0

        for child in graph[currentNode].actions:
            if child not in frontier and child not in explored:
                graph[child].parent = currentNode
                if graph[child].state == goalState:
                    print("Explored:", explored)
                    return actionSequence(graph, initialState, goalState)
                currentChildren += 1
                frontier.append(child)

        if currentChildren == 0:
            del explored[len(explored) - 1]


if __name__ == "__main__":
    path = DFS()
    print("DFS Path:", path)
