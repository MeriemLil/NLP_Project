import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# import data files
train = pd.read_csv('./data/train.txt', header=None, names=['text','label'], sep=';')
test = pd.read_csv('./data/test.txt', header=None, names=['text','label'], sep=';')
val = pd.read_csv('./data/val.txt', header=None, names=['text','label'], sep=';')
