
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction import text 
from sklearn.preprocessing import StandardScaler

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('sqlite:///./data/project.db', echo=False)


import multiprocessing
from joblib import Parallel, delayed
import json
import os

def preprocess_df(df):
    """
    Pre-create different versions of text input
    with stop word and lemmatizations to pass on to tokenizer.
    
    Takes in a df and returns a df with added columns.

    """
    df['sk'] = df.text.str.split(' ').apply(\
            lambda x:' '.join([w for w in x if w not in text.ENGLISH_STOP_WORDS])) 
    df['nltk'] = df.text.str.split(' ').apply(\
            lambda x:' '.join([w for w in x if w not in stopwords.words('english')])) 
    # initialize wordnet lemmatizer and pre-create lemmatized words
    wnl = WordNetLemmatizer()
    df['text_lem'] = df.text.str.split(' ').apply(lambda x:\
                                ' '.join([wnl.lemmatize(w) for w in x]))
    df['sk_lem'] = df.sk.str.split(' ').apply(lambda x:\
                                ' '.join([wnl.lemmatize(w) for w in x]))
    df['nltk_lem'] = df.nltk.str.split(' ').apply(lambda x:\
                                ' '.join([wnl.lemmatize(w) for w in x]))
    return df

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
            col = stop_words
            if stop_words == 'none':
                col = 'text'
            #get lemmatized or non-lemmatized based on lemmatize boolean
            for lem in params['lemmatize']:
                if lem:
                    col += '_lem'
                X_tr = train[col]
                X_ts = dev[col]
                # max features to pass to the vectorizer item
                for max_features in params['max_features']:
                    #initialize vectorizer and fit
                    Vectorizer = vec(stop_words=None,
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
                    if (str(type(Vectorizer).__name__) == 'CountVectorizer') \
                    and (clf_name in ['LogisticRegression','SVC']):
                        X_train = scl.fit_transform(X_train)
                        X_test = scl.transform(X_test)
                    
                    # fit model and get accuracy score
                    clf.fit(X_train, train.label)
                    score = clf.score(X_test, dev.label)
                    
                    #create dictionary of parameters, classifier and accuracy
                    vals = [vec_p, stop_words, lem,
                            max_features, clf_name, score]
                    iters.append(dict(zip(list(params.keys())+['clf_name', 'score'],
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
    
    print('processing data ...')
    train = preprocess_df(train)
    dev = preprocess_df(dev)
    test = preprocess_df(test)
    
    # define the set of configurations to run
    params = {
        'vectorizer':[CountVectorizer, TfidfVectorizer],
        'stopwords':['none', 'sk', 'nltk'],
        'lemmatize':[True, False],
        'max_features':[None, 3000, 2000, 1000, 500, 100]
        }
    # compute number of configurations for each classifier 
    num_confs = 1
    for par in params.values():
        num_confs *= len(par)
        
    classifiers = [GaussianNB(), LogisticRegression(), SVC(), DecisionTreeClassifier(), 
                   RandomForestClassifier()]
    
   
 
    # run the iterations with models in parallel
    processed_list = Parallel(n_jobs=6)(delayed(run_bow_iterations)(params, train, dev, clf) 
                                                      for clf in classifiers)
    # flatten nested list structure
    processed_list = [obj for subobj in processed_list for obj in subobj]
    df = pd.DataFrame(processed_list)
    df.to_sql('bowModels', con=engine, index=False, if_exists='replace')