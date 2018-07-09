import numpy as np

def create():
    ar = np.array([1,2,3,4])
    print('size:',ar.size,'shape:',ar.shape,'ndim:',ar.ndim,'dtype:',ar.dtype)

    ar = np.array([[1, 2, 3, 4],[5,6,7,8]])
    print('size:', ar.size, 'shape:', ar.shape, 'ndim:', ar.ndim, 'dtype:', ar.dtype)

    array_ones = np.ones([3, 3])
    print(array_ones)

    array_zeros = np.zeros((2,2))
    print(array_zeros)

    print(np.random.rand(2, 2))
    print(np.random.uniform(0, 100))#创建指定范围内的一个数
    print(np.random.randint(0, 100))

    ar_normal = np.random.normal(1, 0.1, (2, 3))
    print('原数组：',ar_normal)
    print('\n')
    print('reshape之后的数组,',ar_normal.reshape((3,2)))

def calc():
    scores = np.array([[80, 88], [82, 81], [84, 75], [86, 83], [75, 81]])
    print('学生成绩表：',scores)
    print('分数是否大于80：',scores > 80)
    print('如果大于80，修改为100，否则置为0：',np.where(scores < 80, 0, 100))

def stats():
    scores = np.array([[99, 77], [67, 86], [85, 77], [83, 83], [79, 89]])
    print(scores)
    print('列最大值',np.max(scores,axis=1))
    print('行最大值',np.max(scores,axis=0))
    print('列最小值', np.min(scores, axis=1))
    print('行最小值', np.min(scores, axis=0))
    print('列平均值', np.mean(scores, axis=1))
    print('行平均值', np.mean(scores, axis=0))
    print('列方差', np.std(scores, axis=1))
    print('行方差', np.std(scores, axis=0))

def calc2():
    ones = np.ones((2,3))
    print(ones)
    ones_8 = ones + 8

    print('ones+ones_8:',ones+ones_8)

def calc_matrix():
    mat1 = np.ones((2,3))
    print(mat1)
    mat2 = np.ones((3,4))
    mat2.fill(0.3)
    print(mat2)
    print('mat1 dot mat2',mat1.dot(mat2))

    mat1 = [[0, 1, 2, 3, 4, 5],
          [6, 7, 8, 9, 10, 11]]
    print('mat1:',mat1)
    mat2 = [[12, 13, 14, 15, 16, 17],
          [18, 19, 20, 21, 22, 23]]
    print('mat2:', mat2)
    # 垂直拼接
    result = np.vstack((mat1, mat2))
    print("mat1,mat2 vstack:",result)
def test_basic():
    a = np.array([[0,0.5,1.0,1.5,2.0],[2.5,3,3.5,4,4.5]])
    print(type(a),a.shape)

    print('数组求和:',a.sum(),'数组标准差:',a.std())

    print('a=:',a)
    print('a*2=:',a*2)
    print('a**2=:',a**2)
    print('a.sum(axis=0)按行相加:',a.sum(axis=0))
    print('a.sum(axis=1)按列相加:',a.sum(axis=1))


def expr():
    import numpy as np
    import numexpr as ne
    a = np.arange(10)
    print('a is:',a)
    b = np.arange(0, 20, 2)
    print('b is:',b)
    c = ne.evaluate("2*a+3*b")
    print('c=2a+3b is:',c)
    #array([ 0,  8, 16, 24, 32, 40, 48, 56, 64, 72])

if __name__ == '__main__':
    calc_matrix()