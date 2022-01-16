import fileinput
from collections import deque

adjacency = {}
orien, first, type = input().split()

for line in fileinput.input():
    if line =='\n':
        continue
    st, fin = line.split()
    if st in adjacency:
        adjacency[st].append(fin)
    else:
        adjacency.update({st:[fin]})
    if orien == 'u':
        if fin in adjacency:
            adjacency[fin].append(st)
        else:
            adjacency.update({fin:[st]})
if type == 'd':
    dfs = deque()
    vis = set()
    dfs.append(first)
    while len(dfs) != 0:
        vertex = dfs.pop()
        if vertex not in vis:
            vis.add(vertex)
        else:
            continue
        print(vertex)
        if vertex in adjacency:
            for i in sorted(adjacency.get(vertex), reverse = True):
                dfs.append(i)
else:
    bfs = deque()
    vis = set()
    bfs.append(first)
    while len(bfs) != 0:
        vertex = bfs.popleft()
        if vertex not in vis:
            vis.add(vertex)
        else:
            continue
        print(vertex)
        if vertex in adjacency:
            for i in sorted(adjacency.get(vertex)):
                if i not in vis:
                    bfs.append(i)
