strings = ('puppy', 'kitten', 'puppy', 'puppy',
           'weasel', 'puppy', 'kitten', 'puppy')

counts = {}

for kw in strings:
    if kw not in counts:
        counts[kw] = 1
    else:
        counts[kw] += 1

print(counts)

from collections import defaultdict
counts_default = defaultdict(lambda :0)
for kw in strings:
    counts_default[kw]+=1

print(counts_default)