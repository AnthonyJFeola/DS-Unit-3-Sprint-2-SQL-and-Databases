# SQLite3

import os
import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values
import json

DB_FILEPATH = os.path.join(os.path.dirname(__file__), "rpg_db.sqlite3")

connection = sqlite3.connect(DB_FILEPATH)
print("CONNECTION:", connection)

cursor = connection.cursor()
print("CURSOR", cursor)

query_list = []

table_names = ['armory_item', 'armory_weapon', 'charactercreator_character',
'charactercreator_character_inventory', 'charactercreator_cleric', 'charactercreator_fighter',
'charactercreator_mage', 'charactercreator_necromancer', 'charactercreator_thief']

for name in table_names:
    query = 'SELECT * FROM %s' % (name,)
    query_list.append(query)

for query in query_list:
    table = pd.DataFrame(cursor.execute(query).fetchall())
    table_tuples = list(table.itertuples(index=False, name=None))

#--------------------------------------------------------------------#

# PostgreSQL

load_dotenv()

DB_HOST = os.getenv("DB_HOST", default="OOPS")
DB_NAME = os.getenv("DB_NAME", default="OOPS")
DB_USER = os.getenv("DB_USER", default="OOPS")
DB_PASSWORD = os.getenv("DB_PASSWORD", default="OOPS")

connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
print("CONNECTION", type(connection))

cursor = connection.cursor()
print("CURSOR", type(cursor))


for name in table_names:
    if name == 'armory_item':
        query = 'CREATE TABLE IF NOT EXISTS %s (item_id SERIAL PRIMARY KEY, name varchar(40) NOT NULL, value JSONB, weight JSONB);' % (name,)
    elif name == 'armory_weapon':
        query = 'CREATE TABLE IF NOT EXISTS %s (item_ptr_id SERIAL PRIMARY KEY, power JSONB);' % (name,)
    elif name == 'charactercreator_character':
        query = 'CREATE TABLE IF NOT EXISTS %s (character_id SERIAL PRIMARY KEY, name varchar(40) NOT NULL, level JSONB, exp JSONB, hp JSONB, strength JSONB, intelligence JSONB, dexterity JSONB, wisdom JSONB);' % (name,)
    print("SQL:", query)
    cursor.execute(query)

connection.commit()
cursor.close()
connection.close()