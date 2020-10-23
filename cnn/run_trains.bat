python train.py
python train.py --regularization 0.0005 --dropout 0.75
python train.py --embeddings fasttext
python train.py --embeddings fasttext --regularization 0.0005 --dropout 0.75
python train.py --dropout 0.75 --num-feature-maps 150
python train.py --dropout 0.75 --num-feature-maps 150 --regularization 0.001
python train.py --dropout 0.75 --num-feature-maps 150 --regularization 0.001 --embeddings fasttext
python train.py --dropout 0.5 --mode multichannel --embeddings fasttext
python train.py --dropout 0.5 --mode static --embeddings fasttext
python train.py --dropout 0.7 --mode multichannel --num-feature-maps 150 --embeddings fasttext
python train.py --dropout 0.5 --mode static --num-feature-maps 150 --embeddings fasttext
python train.py --dropout 0.8 --mode multichannel --num-feature-maps 250 --embeddings fasttext
python train.py --dropout 0.8 --mode multichannel --num-feature-maps 250
python train.py --embeddings own
python train.py --embeddings own --regularization 0.0005 --dropout 0.75
python train.py --dropout 0.75 --num-feature-maps 150 --regularization 0.001 --embeddings own
python train.py --dropout 0.5 --mode multichannel --embeddings own
python train.py --dropout 0.5 --mode static --embeddings own
python train.py --dropout 0.5 --mode non-static --embeddings own
python train.py --dropout 0.7 --mode multichannel --num-feature-maps 150 --embeddings own
python train.py --dropout 0.5 --mode non-static --num-feature-maps 150 --embeddings own
python train.py --dropout 0.8 --mode multichannel --num-feature-maps 250 --embeddings own
python train.py --dropout 0.5 --mode multichannel --num-feature-maps 250 --embeddings own
pause