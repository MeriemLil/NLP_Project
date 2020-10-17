import pandas as pd
import shutil
import os

#concat all data and create all_data.txt file
def generate_full_data_file():
    with open('./data/all_data.txt','wb') as wfd:
        for f in ["./data/test.txt", "./data/train.txt", "./data/val.txt"]:
            with open(f,'rb') as fd:
                shutil.copyfileobj(fd, wfd)



def evaluate_matches(data, targets):
    # convert categories to indicator varibles
    match_target = pd.get_dummies(targets, columns=['emotion_type'], prefix='', prefix_sep='')
    
    # group the words
    match_target = match_target.groupby('entry').sum().reset_index()    

    matches = match_target.apply(lambda x: data.text.str.contains(x.entry).astype(int), 1)

    matches = match_target.iloc[:,1:].apply(lambda x: matches.mul(x, axis=0).sum(), 0)

    return matches.idxmax(axis=1)




def string_match(result):
    # put database data into dataFrame
    df = pd.DataFrame(data=result, columns=['entry','emotion_type'])
    
    # check all_data file generated. Otherwise create all_data file
    if not os.path.exists('./data/all_data.txt'):
        generate_full_data_file()

    # read and format data
    data = pd.read_csv('./data/all_data.txt', header=None, names=['text','emotion_type'], sep=';')
    matches = evaluate_matches(data, df)
    accuracy = (matches == data.emotion_type).mean().round(5)
    print('Accuracy of string matching: ', accuracy)
