def execute(data, registers):
    pc = 0
    while pc < len(data):
        line = data[pc]
        if line.startswith("cpy"):
            value, destination = line.split()[1:]
            if value.isdigit():
                value = int(value)
            else:
                value = registers[value]
            registers[destination] = value
        elif line.startswith("inc"):
            destination = line.split()[1]
            registers[destination] += 1
        elif line.startswith("dec"):
            destination = line.split()[1]
            registers[destination] -= 1
        elif line.startswith("jnz"):
            value, address = line.split()[1:]
            if value.isdigit():
                value = int(value)
            else:
                value = registers[value]
            if value:
                pc += int(address)
                continue
        elif line.startswith("glob"):   #custom instruction: add the second argument to the first, then zero out the second argument
            destination, value = line.split()[1:]
            registers[destination] += registers[value]
            registers[value] = 0
        elif line == "nop":     #custom instruction: do nothing
            pass
        else:
            raise Exception("Unrecognized input {}".format(repr(line)))
        pc += 1
    return registers

with open("input") as file:
    data = file.read().strip().split("\n")

#optimization: look for instruction sequences like
#inc a
#dec b
#jnz b -2
#... and replace them with
#glob a b
#nop
#nop
for i in range(len(data)):
    if data[i].startswith("inc") and data[i+1].startswith("dec") and data[i+2].startswith("jnz"):
        first = data[i].split()[1]
        second = data[i+1].split()[1]
        if first != second and data[i+2] == "jnz {} -2".format(second):
            data[i] = "glob {} {}".format(first, second)
            data[i+1] = "nop"
            data[i+2] = "nop"

registers = {k:0 for k in "abcd"}
print(execute(data, registers)["a"])

registers = {k:0 for k in "abcd"}
registers["c"] = 1
print(execute(data, registers)["a"])