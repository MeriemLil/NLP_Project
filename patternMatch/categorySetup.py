import pandas as pd
from database.databaseConnection import *

def get_category(label, harvard_inquirer, include_categories, exclude_categories = []):
    cond = True
    # loop through include_category list and check harvard inquirer has include value and not missing values
    for inc in include_categories:
        cond = cond&~harvard_inquirer[inc].isna()
    # loop through exclude_category list and check harvard inquirer has exclude value and missing values
    if len(exclude_categories) > 0:
        for exc in exclude_categories:
            cond = cond&harvard_inquirer[exc].isna()
    word = harvard_inquirer.loc[cond,'Entry'].str.lower()
    # some entry has # sign. remove that from the word
    word = pd.DataFrame(word.str.split('#').str[0])
    # set emotion_type to the data frame.
    word['emotion_type'] = label
    word.columns = word.columns.str.lower()
    # remove duplicates
    word.drop_duplicates(inplace=True)
    return word


# create data frame with entry and emotion_type
# save to database
def assign_category(category_list, harvard_inquirer):
    dataFrame = pd.DataFrame(columns=['entry','emotion_type'])
    for emotion_type, categories in category_list.items():
        dataFrame = dataFrame.append(get_category(emotion_type, harvard_inquirer, categories['include'], categories['exclude'])
    dataFrame.to_sql('harvardWords', con=engine, index=False, if_exists='replace')
    return True
