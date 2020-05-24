import os
import sqlite3
import pandas as pd

DB_FILEPATH = os.path.join(os.path.dirname(__file__), "buddymove_holidayiq.sqlite3")
BUDDY_FILEPATH = os.path.join(os.path.dirname(__file__), "buddymove_holidayiq.csv")

connection = sqlite3.connect(DB_FILEPATH)
print("CONNECTION:", connection)

cursor = connection.cursor()
print("CURSOR", cursor)

df = pd.read_csv(BUDDY_FILEPATH)
df.to_sql('review', con=connection)