favorite = 1362
#favorite = 10
def is_wall(x,y):
    val = x*x + 3*x + 2*x*y + y + y*y + favorite
    return bin(val).count("1") % 2 == 1    

def neighbors(x,y):
    deltas = ((0,1),(0,-1),(1,0),(-1,0))
    for delta in deltas:
        cur = (x+delta[0], y+delta[1])
        if cur[0] >= 0 and cur[1] >= 0 and not is_wall(*cur):
            yield cur

def bfs(quit_upon_finding_goal = True, max_depth=float("inf")):
    start = (1,1)
    end = (31, 39)
    pending = {start}
    paths = {start: None}
    cur_depth = 0
    while pending and cur_depth < max_depth:
        next_pending = set()
        for item in pending:
            for neighbor in neighbors(*item):
                if neighbor not in paths:
                    paths[neighbor] = item
                    next_pending.add(neighbor)
                    if neighbor == end: return paths
        pending = next_pending
        cur_depth += 1
    return paths

def reproduce_path(paths, end):
    ret = []
    while True:
        end = paths[end]
        if end is None: break
        ret.append(end)
    return ret

d = bfs()
print(len(reproduce_path(d, (31, 39))))

d = bfs(False, 50)
print(len(d))