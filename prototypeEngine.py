import random
from init_data import BeegData
from random import choices
import time

class Game():

    #   INITIALIZE CONNECTION AND DATABASES
    def __init__(self):
        #   GLOBALS
        self.rarities = ["'TRASH'", "'COMMON'", "'RARE'", "'ODD'", "'UNEARTHLY'"]
        self.junk_query = 'SELECT * FROM junk WHERE junk_rarity='
        self.junk_queries = []
        for r in self.rarities:
            self.junk_queries.append(self.junk_query + r)
        self.creature_query = 'SELECT * FROM creature WHERE creature_rarity='
        self.creature_queries = []
        for r in self.rarities:
            self.creature_queries.append(self.creature_query + r)
        # print(self.creature_queries)
        self.points = 0
        #   CREATE MATERIALS INDEX
        self.materials_keywords = ['rarity\n', 'junk\n', 'creature\n']
        self.materials_files = ["index/resetTables.txt", "index/createTables.txt", "index/materialsIndex.txt"]
        #       update these lists when creating new index
        self.materials_tables = ["rarity", "junk", "creature"]
        self.materials_tuples = ["rarity(obj_rarity,rate)", "junk(name, junk_rarity, point_value)",
                                 "creature(name, creature_rarity, point_value, purchase_item, purchase_cost)"]
        #   CREATE INVENTORY
        self.inv_keywords = ['junk\n', 'creature\n']
        self.inv_files = ["inventory/resetTables.txt", "inventory/createTables.txt"]
        #       update these when creating new 'pocket'
        self.inv_tables = ["junk", "creature"]
        self.inv_tuples = ["junk(name, junk_rarity, point_value, owned)", "creature(name, creature_rarity, point_value, owned)"]
        #   CREATE DATA OBJECT
        self.materials = BeegData()
        #   CONNECT TO DATABASE
        self.material_connection = self.materials.create_connection("materials.sqlite")
        #   RESET, CREATE, FILL
        self.materials.rcf(self.materials_files, self.materials_keywords, self.material_connection)
        #   DISPLAY
        # self.materials.display_all(self.materials_tables, self.material_connection)
        #   CREATE DATA OBJECT
        self.inventory = BeegData()
        #   CONNECT TO DATABASE
        self.inv_connection = self.inventory.create_connection("inventory.sqlite")
        #   RESET, CREATE, FILL
        self.inventory.rcf(self.inv_files, self.inv_keywords, self.inv_connection)
        # #   DISPLAY
        # self.inventory.display_all(inv_tables, inv_connection)

    def encounter(self):
        enc = ["nothing", "item", "creature", "event"]
        return choices(enc, weights=[75, 50, 15, 1], k=1)

    def determine_rarity(self):
        return choices(self.rarities, weights=[60, 35, 10, 2, 1], k=1)

    def determine_obj(self, obj):
        return obj[random.randrange(0, len(obj))]

    def get_objs(self, rarity, queries):
        if rarity[0] == "'TRASH'":
            return self.materials.execute_read_query(self.material_connection, queries[0])
        elif rarity[0] == "'COMMON'":
            return self.materials.execute_read_query(self.material_connection, queries[1])
        elif rarity[0] == "'RARE'":
            return self.materials.execute_read_query(self.material_connection, queries[2])
        elif rarity[0] == "'ODD'":
            return self.materials.execute_read_query(self.material_connection, queries[3])
        elif rarity[0] == "'UNEARTHLY'":
            return self.materials.execute_read_query(self.material_connection, queries[4])

    def show_dialogues(self, file, n, object):
        find_text = BeegData.get_cmd(BeegData, file, str(random.randrange(1, n+1)) + "\n").split("^")
        shown_text = ""
        l = len(find_text)
        for i in range(l):
            if i == l - 1:
                shown_text += find_text[i]
            else:
                shown_text += (find_text[i] + object[1])
        print(shown_text)

    def add_obj(self, obj):
        query = "SELECT name FROM junk WHERE name='" + str(obj[1] + "'")
        check = self.inventory.execute_read_query(self.inv_connection, query)
        if not check:
            self.inventory.add_row(self.inv_connection, self.inv_tuples[0],
                                   "('" + str(obj[1]) + "', '" + str(obj[2]) + "', " + str(
                                       obj[3]) + ", " + "1" + ")")
        else:
            in_possession = self.inventory.execute_read_query(self.inv_connection,
                                                              "SELECT owned FROM junk WHERE name = '" + str(
                                                                  check[0][0]) + "'")
            update = "UPDATE junk SET owned = " + str(in_possession[0][0] + 1) + " WHERE name = '" + str(
                check[0][0]) + "'"
            self.inventory.execute_query(self.inv_connection, update)
        self.points += obj[3]

    def do_nothing(self):
        print(BeegData.get_cmd(BeegData, "Dialogues/nothing.txt", str(random.randrange(1, 10)) + "\n"))

    def do_menu(self):
        print("-----========MENU=======-----")
        print(
            """
Simply Press the `Enter` key to advance on your walk
`quit`  - Quit the game
`inv`   - Check Inventory
`score` - Check Current Score
            """
        )
        print("-----===================-----")

    def do_score(self):
        print("-----========SCORE=======-----")
        print("           ", self.points)
        print("-----====================-----")

    def do_item(self):
        item = self.determine_obj(self.get_objs(self.determine_rarity(), self.junk_queries))
        self.show_dialogues("Dialogues/getItem.txt", 8, item)
        #   I want to heck if the item I've aquired already exists in my inventory
        self.add_obj(item)

    def do_creature(self):
        rarity = self.determine_rarity()
        creatures = self.get_objs(rarity, self.creature_queries)
        creature_enc = self.determine_obj(creatures)
        #   IF COST THEN GO INTO `feed.txt`; ELSE GO INTO `adopt.txt`
        # creature_enc = ('SQUIRREL', 'COMMON', 24, 'ACORN', 6)
        # for i in range(6):
        #     self.add_obj((4, 'ACORN', 'TRASH', 4))
        # self.show_inv()
        if creature_enc[4] == None:
            self.adopt(creature_enc)
        else:
            self.feed(creature_enc)

    def adopt(self, creature):
        self.show_dialogues("Dialogues/adopt.txt", 5, creature)
        self.add_obj(creature)

    def feed(self, creature):
        find_text = BeegData.get_cmd(BeegData, "Dialogues/feed.txt", str(random.randrange(1, 8)) + "\n")
        splits = 0
        for char in find_text:
            if char == "^":
                splits += 1
        find_text = find_text.split("^")
        shown_text = ""
        l = len(find_text)
        for i in range(l):
            if i == l - 1:
                shown_text += find_text[i]
            else:
                if splits == 1:
                    shown_text += (find_text[i] + creature[4] + " (X " + str(creature[5]) + ")")
                else:
                    shown_text += (find_text[i] + creature[1])
            splits -= 1
        choice = input(shown_text)
        quit = False
        while not quit:
            if choice == 'y':
                feed_check = "SELECT owned FROM junk WHERE name='" + str(creature[4]) + "'"
                amount_owned = self.inventory.execute_read_query(self.inv_connection, feed_check)
                feed_required = creature[5]
                if not amount_owned or amount_owned[0][0] < feed_required:
                    print("You don't have enough " + creature[4] + "'s")
                    quit = True
                else:
                    query = "SELECT * FROM creature WHERE name='" + str(creature[1]) + "'"
                    check = self.inventory.execute_read_query(self.inv_connection, query)
                    #   Subtracts the feed cost from inventory
                    print(creature[1] + " has been tamed!")
                    subtract = "UPDATE junk SET owned = " + str(amount_owned[0][0] - feed_required) + " WHERE name = '" + creature[
                        4] + "'"
                    self.inventory.execute_read_query(self.inv_connection, subtract)
                    if not check:
                        self.inventory.add_row(self.inv_connection, self.inv_tuples[1],
                                               "('" + str(creature[1]) + "', '" + str(creature[2]) + "', " + str(
                                                   creature[3]) + ", " + "1" + ")")
                    else:
                        update = "UPDATE creature SET owned = " + str(check[0][3] + 1) + " WHERE name = '" + str(
                            check[0][0]) + "'"
                        self.inventory.execute_query(self.inv_connection, update)
                    self.points += creature[3]
                    quit = True
            elif choice == 'n':
                quit = True
            else:
                choice = input("Invalid input, type `y` or `n`\n")

    def do_event(self):
        pass


    def calc_filler_text(self, item_name):
        filler = ""
        for i in range(23+3-len(item_name)):
            filler += " "
        return filler

    def show_inv(self):
        print("-----========INVENTORY=======-----")
        for table in self.inv_tables:
            items = self.inventory.execute_read_query(self.inv_connection, "SELECT * FROM " + table)
            for thing in items:
                print(thing[0] + self.calc_filler_text(thing[0]) + "   " + "X", thing[3])
        print("-----========================-----")

    def play(self):
        print("Welcome to Walking Simulator 2077.69 Sigma Male Grindset Edition")
        print("type `quit` to quit, `menu` to see more options")
        while True:
            player_input = input()
            #   DETERMINE ENCOUNTER TYPE
            enc = self.encounter()[0]
            if player_input == "quit":
                break
            elif player_input == "menu":
                self.do_menu()
            elif player_input == "inv":
                self.show_inv()
            elif player_input == "score":
                self.do_score()
            elif enc == "nothing":
                self.do_nothing()
            elif enc == "item":
                self.do_item()
            elif enc == "creature":
                self.do_creature()
            elif enc == "event":
                pass


game = Game()

game.play()
# for i in range(2):
#     game.do_creature()
# game.do_creature()
# game.do_item()
# game.show_inv()
# game.do_score()
# while True:
#     game.do_item()