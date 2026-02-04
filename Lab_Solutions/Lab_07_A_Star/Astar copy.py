from operator import itemgetter

graph = {'Arad': [['Zerind', 75, 374], ['Timisoara', 118, 329], ['Sibiu', 140, 253]],
         'Zerind': [['Oradea', 71, 380], ['Arad', 75, 366]],
         'Oradea': [['Zerind', 71, 374], ['Sibiu', 151, 253]],
         'Sibiu': [['Rimniciu Vilcea', 80, 193], ['Fagaras', 99, 176], ['Arad', 140, 366], ['Oradea', 151, 380]],
         'Fagaras': [['Sibiu', 99, 253], ['Bucharest', 211, 0]],
         'Rimniciu Vilcea': [['Pitesti', 97, 100], ['Craiova', 146, 160], ['Sibiu', 80, 253]],
         'Timisoara': [['Lugoj', 111, 244], ['Arad', 118, 366]],
         'Lugoj': [['Mehadia', 70, 241], ['Timisoara', 111, 329]],
         'Mehadia': [['Lugoj', 70, 244], ['Dobreta', 75, 242]],
         'Dobreta': [['Mehadia', 75, 241], ['Craiova', 120, 160]],
         'Pitesti': [['Craiova', 138, 160], ['Bucharest', 101, 0]],
         'Craiova': [['Pitesti', 138, 100], ['Dobreta', 120, 242], ['Rimniciu Vilcea', 146, 193]],
         'Bucharest': [['Giurgiu', 90, 77], ['Urziceni', 85, 80], ['Fagaras', 211, 178], ['Pitesti', 101, 100]],
         'Giurgiu': [['Bucharest', 90, 0]],
         'Urziceni': [['Vaslui', 142, 199], ['Hirsova', 98, 151], ['Bucharest', 85, 0]],
         'Vaslui': [['Lasi', 92, 226], ['Urziceni', 142, 80]],
         'Lasi': [['Neamt', 87, 234], ['Vaslui', 92, 199]],
         'Neamt': [['Lasi', 87, 226]],
         'Hirsova': [['Eforie', 86, 161], ['Urziceni', 98, 80]],
         'Eforie': [['Hirsova', 86, 151]], }

def astarik_traversal(graph, start, goal):
    # [node_name, g_cost, h_cost, path]
    opened = [[start[0], start[1], start[2], [start[0]]]]
    # opened = [start]
    closed = []
    
    while opened:
        node = opened.pop(0)
        print('current',node)
        
        if node[0] == goal[0]:
          closed.append(node)
          print('Closed:',closed)
          return node[3]
        else:
            closed.append(node)
            print('Closed:',closed)
            fresh_opened = [node[0] for node in opened]
            fresh_closed = [node[0] for node in closed]
            
            for item in graph[node[0]]:
                child_name = item[0]
                step_cost = item[1]
                h_cost = item[2]
                if item[0] not in fresh_opened and item[0] not in fresh_closed:
                    new_g = node[1] + step_cost
                    new_path = node[3] + [child_name]
                    opened.append([child_name, new_g, h_cost, new_path])
            # opened = opened + [[item[0],closed[-1][1]+item[1],item[2]] for item in graph[node[0]] if item[0] not in fresh_closed] #]
            print ('Open:',opened)
            
        opened.sort(key=lambda element:element[1]+element[2])
        #opened.sort(key=sort_key)
        print('Sorted Open:',opened)
        print("-" * 60)
    return 'GOAL Not FOUND'

def astar_traversal_dict(graph, start, goal):
    # opened items: [node_name, g_cost, h_cost]
    opened = [[start[0], start[1], start[2]]]
    closed = []

    # parent map
    parent = {start[0]: None}

    while opened:
        node = opened.pop(0)
        node_name, g_cost, h_cost = node
        print("Current:", node)

        if node_name == goal[0]:
            closed.append(node)
            print("Closed:", closed)
            
            # reconstruct path
            path = []
            curr = node_name
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            return path[::-1]  # reverse path

        closed.append(node)
        print("Closed:", closed)

        fresh_opened = [n[0] for n in opened]
        fresh_closed = [n[0] for n in closed]

        for child in graph[node_name]:
            child_name = child[0]
            step_cost = child[1]
            h2 = child[2]

            if child_name not in fresh_opened and child_name not in fresh_closed:
                new_g = g_cost + step_cost

                opened.append([child_name, new_g, h2])
                parent[child_name] = node_name  # store parent

        print("Open:", opened)
        opened.sort(key=lambda x: x[1] + x[2])
        print("Sorted Open:", opened)
        print("-" * 60)

    return "GOAL NOT FOUND"


#def sort_key(element):
    #print(element)
    #return element[1] + element[2]


# print(astarik_traversal(graph, ['Arad', 0, 244], ['Bucharest', 0, 0]))
print("Final Path:", astarik_traversal(graph, ['Arad', 0, 244], ['Bucharest', 0, 0]))
