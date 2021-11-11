import sqlite3
from sqlite3 import Error

class BeegData:

    def __init__(self):
        pass

    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            #print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection

    #   THIS IS FOR DITING DATABASES AND CREATING NEW TABLES ETC
    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            # print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    #   THIS IS FOR SELECT'S AND SEARCHES
    def execute_read_query(self, connection, query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    def add_row(self, connection, table, tuple):
        CMD = "INSERT INTO " + table + " VALUES " + tuple
        self.execute_query(connection, CMD)

    def display_query(self, table, connection):
        select = "SELECT * FROM " + table
        r = self.execute_read_query(connection, select)
        for e in r:
            print(e)

    #   if `keyword` is being included in the output, try adding a newline character to the end of the it
    def get_cmd(self, file, keyword):
        temp = open(file, "r")
        create_cmd = ""
        start_delay, switch = False, False
        for x in temp:
            if x == keyword:
                start_delay = True
            elif start_delay:
                switch = True
                start_delay = False
            if switch:
                if x == keyword:
                    break
                create_cmd += x
        temp.close()
        return create_cmd

    def rcf(self, files, keywords, connection):
        for file in files:
            for x in keywords:
                self.execute_query(connection, self.get_cmd(file, x))

    def display_all(self, tables, connection):
        for table in tables:
            self.display_query(table, connection)


