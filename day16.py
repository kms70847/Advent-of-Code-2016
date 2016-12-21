from math import ceil, log

def f(s):
    return s + "0" + "".join("0" if c == "1" else "1" for c in s)[::-1]

def checksum(s):
    while len(s)%2 == 0:
        result = []
        for i in range(0, len(s), 2):
            a,b = s[i:i+2]
            result.append("1" if a == b else "0")
        s = "".join(result)
    return s

initial_input = "11100010111110100"
for target_length in (272, 35651584):
    s = initial_input
    while len(s) < target_length:
        s = f(s)
    s = s[:target_length]
    print(checksum(s))