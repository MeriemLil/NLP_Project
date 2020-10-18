import nltk
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet as wn, stopwords
import pandas as pd
from sklearn.model_selection import train_test_split

#tokenize the original data
file_content = open("./data/all_data.txt").read()
tokens = nltk.word_tokenize(file_content)

#suggest various filtering strategies
def preprocess(sentence):
    stop_words = set(stopwords.words("English"))
    #tokenization and stopwords removal
    words = word_tokenize(sentence)
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words]
    #stemming
    stemmed = []
    for w in filtered_words:
        stemmed.append(PorterStemmer().stem(w))
    #position tag
    tagged1 = nltk.pos_tag(words)
    tagged2 = nltk.pos_tag(filtered_words)
    return words, filtered_words, stemmed, tagged1, tagged2 #depending on the use select from the return list

#split the original data into 70% training and 30% testing
dataset = pd.read_csv('./data/all_data.txt', header=None, names=['text','label'], sep=';')

train_dataset = dataset.head(int(0.7*len(dataset)))
test_dataset = dataset.tail(len(dataset) - len(train_dataset))

train_dataset.to_csv('./data/splitTrain70.csv')
test_dataset.to_csv('./data/splitTest30.csv')


