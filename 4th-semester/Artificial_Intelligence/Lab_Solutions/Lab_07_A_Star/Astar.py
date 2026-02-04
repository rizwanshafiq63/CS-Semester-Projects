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
    opened = [start]
    closed = []
    while opened:
        node = opened.pop(0)
        print('current',node)
        if node[0] == goal[0]:
          closed.append(node)
          print('closed',closed)
          return [a[0] for a in closed]
        else:
            closed.append(node)
            print('closed',closed)
            fresh_closed = [node[0] for node in closed]
            opened = opened + [[item[0],closed[-1][1]+item[1],item[2]] for item in graph[node[0]] if item[0] not in fresh_closed] #]
            print ('open',opened)
        opened.sort(key=lambda element:element[1]+element[2])
        #opened.sort(key=sort_key)
        print('sortedopen',opened)
    return 'GOAL Not FOUND'

#def sort_key(element):
    #print(element)
    #return element[1] + element[2]


print(astarik_traversal(graph, ['Arad', 0, 244], ['Bucharest', 0, 0]))