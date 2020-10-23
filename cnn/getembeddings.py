# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 12:54:02 2020

@author: lauri
"""
import pandas as pd
from gensim.models import Word2Vec
from copy import deepcopy

if __name__ == '__main__':
    train = pd.read_csv('../data/train.txt', sep=';', header=None, names=['text','label'])
    test = pd.read_csv('../data/test.txt', sep=';', header=None, names=['text','label'])
    sents = train.text.str.split()
    model = Word2Vec(sents, size=100, window=5, min_count=1, iter=1,
                     workers=4, compute_loss=True)
    NUM_ITER = 1000
    min_loss = model.get_latest_training_loss()
    for i in range(NUM_ITER):
        model.train(sentences=sents, total_examples=model.corpus_count, epochs=1, compute_loss=True)
        t_loss = model.get_latest_training_loss()
        if t_loss < min_loss:
            min_loss = t_loss
            best_model = deepcopy(model)
            print(f'loss {min_loss} on iteration {i}')
   
    best_model.wv.save('../data/own_vec.vec')
    
