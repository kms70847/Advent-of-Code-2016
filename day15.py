import re
import itertools
import sys

def get_first_time(constraints):
    running_product = 1
    result = 0
    for lag, cycle_size, offset in constraints:
        while (result + offset + lag) % cycle_size != 0:
            result += running_product
        running_product *= cycle_size
    return result

constraints = []
with open("input") as file:
    for line in file:
        match = re.match(r"Disc #(\d*) has (\d*) positions; at time=0, it is at position (\d*).", line)
        if not match: raise Exception("Could not parse line {}".format(line))
        lag, cycle_size, offset = map(int, match.groups())
        constraints.append((lag, cycle_size, offset))
print(get_first_time(constraints))
constraints.append((constraints[-1][0]+1, 11, 0))
print(get_first_time(constraints))