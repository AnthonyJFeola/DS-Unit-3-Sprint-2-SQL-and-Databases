import os
import sqlite3

DB_FILEPATH = os.path.join(os.path.dirname(__file__), "buddymove_holidayiq.sqlite3")

connection = sqlite3.connect(DB_FILEPATH)
print("CONNECTION:", connection)

cursor = connection.cursor()
print("CURSOR", cursor)

query1 = """
SELECT
count(review."User Id") as rows
FROM review
"""

query2 = """
SELECT
count(DISTINCT"User Id")
FROM review
WHERE Nature >= 100 AND Shopping >= 100
"""

result1 = cursor.execute(query1).fetchall()
print("RESULT 1", result1)

result2 = cursor.execute(query2).fetchall()
print("RESULT 2", result2)