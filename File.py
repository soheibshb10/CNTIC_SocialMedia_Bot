import sqlite3
from DatabaseHelper import DatabaseHelper
from User import User


# File class
class File:
    def __init__(
        self,
        file_id=None,
        file_path=None,
        posting_time=None,
        option=None,
        user_id=None,
        isposted=0,
    ):
        self.file_id = file_id
        self.file_path = file_path
        self.posting_time = posting_time
        self.option = option
        self.user_id = user_id
        self.isposted = isposted
        self.db_helper = DatabaseHelper(
            "cntic_bot.db"
        )  # Initialize the DatabaseHelper instance
        self.db_helper.connect()

    def create_file(self):
        user = User()
        if user.get_user_by_id(self.user_id):
            try:  # Use the DatabaseHelper instance to perform database operations
                columns = [
                    "file_id",
                    "file_path",
                    "posting_time",
                    "option",
                    "isposted",
                    "user_id",
                ]
                values = [
                    self.file_id,
                    self.file_path,
                    self.posting_time,
                    self.option,
                    self.isposted,
                    self.user_id,
                ]

                # Assuming you have a 'users' table, you can insert data like this
                self.db_helper.insert_data("files", columns, values)
                print("file created succesfuly")
                return True

                # You can also execute other database operations using self.db_helper
            except sqlite3.Error as e:
                print(f"Error creating file: {e}")
                return False
        else:
            print(f"user with{self.user_id} does not existed ")
            return False

    def get_all_files(self):
        try:
            query = "SELECT * FROM files"
            users = self.db_helper.execute_query(query).fetchall()
            return users
        except sqlite3.Error as e:
            print(f"Error retrieving all users: {e}")
            return []

    def get_user_files(self, user_id):
        try:
            query = """ SELECT  files.file_id,files.file_path, files.posting_time, files.option,files.isposted
            FROM files
            JOIN users ON files.user_id = users.user_id
            WHERE users.user_id = ?"""
            user_files = self.db_helper.execute_query(query, (user_id,)).fetchall()
            return user_files
        except Exception as e:
            print(f"Error retrieving user files: {e}")
            return []

    def changePostType(self, file_id):
        try:
            query = """UPDATE files SET isposted = 1 WHERE file_id = ?"""
            if self.db_helper.execute_query(query, (file_id,)):
                print("status was changed successfully")
                return 1
        except Exception as e:
            print(f"Error changing post type: {e}")
            return 0

    def delete_All_files(self, user_id):
        try:
            query = """DELETE FROM files 
                   WHERE user_id = ?"""
            self.db_helper.execute_query(query, (user_id,))
            return True
        except Exception as e:
            print(f"Error deleting user files: {e}")
            return False

    def delete_file(self, file_id):
        try:
            query = "DELETE FROM files WHERE file_id = ?"
            self.db_helper.execute_query(query, (file_id,))
            return True
        except Exception as e:
            print(f"Error deleting this file: {e}")
            return False

    def disconnect_file(self):
        self.db_helper.disconnect()


with open("test.jpg", "rb") as pct:
    file_data = pct.read()
file = File(112, file_data, "2023-28-09 11:05", 1, 1)

if file.create_file() == True:
    print("File created successfully")
else:
    print("Failed to create file")

# Assuming you have implemented these methods in your File class
# file=File(112,)
# user_files = file.get_user_files(1)
# if user_files:
#     print("User files:")
#     for user_file in user_files:
#         print(user_file)
# else:
#     print("Failed to retrieve user files")

# Assuming you have implemented a method like this to delete a file by its ID
# if file.delete_file(112):
#     print("File deleted successfully")
# else:
#     print("Failed to delete file")
# file = File()

# if file.delete_All_files("1"):
#     print("we  deleted all files successfully")
# else:
#     print("Failed to delete files")

# file = File()
# user_files = file.get_all_files()
# print(user_files)
# if user_files:
#     print("User files:")
#     for user_file in user_files:
#         print(user_file)
# else:
#     print("Failed to retrieve user files")
