from collections import Counter
for x in (0, -1):
    print("".join(Counter(column).most_common()[x][0] for column in zip(*open("input").read().strip().split("\n"))))
    
#extra credit: one line, no imports
#for x in (0, -1): print("".join(sorted(set(column), key=column.count, reverse=True)[x] for column in zip(*open("input").read().strip().split("\n"))))