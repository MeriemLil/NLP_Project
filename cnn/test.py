"""
Adapted from https://github.com/baaesh/CNN-sentence-classification-pytorch/
"""


import argparse
import json

import torch
from torch import nn

from model import CNNSentence
from cnndata import DATA, getVectors


def test(model, data, mode='test'):
    """
    Runs testing for a given model and a given dataset
    Parameters
    ----------
    model : TYPE
        A trained torch classification model.
    data : object of class DATA
    mode : str
        Defines, whether to run the test on dev set or test set. The default is 'test'.

    Returns
    -------
    loss : loss for the dataset
    acc : accuracy of model

    """
    #create iterator from input dataset
    if mode == 'dev':
        iterator = iter(data.dev_iter)
    else:
        iterator = iter(data.test_iter)
    
    #define loss and prep model for evaluation
    criterion = nn.CrossEntropyLoss()
    model.eval()
    acc, loss, size = 0, 0, 0
    preds = torch.empty(0, 1)
    #run test for batch iterators
    for batch in iterator:
        pred = model(batch)
        #evaluate loss for batch
        batch_loss = criterion(pred, batch.label)
        loss += batch_loss.item()
        #predict and compare to labels to get sum of correct predictions
        _, pred = pred.max(dim=1)
        preds = torch.cat((preds, pred), 0)
        acc += (pred == batch.label).sum().float()
        size += len(pred)
    #divide by n to get accuracy
    acc /= size
    acc = acc.cpu().item()
    return loss, acc, preds


def load_args(args):
    """
    Helper function to load model args from file    
    """
    with open(f'saved_models/args{args.model_time}.txt', 'r') as f:
        arg_dict = json.load(f)
    args.__dict__.update(arg_dict)
    return args

def load_model(args, data):
    """
    Helper function to load model from file    
    """
    model_path = f'saved_models/CNN_sentence_{args.model_time}.pt'
    model = CNNSentence(args, data)
    model.load_state_dict(torch.load(model_path))

    return model


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-time', default='08-31-53', type=str)
    args = parser.parse_args()
    args = load_args(args)
    print('loading data...')
    data = DATA(args)
    setattr(args, 'word_vocab_size', len(data.TEXT.vocab))
    setattr(args, 'class_size', len(data.LABEL.vocab))
    print('loading vectors...')
    vectors = getVectors(args, data)
    print('loading model...')
    model = load_model(args, data, vectors)
    loss, acc, preds = test(model, data)
    print(preds)
    print(f'test acc: {acc:.3f}')    
    print(f'loss acc: {loss:.3f}')