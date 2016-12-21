def construct_graph(items, connected_func):
    graph = {}
    for a in items:
        if a not in graph:
            graph[a] = set()
        for b in items:
            if a is b: continue
            if connected_func(a,b):
                graph[a].add(b)
    return graph

def search(graph, start):
    seen = set()
    to_visit = {start}
    while to_visit:
        x = to_visit.pop()
        yield x
        seen.add(x)
        for neighbor in graph[x]:
            if neighbor not in seen:
                to_visit.add(neighbor)

def iter_islands(graph):
    to_visit = set(graph)
    while to_visit:
        x = to_visit.pop()
        island = {x}
        for item in search(graph, x):
            island.add(item)
        yield island
        to_visit -= island

def overlaps(a,b):
    return a[0] <= b[0] <= a[1] or \
           a[0] <= b[1] <= a[1] or \
           b[0] <= a[0] <= b[1] or \
           b[0] <= a[1] <= b[1] or \
           a[1]+1 == b[0] or \
           b[1]+1 == a[0]

def merged(tups):
    return (min(tup[0] for tup in tups), max(tup[1] for tup in tups))

with open("input") as file:
    data = {tuple(map(int, line.split("-"))) for line in file}

graph = construct_graph(data, overlaps)

merged_data = set()
for island in iter_islands(graph):
    merged_data.add(merged(island))

merged_data = sorted(merged_data)

#part 1
if merged_data[0][0] > 0:
    print(merged_data[0][0]-1)
else:
    print(merged_data[0][1]+1)

#part 2
total = 0
total += merged_data[0][0]
for a,b in zip(merged_data, merged_data[1:]):
    total += b[0] - a[1] - 1
total += 4294967295 - merged_data[-1][1]
print(total)