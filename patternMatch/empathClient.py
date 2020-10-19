from empath import Empath
import pandas as pd
from nltk.corpus import wordnet as wn

def process_lexicon(texts):
    lexicon = Empath()
    data = {}
    # apply lambda function to each text in texts to analyze text over all pre-built categories in empath client
    data = texts.apply(lambda x: [k for k, v in lexicon.analyze(x, normalize=False).items() if v > 0])
    data = data.apply(pd.Series).stack().reset_index(level=1, drop=True)
    return data



def empath_exact_category_accuracy(data, categories):
     # filter defined emotion type from categoty list (if any)
    emotion_type_pred = categories[categories.isin(data.emotion_type)]
    # group by index and get the last one (there can be more than one defined emotion types assign to one sentence)
    emotion_type_pred = emotion_type_pred.reset_index().groupby('index').last().iloc[:, 0]
    emotion_type_pred.name = 'emotion_type_pred'
    # join predicted type with data so that we can compare predicted emotion type with actual emotion type
    com = data.join(emotion_type_pred)
    # calculate accuracy with actual emotion type
    accuracy = ((com.emotion_type_pred == data.emotion_type).sum()/(len(com.emotion_type_pred == data.emotion_type))).round(5)
    return accuracy


def evaluate_labels(data, categories, how='min_depth'):
       
    # get emotion_type and empath unique category similarity
    similarity = get_category_similarities(data.emotion_type, categories, how)
   
    # convert categories into dataframe and merge with created similarity
    cat_labels = pd.merge(pd.DataFrame(categories, columns=['category']).reset_index(), similarity, on='category', how='inner')  

    com = cat_labels.groupby('index')['emotion_type'].agg(lambda x:x.value_counts().index[0])
    
    # combine predicted emotion_type to data
    com = data.join(com, rsuffix='_pred')
    
    # calculate accuracy
    accuracy = ((com.emotion_type_pred == data.emotion_type).sum()/(len(com.emotion_type_pred == data.emotion_type))).round(5)
    return accuracy




def get_category_similarities(emotion_type, categories, how='min_depth'):
    # get the unique emotion_types ['sadness' 'joy' 'fear' 'anger' 'love' 'surprise']
    emotion_type = emotion_type.unique()

    # get unique empath categories.
    empath_unique_categories = pd.Series(categories.unique(), name='category')

    # get synsets of empath categories
    empath_unique_category_synsets = empath_unique_categories.apply(lambda x: (wn.synsets(x)+[]))

    empath_unique_category_synsets = empath_unique_category_synsets[empath_unique_category_synsets.apply(lambda x: len(x) != 0)]

    # get synsets for defined emotion types
    emotion_type_synsets = pd.Series(emotion_type).apply(lambda x: (wn.synsets(x)))


    def path_sims(a, b):
        c = [[i.path_similarity(j) for i in a if i.path_similarity(j) is not None] for j in b]
        return max([it for sub in c for it in sub]+[0])
    def min_depth(a, b):
        c = [[i.lowest_common_hypernyms(j)[0].min_depth() for i in a \
              if len(i.lowest_common_hypernyms(j)) != 0] for j in b]
        return max([it for sub in c for it in sub]+[0])
    if how == 'min_depth':
        func = min_depth
    else:
        func = path_sims
    
    hypernyms = empath_unique_category_synsets.apply(lambda x: emotion_type_synsets.apply(\
                                   lambda y: func(x, y)))

    hypernyms = hypernyms[hypernyms.apply(lambda x: x == hypernyms.max(1)).sum(1) == 1]

    hypernyms.columns = emotion_type
    empath_unique_categories = pd.DataFrame(empath_unique_categories[hypernyms.index])
   
    # empath unique category map to emotion type using calculated hypernyms
    empath_unique_categories['emotion_type'] = hypernyms.idxmax(1)

    return empath_unique_categories



