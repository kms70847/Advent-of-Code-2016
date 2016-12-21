def decompressed_length(line, max_passes):
    if max_passes == 0:
        return len(line)
    size = 0
    while line:
        if line.startswith("("):
            instruction, _, line = line.partition(")")
            length, repetitions = map(int, instruction.strip("()").split("x"))
            sub_line = line[:length]
            size += decompressed_length(sub_line, max_passes-1)*repetitions
            line = line[length:]
        else:
            size += 1
            line = line[1:]
    return size

with open("input") as file:
    data = file.read().strip()

print decompressed_length(data, 1)
print decompressed_length(data, float("inf"))