import itertools

#the assembly code is equivalent to:
# d = a+15*170
# while True:
    # a = d
    # while a != 0:
        # a,b = divmod(a,2)
        # out b

#so we're looking for `a` such that bin(a+15*70) is an alternating sequence of zeroes and ones, with the rightmost bit being a zero.
def alternates(a):
    x = 0
    while a != 0:
        if a % 2 != x:
            return False
        a /= 2
        x = 1-x
    return True

for i in itertools.count(1):
    if alternates(i+15*170):
        print i
        break
