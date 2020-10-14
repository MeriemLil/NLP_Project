"""
Adapted from https://github.com/baaesh/CNN-sentence-classification-pytorch/
"""


import argparse

import torch
from torch import nn

from model import CNNSentence
from cnndata import DATA


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
    
    #run test for batch iterators
    for batch in iterator:
        pred = model(batch)
        #evaluate loss for batch
        batch_loss = criterion(pred, batch.label)
        loss += batch_loss.item()
        #predict and compare to labels to get sum of correct predictions
        _, pred = pred.max(dim=1)
        acc += (pred == batch.label).sum().float()
        size += len(pred)
    #divide by n to get accuracy
    acc /= size
    acc = acc.cpu().item()
    return loss, acc


def load_model(args, data):
    """
    
    
    """
    model = CNNSentence(args, data)
    model.load_state_dict(torch.load(args.model_path))

    if args.device == 'gpu':
        model.cuda(args.gpu)

    return model


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch-size', default=64, type=int)
    parser.add_argument('--dropout', default=0.5, type=float)
    parser.add_argument('--device', default='cpu')
    parser.add_argument('--word-dim', default=300, type=int)
    parser.add_argument("--mode", default="non-static", help="available models: rand, static, non-static, multichannel")
    parser.add_argument('--num-feature-maps', default=5, type=int)

    args = parser.parse_args()

    print('loading SNLI data...')
    data = DATA(args)

    setattr(args, 'word_vocab_size', len(data.TEXT.vocab))
    setattr(args, 'class_size', len(data.LABEL.vocab))

    # if block size is lower than 0, a heuristic for block size is applied.
    if args.block_size < 0:
        args.block_size = data.block_size

    print('loading model...')
    model = load_model(args, data)

    _, acc = test(model, data)

    print(f'test acc: {acc:.3f}')