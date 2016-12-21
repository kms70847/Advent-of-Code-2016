def next_generation(row):
    num_cols = len(row)
    new_row = []
    for x in range(num_cols):
        new_row.append((x > 0 and row[x-1]) ^ (x < num_cols-1 and row[x+1]))
    return new_row

def safe_count(row, num_rows):
    total = row.count(False)
    for _ in range(num_rows-1):
        row = next_generation(row)
        total += row.count(False)
    return total

with open("input") as file:
    line = [c=="^" for c in file.read().strip()]

print safe_count(line, 40)
print safe_count(line, 400000)
