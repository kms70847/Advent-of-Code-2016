import hashlib
import itertools
import time
import random
import string

def digest(bytes):
    h = hashlib.md5()
    h.update(bytes)
    return h.hexdigest()

base = b"wtnhxymk"

possible_chars = string.digits + "abcdef"

def part_one():
    last_printed_time = 0
    found = []
    for i in itertools.count():
        now = time.time()
        if now - last_printed_time > 0.10:
            print "\r" + "".join(found + [random.choice(possible_chars) for _ in range(8-len(found))]),
            last_printed_time = now
        s = digest(base + str(i))
        if s[:5] == "00000":
            found.append(s[5])
            if len(found) == 8: break

    print "\r" + "".join(found)

def part_two():
    last_printed_time = 0
    found = [None] * 8
    for i in itertools.count():
        now = time.time()
        if now - last_printed_time > 0.10:
            print "\r" + "".join(c if c is not None else random.choice(possible_chars) for c in found),
            last_printed_time = now
        s = digest(base + str(i))
        if s[:5] == "00000":
            idx = int(s[5], 16)
            c = s[6]
            if idx <= 7 and found[idx] is None:
                found[idx] = c
                if all(c is not None for c in found): break

part_one()

part_two()