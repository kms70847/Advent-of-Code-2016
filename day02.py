def matrix_to_dict(seq, empty_sentinel="0"):
    return {(x+1j*y):item for y,row in enumerate(seq) for x,item in enumerate(row) if item != empty_sentinel}

def get_digit_sequence(pad, instructions):
    deltas = dict((c,1j**i) for i,c in enumerate("DLUR", 1))
    pad = matrix_to_dict(pad)
    pos = next(k for k,v in pad.iteritems() if v=="5")
    digits = []
    for row in instructions:
        for c in row:
            if pos + deltas[c] in pad:
                pos += deltas[c]
        digits.append(pad[pos])
    return digits


with open("input") as file:
    instructions = file.read().strip().split("\n")

pads = ["""\
123
456
789""",

"""\
001
0234
56789
0ABC
00D"""]

for pad in pads:
    print(get_digit_sequence(pad.split(), instructions))
