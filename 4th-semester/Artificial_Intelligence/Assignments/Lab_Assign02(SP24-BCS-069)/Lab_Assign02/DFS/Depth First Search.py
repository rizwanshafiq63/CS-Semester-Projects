graph = {'A':['B','C','D'],
         'B':['E','F'],
         'C':['G','H'],
         'D':['I','J'],
         'E':['K','L'],
         'F':['L','M'],
         'G':['N'],
         'H':['O','P'],
         'I':['P','Q'],
         'J':['R'],
         'K':['S'],
         'L':['T'],
         'P':['U'],
         'S':[],
         'T':[],
         'M':[],
         'N':[],
         'O':[],
         'U':[],
         'Q':[],
         'R':[]}

def dfs_traversal(graph, start, goal):

    opened = [start]
    closed = []
    while opened:
        node = opened.pop(0)
        if node == goal:
          closed.append(node)
          return "Goal Reached", closed
        else:
          closed.append(node)
          opened = [child for child in graph[node] if child not in opened and child not in closed] + opened
    return 'GOAL Not FOUND'

msg, dfsTraversal = dfs_traversal(graph,'A','M')
print(msg,"\nDFS Traversal = ", dfsTraversal)