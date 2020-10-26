# -*- coding: utf-8 -*-
"""
Runs a word2vec model on the training data with vector size 100.
"""
import pandas as pd
from gensim.models import Word2Vec, FastText
from copy import deepcopy
from gensim.test.utils import datapath

if __name__ == '__main__':
    train = pd.read_csv('../data/train.txt', sep=';', header=None, names=['text','label'])
    test = pd.read_csv('../data/test.txt', sep=';', header=None, names=['text','label'])
    sents = train.text.str.split()
    
    """
    model = FastText(sents, size=50, window=5, min_count=1, iter=1,
                     workers=4)
    NUM_ITER = 1000
    max_acc = 0
    stop = 0
    for i in range(NUM_ITER):
        model.train(sentences=sents, total_examples=model.corpus_count, epochs=1)
        acc = model.wv.evaluate_word_analogies(datapath('questions-words.txt'))[0]
        if acc > max_acc:
            max_acc = acc
            best_model = deepcopy(model)
            print(f'accuracy {max_acc} on iteration {i}')
            stop = 0
        stop +=1
        if stop >= 10:
            break
   
    best_model.wv.save('../data/own_fast_50.vec')
    
    model = FastText(sents, size=100, window=5, min_count=1, iter=1,
                     workers=4)
    NUM_ITER = 1000
    max_acc = 0
    stop = 0
    for i in range(NUM_ITER):
        model.train(sentences=sents, total_examples=model.corpus_count, epochs=1)
        acc = model.wv.evaluate_word_analogies(datapath('questions-words.txt'))[0]
        if acc > max_acc:
            max_acc = acc
            best_model = deepcopy(model)
            print(f'accuracy {max_acc} on iteration {i}')
            stop = 0
        stop +=1
        if stop >= 10:
            break            
    best_model.wv.save('../data/own_fast_100.vec')
    
    model = FastText(sents, size=300, window=5, min_count=1, iter=1,
                     workers=4)
    NUM_ITER = 1000
    max_acc = 0
    stop = 0
    for i in range(NUM_ITER):
        model.train(sentences=sents, total_examples=model.corpus_count, epochs=1)
        acc = model.wv.evaluate_word_analogies(datapath('questions-words.txt'))[0]
        if acc > max_acc:
            max_acc = acc
            best_model = deepcopy(model)
            print(f'accuracy {max_acc} on iteration {i}')
            stop = 0
        stop +=1
        if stop >= 10:
            break
            
    best_model.wv.save('../data/own_fast_300.vec')
    
    """
    
    model = Word2Vec(sents, size=100, window=5, sg=1, min_count=1, iter=1,
                     workers=4)
                     
    NUM_ITER = 1000
    max_acc = 0
    stop = 0
    for i in range(NUM_ITER):
        model.train(sentences=sents, total_examples=model.corpus_count, epochs=1)
        acc = model.wv.evaluate_word_analogies(datapath('questions-words.txt'))[0]
        if acc > max_acc:
            max_acc = acc
            best_model = deepcopy(model)
            print(f'accuracy {max_acc} on iteration {i}')
            stop = 0
        stop +=1
        if stop >= 10:
            break
            
    best_model.wv.save('../data/own_vec_100.vec')
    
    model = Word2Vec(sents, size=300, window=5, sg=1, min_count=1, iter=1,
                     workers=4)
    NUM_ITER = 1000
    max_acc = 0
    stop = 0
    for i in range(NUM_ITER):
        model.train(sentences=sents, total_examples=model.corpus_count, epochs=1)
        acc = model.wv.evaluate_word_analogies(datapath('questions-words.txt'))[0]
        if acc > max_acc:
            max_acc = acc
            best_model = deepcopy(model)
            print(f'accuracy {max_acc} on iteration {i}')
            stop = 0
        stop +=1
        if stop >= 10:
            break
            
    best_model.wv.save('../data/own_vec_300.vec')
    
    model = Word2Vec(sents, size=50, window=5, sg=1, min_count=1, iter=1,
                     workers=4)
    NUM_ITER = 1000
    max_acc = 0
    stop = 0
    for i in range(NUM_ITER):
        model.train(sentences=sents, total_examples=model.corpus_count, epochs=1)
        acc = model.wv.evaluate_word_analogies(datapath('questions-words.txt'))[0]
        if acc > max_acc:
            max_acc = acc
            best_model = deepcopy(model)
            print(f'accuracy {max_acc} on iteration {i}')
            stop = 0
        stop +=1
        if stop >= 10:
            break            
    best_model.wv.save('../data/own_vec_50.vec')
    
    
