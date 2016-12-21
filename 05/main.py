import hashlib
import itertools

def digest(bytes):
    h = hashlib.md5()
    h.update(bytes)
    return h.hexdigest()

base = b"wtnhxymk"

def part_one():
    found = []
    for i in itertools.count():
        s = digest(base + str(i))
        if s[:5] == "00000":
            found.append(s[5])
            print(i, found)
            if len(found) == 8: break

    print "".join(found)

def part_two():
    found = [None] * 8
    for i in itertools.count():
        s = digest(base + str(i))
        if s[:5] == "00000":
            idx = int(s[5], 16)
            c = s[6]
            if idx <= 7 and found[idx] is None:
                found[idx] = c
                print("".join(c if c is not None else "_" for c in found))
                if all(c is not None for c in found): break

part_one()
part_two()