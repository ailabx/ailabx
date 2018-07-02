import numpy as np

def test_basic():
    a = np.array([[0,0.5,1.0,1.5,2.0],[2.5,3,3.5,4,4.5]])
    print(type(a),a.shape)

    print('数组求和:',a.sum(),'数组标准差:',a.std())

    print('a=:',a)
    print('a*2=:',a*2)
    print('a**2=:',a**2)
    print('a.sum(axis=0)按行相加:',a.sum(axis=0))
    print('a.sum(axis=1)按列相加:',a.sum(axis=1))


import numpy as np
import numexpr as ne
a = np.arange(10)
print('a is:',a)
b = np.arange(0, 20, 2)
print('b is:',b)
c = ne.evaluate("2*a+3*b")
print('c=2a+3b is:',c)
#array([ 0,  8, 16, 24, 32, 40, 48, 56, 64, 72])