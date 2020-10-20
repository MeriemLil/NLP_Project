import pandas as pd
from patternMatch.categorySetup import * 
from patternMatch.constants import *
from patternMatch.stringMatching import *
from database.databaseConnection import engine
from patternMatch.empathClient import *
from sqlalchemy import create_engine
engine = create_engine('sqlite:///./data/project.db', echo=False)


#Here we open the Harvard inquirer XL file
harvardInquirer = pd.read_excel('./data/inquirerbasic.xls')

# task1
if not engine.has_table('harvardWords'):
    is_database_created = assign_category(category_list, harvardInquirer)
    print('Database created successfully')
else:
    print("Database creation Done")


# task2
if engine.has_table('harvardWords'):
    result = engine.execute('SELECT * FROM harvardWords')
    string_match(result)
else:
    print('Database is not exist')

# task3
data = read_all_data()
categories = process_lexicon(data.text)
categories.to_sql('empathCategories', con=engine, index=True, if_exists='replace')

empath_accuracy = evaluate_labels(data, categories)
print('Accuracy of Empath: ', empath_accuracy)

# calculate accuracy of empath using exact categories
accuracy_exact_category = empath_exact_category_accuracy(data, categories)
print('Accuracy of Empath using exact categories: ', accuracy_exact_category)

# task 4
#drop redundant index columns with iloc
csv_one = pd.read_csv( "data/combined_cvs/combined_one.csv").iloc[:,2:]
csv_all = pd.read_csv( "data/combined_cvs/combined_all.csv").iloc[:,2:]

#migrate to sql database
csv_one.to_sql('semanticSimilarityOne', con=engine, if_exists='replace')
csv_all.to_sql('semanticSimilarityAll', con=engine, if_exists='replace')


#variables to count the matching of the original label and the predicted label of a sentence
count_one = 0
count_all = 0
# This count is needed in the calculation of accuracy
for i in range(len(csv_all)):
    if csv_one['Original Label'][i] == csv_one['Predicted Label'][i]:
        count_one += 1
    if csv_all['Original Label'][i] == csv_all['Predicted Label'][i]:
        count_all += 1

accuracy_combined_one = count_one/len(csv_one)
accuracy_combined_all = count_all/len(csv_all)
#
print("Accuracy of semantic similarity, 1 synset of a category approach: ", accuracy_combined_one)
print("Accuracy of semantic similarity, all synsets of a category approach: ", accuracy_combined_all)

# task 5
senti = pd.read_csv('data\sentistrength\sentistrength_results.csv')
#rename columns for data migration
senti.columns = ['Index', 'Text'] + senti.columns[2:].to_list()
#migrate to sql database
senti.to_sql('SentiStrengthScores', con=engine, index=False, if_exists='replace')