from collections import deque

# Columns (0..5) left→right; Rows (0..5) top→bottom; goal is above (col=4,row=0)
start = (2, 2)  # column 2, row 2 (yellow node)
GOAL  = "G"

# Build adjacency to match the figure exactly
E = {}
def link(a,b): E.setdefault(a,set()).add(b); E.setdefault(b,set()).add(a)

# outer ring
for c in range(5): 
    link((c,0),(c+1,0))      # top
for r in range(5): 
    link((5,r),(5,r+1))      # right
for c in range(5): 
    link((c,5),(c+1,5))      # bottom
for r in range(5): 
    link((0,r),(0,r+1))      # left

# interior column under start
link((2,2),(2,3)); link((2,3),(2,4)); link((2,4),(2,5))

# right-side extras (dead-end mid, 2x2 at bottom-right)
link((4,2),(5,2))              # mid dead-end
link((4,5),(4,4)); link((4,4),(5,4)); link((4,5),(5,5))  # 2x2
link(GOAL,(4,0))               # goal above top row, col 4

# BFS
def bfs(s,g):
    q=deque([s]); parent={s:None}
    while q:
        u=q.popleft()
        if u==g: 
            break
        for v in E.get(u,()):
            if v not in parent:
                parent[v]=u; q.append(v)
    path=[]; cur=g
    while cur is not None: 
        path.append(cur); cur=parent[cur]
    return list(reversed(path))

path = bfs(start, GOAL)
moves = []
for (x1,y1),(x2,y2) in zip(path, path[1:]):
    if x2==x1 and y2==y1+1: 
        moves.append("D")
    elif x2==x1 and y2==y1-1: 
        moves.append("U")
    elif y2==y1 and x2==x1+1: 
        moves.append("R")
    elif y2==y1 and x2==x1-1:
        moves.append("L")
print(moves)  # ['D','D','D','R','R','U','R','U','U','U','U','L','U']
