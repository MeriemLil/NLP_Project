import pymysql
import pandas as pd

# Setup db connection. replace user and password with proper values.
db_connection = pymysql.connect(host='localhost',
                         user='root',
                         password='root')

# creating database_cursor to perform SQL operation
db_cursor = db_connection.cursor()

def create_database():
    # # executing cursor with execute method to create database if it is not exists
    db_cursor.execute("CREATE DATABASE IF NOT EXISTS nlp_project_db")

    # #select database
    db_cursor.execute("USE nlp_project_db")

    # #creating database table as emotion
    db_cursor.execute("CREATE TABLE IF NOT EXISTS emotion (id INT AUTO_INCREMENT PRIMARY KEY, entry VARCHAR(255), emotion_type VARCHAR(255))")



def get_data():
    db_cursor.execute("USE nlp_project_db")
    # Create a new query that selects the entire contents of `employee`
    sql = "SELECT entry, emotion_type FROM `emotion`"
    db_cursor.execute(sql)

    # Fetch all the records
    result = db_cursor.fetchall()
    return result


def is_database_exist():
    res = db_cursor.execute("SHOW DATABASES LIKE 'nlp_project_db'")
    if res:
        return True
    else:
        return False
