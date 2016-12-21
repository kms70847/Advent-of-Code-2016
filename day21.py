import re
import itertools


class Matcher:
    """
    stateful representation of a regex match.
    keeps track of the result of the last `match` call.
    This is more convenient than assigning the result to a name manually,
    especially when doing several matches in the conditionals of a big if-elif block
    """
    def __init__(self, string):
        self.string = string
        self.last_match = None
    def match(self, pattern, *args, **kargs):
        self.last_match = re.match(pattern, self.string, *args, **kargs)
        return self.last_match
    def groups(self):
        return self.last_match.groups()

def rotated(seq, amt):
    amt %= len(seq)
    return seq[-amt:] + seq[:-amt]

def decode(instructions, line):
    line = list(line)
    for instruction in instructions:
        m = Matcher(instruction)
        if m.match(r"swap position (\d*) with position (\d)"):
            a, b = map(int, m.groups())
            line[a], line[b] = line[b], line[a]
        elif m.match(r"swap letter (.) with letter (.)"):
            a,b = m.groups()
            for i,c in enumerate(line):
                if c == a: line[i] = b
                if c == b: line[i] = a
        elif m.match(r"rotate (right|left) (\d*) steps?"):
            direction, count = m.groups()
            count = int(count)
            if direction == "left": count *= -1
            line = rotated(line, count)
        elif m.match(r"rotate based on position of letter (.)"):
            letter = m.groups()[0]
            idx = line.index(letter)
            rotate_count = idx + 1 + int(idx >= 4)
            line = rotated(line, rotate_count)
        elif m.match(r"reverse positions (\d*) through (\d*)"):
            start, end = map(int, m.groups())
            line[start:end+1] = reversed(line[start:end+1])
        elif m.match(r"move position (\d*) to position (\d*)"):
            start, end = map(int, m.groups())
            c = line[start]
            del line[start]
            line.insert(end, c)
        else:
            raise Exception("Parsing not implemented yet for line {}".format(repr(instruction)))

    return "".join(line)

def encode(line, instruction):
    line = list(line)
    m = Matcher(instruction)

    if m.match(r"swap position (\d*) with position (\d)"):
        a, b = map(int, m.groups())
        line[a], line[b] = line[b], line[a]
        return {"".join(line)}
    elif m.match(r"swap letter (.) with letter (.)"):
        a,b = m.groups()
        for i,c in enumerate(line):
            if c == a: line[i] = b
            if c == b: line[i] = a
        return {"".join(line)}
    elif m.match(r"rotate (right|left) (\d*) steps?"):
        direction, count = m.groups()
        count = int(count)
        if direction == "left": count *= -1
        line = rotated(line, -count)
        return {"".join(line)}
    elif m.match(r"rotate based on position of letter (.)"):
        candidates = set()
        for i in range(len(line)):
            candidate = "".join(rotated(line, i))
            if decode([instruction], candidate) == "".join(line):
                candidates.add(candidate)
        return candidates
    elif m.match(r"reverse positions (\d*) through (\d*)"):
        start, end = map(int, m.groups())
        line[start:end+1] = reversed(line[start:end+1])
        return {"".join(line)}
    elif m.match(r"move position (\d*) to position (\d*)"):
        end, start = map(int, m.groups())
        c = line[start]
        del line[start]
        line.insert(end, c)
        return {"".join(line)}
    else:
        raise Exception("Parsing not implemented yet for line {}".format(repr(instruction)))
    raise Exception("exited block unexpectedly")

with open("input") as file:
    instructions = file.read().strip().split("\n")

#part 1
print decode(instructions, "abcdefgh")

#part 2
candidates = {"fbgdceah"}
for instruction in reversed(instructions):
    candidates = {x for line in candidates for x in encode(line, instruction)}

assert len(candidates) == 1
print candidates.pop()