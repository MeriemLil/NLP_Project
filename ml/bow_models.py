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


def run_bow_iterations(params, train, dev, clf, verbose=True):
    """
    Function to run different setups and compute accuracy for different model 
    setups sepcified in the project guidelines. Stores the parameters, 
    classifier name and accuracy for each iteration, for future use.


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
    # iteration number for verbose output
    iter_num = 0
    
    # list for iteration data
    iters = []
    # get name of the passed classifier to store
    clf_name = str(type(clf).__name__)
    
    # initialize scaling to be used with count-vectorize. with_mean=False reserves sparsity
    scl = StandardScaler(with_mean=False)
    
    ## iterate over the parameter grid defined by params dict
    for vec in params['vectorizer']:
        vec_p = str(type(vec()).__name__)
        #stopwords to pass to the vectorizer item
        for stop_words in params['stopwords']:
            #for nltk stopwords, a list of stopwords is passed
            if str(type(stop_words).__name__)=='list':
                stop_words_p = 'nltk'
            else:
                stop_words_p = stop_words
            #get lemmatized or non-lemmatized based on lemmatize boolean
            for lem in params['lemmatize']:
                if lem:
                    X_tr = train.lem_text
                    X_ts = dev.lem_text
                else:
                    X_tr = train.text
                    X_ts = dev.text
                
                # max features to pass to the vectorizer item
                for max_features in params['max_features']:
                    #initialize vectorizer and fit
                    Vectorizer = vec(stop_words=stop_words,
                                     max_features=max_features)
                    X_train = Vectorizer.fit_transform(X_tr)
                    X_test = Vectorizer.transform(X_ts)
                    
                    # naive-bayes classifier cannot handle sparse input
                    # matrix produced by vectorizers
                    if clf_name == "GaussianNB":
                        X_train = X_train.toarray()
                        X_test = X_test.toarray()
                    # some algorithms (e.g. logistic regression, SVC) converge
                    # better when input produced by CountVectorizer is scaled
                    if str(type(Vectorizer).__name__) == 'CountVectorizer':
                        X_train = scl.fit_transform(X_train)
                        X_test = scl.transform(X_test)
                    
                    # fit model and get accuracy score
                    clf.fit(X_train, train.label)
                    score = clf.score(X_test, dev.label)
                    
                    #create dictionary of parameters, classifier and accuracy
                    vals = [vec_p, stop_words_p, lem,
                            max_features, clf_name, score]
                    iters.append(dict(zip(list(params.keys())+['score'],
                                          vals)))
                    # print model result and progress
                    iter_num += 1
                    if verbose:
                        print(f'Accuracy {score:.3f} for iteration',
                              f'{iter_num} / {num_confs},', clf_name)
    return iters



num_cores = multiprocessing.cpu_count()

if __name__ == "__main__":

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
        
    classifiers = [GaussianNB(), LogisticRegression(), SVC(), DecisionTreeClassifier(), 
                   RandomForestClassifier(), GradientBoostingClassifier()]
    
    #initialize wordnet lemmatizer and pre-create lemmatized words
    wnl = WordNetLemmatizer()
    train['lem_text'] = train.text.str.split(' ').apply(lambda x: ' '.join([wnl.lemmatize(w) for w in x]))
    test['lem_text'] = test.text.str.split(' ').apply(lambda x: ' '.join([wnl.lemmatize(w) for w in x]))
    dev['lem_text'] = dev.text.str.split(' ').apply(lambda x: ' '.join([wnl.lemmatize(w) for w in x]))
 
    #run the iterations with models in parallel
    processed_list = Parallel(n_jobs=6)(delayed(run_bow_iterations)(params, train, dev, clf) 
                                                        for clf in classifiers)
    if not os.path.exists('results'):
        os.makedirs('results')
    with open('results/results.json', 'w') as f:
        json.dump(processed_list , f)