with open("input") as file:
    raw_data = file.read()

data = [(item[0], int(item[1:])) for item in raw_data.split(", ")]

pos = 0+0j
heading = 1j
seen = {pos}
first_crossover_point = None
for dir_change, distance in data:
    heading *= (-1j if dir_change == "R" else 1j)
    for _ in range(distance):
        pos += heading
        if pos in seen and first_crossover_point is None:
            first_crossover_point = pos
        seen.add(pos)

taxicab_distance = lambda x: int(abs(x.real) + abs(x.imag))
print(taxicab_distance(pos))
print(taxicab_distance(first_crossover_point))