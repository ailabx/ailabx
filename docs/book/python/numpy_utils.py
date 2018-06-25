import numpy as np

a = np.array([[0,0.5,1.0,1.5,2.0],[2.5,3,3.5,4,4.5]])
print(type(a),a.shape)

print('数组求和:',a.sum(),'数组标准差:',a.std())

print('a=:',a)
print('a*2=:',a*2)
print('a**2=:',a**2)
print('a.sum(axis=0)按行相加:',a.sum(axis=0))
print('a.sum(axis=1)按列相加:',a.sum(axis=1))
