import collections

d = collections.deque('abcdefg')
print('Deque:', d)
print('Length:', len(d))
print('Left end:', d[0])
print('Right end:', d[-1])

d.remove('c')
print('remove(c):', d)

d.append('h')
print('append h:',d)
d.appendleft('a0')
print('appendleft a0:',d)

d.pop()
print(d)
d.popleft()
print(d)