import nltk
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet as wn, stopwords
import pandas as pd

#function that performs different preprocessing steps on a given sentence
def preprocess(sentence):
    stop_words = set(stopwords.words("English"))
    #tokenization and stopwords removal
    words = word_tokenize(sentence)
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words]
    #stemming
    stemmed = []
    for w in filtered_words:
        stemmed.append(PorterStemmer().stem(w))
    #position tag
    tagged1 = nltk.pos_tag(words)
    tagged2 = nltk.pos_tag(filtered_words)
    return words, filtered_words, stemmed, tagged1, tagged2 #depending on the use select from the return list

#function that calculates similarity : sim(sentence, category) = average(wup similarity between each noun in a sentence and a category)
def semantic_similarity(sentence, category):
    sum = 0
    count = 0
    #words = preprocess(sentence)[3] #position tagged
    words = preprocess(sentence)[4] #position tagged and filtered
    for word in words:
        if word[1] == 'NN' or word[1] == 'NNP' or word[1] == 'NNS' or word[1] == 'NNPS':
            if wn.synsets(word[0]): #there exists at least one synset
                if category.wup_similarity(wn.synsets(word[0])[0]): #similarity is not none
                    sum += category.wup_similarity(wn.synsets(word[0])[0])
                    count += 1
    if count != 0:
        return sum/count
    else:
        #print("Error! division by 0 becuase there are no nouns in the sentence")
        sim = 0
        return sim

#function that calculates the similarity between every category (as one synset) and every sentence (each noun as one synset) in input file, and creates output result file
def find_sims_all(file, df_file, result):
    # These are our six categories
    anger = wn.synsets("anger")
    love = wn.synsets("love")
    sadness = wn.synsets("sadness")
    surprise = wn.synsets("surprise")
    joy = wn.synsets("joy")
    fear = wn.synsets("fear")

    l1 = len(anger)  # 5
    l2 = len(love)  # 10
    l3 = len(sadness)  # 3
    l4 = len(surprise)  # 6
    l5 = len(joy)  # 4
    l6 = len(fear)  # 8

    for i in range(len(file)):
        mean_anger = (semantic_similarity((file.iloc[i])[0], anger[0]) + semantic_similarity((file.iloc[i])[0], anger[1]) + semantic_similarity((file.iloc[i])[0], anger[2]) + semantic_similarity((file.iloc[i])[0], anger[3]) + semantic_similarity((file.iloc[i])[0], anger[4])) / l1
        mean_love = (semantic_similarity((file.iloc[i])[0], love[0]) + semantic_similarity((file.iloc[i])[0], love[1]) + semantic_similarity((file.iloc[i])[0], love[2]) + semantic_similarity((file.iloc[i])[0],love[3]) + semantic_similarity((file.iloc[i])[0], love[4]) + semantic_similarity((file.iloc[i])[0], love[5]) + semantic_similarity((file.iloc[i])[0], love[6]) + semantic_similarity((file.iloc[i])[0], love[7]) + semantic_similarity((file.iloc[i])[0], love[8]) + semantic_similarity((file.iloc[i])[0], love[9])) / l2
        mean_sadness = (semantic_similarity((file.iloc[i])[0], sadness[0]) + semantic_similarity((file.iloc[i])[0],sadness[1]) + semantic_similarity((file.iloc[i])[0], sadness[2])) / l3
        mean_surprise = (semantic_similarity((file.iloc[i])[0], surprise[0]) + semantic_similarity((file.iloc[i])[0],surprise[1]) + semantic_similarity((file.iloc[i])[0], surprise[2]) + semantic_similarity((file.iloc[i])[0], surprise[3]) + semantic_similarity((file.iloc[i])[0], surprise[4]) + semantic_similarity((file.iloc[i])[0], surprise[5])) / l4
        mean_joy = (semantic_similarity((file.iloc[i])[0], joy[0]) + semantic_similarity((file.iloc[i])[0],joy[1]) + semantic_similarity((file.iloc[i])[0], joy[2]) + semantic_similarity((file.iloc[i])[0], joy[3])) / l5
        mean_fear = (semantic_similarity((file.iloc[i])[0], fear[0]) + semantic_similarity((file.iloc[i])[0], fear[1]) + semantic_similarity((file.iloc[i])[0], fear[2]) + semantic_similarity((file.iloc[i])[0],fear[3]) + semantic_similarity((file.iloc[i])[0], fear[4]) + semantic_similarity((file.iloc[i])[0], fear[5]) + semantic_similarity((file.iloc[i])[0], fear[6]) + semantic_similarity((file.iloc[i])[0], fear[7])) / l6

        df_file.loc[i, ['Original Label']] = (file.iloc[i])[1]
        df_file.loc[i, ['ANGER']] = round(mean_anger, 3)
        df_file.loc[i, ['LOVE']] = round(mean_love, 3)
        df_file.loc[i, ['SADNESS']] = round(mean_sadness, 3)
        df_file.loc[i, ['SURPRISE']] = round(mean_surprise, 3)
        df_file.loc[i, ['JOY']] = round(mean_joy, 3)
        df_file.loc[i, ['FEAR']] = round(mean_fear, 3)

        max_sim = max(round(mean_anger, 3),
                      round(mean_love, 3),
                      round(mean_sadness, 3),
                      round(mean_surprise, 3),
                      round(mean_joy, 3),
                      round(mean_fear, 3))

        if max_sim == round(mean_anger, 3) and max_sim != 0:
            cat = "anger"
        elif max_sim == round(mean_love, 3) and max_sim != 0:
            cat = "love"
        elif max_sim == round(mean_sadness, 3) and max_sim != 0:
            cat = "sadness"
        elif max_sim == round(mean_surprise, 3) and max_sim != 0:
            cat = "surprise"
        elif max_sim == round(mean_joy, 3) and max_sim != 0:
            cat = "joy"
        elif max_sim == round(mean_fear, 3) and max_sim != 0:
            cat = "fear"
        elif max_sim == 0:
            cat = "not found"
        df_file.loc[i, ['Predicted Label']] = cat

    df_file.to_csv(result, sep=',')

#function that calculates the similarity between every category (taking the average of all its synsets) and every sentence (each noun as one synset) in input file, and creates output result file
def find_sims_one(file, df_file, result):
    # These are our six categories
    anger = wn.synsets("anger")[0]
    love = wn.synsets("love")[0]
    sadness = wn.synsets("sadness")[0]
    surprise = wn.synsets("surprise")[0]
    joy = wn.synsets("joy")[0]
    fear = wn.synsets("fear")[0]
    for i in range(len(file)):
        an = round(semantic_similarity((file.iloc[i])[0], anger), 3)
        lo = round(semantic_similarity((file.iloc[i])[0], love), 3)
        sa = round(semantic_similarity((file.iloc[i])[0], sadness), 3)
        su = round(semantic_similarity((file.iloc[i])[0], surprise), 3)
        jo = round(semantic_similarity((file.iloc[i])[0], joy), 3)
        fe = round(semantic_similarity((file.iloc[i])[0], fear), 3)

        df_file.loc[i, ['Original Label']] = (file.iloc[i])[1]
        df_file.loc[i, ['ANGER']] = an
        df_file.loc[i, ['LOVE']] = lo
        df_file.loc[i, ['SADNESS']] = sa
        df_file.loc[i, ['SURPRISE']] = su
        df_file.loc[i, ['JOY']] = jo
        df_file.loc[i, ['FEAR']] = fe

        max_sim = max(an, lo, sa, su, jo, fe)

        if max_sim == an and max_sim != 0:
            cat = "anger"
        elif max_sim == lo and max_sim != 0:
            cat = "love"
        elif max_sim == sa and max_sim != 0:
            cat = "sadness"
        elif max_sim == su and max_sim != 0:
            cat = "surprise"
        elif max_sim == jo and max_sim != 0:
            cat = "joy"
        elif max_sim == fe and max_sim != 0:
            cat = "fear"
        elif max_sim == 0:
            cat = "not found"
        df_file.loc[i, ['Predicted Label']] = cat

    df_file.to_csv(result, sep=',')

#input data files
train = pd.read_csv('./data/train.txt', header=None, names=['text','label'], sep=';')
test = pd.read_csv('./data/test.txt', header=None, names=['text','label'], sep=';')
val = pd.read_csv('./data/val.txt', header=None, names=['text','label'], sep=';')

#output dataframes
df_train = pd.DataFrame(columns=['Original Label','ANGER', 'LOVE', 'SADNESS', 'SURPRISE', 'JOY', 'FEAR', 'Predicted Label'])
df_test = pd.DataFrame(columns=['Original Label','ANGER', 'LOVE', 'SADNESS', 'SURPRISE', 'JOY', 'FEAR', 'Predicted Label'])
df_val = pd.DataFrame(columns=['Original Label','ANGER', 'LOVE', 'SADNESS', 'SURPRISE', 'JOY', 'FEAR', 'Predicted Label'])

# #here we generate output files that contain semantic similarity between each sentence in the input file with each of our six categories, First: one synset of a category approach
# find_sims_one(train, df_train, "train_one.csv")
# find_sims_one(test, df_test, "test_one.csv")
# find_sims_one(val, df_val, "val_one.csv")
#
# #here we generate output files that contain semantic similarity between each sentence in the input file with each of our six categories, Second: average of all synsets of a category approach
# find_sims_all(train, df_train, "train_all.csv")
# find_sims_all(test, df_test, "test_all.csv")
# find_sims_all(val, df_val, "val_all.csv")

#here we read our generated output files
trained_one = pd.read_csv('./one_synset_generated_output_file/train_one.csv')
tested_one = pd.read_csv('./one_synset_generated_output_file/test_one.csv')
validated_one = pd.read_csv('./one_synset_generated_output_file/val_one.csv')

trained_all = pd.read_csv('./all_synset_generated_output_file/train_all.csv')
tested_all = pd.read_csv('./all_synset_generated_output_file/test_all.csv')
validated_all = pd.read_csv('./all_synset_generated_output_file/val_all.csv')


#here we join our output data files in one file
combined_csv_one = pd.concat([trained_one, tested_one, validated_one])
combined_csv_all = pd.concat([trained_all, tested_all, validated_all])
#export to csv
combined_csv_one.to_csv( "combined_one.csv", sep= ',')
combined_csv_all.to_csv( "combined_all.csv", sep= ',')

