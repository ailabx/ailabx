import torch
from torch.utils.data import Dataset

class NlpDataset(Dataset):
    def __init__(self):
        pass

    def __len__(self):
        return len(self.datas)

    def __getitem__(self, idx):
        return self.datas[idx]


    def build_vocab_idxs(self,words):
        self.vocab = set(words)
        self.word_to_ix = {word: i for i, word in enumerate(self.vocab)}

    def build_cbow(self,words):
        self.build_vocab_idxs(words)
        self.datas = []

        for i in range(2, len(words) - 2):
            context = [
                words[i - 2], words[i - 1], words[i + 1], words[i + 2]
            ]
            context_idxs = torch.tensor([self.word_to_ix[w] for w in context], dtype=torch.long)
            print(context_idxs.size())
            target = words[i]
            target_idx = torch.tensor([self.word_to_ix[target]], dtype=torch.long)

            self.datas.append((context_idxs, target_idx))
        print(len(self.datas), self.datas)


    def build_ngram(self,words):
        self.build_vocab_idxs(words)

        self.datas = []
        for i in range(len(words) - 2):
            context = [words[i], words[i + 1]]
            context_idxs = torch.tensor([self.word_to_ix[w] for w in context], dtype=torch.long)
            print(context_idxs.size())
            target = words[i]
            target_idx = torch.tensor([self.word_to_ix[target]], dtype=torch.long)

            self.datas.append((context_idxs,target_idx))
        print(len(self.datas),self.datas)

if __name__ == '__main__':
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
    handler.build_cbow(words)




