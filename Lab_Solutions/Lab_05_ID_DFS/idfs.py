# graph = {'A':['B','C','D'],
#          'B':['E','F'],
#          'C':['G','H'],
#          'D':['I','J'],
#          'E':['K','L'],
#          'F':['L','M'],
#          'G':['N'],
#          'H':['O','P'],
#          'I':['P','Q'],
#          'J':['R'],
#          'K':['S'],
#          'L':['T'],
#          'P':['U'],
#          'S':[],
#          'T':[],
#          'M':[],
#          'N':[],
#          'O':[],
#          'U':[],
#          'Q':[],
#          'R':[]}
graph = {
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

def idfs(graph, start, goal, max_depth):

    for depth_limit in range(max_depth + 1):
      
        print("Searching at depth limit:", depth_limit)
        opened = [[start, 0]]   
        closed = []

        while opened:
            node, depth = opened.pop(0)

            if node == goal:
                closed.append(node)
                return "Goal Reached", closed
            else:
                closed.append(node)
                if depth < depth_limit:
                  opened = [[child, depth+1] for child in graph[node] if child not in opened and child not in closed] + opened

        print(closed)

    return "Goal Not Found", []


msg, traversal = idfs(graph, 'Arad', 'Bucharest', 5)
print("\n", msg, "\nTraversal =", traversal)
