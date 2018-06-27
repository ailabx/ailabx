import torch.nn as nn
import torch

hidden_size = 20
batch = 3
seq_len = 5
num_layers = 2
input_features = 10
lstm = nn.LSTM(input_features, hidden_size, num_layers,batch_first=True)

input = torch.randn(batch,seq_len,input_features)
output, hn = lstm(input)
print(output.size()) #(batch,seqLen,hidden)
