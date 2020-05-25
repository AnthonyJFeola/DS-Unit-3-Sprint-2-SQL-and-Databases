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

table_names = ['armory_item', 'armory_weapon', 'charactercreator_character',
'charactercreator_character_inventory', 'charactercreator_cleric', 'charactercreator_fighter',
'charactercreator_mage', 'charactercreator_necromancer', 'charactercreator_thief']

query_list = []

tuple_list = []

for name in table_names:
    query = 'SELECT * FROM %s' % (name,)
    query_list.append(query)

for query in query_list:
    table = pd.DataFrame(cursor.execute(query).fetchall())
    table_tuples = list(table.itertuples(index=False, name=None))
    tuple_list.append(table_tuples)

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
        query = 'CREATE TABLE IF NOT EXISTS %s (item_id SERIAL PRIMARY KEY, name varchar(40) NOT NULL, value int, weight int);' % (name,)

    elif name == 'armory_weapon':
        query = 'CREATE TABLE IF NOT EXISTS %s (item_ptr_id SERIAL PRIMARY KEY, power int);' % (name,)

    elif name == 'charactercreator_character':
        query = 'CREATE TABLE IF NOT EXISTS %s (character_id SERIAL PRIMARY KEY, name varchar(40) NOT NULL, level int, exp int, hp int, strength int, intelligence int, dexterity int, wisdom int);' % (name,)

    elif name == 'charactercreator_character_inventory':
        query = 'CREATE TABLE IF NOT EXISTS %s (id SERIAL PRIMARY KEY, character_id int, item_id int);' % (name,)

    elif name == 'charactercreator_cleric':
        query = 'CREATE TABLE IF NOT EXISTS %s (character_ptr_id SERIAL PRIMARY KEY, using_shield int, mana int);' % (name,)

    elif name == 'charactercreator_fighter':
        query = 'CREATE TABLE IF NOT EXISTS %s (character_ptr_id SERIAL PRIMARY KEY, using_shield int, rage int);' % (name,)

    elif name == 'charactercreator_mage':
        query = 'CREATE TABLE IF NOT EXISTS %s (character_ptr_id SERIAL PRIMARY KEY, has_pet int, mana int);' % (name,)

    elif name == 'charactercreator_necromancer':
        query = 'CREATE TABLE IF NOT EXISTS %s (mage_ptr_id SERIAL PRIMARY KEY, talisman_charged int);' % (name,)

    elif name == 'charactercreator_thief':
        query = 'CREATE TABLE IF NOT EXISTS %s (character_ptr_id SERIAL PRIMARY KEY, is_sneaking int, energy int);' % (name,)

    else:
        break

    print("SQL:", query)
    cursor.execute(query)

for name in table_names:
    if name == 'armory_item':
        insertion_query = 'INSERT INTO armory_item (item_id, name, value, weight) VALUES %s;'
        execute_values(cursor, insertion_query, tuple_list[0])

    elif name == 'armory_weapon':
        insertion_query = 'INSERT INTO armory_weapon (item_ptr_id, power) VALUES %s;'
        execute_values(cursor, insertion_query, tuple_list[1])
   
    elif name == 'charactercreator_character':
        insertion_query = 'INSERT INTO charactercreator_character (character_id, name, level, exp, hp, strength, intelligence, dexterity, wisdom) VALUES %s;'
        execute_values(cursor, insertion_query, tuple_list[2])

    elif name == 'charactercreator_character_inventory':
        insertion_query = 'INSERT INTO charactercreator_character_inventory (id, character_id, item_id) VALUES %s;'
        execute_values(cursor, insertion_query, tuple_list[3])

    elif name == 'charactercreator_cleric':
        insertion_query = 'INSERT INTO charactercreator_cleric (character_ptr_id, using_shield, mana) VALUES %s;'
        execute_values(cursor, insertion_query, tuple_list[4])

    elif name == 'charactercreator_fighter':
        insertion_query = 'INSERT INTO charactercreator_fighter (character_ptr_id, using_shield, rage) VALUES %s;'
        execute_values(cursor, insertion_query, tuple_list[5])

    elif name == 'charactercreator_mage':
        insertion_query = 'INSERT INTO charactercreator_mage (character_ptr_id, has_pet, mana) VALUES %s;'
        execute_values(cursor, insertion_query, tuple_list[6])

    elif name == 'charactercreator_necromancer':
        insertion_query = 'INSERT INTO charactercreator_necromancer (mage_ptr_id, talisman_charged) VALUES %s;'
        execute_values(cursor, insertion_query, tuple_list[7])

    elif name == 'charactercreator_thief':
        insertion_query = 'INSERT INTO charactercreator_thief (character_ptr_id, is_sneaking, energy) VALUES %s;'
        execute_values(cursor, insertion_query, tuple_list[8])

    else:
        break

# --------------------- Titanic ------------------------#

titanic_file_path = DB_FILEPATH = os.path.join(os.path.dirname(__file__), "titanic.csv")

titanic_df = pd.read_csv(titanic_file_path)

titanic_tuples = list(titanic_df.itertuples(index=True, name=None))

table_creation_query = 'CREATE TABLE IF NOT EXISTS titanic (id SERIAL PRIMARY KEY, Survived int, Pclass int, Name varchar(120) NOT NULL, Sex varchar(40) NOT NULL, Age real, Siblings_Spouses_Aboard int, Parents_Children_Aboard int, Fare real);'
print("SQL:", table_creation_query)
cursor.execute(table_creation_query)

insertion_query = 'INSERT INTO titanic (id, Survived, Pclass, Name, Sex, Age, Siblings_Spouses_Aboard, Parents_Children_Aboard, Fare) VALUES %s;'
execute_values(cursor, insertion_query, titanic_tuples)

connection.commit()
cursor.close()
connection.close()