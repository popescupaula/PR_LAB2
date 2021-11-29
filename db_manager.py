import sqlite3
from sqlite3 import Error

class DataBaseManager:
    def __init__(self, db_path : str):
        '''
            The constructor of the Data Base Manager.
        :param db_path: str
            The pth to the data base file.
        '''
        try:
            self.conn = sqlite3.connect(db_path)
        except Error as e:
            print(e)

        self.cursor = self.conn.cursor()

        self.remainder_table_creation_query = '''CREATE TABLE IF NOT EXISTS remainders(
                                                 id integer PRIMARY KEY,
                                                 name text NOT NULL,
                                                 body text NOT NULL,
                                                 time text NOT NULL);'''

        self.task_table_creation_query = '''CREATE TABLE IF NOT EXISTS tasks(
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            body text NOT NULL,
                                            due_date text NOT NULL);'''

        self.remainder_insert_query = '''INSERT INTO remainders (name,
                                                                 body,
                                                                 time)
                                         VALUES (?, ?, ?)'''

        self.task_insert_query = '''INSERT INTO tasks (name,
                                                       body,
                                                       due_date)
                                    VALUES (?, ?, ?)'''

        self.cursor.execute(self.remainder_table_creation_query)
        self.cursor.execute(self.task_table_creation_query)
        self.conn.commit()

    def add_remainder(self, name, body, time):
        '''
            The remainder insertion function.
        :param name: str
            The name of the remainder.
        :param body: str
            The body of the remainder.
        :param time: str
            The time of the remainder.
        '''
        self.cursor.execute(self.remainder_insert_query, (name, body, time))
        self.conn.commit()

    def add_task(self, name, body, due_date):
        '''
            The task insertion function.
        :param name: str
            The name of the task.
        :param body: str
            The body of the task.
        :param due_date: str
            The due date and time of the task.
        '''
        self.cursor.execute(self.task_insert_query, (name, body, due_date))
        self.conn.commit()

    def close(self):
        '''
            This function closes the access to the data base.
        '''
        self.cursor.close()
        self.conn.close()
