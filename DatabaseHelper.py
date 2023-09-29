import sqlite3


# Use it to do database operations
class DatabaseHelper:
    def __init__(self, database_name):
        self.database_name = database_name
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.database_name)
            print(f"Connected to database: {self.database_name}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print("Disconnected from the database")

    def execute_query(self, query, parameters=None):
        try:
            cursor = self.conn.cursor()
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
            self.conn.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None

    def create_table(self, table_name, schema):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})"
        self.execute_query(query)

    def insert_data(self, table_name, columns, values):
        placeholders = ",".join(["?"] * len(values))
        query = (
            f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"
        )
        self.execute_query(query, values)

    def delete_user_by_id(self, user_id, table_name):
        try:
            query = f"DELETE FROM {table_name} WHERE user_id = ?"
            cursor = self.conn.cursor()
            cursor.execute(query, (user_id,))
            self.conn.commit()
            return 1
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return -1

    def fetch_data(self, table_name, columns="*", condition=None, params=None):
        query = f"SELECT {columns} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        cursor = self.execute_query(query, params)
        if cursor:
            return cursor.fetchall()
        return None
