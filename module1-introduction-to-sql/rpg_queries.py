import os
import sqlite3

DB_FILEPATH = os.path.join(os.path.dirname(__file__), "rpg_db.sqlite3")

connection = sqlite3.connect(DB_FILEPATH)
print("CONNECTION:", connection)

cursor = connection.cursor()
print("CURSOR", cursor)

query1 = """
SELECT
	count(DISTINCT character_id) as character_count
FROM charactercreator_character
"""

query2 = """
SELECT
	count(DISTINCT character_ptr_id) as cleric_count
FROM charactercreator_cleric
"""

query3 = """
SELECT
	count(DISTINCT character_ptr_id) as fighter_count
FROM charactercreator_fighter
"""

query4 = """
SELECT
	count(DISTINCT mage_ptr_id) as necro_count
FROM
(SELECT *
FROM charactercreator_mage
JOIN charactercreator_necromancer ON charactercreator_mage.character_ptr_id = charactercreator_necromancer.mage_ptr_id)
"""

query5 = """
SELECT
	count(DISTINCT character_ptr_id) as mage_count
FROM
(SELECT *
FROM charactercreator_mage
LEFT JOIN charactercreator_necromancer ON charactercreator_mage.character_ptr_id = charactercreator_necromancer.mage_ptr_id)
"""

query6 = """
SELECT
	count(DISTINCT character_ptr_id) as thief_count
FROM charactercreator_thief
"""

query7 = """
SELECT
	count(DISTINCT item_id) as item_count
FROM armory_item
"""

query8 = """
SELECT
	count(DISTINCT item_ptr_id) as weapon_count
FROM
(SELECT *
FROM armory_item
JOIN armory_weapon ON armory_item.item_id = armory_weapon.item_ptr_id)
"""

query9 = """
SELECT
	count(DISTINCT item_id) as non_weapon_count
FROM
(SELECT *
FROM armory_item
LEFT JOIN armory_weapon ON armory_item.item_id = armory_weapon.item_ptr_id
WHERE item_ptr_id IS NULL)
"""

query10 = """
SELECT
	count(character_id) as items_per_character
FROM charactercreator_character_inventory
GROUP BY character_id
LIMIT 20
"""

query11 = """
SELECT
	charactercreator_character.character_id,
	charactercreator_character.name,
	count(DISTINCT item_ptr_id) as weapons
FROM charactercreator_character
LEFT JOIN charactercreator_character_inventory ON charactercreator_character.character_id = charactercreator_character_inventory.character_id
LEFT JOIN armory_weapon ON armory_weapon.item_ptr_id = charactercreator_character_inventory.item_id
GROUP BY charactercreator_character.character_id
LIMIT 20
"""

query12 = """
SELECT avg(items_per_character) as average_items_per_character
FROM (

SELECT
	count(character_id) as items_per_character
FROM charactercreator_character_inventory
GROUP BY character_id)
"""

query13 = """
SELECT avg(weapons) as average_weapons_per_character
FROM (
SELECT
	charactercreator_character.character_id,
	charactercreator_character.name,
	count(DISTINCT item_ptr_id) as weapons
FROM charactercreator_character
LEFT JOIN charactercreator_character_inventory ON charactercreator_character.character_id = charactercreator_character_inventory.character_id
LEFT JOIN armory_weapon ON armory_weapon.item_ptr_id = charactercreator_character_inventory.item_id
GROUP BY charactercreator_character.character_id)
"""


result1 = cursor.execute(query1).fetchall()
print("RESULT 1", result1)

result2 = cursor.execute(query2).fetchall()
print("RESULT 2", result2)

result3 = cursor.execute(query3).fetchall()
print("RESULT 3", result3)

result4 = cursor.execute(query4).fetchall()
print("RESULT 4", result4)

result5 = cursor.execute(query5).fetchall()
print("RESULT 5", result5)

result6 = cursor.execute(query6).fetchall()
print("RESULT 6", result6)

result7 = cursor.execute(query7).fetchall()
print("RESULT 7", result7)

result8 = cursor.execute(query8).fetchall()
print("RESULT 8", result8)

result9 = cursor.execute(query9).fetchall()
print("RESULT 9", result9)

result10 = cursor.execute(query10).fetchall()
print("RESULT 10", result10)

result11 = cursor.execute(query11).fetchall()
print("RESULT 11", result11)

result12 = cursor.execute(query12).fetchall()
print("RESULT 12", result12)

result13 = cursor.execute(query13).fetchall()
print("RESULT 13", result13)
