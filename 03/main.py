def is_possible(tup):
    tup = sorted(tup)
    return tup[0] + tup[1] > tup[2]

with open("input") as file:
    data = [map(int, line.split()) for line in file]

print(len(filter(is_possible, data)))

new_data = []
for major_y in range(0, len(data), 3):
    for i in range(3):
        new_data.append([data[major_y+minor_y][i] for minor_y in range(3)])

print(len(filter(is_possible, new_data)))
