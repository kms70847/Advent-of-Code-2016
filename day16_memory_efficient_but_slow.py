from math import ceil, log
import itertools

def dragon(s, idx):
    assert idx >= 0
    #print "dragon({}->{}, {})".format(repr(s), len(s),idx)
    #a dragon string has length (2**k)*(N+1)-1, where N is the length of the input string, and k is the number of iterations made.
    n = len(s)
    assert isinstance(idx, int), "expected int, got {} {}".format(type(idx), repr(idx))
    if idx < n: return s[idx]
    if idx == n: return "0"
    #find the smallest value of k that contains idx
    k = int(ceil(log((idx+2.)/(n+1.)) / log(2)))
    assert k > 0, "miscalculated k for inputs {} {}".format(s, idx)

    #determine length of k-1th iteration
    half_length = (2**(k-1))*(n+1)-1
    assert isinstance(half_length, int), "expected int, got {} {}".format(type(half_length), repr(half_length))
    #find the position of idx's reverse/flipped counterpart, it it exists
    if idx == half_length: 
        return "0"
    else:
        new_idx = 2*half_length - idx
        return {"0":"1", "1":"0"}[dragon(s, new_idx)]

def checksum(s):
    while len(s)%2 == 0:
        result = []
        for i in range(0, len(s), 2):
            a,b = s[i:i+2]
            result.append("1" if a == b else "0")
        s = "".join(result)
    return s

def gen_checksum(iterable):
    while True:
        if next(iterable) == next(iterable):
            yield "1"
        else:
            yield "0"

def required_checksum_generations(size):
    ret = 0
    while size % 2 == 0:
        ret += 1
        size /= 2
    return ret, size

def loud(iterable):
    def round(x):
        if x < 10: return True
        return x%10 == 0 and round(x/10)
    for x in iterable:
        if round(x):
            print(x)
        yield x

initial_input = "11100010111110100"
for target_length in (272, 35651584):
    checksum_generations, final_checksum_length = required_checksum_generations(target_length)
    iterable = (dragon(initial_input, i) for i in loud(itertools.count()))
    for _ in range(checksum_generations):
        iterable = gen_checksum(iterable)
    print "".join(itertools.islice(iterable, final_checksum_length))