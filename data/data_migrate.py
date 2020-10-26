"""
Script to migrate machine learning model results
into the project database.

"""

import pandas as pd
import numpy as np
import glob
from sqlalchemy import create_engine


def flatten_conf(data):
    """
    Helper function to flatten the nested structure
    of the confusion matrices to separate columns.
    Needed to save.

    """
    data.reset_index(inplace=True)
    conf_df = pd.DataFrame(data.conf.to_list())
    conf_dfs = []
    for i in range(0, len(conf_df.columns), 2):
        t = pd.DataFrame(conf_df.iloc[:,i].to_list())
        lbl = conf_df.iloc[0,(i+1)]
        sub_dfs = []
        for j in range(2):
            sub_dfs.append(pd.DataFrame(t.iloc[:,j].to_list()))
        sub_dfs = pd.concat(sub_dfs, axis=1)
        sub_dfs.columns = [lbl+'_tn', lbl+'_fp',lbl+'_fn', lbl+'_tp']
        conf_dfs.append(sub_dfs)
    return data.join(pd.concat(conf_dfs, axis=1)).drop('conf', axis=1)

if __name__ == '__main__':
    engine = create_engine('sqlite:///project.db', echo=False)
    bow_detailed = pd.read_json('../ml/results/detailed_res.json')
    bow_detailed['conf'] = bow_detailed.conf.apply(lambda l: [item for sublist in l for item in sublist])
    
    cnns = glob.glob('../cnn/saved_models/test_res*')
    dfs = []
    args = []
    cols = ['conf', 'acc', 'loss', 'prec', 'rec', 'dev_loss', 'dev_acc', 'name',
           'batch_size', 'dropout', 'mode', 'num_feature_maps', 'embeddings',
           'regularization', 'word_dim']
    for cnn in cnns:
        arg = cnn.replace('test_res','args')
        t_df = pd.read_json(cnn)
        t_df['iter'] = cnn[-12:-4]
        t_df['conf'] = t_df.groupby('iter')['conf'].transform('sum')
        t_df = t_df.groupby('iter').first().reset_index(drop=True)
        arg = pd.read_json(arg).groupby('model_time').first().reset_index(drop=True)
        dfs.append(t_df.join(arg))
    
    df = pd.concat(dfs).reset_index(drop=True)

    
    df['name'] = np.select([df.embeddings=='fasttext', df.embeddings=='word2vec', df.embeddings =='ownfast'],
                           ['cnn_fasttext', 'cnn_word2vec', 'cnn_own_fasttext], default='cnn_own')

    #get best models by dev loss
    final_results = pd.concat([bow_detailed, df.loc[df.groupby('embeddings')['dev_acc'].idxmax(),:]])
    final_results = flatten_conf(final_results[cols]).iloc[:, 1:]
    finel_results_cnn = flatten_conf(df[cols]).iloc[:, 1:]
    final_results.to_sql('bestModels', con=engine, index=False, if_exists='replace')
    finel_results_cnn.to_sql('cnnModels', con=engine, index=False, if_exists='replace')
