import torch
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()
        self.hidden = torch.nn.Linear(n_feature, n_hidden)
        self.predict = torch.nn.Linear(n_hidden, n_output)

    def forward(self, x):
        x = F.relu(self.hidden(x))
        x = self.predict(x)
        return x

net1 = Net(1, 10, 1)

net2 = torch.nn.Sequential(
    torch.nn.Linear(1, 10),
    torch.nn.ReLU(),
    torch.nn.Linear(10, 1)
)


class Net3(nn.Module):
    def __init__(self,layers,seq):
        super(Net3,self).__init__()
        self.linear = layers
        self.seq = seq

    def forward(self, x):
        pass

net3 = Net3([nn.Linear(1,1),],nn.Sequential(nn.Linear(2,2)))
for p in net3.parameters():
    print(p)


