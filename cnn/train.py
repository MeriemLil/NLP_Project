"""
Adapted from https://github.com/baaesh/CNN-sentence-classification-pytorch/
"""

import argparse
import json
import copy
import os
import torch

from torch import nn, optim
from tensorboardX import SummaryWriter
from time import gmtime, strftime

from model import CNNSentence
from cnndata import DATA, getVectors
from test import test


def train(args, data, vectors):
	model = CNNSentence(args, data, vectors)
	model.to(torch.device(args.device))

	parameters = filter(lambda p: p.requires_grad, model.parameters())
	#adam optimizer seems to provide best convergence
	optimizer = optim.Adam(parameters, lr=args.learning_rate, weight_decay = args.regularization)
	criterion = nn.CrossEntropyLoss()

	writer = SummaryWriter(log_dir='runs/' + args.model_time)

	model.train()
	acc, loss, size, last_epoch = 0, 0, 0, -1
	min_test_loss = 100

	print_summary = False
	iterator = data.train_iter
	early_stop = 0
	print(args.early_stop)
	for i, batch in enumerate(iterator):
		present_epoch = int(iterator.epoch)
		if present_epoch == args.epoch or early_stop >= args.early_stop:
			break
		if present_epoch > last_epoch:
			print('epoch:', present_epoch + 1)
			print_summary = True
		last_epoch = present_epoch

		pred = model(batch)
		optimizer.zero_grad()
		batch_loss = criterion(pred, batch.label)
		loss += batch_loss.item()
		batch_loss.backward()
		nn.utils.clip_grad_norm_(parameters, max_norm=args.norm_limit)
		optimizer.step()


		_, pred = pred.max(dim=1)
		acc += (pred == batch.label).sum().float()
		size += len(pred)
		
		if print_summary:
			print_summary = False
			acc /= size
			acc = acc.cpu().item()

			test_loss, test_acc, _ = test(model, data, mode='dev')
			early_stop += 1
			c = present_epoch

			writer.add_scalar('loss/train', loss, c)
			writer.add_scalar('acc/train', acc, c)
			writer.add_scalar('loss/test', test_loss, c)
			writer.add_scalar('acc/test', test_acc, c)

			print(f'train loss: {loss:.3f} / test loss: {test_loss:.3f}'
				  f' / train acc: {acc:.3f} / test acc: {test_acc:.3f}')

			if test_loss < min_test_loss:
				min_test_loss = test_loss
				best_model = copy.deepcopy(model)
				early_stop = 0
			acc, loss, size = 0, 0, 0
			model.train()
	writer.close()

	return best_model


def main():
    
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch-size', default=50, type=int)
    parser.add_argument('--dropout', default=0.5, type=float)
    parser.add_argument('--epoch', default=300, type=int)
    parser.add_argument('--device', default='cpu')
    parser.add_argument('--learning-rate', default=0.001, type=float)
    parser.add_argument('--word-dim', default=300, type=int)
    parser.add_argument('--norm-limit', default=3.0, type=float)
    parser.add_argument("--mode", default="non-static",
                        help="available models: rand, static, non-static, multichannel")
    parser.add_argument('--num-feature-maps', default=100, type=int)
    parser.add_argument('--embeddings', default='word2vec',
                        help='available vector models: word2vec, fasttext, own')
    parser.add_argument('--early-stop', default=3, type=int)
    parser.add_argument('--regularization', default=0.0, type=float)
    
    args = parser.parse_args()
    data = DATA(args)
    vectors = getVectors(args, data)

    setattr(args, 'word_vocab_size', len(data.TEXT.vocab))
    setattr(args, 'class_size', len(data.LABEL.vocab))
    setattr(args, 'model_time', strftime('%H_%M_%S', gmtime()))
    setattr(args, 'FILTER_SIZES', [3, 4, 5])
    
    
    print('training start!')
    best_model = train(args, data, vectors)
    
    #save model trainable params
    if not os.path.exists('saved_models'):
    	os.makedirs('saved_models')
    torch.save(best_model.state_dict(), f'saved_models/CNN_sentence_{args.model_time}.pt')
    #save model arguments to json
    with open(f'saved_models/args{args.model_time}.txt', 'w') as f:
         json.dump(args.__dict__, f, indent=2)
    print('training finished!')


if __name__ == '__main__':
	main()