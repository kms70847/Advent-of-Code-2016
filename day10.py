import re
from collections import defaultdict

init_pattern = re.compile(r"value (\d*) goes to bot (\d*)")
neighbor_pattern = re.compile(r"bot (\d*) gives low to (bot|output) (\d*) and high to (bot|output) (\d*)")

bots = {}
outputs = defaultdict(list)

def init_bot(num):
    if num in bots: return
    bots[num] = {"holding": [], "neighbors":[]}

with open("input") as file:
    for line in file:
        init_match = init_pattern.match(line)
        neighbor_match = neighbor_pattern.match(line)
        if init_match:
            value, num = map(int, init_match.groups())
            init_bot(num)
            bots[num]["holding"].append(value)
        elif neighbor_match:
            num = int(neighbor_match.group(1))
            init_bot(num)
            for i in range(2):
                neighbor_kind = neighbor_match.group(2+2*i)
                neighbor_num = int(neighbor_match.group(3+2*i))
                bots[num]["neighbors"].append((neighbor_kind, neighbor_num))
        else:
            raise Exception("Unrecognized input {}".format(repr(line)))

pending = set()
for num, bot in bots.iteritems():
    if len(bot["holding"]) == 2:
        pending.add(num)

while True:
    next_pending = set()
    while pending:
        num = pending.pop()
        chips = sorted(bots[num]["holding"])
        if chips == [17, 61]: print num
        assert len(chips) == 2
        for chip, neighbor in zip(chips, bots[num]["neighbors"]):
            neighbor_kind, neighbor_num = neighbor
            if neighbor_kind == "output":
                outputs[neighbor_num].append(chip)
            elif neighbor_kind == "bot":
                bots[neighbor_num]["holding"].append(chip)
                if len(bots[neighbor_num]["holding"]) > 1:
                    next_pending.add(neighbor_num)
    if next_pending:
        pending = next_pending
    else:
        break

print outputs[0][0] * outputs[1][0] * outputs[2][0]