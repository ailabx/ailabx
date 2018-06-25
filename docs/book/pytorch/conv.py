import torch
import torch.nn.functional as F

filters = torch.randn(8,4,3,3)
inputs = torch.randn(1,4,5,5)
print(F.conv2d(inputs, filters, padding=1))