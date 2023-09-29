import sqlite3
from DatabaseHelper import DatabaseHelper


# User class
class User:
    def __init__(self, user_id=None, username=None, password=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.db_helper = DatabaseHelper("cntic_bot.db")
        self.db_helper.connect()

    # Rest of your code...

    def disconnect_user(self):
        self.db_helper.disconnect()

    def create_user(self):
        try:
            columns = ["user_id", "username", "password"]
            values = [self.user_id, self.username, self.password]
            self.db_helper.insert_data("users", columns, values)
            return True
        except sqlite3.Error as e:
            print(f"Error creating user: {e}")
            return False

    def get_user_by_id(self, user_id):
        try:
            query = "SELECT * FROM users WHERE user_id = ?"
            user = self.db_helper.execute_query(query, (user_id,)).fetchone()
            if user:
                user_id, username, password = user
                return {"user_id": user_id, "username": username, "password": password}
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error retrieving user by ID: {e}")
            return None

    def get_all_users(self):
        try:
            query = "SELECT * FROM users"
            users = self.db_helper.execute_query(query).fetchall()
            return users
        except sqlite3.Error as e:
            print(f"Error retrieving all users: {e}")
            return []

    def delete_user_by_id(self, user_id):
        try:
            return self.db_helper.delete_user_by_id(user_id, "users")
        except sqlite3.Error as e:
            print(f"Error deleting user by ID: {e}")
            return False

    def process_input(self, input_string: str):
        # Split the input string by ","
        parts = input_string.split(",")

        # Initialize username and password to None
        username = None
        password = None

        # Extract and assign username and password values
        for part in parts:
            key, value = part.split(":")
            if key == "username":
                username = value
            elif key == "password":
                password = value
        print("Username:", username)
        print("Password:", password)

        self.username = username
        self.password = password
        return self.create_user()


#   Testing code
# user = User(1, "john_doe", "password123")
# user = User()
# if user.create_user():
#     print("User created successfully")
# else:
#     print("Failed to create user")
# print(user.get_all_users())
# # user.delete_user_by_id(int(1))
# # print(user.get_user_by_id(1))
# # print("user:", user.get_all_users())
# # user.delete_user_by_id(1)
# # print("user:", user.get_all_users())
# user.disconnect_user()
# print("user:", user.get_all_users())
