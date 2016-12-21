import re

rect_re = re.compile(r"rect (\d*)x(\d*)")
rotate_row_re = re.compile(r"rotate row y=(\d*) by (\d*)")
rotate_col_re = re.compile(r"rotate column x=(\d*) by (\d*)")

height = 6
width = 50
field = [[0 for x in range(width)] for y in range(height)]

with open("input") as file:
    for line in file:
        if rect_re.match(line):
            x,y = map(int, rect_re.match(line).groups())
            for i in range(x):
                for j in range(y):
                    if i < width and j < height:
                        field[j][i] = 1
        elif rotate_row_re.match(line):
            y, amt = map(int, rotate_row_re.match(line).groups())
            field[y] = [field[y][(i-amt)%width] for i in range(width)]
        elif rotate_col_re.match(line):
            x, amt = map(int, rotate_col_re.match(line).groups())
            new_col = [field[(j-amt)%height][x] for j in range(height)]
            for j in range(height):
                field[j][x] = new_col[j]
        else:
            raise Exception("Could not parse instruction " + repr(line))

print(sum(sum(row) for row in field))

for row in field:
    print("".join(" #"[val] for val in row))
