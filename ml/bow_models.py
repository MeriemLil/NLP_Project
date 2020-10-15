# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 16:49:46 2020

@author: lauri
"""

from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import multiprocessing
from joblib import Parallel, delayed
import json
import os

"""
TODO:
    Add different options e.g. scaling the input for the different classifiers
    based on their behaviour
    
    Comment the bow_iterations function
    

"""

def run_bow_iterations(params, train, dev, clf, verbose=True):
    """
    Function to run different setups and compute accuracy for different model 
    setups sepcified in the project guidelines.

    Parameters
    ----------
    params : dict
        dict of parameters as specified below in main
    train : pandas dataframe
        training dataset 
    dev : pandas dataframe
        test dataset
    clf : a scikit-learn classifier

    verbose : Bool,
        Determines whether to print model accuracy for the iterations.
        The default is True.

    Returns
    -------
    iters : list of dicts
        list of dictionaries that show the accuracy and specification
        of the model

    """
    i = 0
    iters = []
    clf_name = str(type(clf).__name__)
    scl = StandardScaler(with_mean=False)
    for vec in params['vectorizer']:
        vec_p = str(type(vec()).__name__)
        for stop_words in params['stopwords']:
            if str(type(i).__name__)=='list':
                stop_words_p = 'nltk'
            else:
                stop_words_p = stop_words
            for lem in params['lemmatize']:
                if lem:
                    X_tr = train.lem_text
                    X_ts = dev.lem_text
                else:
                    X_tr = train.text
                    X_ts = dev.text
                for max_features in params['max_features']:
                    Vectorizer = vec(stop_words=stop_words, max_features=max_features)
                    X_train = Vectorizer.fit_transform(X_tr)
                    X_test = Vectorizer.transform(X_ts)
                    if clf_name == "GaussianNB":
                        X_train = X_train.toarray()
                        X_test = X_test.toarray()
                    if str(type(Vectorizer).__name__) == 'CountVectorizer':
                        X_train = scl.fit_transform(X_train)
                        X_test = scl.transform(X_test)
                    clf.fit(X_train, train.label)
                    score = clf.score(X_test, dev.label)
                    vals = [vec_p, stop_words_p, lem, max_features, clf_name, score]
                    iters.append(dict(zip(list(params.keys())+['score'], vals)))
                    i += 1
                    if verbose:
                        print(f'Accuracy {score:.3f} for iteration {i} / {num_confs}, ' + clf_name)
    return iters



num_cores = multiprocessing.cpu_count()

if __name__ == "__main__":
    ## Currently ignoring warnings
    import warnings
    from sklearn.exceptions import DataConversionWarning
    warnings.filterwarnings(action='ignore', category=DataConversionWarning)

    # import data files
    train = pd.read_csv('../data/train.txt', header=None, names=['text','label'], sep=';')
    dev = pd.read_csv('../data/test.txt', header=None, names=['text','label'], sep=';')
    test = pd.read_csv('../data/val.txt', header=None, names=['text','label'], sep=';')
    
    
    # define the set of configurations to run
    params = {
        'vectorizer':[CountVectorizer, TfidfVectorizer],
        'stopwords':[None, 'english', stopwords.words('english')],
        'lemmatize':[True, False],
        'max_features':[None, 3000, 2000, 1000, 500, 100]
        }
    # compute number of configurations for each classifier 
    num_confs = 1
    for par in params.values():
        num_confs *= len(par)
        
    classifiers = [GaussianNB(), LogisticRegression(penalty='none'), SVC(), DecisionTreeClassifier(), 
                   RandomForestClassifier(), GradientBoostingClassifier()]
    #initialize wordnet lemmatizer
    wnl = WordNetLemmatizer()
    
    train['lem_text'] = train.text.str.split(' ').apply(lambda x: ' '.join([wnl.lemmatize(w) for w in x]))
    test['lem_text'] = test.text.str.split(' ').apply(lambda x: ' '.join([wnl.lemmatize(w) for w in x]))
    dev['lem_text'] = dev.text.str.split(' ').apply(lambda x: ' '.join([wnl.lemmatize(w) for w in x]))
 
    processed_list = Parallel(n_jobs=5)(delayed(run_bow_iterations)(params, train, dev, clf) 
                                                        for clf in classifiers)
    if not os.path.exists('results'):
        os.makedirs('results')
    with open('results/results.json', 'w') as f:
        json.dump(processed_list , f)