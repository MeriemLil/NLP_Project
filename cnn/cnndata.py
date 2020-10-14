"""
Adapted from https://github.com/baaesh/CNN-sentence-classification-pytorch/
"""

from torchtext import data
import numpy as np

from gensim.models import KeyedVectors, fasttext

def getVectors(args, data):
    """
    

    Parameters
    ----------
    args : argparse object of arguments fed to train
    data : object of class DATA.

    Returns
    -------
   numpy array of word vectors for each text in data

    """
    vectors = []

    if args.mode != 'rand':
        if args.embeddings != 'fasttext':
            embed = KeyedVectors.load_word2vec_format('../data/GoogleNews-vectors-negative300.bin', binary=True)
        else:
            embed = fasttext.load_facebook_vectors('../data/cc.en.300.bin', encoding='utf-8')
        for i in range(len(data.TEXT.vocab)):
            word = data.TEXT.vocab.itos[i]
            if word in embed.vocab:
                vectors.append(embed[word])
            else:
                vectors.append(np.random.uniform(-0.01, 0.01, args.word_dim))
    else:
        for i in range(len(data.TEXT.vocab)):
            vectors.append(np.random.uniform(-0.01, 0.01, args.word_dim))

    return np.array(vectors)

class TextDataset(data.TabularDataset):

    
    @staticmethod
    def sort_key(ex):
        return len(ex.text)
    
class DATA():
    """
    Class defining the dataset to be fed into the model.
    """
    def __init__(self, args):
        self.TEXT = data.Field(batch_first=True, lower=True, fix_length=70)
        self.LABEL = data.Field(sequential=False, unk_token=None)
        fields = [('text', self.TEXT), ('label', self.LABEL)]        
        
        self.train = TextDataset('../data/train.txt', 'CSV', fields,
                                             csv_reader_params={'delimiter':';'})
        self.dev = TextDataset('../data/test.txt', 'CSV', fields,
                                             csv_reader_params={'delimiter':';'})
        self.test = TextDataset('../data/val.txt', 'CSV', fields,
                                             csv_reader_params={'delimiter':';'})
            
        self.TEXT.build_vocab(self.train, self.dev, self.test)
        self.test_iter, self.dev_iter = \
            data.BucketIterator.splits((self.test, self.dev),
                								   batch_size=args.batch_size,
                								   device=args.device,
                                                   repeat=False)
        self.train_iter, _ = \
            data.BucketIterator.splits((self.test, self.dev),
                								   batch_size=args.batch_size,
                								   device=args.device,
                                                   repeat=True)
        self.LABEL.build_vocab(self.train)