import sqlite3

conn = sqlite3.connect("cntic_bot.db")

cursor = conn.cursor()


cursor.execute(
    """CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    username TEXT,
                    password TEXT)"""
)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS files (
        file_id TEXT PRIMARY KEY,
        file_path BLOB,
        posting_time TIMESTAMP,
        option INTEGER,
        isposted BOOLEAN DEFAULT  0,
        user_id TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
"""
)


conn.commit()
conn.close()
