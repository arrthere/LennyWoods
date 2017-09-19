import sqlite3

class Sqyler:

    def __init__(self, name):
        self.connector = sqlite3.connect(name)

    def start(self):
        self.cursor = self.connector.cursor()

    def create_table(self, table_name, columns):
        data = []
        for key in columns.keys():
            data.append(key + ' ' + columns[key])

        data = ', '.join(data)
        command = 'CREATE TABLE {} ({})'.format(table_name, data)
        print(command)
        self.cursor.execute(command)

    def insert(self, table_name, values):
        data = []
        for value in values:
            data.append('\'' + str(value) + '\'')


        data = ', '.join(data)

        command = 'INSERT INTO {} VALUES ({})'.format(table_name, data)
        print(command)
        self.cursor.execute(command)

    def select(self, table_name, key, value):
        command = 'SELECT * FROM {} WHERE {} = ?'.format(table_name, key)
        self.cursor.execute(command, (value, ))

    def update(self, table_name, key, value, search_key, search_value):
        command = 'UPDATE {} SET {} = ? WHERE {} = ?'.format(table_name, key, search_key)
        print(command)
        self.cursor.execute(command, (value, search_value))

    def fetchone(self):
        return self.cursor.fetchone()


    def save(self):
        self.connector.commit()

    def close(self):
        self.connector.close()
