import numpy as np
import torch
import torch.nn as nn

def test_tensor_type():
    x_train = np.array([[3.3], [4.4], [5.5], [6.71], [6.93], [4.168],
                        [9.779], [6.182], [7.59], [2.167], [7.042],
                        [10.791], [5.313], [7.997], [3.1]])

    x_train_ts = torch.Tensor(x_train)
    x_train_np = torch.from_numpy(x_train)
    print(x_train_ts,x_train_np)
    out = nn.Linear(1,1)(x_train_np)
    print(out)

#https://www.cnblogs.com/hellcat/p/8496850.html
def test_functional():
    input = torch.rand(2,3)
    o1 = torch.nn.ReLU()(input)
    o2 = torch.nn.functional.relu(input)
    print(o1==o2)


if __name__ == '__main__':
    test_functional()