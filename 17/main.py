import hashlib
import heapq
import collections

#compares equal to everything.
class Wildcard:
    def __eq__(self, other): return True
    def __ne__(self, other): return False

def digest(x):
    return hashlib.md5(x).hexdigest()

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
    x1,y1 = a[1]
    x2,y2 = b[1]
    return abs(x2-x1) + abs(y2-y1)

def neighbors(state):
    x,y = state[1]
    path = state[0]
    s = digest(prefix + path)
    if y > 0 and s[0] in "bcdef":
        yield (path + "U", (x, y-1))
    if y < 3 and s[1] in "bcdef":
        yield (path + "D", (x, y+1))
    if x > 0 and s[2] in "bcdef":
        yield (path + "L", (x-1, y))
    if x < 3 and s[3] in "bcdef":
        yield (path + "R", (x+1, y))

prefix = "gdjjyniy"
start = ("", (0,0))
goal = (Wildcard(), (3,3))
path = a_star(start, goal, heuristic, neighbors)
if path:
    print path[-1][0]
else:
    print "No path found"

to_explore = {start}
best = None
while to_explore:
    cur = to_explore.pop()
    if cur[1] == (3,3): #candidate for best
        if best is None or len(cur[0]) > len(best[0]):
            best = cur
    else:
        for neighbor in neighbors(cur):
            to_explore.add(neighbor)
if best:
    print len(best[0])
else:
    print "no valid path found"