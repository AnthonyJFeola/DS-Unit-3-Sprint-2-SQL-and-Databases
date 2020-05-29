# SQLite3

import os
import sqlite3
import pymongo
import pandas as pd
import os
from dotenv import load_dotenv


DB_FILEPATH = os.path.join(os.path.dirname(__file__), "rpg_db.sqlite3")

connection = sqlite3.connect(DB_FILEPATH)
print("CONNECTION:", connection)

cursor = connection.cursor()
print("CURSOR", cursor)

table_names = ['armory_item', 'armory_weapon', 'charactercreator_character',
'charactercreator_character_inventory', 'charactercreator_cleric', 'charactercreator_fighter',
'charactercreator_mage', 'charactercreator_necromancer', 'charactercreator_thief']

query_list = []

dict_list = []

for name in table_names:
    query = 'SELECT * FROM %s' % (name,)
    query_list.append(query)

for query in query_list:
    data = cursor.execute(query).fetchall()
    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
    table = pd.DataFrame(data, columns=field_names)
    table_dict = table.to_dict('records')
    dict_list.append(table_dict)

#--------------------------------------------------------------------#

# MongoDB

load_dotenv()

DB_USER = os.getenv("MONGO_USER", default="OOPS")
DB_PASSWORD = os.getenv("MONGO_PASSWORD", default="OOPS")
CLUSTER_NAME = os.getenv("MONGO_CLUSTER_NAME", default="OOPS")

connection_uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{CLUSTER_NAME}.mongodb.net/test?retryWrites=true&w=majority"
print("----------------")
print("URI:", connection_uri)

client = pymongo.MongoClient(connection_uri)
print("----------------")
print("CLIENT:", type(client), client)

db = client.rpg_db # "test_database" or whatever you want to call it
print("----------------")
print("DB:", type(db), db)

collection = db.rpg_collection # "pokemon_test" or whatever you want to call it
print("----------------")
print("COLLECTION:", type(collection), collection)

print("----------------")
print("COLLECTIONS:")
print(db.list_collection_names())

for element in dict_list:
    collection.insert_many(element)

print("DOCS:", collection.count_documents({}))
print(collection.count_documents({"name": "RPG"}))