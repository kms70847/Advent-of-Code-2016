import hashlib
import itertools

def memoize(fn):
    answers = {}
    def fn_(*args):
        if args not in answers:
            answers[args] = fn(*args)
        return answers[args]
    return fn_

@memoize
def hash(index, depth=0):
    salt = "ihaygndm"
    x = hashlib.md5(salt + str(index)).hexdigest()
    for i in range(depth):
        x = hashlib.md5(x).hexdigest()
    return x

def produces_key(index, depth=0):
    a = hash(index, depth)
    for i in range(len(a)-2):
        if a[i] == a[i+1] == a[i+2]:
            triple = a[i]
            break
    else:
        return False
    for i in range(1, 1001):
        b = hash(index+i, depth)
        if triple*5 in b:
            return True

def get_nth(n, depth=0):
    found = 0
    for i in itertools.count():
        if produces_key(i, depth):
            found += 1
            if found == n:
                return i

print(get_nth(64, 0))
print(get_nth(64, 2016))
