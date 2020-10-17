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

def save_to_database(data):
    # print(data)
    try:
        # create database and table if not exist
        create_database()
        # replace nan with none
        data.dropna(inplace=True)
        data[(data['entry']!='nan') & (data['emotion_type']!='nan')]
        df1 = data.where((pd.notnull(data)), None)
        cols = "`,`".join([str(i) for i in df1.columns.tolist()])
        # Insert DataFrame records one by one.
        for i,row in df1.iterrows():
            sql = "INSERT INTO `emotion` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
            db_cursor.execute(sql, tuple(row))
            # the connection is not autocommitted by default, so commit to save changes
            db_connection.commit()
    except:
        db_connection.close()
        print("Fail to save data")

# create data frame with entry and emotion_type
# save to database
def assign_category(category_list, harvard_inquirer):
    dataFrame = pd.DataFrame(columns=['entry','emotion_type'])
    for emotion_type, categories in category_list.items():
        dataFrame = dataFrame.append(get_category(emotion_type, harvard_inquirer, categories['include'], categories['exclude']))
    save_to_database(dataFrame)
    return True
