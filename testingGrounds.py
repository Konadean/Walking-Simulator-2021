import random
from init_data import BeegData
# a = str(random.randrange(1, 7)) + "\n"
# print(a)
#
# print(BeegData.get_cmd(BeegData, "Dialogues/nothing.txt", a))

# materials_keywords = ['rarity\n', 'junk\n', 'creature\n']
# materials_files = ["index/resetTables.txt", "index/createTables.txt", "index/materialsIndex.txt"]
# #       update these lists when creating new index
# materials_tables = ["rarity", "junk", "creature"]
#
#
# #   CREATE DATA OBJECT
# materials = BeegData()
# #   CONNECT TO DATABASE
# material_connection = materials.create_connection("materials.sqlite")
# #   RESET, CREATE, FILL
# materials.rcf(materials_files, materials_keywords, material_connection)
#
# print(materials.execute_read_query(material_connection, "SELECT name FROM junk WHERE name='STICK'")[0][0])


#   CREATE INVENTORY
inv_keywords = ['junk\n', 'creature\n']
inv_files = ["inventory/resetTables.txt", "inventory/createTables.txt"]
#       update these when creating new 'pocket'
inv_tables = []
inv_tuples = ["junk(name, junk_rarity, point_value, owned)", "creature(name, creature_rarity, point_value, owned)"]

#   CREATE DATA OBJECT
inventory = BeegData()
#   CONNECT TO DATABASE
inv_connection = inventory.create_connection("inventory.sqlite")
#   RESET, CREATE, FILL
inventory.rcf(inv_files, inv_keywords, inv_connection)
# #   DISPLAY
inventory.display_all(inv_tables, inv_connection)

inventory.add_row(inv_tuples[0], ())

