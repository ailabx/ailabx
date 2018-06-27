import torch
import torch.nn as nn

# Embedding层 containing 长度为10，size3
embedding = nn.Embedding(10, 3)
# 2行4列
input = torch.LongTensor([[1,2,4,5],[4,3,2,9]])
out = embedding(input)
print(out.size()) #[2,4,3]


import torch
import torch.nn as nn
word_to_ix = {'hello': 0, 'world': 1}

embeds = nn.Embedding(len(word_to_ix), 5)
hello_idx = torch.LongTensor([word_to_ix['hello'],word_to_ix['world']])
print(hello_idx.size())
hello_embed = embeds(hello_idx)
print(hello_embed,hello_embed.size())