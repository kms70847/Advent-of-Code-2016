import heapq
import collections
import itertools

def a_star(start, goal, heuristic, neighbors):
    closed_set = set()
    open_heap = [(0, start)]
    heapq.heapify(open_heap)
    open_set = {start}
    came_from = {}
    
    g_score = collections.defaultdict(lambda: float("inf"))
    g_score[start] = 0

    f_score = collections.defaultdict(lambda: float("inf"))
    f_score[start] = heuristic(start, goal)

    while open_set:
        _, current = heapq.heappop(open_heap)
        if current == goal:
            return reconstruct_path(came_from, current, start)
        open_set.remove(current)
        closed_set.add(current)
        for neighbor in neighbors(current):
            if neighbor in closed_set:
                continue
            tentative_g_score = g_score[current] + 1
            if neighbor not in open_set:
                heapq.heappush(open_heap, (tentative_g_score, neighbor))
                open_set.add(neighbor)
            elif tentative_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
    return None

def reconstruct_path(came_from, end, start):
    ret = [end]
    while end != start:
        end = came_from[end]
        ret.append(end)
    return list(reversed(ret))

def heuristic(a,b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def neighbors(pos):
    x,y = pos
    for dx, dy in ((0,1), (0,-1), (1,0), (-1,0)):
        if 0<= x+dx < width and 0 <= y+dy < height and data[dy+y][dx+x] != "#":
            yield (x+dx, y+dy)

with open("input") as file:
    data = file.read().strip().split("\n")

height = len(data)
width = len(data[0])
waypoints = {}
for x in range(width):
    for y in range(height):
        if data[y][x].isdigit():
            waypoints[int(data[y][x])] = (x,y)

#determine the optimal lengths between each pair of waypoints
lengths = {}
for i in range(len(waypoints)):
    for j in range(i+1, len(waypoints)):
        if i == j: continue
        #print i,j
        lengths[(i,j)] = lengths[(j,i)] = len(a_star(waypoints[i], waypoints[j], heuristic, neighbors)) - 1

def path_length(waypoints):
    return sum(lengths[a,b] for a,b in zip(waypoints, waypoints[1:]))

print min(path_length(ordering) for ordering in itertools.permutations(waypoints) if ordering[0]==0)
print min(path_length(ordering+(0,)) for ordering in itertools.permutations(waypoints) if ordering[0]==0)
