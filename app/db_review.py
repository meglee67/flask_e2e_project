# this code is copied and modified from https://github.com/hantswilliams/HHA_504_2023/blob/main/WK7/google_flask_app/db_review.py

import sqlite3
import pandas as pd

# Initialize the database
DATABASE = 'oauth/users.db'

# search for user in database
db = sqlite3.connect(DATABASE)
cursor = db.cursor()

# get list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

# get values from users table
df = pd.read_sql_query("SELECT * FROM users", db)
df