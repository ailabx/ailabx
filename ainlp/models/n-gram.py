import torch
import torch.nn as nn
import torch.nn.functional as F
from ainlp.basemodel import BaseModel
from ainlp.data.datahandler import NlpDataset
import torch.optim as optim

words = """When forty winters shall besiege thy brow,
    And dig deep trenches in thy beauty's field,
    Thy youth's proud livery so gazed on now,
    Will be a totter'd weed of small worth held:
    Then being asked, where all thy beauty lies,
    Where all the treasure of thy lusty days;
    To say, within thine own deep sunken eyes,
    Were an all-eating shame, and thriftless praise.
    How much more praise deserv'd thy beauty's use,
    If thou couldst answer 'This fair child of mine
    Shall sum my count, and make my old excuse,'
    Proving his beauty by succession thine!
    This were to be new made when thou art old,
    And see thy blood warm when thou feel'st it cold.""".split()

handler = NlpDataset()
handler.build_ngram(words)


class NGramLanguageModeler(BaseModel):
    def __init__(self, vocab_size, embedding_dim, context_size):
        super(NGramLanguageModeler, self).__init__()
        self.embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.linear1 = nn.Linear(context_size * embedding_dim, 128)
        self.linear2 = nn.Linear(128, vocab_size)

    def forward(self, inputs):
        embeds = self.embeddings(inputs).view((1, -1))
        out = F.relu(self.linear1(embeds))
        out = self.linear2(out)
        log_probs = F.log_softmax(out, dim=1)
        return log_probs

CONTEXT_SIZE = 2
EMBEDDING_DIM = 10

model = NGramLanguageModeler(len(handler.vocab),EMBEDDING_DIM,CONTEXT_SIZE)
model.compile(optimizer=optim.SGD,loss=nn.NLLLoss)
model.fit_dataloader(handler,num_epochs=1000,batch_size=1)
