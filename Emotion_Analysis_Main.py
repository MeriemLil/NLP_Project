import nltk
from nltk import word_tokenize
from nltk.corpus import wordnet as wn, stopwords
import pandas as pd
import re
from empath import Empath

#These are our six categories
anger = wn.synset("anger.n.01")
love = wn.synset("love.n.01")
sadness = wn.synset("sadness.n.01")
surprise = wn.synset("surprise.n.01")
joy = wn.synset("joy.n.01")
fear = wn.synset("fear.n.01")
#joined in a list
categories = [anger, love, sadness, surprise, joy, fear]

# import data files
train = pd.read_csv('./data/train.txt', header=None, names=['text','label'], sep=';')
test = pd.read_csv('./data/test.txt', header=None, names=['text','label'], sep=';')
val = pd.read_csv('./data/val.txt', header=None, names=['text','label'], sep=';')

#Here we open the Harvard inquirer XL file
harvardInquirer = pd.read_excel('./data/inquirerbasic.xls')
