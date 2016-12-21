def fast_ring(x):
    result = 0
    for c in bin(x)[3:]: #not sure why you need to skip the leftmost bit, but whatever works...
        result *= 2
        if c == "1":
            result += 2
    return result + 1

def cross_ring(x):
    seq = list(range(1, x+1))
    idx = 0
    while len(seq) > 1:
        target = (idx + len(seq)/2) % len(seq)
        del seq[target]
        if target > idx:
            idx += 1
        idx = idx % len(seq)
    return seq[0]

puzzle_input = 3018458
print fast_ring(puzzle_input)
print cross_ring(puzzle_input)