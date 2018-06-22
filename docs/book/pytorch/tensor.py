import numpy as np
import torch
from torch import nn

def test_tensor_type():
    x_train = np.array([[3.3], [4.4], [5.5], [6.71], [6.93], [4.168],
                        [9.779], [6.182], [7.59], [2.167], [7.042],
                        [10.791], [5.313], [7.997], [3.1]])

    x_train_ts = torch.Tensor(x_train)
    x_train_np = torch.from_numpy(x_train)
    print(x_train_ts,x_train_np)
    out = nn.Linear(1,1)(x_train_np)
    print(out)

if __name__ == '__main__':
    test_tensor_type()