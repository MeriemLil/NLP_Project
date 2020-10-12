import nltk
from nltk import word_tokenize
from nltk.corpus import wordnet as wn, stopwords
import pandas as pd
import re
from empath import Empath

#These are our five categories
anger = wn.synset("anger.n.01")
love = wn.synset("love.n.01")
sadness = wn.synset("sadness.n.01")
surprise = wn.synset("surprise.n.01")
joy = wn.synset("joy.n.01")
#joined in a list
categories = [anger, love, sadness, surprise, joy]

#Step 0
#First collect the emotion dataset
def load_dataset(file):
    lines = []
    with open(file) as f:
        for line in f.readlines():
            lines.append(line)
    return lines

#Now load the emotion dataset
train_data = load_dataset("C:/Users/ine_m/Desktop/Oulun Yliopisto/M1/NLP/NLP_Project/NLP_Project/emotion dataset/train.txt")
test_data = load_dataset("C:/Users/ine_m/Desktop/Oulun Yliopisto/M1/NLP/NLP_Project/NLP_Project/emotion dataset/test.txt")
val_data = load_dataset("C:/Users/ine_m/Desktop/Oulun Yliopisto/M1/NLP/NLP_Project/NLP_Project/emotion dataset/val.txt")

#Here we open the Harvard inquirer XL file
file = r'inquirerbasic.xls'
xl = pd.read_excel(file)

#Step 1
