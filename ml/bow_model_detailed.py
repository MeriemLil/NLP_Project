import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import PredefinedSplit
from sklearn.metrics import multilabel_confusion_matrix, precision_score
from sklearn.metrics import recall_score, log_loss, accuracy_score


def get_results(model):
    model_name = str(type(model).__name__)
    pred_dev = model.predict(X_dev.toarray())
    pred_dev_p = model.predict_proba(X_dev.toarray())
    pred_ts = model.predict(X_ts.toarray())
    pred_ts_p = model.predict_proba(X_ts.toarray())

    dev_acc = accuracy_score(pred_dev, dev.label)
    acc = accuracy_score(pred_ts, test.label)
    dev_loss = log_loss(dev.label, pred_dev_p)
    loss = log_loss(test.label, pred_ts_p)
    conf = multilabel_confusion_matrix(test.label, pred_ts, labels=labels)
    prec = precision_score(test.label, pred_ts, average='weighted')
    rec = recall_score(test.label, pred_ts, average='weighted')
    #restructure the confusion matrix to list
    conf = [[conf[i,:,:].tolist(),labels[i]] \
            for i in range(conf.shape[0])]
    res_dict = {'conf':conf,'acc':acc,'loss':loss, 'prec':prec,'rec':rec,
			'dev_loss':dev_loss, 'dev_acc':dev_acc, 'name': model_name}
    return res_dict



if __name__ == '__main__':
    # import data files
    train = pd.read_csv('../data/train.txt', header=None, names=['text','label'], sep=';')
    dev = pd.read_csv('../data/test.txt', header=None, names=['text','label'], sep=';')
    test = pd.read_csv('../data/val.txt', header=None, names=['text','label'], sep=';')
    
    # create a sklearn CV object to use for hyperparameter tuning
    traindev = pd.concat([train, dev]).reset_index(drop=True)
    split_index = [-1 if x in train.index else 0 for x in traindev.index]
    pdsplit = PredefinedSplit(test_fold = split_index)
    
    # grid of parameters to search from
    param_grid = {
     'min_samples_leaf': [1, 2, 3],
     'min_samples_split': [2, 4, 6, 10, 15, 20],
     'n_estimators': [500, 600, 800, 1000, 1400, 1700, 2000]}
    
    #initialize vectorizer and hyperparameter tuning
    tf_idf = TfidfVectorizer(stop_words='english')
    
    rf_random = RandomizedSearchCV(estimator = RandomForestClassifier(),
                                   param_distributions = param_grid,
                                   n_iter = 36, cv = pdsplit, verbose=True,
                                   random_state=42, n_jobs = 6,
                                   scoring='accuracy')    
    
    
    X_tr = tf_idf.fit_transform(train.text)
    X_trdev = tf_idf.transform(traindev.text)
    X_ts = tf_idf.transform(test.text)
    X_dev = tf_idf.transform(dev.text)
    
    print('Tuning hyperparameters for RandomForest')
    rf_random.fit(X_trdev, traindev.label)
    print(f'Best dev set score for RandomForest: {rf_random.best_score_}')
    #initialize and fit final models
    rf = RandomForestClassifier(**rf_random.best_params_)
    rf.fit(X_tr, train.label)
    
    gnb = MultinomialNB()
    logreg = LogisticRegression(max_iter=3000)
    gnb.fit(X_tr.toarray(), train.label)
    logreg.fit(X_tr, train.label)
    
    models = [gnb, logreg, rf]
    labels = ['joy','sadness','anger','fear','love','surprise']
    res = []
    i = 0
    for model in models:
        res.append(get_results(model)) 
    res = pd.DataFrame(res)

    res.to_json('results/detailed_res.json')