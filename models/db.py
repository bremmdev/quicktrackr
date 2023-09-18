import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.conn.execute('PRAGMA foreign_keys = ON;')

    def get_connection(self):
        return self.conn
