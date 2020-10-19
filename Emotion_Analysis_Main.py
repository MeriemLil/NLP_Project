import pandas as pd
from patternMatch.categorySetup import * 
from patternMatch.constants import *
from patternMatch.stringMatching import *
from database.databaseConnection import engine
from patternMatch.empathClient import *

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

