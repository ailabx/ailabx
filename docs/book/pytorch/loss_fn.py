import torch
import torch.nn as nn

#https://blog.csdn.net/zhangxb35/article/details/72464152?utm_source=itdadao&utm_medium=referral

def mseloss():
    loss_fn = nn.MSELoss()
    input = torch.Tensor([[1,1,1,1],[2,2,2,2]])
    target = torch.Tensor([[3,3,3,3],[4,4,4,4]])

    loss = loss_fn(input, target)
    print(input);
    print(target);
    print(loss.data.item())#其实是一个标量
    print(input.size(), target.size(), loss.size())

def cross_entropy():
    weight = torch.Tensor([1, 2, 1, 1, 10])

    loss_fn = torch.nn.CrossEntropyLoss(reduce=False, size_average=False, weight=weight)
    input = torch.randn(3, 5)  # (batch_size, C)
    target = torch.LongTensor(3).random_(5)

    print(input);
    print(target);

    loss = loss_fn(input, target)
    print(loss)

def nll():
    # input is of size N x C = 3 x 5
    input = torch.randn(3, 5, requires_grad=True)
    # each element in target has to have 0 <= value < C
    target = torch.tensor([1, 0, 4])
    output = torch.nn(torch.nn.LogSoftmax(input), target)
    output.backward()

nll()