from collections import defaultdict
l = ['a', 'b', 'f', 'f', 'b', 'b']
d = defaultdict(int)
for item in l:
    d[item] += 1

print d