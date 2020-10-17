import pandas as pd
from patternMatch.categorySetup import * 
from patternMatch.constants import *
from patternMatch.stringMatching import *
from database.databaseConnection import engine

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
