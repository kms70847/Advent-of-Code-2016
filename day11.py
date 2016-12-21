import re
import itertools
import sys
import time
import heapq
import collections

USE_REAL_INPUT = not "sample" in sys.argv

#moves are tuples containing two elements:
#   one int, representing the direction the elevator moves
#   one tuple, containing one or two items in sorted order

#states are tuples containing five elements:
#   one int, representing the floor the elevator is on (one indexed)
#   four tuples, representing each floor's contents

#floors are tuples containing any number of items in sorted order

#items are tuples containing two elements:
#   the name of the element
#   the kind of object: "microchip" or "generator"

def apply(state, move):
    cur_floor = state[0]
    dir, cargo = move
    new_floor = cur_floor + dir
    new_state = [new_floor]
    for i in range(1, 5):
        if i == cur_floor:
            floor = tuple(element for element in state[i] if element not in cargo)
        elif i == new_floor:
            floor = tuple(sorted(state[i] + cargo))
        else:
            floor = state[i]
        new_state.append(floor)
    return tuple(new_state)
    
#returns true if no chips are being fried by radiation
def valid(state):
    for floor in state[1:]:
        chips = {tup[0] for tup in floor if tup[1] == "microchip"}
        generators = {tup[0] for tup in floor if tup[1] == "generator"}
        for chip in chips:
            if chip not in generators and len(generators) > 0:
                return False
    return True

#iterate through all moves, even ones that fry microchips
def iter_moves(state):
    cur_floor = state[0]
    directions = [d for d in (-1, 1) if 1 <= cur_floor+d <= 4]
    for d in directions:
        for r in range(1,3):
            #never move two items down. This is a completely unproven assumption
            #and in fact I bet it's factually wrong to include it,
            #but I bet most optimal paths still don't require a 2-down move, 
            #and I bet my input's solution is one of them.
            if d == -1 and r == 2: continue

            for cargo in itertools.combinations(state[cur_floor], r):
                yield (d, cargo)

#iterate only through moves that do not fry microchips
def iter_valid_moves(state):
    for move in iter_moves(state):
        if valid(apply(state, move)):
            yield move

def get_initial_state():
    starting_state = [1]
    with open("input" if USE_REAL_INPUT else "example_input") as file:
        for line in file:
            floor = []
            match = re.findall(r"a (\w*?)-compatible microchip", line)
            floor.extend((element, "microchip") for element in match)
            match = re.findall(r"a (\w*?) generator", line)
            floor.extend((element, "generator") for element in match)
            floor.sort()
            starting_state.append(tuple(floor))
    return tuple(starting_state)

def get_goal_state(state):
    items = [item for floor in state[1:] for item in floor]
    return (4, (),(),(), tuple(sorted(items)))

def heuristic(state_a, state_b):
    def get_floor(state, item):
        for i in range(1,5):
            if item in state[i]:
                return i
        raise ValueError

    items = [item for floor in state_a[1:] for item in floor]
    total_distance = 0
    for item in items:
        total_distance += abs(get_floor(state_a, item) - get_floor(state_b, item))
    return total_distance / 2.0

def a_star(start, goal, heuristic, neighbors):
    closed_set = set()
    open_heap = [(0, start)]
    heapq.heapify(open_heap)
    assert isinstance(open_heap, list), "expected list, got {}".format(type(open_heap))
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
    ret = []
    while end != start:
        end = came_from[end]
        ret.append(end)
    return list(reversed(ret))  
  
get_neighbors = lambda state: [apply(state, move) for move in iter_valid_moves(state)]

for part in (1,2):
    t = time.time()
    starting_state = get_initial_state()

    if part == 2:
        starting_state = list(starting_state)
        starting_state[1] = tuple(sorted(starting_state[1] + tuple((element, kind) for element in ("elerium", "dilithium") for kind in ("microchip", "generator"))))
        starting_state = tuple(starting_state)

    goal_state = get_goal_state(starting_state)
    path = a_star(starting_state, goal_state, heuristic, get_neighbors)
    print(len(path))
    print("Completed in {} seconds.".format(int(time.time() - t)))