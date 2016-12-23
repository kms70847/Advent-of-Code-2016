import sys
import copy

VERBOSE = False

def execute(data, registers):
    #detects whether an addition optimization can be performed on the current line.
    #returns either false or a data structure detailing the operation.
    def addition_optimization(idx):
        if idx + 2 >= len(data):
            return False
        if not all(line["op"] in ("inc", "dec") for line in (data[idx], data[idx+1])):
            return False
        if data[idx+2]["op"] != "jnz":
            return False
        if data[idx+2]["args"][1] != "-2":
            return False

        sentinel = data[idx+2]["args"][0]
        #the sentinel and the target are both (in|dec)remented, but we don't yet know in what order.
        if data[idx]["args"][0] == sentinel:
            sentinel_idx = idx
            target_idx = idx+1
        elif data[idx+1]["args"][0] == sentinel:
            sentinel_idx = idx+1
            target_idx = idx
        else:
            #this isn't likely to happen in a program that halts,
            #but neither -crement command refers to the sentinel, 
            #so this isn't actually an addition subroutine.
            return False
        reg_and_sign = lambda x: (data[x]["args"][0], (1 if data[x]["op"] == "inc" else -1))
        sentinel_register, sentinel_sign = reg_and_sign(sentinel_idx)
        target_register, target_sign = reg_and_sign(target_idx)
        if sentinel_register == target_register: 
            return False
        return sentinel_register, sentinel_sign, target_register, target_sign

    #detects whether a multiplication optimization can be performed on the current line.
    def multiplication_optimization(idx):
        if idx + 4 >= len(data):
            return False
        add_opt = addition_optimization(idx)
        if not add_opt:
            return False
        if data[idx+3]["op"] not in ("inc", "dec"):
            return False
        if data[idx+4]["op"] != "jnz":
            return False
        if data[idx+4]["args"][1] != "-5":
            return False
        if data[idx+3]["args"][0] != data[idx+4]["args"][0]:
            return False
        mult_sentinel_register = data[idx+3]["args"][0]
        mult_sentinel_sign = 1 if data[idx+3]["op"] == "inc" else -1
        #not likely to happen in a well-formed program, but
        #it's only a multiplication if all three registers
        #are unique.
        if mult_sentinel_register in (add_opt[0], add_opt[2]):
            return False
        return add_opt + (mult_sentinel_register, mult_sentinel_sign)

    deref = lambda value: registers[value] if value in registers else int(value)
    pc = 0
    data = copy.deepcopy(data)
    while pc < len(data):
        if VERBOSE:print registers
        opt = multiplication_optimization(pc)
        if opt:
            sr, ss, tr, ts, mr, ms = opt
            if VERBOSE:print pc+1, "mult {} += {}{} * {}".format(tr, "" if ts==1 else "-", sr, mr)
            if ss*registers[sr] > 0 or ms*registers[mr] > 0:
                raise Exception("Infinite loop detected at multiplication subroutine {} with register values {} and optimization info {}".format(pc+1, registers, opt))
            registers[tr] += ts * abs(registers[sr]) * abs(registers[mr])
            registers[sr] = 0
            registers[mr] = 0
            pc += 5
            continue
        else:
            opt = addition_optimization(pc)
            if opt:
                sr, ss, tr, ts = opt
                if VERBOSE:print pc+1, "add {} += {}{}".format(tr, "" if ts == 1 else "-", sr)
                if ss*registers[sr] > 0:
                    raise Exception("Infinite loop detected at addition subroutine {}".format(pc+1))
                registers[tr] += ts * abs(registers[sr])
                registers[sr] = 0
                pc += 3
                continue
        op, args = data[pc]["op"], data[pc]["args"]
        if VERBOSE:print pc+1, " ".join(str(data[pc][k]) for k in ("op", "args"))
        if op == "cpy":
            value, destination = args
            value = deref(value)
            if destination.isalpha():
                registers[destination] = value
            else:
                pass #ignore attempts to copy onto nonregisters
        elif op == "inc":
            registers[args[0]] += 1
        elif op == "dec":
            registers[args[0]] -= 1
        elif op == "jnz":
            value, address = map(deref, args)
            if value:
                pc += int(address)
                continue
        elif op == "tgl":
            value = deref(args[0])
            address = pc+value
            if 0<=address<len(data):
                target_line = data[address]
                name = target_line["op"]
                if len(target_line["args"]) == 1:
                    data[address]["op"] = "dec" if name == "inc" else "inc"
                elif len(target_line["args"]) == 2:
                    data[address]["op"] = "cpy" if name == "jnz" else "jnz"
                else:
                    raise Exception("Unrecognized command {}".format(repr(data[address])))
        else:
            raise Exception("Unrecognized input {}".format(repr(line)))
        pc += 1
    return registers

with open("sample_input.txt" if "sample" in sys.argv else "input") as file:
    raw_data = file.read().strip().split("\n")
data = []
for row in raw_data:
    row = row.split()
    data.append({"op": row[0], "args": row[1:]})

registers = {k:0 for k in "abcd"}
registers["a"] = 7
print(execute(copy.deepcopy(data), registers)["a"])

registers = {k:0 for k in "abcd"}
registers["a"] = 12
print(execute(data, registers)["a"])
# #9438? Too low