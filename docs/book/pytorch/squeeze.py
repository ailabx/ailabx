import torch

def squeeze():
    a = torch.Tensor(1,3)
    print(a,a.size())

    b = a.squeeze(0)
    print(b.size())

    c =  a.squeeze(1)
    print(c.size())

d = torch.Tensor(2,2)
print(d.size(),'unsqueeze(1)=>',d.unsqueeze(1).size())