from collections import Counter

def rot(s,amt):
    return "".join(chr((ord(c) + amt - ord("a")) % 26 + ord("a")) if c.isalpha() else c for c in s)

def is_valid(row):
    d = Counter(row["name"].replace("-",""))
    x = sorted(d.items(), key=lambda t: (-t[1],t[0]))
    checksum = "".join(t[0] for t in x[:5])
    return checksum == row["checksum"]

data = []
with open("input") as file:
    for line in file:
        line, checksum = line.strip("]\n").split("[")
        name, _, sector = line.rpartition("-")
        data.append({"name": name, "sector": int(sector), "checksum": checksum})

data = filter(is_valid, data)

print(sum(row["sector"] for row in data))
for row in data:
    name = rot(row["name"], row["sector"])
    if "north" in name:
        print name, row["sector"]