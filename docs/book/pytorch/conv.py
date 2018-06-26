import torch
import torch.nn as nn

#Conv2d(in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, bias=True)
in_channels = 1
out_channels = 13
kernel_size = 3
N = 32
m = nn.Conv2d(in_channels, out_channels, 3, stride=2)

#Input: (N,Cin,Hin,Win)
input = torch.randn(N, in_channels, 50, 100)
#Output: (N,Cout,Hout,Wout)
output = m(input)
print(output.size())
#[N, out_channels, 24, 49]